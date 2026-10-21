import ClayStatement.BridgeEquiv
import NavierStokes.ComparatorCompleteSolution

/-!
# Optional converse directions for (C) and (D)

Added by the builder (S522). The delivered `Bridge.lean` states (C) and (D) in the direction the solve needs
(authors' option → Fefferman's statement) and calls the reverse directions optional. The equivalences in
`BridgeEquiv` already give them, so Fefferman's (C) and (D) and the authors' `OptionC` and `OptionD` correspond in
both directions, as (A) and (B) do. Nothing imports this file; it is not used by either solution.
-/

namespace Clay.NavierStokes.BridgeConverse
open Clay.NavierStokes Clay.NavierStokes.BridgeEquiv

theorem statementC_imp_optionC : StatementC → NavierStokes.Comparator.OptionC := by
  intro h ν hν
  obtain ⟨u0, f, hs, hd, hF, hNot⟩ := h ν hν
  refine ⟨u0, fun x t => f t x, (initR3_iff u0).mpr ⟨hs, hd⟩, (forceR3_iff (fun x t => f t x)).mpr hF, ?_⟩
  intro hSol
  exact hNot ((solR3_iff ν u0 (fun x t => f t x)).mp hSol)

theorem statementD_imp_optionD : StatementD → NavierStokes.Comparator.OptionD := by
  intro h ν hν
  obtain ⟨u0, f, hs, hp, hF, hNot⟩ := h ν hν
  refine ⟨u0, fun x t => f t x, (initTorus_iff u0).mpr ⟨hs, hp⟩, (forceTorus_iff (fun x t => f t x)).mpr hF, ?_⟩
  intro hSol
  exact hNot ((solTorus_iff ν u0 (fun x t => f t x)).mp hSol)

end Clay.NavierStokes.BridgeConverse
