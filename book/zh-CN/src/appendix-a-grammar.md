# 附录 A. 闭合 EBNF 语法

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
