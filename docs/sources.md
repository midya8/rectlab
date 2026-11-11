# Sources and design provenance

Read November 10, 2026. Existing results are attributed here; all fixture matrices are synthetic developed controls or seeded generation, not copied benchmarks.

|Source|Type|Used for|
|---|---|---|
|[Miettinen and Neumann, Recent Developments in Boolean Matrix Factorization, IJCAI 2020](https://ijcai.org/proceedings/2020/685)|Peer-reviewed survey|Boolean OR product, equivalence to biclique cover; exact rank is not noise robust. No approximate BMF claims imported into this exact tool.|
|[Theis, On some lower bounds on the number of bicliques needed to cover a bipartite graph, 2011](https://arxiv.org/abs/0708.1174)|Primary research|Cover/Boolean-rank equivalence and fooling-set lower bound. Other lower bounds in the paper are not implemented.|
|[Pourmoradnasseri and Theis, The Rectangle Covering Number of Random Boolean Matrices, 2017](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i2p37/pdf/)|Primary research|All-one rectangle definition, overlap permitted, conflict graph relation. Random asymptotics are not tested or claimed.|
|[Bun, Communication Complexity lecture 2, Boston University](https://cs-people.bu.edu/mbun/courses/591_F19/notes/lec2.pdf)|University notes|Fooling sets versus covering and partitioning. No deterministic protocol complexity result is inferred.|
|[Konecny, FCA in Boolean Matrix Factorization, ICFCA 2023](https://www.kde.cs.uni-kassel.de/icfca2023/assets/slides/Konecny.pdf)|Research tutorial|Relation to formal concepts/maximal rectangles; distinguishes approximation and exact from-below factorization.|
|[Miettinen and Vreeken, Binary matrix factorizations tutorial](https://cs.uef.fi/~pauli/bmf_tutorial/material.html)|University tutorial bibliography|Separates normal, Boolean and modulo 2 algebras; cover and partition precedents.|
|[SciPy milp documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html)|Official software documentation|Binary-variable set-cover/partition and incompatibility constraints. Documentation currently describes a newer release; executed reference is pinned 1.15.3.|

[Geraci, Kunin and Seceleanu, Boolean Rank via Monomial Ideals, 2025](https://arxiv.org/abs/2509.09570) was inspected as recent adjacent primary work. Its algebraic bounds are not implemented or claimed. Abstract-only use is limited to identifying the adjacent topic.

Portfolio distinction: ConceptLab studies closures, concepts and implications. RectLab optimizes/counts covers across all legal rectangles, separately restricted maximal rectangles and disjoint partitions, and checks the fooling-set gap. It does not reimplement concept-lattice exploration as a new project.
