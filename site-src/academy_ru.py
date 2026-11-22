# -*- coding: utf-8 -*-
"""Сборка русских пересказов курсов Anthropic Academy из academy/ru/*.json.

    python academy_ru.py check      # проверить, что каждый урок курса присутствует
    python academy_ru.py fill       # добавить пустые заготовки для недостающих уроков

Пересказы - наши собственные тексты по мотивам открытых уроков. Исходные
английские страницы кэшируются в academy/raw/ (в репозиторий не идут).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RU = os.path.join(HERE, "academy", "ru")
INDEX = os.path.join(HERE, "academy", "index.json")


def load():
    with open(INDEX, encoding="utf-8") as f:
        index = json.load(f)
    ru = {}
    if os.path.isdir(RU):
        for name in sorted(os.listdir(RU)):
            if name.endswith(".json"):
                with open(os.path.join(RU, name), encoding="utf-8") as f:
                    data = json.load(f)
                # файлы без курса (например, текст практикума) сюда не относятся
                if isinstance(data, dict) and "slug" in data and "lessons" in data:
                    ru[data["slug"]] = data
    return index, ru


def check(index, ru):
    problems = 0
    for course in index:
        slug = course["slug"]
        if slug not in ru:
            print("%-42s нет пересказа" % slug)
            problems += 1
            continue
        have = {l["page"] for l in ru[slug]["lessons"]}
        missing = [p["page"] for p in course["pages"] if p["page"] not in have and p["page"] != "badge"]
        empty = [l["page"] for l in ru[slug]["lessons"] if not l.get("summary")]
        if missing:
            print("%-42s не хватает уроков: %s" % (slug, ", ".join(missing)))
            problems += 1
        if empty:
            print("%-42s без пересказа: %d" % (slug, len(empty)))
    print("Курсов: %d, с пересказом: %d, проблем: %d" % (len(index), len(ru), problems))
    return 1 if problems else 0


def fill(index, ru):
    for course in index:
        slug = course["slug"]
        data = ru.get(slug) or {"slug": slug, "title": course["title"], "why": "", "src": "", "badge": "", "lessons": []}
        have = {l["page"] for l in data["lessons"]}
        for p in course["pages"]:
            if p["page"] in have or p["page"] == "badge":
                continue
            data["lessons"].append({"page": p["page"], "title": p["page"].replace("-", " ").capitalize(),
                                    "summary": [], "points": [], "try": [],
                                    "task": {"title": "Задание по мотивам курса", "intro": "", "steps": [], "check": []}})
        os.makedirs(RU, exist_ok=True)
        with open(os.path.join(RU, slug + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    print("Заготовки обновлены в", RU)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    index, ru = load()
    sys.exit(check(index, ru) if cmd == "check" else fill(index, ru) or 0)
