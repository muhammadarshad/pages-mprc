# Dyadic Cubic Paper Verification

Exact reference programs for the [five-paper dyadic cubic series](../README.md), published individually on Zenodo on September 20, 2026. The DOI records contain the canonical publication files.

| Paper | Canonical DOI | Verification |
|---|---|---|
| Paper 1 — Simplex Cubic Decomposition | [10.5281/zenodo.22850767](https://doi.org/10.5281/zenodo.22850767) | `verify_quantinion_simplex_cubic.py` |
| Paper 2 — Exact Cubic Dictionary Capacity | [10.5281/zenodo.22850810](https://doi.org/10.5281/zenodo.22850810) | `verify_cubic_dictionary_capacity.py` |
| Paper 3 — Eight-State Operator / Transpose Geometry | [10.5281/zenodo.22850830](https://doi.org/10.5281/zenodo.22850830) | `verify_quantinion_operator_geometry.py` |
| Paper 4 — Dimension-Free n+2 Identifiability | [10.5281/zenodo.22850834](https://doi.org/10.5281/zenodo.22850834) | analytical proof; no finite verifier required |
| Paper 5 — n+3 Koszul–Sidon Rigidity | [10.5281/zenodo.22850842](https://doi.org/10.5281/zenodo.22850842) | `t3_koszul_certificate.py` |

All programs use exact integer/GF(2) arithmetic only. Paper 5's program is part of the computer-assisted proof: it verifies the 20 analytically admissible GL(3,2) orbit representatives after the dimension-free reduction.

Paper 5 also archives the JSON certificate alongside the PDF and verifier in its DOI record. See the [release provenance](../README.md#reproducibility-and-release-provenance).
