# Method and semantics

## Exact reconstruction

For a binary matrix A, a legal factor is a nonempty row set R and nonempty column set C with A[i,j]=1 for every pair. Its mask is R×C over row-major positive-cell indices. The OR of chosen factors must reproduce A exactly. Ordinary addition would record multiplicity; it is not the product used for reconstruction. XOR is not used.

Boolean rank is the fewest factors. Every factor is listed in ascending row-bitmask then column-bitmask order. Cover witnesses are sorted factor-id sets. A minimum solution never needs duplicate factors, and duplicates are excluded from the counts. Factor permutations are not counted as different explanations.

## Complete cover counts

The producer visits each ordered candidate exactly once with skip/take recursion. A state records candidate index and covered-cell mask. A take must add an uncovered cell. Returning at full coverage is safe for optimum counting: additional factors would not be minimum. The state stores optimum remaining size, a Python integer/BigInt count and lexicographically first optimal witness. No optimum family is truncated. The certificate materializes the first witness and the complete factor inclusion vector; indexed access reconstructs any optimum on demand.

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

## Exact membership and indexed access (0.2)

For each family, every legal rectangle receives the number of optimal distinct unordered factor sets containing it. Mandatory means this count equals the positive family count, optional means strictly between zero and the family count, and never means zero. Ineligible nonmaximal factors have zero count in maximal-only mode and are explicitly labeled ineligible in the UI. A singleton empty family has one empty set and no factors. The sum of factor inclusion counts equals optimum cardinality times family count.

The producer traverses only optimal DP edges. A forward state count records how many optimal prefixes reach the state. Each take edge contributes prefix count times its child's optimal suffix count to that factor's inclusion count. Merged DP states add prefix counts without collapsing distinct factor sets. A completed state stops because extra factors would not be minimum.

The independent checker forces each factor R and counts k-1 other factors covering U minus R using inclusion-exclusion. Partition membership instead uses the independent residual-partition optimum/count after removing R, and is zero unless the residual optimum is k-1. This construction does not use the producer's optimal-edge traversal.

Rank/unrank orders sorted fixed-cardinality factor-id lists lexicographically. Taking the current smallest available factor precedes skipping it. Unrank subtracts whole optimal suffix blocks, never materializes the family. Rank adds those blocks for each skipped eligible take. Tests enumerate every legal optimum independently for all 512 binary 3×3 matrices and all nine developed controls, checking order, bijection, reconstruction and membership. These APIs are bounded utilities, not a novel ranking algorithm.

Indices are canonical unsigned decimal strings up to 100 digits, bounded by the exact count. Factor lists must be sorted distinct integer IDs from the chosen candidate family and must be optimal. Native/JavaScript APIs reject negatives, padded numbers, noncanonical zeros, floats and out-of-range inputs. The browser previous/next buttons stop at boundaries rather than wrap. Invalid index selection reports rejection and preserves the prior valid witness.

Schema `rectlab/2` adds the complete census. Old schema1 certificates must be regenerated from their input. A certificate always exports the canonical first witness, regardless of which index the UI is currently inspecting. This keeps the report deterministic; input/family/index can reproduce the selected view. Uniform combinatorial proportions do not imply statistical, semantic or learned likelihood.
