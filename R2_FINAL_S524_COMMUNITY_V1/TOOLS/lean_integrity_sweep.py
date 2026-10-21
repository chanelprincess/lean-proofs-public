#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrity sweep of a Lean source tree or a tarball of one.
Every .lean file is read with comments (line, nested block, doc) and string/char literals masked, then searched for the constructs below. Standalone: standard library only.
usage: lean_integrity_sweep.py <tarball-or-dir> [--json out.json]
Constructs: sorry, sorryAx, admit, axiom (declaration), native_decide, ofReduceBool/reduceBool, implemented_by, extern, unsafe, #exit, skipKernelTC / kernel-skipping options, trustCompiler, addDecl (kernel bypass by metaprogram)
Rules: zero hits outside ComparatorChallenges/; inside it exactly one `sorry` per challenge theorem (a theorem whose proof is `sorry`)."""
import json, re, sys, tarfile, pathlib

CONSTRUCTS = [
    ("sorry",          re.compile(r"\bsorry\b")),
    ("sorryAx",        re.compile(r"\bsorryAx\b")),
    ("admit",          re.compile(r"\badmit\b")),
    ("axiom",          re.compile(r"(?m)^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*(?:(?:private|protected|noncomputable|unsafe|partial)[ \t]+)*axiom\b")),
    ("native_decide",  re.compile(r"\bnative_decide\b")),
    ("ofReduceBool",   re.compile(r"\b(?:Lean\.)?(?:ofReduceBool|reduceBool|reduceNat)\b")),
    ("implemented_by", re.compile(r"\bimplemented_by\b")),
    ("extern",         re.compile(r"(?:@\[[^\]\n]*\bextern\b|(?m:^)[ \t]*extern\b)")),
    ("unsafe",         re.compile(r"\bunsafe\b")),
    ("#exit",          re.compile(r"#exit\b")),
    ("skipKernelTC",   re.compile(r"\b(?:debug\.skipKernelTC|skipKernelTC|debug\.byAsSorry)\b")),
    ("trustCompiler",  re.compile(r"\btrustCompiler\b|\bLean\.trustCompiler\b")),
    ("addDecl",        re.compile(r"\baddDecl\b|\bDeclaration\.axiomDecl\b")),
]
THM = re.compile(r"(?m)^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*(?:(?:private|protected|nonrec)[ \t]+)*(?:theorem|lemma)\b")


def mask(text):
    """Replace comments and string/char literals with spaces (newlines kept) so line numbers are preserved."""
    out = []; i = 0; n = len(text); depth = 0
    while i < n:
        c = text[i]; two = text[i:i + 2]
        if depth:
            if two == "/-": depth += 1; out += ["  "]; i += 2
            elif two == "-/": depth -= 1; out += ["  "]; i += 2
            else: out.append("\n" if c == "\n" else " "); i += 1
        elif two == "/-": depth = 1; out += ["  "]; i += 2
        elif two == "--":
            while i < n and text[i] != "\n": out.append(" "); i += 1
        elif c == '"':
            out.append(" "); i += 1
            while i < n and text[i] != '"':
                if text[i] == "\\" and i + 1 < n: out += [" ", "\n" if text[i + 1] == "\n" else " "]; i += 2
                else: out.append("\n" if text[i] == "\n" else " "); i += 1
            out.append(" "); i += 1
        elif c == "'" and (re.match(r"'(?:\\.|[^\\'])'", text[i:i + 4])):
            m = re.match(r"'(?:\\.|[^\\'])'", text[i:i + 4]); out.append(" " * len(m.group(0))); i += len(m.group(0))
        else: out.append(c); i += 1
    return "".join(out)


def lines_of(rx, masked):
    return [masked.count("\n", 0, m.start()) + 1 for m in rx.finditer(masked)]


def files_of(src):
    p = pathlib.Path(src)
    if p.is_dir():
        for f in sorted(p.rglob("*.lean")):
            if ".lake" in f.parts: continue
            yield f.relative_to(p).as_posix(), f.read_bytes().decode("utf-8", "replace")
    else:
        with tarfile.open(p, "r:*") as t:
            for m in t.getmembers():
                if m.isfile() and m.name.endswith(".lean") and "/.lake/" not in "/" + m.name:
                    yield m.name.lstrip("./"), t.extractfile(m).read().decode("utf-8", "replace")


def configs_of(src):
    """ComparatorChallenges/*.json files that name a challenge module and the theorems the Comparator checks."""
    p = pathlib.Path(src); out = {}
    def take(name, data):
        try: j = json.loads(data)
        except Exception: return
        if isinstance(j, dict) and "challenge_module" in j and "theorem_names" in j: out[name] = j
    if p.is_dir():
        for f in sorted(p.glob("ComparatorChallenges/*.json")): take(f.relative_to(p).as_posix(), f.read_bytes().decode("utf-8", "replace"))
    else:
        with tarfile.open(p, "r:*") as t:
            for m in t.getmembers():
                nm = m.name.lstrip("./")
                if m.isfile() and nm.startswith("ComparatorChallenges/") and nm.endswith(".json"): take(nm, t.extractfile(m).read().decode("utf-8", "replace"))
    return out


def decl_blocks(masked):
    """{short theorem name: (start_line, end_line)}: a block runs to the next top-level declaration, namespace/end or section line."""
    lines = masked.split("\n"); starts = []
    for i, l in enumerate(lines):
        m = re.match(r"[ \t]*(?:@\[[^\]]*\][ \t]*)*(?:(?:private|protected|noncomputable|nonrec)[ \t]+)*(theorem|lemma|def|abbrev|structure|class|instance|inductive|namespace|end|section|open|variable)\b[ \t]*([A-Za-z0-9_.\u00c0-\uffff']*)", l)
        if m: starts.append((i + 1, m.group(1), m.group(2)))
    blocks = {}
    for k, (ln, kind, nm) in enumerate(starts):
        if kind in ("theorem", "lemma"): blocks[nm.split(".")[-1]] = (ln, (starts[k + 1][0] - 1) if k + 1 < len(starts) else len(lines))
    return blocks


def sweep(src):
    eliminator = None
    hits = []; per_file = {}; disagreements = []; n = 0
    for name, text in files_of(src):
        n += 1; m = mask(text); inside = name.startswith("ComparatorChallenges/")
        mine = lines_of(CONSTRUCTS[0][1], m)
        if eliminator is not None:
            theirs = [i + 1 for i in eliminator(text)]
            # the eliminator's rule is a superset (sorryAx counts): compare with sorry + sorryAx
            mine_x = sorted(set(mine) | set(lines_of(CONSTRUCTS[1][1], m)))
            if mine_x != sorted(theirs): disagreements.append({"file": name, "own": mine_x, "eliminator": sorted(theirs)})
        for kind, rx in CONSTRUCTS:
            for ln in lines_of(rx, m): hits.append({"file": name, "line": ln, "construct": kind, "inside_ComparatorChallenges": inside})
        if inside:
            per_file[name] = {"theorems": len(lines_of(THM, m)), "sorry": len(mine), "_sorry_lines": mine, "_blocks": decl_blocks(m)}
    cfg = configs_of(src); challenge = {}
    for cname, j in cfg.items():
        mod_file = j["challenge_module"].replace(".", "/") + ".lean"; info = per_file.get(mod_file)
        if info is None: challenge[cname] = {"error": "challenge module file %s not found" % mod_file}; continue
        rows = []
        for tn in j["theorem_names"]:
            short = tn.split(".")[-1]; blk = info["_blocks"].get(short)
            cnt = sum(1 for s in info["_sorry_lines"] if blk and blk[0] <= s <= blk[1]) if blk else None
            rows.append({"theorem": tn, "found": blk is not None, "sorry_in_its_body": cnt})
        extra = [s for s in info["_sorry_lines"] if not any(r["found"] and info["_blocks"][r["theorem"].split(".")[-1]][0] <= s <= info["_blocks"][r["theorem"].split(".")[-1]][1] for r in rows)]
        challenge[cname] = {"module_file": mod_file, "theorems": rows, "sorry_lines_outside_the_named_theorems": extra}
    for v in per_file.values(): v.pop("_sorry_lines", None); v.pop("_blocks", None)
    return {"files_scanned": n, "hits": hits, "challenge_files": per_file, "challenge_configs": challenge, "eliminator_available": eliminator is not None, "eliminator_disagreements": disagreements}


def verdict(r):
    outside = [h for h in r["hits"] if not h["inside_ComparatorChallenges"]]
    inside_other = [h for h in r["hits"] if h["inside_ComparatorChallenges"] and h["construct"] != "sorry"]
    bad = {}
    for c, v in r["challenge_configs"].items():
        if "error" in v: bad[c] = v["error"]; continue
        wrong = [t for t in v["theorems"] if not t["found"] or t["sorry_in_its_body"] != 1]
        if wrong or v["sorry_lines_outside_the_named_theorems"]: bad[c] = {"named_theorems_without_exactly_one_sorry": wrong, "sorry_lines_outside_named_theorems": v["sorry_lines_outside_the_named_theorems"]}
    in_cfg_files = {v["module_file"] for v in r["challenge_configs"].values() if "module_file" in v}
    unconfigured = sorted(f for f, v in r["challenge_files"].items() if v["sorry"] and f not in in_cfg_files)
    return {"hits_outside_ComparatorChallenges": len(outside), "non_sorry_constructs_inside_ComparatorChallenges": len(inside_other), "challenge_configs_violating_one_sorry_per_named_theorem": bad,
            "files_in_ComparatorChallenges_with_sorry_but_no_comparator_config": unconfigured, "PASS": not outside and not inside_other and not bad and not r["eliminator_disagreements"]}


if __name__ == "__main__":
    src = sys.argv[1]; r = sweep(src); v = verdict(r); r["verdict"] = v
    print("files scanned: %d | eliminator cross-check: %s | disagreements: %d" % (r["files_scanned"], "not used", len(r["eliminator_disagreements"])))
    print("%-72s %6s  %s" % ("file", "line", "construct"))
    for h in r["hits"]: print("%-72s %6d  %s%s" % (h["file"][:72], h["line"], h["construct"], "   [inside ComparatorChallenges/]" if h["inside_ComparatorChallenges"] else "   [OUTSIDE]"))
    print("challenge configs (named theorem -> sorry lines inside its body):")
    for c, cv in r["challenge_configs"].items(): print("  %-52s %s | sorry outside named theorems: %s" % (c, [(tt["theorem"].split(".")[-1], tt["sorry_in_its_body"]) for tt in cv.get("theorems", [])], cv.get("sorry_lines_outside_the_named_theorems")))
    print("verdict:", json.dumps(v))
    if "--json" in sys.argv: pathlib.Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(r, indent=1), encoding="utf-8")
    sys.exit(0 if v["PASS"] else 1)
