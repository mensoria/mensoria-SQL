# Mensoria SQL 标准草案——完整版（中文版）

| 项目 | 内容 |
| --- | --- |
| 文档编号 | MSQL-SD-001 |
| 草案修订号 | 0.1.0-draft.1 |
| 语言版本 | 1 |
| 状态 | 拟议规范性草案；尚未建立运行时符合性证明 |
| 日期 | 2026-10-29，Asia/Shanghai |
| 产品 | Mensoria DB |

[文档索引](README.md) · [英文原文](137-mensoria-sql-standard-draft.md) · [架构与交付](136-mensoria-db-sql-design.md) · [传输契约](../../specs/004-surrealdb-rust-ai-baas/contracts/mensoria-sql.md) · [功能需求](../../specs/004-surrealdb-rust-ai-baas/spec.md) · [审查与证据](../../specs/004-surrealdb-rust-ai-baas/mensoria-sql-design-review.md)

本文件是英文修订版 0.1.0-draft.1 的完整中文译本。章节、规则、能力和案例编号与英文一致；SQL、EBNF、标识符及示例字面值保持原样。译文不增加或改变语言能力；如发现两版语义不一致，以英文原文为核对依据并修正译文，不得据此启用实现能力。

## 目录

1. 目的、权威边界与规范性用语
2. 符合性档位与能力登记表
3. 数据库模型、名称与绑定
4. 词法结构
5. 数据类型与值
6. 类型解析与转换
7. 表达式、谓词与 NULL
8. SELECT、排序与逻辑行数上限
9. JOIN
10. 分组与聚合
11. 可选关系查询结构
12. 数据修改
13. 请求事务、幂等与未知结果
14. Schema 定义与迁移
15. 目录与能力发现
16. 校验、制品与 EXPLAIN
17. 参数、结果与分页
18. 诊断
19. 预算、截止时间与取消
20. 授权、血缘与审计
21. 多模型扩展框架
22. 兼容性、版本化与实现要求
23. 符合性证据与发布要求
24. 参考资料

附录：A. 闭合语法；B. 带预期结果的符合性案例集；C. 排除的语法；D. 审查清单与修订历史。

## 1. 目的、权威边界与规范性用语

### 1.1 范围

Mensoria SQL 是一种面向标准 SQL、实施版本管理的查询与数据修改语言，用于访问单个 Mensoria DB 项目环境内已授权的逻辑关系。它采用常见 SQL 写法及部分 PostgreSQL 便利语法，同时保留 Mensoria 现有身份、Schema、命令和操作的职责归属。

本文件规定可观察行为。它不替换 SurrealDB 存储引擎，不创建新的授权服务，也不要求引入第二套数据库。解析器、原生数据库或客户端能够接受相似文本，并不构成符合性证据。

**N001.** 本文件中的 MUST/SHALL 译为“必须”，表示强制要求；MUST NOT/SHALL NOT 译为“不得”，表示禁止；SHOULD 译为“应当”，表示偏离时需要记录理由的建议；MAY 译为“可以”，表示可选。声明符合某个档位的实现，必须满足所有适用的“必须”要求，并公布其已启用的可选能力。

**N002.** 本草案是语言规范的权威。[第 136 章](136-mensoria-db-sql-design.md)负责架构与分阶段交付；[接口契约](../../specs/004-surrealdb-rust-ai-baas/contracts/mensoria-sql.md)负责具体请求和结果编码。启用受影响能力之前必须消除冲突；实现不得静默选择更容易实现的解释。

**N003.** 任何实现均不得仅依据本草案声明完整 ISO SQL、完整 PostgreSQL、JDBC/ODBC、ORM、BI 工具或 PostgreSQL 线协议兼容。此类声明必须另行列明版本、支持范围及实际证据。

### 1.2 术语

| 术语 | 含义 |
| --- | --- |
| 作用域（Scope） | 经身份验证的组织／项目／环境绑定 |
| 环境代次（Incarnation） | 用于区分当前物理环境与旧环境的恢复代次 |
| 逻辑关系（Logical relation） | 已发布的 SQL 表或限定作用域的查询结果，不等于原生物理表 |
| 绑定（Binding） | 逻辑 SQL 名称／类型到已发布集合及 Schema 元数据的版本化映射 |
| 制品（Artifact） | 经校验、不可变的 SQL／带类型计划修订版，包含声明的依赖 |
| 操作（Operation） | 现有持久权威记录，负责已接纳执行及其原始幂等键对应的结果 |
| 结果发布（Publication） | 经最终授权后释放结果字节、元数据或后续分页能力 |
| 未知（Unknown） | 证据不足，无法确认提交、失败或底层物理执行完成 |
| 完整结果（Complete result） | 已交付 SQL 表达式及其显式逻辑上限所要求的全部行 |
| 已完成资格验证的能力（Qualified feature） | 已冻结实现配置，并具有所需通过证据的能力 |

除规则或附录 B 明确给出预期结果外，示例均用于说明。“暂缓”能力在 v1 中没有可执行契约；“已规定的可选”能力在本文中已有规则，但仍需单独启用。

## 2. 符合性档位与能力登记表

### 2.1 档位

**N004.** 档位启用必须限定作用域、实施版本管理并具有证据支持。解析器能够构造 AST，不得成为启用能力的依据。

| 档位 | 最低必需行为 | 依赖 |
| --- | --- | --- |
| R1 | 单关系 SELECT；BOOLEAN/BIGINT/TEXT；比较、AND/OR/NOT、NULL 检查、IN；别名、标量 CAST、排序、LIMIT/FETCH；已授权元数据和 EXPLAIN | 当前原生身份、策略／结果发布屏障，以及经资格验证的有效预算 |
| W1 | 单行 INSERT；带精确 id/revision 的 UPDATE/DELETE；显式列 RETURNING；原子请求批次 | R1，以及经资格验证的同事务命令向量／收据能力 |
| R2 | DISTINCT；两个关系的 INNER/LEFT 等值连接；GROUP BY/HAVING；五种指定聚合；CASE/COALESCE；NUMERIC(p,s) | R1，以及在有界关系执行下的一致、已授权输入视图 |
| M1 | CREATE TABLE、ADD COLUMN、CREATE/DROP INDEX、DROP TABLE 提案 | R1，以及现有 SchemaAdmin／维护发布流程 |
| X1 | 逐项命名的多模型扩展框架 | R1 及每个扩展各自的前置条件；不整体启用 |
| P1 | 预留的驱动／线协议兼容档位 | 另行规定协议和客户端版本；不属于本语言草案的规定范围 |

R2 不隐含 W1 或 M1；W1 不隐含 R2。M1 不得接受对应类型能力尚未启用的类型。X1 和 P1 单独均不能构成完整的 SQL 支持声明。

### 2.2 能力标识符

下列稳定标识符表示语言能力，不是可执行函数名称。必需能力仅随所属档位启用。已规定的可选能力在明确通过资格验证之前保持关闭。

| 能力 ID | 状态／所属档位 | 规则 |
| --- | --- | --- |
| `read.single_relation` | R1 必需 | 第 3、8 节 |
| `expr.boolean_predicates` | R1 必需 | 第 7 节 |
| `expr.in_list` | R1 必需 | 第 7 节 |
| `type.boolean_bigint_text` | R1 必需 | 第 5–6 节 |
| `read.order_limit` | R1 必需 | 第 8 节 |
| `catalog.scoped` | R1 必需 | 第 15 节 |
| `plan.explain` | R1 必需 | 第 16 节 |
| `read.nullable_order` | R1 已规定的可选能力 | 第 8、17 节 |
| `type.uuid` | R1 已规定的可选能力 | 第 5–6 节 |
| `write.cas` | W1 必需 | 第 12 节 |
| `write.returning` | W1 必需 | 第 12 节 |
| `write.atomic_batch` | W1 必需 | 第 13 节 |
| `write.multi_values` | W1 已规定的可选能力 | 第 12–13 节 |
| `read.distinct` | R2 必需 | 第 8 节 |
| `read.equijoin` | R2 必需 | 第 9 节 |
| `read.group_aggregate` | R2 必需 | 第 10 节 |
| `expr.case_coalesce` | R2 必需 | 第 7 节 |
| `type.numeric` | R2 必需 | 第 5–6、10 节 |
| `expr.numeric_arithmetic` | R2 已规定的可选能力 | 第 7 节 |
| `expr.text_basic` | R2 已规定的可选能力 | 第 7 节 |
| `read.cte` | R2 已规定的可选能力 | 第 11 节 |
| `read.exists` | R2 已规定的可选能力 | 第 11 节 |
| `read.union_all` | R2 已规定的可选能力 | 第 11 节 |
| `type.double` | R2 已规定的可选能力 | 第 5–6、10 节 |
| `type.timestamptz` | R2 已规定的可选能力 | 第 5–6 节 |
| `schema.proposal` | M1 必需 | 第 14 节 |
| `schema.literal_default` | M1 已规定的可选能力 | 第 14 节 |
| `extension.json` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.graph` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.fulltext` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.vector` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `driver.postgresql` | P1 预留 | 需要单独的驱动规范 |

**N005.** 需要多项能力的语句必须满足这些能力的并集，包括类型和运算符依赖。对于已关闭或暂缓的语法，即便解析器能够识别，也必须在执行前以 `SQL_FEATURE_UNSUPPORTED` 拒绝。

**N006.** 在完整档位通过资格验证之前，实现可以开放单独命名的预览能力，但不得宣称该档位已启用。预览仍须遵守所有适用的规范性语义及安全要求。有效限制和档位尚未满足的要求必须能够被查询。

## 3. 数据库模型、名称与绑定

**N007.** 一次执行必须绑定到一个由服务端确定的作用域和环境代次。SQL 不得覆盖物理目标、切换命名空间／数据库，或跨项目环境进行连接。

默认 Schema 为 `public`。用户表引用采用 `table_name` 或 `public.table_name`。仅第 15 节的三个虚拟目录关系使用其他 Schema。禁止三段式名称、`search_path`、临时 Schema 及原生记录目标写法。

**N008.** 逻辑表必须映射到已发布的集合绑定，其中包含逻辑身份、SchemaRevision、映射修订号、有序列、类型、可空性、来源映射及策略约束。任意原生表或无 Schema 表不得自动成为 SQL 表。

平台 SQL 列包括 `id TEXT NOT NULL`、`revision BIGINT NOT NULL`；在确实存在映射且能力已启用时，还可包含经资格验证的 `created_at`／`updated_at` 时间戳列。不具备合适数据的历史集合不隐含这些时间戳列。`id` 不可变。`revision` 由服务端管理，SQL 新建行的初始值为 1，每次已提交的 UPDATE 加 1，包括业务值未变化的更新。修订号溢出导致事务失败。

**N009.** 新 SQL 绑定必须保留 `id`、`revision`、`created_at` 和 `updated_at`，防止与业务列重名。现有冲突字段必须使用经显式审查的 SQL 别名；绑定不得隐式重命名已存数据。

**N010.** 名称解析必须使用已授权的目录元数据。对于不存在或未授权的公共资源引用，必须返回相同且经过敏感信息清理的 `SQL_REFERENCE_DENIED`；不得返回隐藏物理表、名称、行数或原生错误。

表别名会在当前查询块内隐藏原表限定名。列引用可以不带限定名，也可以使用当前有效的表／CTE 别名限定。存在歧义的引用予以拒绝。输出别名仅在 ORDER BY 中可见，在 WHERE/ON/GROUP BY/HAVING 以及同一 SELECT 列表的其他项中不可见。当 ORDER BY 中的名称同时匹配输出标签和输入列时，解析到唯一的输出标签；匹配多个同名输出标签时构成歧义。

## 4. 词法结构

### 4.1 源文本编码与标识符

**N011.** SQL 源文本必须是有效 UTF-8，且不得包含 U+0000 或字节顺序标记。字符串和注释外的空白仅包括 ASCII 空格、制表符、CR 或 LF；诊断位置计算时 CRLF 算作一次换行。其他非预期控制字符均予以拒绝。

未加引号的标识符采用 `[A-Za-z_][A-Za-z0-9_]*`，并折叠为小写。加引号的标识符使用双引号并保留大小写，但 v1 要求其解码内容仍匹配上述 ASCII 模式。因此，`notes`、`NOTES` 和 `"notes"` 解析为相同名称，而 `"Notes"` 是不同名称。解码后包含引号、空白或 Unicode 名称的内容不是有效 v1 标识符，必须使用经审查的别名。标识符最多 63 个 UTF-8 字节，不得静默截断。

附录 A 中以大写形式显示的所有单词终结符均为保留字，在未加引号时不区分大小写匹配。如果解码后的内容符合标识符限制，可以用引号使用原本的保留字。`PUBLIC`、`INFORMATION_SCHEMA` 和 `MENSORIA` 仍是普通 Schema 标识符，不是额外的 SQL 关键字。

### 4.2 字面值与注释

| 词法单元 | 语法与含义 |
| --- | --- |
| 字符串 | 单引号包围的 Unicode 文本；`''` 表示一个单引号；反斜杠是普通字符 |
| 整数 | 一个或多个 ASCII 数字；可选正负号由标量语法处理；先处理符号再检查 BIGINT 范围 |
| 小数 | 数字、句点、数字；可选正负号由标量语法处理；要求 `type.numeric`；精度和小数位数最多 38 |
| 布尔值 | `TRUE` 或 `FALSE` |
| SQL NULL | `NULL`，类型由上下文推断或显式 CAST 指定 |
| 参数 | `$` 后跟无前导零的正整数位置，例如 `$1` |
| 注释 | `--` 延伸至行尾；不允许嵌套的 `/* ... */`；未终止或嵌套块注释均拒绝 |

`-9223372036854775808` 是有效 BIGINT 字面值，即使其无符号绝对值大于 BIGINT 的正数上限。指数、十六进制／二进制字面值、美元符号引用、反斜杠转义字符串前缀、位串以及依赖区域设置的数字均暂缓。UUID／时间戳／double 值使用带类型参数或从 TEXT 显式 CAST，不引入特殊字面值词法类别。

**N012.** 普通执行必须接受恰好一条经解析的语句，并允许末尾最多一个分号。必须拒绝空输入、额外语句或词法单元，以及未闭合的词法结构。批次输入必须是逐条独立解析的语句数组，禁止按分号拆分。注释或字符串内部的 SQL 文本绝不是语句。

源位置使用从 1 开始的 Unicode 码点行／列号，结束位置不包含在范围内。语义等价的规范化源文本可以共享计划缓存项，但字面值和参数值仍属于执行身份的一部分。

## 5. 数据类型与值

**N013.** 标量值必须具有一个声明的逻辑类型，或为上下文类型已知的 SQL NULL。后端值必须通过声明的编解码校验；禁止有损强制转换或暴露为原生裸值。

| 类型写法 | 值域 | 比较／分组 |
| --- | --- | --- |
| `BOOLEAN` | TRUE、FALSE | 相等比较；排序时 FALSE 在 TRUE 前；可空布尔值的 UNKNOWN 对应 SQL NULL |
| `BIGINT` | 有符号 64 位整数 | 精确相等、排序和分组 |
| `TEXT` | 不含 U+0000 的有效 Unicode 标量序列，允许空字符串 | 按码点内容精确比较相等；按 UTF-8 字节字典序排序；不进行规范化或区域化处理 |
| `UUID` | 128 位 UUID；可选类型能力 | 支持相等、IN、DISTINCT、GROUP BY；v1 禁止排序及 MIN/MAX |
| `NUMERIC(p,s)` | 十进制数，1 <= p <= 38，0 <= s <= p | 安全解析公共类型后进行精确相等、排序和分组 |
| `DOUBLE PRECISION` | 有限 IEEE binary64；可选类型能力 | 数值相等和排序；-0 与 +0 比较和分组时相等；禁止 NaN 和无穷值 |
| `TIMESTAMP WITH TIME ZONE` | UTC 时刻，微秒精度，年份 0001–9999 | 按时刻比较相等、排序和分组；没有会话时区 |

本草案的类型名称语法有意排除 INT/INTEGER/VARCHAR/DECIMAL 别名；遇到这些名称时视为不支持的语法，不得推断为隐含别名。不带精度和小数位数的 `NUMERIC` 也不受支持。后续版本化修订可以重新考虑这些选择。

NUMERIC 值是 10^-s 的精确倍数，其绝对值小于 10^(p-s)。小数字面值的类型依据书写的总位数和小数位数确定，不计正负号及整数部分的前导零，精度至少足以容纳小数位数且至少为 1。小数点前必须有一个前导数字零或其他数字。末尾小数零计入推断的小数位数。参数类型显式声明 p/s。

TEXT 不裁剪末尾空格，也没有 CHAR 填充语义。TEXT 字面值、带类型参数和结果均禁止 U+0000；无效参数以 SQL_INVALID_TEXT_VALUE 拒绝，无效已存值／返回值以 SQL_TYPE_ERROR 拒绝，绝不删除该字符后继续。合法字符串／参数编码中的其他非 NUL 控制字符可以作为 TEXT 数据存在；日志和结果仍受保护。原生记录 ID、几何、时长、数组和任意对象不属于这些值域。

**N014.** 对已授权但缺失的可选业务字段，以及显式存储的 null，必须统一映射为关系视图中的 SQL NULL。缺失必需列必须以 `SQL_TYPE_ERROR` 失败；不可读字段必须按第 20 节处理，不得变为普通 NULL。

**N015.** JSON 不是 v1 核心类型。未来登记的 JSON 扩展必须区分 SQL NULL 与 JSON 值 null，并单独规定路径缺失行为。传输层预留了 JSON 标签，并不意味着该扩展已可执行。

## 6. 类型解析与转换

### 6.1 一般解析

**N016.** 同一参数重复出现时，必须解析为同一个声明类型。参数位置必须从 1 连续编号，绑定必须恰好包含这些位置。不得通过试执行后端查询来推断类型。

当存在唯一明确的公共类型时，无类型 NULL 采用另一比较／赋值／CASE／COALESCE／UNION 操作数的类型。`NULL IS NULL` 无需标量载荷类型即可合法使用，因为其结果是不可空 BOOLEAN。`NULL = NULL` 合法，得到可空 BOOLEAN 的 UNKNOWN；编译器可以对这类比较使用内部的仅 NULL 类型。直接投影裸 NULL、结果全为 NULL 的 CASE/COALESCE，或没有类型约束的参数，都要求显式类型声明／CAST。

比较、CASE、COALESCE 和 UNION 的公共类型规则如下：

1. 相同类型保留该类型。
2. BIGINT 与 NUMERIC 混用时可以扩展为 NUMERIC(19,0)；解析得到的 p/s 必须能够精确表示两个值域。
3. 两个 NUMERIC(p,s) 类型取 scale=max(s1,s2)，整数位数=max(p1-s1,p2-s2)，p=整数位数+scale。若 p>38，绑定时拒绝表达式，不得静默减少小数位数。
4. 不进行 TEXT／数值／BOOLEAN／UUID／时间戳之间的隐式转换；不进行精确数值与 DOUBLE 之间的隐式转换。

### 6.2 显式 CAST

**N017.** 除明确规定的浮点转换外，CAST 必须精确生成指定类型，否则返回类型化错误。SQL NULL 可以转换为任意已启用标量类型，且结果仍为 SQL NULL。

| 来源 → 目标 | 行为 |
| --- | --- |
| 相同类型 | 恒等转换，但仍需验证目标类型修饰参数 |
| TEXT → BIGINT | 仅允许可选正负号及数字，无空白；范围为有符号 64 位 |
| TEXT → BOOLEAN | 仅允许不区分大小写的 `true` 或 `false`，无空白 |
| TEXT → NUMERIC(p,s) | 仅允许带符号的十进制／整数写法；不允许指数；允许补齐目标小数位，拒绝丢弃非零位 |
| BIGINT / NUMERIC → NUMERIC(p,s) | 必须精确表示；可移除多余的小数零，不舍入 |
| NUMERIC → BIGINT | 小数部分必须为零，且数值在范围内 |
| BIGINT / NUMERIC → DOUBLE | 仅在启用 `type.double` 时允许；明确允许按 binary64 最近值、恰好中点取偶数舍入；拒绝溢出 |
| TEXT → DOUBLE | 使用后端配置中指明的严格有限十进制／指数解析器；拒绝首尾空白、NaN 和无穷值 |
| TEXT → UUID | 标准带连字符的 8-4-4-4-12 十六进制形式；输入不区分大小写，输出规范化为小写 |
| TEXT → TIMESTAMP WITH TIME ZONE | RFC3339 日期时间，包含 `T`、秒，以及必需的 `Z` 或 ±HH:MM；小数最多 6 位，不允许闰秒 |
| BIGINT/NUMERIC/BOOLEAN/UUID/时间戳 → TEXT | 与区域设置无关的规范编解码写法；时间戳输出 UTC `Z` |

DOUBLE → TEXT 使用固定版本的、能保证有限值往返的最短字符串编解码器；DOUBLE → 精确数值暂缓。时间戳转换拒绝 `-00:00`（表示本地偏移未知）、超范围的本地组成部分／偏移，以及偏移归一化后超出年份 0001–9999 的 UTC 时刻。数字偏移的小时必须为 00–23、分钟为 00–59；转换后检查 UTC 跨日／跨年，不得钳制到边界。未列出的 UUID／数值／BOOLEAN 跨类型转换不受支持。NUMERIC → TEXT 保留声明的小数位数；BIGINT 无前导加号或前导零；BOOLEAN 使用小写 `true`／`false`。浮点 TEXT 解析和格式化必须固定在实现指纹中，原生库默认行为本身不是契约。

## 7. 表达式、谓词与 NULL

### 7.1 布尔与比较语义

**N018.** WHERE、ON、HAVING 及搜索式 CASE 的条件必须为 BOOLEAN。不得使用数值／字符串／原生类型的真假值转换。仅 TRUE 通过过滤或形成 ON 匹配，FALSE 和 UNKNOWN 均不通过。

| A | B | A AND B | A OR B |
| --- | --- | --- | --- |
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

AND/OR 满足交换律。NOT TRUE=FALSE；NOT FALSE=TRUE；NOT UNKNOWN=UNKNOWN。UNKNOWN 是 NULL BOOLEAN 的真值解释，不是独立存储的标量标签。

`=`、`<>`、`<`、`<=`、`>`、`>=` 用于具有可比公共类型的操作数。接受 `!=` 作为 `<>` 的别名。普通比较只要涉及 SQL NULL，就产生 UNKNOWN，包括 NULL 与 NULL 的比较。在另行规定排序能力之前，UUID 仅支持相等／不等比较。`IS NULL` 和 `IS NOT NULL` 返回不可空 BOOLEAN。

对于 `x IN (a,b,...)`，若任一带类型比较为 TRUE，则结果为 TRUE；否则若任一比较为 UNKNOWN，则结果为 UNKNOWN；其余情况为 FALSE。NOT IN 对该结果应用逻辑 NOT。列表必须非空且为标量值；IN 子查询、行构造器和数组成员判断暂缓。因此，左操作数为 NULL 时，与非空列表比较得到 UNKNOWN。

**N019.** 布尔求值顺序不构成对用户可见的短路保证。校验必须检查所有分支，包括不可达分支的资源、类型和副作用权限。CASE/COALESCE 的值求值遵循第 7.2 节，但不得因此忽略分支中的绑定错误。

### 7.2 CASE 与 COALESCE，R2

搜索式 `CASE WHEN condition THEN value ... [ELSE value] END` 返回第一个条件为 TRUE 的分支；省略 ELSE 时返回带类型 SQL NULL。所有结果分支解析为同一个公共类型。条件为 FALSE 或 UNKNOWN 时继续检查后续分支。简单 CASE 暂缓。

`COALESCE(a,b,...)` 至少需要两个具有公共结果类型的参数；返回第一个非 NULL 参数，若全部为 NULL 则返回带类型 NULL。全部参数都是无类型 NULL 时拒绝，除非显式转换提供公共类型。

**N020.** 对标量表达式，未选中的 CASE 结果以及 COALESCE 已选中值之后的参数，不得引发运行时值错误。编译器仍必须绑定和授权其内容。分组聚合在 SELECT 的标量 CASE 之前计算，因此不能使用 CASE 屏蔽聚合错误。

### 7.3 可选算术与文本表达式

`expr.numeric_arithmetic` 为解析到相同数值域的操作数启用一元 +/- 和二元 +,-,*,/。一元符号传播 SQL NULL。二元运算符的已求值操作数中只要有 SQL NULL，就返回带类型 SQL NULL，包括带类型 NULL 除以零；除法运算符仅在两侧均非 NULL 时检查除数是否为零。但仍须求值各操作数表达式自身的错误，顺序不限，因此 NULL 加上一个单独求值就会失败的 CAST 仍是错误。CASE/COALESCE 保留其明确的惰性值分支语义。BIGINT +,-,* 返回 BIGINT 并检查溢出；BIGINT / BIGINT 返回 NUMERIC(38,6)，按恰好中点取偶数舍入。除以零报错。BIGINT/NUMERIC 混用时先按第 6 节精确解析；所有 NUMERIC 运算遵循下述规则。DOUBLE 仅与 DOUBLE 运算，返回有限 binary64，并拒绝非有限结果和除以零。

NUMERIC +,- 返回 NUMERIC(38,max(s1,s2))；乘法返回 NUMERIC(38,min(38,s1+s2))，但超过 38 位小数时，若需丢弃任何非零小数位，必须拒绝而非截断。NUMERIC 除法返回 NUMERIC(38,max(s1,s2,6))，仅在生成结果小数位数时按恰好中点取偶数舍入一次。所有运算均拒绝整数部分无法容纳的结果。算术精度和小数位数在执行前确定，不随行值变化。

`expr.text_basic` 启用 TEXT 拼接 `||`、`CHAR_LENGTH(TEXT) -> BIGINT` 和 `OCTET_LENGTH(TEXT) -> BIGINT`。拼接和这两个函数均传播 NULL。字符长度统计 Unicode 标量值，不统计字素簇；字节长度统计 UTF-8 字节。不进行标量到 TEXT 的隐式转换。LIKE、正则、LOWER/UPPER、区域化排序及用户函数均暂缓。

运算符优先级从高到低依次为：括号／CAST／函数／CASE；一元符号；*/；二元 +/-；||；比较／IN／IS NULL；NOT；AND；OR。二元算术与拼接左结合。比较不得连写：`1 < 2 < 3` 无效。

## 8. SELECT、排序与逻辑行数上限

### 8.1 逻辑求值

**N021.** SELECT 的行为必须等价于以下顺序：绑定并授权关系／列 → 获取经资格验证的输入视图 → 对每个关系应用行策略 → FROM/JOIN → WHERE → 存在时执行 GROUP／聚合 → HAVING → 投影 → DISTINCT → ORDER BY → 逻辑 LIMIT/FETCH → 经授权发布结果。只有在证明语义等价时，物理执行顺序才可不同。

R1 要求 FROM 中恰好包含一个关系。不带 FROM 的 SELECT 暂缓。投影接受已启用能力允许的标量表达式，并可使用 `AS output_name`；v1 为输出指定别名时必须写 AS。未指定别名的简单列使用其列名；其他未指定别名的表达式使用确定性的 `expr_1`、`expr_2` 等标签，数字取其投影序号。顶层读取允许重复输出标签，因为传输行使用序号表示列，但不得以存在歧义的方式引用这些标签。

`*` 或 `alias.*` 按目录顺序展开已授权的绑定列。v1 不允许在同一 SELECT 列表中把星号与其他项混用。未授权或受逐行掩码影响的字段不得被静默纳入后再置为 NULL。展开结果冻结在制品中；不兼容的绑定／策略变更会使其失效。

**N022.** 默认 SELECT ALL 必须保留重复的投影行。DISTINCT 要求 R2，在元组相等判定时将 SQL NULL 归为同组。必须比较完整的带类型元组，不能只比较哈希值。对于 DISTINCT，ORDER BY 表达式必须是已投影表达式或唯一输出标签；隐藏排序列不得改变去重语义。

### 8.2 ORDER BY

每个排序键必须是允许的输入／投影列引用，或唯一输出别名；按数字序号排序及任意排序表达式暂缓。默认方向为 ASC。默认 NULL 位置为 ASC NULLS LAST、DESC NULLS FIRST；显式 NULLS FIRST/LAST 可覆盖默认值。

**N023.** 所有可空排序键，包括因 LEFT JOIN 而变得可空的键，都必须要求 `read.nullable_order`。未启用该能力时，校验拒绝该排序。所有键均使用声明的逻辑比较规则，不采用后端区域设置或记录顺序行为。

R1 最多支持四个排序键。R2 保留相同的默认上限，除非安装实例公布更高且经资格验证的限制。显式排序键未构成全序时，并列项之间的顺序未定义。执行器内部可以选择可重复顺序，但不能将其承诺为 SQL 语义。

### 8.3 LIMIT 与 FETCH

LIMIT n 和 FETCH FIRST n ROWS ONLY 是两种互斥的非负整数字面值行数上限，数值须在 BIGINT 及公开的最大逻辑结果界限之内。LIMIT 0 返回带类型空结果，但仍执行绑定和授权检查。同时使用两种形式、OFFSET、LIMIT ALL、FETCH NEXT 和 WITH TIES 均暂缓。

**N024.** 不写 LIMIT 必须表示在显式资源约束下返回完整逻辑结果，而不是使用未记录的默认 LIMIT。SQL 行数上限必须与传输页大小、截止时间和扫描预算区分。部分结果不得报告为完整结果。

没有 ORDER BY 时，LIMIT 选中哪些行未定义。精确的跨页继续读取要求满足第 17 节的更强条件；传输层不得静默追加 id 排序键并宣称这是用户请求的 SQL 顺序。

## 9. JOIN

R2 支持在两个关系引用之间执行一次 INNER JOIN 或 LEFT [OUTER] JOIN。单写 JOIN 等价于 INNER JOIN。当限定名可能存在歧义时，两侧必须使用无歧义别名。RIGHT/FULL/CROSS/NATURAL JOIN、USING、逗号连接及横向连接暂缓。

**N025.** ON 必须是非空的带类型相等条件合取，每项比较左侧关系的一列与右侧关系的一列。v1 连接条件不允许 OR、常量、其余不等式或副作用。每个输入必须已满足其当前原生行策略。

INNER JOIN 输出所有匹配行对并保留重数。LEFT JOIN 输出所有匹配行对；若不存在已授权的右侧匹配元组，则输出一行右侧补 NULL 的元组。原生缺失值与 SQL NULL 不通过普通相等比较形成匹配。WHERE 在 JOIN 之后执行；对右侧补 NULL 列进行过滤可能删除该输出行。

**N026.** 两个输入关系必须从同一个经资格验证的一致视图读取；禁止连接独立实时分页 API 的结果。除非在 SQL NULL、重复行及策略规则下证明等价，否则规划器不得将 LEFT JOIN 替换为 INNER JOIN，也不得将 WHERE 谓词移动到 ON 中。

经资格验证的输入视图是内部执行保证，并不授权声明某个具名 PostgreSQL 隔离级别。普通 R1 游标在各页独立执行之间仍可能对应可变的实时列表。

## 10. 分组与聚合

GROUP BY 仅接受显式输入列引用；输出别名、序号、表达式分组、rollup/cube/grouping sets 及基于函数依赖放宽分组约束均暂缓。允许无聚合的分组，每组输出一行。SQL NULL 值形成同一组；复合分组相等性遵循元组语义。

**N027.** 在分组查询中，SELECT/HAVING/ORDER BY 内所有非聚合列引用都必须是 GROUP BY 键。在没有 GROUP BY 的聚合查询中，不得投影非聚合输入列，也不得在 HAVING/ORDER BY 中引用这些列。聚合调用仅允许出现在 SELECT/HAVING，且不得嵌套。

HAVING 要求查询存在分组或聚合，仅保留 TRUE。WHERE/ON/GROUP BY 不得包含聚合调用。ORDER BY 可以使用唯一的已投影聚合别名，但不能引入新的聚合表达式。聚合 DISTINCT、FILTER、有序聚合及窗口子句暂缓。

| 签名 | 结果类型 | 空输入／全部为 NULL 时的行为 |
| --- | --- | --- |
| COUNT(*) | BIGINT NOT NULL | 0 |
| COUNT(x)，x 为任意已启用标量 | BIGINT NOT NULL | 0 |
| SUM(BIGINT) | NUMERIC(38,0) | NULL |
| SUM(NUMERIC(p,s)) | NUMERIC(38,s) | NULL |
| AVG(BIGINT) | NUMERIC(38,6) | NULL |
| AVG(NUMERIC(p,s)) | NUMERIC(38,max(s,6)) | NULL |
| MIN/MAX(x)，x 为 BOOLEAN/BIGINT/TEXT/NUMERIC/时间戳 | 与 x 相同的类型 | NULL |
| SUM/AVG(DOUBLE) | DOUBLE PRECISION | NULL |
| MIN/MAX(DOUBLE) | DOUBLE PRECISION | NULL |

可选类型签名要求相应能力。UUID 允许用于 COUNT/DISTINCT/GROUP BY，但不允许用于 MIN/MAX。NUMERIC 是 R2 必需能力，确保 BIGINT 聚合始终具有明确的精确结果表示。

**N028.** 除 COUNT(*) 外的聚合必须忽略 SQL NULL 输入。精确数值的 SUM 必须使用数学上精确的累加器，并检查最终声明结果；AVG 必须用精确总和除以计数，并仅在生成其声明的小数位数时按恰好中点取偶数舍入一次。结果无法容纳时必须报错。COUNT 溢出也报错。

浮点聚合的累加顺序可以变化，必须公布其编解码器／算法、允许的比较误差及可重复性限制。不能仅因返回了有限浮点值，就认为满足精确数值等价性。SUM/AVG 不得为了满足工作预算而静默截断数据集。

输入为零行时，无 GROUP BY 的聚合查询在 HAVING 前恰好产生一行聚合结果；有 GROUP BY 的查询产生零个组。TEXT 的 MIN/MAX 使用字节序。即使当前输入非空，也保留聚合结果的可空元数据。

## 11. 可选关系查询结构

### 11.1 非递归 CTE

`read.cte` 启用 `WITH name AS (select), ... select`。CTE 主体和主语句都必须是 SELECT 查询。CTE 可以引用更早定义的 CTE，不得引用自身或后续项；名称重复或循环均为错误。每个 CTE 必须投影明确且唯一的输出名称；列名称列表、递归／数据修改 CTE 及物化提示暂缓。CTE 名称在语句内隐藏同名且未限定的 public 表；显式 `public.name` 仍引用该表。

**N029.** CTE 必须保留多重集合、NULL、类型、血缘及已授权一致视图语义。物化／内联不得改变查询结果或绕过预算。每个查询块仍受两个关系的连接上限约束；完整语句还受公开的关系总数／节点总数限制。

### 11.2 EXISTS

`read.exists` 启用带非关联 SELECT 主体的 [NOT] EXISTS，且仅能作为谓词使用。其已授权主体结果至少有一行时返回 TRUE，否则返回 FALSE，绝不返回 UNKNOWN。主体必须恰好投影一个字面值 `1`，且所有关系／过滤引用均需绑定和授权。关联子查询、标量子查询、IN 子查询以及任意投影形式的 EXISTS 均暂缓。

EXISTS 观察主体在逻辑 WHERE／分组／上限处理后的结果，因此 LIMIT 0 得到 FALSE；对能够产生聚合结果的 FROM 执行 `SELECT 1`，不会因此成为特殊捷径。EXISTS 主体不得削弱父查询的一致输入视图要求。

### 11.3 UNION ALL

`read.union_all` 启用有界的 SELECT 分支链，不启用 UNION DISTINCT/INTERSECT/EXCEPT。分支必须具有相同列数；各列位置解析为一个公共类型。标签取自第一个分支；输出可空性为所有分支对应列可空性的合并。保留全部重复行。

**N030.** UNION ALL 各分支必须共享语句的经资格验证的一致视图及授权血缘。没有最终 ORDER BY 时，分支输出顺序未定义。v1 不允许分支各自带 ORDER BY 或行数上限；最终 ORDER BY 仅引用唯一输出标签，最终上限作用于整个并集。

仅当全部必需能力已启用，且完整 AST 满足语法、深度和预算规则时，才能组合 CTE/EXISTS/UNION。可选语法不会放宽父查询限制。

## 12. 数据修改

### 12.1 W1 通用规则

**N031.** W1 必须编译为现有作用域内的带类型命令，并在一个原生事务中满足原有 Operation/Outbox/guard 约束。禁止直接以系统身份执行用户文本，也禁止依次调用各自独立提交的命令来冒充原子执行。

目标为已发布的 `public` 表，经校验制品包含准确的预期 Schema／映射修订号。W1 不支持目标别名、连接、FROM/USING 子句、子查询、副作用、用户提供的触发器、生成值或表达式赋值。值只能是字面值、带类型参数或对值的 CAST，不能引用业务列。

INSERT 必须显式列出列名，且恰好包含一次 `id`。UPDATE 赋值中每个业务列最多出现一次。不得赋值平台修订号／时间戳／owner／ACL 字段。Schema 写权限及 NOT NULL／类型／默认值规则适用于每项赋值和省略字段。

### 12.2 INSERT

基础 W1 接受一个 `VALUES (...)` 元组，其列数必须与显式且不重复的列列表一致。逻辑 id 是非 NULL TEXT。采用“仅不存在时创建”，不得覆盖已有 ID。除非存在经资格验证的字面默认值，否则省略的可选业务列成为 SQL NULL；省略无默认值的必需列则失败。显式 NULL 不触发默认值。

**N032.** INSERT 成功时必须提交修订号为 1 的行，并返回 affected_rows=1。唯一性／id 冲突必须返回统一且经敏感信息清理的完整性错误，不包含已有行数据或约束细节。条件冲突错误不证明受保护行可读；服务无法承诺在信息论意义上完全隐藏攻击者自选唯一键是否已占用。

`write.multi_values` 可选地接受多个字面值／参数元组。一个请求内，包括所有语句在内的修改总行数仍须 <=16。语句／批次内目标 ID 重复时，在修改前拒绝；多行 INSERT 不得部分成功。INSERT SELECT、DEFAULT VALUES、RETURNING *、ON CONFLICT/UPSERT 及自动生成身份均暂缓。

### 12.3 UPDATE 与 DELETE

**N033.** UPDATE/DELETE 必须带 WHERE 谓词，该谓词是原子比较／NULL 检查的合取，并强制包含精确的 `id = value` 和 `revision = value` 两项。每种守卫必须恰好一个，左侧为 id/revision，右侧为非 NULL 带类型标量值，id 为 TEXT，revision 为正 BIGINT。W1 谓词禁止 OR、NOT、IN、函数或列对列守卫。

括号可以分组这些合取条件，但不得使任一守卫变为可选。附加条件可以读取已授权业务列；v1 拒绝除强制守卫之外对 id/revision 的额外引用。UPDATE 赋值不得引用旧行数据；用户先读取修订号，再显式准备新的目标值。

已授权 UPDATE 将当前修订号加 1，并在支持时更新映射的时间戳，即便业务值未变化。DELETE 通过现有删除命令删除当前行或写入墓碑；RETURNING 引用已授权的删除前行。

**N034.** 普通未匹配 UPDATE/DELETE 必须返回 affected_rows=0 和空 RETURNING 行集，对目标不存在、不可见、修订号不匹配或附加条件不匹配保持一致。将现有 CAS 失败转换为零匹配，必须以证明没有修改提交为前提。Schema／会话／守卫失败不是零匹配。

### 12.4 RETURNING

RETURNING 接受显式、非空的已授权简单列列表，可附带 AS 别名。INSERT/UPDATE 返回修改后值，包括新修订号；DELETE 返回删除前值。所有结果仍受最终发布检查保护。省略 RETURNING 时仍返回受影响行数，不得编造业务结果列。

**N035.** 已提交写入的 RETURNING 内容若当前无法发布，必须保留其已提交操作结果。服务必须隐去内容，不得报告回滚，也不得自动换新键重发修改。

## 13. 请求事务、幂等与未知结果

### 13.1 原子请求契约

事务是一次提交的 W1 语句数组，不是交互式 SQL 会话。基础限制为最多 16 个条目、总修改行数最多 16，限定相同作用域／环境代次，每个目标逻辑行最多修改一次。禁止 SELECT 和 DDL 条目、保存点、条目之间的值依赖，以及跨请求 BEGIN/COMMIT。RETURNING 提供写操作的读取结果。

**N036.** 事务必须原子验证当前原生主体／会话／会话族、Schema／映射、记录守卫及准入约束，然后一起提交业务变更、有序逐项结果、原始 Operation 收据及 Outbox 记录。已确认的提交前失败不得留下部分业务变更，也不得发布部分 RETURNING。

请求契约允许对 UPDATE/DELETE 条目附加 `require_affected_rows: 1` 断言；该条目将匹配零行时，整个事务中止。普通独立 SQL 仍保持零匹配成功的语义。条目结果遵循请求顺序；批次提交前不发布中间结果。

此原子请求保证不隐含任何具名 SQL 隔离级别。`SET TRANSACTION`、SERIALIZABLE 标签及关于幻读／写偏斜的声明都要求独立的资格验证契约；不支持的请求应拒绝，而非忽略。

### 13.2 原始键身份

**N037.** 每次已接纳执行必须具有一个原始幂等键，绑定主体、作用域／环境代次、语言／编译器／档位指纹、规范化带类型 IR、带类型值、预期修订号及有序批次断言。同键不同身份必须冲突；同键同身份必须在当前授权下关联原操作。

规范化 IR 必须保留所有语义差异，包括字面值、有语义意义时的十进制小数位数、NULL 类型、对重复项敏感的运算符及条目顺序。语言不强制采用某种 JSON 序列化器或密码学摘要；实现契约必须固定其规范化规则及以键确定身份的协议。

重复读取关联其原执行，不构成新读取。受保护结果到期后，原读取返回 `SQL_RESULT_EXPIRED`；用户明确发起的新读取可以使用新键。查询状态不得创建或重放旧操作正文。

### 13.3 结果与取消

**N038.** 回复丢失、到达截止时间、客户端断开、缺少观察结果或收到取消请求，均不得被解释为回滚、失败、底层物理执行完成或允许换新键修改。核对必须引用原始操作／键／环境代次。

现有操作权威区分已接纳／执行中、确认已提交、确认失败及未知／需要核对等结果。SQL 必须复用该权威，不得维护另一个可独立写入的提交状态。仅在证明原尝试未提交之后，后端确认的冲突才可能允许有界的完整事务内部重试；普通传输错误不具备该含义。

撤权可能阻止用户查看现有操作。授权失败不改变持久操作的结果。恢复后，旧环境代次的身份和制品不能仅凭复用原键访问新目标。

## 14. Schema 定义与迁移

M1 将 DDL 解析为提案。按第 14 节限制语法，接受 CREATE TABLE、ALTER TABLE ADD COLUMN、CREATE INDEX、DROP INDEX 和 DROP TABLE。各项均作用于当前 public Schema，SQL 之外携带预期 Schema／映射元数据。预览成功创建的是提案，不是对在线数据库的变更。

**N039.** 只有现有 Schema 服务，使用当前 SchemaAdmin 权限及具有安全围栏的维护权威，才能应用 DDL 提案。查询执行不得安装原生 Schema，也不得向自身授予管理凭据。

### 14.1 列与约束

CREATE TABLE 必须恰好包含一个 `id TEXT PRIMARY KEY` 列。PRIMARY KEY 仅允许用于 id，隐含 NOT NULL，且不能写为表级约束。平台修订号／时间戳由绑定管理，用户不得将它们声明为业务列。其他声明列默认可空，除非指定 NOT NULL。新建绑定的列顺序为 id、revision、经资格验证后存在的 created_at/updated_at，随后为按声明顺序排列且不含 id 的业务列。已有绑定保留其明确发布的顺序；ADD COLUMN 将新业务列追加到末尾。

`schema.literal_default` 允许 `DEFAULT <literal>` 或对字面值进行 CAST，并按目标类型检查一次。参数、函数、SQL 表达式、序列、INSERT 中的 DEFAULT 关键字、生成列及易变默认值均暂缓。默认值作用于 INSERT 省略的列；SET 显式赋 NULL 后仍为 NULL。

**N040.** 对非空关系执行带 NOT NULL 的 ADD COLUMN，必须有明确且经资格验证的默认值／回填来源，并在发布前实际验证。如果提案语言无法表达足够安全的回填，必须拒绝提案，要求另行进行经审查的 Schema 迁移。

不带默认值的 ADD COLUMN 对所有历史行呈现 SQL NULL，因此仅允许用于可空列或已经证明为空的关系。带经资格验证字面默认值的 ADD COLUMN，无论列是否可空，都必须在发布新绑定之前为每个历史行物化该默认值。默认值不会在后续读取时动态替换缺失值或 null。此后所有修改路径都必须遵循已发布的省略值／默认值契约。

逻辑索引位于当前 `public` Schema；索引名称在该环境所有逻辑 SQL 表之间唯一。每个索引绑定恰好一个表身份，以及不可变列列表／类型映射。CREATE 使用“仅不存在时创建”的名称预留；任何当前名称冲突均返回经过敏感信息清理的 SQL_CONSTRAINT_CONFLICT，不透露所有者／表细节。以同一原始操作重试提案时，核对原有名称预留。DROP 解析 `public.index_name` 或不带限定名的等价写法，要求对所属表具有管理权限并提供预期索引／绑定修订号；对于名称不存在或未授权的情况，统一返回 SQL_REFERENCE_DENIED。逻辑名称不得指向调用方选择的物理索引。

CREATE INDEX 针对显式命名且经资格验证的标量列创建非唯一索引提案。索引方法、物理名称和就绪状态归适配器管理；没有经资格验证的映射时拒绝提案。DROP INDEX/TABLE 使用明确的当前资源版本并经过破坏性变更审查；不定义 CASCADE/IF EXISTS/IF NOT EXISTS 快捷路径。

UNIQUE、FOREIGN KEY、CHECK、可延迟约束、约束校验提示及级联动作均暂缓。除非每个写接口及直接原生写入边界都遵守相应约束，否则不得将已接受的原生声明宣传为 SQL 强制约束。仅在 SQL 路径校验，不证明数据库全局不变量成立。

### 14.2 发布与失败

**N041.** 迁移必须采用：预览 → 预期版本检查 → 关闭准入／排空 → 扩展／回填 → 实际 Schema／数据／索引验证 → CAS 发布绑定 → 按当前安全水位重新开放。部分完成、不兼容或未知状态必须保持未发布／BLOCKED，等待原始操作核对。

索引准备／就绪与绑定发布是不同状态。移除／收缩必须尊重保留中的制品、版本和活跃所有者。仅运行旧二进制不能回滚破坏性变更。恢复时必须重新验证映射资格，并使旧环境代次制品／游标失效。

## 15. 目录与能力发现

**N042.** 目录数据必须从当前已授权、已发布的绑定生成，绝不能取自特权原生 Schema 导出。不得披露不可见资源的名称、序号、类型、基数或物理位置。

R1 最低要求的虚拟关系为：

| 关系 | 有序列 |
| --- | --- |
| `information_schema.tables` | table_schema TEXT, table_name TEXT, table_type TEXT |
| `information_schema.columns` | table_schema TEXT, table_name TEXT, column_name TEXT, ordinal_position BIGINT, data_type TEXT, is_nullable TEXT |
| `mensoria.sql_capabilities` | feature_name TEXT, enabled BOOLEAN, profile TEXT, language_version TEXT |

目录列不可空。table_type 为 `BASE TABLE`；is_nullable 为 `YES` 或 `NO`；data_type 是规范 SQL 写法，包括 NUMERIC(p,s)。ordinal_position 是冻结的绑定位置，即便过滤未授权列后留下空号也不改变。这里不承诺隐藏全部 Schema 形状推断；访问目录本身要求元数据权限。目录中不包含原生位置、秘密或系统表。

能力发现通过传输 API 暴露公共能力 ID、在当前作用域下的有效可用性及清单元数据，不得借此断言不存在的业务资源存在。实现必须公布编译器／后端／档位／Schema 适配器版本、能力／类型／函数编解码器、限制／执行模式和证据引用。不得把未知清单版本静默解释为某个更旧的兼容版本。

## 16. 校验、制品与 EXPLAIN

**N043.** 校验必须完成解析、穷尽检查 AST 节点、解析已授权元数据、绑定类型／可空性／副作用、执行能力／大小／预算规划门槛检查，并记录不可变依赖修订号。校验结果不授权执行或任何外部副作用。

制品绑定源文本／规范计划摘要、声明的参数类型、作用域／环境代次、主体授权约束、Schema／映射／安全版本、编译器／档位指纹及到期时间。SQL 字面值和源文本属于受保护制品内容。仅元数据预览不得借用普通业务读取权限或管理凭据。

**N044.** 执行必须加载准确的制品修订版，并在访问后端前以及发布结果前再次检查当前授权和兼容性。编辑以及不兼容的 Schema／策略／编译器／环境代次变更都要求重新校验；不得静默重新编译或提升已有制品。

EXPLAIN 是经过授权且不执行查询的逻辑计划操作，通过传输路由或 `EXPLAIN <select>` 语法接受时，要求启用 `plan.explain`。它返回逻辑资源引用、带类型运算符、所需能力及拟议有效限制。不得扫描业务数据，不得暴露原生文本／位置／隐藏基数，也不得执行 ANALYZE。参数采样和优化器建议不能发布 Schema 变更。

## 17. 参数、结果与分页

### 17.1 值与结果形状

**N045.** 参数必须绑定标量值，绝不能绑定标识符、关键字、方向、表达式、作用域或可执行片段。包含 SQL 语法的字符串仍是 TEXT 值。另行规定之前，禁止通过数组／JSON／原生带标签参数绕过限制。

结果元数据包含有序列，每列具备从 1 开始的序号、标签、声明逻辑类型／类型修饰参数及可空性。行按相同顺序使用数组表示，允许标签重复而不丢失数据。Schema 类型不因当前值恰好为 NULL 而变化。

传输使用带标签值。BIGINT/NUMERIC 使用精确十进制字符串；UUID／时间戳使用规范字符串；BOOLEAN 使用布尔值；DOUBLE 使用有限数字；SQL NULL 使用 `{"type":"null"}`。可空列中的非 NULL 值保留其普通类型标签。完整 JSON 形状由接口契约规定。DML 的 `affected_rows` 是精确 BIGINT 十进制字符串；SELECT 中该字段为 null。

### 17.2 继续读取与完整性

**N046.** 传输 page_size 不得改变 SQL LIMIT。LIMIT 120/page_size 50 的结果最多分为 50/50/20 行。继续读取必须跟踪剩余逻辑上限和已消费行数，不得每页重新执行 LIMIT 120。

可继续的 R1 实时 keyset 分页要求显式全序，包含已授权且唯一的逻辑 id。可空排序要求正确的 NULL 排位／值／id 继续谓词及对应能力。没有已证明的全序时，执行器必须一次交付有界完整结果，或拒绝继续读取。R2 的连接、聚合、DISTINCT 和 UNION 要求保留经资格验证的完整结果，或使用另行证明正确的可继续执行计划；简单 id 游标不足以满足要求。

**N047.** 游标必须绑定主体／授权、查询／制品／带类型绑定摘要、版本、作用域／环境代次／安全序列、排序状态、剩余上限及原始到期时间。每页，包括空响应或仅游标响应，都必须通过当前结果发布授权。角色／Schema／环境代次变更、到期或摘要变化都会使游标失效。

实时 keyset 是跨页可变列表：排序键变化、插入和删除都可能导致遗漏或重复。它不是事务快照。物化结果必须来自经资格验证的输入视图并保留受保护来源信息；到期或撤权终止访问。快照导出使用另行完成资格验证的现有 SnapshotTicket 流程。

**N048.** 响应必须区分完整逻辑结果、可继续读取的普通部分页面，以及因预算／截止时间／错误而不完整的结果。不完整聚合不得标记为完整。不得从页面长度推断总行数。传输字段为 `page.result_complete`，不能用无关的成功标志代替。

## 18. 诊断

**N049.** 错误必须包含稳定的 Mensoria 错误码、五字符 SQLSTATE 风格类别、经过敏感信息清理的消息、阶段、重试提示，以及已接纳且当前可见时的原始操作引用。能够安全定位时可附带源位置范围。不得包含受保护原生文本、资源存在性细节、值、凭据或后端堆栈。

| 错误码 | 类别 | 触发条件 |
| --- | --- | --- |
| SQL_SYNTAX_ERROR | 42601 | 无效词法单元／语法或额外语句 |
| SQL_FEATURE_UNSUPPORTED | 0A000 | 已规定可选能力未启用、暂缓语法或不支持节点 |
| SQL_REFERENCE_DENIED | 42501 | 未知／未授权公共引用 |
| SQL_TYPE_ERROR | 42804 | 类型不兼容、编解码／来源映射无效或类型未解析 |
| SQL_VALUE_OUT_OF_RANGE | 22003 | 溢出、不允许的精度损失或非有限数字 |
| SQL_INVALID_TEXT_VALUE | 22018 | 文本无法解析为声明标量类型 |
| SQL_DIVISION_BY_ZERO | 22012 | 实际求值的数值除法除以零 |
| SQL_AMBIGUOUS_REFERENCE | 42702 | 允许使用的名称匹配多个已授权对象 |
| SQL_INVALID_GROUPING | 42803 | 聚合位置非法或引用未分组列 |
| SQL_ARTIFACT_STALE | 55000 | 执行依赖修订版不兼容 |
| SQL_WRITE_PRECONDITION_REQUIRED | 0A000 | 缺少 W1 强制守卫形状，或形状不安全 |
| SQL_PRECONDITION_FAILED | 40001 | 显式受影响行数断言失败 |
| SQL_CONSTRAINT_CONFLICT | 23000 | 经过敏感信息清理的完整性约束冲突 |
| SQL_KEY_CONFLICT | 23000 | 已有原始键绑定到不同请求身份 |
| SQL_BUDGET_EXCEEDED | 54000 | 超出已证明的资源界限，或计划缺少所需可强制执行预算 |
| SQL_CURSOR_INVALID | 24000 | 游标到期或绑定／版本不匹配 |
| SQL_RESULT_EXPIRED | 55000 | 原受保护结果不再保留 |
| SQL_OUTCOME_UNKNOWN | 08007 | 已接纳操作／提交尚未确认 |
| SQL_DEPENDENCY_UNAVAILABLE | 08006 | 必需依赖不可访问 |
| SQL_CANCEL_PENDING | 57014 | 已请求取消，但物理执行／提交结果尚未确认 |

这些类别不承诺 PostgreSQL 驱动行为。尤其是，40001 绝不授权盲目换新键重试，57014 绝不证明回滚。客户端必须联合使用 Mensoria 错误码、phase、retry_hint 和操作引用。

重试提示为 `edit`、`revalidate`、`restart_read`、`reconcile_original`、`observe_original`、`none`。准入之后的不确定性，优先于表面上会暗示“没有执行任何工作”的传输／前置条件错误。授权失败可以隐藏操作可见性，但不改变其持久结果。

## 19. 预算、截止时间与取消

**N050.** 已启用实现必须强制执行并公布源文本／请求体大小、AST 节点数／深度、结果列／页面字节数、修改行数、执行所有权、并发，以及计划使用的每种底层物理工作／中间资源界限。无法强制执行必需预算时，必须拒绝计划。

初始设计上限为：请求体 <=64 KiB；AST 节点 <=1,024；深度 <=32；选择列 <=32；排序键 <=4；page_size 默认 50、最大 100；页面字节 <=256 KiB；批次条目 <=16；总修改行数 <=16。这些是拟议准入界限，不是容量或 SLO 实测。经资格验证的安装实例可以公布更低界限；提高界限要求相应资格验证。

扫描行数／字节、输入快照大小、连接扇出、聚合组数、排序内存、结果物化、执行时长及租户并发，都需要在清单中具有明确的有效数字上限和执行模式。LIMIT 1 不限制聚合／连接／排序的工作量。等待 RPC 的时间不构成底层物理工作量界限。

**N051.** 服务必须区分客户端等待超时、执行截止时间、取消意图、确认 worker 完成和确认提交结果。在实际完成，或既定安全围栏／核对规则允许释放之前，必须继续核算执行所有权和许可占用。服务必须隐去未授权或过期的迟到结果。

已发布的部分读取字节无法收回。结果发布围栏必须定义撤权从哪个边界开始阻止后续字节，不得宣称能够撤回网络字节。流式输出和可继续读取能力，需要超出缓冲页面测试范围的证据。

## 20. 授权、血缘与审计

**N052.** SQL 必须复用原生行／字段授权、限定作用域的 Control 准入及当前会话／会话族检查。不得用特权扫描后过滤、缓存授权、调用方指定角色或具有业务数据访问权的签发身份替代这些机制。

在投影、谓词、排序、连接、分组、聚合输入、CASE 分支及 RETURNING 中引用受保护字段，均予以拒绝。无法证明对整个绑定输入均可读的逐行字段掩码，会使该 SQL 列不能用于该制品。星号仅展开可证明可读的列。出现预期外被掩码值时，使待发布结果失效，不得将其当作缺失数据。

**N053.** 读取计划、历史、元数据、缓存结果、制品、游标及原始操作结果时，都必须按当前权限重新授权受保护内容。计划缓存键不是授权凭据。最终发布之前撤权时，即使后端计算已经完成，也必须隐去待发布内容及后续读取能力。

聚合可能有意披露已授权行的统计信息；本语言提供访问控制，不提供差分隐私。必须记录唯一键冲突、已授权计数和目录形状带来的推断风险，不得虚假承诺普遍不可推断。原生错误的敏感信息清理仍为强制要求。

**N054.** 审计必须关联主体／作用域、制品／编译器／档位／Schema 版本、脱敏查询形状和带类型值摘要、原始操作、安全／环境代次水位、已消耗预算、执行结果及发布状态。普通日志必须省略原始 SQL 字面值、参数、结果行和凭据；查询／主体标签不得导致指标基数无限增长。

审计保留和支持访问遵循现有平台控制。模型生成的 SQL 是不可信源文本。向外部模型披露 SQL 文本、Schema 样本或结果数据，需要另行具备当前有效的披露授权，不得在执行中隐式发生。

## 21. 多模型扩展框架

**N055.** 语言扩展在其解析器／执行器接受输入之前，必须登记稳定的 `mensoria` 命名空间、精确语法／签名、参数／结果编解码器、NULL 行为、确定性／副作用、作用域／血缘、限制、索引就绪条件、证据及版本规则。核心表达式不得静默透传原生 SurrealQL 片段。

本草案不规定任何可执行 JSON／图／全文／向量函数。能力发现中的相应名称仅是能力预留。未来扩展规范至少需要定义：

| 扩展 | 必需的补充契约 |
| --- | --- |
| JSON | SQL NULL 与 JSON null、路径缺失、提取／转换、对象／数组相等性、重复键及嵌套限制 |
| 图 | 边关系绑定、允许方向／标签、逐跳策略、环路、深度／边／顶点限制、结果血缘 |
| 全文 | 分析器／语言／索引修订号、匹配／评分语义、授权前置过滤、就绪条件和确定性限制 |
| 向量 | 维度／距离度量／值编解码器、精确与 ANN 模式、候选／输出预算、过滤语义、索引代次及召回评估 |

现有已批准的边集合在绑定通过资格验证后，可以作为普通 R2 关系查询，但这不启用图遍历语法。箭头路径、原生函数调用、实时订阅及提供方专有向量运算符仍予以拒绝。

**N056.** 外部模型调用、嵌入生成、HTTP／文件访问、对象上传及任务调度，不得作为隐藏 SQL 事务副作用发生。它们仍是独立授权的平台命令，具有自己的外部未知结果核对流程。ANN 结果绝不得宣称满足精确关系等价性。

## 22. 兼容性、版本化与实现要求

**N057.** 每个已接受制品必须绑定语言版本、草案／语义修订号、编译器指纹、已启用能力集，以及 Schema 适配器／后端配置。任何 NULL、数值转换、排序、守卫或权限行为的语义变更，都要求新的兼容版本决策，并重新校验受影响制品。

新增可选能力不得重新解释已接受的语法。安全撤回可以立即关闭能力，并按需使缓存计划／制品／游标失效。不保证过期制品能够跨升级继续使用。服务端不得将未知语言版本或清单版本重新解释为版本 1。

解析器版本和上游后端行为是实现输入，不是语言规范权威。可以使用成熟解析器，但必须将其 AST 穷尽分类为闭合的带类型 IR；未知节点默认拒绝。SurrealDB SDK／服务端 3.3.0 是当前仓库固定的参考运行时，不表示它已经实现本 SQL 草案。

**N058.** SQL 兼容性、原生 SurrealQL 兼容性、PostgreSQL 线协议兼容性和具名客户端兼容性必须分别报告。P1 文档必须规定协议版本、认证／TLS、会话、Parse/Bind/Execute/Sync/portal 行为、类型编解码器／OID、元数据视图、错误、取消及事务语义。本草案不授予上述任何能力。

R1/W1/M1 的强制 CAS、无交互式事务及受限目录等限制，是可观察的兼容性差异。ORM 若依赖尚未提供的功能，必须明确失败或使用经过显式验证的适配器；服务不得丢弃语句后伪称执行成功。

## 23. 符合性证据与发布要求

**N059.** 能力资格验证必须冻结源码／构建／编译器／解析器／后端／存储配置、夹具 Schema／策略／数据、能力限制，以及完整的带类型预期／实际结果。负例必须验证在执行前拒绝；故障案例必须保留未知或失败证据。

必需证据包括附录 B 的语义案例及[验收映射](../../specs/004-surrealdb-rust-ai-baas/mensoria-sql-design-review.md)中的 SQL-A01–A16。差分检查仅针对共同 SQL 子集使用固定版本的参考数据库，并先记录有意保留的差异。有 ORDER BY 时比较完整有序序列，否则比较带类型多重集合。必须保留重复项、NULL 标签和精度。浮点／ANN 模式要求声明误差／质量指标，不得静默认为满足精确案例。

**N060.** 文档检查、本地解析器／运行时测试、CI、驱动资格验证、真实客户验收及生产资格验证，必须独立记录。本文件、语法、合成案例集或静态链接检查通过的存在，都不能启用任何 SQL 档位。

## 24. 参考资料

参考资料是说明性技术输入；以上带编号的规范性规则定义 Mensoria 的选择。核对日期为 2026-10-29。未复制受专有版权保护的 ISO 标准正文，也未声称已审阅该正文。

- [PostgreSQL 18 词法结构](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)：实际词法参考；Mensoria 有意收窄标识符和字面值语法。
- [PostgreSQL 18 值表达式](https://www.postgresql.org/docs/18/sql-expressions.html)：表达式存在超出语法解析的上下文规则；Mensoria 自行定义闭合子集。
- [PostgreSQL 18 比较](https://www.postgresql.org/docs/18/functions-comparison.html)：涉及 NULL 的比较背景。
- [PostgreSQL 18 SELECT](https://www.postgresql.org/docs/18/sql-select.html)：关系子句参考，不声明支持其完整语法。
- [PostgreSQL 18 聚合函数](https://www.postgresql.org/docs/18/functions-aggregate.html)：聚合类型和空输入参考；Mensoria 的十进制结果小数位数和舍入规则是明确的自身选择。
- [PostgreSQL 18 WITH 查询](https://www.postgresql.org/docs/18/queries-with.html)：CTE 背景；Mensoria 排除递归和数据修改。
- [PostgreSQL 18 错误码](https://www.postgresql.org/docs/18/errcodes-appendix.html)：五字符类别参考；Mensoria 错误码及重试行为仍是独立契约。
- [PostgreSQL 18 协议概览](https://www.postgresql.org/docs/18/protocol-overview.html)：驱动／会话协议需要单独契约。
- [SurrealDB NONE 与 NULL](https://surrealdb.com/docs/reference/query-language/language-primitives/data-types/none-and-null)：原生缺失与 null 的区别；不自动等同于 SQL。
- [SurrealDB 事务](https://surrealdb.com/docs/learn/querying/concepts-and-guides/transactions)：原生执行是实现输入，需要在固定版本上完成资格验证。
- [sqlparser-rs 文档](https://docs.rs/crate/sqlparser/latest)：候选语法解析器；语义检查仍由 Mensoria 负责。

## 附录 A. 闭合 EBNF 语法

本附录是规范性语法，受第 2–23 节档位／类型／授权约束限定，不表示解析器已经实现。`::=` 定义产生式；`|` 表示选择；`[ ... ]` 表示可选；`{ ... }` 表示重复零次或多次；带引号字符串为终结符；`? ... ?` 表示第 4 节定义的词法扫描规则。词法单元之间可以出现空白／注释。关键字终结符不区分大小写匹配。词法采用最长匹配；<=/>=/<>/!= 均为单个运算符。

语法包含已规定的可选能力，出现在语法中不表示已启用。规范正文的上下文限制优先于“语法上能够构造”这一事实。不得通过语法恢复机制接受未知 AST 形式。

```ebnf
statement ::= (select_query | insert_statement | update_statement | delete_statement | ddl_statement | explain_statement) [";"] ;

select_query ::= [with_clause] select_chain [order_by_clause] [row_cap] ;
with_clause ::= "WITH" cte_definition {"," cte_definition} ;
cte_definition ::= identifier "AS" "(" select_query ")" ;
select_chain ::= select_core {"UNION" "ALL" select_core} ;
select_core ::= "SELECT" [set_quantifier] projection "FROM" from_clause [where_clause] [group_by_clause] [having_clause] ;
set_quantifier ::= "ALL" | "DISTINCT" ;
projection ::= "*" | identifier "." "*" | select_item {"," select_item} ;
select_item ::= expression ["AS" identifier] ;
from_clause ::= relation_reference [join_clause] ;
relation_reference ::= relation_name [["AS"] identifier] ;
relation_name ::= identifier ["." identifier] ;
join_clause ::= ["INNER" | "LEFT" ["OUTER"]] "JOIN" relation_reference "ON" expression ;
where_clause ::= "WHERE" expression ;
group_by_clause ::= "GROUP" "BY" column_reference {"," column_reference} ;
having_clause ::= "HAVING" expression ;
order_by_clause ::= "ORDER" "BY" order_key {"," order_key} ;
order_key ::= column_reference ["ASC" | "DESC"] ["NULLS" ("FIRST" | "LAST")] ;
row_cap ::= "LIMIT" integer_literal | "FETCH" "FIRST" integer_literal "ROWS" "ONLY" ;

expression ::= or_expression ;
or_expression ::= and_expression {"OR" and_expression} ;
and_expression ::= not_expression {"AND" not_expression} ;
not_expression ::= ["NOT"] predicate ;
predicate ::= "EXISTS" "(" select_query ")" | scalar_expression [predicate_suffix] ;
predicate_suffix ::= comparison_operator scalar_expression | "IS" ["NOT"] "NULL" | ["NOT"] "IN" "(" write_value {"," write_value} ")" ;
comparison_operator ::= "=" | "<>" | "!=" | "<" | "<=" | ">" | ">=" ;
scalar_expression ::= additive_expression {"||" additive_expression} ;
additive_expression ::= multiplicative_expression {("+" | "-") multiplicative_expression} ;
multiplicative_expression ::= unary_expression {("*" | "/") unary_expression} ;
unary_expression ::= [sign] primary ;
primary ::= unsigned_literal | parameter | column_reference | "(" expression ")" | cast_expression | case_expression | coalesce_expression | text_function | aggregate_expression ;
cast_expression ::= "CAST" "(" expression "AS" data_type ")" ;
case_expression ::= "CASE" when_clause {when_clause} ["ELSE" expression] "END" ;
when_clause ::= "WHEN" expression "THEN" expression ;
coalesce_expression ::= "COALESCE" "(" expression "," expression {"," expression} ")" ;
text_function ::= ("CHAR_LENGTH" | "OCTET_LENGTH") "(" expression ")" ;
aggregate_expression ::= "COUNT" "(" ("*" | expression) ")" | ("SUM" | "AVG" | "MIN" | "MAX") "(" expression ")" ;
column_reference ::= identifier ["." identifier] ;

insert_statement ::= "INSERT" "INTO" relation_name "(" column_list ")" "VALUES" value_tuple {"," value_tuple} [returning_clause] ;
column_list ::= identifier {"," identifier} ;
value_tuple ::= "(" write_value {"," write_value} ")" ;
write_value ::= literal | parameter | "CAST" "(" write_value "AS" data_type ")" ;
update_statement ::= "UPDATE" relation_name "SET" assignment {"," assignment} where_clause [returning_clause] ;
assignment ::= identifier "=" write_value ;
delete_statement ::= "DELETE" "FROM" relation_name where_clause [returning_clause] ;
returning_clause ::= "RETURNING" returning_item {"," returning_item} ;
returning_item ::= identifier ["AS" identifier] ;

explain_statement ::= "EXPLAIN" select_query ;
ddl_statement ::= create_table | add_column | create_index | drop_index | drop_table ;
create_table ::= "CREATE" "TABLE" relation_name "(" column_definition {"," column_definition} ")" ;
column_definition ::= identifier data_type [primary_key_clause | not_null_clause] [default_clause] ;
primary_key_clause ::= "PRIMARY" "KEY" ;
not_null_clause ::= "NOT" "NULL" ;
default_clause ::= "DEFAULT" default_value ;
default_value ::= literal | "CAST" "(" default_value "AS" data_type ")" ;
add_column ::= "ALTER" "TABLE" relation_name "ADD" "COLUMN" column_definition ;
create_index ::= "CREATE" "INDEX" identifier "ON" relation_name "(" column_list ")" ;
drop_index ::= "DROP" "INDEX" relation_name ;
drop_table ::= "DROP" "TABLE" relation_name ;

data_type ::= "BOOLEAN" | "BIGINT" | "TEXT" | "UUID" | "NUMERIC" "(" integer_literal "," integer_literal ")" | "DOUBLE" "PRECISION" | "TIMESTAMP" "WITH" "TIME" "ZONE" ;
literal ::= [sign] numeric_literal | string_literal | "TRUE" | "FALSE" | "NULL" ;
unsigned_literal ::= numeric_literal | string_literal | "TRUE" | "FALSE" | "NULL" ;
numeric_literal ::= integer_literal | decimal_literal ;
sign ::= "+" | "-" ;
identifier ::= bare_identifier | quoted_identifier ;
bare_identifier ::= ? ASCII identifier scanner, section 4.1; excludes reserved keywords ? ;
quoted_identifier ::= ? Double-quoted identifier scanner, section 4.1 ? ;
integer_literal ::= ? One or more ASCII digits, section 4.2 ? ;
decimal_literal ::= ? ASCII digits then period then ASCII digits, section 4.2 ? ;
string_literal ::= ? Single-quoted UTF-8 string with doubled apostrophes, section 4.2 ? ;
parameter ::= ? Dollar sign and positive decimal index without leading zero, section 4.2 ? ;
```

附加的上下文语法限制：

- DDL 仅由迁移预览接纳，EXPLAIN 仅由计划路径接纳，DML 仅在 W1 下接纳；普通 SQL 执行不得因为 `statement` 能解析 DDL 就接纳 DDL。
- 关系名称可选的第一部分是 Schema；列引用的第一部分是当前有效关系限定名。语义绑定拒绝不支持的 Schema。
- R1 允许带正负号的数值字面值，但对列／参数／CAST 使用一元符号要求 `expr.numeric_arithmetic`；二元算术／拼接要求各自能力。本语法不包含嵌套一元符号。
- IN 列表项是字面值／参数或对它们的 CAST，不能是列表达式或查询。
- W1 的 where_clause 进一步受第 12.3 节已证明的合取守卫形状限制。M1 ADD COLUMN 不能声明第二个主键或平台列。
- 本语法不允许客户端提供任意函数名：上述已启用的具名结构构成闭合集合。未来扩展语法必须经过新的已登记语法修订。

## 附录 B. 带预期结果的符合性案例集

下列夹具和预期结果是规范性语言示例，不是已经执行的 SQL 验收。SQL 类型是每个预期结果的一部分；表中的数字表示精确逻辑值，不表示经 JSON binary64 转换后的数字。每个 SELECT 都显式使用 FROM，包括常量表达式示例。

### B.1 夹具 S：可见逻辑数据

对主体 A，除明确标为隐藏的行外，所有列和行均可读。实际测试必须通过受控夹具权限创建这些表，表不会因为出现在文档中就存在。

`public.notes`：id TEXT NOT NULL、revision BIGINT NOT NULL、title TEXT NOT NULL、category TEXT 可空、score BIGINT 可空。

| id | revision | title | category | score |
| --- | --- | --- | --- | --- |
| n1 | 1 | Alpha | a | 10 |
| n2 | 1 | Beta | a | 原生缺失 → SQL NULL |
| n3 | 1 | Gamma | SQL NULL | 20 |
| n4 | 1 | Delta | a | 10 |
| n5 | 1 | Epsilon | SQL NULL | SQL NULL |
| n_hidden | 1 | Hidden | secret | 999；该行对 A 不可见 |

`public.labels`：id TEXT NOT NULL、revision BIGINT NOT NULL、code TEXT NOT NULL、label TEXT NOT NULL。

| id | revision | code | label |
| --- | --- | --- | --- |
| l1 | 1 | a | Primary |
| l2 | 1 | a | Duplicate |
| l_hidden | 1 | secret | Hidden；该行对 A 不可见 |

`public.empty_notes` 与 notes 具有相同列且没有行。除非明确描述连续／并发场景，否则每个修改示例都从全新夹具开始。夹具 H 与上述数据相同，但拒绝主体 A 访问 score，仅用于拒绝案例。labels 中 code 重复是有意设计，不要求唯一约束。

### B.2 R1 值、NULL 与排序

**C01 — R1，缺失与 null 的等价映射。**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

预期按顺序返回 TEXT 行：`[n2]`、`[n5]`。隐藏行绝不进入求值过程。

**C02 — R1，普通 NULL 相等比较。**

```sql
SELECT id FROM public.notes WHERE score = NULL ORDER BY id;
```

预期为带类型空结果。`NULL = NULL` 同样得到 UNKNOWN，不是 TRUE。

**C03 — R1，包含 NULL 的 NOT IN。**

```sql
SELECT id FROM public.notes WHERE score NOT IN (10, NULL) ORDER BY id;
```

预期空结果：score=10 经 NOT 后为 FALSE；score=20 和 NULL 产生 UNKNOWN。

**C04 — R1，绑定文本始终是数据。**

```sql
SELECT id FROM public.notes WHERE title = $1 ORDER BY id;
```

TEXT `$1 = "x'; DELETE FROM public.notes; --"` 时，预期空行集且不发生修改。参数绝不重新解析为 SQL。

**C05 — R1 + read.nullable_order，显式 NULL 排位。**

```sql
SELECT id, score FROM public.notes
ORDER BY score DESC NULLS LAST, id ASC LIMIT 4;
```

预期 `(TEXT, 可空 BIGINT)` 行为：`[n3,20]`、`[n1,10]`、`[n4,10]`、`[n2,NULL]`。未启用可空排序能力时，预期在执行前返回 SQL_FEATURE_UNSUPPORTED。

**C06 — R1，重复标签保留为独立列。**

```sql
SELECT id AS x, title AS x FROM public.notes WHERE id = 'n1';
```

预期列为 `x TEXT`、`x TEXT`，有一行按列顺序排列的结果 `[n1,Alpha]`。为该查询添加 `ORDER BY x` 必须产生 SQL_AMBIGUOUS_REFERENCE。

### B.3 R2 重复项、JOIN 与聚合

**C07 — R2，DISTINCT 保留一个 NULL 组。**

```sql
SELECT DISTINCT category FROM public.notes ORDER BY category NULLS LAST;
```

要求 read.nullable_order。预期可空 TEXT 行为 `[a]`、`[NULL]`。

**C08 — R2，LEFT JOIN 保留重数及未匹配行。**

```sql
SELECT n.id, l.label FROM public.notes AS n
LEFT JOIN public.labels AS l ON n.category = l.code
ORDER BY n.id, l.label NULLS LAST;
```

由于 l.label 变为可空，要求 read.nullable_order。预期 `(TEXT, 可空 TEXT)` 行为：`[n1,Duplicate]`、`[n1,Primary]`、`[n2,Duplicate]`、`[n2,Primary]`、`[n3,NULL]`、`[n4,Duplicate]`、`[n4,Primary]`、`[n5,NULL]`。隐藏行不参与计算。

**C09 — R2，精确聚合类型与 NULL 输入。**

```sql
SELECT COUNT(*) AS rows_n, COUNT(score) AS values_n,
       SUM(score) AS total, AVG(score) AS mean
FROM public.notes;
```

预期一行：BIGINT 5、BIGINT 3、NUMERIC(38,0) `40`、NUMERIC(38,6) `13.333333`。

**C10 — R2，将 NULL 类别归为同组。**

```sql
SELECT category, COUNT(*) AS n, SUM(score) AS total
FROM public.notes GROUP BY category ORDER BY category NULLS LAST;
```

要求 read.nullable_order。预期行为 `[a,3,20]`、`[NULL,2,20]`；n 为 BIGINT，total 为 NUMERIC(38,0)，category 为可空 TEXT。

**C11 — R2，空输入聚合与空分组的区别。**

```sql
SELECT COUNT(*) AS n, SUM(score) AS total FROM public.empty_notes;
```

预期一行 `[BIGINT 0, NUMERIC(38,0) NULL]`。增加 `GROUP BY category` 且不投影 category 后，结果为零行，而不是一个计数为零的分组。

**C12 — R2 + expr.numeric_arithmetic，按条件求值。**

```sql
SELECT CASE WHEN score = 0 THEN CAST(0 AS NUMERIC(38,6))
            ELSE 10 / score END AS ratio
FROM public.notes WHERE id = 'n1';
```

预期 NUMERIC(38,6) `1.000000`。在 n1.score=0 的专门夹具中，预期 `0.000000`，不出现实际求值的除零错误。若 score=0 行位于聚合参数中，仍遵循先聚合后投影规则。

**C13 — R2，COALESCE 公共类型。**

```sql
SELECT id, COALESCE(score, 0) AS score_value
FROM public.notes WHERE id = 'n2';
```

预期 `[TEXT n2, BIGINT 0]`。没有上下文类型的 `COALESCE(NULL,NULL)` 返回 SQL_TYPE_ERROR。

### B.4 已规定的可选关系能力

**C14 — R2 + read.cte，非递归派生关系。**

```sql
WITH published AS (
    SELECT id, score FROM public.notes WHERE score >= 10
)
SELECT id FROM published ORDER BY id;
```

预期 `[n1]`、`[n3]`、`[n4]`。递归／自引用返回 SQL_FEATURE_UNSUPPORTED 或经过敏感信息清理的引用错误，不执行后端查询。

**C15 — R2 + read.exists，已授权的非关联存在性判断。**

```sql
SELECT id FROM public.notes
WHERE EXISTS (SELECT 1 FROM public.labels WHERE code = 'secret')
ORDER BY id;
```

对 A 预期空行集：唯一匹配标签不可见。将 `'secret'` 改为 `'a'` 后，结果为 n1–n5。

**C16 — R2 + read.union_all，多重集合拼接。**

```sql
SELECT id FROM public.notes WHERE id = 'n1'
UNION ALL
SELECT id FROM public.notes WHERE id = 'n1'
ORDER BY id;
```

预期两行相同 TEXT 结果 `[n1]`、`[n1]`；不得推断为 DISTINCT。

### B.5 W1、M1、类型与拒绝

**C17 — W1，CAS 成功。**

```sql
UPDATE public.notes SET title = $1
WHERE id = $2 AND revision = $3
RETURNING id, title, revision;
```

TEXT `$1=Reviewed`、TEXT `$2=n1`、BIGINT `$3=1` 时，预期 affected_rows 为 `1`，结果行为 `[n1,Reviewed,2]`。该更新确认完成后，另行提交预期修订号仍为 1 的命令，返回 affected_rows `0`。以同一原始键重放时关联首次操作，不再次增加修订号。

**C18 — W1，拒绝不安全守卫。**

```sql
UPDATE public.notes SET title = 'Bad'
WHERE id = 'n1' OR revision = 1;
```

预期在后端修改前返回 SQL_WRITE_PRECONDITION_REQUIRED。完全移除 WHERE 也不得执行，此时语法校验失败。禁止 `revision=revision` 及修改 revision。

**C19 — W1，两个条目的原子断言失败。**

将两个采用 C17 形状的独立制品作为一个请求提交：条目 1 指向 n1、修订号 1；条目 2 指向 n3、修订号 99；两者均设置 require_affected_rows=1。预期确认返回 SQL_PRECONDITION_FAILED，n1/n3 均不变。若丢失的是提交回复，则必须核对原始键，不得称为已经确认回滚。

**C20 — M1，仅生成 Schema 提案。**

```sql
CREATE TABLE public.review_notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT
);
```

预期在预览中生成迁移提案；实际维护／验证／发布完成之前，该表不可查询。将该语句提交到普通 SQL 执行路径时，必须按不支持的执行类别拒绝。

**C21 — R1，BIGINT 范围与显式类型。**

```sql
SELECT CAST($1 AS BIGINT) AS v FROM public.notes WHERE id = 'n1';
```

TEXT `$1=-9223372036854775808` 得到精确 BIGINT 最小值。TEXT `$1=9223372036854775808` 返回 SQL_VALUE_OUT_OF_RANGE。TEXT `$1=12x` 返回 SQL_INVALID_TEXT_VALUE。

**C22 — R2，NUMERIC 转换不得静默舍入。**

```sql
SELECT CAST($1 AS NUMERIC(5,2)) AS v
FROM public.notes WHERE id = 'n1';
```

TEXT `$1=12.340` 得到 NUMERIC(5,2) `12.34`；`$1=12.345` 返回 SQL_VALUE_OUT_OF_RANGE。`$1=1000` 也因超过三位整数容量而溢出。

**C23 — R1，权限掩码列不等于 NULL。**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

在夹具 H 下，预期 SQL_REFERENCE_DENIED。不得将被掩码的 score 解释为缺失／null，从而返回全部五行可见行。

**C24 — R1，分页与失效。**

使用独立的 120 行夹具，id 为唯一且有序的 TEXT；以 page_size 50 执行 `SELECT id FROM public.page_notes ORDER BY id LIMIT 120`。预期分别得到 50/50/20 行，result_complete=false/false/true。在第 2 页之前撤销会话或改变 Schema／环境代次：旧游标必须失败，且不发布新的行或游标。这是预期场景，不表示这里实际执行过分页。

**C25 — W1，原始键与回复丢失。**

在 C17 实际提交后注入回复丢失，按运行时资格验证规定重启自行管理的 API／数据库，然后检查原操作。预期只有一次已提交更新，修订号为 2；或者在权威核对完成之前明确保持未解决状态。不得再次修改或自动生成新键。运行时资格验证必须区分提交前与提交后丢失，并保留两类收据。

**C26 — R1，目录与不执行查询的计划。**

```sql
EXPLAIN SELECT id FROM public.notes WHERE id = $1;
```

声明 TEXT 参数类型。预期返回经过敏感信息清理的逻辑 Scan/Filter/Project 信息及所需能力；不扫描业务数据，不包含行值、原生物理名称、隐藏基数，也不授予权限。

**C27 — R2 + type.numeric，聚合结果小数位数。**

独立表 `public.decimals` 包含 id TEXT、value NUMERIC(6,2)，行值为 `[d1,1.00]`、`[d2,2.00]`、`[d3,NULL]`，且具备经资格验证的映射。`SELECT SUM(value) AS s, AVG(value) AS a FROM public.decimals` 得到 NUMERIC(38,2) `3.00`、NUMERIC(38,6) `1.500000`。

**C28 — 已关闭／暂缓语法。**

```sql
SELECT http::get('https://example.invalid') FROM public.notes;
```

预期在执行前因语法或能力限制被拒绝，不发出外部请求。解析器识别出原生调用，不允许回退到原生执行。不支持的图箭头、UDF、交互式事务和未登记扩展函数遵循相同规则。

## 附录 C. 明确排除的语法

此列表是规范性拒绝范围，不构成未来实现这些能力的承诺。

| 类别 | 本草案排除项 |
| --- | --- |
| 词法便利语法 | Unicode／含空格标识符、美元引用字符串、转义字符串前缀、指数 SQL 字面值、类型名称别名 |
| 查询形状 | 无 FROM 的 SELECT、OFFSET、标量／关联／IN 子查询、派生表语法、SELECT INTO、TABLE 简写 |
| 连接 | CROSS/NATURAL/RIGHT/FULL/LATERAL、USING、逗号连接、非等值连接、单个查询块超过两个关系引用 |
| 分组／窗口 | GROUP BY 表达式／序号、grouping sets/rollup/cube、聚合 DISTINCT/FILTER/ORDER BY、窗口函数 |
| 集合表达式 | UNION DISTINCT、INTERSECT、EXCEPT、分支各自的上限／排序 |
| 谓词／函数 | BETWEEN、LIKE、正则、IS DISTINCT FROM、IS TRUE/FALSE/UNKNOWN、一般 UDF 调用、易变函数 |
| DML | 一般集合 UPDATE/DELETE、盲覆盖／upsert、INSERT SELECT、MERGE、生成键、表达式赋值、RETURNING * |
| 事务 | SQL BEGIN/COMMIT/ROLLBACK、保存点、客户端保持的开放事务、SET TRANSACTION、分布式事务 |
| DDL／安全 | 创建 Schema／角色／用户／数据库、GRANT/REVOKE、过程／触发器、ALTER TYPE/RENAME/DROP COLUMN、TRUNCATE、任意原生 Schema |
| 约束 | 一般 UNIQUE/FOREIGN KEY/CHECK、级联或延迟约束、未经资格验证的原生索引强制约束 |
| 原生／外部 | USE、命名空间切换、原生记录 ID／箭头遍历、原生函数命名空间、文件／网络访问、COPY／导入／导出、实时查询语法 |
| 扩展 | 在独立扩展规范完成登记并具有证据前，所有可执行 JSON／图／全文／向量语法 |
| 驱动声明 | 完整 pg_catalog/INFORMATION_SCHEMA、PostgreSQL 会话／portal／OID、通用 ORM／BI 兼容性 |

对于已识别但被排除的 AST，可以返回 SQL_FEATURE_UNSUPPORTED；对于语法范围外的文本，可以返回 SQL_SYNTAX_ERROR。两者都必须在后端执行之前拒绝。错误分类不得暴露受保护资源是否存在。

## 附录 D. 审查清单与修订历史

### D.1 草案完整性标准

- 每个语法非终结符都有定义；每个终结符／词法类别都有规则。
- 每个已启用档位都具有最低能力集、语义规则、适用案例集及实现门槛。
- 每个已规定可选能力都具有依赖、支持语法、类型／NULL 行为及未启用时的拒绝规则。
- 每个顶层示例都标明所需档位／能力或预期拒绝结果。
- 各权威文档对类型解析、NULL、多重集合、连接、聚合、守卫、原始键结果及发布规则的规定一致。
- 文档、本地运行时、CI、客户端及业务／生产证据保持独立。

### D.2 修订版 0.1.0-draft.1

首个完整规范版。将此前架构提案展开为语言标准草案，保留现有架构／传输／操作职责归属。明确 NUMERIC 为 R2 必需能力，定义精确聚合结果的小数位数和 AVG 的中点取偶数舍入，规定闭合语法及 28 个带预期结果的案例。这里不替代任何既有 SQL 实现或已发布标准，因为尚未建立此类资格证明。
