> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник по hooks

> Справочник по событиям hook Claude Code, схеме конфигурации, форматам JSON входа/выхода, кодам выхода, асинхронным hooks, HTTP hooks, prompt hooks и MCP tool hooks.

> [!TIP]
>
> Для краткого руководства с примерами см. [Автоматизация рабочих процессов с помощью hooks](https://code.claude.com/docs/ru/hooks-guide.md).

Hooks — это определяемые пользователем команды оболочки, конечные точки HTTP, вызовы инструментов MCP, подсказки LLM или подагенты, которые выполняются автоматически в определённых точках жизненного цикла Claude Code. Claude Code запускает одни и те же события hook везде, где он работает: сеансы в терминале, расширения IDE, [приложение Desktop](https://code.claude.com/docs/ru/desktop-quickstart.md) и [облачные сеансы](https://code.claude.com/docs/ru/claude-code-on-the-web.md). Используйте этот справочник для поиска схем событий, параметров конфигурации, форматов JSON входа/выхода и расширенных функций, таких как асинхронные hooks, HTTP hooks и MCP tool hooks.

Плагин также может регистрировать hooks как функции JavaScript, которые Claude Code вызывает в своём собственном процессе, которые могут отображаться в интерфейсе, а также реагировать на события. Плагин, который это делает, — это [mod](https://code.claude.com/docs/ru/plugins/mods/overview.md), и эти функциональные hooks рассматриваются в разделе [Реагирование на события](https://code.claude.com/docs/ru/plugins/mods/events.md), а не здесь. Hooks на этой странице продолжают работать наряду с модами.

## Жизненный цикл hook

Claude Code запускает hooks в определённых точках во время сеанса. Когда событие срабатывает и совпадает с фильтром, Claude Code передаёт JSON-контекст события вашему обработчику hook. Для command hooks входные данные поступают на stdin. Для HTTP hooks они поступают как тело POST-запроса. Ваш обработчик может затем проверить входные данные, выполнить действие и опционально вернуть решение.

События срабатывают в трёх ритмах:

* один раз за сеанс: `SessionStart` и `SessionEnd`
* один раз за ход: `UserPromptSubmit`, `Stop` и `StopFailure`
* при каждом вызове инструмента внутри агентного цикла: `PreToolUse` и `PostToolUse`, за исключением вызовов [`EndConversation`](https://code.claude.com/docs/ru/tools-reference#endconversation-tool-behavior), которые пропускают оба

![Диаграмма жизненного цикла hook, показывающая опциональный Setup, переходящий в SessionStart, затем цикл за ход, содержащий UserPromptSubmit, UserPromptExpansion для slash commands, вложенный агентный цикл (PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart/Stop, TaskCreated, TaskCompleted) и Stop или StopFailure, за которым следуют TeammateIdle, PreCompact, PostCompact и SessionEnd, с Elicitation и ElicitationResult вложенными внутри выполнения MCP tool, PermissionDenied как боковая ветвь от PermissionRequest для автоматических отказов, WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged, FileChanged и DirectoryAdded как отдельные асинхронные события, PreModelSwitch как отдельное последовательное событие, которое запускается перед запрошенным переключением модели, PostModelSwitch как отдельное асинхронное событие, которое запускается после изменения модели сеанса, и MessageDisplay как событие только для отображения, которое запускается во время потоковой передачи текста сообщения помощника](https://mintcdn.com/claude-code/x7pO8l4XcvAXCoVc/images/hooks-lifecycle.svg?fit=max\&auto=format\&n=x7pO8l4XcvAXCoVc\&q=85\&s=81b9256c1bbe8832553485f5d9e9c746)

Таблица ниже суммирует, когда срабатывает каждое событие. Раздел [Hook events](#hook-events) документирует полную схему входа и параметры управления решением для каждого события.

| Событие | Когда оно срабатывает |
| :- | :- |
| `SessionStart` | Когда сеанс начинается или возобновляется |
| `Setup` | Когда вы запускаете Claude Code с `--init-only`, или с `--init` или `--maintenance` в режиме `-p`. Для одноразовой подготовки в CI или скриптах |
| `UserPromptSubmit` | Когда отправляется промпт, прежде чем Claude его обработает. Также срабатывает для [ходов, которые Claude Code начинает самостоятельно](https://code.claude.com/docs/ru/hooks.md#userpromptsubmit) |
| `UserPromptExpansion` | Когда команда, введённая пользователем, расширяется в запрос, прежде чем она достигнет Claude. Может заблокировать расширение |
| `PreToolUse` | Перед выполнением вызова инструмента. Может заблокировать его |
| `PermissionRequest` | Когда вызов инструмента требует решения о разрешении |
| `PermissionDenied` | Когда автоматический режим отклоняет вызов инструмента, включая отклонения без вердикта классификатора. Используйте JSON `hookSpecificOutput.retry: true`, чтобы сообщить модели, что она может повторить попытку отклонённого вызова инструмента. Claude Code игнорирует `retry`, когда классификатор не выдал вердикт |
| `PostToolUse` | После успешного выполнения вызова инструмента |
| `PostToolUseFailure` | После неудачного выполнения вызова инструмента |
| `PostToolBatch` | После разрешения полного пакета параллельных вызовов инструментов, перед следующим вызовом модели |
| `Notification` | Когда Claude Code отправляет уведомление |
| `MessageDisplay` | Во время отображения текста сообщения помощника |
| `SubagentStart` | Когда порождается подагент |
| `SubagentStop` | Когда подагент завершает работу |
| `TaskCreated` | Когда задача создаётся через `TaskCreate` |
| `TaskCompleted` | Когда задача отмечается как завершённая |
| `Stop` | Когда Claude завершает ответ |
| `StopFailure` | Когда ход завершается из-за ошибки API |
| `TeammateIdle` | Когда товарищ по команде [команды агентов](https://code.claude.com/docs/ru/agent-teams.md) собирается перейти в режим ожидания |
| `InstructionsLoaded` | Когда файл CLAUDE.md или `.claude/rules/*.md` загружается в контекст. Срабатывает при запуске сеанса и когда файлы ленивой загрузки загружаются во время сеанса |
| `ConfigChange` | Когда файл конфигурации изменяется во время сеанса |
| `CwdChanged` | Когда рабочий каталог изменяется, например когда Claude выполняет команду `cd`. Полезно для реактивного управления окружением с помощью инструментов, таких как direnv |
| `DirectoryAdded` | Когда рабочий каталог добавляется в середине сеанса через `/add-dir` или запрос управления SDK `register_repo_root` |
| `FileChanged` | Когда наблюдаемый файл изменяется на диске. Поле `matcher` указывает, какие имена файлов отслеживать |
| `WorktreeCreate` | Когда worktree создаётся через `--worktree`, `isolation: "worktree"`, или для фонового сеанса. Заменяет поведение git по умолчанию |
| `WorktreeRemove` | Когда удаляется worktree, созданный хуком `WorktreeCreate` |
| `PreCompact` | Перед компактизацией контекста |
| `PostCompact` | После завершения компактизации контекста |
| `PreModelSwitch` | Перед тем как Claude Code применяет переключение модели, которое вы или клиент запросили. Может заблокировать переключение |
| `PostModelSwitch` | После изменения модели сеанса, включая изменения, которые Claude Code делает самостоятельно, такие как восстановление модели при возобновлении сеанса |
| `Elicitation` | Когда сервер MCP запрашивает ввод пользователя во время вызова инструмента |
| `ElicitationResult` | После того как пользователь отвечает на запрос MCP, перед отправкой ответа обратно на сервер |
| `SessionEnd` | Когда сеанс завершается |

### Как разрешается hook

Чтобы увидеть, как событие, matcher и обработчик работают вместе, рассмотрим этот хук `PreToolUse`, который блокирует команды `rm -rf`.

> [tab] macOS/Linux
>
> `matcher` сужает область до вызовов инструмента Bash и [команд Monitor](#match-monitor-commands), а условие `if` сужает её дальше до подкоманд Bash, совпадающих с `rm *`, поэтому `block-rm.sh` запускается, только когда оба фильтра совпадают:
>
> ```json theme={null}
> {
>   "hooks": {
>     "PreToolUse": [
>       {
>         "matcher": "Bash",
>         "hooks": [
>           {
>             "type": "command",
>             "if": "Bash(rm *)",
>             "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
>             "args": []
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Скрипт читает JSON входные данные из stdin, извлекает команду и возвращает `permissionDecision` со значением `"deny"`, если она содержит `rm -rf`. Сохраните его в `.claude/hooks/block-rm.sh` в вашем проекте и сделайте его исполняемым с помощью `chmod +x .claude/hooks/block-rm.sh`, чтобы Claude Code мог его запустить:
>
> ```bash theme={null}
> #!/bin/bash
> # .claude/hooks/block-rm.sh
> COMMAND=$(jq -r '.tool_input.command')
>
> if echo "$COMMAND" | grep -q 'rm -rf'; then
>   jq -n '{
>     hookSpecificOutput: {
>       hookEventName: "PreToolUse",
>       permissionDecision: "deny",
>       permissionDecisionReason: "Destructive command blocked by hook"
>     }
>   }'
> else
>   exit 0  # no decision; normal permission flow applies
> fi
> ```
>
> Этот скрипт, как и другие примеры Bash на этой странице, которые анализируют JSON входные данные, использует `jq`, поэтому установите `jq` и убедитесь, что он находится в вашем `PATH`, перед попыткой их использования.

> [tab] Windows (PowerShell)
>
> matcher `Bash|PowerShell` охватывает [инструмент PowerShell](#powershell), а также Bash. Одно правило `if` называет только один инструмент, поэтому каждый инструмент получает свой обработчик: первый сужает область до подкоманд Bash, совпадающих с `rm *`, второй — до команд PowerShell, совпадающих с `Remove-Item *`. Оба запускают один и тот же скрипт через `powershell.exe`:
>
> ```json theme={null}
> {
>   "hooks": {
>     "PreToolUse": [
>       {
>         "matcher": "Bash|PowerShell",
>         "hooks": [
>           {
>             "type": "command",
>             "if": "Bash(rm *)",
>             "command": "powershell.exe",
>             "args": [
>               "-NoProfile",
>               "-ExecutionPolicy",
>               "Bypass",
>               "-File",
>               "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.ps1"
>             ]
>           },
>           {
>             "type": "command",
>             "if": "PowerShell(Remove-Item *)",
>             "command": "powershell.exe",
>             "args": [
>               "-NoProfile",
>               "-ExecutionPolicy",
>               "Bypass",
>               "-File",
>               "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.ps1"
>             ]
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Флаг `-NoProfile` пропускает загрузку вашего профиля PowerShell, чтобы hook запустился быстро, а `-ExecutionPolicy Bypass` позволяет PowerShell запустить локальный файл скрипта.
>
> Скрипт читает JSON входные данные из stdin, извлекает команду и возвращает `permissionDecision` со значением `"deny"`, если она содержит `rm -rf` или `Remove-Item` с последующим `-Recurse`. Сохраните его в `.claude/hooks/block-rm.ps1` в вашем проекте:
>
> ```powershell theme={null}
> # .claude/hooks/block-rm.ps1
> $callInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
> $command = $callInput.tool_input.command
>
> if ($command -match 'rm -rf|Remove-Item.*-Recurse') {
>   @{
>     hookSpecificOutput = @{
>       hookEventName = "PreToolUse"
>       permissionDecision = "deny"
>       permissionDecisionReason = "Destructive command blocked by hook"
>     }
>   } | ConvertTo-Json
> } else {
>   exit 0  # no decision; normal permission flow applies
> }
> ```

Теперь предположим, что Claude Code решает запустить `Bash "rm -rf /tmp/build"` с конфигурацией macOS/Linux. Вот что происходит:

![Диаграмма разрешения hook: срабатывает событие PreToolUse, фильтр проверяет совпадение Bash, затем условие if проверяет совпадение Bash(rm \*). Если оба совпадают, команда hook запускается и возвращает permissionDecision deny, поэтому вызов инструмента блокируется и Claude Code продолжает работу. Если одна из проверок не совпадает, hook пропускается и вызов инструмента может продолжить работу.](https://mintcdn.com/claude-code/ikqp3_70mqIahteV/images/hook-resolution.svg?fit=max\&auto=format\&n=ikqp3_70mqIahteV\&q=85\&s=be0bf3053550c26de5f54cd64674c197)

**1. Событие срабатывает**

Событие `PreToolUse` срабатывает. Claude Code отправляет входные данные инструмента как JSON на stdin hook:

```json theme={null}
{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
```

**2. Фильтр проверяет**

Фильтр `"Bash"` совпадает с именем инструмента, поэтому эта группа hook активируется. Если вы опустите фильтр или используете `"*"`, группа активируется при каждом возникновении события.

**3. Условие if проверяет**

Условие `if` `"Bash(rm *)"` совпадает, потому что `rm -rf /tmp/build` — это подкоманда, совпадающая с `rm *`, поэтому этот обработчик запускается. Если бы команда была `npm test`, проверка `if` не удалась бы и `block-rm.sh` никогда не запустился бы, избегая затрат на порождение процесса. Поле `if` опционально; без него каждый обработчик в совпадающей группе запускается.

**4. Обработчик hook запускается**

Скрипт проверяет полную команду и находит `rm -rf`, поэтому выводит решение на stdout:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

Если бы команда была более безопасным вариантом `rm`, таким как `rm file.txt`, скрипт выполнил бы `exit 0` вместо этого. Код выхода 0 без вывода означает, что hook не имеет решения для отчёта, поэтому вызов инструмента продолжается через нормальный [поток разрешений](https://code.claude.com/docs/ru/permissions.md). Hook может отклонить вызов, но молчание не одобряет его.

**5. Claude Code действует на основе результата**

Claude Code читает JSON решение, блокирует вызов инструмента и показывает Claude причину.

Раздел [Configuration](#configuration) ниже документирует полную схему, и каждый раздел [hook event](#hook-events) документирует, какой входной JSON получает ваша команда и какой выход она может вернуть.

## Конфигурация

Хуки определяются в JSON-файлах настроек. Конфигурация имеет три уровня вложенности:

1. Выберите [событие хука](#hook-events), на которое нужно реагировать, например `PreToolUse` или `Stop`
2. Добавьте [группу matcher](#matcher-patterns), чтобы отфильтровать, когда он срабатывает, например «для инструмента Bash»
3. Определите один или несколько [обработчиков хука](#hook-handler-fields), которые будут запускаться при совпадении

Полный разбор с аннотированным примером см. выше в разделе [Как разрешается хук](#how-a-hook-resolves).

> [!NOTE]
>
> На этой странице для каждого уровня используются определённые термины: **событие хука** — для точки жизненного цикла, **группа matcher** — для фильтра и **обработчик хука** — для запускаемой shell-команды, HTTP-эндпоинта, MCP-инструмента, промпта или агента. Слово «хук» само по себе обозначает функцию в целом.

### Расположение хуков

Место, где вы определяете хук, определяет его область действия:

| Расположение | Область действия | Можно ли поделиться |
| :- | :- | :- |
| `~/.claude/settings.json` | Все ваши проекты | Нет, локально для вашего компьютера |
| `.claude/settings.json` | Один проект | Да, можно закоммитить в репозиторий |
| `.claude/settings.local.json` | Один проект | Нет, добавляется в gitignore, когда Claude Code сохраняет в него настройку |
| Настройки управляемой политики | Вся организация | Да, контролируется администратором |
| `hooks/hooks.json` [плагина](https://code.claude.com/docs/ru/plugins/overview.md) | Когда плагин включён | Да, поставляется вместе с плагином |
| Frontmatter [скилла](https://code.claude.com/docs/ru/skills.md) | Оставшаяся часть сессии после вызова скилла. См. [Хуки в скиллах и агентах](#hooks-in-skills-and-agents) | Да, определяется в файле скилла |
| Frontmatter [субагента](https://code.claude.com/docs/ru/sub-agents.md) | Пока работает этот субагент | Да, определяется в файле субагента |

[Облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) не читают ваш локальный `~/.claude/settings.json`. В [самостоятельно размещённом окружении](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#permissions-and-tool-approval) Claude Code также запускает хуки, которые оператор заранее поместил в `~/.claude/` хоста раннера, и запускает хуки из файла управляемых настроек образа раннера, когда этот файл входит в число [управляемых источников, которые применяет Claude Code](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources), что по умолчанию означает: только когда ни настройки, управляемые сервером, ни политика Claude Code, доставленная через MDM, не предоставляют управляемый уровень. О том, какие файлы настроек и плагины, а значит и какие хуки, попадают в облачную сессию, см. [что переносится из вашей настройки](https://code.claude.com/docs/ru/cloud-environments.md#what-carries-over-from-your-setup).

Подробнее о разрешении файлов настроек см. [настройки](https://code.claude.com/docs/ru/settings.md).

Хуки из файлов настроек, настроек управляемой политики и плагинов также запускаются внутри [субагентов](https://code.claude.com/docs/ru/sub-agents.md). Когда субагент вызывает инструмент, события инструментов, такие как `PreToolUse` и `PostToolUse`, запускают те же настроенные хуки, что и в основном диалоге, а входные данные содержат [общие поля входных данных](#common-input-fields) `agent_id` и `agent_type`, которые идентифицируют субагента.

Администраторы могут использовать [`allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#allowmanagedhooksonly) в [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md), чтобы ограничить, какие хуки запускаются:

* Ваши пользовательские, проектные, локальные хуки и хуки плагинов блокируются. Исключение составляют хуки из плагинов, принудительно включённых в `enabledPlugins` управляемых настроек
* Claude Code также ограничивает ваши настройки [`statusLine`](https://code.claude.com/docs/ru/statusline) и [`fileSuggestion`](https://code.claude.com/docs/ru/settings-reference#filesuggestion) управляемыми настройками
* Claude Code также отключает плагины с [источником `command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source), включая плагины, принудительно включённые в `enabledPlugins` управляемых настроек, если только [`disableCommandPluginSources`](https://code.claude.com/docs/ru/settings-reference#disablecommandpluginsources) явно не установлен в `false`. Источники `command` требуют Claude Code v2.1.229 или новее
* Claude Code также блокирует [команды `headersHelper`](https://code.claude.com/docs/ru/plugins/host-marketplace#authenticate-archive-downloads) маркетплейсов, если только [`disableCommandPluginSources`](https://code.claude.com/docs/ru/settings-reference#disablecommandpluginsources) явно не установлен в `false`, за исключением маркетплейса, который объявлен в самих управляемых настройках

См. [что запускается при `allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#what-runs-under-allowmanagedhooksonly).

Записи хуков объединяются между уровнями настроек, а не заменяют друг друга: пользовательские, проектные и локальные настройки добавляют собственные хуки, не удаляя управляемые, а настройка [`disableAllHooks`](#disable-or-remove-hooks) не может отключить управляемые хуки, если задана вне управляемых настроек.

#### Ограничение HTTP-хуков

Задайте эти [списки разрешённых для HTTP-хуков](https://code.claude.com/docs/ru/settings-reference.md#hook-and-skill-settings) в управляемых настройках, чтобы охватить хуки, которые развёртывает ваша организация, или в любом файле настроек, чтобы охватить другие хуки:

* `allowedHttpHookUrls`: если задан, Claude Code запускает обработчик HTTP-хука, только если его URL соответствует объединённому списку разрешённых
* `httpHookAllowedEnvVars`: если задан, Claude Code подставляет в заголовки хуков только переменные окружения из этого списка

### Шаблоны matcher

Поле `matcher` фильтрует, когда срабатывают хуки. То, как вычисляется matcher, зависит от содержащихся в нём символов:

| Значение matcher | Вычисляется как | Пример |
| :- | :- | :- |
| `"*"`, `""` или отсутствует | Совпадение со всем | срабатывает при каждом возникновении события |
| Только буквы, цифры, `_`, `-`, пробелы, `,` и `\|` | Точная строка или список точных строк, разделённых `\|` или `,` с необязательными пробелами вокруг | `Bash` соответствует инструменту Bash, а в `PreToolUse` и `PermissionRequest` также [командам Monitor](#match-monitor-commands); `Edit\|Write` и `Edit, Write` соответствуют в точности любому из двух инструментов; `code-reviewer` соответствует только этому типу агента |
| Содержит любой другой символ | Регулярное выражение JavaScript без привязки | `^Notebook` соответствует любому инструменту, имя которого начинается с `Notebook`; `mcp__memory__.*` соответствует всем инструментам сервера `memory` |

Matcher, вычисляемый как регулярное выражение, проверяется с помощью `RegExp.prototype.test` в JavaScript, который успешно срабатывает при совпадении в любом месте значения. `Edit.*` соответствует и `Edit`, и `NotebookEdit`; оберните шаблон в `^` и `$`, как в `^Edit$`, если вам нужно совпадение со всей строкой.

`FileChanged` и `StopFailure` используют более узкий набор символов для точного совпадения: только буквы, цифры, `_` и `|`. Дефис, пробел или запятая в matcher для этих двух событий оставляют его на пути регулярного выражения, и альтернативы разделяет только `|`. Все остальные события с поддержкой matcher в следующей таблице принимают `|` или `,`.

Событие `FileChanged` не следует этим правилам при построении списка отслеживаемых файлов. См. [FileChanged](#filechanged).

Каждый тип события сопоставляется по своему полю:

| Событие | Что фильтрует matcher | Примеры значений matcher |
| :- | :- | :- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | имя инструмента | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | как началась сессия | `startup`, `resume`, `clear`, `compact`, `fork` |
| `Setup` | какой флаг CLI запустил настройку | `init`, `maintenance` |
| `SessionEnd` | почему завершилась сессия | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` |
| `Notification` | тип уведомления | `permission_prompt`, `idle_prompt`, `auth_success`, `auth_storage_failure`, `elicitation_dialog`, `elicitation_url_dialog`, `elicitation_complete`, `elicitation_response`, `agent_needs_input`, `agent_completed`, `quota_auto_resume_fired`, `quota_auto_resume_stale`, `quota_auto_resume_disabled`, `plugin_notification` |
| `SubagentStart` | тип агента | `general-purpose`, `Explore`, `Plan`, имена пользовательских агентов или имена с областью плагина, например `^my-plugin:reviewer$` |
| `PreCompact`, `PostCompact` | что запустило сжатие контекста | `manual`, `auto` |
| `PreModelSwitch`, `PostModelSwitch` | каноническое имя модели, на которую переключается сессия, как описано в разделе [PreModelSwitch](#premodelswitch) | `claude-opus-5`, `claude-opus-4-6\|claude-opus-5`, `.*opus.*` |
| `SubagentStop` | тип агента | те же значения, что и для `SubagentStart` |
| `ConfigChange` | источник конфигурации | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `CwdChanged` | matcher не поддерживается | всегда срабатывает при каждом возникновении |
| `DirectoryAdded` | как был добавлен каталог | `slash_command`, `register_repo_root` |
| `FileChanged` | буквальные имена файлов для отслеживания (см. [FileChanged](#filechanged)) | `.envrc\|.env` |
| `StopFailure` | тип ошибки | `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `account_on_hold`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `cloud_credential_error`, `unknown` |
| `InstructionsLoaded` | причина загрузки | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `UserPromptExpansion` | имя команды | имена ваших скиллов или команд |
| `Elicitation` | имя MCP-сервера | имена ваших настроенных MCP-серверов |
| `ElicitationResult` | имя MCP-сервера | те же значения, что и для `Elicitation` |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `MessageDisplay` | matcher не поддерживается | всегда срабатывает при каждом возникновении |

Сопоставление `StopFailure` по `cloud_credential_error` требует Claude Code v2.1.267 или новее — первой версии, которая сообщает об ошибках загрузки учётных данных с этим значением, а не с `server_error` или `unknown`.

Для большинства событий Claude Code вычисляет matcher по полю из [входных данных JSON](#hook-input-and-output), которые он отправляет вашему хуку через stdin. Для событий инструментов это поле `tool_name`. Для `PreModelSwitch` и `PostModelSwitch` Claude Code вычисляет matcher по каноническому имени, которое он выводит из `to_model`, как описано в разделе [PreModelSwitch](#premodelswitch). В разделе каждого [события хука](#hook-events) перечислен полный набор значений matcher и схема входных данных для этого события.

Этот пример запускает скрипт линтинга только тогда, когда Claude записывает или редактирует файл:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

Если вы добавите поле `matcher` к событию без поддержки matcher, оно будет молча проигнорировано.

Для событий инструментов можно фильтровать точнее, задав [поле `if`](#common-fields) в отдельных обработчиках хуков. `if` использует [синтаксис правил разрешений](https://code.claude.com/docs/ru/permissions.md) для сопоставления имени инструмента и аргументов вместе, поэтому `"Bash(git *)"` запускается, когда любая подкоманда во входных данных Bash соответствует `git *`, а `"Edit(*.ts)"` запускается только для файлов TypeScript.

#### Сопоставление MCP-инструментов

Инструменты [MCP](https://code.claude.com/docs/ru/mcp.md)-серверов отображаются как обычные инструменты в событиях инструментов (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), поэтому их можно сопоставлять так же, как любое другое имя инструмента.

MCP-инструменты следуют шаблону именования `mcp__<server>__<tool>`, например:

* `mcp__memory__create_entities`: инструмент создания сущностей сервера Memory
* `mcp__filesystem__read_file`: инструмент чтения файла сервера Filesystem
* `mcp__github__search_repositories`: инструмент поиска сервера GitHub

Чтобы сопоставить все инструменты сервера, добавьте `.*` к префиксу сервера. `.*` обязателен: matcher вроде `mcp__memory` или `mcp__brave-search` содержит только символы точного совпадения, поэтому он сравнивается как точная строка и не соответствует ни одному инструменту.

* `mcp__memory__.*` соответствует всем инструментам сервера `memory`
* `mcp__brave-search__.*` соответствует всем инструментам сервера, имя которого содержит дефис
* `mcp__.*__write.*` соответствует любому инструменту любого сервера, имя которого начинается с `write`

Инструменты [MCP-сервера, поставляемого с плагином](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers), используют сегмент сервера с областью, включающий имя плагина: `mcp__plugin_<plugin-name>_<server-name>__<tool>`. Matcher, написанный для голого ключа сервера, никогда не срабатывает для этих инструментов. Для плагина с именем `my-plugin`, который поставляет сервер под ключом `db`, инструмент `query` отображается как `mcp__plugin_my-plugin_db__query`, поэтому matcher для всех инструментов этого сервера — `mcp__plugin_my-plugin_db__.*`. Используйте то же имя инструмента с областью в [поле `if`](#common-fields) обработчика. О том, как строится имя с областью, см. [MCP-серверы, предоставляемые плагинами](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers).

Этот пример записывает в лог все операции сервера memory и проверяет операции записи от любого MCP-сервера:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

#### Сопоставление команд Monitor

Хук [`PreToolUse`](#pretooluse) или [`PermissionRequest`](#permissionrequest) с matcher `Bash` также запускается для shell-команд, которые Claude запускает с помощью [инструмента Monitor](https://code.claude.com/docs/ru/tools-reference.md#monitor-tool), но его `allow` и [`updatedInput`](#pretooluse-decision-control) на них не действуют. Требуется Claude Code v2.1.314 или новее. Matcher, такие как `Bash|PowerShell`, `^Bash$` и `Bash.*`, тоже являются matcher `Bash`. Хук с matcher `Bash` не запускается для [наблюдения за WebSocket](https://code.claude.com/docs/ru/tools-reference.md#websocket-source), а хук `PostToolUse` с таким matcher не запускается для Monitor.

Хук, который запускается для команды Monitor, может отклонить её или заставить Claude Code спросить вас о ней. Чтобы разрешить или переписать команду, замените matcher `Bash` на тот, который включает Monitor:

* **Matcher, включающий Monitor**: с matcher, например `Bash|Monitor` или `.*`, или без matcher хук получает собственные входные данные вызова Monitor, и `allow` и `updatedInput` применяются. В [`if`](#common-fields) укажите Monitor, как в `Monitor(tail *)`, который сопоставляется по [тем же правилам, что и `Bash(tail *)`](#bash-if-matching). Если в его `if` указан Bash, хук всё равно получает входные данные вызова Monitor, но `allow` и `updatedInput` не действуют
* **Matcher `Bash`**: хук получает вызов Bash. В `if` укажите Bash, как в `Bash(tail *)`. Хук не запускается, если в его `if` указан Monitor

### Поля обработчика хука

Каждый объект во внутреннем массиве `hooks` — это обработчик хука: shell-команда, HTTP-эндпоинт, MCP-инструмент, промпт LLM или агент, который запускается при совпадении matcher. Существует пять типов:

* **[Командные хуки](#command-hook-fields)** (`type: "command"`): запускают shell-команду. Ваш скрипт получает [входные данные JSON](#hook-input-and-output) события через stdin и сообщает результаты через коды выхода и stdout.
* **[HTTP-хуки](#http-hook-fields)** (`type: "http"`): отправляют входные данные JSON события как HTTP POST-запрос на URL. Эндпоинт сообщает результаты через тело ответа, используя тот же [формат вывода JSON](#json-output), что и командные хуки.
* **[Хуки MCP-инструментов](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): вызывают инструмент на настроенном [MCP-сервере](https://code.claude.com/docs/ru/mcp.md). Текстовый вывод инструмента обрабатывается так же, как stdout командного хука.
* **[Хуки с промптом](#prompt-and-agent-hook-fields)** (`type: "prompt"`): отправляют промпт модели Claude для однократной оценки. Модель возвращает своё решение в виде JSON. См. [Хуки на основе промптов](#prompt-based-hooks).
* **[Хуки агентов](#prompt-and-agent-hook-fields)** (`type: "agent"`): порождают субагента, который может использовать такие инструменты, как Read, Grep и Glob, чтобы проверить условия перед возвратом решения. Хуки агентов являются экспериментальными и могут измениться. См. [Хуки на основе агентов](#agent-based-hooks).

Когда событие срабатывает, соответствующие ему хуки запускаются параллельно. Если более 12 из них являются хуками с промптом или хуками агентов, 12 из них запускаются одновременно, а остальные запускаются по мере завершения работающих. [`timeout`](#common-fields) каждого ожидающего хука начинает отсчёт, когда этот хук запускается.

Если вы определите один и тот же обработчик в нескольких файлах настроек, он запустится один раз. Копия того же обработчика в плагине или скилле остаётся отдельной.

Обработчики запускаются в текущем каталоге с окружением Claude Code. Если текущий каталог больше не существует, например worktree или временный каталог, который другая оболочка удалила посреди сессии, Claude Code запускает командные хуки из первого из следующих каталогов, который ещё существует: каталог, в котором началась сессия, корень проекта, ваш домашний каталог или системный временный каталог. Claude Code записывает предупреждение с названием резервного каталога в [лог отладки](#debug-hooks). О сессии в worktree, которую вы запускаете из десктопного приложения, см. [Что worktree разделяют с основной рабочей копией](https://code.claude.com/docs/ru/worktrees.md#what-worktrees-share-with-the-main-checkout).

Переменная окружения `$CLAUDE_CODE_REMOTE` имеет значение `"true"` в удалённых веб-окружениях и не задана в локальном CLI. Claude Code v2.1.199 и новее устанавливает [`$CLAUDE_CODE_BRIDGE_SESSION_ID`](https://code.claude.com/docs/ru/env-vars) в идентификатор сессии [Remote Control](https://code.claude.com/docs/ru/remote-control.md), пока у локальной сессии есть активное подключение Remote Control.

#### Общие поля

Эти поля применяются ко всем типам хуков:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `type` | да | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"` или `"agent"` |
| `if` | нет | [Синтаксис правил разрешений](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax) для фильтрации того, когда запускается этот хук, например `"Bash(git *)"` или `"Edit(*.ts)"`. Команда хука запускается, только если вызов инструмента соответствует шаблону. О том, как шаблоны Bash вычисляются для подкоманд, `$()` и обратных кавычек, см. [таблицу сопоставления Bash](#bash-if-matching). Вычисляется только для событий инструментов: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` и `PermissionDenied`. Для других событий хук с заданным `if` никогда не запускается |
| `timeout` | нет | Количество секунд до отмены. Claude Code не применяет его к командному хуку, который вы запускаете с [`async: true`](#run-hooks-in-the-background). Значения по умолчанию: 600 для `command`, `http` и `mcp_tool`; 30 для `prompt`; 60 для `agent`. Claude Code снижает значение по умолчанию для `command`, `http` и `mcp_tool` до 30 в [`UserPromptSubmit`](#userpromptsubmit), [`PreModelSwitch`](#premodelswitch) и [`PostModelSwitch`](#postmodelswitch) и до 10 в [`MessageDisplay`](#messagedisplay). Хуки [`SessionEnd`](#sessionend) делят общий бюджет в 1,5 секунды; если ваши настройки задают более длинный `timeout` для отдельного хука, Claude Code увеличивает бюджет до этого значения, но не более чем до 60 секунд |
| `statusMessage` | нет | Пользовательское сообщение индикатора, отображаемое во время работы хука |
| `once` | нет | Если `true`, Claude Code удаляет хук после его первого успешного запуска. Запуск, который завершается ошибкой, блокирует с кодом выхода 2 или превышает таймаут, оставляет хук на месте, поэтому он запускается снова при следующем подходящем событии. Учитывается только для хуков, объявленных во [frontmatter скилла](#hooks-in-skills-and-agents); игнорируется в файлах настроек и frontmatter агентов |

Поле `if` содержит ровно одно правило разрешений. Синтаксиса `&&`, `||` или списка для объединения правил нет; чтобы применить несколько условий, определите отдельный обработчик хука для каждого.

В условии `if` для файлового инструмента шаблон каталога из одного сегмента, например `"Edit(src/**)"`, соответствует только каталогу `src` в рабочем каталоге и файлам внутри него. Чтобы сопоставить каталог с именем `src` на любой глубине, напишите `"Edit(**/src/**)"`.

#### Как шаблоны `if` сопоставляются с командами Bash

Для шаблонов Bash в [поле `if`](#common-fields) то, запустится ли команда вашего хука, зависит от формы шаблона и команды Bash, которую вызывает Claude. Начальные присваивания `VAR=value` удаляются перед сопоставлением.

| Шаблон `if` | Команда Bash | Хук запускается? | Почему |
| :- | :- | :- | :- |
| `Bash(git *)` | `FOO=bar git push` | да | начальные присваивания удаляются; `git push` соответствует |
| `Bash(git *)` | `npm test && git push` | да | проверяется каждая подкоманда; `git push` соответствует |
| `Bash(rm *)` | `echo $(rm -rf /)` | да | команды внутри `$()` и обратных кавычек проверяются; `rm -rf /` соответствует |
| `Bash(rm *)` | `echo $(date)` | нет | ни одна подкоманда не соответствует `rm *` |
| `Bash(git push *)` | `echo $(date)` | да | шаблоны, указывающие больше, чем имя команды, всё равно запускают хук при наличии `$()`, обратных кавычек или `$VAR` |

Когда Claude Code не может разбить входные данные Bash на подкоманды, он запускает ваш хук независимо от шаблона. Поскольку фильтр `if` работает по принципу «насколько возможно», для строгого разрешения или запрета используйте [систему разрешений](https://code.claude.com/docs/ru/permissions.md), а не хук.

#### Поля командного хука

Помимо [общих полей](#common-fields), командные хуки принимают следующие поля:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `command` | да | Shell-команда для выполнения. С `args` — исполняемый файл, запускаемый напрямую. См. [Форма exec и форма shell](#exec-form-and-shell-form) |
| `args` | нет | Список аргументов. Если он присутствует, `command` разрешается как исполняемый файл и запускается напрямую с `args` в качестве вектора аргументов, без участия оболочки. См. [Форма exec и форма shell](#exec-form-and-shell-form) |
| `async` | нет | Если `true`, выполняется в фоне без блокировки. См. [Запуск хуков в фоне](#run-hooks-in-the-background) |
| `asyncRewake` | нет | Если `true`, выполняется в фоне и пробуждает Claude при коде выхода 2. Stderr хука, или stdout, если stderr пуст, показывается Claude как [системное напоминание](https://code.claude.com/docs/ru/glossary.md#system-reminder), чтобы он мог отреагировать на сбой длительной фоновой задачи |
| `shell` | нет | Оболочка для этого хука. Принимает `"bash"` или `"powershell"`. По умолчанию `"bash"` или `"powershell"` в Windows, если Git Bash не установлен. Значение `"powershell"` запускает команду через PowerShell в Windows. Не требует `CLAUDE_CODE_USE_POWERSHELL_TOOL`, поскольку хуки запускают PowerShell напрямую. Игнорируется, если задан `args` |
| `onFailure` | нет | Выполняется ли действие, вызвавшее хук, если хук завершился сбоем: `"continue"` или `"block"`. О `"block"` и о случае, когда поле не задано, см. [Блокировка действия при сбое хука](#block-the-action-when-a-hook-fails). Требуется Claude Code v2.1.295 или новее |

##### Форма exec и форма shell

Командный хук выполняется в форме exec, если задан `args`, и в форме shell, если `args` опущен. Задавайте `args` всякий раз, когда хук ссылается на [плейсхолдер пути](#reference-scripts-by-path), поскольку каждый элемент передаётся как один аргумент без экранирования кавычками. Опускайте `args`, если вам нужны возможности оболочки, такие как конвейеры или `&&`, или если ни одно из этих соображений не применимо.

**Форма exec** используется, когда `args` присутствует. Claude Code разрешает `command` как исполняемый файл в `PATH` и запускает его напрямую с `args` в качестве вектора аргументов. Оболочки нет, поэтому каждый элемент `args` — это ровно один аргумент в том виде, в котором он написан, а плейсхолдеры путей, такие как `${CLAUDE_PLUGIN_ROOT}`, подставляются в `command` и в каждый элемент `args` как обычные строки. Специальные символы, такие как апострофы, `$` и обратные кавычки, передаются как есть, поскольку нет оболочки, которая бы их интерпретировала. Токенизация оболочкой не выполняется ни на одной платформе.

**Форма shell** используется, когда `args` отсутствует. Строка `command` передаётся оболочке: `sh -c` в macOS и Linux, Git Bash в Windows или PowerShell, если Git Bash не установлен. Задайте поле `shell`, чтобы выбрать явно. Оболочка токенизирует строку, раскрывает переменные и интерпретирует конвейеры, `&&`, перенаправления и glob-шаблоны.

> [!NOTE]
>
> В Windows форма exec требует, чтобы `command` разрешался в настоящий исполняемый файл, например `.exe`. Прослойки `.cmd` и `.bat`, которые npm, npx, eslint и другие инструменты устанавливают в `node_modules/.bin`, не являются исполняемыми файлами и не могут быть запущены без оболочки. Чтобы запустить их в форме exec, вызовите базовый скрипт напрямую через `node`, например `"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/node_modules/eslint/bin/eslint.js"]`. Шаблон «`node` плюс путь к скрипту» работает на любой платформе, поскольку `node.exe` — настоящий двоичный файл. Чтобы запустить прослойку `.cmd` или `.bat` по имени, используйте форму shell.

Этот пример запускает Node-скрипт, поставляемый с плагином. Форма exec передаёт разрешённый путь к скрипту как один аргумент без экранирования кавычками:

```json theme={null}
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

Эквивалентная форма shell требует кавычек для обработки путей с пробелами или специальными символами:

```json theme={null}
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

Обе формы поддерживают одни и те же [плейсхолдеры путей](#reference-scripts-by-path), и обе экспортируют их как переменные окружения `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT` и `CLAUDE_PLUGIN_DATA` в запущенный процесс, поэтому скрипт может читать `process.env.CLAUDE_PLUGIN_ROOT` независимо от того, как он был запущен.

Хуки плагинов дополнительно подставляют значения [`${user_config.*}`](https://code.claude.com/docs/ru/plugins/manifest-reference#user-configuration), только в форме exec: значение подставляется в `command` и в каждый элемент `args` как обычная строка, поэтому никакая оболочка не разбирает его повторно.

Хук плагина в форме shell, у которого `command` ссылается на `${user_config.*}`, завершается [ошибкой](https://code.claude.com/docs/ru/errors.md#plugin-command-references-user-config) вместо запуска. Чтобы использовать значение параметра из хука в форме shell, читайте переменную окружения `$CLAUDE_PLUGIN_OPTION_<KEY>`, например `$CLAUDE_PLUGIN_OPTION_WEBHOOK_URL` для параметра `webhook_url`, или задайте `args`, чтобы переключить хук в форму exec. До v2.1.207 команды хуков плагинов в форме shell также подставляли `${user_config.*}`.

> [!NOTE]
>
> В форме exec `command` — это только имя или путь исполняемого файла. Если `command` — голое имя без разделителя пути и содержит пробелы при наличии `args`, Claude Code записывает в лог предупреждение, поскольку запуск завершится неудачей: исполняемого файла с именем `node script.js` не существует. Перенесите лишние токены в `args`. Абсолютные пути с пробелами, такие как `C:\Program Files\nodejs\node.exe`, являются одним допустимым исполняемым файлом и не вызывают предупреждения.

#### Поля HTTP-хука

Помимо [общих полей](#common-fields), HTTP-хуки принимают следующие поля:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `url` | да | URL, на который отправляется POST-запрос |
| `headers` | нет | Дополнительные HTTP-заголовки в виде пар «ключ-значение». Значения поддерживают подстановку переменных окружения с помощью синтаксиса `$VAR_NAME` или `${VAR_NAME}`. Разрешаются только переменные, перечисленные в `allowedEnvVars` |
| `allowedEnvVars` | нет | Список имён переменных окружения, которые можно подставлять в значения заголовков. Ссылки на неперечисленные переменные заменяются пустыми строками. Требуется для работы любой подстановки переменных окружения |
| `onFailure` | нет | Выполняется ли действие, вызвавшее хук, если хук завершился сбоем: `"continue"` или `"block"`. О `"block"` и о случае, когда поле не задано, см. [Блокировка действия при сбое хука](#block-the-action-when-a-hook-fails). Требуется Claude Code v2.1.295 или новее |

Claude Code отправляет [входные данные JSON](#hook-input-and-output) хука как тело POST-запроса с `Content-Type: application/json`. Тело ответа использует тот же [формат вывода JSON](#json-output), что и командные хуки.

Обработка ошибок отличается от командных хуков; см. [Обработка HTTP-ответов](#http-response-handling).

Этот пример отправляет события `PreToolUse` в локальный сервис проверки, аутентифицируясь токеном из переменной окружения `MY_TOKEN`:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### Поля хука MCP-инструмента

Помимо [общих полей](#common-fields), хуки MCP-инструментов принимают следующие поля:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `server` | да | Имя настроенного MCP-сервера. Для [сервера, поставляемого с плагином](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers), это имя с областью `plugin:<plugin-name>:<server-name>`, например `plugin:my-plugin:db`, а не голый ключ сервера |
| `tool` | да | Имя инструмента, вызываемого на этом сервере |
| `input` | нет | Аргументы, передаваемые инструменту. Строковые значения поддерживают подстановку `${path}` из [входных данных JSON](#hook-input-and-output) хука, например `"${tool_input.file_path}"` |

Этот пример вызывает инструмент `security_scan` на MCP-сервере `my_server` после каждого `Write` или `Edit`, передавая путь к отредактированному файлу:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

##### Как читается результат инструмента

Claude Code читает текстовое содержимое инструмента так же, как stdout командного хука, следуя [правилу разбора для кода выхода 0](#exit-code-0). Если инструмент возвращает `isError: true`, хук выдаёт неблокирующую ошибку, и выполнение продолжается.

Если ошибка хука содержит одно из этих сообщений, Claude Code не смог прочитать ответ инструмента, поэтому хук не вынес вердикта:

```text theme={null}
MCP tool "security_scan" on server "my_server" gave no answer that could be read, because a message from the server was too large, so this hook gave no verdict. If this keeps happening, the tool must send a smaller answer.
MCP tool "security_scan" on server "my_server" answered without its text, which happens when a result is too large, so this hook gave no verdict. If this keeps happening, the tool must send a smaller answer.
```

В `PreToolUse` Claude Code отклоняет вызов инструмента, который проверял хук. В других событиях, таких как `UserPromptSubmit`, `PostToolUse` и `Stop`, ошибка является неблокирующей.

Если ошибка продолжает появляться, возвращайте из инструмента меньше данных или измените [`tool` или `input`](#mcp-tool-hook-fields) хука, чтобы ответ был меньше.

##### Когда сервер ещё подключается

В событиях, где хук может заблокировать или изменить результат, таких как `PreToolUse` или `Stop`, Claude Code ожидает подключающийся сервер, прежде чем вызвать инструмент, не дольше [`MCP_TIMEOUT`](https://code.claude.com/docs/ru/env-vars) и в пределах собственного [`timeout`](#common-fields) хука. В наблюдательных событиях, таких как `Notification` или `SessionEnd`, он не ждёт.

Сервер со [статусом `cached`](https://code.claude.com/docs/ru/mcp#server-status-detail) подключается, когда хук вызывает его инструмент. Если в этот момент сервер не подключён, хук выдаёт неблокирующую ошибку, и выполнение продолжается. Хук никогда не запускает процесс OAuth, поэтому сначала [аутентифицируйте сервер через `/mcp`](https://code.claude.com/docs/ru/mcp#authenticate-with-remote-mcp-servers).

##### События, которые срабатывают до того, как MCP-серверы становятся доступны

`SessionStart` при запуске, в том числе с `--continue` или `--resume`, и каждое событие `Setup` срабатывают до того, как MCP-серверы сессии становятся доступны хукам. Claude Code пропускает их хуки `mcp_tool`, не вызывая инструмент, а в [лог отладки](#debug-hooks) записывается `mcp_tool hooks are not available for the 'SessionStart' hook event (no MCP client context)` или то же сообщение с упоминанием `Setup`. Когда `SessionStart` срабатывает снова позже в сессии, после `/clear` или сжатия контекста, его хуки `mcp_tool` запускаются. Для всего, что нужно сессии при запуске, используйте вместо этого хук `type: "command"` в `SessionStart`.

#### Поля хуков с промптом и хуков агентов

Помимо [общих полей](#common-fields), хуки с промптом и хуки агентов принимают следующие поля:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `prompt` | да | Текст промпта, отправляемого модели. Используйте `$ARGUMENTS` как плейсхолдер для входных данных JSON хука. Экранируйте обратной косой чертой, чтобы включить буквальный текст: `\$1.00` отображается как `$1.00` |
| `model` | нет | Модель для оценки. По умолчанию используется модель, которую Claude Code использует для [фоновой функциональности](https://code.claude.com/docs/ru/model-config.md#environment-variables) |

### Ссылки на скрипты по пути

Используйте эти плейсхолдеры, чтобы ссылаться на скрипты хуков относительно корня проекта или плагина, независимо от рабочего каталога в момент запуска хука:

* `${CLAUDE_PROJECT_DIR}`: корень проекта, в котором началась сессия. Claude Code также задаёт эту переменную в окружении [stdio MCP-серверов](https://code.claude.com/docs/ru/mcp.md#option-3-add-a-local-stdio-server) и LSP-серверов плагинов.
* `${CLAUDE_PLUGIN_ROOT}`: каталог установки плагина, для скриптов, поставляемых с [плагином](https://code.claude.com/docs/ru/plugins/overview.md). О том, как ведёт себя путь при обновлениях, см. [переменные окружения плагинов](https://code.claude.com/docs/ru/plugins/manifest-reference.md#environment-variables).
* `${CLAUDE_PLUGIN_DATA}`: [каталог постоянных данных](https://code.claude.com/docs/ru/plugins/components.md#path-variables-and-persistent-data) плагина, для зависимостей и состояния, которые должны сохраняться при обновлениях плагина.

> [!NOTE]
>
> **С worktree всё иначе.** Если Claude входит в [worktree](https://code.claude.com/docs/ru/worktrees.md) во время сессии, Claude Code оставляет `${CLAUDE_PROJECT_DIR}` там, где он был, и передаёт путь worktree вашим хукам другим способом:
>
> * **`${CLAUDE_PROJECT_DIR}` остаётся на месте**: он по-прежнему указывает на корень проекта, в котором началась сессия, поэтому команда вроде `${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh` по-прежнему запускает скрипт в основной рабочей копии.
> * **`cwd` следует за Claude**: поле `cwd` во [входных данных JSON](#common-input-fields) хука — это корень worktree после того, как Claude входит в worktree, и новый каталог после того, как Claude выполняет `cd`. Читайте его, когда хуку нужно знать, в каком каталоге работает Claude.
>
> О сессии в worktree, которую вы запускаете из десктопного приложения, и о том, куда указывает `${CLAUDE_PROJECT_DIR}`, см. [Что worktree разделяют с основной рабочей копией](https://code.claude.com/docs/ru/worktrees.md#what-worktrees-share-with-the-main-checkout).

Для любого хука, ссылающегося на плейсхолдер пути, предпочитайте [форму exec](#exec-form-and-shell-form). В форме shell заключайте каждый плейсхолдер в двойные кавычки.

> [tab] Скрипты проекта
>
> Этот пример использует `${CLAUDE_PROJECT_DIR}` для запуска средства проверки стиля из каталога `.claude/hooks/` проекта после любого вызова инструмента `Write` или `Edit`:
>
> ```json theme={null}
> {
>   "hooks": {
>     "PostToolUse": [
>       {
>         "matcher": "Write|Edit",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh",
>             "args": []
>           }
>         ]
>       }
>     ]
>   }
> }
> ```

> [tab] Скрипты плагинов
>
> Определяйте хуки плагина в `hooks/hooks.json` с необязательным полем `description` верхнего уровня. Когда плагин включён, его хуки объединяются с вашими пользовательскими и проектными хуками.
>
> Этот пример запускает скрипт форматирования, поставляемый с плагином:
>
> ```json theme={null}
> {
>   "description": "Automatic code formatting",
>   "hooks": {
>     "PostToolUse": [
>       {
>         "matcher": "Write|Edit",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
>             "args": [],
>             "timeout": 30
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Подробнее о создании хуков плагинов см. в [справочнике по компонентам плагинов](https://code.claude.com/docs/ru/plugins/components.md#hooks).

### Хуки в скиллах и агентах

Помимо файлов настроек и плагинов, хуки можно определять непосредственно в [скиллах](https://code.claude.com/docs/ru/skills.md) и [субагентах](https://code.claude.com/docs/ru/sub-agents.md) с помощью frontmatter, в том же формате конфигурации, что и хуки на основе настроек. То, как долго Claude Code держит их зарегистрированными, зависит от компонента:

* **Хуки субагентов**: Claude Code запускает их только во время работы этого субагента и удаляет, когда он завершается. Claude Code преобразует хук `Stop` здесь в `SubagentStop` — событие, которое срабатывает при завершении субагента.
* **Хуки скиллов**: Claude Code регистрирует их, когда вы или Claude вызываете скилл, и продолжает запускать их до конца сессии, в том числе на ходах после собственного хода скилла. Чтобы Claude Code вместо этого удалял хук после его первого успешного запуска, задайте для него [`once: true`](#common-fields).

Этот скилл определяет хук `PreToolUse`, который запускает скрипт проверки безопасности перед каждой командой `Bash`:

```yaml theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: '"${CLAUDE_PROJECT_DIR}"/scripts/security-check.sh'
---
```

Субагенты используют тот же формат в своём YAML frontmatter.

Хуки во frontmatter проектного скилла следуют тому же [правилу доверия к рабочему пространству, что и хуки в файлах настроек](#workspace-trust). Claude Code регистрирует их, когда вы или Claude вызываете скилл, в том числе при запуске с `-p` в папке, которой вы не доверяете.

Хуки во frontmatter проектного субагента запускаются только после того, как вы примете [диалоговое окно доверия к рабочему пространству](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust) для папки, из которой взят файл агента. Сессия `-p` не считается его принятием. В разделе [Что запускается до того, как вы доверитесь папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) это сравнивается с правилом для файлов настроек, а на странице субагентов перечислено, [какие области действия освобождены](https://code.claude.com/docs/ru/sub-agents.md#hooks-in-subagent-frontmatter).

#### Ограничения хуков скиллов

Если хуки во frontmatter скилла не срабатывают после того, как вы или Claude вызвали скилл, выполните [`/hooks`](#the-%2Fhooks-menu) в этой сессии. Если они там перечислены, см. [Хук не срабатывает](https://code.claude.com/docs/ru/hooks-guide.md#hook-not-firing). Если ни один из них не перечислен, скилл может находиться под блокировкой «только плагины» или превышать лимит хуков и работает без каких-либо своих хуков из frontmatter. Проверьте каждый случай:

* **Блокировка «только плагины»**: администратор вашей организации может ограничить хуки плагинами и управляемыми настройками с помощью управляемой настройки [`strictPluginOnlyCustomization`](https://code.claude.com/docs/ru/settings-reference#strictpluginonlycustomization-hooks). При такой блокировке скилл сохраняет свои хуки из frontmatter, только если это скилл плагина, [встроенный скилл](https://code.claude.com/docs/ru/skills.md#bundled-skills) или скилл в [каталоге управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms). Хуки в ваших собственных файлах настроек тоже не запускаются.
  * **Проверка**: введите `/status` в сессии Claude Code. Если [строка `Setting sources`](https://code.claude.com/docs/ru/settings#check-what-your-organization-enforces) содержит `Enterprise managed settings`, спросите администратора, блокирует ли `strictPluginOnlyCustomization` хуки.
  * **Исправление**: перенесите скилл в [плагин](https://code.claude.com/docs/ru/plugins/create.md#convert-an-existing-claude-setup), поскольку скиллы плагинов сохраняют свои хуки из frontmatter. Добавьте плагин в [маркетплейс](https://code.claude.com/docs/ru/plugins/create-marketplace.md#create-a-marketplace), а затем установите его оттуда. Если Claude Code отклоняет маркетплейс с сообщением [`is blocked by enterprise policy`](https://code.claude.com/docs/ru/plugins/troubleshooting#marketplace-source-is-blocked-by-enterprise-policy), попросите администратора разрешить этот маркетплейс.
* **Лимит хуков**: в Claude Code v2.1.304 или новее у каждого источника скиллов есть собственный лимит на сессию. Ваш проект, ваша папка личных скиллов и каждый плагин считаются отдельными источниками. Скиллы из одного источника могут зарегистрировать не более 1 024 хуков. Matcher этих хуков в сумме могут содержать не более 16 384 символов. Matcher, под которым находится несколько хуков, учитывается один раз для каждого хука.
  * **Проверка**: повторите сессию, в которой хук не сработал, с включённым логированием отладки:
    1. Запустите новую сессию из оболочки с помощью `claude --debug`. Если вы не запускаете сессии из оболочки, вместо этого сначала введите [`/debug`](https://code.claude.com/docs/ru/commands#all-commands) в новой сессии.
    2. Вызовите те же скиллы в том же порядке, включая те, которые вызывал Claude, поскольку оба итоговых значения накапливаются скилл за скиллом. Попросите Claude вызвать любой скилл, который вы не можете ввести как команду.
    3. Найдите в [логе отладки](#debug-hooks) `registers none of its hooks`. Строка с этим текстом называет скилл, который превысил лимит.
  * **Исправление**: объявите меньше хуков или более короткие matcher в этом скилле или в других скиллах из его источника, затем начните новую сессию. Если эти скиллы не ваши и вы не можете их редактировать, попросите их автора внести это изменение. До тех пор начинайте новую сессию и вызывайте нужный скилл раньше любого другого скилла из его источника.

Если ни один из случаев не ваш, проверьте, нет ли [frontmatter, который не удалось разобрать](https://code.claude.com/docs/ru/skills.md#skill-not-triggering).

### Меню `/hooks`

Введите `/hooks` в Claude Code, чтобы открыть браузер настроенных хуков только для чтения. В списке каждый хук помечен источником, например пользовательские настройки, проектные настройки, локальные настройки, плагин или текущая сессия.

Выберите хук, чтобы увидеть полный текст того, что он запускает, и место, где он определён, например путь к его файлу настроек или имя его плагина.

Чтобы просмотреть все события хуков, включая те, для которых хуки не настроены, выберите `All events` в конце списка.

### Отключение или удаление хуков

Чтобы удалить хук, определённый в файле настроек, удалите его запись из этого файла.

Чтобы временно отключить все хуки, не удаляя их, задайте `"disableAllHooks": true` в файле настроек. Claude Code читает значение, оставшееся после применения [приоритета настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence), поэтому `"disableAllHooks": false` в `.claude/settings.json` проекта переопределяет `true` в ваших пользовательских настройках. Чтобы отключить хуки для одного запуска независимо от настроек проекта, передайте `--settings '{"disableAllHooks": true}'`, что имеет приоритет над проектными и локальными настройками. Способа отключить отдельный хук, сохранив его в конфигурации, нет.

Настройка `disableAllHooks` учитывает иерархию управляемых настроек. Если администратор настроил хуки через настройки управляемой политики, `disableAllHooks`, заданный в пользовательских, проектных или локальных настройках, не может отключить эти управляемые хуки. Только `disableAllHooks`, заданный на уровне управляемых настроек, может отключить управляемые хуки. О полном охвате каждого уровня см. [`disableAllHooks`](https://code.claude.com/docs/ru/settings-reference#disableallhooks).

Прямые изменения хуков в файлах настроек обычно подхватываются автоматически средством отслеживания файлов.

## Входные и выходные данные хуков

Командные хуки получают данные JSON через stdin и сообщают результаты через коды выхода, stdout и stderr. HTTP-хуки получают тот же JSON в теле POST-запроса и сообщают результаты через тело HTTP-ответа. В этом разделе описаны поля и поведение, общие для всех событий. Раздел каждого события в [Событиях хуков](#hook-events) содержит его собственную схему входных данных и параметры управления решениями.

В macOS и Linux командные хуки выполняются в собственной сессии без управляющего терминала. Процесс хука и любые дочерние процессы не могут открыть `/dev/tty` или отправлять escape-последовательности напрямую в интерфейс Claude Code. В Windows `/dev/tty` отсутствует.

Чтобы показать сообщение пользователю на любой платформе, верните [`systemMessage`](#json-output) в выводе JSON. Некоторые события отбрасывают его или доставляют в другое место, и [раздел каждого события](#hook-events) об этом сообщает. Чтобы вызвать уведомление на рабочем столе, задать заголовок окна или подать звуковой сигнал, верните вместо этого [`terminalSequence`](#emit-terminal-notifications).

### Общие поля входных данных

События хуков получают эти поля в формате JSON в дополнение к специфичным для события полям, описанным в разделе каждого [события хука](#hook-events). Для командных хуков этот JSON поступает через stdin. Для HTTP-хуков он поступает в теле POST-запроса.

| Поле | Описание |
| :- | :- |
| `session_id` | Идентификатор текущей сессии |
| `prompt_id` | UUID, идентифицирующий промпт пользователя, который обрабатывается в данный момент. Совпадает с [атрибутом `prompt.id` в событиях OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage#event-correlation-attributes), поэтому вы можете сопоставить вывод хука с телеметрией для отдельного промпта. Отсутствует до первого ввода пользователя |
| `transcript_path` | Путь к JSON диалога. Файл транскрипта записывается асинхронно и может отставать от диалога в памяти, поэтому в момент срабатывания хука он может ещё не содержать самые последние сообщения текущего хода. Хукам, которым нужен итоговый текст ассистента текущего хода, следует использовать `last_assistant_message` в [Stop](#stop) и [SubagentStop](#subagentstop) вместо чтения транскрипта |
| `cwd` | Текущий рабочий каталог на момент вызова хука |
| `scratchpad_dir` | Путь к [каталогу scratchpad](https://code.claude.com/docs/ru/claude-directory.md#session-scratchpad-directory) сессии, где Claude хранит временные рабочие файлы. Отсутствует, если у сессии нет scratchpad или временный каталог недоступен. Требуется Claude Code v2.1.257 или новее |
| `permission_mode` | Текущий [режим разрешений](https://code.claude.com/docs/ru/permissions.md#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` или `"bypassPermissions"`. Режим с меткой **Manual** передаётся как `"default"`, а не как `"manual"`, поэтому скрипты, проверяющие `"default"`, продолжают работать. Не все события получают это поле. Смотрите пример JSON в разделе каждого [события хука](#hook-events) |
| `effort` | Объект, поле `level` которого содержит настройку [уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) на момент выполнения хука, включая уровень скилла, субагента или `ultrathink`: `"low"`, `"medium"`, `"high"`, `"xhigh"` или `"max"`. Присутствует для `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop` и других событий с контекстом использования инструментов на моделях, поддерживающих effort. Если модель не поддерживает ваш уровень, `level` содержит уровень, с которым фактически выполнялась работа. Изменённый вами уровень может отображаться здесь до того, как он [вступит в силу](https://code.claude.com/docs/ru/model-config.md#when-a-new-effort-level-starts). `$CLAUDE_EFFORT` содержит тот же уровень. |
| `hook_event_name` | Имя сработавшего события |

`agent_id` и `agent_type` сообщают вашему скрипту, в каком агенте сработал хук, например в субагенте, [участнике команды, работающем в том же процессе](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), или агенте, выбранном с помощью `--agent`:

| Поле | Описание |
| :- | :- |
| `agent_id` | Уникальный идентификатор субагента или участника команды в том же процессе, в котором срабатывает хук. |
| `agent_type` | Имя агента (например, `"Explore"` или `"security-reviewer"`). Присутствует, если сессия использует `--agent` или хук срабатывает внутри субагента. Для субагентов тип субагента имеет приоритет над значением `--agent` сессии. Смотрите [SubagentStart](#subagentstart), чтобы узнать, какие значения сообщают пользовательские субагенты и субагенты плагинов и как написать matcher для имени с областью действия плагина. |

Только хуки [`SessionStart`](#sessionstart) могут получать поле `model`, и Claude Code не всегда его включает. Хуки [`PreModelSwitch`](#premodelswitch) и [`PostModelSwitch`](#postmodelswitch) вместо этого получают `from_model` и `to_model`, поэтому используйте хук PostModelSwitch, чтобы отслеживать модель при её смене в ходе сессии.

Переменной окружения `$CLAUDE_MODEL` не существует. Хук может прочитать `$ANTHROPIC_MODEL`, если вы задали её в своей оболочке, но это значение не меняется, когда вы переключаете модели с помощью `/model` в ходе сессии.

Процесс хука наследует родительское окружение, за исключением переменных экспортёра `OTEL_*`, которые Claude Code [удаляет из каждого запускаемого им подпроцесса](https://code.claude.com/docs/ru/monitoring-usage.md#administrator-configuration), и, если [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](https://code.claude.com/docs/ru/env-vars#variables) установлена в `1`, переменных, которые он при этом удаляет. В сессии, которая [получает конфигурацию HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md#check-how-developers-sign-in-and-connect), Claude Code также [удаляет учётные данные Anthropic](https://code.claude.com/docs/ru/hipaa-setup.md#anthropic-credentials-in-commands-hooks-and-mcp-servers) из окружения хука.

Например, хук `PreToolUse` для команды Bash получает через stdin следующее:

```json theme={null}
{
  "session_id": "abc123",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "scratchpad_dir": "/tmp/claude-1000/-home-user-my-project/abc123/scratchpad",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite",
    "timeout": 120000,
    "run_in_background": false
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

Поля `tool_name`, `tool_input` и `tool_use_id` специфичны для события. Раздел каждого [события хука](#hook-events) описывает дополнительные поля для этого события.

### Вывод через код выхода

Когда выполнение вашего хука завершается, Claude Code по его коду выхода решает, продолжать ли действие, которое вызвало хук, например вызов инструмента или промпт:

* **Успех**: ваш хук завершается с кодом 0. Claude Code применяет все поля [вывода JSON](#json-output), которые вывел ваш хук, и действие выполняется, если эти поля не блокируют и не отклоняют его. Исключение описано в разделе [Хуки, запускающие фоновый процесс](#hooks-that-start-a-background-process).
* **Блокирующая ошибка**: ваш хук завершается с кодом 2. Для [событий, которые могут блокировать](#exit-code-2-behavior-per-event), Claude Code останавливает действие.
* **Неблокирующая ошибка**: ваш хук завершается с любым другим кодом или завершается сбоем иным образом, например не запускается или выводит некорректный JSON. Действие выполняется, за исключением хуков, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails), например хука с `onFailure`, установленным в `"block"`. Для таких событий, как `PreToolUse`, в транскрипте отображается уведомление `<hook name> hook error`.

То, что ваш хук выводит в stdout, может изменить результат. Например, если хук `PreToolUse` завершается с кодом 1, но выводит JSON, прошедший проверку, этот JSON всё равно может определить, что произойдёт. Чтобы узнать результат вашего хука для такого события, как `PreToolUse`, найдите в первом столбце то, что он вывел в stdout, а в верхней строке — его код выхода:

| Stdout | Выход с кодом 0 | Выход с кодом 2 | Любой другой код выхода |
| :- | :- | :- | :- |
| Объект JSON, прошедший [проверку схемы](#json-output) | Успех. Поля применяются | Блокирующая ошибка. Claude Code всё равно читает поля, но вызов `PreToolUse` остаётся заблокированным, даже если вы возвращаете `"allow"` или `continue: false`. Для других событий смотрите [Код выхода 2](#exit-code-2) | Успех. Claude Code игнорирует код выхода, и результат определяют только поля. Для хуков, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails), запуск вместо этого считается сбоем |
| JSON, который [не удаётся разобрать](#exit-code-0) или который не прошёл проверку схемы | Неблокирующая ошибка. Уведомление содержит сообщение о разборе или проверке | Блокирующая ошибка. Причиной служит ваш stderr | Неблокирующая ошибка. Уведомление содержит сообщение о разборе или проверке |
| [Обычный текст](#exit-code-0) или ничего | Успех | Блокирующая ошибка. Причиной служит ваш stderr | Неблокирующая ошибка. Уведомление содержит первую строку вашего stderr |

У некоторых событий собственные правила:

* **`WorktreeCreate`**: любой ненулевой код выхода приводит к ошибке создания worktree, что бы ни содержал ваш JSON.
* **`WorktreeRemove`**: любой ненулевой код выхода приводит к ошибке удаления worktree, если каталог после этого всё ещё существует.
* **`Stop`, `SubagentStop`, `TaskCompleted` и хук `UserPromptSubmit` плагина**: если ваш хук завершается с кодом 2, ничего не выводит в stdout, а его stderr сообщает об отсутствии файла, например `No such file or directory`, Claude Code обрабатывает запуск как неблокирующую ошибку.
* **`Elicitation` и `ElicitationResult`**: Claude Code применяет ваш `hookSpecificOutput`, когда хук завершается с кодом 0, и игнорирует его при любом другом коде выхода.
* **События, отбрасывающие вывод хука, такие как `StopFailure`**: Claude Code игнорирует ваш JSON при любом коде выхода, за исключением полей с побочными эффектами, таких как `terminalSequence`, которые всё равно срабатывают.

Чтобы узнать, что делает код выхода 2 для вашего события, смотрите [Поведение кода выхода 2 для каждого события](#exit-code-2-behavior-per-event). Чтобы узнать, какие поля решений оно учитывает, смотрите [Управление решениями](#decision-control).

#### Код выхода 0

Выход с кодом 0 означает успех и является предполагаемым кодом выхода, когда вы выводите JSON для структурированного управления. Если ваш хук завершается с кодом 0, но выводит JSON, который не удаётся разобрать или который не проходит [проверку схемы](#json-output), действие выполняется, если хук не относится к тем, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails). Вместо успеха с применёнными полями запуск считается [неблокирующей ошибкой](#exit-code-output).

Если уведомление `<hook name> hook error` содержит сообщение об ошибке разбора или проверки, используйте его, чтобы исправить вывод. Для хука, который не является [асинхронным](#how-async-hooks-execute), ваш stdout считается [выводом JSON](#json-output), только если вы выводите один объект JSON (на одной строке или на нескольких), вокруг которого нет ничего, кроме пробельных символов. Любой другой stdout Claude Code воспринимает как обычный текст или как ошибку разбора:

* **Вывод, который не начинается с `{` или начинается с `{`, но не заканчивается `}`**: обычный текст. По этому правилу массив JSON и строка JSON в кавычках считаются обычным текстом.
* **Две или более строк, каждая из которых по отдельности разбирается как JSON, причём первая начинается с `{`, а последняя заканчивается `}`**: обычный текст, если ни одна строка не является объектом вывода JSON, задающим какое-либо поле. Если такая строка есть, вывод считается ошибкой разбора, поэтому выводите этот объект, не добавляя в stdout ничего другого.
* **Всё остальное, что начинается с `{` и заканчивается `}`, но не является корректным JSON**: ошибка разбора.

Для следующих событий ваш stdout с обычным текстом доходит до Claude или до сводки сжатия контекста:

* **`UserPromptSubmit`, `UserPromptExpansion`, `SessionStart` и `PostModelSwitch`**: Claude Code добавляет обычный текст из stdout как контекст, который Claude может видеть и учитывать. Stdout, который ему не удалось разобрать, Claude Code не добавляет.
* **`PreCompact`**: ваш stdout становится [инструкциями для сводки сжатия контекста](#precompact-output)

Claude никогда не видит stderr хука, завершившегося с кодом 0. Чтобы прочитать его самостоятельно для таких событий, как `PreToolUse`, включите [отладочное логирование](#debug-hooks). Чтобы передать предупреждение Claude из хука `PostToolUse` или `PostToolUseFailure`, вместо этого выйдите с кодом 2, чтобы [Claude увидел stderr](#exit-code-2-behavior-per-event), хотя инструмент уже выполнился.

#### Код выхода 2

Завершитесь с кодом 2, чтобы заблокировать действие. Для [событий, которые могут блокировать](#exit-code-2-behavior-per-event), Claude Code останавливает действие: например, хук `PreToolUse` блокирует вызов инструмента, а хук `UserPromptSubmit` отклоняет промпт.

Сообщением, сопровождающим блокировку, служит stderr вашего хука. Если ваш хук также вывел JSON с блокирующим решением, Claude Code вместо этого использует причину из этого решения.

Выход с кодом 2 по-прежнему блокирует при большей части JSON, который выводит ваш хук:

* **JSON, задающий `continue: false`**: для таких событий, как `Stop` и `SubagentStop`, это поле имеет приоритет над кодом выхода 2, поэтому Claude или субагент завершает свой ход. Чтобы Claude или субагент продолжал работу, не указывайте это поле. Для `PreToolUse` вызов инструмента остаётся заблокированным как с этим полем, так и без него.
* **Другой JSON, прошедший проверку схемы**: Claude Code по-прежнему читает поля [вывода JSON](#json-output). Даже `permissionDecision` со значением `"allow"` не пропускает действие. Для `Elicitation` и `ElicitationResult` поле `hookSpecificOutput` хука, завершившегося с кодом 2, игнорируется.
* **JSON, не прошедший проверку схемы**: хук всё равно блокирует. Claude Code использует ваш stderr как причину блокировки и записывает ошибку проверки в отладочный лог.

Этот скрипт блокирует команды `rm`, завершаясь с кодом 2, и оставляет все остальные команды обычному процессу разрешений:

```bash theme={null}
#!/bin/bash
# Reads JSON input from stdin, checks the command
input=$(cat)
command=$(jq -r '.tool_input.command' <<<"$input")

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # No decision: the normal permission flow applies
```

Если этот скрипт зарегистрирован как хук `PreToolUse` для `Bash`, команда, начинающаяся с `rm`, блокируется, а Claude получает stderr хука как ошибку инструмента с префиксом из имени события, имени инструмента и команды хука:

```text theme={null}
PreToolUse:Bash hook error: [${CLAUDE_PROJECT_DIR}/.claude/hooks/no-rm.sh]: Blocked: rm commands are not allowed
```

#### Другие коды выхода

Уведомление `<hook name> hook error` с `Failed with non-blocking status code:` означает, что код выхода вашего хука не был равен 0 или 2, а его stdout содержал обычный текст или был пустым. Запуск считается [неблокирующей ошибкой](#exit-code-output), поэтому ваш хук не остановил действие. Если уведомление обрезает ваш stderr, включите отладочное логирование, как описано в разделе [Отладка хуков](#debug-hooks), и запустите хук повторно.

Например, если хук `PreToolUse` для `Bash` выводит `something broke` в stderr и завершается с кодом 1, уведомление `PreToolUse:Bash hook error` содержит такую строку:

```text theme={null}
Failed with non-blocking status code: something broke
```

Если уведомление содержит сообщение оболочки `No such file or directory`, как в следующей строке, хук так и не был запущен, например потому что путь к его скрипту не существует:

```text theme={null}
Failed with non-blocking status code: /bin/sh: /path/to/hook.sh: No such file or directory
```

Если путь неверен, исправьте его там, где настроен хук. В форме оболочки, если путь к скрипту не существует или файл не является исполняемым, оболочка завершается с кодом вроде 127, и уведомление содержит сообщение интерпретатора. Если хук не относится к тем, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails), хук, который не удаётся запустить, тоже считается неблокирующей ошибкой.

Настраивая хук для политики, следите за этим уведомлением при его первом запуске, потому что опечатка в пути в `settings.json` означает, что хук никогда не выполнится. Чтобы блокировать действие, когда хук не удаётся запустить, установите [`onFailure: "block"`](#block-the-action-when-a-hook-fails).

> [!WARNING]
>
> Код выхода 1 без корректного вывода JSON является неблокирующей ошибкой, если хук не относится к тем, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails), хотя 1 — общепринятый код ошибки в Unix. Если ваш хук предназначен для соблюдения политики, используйте `exit 2`.

#### Таймауты

За исключением командного хука, запущенного с [`async: true`](#run-hooks-in-the-background), Claude Code отменяет хук `command`, `http` или `mcp_tool`, достигший своего [`timeout`](#common-fields), и отбрасывает вывод хука, поэтому для большинства событий хук, превысивший таймаут, не выносит никакого решения. Для [`PreModelSwitch`](#premodelswitch) хук, отменённый по таймауту, блокирует переключение модели.

Для `PreToolUse` хук `command`, `http` или `mcp_tool`, превысивший таймаут, не блокирует вызов инструмента, за исключением хуков, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails). Вызов продолжается через обычный [процесс разрешений](https://code.claude.com/docs/ru/permissions.md), поэтому не рассчитывайте, что зависший хук сработает как защитный барьер. Чтобы блокировать вызов при превышении таймаута хуком `command` или `http`, установите [`onFailure: "block"`](#block-the-action-when-a-hook-fails). [Callback-хук Agent SDK](https://code.claude.com/docs/ru/agent-sdk/hooks.md), превысивший свой таймаут, [блокирует вызов инструмента](#pretooluse).

> [!NOTE]
>
> Если вы используете Code Mode, таймауты для `PreToolUse` работают иначе. Смотрите [Вызов инструмента отклонён хуком](https://code.claude.com/docs/ru/code-mode.md#tool-call-refused-by-a-hook).

#### Хуки, запускающие фоновый процесс

Хук может запустить долго работающую программу, например сервер разработки, и оставить её работать, пока сессия продолжается. В скрипте хука или в команде в [форме оболочки](#exec-form-and-shell-form):

* Запустите программу в фоновом режиме
* Перенаправьте её stdout и stderr. Например, команда Bash `npm run dev > dev-server.log 2>&1 &` направляет оба потока в файл. Если вы их не перенаправите, хуку, который не является [асинхронным](#run-hooks-in-the-background), требуется до 10 секунд, чтобы завершиться после выхода собственного процесса.

Если ваш командный хук принимает решение в фоновом процессе и завершается, то отказ, который этот процесс выводит после того, как Claude Code перестал читать вывод, не блокирует вызов инструмента. Для хука, который не является [асинхронным](#run-hooks-in-the-background), Claude Code заканчивает чтение вывода хука вскоре после завершения собственного процесса хука.

Выводите решение до запуска фонового процесса и перенаправляйте stdout и stderr этого процесса. Если ваш скрипт выводит разрешение, а затем запускает фоновый процесс, не перенаправив его stdout и stderr, Claude Code блокирует вызов инструмента. Ошибка хука содержит `stdio went quiet` и `refusing to honor the suspect capture`.

Этот скрипт хука `PreToolUse` выводит решение с помощью `policy-check.sh`, а затем загружает метрики в фоновом режиме:

```bash theme={null}
#!/bin/bash
"$CLAUDE_PROJECT_DIR"/.claude/hooks/policy-check.sh || exit $?
"$CLAUDE_PROJECT_DIR"/.claude/hooks/upload-metrics.sh >/dev/null 2>&1 &
```

Остальная часть скрипта делает следующее:

* **`|| exit $?`**: делает код выхода проверки собственным кодом выхода хука, поэтому проверка, завершающаяся с кодом 2 для отказа, по-прежнему блокирует. Иначе хук завершается с кодом последней строки, то есть 0.
* **`>/dev/null 2>&1 &`**: запускает `upload-metrics.sh` в фоновом режиме с перенаправленным выводом, чтобы он не удерживал вывод хука открытым.

Чтобы проверить скрипт, сделайте так, чтобы `policy-check.sh` завершался с кодом 2, а затем вызовите инструмент, которому соответствует хук. Вызов инструмента будет заблокирован.

#### Блокировка действия при сбое хука

Для большинства событий, когда хук завершается сбоем или превышает таймаут, Claude Code всё равно выполняет действие. В результате хук политики с неверным путём или падающим скриптом пропускает всё. Чтобы вместо этого блокировать действие, установите `"onFailure": "block"` для хука `command` или `http`. Требуется Claude Code v2.1.295 или новее. О callback-хуках Agent SDK смотрите [Блокировка действия при сбое callback](https://code.claude.com/docs/ru/agent-sdk/hooks.md#block-the-action-when-a-callback-fails).

> [!NOTE]
>
> В Windows без Git Bash командный хук `PreToolUse` или `PermissionRequest` в форме оболочки, завершившийся сбоем при незаданном `onFailure`, может вместо этого [заблокировать вызов инструмента](#failed-hooks-on-windows-without-git-bash).

Этот хук `PreToolUse` в `.claude/settings.json` запускает скрипт проекта перед каждой командой Bash и блокирует команду, если скрипт завершается сбоем:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/check-command.js"],
            "onFailure": "block"
          }
        ]
      }
    ]
  }
}
```

Чтобы проверить его, не создавайте `check-command.js` и попросите Claude выполнить команду Bash, например `ls`. Claude Code блокирует вызов, и ошибка содержит `failed; blocking because onFailure is "block"`, за которым следует собственный вывод ошибки node, сокращённый здесь до одной строки:

```text theme={null}
PreToolUse:Bash hook error: [node ${CLAUDE_PROJECT_DIR}/.claude/hooks/check-command.js]: failed; blocking because onFailure is "block"
Error: Cannot find module '/path/to/project/.claude/hooks/check-command.js'
```

После таймаута сообщение содержит `timed out` вместо `failed`. Без заданного `onFailure` тот же отсутствующий скрипт является неблокирующей ошибкой, и `ls` выполняется.

Каждый из следующих случаев считается сбоем:

* **Не удаётся запустить**: командный хук не запускается, например потому что скрипт или исполняемый файл не существует
* **Код выхода, отличный от 0 или 2**: учитывается для командного хука, даже если он вывел JSON, разрешающий действие, например `permissionDecision: "allow"`. Чтобы вернуть решение в JSON, завершитесь с кодом 0
* **Ошибка HTTP**: соединение HTTP-хука не удаётся установить, или статус ответа не 2xx
* **Таймаут**: хук достигает своего [`timeout`](#common-fields)
* **Некорректный вывод**: вывод JSON [не удаётся разобрать](#exit-code-0) или он не проходит [проверку схемы](#json-output). Для HTTP-хука сбоем также считается тело ответа 2xx, которое не является ни пустым, ни объектом JSON. Обычный текст в stdout командного хука сбоем не считается

При установленном `"block"` сбой действует так же, как [код выхода 2 для этого события](#exit-code-2-behavior-per-event), за исключением `PermissionRequest`, где он отклоняет запрос. Например, сбой `PreToolUse` блокирует вызов инструмента, а сбой `UserPromptSubmit` блокирует промпт.

Поле не действует для следующих хуков:

* **Хуки `Stop`, `SubagentStop`, `TaskCompleted` и `TeammateIdle`**: код выхода 2 для этих событий отправляет Claude продолжать работу, а Claude не может исправить хук, который не запускается
* **Фоновые командные хуки**: командные хуки, в которых задано [`async` или `asyncRewake`](#run-hooks-in-the-background)

> [!NOTE]
>
> Если вы используете Code Mode, сбои для `PreToolUse` обрабатываются иначе. Смотрите [Вызов инструмента отклонён хуком](https://code.claude.com/docs/ru/code-mode.md#tool-call-refused-by-a-hook).

#### Сбой хуков в Windows без Git Bash

Если ошибка заблокированного вызова инструмента содержит этот текст, командный хук `PreToolUse` или `PermissionRequest` завершился сбоем или превысил таймаут и заблокировал вызов:

```text theme={null}
blocking because Git Bash wasn't found, so only exit code 0 or 2 counts as this hook's verdict.
```

Если ошибка также содержит `PowerShell started no program`, начните с [исправлений для `command`, состоящего только из строк в кавычках](#powershell-started-no-program), которые PowerShell выводит вместо того, чтобы выполнять.

Без Git Bash любой код выхода этого хука, отличный от 0 или 2, считается [сбоем](#block-the-action-when-a-hook-fails), даже если хук выводит JSON, который не отклоняет вызов. Чтобы узнать причину сбоя хука, проверьте [отладочный лог](#debug-hooks). Затем выберите исправление, подходящее для вашего хука:

* **Действие должно выполняться при сбое хука**: добавьте в хук [`"onFailure": "continue"`](#block-the-action-when-a-hook-fails)
* **Хук завершается с кодом 1 для предупреждения, но должен блокировать при падении**: с `"onFailure": "continue"` вызов выполняется при коде выхода 1 — как при предупреждении, так и при падении. Вместо этого добавьте `"onFailure": "block"` и завершайте скрипт с кодом 0 там, где он выдаёт предупреждение, чтобы такие вызовы выполнялись. Чтобы по-прежнему показывать предупреждение для `PreToolUse`, выведите его в stdout в поле [`systemMessage`](#json-output) одного объекта JSON.
* **Хук написан для Bash**: без Git Bash хук в [форме оболочки](#exec-form-and-shell-form) без заданного `shell` выполняется в PowerShell, где он может завершиться сбоем. Установите [Git for Windows](https://git-scm.com/downloads/win) или задайте [`CLAUDE_CODE_GIT_BASH_PATH`](https://code.claude.com/docs/ru/env-vars), если Git Bash установлен там, где Claude Code его не находит. Затем начните новую сессию.
* **Хук запускает один файл `.exe`, а не файл `.cmd` или `.bat`**: укажите программу в `command`, а её аргументы в `args`, чтобы использовать форму exec, и добавьте `"onFailure": "block"`. Тогда Claude Code запускает программу без оболочки. Без `"onFailure": "block"` вызов может выполниться, если программа завершается сбоем, отсутствует или превышает таймаут
* **Защитный хук PowerShell, который должен блокировать при сбое**: при незаданном `onFailure` он перестаёт это делать, как только установлен Git for Windows и Claude Code находит Git Bash. Добавьте `"onFailure": "block"`, чтобы сбой или таймаут блокировал вызов как с Git Bash, так и без него. Также задайте `"shell": "powershell"`, чтобы хук и дальше выполнялся в PowerShell, а не в Git Bash

До версии v2.1.309 сообщение выглядело так: `blocking because Git Bash wasn't found and this hook doesn't set "shell" to "powershell", so only exit code 0 or 2 counts as its verdict.`

#### PowerShell started no program

Хук с этой ошибкой выполнялся в PowerShell, который выводит `command`, состоящий только из строк в кавычках, например `"command": "\"C:\\Tools\\guard.exe\""`, вместо того чтобы его выполнить.

* **Чтобы вывести текст, например JSON**: задайте `"shell": "powershell"`, и хук завершится с кодом 0
* **Чтобы запустить файл `.ps1`, `.cmd` или `.bat` либо `.exe`, путь к которому содержит переменную**: задайте `"shell": "powershell"` и поставьте `&` перед путём в кавычках. Оставьте `$HOME` как есть, а переменные окружения записывайте так, как [пример `check.ps1`](#reference-scripts-by-path-in-powershell-hooks) записывает `$env:CLAUDE_PROJECT_DIR`
* **Чтобы запустить один `.exe` по пути без `$`**: удалите внутренние кавычки из `command`, затем примените [исправление для хука, запускающего один `.exe`](#failed-hooks-on-windows-without-git-bash), указав `"args": []`, если программа не принимает аргументов
* **Чтобы запустить скрипт, написанный для Bash**: примените [исправление для хука, написанного для Bash](#failed-hooks-on-windows-without-git-bash)

#### Поведение кода выхода 2 для каждого события

Код выхода 2 — это способ, которым хук сигнализирует «стоп, не делай этого». Эффект зависит от события, потому что одни события представляют действия, которые можно заблокировать (например, вызов инструмента, который ещё не произошёл), а другие — то, что уже произошло или не может быть предотвращено.

Если ваш хук завершается с кодом 2 и при этом задаёт `continue: false`, сначала смотрите [Код выхода 2](#exit-code-2), потому что результат может отличаться от указанного в строке вашего события.

| Событие хука | Может блокировать? | Что происходит при выходе с кодом 2 |
| :- | :- | :- |
| `PreToolUse` | Да | Блокирует вызов инструмента |
| `PermissionRequest` | Нет | Код выхода 2 не учитывается для этого события, и процесс разрешений продолжается без изменений. Вместо этого отклоняйте через [объект `decision`](#permissionrequest-decision-control) |
| `UserPromptSubmit` | Да | Блокирует промпт, поэтому он никогда не доходит до Claude. Смотрите [Что остаётся после заблокированного промпта](#what-a-blocked-prompt-leaves-behind) |
| `UserPromptExpansion` | Да | Блокирует раскрытие |
| `Stop` | Да | Не даёт Claude остановиться, диалог продолжается |
| `SubagentStop` | Да | Не даёт субагенту остановиться |
| `TeammateIdle` | Да | Не даёт участнику команды перейти в режим ожидания, поэтому он продолжает работу |
| `TaskCreated` | Да | Откатывает создание задачи |
| `TaskCompleted` | Да | Не даёт отметить задачу как выполненную |
| `ConfigChange` | Да | Блокирует вступление изменения конфигурации в силу (кроме `policy_settings`) |
| `StopFailure` | Нет | Вывод и код выхода игнорируются, кроме `terminalSequence` |
| `PostToolUse` | Нет | Показывает stderr Claude; инструмент уже выполнился |
| `PostToolUseFailure` | Нет | Показывает stderr Claude; инструмент уже завершился с ошибкой |
| `PostToolBatch` | Да | Останавливает агентный цикл перед следующим вызовом модели |
| `PermissionDenied` | Нет | Код выхода и stderr игнорируются, потому что отказ уже произошёл. Используйте JSON `hookSpecificOutput.retry: true`, чтобы сообщить модели, что она может повторить попытку; Claude Code игнорирует `retry: true` для [отказов без вердикта](#permissiondenied-decision-control) |
| `Notification` | Нет | Код выхода и stderr игнорируются |
| `SubagentStart` | Нет | Показывает stderr только пользователю |
| `SessionStart` | Нет | Показывает stderr только пользователю |
| `Setup` | Нет | Код выхода и stderr игнорируются |
| `SessionEnd` | Нет | Показывает stderr только пользователю |
| `CwdChanged` | Нет | Показывает stderr только пользователю |
| `DirectoryAdded` | Нет | Stderr попадает в отладочный лог; каталог уже добавлен |
| `FileChanged` | Нет | Показывает stderr только пользователю |
| `PreCompact` | Да | Блокирует сжатие контекста |
| `PostCompact` | Нет | Показывает stderr только пользователю |
| `PreModelSwitch` | Да | Блокирует переключение модели и показывает stderr пользователю |
| `PostModelSwitch` | Нет | Показывает stderr только пользователю; модель уже переключена |
| `Elicitation` | Да | Отклоняет запрос, и диалоговое окно не появляется |
| `ElicitationResult` | Да | Блокирует ответ (действие становится отказом) |
| `WorktreeCreate` | Да | Любой ненулевой код выхода приводит к ошибке создания worktree |
| `WorktreeRemove` | Да | Любой ненулевой код выхода приводит к ошибке удаления worktree, если каталог после этого всё ещё существует. Смотрите [WorktreeRemove](#worktreeremove), чтобы узнать, что происходит с каталогом |
| `InstructionsLoaded` | Нет | Код выхода игнорируется |
| `MessageDisplay` | Нет | Отображается исходный текст |

Для `SessionStart`, `SubagentStart` и `PostModelSwitch` Claude Code отображает stderr при коде выхода 2 в транскрипте как уведомление `<hook name> hook error` — так же, как отображает [неблокирующую ошибку](#exit-code-output). Claude его не видит, и сессия или субагент продолжают работу. Для `SubagentStart` уведомление появляется в собственном транскрипте субагента, а не в родительском диалоге.

### Обработка HTTP-ответов

HTTP-хуки используют коды состояния HTTP и тела ответов вместо кодов выхода и stdout. Чтобы блокировать действие, когда запрос завершается сбоем или возвращает статус не 2xx, установите [`onFailure: "block"`](#block-the-action-when-a-hook-fails). Чтобы заблокировать вызов инструмента или отклонить разрешение, верните ответ 2xx с телом JSON, содержащим соответствующие [поля решения](#decision-control).

После [неблокирующей ошибки](#exit-code-output) действие выполняется, если хук не относится к тем, [сбой которых блокирует действие](#block-the-action-when-a-hook-fails). За исключением событий с собственным контрактом обработки сбоев в [таблице по событиям](#exit-code-2-behavior-per-event), таких как `WorktreeCreate`, для каждого ответа или сбоя вы получаете следующие результаты:

* **2xx с пустым телом**: успех, эквивалентно коду выхода 0 без вывода
* **2xx с телом в виде объекта JSON**: разбирается по той же схеме [вывода JSON](#json-output), что и для командных хуков. Тело, не прошедшее проверку схемы, является неблокирующей ошибкой
* **2xx с любым другим телом, например обычным текстом**: неблокирующая ошибка, обрабатывается так же, как статус не 2xx. Claude Code не добавляет текст в контекст Claude
* **Статус не 2xx**: неблокирующая ошибка
* **Сбой соединения**: неблокирующая ошибка
* **Таймаут**: хук отменяется, как описано в разделе [Таймауты](#timeouts)

### Вывод JSON

Коды выхода позволяют только блокировать или ничего не сообщать, а вывод JSON даёт более тонкое управление. Вместо выхода с кодом 2 для блокировки завершитесь с кодом 0 и выведите объект JSON в stdout. Claude Code читает определённые поля из этого JSON для управления поведением, включая [управление решениями](#decision-control) для блокировки, разрешения или передачи решения пользователю.

> [!NOTE]
>
> Выберите один подход для каждого хука: либо используйте только коды выхода для сигнализации, либо завершайтесь с кодом 0 и выводите JSON для структурированного управления. О том, что происходит, если вы их смешиваете, смотрите [Вывод через код выхода](#exit-code-output).

Выводите в stdout только объект JSON. Для хука, который не является [асинхронным](#how-async-hooks-execute), любой другой текст там, например строка, которую профиль вашей оболочки выводит при запуске, мешает Claude Code прочитать объект как JSON; в разделе [JSON хука не действует](https://code.claude.com/docs/ru/hooks-guide.md#hook-json-has-no-effect) показано, как найти и убрать этот текст.

Строки `additionalContext`, `systemMessage` и `initialUserMessage` хука, а также его обычный stdout ограничены 10 000 символов:

* **Область действия**: Claude Code измеряет каждую строку отдельно, даже если для одного события выполняется несколько хуков. Для вывода JSON каждое поле измеряется отдельно; обычный stdout измеряется целиком.
* **Превышение лимита**: за исключением [stdout хука PreCompact](#precompact-output), Claude Code сохраняет вывод в файл в каталоге сессии. Он заменяет вывод путём к файлу и превью, содержащим до 2 000 первых символов. Большой корректный результат Bash обрабатывается так же, как описано в разделе [Ограничения вывода](https://code.claude.com/docs/ru/tools-reference.md#output-limits). В отличие от этого ограничения Bash, у данного лимита нет настройки или переменной окружения, позволяющей его увеличить.
* **Чтение файла**: Claude Code не просит Claude прочитать файл, поэтому держите всё, что Claude должен видеть всегда, в пределах лимита.

Объект JSON поддерживает три вида полей:

* **Универсальные поля**, такие как `continue`, перечислены в таблице ниже. Их принимает каждое событие, но некоторые события отбрасывают их или доставляют `systemMessage` не в транскрипт, а в другое место. Раздел каждого события об этом сообщает. `terminalSequence` тоже работает для этих событий, с исключениями, перечисленными в разделе [Вывод уведомлений терминала](#emit-terminal-notifications).
* **`decision` и `reason` верхнего уровня** используются некоторыми событиями для блокировки или предоставления обратной связи.
* **`hookSpecificOutput`** — вложенный объект для событий, которым требуется более развитое управление. Он требует поле `hookEventName`, установленное в имя события.

| Поле | По умолчанию | Описание |
| :- | :- | :- |
| `continue` | `true` | Если `false`, Claude полностью прекращает обработку после выполнения хука. Оно не блокирует вызов инструмента `PreToolUse`, поэтому для этого также верните `permissionDecision: "deny"` |
| `stopReason` | нет | Сообщение, показываемое пользователю, когда `continue` равно `false`. Оно остаётся в диалоге, поэтому Claude видит его, если диалог продолжается |
| `suppressOutput` | `false` | Не действует |
| `systemMessage` | нет | Предупреждающее сообщение, показываемое пользователю. В выводе [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) и [`--output-format stream-json`](https://code.claude.com/docs/ru/headless) оно может поступать как [`SDKInformationalMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkinformationalmessage) |
| `terminalSequence` | нет | Escape-последовательность терминала, которую Claude Code выводит от вашего имени, например уведомление на рабочем столе, заголовок окна или звуковой сигнал. Ограничено OSC `0`/`1`/`2`/`9`/`99`/`777` и BEL. Если значение содержит что-либо вне списка разрешённых последовательностей, поле игнорируется. Используйте его вместо записи в `/dev/tty`, который недоступен хукам |

Чтобы полностью остановить Claude:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

Для хуков `PreToolUse` и `PostToolUse` остановка применяется, даже если вызов инструмента завершается ошибкой или выполняется, пока Claude ещё передаёт ответ в потоковом режиме. Она не применяется, когда проверка разрешений отклоняет вызов `PreToolUse`.

#### Вывод уведомлений терминала

Хуки выполняются без управляющего терминала, поэтому запись escape-последовательностей напрямую в `/dev/tty` не работает. Вместо этого верните escape-последовательность в поле `terminalSequence`, и Claude Code выведет её за вас через собственный путь записи в терминал. Это исключает состояние гонки и работает в Windows, где `/dev/tty` отсутствует.

Поле принимает строку из одной или нескольких escape-последовательностей из списка разрешённых:

* OSC `0`, `1`, `2`: заголовки окна и значка
* OSC `9`: уведомления iTerm2, ConEmu, Windows Terminal и WezTerm, включая индикатор прогресса на панели задач `9;4`
* OSC `99`: уведомления Kitty
* OSC `777`: уведомления urxvt, Ghostty и Warp
* Одиночный BEL

Последовательности могут завершаться символом BEL или ST. Всё, что не входит в список разрешённых последовательностей, включая последовательности CSI для курсора и цвета, последовательности OSC для палитры, гиперссылки OSC 8, запись в буфер обмена OSC 52 и OSC 1337, отклоняется, а поле игнорируется.

Claude Code сам записывает последовательность при обработке вывода вашего хука, поэтому поле работает для событий, которые отбрасывают `systemMessage` и `continue`, таких как `Notification` и `StopFailure`. У него есть некоторые ограничения:

* Claude Code записывает последовательность только в интерактивной сессии и только пока его интерфейс находится на экране. В неинтерактивном режиме с флагом `-p` и в Agent SDK он игнорирует это поле.
* Поле работает только в хуке, который не выполняется в [фоновом режиме](#run-hooks-in-the-background), поэтому не включайте `async` и `asyncRewake`.
* Командный хук `WorktreeCreate` не может возвращать JSON, потому что Claude Code читает его stdout как путь к worktree. HTTP-хук `WorktreeCreate` возвращает JSON и может включать это поле.

Если вы используете tmux или GNU screen, сначала выполните [их настройку](#get-terminal-notifications-inside-tmux-or-gnu-screen). В примере ниже хук `Notification` вызывает уведомление на рабочем столе в терминале, который читает OSC `777`, например Ghostty или Warp. Вызов `jq -nc --arg` в скрипте формирует вывод JSON и экранирует все кавычки, обратные слеши и переводы строк в тексте уведомления:

```bash theme={null}
#!/bin/bash
# Notification hook: ping the desktop when Claude Code needs attention.
input=$(cat)
title="Claude Code"
body=$(jq -r '.message // "Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

Структура `{ "terminalSequence": "..." }` одинакова для любой оболочки или языка.

#### Получение уведомлений терминала внутри tmux или GNU screen

Когда Claude Code работает внутри tmux или GNU screen, для того чтобы последовательности OSC доходили до вашего терминального приложения, необходимо следующее:

* **tmux 3.3 или новее**: добавьте `set -g allow-passthrough on` в `~/.tmux.conf`, затем выполните `tmux source-file ~/.tmux.conf` из оболочки. Параметр применяется ко всем программам в этих панелях, а не только к Claude Code. Со значением `on` отправлять их могут только панели, которые tmux показывает на экране. Чтобы их могли отправлять и другие панели в сессии, к которой вы подключены, используйте `all` вместо `on` в tmux 3.4 или новее.
* **GNU screen**: держите окно Claude Code отображаемым в screen, потому что последовательности из фонового окна не доходят до вашего терминального приложения

#### Добавление контекста для Claude

Поле `additionalContext` передаёт строку из вашего хука в контекстное окно Claude. Claude Code оборачивает строку в [системное напоминание](https://code.claude.com/docs/ru/glossary.md#system-reminder) и вставляет его в диалог в точке срабатывания хука. Claude читает напоминание при следующем запросе к модели, но оно не отображается в интерфейсе как сообщение чата.

Возвращайте `additionalContext` внутри `hookSpecificOutput` вместе с именем события:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Место появления напоминания зависит от события:

* [SessionStart](#sessionstart) и [SubagentStart](#subagentstart): в начале диалога, перед первым промптом
* [UserPromptSubmit](#userpromptsubmit) и [UserPromptExpansion](#userpromptexpansion): вместе с отправленным промптом
* [PreToolUse](#pretooluse), [PostToolUse](#posttooluse), [PostToolUseFailure](#posttoolusefailure) и [PostToolBatch](#posttoolbatch): рядом с результатом инструмента
* [Stop](#stop) и [SubagentStop](#subagentstop): в конце хода. Диалог продолжается, чтобы Claude мог отреагировать на обратную связь. Смотрите [Управление решениями Stop](#stop-decision-control)
* [PostModelSwitch](#postmodelswitch): со следующим запросом после переключения. Смотрите [Управление решениями PostModelSwitch](#postmodelswitch-decision-control), чтобы узнать о времени доставки

Когда несколько хуков возвращают `additionalContext` для одного события, Claude получает все значения.

Если ваша строка содержит тег `<system-reminder>` или `</system-reminder>`, Claude получает строку, в которой `<` этого тега заменён на `&lt;`.

Если значение превышает 10 000 символов, Claude Code записывает текст в файл в каталоге сессии и вместо этого передаёт Claude путь к файлу с превью, содержащим до 2 000 первых символов. Claude может прочитать файл, но Claude Code не просит его об этом.

Используйте `additionalContext` для информации, которую Claude следует знать о текущем состоянии вашего окружения или об только что выполненной операции:

* **Состояние окружения**: текущая ветка, цель развёртывания или активные флаги функций
* **Условные правила проекта**: какая команда тестирования применима к только что отредактированному файлу, какие каталоги доступны только для чтения в этом worktree
* **Внешние данные**: открытые задачи, назначенные вам, недавние результаты CI, содержимое, полученное из внутреннего сервиса

Для инструкций, которые никогда не меняются, предпочтительнее [CLAUDE.md](https://code.claude.com/docs/ru/memory.md). Он загружается без запуска скрипта и является стандартным местом для статических соглашений проекта.

Пишите текст в виде фактических утверждений, а не императивных системных инструкций. Формулировки вроде «The deployment target is production» или «This repo uses `bun test`» воспринимаются как информация о проекте. Текст, оформленный как внеполосные системные команды, может активировать защиту Claude от промпт-инъекций, из-за чего Claude покажет этот текст вам вместо того, чтобы воспринять его как контекст.

Claude Code сохраняет внедрённый текст в транскрипте сессии. Для событий в середине сессии, таких как `PostToolUse` или `UserPromptSubmit`, при возобновлении с `--continue` или `--resume` Claude Code воспроизводит сохранённый текст, а не запускает хук повторно для прошлых ходов, поэтому такие значения, как временные метки или SHA коммитов, устаревают. Хуки `SessionStart` при возобновлении запускаются снова с `source`, установленным в `"resume"`, или в `"fork"`, если вы добавили `--fork-session`, поэтому они могут обновить свой контекст.

#### Управление решениями

Не каждое событие поддерживает блокировку или управление поведением через JSON. События, которые это поддерживают, используют разные наборы полей для выражения решения. Используйте эту таблицу как краткий справочник перед написанием хука:

| События | Шаблон решения | Ключевые поля |
| :- | :- | :- |
| UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | `decision` верхнего уровня | `decision: "block"`, `reason`. Stop и SubagentStop также принимают `hookSpecificOutput.additionalContext` для [обратной связи без ошибки, при которой диалог продолжается](#stop-decision-control) |
| TeammateIdle, TaskCompleted | Код выхода или `decision` верхнего уровня | Код выхода 2 или `decision: "block"` заставляет участника команды продолжать работу или оставляет задачу открытой. С `continue: false` участник команды переходит в режим ожидания. [Claude Code игнорирует `continue: false` при вызове `TaskUpdate`](#taskcompleted-decision-control) |
| TaskCreated | Код выхода или `decision` верхнего уровня | Код выхода 2 или `decision: "block"` [отменяет задачу](#taskcreated-decision-control) и возвращает сообщение Claude. `continue: false` игнорируется |
| PreToolUse | `hookSpecificOutput` | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason` |
| PreModelSwitch | `hookSpecificOutput` или `decision` верхнего уровня | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`. `decision: "block"` также [отменяет переключение](#premodelswitch-decision-control) |
| PermissionRequest | `hookSpecificOutput` | `decision.behavior` (allow/deny) |
| PermissionDenied | `hookSpecificOutput` | `retry: true` сообщает модели, что она может повторить попытку отклонённого вызова инструмента; Claude Code игнорирует его для [отказов без вердикта](#permissiondenied-decision-control) |
| WorktreeCreate | возврат пути | Командный хук выводит путь в stdout; HTTP-хук возвращает `hookSpecificOutput.worktreePath`. Сбой хука или отсутствие пути прерывает создание |
| WorktreeRemove | Код выхода | Любой ненулевой код выхода приводит к ошибке удаления, если каталог после этого всё ещё существует. Вывод JSON отбрасывается |
| Elicitation, ElicitationResult | `hookSpecificOutput` или `decision` верхнего уровня | `action` (accept/decline/cancel), `content` (значения полей формы). `decision: "block"` также [отклоняет запрос](#other-ways-to-decline-an-elicitation) |
| MessageDisplay | `hookSpecificOutput` | `displayContent` заменяет отображаемый на экране текст. Только для отображения: транскрипт и то, что видит Claude, сохраняют оригинал |
| SessionStart, SubagentStart, PostModelSwitch | Только контекст | `hookSpecificOutput.additionalContext` добавляет контекст для Claude. SessionStart также принимает [`initialUserMessage`, `watchPaths`, `sessionTitle` и `reloadSkills`](#sessionstart-decision-control). Без блокировки и управления решениями |
| Setup, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, DirectoryAdded, FileChanged | Нет | Без управления решениями. Используются для побочных эффектов, таких как логирование или очистка |

Некоторые события также могут переписывать содержимое, а не только разрешать или блокировать его:

* `PreToolUse`: `updatedInput` непосредственно в `hookSpecificOutput` заменяет аргументы инструмента перед его запуском. Смотрите [Управление решениями PreToolUse](#pretooluse-decision-control)
* `PermissionRequest`: `updatedInput` внутри объекта `decision`. Смотрите [Управление решениями PermissionRequest](#permissionrequest-decision-control)
* `PostToolUse`: `updatedToolOutput` заменяет результат инструмента. В облачной сессии [Cowork](https://claude.com/docs/cowork/overview) Claude Code игнорирует `updatedToolOutput`, если инструментом является `AskUserQuestion` или `ExitPlanMode`, и Claude читает исходный ответ или план. Смотрите [Управление решениями PostToolUse](#posttooluse-decision-control)
* `UserPromptSubmit`: не может заменить промпт; он только внедряет `additionalContext` рядом с ним

Для сценариев редактирования или преобразования данных перехватывайте исходящие входные данные инструментов в `PreToolUse`, а результаты успешных вызовов — в `PostToolUse`. `PostToolUseFailure` не может переписать результат, поэтому вывод завершившейся с ошибкой команды доходит до Claude без изменений.

Вот примеры каждого шаблона в действии:

> [tab] decision верхнего уровня
>
> Единственное значение для `decision` — `"block"`. Чтобы разрешить продолжение действия, не указывайте `decision` в вашем JSON или завершитесь с кодом 0 вообще без JSON:
>
> ```json theme={null}
> {
>   "decision": "block",
>   "reason": "Test suite must pass before proceeding"
> }
> ```

> [tab] PreToolUse
>
> Использует `hookSpecificOutput` для более развитого управления: разрешить, отклонить или передать решение пользователю. Вы также можете изменить входные данные инструмента перед его запуском или внедрить дополнительный контекст для Claude. Смотрите [Управление решениями PreToolUse](#pretooluse-decision-control), чтобы узнать обо всех доступных параметрах.
>
> ```json theme={null}
> {
>   "hookSpecificOutput": {
>     "hookEventName": "PreToolUse",
>     "permissionDecision": "deny",
>     "permissionDecisionReason": "Database writes are not allowed"
>   }
> }
> ```

> [tab] PermissionRequest
>
> Использует `hookSpecificOutput`, чтобы разрешить или отклонить запрос разрешения от имени пользователя. При разрешении вы также можете изменить входные данные инструмента или применить правила разрешений, чтобы пользователю не пришлось подтверждать снова. Смотрите [Управление решениями PermissionRequest](#permissionrequest-decision-control), чтобы узнать обо всех доступных параметрах.
>
> ```json theme={null}
> {
>   "hookSpecificOutput": {
>     "hookEventName": "PermissionRequest",
>     "decision": {
>       "behavior": "allow",
>       "updatedInput": {
>         "command": "npm run lint"
>       }
>     }
>   }
> }
> ```

Расширенные примеры, включая проверку команд Bash, фильтрацию промптов и скрипты автоматического одобрения, смотрите в разделе [Что можно автоматизировать](https://code.claude.com/docs/ru/hooks-guide.md#what-you-can-automate) руководства и в [эталонной реализации валидатора команд Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## События хуков

Каждое событие соответствует точке в жизненном цикле Claude Code, в которой могут выполняться хуки. Разделы ниже упорядочены в соответствии с жизненным циклом: от настройки сессии через агентный цикл до завершения сессии. В каждом разделе описано, когда срабатывает событие, какие значения matcher оно поддерживает, какие входные данные JSON получает и как управлять поведением через вывод.

### SessionStart

Выполняется, когда Claude Code начинает новую сессию или возобновляет существующую. Полезно для загрузки контекста разработки, например существующих issues или недавних изменений в вашей кодовой базе, или для настройки переменных окружения. Для статического контекста, который не требует скрипта, используйте вместо этого [CLAUDE.md](https://code.claude.com/docs/ru/memory.md).

SessionStart выполняется в каждой сессии, поэтому такие хуки должны работать быстро. Поддерживаются только хуки `type: "command"` и `type: "mcp_tool"`. О том, когда выполняются хуки `mcp_tool`, см. [Поля хука MCP-инструмента](#mcp-tool-hook-fields).

Значение matcher соответствует тому, как была запущена сессия:

| Matcher | Когда срабатывает |
| :- | :- |
| `startup` | Новая сессия |
| `resume` | `--resume`, `--continue` или `/resume` |
| `clear` | `/clear` |
| `compact` | Автоматическое или ручное сжатие контекста |
| `fork` | Новая сессия, ответвлённая от существующей: `--fork-session` вместе с `--resume` или `--continue`, фоновая копия `/fork`, `/branch` или диалог, который вы [переводите в фон](https://code.claude.com/docs/ru/agent-view.md#from-inside-a-session) |

Когда вы начинаете интерактивную сессию, возобновляете диалог при запуске с `--continue` или `--resume` или выполняете `/clear`, хуки SessionStart выполняются в фоне. Вы можете сразу начать вводить текст, а возобновлённый диалог появляется, не дожидаясь хуков. Первый ответ Claude всё равно ждёт завершения хуков, чтобы их контекст дошёл до Claude.

Когда вы переключаете диалоги с помощью `/resume` внутри сессии, переключение, напротив, ждёт завершения хуков. Если вы выполните `/clear` или переключитесь на другой диалог, пока фоновые хуки ещё выполняются, ничто из того, что они вернут, не применится к сессии.

То же ожидание действует и при запуске, включая возобновлённую сессию: промпт, который вы отправляете, пока хуки SessionStart ещё выполняются, не дойдёт до Claude, пока они не завершатся.

Во время любого из этих ожиданий нажмите `Esc`, чтобы вернуть промпт в поле ввода, не отправляя его. Хуки продолжат выполняться.

#### Входные данные SessionStart

Помимо [общих входных полей](#common-input-fields), хуки SessionStart получают `source` и, необязательно, `model`, `agent_type` и `session_title`:

| Поле | Описание |
| :- | :- |
| `source` | Как началась сессия: `"startup"` для новых сессий, `"resume"` для возобновлённых сессий, `"clear"` после `/clear`, `"compact"` после сжатия контекста или `"fork"` для новой сессии, ответвлённой от существующей |
| `model` | Идентификатор активной модели. Может отсутствовать, например после `/clear` или когда сессия восстанавливается через восстановление диалога, поэтому проверяйте наличие поля перед чтением |
| `agent_type` | Имя агента; присутствует, когда вы запускаете Claude Code с `claude --agent <name>` |
| `session_title` | Пользовательское название сессии; присутствует, когда оно задано, например с помощью `--name`, `/rename`, вывода `sessionTitle` хука или `renameSession()` в Agent SDK. Хук, который выводит `sessionTitle`, может сначала проверить это поле, чтобы не перезаписать существующее пользовательское название |

Сессия, которой вы не дали имя, всё равно может иметь [сгенерированное название](https://code.claude.com/docs/ru/sessions.md#name-your-sessions). Такое название не является пользовательским и не появляется в `session_title`.

Когда `source` равен `"resume"` или `"fork"` и транскрипт содержит хотя бы один ответ Claude, хуки SessionStart также получают четыре поля ниже. Ваш хук может использовать их, чтобы до первого запроса сообщить, во что обойдётся возобновление устаревшего диалога, например в [`systemMessage`](#json-output). Для этих полей требуется Claude Code v2.1.251 или новее.

| Поле | Описание |
| :- | :- |
| `seconds_since_last_response` | Реальное время в секундах с момента последнего ответа в возобновлённом транскрипте |
| `context_tokens` | Токены, которые первый запрос возобновлённой сессии повторно отправляет в качестве промпта |
| `prompt_cache_likely_expired` | `true`, когда последний ответ старше [времени жизни кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime) сессии или когда последующее сжатие контекста заменило кэшированный диалог |
| `estimated_cache_write_usd` | Оценочная стоимость в долларах США записи `context_tokens` в кэш промптов на модели сессии, без учёта ответа |

В этом примере показаны входные данные для сессии, возобновлённой через 90 минут после её последнего ответа:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "resume",
  "model": "claude-opus-5",
  "seconds_since_last_response": 5400,
  "context_tokens": 182340,
  "prompt_cache_likely_expired": true,
  "estimated_cache_write_usd": 1.1396
}
```

#### Управление решениями SessionStart

Хук SessionStart может добавить контекст для Claude, задать первое сообщение пользователя, задать название сессии, отслеживать файлы и перезагружать скиллы. Для каждого из этих действий верните соответствующее поле в дополнение к [полям вывода JSON](#json-output), доступным всем хукам:

| Поле | Описание |
| :- | :- |
| `additionalContext` | Строка, добавляемая в контекст Claude в начале диалога, перед первым промптом. О том, как доставляется текст и что в него включать, см. [Добавление контекста для Claude](#add-context-for-claude) |
| `initialUserMessage` | Строка, используемая как первое сообщение пользователя в сессии в [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) с флагом `-p`. Она становится первым ходом, даже если вы не передаёте промпт. Переданный вами промпт следует следующим ходом |
| `sessionTitle` | Задаёт название сессии с тем же эффектом, что и `/rename`. Применяется, когда `source` равен `"startup"`, `"resume"` или `"fork"` |
| `watchPaths` | Массив абсолютных путей для отслеживания событий [FileChanged](#filechanged) в этой сессии |
| `reloadSkills` | Логическое значение. Если `true`, Claude Code повторно сканирует каталоги [скиллов](https://code.claude.com/docs/ru/skills.md) и команд после завершения хуков SessionStart. См. [Перезагрузка скиллов, которые устанавливает хук](#reload-skills-that-a-hook-installs) |

Этот вывод добавляет контекст и даёт сессии имя:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2",
    "sessionTitle": "auth-refactor"
  }
}
```

Хук, который только добавляет контекст, может просто напечатать его, не формируя JSON, поскольку Claude Code добавляет [обычный текстовый stdout](#exit-code-0) хука SessionStart в контекст Claude.

Если хук SessionStart вашего плагина задаёт `initialUserMessage` или `sessionTitle`, установите плагин до начала сессии. Claude Code игнорирует оба поля от плагина, установка которого завершается после того, как хуки SessionStart уже выполнились.

#### Перезагрузка скиллов, которые устанавливает хук

Чтобы скиллы, которые устанавливает хук SessionStart, стали доступны в той же сессии, верните `reloadSkills`. Обнаружение скиллов обычно выполняется до завершения хуков SessionStart, поэтому без этого поля файлы, которые хук записывает в `~/.claude/skills/` или `.claude/skills/`, могут отсутствовать при выполнении первого промпта.

Этот пример синхронизирует общий репозиторий скиллов и запрашивает повторное сканирование:

```bash theme={null}
#!/bin/bash

git -C ~/.claude/skills/team-skills pull --quiet 2>/dev/null || \
  git clone --quiet https://git.example.com/your-org/team-skills.git ~/.claude/skills/team-skills

echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "reloadSkills": true}}'
```

URL репозитория — это заглушка. Замените его на свой репозиторий скиллов.

#### Сохранение переменных окружения

Хуки SessionStart имеют доступ к переменной окружения `CLAUDE_ENV_FILE`, которая указывает путь к файлу, где можно сохранить переменные окружения для shell-команд, которые Claude выполняет позже в сессии.

Чтобы задать отдельные переменные окружения, запишите операторы `export` в `CLAUDE_ENV_FILE`. Используйте дозапись (`>>`), чтобы сохранить переменные, заданные другими хуками:

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Чтобы зафиксировать все изменения окружения от команд настройки, сравните экспортированные переменные до и после:

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Каждая команда Bash выполняет содержимое файла как shell-код перед самой командой, поэтому строка в нём может использовать всё, что вычисляет Bash, например ссылку на `$PATH` в `export PATH="$PATH:./node_modules/.bin"`.

##### Сохранённые переменные в командах PowerShell

Команды [PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool) тоже получают переменные из `CLAUDE_ENV_FILE` в Claude Code v2.1.296 или новее, но PowerShell никогда не выполняет этот файл. Вместо этого Claude Code считывает из него присваивания и копирует их в окружение команды PowerShell. Это происходит, только если каждая строка относится к одному из следующих видов — во всём, что записали все хуки в этой сессии, и в любом скрипте, на который вы [установили `CLAUDE_ENV_FILE`](https://code.claude.com/docs/ru/env-vars) до запуска:

* Пустая строка или комментарий `#`
* Одно присваивание в начале строки, записанное как `export NAME=value`, `declare -x NAME=value` или `NAME=value`, со значением, которое Bash использовал бы в точности как написано, составленным из любого сочетания следующих частей: текст без кавычек, использующий только буквы, цифры и символы `_ @ % + = : , . / -`, текст в одинарных кавычках и текст в двойных кавычках, где любые `$`, обратная кавычка или `"` внутри экранированы обратной косой чертой

Если какая-либо строка имеет другой вид, например `export PATH="$PATH:./node_modules/.bin"` с неэкранированным `$PATH`, команда `source` или строки `$'...'`, которые печатает `direnv export bash`, команды PowerShell не получают ни одной переменной, а `claude --debug` записывает в лог `Session environment is not all plain assignments`. Команды Bash по-прежнему получают их все. В Windows команды PowerShell также не получают переменную, значение которой содержит `/` или `\`, поскольку Git Bash и Windows записывают пути по-разному. Команда PowerShell, выполняемая [в песочнице](https://code.claude.com/docs/ru/sandboxing.md), не получает ни одной переменной.

> [!NOTE]
>
> `CLAUDE_ENV_FILE` доступна для хуков SessionStart, [Setup](#setup), [CwdChanged](#cwdchanged) и [FileChanged](#filechanged). Другие события хуков не имеют доступа к этой переменной, как и хук, выполняемый в PowerShell, будь то через [`"shell": "powershell"`](#command-hook-fields) или по умолчанию в Windows без Git Bash.

### Setup

Срабатывает, только когда вы запускаете Claude Code с `--init-only` либо с `--init` или `--maintenance` в [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) с флагом `-p`. При обычном запуске не срабатывает. Используйте его для однократной установки зависимостей или плановой очистки, которую вы явно запускаете из CI или скриптов, отдельно от обычного начала сессии. Для инициализации на уровне каждой сессии используйте вместо этого [SessionStart](#sessionstart).

Значение matcher соответствует флагу CLI, который запустил хук:

| Matcher | Когда срабатывает |
| :- | :- |
| `init` | `claude --init-only` или `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

Когда вы выполняете `claude --init-only`, Claude Code запускает хуки Setup и хуки `SessionStart` с matcher `startup`, а затем завершает работу, не начиная диалог.

Когда вы начинаете или продолжаете диалог с `-p`, необходимо также передать промпт — как аргумент или через stdin. Промпт можно не передавать, если хук `SessionStart` задаёт [`initialUserMessage`](#sessionstart-decision-control) или если вы возобновляете сессию с [отложенным вызовом инструмента](#defer-a-tool-call-for-later).

При успешном выполнении `--init-only` ничего не выводит в терминал. Чтобы убедиться, что хуки выполнились, запустите `claude --debug-file <path> --init-only`, заменив `<path>` расположением файла лога, и проверьте в логе записи хуков Setup и SessionStart.

Поскольку Setup срабатывает не при каждом запуске, плагин, которому нужна установленная зависимость, не может полагаться только на Setup. Практичный подход — проверять наличие зависимости при первом использовании и устанавливать её при отсутствии, например хук или скилл, который проверяет наличие `${CLAUDE_PLUGIN_DATA}/node_modules` и выполняет `npm install`, если её нет. О том, где хранить установленные зависимости, см. [каталог постоянных данных](https://code.claude.com/docs/ru/plugins/components.md#path-variables-and-persistent-data). Если вы распространяете плагин через маркетплейс, этот подход может не понадобиться: Claude Code [автоматически устанавливает подходящие зависимости пакетов Node.js](https://code.claude.com/docs/ru/plugins/loading.md#node-js-package-dependencies) при кэшировании плагина.

#### Входные данные Setup

Помимо [общих входных полей](#common-input-fields), хуки Setup получают поле `trigger` со значением `"init"` или `"maintenance"`:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### Управление решениями Setup

Хуки Setup не могут блокировать; выполнение продолжается при любом коде выхода. При любом коде выхода Claude Code отбрасывает [поля вывода JSON](#json-output) хука Setup, такие как `systemMessage`, `continue` и `hookSpecificOutput.additionalContext`. С `-p` stdout, stderr и код выхода хука Setup появляются в выводе запуска только как [события `hook_response`](https://code.claude.com/docs/ru/headless#read-session-metadata), если вы запускаете с `--output-format stream-json --verbose`.

Хуки Setup имеют доступ к `CLAUDE_ENV_FILE`. Если ваш хук записывает переменные в этот файл, они сохраняются для последующих команд Bash в сессии, как и в [хуках SessionStart](#persist-environment-variables). На `Setup` запускаются только хуки `type: "command"`. Хук `type: "mcp_tool"` на `Setup` всегда пропускается, как описано в разделе [Поля хуков MCP-инструментов](#mcp-tool-hook-fields).

### InstructionsLoaded

Срабатывает, когда файл `CLAUDE.md` или `.claude/rules/*.md` загружается в контекст. Это событие срабатывает в начале сессии для файлов, загружаемых сразу, и позже при отложенной загрузке файлов, например когда Claude обращается к подкаталогу, содержащему вложенный `CLAUDE.md`, или когда срабатывают условные правила с frontmatter `paths:`. Хук не поддерживает блокировку или управление решениями. Он выполняется асинхронно для целей наблюдаемости.

Это событие не срабатывает, когда Claude [читает `AGENTS.md` напрямую](https://code.claude.com/docs/ru/memory#agents-md) через настройку **Project instructions**. Оно срабатывает, когда `CLAUDE.md` импортирует ваш `AGENTS.md` — с `load_reason`, равным `include`, как для любого другого импортированного файла, — и когда `CLAUDE.md` является символической ссылкой на него — как обычная загрузка `CLAUDE.md`.

Matcher сопоставляется с `load_reason`. Например, используйте `"matcher": "session_start"`, чтобы срабатывать только для файлов, загружаемых в начале сессии, или `"matcher": "path_glob_match|nested_traversal"`, чтобы срабатывать только при отложенных загрузках.

#### Входные данные InstructionsLoaded

Помимо [общих входных полей](#common-input-fields), хуки InstructionsLoaded получают следующие поля:

| Поле | Описание |
| :- | :- |
| `file_path` | Абсолютный путь к загруженному файлу инструкций |
| `memory_type` | Область действия файла: `"User"`, `"Project"`, `"Local"` или `"Managed"` |
| `load_reason` | Почему файл был загружен: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` или `"compact"`. Значение `"compact"` возникает, когда файлы инструкций повторно загружаются после сжатия контекста |
| `globs` | Glob-шаблоны путей из frontmatter `paths:` файла, если есть. Присутствует только для загрузок `path_glob_match` |
| `trigger_file_path` | Путь к файлу, обращение к которому вызвало эту загрузку, для отложенных загрузок |
| `parent_file_path` | Путь к родительскому файлу инструкций, который включил этот файл, для загрузок `include` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### Управление решениями InstructionsLoaded

Хуки InstructionsLoaded не имеют управления решениями. Они не могут блокировать или изменять загрузку инструкций. Claude Code отбрасывает их [поля вывода JSON](#json-output), такие как `systemMessage` и `continue`. Используйте это событие для журнала аудита, отслеживания соответствия требованиям или наблюдаемости.

### UserPromptSubmit

Выполняется при отправке промпта, до того как Claude его обработает. Это позволяет
добавлять дополнительный контекст на основе промпта/диалога, проверять промпты или
блокировать определённые типы промптов.

Хуки `UserPromptSubmit` срабатывают не только на промпты, которые вы вводите. Claude Code также запускает их, когда:

* срабатывает [запланированная задача на уровне сессии](https://code.claude.com/docs/ru/scheduled-tasks.md), включая итерацию `/loop`
* [Фоновый субагент](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background) отчитывается перед сессией, которая его запустила
* [Другая сессия отправляет сообщение](https://code.claude.com/docs/ru/cross-session-messaging.md) в ваш основной диалог
* Появляется вывод кода, который Claude запускает в сессии [Code Mode](https://code.claude.com/docs/ru/code-mode.md#code-output-withheld-by-a-hook), — для хуков `command`, `http` и `mcp_tool`, когда код может выполняться в фоне

Хуки `UserPromptSubmit` имеют таймаут по умолчанию 30 секунд для типов `command`, `http` и `mcp_tool` — меньше, чем 600 секунд по умолчанию для этих типов в большинстве других событий. Поскольку этот хук выполняется перед каждым промптом и блокирует обработку моделью до своего завершения, зависший хук останавливает сессию. Если вашему хуку нужно больше времени, задайте поле `timeout` в записи хука.

За исключением командного хука, запускаемого с [`async: true`](#run-hooks-in-the-background), хук `UserPromptSubmit` типа command, HTTP или MCP-инструмент, достигший таймаута, отменяется, а его вывод, включая любой `additionalContext`, отбрасывается. Промпт всё равно доходит до Claude, но без этого контекста. Чтобы вместо этого заблокировать промпт, задайте [`onFailure: "block"`](#block-the-action-when-a-hook-fails) для командного или HTTP-хука. В транскрипте отображается уведомление с именем хука, сработавшим таймаутом и сообщением о том, что вывод был отброшен.

[Callback-хук Agent SDK](https://code.claude.com/docs/ru/agent-sdk/hooks.md) на `UserPromptSubmit`, достигший таймаута, блокирует промпт с сообщением, в котором указаны хук и таймаут, потому что callback в этом месте может выполнять роль политики, которая не должна пропускать промпт при сбое. Сессия продолжается.

#### `Esc` во время проверки промпта

Если вы нажмёте `Esc` или прервёте сессию, пока хуки ещё проверяют промпт, проверка останавливается, и промпт не доходит до Claude. Текст, который вы ввели в терминале, возвращается в поле ввода промпта, и хуки проверяют его снова, когда вы отправляете его повторно.

Хук может заблокировать промпт в тот же момент, когда вы прерываете сессию. В этом случае промпт остаётся заблокированным: вы видите [сообщение о блокировке](#what-a-blocked-prompt-leaves-behind) этого хука, а текст не возвращается в поле ввода.

#### Входные данные UserPromptSubmit

Помимо [общих входных полей](#common-input-fields), хуки UserPromptSubmit получают поле `prompt`, содержащее отправленный текст. Вставленное содержимое, свёрнутое в заглушку `[Pasted text #N]`, поступает развёрнутым на своём месте. В сессиях, где Claude Code [помечает вставленный текст для Claude](https://code.claude.com/docs/ru/terminal-config.md#how-claude-treats-pasted-text), это развёрнутое содержимое находится между строкой `<pasted_content id="…">` и строкой `</pasted_content id="…">`, поэтому учитывайте эти строки, если ваш хук разбирает промпт.

Хуки UserPromptSubmit также получают `session_title`, когда у сессии есть пользовательское название, с тем же значением, что и [поле `session_title` в SessionStart](#sessionstart-input).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

Когда промпт — это введённый вами [скилл](https://code.claude.com/docs/ru/skills.md) или пользовательская команда, например `/deploy staging`, хук получает эту строку в том виде, в каком вы её ввели, а не развёрнутое содержимое скилла. Если хук блокирует промпт, команда не выполняется, поэтому shell-команды, которые скилл [вставляет с помощью `` !`<command>` ``](https://code.claude.com/docs/ru/skills#inject-dynamic-context), тоже не выполняются. Чтобы вместо этого сопоставлять имя или аргументы команды, используйте [UserPromptExpansion](#userpromptexpansion).

#### Управление решениями UserPromptSubmit

Хуки `UserPromptSubmit` могут управлять тем, обрабатывается ли отправленный промпт, и добавлять контекст. Доступны все [поля вывода JSON](#json-output).

Есть два способа добавить контекст в диалог при коде выхода 0:

* **Обычный текстовый stdout**: Claude Code добавляет stdout, который он [считает обычным текстом](#exit-code-0), в контекст Claude
* **JSON с `additionalContext`**: используйте формат JSON ниже для большего контроля. Поле `additionalContext` добавляется как контекст

Ни один из каналов не создаёт видимой записи в транскрипте. Обычный stdout и значение `additionalContext` внедряются каждое как системное напоминание, начинающееся с имени хука; Claude читает оба. Чтобы подтвердить доставку, проверьте [лог отладки](#debug-hooks).

Чтобы заблокировать промпт, верните объект JSON с `decision`, равным `"block"`:

| Поле | Описание |
| :- | :- |
| `decision` | `"block"` останавливает промпт до того, как он дойдёт до Claude. Не указывайте, чтобы разрешить продолжение |
| `reason` | Показывается пользователю, когда `decision` равно `"block"`. Не добавляется в контекст, за исключением случаев, когда хук блокирует [вывод Code Mode](https://code.claude.com/docs/ru/code-mode.md#code-output-withheld-by-a-hook) |
| `additionalContext` | Строка, добавляемая в контекст Claude вместе с отправленным промптом. См. [Добавление контекста для Claude](#add-context-for-claude) |
| `sessionTitle` | Задаёт название сессии. Используйте для автоматического именования сессий на основе содержимого промпта |
| `suppressOriginalPrompt` | Если `true`, когда хук блокирует промпт, текст промпта не включается в сообщение о блокировке. См. [Что остаётся после заблокированного промпта](#what-a-blocked-prompt-leaves-behind) |

Если ваш хук блокирует, завершаясь с кодом 2, текст его stderr обрабатывается так же, как `reason`.

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title",
    "suppressOriginalPrompt": true
  }
}
```

#### Что остаётся после заблокированного промпта

Заблокированный промпт никогда не доходит до Claude, но его текст удаляется не везде. По умолчанию сообщение о блокировке, показываемое пользователю, заканчивается строкой `Original prompt:`, за которой следует отправленный текст, и Claude Code записывает это сообщение в файл транскрипта сессии на диске. Чтобы исключить текст из сообщения, выведите JSON с `"suppressOriginalPrompt": true` внутри `hookSpecificOutput`. Это работает независимо от того, блокирует ли хук через `decision: "block"` или через выход с кодом 2.

`suppressOriginalPrompt` изменяет только сообщение о блокировке. Отправленный текст всё равно может оказаться в локальных файлах, таких как транскрипт сессии и история ваших промптов, поэтому блокирующий хук не является способом не допустить попадания секрета на диск. Чтобы ограничить или удалить эти файлы, см. [Хранение в открытом виде](https://code.claude.com/docs/ru/claude-directory.md#plaintext-storage) и [Очистка локальных данных](https://code.claude.com/docs/ru/claude-directory.md#clear-local-data).

### UserPromptExpansion

Выполняется, когда введённая пользователем команда разворачивается в промпт до того, как дойти до Claude. Используйте это, чтобы блокировать прямой вызов определённых команд, внедрять контекст для конкретного скилла или логировать, какие команды вызывают пользователи. Например, хук с matcher `deploy` может блокировать `/deploy`, если нет файла подтверждения, а хук, соответствующий скиллу ревью, может добавлять чек-лист ревью команды в качестве `additionalContext`.

Это событие покрывает путь, который не покрывает `PreToolUse`: хук `PreToolUse`, соответствующий инструменту `Skill`, срабатывает только когда Claude вызывает этот инструмент, а прямой ввод `/skillname` обходит `PreToolUse`. `UserPromptExpansion` срабатывает на этом прямом пути.

Сопоставляется с `command_name`. Оставьте matcher пустым, чтобы срабатывать на каждую команду типа prompt.

#### Входные данные UserPromptExpansion

Помимо [общих входных полей](#common-input-fields), хуки UserPromptExpansion получают `expansion_type`, `command_name`, `command_args`, `command_source` и строку `prompt`. Поле `expansion_type` имеет значение `slash_command` для скиллов и пользовательских команд или `mcp_prompt` для промптов MCP-сервера.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "my-plugin:example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/my-plugin:example-skill arg1 arg2"
}
```

#### Управление решениями UserPromptExpansion

Хуки `UserPromptExpansion` могут блокировать развёртывание или добавлять контекст. Доступны все [поля вывода JSON](#json-output).

| Поле | Описание |
| :- | :- |
| `decision` | `"block"` предотвращает развёртывание команды. Не указывайте, чтобы разрешить продолжение |
| `reason` | Показывается пользователю, когда `decision` равен `"block"` |
| `additionalContext` | Строка, добавляемая в контекст Claude вместе с развёрнутым промптом. См. [Добавление контекста для Claude](#add-context-for-claude) |

Хук, который блокирует через выход с кодом 2, обрабатывается так же, как `reason`: сообщение о блокировке показывает пользователю текст stderr.

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### MessageDisplay

Выполняется, пока сообщение ассистента выводится на экран в потоковом режиме. Claude Code отображает сообщение порциями: каждый раз, когда готова к отрисовке партия только что завершённых строк, хук выполняется один раз с этими строками, и Claude Code отрисовывает на их месте текст замены от хука. Длинное сообщение приводит к нескольким вызовам; короткое может привести только к одному.

Используйте MessageDisplay, чтобы:

* убирать markdown для минималистичного отображения
* преобразовывать текст, который приложение на Agent SDK показывает своим пользователям
* скрывать API-ключи или внутренние имена хостов из ответов Claude

Claude Code удерживает каждую партию, пока ваш хук не вернёт результат, поэтому хук должен работать быстро. Если хук завершается с ошибкой или по таймауту, Claude Code отображает исходный текст. Таймаут по умолчанию для этого события — 10 секунд; если вашему хуку нужно больше времени, задайте поле `timeout` в записи хука.

MessageDisplay влияет только на отображение: текст замены меняет только то, что отрисовывается на экране. В транскрипте и в том, что видит Claude, сохраняется исходный текст, поэтому Claude никогда не видит замену, а подробный режим показывает оригинал. Хук получает только текст сообщений ассистента, поэтому результаты инструментов и вводимый вами текст отображаются без изменений.

MessageDisplay не поддерживает matcher и срабатывает для каждого сообщения ассистента, которое передаёт текст в потоке; сообщения без текста, например ответы, состоящие только из вызовов инструментов, его не вызывают.

В неинтерактивных запусках, включая запросы Agent SDK и `claude -p`, MessageDisplay выполняется один раз на сообщение ассистента, а не один раз на партию строк. Единственный вызов поступает после завершения сообщения и содержит полный текст сообщения: `index` равен `0`, `final` равен `true`, а `delta` содержит всё сообщение. Хук, собирающий текст `delta` для каждого сообщения, получает в обоих режимах одинаковый итоговый текст.

#### Входные данные MessageDisplay

Помимо [общих входных полей](#common-input-fields), хуки MessageDisplay получают идентификаторы хода и сообщения, позицию этого вызова в сообщении и новый текст в `delta`. Границы партий зависят от того, как передаётся текст в потоке, поэтому используйте `index` и `final` для отслеживания продвижения по сообщению, а не рассчитывайте на определённую группировку строк.

| Поле | Описание |
| :- | :- |
| `turn_id` | UUID текущего хода |
| `message_id` | UUID отображаемого сообщения ассистента. Неизменен во всех партиях одного сообщения. Это не id `msg_…` из API, поэтому его нельзя сопоставить с id сообщений в транскрипте |
| `index` | Индекс этой партии в сообщении, начиная с нуля |
| `final` | `true` в последней партии сообщения. У каждого сообщения ровно одна финальная партия |
| `delta` | Строки, завершённые с момента предыдущей партии, включая завершающие символы новой строки. Всегда целые строки, кроме финальной партии, которая может заканчиваться посреди строки. В интерактивных запусках delta финальной партии пуста, если сообщение заканчивается символом новой строки, поэтому считайте сигналом конца сообщения `final`, а не непустую delta. В запусках Agent SDK и `claude -p` единственный вызов содержит всё сообщение |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "MessageDisplay",
  "turn_id": "0c9e6a2f-7d41-4f4e-9a15-3f4f7c2b8d10",
  "message_id": "5b2a9c8e-1f63-4d8a-b7c4-9e0d2a6f1c3b",
  "index": 0,
  "final": false,
  "delta": "Here is the plan:\n"
}
```

#### Вывод MessageDisplay

Помимо [полей вывода JSON](#json-output), доступных всем хукам, хуки MessageDisplay могут вернуть `displayContent`, чтобы заменить delta на экране:

| Поле | Описание |
| :- | :- |
| `displayContent` | Текст, отображаемый вместо delta. Не указывайте, чтобы отобразить оригинал |

Хуки MessageDisplay не имеют управления решениями. Они не могут блокировать сообщение или изменять то, что сохраняется в транскрипте или отправляется Claude. Claude Code учитывает `displayContent` из их вывода JSON и отбрасывает `systemMessage` и `continue`.

Этот пример убирает форматирование markdown из ответов Claude для отображения обычным текстом. Скрипт считывает каждую партию из stdin, удаляет из `delta` маркеры полужирного шрифта и обратные кавычки встроенного кода и возвращает результат как `displayContent`.

> [tab] macOS/Linux
>
> Зарегистрируйте командный хук для события в файле настроек:
>
> ```json theme={null}
> {
>   "hooks": {
>     "MessageDisplay": [
>       {
>         "hooks": [
>           {
>             "type": "command",
>             "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.sh",
>             "args": []
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Сохраните этот скрипт в `.claude/hooks/plain-display.sh` в своём проекте и сделайте его исполняемым с помощью `chmod +x`:
>
> ```bash theme={null}
> #!/bin/bash
> jq '{hookSpecificOutput: {hookEventName: "MessageDisplay", displayContent: (.delta | gsub("\\*\\*"; "") | gsub("`"; ""))}}'
> ```

> [tab] Windows (PowerShell)
>
> Зарегистрируйте командный хук, который запускает скрипт через PowerShell:
>
> ```json theme={null}
> {
>   "hooks": {
>     "MessageDisplay": [
>       {
>         "hooks": [
>           {
>             "type": "command",
>             "command": "powershell.exe",
>             "args": [
>               "-NoProfile",
>               "-ExecutionPolicy",
>               "Bypass",
>               "-File",
>               "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.ps1"
>             ]
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Флаг `-NoProfile` пропускает загрузку вашего профиля PowerShell, чтобы хук запускался быстро, а `-ExecutionPolicy Bypass` позволяет PowerShell выполнить локальный файл скрипта.
>
> Сохраните этот скрипт в `.claude/hooks/plain-display.ps1` в своём проекте:
>
> ```powershell theme={null}
> $batch = [Console]::In.ReadToEnd() | ConvertFrom-Json
> $text = $batch.delta -replace '\*\*', '' -replace '`', ''
> @{
>   hookSpecificOutput = @{
>     hookEventName = "MessageDisplay"
>     displayContent = $text
>   }
> } | ConvertTo-Json
> ```

Партии без markdown проходят без изменений. Если скрипт завершается с ошибкой, например из-за отсутствия `jq`, Claude Code отображает исходный текст и отмечает сбой только в [выводе отладки](#debug-hooks), а не в сессии.

### PreToolUse

Выполняется после того, как Claude сформирует параметры инструмента, и до обработки вызова инструмента. Сопоставляется с любым именем инструмента, кроме `EndConversation`: встроенными инструментами, такими как `Bash`, `PowerShell`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `Workflow`, `WebFetch`, `WebSearch`, `AskUserQuestion` и `ExitPlanMode`, а также любыми [именами MCP-инструментов](#match-mcp-tools).

Чтобы запускать хук при изменении конкретного файла на диске, независимо от того, что его записало, используйте [FileChanged](#filechanged) вместо сопоставления инструментов редактирования файлов по имени. В отличие от PreToolUse, Claude Code запускает хуки FileChanged после изменения, и у них нет управления решениями, поэтому они не могут заблокировать запись.

> [!WARNING]
>
> PreToolUse выполняется только тогда, когда Claude вызывает инструмент. По умолчанию файлы, на которые вы [ссылаетесь с помощью `@` в промпте](https://code.claude.com/docs/ru/common-workflows#reference-files-and-directories), добавляются без какого-либо вызова инструмента. Claude Code вставляет их содержимое при формировании промпта, поэтому для них не срабатывает ни один хук PreToolUse, включая хуки, соответствующие `Read`. PreToolUse также не срабатывает для [`EndConversation`](https://code.claude.com/docs/ru/tools-reference#endconversation-tool-behavior).
>
> Вы можете блокировать определённые пути в ссылках `@` или отключить вставку:
>
> * **Блокировка определённых путей**: добавьте для них [правило запрета `Read`](https://code.claude.com/docs/ru/permissions#read-and-edit)
> * **Отключение вставки**: задайте [`CLAUDE_CODE_DISABLE_FILE_MENTIONS=1`](https://code.claude.com/docs/ru/env-vars#variables) в своей оболочке, пользовательских настройках или управляемых настройках. Тогда Claude получает упомянутые пути с пометкой прочитать их с помощью своих файловых инструментов. Если он это делает, выполняются соответствующие хуки PreToolUse. Для этой переменной требуется Claude Code v2.1.299 или новее, и Claude Code игнорирует её в настройках проекта и локальных настройках.

Используйте [управление решениями PreToolUse](#pretooluse-decision-control), чтобы разрешить, запретить, запросить подтверждение или отложить вызов инструмента.

[Хук обратного вызова Agent SDK](https://code.claude.com/docs/ru/agent-sdk/hooks.md#hook-timeout) в `PreToolUse`, превысивший свой таймаут, блокирует вызов инструмента.

#### Входные данные PreToolUse

Помимо [общих входных полей](#common-input-fields), хуки PreToolUse получают `tool_name`, `tool_input` и `tool_use_id`.

Для [MCP-инструмента](#match-mcp-tools) входные данные также содержат `mcp_server` — объект с `name` сервера и `source`, указывающим, откуда взято определение сервера. Значения `source` включают `plugin`, `sdk` и области действия конфигурации, такие как `user` и `project`. [`McpServerProvenance`](https://code.claude.com/docs/ru/agent-sdk/typescript#mcpserverprovenance) в справочнике Agent SDK перечисляет их все и описывает, как обрабатывать нераспознанное значение. Основывайте решения о доверии на `source`, а не на `name` или префиксе имени инструмента `mcp__<server>__`. Для поля `mcp_server` требуется Claude Code v2.1.274 или новее.

Для файловых инструментов `Write`, `Edit` и `Read` значение `tool_input.file_path` всегда абсолютное:

* Claude Code раскрывает `~` и относительные пути до выполнения хуков, поэтому хук, сопоставляющий пути, нельзя обойти через `~` или относительную запись того же пути
* В Windows путь поступает с обратными косыми чертами в качестве разделителей, даже если ваш хук выполняется в Git Bash, где `$PWD` выглядит как `/c/project`
* Сравнение, записанное с прямыми косыми чертами, например проверка `/src/`, никогда не совпадёт с путём с обратными косыми чертами, и вызов инструмента продолжится так, будто хуку нечего было блокировать
* Нормализуйте разделители перед сравнением: `FILE_PATH="${FILE_PATH//\\//}"` в Bash или `file_path.replace("\\", "/")` в Python, а затем сопоставляйте сегмент пути, например `/src/`, а не привязывайтесь к началу с помощью `^`, поскольку путь абсолютный

Вызов `Write` в Windows передаёт:

```json theme={null}
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "C:\\project\\src\\index.ts",
    "content": "..."
  },
  ...
}
```

Поля `tool_input` зависят от инструмента:

##### Bash

Выполняет shell-команды.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `command` | string | `"npm test"` | Shell-команда для выполнения |
| `description` | string | `"Run test suite"` | Необязательное описание того, что делает команда |
| `timeout` | number | `120000` | Необязательный таймаут в миллисекундах. Значения выше [максимума](https://code.claude.com/docs/ru/tools-reference.md#bash-tool-behavior) уменьшаются до максимума, а не отклоняются |
| `run_in_background` | boolean | `false` | Выполнять ли команду в фоне |

Когда команда Bash изменяет файлы в репозитории Git, Claude Code может записывать, что изменилось. Он записывает изменения в любом режиме разрешений, когда это включено настройкой [`bashEditDiffEnabled`](https://code.claude.com/docs/ru/settings-reference#basheditdiffenabled); в описании этой настройки указано, какие файлы могут её задавать. В противном случае он записывает их только в авторежиме и режиме `bypassPermissions`, и только когда Claude Code направляет Claude редактировать файлы через Bash. Задайте `bashEditDiffEnabled` равным `false`, чтобы отключить запись. Фоновые команды и команды только для чтения не содержат diff.

Затем ваш [хук PostToolUse](#posttooluse) получает изменённые файлы в `tool_response.bashEditDiff`. Список охватывает то, что изменилось в репозитории во время выполнения команды. Файлы, которые игнорирует Git, и файлы в подмодулях не перечисляются. Требуется Claude Code v2.1.269 или новее.

> [!NOTE]
>
> Список формируется по принципу «насколько возможно» и доступен в публичной бета-версии. Claude Code может пропустить изменение, включить файл, который одновременно изменил другой процесс, или остановиться на своих ограничениях размера. Структура поля может измениться. Используйте список, чтобы найти, что проверить, а не для принудительного применения политики.

`changedFiles` и `files` перечисляют то, что изменила команда; остальные поля указывают, насколько полон и надёжен этот список.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `changedFiles` | array | `["/path/to/src/app.ts"]` | Абсолютные пути файлов, изменённых командой, не более 200. Присутствует всякий раз, когда `files` содержит diff или `moreFiles` больше нуля |
| `files` | array | `[{"filePath": "/path/to/src/app.ts", "hunks": [...]}]` | Diff до 5 изменённых файлов для отображения. `created` или `deleted` равно `true` для файла, который команда добавила или удалила |
| `moreFiles` | number | `2` | Количество изменённых файлов без diff в `files` |
| `unavailable` | boolean | `true` | Устанавливается, когда diff неполон или его не удалось получить |
| `skipped` | boolean | `true` | Устанавливается для команды Git, которая перемещает рабочее дерево, например `git checkout` или `git stash`, поэтому Claude Code не получает diff |
| `shared` | boolean | `true` | Устанавливается, когда другой вызов инструмента Bash, например от субагента, выполнялся в том же репозитории в то же время, поэтому некоторые перечисленные изменения могут принадлежать той команде |

##### PowerShell

Выполняет команды PowerShell. Доступность по платформам см. в описании [инструмента PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool).

Поля совпадают с инструментом Bash, строка команды находится в `command`:

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `command` | string | `"Get-ChildItem -Recurse"` | Команда PowerShell для выполнения |
| `description` | string | `"List files recursively"` | Необязательное описание того, что делает команда |
| `timeout` | number | `120000` | Необязательный таймаут в миллисекундах |
| `run_in_background` | boolean | `false` | Выполнять ли команду в фоне |

В хуках, проверяющих shell-команды, используйте matcher `Bash|PowerShell`, чтобы они охватывали оба инструмента:

* В Windows везде, где включён инструмент PowerShell, Claude считает PowerShell основной оболочкой и направляет shell-команды через него.
* В Windows без Git Bash инструмент включается автоматически, и Claude Code вообще не регистрирует инструмент Bash.
* Хук, соответствующий только `Bash`, там никогда не срабатывает.

##### Write

Создаёт или перезаписывает файл.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | Абсолютный путь к файлу для записи |
| `content` | string | `"file content"` | Содержимое для записи в файл |

##### Edit

Заменяет строку в существующем файле.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | Абсолютный путь к файлу для редактирования |
| `old_string` | string | `"original text"` | Текст для поиска и замены |
| `new_string` | string | `"replacement text"` | Текст замены |
| `replace_all` | boolean | `false` | Заменять ли все вхождения |

##### Read

Читает содержимое файла.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | Абсолютный путь к файлу для чтения |
| `offset` | number | `10` | Необязательный номер строки, с которой начинать чтение |
| `limit` | number | `50` | Необязательное количество строк для чтения |

##### Glob

Находит файлы, соответствующие glob-шаблону.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `pattern` | string | `"**/*.ts"` | Glob-шаблон для сопоставления файлов |
| `path` | string | `"/path/to/dir"` | Необязательный каталог для поиска. По умолчанию — текущий рабочий каталог |

##### Grep

Ищет в содержимом файлов с помощью регулярных выражений.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `pattern` | string | `"TODO.*fix"` | Шаблон регулярного выражения для поиска |
| `path` | string | `"/path/to/dir"` | Необязательный файл или каталог для поиска |
| `glob` | string | `"*.ts"` | Необязательный glob-шаблон для фильтрации файлов |
| `output_mode` | string | `"content"` | `"content"`, `"files_with_matches"` или `"count"`. По умолчанию `"files_with_matches"` |
| `-i` | boolean | `true` | Поиск без учёта регистра |
| `multiline` | boolean | `false` | Включить многострочное сопоставление |

##### WebFetch

Загружает и обрабатывает веб-содержимое.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `url` | string | `"https://example.com/api"` | URL, с которого загружается содержимое |
| `prompt` | string | `"Extract the API endpoints"` | Промпт, применяемый к загруженному содержимому |
| `offset` | number | `100000` | Необязательное количество символов, пропускаемых от начала страницы. Claude задаёт его, чтобы продолжить чтение длинной страницы. Требуется Claude Code v2.1.290 или новее |

##### WebSearch

Выполняет поиск в интернете.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `query` | string | `"react hooks best practices"` | Поисковый запрос |
| `allowed_domains` | array | `["docs.example.com"]` | Необязательно: включать результаты только с этих доменов |
| `blocked_domains` | array | `["spam.example.com"]` | Необязательно: исключать результаты с этих доменов |
| `mode` | string | `"extended"` | Необязательно: тип поиска. `"standard"` запрашивает облегчённый поиск, а `"extended"` — полный поиск. Некоторые сессии не отправляют `mode`, и вызов без него выполняет полный поиск. Требует Claude Code v2.1.282 или новее |

##### Agent

Запускает [субагента](https://code.claude.com/docs/ru/sub-agents.md).

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `prompt` | string | `"Find all API endpoints"` | Задача, которую должен выполнить агент |
| `description` | string | `"Find API endpoints"` | Краткое описание задачи |
| `subagent_type` | string | `"Explore"` | Тип используемого специализированного агента |
| `model` | string | `"sonnet"` | Необязательный псевдоним модели для переопределения модели по умолчанию |

Когда вызов Agent на переднем плане завершается, ваш [хук PostToolUse](#posttooluse) получает результат субагента и телеметрию запуска в `tool_response`. Читайте эти поля, чтобы проанализировать запуск; для сводных данных по токенам и стоимости по всем субагентам используйте [счётчики токенов и стоимости](https://code.claude.com/docs/ru/monitoring-usage.md#token-counter), отфильтрованные по `query_source` `"subagent"`, поскольку `totalTokens` и `usage` охватывают только последний запрос:

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `status` | string | `"completed"` | `"completed"` для субагентов на переднем плане, `"async_launched"` для фоновых субагентов. О том, какие субагенты как выполняются, см. [Запуск субагентов на переднем плане или в фоне](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background) |
| `agentId` | string | `"a4d2c8f1e0b3a297"` | Идентификатор запуска субагента |
| `content` | array | `[{"type": "text", "text": "Found 12 endpoints..."}]` | Финальные текстовые блоки субагента или, для субагента, чей отчёт передаётся через `SubagentHandback`, вместо них — краткая заметка об этой передаче |
| `resolvedModel` | string | `"claude-sonnet-4-5"` | Модель, на которой запустился субагент; может отличаться от запрошенной модели |
| `modelsUsed` | array | `["claude-sonnet-4-5", "claude-haiku-4-5"]` | Использованные модели по порядку, последовательные повторы схлопнуты; задаётся, только если модель менялась во время запуска |
| `totalTokens` | number | `12450` | Количество токенов из последнего API-запроса субагента: входные, выходные и кэш-токены вместе. Это не итог за весь запуск |
| `totalDurationMs` | number | `48211` | Реальная длительность запуска субагента |
| `totalToolUseCount` | number | `7` | Количество вызовов инструментов, сделанных субагентом |
| `usage` | object | `{"input_tokens": 8320, ...}` | Разбивка токенов последнего API-запроса по типам: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` |

В Claude Code v2.1.271 или новее субагент, работающий с инструментом [`SubagentHandback`](https://code.claude.com/docs/ru/tools-reference), который Claude Code предоставляет в [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), передаёт свой отчёт через этот инструмент, а не возвращает его как текст. Тогда поле `content` его результата `completed` содержит краткую заметку об этой передаче, а не сам отчёт. Чтобы прочитать отчёт, настройте хук `PreToolUse` или `PostToolUse` с matcher `SubagentHandback` и читайте `tool_input.message`.

Для фоновых субагентов инструмент возвращает результат, когда задача переходит в фон, поэтому `tool_response` не содержит полей использования: фоновый запуск возвращается сразу, а задача на переднем плане, которую Claude Code переводит в фон во время выполнения, возвращается в момент этого перехода. Он содержит `status: "async_launched"`, `agentId`, `description`, `prompt`, `outputFile` и `resolvedModel`.

В ответе `completed` поле `resolvedModel` указывает модель, на которой запустился субагент; она может отличаться от значения `model` в `tool_input`, например когда применяется `availableModels` или другое переопределение. В ответе `async_launched` поле `resolvedModel` указывает модель, использовавшуюся в момент перехода агента в фон, поэтому смена модели, произошедшая до перехода в фон, отражается там.

##### AskUserQuestion

Задаёт пользователю от одного до четырёх вопросов с вариантами ответа.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `questions` | array | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React", "description": "Component library"}, {"label": "Vue", "description": "Progressive framework"}], "multiSelect": false}]` | Вопросы для показа, каждый со строкой `question`, кратким `header`, массивом `options` и необязательным флагом `multiSelect` |
| `answers` | object | `{"Which framework?": "React"}` | Необязательно. Сопоставляет текст вопроса с меткой выбранного варианта. Ответы с множественным выбором объединяют метки через запятые. Claude не задаёт это поле; передайте его через `updatedInput`, чтобы отвечать программно |

##### ExitPlanMode

Представляет план и просит пользователя утвердить его, прежде чем Claude выйдет из [режима планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode). Claude записывает план в файл на диске перед вызовом инструмента, поэтому буквальный `tool_input` от модели обычно пуст. Claude Code внедряет содержимое плана и путь к файлу перед передачей входных данных хукам.

| Поле | Тип | Пример | Описание |
| :- | :- | :- | :- |
| `plan` | string | `"## Refactor auth\n1. Extract..."` | Содержимое плана в Markdown. Внедряется из файла плана на диске |
| `planFilePath` | string | `"/Users/.../plans/refactor-auth.md"` | Путь к файлу плана. Внедряется |
| `allowedPrompts` | array | `[{"tool": "Bash", "prompt": "run tests"}]` | Устаревшее. Claude Code принимает поле, но игнорирует его. До v2.1.205 оно содержало разрешения на основе промптов, которые Claude запрашивал для реализации плана |

В `PostToolUse` `tool_response` — это объект с полями `plan` и `filePath`, содержащими утверждённый план, а также внутренними флагами статуса. Читайте содержимое плана из `tool_response.plan`, а не перечитывайте файл с диска.

#### Управление решениями PreToolUse

Хуки `PreToolUse` могут управлять тем, будет ли выполнен вызов инструмента. В отличие от других хуков, использующих поле `decision` верхнего уровня, PreToolUse возвращает своё решение внутри объекта `hookSpecificOutput`. Это даёт более богатые возможности управления: четыре исхода (разрешить, запретить, запросить подтверждение или отложить), а также возможность изменить входные данные инструмента перед выполнением. О том, как разрешить или переписать команду Monitor, см. [Сопоставление команд Monitor](#match-monitor-commands).

| Поле | Описание |
| :- | :- |
| `permissionDecision` | `"allow"` пропускает запрос разрешения, за исключением [действий, которые не одобряет автоматически ни один режим](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves), и [чтения из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths). Оно также не пропускает подтверждение вызовов [инструментов, которые приложение Agent SDK помечает как `always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools), если только [режим разрешений не одобряет вызов](https://code.claude.com/docs/ru/agent-sdk/typescript.md#permission-modes-that-can-approve-an-always_ask-call). Для `AskUserQuestion` и `ExitPlanMode` нужен [`updatedInput` в паре с `"allow"`](#allow-with-updatedinput). О режиме планирования см. [Одобрение хуками в режиме планирования](https://code.claude.com/docs/ru/permissions.md#hook-approvals-in-plan-mode). `"deny"` предотвращает вызов инструмента. `"ask"` просит пользователя подтвердить. `"defer"` завершает ход, чтобы инструмент можно было возобновить позже, и требует [неинтерактивного режима](#defer-a-tool-call-for-later) с флагом `-p`. [Правила запрета и запроса подтверждения](https://code.claude.com/docs/ru/permissions.md#manage-permissions) всё равно проверяются независимо от того, что возвращает хук |
| `permissionDecisionReason` | Для `"ask"` показывается пользователю в запросе разрешения. Когда Claude Code [запрещает вызов](https://code.claude.com/docs/ru/headless.md#turn-off-permission-prompts-in-unattended-runs) в запуске `-p`, где никто не может ответить на этот запрос, Claude вместо этого читает причину в результате инструмента. Для `"deny"` показывается Claude. Для `"allow"` и `"defer"` записывается только в [лог отладки](#debug-hooks) |
| `updatedInput` | Изменяет входные параметры инструмента перед выполнением. Заменяет весь объект ввода, поэтому включайте неизменённые поля вместе с изменёнными. Claude Code оценивает правила разрешений и [возможность автоматического перевода в фон](https://code.claude.com/docs/ru/tools-reference.md#foreground-commands-that-move-to-the-background) команды Bash по вводу, который возвращает хук, а не по вводу, отправленному Claude. Сочетайте с `"allow"` для автоматического подтверждения или с `"ask"`, чтобы показать пользователю изменённый ввод. Для `"defer"` игнорируется. Без `permissionDecision` [авторежим может отклонить изменённый вызов](#pretooluse-updatedinput-in-auto-mode) |
| `additionalContext` | Строка, добавляемая в контекст Claude вместе с результатом инструмента. Игнорируется, когда `permissionDecision` равен `"defer"`. См. [Добавление контекста для Claude](#add-context-for-claude) |

Когда несколько хуков PreToolUse возвращают разные решения, приоритет таков: `deny` > `defer` > `ask` > `allow`.

Хук, который блокирует через выход с кодом 2, обрабатывается так же, как `"deny"`: Claude видит сообщение stderr как причину запрета.

Когда хук возвращает `"ask"`, запрос разрешения, показываемый пользователю, содержит метку, указывающую, откуда взят хук: `[settings]` для хука из любого файла настроек или из frontmatter агента, `[plugin:<name>]` для хука плагина или `[skill]` для хука из frontmatter скилла. Это помогает пользователям понять, какой источник конфигурации запрашивает подтверждение.

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

> [!NOTE]
>
> Ранее PreToolUse использовал поля `decision` и `reason` верхнего уровня, но для этого события они объявлены устаревшими. Используйте вместо них `hookSpecificOutput.permissionDecision` и `hookSpecificOutput.permissionDecisionReason`. Устаревшие значения `"approve"` и `"block"` соответствуют `"allow"` и `"deny"`. Другие события, такие как PostToolUse и Stop, по-прежнему используют `decision` и `reason` верхнего уровня в качестве текущего формата.

#### `updatedInput` в PreToolUse в авторежиме

Когда хук возвращает `updatedInput` без `permissionDecision` в [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), Claude Code может отклонить изменённый вызов. [Сервер проверил](https://code.claude.com/docs/ru/permission-modes.md#server-side-classifier-review) ввод, который написал Claude, а не ввод, который вернул хук. В интерактивных сессиях терминала и сессиях VS Code с прямым подключением к Anthropic API отказ содержит такой текст:

```text theme={null}
a hook changed this call's input after auto mode reviewed it
```

После отказа с этим текстом Claude может снова выполнить изменённый вызов, чтобы сервер его проверил. Если Claude в следующем ответе в точности повторяет изменённый ввод, ваш хук всё равно выполняется:

* Он может отклонить вызов или отправить его на запрос разрешения
* Любой возвращённый им `updatedInput` отбрасывается, поэтому выполняется то, что проверил сервер

Менять хук из-за этого отказа не нужно, если только [Claude не сообщит в ответе, что авторежим не смог проверить вызов](https://code.claude.com/docs/ru/errors.md#hook-changed-input-after-review).

В сессиях, где показывается этот текст, [`command`-хук](#command-hook-fields) в настройках или в файле хуков плагина может изменять вызовы Bash, PowerShell, Monitor, Edit, Write и NotebookEdit без этого отказа. Отказ всё же может появиться, например когда какой-либо хук изменил более ранний вызов в том же ответе Claude или команда Bash запрашивает выполнение вне песочницы.

#### Решения `ask` в PreToolUse в авторежиме

В [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) `"ask"` хука PreToolUse обычно отправляет вызов инструмента в запрос разрешения, и [классификатор](https://code.claude.com/docs/ru/permission-modes.md#how-the-classifier-evaluates-actions) по нему не решает. Некоторые вызовы идут другим путём:

* **Вызовы, которые также помечают собственные проверки Claude Code**: к ним относятся запись в [защищённые пути](https://code.claude.com/docs/ru/permission-modes.md#protected-paths) и команды, запрашивающие [выполнение вне песочницы](https://code.claude.com/docs/ru/sandboxing.md#the-unsandboxed-retry-escape-hatch). Классификатор может отклонить такой вызов до появления какого-либо запроса. Если он одобряет, вызов обычно всё равно попадает в запрос.
* **Вызовы `SubagentHandback`**: этот инструмент передаёт отчёт субагента. Для него запрос не появляется, и вызов выполняется, даже если классификатор возражает.

Чтобы остановить вызов `SubagentHandback`, верните `"deny"`. Тогда Claude Code сообщает субагенту — до трёх раз, — что его отчёт не был доставлен и что нужно вызвать инструмент снова. Если ваш хук продолжает отклонять, субагент завершается, не доставив отчёт через этот инструмент, а ожидающий его диалог получает примечание об этом.

#### Инструменты, требующие взаимодействия с пользователем

`AskUserQuestion` и `ExitPlanMode` требуют взаимодействия с пользователем. В [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) с флагом `-p` Claude Code предлагает их, только если у запуска есть [хост разрешений](https://code.claude.com/docs/ru/headless.md#turn-off-permission-prompts-in-unattended-runs), принимающий запрос, например callback `canUseTool` в Agent SDK.

Хук `PreToolUse` удовлетворяет этому требованию, если он делает следующее:

1. Считывает входные данные инструмента из stdin
2. Собирает ответ через ваш собственный интерфейс
3. Возвращает `permissionDecision: "allow"` вместе с `updatedInput`, содержащим ответ, чтобы инструмент выполнился без запроса

Одного возврата `"allow"` для этих инструментов недостаточно.

Для `AskUserQuestion` верните исходный массив `questions` и добавьте объект [`answers`](#askuserquestion), сопоставляющий текст каждого вопроса с выбранным ответом. Этот вывод отвечает на один вопрос вариантом `React`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "questions": [
        {
          "question": "Which framework?",
          "header": "Framework",
          "options": [{"label": "React", "description": "Component library"}, {"label": "Vue", "description": "Progressive framework"}],
          "multiSelect": false
        }
      ],
      "answers": {"Which framework?": "React"}
    }
  }
}
```

MCP-инструмент, который сервер помечает с помощью [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/ru/mcp#require-approval-for-a-specific-tool), обрабатывается строже: хук не может пропустить его запрос подтверждения с помощью `"allow"`, с `updatedInput` или без, поскольку Claude Code не может убедиться, что хук собрал взаимодействие, необходимое инструменту.

#### Отложить вызов инструмента на потом

`"defer"` предназначен для интеграций, которые запускают `claude -p` как подпроцесс и читают его вывод в формате JSON, например для приложения на Agent SDK или собственного интерфейса, построенного поверх Claude Code. Он позволяет вызывающему процессу приостановить Claude на вызове инструмента, собрать ввод через собственный интерфейс и продолжить с того места, где работа была прервана.

Claude Code учитывает `"defer"` только в [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) с флагом `-p` и только когда Claude делает единственный вызов инструмента за ход:

* **В интерактивных сессиях**: записывается предупреждение, а результат хука игнорируется
* **Несколько вызовов инструментов одновременно**: `"defer"` игнорируется с предупреждением, и инструмент проходит обычный процесс проверки разрешений

Типичный случай — инструмент `AskUserQuestion`: Claude хочет что-то спросить у пользователя, но терминала для ответа нет. Запуск `-p` предлагает `AskUserQuestion` только при наличии [хоста разрешений](https://code.claude.com/docs/ru/headless.md#turn-off-permission-prompts-in-unattended-runs), например MCP-инструмента, который вы передаёте через `--permission-prompt-tool`, поэтому начинайте запуск с ним. Цикл работает так:

1. Claude вызывает `AskUserQuestion`. Срабатывает хук `PreToolUse`.
2. Хук возвращает `permissionDecision: "defer"`. Инструмент не выполняется. Ход завершается результатом с `stop_reason: "tool_deferred"`, а ожидающий вызов инструмента остаётся в транскрипте.
3. Вызывающий процесс читает `deferred_tool_use` из результата SDK, показывает вопрос в своём интерфейсе и ждёт ответа.
4. Вызывающий процесс выполняет `claude -p --resume <session-id>` с тем же хостом разрешений. Тот же вызов инструмента снова вызывает `PreToolUse`.
5. Хук возвращает `permissionDecision: "allow"` с ответом в `updatedInput`. Инструмент выполняется, и Claude продолжает работу.

Поле `deferred_tool_use` содержит `id`, `name` и `input` инструмента:

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React", "description": "Component library"}, {"label": "Vue", "description": "Progressive framework"}], "multiSelect": false }] }
  }
}
```

Ни таймаута, ни ограничения на число повторных попыток нет. Сессия хранится на диске, пока её не удалит [плановая очистка](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically) по [`cleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#cleanupperioddays), по умолчанию через 30 дней.

Если ответ ещё не готов к моменту возобновления, хук может снова вернуть `"defer"`. Если при этом возобновлении вы отправили промпт, Claude ответит на него без результата инструмента и не выполнит вызов. Возобновляйте без промпта, пока хук не вернёт `"allow"` или `"deny"`.

> [!NOTE]
>
> Чтобы возобновить отложенную сессию в режиме планирования, передайте [`--permission-prompt-tool`](https://code.claude.com/docs/ru/cli-reference#cli-flags) вместе с `--resume`, чтобы Claude Code мог представить план на утверждение. Прочие условия см. в разделе [Возобновление в режиме планирования с `-p`](https://code.claude.com/docs/ru/sessions#resume-in-plan-mode-with-p). Требуется Claude Code v2.1.246 или новее.
>
> При возобновлении с `-p` Claude Code не восстанавливает никакой другой сохранённый режим разрешений. Запуск начинается в том режиме разрешений, в котором начался бы новый запуск `claude -p`, поэтому снова передайте `--permission-mode` или `--dangerously-skip-permissions`, если отложенная сессия их использовала.

##### Возобновление, когда отложенный инструмент недоступен

Результат с `stop_reason: "tool_deferred_unavailable"` означает, что инструмент отложенного вызова недоступен в возобновлённой сессии, например потому что его MCP-сервер не подключён. Ваш хук `PreToolUse` не срабатывает, а поле `deferred_tool_use` результата указывает инструмент.

Пока вызов ожидает, любой отправленный вами промпт не доходит до Claude, а запуск завершается с кодом выхода 1. Поле `result` начинается с `<tool> isn't available, so its deferred call didn't run.` Выполните вызов или отбросьте его, чтобы он не выполнялся:

* **Чтобы выполнить вызов**: сделайте инструмент доступным и возобновите сессию снова.
* **Чтобы отбросить вызов**: возобновите сессию с промптом, установив [`CLAUDE_CODE_DROP_UNAVAILABLE_DEFERRED_TOOL`](https://code.claude.com/docs/ru/env-vars#variables) в `1`. Claude получит ошибку в качестве результата вызова и ответит на ваш промпт. При следующем возобновлении ожидающих вызовов не будет.

Когда вы отбрасываете вызов, запуск записывает результат `tool_deferred_unavailable` с пустым полем `result`, а затем ответ Claude во втором результате. Он завершается с кодом выхода 0, если только этот ответ не является ошибкой. Если вы установите переменную и не отправите промпт, запуск всё равно отбросит вызов и завершится с кодом выхода 1.

До v2.1.319 Claude Code отвечал на промпт без результата инструмента и отбрасывал вызов. В этих версиях отправьте новый промпт, когда инструмент станет доступен.

### PermissionRequest

Выполняется, когда Claude Code собирается запросить у вас разрешение на использование инструмента. В сессиях, которые не могут показать запрос, например у фоновых субагентов в [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md), Claude Code всё равно запускает эти хуки, и если ни один хук не вернёт решение, он запрещает вызов инструмента. Для вызова, который доходит до `--permission-prompt-tool` или [callback `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/permissions) в Agent SDK, хуки выполняются параллельно с вашим хостом, и применяется решение того, кто примет его первым.
Используйте [управление решениями PermissionRequest](#permissionrequest-decision-control), чтобы разрешать или запрещать от имени пользователя.

Используйте это событие, когда вам нужен сигнал в тот момент, когда Claude запрашивает разрешение на использование инструмента. Claude Code запускает хук [Notification](#notification) с типом `permission_prompt` только после того, как запрос прождёт около шести секунд.

Claude Code не запускает хуки PermissionRequest для [сетевого запроса](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) команды, выполняемой в песочнице. Чтобы получить сигнал для такого запроса, используйте тип уведомления `permission_prompt`.

Сопоставляется с именем инструмента, с теми же значениями, что и PreToolUse.

#### Входные данные PermissionRequest

Хуки PermissionRequest получают поля `tool_name` и `tool_input`, как и хуки PreToolUse, но без `tool_use_id`. Для инструмента MCP они также получают объект [`mcp_server`](#pretooluse-input). Необязательный массив `permission_suggestions` содержит [обновления разрешений](#permission-update-entries), которые Claude Code предлагает для этого запроса, например добавление разрешающего правила или изменение режима разрешений.

Массив `permission_suggestions` не является точным списком вариантов, которые вы видите, поскольку каждое диалоговое окно разрешения формирует собственные варианты. Некоторые диалоговые окна, например окно для правок файлов, вообще не читают этот массив и получают варианты из самого запроса. Диалоговое окно, которое читает массив, всё равно может скрыть вариант, предложение для которого остаётся в массиве, например когда [`allowManagedPermissionRulesOnly`](https://code.claude.com/docs/ru/settings-reference#allowmanagedpermissionrulesonly) скрывает варианты сохранения правил. Оно также может предлагать варианты, для которых нет записи в предложениях, например [**Yes, and switch to auto mode**](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes), который меняет режим разрешений напрямую, а не через обновление разрешений.

Хуки PreToolUse запускаются перед каждым вызовом инструмента, независимо от того, требуется ли для него разрешение. Хуки PermissionRequest запускаются только тогда, когда Claude Code собирается запросить у вас разрешение, или когда он в противном случае автоматически отклонил бы вызов, для которого невозможно показать запрос. Ни одно из этих событий не срабатывает для [`EndConversation`](https://code.claude.com/docs/ru/tools-reference#endconversation-tool-behavior).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### Управление решениями PermissionRequest

Хуки `PermissionRequest` могут разрешать или отклонять запросы разрешений. Помимо [полей вывода JSON](#json-output), доступных всем хукам, ваш скрипт хука может вернуть объект `decision` со следующими полями, специфичными для события:

| Поле | Описание |
| :- | :- |
| `behavior` | `"allow"` предоставляет разрешение, `"deny"` отклоняет его. [Правила запрета и запроса](https://code.claude.com/docs/ru/permissions.md#manage-permissions) всё равно проверяются, поэтому хук, возвращающий `"allow"`, не переопределяет совпадающее правило запрета |
| `updatedInput` | Только для `"allow"`: изменяет входные параметры инструмента перед выполнением. Заменяет весь объект входных данных, поэтому включайте неизменённые поля вместе с изменёнными. Изменённые входные данные повторно проверяются на соответствие правилам запрета и запроса. `AskUserQuestion` и `ExitPlanMode` [требуют это поле](#allow-with-updatedinput) |
| `updatedPermissions` | Только для `"allow"`: массив [записей обновления разрешений](#permission-update-entries) для применения, например добавление разрешающего правила или изменение режима разрешений сессии |
| `message` | Только для `"deny"`: сообщает Claude, почему разрешение было отклонено |
| `interrupt` | Только для `"deny"`: если `true`, останавливает Claude |

Чтобы разрешить или переписать команду Monitor, см. раздел [Сопоставление команд Monitor](#match-monitor-commands).

Хук, завершающийся с кодом 2 без объекта `decision`, оставляет процесс обработки разрешения без изменений, а его stderr отбрасывается. Чтобы предоставить или отклонить запрос, верните объект `decision`.

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Записи обновления разрешений

Поле вывода `updatedPermissions` и [поле ввода `permission_suggestions`](#permissionrequest-input) используют один и тот же массив объектов-записей. Каждая запись имеет поле `type`, определяющее её остальные поля, и поле `destination`, которое управляет тем, куда записывается изменение.

| `type` | Поля | Эффект |
| :- | :- | :- |
| `addRules` | `rules`, `behavior`, `destination` | Добавляет правила разрешений. `rules` — массив объектов `{toolName, ruleContent?}`. Опустите `ruleContent`, чтобы правило соответствовало всему инструменту. `behavior` принимает значения `"allow"`, `"deny"` или `"ask"` |
| `replaceRules` | `rules`, `behavior`, `destination` | Заменяет все правила с указанным `behavior` в `destination` на переданные `rules` |
| `removeRules` | `rules`, `behavior`, `destination` | Удаляет совпадающие правила с указанным `behavior` |
| `setMode` | `mode`, `destination` | Изменяет режим разрешений. Допустимые режимы: `default`, `auto`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, а также `manual` как псевдоним для `default` |
| `addDirectories` | `directories`, `destination` | Добавляет рабочие каталоги. `directories` — массив строк с путями |
| `removeDirectories` | `directories`, `destination` | Удаляет рабочие каталоги |

В `rules` для [правила разрешений](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax), записанного как `Tool(specifier)`, `toolName` — это имя инструмента, а `ruleContent` — спецификатор:

* `Bash(npm test)`: `{ "toolName": "Bash", "ruleContent": "npm test" }`
* `Bash` или `Bash(*)`: `{ "toolName": "Bash" }`, потому что оба соответствуют всему инструменту
* `mcp__github__get_issue`: `{ "toolName": "mcp__github__get_issue" }`

Не указывайте `ruleContent` в разрешающем правиле для [MCP-инструмента](https://code.claude.com/docs/ru/permissions.md#mcp). Если его добавить, правило не будет соответствовать ни одному вызову.

> [!NOTE]
>
> `setMode` с `bypassPermissions` вступает в силу, только если вы запустили сессию, когда режим обхода уже был доступен: `--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions` или `permissions.defaultMode: "bypassPermissions"` в [пользовательских настройках, `--settings` или управляемых настройках](https://code.claude.com/docs/ru/settings-reference#permissions-defaultmode). В противном случае обновление ничего не делает. Обновление также ничего не делает, когда [`permissions.disableBypassPermissionsMode`](https://code.claude.com/docs/ru/permissions#managed-settings) отключает этот режим или когда сессия запускается в [ограниченном режиме](https://code.claude.com/docs/ru/cli-reference.md#cli-flags).
>
> `bypassPermissions` никогда не сохраняется как `defaultMode`, независимо от `destination`.

Поле `destination` в каждой записи определяет, останется ли изменение в памяти или будет сохранено в файл настроек.

| `destination` | Куда записывается |
| :- | :- |
| `session` | только в памяти, отбрасывается по завершении сессии |
| `localSettings` | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json` |
| `userSettings` | `~/.claude/settings.json` |

Хук может вернуть одно из полученных `permission_suggestions` в качестве собственного вывода `updatedPermissions`.

### PostToolUse

Запускается сразу после успешного завершения инструмента.

Сопоставляется по имени инструмента, с теми же значениями, что и PreToolUse.

Используйте более широкое сопоставление, когда имя инструмента не подходит в качестве фильтра:

* Чтобы запускать хук после успешного завершения любого инструмента, опустите `matcher` или установите его в `"*"`. Тогда ваш хук может сам определить, что изменилось, например выполнив `git status --porcelain`, который также перечисляет неотслеживаемые файлы, пропускаемые `git diff`. Для вызовов инструментов, завершившихся с ошибкой, добавьте тот же хук в [PostToolUseFailure](#posttoolusefailure).
* Чтобы запускать хук при изменении определённого файла на диске, независимо от того, кто его записал, используйте [FileChanged](#filechanged). Claude Code не запускает хук `PostToolUse` с matcher `Edit|Write`, когда тот же файл перезаписывает команда `Bash` или процесс вне Claude Code.

#### PostToolUse после прерывания

Если хук `PostToolUse` останавливается раньше времени после того, как вы отправили сообщение или прервали работу во время вызова инструмента, проверьте, нажали ли вы `Ctrl+Enter`, `Enter` или `Esc`:

* **`Ctrl+Enter`**: если нажатие [завершает ход](https://code.claude.com/docs/ru/interactive-mode.md#when-claude-code-sends-what-you-queued) во время работы инструмента и инструмент завершается, ваши хуки `PostToolUse` выполняются на его результате, и у них есть 10 секунд на завершение. Клавиша действует как `Esc`, если вы поставили в очередь команду `!` перед своими сообщениями или фоновые задачи отключены, например с помощью [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](https://code.claude.com/docs/ru/env-vars#variables).
* **`Enter`**: сообщение, поставленное в очередь с помощью `Enter`, не прерывает ход, поэтому хуки сохраняют свой обычный `timeout`.
* **`Esc`**: вы сразу отменяете хуки, поэтому отправляйте сообщение с помощью `Enter` или `Ctrl+Enter`, когда хуки должны выполниться.

Когда 10 секунд истекают, Claude Code завершает всё ещё работающий хук команды, независимо от его [`timeout`](#common-fields). Чтобы позволить более долгому хуку команды завершиться, запускайте его с [`async: true`](#run-hooks-in-the-background); это означает, что хук не сможет заблокировать или переписать результат.

До v2.1.319 хуки не запускались после того, как вы прерывали ход сообщением, а работающий хук останавливался.

#### Входные данные PostToolUse

Хуки `PostToolUse` срабатывают после того, как инструмент уже успешно выполнился. Входные данные включают как `tool_input` — аргументы, переданные инструменту, так и `tool_response` — возвращённый им результат. Точная схема обоих полей зависит от инструмента. Пути в `tool_input` файловых инструментов приходят в том же формате, что и для [PreToolUse](#pretooluse-input): всегда абсолютные, с нативными разделителями платформы, то есть с обратными слешами в Windows. Для инструмента MCP входные данные также содержат объект [`mcp_server`](#pretooluse-input).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "type": "create"
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| Поле | Описание |
| :- | :- |
| `duration_ms` | Необязательное. Время выполнения инструмента в миллисекундах. Не включает время, проведённое в запросах разрешений и хуках PreToolUse |

#### Управление решениями PostToolUse

Хуки `PostToolUse` могут предоставлять Claude обратную связь после выполнения инструмента. Помимо [полей вывода JSON](#json-output), доступных всем хукам, ваш скрипт хука может вернуть следующие поля, специфичные для события:

| Поле | Описание |
| :- | :- |
| `decision` | `"block"` добавляет `reason` рядом с результатом инструмента. Claude по-прежнему видит исходный вывод; чтобы заменить его, используйте `updatedToolOutput` |
| `reason` | Объяснение, показываемое Claude, когда `decision` равно `"block"` |
| `additionalContext` | Строка, добавляемая в контекст Claude вместе с результатом инструмента. См. [Добавление контекста для Claude](#add-context-for-claude) |
| `classifierContext` | Краткое примечание о результате этого вызова, предназначенное для классификатора [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), а не для Claude. См. [Аннотирование результата для классификатора авторежима](#annotate-a-result-for-the-auto-mode-classifier). Требуется Claude Code v2.1.236 или новее |
| `updatedToolOutput` | Заменяет вывод инструмента переданным значением до того, как он будет отправлен Claude. Значение должно соответствовать структуре вывода инструмента. В облачной сессии [Cowork](https://claude.com/docs/cowork/overview) Claude Code игнорирует это поле, когда инструментом является `AskUserQuestion` или `ExitPlanMode`, и Claude читает исходный ответ или план |
| `updatedMCPToolOutput` | Заменяет вывод только для [MCP-инструментов](#match-mcp-tools). Предпочитайте `updatedToolOutput`, который работает и для встроенных инструментов |

Пример ниже заменяет вывод вызова `Bash`. Значение замены соответствует форме вывода инструмента `Bash`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

> [!WARNING]
>
> `updatedToolOutput` изменяет только то, что видит Claude. К моменту срабатывания хука инструмент уже выполнился, поэтому все записанные файлы, выполненные команды или отправленные сетевые запросы уже вступили в силу. Телеметрия, такая как спаны инструментов OpenTelemetry и аналитические события, также фиксирует исходный вывод до запуска хука. Чтобы предотвратить или изменить вызов инструмента до его выполнения, используйте вместо этого хук [PreToolUse](#pretooluse).
>
> Значение замены должно соответствовать форме вывода инструмента. Встроенные инструменты возвращают структурированные объекты, а не простые строки. Например, `Bash` возвращает объект с полями `stdout`, `stderr`, `interrupted` и `isImage`. Для встроенных инструментов значение, не соответствующее схеме вывода инструмента, игнорируется, и используется исходный вывод. Вывод инструментов MCP передаётся без проверки схемы. Удаление сведений об ошибках, которые нужны Claude, может привести к тому, что он продолжит работу на основе ложного предположения.

#### Аннотирование результата для классификатора авторежима

Верните `classifierContext`, чтобы отправить короткую заметку о результате вызова инструмента классификатору [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), а не Claude. Заметка предназначена для проверки классификатором последующих действий. Поле требует Claude Code v2.1.236 или новее.

Пример ниже сообщает классификатору, откуда получен вывод запроса:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "classifierContext": "This query ran against the staging database, not production."
  }
}
```

Какой вес классификатор придаёт примечанию, зависит от того, где вы настроили хук:

* **Хуки, настроенные в Claude Code**: для хуков из файлов настроек, плагинов, скиллов и frontmatter агентов классификатор рассматривает примечание как непроверенный контекст, предоставленный приложением. Примечание никогда не устанавливает намерение пользователя, и если оно утверждает, что вы что-то одобрили или запросили, классификатор сверяет это утверждение с вашими собственными сообщениями в диалоге
* **Внутрипроцессные обратные вызовы Agent SDK**: когда приложение, встраивающее Claude Code, регистрирует хук как [обратный вызов TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/hooks.md) и возвращает примечание во время активной сессии, классификатор может учитывать переданное в примечании утверждение пользователя как намерение пользователя. Такое утверждение может удовлетворить требование согласия, которое классификатор принял бы от отправленного вами сообщения, но оно никогда не снимает блокировку, которую не смогло бы снять и ваше собственное сообщение. После возобновления сессии Claude Code рассматривает восстановленные примечания как непроверенный контекст. Когда хуки из обеих групп аннотируют один и тот же вызов, классификатор рассматривает объединённое примечание как непроверенное

При доставке примечания Claude Code применяет следующие ограничения:

* **Длина**: Claude Code ограничивает примечания для одного вызова инструмента 2000 символами и обрезает остальное. Ограничение общее для всех хуков, отвечающих на этот вызов
* **Только синхронные ответы**: Claude Code игнорирует это поле в ответе хука, который [выполняется в фоне](#run-hooks-in-the-background), поскольку такой ответ приходит после того, как Claude Code записал результат инструмента
* **Вызовы, которые классификатор не записывает**: транскрипт классификатора не включает операции только для чтения, такие как чтение файлов и поиск. Claude Code отбрасывает примечание, прикреплённое к одному из таких вызовов
* **Взаимодействие с перезаписью**: когда примечание описывает вывод, который вы заменяете с помощью `updatedToolOutput`, возвращайте оба поля в одном ответе хука. Claude Code отбрасывает примечание, если эта перезапись отклонена или её заменяет перезапись другого хука. Claude Code доставляет примечание, возвращённое без перезаписи, даже если другой хук перезаписывает вывод

> [!WARNING]
>
> Классификатор читает содержимое, помещённое вами в `classifierContext`, как информацию от приложения, в котором размещена сессия, поэтому не копируйте в него ненадёжный вывод инструментов или сторонний текст. Ограничивайте примечание кратким утверждением об этом одном вызове, например фактом о его происхождении или утверждением пользователя о нём; не используйте это поле для доставки посторонних сообщений или потока событий.

### PostToolUseFailure

Запускается, когда инструмент, начавший выполнение, завершается с ошибкой: инструмент выбросил ошибку или инструмент MCP вернул результат с ошибкой. Используйте это для логирования сбоев, отправки оповещений или предоставления Claude корректирующей обратной связи.

Сопоставляется по имени инструмента, с теми же значениями, что и PreToolUse.

> [!NOTE]
>
> Это событие не срабатывает для вызовов инструментов, отклонённых до выполнения: неизвестное имя инструмента, входные данные, не прошедшие проверку схемы или специфичную для инструмента валидацию, или отказ в разрешении. Отклонения при валидации возвращаются как результаты `tool_use_error` и происходят до запуска хуков, поэтому не вызывают ни `PreToolUse`, ни `PostToolUseFailure`. Отказы в разрешении вызывают `PreToolUse`, но не это событие; см. [PermissionDenied](#permissiondenied).

#### Входные данные PostToolUseFailure

Хуки PostToolUseFailure получают те же поля `tool_name` и `tool_input`, что и PostToolUse, а также информацию об ошибке в виде полей верхнего уровня. Для инструмента MCP они также получают объект [`mcp_server`](#pretooluse-input). Например, неудавшаяся команда `npm test` может передать:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Exit code 1\nError: Cannot find module 'express'",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| Поле | Описание |
| :- | :- |
| `error` | Строка, описывающая, что пошло не так. Формат зависит от инструмента, завершившегося с ошибкой |
| `is_interrupt` | Необязательное логическое значение. True, когда сбой дошёл до Claude Code как прерывание, а не как ошибка, о которой сообщил инструмент. Отмена выполняющегося инструмента не вызывает этот хук; вместо этого результат инструмента содержит сообщение о прерывании |
| `duration_ms` | Необязательное. Время выполнения инструмента в миллисекундах. Не включает время, проведённое в запросах разрешений и хуках PreToolUse |

Строка `error` обычно совпадает с текстом, который Claude получает как результат неудавшегося инструмента. Её формат зависит от инструмента и сбоя. Ориентируйте свой хук на `tool_name`, `is_interrupt` и первую строку `Exit code N`; остальную часть строки рассматривайте как текст для отображения, а не как стабильный формат.

* Для Bash и PowerShell команда, которая выполнилась и завершилась, даёт первую строку `Exit code N`, а затем любой вывод команды одним блоком, где stdout и stderr перемежаются
* Данные события также могут содержать просто сообщение о сбое без строки с кодом выхода, когда Claude Code не смог запустить сам процесс оболочки
* Claude Code обрезает длинные строки посередине вокруг маркера `... [N characters truncated] ...` и может вставлять собственные строки, например `Command timed out after 2m 0s`

#### Управление решениями PostToolUseFailure

Хуки `PostToolUseFailure` могут предоставлять Claude контекст после сбоя инструмента. Помимо [полей вывода JSON](#json-output), доступных всем хукам, ваш скрипт хука может вернуть следующие поля, специфичные для события:

| Поле | Описание |
| :- | :- |
| `additionalContext` | Строка, добавляемая в контекст Claude вместе с ошибкой. См. [Добавление контекста для Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PostToolBatch

Запускается один раз после того, как все вызовы инструментов в пакете завершены, до того как Claude Code отправит следующий запрос модели. `PostToolUse` срабатывает один раз для каждого инструмента, а значит, срабатывает параллельно, когда Claude делает параллельные вызовы инструментов. `PostToolBatch` срабатывает ровно один раз со всем пакетом, поэтому это подходящее место для внедрения контекста, который зависит от набора выполненных инструментов, а не от какого-либо одного инструмента. Для этого события нет matcher.

#### Входные данные PostToolBatch

Помимо [общих полей входных данных](#common-input-fields), хуки PostToolBatch получают `tool_calls` — массив, описывающий каждый вызов инструмента в пакете:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "1\tfrom __future__ import annotations\n2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "1\tfrom __future__ import annotations\n2\t..."
    }
  ]
}
```

`tool_response` содержит то же содержимое, которое модель получает в соответствующем блоке `tool_result`. Значение — это сериализованная строка или массив блоков содержимого, ровно в том виде, в каком его выдал инструмент. Для `Read` это означает текст с префиксами номеров строк, а не необработанное содержимое файла. Ответы могут быть большими, поэтому разбирайте только нужные поля.

> [!NOTE]
>
> Форма `tool_response` отличается от формы в `PostToolUse`. `PostToolUse` передаёт структурированный объект `Output` инструмента, например `{filePath: "...", type: "create"}` для `Write`; `PostToolBatch` передаёт сериализованное содержимое `tool_result`, которое видит модель.

#### Управление решениями PostToolBatch

Хуки `PostToolBatch` могут внедрять контекст для Claude. Помимо [полей вывода JSON](#json-output), доступных всем хукам, ваш скрипт хука может вернуть следующие поля, специфичные для события:

| Поле | Описание |
| :- | :- |
| `additionalContext` | Строка контекста, внедряемая один раз перед следующим вызовом модели. См. [Добавление контекста для Claude](#add-context-for-claude), где описаны подробности доставки, что в неё помещать и как возобновлённые сессии обрабатывают прошлые значения |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

Возврат `decision: "block"` или `continue: false` останавливает агентный цикл перед следующим вызовом модели. Сообщение о блокировке берётся из JSON-поля `reason` или `stopReason` либо из stderr при коде выхода 2. Вы видите его как предупреждение в транскрипте, и оно остаётся в диалоге, поэтому Claude видит его при продолжении диалога.

### PermissionDenied

Запускается, когда [авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) отклоняет вызов инструмента, в том числе когда он отклоняет его без вердикта классификатора, потому что [проверка безопасности, отдельная от авторежима, отклонила собственный запрос классификатора](https://code.claude.com/docs/ru/errors.md#auto-mode-cannot-determine-the-safety-of-an-action) или его ответ не удалось разобрать. Этот хук срабатывает только в авторежиме: он не запускается, когда вы вручную отклоняете диалоговое окно разрешения, когда хук `PreToolUse` блокирует вызов или когда срабатывает правило `deny`. Используйте его для логирования отказов, корректировки конфигурации или для того, чтобы сообщить модели, что она может повторить попытку вызова инструмента.

Сопоставляется по имени инструмента, с теми же значениями, что и PreToolUse.

#### Входные данные PermissionDenied

Помимо [общих полей входных данных](#common-input-fields), хуки PermissionDenied получают `tool_name`, `tool_input`, `tool_use_id` и `reason`. Для инструмента MCP они также получают объект [`mcp_server`](#pretooluse-input).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "[Irreversible Local Destruction]"
}
```

| Поле | Описание |
| :- | :- |
| `reason` | Причина отказа |

При логировании отказов ожидайте в `reason` текст вроде следующего:

* **Вердикт классификатора**: в большинстве сессий — совпавшая [политика](https://code.claude.com/docs/ru/auto-mode-config.md#fix-a-policy-denial) или правило в квадратных скобках, например `[Destructive or Unwanted Actions]`. Другие формы см. в разделе [Просмотр отказов](https://code.claude.com/docs/ru/auto-mode-config.md#review-denials).
* **[Нет вердикта от классификатора](#permissiondenied-decision-control)**: начинается с `Auto mode could not evaluate this action and is blocking it for safety`
* **Модель классификатора недоступна или [серверная проверка завершилась неудачей или по таймауту](https://code.claude.com/docs/ru/errors.md#the-server-returned-no-safety-verdict)**: текст `Classifier unavailable`

#### Управление решениями PermissionDenied

Хуки PermissionDenied могут сообщить модели, что она может повторить попытку отклонённого вызова инструмента. Верните JSON-объект с `hookSpecificOutput.retry`, установленным в `true`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Когда `retry` равно `true`, Claude Code добавляет в диалог сообщение, сообщающее модели, что она может повторить попытку вызова инструмента. Сам отказ Claude Code не отменяет. Если ваш хук не возвращает JSON или возвращает `retry: false`, отказ остаётся в силе, и модель получает исходное сообщение об отклонении.

Claude Code игнорирует `retry: true`, когда классификатор [не вынес вердикта по действию](https://code.claude.com/docs/ru/errors.md#auto-mode-cannot-determine-the-safety-of-an-action): его ответ не удалось разобрать или проверка безопасности, отдельная от авторежима, отклонила собственный запрос классификатора. Для таких отказов Claude Code уже сообщает модели в сообщении об отклонении, следует ли повторить попытку позже или двигаться дальше.

### Notification

Запускается, когда Claude Code отправляет уведомления. Сопоставляется по типу уведомления. Опустите matcher, чтобы запускать хуки для всех типов уведомлений.

Вы получаете эти события хуков даже при отключённых уведомлениях на рабочем столе: настройка `preferredNotifChannel`, включая `notifications_disabled`, меняет только способ оповещения, но не то, запускается ли ваш хук.

| Matcher | Когда срабатывает |
| :- | :- |
| `permission_prompt` | Claude нужно ваше подтверждение для использования инструмента или [сетевого запроса](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) команды в песочнице, и запрос ожидает около шести секунд |
| `idle_prompt` | Claude закончил отвечать около 60 секунд назад, и с тех пор вы ничего не вводили |
| `auth_success` | Аутентификация завершена |
| `auth_storage_failure` | Вход выполнен, но Claude Code не может сохранить новые учётные данные в своё [хранилище учётных данных](https://code.claude.com/docs/ru/authentication.md#credential-management). Срабатывает вместо `auth_success` |
| `elicitation_dialog` | MCP-сервер открывает форму запроса данных, и вы ничего не вводили около шести секунд |
| `elicitation_url_dialog` | MCP-сервер просит вас открыть URL в браузере, и вы ничего не вводили около шести секунд |
| `elicitation_complete` | MCP-сервер сообщает, что [запрос данных в режиме URL](#elicitation-input) завершён |
| `elicitation_response` | Ответ на запрос данных MCP отправлен обратно на сервер |
| `agent_needs_input` | Фоновая сессия начинает ожидать вашего ввода, пока в терминале открыт [вид агентов](https://code.claude.com/docs/ru/agent-view.md). Также срабатывает, когда терминальная сессия показывает вам [вопрос о настройке терминала от участника команды агентов](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode) или уведомление авторежима о [плате за запросы классификатора](https://code.claude.com/docs/ru/auto-mode-classifier-billing.md), и вы ничего не вводили около шести секунд |
| `agent_completed` | Фоновая сессия завершается или завершается с ошибкой. Срабатывает, только пока в терминале открыт [вид агентов](https://code.claude.com/docs/ru/agent-view.md) |
| `quota_auto_resume_fired` | Claude Code продолжает вашу задачу после того, как её приостановил лимит использования claude.ai: в момент сброса или раньше, когда какое-то ваше действие в Claude Code во время ожидания, например добавление кредитов использования, повышение тарифа или смена модели, снова делает использование доступным, с [исключением для настройки модели](https://code.claude.com/docs/ru/interactive-mode.md#wait-for-a-usage-limit-to-reset) |
| `quota_auto_resume_stale` | Лимит использования claude.ai сбросился, пока ваш компьютер находился в спящем режиме более 30 минут. Claude Code ждёт, пока вы нажмёте `Enter`, вместо того чтобы продолжить. После более короткого сна он продолжает работу и вместо этого срабатывает `quota_auto_resume_fired` |
| `quota_auto_resume_disabled` | Claude Code прекращает ожидание лимита использования claude.ai, не продолжая вашу задачу: [`autoContinueAtUsageLimit`](https://code.claude.com/docs/ru/settings-reference#autocontinueatusagelimit) был отключён или сброс сместился более чем на 24 часа вперёд во время ожидания, которое Claude Code начал самостоятельно, продолженная задача продолжала упираться в лимит, или продолжение было заблокировано до того, как дошло до модели. Не срабатывает, когда вы нажимаете `Esc` или `Ctrl+C` или выбираете **Don't continue automatically** |
| `plugin_notification` | [Мод](https://code.claude.com/docs/ru/plugins/mods/api.md#show-something-without-starting-a-turn) выводит уведомление с помощью `$.ui.notify`. `title` хука — это имя мода, если мод не задал его сам |

Типы `quota_auto_resume_fired`, `quota_auto_resume_stale` и `quota_auto_resume_disabled` требуют Claude Code v2.1.234 или новее. Тип `auth_storage_failure` требует v2.1.288 или новее.

В терминальных сессиях для `permission_prompt` при сетевом запросе команды в песочнице требуется Claude Code v2.1.246 или новее.

Для `agent_needs_input` при вопросе участника команды о настройке терминала требуется Claude Code v2.1.248 или новее.

> [!NOTE]
>
> Типы `permission_prompt`, `idle_prompt`, `elicitation_dialog` и `elicitation_url_dialog` используют то же время срабатывания, что и уведомления на рабочем столе, поэтому в терминальных сессиях вы видите их, только когда кажется, что вы отошли от терминала:
>
> * Ожидайте `permission_prompt`, когда вы ничего не вводили около шести секунд. Таймер запускается при появлении запроса разрешения, и каждое нажатие клавиши откладывает его. Чтобы запускать хук сразу, когда Claude запрашивает разрешение на использование инструмента, используйте вместо этого [PermissionRequest](#permissionrequest).
> * Ожидайте `idle_prompt` примерно через 60 секунд после того, как Claude закончит отвечать, и только если вы с тех пор ничего не вводили и ни один фоновый агент, например фоновый [субагент](https://code.claude.com/docs/ru/sub-agents.md), всё ещё не выполняется. Claude Code не отправляет `idle_prompt`, пока ожидает сброса лимита использования claude.ai. Когда ожидание завершается само по себе, вместо этого срабатывает один из типов `quota_auto_resume_*`.
> * Ожидайте `elicitation_dialog` для формы запроса данных или `elicitation_url_dialog` для запроса URL в браузере, когда вы ничего не вводили около шести секунд. Оба используют тот же шестисекундный порог, что и `permission_prompt`: таймер запускается при появлении диалогового окна, и каждое нажатие клавиши откладывает его.
>
> Запрос разрешения или запрос данных, поступивший, пока на экране открыто другое диалоговое окно, сохраняет тот же шестисекундный порог, отсчитываемый от момента поступления запроса. Его уведомление может дойти до вас, пока запрос ещё ожидает за открытым диалоговым окном.

Claude Code иначе определяет время срабатывания `permission_prompt` в сессиях, где он отправляет запросы разрешений в [обратный вызов `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) Agent SDK — именно так Claude Desktop и расширение VS Code размещают Claude Code:

* Ожидайте `permission_prompt` примерно через шесть секунд после того, как Claude запросит разрешение. Claude Code не откладывает его, пока вы вводите текст.
* Если вы или хук [PermissionRequest](#permissionrequest) ответите раньше, Claude Code не запускает `permission_prompt`.
* Установите [`CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`](https://code.claude.com/docs/ru/env-vars) в `1`, чтобы отключить `permission_prompt` в этих сессиях.

До v2.1.233 `permission_prompt` в этих сессиях не срабатывал.

Используйте отдельные matcher, чтобы запускать разные обработчики в зависимости от типа уведомления. Эта конфигурация запускает скрипт оповещения, специфичный для разрешений, когда Claude нужно подтверждение разрешения, и другое уведомление, когда Claude бездействует:

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Входные данные Notification

Помимо [общих полей входных данных](#common-input-fields), хуки Notification получают `message` с текстом уведомления, необязательный `title` и `notification_type`, указывающий, какой тип сработал.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission",
  "notification_type": "permission_prompt"
}
```

Хуки Notification не могут блокировать или изменять уведомления. Claude Code отбрасывает их поля `systemMessage` и `continue`, но по-прежнему выводит [`terminalSequence`](#emit-terminal-notifications), на что и опирается пример уведомления на рабочем столе. Хуки Notification предназначены для побочных эффектов, например пересылки уведомления во внешний сервис.

### SubagentStart

Запускается, когда Claude порождает субагента с помощью инструмента Agent, когда Claude [возобновляет субагента](https://code.claude.com/docs/ru/sub-agents.md#resume-subagents), а также каждый раз, когда внутрипроцессный участник [команды агентов](https://code.claude.com/docs/ru/agent-teams.md) обрабатывает новое сообщение. Поддерживает matcher для фильтрации по имени типа агента. Для встроенных агентов это имя агента, например `general-purpose`, `Explore` или `Plan`. Для [пользовательских субагентов](https://code.claude.com/docs/ru/sub-agents.md) это поле `name` из frontmatter агента, а не имя файла.

Для субагентов, поставляемых [плагином](https://code.claude.com/docs/ru/plugins/overview.md), тип агента — это идентификатор в области плагина, например `my-plugin:reviewer`, а не просто имя из frontmatter. Двоеточие переводит имя в области плагина на путь регулярных выражений, поэтому для точного совпадения привяжите matcher с помощью `^` и `$`: `^my-plugin:reviewer$`.

#### Входные данные SubagentStart

Помимо [общих полей входных данных](#common-input-fields), хуки SubagentStart получают `agent_id` с уникальным идентификатором субагента и `agent_type` с именем агента, по которому фильтрует matcher.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Хуки SubagentStart не могут блокировать создание субагента, но могут внедрять контекст в субагента. Помимо [полей вывода JSON](#json-output), доступных всем хукам, вы можете вернуть:

| Поле | Описание |
| :- | :- |
| `additionalContext` | Строка, добавляемая в контекст субагента в начале его диалога, перед его первым промптом. См. [Добавление контекста для Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

Когда хук снова запускается для того же субагента, Claude Code внедряет возвращённый контекст, только если контекст субагента ещё не содержит копию из предыдущего запуска. Копия, внедрённая при запуске, остаётся на месте, сохраняя [кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md#subagents-and-the-cache) субагента нетронутым. После того как [автосжатие](https://code.claude.com/docs/ru/sub-agents.md#auto-compaction) отбросит эту копию, Claude Code снова внедряет контекст следующего запуска.

### SubagentStop

Запускается, когда субагент Claude Code закончил отвечать. Сопоставляется по типу агента, с теми же значениями, что и SubagentStart.

#### Входные данные SubagentStop

Помимо [общих полей входных данных](#common-input-fields), хуки SubagentStop получают `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` и `last_assistant_message`. Поле `agent_type` — это значение, используемое для фильтрации через matcher. `transcript_path` — это транскрипт основной сессии, а `agent_transcript_path` — собственный транскрипт субагента, хранящийся во вложенной папке `subagents/`. Поле `last_assistant_message` содержит текстовое содержимое финального ответа субагента, поэтому хуки могут получить к нему доступ без разбора файла транскрипта.

Не каждое событие SubagentStop исходит от субагента, порождённого Claude. Claude Code также запускает внутренних агентов для некоторых своих функций, таких как [предложения промптов](https://code.claude.com/docs/ru/interactive-mode.md#prompt-suggestions) и [побочные вопросы `/btw`](https://code.claude.com/docs/ru/interactive-mode#side-questions-with-%2Fbtw), и SubagentStop срабатывает и тогда, когда один из них завершается. Для таких событий `agent_type` — это имя агента, под которым выполняется сама сессия, например заданное с помощью [`--agent`](https://code.claude.com/docs/ru/cli-reference#cli-flags) или [настройки `agent`](https://code.claude.com/docs/ru/settings-reference#agent), и пустая строка, когда сессия выполняется без него.

`matcher`, в котором указаны типы агентов, не совпадает с пустым `agent_type`. Хук, у которого matcher опущен, равен `""` или `"*"` либо является регулярным выражением, совпадающим с пустой строкой, запускается и для событий с пустым `agent_type`.

В Claude Code v2.1.271 или новее субагент, работающий с инструментом [`SubagentHandback`](https://code.claude.com/docs/ru/tools-reference), передаёт свой отчёт через этот инструмент перед остановкой. Тогда поле `last_assistant_message` содержит заключительный текст субагента, если он есть, который не является переданным отчётом. Отчёт — это входной параметр `message` того вызова, который хук `PreToolUse` или `PostToolUse` с matcher на `SubagentHandback` получает как `tool_input.message`.

Хуки SubagentStop также получают массивы `background_tasks` и `session_crons`, описанные в разделе [Входные данные Stop](#stop-input). Оба массива относятся к родительской сессии, а не к субагенту.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues...",
  "background_tasks": [],
  "session_crons": []
}
```

Хуки SubagentStop используют тот же формат управления решениями, что и [хуки Stop](#stop-decision-control), включая `hookSpecificOutput.additionalContext` с `hookEventName`, установленным в `"SubagentStop"`, для обратной связи, не являющейся ошибкой, которая продолжает работу субагента. Возврат `decision: "block"` с `reason` продолжает работу субагента и передаёт `reason` субагенту как его следующую инструкцию. Хук, блокирующий с кодом выхода 2, передаёт своё сообщение из stderr тем же способом. Чтобы внедрить контекст в родительскую сессию после возврата субагента, используйте вместо этого хук [`PostToolUse`](#posttooluse) на инструменте `Agent`.

### TaskCreated

Запускается, когда задача создаётся с помощью инструмента `TaskCreate`. Используйте это для соблюдения соглашений об именовании, требования описаний задач или предотвращения создания определённых задач. В [сессии без инструментов Task](https://code.claude.com/docs/ru/tools-reference.md#task-tool-availability) это событие не срабатывает.

Хуки TaskCreated не поддерживают matcher и срабатывают при каждом возникновении события.

#### Входные данные TaskCreated

Помимо [общих полей входных данных](#common-input-fields), хуки TaskCreated получают `task_id`, `task_subject` и, при наличии, `task_description`, `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| Поле | Описание |
| :- | :- |
| `task_id` | Идентификатор создаваемой задачи |
| `task_subject` | Заголовок задачи |
| `task_description` | Подробное описание задачи. Может отсутствовать |
| `teammate_name` | Имя участника команды, создающего задачу. Может отсутствовать |
| `team_name` | Устаревшее. Имя команды, производное от сессии; будет удалено в будущем выпуске |
| `agent_id` | Для этого события [общее поле входных данных](#common-input-fields) идентифицирует субагента или [внутрипроцессного участника команды](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), создающего задачу. Может отсутствовать. Требуется Claude Code v2.1.290 или новее |

#### Управление решениями TaskCreated

Хук TaskCreated может заблокировать создание с помощью кода выхода 2 или решения в JSON. В любом случае Claude Code удаляет задачу и возвращает ваше сообщение Claude как ошибку инструмента. Claude Code игнорирует `continue: false` от этого события, и Claude продолжает работу.

* **Код выхода 2**: Claude Code возвращает текст из stderr в качестве сообщения.
* **JSON `{"decision": "block", "reason": "..."}`**: Claude Code возвращает `reason` в качестве сообщения.

Этот пример блокирует задачи, заголовки которых не соответствуют требуемому формату:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Запускается, когда задача помечается как завершённая. Это происходит в двух ситуациях: когда любой агент явно помечает задачу как завершённую через инструмент TaskUpdate или когда участник [команды агентов](https://code.claude.com/docs/ru/agent-teams.md) заканчивает свой ход с задачами в процессе выполнения. Используйте это для соблюдения критериев завершения, таких как прохождение тестов или проверок линтера, прежде чем задачу можно будет закрыть.

Хуки TaskCompleted не поддерживают matcher и срабатывают при каждом возникновении события.

#### Входные данные TaskCompleted

Помимо [общих полей входных данных](#common-input-fields), хуки TaskCompleted получают `task_id`, `task_subject` и, при наличии, `task_description`, `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| Поле | Описание |
| :- | :- |
| `task_id` | Идентификатор завершаемой задачи |
| `task_subject` | Заголовок задачи |
| `task_description` | Подробное описание задачи. Может отсутствовать |
| `teammate_name` | Имя участника команды, завершающего задачу. Может отсутствовать |
| `team_name` | Устаревшее. Имя команды, производное от сессии; будет удалено в будущем выпуске |
| `agent_id` | Для этого события [общее поле входных данных](#common-input-fields) идентифицирует субагента или [внутрипроцессного участника команды](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), завершающего задачу. Может отсутствовать. Требуется Claude Code v2.1.290 или новее |

#### Управление решениями TaskCompleted

С помощью хука TaskCompleted вы можете оставить задачу открытой или позволить участнику команды перейти в режим ожидания:

* **Код выхода 2**: задача не помечается как завершённая, а сообщение из stderr передаётся модели в качестве обратной связи.
* **JSON `{"decision": "block", "reason": "..."}`**: задача остаётся открытой. Claude получает `reason` и продолжает работу.
* **JSON `{"continue": false, "stopReason": "..."}`**: в конце хода участника команды он переходит в режим ожидания с задачей, всё ещё находящейся в процессе выполнения, даже если другой ваш хук TaskCompleted блокирует. `stopReason` появляется в транскрипте участника команды. При вызове `TaskUpdate` Claude Code игнорирует `continue: false`.

Этот пример запускает тесты и блокирует завершение задачи, если они не проходят:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

Запускается, когда основной агент Claude Code закончил отвечать. Не запускается, если
остановка произошла из-за прерывания пользователем. Ошибки API вместо этого вызывают
[StopFailure](#stopfailure).

> [!TIP]
>
> Команда [`/goal`](https://code.claude.com/docs/ru/goal) — это встроенный быстрый способ создать хук Stop на основе промпта в рамках сессии. Используйте её, когда хотите, чтобы Claude продолжал работать до достижения условия, не создавая конфигурацию хука.

#### Входные данные Stop

Помимо [общих полей входных данных](#common-input-fields), хуки Stop получают `stop_hook_active`, `last_assistant_message`, `background_tasks` и `session_crons`. Поле `stop_hook_active` равно `true`, когда Claude Code уже продолжает работу в результате хука остановки. Проверяйте это значение или обрабатывайте транскрипт, чтобы избежать блокировки по условию, которое никогда не выполнится.

Claude Code применяет ограничение в 8 последовательных продолжений: после того как хуки остановки продолжили ход восемь раз подряд, Claude Code переопределяет следующую блокировку и завершает ход. Счётчик последовательных продолжений сбрасывается каждый раз, когда Claude вызывает инструмент. Чтобы повысить ограничение, установите [`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](https://code.claude.com/docs/ru/env-vars).

Поле `last_assistant_message` содержит текстовое содержимое финального ответа Claude, поэтому хуки могут получить к нему доступ без разбора файла транскрипта. Для хуков, которые работают с только что завершённым ходом, например хуков чтения вслух или уведомлений, используйте это поле, а не чтение `transcript_path`: не во всех версиях гарантируется, что файл транскрипта содержит финальное сообщение в момент Stop.

Массивы `background_tasks` и `session_crons` позволяют хукам отличать «сессия завершена» от «сессия приостановлена в ожидании фоновой работы, которая её разбудит». Оба массива присутствуют, когда реестр задач доступен, и пусты, когда ничего не выполняется и не запланировано.

Каждая запись в `background_tasks` описывает одну выполняющуюся задачу и использует следующие поля:

| Поле | Описание |
| :- | :- |
| `id` | Идентификатор задачи |
| `type` | Понятная метка типа задачи, например `shell`, `subagent`, `monitor`, `workflow`, `teammate`, `cloud session` или `MCP task`. Каждая метка указывает, какая функция Claude Code создала задачу. Для нераспознанных типов используется необработанный дискриминант |
| `status` | Текущий статус задачи |
| `description` | Текстовое описание, ограниченное 1000 символами, с маркером `… [+N chars]` внутри строки при обрезке |
| `command` | Командная строка оболочки, ограниченная 1000 символами. Присутствует только для задач `shell` |
| `agent_type` | Имя типа субагента. Присутствует только для задач `subagent` |
| `server` | Имя MCP-сервера. Присутствует только для задач `monitor` и `MCP task` |
| `tool` | Имя инструмента MCP. Присутствует только для задач `monitor` и `MCP task` |
| `name` | Имя workflow. Присутствует только для задач `workflow` |

Каждая запись в `session_crons` описывает одно запланированное пробуждение в рамках сессии, созданное через `CronCreate`, `ScheduleWakeup` и `/loop`:

| Поле | Описание |
| :- | :- |
| `id` | Идентификатор задачи cron |
| `schedule` | Выражение cron, например `0 9 * * 1-5` |
| `recurring` | `false` для одноразовых пробуждений, расписание которых кодирует единственное время срабатывания, `true` для задач, повторно срабатывающих при каждом совпадении |
| `prompt` | Промпт, отправляемый при срабатывании cron, ограниченный 1000 символами с тем же маркером `… [+N chars]` |

Этот пример показывает входные данные Stop с одной выполняющейся задачей оболочки и одним повторяющимся cron:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary...",
  "background_tasks": [
    {
      "id": "task-001",
      "type": "shell",
      "status": "running",
      "description": "tail logs",
      "command": "tail -f /var/log/syslog"
    }
  ],
  "session_crons": [
    {
      "id": "cron-001",
      "schedule": "0 9 * * 1-5",
      "recurring": true,
      "prompt": "check the build"
    }
  ]
}
```

#### Управление решениями Stop

Хуки `Stop` и `SubagentStop` могут управлять тем, продолжит ли Claude работу. Помимо [полей вывода JSON](#json-output), доступных всем хукам, ваш скрипт хука может вернуть следующие поля, специфичные для события:

| Поле | Описание |
| :- | :- |
| `decision` | `"block"` не даёт Claude остановиться. Опустите, чтобы позволить Claude остановиться |
| `reason` | Обязательно, когда `decision` равно `"block"`. Сообщает Claude, почему он должен продолжить |
| `hookSpecificOutput.additionalContext` | Обратная связь для Claude, не являющаяся ошибкой. Диалог продолжается, чтобы Claude мог на неё отреагировать, но, в отличие от `decision: "block"`, она показывается в транскрипте как обратная связь хука, а не как ошибка хука |

Хук, блокирующий с кодом выхода 2, обрабатывается так же, как `reason`: Claude получает сообщение из stderr в качестве объяснения, почему он должен продолжить.

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

Используйте `additionalContext`, когда хук работает так, как задумано, и даёт Claude указания, например «запусти набор тестов перед завершением». Он продолжает диалог с теми же защитами от зацикливания, что и `decision: "block"`, а именно входным полем `stop_hook_active` и ограничением в 8 последовательных продолжений, но транскрипт помечает его как `Stop hook feedback`, и уведомление об ошибке хука не показывается:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Please run the test suite before finishing"
  }
}
```

### StopFailure

Запускается вместо [Stop](#stop), когда ход завершается из-за ошибки API. Claude Code игнорирует вывод и код выхода хука, за исключением [`terminalSequence`](#emit-terminal-notifications). Используйте это для логирования сбоев, отправки оповещений или выполнения действий по восстановлению, когда Claude не может завершить ответ из-за ограничений частоты запросов, проблем с аутентификацией или других ошибок API.

#### Входные данные StopFailure

Помимо [общих полей входных данных](#common-input-fields), хуки StopFailure получают `error`, необязательное `error_details` и необязательное `last_assistant_message`. Поле `error` определяет тип ошибки и используется для фильтрации через matcher.

| Поле | Описание |
| :- | :- |
| `error` | Тип ошибки: `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `account_on_hold`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `cloud_credential_error` или `unknown`. Для ответа HTTP `529` о перегрузке значение равно `server_error` |
| `error_details` | Дополнительные сведения об ошибке, если доступны |
| `last_assistant_message` | Отображаемый текст ошибки, показанный в диалоге. В отличие от `Stop` и `SubagentStop`, где это поле содержит разговорный вывод Claude, для `StopFailure` оно содержит саму строку ошибки API, например `"API Error: Rate limit reached"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

У хуков StopFailure нет управления решениями. Они выполняются только для уведомлений и логирования.

### TeammateIdle

Запускается, когда участник [команды агентов](https://code.claude.com/docs/ru/agent-teams.md) собирается перейти в режим простоя после завершения своего хода. Используйте это для применения контрольных проверок качества до того, как участник команды прекратит работу, например для требования прохождения проверок линтера или проверки наличия выходных файлов.

Хуки TeammateIdle не поддерживают matcher и срабатывают при каждом возникновении события.

#### Входные данные TeammateIdle

Помимо [общих полей входных данных](#common-input-fields), хуки TeammateIdle получают `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "session-a1b2c3d4"
}
```

| Поле | Описание |
| :- | :- |
| `teammate_name` | Имя участника команды, который собирается перейти в режим простоя |
| `team_name` | Устаревшее. Имя команды, производное от сессии; будет удалено в будущем выпуске |
| `agent_id` | Для этого события [общее поле входных данных](#common-input-fields) идентифицирует [внутрипроцессного участника команды](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), который собирается перейти в режим простоя. Может отсутствовать. Требуется Claude Code v2.1.290 или новее |

#### Управление решениями TeammateIdle

С помощью хука TeammateIdle вы можете заставить участника команды продолжать работу или позволить ему перейти в режим ожидания:

* **Код выхода 2**: участник команды получает сообщение из stderr в качестве обратной связи и продолжает работу.
* **JSON `{"decision": "block", "reason": "..."}`**: участник команды получает `reason` и продолжает работу.
* **JSON `{"continue": false, "stopReason": "..."}`**: участник команды [переходит в режим ожидания](https://code.claude.com/docs/ru/agent-teams.md#start-your-first-agent-team), даже если другой ваш хук TeammateIdle блокирует. `stopReason` появляется в транскрипте участника команды.

Этот пример проверяет наличие артефакта сборки, прежде чем позволить участнику команды перейти в режим простоя:

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

Запускается, когда файл конфигурации изменяется во время сессии. Используйте это для аудита изменений настроек, применения политик безопасности или блокировки несанкционированных изменений файлов конфигурации.

Claude Code запускает хуки ConfigChange, когда изменяется файл настроек, файл управляемой политики или файл скилла. Для управляемой политики он запускает их, только когда изменяется `managed-settings.json` или файл в `managed-settings.d/`.

Matcher фильтрует по источнику конфигурации:

| Matcher | Когда срабатывает |
| :- | :- |
| `user_settings` | Изменяется `~/.claude/settings.json` |
| `project_settings` | Изменяется `.claude/settings.json` |
| `local_settings` | Изменяется `.claude/settings.local.json` |
| `policy_settings` | Изменяется `managed-settings.json` или файл в `managed-settings.d/` |
| `skills` | Изменяется файл скилла в `.claude/skills/` |

Изменения, подобные перечисленным ниже, вступают в силу без запуска хуков:

* Правила и настройки, которые вы сохраняете через **Yes, and don't ask again**, `/permissions` или `/model`, в той сессии, из которой вы их сохранили. Если другая открытая сессия загружает тот же файл, хуки запускаются в ней.
* Обновления [настроек, управляемых сервером](https://code.claude.com/docs/ru/server-managed-settings.md), управляемых настроек macOS или политик реестра Windows
* В WSL с [`wslInheritsWindowsSettings`](https://code.claude.com/docs/ru/settings-reference#wslinheritswindowssettings) — изменённый файл управляемых настроек на стороне Windows, который Claude Code подхватывает при опросе политик

В этом примере изменения конфигурации записываются в журнал для аудита безопасности:

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/audit-config-change.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

#### Входные данные ConfigChange

Помимо [общих полей входных данных](#common-input-fields), хуки ConfigChange получают `source` и, при наличии, `file_path`. Поле `source` указывает, какой тип конфигурации изменился, а `file_path` содержит путь к конкретному изменённому файлу.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### Управление решениями ConfigChange

Хуки ConfigChange могут блокировать вступление изменений конфигурации в силу. Используйте код выхода 2 или JSON-поле `decision`, чтобы предотвратить изменение. При блокировке новые настройки не применяются к работающей сессии.

| Поле | Описание |
| :- | :- |
| `decision` | `"block"` предотвращает применение изменения конфигурации. Опустите, чтобы разрешить изменение |
| `reason` | Принимается, но никогда не показывается |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Изменения `policy_settings` нельзя заблокировать. Хуки по-прежнему срабатывают для источников `policy_settings`, когда изменяется файл управляемых настроек на машине, поэтому вы можете использовать их для записи этих правок в лог, но любое решение о блокировке игнорируется. Это гарантирует, что корпоративные управляемые настройки всегда вступают в силу. Claude Code не запускает хуки `ConfigChange`, когда [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md), поступают или обновляются.

Claude Code выполняет решение о блокировке из JSON-вывода хука ConfigChange и отбрасывает `systemMessage` и `continue`. Заблокированное изменение не выводит никакого сообщения ни вам, ни Claude, независимо от того, блокируете ли вы его с помощью `reason` или через stderr с кодом выхода 2. Claude Code лишь записывает строку в отладочный лог.

### CwdChanged

Запускается, когда shell-команда в основном диалоге изменяет рабочий каталог, например когда Claude выполняет команду `cd`. Используйте это для реакции на смену каталога: перезагрузки переменных окружения, активации специфичных для проекта наборов инструментов или автоматического запуска скриптов настройки. Работает в паре с [FileChanged](#filechanged) для таких инструментов, как [direnv](https://direnv.net/), которые управляют окружением для каждого каталога.

Хуки CwdChanged имеют доступ к [`CLAUDE_ENV_FILE`](#persist-environment-variables). Если ваш хук записывает переменные в этот файл, они сохраняются в последующих командах Bash до следующего события CwdChanged, когда Claude Code их очищает.

CwdChanged не поддерживает matcher и срабатывает при каждом возникновении события.

#### Входные данные CwdChanged

Помимо [общих полей входных данных](#common-input-fields), хуки CwdChanged получают `old_cwd` и `new_cwd`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### Вывод CwdChanged

Помимо [полей вывода JSON](#json-output), доступных всем хукам, хуки CwdChanged могут вернуть `watchPaths`, чтобы динамически задать, за какими путями к файлам следит [FileChanged](#filechanged):

| Поле | Описание |
| :- | :- |
| `watchPaths` | Массив абсолютных путей. Заменяет текущий динамический список отслеживания. Пути из вашей конфигурации `matcher` отслеживаются всегда. Возврат пустого массива очищает динамический список, что типично при входе в новый каталог |

У хуков CwdChanged нет управления решениями. Они не могут заблокировать смену каталога.

Claude Code читает `watchPaths` и `systemMessage` из их JSON-вывода и отбрасывает `continue`. В интерактивных сессиях он показывает `systemMessage` как короткое уведомление в терминале. Сообщение не попадает в поток сообщений SDK.

### DirectoryAdded

Запускается после того, как вы добавляете рабочий каталог посреди сессии с помощью команды `/add-dir`, или после того, как SDK-клиент добавляет его с помощью управляющего запроса `register_repo_root`. Используйте это для подготовки только что добавленного репозитория, например для установки его зависимостей.

Claude Code не вызывает это событие, когда:

* Вы передаёте каталог с флагом запуска `--add-dir`; эти каталоги охватывает [SessionStart](#sessionstart)
* Вы добавляете каталог на вкладке Workspace в `/permissions`
* Вы добавляете каталог, который уже является рабочим каталогом или находится внутри него

Claude Code вызывает DirectoryAdded после обновления состояния песочницы и разрешений, поэтому инструменты в песочнице уже видят новый каталог, когда запускается ваш хук. Сами команды хуков выполняются вне песочницы.

Claude Code не ждёт хук: добавление завершается немедленно, а хук выполняется в фоне с таймаутом по умолчанию 600 секунд.

Matcher фильтрует по способу добавления каталога:

| Matcher | Когда срабатывает |
| :- | :- |
| `slash_command` | Вы добавляете каталог с помощью `/add-dir` |
| `register_repo_root` | SDK-клиент добавляет каталог с помощью управляющего запроса `register_repo_root` |

#### Входные данные DirectoryAdded

Помимо [общих полей входных данных](#common-input-fields), хуки DirectoryAdded получают `directory` и `source`.

| Поле | Описание |
| :- | :- |
| `directory` | Абсолютный путь к добавленному каталогу |
| `source` | Способ добавления каталога: `"slash_command"` для `/add-dir` или `"register_repo_root"` для управляющего запроса SDK |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "DirectoryAdded",
  "directory": "/Users/my-other-repo",
  "source": "slash_command"
}
```

У хуков DirectoryAdded нет управления решениями. Они не могут заблокировать добавление, которое уже завершено к моменту запуска хука. Claude Code отбрасывает поле `continue` из их JSON-вывода, а остальное обрабатывает по-разному в зависимости от источника:

* `slash_command`: Claude Code передаёт `systemMessage` хука Claude как контекст на следующем ходе диалога, а не показывает его вам. В транскрипте появляется количество хуков, завершившихся с ошибкой. Полный вывод ошибок записывается в отладочный лог
* `register_repo_root`: Claude Code записывает вывод `systemMessage` и вывод ошибок только в отладочный лог

### FileChanged

Запускается, когда отслеживаемый файл изменяется на диске. Claude Code обнаруживает изменения с помощью наблюдателя файловой системы, а не путём анализа вызовов инструментов, поэтому запускает хук независимо от того, что изменило файл: вызов инструмента `Edit` или `Write`, скрипт, который Claude запускает через `Bash`, или процесс полностью вне Claude Code. Типичный сценарий использования — перезагрузка переменных окружения при изменении файлов конфигурации проекта.

`matcher` для этого события выполняет две роли:

* **Формирование списка отслеживания**: значение разбивается по `|`, и каждый сегмент регистрируется как буквальное имя файла в рабочем каталоге, поэтому `".envrc|.env"` отслеживает ровно эти два файла. Регулярные выражения здесь бесполезны: значение вроде `^\.env` будет отслеживать файл с буквальным именем `^\.env`.
* **Фильтрация запускаемых хуков**: когда отслеживаемый файл изменяется, то же значение фильтрует, какие группы хуков запускаются, по стандартным [правилам matcher](#matcher-patterns) применительно к базовому имени изменённого файла.

Этот пример нормализует окончания строк в `data.csv` после любого изменения, включая перезапись файла командой `Bash` или внешним скриптом:

```json theme={null}
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": "data.csv",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/normalize-line-endings.sh"
          }
        ]
      }
    ]
  }
}
```

Хук считывает абсолютный путь изменённого файла из поля `file_path` [входных данных JSON](#filechanged-input) на stdin. Его проверка `grep` ищет то же, что удаляет `perl`, — символ CR в конце строки, поэтому запуск после нормализации завершается, не затрагивая файл. Более мягкая проверка приводит к бесконечному циклу, потому что `perl -i` перезаписывает файл, даже если ничего не заменяет, а Claude Code запускает хук снова после каждой перезаписи. Сохраните этот скрипт по пути `/path/to/normalize-line-endings.sh` и сделайте его исполняемым:

```bash theme={null}
#!/bin/bash
FILE=$(jq -r .file_path)
if grep -q $'\r$' "$FILE"; then
  perl -pi -e 's/\r$//' "$FILE"
fi
```

Чтобы убедиться, что хук работает, попросите Claude добавить строку с CRLF в `data.csv` командой `Bash`. Claude Code запустит хук, и в файле останутся окончания LF.

Чтобы отслеживать файлы, имена которых нельзя указать заранее, возвращайте [`watchPaths`](#filechanged-output) из хука для динамического обновления списка отслеживания. Claude Code запускает наблюдатель только тогда, когда что-то указывает файл для отслеживания, поэтому заполните список группой FileChanged, matcher которой называет хотя бы один файл, или хуком [SessionStart](#sessionstart-decision-control) или [CwdChanged](#cwdchanged), возвращающим `watchPaths`. Matcher по-прежнему фильтрует, какие группы хуков запускаются при изменении отслеживаемого файла, поэтому для группы, обрабатывающей динамические пути, не указывайте matcher: тогда он соответствует каждому отслеживаемому файлу и ничего не добавляет в список отслеживания. Matcher `"*"` тоже соответствует каждому файлу, но Claude Code регистрирует его в списке отслеживания как любое другое значение — как файл с буквальным именем `*`.

Хуки FileChanged имеют доступ к [`CLAUDE_ENV_FILE`](#persist-environment-variables). Переменные, записанные в этот файл, сохраняются для последующих команд Bash до следующего события [CwdChanged](#cwdchanged), когда Claude Code их очищает.

#### Входные данные FileChanged

Помимо [общих входных полей](#common-input-fields), хуки FileChanged получают `file_path` и `event`.

| Поле | Описание |
| :- | :- |
| `file_path` | Абсолютный путь к изменённому файлу |
| `event` | Что произошло: `"change"` для изменённого файла, `"add"` для созданного файла или `"unlink"` для удалённого файла |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### Выходные данные FileChanged

Помимо [полей вывода JSON](#json-output), доступных всем хукам, хуки FileChanged могут возвращать `watchPaths` для динамического обновления отслеживаемых путей файлов:

| Поле | Описание |
| :- | :- |
| `watchPaths` | Массив абсолютных путей. Заменяет текущий динамический список отслеживания. Пути из конфигурации `matcher` отслеживаются всегда. Используйте это, когда скрипт хука обнаруживает дополнительные файлы для отслеживания на основе изменённого файла |

Хуки FileChanged не управляют решениями. Они не могут предотвратить изменение файла.

Claude Code считывает `watchPaths` и `systemMessage` из их вывода JSON и отбрасывает `continue`. В интерактивных сессиях `systemMessage` показывается как краткое уведомление в терминале. Сообщение не попадает в поток сообщений SDK.

### WorktreeCreate

Запускается, когда Claude Code создаёт worktree, например в таких случаях:

* Вы запускаете сессию командой `claude --worktree`
* Claude создаёт worktree во время сессии и переключается в него с помощью инструмента [`EnterWorktree`](https://code.claude.com/docs/ru/tools-reference)
* [Субагент использует `isolation: "worktree"`](https://code.claude.com/docs/ru/sub-agents#choose-the-subagent-scope)
* [Рабочий процесс](https://code.claude.com/docs/ru/workflows.md#migrate-many-files-in-parallel) запускает агента в собственном worktree
* Claude Code изолирует [фоновую сессию](https://code.claude.com/docs/ru/agent-view.md#how-file-edits-are-isolated) в собственном worktree
* [`claude remote-control`](https://code.claude.com/docs/ru/remote-control#start-a-remote-control-session) в режиме `worktree` запускает сессию в собственном worktree

Хук WorktreeCreate не запускается для worktree, который Claude добавляет через Bash, а хук плагина не запускается для worktree, создаваемого при запуске с `--worktree` и [`--tmux`](https://code.claude.com/docs/ru/cli-reference#cli-flags):

* **`git worktree add` через Bash**: чтобы проверить или заблокировать эту команду, добавьте хук [`PreToolUse`](#pretooluse) с matcher `Bash`.
* **`--worktree` с `--tmux`**: Claude Code создаёт worktree до загрузки плагинов, поэтому хук WorktreeCreate из плагина не запускается. Чтобы ваш хук запускался с обоими флагами, определите его в [файле настроек](#configuration). До v2.1.300 хук WorktreeCreate плагина не запускался и с одним только `--worktree`.

По умолчанию Claude Code создаёт изолированную рабочую копию с помощью `git worktree`. Настройка хука WorktreeCreate заменяет это стандартное поведение git, позволяя использовать другую систему контроля версий, например SVN, Perforce или Mercurial.

Поскольку хук полностью заменяет стандартное поведение, [`.worktreeinclude`](https://code.claude.com/docs/ru/worktrees#copy-gitignored-files-into-worktrees) не обрабатывается. Если нужно скопировать локальные файлы конфигурации, такие как `.env`, в новый worktree, делайте это в скрипте хука.

Хук должен вернуть путь к созданному каталогу worktree. Claude Code использует этот путь как рабочий каталог для изолированной сессии. О том, как каждый тип хука возвращает путь, см. [Выходные данные WorktreeCreate](#worktreecreate-output).

Claude Code учитывает успешность хука и возвращённый путь и отбрасывает `systemMessage` и `continue`.

Этот пример создаёт рабочую копию SVN и выводит путь для использования в Claude Code. Замените URL репозитория своим:

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Хук считывает `name` worktree из входных данных JSON на stdin, извлекает свежую копию в новый каталог и выводит путь к каталогу. `echo` в последней строке — это то, что Claude Code считывает как путь к worktree. Перенаправляйте любой другой вывод в stderr, чтобы он не мешал пути.

#### Входные данные WorktreeCreate

Помимо [общих входных полей](#common-input-fields), хуки WorktreeCreate получают поле `name`. Это slug-идентификатор нового worktree, заданный пользователем или сгенерированный автоматически, например `bold-oak-a3f2`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Выходные данные WorktreeCreate

Хуки WorktreeCreate не используют стандартную модель решений разрешения/блокировки. Вместо этого результат определяется успехом или неудачей хука. Хук должен вернуть путь к созданному каталогу worktree:

* **Хуки команд** (`type: "command"`): выведите путь последней непустой строкой stdout. Claude Code удаляет escape-коды ANSI перед чтением этой строки, поэтому баннеры запуска оболочки, выведенные до вашего `echo`, игнорируются. Перенаправляйте любой другой вывод хука в stderr.
* **HTTP-хуки** (`type: "http"`): верните `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` в теле ответа.

Если хук завершается неудачей или не выдаёт путь, создание worktree завершается с ошибкой. Claude Code разрешает относительный путь относительно каталога, в котором выполнялся хук, сворачивая в нём любые сегменты `.` или `..`. Если полученный путь не является каталогом, в который Claude Code может перейти, сессия выводит ошибку с указанием пути и завершается с кодом 1.

Claude Code отклоняет абсолютный путь, содержащий сегменты `.` или `..`, а также любой путь, проходящий через символическую ссылку ниже корня репозитория. В ошибке указывается отклонённый компонент. Символическая ссылка, закоммиченная в репозиторий, могла бы перенаправить worktree за его пределы. Возвращайте нормализованный путь, не проходящий через символическую ссылку внутри репозитория.

### WorktreeRemove

Запускается, когда Claude Code очищает worktree, созданный вашим хуком [`WorktreeCreate`](#worktreecreate). Событие срабатывает, когда:

* Вы выходите из интерактивной [сессии worktree](https://code.claude.com/docs/ru/worktrees.md#start-claude-in-a-worktree) и выбираете удаление worktree в ответ на запрос Claude Code
* Вы выходите из интерактивной сессии worktree, которой не [дали имя](https://code.claude.com/docs/ru/sessions.md#name-your-sessions), Claude Code не находит изменённых или неотслеживаемых файлов и удаляет worktree без запроса
* Вы удаляете [фоновую сессию](https://code.claude.com/docs/ru/agent-view.md#what-deleting-a-session-removes), работающую в worktree
* Вы просите Claude выйти и удалить worktree во время сессии, и Claude удаляет его инструментом [`ExitWorktree`](https://code.claude.com/docs/ru/tools-reference)
* Сессия, которую [`claude remote-control`](https://code.claude.com/docs/ru/remote-control#start-a-remote-control-session) запустил в режиме `worktree`, завершается без сбоя, и Claude Code не находит в её worktree изменённых или неотслеживаемых файлов и новых коммитов
* Вы останавливаете `claude remote-control`, пока запущенные им в режиме `worktree` сессии ещё работают, и Claude Code не находит в их worktree изменённых или неотслеживаемых файлов и новых коммитов

Когда субагент или агент рабочего процесса завершает работу, Claude Code сохраняет worktree, созданный для него вашим хуком WorktreeCreate, и не запускает хук WorktreeRemove. Удаляйте такие worktree самостоятельно, когда работа завершена.

Claude Code не запрашивает подтверждение перед запуском хука для вызова `ExitWorktree` или очистки `claude remote-control`. `ExitWorktree` отказывается удалять созданный хуком worktree, если вызов не передаёт [`discard_changes: true`](https://code.claude.com/docs/ru/agent-sdk/typescript#exitworktree), что делает ваш хук последней проверкой на этом пути.

Claude Code использует git для поиска изменённых или неотслеживаемых файлов, поэтому не находит их в worktree, который не является git-checkout и не находится внутри него, даже если в каталоге есть незакоммиченная работа. Проверяйте наличие такой работы в хуке WorktreeRemove, прежде чем он что-либо удалит.

Для worktree на основе git Claude Code автоматически выполняет очистку с помощью `git worktree remove`. Если вы настроили хук WorktreeCreate, дополните его хуком WorktreeRemove, чтобы управлять очисткой:

* **Нет хука WorktreeRemove**: Claude Code использует git как резервный вариант при удалении на выходе или через `ExitWorktree` и сохраняет worktree при очистке `claude remote-control`:
  * **Вы выходите из сессии worktree или Claude вызывает `ExitWorktree`**: Claude Code удаляет путь, возвращённый хуком WorktreeCreate, так же, как это сделал бы `git worktree remove --force`, поэтому worktree, распознаваемый git, удаляется. Worktree, который git не распознаёт, например созданный хуком с системой контроля версий, отличной от git, остаётся на диске.
  * **`claude remote-control` очищает worktree сессии**: worktree остаётся на диске, а терминал, в котором работает `claude remote-control`, показывает `worktree removal failed, kept: <path>`.
  * **Вы удаляете фоновую сессию**: см. [Что удаляется при удалении сессии](https://code.claude.com/docs/ru/agent-view.md#what-deleting-a-session-removes).
* **Хук завершается с кодом 0**: worktree считается удалённым. Claude Code больше ничего не считывает из хука, поэтому убедитесь, что хук удалил каталог.
* **Хук завершается с ненулевым кодом**: удаление завершается неудачей, если каталог по пути `worktree_path` после этого всё ещё существует, и worktree остаётся на диске без резервного варианта через git. Хук, удаливший каталог перед завершением с ненулевым кодом, считается выполнившим удаление. О том, как сообщается о неудаче, см. [Входные данные WorktreeRemove](#worktreeremove-input).

Claude Code никогда не удаляет ветку, принадлежащую worktree, созданному хуком, поскольку знает только путь, возвращённый вашим хуком WorktreeCreate. Если ваш хук WorktreeCreate создаёт ветку, удаляйте её в хуке WorktreeRemove. Claude Code отбрасывает [поля вывода JSON](#json-output) хука WorktreeRemove, такие как `systemMessage` и `continue`.

При удалении фоновой сессии Claude Code проверяет сохранённый путь к worktree перед запуском хука и отклоняет путь, который является символической ссылкой или проходит через неё ниже корня репозитория. На этом пути хук запускается для worktree, в котором ещё есть файлы, только если вы подтверждаете удаление в [представлении агентов](https://code.claude.com/docs/ru/agent-view.md#what-deleting-a-session-removes). Для такого worktree [`claude rm`](https://code.claude.com/docs/ru/agent-view#manage-sessions-from-the-shell) вместо этого сохраняет сессию и worktree.

Claude Code передаёт путь, возвращённый WorktreeCreate, как `worktree_path` во входных данных хука. Этот пример считывает этот путь и удаляет каталог:

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'p=$(jq -er .worktree_path) && rm -rf -- \"$p\"'"
          }
        ]
      }
    ]
  }
}
```

#### Входные данные WorktreeRemove

Помимо [общих входных полей](#common-input-fields), хуки WorktreeRemove получают поле `worktree_path` — абсолютный путь к удаляемому worktree.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Результат определяется кодом выхода хука WorktreeRemove. Если хук завершается с ненулевым кодом, а каталог по пути `worktree_path` после этого всё ещё существует, удаление завершается неудачей:

* Если вы удаляли фоновую сессию, сессия тоже сохраняется. Сообщение об отказе в [представлении агентов](https://code.claude.com/docs/ru/agent-view.md#what-deleting-a-session-removes) сообщает, как завершился хук, например `exited 1`, цитирует начало его stderr и указывает, удалит ли повторное удаление сессии каталог в любом случае.
* Если `claude remote-control` очищал worktree сессии, терминал, в котором он работает, показывает `worktree removal failed, kept: <path>`.

### PreCompact

Запускается перед тем, как Claude Code выполнит операцию сжатия контекста.

Значение matcher указывает, было ли сжатие запущено вручную или автоматически:

| Matcher | Когда срабатывает |
| :- | :- |
| `manual` | `/compact` |
| `auto` | Автосжатие, когда диалог достигает [окна автосжатия](https://code.claude.com/docs/ru/model-config.md#set-the-auto-compact-window), и [сжатие при простое](https://code.claude.com/docs/ru/settings-reference.md#idlecompaction) |

Завершитесь с кодом 2, чтобы заблокировать сжатие. Для ручного `/compact` сообщение из stderr показывается пользователю. Также можно заблокировать сжатие, вернув JSON с `"decision": "block"`.

Блокировка автоматического сжатия имеет разные последствия в зависимости от момента срабатывания. Если сжатие было запущено заблаговременно, до достижения лимита контекста, Claude Code пропускает его, и диалог продолжается без сжатия. Если сжатие было запущено для восстановления после ошибки лимита контекста, уже возвращённой API, исходная ошибка выводится, и текущий запрос завершается неудачей.

Claude Code отбрасывает поля `systemMessage` и `continue` хука PreCompact.

#### Входные данные PreCompact

Помимо [общих входных полей](#common-input-fields), хуки PreCompact получают `trigger` и `custom_instructions`. Для `manual` поле `custom_instructions` содержит то, что пользователь передаёт в `/compact`, и равно `null`, если ничего не передано. Для `auto` поле `custom_instructions` равно `null`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": null
}
```

#### Выходные данные PreCompact

Когда хук PreCompact завершается с кодом 0 и не блокирует сжатие, Claude Code использует его stdout как инструкции для сводки сжатия. Ограничивайте этот stdout 10 000 символов на хук. Более длинный вывод Claude Code обрезает на этом пределе и добавляет маркер.

### PostCompact

Запускается после того, как Claude Code завершает операцию сжатия контекста. Используйте это событие, чтобы реагировать на новое сжатое состояние, например чтобы записать в лог сгенерированную сводку или обновить внешнее состояние. Claude Code отбрасывает поля `systemMessage` и `continue` хука PostCompact.

Применяются те же значения matcher, что и для `PreCompact`:

| Matcher | Когда срабатывает |
| :- | :- |
| `manual` | После `/compact` |
| `auto` | После автосжатия, когда диалог достигает [окна автосжатия](https://code.claude.com/docs/ru/model-config.md#set-the-auto-compact-window), и после [сжатия при простое](https://code.claude.com/docs/ru/settings-reference.md#idlecompaction) |

#### Входные данные PostCompact

Помимо [общих входных полей](#common-input-fields), хуки PostCompact получают `trigger` и `compact_summary`. Поле `compact_summary` содержит сводку диалога, сгенерированную операцией сжатия.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

Хуки PostCompact не управляют решениями. Они не могут повлиять на результат сжатия, но могут выполнять последующие задачи.

### PreModelSwitch

Запускается перед тем, как Claude Code применит переключение модели, запрошенное вами или клиентом. Используйте его, чтобы заблокировать переключение, потребовать подтверждения или показать, во что обойдётся переключение, до того как оно произойдёт.

PreModelSwitch требует Claude Code v2.1.251 или новее. Claude Code запускает его для следующих запросов:

* `/model <name>` и окно выбора `/model`
* Окно выбора модели `Option+P` или `Alt+P`
* Настройка Model в `/config`
* Включение [быстрого режима](https://code.claude.com/docs/ru/fast-mode.md), если это меняет модель сессии
* Запрос `set_model` или изменение модели в запросе `apply_flag_settings` от хоста [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md#query-object) или [Remote Control](https://code.claude.com/docs/ru/remote-control.md)

Claude Code не запускает хуки PreModelSwitch для переключений, которые он выполняет сам, например при [автоматическом переключении на резервную модель](https://code.claude.com/docs/ru/model-config.md#automatic-model-fallback) или восстановлении модели при возобновлении сессии. Такие изменения доходят только до [PostModelSwitch](#postmodelswitch).

Claude Code сравнивает matcher с каноническим именем модели, на которую переключается сессия, игнорируя суффикс `[1m]`. Псевдоним, например `opus`, идентификатор модели с датой и идентификатор конкретного провайдера, например идентификатор модели Amazon Bedrock, соответствуют одному каноническому имени, в которое они разрешаются, поэтому `claude-opus-5` охватывает все варианты написания Opus 5.

Если Claude Code не может определить каноническое имя целевой модели, например для пользовательского идентификатора модели, известного только вашему [LLM-шлюзу](https://code.claude.com/docs/ru/llm-gateway), он запускает каждый хук PreModelSwitch независимо от matcher. Поэтому блокирующий хук должен проверять `to_model` из входных данных, а не полагаться только на matcher.

Записывайте matcher как точное имя, список через `|`, например `claude-opus-4-6|claude-opus-5`, или регулярное выражение, например `.*opus.*`. Этот пример использует matcher с точным именем и дополнительно проверяет `to_model` из входных данных хука, поэтому он отклоняет переключение на Opus 4.6, завершаясь с кодом 2, и пропускает любую другую целевую модель:

> [tab] macOS/Linux
>
> Команда проверяет `to_model` с помощью `jq`:
>
> ```json theme={null}
> {
>   "hooks": {
>     "PreModelSwitch": [
>       {
>         "matcher": "claude-opus-4-6",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "jq -e '.to_model | test(\"opus-4-6\")' > /dev/null && { echo 'Opus 4.6 is retired for this project. Use a newer model.' >&2; exit 2; }; exit 0"
>           }
>         ]
>       }
>     ]
>   }
> }
> ```

> [tab] Windows (PowerShell)
>
> Зарегистрируйте хук команды, который запускает скрипт через PowerShell:
>
> ```json theme={null}
> {
>   "hooks": {
>     "PreModelSwitch": [
>       {
>         "matcher": "claude-opus-4-6",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "powershell.exe",
>             "args": [
>               "-NoProfile",
>               "-ExecutionPolicy",
>               "Bypass",
>               "-File",
>               "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-opus-46.ps1"
>             ]
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Сохраните этот скрипт в `.claude/hooks/block-opus-46.ps1` в вашем проекте:
>
> ```powershell theme={null}
> $hookInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
> if ($hookInput.to_model -match 'opus-4-6') {
>   [Console]::Error.WriteLine('Opus 4.6 is retired for this project. Use a newer model.')
>   exit 2
> }
> exit 0
> ```

Чтобы убедиться, что хук работает, выполните `/model claude-opus-4-6` в сессии с другой моделью. Claude Code сохранит текущую модель и сообщит, что хук PreModelSwitch заблокировал переключение, указав ваше сообщение в качестве причины.

#### Входные данные PreModelSwitch

Помимо [общих входных полей](#common-input-fields), хуки PreModelSwitch получают поля из этой таблицы. Последние пять описывают стоимость повторной отправки диалога новой модели, чтобы хук мог показать эту цифру до переключения.

| Поле | Тип | Описание |
| :- | :- | :- |
| `from_model` | string | Идентификатор модели, с которой выполняется переключение |
| `to_model` | string | Идентификатор модели, на которую выполняется переключение. Matcher сравнивается с каноническим именем этой модели |
| `requested_model` | string или `null` | Модель, указанная в запросе: псевдоним, например `opus`, полный идентификатор модели или `null`, если запрашивалась модель по умолчанию |
| `source` | string | Откуда пришёл запрос: `"command"` для `/model <name>`, настройки Model в `/config` или включения быстрого режима; `"picker"` для окна выбора модели; `"sdk"` для запроса `set_model` или изменения модели в запросе `apply_flag_settings` от хоста Agent SDK или Remote Control |
| `context_tokens` | number | Токены, которые следующий запрос отправит повторно в качестве промпта: сумма входных токенов, токенов чтения кэша, создания кэша и выходных токенов последнего ответа в основном диалоге. `0` до первого ответа |
| `prompt_cache_warm` | boolean | Вероятно ли, что кэш промптов текущей модели ещё «тёплый», то есть переключение приведёт к его потере |
| `cache_ttl` | string | [Время жизни кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime) основного диалога на момент этой смены: `"5m"` или `"1h"` |
| `estimated_cache_write_usd` | number | Оценочная стоимость в долларах США записи `context_tokens` в кэш промптов на `to_model` по тарифу `cache_ttl`, без учёта следующего ответа. Серверу может не потребоваться повторно кэшировать весь контекст, поэтому считайте это оценкой |
| `pricing` | string | Как Claude Code рассчитал `estimated_cache_write_usd`: `"configured"` — по собственным тарифам вашей организации, если она их настроила, `"catalog"` — по прейскурантной цене, или `"default"` — если цена `to_model` неизвестна и Claude Code использовал тариф по умолчанию |

Этот пример показывает входные данные для `/model opus` в сессии с Sonnet 5:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreModelSwitch",
  "from_model": "claude-sonnet-5",
  "to_model": "claude-opus-5",
  "requested_model": "opus",
  "source": "command",
  "context_tokens": 182340,
  "prompt_cache_warm": true,
  "cache_ttl": "5m",
  "estimated_cache_write_usd": 1.1396,
  "pricing": "catalog"
}
```

#### Управление решениями PreModelSwitch

Хуки `PreModelSwitch` могут отменить переключение, попросить пользователя подтвердить его или разрешить его выполнение. Код выхода 2 или `decision: "block"` на верхнем уровне отменяет переключение.

Для более тонкого управления возвращайте `permissionDecision` и `permissionDecisionReason` в объекте `hookSpecificOutput`, как в [PreToolUse](#pretooluse-decision-control). `PreModelSwitch` принимает `"allow"`, `"deny"` и `"ask"`. Он не принимает `"defer"`, `updatedInput` или `additionalContext`. В таблице ниже описаны оба поля:

| Поле | Описание |
| :- | :- |
| `permissionDecision` | `"allow"` продолжает и пропускает [подтверждение, которое Claude Code показывает, пока кэш промптов «тёплый»](https://code.claude.com/docs/ru/prompt-caching.md#switching-models). `"deny"` отменяет переключение. `"ask"` просит пользователя подтвердить его |
| `permissionDecisionReason` | Для `"deny"` показывается пользователю как причина блокировки переключения или возвращается как ошибка для запроса `set_model`. Для `"ask"` показывается в запросе подтверждения. Игнорируется для `"allow"` |

Только `/model` в интерактивной сессии может показать запрос `"ask"`. Во всех остальных интерфейсах, включая неинтерактивный режим с флагом `-p`, `/config` и запросы `set_model`, Claude Code рассматривает `"ask"` как отказ.

Этот пример просит пользователя подтвердить переключение и приводит количество токенов из `context_tokens`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreModelSwitch",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Switching now re-sends about 180k tokens to the new model. Continue?"
  }
}
```

Когда несколько хуков PreModelSwitch возвращают разные решения, приоритет такой: `deny` > `ask` > `allow`.

Claude Code показывает пользователю любое `systemMessage`, возвращённое хуком, независимо от решения, поэтому хук для отчёта о стоимости может вернуть `{"systemMessage": "..."}` и завершиться с кодом 0.

#### Таймауты PreModelSwitch и другие коды выхода

Хук PreModelSwitch, не ответивший до истечения таймаута, блокирует переключение. Таймаут по умолчанию для этого события — 30 секунд.

Код выхода, отличный от 0 или 2, без корректного вывода JSON является [неблокирующей ошибкой](#other-exit-codes), поэтому переключение выполняется, за исключением хуков, [сбой которых его блокирует](#block-the-action-when-a-hook-fails).

### PostModelSwitch

Запускается после изменения модели сессии. Используйте его, чтобы дать Claude указания для конкретной модели без редактирования каждого CLAUDE.md, например инструкцию уровня организации, применимую к определённым моделям.

PostModelSwitch требует Claude Code v2.1.251 или новее. Он не может блокировать, потому что модель уже изменилась. Claude Code запускает хуки PostModelSwitch после любого из следующих изменений:

* Переключение, запрошенное вами или клиентом
* [Автоматическое переключение на резервную модель](https://code.claude.com/docs/ru/model-config.md#automatic-model-fallback), которое меняет модель сессии
* Вход в режим планирования или выход из него при настройке, такой как [`opusplan`](https://code.claude.com/docs/ru/model-config#opusplan-model-setting)
* Восстановление модели Claude Code при возобновлении сессии

Claude Code не запускает хуки PostModelSwitch, когда ход обслуживает модель из [цепочки резервных моделей](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains), потому что такая замена длится один ход и не меняет модель сессии.

Matcher подчиняется тем же правилам, что и в [PreModelSwitch](#premodelswitch): Claude Code сравнивает его с каноническим именем модели, на которую переключилась сессия.

Этот пример добавляет указания всякий раз, когда модель сессии меняется на любую модель Opus:

```json theme={null}
{
  "hooks": {
    "PostModelSwitch": [
      {
        "matcher": ".*opus.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'On Opus, delegate implementation work to subagents and keep this conversation for planning and review.'"
          }
        ]
      }
    ]
  }
}
```

Чтобы убедиться, что хук работает, переключитесь на модель Opus в сессии с другой моделью, например выполните `/model opus` в сессии Sonnet, а затем спросите Claude, какие у него есть указания относительно текущей модели.

#### Входные данные PostModelSwitch

Хуки PostModelSwitch получают те же поля, что и [PreModelSwitch](#premodelswitch-input), при этом `hook_event_name` равно `"PostModelSwitch"`, и есть ещё два значения `source`: `"auto"` для автоматического переключения на резервную модель или другого изменения, сделанного Claude Code самостоятельно, и `"resume"` для модели, восстановленной при возобновлении сессии.

`requested_model` равно `null`, когда `source` равно `"auto"`. Когда `source` равно `"resume"`, это сохранённая настройка модели, которую восстановил Claude Code.

#### Управление решениями PostModelSwitch

Claude Code берёт [простой текст stdout](#exit-code-0) вашего хука при коде выхода 0 или `additionalContext` из вывода JSON и передаёт его Claude со следующим запросом после переключения. Помимо [полей вывода JSON](#json-output), доступных всем хукам, можно вернуть:

| Поле | Описание |
| :- | :- |
| `additionalContext` | Строка, добавляемая в контекст Claude со следующим запросом. См. [Добавление контекста для Claude](#add-context-for-claude) |

Если хук не завершился в течение пяти секунд после отправки следующего промпта, Claude Code отправляет этот запрос без вывода и прикрепляет его к следующему за ним запросу. Если модель меняется несколько раз до следующего запроса, Claude Code передаёт только вывод для целевой модели последнего переключения.

### SessionEnd

Запускается при завершении сессии Claude Code. Полезен для задач очистки, записи
статистики сессии в лог или сохранения состояния сессии. Поддерживает matcher для фильтрации по причине выхода.

Поле `reason` во входных данных хука указывает, почему сессия завершилась:

| Причина | Описание |
| :- | :- |
| `clear` | Сессия очищена командой `/clear` |
| `resume` | Сессия переключена через интерактивную `/resume` |
| `logout` | Пользователь вышел из системы |
| `prompt_input_exit` | Пользователь вышел, пока было видно поле ввода промпта |
| `other` | Другие причины выхода |
| `bypass_permissions_disabled` | Удалено в v2.1.234; Claude Code его не отправляет. Уберите его из matcher для `SessionEnd` |

#### Входные данные SessionEnd

Помимо [общих входных полей](#common-input-fields), хуки SessionEnd получают поле `reason`, указывающее, почему сессия завершилась. Все значения см. в [таблице причин](#sessionend) выше.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Хуки SessionEnd не управляют решениями. Они не могут заблокировать завершение сессии, но могут выполнять задачи очистки. Claude Code отбрасывает их [поля вывода JSON](#json-output), такие как `systemMessage`.

Таймаут по умолчанию для хуков SessionEnd — 1,5 секунды. Он действует, когда вы выходите, выполняете `/clear` или переключаете сессии через интерактивную `/resume`. Дать хуку больше времени можно двумя способами:

* **`timeout` для отдельного хука**: задайте `timeout` в конфигурации этого хука. Общий лимит времени автоматически увеличивается до наибольшего значения `timeout` отдельного хука в ваших файлах настроек, но не более 60 секунд. Если вы увеличиваете лимит таким образом, хук без собственного `timeout` по-прежнему сохраняет значение по умолчанию. Таймауты, заданные для хуков из плагинов, не увеличивают лимит.
* **`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`**: задайте эту переменную окружения в миллисекундах, чтобы явно переопределить лимит. Заданное значение также становится таймаутом для каждого хука без собственного `timeout`.

Этот пример устанавливает лимит в 5 секунд:

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

До v2.1.268 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` увеличивала только общий лимит, а хук без собственного `timeout` всё равно отменялся через 1,5 секунды.

### Elicitation

Запускается, когда MCP-сервер запрашивает ввод пользователя посреди задачи. По умолчанию Claude Code показывает интерактивное диалоговое окно для ответа пользователя. Хуки могут перехватить этот запрос и ответить программно, полностью пропуская диалоговое окно.

Полный хук с записью в настройках и скриптом см. в разделе [Ответ на запрос формы из скрипта](#answer-a-form-request-from-a-script).

Поле matcher сопоставляется с именем MCP-сервера.

#### Входные данные Elicitation

Помимо [общих входных полей](#common-input-fields), хуки Elicitation получают `mcp_server_name`, `message` и необязательные поля `mode`, `url`, `elicitation_id` и `requested_schema`.

Для elicitation в режиме формы, наиболее распространённого случая:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Для elicitation в режиме URL, используемого для аутентификации через браузер:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Выходные данные Elicitation

Хук Elicitation может ответить на запрос вместо пользователя, отклонить или отменить его либо оставить его диалоговому окну. Чтобы ответить, отклонить или отменить, завершитесь с кодом 0 и выведите объект `hookSpecificOutput` с `action`. Сервер получит ваш ответ, и диалоговое окно не появится. Каждая строка этой таблицы показывает, что вернуть для одного исхода и что получит MCP-сервер:

| Чтобы | Верните | Сервер получит |
| :- | :- | :- |
| Ответить вместо пользователя | `"action": "accept"` со значениями полей формы в `content` | `accept` с вашим `content` |
| Отклонить запрос | `"action": "decline"` | `decline` |
| Отменить запрос | `"action": "cancel"` | `cancel` |
| Оставить запрос пользователю | Без вывода, с кодом выхода 0 | Ответ пользователя из [диалогового окна](https://code.claude.com/docs/ru/mcp.md#respond-to-mcp-elicitation-requests) |

Этот вывод отвечает на запрос в режиме формы, показанный в разделе [Входные данные Elicitation](#elicitation-input). Ключи в `content` — это имена свойств из `requested_schema` этого запроса:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

Этот вывод отклоняет запрос:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "decline"
  }
}
```

Для запроса в режиме URL хук, возвращающий `accept`, пропускает диалоговое окно, поэтому URL так и не открывается.

Claude Code отбрасывает `reason`, `systemMessage` и `continue` из вывода JSON хука Elicitation, какой бы `action` вы ни вернули.

#### Другие способы отклонить elicitation

Хук также может отклонить запрос следующими способами. Сервер получит тот же `decline`, что и для `"action": "decline"`:

* **Завершение с кодом 2**: Claude Code игнорирует `hookSpecificOutput`, выведенный тем же хуком
* **Вывод `"decision": "block"` на верхнем уровне**: блокировка переопределяет `action` в том же выводе

Когда одному запросу соответствует несколько хуков, отклонение от одного из них переопределяет `accept` или `cancel` от другого.

Этот скрипт отклоняет запросы в режиме URL и оставляет запросы формы диалоговому окну:

```bash theme={null}
#!/bin/bash
if [ "$(jq -r '.mode')" = "url" ]; then
  exit 2
fi
```

Ни пользователь, ни сервер не видят, почему хук отклонил запрос, потому что Claude Code не показывает ваш stderr или ваш `reason`.

Claude Code игнорировал `decision` верхнего уровня от хуков `Elicitation` и `ElicitationResult`, начиная с v2.1.105 и до исправления в v2.1.284.

#### Ответ на запрос формы из скрипта

Этот пример отвечает на один повторяющийся вопрос вместо пользователя. MCP-сервер с именем `issue-tracker` запрашивает ключ проекта в форме, и хук подставляет `DOCS`. Скрипт принимает запрос, когда `project_key` — единственное поле формы. Для любого другого запроса он ничего не выводит, поэтому появляется диалоговое окно.

> [tab] macOS/Linux
>
> Зарегистрируйте хук команды для этого события в файле настроек, указав имя сервера в качестве matcher:
>
> ```json theme={null}
> {
>   "hooks": {
>     "Elicitation": [
>       {
>         "matcher": "issue-tracker",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/answer-project-key.sh",
>             "args": []
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Сохраните этот скрипт в `.claude/hooks/answer-project-key.sh` в вашем проекте и сделайте его исполняемым с помощью `chmod +x`:
>
> ```bash theme={null}
> #!/bin/bash
> input=$(cat)
> fields=$(jq -c '.requested_schema.properties // {} | keys' <<<"$input")
>
> if [ "$fields" = '["project_key"]' ]; then
>   jq -n '{hookSpecificOutput: {hookEventName: "Elicitation", action: "accept", content: {project_key: "DOCS"}}}'
> fi
> ```

> [tab] Windows (PowerShell)
>
> Зарегистрируйте хук команды, который запускает скрипт через PowerShell, указав имя сервера в качестве matcher:
>
> ```json theme={null}
> {
>   "hooks": {
>     "Elicitation": [
>       {
>         "matcher": "issue-tracker",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "powershell.exe",
>             "args": [
>               "-NoProfile",
>               "-ExecutionPolicy",
>               "Bypass",
>               "-File",
>               "${CLAUDE_PROJECT_DIR}/.claude/hooks/answer-project-key.ps1"
>             ]
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> Сохраните этот скрипт в `.claude/hooks/answer-project-key.ps1` в вашем проекте:
>
> ```powershell theme={null}
> $request = [Console]::In.ReadToEnd() | ConvertFrom-Json
> $fields = @($request.requested_schema.properties.PSObject.Properties.Name)
>
> if ($fields.Count -eq 1 -and $fields[0] -eq 'project_key') {
>   @{
>     hookSpecificOutput = @{
>       hookEventName = "Elicitation"
>       action = "accept"
>       content = @{ project_key = "DOCS" }
>     }
>   } | ConvertTo-Json -Depth 3
> }
> ```

Чтобы убедиться, что хук работает, запустите Claude Code с `claude --debug` и дайте Claude задачу, при которой сервер запрашивает ключ проекта. Диалоговое окно не появится, а в [отладочном логе](#debug-hooks) будет строка, содержащая `Elicitation resolved by hook:` и `accept`.

### ElicitationResult

Запускается после того, как пользователь отвечает на elicitation MCP. Хуки могут просматривать, изменять или блокировать ответ до его отправки обратно MCP-серверу.

Когда хук [Elicitation](#elicitation) отвечает на запрос, Claude Code отправляет этот ответ серверу, не запуская хуки ElicitationResult.

Поле matcher сопоставляется с именем MCP-сервера.

#### Входные данные ElicitationResult

Помимо [общих входных полей](#common-input-fields), хуки ElicitationResult получают `mcp_server_name`, `action` и необязательные поля `mode`, `elicitation_id` и `content`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form"
}
```

#### Выходные данные ElicitationResult

Хук ElicitationResult может пропустить ответ пользователя, изменить его значения или заблокировать его. Чтобы изменить или заблокировать ответ, завершитесь с кодом 0 и выведите объект `hookSpecificOutput` с `action`. Каждая строка этой таблицы показывает, что вернуть для одного исхода и что получит MCP-сервер:

| Чтобы | Верните | Сервер получит |
| :- | :- | :- |
| Пропустить ответ | Без вывода, с кодом выхода 0 | Ответ пользователя без изменений |
| Изменить отправленные значения | `"action": "accept"` с новыми значениями в `content` | `accept` с вашим `content` вместо значений пользователя |
| Заблокировать ответ | `"action": "decline"` | `decline` без значений пользователя |
| Отменить запрос | `"action": "cancel"` | `cancel` вместе со значениями, отправленными пользователем. Чтобы не передавать их, верните `"decline"` |

Этот вывод изменяет ответ, показанный в разделе [Входные данные ElicitationResult](#elicitationresult-input), так что сервер получает `alice@example.com` вместо отправленного пользователем `alice`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "accept",
    "content": {
      "username": "alice@example.com"
    }
  }
}
```

Ваш `content` заменяет весь объект `content` пользователя, поэтому включайте и поля, которые не изменяете. Возвращайте вместе с ним `action`, потому что Claude Code игнорирует `hookSpecificOutput` без `action`.

Хуки ElicitationResult также запускаются, когда пользователь отклоняет или отменяет запрос, и ваш `action` заменяет его действие. Прежде чем возвращать `accept`, проверяйте, что `action` во входных данных равен `accept`, иначе хук превратит отклонённый запрос в принятый. Этот скрипт вносит то же изменение, если пользователь принял запрос, сохраняет остальные поля и в противном случае ничего не выводит:

```bash theme={null}
#!/bin/bash
input=$(cat)

if [ "$(jq -r '.action' <<<"$input")" = "accept" ]; then
  jq '{hookSpecificOutput: {hookEventName: "ElicitationResult", action: "accept", content: (.content + {username: (.content.username + "@example.com")})}}' <<<"$input"
fi
```

Этот вывод блокирует ответ:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline"
  }
}
```

Код выхода 2 и `"decision": "block"` на верхнем уровне также блокируют ответ. В разделе [Другие способы отклонить elicitation](#other-ways-to-decline-an-elicitation) описано, какой из вариантов действует, когда хук их сочетает, что видит пользователь и какие версии игнорировали `decision`.

Claude Code отбрасывает `reason`, `systemMessage` и `continue` из вывода JSON хука ElicitationResult, какой бы `action` вы ни вернули.

## Prompt-based hooks

В дополнение к command, HTTP и MCP tool hooks, Claude Code поддерживает prompt-based hooks (`type: "prompt"`), которые используют LLM для оценки разрешения или блокировки действия, и agent hooks (`type: "agent"`), которые порождают агентного верификатора с доступом к инструментам. Не все события поддерживают каждый тип hook.

События, которые поддерживают все пять типов hook (`command`, `http`, `mcp_tool`, `prompt` и `agent`):

* `PermissionDenied`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `TeammateIdle`
* `UserPromptExpansion`
* `UserPromptSubmit`

`PermissionRequest` поддерживает `command`, `http`, `mcp_tool` и `prompt` hooks, но не `agent` hooks. Если вы настроите agent hook на этом событии, Claude Code пропустит его и поток разрешений продолжится без изменений. Чтобы разрешить или отклонить из hook, верните [объект решения](#permissionrequest-decision-control) из command или HTTP hook.

События, которые поддерживают `command`, `http` и `mcp_tool` hooks, но не `prompt` или `agent`:

* `ConfigChange`
* `CwdChanged`
* `DirectoryAdded`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `MessageDisplay`
* `Notification`
* `PostCompact`
* `PostModelSwitch`
* `PreCompact`
* `PreModelSwitch`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `WorktreeCreate`
* `WorktreeRemove`

`Setup` поддерживает только `command` hooks. `SessionStart` поддерживает только `command` и `mcp_tool` hooks, а [MCP tool hook fields](#mcp-tool-hook-fields) описывает, когда запускаются его `mcp_tool` hooks.

### How prompt-based hooks work

Вместо выполнения команды Bash, prompt-based hooks:

1. Отправляют входные данные хука и ваш промпт модели Claude, по умолчанию той, которую Claude Code использует для [фоновой функциональности](https://code.claude.com/docs/ru/model-config.md#environment-variables)
2. LLM отвечает структурированным JSON, содержащим решение
3. Claude Code автоматически обрабатывает решение

### Prompt hook configuration

Установите `type` на `"prompt"` и предоставьте строку `prompt` вместо `command`. Используйте заполнитель `$ARGUMENTS` для внедрения данных JSON входа hook в текст вашей подсказки.

В prompt или [agent хуке](#agent-based-hooks) вы можете написать `prompt` как правило о том, что блокировать или разрешать, например «Блокировать любую команду Bash, которая читает файлы `.env`», или как условие, которое должно выполняться, например «Все модульные тесты проходят».

Этот hook `Stop` просит LLM оценить, должен ли Claude остановиться перед разрешением Claude закончить:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `type` | да | Должно быть `"prompt"` |
| `prompt` | да | Текст подсказки для отправки LLM. Используйте `$ARGUMENTS` как заполнитель для JSON входа hook. Если `$ARGUMENTS` отсутствует, JSON входа добавляется к подсказке |
| `model` | нет | Модель для использования при оценке. По умолчанию модель, которую Claude Code использует для [фоновой функциональности](https://code.claude.com/docs/ru/model-config.md#environment-variables) |
| `timeout` | нет | Таймаут в секундах. По умолчанию: 30 |
| `continueOnBlock` | нет | На событиях, к которым это применяется, `true` передаёт причину `ok: false` обратно Claude и продолжает вместо завершения хода. По умолчанию: `false`. См. [Response schema](#response-schema) для поведения для каждого события |

### Response schema

LLM должен ответить JSON, содержащим:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision",
  "impossible": true | false
}
```

| Поле | Описание |
| :- | :- |
| `ok` | `true` разрешает действие. Для `false`, см. поведение для каждого события ниже |
| `reason` | Требуется при `ok` равном `false` |
| `impossible` | Опционально. Модель возвращает его с `ok: false`, когда она судит, что условие никогда не может быть удовлетворено. На `Stop` и `SubagentStop`, Claude Code затем позволяет ходу закончиться вместо передачи причины обратно. Agent hooks и другие события игнорируют его |

Что происходит при `ok: false`, зависит от события:

* `Stop` и `SubagentStop`: причина передаётся обратно Claude как его следующая инструкция и ход продолжается, если только ответ также не устанавливает `impossible: true`, в этом случае Claude Code позволяет остановке и ход заканчивается
* `PreToolUse`: вызов инструмента отклоняется; по умолчанию ход заканчивается и причина отказа появляется в чате как строка предупреждения. Установите `continueOnBlock: true` для возврата причины Claude как ошибки инструмента, чтобы он мог скорректировать и продолжить, эквивалентно `permissionDecision: "deny"` из command hook
* `PostToolUse`: по умолчанию ход заканчивается и причина появляется в чате как строка предупреждения. Установите `continueOnBlock: true` для передачи причины обратно Claude и продолжения хода вместо этого
* `PostToolBatch`, `UserPromptSubmit` и `UserPromptExpansion`: ход заканчивается и причина появляется как строка предупреждения. Эти события заканчивают ход на `decision: "block"` независимо от `continue`
* `PostToolUseFailure` и `TaskCreated`: причина возвращается Claude как ошибка инструмента и ход продолжается, независимо от `continueOnBlock`
* `TaskCompleted` при вызове `TaskUpdate`: Claude получает причину как результат инструмента и ход продолжается, независимо от `continueOnBlock`
* `TeammateIdle`, а также `TaskCompleted` в конце хода товарища по команде: по умолчанию товарищ по команде переходит в режим ожидания и причина появляется в его транскрипте. Установите `continueOnBlock: true`, чтобы отправить причину товарищу по команде и продолжить его работу
* `PermissionRequest`: `ok: false` не имеет эффекта. Чтобы отклонить одобрение из hook, используйте [command hook](#command-hook-fields), возвращающий `hookSpecificOutput.decision.behavior: "deny"`
* `PermissionDenied`: `ok: false` не имеет эффекта, потому что отказ уже произошёл. Единственный результат, который это событие читает, это `hookSpecificOutput.retry`, который prompt и agent hooks не могут установить. Они запускаются на этом событии, но их результат отбрасывается. Используйте [command hook](#command-hook-fields) для возврата `retry`

Если вам нужен более точный контроль над любым событием, используйте [command hook](#command-hook-fields) с полями для каждого события, описанными в [Decision control](#decision-control).

### Check multiple conditions before stopping

Этот hook `Stop` использует подробную подсказку для проверки трёх условий перед разрешением Claude остановиться. Hooks `SubagentStop` используют тот же формат для оценки, должен ли [subagent](https://code.claude.com/docs/ru/sub-agents.md) остановиться. Если модель возвращает `"ok": false`, потому что условие ещё не выполнено, Claude продолжает работать с предоставленной причиной как своей следующей инструкцией:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Agent-based hooks

> [!WARNING]
>
> Agent hooks являются экспериментальными. Поведение и конфигурация могут измениться в будущих выпусках. Для рабочих процессов в производстве предпочитайте [command hooks](#command-hook-fields).

Agent-based hooks (`type: "agent"`) похожи на prompt-based hooks, но с многооборотным доступом к инструментам. Вместо одного вызова LLM, agent hook порождает subagent, который может читать файлы, искать код и проверять кодовую базу для проверки условий. Agent hooks поддерживают те же события, что и [prompt-based hooks](#prompt-based-hooks), за исключением `PermissionRequest`.

### How agent hooks work

Когда срабатывает agent hook:

1. Claude Code порождает subagent с вашей подсказкой и JSON входом hook
2. Subagent может использовать инструменты, такие как Read, Grep и Glob, для исследования
3. После до 50 оборотов subagent возвращает структурированное решение `{ "ok": true/false }`
4. Claude Code разрешает действие, если `ok` имеет значение `true`. Если `ok` имеет значение `false`, Claude Code обрабатывает блокировку так же, как prompt hook с `continueOnBlock: true` на этом событии, как указано в разделе [Response schema](#response-schema)

Agent hooks полезны, когда проверка требует проверки фактических файлов или выхода тестов, а не только оценки данных входа hook.

### Agent hook configuration

Установите `type` на `"agent"` и предоставьте строку `prompt`, используя `$ARGUMENTS` как заполнитель для JSON входа hook. Поля конфигурации те же, что и [prompt hooks](#prompt-hook-configuration), за исключением того, что agent hooks имеют более длинный таймаут по умолчанию в 60 секунд и не имеют поля `continueOnBlock`.

Схема ответа — это `{ "ok": true }` для разрешения или `{ "ok": false, "reason": "..." }` для блокировки. При `ok: false`, Claude Code обрабатывает agent hook так же, как он обрабатывает [prompt hook с `continueOnBlock: true`](#response-schema) на том же событии; agent hooks не имеют поля `continueOnBlock` и не поддерживают поле `impossible` из prompt hook.

Этот hook `Stop` проверяет, что все модульные тесты проходят перед разрешением Claude закончить:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Запуск hooks в фоне

По умолчанию hooks блокируют выполнение Claude до их завершения. Для долгоживущих задач, таких как развёртывания, наборы тестов или вызовы внешних API, установите `"async": true` для запуска hook в фоне, пока Claude продолжает работать. Асинхронные hooks не могут блокировать или управлять поведением Claude: поля ответа, такие как `decision`, `permissionDecision` и `continue`, не имеют эффекта, потому что действие, которое они контролировали, уже завершено.

### Настройка асинхронного hook

Добавьте `"async": true` к конфигурации command hook для запуска его в фоне без блокировки Claude. Это поле доступно только на hooks `type: "command"`.

Этот hook запускает скрипт тестирования после каждого вызова инструмента `Write`. Claude продолжает работать немедленно, пока `run-tests.sh` выполняется. Когда скрипт завершается, его выход доставляется на следующий ход разговора:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

Как только асинхронный hook запущен в фоне, Claude Code не применяет `timeout` к нему. Claude Code по-прежнему применяет `timeout` к hook, который вы запускаете с `asyncRewake`.

Claude Code доставляет результаты асинхронного hook только во время работы сеанса:

* В [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) с флагом `-p` Claude Code завершает любой асинхронный hook, который всё ещё работает при завершении, и завершает его с результатом `cancelled`
* Если работа вашего hook должна пережить сеанс `claude -p`, запустите полностью отделённый процесс из него

### Как выполняются асинхронные hooks

Когда срабатывает асинхронный hook, Claude Code запускает процесс hook и немедленно продолжает без ожидания его завершения. Hook получает те же JSON входные данные через stdin, что и синхронный hook.

После выхода фонового процесса Claude Code доставляет поля `additionalContext` и `systemMessage` из JSON-ответа хука к Claude на следующем ходу диалога, за исключением [повторного вывода `SessionStart`](#limitations). В отличие от `systemMessage` синхронного хука, ни одно из этих полей не показывается вам.

Выводите JSON-ответ в stdout либо единственным содержимым, либо на отдельной строке:

* **Единственным содержимым stdout**: когда ответ — единственный текст в stdout, он может занимать несколько строк, например отформатированный вывод `jq`. Для ответа на нескольких строках требуется Claude Code v2.1.295 или новее.
* **На отдельной строке**: асинхронный хук может выводить в stdout другой текст, если ответ целиком умещается на отдельной строке, например при использовании `jq -c`.

Claude Code проверяет, что JSON-ответ соответствует той же [схеме выходных данных](#json-output), что и у синхронных хуков, и отбрасывает любое поле, значение которого имеет неправильный тип, например `systemMessage`, который не является строкой, вместо его доставки. Запустите с `--debug` для просмотра предупреждения, называющего каждое отброшенное поле.

Уведомления о завершении асинхронного hook подавляются по умолчанию. Чтобы их увидеть, включите подробный режим с помощью `Ctrl+O` или запустите Claude Code с `--verbose`.

### Запуск тестов после изменения файлов

Этот hook запускает набор тестов в фоне всякий раз, когда Claude пишет файл, затем сообщает результаты обратно Claude при завершении тестов. Сохраните этот скрипт в `.claude/hooks/run-tests-async.sh` в вашем проекте и сделайте его исполняемым с помощью `chmod +x`:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results to Claude via additionalContext
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="Tests passed after editing $FILE_PATH"
else
  MSG="Tests failed after editing $FILE_PATH: $RESULT"
fi
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```

Затем добавьте эту конфигурацию в `.claude/settings.json` в корне вашего проекта. Флаг `async: true` позволяет Claude продолжать работу, пока тесты запускаются:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests-async.sh",
            "args": [],
            "async": true
          }
        ]
      }
    ]
  }
}
```

### Ограничения

Асинхронные hooks имеют дополнительные ограничения по сравнению с синхронными hooks:

* Выход hook доставляется на следующий ход разговора. Если сеанс неактивен, ответ ждёт до следующего взаимодействия пользователя. Исключение: hook `asyncRewake`, который выходит с кодом 2, пробуждает Claude немедленно даже когда сеанс неактивен.
* Каждое выполнение создаёт отдельный фоновый процесс.
* Асинхронный хук `SessionStart` запускается каждый раз, когда срабатывает событие. Claude Code пропускает вывод хука, если текст `additionalContext` и `systemMessage` совпадает с тем, что Claude последним получил от этого хука, если только синхронный хук `SessionStart` с тех пор не добавил другой текст. Claude Code доставляет текст, когда он меняется, а также в следующий раз, когда хук запускается после сжатия контекста или `/clear`. До v2.1.295 Claude Code добавлял один и тот же текст в диалог заново при каждом возобновлении.

## Соображения безопасности

### Отказ от ответственности

> [!WARNING]
>
> Command hooks выполняют команды оболочки с вашими полными разрешениями пользователя. Они могут изменять, удалять или получать доступ к любым файлам, к которым может получить доступ ваша учётная запись пользователя. Проверьте и протестируйте все команды hook перед добавлением их в вашу конфигурацию.

### Доверие рабочей области

Claude Code проверяет доверие рабочей области перед запуском любого hook из файла параметров. Что считается доверенным, зависит от типа сеанса:

* **Интерактивный сеанс**: Claude Code удерживает hooks из каждого файла параметров, включая ваш собственный `~/.claude/settings.json`, пока вы не примете [диалог доверия рабочей области](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust) для папки или для родительского каталога, чьё доверие распространяется на неё
* **Сеанс `-p` или SDK**: Claude Code никогда не показывает диалог и рассматривает папку как доверенную, поэтому hooks, зафиксированные в `.claude/settings.json` репозитория, запускаются в папке, которой вы никогда не доверяли

Перед тем как запустить `claude -p` над репозиторием, который вы не писали, проверьте его файлы параметров `.claude/`, начните с [`--bare`](https://code.claude.com/docs/ru/headless#start-faster-with-bare-mode) или [отключите hooks для этого запуска](#disable-or-remove-hooks) с помощью `--settings '{"disableAllHooks": true}'`. Frontmatter hooks в проектном подагенте следуют более строгому правилу, чем hooks файлов параметров. [Что запускается перед доверием папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) перечисляет каждый вид содержимого репозитория по типу сеанса.

### Лучшие практики безопасности

Помните об этих практиках при написании hooks:

* **Проверяйте и санитизируйте входные данные**: никогда не доверяйте входным данным вслепую
* **Всегда заключайте переменные оболочки в кавычки**: используйте `"$VAR"` не `$VAR`
* **Блокируйте обход пути**: проверяйте наличие `..` в путях файлов
* **Используйте абсолютные пути**: указывайте полные пути для скриптов. В форме exec используйте `${CLAUDE_PROJECT_DIR}` и путь не требует кавычек. В форме shell оберните его в двойные кавычки
* **Пропускайте чувствительные файлы**: избегайте `.env`, `.git/`, ключей и т. д.

## Windows PowerShell tool

На Windows вы можете запустить отдельные hooks в PowerShell, установив `"shell": "powershell"` на command hook. Claude Code автоматически обнаруживает `pwsh.exe`, исполняемый файл PowerShell 7 и более поздних версий, и переходит на `powershell.exe` для Windows PowerShell 5.1.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

### Ссылки на скрипты по пути в хуках PowerShell

Чтобы ссылаться на корневой каталог проекта из команды PowerShell в форме shell, напишите `${CLAUDE_PROJECT_DIR}` или `$env:CLAUDE_PROJECT_DIR`. Claude Code переписывает заполнители `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}` и `${CLAUDE_PLUGIN_DATA}` в команде PowerShell в форме shell в форму `${env:NAME}` PowerShell, независимо от того, определён ли хук в `settings.json`, плагине или скилле. PowerShell затем разрешает значение из экспортированного окружения после анализа, поэтому заполнитель работает внутри строк в двойных кавычках, но не внутри строк в одинарных кавычках, где PowerShell никогда не расширяет переменные.

Не пишите простое написание `$CLAUDE_PROJECT_DIR` в hook PowerShell. PowerShell анализирует его как неопределённую локальную переменную и разрешает её в `$null`, что оставляет путь скрипта без префикса корневого каталога проекта. Claude Code не переписывает эту форму; вместо этого она регистрирует предупреждение в [debug log](#debug-hooks).

Пример ниже показывает хук в `settings.json`, который запускает скрипт проекта с формой `$env:`:

```json theme={null}
{
  "type": "command",
  "shell": "powershell",
  "command": "& \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\check.ps1\""
}
```

## Debug hooks

Детали выполнения hooks записываются в файл отладочного журнала. Запустите Claude Code с `claude --debug-file <path>` для записи журнала в известное расположение, или запустите `claude --debug` и прочитайте журнал в `~/.claude/debug/<session-id>.txt`. Флаг `--debug` не выводит на терминал.

Например, hook `PostToolUse` на `Write`, чья команда выводит `hook-ran`, создаёт записи вроде:

```text theme={null}
2026-07-19T02:03:24.382Z [DEBUG] Hook output does not start with {, treating as plain text
2026-07-19T02:03:24.382Z [DEBUG] "Hook PostToolUse:Write (PostToolUse) success:\nhook-ran"
```

Чтобы найти медленный хук, ищите в логе строки `Hooks:`, которые заканчиваются длительностью. В Claude Code v2.1.296 или новее каждый командный хук на событии инструмента, `UserPromptSubmit`, `SessionStart`, `Stop` и ряде других событий оставляет такую строку по завершении, независимо от того, что он вывел. Строка содержит имя события, соединённое двоеточием с именем инструмента или другим значением, по которому сработал хук, затем команду хука в квадратных скобках, плагин, из которого он получен (если есть), то, чем завершился запуск, и его длительность, например `Hooks: PostToolUse:Write [.claude/hooks/log-write.sh] finished with status 0 (31ms)`. Запуск также может завершиться как `timed out after <N>ms`, `cancelled`, `moved to the background` или `failed to start`. На некоторых событиях, таких как `Notification`, `SessionEnd` и `PreCompact`, командный хук вместо этого оставляет строку `completed with status` без длительности.

Для более детальной информации о совпадении hooks установите `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` для просмотра дополнительных строк логирования, таких как количество совпадений фильтра hook и совпадение запроса.

Для устранения неполадок распространённых проблем, таких как hooks, которые не срабатывают, Stop hooks, которые продолжают блокировать, или ошибки конфигурации, см. [Limitations and troubleshooting](https://code.claude.com/docs/ru/hooks-guide.md#limitations-and-troubleshooting) в руководстве. Для более широкого диагностического пошагового руководства, охватывающего `/context`, `/doctor` и приоритет параметров, см. [Debug your config](https://code.claude.com/docs/ru/debug-your-config.md).
