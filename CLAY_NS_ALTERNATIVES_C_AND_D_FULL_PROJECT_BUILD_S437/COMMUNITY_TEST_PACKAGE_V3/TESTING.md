# Testing instructions

## 1. Prerequisites (declared, not installed by the script)
Linux x86_64 with a Landlock-enabled kernel (Comparator runs the nanoda kernel under `landrun`, which uses Landlock). Tested only on Ubuntu 24.04.5.

| Tool | Tested with | Notes |
|---|---|---|
| `elan` with Lean `leanprover/lean4:v4.34.1` | 4.34.1 | `lean-toolchain` selects it; elan will install it if missing (network) |
| `git`, `gcc` | 2.43.0, 13.3.0 | |
| Rust (`cargo`, `rustc`) | 1.99.0 | builds `nanoda_bin`; `Cargo.lock` is pinned |
| Go | go1.27.2 | builds `landrun`; the script uses `GOTOOLCHAIN=local` |
| `python3` | 3.12+ | only for the script's own helper checks |
| Network | | git clones, crates, Go modules; and the Mathlib cache if you do not already have it |
| Disk | | several GB to tens of GB (not measured precisely) |

If you lack these: install `elan` (https://github.com/leanprover/elan), Rust (https://rustup.rs) and Go (https://go.dev/dl/) by their own instructions. **We did not test installing them from nothing.**

## 2. The Mathlib cache
The project pins Mathlib at revision `d13f23b723b8a846827a245b89c10fc7d3f11612` (`project/lakefile.toml`, `project/lake-manifest.json`, `project/DEPENDENCY_CLOSURE.json` agree). Step 10 runs `lake exe cache get`: if a cache for that revision exists on your machine it is reused; otherwise it downloads it. Our runs found it already present and downloaded nothing; a first-time download was **not tested**. Do not run `lake update`; the script checks that `lake-manifest.json` is unchanged at the end.

## 3. Run
```
tar xzf ns-blowup-lean-test.tar.gz
cd ns-blowup-lean-test
scripts/reproduce.sh /path/to/fresh/empty/workdir
```
Runtime: the challenge step alone took about 36 minutes in our runs; plan for roughly an hour end to end on a comparable machine.

## 4. What you should see
1. Steps 1-14 announced as `== step n/14`.
2. After step 13, four controls: `simple_match` exit 0, `simple_mismatch` exit 1, `simple_nanoda` exit 0, `simple_nanoda_mismatch` exit 1 (a mismatch control must fail; a checker that accepts it is not trusted).
3. After step 14: Comparator lines `nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`, `Your solution is okay!`.
4. The independent axiom check: each declaration depends only on `propext`, `Classical.choice`, `Quot.sound`.
5. `RESULT: PASS ...`. Any other ending prints `FAIL: ...` with the step.

The two `sorry` tokens in `project/ComparatorChallenges/NavierStokes.lean` are the challenge placeholders; that file is not imported by the solution.

## 5. The procedure by hand
`project/RESTORE_AND_VERIFY.md` lists the same 14 steps in a fenced block; `scripts/reproduce.sh` embeds exactly those commands.

## 6. What a pass means
Repeatable verification of two kernel acceptances against the challenge statements. It does not by itself establish correspondence with the official problem (see `docs/02_CORRESPONDENCE_ASSESSMENT.md`), the correctness of the informal paper, or byte-identical binaries (rebuilt checker binaries differed in length between our runs).
