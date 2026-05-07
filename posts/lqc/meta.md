# Publishing Metadata — LQC Post

## Post Identity

| Field | Value |
|---|---|
| Title | The Key That Was Never Sent: Post-Quantum Cryptography from Ring Geometry |
| Subtitle | A new communication channel where key agreement requires no transmission |
| Author | Muhammad Arshad |
| Date written | 2026-05-03 |
| Source file | `lqc.md` |
| Canonical URL | https://muhammadarshad.github.io/pages-mprc/ |

---

## Artifacts

| File | Platform | Status |
|---|---|---|
| `lqc.md` | Source (canonical) | ✅ Ready |
| `medium.md` | Medium | ✅ Ready to paste |
| `substack.md` | Substack | ✅ Ready to paste |
| `images/banner.svg` | Post cover image (1200×630) | ✅ Ready |
| `images/fig1-conjugate-birth.svg` | Figure 1 — Conjugate Birth Invariant (900×480) | ✅ Ready |
| `images/fig2-three-layers.svg` | Figure 2 — Three Security Layers (900×560) | ✅ Ready |
| `images/fig3-domain-clock.svg` | Figure 3 — Z₂₅₆ Domain Clock Shield (900×520) | ✅ Ready |

### Image placement in post

| Image | Insert after section |
|---|---|
| `banner.svg` | Post header / cover image |
| `fig1-conjugate-birth.svg` | After "The Conjugate Birth Invariant" section |
| `fig2-three-layers.svg` | After "Three Independent Layers, Three Independent Adversaries" section |
| `fig3-domain-clock.svg` | After "Layer 3: The Birth Tick Is Not on the Wire" section |

### Platform image notes

**Medium:** Upload SVGs via the image icon in the editor (drag & drop works). Add alt text for accessibility.

**Substack:** SVGs are not directly supported — export each to PNG at 2× resolution (1800×1260 for banner, 1800×960 for figures) before uploading. Use a browser to open the SVG and screenshot, or use Inkscape/Illustrator to export.

---

## Medium

**Publication target:** Self-publish or submit to *Towards Data Science* / *The Startup*

**Tags (up to 5):**
- Post-Quantum Cryptography
- Cryptography
- Mathematics
- Security
- Quantum Computing

**Steps:**
1. Go to medium.com → Write a story
2. Paste contents of `medium.md`
3. Set title and subtitle manually (Medium doesn't parse front-matter)
4. Add canonical URL in Story Settings → Advanced Settings → Canonical Link
5. Add tags above
6. Publish or submit to publication

**Canonical link to set:** `https://muhammadarshad.github.io/pages-mprc/`

---

## Substack

**Section:** Science & Technology (or create a dedicated "MPRC Framework" section)

**Tags:** cryptography, post-quantum, mathematics, security, ring theory, independent research

**Steps:**
1. Go to your Substack dashboard → New Post
2. Paste contents of `substack.md`
3. Set title: *The Key That Was Never Sent: Post-Quantum Cryptography from Ring Geometry*
4. Set subtitle: *A new communication channel where key agreement requires no transmission — not classical, not quantum*
5. Add tags in post settings
6. Choose: Free post (recommended for reach) or Paid
7. Send as newsletter or publish only

---

## LinkedIn

**Suitability:** YES — "key born into nodes, never transmitted" is a strong and unique hook for a professional audience interested in cryptography, security, and emerging tech.

**Format:** Short post, ~1300 characters. No markdown required — plain text only on LinkedIn.

**Suggested post:**

---

The future of cryptography doesn't transmit keys.

Current quantum key distribution (BB84, E91) still relies on sending quantum states over a channel. An eavesdropper can probe that channel.

The MPRC Framework proposes something different: a protocol where the shared key is *derived* at each node independently, from a common prime p and local depth values. No key is ever on the wire. There is nothing to intercept.

The math: Alice chooses depth d_A, Bob chooses d_B, such that d_A + d_B ≡ 0 (mod p). Both independently derive the same session key: a pair of ring states on the Z₂₅₆ geometric lattice. The conjugate birth invariant makes the key unique. A replay gives a different key. An eavesdropper who captures the channel sees... nothing useful.

Three layers of security:
→ Ring geometry: no RSA/ECC assumptions
→ Domain Clock: session-bound, replay-immune
→ Birth Tick: never transmitted

The key was never sent. It was born simultaneously at both ends.

Full framework: muhammadarshad.github.io/pages-mprc

#PostQuantumCryptography #Cryptography #QuantumSecurity #Mathematics #Cybersecurity

---

**Character count:** ~1200 (within LinkedIn limit)

---

## Content Notes

- Tables render natively on both platforms — no changes needed
- Bold math expressions (e.g. **d_A + d_B ≡ 0 (mod p)**) will render as bold text; consider using Medium's equation tool for the key formulas if desired
- The Status section bullets use `**bold:**` syntax — renders correctly on both platforms
- No images required; post is self-contained as text

---

## Series Context

This post covers **Model 3 (LQC)** of the MPRC Framework. Suggested series order for future posts:

| Post # | Topic | Source material |
|---|---|---|
| 1 | The Z₂₅₆ Ring: Nature's Own Arithmetic | `docs/work/model-1/` |
| 2 | Atomic Stability from Ring Geometry | `docs/MPRC_Framework_QH4_Atomic_Prediction.tex` |
| 3 | The Key That Was Never Sent (LQC) | `posts/lqc/lqc.md` ← **this post** |
| 4 | Gravity Without Curves | `mprc-artemis-prediction/paper/` |
| 5 | SILIQ: Self-Integrating Liquid Crystal | `docs/work/model-4/` |
