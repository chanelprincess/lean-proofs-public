# Controls

`run_controls.sh <disposable-tree-copy> <this directory> <output directory>` (run by `VERIFY.sh` on a copy of the built tree). Every negative control passes **only** when the intended failure text is observed; a missing tool, a network failure or an unrelated compiler error is reported as FAIL. Lean control sources are stored as `.lean.txt` / `.json.txt` so they never parse as part of the project; the runner restores them inside the disposable copy.

| id | what it guards | expected |
|---|---|---|
| REAL_chain_accepted, R3_solution_modules_accepted | the real chain and R3 solutions build, so a rejection below is about the mutant | accepted |
| R2F1_collision_rejected / R2F1_resolved_pair_accepted | two modules that each work alone must load together | rejected (`already contains`) / accepted |
| R2F2_delivered_pair_flagged / R2F2_tree_fully_covered | a proved route must be named by a configuration | flagged / covered |
| C_from_periodic_rejected | (C) "proved" from the periodic theorem | `Application type mismatch` |
| R2F4_* | weakened-target bridge: one-way accepted, converse and two-way chain rejected | as stated |
| MUT_F5_removed_disjunction, MUT_force_bound_weakened, MUT_clause_3_altered | mutated challenge statements | Comparator: `Const does not match between challenge and target '<const>'` |
| MUT_sorry_solution, R3_C_sorry_solution | a `sorry` solution | Comparator: `Illegal axiom detected: 'sorryAx'` |
| R3_C_without_F5, R3_D_force_bound_weakened | R3 challenges over mutated statements | Comparator: `Const does not match between challenge and target` |
Source-binding tamper controls are in `TOOLS/source_binding_check.py selftest` (run as stage C2). The converse failure in R2F4 is the observed failure of the converse as written, not a proof that no converse proof exists.
