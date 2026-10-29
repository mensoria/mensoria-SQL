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

## Current publication record

Configuration and local validation are being prepared. Repository access was verified: the connected Personal account has administrative permission, and local SSH can read the empty remote. GitHub CLI is not authenticated and the current browser is logged out; the connector does not expose the Pages administration endpoint. The one-time Pages setting therefore still requires an authenticated administration path. This paragraph is updated only after actual remote deployment evidence exists.
