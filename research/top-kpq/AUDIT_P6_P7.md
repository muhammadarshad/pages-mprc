# Referee Audit — P6 / P7

Audit date: 2026-09-22

Status: **mathematical audit passed after revision; publication remains on hold for external novelty review and typeset proofing.**

This audit is intentionally adversarial. It separates:
- correctness,
- proof completeness,
- terminology,
- classical overlap,
- novelty,
- open claims.

It does not treat computational agreement as a substitute for proof.

---

## P6 — Top-KPQ Completeness and Q-Space Geometry on Even Cyclic Rings

Current source blob: `197633779a193f5476916a3ab978a25695fb4152`

### Verdict

**CORE MATHEMATICS: PROVED under the stated collision congruence.**

No counterexample was found to the completeness theorem. The audit independently rechecked the canonical formula against actual rewriting over 43,043 movement multisets for `H=2..8`, `m=0..5`, with zero mismatches. This is additional regression evidence only; the manuscript proof is now self-contained.

### Audit findings corrected in manuscript

1. **K versus m off-by-one — corrected.**
   - `K` = selected positions.
   - `m=K-1` = movement slots.
   - Correct terminal zero count:
     `z=m-h-[a>0]-[b>0]`.

2. **Unique-terminal proof was too compressed — strengthened.**
   The revised proof explicitly derives `a,b` from `L,P` modulo `H`, then forces `h,z`.

3. **Q integrality/nonnegativity was asserted, not proved — corrected.**
   The manuscript now uses
   `D(e) ≡ e (mod 2)`
   and the circular triangle inequality.

4. **Static simplex derivation was under-explained — corrected.**
   The revised text derives `A mod H`, `B mod H`, the eta coordinates, and
   `eta+ + eta- + eta_H = T`.

5. **Exact admissibility was stated without proof — corrected.**
   Necessity follows from the ordinary-movement cap `H-1`; sufficiency is constructive by decomposing directional totals into bounded movement magnitudes and padding with zero moves.

6. **Minimum order K* lacked a lower-bound proof — corrected.**
   The revised manuscript proves
   `c_H(a+H eta) >= eta+[a>0]`
   and shows the canonical terminal attains equality.

7. **“Affine ring automorphism” was incorrect terminology — corrected.**
   `e -> e+H` is not a group/ring automorphism because it does not fix zero.
   The theorem now concerns **affine bijections of the cyclic movement set**.

8. **Symmetry count corrected.**
   Coordinate permutations act on `m=K-1` movements, so the stated group is
   `S_m x V4`, for `m>=1`.

### Remaining scope boundary

P6 proves completeness only for the stated primitive same-sign collision relations plus movement permutation. It must not be cited as:
- byte identity,
- semantic identity,
- address identity,
- equality of the finer histogram fiber.

This boundary is explicitly stated in the paper.

### Literature / novelty audit

The one-sign move is closely related to classical unit-transfer / majorization operations. Rational-normal-curve toric ideals also have known chip-firing/combinatorial interpretations. Therefore P6 must **not** claim invention of transfer dynamics or general confluence machinery.

Current defensible contribution:
- the exact signed even-cycle `(K,P,Q)` synthesis;
- the explicit terminal coordinates;
- the Q-space simplex/admissibility form;
- the self-conjugate quotient;
- the exact metric-affine action in this model.

**Novelty verdict:** plausible model-specific novelty, but not yet externally established to publication standard. A dedicated prior-art search on equivalent invariants/normal forms is still required before submission.

---

## P7 — Collision Algebras and Exact Dyadic Ramification on the MPRC Ring

Current source blob: `01056113b3c3ff130c9f6a1551ef1052b6edce88`

### Verdict

**MATHEMATICAL SYNTHESIS: PROVED after revision.**

The current manuscript cleanly separates classical algebra from MPRC-specific identification.

### Audit findings corrected in manuscript

1. **Classical rational-normal-curve overlap — corrected.**
   Each one-sign family is exactly the classical Hankel minor ideal of a rational normal curve. Eagon-Northcott, Cohen-Macaulayness, the one-sign Betti table, and related Gröbner-degeneration theory are not claimed as new.

2. **Explicit monomial order was missing — corrected.**
   The manuscript now defines a graded matrix order using
   `w(z)=H^2`, `w(h)=0`, `w(x_i)=w(y_i)=H^2-i^2`,
   for which every primitive source is the leading monomial.

3. **Eagon-Northcott exactness hypothesis was implicit — corrected.**
   The one-sign quotient is finite free over `k[z,h]`, so it has dimension 2; the minor ideal therefore has expected height `H-1`, justifying the Eagon-Northcott resolution.

4. **Tensor-product Betti factorization needed proof — corrected.**
   The two one-sign rings are free/flat over the shared endpoint ring. The manuscript now explains why tensoring their minimal resolutions is exact and remains minimal.

5. **Dense localization was not written as an isomorphism — corrected.**
   The manuscript now records
   `A_{D,U} ~= D[z^{±1},t^{±1}] tensor_D D[u]/(u^128-1)`
   and gives the forward/inverse coordinates.

6. **Transfer of nilpotence from the cyclic factor to the dense algebra — corrected.**
   The Laurent factor is faithfully flat over `D`, so the exact ideal-power index transfers.

7. **Notation collision in the ramification proof — corrected.**
   The relative rotor `u` was incorrectly reused as an “odd unit” coefficient.
   The binomial coefficient is now written
   `C(128,64)=2 omega`, with `omega` an odd scalar unit.

8. **Final layer generation needed proof — corrected.**
   The manuscript now shows every degree-575 generator containing a factor `2^a`, `a>=1`, has weight (>575) and vanishes, so
   `m^575=<128 epsilon^127>`.

9. **Augmentation ideal versus Jacobson radical — corrected.**
   In
   `T_8=(Z/256)[C_128]`,
   the augmentation ideal is `(epsilon)`.
   The larger local radical is `m=(2,epsilon)`.
   These are not the same ideal.

### Classical ramification overlap

The nilpotency index of the **augmentation ideal** `(epsilon)` is already covered by classical cyclic group-ring / periodic-polynomial results. The cyclic formula
[

u=(eta(p-1)+1)p^{alpha-1}
]
gives, for `p=2, alpha=7, beta=8`,
[

u=9*64=576.
]

Therefore **“epsilon has index 576” is not a new general theorem**.

What the manuscript additionally proves in its own MPRC weight calculation is:
- identification of the dense MPRC relative factor with this cyclic group ring;
- every mixed generator `2^a epsilon^(576-a)` vanishes;
- hence the larger radical `(2,epsilon)` also has exact index 576;
- faithful-flat transfer gives the same exact index for the extended dense-diagonal ideal.

A broader literature search is still needed before claiming that the full-radical equality is novel in group-ring theory.

### Field-side novelty

The following are classical once the MPRC collision ideal is recognized:
- rational-normal-curve Hankel minors;
- Eagon-Northcott resolution;
- one-sign Cohen-Macaulayness;
- rational-normal-curve/chip-firing connections.

The two-sign shared-endpoint tensor synthesis and its MPRC interpretation are the appropriate focus, not rediscovery claims about those classical components.

### Open result deliberately excluded

The full analytic presentation of
`gr_m(T_8)`
is **not proved in P7** and remains open.

The CXR / ViT numerical bridge is also excluded.

---

## Literature anchors confirmed during audit

- Marshall, Olkin, Arnold — *Inequalities: Theory of Majorization and Its Applications*, 2nd ed., Springer, 2011.
- Karki, Manjunath — *Rational Normal Curves, Chip Firing and Free Resolutions*, arXiv:2301.09104.
- Eagon, Northcott — *Ideals defined by matrices and a certain complex associated with them*, Proc. Royal Soc. A 269 (1962).
- Richard M. Wilson — *A lemma on polynomials modulo p^m and applications to coding theory*, Discrete Mathematics 306 (2006), DOI 10.1016/j.disc.2004.10.030.
- Uwe Schauz — *The Largest Possible Finite Degree of Functions between Commutative Groups*, arXiv:2103.16467; its cyclic formula reproduces the augmentation index 576.

---

## Publication gate

### P6
- Mathematical proof: **PASS**
- Internal regression: **PASS**
- Terminology/scope: **PASS after revision**
- Prior-art / novelty review: **HOLD**
- Typeset compile/proofread: **HOLD**

### P7
- Mathematical proof of stated synthesis: **PASS**
- Classical attribution: **PASS after revision**
- Dense-radical index proof: **PASS**
- Novelty of general algebra facts: **NOT CLAIMED**
- Novelty of full-radical 576 statement: **HOLD pending deeper literature review**
- Associated graded theorem: **OPEN / excluded**
- Typeset compile/proofread: **HOLD**

## Overall audit verdict

**Neither paper should be published yet.**

But the reason is no longer an unresolved mathematical contradiction.

The current blockers are:
1. external novelty/prior-art review;
2. typeset compilation and line-by-line PDF proofing;
3. for P7, deciding whether the strongest publication framing is a standalone algebra paper or an MPRC application/synthesis paper.

The proved mathematics presently survives the audit.
