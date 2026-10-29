# 附录 B. 带预期结果的符合性案例集

下列夹具和预期结果是规范性语言示例，不是已经执行的 SQL 验收。SQL 类型是每个预期结果的一部分；表中的数字表示精确逻辑值，不表示经 JSON binary64 转换后的数字。每个 SELECT 都显式使用 FROM，包括常量表达式示例。

## B.1 夹具 S：可见逻辑数据

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

## B.2 R1 值、NULL 与排序

<a id="c01"></a>

**C01 — R1，缺失与 null 的等价映射。**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

预期按顺序返回 TEXT 行：`[n2]`、`[n5]`。隐藏行绝不进入求值过程。

<a id="c02"></a>

**C02 — R1，普通 NULL 相等比较。**

```sql
SELECT id FROM public.notes WHERE score = NULL ORDER BY id;
```

预期为带类型空结果。`NULL = NULL` 同样得到 UNKNOWN，不是 TRUE。

<a id="c03"></a>

**C03 — R1，包含 NULL 的 NOT IN。**

```sql
SELECT id FROM public.notes WHERE score NOT IN (10, NULL) ORDER BY id;
```

预期空结果：score=10 经 NOT 后为 FALSE；score=20 和 NULL 产生 UNKNOWN。

<a id="c04"></a>

**C04 — R1，绑定文本始终是数据。**

```sql
SELECT id FROM public.notes WHERE title = $1 ORDER BY id;
```

TEXT `$1 = "x'; DELETE FROM public.notes; --"` 时，预期空行集且不发生修改。参数绝不重新解析为 SQL。

<a id="c05"></a>

**C05 — R1 + read.nullable_order，显式 NULL 排位。**

```sql
SELECT id, score FROM public.notes
ORDER BY score DESC NULLS LAST, id ASC LIMIT 4;
```

预期 `(TEXT, 可空 BIGINT)` 行为：`[n3,20]`、`[n1,10]`、`[n4,10]`、`[n2,NULL]`。未启用可空排序能力时，预期在执行前返回 SQL_FEATURE_UNSUPPORTED。

<a id="c06"></a>

**C06 — R1，重复标签保留为独立列。**

```sql
SELECT id AS x, title AS x FROM public.notes WHERE id = 'n1';
```

预期列为 `x TEXT`、`x TEXT`，有一行按列顺序排列的结果 `[n1,Alpha]`。为该查询添加 `ORDER BY x` 必须产生 SQL_AMBIGUOUS_REFERENCE。

## B.3 R2 重复项、JOIN 与聚合

<a id="c07"></a>

**C07 — R2，DISTINCT 保留一个 NULL 组。**

```sql
SELECT DISTINCT category FROM public.notes ORDER BY category NULLS LAST;
```

要求 read.nullable_order。预期可空 TEXT 行为 `[a]`、`[NULL]`。

<a id="c08"></a>

**C08 — R2，LEFT JOIN 保留重数及未匹配行。**

```sql
SELECT n.id, l.label FROM public.notes AS n
LEFT JOIN public.labels AS l ON n.category = l.code
ORDER BY n.id, l.label NULLS LAST;
```

由于 l.label 变为可空，要求 read.nullable_order。预期 `(TEXT, 可空 TEXT)` 行为：`[n1,Duplicate]`、`[n1,Primary]`、`[n2,Duplicate]`、`[n2,Primary]`、`[n3,NULL]`、`[n4,Duplicate]`、`[n4,Primary]`、`[n5,NULL]`。隐藏行不参与计算。

<a id="c09"></a>

**C09 — R2，精确聚合类型与 NULL 输入。**

```sql
SELECT COUNT(*) AS rows_n, COUNT(score) AS values_n,
       SUM(score) AS total, AVG(score) AS mean
FROM public.notes;
```

预期一行：BIGINT 5、BIGINT 3、NUMERIC(38,0) `40`、NUMERIC(38,6) `13.333333`。

<a id="c10"></a>

**C10 — R2，将 NULL 类别归为同组。**

```sql
SELECT category, COUNT(*) AS n, SUM(score) AS total
FROM public.notes GROUP BY category ORDER BY category NULLS LAST;
```

要求 read.nullable_order。预期行为 `[a,3,20]`、`[NULL,2,20]`；n 为 BIGINT，total 为 NUMERIC(38,0)，category 为可空 TEXT。

<a id="c11"></a>

**C11 — R2，空输入聚合与空分组的区别。**

```sql
SELECT COUNT(*) AS n, SUM(score) AS total FROM public.empty_notes;
```

预期一行 `[BIGINT 0, NUMERIC(38,0) NULL]`。增加 `GROUP BY category` 且不投影 category 后，结果为零行，而不是一个计数为零的分组。

<a id="c12"></a>

**C12 — R2 + expr.numeric_arithmetic，按条件求值。**

```sql
SELECT CASE WHEN score = 0 THEN CAST(0 AS NUMERIC(38,6))
            ELSE 10 / score END AS ratio
FROM public.notes WHERE id = 'n1';
```

预期 NUMERIC(38,6) `1.000000`。在 n1.score=0 的专门夹具中，预期 `0.000000`，不出现实际求值的除零错误。若 score=0 行位于聚合参数中，仍遵循先聚合后投影规则。

<a id="c13"></a>

**C13 — R2，COALESCE 公共类型。**

```sql
SELECT id, COALESCE(score, 0) AS score_value
FROM public.notes WHERE id = 'n2';
```

预期 `[TEXT n2, BIGINT 0]`。没有上下文类型的 `COALESCE(NULL,NULL)` 返回 SQL_TYPE_ERROR。

## B.4 已规定的可选关系能力

<a id="c14"></a>

**C14 — R2 + read.cte，非递归派生关系。**

```sql
WITH published AS (
    SELECT id, score FROM public.notes WHERE score >= 10
)
SELECT id FROM published ORDER BY id;
```

预期 `[n1]`、`[n3]`、`[n4]`。递归／自引用返回 SQL_FEATURE_UNSUPPORTED 或经过敏感信息清理的引用错误，不执行后端查询。

<a id="c15"></a>

**C15 — R2 + read.exists，已授权的非关联存在性判断。**

```sql
SELECT id FROM public.notes
WHERE EXISTS (SELECT 1 FROM public.labels WHERE code = 'secret')
ORDER BY id;
```

对 A 预期空行集：唯一匹配标签不可见。将 `'secret'` 改为 `'a'` 后，结果为 n1–n5。

<a id="c16"></a>

**C16 — R2 + read.union_all，多重集合拼接。**

```sql
SELECT id FROM public.notes WHERE id = 'n1'
UNION ALL
SELECT id FROM public.notes WHERE id = 'n1'
ORDER BY id;
```

预期两行相同 TEXT 结果 `[n1]`、`[n1]`；不得推断为 DISTINCT。

## B.5 W1、M1、类型与拒绝

<a id="c17"></a>

**C17 — W1，CAS 成功。**

```sql
UPDATE public.notes SET title = $1
WHERE id = $2 AND revision = $3
RETURNING id, title, revision;
```

TEXT `$1=Reviewed`、TEXT `$2=n1`、BIGINT `$3=1` 时，预期 affected_rows 为 `1`，结果行为 `[n1,Reviewed,2]`。该更新确认完成后，另行提交预期修订号仍为 1 的命令，返回 affected_rows `0`。以同一原始键重放时关联首次操作，不再次增加修订号。

<a id="c18"></a>

**C18 — W1，拒绝不安全守卫。**

```sql
UPDATE public.notes SET title = 'Bad'
WHERE id = 'n1' OR revision = 1;
```

预期在后端修改前返回 SQL_WRITE_PRECONDITION_REQUIRED。完全移除 WHERE 也不得执行，此时语法校验失败。禁止 `revision=revision` 及修改 revision。

<a id="c19"></a>

**C19 — W1，两个条目的原子断言失败。**

将两个采用 C17 形状的独立制品作为一个请求提交：条目 1 指向 n1、修订号 1；条目 2 指向 n3、修订号 99；两者均设置 require_affected_rows=1。预期确认返回 SQL_PRECONDITION_FAILED，n1/n3 均不变。若丢失的是提交回复，则必须核对原始键，不得称为已经确认回滚。

<a id="c20"></a>

**C20 — M1，仅生成 Schema 提案。**

```sql
CREATE TABLE public.review_notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT
);
```

预期在预览中生成迁移提案；实际维护／验证／发布完成之前，该表不可查询。将该语句提交到普通 SQL 执行路径时，必须按不支持的执行类别拒绝。

<a id="c21"></a>

**C21 — R1，BIGINT 范围与显式类型。**

```sql
SELECT CAST($1 AS BIGINT) AS v FROM public.notes WHERE id = 'n1';
```

TEXT `$1=-9223372036854775808` 得到精确 BIGINT 最小值。TEXT `$1=9223372036854775808` 返回 SQL_VALUE_OUT_OF_RANGE。TEXT `$1=12x` 返回 SQL_INVALID_TEXT_VALUE。

<a id="c22"></a>

**C22 — R2，NUMERIC 转换不得静默舍入。**

```sql
SELECT CAST($1 AS NUMERIC(5,2)) AS v
FROM public.notes WHERE id = 'n1';
```

TEXT `$1=12.340` 得到 NUMERIC(5,2) `12.34`；`$1=12.345` 返回 SQL_VALUE_OUT_OF_RANGE。`$1=1000` 也因超过三位整数容量而溢出。

<a id="c23"></a>

**C23 — R1，权限掩码列不等于 NULL。**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

在夹具 H 下，预期 SQL_REFERENCE_DENIED。不得将被掩码的 score 解释为缺失／null，从而返回全部五行可见行。

<a id="c24"></a>

**C24 — R1，分页与失效。**

使用独立的 120 行夹具，id 为唯一且有序的 TEXT；以 page_size 50 执行 `SELECT id FROM public.page_notes ORDER BY id LIMIT 120`。预期分别得到 50/50/20 行，result_complete=false/false/true。在第 2 页之前撤销会话或改变 Schema／环境代次：旧游标必须失败，且不发布新的行或游标。这是预期场景，不表示这里实际执行过分页。

<a id="c25"></a>

**C25 — W1，原始键与回复丢失。**

在 C17 实际提交后注入回复丢失，按运行时资格验证规定重启自行管理的 API／数据库，然后检查原操作。预期只有一次已提交更新，修订号为 2；或者在权威核对完成之前明确保持未解决状态。不得再次修改或自动生成新键。运行时资格验证必须区分提交前与提交后丢失，并保留两类收据。

<a id="c26"></a>

**C26 — R1，目录与不执行查询的计划。**

```sql
EXPLAIN SELECT id FROM public.notes WHERE id = $1;
```

声明 TEXT 参数类型。预期返回经过敏感信息清理的逻辑 Scan/Filter/Project 信息及所需能力；不扫描业务数据，不包含行值、原生物理名称、隐藏基数，也不授予权限。

<a id="c27"></a>

**C27 — R2 + type.numeric，聚合结果小数位数。**

独立表 `public.decimals` 包含 id TEXT、value NUMERIC(6,2)，行值为 `[d1,1.00]`、`[d2,2.00]`、`[d3,NULL]`，且具备经资格验证的映射。`SELECT SUM(value) AS s, AVG(value) AS a FROM public.decimals` 得到 NUMERIC(38,2) `3.00`、NUMERIC(38,6) `1.500000`。

<a id="c28"></a>

**C28 — 已关闭／暂缓语法。**

```sql
SELECT http::get('https://example.invalid') FROM public.notes;
```

预期在执行前因语法或能力限制被拒绝，不发出外部请求。解析器识别出原生调用，不允许回退到原生执行。不支持的图箭头、UDF、交互式事务和未登记扩展函数遵循相同规则。
