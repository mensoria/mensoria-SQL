#!/usr/bin/env python3
"""Build the bilingual HTML book, and optionally an EPUB for each language."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True)


def mdbook_executable():
    local = ROOT / ".cache/tools/mdbook"
    executable = str(local) if local.is_file() else shutil.which("mdbook")
    if not executable:
        raise SystemExit("Run python3 scripts/bootstrap_mdbook.py first (or install mdbook 0.5.4).")
    version = subprocess.check_output([executable, "--version"], text=True).strip()
    if version != "mdbook v0.5.4":
        raise SystemExit(f"Expected mdbook v0.5.4; found {version}")
    return executable


def check_epub(path):
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        assert archive.read("mimetype") == b"application/epub+zip"
        assert archive.infolist()[0].filename == "mimetype" and archive.infolist()[0].compress_type == 0
        documents = {n: ET.fromstring(archive.read(n)) for n in names if n.endswith((".xhtml", ".html"))}
        ids = {n: {e.attrib["id"] for e in document.iter() if "id" in e.attrib} for n, document in documents.items()}
        for name, document in documents.items():
            for element in document.iter():
                for key in ("href", "src"):
                    if key not in element.attrib:
                        continue
                    url = urlsplit(element.attrib[key])
                    if url.scheme or url.netloc:
                        continue
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name
                    assert target in names, f"Broken EPUB target: {name} -> {element.attrib[key]}"
                    if url.fragment and target in ids:
                        assert unquote(url.fragment) in ids[target], f"Broken EPUB anchor: {element.attrib[key]}"
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        rootfile = container.find(".//{*}rootfile").attrib["full-path"]
        assert rootfile in names
        return len(documents)


def build_epub(lang):
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("EPUB output requires Pandoc 3.x; HTML does not. Install it or omit --epub.")
    version = subprocess.check_output([pandoc, "--version"], text=True).splitlines()[0]
    if not version.startswith("pandoc 3."):
        raise SystemExit(f"Expected Pandoc 3.x; found {version}")
    source = ROOT / "book" / lang / "src"
    summary = (source / "SUMMARY.md").read_text()
    files = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", summary)
    sections = []
    for name in files:
        text = (source / name).read_text()
        text = re.sub(r"^# (.+)$", rf"# \1 {{#chapter-{Path(name).stem}}}", text, count=1, flags=re.M)
        text = re.sub(r'<a id="([^"]+)"></a>', r'[]{#\1}', text)
        def fix_link(match):
            label, target = match.groups()
            if urlsplit(target).scheme:
                return match.group()
            file, _, fragment = target.partition("#")
            anchor = fragment or (f"chapter-{Path(file).stem}" if file else "")
            return f"[{label}](#{anchor})"
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", fix_link, text)
        sections.append(text)
    merged = ROOT / ".cache" / f"manuscript-{lang}.md"
    merged.parent.mkdir(exist_ok=True)
    merged.write_text("\n\n".join(sections))
    output = ROOT / "dist" / f"mensoria-sql-0.1.0-draft.1-{lang}.epub"
    title = "Mensoria SQL — Language Standard and Reference" if lang == "en" else "Mensoria SQL——语言标准与参考手册"
    run(pandoc, merged, "--from=markdown+bracketed_spans", "--data-dir=book/pandoc", "--to=epub3", "--standalone", "--toc", "--toc-depth=2", "--split-level=1", "--metadata", f"title={title}", "--metadata", "author=Mensoria", "--metadata", f"lang={lang}", "--metadata", "date=2026-10-29", "--metadata", f"identifier=urn:mensoria:sql:0.1.0-draft.1:{lang}", "--css=book/theme/epub.css", "--epub-cover-image=book/cover.svg", "--output", output)
    documents = check_epub(output)
    shutil.copy2(output, ROOT / "site/downloads" / output.name)
    return {"path": str(output.relative_to(ROOT)), "pandoc": version, "xhtml_documents_checked": documents, "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def landing(epub):
    downloads = ""
    if epub:
        downloads = '<section class="downloads"><h2>Additional formats / 附加格式</h2><a href="downloads/mensoria-sql-0.1.0-draft.1-en.epub">English EPUB</a> · <a href="downloads/mensoria-sql-0.1.0-draft.1-zh-CN.epub">中文 EPUB</a></section>'
    return (ROOT / "web/index.html").read_text().replace("{{epub_links}}", downloads)


def site_metadata():
    site = ROOT / "site"
    (site / "assets").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "web/site.css", site / "assets/site.css")
    shutil.copy2(ROOT / "web/404.html", site / "404.html")
    (site / ".nojekyll").write_text("")
    canonical = "https://mensoria.github.io/mensoria-SQL/"
    (site / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + canonical + "sitemap.xml\n")
    urls = [canonical]
    for lang in ("en", "zh-CN"):
        summary = (ROOT / "book" / lang / "src/SUMMARY.md").read_text()
        for name in re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", summary):
            page = "index.html" if name == "preface.md" else Path(name).with_suffix(".html").name
            urls.append(canonical + lang + "/" + page)
    document = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in urls:
        ET.SubElement(ET.SubElement(document, "url"), "loc").text = url
    ET.ElementTree(document).write(site / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epub", action="store_true", help="Also generate EPUB with locally installed Pandoc 3.x")
    args = parser.parse_args()
    run(sys.executable, ROOT / "scripts/check_book.py")
    executable = mdbook_executable()
    for name in ("site", "dist"):
        (ROOT / name).mkdir(exist_ok=True)
    for lang in ("en", "zh-CN"):
        run(executable, "build", ROOT / "book" / lang, "--dest-dir", ROOT / "site" / lang)
    # Replace only outputs owned by this builder, so an HTML-only build cannot advertise stale EPUBs.
    downloads = ROOT / "site/downloads"
    downloads.mkdir(exist_ok=True)
    for old in downloads.glob("mensoria-sql-*.epub"):
        old.unlink()
    epub = [build_epub(lang) for lang in ("en", "zh-CN")] if args.epub else []
    (ROOT / "site/index.html").write_text(landing(bool(epub)))
    site_metadata()
    run(sys.executable, ROOT / "scripts/check_book.py", "--html")
    report = {"edition": "0.1.0-draft.1", "mdbook": "0.5.4", "status": "documentation_site_build_only", "languages": ["en", "zh-CN"], "epub": epub, "runtime_sql_acceptance": "not_run", "ci": "not_run_locally", "deployment": "not_performed"}
    (ROOT / "dist/build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print("Documentation site build complete: site/index.html")


if __name__ == "__main__":
    main()
