#!/usr/bin/env python3
"""Exact verifier for the cubic dictionary capacity theorem.

Pure Python. No floats, NumPy, or external packages.
"""
from __future__ import annotations
from itertools import combinations
from math import comb


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


def supports(n: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for k in range(1, min(3, n) + 1):
        out.extend(combinations(range(n), k))
    return out


def selected_coordinate(s: tuple[int, ...]) -> tuple[int, int, int]:
    if len(s) == 1:
        return (s[0], s[0], s[0])
    if len(s) == 2:
        return (s[0], s[0], s[1])
    return (s[0], s[1], s[2])


def dense_atom(n: int, s: tuple[int, ...], mod: int) -> list[int]:
    ss = set(s)
    return [1 if i in ss else (2 % mod) for i in range(n)]


def zeta_minor(n: int, mod: int = 2) -> list[list[int]]:
    ss = supports(n)
    rows: list[list[int]] = []
    for r in ss:
        i, j, k = selected_coordinate(r)
        row = []
        for s in ss:
            v = dense_atom(n, s, mod)
            row.append((v[i] * v[j] * v[k]) % mod)
        rows.append(row)
    return rows


def cube_binary(v: list[int]) -> list[int]:
    n = len(v)
    return [(v[i] & v[j] & v[k]) for i in range(n) for j in range(n) for k in range(n)]


def verify_capacities() -> None:
    expected = [1, 3, 7, 14, 25, 41, 63, 92]
    for n, cap in enumerate(expected, 1):
        formula = sum(comb(n, k) for k in range(1, min(3, n) + 1))
        assert formula == cap
        z = zeta_minor(n, 2)
        rank = gf2_rank(z)
        assert rank == cap, (n, rank, cap)
        print(f"n={n}: capacity={cap}; zeta-minor rank={rank} PASS")


def verify_four_coordinate_dependency() -> None:
    n = 8
    q = (0, 1, 2, 3)
    atoms = []
    for k in range(1, 5):
        for s in combinations(q, k):
            v = [1 if i in s else 0 for i in range(n)]
            atoms.append(cube_binary(v))
    assert len(atoms) == 15

    parity_sum = [0] * (n ** 3)
    for atom in atoms:
        parity_sum = [a ^ b for a, b in zip(parity_sum, atom)]
    assert not any(parity_sum)

    exact = [0] * (n ** 3)
    for atom in atoms:
        exact = [(a + 128 * b) & 0xFF for a, b in zip(exact, atom)]
    assert not any(exact)
    print("15-atom four-coordinate torsion relation PASS over Z_256")


if __name__ == "__main__":
    verify_capacities()
    verify_four_coordinate_dependency()
    print("ALL CHECKS PASS")
