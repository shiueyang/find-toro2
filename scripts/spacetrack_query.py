"""
用自己的 Space-Track 帳號送任意查詢（帳密只從環境變數 SPACETRACK_USER / SPACETRACK_PASS 讀）。

用法：
  python scripts/spacetrack_query.py "class/satcat/NORAD_CAT_ID/66746"
  python scripts/spacetrack_query.py "class/gp_history/NORAD_CAT_ID/66746/EPOCH/>2026-03-01/orderby/EPOCH asc" --fields EPOCH,MEAN_MOTION,BSTAR,OBJECT_NAME
  python scripts/spacetrack_query.py "class/gp/NORAD_CAT_ID/66746"
選項：--fields 逗號分隔只印這些欄位；--save 檔名 把完整 JSON 存到 data/raw/
"""
import argparse, json, os, sys, requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.space-track.org"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="basicspacedata/query/ 之後的路徑")
    ap.add_argument("--fields", default=None)
    ap.add_argument("--save", default=None)
    a = ap.parse_args()
    user, pw = os.environ.get("SPACETRACK_USER"), os.environ.get("SPACETRACK_PASS")
    if not user or not pw:
        sys.exit("請先設定環境變數 SPACETRACK_USER / SPACETRACK_PASS")
    s = requests.Session()
    r = s.post(f"{BASE}/ajaxauth/login", data={"identity": user, "password": pw}, timeout=60)
    r.raise_for_status()
    if "Failed" in r.text:
        sys.exit("Space-Track 登入失敗")
    url = f"{BASE}/basicspacedata/query/{a.path}/format/json"
    print("GET", url)
    r = s.get(url, timeout=300)
    r.raise_for_status()
    rows = r.json()
    if isinstance(rows, dict):
        print(rows); return
    print(f"{len(rows)} rows")
    fields = a.fields.split(",") if a.fields else None
    for row in rows[:200]:
        print({k: row.get(k) for k in fields} if fields else row)
    if a.save:
        p = os.path.join(ROOT, "data", "raw", a.save)
        json.dump(rows, open(p, "w", encoding="utf-8"), indent=1)
        print("saved", p)


if __name__ == "__main__":
    main()
