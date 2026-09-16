"""
（需自行輸入 Space-Track 帳號）下載 Transporter-15 全部物件在部署後前幾週的歷史 TLE

用途：獨立驗證 GCAT 對未識別物件的名字指派 —— 部署得越早/越晚的物件，在早期歷元的
沿軌相位應呈單調順序（見 analyze_deployment_order.py）。

用法（帳密只從環境變數讀，不會寫進 repo）：
    set SPACETRACK_USER=you@example.com
    set SPACETRACK_PASS=********
    python scripts/fetch_spacetrack_history.py [--start 2025-11-29] [--end 2025-12-15]

輸出：data/raw/spacetrack_gp_history_2025-276.json  （Space-Track gp_history 原始 JSON）
      data/raw/spacetrack_gp_history_2025-276.tle   （3LE 格式，每筆一組）
"""
import argparse, json, os, sys, time, requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
BASE = "https://www.space-track.org"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2025-12-17", help="首批公開根數是 2025-12-18")
    ap.add_argument("--end", default="2026-01-10")
    ap.add_argument("--intdes", default="2025-276")
    ap.add_argument("--norad", default="66666-66700,66701-66740,66741-66790,67483-67483",
                    help="NORAD 範圍清單，逗號分隔（例：2026-067 用 68416-68470,68471-68530,68800-68840）")
    ap.add_argument("--sanity", type=int, default=66673, help="用來確認登入的 NORAD 編號")
    a = ap.parse_args()
    ranges = [tuple(int(x) for x in seg.split("-")) for seg in a.norad.split(",")]

    user, pw = os.environ.get("SPACETRACK_USER"), os.environ.get("SPACETRACK_PASS")
    if not user or not pw:
        sys.exit("請先設定環境變數 SPACETRACK_USER / SPACETRACK_PASS（不要把帳密寫進程式或 repo）")

    s = requests.Session()
    r = s.post(f"{BASE}/ajaxauth/login", data={"identity": user, "password": pw}, timeout=60)
    r.raise_for_status()
    if "Failed" in r.text:
        sys.exit("Space-Track 登入失敗")

    short = a.intdes[2:].replace("-", "")          # 2025-276 -> 25276（gp_history 的 INTLDES 是 TLE 短格式）

    def get(path, label):
        q = f"{BASE}/basicspacedata/query/{path}/format/json"
        print(f"[{label}] GET {q}")
        for attempt in range(3):
            r = s.get(q, timeout=600)
            if r.status_code == 200:
                break
            print(f"  HTTP {r.status_code}, retry {attempt + 1}/3 ... {r.text[:200]}")
            time.sleep(15)
        r.raise_for_status()
        try:
            rows = r.json()
        except ValueError:
            print("  非 JSON 回應（可能未登入）：", r.text[:300])
            return []
        if isinstance(rows, dict):
            print("  伺服器回：", rows)
            return []
        print(f"  {len(rows)} rows")
        if rows:
            print("  sample:", {k: rows[0].get(k) for k in ("NORAD_CAT_ID", "INTLDES", "OBJECT_ID", "OBJECT_NAME", "EPOCH")})
        time.sleep(3)
        return rows

    # 1) 登入 / 權限 sanity check：現行 gp
    if not get(f"class/gp/NORAD_CAT_ID/{a.sanity}", f"sanity gp {a.sanity}"):
        sys.exit("連現行 gp 都查不到，代表登入或權限有問題")
    # 2) 單一物件的歷史（不加日期條件），確認 gp_history 可用，並看首批公開根數的日期
    get(f"class/gp_history/NORAD_CAT_ID/{a.sanity}/orderby/EPOCH asc/limit/3", f"sanity gp_history {a.sanity} (earliest)")

    # 3) 正式抓取。注意：Transporter 這類發射的物件通常要到部署後 2~3 週才進公開目錄，日期窗要從那之後起算。
    #    OBJECT_ID 的 ^ 運算子在 gp_history 不可用，改用 NORAD 編號範圍 + EPOCH >/<。
    data = []
    for lo, hi in ranges:
        rows = get(f"class/gp_history/NORAD_CAT_ID/{lo}--{hi}/EPOCH/>{a.start}/EPOCH/<{a.end}/orderby/NORAD_CAT_ID,EPOCH asc",
                   f"history {lo}-{hi}")
        data += [e for e in rows if str(e.get("OBJECT_ID", "")).startswith(a.intdes)
                 or str(e.get("INTLDES", "")).startswith(short)]
    print(f"  total {len(data)} element sets, {len({e['NORAD_CAT_ID'] for e in data})} objects")
    if not data:
        sys.exit("沒有取得任何資料，請把上面的輸出貼給 Claude 檢查查詢條件")

    os.makedirs(RAW, exist_ok=True)
    jp = os.path.join(RAW, f"spacetrack_gp_history_{a.intdes}.json")
    json.dump(data, open(jp, "w", encoding="utf-8"), indent=1)
    tp = os.path.join(RAW, f"spacetrack_gp_history_{a.intdes}.tle")
    with open(tp, "w", encoding="utf-8", newline="\n") as f:
        for e in data:
            f.write(f"{e['OBJECT_NAME']}\n{e['TLE_LINE1']}\n{e['TLE_LINE2']}\n")
    print("  wrote", os.path.relpath(jp, ROOT), "and", os.path.relpath(tp, ROOT))


if __name__ == "__main__":
    main()
