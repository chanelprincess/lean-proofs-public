# Restore and verify (S412_ESTATE_PORT_v4.34.1)

Prerequisites: git, elan with toolchain leanprover/lean4:v4.34.1, network access for the one-time restoration, Linux x86_64.
Executed and verified on: Ubuntu 24.04.5 LTS (x86_64). No other operating system has been tested; Windows and offline restoration are NOT claimed.

1. Install the toolchain in `lean-toolchain` through elan.
2. From this directory run `lake exe cache get` (it restores the manifest-pinned packages and the Mathlib cache). Do NOT run `lake update`.
3. Build the verification tools with the same toolchain: Comparator and lean4export at the revisions in `DEPENDENCY_CLOSURE.json`; place landrun and nanoda_bin on PATH.
4. Run `lake exe comparator ComparatorChallenges/NavierStokes.json` from this directory.

The declarations checked: NavierStokes.Comparator.navier_stokes_breakdown_R3, NavierStokes.Comparator.navier_stokes_breakdown_periodic. Permitted axioms: propext, Classical.choice, Quot.sound.
Official-statement correspondence has not been reviewed (see UPSTREAM_PROVENANCE.json).
