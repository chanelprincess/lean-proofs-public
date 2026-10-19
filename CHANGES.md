# Changes relative to upstream (openai/NavierStokesAndEuler @ f9e8bc5b)

Edited Lean modules (21), all under PROOFS/S412_ESTATE_PORT_v4.34.1/:

- NavierStokes/ActualCandidateConstruction.lean
- NavierStokes/EdgeWeightJets.lean
- NavierStokes/PrimaryPulseBounds.lean
- NavierStokes/R3/CompactComparisonBounds.lean
- NavierStokes/R3/ComparatorBridge.lean
- NavierStokes/R3/ComparisonCutoffs.lean
- NavierStokes/R3/ComparisonFiniteEnergy.lean
- NavierStokes/R3/ComparisonTimeAverages.lean
- NavierStokes/R3/LocalizedFluxEstimates.lean
- NavierStokes/R3/LocalizedTensorBounds.lean
- NavierStokes/R3/LpNormTools.lean
- NavierStokes/R3/PairedKernelBound.lean
- NavierStokes/R3/PressureFlux.lean
- NavierStokes/R3/PressureFluxTest.lean
- NavierStokes/R3/PressureFunctionals.lean
- NavierStokes/R3/RieszTestOperators.lean
- NavierStokes/R3/SmoothSobolevL6.lean
- NavierStokes/R3/WeightedInterpolation.lean
- NavierStokes/R3/WeightedSobolev.lean
- NavierStokes/R3FiniteEnergyComparison.lean
- NavierStokes/WeightedRadialPrimitive.lean

Pin files edited: lean-toolchain, lakefile.toml, lake-manifest.json
Files added: DEPENDENCY_CLOSURE.json, RESTORE_AND_VERIFY.md, UPSTREAM_PROVENANCE.json
Not carried over: .gitignore

Unchanged: all other files, the Euler library, and ComparatorChallenges/NavierStokes.lean.
Downstream estimate: about 418 NavierStokes modules depend on the edited ones (import-line scan, not a lake export).

## Why the port was needed
Upstream commit `f9e8bc5` builds on Lean 4.34.0-rc2 (and on 4.33.1 after `lake update`). Per [Reservoir](https://reservoir.lean-lang.org/@openai/NavierStokesAndEuler) it fails to build on Lean 4.34.1. This port makes it build on 4.34.1 (21 modules and 3 pin files changed), with statements unchanged and two-kernel verification (Lean default and nanoda).
