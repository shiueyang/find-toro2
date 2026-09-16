"""
Step 2 - 從 Transporter-15 的未識別物件中，找出最可能是 TORO-2 的 TLE

輸入：data/raw/ 的 Celestrak TLE、SATCAT、GCAT satcat
輸出：results/all_objects_elements.csv        全部 2025-276 物件的軌道根數 / 阻力參數
      results/candidates_ranked.csv          12 個未識別物件的評分排名
      results/candidates_ranked.md           排名報告（給人看）
      results/toro2_candidate_tles.txt       候選 TLE（第一組 = 最可能）
      data/processed/t15_unknown.tce         給 STK ImportTLEFile 用（名稱已淨化，R01 = 最可能）
      data/processed/t15_reference_8U.tce    同級（8U, 10~25 kg）已識別物件，作為阻力對照

評分邏輯（每項 0~1，加權）：
  A. 物理等級：GCAT 給的質量/尺寸是否落在 TORO-2 規格（8U，~15 kg）附近          權重 0.35
  B. GCAT 識別：Jonathan McDowell 依部署時序 + 早期 TLE 相位推得的名字是否為 TORO2   權重 0.35
  C. 阻力一致性：B* 是否落在「同級 8U 物件」的合理範圍（失控翻滾者阻力偏高屬正常）   權重 0.20
  D. 部署時序：TORO-2 是 T+55 min 第一顆分離（19:39:09 UTC）；此項需 Space-Track 歷史
     TLE 才能獨立驗證（見 scripts/analyze_deployment_order.py），這裡只給部署時間差    權重 0.10
"""
import csv, math, os, re, sys, datetime as dt
from sgp4.api import Satrec

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, RES, PROC = (os.path.join(ROOT, *d.split("/")) for d in ("data/raw", "results", "data/processed"))
INTDES = "2025-276"
MU, RE = 398600.4418, 6378.137

TORO2 = dict(name="TORO-2 (TORO-8U-1)", mass_kg=11.0, form="8U，帆板已展開（帆板面 8U+8U+4U）",
             # m^2/kg。由 CAD（8u_asm_0312.stp 展開態，scripts/projected_area.py 輪廓法）算出：
             #   隨機翻滾平均投影 0.1405 m^2 -> 0.0128；最大投影（大面迎風）0.1999 m^2 -> 0.0182；最小 0.0403 -> 0.0037
             #   （手算的 總表面積/4 = 0.0155 高估了，因為帆板與本體互相遮蔽）
             am_tumbling=0.0128, am_max=0.0182, am_min=0.0037,
             sep_time=dt.datetime(2025, 11, 28, 19, 39, 9), launch=dt.datetime(2025, 11, 28, 18, 44))
# 權重：A 物理等級（GCAT 的質量是「指派名字」的屬性，對未識別物件有循環論證之嫌，權重調低）、
#       B GCAT 識別、C B* 相對同級、D 部署時序、E 由歷史根數 + 大氣模型反推的 A/m 是否符合 TORO-2 實際規格
WEIGHTS = dict(A=0.20, B=0.30, C=0.10, D=0.05, E=0.35)
UNKNOWN_RE = re.compile(r"TRANSPORTER-15 OBJECT|TBA - TO BE ASSIGNED|OBJECT [A-Z]+$")
# GCAT satcat.tsv 欄位（若檔案缺 #JCAT 標題列時使用）
GCAT_HEADER = ("JCAT Satcat Launch_Tag Piece Type Name PLName LDate Parent SDate Primary DDate Status Dest Owner State "
               "Manufacturer Bus Motor Mass MassFlag DryMass DryFlag TotMass TotFlag Length LFlag Diameter DFlag Span "
               "SpanFlag Shape ODate Perigee PF Apogee AF Inc IF OpOrbit OQUAL AltNames").split()


def read_tles():
    path = os.path.join(RAW, f"celestrak_{INTDES}_tle.txt")
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
    out = {}
    for i in range(0, len(lines), 3):
        name, l1, l2 = lines[i].strip(), lines[i + 1], lines[i + 2]
        s = Satrec.twoline2rv(l1, l2)
        n_rad_s = s.no_kozai / 60.0
        a = (MU / n_rad_s ** 2) ** (1 / 3)
        epoch = dt.datetime(2000, 1, 1) + dt.timedelta(days=s.jdsatepoch + s.jdsatepochF - 2451544.5)
        out[int(l1[2:7])] = dict(
            name=name, norad=int(l1[2:7]), intdes=l1[9:17].strip(), l1=l1, l2=l2,
            epoch=epoch, a_km=a, alt_km=a - RE, inc_deg=math.degrees(s.inclo), raan_deg=math.degrees(s.nodeo),
            ecc=s.ecco, argp_deg=math.degrees(s.argpo), ma_deg=math.degrees(s.mo),
            mm_rev_day=s.no_kozai * 1440 / (2 * math.pi), ndot=float(l1[33:43]), bstar=s.bstar,
            unknown=bool(UNKNOWN_RE.search(name)))
    return out


def read_satcat():
    p = os.path.join(RAW, f"celestrak_satcat_{INTDES}.csv")
    return {int(r["NORAD_CAT_ID"]): r for r in csv.DictReader(open(p, encoding="utf-8"))}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def read_gcat():
    p = os.path.join(RAW, f"gcat_satcat_{INTDES}.tsv")
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
        sd = r["SDate"].strip()
        sep = None
        m2 = re.match(r"(\d{4}) (\w{3}) (\d+) (\d{2})(\d{2}):(\d{2})", sd)
        if m2:
            sep = dt.datetime.strptime(" ".join(m2.groups()[:3]), "%Y %b %d").replace(
                hour=int(m2[4]), minute=int(m2[5]), second=int(m2[6]))
        out[int(m[1])] = dict(gcat_name=r["Name"].strip(), gcat_owner=r["Owner"].strip(), gcat_type=r["Type"].strip(),
                              mass_kg=num(r["Mass"]), length_m=num(r["Length"]), diam_m=num(r["Diameter"]),
                              span_m=num(r["Span"]), shape=r["Shape"].strip(), sep_time=sep, sep_raw=sd)
    return out


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def clean_name(s):
    return re.sub(r"[^A-Za-z0-9_]", "_", s).strip("_")


def is_8u_class(o):
    m, L = o.get("mass_kg"), o.get("length_m")
    return m is not None and L is not None and 10 <= m <= 25 and 0.3 <= L <= 0.45


def main():
    for d in (RES, PROC):
        os.makedirs(d, exist_ok=True)
    tles, satcat, gcat = read_tles(), read_satcat(), read_gcat()
    for n, o in tles.items():
        o.update(gcat.get(n, {}))
        o["owner_celestrak"] = satcat.get(n, {}).get("OWNER", "")

    # --- 全部物件根數表 -------------------------------------------------------
    cols = ["norad", "intdes", "name", "gcat_name", "gcat_owner", "mass_kg", "length_m", "diam_m", "span_m", "shape",
            "sep_raw", "epoch", "alt_km", "inc_deg", "raan_deg", "ecc", "mm_rev_day", "ndot", "bstar", "unknown"]
    with open(os.path.join(RES, "all_objects_elements.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for o in sorted(tles.values(), key=lambda o: o["alt_km"]):
            w.writerow({**o, "epoch": o["epoch"].isoformat(timespec="seconds")})

    # --- 8U 同級對照組（已識別、質量 10~25 kg、長度 0.3~0.45 m）------------------------------
    ref = [o for o in tles.values() if not o["unknown"] and is_8u_class(o)]
    ref_bstar_med = median([o["bstar"] for o in ref])
    ref_alt_med = median([o["alt_km"] for o in ref])
    unknowns = [o for o in tles.values() if o["unknown"]]

    # --- E：歷史根數反推的 A/m（results/ballistic_estimate.csv，由 estimate_ballistic.py 產生；沒有就不計分）----
    am = {}
    bp = os.path.join(RES, "ballistic_estimate.csv")
    if os.path.exists(bp):
        for r in csv.DictReader(open(bp, encoding="utf-8")):
            am[int(r["norad"])] = float(r["am"])
    W = dict(WEIGHTS)
    if not am:
        W["E"] = 0.0
    wsum = sum(W.values())

    # --- 評分 ---------------------------------------------------------------------
    for o in unknowns:
        m, L = o.get("mass_kg"), o.get("length_m")
        if m is None:
            sA = 0.5
        elif 10 <= m <= 25 and L and 0.35 <= L <= 0.45:
            sA = 1.0                                               # 8U / 16U 級
        elif 10 <= m <= 25:
            sA = 0.5                                               # 6U 級
        else:
            sA = 0.0                                               # 1U / 3U
        sB = 1.0 if o.get("gcat_name", "").upper().startswith("TORO") else 0.0
        ratio = o["bstar"] / ref_bstar_med if ref_bstar_med else 1.0
        sC = 1.0 if 0.5 <= ratio <= 3.0 else 0.5 if 0.3 <= ratio <= 5.0 else 0.0
        dtsep = (o["sep_time"] - TORO2["sep_time"]).total_seconds() if o.get("sep_time") else None
        sD = 1.0 if dtsep == 0 else 0.5 if dtsep is not None and abs(dtsep) < 180 else 0.0
        am_ratio = am.get(o["norad"], float("nan")) / TORO2["am_tumbling"]
        # 失控衛星的姿態可能介於「隨機翻滾」與「大面長期迎風」之間，因此接受區間取 [0.8×翻滾平均, 1.25×最大投影]
        # （1.25 涵蓋平板 Cd 可達 2.6~3 而非 2.2 的效應）；外圈 [0.5×翻滾, 1.6×最大] 給半分
        am_v = am.get(o["norad"], float("nan"))
        lo1, hi1 = 0.8 * TORO2["am_tumbling"], 1.25 * TORO2["am_max"]
        lo2, hi2 = 0.5 * TORO2["am_tumbling"], 1.6 * TORO2["am_max"]
        sE = 0.0 if am_v != am_v else 1.0 if lo1 <= am_v <= hi1 else 0.5 if lo2 <= am_v <= hi2 else 0.0
        o.update(score_A_physical=sA, score_B_gcat=sB, score_C_drag=sC, score_D_sep=sD, score_E_am=sE,
                 bstar_ratio_vs_8U=ratio, sep_dt_s=dtsep, am_est=am.get(o["norad"]), am_ratio_vs_toro2=am_ratio,
                 score=round((W["A"] * sA + W["B"] * sB + W["C"] * sC + W["D"] * sD + W["E"] * sE) / wsum, 3))
    unknowns.sort(key=lambda o: (-o["score"], o["norad"]))

    # --- CSV ------------------------------------------------------------------------
    cols = ["rank", "norad", "intdes", "name", "gcat_name", "gcat_owner", "mass_kg", "length_m", "diam_m", "span_m",
            "sep_raw", "sep_dt_s", "alt_km", "inc_deg", "raan_deg", "bstar", "bstar_ratio_vs_8U", "ndot", "epoch",
            "am_est", "am_ratio_vs_toro2",
            "score_A_physical", "score_B_gcat", "score_C_drag", "score_D_sep", "score_E_am", "score"]
    with open(os.path.join(RES, "candidates_ranked.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for i, o in enumerate(unknowns, 1):
            w.writerow({**o, "rank": i, "epoch": o["epoch"].isoformat(timespec="seconds")})

    # --- TLE 輸出 -------------------------------------------------------------------
    now = dt.datetime.utcnow()
    with open(os.path.join(RES, "toro2_candidate_tles.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# TORO-2 candidate TLEs, ranked (generated {now:%Y-%m-%d %H:%M} UTC from Celestrak)\n")
        for i, o in enumerate(unknowns, 1):
            f.write(f"# rank {i}  score {o['score']}  GCAT={o.get('gcat_name', '?')}  "
                    f"alt={o['alt_km']:.1f} km  epoch={o['epoch']:%Y-%m-%d %H:%M}Z\n")
            f.write(f"{o['name']}\n{o['l1']}\n{o['l2']}\n")
    with open(os.path.join(PROC, "t15_unknown.tce"), "w", encoding="ascii", newline="\n") as f:
        for i, o in enumerate(unknowns, 1):
            short = clean_name(o["name"].replace("TRANSPORTER-15 ", "T15_"))
            f.write(f"R{i:02d}_{short}_{o['norad']}\n{o['l1']}\n{o['l2']}\n")
    with open(os.path.join(PROC, "t15_reference_8U.tce"), "w", encoding="ascii", newline="\n") as f:
        for o in sorted(ref, key=lambda o: o["norad"]):
            f.write(f"REF_{clean_name(o['name'])}_{o['norad']}\n{o['l1']}\n{o['l2']}\n")

    # --- Markdown 報告 ----------------------------------------------------------------
    latest = max(o["epoch"] for o in tles.values())
    top = unknowns[0]
    md = [f"# TORO-2 候選物件排名（Transporter-15 / {INTDES}）\n",
          f"產生時間：{now:%Y-%m-%d %H:%M} UTC　TLE 來源：Celestrak（最新歷元 {latest:%Y-%m-%d %H:%M}Z）\n",
          f"目標：{TORO2['name']}，{TORO2['form']}，約 {TORO2['mass_kg']:.0f} kg，"
          f"分離時間 {TORO2['sep_time']:%Y-%m-%d %H:%M:%S} UTC（升空後第一顆分離）。\n",
          f"Celestrak 上此次發射共 {len(tles)} 個有 TLE 的物件，其中 **{len(unknowns)} 個仍為未識別"
          f"（TRANSPORTER-15 OBJECT xx）**。\n",
          "## 排名\n",
          f"權重：A 物理等級 {W['A']}、B GCAT 識別 {W['B']}、C B* 相對同級 8U {W['C']}、D 部署時序 {W['D']}、"
          f"E 反推 A/m 落在 CAD 算出的 TORO-2 區間（翻滾平均 {TORO2['am_tumbling']} ~ 大面迎風 {TORO2['am_max']} m²/kg，11 kg）{W['E']}"
          + ("" if am else "（無 ballistic_estimate.csv，E 不計分）") + "\n",
          "| # | NORAD | COSPAR | GCAT 推定名稱 | GCAT 質量 kg | 分離時刻 (UTC) | 高度 km | B*/8U中位 | 反推 A/m | A/m ÷ TORO-2理論 | "
          "A | B | C | D | E | **總分** |",
          "|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|"]
    for i, o in enumerate(unknowns, 1):
        sep = f"{o['sep_time']:%H:%M:%S}" if o.get("sep_time") else "—"
        am_s = f"{o['am_est']:.4f}" if o.get("am_est") is not None else "—"
        amr = f"{o['am_ratio_vs_toro2']:.2f}" if o["am_ratio_vs_toro2"] == o["am_ratio_vs_toro2"] else "—"
        md.append(f"| {i} | {o['norad']} | {o['intdes']} | {o.get('gcat_name', '?')} ({o.get('gcat_owner', '?')}) | "
                  f"{o.get('mass_kg') or '?'} | {sep} | {o['alt_km']:.1f} | {o['bstar_ratio_vs_8U']:.2f} | {am_s} | {amr} | "
                  f"{o['score_A_physical']:.1f} | {o['score_B_gcat']:.0f} | {o['score_C_drag']:.1f} | {o['score_D_sep']:.1f} | "
                  f"{o['score_E_am']:.1f} | **{o['score']}** |")
    md += ["", "## 8U 同級對照組（已識別）\n",
           f"B* 中位數 {ref_bstar_med:.2e}，高度中位數 {ref_alt_med:.1f} km。\n",
           "| NORAD | 名稱 | GCAT | 質量 kg | 尺寸 m | 外形 | 高度 km | B* |", "|--|--|--|--|--|--|--|--|"]
    for o in sorted(ref, key=lambda o: o["alt_km"]):
        md.append(f"| {o['norad']} | {o['name']} | {o.get('gcat_name', '')} | {o.get('mass_kg')} | "
                  f"{o.get('length_m')}×{o.get('diam_m')}×{o.get('span_m')} | {o.get('shape', '')} | "
                  f"{o['alt_km']:.1f} | {o['bstar']:.2e} |")
    md += ["", "## 結論\n",
           f"最可能為 TORO-2 的物件：**{top['name']}（NORAD {top['norad']}，{top['intdes']}）**，總分 {top['score']}。\n",
           "理由：",
           f"1. GCAT（Jonathan McDowell）依 SpaceX 部署時序與早期 TLE 相位，將此物件識別為 TORO2（TASA/PYRAS），"
           f"且它是本次發射 **第一顆分離** 的酬載（{TORO2['sep_time']:%H:%M:%S} UTC）。",
           "2. 未識別物件中，GCAT 物理等級屬 8U/16U 級的只有它與 CTC-1 A/B/C（21 kg）；其餘為 1U/3U/6U"
           "（注意：未識別物件的 GCAT 質量是隨指派名字而來的，非量測值）。",
           (f"3. 由 Space-Track 歷史根數的衰減率 + NRLMSISE-00 反推，其 A/m ≈ {top['am_est']:.4f} m²/kg；"
            f"TORO-2 展開態 CAD 的隨機翻滾平均是 {TORO2['am_tumbling']}、大面迎風最大值 {TORO2['am_max']} m²/kg（11 kg），"
            f"觀測值為翻滾平均的 {top['am_ratio_vs_toro2']:.2f} 倍、接近大面迎風上限（平板 Cd 高於 2.2 可解釋差額）；"
            "受控的同級 8U 只有 0.005~0.009。這是與名字指派無關的獨立物理證據（方法已用 PARUS-6U1 驗證，誤差 5%）。" if top.get("am_est") else
            f"3. 它的 B* 為同級 8U 中位數的 {top['bstar_ratio_vs_8U']:.1f} 倍，阻力偏高，符合失控翻滾。"),
           "",
           "備援順位（若追蹤主候選無回應）：" +
           "、".join(f"{o['name']} ({o['norad']}, GCAT={o.get('gcat_name')}, 總分 {o['score']})" for o in unknowns[1:4]) + "。",
           "", "## 尚待驗證\n",
           "- **部署時序獨立驗證**：需 Space-Track 2025-11-29 ~ 2025-12-15 的歷史 TLE。用你自己的帳號執行 "
           "`scripts/fetch_spacetrack_history.py`，再跑 `scripts/analyze_deployment_order.py`，"
           "檢查各物件在早期歷元的沿軌相位順序是否與 GCAT 分離時間單調對應。",
           "- **地面站盲追**：`scripts/stk_build_scenario.py` 把 12 個候選載入 STK 10 並輸出對 NTUT / TASA 的過境時段"
           "（results/stk/）。先追主候選，過境時以 Doppler 掃 TORO-2 下行頻率。",
           "- TLE 每日更新：重新執行 `python scripts/fetch_data.py && python scripts/analyze_candidates.py`。"]
    open(os.path.join(RES, "candidates_ranked.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")

    print("\n".join(md[:8 + len(unknowns)]))
    print("\n-> results/candidates_ranked.md, candidates_ranked.csv, toro2_candidate_tles.txt, data/processed/*.tce")


if __name__ == "__main__":
    main()
