> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Распространённые рабочие процессы

> Пошаговые руководства по изучению кодовых баз, исправлению ошибок, рефакторингу, тестированию и другим повседневным задачам с Claude Code.

На этой странице собраны короткие рецепты для повседневной разработки. Для получения более высокоуровневого руководства по подсказкам и управлению контекстом см. [Лучшие практики](https://code.claude.com/docs/ru/best-practices.md).

На этой странице рассматриваются:

* [Рецепты подсказок](#prompt-recipes) для изучения кода, исправления ошибок, рефакторинга, тестирования, PR и документации
* [Возобновление предыдущих разговоров](#resume-previous-conversations) для того, чтобы задача могла охватывать несколько сеансов
* [Запуск параллельных сеансов с worktrees](#run-parallel-sessions-with-worktrees) для того, чтобы одновременные редактирования не конфликтовали
* [Планирование перед редактированием](#plan-before-editing) для проверки изменений перед их записью на диск
* [Делегирование исследований subagents](#delegate-research-to-subagents) для сохранения чистоты вашего основного контекста
* [Передача Claude в скрипты](#pipe-claude-into-scripts) для CI и пакетной обработки

## Рецепты подсказок

Это паттерны подсказок для повседневных задач, таких как изучение незнакомого кода, отладка, рефакторинг, написание тестов и создание PR. Каждый работает на любой поверхности Claude Code; адаптируйте формулировку к вашему проекту.

### Понимание новых кодовых баз

Для настройки Claude Code в монорепозитории или большой кодовой базе см. [Монорепозитории и большие репозитории](https://code.claude.com/docs/ru/large-codebases.md).

#### Получение быстрого обзора кодовой базы

Предположим, вы только что присоединились к новому проекту и вам нужно быстро понять его структуру.

**1. Перейдите в корневой каталог проекта**

```bash theme={null}
cd /path/to/project 
```

Замените `/path/to/project` на путь к вашему проекту.

**2. Запустите Claude Code**

```bash theme={null}
claude 
```

**3. Попросите высокоуровневый обзор**

```text wrap theme={null}
give me an overview of this codebase
```

**4. Углубитесь в конкретные компоненты**

```text wrap theme={null}
explain the main architecture patterns used here
```

```text wrap theme={null}
what are the key data models?
```

```text wrap theme={null}
how is authentication handled?
```

> [!TIP]
>
> Советы:
>
> * Начните с широких вопросов, затем сужайте до конкретных областей
> * Спросите о соглашениях кодирования и паттернах, используемых в проекте
> * Запросите глоссарий терминов, специфичных для проекта

#### Поиск релевантного кода

Предположим, вам нужно найти код, связанный с конкретной функцией или функциональностью.

**1. Попросите Claude найти релевантные файлы**

```text wrap theme={null}
find the files that handle user authentication
```

**2. Получите контекст о том, как компоненты взаимодействуют**

```text wrap theme={null}
how do these authentication files work together?
```

**3. Поймите поток выполнения**

```text wrap theme={null}
trace the login process from front-end to database
```

> [!TIP]
>
> Советы:
>
> * Будьте конкретны в том, что вы ищете
> * Используйте предметный язык из проекта
> * Установите [плагин анализа кода](https://code.claude.com/docs/ru/plugins/code-intelligence.md) для вашего языка, чтобы дать Claude точную навигацию "перейти к определению" и "найти ссылки"

***

### Эффективное исправление ошибок

Предположим, вы столкнулись с сообщением об ошибке и вам нужно найти и исправить его источник.

**1. Поделитесь ошибкой с Claude**

```text wrap theme={null}
I'm seeing an error when I run npm test
```

**2. Попросите рекомендации по исправлению**

```text wrap theme={null}
suggest a few ways to fix the @ts-ignore in user.ts
```

**3. Примените исправление**

```text wrap theme={null}
update user.ts to add the null check you suggested
```

> [!TIP]
>
> Советы:
>
> * Скажите Claude команду для воспроизведения проблемы и получите трассировку стека
> * Упомяните любые шаги для воспроизведения ошибки
> * Дайте Claude знать, является ли ошибка прерывистой или постоянной

***

### Рефакторинг кода

Предположим, вам нужно обновить старый код для использования современных паттернов и практик.

Для переноса всей кодовой базы на новый язык см. [как Anthropic проводит крупномасштабные миграции кода с помощью Claude Code](https://claude.com/blog/ai-code-migration) в блоге.

**1. Определите устаревший код для рефакторинга**

```text wrap theme={null}
find deprecated API usage in our codebase
```

**2. Получите рекомендации по рефакторингу**

```text wrap theme={null}
suggest how to refactor utils.js to use modern JavaScript features
```

**3. Примените изменения безопасно**

```text wrap theme={null}
refactor utils.js to use ES2024 features while maintaining the same behavior
```

**4. Проверьте рефакторинг**

```text wrap theme={null}
run tests for the refactored code
```

> [!TIP]
>
> Советы:
>
> * Попросите Claude объяснить преимущества современного подхода
> * Запросите, чтобы изменения сохраняли обратную совместимость при необходимости
> * Выполняйте рефакторинг небольшими, тестируемыми шагами

***

### Работа с тестами

Предположим, вам нужно добавить тесты для непокрытого кода.

**1. Определите непротестированный код**

```text wrap theme={null}
find functions in NotificationsService.swift that are not covered by tests
```

**2. Создайте каркас тестов**

```text wrap theme={null}
add tests for the notification service
```

**3. Добавьте значимые тестовые случаи**

```text wrap theme={null}
add test cases for edge conditions in the notification service
```

**4. Запустите и проверьте тесты**

```text wrap theme={null}
run the new tests and fix any failures
```

Claude может создавать тесты, которые следуют существующим паттернам и соглашениям вашего проекта. При запросе тестов будьте конкретны в отношении поведения, которое вы хотите проверить. Claude изучает ваши существующие файлы тестов, чтобы соответствовать стилю, фреймворкам и паттернам утверждений, уже используемым в проекте.

Чтобы улучшить покрытие, попросите Claude определить граничные случаи, которые вы могли пропустить. Claude может анализировать пути вашего кода и предлагать тесты для условий ошибок, граничных значений и неожиданных входных данных, которые часто упускают из виду.

***

### Создание pull requests

Вы можете создавать pull requests, попросив Claude напрямую ("create a pr for my changes"), или направить Claude пошагово:

**1. Суммируйте ваши изменения**

```text wrap theme={null}
summarize the changes I've made to the authentication module
```

**2. Создайте pull request**

```text wrap theme={null}
create a pr
```

**3. Просмотрите и уточните**

```text wrap theme={null}
enhance the PR description with more context about the security improvements
```

Чтобы найти сеанс позже, запустите `claude --from-pr 1234` с номером вашего PR, который открывает средство выбора сеанса, отфильтрованное по сеансам, связанным с этим PR, или вставьте URL PR в средство выбора [`/resume`](https://code.claude.com/docs/ru/sessions#use-the-session-picker). Claude Code связывает сеанс с PR, когда Claude создает его с помощью `gh pr create` или `glab mr create`, и когда Claude [работает над существующим PR](https://code.claude.com/docs/ru/agent-view.md#pull-request-status).

> [!TIP]
>
> Просмотрите PR, созданный Claude, перед отправкой и попросите Claude выделить потенциальные риски или соображения.

### Работа с документацией

Предположим, вам нужно добавить или обновить документацию для вашего кода.

**1. Определите недокументированный код**

```text wrap theme={null}
find functions without proper JSDoc comments in the auth module
```

**2. Создайте документацию**

```text wrap theme={null}
add JSDoc comments to the undocumented functions in auth.js
```

**3. Просмотрите и улучшите**

```text wrap theme={null}
improve the generated documentation with more context and examples
```

**4. Проверьте документацию**

```text wrap theme={null}
check if the documentation follows our project standards
```

> [!TIP]
>
> Советы:
>
> * Укажите стиль документации, который вы хотите (JSDoc, docstrings и т.д.)
> * Попросите примеры в документации
> * Запросите документацию для публичных API, интерфейсов и сложной логики

***

### Работа с заметками и папками, не содержащими код

Claude Code работает в любом каталоге. Запустите его внутри хранилища заметок, папки документации или любой коллекции файлов markdown для поиска, редактирования и переорганизации содержимого так же, как вы работаете с кодом.

Каталог `.claude/` и `CLAUDE.md` находятся рядом с каталогами конфигурации других инструментов без конфликтов. Claude читает файлы заново при каждом вызове инструмента, поэтому он видит изменения, которые вы вносите в другом приложении при следующем чтении этого файла.

***

### Работа с изображениями

Предположим, вам нужно работать с изображениями в вашей кодовой базе, и вы хотите помощь Claude в анализе содержимого изображения.

**1. Добавьте изображение в разговор**

Вы можете использовать любой из этих методов:

1. Перетащите изображение в окно Claude Code
2. Скопируйте изображение и вставьте его в CLI с помощью `Ctrl+V`, или с помощью [`Alt+V` на Windows и WSL](https://code.claude.com/docs/ru/interactive-mode#general-controls)
3. Предоставьте Claude путь к изображению, например "Analyze this image: /path/to/your/image.png"

**2. Попросите Claude проанализировать изображение**

```text wrap theme={null}
What does this image show?
```

```text wrap theme={null}
Describe the UI elements in this screenshot
```

```text wrap theme={null}
Are there any problematic elements in this diagram?
```

**3. Используйте изображения для контекста**

```text wrap theme={null}
Here's a screenshot of the error. What's causing it?
```

```text wrap theme={null}
This is our current database schema. How should we modify it for the new feature?
```

**4. Получите предложения кода из визуального содержимого**

```text wrap theme={null}
Generate CSS to match this design mockup
```

```text wrap theme={null}
What HTML structure would recreate this component?
```

> [!TIP]
>
> Советы:
>
> * Используйте изображения, когда текстовые описания были бы неясными или громоздкими
> * Включайте скриншоты ошибок, дизайны пользовательского интерфейса или диаграммы для лучшего контекста
> * Вы можете работать с несколькими изображениями в разговоре
> * Анализ изображений работает с диаграммами, скриншотами, макетами и многим другим
> * Когда Claude ссылается на изображения (например, `[Image #1]`), `Cmd+Click` (Mac) или `Ctrl+Click` (Windows/Linux) ссылку для открытия изображения в вашем средстве просмотра по умолчанию

***

### Ссылка на файлы и каталоги

Используйте @ для быстрого включения файлов или каталогов без ожидания, пока Claude их прочитает.

**1. Ссылка на один файл**

```text wrap theme={null}
Explain the logic in @src/utils/auth.js
```

Это включает содержимое файла в диалог, если оно укладывается в лимит токенов [инструмента Read](https://code.claude.com/docs/ru/tools-reference.md#read-tool-behavior), по умолчанию 25 000 токенов. Текстовый файл размером более 256 КБ не включается.

**2. Ссылка на каталог**

```text wrap theme={null}
What's the structure of @src/components?
```

**3. Ссылка на MCP ресурсы**

```text wrap theme={null}
Show me the data from @github:repos/owner/repo/issues
```

См. [MCP ресурсы](https://code.claude.com/docs/ru/mcp.md#use-mcp-resources) для подробностей.

> [!TIP]
>
> Советы:
>
> * Пути к файлам могут быть относительными или абсолютными
> * Введите `@` для открытия меню предложений пути, затем нажмите Enter или Tab для принятия выделенного пути и снова Enter для отправки сообщения
> * Ссылки на файлы @ добавляют `CLAUDE.md` в каталог файла и родительские каталоги в контекст
> * Ссылки на каталоги показывают списки файлов, а не содержимое
> * Вы можете ссылаться на несколько файлов в одном сообщении (например, "@file1.js and @file2.js")

Чтобы ссылки `@` не включали содержимое файлов и списки каталогов, задайте для [`CLAUDE_CODE_DISABLE_FILE_MENTIONS`](https://code.claude.com/docs/ru/env-vars#variables) значение `1` в вашей оболочке или в [блоке `env`](https://code.claude.com/docs/ru/env-vars#set-variables-in-settings-files) пользовательских настроек или [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md). Тогда Claude получает указанные вами пути с пометкой прочитать их с помощью своих файловых инструментов. Для этой переменной требуется Claude Code v2.1.299 или новее, и Claude Code игнорирует её в настройках проекта и локальных настройках.

Ваши [хуки `PreToolUse`](https://code.claude.com/docs/ru/hooks#pretooluse) не запускаются, когда Claude Code включает файл, на который вы ссылаетесь с помощью `@`, поскольку при этом не выполняется вызов инструмента. Если вы полагаетесь на эти хуки, чтобы контролировать, что читает Claude, заблокируйте определённые пути или запретите ссылкам `@` включать файлы:

* **Заблокируйте определённые пути**: добавьте для них [правило запрета `Read`](https://code.claude.com/docs/ru/permissions#read-and-edit). Claude Code не включает файл, которому соответствует это правило.
* **Запретите ссылкам `@` включать файлы**: задайте `CLAUDE_CODE_DISABLE_FILE_MENTIONS=1`, что не позволяет ссылкам `@` на файлы и каталоги в ваших сообщениях включать содержимое, даже для путей, которые ваши хуки не проверяют. Тогда соответствующие хуки запускаются до того, как Claude откроет указанный путь с помощью инструмента, такого как `Read`.

***

### Запуск Claude по расписанию

Предположим, вы хотите, чтобы Claude автоматически выполнял задачу на повторяющейся основе, например просматривая открытые PR каждое утро, проверяя зависимости еженедельно или проверяя сбои CI в течение ночи.

Выберите вариант планирования на основе того, где вы хотите, чтобы задача выполнялась:

| Вариант | Где выполняется | Лучше всего для |
| :- | :- | :- |
| [Облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md) | Облако, по умолчанию управляемое Anthropic | Задачи, которые должны выполняться даже когда ваш компьютер выключен. Также могут срабатывать на вызовы API или события GitHub в дополнение к расписанию. Настройте на [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Запланированные задачи рабочего стола](https://code.claude.com/docs/ru/desktop-scheduled-tasks.md) | Ваша машина, через настольное приложение | Задачи, которым нужен прямой доступ к локальным файлам, инструментам или незафиксированным изменениям. |
| [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) | Ваш конвейер CI | Задачи, связанные с событиями репозитория, такими как открытые PR, или расписания cron, которые должны находиться рядом с конфигурацией рабочего процесса. |
| [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) | Текущий сеанс CLI | Быстрый опрос во время открытого сеанса. `--resume` и `--continue` восстанавливают неистекшие циклы с фиксированным интервалом. |

> [!TIP]
>
> При написании подсказок для запланированных задач будьте явны в отношении того, что означает успех и что делать с результатами. Задача выполняется автономно, поэтому она не может задавать уточняющие вопросы. Например: "Просмотрите открытые PR с меткой `needs-review`, оставьте встроенные комментарии по любым проблемам и опубликуйте сводку в канале `#eng-reviews` Slack."

***

### Спросите Claude о его возможностях

Claude может ответить на вопросы о своих собственных функциях и ограничениях. Он ищет ответы в актуальной документации Claude Code, поэтому они не ограничены версией, которую вы используете.

#### Примеры вопросов

```text wrap theme={null}
can Claude Code create pull requests?
```

```text wrap theme={null}
how does Claude Code handle permissions?
```

```text wrap theme={null}
what skills are available?
```

```text wrap theme={null}
how do I use MCP with Claude Code?
```

```text wrap theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text wrap theme={null}
what are the limitations of Claude Code?
```

> [!NOTE]
>
> Claude предоставляет ответы на основе документации на эти вопросы. Для исполняемых примеров запустите `/powerup` для интерактивных уроков с анимированными демонстрациями, или обратитесь к конкретным разделам рабочих процессов выше.

> [!TIP]
>
> Советы:
>
> * Задавайте конкретные вопросы для получения подробных ответов
> * Claude может объяснить сложные функции, такие как интеграция MCP, конфигурации предприятия и продвинутые рабочие процессы

***

## Возобновление предыдущих разговоров

Когда задача охватывает несколько сеансов, продолжайте с того места, где вы остановились, вместо того чтобы переобъяснять контекст. Claude Code сохраняет каждый разговор локально.

```bash theme={null}
claude --continue
```

Это возобновляет самый последний сеанс в текущем каталоге; если его ещё нет, выводится `No conversation found to continue` и программа выходит. Используйте `claude --resume` для выбора из списка, или `/resume` из активного сеанса. См. [Управление сеансами](https://code.claude.com/docs/ru/sessions.md) для именования, ветвления и полного справочника средства выбора.

## Запуск параллельных сеансов с worktrees

Работайте над функцией в одном терминале, пока Claude исправляет ошибку в другом, без конфликтов редактирования. Каждый [git worktree](https://git-scm.com/docs/git-worktree) — это отдельный checkout на своей собственной ветке, созданный из существующего коммита, поэтому репозиторий должен иметь хотя бы один коммит в первую очередь.

```bash theme={null}
claude --worktree feature-auth
```

Запустите ту же команду с другим именем во втором терминале для запуска изолированной параллельной сессии. См. [Worktrees](https://code.claude.com/docs/ru/worktrees.md) для очистки, `.worktreeinclude` и поддержки VCS, не основанных на git. Для мониторинга параллельных сессий с одного экрана вместо отдельных терминалов см. [фоновые агенты](https://code.claude.com/docs/ru/agent-view.md).

## Планирование перед редактированием

Для изменений, которые вы хотите просмотреть перед их записью на диск, переключитесь в режим плана. Claude читает файлы и предлагает план, но не вносит изменения, пока вы не одобрите. Строка состояния показывает `⏸ plan mode on` во время активного режима плана.

```bash theme={null}
claude --permission-mode plan
```

Вы также можете нажать `Shift+Tab` во время сеанса до тех пор, пока строка состояния не покажет `⏸ plan mode on`. См. [Plan mode](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode) для потока одобрения и редактирования плана в вашем текстовом редакторе.

## Делегирование исследований subagents

Изучение большой кодовой базы заполняет ваш контекст чтением файлов. Делегируйте исследование, чтобы только результаты вернулись.

```text wrap theme={null}
use a subagent to investigate how our auth system handles token refresh
```

Subagent читает файлы в своём собственном контекстном окне и сообщает сводку. См. [Subagents](https://code.claude.com/docs/ru/sub-agents.md) для определения пользовательских агентов с их собственными инструментами и подсказками.

## Передача Claude в скрипты

Запустите Claude неинтерактивно для CI, pre-commit хуков или пакетной обработки.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

См. [Неинтерактивный режим](https://code.claude.com/docs/ru/headless.md) для форматов вывода, флагов разрешений и паттернов fan-out.

## Следующие шаги

> [card] [Лучшие практики](https://code.claude.com/docs/ru/best-practices.md)
>
> Паттерны для получения максимума от Claude Code

> [card] [Управление сеансами](https://code.claude.com/docs/ru/sessions.md)
>
> Возобновление, именование и ветвление разговоров

> [card] [Worktrees](https://code.claude.com/docs/ru/worktrees.md)
>
> Запуск изолированных параллельных сеансов

> [card] [Расширение Claude Code](https://code.claude.com/docs/ru/features-overview.md)
>
> Добавление skills, hooks, MCP, subagents и plugins
