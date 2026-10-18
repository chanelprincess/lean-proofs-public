# Lean test package: finite-time blowup for forced Navier-Stokes (Clay alternatives (C) and (D))

This archive lets you independently check, with Lean, two theorems about the forced Navier-Stokes equations, and read how their statements were compared with the official Clay problem text. It is offered for **testing and review**. It does not claim that a Clay Millennium Prize problem has been solved or accepted.

## What is being checked
The two declarations, for every viscosity `nu > 0`:
- `NavierStokes.Comparator.navier_stokes_breakdown_R3` (whole space, Clay alternative (C))
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic` (periodic, Clay alternative (D))

Each says there are smooth data and a smooth force for which no smooth global solution of the stated class exists. The check is Lean's `Comparator` tool: it compares the solution's statements with the challenge statements in `project/ComparatorChallenges/NavierStokes.lean`, replays the solution in the Lean kernel and in the independent `nanoda` kernel, and allows only the axioms `propext`, `Classical.choice`, `Quot.sound`.

## Who did what
The mathematics and the Lean proof are by OpenAI (paper and repository `openai/NavierStokesAndEuler`, Apache-2.0). The challenge statements come from the Formal Conjectures project (Google DeepMind repository, Apache-2.0). The packager ported the proof to Lean 4.34.1 and ran and documented the checks. See `NOTICE.md`. The packager did not author the proof.

## Run it
```
scripts/reproduce.sh [WORKDIR]
```
It copies `project/` into a fresh work directory, builds the two checker tools from pinned source, builds the project's checked closure, runs Comparator's four control projects and then the challenge, and independently prints the axioms of both theorems. Prerequisites, expected output, runtime and disk needs: `TESTING.md`.

Expected final line: `RESULT: PASS -- both declarations accepted by Lean's default kernel and by nanoda ...`

## What was tested, and what was not
See `docs/03_VERIFICATION_SUMMARY.md` and `KNOWN_LIMITS.md`. In short: `scripts/reproduce.sh` itself was executed once end to end by an isolated runner and passed (see KNOWN_LIMITS); two runs on one Ubuntu 24.04.5 x86_64 machine with resident toolchains and an already populated Mathlib cache; first-time downloading and clean-machine restoration were not tested; Windows and macOS were not tested.

## Questions we would like reviewed
1. Does the formal statement of (C) say what the official alternative (C) says? (`docs/02_CORRESPONDENCE_ASSESSMENT.md`, section 4.)
2. For (D): is it right to read the Clay erratum as requiring periodic pressure in the solution class? If not, the formal (D) concerns a smaller class than the printed list. (Section 5.)
3. Is the one-sided smoothness reading on the closed half-space acceptable as standard? (J2.)
4. Are there faults in the formalisation of the definitions in `ComparatorChallenges/NavierStokes.lean`?

The correspondence assessment was written by the packager; it is not an independent referee report. The 166-page informal paper has not been independently refereed in these records.

## Reporting a failure
Open an issue (or message) with: the output of `scripts/reproduce.sh` (`WORKDIR/reproduce.log`), `uname -a`, `lean --version`, `cargo --version`, `go version`, and the step number where it stopped. A failure on a different platform or with a cold Mathlib cache is useful information, not a mistake on your part.

## Contents
- `scripts/reproduce.sh` - the entry point
- `TESTING.md`, `KNOWN_LIMITS.md`, `NOTICE.md`
- `FILES_R2.txt` - the exact list of the 2,674 files in `project/` with sizes
- `docs/01_MATHEMATICAL_ACCOUNT.md`, `docs/02_CORRESPONDENCE_ASSESSMENT.md`, `docs/03_VERIFICATION_SUMMARY.md`
- `project/` - the complete Lean project, including its own `RESTORE_AND_VERIFY.md`
