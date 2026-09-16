# Method: finding TORO-2 among the Transporter-15 unidentified objects

*中文版：[method.zh-TW.md](method.zh-TW.md)*

## 1. Background and assumptions

- **TORO-2** (Pyras Technology / TASA, "TORO-8U-1", 8U CubeSat, ~11 kg) launched on SpaceX Transporter-15 on
  2025-11-28 18:44 UTC from Vandenberg SLC-4E, COSPAR **2025-276**, into a ~510 km, 97.4° sun-synchronous orbit.
- Per the SpaceX deployment timeline TORO-2 was the **first of 140 payloads to separate** (GCAT separation time
  19:39:09 UTC, T+55 min; Spaceflight Now: "deployment began with the Toro2 spacecraft a little more than 54 minutes after liftoff").
- No beacon has been received since separation. Working hypothesis: the spacecraft is intact and in orbit, but the
  OBC/beacon never started or attitude was never established. Goal: find its entry among the unidentified objects in
  the 18 SDS catalog and obtain a TLE for blind tracking.

## 2. Data sources

| Source | Use | Access |
|--|--|--|
| Celestrak GP `INTDES=2025-276` | Latest TLEs for all 122 objects still tracked | celestrak.org times out from the lab network; the fetch script falls back to the r.jina.ai read-only proxy |
| Celestrak SATCAT | Names, owners, decay status | same |
| GCAT (Jonathan McDowell, planet4589.org) | **Separation time**, mass, dimensions, and his identification of unknown objects | satcat.tsv / psatcat.tsv, filtered to 2025-276 |
| Space-Track gp_history | Element-set history from 2025-12-18 (first public elsets) | **user's own account**, credentials from environment variables; not redistributed |
| Celestrak SW-Last5Years.txt | Daily F10.7 / Ap for NRLMSISE-00 | via proxy |

## 3. The unidentified objects

Celestrak lists 11 `TRANSPORTER-15 OBJECT xx` entries still with TLEs (H, L, R, AA, AB, CN, CX, CY, CZ, DD, DM).
OBJECT CJ has had no new TLE since 2026-04 (decayed or untracked).

## 4. Ranking logic (`scripts/analyze_candidates.py`)

Five components, each 0–1, weighted:

| Component | Weight | Content |
|--|--|--|
| A Size class | 0.20 | GCAT mass/dimensions in the 8U/16U class. Only H (15 kg nominal) and CTC-1 A/B/C (21 kg) qualify; others are 1U/3U/6U. Note: for unidentified objects the GCAT mass follows the *assigned name*, so this is weak evidence and weighted low. |
| B GCAT identification | 0.30 | McDowell lists 2025-276H as TORO2 (with a `?` tentative flag). |
| C B* relative to class | 0.10 | TLE B* relative to identified 8U objects; H is ~2.5–3× the median. |
| D Separation timing | 0.05 | Time offset from TORO-2's separation; real verification needs history (§6). |
| E Derived A/m vs. TORO-2 spec | 0.35 | From `results/ballistic_estimate.csv` (§7). Accepted band: [0.8 × CAD tumbling mean, 1.25 × CAD largest-face] = [0.0102, 0.0227] m²/kg. |

Result: **OBJECT H / NORAD 66673 / 2025-276H** scores 1.0; the rest ≤ 0.575. See `results/candidates_ranked.md`.

## 5. STK 10 scenario (`scripts/stk_build_scenario.py`)

Automated through STK Connect (TCP 5001), no pywin32 needed:

1. Create or reuse scenario `FindTORO2`, analysis period = now + 7 days.
2. Ground stations `NTUT` (25.04295°N, 121.53612°E, 50 m) and `TASA` (24.80165°N, 121.00111°E, 40 m), 10° minimum elevation.
3. `ImportTLEFile` for the 11 candidates (`R01_…` = most likely) and an 8U reference set; SGP4 propagation.
4. Access per candidate × station; pass tables with AOS/LOS, azimuths, max elevation, minimum range in `results/stk/`.
5. Scenario saved to `~/Documents/STK 10/FindTORO2/`.

Implementation notes: STK 10 Connect replies with a bare 3-byte `ACK` for commands without output, and a padded
42-byte header plus byte count for commands with output; `ImportTLEFile` names satellites `tle-<NORAD>` regardless
of the name line; the lab's "Access" report style is customized, so intervals are taken from the Access command
payload and look angles from a facility-side "AER" report.

## 6. Space-Track history: phase back-extrapolation (inconclusive)

```bash
python scripts/fetch_spacetrack_history.py        # 10,909 elsets, 113 objects, 2025-12-17 .. 2026-01-10
python scripts/analyze_deployment_order.py
```

**Key limitation: these objects only entered the public catalog on 2025-12-18, 20 days after deployment.**
Space-Track quirks: in `gp_history` the `INTLDES` field is empty and `OBJECT_ID` does not accept the `^` prefix
operator; query `NORAD_CAT_ID/66666--66790` with `EPOCH/>date/EPOCH/<date`.

Linearly extrapolating each object's along-track phase (relative to a reference object) back to the deployment epoch
gives Spearman ρ = 0.3 between phase and separation time, with a residual σ ≈ 16° while the whole 30-minute deployment
sequence spans only ~13° of phase. The signal is the same size as the noise, so **this dataset can neither confirm nor
refute the GCAT assignment**. A quadratic extrapolation over 20 days diverges (σ ≈ 94°) and was discarded. The three
objects that come out "earliest" (R, DD, H) are exactly the three highest-drag objects: a bias of the linear method,
not evidence.

## 7. Area-to-mass ratio from decay rate (`scripts/estimate_ballistic.py`)

### 7.1 Method

- Near-circular orbit: `da/dt = −ρ (Cd A/m) √(μa)`, Cd = 2.2.
- ρ from NRLMSISE-00, averaged over 48 points along the SGP4 orbit, daily F10.7/Ap from the Celestrak space-weather file
  (F10.7 114–189 in the 2025-12-19 .. 2026-01-08 window).
- da/dt from a Theil–Sen (median) slope over all element sets in the window, **after rejecting bad element sets**:
  OBJECT H has 17 cross-tagged sets between 2025-12-24 and 12-29 (altitude jumping 501–514 km, eccentricity ×4, B* flipping sign).
  Without the filter a least-squares fit gives a nonsensical positive slope.

### 7.2 Calibration on identified objects

| Class | Derived A/m (m²/kg) |
|--|--|
| Attitude-controlled 8U: BRO-17 / BRO-20 / Black Kite-1 / T.MicroSat-1 | 0.0057 / 0.0062 / 0.0085 / 0.0092 |
| 3U Dove (Flock 4H, deployed wings) | 0.0094–0.0098, close to the theoretical tumbling value ~0.011 |
| 6U with deployed panels (AE5R A/B/C) | 0.019–0.021 |
| PocketQubes (Sari, Hunity) | 0.031–0.037 |

### 7.3 Unidentified objects

| NORAD | Object | GCAT name | Rejected elsets | A/m (m²/kg) |
|--|--|--|--|--|
| 66681 | OBJECT R | CTC-1B (16U, 21 kg) | 0 | 0.0242 |
| **66673** | **OBJECT H** | **TORO2** | 17 | **0.0210** |
| 66765 | OBJECT DD | WISDOM B (3U) | 0 | 0.0185 |
| 66761 / 66691 | OBJECT CZ / AB | TRYAD 2 / 1 (6U) | 0 / 4 | 0.0147 / 0.0144 |
| 66759 | OBJECT CX | Phasma-Lamarr (3U) | 15 | 0.0101 |
| 66676 | OBJECT L | HCT-SAT2 (1U) | 17 | 0.0094 |
| 66690 / 66760 | OBJECT AA / CY | SPiN 2 / PW-6U | 3 / 10 | 0.0080 / 0.0078 |
| 66773 / 66750 | OBJECT DM / CN | CTC-1A / 1C | 0 / 10 | 0.0077 / 0.0072 |

### 7.4 Method validation on PARUS-6U1 (NORAD 68456, 2026-067AS)

A satellite whose state is known: the lab's 6U, launched 2026-03-30 on Transporter-16, 7 kg, panels stowed, ADCS only
detumbling, no attitude solution. Its beacons show IMU rates of 5–10 deg/s in May–June 2026 and 2–7 deg/s in September,
TUMB/DES/EKF flags always 0: a genuine random tumble, so the "surface area / 4" model applies.

| Item | Value |
|--|--|
| Theory (6U 0.1×0.2×0.3 m, surface 0.22 m² / 4 / 7 kg) | **0.0079 m²/kg** |
| Observed (66 elsets, none rejected, 516 km, ρ 4.97e-13 kg/m³, da/dt −0.037 km/day) | **0.0075 m²/kg** |
| Observed / theory | **0.95** |
| Same-launch references: TORO-3 (Pyras 8U, 12 kg, controlled) / BRO-19 / Black Kite-2 / AISSAT-4 | 0.0086 / 0.0052 / 0.0101 / 0.0090 |

The absolute error of the method on a known tumbling object is 5%, so the 0.021 m²/kg derived for OBJECT H is a
trustworthy absolute value.

### 7.5 Projected area from the CAD model (`scripts/projected_area.py`)

The deployed-configuration assembly (`8u_asm_0312.stp`, Creo export, 88 solids, envelope 327 × 498 × 454 mm) was
converted to STL with FreeCAD 1.1 headless (1 mm tessellation, 4.7e5 triangles). 4 million surface sample points were
projected along 300 directions uniformly distributed on the sphere and counted on a 2 mm pixel grid. This silhouette
method correctly accounts for panels shadowing the body and each other, which "surface area / 4" does not.

| Quantity (11 kg) | Area (m²) | A/m (m²/kg) |
|--|--|--|
| **Random-tumble mean projected area** | **0.1405** | **0.0128** |
| Maximum projection (largest face into the flow) | 0.1999 | 0.0182 |
| Minimum projection | 0.0403 | 0.0037 |
| Along +X / +Y / +Z | 0.1965 / 0.1044 / 0.0295 | 0.0179 / 0.0095 / 0.0027 |
| Convex hull / 4 (equals the earlier hand estimate) | 0.1700 | 0.0155 |

Interpretation:
- The hand estimate 0.0155 was the convex hull / 4 and overstates the tumbling mean by ~20%; the correct mean is 0.0128.
- OBJECT H's 0.021 is 1.64× the tumbling mean but only 15% above the largest-face-into-flow value 0.0182. In free
  molecular flow a flat plate normal to the flow has Cd ≈ 2.6–3.0 rather than 2.2, which closes that gap.
- So if H is TORO-2, **it is not tumbling randomly; the panel face is biased toward ram.** After nine months without
  control, eddy-current damping and gravity gradient commonly slow a spacecraft into a passive principal-axis attitude.
  PARUS-6U1 still tumbles at 2–10 deg/s and fits the random model; TORO-2 may have slowed down. This is testable from the
  fading period of any received signal.
- Stowed panels (≤ 0.0064) or controlled attitude (0.0037) remain excluded; DM / CN at 0.007–0.008 correspond to those cases.

## 8. Ground-station operations

- Track `results/toro2_candidate_tles.txt` entry 1 (OBJECT H) first; passes in `results/stk/access_R01_*`.
- H has high drag (n-dot ~1.5e-4 rev/day²); refresh TLEs daily (`fetch_data.py` → `analyze_candidates.py` → `stk_build_scenario.py`).
- If several passes yield nothing, move to OBJECT R (66681), then AB / CZ, then DM / CN.
- Sweep Doppler around the expected downlink during the highest-elevation minutes of each pass.
