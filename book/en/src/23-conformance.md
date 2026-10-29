# 23. Conformance evidence and release requirements

<a id="n059"></a>

**N059.** Feature qualification MUST freeze source/build/compiler/parser/backend/storage settings, fixture schema/policies/data, capability limits and complete expected/actual typed results. Negative tests must verify rejection before execution; fault cases must retain uncertain/failed evidence.

Required evidence includes Appendix B's semantic cases and SQL-A01–A16 in [the acceptance map](acceptance-scenarios.md). Differential checks use a fixed reference database only for the shared SQL subset, after documenting deliberate differences. Compare complete ordered sequences with ORDER BY and typed multisets otherwise. Preserve duplicates, NULL tags and precision. Floating/ANN modes require declared tolerances/quality metrics and cannot silently satisfy exact cases.

<a id="n060"></a>

**N060.** Documentation checks, local parser/runtime tests, CI, driver qualification, real customer acceptance and production qualification MUST be recorded independently. No SQL profile is enabled by the existence of this document, its grammar, synthetic corpus or passing static link checks.
