# find-toro2 — 用 STK 10 尋找 TORO-2 的正確 TLE

TORO-2（Pyras / TASA，8U CubeSat，約 15 kg）於 2025-11-28 18:44 UTC 搭乘 SpaceX **Transporter-15**
（COSPAR 2025-276，Vandenberg SLC-4E，SSO ~510 km）升空，入軌後未收到 beacon。
本專案假設衛星仍在軌、只是 beacon 未開，目標是從 Celestrak / Space-Track 上
Transporter-15 的 **未識別物件（TRANSPORTER-15 OBJECT xx）** 中找出最可能是 TORO-2 的 TLE，
並在實驗室的 STK 10 中建立場景、計算對 NTUT / TASA 地面站的過境時段，供地面站盲追。

## 目前結論（2026-09-17 修正）

**2026-09-16 重大修正：先前的主候選 OBJECT H (66673) 已由 SatNOGS / Libre Space 以射頻觀測與 ikhnos Doppler 分析確認為 PHASMA-LAMARR，
OBJECT R (66681) 為 PHASMA-DIRAC（兩顆都是帆板展開的 3U）。射頻證據優先於軌道動力學推論，H 與 R 排除。**
GCAT 對本次發射的名字指派多處錯誤（H、R、CX、CJ），排名已不再使用 GCAT 的識別與質量。詳見 [docs/method.zh-TW.md §9](docs/method.zh-TW.md)。

**目前最可能是 TORO-2 的物件：TRANSPORTER-15 OBJECT DD，NORAD 66765（2025-276DD）；替代候選 OBJECT CJ，NORAD 66746（自 2026-04-07 起無新 TLE，狀態待查）。**

依據（只用與名字無關的物理量）：

| 群（Space-Track 歷史根數 + NRLMSISE-00 反推 A/m） | 物件 | 對應酬載 |
|--|--|--|
| 低 0.0072–0.0080 m²/kg | CN、DM、CY、AA | CTC-1 ×3、PW-6U、3UCubed-A（貼附電池） |
| 中 0.0094–0.0101 | L、CX | WISDOM B、SPiN-2 |
| 高 0.0136–0.0185 | AB、CZ（成對）、**DD**、**CJ** | TRYAD-1/2（成對）、**TORO-2**、＋一個未知 |

TORO-2 展開態 CAD 的理論 A/m：隨機翻滾 0.0128、大面迎風 0.0182。DD 的 0.0185 對應大面迎風（1.02×），CJ 的 0.0136 對應隨機翻滾（1.06×）。
A/m 分不出兩者，但 DD 有可用 TLE，實務上先追 DD。方法本身已用實驗室的 PARUS-6U1（狀態已知）驗證，誤差 5%。

教訓：A/m 不能單獨定案（H 的 0.021 同樣符合 3U＋帆板）；提出候選前先查 SatNOGS DB 與 community.libre.space 的發射討論串，
已確認的射頻識別收在 [data/identifications.json](data/identifications.json)，排名腳本自動排除。

候選 TLE 見 [results/toro2_candidate_tles.txt](results/toro2_candidate_tles.txt)，完整評分見 [results/candidates_ranked.md](results/candidates_ranked.md)，
過境時段見 [results/stk/pass_schedule_R01.md](results/stk/pass_schedule_R01.md)（重跑 `stk_build_scenario.py` 後 R01 = DD）。

## 每日更新流程

```bash
python scripts/fetch_data.py            # 重抓 Celestrak TLE / SATCAT / GCAT
python scripts/analyze_candidates.py    # 重新排名，輸出候選 TLE 與 STK 用 .tce
python scripts/stk_build_scenario.py    # 在已開啟的 STK 10 建立/更新 FindTORO2 場景，輸出 7 天過境表
```

（可選，需 Space-Track 帳號）`fetch_spacetrack_history.py` → `estimate_ballistic.py` 會重算各物件的 A/m，
`analyze_candidates.py` 偵測到 `results/ballistic_estimate.csv` 時會把它納入評分（權重 0.35）。

需求：Python 3.10+、`pip install -r requirements.txt`、STK 10 已開啟（Connect 走 TCP 5001）。

## 獨立驗證（需自己的 Space-Track 帳號）

```bash
set SPACETRACK_USER=<login>
set SPACETRACK_PASS=<password>
python scripts/fetch_spacetrack_history.py
python scripts/analyze_deployment_order.py
```
檢查部署後前兩週各物件的沿軌相位順序是否與分離時刻對應，確認 OBJECT H 落在「第一顆分離」的位置。方法細節見 [docs/method.zh-TW.md](docs/method.zh-TW.md)。

## 目錄
```
data/raw/        Celestrak TLE / SATCAT、GCAT 目錄、TLE API 原始下載
data/processed/  給 STK ImportTLEFile 用的 .tce（候選 R01~R11、8U 對照組）
scripts/         下載、分析、STK 自動化、Space-Track 驗證腳本
results/         排名結果、候選 TLE、STK 過境報表（results/stk/）
docs/            方法說明
```

## 狀態
- [x] 步驟 1：資料收集（Celestrak 2025-276 全部物件 TLE + SATCAT，GCAT 識別表）
- [x] 步驟 2：候選物件分析與排名（OBJECT H / 66673 居首）
- [x] 步驟 3：STK 10 場景 FindTORO2 建立、NTUT / TASA 過境計算
- [x] 步驟 4：候選 TLE 交付（results/toro2_candidate_tles.txt）
- [x] 步驟 5：Space-Track 歷史 TLE 驗證（相位回推無鑑別力；衰減率支持 H 為失控 8U，備援改為 R）
- [x] 步驟 6：SatNOGS 回覆：H = PHASMA-LAMARR、R = PHASMA-DIRAC，候選改為 DD（備援 CJ）
- [ ] 步驟 7：Space-Track 查 CJ 狀態與 RCS_SIZE；SatNOGS 對 DD 排觀測；地面站追蹤結果回饋
