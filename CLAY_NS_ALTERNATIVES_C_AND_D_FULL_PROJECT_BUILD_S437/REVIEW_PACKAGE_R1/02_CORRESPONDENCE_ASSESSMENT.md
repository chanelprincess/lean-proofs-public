# 02 — Formal-to-official correspondence assessment

Performed 11 October 2026 by the Chaos coordinator session (a reasoned reading of the two texts). It is not an independent mathematician's review and no review receipt exists or is claimed. It replaces the earlier line "correspondence has NOT been reviewed" in scope only: an assessment now exists, with the residual judgments named below. The earlier files are preserved unchanged.

## 1. Texts compared

- **Official**: Charles L. Fefferman, "Existence and smoothness of the Navier–Stokes equation", Clay Mathematics Institute, `https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf` (6 pp., retrieved 11 Oct 2026, including its Errata section). Alternatives (C) and (D), conditions (1)–(11). No version date is printed in the retrieved text; the version used is the file served at that URL on the retrieval date.
- **Formal**: `ComparatorChallenges/NavierStokes.lean`, whose header states it was copied from `google-deepmind/formal-conjectures` at commit `8bf45ed70d48b2b2a501de9c00b26bfa38c573ee` with adaptations (imports, namespace, local notation; Apache-2.0, "The Formal Conjectures Authors"). The definitions were not authored by OpenAI or by the estate. Semantics of Mathlib symbols were taken from Mathlib at the pinned revision `d13f23b7…`; I re-read `Mathlib/Analysis/InnerProductSpace/Laplacian.lean` at that revision, not the files defining `gradient`, `fderiv` composition or `MemLp`.

What is being compared is the *challenge* statement, because Comparator established that the solution theorems have the same statements (including the definitions they mention) as the challenge. The project's internal vocabulary (`CandidateProperties`, `breakdownStatement`) affects the proof, not the correspondence; the conversions between the two are theorems checked by the kernel (see 01 §3.2.6).

## 2. Clause-by-clause: (C), whole space

| Official clause | Formal counterpart | Relation | Reasoning |
|---|---|---|---|
| "Take ν > 0 and n = 3" | `(nu : ℝ) (hnu : nu > 0)`; `ℝ³ = EuclideanSpace ℝ (Fin 3)` | Established | The formal theorem is for every ν > 0. If the official sentence is read as "for the ν you are given", this is identical; if read as "for some ν", the formal statement is stronger (implies it). Dimension 3 is explicit. |
| "there exist a smooth, divergence-free u° and a smooth f … satisfying (4), (5)" | `∃ u₀ f, InitialVelocityConditionDecay u₀ ∧ ForceConditionDecay f` | Established | The order of quantifiers is ∀ν ∃(u₀,f) ¬∃(v,p); official: given ν, there exist data with no solutions. Same. Data may depend on ν in both. |
| u° smooth (C^∞) | `ContDiff ℝ ∞ u₀` | Established | `∞` is every finite order (the file's `open ContDiff` scope; the proof project notes `⊤` would be analytic). |
| u° divergence-free | `∀ x, ∇⬝ u₀ x = 0`, `∇⬝ = trace of fderiv` | Established | The trace of the Jacobian is Σᵢ ∂ᵢuᵢ in the standard basis (basis-independent). |
| (4) `|∂ₓ^α u°(x)| ≤ C_{αK}(1+|x|)^{-K}`, all α, K | `∀ m K, ∃ C, ∀ x, ‖iteratedFDeriv ℝ m u₀ x‖ ≤ C/(1+‖x‖)^K` | Established | The m-th Fréchet derivative's norm is equivalent, with dimensional constants, to the maximum of the partials of order m, so bounds for all α with |α| = m are equivalent to a bound for the m-th derivative. Norms on ℝ³ are equivalent. `K : ℝ` includes negative K, where the bound follows from K = 0 up to a constant. |
| f smooth on ℝ³ × [0,∞) | `ContDiffOn ℝ ∞ (↿f) (univ ×ˢ Ici 0)` | Established, with direction noted | "Smooth on a closed half-space" has two usual readings: all one-sided derivatives exist and are continuous, or restriction of a smooth function on ℝ⁴. The first (the formal one) is weaker; the second implies it. For the *data* the proof's `f` is globally smooth, which satisfies both readings. See also item "(6)". |
| (5) `|∂ₓ^α ∂ₜ^m f| ≤ C (1+|x|+t)^{-K}` on ℝ³ × [0,∞) | `∀ m K, ∃ C, ∀ x, ∀ t ≥ 0, ‖iteratedFDerivWithin ℝ m (↿f) (univ ×ˢ Ici 0) (x,t)‖ ≤ C/(1+‖x‖+t)^K` | Established | Same equivalence of derivative norms; the within-derivative at t = 0 is one-sided on a set with unique differentiability. Decay is joint in (x,t) as in (5). |
| Equation (1) | `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = nu • Δ (v · t) x − gradient (p · t) x + f x t`, for all x, t ≥ 0 | Established by definitions | `fderiv ℝ (v · t) x` applied to the vector `v x t` is Σⱼ vⱼ ∂ⱼ v (the advection term). `Δ` is the Mathlib Laplacian: at the pinned revision `laplacian_eq_iteratedFDeriv_stdOrthonormalBasis` gives `Δ f x = Σᵢ D²f(x)(eᵢ,eᵢ)` and `laplacian_CLM_comp_left` shows it commutes with continuous linear maps, so on vector fields it is the componentwise Laplacian. `gradient` is the Riesz dual of the Fréchet derivative (coordinates ∂ᵢp) — read from the standard definition, not re-read in this pass. Time derivative is one-sided at t = 0, as it must be on [0,∞). |
| (2) div u = 0 for x, t ≥ 0 | `∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0` | Established | As above. |
| (3) u(x,0) = u°(x) | `∀ x, v x 0 = u₀ x` | Established | |
| (6) p, u ∈ C^∞(ℝ³ × [0,∞)) | `ContDiffOn ℝ ∞ (↿v)`, `(↿p)` on `univ ×ˢ Ici 0` | Justified implication, correct direction | A non-existence claim quantifies over competitors. Under the "restriction of a smooth function" reading the official class is contained in the formal class; the formal class is the larger one. No element of the larger class ⇒ none in the smaller. So the formal (C) implies the official (C) under either reading. |
| (7) `∫|u(x,t)|² dx < C` for all t ≥ 0 | `∀ t ≥ 0, MemLp (‖v · t‖) 2` and `∃ E, ∀ t ≥ 0, ∫ x, ‖v x t‖² < E` | Established | The Bochner integral is 0 for a non-integrable integrand; the explicit `MemLp … 2` removes that junk-value hazard, so the two conditions together say exactly "square-integrable at every time with a uniform bound". Constant strictness is immaterial. |
| "there exist no solutions (p,u) of (1),(2),(3),(6),(7)" | `¬ (∃ v p, NavierStokesExistenceAndSmoothnessRn nu u₀ f v p)` | Established | Competitor class = (1)(2)(3)(6)(7) as above, with the direction noted at (6). |

No clause of (C) was found mismatched.

## 3. Clause-by-clause: (D), periodic

| Official clause | Formal counterpart | Relation | Reasoning |
|---|---|---|---|
| Setting, ν, n | as in (C) | Established | |
| (8) u°, f periodic: `u°(x+e_j) = u°(x)`, `f(x+e_j,t) = f(x,t)` | `IsOnePeriodic u₀`; `∀ t ≥ 0, IsOnePeriodic (f · t)` | Established | e_j shift by `EuclideanSpace.single i 1`. Periodicity of f is required for t ≥ 0 only, which is the domain of f. |
| u° smooth, divergence-free | `InitialVelocityCondition` (smooth, `∇⬝ u₀ = 0`) | Established | As in (C). Note that no spatial decay is required for u° in (D); the formal periodic condition has none. |
| (9) `|∂ₓ^α ∂ₜ^m f| ≤ C (1+|t|)^{-K}` on ℝ³ × [0,∞) | `ForceConditionPeriodic.decay`: bound with `(1+t)^K`, uniform in x | Established | As in (C) with the spatial weight dropped, as in (9). |
| f smooth on ℝ³ × [0,∞) | `ForceCondition.smooth` | Established | As in (C). |
| (10) `u(x,t) = u(x+e_j,t)` | `∀ t ≥ 0, IsOnePeriodic (v · t)` | Established | |
| Erratum: "the further condition p(x+e_j,t) = p(x,t) should be made explicit in Eqn (8)" | `∀ t ≥ 0, IsOnePeriodic (p · t)` (the comparator comment cites "Clay errata") | **Reading-dependent** | See §4. |
| (11) p, u ∈ C^∞(ℝ³ × [0,∞)) | as (6) | Justified implication, correct direction | As (6). |
| (1), (2), (3) | as (C) | Established | |
| No energy condition in (D) | none in `NavierStokesExistenceAndSmoothnessPeriodic` | Established | The periodic class has no (7); the formal class matches. |
| "no solutions of (1),(2),(3),(10),(11)" | `¬ (∃ v p, NavierStokesExistenceAndSmoothnessPeriodic nu u₀ f v p)` | Established modulo the erratum reading | |

## 4. The one reading-dependent point: pressure periodicity in (D)

The retrieved text of the erratum says the pressure-periodicity condition "should be made explicit in Eqn (8)". In the printed list, (8) is the periodicity of the data u°, f, which contains no pressure. The erratum's second item says "Eqn (10) should read:" followed by the weak formulation, which in the printed list is equation (12). The erratum's numbering is therefore offset by two from the printed list; under that offset its "(8)" corresponds to the printed (10), the periodicity of the solution, where the pressure condition belongs. This inference is mine, not stated in the document. The formal statement takes this reading.

Consequence if the reading is rejected: the competitor class loses the pressure-periodicity restriction and becomes larger, so the formal (D) would be a weaker statement than a version without that restriction; the machine-checked theorem would not by itself settle that version. Observation (an analyst's remark, not machine-checked): for periodic `u` and `f` the equation forces `∇p` to be periodic, so `p(x+e_j,t) − p(x,t)` depends only on t; without periodicity of `p`, a competitor therefore differs from one with periodic pressure only by a spatially uniform, time-dependent force `a(t)` (the cell average of `∇p`). Whether (D) also holds for the larger class is a different mathematical question not answered here. The proof's own periodic competitor class (`PeriodicPaper.GlobalSmoothSolution`) requires a periodic pressure.

## 5. Conversions the proof makes between its own vocabulary and the challenge's
All are theorems in the closure; kernel-accepted. Listed so a reviewer can find them:
1. Whole space: zero initial datum is a valid datum (`zero_initial_condition_decay`); compactly supported smooth force has decay of every order for every real exponent (`forceConditionDecay_of_compact`, `CompactSpatialForceDecay`).
2. Whole space: a comparator solution yields a project `GlobalFiniteEnergySolution` (`globalSolutionOfComparator`): same smoothness domain, same equation, zero initial value, and the energy bound `max 0 (E/2)` for ½∫|v|² — the factor ½ and the strict `< E` are handled there.
3. Periodic: zero datum valid (`zero_initial_condition`); periodic force decays in t (`futureJet_decay`); comparator periodic solution yields a project `GlobalSmoothSolution` (`periodicPaperSolution_of_comparator`, not read line by line).
Direction check: each conversion maps a hypothetical *official-class* competitor into the project's competitor class, so excluding the project's class excludes the official one. Where the official class is smaller than the project's (the closed-half-space readings), the implication goes the right way, as noted.

## 6. Residual judgments (named, not closed)
- **J1** The erratum reading in §4.
- **J2** The reading of "C^∞ on ℝ³ × [0,∞)" is covered in the correct direction (no residual for the claim), but a reviewer may wish to confirm that the equivalence of the two readings (a Whitney-type extension result) is not needed; it is not used.
- **J3** `gradient` and the Mathlib definitions other than the Laplacian were read by their standard meaning; no machine-checked bridge from these Lean expressions to coordinate formulas was run. I considered a small Lean file proving the coordinate formulas against the pinned Mathlib and did not build one: the runner has no operation that compiles an additional file against the project environment, and extending it was not warranted for a definitional reading. The challenge statements are a third party's formalisation; its fidelity is its authors' claim, assessed here by reading, not independently proved.
- **J4** Non-vacuity of the competitor class: the zero field with zero force solves the project's whole-space class (`zero_force_has_global_solution`, READ); the corresponding statement for the comparator-side class was not found and is not claimed.
- **J5** This assessment was made by an automated coordinator session reading the texts. Its standing is that of a documented analysis; the standard of record is review by qualified mathematicians, who have not reviewed this package.

## 7. Conclusion
For (C), every clause of the official statement has an established counterpart or a justified implication in the correct direction; no mismatch was found. For (D), the same holds except that the pressure-periodicity clause depends on reading the Clay erratum as extending the solution condition (10). If that reading is accepted, the formal statements (C) and (D) correspond to the official alternatives (C) and (D). A kernel-accepted proof of these two formal statements would then establish the official alternatives as stated; whether that suffices for any institution's acceptance is outside this package.
