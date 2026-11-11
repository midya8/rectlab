# Validation and reproduction

Local results for 0.1:

- 12 Python unittest cases, including all 512 binary 3×3 matrices against independently reconstructed full reports.
- 64 complete Python/JavaScript reports: 9 developed and 55 seeded inputs; 964 legal rectangles and24,575 fooling-subset audits.
-All 140 primitive, noninput fields of a three-positive-cell certificate individually forged and rejected by both engines. Structural deletion, extra fields, list reordering and integer/Boolean substitutions are also checked in Python. This is bounded adversarial testing, not a universal security result.
-Actual SciPy 1.15.3 MILP: 159 input-built models over the 53 nonempty inputs, covering minimum cover, minimum partition and maximum fooling-set objectives. The reference regenerates rectangles from raw cell subsets. Objective matches and returned binary witnesses are checked. HiGHS uses numerical tolerances; this does not prove exactness or tie counts.
-Actual Chrome: 36 responsive control views at 1440/768/390/320 pixels, 108 witness-family selections, all maximum fooling witnesses, 18 trusted input/certificate downloads and native certificate upload/replay. Downloaded reports pass the Python checker. Input edits invalidate stale outputs and disable downloads until recomputed.

Run `python tools/fixtures.py` before browser checks to regenerate the deterministic corpus. `npm test` runs three engine tests plus one native Chrome test. Optional `RECTLAB_URL` runs the same behavior checks against a deployed site. Screenshots are unmasked PNG captures; live asset and pixel parity are deployment checks, not evidence of algorithm correctness.

The installed-package checker builds an isolated wheel installation, imports all five package modules from the virtual environment, runs both CLI entrypoints outside the checkout on all nine developed inputs, and rejects a forged count from each. Development and public-source reproductions are checked separately.

See workflows for the Python-version matrix, native browser test, numerical reference and Pages deployment. A local pass does not imply a remote workflow or live deployment passed. Publication is reported complete only after those checks are actually observed.
