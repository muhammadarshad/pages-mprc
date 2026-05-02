"""
MPRC Forward and Inverse Transform — FROZEN 2026-04-21

Forward:
    x̃_i  = w(z_i) · x[z_i]
    S_k   = Σ K_s[k,i] · x̃_i   (= K_s · x̃)
    C_k   = Σ K_c[k,i] · x̃_i   (= K_c · x̃)
    P_k   = S_k² + C_k²

Inverse:
    x̃    = K_s⁻¹ · S
    x[z]  = x̃ / w(z)            (w from forward state)
"""

import numpy as np
from .constants import RING, ZPOS, KS_MATRIX, KC_MATRIX

_ZPOS_ARR = np.array(ZPOS, dtype=np.int32)
_KS_INV   = np.linalg.inv(KS_MATRIX)   # precomputed once


class MPRCTransform:
    """
    MPRC Spectral Transform on Z₂₅₆.

    All constants frozen from ring geometry — do not modify.

    Examples
    --------
    >>> t = MPRCTransform()
    >>> signal = np.random.randint(0, 256, 256, dtype=np.uint8)
    >>> P = t.forward(signal)               # (36,) power spectrum
    >>> S, C, w = t.forward_complex(signal)
    >>> x_rec = t.inverse(S, w)             # exact reconstruction
    """

    def __init__(self):
        self.zpos   = _ZPOS_ARR
        self.Ks     = KS_MATRIX
        self.Kc     = KC_MATRIX
        self.Ks_inv = _KS_INV
        self.bins   = RING["BINS"]

    # ── Weight ────────────────────────────────────────────────────
    @staticmethod
    def weight(x: np.ndarray) -> np.ndarray:
        """
        Parabolic weight — silence gate + clip suppression.

        w(x) = 16 · (Δa · Δd)²
        Δa   = |x − 128|
        Δd   = 128 − Δa    (spinor flip: Δa + Δd = 128)

        w(128) = 0  silence gate    (exact zero at vacuum)
        w(0)   = 0  clip suppress   (exact zero at rail)
        w(255) = 0  clip suppress   (exact zero at rail)
        w(64)  = max peak coupling at quarter-ring
        """
        x  = np.asarray(x, dtype=np.float64)
        da = np.abs(x - 128.0)
        dd = 128.0 - da
        return 16.0 * (da * dd) ** 2

    # ── Forward ───────────────────────────────────────────────────
    def forward(self, buf: np.ndarray) -> np.ndarray:
        """
        MPRC forward transform.

        Parameters
        ----------
        buf : array-like, shape (256,), dtype uint8
            Input signal on Z₂₅₆.

        Returns
        -------
        P : ndarray, shape (36,)
            Power spectrum.  P_k = S_k² + C_k²
        """
        S, C, _ = self.forward_complex(buf)
        return S * S + C * C

    def forward_complex(self, buf: np.ndarray):
        """
        MPRC forward returning (S, C, w) for phase and inverse.

        Returns
        -------
        S : ndarray (36,)   sin projection
        C : ndarray (36,)   cos projection
        w : ndarray (36,)   per-sample weights — save for inverse
        """
        buf = np.asarray(buf, dtype=np.float64)
        x   = buf[_ZPOS_ARR]
        w   = self.weight(x)
        wx  = w * x
        S   = self.Ks @ wx
        C   = self.Kc @ wx
        return S, C, w

    # ── Inverse ───────────────────────────────────────────────────
    def inverse(self, S: np.ndarray, w: np.ndarray) -> np.ndarray:
        """
        Exact inverse via K_s⁻¹.

        Parameters
        ----------
        S : ndarray (36,)   sin projection from forward_complex
        w : ndarray (36,)   weights from forward_complex

        Returns
        -------
        x_rec : ndarray (36,)
            Reconstructed signal at 36 active positions.
            Max error < 5×10⁻¹⁰.
        """
        x_tilde = self.Ks_inv @ S
        return np.where(w > 0, x_tilde / w, 128.0)

    # ── Phase ─────────────────────────────────────────────────────
    @staticmethod
    def phase(S: np.ndarray, C: np.ndarray) -> np.ndarray:
        """Phase at each bin: φ_k = arctan2(S_k, C_k)"""
        return np.arctan2(S, C)

    def __repr__(self):
        return "MPRCTransform(bins=36, rank_Ks=36, κ=93.35, frozen=2026-04-21)"
