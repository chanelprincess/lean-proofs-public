# PORT_DIFF_vs_f9e8bc5.patch — provenance note

This file is a standalone, fetchable diff of the 24 files from
`CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437/RECEIPTS/node_return/s437.lpb.t6.full_lpb_S2_changed.txt`
between:

| side | content |
|---|---|
| LEFT  (`a/`) | upstream `github.com/openai/NavierStokesAndEuler` commit `f9e8bc5` (Apache-2.0) |
| RIGHT (`b/`) | this repo @ `s437-v1` tag, path `CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437/PROOFS/S412_ESTATE_PORT_v4.34.1/` |

## How it was generated

```bash
diff -u --strip-trailing-cr \
  <upstream>/<file> \
  CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437/PROOFS/S412_ESTATE_PORT_v4.34.1/<file>
```
for each of the 24 files in `S2_changed.txt`, concatenated into one patch.

## Why this file exists

`PROVENANCE.json` (field `source.port`) says "PORT.patch applied once to the
base (24 files); patched files equal the reference realization under
LF-normalised byte comparison". That PORT.patch was previously only visible
through the bundled `ARTIFACTS/s437.lpb.t6.full.project.tar.gz` (6.6 MB) —
no standalone, directly-fetchable diff file existed at the s437-v1 tag.

The public S437 page at https://tim-jacobs.net/formal-work/s437/ needs to
link each item to its own file (per CHAOS BUILDER v7.27 §2 / L-42). This
file provides that: a 41 KB standalone unified diff.

## Verification

To reproduce:

```bash
git clone --depth 100 https://github.com/openai/NavierStokesAndEuler upstream
cd upstream && git checkout f9e8bc5 && cd ..
git clone --branch s437-v1 https://github.com/kts-global/lean-proofs-public lpp
PORT=lpp/CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437/PROOFS/S412_ESTATE_PORT_v4.34.1
while read f; do
  diff -u --strip-trailing-cr --label "a/$f" --label "b/$f" "upstream/$f" "$PORT/$f"
done < lpp/CLAY_NS_ALTERNATIVES_C_AND_D_FULL_PROJECT_BUILD_S437/RECEIPTS/node_return/s437.lpb.t6.full_lpb_S2_changed.txt
```

The output should byte-match this file after the comment header.

## Not claimed

- This is not a new porting result. The port pre-existed (see PROVENANCE
  `not_claimed[2]`). This file is a readability aid, not a new artifact.
- It does not include lake-manifest.json / lakefile.toml / lean-toolchain
  substantive changes (toolchain pinning metadata, included for completeness).
