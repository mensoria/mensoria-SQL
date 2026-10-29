# 原始资料背景

本书可以独立阅读。以下原始资料引用用于说明来源和职责，不是理解规范语言之前必须下载的缺失依赖。原仓库路径保留为标识，不作为失效的本地链接。

<a id="feature-requirements"></a>

## 功能需求

原功能目录为 `specs/004-surrealdb-rust-ai-baas`。MSQL-001–008 覆盖语言档位、类型、授权、受守卫保护的写入、迁移、接口、证据及完整标准。SQLD/SQLS 属于文档任务；SQLI001–008 仍是未来实现。本次出版不改变其状态。本书重现的规范要求为 N001–N060。

<a id="data-model-and-write-ownership"></a>

## 数据模型与写入职责

原第 27 章定义逻辑集合／Schema 修订、记录 CAS、当前身份检查、带守卫的原生事务及业务／Operation／Outbox 职责。本书[数据修改](12-data-modification.md)和[事务](13-transactions.md)明确 SQL 约束；SQL 不得引入特权绕过路径。

<a id="structured-query-baseline"></a>

## 结构化查询基线

原第 38 章描述早期 JSON 查询子集和实时 keyset 游标。历史检查不证明 SQL NULL/OR/连接/聚合、底层工作预算或 SQL 符合性。[SQL 分页契约](17-parameters-results-pagination.md)才是这里的语言要求。

<a id="assistant-query-boundary"></a>

## 助手与查询边界

原第 19 章在可信查询执行器下区分生成、校验、执行和优化。模型生成源文本不授予执行／披露权限；本书在[制品](16-artifacts-explain.md)和[授权](20-authorization-audit.md)中保留该边界。

<a id="studio-boundary"></a>

## Studio 边界

原第 133 章描述浏览器／API 桥及身份／会话／票据约束。平台 Member 角色不隐含业务数据权限。SQL 使用相同的当前原生授权及最终结果发布围栏。

## 工程参考

[架构参考](companion-architecture.md)、[传输契约](companion-transport.md)和[资格验证场景](acceptance-scenarios.md)作为说明性实现资料保留。历史完整审查快照位于仓库来源归档；其中旧的本地收据不是本书的运行时证据。
