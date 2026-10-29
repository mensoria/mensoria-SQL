# Mensoria SQL

Mensoria DB 的 SQL 语言规范与实现参考。

<p class="document-meta"><span>语言版本 1</span><span>草案 0.1.0-draft.1</span><span>MSQL-SD-001</span></p>

[开始阅读](01-purpose.md) [阅读指南](reading-guide.md)

## 规范内容

| 章节 | 内容 |
| --- | --- |
| [语言基础](01-purpose.md) | 档位、逻辑模型、词法、类型与表达式。 |
| [关系查询](08-select.md) | SELECT、排序、连接、聚合及可选查询结构。 |
| [数据修改与 Schema](12-data-modification.md) | 受守卫保护的写入、原子请求事务与迁移提案。 |
| [执行契约](15-catalog.md) | 目录、制品、结果、诊断、预算及授权。 |
| [兼容性与符合性](21-extensions.md) | 扩展边界、版本管理与实现所需证据。 |

## 参考索引

[完整语法](appendix-a-grammar.md) · [语句索引](statement-index.md) · [错误码](18-diagnostics.md) · [规范规则](rules-index.md)

本版包含 24 章规范、四个附录与 28 个带预期结果的案例。当前为语言标准草案，不表示运行时或驱动已经通过符合性验证。能力范围见[档位定义](02-profiles.md)。
