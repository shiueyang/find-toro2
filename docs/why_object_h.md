# Why OBJECT H (NORAD 66673, 2025-276H) was identified as TORO-2 — SUPERSEDED

> **Correction, 2026-09-16.** This conclusion is wrong. SatNOGS / Libre Space identified OBJECT H as **PHASMA-LAMARR** and
> OBJECT R as **PHASMA-DIRAC** (3U, deployed panels) from RF observations and ikhnos Doppler analysis. The document is kept
> as a record of the reasoning and of where it failed: the A/m evidence in §4 is equally consistent with a 3U-with-panels,
> and the GCAT name assignment in §1 turned out to be unreliable for this launch. The current analysis is in
> [method.md §9](method.md); the present best candidate is OBJECT DD (66765), with OBJECT CJ (66746) as the alternative.

*中文版：[why_object_h.zh-TW.md](why_object_h.zh-TW.md)*

Compiled 2026-09-15. Four layers of evidence: the first two come from external catalogs, the last two were derived in
this project from physical quantities that do not depend on any name assignment.

## 1. Deployment sequence and third-party identification

- The Transporter-15 deployment sequence started with TORO-2 (Spaceflight Now: "deployment began with the Toro2
  spacecraft a little more than 54 minutes after liftoff"). GCAT records the separation at 2025-11-28 19:39:09 UTC,
  first of 140 payloads.
- Jonathan McDowell's GCAT lists 2025-276H as TORO2 (TASA/PYRAS). It is the only public source that has systematically
  assigned names to this launch's unidentified objects; sites such as satellitemap.space copy it.
- Limitation: GCAT flags the assignment as tentative (`?`). We tried to reproduce it from Space-Track history, but public
  element sets only begin 20 days after deployment and differential drift has erased the deployment order
  (Spearman ρ ≈ 0.3, residual σ comparable to the whole deployment signal). This layer is therefore "consistent with H",
  not independent confirmation.

## 2. Size-class elimination

- Of the 11 unidentified objects, only H (TORO2) and R / DM / CN (CTC-1B / 1A / 1C, 16U, 21 kg) fall in the 8U/16U class
  according to GCAT; the rest are 1U, 3U or 6U.
- Limitation: for unidentified objects the GCAT mass follows the assigned name, not a measurement, so this layer only
  excludes clearly different classes and cannot separate H from R.

## 3. Drag behaviour (B* and decay rate), independent of any name

- H is now at ~490 km while attitude-controlled 8U CubeSats from the same launch (BRO-17/20, Black Kite-1, T.MicroSat-1)
  are still at 500–511 km. Its B* is 2.5–3× the class median.
- From Space-Track history (2025-12-19 .. 2026-01-08) H's semi-major-axis decay rate is −0.122 km/day against a
  controlled-8U median of −0.046 km/day, about 2.6×.
- Only H and R among the 11 unknowns decay this fast for their class. That is exactly how a satellite that never
  established attitude and is flying with deployed panels should behave. DM / CN decay like controlled satellites; if they
  were TORO-2, TORO-2 would have to be actively controlling its attitude, which contradicts the absent beacon.

## 4. Quantitative match to the spacecraft: the strongest layer

- Spacecraft properties: ~11 kg, panels deployed. The deployed CAD model gives a random-tumble mean projected area of
  0.1405 m² (A/m **0.0128 m²/kg**) and a largest-face-into-flow projection of 0.1999 m² (**0.0182**).
- A/m derived from decay rate + NRLMSISE-00 (orbit-averaged density, daily F10.7/Ap, Cd 2.2, Theil–Sen slope,
  cross-tagged element sets rejected):

| Object | Derived A/m (m²/kg) | Corresponding TORO-2 state |
|--|--|--|
| **OBJECT H** | **0.021** | Panels deployed, large face biased toward ram (flat-plate Cd > 2.2 explains the 15% excess over 0.0182) |
| OBJECT R | 0.024 | Same, but GCAT assigns it to a 21 kg 16U |
| OBJECT DM / CN | 0.008 / 0.007 | Only "controlled" or "panels stowed" |
| Controlled 8U references | 0.006–0.009 | calibration |
| 3U Dove references | 0.0094–0.0098 | close to the theoretical tumbling ~0.011, confirming the absolute scale |

- Meaning: a controlled 8U would sit at 0.006–0.009; a tumbling 8U with stowed panels at ~0.0064. The observed 0.021 is
  only explained by "panels deployed, ~11 kg, large face toward the flow", which is TORO-2's situation. This layer does
  not use GCAT's name or mass at all.
- Validation: the same pipeline applied to PARUS-6U1 (NORAD 68456, known 7 kg, 6U, tumbling) reproduces its A/m to within 5%.

## 5. Consistency

The four layers are independent (deployment timeline vs. orbital dynamics with different data and methods) and point to
the same object. The only alternative that also passes layers 3 and 4 is OBJECT R, but R has no layer-1 support (GCAT
assigns it to CTC-1B, separated 4.5 minutes later) and, as a 21 kg 16U, would need even larger fully-deployed panels to
reach 0.024.

## 6. Remaining uncertainty

- The deployed CAD used is the March 2026 assembly; a more precise June model was supplied but the file was truncated and
  could not be read.
- Atmospheric model absolute error at 500 km near solar maximum is up to ±30%, Cd ±15%; the PARUS-6U1 check suggests the
  actual error is much smaller, but "1.15× the face-on value" should be read as "consistent", not "exact".
- If CTC-1B is also a dead satellite, orbital dynamics alone cannot decide between H and R. The final confirmation has to
  come from a ground station receiving a signal during an H pass.

## 7. Recommended tracking order

1. OBJECT H / 66673
2. OBJECT R / 66681
3. OBJECT AB / 66691, OBJECT CZ / 66761
4. OBJECT DM / 66773, OBJECT CN / 66750

Refresh TLEs daily (H's n-dot is ~1.5e-4 rev/day², so along-track error grows quickly); pass tables come from
`scripts/stk_build_scenario.py`.
