"""
MPRC Artemis III Trajectory Analysis — April 20, 2026
NRHO vacuum boundary crossings, frame transition, predictions.
"""
import numpy as np

G   = 6.674e-11
M_e = 5.972e24
M_m = 7.342e22
M_s = 1.989e30
R_m = 1.737e6
R_e = 6.371e6
cos_e = np.cos(np.radians(23.5))
cos_m = np.cos(np.radians(6.68))
R_SOI_moon = 66100e3

def moon_r_to_u(r):
    frac = np.clip((r*cos_m - R_m)/(R_SOI_moon - R_m), 0, 1)
    return int(round(frac*255))

def vac_alt_moon(u_vac):
    frac   = u_vac/255
    r_ring = R_m + frac*(R_SOI_moon - R_m)
    return r_ring/cos_m - R_m

# NRHO parameters (NASA published, Williams et al. 2019)
nrho_peri = 1500e3
nrho_apo  = 70000e3
r_peri    = R_m + nrho_peri
r_apo     = R_m + nrho_apo
u_peri    = moon_r_to_u(r_peri)
u_apo     = moon_r_to_u(r_apo)

print("=" * 62)
print("ARTEMIS III NRHO — MPRC Z256 MAPPING")
print("=" * 62)
print(f"\n  Perilune: {nrho_peri/1e3:.0f} km  ->  u={u_peri}")
print(f"  Apolune : {nrho_apo/1e3:.0f} km  ->  u={u_apo}")
print(f"  Z256 sweep: {u_apo - u_peri} u-steps per 6.56-day orbit")

print(f"\n  Vacuum boundaries crossed each orbit:")
for u_v in [64, 128, 192]:
    alt = vac_alt_moon(u_v)
    if r_peri <= R_m + alt <= r_apo:
        print(f"    u={u_v}: {alt/1e3:.1f} km  YES")
    else:
        print(f"    u={u_v}: {alt/1e3:.1f} km  no")

# 3-body regime at apolune
r_moon_earth = 3.844e8
g_moon_apo   = G*M_m/r_apo**2
g_earth_apo  = G*M_e/(r_moon_earth + r_apo)**2
print(f"\n  At apolune:")
print(f"    Moon gravity : {g_moon_apo:.4e} m/s^2")
print(f"    Earth gravity: {g_earth_apo:.4e} m/s^2")
print(f"    Earth/Moon   : {g_earth_apo/g_moon_apo:.2f}x  <- 3-body regime")

# Frame transition
r_L2 = r_moon_earth * (M_m/(3*M_e))**(1/3)
transition_r = r_L2 * 0.3
print(f"\n  L2 distance from Moon: {r_L2/1e3:.1f} km")
print(f"  Frame transition at  : {transition_r/1e3:.1f} km (MPRC prediction)")

print(f"\n{'=' * 62}")
print("THREE FORMAL PREDICTIONS — April 20, 2026")
print(f"{'=' * 62}")
print(f"""
  P1 — E-field at landing site (-89 deg S):
       IM-1 at -80 deg S: < 1.0 mV/m  (Farrell et al. 2024)
       IM-2 at -84 deg S: ~ 2.1 mV/m  (MAPP 2025)
       PREDICTED at -89 deg S: > 2.1 mV/m (est. 4-6 mV/m)
       FALSIFIED if: E-field <= 2.1 mV/m

  P2 — Vacuum discontinuity during powered descent:
       Moon Z256 u=0 vacuum altitude: {vac_alt_moon(0)/1e3:.1f} km
       PREDICTED: IMU anomaly at ~{vac_alt_moon(0)/1e3:.0f} km altitude
       FALSIFIED if: smooth IMU deceleration through that altitude

  P3 — NRHO frame transition boundary:
       PREDICTED: residual shift at ~{transition_r/1e3:.0f} km from Moon
       FALSIFIED if: NRHO residuals show no structure there
""")
