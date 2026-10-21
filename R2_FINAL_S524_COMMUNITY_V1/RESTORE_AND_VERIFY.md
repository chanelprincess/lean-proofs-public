# Restore and verify

## Prerequisites (declared, not installed by `VERIFY.sh`)
Native **Ubuntu 24.04 x86_64** (the only platform the publisher ran this on), a Landlock-enabled kernel, `git`, `gcc`, Rust (`cargo`, `rustc`), Go (`GOTOOLCHAIN=local`), `python3` ≥ 3.9, `/usr/bin/time`, and `elan` with the toolchain `leanprover/lean4:v4.34.1` already installed (`elan toolchain install leanprover/lean4:v4.34.1`). At least **30 GB** free disk at the work directory, network access to the public sources below, and an **open-file limit of at least 8192** (`VERIFY.sh` raises the soft limit to the hard limit and refuses to continue if it is still too low: the Mathlib cache restore opens many files at once on many-core machines).
Declared network use: `github.com` (mathlib4, nanoda_lib, landrun, upstream NavierStokesAndEuler and the pinned Lake dependencies), crates.io and the Go module proxy (for the two tools), and the public Mathlib build cache (`lake exe cache get`). **A cold download of the Mathlib cache was not part of the publisher's run**: the machine already held the cache for the pinned revision.

## Run
```
./VERIFY.sh /path/to/a/fresh/empty/directory      # the directory must not exist or must be empty; nothing outside it is written except the usual per-user Mathlib cache
```
Output: `results.json`, `SUMMARY.md`, `results.tsv` and `logs/` in that directory. Exit status 0 only if every required check passed; a required stage that did not run counts as failed.

## Stages
- `C0` (16 s): disposable copy of the built tree for the controls
- `C1` (1229 s): Lean-level controls and comparator mutation controls (disposable copy)
- `C2` (8 s): source-binding self-test (tampered added/modified file, deleted file, unlisted extra file)
- `K_ClayC` (879 s): Comparator: ComparatorChallenges/ClayC.json (Lean default kernel and nanoda)
- `K_ClayD` (835 s): Comparator: ComparatorChallenges/ClayD.json (Lean default kernel and nanoda)
- `K_ClayFefferman` (870 s): Comparator: ComparatorChallenges/ClayFefferman.json (Lean default kernel and nanoda)
- `K_ClayFeffermanViaD` (868 s): Comparator: ComparatorChallenges/ClayFeffermanViaD.json (Lean default kernel and nanoda)
- `K_NavierStokesComplete` (856 s): Comparator: ComparatorChallenges/NavierStokesComplete.json (Lean default kernel and nanoda)
- `P0` (3 s): prerequisites, platform and network
- `S1` (0 s): package input integrity (INPUTS.sha256)
- `S10` (22 s): build every claimed solution module and the statement-only challenge modules explicitly
- `S11` (2 s): upstream checkout at the pinned revision
- `S12` (1 s): source binding: upstream + shipped patch + listed extra files == shipped project (added and modified files)
- `S13` (18 s): integrity sweep (sorry, admit, axiom, native_decide, reduceBool, implemented_by, extern, unsafe, ...)
- `S14` (0 s): route coverage: every proved route is named by a Comparator configuration
- `S15` (35 s): theorem bindings: each configuration's theorems exist in its solution module within the permitted axioms
- `S16` (342 s): axiom enumeration over the whole claimed closure
- `S17` (14 s): Comparator trial projects (expected exits 0, 1, 0, 1)
- `S2` (0 s): copy the project to the workdir
- `S3` (91 s): toolchain and dependency pins
- `S4` (23 s): build nanoda_bin from the pinned source
- `S5` (3 s): build landrun from the pinned source
- `S6` (42 s): restore Mathlib build cache (public cache)
- `S7` (8 s): build lean4export; restore its toolchain file
- `S8` (12 s): build the Comparator
- `S9` (752 s): default build (lake build)

Pinned public sources: `lean-toolchain: leanprover/lean4:v4.34.1`; `dependency Comparator     rev 19e111e2141cf333c7daff0f64c5f24acc91dd2e  https://github.com/leanprover/comparator.git`; `dependency mathlib        rev d13f23b723b8a846827a245b89c10fc7d3f11612  https://github.com/leanprover-community/mathlib4.git`; `dependency lean4export    rev cacf989bd75f608700820f6afc595f32e7a99a4d  https://github.com/leanprover/lean4export`; `dependency plausible      rev 118aa17ee84656b8bd727fef7c458ee8c833385c  https://github.com/leanprover-community/plausible`; `dependency LeanSearchClient rev ddf04cf3949fa556442341e87d47f9f6e6074707  https://github.com/leanprover-community/LeanSearchClient`; `dependency importGraph    rev e928b72544873815af278d38681b31c0293588e3  https://github.com/leanprover-community/import-graph`; `dependency proofwidgets   rev 106ff4fafc74ef4ac99d81dbf3ab399118f497a5  https://github.com/leanprover-community/ProofWidgets4`; `dependency aesop          rev 355695d523e41d0554926416cba2a2b3544fbbc9  https://github.com/leanprover-community/aesop`; `dependency Qq             rev 6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259  https://github.com/leanprover-community/quote4`; `dependency batteries      rev f2effa3d803fda822b1f97b806c47cf2adfbcbc2  https://github.com/leanprover-community/batteries`; `dependency Cli            rev e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204  https://github.com/leanprover/lean4-cli`
Upstream revision for the source-binding check: `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (`https://github.com/openai/NavierStokesAndEuler`).

## What the script guarantees about itself
It refuses an existing non-empty work directory; it checks prerequisites and network before any expensive work; it never pipes a checker's exit status away (each stage's exit code and the Comparator's own exit status are recorded); it builds `nanoda_bin` and `landrun` from the pinned sources; **`lean4export`'s `lean-toolchain` file is edited only around that package's own build and restored afterwards, also on failure and on interruption, with a check that the dependency checkout is clean** (leaving it edited makes Lake warn on every later command); success is never inferred from a single "okay" line: the Comparator's exit status and **both** kernels' acceptance lines are required.

## Windows
`VERIFY.ps1 -WorkDirLinux ~/r2_verify_run1` launches the same script inside a WSL2 Ubuntu distribution. This is **not** native Windows verification; it was parsed and dry-run on Windows but not run against a working WSL2 Ubuntu by the publisher.

## The publisher's run: environment
- free disk at WORKDIR: 54 GB (need >= 30)
- Linux 7.0.0-34-generic x86_64
- PRETTY_NAME="Ubuntu 24.04.5 LTS"
- cores: 88 (jobs for parallel stages: 32)
- MemTotal:       396127476 kB
- git version 2.43.0
- gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
- cargo 1.99.0 (5f94df478 2026-08-27)
- rustc 1.99.0 (b940084d7 2026-09-28)
- go version go1.27.2 linux/amd64
- Python 3.12.3
- Landlock in the kernel LSM list: landlock
