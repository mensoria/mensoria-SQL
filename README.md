# Mensoria SQL

**Official documentation website · Draft 0.1.0-draft.1 · Language version 1**

[简体中文](README.zh-CN.md) · [English contents](book/en/src/SUMMARY.md) · [中文目录](book/zh-CN/src/SUMMARY.md)

The bilingual documentation website for the Mensoria SQL language draft: **24 normative chapters, four normative appendices, 60 rules, 32 feature definitions, 71 EBNF productions and 28 worked cases**. Each language also has front matter, reading routes, rule/feature/statement indexes, a glossary and marked informative engineering references.

This repository is the source and GitHub Pages publisher for the official documentation website. The draft does not establish a working SQL implementation, PostgreSQL protocol/driver compatibility, runtime conformance or production readiness.

## Documentation website

Official website: **[mensoria.github.io/mensoria-SQL](https://mensoria.github.io/mensoria-SQL/)**. GitHub Pages is enabled with GitHub Actions as its publishing source. See [publishing instructions and the verified deployment record](docs/site-publishing.md).

## Read the sources

| Edition | Start | Full contents |
| --- | --- | --- |
| English | [Preface](book/en/src/preface.md) | [Contents](book/en/src/SUMMARY.md) |
| 简体中文 | [前言](book/zh-CN/src/preface.md) | [目录](book/zh-CN/src/SUMMARY.md) |

The book has five parts: language foundations; relational queries; mutation and schema; execution contract; evolution and evidence. Normative appendices provide the grammar, worked corpus, excluded syntax and revision checklist. The English architecture/transport companions remain explicitly informative in both editions.

## Build the book

Requirements: Python **3.10+** and [mdBook **0.5.4**](https://github.com/rust-lang/mdBook/releases/tag/v0.5.4). The bootstrap downloads the official release, verifies a pinned archive SHA-256 and places the executable under ignored `.cache/tools/`; it does not install globally. macOS arm64/x86_64 and Linux arm64/x86_64 are covered.

```sh
python3 scripts/bootstrap_mdbook.py
python3 scripts/check_book.py
python3 scripts/build.py
```

The bilingual entry page is generated at `site/index.html`; each edition has its own navigation, search, same-chapter language switch and single-page print view. Build output is ignored by Git.

For EPUB, also install Pandoc **3.x**, then run:

```sh
python3 scripts/build.py --epub
```

This produces two EPUB files and a local build report in `dist/`, and copies the EPUB downloads into `site/downloads/`. HTML-only builds do not require Pandoc and do not advertise old EPUB files. Build tooling validates EPUB package targets/anchors; it does not claim external EPUBCheck or universal reader certification.

## Preview locally

After building:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open [the local book](http://127.0.0.1:8000/). Use either edition's print button for its single-page print view and browser Save as PDF. The workflow validates pull requests and deploys the `site/` artifact to GitHub Pages after updates to `main` or a manual main-branch run. Pull requests never deploy. Publishing is separate from SQL implementation qualification.

## Repository map

| Path | Purpose |
| --- | --- |
| `book/en/src/`, `book/zh-CN/src/` | Maintained, paired chapter manuscripts |
| `book/*/book.toml`, `book/*/src/SUMMARY.md` | Edition configuration and reading order |
| `book/structure.json` | Stable chapter/file correspondence |
| `book/theme/`, `book/cover.svg` | Shared reading/print/EPUB typography and cover |
| `sources/archstudio/`, `sources/manifest.json` | Five original snapshots and their provenance hashes |
| `scripts/` | Pinned tool bootstrap, content checks, HTML/EPUB build |
| `docs/` | Editorial policy and local delivery evidence |
| `web/` | Official documentation homepage, assets and root 404 |
| `.github/workflows/book.yml` | Validate, build and deploy the documentation via GitHub Pages |
| `site/`, `dist/`, `.cache/` | Generated, ignored local outputs |

See [editorial policy](CONTRIBUTING.md), [provenance](sources/README.md), [the change log](CHANGELOG.md) and [local verification](docs/book-verification.md). Original source snapshots contain historical links; standalone navigation checks apply to the adapted manuscript, not those frozen inputs.
