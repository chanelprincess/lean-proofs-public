# KTS Global · Lean 4 formal verification · work in progress

Pre-release research package. Not a claimed solution.

## S437 · independent rebuild (Navier–Stokes alternatives C and D)
- Upstream: openai/NavierStokesAndEuler @ f9e8bc5 (Apache-2.0), ported to Lean 4.34.1
- Pins: Mathlib d13f23b, Comparator 19e111e, lean4export cacf989
- Declarations: NavierStokes.Comparator.navier_stokes_breakdown_R3, NavierStokes.Comparator.navier_stokes_breakdown_periodic
- Kernels: Lean default and nanoda; axioms: propext, Classical.choice, Quot.sound
- Scope: kernel acceptance against the challenge statement only. Correspondence with the official Clay problem statement has not been reviewed and is not claimed.

## Status
Further work, including reduced-axiom variants, is in progress and will be published with its own receipts.
