# -*- coding: utf-8 -*-
"""Собрать главу «Курсы Anthropic Academy» из русских пересказов academy/ru/*.json.

    python academy_build.py            # XHTML-фрагмент в stdout
    python academy_build.py --html     # то же, в файл academy/glava.html

Фрагмент состоит из <h2> (глава), <h3> (курсы), <h4> (уроки) и вставляется
build_site.py вместо разметки, которая есть в исходнике Книга-Claude-Code.html.
Ссылки на задания: <a href="#task-slug-page">, сами задания рисует
assets/tasks.js. Схемы урока берутся из academy/media (скачает
academy_figures.py), подписи - из academy/media/captions_ru.json.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RU = os.path.join(HERE, "academy", "ru")
MEDIA = os.path.join(HERE, "academy", "media")

# Адрес схемы на сайте (build_site.py копирует сжатые копии в assets/academy/).
SITE_MEDIA = "/assets/academy/"

# Лицензия и источник. Схемы принадлежат Anthropic; на сайте подписаны
# по CC BY-NC-SA 4.0 со ссылкой на урок.
LICENSE_NOTE = ("Схемы из уроков воспроизведены по лицензии Creative Commons Attribution-NonCommercial-ShareAlike 4.0 "
                "International (CC BY-NC-SA 4.0), источник - Anthropic Academy (academy.claude.com). "
                "Под каждым изображением - ссылка на исходный урок и подпись автора материалов.")
H2 = '<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy: полный разбор</h2>'

LICENSE_HREF = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ru"

INTRO = [
    "Каждый курс Anthropic Academy разобран по урокам: пересказ по разделам оригинала (задание «Попробуйте» и "
    "проверочные вопросы тоже переведены), схемы из урока с подписями на русском, ключевые выводы и задание по "
    "мотивам урока. Пересказы - собственный текст книги; схемы взяты из уроков по лицензии CC BY-NC-SA 4.0 со "
    "ссылкой на оригинал.",
    "Официальные страницы курсов открыты для чтения, но отметки о прохождении выдают только на платформе "
    "academy.claude.com после входа в аккаунт. Задания и проверочные вопросы на этом сайте - для тренировки: они "
    "сохраняют ответы в браузере и не отправляют отметок.",
]

CERTIFICATES = [
    ("Completion badge и сертификат", "После курса на платформе есть итоговый тест. У большинства курсов завершение даёт отметку о прохождении (completion badge), у AI Fluency и Claude 101 - сертификат с проверяемой ссылкой. Порог в AI Fluency - 80% из 10 вопросов."),
    ("Где выдаются", "Только на academy.claude.com и в вашем профиле платформы. Вход по учётной записи; прогресс сохраняется между устройствами."),
    ("Чего нельзя получить на этом сайте", "Официальной отметки, проверяемой ссылки и записи в профиле. Задания здесь - для практики, ответы сохраняются только в вашем браузере."),
    ("Как пройти", "Зарегистрируйтесь на платформе, откройте нужный курс, пройдите уроки и тест. Изучать курс можно и по книге, а тест пройти на платформе."),
    ("Что написано в отметке", "Название курса и факт прохождения. Пособие помогает пройти курс, но отметку выдаёт только платформа."),
]

SOURCE_NOTE = ("Часть данных взята с курсов Anthropic Academy (academy.claude.com): структура курсов, темы уроков, "
               "порядок изложения, задания. Тексты уроков пересказаны на русском языке; схемы из уроков "
               "воспроизводятся по лицензии CC BY-NC-SA 4.0 и остаются собственностью Anthropic.")


def esc(s):
    return html.escape(s, quote=True)


def _load(name, default):
    path = os.path.join(MEDIA, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _inline(s):
    """`код`, **жирный**, ссылки http(s) внутри абзаца пересказа."""
    s = re.sub(r"`([^`\n]+)`", lambda m: "<code>%s</code>" % m.group(1), esc(s))
    s = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", s)
    return s


def figures(slug, page):
    fig = _load("figures.json", {})
    caps = _load("captions_ru.json", {})
    return [{"file": f, "alt": caps.get(f, "")} for f in fig.get("%s/%s" % (slug, page), [])]


def render_figure(f, slug, page, src):
    img = SITE_MEDIA + f["file"]
    return '<img class="academy-figure-img" src="%s" alt="">' % esc(img)


def epub_path_plain():
    """Глава с абсолютными путями картинок: её берут EPUB и фрагменты сайта."""
    return os.path.join(HERE, "academy", "epub_chapter_plain.html")


def epub_path():
    """Файл с главой для EPUB (её собирает --file)."""
    return os.path.join(HERE, "academy", "epub_chapter.html")


def figure_block(img_html, alt, link):
    return ('<figure class="academy-figure">%s'
            '<figcaption><span class="academy-figure-alt">%s</span>'
            '<span class="academy-figure-src">Источник: <a href="%s" target="_blank" rel="noopener">Anthropic Academy'
            '</a> (CC BY-NC-SA 4.0)</span></figcaption></figure>'
            % (img_html, esc(alt), esc(link)))


def render():
    courses = []
    for name in sorted(os.listdir(RU)):
        if name.endswith(".json"):
            with open(os.path.join(RU, name), encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "slug" in data and "lessons" in data:
                courses.append(data)
    courses.sort(key=lambda c: (c.get("order", 0), c["slug"]))

    out = [H2]
    out.append('<p class="lead-in">%s</p>' % esc(INTRO[0]))
    out.append('<p>%s</p>' % esc(INTRO[1]))
    out.append('<div class="callout source-note"><span class="label">Источник материалов</span><p>%s</p>'
               '<p>%s</p><p><a href="%s" target="_blank" rel="noopener">Текст лицензии CC BY-NC-SA 4.0 на русском</a></p></div>'
               % (esc(SOURCE_NOTE), esc(LICENSE_NOTE), LICENSE_HREF))

    out.append('<h3 id="academy-certificates">33.1. Сертификаты и отметки о прохождении</h3>')
    out.append('<div class="table-wrap"><table><thead><tr><th>Вопрос</th><th>Ответ</th></tr></thead><tbody>')
    for q, a in CERTIFICATES:
        out.append("<tr><td>%s</td><td>%s</td></tr>" % (esc(q), esc(a)))
    out.append("</tbody></table></div>")

    out.append('<h3 id="academy-howto">33.2. Как читать главу</h3>')
    out.append("<ul>"
               "<li>Для каждого урока: <strong>пересказ</strong> по разделам оригинала, <strong>схемы</strong> из "
               "урока с русскими подписями и ссылкой на источник, <strong>ключевые выводы</strong>.</li>"
               "<li>Курсы Claude Code 101, Claude Code in Action, «Субагенты» и «Навыки» начинаются с задания "
               "«Попробуйте» и заканчиваются заданием по мотивам урока: шаги, критерии проверки, поле для ответа. "
               "Ответ сохраняется в браузере.</li>"
               "<li>В конце главы - <strong>самопроверка</strong> с вариантами ответов.</li>"
               "</ul>")

    out.append('<h3 id="academy-courses">33.3. Курсы</h3>')
    out.append('<div class="table-wrap academy-overview"><table><thead><tr><th>Курс</th><th>Уроков</th>'
               '<th>Что внутри</th></tr></thead><tbody>')
    for c in courses:
        out.append('<tr><td><a href="#course-block-%s">%s</a></td><td>%d</td><td>%s</td></tr>'
                   % (esc(c["slug"]), esc(c["title"]), len(c["lessons"]), esc(c.get("why") or "")))
    out.append('</tbody></table></div>')
    out.append('<div class="academy-index">')
    for c in courses:
        out.append('<section class="academy-course">')
        out.append('<h4 id="course-%s">%s</h4>' % (esc(c["slug"]), esc(c["title"])))
        if c.get("why"):
            out.append("<p>%s</p>" % esc(c["why"]))
        if c.get("src"):
            out.append('<p class="academy-src">Курс на платформе: <a href="%s" rel="noopener" target="_blank">%s</a></p>'
                       % (esc(c["src"]), esc(c["src"].replace("https://", ""))))
        if c.get("badge"):
            out.append('<p class="academy-badge">%s</p>' % esc(c["badge"]))
        out.append('<ul class="academy-lessons">')
        for l in c["lessons"]:
            out.append('<li><a href="#lesson-%s-%s">%s</a></li>' % (esc(c["slug"]), esc(l["page"]), esc(l["title"])))
        out.append("</ul></section>")
    out.append("</div>")

    out.append('<h3 id="academy-lessons">33.4. Уроки</h3>')
    for ci, c in enumerate(courses, 1):
        out.append('<section class="academy-course-block">')
        out.append('<h4 id="course-block-%s">33.4.%d. %s</h4>' % (esc(c["slug"]), ci, esc(c["title"])))
        src = c.get("src") or "https://academy.claude.com/courses"
        for l in c["lessons"]:
            lid = "lesson-%s-%s" % (c["slug"], l["page"])
            out.append('<div class="academy-lesson">')
            out.append('<h5 id="%s">%s</h5>' % (esc(lid), esc(l["title"])))
            out.append('<p class="academy-lesson-src">Урок на платформе: <a href="%s/%s" target="_blank" rel="noopener">'
                       'academy.claude.com/%s/%s</a></p>'
                       % (esc(src), esc(l["page"]), esc(c["slug"]), esc(l["page"])))
            for p in l.get("summary", []):
                out.append("<p>%s</p>" % _inline(p))
            for f in figures(c["slug"], l["page"]):
                alt = f["alt"] or "Схема из урока Anthropic Academy"
                link = "%s/%s/%s" % (src, c["slug"], l["page"])
                out.append(figure_block(render_figure(f, c["slug"], l["page"], src), alt, link))
            if l.get("points"):
                out.append('<p class="academy-points-title">Ключевое из урока</p>')
                out.append("<ul>")
                for p in l["points"]:
                    out.append("<li>%s</li>" % _inline(p))
                out.append("</ul>")
            if l.get("try"):
                out.append('<div class="callout try"><span class="label">Попробуйте</span>')
                for p in l["try"]:
                    out.append("<p>%s</p>" % _inline(p))
                out.append("</div>")
            t = l.get("task") or {}
            if t.get("steps") or t.get("check"):
                tid = "task-%s-%s" % (c["slug"], l["page"])
                out.append('<div class="task" data-task="%s" data-course="%s" data-lesson="%s" id="%s">'
                           % (esc(c["slug"] + "/" + l["page"]), esc(c["title"]), esc(l["title"]), tid))
                out.append('<p class="task-title">%s</p>' % esc(t.get("title") or "Задание"))
                out.append('<div class="task-body" aria-live="polite"></div>')
                out.append('<details class="task-brief"><summary>Условие</summary>')
                if t.get("intro"):
                    out.append("<p>%s</p>" % esc(t["intro"]))
                out.append('<ol class="task-brief-steps">')
                for s in t.get("steps", []):
                    out.append("<li>%s</li>" % esc(s))
                out.append("</ol>")
                if t.get("check"):
                    out.append("<p><strong>Критерии проверки:</strong></p><ul>")
                    for s in t["check"]:
                        out.append("<li>%s</li>" % esc(s))
                    out.append("</ul>")
                out.append("</details></div>")
            out.append("</div>")
        out.append("</section>")

    out.append('<h3 id="academy-selfcheck">33.5. Самопроверка по всем курсам</h3>')
    out.append('<p>Пятнадцать вопросов по выбору. Ответ проверяется сразу, итог считается в браузере.</p>')
    out.append('<div class="quiz" id="academy-quiz" data-quiz="academy-final"></div>')

    out.append('<h3 id="academy-next">33.6. Что дальше</h3>')
    out.append("<p>Пройдите курсы на платформе, сверяя практику с пересказами. Сохраняйте сертификаты в профиле и "
               "возвращайтесь к заданиям из книги при работе над своими проектами: отметки «сдано» хранятся в этом браузере.</p>")
    return "\n".join(out)


QUIZ_QUESTIONS = [
    {"q": "Чем агент отличается от чата?",
     "options": ["Агент отвечает длиннее", "Агент сам выполняет действия: правит файлы, запускает команды",
                 "Агент работает только в браузере"], "answer": 1,
     "explain": "Агент работает циклом и действует в вашей системе, а не только отвечает текстом."},
    {"q": "Какой шаг завершает агентский цикл?",
     "options": ["Собрать контекст", "Проверить результат", "Задать вопрос пользователю"], "answer": 1,
     "explain": "После действия агент проверяет, достигнут ли итог, и только потом решает, закончить или повторить."},
    {"q": "Какая команда показывает, что занимает контекст?",
     "options": ["/compact", "/context", "/clear"], "answer": 1,
     "explain": "/context показывает объём и распределение контекста; /compact и /clear меняют его."},
    {"q": "Когда уместнее /clear, а не /compact?",
     "options": ["Когда продолжаете ту же функцию", "Когда начинаете новую задачу", "Когда контекст пуст"],
     "answer": 1,
     "explain": "Старый разговор искажает новую задачу; /compact нужен, чтобы продолжить текущую."},
    {"q": "Что надёжнее просьбы в CLAUDE.md?",
     "options": ["Повторить просьбу дважды", "Hook с блокировкой", "Дольше объяснять в чате"], "answer": 1,
     "explain": "Hook - это код, он срабатывает всегда; CLAUDE.md - рекомендация."},
    {"q": "Какой код выхода хука PreToolUse блокирует действие?",
     "options": ["0", "1", "2"], "answer": 2,
     "explain": "2 блокирует и передаёт stderr агенту как причину; 0 - продолжать, другие коды - ошибка без блокировки."},
    {"q": "Когда субагент полезен?",
     "options": ["Когда нужен только результат, а не путь к нему", "Когда каждый шаг зависит от предыдущего",
                 "Всегда"], "answer": 0,
     "explain": "Субагент прячет исследование в своём контексте и возвращает сводку."},
    {"q": "Какой режим лучше для автономного запуска в CI?",
     "options": ["Обход подтверждений", "Auto", "Ручной"], "answer": 1,
     "explain": "В Auto остаётся классификатор безопасности; обход подтверждений убирает последний предохранитель."},
    {"q": "Что стоит проверить в дифе первым делом?",
     "options": ["Правки, о которых вы не просили", "Количество строк", "Имя ветки"], "answer": 0,
     "explain": "Лишние правки, ослабленные тесты и вписанные в код ключи - главные признаки проблем."},
    {"q": "Из чего состоит эвал?",
     "options": ["Вопрос, ответ модели, оценка человека", "Входы, ожидаемые ответы, способ оценки", "Только рубрика"], "answer": 1,
     "explain": "Три части: реалистичные входы, ожидаемые ответы и оценщик (код, модель, человек)."},
    {"q": "Если модель ниже порога, что делать сначала?",
     "options": ["Сменить на дорогую модель", "Прочитать ошибки и исправить промпт", "Уменьшить набор случаев"], "answer": 1,
     "explain": "Правка промпта дешевле смены модели и часто решает проблему."},
    {"q": "Как Claude узнаёт, какой навык применить?",
     "options": ["По описанию в заголовке SKILL.md", "По имени папки", "По размеру файла"], "answer": 0,
     "explain": "В начале загружаются имя и описание; по ним Claude выбирает навык."},
    {"q": "Кто выполняет инструмент в Claude API?",
     "options": ["Модель внутри API", "Ваш код", "Сервер Anthropic всегда"], "answer": 1,
     "explain": "Модель только просит вызвать инструмент; выполняет ваш код, кроме серверных инструментов."},
    {"q": "Что даёт strict tool use?",
     "options": ["Ускоряет модель", "Строгое соответствие аргументов схеме", "Отключает проверки"], "answer": 1,
     "explain": "Схема компилируется в грамматику, и модель не может выдать неверный тип или пропустить поле."},
    {"q": "Зачем нужен ресурс MCP?",
     "options": ["Чтобы предоставлять данные для подстановки в промпт", "Чтобы модель сама нажимала кнопки",
                 "Чтобы заменить промпты"], "answer": 0,
     "explain": "Ресурсы отдают данные, инструменты выполняют действия, промпты задают сценарии."},
    {"q": "Какой транспорт нужен, чтобы сервер мог инициировать запрос (sampling)?",
     "options": ["Только stdio", "Транспорт с потоком событий, например StreamableHTTP", "Любой"], "answer": 1,
     "explain": "Без долгого соединения запросы от сервера к клиенту невозможны."},
    {"q": "Что такое добросовестность (diligence) в рамке 4D?",
     "options": ["Умение писать промпты", "Ответственность и прозрачность при работе с ИИ", "Выбор модели"], "answer": 1,
     "explain": "Это этическая и ответственностная часть: выбор системы, прозрачность, владение результатом."},
    {"q": "Что главное в Cowork для безопасности?",
     "options": ["Выбранная рабочая папка", "Размер промпта", "Скорость модели"], "answer": 0,
     "explain": "Папка задаёт границы чтения и записи."},
    {"q": "Что позволяет командный агент, чего не умеет «личный»?",
     "options": ["Свою идентичность, общую память и общий контекст команды", "Отвечать быстрее", "Работать без сети"], "answer": 0,
     "explain": "Три отличия командного агента: идентичность, общая память, общий контекст."},
]


def quiz_json():
    return json.dumps(QUIZ_QUESTIONS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


if __name__ == "__main__":
    text = render()
    if "--file" in sys.argv:
        # Для EPUB: глава целиком (с заголовком), картинки по относительным путям.
        path = os.path.join(HERE, "academy", "epub_chapter.html")
        html_text = render()
        # Вариант с абсолютными путями: его берут EPUB и фрагменты глав сайта.
        with open(epub_path_plain(), "w", encoding="utf-8", newline="\n") as f:
            f.write(html_text)
        html_text = html_text.replace(SITE_MEDIA, "media/")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html_text)
        print(path, len(html_text))
    elif "--html" in sys.argv:
        path = os.path.join(HERE, "academy", "glava.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(path, len(text))
    else:
        sys.stdout.write(text)
