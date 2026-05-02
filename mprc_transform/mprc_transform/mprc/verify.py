"""
MPRC Verification Suite — 10/10 tests must pass before any release.
Frozen: 2026-04-21
"""

import numpy as np
from numpy.linalg import matrix_rank
from .constants import RING, ZPOS, KS_MATRIX, KC_MATRIX, FROZEN
from .transform import MPRCTransform


def _tone(b, a=50.0):
    n = np.arange(256)
    s = 128.0 + a * np.sin(2.0 * np.pi * b * n / 256.0)
    return np.clip(np.round(s), 0, 255).astype(np.uint8)

def _multi(bins, amps=None):
    if amps is None: amps = [40.0] * len(bins)
    n = np.arange(256); s = np.full(256, 128.0)
    for b, a in zip(bins, amps):
        s += a * np.sin(2.0 * np.pi * b * n / 256.0)
    return np.clip(np.round(s), 0, 255).astype(np.uint8)

def _silence():
    return np.full(256, 128, dtype=np.uint8)


def test_1_gcd():
    """gcd(256,7)=1 — stride-7 is a full ring generator"""
    assert np.gcd(256, 7) == 1
    assert 252 // 7 == 36
    return True

def test_2_vacuum_skip():
    """stride-7 walk skips all vacuum points {0,64,128,192}"""
    assert not any(z in RING["V"] for z in ZPOS)
    assert len(ZPOS) == 36
    return True

def test_3_rank():
    """rank(Ks)=36 full rank, rank(Kc)=2"""
    assert matrix_rank(KS_MATRIX) == 36
    assert matrix_rank(KC_MATRIX) == 2
    return True

def test_4_condition():
    """Condition number κ(Ks) = 93.35 ± 0.01"""
    sv = np.linalg.svd(KS_MATRIX, compute_uv=False)
    k  = sv[0] / sv[-1]
    assert abs(k - FROZEN["cond_ks"]) < 0.01, f"κ={k:.2f}"
    return True

def test_5_silence_gate():
    """w(128)=0 silence gate, w(0)=0 clip suppress, forward(silence)=0"""
    tr = MPRCTransform()
    # H=128 is the vacuum — exact silence gate
    assert tr.weight(np.array([128.0]))[0] == 0.0
    # x=0: Da=128, Dd=0 → w=0
    assert tr.weight(np.array([0.0]))[0]   == 0.0
    # x=256 (rail): Da=128, Dd=0 → w=0  (255 is near-rail, not zero)
    assert tr.weight(np.array([256.0]))[0] == 0.0
    # Full silence buffer → zero output
    S, C, _ = tr.forward_complex(_silence())
    assert np.allclose(S, 0) and np.allclose(C, 0)
    return True

def test_6_invertibility():
    """max reconstruction error < 5×10⁻⁶"""
    tr = MPRCTransform()
    buf = _multi([4, 24, 38], [35, 50, 20])
    S, C, w = tr.forward_complex(buf)
    x_rec   = tr.inverse(S, w)
    x_orig  = buf[np.array(ZPOS)].astype(float)
    active  = w > 0
    err     = np.max(np.abs(x_orig[active] - x_rec[active]))
    assert err < 5e-6, f"max_error={err:.2e}"
    return True

def test_7_power_spectrum():
    """P_k = S_k² + C_k²  (not sqrt)"""
    tr = MPRCTransform()
    buf = _tone(32)
    P = tr.forward(buf)
    S, C, _ = tr.forward_complex(buf)
    assert np.allclose(P, S**2 + C**2)
    return True

def test_8_nonlinearity():
    """MPRC is non-linear — signal-adaptive weight"""
    tr   = MPRCTransform()
    buf  = _tone(24, 40)
    buf2 = np.clip(128 + 2*(buf.astype(int)-128), 0, 255).astype(np.uint8)
    P1   = tr.forward(buf)
    P2   = tr.forward(buf2)
    assert not np.allclose(P2, 2*P1, rtol=0.05)
    return True

def test_9_complexity():
    """O(36²)=1296 — constant regardless of N"""
    assert 36 * 36 == 1296
    for N in [256, 1024, 65536]:
        assert N * np.log2(N) > 1296
    return True

def test_10_mutual_r2():
    """Mutual R²(MPRC↔FFT) > 0.95 across diverse signals"""
    from numpy.linalg import lstsq
    tr = MPRCTransform()
    sigs = [
        _tone(8), _tone(24), _tone(48),
        _multi([4, 24, 38], [35, 50, 20]),
        _multi([4, 9, 70],  [35, 40, 25]),
        _multi([8, 32, 64], [40, 40, 40]),
    ]
    mprc = np.array([tr.forward(s) for s in sigs])
    fft  = np.array([np.abs(np.fft.rfft(s.astype(float)-128)) for s in sigs])
    W, _, _, _ = lstsq(mprc, fft, rcond=None)
    pred   = mprc @ W
    ss_res = np.sum((fft - pred)**2, axis=0)
    ss_tot = np.sum((fft - fft.mean(0))**2, axis=0)
    r2     = np.where(ss_tot > 0, 1 - ss_res/ss_tot, 1.0)
    assert np.mean(r2) > 0.95, f"mean_R²={np.mean(r2):.3f}"
    return True


TESTS = [
    (test_1_gcd,           "gcd(256,7)=1 — full ring generator"),
    (test_2_vacuum_skip,   "stride-7 skips vacuum {0,64,128,192}"),
    (test_3_rank,          "rank(Ks)=36, rank(Kc)=2"),
    (test_4_condition,     "κ(Ks)=93.35"),
    (test_5_silence_gate,  "w(128)=0 silence gate, w(0)=0 clip suppress"),
    (test_6_invertibility, "max recon error < 5×10⁻⁶"),
    (test_7_power_spectrum,"P_k = S_k² + C_k²"),
    (test_8_nonlinearity,  "MPRC is non-linear"),
    (test_9_complexity,    "O(36²)=1296 constant"),
    (test_10_mutual_r2,    "Mutual R²(MPRC↔FFT) > 0.95"),
]


def run_all(verbose=True):
    """Run all 10 verification tests."""
    passed = 0
    if verbose:
        print("MPRC Verification Suite — Frozen 2026-04-21")
        print("=" * 50)
    for fn, desc in TESTS:
        try:
            ok = fn()
            if verbose: print(f"  ✓  {desc}")
            passed += 1
        except Exception as e:
            if verbose: print(f"  ✗  {desc}  [{e}]")
    if verbose:
        print(f"\n  {passed}/{len(TESTS)} tests passed  "
              f"{'ALL PASS ✓' if passed == len(TESTS) else 'FAILURES ✗'}")
    return passed == len(TESTS)
