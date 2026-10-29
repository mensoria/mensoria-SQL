# Appendix D. Review checklist and revision history

## D.1 Draft completeness criteria

- Every grammar nonterminal resolves; every terminal/lexical category has a rule.
- Every enabled profile has a minimum feature set, semantic rules, applicable corpus and implementation gates.
- Every specified optional feature has dependencies, supported syntax, types/NULL behavior and rejection when disabled.
- Every top-level example names its required profile/features or rejection expectation.
- Type resolution, NULL, bags, joins, aggregates, guards, original-key outcome and publication rules agree across the authorities.
- Documentation, local runtime, CI, client and business/production evidence remain separate.

## D.2 Revision 0.1.0-draft.1

Initial full normative edition. Expands the earlier architecture proposal into a language standard draft; preserves existing architecture/transport/operation ownership. Resolves R2 NUMERIC as mandatory, defines exact aggregate result scales/half-even AVG, specifies a closed grammar and a 28-case worked corpus. No existing SQL implementation or released standard is superseded because none has been qualified here.
