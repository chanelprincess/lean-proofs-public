# KTS Global · Lean 4 · Navier–Stokes R2/R3 community verification package

> This repository publishes the Lean 4 **Navier–Stokes R2/R3 community
> verification package**, release [`r2-r3-v1`](https://github.com/kts-global/lean-proofs-public/releases/tag/r2-r3-v1).
> The release body is the canonical source for the claim boundary,
> contribution attribution and verification details below. If this README
> and the release body ever disagree, **the release body wins**.
>
> **Not** a claimed solution of a Clay Millennium Problem.
> **No** Clay Institute recognition. **No** independent specialist review.
> **Not** an independent replication: verification runs are publisher-executed
> on one platform (Ubuntu 24.04 x86_64).

## Canonical release

| field | value |
|---|---|
| Release | [`r2-r3-v1`](https://github.com/kts-global/lean-proofs-public/releases/tag/r2-r3-v1) |
| Published | 2026-10-21 13:48 UTC |
| Asset | [`R2_FINAL_S524_COMMUNITY_V1.tar.gz`](https://github.com/kts-global/lean-proofs-public/releases/download/r2-r3-v1/R2_FINAL_S524_COMMUNITY_V1.tar.gz) |
| Cite with DOI | [10.5281/zenodo.23535805](https://doi.org/10.5281/zenodo.23535805) |
| Wikidata | [Q141803373](https://www.wikidata.org/wiki/Q141803373) |

Please cite **this release's own DOI and tag** (`10.5281/zenodo.23535805`,
`r2-r3-v1`). See [`CITATION.cff`](./CITATION.cff) for machine-readable
citation metadata.

## Claim (canonical, verbatim from release body)

Proved (Lean 4.34.1, Comparator on two kernels): the encoded forms of
Fefferman's alternatives (C) and (D) for forced Navier–Stokes, and
A ∨ B ∨ C ∨ D through them. **Not claimed:** (A) or (B); that the encoding
matches Fefferman's published prose; Clay acceptance.

## Contribution attribution (canonical, verbatim)

- **Inherited mathematics:** OpenAI, [`openai/NavierStokesAndEuler`](https://github.com/openai/NavierStokesAndEuler) at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (Apache-2.0). The mathematics and the underlying formalization are OpenAI's.
- **This release adds:** Tim Jacobs, KTS Global ([ORCID 0009-0008-7130-1448](https://orcid.org/0009-0008-7130-1448)) — the statement and bridge layer, the R3 per-alternative packaging, and the public verification tooling and documentation.
- **Verification:** publisher-executed, not independent replication (publisher
  wall-clock run: 5,678 s; `RECEIPTS/community_run/`).

## Theorems (named, canonical)

`NavierStokes.ClayChallenge.clay_navier_stokes_fefferman` and `..._via_D`
(A ∨ B ∨ C ∨ D through (C) / through (D)); `NavierStokes.ClayC.clay_C`;
`NavierStokes.ClayD.clay_D`; `NavierStokes.Comparator.navier_stokes_clay_via_C`
and `..._via_D`; the bridges `Clay.NavierStokes.Bridge.*` and
`BridgeConverse.*`. Alternatives (A) and (B) are shipped as statement files
only.

## Axioms

All 40,986 theorems of the 620-module closure were enumerated; none depends
on an axiom outside `propext`, `Classical.choice`, `Quot.sound`. 35,970
depend on exactly those three; 5,016 depend on a strict subset. Each named
theorem above was checked for exactly those three on both kernels
(Lean default kernel and nanoda): ClayFefferman exit 0; ClayFeffermanViaD
exit 0; NavierStokesComplete exit 0; ClayC exit 0; ClayD exit 0.

## Verify

Ubuntu 24.04; prerequisites listed in `RESTORE_AND_VERIFY.md`.

```
tar xzf R2_FINAL_S524_COMMUNITY_V1.tar.gz
cd R2_FINAL_S524_COMMUNITY_V1
./VERIFY.sh /path/to/a/fresh/empty/directory
```

Exit 0 only if every required check passes.

## Limits

Publisher-executed, not an independent replication; one platform
(native Ubuntu 24.04); no native Windows, offline or cold-cache verification;
`landrun` not byte-reproducible; the encoding has not been independently
reviewed against Fefferman's prose; (A) and (B) are open; no Clay acceptance.
See `KNOWN_LIMITS.md`.

## Licence

Upstream OpenAI material remains under its Apache-2.0 licence. Files added
by the package publisher are published under the Apache-2.0 [`LICENSE`](./LICENSE)
at the root of this repository; see
[`THIRD_PARTY_NOTICES.md`](./R2_FINAL_S524_COMMUNITY_V1/THIRD_PARTY_NOTICES.md).
The CHAOS implementation is not distributed or licensed by this package.

## Prior work (separate release, separate citation)

The Lean 4.34.1 port of OpenAI's `NavierStokesAndEuler` that this release
builds on is published as its own release
[`s437-v1`](https://github.com/kts-global/lean-proofs-public/releases/tag/s437-v1).
It is a **separate release with a separate DOI**. **Do not use any S437
identifier to cite R2/R3** — the citation for R2/R3 is the DOI and tag
listed above. S437's own identifiers appear on its release page.

Each release in this repository is a distinct, citable artefact. Cite the
release tag you used.
