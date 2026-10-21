# KTS Global · Lean 4 · Navier–Stokes research packages

Research packages published by KTS Global. None is a claimed solution of a Clay Millennium Problem, and none has Clay Institute recognition or independent specialist review.

## Releases

| Release | Package | Identifiers |
|---|---|---|
| [`s437-v1`](https://github.com/kts-global/lean-proofs-public/releases/tag/s437-v1) | S437: Lean 4.34.1 port and rebuild of OpenAI's NavierStokesAndEuler formalization (Clay alternatives C and D) | DOI 10.5281/zenodo.23448690 · Wikidata Q141761720 |
| [`r2-r3-v1`](https://github.com/kts-global/lean-proofs-public/releases/tag/r2-r3-v1) | R2/R3 community verification package: Fefferman-style statement and bridge layer, per-alternative packages, public verification script and receipts | No DOI issued yet |

Each release is a separate, citable artifact. Cite the release tag you used. Do not use the S437 DOI for R2/R3.

## Inherited mathematics

The mathematics and the Lean formalization are OpenAI's: [`openai/NavierStokesAndEuler`](https://github.com/openai/NavierStokesAndEuler) at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (Apache-2.0). Toolchain: Lean 4.34.1, Mathlib `d13f23b`.

## S437: port and rebuild

- 21 Lean modules edited (all under `NavierStokes/`), plus the pin files `lean-toolchain`, `lakefile.toml` and `lake-manifest.json`.
- Challenge statements (`ComparatorChallenges/NavierStokes.lean`) unchanged from upstream.
- Checked: `NavierStokes.Comparator.navier_stokes_breakdown_R3` and `..._breakdown_periodic` (alternatives C and D), on Lean's default kernel and nanoda, axioms `propext`, `Classical.choice`, `Quot.sound` only.
- Full change list: `CHANGES.md`. Receipts: `RECEIPTS/`. Statement: `STATEMENT.md`. Provenance: `PROVENANCE.json`.
- Review packages (`REVIEW_PACKAGE_R1`, `REVIEW_PACKAGE_R2`, `CANDIDATE_R2`, `COMMUNITY_TEST_PACKAGE`, `COMMUNITY_TEST_PACKAGE_V3`) are the authors' own analysis.

## R2/R3: statement, bridge and community verification

Folder: `R2_FINAL_S524_COMMUNITY_V1/`. Contribution: Tim Jacobs, KTS Global (ORCID [0009-0008-7130-1448](https://orcid.org/0009-0008-7130-1448)).

- Adds the Fefferman-style statement and bridge layer (`Bridge`, `BridgeConverse`), the R3 per-alternative files, a public verification script and receipts.
- Proves the encoded forms of alternatives C and D for forced Navier–Stokes, and A ∨ B ∨ C ∨ D through them. Alternatives A and B are shipped as statement files only.
- Comparator on both kernels: ClayFefferman, ClayFeffermanViaD, NavierStokesComplete, ClayC and ClayD, all exit 0. All 40,986 theorems in the 620-module closure depend only on the three standard axioms.
- Verify on Ubuntu 24.04 with `VERIFY.sh`; see `RESTORE_AND_VERIFY.md` in that folder.

## What is not claimed

- No claim about alternatives A or B; they remain open.
- No claim that the Lean encoding matches Fefferman's published prose; this has not been independently reviewed.
- No Clay acceptance, original discovery of the underlying mathematics, or independent replication. Verification runs are publisher-executed on one platform (Ubuntu 24.04 x86_64). See `KNOWN_LIMITS.md`.

## Licence

Upstream material remains under its Apache-2.0 licence. Files added by KTS Global are published under the Apache-2.0 `LICENSE` at the root of this repository. The CHAOS implementation is not distributed or licensed by these packages.
