# Reconciliation and stage separation (S437)

| Stage | State | Evidence |
|---|---|---|
| Delivery to the node | DONE | envelope + bundle in spool/inbox; node size/mtime witnesses equalled local before launch |
| Execution | DONE | job s437.lpb.t6.full, 1817.4 s, Ubuntu 24.04.5, Lean 4.34.1; RECEIPTS/RESULT.json |
| Runner-determined verification | PASS (20/20 checks) | RECEIPTS/RESULT.json `checks`; step logs in RECEIPTS/node_return |
| Return and reconciliation by Chaos | DONE | artifacts pulled; size/mtime witnesses node==local; request binding echoed; package inventory read back |
| Deposit (this folder) | DONE, release_state=HELD | release_state.json |
| Release | NOT DONE | operator word alone releases |
| Admission into the persistent theorem field | NOT DONE | field stop remains; the receiving adapter for fresh results (theorem_kfield_owner) is a separate step |
| Application / later use | NOT DONE | none |

Existing records preserved unchanged (verified by file name/size/mtime before and after placement): CLAY_NS_ALTERNATIVES_C_AND_D, ..._COMPARATOR_VERDICT_S410, ..._S405, ..._SECONDARY_PORT_VERDICT_S412, MINT_CANDIDATE_CLAY_NS_C_AND_D, MINT_PROJECTION_CLAY_NS_C_AND_D, NAVIER_STOKES_BREAKDOWN_S315.

The result file marks its own verdict `reserved_for_chaos_reconciler`: the runner supplied checks; this reconciliation is the Chaos-side grading, and it grades the execution only. It does not mint, admit or release anything.
