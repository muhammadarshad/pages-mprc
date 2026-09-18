# Literature and Novelty Audit

Audit date: 18 September 2026

This file records the closest literature found during submission hardening. It is not a proof of novelty. The journal-facing manuscripts deliberately use cautious language such as "to the author's knowledge".

## Paper 1 — Simplex Cubic Decomposition over 2-Power Rings

### Closest work found

1. Pravesh K. Kothari, Ankur Moitra, Alexander S. Wein, **Overcomplete Tensor Decomposition via Koszul-Young Flattenings**, arXiv:2411.14344; FOCS 2025.
   - Generic overcomplete order-three tensor decomposition.
   - Field/real-complex style setting rather than the local ring Z/(2^m).
   - Uses Koszul-Young flattenings and generic components.
   - Does not match the binary-simplex plus exact bit-lift mechanism.

2. Giuseppe Cotardo, Ferdinando Zullo, **Symmetric Tensor Decompositions over Finite Fields**, arXiv:2605.12295 (2026).
   - Finite-field symmetric tensor decomposition/rank questions.
   - Uses finite fields and Frobenius/linearized-polynomial structure.
   - Does not use the non-field dyadic local ring Z/(2^m).

3. X. Song, B. Zheng, R. Huang, **The symmetric rank and decomposition of m-order n-dimensional (n=2,3,4) symmetric tensors over the binary field**, Linear Algebra and its Applications 653 (2022), 1-32.
   - Relevant binary-field symmetric-rank background.
   - Different dimension/order focus and no dyadic Hensel lift.

4. Real regular-simplex tensor literature studies eigenstructure and robustness of simplex tensors.
   - Different ground field and research question.

### Exact novelty wording to keep

The manuscript may claim:
- a global n+1-term identifiability theorem for the stated binary-simplex cubic class over Z/(2^m);
- constructive parity recovery from contraction ranks;
- exact one-bit lifting with an injective Jacobian;
- the structured residual-simplex n+2 extension under its stated condition.

The manuscript must not claim:
- the first overcomplete tensor decomposition algorithm;
- general overcomplete tensor identifiability;
- generic rank n+2 recovery;
- novelty for Hensel lifting in general.

### Exact-phrase search outcome

Searches for combinations of:
- "Z/2^m symmetric tensor decomposition cubic simplex frame"
- "binary simplex frame cubic tensor decomposition"
- "Hensel tensor decomposition Z/2^m"

did not surface a matching theorem in the indexed sources checked on the audit date.

## Paper 2 — Exact Cubic Dictionary Capacity

### Closest work found

1. Nathan Linial, Bruce L. Rothschild, **Incidence Matrices of Subsets—A Rank Formula**, SIAM Journal on Algebraic Discrete Methods 2(3) (1981), 333-340. DOI: 10.1137/0602037.
   - Classical subset-incidence rank over finite fields.
   - Directly relevant to the zeta/incidence minor.
   - The paper must treat the incidence matrix as classical.

2. Finite-field symmetric tensor decomposition/rank literature as above.
   - Related rank-one symmetric atom geometry.
   - Does not directly state the free-module dictionary-capacity problem over Z/(2^m).

### Exact novelty wording to keep

The claimed contribution is the exact dyadic-ring free-dictionary capacity theorem:
Cap_3(n,m)=sum_{k=1}^{min(3,n)} binom(n,k),
obtained from:
- the characteristic-two square-free support collapse;
- lifting any mod-2 dependence to a nonzero Z/(2^m) module relation;
- an explicit rank-one cubic family attaining the bound.

Do not claim:
- novelty of Boolean zeta matrices;
- generic tensor rank;
- global unknown-atom identifiability at capacity.

### Exact-phrase search outcome

Searches for:
- "dyadic ring symmetric tensor rank-one cubic dictionary capacity"
- "rank-one cubic Z/2^m"
- "free dictionary tensor dyadic ring rank one cubic"

did not surface a direct statement of the same capacity theorem in the indexed sources checked.

## Paper 3 — Eight-State Operator and Transpose Geometry

### Classical material that must be attributed

1. Simone Costa, Marco Pavone, **Orthogonal and oriented Fano planes, triangular embeddings of K7, and geometrical representations of the Frobenius group F21**, AIMS Mathematics 9(12) (2024), 35274-35292. DOI: 10.3934/math.20241676.
   - F21 and oriented seven-point/Fano geometry are classical/currently documented.
   - No novelty claim for the group of order 21.

2. Alexander Stasinski, **Similarity and commutators of matrices over principal ideal rings**, Transactions of the AMS 368(4) (2016), 2333-2354. DOI: 10.1090/tran/6402.
   - Every trace-zero matrix over a principal ideal ring is a commutator.

3. Alexander Stasinski, **Commutators of trace zero matrices over principal ideal rings**, Israel Journal of Mathematics 228(1) (2018), 211-227. DOI: 10.1007/s11856-018-1762-5.
   - Strengthens the principal-ideal-ring result using trace-zero commutator factors.

4. Makoto Suwama, **On trace zero matrices and commutators**, Journal of Algebra 616 (2023), 26-48. DOI: 10.1016/j.jalgebra.2022.11.005.
   - General-ring background and counterexamples outside favorable ring classes.

### Exact novelty wording to keep

The paper claims:
- the explicit 14-reference-coupling generating architecture in the chosen 8-state labeling;
- the exact synthesis with the frozen mixed-radix QH4 address;
- the local transpose orbit decomposition;
- the dyadic tensor-lift kernel theorem.

Do not claim:
- discovery of F21;
- discovery that trace-zero matrices over Z/(2^m) are commutators;
- identification with G2, so(8), octonions or another classical Lie algebra.

## Search limitation

This audit used current web/indexed sources and exact-title/phrase searches. A professional database search (MathSciNet, zbMATH, Scopus/Web of Science, SciSpace, or a university library) should still be performed immediately before formal submission.
