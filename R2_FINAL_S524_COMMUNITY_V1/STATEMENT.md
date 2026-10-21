# Statement

All statements are in Lean, in `project/ClayStatement/Fefferman.lean` (Fefferman's wording, with one fidelity note per departure from a literal reading) and, for the authors' own formulation, `project/ComparatorChallenges/NavierStokesComplete.lean`. `Clay.NavierStokes.ClayNavierStokes := StatementA ∨ StatementB ∨ StatementC ∨ StatementD`.

## Checked by the Comparator (permitted axioms: `propext`, `Classical.choice`, `Quot.sound`; Lean default kernel and `nanoda`)
| Configuration | Theorem(s) | Result in the publisher's run |
|---|---|---|
| `ClayFefferman` | NavierStokes.ClayChallenge.clay_navier_stokes_fefferman : Clay.NavierStokes.ClayNavierStokes (A ∨ B ∨ C ∨ D, proved through C) | exit 0, both kernels accept |
| `ClayFeffermanViaD` | NavierStokes.ClayChallenge.clay_navier_stokes_fefferman_via_D : Clay.NavierStokes.ClayNavierStokes (proved through D) | exit 0, both kernels accept |
| `NavierStokesComplete` | NavierStokes.Comparator.navier_stokes_clay_via_C and ..._via_D (the authors' formal disjunction of their OptionA..OptionD) | exit 0, both kernels accept |
| `ClayC` | NavierStokes.ClayC.clay_C : Clay.NavierStokes.StatementC (alternative (C) alone) | exit 0, both kernels accept |
| `ClayD` | NavierStokes.ClayD.clay_D : Clay.NavierStokes.StatementD (alternative (D) alone) | exit 0, both kernels accept |

## Bridge between the two formulations (`project/ClayStatement/`)
`optionA_iff_statementA`, `optionB_iff_statementB` (both directions); `optionC_imp_statementC`, `optionD_imp_statementD` and the converses `statementC_imp_optionC`, `statementD_imp_optionD` in `BridgeConverse` (also in the main build). These are **logical equivalences between two encodings** in Lean (`↔` and `→`); they are **not** definitional equality, and they are not independent confirmation that either encoding faithfully transcribes Fefferman's published prose.

## Shipped as statement files only (no solution exists)
`ComparatorChallenges/ClayA.lean` (Fefferman's (A)) and `ClayB.lean` (Fefferman's (B)). They compile with a `sorry` body, as Comparator challenge files do. **(A) and (B) are open.**

## What the disjunction result means
Proving `A ∨ B ∨ C ∨ D` through (C) or (D) does **not** prove (A) or (B). The formal (C) and (D) quantify over every ν > 0, which is stronger than Fefferman's "take ν > 0".
