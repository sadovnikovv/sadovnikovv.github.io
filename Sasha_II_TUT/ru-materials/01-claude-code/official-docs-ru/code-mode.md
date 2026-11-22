> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Выполнение вызовов инструментов из кода с помощью Code Mode

> Попробуйте Code Mode — экспериментальную функцию, в которой Claude пишет JavaScript-код, выполняющий несколько вызовов инструментов за один шаг.

Code Mode меняет то, как Claude использует свои [инструменты](https://code.claude.com/docs/ru/tools-reference.md). Без Code Mode Claude запрашивает вызовы инструментов, таких как Bash, Read или Edit, напрямую и читает каждый результат, прежде чем решить, что делать дальше. С Code Mode Claude пишет фрагмент JavaScript-кода, который выполняет вызовы инструментов, а Claude Code запускает этот код в вашей сессии.

> [!NOTE]
>
> Code Mode — экспериментальная функция, по умолчанию отключённая. Она может измениться или быть удалена в любом релизе. Чтобы оставить отзыв, выполните `/feedback`.

## Как работает Code Mode

В сессии с Code Mode вы по-прежнему описываете задачу в промпте, а Claude пишет JavaScript-код для её выполнения. Один фрагмент кода может запускать команды параллельно, использовать один результат в следующем вызове и возвращать ту часть вывода, которую Claude нужно прочитать.

Например, если вы попросите Claude увеличить лимит повторных попыток, Claude может написать такой код, чтобы найти файл, отредактировать его и запустить тесты. Последняя строка возвращает Claude путь к файлу и вывод тестов:

```javascript theme={null}
const files = await $`rg -l "function retryPolicy" src`.text();
const target = files.trim().split("\n")[0];
await edit(target, "maxAttempts: 3", "maxAttempts: 5");
({ edited: target, tests: $`npm test -- retryPolicy`.nothrow() });
```

В диалоге вы видите вызовы инструментов, например diff правки, а не код. Чтобы прочитать код, нажмите `Ctrl+O` и откройте [просмотрщик транскрипта](https://code.claude.com/docs/ru/interactive-mode.md#transcript-viewer). Каждый фрагмент кода отображается там в виде свёрнутой строки **Code** с подсказкой, как её развернуть.

### Когда использовать Code Mode

Попробуйте Code Mode на задачах, требующих множества связанных вызовов инструментов, например:

* Изменение, которое повторяется во многих файлах
* Поиск, результаты которого нужно отфильтровать, прежде чем Claude их прочитает
* Несколько независимых команд, которые можно выполнять одновременно

### Ограничения Code Mode

Прежде чем включить Code Mode, убедитесь, что эти ограничения для вас приемлемы:

* **Возобновление**: сессию с Code Mode можно возобновить только в терминале и только с включённым Code Mode
* **Авторежим**: классификатор авторежима [проверяет код, а не каждый вызов инструмента](#permission-checks)
* **Долго выполняющийся код**: если код не может [выполняться в фоновом режиме](#long-running-code), вы ждёте его завершения, и он останавливается через десять минут
* **Хуки**: вы можете увидеть [отклонённые вызовы инструментов](#tool-call-refused-by-a-hook), когда хук `PreToolUse` не может запуститься или превышает таймаут, а также [вывод кода, заблокированный](#code-output-withheld-by-a-hook) хуком `UserPromptSubmit`
* **Недоступные функции**: вы не можете использовать [Remote Control](https://code.claude.com/docs/ru/remote-control.md), [Claude in Chrome](https://code.claude.com/docs/ru/chrome.md) или [computer use](https://code.claude.com/docs/ru/computer-use.md)
* **Перенос сессии**: вы не можете перенести сессию в приложение Desktop или превратить её в [фоновую сессию](https://code.claude.com/docs/ru/agent-view.md), а `/fork` не может запустить фоновую копию

## Требования

* **Версия**: Claude Code v2.1.323 или новее, на любом [канале релизов](https://code.claude.com/docs/ru/setup.md#configure-release-channel). Более старая версия запускается без Code Mode — с причиной `it isn't open to your account yet` или без неё
* **Аккаунт**: подписка Claude или аккаунт Console. Использовать Code Mode через шлюз, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry или [Claude Models on Google Cloud (Anthropic managed)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md) нельзя
* **Организация**: ваша организация не использует ни [конфигурацию HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md), ни [нулевое хранение данных](https://code.claude.com/docs/ru/zero-data-retention.md)
* **Модель**: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 или Fable 5.2
* **Интерфейс**: интерактивная сессия `claude` в терминале. Code Mode не работает с `-p`, Agent SDK, панелью VS Code, приложением Desktop и облачными сессиями
* **Команды агентов**: чтобы использовать Code Mode с включёнными [командами агентов](https://code.claude.com/docs/ru/agent-teams.md), вам нужна версия v2.1.326 или новее. Участники команды работают в Code Mode в [режиме отображения in-process](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), используемом по умолчанию, и запускаются без него в разделённых панелях
* **Установка**: [нативная сборка](https://code.claude.com/docs/ru/setup.md) Claude Code
* **Windows**: установлен [Git for Windows](https://git-scm.com/downloads/win)

Кроме того, Code Mode не запустится, если включены некоторые настройки, например вспомогательная программа для API-ключа, экспорт OpenTelemetry или `DISABLE_TELEMETRY`. Как исправить каждый из этих случаев, см. в разделе [Code Mode не запускается](#code-mode-doesnt-start).

## Попробуйте Code Mode

Включите Code Mode, дайте Claude задачу и посмотрите на код, который написал Claude.

**1. Проверьте версию**

Выполните `claude --version`. Если версия старше v2.1.323, выполните `claude update`. Если вы на канале `stable` и обновление не доходит до v2.1.323, подождите, пока `stable` догонит, или [переключитесь на `latest`](https://code.claude.com/docs/ru/setup#configure-release-channel).

**2. Запустите Claude Code с включённым Code Mode**

Установите для переменной окружения [`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`](https://code.claude.com/docs/ru/env-vars#variables) значение `1`. Чтобы попробовать Code Mode, задайте её в оболочке. Чтобы включить Code Mode для каждой новой сессии, задайте её в пользовательских настройках.

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1 claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> $env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"
> claude
> ```

> [tab] settings.json
>
> Сохраните этот блок `env` в `~/.claude/settings.json` и запустите `claude`:
>
> ```json theme={null}
> {
>   "env": {
>     "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "1"
>   }
> }
> ```
>
> Claude Code [игнорирует эту переменную в файлах настроек проекта](https://code.claude.com/docs/ru/settings-reference.md#variables-claude-code-ignores-in-env), поэтому клонированный вами репозиторий не может включить Code Mode за вас.

**3. Подтвердите, что хотите использовать Code Mode**

Перед вашей первой сессией с Code Mode Claude Code попросит подтверждения. Выберите **Yes, turn on Code Mode**. Claude Code перезапустится и покажет эту строку в верхней части сессии:

```text theme={null}
Code Mode (experimental) is on · this session can be resumed only with Code Mode on
```

Если вы видите другую строку или не видите никакой, см. раздел [Code Mode не запускается](#code-mode-doesnt-start).

**4. Дайте Claude задачу с множеством вызовов инструментов**

В знакомом вам проекте отправьте промпт, например такой:

```text theme={null}
Read every Markdown file in this project and list the links that point to local files that don't exist.
```

**5. Прочитайте код, написанный Claude**

Нажмите `Ctrl+O` и разверните строку **Code**, чтобы увидеть JavaScript-код, стоящий за вызовами инструментов. Нажмите `Ctrl+O` ещё раз, чтобы вернуться к диалогу.

> [!WARNING]
>
> Чтобы позже возобновить сессию с Code Mode, оставьте для `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` значение `1` при запуске `claude --continue` или `claude --resume`. При отключённом Code Mode Claude Code отказывается возобновлять такую сессию. Сессии, которые вы начали без Code Mode, возобновляются без Code Mode, даже если переменная задана.

### Отключение Code Mode

Удалите `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` из оболочки и из `~/.claude/settings.json`, а затем начните новую сессию. Также можно оставить переменную и изменить её значение на `0` в любом из этих мест. Если в одном месте задано `0`, Code Mode остаётся отключённым, даже если в другом вы задали `1`.

### Блокировка Code Mode для вашей организации

Добавьте `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` со значением `0` в [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md), чтобы никто в вашей организации не мог использовать Code Mode:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "0"
  }
}
```

Пользователи, находящиеся в сессии с Code Mode, остаются в ней, пока не выйдут из Claude Code или не перезапустят его. После этого ваши пользователи запускаются без Code Mode и не могут возобновить свои сессии с Code Mode, пока действует значение `0`. Включить Code Mode для пользователей через управляемые настройки нельзя.

## Разрешения и долго выполняющийся код

Ваш режим разрешений определяет, как проверяется код, который пишет Claude, и можете ли вы общаться с Claude, пока код выполняется.

### Проверки разрешений

Когда Claude выполняет код, каждый вызов инструмента в нём проходит через ваши [правила разрешений](https://code.claude.com/docs/ru/permissions.md) `deny` и `ask` и ваши [хуки `PreToolUse`](https://code.claude.com/docs/ru/hooks#pretooluse) под обычным именем инструмента, например `Bash`. Помимо правил и хуков, в авторежиме код проверяет классификатор, а в режимах, которые запрашивают подтверждение, вы отвечаете на запросы разрешений:

* **[Авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode)**: классификатор проверяет каждый фрагмент кода перед его запуском, а не каждый вызов инструмента. Он не видит значения, вычисляемые во время выполнения, например путь, взятый из вывода поиска, поэтому сохраняйте правила или хуки для вызовов, которые вы обязаны контролировать. Вы по-прежнему можете [получить запрос разрешения, когда новый код запускается, пока выполняется предыдущий](#permission-prompt-with-a-countdown)
* **Другие [режимы разрешений](https://code.claude.com/docs/ru/permission-modes.md)**: код запускается без проверки, а запрос разрешения появляется для каждого вызова инструмента, для которого он появился бы в этом режиме

Если у вас есть хук `PreToolUse`, который разрешает или блокирует shell-команды, сделайте так, чтобы он проверял каждую часть команды, как это [делают правила для Bash](https://code.claude.com/docs/ru/permissions.md#compound-commands). В Code Mode команда `git push` в папке с именем `app` может попасть в ваш хук как `cd 'app' && git push`.

Чтобы проверять сам код, напишите хук `PreToolUse`, который соответствует `REPL` — инструменту, выполняющему код, — и читайте JavaScript-код из `tool_input.code`.

> [!WARNING]
>
> Правила для Bash сопоставляются с текстом команды, поэтому Claude может выполнить запрещённую команду [в форме, которой правило не соответствует](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits), — с Code Mode или без него. Ограничения, не зависящие от текста команды, описаны в разделе об [изоляции в песочнице](https://code.claude.com/docs/ru/sandboxing.md).

### Долго выполняющийся код

Пока код выполняет долгую сборку или тест, Claude либо ждёт его, либо позволяет ему продолжаться в фоновом режиме:

* **Ожидание**: Claude отвечает после завершения кода, а код останавливается через десять минут, включая время, которое вы провели над запросами разрешений
* **Фоновый режим**: вы можете продолжать общаться с Claude, а код может выполняться до двух часов

Чтобы код выполнялся в фоновом режиме, начните сессию в авторежиме или в режиме `bypassPermissions`. Если Claude всё равно ждёт, проверьте текущий режим и то, как вы начали сессию:

* **Вы переключились на другой режим**: нажимайте `Shift+Tab`, пока не вернётесь в режим, в котором начали
* **Вы начали в другом режиме или выбрали сессию из списка `claude --resume`**: если [авторежим вам доступен](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), выйдите, а затем выполните `claude --continue --permission-mode auto` с включённым Code Mode
* **Вы передали имена инструментов в `--tools`**: начните заново в авторежиме без этого флага

## Устранение неполадок

### Code Mode не запускается

Строка `Code Mode (experimental) isn't available` в верхней части сессии означает, что Claude Code запустился без Code Mode. Причина указана в той же строке, и `/status` также её показывает. Найдите причину в этой таблице, внесите изменение и начните новую сессию. Если причины нет в списке, проверьте [требования](#requirements).

| Причина содержит | Что делать |
| :- | :- |
| `it isn't open to your account in this version` или `it isn't open to your account yet` | Если ваша версия старше v2.1.323, [обновитесь](#try-code-mode). В противном случае проверьте сетевое подключение и запустите заново. Если причина не исчезает, попробуйте ещё раз в другой день |
| `it only works directly with the Anthropic API` или `it only works with the Anthropic API` | Удалите настройки, которые направляют запросы через облачного провайдера, шлюз или пользовательский `ANTHROPIC_BASE_URL` |
| `it doesn't work with an API key helper` | Удалите `apiKeyHelper`, `ANTHROPIC_AUTH_TOKEN` и любые заголовки `Authorization` или `X-Api-Key` в `ANTHROPIC_CUSTOM_HEADERS`. Затем войдите в аккаунт или задайте `ANTHROPIC_API_KEY` |
| `it only works with Opus 5.5, Sonnet 5.5 and later models` | Запустите с [поддерживаемой моделью](#requirements), например с `--model opus`. Haiku 5.5 и Fable 5.2 также подходят |
| `it doesn't work in background jobs` | Запускайте на переднем плане, без `--remote-control`. Если причина отображается в разделённой панели участника команды, используйте [внутрипроцессный режим отображения](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), чтобы запускать участников команды в Code Mode |
| `it needs settings that Claude Code downloads from Anthropic` | Удалите переменную, которая [отключает получение флагов функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), например `DISABLE_TELEMETRY` |
| `OpenTelemetry is on` | Удалите `CLAUDE_CODE_ENABLE_TELEMETRY` и `ENABLE_BETA_TRACING_DETAILED`, если можете обойтись без [экспорта OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md) |
| `it doesn't yet work with the plugin` | В сессии выполните `/plugin` и отключите каждый плагин, который указан в причине. Если плагин включила ваша организация, попросите администратора отключить его |
| `it doesn't yet work with an installed mod` | Отключите [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md), который проверяет вызовы инструментов |
| `it can't be used together with agent teams yet` | Чтобы сохранить команды агентов включёнными, [обновите Claude Code](https://code.claude.com/docs/ru/setup.md#update-claude-code) до v2.1.326 или более поздней версии. Чтобы остаться на своей версии, удалите `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| `this launch's tool options` | Запускайте без `--restricted`, добавьте `REPL` в `--tools` и удалите `REPL` из `--disallowedTools` и ваших правил `deny` |
| `couldn't save your answer` | Сделайте `~/.claude.json` доступным для записи |
| `your organization's settings don't allow it` | Спросите администратора об [управляемой настройке](#block-code-mode-for-your-organization) |

Если вы не видите строки о Code Mode, выполните `claude --version`. Если ваша версия старше v2.1.323, обновитесь. Затем убедитесь, что `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` имеет значение `1` в вашей оболочке или пользовательских настройках, и удалите любое значение `0` оттуда и из любого файла `--settings`.

### Запрос разрешения с обратным отсчётом

Когда Claude в авторежиме запускает новый код, пока предыдущий код ещё выполняется, предыдущий код теряет проверку классификатором. Тогда Claude Code спрашивает вас об оставшихся вызовах предыдущего кода, которым потребовалась бы проверка. Если IDE не подключена, запрос показывает обратный отсчёт:

```text theme={null}
Claude Code will automatically block this request in 1:59, to avoid holding up an unattended session
```

Ответьте до окончания отсчёта. В противном случае этот вызов отклоняется, а последующие вызовы, для которых показывался бы обратный отсчёт, отклоняются без запроса. Чтобы снова видеть запросы, отправьте Claude сообщение.

### Tool call refused by a hook

Если Claude сообщает об отклонённом вызове инструмента, попросите его привести текст ошибки. Эти ошибки означают, что хук `PreToolUse` не вынес решения, и вызов отклоняется, даже если [`onFailure`](https://code.claude.com/docs/ru/hooks#block-the-action-when-a-hook-fails) не задан:

* **`the hook failed`**: при вызове из кода ваш хук не смог запуститься, был принудительно завершён, завершился с кодом 126, 127 или кодом выше 128 либо вернул HTTP-ошибку или некорректный вывод. Исправьте хук
* **`the hook did not finish`**: ваш хук превысил таймаут при вызове из кода или при любом другом вызове инструмента после того, как Claude выполнил код в сессии. Увеличьте [`timeout`](https://code.claude.com/docs/ru/hooks#common-fields) хука

Чтобы вызовы выполнялись, когда хук `command` или `http` завершается с ошибкой или превышает таймаут, задайте для него `"onFailure": "continue"`. Если хук `command` завершается с обычным кодом, например 1, вызов выполняется, если только вы не задали `"onFailure": "block"`.

### Вывод кода, задержанный хуком

Если Claude сообщает причину блокировки от хука там, где вы ожидали вывод кода, проверьте ваши хуки [`UserPromptSubmit`](https://code.claude.com/docs/ru/hooks#userpromptsubmit). Когда [код может выполняться в фоновом режиме](#long-running-code), хуки `command`, `http` и `mcp_tool` для этого события также запускаются для вывода кода. Чтобы пропустить вывод, измените хук так, чтобы он не блокировал, когда `source` в его входных данных равен `poll_event`.

## Связанные ресурсы

* [Режимы разрешений](https://code.claude.com/docs/ru/permission-modes.md): сравнение авторежима с режимами, которые запрашивают подтверждение
* [Справочник по хукам](https://code.claude.com/docs/ru/hooks.md): написание хуков `PreToolUse` и `UserPromptSubmit`
* [Управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md): применение единой конфигурации во всей организации
