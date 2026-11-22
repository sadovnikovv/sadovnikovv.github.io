> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка разрешений

> Контролируйте, как ваш агент использует инструменты, с помощью режимов разрешений, hooks и декларативных правил разрешения/запрета.

Claude Agent SDK предоставляет элементы управления разрешениями для управления использованием инструментов Claude. Используйте режимы разрешений и правила для определения того, что разрешено автоматически, и обратный вызов [`canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) для обработки всего остального во время выполнения.

## Как оцениваются разрешения

> [!NOTE]
>
> Если вы загружаете плагин, содержащий [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md), см. [место решений мода среди правил и хуков](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

Когда Claude запрашивает инструмент, Claude Code проверяет вызов на следующих шагах. Каждый шаг может определить исход вызова, передать его в ваш callback `canUseTool` или пропустить дальше:

**1. Хуки**

Запуск [хуков](https://code.claude.com/docs/ru/agent-sdk/hooks.md). Хук может сразу отклонить вызов или передать его дальше. Хук, возвращающий `allow`, не пропускает этапы правил запрета и правил запроса подтверждения: они проверяются независимо от результата хука.

Хук `PreToolUse`, который возвращает `allow`, также не может одобрить команду `rm` или `rmdir`, цель которой Claude Code распознает как [критический путь](https://code.claude.com/docs/ru/permission-modes.md#critical-paths), например `rm -rf ~`. О том, что делает такой `allow` в режиме планирования, см. [Подтверждения хуков в режиме планирования](https://code.claude.com/docs/ru/permissions.md#hook-approvals-in-plan-mode).

**2. Deny rules**

Если совпадает правило deny из `disallowed_tools` или из [файла настроек, который загружает SDK](#rules-in-settings-files), вызов отклоняется и [`canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) не вызывается. Вызов отклоняется таким образом даже в режиме [`bypassPermissions`](#bypass-permissions-mode-bypasspermissions) и даже если хук вернул `allow`.

**3. Ask rules**

Проверьте правила `ask` из [settings.json](https://code.claude.com/docs/ru/settings-reference.md#permission-settings). Если правило ask совпадает, вызов передается в ваш [callback `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) для подтверждения, даже в режиме `bypassPermissions`.

Инструменты, требующие взаимодействия с пользователем, ведут себя так же. `AskUserQuestion` и MCP инструменты, сервер которых устанавливает [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/ru/mcp#require-approval-for-a-specific-tool), передаются в callback, даже когда совпадает правило allow. В режиме `dontAsk` оба случая вместо этого отклоняются, потому что этот режим превращает каждый запрос подтверждения в отказ. Аннотация MCP требует Claude Code v2.1.199 или позже.

Инструменты [claude.ai connector](https://code.claude.com/docs/ru/mcp.md#organization-controls-on-connector-tools), для которых ваша организация установила `ask`, также покидают поток на этом шаге. Каждый вызов передается в callback, даже в режиме `bypassPermissions` и даже когда совпадает правило allow. Callback получает причину `Your organization requires approval for this tool`. В режиме `dontAsk` вызов отклоняется вместо этого, потому что этот режим никогда не запрашивает.

В TypeScript SDK, если вы установите `permission_policy` пользовательского инструмента в значение [`always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools), ни одно правило allow не одобряет его вызовы, даже запись `allowedTools`. В режиме `dontAsk` Claude Code отклоняет такие вызовы, а в режимах `auto`, `plan` или `bypassPermissions` он [может одобрить их](https://code.claude.com/docs/ru/agent-sdk/typescript.md#permission-modes-that-can-approve-an-always_ask-call) до запуска вашего callback.

**4. Permission mode**

Примените активный [режим разрешений](#permission-modes):

* В режиме `bypassPermissions` Claude Code одобряет каждый вызов, достигший этого шага, если только это не одно из [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). О том, какие из этих действий передаются в ваш callback `canUseTool`, см. [Bypass permissions mode](#bypass-permissions-mode-bypasspermissions).
* В режиме `acceptEdits` Claude Code одобряет операции с файлами, перечисленные в разделе [Accept edits mode](#accept-edits-mode-acceptedits).
* В режиме `plan` некоторые вызовы достигают вашего callback, а другие, когда доступен авторежим, вместо этого передаются его классификатору. Подробнее см. [Plan mode](#plan-mode-plan).
* В режимах `default` и `dontAsk` вызов переходит к правилам allow.
* О режиме `auto` см. [Auto mode](#auto-mode-auto).

**5. Allow rules**

Проверьте правила `allow` (из `allowed_tools` и settings.json). Если правило совпадает, инструмент одобряется. Вызов, который инструмент одобряет самостоятельно, также разрешается на этом шаге без необходимости в правиле: например, чтение файла в ваших рабочих каталогах или [команда Bash только для чтения](https://code.claude.com/docs/ru/permissions.md#read-only-commands).

Распознанные [удаления по критическим путям](https://code.claude.com/docs/ru/permission-modes.md#critical-paths) не одобряются правилом allow, а команды с пометкой `Dangerous rm operation not ruled out` не одобряются правилом `Bash` или `Bash(*)`. Достигают ли они затем вашего callback, зависит от режима разрешений: например, в сессии Agent SDK в режиме `auto` Claude Code по умолчанию отклоняет их, не вызывая его. [Таблица режимов для критических путей](https://code.claude.com/docs/ru/permission-modes.md#critical-path-removals-in-each-permission-mode) перечисляет, что каждый режим с ними делает.

Правило разрешения не одобряет чтение из [сетевого пути](https://code.claude.com/docs/ru/permissions.md#network-paths).

**6. Обратный вызов canUseTool**

Если ни один из предыдущих шагов не разрешает запрос, для принятия решения вызывается ваш [обратный вызов `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input). В режиме `dontAsk` этот шаг пропускается и в использовании инструмента отказывается, однако установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) всё же может одобрить [некоторые такие вызовы](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

В TypeScript SDK, если вы установите [`permissionPrompts: 'none'`](https://code.claude.com/docs/ru/agent-sdk/typescript#options), ваш callback не вызывается на этом шаге. Hook [`PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest) все еще получает возможность принять решение, и если он этого не делает, Claude Code отклоняет вызов. Опция требует Claude Code v2.1.259 или позже.

![Диаграмма шестиэтапного потока оценки разрешений, соответствующая шагам выше: запрос инструмента проходит через hooks, правила deny, правила ask, режим разрешений, правила allow и canUseTool. Hooks, правила deny и canUseTool могут маршрутизировать вниз к Blocked; обход режима разрешений, правила allow и canUseTool могут маршрутизировать вверх к Execute; правила ask маршрутизируют к canUseTool.](https://mintcdn.com/claude-code/jYgs7qigNjO1Badj/images/agent-sdk/permissions-flow.svg?fit=max\&auto=format\&n=jYgs7qigNjO1Badj\&q=85\&s=c771ad9085b1277d3708027a49c744bc)

Если вы передаете callback `canUseTool` в конфигурацию, где TypeScript SDK ожидает, что порядок оценки автоматически одобрит вызовы перед консультацией callback, SDK выдает предупреждение процесса Node.js один раз при построении запроса. Код предупреждения — `CLAUDE_SDK_CAN_USE_TOOL_SHADOWED`. Две конфигурации вызывают его:

* `permissionMode: 'bypassPermissions'`: текст предупреждения начинается с `canUseTool will not be invoked: permissionMode 'bypassPermissions'`. Вызовы инструментов одобряются до обращения к `canUseTool`, поэтому ваш callback выполняется лишь для немногих вызовов, например перечисленных в разделе [Bypass permissions mode](#bypass-permissions-mode-bypasspermissions). Чтобы проверять и одобренные вызовы, перенесите проверки вашего callback в [хук `PreToolUse`](https://code.claude.com/docs/ru/agent-sdk/hooks)
* Запись `allowedTools`, содержащая только имя инструмента, например `"Read"`: предупреждение перечисляет каждую такую запись после `canUseTool will not be invoked for:`. Вызовы перечисленного инструмента одобряются до обращения к `canUseTool`, за исключением [вызовов, которые правило allow никогда не одобряет](#calls-an-allow-rule-never-approves). Чтобы ваш callback выполнялся для требующих подтверждения вызовов перечисленного инструмента, удалите запись этого инструмента из `allowedTools`

Записи со спецификатором, такие как `Bash(ls *)`, и режим `acceptEdits` не вызывают его, и правила allow из файлов настроек не видны для проверки.

Предупреждение не блокирует ни один вызов и не изменяет никаких параметров. Если ваш callback уже получает все вызовы, которые вы хотите проверять, оставьте конфигурацию как есть. Чтобы записать предупреждение в лог, подпишитесь с помощью `process.on('warning', ...)` и сопоставьте код `CLAUDE_SDK_CAN_USE_TOOL_SHADOWED`.

Эта страница сосредоточена на **правилах allow и deny** и **режимах разрешений**. Для других шагов:

* **Hooks:** запустите пользовательский код для разрешения, отклонения или изменения запросов инструментов. См. [Control execution with hooks](https://code.claude.com/docs/ru/agent-sdk/hooks.md).
* **canUseTool callback:** запросите у пользователей одобрение во время выполнения, когда ни один более ранний шаг не определит исход вызова. См. [Обработка одобрений и пользовательского ввода](https://code.claude.com/docs/ru/agent-sdk/user-input.md).

## Правила разрешения и запрета

Когда вы задаете `allowedTools` и `disallowedTools` (TypeScript) или `allowed_tools` и `disallowed_tools` (Python), Claude Code добавляет их записи в списки правил разрешения и запрета в [потоке оценки разрешений](#how-permissions-are-evaluated). Любой другой инструмент, не указанный в `allowed_tools`, по-прежнему доступен Claude, и вызов к нему, требующий одобрения, переходит в режим разрешений.

| Опция | Эффект |
| :- | :- |
| `allowed_tools=["Read", "Grep"]` | `Read` и `Grep` автоматически одобрены, за исключением [чтения из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths). Другие инструменты, не указанные здесь, по-прежнему существуют, и вызовы к ним, требующие одобрения, переходят в режим разрешений и `canUseTool`. |
| `disallowed_tools=["Bash"]` | Определение инструмента `Bash` удаляется из запроса. |
| `disallowed_tools=["Bash(rm *)"]` | `Bash` остается доступным. Вызовы, соответствующие `rm *` [как написано](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits), отклоняются в каждом режиме разрешений, включая `bypassPermissions`. Другие вызовы `Bash`, включая `/bin/rm`, переходят в режим разрешений. |
| `disallowed_tools=["*"]` | Глобы имен инструментов поддерживаются в правилах запрета: `"*"` соответствует каждому инструменту и `"mcp__*"` соответствует каждому инструменту MCP на всех серверах. |

Правила разрешения принимают глобы имен инструментов только после буквального префикса `mcp__<server>__`. Сегмент сервера должен быть свободен от глобов, чтобы правило называло конкретный сервер, который вы настроили: `mcp__puppeteer__*` соответствует каждому инструменту с сервера `puppeteer`, а `mcp__github__get_*` соответствует его инструментам `get_`. Неякорированная запись, такая как `allowed_tools=["*"]` или `allowed_tools=["mcp__*"]`, игнорируется и не одобряет ничего автоматически.

> [!WARNING]
>
> **Автоматически одобренные инструменты никогда не достигают `canUseTool`.** Вызов инструмента, одобренный на любом более раннем этапе, по `acceptEdits` или `bypassPermissions`, или по правилу разрешения, пропускает ваш обратный вызов `canUseTool`, поэтому проверки разрешений, которые вы там поместили, молча обходятся для этого инструмента.
>
> Если вызовы инструмента из `allowed_tools` всё равно доходят до вашего обратного вызова `canUseTool` или отклоняются в режиме `dontAsk`, проверьте, не являются ли они [чтением из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths) или одним из следующих вызовов. Ни одно правило разрешения не одобряет эти вызовы. В режиме `dontAsk`, который никогда не запрашивает подтверждение, Claude Code отклоняет их без вызова `canUseTool`, а в других режимах разрешений вы обрабатываете их так, как указано в каждом пункте:
>
> * `AskUserQuestion`, инструменты MCP, отмеченные [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/ru/mcp#require-approval-for-a-specific-tool), и инструменты коннекторов, [для которых ваша организация установила `ask`](https://code.claude.com/docs/ru/mcp#organization-controls-on-connector-tools): отвечайте на них в обратном вызове. В разделе [Обработка уточняющих вопросов](https://code.claude.com/docs/ru/agent-sdk/user-input.md#handle-clarifying-questions) показано, как отвечать на `AskUserQuestion`, а вызов коннектора поступает с причиной `Your organization requires approval for this tool`
>
> * Пользовательские инструменты, которые ваше приложение помечает как [`always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools): принимайте решение о вызове в обратном вызове. Чтобы эти вызовы перестали поступать, [измените политику во время сессии](https://code.claude.com/docs/ru/agent-sdk/typescript.md#mcpsdkserverconfigwithinstance). В режимах `auto`, `plan` и `bypassPermissions` вызов вместо этого может быть одобрен до обратного вызова в случаях, перечисленных в разделе [Режимы разрешений, которые могут одобрить вызов `always_ask`](https://code.claude.com/docs/ru/agent-sdk/typescript#permission-modes-that-can-approve-an-always_ask-call)
>
> * Распознанные удаления `rm` и `rmdir` [по критическим путям](https://code.claude.com/docs/ru/permission-modes.md#critical-paths): в режимах `default`, `acceptEdits` и `bypassPermissions` разрешите или запретите удаление в обратном вызове, где [`decisionReason`](https://code.claude.com/docs/ru/agent-sdk/typescript#canusetool) начинается с `Dangerous rm`. Для режимов `auto` и `plan` см. [Удаления по критическим путям в каждом режиме разрешений](https://code.claude.com/docs/ru/permission-modes.md#critical-path-removals-in-each-permission-mode)
>
> * **Простое имя**: запись, такая как `Read` или `mcp__github__get_issue`, автоматически одобряет каждый вызов этого инструмента, кроме [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves), и [чтения из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths).
>
> * **Правило с областью действия**: запись, такая как `Bash(npm test *)`, автоматически одобряет совпадающие с ней вызовы, а другие вызовы `Bash`, требующие одобрения, переходят в режим разрешений.
>
> Чтобы проверять вызовы, которые одобряет правило разрешения, `acceptEdits` или `bypassPermissions`, используйте [хук `PreToolUse`](https://code.claude.com/docs/ru/agent-sdk/hooks), который выполняется и для таких вызовов. Отказ хука применяется даже в режиме `bypassPermissions`.

Для заблокированного агента объедините `allowedTools` с `permissionMode: "dontAsk"`:

```typescript theme={null}
const options = {
  allowedTools: ["Read", "Glob", "Grep"],
  permissionMode: "dontAsk"
};
```

Перечисленные вызовы `Read`, `Glob` и `Grep` одобряются, кроме [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves), и [чтения из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths). Каждый другой вызов, который запросил бы подтверждение, вместо этого отклоняется, хотя установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) всё же может одобрить [некоторые из этих вызовов](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

Вызовы, которые не требуют одобрения в режиме `default`, выполняются независимо от того, указаны ли они в списке. К ним относятся [команды Bash только для чтения](https://code.claude.com/docs/ru/permissions.md#read-only-commands), инструменты, такие как `Agent`, которые не спрашивают перед запуском, и чтение файлов в ваших рабочих каталогах. Чтобы полностью скрыть встроенный инструмент от Claude, а не отклонять его вызовы, добавьте его простое имя в `disallowedTools`.

> [!WARNING]
>
> **`allowed_tools` не ограничивает `bypassPermissions`.** `allowed_tools` предварительно одобряет инструменты, которые вы указали. В режиме `bypassPermissions` Claude Code одобряет вызов неуказанного инструмента, если только это не одно из [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves).
>
> Если вы установите `allowed_tools=["Read"]` вместе с `permission_mode="bypassPermissions"`, Claude Code всё равно одобрит вызовы таких инструментов, как `Bash`, `Write` и `Edit`. Если вам нужен `bypassPermissions`, но вы хотите заблокировать определенные инструменты, используйте `disallowed_tools`. О вызовах, которые в этом режиме всё же доходят до вашего обратного вызова `canUseTool`, см. [Режим обхода разрешений](#bypass-permissions-mode-bypasspermissions).

Вы также можете настроить правила разрешения, запрета и запроса декларативно в `.claude/settings.json`. Эти правила читаются, когда источник параметра `project` включен, что он есть для параметров `query()` по умолчанию. Если вы явно установите `setting_sources` (TypeScript: `settingSources`), включите `"project"`, чтобы они применялись. См. [Параметры разрешений](https://code.claude.com/docs/ru/settings-reference.md#permission-settings) для синтаксиса правил.

О том, когда применяются правила разрешения из `.claude/settings.json` проекта, см. [Правила разрешения проекта и доверие к рабочему пространству](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust).

### Шаблоны путей в правилах

Правила с областью действия для `Read` и `Edit` принимают шаблон пути. Правила `Edit(path)` управляют всеми встроенными инструментами, которые записывают файлы, включая `Write` и `NotebookEdit`, поэтому для любого из них записывайте правило пути как `Edit(path)`. Если вы запишете правило пути как `Write(path)` или `NotebookEdit(path)`, оно [не совпадет ни с одним вызовом](https://code.claude.com/docs/ru/permissions.md#path-rules-that-never-match) и не будет иметь эффекта.

В `allowed_tools` и `disallowed_tools` начинайте шаблон пути с `//` для абсолютного пути или с одной `/` для пути внутри рабочего каталога сессии:

* **`//path`**: с правилом запрета `Edit(//secrets/**)` Claude Code блокирует записи под `/secrets` на диске из файловых инструментов Claude и из [команд Bash, таких как `tee` и перенаправление `> file`](https://code.claude.com/docs/ru/permissions#what-read-and-edit-rules-cover). Скрипт, который запускает Claude и который сам открывает файлы, всё равно может записывать под `/secrets`. О принудительном применении на уровне операционной системы см. [Настройка изолированного инструмента Bash](https://code.claude.com/docs/ru/sandboxing.md).
* **`/path`**: `Edit(/secrets/**)` соответствует каталогу `secrets` внутри рабочего каталога.

О других способах начать шаблон пути см. [Правила Read и Edit](https://code.claude.com/docs/ru/permissions.md#read-and-edit).

## Режимы разрешений

Режимы разрешений обеспечивают глобальный контроль над тем, как Claude использует инструменты. Вы можете установить режим разрешений при вызове `query()` или изменить его динамически во время сеансов потоковой передачи.

В Claude Code v2.1.302 или более поздней версии ваше приложение запускается в режиме `default`, если вы не установите режим разрешений и приложение не получит его из [`permissions.defaultMode`](https://code.claude.com/docs/ru/settings-reference#permissions-defaultmode) в своих файлах настроек. В режиме `default` Claude Code отклоняет любой вызов инструмента, требующий подтверждения, если вы не подтвердите его с помощью правила разрешения, хука, обратного вызова `canUseTool` или инструмента запроса разрешений. Если вызовы инструментов отклоняются, см. [Вызовы инструментов отклоняются в `claude -p` и запусках Agent SDK](https://code.claude.com/docs/ru/permission-modes#which-mode-a-non-interactive-run-starts-in).

### Доступные режимы

SDK поддерживает эти режимы разрешений:

| Режим | Описание | Поведение инструмента |
| :- | :- | :- |
| `default` | Стандартное поведение разрешений | Нет автоматических одобрений на основе режима; вызовы, требующие одобрения и не соответствующие никакому правилу разрешения, запускают ваш обратный вызов `canUseTool` |
| `dontAsk` | Отклонить вместо запроса | Любой вызов, который иначе запросил бы подтверждение, отклоняется без вызова `canUseTool`, хотя установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) всё равно может одобрить [некоторые из этих вызовов](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods). Вызовы, одобренные `allowed_tools` или правилами разрешения в `settings.json`, выполняются, как и вызовы, не требующие одобрения в режиме `default`. Некоторые вызовы, например [чтение из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths), отклоняются, даже если им соответствует `allowed_tools` или правило разрешения. Список см. в разделе [Режим не спрашивать](#don’t-ask-mode-dontask) |
| `acceptEdits` | Автоматически принимать редактирование файлов | Редактирование файлов и [операции с файловой системой](#accept-edits-mode-acceptedits) (`mkdir`, `rm`, `mv` и т. д.) внутри ваших [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories) автоматически одобряются |
| `bypassPermissions` | Обойти проверки разрешений | Инструменты выполняются без запросов разрешений, за исключением [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves) и, вне [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md), пользовательских инструментов, которые ваше приложение [помечает как `always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools). Используйте с осторожностью |
| `plan` | Режим планирования | Claude исследует и планирует. Редактирование, выполняемое файловыми инструментами Claude, поступает в ваш обратный вызов `canUseTool`, даже когда ему соответствует правило разрешения |
| `auto` | Одобрения, классифицированные моделью | Классификатор модели проверяет действия, такие как команды оболочки и сетевые запросы, разрешая или блокируя каждое из них. См. [Режим Auto](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) для получения информации о доступности и порядке принятия решений |

> [!WARNING]
>
> **Наследование субагентом:** Если ваша основная сессия находится в [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode), субагент, в [`AgentDefinition`](https://code.claude.com/docs/ru/agent-sdk/typescript#agentdefinition) которого задано `permissionMode: "acceptEdits"`, всё равно выполняется в режиме планирования. Вызовы `Edit` и `Write` этого субагента для ваших исходных файлов по-прежнему поступают в ваш обратный вызов `canUseTool`. Режим планирования действует и для определённых вами субагентов, чтобы передача работы одному из них не позволяла обойти предварительную проверку плана.
>
> Субагент наследует `plan`, `acceptEdits`, `auto` или `bypassPermissions` от основной сессии, а при основной сессии в режиме `default` или `dontAsk` он выполняется в заданном вами режиме. Даже в этом случае Claude Code никогда не применяет значение `"bypassPermissions"`, а значение `"auto"` применяет только тогда, когда [авторежим доступен](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) этому субагенту. Исключение `bypassPermissions` требует Claude Code v2.1.267 или более поздней версии.
>
> Подагенты могут иметь различные системные подсказки и менее ограниченное поведение, чем ваш основной агент, поэтому наследование `bypassPermissions` предоставляет им полный автономный доступ к системе. [Действия, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves), по-прежнему применяются.

### Установка режима разрешений

Вы можете установить режим разрешений один раз при запуске запроса или изменить его динамически во время активного сеанса.

> [tab] При запросе
>
> Передайте `permission_mode` (Python) или `permissionMode` (TypeScript) при создании запроса.
>
> ```python Python theme={null}
> import asyncio
> from claude_agent_sdk import query, ClaudeAgentOptions
>
>
> async def main():
>     async for message in query(
>         prompt="Help me refactor this code",
>         options=ClaudeAgentOptions(
>             permission_mode="default",  # Set the mode here
>         ),
>     ):
>         if hasattr(message, "result"):
>             print(message.result)
>
>
> asyncio.run(main())
> ```
>
> ```typescript TypeScript theme={null}
> import { query } from "@anthropic-ai/claude-agent-sdk";
>
> async function main() {
>   for await (const message of query({
>     prompt: "Help me refactor this code",
>     options: {
>       permissionMode: "default" // Set the mode here
>     }
>   })) {
>     if ("result" in message) {
>       console.log(message.result);
>     }
>   }
> }
>
> main();
> ```

> [tab] Во время потоковой передачи
>
> Вызовите `set_permission_mode()` (Python) или `setPermissionMode()` (TypeScript) для изменения режима в середине сеанса. Новый режим вступает в силу немедленно для всех последующих запросов инструментов. Это позволяет вам начать с ограничительного режима и ослабить разрешения по мере развития доверия, например переключиться на `acceptEdits` после проверки первоначального подхода Claude.
>
> ```python Python theme={null}
> import asyncio
> from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
>
>
> async def main():
>     async with ClaudeSDKClient(
>         options=ClaudeAgentOptions(
>             permission_mode="default",  # Start in default mode
>         )
>     ) as client:
>         await client.query("Help me refactor this code")
>
>         # Change mode dynamically mid-session
>         await client.set_permission_mode("acceptEdits")
>
>         # Process messages with the new permission mode
>         async for message in client.receive_response():
>             if hasattr(message, "result"):
>                 print(message.result)
>
>
> asyncio.run(main())
> ```
>
> ```typescript TypeScript theme={null}
> import { query } from "@anthropic-ai/claude-agent-sdk";
>
> async function main() {
>   const q = query({
>     prompt: "Help me refactor this code",
>     options: {
>       permissionMode: "default" // Start in default mode
>     }
>   });
>
>   // Change mode dynamically mid-session
>   await q.setPermissionMode("acceptEdits");
>
>   // Process messages with the new permission mode
>   for await (const message of q) {
>     if ("result" in message) {
>       console.log(message.result);
>     }
>   }
> }
>
> main();
> ```

### Детали режимов

#### Режим принятия редактирования (`acceptEdits`)

Автоматически одобряет операции с файлами, чтобы Claude мог редактировать код без запроса. Другие инструменты (такие как команды Bash, которые не являются операциями с файловой системой) по-прежнему требуют обычных разрешений.

**Автоматически одобренные операции:**

* Редактирование файлов с помощью инструментов Edit, Write и NotebookEdit
* Команды файловой системы: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`

Оба применяются к путям внутри рабочего каталога или добавленного вами каталога. В Python каталог добавляется с помощью `add_dirs`, а в TypeScript — с помощью `additionalDirectories`. В режиме `acceptEdits` Claude Code не одобряет запрос автоматически, когда Claude:

* Работает с путем вне этой области
* Записывает в [защищенный путь](https://code.claude.com/docs/ru/permission-modes.md#protected-paths)
* Удаляет с помощью `rm` или `rmdir` путь, который Claude Code распознает как [критический путь](https://code.claude.com/docs/ru/permission-modes.md#critical-paths)
* Запускает [`touch`](https://code.claude.com/docs/ru/permission-modes#auto-approve-file-edits-with-acceptedits-mode), например, с опцией, glob-шаблоном или префиксом `timeout 5` или `LANG=C`

**Используйте когда:** вы доверяете редактированиям Claude и хотите более быструю итерацию, например во время прототипирования или при работе в изолированном каталоге.

#### Режим не спрашивать (`dontAsk`)

Преобразует любой запрос разрешения в отклонение без вызова `canUseTool`, хотя установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) всё равно может одобрить [некоторые из этих вызовов](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods). Инструменты, предварительно одобренные `allowed_tools`, правилами разрешения в `settings.json` или хуком, выполняются в обычном режиме. Вызовы, не требующие подтверждения в режиме `default`, также выполняются в обычном режиме, например чтение файлов внутри ваших рабочих каталогов и вызовы `Agent`.

Эти вызовы отклоняются, даже если им соответствует правило разрешения:

* Инструменты коннекторов, [для которых ваша организация установила `ask`](https://code.claude.com/docs/ru/mcp#organization-controls-on-connector-tools)
* Инструменты, требующие взаимодействия с пользователем, такие как `AskUserQuestion` и инструменты MCP, сервер которых задаёт [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/ru/mcp#require-approval-for-a-specific-tool)
* Пользовательские инструменты, для которых ваше приложение устанавливает `permission_policy` в значение [`always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools)
* [Чтение из сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths)
* Распознанные [удаления критических путей](https://code.claude.com/docs/ru/permission-modes.md#critical-paths)

Если ваш хук `PreToolUse` возвращает `allow` для распознанного удаления критического пути, чтения из сетевого пути или вызова инструмента, помеченного `always_ask`, вызов всё равно отклоняется. Проверка, которая распознает такие удаления, [может пропустить некоторые команды](https://code.claude.com/docs/ru/permission-modes.md#critical-paths).

**Используйте когда:** вы запускаете headless-агента и хотите жесткого отклонения для каждого вызова, который иначе запросил бы подтверждение.

#### Режим обхода разрешений (`bypassPermissions`)

Автоматически одобряет использование инструментов без запроса, за исключением [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). Хуки по-прежнему выполняются и могут блокировать операции при необходимости. На Linux и macOS Claude Code отказывается запускаться в этом режиме от имени root или под `sudo` вне [признанной песочницы](https://code.claude.com/docs/ru/permission-modes.md#skip-all-checks-with-bypasspermissions-mode), и запрос завершается ошибкой перед первым ходом.

> [!WARNING]
>
> Используйте с крайней осторожностью. Claude имеет полный доступ к системе в этом режиме. Используйте только в контролируемых средах, где вы доверяете всем возможным операциям.
>
> `allowed_tools` не ограничивает этот режим, и вызовы инструментов, которые вы не указали, тоже одобряются. Эти элементы управления по-прежнему применяются:
>
> * Правила отклонения, явные правила `ask` и hooks оцениваются перед проверкой режима и могут по-прежнему блокировать инструмент.
> * Инструменты коннектора, [установленные вашей организацией на `ask`](https://code.claude.com/docs/ru/mcp#organization-controls-on-connector-tools), инструменты, требующие взаимодействия с пользователем, распознанные [удаления критических путей](https://code.claude.com/docs/ru/permission-modes.md#critical-paths) и команды Bash, помеченные [`Dangerous rm operation not ruled out`](https://code.claude.com/docs/ru/permission-modes#dangerous-rm-operation-not-ruled-out), по-прежнему переходят к вашему обратному вызову `canUseTool`. Проверка, которая распознает удаления критических путей, [может пропустить некоторые команды](https://code.claude.com/docs/ru/permission-modes.md#critical-paths), а также вы можете [отключить запрос подтверждения при удалении критических путей](https://code.claude.com/docs/ru/permission-modes.md#turn-off-the-critical-path-removal-prompt-in-bypasspermissions-mode). Вне [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) вызовы пользовательских инструментов, которые ваше приложение [помечает как `always_ask`](https://code.claude.com/docs/ru/agent-sdk/custom-tools#require-approval-for-specific-tools), также переходят к обратному вызову.
> * [Защита обмена сообщениями между сеансами](https://code.claude.com/docs/ru/permission-modes.md#skip-all-checks-with-bypasspermissions-mode) по-прежнему применяется.

#### Режим планирования (`plan`)

Claude исследует кодовую базу и создает план. Во время планирования редактирование, выполняемое файловыми инструментами Claude вне [защищенных путей](https://code.claude.com/docs/ru/permission-modes.md#protected-paths), достигает вашего обратного вызова `canUseTool`, даже когда ему соответствует правило разрешения или хук `PreToolUse` возвращает `allow`. Вызовы [`AskUserQuestion`](https://code.claude.com/docs/ru/agent-sdk/user-input#handle-clarifying-questions) также достигают вашего обратного вызова, даже когда правило разрешения указывает этот инструмент.

Когда [авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) доступен, Claude Code во время планирования отправляет следующие вызовы на проверку [классификатору авторежима](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode), а не в ваш обратный вызов, если их не одобряет никакое правило разрешения:

* Команды оболочки
* Загрузки веб-страниц
* Веб-поиск
* Вызовы инструментов MCP, которые их сервер помечает как доступные только для чтения

Эта проверка включена по умолчанию. Чтобы отключить ее, установите [`useAutoModeDuringPlan`](https://code.claude.com/docs/ru/settings-reference#useautomodeduringplan) в `false` в параметре `settings`, который вы передаете в `query()`, или в своих пользовательских настройках. Пока проверка отключена, веб-поиск и вызовы инструментов MCP, помеченных как доступные только для чтения, достигают вашего обратного вызова.

Для команд оболочки и загрузок веб-страниц таблица показывает, достигает ли каждый вызов вашего обратного вызова:

| Вызов во время планирования | Проверка включена | Проверка отключена или авторежим недоступен |
| :- | :- | :- |
| Команда оболочки [только для чтения](https://code.claude.com/docs/ru/permissions.md#read-only-commands), например `ls` | Выполняется, не достигая вашего обратного вызова | Выполняется, не достигая вашего обратного вызова |
| Любая другая команда оболочки, которую не одобряет никакое правило разрешения, за исключением [удаления критического пути](https://code.claude.com/docs/ru/permission-modes.md#critical-paths) | Поступает классификатору, который одобряет или отклоняет ее без вашего обратного вызова | Достигает вашего обратного вызова |
| Вызов `WebFetch` к [предварительно одобренному домену документации](https://code.claude.com/docs/ru/tools-reference.md#webfetch-tool-behavior) | Выполняется, не достигая вашего обратного вызова | Выполняется, не достигая вашего обратного вызова |
| Любой другой вызов `WebFetch`, который не одобряет никакое правило разрешения | Поступает классификатору, который одобряет или отклоняет его без вашего обратного вызова | Достигает вашего обратного вызова |

О том, что происходит после того, как классификатор отклоняет несколько вызовов подряд, см. [Пороги повторных блокировок](https://code.claude.com/docs/ru/permission-modes.md#repeated-block-thresholds).

> [!NOTE]
>
> В TypeScript SDK, если вы установите `allowDangerouslySkipPermissions: true` вместе с `permissionMode: 'plan'`, редактирование файлов по-прежнему достигает вашего обратного вызова `canUseTool`. Чтобы позже переключить сессию, которая начинается в режиме планирования, на `bypassPermissions` с помощью `setPermissionMode()`, необходимо задать `allowDangerouslySkipPermissions` с самого начала.

**Используйте когда:** вы хотите, чтобы Claude сначала составил план, например во время код-ревью или перед крупным изменением.

#### Авторежим (`auto`)

Модель-классификатор проверяет действия, такие как команды оболочки и сетевые запросы, перед их выполнением и разрешает или блокирует каждое проверяемое действие. О моделях и провайдерах, которые требуются для авторежима, и о порядке, в котором он оценивает действия, см. [Устранение запросов разрешений с помощью авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode).

Если вы переключаете сессию, находящуюся в авторежиме, на модель, которую авторежим не поддерживает, с помощью [`set_model()`](https://code.claude.com/docs/ru/agent-sdk/python#claudesdkclient), [`setModel()`](https://code.claude.com/docs/ru/agent-sdk/typescript#query-object) или [`applyFlagSettings()`](https://code.claude.com/docs/ru/agent-sdk/typescript#applyflagsettings), сессия переходит в режим `default`:

* **Что вы увидите**: сообщение `system` с подтипом `status` и `permissionMode`, установленным в `"default"`, которое TypeScript SDK типизирует как [`SDKStatusMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkstatusmessage). С этого момента вызовы, требующие подтверждения и не соответствующие никакому правилу разрешения, достигают вашего обратного вызова `canUseTool`.
* **Чтобы вернуться в авторежим**: переключитесь на поддерживаемую модель, затем вызовите `set_permission_mode("auto")` или `setPermissionMode("auto")`. Если вы переключите модель обратно без этого вызова, сессия останется в режиме `default`. Пока активна неподдерживаемая модель, вызов завершается ошибкой `Cannot set permission mode to auto: auto mode unavailable for this model`.

Переход в режим `default` после вызова `set_model()`, `setModel()` или `applyFlagSettings()` требует Claude Code v2.1.299 или более поздней версии.

## Связанные ресурсы

Для других этапов потока оценки разрешений:

* [Обработка одобрений и ввода пользователя](https://code.claude.com/docs/ru/agent-sdk/user-input.md): интерактивные подсказки одобрения и уточняющие вопросы
* [Руководство hooks](https://code.claude.com/docs/ru/agent-sdk/hooks.md): запуск пользовательского кода в ключевых точках жизненного цикла агента
* [Правила разрешений](https://code.claude.com/docs/ru/settings-reference.md#permission-settings): декларативные правила разрешения/запрета в `settings.json`
