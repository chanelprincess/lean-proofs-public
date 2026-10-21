# Findings made while preparing this package

Each finding is stated technically. None is a claim about the correctness of the mathematics; they are about the packaging and the checks.

1. **Import collision (two modules that each work alone fail together).** A bridge module that imported the authors' *challenge* module could not be loaded together with `NavierStokes.ComparatorSolution`: both declare the same `NavierStokes.Comparator.*` names (`environment already contains ...`). Fix: import the authors' *solution-side* module (`NavierStokes.ComparatorCompleteSolution`), whose `OptionA..OptionD` are textually identical. Permanent control: `R2F1_*` in `CONTROLS/`.
2. **A proved route with no challenge checking it.** A solution module proved the disjunction through (C) and through (D) while only one route was named by a Comparator configuration. Added `ClayFeffermanViaD`. Permanent control: `TOOLS/route_coverage.py` and `R2F2_*`.
3. **A one-way bridge cannot see a weakened target.** An implication into a weaker statement always holds, so checking only that direction accepts a weakened force bound. The converse as written, and the two-way chain, fail with `Application type mismatch` against the weakened statement (`R2F4_*`). This is the *observed failure of the converse as written*; it is not a proof that no converse proof can exist.
4. **A changed-file list does not cover added files.** Comparing a patched tree with its reference through a list of changed files silently ignores files the patch adds. `TOOLS/source_binding_check.py` compares every file, with a tamper self-test.
5. **Tool provenance.** `nanoda_bin` rebuilt from the pinned source was byte-identical to an earlier build; `landrun` was not.
6. **Authors' libraries.** Seven modules of the authors' `NavierStokes` and `Euler` libraries do not compile on Lean 4.34.1 (outside the claimed closure); see `KNOWN_LIMITS.md`.
7. **R3 solution files did not compile as delivered** (missing `import NavierStokes.ComparatorSolution`); fixed at the import line.
8. **Open-file limit.** The Mathlib cache restore fails under a low open-file limit on many-core machines; `VERIFY.sh` raises the limit and checks it.
