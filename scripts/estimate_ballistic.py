"""
用 Space-Track 歷史根數的半長軸衰減率 + NRLMSISE-00 大氣模型，反推每個物件的面積質量比 A/m，
並與 TORO-2 的實際規格（Pyras 提供：質量約 11 kg，帆板已展開，帆板面 8U+8U+4U）比較。

原理（近圓軌道）：  da/dt = - rho * (Cd*A/m) * sqrt(mu*a)
  -> Cd*A/m = -(da/dt) / (rho * sqrt(mu*a))，rho 取軌道平均（沿 SGP4 軌道取樣，NRLMSISE-00，當日 F10.7/Ap）。
  取 Cd = 2.2 得 A/m。絕對值受大氣模型 ±30% 左右不確定度影響，物件之間的「比值」則相當可靠。

TORO-2 的理論 A/m（隨機翻滾：平均投影面積 = 總表面積 / 4）：
  本體 8U 假設 1x2x4U（0.1 x 0.2 x 0.4 m）：表面積 0.28 m^2
  展開帆板 8U+8U+4U 面 = 0.08+0.08+0.04 = 0.20 m^2，雙面計 0.40 m^2
  -> 翻滾 A/m = (0.28+0.40)/4 / 11 = 0.0155 m^2/kg
  對照：帆板未展開只剩本體翻滾 0.28/4/11 = 0.0064；受控最小阻力面 0.02/11 = 0.0018；最大面朝前 (0.08+0.20)/11 = 0.0255

輸入：data/raw/spacetrack_gp_history_2025-276.tle、celestrak_SW-Last5Years.txt、gcat_satcat_2025-276.tsv、celestrak_2025-276_tle.txt
輸出：results/ballistic_estimate.csv / .md
用法：python scripts/estimate_ballistic.py [--t1 2025-12-19] [--t2 2026-01-08] [--cd 2.2]
"""
import argparse, csv, datetime as dt, math, os, re, sys
import numpy as np
from sgp4.api import Satrec, jday
from nrlmsise00 import msise_model

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, RES = os.path.join(ROOT, "data", "raw"), os.path.join(ROOT, "results")
INTDES = "2025-276"
MU, RE = 398600.4418, 6378.137
# 預設目標：TORO-2；可用 --label/--mass/--body/--panel-faces 換成別的衛星（例：PARUS-6U1 驗算）
TORO2 = dict(label="TORO-2", mass=11.0, body=(0.1, 0.2, 0.4), panel_faces_m2=0.08 + 0.08 + 0.04)
GCAT_HEADER = ("JCAT Satcat Launch_Tag Piece Type Name PLName LDate Parent SDate Primary DDate Status Dest Owner State "
               "Manufacturer Bus Motor Mass MassFlag DryMass DryFlag TotMass TotFlag Length LFlag Diameter DFlag Span "
               "SpanFlag Shape ODate Perigee PF Apogee AF Inc IF OpOrbit OQUAL AltNames").split()


def toro2_hypotheses():
    x, y, z = TORO2["body"]
    body = 2 * (x * y + x * z + y * z)
    pan = 2 * TORO2["panel_faces_m2"]
    m = TORO2["mass"]
    hyp = {
        "翻滾 + 帆板展開（手算 表面積/4）": (body + pan) / 4 / m,
        "翻滾、帆板未展開": body / 4 / m,
        "受控、最小面迎風": (x * y) / m,
        "最大面迎風（帆板+本體，手算）": (y * z + TORO2["panel_faces_m2"]) / m,
    }
    # 若有 CAD 輪廓法結果（scripts/projected_area.py），一併列出（以 CAD 的質量換算到目前 --mass）
    cad = os.path.join(RES, "toro2_projected_area_8u_asm_0312.json")
    if TORO2["label"].startswith("TORO-2") and os.path.exists(cad):
        import json
        c = json.load(open(cad, encoding="utf-8"))
        hyp["CAD 隨機翻滾平均投影（輪廓法）"] = c["proj_mean_m2"] / m
        hyp["CAD 最大投影（大面迎風）"] = c["proj_max_m2"] / m
        hyp["CAD 最小投影"] = c["proj_min_m2"] / m
    return hyp


def load_sw(path):
    """CSSI space weather txt -> {date: (f107_obs, f107_ctr81_obs, ap_daily)}"""
    sw = {}
    for l in open(path, encoding="utf-8", errors="replace"):
        p = l.split()
        if len(p) < 30 or not p[0].isdigit():
            continue
        try:
            d = dt.date(int(p[0]), int(p[1]), int(p[2]))
            sw[d] = (float(p[26]), float(p[28]), float(p[22]))
        except ValueError:
            continue
    return sw


def load_history(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
    hist = {}
    for i in range(0, len(lines), 3):
        l1, l2 = lines[i + 1], lines[i + 2]
        s = Satrec.twoline2rv(l1, l2)
        hist.setdefault(int(l1[2:7]), []).append((s.jdsatepoch + s.jdsatepochF, s, l1, l2))
    return hist


def load_gcat(intdes=INTDES):
    p = os.path.join(RAW, f"gcat_satcat_{intdes}.tsv")
    if not os.path.exists(p):                       # 從完整 GCAT 檔現切一份
        full = os.path.join(RAW, "gcat_satcat_full.tsv")
        lines = open(full, encoding="utf-8").read().splitlines()
        keep = [lines[0]] + [l for l in lines[1:] if f"\t{intdes}\t" in l]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(keep) + "\n")
    rows = open(p, encoding="utf-8").read().splitlines()
    hdr = GCAT_HEADER
    if rows and rows[0].startswith("#JCAT"):
        hdr, rows = rows[0].lstrip("#").split("\t"), rows[1:]
    out = {}
    for l in rows:
        r = dict(zip(hdr, l.split("\t")))
        m = re.match(r"S(\d+)", r.get("JCAT", ""))
        if not m:
            continue
        def num(x):
            try: return float(x)
            except ValueError: return None
        out[int(m[1])] = dict(gcat_name=r["Name"].strip(), mass=num(r["Mass"]), massflag=r["MassFlag"].strip(),
                              length=num(r["Length"]), bus=r["Bus"].strip(), shape=r["Shape"].strip())
    return out


def load_current_names(intdes=INTDES):
    p = os.path.join(RAW, f"celestrak_{intdes}_tle.txt")
    if not os.path.exists(p):                       # 沒有目前 TLE 檔就用 Space-Track 歷史檔裡的名稱
        return {}
    lines = [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip()]
    return {int(lines[i + 1][2:7]): lines[i].strip() for i in range(0, len(lines), 3)}


def clean_sets(win):
    """剔除交叉標記（cross-tag）或發散的根數：B* 非正或過大、偏心率 / 半長軸偏離該物件中位數太多。
    例：OBJECT H 在 2025-12-24~29 有一段高度在 501~514 km 亂跳、B* 正負互換的壞根數。"""
    if len(win) < 4:
        return win
    e = np.array([s.ecco for _, s in win])
    a = np.array([(MU / (s.no_kozai / 60) ** 2) ** (1 / 3) for _, s in win])
    b = np.array([s.bstar for _, s in win])
    e_med, a_med = np.median(e), np.median(a)
    mad_a = np.median(np.abs(a - a_med)) or 0.3
    keep = (b > 0) & (b < 0.01) & (np.abs(e - e_med) < 4 * max(e_med, 1e-4)) & (np.abs(a - a_med) < 6 * mad_a + 1.0)
    return [w for w, k in zip(win, keep) if k]


def theil_sen(t, y):
    """中位數斜率 + 對應截距（比最小平方法更抗離群點）"""
    n = len(t)
    slopes = [(y[j] - y[i]) / (t[j] - t[i]) for i in range(n) for j in range(i + 1, n) if t[j] != t[i]]
    k = float(np.median(slopes))
    c = float(np.median(y - k * t))
    return k, c


def teme_to_geodetic(r, t):
    """粗略：TEME -> 經緯高（忽略極移/章動，密度取樣用足夠）"""
    x, y, z = r
    jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second + t.microsecond / 1e6)
    T = (jd + fr - 2451545.0) / 36525.0
    gmst = (67310.54841 + (876600 * 3600 + 8640184.812866) * T + 0.093104 * T ** 2 - 6.2e-6 * T ** 3) % 86400 / 240.0
    lon = (math.degrees(math.atan2(y, x)) - gmst + 540) % 360 - 180
    rho = math.hypot(x, y)
    lat = math.degrees(math.atan2(z, rho))
    alt = math.sqrt(x * x + y * y + z * z) - RE
    return lat, lon, alt


def orbit_mean_density(sat, t_mid, sw, n_samples=48):
    """沿 t_mid 起一圈軌道取樣 NRLMSISE-00 密度（kg/m^3），回傳平均值與平均高度"""
    d = t_mid.date()
    f107, f107a, ap = sw.get(d) or sw.get(d - dt.timedelta(days=1)) or (150.0, 150.0, 10.0)
    f107_prev = (sw.get(d - dt.timedelta(days=1)) or (f107,))[0]      # MSIS 要「前一天」的 F10.7
    period_min = 2 * math.pi / sat.no_kozai
    dens, alts = [], []
    for k in range(n_samples):
        t = t_mid + dt.timedelta(minutes=period_min * k / n_samples)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        e, r, v = sat.sgp4(jd, fr)
        if e:
            continue
        lat, lon, alt = teme_to_geodetic(r, t)
        out = msise_model(t, alt, lat, lon, f107a, f107_prev, ap)
        dens.append(out[0][5] * 1000.0)          # g/cm^3 -> kg/m^3
        alts.append(alt)
    return float(np.mean(dens)), float(np.mean(alts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", default="2025-12-19")
    ap.add_argument("--t2", default="2026-01-08")
    ap.add_argument("--cd", type=float, default=2.2)
    ap.add_argument("--intdes", default=INTDES, help="發射的國際編號，決定要讀哪個歷史檔與 GCAT 檔")
    ap.add_argument("--target", type=int, default=None, help="要驗算的 NORAD 編號（例 68456）；給了就額外印出該物件的比對")
    ap.add_argument("--label", default=TORO2["label"])
    ap.add_argument("--mass", type=float, default=TORO2["mass"])
    ap.add_argument("--body", type=float, nargs=3, default=TORO2["body"], metavar=("X", "Y", "Z"), help="本體尺寸 m")
    ap.add_argument("--panel-faces", type=float, default=TORO2["panel_faces_m2"], help="展開帆板單面總面積 m²（未展開給 0）")
    a = ap.parse_args()
    TORO2.update(label=a.label, mass=a.mass, body=tuple(a.body), panel_faces_m2=a.panel_faces)
    intdes = a.intdes
    suffix = "" if intdes == INTDES and a.target is None else f"_{intdes}" + (f"_{a.target}" if a.target else "")
    T1, T2 = (dt.datetime.fromisoformat(x) for x in (a.t1, a.t2))
    jd1 = sum(jday(T1.year, T1.month, T1.day, 0, 0, 0)); jd2 = sum(jday(T2.year, T2.month, T2.day, 0, 0, 0))

    hist = load_history(os.path.join(RAW, f"spacetrack_gp_history_{intdes}.tle"))
    sw = load_sw(os.path.join(RAW, "celestrak_SW-Last5Years.txt"))
    gcat, cur = load_gcat(intdes), load_current_names(intdes)
    hyp = toro2_hypotheses()
    days = [T1 + dt.timedelta(days=x) for x in np.linspace(0, (T2 - T1).days, 5)]
    sw_used = [sw.get(t.date()) for t in days]
    print(f"space weather used (F10.7 obs, 81d, Ap): {sw_used}")

    recs = []
    for norad, sets in hist.items():
        win_all = [(ep, s) for ep, s, _, _ in sets if jd1 <= ep <= jd2]
        win = clean_sets(win_all)
        if len(win) < 6:
            continue
        t = np.array([ep - jd1 for ep, _ in win])
        av = np.array([(MU / (s.no_kozai / 60) ** 2) ** (1 / 3) for _, s in win])
        k, c = theil_sen(t, av)                              # km/day（中位數斜率，對殘留的壞根數不敏感）
        resid = float(np.median(np.abs(av - (k * t + c))))
        # 密度：用視窗內 5 個日期、各自最近的 TLE，沿一圈軌道取樣後平均
        dens, alts = [], []
        for tm in days:
            jdm = sum(jday(tm.year, tm.month, tm.day, 0, 0, 0))
            _, s = min(win, key=lambda w: abs(w[0] - jdm))
            rho, alt = orbit_mean_density(s, tm, sw)
            dens.append(rho); alts.append(alt)
        rho = float(np.mean(dens)); a_mean = float(np.mean(av))
        da_dt_ms = k * 1000 / 86400                          # m/s
        sqrt_mua = math.sqrt(MU * 1e9 * a_mean * 1e3)        # m^2/s
        cd_am = -da_dt_ms / (rho * sqrt_mua)                 # m^2/kg
        g = gcat.get(norad, {})
        name = cur.get(norad, "(no current TLE)")
        recs.append(dict(norad=norad, name=name, gcat_name=g.get("gcat_name", "?"), gcat_mass=g.get("mass"),
                         massflag=g.get("massflag", ""), bus=g.get("bus", ""), shape=g.get("shape", ""),
                         n_tle=len(win), n_rejected=len(win_all) - len(win), da_dt_km_day=k, fit_resid_km=resid,
                         alt_km=float(np.mean(alts)),
                         rho_kg_m3=rho, cd_am=cd_am, am=cd_am / a.cd,
                         unknown=bool(re.search(r"OBJECT [A-Z]+$|TBA", name))))
    if not recs:
        sys.exit("視窗內沒有足夠的根數")

    ref_am = hyp.get("CAD 隨機翻滾平均投影（輪廓法）", hyp["翻滾 + 帆板展開（手算 表面積/4）"])
    for r in recs:
        r["ratio_to_toro2_tumbling"] = r["am"] / ref_am
        # 與四種假設中最接近者
        r["closest_hyp"] = min(hyp, key=lambda h: abs(math.log(max(r["am"], 1e-6) / hyp[h])))
    recs.sort(key=lambda r: -r["am"])

    os.makedirs(RES, exist_ok=True)
    cols = ["norad", "name", "gcat_name", "gcat_mass", "massflag", "bus", "shape", "n_tle", "n_rejected", "da_dt_km_day", "fit_resid_km",
            "alt_km", "rho_kg_m3", "cd_am", "am", "ratio_to_toro2_tumbling", "closest_hyp", "unknown"]
    with open(os.path.join(RES, f"ballistic_estimate{suffix}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in recs:
            w.writerow(r)

    unk = [r for r in recs if r["unknown"]]
    ident = [r for r in recs if not r["unknown"]]
    L = TORO2["label"]
    md = [f"# 面積質量比（A/m）估計：衰減率 + NRLMSISE-00（{intdes}，{a.t1} ~ {a.t2}，Cd = {a.cd}）\n",
          f"{L} 規格：質量 {TORO2['mass']:.1f} kg，本體 {TORO2['body'][0]}×{TORO2['body'][1]}×{TORO2['body'][2]} m，"
          f"展開帆板單面總面積 {TORO2['panel_faces_m2']:.2f} m²。\n",
          f"| {L} 姿態假設 | 理論 A/m (m²/kg) |", "|--|--|"]
    md += [f"| {h} | {v:.4f} |" for h, v in hyp.items()]
    md += ["", f"太空天氣（{a.t1}~{a.t2}）：F10.7 obs / 81 日平均 / Ap = " +
           ", ".join(f"{s[0]:.0f}/{s[1]:.0f}/{s[2]:.0f}" for s in sw_used if s), ""]
    tgt = next((r for r in recs if r["norad"] == a.target), None) if a.target else None
    if a.target:
        md += [f"## 驗算目標 {L}（NORAD {a.target}）\n"]
        if tgt:
            md += [f"- 視窗內根數 {tgt['n_tle']} 組（剔除 {tgt['n_rejected']} 組），平均高度 {tgt['alt_km']:.0f} km，"
                   f"軌道平均密度 {tgt['rho_kg_m3']:.2e} kg/m³",
                   f"- 半長軸衰減率 da/dt = {tgt['da_dt_km_day']:.4f} km/day",
                   f"- **反推 A/m = {tgt['am']:.4f} m²/kg**，為「翻滾 + 帆板展開」理論值的 {tgt['ratio_to_toro2_tumbling']:.2f} 倍；"
                   f"最接近的假設：**{tgt['closest_hyp']}**",
                   "- 各假設的比值：" + "、".join(f"{h} ×{tgt['am'] / v:.2f}" for h, v in hyp.items()), ""]
        else:
            md += ["- 視窗內找不到足夠的根數（需 ≥ 6 組）", ""]
    md += ["## 未識別物件\n",
           f"| NORAD | Celestrak | GCAT 推定 (kg, flag) | 根數 用/剔除 | da/dt km/day | 高度 km | ρ kg/m³ | **A/m m²/kg** | / {L}翻滾展開 | 最接近的 {L} 假設 |",
           "|--|--|--|--|--|--|--|--|--|--|"]
    for r in unk:
        md.append(f"| {r['norad']} | {r['name']} | {r['gcat_name']} ({r['gcat_mass']}{r['massflag']}) | {r['n_tle']}/{r['n_rejected']} | "
                  f"{r['da_dt_km_day']:.4f} | {r['alt_km']:.0f} | {r['rho_kg_m3']:.2e} | **{r['am']:.4f}** | "
                  f"{r['ratio_to_toro2_tumbling']:.2f} | {r['closest_hyp']} |")
    md += ["", "## 已識別物件（依 A/m 排序，供校準：受控衛星應接近『最小面迎風』，3U Dove 翻滾約 0.01）\n",
           "| NORAD | 名稱 | GCAT 質量 | Bus | 外形 | da/dt km/day | A/m m²/kg |", "|--|--|--|--|--|--|--|"]
    for r in ident:
        md.append(f"| {r['norad']} | {r['name']} | {r['gcat_mass']}{r['massflag']} | {r['bus']} | {r['shape']} | "
                  f"{r['da_dt_km_day']:.4f} | {r['am']:.4f} |")
    # 結論段
    tol = (0.6, 1.6)
    hits = [r for r in unk if tol[0] <= r["ratio_to_toro2_tumbling"] <= tol[1]]
    md += ["", "## 判讀\n",
           f"- 與「{L}：{TORO2['mass']:.0f} kg、翻滾」理論值 {ref_am:.4f} m²/kg 相差在 ×{tol[0]}~×{tol[1]} 內（涵蓋大氣模型與 Cd 的不確定度）的未識別物件："
           + ("、".join(f"**{r['name']} ({r['norad']}, A/m {r['am']:.4f}, ×{r['ratio_to_toro2_tumbling']:.2f})**" for r in hits) if hits else "無") + "。",
           f"- A/m 明顯低於理論值的物件，若要是 {L}，就必須是「帆板沒展開」或「姿態受控」。",
           "- 絕對值受 NRLMSISE-00 在太陽極大期 500 km 的誤差（±30% 量級）影響；物件之間的比值可靠得多，"
           "可用已識別的受控 8U（BRO、Black Kite、Bellbird）與 3U Dove 當量尺。"]
    open(os.path.join(RES, f"ballistic_estimate{suffix}.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
    cut = next(i for i, l in enumerate(md) if l.startswith("## 未識別物件")) + 3 + len(unk)
    print("\n".join(md[:cut]))
    print("\n".join(md[-5:]))
    print(f"-> results/ballistic_estimate{suffix}.md / .csv")


if __name__ == "__main__":
    main()
