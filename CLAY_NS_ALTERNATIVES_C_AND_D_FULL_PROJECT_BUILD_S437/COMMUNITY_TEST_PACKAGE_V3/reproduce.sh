#!/usr/bin/env bash
# reproduce.sh -- restore the checker tools, build the project's checked closure, run Lean's Comparator on the two target theorems.
# Derived from the 14-step procedure that was executed and verified (see TESTING.md). The 14 commands below are embedded verbatim.
# It does NOT run `lake update`, does not change any revision, and uses whatever Mathlib cache `lake exe cache get` finds.
# Usage:  scripts/reproduce.sh [WORKDIR]      (default WORKDIR: ./ns-test-work ; must not exist or must be empty)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mkdir -p "${1:-$PWD/ns-test-work}" && cd "${1:-$PWD/ns-test-work}" && pwd)"
LOG="$WORK/reproduce.log"
CONFIG="ComparatorChallenges/NavierStokes.json"
DECLS=("NavierStokes.Comparator.navier_stokes_breakdown_R3" "NavierStokes.Comparator.navier_stokes_breakdown_periodic")
PERMITTED=" propext Classical.choice Quot.sound "
STEPS=(
  "git clone https://github.com/robsimmons/nanoda_lib nanoda_lib"
  "git -C nanoda_lib checkout 68d5ca9db226849b41a6fff59d796ff19d0a8840"
  "cargo fetch --locked --manifest-path nanoda_lib/Cargo.toml"
  "cargo build --release --offline --locked --manifest-path nanoda_lib/Cargo.toml"
  "install -m 755 nanoda_lib/target/release/nanoda_bin bin/nanoda_bin"
  "git clone https://github.com/zouuup/landrun landrun_src"
  "git -C landrun_src checkout 5ed4a3db3a4ad930d577215c6b9abaa19df7f99f"
  "(cd landrun_src && go mod download)"
  "(cd landrun_src && GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off go build -buildvcs=false -o ../bin/landrun ./cmd/landrun)"
  "(cd tree && lake exe cache get)"
  "(cd tree/.lake/packages/lean4export && cp ../../../lean-toolchain lean-toolchain && lake build)"
  "install -m 755 tree/.lake/packages/lean4export/.lake/build/bin/lean4export bin/lean4export"
  "(cd tree && lake build Comparator/comparator)"
  "(cd tree && lake exe comparator ComparatorChallenges/NavierStokes.json)"
)
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
die() { say "FAIL: $*"; exit 1; }

[ -z "$(ls -A "$WORK" 2>/dev/null)" ] || die "WORKDIR $WORK is not empty; choose a fresh directory"
: > "$LOG"
say "reproduce.sh started $(date -u +%FT%TZ); workdir $WORK"
for t in git gcc cargo rustc go lake lean python3 cp install; do command -v "$t" >/dev/null 2>&1 || die "prerequisite not found on PATH: $t (see TESTING.md, prerequisites)"; done
say "tools: $(git --version); $(cargo --version); $(go version); $(gcc --version | head -n 1)"

# fresh project copy, tool and scratch directories inside WORK
cp -a "$HERE/project" "$WORK/tree"
mkdir -p "$WORK/bin" "$WORK/work/cargo" "$WORK/work/go" "$WORK/work/gocache" "$WORK/trial"
cp "$WORK/tree/lake-manifest.json" "$WORK/lake-manifest.before"
export PATH="$WORK/bin:$PATH" CARGO_HOME="$WORK/work/cargo" GOPATH="$WORK/work/go" GOMODCACHE="$WORK/work/go/pkg/mod" GOCACHE="$WORK/work/gocache" GOTOOLCHAIN=local
say "toolchain file: $(cat "$WORK/tree/lean-toolchain")"
say "Mathlib cache directory in use: ${LAKE_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/mathlib} (reused if populated; downloaded by step 10 otherwise)"

# The 14 steps use paths relative to WORKDIR (tree/, bin/, nanoda_lib/, landrun_src/): they must run from there, whatever the caller's current directory is.
cd "$WORK"

n=0
for s in "${STEPS[@]}"; do
  n=$((n+1)); say "== step $n/14: $s"
  case "$n" in
    4) env CARGO_NET_OFFLINE=true bash -c "$s" >>"$LOG" 2>&1 || die "step $n" ;;
    8) env GOFLAGS=-mod=mod bash -c "$s" >>"$LOG" 2>&1 || die "step $n" ;;
    9) env GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off bash -c "$s" >>"$LOG" 2>&1 || die "step $n" ;;
    13) bash -c "$s" >>"$LOG" 2>&1 || die "step $n"
        CMP="$WORK/tree/.lake/packages/Comparator/.lake/build/bin/comparator"; [ -x "$CMP" ] || die "comparator binary missing"
        say "== controls: Comparator's own projects, run before the challenge (expected exit codes 0,1,0,1)"
        TD="$WORK/tree/.lake/packages/Comparator/tests/projects"; ok=1
        for pair in simple_match:0 simple_mismatch:1 simple_nanoda:0 simple_nanoda_mismatch:1; do
          name="${pair%%:*}"; want="${pair##*:}"; cp -a "$TD/$name" "$WORK/trial/$name"; cp "$WORK/tree/lean-toolchain" "$WORK/trial/$name/lean-toolchain"
          [ -f "$WORK/trial/$name/lakefile.toml" ] || printf 'name = "comparatortest"\nversion = "0.1.0"\n\n[[lean_lib]]\nname = "Solution"\n\n[[lean_lib]]\nname = "Challenge"\n' > "$WORK/trial/$name/lakefile.toml"
          set +e; (cd "$WORK/trial/$name" && lake env "$CMP" config.json) >>"$LOG" 2>&1; rc=$?; set -e
          if [ "$rc" = "$want" ]; then say "   control $name: exit $rc (expected $want) ok"; else say "   control $name: exit $rc (expected $want) WRONG"; ok=0; fi
        done
        [ "$ok" = 1 ] || die "a control project did not return its expected result; the checker is not trusted, challenge not run" ;;
    14) set +e; bash -c "$s" >"$WORK/challenge.out" 2>&1; rc=$?; set -e; cat "$WORK/challenge.out" >>"$LOG"
        [ "$rc" = 0 ] || die "comparator exit $rc (see $LOG)"
        for pat in "nanoda kernel accepts the solution" "Lean default kernel accepts the solution" "Your solution is okay!"; do
          grep -q "$pat" "$WORK/challenge.out" || die "expected line not found: $pat"; done
        say "   Comparator: both kernels accept; 'Your solution is okay!'" ;;
    *) bash -c "$s" >>"$LOG" 2>&1 || die "step $n" ;;
  esac
done
# restore steps run from WORK; step 11 and later use the relative layout (tree/, bin/) established above

say "== independent axiom check"
( cd "$WORK/tree" && lake build NavierStokes.ComparatorSolution >>"$LOG" 2>&1 ) || die "building the solution module failed"
{ echo "import NavierStokes.ComparatorSolution"; for d in "${DECLS[@]}"; do echo "#print axioms $d"; done; } > "$WORK/axiom_probe.lean"
( cd "$WORK/tree" && lake env lean "$WORK/axiom_probe.lean" ) > "$WORK/axioms.out" 2>&1 || die "axiom probe failed"
cat "$WORK/axioms.out" >>"$LOG"
for d in "${DECLS[@]}"; do
  line="$(grep -F "'$d' depends on axioms" "$WORK/axioms.out" || true)"; [ -n "$line" ] || die "no axiom line for $d"
  list="$(printf '%s' "$line" | sed -e 's/.*\[//' -e 's/\].*//' | tr ',' ' ')"
  for a in $list; do case "$PERMITTED" in *" $a "*) ;; *) die "axiom not permitted for $d: $a" ;; esac; done
  say "   $d: axioms [${list}]"
done
cmp -s "$WORK/lake-manifest.before" "$WORK/tree/lake-manifest.json" || die "lake-manifest.json changed during the run (it must not)"
say "RESULT: PASS -- both declarations accepted by Lean's default kernel and by nanoda; axioms within {propext, Classical.choice, Quot.sound}; controls as expected; manifest unchanged"
say "log: $LOG"
