Proved (Lean 4.34.1, Comparator on two kernels): the encoded forms of Fefferman's alternatives (C) and (D) for forced Navier–Stokes, and A ∨ B ∨ C ∨ D through them. Not claimed: (A) or (B); that the encoding matches Fefferman's published prose; Clay acceptance.

Inherited mathematics and formalisation: OpenAI, `openai/NavierStokesAndEuler` at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (Apache-2.0). This package adds the statement and bridge layer, the R3 per-alternative files, the public verification tools and the receipts (`UPSTREAM_AND_CONTRIBUTIONS.md`).

# Navier–Stokes, Fefferman's A ∨ B ∨ C ∨ D: a community verification package (R2 final, with the R3 alternative packages)

**Release r2-r3-v1.** The gate (no sorry outside Comparator challenge declarations, axioms, both kernels, a from-scratch rebuild with `VERIFY.sh`, sweep, disclosure) passed on this tree; see `RECEIPTS/community_run/`.

## What you can check
Lean 4.34.1 proofs, built from public sources, that the encoded forms of Fefferman's alternatives **(C)** and **(D)** hold (finite-time breakdown for forced Navier–Stokes, on ℝ³ and on the periodic torus), and that the disjunction **A ∨ B ∨ C ∨ D** follows **through (C) or (D)**. It does **not** resolve (A) or (B), which remain open: those two alternatives are shipped as statement files only.

One command, from an Ubuntu machine with the prerequisites in `RESTORE_AND_VERIFY.md`:

```
./VERIFY.sh /path/to/a/fresh/empty/directory
```

It builds the two independent checker tools from pinned public sources, builds the claimed proof closure, runs the Lean Comparator on five configurations with **both** the Lean default kernel and the independent `nanoda` kernel, enumerates the axioms of every theorem in the closure, runs the integrity sweep and the negative controls, and exits nonzero if any required check fails. It needs no proprietary software, service or credentials.

On Windows, `VERIFY.ps1` launches the same script inside a WSL2 Ubuntu distribution. That is **not** a native Windows verification, and the launcher itself has not been run against a working WSL2 installation by the publisher.

## The publisher's run (what was actually executed)
One execution of `VERIFY.sh` on native Ubuntu 24.04 (88 cores), 94 min 38 s wall clock, **all required checks passed** (`RECEIPTS/community_run/`):

| Configuration | Comparator exit | Lean default kernel | nanoda | Comparator time |
|---|---|---|---|---|
| `ComparatorChallenges/ClayFefferman.json` | 0 | accepts | accepts | 14:30.17 |
| `ComparatorChallenges/ClayFeffermanViaD.json` | 0 | accepts | accepts | 14:27.67 |
| `ComparatorChallenges/NavierStokesComplete.json` | 0 | accepts | accepts | 14:16.41 |
| `ComparatorChallenges/ClayC.json` | 0 | accepts | accepts | 14:38.80 |
| `ComparatorChallenges/ClayD.json` | 0 | accepts | accepts | 13:55.11 |

Axioms: 40,986 theorems in the 620-module claimed closure were enumerated; **none depends on any axiom outside `propext`, `Classical.choice`, `Quot.sound`**; 35,970 depend on exactly those three and 5,016 on a strict subset. Controls: 12 rejected as expected, 7 accepted as expected. Source binding: upstream + shipped patch + 8 listed extra files reproduces the shipped project file for file (15 added and 24 modified by the patch).
This is a **publisher-executed** verification, not an independent replication.

## What is and is not claimed
See `CLAIMS_AND_EVIDENCE.md` (each claim with its exact theorem or configuration, scope, evidence and status) and `KNOWN_LIMITS.md`. In short: an **encoded** statement was proved and kernel-checked; that the encoding faithfully transcribes Fefferman's published prose was **not** independently reviewed; (A) and (B) are not resolved; there is no Clay acceptance and no independent specialist review.

## Layout
`project/` the buildable Lean project (the claimed build target is `ClayStatement`, whose root imports `BridgeConverse`) · `R3_PACKAGES/` per-alternative notes and the delivered R3 files kept as evidence · `SOURCE_PATCH/` the patch against upstream and the list of added files · `TOOLS/` public verification tools (Python standard library only) · `CONTROLS/` negative and positive controls · `RECEIPTS/community_run/` the run's evidence · `INPUTS.sha256`, `PUBLIC_MANIFEST.json` integrity lists · `VERIFY.sh`, `VERIFY.ps1`.
