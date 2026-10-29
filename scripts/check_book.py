#!/usr/bin/env python3
"""Check a book edition's provenance, normative content, navigation and parity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FENCES = re.compile(r"^```[^\n]*\n.*?^```", re.M | re.S)
LINKS = re.compile(r"\[[^\]]+\]\(([^\s)]+)\)")


def normalize(text):
    text = re.sub(r'<a id="[^"]+"></a>\n\n', "", text)
    text = re.sub(r"^#{1,6} ", "", text, flags=re.M)
    text = re.sub(r"(\[[^\]]+\])\([^)]+\)", r"\1", text)
    return text.strip()


def sections(text):
    pattern = r"^## (?:Appendix |附录 )?([A-D]|\d+)\. .*?(?=^## |\Z)"
    return {m[1]: m.group() for m in re.finditer(pattern, text, re.M | re.S)}


def markdown_anchors(text):
    anchors = set(re.findall(r'<a id="([^"]+)"', text))
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.M):
        anchors.add(re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-"))
    return anchors


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append(attrs[name])


def check_html():
    site = ROOT / "site"
    pages = {}
    for path in site.rglob("*.html"):
        parser = Page()
        parser.feed(path.read_text())
        pages[path.resolve()] = parser
    count = 0
    for path, page in pages.items():
        for raw in page.links:
            url = urlsplit(raw)
            if url.scheme or url.netloc or not raw or raw.startswith("/"):
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Broken built link: {path.relative_to(ROOT)} -> {raw}"
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, f"Missing built anchor: {path.name} -> {raw}"
            count += 1
    for lang in ("en", "zh-CN"):
        for path in (site / lang).glob("*.html"):
            sibling = site / ("zh-CN" if lang == "en" else "en") / path.name
            assert sibling.is_file(), f"Missing language switch target: {sibling}"
    return {"html_pages": len(pages), "local_html_links_and_assets": count}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    for item in manifest["files"]:
        path = ROOT / item["snapshot"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], f"Changed source snapshot: {path}"
    layout = json.loads((ROOT / "book/structure.json").read_text())["chapters"]
    code = {}
    pages = {}
    for lang, snapshot in [("en", "137-mensoria-sql-standard-draft.md"), ("zh-CN", "137-mensoria-sql-standard-draft.zh-CN.md")]:
        source = (ROOT / "sources/archstudio" / snapshot).read_text()
        original = sections(source)
        assert len(original) == 28
        manuscript = ROOT / "book" / lang / "src"
        assembled = ""
        for chapter in layout[lang]:
            text = (manuscript / chapter["file"]).read_text()
            assert normalize(text) == normalize(original[chapter["id"]]), f"Normative content drift: {lang}/{chapter['file']}"
            assembled += text + "\n"
        assert re.findall(r"^\*\*(N\d{3})\.\*\*", assembled, re.M) == [f"N{i:03}" for i in range(1, 61)]
        assert re.findall(r"^\*\*(C\d{2}) —", assembled, re.M) == [f"C{i:02}" for i in range(1, 29)]
        registry = (manuscript / "02-profiles.md").read_text().split("## 2.2", 1)[1]
        features = re.findall(r"^\| `([a-z_]+\.[a-z_]+)` \|", registry, re.M)
        assert len(features) == len(set(features)) == 32
        code[lang] = FENCES.findall(assembled)
        summary = (manuscript / "SUMMARY.md").read_text()
        listed = LINKS.findall(summary)
        files = {p.name for p in manuscript.glob("*.md")} - {"SUMMARY.md"}
        assert set(listed) == files and len(listed) == len(files), f"SUMMARY coverage: {lang}"
        pages[lang] = len(files)
        for path in manuscript.glob("*.md"):
            text = path.read_text()
            assert len(re.findall(r"^```", text, re.M)) % 2 == 0, f"Unbalanced fences: {path}"
            assert not re.search(r"@@|NEEDS CLARIFICATION|\[TBD\]|\[TODO\]", text), path
            assert all(line == line.rstrip() for line in text.splitlines()), f"Trailing whitespace: {path}"
            assert not text.endswith("\n\n"), f"Blank final line: {path}"
            without_code = FENCES.sub("", text)
            for raw in LINKS.findall(without_code):
                if urlsplit(raw).scheme:
                    continue
                name, _, fragment = raw.partition("#")
                target = (path.parent / name).resolve() if name else path.resolve()
                assert target.is_file(), f"Broken manuscript link: {path.name} -> {raw}"
                if fragment:
                    assert unquote(fragment) in markdown_anchors(target.read_text()), f"Missing manuscript anchor: {raw}"
    assert code["en"] == code["zh-CN"], "SQL/EBNF bilingual drift"
    grammar = next(x for x in code["en"] if x.startswith("```ebnf"))
    definitions = re.findall(r"^([a-z_]+)\s*::=", grammar, re.M)
    cleaned = re.sub(r'"[^"]*"|\?[^?]*\?', "", grammar)
    refs = {word for line in cleaned.splitlines() if "::=" in line for word in re.findall(r"\b[a-z_]+\b", line.split("::=", 1)[1])}
    assert len(definitions) == len(set(definitions)) == 71
    assert refs <= set(definitions)
    editorial_files = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md")) + [ROOT / "sources/README.md"]
    for path in editorial_files:
        text = path.read_text()
        assert all(line == line.rstrip() for line in text.splitlines()), f"Trailing whitespace: {path}"
        for raw in LINKS.findall(FENCES.sub("", text)):
            if urlsplit(raw).scheme:
                continue
            name, _, fragment = raw.partition("#")
            target = (path.parent / name).resolve() if name else path.resolve()
            assert target.is_file(), f"Broken editorial link: {path.name} -> {raw}"
            if fragment:
                assert unquote(fragment) in markdown_anchors(target.read_text()), f"Missing editorial anchor: {raw}"
    result = {"source_snapshots": len(manifest["files"]), "pages_per_language": pages, "normative_rules_per_language": 60, "features_per_language": 32, "worked_cases_per_language": 28, "identical_normative_code_blocks": len(code["en"]), "closed_grammar_productions": 71, "editorial_documents_checked": len(editorial_files)}
    if args.html:
        result.update(check_html())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
