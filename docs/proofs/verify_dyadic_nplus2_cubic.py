#!/usr/bin/env python3
"""Exact verifier for rank-(n+2) dyadic cubic identifiability.

Pure Python. No floats, NumPy, or third-party packages.

Checks the Quantinion case n=8, r=10:
  1. permutation/GL_8 frame classes via binary [10,2] relation codes;
  2. exactly 32 admissible frame classes (distinct nonzero spanning parities);
  3. cubic lifting Jacobian is injective iff relation-code distance >= 5;
  4. exactly 9 of the 32 classes are rigid;
  5. every non-rigid class has an exact second Z_256 decomposition obtained
     by a top-bit perturbation in a Jacobian-kernel direction;
  6. exhaustive parity-support rigidity for the small control cases n=3,4.
"""
from __future__ import annotations

from itertools import combinations


def gf2_rank(rows: list[int], ncols: int) -> int:
    a = rows[:]
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(a)) if (a[i] >> c) & 1), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> c) & 1):
                a[i] ^= a[r]
        r += 1
    return r


def gf2_nullspace(rows: list[int], ncols: int) -> list[int]:
    a = rows[:]
    r = 0
    pivots: list[int] = []
    for c in range(ncols):
        p = next((i for i in range(r, len(a)) if (a[i] >> c) & 1), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> c) & 1):
                a[i] ^= a[r]
        pivots.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis: list[int] = []
    for f in free:
        x = 1 << f
        for i, c in enumerate(pivots):
            if (a[i] & x).bit_count() & 1:
                x ^= 1 << c
        basis.append(x)
    return basis


def relation_code_from_counts(a: int, b: int, c: int, d: int) -> list[int]:
    """Coordinate-type counts 00,10,01,11 for a 2D relation code."""
    k1 = 0
    k2 = 0
    idx = 0
    for typ, count in [((0, 0), a), ((1, 0), b), ((0, 1), c), ((1, 1), d)]:
        for _ in range(count):
            if typ[0]:
                k1 |= 1 << idx
            if typ[1]:
                k2 |= 1 << idx
            idx += 1
    return [k1, k2]


def frame_from_relation_code(krows: list[int], length: int) -> list[int]:
    """Columns of any full-row-rank S with ker(S)=K, represented as bit vectors."""
    rows = gf2_nullspace(krows, length)
    n = length - 2
    assert len(rows) == n
    cols: list[int] = []
    for j in range(length):
        col = 0
        for i, row in enumerate(rows):
            col |= ((row >> j) & 1) << i
        cols.append(col)
    return cols


def jacobian_rows(cols: list[int], n: int) -> list[int]:
    r = len(cols)
    bits = [[(s >> i) & 1 for i in range(n)] for s in cols]
    rows: list[int] = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                row = 0
                for q, s in enumerate(bits):
                    for a in range(n):
                        value = (
                            ((1 if i == a else 0) & s[j] & s[k])
                            ^ (s[i] & (1 if j == a else 0) & s[k])
                            ^ (s[i] & s[j] & (1 if k == a else 0))
                        )
                        if value:
                            row |= 1 << (q * n + a)
                rows.append(row)
    return rows


def atom_vector(col: int, n: int) -> list[int]:
    return [(col >> i) & 1 for i in range(n)]


def tensor_sum(atoms: list[list[int]], mod: int) -> list[int]:
    n = len(atoms[0])
    out = [0] * (n * n * n)
    for v in atoms:
        t = 0
        for i in range(n):
            for j in range(n):
                vij = v[i] * v[j]
                for k in range(n):
                    out[t] = (out[t] + vij * v[k]) % mod
                    t += 1
    return out


def enumerate_n8_classes() -> None:
    n = 8
    length = 10
    classes = []
    good_weight_triples = []
    exact_bad_collisions = 0

    # GL_2 permutes the three nonzero coordinate types; use b >= c >= d.
    for a in range(length + 1):
        rem = length - a
        for b in range(rem + 1):
            for c in range(rem - b + 1):
                d = rem - b - c
                if not (b >= c >= d):
                    continue
                if sum(x > 0 for x in (b, c, d)) < 2:
                    continue

                weights = tuple(sorted((b + d, c + d, b + c)))
                distance = min(weights)
                # d(K)>=3 iff the frame columns are distinct and nonzero.
                if distance < 3:
                    continue

                K = relation_code_from_counts(a, b, c, d)
                assert gf2_rank(K, length) == 2
                cols = frame_from_relation_code(K, length)
                assert len(cols) == length
                assert len(set(cols)) == length
                assert all(cols)
                assert gf2_rank(cols, n) == n

                J = jacobian_rows(cols, n)
                rank_j = gf2_rank(J, length * n)
                rigid = rank_j == length * n
                assert rigid == (distance >= 5)

                if rigid:
                    good_weight_triples.append(weights)
                else:
                    # Any nonzero Jacobian-kernel vector gives an exact second
                    # decomposition over Z_256 by toggling only the top bit.
                    kernel = gf2_nullspace(J, length * n)
                    assert kernel
                    delta = kernel[0]
                    atoms = [atom_vector(s, n) for s in cols]
                    altered = [v[:] for v in atoms]
                    for q in range(length):
                        for i in range(n):
                            if (delta >> (q * n + i)) & 1:
                                altered[q][i] = (altered[q][i] + 128) & 255
                    assert atoms != altered
                    assert tensor_sum(atoms, 256) == tensor_sum(altered, 256)
                    exact_bad_collisions += 1

                classes.append((a, b, c, d, weights, distance, rank_j))

    assert len(classes) == 32
    assert len(good_weight_triples) == 9
    assert exact_bad_collisions == 23

    expected = {
        (5, 5, 6), (5, 5, 8), (5, 5, 10),
        (5, 6, 7), (5, 6, 9), (5, 7, 8),
        (6, 6, 6), (6, 6, 8), (6, 7, 7),
    }
    assert set(good_weight_triples) == expected

    print("n=8,r=10 relation-code classes: 32 PASS")
    print("rigid classes d(K)>=5: 9 PASS")
    print("non-rigid classes with exact Z_256 top-bit collisions: 23/23 PASS")
    print("rigid relation-weight triples:", sorted(expected))


def moment_mask(x: int, n: int) -> int:
    """Nonconstant square-free Boolean moments of degrees 1,2,3."""
    out = 0
    p = 0
    for degree in range(1, min(3, n) + 1):
        for inds in combinations(range(n), degree):
            value = 1
            for i in inds:
                value &= (x >> i) & 1
            if value:
                out |= 1 << p
            p += 1
    return out


def verify_small_parity_rigidity() -> None:
    # Exhaustive controls. The general n=4..9 proof in the manuscript uses
    # Reed-Muller duality and its low-weight classification.
    for n in (3, 4):
        r = n + 2
        pts = list(range(1, 1 << n))
        signatures: dict[int, tuple[int, ...]] = {}
        checked = 0
        for support in combinations(pts, r):
            if gf2_rank(list(support), n) < n:
                continue
            sig = 0
            for x in support:
                sig ^= moment_mask(x, n)
            assert sig not in signatures or signatures[sig] == support
            signatures[sig] = support
            checked += 1
        print(f"n={n}, r={r}: exhaustive spanning parity supports {checked} unique PASS")


if __name__ == "__main__":
    verify_small_parity_rigidity()
    enumerate_n8_classes()
    print("ALL CHECKS PASS")
