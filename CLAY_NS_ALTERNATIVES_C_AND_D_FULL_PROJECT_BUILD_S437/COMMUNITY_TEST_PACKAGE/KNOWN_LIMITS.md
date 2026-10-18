# Known limits

- **Tested environment**: two runs on one Ubuntu 24.04.5 x86_64 machine with resident Lean, Rust, Go, gcc and git, and an already populated Mathlib cache for the pinned revision. First-time Mathlib download and clean-machine restoration were not tested. Windows and macOS were not tested. No offline restoration is provided.
- **`scripts/reproduce.sh` has not been run end to end.** Its 14 commands are the ones executed and verified twice by a confined runner, and the script was checked statically (bash syntax, exact equality of its steps with `project/RESTORE_AND_VERIFY.md`, archive integrity). Executing the script itself on a machine is exactly the test we are asking for. The runner confined the compile steps (no network, no home directory); the script runs them unconfined, so a difference between the two is possible.
- **Target closure only**: the run compiles the closure of the two checked declarations plus the challenge module, not all 2,659 Lean modules in the repository.
- **Repeatable, not byte-identical**: `nanoda_bin` and `landrun` rebuilt in the two runs differed in length. Only the verification result is claimed to repeat.
- **Correspondence**: the comparison of the formal statements with the official Clay text is the packager's analysis, not an independent review. For (D) it depends on reading the Clay erratum as requiring periodic pressure. Whether (D) also holds without that requirement is open.
- **Informal paper**: not independently refereed in these records.
- **Scope of the theorems**: forced Navier-Stokes alternatives (C) and (D) only; not the unforced alternatives (A) and (B); nothing about the Euler results in the same repository.
- **Not claimed**: Clay acceptance, a prize, or any institutional recognition.
