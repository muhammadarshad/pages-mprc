#!/usr/bin/env python3
"""Exact relation-code/Koszul verifier for excess rank t=3.

Pure Python. No floats, NumPy, or external packages.

For r=n+3, relation-code dimension is 3.  Up to GL_3(F2) and coordinate
permutation, a code is determined by the multiplicities of the eight
coordinate types in F2^3.  This program exhaustively enumerates canonical
types for n=7..12, keeps the admissible d(K)>=5 frames, constructs a parity
frame S with ker(S)=K, and checks injectivity of the exact Koszul map

    kappa_S : F2^n tensor K -> Lambda^3 F2^n.

It also confirms that no admissible [n+3,3,5] code exists for n<7 by the
Griesmer bound.
"""
from __future__ import annotations
from itertools import product, combinations


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


def nullspace(rows: list[int], ncols: int) -> list[int]:
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


def gl3_permutations() -> list[tuple[int, ...]]:
    perms = set()
    for rows in product(range(8), repeat=3):
        if gf2_rank(list(rows), 3) != 3:
            continue
        p = []
        for v in range(8):
            out = 0
            for i, row in enumerate(rows):
                if (row & v).bit_count() & 1:
                    out |= 1 << i
            p.append(out)
        perms.add(tuple(p))
    assert len(perms) == 168
    return sorted(perms)


GL3 = gl3_permutations()


def compositions(total: int, k: int, prefix=()):
    if k == 1:
        yield prefix + (total,)
        return
    for x in range(total + 1):
        yield from compositions(total - x, k - 1, prefix + (x,))


def canonical_counts(counts: tuple[int, ...]) -> tuple[int, ...]:
    reps = []
    for perm in GL3:
        arr = [0] * 8
        for old, count in enumerate(counts):
            arr[perm[old]] = count
        reps.append(tuple(arr))
    return min(reps)


def relation_code_from_counts(counts: tuple[int, ...]) -> list[int]:
    cols: list[int] = []
    for typ, count in enumerate(counts):
        cols.extend([typ] * count)
    rows = [0, 0, 0]
    for j, typ in enumerate(cols):
        for i in range(3):
            if (typ >> i) & 1:
                rows[i] |= 1 << j
    return rows


def code_weights(rows: list[int]) -> list[int]:
    out = []
    for mask in range(1, 8):
        w = 0
        for i, row in enumerate(rows):
            if (mask >> i) & 1:
                w ^= row
        out.append(w.bit_count())
    return sorted(out)


def frame_from_relation_code(K: list[int], length: int) -> list[int]:
    rows = nullspace(K, length)
    n = length - 3
    assert len(rows) == n
    cols = []
    for j in range(length):
        col = 0
        for i, row in enumerate(rows):
            if (row >> j) & 1:
                col |= 1 << i
        cols.append(col)
    return cols


def koszul_rank(K: list[int], cols: list[int], n: int) -> int:
    triples = list(combinations(range(n), 3))
    triple_index = {t: i for i, t in enumerate(triples)}

    omegas = []
    for krow in K:
        om = [[0] * n for _ in range(n)]
        for q, s in enumerate(cols):
            if not ((krow >> q) & 1):
                continue
            inds = [i for i in range(n) if (s >> i) & 1]
            for i, j in combinations(inds, 2):
                om[i][j] ^= 1
                om[j][i] ^= 1
        omegas.append(om)

    images = []
    for om in omegas:
        for a in range(n):
            vec = 0
            for i, j, k in triples:
                value = 0
                if a == i:
                    value ^= om[j][k]
                if a == j:
                    value ^= om[i][k]
                if a == k:
                    value ^= om[i][j]
                if value:
                    vec |= 1 << triple_index[(i, j, k)]
            images.append(vec)

    return gf2_rank(images, len(triples))


def classify(n: int) -> tuple[int, int, int]:
    length = n + 3
    seen = set()
    admissible = 0
    sidon = 0
    rigid = 0

    for counts in compositions(length, 8):
        can = canonical_counts(counts)
        if can in seen:
            continue
        seen.add(can)

        K = relation_code_from_counts(can)
        if gf2_rank(K, length) != 3:
            continue

        weights = code_weights(K)
        if min(weights) < 3:
            continue

        cols = frame_from_relation_code(K, length)
        if any(x == 0 for x in cols) or len(set(cols)) != length:
            continue
        if gf2_rank(cols, n) != n:
            continue

        admissible += 1

        if min(weights) < 5:
            continue

        sidon += 1
        rank = koszul_rank(K, cols, n)
        assert rank == 3 * n, (n, can, weights, rank, 3 * n)
        rigid += 1

    return admissible, sidon, rigid


def main() -> None:
    # Griesmer for a binary [n+3,3,5] code:
    # length >= ceil(5)+ceil(5/2)+ceil(5/4)=5+3+2=10.
    assert 6 + 3 < 10

    expected = {
        7: (80, 2, 2),
        8: (151, 11, 11),
        9: (266, 36, 36),
        10: (440, 91, 91),
        11: (695, 195, 195),
        12: (1059, 373, 373),
    }

    for n in range(7, 13):
        got = classify(n)
        assert got == expected[n], (n, got, expected[n])
        print(
            f"n={n}, r={n+3}: admissible={got[0]}, "
            f"d(K)>=5={got[1]}, Koszul-injective={got[2]} PASS"
        )

    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
