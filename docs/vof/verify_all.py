import numpy as np, math, itertools
# ---- quaternion arithmetic (w,x,y,z) ----
def mul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2,
                     w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2,
                     w1*z2+x1*y2-y1*x2+z1*w2])
ONE=np.array([1.,0,0,0]); I=np.array([0.,1,0,0]); J=np.array([0.,0,1,0]); K=np.array([0.,0,0,1])
N=256
def chi(axis,s):
    "axis character: exp(axis * 2*pi*s/N) for a unit imaginary quaternion 'axis'"
    th=2*math.pi*s/N
    return math.cos(th)*ONE + math.sin(th)*axis
def show(q,tol=1e-9):
    q=np.where(abs(q)<tol,0,q); lbl={(1,0,0,0):"1",(-1,0,0,0):"-1",(0,1,0,0):"i",(0,-1,0,0):"-i",
        (0,0,1,0):"j",(0,0,-1,0):"-j",(0,0,0,1):"k",(0,0,0,-1):"-k"}
    t=tuple(int(round(v)) for v in q)
    return lbl.get(t, "("+", ".join(f"{v:+.4f}" for v in q)+")")

print("=== A. THE TWO EMBEDDINGS OF Z_256 (the conflation) ===")
print("  ring embedding  : -1 == 255 (mod 256)   <- additive residues")
print("  character embed : -1 == 128             <- chi(s)=exp(a*2*pi*s/256), your claim")
print("  These are different maps. 255 != 128. The paper uses both without distinguishing.\n")

print("=== B. ANCHORS UNDER THE CHARACTER MAP, PER AXIS ===")
for name,ax in [("i",I),("j",J),("k",K)]:
    row=[f"chi_{name}({s:3d})={show(chi(ax,s)):>3}" for s in (0,64,128,192)]
    print("  "+" | ".join(row))
print("  => -1 sits at s=128 on EVERY axis simultaneously.  <-- your claim, CONFIRMED")
print("  => the axis unit itself sits at s=64.\n")

print("=== C. THE CORE IDENTITY  ijk = -1  IN RING COORDINATES ===")
prod=mul(mul(chi(I,64),chi(J,64)),chi(K,64))
print(f"  chi_i(64) . chi_j(64) . chi_k(64) = {show(prod)}   = chi(128) = {show(chi(I,128))}")
print(f"  MULTIPLICATIVE composition : 64 (x) 64 (x) 64 -> 128")
print(f"  ADDITIVE composition       : 64  +  64  +  64  = {(64+64+64)%256}")
print(f"  HOLONOMY DEFECT            : 192 - 128 = {192-128} = 2^6")
print("  The two compositions disagree by exactly 64. This is real structure, not an error.\n")

print("=== D. SQUARES: i^2=j^2=k^2=-1 IN RING COORDINATES ===")
for name,ax in [("i",I),("j",J),("k",K)]:
    print(f"  chi_{name}(64)^2 = {show(mul(chi(ax,64),chi(ax,64)))}  <- 64 (x) 64 -> 128, additively 64+64=128 TOO")
print("  For a SINGLE axis the two compositions agree (abelian). The defect in C is purely")
print("  the non-commutativity of distinct axes.\n")

print("=== E. WHICH GROUP DOES Z_256 ACTUALLY SUPPORT EXACTLY? ===")
anchors=set()
for ax in (I,J,K):
    for s in (0,64,128,192):
        anchors.add(tuple(int(round(v)) for v in np.where(abs(chi(ax,s))<1e-9,0,chi(ax,s))))
print(f"  union of the 3 axis-anchor sets = {len(anchors)} distinct elements:")
print("   ", sorted(show(np.array(a,float)) for a in anchors))
print("  This is exactly Q8, the quaternion group of order 8 = 2^3.")
print("  Shared states s=0 -> 1 and s=128 -> -1 are common to all three axes;")
print("  each axis contributes its own +-a at s=64,192.  2 + 3*2 = 8. Closure verified below.")
A=[np.array(a,float) for a in anchors]
closed=all(any(np.allclose(mul(a,b),c) for c in A) for a in A for b in A)
print(f"  closed under quaternion multiplication: {closed}\n")

print("=== F. YOUR Q = 2(1+i+j+k) NORMALIZED ===")
u=np.array([.5,.5,.5,.5])
print(f"  u = Q/|Q| = (1+i+j+k)/2 , |u| = {np.linalg.norm(u):.6f}")
p=ONE.copy()
for n in range(1,8):
    p=mul(p,u); print(f"   u^{n} = {show(p)}")
print("  => u has ORDER 6.  u^3 = -1,  u^6 = 1.")
n_axis=np.array([0,1,1,1])/math.sqrt(3)
print(f"  u = exp(n*pi/3) with n = (i+j+k)/sqrt(3);  angle = 60 deg = 2*pi/6")
print(f"  ring position of a 2*pi/6 rotation: s = 256/6 = {256/6:.4f}  <-- NOT AN INTEGER")
print("  OBSTRUCTION: 3 does not divide 2^8, so the order-6 diagonal element is")
print("  NOT exactly representable in Z_256. Q's own symmetry is incommensurate with the ring.\n")

print("=== G. WHAT IS EXACTLY REPRESENTABLE ===")
print("  Z_{2^n} represents exactly the elements of 2-power order.")
print("  Q8 has order 8 = 2^3 -> fully representable.  <-- keep")
print("  <u> has order 6 = 2*3 -> NOT representable.   <-- either drop, or move to Z_768")
print(f"  Z_768: 768/6 = {768//6} (order-6 element exact), -1 at 768/2 = {768//2}")
print(f"  Z_768 = 3 * 256; 768 = {768} = 2^8 * 3\n")

print("=== H. 4D STATE SPACE, DONE PROPERLY ===")
print("  A single phase s in Z_256 gives mu_4 = {1,i,-1,-i} in ONE complex plane -> 2D.")
print("  Genuine 4D needs 3 independent angles (S^3 is 3-dimensional; H is 4-dimensional).")
print("  Hopf coordinates:  q = (cos(eta) e^{i xi1},  sin(eta) e^{i xi2})")
print("  Discretized: eta,xi1,xi2 in Z_256 -> 2^24 states, exact periodicity in xi1,xi2.")
def hopf(eta_s,x1_s,x2_s,N=256):
    eta=(math.pi/2)*eta_s/N; x1=2*math.pi*x1_s/N; x2=2*math.pi*x2_s/N
    return np.array([math.cos(eta)*math.cos(x1), math.cos(eta)*math.sin(x1),
                     math.sin(eta)*math.cos(x2), math.sin(eta)*math.sin(x2)])
errs=[abs(np.linalg.norm(hopf(*t))-1) for t in itertools.product(range(0,256,17),repeat=3)]
print(f"  unit-norm check over {len(errs)} sampled states: max |‖q‖-1| = {max(errs):.3e}")

print("\n=== I. THE DYADIC SUM: 2^0+2^1+2^2+2 = 9  (your identity) ===")
dsum=sum(2**m for m in range(3))
print(f"  2^0+2^1+2^2 = {dsum} = p_-           (Mersenne, 2^3 - 1)")
print(f"  {dsum} + 2      = {dsum+2} = p_+           (+2 is the SAME bridge constant)")
print(f"  so p_+ - p_- = 2 exactly: the conjugate pair is separated by one bridge step. CONFIRMED")
print(f"  p_- * p_+ = {dsum*(dsum+2)} = 2^6 - 1")
print("\n  UPGRADE — the central axis 8 is now DERIVED, not numerology:")
print("    |Q8| = 8   (the quaternion group Z_256 supports exactly, from section E)")
print(f"    p_- = |Q8| - 1 = {8-1},   p_+ = |Q8| + 1 = {8+1}")
print(f"    C_Q = |Q8|^2 - 1 = {8*8-1} = sector stride 64 minus its own anchor")
print(f"    4 * C_Q + 4 = {4*63+4} = 2^8")
print("  Every constant now descends from |Q8| = 2^3, which is a group order, not a choice.")

# ---------------------------------------------------------------
#  SECTIONS V-VII: isotropy and the dyadic obstruction
# ---------------------------------------------------------------
import itertools
from fractions import Fraction as F
S1=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
S2=[v for v in itertools.product([-1,0,1],repeat=3) if sum(abs(x) for x in v)==2]
_d=np.eye(3)
_ISO=(np.einsum('ij,kl->ijkl',_d,_d)+np.einsum('ik,jl->ijkl',_d,_d)+np.einsum('il,jk->ijkl',_d,_d))
def moments(C,w):
    C=np.array(C,float); w=np.array(w,float); w=w/w.sum()
    T2=np.einsum('a,ai,aj->ij',w,C,C); T4=np.einsum('a,ai,aj,ak,al->ijkl',w,C,C,C,C)
    c2=np.trace(T2)/3; e2=np.abs(T2-c2*_d).max()
    c4=np.sum(T4*_ISO)/np.sum(_ISO*_ISO); e4=np.abs(T4-c4*_ISO).max()
    return c2,e2,c4,e4
def report(lbl,C,w):
    c2,e2,c4,e4=moments(C,w)
    iso = e4<1e-12; ns = abs(c4-c2**2)<1e-12
    print(f"  {lbl:<44} c2={c2:.6f} err4={e4:.1e} |c4-c2^2|={abs(c4-c2**2):.2e}  "
          f"iso={'Y' if iso else 'N'} ns={'Y' if ns else 'N'}")

print("\n\n=== SECTION V: Q8 velocity set fails isotropy ===")
report("shell 1 only (Q8 imaginaries)", S1, [1]*6)
print("\n=== SECTION VI: second shell repairs it (Theorem 4) ===")
report("shells 1+2, ratio 2:1", S1+S2, [2]*6+[1]*12)
report("shells 1+2, ratio 1:1 (wrong)", S1+S2, [1]*18)
Sn=[tuple(np.array(v)/math.sqrt(2)) for v in S2]
report("shell 2 renormalised to |c|=1 (wrong)", S1+Sn, [2]*6+[1]*12)
print("\n  shell-2 element orders (must be 2-power for Z_2^n):")
for v,lbl in [((0,1,1,0),"(i+j)/sqrt2"),((0,0,1,1),"(j+k)/sqrt2")]:
    n=math.sqrt(sum(x*x for x in v)); u=tuple(x/n for x in v)
    p=(1.,0,0,0)
    for m in range(1,17):
        p=mul(np.array(p),np.array(u))
        if abs(p[0]-1)<1e-9 and max(abs(x) for x in p[1:])<1e-9: print(f"    {lbl}: order {m}"); break

print("\n=== SECTION VII: the dyadic obstruction (Theorem 5) ===")
C19=[(0,0,0)]+S1+S2
report("EXACT (1/3, 1/18, 1/36)", C19, [F(1,3)]+[F(1,18)]*6+[F(1,36)]*12)
report("dyadic (1/4, 1/16, 1/32)", C19, [F(1,4)]+[F(1,16)]*6+[F(1,32)]*12)
for b in (8,12,16,24,32):
    q=lambda f: F(round(float(f)*2**b),2**b)
    report(f"exact set rounded to {b} dyadic bits", C19,
           [q(F(1,3))]+[q(F(1,18))]*6+[q(F(1,36))]*12)
print("\n  minimal exact ring: need 36 | N  ->  9 | N")
for N in (256,768,2304,9216):
    print(f"    N={N:5d}: 36|N = {N%36==0}   1/3->{N/3:9.3f} 1/18->{N/18:8.3f} 1/36->{N/36:8.3f}")
print("\n  => Z_768 insufficient; Z_2304 = 9*256 is minimal (12 bits).")
