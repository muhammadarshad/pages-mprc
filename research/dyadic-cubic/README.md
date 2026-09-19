# Dyadic Cubic Research Series

Muhammad Arshad · [ORCID 0009-0002-1314-0494](https://orcid.org/0009-0002-1314-0494) · Published September 20, 2026 · v1 · CC BY 4.0

The five individual Zenodo records are the authoritative citations for this series. The MPRC chapters and collective booklet serve as an index; cite the relevant individual paper. The publication PDFs were frozen without embedding DOI text.

| Paper | Canonical publication | Verification |
|---|---|---|
| P1 — Simplex Cubic Decomposition | [10.5281/zenodo.22850767](https://doi.org/10.5281/zenodo.22850767) | [verify_quantinion_simplex_cubic.py](verification/verify_quantinion_simplex_cubic.py) |
| P2 — Exact Cubic Dictionary Capacity | [10.5281/zenodo.22850810](https://doi.org/10.5281/zenodo.22850810) | [verify_cubic_dictionary_capacity.py](verification/verify_cubic_dictionary_capacity.py) |
| P3 — Eight-State Operator / Transpose Geometry | [10.5281/zenodo.22850830](https://doi.org/10.5281/zenodo.22850830) | [verify_quantinion_operator_geometry.py](verification/verify_quantinion_operator_geometry.py) |
| P4 — Dimension-Free n+2 Identifiability | [10.5281/zenodo.22850834](https://doi.org/10.5281/zenodo.22850834) | Analytical proof; no finite verifier |
| P5 — n+3 Koszul–Sidon Rigidity | [10.5281/zenodo.22850842](https://doi.org/10.5281/zenodo.22850842) | [t3_koszul_certificate.py](verification/t3_koszul_certificate.py) |

## Citations

- Arshad, M. (2026). *Quantinion Simplex Cubic Decomposition over 2-Power Rings: Global Identifiability from Binary Contractions and Exact Bit Lifting* (v1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.22850767
- Arshad, M. (2026). *Exact Free Capacity of Symmetric Rank-One Cubic Dictionaries over Dyadic Rings* (v1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.22850810
- Arshad, M. (2026). *An Eight-State Operator and Transpose Geometry over Dyadic Rings: Trace-Zero Modules, Mixed-Radix Addressing, and Tensor-Lift Kernels* (v1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.22850830
- Arshad, M. (2026). *Dimension-Free Identifiability of (n+2) Symmetric Cubics over Dyadic Rings* (v1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.22850834
- Arshad, M. (2026). *Koszul–Sidon Rigidity for (n+3) Cubic Decompositions over Dyadic Rings* (v1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.22850842

## Reproducibility and release provenance

Paper 5 archives its PDF, `t3_koszul_certificate.py`, and `t3_koszul_certificate.json` together in its DOI record. The unchanged script passed all 20 admissible cases during the freeze check.

The [original freeze check](release-v1/FREEZE_CHECK.md) is retained as a historical prepublication snapshot; its hold language describes that earlier stage. See the [publication report](release-v1/PUBLICATION_REPORT.md) and [verification results](release-v1/PUBLICATION_VERIFICATION.json) for the completed release. The [publication SHA-256 manifest](release-v1/SHA256SUMS_PUBLICATION.txt) supersedes the earlier RC2 manifest for these seven files. Filenames in that manifest refer to files downloaded from the corresponding Zenodo records.

Postpublication verification independently downloaded all seven public files and confirmed exact SHA-256 matches to the frozen manifest.
