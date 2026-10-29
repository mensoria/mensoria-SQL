# Appendix A. Closed EBNF grammar

This appendix is normative syntax, qualified by the profile/type/authorization constraints in §§2–23. It is not a claim that a parser has been implemented. `::=` defines a production; `|` is alternation; `[ ... ]` is optional; `{ ... }` repeats zero or more times; quoted strings are terminals; `? ... ?` denotes a lexical scanner rule defined in §4. Whitespace/comments may occur between tokens. Keyword terminals are matched case-insensitively. Longest lexical token applies; <=/>=/<>/!= are single operators.

The grammar includes specified optional features; their presence does not enable them. A context restriction in the normative text takes precedence over a grammatically constructible expression. Unknown AST forms cannot be accepted through grammar recovery.

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

Additional contextual grammar restrictions:

- DDL is admitted only by migration preview, EXPLAIN only by the plan path, and DML only with W1; normal SQL execution never admits DDL simply because `statement` can parse it.
- A relation name's optional first component is a schema; a column reference's first component is its active relation qualifier. Semantic binding rejects unsupported schemas.
- R1 permits signed numeric literals but unary signs on columns/parameters/CAST require `expr.numeric_arithmetic`; binary arithmetic/concatenation require their feature. Nested unary signs are not part of this grammar.
- IN list entries are literals/parameters/CAST thereof. They cannot be column expressions or queries.
- W1 where_clause is further limited to the proven conjunctive guard shape in §12.3. M1 ADD COLUMN cannot declare a second primary key or platform column.
- There is no grammar for a client-supplied function name: the enabled named constructs above form a closed set. Future extension syntax requires a new registered grammar revision.
