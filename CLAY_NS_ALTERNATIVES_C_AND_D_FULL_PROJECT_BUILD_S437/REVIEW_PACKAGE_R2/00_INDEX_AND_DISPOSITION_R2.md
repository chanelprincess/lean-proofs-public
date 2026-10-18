# 00 R2 — Index and disposition (successor generation)

Prepared 11 October 2026 (S437) inside `CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437`. `release_state.json` is HELD and was not touched. `REVIEW_PACKAGE_R1`, the t6 tree, `ARTIFACTS/`, `RECEIPTS/` and all neighbouring entries are unchanged (checked by name/size/mtime before and after the deposit). Directories `CANDIDATE_R2` and `REVIEW_PACKAGE_R2` are descriptive working labels; the protocol defines no generation numbering.

**This is a review package for a kernel-checked formal artifact and a verified packaged-source rebuild. It is not a confirmed full solution of any Clay problem, not Clay acceptance, and not a release.**

## Where things are
| Item | Location |
|---|---|
| Candidate distribution package (complete Lean project + corrected restore guide) | `CANDIDATE_R2/s437_ns_candidate_R2.project.tar.gz`; changed documents unpacked in `CANDIDATE_R2/`; inventory in `candidate_inventory.json` |
| Receiver change, patch scripts, dispatcher, candidate builder | `REVIEW_PACKAGE_R2/RECEIVER_CHANGE/` |
| Reproducibility appendix | `03_REPRODUCIBILITY_APPENDIX_R2.md` |
| Sharpened correspondence assessment | `02_CORRESPONDENCE_ASSESSMENT_R2.md` |
| Operator decision packet | `05_OPERATOR_DECISION_PACKET_R2.md` |
| Machine-readable disposition | `disposition_R2.json` |
| Raw returned evidence (both rebuild attempts, 21 test jobs) | `EVIDENCE/` |
| Earlier package (unchanged) | `../REVIEW_PACKAGE_R1/` (`01` account, `02` assessment, `03` appendix, `04` provenance remain in force except where `02 R2` and `03 R2` supersede) |

## Disposition of P1-P6
| | Item | Status | Evidence |
|---|---|---|---|
| P1 | Bundle-sourced mode in the existing receiver | **Achieved** | 03 R2 §3: valid bundle, 15 negative cases on the node, tool-missing case, legacy regression; backups and rollback recorded |
| P2 | Complete restore instructions in an owner-controlled candidate | **Achieved** | `CANDIDATE_R2`: guide replaced, `TOOLS_CLOSURE.json` and `CANDIDATE_CHANGES.md` added; all other files byte-identical to t6; the runner refuses a guide that does not match its executed steps |
| P3 | Fresh restoration, build and verification from that exact package on a Linux worker | **Achieved, with stated scope** | job `s437.nspkg.R2.rebuild` (VERIFIED) and `s437.nspkg.R2.rebuild2` (VERIFIED); network for git/crates/Go modules; resident Mathlib cache and toolchains; Linux only |
| P4 | Durable class-appropriate receiving disposition | **Partial** | returned evidence deposited and reconciled under the S437 submission entry by this session (builder-managed). No resident class-specific receiving adapter or field owner was invoked (field stop and scope exclusions), so there is no adapter-validated disposition. The runner's result-without-receipt guard exists in code, not separately exercised; duplicate dispatch refusal was exercised |
| P5 | Sharpened correspondence assessment | **Achieved as coordinator analysis; specialist judgments remain** | `02 R2`: per-clause direction checks, erratum cited by location, operators closed by kernel-checked bridges, one OPEN item (D in the larger pressure class), no expert review |
| P6 | Operator decision packet, release HELD | **Achieved** | `05 R2`; release state unchanged |

## Timeline hygiene (embedded text versus runtime events)
The attached history log contains two very long embedded text blocks (line 1, 55,574 characters; line 778, 774,214 characters, inside an exception message) that carry registry text. Statements inside them describe records, not events at the dump time. `REVIEW_PACKAGE_R1/04` already separates them from the 18 short runtime NS lines and from the cycle 324202/324203 events. Checking the earlier recovery documents (`rg` for work-order ids, the cycle numbers and "attached log"): the Track B appendix R2 and the NS recovery dossiers R1 and R2 cite none of them; dossier R3 cites cycle 324202/324203 and `WO-U-059` only from the native CHRONOS per-cycle record and fold-beat ledger (selected-pid list), not from the dump, and its sentence that the attached log had not been seen is superseded by `R1/04 §3`. No timeline in those documents depended on embedded registry text.

## What a reader may and may not conclude
A recipient with the declared prerequisites can restore and rebuild this exact candidate and obtain the two kernel acceptances, as shown on one worker twice. The mathematical correspondence to the official problem remains a documented analysis without expert review (J1, J2, J5-J7 in `02 R2`). Nothing here says the estate's tools produced the mathematics, that the theorem field has admitted or used the result, or that any institution accepts it.
