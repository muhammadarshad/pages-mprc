"""
MPRC Spectral Transform
=======================
A signal-adapted geometric projection on Z₂₅₆.

Frozen: 2026-04-21
Author: Arshad — MPRC Framework
Status: LOCKED

Quick start:
    from mprc import MPRCTransform
    t = MPRCTransform()
    P = t.forward(signal)          # power spectrum, 36 bins
    S, C, w = t.forward_complex(signal)
    x = t.inverse(S, w)            # exact reconstruction
"""

from .transform import MPRCTransform
from .constants import RING, ZPOS, KS_MATRIX, KC_MATRIX
from .verify import run_all

__version__ = "1.0.0"
__author__  = "Arshad — MPRC Framework"
__date__    = "2026-04-21"
__status__  = "LOCKED"

__all__ = ["MPRCTransform", "RING", "ZPOS", "KS_MATRIX", "KC_MATRIX", "run_all"]
