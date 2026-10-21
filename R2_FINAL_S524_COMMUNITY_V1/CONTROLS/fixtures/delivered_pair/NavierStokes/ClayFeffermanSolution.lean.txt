import ClayStatement.Bridge
import NavierStokes.ComparatorSolution

/-!
# Solution: Fefferman's literal A ∨ B ∨ C ∨ D, through (C)

Proved through (C): the authors' breakdown on ℝ³, carried to Fefferman's
literal statement by the bridge. A second proof goes through (D).
This is not progress on (A) or (B).
-/

namespace NavierStokes.ClayChallenge
open Clay.NavierStokes

theorem clay_navier_stokes_fefferman : ClayNavierStokes :=
  Or.inr (Or.inr (Or.inl
    (Bridge.optionC_imp_statementC NavierStokes.Comparator.navier_stokes_breakdown_R3)))

theorem clay_navier_stokes_fefferman_via_D : ClayNavierStokes :=
  Or.inr (Or.inr (Or.inr
    (Bridge.optionD_imp_statementD NavierStokes.Comparator.navier_stokes_breakdown_periodic)))

end NavierStokes.ClayChallenge
