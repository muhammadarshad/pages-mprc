#!/usr/bin/env python3
"""Exact verifier for the cubic dictionary capacity paper.
Pure Python; integer/bit arithmetic only.
"""
from itertools import combinations
from math import comb

def n3(n):
    return sum(comb(n,k) for k in range(1,min(3,n)+1))

def subsets_upto3(n):
    return [s for k in range(1,min(3,n)+1) for s in combinations(range(n),k)]

def gf2_rank(rows, ncols):
    rows=list(rows); r=0
    for c in range(ncols):
        p=next((i for i in range(r,len(rows)) if (rows[i]>>c)&1),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>c)&1): rows[i]^=rows[r]
        r+=1
        if r==len(rows): break
    return r

def verify_zeta_minor(n):
    subs=subsets_upto3(n)
    rows=[]
    for R in subs:
        bits=0
        RR=set(R)
        for j,S in enumerate(subs):
            if RR.issubset(S): bits |= 1<<j
        rows.append(bits)
    return gf2_rank(rows,len(subs)) == len(subs)

def atom_cube(v, mod):
    n=len(v)
    return [v[i]*v[j]*v[k] % mod for i in range(n) for j in range(n) for k in range(n)]

def verify_torsion(modulus=256):
    n=4
    total=[0]*(n*n*n)
    for mask in range(1,16):
        v=[(mask>>i)&1 for i in range(n)]
        c=atom_cube(v,modulus)
        for i,x in enumerate(c): total[i]=(total[i]+x)%modulus
    return all(((modulus//2)*x) % modulus == 0 for x in total)

def main():
    seq=[]
    for n in range(1,9):
        assert verify_zeta_minor(n)
        seq.append(n3(n))
    assert seq == [1,3,7,14,25,41,63,92]
    assert verify_torsion(256)
    print("capacity sequence:", seq)
    print("Boolean zeta minors: PASS")
    print("explicit Z256 torsion lift: PASS")
    print("ALL CHECKS PASS")

if __name__=="__main__":
    main()
