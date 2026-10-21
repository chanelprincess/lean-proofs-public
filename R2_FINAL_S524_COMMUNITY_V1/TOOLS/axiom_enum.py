#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Axiom enumeration and theorem-binding probe (standalone; Python standard library only).

  axiom_enum.py enum     --tree T --out OUT.json --roots M1 M2 ... [--named NAMED.json] [--jobs N]
  axiom_enum.py bindings --tree T --out OUT.json --configs C1.json C2.json ...

enum:      computes the import closure of the given root modules FROM THE SOURCE TREE (nothing is hardcoded), then runs one `lake env lean` per module that
           prints every theorem declared in that module with the axioms it depends on (a memoised dependency walk; inductives, constructors and recursors use
           Lean's own `collectAxioms`). Rule: NO dependency outside {propext, Classical.choice, Quot.sound}. A strict subset is acceptable and is counted separately.
           `--named` lists theorems that are advertised as depending on EXACTLY those three; that exact assertion is checked for each.
           A module whose enumeration fails (nonzero exit, no summary line) fails the whole run: it is never silently skipped.
bindings:  for every Comparator configuration, imports its solution module and prints `#check` and `#print axioms` for each named theorem; requires that each
           theorem exists, and that its axioms are inside the configuration's permitted list and contain no sorryAx."""
import concurrent.futures, json, os, pathlib, re, subprocess, sys, time

STD = {"propext", "Classical.choice", "Quot.sound"}
TMPL = r'''import Lean
import __MOD__

open Lean

abbrev AxM := StateRefT (Std.HashMap Name (Array Name)) CoreM

partial def axsOf (n : Name) : AxM (Array Name) := do
  if let some r := (← get)[n]? then return r
  let env ← getEnv
  let r ← match env.find? n with
    | none => pure #[]
    | some ci =>
      match ci with
      | .axiomInfo _ => pure #[n]
      | .inductInfo _ | .ctorInfo _ | .recInfo _ => (collectAxioms n : CoreM (Array Name))
      | _ => do
        let mut acc : Array Name := #[]
        for c in ci.getUsedConstantsAsSet.toList do
          for a in (← axsOf c) do
            unless acc.contains a do acc := acc.push a
        pure acc
  modify (·.insert n r)
  return r

def runAll (idx : Nat) : AxM (Array String) := do
  let env ← getEnv
  let mut out : Array String := #[]
  for (n, ci) in env.constants.map₁.toList do
    if let .thmInfo _ := ci then
      if env.getModuleIdxFor? n == some idx then
        let a ← axsOf n
        let s := ", ".intercalate ((a.qsort (fun x y => x.toString < y.toString)).toList.map toString)
        out := out.push s!"AX|__MOD__|{n}|[{s}]"
  return out

#eval show CoreM Unit from do
  let env ← getEnv
  let some idx := env.header.moduleNames.findIdx? (· == `__MOD__) | throwError "module __MOD__ not found among the imports"
  let (lines, _) ← (runAll idx).run {}
  for l in lines.qsort (· < ·) do IO.println l
  IO.println s!"MODSUM|__MOD__|{lines.size}"
'''


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
        else: out.append(c); i += 1
    return "".join(out)


def import_graph(tree):
    g = {}
    for p in pathlib.Path(tree).rglob("*.lean"):
        rel = p.relative_to(tree)
        if ".lake" in rel.parts: continue
        mod = ".".join(rel.with_suffix("").parts)
        g[mod] = re.findall(r"(?m)^\s*import\s+([A-Za-z0-9_.']+)", mask(p.read_bytes().decode("utf-8", "replace")))
    return g


def closure(g, roots):
    seen = set(); st = list(roots)
    while st:
        x = st.pop()
        if x in seen or x not in g: continue
        seen.add(x); st.extend(g[x])
    return seen


def lean_run(tree, path, timeout=3000):
    return subprocess.run(["lake", "env", "lean", str(path)], cwd=str(tree), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def cmd_enum(a):
    tree = pathlib.Path(a.tree).resolve(); g = import_graph(tree); roots = list(a.roots)
    missing = [r for r in roots if r not in g]
    if missing: print("ROOT MODULES NOT IN THE TREE:", missing); return 2
    mods = sorted(closure(g, roots)); work = pathlib.Path(a.out).with_suffix(".work"); work.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); results = {}
    def one(m):
        f = work / (m + ".lean"); f.write_text(TMPL.replace("__MOD__", m), encoding="utf-8")
        r = lean_run(tree, f); return m, r.returncode, r.stdout, r.stderr[-400:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for m, rc, so, se in ex.map(one, mods): results[m] = (rc, so, se)
    rows = []; failed = []
    for m, (rc, so, se) in results.items():
        summ = [l for l in so.splitlines() if l.startswith("MODSUM|")]
        if rc != 0 or not summ: failed.append({"module": m, "rc": rc, "stderr_tail": se}); continue
        for l in so.splitlines():
            mm = re.match(r"AX\|([^|]+)\|([^|]+)\|\[(.*)\]$", l)
            if mm: rows.append((mm.group(1), mm.group(2), frozenset(x.strip() for x in mm.group(3).split(",") if x.strip())))
    outside = [(m, n, sorted(s - STD)) for m, n, s in rows if not s <= STD]
    exact = [r for r in rows if r[2] == STD]; subset = [r for r in rows if r[2] < STD]
    named = json.loads(pathlib.Path(a.named).read_bytes().decode("utf-8")) if a.named else []
    have = {n: s for _, n, s in rows}; named_fail = []
    for nm in named:
        if nm not in have: named_fail.append({"theorem": nm, "problem": "not found among the enumerated theorems"})
        elif have[nm] != STD: named_fail.append({"theorem": nm, "problem": "axioms are %s, not exactly the three" % sorted(have[nm])})
    res = {"roots": roots, "closure_modules": len(mods), "modules_enumerated": len(mods) - len(failed), "modules_failed": failed, "theorems": len(rows), "modules_with_theorems": len({r[0] for r in rows}),
           "exactly_the_three": len(exact), "strict_subset_of_the_three": len(subset), "outside_the_three": outside, "named_exact_checked": len(named), "named_exact_failures": named_fail,
           "subset_examples": [(m, n, sorted(s)) for m, n, s in subset[:6]], "seconds": round(time.time() - t0, 1)}
    res["PASS"] = (not failed) and (not outside) and (not named_fail) and bool(rows)
    pathlib.Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    pathlib.Path(a.out).with_suffix(".theorems.txt").write_text("\n".join("%s|%s|%s" % (m, n, ",".join(sorted(s))) for m, n, s in sorted(rows)) + "\n", encoding="utf-8")
    print("closure modules=%d enumerated=%d failed=%d | theorems=%d in %d modules | exactly-three=%d strict-subset=%d outside=%d | named exact %d checked, %d failed | %.0fs | %s" % (
        res["closure_modules"], res["modules_enumerated"], len(failed), res["theorems"], res["modules_with_theorems"], len(exact), len(subset), len(outside), len(named), len(named_fail), res["seconds"], "PASS" if res["PASS"] else "FAIL"))
    return 0 if res["PASS"] else 1


def cmd_bindings(a):
    tree = pathlib.Path(a.tree).resolve(); rows = []; ok_all = True
    work = pathlib.Path(a.out).with_suffix(".work"); work.mkdir(parents=True, exist_ok=True)
    for cf in a.configs:
        c = json.loads(pathlib.Path(tree / cf).read_bytes().decode("utf-8")); perm = set(c["permitted_axioms"])
        src = "import %s\n" % c["solution_module"] + "".join("#check @%s\n#print axioms %s\n" % (t, t) for t in c["theorem_names"])
        f = work / (pathlib.Path(cf).stem + ".lean"); f.write_text(src, encoding="utf-8"); r = lean_run(tree, f); txt = r.stdout + r.stderr; per = []
        for t in c["theorem_names"]:
            flat = re.sub(r"\s+", " ", txt); m = re.search(r"'" + re.escape(t) + r"' depends on axioms: \[([^\]]*)\]", flat); found = m is not None
            ax = sorted(x.strip() for x in m.group(1).split(",") if x.strip()) if m else None
            good = found and set(ax) <= perm and "sorryAx" not in ax
            per.append({"theorem": t, "exists_in_solution_module": found, "axioms": ax, "inside_permitted_list": bool(good)}); ok_all &= bool(good)
        rows.append({"config": cf, "challenge_module": c["challenge_module"], "solution_module": c["solution_module"], "permitted": sorted(perm), "rc": r.returncode, "theorems": per}); ok_all &= (r.returncode == 0)
    pathlib.Path(a.out).write_text(json.dumps({"bindings": rows, "PASS": ok_all}, indent=1, ensure_ascii=False), encoding="utf-8")
    for r_ in rows: print("%-44s rc=%d %s" % (r_["config"], r_["rc"], [(t["theorem"].split(".")[-1], t["axioms"]) for t in r_["theorems"]]))
    print("BINDINGS", "PASS" if ok_all else "FAIL"); return 0 if ok_all else 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    e = sp.add_parser("enum"); e.add_argument("--tree", required=True); e.add_argument("--out", required=True); e.add_argument("--roots", nargs="+", required=True); e.add_argument("--named"); e.add_argument("--jobs", type=int, default=16)
    b = sp.add_parser("bindings"); b.add_argument("--tree", required=True); b.add_argument("--out", required=True); b.add_argument("--configs", nargs="+", required=True)
    a = ap.parse_args(); sys.exit(cmd_enum(a) if a.cmd == "enum" else cmd_bindings(a))
