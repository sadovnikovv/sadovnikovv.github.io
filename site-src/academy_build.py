# -*- coding: utf-8 -*-
"""Собрать главу «Курсы Anthropic Academy» из русских пересказов academy/ru/*.json.

    python academy_build.py            # XHTML-фрагмент в stdout
    python academy_build.py --html     # то же, в файл academy/glava.html

Фрагмент состоит из <h2> (глава) и <h3> (уроки) и вставляется build_site.py
вместо разметки, которая есть в исходнике Книга-Claude-Code.html. Ссылки на
задания: <a href="#task-slug-page">, сами задания рисует assets/tasks.js.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RU = os.path.join(HERE, "academy", "ru")

INTRO = [
    "Каждый курс Anthropic Academy разобран по урокам: короткий пересказ, ключевые выводы, "
    "задание по мотивам урока и самопроверка. Пересказы - собственный текст книги, "
    "сверенный с уроками; английские оригиналы и их расшифровки остаются собственностью "
    "Anthropic и здесь не копируются.",
    "Официальные страницы курсов открыты для чтения, но отметки о прохождении выдают только "
    "на платформе academy.claude.com после входа в аккаунт. Задания и проверочные вопросы на "
    "этом сайте - для тренировки: они сохраняют ответы в браузере и не отправляют отметок.",
]

CERTIFICATES = [
    ("Completion badge и сертификат", "После курса на платформе есть итоговый тест. У большинства курсов завершение даёт отметку о прохождении (completion badge), у AI Fluency и Claude 101 - сертификат с проверяемой ссылкой. Порог в AI Fluency - 80% из 10 вопросов."),
    ("Где выдаются", "Только на academy.claude.com и в вашем профиле платформы. Вход по учётной записи; прогресс сохраняется между устройствами."),
    ("Чего нельзя получить на этом сайте", "Официальной отметки, проверяемой ссылки и записи в профиле. Задания здесь - для практики, ответы сохраняются только в вашем браузере."),
    ("Как пройти", "Зарегистрируйтесь на платформе, откройте нужный курс, пройдите уроки и тест. Изучать курс можно и по книге, а тест пройти на платформе."),
    ("Что написано в отметке", "Название курса и факт прохождения. Курсы, которые здесь разобраны кратко, требуют больше материала, чем поместилось в книгу, поэтому не гарантируется, что практики из книги достаточно для прохождения теста."),
]

SOURCE_NOTE = ("Часть данных взята с курсов Anthropic Academy (academy.claude.com): структура курсов, "
               "темы уроков, задания и проверочные вопросы. Тексты уроков пересказаны на русском языке; "
               "оригиналы остаются у Anthropic.")


def esc(s):
    return html.escape(s, quote=True)


def render():
    courses = []
    for name in sorted(os.listdir(RU)):
        if name.endswith(".json"):
            with open(os.path.join(RU, name), encoding="utf-8") as f:
                courses.append(json.load(f))
    courses.sort(key=lambda c: (c.get("order", 0), c["slug"]))

    out = ['<h2 id="academy"><span class="chapter">Глава 33</span> Курсы Anthropic Academy: полный разбор</h2>']
    out.append('<p class="lead-in">%s</p>' % esc(INTRO[0]))
    out.append('<p>%s</p>' % esc(INTRO[1]))
    out.append('<div class="callout source-note"><span class="label">Источник материалов</span><p>%s</p></div>' % esc(SOURCE_NOTE))

    out.append('<h3 id="academy-certificates">33.1. Сертификаты и отметки о прохождении</h3>')
    out.append('<div class="table-wrap"><table><thead><tr><th>Вопрос</th><th>Ответ</th></tr></thead><tbody>')
    for q, a in CERTIFICATES:
        out.append("<tr><td>%s</td><td>%s</td></tr>" % (esc(q), esc(a)))
    out.append("</tbody></table></div>")
    out.append('<p class="task-teaser">Проверить себя без платформы: <a href="#academy-selfcheck">самопроверка в конце главы</a>.</p>')

    out.append('<h3 id="academy-howto">33.2. Как устроены пересказы и задания</h3>')
    out.append("<ul>"
               "<li>Для каждого урока: <strong>итог</strong> (2-4 абзаца), <strong>ключевые выводы</strong> и кнопка <strong>«Задание»</strong>.</li>"
               "<li>Задание открывается прямо на странице: шаги, критерии проверки. Ответ пишется в поле и сохраняется в браузере, рядом отметка «сдано».</li>"
               "<li>Там, где урок вёл к проверочным вопросам, ниже есть <strong>самопроверка</strong> с вариантами ответов.</li>"
               "<li>Темы уроков связаны с главами книги: каждое задание ссылается на теоретическую главу.</li>"
               "</ul>")

    out.append('<h3 id="academy-courses">33.3. Курсы</h3>')
    out.append('<div class="academy-index">')
    for c in courses:
        out.append('<section class="academy-course">')
        out.append('<h4 id="course-%s">%s</h4>' % (esc(c["slug"]), esc(c["title"])))
        if c.get("why"):
            out.append("<p>%s</p>" % esc(c["why"]))
        if c.get("src"):
            out.append('<p class="academy-src">Курс на платформе: <a href="%s" rel="noopener">%s</a></p>'
                       % (esc(c["src"]), esc(c["src"].replace("https://", ""))))
        if c.get("badge"):
            out.append('<p class="academy-badge">%s</p>' % esc(c["badge"]))
        out.append('<ul class="academy-lessons">')
        for l in c["lessons"]:
            tid = "task-%s-%s" % (c["slug"], l["page"])
            out.append('<li><a href="#%s">%s</a></li>' % (tid, esc(l["title"])))
        out.append("</ul></section>")
    out.append("</div>")

    out.append('<h3 id="academy-lessons">33.4. Уроки с заданиями</h3>')
    for ci, c in enumerate(courses, 1):
        out.append('<section class="academy-course-block">')
        out.append('<h4 id="course-block-%s">33.4.%d. %s</h4>' % (esc(c["slug"]), ci, esc(c["title"])))
        for li, l in enumerate(c["lessons"], 1):
            out.append('<div class="academy-lesson">')
            out.append('<h5 id="lesson-%s-%s">%s</h5>' % (esc(c["slug"]), esc(l["page"]), esc(l["title"])))
            for p in l.get("summary", []):
                out.append("<p>%s</p>" % esc(p))
            if l.get("points"):
                out.append("<ul>")
                for p in l["points"]:
                    out.append("<li>%s</li>" % esc(p))
                out.append("</ul>")
            if l.get("try"):
                out.append('<div class="callout try"><span class="label">Попробуйте</span>')
                for p in l["try"]:
                    out.append("<p>%s</p>" % esc(p))
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
    {"q": "Какая команда показывает, что занимает контекст?",
     "options": ["/compact", "/context", "/clear"], "answer": 1,
     "explain": "/context показывает объём и распределение контекста; /compact и /clear меняют его."},
    {"q": "Что надёжнее просьбы в CLAUDE.md?",
     "options": ["Повторить просьбу дважды", "Hook с блокировкой", "Дольше объяснять в чате"], "answer": 1,
     "explain": "Hook - это код, он срабатывает всегда; CLAUDE.md - рекомендация."},
    {"q": "Когда субагент полезен?",
     "options": ["Когда нужен только результат, а не путь к нему", "Когда каждый шаг зависит от предыдущего",
                 "Всегда"], "answer": 0,
     "explain": "Субагент прячет исследование в своём контексте и возвращает сводку."},
    {"q": "Какой режим лучше для автономного запуска в CI?",
     "options": ["Обход подтверждений", "Auto", "Ручной"], "answer": 1,
     "explain": "В Auto остаётся классификатор безопасности; обход подтверждений убирает последний предохранитель."},
    {"q": "Из чего состоит эвал?",
     "options": ["Вопрос, ответ модели, оценка человека", "Входы, ожидаемые ответы, способ оценки", "Только рубрика"], "answer": 1,
     "explain": "Три части: реалистичные входы, ожидаемые ответы и оценщик (код, модель, человек)."},
    {"q": "Если модель ниже порога, что делать сначала?",
     "options": ["Сменить на дорогую модель", "Прочитать ошибки и исправить промпт", "Уменьшить набор случаев"], "answer": 1,
     "explain": "Правка промпта дешевле смены модели и часто решает проблему."},
    {"q": "Как Claude узнаёт, какой скилл применить?",
     "options": ["По описанию в заголовке SKILL.md", "По имени папки", "По размеру файла"], "answer": 0,
     "explain": "В начале загружаются имя и описание; по ним Claude выбирает скилл."},
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
    if "--html" in sys.argv:
        path = os.path.join(HERE, "academy", "glava.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(path, len(text))
    else:
        sys.stdout.write(text)
