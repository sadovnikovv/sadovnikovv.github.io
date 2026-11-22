> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Добавление компонентов в плагин

> Добавляйте скиллы, хуки, MCP-серверы и другие типы компонентов в плагин Claude Code, с проходящим валидацию примером для каждого.

Плагин Claude Code строится из компонентов, таких как skills, agents, hooks и MCP серверы. Каждый компонент имеет папку по умолчанию в плагине, необязательный ключ манифеста в `.claude-plugin/plugin.json`, который заменяет или добавляет к этой папке, и имя, которое видит пользователь. Для полной таблицы полей каждого ключа см. [справочник манифеста](https://code.claude.com/docs/ru/plugins/manifest-reference.md#fields).

Используйте эту страницу для добавления компонента в плагин, который уже загружается.

После добавления компонента запустите `/reload-plugins` в работающей сессии или начните новую, чтобы Claude Code загрузил его. Чтобы проверить файл компонента перед загрузкой, запустите [`claude plugin validate .`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-validate) в вашей оболочке из директории плагина.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Создание вашего первого плагина**: начните с [Create a plugin](https://code.claude.com/docs/ru/plugins/create.md)
> * **Установка плагина кого-то другого**: см. [Install plugins](https://code.claude.com/docs/ru/plugins/install.md)
> * **Ваши пользователи плагина находятся на claude.ai или в Cowork**: там загружается другой набор компонентов. См. [Plugin structure and testing](https://claude.com/docs/plugins/build) и [component support table](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app)

## Изучите каталог плагинов

Обозреватель показывает пример плагина `my-plugin`, который содержит следующие компоненты в их расположениях по умолчанию:

* Skill для проверки и команду `about`
* Subagent для проверки безопасности
* Hook, который форматирует файлы после редактирования Claude, и папку `scripts/`, которую он вызывает
* Монитор логов
* Стиль вывода и цветовую тему
* Workflow для аудита маршрутов
* Исполняемый файл `hello-plugin`
* Локальный MCP сервер и языковой сервер Go

Каждый файл — это наименьший допустимый пример своего формата, предназначенный для демонстрации структуры, а не для практического использования: реальный skill или agent содержит полные инструкции и часто вспомогательные файлы, а реальный hook или монитор выполняет реальную работу. Разделы после обозревателя используют те же файлы в качестве примеров и ссылаются на более полные версии. Выберите файл или папку, чтобы прочитать, для чего она нужна, увидеть, что в ней содержится, и найти раздел, который её описывает.

What goes in a plugin

This example plugin, `my-plugin`, has the components listed here, each in its default location. Select a file or folder to read what it’s for and see what goes in it.

Plugin directory

my-plugin/

Selected piece

[Манифест](https://code.claude.com/docs/ru/plugins/manifest-reference.md) — это файл `plugin.json` в директории `.claude-plugin/` плагина. Он содержит метаданные плагина и значения `userConfig`, которые Claude Code запрашивает у пользователя. Claude Code загружает плагин и без него. В файле обязателен только `name`. В этом примере `description` — это текст, который пользователи видят для плагина в `/plugin`, а `version` удерживает пользователей на этой версии, пока вы её не измените:

```json theme={null}
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Review, formatting, and database tools for this team"
}
```

[Skill](https://code.claude.com/docs/ru/skills.md) — это файл `SKILL.md`. Сохраняйте каждый skill в отдельной директории в папке `skills/`. Claude читает `description` каждого skill, и когда то, что просит пользователь, совпадает с ней, например, когда пользователь просит Claude проверить pull request, Claude загружает инструкции skill и следует им. Пользователь также может запустить его напрямую как `/my-plugin:review`:

```markdown theme={null}
---
description: Reviews a pull request for style and test coverage. Use when asked to review code.
---

Review the changed files. Report style problems first, then missing tests.
```

Команда — это один файл Markdown, который пользователь запускает по имени. Команды — это более старый формат: skill запускается по имени таким же образом и может также содержать вспомогательные файлы в собственной директории, поэтому пишите новые как skills и сохраняйте `commands/` для файлов, которые у вас уже есть. Этот файл становится `/my-plugin:about` и принимает тот же frontmatter, что и skill:

```markdown theme={null}
---
description: Summarize the repository
---

Summarize what this repository does in three sentences.
```

[Subagent](https://code.claude.com/docs/ru/sub-agents.md) — это отдельный помощник с собственными инструкциями и собственным контекстным окном, которому Claude может делегировать задачу и получить результат. Каждый файл Markdown в папке `agents/` определяет один: frontmatter называет его и говорит, когда его использовать, а тело — это его системный prompt. Этот назван `my-plugin:security-reviewer`, и пользователь может вызвать его с помощью `@agent-my-plugin:security-reviewer`:

```markdown theme={null}
---
name: security-reviewer
description: Reviews code changes for security issues. Use after edits to authentication or input handling.
model: sonnet
---

You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
```

[Hook](https://code.claude.com/docs/ru/hooks-guide.md) запускает что-то автоматически в точке жизненного цикла Claude Code, например, после каждого редактирования файла: команду shell, HTTP запрос, вызов инструмента MCP, prompt к модели или subagent. Сохраняйте hooks плагина в `hooks/hooks.json` в корне плагина. Этот запускает `scripts/format.sh` плагина после того, как Claude записывает или редактирует файл:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
          }
        ]
      }
    ]
  }
}
```

Монитор — это shell-команда, которую Claude Code запускает в фоне при запуске сессии и держит запущенной до её завершения. То, что он выводит, достигает Claude как уведомления. Поле `when` может вместо этого запустить его в первый раз, когда запустится названный скилл. Этот отслеживает лог ошибок:

```json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Плагин может включать [стили вывода](https://code.claude.com/docs/ru/output-styles.md), которые изменяют, как Claude форматирует и формулирует свои ответы. Сохраняйте каждый стиль вывода как `output-styles/<name>.md`. Этот появляется в `/output-style` как `my-plugin:terse`:

```markdown theme={null}
---
name: terse
description: Answer in as few words as possible
keep-coding-instructions: true
---

Keep every reply short. Skip preambles and summaries.
```

Плагин может включать [цветовые темы](https://code.claude.com/docs/ru/terminal-config.md#create-a-custom-theme) для интерфейса Claude Code. Сохраняйте каждую тему как `themes/<slug>.json`. Этот появляется в `/theme` как `Dracula`, отмеченный как из `my-plugin`:

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555"
  }
}
```

Папка `workflows/` содержит файлы [workflow](https://code.claude.com/docs/ru/workflows.md) `.js`: блок `meta`, затем тело скрипта, которое координирует несколько subagents. Этот запускается как `/my-plugin:audit-routes`:

```javascript theme={null}
export const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler for missing auth checks',
}

const found = await agent('List every .ts file under src/routes/.', {
  schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } },
})

const audits = await pipeline(found.files, file =>
  agent(`Audit ${file} for missing authentication checks.`, { label: file }),
)

return audits.filter(Boolean)
```

`bin/` — это способ, которым плагин поставляет инструмент командной строки. Пока плагин включен, Claude Code помещает эту папку в `PATH` shell, в котором он запускает команды, поэтому Claude или инструкции skill могут запустить инструмент по имени без установки пользователем. С этим [исполняемым файлом](#executables) на месте `hello-plugin` — это команда, которую Claude может запустить:

```bash theme={null}
#!/bin/bash
echo "hello from my-plugin"
```

Hook в `hooks/hooks.json` запускает скрипт, и эта папка — это место, где пример его хранит. Имя `scripts/` — это соглашение, а не что-то, что Claude Code ищет: hook указывает на файл по его пути, `${CLAUDE_PLUGIN_ROOT}/scripts/format.sh`. Скрипт форматирования может выглядеть так:

```bash theme={null}
#!/bin/bash
npx prettier --write .
```

[MCP сервер](https://code.claude.com/docs/ru/mcp.md) предоставляет Claude инструменты из внешней системы. Объявите его в `.mcp.json` в корне плагина. Этот запускает локальный сервер из скрипта внутри плагина и появляется в `/mcp` как `plugin:my-plugin:db`:

```json theme={null}
{
  "mcpServers": {
    "db": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  }
}
```

LSP сервер предоставляет Claude [диагностику и навигацию по коду](https://code.claude.com/docs/ru/plugins/code-intelligence.md) для языка. Объявите сервер в `.lsp.json` в корне плагина. Этот подключает языковой сервер Go для файлов `.go`:

```json theme={null}
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

## Добавление каждого вида компонента

Каждый раздел ниже охватывает один вид компонента: где его файлы находятся в плагине, пример, который проходит валидацию, что видит пользователь после загрузки плагина, и ключ манифеста, который изменяет расположение по умолчанию. Добавляйте те, которые нужны вашему плагину; ни один не требуется.

### Skills

[Skill](https://code.claude.com/docs/ru/skills.md) — это файл `SKILL.md`, который Claude может загрузить, когда его описание совпадает с задачей. Пользователь также может запустить его как команду. Сохраняйте каждый skill в его собственной директории под `skills/`:

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── review/
        └── SKILL.md
```

Дайте `SKILL.md` `description`, чтобы Claude знал, когда его использовать:

```markdown skills/review/SKILL.md theme={null}
---
description: Reviews a pull request for style and test coverage. Use when asked to review code.
---

Review the changed files. Report style problems first, then missing tests.
```

После загрузки плагина `/my-plugin:review` запускает skill. Имя команды и кто может её вызвать следуют этим правилам:

* **Имя команды**: `/<plugin>:<directory>`, поэтому `skills/review/SKILL.md` в `my-plugin` — это `/my-plugin:review`. Если вы установите `name` в frontmatter, он заменит последний сегмент, и префикс плагина остаётся. См. [как skill получает имя команды](https://code.claude.com/docs/ru/skills.md#how-a-skill-gets-its-command-name)
* **Кто вызывает**: Claude, пользователь или оба, контролируется frontmatter. См. [Control who invokes a skill](https://code.claude.com/docs/ru/skills.md#control-who-invokes-a-skill)

Вы также можете разместить skills вне директории по умолчанию `skills/`:

* **Дополнительные директории**: перечислите их в ключе манифеста `skills`. Они добавляются к сканированию по умолчанию `skills/`, а не заменяют его, в отличие от `commands` и `agents`
* **Один skill в корне плагина**: без директории `skills/` и без ключа манифеста `skills`, `SKILL.md` в корне плагина загружается как один skill. Установите `name` в его frontmatter, потому что иначе установка из marketplace назовёт skill по его [директории кэша](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk), а не по вашему плагину

Чтобы включить инструкции в плагин, напишите их как skill. Claude Code не загружает `CLAUDE.md` в корне плагина, и `claude plugin validate` предупреждает `CLAUDE.md at the plugin root is not loaded as project context`.

Если правило должно действовать каждый раз, например [блокирование редактирования защищённых файлов](https://code.claude.com/docs/ru/hooks-guide.md#block-edits-to-protected-files), добавьте его в плагин как [hook](#hooks) вместо skill. Чтобы выбрать между ними, см. вкладку Hook vs Skill под [Compare similar features](https://code.claude.com/docs/ru/features-overview.md#compare-similar-features).

Для полей frontmatter и вспомогательных файлов см. [Skills](https://code.claude.com/docs/ru/skills.md).

### Команды

Команда — это один файл Markdown, который пользователь запускает по имени, например `/my-plugin:about`.

> [!NOTE]
>
> Команды — это более старый формат, и [skills](#skills) их заменяют для новой работы. Skill запускается по имени таким же образом, и он также может содержать вспомогательные файлы в своей директории. Сохраняйте `commands/` для файлов, которые вы переносите из `.claude/commands/`.

Сохраняйте команду в `commands/<file>.md` и она становится `/<plugin>:<file>`. Подпапка добавляет сегмент, поэтому `commands/db/migrate.md` — это `/my-plugin:db:migrate`.

Файлы команд принимают тот же frontmatter, что и skills.

#### Определение команд в манифесте

Это нужно только, если вы хотите сохранить файлы команд где-то в другом месте, чем `commands/`, или определить короткую команду внутри `plugin.json` без отдельного файла Markdown. Установите ключ манифеста `commands`, и Claude Code читает его вместо сканирования `commands/`. Ключ принимает путь, массив путей или объект, который отображает каждое имя команды либо на файл `source`, либо на встроенное `content`.

Этот манифест определяет `/my-plugin:about` встроенным образом, без файла Markdown:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "commands": {
    "about": {
      "content": "Summarize what this repository does in three sentences.",
      "description": "Summarize the repository"
    }
  }
}
```

Загрузите плагин и запустите `/my-plugin:about` в сессии, чтобы подтвердить, что он загрузился.

Для полного синтаксиса ключа см. [`commands`](https://code.claude.com/docs/ru/plugins/manifest-reference#commands).

### Агенты

[Подагент](https://code.claude.com/docs/ru/sub-agents.md) — это отдельный помощник с собственными инструкциями и окном контекста, которому Claude может делегировать задачу. Каждый файл Markdown под `agents/` определяет один:

```markdown agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code changes for security issues. Use after edits to authentication or input handling.
model: sonnet
---

You are a security reviewer. Read the changed files and report injection, authentication, and secrets-handling risks.
```

Этот агент называется `my-plugin:security-reviewer`, и пользователь может [вызвать его явно](https://code.claude.com/docs/ru/sub-agents.md#invoke-subagents-explicitly) с помощью `@agent-my-plugin:security-reviewer`. Форма имени — `<plugin>:<name>`, где `<name>` берётся из поля `name` во frontmatter или из имени файла, если это поле отсутствует.

Ключ `agents` манифеста заменяет сканирование `agents/`.

#### Организация агентов в подпапках

Вы можете поместить файлы агентов плагина в подпапки `agents/`. Claude Code [загружает их рекурсивно](https://code.claude.com/docs/ru/sub-agents.md#choose-the-subagent-scope) и объединяет имя плагина, каждое имя подпапки и имя файла с двоеточиями, чтобы сформировать имя агента с областью видимости. Например, `agents/review/security.md` в плагине с именем `my-plugin` загружается как `my-plugin:review:security`. Два параметра изменяют это имя:

* Frontmatter `name`: он заменяет только имя файла, поэтому `name: audit` в `agents/review/security.md` загружается как `my-plugin:review:audit`
* Манифест [`agents`](https://code.claude.com/docs/ru/plugins/manifest-reference#fields) поле: файл, который вы там перечислите, загружается без имён подпапок, поэтому `"agents": "./custom/review/security.md"` загружается как `my-plugin:security`

#### Поля frontmatter в агентах плагина

Frontmatter агента плагина следует этим правилам:

* **Поддерживаемые поля**: `name`, `description`, `model`, `effort`, `maxTurns`, `autoCompactWindow`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `omitClaudeMd`, `isolation`, `color` и ключ `cacheTtl` из `experimental`. Единственное допустимое значение `isolation` — `"worktree"`. Что делает каждое из них, см. в разделе [поддерживаемые поля frontmatter](https://code.claude.com/docs/ru/sub-agents.md#supported-frontmatter-fields)
* **Игнорируемые поля**: `permissionMode`, `hooks`, `mcpServers` и `initialPrompt`. Файл агента не может добавлять hooks или MCP серверы самостоятельно, поэтому добавляйте их как плагин [hooks](#hooks) и [MCP серверы](#mcp-servers) вместо этого
* **`name` длиннее 256 символов**: Claude Code игнорирует его и называет агента по имени файла, как и в случае, когда поле отсутствует
* **Frontmatter, который не парсится**: агент всё ещё загружается со всеми полями, игнорируемыми. Он назван по имени файла, и его описание читается как `Agent from my-plugin plugin`. Запустите [`claude plugin validate`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-validate) в вашей оболочке, чтобы найти эти файлы

Для того, что делает каждое поле и правила приоритета, см. [Subagents](https://code.claude.com/docs/ru/sub-agents.md#supported-frontmatter-fields).

### Hooks

[Hook](https://code.claude.com/docs/ru/hooks-guide.md) запускает что-то автоматически в точке жизненного цикла Claude Code, например, после каждого редактирования файла: команду оболочки, HTTP запрос, вызов инструмента MCP, prompt к модели или подагента. Сохраняйте hooks плагина в `hooks/hooks.json` в корне плагина, под верхним уровнем ключа `"hooks"`, в той же форме, что и объект `hooks` в `settings.json`. Это позволяет вам скопировать существующий hook параметров без изменений.

Этот hook запускает встроенный скрипт после каждого `Write` или `Edit`:

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh\""
          }
        ]
      }
    ]
  }
}
```

Сохраняйте скрипт в `scripts/format.sh` и сделайте его исполняемым.

Загрузите плагин и попросите Claude отредактировать файл. Hook `PostToolUse`, который выходит с кодом 0, ничего не показывает в транскрипте, поэтому подтвердите, что он запустился с помощью [debug logging](https://code.claude.com/docs/ru/hooks.md#debug-hooks) или по тому, что сам скрипт изменяет.

Hooks в `hooks/hooks.json` и в ключе манифеста `hooks` оба загружаются. Для каждого события и его payload см. [Hook events](https://code.claude.com/docs/ru/hooks.md#hook-events).

Если у другого включённого плагина такое же имя, один из двух регистрирует хуки из своего `hooks/hooks.json`, а хуки другого не подключаются. Какой именно, а также уведомление в `/plugin`, которое сообщает об этом, см. в разделе [Хуки, когда два включённых плагина имеют одинаковое имя](https://code.claude.com/docs/ru/plugins/loading.md#hooks-when-two-enabled-plugins-share-a-name).

Чтобы написать hooks как функции JavaScript, которые запускаются внутри Claude Code и могут рисовать в его интерфейсе, перечислите файл модуля под ключом `modules` в том же `hooks/hooks.json`. Плагин с одним — это мод. См. [Create a mod](https://code.claude.com/docs/ru/plugins/mods/create.md).

#### Когда запускаются hooks плагина

Hooks плагина не ждут использования одного из skills или команд плагина. Claude Code регистрирует их, когда сессия загружает плагин, и они запускаются на своих событиях с этого момента. Чтобы ограничить, когда запускается hook, сузьте его `matcher`.

Если hook никогда не запускается, см. [hooks that don't fire](https://code.claude.com/docs/ru/plugins/troubleshooting.md#failed-to-load-hooks-from-and-hooks-that-dont-fire).

#### Окружение, кавычки и соответствие инструментам MCP

Окружение hook, кавычки `${CLAUDE_PLUGIN_ROOT}` и matchers для собственных инструментов MCP плагина работают следующим образом:

* **Окружение**: каждый процесс hook получает `CLAUDE_PLUGIN_ROOT` и `CLAUDE_PLUGIN_DATA` в своём окружении, плюс `CLAUDE_PLUGIN_OPTION_<KEY>` для каждого значения [конфигурации пользователя](#user-configuration), поэтому ваш скрипт может читать их оттуда
* **Кавычки**: когда `command` не имеет `args`, он запускается через оболочку, поэтому оберните путь `${CLAUDE_PLUGIN_ROOT}` в двойные кавычки, как пример `hooks/hooks.json` под [Hooks](#hooks) делает, чтобы сохранить развёрнутый путь одним словом оболочки. Когда вы передаёте `args` вместо этого, каждый элемент передаётся как один аргумент без оболочки и не нуждается в кавычках. См. [exec form and shell form](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form)
* **Соответствие собственным инструментам MCP плагина**: инструмент из [MCP сервера, который объявляет этот плагин](#mcp-servers), назван `mcp__plugin_<plugin>_<server>__<tool>`, поэтому напишите это полное имя в matcher. Matcher только на имя сервера никогда не запускается. См. [Match MCP tools](https://code.claude.com/docs/ru/hooks.md#match-mcp-tools)

### MCP серверы

MCP сервер предоставляет Claude инструменты из внешней системы. Объявите его в `.mcp.json` в корне плагина, в той же форме, что и [проект `.mcp.json`](https://code.claude.com/docs/ru/mcp#project-scope). Этот `.mcp.json` объявляет один сервер с именем `db`:

```json .mcp.json theme={null}
{
  "mcpServers": {
    "db": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  }
}
```

Вы также можете опустить обёртку `mcpServers` и поместить `db` на верхний уровень файла.

Загрузите плагин и запустите `/mcp`, чтобы подтвердить, что сервер появляется как `plugin:my-plugin:db`.

`claude plugin validate` проверяет `.mcp.json` и сообщает запись сервера, которую Claude Code отбросит во время загрузки, как ошибку. Требуется Claude Code v2.1.281 или позже.

Для того, где плохая запись появляется во время загрузки, см. [MCP servers that don't start](https://code.claude.com/docs/ru/plugins/troubleshooting.md#invalid-mcp-server-config-for-and-mcp-servers-that-dont-start).

Ключ манифеста `mcpServers` принимает встроенную карту сервера, путь к файлу JSON или массив этих. Когда сервер манифеста имеет то же имя, что и один в `.mcp.json`, сервер манифеста заменяет его.

#### Достижение пользователей на claude.ai и Cowork

Локальный сервер stdio, такой как сервер `db` под [MCP servers](#mcp-servers), работает в Claude Code и в сессии Cowork, которая работает на вашей машине в приложении Claude Desktop, но не на claude.ai. Чтобы достичь пользователей там тоже, ссылайтесь на удалённый сервер по его URL `https://`, который claude.ai и Cowork предлагают пользователю как соединитель, как показано в [Bundle an MCP connector with its skill](https://claude.com/docs/plugins/build#bundle-an-mcp-connector-with-its-skill).

#### Имена серверов, имена инструментов и перезагрузки

Имена сервера, подстановка переменных и поведение перезагрузки следуют этим правилам:

* **Имя сервера**: `plugin:<plugin>:<server>`, поэтому сервер `db` в `my-plugin` — это `plugin:my-plugin:db` в `/mcp`. Используйте ту же форму для именования сервера в [hook `mcp_tool`](https://code.claude.com/docs/ru/hooks#mcp-tool-hook-fields)
* **Имена инструментов**: `mcp__plugin_<plugin>_<server>__<tool>`, поэтому инструмент `query` на том сервере `db` — это `mcp__plugin_my-plugin_db__query`. Это имя, которое нужно использовать в [правилах разрешений](https://code.claude.com/docs/ru/permissions.md) и [matchers hook](#hooks)
* **Подстановка**: `${CLAUDE_PLUGIN_ROOT}` и другие [переменные пути](#path-variables-and-persistent-data) подставляются в `command`, `args` и `env`. Кавычки не нужны в `args`, потому что каждый элемент передаётся как один аргумент
* **Перезагрузка**: когда пользователь запускает `/reload-plugins` и [перезагрузка применяется](https://code.claude.com/docs/ru/plugins/cli-reference.md#reloads-that-change-mcp-tools), сервер, конфигурация которого не изменилась, сохраняет своё соединение. Сервер, конфигурация которого изменилась, переподключается, и тот, который вы удалили, отключается

#### Включение упакованного MCPB сервера

Ключ `mcpServers` также принимает упакованный сервер как [файл MCPB](https://github.com/modelcontextprotocol/mcpb), расширение которого `.mcpb` или более старое `.dxt`. Укажите ключ на файл, как путь внутри плагина или URL `https://`:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": "./servers/db.mcpb"
}
```

Сервер берёт своё имя из `name` в манифесте пакета.

Пакет собственного манифеста может объявлять параметры, которые серверу нужны от пользователя в блоке `user_config`. Упакованный сервер с требуемым параметром, который не имеет сохранённого значения, не запускается. На вкладке **Errors** в `/plugin` показывается `Bundled MCP server "<name>" was not started: it needs configuration`.

Пользователи предоставляют значения одним из двух способов:

* **В `/plugin`**: выберите плагин на вкладке **Installed** и выберите **Configure**
* **При установке из оболочки**: передайте [`--config <server>.<key>=<value>`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-install) в `claude plugin install`. Требуется Claude Code v2.1.285 или позже, и работает только для пакета, упакованного внутри плагина.

Для транспортов и аутентификации см. [MCP](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers).

### LSP серверы

LSP сервер предоставляет Claude диагностику и навигацию по коду для языка. Если [официальный плагин code intelligence](https://code.claude.com/docs/ru/plugins/code-intelligence.md) уже охватывает ваш язык, установите его вместо написания собственного. Иначе объявите сервер в `.lsp.json` в корне плагина:

```json .lsp.json theme={null}
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Файл отображает каждое имя сервера непосредственно на его конфигурацию, без объекта-обёртки вокруг карты. `command` — это имя двоичного файла, с его аргументами в `args`. `extensionToLanguage` нуждается по крайней мере в одном расширении, каждое начинается с `.`.

`claude plugin validate` не читает этот файл. Когда любая запись недействительна, весь файл пропускается при загрузке и `Invalid LSP server config for ".lsp.json"` появляется на вкладке **Errors** в `/plugin`.

Ваш плагин конфигурирует соединение, но не устанавливает двоичный файл сервера, и каждое расширение файла получает один сервер:

* **Отсутствующий двоичный файл**: Claude Code запускает `command` по имени из `PATH` пользователя. Когда двоичный файл там не находится, сервер не запускается и `claude --debug` логирует `LSP server <name> failed to start`
* **Конфликты расширений**: когда два включённых сервера претендуют на одно и то же расширение, первый зарегистрированный обрабатывает эти файлы, а другой не используется для них, независимо от того, поступают ли серверы из одного плагина или двух. Вкладка **Errors** в `/plugin` показывает предупреждение `LSP server "<name>" is not used for <ext> files`

Ключ манифеста `lspServers` принимает ту же карту встроенной, путь к файлу JSON или массив этих, и его серверы добавляются к тем, что в `.lsp.json`. Когда сервер манифеста имеет то же имя, что и один в `.lsp.json`, сервер манифеста заменяет его.

Для `transport`, timeouts, restarts и других полей см. [`lspServers`](https://code.claude.com/docs/ru/plugins/manifest-reference#lspservers).

Отправляйте вывод логов в stderr, а не stdout. Claude Code читает stdout сервера только как сообщения протокола и принимает заголовки сообщений до 64 КиБ и тело сообщения до 32 МиБ.

Claude Code отключает сервер, который превышает любой лимит или пишет вывод, не являющийся протоколом, в stdout, и считает отключение сбоем для `restartOnCrash` и `maxRestarts`. Когда вы запускаете с `--debug`, Claude Code пишет ошибку, называющую причину, в журнал отладки.

### Исполняемые файлы

Файлы в `bin/` в корне плагина находятся на `PATH` оболочки инструмента Bash, пока плагин включен, поэтому Claude может запустить их как простые команды. Команда, которую Claude запускает с помощью [инструмента PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool) вне [песочницы](https://code.claude.com/docs/ru/sandboxing.md), тоже находит их в своём `PATH`, а команда PowerShell, запущенная в песочнице, — нет. Добавьте исполняемый скрипт:

```bash bin/hello-plugin theme={null}
#!/bin/bash
echo "hello from my-plugin"
```

Сделайте его исполняемым с помощью `chmod +x bin/hello-plugin` и загрузите плагин. Когда вы просите Claude запустить `hello-plugin`, результат инструмента Bash показывает вывод скрипта.

Директории `bin/` плагина идут после собственных записей `PATH` пользователя, поэтому плагин не может затенять `git`, `ls` или другую системную команду.

claude.ai и Cowork не устанавливают плагин, который имеет директорию `bin/` верхнего уровня, включая тот, который вы [распространяете через параметры организации claude.ai](https://claude.com/docs/plugins/org-sync#keep-executables-out-of-the-top-level-bin-directory).

### Темы и стили вывода

Плагин может включать цветовые темы и стили вывода. Оба появляются в тех же выборщиках, что и собственные пользователя. Для любого из них установка ключа манифеста заменяет сканирование папки.

| Компонент | Сохраняйте как | Формат | Появляется в | Ключ манифеста |
| :- | :- | :- | :- | :- |
| Тема | `themes/<slug>.json` | Формат [пользовательского файла темы](https://code.claude.com/docs/ru/terminal-config.md#create-a-custom-theme), который пользователи пишут в `~/.claude/themes/` | `/theme`, под `name` файла | `experimental.themes` |
| Стиль вывода | `output-styles/<name>.md` | Формат [пользовательского стиля вывода](https://code.claude.com/docs/ru/output-styles.md#create-a-custom-output-style), с frontmatter `name` и `description` | `/output-style`, как `<plugin>:<name>` | `outputStyles` |

Темы плагина доступны только для чтения, поэтому когда пользователь редактирует одну в `/theme`, редактирование сохраняется как копия в их собственной директории тем.

Эта тема перекрашивает акцент prompt и текст ошибки на тёмном предустановке:

```json themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555"
  }
}
```

### Каналы

[Канал](https://code.claude.com/docs/ru/channels.md) позволяет внешней системе, такой как приложение чата, отправлять сообщения в сессию. В плагине канал — это один из MCP серверов плюс запись `channels`, которая привязывает к нему и может запросить собственную конфигурацию. Этот манифест привязывает канал к серверу `telegram` и запрашивает токен бота:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "telegram": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": { "BOT_TOKEN": "${user_config.bot_token}" }
    }
  },
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        }
      }
    }
  ]
}
```

`server` должен совпадать с ключом в `mcpServers`. Per-channel `userConfig` принимает ту же форму, что и [верхний уровень ключа `userConfig`](#user-configuration).

Для того, что должен реализовать сервер и как пользователи включают плагин канала, см. [Package as a plugin](https://code.claude.com/docs/ru/channels-reference.md#package-as-a-plugin) в справочнике каналов. Для таблицы полей см. [`channels`](https://code.claude.com/docs/ru/plugins/manifest-reference#channels).

### Мониторы

Монитор — это команда оболочки, которая работает в фоне для всей сессии. То, что она выводит, достигает Claude как уведомления, поэтому Claude может реагировать на журнал или изменение статуса без просьбы наблюдать за ним. Сохраняйте записи в `monitors/monitors.json`:

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Команда запускается в оболочке, в текущем рабочем каталоге сессии. Она выполняется с полными правами вашего пользователя и вне [песочницы](https://code.claude.com/docs/ru/sandboxing.md).

Команда монитора ограничена в том, где она запускается и на что может ссылаться:

* **Интерактивные сессии**: мониторы плагина не запускаются в неинтерактивном режиме с флагом `-p`
* **Минимальная версия**: в Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform или Microsoft Foundry, а также при заданных `DISABLE_TELEMETRY` или `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` мониторам требуется Claude Code v2.1.310 или новее. Это требование действует, когда [получение feature-флагов](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching) отключено
* **Нет конфигурации пользователя**: `command` получает [переменные пути](#path-variables-and-persistent-data) и `${ENV_VAR}` из окружения, но никогда `${user_config.*}`. Монитор, который ссылается на один, не запускается, и процессы монитора также не получают `CLAUDE_PLUGIN_OPTION_<KEY>`
* **Отключение во время сессии**: если вы отключите плагин во время сессии, Claude Code не останавливает мониторы, которые уже работают. Они останавливаются, когда сессия заканчивается

Ключ манифеста `experimental.monitors` принимает тот же массив встроенным или путь к файлу JSON и читается вместо `monitors/monitors.json`.

Для триггера `when` и других полей см. [`monitors`](https://code.claude.com/docs/ru/plugins/manifest-reference#monitors).

## Запрос значений конфигурации у пользователя

Объявите значения, которые ваш плагин нужен от пользователя, в ключе манифеста `userConfig`, чтобы пользователи не редактировали `settings.json` сами. Каждый вариант появляется в диалоге с его `title` как метка и его `description` под ней.

Установите `"sensitive": true` для токена или пароля. Диалог затем маскирует ввод, и значение хранится в защищённом хранилище, а не в `settings.json`.

Этот манифест запрашивает конечную точку и токен:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "my-plugin",
  "userConfig": {
    "api_url": {
      "type": "string",
      "title": "API URL",
      "description": "Base URL of your team's API"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token for your team's API",
      "sensitive": true
    }
  }
}
```

### Когда появляется диалог конфигурации

Диалог является частью интерактивного интерфейса `/plugin`. Когда пользователь делает любое из следующего, он открывается для любого варианта, который ещё не установлен:

* Устанавливает плагин в `/plugin`
* Запускает `/plugin install <plugin>@<marketplace>` внутри сессии
* Включает плагин из вкладки **Installed** в `/plugin`

Чтобы открыть тот же диалог в любое время, пользователь запускает `/plugin configure <plugin>@<marketplace>`.

Диалог управления плагинами VS Code [Manage plugins dialog](https://code.claude.com/docs/ru/vs-code.md#install-plugins) запрашивает неустановленные варианты в виде формы после установки, и значок шестерёнки в строке плагина открывает форму снова со всеми вариантами.

Команда оболочки `claude plugin install` никогда не запрашивает значения `userConfig`. Чтобы установить значения из оболочки, передайте каждое как `--config KEY=VALUE` при установке, или передайте объект JSON в [`claude plugin configure --values-stdin`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-configure) после этого.

Когда варианты остаются неустановленными, `claude plugin install` выводит строку `userConfig options not yet set`. Для точного текста строки см. [The `userConfig` dialog never appears](https://code.claude.com/docs/ru/plugins/troubleshooting#the-userconfig-dialog-never-appears).

Для полей варианта, где хранится каждое значение, как компонент ссылается на сохранённое значение и какие поля отклоняют `${user_config.*}`, см. [User configuration](https://code.claude.com/docs/ru/plugins/manifest-reference.md#user-configuration).

## Ссылка на пути плагина и хранение данных

Вы не знаете, где будет установлен ваш плагин, поэтому ссылайтесь на его файлы и данные через эти переменные, а не через фиксированные пути. Они подставляются в содержимое skill, команды и агента, в команды hook и монитора, а также в конфигурации MCP и LSP сервера. Они также экспортируются в процессы hook, MCP и LSP:

* **`${CLAUDE_PLUGIN_ROOT}`**: директория установки плагина. Каждая версия имеет свою собственную [директорию кэша](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk), поэтому путь изменяется при обновлении плагина. Не пишите состояние там
* **`${CLAUDE_PLUGIN_DATA}`**: директория, которая выживает обновления, для `node_modules`, виртуальных окружений и кэшей. Она разрешается в `~/.claude/plugins/data/<id>/` и создаётся при первой ссылке
* **`${CLAUDE_PROJECT_DIR}`**: корень проекта, то же значение, которое получают hooks

В пути директории данных `<id>` — это идентификатор плагина со всеми символами, кроме букв, цифр, `_` и `-`, заменённых на `-`, поэтому `my-plugin@my-marketplace` становится `my-plugin-my-marketplace`.

В Windows большинство подставленных путей используют прямые слэши, как в `C:/Users/you/...`. Они сохраняют свои нативные обратные слэши в [хуке в exec-форме](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form) и в хуке, который запускается через PowerShell — оболочку по умолчанию в Windows, если Git Bash не установлен.

### Установка зависимостей в директорию данных

Для плагина, установленного из marketplace, Claude Code автоматически устанавливает подходящие [зависимости пакета Node.js](https://code.claude.com/docs/ru/plugins/loading.md#node-js-package-dependencies) при кэшировании плагина, поэтому вам может не потребоваться устанавливать их самостоятельно. Когда вам нужно, этот hook `SessionStart` устанавливает `node_modules` в `${CLAUDE_PLUGIN_DATA}` при первом запуске и снова после обновления, которое изменяет `package.json`:

```json hooks/hooks.json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

После первой сессии `~/.claude/plugins/data/<id>/node_modules` существует. MCP сервер может затем установить `NODE_PATH` в `${CLAUDE_PLUGIN_DATA}/node_modules` в его `env`. Для того, какие поля подставляют какую переменную, см. [Environment variables](https://code.claude.com/docs/ru/plugins/manifest-reference.md#environment-variables).

## Следующие шаги

* [Plugin manifest reference](https://code.claude.com/docs/ru/plugins/manifest-reference.md): поля `plugin.json`, правила пути и стандартная раскладка
* [Test plugins with evals](https://code.claude.com/docs/ru/plugin-evals.md): проверьте, что компоненты, которые вы добавили, изменяют поведение Claude так, как вы намеревались
* [Publish and distribute a plugin](https://code.claude.com/docs/ru/plugins/publish.md): версионируйте плагин и поместите его в marketplace
* [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md): что делать, когда компонент не загружается или hook не запускается
