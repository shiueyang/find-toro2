"""
Step 1 - 下載 Transporter-15 (COSPAR 2025-276) 相關資料到 data/raw/

來源：
  * Celestrak GP (TLE)      gp.php?INTDES=2025-276&FORMAT=tle
  * Celestrak SATCAT (CSV)  satcat/records.php?INTDES=2025-276&FORMAT=csv
  * GCAT (Jonathan McDowell) satcat.tsv / psatcat.tsv  ->  只保留 2025-276 的列
  * tle.ivanstanojevic.me   TRANSPORTER-15 / TORO 關鍵字（備援）

實驗室網路直接連 celestrak.org 會逾時，因此自動改走 r.jina.ai 唯讀代理。
用法：  python scripts/fetch_data.py
"""
import os, re, sys, requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
INTDES = "2025-276"
TIMEOUT = 60


def get(url, proxy_ok=True):
    """直接抓；失敗時改走 jina 代理並剝掉代理加的標頭。"""
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        if not proxy_ok:
            raise
        print(f"  direct failed ({e.__class__.__name__}); using r.jina.ai proxy")
        r = requests.get("https://r.jina.ai/" + url, timeout=TIMEOUT)
        r.raise_for_status()
        t = r.text
        m = re.search(r"^Markdown Content:\n", t, re.M)
        return t[m.end():] if m else t


def save(name, text):
    p = os.path.join(RAW, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    print(f"  wrote {os.path.relpath(p, ROOT)}  ({len(text.splitlines())} lines)")


def main():
    os.makedirs(RAW, exist_ok=True)

    print("[1/4] Celestrak TLE")
    tle = get(f"https://celestrak.org/NORAD/elements/gp.php?INTDES={INTDES}&FORMAT=tle")
    lines = [l for l in tle.splitlines() if l.strip()]
    assert len(lines) % 3 == 0 and lines[1].startswith("1 "), "TLE format unexpected"
    save(f"celestrak_{INTDES}_tle.txt", "\n".join(lines))

    print("[2/4] Celestrak SATCAT")
    save(f"celestrak_satcat_{INTDES}.csv",
         get(f"https://celestrak.org/satcat/records.php?INTDES={INTDES}&FORMAT=csv"))

    print("[3/4] GCAT satcat / psatcat (large, direct only)")
    for fn in ("satcat", "psatcat"):
        r = requests.get(f"https://planet4589.org/space/gcat/tsv/cat/{fn}.tsv", timeout=300)
        r.raise_for_status()
        rows = r.text.splitlines()
        keep = [rows[0]] + [l for l in rows[1:] if f"\t{INTDES}" in l]
        save(f"gcat_{fn}_{INTDES}.tsv", "\n".join(keep))

    print("[4/4] tle.ivanstanojevic.me backup")
    for key, fn in (("TRANSPORTER-15", "ivanstanojevic_T15.json"), ("TORO", "ivanstanojevic_TORO.json")):
        r = requests.get("https://tle.ivanstanojevic.me/api/tle/",
                         params={"search": key, "page-size": 100}, timeout=30)
        r.raise_for_status()
        save(fn, r.text)


if __name__ == "__main__":
    main()
