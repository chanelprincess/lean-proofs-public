#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Route coverage check (R2-F2 control). Standalone, standard library only.
RULE: every theorem a solution module declares inside a challenge's namespace must be named by some Comparator config that points at that solution module.
A theorem that is proved but named by no config is a PROVED ROUTE NO CHALLENGE CHECKS: the kernel never compared its statement against anything.
usage: route_coverage.py <dir-or-tarball>   (exit 0: every route covered; exit 1: at least one uncovered route)
Reads ComparatorChallenges/*.json (challenge_module, solution_module, theorem_names) and the solution module's source (X.lean, else X.lean.txt)."""
import json, pathlib, re, sys, tarfile

def mask(text):
    out = []; i = 0; n = len(text); depth = 0
    while i < n:
        c = text[i]; two = text[i:i + 2]
        if depth:
            if two == "/-": depth += 1; out.append("  "); i += 2
            elif two == "-/": depth -= 1; out.append("  "); i += 2
            else: out.append("\n" if c == "\n" else " "); i += 1
        elif two == "/-": depth = 1; out.append("  "); i += 2
        elif two == "--":
            while i < n and text[i] != "\n": out.append(" "); i += 1
        elif c == '"':
            out.append(" "); i += 1
            while i < n and text[i] != '"':
                if text[i] == "\\" and i + 1 < n: out.append("  "); i += 2
                else: out.append("\n" if text[i] == "\n" else " "); i += 1
            out.append(" "); i += 1
        else: out.append(c); i += 1
    return "".join(out)

def declared_theorems(masked):
    """Fully qualified names of the theorems declared in a file, tracking `namespace X` / `end X`."""
    stack = []; found = []
    for line in masked.split("\n"):
        m = re.match(r"\s*namespace\s+([A-Za-z0-9_.']+)", line)
        if m: stack.append(m.group(1)); continue
        m = re.match(r"\s*end(?:\s+([A-Za-z0-9_.']+))?\s*$", line)
        if m and stack and (m.group(1) is None or m.group(1) == stack[-1]): stack.pop(); continue
        m = re.match(r"\s*(?:@\[[^\]]*\]\s*)*((?:(?:private|protected|nonrec)\s+)*)(?:theorem|lemma)\s+([A-Za-z0-9_.']+)", line)
        if m and "private" not in m.group(1): found.append(".".join(stack + [m.group(2)]))      # a private theorem cannot be named by a config, so it is a helper, not a route
    return found

def read_all(src):
    p = pathlib.Path(src); files = {}
    if p.is_dir():
        for f in p.rglob("*"):
            if f.is_file() and (f.suffix in (".json", ".lean") or f.name.endswith(".lean.txt")) and ".lake" not in f.parts: files[f.relative_to(p).as_posix()] = f.read_bytes().decode("utf-8", "replace")
    else:
        with tarfile.open(p, "r:*") as t:
            for m in t.getmembers():
                nm = m.name.lstrip("./")
                if m.isfile() and "/.lake/" not in "/" + nm and (nm.endswith(".json") or nm.endswith(".lean") or nm.endswith(".lean.txt")): files[nm] = t.extractfile(m).read().decode("utf-8", "replace")
    return files

def check(src):
    files = read_all(src); cfgs = {}
    for name, text in files.items():
        if name.startswith("ComparatorChallenges/") and name.endswith(".json"):
            try: j = json.loads(text)
            except Exception: continue
            if isinstance(j, dict) and "solution_module" in j and "theorem_names" in j: cfgs[name] = j
    by_solution = {}
    for name, j in cfgs.items(): by_solution.setdefault(j["solution_module"], []).append((name, j))
    rows = []
    for sol, lst in sorted(by_solution.items()):
        path = sol.replace(".", "/") + ".lean"; text = files.get(path) or files.get(path + ".txt")
        named = {t for _, j in lst for t in j["theorem_names"]}
        namespaces = {t.rsplit(".", 1)[0] for t in named if "." in t}
        if text is None: rows.append({"solution_module": sol, "error": "solution source not found (%s)" % path}); continue
        decl = declared_theorems(mask(text)); routes = [d for d in decl if any(d.startswith(ns + ".") and "." not in d[len(ns) + 1:] for ns in namespaces)]
        rows.append({"solution_module": sol, "configs": sorted(n for n, _ in lst), "routes_declared": routes, "named_by_a_config": sorted(r for r in routes if r in named), "UNCOVERED": sorted(r for r in routes if r not in named)})
    return rows

if __name__ == "__main__":
    rows = check(sys.argv[1]); bad = 0
    for r in rows:
        if "error" in r: print("ERROR", r["solution_module"], r["error"]); bad += 1; continue
        print("%-44s routes=%d covered=%d UNCOVERED=%s" % (r["solution_module"], len(r["routes_declared"]), len(r["named_by_a_config"]), r["UNCOVERED"])); bad += len(r["UNCOVERED"])
    print("ROUTE_COVERAGE_%s uncovered=%d solution_modules=%d" % ("OK" if not bad else "GAP", bad, len(rows))); sys.exit(0 if not bad else 1)
