# -*- coding: utf-8 -*-
"""Мелкие правки самого исходника книги, которые должны попасть и в HTML, и в EPUB.

    python fix_book.py           # сделать резервную копию и поправить
    python fix_book.py --check   # только сообщить, есть ли что править

1. Длинное тире (-) заменяется на обычное (-). Двоеточия и прочие знаки не
   трогаются. Текст страницы-заглушки самим исходником не меняется.
2. В заголовках «<span class="chapter">Глава 1</span>Название» добавляется
   пробел после номера главы: глава 1 и название не слипаются.

Повторный запуск ничего не меняет. Резервная копия рядом, одна:
Книга-Claude-Code.before-fix.html.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if not any(n.endswith("-Claude-Code.html") for n in os.listdir(ROOT)):
    for name in sorted(os.listdir(ROOT)):
        sub = os.path.join(ROOT, name)
        if os.path.isdir(sub) and any(n.endswith("-Claude-Code.html") for n in os.listdir(sub)):
            ROOT = sub
            break
BOOK = [os.path.join(ROOT, n) for n in sorted(os.listdir(ROOT)) if n.endswith("-Claude-Code.html")][0]
BACKUP = BOOK[:-5] + ".before-fix.html"

DASH = "—"


def fix(s):
    n_dash = s.count(DASH)
    s = s.replace(" %s " % DASH, " - ")
    s = s.replace(DASH, "-")
    # «</span>Название» только внутри h2 (номер главы перед названием).
    n_space = 0

    def h2(m):
        nonlocal n_space
        inner = m.group(2)
        new = re.sub(r'(<span[^>]*>.*?</span>)(?=[^\s<])', r"\1 ", inner)
        if new != inner:
            n_space += 1
        return "<h2%s>%s</h2>" % (m.group(1), new)

    s = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, s, flags=re.S)
    return s, n_dash, n_space


def main():
    check = "--check" in sys.argv
    with open(BOOK, encoding="utf-8") as f:
        s = f.read()
    new, n_dash, n_space = fix(s)
    if new == s:
        print("Править нечего:", BOOK)
        return 0
    print("Найдено: длинных тире %d, заголовков без пробела %d" % (n_dash, n_space))
    if check:
        return 1
    if not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("Резервная копия:", BACKUP)
    with open(BOOK, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("Исправлено:", BOOK)
    return 0


if __name__ == "__main__":
    sys.exit(main())
