import ClayStatement.Fefferman
import NavierStokes.ComparatorCompleteSolution

/-!
# Bridge lemmas, layer 1: Clay's coordinate-sum operators equal Mathlib's operators

F7 of Statements v2: divergence, Laplacian and gradient are Clay's coordinate sums.
These lemmas relate them to the trace, Δ, gradient and `fderiv` forms used by the authors' challenge.
No clause of either statement is changed here.
-/

namespace Clay.NavierStokes.BridgeLemmas
open Clay.NavierStokes
open scoped Laplacian

/-- (u·∇)u in Clay's coordinate sum is the derivative of g in the direction g x. Holds for every g. -/
theorem advect_eq (g : E3 → E3) (x : E3) : advect g x = fderiv ℝ g x (g x) := by
  have h := (EuclideanSpace.basisFun (Fin 3) ℝ).sum_repr' (g x)
  conv_rhs => rw [← h]
  simp only [map_sum, map_smul, advect, comp, dx, e, EuclideanSpace.basisFun_apply, real_inner_comm]

/-- Clay's coordinate-sum gradient is Mathlib's gradient. Holds for every q. -/
theorem grad_eq (q : E3 → ℝ) (x : E3) : grad q x = gradient q x := by
  have h := (EuclideanSpace.basisFun (Fin 3) ℝ).sum_repr' (gradient q x)
  conv_rhs => rw [← h]
  refine Finset.sum_congr rfl fun i _ => ?_
  have hi : inner ℝ (gradient q x) (EuclideanSpace.single i (1 : ℝ)) = fderiv ℝ q x (EuclideanSpace.single i 1) :=
    InnerProductSpace.toDual_symm_apply
  simp only [dx, e, EuclideanSpace.basisFun_apply]
  rw [real_inner_comm, hi]

/-- Clay's coordinate-sum divergence is the trace of the derivative (the challenge's `divergence`). Holds for every g. -/
theorem div_eq (g : E3 → E3) (x : E3) : div g x = NavierStokes.Comparator.divergence g x := by
  unfold Clay.NavierStokes.div NavierStokes.Comparator.divergence Clay.NavierStokes.comp Clay.NavierStokes.dx
  have h := LinearMap.trace_eq_sum_inner (fderiv ℝ g x : E3 →ₗ[ℝ] E3) (EuclideanSpace.basisFun (Fin 3) ℝ)
  simpa [Clay.NavierStokes.e, real_inner_comm] using h.symm

/-- Clay's coordinate-sum Laplacian is Mathlib's Δ for C² fields. -/
theorem lap_eq (g : E3 → E3) (hg : ContDiff ℝ 2 g) (x : E3) : lap g x = Δ g x := by
  have hL := congrFun (InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis g (EuclideanSpace.basisFun (Fin 3) ℝ)) x
  rw [hL]
  refine Finset.sum_congr rfl fun j _ => ?_
  have hd : DifferentiableAt ℝ (fderiv ℝ g) x :=
    ((hg.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero).differentiableAt
  have hc : DifferentiableAt ℝ (fun _ : E3 => e j) x := differentiableAt_const _
  have h1 := fderiv_clm_apply (c := fderiv ℝ g) (u := fun _ : E3 => e j) hd hc
  have h2 : fderiv ℝ (fun y => fderiv ℝ g y (e j)) x = (fderiv ℝ (fderiv ℝ g) x).flip (e j) := by
    simpa using h1
  simp only [dx, iteratedFDeriv_two_apply, h2]
  simp [e, EuclideanSpace.basisFun_apply]

end Clay.NavierStokes.BridgeLemmas
