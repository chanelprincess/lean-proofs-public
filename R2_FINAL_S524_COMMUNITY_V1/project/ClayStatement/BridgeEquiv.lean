import ClayStatement.BridgeSwap

/-!
# Bridge lemmas, layer 3: the solution classes and data conditions

Equivalences between Fefferman's literal solution classes (`SolR3`, `SolTorus`) and data conditions
(`SmoothDivFree`, `Decay`, `PeriodicDatum`, `ForceR3`, `ForceTorus`) and the authors' structures
(`NavierStokesExistenceAndSmoothness{Rn,Periodic}`, `InitialVelocityCondition*`, `ForceCondition*`).
The authors write fields as `v x t`; Fefferman writes `u t x`. Neither side is edited.
-/

namespace Clay.NavierStokes.BridgeEquiv
open Clay.NavierStokes Clay.NavierStokes.BridgeLemmas Clay.NavierStokes.BridgeSwap
open scoped Laplacian
open MeasureTheory

theorem c2_slice_challenge (v : E3 → ℝ → E3)
    (h : ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (fun z : E3 × ℝ => v z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)))
    {t : ℝ} (ht : 0 ≤ t) : ContDiff ℝ 2 (fun y => v y t) :=
  (slice_of_strip v h ht).of_le (WithTop.coe_le_coe.2 le_top)

theorem c2_slice_fefferman (u : ℝ → E3 → E3)
    (h : ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (fun z : ℝ × E3 => u z.1 z.2) halfSpace)
    {t : ℝ} (ht : 0 ≤ t) : ContDiff ℝ 2 (u t) :=
  (slice_of_halfSpace u h ht).of_le (WithTop.coe_le_coe.2 le_top)

/-- Equation (1) in the authors' form and in Clay's coordinate-sum form agree at a C² slice. -/
theorem ns_form (ν : ℝ) (v : E3 → ℝ → E3) (p : E3 → ℝ → ℝ) (f' : E3 → ℝ → E3) (t : ℝ) (x : E3)
    (hC : ContDiff ℝ 2 (fun y => v y t)) :
    (derivWithin (fun s => v x s) (Set.Ici 0) t + fderiv ℝ (fun y => v y t) x (v x t)
        = ν • Δ (fun y => v y t) x - gradient (fun y => p y t) x + f' x t) ↔
    (derivWithin (fun s => v x s) (Set.Ici 0) t + advect (fun y => v y t) x
        = ν • lap (fun y => v y t) x - grad (fun y => p y t) x + f' x t) := by
  rw [advect_eq, lap_eq _ hC x, grad_eq]

/-- The part of the solution class shared by (A)-(D): equation (1), (2), (3) and smoothness. -/
theorem core_iff (ν : ℝ) (u0 : E3 → E3) (f' : E3 → ℝ → E3) (v : E3 → ℝ → E3) (p : E3 → ℝ → ℝ) :
    NavierStokes.Comparator.NavierStokesExistenceAndSmoothness ν u0 f' v p ↔
      (NSEq ν (fun t x => v x t) (fun t x => p x t) (fun t x => f' x t) ∧
        DivFree (fun t x => v x t) ∧ Initial (fun t x => v x t) u0 ∧
        SmoothHalf (fun t x => v x t) ∧ SmoothHalf (fun t x => p x t)) := by
  constructor
  · intro h
    have hv : ContDiffOn ℝ ((⊤ : ℕ∞) : WithTop ℕ∞) (fun z : E3 × ℝ => v z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)) :=
      h.velocity_smooth
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro t ht x
      exact (ns_form ν v p f' t x (c2_slice_challenge v hv ht)).mp (h.navier_stokes x t ht)
    · intro t ht x
      exact (div_eq (fun y => v y t) x).trans (h.div_free x t ht)
    · intro x
      exact h.initial_condition x
    · exact contDiffOn_of_strip (fun z : ℝ × E3 => v z.2 z.1) hv
    · exact contDiffOn_of_strip (fun z : ℝ × E3 => p z.2 z.1) h.pressure_smooth
  · rintro ⟨hNS, hDF, hI, hSu, hSp⟩
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro x t ht
      have hC := c2_slice_fefferman (fun t x => v x t) hSu ht
      exact (ns_form ν v p f' t x hC).mpr (hNS t ht x)
    · intro x t ht
      exact (div_eq (fun y => v y t) x).symm.trans (hDF t ht x)
    · intro x
      exact hI x
    · exact contDiffOn_to_strip (fun z : ℝ × E3 => v z.2 z.1) hSu
    · exact contDiffOn_to_strip (fun z : ℝ × E3 => p z.2 z.1) hSp

/-- Solution class on ℝ³ (A), (C): the authors' structure iff Fefferman's `SolR3`. -/
theorem solR3_iff (ν : ℝ) (u0 : E3 → E3) (f' : E3 → ℝ → E3) :
    (∃ v p, NavierStokes.Comparator.NavierStokesExistenceAndSmoothnessRn ν u0 f' v p) ↔
      SolR3 ν u0 (fun t x => f' x t) := by
  constructor
  · rintro ⟨v, p, h⟩
    have hc := (core_iff ν u0 f' v p).mp h.toNavierStokesExistenceAndSmoothness
    refine ⟨fun t x => v x t, fun t x => p x t, hc.1, hc.2.1, hc.2.2.1, hc.2.2.2.1, hc.2.2.2.2, ?_⟩
    obtain ⟨E, hE⟩ := h.globally_bounded_energy
    refine ⟨E, fun t ht => ⟨?_, hE t ht⟩⟩
    have hm := h.integrable t ht
    exact (memLp_two_iff_integrable_sq hm.aestronglyMeasurable).mp hm
  · rintro ⟨u, p, hNS, hDF, hI, hSu, hSp, ⟨C, hC⟩⟩
    have hc := (core_iff ν u0 f' (fun x t => u t x) (fun x t => p t x)).mpr ⟨hNS, hDF, hI, hSu, hSp⟩
    refine ⟨fun x t => u t x, fun x t => p t x,
      { toNavierStokesExistenceAndSmoothness := hc
        integrable := ?_
        globally_bounded_energy := ⟨C, fun t ht => (hC t ht).2⟩ }⟩
    intro t ht
    have hcont : Continuous (u t) := (c2_slice_fefferman u hSu ht).continuous
    exact (memLp_two_iff_integrable_sq hcont.norm.aestronglyMeasurable).mpr (hC t ht).1

/-- Solution class on the torus (B), (D): the authors' structure iff Fefferman's `SolTorus`. -/
theorem solTorus_iff (ν : ℝ) (u0 : E3 → E3) (f' : E3 → ℝ → E3) :
    (∃ v p, NavierStokes.Comparator.NavierStokesExistenceAndSmoothnessPeriodic ν u0 f' v p) ↔
      SolTorus ν u0 (fun t x => f' x t) := by
  constructor
  · rintro ⟨v, p, h⟩
    have hc := (core_iff ν u0 f' v p).mp h.toNavierStokesExistenceAndSmoothness
    refine ⟨fun t x => v x t, fun t x => p x t, hc.1, hc.2.1, hc.2.2.1, ?_, ?_, hc.2.2.2.1, hc.2.2.2.2⟩
    · intro t ht j x
      exact h.isOnePeriodic_velocity t ht x j
    · intro t ht j x
      exact h.isOnePeriodic_pressure t ht x j
  · rintro ⟨u, p, hNS, hDF, hI, hPu, hPp, hSu, hSp⟩
    have hc := (core_iff ν u0 f' (fun x t => u t x) (fun x t => p t x)).mpr ⟨hNS, hDF, hI, hSu, hSp⟩
    exact ⟨fun x t => u t x, fun x t => p t x,
      { toNavierStokesExistenceAndSmoothness := hc
        isOnePeriodic_velocity := fun t ht x j => hPu t ht j x
        isOnePeriodic_pressure := fun t ht x j => hPp t ht j x }⟩

/-- Initial datum for (A), (C). -/
theorem initR3_iff (u0 : E3 → E3) :
    NavierStokes.Comparator.InitialVelocityConditionDecay u0 ↔ SmoothDivFree u0 ∧ Decay u0 := by
  constructor
  · intro h
    exact ⟨⟨h.smooth, fun x => (div_eq u0 x).trans (h.div_free x)⟩, h.decay⟩
  · rintro ⟨⟨hs, hd⟩, hdec⟩
    exact { div_free := fun x => (div_eq u0 x).symm.trans (hd x), smooth := hs, decay := hdec }

/-- Initial datum for (B), (D). -/
theorem initTorus_iff (u0 : E3 → E3) :
    NavierStokes.Comparator.InitialVelocityConditionPeriodic u0 ↔ SmoothDivFree u0 ∧ PeriodicDatum u0 := by
  constructor
  · intro h
    exact ⟨⟨h.smooth, fun x => (div_eq u0 x).trans (h.div_free x)⟩, fun j x => h.isOnePeriodic x j⟩
  · rintro ⟨⟨hs, hd⟩, hp⟩
    exact { div_free := fun x => (div_eq u0 x).symm.trans (hd x), smooth := hs, isOnePeriodic := fun x i => hp i x }

/-- Force for (C): smoothness on the half-space and the (5) decay bounds. -/
theorem forceR3_iff (f' : E3 → ℝ → E3) :
    NavierStokes.Comparator.ForceConditionDecay f' ↔ ForceR3 (fun t x => f' x t) := by
  constructor
  · intro h
    refine ⟨contDiffOn_of_strip (fun z : ℝ × E3 => f' z.2 z.1) h.smooth, fun n K => ?_⟩
    obtain ⟨C, hC⟩ := h.decay n K
    refine ⟨C, fun t ht x => ?_⟩
    have e : ‖iteratedFDerivWithin ℝ n (fun z : E3 × ℝ => f' z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖
        = ‖iteratedFDerivWithin ℝ n (fun z : ℝ × E3 => f' z.2 z.1) halfSpace (t, x)‖ :=
      norm_iter_swap (fun z : ℝ × E3 => f' z.2 z.1) n x ht
    exact e.symm.le.trans (hC x t ht)
  · rintro ⟨hs, hd⟩
    refine { smooth := contDiffOn_to_strip (fun z : ℝ × E3 => f' z.2 z.1) hs, decay := fun n K => ?_ }
    obtain ⟨C, hC⟩ := hd n K
    refine ⟨C, fun x t ht => ?_⟩
    have e : ‖iteratedFDerivWithin ℝ n (fun z : E3 × ℝ => f' z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖
        = ‖iteratedFDerivWithin ℝ n (fun z : ℝ × E3 => f' z.2 z.1) halfSpace (t, x)‖ :=
      norm_iter_swap (fun z : ℝ × E3 => f' z.2 z.1) n x ht
    exact e.le.trans (hC t ht x)

/-- Force for (D): smoothness, periodicity in space and the (9) decay bounds in time. -/
theorem forceTorus_iff (f' : E3 → ℝ → E3) :
    NavierStokes.Comparator.ForceConditionPeriodic f' ↔ ForceTorus (fun t x => f' x t) := by
  constructor
  · intro h
    refine ⟨contDiffOn_of_strip (fun z : ℝ × E3 => f' z.2 z.1) h.smooth, fun t ht j x => h.isOnePeriodic t ht x j, fun n K => ?_⟩
    obtain ⟨C, hC⟩ := h.decay n K
    refine ⟨C, fun t ht x => ?_⟩
    have e : ‖iteratedFDerivWithin ℝ n (fun z : E3 × ℝ => f' z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖
        = ‖iteratedFDerivWithin ℝ n (fun z : ℝ × E3 => f' z.2 z.1) halfSpace (t, x)‖ :=
      norm_iter_swap (fun z : ℝ × E3 => f' z.2 z.1) n x ht
    exact e.symm.le.trans (hC x t ht)
  · rintro ⟨hs, hp, hd⟩
    refine { smooth := contDiffOn_to_strip (fun z : ℝ × E3 => f' z.2 z.1) hs, isOnePeriodic := fun t ht x j => hp t ht j x, decay := fun n K => ?_ }
    obtain ⟨C, hC⟩ := hd n K
    refine ⟨C, fun x t ht => ?_⟩
    have e : ‖iteratedFDerivWithin ℝ n (fun z : E3 × ℝ => f' z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖
        = ‖iteratedFDerivWithin ℝ n (fun z : ℝ × E3 => f' z.2 z.1) halfSpace (t, x)‖ :=
      norm_iter_swap (fun z : ℝ × E3 => f' z.2 z.1) n x ht
    exact e.le.trans (hC t ht x)

end Clay.NavierStokes.BridgeEquiv
