# Top-KPQ Booklet Freeze Record

Frozen: 2026-09-21 · updated after M-010/M-011

## Source mathematics

Pinned SILIQ/MPRC source commit:

`7c99e8f85859e3d6294f0533dbe385fed3b31e44`

Authoritative source paths at that commit:

- `MATH_LEDGER.md`
- `model/motif/collision_theorem.py`
- `model/motif/audit_collision.py`
- `model/motif/audit_simplex.py`

## Booklet artifacts

- `chapter-26.html`
  - Git blob: `edee36609caacc70e0dba57484f862c2409dd79d`
  - Contains Theorem 26.1 (Top-KPQ Completeness) and Theorem 26.2 (Dense MPRC Collision Ramification).
- `research/top-kpq/README.md`
  - Git blob: `00b610132f83156707c427d4fe6cf98324048f41`
  - Contains the theorem register, proof spine, provenance, and open-boundary list.

## Promotion boundary

Frozen as proved:

1. Top-KPQ completeness for the stated primitive MPRC rewrite congruence.
2. Dense-diagonal Z256 collision ramification: `p^575 != 0`, `p^576 = 0`.

Frozen as additional theorems after the first record:

3. Self-conjugate sheet quotient: on `P in {0,H}`, the unoriented simplex is `Delta_T/Z2`.
4. Exact metric-affine symmetry: `S_K x V4` for coordinate permutations and the four uniform affine ring maps `I,C,A,AC`.
5. Collision presentation closure: quadratic Groebner basis, initial ideal `X^2+Y^2`, Hilbert series, Cohen-Macaulay/Koszul status, projective dimension, and squared Eagon-Northcott Betti polynomial.

Still open:

- the full associated-graded layer algebra `gr_p` (exact filtration data obtained; analytic presentation not yet frozen);
- the CXR identification of `252=4*7*9` and `576=4*9*16`. The current stored CXR/ViT sources explicitly support the 3x3/252 side but do not yet define the 4x4/576 map, so this remains unpromoted.

This file is a repository freeze marker, not a DOI publication record.


## Gate-discovered notation correction

Claude's independent ROTOR gate found an off-by-one in the first booklet writeup, not in the completeness theorem.

Frozen convention:

- `K` = number of selected positions/states.
- `m=K-1` = number of movements.
- The canonical terminal counts movement slots, hence
  `z=m-h-[a>0]-[b>0]=(K-1)-h-[a>0]-[b>0]`.

The earlier `z=K-h-...` wording is superseded. The theorem `F(c1)=F(c2) iff c1~c2` is unchanged.
