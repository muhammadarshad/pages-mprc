# Submission Readiness — Papers 1–3

Updated: 18 September 2026

This directory separates the public MPRC booklet/preprint presentation from journal-facing submission material.

## Submission policy

- Submit only one journal at a time for each manuscript.
- The public GitHub/booklet copies are author preprints, not peer-reviewed publications.
- Elsevier's general policy permits authors to share preprints before submission.
- Taylor & Francis likewise permits author preprints; journal-specific instructions should still be checked immediately before submission.
- On acceptance, update the public preprint page with the final DOI and journal citation.
- Do not present computational regression as a substitute for a theorem proof.
- Keep the explicit falsification boundaries in the manuscripts.

## Paper 1

**Journal-facing title**  
Simplex Cubic Decomposition over 2-Power Rings: Global Identifiability from Binary Contractions and Exact Bit Lifting

**Primary target**  
Linear Algebra and its Applications (Elsevier)

**Why it fits**  
The journal explicitly covers algebraic, arithmetic, combinatorial and geometric finite-dimensional linear algebra. The paper is a tensor-identifiability theorem over finite local rings with a constructive exact recovery algorithm.

**Secondary target**  
Linear and Multilinear Algebra (Taylor & Francis)

**Public preprint**  
../quantinion_simplex_cubic_decomposition.tex

**Key claim**  
For even n >= 4, an (n+1)-atom symmetric cubic over Z/(2^m) whose parity atoms form a binary simplex frame is globally identifiable up to permutation. A structured residual-simplex r=n+2 extension is also proved within that family.

**Do not claim**
- generic overcomplete tensor decomposition;
- arbitrary rank n+2 identifiability;
- uniqueness under non-unit/even weighting without extra hypotheses.

## Paper 2

**Journal-facing title**  
Exact Free Capacity of Symmetric Rank-One Cubic Dictionaries over Dyadic Rings

**Primary target**  
Linear Algebra and its Applications

**Secondary target**  
SIAM Journal on Discrete Mathematics, if the presentation is shifted toward Boolean incidence matrices and combinatorial module rank.

**Public preprint**  
../exact_cubic_dictionary_capacity.tex

**Key claim**  
The maximal free dictionary of symmetric rank-one cubic atoms over Z/(2^m) has cardinality
sum_{k=1}^{min(3,n)} binom(n,k), attained explicitly. For n=8 the exact capacity is 92.

**Do not claim**
- generic tensor rank 92;
- unknown-atom identifiability at rank 92;
- that the subset-incidence/zeta matrix itself is new.

## Paper 3

**Journal-facing title**  
An Eight-State Operator and Transpose Geometry over Dyadic Rings: Trace-Zero Modules, Mixed-Radix Addressing, and Tensor-Lift Kernels

**Primary target**  
Linear and Multilinear Algebra

**Stretch target**  
Journal of Algebra, only after strengthening the general ring-theoretic formulation beyond the n=8 specialization.

**Public preprint**  
../quantinion_operator_transpose_geometry.tex

**Key claims**
- trace-zero M_8(Z/(2^m)) has an explicit free rank-63 basis;
- 14 reference couplings generate the trace-zero module under commutators and module span;
- the frozen QH4 address simplifies to mixed radix 64,21,7,1;
- the local transpose orbit decomposition is exact;
- ker rho_l = {lambda I : l lambda = 0 mod 2^m}.

**Classical material that must remain attributed**
- the Frobenius group F21;
- elementary matrix-unit identities;
- general trace-zero/commutator background.

## Repository submission files

- paper1_cover_letter.md
- paper2_cover_letter.md
- paper3_cover_letter.md
- paper1_highlights.txt
- paper2_highlights.txt
- paper3_highlights.txt

## Final pre-submission checklist

1. Re-run all exact verifier scripts from a clean Python environment.
2. Compile each TeX manuscript twice and clear all warnings that affect references.
3. Verify every DOI, author name, year, volume and page range.
4. Add author affiliation, postal address, email and ORCID on the journal portal.
5. Declare the public preprint in the cover letter/submission form.
6. Run a similarity check before submission.
7. Ensure no manuscript is under simultaneous consideration elsewhere.
8. Archive the exact submitted commit SHA.
