# Verification summary

Result: **PASS**

Kind: publisher-executed community-package verification (not an independent replication). Started 2026-10-21T10:20:55Z; wall clock 5678 s.

| Check | Result |
|---|---|
| stage P0 exit code 0 | PASS |
| stage S1 exit code 0 | PASS |
| stage S2 exit code 0 | PASS |
| stage S3 exit code 0 | PASS |
| stage S4 exit code 0 | PASS |
| stage S5 exit code 0 | PASS |
| stage S6 exit code 0 | PASS |
| stage S7 exit code 0 | PASS |
| stage S8 exit code 0 | PASS |
| stage S9 exit code 0 | PASS |
| stage S10 exit code 0 | PASS |
| stage S11 exit code 0 | PASS |
| stage S12 exit code 0 | PASS |
| stage S13 exit code 0 | PASS |
| stage S14 exit code 0 | PASS |
| stage S15 exit code 0 | PASS |
| stage S16 exit code 0 | PASS |
| stage K_ClayFefferman exit code 0 | PASS |
| stage K_ClayFeffermanViaD exit code 0 | PASS |
| stage K_NavierStokesComplete exit code 0 | PASS |
| stage K_ClayC exit code 0 | PASS |
| stage K_ClayD exit code 0 | PASS |
| stage S17 exit code 0 | PASS |
| stage C0 exit code 0 | PASS |
| stage C1 exit code 0 | PASS |
| stage C2 exit code 0 | PASS |
| Comparator ClayFefferman: exit 0, Lean default kernel AND nanoda accept, no exception | PASS |
| Comparator ClayFeffermanViaD: exit 0, Lean default kernel AND nanoda accept, no exception | PASS |
| Comparator NavierStokesComplete: exit 0, Lean default kernel AND nanoda accept, no exception | PASS |
| Comparator ClayC: exit 0, Lean default kernel AND nanoda accept, no exception | PASS |
| Comparator ClayD: exit 0, Lean default kernel AND nanoda accept, no exception | PASS |
| axioms: no dependency outside propext/Classical.choice/Quot.sound over the whole claimed closure; named theorems exactly the three | PASS |
| axioms: no module failed to enumerate | PASS |
| theorem bindings (each configuration's theorems exist in its solution module within the permitted axioms) | PASS |
| integrity sweep verdict | PASS |
| sweep: the only challenge files with a sorry and no Comparator configuration are the two statement-only files (A, B) | PASS |
| route coverage: every proved route is named by a configuration | PASS |
| source binding: upstream + patch + listed extras == shipped project (added and modified files) | PASS |
| source binding self-test: tampered added/modified file, deleted file and unlisted extra file each rejected by name | PASS |
| controls: every named control ran and printed its expected outcome; CONTROLS_RESULT PASS | PASS |
| Comparator trial projects behaved as expected (exits 0,1,0,1) | PASS |

## Comparator

| Configuration | checker exit | Lean default kernel | nanoda | elapsed |
|---|---|---|---|---|
| ClayFefferman | 0 | accepts | accepts | 14:30.17 |
| ClayFeffermanViaD | 0 | accepts | accepts | 14:27.67 |
| NavierStokesComplete | 0 | accepts | accepts | 14:16.41 |
| ClayC | 0 | accepts | accepts | 14:38.80 |
| ClayD | 0 | accepts | accepts | 13:55.11 |

## Axioms

40986 theorems in 619 modules (closure of 620 modules recomputed from the package): 35970 depend on exactly the three axioms, 5016 on a strict subset, 0 on anything else.
