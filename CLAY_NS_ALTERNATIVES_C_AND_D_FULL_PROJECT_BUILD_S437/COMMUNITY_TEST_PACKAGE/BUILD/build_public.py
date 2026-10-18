# build_public.py -- build the public community-test archive from the deposited R2 candidate. No hashing; byte equality only.
# Layout: ns-blowup-lean-test/{README.md,TESTING.md,KNOWN_LIMITS.md,NOTICE.md,FILES_R2.txt,scripts/reproduce.sh,docs/*,project/<R2 tree, unchanged>}
import io, json, pathlib, re, sys, tarfile, time
sys.path.insert(0, r"C:\CHAOS_PRODUCTION_COMPLETE\OPERATIONAL_CRYSTALS")
from s437_dispatch_first_kernel import SPOOL

E = pathlib.Path(r"D:\KQAS_NATIVE\VERIFIED_SUBMISSIONS\CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437")
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
TOP = "ns-blowup-lean-test"
ARCHIVE = "ns-blowup-lean-test.tar.gz"
R2 = E / "CANDIDATE_R2" / "s437_ns_candidate_R2.project.tar.gz"
A1, A2 = "s437.nspkg.R2.rebuild", "s437.nspkg.R2.rebuild2"
MATHLIB = "d13f23b723b8a846827a245b89c10fc7d3f11612"
PRIVATE = re.compile(r"ktsadmin|michael-server|/home/|[A-Za-z]:\\|KQAS|CHAOS_PRODUCTION|chaos_node|inthedigitalmix|@gmail")

def rj(j): return json.load(open(SPOOL / "returned" / j / (j + ".result.json"), encoding="utf-8"))

# ---- R2 project files, exactly ----
t = tarfile.open(R2)
tops = {m.name.split("/", 1)[0] for m in t.getmembers()}; assert len(tops) == 1
r2top = tops.pop()
proj = {m.name.split("/", 1)[1]: t.extractfile(m).read() for m in t.getmembers() if m.isreg()}
assert len(proj) == 2674
lake = proj["lakefile.toml"].decode(); man = json.loads(proj["lake-manifest.json"]); dc = json.loads(proj["DEPENDENCY_CLOSURE.json"])
pin_lake = re.search(r'name = "mathlib"[\s\S]*?rev = "([0-9a-f]{40})"', lake).group(1)
pin_man = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib")
pin_dc = next(p for p in dc["packages"] if p["name"] == "mathlib")
assert pin_lake == pin_man == pin_dc["manifest_rev"] == pin_dc["checked_out_head"] == MATHLIB, (pin_lake, pin_man, pin_dc)
a1, a2 = rj(A1), rj(A2)
assert a1["outcome"] == a2["outcome"] == "VERIFIED"
steps = (E / "CANDIDATE_R2" / "restore_steps.txt").read_text(encoding="utf-8").strip().splitlines()
assert len(steps) == 14

# ---- reproduce.sh (steps embedded verbatim from the tested list) ----
STEP_LINES = "\n".join("  %s" % json.dumps(s) for s in steps)
SCRIPT = r'''#!/usr/bin/env bash
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
@@STEPS@@
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
'''.replace("@@STEPS@@", STEP_LINES)

# ---- documents ----
def vs():
    def blk(d, lab):
        ck = d["checks"]; sm = {s["step"]: s for s in d["steps"]}
        th = "; ".join("%s: %s" % (k.split(".")[-1], v["axioms_independent_probe"]) for k, v in d["theorem_outcomes"].items())
        tr = ", ".join("%s=%s" % (x["trial"], x["rc"]) for x in d["trials"])
        return "- %s (%s): outcome **%s**, %d runner checks all passing, wall time %.0f s (challenge step %.0f s). Independent axiom probe: %s. Controls (exit codes): %s." % (lab, d["job_id"], d["outcome"], len(ck), d["elapsed_s"], sm["C1_challenge"]["elapsed_s"], th, tr)
    return ("# Verification summary\n\nThis is a summary of two builder-managed runs of the packaged-source procedure on one Linux machine. It is a record of what was run, not an independent check.\n\n%s\n%s\n\n"
            "Environment of both runs: Ubuntu 24.04.5 LTS, x86_64; Lean 4.34.1; resident toolchains (Lean via elan, Rust, Go, gcc, git) and an already populated Mathlib cache for the pinned revision (`lake exe cache get` found nothing to download in either run). "
            "First-time Mathlib download and clean-machine restoration were **not** tested. Network access was used for the git clones of the pinned dependency repositories and of the two checker tools, for crates (`cargo fetch --locked`) and Go modules (`go mod download`).\n\n"
            "Compiled from source in each run: the project's own modules in the closure of the checked declarations plus the challenge module (not all 2,659 Lean modules of the repository), and the checker tools. Dependency `.olean` files came from the Mathlib cache and dependency builds.\n\n"
            "Not byte-identical: the checker binaries (`nanoda_bin`, `landrun`) built in the two runs differ in length from each other and from an earlier build. The claim is repeatable verification, not reproducible binaries.\n") % (blk(a1, "Run 1"), blk(a2, "Run 2"))

README = """# Lean test package: finite-time blowup for forced Navier-Stokes (Clay alternatives (C) and (D))

This archive lets you independently check, with Lean, two theorems about the forced Navier-Stokes equations, and read how their statements were compared with the official Clay problem text. It is offered for **testing and review**. It does not claim that a Clay Millennium Prize problem has been solved or accepted.

## What is being checked
The two declarations, for every viscosity `nu > 0`:
- `NavierStokes.Comparator.navier_stokes_breakdown_R3` (whole space, Clay alternative (C))
- `NavierStokes.Comparator.navier_stokes_breakdown_periodic` (periodic, Clay alternative (D))

Each says there are smooth data and a smooth force for which no smooth global solution of the stated class exists. The check is Lean's `Comparator` tool: it compares the solution's statements with the challenge statements in `project/ComparatorChallenges/NavierStokes.lean`, replays the solution in the Lean kernel and in the independent `nanoda` kernel, and allows only the axioms `propext`, `Classical.choice`, `Quot.sound`.

## Who did what
The mathematics and the Lean proof are by OpenAI (paper and repository `openai/NavierStokesAndEuler`, Apache-2.0). The challenge statements come from the Formal Conjectures project (Google DeepMind repository, Apache-2.0). The packager ported the proof to Lean 4.34.1 and ran and documented the checks. See `NOTICE.md`. The packager did not author the proof.

## Run it
```
scripts/reproduce.sh [WORKDIR]
```
It copies `project/` into a fresh work directory, builds the two checker tools from pinned source, builds the project's checked closure, runs Comparator's four control projects and then the challenge, and independently prints the axioms of both theorems. Prerequisites, expected output, runtime and disk needs: `TESTING.md`.

Expected final line: `RESULT: PASS -- both declarations accepted by Lean's default kernel and by nanoda ...`

## What was tested, and what was not
See `docs/03_VERIFICATION_SUMMARY.md` and `KNOWN_LIMITS.md`. In short: `scripts/reproduce.sh` itself has not been executed end to end (its commands were verified by a runner that executed the same steps); two runs on one Ubuntu 24.04.5 x86_64 machine with resident toolchains and an already populated Mathlib cache; first-time downloading and clean-machine restoration were not tested; Windows and macOS were not tested.

## Questions we would like reviewed
1. Does the formal statement of (C) say what the official alternative (C) says? (`docs/02_CORRESPONDENCE_ASSESSMENT.md`, section 4.)
2. For (D): is it right to read the Clay erratum as requiring periodic pressure in the solution class? If not, the formal (D) concerns a smaller class than the printed list. (Section 5.)
3. Is the one-sided smoothness reading on the closed half-space acceptable as standard? (J2.)
4. Are there faults in the formalisation of the definitions in `ComparatorChallenges/NavierStokes.lean`?

The correspondence assessment was written by the packager; it is not an independent referee report. The 166-page informal paper has not been independently refereed in these records.

## Reporting a failure
Open an issue (or message) with: the output of `scripts/reproduce.sh` (`WORKDIR/reproduce.log`), `uname -a`, `lean --version`, `cargo --version`, `go version`, and the step number where it stopped. A failure on a different platform or with a cold Mathlib cache is useful information, not a mistake on your part.

## Contents
- `scripts/reproduce.sh` - the entry point
- `TESTING.md`, `KNOWN_LIMITS.md`, `NOTICE.md`
- `FILES_R2.txt` - the exact list of the 2,674 files in `project/` with sizes
- `docs/01_MATHEMATICAL_ACCOUNT.md`, `docs/02_CORRESPONDENCE_ASSESSMENT.md`, `docs/03_VERIFICATION_SUMMARY.md`
- `project/` - the complete Lean project, including its own `RESTORE_AND_VERIFY.md`
"""

TESTING = """# Testing instructions

## 1. Prerequisites (declared, not installed by the script)
Linux x86_64 with a Landlock-enabled kernel (Comparator runs the nanoda kernel under `landrun`, which uses Landlock). Tested only on Ubuntu 24.04.5.

| Tool | Tested with | Notes |
|---|---|---|
| `elan` with Lean `leanprover/lean4:v4.34.1` | 4.34.1 | `lean-toolchain` selects it; elan will install it if missing (network) |
| `git`, `gcc` | 2.43.0, 13.3.0 | |
| Rust (`cargo`, `rustc`) | 1.99.0 | builds `nanoda_bin`; `Cargo.lock` is pinned |
| Go | go1.27.2 | builds `landrun`; the script uses `GOTOOLCHAIN=local` |
| `python3` | 3.12+ | only for the script's own helper checks |
| Network | | git clones, crates, Go modules; and the Mathlib cache if you do not already have it |
| Disk | | several GB to tens of GB (not measured precisely) |

If you lack these: install `elan` (https://github.com/leanprover/elan), Rust (https://rustup.rs) and Go (https://go.dev/dl/) by their own instructions. **We did not test installing them from nothing.**

## 2. The Mathlib cache
The project pins Mathlib at revision `d13f23b723b8a846827a245b89c10fc7d3f11612` (`project/lakefile.toml`, `project/lake-manifest.json`, `project/DEPENDENCY_CLOSURE.json` agree). Step 10 runs `lake exe cache get`: if a cache for that revision exists on your machine it is reused; otherwise it downloads it. Our runs found it already present and downloaded nothing; a first-time download was **not tested**. Do not run `lake update`; the script checks that `lake-manifest.json` is unchanged at the end.

## 3. Run
```
tar xzf ns-blowup-lean-test.tar.gz
cd ns-blowup-lean-test
scripts/reproduce.sh /path/to/fresh/empty/workdir
```
Runtime: the challenge step alone took about 36 minutes in our runs; plan for roughly an hour end to end on a comparable machine.

## 4. What you should see
1. Steps 1-14 announced as `== step n/14`.
2. After step 13, four controls: `simple_match` exit 0, `simple_mismatch` exit 1, `simple_nanoda` exit 0, `simple_nanoda_mismatch` exit 1 (a mismatch control must fail; a checker that accepts it is not trusted).
3. After step 14: Comparator lines `nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`, `Your solution is okay!`.
4. The independent axiom check: each declaration depends only on `propext`, `Classical.choice`, `Quot.sound`.
5. `RESULT: PASS ...`. Any other ending prints `FAIL: ...` with the step.

The two `sorry` tokens in `project/ComparatorChallenges/NavierStokes.lean` are the challenge placeholders; that file is not imported by the solution.

## 5. The procedure by hand
`project/RESTORE_AND_VERIFY.md` lists the same 14 steps in a fenced block; `scripts/reproduce.sh` embeds exactly those commands.

## 6. What a pass means
Repeatable verification of two kernel acceptances against the challenge statements. It does not by itself establish correspondence with the official problem (see `docs/02_CORRESPONDENCE_ASSESSMENT.md`), the correctness of the informal paper, or byte-identical binaries (rebuilt checker binaries differed in length between our runs).
"""

LIMITS = """# Known limits

- **Tested environment**: two runs on one Ubuntu 24.04.5 x86_64 machine with resident Lean, Rust, Go, gcc and git, and an already populated Mathlib cache for the pinned revision. First-time Mathlib download and clean-machine restoration were not tested. Windows and macOS were not tested. No offline restoration is provided.
- **`scripts/reproduce.sh` has not been run end to end.** Its 14 commands are the ones executed and verified twice by a confined runner, and the script was checked statically (bash syntax, exact equality of its steps with `project/RESTORE_AND_VERIFY.md`, archive integrity). Executing the script itself on a machine is exactly the test we are asking for. The runner confined the compile steps (no network, no home directory); the script runs them unconfined, so a difference between the two is possible.
- **Target closure only**: the run compiles the closure of the two checked declarations plus the challenge module, not all 2,659 Lean modules in the repository.
- **Repeatable, not byte-identical**: `nanoda_bin` and `landrun` rebuilt in the two runs differed in length. Only the verification result is claimed to repeat.
- **Correspondence**: the comparison of the formal statements with the official Clay text is the packager's analysis, not an independent review. For (D) it depends on reading the Clay erratum as requiring periodic pressure. Whether (D) also holds without that requirement is open.
- **Informal paper**: not independently refereed in these records.
- **Scope of the theorems**: forced Navier-Stokes alternatives (C) and (D) only; not the unforced alternatives (A) and (B); nothing about the Euler results in the same repository.
- **Not claimed**: Clay acceptance, a prize, or any institutional recognition.
"""

NOTICE = """# Notice and credits
- Mathematics and Lean formalisation of the blowup results: OpenAI, repository `https://github.com/openai/NavierStokesAndEuler` at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, Apache-2.0 (`project/LICENSE`). A 24-file port to Lean 4.34.1 was applied (see `project/UPSTREAM_PROVENANCE.json`).
- Challenge statements: The Formal Conjectures Authors (Google DeepMind), Apache-2.0, as noted in `project/ComparatorChallenges/NavierStokes.lean`.
- Checker: Lean `Comparator` (`leanprover/comparator`), `lean4export`, nanoda (`robsimmons/nanoda_lib`), landrun (`zouuup/landrun`), each at the commit pinned in `project/TOOLS_CLOSURE.json` and `project/DEPENDENCY_CLOSURE.json`.
- Files outside `project/` (this notice, README, TESTING, KNOWN_LIMITS, FILES_R2.txt, scripts/, docs/) were added by the packager. Their licence is to be confirmed by the releasing operator before publication.
- `project/` is byte-identical to the verified R2 candidate (`project/CANDIDATE_CHANGES.md` records how it differs from the earlier verified package: one replaced guide and two added files).
"""

docs = {}
docs["docs/01_MATHEMATICAL_ACCOUNT.md"] = (E / "REVIEW_PACKAGE_R1" / "01_MATHEMATICAL_ACCOUNT.md").read_text(encoding="utf-8")
docs["docs/02_CORRESPONDENCE_ASSESSMENT.md"] = ("> This is the sharpened assessment (it supersedes an earlier version that is not included). It is a packager's analysis, not an independent referee report.\n\n"
    + (E / "REVIEW_PACKAGE_R2" / "02_CORRESPONDENCE_ASSESSMENT_R2.md").read_text(encoding="utf-8"))
docs["docs/03_VERIFICATION_SUMMARY.md"] = vs()
# neutral link/label fixes for the public context
docs["docs/01_MATHEMATICAL_ACCOUNT.md"] = docs["docs/01_MATHEMATICAL_ACCOUNT.md"].replace("(see 03)", "(see `03_VERIFICATION_SUMMARY.md`)").replace("`02_CORRESPONDENCE_ASSESSMENT.md`", "`02_CORRESPONDENCE_ASSESSMENT.md`").replace("PROOFS/S412_ESTATE_PORT_v4.34.1/", "project/")
docs["docs/02_CORRESPONDENCE_ASSESSMENT.md"] = docs["docs/02_CORRESPONDENCE_ASSESSMENT.md"].replace("`REVIEW_PACKAGE_R1/02_CORRESPONDENCE_ASSESSMENT.md`, which is preserved unchanged", "an earlier version")

files = {"README.md": README, "TESTING.md": TESTING, "KNOWN_LIMITS.md": LIMITS, "NOTICE.md": NOTICE, "scripts/reproduce.sh": SCRIPT, **docs}
listing = "\n".join("%s\t%d" % (k, len(v)) for k, v in sorted(proj.items())) + "\n"
files["FILES_R2.txt"] = "# The exact files of the R2 candidate (path<TAB>bytes). %d files. Sizes are byte counts; no hashes are used.\n%s" % (len(proj), listing)
bad = {k: sorted(set(PRIVATE.findall(v)))[:4] for k, v in files.items() if PRIVATE.search(v)}
print("privacy hits in added files:", bad)
# private strings inside the Lean project are the upstream's; report count only
ph = [k for k, v in proj.items() if not k.endswith(".lean") and PRIVATE.search(v.decode("utf-8", "replace"))]
print("non-Lean project files with private-looking strings:", ph)
if bad: sys.exit(2)
# link check
for k, v in files.items():
    if k.endswith(".md"):
        base = pathlib.PurePosixPath(k).parent
        for m in re.finditer(r"\]\(([^)#\s]+)\)", v):
            tgt = m.group(1)
            if "://" in tgt: continue
            p = (base / tgt).as_posix()
            assert p in files or ("project/" + p) in files or p.startswith("project/") and p[8:] in proj, "broken relative link %s in %s" % (tgt, k)

def ti(name, data, mode=0o644):
    x = tarfile.TarInfo(TOP + "/" + name); x.size = len(data); x.mode = mode; x.mtime = int(time.time()); x.uid = x.gid = 0; x.uname = x.gname = ""; return x
dst = OUT / ARCHIVE
with tarfile.open(dst, "w:gz") as o:
    for k in sorted(files):
        d = files[k].encode("utf-8"); o.addfile(ti(k, d, 0o755 if k == "scripts/reproduce.sh" else 0o644), io.BytesIO(d))
    for k in sorted(proj):
        o.addfile(ti("project/" + k, proj[k]), io.BytesIO(proj[k]))
# read back
tb = tarfile.open(dst); names = [m.name for m in tb.getmembers()]
assert len(names) == len(set(names)) and all(n.startswith(TOP + "/") and ".." not in n.split("/") for n in names) and all(m.isreg() for m in tb.getmembers())
back = {m.name[len(TOP) + 1:]: tb.extractfile(m).read() for m in tb.getmembers()}
assert all(back["project/" + k] == v for k, v in proj.items()) and sum(1 for k in back if k.startswith("project/")) == 2674
(OUT / "reproduce.sh").write_bytes(back["scripts/reproduce.sh"])
for k in ("README.md", "TESTING.md", "KNOWN_LIMITS.md"): (OUT / k).write_text(back[k].decode(), encoding="utf-8")
print(json.dumps({"archive": ARCHIVE, "bytes": dst.stat().st_size, "members": len(names), "project_files": 2674, "added_files": len(files), "mathlib_pin": MATHLIB, "pin_sources_agree": True}, indent=1))
