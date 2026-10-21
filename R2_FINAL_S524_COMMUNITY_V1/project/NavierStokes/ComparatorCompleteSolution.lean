import NavierStokes.ComparatorR3Theorem
import NavierStokes.ComparatorTheorem

/-!
# Complete Navier–Stokes statement `A ∨ B ∨ C ∨ D` (S456)

The disjunction follows from the already-proved option (C), and separately from option (D), via the authors' adapters.
The definitions `OptionA`..`OptionD` are textually identical to the challenge module's.
-/

namespace NavierStokes.Comparator

local notation "ℝ³" => EuclideanSpace ℝ (Fin 3)

/-- Fefferman alternative (A) as a proposition: for every positive viscosity and every
initial velocity satisfying the decay condition, with zero force, a smooth bounded-energy
solution exists on ℝ³ (the form of `navier_stokes_existence_and_smoothness_R3`). -/
def OptionA : Prop :=
  ∀ (nu : ℝ), nu > 0 → ∀ (u₀ : ℝ³ → ℝ³), InitialVelocityConditionDecay u₀ →
    ∃ v p, NavierStokesExistenceAndSmoothnessRn nu u₀ (f := 0) v p

/-- Fefferman alternative (B) as a proposition: the periodic analogue of (A). -/
def OptionB : Prop :=
  ∀ (nu : ℝ), nu > 0 → ∀ (u₀ : ℝ³ → ℝ³), InitialVelocityConditionPeriodic u₀ →
    ∃ v p, NavierStokesExistenceAndSmoothnessPeriodic nu u₀ (f := 0) v p

/-- Fefferman alternative (C) as a proposition: breakdown on ℝ³ for every positive
viscosity (the form of `navier_stokes_breakdown_R3`). -/
def OptionC : Prop :=
  ∀ (nu : ℝ), nu > 0 →
    ∃ (u₀ : ℝ³ → ℝ³) (f : ℝ³ → ℝ → ℝ³),
    InitialVelocityConditionDecay u₀ ∧ ForceConditionDecay f ∧
    ¬ (∃ v p, NavierStokesExistenceAndSmoothnessRn nu u₀ f v p)

/-- Fefferman alternative (D) as a proposition: breakdown on ℝ³/ℤ³ for every positive
viscosity (the form of `navier_stokes_breakdown_periodic`). -/
def OptionD : Prop :=
  ∀ (nu : ℝ), nu > 0 →
    ∃ (u₀ : ℝ³ → ℝ³) (f : ℝ³ → ℝ → ℝ³),
    InitialVelocityConditionPeriodic u₀ ∧ ForceConditionPeriodic f ∧
    ¬ (∃ v p, NavierStokesExistenceAndSmoothnessPeriodic nu u₀ f v p)

/-- The complete Navier–Stokes statement `A ∨ B ∨ C ∨ D`, closed through (C). -/
theorem navier_stokes_clay_via_C : OptionA ∨ OptionB ∨ OptionC ∨ OptionD :=
  Or.inr (Or.inr (Or.inl (fun nu hnu => ComparatorBridge.navier_stokes_breakdown_R3 nu hnu)))

/-- The complete Navier–Stokes statement `A ∨ B ∨ C ∨ D`, closed through (D). -/
theorem navier_stokes_clay_via_D : OptionA ∨ OptionB ∨ OptionC ∨ OptionD :=
  Or.inr (Or.inr (Or.inr (fun nu hnu => ComparatorBridge.navier_stokes_breakdown_periodic nu hnu)))

end NavierStokes.Comparator

#print axioms NavierStokes.Comparator.navier_stokes_clay_via_C
#print axioms NavierStokes.Comparator.navier_stokes_clay_via_D
#print axioms NavierStokes.Comparator.OptionA
#print axioms NavierStokes.Comparator.OptionB
