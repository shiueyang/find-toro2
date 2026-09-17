# 面積質量比（A/m）估計：衰減率 + NRLMSISE-00（2025-276，2026-01-10 ~ 2026-04-05，Cd = 2.2）

TORO-2 規格：質量 11.0 kg，本體 0.1×0.2×0.4 m，展開帆板單面總面積 0.20 m²。

| TORO-2 姿態假設 | 理論 A/m (m²/kg) |
|--|--|
| 翻滾 + 帆板展開（手算 表面積/4） | 0.0155 |
| 翻滾、帆板未展開 | 0.0064 |
| 受控、最小面迎風 | 0.0018 |
| 最大面迎風（帆板+本體，手算） | 0.0255 |
| CAD 隨機翻滾平均投影（輪廓法） | 0.0128 |
| CAD 最大投影（大面迎風） | 0.0182 |
| CAD 最小投影 | 0.0037 |

太空天氣（2026-01-10~2026-04-05）：F10.7 obs / 81 日平均 / Ap = 110/148/31, 136/142/4, 108/136/14, 110/126/42, 118/126/12

## 未識別物件

| NORAD | Celestrak | GCAT 推定 (kg, flag) | 根數 用/剔除 | da/dt km/day | 高度 km | ρ kg/m³ | **A/m m²/kg** | / TORO-2翻滾展開 | 最接近的 TORO-2 假設 |
|--|--|--|--|--|--|--|--|--|--|
| 66681 | TRANSPORTER-15 OBJECT R | CTC-1B (21.0) | 268/0 | -0.1210 | 507 | 5.31e-13 | **0.0229** | 1.79 | 最大面迎風（帆板+本體，手算） |
| 66673 | TRANSPORTER-15 OBJECT H | TORO2 (15.0?) | 250/0 | -0.1051 | 509 | 5.16e-13 | **0.0205** | 1.60 | CAD 最大投影（大面迎風） |
| 66765 | TRANSPORTER-15 OBJECT DD | WISDOM B (5.0) | 278/0 | -0.0838 | 505 | 5.51e-13 | **0.0153** | 1.20 | 翻滾 + 帆板展開（手算 表面積/4） |
| 66761 | TRANSPORTER-15 OBJECT CZ | TRYAD 2 (12.0) | 281/0 | -0.0714 | 507 | 5.31e-13 | **0.0135** | 1.06 | CAD 隨機翻滾平均投影（輪廓法） |
| 66691 | TRANSPORTER-15 OBJECT AB | TRYAD 1 (12.0) | 300/0 | -0.0662 | 511 | 4.98e-13 | **0.0133** | 1.04 | CAD 隨機翻滾平均投影（輪廓法） |
| 66759 | TRANSPORTER-15 OBJECT CX | Phasma-Lamarr (5.0) | 264/0 | -0.0514 | 509 | 5.13e-13 | **0.0101** | 0.79 | CAD 隨機翻滾平均投影（輪廓法） |
| 66676 | TRANSPORTER-15 OBJECT L | HCT-SAT2 (1.0) | 245/0 | -0.0412 | 514 | 4.73e-13 | **0.0088** | 0.69 | 翻滾、帆板未展開 |
| 66690 | TRANSPORTER-15 OBJECT AA | SPiN 2 (5.0) | 257/0 | -0.0370 | 514 | 4.77e-13 | **0.0078** | 0.61 | 翻滾、帆板未展開 |
| 66760 | TRANSPORTER-15 OBJECT CY | PW-6U (12.0) | 259/0 | -0.0391 | 510 | 5.06e-13 | **0.0078** | 0.61 | 翻滾、帆板未展開 |
| 66773 | TRANSPORTER-15 OBJECT DM | CTC-1A (21.0) | 271/4 | -0.0376 | 509 | 5.12e-13 | **0.0074** | 0.58 | 翻滾、帆板未展開 |
| 66750 | TRANSPORTER-15 OBJECT CN | CTC-1C (21.0) | 271/0 | -0.0342 | 511 | 4.99e-13 | **0.0069** | 0.54 | 翻滾、帆板未展開 |

## 已識別物件（依 A/m 排序，供校準：受控衛星應接近『最小面迎風』，3U Dove 翻滾約 0.01）

| NORAD | 名稱 | GCAT 質量 | Bus | 外形 | da/dt km/day | A/m m²/kg |
|--|--|--|--|--|--|--|
| 66667 | PELICAN-5 | 160.0 | Pelican | Box+2 pan | -0.5214 | 0.0866 |
| 66703 | PELICAN-6 | 160.0 | Pelican | Box+2 pan | -0.4887 | 0.0771 |
| 66747 | (no current TLE) | 250.0? | VW | Trunc cone | -0.4433 | 0.0628 |
| 66787 | LEMUR-2-MYRA | 5.0 | Cubesat 4U | Box | -0.0747 | 0.0383 |
| 66668 | SARI-1 | 0.25 | PocketQube 1P | Box+2 ant | -0.1940 | 0.0347 |
| 66781 | LEMUR-2-CELIJO-SB-PK | 5.0 | Cubesat 4U | Box | -0.0649 | 0.0339 |
| 66783 | LEMUR-2-STARLIGHT | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0632 | 0.0339 |
| 66669 | SARI-2 | 0.25 | PocketQube 1P | Box+2 ant | -0.1815 | 0.0325 |
| 66670 | HUNITY | 0.75 | PocketQube 3P | Box+3 pan | -0.1780 | 0.0322 |
| 66782 | LEMUR-2-FINNIAN | 5.0 | Cubesat 4U | Box | -0.0615 | 0.0314 |
| 66785 | LEMUR-2-VUKASIN | 5.0 | Cubesat 4U | Box | -0.0534 | 0.0271 |
| 66786 | LEMUR-2-HOTSPUR-TOM | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0493 | 0.0265 |
| 66748 | UMBRA-11 | 84.0 | Espasat? | Box + 2 Pan + Dish | -0.1491 | 0.0262 |
| 66784 | LEMUR-2-TARTIFLETTE | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0457 | 0.0245 |
| 66677 | AE5RC | 10.0? | Cubesat 6U | Box+ 2 pan | -0.1052 | 0.0203 |
| 66685 | AE5RA | 10.0? | Cubesat 6U | Box+ 2 pan | -0.1000 | 0.0193 |
| 66746 | (no current TLE) | 5.0 | Cubesat 3U | Box | -0.1052 | 0.0193 |
| 66720 | FLOCK 4H-17 | 5.7 | Cubesat 3U | Box+2 pan | -0.0935 | 0.0183 |
| 66693 | AE5RB | 10.0? | Cubesat 6U | Box+ 2 pan | -0.0887 | 0.0171 |
| 66687 | LEO EXPRESS 3 | 250.0 | Mira | Box | -0.0828 | 0.0168 |
| 66671 | ANISCSAT-1 | 0.25 | PocketQube 1P | Box+2 ant | -0.0830 | 0.0166 |
| 66714 | FLOCK 4H-11 | 5.7 | Cubesat 3U | Box+2 pan | -0.0819 | 0.0160 |
| 66675 | VEERY-0G | 1.0 | Cubesat 1U | Box | -0.0708 | 0.0144 |
| 66741 | BLACK KITE-1 | 15.0? | Cubesat 8U | Box | -0.0663 | 0.0136 |
| 66696 | IRIDE-MS1-EAGLET 2-2 | 25.0 | Eaglet | Box+2 pan | -0.0633 | 0.0129 |
| 66701 | IRIDE-MS1-EAGLET 2-7 | 25.0 | Eaglet | Box+2 pan | -0.0616 | 0.0126 |
| 66697 | IRIDE-MS1-EAGLET 2-3 | 25.0 | Eaglet | Box+2 pan | -0.0635 | 0.0125 |
| 66777 | LUNA-1 | 12.0? | Cubesat 6U? | Box | -0.0670 | 0.0124 |
| 66700 | IRIDE-MS1-EAGLET 2-6 | 25.0 | Eaglet | Box+2 pan | -0.0622 | 0.0121 |
| 66743 | NUSAT-47 | 41.5 | Newsat V | Box | -0.0576 | 0.0116 |
| 66678 | OTTER SDM | 5.0 | Cubesat 3U | Box+ 2 pan | -0.0533 | 0.0111 |
| 66694 | YAM-9 | 150.0? | ARROW | Trapezoid+2 pan | -0.0423 | 0.0109 |
| 66756 | MAUVE | 24.0 | Cubesat 16U | Box+2 pan | -0.0535 | 0.0107 |
| 66723 | FLOCK 4H-20 | 5.7 | Cubesat 3U | Box+2 pan | -0.0539 | 0.0105 |
| 66725 | FLOCK 4H-22 | 5.7 | Cubesat 3U | Box+2 pan | -0.0513 | 0.0104 |
| 66699 | IRIDE-MS1-EAGLET 2-5 | 25.0 | Eaglet | Box+2 pan | -0.0510 | 0.0104 |
| 66711 | FLOCK 4H-8 | 5.7 | Cubesat 3U | Box+2 pan | -0.0509 | 0.0104 |
| 66719 | FLOCK 4H-16 | 5.7 | Cubesat 3U | Box+2 pan | -0.0501 | 0.0104 |
| 66731 | FLOCK 4H-28 | 5.7 | Cubesat 3U | Box+2 pan | -0.0497 | 0.0103 |
| 66721 | FLOCK 4H-18 | 5.7 | Cubesat 3U | Box+2 pan | -0.0497 | 0.0103 |
| 66705 | FLOCK 4H-2 | 5.7 | Cubesat 3U | Box+2 pan | -0.0522 | 0.0103 |
| 66726 | FLOCK 4H-23 | 5.7 | Cubesat 3U | Box+2 pan | -0.0493 | 0.0102 |
| 66733 | FLOCK 4H-30 | 5.7 | Cubesat 3U | Box+2 pan | -0.0495 | 0.0102 |
| 66710 | FLOCK 4H-7 | 5.7 | Cubesat 3U | Box+2 pan | -0.0499 | 0.0102 |
| 66713 | FLOCK 4H-10 | 5.7 | Cubesat 3U | Box+2 pan | -0.0494 | 0.0102 |
| 66698 | IRIDE-MS1-EAGLET 2-4 | 25.0 | Eaglet | Box+2 pan | -0.0493 | 0.0102 |
| 66702 | IRIDE-MS1-EAGLET 2-8 | 25.0 | Eaglet | Box+2 pan | -0.0497 | 0.0102 |
| 66717 | FLOCK 4H-14 | 5.7 | Cubesat 3U | Box+2 pan | -0.0517 | 0.0101 |
| 66707 | FLOCK 4H-4 | 5.7 | Cubesat 3U | Box+2 pan | -0.0483 | 0.0100 |
| 66727 | FLOCK 4H-24 | 5.7 | Cubesat 3U | Box+2 pan | -0.0486 | 0.0100 |
| 66740 | NUSAT-51 (YVONNE BRILL) | 41.5 | Newsat V | Box | -0.0491 | 0.0100 |
| 66718 | FLOCK 4H-15 | 5.7 | Cubesat 3U | Box+2 pan | -0.0479 | 0.0100 |
| 66732 | FLOCK 4H-29 | 5.7 | Cubesat 3U | Box+2 pan | -0.0481 | 0.0100 |
| 66735 | FLOCK 4H-32 | 5.7 | Cubesat 3U | Box+2 pan | -0.0480 | 0.0099 |
| 66734 | FLOCK 4H-31 | 5.7 | Cubesat 3U | Box+2 pan | -0.0475 | 0.0099 |
| 66706 | FLOCK 4H-3 | 5.7 | Cubesat 3U | Box+2 pan | -0.0478 | 0.0098 |
| 66775 | PHI 1 | 20.0? | Cubesat 12U | Box | -0.0507 | 0.0098 |
| 66729 | FLOCK 4H-26 | 5.7 | Cubesat 3U | Box+2 pan | -0.0465 | 0.0097 |
| 66736 | FLOCK 4H-33 | 5.7 | Cubesat 3U | Box+2 pan | -0.0496 | 0.0097 |
| 66772 | IHI-SAT2 | 12.0 | Cubesat 6U | Box | -0.0502 | 0.0096 |
| 66695 | IRIDE-MS1-EAGLET 2-1 | 25.0 | Eaglet | Box+2 pan | -0.0488 | 0.0095 |
| 66712 | FLOCK 4H-9 | 5.7 | Cubesat 3U | Box+2 pan | -0.0468 | 0.0094 |
| 66739 | FLOCK 4H-36 | 5.7 | Cubesat 3U | Box+2 pan | -0.0464 | 0.0093 |
| 66774 | GENA-OT | 15.0? | Cubesat 12U | Box+2 pan | -0.0479 | 0.0093 |
| 66686 | LEMUR-2-STAS-GORBUK | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0441 | 0.0092 |
| 66704 | FLOCK 4H-1 | 5.7 | Cubesat 3U | Box+2 pan | -0.0462 | 0.0092 |
| 66738 | FLOCK 4H-35 | 5.7 | Cubesat 3U | Box+2 pan | -0.0464 | 0.0091 |
| 66728 | FLOCK 4H-25 | 5.7 | Cubesat 3U | Box+2 pan | -0.0462 | 0.0091 |
| 66716 | FLOCK 4H-13 | 5.7 | Cubesat 3U | Box+2 pan | -0.0460 | 0.0091 |
| 66708 | FLOCK 4H-5 | 5.7 | Cubesat 3U | Box+2 pan | -0.0456 | 0.0090 |
| 66749 | PIAST-S1 | 12.0 | Cubesat 6U | Box | -0.0446 | 0.0089 |
| 66692 | NUSAT-52 | 41.5 | Newsat V | Box | -0.0434 | 0.0089 |
| 66757 | PIAST-S2 | 12.0 | Cubesat 6U | Box | -0.0449 | 0.0089 |
| 66715 | FLOCK 4H-12 | 5.7 | Cubesat 3U | Box+2 pan | -0.0443 | 0.0088 |
| 66754 | ICEYE-X61 | 120.0 | ICEYE | Box + pan | -0.0434 | 0.0088 |
| 66768 | LEMUR-2-TEODOR | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0454 | 0.0088 |
| 66730 | FLOCK 4H-27 | 5.7 | Cubesat 3U | Box+2 pan | -0.0440 | 0.0088 |
| 66680 | LEMUR-2-DEANANDMAEVE | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0419 | 0.0088 |
| 66776 | LEMUR-2-LAILA | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0457 | 0.0088 |
| 66766 | T.MICROSAT-1 | 15.0? | Cubesat 8U | Box | -0.0447 | 0.0087 |
| 66709 | FLOCK 4H-6 | 5.7 | Cubesat 3U | Box+2 pan | -0.0433 | 0.0087 |
| 66724 | FLOCK 4H-21 | 5.7 | Cubesat 3U | Box+2 pan | -0.0441 | 0.0086 |
| 66778 | FORESAIL-1 PRIME | 4.0 | Cubesat 3U | Box | -0.0403 | 0.0086 |
| 66688 | WISDOM A | 5.0 | Cubesat 3U | Box | -0.0412 | 0.0086 |
| 66737 | FLOCK 4H-34 | 5.7 | Cubesat 3U | Box+2 pan | -0.0433 | 0.0086 |
| 66722 | FLOCK 4H-19 | 5.7 | Cubesat 3U | Box+2 pan | -0.0420 | 0.0081 |
| 66758 | PIAST-M | 12.0 | Cubesat 6U | Box | -0.0403 | 0.0081 |
| 66771 | GYEONGGISAT-1 | 25.0? | Cubesat 16U | Box | -0.0399 | 0.0078 |
| 66769 | SPEQTRE | 20.0? | Cubesat 12U | Box | -0.0394 | 0.0077 |
| 66742 | MERCURY ONE (M1) | 50.0 | M1 | Box | -0.0345 | 0.0070 |
| 66762 | HYDROGNSS-1 | 65.0 | SSTL-21 | Box +3 pan | -0.0324 | 0.0070 |
| 66684 | MICE-1 | 5.0 | Cubesat 3U | Box | -0.0317 | 0.0066 |
| 66751 | ICEYE-X58 | 120.0 | ICEYE | Box + pan | -0.0317 | 0.0065 |
| 66780 | FOSSASAT-2E24 | 4.0 | Cubesat 3U | Box + 2 pan | -0.0282 | 0.0059 |
| 66753 | ICEYE-X60 | 120.0 | ICEYE | Box + pan | -0.0275 | 0.0059 |
| 66767 | ACCENTURE-1 | 12.0 | Cubesat 6U | Box | -0.0294 | 0.0058 |
| 66674 | BRO-20 | 15.0? | Cubesat 8U | Box | -0.0269 | 0.0058 |
| 66679 | LILIUM-2 | 12.0 | Cubesat 6U | Box | -0.0251 | 0.0055 |
| 66672 | BRO-17 | 15.0? | Cubesat 8U | Box | -0.0249 | 0.0054 |
| 66683 | 6GSTARLAB | 12.0 | Cubesat 6U | Box+2 pan | -0.0243 | 0.0052 |
| 66779 | FOSSASAT-2E22 | 4.0 | Cubesat 3U | Box + 2 pan | -0.0232 | 0.0049 |
| 66764 | NAHLA | 200.0? | VSP-150 | Box + 2 pan | -0.0224 | 0.0047 |
| 66770 | LILIUM-3 | 12.0 | Cubesat 6U | Box | -0.0213 | 0.0043 |
| 66745 | AC1-002 | 140.0 | P10 | Trunc pyramid | -0.0197 | 0.0041 |
| 66689 | AC1-003 | 140.0 | P10 | Trunc pyramid | -0.0193 | 0.0041 |
| 66744 | AC1-001 | 140.0 | P10 | Trunc pyramid | -0.0194 | 0.0041 |
| 66682 | ION SCV-022 | 150.0 | ION-SC | Box | -0.0044 | 0.0024 |
| 66763 | HYDROGNSS-2 | 65.0 | SSTL-21 | Box +3 pan | -0.0025 | 0.0005 |
| 66752 | ICEYE-X59 | 120.0 | ICEYE | Box + pan | 0.0055 | -0.0013 |
| 66666 | FORMOSAT-8A | 380.0 | FS8 | Box + 2 pan | 0.0308 | -0.0142 |
| 66755 | ICEYE-X62 | 120.0 | ICEYE | Box + pan | 0.2540 | -0.0595 |

## 判讀

- 與「TORO-2：11 kg、翻滾」理論值 0.0128 m²/kg 相差在 ×0.6~×1.6 內（涵蓋大氣模型與 Cd 的不確定度）的未識別物件：**TRANSPORTER-15 OBJECT DD (66765, A/m 0.0153, ×1.20)**、**TRANSPORTER-15 OBJECT CZ (66761, A/m 0.0135, ×1.06)**、**TRANSPORTER-15 OBJECT AB (66691, A/m 0.0133, ×1.04)**、**TRANSPORTER-15 OBJECT CX (66759, A/m 0.0101, ×0.79)**、**TRANSPORTER-15 OBJECT L (66676, A/m 0.0088, ×0.69)**、**TRANSPORTER-15 OBJECT AA (66690, A/m 0.0078, ×0.61)**、**TRANSPORTER-15 OBJECT CY (66760, A/m 0.0078, ×0.61)**。
- A/m 明顯低於理論值的物件，若要是 TORO-2，就必須是「帆板沒展開」或「姿態受控」。
- 絕對值受 NRLMSISE-00 在太陽極大期 500 km 的誤差（±30% 量級）影響；物件之間的比值可靠得多，可用已識別的受控 8U（BRO、Black Kite、Bellbird）與 3U Dove 當量尺。
