# Editing the Mensoria SQL book

## Manuscript ownership

Edit paired chapters in `book/en/src/` and `book/zh-CN/src/`. Keep `book/structure.json` and both `SUMMARY.md` files synchronized. Chapter filenames are stable across languages so same-chapter language switching works.

N001–N060, feature IDs and C01–C28 are traceability identifiers, not disposable numbering. Preserve SQL, EBNF, typed values and result expectations when making editorial/translation changes. The English text is the source for translation reconciliation.

Normative chapters define language behavior; engineering companions explain architecture/transport; front matter, indexes and glossary are editorial aids. Keep that distinction visible. The imported companions retain English in both editions.

## Change classes

- **Editorial:** change navigation, typography, lookup aids or surrounding prose without altering normative meaning. Update paired editions and run content/build checks.
- **Translation:** reconcile against English and preserve code, numbers and modal strength. Record meaningful translation changes.
- **Semantic:** revise the declared language/document version, affected cases, feature dependencies, paired chapters and change log together. The first edition's checker deliberately detects normative drift against its frozen import baseline. A later semantic edition must introduce an explicitly reviewed new baseline and update the edition metadata/checker; do not silently replace historical snapshots or hashes to make checks green.

Sources in `sources/archstudio/` are historical inputs, not the future editing target. Their original paths and hashes identify an import from a working tree; a source base commit is not proof those uncommitted documents existed in that commit.

## Validation

```sh
python3 scripts/check_book.py
python3 scripts/build.py
```

If EPUB formatting changes:

```sh
python3 scripts/build.py --epub
```

Inspect the HTML entry page, representative English/Chinese chapters, a wide grammar/table page, same-chapter switch and a print view. EPUB checks cover package/link structure; use an actual reader and, when required by a release process, EPUBCheck separately. Search and pagination of the book are publishing features, not qualification of SQL execution.

Keep source and output checks proportionate. Do not report CI, customer, driver or production acceptance from a local book build. Review the concrete diff before any commit, push, deployment or release.
