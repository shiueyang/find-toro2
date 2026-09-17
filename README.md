# find-toro2 — identifying TORO-2 among the Transporter-15 unknown objects

*中文版：[README.zh-TW.md](README.zh-TW.md)*

TORO-2 (Pyras / TASA, 8U CubeSat, ~11 kg, solar panels deployed) was launched on SpaceX **Transporter-15** on
2025-11-28 18:44 UTC (COSPAR 2025-276, Vandenberg SLC-4E, ~510 km SSO). No beacon has been received since separation.
Working hypothesis: the spacecraft is intact and in orbit but never powered its beacon on. This project asks which of the
still-unidentified catalog objects from that launch (`TRANSPORTER-15 OBJECT xx`) is TORO-2, so that ground stations can
track it blind and attempt to command it.

## Status (2026-09-17)

> **Correction 2026-09-16.** Our first candidate, OBJECT H (66673), was identified by SatNOGS / Libre Space as
> **PHASMA-LAMARR** (3U, deployed panels) from RF observations and ikhnos Doppler analysis; OBJECT R (66681) is
> **PHASMA-DIRAC**. RF evidence overrides orbital-dynamics inference, so H and R are excluded. GCAT's name assignments for this
> launch proved unreliable (H, R, CX and CJ were all wrong), so the ranking no longer uses GCAT identifications or masses.
> Details in [docs/method.md §9](docs/method.md); the superseded reasoning is kept in [docs/why_object_h.md](docs/why_object_h.md).

**Current best candidate: TRANSPORTER-15 OBJECT DD, NORAD 66765 (2025-276DD). Alternative: OBJECT CJ, NORAD 66746
(no element sets since 2026-04-07, status being checked).**

Evidence, using only quantities independent of any name assignment:

| Group (A/m from Space-Track element-set history + orbit-averaged NRLMSISE-00) | Objects | Plausible payloads |
|--|--|--|
| Low 0.0072–0.0080 m²/kg | CN, DM, CY, AA | CTC-1 ×3 (16U), PW-6U (6U), 3UCubed-A (3U, body-mounted cells) |
| Mid 0.0094–0.0101 | L, CX | WISDOM B (its twin WISDOM A measures 0.0090), SPiN-2 (3U) |
| High 0.0136–0.0185 | AB, CZ (a pair), **DD**, **CJ** | TRYAD-1/2 (a pair), **TORO-2**, plus one unknown |

TORO-2's deployed CAD model gives a random-tumble A/m of 0.0128 m²/kg and a face-into-flow value of 0.0182. DD (0.0185) matches
the face-on case (1.02×), CJ (0.0136) the tumbling case (1.06×). A/m cannot separate them; DD has a usable TLE, so it is tracked first.
The A/m method was validated on the lab's own PARUS-6U1 (known 7 kg 6U, tumbling): theory 0.0079 vs observed 0.0075.

Lesson learned: A/m alone cannot settle identity (H's 0.021 fits a 3U with panels just as well as an 8U). Before proposing a
candidate, check SatNOGS DB and the community.libre.space launch thread; RF-confirmed identifications are kept in
[data/identifications.json](data/identifications.json) and excluded automatically.

Candidate TLEs: [results/toro2_candidate_tles.txt](results/toro2_candidate_tles.txt). Scoring: [results/candidates_ranked.md](results/candidates_ranked.md).
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
python scripts/spacetrack_query.py "class/satcat/NORAD_CAT_ID/66746"   # ad-hoc Space-Track query
```

`analyze_candidates.py` folds `results/ballistic_estimate.csv` into the score when it exists and excludes objects listed in
`data/identifications.json`.

Requirements: Python 3.10+, `pip install -r requirements.txt` (plus `nrlmsise00`, `trimesh` for the optional steps),
STK 10 running with Connect on TCP 5001 for the pass schedule. FreeCAD 1.1 was used headless to convert STEP to STL.

## Notes on data

- Celestrak and GCAT data are included in `data/raw/`. GCAT is © Jonathan McDowell, used with attribution.
- Space-Track element-set history is **not** redistributed here (Space-Track user agreement); fetch it with your own account.
- Script comments, console output and the generated result files are in Traditional Chinese; the analysis is documented in
  English in [docs/method.md](docs/method.md).

## Layout
```
data/raw/            Celestrak TLE / SATCAT, GCAT catalog slices, space-weather file
data/processed/      .tce files for STK ImportTLEFile (candidates R01.., 8U reference set)
data/identifications.json   RF-confirmed identifications (SatNOGS) that override GCAT
scripts/             fetch, analysis, STK automation, Space-Track, ballistic and CAD tools
results/             rankings, candidate TLEs, A/m estimates, STK pass reports (results/stk/)
docs/                method (EN / zh-TW), superseded OBJECT H evidence summary (EN / zh-TW)
```

## Timeline
- [x] Data collection, ranking, STK pass schedules, candidate TLEs
- [x] Space-Track history: phase method inconclusive; decay-rate / A/m analysis
- [x] A/m method validated on PARUS-6U1; CAD-based projected area for TORO-2
- [x] 2026-09-16: SatNOGS identifies H = PHASMA-LAMARR, R = PHASMA-DIRAC; candidate changed to DD (alternative CJ)
- [ ] Space-Track status of CJ and RCS_SIZE check; SatNOGS observations on DD; ground-station result
