> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Изучите директорию .claude

> Где Claude Code читает CLAUDE.md, settings.json, hooks, skills, commands, subagents, workflows, rules и auto memory. Изучите директорию .claude в вашем проекте и ~/.claude в вашей домашней директории.

Claude Code читает инструкции, параметры, skills, subagents и память из директории вашего проекта и из `~/.claude` в вашей домашней директории. Зафиксируйте файлы проекта в git, чтобы поделиться ими с вашей командой; файлы в `~/.claude` — это личная конфигурация, которая применяется ко всем вашим проектам.

На Windows `~/.claude` разрешается в `%USERPROFILE%\.claude`. Если вы зададите [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars), каждый путь `~/.claude` на этой странице будет находиться в этом каталоге. То же относится к `.claude.json`, который в противном случае находится в `~/.claude.json`.

Большинство пользователей редактируют только `CLAUDE.md` и `settings.json`. Если ваш репозиторий уже содержит `AGENTS.md` для других агентов кодирования, Claude Code [может читать его](https://code.claude.com/docs/ru/memory.md#agents-md) вместо `CLAUDE.md`. Остальная часть директории опциональна: добавляйте skills, rules или subagents по мере необходимости.

## Изучите директорию

Нажимайте на файлы в дереве, чтобы увидеть, что каждый из них делает, когда он загружается и пример.

Configuration files

**`CLAUDE.md`**

**When it loads**: Загружается в контекст при запуске сессии

Инструкции для конкретного проекта, определяющие, как Claude работает в этом репозитории. Разместите здесь свои соглашения, часто используемые команды и архитектурный контекст.

**`.mcp.json`**

**When it loads**: В интерактивных сессиях MCP-серверы, которые вы [одобрили](https://code.claude.com/docs/ru/mcp.md#project-scope), загружаются в начале сессии. Схемы инструментов по умолчанию откладываются и загружаются по требованию через [поиск инструментов](https://code.claude.com/docs/ru/mcp.md#scale-with-mcp-tool-search)

Настраивает серверы Model Context Protocol (MCP), которые дают Claude доступ к внешним инструментам: базам данных, API, браузерам и многому другому. Этот файл содержит MCP-серверы уровня проекта, которые использует вся ваша команда. Личные серверы, которые вы хотите оставить только для себя, размещаются в `~/.claude.json`.

**`.worktreeinclude`**

**When it loads**: Читается, когда Claude создаёт [git worktree](https://code.claude.com/docs/ru/worktrees.md) через `--worktree`, инструмент `EnterWorktree` или `isolation: worktree` субагента

Перечисляет игнорируемые git файлы, которые нужно скопировать из основного репозитория в каждый новый worktree. Worktree — это чистые checkout'ы, поэтому неотслеживаемые файлы, такие как `.env`, по умолчанию отсутствуют. Шаблоны здесь используют синтаксис `.gitignore`. Копируются только файлы, которые соответствуют шаблону и при этом игнорируются git.

**`.claude/`**

Настройки проекта, правила, скиллы, субагенты и другая конфигурация. Если вы используете git, добавляйте большинство этих файлов в коммиты, чтобы ваша команда имела к ним общий доступ, а личные файлы, такие как `settings.local.json`, не включайте в коммиты.

**`.claude/settings.json`**

**When it loads**: Читается при запуске сессии. Большинство изменений [применяются к текущей сессии](https://code.claude.com/docs/ru/settings.md#when-edits-take-effect)

Настройки, которые Claude Code применяет напрямую. Разрешения определяют, какие команды и инструменты может использовать Claude; хуки запускают ваши скрипты в определённые моменты сессии. В отличие от CLAUDE.md, который Claude читает как рекомендации, эти настройки применяются принудительно, независимо от того, следует ли им Claude.

В [приоритете настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence) этот файл стоит выше `~/.claude/settings.json` и ниже `.claude/settings.local.json`, флага `--settings` и управляемых настроек. Для большинства ключей с одним значением, таких как `model`, Claude Code использует значение с наивысшим приоритетом. Большинство списков, таких как `permissions.allow`, [объединяются между файлами](https://code.claude.com/docs/ru/settings.md#lists-merge-instead-of-overriding).

**`.claude/settings.local.json`**

**When it loads**: Читается при запуске сессии. Большинство изменений [применяются к текущей сессии](https://code.claude.com/docs/ru/settings.md#when-edits-take-effect)

Ваши личные настройки для этого проекта. Тот же формат JSON, что и у `settings.json`; файл добавляется в gitignore, когда Claude Code сохраняет в него настройку.

В [приоритете настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence) этот файл стоит выше `.claude/settings.json` и ниже флага `--settings` и управляемых настроек. Для большинства ключей с одним значением, таких как `model`, Claude Code использует значение с наивысшим приоритетом. Большинство списков, таких как `permissions.allow`, [объединяются между файлами](https://code.claude.com/docs/ru/settings.md#lists-merge-instead-of-overriding).

**`.claude/rules/`**

**When it loads**: Правила без frontmatter `paths:` загружаются при запуске сессии. Правила с `paths:` загружаются, когда Claude читает, записывает или редактирует соответствующий файл

Инструкции проекта, разделённые на тематические файлы. Как и CLAUDE.md, правила — это рекомендации, которые Claude Code не применяет принудительно. Для принудительного поведения используйте [хуки](https://code.claude.com/docs/ru/hooks.md) или [разрешения](https://code.claude.com/docs/ru/permissions.md).

**`.claude/skills/`**

**When it loads**: Вызывается с помощью `/skill-name` или когда Claude сопоставляет задачу со скиллом

Каждый скилл — это папка с файлом `SKILL.md` и любыми необходимыми вспомогательными файлами. По умолчанию скилл могут вызывать как вы, так и Claude. Используйте [frontmatter](https://code.claude.com/docs/ru/skills.md#frontmatter-reference), чтобы управлять этим: `disable-model-invocation: true`, чтобы Claude не мог самостоятельно вызвать скилл, такой как `/deploy`, или `user-invocable: false`, чтобы скилл мог вызывать только Claude.

**`.claude/commands/`**

**When it loads**: Вызывается с помощью `/command-name` или когда Claude сопоставляет задачу с командой

Содержит однофайловые команды: промпт, сохранённый как `.claude/commands/deploy.md`, запускается как `/deploy`. Для новой команды используйте [скилл](#ce-skills), который может включать справочную документацию, шаблоны или скрипты вместе с промптом.

**`.claude/output-styles/`**

**When it loads**: Читается при запуске в терминале, поэтому перезапустите Claude Code после добавления или редактирования стиля

Каждый Markdown-файл определяет [стиль вывода](https://code.claude.com/docs/ru/output-styles.md#how-output-styles-work) — набор инструкций, который изменяет то, как работает Claude. Разместите стиль здесь, если ваша команда использует его совместно, например режим ревью, которым пользуются все. О том, как выбрать стиль, см. [`~/.claude/output-styles/`](#ce-global-output-styles).

**`.claude/agents/`**

**When it loads**: Каждый субагент работает в собственном контекстном окне, когда вы или Claude его вызываете

Каждый Markdown-файл с frontmatter `name` и `description` определяет субагента с собственным системным промптом, доступом к инструментам и, при необходимости, собственной моделью. Полезно для параллельной работы или изолированных задач.

**`.claude/workflows/`**

**When it loads**: Загружается при запуске, когда [рабочие процессы включены](https://code.claude.com/docs/ru/workflows.md). Каждый сохранённый рабочий процесс запускается как команда `/<name>`

Каждый файл `.js` — это [динамический рабочий процесс](https://code.claude.com/docs/ru/workflows.md): скрипт, который среда выполнения исполняет для запуска и координации множества субагентов. Чтобы добавить его, попросите Claude написать рабочий процесс, затем выполните `/workflows` в сессии и сохраните его здесь.

**`.claude/agent-memory/`**

**When it loads**: Первые 200 строк файла `MEMORY.md` субагента, но не более 25 КБ, загружаются в его системный промпт при запуске субагента

Субагенты с [`memory: project`](https://code.claude.com/docs/ru/sub-agents#enable-persistent-memory) во frontmatter получают здесь выделенную директорию памяти, пока включена [автоматическая память](https://code.claude.com/docs/ru/memory.md#auto-memory). Каждый субагент читает и записывает собственный `MEMORY.md`, отдельный от автоматической памяти вашей основной сессии в `~/.claude/projects/`.

**`.claude/agent-memory/<agent-name>/MEMORY.md`**

**When it loads**: Первые 200 строк, но не более 25 КБ, загружаются в системный промпт субагента при его запуске

Индекс заметок, сохранённых субагентом. Субагент сам создаёт и обновляет этот файл в том же формате, что и индекс вашей основной [автоматической памяти](https://code.claude.com/docs/ru/memory.md#storage-location).

**`~/.claude.json`**

**When it loads**: Читается при запуске сессии для получения ваших предпочтений и MCP-серверов. Claude Code записывает в него изменения, когда вы меняете [глобальный параметр конфигурации](https://code.claude.com/docs/ru/settings-reference.md#global-config-settings) в `/config` или доверяете папке проекта

Содержит данные учётной записи, решения о доверии для каждого проекта, ваши личные MCP-серверы и переключатели интерфейса.

**`~/.claude/`**

Глобальный аналог директории [`.claude/`](#ce-dot-claude) вашего проекта. Файлы конфигурации в этой директории применяются к вам во всех проектах на этом компьютере.

**`~/.claude/CLAUDE.md`**

**When it loads**: Загружается при запуске сессии в каждом проекте на этом компьютере

Ваш глобальный файл инструкций. Загружается вместе с CLAUDE.md проекта. Если они противоречат друг другу, Claude может следовать любому из них. Храните в этом файле только предпочтения, которые применяются везде: стиль ответов, формат коммитов, личные соглашения.

**`~/.claude/settings.json`**

**When it loads**: Читается при запуске сессии. Большинство изменений [применяются к текущей сессии](https://code.claude.com/docs/ru/settings.md#when-edits-take-effect)

Тот же формат, что и у `settings.json` проекта: разрешения, хуки, модель и переменные окружения. Разместите здесь настройки, которые нужны вам в каждом проекте, например разрешающие правила, предпочитаемую модель или хук уведомлений.

В [приоритете настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence) этот файл стоит ниже файлов настроек проекта, флага `--settings` и управляемых настроек. Для большинства ключей с одним значением, таких как `model`, Claude Code использует значение с наивысшим приоритетом. Большинство списков, таких как `permissions.allow`, [объединяются между файлами](https://code.claude.com/docs/ru/settings.md#lists-merge-instead-of-overriding).

**`~/.claude/keybindings.json`**

**When it loads**: Читается при запуске сессии и перезагружается на лету при редактировании файла

Переназначайте сочетания клавиш в интерактивном CLI. Выполните `/keybindings` в сессии, чтобы создать или открыть этот файл. Прежде чем выбрать клавишу, проверьте [зарезервированные сочетания клавиш](https://code.claude.com/docs/ru/keybindings.md#reserved-shortcuts).

**`~/.claude/themes/`**

**When it loads**: Читается при запуске сессии и [перезагружается на лету](https://code.claude.com/docs/ru/terminal-config.md#create-a-custom-theme) при изменении файлов. Отображается в `/theme`

Каждый файл `.json` определяет пользовательскую цветовую тему: встроенный пресет `base` плюс карту `overrides` с цветовыми токенами. Выполните `/theme` в сессии, чтобы создать тему, или напишите JSON самостоятельно. При выборе пользовательской темы в качестве предпочитаемой темы сохраняется `custom:<slug>`.

**`~/.claude/projects/`**

**When it loads**: Файл `memory/MEMORY.md` текущего проекта загружается при запуске сессии, пока включена автоматическая память. Перечисленные в нём тематические файлы читаются по требованию

Содержит [автоматическую память](https://code.claude.com/docs/ru/memory.md#auto-memory) — заметки, которые Claude сохраняет между сессиями: вашу роль и предпочтения, ваши исправления, решения по проекту и то, где найти информацию за пределами проекта. Каждый проект получает собственную директорию памяти, привязанную к пути репозитория.

**`~/.claude/projects/<project>/memory/MEMORY.md`**

**When it loads**: Первые 200 строк, но не более 25 КБ, загружаются при запуске сессии, пока включена [автоматическая память](https://code.claude.com/docs/ru/memory.md#auto-memory)

Индекс, указывающий на тематические файлы с подробностями. Claude создаёт и обновляет этот файл в процессе работы. Вы можете редактировать или удалить его.

**`~/.claude/projects/<project>/memory/user_role.md`**

**When it loads**: Claude читает этот файл, когда возникает связанная задача

Пример тематического файла. Claude сохраняет каждое воспоминание в отдельном тематическом файле, выбирает имя файла и добавляет его в `MEMORY.md`.

**`~/.claude/rules/`**

**When it loads**: Правила без frontmatter `paths:` загружаются при запуске сессии. Правила с `paths:` загружаются, когда Claude читает, записывает или редактирует соответствующий файл

Тот же формат, что и у [`.claude/rules/`](#ce-rules) проекта, но применяется к каждому проекту на этом компьютере. Используйте для соглашений, которые нужны вам во всей вашей работе, например личного стиля кода или формата сообщений коммитов.

**`~/.claude/skills/`**

**When it loads**: Вызывается с помощью `/skill-name` или когда Claude сопоставляет задачу со скиллом

Скиллы, созданные вами для себя и доступные во всех ваших проектах на этом компьютере. Тот же формат, что и у [`.claude/skills/`](#ce-skills) проекта.

**`~/.claude/commands/`**

**When it loads**: Вызывается с помощью `/command-name` или когда Claude сопоставляет задачу с командой

Тот же формат, что и у [`.claude/commands/`](#ce-commands) проекта; доступны во всех ваших проектах на этом компьютере.

**`~/.claude/output-styles/`**

**When it loads**: Читается при запуске в терминале, поэтому перезапустите Claude Code после добавления или редактирования стиля

Каждый Markdown-файл определяет [стиль вывода](https://code.claude.com/docs/ru/output-styles.md#how-output-styles-work) — набор инструкций, который изменяет то, как работает Claude. Используйте стиль, чтобы адаптировать Claude Code для задач за пределами программирования или добавить режимы обучения или ревью.

Выберите встроенный или пользовательский стиль с помощью `/output-style` или `/config` в сессии либо с помощью ключа `outputStyle` в настройках. Стили здесь доступны в каждом проекте на этом компьютере. Если у стиля проекта то же имя, Claude Code использует стиль проекта.

**`~/.claude/agents/`**

**When it loads**: Каждый субагент работает в собственном контекстном окне, когда вы или Claude его вызываете

Субагенты, определённые здесь, доступны во всех ваших проектах на этом компьютере. Тот же формат, что и у [`.claude/agents/`](#ce-agents) проекта.

**`~/.claude/workflows/`**

**When it loads**: Загружается при запуске, когда [рабочие процессы включены](https://code.claude.com/docs/ru/workflows.md). Каждый сохранённый рабочий процесс запускается как команда `/<name>`

Скрипты рабочих процессов, сохранённые здесь, доступны во всех ваших проектах на этом компьютере. Рабочий процесс проекта с тем же именем в `.claude/workflows/` имеет приоритет.

**`~/.claude/agent-memory/`**

**When it loads**: Первые 200 строк файла `MEMORY.md` субагента, но не более 25 КБ, загружаются в его системный промпт при запуске субагента

Субагенты с `memory: user` во frontmatter хранят здесь знания, пока включена [автоматическая память](https://code.claude.com/docs/ru/memory.md#auto-memory). Эти знания сохраняются во всех проектах. О памяти субагентов уровня проекта см. [`.claude/agent-memory/`](#ce-agent-memory).

## Что не показано

Обозреватель охватывает файлы, которые вы создаёте и редактируете. Несколько связанных файлов находятся в других местах:

| Файл | Расположение | Назначение |
| - | - | - |
| `managed-settings.json` | Уровень системы, варьируется в зависимости от ОС | Настройки, применяемые предприятием, которые не могут переопределить ни ваши собственные файлы настроек, ни значения `--settings`, за исключением [узких исключений](https://code.claude.com/docs/ru/settings.md#exceptions-to-managed-settings-precedence). См. [где сохранить файл](https://code.claude.com/docs/ru/managed-settings.md#deploy-a-managed-settings-file) и [какой управляемый источник использует Claude Code](https://code.claude.com/docs/ru/managed-settings.md#precedence-within-the-managed-tier). |
| `CLAUDE.local.md` | Корень проекта | Ваши личные предпочтения для этого проекта, загружаемые вместе с CLAUDE.md. Создайте его вручную и добавьте в `.gitignore`. |
| `AGENTS.md` | Корень проекта, `.claude/` или любой каталог | Инструкции проекта, которые вы пишете для агентов AI кодирования. Claude Code может [загрузить его](https://code.claude.com/docs/ru/memory.md#agents-md) вместо `CLAUDE.md`. |
| Установленные плагины | `~/.claude/plugins` | Клонированные маркетплейсы, установленные версии плагинов, запись установки `installed_plugins.json` и данные для каждого плагина, управляемые командами `claude plugin`. Плагины, [синхронизированные с вашей учётной записью claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), загружаются в `~/.claude/plugins/synced/`. Для плагина, установленного из маркетплейса с источником [`command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source) в режиме ссылки, Claude Code хранит здесь ссылки вместо копии, и файлы плагина остаются в каталоге, который выводит команда. Источник `command` требует Claude Code v2.1.229 или позже. Плагин, указанный относительным путём в маркетплейсе, который вы добавили из локального пути, также [загружается на месте](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk) из своего исходного каталога, а не из копии в кэше. См. [кэширование плагинов](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk), чтобы узнать, как очищаются заброшенные версии. |

`~/.claude` также содержит данные, которые Claude Code записывает во время работы: стенограммы, историю подсказок, снимки файлов, кэши и журналы. См. [данные приложения](#application-data) ниже.

## Выберите правильный файл

Различные виды настройки находятся в разных файлах. Используйте эту таблицу, чтобы найти, где должно быть изменение.

| Вы хотите | Редактировать | Область | Справочник |
| :- | :- | :- | :- |
| Дать Claude контекст проекта и соглашения | `CLAUDE.md` | проект или глобально | [Memory](https://code.claude.com/docs/ru/memory.md) |
| Разрешить или заблокировать определённые вызовы инструментов | `settings.json` `permissions` или `hooks` | проект или глобально | [Permissions](https://code.claude.com/docs/ru/permissions.md), [Hooks](https://code.claude.com/docs/ru/hooks.md) |
| Запустить скрипт до или после вызовов инструментов | `settings.json` `hooks` | проект или глобально | [Hooks](https://code.claude.com/docs/ru/hooks.md) |
| Установить переменные окружения для сеанса | `settings.json` `env` | проект или глобально | [Settings](https://code.claude.com/docs/ru/settings-reference.md#all-settings) |
| Сохранить личные переопределения вне git | `settings.local.json` | только проект | [Области параметров](https://code.claude.com/docs/ru/settings.md#where-settings-live) |
| Добавить подсказку или возможность, которую вы вызываете с `/name` | `skills/<name>/SKILL.md` | проект или глобально | [Skills](https://code.claude.com/docs/ru/skills.md) |
| Определить специализированный subagent с его собственными инструментами | `agents/*.md` | проект или глобально | [Subagents](https://code.claude.com/docs/ru/sub-agents.md) |
| Организовать множество subagents из скрипта | `workflows/*.js` | проект или глобально | [Dynamic workflows](https://code.claude.com/docs/ru/workflows.md) |
| Подключить внешние инструменты через MCP | `.mcp.json` | только проект | [MCP](https://code.claude.com/docs/ru/mcp.md) |
| Изменить способ форматирования ответов Claude | `output-styles/*.md` | проект или глобально | [Output styles](https://code.claude.com/docs/ru/output-styles.md) |

## Справочник файлов

Эта таблица перечисляет каждый файл, который охватывает обозреватель. Файлы с областью действия проекта находятся в вашем репозитории под `.claude/` (или в корне для `CLAUDE.md`, `.mcp.json` и `.worktreeinclude`). Файлы с глобальной областью действия находятся в `~/.claude/` и применяются ко всем проектам.

> [!NOTE]
>
> Несколько вещей могут переопределить то, что вы поместили в эти файлы:
>
> * [Управляемые настройки](https://code.claude.com/docs/ru/server-managed-settings.md), развёрнутые вашей организацией, имеют приоритет над всеми файлами настроек и значениями `--settings`, за исключением [исключений, описанных в разделе «Приоритет настроек»](https://code.claude.com/docs/ru/settings.md#exceptions-to-managed-settings-precedence)
> * Флаги CLI, такие как `--permission-mode` или `--settings`, переопределяют `settings.json` для этого сеанса
> * Некоторые переменные окружения имеют приоритет над их эквивалентным параметром, но это варьируется: проверьте [справочник переменных окружения](https://code.claude.com/docs/ru/env-vars.md) для каждого из них
>
> См. [приоритет параметров](https://code.claude.com/docs/ru/settings.md#settings-precedence) для полного порядка.

Нажмите на имя файла, чтобы открыть этот узел в обозревателе выше.

| Файл | Область | Зафиксировать | Что он делает | Справочник |
| - | - | - | - | - |
| [`CLAUDE.md`](#ce-claude-md) | Проект и глобально | ✓ | Инструкции, загруженные каждый сеанс | [Memory](https://code.claude.com/docs/ru/memory.md) |
| [`rules/*.md`](#ce-rules) | Проект и глобально | ✓ | Инструкции с областью действия темы, опционально с ограничением по пути | [Rules](https://code.claude.com/docs/ru/memory.md#organize-rules-with-claude/rules/) |
| [`settings.json`](#ce-settings-json) | Проект и глобально | ✓ | Разрешения, hooks, переменные окружения, значения по умолчанию модели | [Settings](https://code.claude.com/docs/ru/settings.md) |
| [`settings.local.json`](#ce-settings-local-json) | Только проект | | Ваши личные переопределения, автоматически добавлены в .gitignore при сохранении параметра Claude Code | [Области параметров](https://code.claude.com/docs/ru/settings.md#where-settings-live) |
| [`.mcp.json`](#ce-mcp-json) | Только проект | ✓ | Серверы MCP, общие для команды | [Области MCP](https://code.claude.com/docs/ru/mcp.md#mcp-installation-scopes) |
| [`.worktreeinclude`](#ce-worktreeinclude) | Только проект | ✓ | Файлы, игнорируемые Git, для копирования в новые worktrees | [Worktrees](https://code.claude.com/docs/ru/worktrees.md#copy-gitignored-files-into-worktrees) |
| [`skills/<name>/SKILL.md`](#ce-skills) | Проект и глобально | ✓ | Переиспользуемые подсказки, вызываемые с `/name` или автоматически вызываемые | [Skills](https://code.claude.com/docs/ru/skills.md) |
| [`commands/*.md`](#ce-commands) | Проект и глобально | ✓ | Подсказки в одном файле; тот же механизм, что и skills | [Skills](https://code.claude.com/docs/ru/skills.md) |
| [`output-styles/*.md`](#ce-output-styles) | Проект и глобально | ✓ | Пользовательские наборы инструкций, которые изменяют способ работы Claude | [Output styles](https://code.claude.com/docs/ru/output-styles.md) |
| [`agents/*.md`](#ce-agents) | Проект и глобально | ✓ | Определения subagents с их собственной подсказкой и инструментами | [Subagents](https://code.claude.com/docs/ru/sub-agents.md) |
| [`workflows/*.js`](#ce-workflows) | Проект и глобально | ✓ | Скрипты динамических рабочих процессов, написанные Claude и сохранённые из `/workflows`; каждый сохранённый рабочий процесс запускается как команда `/<name>` | [Динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md) |
| [`agent-memory/<name>/`](#ce-agent-memory) | Проект и глобально | ✓ | Постоянная память для subagents | [Постоянная память](https://code.claude.com/docs/ru/sub-agents.md#enable-persistent-memory) |
| [`~/.claude.json`](#ce-claude-json) | Только глобально | | Состояние приложения, данные учётной записи, переключатели UI, личные MCP-серверы. Если файл отсутствует, Claude Code создаёт его при запуске сессии или выполнении подкоманды, например `claude auth status`, но не при `--version` или `--help`. | [Глобальная конфигурация](https://code.claude.com/docs/ru/settings-reference.md#global-config-settings) |
| [`projects/<project>/memory/`](#ce-global-projects) | Только глобально | | Auto memory: заметки Claude самому себе между сеансами | [Auto memory](https://code.claude.com/docs/ru/memory.md#auto-memory) |
| [`keybindings.json`](#ce-keybindings) | Только глобально | | Пользовательские сочетания клавиш | [Keybindings](https://code.claude.com/docs/ru/keybindings.md) |
| [`themes/*.json`](#ce-themes) | Только глобально | | Пользовательские цветовые темы | [Пользовательские темы](https://code.claude.com/docs/ru/terminal-config.md#create-a-custom-theme) |

## Frontmatter fields by file

Skills, command files, subagents, output styles, and rules read their configuration from YAML [frontmatter](https://code.claude.com/docs/ru/glossary.md#frontmatter) at the top of the file, and each accepts its own set of fields. This table lists the field names for each file and links to the reference that describes them.

| File | Frontmatter fields | Reference |
| - | - | - |
| `skills/<name>/SKILL.md` | `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` | [Skill frontmatter](https://code.claude.com/docs/ru/skills.md#frontmatter-reference) |
| `commands/*.md` | The skill fields except `name` and `paths` | [Skill frontmatter](https://code.claude.com/docs/ru/skills.md#frontmatter-reference) |
| `agents/*.md` | `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental` | [Frontmatter субагента](https://code.claude.com/docs/ru/sub-agents.md#supported-frontmatter-fields) |
| `output-styles/*.md` | `name`, `description`, `keep-coding-instructions`, `force-for-plugin` | [Output style frontmatter](https://code.claude.com/docs/ru/output-styles.md#frontmatter) |
| `rules/*.md` | `paths` | [Rule frontmatter](https://code.claude.com/docs/ru/memory.md#rules-frontmatter-reference) |

Agents shipped in a [plugin](https://code.claude.com/docs/ru/plugins/components.md#agents) honor a subset of the subagent fields.

## Устранение неполадок конфигурации

Если параметр, hook или файл не вступает в силу, см. [Отладка вашей конфигурации](https://code.claude.com/docs/ru/debug-your-config.md) для команд проверки и таблицы поиска по симптомам.

## Данные приложения

Помимо конфигурации, которую вы создаёте сами, `~/.claude` содержит данные, которые Claude Code записывает во время сессий. Эти файлы хранятся в открытом виде. Всё, что проходит через инструмент, записывается в транскрипт на диске: содержимое файлов, вывод команд, вставленный текст.

Транскрипт также может содержать то, что Claude Code отправляет модели вместе с вашими сообщениями:

* Системный промпт
* Определения инструментов
* Параметры запросов
* Загруженные им файлы инструкций, например CLAUDE.md

### Автоматически очищаемые данные

Claude Code удаляет файлы по указанным ниже путям, когда они становятся старше [`cleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#cleanupperioddays), при условии что он может надёжно определить срок хранения. Значение по умолчанию — 30 дней, минимальное — 1; значение `0` приводит к ошибке валидации. Тот же порог возраста применяется к автоматическому удалению [осиротевших worktree](https://code.claude.com/docs/ru/worktrees.md#clean-up-subagent-and-background-session-worktrees).

| Путь в `~/.claude/` | Содержимое |
| - | - |
| `projects/<project>/<session>.jsonl` | Транскрипт диалога: сообщения, вызовы инструментов и результаты инструментов, а также системный промпт, определения инструментов и параметры запросов, которые Claude Code отправлял модели |
| `projects/<project>/<session>.orphaned-<timestamp>-<suffix>.jsonl`, `projects/<project>/<session>.jsonl.superseded-<timestamp>` | Предыдущий транскрипт сессии, который Claude Code отложил вместо того, чтобы перезаписать или удалить его. Он не отображается в списке выбора сессий |
| `projects/<project>/<session>/subagents/` | Транскрипты [субагентов](https://code.claude.com/docs/ru/sub-agents.md) в том же формате, что и транскрипт сессии; удаляются вместе с транскриптом родительской сессии, когда истекает его срок хранения |
| `projects/<project>/<session>/tool-results/` | Большие выводы инструментов, вынесенные в отдельные файлы, и полноразмерные копии [изображений, которые возвращают инструменты MCP](https://code.claude.com/docs/ru/mcp.md#images-in-tool-results) |
| `projects/<project>/<session>/mcp-tasks/` | Данные, необходимые возобновлённой сессии, чтобы снова отслеживать выполняющиеся [задачи MCP](https://code.claude.com/docs/ru/mcp.md#mcp-tasks-that-run-on-the-server), и результаты завершённых задач, которые Claude ещё не прочитал |
| `file-history/<session>/` | Снимки файлов до редактирования, изменённых Claude, используемые для [восстановления чекпоинтов](https://code.claude.com/docs/ru/checkpointing.md). Хранит снимки для 100 последних чекпоинтов; файлы снимков, на которые не ссылается ни один сохранённый чекпоинт, удаляются, за исключением первого снимка каждого файла |
| `plans/` | Файлы планов, записанные в [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode) |
| `debug/` | Отладочные логи для каждой сессии, записываемые при включённом отладочном логировании, например когда вы запускаете с [`--debug`](https://code.claude.com/docs/ru/cli-reference#cli-flags) или выполняете `/debug` |
| `paste-cache/` | Содержимое больших вставок |
| `image-cache/<session>/` | Прикреплённые изображения, сохранённые Claude Code v2.1.274 и более ранними версиями. Более поздние версии сохраняют вставленные и прикреплённые изображения вне `~/.claude`, в каталоге `images/` для каждой сессии во временном каталоге, который задаёт [`CLAUDE_CODE_TMPDIR`](https://code.claude.com/docs/ru/env-vars). Очистка удаляет оставшиеся здесь каталоги других сессий независимо от их возраста. |
| `uploads/<session>/` | Файлы, которые вы прикрепляете из веб- или мобильного приложения, и фотографии, которые вы прикрепляете из мобильного приложения, при отправке сообщений в сессию [Remote Control](https://code.claude.com/docs/ru/remote-control.md). Вложение в [облачную сессию](https://code.claude.com/docs/ru/claude-code-on-the-web.md) вместо этого сохраняется в собственном облачном окружении этой сессии, а не на вашем компьютере. |
| `dev-mods/<session>/` | [Моды, написанные Claude](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod) во время сессии |
| `session-env/` | Метаданные окружения для каждой сессии |
| `tasks/` | Списки задач, записанные инструментами задач, по одному каталогу на список |
| `shell-snapshots/` | Псевдонимы, функции и параметры оболочки, захваченные при запуске и применяемые [инструментом Bash](https://code.claude.com/docs/ru/tools-reference.md#bash-tool-behavior) к каждой команде. Удаляются при корректном завершении. Очистка удаляет всё, что осталось после сбоя. |
| `backups/` | Предыдущие версии `~/.claude.json`, копируемые, когда Claude Code перезаписывает файл. Claude Code хранит пять самых новых, а также копию любой версии, которую не удалось разобрать. По истечении порога возраста удаляется и последняя копия, содержащая вашу конфигурацию. Если текущий файл успешно разбирается, содержит вашу конфигурацию и занимает менее 8 MiB, у вас остаётся его новая копия. |
| `feedback-bundles/` | Архивы транскриптов с удалёнными конфиденциальными данными, записанные `/feedback` у сторонних провайдеров или когда учётные данные Anthropic не настроены, для отправки вашей команде по работе с клиентами Anthropic |
| `feedback/drafts/` | Поставленные в очередь [отзывы, составленные Claude](https://code.claude.com/docs/ru/tools-reference.md#sendfeedback-tool-behavior), ожидающие вашей проверки в `/feedback`. Удаляются по истечении `cleanupPeriodDays` или 30 дней, в зависимости от того, что короче. Когда очередь достигает лимита в 10 черновиков, Claude Code удаляет самый старый черновик, чтобы освободить место. |
| `usage-data/` | `report.html` и копии отчётов с отметкой времени, записанные [`/insights`](https://code.claude.com/docs/ru/costs#analyze-your-usage-patterns), а также кэшированные данные анализа по каждой сессии, используемые для их построения |
| `skills/.trash/`, `plugins/.trash/` | [Скиллы](https://code.claude.com/docs/ru/skills.md#how-synced-skills-behave) и [плагины](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), удалённые синхронизацией с claude.ai, например после того как вы отключили один из них на claude.ai или прекратили синхронизацию. Файлы остаются здесь, чтобы вы могли восстановить их, пока очистка их не удалит |
| `plugins/installed_plugins.set-aside.<date>.<hash>.json`, `plugins/installed_plugins.unreadable.<date>.<hash>.kept` | Датированные копии, которые Claude Code создаёт перед перезаписью [`installed_plugins.json`](https://code.claude.com/docs/ru/plugins/loading#find-plugins-on-disk): записи об установке, которые он отбросил, и содержимое файла, который он не смог прочитать. |
| `plugins/mcpb/` | Файлы, которые Claude Code извлёк из [пакетов MCP](https://code.claude.com/docs/ru/plugins/components.md#include-a-packaged-mcpb-server), объявленных плагинами. Возраст пакета отсчитывается от последней сессии, которая его использовала. |
| `todos/`, `statsig/`, `logs/` | Устаревшие каталоги из старых версий. Больше не записываются. Очистка удаляет их содержимое, а затем и пустой каталог. |

Файлы сессий в `sessions/`, автоматическая память и транскрипты Claude Desktop и Cowork подчиняются собственным правилам хранения:

* **`sessions/`**: содержит по одному небольшому файлу на каждую запущенную сессию; используется для обнаружения параллельных сессий и сбоев. Этот каталог не входит в очистку по возрасту: Claude Code удаляет каждый файл при завершении его сессии и очищает остатки после сбоев при следующем запуске.
* **`seed-admin/`**: временные git-каталоги, которые Claude Code создаёт при упаковке вашего репозитория для [ultrareview](https://code.claude.com/docs/ru/ultrareview.md) или [загрузки в облачную сессию](https://code.claude.com/docs/ru/claude-code-on-the-web.md#send-local-repositories-without-github). Когда загрузка завершается (или в одной из последующих сессий, если загрузка была прервана), Claude Code удаляет каталог этой загрузки, а сам `seed-admin/` оставляет на месте.
* **Автоматическая память**: очистка не удаляет файлы памяти в каталоге [автоматической памяти](https://code.claude.com/docs/ru/memory.md#auto-memory) проекта, `projects/<project>/memory/`. Claude Code удаляет этот каталог, только если он оставался пустым в течение всего срока хранения. До v2.1.228 очистка считала папки внутри каталога памяти данными сессий и могла удалять старые файлы в нём.
* **Транскрипты Claude Desktop и Cowork**: Claude Code хранит транскрипт сессии, которую вы начали или последней продолжили в Claude Desktop или Cowork, независимо от её возраста. Чтобы задать для этих транскриптов ограничение по возрасту, установите [`desktopSessionCleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#desktopsessioncleanupperioddays). Требуется Claude Code v2.1.248 или новее; более ранние версии удаляют их по истечении `cleanupPeriodDays`.

  Вместо этого Claude Code удаляет эти транскрипты по истечении `cleanupPeriodDays`, например, в следующих случаях:

  * [Управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) задают `cleanupPeriodDays`
  * [К вашим сессиям применяется конфигурация HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md#check-how-developers-sign-in-and-connect)

Claude Code пропускает очистку по возрасту в следующих случаях:

* **Режим bare**: когда вы запускаете `claude -p` с [`--bare`](https://code.claude.com/docs/ru/headless#start-faster-with-bare-mode), Claude Code не выполняет очистку в этой сессии.
* **Приостановленная очистка**: если Claude Code не может надёжно определить срок хранения, он приостанавливает очистку; [событие `retention_sweep`](https://code.claude.com/docs/ru/monitoring-usage#retention-sweep-event) перечисляет все конфигурации, которые её приостанавливают. Если причина — файл настроек, который не удаётся прочитать или разобрать, или ошибки настроек при заданных `cleanupPeriodDays` или `desktopSessionCleanupPeriodDays`, `/status` показывает предупреждение, пока вы не устраните причину.

Когда [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) задают `cleanupPeriodDays`, Claude Code выполняет очистку с управляемым значением, даже если в файле настроек с более низким приоритетом есть ошибки.

Чтобы убедиться, что компьютеры в вашей организации выполняют очистку с заданным вами сроком хранения, см. раздел [Проверка очистки по сроку хранения](https://code.claude.com/docs/ru/monitoring-usage.md#check-the-retention-sweep).

### Каталог черновиков сессии

Каталог черновиков (scratchpad) — это отдельный для каждой сессии каталог, который Claude Code предоставляет Claude для временных файлов: промежуточных результатов, вспомогательных скриптов и черновиков, которым не место в вашем проекте. Когда Claude сообщает, что сохранил что-то «в scratchpad», файл находится именно там. Claude использует его вместо `/tmp` и может создавать, редактировать и читать в нём файлы без запроса разрешения.

Каталог черновиков находится во временном каталоге Claude Code, а не в `~/.claude`. Путь для текущей сессии на вашей платформе:

* **macOS**: `/private/tmp/claude-<uid>/<project>/<session-id>/scratchpad/`
* **Linux**: `/tmp/claude-<uid>/<project>/<session-id>/scratchpad/` или такой же путь внутри `$TMPDIR`, если он задан в вашей системе
* **Windows**: `%TEMP%\claude\<project>\<session-id>\scratchpad\`

`<project>` — это путь к вашему рабочему каталогу, в котором каждый символ, кроме букв и цифр, заменён на `-`, например `-Users-you-my-project`. В Windows `<project>` — это 16-символьный хеш этой строки, например `73295dabccd14c56`. В сессии приложения Desktop это может быть сама строка. Чтобы узнать точный путь, спросите Claude. Если вы задали [`CLAUDE_CODE_TMPDIR`](https://code.claude.com/docs/ru/env-vars), всё дерево перемещается в этот каталог. Хуки получают путь текущей сессии в поле [`scratchpad_dir`](https://code.claude.com/docs/ru/hooks#common-input-fields).

Файлы каталога черновиков хранятся столько же, сколько транскрипт сессии: [очистка по сроку хранения](#cleaned-up-automatically) удаляет каталог вместе с транскриптом, а [`claude purge`](#clear-local-data) не затрагивает временный каталог. Поскольку каталог находится в системном временном расположении, ваша операционная система также может очистить его, например при перезагрузке. Чтобы сохранить что-то, что Claude там записал, попросите Claude переместить это в ваш проект.

Каталог черновиков есть у сессии, только если выполнены все следующие условия:

* Вы вошли с учётной записью claude.ai, а не с API-ключом
* Сессия использует Anthropic API, а не Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry
* [`enableArtifact`](https://code.claude.com/docs/ru/settings-reference#enableartifact) не установлен в `false`

### Хранятся, пока вы их не удалите

За исключением строк, где указано иное, очистка по сроку хранения не удаляет указанные ниже пути, и Claude Code хранит их, пока вы их не удалите.

| Путь в `~/.claude/` | Содержимое |
| - | - |
| `history.jsonl` | Введённые вами промпты с отметкой времени и путём к проекту. Используется для вызова по стрелке вверх, поиска по истории `Ctrl+R` и автодополнения shell-команд `!`. Каждая очистка удаляет записи старше `cleanupPeriodDays`, когда [к вашим сессиям применяется конфигурация HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md#check-how-developers-sign-in-and-connect). |
| `stats-cache.json` | Агрегированные данные о токенах и стоимости, отображаемые `/usage` |
| `remote-settings.json` | Кэшированная копия [серверных управляемых настроек](https://code.claude.com/docs/ru/server-managed-settings.md) для вашей организации или `{}`, если ваша организация их не настроила. Присутствует, только если сессия [загружает их](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability). Claude Code проверяет наличие обновлений при запуске и ежечасно во время сессии. Claude Code удаляет этот файл, когда вы выходите из учётной записи. |
| `cache/changelog.md` | Кэшированная копия журнала изменений Claude Code, отображаемая `/release-notes`. Обновляется в фоновом режиме. |
| `policy-limits.json` | Кэшированные настройки политик функций для вашей организации. Присутствует только для некоторых типов учётных записей. Обновляется автоматически. Сопутствующий файл `policy-limits.json.stamp.json` фиксирует, какой учётной записи или API-ключу принадлежит кэш. Claude Code удаляет оба файла, когда вы выходите из учётной записи. |

#### Файлы состояния, которые нужно сохранить

В зависимости от используемых функций `~/.claude/` также содержит файлы, не перечисленные в таблицах раздела [Данные приложения](#application-data). Из них кэши и файлы блокировок можно безопасно удалять. Сохраните следующие файлы состояния:

* `.credentials.json`: ваши [учётные данные для входа](https://code.claude.com/docs/ru/authentication.md#credential-management)
* `agent-memory/`: [память субагентов](https://code.claude.com/docs/ru/sub-agents.md#enable-persistent-memory)
* `jobs/` и `daemon/`: состояние [фоновых сессий](https://code.claude.com/docs/ru/agent-view.md#where-state-is-stored)

### Хранение в открытом виде

Транскрипты и история не шифруются при хранении. Единственная защита — права доступа к файлам ОС. Если инструмент читает файл `.env` или команда выводит учётные данные, это значение записывается в `projects/<project>/<session>.jsonl`. Чтобы снизить риск:

* Уменьшите `cleanupPeriodDays`, чтобы сократить срок хранения транскриптов в Claude Code
* Установите [`desktopSessionCleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#desktopsessioncleanupperioddays), чтобы задать ограничение по возрасту и для транскриптов Claude Desktop и Cowork
* Установите переменную окружения [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/ru/env-vars), чтобы не записывать транскрипты и историю промптов в любом режиме. В неинтерактивном режиме вместо этого можно передать `--no-session-persistence` вместе с `-p` или установить `persistSession: false` в TypeScript Agent SDK; в Python SDK эквивалентного параметра нет.
* Используйте [правила разрешений](https://code.claude.com/docs/ru/permissions.md), чтобы запретить чтение файлов с учётными данными

### Очистка локальных данных

Выполните `claude purge`, чтобы удалить состояние, которое Claude Code хранит для одного проекта. Команда удаляет:

* Транскрипты и автоматическую память в `projects/`
* Записи `tasks/`, `debug/` и `file-history/` для каждой сессии
* Соответствующие строки промптов в `history.jsonl`
* Запись проекта в `~/.claude.json`

Изображения, которые вы вставляли или прикрепляли в сессиях проекта, и [каталог черновиков](#session-scratchpad-directory) каждой сессии хранятся во временном каталоге Claude Code, а не в `~/.claude`, поэтому очистка их не удаляет. [Очистка по сроку хранения](#cleaned-up-automatically) по-прежнему удаляет изображения, когда они становятся старше `cleanupPeriodDays`; каталог черновиков очищенной сессии остаётся, пока вы его не удалите или ваша операционная система не очистит временный каталог.

Команда выводит полный план удаления и запрашивает подтверждение, прежде чем что-либо удалить.

До v2.1.288 команда называлась `claude project purge`.

В примерах ниже `~/work/my-repo` используется как условное значение. Замените его путём к вашему проекту. Если для указанного пути нет соответствующего состояния, команда выводит ошибку и завершается с кодом 1.

Предварительный просмотр плана без удаления:

```bash theme={null}
claude purge ~/work/my-repo --dry-run
```

План перечисляет каждый подходящий элемент и причину его включения:

```text theme={null}
Purge plan for /home/user/work/my-repo:

  dir:    /home/user/.claude/projects/-home-user-work-my-repo
           project transcripts (.jsonl) and memory/
  config: projects["/home/user/work/my-repo"]
           project entry in ~/.claude.json (trust, history, MCP servers)
  filter: /home/user/.claude/history.jsonl
           12 prompt(s) typed in this project

shell-snapshots/ are not project-scoped and will not be touched
backups/ may still contain this project entry in old .claude.json snapshots (/home/user/.claude/backups); at most 5 are kept and they rotate out automatically
Dry run: 3 item(s) would be deleted.
```

Удаление с одним запросом подтверждения:

```bash theme={null}
claude purge ~/work/my-repo
```

Команда выводит тот же план, затем спрашивает `Delete 3 item(s) for /home/user/work/my-repo? This cannot be undone. [y/N]` и выполняет удаление, только если вы ответите `y`.

Не указывайте путь, чтобы выбрать проект из интерактивного списка.

Пропуск запроса подтверждения для использования в скриптах:

```bash theme={null}
claude purge ~/work/my-repo --yes
```

Другие параметры:

* Передайте `--all` вместо пути, чтобы очистить состояние всех проектов сразу; в этом случае `history.jsonl` удаляется целиком, а не фильтруется.
* Передайте `-i`, чтобы пройти по плану удаления поэлементно.

Команда не трогает `shell-snapshots/` и `backups/`, поскольку они не привязаны к проекту, и предупреждает о них в выводе плана. Если кто-либо выполнял [`/heapdump`](https://code.claude.com/docs/ru/troubleshooting#high-cpu-or-memory-usage) на этом компьютере, удалите также записанные им файлы `.heapsnapshot`. Снимок кучи содержит весь диалог и все учётные данные, которые хранил процесс, и ни очистка по сроку хранения, ни команда purge его не затрагивают.

Вы также можете самостоятельно удалить любые из указанных выше путей данных приложения, за исключением [файлов состояния, которые нужно сохранить](#state-files-to-keep).

| Удалить | Что вы потеряете |
| - | - |
| `~/.claude/projects/` | Возобновление, продолжение и откат прошлых сессий, а также автоматическую память для всех проектов |
| `~/.claude/history.jsonl` | Вызов промптов по стрелке вверх, поиск по истории `Ctrl+R` и автодополнение shell-команд `!` |
| `~/.claude/paste-cache/` | Вставленный текст в вызванных промптах; см. [вставка большого содержимого](https://code.claude.com/docs/ru/terminal-config.md#paste-large-content) |
| `~/.claude/uploads/` | Вложения, на которые по пути ссылаются прошлые сессии [Remote Control](https://code.claude.com/docs/ru/remote-control.md) |
| `~/.claude/file-history/` | Восстановление чекпоинтов для прошлых сессий |
| `~/.claude/stats-cache.json` | Исторические итоги, отображаемые `/usage` |
| `~/.claude/usage-data/` | Прошлые отчёты [`/insights`](https://code.claude.com/docs/ru/costs#analyze-your-usage-patterns) и кэшированные данные анализа, использованные для их построения |
| `~/.claude/feedback-bundles/` | Архивы отзывов и отчётов об ошибках, которые вы ещё не отправили своей команде по работе с клиентами Anthropic |
| `~/.claude/feedback/drafts/` | [Отзывы, составленные Claude](https://code.claude.com/docs/ru/tools-reference.md#sendfeedback-tool-behavior), которые вы не отправили |
| `~/.claude/remote-settings.json` | Ничего. Загружается заново при следующем запуске. |
| `~/.claude/cache/changelog.md` | Ничего. Обновляется в фоновом режиме. |
| `~/.claude/policy-limits.json` | Ничего. Обновляется автоматически. |
| `~/.claude/tasks/` | Ваши [списки задач](https://code.claude.com/docs/ru/interactive-mode.md#task-list), включая те, что ещё используются |
| `~/.claude/skills/.trash/`, `~/.claude/plugins/.trash/` | Возможность восстановить [синхронизированные скиллы](https://code.claude.com/docs/ru/skills.md#how-synced-skills-behave) и [синхронизированные плагины](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), удалённые Claude Code |
| `~/.claude/plugins/installed_plugins.set-aside.<date>.<hash>.json`, `~/.claude/plugins/installed_plugins.unreadable.<date>.<hash>.kept` | Копии записей об установке плагинов, которые Claude Code отбросил или не смог прочитать. Ничто их обратно не считывает |
| `~/.claude/debug/`, `~/.claude/plans/`, `~/.claude/session-env/`, `~/.claude/shell-snapshots/` | Ничего значимого для пользователя |
| `~/.claude/backups/` | Предыдущие копии, из которых можно [восстановить `~/.claude.json`](https://code.claude.com/docs/ru/errors#configuration-error-in-claude-json) |
| `~/.claude/todos/`, `~/.claude/statsig/`, `~/.claude/logs/`, `~/.claude/image-cache/` | Ничего. Устаревшие каталоги, которые текущие версии не записывают. |

Не удаляйте `~/.claude.json`, `~/.claude/settings.json` или `~/.claude/plugins/`: в них хранятся данные вашей учётной записи, ваши настройки и установленные плагины.

## Связанные ресурсы

* [Управляйте памятью Claude](https://code.claude.com/docs/ru/memory.md): пишите и организуйте CLAUDE.md, rules и auto memory
* [Настройте параметры](https://code.claude.com/docs/ru/settings.md): установите разрешения, hooks, переменные окружения и значения по умолчанию модели
* [Создавайте skills](https://code.claude.com/docs/ru/skills.md): создавайте переиспользуемые подсказки и рабочие процессы
* [Настройте subagents](https://code.claude.com/docs/ru/sub-agents.md): определите специализированные агенты с их собственным контекстом
