#!/usr/bin/env bash
# VERIFY.sh -- public verification entry point for the R2 community package.
#
#   ./VERIFY.sh <WORKDIR>
#
# WORKDIR must not exist, or must be an empty directory. Nothing outside WORKDIR is written, except the public Mathlib cache that `lake exe cache get`
# maintains in its usual per-user location (declared below). The package directory itself is only read.
#
# What it does, in order (every stage logs its command, stdout, stderr, exit code and wall time under WORKDIR/logs; results.tsv lists them):
#   P0 prerequisites -> S1 package input integrity -> S2 copy project -> S3 pins -> S4/S5 build nanoda_bin and landrun from pinned public sources
#   -> S6 Mathlib cache -> S7 lean4export (toolchain file restored afterwards, also on failure) -> S8 Comparator build -> S9 default build
#   -> S10 explicit solution/challenge modules -> upstream checkout + source binding -> integrity sweep -> route coverage -> theorem bindings
#   -> axiom enumeration over the whole claimed closure -> five Comparator configurations (both kernels) -> four Comparator trial projects
#   -> disposable-copy controls (run concurrently from stage S10 on) -> summary (results.json, SUMMARY.md).
# The exit status is 0 only if every required stage passed. A stage that did not run counts as failed.
#
# Declared network use: github.com (mathlib4, nanoda_lib, landrun, upstream NavierStokesAndEuler, and the pinned Lake dependencies), crates.io and the Go module proxy
# (for the two tools), and the public Mathlib cache that `lake exe cache get` uses. Declared resident components (NOT installed by this script): elan with the
# toolchain leanprover/lean4:v4.34.1, Rust (cargo), Go, gcc, git, python3 (>= 3.9). A cold download of the Mathlib cache was not part of the publisher's run.
set -u -o pipefail
# Open-file limit: on many-core machines the Mathlib cache restore decompresses with many threads at once and fails with "No file descriptors available" under a low
# soft limit. Raise the soft limit as far as the hard limit allows; the prerequisite check below requires at least 8192.
ulimit -n unlimited 2>/dev/null || ulimit -n "$(ulimit -Hn)" 2>/dev/null || true

NANODA_URL="https://github.com/robsimmons/nanoda_lib";   NANODA_REV="68d5ca9db226849b41a6fff59d796ff19d0a8840"
LANDRUN_URL="https://github.com/zouuup/landrun";         LANDRUN_REV="5ed4a3db3a4ad930d577215c6b9abaa19df7f99f"
UPSTREAM_URL="https://github.com/openai/NavierStokesAndEuler"; UPSTREAM_REV="f9e8bc5b38b6e212696e8a30e3e91517af887bbd"
TOOLCHAIN="leanprover/lean4:v4.34.1"
CONFIGS="ClayFefferman ClayFeffermanViaD NavierStokesComplete ClayC ClayD"
ROOTS="ClayStatement NavierStokes.ClayFeffermanSolution NavierStokes.ComparatorCompleteSolution NavierStokes.ComparatorSolution NavierStokes.ClayCSolution NavierStokes.ClayDSolution"

PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${1:-}"
[ -n "$WORK" ] || { echo "usage: $0 <WORKDIR>   (WORKDIR must not exist, or must be an empty directory)"; exit 2; }
case "$WORK" in /*) ;; *) WORK="$PWD/$WORK" ;; esac
if [ -e "$WORK" ]; then
  if [ -d "$WORK" ] && [ -z "$(ls -A "$WORK" 2>/dev/null)" ]; then :; else echo "REFUSING: $WORK exists and is not an empty directory. Choose a fresh path."; exit 2; fi
fi
case "$WORK/" in "$PKG"/*) echo "REFUSING: WORKDIR must be outside the package directory."; exit 2 ;; esac
mkdir -p "$WORK/logs" "$WORK/bin" || { echo "cannot create $WORK"; exit 2; }
T="$WORK/tree"
export PATH="$WORK/bin:$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$PATH"
export GOTOOLCHAIN=local
RES="$WORK/results.tsv"; : > "$RES"
NPROC="$(nproc 2>/dev/null || echo 4)"; JOBS=$(( NPROC / 2 )); [ "$JOBS" -gt 32 ] && JOBS=32; [ "$JOBS" -lt 2 ] && JOBS=2
RUN_START="$(date -u +%FT%TZ)"; RUN_START_S="$(date +%s)"

stage() {   # stage <id> <required 1|0> <description> -- command...   (no pipes between the command and its exit status)
  local id="$1" req="$2" desc="$3"; shift 4
  local t0; t0="$(date +%s.%N)"
  printf '%s\n' "$*" > "$WORK/logs/$id.cmd"
  echo "[$(date -u +%H:%M:%SZ)] START $id: $desc"
  "$@" > "$WORK/logs/$id.out" 2> "$WORK/logs/$id.err"
  local rc=$?
  local t1; t1="$(date +%s.%N)"
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$req" "$rc" "$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')" "$desc" >> "$RES"
  echo "[$(date -u +%H:%M:%SZ)] END   $id rc=$rc"
  return $rc
}
finish() {  # summary is always produced; its exit status is the script's
  [ -n "${CTL_PID:-}" ] && wait "$CTL_PID" 2>/dev/null
  restore_l4e_if_dirty
  python3 "$PKG/TOOLS/summarize.py" --work "$WORK" --pkg "$PKG" --start "$RUN_START" --seconds "$(( $(date +%s) - RUN_START_S ))"
  exit $?
}
abort() { echo "ABORT at stage $1: later stages that depend on it are not run and count as FAILED."; finish; }

# ---------------------------------------------------------------- lean4export: edit the package's toolchain file only around its own build, and restore it
L4E="$T/.lake/packages/lean4export"
restore_l4e_if_dirty() { [ -d "$L4E/.git" ] && [ -n "$(git -C "$L4E" status --porcelain 2>/dev/null)" ] && git -C "$L4E" checkout -- lean-toolchain 2>/dev/null; return 0; }
trap 'restore_l4e_if_dirty' EXIT INT TERM
build_l4e() {
  [ -d "$L4E" ] || { echo "lean4export package missing from the restored dependencies"; return 1; }
  cp "$T/lean-toolchain" "$L4E/lean-toolchain" || return 1
  ( cd "$L4E" && lake build ); local rc=$?
  git -C "$L4E" checkout -- lean-toolchain; local rc2=$?          # restored whether or not the build succeeded
  [ $rc -eq 0 ] || { echo "lean4export build failed (rc=$rc); toolchain file restored (rc=$rc2)"; return 1; }
  [ $rc2 -eq 0 ] || return 1
  install -m 755 "$L4E/.lake/build/bin/lean4export" "$WORK/bin/lean4export" || return 1
  [ -z "$(git -C "$L4E" status --porcelain)" ] || { echo "lean4export checkout is dirty after the restore"; return 1; }
  echo "lean4export built; package checkout clean"
}

# ---------------------------------------------------------------- stage bodies
prereq_check() {
  local miss=0
  for c in git gcc cargo rustc go python3 curl tar sha256sum awk lake lean elan /usr/bin/time; do
    if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then printf 'found   %s\n' "$c"; else printf 'MISSING %s\n' "$c"; miss=1; fi
  done
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || { echo "MISSING python3 >= 3.9"; miss=1; }
  elan toolchain list 2>/dev/null | grep -q "v4.34.1" || { echo "MISSING Lean toolchain $TOOLCHAIN (install it with: elan toolchain install $TOOLCHAIN)"; miss=1; }
  local nofile; nofile="$(ulimit -n)"; echo "open-file limit: $nofile (need >= 8192)"
  if [ "$nofile" != "unlimited" ] && [ "$nofile" -lt 8192 ]; then echo "OPEN-FILE LIMIT TOO LOW (hard limit $(ulimit -Hn)); raise it, e.g. with: ulimit -n 1048576  (or LimitNOFILE in a systemd unit)"; miss=1; fi
  local avail; avail="$(df -P -BG "$WORK" | awk 'NR==2{gsub("G","",$4); print $4}')"
  echo "free disk at WORKDIR: ${avail} GB (need >= 30)"; [ "${avail:-0}" -ge 30 ] || miss=1
  for u in "$UPSTREAM_URL" "$NANODA_URL" "$LANDRUN_URL" https://github.com/leanprover-community/mathlib4; do
    git ls-remote --exit-code "$u" HEAD >/dev/null 2>&1 && echo "network ok: $u" || { echo "NETWORK FAILURE: $u"; miss=1; }
  done
  echo "--- environment"; uname -srm; grep -E '^(PRETTY_NAME)=' /etc/os-release; echo "cores: $NPROC (jobs for parallel stages: $JOBS)"; grep -m1 MemTotal /proc/meminfo
  git --version; gcc --version | head -1; cargo --version; rustc --version; go version; python3 --version
  echo "Landlock in the kernel LSM list: $(grep -o landlock /sys/kernel/security/lsm 2>/dev/null | head -1 || true)"
  return $miss
}
inputs_integrity() { ( cd "$PKG" && sha256sum -c INPUTS.sha256 ); }
copy_project() { cp -a "$PKG/project" "$T"; }
print_pins() {
  echo "lean-toolchain: $(cat "$T/lean-toolchain")"
  ( cd "$T" && lake env lean --version 2>&1 | head -2 )
  python3 - "$T/lake-manifest.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
for p in m["packages"]: print("dependency %-14s rev %s  %s" % (p["name"], p.get("rev"), p.get("url")))
PY
  echo "nanoda_lib pin: $NANODA_REV"; echo "landrun pin:    $LANDRUN_REV"; echo "upstream pin:   $UPSTREAM_REV"
}
build_nanoda() {
  cd "$WORK" && rm -rf nanoda_lib && git clone -q "$NANODA_URL" nanoda_lib && git -C nanoda_lib checkout -q "$NANODA_REV" || return 1
  [ "$(git -C nanoda_lib rev-parse HEAD)" = "$NANODA_REV" ] || { echo "nanoda_lib revision mismatch"; return 1; }
  cargo fetch --locked --manifest-path nanoda_lib/Cargo.toml || return 1
  cargo build --release --offline --locked --manifest-path nanoda_lib/Cargo.toml || return 1
  install -m 755 nanoda_lib/target/release/nanoda_bin "$WORK/bin/nanoda_bin" && sha256sum "$WORK/bin/nanoda_bin"
}
build_landrun() {
  cd "$WORK" && rm -rf landrun_src && git clone -q "$LANDRUN_URL" landrun_src && git -C landrun_src checkout -q "$LANDRUN_REV" || return 1
  [ "$(git -C landrun_src rev-parse HEAD)" = "$LANDRUN_REV" ] || { echo "landrun revision mismatch"; return 1; }
  ( cd landrun_src && go mod download ) || return 1
  ( cd landrun_src && GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off go build -buildvcs=false -o "$WORK/bin/landrun" ./cmd/landrun ) || return 1
  sha256sum "$WORK/bin/landrun"
}
cache_get()   { ( cd "$T" && lake exe cache get ); }
build_comparator() { ( cd "$T" && lake build Comparator/comparator ); }
build_default()    { ( cd "$T" && lake build ); }
build_solutions()  { ( cd "$T" && lake build NavierStokes.ClayFeffermanSolution NavierStokes.ComparatorCompleteSolution NavierStokes.ComparatorSolution NavierStokes.ClayCSolution NavierStokes.ClayDSolution ClayStatement.Bridge ClayStatement.BridgeConverse ComparatorChallenges.ClayA ComparatorChallenges.ClayB ); }
clone_upstream() { cd "$WORK" && rm -rf upstream && git clone -q "$UPSTREAM_URL" upstream && git -C upstream checkout -q "$UPSTREAM_REV" && [ "$(git -C upstream rev-parse HEAD)" = "$UPSTREAM_REV" ]; }
binding_check() { python3 "$PKG/TOOLS/source_binding_check.py" check --project "$PKG/project" --upstream "$WORK/upstream" --patch "$PKG/SOURCE_PATCH/R2_over_upstream.patch" --extra "$PKG/SOURCE_PATCH/R3_additions.txt" --out "$WORK/source_binding.json"; }
sweep()          { python3 "$PKG/TOOLS/lean_integrity_sweep.py" "$PKG/project" --json "$WORK/sweep.json"; }
route_cov()      { python3 "$PKG/TOOLS/route_coverage.py" "$PKG/project"; }
bindings()       { python3 "$PKG/TOOLS/axiom_enum.py" bindings --tree "$T" --out "$WORK/bindings.json" --configs $(for c in $CONFIGS; do printf 'ComparatorChallenges/%s.json ' "$c"; done); }
axiom_enum()     { python3 "$PKG/TOOLS/axiom_enum.py" enum --tree "$T" --out "$WORK/axioms.json" --roots $ROOTS --named "$PKG/TOOLS/named_exact.json" --jobs "$JOBS"; }
cmp_run() {   # cmp_run <config name> ; the checker's own exit status is kept in the time record and in the stage rc
  local c="$1"
  ( cd "$T" && /usr/bin/time -v -o "$WORK/logs/cmp_$c.time" lake exe comparator "ComparatorChallenges/$c.json" )
}
trials() {
  local CMP="$T/.lake/packages/Comparator/.lake/build/bin/comparator" bad=0 P want rc d
  for pw in simple_match:0 simple_mismatch:1 simple_nanoda:0 simple_nanoda_mismatch:1; do
    P="${pw%%:*}"; want="${pw##*:}"; d="$WORK/trials/$P"; mkdir -p "$WORK/trials"
    cp -r "$T/.lake/packages/Comparator/tests/projects/$P" "$d" || { echo "trial project $P missing"; bad=1; continue; }
    cp "$T/lean-toolchain" "$d/lean-toolchain"
    [ -f "$d/lakefile.toml" ] || printf 'name = "comparatortest"\n\n[[lean_lib]]\nname = "Solution"\n\n[[lean_lib]]\nname = "Challenge"\n' > "$d/lakefile.toml"
    ( cd "$d" && timeout 600 lake env "$CMP" config.json > out.txt 2>&1 ); rc=$?
    echo "TRIAL $P: exit $rc (expected $want)"; [ "$rc" = "$want" ] || bad=1
  done
  return $bad
}
controls_group() {   # runs concurrently from stage S10 on; its own results file
  RES="$WORK/results_controls.tsv"; : > "$RES"
  stage C0 1 "disposable copy of the built tree for the controls" -- cp -a --reflink=auto "$T" "$WORK/ctl_tree" || return 1
  stage C1 1 "Lean-level controls and comparator mutation controls (disposable copy)" -- "$PKG/CONTROLS/run_controls.sh" "$WORK/ctl_tree" "$PKG/CONTROLS" "$WORK/controls_out"
  stage C2 1 "source-binding self-test (tampered added/modified file, deleted file, unlisted extra file)" -- python3 "$PKG/TOOLS/source_binding_check.py" selftest --project "$PKG/project" --upstream "$WORK/upstream" --patch "$PKG/SOURCE_PATCH/R2_over_upstream.patch" --extra "$PKG/SOURCE_PATCH/R3_additions.txt" --out "$WORK/source_binding_selftest.json"
}

# ---------------------------------------------------------------- run
echo "R2 community verification | start $RUN_START | package $PKG | workdir $WORK"
stage P0  1 "prerequisites, platform and network" -- prereq_check || abort P0
stage S1  1 "package input integrity (INPUTS.sha256)" -- inputs_integrity || abort S1
stage S2  1 "copy the project to the workdir" -- copy_project || abort S2
stage S3  1 "toolchain and dependency pins" -- print_pins || abort S3
stage S4  1 "build nanoda_bin from the pinned source" -- build_nanoda || abort S4
stage S5  1 "build landrun from the pinned source" -- build_landrun || abort S5
stage S6  1 "restore Mathlib build cache (public cache)" -- cache_get || abort S6
stage S7  1 "build lean4export; restore its toolchain file" -- build_l4e || abort S7
stage S8  1 "build the Comparator" -- build_comparator || abort S8
stage S9  1 "default build (lake build)" -- build_default || abort S9
stage S10 1 "build every claimed solution module and the statement-only challenge modules explicitly" -- build_solutions || abort S10
stage S11 1 "upstream checkout at the pinned revision" -- clone_upstream || abort S11
controls_group > "$WORK/logs/controls_group.log" 2>&1 &
CTL_PID=$!
stage S12 1 "source binding: upstream + shipped patch + listed extra files == shipped project (added and modified files)" -- binding_check
stage S13 1 "integrity sweep (sorry, admit, axiom, native_decide, reduceBool, implemented_by, extern, unsafe, ...)" -- sweep
stage S14 1 "route coverage: every proved route is named by a Comparator configuration" -- route_cov
stage S15 1 "theorem bindings: each configuration's theorems exist in its solution module within the permitted axioms" -- bindings
stage S16 1 "axiom enumeration over the whole claimed closure" -- axiom_enum
for c in $CONFIGS; do stage "K_$c" 1 "Comparator: ComparatorChallenges/$c.json (Lean default kernel and nanoda)" -- cmp_run "$c"; done
stage S17 1 "Comparator trial projects (expected exits 0, 1, 0, 1)" -- trials
finish
