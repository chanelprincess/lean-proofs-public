# 00 — NS review package R1: index and readiness disposition

Prepared 11 October 2026 (S437), inside the existing submission entry `CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437`. `release_state.json` is HELD and was not touched. Nothing pre-existing in this entry or in the neighbouring entries was modified; this folder was added.

**This is a review package for a kernel-checked formal artifact. It is not a confirmed full solution of any Clay problem, not a claim of Clay acceptance, and not a release.**

## Where things are
| Item | Location |
|---|---|
| Complete Lean project (2,672 regular files; 2,659 Lean modules) | `PROOFS/S412_ESTATE_PORT_v4.34.1/` and the byte-identical archive `ARTIFACTS/s437.lpb.t6.full.project.tar.gz` |
| Proof entry points | `NavierStokes/ComparatorSolution.lean` (two theorems, no `sorry`); challenge statements `ComparatorChallenges/NavierStokes.lean` (two intentional `sorry`); checker config `ComparatorChallenges/NavierStokes.json`; restore notes `RESTORE_AND_VERIFY.md` |
| Verification record | `RECEIPTS/RESULT.json` (20 runner checks), `RECEIPTS/node_return/` (step logs), `ARTIFACTS/…evidence.tar.gz`, `PROVENANCE.json`, `RECONCILIATION.md`, `STATEMENT.md` (earlier, preserved) |
| Mathematical account | `01_MATHEMATICAL_ACCOUNT.md` |
| Official-statement correspondence assessment | `02_CORRESPONDENCE_ASSESSMENT.md` |
| Reproducibility appendix | `03_REPRODUCIBILITY_APPENDIX.md` |
| Provenance, credit, historical limitations | `04_PROVENANCE_AND_CREDIT.md` |
| Machine-readable disposition | `disposition.json` |
| Audit evidence (two attempts, both kept) | `EVIDENCE/package_audit_attempt1_R1/`, `EVIDENCE/package_audit_R1b/` |
| Recovery dossiers | `SESSION_REPORTS/S437_THEOREM_RECOVERY/NS_RECOVERY_DOSSIER_R1_interim.md`, `…R2_chronos_lse_afo.md`, `…R3_native_temporal_and_BAS.md` |

Earlier files in this entry state that statement correspondence "has NOT been reviewed". They are preserved unchanged; that sentence is superseded in scope by `02`, which is a reasoned assessment, still without expert review.

## Disposition — four separate questions
This text is the coordinator's evidence-bound summary. It is not an owner admission or approval receipt, and it creates no authority.

1. **Complete kernel-checked formal artifact — yes, within its scope.** The two declarations `NavierStokes.Comparator.navier_stokes_breakdown_R3` and `…_periodic` are accepted by Lean's default kernel and by nanoda against their challenge statements, with axioms exactly `propext`, `Classical.choice`, `Quot.sound`; 20/20 runner checks; package bound to the executed tree by exact bytes; checker binaries bound to their recorded builds by exact bytes. Scope: Linux only, network restoration, dependency sources not bundled. (03)
2. **Complete review package — assembled, with named unresolved items.**
   - U1 No independent expert review of the formal-to-official correspondence exists; none is claimed or fabricated (02 §6, J5).
   - U2 The periodic alternative (D) depends on reading the Clay erratum as adding pressure periodicity to the solution class; under the opposite reading the machine-checked statement is weaker than the claim (02 §4).
   - U3 The 166-page informal paper has not been independently refereed in these records; the package makes no claim about it beyond what is formalized (01 §4–5).
   - U4 No Lean rebuild from the unpacked package was run (03 §4); Windows and offline restoration are not claimed; dependencies need the network.
   - U5 The nanoda binary's identity is bound by exact comparison to its recorded build, not by an independent rebuild (03 §3).
   - U6 The package's own `RESTORE_AND_VERIFY.md` omits the source of `nanoda_bin` and `landrun`; the supplement is in 03 §5 and the package file was left unchanged.
   - U7 Historical attribution of estate tools to the proof is not established; the estate's own S425 report records the proof as upstream's; the S314/S315 reports and command logs were not found (04 §3). A historical inconsistency about `sorryAx` in the S314 ledger entries is unreconciled and is not a premise of this result (04 §2).
3. **Original-problem correspondence — established by reasoned assessment to the extent stated in `02`.** No mismatched clause was found. Clauses with a closed-half-space smoothness reading are covered in the correct direction. One clause (pressure periodicity in (D)) is reading-dependent. The assessment's standing is that of a documented analysis by an automated coordinator session.
4. **Release / publication — HELD.** The operator word alone releases. External submission, publication, and any institution's acceptance are separate acts, not implied by this folder.

## Statement of what a reader may and may not conclude
- If the formal statements correspond to the official alternatives as assessed in `02`, then the kernel-accepted theorems establish the official alternatives (C) and (D) as stated. The correspondence is documented, not independently reviewed.
- A reader may not conclude that the estate's tools produced the mathematics, that the persistent theorem field has admitted or used this result, or that the problem is accepted as solved.
- Field stop, release holds, previous mints and the completed t6 build are unchanged.

## Reading order
`01` (what is proved and how) → `02` (does it say what the official problem says) → `03` (what was run, what is bound to what) → `04` (who did what, what is unknown) → `disposition.json`.
