# find-toro2 — 用 STK 10 尋找 TORO-2 的正確 TLE

TORO-2（Pyras / TASA，8U CubeSat，約 15 kg）於 2025-11-28 18:44 UTC 搭乘 SpaceX **Transporter-15**
（COSPAR 2025-276，Vandenberg SLC-4E，SSO ~510 km）升空，入軌後未收到 beacon。
本專案假設衛星仍在軌、只是 beacon 未開，目標是從 Celestrak / Space-Track 上
Transporter-15 的 **未識別物件（TRANSPORTER-15 OBJECT xx）** 中找出最可能是 TORO-2 的 TLE，
並在實驗室的 STK 10 中建立場景、計算對 NTUT / TASA 地面站的過境時段，供地面站盲追。

## 目前結論（2026-09-10）

**最可能是 TORO-2 的物件：TRANSPORTER-15 OBJECT H，NORAD 66673，COSPAR 2025-276H。**

| 依據 | 內容 |
|--|--|
| 部署時序 | TORO-2 是本次第一顆分離的酬載（19:39:09 UTC）；GCAT（J. McDowell）依部署時序與早期 TLE 相位把 OBJECT H 識別為 TORO2 |
| 物理等級 | 11 個未識別物件中只有 H（15 kg, 8U）與 CTC-1 A/B/C（21 kg, 8U）屬 8U 級，其餘是 1U/3U/6U |
| 阻力行為 | H 高度已掉到 ~491 km（同級受控 8U 在 500~511 km），B* 為同級中位數 2.5 倍 → 符合失控翻滾、姿態未建立的情境 |

**以 Pyras 實際規格（質量約 11 kg、帆板已展開、帆板面 8U+8U+4U）做的獨立物理檢驗**（[docs/method.zh-TW.md §7](docs/method.zh-TW.md)）：
用 Space-Track 歷史根數的衰減率加 NRLMSISE-00 大氣模型反推面積質量比，並以 CAD 展開態模型（`8u_asm_0312.stp`，輪廓投影法）算 TORO-2 的理論值：隨機翻滾平均 0.0128、大面迎風 0.0182 m²/kg（[docs/method.zh-TW.md §7.5](docs/method.zh-TW.md)）。Pyras 提供的精確模型 `00_mass_asm.stp` 檔案截斷不完整，待補。

| 物件 | 反推 A/m (m²/kg) | 判讀（CAD 展開態：翻滾平均 0.0128、大面迎風 0.0182） |
|--|--|--|
| **OBJECT H (66673)** | **0.021** | 落在「帆板展開、大面偏向迎風」區間（平板 Cd > 2.2 可解釋差額） |
| OBJECT R (66681) | 0.024 | 略高於上限，第一備援 |
| OBJECT DM / CN | 0.008 / 0.007 | 和受控 8U 一樣（0.005~0.009），對應帆板未展或受控，不像失聯的 TORO-2 |

**方法驗算**：用本實驗室狀態已知的 PARUS-6U1（68456，6U、7 kg、帆板未展、確定在翻滾）跑同一套演算法，理論 0.0079 對反推 0.0075 m²/kg，誤差 5%（[docs/method.zh-TW.md §7.4](docs/method.zh-TW.md)）。

GCAT 標示的 15 kg 只是 8U 的標稱值，未識別物件的 GCAT 質量是隨指派名字而來，所以這項 A/m 檢驗刻意不依賴它。
Space-Track 的相位回推法在此資料下無鑑別力（§6），且 OBJECT H 的歷史裡有一段 2025-12-24~29 的交叉標記壞根數，腳本已自動剔除。

備援順位：**OBJECT R (66681)** → OBJECT AB / CZ (66691 / 66761，TRYAD) → OBJECT DM (66773) → OBJECT CN (66750)。（自動評分把 TRYAD 排在 R 之前，因為 R 的 A/m 略超出 CAD 上限；但 R 是唯一另一個高阻力的 8U 級物件，實務上仍建議先追 R。）
候選 TLE 見 [results/toro2_candidate_tles.txt](results/toro2_candidate_tles.txt)，
完整評分見 [results/candidates_ranked.md](results/candidates_ranked.md)，
未來 7 天過境時段見 [results/stk/pass_schedule_R01.md](results/stk/pass_schedule_R01.md)。

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
- [ ] 步驟 6：地面站實際追蹤結果回饋
