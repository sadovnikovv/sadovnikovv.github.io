# -*- coding: utf-8 -*-
"""Собрать статический сайт из книги и ru-materials/.

Только стандартная библиотека Python 3. Источники (источник истины) -
../Книга-Claude-Code.html и ../ru-materials/; скрипт их только читает.

    python build_site.py                 # страницы + папка с материалами
    python build_site.py --no-materials  # только страницы (быстро)

Результат - содержимое ../site/ - публикуется на GitHub Pages
workflow .github/workflows/pages.yml.
"""
import os
import sys

# Windows без -X utf8 кодирует пути в cp1251: имена с кириллицей при чтении
# исходника превращаются в «?». Перезапускаемся в UTF-8-режиме.
if sys.platform == "win32" and not sys.flags.utf8_mode and not os.environ.get("BUILD_SITE_UTF8"):
    os.environ["BUILD_SITE_UTF8"] = "1"
    os.execv(sys.executable, [sys.executable, "-X", "utf8"] + sys.argv)

import argparse
import html
import json
import posixpath
import re
import shutil
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_book  # site-src/fix_book.py
import academy_build  # site-src/academy_build.py
import practice_build  # site-src/practice_build.py

HERE = os.path.dirname(os.path.abspath(__file__))
# Два раскладки: локально комплект лежит в Sasha_II_TUT/Sasha_II_TUT (на уровень
# ниже), на GitHub site-src/ - в корне репозитория рядом с книгой.
# Ищем корень по книге; конкретные имена - через ASCII-подстроки.
def _find_opt(folder, needle):
    return any(needle in n for n in os.listdir(folder))


def _find(folder, needle, is_dir=False):
    for name in sorted(os.listdir(folder)):
        ok = os.path.isdir(os.path.join(folder, name)) if is_dir else os.path.isfile(os.path.join(folder, name))
        if ok and needle in name:
            return os.path.join(folder, name)
    raise SystemExit("В %s не найден файл %r" % (folder, needle))


_UP = os.path.dirname(HERE)


def _root_of(folder):
    """Папка, в которой лежит книга: сама folder или первый подкаталог, где она есть."""
    if any(n.endswith("-Claude-Code.html") for n in os.listdir(folder)):
        return folder
    for name in sorted(os.listdir(folder)):
        sub = os.path.join(folder, name)
        if os.path.isdir(sub) and name != "site" and any(n.endswith("-Claude-Code.html") for n in os.listdir(sub)):
            return sub
    return folder


# На GitHub Pages собирается только папка site/ (artifact), поэтому выход -
# всегда site/ рядом с site-src/; книга и материалы ищутся отдельно.
OUT = os.path.join(_UP, "site")
def _book_root(base):
    """base, если книга в нём, иначе первый подкаталог с книгой (Sasha_II_TUT/)."""
    if any(n.endswith("-Claude-Code.html") for n in os.listdir(base)):
        return base
    for name in sorted(os.listdir(base)):
        sub = os.path.join(base, name)
        if os.path.isdir(sub) and any(n.endswith("-Claude-Code.html") for n in os.listdir(sub)):
            return sub
    raise SystemExit("Не найдена книга *-Claude-Code.html ни в %s, ни в его подпапках" % base)


SRC = _book_root(_UP)


def _find(folder, needle, is_dir=False):
    for name in sorted(os.listdir(folder)):
        ok = os.path.isdir(os.path.join(folder, name)) if is_dir else os.path.isfile(os.path.join(folder, name))
        if ok and needle in name:
            return os.path.join(folder, name)
    raise SystemExit("В %s не найден файл %r" % (folder, needle))


BOOK = _find(SRC, "-Claude-Code.html")
MATERIALS = _find(SRC, "ru-materials", is_dir=True)
MATERIALS_NAME = os.path.basename(MATERIALS)
BOOK_NAME = os.path.basename(BOOK)
EPUB_NAME = BOOK_NAME[:-5] + ".epub"

SITE_TITLE = "Claude Code для инженера"
SITE_DESC = "Практическое пособие для инженера: Claude Code, OmniRoute, DeepSeek, основы ИИ, агенты."
SITE_URL = "https://sadovnikovv.github.io"
# Главы с личными данными (выписка по оплате, выгрузка переписки) на сайт не идут.
PRIVATE = {"deepseek-billing", "migration", "new-pc"}
REDACTED_CHAPTER = ('<p class="note-redacted">Эта глава не опубликована: в ней личные данные '
                    '(выписка по балансу, сохранённая переписка). Она остаётся в офлайн-книге.</p>')
REPO_URL = "https://github.com/sadovnikovv/sadovnikovv.github.io/raw/main"

# ru-materials → site/materials: что копируем.
COPY_EXT = (".md", ".pdf", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp")
# В git не кладём крупные PDF (папка site/ пересобирается, а история git - нет);
# вместо них - ссылка на исходник в репозитории.
NO_COPY_OVER = 3 * 1024 * 1024
BIG_PDFS = [[]]   # заполняется в build_materials: какие PDF ушли в репозиторий
FINAL = [set()]   # то же, что LinkMap.files: все адреса материалов на сайте
SKIP_DIRS = {".github", "__pycache__", "node_modules"}

# Файлы сайта, которые нельзя затереть.
PROTECTED = {"index.html", "pages", "book.html", "404.html", "about.html", "CNAME",
             "robots.txt", "sitemap.xml", "download", "materials",
             "CLAUDE.md", "site-src", "ru-materials", "claude-code-handbook-ru",
             "assets", "_headers", ".nojekyll"}


# --------------------------------------------------------------------------
# Мини-Markdown. Сырой HTML из чужого Markdown всегда экранируется.
# --------------------------------------------------------------------------
INLINE = re.compile(
    r"(?<!\\)(?P<code>`[^`\n]+`)"
    r"|(?P<img>!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\))"
    r"|(?P<link>\[(?P<text>[^\]]+)\]\((?P<href>[^)\s]+)(?:\s+\"[^\"]*\")?\))"
    r"|(?P<auto><(?P<url>https?://[^>\s]+)>)"
    r"|(?P<bold>\*\*(?P<btxt>[^*]+)\*\*)"
    r"|(?<![\w*])(?P<ital>\*(?P<itxt>[^*\n]+)\*)(?![\w*])"
)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
UL_ITEM = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OL_ITEM = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?(?:\s*:?-{2,}:?\s*\|)+\s*(?::?-{2,}:?)?\s*$")
HR = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
FENCE = re.compile(r"^\s*(```|~~~)\s*([\w+#.-]*)\s*$")
DETAILS = re.compile(r"^\s*<details\b.*$", re.I)


def esc(s):
    return html.escape(s, quote=True)


class Anchorer:
    def __init__(self):
        self.used = set()

    def make(self, text):
        slug = re.sub(r"[^\w]+", "-", text.lower().replace("ё", "е")).strip("-") or "h"
        if not re.search(r"[a-z0-9]", slug):
            slug = "h"
        base, n = slug, 2
        while slug in self.used:
            slug = "%s-%d" % (base, n)
            n += 1
        self.used.add(slug)
        return slug


class LinkMap:
    """Урлы материалов, как они появятся на сайте (с папкой materials/)."""

    def __init__(self, out_files):
        self.files = set()
        for f in out_files:
            self.files.add(f)
            if f.lower().endswith(".md"):
                self.files.add(f[:-3] + ".html")
        self.dirs = {""}
        for f in self.files:
            d = posixpath.dirname(f)
            while d:
                self.dirs.add(d)
                d = posixpath.dirname(d)

    def href(self, url, current_rel, page_dir):
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith(("#", "//")):
            return url
        path, sep, frag = url.partition("#")
        if not path:
            return "#" + frag
        path = urllib.parse.unquote(path)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(current_rel), path))
        full = "materials/" + target if target and target != "." else "materials"
        if not (full in self.files or full.rstrip("/") in self.dirs):
            return url                                   # битая ссылка - оставляем как есть
        page_dir = page_dir or "."
        out = posixpath.relpath(full, page_dir)
        if full in self.dirs or path.endswith("/"):
            out = out.rstrip("/") + "/index.html"
        elif full.lower().endswith(".md"):
            out = out[:-3] + ".html"
        return urllib.parse.quote(out, safe="/.-~") + ("#" + frag if sep else "")


def inline(text, current_rel, lm, page_dir):
    out, pos = [], 0
    for m in INLINE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        pos = m.end()
        g = m.groupdict()
        if g["code"]:
            out.append("<code>%s</code>" % esc(g["code"][1:-1]))
        elif g["img"]:
            out.append('<img src="%s" alt="%s" loading="lazy">'
                       % (esc(lm.href(g["src"], current_rel, page_dir)), esc(g["alt"] or "")))
        elif g["link"]:
            out.append('<a href="%s">%s</a>'
                       % (esc(lm.href(g["href"], current_rel, page_dir)), inline(g["text"], current_rel, lm, page_dir)))
        elif g["auto"]:
            out.append('<a href="%s">%s</a>' % (esc(g["url"]), esc(g["url"])))
        elif g["bold"]:
            out.append("<strong>%s</strong>" % inline(g["btxt"], current_rel, lm, page_dir))
        elif g["ital"]:
            out.append("<em>%s</em>" % inline(g["itxt"], current_rel, lm, page_dir))
        else:
            out.append(esc(m.group(0)))
    out.append(esc(text[pos:]))
    return "".join(out)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def anchor_html(level, raw, lm, page_dir, anchors):
    hid = anchors.make(raw)
    return ('<h%d id="%s">%s <a class="h-anchor" href="#%s" aria-label="Ссылка на раздел">#</a></h%d>'
            % (level, hid, inline(raw, "", lm, page_dir), hid, level))


# Порядок блоков кода в документе: practice_build.py ставит им подписи.
CODE_ORDER = []

def md_to_html(text, current_rel, lm, page_dir, anchors, base_level=2):
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")
    lines = text.split("\n")
    out, para = [], []
    i, n = 0, len(lines)

    def inl(s):
        return inline(s, current_rel, lm, page_dir)

    def flush():
        if para:
            out.append("<p>%s</p>" % inl("\n".join(para).strip()))
            para.clear()

    while i < n:
        line = lines[i]

        m = FENCE.match(line)
        if m:
            flush()
            fence = m.group(1)
            lang = m.group(2)
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith(fence):
                body.append(lines[i])
                i += 1
            i += 1
            cls = ' class="language-%s"' % esc(lang) if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(body))))
            CODE_ORDER.append(lang or "text")
            continue

        if DETAILS.match(line):
            flush()
            buf = []
            while i < n:
                buf.append(lines[i])
                done = re.match(r"^\s*</details>\s*$", lines[i], re.I)
                i += 1
                if done:
                    break
            inner = "\n".join(buf).strip()
            inner = re.sub(r"^<details\b[^>]*>\s*", "", inner, flags=re.I)
            inner = re.sub(r"\s*</details>\s*$", "", inner, flags=re.I)
            summ = ""
            sm = re.match(r"\s*<summary[^>]*>(.*?)</summary>", inner, re.S | re.I)
            if sm:
                summ = re.sub(r"<[^>]+>", "", sm.group(1)).strip()
                inner = inner[sm.end():]
            out.append("<details><summary>%s</summary>\n%s\n</details>"
                       % (inl(summ or "Подробнее"), md_to_html(inner, current_rel, lm, page_dir, anchors, base_level)))
            continue

        if not line.strip():
            flush()
            i += 1
            continue

        m = HEADING.match(line)
        if m:
            flush()
            level = max(base_level, min(6, len(m.group(1)) + 1))
            raw = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.group(2))
            raw = re.sub(r"[`*]", "", raw) if base_level == 2 else raw
            if len(m.group(1)) == 1 and base_level == 1:
                level = 1
            out.append(anchor_html(level, raw, lm, page_dir, anchors))
            i += 1
            continue

        if HR.match(line):
            flush()
            out.append("<hr>")
            i += 1
            continue

        if "|" in line and i + 1 < n and TABLE_SEP.match(lines[i + 1]):
            flush()
            head = split_row(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            out.append("<div class=\"table-wrap\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (
                "".join("<th>%s</th>" % inl(c) for c in head),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inl(c) for c in r) for r in rows)))
            continue

        if line.lstrip().startswith(">"):
            flush()
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>\n%s\n</blockquote>"
                       % md_to_html("\n".join(buf), current_rel, lm, page_dir, anchors, base_level))
            continue

        if UL_ITEM.match(line) or OL_ITEM.match(line):
            flush()
            items, ordered = [], bool(OL_ITEM.match(line))
            while i < n:
                cur = lines[i]
                mu, mo = UL_ITEM.match(cur), OL_ITEM.match(cur)
                if mu:
                    items.append(mu.group(2))
                elif mo:
                    items.append(mo.group(3))
                elif not cur.strip():
                    break
                elif items and cur.startswith((" ", "\t")) and not FENCE.match(cur):
                    items[-1] += " " + cur.strip()
                else:
                    break
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>\n%s\n</%s>" % (tag, "\n".join("<li>%s</li>" % inl(t) for t in items), tag))
            continue

        para.append(line)
        i += 1

    flush()
    return "\n".join(out)


def first_heading(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        t = re.sub(r"[`*_\[\]]|\[([^\]]*)\]\([^)]*\)", lambda x: x.group(1) or "", m.group(1))
        return re.sub(r"\s+", " ", t).strip() or fallback
    return fallback


# --------------------------------------------------------------------------
# Книга
# --------------------------------------------------------------------------
def extract_main(s, trim_practice=True):
    m = re.search(r'<main id="content"[^>]*>', s)
    if not m:
        raise SystemExit('В книге не найден <main id="content">')
    depth, pos = 1, m.end()
    for t in re.finditer(r"<(/?)main\b[^>]*>", s[pos:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            body = s[pos:pos + t.start()]
            if trim_practice:
                # из исходника могла остаться старая версия практикума: берём главу заново
                body = re.sub(r'<h2 id="practice"[^>]*>.*?(?=<h2\\b|</main>)', '', body, flags=re.S)
            return body
    raise SystemExit('В книге не закрыт <main id="content">')


def cover_title(s):
    m = re.search(r'<header class="cover"[^>]*>.*?<h1[^>]*>(.*?)</h1>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else SITE_TITLE


def replace_academy_chapters(chapters):
    """Вместо короткой главы из исходника - разбор курсов академии из academy/ru. Сама книга
    по-прежнему правится в одном HTML; разбор курсов собирается отдельно."""
    ru = academy_build.render().strip()
    block = ('<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy</h2>'
             '<p>Подробный разбор в главе ниже, по уроку на каждую тему, с заданиями.</p>')
    # вставляем прямо в текст главы, заголовок главы уже есть в шаблоне разбора
    ru = ru.replace('<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy: полный разбор</h2>', "", 1)
    for i, c in enumerate(chapters):
        if c["id"] == "academy":
            chapters[i]["html"] = block + ru
            chapters[i]["title"] = "Глава 33 Курсы Anthropic Academy"
            chapters[i]["short"] = "Глава 33"
            return
    # в исходнике главы нет - добавляем в конец
    chapters.append({"id": "academy", "title": "Глава 33 Курсы Anthropic Academy", "short": "Глава 33",
                     "raw_title": "", "html": block + ru})



def add_practice_chapter(chapters):
    """Глава 34: практикум по сбору данных в браузере (код и задания собираются отдельно)."""
    chapter = {"id": "practice", "title": "Глава 34 Практикум: агент в браузере",
               "short": "Глава 34", "raw_title": "", "html": practice_build.make_section(practice_inner_html())}
    for i, c in enumerate(chapters):
        if c["id"] == "practice":
            chapters[i] = chapter
            return chapters
    chapters.append(chapter)
    return chapters


def practice_inner_html():
    """HTML главы 34 с подписями у блоков кода (lang и заголовок программы)."""
    del CODE_ORDER[:]
    md = practice_build.markdown()
    # Разметка заданий - сырой HTML: на время перевода Markdown->HTML он прячется
    # за метками, иначе экранируется как текст.
    blocks = []

    def hide(m):
        blocks.append(m.group(0))
        return "@@PRACTICE_BLOCK_%d@@" % (len(blocks) - 1)

    md = re.sub(r'<div class="task".*?</details></div>', hide, md, flags=re.S)
    md = re.sub(r'<div class="callout warn">.*?</div>', hide, md, flags=re.S)
    md = re.sub(r'<div class="quiz".*?</div>', hide, md, flags=re.S)
    inner = md_to_html(md, "practice.md", LinkMap(set()), "", Anchorer(), base_level=2)
    inner = re.sub(r"@@PRACTICE_BLOCK_(\d+)@@", lambda m: blocks[int(m.group(1))], inner)
    labels = list(CODE_ORDER)
    ordered = [c["title"] for c in practice_build.load()[0]["chapters_code"]]
    n = [0]

    def label(m):
        i = n[0]
        n[0] += 1
        lang = labels[i] if i < len(labels) else "text"
        title = ordered[i] if i < len(ordered) else "код"
        return '<pre data-lang="%s" data-label="%s">' % (esc(lang), esc(title))

    inner = re.sub(r"<pre>", label, inner)
    return inner


def split_chapters(main):
    starts = [m.start() for m in re.finditer(r"<h2\b", main)]
    chunks = []
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else len(main)
        seg = main[s:e]
        m = re.match(r"<h2([^>]*)>(.*?)</h2>", seg, re.S)
        if not m:
            continue
        hid = re.search(r'id="([^"]+)"', m.group(1))
        raw_title = m.group(2)
        # «<span>Глава 6</span>История…» → «Глава 6. История…»
        spaced = re.sub(r"</span>", "</span> ", raw_title)
        title = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", spaced))).strip()
        num = re.search(r'<span[^>]*class="chapter[^"]*"[^>]*>(.*?)</span>', raw_title, re.S)
        short = html.unescape(re.sub(r"<[^>]+>", "", num.group(1))).strip() if num else title
        chunks.append({"id": hid.group(1) if hid else "glava-%d" % k,
                       "raw_title": raw_title, "title": title, "short": short, "html": seg})
    return chunks, main[:starts[0]] if starts else main


PAGE_TPL = """<!DOCTYPE html>
<html lang="ru" data-book-src="{root}book.html">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site_url}/assets/favicon.svg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/serif-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/sans-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/fonts/fonts.css">
<link rel="stylesheet" href="{root}assets/style.css">
{extra_head}
</head>
<body>
<a class="skip-link" href="#book">Перейти к тексту</a>
<header class="site-header">
  <div class="bar">
    <strong><a href="{root}index.html">{site}</a></strong>
    <a href="{root}materials/index.html">Материалы</a>
    <a href="{root}about.html">О книге</a>
    <a href="{root}download/{book_epub}" download>EPUB</a>
    <details class="bar__support">
      <summary><span class="bar__support-label">Поддержать проект</span><span class="bar__support-arrow" aria-hidden="true"></span></summary>
      <div class="bar__support-panel">
        <p>Книга бесплатна. Поддержка добровольная - сумму выбираете вы.</p>
        <iframe
          src="https://yoomoney.ru/quickpay/fundraise/widget?billNumber=1LNFDBQH1ED.261122&"
          title="ЮMoney - поддержать автора книги"
          width="500"
          height="480"
          frameborder="0"
          allowtransparency="true"
          scrolling="no"
          loading="lazy"
        ></iframe>
        <p><a href="https://yoomoney.ru/fundraise/1LNFDBQH1ED.261122" target="_blank" rel="noopener">Открыть форму поддержки на ЮMoney</a></p>
      </div>
    </details>
</header>
<div class="progress" aria-hidden="true"><span id="progress-bar"></span></div>
<aside class="side-toc" id="side-toc" aria-label="Оглавление книги"><div class="side-toc-title"><a href="{root}index.html">Оглавление</a></div></aside>
<main class="wrap" id="book">
{body}
</main>
<footer class="site-footer">
  <nav class="chapter-nav" aria-label="Навигация по главам">
    <span>{prev}</span>
    <a data-rel="toc" href="{root}index.html">Оглавление</a>
    <span>{next}</span>
  </nav>
  <p>Источник - <a href="{root}book.html">книга одним файлом</a>,
  <a href="{root}download/{book_epub}">EPUB</a>.</p>
</footer>
<script type="application/json" id="page-list">{pages}</script>
<script type="application/json" id="quiz-data">{quiz}</script>
<script type="application/json" id="practice-quiz-data">{practice_quiz}</script>
<script src="{root}assets/app.js" defer></script>
<script src="{root}assets/code-copy.js" defer></script>
<script src="{root}assets/tasks.js" defer></script>
<script>
document.addEventListener('click', function (e) {{
  document.querySelectorAll('.bar__support[open]').forEach(function (d) {{
    if (!d.contains(e.target)) d.open = false;
  }});
}});
document.addEventListener('keydown', function (e) {{
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.bar__support[open]').forEach(function (d) {{
    d.open = false;
    var s = d.querySelector('summary');
    if (s) s.focus();
  }});
}});
</script>
</body>
</html>
"""


def shell(rel, title, body, pages_json, extra_head="", prev="", next=""):
    root = "../" * rel.count("/")
    base = "index.html" if rel in ("index.html", "pages/index.html") else posixpath.basename(rel)
    canonical = SITE_URL + "/" + ("" if base == "index.html" else posixpath.dirname(rel) + "/")
    return PAGE_TPL.format(
        title=esc(title), desc=esc(SITE_DESC), site=SITE_TITLE, site_url=SITE_URL,
        canonical=esc(canonical), root=root, body=body, pages=pages_json,
        extra_head=extra_head, prev=prev, next=next,
        book_epub=EPUB_NAME, quiz=academy_build.quiz_json(),
        practice_quiz=json.dumps(practice_build.questions(), ensure_ascii=False).replace("</", "<\\/"))


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


MAT_LINK = re.compile(r'href="(%s)([^"]*)?"' % re.escape(MATERIALS_NAME))


def _md_url(url):
    path, sep, frag = url.partition("#")
    if path.endswith(".md"):
        path = path[:-3] + ".html"
    elif path and not path.endswith("/") and not posixpath.splitext(path)[1]:
        path += "/index.html"
    return path + ("#" + frag if sep else "")


def _fix_mat(m):
    tail = m.group(2) or ""
    if not tail:
        out = "/index.html"
    elif tail.startswith("/"):
        out = _md_url(tail) if not tail.endswith("/") else tail + "index.html"
    elif tail.endswith("/"):
        out = tail + "index.html"
    elif not posixpath.splitext(tail)[1]:
        out = tail + "/index.html"
    else:
        return m.group(0)
    return 'href="materials%s"' % urllib.parse.quote(out, safe="/#")


def _pdf_in_source(rel):
    return os.path.isfile(os.path.join(MATERIALS, rel.replace("/", os.sep)))


def lm_files():
    files, _ = collect_materials()
    out = set()
    big = set()
    for f in files:
        src = os.path.join(MATERIALS, f.replace("/", os.sep))
        if f.lower().endswith(".pdf") and os.path.getsize(src) > NO_COPY_OVER:
            big.add(f)
    for f in files:
        if f in big:
            out.add("materials/" + f + ".html")
        else:
            out.add("materials/" + f)
        if f.lower().endswith(".md"):
            out.add("materials/" + f[:-3] + ".html")
    return out


def rewrite_links(s, exists=None, big_pdfs=()):
    """Папка ru-materials из книги → папка сайта materials/. Абсолютные адреса
    (/materials/...) работают и со страниц pages/, и с главной. Крупные PDF
    на сайте - страницы-переходы (*.pdf.html)."""
    def fix(m):
        tail = m.group(2) or ""
        url = urllib.parse.unquote(tail)          # убираем уже готовое %-кодирование
        path, sep, frag = url.partition("#")
        if path:
            rel = path.strip("/")
            ok = (path.endswith("/") or rel in FINAL[0] or rel.lower().endswith(".md")
                  or _pdf_in_source(rel))
            if not ok:
                return m.group(0)                 # битая ссылка - оставляем как есть
            path = _md_url(path) if not path.endswith("/") else path + "index.html"
            if path.lstrip("/").removeprefix("materials/") in big_pdfs:
                path += ".html"
        out = "materials" + path
        return 'href="/%s%s"' % (urllib.parse.quote(out, safe="/"), ("#" + frag) if sep else "")
    return MAT_LINK.sub(fix, s)


def build_pages():
    with open(BOOK, encoding="utf-8") as f:
        raw = f.read()
    # Те же правки, что и fix_book.py: работают, даже если его не запускали.
    raw = fix_book.fix(raw)[0]

    main = extract_main(raw, trim_practice=False)
    title = cover_title(raw)
    chapters, cover = split_chapters(main)
    replace_academy_chapters(chapters)
    add_practice_chapter(chapters)

    all_files = lm_files()
    BIG_PDFS[0] = [x[len("materials/"):][:-5] for x in all_files if x.endswith(".pdf.html")]
    FINAL[0] = {x[len("materials/"):] for x in all_files}
    big_set = {f for f in BIG_PDFS[0]} | {"materials/" + f for f in BIG_PDFS[0]}
    for c in chapters:
        c["html"] = rewrite_links(c["html"], None, big_set)
        if c["id"] in PRIVATE:
            c["html"] = REDACTED_CHAPTER
            c["short"] = c["title"] = c["title"].split(" ")[0] + " " + c["title"].split(" ")[1] + " (не публикуется)"
    cover = rewrite_links(cover, None, big_set)

    pages = [{"title": c["title"], "short": c["short"],
              "url": "pages/%s.html" % re.sub(r"[^A-Za-z0-9_-]", "-", c["id"])} for c in chapters]
    # Экранируем "</", чтобы строки с </h2> в заголовках не рвали <script>.
    pages_json = json.dumps(pages, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    # Отдельные страницы глав.
    for k, c in enumerate(chapters):
        body = ('<section class="chapter">%s</section>' % c["html"])
        prev = ""
        nxt = ""
        if k > 0:
            prev = '<a data-rel="prev" href="../%s">← %s</a>' % (pages[k - 1]["url"], esc(pages[k - 1]["short"]))
        if k + 1 < len(chapters):
            nxt = '<a data-rel="next" href="../%s">%s →</a>' % (pages[k + 1]["url"], esc(pages[k + 1]["short"]))
        root = "../" * pages[k]["url"].count("/")
        head = ('<link rel="alternate" type="text/html" href="%sbook.html#%s">\n'
                '<meta name="page-index" content="%d">') % (root, esc(c["id"]), k + 1)
        write(pages[k]["url"], shell(pages[k]["url"], "%s - %s" % (c["short"], title),
                                     body, pages_json, head, prev, nxt))

    # Главная.
    toc_items = "".join('<li><a href="%s">%s</a></li>' % (p["url"], esc(p["title"])) for p in pages)
    body = (cover + '\n<div class="toc-wrap"><h2 id="oglavlenie">Оглавление</h2>'
            '<p class="toc-note">Каждая глава открывается отдельно. '
            '<a href="book.html">Открыть всю книгу одним файлом</a>.</p>'
            '<div class="toc-grid"><ol>%s</ol></div></div>'
            '\n<section class="downloads"><h2 id="formats">Другие форматы</h2><ul>'
            '<li><a href="download/%s" download>EPUB</a> - для читалки, крупный масштабируемый шрифт.</li>'
            '<li><a href="book.html">HTML одним файлом</a> - сохранить и читать без сети.</li>'
            '<li><a href="materials/index.html">Папка с материалами</a> - документация, гайды, открытые книги.</li>'
            '</ul></section>' % (toc_items, EPUB_NAME))
    # Якоря #глава на главной ведут на отдельные страницы глав.
    ids = {c["id"] for c in chapters}
    body = re.sub(r'href="#([A-Za-z0-9_-]+)"',
                  lambda m: 'href="pages/%s.html"' % m.group(1) if m.group(1) in ids else m.group(0), body)
    body += "".join('<a id="%s"></a>' % esc(c["id"]) for c in chapters if c["id"])
    head = '<meta name="page-index" content="0">\n<link rel="alternate" type="text/html" href="book.html">'
    write("index.html", shell("index.html", title, body, pages_json, head))

    build_book(raw)
    write("404.html", build_404())
    write("about.html", build_about(len(chapters)))
    write("CNAME", SITE_URL.replace("https://", "") + "\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    urls = ["%s/" % SITE_URL] + ["%s/%s" % (SITE_URL, p["url"]) for p in pages] + \
           ["%s/about.html" % SITE_URL, "%s/book.html" % SITE_URL]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n'
          % "".join("<url><loc>%s</loc></url>" % esc(u) for u in urls))
    write("assets/favicon.svg", FAVICON)
    write(".nojekyll", "")
    write("_headers", HEADERS)
    print("Книга: глав %d, страниц глав %d" % (len(chapters), len(chapters)))
    return pages


ACADEMY_H2_LONG = '<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy: полный разбор</h2>'
ACADEMY_H2_SHORT = '<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy</h2>\n'
TASK_SCRIPTS = ('<script src="assets/book-app.js" defer></script>\n'
                '<script src="assets/code-copy.js" defer></script>\n'
                '<script src="assets/tasks.js" defer></script>\n'
                '<script type="application/json" id="quiz-data">%s</script>\n'
                '<script type="application/json" id="practice-quiz-data">%s</script>\n</body>')


def build_book(raw):
    """book.html - офлайн-издание; подключаем общие стили сайта."""
    head = ('<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n'
            '<link rel="stylesheet" href="assets/fonts/fonts.css">\n'
            '<link rel="stylesheet" href="assets/style.css">\n')
    s = raw.replace("</head>", head + "</head>", 1)
    s = rewrite_links(s, None, {"materials/" + f for f in BIG_PDFS[0]} | set(BIG_PDFS[0]))
    # Офлайн-файл: ссылки на Markdown оставляем как есть, а не на .html.
    def back(m):
        tgt = os.path.join(OUT, urllib.parse.unquote(m.group(1)))
        if not os.path.exists(tgt) and os.path.exists(tgt[:-5] + ".md"):
            return m.group(1)[:-5] + ".md" + (m.group(2) or "")
        return m.group(0)
    s = re.sub(r'href="(materials/[^"#]*\.html)(#[^"]*)?"', back, s)
    # Крупные PDF: в офлайн-файле - прямая ссылка на файл в репозитории.
    for f in BIG_PDFS[0]:
        s = s.replace("/materials/%s.html" % f,
                      REPO_URL + urllib.parse.quote("/" + posixpath.join(MATERIALS_NAME, f), safe="/"))
    # Личные главы в публичную версию не попадают.
    for cid in PRIVATE:
        m = re.search(r'<h2 id="%s"[^>]*>.*?(?=<h2\b|</main>)' % re.escape(cid), s, re.S)
        if m:
            s = s[:m.start()] + ('<h2 id="%s">Глава не публикуется</h2>\n%s\n'
                                 % (cid, REDACTED_CHAPTER)) + s[m.end():]
    # Главы 33 и 34 офлайн-книги собираются заново: тело из сборщика, а не
    # короткая версия из исходника. Новая версия идёт вместо старой.
    body_html = ACADEMY_H2_SHORT + academy_build.render().strip().replace(ACADEMY_H2_LONG, "")
    for ch in add_practice_chapter(list(split_chapters(extract_main(raw, trim_practice=False))[0])):
        if ch["id"] == "practice":
            body_html += ch["html"]
    # сначала старые копии из исходника, потом новая версия перед </main>.
    # Главы 33 и 34 собираются заново и идут в конец книги, как на сайте.
    def cut(s, cid):
        start = s.find('<h2 id="%s"' % cid)
        if start < 0:
            return s
        end = s.find('<h2', start + 4)
        if end < 0:
            end = s.find('</main>', start)
        if end < 0:
            end = s.find('<footer', start)
        return s[:start] + s[end:]
    for cid in ('academy', 'practice'):
        s = cut(s, cid)
    main_end = s.find('</main>')
    s = s[:main_end] + body_html + s[main_end:]
    s = s.replace("</body>", TASK_SCRIPTS % (academy_build.quiz_json(),
                                             json.dumps(practice_build.questions(), ensure_ascii=False).replace("</", "<\\/")), 1)
    # «Поддержать автора» в шапке книги: кнопка после EPUB.
    # «Поддержать автора» в шапке книги: кнопка после EPUB.
    # «Поддержать автора»: в книге на одной странице - кнопка в боковой панели
    # рядом с настройками чтения (сверху в HTML нет шапки сайта).
    book_support = ("""
    <details class="bar__support">
      <summary><span class="bar__support-label">Поддержать проект</span><span class="bar__support-arrow" aria-hidden="true"></span></summary>
      <div class="bar__support-panel">
        <p>Книга бесплатна. Поддержка добровольная - сумму выбираете вы.</p>
        <iframe
          src="https://yoomoney.ru/quickpay/fundraise/widget?billNumber=1LNFDBQH1ED.261122&"
          title="ЮMoney - поддержать автора книги"
          width="500"
          height="480"
          frameborder="0"
          allowtransparency="true"
          scrolling="no"
          loading="lazy"
        ></iframe>
        <p><a href="https://yoomoney.ru/fundraise/1LNFDBQH1ED.261122" target="_blank" rel="noopener">Открыть форму поддержки на ЮMoney</a></p>
      </div>
    </details>
    """)
    s = s.replace('<p class="nav-note">', book_support + '<p class="nav-note">', 1)
    write("book.html", s)


def build_404():
    body = ("<section class='cover'><h1>Страница не найдена</h1>"
            "<p class='lead'>Возможно, у главы изменился адрес. Откройте оглавление - там весь текст.</p>"
            "<p><a href='index.html'>← К оглавлению</a></p></section>")
    s = shell("404.html", "404 - " + SITE_TITLE, body, "[]")
    return s


def build_about(n_chapters):
    body = """<section class="cover">
<h1>О книге</h1>
<p class="lead">«Claude Code для инженера» - практическое пособие о том, как устроены
ИИ-агент, языковая модель и инструменты вокруг них, и как встроить их в инженерную
работу: схемы, платы, контроллеры, CAD, документация. %d глав.</p>
<h2 id="editions">Издания</h2>
<div class="table-wrap"><table>
<thead><tr><th>Формат</th><th>Где</th><th>Когда выбрать</th></tr></thead>
<tbody>
<tr><td>Сайт с оглавлением</td><td><a href="index.html">главная</a></td><td>чтение с телефона и компьютера, ссылки на разделы</td></tr>
<tr><td>Книга одним файлом</td><td><a href="book.html">book.html</a></td><td>весь текст на одной странице, поиск браузера; можно сохранить и читать без сети</td></tr>
<tr><td>EPUB</td><td><a href="download/%s" download>%s</a></td><td>читалка, крупный масштабируемый шрифт</td></tr>
<tr><td>Материалы</td><td><a href="materials/index.html">папка с материалами</a></td><td>официальная документация, гайды, открытые книги</td></tr>
</tbody></table></div>
<h2 id="how">Как обновляется</h2>
<p>Исходник книги - один файл в корне репозитория. После правки
запускается <code>python build_site.py</code> из папки <code>site-src/</code>,
и сайт публикуется заново.</p>
<h2 id="rights">Права</h2>
<p>Сторонние материалы в папке с материалами принадлежат их авторам и
распространяются по лицензиям, указанным в самих материалах.</p>
</section>""" % (n_chapters, EPUB_NAME, EPUB_NAME)
    return shell("about.html", "О книге - " + SITE_TITLE, body, "[]")


HEADERS = r"""/\*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; font-src 'self'; frame-src https://yoomoney.ru; frame-ancestors 'self'
  Cache-Control: public, max-age=600

/assets/\*
  Cache-Control: public, max-age=31536000, immutable

/book.html
  Cache-Control: public, max-age=3600
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="12" fill="#17505f"/>
<text x="32" y="45" font-family="Georgia,serif" font-size="32" font-weight="700"
 fill="#fff" text-anchor="middle">CC</text>
</svg>
"""


# --------------------------------------------------------------------------
# Папка с материалами
# --------------------------------------------------------------------------
MAT_TPL = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{title}</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{site_root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{site_root}assets/fonts/fonts.css">
<link rel="stylesheet" href="{site_root}assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Перейти к тексту</a>
<header class="site-header">
  <div class="bar">
    <strong><a href="{site_root}index.html">{site}</a></strong>
    <a href="{site_root}materials/index.html">Материалы</a>
    <a href="{site_root}about.html">О книге</a>
    <details class="bar__support">
      <summary><span class="bar__support-label">Поддержать проект</span><span class="bar__support-arrow" aria-hidden="true"></span></summary>
      <div class="bar__support-panel">
        <p>Книга бесплатна. Поддержка добровольная - сумму выбираете вы.</p>
        <iframe
          src="https://yoomoney.ru/quickpay/fundraise/widget?billNumber=1LNFDBQH1ED.261122"
          title="ЮMoney - поддержать автора книги"
          loading="lazy"
        ></iframe>
        <p><a href="https://yoomoney.ru/fundraise/1LNFDBQH1ED.261122" target="_blank" rel="noopener">Открыть форму поддержки на ЮMoney ↗</a></p>
      </div>
    </details>
  </div>
</header>
<main class="wrap mat" id="main">
<nav class="crumbs" aria-label="Хлебные крошки"><a href="{root}materials/index.html">Материалы</a>{crumbs}</nav>
{body}
</main>
<footer class="site-footer">
  <p>Материалы собраны из открытых источников; права принадлежат их авторам.</p>
</footer>
<script src="{root}assets/code-copy.js" defer></script>
<script>
document.addEventListener('click', function (e) {{
  document.querySelectorAll('.bar__support[open]').forEach(function (d) {{
    if (!d.contains(e.target)) d.open = false;
  }});
}});
document.addEventListener('keydown', function (e) {{
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.bar__support[open]').forEach(function (d) {{
    d.open = false;
    var s = d.querySelector('summary');
    if (s) s.focus();
  }});
}});
</script>
</html>
"""


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def collect_materials():
    files, dirs = [], []
    for dirpath, dirnames, filenames in os.walk(MATERIALS):
        dirnames[:] = sorted((d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")), key=natural)
        rel = os.path.relpath(dirpath, MATERIALS).replace(os.sep, "/")
        rel = "" if rel == "." else rel
        for f in sorted(filenames, key=natural):
            if f.startswith("."):
                continue
            if f.lower().endswith(COPY_EXT):
                files.append(posixpath.join(rel, f) if rel else f)
        for d in dirnames:
            dirs.append(posixpath.join(rel, d) if rel else d)
    return files, dirs


def mat_shell(rel_dir, title, body, root, crumbs, site_root):
    # root - от папки материалов до site/, site_root - от самой страницы; URL-ы
    # не должны содержать "../" (GitHub Pages такие пути не отдаёт).
    page = posixpath.join("materials", rel_dir, "index.html") if rel_dir else "materials/index.html"
    return MAT_TPL.format(title=esc(title), site=SITE_TITLE,
                          site_root=site_root, root=root, body=body, crumbs=crumbs)



def build_materials():
    files, dirs = collect_materials()
    # В пространстве site/ у Markdown-страниц расширение .html - регистрируем и его.
    lm = LinkMap(files)
    linked = set()
    for f in files:
        src = os.path.join(MATERIALS, f.replace("/", os.sep))
        if f.lower().endswith(".pdf") and os.path.getsize(src) > NO_COPY_OVER:
            linked.add(f)
            # Ссылки из Markdown и книги должны указывать на копию в репозитории.
            lm.files.add("materials/" + f + ".html")
            BIG_PDFS[0].append(f)
            continue
        dst = os.path.join(OUT, "materials", f.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    by_dir = {}
    for f in files:
        by_dir.setdefault(posixpath.dirname(f), []).append(f)

    md_pages = 0
    for f in files:
        if not f.lower().endswith(".md"):
            continue
        with open(os.path.join(MATERIALS, f.replace("/", os.sep)), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        rel_dir = posixpath.dirname(f)
        out_rel = "materials/" + f[:-3] + ".html"
        page_dir = posixpath.dirname(out_rel)
        root = "../" * out_rel.count("/")
        crumbs = ""
        parts = rel_dir.split("/") if rel_dir else []
        for k, part in enumerate(parts):
            sub = "/".join(parts[:k + 1])
            crumbs += ' / <a href="%sindex.html">%s</a>' % (
                root + "materials/" + urllib.parse.quote(sub, safe="/") + "/", esc(part))
        body = md_to_html(text, f, lm, page_dir, Anchorer(), base_level=1)
        title = first_heading(text, posixpath.basename(f))
        write(out_rel, mat_shell(rel_dir, title, body, root, crumbs, root))
        md_pages += 1

    all_dirs = {""} | {posixpath.dirname(f) for f in files} | set(dirs)
    idx_pages = 0
    for d in sorted(all_dirs, key=lambda x: (x.count("/"), natural(x))):
        root = "../" * (d.count("/") + 2) if d else "../"
        rel_dir = d
        crumbs = ""
        parts = d.split("/") if d else []
        for k, part in enumerate(parts):
            sub = "/".join(parts[:k + 1])
            crumbs += ' / <a href="%sindex.html">%s</a>' % (
                root + "materials/" + urllib.parse.quote(sub, safe="/") + "/", esc(part))
        parts_out = ['<h1>%s</h1>' % esc("Материалы" if d == "" else posixpath.basename(d))]
        if d == "":
            parts_out.append("<p class='lead'>Скачанные документы: официальная документация Claude Code "
                             "и OmniRoute, гайды сообщества, основы ИИ и открытые книги.</p>")
        subdirs = sorted({x for x in dirs if posixpath.dirname(x) == d and any(f.startswith(x + "/") for f in files)},
                         key=natural)
        if subdirs:
            parts_out.append('<h2>Папки</h2><ul class="dir-list">')
            for x in subdirs:
                parts_out.append('<li><a href="%s/index.html">%s/</a></li>'
                                 % (urllib.parse.quote(posixpath.basename(x)), esc(posixpath.basename(x))))
            parts_out.append("</ul>")
        entries = sorted(by_dir.get(d, []), key=natural)
        readme = [f for f in entries if posixpath.basename(f).lower() == "readme.md"]
        if readme:
            rn = [f for f in entries if posixpath.basename(f).lower() == "readme.md"][0]
            parts_out.append('<p><a class="readme-link" href="%s.html">Открыть README этого раздела →</a></p>'
                             % esc(urllib.parse.quote(posixpath.basename(rn)[:-3])))
        docs = [f for f in entries if f.lower().endswith(".md") and f not in readme]
        if docs:
            parts_out.append("<h2>Документы</h2><ul class=\"doc-list\">")
            for f in docs:
                with open(os.path.join(MATERIALS, f.replace("/", os.sep)), encoding="utf-8", errors="replace") as fh:
                    t = first_heading(fh.read(), posixpath.basename(f))
                name = urllib.parse.quote(posixpath.basename(f))
                parts_out.append('<li><a href="%s.html">%s</a> <small>%s</small></li>'
                                 % (name[:-3], esc(t), esc(posixpath.basename(f))))
            parts_out.append("</ul>")
        pdfs = [f for f in entries if f.lower().endswith(".pdf")]
        if pdfs:
            parts_out.append("<h2>PDF</h2><ul class=\"doc-list\">")
            for f in pdfs:
                name = posixpath.basename(f)
                kb = os.path.getsize(os.path.join(MATERIALS, f.replace("/", os.sep))) // 1024
                # Крупные PDF лежат в репозитории: *.pdf - страница-переход.
                size = ("%d МБ, хранится в репозитории" % (kb // 1024)) if f in linked else ("%d КБ" % kb)
                href = urllib.parse.quote(name) + (".html" if f in linked else "")
                parts_out.append('<li><a href="%s" download>%s</a> <small>%s</small></li>'
                                 % (esc(href), esc(name), size))
            parts_out.append("</ul>")
        others = [f for f in entries if f.lower().endswith(COPY_EXT[1:])]
        if others:
            parts_out.append('<h2>Картинки</h2><ul class="dir-list">')
            for f in others:
                name = posixpath.basename(f)
                if f in linked:          # крупный PDF: на сайте только страница-переход
                    continue
                parts_out.append('<li><a href="%s">%s</a></li>' % (esc(urllib.parse.quote(name)), esc(name)))
            parts_out.append("</ul>")
        if not (subdirs or docs or pdfs or readme or others):
            parts_out.append("<p>В этой папке нет документов для чтения.</p>")
        out_rel = "materials/%sindex.html" % (d + "/" if d else "")
        title = "Материалы" if d == "" else posixpath.basename(d)
        write(out_rel, mat_shell(rel_dir, title, "\n".join(parts_out), root, crumbs, root))
        idx_pages += 1
    write_pdf_redirects(linked)
    print("Материалы: файлов %d (крупных PDF по ссылке: %d), страниц Markdown %d, индексов %d"
          % (len(files), len(linked), md_pages, idx_pages))


REDIRECT_TPL = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<title>Переход к файлу</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
</head><body><p>Файл большой и хранится в репозитории:
<a href="{url}">{name}</a>.</p></body></html>
"""


def write_pdf_redirects(linked):
    """Крупные PDF физически не лежат на сайте - отдаём маленькую страницу-переход."""
    for f in linked:
        name = posixpath.basename(f)
        url = REPO_URL + urllib.parse.quote("/" + posixpath.join(MATERIALS_NAME, f), safe="/")
        write("materials/" + f + ".html", REDIRECT_TPL.format(url=esc(url), name=esc(name)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-materials", action="store_true", help="не пересобирать папку с материалами")
    ap.add_argument("--debug", action="store_true", help="печатать, какие ссылки переписаны")
    args = ap.parse_args()

    for name in os.listdir(OUT) if os.path.isdir(OUT) else []:
        if os.path.join(OUT, name) in (SRC,):
            raise SystemExit("site/ указывает на корень проекта - проверьте пути")
        if name not in PROTECTED:
            raise SystemExit("В site/ найден неожиданный файл %r - сайт собирается только здесь" % name)

    os.makedirs(OUT, exist_ok=True)
    assets = os.path.join(OUT, "assets")
    os.makedirs(assets, exist_ok=True)
    shutil.copy2(os.path.join(HERE, "css", "style.css"), os.path.join(assets, "style.css"))
    shutil.copy2(os.path.join(HERE, "js", "app.js"), os.path.join(assets, "app.js"))
    shutil.copy2(os.path.join(HERE, "js", "book-app.js"), os.path.join(assets, "book-app.js"))
    shutil.copy2(os.path.join(HERE, "js", "tasks.js"), os.path.join(assets, "tasks.js"))
    shutil.copy2(os.path.join(HERE, "js", "code-copy.js"), os.path.join(assets, "code-copy.js"))
    shutil.copytree(os.path.join(HERE, "vendor", "fonts"), os.path.join(assets, "fonts"), dirs_exist_ok=True)

    dl = os.path.join(OUT, "download")
    os.makedirs(dl, exist_ok=True)
    # HTML-издание целиком - это и есть book.html (сайт встраивает в него
    # свои стили и скрипт). Отдельную копию не кладём: сайт должен быть лёгким.
    for f in (EPUB_NAME,):
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(dl, f))
        else:
            print("warning: нет файла", p)

    build_pages()
    if not args.no_materials:
        build_materials()
    print("Готово:", OUT)


if __name__ == "__main__":
    main()
