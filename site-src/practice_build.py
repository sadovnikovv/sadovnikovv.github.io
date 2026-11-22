# -*- coding: utf-8 -*-
"""Глава 34: практикум «агент в браузере» (сбор данных с сайта).

Сборка: из practice_ru.json (текст, задания, вопросы) и practice/code.json
(очищенный код программ) делается Markdown для md_to_html; блоки кода получают
подписи. Код из code.json содержит только программы - без профилей, кэшей
и собранных данных.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.join(HERE, "academy", "practice_ru.json")
CODE = os.path.join(HERE, "academy", "practice", "code.json")


def esc(s):
    return html.escape(s, quote=True)


def load():
    with open(TEXT, encoding="utf-8") as f:
        text = json.load(f)
    with open(CODE, encoding="utf-8") as f:
        code = json.load(f)
    return text, code


def markdown():
    """Текст главы (без заголовка h2) в Markdown для md_to_html."""
    text, code = load()
    out = ["**Практикум.** " + text["why"], ""]

    for s in text["sections"]:
        out.append("## " + s["title"])
        out.append("")
        for p in s.get("paras", []):
            out.append(p)
            out.append("")
        if s.get("bullets"):
            out.extend("- " + b for b in s["bullets"])
            out.append("")
        if s["title"].startswith("Безопасность"):
            out.append('<div class="callout warn"><span class="label">Перед запуском</span>'
                       '<p>Практикум собран из рабочего примера сбора товаров. Весь код с персональными полями '
                       'вычищен: в примере нет телефонов, почт, имён, адресов и ссылок на профили. '
                       'Если ваш сценарий требует таких данных, не собирайте их.</p></div>')
            out.append("")

    out.append("## Код программ")
    out.append("")
    out.append("Можно скопировать целиком: у каждого блока вверху кнопка «Копировать» и, для одиночных "
               "команд, «Вставить в терминал». Перед запуском замените адрес выдачи и CSS-селекторы "
               "карточек на те, что есть на вашей странице.")
    out.append("")
    for item in text["chapters_code"]:
        out.append("### " + item["title"])
        out.append("")
        out.append(item["about"])
        out.append("")
        out.append("```" + item["lang"])
        out.append(code[item["key"]].rstrip())
        out.append("```")
        out.append("")

    out.append("## Задания")
    out.append("")
    for t in text["tasks"]:
        tid = "task-practice-" + "".join(ch if ch.isalnum() else "-" for ch in t["title"].lower()).strip("-")
        out.append("### " + t["title"])
        out.append("")
        out.append(t["intro"])
        out.append("")
        out.append('<div class="task" data-task="practice/%s" data-course="Практикум: агент в браузере" '
                   'data-lesson="%s" id="%s"><p class="task-title">%s</p>'
                   '<div class="task-body" aria-live="polite"></div>'
                   '<details class="task-brief"><summary>Условие</summary><ol class="task-brief-steps">'
                   % (esc(tid), esc(t["title"]), tid, esc(t["title"])))
        out.extend("<li>%s</li>" % esc(s) for s in t["steps"])
        out.append("</ol><p><strong>Критерии проверки:</strong></p><ul>")
        out.extend("<li>%s</li>" % esc(s) for s in t["check"])
        out.append("</ul></details></div>")
        out.append("")

    out.append("## Самопроверка")
    out.append("")
    out.append("Пять вопросов по инструментам, которые использованы в примере.")
    out.append("")
    out.append('<div class="quiz" id="practice-quiz" data-quiz="practice"></div>')
    return "\n".join(out)


def make_section(inner_html):
    # обёртки нет: глава вставляется между <h2> и следующим <h2>, как остальные
    return ('<h2 id="practice"><span class="chapter">Глава 34</span> '
            'Практикум: агент в браузере, сбор данных с сайта</h2>\n' + inner_html + '\n')


def questions():
    text, _ = load()
    return text["questions"]
