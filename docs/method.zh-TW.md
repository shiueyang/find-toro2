# 方法說明：從 Transporter-15 未識別物件中找出 TORO-2

## 1. 背景與假設

- **TORO-2**（Pyras Technology / TASA，「TORO-8U-1」，8U CubeSat，約 15 kg）搭乘 SpaceX Transporter-15
  於 2025-11-28 18:44 UTC 自 Vandenberg SLC-4E 升空，COSPAR 國際編號 **2025-276**，目標軌道約 510 km SSO（傾角 97.4°）。
- 依 SpaceX 部署時程，TORO-2 是本次 140 個酬載中 **第一顆分離** 的（GCAT 記錄分離時刻 19:39:09 UTC，T+55 min；
  Spaceflight Now 報導「deployment began with the Toro2 spacecraft a little more than 54 minutes after liftoff」）。
- 入軌後未收到 beacon。本專案的工作假設：衛星仍在軌、結構完整，只是 OBC/beacon 未啟動或姿態未建立。
  因此目標是找到它在美軍 18 SDS 目錄中對應的「未識別物件」，取得 TLE 讓地面站盲追。

## 2. 資料來源

| 來源 | 用途 | 取得方式 |
|--|--|--|
| Celestrak GP `INTDES=2025-276` | 全部 122 個仍有 TLE 之物件的最新 TLE | 實驗室網路連 celestrak.org 逾時，改走 r.jina.ai 唯讀代理（`scripts/fetch_data.py` 自動 fallback） |
| Celestrak SATCAT | 物件名稱、擁有者、是否已衰減 | 同上 |
| GCAT（Jonathan McDowell, planet4589.org） | 每個物件的 **分離時刻**、質量、尺寸、以及他對未識別物件的名字推定 | 直接下載 satcat.tsv / psatcat.tsv，篩 2025-276 |
| tle.ivanstanojevic.me | 備援 TLE API | 直接 |
| Space-Track gp_history | 部署後前兩週歷史 TLE（獨立驗證用） | **需使用者自己的帳號**，`scripts/fetch_spacetrack_history.py` 從環境變數讀帳密 |

## 3. 未識別物件清單

Celestrak 上 2025-276 目前有 11 個 `TRANSPORTER-15 OBJECT xx` 仍有 TLE（H, L, R, AA, AB, CN, CX, CY, CZ, DD, DM），
另有 OBJECT CJ 自 2026-04 起無新 TLE（可能已衰減或未追蹤）。

## 4. 排名邏輯（`scripts/analyze_candidates.py`）

四個面向各給 0~1 分後加權：

| 面向 | 權重 | 內容 |
|--|--|--|
| A 物理等級 | 0.35 | GCAT 質量/尺寸是否為 8U、~15 kg。11 個未識別物件中只有 OBJECT H（15 kg）與 CTC-1 A/B/C（21 kg）屬 8U 級；其餘是 1U/3U/6U |
| B GCAT 識別 | 0.35 | McDowell 依 SpaceX 部署時序 + 早期 TLE 沿軌相位，把 OBJECT H 指派為 TORO2（帶 `?` 表示推定） |
| C 阻力一致性 | 0.20 | B* 相對「同級 8U 已識別物件」中位數的比值落在 0.5~3 倍內即合理。OBJECT H 約 2.5 倍、高度已掉到 ~491 km（同級受控衛星在 500~511 km）：**阻力偏高，符合失控翻滾 + 帆板展開的情境**，與 beacon 未開互相印證 |
| D 部署時序 | 0.10 | 分離時刻與 TORO-2 的差；此項的真正驗證需歷史 TLE（見 §6） |

結果：**OBJECT H / NORAD 66673 / 2025-276H** 總分 1.0，第二名 OBJECT DM（CTC-1A）0.46。詳見 `results/candidates_ranked.md`。

## 5. STK 10 場景（`scripts/stk_build_scenario.py`）

透過 STK Connect（TCP 5001）自動化，不依賴 pywin32：

1. 建立 / 重用場景 `FindTORO2`，分析時段 = 現在起 7 天。
2. 地面站：`NTUT`（25.04295°N, 121.53612°E, 50 m）、`TASA`（24.80165°N, 121.00111°E, 40 m），最低仰角 10°。
   座標取自實驗室既有場景 `6u/ntut.f`、`6u/tasa.f`。
3. `ImportTLEFile` 載入 11 個候選（`R01_...` = 最可能）與同級 8U 對照組（`REF_...`），SGP4 自動推算。
4. 對每個候選 × 地面站計算 Access，輸出過境區間與主候選的 AER（方位 / 仰角 / 距離 / 距離率）報表到 `results/stk/`。
5. 場景存到 `~/Documents/STK 10/FindTORO2/`，可直接在 STK GUI 打開檢視。

## 6. Space-Track 歷史 TLE 的獨立驗證（2026-09-10 已執行）

```bash
$env:SPACETRACK_USER="<login>"; $env:SPACETRACK_PASS="<password>"
python scripts/fetch_spacetrack_history.py        # 10,909 組根數、113 個物件，2025-12-17 ~ 2026-01-10
python scripts/analyze_deployment_order.py         # results/deployment_order_check.md
```

**關鍵限制：這批物件到 2025-12-18（部署後第 20 天）才進公開目錄**，沒有更早的根數。
Space-Track 查詢上的兩個坑：`gp_history` 的 `INTLDES` 欄是空的、`OBJECT_ID` 不支援 `^` 前綴運算子，
要用 `NORAD_CAT_ID/66666--66790` 範圍加 `EPOCH/>date/EPOCH/<date`。

### 6.1 相位回推（部署順序）→ 無法判別

把每個物件在 12-19 ~ 01-08 之間的沿軌相位（相對參考物件 BLACK KITE-1）線性外推回部署時刻：

| 指標 | 值 |
|--|--|
| 直接用 12-19 相位 vs 分離時刻的 Spearman ρ | −0.01 |
| 回推到部署時刻後的 Spearman ρ | 0.31 |
| 線性擬合斜率 | 0.44°/min → 整個 30 分鐘部署序列只對應約 13° |
| 擬合殘差 σ | 15.7° |

殘差與整段部署序列的訊號同量級，所以 **這份資料不能獨立確認、也不能否定 GCAT 的指派**。
OBJECT H 的回推相位落在「早分離」那一側（殘差 −10°，0.6σ），與第一顆分離相容，但不具鑑別力。
二次多項式外推 20 天會發散（σ 94°），不採用。

### 6.2 半長軸衰減率（阻力）→ 支持「失控翻滾的 8U」

| 等級（已識別物件） | n | da/dt 中位數 km/day |
|--|--|--|
| 8U 級（10–25 kg，L ≥ 0.35 m） | 14 | −0.046 |
| 6U 級 | 15 | −0.053 |
| 3U 級 | 43 | −0.048 |

| 未識別 8U 級物件 | GCAT 推定 | da/dt km/day | 相對 8U 中位數 |
|--|--|--|--|
| **OBJECT H (66673)** | TORO2, 15 kg | **−0.113** | 2.5× |
| OBJECT R (66681) | CTC-1B, 21 kg | −0.130 | 2.8× |
| OBJECT DM (66773) | CTC-1A, 21 kg | −0.043 | 0.9× |
| OBJECT CN (66750) | CTC-1C, 21 kg | −0.040 | 0.9× |

11 個未識別物件中，只有 H 和 R 這兩個 8U 級物件的阻力是同級受控衛星的 2.5 倍以上，
符合「未建立姿態、帆板展開後翻滾」。這正是 beacon 未開的 TORO-2 應有的樣子；DM / CN 的阻力和受控 8U 一樣，可信度降低。

### 6.3 綜合結論與追蹤順序

1. **OBJECT H / 66673**：GCAT 指派 + 質量 15 kg 完全吻合 + 高阻力（失控特徵）+ 回推相位偏早。主候選。
2. **OBJECT R / 66681**：唯一另一個「高阻力 8U 級」未識別物件（GCAT 認為是 21 kg 的 CTC-1B）。若 H 追不到，第一備援。
3. OBJECT DM / 66773、OBJECT CN / 66750：8U 級但阻力正常（像受控衛星），排後。

## 7. 以 TORO-2 實際規格反推面積質量比（2026-09-15，`scripts/estimate_ballistic.py`）

Pyras 提供的實際規格：**質量約 11 kg、帆板已展開、帆板面 8U + 8U + 4U**。GCAT 的 15 kg 只是 8U 的標稱值（MassFlag `?`），
且未識別物件的 GCAT 質量是「跟著指派的名字來的」，用它排除候選有循環論證之嫌。
因此改用與名字無關的物理量：由 Space-Track 歷史根數的半長軸衰減率反推 A/m。

### 7.1 方法

- 近圓軌道 `da/dt = −ρ (Cd A/m) √(μa)`，取 Cd = 2.2。
- ρ 用 NRLMSISE-00，沿 SGP4 軌道每圈取 48 點平均，太空天氣（F10.7、Ap）取 Celestrak SW 檔當日值；
  視窗 2025-12-19 ~ 2026-01-08 內 F10.7 在 114 ~ 189 之間。
- da/dt 用 Theil–Sen 中位數斜率；**先剔除壞根數**：OBJECT H 在 2025-12-24 ~ 12-29 有 17 組交叉標記（cross-tag）的根數，
  高度在 501 ~ 514 km 亂跳、偏心率暴增 4 倍、B* 正負互換。不剔除的話最小平方擬合會得到「高度上升」的荒謬結果。
- TORO-2 理論 A/m（隨機翻滾的平均投影面積 = 總表面積 / 4，本體假設 1×2×4U = 0.1×0.2×0.4 m）：

| TORO-2 姿態假設 | A/m (m²/kg) |
|--|--|
| 翻滾 + 帆板展開（Pyras 判斷的狀態） | **0.0155** |
| 翻滾、帆板未展開 | 0.0064 |
| 受控、最小面迎風 | 0.0018 |
| 最大面迎風（帆板 + 本體） | 0.0255 |

### 7.2 校準（已識別物件的反推 A/m）

| 類別 | 反推 A/m | 說明 |
|--|--|--|
| 受控 8U：BRO-17 / BRO-20 / Black Kite-1 / T.MicroSat-1 | 0.0057 / 0.0062 / 0.0085 / 0.0092 | 姿態受控的同級衛星 |
| 3U Dove（Flock 4H，含展開帆板） | 0.0094 ~ 0.0098 | 與理論翻滾值 ~0.011 相近，絕對尺度可信 |
| 6U + 展開帆板（AE5RA/B/C） | 0.019 ~ 0.021 | 大帆板、高阻力姿態 |
| PocketQube（Sari、Hunity） | 0.031 ~ 0.037 | 極小質量，預期最高 |

### 7.3 未識別物件

| NORAD | 物件 | GCAT 推定 | 剔除壞根數 | A/m (m²/kg) | ÷ TORO-2 翻滾展開 | 判讀 |
|--|--|--|--|--|--|--|
| 66681 | OBJECT R | CTC-1B (16U, 21 kg) | 0 | 0.0242 | 1.57 | 高阻力；若是 21 kg 16U，需大帆板全展且翻滾 |
| **66673** | **OBJECT H** | **TORO2** | 17 | **0.0210** | **1.36** | **與 11 kg + 帆板展開 + 翻滾一致（模型誤差內）** |
| 66765 | OBJECT DD | WISDOM B (3U, 5 kg) | 0 | 0.0185 | 1.20 | 若真是 3U 光體，需翻滾 + 大帆板 |
| 66761 / 66691 | OBJECT CZ / AB | TRYAD 2 / 1 (6U) | 0 / 4 | 0.0147 / 0.0144 | 0.95 / 0.93 | 6U + 帆板翻滾也會落在此區 |
| 66759 | OBJECT CX | Phasma-Lamarr (3U) | 15 | 0.0101 | 0.65 | |
| 66676 | OBJECT L | HCT-SAT2 (1U) | 17 | 0.0094 | 0.61 | |
| 66690 / 66760 | OBJECT AA / CY | SPiN 2 / PW-6U | 3 / 10 | 0.0080 / 0.0078 | 0.52 / 0.50 | 受控或帆板未展 |
| 66773 / 66750 | OBJECT DM / CN | CTC-1A / 1C | 0 / 10 | 0.0077 / 0.0072 | 0.50 / 0.46 | 與受控 8U/16U 同級，**不像失控的 TORO-2** |

結論：以 A/m 這個與名字無關的量來看，OBJECT H 的 0.021 明確落在「帆板展開且翻滾」的區間（受控 8U 只有 0.006 ~ 0.009），
和 Pyras「帆板已展開、beacon 未開」的判斷一致；DM / CN 若是 TORO-2 就必須是受控或帆板未展，機率低。
R 的阻力比 H 更高一點，仍是第一備援。

### 7.4 方法驗算：PARUS-6U1（NORAD 68456，2026-067AS）

用一顆**狀態已知**的衛星驗證同一套演算法。PARUS-6U1 是本實驗室的 6U，2026-03-30 搭 Transporter-16 升空：
質量 7 kg、帆板未展開、ADCS 只有 detumbling 有效、算不出姿態四元數；
beacon 資料（jamesxie98021.github.io/parus_6U1_web）顯示 5~6 月 IMU 角速率中位數 5~10 deg/s，9 月仍 2~7 deg/s，
TUMB / DES / EKF 旗標全程為 0——確定是隨機翻滾，「總表面積 ÷ 4」的模型適用。

```bash
python scripts/fetch_spacetrack_history.py --intdes 2026-067 --norad 68416-68470,68471-68530,68800-68840 --start 2026-04-15 --end 2026-05-10 --sanity 68456
python scripts/estimate_ballistic.py --intdes 2026-067 --target 68456 --label PARUS-6U1 --mass 7 --body 0.1 0.2 0.3 --panel-faces 0 --t1 2026-04-16 --t2 2026-05-09
```

| 項目 | 值 |
|--|--|
| 理論 A/m（6U 0.1×0.2×0.3 m，表面積 0.22 m² ÷ 4 ÷ 7 kg） | **0.0079 m²/kg** |
| 觀測：66 組根數、無壞根數、平均高度 516 km、軌道平均密度 4.97e-13 kg/m³、da/dt −0.037 km/day | **0.0075 m²/kg** |
| 觀測 ÷ 理論 | **0.95** |
| 同批對照：TORO-3（Pyras 8U，12 kg，受控） / BRO-19 / Black Kite-2 / AISSAT-4 | 0.0086 / 0.0052 / 0.0101 / 0.0090 |

結論：對一顆已知在翻滾、質量與外形都確定的衛星，演算法的絕對誤差只有 5%，遠小於先前保守估的 ±30%。
這表示 §7.3 對 OBJECT H 得到的 0.021 m²/kg 是可信的絕對值，而 H 的 0.021 與「11 kg、帆板展開、翻滾」的 0.0155
相差 1.36 倍，最可能的解釋是實際帆板面積或本體表面積比我假設的略大（或翻滾時帆板面較常朝向來流）；
反過來說，若 H 是帆板未展或受控的 TORO-2（0.006 以下），與觀測相差 3 倍以上，可以排除。

### 7.5 用 CAD 模型取代手算投影面積（2026-09-15，`scripts/projected_area.py`）

Pyras 提供的精確模型 `00_mass_asm.stp`（Creo 匯出，359 MB）**檔案不完整**：在第 7,419,036 行中途截斷、
沒有 `END-ISO-10303-21`，FreeCAD 讀取有 1,079,729 個未解析參照，無法使用，需重新匯出或重新複製。
暫以同一資料夾中 2026-03-12 的展開態組合件 `8u_asm_0312.stp`（18 MB，88 個實體，包絡 327 × 498 × 454 mm）代替。

方法：FreeCAD 1.1 headless 讀 STEP、1 mm 公差網格化（47 萬三角形）→ 表面均勻取樣 400 萬點 →
對球面均勻分布的 300 個方向，把點投影到垂直平面、以 2 mm 像素計數輪廓面積。這會正確處理帆板與本體的互相遮蔽，
而「總表面積 ÷ 4」不會。

| 量（11 kg） | 面積 m² | A/m m²/kg |
|--|--|--|
| **隨機翻滾平均投影（輪廓法）** | **0.1405** | **0.0128** |
| 最大投影（大面迎風） | 0.1999 | 0.0182 |
| 最小投影 | 0.0403 | 0.0037 |
| 沿 +X / +Y / +Z 軸 | 0.1965 / 0.1044 / 0.0295 | 0.0179 / 0.0095 / 0.0027 |
| 凸包表面積 ÷ 4（= 我先前的手算 0.0155） | 0.1700 | 0.0155 |

意義：
- 手算的 0.0155 其實就是凸包 ÷ 4，高估了翻滾平均約 20%；正確的隨機翻滾平均是 **0.0128**。
- OBJECT H 觀測到的 0.021 是翻滾平均的 1.64 倍，卻只比「最大面永遠迎風」的 0.0182 高 15%。
  平板正對來流時自由分子流的 Cd 約 2.6~3.0 而非 2.2，把這點算進去，0.021 就落在「大面長期迎風」的預期內。
- 這表示 TORO-2 若是 H，**它的姿態並非完全隨機翻滾，而是偏向大面（帆板面）迎風**。
  一顆姿態失控 9 個月的衛星，在渦電流阻尼與重力梯度作用下角速度衰減後，被動地穩定在某個慣量主軸姿態並不罕見；
  PARUS-6U1 仍在 2~10 deg/s 翻滾所以符合隨機模型，TORO-2 可能已慢下來。這是可以用地面站訊號強度變化週期驗證的預測。
- 反過來，帆板未展（≤ 0.0064）或姿態受控（0.0037）仍然被排除；DM / CN 的 0.007~0.008 對應「帆板未展的翻滾」或「受控」。

評分腳本已改用 CAD 值：接受區間 [0.8 × 翻滾平均, 1.25 × 最大投影] = [0.0102, 0.0227] m²/kg。

### 7.6 附帶發現：相位回推的系統偏差

§6.1 回推相位「偏早」的三個物件（R、DD、H）正好是阻力最大的三個。高阻力物件的漂移率隨時間加快，
線性回推 20 天會過度修正，把它們推向「太早分離」——這是方法偏差，不是部署順序的證據，再次確認相位法在此資料下不可用。

## 9. 2026-09-16 修正：OBJECT H 不是 TORO-2

Libre Space / SatNOGS（fredy）回覆：**OBJECT H (66673) = PHASMA-LAMARR、OBJECT R (66681) = PHASMA-DIRAC**，
兩顆都是帆板展開的 3U，依據是 SatNOGS Network 與第三方射頻觀測加 ikhnos Doppler 分析
（community.libre.space PHASMA 討論串第 133 篇，2026-01-28）。這是射頻證據，優先於任何軌道動力學推論。

### 9.1 哪裡錯了

- **GCAT 的名字指派不可信**：H（TORO2）、R（CTC-1B）、CX（Lamarr）、CJ（Dirac）四個都錯，而且 GCAT 漏列 3UCubed-A。
  §1、§4 的「B GCAT 識別」與「A 物理等級」（質量隨指派名字而來）都是建立在錯誤前提上，權重已歸零。
- **A/m 無法單獨定案**：H 的 0.021 m²/kg 既符合「8U 11 kg、帆板展開、大面迎風」，也符合「3U 5 kg、帆板展開、翻滾」。
  事後看，H 與 R 的 A/m 幾乎相同（0.021 / 0.024），本該懷疑它們是同設計的一對——這正是 PHASMA 的雙星。
- 教訓：提出候選前，**先查 SatNOGS DB（每個未識別 NORAD 的條目、各衛星臨時編號 98xxx 的 `norad_follow_id`）與
  community.libre.space 的發射討論串**，把射頻已確認的物件排除。現在寫進 `data/identifications.json`，排名腳本自動排除。

### 9.2 SatNOGS DB 現況（2026-09-17）

- 有條目且已對應目錄物件的未識別 NORAD：只有 66673、66681（PHASMA）。其餘 9 個未識別物件沒有任何 SatNOGS 條目。
- 臨時編號仍 `follow=None`（尚未對應）的酬載：TORO-2 (98495)、SPIN-2 (98471)、TRYAD-1/2 (98514/98472)、CTC-1A/B/C (98482/81/80)、
  PW-6U (98513)、3UCUBED-A (98517)。WISDOM B 沒有條目。
- HCT-SAT2 (98470) 對應到 66671——而 18 SDS 把 66671 命名為 ANISCSAT-1，兩者之一有誤；OBJECT L 因此不一定是 HCT-SAT2。
- 3UCubed-A 有在發射（437.01 MHz 每 60 秒 beacon，訊號太弱無法解碼），設計為**本體貼附式**太陽電池（無展開帆板）。

### 9.3 重新配對：只用與名字無關的 A/m

剩下 10 個未識別物件（L、AA、AB、CN、CX、CY、CZ、DD、DM，加上 4 月起無 TLE 的 CJ）對 10 個未對應的酬載名字
（TORO-2、SPiN-2、TRYAD-1、TRYAD-2、CTC-1A/B/C、PW-6U、3UCubed-A、WISDOM B）。以 §7 的 A/m 分群：

| 群 | 物件（A/m m²/kg） | 可能的酬載 | 說明 |
|--|--|--|--|
| 低 0.0072–0.0080 | CN、DM、CY、AA | CTC-1 ×3（16U, 21 kg）、PW-6U（6U）、3UCubed-A（3U 貼附電池） | DM/CN 成對，符合 CTC-1 雙胞胎 |
| 中 0.0094–0.0101 | L、CX | WISDOM B（其雙胞胎 WISDOM A 實測 0.0090）、SPiN-2（3U） | |
| 高 0.0136–0.0185 | **AB、CZ**（0.0144/0.0147，成對）、**DD**（0.0185）、**CJ**（0.0136） | TRYAD-1/2（成對 → AB/CZ）、**TORO-2**、＋一個未知 | 高群 4 個物件對 3 個名字，多出的一個只能是 SPiN-2 或 PW-6U 帶大型展開物 |

TORO-2 的 CAD 理論值：隨機翻滾 0.0128、大面迎風 0.0182（§7.5）。
- **OBJECT DD (66765)**：0.0185 = 大面迎風值的 1.02 倍；目前有 TLE；高度 489 km（本次發射掉最快的三顆之一，另兩顆就是 PHASMA）。
- **OBJECT CJ (66746)**：0.0136 = 隨機翻滾值的 1.06 倍；但 Space-Track 自 2026-04-07 起沒有新根數，原因待查（不會是再入，可能是交叉標記合併或失追）。

兩者各自完美對應一種姿態假設，A/m 分不出來。PARUS-6U1 的經驗（5 個月後仍 2~10 deg/s 翻滾）讓「隨機翻滾」的先驗略高，
但 DD 有可用 TLE、CJ 沒有，所以**實務上先追 DD**。

### 9.4 待辦

1. Space-Track：查 66746 的最後根數與 satcat 狀態（`scripts/spacetrack_query.py`），確認 CJ 是失追還是被合併。
2. Space-Track satcat 的 `RCS_SIZE`：8U＋展開帆板（包絡 0.33 × 0.5 × 0.45 m）與 3U＋帆板可能落在不同等級，用 H/R、BRO、DD、CJ 校準。
3. 請 SatNOGS 對 OBJECT DD 排觀測；並請他們確認 SPiN-2 (98471) 的訊號是否曾以 Doppler 對應到 DD 或 CJ——若 SPiN-2 是其中一個，TORO-2 就是另一個。

## 8. 地面站操作建議（2026-09-16 起改追 OBJECT DD，備援 CJ 視 Space-Track 狀態而定）

- 先用 `results/toro2_candidate_tles.txt` 第一組（OBJECT H）追蹤；過境時段見 `results/stk/access_R01_*`。
- OBJECT H 阻力大、TLE 沿軌誤差累積快，**每天重抓 TLE**（`fetch_data.py` → `analyze_candidates.py` → `stk_build_scenario.py`）。
- 若連續數次過境都無訊號，依序改追 R02（OBJECT DM）、R06（OBJECT R）、R07（OBJECT CN）—— 這三個是另外的 8U 級物件（CTC-1 A/B/C）。
- 若衛星處於低功率 / 翻滾狀態，訊號可能斷續；建議在 AER 報表仰角最高的幾分鐘內以 Doppler 掃頻方式搜尋。
