#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Source-binding check (standalone; Python standard library + git).

Question answered: is the shipped Lean project exactly (upstream at the pinned commit) + (the shipped patch) + (the listed additional files)?
  1. a fresh copy of the upstream checkout (given as --upstream, already at the pinned commit) gets `git apply` of the shipped patch;
  2. every file of the shipped project must equal the corresponding file of that result, byte for byte (line endings normalised), whether the patch MODIFIED it or ADDED it;
  3. the only files allowed outside that result are those listed in --extra (one relative path per line);
  4. no file of the patched result may be missing from the shipped project.
The classification (modified / added / extra) is printed. A mismatch names the file.
`selftest` builds disposable copies and proves the check can fail: a tampered ADDED file, a tampered MODIFIED file, a deleted file and an unlisted extra file must each be reported by name.
  source_binding_check.py check    --project P --upstream U --patch X.patch --extra EXTRA.txt [--out OUT.json]
  source_binding_check.py selftest --project P --upstream U --patch X.patch --extra EXTRA.txt [--out OUT.json]"""
import json, pathlib, re, shutil, subprocess, sys, tempfile

SKIP_DIRS = {".git", ".lake", "build"}


def files_of(root):
    root = pathlib.Path(root); out = {}
    for p in root.rglob("*"):
        if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS): out[p.relative_to(root).as_posix()] = p
    return out


def norm(b): return b.replace(b"\r\n", b"\n")


def expected_tree(upstream, patch, tmp):
    dst = pathlib.Path(tmp) / "expected"
    shutil.copytree(upstream, dst, ignore=shutil.ignore_patterns(".git", ".lake"))
    subprocess.run(["git", "init", "-q"], cwd=dst, check=True, capture_output=True)
    r = subprocess.run(["git", "apply", "--whitespace=nowarn", str(pathlib.Path(patch).resolve())], cwd=dst, capture_output=True, text=True)
    if r.returncode: raise SystemExit("patch does not apply to the upstream checkout: " + r.stderr[-400:])
    return dst


def added_and_modified(patch_text):
    added = set(re.findall(r"(?m)^diff --git a/(\S+) b/\S+\nnew file mode", patch_text))
    allf = set(re.findall(r"(?m)^diff --git a/(\S+) b/", patch_text))
    return added, allf - added


def run_check(project, upstream, patch, extra_file):
    project = pathlib.Path(project); extra = {l.strip() for l in pathlib.Path(extra_file).read_text(encoding="utf-8").splitlines() if l.strip()}
    with tempfile.TemporaryDirectory(prefix="srcbind_") as tmp:
        exp = expected_tree(upstream, patch, tmp); E = files_of(exp); P = files_of(project)
        added, modified = added_and_modified(pathlib.Path(patch).read_bytes().decode("utf-8", "replace"))
        problems = []
        for rel, pp in P.items():
            if rel in E:
                if norm(pp.read_bytes()) != norm(E[rel].read_bytes()):
                    kind = "ADDED by the patch" if rel in added else "MODIFIED by the patch" if rel in modified else "unchanged upstream file"
                    problems.append({"file": rel, "problem": "differs from upstream+patch (%s)" % kind})
            elif rel not in extra: problems.append({"file": rel, "problem": "not in upstream+patch and not listed as an extra file"})
        for rel in E:
            if rel not in P: problems.append({"file": rel, "problem": "present in upstream+patch but missing from the project"})
        for rel in extra:
            if rel not in P: problems.append({"file": rel, "problem": "listed as an extra file but missing"})
            if rel in E: problems.append({"file": rel, "problem": "listed as an extra file but also exists in upstream+patch"})
        res = {"project_files": len(P), "upstream_plus_patch_files": len(E), "patch_added": len(added), "patch_modified": len(modified), "extra_files": len(extra), "problems": problems, "PASS": not problems}
    return res


def cmd_check(a):
    res = run_check(a.project, a.upstream, a.patch, a.extra)
    print("project files %d | upstream+patch %d | patch: %d added, %d modified | extra: %d | problems: %d -> %s" % (res["project_files"], res["upstream_plus_patch_files"], res["patch_added"], res["patch_modified"], res["extra_files"], len(res["problems"]), "PASS" if res["PASS"] else "FAIL"))
    for p in res["problems"][:20]: print("  PROBLEM", p["file"], "|", p["problem"])
    if a.out: pathlib.Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    return 0 if res["PASS"] else 1


def cmd_selftest(a):
    base = run_check(a.project, a.upstream, a.patch, a.extra)
    patch_text = pathlib.Path(a.patch).read_bytes().decode("utf-8", "replace"); added, modified = added_and_modified(patch_text)
    results = [{"control": "unaltered copy", "expected": "PASS", "got": "PASS" if base["PASS"] else "FAIL", "ok": base["PASS"]}]
    def trial(label, mutate, must_name):
        with tempfile.TemporaryDirectory(prefix="srcbind_ctl_") as tmp:
            c = pathlib.Path(tmp) / "p"; shutil.copytree(a.project, c, ignore=shutil.ignore_patterns(".git", ".lake")); mutate(c)
            r = run_check(c, a.upstream, a.patch, a.extra); names = {p["file"] for p in r["problems"]}
            ok = (not r["PASS"]) and must_name in names; results.append({"control": label, "expected": "FAIL naming " + must_name, "got": ("FAIL naming %s" % sorted(names)[:3]) if not r["PASS"] else "PASS (the check did not notice)", "ok": ok})
    add = sorted(f for f in added if f.endswith(".lean") and f.startswith("ClayStatement/"))[0]
    mod = sorted(f for f in modified if f.endswith(".lean"))[0]
    trial("tampered ADDED file (%s)" % add, lambda c: (c / add).write_bytes((c / add).read_bytes() + b"\n-- tampered\n"), add)
    trial("tampered MODIFIED file (%s)" % mod, lambda c: (c / mod).write_bytes((c / mod).read_bytes() + b"\n-- tampered\n"), mod)
    trial("deleted ADDED file (%s)" % add, lambda c: (c / add).unlink(), add)
    trial("unlisted extra file (Sneaky.lean)", lambda c: (c / "Sneaky.lean").write_bytes(b"theorem x : 1 = 1 := rfl\n"), "Sneaky.lean")
    ok = all(r["ok"] for r in results)
    for r in results: print("  %-58s expected %-34s got %s | %s" % (r["control"][:58], r["expected"][:34], r["got"][:60], "ok" if r["ok"] else "NOT AS EXPECTED"))
    print("SOURCE_BINDING_SELFTEST", "PASS" if ok else "FAIL")
    if a.out: pathlib.Path(a.out).write_text(json.dumps({"results": results, "PASS": ok}, indent=1), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "selftest"]); ap.add_argument("--project", required=True); ap.add_argument("--upstream", required=True); ap.add_argument("--patch", required=True); ap.add_argument("--extra", required=True); ap.add_argument("--out")
    a = ap.parse_args(); sys.exit(cmd_check(a) if a.cmd == "check" else cmd_selftest(a))
