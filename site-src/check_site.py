# -*- coding: utf-8 -*-
"""Проверка собранного сайта: битые ссылки, якоря, отсутствующие ресурсы.

    python check_site.py [../site]

Код возврата 1, если найдены ошибки. Внешние адреса (http/https) и корневые
адреса (/materials/...) проверяются: первые - пропускаются, вторые
приводятся к пути внутри site/.
"""
import glob
import os
import re
import sys
import urllib.parse
from html.parser import HTMLParser


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)
            if tag == "a" and k == "name" and v:
                self.ids.add(v)


def main(site):
    site = os.path.abspath(site)
    html_files = [p for p in glob.glob(os.path.join(site, "**", "*.html"), recursive=True)]
    ids = {}
    for p in html_files:
        a = Anchors()
        with open(p, encoding="utf-8", errors="replace") as f:
            a.feed(f.read())
        ids[os.path.normcase(p)] = a.ids

    problems = []
    for p in html_files:
        rel = posix = os.path.relpath(p, site).replace(os.sep, "/")
        with open(p, encoding="utf-8", errors="replace") as f:
            s = f.read()
        # Проверяем только «свои» страницы и оглавления; содержимое чужих
        # документов содержит их собственные пути к файлам, которых на сайте нет.
        if posix.startswith("materials/") and not posix.endswith("/index.html"):
            continue
        for m in re.finditer(r'\b(href|src)="([^"]*)"', s):
            url = m.group(2)
            if not url or url.startswith(("http:", "https:", "mailto:", "data:", "javascript:")):
                continue
            path, _, frag = url.partition("#")
            path = urllib.parse.unquote(path)
            if path.startswith("/"):
                target = os.path.normpath(os.path.join(site, path.lstrip("/")))
            elif not path:
                target = p
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(p), path))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                problems.append("%s: нет файла %s" % (rel, url))
                continue
            if frag and os.path.normcase(target) in ids and urllib.parse.unquote(frag) not in ids[os.path.normcase(target)]:
                problems.append("%s: нет якоря %s" % (rel, url))

    seen = sorted(set(problems))
    for pr in seen[:100]:
        print(pr)
    print("HTML-страниц: %d, проблем: %d" % (len(html_files), len(seen)))
    return 1 if seen else 0


if __name__ == "__main__":
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default))
