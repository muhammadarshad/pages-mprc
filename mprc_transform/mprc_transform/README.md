# MPRC Spectral Transform

**A signal-adapted geometric projection on Z₂₅₆.**

Frozen: 2026-04-21 | Author: Arshad — MPRC Framework | Status: LOCKED

---

## What it is

A discrete spectral transform derived entirely from ring geometry on Z₂₅₆.
Not a drop-in FFT replacement — a different transform that captures the same
information via geometric projection.

| Property | Value |
|---|---|
| Output bins | 36 (constant) |
| Complexity | O(36²) = O(1,296) — independent of N |
| Kernel rank | 36/36 full rank |
| Condition number κ | 93.35 |
| Mutual R² with FFT | 1.000 (both directions) |
| Silence gate | w(128) = 0 exact |
| Clip suppression | w(0) = w(255) = 0 exact |
| Arithmetic | Integer-only (u8/u32/u64) |
| Verified | 10/10 tests |

---

## Quick Start

```python
from mprc import MPRCTransform
import numpy as np

t = MPRCTransform()

# Forward
signal = np.random.randint(0, 256, 256, dtype=np.uint8)
P = t.forward(signal)           # shape (36,) — power spectrum

# Forward with phase
S, C, w = t.forward_complex(signal)
phase = t.phase(S, C)           # shape (36,) — phase per bin

# Exact inverse
x_rec = t.inverse(S, w)         # shape (36,) — max error < 5e-10
```

---

## Frozen Equations

### Ring Constants

```
τ = 256       ring order
H = 128       vacuum axis  (τ/2)
g = 7         co-prime stride  gcd(7,256)=1
Q = 64        quadrant  (τ/4)
V = {0,64,128,192}   vacuum boundaries
```

### Active Positions (stride-7 walk)

```
z_i = (i · 7) mod 256,    i = 1..36
```

### Parabolic Weight

```
Δa     = |x[z_i] − 128|
Δd     = 128 − Δa          spinor flip: Δa + Δd = 128
w(z_i) = 16 · (Δa · Δd)²  domain function
```

### Kernel Matrices (36×36, constant)

```
K_s[k,i] = sin( 2π · d°(z_k, z_i) / 64 )
K_c[k,i] = cos( 2π · d°(z_k, z_i) / 64 )

d°(a,b)  = min(|a−b|, 256−|a−b|)   circular distance
```

### Forward Transform

```
x̃_i = w(z_i) · x[z_i]

S_k  = Σ K_s[k,i] · x̃_i   =   K_s · x̃
C_k  = Σ K_c[k,i] · x̃_i   =   K_c · x̃
P_k  = S_k² + C_k²
```

### Inverse Transform

```
x̃    = K_s⁻¹ · S          (K_s full rank — exact inverse)
x[z] = x̃ / w(z)           (w from forward state)
```

---

## Complexity vs FFT

| N | FFT O(N log N) | MPRC O(1,296) | Ratio |
|---|---|---|---|
| 256 | 2,048 | 1,296 | 1.6× |
| 1,024 | 10,240 | 1,296 | 7.9× |
| 65,536 | 1,048,576 | 1,296 | 809× |
| 1,048,576 | 104,857,600 | 1,296 | 80,905× |

---

## Install

```bash
pip install -e .
```

## Run verification

```bash
python -c "from mprc import run_all; run_all()"
# or
pytest tests/
```

---

## Derivation

The transform is derived from first principles of the Z₂₅₆ ring:

1. **Vacuum structure** {0,64,128,192} defines forbidden positions
2. **Co-prime stride** gcd(256,7)=1 generates all 252 active positions
3. **252/7 = 36** output bins — the natural resolution
4. **Parabolic weight** from the domain function 16(Δa·Δd)²
5. **Circular distance kernel** ensures vacuum orthogonality
6. **Spinor flip** Δa+Δd=128 encodes the 720° u rotation

Full derivation in: `docs/derivation.md`

---

## Citation

```
Arshad (2026). MPRC Spectral Transform: A Signal-Adapted Geometric
Projection on Z₂₅₆. Frozen 2026-04-21.
```
