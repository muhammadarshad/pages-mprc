# Status Update — 20 September 2026

The earlier three-paper novelty framing is superseded.

## Primary novelty candidate

**Rank-(n+2) Cubic Identifiability over Dyadic Rings: Reed–Muller Rigidity and a Relation-Code/Sidon Classification**

Current theorem candidate:

- Ring: `R_m = Z/(2^m)`, `m >= 2`.
- Rank: `r = n+2`.
- Parity frame: distinct nonzero spanning columns `S=[s_1 ... s_{n+2}]`.
- Relation code: `K = ker S`, a binary `[n+2,2]` code.
- Global parity support recovery: proved for every `n >= 3`.
- Dyadic lift rigidity: proved for all `n >= 3` in this rank-`n+2` setting:
  `ker J_S = 0 iff d(K) >= 5`.
- Classical reformulation: `d(K) >= 5` iff `{0,s_1,...,s_{n+2}}` is a binary Sidon set.
- Exact converse: if `d(K) <= 4`, a 3- or 4-atom circuit yields a nonzero Jacobian direction, and toggling it in the top dyadic bit gives an exact second decomposition over every `Z/(2^m)`.
- Quantinion case `n=8,r=10`: 32 frame classes, exactly 9 rigid and 23 non-rigid; every non-rigid class has an exact `Z_256` counter-decomposition.

The current parity-support proof uses Reed–Muller duality, the minimum-weight affine-flat theorem, and a general projective-triorthogonal dimension bound derived from Schur-product Kneser theory; there is no remaining upper dimension cutoff at rank `n+2`.

### Closest prior work now explicitly acknowledged

1. Kopparty–Potukuchi (SODA 2018): Reed–Muller syndrome decoding and equivalent tensor decomposition over finite fields.
2. Berlekamp–Sloane / Kasami–Tokura: low-weight Reed–Muller structure.
3. Nagy (JCTA 2025) and Czerwinski–Pott (JCTA 2026): binary Sidon sets and their equivalence with minimum-distance-five binary codes.
4. General Hensel lifting: classical; not claimed as novel.

The novelty claim, if it survives professional review, is therefore **not** Reed–Muller theory, Sidon sets, distance five, or Hensel lifting individually. It is the exact coupling:

```
rank n+2 cubic over Z/(2^m)
+ global parity rigidity
+ relation-code/Sidon criterion
+ exact iff dyadic lift rigidity
+ explicit top-bit non-uniqueness when the criterion fails.
```

## Status of the earlier papers

- **Simplex cubic paper:** foundational special case and derivation history. It should become a precursor/section of the new classification paper rather than the primary novelty claim.
- **Exact cubic dictionary capacity:** supporting Boolean/Reed–Muller structure; not currently treated as a standalone novelty paper.
- **Operator/Transpose geometry:** MPRC internal algebra and supporting derivation; substantial classical content, not currently treated as the main novelty paper.

The active submission target is therefore **one principal theorem paper**, not three novelty claims.

---

# Literature and Novelty Audit

Audit date: 18 September 2026

This file records the closest literature found during submission hardening. It is not a proof of novelty. The journal-facing manuscripts deliberately use cautious language such as "to the author's knowledge".

## All-dimensions upgrade — 20 September 2026

The previous finite range `3 <= n <= 17` is superseded.

### New projective triorthogonal span lemma

Let `C <= F_2^c` be full-support and projective, with
`C^{<2>} <= C^perp`.  If `r=dim C`, then

```
r <= 8c/21.
```

Proof ingredients:
- Schur-product Kneser theorem for codes:
  `dim(C*C) >= 2 dim C - dim St(C*C)`;
- triorthogonality:
  `C*C <= C^perp`;
- the stabilizer decomposition into disjoint support blocks;
- every block inherits a full-support projective self-orthogonal binary code;
- such a block has length at least 7.  Lengths 1..5 are excluded by
  `r <= floor(l/2)` plus projectivity `l <= 2^r-1`; length 6 would force a
  projective self-dual [6,3,>=4] code, contradicting the Griesmer bound.

Hence every stabilizer block has size at least seven, so
`dim St(C*C) <= c/7`, giving the stated `8c/21` bound.

### Consequence for cubic parity collisions

For a parity collision support `F` of size `c`, delete a possible zero point
and form the row code from the remaining distinct support points.  The cubic
moment equations make this code projective and all-even triorthogonal.

- If `0 in F`, the `8(c-1)/21` rank bound contradicts spanning for every
  nonzero Reed-Muller collision because `c >= 16`.
- If `0 notin F` and `c >= 18`, the `8c/21` bound contradicts spanning.
- The only remaining case is `c=16`.  A minimum-weight word of
  `RM(n-4,n)` is an affine 4-flat, whose linear span has dimension at most 5;
  this also contradicts an `n+2`-point spanning frame.

Therefore the parity-support theorem now holds for **every `n >= 3`**, not
merely through a finite dimension.

### Updated main theorem candidate

For every `n >= 3`, `m >= 2`, and every rank-`n+2` cubic

```
T = sum_q v_q^{tensor 3}
```

whose parity columns are distinct, nonzero and spanning, let
`K=ker[s_1 ... s_{n+2}]`.  Then

```
global (n+2)-term uniqueness over Z/(2^m)
iff d(K) >= 5
iff {0,s_1,...,s_{n+2}} is a binary Sidon set.
```

If the condition fails, a 3- or 4-point circuit supplies a nonzero one-bit
Jacobian direction and a top-bit perturbation gives an exact second
decomposition over every dyadic modulus.

### New prior art that must be cited

- Chenying Lin and Gilles Zémor, *Kneser's theorem for codes and ell-divisible
  set families*, Finite Fields and Their Applications 111 (2026), 102783.
  The Schur-product Kneser theorem and stabilizer decomposition are classical /
  prior tools used essentially in the new all-dimensions proof.

- Heng Li and Xizhi Liu, *Sharp bounds for minimal dependencies of linear-form
  powers* (2026 preprint).  They prove sharp Veronese-circuit dimension bounds
  via Schur-product Kneser theory.  In characteristic two their
  positive-characteristic variant replaces cubic degree 3 by the binary digit
  sum `w_2(3)=2`, giving a `t/2` circuit-span bound.  This is neighboring
  prior art and must be discussed; the present projective-triorthogonal
  `8c/21` support bound is stronger for the collision geometry used here.

The novelty claim must therefore remain the **combined dyadic identifiability
classification**, not Kneser, Sidon sets, Reed-Muller theory, Veronese circuits,
or Hensel lifting separately.

---

## SciSpace professional-index pass — 20 September 2026

A targeted SciSpace search was run across the academic index using full natural-language questions rather than keyword matching.

### Search questions

1. Are there papers proving identifiability or unique decomposition of symmetric cubic tensors over finite local rings `Z/2^m Z), especially overcomplete rank `n+2`?
2. Are there papers connecting binary Sidon sets / minimum-distance-five codes to uniqueness of symmetric cubic tensor decompositions?
3. Are there papers combining Reed–Muller low-weight structure with Hensel lifting for tensor decomposition over finite local rings?
4. What literature studies tensor decomposition over finite local rings, chain rings, `Z/4Z`, or `Z/2^mZ` rather than fields?

### Closest results surfaced

- Kopparty–Potukuchi, *Syndrome decoding of Reed-Muller codes and tensor decomposition over finite fields* (SODA 2018).
  - Explicitly establishes an equivalence between Reed–Muller syndrome decoding and random low-rank tensor decomposition over finite fields.
  - Uses finite-field Jennrich / decoding methods.
  - Does not work over dyadic local rings or give the Sidon/relation-code lifting criterion.

- Czerwinski–Pott, *Sidon sets, sum-free sets and linear codes* (Advances in Mathematics of Communications, 2024).
  - Explicitly recalls the one-to-one correspondence between sum-free Sidon sets in `F_2^t` and binary linear codes with minimum distance at least five.
  - Does not connect this condition to cubic tensor identifiability or local-ring lifting.

- Standard symmetric-tensor identifiability papers (Chiantini–Ottaviani–Vannieuwenhoven and related work).
  - Work over fields, typically `C` / algebraic-geometric settings.
  - Do not address `Z/2^mZ`, Reed–Muller parity supports, or top-bit exact counter-decompositions.

- Searches specifically requesting finite local / chain ring / `Z/4Z` tensor decomposition did not surface a directly matching symmetric cubic identifiability theorem. Returned results were mostly ordinary tensor-ring/network papers or field-based tensor geometry.

### Current novelty statement after the SciSpace pass

The manuscript must not claim novelty for:
- Reed–Muller/tensor correspondence;
- Sidon sets;
- the minimum-distance-five code correspondence;
- Reed–Muller low-weight classification;
- Hensel lifting;
- generic symmetric tensor identifiability.

The remaining candidate novelty is the exact combined theorem:

```
rank r=n+2 symmetric cubic over Z/(2^m)
+ globally rigid parity support for 3<=n<=13
+ relation code K=ker S
+ Sidon iff d(K)>=5
+ ker(J_S)=0 iff Sidon
+ explicit exact top-bit second decomposition for every non-Sidon frame.
```

No directly matching theorem surfaced in the SciSpace searches. This remains a literature finding, not a proof of priority.

### Current mathematical boundary

For `n=14`, parity collisions can first involve weight `32=2d` codewords of `RM(10,14)`. Non-minimal weight-32 words are unions of two disjoint minimum affine 4-flats and therefore have low-dimensional support; they cannot host a rank-14 16-point frame. The unresolved obstruction is a **minimal** weight-32 word whose support has full linear span 14.

That exact geometric question is the next proof target.

---

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
