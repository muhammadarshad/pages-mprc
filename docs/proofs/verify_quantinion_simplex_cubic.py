#!/usr/bin/env python3
"""Exact regression verifier for the Quantinion Simplex Cubic Decomposition Theorem.

Pure Python. No floats, NumPy, or external packages.
Checks:
  1) full-rank contraction count/rank law for n=4,6,8,10;
  2) Jacobian full column rank for canonical simplex frames;
  3) blind exact recovery of random GL_n(F2)-hidden simplex frames with
     random lifts in Z_256 for n=4,6,8.
"""
from __future__ import annotations
import random

SEED = 20260918
random.seed(SEED)


def gf2_rank(rows: list[list[int]], ncols: int | None = None) -> int:
    if not rows:
        return 0
    a = [[x & 1 for x in row] for row in rows]
    m = len(a)
    n = len(a[0]) if ncols is None else ncols
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
        if r == m:
            break
    return r


def gf2_solve(a: list[list[int]], b: list[int]) -> list[int]:
    m = len(a)
    n = len(a[0])
    aug = [[x & 1 for x in a[i]] + [b[i] & 1] for i in range(m)]
    r = 0
    pivots: list[int] = []
    for c in range(n):
        p = next((i for i in range(r, m) if aug[i][c]), None)
        if p is None:
            continue
        aug[r], aug[p] = aug[p], aug[r]
        for i in range(m):
            if i != r and aug[i][c]:
                aug[i] = [u ^ v for u, v in zip(aug[i], aug[r])]
        pivots.append(c)
        r += 1
    for i in range(r, m):
        if not any(aug[i][:n]) and aug[i][n]:
            raise AssertionError("inconsistent GF(2) system")
    if r != n:
        raise AssertionError(f"non-unique GF(2) system: rank {r}/{n}")
    x = [0] * n
    for i, c in enumerate(pivots):
        x[c] = aug[i][n]
    return x


def canonical_simplex(n: int) -> list[list[int]]:
    out = [[1] * n]
    for i in range(n):
        e = [0] * n
        e[i] = 1
        out.append(e)
    return out


def mat_vec_mod2(g: list[list[int]], v: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, v)) & 1 for row in g]


def random_gl(n: int) -> list[list[int]]:
    while True:
        g = [[random.getrandbits(1) for _ in range(n)] for _ in range(n)]
        if gf2_rank(g) == n:
            return g


def tensor_sum(atoms: list[list[int]], mod: int) -> list[int]:
    n = len(atoms[0])
    t = [0] * (n * n * n)
    for v in atoms:
        idx = 0
        for i in range(n):
            for j in range(n):
                vij = v[i] * v[j]
                for k in range(n):
                    t[idx] = (t[idx] + vij * v[k]) % mod
                    idx += 1
    return t


def tensor_get(t: list[int], n: int, i: int, j: int, k: int) -> int:
    return t[(i * n + j) * n + k]


def contraction_matrix(t2: list[int], n: int, x: list[int]) -> list[list[int]]:
    out = [[0] * n for _ in range(n)]
    for j in range(n):
        for k in range(n):
            s = 0
            for i in range(n):
                s ^= x[i] & tensor_get(t2, n, i, j, k)
            out[j][k] = s
    return out


def recover_supports(t2: list[int], n: int) -> list[list[int]]:
    dual = []
    for mask in range(1, 1 << n):
        x = [(mask >> i) & 1 for i in range(n)]
        if gf2_rank(contraction_matrix(t2, n, x)) == n:
            dual.append(x)
    assert len(dual) == n + 1, (n, len(dual))
    supports = []
    for q in range(n + 1):
        rhs = [1] * (n + 1)
        rhs[q] = 0
        supports.append(gf2_solve(dual, rhs))
    return supports


def build_jacobian(supports: list[list[int]]) -> list[list[int]]:
    r = len(supports)
    n = len(supports[0])
    rows: list[list[int]] = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                row = [0] * (r * n)
                for q, s in enumerate(supports):
                    for a in range(n):
                        value = 0
                        if i == a:
                            value ^= s[j] & s[k]
                        if j == a:
                            value ^= s[i] & s[k]
                        if k == a:
                            value ^= s[i] & s[j]
                        row[q * n + a] = value
                rows.append(row)
    return rows


def recover_atoms(t: list[int], n: int, m: int = 8) -> list[list[int]]:
    t2 = [x & 1 for x in t]
    supports = recover_supports(t2, n)
    cur = [s[:] for s in supports]
    jac = build_jacobian(supports)
    assert gf2_rank(jac) == n * (n + 1)
    for b in range(1, m):
        mod = 1 << (b + 1)
        step = 1 << b
        pred = tensor_sum(cur, mod)
        rhs = []
        for target, got in zip(t, pred):
            d = (target - got) % mod
            assert d % step == 0
            rhs.append((d // step) & 1)
        delta = gf2_solve(jac, rhs)
        for q in range(n + 1):
            for i in range(n):
                cur[q][i] = (cur[q][i] + step * delta[q * n + i]) % mod
    return cur


def canon_set(vs: list[list[int]]) -> list[tuple[int, ...]]:
    return sorted(tuple(v) for v in vs)


def verify_rank_law() -> None:
    for n in (4, 6, 8, 10):
        t2 = tensor_sum(canonical_simplex(n), 2)
        full = 0
        for mask in range(1, 1 << n):
            x = [(mask >> i) & 1 for i in range(n)]
            w = sum(x)
            rank = gf2_rank(contraction_matrix(t2, n, x))
            expected = w if w % 2 == 0 else w + 1
            assert rank == expected, (n, x, rank, expected)
            if rank == n:
                full += 1
        assert full == n + 1
        jac = build_jacobian(canonical_simplex(n))
        assert gf2_rank(jac) == n * (n + 1)
        print(f"n={n}: contraction law PASS; full observers={full}; Jacobian rank={n*(n+1)}")


def verify_random_recovery() -> None:
    for n in (4, 6, 8):
        trials = 20
        for trial in range(trials):
            g = random_gl(n)
            supports = [mat_vec_mod2(g, s) for s in canonical_simplex(n)]
            atoms = []
            for s in supports:
                atom = []
                for bit in s:
                    atom.append(2 * random.randrange(128) + bit)
                atoms.append(atom)
            t = tensor_sum(atoms, 256)
            got = recover_atoms(t, n, 8)
            assert canon_set(got) == canon_set(atoms), (n, trial)
        print(f"n={n}: {trials}/{trials} blind Z_256 recoveries PASS")


def xor_vecs(vs: list[list[int]]) -> list[int]:
    out = [0] * len(vs[0])
    for v in vs:
        out = [a ^ b for a, b in zip(out, v)]
    return out


def recover_residual_simplex(t: list[int], n: int, m: int = 8) -> list[list[int]]:
    """Recover a simplex frame plus one residual atom when the combined Jacobian is full rank."""
    t2 = [x & 1 for x in t]
    # Over F2, diag(v^{⊗3}) = v.  The simplex frame sums to zero,
    # therefore the total diagonal is exactly the extra residual support.
    u = [tensor_get(t2, n, i, i, i) for i in range(n)]
    u3 = tensor_sum([u], 2)
    simplex_tensor = [a ^ b for a, b in zip(t2, u3)]
    simplex_supports = recover_supports(simplex_tensor, n)
    supports = simplex_supports + [u]

    jac = build_jacobian(supports)
    expected = (n + 2) * n
    assert gf2_rank(jac) == expected

    cur = [s[:] for s in supports]
    for b in range(1, m):
        mod = 1 << (b + 1)
        step = 1 << b
        pred = tensor_sum(cur, mod)
        rhs = []
        for target, got in zip(t, pred):
            d = (target - got) % mod
            assert d % step == 0
            rhs.append((d // step) & 1)
        delta = gf2_solve(jac, rhs)
        for q in range(n + 2):
            for i in range(n):
                cur[q][i] = (cur[q][i] + step * delta[q * n + i]) % mod
    return cur


def verify_residual_simplex_extension() -> None:
    n = 8
    base = canonical_simplex(n)
    expected_ranks = {1: 72, 2: 78, 3: 78, 4: 80, 5: 80, 6: 78, 7: 78, 8: 72}
    for w, expected in expected_ranks.items():
        u = [1] * w + [0] * (n - w)
        rank = gf2_rank(build_jacobian(base + [u]))
        assert rank == expected, (w, rank, expected)
    print("n=8 residual-simplex Jacobian profile PASS: 72,78,78,80,80,78,78,72")

    trials = 20
    for trial in range(trials):
        g = random_gl(n)
        simplex_supports = [mat_vec_mod2(g, s) for s in base]
        chosen = random.sample(range(n + 1), 4)
        u = xor_vecs([simplex_supports[q] for q in chosen])
        supports = simplex_supports + [u]
        assert gf2_rank(build_jacobian(supports)) == 80
        atoms = []
        for s in supports:
            atoms.append([2 * random.randrange(128) + bit for bit in s])
        t = tensor_sum(atoms, 256)
        got = recover_residual_simplex(t, n, 8)
        assert canon_set(got) == canon_set(atoms), trial
    print(f"n=8 balanced residual-simplex: {trials}/{trials} blind Z_256 recoveries PASS")


if __name__ == "__main__":
    print(f"seed={SEED}")
    verify_rank_law()
    verify_random_recovery()
    verify_residual_simplex_extension()
    print("ALL CHECKS PASS")
