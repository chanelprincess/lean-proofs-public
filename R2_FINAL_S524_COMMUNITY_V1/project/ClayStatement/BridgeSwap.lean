import ClayStatement.BridgeLemmas

/-!
# Bridge lemmas, layer 2: the argument-order swap

Fefferman's fields are `u t x` on the closed half-space {t ≥ 0} ⊆ ℝ × ℝ³; the authors' challenge writes
`v x t` on `univ ×ˢ Ici 0` ⊆ ℝ³ × ℝ. These lemmas transport smoothness, fixed-time slices and the
iterated-derivative norms across `Prod.swap`, which is a linear isometry. No clause is changed.
-/

namespace Clay.NavierStokes.BridgeSwap
open Clay.NavierStokes
open scoped ContDiff

theorem uniqueDiffOn_halfSpace : UniqueDiffOn ℝ halfSpace := by
  have h : halfSpace = Set.Ici (0 : ℝ) ×ˢ (Set.univ : Set E3) := by
    ext z; simp [halfSpace]
  rw [h]
  exact (uniqueDiffOn_Ici 0).prod uniqueDiffOn_univ

theorem contDiffOn_to_strip {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] (G : ℝ × E3 → F) {n : WithTop ℕ∞}
    (h : ContDiffOn ℝ n G halfSpace) :
    ContDiffOn ℝ n (fun z : E3 × ℝ => G (z.2, z.1)) (Set.univ ×ˢ Set.Ici (0 : ℝ)) := by
  have h1 := h.comp_continuousLinearMap (ContinuousLinearEquiv.prodComm ℝ E3 ℝ : E3 × ℝ →L[ℝ] ℝ × E3)
  have hs : ((ContinuousLinearEquiv.prodComm ℝ E3 ℝ : E3 × ℝ →L[ℝ] ℝ × E3) ⁻¹' halfSpace)
      = Set.univ ×ˢ Set.Ici (0 : ℝ) := by
    ext z; simp [halfSpace]
  rw [hs] at h1
  exact h1

theorem contDiffOn_of_strip {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] (G : ℝ × E3 → F) {n : WithTop ℕ∞}
    (h : ContDiffOn ℝ n (fun z : E3 × ℝ => G (z.2, z.1)) (Set.univ ×ˢ Set.Ici (0 : ℝ))) :
    ContDiffOn ℝ n G halfSpace := by
  have h1 := h.comp_continuousLinearMap (ContinuousLinearEquiv.prodComm ℝ ℝ E3 : ℝ × E3 →L[ℝ] E3 × ℝ)
  have hs : ((ContinuousLinearEquiv.prodComm ℝ ℝ E3 : ℝ × E3 →L[ℝ] E3 × ℝ) ⁻¹'
      (Set.univ ×ˢ Set.Ici (0 : ℝ))) = halfSpace := by
    ext z; simp [halfSpace]
  rw [hs] at h1
  exact h1

/-- At a fixed time t ≥ 0, a function smooth on the half-space is smooth in x. -/
theorem slice_of_halfSpace {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] (g : ℝ → E3 → F) {n : WithTop ℕ∞}
    (h : ContDiffOn ℝ n (fun z : ℝ × E3 => g z.1 z.2) halfSpace) {t : ℝ} (ht : 0 ≤ t) :
    ContDiff ℝ n (g t) := by
  have hc : ContDiff ℝ n (fun y : E3 => ((t, y) : ℝ × E3)) := contDiff_const.prodMk contDiff_id
  have h2 := h.comp (hc.contDiffOn (s := Set.univ)) (fun y _ => (show (0 : ℝ) ≤ t from ht))
  exact contDiffOn_univ.mp h2

/-- Same for the challenge's argument order. -/
theorem slice_of_strip {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] (v : E3 → ℝ → F) {n : WithTop ℕ∞}
    (h : ContDiffOn ℝ n (fun z : E3 × ℝ => v z.1 z.2) (Set.univ ×ˢ Set.Ici (0 : ℝ))) {t : ℝ} (ht : 0 ≤ t) :
    ContDiff ℝ n (fun y => v y t) := by
  have hc : ContDiff ℝ n (fun y : E3 => ((y, t) : E3 × ℝ)) := contDiff_id.prodMk contDiff_const
  have h2 := h.comp (hc.contDiffOn (s := Set.univ)) (fun y _ => (show y ∈ Set.univ ∧ t ∈ Set.Ici (0 : ℝ) from ⟨trivial, ht⟩))
  exact contDiffOn_univ.mp h2

/-- The norm of the m-th iterated derivative is unchanged by the swap isometry. -/
theorem norm_iter_swap (G : ℝ × E3 → E3) (m : ℕ) (x : E3) {t : ℝ} (ht : 0 ≤ t) :
    ‖iteratedFDerivWithin ℝ m (fun z : E3 × ℝ => G (z.2, z.1)) (Set.univ ×ˢ Set.Ici (0 : ℝ)) (x, t)‖
      = ‖iteratedFDerivWithin ℝ m G halfSpace (t, x)‖ := by
  have h1 := (LinearIsometryEquiv.prodComm ℝ E3 ℝ).norm_iteratedFDerivWithin_comp_right G
    uniqueDiffOn_halfSpace (x := (x, t)) (show ((LinearIsometryEquiv.prodComm ℝ E3 ℝ) (x, t)) ∈ halfSpace from ht) m
  have hs : ((LinearIsometryEquiv.prodComm ℝ E3 ℝ) ⁻¹' halfSpace) = Set.univ ×ˢ Set.Ici (0 : ℝ) := by
    ext z; simp [halfSpace]
  rw [hs] at h1
  exact h1

end Clay.NavierStokes.BridgeSwap
