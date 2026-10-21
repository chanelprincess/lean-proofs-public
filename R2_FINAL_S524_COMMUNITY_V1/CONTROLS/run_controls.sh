#!/bin/bash
# Public negative and positive controls for the R2 community package.
#   run_controls.sh <TREE-COPY> <CONTROLS-DIR> <OUT-DIR>
# <TREE-COPY> must be a DISPOSABLE, already built copy of the project tree (this script adds library entries to its lakefile.toml and writes control files into it).
# Nothing is written to <CONTROLS-DIR>; raw outputs go to <OUT-DIR>. Needs landrun, nanoda_bin and lean4export on PATH (VERIFY.sh provides them).
# Every control states its expected outcome. A negative control passes ONLY when the intended failure text is observed: a missing executable, a network failure or an
# unrelated compiler error is reported as FAIL. Last line: CONTROLS_RESULT PASS|FAIL (exit 0 / 1).
T=$1; C=$2; OUT=$3
[ -d "$T" ] && [ -d "$C" ] && [ -n "$OUT" ] || { echo "usage: run_controls.sh <tree-copy> <controls-dir> <out-dir>"; exit 2; }
for x in lake python3; do command -v "$x" >/dev/null 2>&1 || { echo "CONTROL prerequisites: FAIL missing $x"; echo "CONTROLS_RESULT FAIL"; exit 1; }; done
for x in landrun nanoda_bin lean4export; do command -v "$x" >/dev/null 2>&1 || { echo "CONTROL prerequisites: FAIL missing $x on PATH"; echo "CONTROLS_RESULT FAIL"; exit 1; }; done
mkdir -p "$OUT" || exit 2; cd "$T" || exit 2; fail=0

# restore the control sources (stored as .lean.txt / .json.txt so that they never parse as part of the project)
for f in $(cd "$C/lean" && find . -type f \( -name '*.lean.txt' -o -name '*.json.txt' \)); do d=${f#./}; d=${d%.txt}; mkdir -p "$(dirname "$d")"; cp "$C/lean/${f#./}" "$d"; done
# the weakened-target bridge chain: the real bridge modules rebuilt against the weakened-force statement
mkdir -p ClayStatementCtl3
for n in BridgeLemmas BridgeSwap BridgeEquiv BridgeConverse Bridge; do
  sed -e 's/import ClayStatement.Fefferman/import ClayStatementCtl.FeffermanWeakForce/' -e 's/import ClayStatement\.\(Bridge[A-Za-z]*\)/import ClayStatementCtl3.\1/' "ClayStatement/$n.lean" > "ClayStatementCtl3/$n.lean"
done
for L in R2Controls ClayStatementCtl ClayStatementCtl3; do grep -q "name = \"$L\"" lakefile.toml || printf '\n[[lean_lib]]\nname = "%s"\nglobs = ["%s.+"]\n' "$L" "$L" >> lakefile.toml; done

ok()  { id=$1; shift; lake build "$@" > "$OUT/$id.txt" 2>&1; rc=$?; if [ $rc -eq 0 ]; then echo "CONTROL $id: ACCEPTED as expected (rc=0)"; else echo "CONTROL $id: FAIL unexpected rejection (rc=$rc)"; fail=1; fi; }
rej() { id=$1; pat=$2; shift 2; lake build "$@" > "$OUT/$id.txt" 2>&1; rc=$?; if [ $rc -ne 0 ] && grep -q "$pat" "$OUT/$id.txt"; then echo "CONTROL $id: REJECTED as expected (rc=$rc; matched '$pat')"; else echo "CONTROL $id: FAIL expected rejection matching '$pat', got rc=$rc"; fail=1; fi; }
cmp_rej() {  # cmp_rej <id> <config name> <diagnostic text that must appear>
  id=$1; cfg=$2; pat=$3; lake exe comparator "ComparatorChallenges/$cfg.json" > "$OUT/$id.txt" 2>&1; rc=$?
  if [ $rc -ne 0 ] && grep -q "$pat" "$OUT/$id.txt"; then echo "CONTROL $id: REJECTED as expected by the Comparator (rc=$rc; matched '$pat'; first diagnostic: $(grep -m1 -E 'uncaught exception|Illegal|does not match' "$OUT/$id.txt" | cut -c1-170))"; else echo "CONTROL $id: FAIL expected a Comparator rejection matching '$pat', got rc=$rc"; fail=1; fi
}

# ---- the real chain and the R3 solutions are accepted (so a rejection below is about the mutant, not about the chain)
ok  REAL_chain_accepted           ClayStatement.BridgeConverse
ok  R3_solution_modules_accepted  NavierStokes.ClayCSolution NavierStokes.ClayDSolution
# ---- import collision: two modules that each work alone must load together
rej R2F1_collision_rejected       "already contains"        R2Controls.F1_Collision
ok  R2F1_resolved_pair_accepted   R2Controls.F1_Resolved
# ---- route coverage: a proved route must be named by a challenge configuration
python3 "$C/route_coverage.py" "$C/fixtures/delivered_pair" > "$OUT/R2F2_delivered.txt" 2>&1; rc=$?
if [ $rc -eq 1 ] && grep -q "clay_navier_stokes_fefferman_via_D" "$OUT/R2F2_delivered.txt"; then echo "CONTROL R2F2_delivered_pair_flagged: REJECTED as expected (uncovered route: via_D)"; else echo "CONTROL R2F2_delivered_pair_flagged: FAIL (rc=$rc)"; fail=1; fi
python3 "$C/route_coverage.py" "$T" > "$OUT/R2F2_tree.txt" 2>&1; rc=$?
if [ $rc -eq 0 ]; then echo "CONTROL R2F2_tree_fully_covered: ACCEPTED as expected ($(tail -1 "$OUT/R2F2_tree.txt"))"; else echo "CONTROL R2F2_tree_fully_covered: FAIL (rc=$rc)"; fail=1; fi
# ---- (C) 'proved' from the periodic theorem must not typecheck
rej C_from_periodic_rejected      "Application type mismatch" NavierStokes.CtlCFromPeriodic
# ---- weakened-target bridge: the one-way direction cannot see the weakening, the converse and the two-way chain can
ok  R2F4_weak_chain_base          ClayStatementCtl3.BridgeSwap
ok  R2F4_oneway_accepts_weak      ClayStatementCtl3.OneWay
rej R2F4_converse_rejects_weak    "Application type mismatch" ClayStatementCtl3.ConverseAttempt
rej R2F4_bridge_equiv_rejects_weak "Application type mismatch" ClayStatementCtl3.BridgeEquiv
# ---- Comparator mutation controls: each mutated challenge or solution must be rejected for the intended reason
lake build ClayStatementCtl.FeffermanNoF5 ClayStatementCtl.FeffermanWeakForce ClayStatementCtl.FeffermanClauseMut ComparatorChallenges.CtlNoF5 ComparatorChallenges.CtlWeakForce ComparatorChallenges.CtlClauseMut ComparatorChallenges.CtlClayCNoF5 ComparatorChallenges.CtlClayDWeakForce NavierStokes.CtlSorry NavierStokes.CtlClayCSorry > "$OUT/MUTANT_MODULES_BUILD.txt" 2>&1; rc=$?
if [ $rc -eq 0 ]; then echo "CONTROL MUTANT_MODULES_BUILD: ACCEPTED as expected (the mutants themselves elaborate; their rejection below is the Comparator's)"; else echo "CONTROL MUTANT_MODULES_BUILD: FAIL (rc=$rc)"; fail=1; fi
cmp_rej MUT_F5_removed_disjunction        CtlNoF5       "Const does not match between challenge and target 'Clay.NavierStokes.FiniteEnergy'"
cmp_rej MUT_force_bound_weakened          CtlWeakForce  "Const does not match between challenge and target 'Clay.NavierStokes.ForceTorus'"
cmp_rej MUT_clause_3_altered              CtlClauseMut  "Const does not match between challenge and target 'Clay.NavierStokes.Initial'"
cmp_rej MUT_sorry_solution                CtlSorry      "Illegal axiom detected: 'sorryAx'"
cmp_rej R3_C_without_F5                   CtlClayCNoF5  "Const does not match between challenge and target"
cmp_rej R3_D_force_bound_weakened         CtlClayDWeakForce "Const does not match between challenge and target"
cmp_rej R3_C_sorry_solution               CtlClayCSorry "Illegal axiom detected: 'sorryAx'"
[ $fail -eq 0 ] && echo "CONTROLS_RESULT PASS" || echo "CONTROLS_RESULT FAIL"
exit $fail
