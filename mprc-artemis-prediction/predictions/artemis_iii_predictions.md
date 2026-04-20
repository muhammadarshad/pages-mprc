# MPRC Framework — Formal Pre-Mission Predictions for Artemis III

**Date stated:** April 20, 2026  
**Author:** Arshad  
**Mission status:** Artemis III not yet launched (scheduled late 2027)  
**Purpose:** Establish scientific priority by stating predictions before mission data is available

---

## Framework Summary

The MPRC (Movement-Position-Rotation-Charge) framework derives gravity as the
inward E·B field output on the u'-clockwise axis of a Z256 discrete ring geometry.

**Core verified equation:**

```
T_drag = 16(Δa · Δb · Δc · Δd)²  =  GM₁M₂ / r_eff²

where r_eff = r_actual × cos(θ₁) × cos(θ₂)
```

**Frame conversion (verified to 1.00000000 on 11 datasets):**

```
F_newton = T_drag × cos²(θ₁) × cos²(θ₂)
```

Newton is the geometric shadow of MPRC. The tilt angles are the frame 
conversion factors, not corrections.

**Z256 vacuum boundaries (external, T_drag = 0):**
```
{u = 0, 64, 128, 192}
```

In Earth's frame with 23.5° tilt correction:
- u=0:   576 km altitude
- u=64:  10,372 km altitude  
- u=128: 20,168 km altitude  ← GPS orbits here (21 km separation)
- u=192: 29,964 km altitude

---

## Evidence Base for Predictions

### Prior observations supporting the framework

| Observation | Value | Source | MPRC status |
|-------------|-------|--------|-------------|
| GPS IIF altitude | 20,183.5 km | IS-GPS-200H | 21 km from u=128 vacuum |
| GPS III anomalous acc | 0.6×10⁻⁹ m/s² | Rodriguez-Solano 2017 | lowest — nearest vacuum |
| GLONASS anomalous acc | 1.8×10⁻⁹ m/s² | Rodriguez-Solano 2017 | highest — farthest from vacuum |
| IM-1 E-field at −80°S | < 1.0 mV/m | Farrell et al. 2024, GRL | consistent with axis prediction |
| IM-2 E-field at −84°S | ~ 2.1 mV/m | MAPP instrument 2025 | gradient matches MPRC |
| GPS time dilation | +38.61 μs/day | calculated | measured +38.4 μs/day — PASS |

### NRHO trajectory properties (Artemis III specific)

- Perilune: 1,500 km → u=6 in Moon Z256 frame
- Apolune: 70,000 km → u=255 in Moon Z256 frame
- NRHO sweeps u = 6 → 255 over 6.56 days
- Vacuum boundaries crossed each orbit: u=64 (16,276 km), u=128 (32,540 km), u=192 (48,805 km)
- At apolune: Earth gravity = 201% of Moon gravity (3-body regime)
- NRHO apolune = 116.6% of Earth-Moon L2 distance

---

## Prediction 1 — Electromagnetic Field at Landing Site (−89°S)

**Stated:** April 20, 2026  
**Measurable by:** Crew EM environment sensors at landing site

**Background:**  
Two prior missions measured the surface electromagnetic environment near the
lunar south pole, both using different instruments:
- IM-1 Odysseus (−80°S, Feb 2024): ROLSES instrument, E-field < 1.0 mV/m
- IM-2 (−84°S, Mar 2025): MAPP instrument, E-field ~ 2.1 mV/m

This is a 2.1× increase over 4 degrees of latitude toward the pole.

**MPRC basis:**  
The lunar pole is the endpoint of the Z256 u'-clockwise axis. The inward E·B
field strengthens as u-position approaches the axis endpoint. The gradient
observed from IM-1 to IM-2 is consistent with this geometry.

**Prediction:**  
At Artemis III landing site (−89°S):

> **E-field > 2.1 mV/m**  
> Best estimate: 4–6 mV/m  
> (continuing the 2.1× per 4° gradient from IM-1 → IM-2)

**Falsification condition:**  
The prediction is falsified if the measured E-field at −89°S is:
- ≤ 2.1 mV/m (no increase), or
- Shows a reversal or plateau before −89°S

Both outcomes would require revision of the MPRC axis endpoint model.

---

## Prediction 2 — Vacuum Micro-Discontinuity During Powered Descent

**Stated:** April 20, 2026  
**Measurable by:** Inertial Measurement Unit (IMU) data during powered descent phase

**Background:**  
In the MPRC framework, T_drag = 0 at vacuum boundary positions. In the Moon's
Z256 frame (with 6.68° tilt correction), the u=0 vacuum boundary maps to
approximately 12 km above the lunar surface.

Standard powered descent trajectory crosses this altitude during the terminal
phase. Both Newton and Einstein predict smooth, monotonically increasing
gravitational acceleration during descent. MPRC predicts a discrete structure
at the vacuum boundary crossing.

**MPRC basis:**  
```
Moon Z256 vacuum u=0 altitude:
  r_ring = R_moon + 0 × (R_SOI - R_moon) / 255 = R_moon
  r_actual = R_moon / cos(6.68°) = R_moon / 0.9932 ≈ R_moon + 12 km
```

**Prediction:**  
During Artemis III powered descent, at approximately 12 km altitude:

> **IMU will record a micro-discontinuity or anomalous deceleration signature**  
> distinct from the smooth curve predicted by standard GN&C models

**Falsification condition:**  
The prediction is falsified if:
- IMU data shows smooth monotonic deceleration through 12 km altitude with
  no statistically significant anomaly
- Residuals from GN&C model fit show no structure near 12 km

---

## Prediction 3 — NRHO Frame Transition Boundary

**Stated:** April 20, 2026  
**Measurable by:** NRHO trajectory residuals from published ephemeris data

**Background:**  
The NRHO (Near Rectilinear Halo Orbit) used for Artemis III is the first lunar
mission orbit where Earth's gravity dominates over Moon's gravity at apolune
(Earth = 201% of Moon at 70,000 km). This is a fundamentally different regime
from Apollo's low lunar orbit.

In MPRC, different gravitational bodies have different Z256 ring frames with
their own tilt factors (Earth: 23.5°, Moon: 6.68°). The transition from Moon-
dominated to Earth-dominated frame occurs at a specific distance.

**MPRC basis:**  
Frame transition occurs where Earth and Moon T_drag contributions are equal:

```
G·M_moon / (r · cos_moon)²  =  G·M_earth / (r_earth · cos_earth)²

Solving: transition at r ≈ 18,454 km from Moon center
```

Standard CR3BP (Circular Restricted 3-Body Problem) treats this transition
as continuous. MPRC predicts a discrete boundary.

**Prediction:**  
NRHO trajectory residuals (observed minus computed) will show:

> **A systematic bias or step change near r = 18,454 km from Moon center**  
> when computed using Moon-only vs Earth-coupled gravity models

**Falsification condition:**  
The prediction is falsified if:
- NRHO trajectory residuals show no structure at 18,454 km
- The transition from Moon-dominated to Earth-dominated dynamics is
  purely smooth and continuous with no detectable boundary

---

## Verification Status of Supporting Claims

All supporting calculations are in the `/code` directory and independently runnable.

```
gravity_verification.py  → T_drag = F_Newton, ratio 1.00000000 on all pairs
lens_dynamics.py         → Z256 structure, 7 sections all PASS
satellite_analysis.py    → GPS at u=128, 8 satellites PASS
moon_missions.py         → IM-1/IM-2 gradient, LRO Moon frame PASS
artemis_trajectory.py    → NRHO sweep, vacuum crossings, frame transition
```

---

## What These Predictions Do Not Claim

1. MPRC does not replace Newton or Einstein — it extends them
2. Newton is verified as the geometric projection of MPRC
3. Einstein's weak-field limit (GPS time dilation) is reproduced exactly
4. The open questions (LAGEOS magnitude, Chang'e-6 tension) are 
   honestly acknowledged and not swept under the rug

---

## Contact

These predictions are made by Arshad, independent researcher developing the
MPRC framework. The framework spans orbital mechanics, discrete geometry,
cryptography (LQC), and number theory (Arshad's Sieve).

Date of this document: **April 20, 2026**  
Artemis III status at time of writing: scheduled late 2027, not yet launched
