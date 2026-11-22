# -*- coding: utf-8 -*-
"""Генератор кода для главы 34 из образца: только программы, без личных данных.

Запуск: python gen-code.py  (пишет practice/code.json)
Образец расположен в C:/Users/user/Downloads/avito_kites (только чтение).
В JSON попадает только текст кода .py/.ps1 после очистки: адреса, названия
и селекторы площадки заменены, контакты, телефоны, поля продавца удалены.
Профиль браузера, кэш, логи и собранные данные не читаются.

Программы приводятся к связному набору: те же принципы и механизмы, что в
образце, но пути по умолчанию и имена файлов согласованы между модулями,
чтобы пример запускался от начала до конца.
"""
import json
import re
from pathlib import Path

SRC = Path("C:/Users/user/Downloads/avito_kites")
OUT = Path(__file__).with_name("practice") / "code.json"


def strip_comments(text):
    text = re.sub(r'^(\s*)"""(?:.|\n)*?"""\s*\n', '', text, flags=re.M)
    text = re.sub(r'^(\s*)#.*$', '', text, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', text).lstrip("\n")


def dedent(t):
    lines = t.split("\n")
    ind = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
    return "\n".join(l[ind:] if l.strip() else "" for l in lines).strip("\n")


def common(text):
    for a, b in (
        ("https://www.avito.ru/moskva", "https://example.com"),
        ("avito.ru", "example.com"), ("__staticRouterHydrationData", "__pageData"),
        ("catalog-or-main-or-item", "listing-page"), ("buyerItem", "listing"),
        ("avito_id", "item_id"), ("avito", "items"), ("Авито", "площадку"),
        ("[OPERA]", "[BROWSER]"),
        ('[data-marker="item"]', '[data-testid="listing-card"]'),
        ('[data-marker="item-title"]', '[data-testid="listing-title"]'),
        ('[data-marker="item-price"]', '[data-testid="listing-price"]'),
        ('[itemprop="price"]', '[data-testid="listing-price"]'),
        ("Запросы, похожие на ваши", "Подтвердите, что вы не робот"),
        ("Доступ ограничен", "Доступ временно ограничен"),
        ("avito_kites", "search"),
        ('HERE / "items_kites.json"', 'HERE / "search.json"'),
        ('HERE / "items_kites.csv"', 'HERE / "search.csv"'),
        ('"items_kites.json"', '"search.json"'),
        ('"items_kites.csv"', '"search.csv"'),
        ("classification_log.csv", "classification.csv"),
        ("collect_kites", "run_pipeline"),
        ("collect_enriched", "enriched"),
        ('"collect_items.json"', '"search.json"'),
        ('"collect_items.csv"', '"search.csv"'),
    ):
        text = text.replace(a, b)
    text = re.sub(r'^OUT = HERE / "[^"]*"$', 'OUT = HERE / "enriched"', text, flags=re.M)
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "user@example.com", text)
    text = re.sub(r"[A-Za-z0-9+/]{80,}={0,2}", "<base64>", text)
    return text


def read(name):
    return (SRC / name).read_text(encoding="utf-8")


def ps1():
    t = strip_comments(read("start_opera_debug.ps1"))
    t = t.replace("$OperaExe", "$BrowserExe")
    t = re.sub(r'^.*\$AvitoUrl.*$', '$StartUrl = "about:blank"', t, flags=re.M)
    t = t.replace("$AvitoUrl", "$StartUrl")
    t = t.replace('"Debuging ready:"', '"Remote debugging ready:"')
    return dedent(common(t))


def parse():
    t = read("parse_avito.py")
    t = re.sub(r'BASE = \(\n(?:.*\n)*?\)', 'BASE = "https://example.com/search?q=...&p={page}"', t, count=1)
    return dedent(common(strip_comments(t)))


def classify():
    return dedent(common(strip_comments(read("classify.py"))))


def build():
    t = dedent(common(strip_comments(read("build_outputs.py"))))
    t = re.sub(r'^\s*"(seller_name|seller_rating|seller_review_count|address|seller_profile_url)": .*\n', '',
               t, flags=re.M)
    t = t.replace('"items_kites_under_60000.csv"', '"found.csv"').replace('"items_under_60000.csv"', '"found.csv"')
    t = t.replace('"items_all_under_60000.csv"', '"found_all.csv"')
    t = t.replace('"kites_under_60000.csv"', '"found.csv"')
    t = t.replace('"kites_all_under_60000.csv"', '"found_all.csv"')
    t = re.sub(r'_under_60000', '', t)
    return t


def summary():
    t = dedent(common(strip_comments(read("summary.py"))))
    t = t.replace('"kites_under_60000.csv"', '"found.csv"').replace('"kites_all_under_60000.csv"', '"found_all.csv"')
    t = re.sub(r'_under_60000', '', t)
    t = re.sub(r'^TITLE = .*$', 'TITLE = "Итог обработки выгрузки объявлений"', t, flags=re.M)
    t = re.sub(r'Кайты до 60 000 .*\"\)', 'Найдено в бюджете )', t)
    return t


def enrich():
    t = strip_comments(read("enrich.py"))
    t = re.sub(r'^OUT = .*$', 'OUT = HERE / "enriched"', t, flags=re.M)
    t = common(t)
    t = t.replace('''        "seller_name": None, "seller_profile_url": None, "seller_is_company": None,
        "seller_rating_raw": None, "seller_rating": None, "seller_review_count": None,
        "location": None, "address": None, "listing_status": None,''',
                  '''        "seller_is_company": None, "listing_status": None,''')
    t = re.sub(r'\n    s = item\.get\("seller"\)(?:.|\n)*?rec\["seller_rating_raw"\] = .*?\n',
               '\n    s = item.get("seller") or bi.get("seller") or {}\n'
               '    rec["seller_is_company"] = s.get("isCompany")\n', t)
    t = re.sub(r'\n\s+rec\["(address|location)"\] = .*$', '', t, flags=re.M)
    t = re.sub(r'\n    r = bi\.get\("rating"\)(?:.|\n)*?(?=\n    rec\["params"\])', '\n', t)
    return dedent(t)


def orchestrator():
    """Оркестратор: пути согласованы с модулями; лишняя обработка стадий убрана."""
    return dedent('''
import argparse
import importlib.util
import os
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="адрес выдачи с фильтрами (без параметра страницы)")
    ap.add_argument("--slug", required=True, help="короткое имя поиска для папки выгрузки")
    ap.add_argument("--pages", type=int, default=23)
    ap.add_argument("--limit", type=int, default=60000, help="предел цены для отбора")
    args = ap.parse_args()

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    slug = re.sub(r"[^\\w\\-]+", "_", args.slug, flags=re.UNICODE).strip("_")
    out = HERE / "enriched" / f"{ts}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    print(f"[OUT] {out}", flush=True)

    # 1) сбор выдачи (повторный запуск продолжает с места остановки)
    pa = load_mod("collect")
    pa.OUT_DIR = out
    pa.OUT_JSON = out / "search.json"
    pa.OUT_CSV = out / "search.csv"
    pa.BASE = args.url.split("&p=")[0].replace("&p={page}", "")
    sys.argv = ["collect.py", "--out", str(out),
                "--json-name", "search.json", "--csv-name", "search.csv",
                "--url", args.url, "--pages", str(args.pages)]
    pa.main()

    # 2) классификация: отбираем кандидатов для открытия карточек
    cl = load_mod("classify")
    g = cl.main.__globals__
    g["OUT"] = out
    g["PRICE_LIMIT"] = args.limit
    cl.main()

    # 3) открываем карточки кандидатов, каждая дописывается в кэш
    en = load_mod("enrich")
    g = en.main.__globals__
    g["OUT"] = out
    g["CACHE"] = out / "page_cache.jsonl"
    en.main()

    # 4) итоговые файлы по кэшу и сводка
    bo = load_mod("build_report")
    g = bo.main.__globals__
    g["OUT"] = out
    g["CACHE"] = out / "page_cache.jsonl"
    g["LIMIT"] = args.limit
    bo.main()

    su = load_mod("summary")
    g = su.main.__globals__
    g["OUT"] = out
    su.main()
    print(f"[FILES] {out}", flush=True)

if __name__ == "__main__":
    main()
''')


code = {
    "start_browser": ps1(),
    "collect_list": parse(),
    "open_cards": enrich(),
    "classify": classify(),
    "build_report": build(),
    "summary": summary(),
    "orchestrator": orchestrator(),
}
for k, v in code.items():
    bad = [w for w in ("phone", "телефон", "tel:", "seller_name", "avito") if w in v.lower()]
    if bad:
        raise SystemExit("%s: найдены запрещённые слова %s" % (k, bad))
    print(k, len(v.split("\n")), "строк")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(code, ensure_ascii=False, indent=1), encoding="utf-8")
print("записано", OUT)
