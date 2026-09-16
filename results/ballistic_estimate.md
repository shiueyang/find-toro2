# 面積質量比（A/m）估計：衰減率 + NRLMSISE-00（2025-12-19 ~ 2026-01-08，Cd = 2.2）

TORO-2 規格（Pyras）：質量 11 kg，本體 8U 假設 0.1×0.2×0.4 m，展開帆板面 8U+8U+4U = 0.20 m²。

| TORO-2 姿態假設 | 理論 A/m (m²/kg) |
|--|--|
| 翻滾 + 帆板展開 | 0.0155 |
| 翻滾、帆板未展開 | 0.0064 |
| 受控、最小面迎風 | 0.0018 |
| 最大面迎風（帆板+本體） | 0.0255 |

太空天氣（2025-12-19~2026-01-08）：F10.7 obs / 81 日平均 / Ap = 114/148/6, 130/146/20, 189/149/8, 160/150/10, 136/150/13

## 未識別物件

| NORAD | Celestrak | GCAT 推定 (kg, flag) | 根數 用/剔除 | da/dt km/day | 高度 km | ρ kg/m³ | **A/m m²/kg** | / TORO-2翻滾展開 | 最接近的 TORO-2 假設 |
|--|--|--|--|--|--|--|--|--|--|
| 66681 | TRANSPORTER-15 OBJECT R | CTC-1B (21.0) | 89/0 | -0.1428 | 514 | 5.91e-13 | **0.0242** | 1.57 | 最大面迎風（帆板+本體） |
| 66673 | TRANSPORTER-15 OBJECT H | TORO2 (15.0?) | 65/17 | -0.1223 | 515 | 5.83e-13 | **0.0210** | 1.36 | 最大面迎風（帆板+本體） |
| 66765 | TRANSPORTER-15 OBJECT DD | WISDOM B (5.0) | 92/0 | -0.1151 | 511 | 6.23e-13 | **0.0185** | 1.20 | 翻滾 + 帆板展開 |
| 66761 | TRANSPORTER-15 OBJECT CZ | TRYAD 2 (12.0) | 96/0 | -0.0899 | 511 | 6.14e-13 | **0.0147** | 0.95 | 翻滾 + 帆板展開 |
| 66691 | TRANSPORTER-15 OBJECT AB | TRYAD 1 (12.0) | 90/4 | -0.0842 | 515 | 5.87e-13 | **0.0144** | 0.93 | 翻滾 + 帆板展開 |
| 66759 | TRANSPORTER-15 OBJECT CX | Phasma-Lamarr (5.0) | 64/15 | -0.0607 | 512 | 6.06e-13 | **0.0101** | 0.65 | 翻滾 + 帆板展開 |
| 66676 | TRANSPORTER-15 OBJECT L | HCT-SAT2 (1.0) | 61/17 | -0.0535 | 517 | 5.70e-13 | **0.0094** | 0.61 | 翻滾、帆板未展開 |
| 66690 | TRANSPORTER-15 OBJECT AA | SPiN 2 (5.0) | 76/3 | -0.0461 | 516 | 5.76e-13 | **0.0080** | 0.52 | 翻滾、帆板未展開 |
| 66760 | TRANSPORTER-15 OBJECT CY | PW-6U (12.0) | 73/10 | -0.0467 | 513 | 6.04e-13 | **0.0078** | 0.50 | 翻滾、帆板未展開 |
| 66773 | TRANSPORTER-15 OBJECT DM | CTC-1A (21.0) | 91/0 | -0.0470 | 512 | 6.12e-13 | **0.0077** | 0.50 | 翻滾、帆板未展開 |
| 66750 | TRANSPORTER-15 OBJECT CN | CTC-1C (21.0) | 78/10 | -0.0428 | 513 | 6.00e-13 | **0.0072** | 0.46 | 翻滾、帆板未展開 |

## 已識別物件（依 A/m 排序，供校準：受控衛星應接近『最小面迎風』，3U Dove 翻滾約 0.01）

| NORAD | 名稱 | GCAT 質量 | Bus | 外形 | da/dt km/day | A/m m²/kg |
|--|--|--|--|--|--|--|
| 66669 | SARI-2 | 0.25 | PocketQube 1P | Box+2 ant | -0.2209 | 0.0373 |
| 66666 | FORMOSAT-8A | 380.0 | FS8 | Box + 2 pan | -0.0871 | 0.0322 |
| 66670 | HUNITY | 0.75 | PocketQube 3P | Box+3 pan | -0.1850 | 0.0315 |
| 66668 | SARI-1 | 0.25 | PocketQube 1P | Box+2 ant | -0.1932 | 0.0310 |
| 66748 | UMBRA-11 | 84.0 | Espasat? | Box + 2 Pan + Dish | -0.1637 | 0.0266 |
| 66722 | FLOCK 4H-19 | 5.7 | Cubesat 3U | Box+2 pan | -0.1281 | 0.0210 |
| 66693 | AE5RB | 10.0? | Cubesat 6U | Box+ 2 pan | -0.1211 | 0.0205 |
| 66677 | AE5RC | 10.0? | Cubesat 6U | Box+ 2 pan | -0.1146 | 0.0195 |
| 66685 | AE5RA | 10.0? | Cubesat 6U | Box+ 2 pan | -0.1136 | 0.0194 |
| 66687 | LEO EXPRESS 3 | 250.0 | Mira | Box | -0.0983 | 0.0176 |
| 66671 | ANISCSAT-1 | 0.25 | PocketQube 1P | Box+2 ant | -0.1013 | 0.0175 |
| 66777 | LUNA-1 | 12.0? | Cubesat 6U? | Box | -0.0952 | 0.0152 |
| 66746 | (no current TLE) | 5.0 | Cubesat 3U | Box | -0.0883 | 0.0136 |
| 66714 | FLOCK 4H-11 | 5.7 | Cubesat 3U | Box+2 pan | -0.0797 | 0.0134 |
| 66675 | VEERY-0G | 1.0 | Cubesat 1U | Box | -0.0774 | 0.0133 |
| 66694 | YAM-9 | 150.0? | ARROW | Trapezoid+2 pan | -0.0716 | 0.0122 |
| 66772 | IHI-SAT2 | 12.0 | Cubesat 6U | Box | -0.0708 | 0.0115 |
| 66684 | MICE-1 | 5.0 | Cubesat 3U | Box | -0.0663 | 0.0114 |
| 66776 | LEMUR-2-LAILA | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0682 | 0.0111 |
| 66768 | LEMUR-2-TEODOR | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0673 | 0.0110 |
| 66743 | NUSAT-47 | 41.5 | Newsat V | Box | -0.0633 | 0.0109 |
| 66723 | FLOCK 4H-20 | 5.7 | Cubesat 3U | Box+2 pan | -0.0641 | 0.0106 |
| 66740 | NUSAT-51 (YVONNE BRILL) | 41.5 | Newsat V | Box | -0.0622 | 0.0105 |
| 66778 | FORESAIL-1 PRIME | 4.0 | Cubesat 3U | Box | -0.0575 | 0.0103 |
| 66736 | FLOCK 4H-33 | 5.7 | Cubesat 3U | Box+2 pan | -0.0625 | 0.0103 |
| 66717 | FLOCK 4H-14 | 5.7 | Cubesat 3U | Box+2 pan | -0.0603 | 0.0099 |
| 66705 | FLOCK 4H-2 | 5.7 | Cubesat 3U | Box+2 pan | -0.0587 | 0.0098 |
| 66757 | PIAST-S2 | 12.0 | Cubesat 6U | Box | -0.0584 | 0.0097 |
| 66692 | NUSAT-52 | 41.5 | Newsat V | Box | -0.0559 | 0.0096 |
| 66775 | PHI 1 | 20.0? | Cubesat 12U | Box | -0.0587 | 0.0096 |
| 66774 | GENA-OT | 15.0? | Cubesat 12U | Box+2 pan | -0.0579 | 0.0095 |
| 66686 | LEMUR-2-STAS-GORBUK | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0551 | 0.0094 |
| 66749 | PIAST-S1 | 12.0 | Cubesat 6U | Box | -0.0560 | 0.0094 |
| 66733 | FLOCK 4H-30 | 5.7 | Cubesat 3U | Box+2 pan | -0.0544 | 0.0094 |
| 66704 | FLOCK 4H-1 | 5.7 | Cubesat 3U | Box+2 pan | -0.0562 | 0.0094 |
| 66766 | T.MICROSAT-1 | 15.0? | Cubesat 8U | Box | -0.0557 | 0.0092 |
| 66725 | FLOCK 4H-22 | 5.7 | Cubesat 3U | Box+2 pan | -0.0532 | 0.0091 |
| 66711 | FLOCK 4H-8 | 5.7 | Cubesat 3U | Box+2 pan | -0.0529 | 0.0091 |
| 66688 | WISDOM A | 5.0 | Cubesat 3U | Box | -0.0516 | 0.0090 |
| 66724 | FLOCK 4H-21 | 5.7 | Cubesat 3U | Box+2 pan | -0.0544 | 0.0089 |
| 66700 | IRIDE-MS1-EAGLET 2-6 | 25.0 | Eaglet | Box+2 pan | -0.0540 | 0.0089 |
| 66735 | FLOCK 4H-32 | 5.7 | Cubesat 3U | Box+2 pan | -0.0517 | 0.0089 |
| 66713 | FLOCK 4H-10 | 5.7 | Cubesat 3U | Box+2 pan | -0.0516 | 0.0089 |
| 66712 | FLOCK 4H-9 | 5.7 | Cubesat 3U | Box+2 pan | -0.0528 | 0.0089 |
| 66719 | FLOCK 4H-16 | 5.7 | Cubesat 3U | Box+2 pan | -0.0508 | 0.0088 |
| 66716 | FLOCK 4H-13 | 5.7 | Cubesat 3U | Box+2 pan | -0.0526 | 0.0087 |
| 66758 | PIAST-M | 12.0 | Cubesat 6U | Box | -0.0518 | 0.0087 |
| 66699 | IRIDE-MS1-EAGLET 2-5 | 25.0 | Eaglet | Box+2 pan | -0.0503 | 0.0086 |
| 66678 | OTTER SDM | 5.0 | Cubesat 3U | Box+ 2 pan | -0.0487 | 0.0086 |
| 66708 | FLOCK 4H-5 | 5.7 | Cubesat 3U | Box+2 pan | -0.0514 | 0.0086 |
| 66720 | FLOCK 4H-17 | 5.7 | Cubesat 3U | Box+2 pan | -0.0510 | 0.0085 |
| 66771 | GYEONGGISAT-1 | 25.0? | Cubesat 16U | Box | -0.0517 | 0.0085 |
| 66741 | BLACK KITE-1 | 15.0? | Cubesat 8U | Box | -0.0495 | 0.0085 |
| 66696 | IRIDE-MS1-EAGLET 2-2 | 25.0 | Eaglet | Box+2 pan | -0.0490 | 0.0084 |
| 66728 | FLOCK 4H-25 | 5.7 | Cubesat 3U | Box+2 pan | -0.0506 | 0.0084 |
| 66695 | IRIDE-MS1-EAGLET 2-1 | 25.0 | Eaglet | Box+2 pan | -0.0508 | 0.0084 |
| 66706 | FLOCK 4H-3 | 5.7 | Cubesat 3U | Box+2 pan | -0.0489 | 0.0084 |
| 66702 | IRIDE-MS1-EAGLET 2-8 | 25.0 | Eaglet | Box+2 pan | -0.0486 | 0.0084 |
| 66710 | FLOCK 4H-7 | 5.7 | Cubesat 3U | Box+2 pan | -0.0485 | 0.0083 |
| 66739 | FLOCK 4H-36 | 5.7 | Cubesat 3U | Box+2 pan | -0.0494 | 0.0083 |
| 66727 | FLOCK 4H-24 | 5.7 | Cubesat 3U | Box+2 pan | -0.0478 | 0.0082 |
| 66701 | IRIDE-MS1-EAGLET 2-7 | 25.0 | Eaglet | Box+2 pan | -0.0480 | 0.0082 |
| 66718 | FLOCK 4H-15 | 5.7 | Cubesat 3U | Box+2 pan | -0.0471 | 0.0082 |
| 66680 | LEMUR-2-DEANANDMAEVE | 7.6 | Cubesat 3U | Box+ 2 pan | -0.0466 | 0.0082 |
| 66730 | FLOCK 4H-27 | 5.7 | Cubesat 3U | Box+2 pan | -0.0491 | 0.0082 |
| 66709 | FLOCK 4H-6 | 5.7 | Cubesat 3U | Box+2 pan | -0.0489 | 0.0082 |
| 66707 | FLOCK 4H-4 | 5.7 | Cubesat 3U | Box+2 pan | -0.0473 | 0.0082 |
| 66726 | FLOCK 4H-23 | 5.7 | Cubesat 3U | Box+2 pan | -0.0472 | 0.0081 |
| 66697 | IRIDE-MS1-EAGLET 2-3 | 25.0 | Eaglet | Box+2 pan | -0.0488 | 0.0081 |
| 66769 | SPEQTRE | 20.0? | Cubesat 12U | Box | -0.0491 | 0.0081 |
| 66732 | FLOCK 4H-29 | 5.7 | Cubesat 3U | Box+2 pan | -0.0465 | 0.0080 |
| 66738 | FLOCK 4H-35 | 5.7 | Cubesat 3U | Box+2 pan | -0.0483 | 0.0080 |
| 66729 | FLOCK 4H-26 | 5.7 | Cubesat 3U | Box+2 pan | -0.0460 | 0.0080 |
| 66731 | FLOCK 4H-28 | 5.7 | Cubesat 3U | Box+2 pan | -0.0451 | 0.0078 |
| 66756 | MAUVE | 24.0 | Cubesat 16U | Box+2 pan | -0.0464 | 0.0078 |
| 66721 | FLOCK 4H-18 | 5.7 | Cubesat 3U | Box+2 pan | -0.0446 | 0.0078 |
| 66737 | FLOCK 4H-34 | 5.7 | Cubesat 3U | Box+2 pan | -0.0467 | 0.0077 |
| 66742 | MERCURY ONE (M1) | 50.0 | M1 | Box | -0.0455 | 0.0077 |
| 66715 | FLOCK 4H-12 | 5.7 | Cubesat 3U | Box+2 pan | -0.0459 | 0.0076 |
| 66734 | FLOCK 4H-31 | 5.7 | Cubesat 3U | Box+2 pan | -0.0438 | 0.0076 |
| 66755 | ICEYE-X62 | 120.0 | ICEYE | Box + pan | -0.0431 | 0.0073 |
| 66698 | IRIDE-MS1-EAGLET 2-4 | 25.0 | Eaglet | Box+2 pan | -0.0424 | 0.0073 |
| 66683 | 6GSTARLAB | 12.0 | Cubesat 6U | Box+2 pan | -0.0393 | 0.0068 |
| 66767 | ACCENTURE-1 | 12.0 | Cubesat 6U | Box | -0.0402 | 0.0067 |
| 66751 | ICEYE-X58 | 120.0 | ICEYE | Box + pan | -0.0384 | 0.0065 |
| 66753 | ICEYE-X60 | 120.0 | ICEYE | Box + pan | -0.0371 | 0.0064 |
| 66763 | HYDROGNSS-2 | 65.0 | SSTL-21 | Box +3 pan | -0.0363 | 0.0063 |
| 66747 | (no current TLE) | 250.0? | VW | Trunc cone | -0.0365 | 0.0062 |
| 66674 | BRO-20 | 15.0? | Cubesat 8U | Box | -0.0353 | 0.0062 |
| 66754 | ICEYE-X61 | 120.0 | ICEYE | Box + pan | -0.0363 | 0.0061 |
| 66752 | ICEYE-X59 | 120.0 | ICEYE | Box + pan | -0.0357 | 0.0061 |
| 66679 | LILIUM-2 | 12.0 | Cubesat 6U | Box | -0.0340 | 0.0060 |
| 66762 | HYDROGNSS-1 | 65.0 | SSTL-21 | Box +3 pan | -0.0332 | 0.0058 |
| 66672 | BRO-17 | 15.0? | Cubesat 8U | Box | -0.0322 | 0.0057 |
| 66667 | PELICAN-5 | 160.0 | Pelican | Box+2 pan | -0.0291 | 0.0050 |
| 66764 | NAHLA | 200.0? | VSP-150 | Box + 2 pan | -0.0287 | 0.0049 |
| 66703 | PELICAN-6 | 160.0 | Pelican | Box+2 pan | -0.0268 | 0.0046 |
| 66689 | AC1-003 | 140.0 | P10 | Trunc pyramid | -0.0253 | 0.0044 |
| 66745 | AC1-002 | 140.0 | P10 | Trunc pyramid | -0.0253 | 0.0044 |
| 66770 | LILIUM-3 | 12.0 | Cubesat 6U | Box | -0.0264 | 0.0044 |
| 66682 | ION SCV-022 | 150.0 | ION-SC | Box | -0.0134 | 0.0036 |
| 66744 | AC1-001 | 140.0 | P10 | Trunc pyramid | -0.0115 | 0.0018 |

## 判讀

- 與「11 kg、帆板展開、翻滾」理論值 0.0155 m²/kg 相差在 ×0.6~×1.6 內（涵蓋大氣模型與 Cd 的不確定度）的未識別物件：**TRANSPORTER-15 OBJECT R (66681, A/m 0.0242, ×1.57)**、**TRANSPORTER-15 OBJECT H (66673, A/m 0.0210, ×1.36)**、**TRANSPORTER-15 OBJECT DD (66765, A/m 0.0185, ×1.20)**、**TRANSPORTER-15 OBJECT CZ (66761, A/m 0.0147, ×0.95)**、**TRANSPORTER-15 OBJECT AB (66691, A/m 0.0144, ×0.93)**、**TRANSPORTER-15 OBJECT CX (66759, A/m 0.0101, ×0.65)**、**TRANSPORTER-15 OBJECT L (66676, A/m 0.0094, ×0.61)**。
- A/m 明顯低於理論值的物件，若要是 TORO-2，就必須是「帆板沒展開」或「姿態受控」——與 Pyras 的帆板已展開判斷矛盾。
- 絕對值受 NRLMSISE-00 在太陽極大期 500 km 的誤差（±30% 量級）影響；物件之間的比值可靠得多，可用已識別的受控 8U（BRO、Black Kite、Bellbird）與 3U Dove 當量尺。
