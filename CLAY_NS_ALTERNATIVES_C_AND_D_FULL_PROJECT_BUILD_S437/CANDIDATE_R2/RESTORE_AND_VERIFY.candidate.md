# Restore and verify: candidate distribution R2 of the NS Lean project

This file replaces the t6 package's `RESTORE_AND_VERIFY.md`, which did not say where `nanoda_bin` and `landrun` come from. The change is recorded in `CANDIDATE_CHANGES.md`. All Lean sources and project configuration in this package are byte-identical to the t6 package (job `s437.lpb.t6.full`); only documentation differs.

## What this package establishes, and what it does not
- Checked claim: Lean kernel acceptance (Lean default kernel and nanoda) of `NavierStokes.Comparator.navier_stokes_breakdown_R3` and `NavierStokes.Comparator.navier_stokes_breakdown_periodic` against `ComparatorChallenges/NavierStokes.lean`, with axioms within `propext`, `Classical.choice`, `Quot.sound`.
- Not established by this file: correspondence of those statements to the official Clay problem (a coordinator-authored assessment exists in the review package; it is not an independent referee report), the correctness of the informal paper, Windows or offline restoration. `UPSTREAM_PROVENANCE.json` is unchanged from the t6 package; its correspondence sentence predates that assessment.
- Whether a particular restoration of this exact package succeeded is recorded in the returned job result named in `CANDIDATE_CHANGES.md`. This file does not assert it.

## Prerequisites (declared, not installed by this procedure)
- Linux x86_64 with a Landlock-enabled kernel (landrun uses Landlock). Tested platform: Ubuntu 24.04.5, kernel 7.0.0-34-generic. No other platform is claimed.
- Network access for restoration (git clones, crates, Go modules, Mathlib cache). An offline restoration is not provided or tested.
- `git`, a C compiler (`gcc`), Rust (`cargo`, `rustc`; observed 1.99.0 stable), Go (observed go1.27.2; use `GOTOOLCHAIN=local`), and `elan` with `leanprover/lean4:v4.34.1` installed (`lake` and `lean` on PATH through elan). Exact observed versions are in `TOOLS_CLOSURE.json`.
- Free disk space for the dependency checkouts, build products and the Mathlib cache (the amount has not been measured; do not assume a small footprint).

## Dependency cache disclosure
`lake exe cache get` downloads precompiled Mathlib and dependency `.olean` files. The Lean sources of this project are compiled from source; no precompiled project `.olean` is shipped or used. A complete source-only rebuild of Mathlib and the other dependencies is not claimed.

## Layout
Choose a scratch directory S. Unpack this package so that its top-level directory becomes `S/tree`. Create `S/bin` and put it first on PATH. All commands below run in S. Do NOT run `lake update`; do not change `lake-manifest.json`.

## Restore steps (executed in this order, numbered 1-14 by line; this block is checked verbatim by the verifying runner)
```restore-steps
git clone https://github.com/robsimmons/nanoda_lib nanoda_lib
git -C nanoda_lib checkout 68d5ca9db226849b41a6fff59d796ff19d0a8840
cargo fetch --locked --manifest-path nanoda_lib/Cargo.toml
cargo build --release --offline --locked --manifest-path nanoda_lib/Cargo.toml
install -m 755 nanoda_lib/target/release/nanoda_bin bin/nanoda_bin
git clone https://github.com/zouuup/landrun landrun_src
git -C landrun_src checkout 5ed4a3db3a4ad930d577215c6b9abaa19df7f99f
(cd landrun_src && go mod download)
(cd landrun_src && GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off go build -buildvcs=false -o ../bin/landrun ./cmd/landrun)
(cd tree && lake exe cache get)
(cd tree/.lake/packages/lean4export && cp ../../../lean-toolchain lean-toolchain && lake build)
install -m 755 tree/.lake/packages/lean4export/.lake/build/bin/lean4export bin/lean4export
(cd tree && lake build Comparator/comparator)
(cd tree && lake exe comparator ComparatorChallenges/NavierStokes.json)
```
Notes on the steps:
- Steps 1-5 build `nanoda_bin` from nanoda_lib at the pinned commit with the committed `Cargo.lock` (`--locked`). Step 4 runs offline after step 3 fetched the crates.
- Steps 6-9 build `landrun` from the pinned commit; step 8 downloads the Go modules, step 9 builds offline. A newer landrun release exists; it is deliberately not used.
- Step 11 builds `lean4export` with this project's toolchain (the package pins its own toolchain; the project's `lean-toolchain` is copied over it for the build).
- Step 14 compiles the project from its Lean sources (including `ComparatorChallenges/NavierStokes.lean` and the solution closure), runs Comparator, replays the exported declarations in the Lean default kernel and in nanoda, and prints "Your solution is okay!" on success.

## Control projects (run before the challenge)
Comparator ships four control projects under `tree/.lake/packages/Comparator/tests/projects`. Copy each of `simple_match`, `simple_mismatch`, `simple_nanoda`, `simple_nanoda_mismatch` to a scratch directory, copy `tree/lean-toolchain` into it, make sure it has a `lakefile.toml` declaring libraries `Solution` and `Challenge` (name `comparatortest`), and run `lake env <path to comparator binary> config.json` there. Expected exit codes: 0, 1, 0, 1. The mismatch projects must fail; a checker that accepts them is not trusted.

## Declarations and axiom policy
Declarations: `NavierStokes.Comparator.navier_stokes_breakdown_R3`, `NavierStokes.Comparator.navier_stokes_breakdown_periodic`. Permitted axioms: `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` is not permitted. The two `sorry` tokens in `ComparatorChallenges/NavierStokes.lean` are the challenge placeholders; that file is not imported by the solution.

## Entry points
`NavierStokes/ComparatorSolution.lean` (solution), `ComparatorChallenges/NavierStokes.lean` (challenge statements), `ComparatorChallenges/NavierStokes.json` (Comparator configuration), `lakefile.toml`, `lean-toolchain`, `lake-manifest.json`, `DEPENDENCY_CLOSURE.json` (Lean package pins), `TOOLS_CLOSURE.json` (checker-tool pins and observed host versions).
