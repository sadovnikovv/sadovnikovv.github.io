# -*- coding: utf-8 -*-
"""Скачать уроки Anthropic Academy (academy.claude.com) и выделить из них текст,
задания «Try it now» и проверочные вопросы.

    python academy_fetch.py            # скачать всё, что перечислено в SLUGS
    python academy_fetch.py --text     # заодно печатать текст уроков

Только чтение открытых страниц, кэш в site-src/academy/raw/. Страницы
курируемые (без входа видны текст, задания и тесты; проверка ответов - после
входа), поэтому тексты пересказываются по-русски в academy_ru.py, а не
копируются целиком.
"""
import html
import html.parser
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "academy", "raw")
BASE = "https://academy.claude.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# Курсы, которые попадут в книгу. Расширяется по мере пересказа.
SLUGS = [
    "claude-code-101",
    "claude-code-in-action",
    "introduction-to-subagents",
    "introduction-to-evals",
    "introduction-to-agent-skills",
    "introduction-to-model-context-protocol",
    "model-context-protocol-advanced-topics",
    "building-with-the-claude-api",
    "tool-use-with-the-messages-api",
    "claude-101",
    "claude-platform-101",
    "ai-fluency-framework-foundations",
    "building-effective-human-agent-teams",
    "introduction-to-claude-cowork",
]

DROP = {"script", "style", "svg", "noscript", "template", "head", "nav", "header",
        "footer", "aside", "button", "input", "select", "label"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "pre", "blockquote", "tr"}


def get(url, cache_name):
    path = os.path.join(RAW, cache_name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read().decode("utf-8", "replace")
    os.makedirs(RAW, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    time.sleep(0.4)
    return data


class MainText(html.parser.HTMLParser):
    """Текст <main> с грубой структурой: строки по блокам, «[код]» для pre."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.skip = 0
        self.lines = []
        self.cur = []
        self.pre = 0

    def handle_starttag(self, tag, attrs):
        if tag == "main" and not self.depth:
            self.depth = 1
            return
        if not self.depth:
            return
        if tag == "main":
            self.depth += 1
        if tag in DROP:
            self.skip += 1
        if tag == "pre":
            self.flush()
            self.pre += 1
            self.cur.append("CODE: ")
        if tag in BLOCK:
            self.flush()

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "main":
            self.depth -= 1
            if not self.depth:
                self.flush()
            return
        if tag in DROP and self.skip:
            self.skip -= 1
        if tag == "pre" and self.pre:
            self.flush()
            self.pre -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if not self.depth or self.skip:
            return
        if self.pre:
            self.cur.append(data)
        else:
            self.cur.append(re.sub(r"\s+", " ", data))

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.cur)).strip()
        self.cur = []
        if t:
            self.lines.append(t)


def parse_page(s):
    p = MainText()
    p.feed(s)
    lines = p.lines
    # Сайдбар оглавления попадает в <main> - он идёт после «Lesson N of M».
    out = []
    stop = re.compile(r"^(Previous lesson|Next lesson|Lesson \d+ of \d+)")
    for ln in lines:
        if stop.match(ln) and out:
            break
        out.append(ln)
    return out


def course_index(slug):
    s = get("%s/courses/%s" % (BASE, slug), slug + ".html")
    links = []
    seen = set()
    for m in re.finditer(r'href="(/courses/%s/([a-z0-9-]+))"' % re.escape(slug), s):
        if m.group(2) in seen:
            continue
        seen.add(m.group(2))
        links.append(m.group(2))
    title = re.search(r"<title>([^<]*)</title>", s)
    return {
        "slug": slug,
        "title": html.unescape(title.group(1).split("·")[0].strip()) if title else slug,
        "pages": links,
    }


def main():
    show_text = "--text" in sys.argv
    index = []
    for slug in SLUGS:
        try:
            info = course_index(slug)
        except Exception as e:
            print("%-40s ОШИБКА %s" % (slug, e))
            continue
        pages = []
        for page in info["pages"]:
            if page == "badge":
                continue
            try:
                s = get("%s/courses/%s/%s" % (BASE, slug, page), "%s__%s.html" % (slug, page))
            except Exception as e:
                print("   %s/%s ОШИБКА %s" % (slug, page, e))
                continue
            lines = parse_page(s)
            pages.append({"page": page, "lines": lines})
            if show_text:
                print("\n===== %s / %s =====" % (slug, page))
                print("\n".join(lines))
        index.append({"slug": slug, "title": info["title"], "pages": pages})
        print("%-40s страниц: %d" % (slug, len(pages)))
    with open(os.path.join(HERE, "academy", "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
