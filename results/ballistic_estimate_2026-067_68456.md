# 面積質量比（A/m）估計：衰減率 + NRLMSISE-00（2026-067，2026-04-16 ~ 2026-05-09，Cd = 2.2）

PARUS-6U1 規格：質量 7.0 kg，本體 0.1×0.2×0.3 m，展開帆板單面總面積 0.00 m²。

| PARUS-6U1 姿態假設 | 理論 A/m (m²/kg) |
|--|--|
| 翻滾 + 帆板展開 | 0.0079 |
| 翻滾、帆板未展開 | 0.0079 |
| 受控、最小面迎風 | 0.0029 |
| 最大面迎風（帆板+本體） | 0.0086 |

太空天氣（2026-04-16~2026-05-09）：F10.7 obs / 81 日平均 / Ap = 109/124/2, 114/125/20, 144/128/6, 146/129/8, 125/127/4

## 驗算目標 PARUS-6U1（NORAD 68456）

- 視窗內根數 66 組（剔除 0 組），平均高度 516 km，軌道平均密度 4.97e-13 kg/m³
- 半長軸衰減率 da/dt = -0.0370 km/day
- **反推 A/m = 0.0075 m²/kg**，為「翻滾 + 帆板展開」理論值的 0.95 倍；最接近的假設：**翻滾 + 帆板展開**
- 各假設的比值：翻滾 + 帆板展開 ×0.95、翻滾、帆板未展開 ×0.95、受控、最小面迎風 ×2.62、最大面迎風（帆板+本體） ×0.87

## 未識別物件

| NORAD | Celestrak | GCAT 推定 (kg, flag) | 根數 用/剔除 | da/dt km/day | 高度 km | ρ kg/m³ | **A/m m²/kg** | / PARUS-6U1翻滾展開 | 最接近的 PARUS-6U1 假設 |
|--|--|--|--|--|--|--|--|--|--|
| 68440 | TRANSPORTER-16 OBJECT AA | Harbinger (5.0?) | 63/0 | -0.1347 | 512 | 5.34e-13 | **0.0253** | 3.22 | 最大面迎風（帆板+本體） |
| 68467 | TRANSPORTER-16 OBJECT BD | ERMIS 1 (10.0?) | 63/0 | -0.1081 | 515 | 5.10e-13 | **0.0213** | 2.71 | 最大面迎風（帆板+本體） |
| 68438 | TRANSPORTER-16 OBJECT Y | Phobos (5.0?) | 62/0 | -0.1073 | 512 | 5.34e-13 | **0.0202** | 2.57 | 最大面迎風（帆板+本體） |
| 68439 | TRANSPORTER-16 OBJECT Z | Ghost Rider (5.0?) | 68/0 | -0.0974 | 513 | 5.29e-13 | **0.0185** | 2.35 | 最大面迎風（帆板+本體） |
| 68426 | TRANSPORTER-16 OBJECT L | TES-23 (1.0) | 58/0 | -0.0751 | 511 | 5.43e-13 | **0.0139** | 1.77 | 最大面迎風（帆板+本體） |
| 68457 | TRANSPORTER-16 OBJECT AT | Decimalsat-1 (0.25) | 61/0 | -0.0670 | 512 | 5.40e-13 | **0.0125** | 1.59 | 最大面迎風（帆板+本體） |

## 已識別物件（依 A/m 排序，供校準：受控衛星應接近『最小面迎風』，3U Dove 翻滾約 0.01）

| NORAD | 名稱 | GCAT 質量 | Bus | 外形 | da/dt km/day | A/m m²/kg |
|--|--|--|--|--|--|--|
| 68484 | VINDLER 2.2 | 130.0? | Muon Halo | Box+ 2 pan | -0.1338 | 0.0805 |
| 68488 | VINDLER 2.1 | 130.0? | Muon Halo | Box+ 2 pan | -0.0826 | 0.0509 |
| 68475 | UNICORN-2S | 0.75? | PocketQube 3P | Box+2 pan | -0.0556 | 0.0351 |
| 68477 | UNICORN-2R | 0.75? | PocketQube 3P | Box+2 pan | -0.0550 | 0.0349 |
| 68446 | HADES-SA (SPINNYONE) | 0.25 | PocketQube 1P | Box+2 ant | -0.1164 | 0.0230 |
| 68492 | LEMUR-2-EMARCHIA | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0361 | 0.0229 |
| 68471 | LEMUR-2-DELOITTE-3 | 10.0 | Cubesat 6U | Box | -0.0311 | 0.0198 |
| 68505 | GEMS2-AMETHYST | 10.0? | Cubesat 6U | Box | -0.0297 | 0.0193 |
| 68479 | LEMUR-2-PEGGY-2004 | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0320 | 0.0192 |
| 68437 | AIGLONSAT-1 | 1.7 | Cubesat 1U | Box | -0.0942 | 0.0178 |
| 68483 | LEMUR-2-CLARA | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0291 | 0.0173 |
| 68493 | LEMUR-2-POLO-11 | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0266 | 0.0169 |
| 68487 | AE1A | 10.0? | Cubesat 6U | Box+ 2 pan | -0.0278 | 0.0165 |
| 68476 | LEMUR-2-JULIA-JOEL | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0274 | 0.0163 |
| 68491 | LEMUR-2-DELOITTE-2 | 10.0 | Cubesat 6U | Box | -0.0251 | 0.0159 |
| 68429 | TROOP-F3 | 10.0? | Cubesat 6U | Box+ 4 pan | -0.0751 | 0.0141 |
| 68473 | VIGORIDE-7 | 363.0 | Vigoride | Box | -0.0713 | 0.0135 |
| 68480 | LEMUR-2-IRINA | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0225 | 0.0132 |
| 68489 | LEMUR-2-CARROLLEMO | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0207 | 0.0130 |
| 68482 | LEMUR-2-SEJONG-3 | 11.0 | Cubesat 6U | Box+ 2 pan | -0.0219 | 0.0128 |
| 68498 | IO-1 | 8.0? | Cubesat 4U | Box+boom | -0.0195 | 0.0122 |
| 68420 | ERMIS-2 | 10.0? | Cubesat 6U | Box | -0.0652 | 0.0119 |
| 68468 | ERMIS-1 | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0559 | 0.0114 |
| 68485 | CAPELLA-20 (ACADIA-10) | 180.0? | Acadia | Box+ pan + Dish+boom | -0.0185 | 0.0111 |
| 68427 | EMISAR | 1.0? | Cubesat 1U | Box | -0.0593 | 0.0110 |
| 68466 | DB-PFW | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0539 | 0.0109 |
| 68496 | ICEYE-X73 | 120.0 | ICEYE | Box + pan | -0.0172 | 0.0104 |
| 68458 | SAL-E | 5.0? | Cubesat 3U | Box | -0.0514 | 0.0103 |
| 68494 | ICEYE-X71 | 120.0 | ICEYE | Box + pan | -0.0165 | 0.0103 |
| 68431 | DISCO-2 | 5.0? | Cubesat 3U | Box | -0.0544 | 0.0102 |
| 68470 | LUNA-2 | 12.0? | Cubesat 6U? | Box | -0.0499 | 0.0102 |
| 68474 | BLACK KITE-2 | 15.0? | Cubesat 8U | Box | -0.0171 | 0.0101 |
| 68497 | ICEYE-X75 | 120.0 | ICEYE | Box + pan | -0.0162 | 0.0098 |
| 68502 | ICEYE-X76 | 120.0 | ICEYE | Box + pan | -0.0157 | 0.0097 |
| 68460 | COSMO | 10.0? | Cubesat 6UXL | Box | -0.0479 | 0.0097 |
| 68501 | N1-ATLAS | 13.0 | Cubesat 6U | Box+ 2 pan | -0.0153 | 0.0097 |
| 68451 | IRIDE-MS1-EAGLET 2-10 | 25.0 | Eaglet | Box+2 pan | -0.0508 | 0.0096 |
| 68461 | IRIDE-MS1-EAGLET 2-12 | 25.0 | Eaglet | Box+2 pan | -0.0488 | 0.0096 |
| 68452 | IRIDE-MS1-EAGLET 2-16 | 25.0 | Eaglet | Box+2 pan | -0.0484 | 0.0095 |
| 68462 | IRIDE-MS1-EAGLET 2-15 | 25.0 | Eaglet | Box+2 pan | -0.0496 | 0.0095 |
| 68450 | IRIDE-MS1-EAGLET 2-13 | 25.0 | Eaglet | Box+2 pan | -0.0499 | 0.0095 |
| 68449 | IRIDE-MS1-EAGLET 2-9 | 25.0 | Eaglet | Box+2 pan | -0.0481 | 0.0095 |
| 68447 | IRIDE-MS1-EAGLET 2-14 | 25.0 | Eaglet | Box+2 pan | -0.0501 | 0.0094 |
| 68500 | ICEYE-X74 | 120.0 | ICEYE | Box + pan | -0.0151 | 0.0094 |
| 68453 | IRIDE-MS1-EAGLET 2-11 | 25.0 | Eaglet | Box+2 pan | -0.0495 | 0.0094 |
| 68504 | ICEYE-X72 | 120.0 | ICEYE | Box + pan | -0.0150 | 0.0092 |
| 68454 | AISSAT 4 | 12.0 | Cubesat 6U | Box | -0.0450 | 0.0090 |
| 68503 | FLYLAB2 | 10.0? | Cubesat 6U | Box+ 4 pan | -0.0133 | 0.0087 |
| 68430 | VEGAFLY-1 | 5.0? | Cubesat 3U? | Box | -0.0462 | 0.0086 |
| 68490 | MIMIR 1 | 93.0 | Mimir | Box+ 2 pan + antenna | -0.0138 | 0.0086 |
| 68481 | TORO-3 | 12.0 | Cubesat 8U | Box | -0.0142 | 0.0086 |
| 68416 | PEAKSAT | 5.0? | Cubesat 3U | Box | -0.0464 | 0.0085 |
| 68417 | JACK-002 | 5.0 | Cubesat 3U | Box | -0.0449 | 0.0082 |
| 68459 | DB GME UT (DB-GLOBE MI*) | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0382 | 0.0077 |
| 68444 | SHARJAH-SAT-2 | 10.0? | Cubesat 6U | Box | -0.0406 | 0.0076 |
| 68456 | PARUS-6U1 | 10.0? | Cubesat 6U | Box | -0.0370 | 0.0075 |
| 68463 | GARAI-B (UNAMUNO) | 115.0 | Innosat | Box | -0.0379 | 0.0075 |
| 68424 | SPACEVAN-002 | 125.0 | MP42 | Box+ 2 pan | -0.0386 | 0.0074 |
| 68495 | GRAVITAS | 2000.0 | Gravitas | Box + 2 pan | -0.0063 | 0.0073 |
| 68432 | NUSAT-53 (JANE GOODALL) | 41.5 | Newsat V | Box | -0.0378 | 0.0072 |
| 68442 | NUSAT-54 (BRANCA MARQU*) | 41.5 | Newsat V | Box | -0.0358 | 0.0071 |
| 68499 | SERT3 | 130.0 | Muon Halo | Box+ 2 pan | -0.0109 | 0.0068 |
| 68486 | VINDLER 2.3 | 130.0? | Muon Halo | Box+ 2 pan | -0.0108 | 0.0066 |
| 68433 | T.MICROSAT-2 | 10.0? | Cubesat 6U | Box | -0.0327 | 0.0066 |
| 68423 | SPOQC | 20.0? | Cubesat 12U | Box | -0.0349 | 0.0065 |
| 68443 | DB-WALI-WMU | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0320 | 0.0064 |
| 68425 | ERMIS-3 | 10.0? | Cubesat 6U | Box | -0.0338 | 0.0063 |
| 68455 | DB CHARMS ND | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0312 | 0.0063 |
| 68464 | FGN-100-D3 | 113.0 | FGN-100 | Box | -0.0319 | 0.0063 |
| 68445 | DB SKYFORGE CORE TU | 0.5 | Thinsat 0.5U | Box+2 pan | -0.0272 | 0.0055 |
| 68421 | VIREON-2 | 20.0? | Cubesat 16U EPIC | Box | -0.0285 | 0.0053 |
| 68422 | BRO-19 | 15.0? | Cubesat 8U | Box | -0.0282 | 0.0052 |
| 68434 | VIREON-1 | 20.0? | Cubesat 16U EPIC | Box | -0.0272 | 0.0051 |
| 68441 | HAWK-14C | 31.0? | Hawk2G | Box + 2 pan | -0.0262 | 0.0050 |
| 68428 | OUT OF THE BOX (OOTB) | 20.0? | Cubesat 16U | Box | -0.0265 | 0.0050 |
| 68448 | HAWK-14A | 31.0? | Hawk2G | Box + 2 pan | -0.0252 | 0.0048 |
| 68436 | HAWK-14B | 31.0? | Hawk2G | Box + 2 pan | -0.0234 | 0.0045 |
| 68465 | HOTSAT-2 | 130.0 | DarkCarb | Box+cone+1 pan? | -0.0216 | 0.0043 |
| 68419 | FEMTO-1 | 1.0? | Cubesat 1U? | Box | -0.0223 | 0.0041 |
| 68469 | (no current TLE) | 250.0? | VW | Trunc cone | -0.0231 | 0.0040 |
| 68435 | ION SCV-019 (ASTOUNDIN*) | 150.0 | ION-SC | Box | -0.0197 | 0.0038 |
| 68478 | FOSSASAT-2E25 | 5.0 | Cubesat 3U | Box | -0.0060 | 0.0036 |
| 68418 | OPTISAT | 10.0? | Cubesat 6U | Box | -0.0189 | 0.0035 |
| 68472 | FLYLAB1 | 15.0? | Cubesat 8U | Box+ 4 pan | -0.0029 | 0.0019 |

## 判讀

- 與「PARUS-6U1：7 kg、翻滾」理論值 0.0079 m²/kg 相差在 ×0.6~×1.6 內（涵蓋大氣模型與 Cd 的不確定度）的未識別物件：**TRANSPORTER-16 OBJECT AT (68457, A/m 0.0125, ×1.59)**。
- A/m 明顯低於理論值的物件，若要是 PARUS-6U1，就必須是「帆板沒展開」或「姿態受控」。
- 絕對值受 NRLMSISE-00 在太陽極大期 500 km 的誤差（±30% 量級）影響；物件之間的比值可靠得多，可用已識別的受控 8U（BRO、Black Kite、Bellbird）與 3U Dove 當量尺。
