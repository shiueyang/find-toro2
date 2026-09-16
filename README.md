# find-toro2 — identifying TORO-2 among the Transporter-15 unknown objects

*中文版：[README.zh-TW.md](README.zh-TW.md)*

TORO-2 (Pyras / TASA, 8U CubeSat, ~11 kg) was launched on SpaceX **Transporter-15** on 2025-11-28 18:44 UTC
(COSPAR 2025-276, Vandenberg SLC-4E, ~510 km SSO). No beacon has been received since separation.
Working hypothesis: the spacecraft is intact and in orbit, but never powered its beacon on.
This project asks which of the still-unidentified catalog objects from that launch (`TRANSPORTER-15 OBJECT xx`)
is TORO-2, so that ground stations can track it blind and attempt to command it.

## Current conclusion (2026-09-15)

**Most likely TORO-2: TRANSPORTER-15 OBJECT H, NORAD 66673, COSPAR 2025-276H.**

| Evidence | Summary |
|--|--|
| Deployment sequence | TORO-2 was the first payload released (19:39:09 UTC). Jonathan McDowell's GCAT lists 2025-276H as TORO2 (flagged as a tentative identification). |
| Size class | Of the 11 unidentified objects, only H and the three CTC-1 objects (R, DM, CN) are in the 8U/16U class per GCAT; the rest are 1U/3U/6U. |
| Drag behaviour | H has decayed to ~490 km while attitude-controlled 8U CubeSats from the same launch are still at 500–511 km. Its semi-major-axis decay rate is 2.6× the controlled-8U median. |

**Independent physical check using the real spacecraft properties** (11 kg, solar panels deployed, panel faces 8U+8U+4U),
see [docs/method.md §7](docs/method.md): from Space-Track element-set history and orbit-averaged NRLMSISE-00 density
we derive the area-to-mass ratio of every object on the launch, and compare with TORO-2's deployed CAD model
(silhouette projection method): random-tumble mean **0.0128 m²/kg**, largest-face-into-flow **0.0182 m²/kg**.

| Object | Derived A/m (m²/kg) | Reading |
|--|--|--|
| **OBJECT H (66673)** | **0.021** | Panels deployed, large face biased toward ram (flat-plate Cd above 2.2 explains the excess) |
| OBJECT R (66681) | 0.024 | Slightly above the CAD upper bound; first backup |
| OBJECT DM / CN | 0.008 / 0.007 | Same as controlled 8U CubeSats (0.005–0.009); would need stowed panels or active control |

**Method validation**: the same pipeline applied to the lab's own PARUS-6U1 (NORAD 68456, 6U, 7 kg, panels stowed,
confirmed tumbling from its ADCS beacons) reproduces its A/m to within 5% (theory 0.0079, observed 0.0075).

GCAT's 15 kg for TORO2 is a nominal 8U value (MassFlag `?`), and for unidentified objects the GCAT mass follows the
assigned name, so the A/m check deliberately does not depend on it. The Space-Track phase back-extrapolation (§6)
has no discriminating power on this data, and OBJECT H's history contains a cross-tagged stretch (2025-12-24 to 12-29)
that the scripts reject automatically.

Backup order if H yields nothing: **OBJECT R (66681)** → OBJECT AB / CZ (66691 / 66761) → OBJECT DM (66773) → OBJECT CN (66750).

Candidate TLEs: [results/toro2_candidate_tles.txt](results/toro2_candidate_tles.txt).
Full scoring: [results/candidates_ranked.md](results/candidates_ranked.md).
7-day pass schedule for the top candidate (NTUT and TASA ground stations, Taiwan): [results/stk/pass_schedule_R01.md](results/stk/pass_schedule_R01.md).

## Daily update

```bash
python scripts/fetch_data.py            # Celestrak TLE / SATCAT / GCAT
python scripts/analyze_candidates.py    # re-rank, write candidate TLEs and STK .tce files
python scripts/stk_build_scenario.py    # build/refresh the FindTORO2 scenario in a running STK 10, 7-day pass tables
```

Optional, needs your own Space-Track account (credentials are read from `SPACETRACK_USER` / `SPACETRACK_PASS`
environment variables and never stored):

```bash
python scripts/fetch_spacetrack_history.py          # element-set history for 2025-276
python scripts/estimate_ballistic.py                # A/m of every object via decay rate + NRLMSISE-00
python scripts/analyze_deployment_order.py          # phase back-extrapolation (inconclusive here, kept for reference)
python scripts/projected_area.py <deployed.stl> --mass 11   # tumbling-average projected area from a CAD mesh
```

`analyze_candidates.py` folds `results/ballistic_estimate.csv` into the score (weight 0.35) when it exists.

Requirements: Python 3.10+, `pip install -r requirements.txt` (plus `nrlmsise00`, `trimesh` for the optional steps),
STK 10 running with Connect on TCP 5001 for the pass schedule. FreeCAD 1.1 was used headless to convert STEP to STL.

## Notes on data

- Celestrak and GCAT data are included in `data/raw/`. GCAT is © Jonathan McDowell, used with attribution.
- Space-Track element-set history is **not** redistributed here (Space-Track user agreement); fetch it with your own account.
- Script comments, console output and the generated result files are in Traditional Chinese; the analysis logic is
  documented in English in [docs/method.md](docs/method.md), and the case for OBJECT H in [docs/why_object_h.md](docs/why_object_h.md).

## Layout
```
data/raw/        Celestrak TLE / SATCAT, GCAT catalog slices, space-weather file
data/processed/  .tce files for STK ImportTLEFile (candidates R01..R11, 8U reference set)
scripts/         fetch, analysis, STK automation, Space-Track, ballistic and CAD tools
results/         rankings, candidate TLEs, A/m estimates, STK pass reports (results/stk/)
docs/            method (EN / zh-TW), evidence summary (EN / zh-TW)
```

## Status
- [x] Data collection (Celestrak 2025-276 TLE + SATCAT, GCAT)
- [x] Candidate ranking (OBJECT H / 66673 on top)
- [x] STK 10 scenario and NTUT / TASA pass schedules
- [x] Candidate TLEs delivered
- [x] Space-Track history: phase method inconclusive; decay-rate / A/m analysis supports H
- [x] A/m method validated on PARUS-6U1; CAD-based projected area for TORO-2 deployed model
- [ ] Ground-station tracking result
