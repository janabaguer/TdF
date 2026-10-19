# Progress Log

Running log of decisions, dead ends, and findings. Keep entries short — not a polished report.

## Week 1 — Research design
- [x] Finalize research proposal
- [x] Confirm data source access: TidyTuesday "Tour de France" dataset (`rfordatascience/tidytuesday`, `data/2020/2020-04-07`). Chosen for easy access (open source, CC0)
- [x] Define exact target variable for Task A → **log gap to stage winner**, `log(1 + gap_s)`, stage type as a feature (see Week 2 findings)

## Week 2 — Data acquisition & cleaning
- [x] EDA notebook started (`notebooks/01_eda.ipynb`): sections 1–5 and 8 done
- [x] **Dead end:** TidyTuesday `stage_data.csv` has corrupted times. `time`/`elapsed` were `lubridate::period` objects and only the seconds survived the CSV export (values 0–59). Verified: `time` = gap mod 60, `elapsed` = stage time mod 60, on 100% of 247,668 non-winner rows
- [x] **Fix:** full times recovered from the `tdf` R package (`alastairrushworth/tdf`, `editions.rda`), the upstream source of the TidyTuesday data. `src/load_data.py` downloads all raw files (both repos pinned to a commit) and writes `data/processed/stage_results.csv`. Matches TidyTuesday row for row and agrees with known results (e.g. Garin 1903, Thomas 2017 ITT)
- [x] Missing values: `team`/`bib_number` ~100% missing before 1930, data essentially complete from the 1930s
- [x] Non-finishers in `rank`: DNF 4,236 · DNS 672 · OTL 467 · DSQ 214 · DF 155 · NQ 9 (DF/NQ undocumented)
- [x] Join results ↔ stages on `(year, stage label)`, with prologue `P` → `0`: 2,198 stages match. Stage info stops in 2017 → **models with stage features limited to ≤ 2017**
- [x] Stage `Type` grouped into flat / hilly / mountain / itt / ttt / other. The taxonomy is era-dependent: "hilly" only exists from 1972
- [x] **Cleaning rule (provisional):** drop TTT stages (rows hold GC times, median "speed" 11 km/h), drop `other`, drop stages whose winner's speed is outside 15–60 km/h (mostly split stages with mixed-up times). 2,049 of 2,198 stages kept
- [x] Log-gap checks (1970+): zero spike is a flat-stage effect (38% of flat finishers at gap 0; 2.5% of rows once flat stages are excluded). Within-stage SD ~0.5 for ITTs vs ~1.0–1.2 for other types → **σ should depend on stage type**
- [x] ITT gaps scale with distance (median 0.7 min for < 15 km vs 6.2 min for longer) → stage distance needed as a feature
- [x] Breakaways: on 34% of flat stages the bunch finishes ≥ 1 min behind the winner, so gaps reflect the breakaway's margin, not each rider's performance
- [x] **Tried and rejected: median finisher as gap reference** (EDA 8.5), meant to remove the breakaway effect. Gap = rider time − stage median time (negative for half the riders), tested with signed log, asinh(x/60) and asinh(x/300)
  - 72% of flat-stage finishers at exactly zero (vs 38% with the winner reference): the median finisher sits in the bunch
  - 44% of all rows at zero (vs 20.5%)
  - Hilly and mountain stages split into two humps under every transform: the median rider sits in the group of dropped riders, with faster riders minutes below and slower riders minutes above
  - **Why rejected:** the shapes come from the reference, not the transform, so no transform fixes them, and modelling them would need a spike-plus-mixture likelihood. The winner reference with a per-stage effect handles breakaways without these side effects
- [x] **Gap reference → stage winner, plus a per-stage random effect** in the models, so breakaway margins are absorbed by the stage's shift. For a future stage that shift is unknown, which widens predictive intervals
- [ ] **Open:** Task B event definition (DNF only vs DNF + DNS (+ OTL); DSQ excluded)
- [ ] EDA section 6: year range (pre-1970 gaps are on a much larger scale)
- [ ] EDA section 7: rider history length (enough sparse-history riders for H2?)
- [ ] Limitation to note in the report: no elevation data, stage type used as a proxy

## Week 3 — Feature engineering
- [ ]

## Week 4 — Baseline + tree models
- [ ]

## Week 5 — Bayesian hierarchical model
- [ ]

## Week 6 — Evaluation & calibration
- [ ]

## Week 7 — DNF/survival extension
- [ ]

## Week 8 — Report + polish
- [ ]
