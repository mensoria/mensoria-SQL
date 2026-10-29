# 阅读指南

全书分为五篇。可以顺序阅读完整契约，也可以按角色选择路径。

| 读者 | 建议路径 | 回答的问题 |
| --- | --- | --- |
| 应用开发者 | [档位](02-profiles.md) → [SELECT](08-select.md) → [参数与结果](17-parameters-results-pagination.md) → [数据修改](12-data-modification.md) | 应用可以提交什么，又能依赖什么？ |
| 语言实现者 | [词法](04-lexical-structure.md) → [类型](05-data-types.md) → [表达式](07-expressions.md) → [语法](appendix-a-grammar.md) | 哪些输入被接受，如何确定类型并求值？ |
| 数据／授权审查者 | [绑定](03-database-model.md) → [JOIN](09-joins.md) → [事务](13-transactions.md) → [授权](20-authorization-audit.md) | 谁拥有执行，何时可以发布数据？ |
| Schema 运维人员 | [迁移提案](14-schema-migrations.md) → [预算](19-budgets-cancellation.md) → [符合性](23-conformance.md) | 发布或重新开放前需要验证什么？ |
| 符合性工程师 | [案例集](appendix-b-conformance-corpus.md) → [资格验证场景](acceptance-scenarios.md) → [排除语法](appendix-c-excluded-syntax.md) | 正例、负例和故障边界分别需要什么证据？ |

## 如何阅读要求

`N001`–`N060` 是稳定规范规则编号；`C01`–`C28` 是带预期结果的语言案例；`SQL-A01`–`SQL-A16` 是未来语义／安全／故障资格验证场景。文档检查通过不等于运行时案例通过。

MUST/SHALL 和 MUST NOT/SHALL NOT 分别表示“必须”和“不得”。SHOULD 表示偏离时需要记录理由的“应当”；MAY 表示“可以”。产生式的存在不授权可选能力，示例也不是运行收据。

## 五篇结构

1. **语言基础**：范围、档位、逻辑名称、词法、类型与表达式。
2. **关系查询**：投影、排序、连接、聚合及可选结构。
3. **修改与 Schema**：受守卫保护的命令、原子请求批次、未知结果及迁移。
4. **执行契约**：元数据、制品、传输值、诊断、预算与授权。
5. **演进与证据**：扩展、兼容性、资格验证与参考资料。

规范正文之后是语法与精确示例。规则、能力、语句和术语索引便于查阅；说明性工程参考解释实现职责和传输，但不创建新的语言规范权威。
