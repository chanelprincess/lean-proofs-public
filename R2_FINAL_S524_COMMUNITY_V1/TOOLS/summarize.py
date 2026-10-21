#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Summarise a VERIFY.sh run: results.json and SUMMARY.md. Exit status 0 only if every REQUIRED check passed. Standard library only.
Success is judged from raw evidence: stage exit codes, the checker's own exit status recorded by /usr/bin/time, BOTH kernels' acceptance lines, the JSON results of the
tools, and the controls' own expected-diagnostic lines. A single "okay" line is never enough; a required stage that did not run counts as failed."""
import argparse, json, pathlib, re, sys

CONFIGS = ["ClayFefferman", "ClayFeffermanViaD", "NavierStokesComplete", "ClayC", "ClayD"]
REQUIRED = ["P0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16"] + ["K_" + c for c in CONFIGS] + ["S17", "C0", "C1", "C2"]
CONTROL_IDS = ["REAL_chain_accepted", "R3_solution_modules_accepted", "R2F1_collision_rejected", "R2F1_resolved_pair_accepted", "R2F2_delivered_pair_flagged", "R2F2_tree_fully_covered", "C_from_periodic_rejected", "R2F4_weak_chain_base", "R2F4_oneway_accepts_weak",
               "R2F4_converse_rejects_weak", "R2F4_bridge_equiv_rejects_weak", "MUTANT_MODULES_BUILD", "MUT_F5_removed_disjunction", "MUT_force_bound_weakened", "MUT_clause_3_altered", "MUT_sorry_solution", "R3_C_without_F5", "R3_D_force_bound_weakened", "R3_C_sorry_solution"]
STATEMENT_ONLY = {"ComparatorChallenges/ClayA.lean", "ComparatorChallenges/ClayB.lean"}
LEAN_OK = "Lean default kernel accepts the solution"; NANODA_OK = "nanoda kernel accepts the solution"; OKAY = "Your solution is okay!"


def rd(p): return pathlib.Path(p).read_bytes().decode("utf-8", "replace") if pathlib.Path(p).exists() else ""
def js(p):
    try: return json.loads(rd(p))
    except Exception: return None


def stages(work):
    out = {}
    for f in ("results.tsv", "results_controls.tsv"):
        for line in rd(work / f).splitlines():
            p = line.split("\t")
            if len(p) >= 5: out[p[0]] = {"required": p[1] == "1", "rc": int(p[2]), "seconds": float(p[3]), "description": p[4]}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--work", required=True); ap.add_argument("--pkg", required=True); ap.add_argument("--start", default=""); ap.add_argument("--seconds", default="0"); a = ap.parse_args()
    W = pathlib.Path(a.work); L = W / "logs"; st = stages(W); checks = []; problems = []
    def add(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        if not ok: problems.append("%s: %s" % (name, detail))
    for sid in REQUIRED:
        if sid not in st: add("stage %s ran" % sid, False, "NOT RUN (counts as failed)")
        else: add("stage %s exit code 0" % sid, st[sid]["rc"] == 0, "rc=%d (%s)" % (st[sid]["rc"], st[sid]["description"]))
    comp = {}
    for c in CONFIGS:
        out = rd(L / ("K_%s.out" % c)) + "\n" + rd(L / ("K_%s.err" % c)); tm = rd(L / ("cmp_%s.time" % c))
        ex = re.search(r"Exit status: (\d+)", tm); el = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", tm); mx = re.search(r"Maximum resident set size \(kbytes\): (\d+)", tm)
        d = {"checker_exit_status": int(ex.group(1)) if ex else None, "stage_rc": st.get("K_" + c, {}).get("rc"), "lean_default_kernel_accepts": LEAN_OK in out, "nanoda_accepts": NANODA_OK in out, "okay_line": OKAY in out, "uncaught_exception": "uncaught exception" in out,
             "elapsed": el.group(1) if el else None, "max_rss_kb": int(mx.group(1)) if mx else None}
        d["PASS"] = d["checker_exit_status"] == 0 and d["stage_rc"] == 0 and d["lean_default_kernel_accepts"] and d["nanoda_accepts"] and not d["uncaught_exception"] and d["okay_line"]
        comp[c] = d; add("Comparator %s: exit 0, Lean default kernel AND nanoda accept, no exception" % c, d["PASS"], json.dumps(d))
    ax = js(W / "axioms.json"); add("axioms: no dependency outside propext/Classical.choice/Quot.sound over the whole claimed closure; named theorems exactly the three", bool(ax and ax.get("PASS")), (json.dumps({k: ax[k] for k in ("closure_modules", "modules_enumerated", "theorems", "exactly_the_three", "strict_subset_of_the_three", "named_exact_checked")}) if ax else "axioms.json missing"))
    if ax: add("axioms: no module failed to enumerate", not ax.get("modules_failed"), str(ax.get("modules_failed"))[:200])
    bd = js(W / "bindings.json"); add("theorem bindings (each configuration's theorems exist in its solution module within the permitted axioms)", bool(bd and bd.get("PASS")), str([(b["config"], [t["axioms"] for t in b["theorems"]]) for b in bd["bindings"]])[:300] if bd else "bindings.json missing")
    sw = js(W / "sweep.json"); v = (sw or {}).get("verdict", {})
    add("integrity sweep verdict", bool(sw and v.get("PASS")), json.dumps(v)[:300] if sw else "sweep.json missing")
    unconf = set(v.get("files_in_ComparatorChallenges_with_sorry_but_no_comparator_config", [])) if sw else None
    add("sweep: the only challenge files with a sorry and no Comparator configuration are the two statement-only files (A, B)", unconf == STATEMENT_ONLY, "got %s" % (sorted(unconf) if unconf is not None else None))
    rc_out = rd(L / "S14.out"); add("route coverage: every proved route is named by a configuration", "ROUTE_COVERAGE_OK" in rc_out, rc_out.strip().splitlines()[-1] if rc_out.strip() else "no output")
    sb = js(W / "source_binding.json"); add("source binding: upstream + patch + listed extras == shipped project (added and modified files)", bool(sb and sb.get("PASS")), (json.dumps({k: sb[k] for k in ("project_files", "patch_added", "patch_modified", "extra_files")}) if sb else "missing"))
    sbt = js(W / "source_binding_selftest.json"); add("source binding self-test: tampered added/modified file, deleted file and unlisted extra file each rejected by name", bool(sbt and sbt.get("PASS")), str([(r["control"][:40], r["ok"]) for r in sbt["results"]]) if sbt else "missing")
    c1 = rd(L / "C1.out"); ctl_lines = [l for l in c1.splitlines() if l.startswith("CONTROL ")]
    by_id = {}
    for l in ctl_lines:
        m = re.match(r"CONTROL (\S+):", l)
        if m: by_id[m.group(1)] = l
    missing_ids = [i for i in CONTROL_IDS if i not in by_id]; not_expected = [i for i in CONTROL_IDS if i in by_id and ("as expected" not in by_id[i] or ": FAIL" in by_id[i])]
    add("controls: every named control ran and printed its expected outcome; CONTROLS_RESULT PASS", "CONTROLS_RESULT PASS" in c1 and not missing_ids and not not_expected, "%d of %d named controls present; missing %s; not as expected %s; %d rejected-as-expected, %d accepted-as-expected" % (len(CONTROL_IDS) - len(missing_ids), len(CONTROL_IDS), missing_ids, not_expected, sum("REJECTED as expected" in l for l in ctl_lines), sum("ACCEPTED as expected" in l for l in ctl_lines)))
    tr = [l for l in rd(L / "S17.out").splitlines() if l.startswith("TRIAL ")]; add("Comparator trial projects behaved as expected (exits 0,1,0,1)", len(tr) == 4 and all(re.search(r"exit (\d+) \(expected \1\)", l) for l in tr), "; ".join(tr))
    env = [l for l in rd(L / "P0.out").splitlines() if re.match(r"(Linux|PRETTY_NAME|cores:|MemTotal|git version|gcc|cargo|rustc|go version|Python|Landlock|free disk)", l)]
    pins = [l for l in rd(L / "S3.out").splitlines()]; hashes = [l for l in (rd(L / "S4.out") + rd(L / "S5.out")).splitlines() if re.match(r"[0-9a-f]{64}\s", l)]
    ok = all(c["pass"] for c in checks)
    res = {"schema": "R2_COMMUNITY_VERIFY_RESULT/1", "kind": "publisher-executed community-package verification (not an independent replication)", "started_utc": a.start, "wall_seconds": int(a.seconds), "PASS": ok,
           "stages": {k: v_ for k, v_ in sorted(st.items())}, "comparators": comp, "axioms": ax, "bindings": bd, "sweep_verdict": v, "source_binding": sb, "source_binding_selftest": sbt, "control_lines": ctl_lines, "trials": tr,
           "environment": env, "pins": pins, "tool_hashes_observed": hashes, "checks": checks, "problems": problems,
           "declared": {"network": "github.com (mathlib4, nanoda_lib, landrun, upstream, Lake dependencies), crates.io, Go module proxy, public Mathlib cache", "resident_components_not_installed_by_the_script": "elan + Lean 4.34.1, Rust, Go, gcc, git, python3", "mathlib_cache": "public cache via `lake exe cache get`; a cold download was not part of this run"}}
    (W / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Verification summary", "", "Result: **%s**" % ("PASS" if ok else "FAIL"), "", "Kind: publisher-executed community-package verification (not an independent replication). Started %s; wall clock %d s." % (a.start, int(a.seconds)), "", "| Check | Result |", "|---|---|"]
    md += ["| %s | %s |" % (c["check"][:150], "PASS" if c["pass"] else "**FAIL**") for c in checks]
    md += ["", "## Comparator", "", "| Configuration | checker exit | Lean default kernel | nanoda | elapsed |", "|---|---|---|---|---|"]
    md += ["| %s | %s | %s | %s | %s |" % (c, d["checker_exit_status"], "accepts" if d["lean_default_kernel_accepts"] else "NOT SHOWN", "accepts" if d["nanoda_accepts"] else "NOT SHOWN", d["elapsed"]) for c, d in comp.items()]
    if ax: md += ["", "## Axioms", "", "%d theorems in %d modules (closure of %d modules recomputed from the package): %d depend on exactly the three axioms, %d on a strict subset, %d on anything else." % (ax["theorems"], ax["modules_with_theorems"], ax["closure_modules"], ax["exactly_the_three"], ax["strict_subset_of_the_three"], len(ax["outside_the_three"]))]
    if problems: md += ["", "## Problems", ""] + ["- " + p for p in problems]
    (W / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md)); return 0 if ok else 1


if __name__ == "__main__": sys.exit(main())
