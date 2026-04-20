# Verified Results — April 20, 2026

## Planetary Pairs (gravity_verification.py)

| Pair | Ratio | Status |
|------|-------|--------|
| Earth-Moon | 1.0000000000 | PASS |
| Earth-Sun | 1.0000000000 | PASS |
| Moon-Sun | 1.0000000000 | PASS |

## Satellites (gravity_verification.py)

All 8 satellites: ratio = 1.0000000000 PASS

GPS time dilation: +38.6127 μs/day vs measured +38.4 PASS

## Z256 Lens Structure (lens_dynamics.py)

All 7 sections PASS:
- 126 + 126 + 4 = 256 (structural)
- v/c in (0,1) for 1.0 MeV/c electron
- Full/half cycle ratio = 2.0
- 4D unit circle holds at all steps
- Charge flips with rotation direction
- Vacuum neutrality verified
- z3 = z4·|sinθ| across full 126-step cycle

## Key Numbers

- GPS IIF separation from u=128 vacuum: 21 km
- GLONASS anomalous acc: 1.8e-9 m/s² (1031 km from vac128)
- GPS III anomalous acc: 0.6e-9 m/s² (21 km from vac128)
- NRHO Z256 sweep: u=6 → u=255 per 6.56-day orbit
- Earth gravity at NRHO apolune: 201% of Moon gravity
- Moon distance April 20 2026: 358,507.8 km (live ephemeris)
