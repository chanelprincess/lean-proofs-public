# 03 R2 — Packaged-source rebuild: reproducibility evidence

Successor to `REVIEW_PACKAGE_R1/03_REPRODUCIBILITY_APPENDIX.md` (preserved unchanged). Every number below is read from the returned result files of the named jobs. No hash was computed anywhere in this work: "identical" means exact byte comparison.

## 1. Management and worker
- **Management path: builder-managed, operator-directed.** This session submitted, observed and received the jobs through the existing authorized route (ssh/scp envelope, `run_v4_once.sh`, `envelope_runner_v4.sh`, outbox). It was not an autonomous Chaos runtime requester; the Chaos runtime requester was not used, and autonomous dispatch was not validated by this work.
- **Worker**: the existing Omniscient node, `Linux-7.0.0-34-generic-x86_64-with-glibc2.39` (Ubuntu 24.04.5 LTS, x86_64). Lean `Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)`.
- All substantive builds, tests and comparisons ran on that node under the existing confinement profiles. Nothing was compiled or checked locally.

## 2. The candidate package and its binding
- Archive `CANDIDATE_R2/s437_ns_candidate_R2.project.tar.gz` (6,618,138 bytes), top directory `S412_ESTATE_PORT_v4.34.1__candidate_R2`. The label "R2" is descriptive; the VERIFIED_SUBMISSIONS protocol (v1.0) defines no candidate-generation numbering, so no canonical ID was invented.
- Membership (exact): 2,674 regular files = 2,671 byte-identical to the t6 package + 1 modified (`RESTORE_AND_VERIFY.md`) + 2 added (`CANDIDATE_CHANGES.md`, `TOOLS_CLOSURE.json`); 0 removed. 2,659 Lean files, all identical to t6.
- Reconciling the earlier counts by membership: the t6 package has 2,672 regular files; of these 2,669 are the git-tracked files of the executed t6 tree and 3 were added by the runner at packaging time (`DEPENDENCY_CLOSURE.json`, `RESTORE_AND_VERIFY.md`, `UPSTREAM_PROVENANCE.json`), as recorded by job `s437.nspkg.R1b.bind`. The candidate replaces one of those three and adds two.
- The runner bound the candidate to the node-produced, runner-VERIFIED reference (`s437.lpb.t6.full`) by exact bytes before any execution: 2,671 identical, modified ['RESTORE_AND_VERIFY.md'], added ['CANDIDATE_CHANGES.md', 'TOOLS_CLOSURE.json'], removed []; 2,666 proof-bearing files (Lean sources, `lakefile*`, `lean-toolchain`, `lake-manifest.json`, `ComparatorChallenges/`, `LICENSE`) compared, all identical: True. The set of permitted differences comes from the trusted request, not from the package.
- The archive the node received (inbox copy) was compared byte-for-byte with the candidate archive at deposit time.
- `PORT.patch` was **not** applied: the package is already ported; the patch remains provenance.

## 3. P1 — bundle-sourced mode added to the existing receiver
**Change** (`RECEIVER_CHANGE/`): new source kind `bundle_package` in `LEAN_PINNED_BUILD`; the legacy `git_base_plus_patch` mode is wrapped, re-indented and otherwise byte-identical in content (checked). Backups on the node: `envelope_runner_v4.sh.bak_bundle_20261011T103934Z` (before any bundle work) and `envelope_runner_v4.sh.bak_bundle2_20261011T111728Z` (attempt-1 bundle runner). Rollback = copy the chosen backup over `envelope_runner_v4.sh`. No new runner, daemon, queue or work class was created; the same launcher lock applies.

**Safeguards implemented and tested on the node:** whole-archive validation before extraction (readable tar; no absolute or `..` paths; only regular files and directories, so no links, devices or special members; no duplicate names; no file/directory overlap; a single declared top directory; no `.git/`, `.lake/`, `build/`, `.olean`, `.ilean`, `.trace`, `.hash` members; member and size limits); extraction only into a fresh workspace; exact-byte binding to a node-produced VERIFIED reference with the permitted differences fixed by the trusted request (proof-bearing paths may not be listed as permitted changes); pinned git-only dependencies (no path dependency); the restore guide's fenced step block must equal, line for line, the steps the runner executes; tool commits are request-pinned and must be clean checkouts; no `lake update`, no mutable branch heads, no patching of ported source; the package supplies no commands and no verdict.

**Focused tests** (all through the real route on the node; each blocked for its intended reason, with the recorded step list showing what executed):

| Job | Outcome | rc | Failing step | Steps run | Recorded reason |
|---|---|---|---|---|---|
| `t1.negallowed` | BLOCKED_REQUEST | 96 | - | 0 | allowed_changes may not include proof-bearing source or configuration: NavierStokes/ComparatorSolution.lean |
| `t1.negdecl` | BLOCKED_REQUEST | 96 | S2_gate | 2 | challenge config in the built tree differs from the request |
| `t1.negduplicate` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: duplicate member: S412_ESTATE_PORT_v4.34.1__candidate_R2/lean-toolchain |
| `t1.negescape` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: invalid path: 'S412_ESTATE_PORT_v4.34.1__candidate_R2/../escape.txt' |
| `t1.negguide` | BLOCKED_SOURCE_MISMATCH | 98 | S2_gate | 0 | restore guide does not document the executed restore steps / tools closure |
| `t1.negmismatch` | BLOCKED_SOURCE_MISMATCH | 98 | S2_gate | 0 | candidate differs from the reference outside the declared changes: modified=['NavierStokes/ComparatorSolution.lean', 'RESTORE_AND_VERIFY.md' |
| `t1.negmissingtool` | EXECUTION_ERROR | 1 | R2_landrun_checkout | 7 | step R2_landrun_checkout rc=128: fatal: reference is not a tree: 1111111111111111111111111111111111111111 |
| `t1.negnotatar` | BLOCKED_REQUEST | 96 | - | 0 | bundle is not a readable tar archive: ReadError("file could not be opened successfully:\n- method gz: ReadError('not a gzip file')\n- method |
| `t1.negoverlap` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: file/directory overlap at S412_ESTATE_PORT_v4.34.1__candidate_R2/NavierStokes/ComparatorSolution.l |
| `t1.negpin` | BLOCKED_SOURCE_MISMATCH | 98 | S2_gate | 2 | manifest pin differs for mathlib |
| `t1.negprebuilt` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: prebuilt or forbidden member: S412_ESTATE_PORT_v4.34.1__candidate_R2/NavierStokes/ComparatorSoluti |
| `t1.negref` | BLOCKED_SOURCE_MISMATCH | 98 | - | 0 | reference job outputs absent in this node's outbox: s437.no.such.job |
| `t1.negsymlink` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: link/device/special member: S412_ESTATE_PORT_v4.34.1__candidate_R2/link |
| `t1.negtoolsrc` | BLOCKED_REQUEST | 96 | - | 0 | tools_source is not allowed in bundle_package mode (tools are restored from pinned source) |
| `t1.negtoplevel` | BLOCKED_REQUEST | 96 | - | 0 | archive rejected whole before extraction: outside the declared top directory: OTHER_TOP/x |
| `t1.negundeclared` | BLOCKED_SOURCE_MISMATCH | 98 | S2_gate | 0 | candidate differs from the reference outside the declared changes: modified=['RESTORE_AND_VERIFY.md'] added=['CANDIDATE_CHANGES.md', 'TOOLS_ |
| `t1.source` | PARTIAL_RUN_COMPLETED_THROUGH_SOURCE | 0 | - | 2 | run_until limit reached; theorem verification not performed |
| `t2.legacyrepo` | BLOCKED_REQUEST | 96 | - | 0 | source.repo_url not in the authorized retrieval set |
| `t2.legacysource` | PARTIAL_RUN_COMPLETED_THROUGH_SOURCE | 0 | - | 10 | run_until limit reached; theorem verification not performed |
| `t3.negmismatch` | BLOCKED_SOURCE_MISMATCH | 98 | S2_gate | 0 | candidate differs from the reference outside the declared changes: modified=['NavierStokes/ComparatorSolution.lean', 'RESTORE_AND_VERIFY.md' |
| `t3.source` | PARTIAL_RUN_COMPLETED_THROUGH_SOURCE | 0 | - | 2 | run_until limit reached; theorem verification not performed |

Coverage statement: a valid bundle (source phase), malformed archive (`negnotatar`), escaping member (`negescape`), duplicate, symlink, overlap, prebuilt artifact, wrong top directory, source mismatch (`negmismatch`: one proof file altered), undeclared addition, a guide that no longer matches the executed steps, wrong manifest pin (`negpin`), missing target (`negdecl`: declaration not in the checked configuration), forbidden field (`negtoolsrc`), proof file listed as a permitted change (`negallowed`), absent reference (`negref`), and a missing tool (`negmissingtool`: a nonexistent landrun commit failed at `git checkout` after nanoda had cloned, checked out and fetched its crates under the retrieval profile). Legacy regression: `legacyrepo` (blocked as before) and `legacysource` (source phase passes, 10 checks). A non-zero checker result is exercised by Comparator's own control projects inside the full jobs (`simple_mismatch` and `simple_nanoda_mismatch` must return 1 and did); no separate injected checker failure was run. Duplicate dispatch of an existing job id was refused by the dispatcher (`ABORT: job id already present on the node`). The runner's own guard for a result that exists without a receipt (completion unknown, not re-executed) is present in the code and was not separately exercised.

## 4. The restoration procedure that was executed
The candidate guide's fenced block (checked equal to the runner's steps) is, in order:
```
git clone https://github.com/robsimmons/nanoda_lib nanoda_lib
git -C nanoda_lib checkout 68d5ca9db226849b41a6fff59d796ff19d0a8840
cargo fetch --locked --manifest-path nanoda_lib/Cargo.toml
cargo build --release --offline --locked --manifest-path nanoda_lib/Cargo.toml
install -m 755 nanoda_lib/target/release/nanoda_bin bin/nanoda_bin
git clone https://github.com/zouuup/landrun landrun_src
git -C landrun_src checkout 5ed4a3db3a4ad930d577215c6b9abaa19df7f99f
(cd landrun_src && go mod download)
(cd landrun_src && GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off go build -buildvcs=false -o ../bin/landrun ./cmd/landrun)
(cd tree && lake exe cache get)
(cd tree/.lake/packages/lean4export && cp ../../../lean-toolchain lean-toolchain && lake build)
install -m 755 tree/.lake/packages/lean4export/.lake/build/bin/lean4export bin/lean4export
(cd tree && lake build Comparator/comparator)
(cd tree && lake exe comparator ComparatorChallenges/NavierStokes.json)
```
Observation: the runner performed these steps, with the network-using ones (steps 1-3, 6-8, 10) in the retrieval profile and the builds and checks (steps 4, 9, 11-14) in the compile profile (no network, no home directory, no credentials, read-only toolchain). It also runs Comparator's four control projects before the challenge. A person following the guide independently was not tested; the guide matches the executed steps by the verbatim check.

## 5. Results
### Attempt 1: job `s437.nspkg.R2.rebuild`
Outcome **VERIFIED** (rc 0), complete run True, elapsed 1774.8 s; 27 runner-determined checks, all pass: True.

Step timings: S3_cache 133.3 s; B1_lean4export_build 7.8 s; B2_comparator_build 10.6 s; R3_nanoda_build 19.5 s; R4_landrun_build 7.3 s; C1_challenge 1550.2 s.
Non-zero step return codes (every one accounted for below): R5_host_rustc rc=127, R5_host_cargo rc=127, B3_tool_probe_nanoda_bin rc=1, T_simple_mismatch rc=1, T_simple_nanoda_mismatch rc=1.
Controls (Comparator's own projects, run before the challenge): simple_match rc=0 (expected 0), simple_mismatch rc=1 (expected 1), simple_nanoda rc=0 (expected 0), simple_nanoda_mismatch rc=1 (expected 1).
Theorem outcomes:
- `NavierStokes.Comparator.navier_stokes_breakdown_R3`: independent probe ['Classical.choice', 'Quot.sound', 'propext']; build-printed ['Classical.choice', 'Quot.sound', 'propext']
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic`: independent probe ['Classical.choice', 'Quot.sound', 'propext']; build-printed ['Classical.choice', 'Quot.sound', 'propext']
Host prerequisites recorded by the job: rustc: /usr/bin/env: ‘/home/ktsadmin/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc’: No such file or directory; cargo: /usr/bin/env: ‘/home/ktsadmin/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo’: No such file or directory; go: go version go1.27.2 linux/amd64; gcc: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; git: git version 2.43.0.
Compile provenance: not recorded by this attempt's runner.
Mathlib cache: `/home/ktsadmin/.cache/mathlib`, entries before 17655, after 17655.

| Check | Result |
|---|---|
| `archive_validated_before_extraction` | pass |
| `candidate_equals_reference_except_declared_changes` | pass |
| `dependencies_are_pinned_git_only` | pass |
| `restore_guide_documents_executed_steps` | pass |
| `confinement_effective:retrieve` | pass |
| `confinement_effective:compile` | pass |
| `toolchain_expected` | pass |
| `manifest_pin:mathlib` | pass |
| `manifest_pin:Comparator` | pass |
| `manifest_pin:lean4export` | pass |
| `challenge_config_matches_request` | pass |
| `dependency_checkouts_match_manifest` | pass |
| `tool_source_at_pinned_commit:nanoda` | pass |
| `tool_source_tree_clean:nanoda` | pass |
| `tool_source_at_pinned_commit:landrun` | pass |
| `tool_source_tree_clean:landrun` | pass |
| `tool_invoked_equals_build_output:nanoda_bin` | pass |
| `tool_invoked_equals_build_output:landrun` | pass |
| `trials_all_as_expected_including_negative_controls` | pass |
| `comparator_rc_zero` | pass |
| `nanoda_kernel_accepts` | pass |
| `lean_default_kernel_accepts` | pass |
| `comparator_okay_line` | pass |
| `statements_exported_for_all_declarations` | pass |
| `no_sorry_warning_outside_challenge_file` | pass |
| `axioms_independent_probe:NavierStokes.Comparator.navier_stokes_breakdown_R3` | pass |
| `axioms_independent_probe:NavierStokes.Comparator.navier_stokes_breakdown_periodic` | pass |

Defect found in attempt 1 and retained: the two Rust host-version probes (`R5_host_rustc`, `R5_host_cargo`) ran without the read-only toolchain bind, returned rc 127 and recorded an error string, so that result lacks cargo/rustc versions. Cause: my change omitted `ro_paths` on those two informational steps (the real `cargo` steps had it). It did not affect any check. Corrected in the runner (`runner_patch2.py`), together with an added gating check and the compile-provenance record, and attempt 2 was run from the same candidate bytes.

### Attempt 2 (final): job `s437.nspkg.R2.rebuild2`
Outcome **VERIFIED** (rc 0), complete run True, elapsed 1824.6 s; 28 runner-determined checks, all pass: True.

Step timings: S3_cache 134.8 s; B1_lean4export_build 7.6 s; B2_comparator_build 11.0 s; R3_nanoda_build 21.2 s; R4_landrun_build 7.2 s; C1_challenge 1596.4 s.
Non-zero step return codes (every one accounted for below): B3_tool_probe_nanoda_bin rc=1, T_simple_mismatch rc=1, T_simple_nanoda_mismatch rc=1.
Controls (Comparator's own projects, run before the challenge): simple_match rc=0 (expected 0), simple_mismatch rc=1 (expected 1), simple_nanoda rc=0 (expected 0), simple_nanoda_mismatch rc=1 (expected 1).
Theorem outcomes:
- `NavierStokes.Comparator.navier_stokes_breakdown_R3`: independent probe ['Classical.choice', 'Quot.sound', 'propext']; build-printed ['Classical.choice', 'Quot.sound', 'propext']
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic`: independent probe ['Classical.choice', 'Quot.sound', 'propext']; build-printed ['Classical.choice', 'Quot.sound', 'propext']
Host prerequisites recorded by the job: rustc: rustc 1.99.0 (b940084d7 2026-09-28); cargo: cargo 1.99.0 (5f94df478 2026-08-27); go: go version go1.27.2 linux/amd64; gcc: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; git: git version 2.43.0.
Compile provenance: project oleans 610 (created after job start: 610); dependency oleans under packages 8934 (created after job start: 8934); workspace bytes {"tree": 10567455247, "nanoda_lib": 84462126, "landrun_src": 327163, "work": 110805724}.
Mathlib cache: `/home/ktsadmin/.cache/mathlib`, entries before 17655, after 17655.

| Check | Result |
|---|---|
| `archive_validated_before_extraction` | pass |
| `candidate_equals_reference_except_declared_changes` | pass |
| `dependencies_are_pinned_git_only` | pass |
| `restore_guide_documents_executed_steps` | pass |
| `confinement_effective:retrieve` | pass |
| `confinement_effective:compile` | pass |
| `toolchain_expected` | pass |
| `manifest_pin:mathlib` | pass |
| `manifest_pin:Comparator` | pass |
| `manifest_pin:lean4export` | pass |
| `challenge_config_matches_request` | pass |
| `dependency_checkouts_match_manifest` | pass |
| `tool_source_at_pinned_commit:nanoda` | pass |
| `tool_source_tree_clean:nanoda` | pass |
| `tool_source_at_pinned_commit:landrun` | pass |
| `tool_source_tree_clean:landrun` | pass |
| `tool_invoked_equals_build_output:nanoda_bin` | pass |
| `tool_invoked_equals_build_output:landrun` | pass |
| `trials_all_as_expected_including_negative_controls` | pass |
| `comparator_rc_zero` | pass |
| `nanoda_kernel_accepts` | pass |
| `lean_default_kernel_accepts` | pass |
| `comparator_okay_line` | pass |
| `statements_exported_for_all_declarations` | pass |
| `no_sorry_warning_outside_challenge_file` | pass |
| `axioms_independent_probe:NavierStokes.Comparator.navier_stokes_breakdown_R3` | pass |
| `axioms_independent_probe:NavierStokes.Comparator.navier_stokes_breakdown_periodic` | pass |
| `project_oleans_compiled_in_this_workspace` | pass |


## 6. Tool identity (bound to the executables actually used)
- **nanoda_bin** (attempt 2): `k:nanoda_bin|1308032|1791717704` = build output `k:nanoda_bin|1308032|1791717704` (exact comparison inside the job); source `robsimmons/nanoda_lib` at `68d5ca9db226849b41a6fff59d796ff19d0a8840`, clean checkout, built with `cargo build --release --offline --locked` after `cargo fetch --locked`. Built from source in this workspace; not copied from S410.
- **landrun** (attempt 2): `k:landrun|7528280|1791717711`; source `zouuup/landrun` at `5ed4a3db3a4ad930d577215c6b9abaa19df7f99f` (the commit recorded by the Go module cache for the S410 version `v0.1.16-0.20251001204025-5ed4a3db3a4a`), built with `go build -buildvcs=false ./cmd/landrun` after `go mod download`; `landrun --version` prints `landrun version 0.1.15` as in S410; Go build info lists the dependency set (in `R4_landrun_buildinfo`).
- **lean4export** at `cacf989bd75f608700820f6afc595f32e7a99a4d` and **comparator** at `19e111e2141cf333c7daff0f64c5f24acc91dd2e`, built in the job with the project toolchain.
- **Comparison with S410's binaries (informational)**: the freshly built nanoda_bin is byte-identical to the S410 copy: False; landrun: False. Sizes differ (nanoda_bin 1308032 vs the S410 copy's recorded 1,306,592 bytes). The same source commit built in a different path and environment is not claimed to give the same bytes; no reproducible-build claim is made. The earlier byte-identity of the S410 `nanoda_bin` to its own cargo output (R1 appendix) remains valid for that artifact. The restored executables are bound to their pinned source and to their build outputs, and both accepted the match controls and rejected the mismatch controls in this job.
- **Measured after the fact (read-only `stat`, `cmp`, `strings` on the node):** the nanoda_bin built in attempt 1 (1,308,000 bytes) and in attempt 2 (1,308,032 bytes) differ in length, so they are not byte-identical to each other; the landrun binaries differ likewise (7,528,288 vs 7,528,280 bytes); both differ in length from the S410 copies (1,306,592 and 7,524,064 bytes). The attempt-2 nanoda_bin contains 30 strings that include the job-specific workspace path; the S410 copy contains none that include its build directory name. Build-path dependence is therefore plausible but was not established, and nothing in this package depends on it.
- The `nanoda_bin --version` probe returns rc 1 because the program expects a configuration file; its output is recorded and is not an identity claim.

## 7. What came from the network, what from resident caches
- **Network retrieval in this job (retrieval profile only):** `git clone` of nanoda_lib and landrun; `lake` cloned the 11 pinned dependency repositories at their manifest revisions (Comparator, mathlib4, lean4export, plausible, LeanSearchClient, import-graph, ProofWidgets4, aesop, quote4, batteries, lean4-cli); `cargo fetch --locked` downloaded the crates from crates.io; `go mod download` fetched the Go modules.
- **Resident caches/prerequisites (not fetched here):** `lake exe cache get` reported "No files to download" and decompressed 8,907 already-cached files from the node's resident Mathlib cache (`~/.cache/mathlib`, 17,655 entries before and after). A first-time download of those files from the cache service was therefore **not exercised**. The Lean toolchain `leanprover/lean4:v4.34.1` (elan), the Rust toolchain, Go, gcc and git were pre-installed; this was not a blank-machine reproduction.
- **Project compiled from source:** the package ships no project `.olean` (the validator forbids them). The job built the project's own modules in the fresh workspace: attempt 2 recorded 610 project oleans, all created after job start. Only the closure of the checked declarations plus the challenge module was built, not every one of the project's 2,659 Lean modules. Dependency oleans come from the cache and dependency builds and are counted, not claimed to be source-rebuilt. A complete source-only rebuild of Mathlib is not claimed.
- Workspace size: `du -sh` on attempt 1's retained workspace reported 4.9 GB (4.7 GB for the project tree); attempt 2's job summed file sizes by name to 10.57 GB for the tree. These are different measures (the sum counts each name separately); they were not reconciled. Plan for several GB to tens of GB of disk.
- Isolation from the earlier workspace: the job's PATH, HOME, caches and tool directories are inside its own workspace; the earlier t6 workspace and the S410 installation were not visible to the confined steps and were not inputs (`tools_source` is rejected in this mode; the S410 binaries were compared afterwards for information only).

## 8. Failed and retained items
- R1b attempt 1 (earlier): two failed tests, both defects in my own oracles; retained.
- This work: (a) my patch script's first run aborted on its own anchor check (my inserted code duplicated an anchor line); no node effect; fixed by ordering. (b) My dispatcher falsely refused the job id `negtool` because its existence check matched the prefix of `negtoolsrc`; nothing launched; the check now matches the id plus a dot. (c) The attempt-1 host-probe defect above.
- Honest limits of `check_all_pass`: a green result means the runner's own checks passed. The verdict class stays `reserved_for_chaos_reconciler`; this appendix is that reconciliation, by this session, not by an autonomous Chaos owner.

## 9. Not established
Windows or offline restoration; a clean machine without resident toolchains or caches; first-time Mathlib cache download; an independent person following the guide by hand; byte-reproducible tool binaries; any statement about the informal paper; the correspondence questions in `02 R2`.
