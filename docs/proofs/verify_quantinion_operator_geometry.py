#!/usr/bin/env python3
"""Exact regression verifier for Quantinion Operator & Transpose Geometry.

Pure Python. No floats, NumPy, or external packages.
"""
from __future__ import annotations
from math import gcd

MOD = 256
REF = 7  # matrix index used as the distinguished reference state


def gf2_rank(a: list[list[int]]) -> int:
    a = [[x & 1 for x in row] for row in a]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(m):
            if i != r and a[i][c]:
                a[i] = [u ^ v for u, v in zip(a[i], a[r])]
        r += 1
    return r


def mat_unit(i: int, j: int) -> list[list[int]]:
    m = [[0] * 8 for _ in range(8)]
    m[i][j] = 1
    return m


def mat_sub(a, b):
    return [[(a[i][j] - b[i][j]) & 0xFF for j in range(8)] for i in range(8)]


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(8)) & 0xFF for j in range(8)] for i in range(8)]


def comm(a, b):
    return mat_sub(mat_mul(a, b), mat_mul(b, a))


def flatten(a):
    return [x for row in a for x in row]


def verify_f21() -> None:
    multipliers = (1, 2, 4)
    maps = [tuple((a * x + b) % 7 for x in range(7)) for a in multipliers for b in range(7)]
    assert len(set(maps)) == 21
    pool = set(maps)
    for f in maps:
        for g in maps:
            h = tuple(f[g[x]] for x in range(7))
            assert h in pool
    q = {1, 2, 4}
    nq = {(-x) % 7 for x in q}
    assert q.isdisjoint(nq) and q | nq == set(range(1, 7))
    edges = [(x, y) for x in range(7) for y in range(7) if x != y and ((y - x) % 7) in q]
    assert len(edges) == 21
    assert len({frozenset((x, y)) for x, y in edges}) == 21
    print("F21 and 21-edge orientation PASS")


def verify_operator_module() -> None:
    basis = []
    # 56 off-diagonal units.
    for i in range(8):
        for j in range(8):
            if i != j:
                basis.append(flatten(mat_unit(i, j)))
    # Seven diagonal differences E_aa - E_ref,ref.
    for a in range(7):
        basis.append(flatten(mat_sub(mat_unit(a, a), mat_unit(REF, REF))))
    assert len(basis) == 63
    assert gf2_rank(basis) == 63

    # Fourteen reference couplings generate all matrix-unit basis directions.
    for a in range(7):
        lhs = comm(mat_unit(a, REF), mat_unit(REF, a))
        rhs = mat_sub(mat_unit(a, a), mat_unit(REF, REF))
        assert lhs == rhs
        for b in range(7):
            if a == b:
                continue
            lhs = comm(mat_unit(a, REF), mat_unit(REF, b))
            assert lhs == mat_unit(a, b)
    print("63-dimensional trace-zero basis and 14-generator commutators PASS")


def verify_qh4_mixed_radix() -> None:
    vac = {0, 64, 128, 192}
    positions = []
    for theta in range(4):
        local = []
        for a in range(3):
            for p in range(3):
                for sigma in range(1, 8):
                    m = 64 * theta + 21 * a + 7 * p + sigma
                    local.append(m)
                    z = (7 * m) & 0xFF
                    positions.append(z)
        assert local == list(range(64 * theta + 1, 64 * theta + 64))
    assert len(positions) == 252
    assert len(set(positions)) == 252
    assert set(range(256)) - set(positions) == vac
    print("QH4 mixed-radix 252/252 bijection PASS")


def verify_transpose() -> None:
    for k in range(3):
        fixed = 0
        pairs = set()
        for theta in range(4):
            for sigma in range(1, 8):
                for a in range(3):
                    for p in range(3):
                        aa = (p + k) % 3
                        pp = (a - k) % 3
                        # involution
                        assert ((pp + k) % 3, (aa - k) % 3) == (a, p)
                        # invariant and transported coordinate
                        assert (aa + pp) % 3 == (a + p) % 3
                        j = (p - a) % 3
                        jj = (pp - aa) % 3
                        assert jj == (-(j + 2 * k)) % 3
                        s0 = (theta, sigma, a, p)
                        s1 = (theta, sigma, aa, pp)
                        if s0 == s1:
                            fixed += 1
                        else:
                            pairs.add(tuple(sorted((s0, s1))))
        assert fixed == 84
        assert len(pairs) == 84
    print("Arshad Transpose: 84 fixed + 84 two-cycles for each k PASS")


def verify_tensor_lift_kernel() -> None:
    for ell in range(1, 9):
        scalars = [lam for lam in range(MOD) if (ell * lam) % MOD == 0]
        assert len(scalars) == gcd(ell, MOD)
    assert [x for x in range(MOD) if (2 * x) % MOD == 0] == [0, 128]
    assert [x for x in range(MOD) if (3 * x) % MOD == 0] == [0]
    assert [x for x in range(MOD) if (4 * x) % MOD == 0] == [0, 64, 128, 192]
    print("tensor-lift scalar kernel counts PASS; ell=4 gives QH4 quartet")


if __name__ == "__main__":
    verify_f21()
    verify_operator_module()
    verify_qh4_mixed_radix()
    verify_transpose()
    verify_tensor_lift_kernel()
    print("ALL CHECKS PASS")
