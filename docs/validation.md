# Validation and reproduction

Local results for 0.2:

- 18 Python unittest cases, including all 512 binary 3×3 matrices against independently reconstructed full reports.
- 64 complete Python/JavaScript reports: 9 developed and 55 seeded inputs; 964 legal rectangles and24,575 fooling-subset audits.
-All 170 primitive, noninput fields of a three-positive-cell certificate individually forged and rejected by both engines. Structural deletion, extra fields, list reordering and integer/Boolean substitutions are also checked in Python. This is bounded adversarial testing, not a universal security result.
-Actual SciPy 1.15.3 MILP: 159 input-built models over the 53 nonempty inputs, covering minimum cover, minimum partition and maximum fooling-set objectives. The reference regenerates rectangles from raw cell subsets. Objective matches and returned binary witnesses are checked. HiGHS uses numerical tolerances; this does not prove exactness or tie counts.
-Actual Chrome: 36 responsive control views at 1440/768/390/320 pixels, 108 witness-family selections, 520 optimal-set inspections, 2,988 factor-membership rows, all maximum fooling witnesses, 18 trusted input/certificate downloads and native certificate upload/replay. Downloaded reports pass the Python checker. Input edits invalidate stale outputs and disable downloads until recomputed.

Run `python tools/fixtures.py` before browser checks to regenerate the deterministic corpus. `npm test` runs five engine tests plus one native Chrome test. Optional `RECTLAB_URL` runs the same behavior checks against a deployed site. Screenshots are unmasked PNG captures; live asset and pixel parity are deployment checks, not evidence of algorithm correctness.

The installed-package checker builds an isolated wheel installation, imports all six package modules from the virtual environment, runs both CLI entrypoints outside the checkout on all nine developed inputs, and rejects a forged count from each. Development and public-source reproductions are checked separately.

See workflows for the Python-version matrix, native browser test, numerical reference and Pages deployment. A local pass does not imply a remote workflow or live deployment passed. Publication is reported complete only after those checks are actually observed.

The six new native tests explicitly enumerate all optimal factor sets of all three families on every 3×3 binary matrix, plus every developed control. They check exact membership totals and each index/order/round trip. The nine controls retain 130 complete optimal sets across the three families, not 130 different matrices. The browser checks those 130 sets at each of four widths (520 views), every factor-matrix grid, membership row and rank label. Native button clicks test next/previous and selection of index 67, then reject out-of-range/noncanonical values while preserving the last valid witness. All 170 primitive noninput fields of the small certificate, including new census fields, are forged individually per engine. Installed checks add 54 select/rank pairs across both entrypoints outside the checkout. Optional numerical MILP still checks only objectives, not membership counts or ranks.
