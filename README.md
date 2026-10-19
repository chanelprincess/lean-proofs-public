# KTS Global · Lean 4 · Navier–Stokes C/D port (S437)

Pre-release research package. Not a claimed solution of any Clay problem.

## What this is
A corrected and rebuilt port, to Lean 4.34.1 and Mathlib `d13f23b`, of OpenAI's Lean formalization
[`openai/NavierStokesAndEuler`](https://github.com/openai/NavierStokesAndEuler) at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (Apache-2.0).
The mathematics and the Lean formalization are OpenAI's. This repository's contribution is the port, the rebuild and the review material listed below.

## What was changed relative to upstream
- 21 Lean modules edited (all under `NavierStokes/`), plus the three pin files `lean-toolchain`, `lakefile.toml` and `lake-manifest.json`.
- 3 files added: `DEPENDENCY_CLOSURE.json`, `RESTORE_AND_VERIFY.md`, `UPSTREAM_PROVENANCE.json`. Upstream `.gitignore` not carried over.
- Every other file (2,644 of 2,668 shared) is byte-identical to upstream. The Euler library is unchanged.
- An import-graph scan estimates that about 418 NavierStokes modules depend on the edited ones and were therefore rebuilt and re-verified; the pin changes rebuild all 2,659 modules.
- The challenge statements (`ComparatorChallenges/NavierStokes.lean`) are unchanged from upstream.
- Full list of edited files: `CHANGES.md`.

## What was checked
- Declarations: `NavierStokes.Comparator.navier_stokes_breakdown_R3` and `NavierStokes.Comparator.navier_stokes_breakdown_periodic` (Clay alternatives C and D).
- Kernels: Lean default and nanoda. Axioms: `propext`, `Classical.choice`, `Quot.sound` only.
- Pins: Mathlib `d13f23b`, Comparator `19e111e`, lean4export `cacf989`. Executed on Ubuntu 24.04.5 x86_64 only.
- Receipts: `RECEIPTS/`; statement: `STATEMENT.md`; provenance: `PROVENANCE.json`.

## Review packages
`REVIEW_PACKAGE_R1`, `REVIEW_PACKAGE_R2`, `CANDIDATE_R2`, `COMMUNITY_TEST_PACKAGE` and `COMMUNITY_TEST_PACKAGE_V3` contain a clause-by-clause comparison of the Lean statements with the official problem text, plus reproduction material. This is the authors' own analysis. No independent referee or expert review has been obtained.

## What is not claimed
- Correspondence between the Lean definitions and the official Clay problem statement has not been independently reviewed.
- No claim about alternatives A or B. They are outside this release.
- No claim of Clay Institute recognition, original discovery, or independent evaluation.
- Not a new porting result: the port and its historical two-kernel check pre-existed this fresh full build.

## Identifiers
Release `s437-v1` · DOI [10.5281/zenodo.23448690](https://doi.org/10.5281/zenodo.23448690) · Wikidata Q141761720 · License Apache-2.0.
