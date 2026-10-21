# Community-package verification run (publisher-executed)

These are the raw outputs of one execution of `VERIFY.sh` on the candidate whose runnable inputs are listed in `INPUTS.sha256` (sha256 of that file: `13867b24153acb98c5b6fb043b2815ce166d12d4cb95d1b2cca4e1e4f5f822bb`; the same file was used by the run and is shipped here unchanged).

- **Kind:** publisher-executed verification of the community package. It is **not** an independent replication.
- **Path normalisation:** the publisher's absolute paths were replaced mechanically by `<WORKDIR>`, `<PACKAGE>`, `<HOME>`, `<USER>` and `<RUN>`. Nothing else was edited. The unmodified originals are retained privately and are not shipped.
- `results.json` and `SUMMARY.md` are produced by `TOOLS/summarize.py` from these files; `results.tsv` lists every stage with its exit code and actual wall time; `logs/` holds each stage's command, stdout, stderr and exit record; `logs/cmp_*.time` holds the Comparator's own exit status and timing.
- An earlier attempt of the same entry point stopped at the Mathlib cache stage (open-file limit too low); see `KNOWN_LIMITS.md` and `CHANGELOG.md`. That attempt's evidence is not part of this run.
