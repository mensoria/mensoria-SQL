# 7. 表达式、谓词与 NULL

## 7.1 布尔与比较语义

<a id="n018"></a>

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

<a id="n019"></a>

**N019.** 布尔求值顺序不构成对用户可见的短路保证。校验必须检查所有分支，包括不可达分支的资源、类型和副作用权限。CASE/COALESCE 的值求值遵循第 7.2 节，但不得因此忽略分支中的绑定错误。

## 7.2 CASE 与 COALESCE，R2

搜索式 `CASE WHEN condition THEN value ... [ELSE value] END` 返回第一个条件为 TRUE 的分支；省略 ELSE 时返回带类型 SQL NULL。所有结果分支解析为同一个公共类型。条件为 FALSE 或 UNKNOWN 时继续检查后续分支。简单 CASE 暂缓。

`COALESCE(a,b,...)` 至少需要两个具有公共结果类型的参数；返回第一个非 NULL 参数，若全部为 NULL 则返回带类型 NULL。全部参数都是无类型 NULL 时拒绝，除非显式转换提供公共类型。

<a id="n020"></a>

**N020.** 对标量表达式，未选中的 CASE 结果以及 COALESCE 已选中值之后的参数，不得引发运行时值错误。编译器仍必须绑定和授权其内容。分组聚合在 SELECT 的标量 CASE 之前计算，因此不能使用 CASE 屏蔽聚合错误。

## 7.3 可选算术与文本表达式

`expr.numeric_arithmetic` 为解析到相同数值域的操作数启用一元 +/- 和二元 +,-,*,/。一元符号传播 SQL NULL。二元运算符的已求值操作数中只要有 SQL NULL，就返回带类型 SQL NULL，包括带类型 NULL 除以零；除法运算符仅在两侧均非 NULL 时检查除数是否为零。但仍须求值各操作数表达式自身的错误，顺序不限，因此 NULL 加上一个单独求值就会失败的 CAST 仍是错误。CASE/COALESCE 保留其明确的惰性值分支语义。BIGINT +,-,* 返回 BIGINT 并检查溢出；BIGINT / BIGINT 返回 NUMERIC(38,6)，按恰好中点取偶数舍入。除以零报错。BIGINT/NUMERIC 混用时先按第 6 节精确解析；所有 NUMERIC 运算遵循下述规则。DOUBLE 仅与 DOUBLE 运算，返回有限 binary64，并拒绝非有限结果和除以零。

NUMERIC +,- 返回 NUMERIC(38,max(s1,s2))；乘法返回 NUMERIC(38,min(38,s1+s2))，但超过 38 位小数时，若需丢弃任何非零小数位，必须拒绝而非截断。NUMERIC 除法返回 NUMERIC(38,max(s1,s2,6))，仅在生成结果小数位数时按恰好中点取偶数舍入一次。所有运算均拒绝整数部分无法容纳的结果。算术精度和小数位数在执行前确定，不随行值变化。

`expr.text_basic` 启用 TEXT 拼接 `||`、`CHAR_LENGTH(TEXT) -> BIGINT` 和 `OCTET_LENGTH(TEXT) -> BIGINT`。拼接和这两个函数均传播 NULL。字符长度统计 Unicode 标量值，不统计字素簇；字节长度统计 UTF-8 字节。不进行标量到 TEXT 的隐式转换。LIKE、正则、LOWER/UPPER、区域化排序及用户函数均暂缓。

运算符优先级从高到低依次为：括号／CAST／函数／CASE；一元符号；*/；二元 +/-；||；比较／IN／IS NULL；NOT；AND；OR。二元算术与拼接左结合。比较不得连写：`1 < 2 < 3` 无效。
