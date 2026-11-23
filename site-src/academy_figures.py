# -*- coding: utf-8 -*-
"""Схемы из уроков Anthropic Academy: скачать и описать по-русски.

    python academy_figures.py            # скачать недостающие, обновить captions.json
    python academy_figures.py --check    # только отчёт: какие схемы есть, какие нет

Что делается:
1. из кэша academy/raw/<slug>__<page>.html выписываются адреса <img> с /assets/media/;
2. картинка скачивается в academy/media/<имя>.webp (копия для офлайн-книги и EPUB);
3. alt из оригинала переводится на русский в academy/media/captions.json.

Лицензия: материалы курсов Anthropic Academy используются по лицензии
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0). На сайте схемы подписаны «Источник: Anthropic Academy
(CC BY-NC-SA 4.0)» со ссылкой на урок, книги не продаются и не
сопровождаются рекламой. Для каждого урока в academy_build.py указан
оригинал со ссылкой.
"""
import argparse
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "academy", "raw")
MEDIA = os.path.join(HERE, "academy", "media")
INDEX = os.path.join(HERE, "academy", "index.json")
CAPTIONS = os.path.join(MEDIA, "captions.json")
BASE = "https://academy.claude.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")

MEDIA_RE = re.compile(r'src="(/assets/media/([0-9a-f]{64})\.(?:jpg|png|webp|gif))"')


def figures_of(slug, page):
    path = os.path.join(RAW, "%s__%s.html" % (slug, page))
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        s = f.read()
    out, seen = [], set()
    for m in MEDIA_RE.finditer(s):
        name = m.group(2)
        if name in seen:
            continue
        seen.add(name)
        quoted = s.rfind('src="' + m.group(1), 0, m.start())
        tag_start = s.rfind("<img", 0, quoted if quoted != -1 else m.start())
        tag = s[tag_start:s.find('>', m.start()) + 1 if s.find('>', m.start()) != -1 else m.start() + 200]
        alt = re.search(r'alt="([^"]*)"', tag)
        out.append({"file": name + ".webp", "src": m.group(1),
                    "alt": (alt.group(1) if alt else "").strip()})
    return out


def download(url, path):
    if os.path.exists(path):
        return False
    req = urllib.request.Request(BASE + url + "?w=1600", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    time.sleep(0.3)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    with open(INDEX, encoding="utf-8") as f:
        index = json.load(f)
    os.makedirs(MEDIA, exist_ok=True)
    captions = {}
    if os.path.exists(CAPTIONS):
        with open(CAPTIONS, encoding="utf-8") as f:
            captions = json.load(f)
    missing, total = [], 0
    for c in index:
        for p in c["pages"]:
            figs = figures_of(c["slug"], p["page"])
            total += len(figs)
            for f in figs:
                missing.append(f["file"])
                if args.check:
                    continue
                download(f["src"], os.path.join(MEDIA, f["file"]))
                if f["file"] not in captions:
                    captions[f["file"]] = f["alt"]
    if not args.check:
        with open(CAPTIONS, "w", encoding="utf-8", newline="\n") as f:
            json.dump(captions, f, ensure_ascii=False, indent=1, sort_keys=True)
    have = sum(1 for f in set(missing) if os.path.exists(os.path.join(MEDIA, f)))
    print("Схем на страницах: %d, уникальных: %d, скачано: %d, без перевода подписи: %d"
          % (total, len(set(missing)), have,
             sum(1 for f in set(missing) if f in captions and re.search(r"[A-Za-z]{4,}", captions[f]))))


if __name__ == "__main__":
    main()
