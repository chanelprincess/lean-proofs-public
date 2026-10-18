# deposit_public.py -- append-only deposit of the frozen community-test package, drafts and test evidence into the S437 entry.
import json, pathlib, shutil, subprocess, sys, tarfile, tempfile, time
sys.path.insert(0, r"C:\CHAOS_PRODUCTION_COMPLETE\OPERATIONAL_CRYSTALS")
from s437_dispatch_first_kernel import SPOOL

HERE = pathlib.Path(__file__).resolve().parent
EST = HERE.parents[2]
V = pathlib.Path(r"D:\KQAS_NATIVE\VERIFIED_SUBMISSIONS")
E = V / "CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437"
NW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
ARCH = HERE / "out" / "ns-blowup-lean-test.tar.gz"
JOBS = ["s437.pubpkg.R1.static", "s437.pubpkg.R1.static2", "s437.pubpkg.R1.static3"]
FINAL = "s437.pubpkg.R1.static3"


def wit(root):
    return sorted((str(p.relative_to(root)), p.stat().st_size, int(p.stat().st_mtime)) for p in pathlib.Path(root).rglob("*") if p.is_file())


POST = """# DRAFT - NOT POSTED. For the operator to edit and post (Lean Zulip / community channel). Nothing here has been sent.

**Title:** Independent testing wanted: Lean check of two forced Navier-Stokes blowup theorems (Clay alternatives (C) and (D))

We would like help testing a Lean 4 package, and help reading the statements it checks.

**What it is.** The package contains OpenAI's Lean formalisation (repository `openai/NavierStokesAndEuler`, Apache-2.0) of its finite-time blowup results for the *forced* Navier-Stokes equations, ported to Lean 4.34.1, with Mathlib pinned at `d13f23b723b8a846827a245b89c10fc7d3f11612`. Lean's `Comparator` checks the two target theorems against challenge statements taken from the Formal Conjectures project, in Lean's kernel and in nanoda, with axioms limited to `propext`, `Classical.choice`, `Quot.sound`. We did not write the mathematics or the proof; we ported it and ran and documented the checks.

**What it is not.** It is not a claim that a Clay Millennium Prize problem is solved or accepted. The comparison of the formal statements with the official Clay text is our own analysis, not an independent review, and the 166-page informal paper has not been independently refereed in our records.

**How to try it.** `scripts/reproduce.sh WORKDIR` (details in `TESTING.md`). It builds the checker tools from pinned source, runs Comparator's four control projects (two must fail), runs the challenge, and prints the axioms of both theorems. Expected last line: `RESULT: PASS ...`. Runtime was about an hour for us.

**What we tested, honestly.** Two runs of the same 14-step procedure, on one Ubuntu 24.04.5 x86_64 machine, with resident Lean/Rust/Go toolchains and an already populated Mathlib cache; both passed. We did **not** test a first-time Mathlib download, a clean machine, Windows or macOS. `reproduce.sh` itself has been checked statically but **has not been run end to end**: running it is the test we are asking for. We compile the closure of the two target theorems and the challenge module, not all 2,659 Lean modules. We claim repeatable verification, not byte-identical binaries: the rebuilt `nanoda_bin` and `landrun` differed in length between our runs.

**What we would most like reviewed.**
1. Does the formal (C) say what Clay's alternative (C) says?
2. For (D): is reading the Clay erratum as requiring periodic pressure in the solution class right? If not, our (D) concerns a smaller class than the printed list; whether it also holds without that is open.
3. Is the one-sided smoothness reading on the closed half-space acceptable?
4. Any fault in the definitions in `ComparatorChallenges/NavierStokes.lean`.

**If it fails.** Please post `reproduce.log`, `uname -a`, `lean --version`, `cargo --version`, `go version` and the step number. Failures on other platforms or with a cold cache are useful results.

**Download:** [OPERATOR TO ADD LOCATION AFTER UPLOAD - none exists yet] (6.5 MB; contents listed in `FILES_R2.txt`).
**Licence of our added files:** [OPERATOR TO CONFIRM]
"""

PACKET = """# S437 community test release: operator decision packet

Prepared 11 October 2026. Nothing here posts, uploads or releases anything. Release disposition of the exact candidate: **HELD** (`release_state.json` unchanged).

## The frozen candidate
- Archive `COMMUNITY_TEST_PACKAGE/ns-blowup-lean-test.tar.gz`, **6,547,762 bytes**, 2,683 regular files in one top directory `ns-blowup-lean-test/`; `project/` = the 2,674 files of R2, byte-identical (exact comparison on the node, job `%s`).
- Identity: the archive that the node tested (inside the bundle of `%s`) equals the deposited archive byte for byte (compared at deposit). No hash was used.
- Predecessors, preserved: first static test (`s437.pubpkg.R1.static`, 8 passed / 1 failed - an over-broad wording oracle in my test, not a package defect); second (`...static2`, 9/9) tested the archive before the "not run end to end" statement was made explicit in the public text. The final archive differs from it only in that sentence in two documents; the second archive is retained inside the `static2` bundle.

## Reproduction command and expected results
`scripts/reproduce.sh WORKDIR`; expected final line `RESULT: PASS ...`; controls exit 0,1,0,1; both kernels accept; axioms within the three permitted. See `TESTING.md` inside the archive.

## Your checklist
| Item | Status |
|---|---|
| Pinned Mathlib revision | `d13f23b723b8a846827a245b89c10fc7d3f11612`; `lakefile.toml`, `lake-manifest.json`, `DEPENDENCY_CLOSURE.json` agree (checked twice: at build and on the node) |
| Exact files in R2 | `FILES_R2.txt` in the archive: 2,674 files with byte sizes; checked equal to the R2 archive on the node |
| Tester instructions | `TESTING.md` (prerequisites with versions, cache note, run, expected output, what a pass means) |
| Community post draft | `DRAFT_POST_NOT_POSTED.md`; has two operator-owned blanks (download location, licence of our added files) |
| Build artifacts ready | Yes, with the limits below |

## Tested and untested
- Tested on the node (static, 9/9): safe extraction (single top directory, no links, no escapes, executable script), project byte-identical to R2, file list exact, `bash -n` clean, the 14 embedded commands equal the guide's block, no `lake update`/pin changes in the script, pin consistent everywhere, relative links resolve, required limit wording present, no private strings in the added files.
- Reused evidence (not repeated): two verified R2 rebuilds with the resident Mathlib cache and toolchains.
- **Not tested:** `scripts/reproduce.sh` executed end to end (its compile steps are unconfined, unlike the verified runner's); first-time Mathlib download; clean machine; Windows/macOS; offline.
- The empty-cache test was withdrawn by you and was not run.

## What remains yours
1. Decide whether to run `reproduce.sh` once on the node before sharing (about an hour; needs a new receiver mode or a manual run on the node - not built). Sharing without it is consistent with the wording, which says plainly it is untested.
2. Choose the upload location and the licence for the added files, edit the draft, and post it. Posting is yours alone.
3. Say explicitly if you release this exact candidate; the owner record of that release is separate and has not been made.
4. The correspondence questions in the post need people who are not us.

## Limits that must stay in any public wording
Packager's analysis not independent review; (D) depends on the erratum reading; informal paper unrefereed here; target closure only; repeatable not byte-identical; one platform; resident environment.
"""

DISP = {"schema": "NS_COMMUNITY_TEST_DISPOSITION/1", "prepared_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "set_by": "coordinator session from the cited evidence; NOT an owner release record; creates no authority",
        "candidate": {"archive": "ns-blowup-lean-test.tar.gz", "bytes": None, "project_files": 2674, "added_files": 9, "project_equals": "R2 candidate (exact bytes)", "mathlib_pin": "d13f23b723b8a846827a245b89c10fc7d3f11612"},
        "tests": {"static_final": {"job": FINAL, "result": "9 passed"}, "predecessors": {"s437.pubpkg.R1.static": "8 passed, 1 failed (test oracle defect)", "s437.pubpkg.R1.static2": "9 passed (archive before explicit not-run wording)"}},
        "not_tested": ["scripts/reproduce.sh executed end to end", "first-time Mathlib download", "clean machine", "Windows/macOS", "offline restoration"],
        "withdrawn_by_operator": "mandatory empty-cache test",
        "release": {"state": "HELD", "authority": "operator word, recorded by the actual owner", "posting": "not done; not authorized by this record"}}


def main():
    assert not (E / "COMMUNITY_TEST_PACKAGE").exists(), "append-only: destination exists"
    before = {p.name: wit(p) for p in V.iterdir() if p.is_dir()}
    rs = (E / "release_state.json").read_bytes()
    for j in JOBS:   # PYTHON_WORK jobs: explicit file list (the build-job `pull` uses different artifact names)
        d = SPOOL / "returned" / j; d.mkdir(parents=True, exist_ok=True)
        for src in ("chaos_node/spool/logs/%s_pw_stdout.txt" % j, "chaos_node/spool/logs/%s_pw_stderr.txt" % j, "chaos_node/spool/outbox/%s.result.json" % j, "chaos_node/workspace/%s/out/OBS.jsonl" % j):
            r = subprocess.run(["scp", "-p", "-o", "BatchMode=yes", "michael-server:" + src, str(d / pathlib.Path(src).name)], capture_output=True, text=True, timeout=120, creationflags=NW)
            assert r.returncode == 0, (j, src, r.stderr[:120])
    # the archive the node tested == the archive being deposited
    tmp = pathlib.Path(tempfile.mkdtemp()); b = tmp / "b.tar"
    r = subprocess.run(["scp", "-p", "-o", "BatchMode=yes", "michael-server:chaos_node/spool/inbox/%s.bundle.tar" % FINAL, str(b)], capture_output=True, text=True, timeout=300, creationflags=NW); assert r.returncode == 0, r.stderr
    with tarfile.open(b) as t: node_arch = t.extractfile("data/ns-blowup-lean-test.tar.gz").read()
    local = ARCH.read_bytes(); assert node_arch == local, "archive tested on the node differs from the archive to deposit"
    shutil.rmtree(tmp)
    C = E / "COMMUNITY_TEST_PACKAGE"; C.mkdir()
    shutil.copy2(ARCH, C / ARCH.name); assert (C / ARCH.name).read_bytes() == local
    (C / "DRAFT_POST_NOT_POSTED.md").write_text(POST, encoding="utf-8", newline="\n")
    (C / "OPERATOR_DECISION_PACKET.md").write_text(PACKET % (FINAL, FINAL), encoding="utf-8", newline="\n")
    d = dict(DISP); d["candidate"] = dict(d["candidate"], bytes=len(local)); (C / "disposition.json").write_text(json.dumps(d, indent=1), encoding="utf-8", newline="\n")
    for f in ("reproduce.sh", "README.md", "TESTING.md", "KNOWN_LIMITS.md"): shutil.copy2(HERE / "out" / f, C / f)
    ev = C / "EVIDENCE"; ev.mkdir()
    for j in JOBS:
        (ev / j).mkdir()
        for f in (SPOOL / "returned" / j).iterdir():
            shutil.copy2(f, ev / j / f.name); assert (ev / j / f.name).read_bytes() == f.read_bytes()
    bd = C / "BUILD"; bd.mkdir()
    for f in ("build_public.py", "deposit_public.py"): shutil.copy2(HERE / f, bd / f)
    shutil.copy2(HERE / "tests" / "test_public.py", bd / "test_public.py")
    after = {p.name: wit(p) for p in V.iterdir() if p.is_dir() and p.name in before}
    lost = {k: [x for x in v if x not in set(after[k])] for k, v in before.items()}; lost = {k: v for k, v in lost.items() if v}
    assert not lost, lost
    assert (E / "release_state.json").read_bytes() == rs
    # read-back through the deposit
    with tempfile.TemporaryDirectory() as dd:
        with tarfile.open(C / ARCH.name) as t:
            try: t.extractall(dd, filter="data")
            except TypeError: t.extractall(dd)
        root = pathlib.Path(dd) / "ns-blowup-lean-test"
        links = [p for p in pathlib.Path(dd).rglob("*") if p.is_symlink()]
        r2 = {m.name.split("/", 1)[1]: tarfile.open(E / "CANDIDATE_R2" / "s437_ns_candidate_R2.project.tar.gz").extractfile(m).read() for m in tarfile.open(E / "CANDIDATE_R2" / "s437_ns_candidate_R2.project.tar.gz").getmembers() if m.isreg()}
        bad = [k for k, v in r2.items() if (root / "project" / k).read_bytes() != v]
        print("read-back: extracted files", sum(1 for p in root.rglob("*") if p.is_file()), "| symlinks", len(links), "| project files differing from R2:", len(bad), "| script executable:", (root / "scripts" / "reproduce.sh").stat().st_mode & 0o111 != 0)
    print("archive bytes", len(local), "| deposited to", C)
    print("pre-existing files unchanged in all entries (names/size/mtime) and release_state unchanged:", True, "|", json.loads(rs.decode())["release_state"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace"); main()
