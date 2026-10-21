import ClayStatement.BridgeEquiv
import NavierStokes.ComparatorCompleteSolution

/-!
# Bridge: the authors' formal options and Fefferman's literal statements

These are the obligations that connect the authors' `OptionA`..`OptionD`
(S456 challenge file, built from the authors' own definitions) to the
literal Fefferman statements in `ClayStatement.Fefferman`.

A and B are linked in both directions. That gives a formal statement
correspondence, not a proof of either: both remain open problems.

C and D need only the direction Option → Statement, which is what the solve
uses. The reverse directions are optional.

Build note (S522). The delivered file imported `ComparatorChallenges.NavierStokesComplete`. A module that also
imports the S412 `NavierStokes.ComparatorSolution` then fails to load (`NavierStokes.ComparatorDefinitions` redeclares
the challenge's `NavierStokes.Comparator.*` names). This file imports the S456 solution module instead; its
`OptionA`..`OptionD` are textually identical to the challenge module's (S456 solution header). No statement below
and no clause of either side was changed.

Proof ingredients, in the modules this file imports:
- `BridgeLemmas`: coordinate-sum divergence, Laplacian, gradient and (u·∇)u equal trace, Mathlib Δ, gradient and `fderiv`;
- `BridgeSwap`: the `(t, x)` / `(x, t)` argument order, smoothness and iterated-derivative norms across `Prod.swap`;
- `BridgeEquiv`: integrable ‖u‖² plus a bound iff `MemLp 2` plus a bound, and the data-condition clauses.
-/

namespace Clay.NavierStokes.Bridge
open Clay.NavierStokes
open Clay.NavierStokes.BridgeEquiv

-- Statement correspondence for the open problems (both directions)
theorem optionA_iff_statementA : NavierStokes.Comparator.OptionA ↔ StatementA := by
  constructor
  · intro h ν hν u0 hs hd
    exact (solR3_iff ν u0 0).mp (h ν hν u0 ((initR3_iff u0).mpr ⟨hs, hd⟩))
  · intro h ν hν u0 hI
    have h1 := (initR3_iff u0).mp hI
    exact (solR3_iff ν u0 0).mpr (h ν hν u0 h1.1 h1.2)

theorem optionB_iff_statementB : NavierStokes.Comparator.OptionB ↔ StatementB := by
  constructor
  · intro h ν hν u0 hs hp
    exact (solTorus_iff ν u0 0).mp (h ν hν u0 ((initTorus_iff u0).mpr ⟨hs, hp⟩))
  · intro h ν hν u0 hI
    have h1 := (initTorus_iff u0).mp hI
    exact (solTorus_iff ν u0 0).mpr (h ν hν u0 h1.1 h1.2)

-- The direction the solve needs
theorem optionC_imp_statementC : NavierStokes.Comparator.OptionC → StatementC := by
  intro h ν hν
  obtain ⟨u0, f', hI, hF, hNot⟩ := h ν hν
  obtain ⟨hs, hd⟩ := (initR3_iff u0).mp hI
  exact ⟨u0, fun t x => f' x t, hs, hd, (forceR3_iff f').mp hF, fun hSol => hNot ((solR3_iff ν u0 f').mpr hSol)⟩

theorem optionD_imp_statementD : NavierStokes.Comparator.OptionD → StatementD := by
  intro h ν hν
  obtain ⟨u0, f', hI, hF, hNot⟩ := h ν hν
  obtain ⟨hs, hp⟩ := (initTorus_iff u0).mp hI
  exact ⟨u0, fun t x => f' x t, hs, hp, (forceTorus_iff f').mp hF, fun hSol => hNot ((solTorus_iff ν u0 f').mpr hSol)⟩

end Clay.NavierStokes.Bridge
