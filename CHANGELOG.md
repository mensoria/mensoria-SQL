# Change log

## 0.1.0-draft.1 — first book edition, 2026-10-29

- Organize the existing English and Simplified Chinese language drafts into five parts, 24 normative chapters and four normative appendices per edition.
- Add front matter, reader routes, a glossary and rule/feature/statement indexes.
- Preserve 60 normative rules, 32 features, 71 EBNF productions and 28 worked cases; retain identical normative SQL/EBNF across languages.
- Resolve historical workspace references within the book; include marked English engineering companions and source provenance.
- Add pinned mdBook HTML/print builds, optional Pandoc EPUB output, same-chapter switching, source/content/link checks and artifact-only CI configuration.

This is an editorial book edition of the existing language draft. It adds no executable SQL capability or runtime conformance claim. No Git tag or hosted release is implied by this entry.

## Official documentation publishing configuration — 2026-10-29

- Make the bilingual online documentation the primary product surface, with a dedicated official homepage and reference navigation.
- Add GitHub Pages artifact upload/deployment for main, read-only PR builds, a project-path 404, sitemap, robots metadata and `.nojekyll`.
- Keep EPUB/print as optional formats and preserve the normative manuscript, source hashes and language-qualification boundaries.
- Record Pages activation, authentication and live deployment verification separately in `docs/site-publishing.md`.
