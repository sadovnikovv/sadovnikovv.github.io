# -*- coding: utf-8 -*-
"""Копии схем Academy для сайта и EPUB.

Схемы лежат в academy/media/*.webp (скачивает academy_figures.py). Для
публикации картинки пережимаются в меньший размер (чтобы не гнать 20 МБ) и
раскладываются в site/assets/academy/; в EPUB попадает та же уменьшенная копия.
Нужен Pillow; при его отсутствии картинки копируются как есть.
"""
import glob
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "academy", "media")
SITE_DIR = os.path.join(SRC, "site")   # сжатые копии для сайта и EPUB (строка в .gitignore)
RASTER = (".webp", ".jpg", ".jpeg", ".png")


def compress(src_dir, dst_dir, max_w=640, quality=52):
    os.makedirs(dst_dir, exist_ok=True)
    files = [f for f in glob.glob(os.path.join(src_dir, "*.webp"))
             + glob.glob(os.path.join(src_dir, "*.png"))
             + glob.glob(os.path.join(src_dir, "*.jpg"))]
    try:
        from PIL import Image
    except ImportError:
        for f in files:
            shutil.copy2(f, os.path.join(dst_dir, os.path.basename(f)))
        return len(files), 0.0, False
    keep = {os.path.basename(f)[:-5] + ".webp" for f in files}
    for name in os.listdir(dst_dir):
        if name not in keep:
            os.remove(os.path.join(dst_dir, name))
    total = 0
    blank = []
    for f in files:
        out = os.path.join(dst_dir, os.path.basename(f)[:-5] + ".webp")
        try:
            from PIL import Image as _I
            w = _I.open(f).width
        except Exception:
            w = 0
        if os.path.exists(out) and _I.open(out).width <= max_w:
            total += os.path.getsize(out)
            continue
            total += os.path.getsize(out)
            continue
        im = Image.open(f).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=quality, method=6)
        blank.append(os.path.basename(out)) if im.convert("L").getextrema()[1] < 20 else None
        total += os.path.getsize(out)
    if blank:
        print("пустые схемы (не загрузились в оригинале): %d" % len(blank))
    return len(files), total / 1e6, True


CODE = {"claude-code-101": "cc101", "claude-code-in-action": "cia",
        "introduction-to-subagents": "sub", "introduction-to-evals": "evals",
        "introduction-to-agent-skills": "skills",
        "introduction-to-model-context-protocol": "mcp",
        "model-context-protocol-advanced-topics": "mcpa",
        "building-with-the-claude-api": "api",
        "tool-use-with-the-messages-api": "tool", "claude-101": "c101",
        "claude-platform-101": "p101",
        "ai-fluency-framework-foundations": "fluency",
        "building-effective-human-agent-teams": "teams",
        "introduction-to-claude-cowork": "cowork"}


def _codes(index):
    out = {}
    for n, c in enumerate(index, 1):
        out[c["slug"]] = CODE.get(c["slug"], "k%d" % n)
    return out


def figures_map():
    """Какие схемы показывать в каком уроке: academy/media/figures.json."""
    top = HERE
    import importlib.util
    spec = importlib.util.spec_from_file_location("academy_figures", os.path.join(top, "academy_figures.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(os.path.join(HERE, "academy", "index.json"), encoding="utf-8") as f:
        index = json.load(f)
    data = {}
    for c in index:
        for p in c["pages"]:
            files = [f["file"] for f in mod.figures_of(c["slug"], p["page"])]
            if files:
                data["%s/%s" % (c["slug"], p["page"])] = files
    # Английская подпись (описание для инструментов) - для перевода.
    path_cap = os.path.join(HERE, "academy", "work", "captions_src.json")
    old_caps = {}
    if os.path.exists(path_cap):
        with open(path_cap, encoding="utf-8") as f:
            old_caps = json.load(f)
    text, used, n = {}, set(), 0
    codes = _codes(index)
    for c in index:
        for pos, p in enumerate(c["pages"], 1):
            for f in mod.figures_of(c["slug"], p["page"]):
                used.add(f["file"])
                key = "%s-%d-%s" % (codes[c["slug"]], pos, f["file"].split(".")[0][:6])
                text[key] = f["alt"]
                n += 1
    orphan = [f for f in sorted(os.listdir(SRC)) if f.endswith(".webp") and f not in used]
    for i, f in enumerate(orphan, 1):
        text["x%d" % i] = old_caps.get("x%d" % i, "")
    with open(path_cap, "w", encoding="utf-8", newline="\n") as f:
        json.dump(text, f, ensure_ascii=False, indent=1)
    path = os.path.join(SRC, "figures.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)
    return len(data), sum(len(v) for v in data.values())


if __name__ == "__main__":
    print("уроков со схемами: %d, схем: %d" % figures_map())
    n, mb, ok = compress(SRC, SITE_DIR)
    print("схем: %d, вес: %.1f МБ, Pillow: %s" % (n, mb, "да" if ok else "нет - скопировано"))
