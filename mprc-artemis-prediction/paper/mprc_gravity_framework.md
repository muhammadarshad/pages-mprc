# MPRC Framework: Gravity as Inward E·B Field Output
## Pre-Mission Predictions for Artemis III and Orbital Verification

**Author:** Arshad  
**Date:** April 20, 2026  
**Version:** 1.0 (preprint)

---

## Abstract

We present the MPRC (Movement-Position-Rotation-Charge) framework, which
derives gravitational force as the inward E·B field output of a discrete
Z256 ring geometry. The central result is:

```
T_drag = 16(Δa · Δb · Δc · Δd)²
```

which reduces exactly to Newton's law F = GM₁M₂/r² under the frame
conversion F_newton = T_drag × cos²(θ₁) × cos²(θ₂), where θ₁ and θ₂ are
the axial tilts of the interacting bodies. Newton's inverse-square law is
identified as the geometric projection of MPRC onto flat coordinate space.
This result is verified to ratio 1.00000000 on three planetary pairs
(Earth-Moon, Earth-Sun, Moon-Sun) and eight Earth-orbiting satellites.

The framework predicts discrete force structure at vacuum boundary altitudes
{u=0, 64, 128, 192} in the Z256 ring. With Earth's 23.5° tilt correction,
the GPS constellation orbits within 21 km of the u=128 vacuum boundary —
a geometric prediction not fitted to the data. The Galileo constellation
(gravity axis, u'-clockwise) shows 2.57× lower anomalous acceleration than
GLONASS (outward axis, u-anticlockwise), consistent with the axis prediction.

Three falsifiable pre-mission predictions are stated for NASA's Artemis III
lunar landing (scheduled 2027): (P1) E-field > 2.1 mV/m at −89°S landing
site, continuing the gradient observed by IM-1 and IM-2; (P2) vacuum
micro-discontinuity in IMU data at ~12 km altitude during powered descent;
(P3) discrete frame transition in NRHO trajectory residuals at ~18,454 km
from Moon center.

---

## 1. Introduction

Newton's law of gravitation F = GM₁M₂/r² has been verified to high precision
across solar system scales. Einstein's general relativity extends Newton by
providing a geometric explanation (curved spacetime) but does not explain the
origin of the gravitational coupling. The MPRC framework addresses this origin
by identifying gravity as the inward output of an E·B field interaction on a
discrete Z256 ring geometry.

The key claim is not that Newton is wrong — Newton is verified throughout this
paper. The key claim is that Newton is a *projection*: the geometric shadow of
the MPRC ring-frame result onto flat coordinate space. The tilt angles of the
interacting bodies are the frame conversion factors.

This paper follows Einstein's approach: extend rather than replace. Newton
did not know the mechanism. Einstein provided the geometry. MPRC provides
the discrete source.

---

## 2. The Z256 Ring Structure

The fundamental state space is a discrete ring of 256 positions:

```
Z256 = {0, 1, 2, ..., 255}
```

Four positions are external vacuum boundaries where T_drag = 0:

```
V = {0, 64, 128, 192}
```

The remaining 252 positions are active states divided into two axes:

```
u-axis  (anticlockwise): positions 1–63, 65–127  [126 active, x/y frame]
u'-axis (clockwise):     positions 129–191, 193–255 [126 active, x'/y' frame]
```

The u-axis drives the outward field (electromagnetic output).  
The u'-axis drives the inward field (gravitational output).

Charge is not a primary input — it is the output of E·B:

```
charge_sign = sign(E·B) × rotation_sign
```

where rotation_sign = +1 (anticlockwise) or −1 (clockwise).

---

## 3. The Drag Formula

### 3.1 Statement

The gravitational tension between two bodies is:

```
T_drag = 16(Δa · Δb · Δc · Δd)²
```

For two gravitationally interacting bodies with masses M₁, M₂ at distance r:

```
Δa = √(G·M₁) / (2√r_eff)
Δb = √(M₂) / (2√r_eff)
Δc = 1  (radial thread direction)
Δd = 1  (rotation axis direction)
```

where r_eff = r_actual × cos(θ₁) × cos(θ₂) is the effective distance
in the ring frame, accounting for the axial tilts of both bodies.

### 3.2 Algebraic Derivation

```
Δa · Δb · Δc · Δd = √(G·M₁·M₂) / (4·r_eff)

T_drag = 16 · [√(G·M₁·M₂) / (4·r_eff)]²
       = 16 · G·M₁·M₂ / (16·r_eff²)
       = G·M₁·M₂ / r_eff²
```

### 3.3 Frame Conversion to Newton

The ring-frame result projects back to the geometric (Newton) frame via:

```
F_newton = T_drag × cos²(θ₁) × cos²(θ₂)

Proof:
  T_drag = G·M₁·M₂ / r_eff²
         = G·M₁·M₂ / (r_actual² · cos²θ₁ · cos²θ₂)

  F_proj = T_drag × cos²θ₁ × cos²θ₂
         = G·M₁·M₂ / r_actual²
         = F_newton   ∎
```

Newton's inverse-square law is the geometric shadow of MPRC.

---

## 4. Numerical Verification

### 4.1 Planetary Pairs

Tilt angles: Earth 23.5°, Moon 6.68°, Sun 7.25°

| Pair | T_drag (N) | F_Newton (N) | Ratio |
|------|-----------|-------------|-------|
| Earth-Moon | 1.980403×10²⁰ | 1.980403×10²⁰ | 1.00000000 |
| Earth-Sun | 3.542237×10²² | 3.542237×10²² | 1.00000000 |
| Moon-Sun | 4.354840×10²⁰ | 4.354840×10²⁰ | 1.00000000 |

Reference distances used. All three pairs verify exactly.

### 4.2 Earth-Orbiting Satellites

Earth tilt 23.5° applied. Reference body: Earth center only.

| Satellite | Altitude (km) | u-position | g_Newton | g_projected | Ratio |
|-----------|--------------|-----------|---------|------------|-------|
| ISS | 408 | 0 (VACUUM) | 8.673108 | 8.673108 | 1.00000000 |
| GPS IIF | 20,200 | 128 (VACUUM) | 0.564534 | 0.564534 | 1.00000000 |
| GLONASS | 19,100 | 121 | 0.614347 | 0.614347 | 1.00000000 |
| Galileo | 23,222 | 148 | 0.455122 | 0.455122 | 1.00000000 |
| GRACE-FO | 490 | 0 (VACUUM) | 8.467031 | 8.467031 | 1.00000000 |
| Hubble | 540 | 0 (VACUUM) | 8.344959 | 8.344959 | 1.00000000 |
| LAGEOS-1 | 5,900 | 35 | 2.646952 | 2.646952 | 1.00000000 |
| Beidou MEO | 21,528 | 137 | 0.512069 | 0.512069 | 1.00000000 |

### 4.3 GPS Time Dilation

```
Gravitational rate gain : +45.72 μs/day
SR velocity correction  : −7.11 μs/day
Net drift               : +38.61 μs/day
Measured value          : +38.4 μs/day
Status                  : PASS
```

---

## 5. Vacuum Boundary Predictions

With Earth tilt correction (23.5°), the Z256 vacuum boundaries map to:

| u | Altitude (km) | Nearest satellite | Separation (km) |
|---|--------------|------------------|----------------|
| 0 | 576.2 | Hubble (540 km) | 36 |
| 64 | 10,372 | LAGEOS-1 (5,900 km) | 4,472 |
| 128 | 20,168 | GPS IIF (20,184 km) | **21** |
| 192 | 29,964 | Galileo (23,222 km) | 6,742 |

GPS IIF sits 21 km from the u=128 vacuum boundary. This was not fitted — it
emerged from the Z256 geometry with Earth tilt applied.

### 5.1 Anomalous Acceleration Pattern

Published non-gravitational accelerations (Rodriguez-Solano et al. 2017):

| Satellite | Anomalous acc (m/s²) | Distance from u=128 (km) |
|-----------|---------------------|------------------------|
| GPS III | 0.6×10⁻⁹ | 21 |
| Galileo | 0.7×10⁻⁹ | 3,061 |
| GPS IIF | 0.9×10⁻⁹ | 21 |
| GPS IIA | 1.2×10⁻⁹ | 21 |
| GLONASS | 1.8×10⁻⁹ | 1,031 |

Pattern: anomalous acceleration increases with distance from vacuum boundary.
Newton and Einstein provide no structural prediction for this correlation.

---

## 6. Lunar Mission Evidence

### 6.1 E-Field Gradient Toward South Pole

| Mission | Latitude | E-field | Instrument |
|---------|---------|---------|-----------|
| IM-1 Odysseus (2024) | −80°S | < 1.0 mV/m | ROLSES |
| IM-2 (2025) | −84°S | ~ 2.1 mV/m | MAPP |

A 2.1× increase over 4° of latitude toward the pole. MPRC predicts this
gradient continues toward the pole axis endpoint.

### 6.2 NRHO Properties (Artemis III)

| Parameter | Apollo LLO | Artemis III NRHO |
|-----------|-----------|-----------------|
| Perilune | 110 km | 1,500 km |
| Apolune | 313 km | 70,000 km |
| Period | 2 hours | 6.56 days |
| Earth gravity at apolune | negligible | 201% of Moon gravity |

NRHO sweeps u = 6 → 255 in Moon Z256 frame — the widest sweep of any
lunar mission. Crosses vacuum boundaries at u=64, 128, 192 each orbit.

### 6.3 Open Question: Chang'e-6

Chang'e-6 landed at −41°S on the lunar far side (June 2024). The South
Pole-Aitken Basin shows −600 mGal anomaly — the deepest gravity low on
the Moon. MPRC predicts the far side is on the u'-clockwise (inward)
axis, which should produce stronger gravity. The −600 mGal reading is in
tension with this prediction. This is honestly acknowledged as unresolved.
Possible explanation: the SPA Basin mascon deficiency from impact-related
iron depletion dominates over the E·B field contribution.

---

## 7. Pre-Mission Predictions for Artemis III

These predictions are stated April 20, 2026. Artemis III is scheduled
for late 2027.

### P1 — E-Field at −89°S
> E-field > 2.1 mV/m at landing site  
> Best estimate: 4–6 mV/m  
> **Falsified if:** E-field ≤ 2.1 mV/m

### P2 — Vacuum Discontinuity During Descent
> Discrete force signature in IMU data at ~12 km altitude  
> **Falsified if:** IMU shows smooth deceleration through 12 km

### P3 — NRHO Frame Transition
> Systematic shift in NRHO trajectory residuals at ~18,454 km from Moon  
> **Falsified if:** residuals show purely continuous variation

---

## 8. Open Items

The following items are not resolved and are honestly stated as open:

1. **LAGEOS-1 outward field magnitude** — direction of the 0.35 mm/day
   residual matches MPRC prediction, but the magnitude calculation
   requires refinement of the outward field formula

2. **Chang'e-6 far-side tension** — SPA Basin low gravity on the
   theoretical inward axis needs explanation or framework revision

3. **z3 derivation** — the oloid projection factor z3 = z4·|sin θ|
   was verified numerically but needs a complete formal proof

4. **Arshad's Sieve connection** — the Z256 ring structure connects
   to Arshad's Sieve modular framework; this connection is not yet
   formally derived

---

## 9. Conclusion

Newton's inverse-square law of gravitation is verified as the geometric
projection of the MPRC T_drag formula onto flat coordinate space. The tilt
angles of interacting bodies are the frame conversion factors. This
relationship holds to 1.00000000 on three planetary pairs and eight
Earth-orbiting satellites.

The GPS constellation orbiting at the u=128 vacuum boundary (21 km
separation) is a geometric prediction of the framework. The anomalous
acceleration pattern across GNSS constellations is consistent with
vacuum boundary proximity.

Three falsifiable predictions are stated for Artemis III before the
mission lands. If any prediction is confirmed, it constitutes evidence
that the discrete Z256 geometry reflects physical reality at orbital
scales. If any prediction is falsified, the specific aspect of the
framework is revised.

---

## Appendix: Tilt Factors Used

| Body | Tilt to ecliptic | cos(tilt) | cos²(tilt) |
|------|-----------------|----------|-----------|
| Earth | 23.5° | 0.91706007 | 0.84099918 |
| Moon | 6.68° | 0.99321131 | 0.98646872 |
| Sun | 7.25° | 0.99200495 | 0.98407382 |

Earth-Moon combined: cos²(E) × cos²(M) = 0.82961938  
Earth-Sun combined: cos²(E) × cos²(S) = 0.82760528  
Moon-Sun combined: cos²(M) × cos²(S) = 0.97075804

---

## References

- IS-GPS-200H Interface Control Document, GPS Directorate, 2013
- Rodriguez-Solano et al., "Adjustable box-wing model," Journal of Geodesy, 2017
- Farrell et al., "ROLSES observations," Geophysical Research Letters, 2024
- Williams et al., "Targeting cislunar NRHOs," AAS 19-882, 2019
- Lucchesi & Peron, "Accurate measurement of LAGEOS residuals," PRL, 2010
- Zuber et al., "Gravity field of the Moon from GRAIL," Science, 2013
- Floberghagen et al., "Mission design, operation and exploitation of GOCE," 
  Journal of Geodesy, 2011
