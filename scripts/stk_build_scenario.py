"""
Step 3 - 在本機正在執行的 STK 10 中建立 FindTORO2 場景，並輸出地面站過境報表

透過 STK Connect（TCP 5001，STK 預設開啟）下命令，不需 pywin32。
  1. 新建場景 FindTORO2（若已有場景會先卸載），分析時段 = 現在(UTC) 起 N 天
  2. 建立地面站 Facility：NTUT（北科大）與 TASA（新竹），最低仰角 10 度
     （座標取自實驗室既有 STK 場景 6u/ntut.f、6u/tasa.f，可用 --gs 覆寫）
  3. ImportTLEFile 載入 data/processed/t15_unknown.tce（12 個未識別候選，R01 = 最可能）
     與 data/processed/t15_reference_8U.tce（同級已識別 8U，對照用）
  4. 對每個候選 × 每個地面站計算 Access，輸出：
        results/stk/access_<sat>_<gs>.txt   過境起訖時間、持續秒數
        results/stk/aer_<sat>_<gs>.txt      主候選（R01）過境期間每 10 s 的方位/仰角/距離/距離率
  5. 場景存到 ~/Documents/STK 10/FindTORO2/

用法：python scripts/stk_build_scenario.py [--days 7] [--gs NTUT,TASA] [--port 5001] [--no-save]
"""
import argparse, datetime as dt, glob, os, re, socket, sys, time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "results", "stk")
SCEN_NAME = "FindTORO2"
SCEN_DIR = os.path.join(os.path.expanduser("~"), "Documents", "STK 10", SCEN_NAME)

# lat(deg) lon(deg) alt(m) min_elev(deg)
GROUND_STATIONS = {
    "NTUT": (25.0429512137040, 121.536123244751, 50.0, 10.0),   # 國立臺北科技大學
    "TASA": (24.8016534493410, 121.001108487184, 40.0, 10.0),   # 國家太空中心（新竹）
}


class Connect:
    def __init__(self, host="127.0.0.1", port=5001):
        self.s = socket.create_connection((host, port), timeout=600)
        self.buf = b""

    def _fill(self):
        chunk = self.s.recv(65536)
        if not chunk:
            raise ConnectionError("STK closed the Connect socket")
        self.buf += chunk

    def _readline(self):
        while b"\n" not in self.buf:
            self._fill()
        line, self.buf = self.buf.split(b"\n", 1)
        return line.decode(errors="replace")

    def _readn(self, n):
        while len(self.buf) < n:
            self._fill()
        data, self.buf = self.buf[:n], self.buf[n:]
        return data.decode(errors="replace")

    def cmd(self, c, quiet=False, data=False):
        """送出一條 Connect 命令，回傳 (ok, [payload lines])；NACK 會 raise。

        STK 10 Connect 回覆格式（實測）：
          * 無資料的命令：裸的 b'ACK'（3 bytes，無換行）或 b'NACK'
          * 有資料的命令（GetStkVersion / CheckScenario / AllInstanceNames ...）：
            'ACK<CMD> <nbytes>' 標頭補空白到 42 bytes 再接 '\\n'，其後緊接 nbytes 的資料。
        呼叫端用 data=True 標示會回資料的命令。"""
        self.s.sendall((c + "\n").encode())
        payload = []
        if data:
            hdr = self._readline()
            if hdr.startswith("NACK"):
                raise RuntimeError(f"NACK from STK for: {c}")
            m = re.match(r"ACK\S*\s+(\d+)", hdr)
            n = int(m.group(1)) if m else 0
            if n:
                payload = [l for l in self._readn(n).splitlines() if l.strip()]
        else:
            tag = self._readn(3)
            if tag == "NAC":
                self._readn(1)
                raise RuntimeError(f"NACK from STK for: {c}")
            if tag != "ACK":
                raise RuntimeError(f"unexpected reply {tag!r} for: {c}")
        if not quiet:
            print(f"  OK   {c[:110]}")
        return True, payload


def stk_time(t):
    return t.strftime("%d %b %Y %H:%M:%S.000")


def tce_names(path):
    names = []
    for l in open(path):
        l = l.rstrip("\n")
        if l and not l.startswith(("1 ", "2 ")):
            names.append(l.strip())
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=7.0)
    ap.add_argument("--gs", default="NTUT,TASA", help="逗號分隔，或 name:lat:lon:alt_m:minel")
    ap.add_argument("--port", type=int, default=5001)
    ap.add_argument("--no-save", action="store_true")
    ap.add_argument("--aer-top", type=int, default=1, help="輸出 AER 細節報表的前 N 名候選")
    a = ap.parse_args()

    gs = {}
    for item in a.gs.split(","):
        if ":" in item:
            n, lat, lon, alt, mel = item.split(":")
            gs[n] = (float(lat), float(lon), float(alt), float(mel))
        else:
            gs[item] = GROUND_STATIONS[item]

    unk_tce = os.path.join(PROC, "t15_unknown.tce")
    ref_tce = os.path.join(PROC, "t15_reference_8U.tce")
    if not os.path.exists(unk_tce):
        sys.exit("先執行 scripts/analyze_candidates.py 產生 data/processed/t15_unknown.tce")
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "*.txt")):
        os.remove(f)

    t0 = dt.datetime.utcnow().replace(microsecond=0)
    t1 = t0 + dt.timedelta(days=a.days)
    print(f"STK Connect 127.0.0.1:{a.port}  時段 {t0:%Y-%m-%d %H:%M}Z -> {t1:%Y-%m-%d %H:%M}Z")

    c = Connect(port=a.port)
    print("STK:", c.cmd("GetStkVersion /", quiet=True, data=True)[1])
    if c.cmd("CheckScenario /", quiet=True, data=True)[1][0].strip() == "1":
        _, names = c.cmd("AllInstanceNames /", quiet=True, data=True)
        scen = [p for p in " ".join(names).split() if p.count("/") == 2][0]
        if scen.endswith("/" + SCEN_NAME):
            print(f"  場景 {SCEN_NAME} 已開啟，清掉舊物件後重用")
            for cls in ("Satellite", "Facility", "Constellation"):
                c.cmd(f"UnloadMulti / */{cls}/*", quiet=True)
        else:
            print(f"  卸載目前場景 {scen} 並新建 {SCEN_NAME}")
            c.cmd("Unload / *")
            c.cmd(f"New / Scenario {SCEN_NAME}")
    else:
        c.cmd(f"New / Scenario {SCEN_NAME}")
    c.cmd(f'SetAnalysisTimePeriod * "{stk_time(t0)}" "{stk_time(t1)}"')
    c.cmd(f'SetEpoch * "{stk_time(t0)}"')
    c.cmd("Animate * Reset")

    for name, (lat, lon, alt, mel) in gs.items():
        c.cmd(f"New / */Facility {name}")
        c.cmd(f"SetPosition */Facility/{name} Geodetic {lat:.7f} {lon:.7f} {alt/1000.0:.4f}")
        c.cmd(f"SetConstraint */Facility/{name} ElevationAngle Min {mel}")

    # 載入 TLE：AutoPropagate On 讓 SGP4 直接算到場景時段；名稱由 .tce 的第 0 行決定
    c.cmd(f'ImportTLEFile * "{unk_tce}" AutoPropagate On TimeStep 60 '
          f'StartStop "{stk_time(t0)}" "{stk_time(t1)}" Constellation T15_UNKNOWN')
    if os.path.exists(ref_tce):
        c.cmd(f'ImportTLEFile * "{ref_tce}" AutoPropagate On TimeStep 60 '
              f'StartStop "{stk_time(t0)}" "{stk_time(t1)}" Constellation T15_REF_8U')
    _, sats = c.cmd("AllInstanceNames /", quiet=True, data=True)
    sat_paths = [p for p in " ".join(sats).split() if "/Satellite/" in p]
    print(f"  場景內衛星 {len(sat_paths)} 顆")

    # 對應 .tce 名稱 -> 場景內實際衛星名稱（STK 若忽略名稱列，會以 SSC 號碼命名，用號碼比對）
    cand, actual = [], {}
    for n in tce_names(unk_tce):
        norad = n.rsplit("_", 1)[-1]
        hit = [p for p in sat_paths if p.endswith("/Satellite/" + n)] or \
              [p for p in sat_paths if norad in p.rsplit("/", 1)[-1]]
        cand.append(n)
        if hit:
            actual[n] = hit[0].rsplit("/", 1)[-1]
    missing = [n for n in cand if n not in actual]
    if missing:
        print("  ! 以下候選未成功載入：", missing)

    # 注意：本機 STK 的 "Access" 報表樣式被改成只有 Range/Time（Config/Styles/Access/ACCESS.rst），
    # 所以過境區間直接取 Access 命令回傳的資料；方位/仰角則用 *地面站端* 的 AER 報表（衛星端會是負仰角）。
    summary, rows = [], []
    for rank, n in enumerate(cand, 1):
        if n in missing:
            continue
        sat = f"*/Satellite/{actual[n]}"
        for g in gs:
            fac = f"*/Facility/{g}"
            _, acc = c.cmd(f"Access {sat} {fac}", quiet=True, data=True)
            intervals = parse_access_payload(" ".join(acc))
            aer_file = os.path.join(OUT, f"aer_{n}_{g}.txt")
            aer = []
            if intervals:
                c.cmd(f'ReportCreate {fac} Type Save Style "AER" File "{aer_file}" AccessObject {sat} '
                      f'TimePeriod UseAccessTimes TimeStep 10', quiet=True)
                aer = parse_aer(aer_file)
            passes = summarize_passes(intervals, aer)
            write_schedule(os.path.join(OUT, f"access_{n}_{g}.txt"), n, actual[n], g, t0, t1, passes)
            tot = sum(p["dur_s"] for p in passes)
            summary.append((n, g, len(passes), tot))
            rows += [dict(rank=rank, satellite=n, stk_name=actual[n], ground_station=g, **p) for p in passes]
            best = max((p["max_el"] for p in passes if p["max_el"] is not None), default=float("nan"))
            print(f"  {n:34s} -> {g}: {len(passes):3d} passes, {tot/60:6.1f} min total, best max-el {best:5.1f} deg")

    with open(os.path.join(OUT, "access_summary.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("satellite,ground_station,passes,total_seconds,window_start_utc,window_end_utc\n")
        for n, g, npass, tot in summary:
            f.write(f"{n},{g},{npass},{tot:.0f},{t0.isoformat()}Z,{t1.isoformat()}Z\n")
    with open(os.path.join(OUT, "pass_schedule.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("rank,satellite,stk_name,ground_station,aos_utc,los_utc,aos_local_utc8,dur_s,aos_az,max_el,t_max_el_utc,los_az,min_range_km\n")
        for r in rows:
            f.write(",".join(fmt(r.get(k)) for k in ("rank", "satellite", "stk_name", "ground_station", "aos", "los",
                                                       "aos_local", "dur_s", "aos_az", "max_el", "t_max_el", "los_az",
                                                       "min_range_km")) + "\n")
    write_top_markdown(os.path.join(OUT, "pass_schedule_R01.md"), rows, cand[0] if cand else "", t0, t1)

    if not a.no_save:
        os.makedirs(SCEN_DIR, exist_ok=True)
        c.cmd(f'Save / * "{SCEN_DIR}"')
        print(f"  場景已存到 {SCEN_DIR}")
    print(f"-> {os.path.relpath(OUT, ROOT)}/access_*.txt, aer_*.txt, pass_schedule.csv, pass_schedule_R01.md")


STK_T = "%d %b %Y %H:%M:%S.%f"
TW = dt.timezone(dt.timedelta(hours=8))


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, dt.datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, float):
        return f"{v:.1f}"
    return str(v)


def parse_access_payload(s):
    """Access 命令回傳：'<satPath> <facPath> <N> <start1> <stop1> ... <startN> <stopN>'，每個時間佔 4 個 token。"""
    tok = s.split()
    if len(tok) < 3:
        return []
    try:
        n = int(tok[2])
    except ValueError:
        return []
    times = tok[3:3 + 8 * n]
    out = []
    for i in range(0, len(times) - 7, 8):
        t1 = dt.datetime.strptime(" ".join(times[i:i + 4]), STK_T)
        t2 = dt.datetime.strptime(" ".join(times[i + 4:i + 8]), STK_T)
        out.append((t1, t2))
    return out


def parse_aer(path):
    """地面站端 AER 報表：回傳 [(time, az, el, range_km), ...]"""
    rows = []
    if not os.path.exists(path):
        return rows
    pat = re.compile(r"^\s*(\d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2}\.\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)")
    for l in open(path, encoding="utf-8", errors="replace"):
        m = pat.match(l)
        if m:
            rows.append((dt.datetime.strptime(m.group(1), STK_T), float(m.group(2)), float(m.group(3)), float(m.group(4))))
    return rows


def summarize_passes(intervals, aer):
    passes = []
    for t1, t2 in intervals:
        pts = [r for r in aer if t1 - dt.timedelta(seconds=1) <= r[0] <= t2 + dt.timedelta(seconds=1)]
        p = dict(aos=t1, los=t2, aos_local=t1.replace(tzinfo=dt.timezone.utc).astimezone(TW).replace(tzinfo=None),
                 dur_s=(t2 - t1).total_seconds(), aos_az=None, max_el=None, t_max_el=None, los_az=None, min_range_km=None)
        if pts:
            top = max(pts, key=lambda r: r[2])
            p.update(aos_az=pts[0][1], los_az=pts[-1][1], max_el=top[2], t_max_el=top[0], min_range_km=min(r[3] for r in pts))
        passes.append(p)
    return passes


def write_schedule(path, name, stk_name, gs, t0, t1, passes):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Pass schedule  {name}  (STK object {stk_name})  ->  ground station {gs}\n")
        f.write(f"# window {t0:%Y-%m-%d %H:%M}Z .. {t1:%Y-%m-%d %H:%M}Z   min elevation 10 deg   times UTC, local = UTC+8\n")
        f.write(f"# {len(passes)} passes, {sum(p['dur_s'] for p in passes)/60:.1f} min total\n")
        f.write(f"{'#':>3s} {'AOS (UTC)':19s} {'AOS (local)':19s} {'LOS (UTC)':19s} {'dur s':>6s} {'AOS az':>7s} {'max el':>7s} {'@ (UTC)':8s} {'LOS az':>7s} {'min rng km':>10s}\n")
        for i, p in enumerate(passes, 1):
            f.write(f"{i:3d} {fmt(p['aos']):19s} {fmt(p['aos_local']):19s} {fmt(p['los']):19s} {p['dur_s']:6.0f} "
                    f"{fmt(p['aos_az']):>7s} {fmt(p['max_el']):>7s} {p['t_max_el'].strftime('%H:%M:%S') if p['t_max_el'] else '':8s} "
                    f"{fmt(p['los_az']):>7s} {fmt(p['min_range_km']):>10s}\n")


def write_top_markdown(path, rows, top_name, t0, t1):
    rows = [r for r in rows if r["satellite"] == top_name]
    md = [f"# 主候選 {top_name} 過境時段（{t0:%Y-%m-%d %H:%M}Z ~ {t1:%Y-%m-%d %H:%M}Z，最低仰角 10°）\n",
          "時間為 UTC；括號內為台灣時間（UTC+8）。以最大仰角排序前 15 個過境優先追。\n",
          "| 地面站 | AOS (UTC) | AOS (台灣) | 持續 s | AOS 方位 | 最大仰角 | 最大仰角時刻 | LOS 方位 | 最近距離 km |",
          "|--|--|--|--|--|--|--|--|--|"]
    for r in sorted(rows, key=lambda r: -(r["max_el"] or 0))[:15]:
        md.append(f"| {r['ground_station']} | {fmt(r['aos'])} | {fmt(r['aos_local'])} | {r['dur_s']:.0f} | {fmt(r['aos_az'])} | "
                  f"**{fmt(r['max_el'])}** | {r['t_max_el'].strftime('%H:%M:%S') if r['t_max_el'] else ''} | {fmt(r['los_az'])} | {fmt(r['min_range_km'])} |")
    md.append("\n完整時序見 access_*.txt / pass_schedule.csv；每日重跑以更新 TLE。")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
