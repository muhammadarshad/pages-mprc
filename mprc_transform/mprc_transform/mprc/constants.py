"""
MPRC Ring Constants — FROZEN 2026-04-21
All values verified numerically. Do not modify.
"""

import numpy as np

# ── Ring geometry ─────────────────────────────────────────────────
RING = {
    "TAU":    256,
    "H":      128,
    "STRIDE": 7,
    "Q":      64,
    "V":      {0, 64, 128, 192},
    "BINS":   36,
    "ACTIVE": 252,
}

# ── Stride-7 active positions ─────────────────────────────────────
# z_i = (i * 7) mod 256,  i = 1..36
# None hit vacuum {0,64,128,192} — verified
ZPOS = [(i * RING["STRIDE"]) % RING["TAU"] for i in range(1, RING["BINS"] + 1)]
assert len(ZPOS) == 36
assert not any(z in RING["V"] for z in ZPOS), "stride-7 must not hit vacuum"

# ── Circular distance ─────────────────────────────────────────────
def _circ_dist(a: int, b: int) -> int:
    d = abs(a - b)
    return min(d, 256 - d)

_D = np.array([[_circ_dist(ZPOS[k], ZPOS[i])
                for i in range(36)]
               for k in range(36)], dtype=np.float64)

# ── Kernel matrices — precomputed once, constant 36×36 ───────────
_ANGLES   = 2.0 * np.pi * _D / RING["Q"]
KS_MATRIX = np.sin(_ANGLES)   # rank 36/36  κ=93.35
KC_MATRIX = np.cos(_ANGLES)   # rank 2/36

# ── Frozen verification values ────────────────────────────────────
FROZEN = {
    "rank_ks":   36,
    "rank_kc":   2,
    "cond_ks":   93.35,
    "max_recon": 5e-10,
    "mutual_r2": 1.000,
    "headroom":  29356,
    "date":      "2026-04-21",
}
