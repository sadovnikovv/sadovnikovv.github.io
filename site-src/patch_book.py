# -*- coding: utf-8 -*-
"""Встроить шрифты, стили и скрипт сайта прямо в Книга-Claude-Code.html.

Книга остаётся одним автономным файлом (офлайн, без сети), но получает
единую типографику сайта. Запуск вручную, только по решению автора:

    python patch_book.py           # сделать резервную копию и встроить
    python patch_book.py --check   # только сообщить, встроено ли

Повторный запуск ничего не дублирует. Резервная копия кладётся рядом:
Книга-Claude-Code.before-site.html (одна, не перезаписывается).
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
if not any(n.endswith("-Claude-Code.html") for n in os.listdir(SRC)):
    SRC = HERE
BOOK = [os.path.join(SRC, n) for n in sorted(os.listdir(SRC)) if n.endswith("-Claude-Code.html")][0]
BACKUP = BOOK[:-5] + ".before-site.html"
FONTS = os.path.join(HERE, "vendor", "fonts")

MARK = "встроено из site-src/patch_book.py"


def font_faces():
    """@font-face с base64-встроенными шрифтами: файл остаётся автономным."""
    out = []
    for family, fname in (("Noto Sans Book", "sans-regular.woff2"),
                          ("Noto Sans Book", "sans-700.woff2"),
                          ("Noto Serif Book", "serif-regular.woff2"),
                          ("Noto Sans Mono Book", "mono-regular.woff2")):
        path = os.path.join(FONTS, fname)
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        weight = "700" if "-700" in fname else "400"
        out.append("@font-face{font-family:'%s';font-weight:%s;font-style:normal;font-display:swap;"
                   "src:url(data:font/woff2;base64,%s) format('woff2');}"
                   % (family, weight, data))
    return "\n".join(out)


def css_block():
    css = open(os.path.join(HERE, "css", "style.css"), encoding="utf-8").read()
    # Книга главнее стилей сайта: переменные шрифтов задаём на html, а
    # «рамочное» оформление сайта отключаем.
    css = css.replace(":root {", ":root, html[data-theme] {", 1)
    css += """
/* ---- книга целиком: каркас сайта не нужен ---- */
.site-header, .site-footer, .progress, .skip-link, .crumbs, .side-note,
.chapter-nav, .downloads, .toc-note { display: none !important; }
body { margin: 0; }
.wrap { max-width: none; padding: 0 1rem 4rem; }
"""
    return font_faces() + "\n/* ---- стили сайта ---- */\n" + css


def main():
    check = "--check" in sys.argv
    with open(BOOK, encoding="utf-8") as f:
        s = f.read()
    if MARK in s:
        print("Уже встроено:", BOOK)
        return 0
    if check:
        print("Не встроено:", BOOK)
        return 1
    if "</head>" not in s or "</body>" not in s:
        raise SystemExit("В книге нет </head> или </body>")
    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("Резервная копия:", BACKUP)
    block = ("<!-- %s -->\n<style>\n%s\n</style>\n</head>" % (MARK, css_block()))
    s = s.replace("</head>", block, 1)
    s = s.replace("</body>", '<script src="../site-src/js/book-app.js" defer></script>\n</body>', 1)
    with open(BOOK, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("Встроено:", BOOK, "| размер:", os.path.getsize(BOOK), "байт")
    return 0


if __name__ == "__main__":
    sys.exit(main())
