# Documentation homepage refinement

**Date:** 2026-10-29. **Surface mode:** Read. **Scope:** existing documentation home and shared reading chrome; the language draft is unchanged.

## Decisions

The primary task is to find and read the standard. The prior standalone landing page made language selection the main content and repeated parallel English/Chinese links throughout its reference section.

- The project root now opens the documentation overview directly: Simplified Chinese by default, or the reader's remembered language. The static fallback remains usable when scripting is unavailable.
- A single native language selector occupies the upper-right header position on each reading page. Body content contains no language chooser or paired cross-language links.
- Changing language keeps the chapter filename and stable N-rule, C-case or feature-registry anchor. Explicit localized routes remain usable, and storage failure is caught without blocking navigation.
- The overview uses one title, compact version metadata, one primary reading action, five specification rows and a small reference index. Provenance remains in the sidebar rather than competing with the initial reading action.
- The existing green/neutral palette and mdBook navigation are retained. Shared typography, line measure, sidebar density and header proportions are tuned for reading. Print/theme/GitHub functions remain available through the existing reader; low-priority print/GitHub icons collapse on narrow screens.

This is a refinement of the incumbent interface, not a new product identity or a change to normative content.

## Verification

- `python3 scripts/build.py --epub` passed for both editions; manuscript/source preservation, 60 rule IDs, 32 features, 28 cases and 71 grammar productions remain unchanged.
- The HTML validator checked 88 pages and 3,206 local references/assets. It now also rejects targets escaping the published `site/` root, preventing a local source file from masking a missing deployed asset.
- Browser inspection covered the desktop overview at 1280px and the reading layout at 390px. The mobile sidebar was closed through its existing control for the reading-state check; no document or toolbar horizontal overflow was observed.
- The rendered Chinese desktop page had one language control, zero opposite-language body links and a 32px main heading. Root navigation returned to the remembered English edition after a deliberate switch. Switching `/en/13-transactions.html#n038` returned to `/zh-CN/13-transactions.html#n038`.
- The native selector's explicit accessible label was verified with the browser's label locator. The viewport override was reset after mobile checks, and the desktop sidebar restored.
- Final live inspection caught mdBook's link color overriding the primary action label. The action selector now outranks that default; rendered foreground/background colors are checked after the fix.
- Checked palette contrast: primary text 13.02:1, secondary text 6.11:1, light-theme action 6.07:1, dark-theme action tokens 7.08:1. Dark-theme token contrast was calculated; this is not a complete visual acceptance of every mdBook theme.
- The Impeccable detector ran once over the changed HTML, CSS and JavaScript and returned no findings. It warned that the HTML template's generated `assets/site.css` path is absent in the source template directory; the CSS files were explicit scan targets and actual built resources were checked separately.

The screenshot under ignored `.cache/qa/home-desktop.jpg` is local visual evidence, not part of the deployed site. These UI/build checks do not qualify SQL execution, drivers or business use.
