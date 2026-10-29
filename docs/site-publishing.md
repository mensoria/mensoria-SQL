# Publishing the official documentation

## Site and source

- Repository: `mensoria/mensoria-SQL`.
- Target URL: [https://mensoria.github.io/mensoria-SQL/](https://mensoria.github.io/mensoria-SQL/).
- Publishing branch: `main`.
- Static artifact: `site/`; generated from the maintained bilingual Markdown and `web/` homepage.
- Project base path: `/mensoria-SQL/`; internal assets and navigation are relative, and the root 404 links back to this project path.

This is a GitHub Pages documentation site. EPUB and print views are additional formats. The normative draft and its implementation/conformance boundaries are unchanged.

## One-time repository activation

With repository administration permission, open [Settings → Pages](https://github.com/mensoria/mensoria-SQL/settings/pages) and set **Build and deployment → Source → GitHub Actions**.

The Pages service must be enabled before deployment. A normal workflow `GITHUB_TOKEN` is not sufficient for `configure-pages` automatic enablement; GitHub documents the additional token requirements in [the action inputs](https://github.com/actions/configure-pages/blob/main/action.yml). No personal access token is embedded in this repository or requested through chat.

If using an already authenticated CLI instead of the web setting, an administrator can inspect the service with:

```sh
gh api repos/mensoria/mensoria-SQL/pages
```

For an absent service, the explicit administrator setup action is:

```sh
gh api --method POST repos/mensoria/mensoria-SQL/pages -f build_type=workflow
```

For an existing branch-published site, change its build source only after inspecting that existing configuration; do not blindly recreate or overwrite it. Repository/org policies and the `github-pages` environment may require additional human approval.

## Workflow behavior

`.github/workflows/book.yml` follows [GitHub's custom Pages workflow requirements](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages):

1. On pull requests, validate manuscripts, build both languages and upload a preview artifact. No Pages deployment or deployment credentials are used.
2. On updates to `main` or a manual run on main, also upload the `site/` directory with `actions/upload-pages-artifact`.
3. The separate deploy job depends on build, uses the `github-pages` environment, and has only `pages: write` and `id-token: write` permissions.
4. `actions/deploy-pages` publishes the Pages artifact and reports the resulting URL. No release tag or package publication is implied.

The official Pages actions use GitHub's maintained major-version tags; checkout/preview artifact actions retain their pinned commits. mdBook remains version- and archive-hash-pinned.

## Local review before publishing

```sh
python3 scripts/bootstrap_mdbook.py
python3 scripts/build.py
python3 scripts/check_book.py --html
```

Review the root documentation homepage, both language entries, a normative chapter, reference indexes and project-path assets/404. The build generates `sitemap.xml`, `robots.txt`, `.nojekyll` and the root `404.html`; no external runtime application or database is involved.

## Live verification

A successful local build is not a deployment. Record the exact pushed commit, workflow run and deployment URL; then verify the public homepage and representative English/Chinese routes over HTTPS. A queued, failed or authentication-blocked deployment must not be reported as live. Keep SQL runtime, driver, business and production conformance separate from documentation delivery.

## Verified initial publication — 2026-10-29

- Initial published source commit: `dae054c269d9e35498b6c214249d2a9ec284204f`.
- [Actions run 40847782679](https://github.com/mensoria/mensoria-SQL/actions/runs/40847782679), attempt **2**: build and deploy both **success**.
- GitHub Pages deployment **7408429865**: state **success**, environment `github-pages`, matching the source SHA above.
- [Live official site](https://mensoria.github.io/mensoria-SQL/): public, `build_type=workflow`, HTTPS enforced.
- Public HTTPS probes passed for the homepage, English and Simplified Chinese entries, Chinese grammar appendix, shared stylesheet and sitemap; a deliberately missing path returned HTTP 404 with the custom page.
- The public homepage also rendered in the in-app browser with both language routes and reference navigation.

The first run's build passed but deployment failed with HTTP 404 because the Pages service had not yet been enabled. After the user authenticated the CLI, the absent service was explicitly created with `build_type=workflow`; rerunning the failed deployment succeeded. The failed attempt remains visible in the same Actions run. No credentials are embedded in this record.

[Machine-readable initial publication evidence](site-publication.json) records the exact identifiers and checks. These identify the first verified publication, not a self-referential promise about the commit containing this record. Subsequent main-branch updates use the same workflow and require their own successful deployment.

Local site validation before this publication: **88** generated HTML pages, **3,177** local references/assets, **79** unique sitemap URLs; preserved normative text, bilingual code, source hashes, grammar closure and whitespace checks passed. SQL parser/backend, driver, business and production qualification remain **not run**; website publication does not change that boundary.
