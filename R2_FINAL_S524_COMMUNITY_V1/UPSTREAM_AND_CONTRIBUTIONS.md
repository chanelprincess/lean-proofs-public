# Upstream and contributions

**Inherited mathematics and formalisation.** The proof of finite-time blowup for forced Navier–Stokes and its Lean formalisation are by **OpenAI** (paper "Finite time blowup for Navier–Stokes"; repository https://github.com/openai/NavierStokesAndEuler at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; licence Apache-2.0). They are not the packager's work.

**Port and toolchain changes.** 24 upstream files are modified by `SOURCE_PATCH/R2_over_upstream.patch` (ports to Lean 4.34.1 and Mathlib `d13f23b7`, build configuration):
- `NavierStokes/ActualCandidateConstruction.lean`
- `NavierStokes/EdgeWeightJets.lean`
- `NavierStokes/PrimaryPulseBounds.lean`
- `NavierStokes/R3/CompactComparisonBounds.lean`
- `NavierStokes/R3/ComparatorBridge.lean`
- `NavierStokes/R3/ComparisonCutoffs.lean`
- `NavierStokes/R3/ComparisonFiniteEnergy.lean`
- `NavierStokes/R3/ComparisonTimeAverages.lean`
- `NavierStokes/R3/LocalizedFluxEstimates.lean`
- `NavierStokes/R3/LocalizedTensorBounds.lean`
- `NavierStokes/R3/LpNormTools.lean`
- `NavierStokes/R3/PairedKernelBound.lean`
- `NavierStokes/R3/PressureFlux.lean`
- `NavierStokes/R3/PressureFluxTest.lean`
- `NavierStokes/R3/PressureFunctionals.lean`
- `NavierStokes/R3/RieszTestOperators.lean`
- `NavierStokes/R3/SmoothSobolevL6.lean`
- `NavierStokes/R3/WeightedInterpolation.lean`
- `NavierStokes/R3/WeightedSobolev.lean`
- `NavierStokes/R3FiniteEnergyComparison.lean`
- `NavierStokes/WeightedRadialPrimitive.lean`
- `lake-manifest.json`
- `lakefile.toml`
- `lean-toolchain`

**New files added by the package publisher** (15, in the same patch): the Fefferman-style statement and bridge modules (`ClayStatement/`), the solution and challenge files for the disjunction (`ClayFeffermanSolution`, `ClayFefferman*`, `NavierStokesComplete*` and the authors-formulation solution module), and helpers:
- `ClayStatement.lean`
- `ClayStatement/Bridge.lean`
- `ClayStatement/BridgeConverse.lean`
- `ClayStatement/BridgeEquiv.lean`
- `ClayStatement/BridgeLemmas.lean`
- `ClayStatement/BridgeSwap.lean`
- `ClayStatement/Fefferman.lean`
- `ComparatorChallenges/ClayFefferman.json`
- `ComparatorChallenges/ClayFefferman.lean`
- `ComparatorChallenges/ClayFeffermanViaD.json`
- `ComparatorChallenges/ClayFeffermanViaD.lean`
- `ComparatorChallenges/NavierStokesComplete.json`
- `ComparatorChallenges/NavierStokesComplete.lean`
- `NavierStokes/ClayFeffermanSolution.lean`
- `NavierStokes/ComparatorCompleteSolution.lean`

**R3 additions** (8 files, listed in `SOURCE_PATCH/R3_additions.txt`): the challenge files for (A), (B), (C), (D), the Comparator configurations for (C) and (D), and the two solution modules (one import line added to each delivered file).

**Packaging and verification** (`VERIFY.*`, `TOOLS/`, `CONTROLS/`, `RECEIPTS/`): the package publisher.

**Not reproduced here.** The publisher reported earlier, in a private analysis, that the authors' formal statements for alternatives (A) and (B) match the upstream formal-conjectures project (53 of 53 declarations identical). That comparison is not part of this package and not among its claims.
