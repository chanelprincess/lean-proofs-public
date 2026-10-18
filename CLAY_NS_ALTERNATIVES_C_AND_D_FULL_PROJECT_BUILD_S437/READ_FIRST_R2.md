# Read first (added 11 Oct 2026, S437)

The restore guide inside `PROOFS/S412_ESTATE_PORT_v4.34.1/RESTORE_AND_VERIFY.md` (the t6 tree, unchanged) is INCOMPLETE: it does not say where `nanoda_bin` and `landrun` come from.

Use the candidate distribution package instead: `CANDIDATE_R2/s437_ns_candidate_R2.project.tar.gz`. Its `RESTORE_AND_VERIFY.md` lists every restoration step (checked verbatim by the verifying runner), and the package is byte-identical to the t6 package except for that guide and two added documents (`CANDIDATE_CHANGES.md`, `TOOLS_CLOSURE.json`).

Then read `REVIEW_PACKAGE_R2/00_INDEX_AND_DISPOSITION_R2.md`. Release state is HELD (`release_state.json`, unchanged). Nothing here is a release, an admission into any field, or Clay acceptance.
