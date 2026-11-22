> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Глоссарий

> Определения терминологии Claude Code. Узнайте, что означают agentic loop, compaction, CLAUDE.md, hooks, subagents, MCP и другие основные концепции.

Этот глоссарий определяет терминологию Claude Code. Каждая запись ссылается на страницу, где концепция рассматривается подробно. Для концепций уровня модели, таких как tokens, temperature и RAG, см. [глоссарий платформы](https://platform.claude.com/docs/ru/about-claude/glossary). Для терминов Claude Desktop, таких как desktop extension, MCPB и DXT, см. [Центр справки Claude](https://support.claude.com/).

## A

### AGENTS.md

Файл markdown с инструкциями проекта, которые вы пишете для AI-агентов кодирования. Если в вашем репозитории есть такой файл и нет [CLAUDE.md](#claude-md), Claude читает его как инструкции вашего проекта без необходимости добавлять второй файл. Вы можете изменить параметр **Project instructions** в `/config`, чтобы Claude читал оба файла или только `CLAUDE.md`. Прямое чтение `AGENTS.md` требует Claude Code v2.1.277 или более поздней версии. В некоторых сеансах Claude [не может читать `AGENTS.md`](https://code.claude.com/docs/ru/memory#when-agents-md-support-is-unavailable), поэтому [импортируйте его из `CLAUDE.md`](https://code.claude.com/docs/ru/memory#share-one-file-with-other-coding-tools) вместо этого.

Подробнее: [AGENTS.md](https://code.claude.com/docs/ru/memory.md#agents-md)

### Agent teams

Несколько независимых сеансов Claude Code, координируемых лидером команды, с общим списком задач и обменом сообщениями между участниками. В отличие от [subagents](#subagent), которые работают в одном сеансе и отчитываются только перед родительским агентом, члены команды имеют собственное окно контекста, и вы можете взаимодействовать с любым из них напрямую. Agent teams находятся на экспериментальном этапе и отключены по умолчанию; см. [Enable agent teams](https://code.claude.com/docs/ru/agent-teams.md#enable-agent-teams).

Подробнее: [Run agent teams](https://code.claude.com/docs/ru/agent-teams.md)

### Agentic coding

Рабочий процесс, при котором AI может автономно читать файлы, выполнять команды и вносить изменения, пока вы наблюдаете, перенаправляете или отходите в сторону, в отличие от чат-ассистентов на основе текста, которые только отвечают текстом, который вы должны применить самостоятельно. Claude Code является агентным, потому что он имеет [tools](#tool), которые позволяют ему действовать, а не только давать советы.

Подробнее: [How Claude Code works](https://code.claude.com/docs/ru/how-claude-code-works.md)

### Agentic harness

Инструменты, управление контекстом и среда выполнения, которые превращают языковую модель в способного агента кодирования. Claude Code — это harness; Claude — это модель внутри него. Harness обеспечивает доступ к файлам, выполнение shell-команд, управление разрешениями, загрузку памяти и цикл, который связывает действия вместе.

Подробнее: [How Claude Code works](https://code.claude.com/docs/ru/how-claude-code-works.md)

### Agentic loop

Цикл, через который Claude проходит для каждой задачи: сбор контекста, выполнение действия, проверка результатов и повторение до завершения. Каждое использование инструмента возвращает информацию, которая информирует следующий шаг. Вы можете прервать цикл в любой момент для перенаправления. Большинство точек расширения, включая [hooks](#hook), [skills](#skill) и [MCP](#mcp-model-context-protocol), подключаются к определенным фазам этого цикла.

Подробнее: [How Claude Code works](https://code.claude.com/docs/ru/how-claude-code-works.md#the-agentic-loop)

### Artifact

Живая интерактивная веб-страница, которую Claude Code публикует из вашего сеанса на приватный URL на claude.ai, чтобы вы могли видеть результат визуально или поделиться им вместо чтения текста терминала. Страница обновляется на месте, когда сеанс переиздается. Артефакты, которые вы создаете из Claude Code, появляются в той же галерее, что и артефакты, созданные в разговорах claude.ai. Параметры общего доступа зависят от вашего плана: см. [Share an artifact](https://code.claude.com/docs/ru/artifacts.md#share-an-artifact).

Подробнее: [Share session output as artifacts](https://code.claude.com/docs/ru/artifacts.md)

### Auto memory

Заметки, которые Claude пишет для себя на основе ваших исправлений и предпочтений, хранящиеся в каждом git-репозитории в `~/.claude/projects/`. Все worktrees одного репозитория используют один каталог auto memory. Первые 200 строк или 25 КБ индекса `MEMORY.md` загружаются в начале каждого сеанса. Auto memory — это написанный Claude аналог [CLAUDE.md](#claude-md), который пишете вы.

Подробнее: [Auto memory](https://code.claude.com/docs/ru/memory.md#auto-memory)

### Auto mode

[Режим разрешений](#permission-mode), в котором отдельная модель-классификатор проверяет действия вместо вас, поэтому Claude Code выполняет большинство из них, не спрашивая вас. Claude Code по-прежнему спрашивает вас перед действиями, которым соответствуют ваши явные правила ask. Классификатор блокирует расширение области действия, ненадежную инфраструктуру и [промпт-инъекции](#prompt-injection).

* **Claude Code v2.1.283 или более поздней версии**: авторежим является [встроенным начальным режимом разрешений](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in) для интерактивных сессий в терминале и VS Code
* **Более ранние версии**: авторежим является встроенным начальным режимом разрешений только на планах Pro, Max, Ultra и Team

Подробнее: [Eliminate prompts with auto mode](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode)

## B

### Bare mode

С флагом `--bare` Claude Code запускается без загрузки hooks, skills, пользовательских команд, subagents, установленных plugins, MCP servers, auto memory или CLAUDE.md, за исключением skills в директории, которую вы передаёте с помощью `--add-dir`. Рекомендуется для CI и скриптовых вызовов, где вам нужен одинаковый результат на каждой машине.

Подробнее: [Start faster with bare mode](https://code.claude.com/docs/ru/headless.md#start-faster-with-bare-mode)

### Bundled skills

Основанные на prompt playbooks, включённые в Claude Code, такие как `/batch`, `/code-review`, `/debug` и `/loop`. В отличие от встроенных команд, которые выполняют фиксированную логику, bundled skills дают Claude подробный prompt и позволяют ему организовать работу, поэтому они могут порождать агентов, читать файлы и адаптироваться к вашей кодовой базе.

Подробнее: [Bundled skills](https://code.claude.com/docs/ru/skills.md#bundled-skills)

## C

### Channel

[MCP server](#mcp-model-context-protocol), который отправляет события в ваш работающий сеанс, чтобы Claude мог реагировать на события, происходящие, пока вы отсутствуете в терминале. Channels могут быть двусторонними: Claude читает входящее событие и отвечает через тот же channel. Telegram, Discord и iMessage включены в исследовательский предпросмотр.

Подробнее: [Channels](https://code.claude.com/docs/ru/channels.md)

### Checkpoint

Точка восстановления, создаваемая при каждом отправляемом вами промпте, который начинает ход. Claude Code создаёт снимки файлов перед каждым редактированием, чтобы чекпоинт мог их восстановить. Нажмите `Esc` дважды или запустите `/rewind`, чтобы восстановить код, диалог или и то, и другое до более раннего момента, или чтобы резюмировать часть диалога начиная с выбранного сообщения.

Чекпоинты сохраняются вместе с диалогом, поэтому возобновлённая сессия всё ещё может вернуться к ним с помощью `/rewind`. Откат не отменяет изменения, внесённые в файл командой Bash, если только Claude уже не использовал свои инструменты редактирования файлов для этого файла в вашем диалоге.

Подробнее: [Checkpointing](https://code.claude.com/docs/ru/checkpointing.md)

### `.claude` directory

Каталог, из которого Claude Code читает конфигурацию, ограниченную проектом: settings, hooks, skills, subagents, rules и auto memory. Проект имеет `.claude/` в своём корне; ваши пользовательские значения по умолчанию находятся в `~/.claude/`.

Подробнее: [The `.claude` directory](https://code.claude.com/docs/ru/claude-directory)

### CLAUDE.md

Файл markdown с постоянными инструкциями, которые вы пишете для Claude, загружаемый в начале каждого сеанса как пользовательское сообщение после системного prompt. Поместите сюда соглашения проекта, заметки об архитектуре и правила "всегда делай X". CLAUDE.md в корне проекта сохраняется при [compaction](#compaction) и перечитывается свежим с диска после этого.

Вы можете разместить CLAUDE.md на уровне проекта в `./CLAUDE.md` или `./.claude/CLAUDE.md`, на уровне пользователя в `~/.claude/CLAUDE.md` или как [управляемую политику](#managed-settings) для вашей организации. Все обнаруженные файлы объединяются в контексте, а не переопределяют друг друга, и упорядочиваются от самой широкой области действия к наиболее конкретной. Claude Code также может загружать файлы [AGENTS.md](#agents-md) проекта вместо CLAUDE.md.

Подробнее: [CLAUDE.md files](https://code.claude.com/docs/ru/memory.md#claude-md-files)

### Cloud session

Сессия Claude Code, которая продолжает работать после того, как вы закрыли ноутбук, потому что она выполняется в облачной инфраструктуре, а не на вашем компьютере. По умолчанию этой инфраструктурой управляет Anthropic, либо это может быть [самостоятельно размещённая среда](https://code.claude.com/docs/ru/self-hosted-environments), которой управляет ваша организация. Вы запускаете такую сессию из claude.ai/code, мобильного приложения Claude, приложения Desktop с выбранным режимом **Cloud**, с помощью `claude --cloud` или [облачной запланированной задачи](https://code.claude.com/docs/ru/routines.md).

Сессия в вашем терминале, IDE или приложении Desktop с выбранным режимом **Local** — это локальная сессия; чтобы получить доступ к локальной сессии с другого устройства, используйте [Remote Control](#remote-control).

Подробнее: [Use Claude Code in the cloud](https://code.claude.com/docs/ru/claude-code-on-the-web.md)

### Command

Переиспользуемая инструкция, которую вы вызываете, введя `/name` в prompt. Встроенные команды, такие как `/clear`, `/model` и `/compact`, управляют сеансом. Вы можете определить свои собственные команды как файлы в `.claude/commands/` или установить их из [plugin](#plugin). [Skills](#skill) — это рекомендуемый способ упаковки многошаговых команд.

Два других использования этого слова не связаны: подкоманды CLI `claude`, такие как `claude mcp add`, перечисленные в [справочнике CLI](https://code.claude.com/docs/ru/cli-reference.md#cli-commands), и поле `command` записи stdio [MCP server](#mcp-server), которое указывает исполняемый файл, который Claude Code запускает для запуска сервера.

Подробнее: [Commands](https://code.claude.com/docs/ru/commands.md) · [Skills](https://code.claude.com/docs/ru/skills.md)

### Compaction

Автоматическое резюмирование вашего диалога, когда [контекстное окно](#context-window) приближается к своему пределу. CLAUDE.md в корне проекта и автоматическая память сохраняются при сжатии контекста, но инструкции, данные только в диалоге, могут не сохраниться. Запустите `/compact` для ручного запуска, опционально с фокусом, например `/compact focus on the API changes`.

Подробнее: [What survives compaction](https://code.claude.com/docs/ru/context-window.md#what-survives-compaction) · [When context fills up](https://code.claude.com/docs/ru/how-claude-code-works.md#when-context-fills-up) · [When Claude Code compacts a conversation you leave idle](https://code.claude.com/docs/ru/settings-reference.md#idlecompaction)

### Connector

[MCP server](#mcp-server), добавленный в вашу учётную запись claude.ai, а не настроенный в Claude Code. Когда вы входите в Claude Code с этой учётной записью, ваши connectors появляются в `/mcp` рядом с серверами, которые вы добавили локально. Организации также могут предоставлять connectors и устанавливать элементы управления для каждого tool на них.

Подробнее: [Use MCP servers from claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai)

### Context window

Рабочая память для сеанса, содержащая историю разговора, содержимое файлов, выходы команд, CLAUDE.md, auto memory, загруженные skills и системные инструкции. По мере работы контекст заполняется до [compaction](#compaction), который его резюмирует. Запустите `/context`, чтобы увидеть, что использует пространство. Для базовой концепции модели см. [глоссарий платформы](https://platform.claude.com/docs/ru/about-claude/glossary#context-window).

Подробнее: [Explore the context window](https://code.claude.com/docs/ru/context-window.md)

## D

### Dispatch

Инициируемый телефоном маршрутизатор задач, который запускает сессию Claude Code в приложении Desktop, когда вы отправляете задачу кодирования из мобильного приложения Claude. Ваш промпт автоматически направляется к нужному инструменту. Доступно на планах Pro, Max и Ultra.

Подробнее: [Sessions from Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch)

## E

### Effort level

Параметр, который управляет адаптивным рассуждением, позволяя модели решать, нужно ли и сколько думать на каждом шаге. Более высокий effort означает больше thinking tokens и более глубокое рассуждение; более низкий effort быстрее и дешевле. Effort поддерживается на Fable моделях, на Opus 4.6 и более поздних версиях, на Sonnet 4.6 и более поздних версиях, а также на Haiku 5.5.

Подробнее: [Adjust effort level](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level)

### Extended thinking

Видимое пошаговое рассуждение, которое модель выполняет перед ответом. Вы можете отрегулировать его с помощью [effort level](#effort-level), или ограничить thinking tokens с помощью `MAX_THINKING_TOKENS` на моделях с фиксированным бюджетом thinking. Thinking появляется серым курсивным текстом в терминале.

Подробнее: [Use extended thinking](https://code.claude.com/docs/ru/model-config.md#extended-thinking)

## F

### Frontmatter

Блок параметров YAML в самом начале файла Markdown, между открывающей строкой `---` и закрывающей строкой `---`. Skills, subagents, output styles и rules читают свою конфигурацию из frontmatter, например `description` skill или `tools` subagent, и рассматривают всё после закрывающей `---` как инструкции. Открывающая `---` должна быть первой строкой файла. Каждый тип файла принимает свой собственный набор полей.

Узнайте больше: [Skill frontmatter](https://code.claude.com/docs/ru/skills.md#frontmatter-reference), [Subagent frontmatter](https://code.claude.com/docs/ru/sub-agents.md#supported-frontmatter-fields), [Output style frontmatter](https://code.claude.com/docs/ru/output-styles.md#frontmatter), [Rule frontmatter](https://code.claude.com/docs/ru/memory.md#rules-frontmatter-reference)

## H

### Hook

Определённый пользователем обработчик, который выполняется автоматически в определённой точке жизненного цикла Claude Code, например перед запуском tool, после редактирования файла или при запуске сеанса. Обработчики могут быть shell-командой, HTTP endpoint, MCP tool, LLM prompt или subagent. Hooks являются детерминированными: они срабатывают в фиксированных точках жизненного цикла, а не по усмотрению модели.

Конфигурация hook имеет три уровня:

* **Hook event**: точка жизненного цикла
* **Matcher**: фильтрует, какие события его срабатывают
* **Hook handler**: что запускается

Подробнее: [Get started with hooks](https://code.claude.com/docs/ru/hooks-guide.md) · [Hooks reference](https://code.claude.com/docs/ru/hooks.md)

## M

### Managed settings

Параметры, применяемые организацией IT или DevOps, доставляемые с серверов Anthropic через консоль администратора или развёрнутые на устройствах по пути уровня ОС вне `~/.claude`. Пользователи и параметры проекта не могут переопределять управляемые параметры. Доставка, управляемая сервером, применяется на [подходящих конфигурациях](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability); см. [Соображения безопасности](https://code.claude.com/docs/ru/server-managed-settings.md#security-considerations). Используйте это для политик безопасности, требований соответствия или стандартизированного инструментария на всём парке.

Подробнее: [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) · [Settings files](https://code.claude.com/docs/ru/settings.md#where-settings-live)

### MCP (Model Context Protocol)

Открытый стандарт для подключения инструментов ИИ к внешним источникам данных и сервисам. MCP servers дают Claude новые tools для Slack, Jira, баз данных, браузеров и сотен других интеграций. Вы подключаете servers через `/mcp` или добавляя их в `.mcp.json`. Для самого протокола см. [глоссарий платформы](https://platform.claude.com/docs/ru/about-claude/glossary#mcp-model-context-protocol).

Подробнее: [Model Context Protocol](https://code.claude.com/docs/ru/mcp.md)

### MCP server

Программа, которая предоставляет Claude tools, prompts или ресурсы через [MCP](#mcp-model-context-protocol). Вы добавляете servers с помощью `claude mcp add`, в `.mcp.json`, через [plugin](#plugin) или как claude.ai [connector](#connector). Локальный stdio server запускается как процесс, который Claude Code запускает из полей `command` и `args` его конфигурации, которые не имеют ничего общего с [commands](#command), которые вы вводите в prompt.

Подробнее: [Model Context Protocol](https://code.claude.com/docs/ru/mcp.md)

### MCP Tool Search

Механизм сохранения контекста, который откладывает схемы MCP tool до необходимости. Только имена tool загружаются при запуске; Claude получает полную схему по требованию, когда решает использовать определённый tool. Это предотвращает потребление большого контекста неиспользуемыми MCP servers.

Подробнее: [Scale with MCP Tool Search](https://code.claude.com/docs/ru/mcp.md#scale-with-mcp-tool-search)

## N

### Non-interactive mode

Режим, который выполняет один prompt и выходит без интерактивного сеанса, вызываемый с `-p` или `--print`. Используется для CI, скриптов и piping. Запуск по-прежнему сохраняется как возобновляемый сеанс, если вы не передадите `--no-session-persistence`. [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) — это эквивалент Python и TypeScript. Ранее называлось headless mode.

Подробнее: [Run Claude Code programmatically](https://code.claude.com/docs/ru/headless.md)

## O

### Output style

Конфигурация, которая изменяет инструкции, которые Claude Code дает Claude, для установки поведения ответа, тона или формата. В отличие от [CLAUDE.md](#claude-md), который добавляет контекст проекта наряду с инструкциями Claude Code по умолчанию, пользовательский стиль вывода добавляет собственные инструкции и может исключить инструкции по разработке программного обеспечения по умолчанию.

Подробнее: [Output styles](https://code.claude.com/docs/ru/output-styles.md)

## P

### Permission mode

Базовое поведение одобрения для сеанса. Переключайтесь с `Shift+Tab` в CLI или используйте селектор режима в VS Code, Desktop и claude.ai. Доступные режимы: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk` и `bypassPermissions`.

Режим `default` обозначен как Manual в CLI и в расширениях VS Code и JetBrains, и Claude Code принимает `manual` как псевдоним для этого значения.

Подробнее: [Выберите режим разрешений](https://code.claude.com/docs/ru/permission-modes.md)

### Permission rule

Запись settings, которая разрешает, спрашивает или отрицает вызов tool на основе имени tool и шаблона аргумента. Правила оцениваются deny→ask→allow, первое совпадение побеждает. Permission rules — это детальные элементы управления, наложенные на более широкий [permission mode](#permission-mode).

Подробнее: [Настройте разрешения](https://code.claude.com/docs/ru/permissions.md)

### Plan mode

[permission mode](#permission-mode), где Claude исследует и предлагает изменения без редактирования ваших исходных файлов. Он может читать, искать и выполнять команды исследования, затем представляет план для одобрения перед тем, как что-либо трогать. Войдите в plan mode с `/plan` или нажав `Shift+Tab`.

Подробнее: [Анализируйте перед редактированием с помощью plan mode](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode)

### Plugin

Пакет skills, hooks, subagents и MCP servers, упакованный как единица установки. Plugin skills имеют пространство имён как `plugin-name:skill-name`, поэтому несколько plugins сосуществуют. Распределяйте plugins по командам через [marketplace](https://code.claude.com/docs/ru/plugins/overview.md).

Подробнее: [Plugins](https://code.claude.com/docs/ru/plugins/overview.md)

### Project trust

Диалог принятия каталога перед загрузкой Claude Code его конфигурации. Принятие сохраняется для каждого каталога проекта, за исключением вашего домашнего каталога, где доверие сохраняется только для текущего сеанса и приглашение появляется снова при каждом запуске. До тех пор, пока вы не доверяете каталогу, Claude Code удерживает некоторое содержимое, которое его репозиторий предоставляет, такое как правила разрешений проекта и marketplaces из `.claude/settings.json`. [Что запускается перед тем, как вы доверяете папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) перечисляет каждый вид содержимого, включая то, что запускает сеанс `-p` без диалога.

Подробнее: [Каталог `.claude`](https://code.claude.com/docs/ru/claude-directory)

### Prompt injection

Враждебные инструкции, встроенные в файл, веб-страницу или результат инструмента, которые пытаются направить Claude к действиям, о которых вы не просили. Защита Claude Code включает систему разрешений, обнаружение инъекций команд и проверку доверия. В [авторежиме](#auto-mode) серверная проверка сканирует результаты инструментов на наличие подозрительного содержимого, а классификатор проверяет действия.

Подробнее: [Защититесь от prompt injection](https://code.claude.com/docs/ru/security.md#protect-against-prompt-injection)

## R

### Remote Control

Способ продолжить локальный сеанс Claude Code с вашего телефона или браузера через claude.ai. Ваш код и файлы остаются на вашей машине; интерфейс является удалённым. Отличается от [облачного сеанса](https://code.claude.com/docs/ru/claude-code-on-the-web.md), который работает в облачной песочнице.

Подробнее: [Remote Control](https://code.claude.com/docs/ru/remote-control.md)

### Rules

Модульные файлы инструкций в `.claude/rules/`, которые загружаются вместе с CLAUDE.md. Правило может быть ограничено по пути с помощью YAML frontmatter `paths:`, поэтому оно загружается только тогда, когда Claude читает, записывает или редактирует соответствующий файл, сохраняя контекст компактным до тех пор, пока оно не станет релевантным.

Подробнее: [Organize rules with `.claude/rules/`](https://code.claude.com/docs/ru/memory#organize-rules-with-claude/rules/)

## S

### Sandboxing

Изоляция файловой системы и сети на уровне ОС для инструмента Bash. Команды выполняются внутри границы, которую вы определяете заранее. Изоляция в песочнице — это отдельный уровень, независимый от [правил разрешений](#permission-rule).

Подробнее: [Изоляция в песочнице](https://code.claude.com/docs/ru/sandboxing.md)

### Session

Диалог, привязанный к вашему текущему каталогу, с собственным независимым [контекстным окном](#context-window). Сессии можно возобновить с помощью `claude -c`, разветвить с помощью `--fork-session`, чтобы сохранить историю под новым ID сессии, или запускать параллельно в разных терминалах. Команда `/clear` начинает новую сессию; предыдущая остаётся сохранённой и доступна через `/resume`. Транскрипт каждой сессии хранится в `~/.claude/projects/`.

Подробнее: [Работа с сессиями](https://code.claude.com/docs/ru/how-claude-code-works.md#work-with-sessions)

### Settings layers

Иерархия, из которой Claude Code считывает конфигурацию. В порядке приоритета от высшего к низшему уровни таковы: [управляемая политика](#managed-settings), настройки, переданные с флагом `--settings`, локальные настройки в `.claude/settings.local.json`, настройки проекта в `.claude/settings.json` и пользовательские настройки в `~/.claude/settings.json`. Большинство списков, например `permissions.allow`, [объединяются между файлами](https://code.claude.com/docs/ru/settings.md#lists-merge-instead-of-overriding). См. [Приоритет настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence).

Подробнее: [Файлы настроек](https://code.claude.com/docs/ru/settings.md#where-settings-live)

### Skill

Файл `SKILL.md`, содержащий инструкции, знания или рабочий процесс, который Claude добавляет в свой набор инструментов. Claude загружает скилл автоматически, когда это уместно, или вы вызываете его напрямую с помощью `/skill-name`. Скиллы следуют открытому стандарту Agent Skills; Claude Code расширяет его управлением вызовом и выполнением в субагентах.

Скиллы — это рекомендуемая замена пользовательских команд. Файл `.claude/commands/deploy.md` и файл `.claude/skills/deploy/SKILL.md` оба создают `/deploy` и работают одинаково; существующие файлы команд продолжают работать.

Подробнее: [Расширение возможностей Claude с помощью скиллов](https://code.claude.com/docs/ru/skills.md)

### Subagent

Специализированный ИИ-ассистент, который работает в собственном контекстном окне с пользовательским системным промптом, определённым доступом к инструментам и независимыми разрешениями. Он работает над делегированной задачей и возвращает сводку в основной диалог. Используйте субагентов, чтобы крупные исследования не занимали ваш основной контекст, или для параллельных исследований. Субагент остаётся внутри сессии, которая его создала. Чтобы передавать результаты между отдельными сессиями, которые вы запускаете сами, используйте [обмен сообщениями между сессиями](https://code.claude.com/docs/ru/cross-session-messaging.md).

Встроенные субагенты включают Explore, Plan и general-purpose.

Подробнее: [Создание пользовательских субагентов](https://code.claude.com/docs/ru/sub-agents.md)

### Surface

Любое место, где вы работаете с Claude Code: CLI, VS Code, JetBrains, Desktop или claude.ai. Все интерфейсы используют один и тот же движок. Сессии на вашем компьютере читают ваш локальный CLAUDE.md, настройки и скиллы; [облачные сессии](https://code.claude.com/docs/ru/cloud-environments.md#what-carries-over-from-your-setup) начинаются со свежего клона вашего репозитория и не читают `~/.claude/` на вашем компьютере. Slack и расширение Chrome — это интеграции, которые подключаются к интерфейсу, а не самостоятельные интерфейсы.

Подробнее: [Платформы и интеграции](https://code.claude.com/docs/ru/platforms.md)

### System prompt

Инструкции, которые Claude Code отправляет перед вашим диалогом в каждом запросе: они описывают, как Claude использует инструменты, как безопасно себя ведёт и как форматирует свои ответы. Вы можете дополнить системный промпт с помощью `--append-system-prompt` или заменить его с помощью `--system-prompt`. Системный промпт — это первый уровень [кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#how-the-cache-is-organized).

Ваши файлы [CLAUDE.md](#claude-md) и инструкции вашего [стиля вывода](#output-style) не входят в системный промпт. Claude Code передаёт их в диалоге как [системные напоминания](#system-reminder).

Подробнее: [Флаги системного промпта](https://code.claude.com/docs/ru/cli-reference.md#system-prompt-flags)

### System reminder

Сообщение, которое Claude Code как [агентная обвязка](#agentic-harness) добавляет в диалог, чтобы дать Claude контекст. Вы не отправляете системные напоминания сами. Claude Code вставляет их по ходу сессии, например при запуске сессии или когда хук возвращает текст. Claude читает их вместе с вашими сообщениями. Всё перечисленное ниже поступает к Claude в виде системных напоминаний:

* Ваши файлы [CLAUDE.md](#claude-md)
* Инструкции вашего [стиля вывода](#output-style)
* Текст, который [хук](#hook) возвращает как `additionalContext`
* Список доступных [скиллов](#skill)
* Уведомление о том, что файл, который Claude ранее редактировал, с тех пор изменился на диске
* Строки атрибуции коммитов и pull request

В залогированном запросе API системное напоминание отображается обёрнутым в теги `<system-reminder>` внутри пользовательского сообщения, а на некоторых моделях — как отдельное сообщение с ролью `system`.

Подробнее: [Контекст, который Claude Code добавляет вне системного промпта](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#context-claude-code-adds-outside-the-system-prompt)

## T

### Teleport

Команда, `/teleport`, которая вытягивает облачный сеанс Claude Code в ваш локальный терминал. Claude получает ветку, загружает историю разговора и возобновляет с последнего состояния облачного сеанса. Обратное направление — `--cloud`, которое отправляет локальную задачу для запуска в облаке.

Подробнее: [Продолжение облачной сессии в терминале](https://code.claude.com/docs/ru/claude-code-on-the-web.md#from-cloud-to-terminal)

### Tool

Действие, которое может предпринять Claude: прочитать файл, отредактировать код, выполнить shell-команду, поискать в веб-сети, порождать subagent. Tools — это то, что делает Claude Code agentic. Без них Claude может только отвечать текстом. Каждое использование tool возвращает результат, который информирует следующее решение Claude в [agentic loop](#agentic-loop).

Подробнее: [Tools available to Claude](https://code.claude.com/docs/ru/tools-reference.md)

### Transcript

Сохранённая запись [session](#session). Разговор — это то, что вы и Claude обмениваете; transcript — это тот же разговор, сохранённый как файл, по умолчанию в `~/.claude/projects/<project>/<session-id>.jsonl`. Claude Code читает файл обратно, когда вы возобновляете, что позволяет разговору продолжаться после завершения сеанса. Для просмотра того же разговора на экране см. [transcript viewer](https://code.claude.com/docs/ru/interactive-mode.md#transcript-viewer).

Подробнее: [Where transcripts are stored](https://code.claude.com/docs/ru/sessions.md#where-transcripts-are-stored)

### Turn

Один полный ответ от Claude в рамках [session](#session). Turn начинается, когда вы отправляете сообщение, и заканчивается, когда Claude завершает ответ, с любым количеством вызовов [tool](#tool) между ними. [Stop hooks](#hook) срабатывают в конце каждого turn. Session состоит из множества turn, и [agentic loop](#agentic-loop) описывает, что происходит внутри одного.

Подробнее: [How Claude Code works](https://code.claude.com/docs/ru/how-claude-code-works.md#the-agentic-loop)

## V

### Verification loop

Как сессия узнаёт, что работа действительно выполнена, вместо того чтобы принимать результат, который лишь выглядит правдоподобно. Вы даёте Claude проверку, которую он может запустить, такую как набор тестов, сборка или сравнение скриншотов, и Claude повторяет попытки до тех пор, пока проверка не пройдёт, вместо того чтобы остановиться после одной попытки. Цикл проверки — это предварительное требование для [`/goal`](https://code.claude.com/docs/ru/goal), автоматических запусков и [динамических рабочих процессов](https://code.claude.com/docs/ru/workflows.md): без него единственное, что решает, что агент закончил, — это сам агент.

Подробнее: [Дайте Claude проверку, которую он может запустить](https://code.claude.com/docs/ru/best-practices.md#give-claude-a-check-to-run)

## W

### Worktree isolation

Режим изоляции, который запускает Claude в отдельном git worktree в `.claude/worktrees/`, включаемый флагом `-w` или `isolation: worktree` в конфигурации субагента. Изменения остаются на отдельной ветке в отдельном каталоге, поэтому каждый из параллельных агентов редактирует собственную копию файлов.

Подробнее: [Запуск параллельных сеансов с git worktrees](https://code.claude.com/docs/ru/worktrees.md)

***

## Deprecated and renamed terms

Эти термины появляются в старых документах, постах блога и содержимом сообщества. Используйте текущее имя при поиске на этом сайте.

| Old term | Now called | Notes |
| - | - | - |
| Headless mode | [Non-interactive mode](#non-interactive-mode) | Same `-p` flag, same behavior |
| Web session; "Claude Code on the web" as the name for any cloud session | [Cloud session](#cloud-session) | "Claude Code on the web" now names only the browser surface at claude.ai/code |
| Custom commands | [Skills](#skill) | `.claude/commands/` files still work |
| Slash commands | Commands | "Slash" dropped from product copy |
