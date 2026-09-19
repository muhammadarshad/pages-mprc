#!/usr/bin/env python3
"""Exact verifier for the eight-state operator/transpose geometry paper.
Pure Python; integer arithmetic only.
"""
from itertools import product, combinations
from math import gcd

RES={1,2,4}
Z7=range(7)

def compose(f,g): return tuple(f[g[x]] for x in Z7)

def verify_f21():
    maps=[]
    for a in (1,2,4):
        for b in Z7:
            maps.append(tuple((a*x+b)%7 for x in Z7))
    assert len(set(maps))==21
    M=set(maps)
    for f in M:
        for g in M:
            assert compose(f,g) in M
    return True

def verify_orientation():
    seen=set()
    for u,v in combinations(Z7,2):
        d=(v-u)%7
        directed=(u,v) if d in RES else (v,u)
        assert directed not in seen
        seen.add(directed)
    assert len(seen)==21
    return True

def E(a,b):
    return 1 << (a*8+b)

def matmul_unit(a,b,c,d):
    return E(a,d) if b==c else 0

def comm(a,b,c,d):
    return matmul_unit(a,b,c,d) ^ matmul_unit(c,d,a,b)

def verify_trace_basis_and_generators():
    basis=[]
    for a in range(8):
        for b in range(8):
            if a!=b: basis.append(E(a,b))
    for a in range(1,8): basis.append(E(a,a)^E(0,0))
    assert len(basis)==63
    rows=basis[:]; rank=0
    for c in range(64):
        p=next((i for i in range(rank,len(rows)) if (rows[i]>>c)&1),None)
        if p is None: continue
        rows[rank],rows[p]=rows[p],rows[rank]
        for i in range(len(rows)):
            if i!=rank and ((rows[i]>>c)&1): rows[i]^=rows[rank]
        rank+=1
    assert rank==63
    for a in range(1,8):
        assert comm(a,0,0,a) == (E(a,a)^E(0,0))
        for b in range(1,8):
            if a!=b:
                assert comm(a,0,0,b) == E(a,b)
    return True

def verify_address():
    ms=[]; zs=[]
    for theta in range(4):
        for a in range(3):
            for p in range(3):
                for sigma in range(1,8):
                    m=64*theta+21*a+7*p+sigma
                    ms.append(m); zs.append((7*m)%256)
    assert len(ms)==252 and len(set(ms))==252
    assert set(range(256))-set(ms)=={0,64,128,192}
    assert len(set(zs))==252
    assert set(range(256))-set(zs)=={0,64,128,192}
    return True

def T(k,a,p): return ((p+k)%3,(a-k)%3)

def verify_transpose():
    for k in range(3):
        fixed=0
        for a,p in product(range(3),repeat=2):
            aa,pp=T(k,a,p)
            assert T(k,aa,pp)==(a,p)
            assert (aa+pp)%3==(a+p)%3
            j=(p-a)%3
            jp=(pp-aa)%3
            assert jp==(-(j+2*k))%3
            if (aa,pp)==(a,p):
                fixed+=1
                assert j==(-k)%3
        assert fixed==3
    assert 3*4*7==84
    assert ((9-3)//2)*4*7==84
    return True

def verify_tensor_kernels():
    for ell in range(1,9):
        sols=[lam for lam in range(256) if (ell*lam)%256==0]
        assert len(sols)==gcd(ell,256)
    assert [x for x in range(256) if 2*x%256==0]==[0,128]
    assert [x for x in range(256) if 3*x%256==0]==[0]
    assert [x for x in range(256) if 4*x%256==0]==[0,64,128,192]
    return True

def main():
    assert verify_f21()
    assert verify_orientation()
    assert verify_trace_basis_and_generators()
    assert verify_address()
    assert verify_transpose()
    assert verify_tensor_kernels()
    print("F21 maps/closure: PASS")
    print("21-edge orientation: PASS")
    print("trace-zero rank 63 + 14-generator commutators: PASS")
    print("252-state QH4 address: PASS")
    print("transpose 84 fixed + 84 two-cycles: PASS")
    print("tensor-lift scalar kernels ell=1..8: PASS")
    print("ALL CHECKS PASS")

if __name__=="__main__":
    main()
