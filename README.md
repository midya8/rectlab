# RectLab

RectLab covers the ones in a small binary matrix with all-one rectangles. It
compares minimum overlapping covers, disjoint partitions, fooling-set lower
bounds and arithmetic rank. Every optimal factor set is selectable, with exact
counts of how often each rectangle appears. Version 0.2.

The same binary matrix can have Boolean rank 3, arithmetic rank 4 and minimum partition size 4. A maximum fooling set can have size 3 while every cover needs 4 rectangles. RectLab makes those distinctions inspectable instead of treating any of them as interchangeable evidence.

## Run

Python 3.10+, no runtime dependencies:

```sh
python -m pip install .
printf '{"matrix":[[1,1],[1,0]]}' > input.json
rectlab solve input.json > report.json
rectlab verify report.json
rectlab select input.json --family cover --index 0
rectlab rank input.json --family cover --factors '[1,4]'
python -m rectlab verify report.json
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000` for the browser inspector. Published deployment is verified separately from source publication.

## What it computes

- Every nonempty all-one rectangle, including nonmaximal rectangles.
- Minimum overlapping-cover size, exact decimal count and lexicographically first optimal unordered factor-id set.
- The separate census restricted to maximal rectangles. The optimum size agrees, but the count need not.
- Minimum pairwise-disjoint partition size, count and witness.
- B/C factor matrices, Boolean reconstruction, integer coverage multiplicities and overlap coordinates.
- Every positive-cell subset's fooling-set verdict and first obstructing pair, all maximum witnesses and the exact lower-bound gap.
- Arithmetic rank over the rationals, which is not used as a lower bound on Boolean rank.

The domain is 1..5 rows, 1..5 columns, at most 12 ones. The zero matrix has one empty cover. Counts ignore factor order, forbid repeated rectangles and include nonmaximal factors unless explicitly labeled otherwise. The certificate retains index 0 per family. The UI and CLI can select any zero-based lexicographic optimum by its exact decimal index, without materializing the entire family. Each legal factor has an exact inclusion count and mandatory/optional/never classification, relative to the selected family. Ineligible nonmaximal factors are labeled separately in maximal-only mode. All maximum fooling sets are selectable; every subset audit is in the certificate.

## Producer and independent verifier

`rectlab/engine.py` enumerates row/column subsets and solves ordered skip/take DP. `rectlab/verify.py` imports only schema helpers, discovers rectangles from positive-cell subsets, checks cover counts with inclusion-exclusion, checks partitions by first-uncovered-cell recursion, and computes arithmetic rank from determinant minors. It does not trust the producer's rectangle list, optimum, count, witnesses or audits. Repeated certificates for the same validated matrix reuse a bounded cache of serialized expected results. This is input-keyed recomputation, not a cryptographic certificate or a scalable proof system.

The browser has a separate JavaScript/BigInt implementation. Browser certificate replay uses that same browser engine and is labeled accordingly. Use the Python verifier for independent validation.

## Reproduce

```sh
python -m unittest discover -s tests -v
python tools/fixtures.py
npm test
python tools/installed.py
# Optional numerical third-party reference:
python -m pip install scipy==1.15.3
python tools/reference.py
```

Node 22+ and Chrome are needed for native browser tests. `CHROME_BIN` can name a Chrome executable. No npm runtime packages are needed.

The developed lower-bound-gap control has 11 ones, 41 legal rectangles, minimum size 4, 68 unrestricted minimum covers, 13 maximal-only minimum covers and maximum fooling-set size 3. The overlap control has a unique 3-factor cover, minimum partition size 4 and arithmetic rank 4. These are synthetic developed examples, not learned data, causal ablations or a benchmark victory.

## Selecting and counting optimal factor sets

The default has 68 optimal covers. Factor R0 appears in only 1/68; R12 appears in 40/68, versus 9/13 under maximal-only restriction. No factor is mandatory in that control. The unique-cover overlap control instead makes all three selected factors mandatory. These are exact combinatorial proportions under a specified uniform counting convention, not learned likelihoods or explanations of a real dataset.

The generator propagates optimal-prefix counts over its DP state graph and multiplies them by exact suffix counts for each take edge. The independent checker forces each factor and counts residual completions with inclusion-exclusion, or independent residual partition recursion. It checks the entire inclusion vector and all classifications. Rank/unrank follows take-before-skip branch counts, which matches lexicographic sorted fixed-cardinality factor-id sets.

Schema is now `rectlab/2`. Version 0.2 rejects old `rectlab/1` certificates rather than silently pretending they contain the new census. Regenerate from the embedded input. Public API `select_witness(input,family,index)` / `rank_witness(input,family,factors)` computes its own report; lower-level `select_from` / `rank_from` assume an already generated or verified report.

See [method](docs/method.md), [validation](docs/validation.md) and [sources](docs/sources.md). This project implements established finite mathematics. It does not claim noisy matrix factorization, large-scale performance, neural representation quality, access-control deployment or a new lower bound.
