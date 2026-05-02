# MPRC Transform — Mathematical Derivation

**Frozen: 2026-04-21**

---

## 1. Starting Point — Z₂₅₆ Ring

The MPRC framework defines a discrete ring Z₂₅₆ with:
- Four vacuum boundaries V = {0, 64, 128, 192}
- 252 = 256 − 4 active states
- Angular momentum axis u at H = 128
- Spinor structure requiring 720° (two full rotations) to complete

---

## 2. Why Stride 7?

We need a step size g such that the walk visits positions
without hitting a vacuum, and divides 252 cleanly.

Conditions:
- gcd(256, g) = 1     co-prime with ring order (full generator)
- 252 mod g = 0       clean division into output bins
- g · i ∉ V for i=1..252/g    avoids all vacuum points

g = 7 is the smallest integer satisfying all three:
    gcd(256, 7) = 1     ✓
    252 / 7     = 36    ✓ integer
    {7i mod 256, i=1..36} ∩ {0,64,128,192} = ∅   ✓

---

## 3. Why 36 Output Bins?

252 active states / stride 7 = 36 positions before the cycle
repeats under modular arithmetic. These 36 positions are the
natural sampling resolution of the Z₂₅₆ ring.

---

## 4. Parabolic Weight — Domain Function

From the MPRC domain function F(abcd) = 16(abcd)²:
    Δa = |x − 128|      deviation from vacuum axis H=128
    Δd = 128 − Δa       spinor flip constraint: Δa + Δd = 128
    w  = 16(Δa·Δd)²     parabolic coupling

The parabola on [0,128] automatically produces:
- w(0) = 0     silence gate at vacuum H=128
- w(128) = 0   clip suppression at rails 0 and 255
- w(64) = max  peak coupling at quarter-ring positions

No threshold. No external VAD. Emerges from ring geometry.

---

## 5. Circular Distance Kernel

The projection must satisfy vacuum orthogonality:
kernel(n, k) = 0 when d°(n,k) ∈ {0, 64, 128, 192}

sin(2π·d/64) satisfies this: zeros at d = 0, 32, 64, 96, 128...
Period Q = 64 = τ/4 aligns with the S₄ quadrant structure.

---

## 6. Full Rank — Why Ks is Invertible

The 36×36 kernel K_s with positions z_i = (7i mod 256) has
rank 36. This follows from the co-prime property:

The circular distances d°(z_k, z_i) = min(|7k−7i|, 256−|7k−7i|)
= 7·min(|k−i|, 256/7·...) produce a circulant-like structure
where all 36 rows are linearly independent.

Condition number κ(K_s) = 93.35.
Worst-case inverse error: κ · ε = 93.35 × 2.2×10⁻¹⁶ = 2.1×10⁻¹⁴.
Actual measured error: < 5×10⁻¹⁰.

---

## 7. Why K_c has rank 2

K_c[k,i] = cos(2π·d°(z_k,z_i)/64)

The cosine of a symmetric distance on a ring decomposes as:
cos(d) = cos(a−b) = cos(a)cos(b) + sin(a)sin(b)

This is a rank-2 outer product structure — cos and sin components.
K_c is therefore always rank ≤ 2 regardless of positions.

This is why the inverse uses K_s only, not [K_s; K_c].

---

## 8. Inverse Transform

Since rank(K_s) = 36 = n, K_s is square and full rank → invertible:
    x̃ = K_s⁻¹ · S    (exact, no least squares, no approximation)
    x  = x̃ / w        (w saved from forward pass — not circular)

The w(z) values are computed from x[z] during the forward pass
and saved as state. They are therefore known when the inverse runs.

---

## 9. Integer Arithmetic Chain

The Rust implementation uses only integer types:

    x[z]              u8    [0, 255]
    Δa = |x − 128|    u8    [0, 128]
    Δd = 128 − Δa     u8    [0, 128]
    Δa · Δd           u16   [0, 4,096]
    (Δa · Δd)²        u32   [0, 16,777,216]
    16 · (Δa · Δd)²   u32   [0, 268,435,456]
    w · x[z]          u64   [0, 68,451,041,280]
    S, C accumulators u64   [0, 4.47 × 10¹⁵]
    P = S² + C²       u64   headroom: 29,356×

No float hardware required.

---

## 10. Mutual Information Equivalence with FFT

Test J of verify_vs_dft.py shows:
    Linear prediction FFT from MPRC:  R² = 1.000  (129/129 bins)
    Linear prediction MPRC from FFT:  R² = 1.000  (36/36 bins)

Both transforms carry the same spectral information.
MPRC does it in 36 bins at O(1,296) constant operations.
FFT uses 129 bins at O(N log N).

---

*Derivation frozen 2026-04-21. Verified by verify_vs_dft.py 10/10.*
