# Claims and evidence

Every claim names its exact theorem or configuration, its scope, the evidence file, and a status. Status **VERIFIED (publisher run)** means the check passed in the run recorded under `RECEIPTS/community_run/`; **NOT CLAIMED** means the package does not assert it.

| # | Claim | Exact theorem / configuration | Scope | Evidence | Status |
|---|---|---|---|---|---|
| 1 | The claimed proof closure builds (default target `ClayStatement`, incl. `BridgeConverse`) | `lake build` | Lean 4.34.1, Mathlib d13f23b7, Ubuntu 24.04 | `logs/S9.*`, `results.tsv` | VERIFIED (publisher run) |
| 2 | Every claimed solution module builds explicitly | `NavierStokes.ClayFeffermanSolution`, `ComparatorCompleteSolution`, `ComparatorSolution`, `ClayCSolution`, `ClayDSolution`, `ClayStatement.Bridge`, `BridgeConverse` | as above | `logs/S10.*` | VERIFIED (publisher run) |
| 3 | A ∨ B ∨ C ∨ D (Fefferman's encoding) through (C) | `ClayFefferman.json` | encoded statement | `logs/K_ClayFefferman.*`, `logs/cmp_ClayFefferman.time` | VERIFIED (publisher run) |
| 4 | The same, through (D) | `ClayFeffermanViaD.json` | encoded statement | `logs/K_ClayFeffermanViaD.*` | VERIFIED (publisher run) |
| 5 | The authors' own formal disjunction | `NavierStokesComplete.json` | authors' encoding | `logs/K_NavierStokesComplete.*` | VERIFIED (publisher run) |
| 6 | Alternative (C) alone | `ClayC.json` (`NavierStokes.ClayC.clay_C`) | encoded statement | `logs/K_ClayC.*` | VERIFIED (publisher run) |
| 7 | Alternative (D) alone | `ClayD.json` (`NavierStokes.ClayD.clay_D`) | encoded statement | `logs/K_ClayD.*` | VERIFIED (publisher run) |
| 8 | The two encodings of each alternative are logically equivalent as stated in `STATEMENT.md` | `Bridge`, `BridgeConverse` theorems | Lean `↔` / `→` | `axioms.json` (named theorems exactly the three axioms) | VERIFIED (publisher run) |
| 9 | No theorem in the claimed closure depends on an axiom outside `propext`, `Classical.choice`, `Quot.sound` | enumeration over 620 modules / 40,986 theorems | recomputed from the package, not hardcoded | `axioms.json`, `axioms.theorems.txt` | VERIFIED (publisher run) |
| 10 | `sorry` occurs only in the Comparator statement placeholders: exactly one in each configuration-named challenge theorem, plus the two statement-only files (A, B); no `admit`, `axiom` declaration, `native_decide`, `reduceBool`, `implemented_by`, `extern`, `unsafe`, `#exit` or kernel-skipping option anywhere in the shipped Lean files | integrity sweep | all shipped `.lean` files | `sweep.json`, `logs/S13.out` | VERIFIED (publisher run) |
| 11 | Every proved route is named by a Comparator configuration | route coverage | all solution modules with a configuration | `logs/S14.out` | VERIFIED (publisher run) |
| 12 | The shipped project equals upstream `f9e8bc5b38b6` + the shipped patch + the listed extra files, covering added **and** modified files; the check rejects a tampered added file, a tampered modified file, a deleted file and an unlisted extra file | `source_binding_check.py` | the project tree | `source_binding.json`, `source_binding_selftest.json` | VERIFIED (publisher run) |
| 13 | Negative controls reject for the intended reason (mutated statements, weakened force bound, `sorry` solution, import collision, (C) from the periodic theorem, weakened-target bridge) and positive controls accept | `CONTROLS/run_controls.sh` | disposable copy | `logs/C1.out`, `controls_out/` | VERIFIED (publisher run) |
| 14 | The four standard Comparator trial projects behave as expected (exits 0, 1, 0, 1) | Comparator test projects | the pinned Comparator | `logs/S17.out` | VERIFIED (publisher run) |
| 15 | Fefferman's (A) | — | — | — | **NOT CLAIMED (open)** |
| 16 | Fefferman's (B) | — | — | — | **NOT CLAIMED (open)** |
| 17 | `Fefferman.lean` transcribes Fefferman's published prose exactly | — | — | — | **NOT CLAIMED** (no independent review) |
| 18 | Independent replication; native Windows; offline restoration; a from-source Mathlib build; byte-identical `landrun`; cold Mathlib cache download | — | — | — | **NOT CLAIMED** |
| 19 | Clay acceptance or recognition; T-ABCD complete | — | — | — | **NOT CLAIMED** |
