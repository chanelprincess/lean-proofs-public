# Static packaging tests for the public community archive. Runs on the node (PYTHON_WORK). Does NOT run the Lean build or the script.
# Oracles: exact byte equality with the R2 candidate archive; the guide's own fenced step block; bash's own syntax checker.
import json, os, re, subprocess, tarfile, tempfile
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "out"
if not OUT.is_dir():
    OUT = ROOT / "out_local"; OUT.mkdir(exist_ok=True)
PUB = ROOT / "data" / "ns-blowup-lean-test.tar.gz"
R2 = ROOT / "data" / "r2.project.tar.gz"
TOP = "ns-blowup-lean-test"


def obs(name, **kw):
    with open(OUT / "OBS.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"test": name, **kw}, ensure_ascii=False, sort_keys=True, default=str) + "\n")


def members(p):
    t = tarfile.open(p); r = {}
    for m in t.getmembers():
        r[m.name] = (m, t.extractfile(m).read() if m.isreg() else None)
    return r


PUBM = members(PUB)
R2M = members(R2)
R2TOP = next(iter(R2M)).split("/", 1)[0]
R2F = {n.split("/", 1)[1]: d for n, (m, d) in R2M.items() if m.isreg()}
PF = {n[len(TOP) + 1:]: d for n, (m, d) in PUBM.items() if m.isreg()}


def test_archive_members_are_safe():
    bad = []
    for n, (m, _) in PUBM.items():
        if not (m.isreg() or m.isdir()): bad.append(("special", n))
        if n.startswith("/") or ".." in n.split("/") or "\\" in n: bad.append(("path", n))
        if not n.startswith(TOP + "/"): bad.append(("top", n))
    obs("members", total=len(PUBM), regular=sum(1 for _, (m, _) in PUBM.items() if m.isreg()), problems=bad[:5], top=TOP)
    assert not bad and len(PUBM) == len(set(PUBM))


def test_extraction_stays_inside_destination_and_needs_no_symlinks():
    with tempfile.TemporaryDirectory() as d:
        dest = Path(d).resolve()
        with tarfile.open(PUB) as t:
            try: t.extractall(dest, filter="data")
            except TypeError: t.extractall(dest)
        outside = [p for p in dest.rglob("*") if not str(p.resolve()).startswith(str(dest))]
        links = [p for p in dest.rglob("*") if p.is_symlink()]
        tops = sorted(x.name for x in dest.iterdir())
        sh = dest / TOP / "scripts" / "reproduce.sh"
        obs("extract", top_level=tops, outside=len(outside), symlinks=len(links), script_executable=os.access(sh, os.X_OK))
        assert tops == [TOP] and not outside and not links and os.access(sh, os.X_OK)


def test_project_is_byte_identical_to_r2_candidate():
    proj = {k[len("project/"):]: v for k, v in PF.items() if k.startswith("project/")}
    mism = sorted(k for k in proj if k in R2F and proj[k] != R2F[k]); only_pub = sorted(set(proj) - set(R2F)); only_r2 = sorted(set(R2F) - set(proj))
    obs("project_vs_r2", public_project_files=len(proj), r2_files=len(R2F), byte_mismatch=len(mism), only_public=only_pub[:5], only_r2=only_r2[:5])
    assert not mism and not only_pub and not only_r2 and len(proj) == 2674


def test_file_list_matches_r2_exactly():
    rows = [l.split("\t") for l in PF["FILES_R2.txt"].decode().splitlines() if l and not l.startswith("#")]
    lst = {a: int(b) for a, b in rows}
    obs("file_list", rows=len(rows), distinct=len(lst))
    assert lst == {k: len(v) for k, v in R2F.items()} and len(rows) == len(lst)


def test_script_syntax_and_embedded_steps_equal_the_guide():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "reproduce.sh"; p.write_bytes(PF["scripts/reproduce.sh"])
        r = subprocess.run(["bash", "-n", str(p)], capture_output=True, text=True)
        obs("bash_n", rc=r.returncode, stderr=r.stderr[:200])
        assert r.returncode == 0
    guide = R2F["RESTORE_AND_VERIFY.md"].decode().splitlines()
    i = guide.index("```restore-steps"); j = guide.index("```", i + 1); block = guide[i + 1:j]
    sh = PF["scripts/reproduce.sh"].decode()
    m = re.search(r"STEPS=\(\n([\s\S]*?)\n\)\n", sh)
    embedded = [json.loads(l.strip()) for l in m.group(1).splitlines()]
    obs("steps", guide_steps=len(block), embedded_steps=len(embedded), equal=(block == embedded))
    assert len(block) == 14 and block == embedded


def test_script_never_updates_or_changes_pins():
    sh = PF["scripts/reproduce.sh"].decode()
    code = "\n".join(l for l in sh.splitlines() if not l.strip().startswith("#"))
    hits = [w for w in ("lake update", "git checkout -B", "git pull", "rm -rf /", "sudo") if w in code]
    obs("script_hygiene", forbidden_hits=hits, checks_manifest_unchanged="lake-manifest.before" in sh, refuses_nonempty_workdir="is not empty" in sh)
    assert not hits and "lake-manifest.before" in sh and "is not empty" in sh


def test_mathlib_pin_consistent_everywhere():
    pin = "d13f23b723b8a846827a245b89c10fc7d3f11612"
    man = json.loads(PF["project/lake-manifest.json"]); dc = json.loads(PF["project/DEPENDENCY_CLOSURE.json"])
    lk = re.search(r'name = "mathlib"[\s\S]*?rev = "([0-9a-f]{40})"', PF["project/lakefile.toml"].decode()).group(1)
    mm = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib"); dm = next(p for p in dc["packages"] if p["name"] == "mathlib")
    docs = [k for k in PF if k.endswith((".md", ".sh")) and pin in PF[k].decode("utf-8", "replace")]
    wrong = [k for k in PF if k.endswith((".md", ".sh")) and re.search(r"d13f23b7[0-9a-f]*", PF[k].decode("utf-8", "replace")) and not pin in PF[k].decode("utf-8", "replace")]
    obs("pin", lakefile=lk, manifest=mm, closure=dm["manifest_rev"], closure_head=dm["checked_out_head"], docs_naming_full_pin=docs, docs_with_other_d13_strings=wrong)
    assert lk == mm == dm["manifest_rev"] == dm["checked_out_head"] == pin and not wrong


def test_relative_links_resolve_and_wording_limits_present():
    broken = []
    for k, d in PF.items():
        if k.endswith(".md") and not k.startswith("project/"):
            base = Path(k).parent
            for m in re.finditer(r"\]\(([^)#\s]+)\)", d.decode()):
                if "://" in m.group(1): continue
                if (base / m.group(1)).as_posix() not in PF: broken.append((k, m.group(1)))
    txt = (PF["README.md"] + PF["KNOWN_LIMITS.md"] + PF["TESTING.md"]).decode()
    must = ["not tested", "resident", "Target closure only", "Repeatable, not byte-identical", "independent referee"]
    missing = [w for w in must if w.lower() not in txt.lower()]
    forbidden = [w for w in ("first-time download succeeded", "tested on a clean machine", "proves the Millennium", "clean-machine restoration was tested") if w.lower() in txt.lower()]   # positive-claim phrases only; negated mentions of byte-identical binaries are intended wording (attempt 1 flagged one: oracle too crude, retained)
    obs("links_wording", broken=broken, missing_limit_phrases=missing, forbidden_phrases=forbidden)
    assert not broken and not missing and not forbidden


def test_privacy_scan_of_added_files():
    pat = re.compile(r"ktsadmin|michael-server|/home/|[A-Za-z]:\\|KQAS|CHAOS_PRODUCTION|chaos_node|inthedigitalmix|@gmail")
    hits = {k: sorted(set(pat.findall(d.decode("utf-8", "replace"))))[:3] for k, d in PF.items() if not k.startswith("project/") and pat.search(d.decode("utf-8", "replace"))}
    nonlean = {k: 1 for k, d in PF.items() if k.startswith("project/") and not k.endswith(".lean") and pat.search(d.decode("utf-8", "replace"))}
    obs("privacy", added_file_hits=hits, project_nonlean_hits=list(nonlean)[:5])
    assert not hits and not nonlean
