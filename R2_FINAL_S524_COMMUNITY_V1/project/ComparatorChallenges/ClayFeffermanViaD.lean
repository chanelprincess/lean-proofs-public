import ClayStatement.Fefferman

/-!
# Comparator challenge: Fefferman's literal A ∨ B ∨ C ∨ D, route through (D)

Added by the builder (S522). The delivered `ClayFefferman` challenge states the disjunction once; the solution proves it
twice (through C and through D), but only the first theorem name is listed in that challenge's configuration. This file
states the same proposition under the solution's second theorem name so that the route through (D) is kernel-checked too.
A `sorry` here is expected, as in every Comparator challenge.
-/

namespace NavierStokes.ClayChallenge

theorem clay_navier_stokes_fefferman_via_D : Clay.NavierStokes.ClayNavierStokes := by sorry

end NavierStokes.ClayChallenge
