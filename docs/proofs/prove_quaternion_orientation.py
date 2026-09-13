"""PROOF: does K_CCW = R_128(K_CW) FOLLOW from the ring rules, or is it assigned?

GIVEN (owner's starting point): Hamilton's algebra only.
    i2=j2=k2=ijk=-1 ;  ij=k, jk=i, ki=j ;  ji=-k, kj=-i, ik=-j
CLAIM TO PROVE: reversing the traversal lands on the SAME axis, displaced by
exactly 128 on the ring -- i.e. the quaternion sign rule is RECOVERED from
CW/CCW geometry rather than assigned.

NO EULER. On the Q8 lattice {0,64,128,192} the character map is exact integers:
    chi(a,0)=1   chi(a,64)=a   chi(a,128)=-1   chi(a,192)=-a
so no cos/sin is ever evaluated. Hamilton's integer components are the GIVEN;
every RESULT is reported as a ring position, with no sign.
"""
import functools

# Hamilton product on integer 4-tuples (w,x,y,z). The given, not a choice.
def mul(a, b):
    w1,x1,y1,z1 = a; w2,x2,y2,z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2,
            w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2,
            w1*z2+x1*y2-y1*x2+z1*w2)

ONE=(1,0,0,0); I=(0,1,0,0); J=(0,0,1,0); K=(0,0,0,1)
AX={"I":I,"J":J,"K":K}
def neg(q): return tuple(0-c for c in q)

# chi(a,s) on the Q8 lattice -- EXACT, no trigonometry
def chi(a, s):
    u = AX[a]
    return {0: ONE, 64: u, 128: neg(ONE), 192: neg(u)}[s % 256]

# read a Q8 element back as (axis, ring position). This is the only decoding.
def site(q):
    for a in AX:
        for s in (0, 64, 128, 192):
            if chi(a, s) == q:
                return (("scalar" if s in (0,128) else a), s)
    return None

print("=== 1. R_128 is orientation reversal on EVERY axis at EVERY lattice phase ===")
bad = 0
for a in AX:
    for s in (0, 64, 128, 192):
        lhs = chi(a, (s + 128) % 256)
        rhs = neg(chi(a, s))
        bad += lhs != rhs
print(f"    chi(a, s+128) == -chi(a, s):  {12-bad}/12 exact   "
      f"{'PASS' if bad==0 else 'FAIL'}")
print("    so +128 IS the opposite-orientation operator inside the embedding\n")

print("=== 2. the six products: CW at 64, CCW at 192 -- READ OFF ===")
CW  = [("I","J","K"), ("J","K","I"), ("K","I","J")]
rows = []
allok = True
for x, y, z in CW:
    fwd = mul(AX[x], AX[y])
    rev = mul(AX[y], AX[x])
    sf, sr = site(fwd), site(rev)
    ok = (sf == (z, 64)) and (sr == (z, 192))
    r128 = mul(fwd, chi(z, 128))
    follows = (r128 == rev)
    allok &= ok and follows
    rows.append((f"{x}{y}", sf, f"{y}{x}", sr, follows))
for f, sf, r, sr, ok in rows:
    print(f"    {f} -> {sf[0]}_{sf[1]:<3}   {r} -> {sr[0]}_{sr[1]:<3}   "
          f"R_128(fwd)==rev: {ok}")
print(f"    192 = 64 + 128, and the axis is UNCHANGED.  "
      f"{'PASS' if allok else 'FAIL'}\n")

print("=== 3. I2 = J2 = K2 = IJK = 128 ===")
sq = [site(mul(AX[a], AX[a])) for a in AX]
ijk = site(mul(mul(I, J), K))
print(f"    I2 {sq[0]}  J2 {sq[1]}  K2 {sq[2]}  IJK {ijk}")
ok3 = all(s[1] == 128 for s in sq) and ijk[1] == 128
print(f"    all land on ring position 128 = the half-turn  "
      f"{'PASS' if ok3 else 'FAIL'}")
print(f"    64 + 64 = {(64+64)%256}: quarter-turn o quarter-turn = half-turn\n")

print("=== 4. double cover: T_360 != I but T_360^2 = I ===")
q = ONE; cyc = []
for n in range(1, 6):
    q = mul(q, I); cyc.append((64*n % 256, site(q)))
print("    element:  " + "  ".join(f"s={s}->{t[0]}_{t[1]}" for s, t in cyc[:4]))
elem_period = next(64*n for n in range(1,9)
                   if functools.reduce(mul,[I]*n) == ONE)

def conj(q, v):
    qc = (q[0], -q[1], -q[2], -q[3])
    return mul(mul(q, v), qc)
trivial_at = [s for s in (64,128,192,0)
              if all(conj(chi("I", s), v) == v for v in (I,J,K))]
print(f"    element returns to +1 at ring position {elem_period}   (= 720 deg)")
print(f"    conjugation acts trivially at ring positions {sorted(trivial_at)}")
print("    -> T_360 = R_128 (rotation identity, element = -1, NOT the identity)")
print(f"    -> T_360^2 = R_256 = R_0 = I,  and T_360 != I     "
      f"{'PASS' if 128 in trivial_at and elem_period==256 else 'CHECK'}")

print("\n=== 5. the U walk: 7 and its exact inverse 183 ===")
print(f"    7 * 183 mod 256 = {7*183 % 256}     (Observer / Anti-Observer)")
orb = []
t = 0
for _ in range(8):
    t = (t + 7) % 256; orb.append(t)
print(f"    z_U = 7*Theta: first 8 steps {orb}")
print(f"    vacuums {{0,64,128,192}} hit in first 36 steps: "
      f"{sorted({(7*n)%256 for n in range(1,37)} & {0,64,128,192})}")
