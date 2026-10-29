# Mensoria SQL

**官方文档网站 · 草案 0.1.0-draft.1 · 语言版本 1**

[English](README.md) · [开始阅读](book/zh-CN/src/preface.md) · [完整目录](book/zh-CN/src/SUMMARY.md)

本仓库是 Mensoria SQL 官方文档网站的源码与 GitHub Pages 发布仓库，包含 **24 章规范正文、4 个规范附录、60 条规则、32 项能力、71 条 EBNF 产生式，以及 28 个带预期结果的案例**。每种语言另有前言、阅读路线、规则／能力／语句索引、术语表，以及明确标为说明性的工程参考。

本仓库发布中英文语言文档，在线阅读是主要入口，EPUB 和单页打印为附加格式。草案不证明 SQL 实现、PostgreSQL 协议／驱动兼容、运行时符合性或生产就绪。

## 官网地址

目标 GitHub Pages 地址：[mensoria.github.io/mensoria-SQL](https://mensoria.github.io/mensoria-SQL/)。首次发布需要在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。启用和上线核验见[发布说明](docs/site-publishing.md)。

## 阅读结构

1. **语言基础**：范围、档位、模型、词法、类型与表达式。
2. **关系查询**：SELECT、排序、连接、聚合与可选结构。
3. **修改与 Schema**：受守卫保护的 DML、事务、未知结果与迁移。
4. **执行契约**：目录、制品、传输结果、诊断、预算与授权。
5. **演进与证据**：扩展、兼容性、符合性和参考资料。

四个规范附录收录完整语法、案例集、排除语法和审查／修订记录。架构与传输工程参考在两版中均保留英文，并明确区分于规范正文。

## 构建与阅读

需要 Python **3.10+**。引导脚本从官方发行下载固定的 mdBook **0.5.4**，验证归档 SHA-256 后放入忽略目录 `.cache/tools/`，不全局安装。覆盖 macOS arm64/x86_64 和 Linux arm64/x86_64。

```sh
python3 scripts/bootstrap_mdbook.py
python3 scripts/check_book.py
python3 scripts/build.py
```

生成的双语入口为 `site/index.html`。每版独立提供目录、搜索、同章语言切换和单页打印视图。

另有 Pandoc **3.x** 时，可以生成两种语言的 EPUB：

```sh
python3 scripts/build.py --epub
```

电子书与本地构建报告位于 `dist/`，下载副本位于 `site/downloads/`。HTML 构建不依赖 Pandoc；仅构建 HTML 时不展示旧 EPUB 下载。构建器检查 EPUB 包结构和引用，不据此声明通过外部 EPUBCheck 或所有阅读器认证。

本地预览：

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

打开[本地书籍入口](http://127.0.0.1:8000/)。每版打印按钮可打开单页打印视图，再通过浏览器另存为 PDF。GitHub 工作流校验 PR，在 `main` 更新或手动运行主分支工作流后，将 `site/` 部署到 GitHub Pages；PR 不部署。网站发布与 SQL 实现资格验证分开记录。

## 维护

- 书稿：`book/en/src/` 与 `book/zh-CN/src/`。
- 目录和映射：各版 `SUMMARY.md`、`book/structure.json`。
- 来源：`sources/archstudio/` 和逐文件摘要清单。
- 生成输出：`site/`、`dist/`、`.cache/`，均不入库。

详见[编辑规则](CONTRIBUTING.md)、[来源说明](sources/README.md)、[修订历史](CHANGELOG.md)及[本地验证记录](docs/book-verification.md)。原始快照保留历史链接，独立阅读链接检查针对经过整理的书稿，而不是这些冻结输入。
