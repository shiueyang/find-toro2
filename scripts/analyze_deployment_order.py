"""
用 Space-Track 歷史 TLE 檢驗「未識別物件 <-> 部署時序」的對應（GCAT 識別法的獨立重現）

原理：Transporter 任務所有酬載由同一枚二級在幾乎同一軌道上、依固定時程逐顆彈出，分離時間差與
分離 Δv（~1 m/s）決定「部署當下」的沿軌相位差（只有幾度）。但公開根數從部署後第 20 天
（2025-12-18）才開始，此時差異阻力 / 半長軸差造成的相位漂移已達 ±140 度，直接看相位順序看不出部署順序。

因此本腳本做兩件事：
  1. 取兩個共同歷元 T1、T2（皆在有資料的區間內），用 SGP4 算每個物件的沿軌角 u，
     得到相位漂移率 rate = (u(T2) - u(T1)) / (T2 - T1)。
  2. 把相位線性回推到部署時刻 T0：u0 = u(T1) - rate * (T1 - T0)。
     回推後的相位 u0 應與 GCAT 的分離時刻高度相關（Spearman ρ）。
  最後看目前仍未識別的物件（Celestrak 名稱 OBJECT xx）落在回推相位序列的哪裡，
  並用「已識別物件的 u0 vs 分離時刻」線性擬合，反推每個未識別物件的「推定分離時刻」，
  與 GCAT 指派的名字（及其分離時刻）比對。

輸入：data/raw/spacetrack_gp_history_2025-276.tle（fetch_spacetrack_history.py 產生）
      data/raw/gcat_satcat_2025-276.tsv、data/raw/celestrak_2025-276_tle.txt（目前名稱）
輸出：results/deployment_order_check.csv / .md

用法：python scripts/analyze_deployment_order.py [--t1 2025-12-19T00:00:00] [--t2 2026-01-08T00:00:00]
"""
import argparse, csv, datetime as dt, math, os, re, sys
import numpy as np
from sgp4.api import Satrec, jday

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, RES = os.path.join(ROOT, "data", "raw"), os.path.join(ROOT, "results")
INTDES = "2025-276"
T0 = dt.datetime(2025, 11, 28, 19, 40, 0)        # 部署開始（TORO-2 19:39:09，最後一顆 ~20:10）
GCAT_HEADER = ("JCAT Satcat Launch_Tag Piece Type Name PLName LDate Parent SDate Primary DDate Status Dest Owner State "
               "Manufacturer Bus Motor Mass MassFlag DryMass DryFlag TotMass TotFlag Length LFlag Diameter DFlag Span "
               "SpanFlag Shape ODate Perigee PF Apogee AF Inc IF OpOrbit OQUAL AltNames").split()


def load_history(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
    hist = {}
    for i in range(0, len(lines), 3):
        l1, l2 = lines[i + 1], lines[i + 2]
        s = Satrec.twoline2rv(l1, l2)
        hist.setdefault(int(l1[2:7]), []).append((s.jdsatepoch + s.jdsatepochF, l1, l2))
    # 剔除交叉標記 / 發散的根數（B* 非正或過大、偏心率或半長軸偏離該物件中位數太多），
    # 例：OBJECT H 2025-12-24~29 有一段高度亂跳、B* 正負互換的壞根數
    for n, sets in hist.items():
        if len(sets) < 4:
            continue
        sr = [Satrec.twoline2rv(l1, l2) for _, l1, l2 in sets]
        e = np.array([s.ecco for s in sr]); b = np.array([s.bstar for s in sr])
        a_ = np.array([(398600.4418 / (s.no_kozai / 60) ** 2) ** (1 / 3) for s in sr])
        e_med, a_med = np.median(e), np.median(a_)
        mad_a = np.median(np.abs(a_ - a_med)) or 0.3
        keep = (b > 0) & (b < 0.01) & (np.abs(e - e_med) < 4 * max(e_med, 1e-4)) & (np.abs(a_ - a_med) < 6 * mad_a + 1.0)
        hist[n] = [w for w, k in zip(sets, keep) if k]
    return hist


def load_gcat():
    rows = open(os.path.join(RAW, f"gcat_satcat_{INTDES}.tsv"), encoding="utf-8").read().splitlines()
    hdr = GCAT_HEADER
    if rows and rows[0].startswith("#JCAT"):
        hdr, rows = rows[0].lstrip("#").split("\t"), rows[1:]
    out = {}
    for l in rows:
        r = dict(zip(hdr, l.split("\t")))
        m = re.match(r"S(\d+)", r.get("JCAT", ""))
        if not m:
            continue
        sep = None
        m2 = re.match(r"(\d{4}) (\w{3}) (\d+) (\d{2})(\d{2}):(\d{2})", r["SDate"].strip())
        if m2:
            sep = dt.datetime.strptime(" ".join(m2.groups()[:3]), "%Y %b %d").replace(
                hour=int(m2[4]), minute=int(m2[5]), second=int(m2[6]))
        def num(x):
            try: return float(x)
            except ValueError: return None
        out[int(m[1])] = dict(gcat_name=r["Name"].strip(), sep=sep, piece=r["Piece"].strip().replace(INTDES, ""),
                              mass=num(r["Mass"]), length=num(r["Length"]))
    return out


def load_current_names():
    lines = [l.rstrip("\n") for l in open(os.path.join(RAW, f"celestrak_{INTDES}_tle.txt"), encoding="utf-8") if l.strip()]
    return {int(lines[i + 1][2:7]): lines[i].strip() for i in range(0, len(lines), 3)}


def state_at(hist_sets, T):
    """取離 T 最近的 TLE，SGP4 傳播到 T，回傳 (沿軌角 deg, a km, |epoch-T| 小時)"""
    jd, fr = jday(T.year, T.month, T.day, T.hour, T.minute, T.second)
    ep, l1, l2 = min(hist_sets, key=lambda s: abs(s[0] - (jd + fr)))
    s = Satrec.twoline2rv(l1, l2)
    e, r, v = s.sgp4(jd, fr)
    if e:
        return None
    r, v = np.array(r), np.array(v)
    h = np.cross(r, v)
    n = np.cross([0.0, 0.0, 1.0], h)
    u = math.degrees(math.atan2(np.dot(np.cross(n, r), h) / np.linalg.norm(h), np.dot(n, r))) % 360.0
    a = (398600.4418 / (s.no_kozai / 60.0) ** 2) ** (1 / 3)
    return u, a, abs(ep - (jd + fr)) * 24


def wrap(x):
    return (x + 180.0) % 360.0 - 180.0


def spearman(x, y):
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1]) if len(x) > 2 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", default="2025-12-19T00:00:00")
    ap.add_argument("--t2", default="2026-01-08T00:00:00")
    ap.add_argument("--step", type=float, default=2.0, help="取樣間隔（天）")
    ap.add_argument("--fit", choices=["lin", "quad"], default="lin",
                    help="相位外推用的多項式階數（quad 往前外推 20 天會發散，僅供比較）")
    a = ap.parse_args()
    hpath = os.path.join(RAW, f"spacetrack_gp_history_{INTDES}.tle")
    if not os.path.exists(hpath):
        sys.exit("找不到歷史 TLE，請先用自己的帳號執行 scripts/fetch_spacetrack_history.py")
    hist, gcat, cur = load_history(hpath), load_gcat(), load_current_names()
    T1, T2 = dt.datetime.fromisoformat(a.t1), dt.datetime.fromisoformat(a.t2)
    days12 = (T2 - T1).total_seconds() / 86400
    days01 = (T1 - T0).total_seconds() / 86400

    # 在 T1..T2 之間每 step 天取樣一次相位（SGP4），之後對「相對參考物件的相位」做二次多項式擬合再外推到 T0
    samples = [T1 + dt.timedelta(days=d) for d in np.arange(0, days12 + 1e-6, a.step)]
    recs = []
    for norad, sets in hist.items():
        st = [state_at(sets, T) for T in samples]
        if any(s is None or s[2] > 48 for s in st):
            continue
        g = gcat.get(norad, {})
        name = cur.get(norad, "(no current TLE)")
        recs.append(dict(norad=norad, name=name, piece=g.get("piece", "?"), gcat_name=g.get("gcat_name", "?"),
                         sep=g.get("sep"), mass=g.get("mass"), length=g.get("length"),
                         us=np.array([s[0] for s in st]), u1=st[0][0], u2=st[-1][0], a1=st[0][1], a2=st[-1][1],
                         unknown=bool(re.search(r"OBJECT [A-Z]+$|TBA", name))))
    if not recs:
        sys.exit("歷史 TLE 檔是空的或無法傳播")

    # 以半長軸中位數者為參考物件（漂移最接近群體中心，避免 ±180 纏繞）；
    # 只從「已識別、目前仍有 TLE」的物件挑，避免選到已再入的 W-5 或會機動的物件
    a_med = float(np.median([r["a1"] for r in recs]))
    pool = [r for r in recs if not r["unknown"] and r["norad"] in cur] or recs
    ref = min(pool, key=lambda r: abs(r["a1"] - a_med))
    tdays = np.array([(T - T0).total_seconds() / 86400 for T in samples])
    for r in recs:
        rel = np.array([wrap(x) for x in (r["us"] - ref["us"])])
        rel = np.degrees(np.unwrap(np.radians(rel)))                 # 連續化
        r["rel1"] = float(rel[0])
        deg = 2 if a.fit == "quad" and len(rel) >= 4 else 1
        p = np.polyfit(tdays, rel, deg)
        r["rate"] = float(np.polyval(np.polyder(p), tdays[0]))       # T1 當下的相對漂移率 deg/day
        r["u0"] = float(np.polyval(p, 0.0))                          # 外推到部署時刻 T0
        r["fit_rms"] = float(np.sqrt(np.mean((np.polyval(p, tdays) - rel) ** 2)))
        r["outlier"] = abs(r["a1"] - a_med) > 10 or abs(r["rate"]) > 15   # FORMOSAT-8A 抬軌等
    u0_med = float(np.median([r["u0"] for r in recs if not r["outlier"]]))
    for r in recs:
        r["u0"] -= u0_med
    recs.sort(key=lambda r: r["u0"])

    # 已識別、有分離時刻、非離群者 -> 相關與線性擬合 u0 = k * (sep - T0) + c
    fit = [r for r in recs if not r["unknown"] and r["sep"] and not r["outlier"]]
    ts = np.array([(r["sep"] - T0).total_seconds() / 60 for r in fit])       # 分離時刻（min after T0）
    us = np.array([r["u0"] for r in fit])
    rho_raw = spearman(ts, np.array([r["rel1"] for r in fit]))
    rho_back = spearman(ts, us)
    k, c = np.polyfit(ts, us, 1)
    resid = us - (k * ts + c)
    sigma = float(np.std(resid))
    for r in recs:
        r["pred_sep_min"] = (r["u0"] - c) / k if k else float("nan")
        r["pred_sep"] = T0 + dt.timedelta(minutes=float(r["pred_sep_min"]))
        r["gcat_sep_resid_deg"] = (r["u0"] - (k * (r["sep"] - T0).total_seconds() / 60 + c)) if r["sep"] else None

    os.makedirs(RES, exist_ok=True)
    cols = ["u0", "rel1", "rate", "a1", "norad", "piece", "name", "gcat_name", "sep", "pred_sep", "gcat_sep_resid_deg",
            "mass", "length", "unknown", "outlier"]
    with open(os.path.join(RES, "deployment_order_check.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in recs:
            w.writerow({**r, "sep": r["sep"].isoformat() if r["sep"] else "", "pred_sep": r["pred_sep"].isoformat(timespec="seconds")})

    unk = [r for r in recs if r["unknown"] and not r["outlier"]]
    H = next((r for r in recs if r["norad"] == 66673), None)
    md = [f"# 部署時序 vs 回推相位（T1={T1:%Y-%m-%d}, T2={T2:%Y-%m-%d}，回推到 {T0:%Y-%m-%d %H:%M} UTC）\n",
          f"- 物件數 {len(recs)}（含 {len(unk)} 個目前仍未識別），擬合用已識別物件 {len(fit)} 個，參考物件 {ref['name']} ({ref['norad']})。",
          f"- 直接用 T1 相位 vs 分離時刻：Spearman ρ = {rho_raw:.3f}（差異漂移已把部署順序洗掉）。",
          f"- **回推到部署時刻後：Spearman ρ = {rho_back:.3f}**，線性擬合 u0 = {k:.3f}°/min × (分離時刻) + {c:.2f}°，殘差 σ = {sigma:.1f}°。",
          ""]
    if H:
        neigh = sorted(recs, key=lambda r: abs(r["u0"] - H["u0"]))[1:7]
        md += ["## OBJECT H（NORAD 66673）\n",
               f"- 回推相位 u0 = {H['u0']:+.1f}°，由擬合反推的分離時刻 ≈ **{H['pred_sep']:%H:%M:%S} UTC**；"
               f"GCAT 指派 TORO2 的分離時刻 19:39:09，殘差 {H['gcat_sep_resid_deg']:+.1f}°（σ = {sigma:.1f}°）。",
               "- 相位最接近的鄰居：" + "、".join(f"{r['gcat_name']}({r['sep']:%H:%M:%S})" if r["sep"] else r["gcat_name"] for r in neigh) + "。",
               ""]
    # 衰減率（半長軸變化 km/day）：與相位無關的獨立物理量，可比較未識別物件與各已知等級
    for r in recs:
        r["da_dt"] = (r["a2"] - r["a1"]) / days12
    def cls(r):
        m, L = r["mass"], r["length"] or 0
        if m is None: return "?"
        if 10 <= m <= 25 and L >= 0.35: return "8U級 (10-25 kg, L>=0.35 m)"
        if 10 <= m <= 25: return "6U級 (10-25 kg, L~0.3 m)"
        if 4 <= m < 10: return "3U級 (4-10 kg)"
        if m < 4: return "1U/PocketQube (<4 kg)"
        return "大型 (>25 kg)"
    groups = {}
    for r in recs:
        if not r["unknown"] and not r["outlier"]:
            groups.setdefault(cls(r), []).append(r["da_dt"])
    md += ["## 半長軸衰減率（T1→T2，km/day；越負 = 阻力越大）\n",
           "| 等級（已識別物件） | n | 中位數 | 最小 | 最大 |", "|--|--|--|--|--|"]
    for k in sorted(groups):
        v = groups[k]
        md.append(f"| {k} | {len(v)} | {np.median(v):.4f} | {min(v):.4f} | {max(v):.4f} |")
    md += ["", "| 未識別物件 | GCAT 推定 | 質量 kg | da/dt km/day | 對應等級中位數 |", "|--|--|--|--|--|"]
    for r in sorted(unk, key=lambda r: r["da_dt"]):
        g = groups.get(cls(r), [])
        md.append(f"| {r['name']} ({r['norad']}) | {r['gcat_name']} | {r['mass']} | {r['da_dt']:.4f} | "
                  f"{np.median(g):.4f} ({cls(r)}) |" if g else
                  f"| {r['name']} ({r['norad']}) | {r['gcat_name']} | {r['mass']} | {r['da_dt']:.4f} | — |")
    md.append("")
    md += ["## 目前仍未識別物件的回推相位與推定分離時刻\n",
           "| NORAD | Celestrak | GCAT 推定 (分離時刻) | 質量 kg | u0 (deg) | 推定分離時刻 | 殘差 vs GCAT (deg) | 8U級? |",
           "|--|--|--|--|--|--|--|--|"]
    for r in sorted(unk, key=lambda r: r["u0"]):
        is8u = r["mass"] is not None and 10 <= r["mass"] <= 25 and (r["length"] or 0) >= 0.35
        md.append(f"| {r['norad']} | {r['name']} | {r['gcat_name']} ({r['sep']:%H:%M:%S}) | {r['mass']} | {r['u0']:+.1f} | "
                  f"{r['pred_sep']:%H:%M:%S} | {r['gcat_sep_resid_deg']:+.1f} | {'**是**' if is8u else ''} |"
                  if r["sep"] else f"| {r['norad']} | {r['name']} | {r['gcat_name']} | {r['mass']} | {r['u0']:+.1f} | {r['pred_sep']:%H:%M:%S} | — | |")
    md += ["", "## 全部物件（依回推相位排序）\n",
           "| u0 (deg) | T1 相位 | 漂移 °/day | a(T1) km | NORAD | Celestrak 名稱 | GCAT 推定 | 分離 (UTC) | 推定分離 |",
           "|--|--|--|--|--|--|--|--|--|"]
    for r in recs:
        flag = " **←未識別**" if r["unknown"] else ""
        out = " (離群)" if r["outlier"] else ""
        sep = f"{r['sep']:%H:%M:%S}" if r["sep"] else "—"
        md.append(f"| {r['u0']:+7.1f} | {r['rel1']:+7.1f} | {r['rate']:+6.2f} | {r['a1']:.1f} | {r['norad']} | {r['name']}{flag}{out} | "
                  f"{r['gcat_name']} | {sep} | {r['pred_sep']:%H:%M:%S} |")
    md += ["", "判讀方式：若 OBJECT H 是 TORO-2（第一顆分離，19:39:09），其回推相位應落在 19:39~19:40 分離群（BRO-17、BRO-20、Sari、Hunity、"
           "Lemur-2 Laila、IHI-SAT-2 等）之中，且是 11 個未識別物件裡唯一同時滿足「早分離相位」與「8U / 15 kg」的物件。"]
    open(os.path.join(RES, "deployment_order_check.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
    print("\n".join(md[:len(md) - len(recs) - 4]))


if __name__ == "__main__":
    main()
