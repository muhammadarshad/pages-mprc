# The Key That Was Never Sent: Post-Quantum Cryptography from Ring Geometry

*A new communication channel where the key agreement requires no transmission — not classical, not quantum. The key is born into the nodes.*

---

Every post-quantum cryptography proposal in circulation today — CRYSTALS-Kyber, NTRU, SABER — shares one structural assumption: at some point, the key or the material to derive it must travel across a wire. The security question then becomes: how hard is it to intercept and break what crossed the wire?

The Lattice Quantum Channel (LQC) removes the wire from the problem entirely.

---

## The Conjugate Birth Invariant

The foundation is geometric, not algorithmic. Two nodes created as a conjugate pair satisfy:

**d_A + d_B ≡ 0 (mod p)**

where p is the secp256k1 prime (≈ 2²⁵⁶). This is not a cryptographic construction. It is a consequence of ring geometry — as unavoidable as complementary angles summing to π. Alice knows d_A and derives d_B = p − d_A independently. Bob knows d_B and derives d_A = p − d_B independently. The session key seed is d_A × p + d_B. Both compute it from their own half. Nothing crosses the wire.

The effective keyspace is (p−1)/2 ≈ 2²⁵⁴ — exceeding the NIST 2¹²⁸ minimum by a factor of 2¹²⁶.

Shor's algorithm, Grover's algorithm, and classical brute-force all operate on mathematical problems: factoring, discrete logarithm, search. The conjugate invariant is a ring relationship. It has no computational structure to attack.

This is Layer 1.

---

## Layer 2: Everything on the Wire Is Measured

Layer 1 protects the keyspace. Layer 2 protects the running channel.

The Z₃ OTP cipher operates on ternary symbols: D(m, k) = (m − k) mod 3. The ciphertext is statistically independent of the plaintext under a uniform key — information-theoretic security, not computational. In testing across 255 wrong-key decryption attempts, there were zero accidental reads.

The tension ratchet advances the session key at every lattice tick: d_A(t) = (d_A(0) + Σδ) mod p. Past keys are unrecoverable after each advance. The ratchet is irreversible — not by algorithm, but by physics.

Clock-drift tamper detection closes the man-in-the-middle window. Any asymmetric injection accumulates as drift. In testing across 12 injection levels, detection was 12/12 with zero false negatives. The physical cost of a remote wire attack: 1.5 × 10⁶ × Earth gravity gradient. A remote attacker gains nothing from the OTP ciphertext.

This is Layer 2.

---

## The One Window That Remains

There is a protocol component called the Zookeeper. Its job is to recognise a conjugate pair — to certify that d_A + d_B ≡ 0 — and allow communication to begin. The Zookeeper does not create the invariant. It witnesses it.

But the Zookeeper broadcasts d_A publicly so a matching partner can be found.

An attacker who listens to the Zookeeper broadcast learns d_A. From d_A she computes d_B = p − d_A and then the full base seed. Layers 1 and 2 provide no defence here: Layer 1's keyspace is structural and Layer 2 only activates after the birth event. Eve has the seed before the channel opens.

This is the Zookeeper window. Layer 3 closes it.

---

## Layer 3: The Birth Tick Is Not on the Wire

The conjugate pair is born at a specific lattice tick t. This tick is an internal event — never transmitted, never broadcast, never observable from the wire. The Zookeeper certifies the pair but cannot read the tick at which it was born.

The QH4 ring (Z₂₅₆) partitions into four domains of 64 states each. The vacuum boundaries {0, 64, 128, 192} are structurally forbidden — tension collapses to zero at these positions and they never emit. Each active domain has exactly 63 active states.

The domain clock function:

**κ(t) = (δ(t) × stride) mod 64**

where δ(t) = t mod 64 is the intra-domain position at birth tick t, and stride satisfies gcd(stride, 63) = 1.

The session key becomes: PRNG(base_seed ⊕ κ(t))

Eve intercepts the Zookeeper broadcast and correctly computes the base seed. But the actual keystream requires κ(t), derived from the birth tick she can never observe. Her seed is correct. Her keystream is wrong.

---

## Why the Coprime Condition Is Not Optional

The 63 active states form a cyclic group Z₆₃. The domain clock walk visits states as κ_k = (k × stride) mod 63. The orbit length is 63 / gcd(stride, 63).

A stride that shares a factor with 63 produces a short orbit. stride = 7 gives gcd(7, 63) = 7, orbit length 9 — Eve's search space collapses to 9 candidates, roughly 3 bits. stride = 11 gives gcd(11, 63) = 1, orbit length 63 — full ~6 bits of physical entropy per session.

63 = 3² × 7. Valid strides are all numbers in 1..62 not divisible by 3 or 7. By Euler's totient function, φ(63) = 36 valid strides exist — all produce a full orbit covering all 63 positions.

Verified across all 62 strides in 1..62: 36 full-orbit, 26 short-orbit. Stride 11 (recommended) confirmed valid.

---

## What Eve Actually Has

| What Eve has | What she can compute | What she is missing | Outcome |
|---|---|---|---|
| d_A from Zookeeper | d_B, base_seed | birth tick t (internal) | Keystream wrong — correct seed, wrong κ |
| Ciphertext stream | OTP analysis | κ(t) → 63 candidates | ~6 bits brute force, no plaintext oracle |
| Multiple sessions | Correlate κ across sessions | t advances independently per session | No correlation — coprime walk is independent |

Across 315 wrong-κ decryption attempts in testing: 0 accidental recoveries.

---

## Three Independent Layers, Three Independent Adversaries

| Layer | Mechanism | Adversary defeated |
|---|---|---|
| L1 — Geometric | d_A + d_B ≡ 0 (mod p) | Shor's algorithm, factoring, classical brute-force |
| L2 — Physical | Z₃ OTP + tension ratchet + clock-drift detection | Wire interception, MitM, replay |
| L3 — Temporal | κ(t) = (δ(t) × stride) mod 64 | Zookeeper broadcast intercept |

The three layers are orthogonal. Each defeats a different class of adversary. An attacker who defeats one layer still faces two others — and the layers compound rather than stack additively.

---

## Security as Ontological Impossibility

Standard post-quantum security is computational hardness: breaking the system requires solving a problem believed to be hard. The hardness is an assumption about the limits of computation.

LQC security is different in kind. The conjugate birth invariant cannot be broken by computation because it is not a computational structure. The birth tick cannot be intercepted because it is never transmitted — it is an internal clock reading that exists only inside the node at the moment of pair creation. There is no protocol change, no key size increase, no algorithmic update that gives Eve access to t. The impossibility is physical, not computational.

---

## Status

All three layers are formally derived:

- Layer 1: Conjugate birth invariant — derived, 0 violations across 100,000 lattice steps
- Layer 2: Z₃ OTP + ratchet + tamper detection — derived across experiments exp33–38
- Layer 3: Domain Clock Shield — derived, all five falsification claims passed (exp39)

The framework is theoretical. Physical implementation has not been tested. What has been tested is the mathematical and geometric structure — that the invariant holds, that the ratchet is irreversible, that the domain clock provides statistically uniform entropy independent of session history.

The working implementation is in Rust. The derivations are in the MPRC Framework booklet at [muhammadarshad.github.io/pages-mprc](https://muhammadarshad.github.io/pages-mprc).

---

*Muhammad Arshad is an independent researcher developing the MPRC (Movement-Position-Rotation-Charge) framework — a discrete geometric theory of nature built on the Z₂₅₆ ring structure.*