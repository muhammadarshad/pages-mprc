# Dyadic Cubic Paper Verification

Exact reference programs for the five-paper dyadic cubic series.

| Paper | Verification |
|---|---|
| Paper 1 — Simplex Cubic Decomposition | `verify_quantinion_simplex_cubic.py` |
| Paper 2 — Exact Cubic Dictionary Capacity | `verify_cubic_dictionary_capacity.py` |
| Paper 3 — Eight-State Operator / Transpose Geometry | `verify_quantinion_operator_geometry.py` |
| Paper 4 — Dimension-Free n+2 Identifiability | analytical proof; no finite verifier required |
| Paper 5 — n+3 Koszul–Sidon Rigidity | `t3_koszul_certificate.py` |

All programs use exact integer/GF(2) arithmetic only. Paper 5's program is part of the computer-assisted proof: it verifies the 20 analytically admissible GL(3,2) orbit representatives after the dimension-free reduction.
