# Post-Series MPRC Collision Papers

Muhammad Arshad · September 2026

This directory separates the post-five-paper Top-KPQ/Q-space results from the immutable publication provenance under \`research/dyadic-cubic/release-v1/\`.

## Manuscripts

### P6 — Top-KPQ Completeness and Q-Space Geometry on Even Cyclic Rings

Source: [top_kpq_qspace_geometry.tex](top_kpq_qspace_geometry.tex)

Core proved results:

- \`F(c1)=F(c2) iff c1~c2\` for the primitive MPRC collision congruence.
- Corrected convention: \`K\` selected positions, \`m=K-1\` movements.
- Canonical terminal \`(a,b,h,z)\` with
  \`z=m-h-[a>0]-[b>0]\`.
- Exact static Q-space simplex and admissibility.
- Exact minimum order \`K*\`.
- Self-conjugate sheet quotient \`Delta_T/Z2\`.
- Exact metric-affine symmetry \`S_m x V4\`.

### P7 — Collision Algebras and Exact Dyadic Ramification on the MPRC Ring

Source: [collision_algebra_dyadic_ramification.tex](collision_algebra_dyadic_ramification.tex)

Core proved results:

- Primitive collision quadrics are two shared-endpoint Hankel minor families.
- Quadratic Groebner basis and
  \`in(I_H)=X^2+Y^2\`.
- \`Hilb(t)=((1+(H-1)t)^2)/(1-t)^2\`.
- Cohen-Macaulay, Koszul, dimension 2, projective dimension \`2H-2\`.
- Squared Eagon-Northcott Betti polynomial.
- Dense localization collapses to one relative rotor \`u^128=1\`.
- Over \`Z256\`,
  \`p^575 != 0\`, \`p^576=0\`, terminal layer \`<128 epsilon^127>\`.
- Exact dense ramification length \`576=9*64\`.

## Deliberately open

These are not promoted into either paper:

- complete analytic presentation of \`gr_p\`;
- structural identification of the CXR \`3x3 -> 4x4\` lift with
  \`252=4*7*9 -> 576=4*9*16\`;
- any claim that ViT \`24x24\` geometry is algebraically identical to the ramification result.

## Provenance

The booklet exposition is [Chapter 26](../../chapter-26.html).

The theorem ledger and reference gates live in:

- \`muhammadarshad/siliq-rotor/MATH_LEDGER.md\`
- \`model/motif/collision_theorem.py\`
- \`model/motif/audit_collision.py\`
- \`model/motif/audit_simplex.py\`
- \`model/motif/audit_qspace_symmetry.py\`

The earlier five-paper Dyadic Cubic Series and its DOI records are unchanged.
