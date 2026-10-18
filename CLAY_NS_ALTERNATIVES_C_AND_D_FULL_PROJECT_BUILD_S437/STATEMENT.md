# Statement

The checked statements are the two declarations named in `ComparatorChallenges/NavierStokes.json`, whose challenge-side statements live in `PROOFS/S412_ESTATE_PORT_v4.34.1/ComparatorChallenges/NavierStokes.lean` (3 `sorry` placeholders there are the challenge file itself and are expected). The proof side is `PROOFS/S412_ESTATE_PORT_v4.34.1/NavierStokes/ComparatorSolution.lean` (0 `sorry`).

Declarations:
- `NavierStokes.Comparator.navier_stokes_breakdown_R3`
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic`

Permitted axioms: `propext`, `Classical.choice`, `Quot.sound`. Observed (independent `#print axioms` probe and the build's own output agree): exactly those three for both declarations.

Scope: this is kernel acceptance against the challenge statement. Correspondence between the Lean definitions and the official Clay problem statement has NOT been reviewed and is not claimed.
