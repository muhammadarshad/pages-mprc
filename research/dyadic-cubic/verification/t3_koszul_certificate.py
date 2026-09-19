#!/usr/bin/env python3
"""
t3_koszul_certificate.py

Exact, dependency-free GF(2) proof certificate for the t=3 cubic-lift frontier.

It verifies the finite endgame of the dimension-free reduction:

  dim K = 3, d(K) >= 5, ker(kappa_S) != 0
      => active relation-code length N is in {10,11,12,13,14}
      => every nonzero k in K satisfies the analytic necessary bound
             lower_rank_Omega(k) <= 6
      => only 20 GL(3,2)-orbits remain.

For each of those 20 orbits this program constructs a parity-check frame
S with ker S = K, constructs

    Omega_S(k) = sum_{p<q, k_p=k_q=1} s_p wedge s_q,

and the Koszul map

    kappa_S : V tensor K -> Lambda^3 V,
    e_i tensor k_j |-> e_i wedge Omega_S(k_j),

then checks exact full column rank over GF(2).

No floats, NumPy, Sage, GAP, or external packages.
"""

from itertools import product, combinations

VECS = tuple(range(1, 8))  # nonzero vectors of F_2^3


def dot3(a, b):
    return ((a & b).bit_count() & 1)


def gf2_rank(rows, ncols):
    rows = list(rows)
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> c) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= rows[r]
        r += 1
        if r == len(rows):
            break
    return r


def gf2_rref(rows, ncols):
    rows = list(rows)
    pivots = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> c) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= rows[r]
        pivots.append(c)
        r += 1
        if r == len(rows):
            break
    return rows, pivots


def gf2_nullspace_basis(rows, ncols):
    rr, pivots = gf2_rref(rows, ncols)
    free = [c for c in range(ncols) if c not in pivots]
    out = []
    for f in free:
        x = 1 << f
        for i, p in enumerate(pivots):
            if (rr[i] >> f) & 1:
                x |= 1 << p
        out.append(x)
    return out


def compositions(total, k, prefix=()):
    if k == 1:
        yield prefix + (total,)
        return
    for i in range(total + 1):
        yield from compositions(total - i, k - 1, prefix + (i,))


def build_gl3_permutations():
    perms = set()
    for a, b, c in product(VECS, repeat=3):
        if gf2_rank((a, b, c), 3) < 3:
            continue
        perm = []
        for x in VECS:
            y = 0
            if x & 1:
                y ^= a
            if x & 2:
                y ^= b
            if x & 4:
                y ^= c
            perm.append(VECS.index(y))
        perms.add(tuple(perm))
    assert len(perms) == 168
    return tuple(sorted(perms))


GL3 = build_gl3_permutations()


def canonical_multiplicity(m):
    images = []
    for p in GL3:
        mm = [0] * 7
        for i, j in enumerate(p):
            mm[j] = m[i]
        images.append(tuple(mm))
    return min(images)


def code_weights(m):
    return tuple(
        sum(m[i] for i, v in enumerate(VECS) if dot3(a, v))
        for a in VECS
    )


def min_distance(m):
    return min(code_weights(m))


def generator_rows(m):
    cols = []
    for multiplicity, v in zip(m, VECS):
        cols.extend([v] * multiplicity)

    rows = []
    for a in (1, 2, 4):
        row = 0
        for j, v in enumerate(cols):
            if dot3(a, v):
                row |= 1 << j
        rows.append(row)
    assert gf2_rank(rows, len(cols)) == 3
    return tuple(rows)


def codeword(rows, coeff):
    x = 0
    for i in range(3):
        if (coeff >> i) & 1:
            x ^= rows[i]
    return x


def shortened_dimension(rows, k):
    contained = 0
    for a in range(8):
        u = codeword(rows, a)
        if u & ~k == 0:
            contained += 1
    assert contained in (2, 4, 8)
    return {2: 1, 4: 2, 8: 3}[contained]


def analytic_omega_rank_lower_bound(weight, h):
    # Correct quotient lower bound:
    #   even w: rank Omega >= w - 2h
    #   odd  w: rank Omega >= w - 2h + 1
    return weight - 2 * h + (weight & 1)


def analytically_admissible(m):
    if min_distance(m) < 5:
        return False
    rows = generator_rows(m)
    for a in VECS:
        k = codeword(rows, a)
        w = k.bit_count()
        h = shortened_dimension(rows, k)
        if analytic_omega_rank_lower_bound(w, h) > 6:
            return False
    return True


def parity_check_columns(m):
    Krows = generator_rows(m)
    N = sum(m)
    Hrows = gf2_nullspace_basis(Krows, N)
    n = N - 3
    assert len(Hrows) == n
    assert gf2_rank(Hrows, N) == n

    scols = []
    for q in range(N):
        s = 0
        for i, row in enumerate(Hrows):
            if (row >> q) & 1:
                s |= 1 << i
        scols.append(s)

    # Check S*k^T=0 for the whole basis.
    for kr in Krows:
        accum = 0
        for q, s in enumerate(scols):
            if (kr >> q) & 1:
                accum ^= s
        assert accum == 0

    return tuple(scols), Krows


def pair_positions(n):
    return {(i, j): p
            for p, (i, j) in enumerate(combinations(range(n), 2))}


def triple_positions(n):
    return {(i, j, k): p
            for p, (i, j, k) in enumerate(combinations(range(n), 3))}


def wedge2(a, b, n, pair_pos):
    out = 0
    for i in range(n):
        ai = (a >> i) & 1
        bi = (b >> i) & 1
        for j in range(i + 1, n):
            if (ai & ((b >> j) & 1)) ^ (bi & ((a >> j) & 1)):
                out |= 1 << pair_pos[(i, j)]
    return out


def omega(scols, k, n):
    pair_pos = pair_positions(n)
    supp = [q for q in range(len(scols)) if (k >> q) & 1]
    out = 0
    for p, q in combinations(supp, 2):
        out ^= wedge2(scols[p], scols[q], n, pair_pos)
    return out


def alternating_rank(two_form, n):
    pair_pos = pair_positions(n)
    rows = [0] * n
    for (i, j), p in pair_pos.items():
        if (two_form >> p) & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return gf2_rank(rows, n)


def wedge_basis_with_two_form(i, two_form, n):
    pair_pos = pair_positions(n)
    triple_pos = triple_positions(n)
    out = 0
    for (a, b, c), p in triple_pos.items():
        if i == a:
            bit = (two_form >> pair_pos[(b, c)]) & 1
        elif i == b:
            bit = (two_form >> pair_pos[(a, c)]) & 1
        elif i == c:
            bit = (two_form >> pair_pos[(a, b)]) & 1
        else:
            bit = 0
        if bit:
            out |= 1 << p
    return out


def kappa_data(m):
    N = sum(m)
    n = N - 3
    scols, Krows = parity_check_columns(m)

    omegas = [omega(scols, Krows[j], n) for j in range(3)]

    columns = []
    for j in range(3):
        for i in range(n):
            columns.append(wedge_basis_with_two_form(i, omegas[j], n))

    codim = n * (n - 1) * (n - 2) // 6
    rank = gf2_rank(columns, codim)

    all_omega_ranks = []
    for a in VECS:
        k = codeword(Krows, a)
        all_omega_ranks.append(alternating_rank(omega(scols, k, n), n))

    return rank, tuple(all_omega_ranks)


def orbit_representatives(N):
    reps = {}
    for m in compositions(N, 7):
        if min_distance(m) >= 5:
            reps.setdefault(canonical_multiplicity(m), None)
    return tuple(sorted(reps))


def main():
    expected_all_active_orbits = {10: 2, 11: 9, 12: 25, 13: 55, 14: 104}
    expected_candidates = {10: 2, 11: 7, 12: 8, 13: 2, 14: 1}

    certificate = []
    summary = []

    for N in range(10, 15):
        reps = orbit_representatives(N)
        assert len(reps) == expected_all_active_orbits[N]

        candidates = [m for m in reps if analytically_admissible(m)]
        assert len(candidates) == expected_candidates[N]

        full = 0
        for m in candidates:
            kr, omega_ranks = kappa_data(m)
            n = N - 3
            target = 3 * n
            assert kr == target
            full += 1
            certificate.append({
                "N": N,
                "n": n,
                "multiplicities": list(m),
                "weights": list(code_weights(m)),
                "omega_ranks": list(omega_ranks),
                "kappa_rank": kr,
                "kappa_columns": target,
            })

        summary.append((N, N - 3, len(reps), len(candidates), full))

    assert len(certificate) == 20
    assert sum(row[4] for row in summary) == 20

    print("t=3 Koszul proof certificate")
    print("GL(3,2) size:", len(GL3))
    print()
    print(" N   n   active Sidon orbits   analytic candidates   full-rank kappa")
    for N, n, all_orb, cand, full in summary:
        print(f"{N:2d}  {n:2d}         {all_orb:3d}                  {cand:2d}               {full:2d}/{cand:2d}")
    print()
    print("TOTAL analytic candidates: 20")
    print("TOTAL full-rank kappa:      20/20")
    print("RESULT: PASS")

    return certificate


if __name__ == "__main__":
    cert = main()