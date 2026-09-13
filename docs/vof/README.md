# QH4 VOF Interface Reconstruction — Reproducibility Bundle

Companion source for **Chapter 19: Volume-of-Fluid Interface Reconstruction on the QH4 Ring**.

The paper ties its numerical claims to executable programs. This directory preserves the supplied sources alongside the web chapter.

## Files

- `mprc_core.py` — QH4 / quaternion-ring structural checks used by the supplied research bundle.
- `ring_plic.py` — ring-native PLIC encoding, finite-difference branch generation, offset inversion and curvature checks.
- `verify_all.py` — extended verification and isotropy/dyadic checks from the supplied bundle.
- `diag3.c` — pure-translation diagnostic for the corrected signed-normal PLIC flux.
- `vof3d.c` — 3-D unsplit decomposition-invariance comparison across naive float, Kahan, fixed-point accumulation and the Z_256 ring path.
- `repro_vof.c` — 2-D decomposition reproducibility experiment on the corrected PLIC scheme.
- `accuracy_vof.c` — Rider–Kothe reversed-vortex accuracy benchmark and ring-depth experiments.

## Typical builds

```bash
gcc -O2 -o diag3 diag3.c -lm
gcc -O2 -o vof3d vof3d.c -lm
gcc -O2 -o repro_vof repro_vof.c -lm
gcc -O2 -o accuracy_vof accuracy_vof.c -lm
```

Python programs can be run directly with a compatible Python 3 environment; `ring_plic.py` uses NumPy.

## Claim boundary

The manuscript explicitly distinguishes verified 2-D results from untested extensions. In particular, the 2-D ring-depth law is tested, while the corresponding 3-D scaling law remains a prediction. Normal estimation remains floating-point in the reference implementation, and the manuscript makes no performance claim against the analytic Scardovelli–Zaleski inversion.

See [`../../chapter-19.html`](../../chapter-19.html) for the web edition.
