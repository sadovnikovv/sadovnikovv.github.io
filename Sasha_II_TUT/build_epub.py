# -*- coding: utf-8 -*-
"""Собрать самодостаточный EPUB 3 с крупным шрифтом из Книга-Claude-Code.html.

Нужен только Python 3 стандартной библиотеки (html.parser, zipfile) — никаких
внешних пакетов и интернета. Результат: Книга-Claude-Code.epub рядом со скриптом.

Запуск:
    python build_epub.py
"""
import os
import re
import uuid
import zipfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Книга-Claude-Code.html")
OUT = os.path.join(HERE, "Книга-Claude-Code.epub")

TITLE = "Claude Code для инженера"
AUTHOR = "Практическое пособие: Claude Code, OmniRoute, DeepSeek"
LANG = "ru"

KEEP = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "section", "article",
    "blockquote", "ul", "ol", "li", "pre", "code", "table", "thead", "tbody",
    "tfoot", "tr", "td", "th", "hr", "br", "dl", "dt", "dd", "figure",
    "figcaption", "a", "b", "strong", "i", "em", "u", "s", "sup", "sub",
    "kbd", "caption", "details", "summary", "span",
}
DROP = {"script", "style", "svg", "noscript", "iframe", "template", "head",
        "nav", "img", "link", "meta", "button", "input", "form", "object"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


class Conv(HTMLParser):
    """Переводит фрагмент HTML в безопасный XHTML: только KEEP-теги, без атрибутов."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.stack = []       # открытые теги, которые реально выведены
        self.drop_depth = 0

    def _open(self, tag, attrs=None):
        self.parts.append("<%s>" % tag)
        self.stack.append(tag)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in DROP:
            if tag not in ("br", "hr", "img", "link", "meta", "input"):
                self.drop_depth += 1
            return
        if self.drop_depth:
            return
        if tag not in KEEP:
            return
        if tag == "br":
            self.parts.append("<br/>")
            return
        if tag == "hr":
            return
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("http://") or href.startswith("https://"):
                self.parts.append('<a href="%s">' % esc(href))
                self.stack.append("a")
            return
        if tag == "div":
            tag = "p"
        self._open(tag)

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        if not self.drop_depth and tag == "br":
            self.parts.append("<br/>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in DROP and tag not in ("br", "hr", "img", "link", "meta", "input"):
            if self.drop_depth:
                self.drop_depth -= 1
            return
        if self.drop_depth:
            return
        if tag == "a":
            if "a" in self.stack:
                while self.stack:
                    t = self.stack.pop()
                    self.parts.append("</%s>" % t)
                    if t == "a":
                        break
            return
        if tag == "div":
            tag = "p"
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.parts.append("</%s>" % t)
                if t == tag:
                    break

    def handle_data(self, data):
        if self.drop_depth:
            return
        self.parts.append(esc(data))

    def result(self):
        while self.stack:
            self.parts.append("</%s>" % self.stack.pop())
        return "".join(self.parts)


def convert(fragment):
    c = Conv()
    c.feed(fragment)
    c.close()
    return c.result()


def heading_text(fragment):
    t = strip_tags(fragment)
    t = re.sub(r"\s+", " ", t).strip()
    return t or "Раздел"


def split_chapters(body):
    """Режем книгу на главы по <h2>; заголовок h1 идёт на титул."""
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)
    book_title = heading_text(h1.group(1)) if h1 else TITLE
    if h1:
        body = body[: h1.start()] + body[h1.end():]

    # Секции верхнего уровня в этой книге — <h2 class="...">…</h2>; содержимое
    # между ними относится к текущей главе. finditer по позициям сохраняет
    # вложенность.
    starts = [m.start() for m in re.finditer(r"<h2\b", body, re.I)]
    chapters = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(body)
        seg = body[s:e]
        m = re.match(r"<h2\b[^>]*>(.*?)</h2>", seg, re.S | re.I)
        if m:
            # <span class="chapter">Глава N</span> сохраняем как префикс.
            parts = [heading_text(x) for x in re.findall(r"<span\b[^>]*>(.*?)</span>", m.group(1), re.S | re.I)]
            parts.append(heading_text(re.sub(r"<span\b.*?</span>", "", m.group(1), flags=re.S | re.I)))
            title = " ".join(p for p in parts if p) or "Раздел %d" % (i + 1)
        else:
            title = "Раздел %d" % (i + 1)
        chapters.append((title, seg))
    if not chapters:
        chapters = [(book_title, body)]
    else:
        preface = body[: starts[0]]
        if strip_tags(preface).strip():
            chapters.insert(0, ("От автора", preface))
    return book_title, chapters


STYLE = """@charset "utf-8";
html { font-size: 130%; }
body { font-family: Georgia, "PT Serif", "Times New Roman", serif;
       line-height: 1.65; color: #111; background: #fff; margin: 0 4%;
       hyphens: auto; }
h1, h2, h3, h4 { line-height: 1.25; margin: 1.4em 0 0.6em; page-break-after: avoid; }
h1 { font-size: 1.9em; }
h2 { font-size: 1.55em; border-bottom: 2px solid #333; padding-bottom: .25em; }
h3 { font-size: 1.25em; }
p { margin: 0 0 .9em; text-align: justify; }
a { color: #0a3d62; text-decoration: underline; }
pre { font-family: Consolas, "Courier New", monospace; font-size: .9em;
      line-height: 1.45; background: #f4f4f4; border-left: 4px solid #666;
      padding: .7em; white-space: pre-wrap; word-wrap: break-word;
      page-break-inside: avoid; }
code { font-family: Consolas, "Courier New", monospace; font-size: .95em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .9em; }
th, td { border: 1px solid #999; padding: .35em .5em; vertical-align: top; text-align: left; }
th { background: #eee; }
blockquote { margin: 1em 1.5em; padding-left: 1em; border-left: 4px solid #bbb; font-style: italic; }
ul, ol { margin: 0 0 .9em 1.4em; }
li { margin-bottom: .35em; }
hr { border: 0; border-top: 1px solid #999; margin: 1.5em 0; }
.titlepage { text-align: center; margin-top: 30%; }
.titlepage h1 { font-size: 2.2em; }
.titlepage .sub { font-size: 1.15em; color: #333; margin-top: 1.5em; }
.titlepage .meta { font-size: .95em; color: #555; margin-top: 3em; }
"""

XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="ru" xml:lang="ru">
<head><meta charset="utf-8"/><title>{title}</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body>
</html>
"""


def page(title, body):
    return XHTML.format(title=esc(title), body=body)


def build():
    with open(SRC, encoding="utf-8") as f:
        raw = f.read()

    m = re.search(r"<body\b[^>]*>(.*)</body>", raw, re.S | re.I)
    body = m.group(1) if m else raw
    body = re.sub(r"(?is)<(script|style|svg|head)\b.*?</\1>", "", body)

    book_title, chapters = split_chapters(body)

    items = []  # (имя_файла, xhtml)
    toc = []    # (заголовок, имя_файла)

    title_body = (
        '<section class="titlepage" epub:type="titlepage">'
        "<h1>%s</h1>"
        '<p class="sub">Практическое пособие для инженера</p>'
        '<p class="meta">Текст можно увеличивать в читалке — верстка подстроится.<br/>'
        "Claude Code · OmniRoute · DeepSeek</p>"
        "</section>" % esc(book_title)
    )
    items.append(("title.xhtml", page("Титул", title_body)))
    toc.append(("Титул", "title.xhtml"))

    for i, (ch_title, ch_seg) in enumerate(chapters, 1):
        fname = "ch%03d.xhtml" % i
        html = convert(ch_seg)
        if not strip_tags(html).strip():
            continue
        items.append((fname, page(ch_title, '<section class="chapter">%s</section>' % html)))
        toc.append((ch_title, fname))

    nav = ('<nav epub:type="toc" id="toc"><h1>Оглавление</h1><ol>%s</ol></nav>'
           % "".join('<li><a href="%s">%s</a></li>' % (f, esc(t)) for t, f in toc))
    items.append(("nav.xhtml", page("Оглавление", nav)))

    ncx_points = "".join(
        '<navPoint id="np%d" playOrder="%d"><navLabel><text>%s</text></navLabel>'
        '<content src="%s"/></navPoint>' % (i, i, esc(t), f)
        for i, (t, f) in enumerate(toc, 1))
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="ru">'
           '<head><meta name="dtb:uid" content="{uid}"/><meta name="dtb:depth" content="1"/>'
           '<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>'
           '<docTitle><text>{title}</text></docTitle><navMap>{points}</navMap></ncx>')

    book_id = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "claude-code-engineer-ru-book"))
    items.append(("toc.ncx", ncx.format(uid=book_id, title=esc(book_title), points=ncx_points)))

    content_files = [(n, d) for n, d in items if n not in ("nav.xhtml", "toc.ncx")]
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                '<item id="css" href="style.css" media-type="text/css"/>']
    spine = []
    for name, _ in content_files:
        stem = name.rsplit(".", 1)[0]
        manifest.append('<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (stem, name))
        spine.append('<itemref idref="%s"/>' % stem)

    opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="ru">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">%s</dc:identifier>
<dc:title>%s</dc:title>
<dc:creator>%s</dc:creator>
<dc:language>ru</dc:language>
<dc:description>Практическое пособие для инженера. Крупный шрифт, масштабируемый текст для слабовидящих.</dc:description>
<meta property="dcterms:modified">2026-11-18T00:00:00Z</meta>
<meta property="schema:accessMode">textual</meta>
<meta property="schema:accessModeSufficient">textual</meta>
<meta property="schema:accessibilityFeature">structuralNavigation</meta>
<meta property="schema:accessibilityFeature">readingOrder</meta>
<meta property="schema:accessibilityHazard">none</meta>
<meta property="schema:accessibilitySummary">Крупный шрифт, текст масштабируется средствами читалки.</meta>
</metadata>
<manifest>
%s
</manifest>
<spine toc="ncx">
%s
</spine>
</package>""" % (book_id, esc(book_title), esc(AUTHOR), "\n".join(manifest), "\n".join(spine))

    container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w") as z:
        # mimetype строго первым и без сжатия — требование спецификации EPUB.
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        # Все файлы книги лежат в OEBPS — туда же, где content.opf и style.css.
        entries = [("OEBPS/container.xml", None),
                   ("META-INF/container.xml", container),
                   ("OEBPS/content.opf", opf),
                   ("OEBPS/style.css", STYLE)] + [("OEBPS/" + n, d) for n, d in items]
        for path, data in entries:
            if data is None:
                continue
            info = zipfile.ZipInfo(path, date_time=(2026, 11, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)

    print("OK:", OUT)
    print("Глав:", len(toc), "| размер:", os.path.getsize(OUT), "байт")


if __name__ == "__main__":
    build()
