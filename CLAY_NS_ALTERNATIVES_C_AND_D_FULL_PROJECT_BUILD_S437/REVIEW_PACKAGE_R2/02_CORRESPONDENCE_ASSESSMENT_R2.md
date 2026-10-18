# 02 R2 — Formal-to-official correspondence assessment (sharpened)

Successor to `REVIEW_PACKAGE_R1/02_CORRESPONDENCE_ASSESSMENT.md`, which is preserved unchanged. Written 11 October 2026 by the Chaos coordinator session. It is a documented analysis. It is not an independent referee report, no expert review has been obtained, and none is claimed. A successful rebuild (see 03 R2) does not close any question in this file.

Evidence levels: **READ** = text read in full for this assessment, with locations. **KERNEL** = a theorem in the verified closure (accepted by both kernels in the t6 run). **HAND** = checked by me by hand, not machine-checked. **STANDARD** = a standard analysis fact cited, not proved here. **OPEN** = not established.

## 0. What changed relative to R1
1. R1 described the challenge definitions after a partial view of the file. This pass re-read `ComparatorChallenges/NavierStokes.lean` lines 40–286 in full (numbered). R1's quoted definitions agree with the file; no clause in R1 was found misquoted. What R1 left unchecked is checked below.
2. The official text was re-read directly. Equation numbers and the erratum are now cited with locations (§3).
3. R1's open point "gradient and Mathlib definitions read by standard meaning" is closed by KERNEL theorems in the closure (§4).
4. R1's remark about a spatially uniform force in the periodic case is replaced by a derived relation with its exact scope (§5).
5. The direction of every inclusion is stated per clause, separately for the competitor side and the data side (§2).

## 1. Texts
- **Official**: C. L. Fefferman, "Existence and smoothness of the Navier–Stokes equation", Clay Mathematics Institute, `https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf`, as retrieved 11 Oct 2026. Page and line numbers below are those of the retrieved text extraction, not necessarily printed page numbers. The file carries no version date.
- **Formal**: `ComparatorChallenges/NavierStokes.lean`, copied (per its header) from `google-deepmind/formal-conjectures` commit `8bf45ed70d48b2b2a501de9c00b26bfa38c573ee`, Apache-2.0, "modified from its original form". Line numbers below are the file's own. The theorems (lines 273–276, 280–283) are the two checked declarations; Comparator established that the solution theorems have the same statements, with the same definitions, as the challenge.
- **Mathlib** at `d13f23b723b8a846827a245b89c10fc7d3f11612`, read directly in the retained t6 workspace (`gradient` at `Mathlib/Analysis/Calculus/Gradient/Basic.lean:84`; `contDiffOn_infty_iff_fderivWithin` at `…/ContDiff/Defs.lean:885`; `UniqueDiffOn.prod` at `…/TangentCone/Prod.lean:63`; `uniqueDiffOn_Ici` at `…/TangentCone/Real.lean:87`; `ContDiffWithinAt` at `…/ContDiff/Defs.lean:131`).

The official statement says "we ask for a proof of one of the following four statements" (page 2, line 56). Alternatives (C) and (D) are independent targets and are assessed separately: an unresolved point in (D) does not affect (C).

## 2. What must be shown, and in which direction
Let a *competitor* be a pair (v, p). Each theorem says: for every ν > 0 there are data (u₀, f) such that no competitor exists in the formal class.

- **Competitor side** (needed so that "no formal competitor" implies "no official competitor"): every official solution, taken as the same pair (v, p), must lie in the formal class. This is the inclusion **official class ⊆ formal class**.
- **Data side** (needed so that the witness data are admissible in the official statement): the data produced by the proof must satisfy the official data conditions. This is the implication **formal data conditions ⇒ official data conditions**, or a direct argument about the actual witness.

Larger formal competitor class ⇒ safe. A smaller formal competitor class ⇒ the inference fails unless separately justified. The two sides are different questions and are tabulated separately.

## 3. Official text (READ) and the equations it numbers
Page 1: (1) the equation; (2) div u = 0; (3) u(x,0) = u°(x); (4) decay of ∂ₓ^α u° (line 19); (5) decay of ∂ₓ^α ∂ₜ^m f in (1+|x|+t) (line 23); (6) "p, u ∈ C^∞(ℝⁿ × [0,∞))" (line 27); (7) "∫|u(x,t)|² dx < C for all t ≥ 0" (line 31); (8) u°(x+e_j) = u°(x), f(x+e_j,t) = f(x,t) (line 35).
Page 2: (9) decay of ∂ₓ^α ∂ₜ^m f in (1+|t|), "in place of (4) and (5), we assume that u° is smooth" (line 46); (10) u(x,t) = u(x+e_j,t) on ℝ³×[0,∞) (line 50); (11) p, u ∈ C^∞(ℝⁿ × [0,∞)) (line 54). **(C)** (line 60): ν > 0, n = 3; there exist smooth divergence-free u° and smooth f on ℝ³ × [0,∞) satisfying (4), (5), with no solutions (p,u) of (1), (2), (3), (6), (7). **(D)** (line 61): data satisfying (8), (9); no solutions of (1), (2), (3), (10), (11).
Page 3, line 86: the weak formulation is printed as **(12)**, with "− ∬ p·(div θ)".
Page 6, lines 143–149 (Errata): "The further condition p(x+e_j,t) = p(x,t) should be made explicit in Eqn (8)." and "Eqn (10) should read:" followed by the weak formulation (with "+ ∬ p·(div θ)").

Observation: the erratum's "(10)" displays the weak formulation, which the printed list numbers (12). So the erratum's label is two below the printed number. Applying the same shift to the erratum's "(8)" gives printed (10), the periodicity of the solution velocity, which is where a pressure condition belongs; printed (8) concerns the data u°, f only, which contain no pressure. The shift is consistent across the two erratum items; it is an observation about the numbering, not a proof of the author's intent (§5b).

## 4. (C), whole space

### 4a. Competitor side: official class ⊆ formal class (`NavierStokesExistenceAndSmoothnessRn`, lines 245–253, extending lines 217–235)
| Official | Formal | Argument | Level |
|---|---|---|---|
| (1) for x ∈ ℝ³, t ≥ 0 | `navier_stokes` (L222): `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = nu • Δ (v · t) x − gradient (p · t) x + f x t`, all x, all t ≥ 0 | Same equation. `derivWithin … (Ici 0)` is the right derivative at t = 0 and the ordinary derivative for t > 0 (`temporalDerivative_eq`, t > 0, KERNEL). `fderiv … (v x t)` is Σⱼ vⱼ ∂ⱼ v. `Δ` is Mathlib's Laplacian; `gradient` is the Riesz dual of `fderiv` (Mathlib def, READ). | READ, KERNEL |
| (2) | `div_free` (L227): `∇⬝ (v · t) x = 0`, t ≥ 0; `divergence` L81 = trace of `fderiv` | trace of the Jacobian = Σᵢ ∂ᵢvᵢ; `divergence_eq` proves it equals the project's Σᵢ (D_x v (eᵢ))ᵢ | READ, KERNEL |
| (3) | `initial_condition` (L229) | identical | READ |
| (6) smooth on ℝ³×[0,∞) | `velocity_smooth`, `pressure_smooth` (L232, 235): `ContDiffOn ℝ ∞ (↿v) (univ ×ˢ Ici 0)` | Reading A (restriction of a C^∞ function on an open neighbourhood): `ContDiff.contDiffOn`. Reading B (all partial derivatives exist, with one-sided derivatives at t = 0, and are continuous up to the boundary): on a `UniqueDiffOn` set `ContDiffOn ℝ ∞ f s ↔ DifferentiableOn f s ∧ ContDiffOn ℝ ∞ (fderivWithin f s) s` (`contDiffOn_infty_iff_fderivWithin`, Mathlib, READ), and `univ ×ˢ Ici 0` is `UniqueDiffOn` (`UniqueDiffOn.prod`, `uniqueDiffOn_Ici`, `uniqueDiffOn_univ`, READ). That equivalence is the recursive form of "all iterated one-sided derivatives exist and are continuous". `∞` here is "every finite order": the `ContDiffWithinAt` definition has a separate `ω` (analytic) branch. Under B the official hypothesis is the formal one, and the bridge from continuous extension of the interior derivatives to `fderivWithin` is a STANDARD one-sided-derivative argument not machine-checked here. | READ; A: Mathlib; B: STANDARD |
| (7) | `integrable` (L250) `MemLp (‖v · t‖) 2`, and `globally_bounded_energy` (L253) `∃ E, ∀ t ≥ 0, ∫ ‖v x t‖² < E` | v continuous ⇒ ‖v(·,t)‖ is measurable; a finite integral of the square gives `MemLp … 2`; take E = the official constant C. The explicit `MemLp` removes the Bochner junk-value hazard (an integral of a non-integrable function is 0). The measure is Mathlib's `volume` on `EuclideanSpace ℝ (Fin 3)`, the standard Lebesgue measure; that instance was not re-read here. | HAND; measure instance not re-read |
| `∇⬝` is junk-valued (0) where `fderiv` is the zero map (L77–78) | | The competitor class has `ContDiffOn` on the closed half-space, so each time slice `x ↦ v x t` (t ≥ 0) is differentiable and `∇⬝` is never evaluated at its junk value. | HAND |
Conclusion for the competitor side: under either reading of (6), official class ⊆ formal class. Hence ¬∃ formal competitor ⇒ ¬∃ official competitor.

### 4b. Data side: the witness satisfies the official data conditions
The witness is explicit and was read in full in `NavierStokes/R3/ComparatorBridge.lean`: `u₀ = fun _ => 0`, `f' = toComparator f` with `toComparator f x t = f (t, x)` (`ComparatorBridge.lean`, READ), where `f` is the candidate force with `ContDiff ℝ ∞ f` (global spacetime smoothness) and `HasCompactSupport f` (`comparator_of_breakdown` statement and body, READ).
| Official | Argument | Level |
|---|---|---|
| u° smooth, divergence-free | constant zero | HAND |
| (4) | `InitialVelocityConditionDecay.decay` bounds ‖D^m u₀‖ ≤ C/(1+‖x‖)^K for all m, K ∈ ℝ. A partial derivative ∂ₓ^α is that derivative evaluated on unit vectors, hence bounded by its norm; so (4) follows. For u₀ = 0 it is trivial. | HAND |
| f smooth on ℝ³×[0,∞) | f' is the restriction to t ≥ 0 of `(x,t) ↦ f(t,x)`, a globally C^∞ function; this satisfies reading A directly, and B follows. This holds for the actual witness; it is not part of the theorem's formal conclusion. `toComparator_smooth` is a KERNEL theorem in `ComparatorBridge.lean`. | READ, KERNEL |
| (5) | `ForceConditionDecay.decay` bounds ‖iteratedFDerivWithin ℝ m (↿f') (univ ×ˢ Ici 0) (x,t)‖ ≤ C/(1+‖x‖+t)^K. A mixed partial ∂ₓ^α ∂ₜ^m is that derivative of total order |α|+m evaluated on unit vectors (unit in the product norm, which is the maximum norm), hence bounded by its norm. For the witness the force has compact spacetime support, so the decay is proved from the support (`forceConditionDecay_of_compact`, READ, KERNEL). | HAND; KERNEL for the witness |
Conclusion for the data side: the witness satisfies (4), (5) and the smoothness and divergence requirements under both readings.

### 4c. Whole-space result
Every clause of (C) has its counterpart; the competitor-side inclusion goes in the safe direction; the witness data are admissible. The statement is for every ν > 0, which is at least what "Take ν > 0" asks.

## 5. (D), periodic

### 5a. Clauses that match (formal class lines 262–269, extending 217–235; data lines 164–167 and 200–205)
- (8): `InitialVelocityConditionPeriodic.isOnePeriodic` (L167, `IsOnePeriodic u₀`, L121) and `ForceConditionPeriodic.isOnePeriodic` (L202, for t ≥ 0). READ.
- (9): `ForceConditionPeriodic.decay` (L204–205), bound in `(1 + t)^K`, uniform in x; `ForceCondition.smooth` for smoothness. READ. No spatial decay is demanded of u°, as (9) says "in place of (4) and (5)".
- (10): `isOnePeriodic_velocity` (L267). (11): smoothness as in (6). (1), (2), (3): as in 4a.
- The periodic competitor class carries **no energy condition** (it extends the common core only). This matches the official (D), which lists no (7). No bounded-energy condition was added.
- Direction on (11): as in 4a, official class ⊆ formal class.

### 5b. The one reading-dependent clause: pressure periodicity
The formal class adds `isOnePeriodic_pressure` (L269), documented in the file as "following the errata appended to the Clay problem statement".
- Under the printed list alone, (D)'s competitor class is (1), (2), (3), (10), (11) with no pressure condition (call it class R0). The formal class is R0 plus periodic pressure (class R1, the erratum reading). R1 ⊆ R0, so **nonexistence in R1 does not by itself give nonexistence in R0.**
- Evidence for R1: the erratum (page 6, line 145) requires the pressure periodicity to be made explicit "in Eqn (8)"; printed (8) lists data only, while the erratum's own equation label "(10)" (line 147) is printed (12), i.e. the labels shift by two; under that shift "(8)" is the printed (10), the periodicity of the solution. This is consistent, and no other placement for a pressure condition exists in the printed list.
- Relation between R0 and R1 (HAND, derived here, not machine-checked). If (v,p) ∈ R0 for (u₀,f) with f and v periodic, every term of (1) except ∇p is periodic, so ∇p is periodic and p(x+e_j,t) − p(x,t) = c_j(t) does not depend on x. Put q = p − Σⱼ cⱼ(t) xⱼ; q is periodic and (v,q) solves (1) with force f − c(t). Averaging (1) over a cell shows c(t) = (cell average of f) − m′(t), where m(t) is the cell average of v. So R0 contains exactly the periodic-pressure solutions for forces f − c(t), for all admissible c: the freedom is a prescribed uniform pressure gradient, equivalently a prescribed mean flow. The erratum removes that freedom.
- Whether the witness of (D) also has no solution in R0 is **OPEN**. It would need an argument that no choice of mean flow can rescue a global solution (a Galilean change of frame is the natural tool); none was carried out.

### 5c. Data side for (D)
Zero initial datum: `zero_initial_condition` (KERNEL). Periodic force with decay in t: `forceConditionPeriodic_of_decay` and `CandidateConsequences.futureJet_decay` (named; KERNEL; the module `PeriodicComparatorSolution` was not read line by line). Smoothness of the witness force as in 4b. For (8) the witness force is the periodisation of a compactly supported field (R1 01 §3.3).

## 6. Operators, closed
R1 listed "gradient and the other Mathlib definitions read by their standard meaning" as an open judgment. The closure contains kernel-checked equalities between the challenge's operators and the project's coordinate forms: `divergence_eq`, `gradient_eq`, `laplacian_eq` (for slices of class C²) and `temporalDerivative_eq` (t > 0), in `NavierStokes/ComparatorBridge.lean` (module in the closure per job R1b). The project's coordinate forms (`ProblemStatement.lean` L55–80) are: `spatialDivergence = Σᵢ (D_x u eᵢ)ᵢ`, `pressureGradient = Σᵢ (∂ᵢp) eᵢ`, `spatialLaplacian = Σᵢ ∂ᵢ(∂ᵢu)`, `advection = (D_x u)(u)`, `temporalDerivative = D_t u`. These are the textbook coordinate formulas (READ). The only operator point not covered by a theorem is the one-sided time derivative at t = 0, which is `derivWithin … (Ici 0)` by Mathlib's definition and is the right derivative, as equation (1) on [0,∞) requires. Residual: the equalities hold under the stated hypotheses; for competitors these hold by the smoothness clause.

## 7. Non-vacuity of the competitor classes
v = 0, p = 0 satisfies every clause of the formal whole-space and periodic classes for u₀ = 0, f = 0 (each clause evaluates at the zero function; HAND). The project's own class is shown inhabited in the closure (`zero_force_has_global_solution`, `R3/ProblemStatement.lean`, READ, KERNEL). The theorems are therefore not true by emptiness of the competitor class.

## 8. Residual judgments (named, not closed)
- **J1** (D): acceptance of the erratum reading R1 (§5b). Evidence given; the interpretation is not machine-checkable.
- **J2** Reading B of "C^∞ on the closed half-space" on the competitor side: STANDARD argument, not machine-checked. Moot for the data side (§4b) and for reading A.
- **J3** Closed to the extent stated in §6; the measure instance and the one-sided derivative at t = 0 are by definition, not by theorem.
- **J4** Whether (D) also holds in R0 (§5b): OPEN.
- **J5** No independent expert review of any of this exists. The formalisation is a third party's (Formal Conjectures); its fidelity is assessed here only by reading.
- **J6** What any institution requires beyond a statement-level proof (publication, waiting period, committee) is outside this package.
- **J7** The 166-page informal paper has not been refereed in these records. The formal theorems do not depend on it for their kernel acceptance, but this package does not assert the paper's correctness.

## 9. Disposition
(C): every clause matched; competitor inclusion in the safe direction; witness data admissible. No mismatch found. Residual J2 (reading B, STANDARD).
(D): matches except that the pressure-periodicity clause depends on reading the erratum as part of the solution class (J1). If accepted, (D) matches. If not, the formal (D) is a theorem about a smaller class than the printed list's, and the machine-checked result would not settle the larger class (J4).
This is a coordinator assessment. It narrows the specialist judgments to J1, J2 and J5–J7; it does not replace them.

## 10. Reviewer packet (prepared; not sent)
For an appropriate mathematical reviewer: the official PDF; `ComparatorChallenges/NavierStokes.lean` L40–286; `NavierStokes/ProblemStatement.lean` L30–80 and `ComparatorBridge.lean` (operator equalities); `R3/ComparatorBridge.lean` and `PeriodicPaperComparator.lean` (witness and conversions); questions: (1) accept the erratum reading R1? (2) is the Reading B step acceptable as standard? (3) is the formalisation faithful in the clauses of §4a and §5a? (4) is (D) in R0 of interest? No external transmission has been made or authorized.
