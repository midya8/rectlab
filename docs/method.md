# Method and semantics

## Exact reconstruction

For a binary matrix A, a legal factor is a nonempty row set R and nonempty column set C with A[i,j]=1 for every pair. Its mask is R×C over row-major positive-cell indices. The OR of chosen factors must reproduce A exactly. Ordinary addition would record multiplicity; it is not the product used for reconstruction. XOR is not used.

Boolean rank is the fewest factors. Every factor is listed in ascending row-bitmask then column-bitmask order. Cover witnesses are sorted factor-id sets. A minimum solution never needs duplicate factors, and duplicates are excluded from the counts. Factor permutations are not counted as different explanations.

## Complete cover counts

The producer visits each ordered candidate exactly once with skip/take recursion. A state records candidate index and covered-cell mask. A take must add an uncovered cell. Returning at full coverage is safe for optimum counting: additional factors would not be minimum. The state stores optimum remaining size, a Python integer/BigInt count and lexicographically first optimal witness. No optimum family is truncated, but only one cover witness per family is materialized.

Any legal rectangle can be extended to a maximal one. Extending all rectangles of a minimum cover produces a maximal cover with no more factors; fewer would contradict the original minimum. Thus sizes agree. This argument does not preserve the census. RectLab reports both counts and does not describe the maximal-only count as all minimum factorizations.

Partitions impose pairwise-disjoint masks on takes. They are not a restriction silently applied to covers. Coverage multiplicity makes the difference visible.

## Independent counting

The checker enumerates all subsets of positive cells. A nonempty subset is a rectangle exactly when its size equals the product of its distinct row and column counts. This generates the legal factors independently of the producer's row/column scan.

For candidate set J, required cell set U and target factor count k, the checker uses inclusion-exclusion:

`count(J,U,k) = sum over T subset U of (-1)^|T| choose(number of J rectangles avoiding T, k)`.

The first k with nonzero count is optimal. Greedy lexicographic witness reconstruction is not a greedy cover heuristic: it asks the exact suffix count whether each next factor can complete an optimum. A separate first-cell recursion checks partition optimum/count/witness without counting factor permutations.

The checker reconstructs the full report from its input and compares every field with strict Python types. Extra/missing fields, wrong order and Boolean substitutions for integers fail. Duplicate JSON keys and nonfinite constants fail in the Python CLI. Browser JSON parsing does not promise duplicate-key detection.

## Fooling sets and rank

A set of positive cells is a fooling set when no pair fits in one legal rectangle. For two selected cells (i,j),(k,l), both cross cells existing is an obstruction. A same-row or same-column pair is therefore also rejected. The complete 2^n subset audit identifies the first obstructing pair in cell-index order. An empty input has maximum size 0 and the unique empty witness. Every cover needs at least one rectangle per fooling-set cell; equality is not guaranteed.

Arithmetic rank is computed exactly by rational Gaussian elimination in the producer and determinant minors in the checker. It is displayed as a contrast, not asserted to lower-bound Boolean rank. The overlap control demonstrates why: Boolean rank 3, arithmetic rank 4.

## Limits and resource bounds

At most 5×5 with 12 ones, hence at most 4096 cell subsets and at most 961 row/column subset pairs before legality checks. The algorithms are exponential and synchronous in the browser; these limits are part of the model, not a benchmark claim. Counts are decimal strings. Coordinates and masks fit exact small integer ranges. Reports are deterministic and include the input. There is no authenticity, signature or privacy guarantee from a certificate; valid evidence is relative to its embedded input.
