# R3 alternative packages (A, B, C, D)

| Alternative | Content | Status | Evidence |
|---|---|---|---|
| (A) | `ComparatorChallenges/ClayA.lean` (statement file; `sorry` is required by the Comparator format) | **OPEN. No solution exists.** | compiles as a statement file (`logs/S10.*`) |
| (B) | `ComparatorChallenges/ClayB.lean` (statement file) | **OPEN. No solution exists.** | compiles as a statement file |
| (C) | `ClayC.lean`, `ClayC.json`, `NavierStokes/ClayCSolution.lean` | proved; Comparator on both kernels: exit 0 | `logs/K_ClayC.*` |
| (D) | `ClayD.lean`, `ClayD.json`, `NavierStokes/ClayDSolution.lean` | proved; Comparator on both kernels: exit 0 | `logs/K_ClayD.*` |

(C) is carried from the authors' `navier_stokes_breakdown_R3` and (D) from `navier_stokes_breakdown_periodic` through the checked bridge. The delivered solution files lacked `import NavierStokes.ComparatorSolution`; the delivered files are in `evidence/` and the shipped ones carry that one added import line. The delivered per-package READMEs are `*/README.delivered.md`. A proof of ¬(A) or ¬(B), if one is ever found, would be a separate package.
Controls specific to R3: `R3_C_without_F5`, `R3_D_force_bound_weakened`, `R3_C_sorry_solution` (`CONTROLS/`).
