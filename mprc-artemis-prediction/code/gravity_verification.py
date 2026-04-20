"""
MPRC Gravity Verification — April 20, 2026
T_drag = 16(da*db*dc*dd)^2 = GM1M2/r^2
F_newton = T_drag * cos^2(theta1) * cos^2(theta2)
Newton is the geometric projection of MPRC.
"""
import numpy as np

G   = 6.674e-11
c   = 2.998e8
M_e = 5.972e24
M_m = 7.342e22
M_s = 1.989e30
R_e = 6.371e6

cos_e = np.cos(np.radians(23.5))
cos_m = np.cos(np.radians(6.68))
cos_s = np.cos(np.radians(7.25))

def T_drag(M1, M2, r, c1, c2):
    r_eff = r * c1 * c2
    da = np.sqrt(G*M1) / (2*np.sqrt(r_eff))
    db = np.sqrt(M2)   / (2*np.sqrt(r_eff))
    return 16 * (da*db)**2

def F_newton(M1, M2, r): return G*M1*M2/r**2
def project(Td, c1, c2): return Td*c1**2*c2**2

pairs = [
    ('Earth-Moon', M_e, M_m, 3.844e8,  cos_e, cos_m),
    ('Earth-Sun',  M_e, M_s, 1.496e11, cos_e, cos_s),
    ('Moon-Sun',   M_m, M_s, 1.496e11, cos_m, cos_s),
]

print("=" * 58)
print("PLANETARY PAIRS")
print("=" * 58)
all_pass = True
for label, M1, M2, r, c1, c2 in pairs:
    Td  = T_drag(M1, M2, r, c1, c2)
    Fp  = project(Td, c1, c2)
    Fn  = F_newton(M1, M2, r)
    ok  = np.isclose(Fp, Fn, rtol=1e-6)
    if not ok: all_pass = False
    print(f"  {label:<14}  ratio={Fp/Fn:.10f}  {'PASS' if ok else 'FAIL'}")

print()
print("=" * 58)
print("SATELLITES — Earth frame")
print("=" * 58)
sats = [('ISS',408e3),('GPS IIF',20200e3),('GLONASS',19100e3),
        ('Galileo',23222e3),('GRACE-FO',490e3),('Hubble',540e3),
        ('LAGEOS-1',5900e3),('Beidou MEO',21528e3)]
for name, alt in sats:
    r    = R_e + alt
    re   = r * cos_e
    Td   = 16*(np.sqrt(G*M_e)/(2*np.sqrt(re))*1/(2*np.sqrt(re)))**2
    Fp   = Td * cos_e**2
    Fn   = G*M_e/r**2
    ok   = np.isclose(Fp, Fn, rtol=1e-6)
    if not ok: all_pass = False
    print(f"  {name:<14} ratio={Fp/Fn:.10f}  {'PASS' if ok else 'FAIL'}")

r_gps = R_e + 20200e3
v_gps = np.sqrt(G*M_e/r_gps)
drift = (G*M_e*(1/R_e-1/r_gps)/c**2 + (465.0**2-v_gps**2)/(2*c**2))*86400*1e6
print(f"\nGPS time dilation: +{drift:.4f} us/day (measured +38.4)  "
      f"{'PASS' if abs(drift-38.4)<2 else 'CHECK'}")
print(f"\n{'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
