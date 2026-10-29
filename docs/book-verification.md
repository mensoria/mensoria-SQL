# First book edition: local verification

**Date:** 2026-10-29, Asia/Shanghai. **Edition:** 0.1.0-draft.1. **Scope:** local manuscript organization and book outputs in `mensoria-SQL`.

## Delivered manuscript

- Five parts, 24 normative chapters and four normative appendices in English and Simplified Chinese.
- 39 reading pages per language, including front matter, four lookup aids, informative English engineering companions, qualification scenarios and historical source context.
- 60 normative rules, 32 features, 28 worked cases and 71 closed EBNF productions retained per normative edition.
- Five original source snapshots with per-file SHA-256 and source working-tree provenance.

The manuscript checker compares every normative chapter's full text with its source clause after allowing only heading-level changes, local link rebasing and stable navigation anchors. All 25 normative SQL/EBNF fenced blocks are identical across editions. This is editorial preservation evidence, not a proof that the language grammar is unambiguous or implemented.

## Exact local commands and results

| Command | Result |
| --- | --- |
| `python3 scripts/bootstrap_mdbook.py` | Official mdBook 0.5.4 archive verified against pinned SHA-256 and installed to ignored project-local cache |
| `python3 scripts/check_book.py` | Source hashes, whole-clause preservation, IDs, grammar closure, contents coverage, local references, fences and whitespace passed |
| `python3 scripts/build.py --epub` | Both HTML editions and both EPUBs built locally; final build had no Pandoc Chinese-translation warnings |
| `python3 scripts/check_book.py --html` | 87 generated HTML pages; 3,166 local HTML references/assets resolved, including fragment checks and same-filename language-switch targets |

The first direct bootstrap attempt encountered a transient TLS EOF. The bootstrap now uses bounded verified retries and a SHA-256-checked archive cache while preserving an existing executable on download failure; its actual subsequent installation passed without disabling certificate checks. Two final blank lines in the informative scenario pages were removed after the Git whitespace check found them.

Local toolchain: macOS arm64, mdBook **0.5.4**, Pandoc **3.10**, Python from the local environment. The EPUB checker verified the uncompressed first `mimetype` entry, package/container reference, and local targets/fragments across **42 XHTML documents per edition**. It did not run external EPUBCheck or certify every reader.

`dist/build-report.json` records the actual built EPUB hashes, tool versions and unrun acceptance layers; it is generated and ignored. HTML-only builds intentionally do not advertise retained old EPUB files. Chinese EPUB interface labels are supplied through a local Pandoc translation data file.

## Browser inspection

The local entry page displayed both language entrances, print views and EPUB download links. The Chinese book visibly displayed the normative text and feature table with the same-chapter English switch. This was a limited local browser inspection; complete responsive, keyboard, search-relevance, accessibility and physical-print acceptance were not established.

## Scope boundaries

The starting target repository had no commits and contained no manuscript. All content was assembled locally; original ArchStudio source files were read, not edited, during this import. The configured origin is `git@github.com:mensoria/mensoria-SQL.git`.

The GitHub workflow is configured to validate/build and upload an HTML artifact. It has **not run**. No GitHub Pages setting, public deployment, tag, release, commit or push was performed. SQL parser/backend, fault, driver, business and production acceptance were **not run**.
