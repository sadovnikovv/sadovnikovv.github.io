> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Запуск Claude Code программно

> Используйте Agent SDK для программного запуска Claude Code из CLI, Python или TypeScript.

[Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) предоставляет вам те же инструменты, цикл агента и управление контекстом, которые питают Claude Code. Он доступен как CLI для скриптов и CI/CD, или как пакеты [Python](https://code.claude.com/docs/ru/agent-sdk/python.md) и [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md) для полного программного управления.

Чтобы запустить Claude Code в неинтерактивном режиме, передайте `-p` с вашим запросом и [параметрами CLI](https://code.claude.com/docs/ru/cli-reference.md), которые вам нужны:

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

На этой странице рассматривается использование Agent SDK через CLI (`claude -p`). Для пакетов Python и TypeScript SDK со структурированными выходами, обратными вызовами одобрения инструментов и собственными объектами сообщений см. [полную документацию Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md).

## Базовое использование

Добавьте флаг `-p` (или `--print`) к любой команде `claude`, чтобы запустить её в неинтерактивном режиме. Не каждый [параметр CLI](https://code.claude.com/docs/ru/cli-reference.md) сочетается с `-p`. Claude Code отклоняет `--bg`, а также `--cloud` с описанием задачи, выдавая ошибку с указанием конфликта; `--cloud` с ID сессии и `-p` вместо этого [ставит сообщение в очередь этой облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md#send-follow-ups-from-the-cli) и завершает работу. Параметры, которые вы будете часто сочетать с `-p`, включают:

* `--continue` для [продолжения диалогов](#continue-conversations)
* `--allowedTools` для [автоматического подтверждения инструментов](#auto-approve-tools)
* `--output-format` для [структурированного вывода](#get-structured-output)

В этом примере Claude задаётся вопрос о вашей кодовой базе, а ответ выводится на экран:

```bash theme={null}
claude -p "What does the auth module do?"
```

Claude Code завершает работу с кодом 0 при успехе и с ненулевым кодом при сбое запуска, поэтому ваши скрипты могут ветвиться в зависимости от кода завершения. Если вы передадите недопустимый флаг, Claude Code сообщит об ошибке в stderr до начала запуска. Если сбой происходит во время запуска, например из-за отсутствия аутентификации, Claude Code выводит сбой как результат в stdout.

### Более быстрый запуск в режиме bare

Добавьте `--bare`, чтобы сократить время запуска за счёт пропуска автоматического обнаружения хуков, скиллов, пользовательских команд, [субагентов](https://code.claude.com/docs/ru/sub-agents.md), установленных плагинов, MCP-серверов, автоматической памяти и CLAUDE.md. Без этого флага `claude -p` обнаруживает и загружает их так же, как интерактивная сессия, включая всё, что настроено в рабочем каталоге или в `~/.claude`.

Режим bare полезен для CI и скриптов, где требуется одинаковый результат на каждой машине. Хук в `~/.claude` коллеги или MCP-сервер в `.mcp.json` проекта не будут запущены, потому что режим bare никогда их не читает. Каталог, указанный через `--add-dir`, является частичным исключением: режим bare загружает скиллы из его папки `.claude/skills/`, но по-прежнему пропускает его папки `.claude/commands/` и `.claude/agents/`. В разделе [Скиллы из дополнительных каталогов](https://code.claude.com/docs/ru/skills.md#skills-from-additional-directories) описано, что загружается, а что нет.

Без `--bare` сессия `-p` запускает хуки из `.claude/settings.json` проекта и подключает серверы из его `.mcp.json`, даже в папке, которой вы никогда не доверяли. Сессия `-p` не показывает диалоговое окно доверия рабочему пространству и не запрашивает подтверждение для каждого сервера. В разделе [Что запускается до того, как вы доверитесь папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) описан каждый вид содержимого репозитория при `-p` и то, как не допустить его загрузку.

В этом примере разовая задача составления сводки выполняется в режиме bare с предварительно разрешённым инструментом Read, чтобы вызов завершился без запроса разрешения. Перед запуском задайте `ANTHROPIC_API_KEY`, потому что режим bare не использует вход по подписке:

```bash theme={null}
claude --bare -p "Summarize README.md" --allowedTools "Read"
```

В режиме bare Claude Code никогда не читает учётные данные OAuth или системную связку ключей. Для Anthropic API задайте в окружении `ANTHROPIC_API_KEY` с ключом, созданным в [Claude Console](https://platform.claude.com), или укажите `apiKeyHelper` в JSON для `--settings`. Amazon Bedrock, Agent Platform от Google Cloud и Microsoft Foundry продолжают читать собственные учётные данные провайдера как обычно.

В режиме bare Claude имеет доступ к инструментам Bash, чтения файлов и редактирования файлов. Передайте необходимый контекст с помощью флага:

| Что загрузить | Что использовать |
| - | - |
| Дополнения к системному промпту | `--append-system-prompt`, `--append-system-prompt-file` |
| Настройки | `--settings <file-or-json>` |
| MCP-серверы | `--mcp-config <file-or-json>` |
| [Пользовательские агенты](https://code.claude.com/docs/ru/sub-agents.md#choose-the-subagent-scope) | `--agents <file-or-json>` |
| Плагин | `--plugin-dir <path>`, `--plugin-url <url>` |

Хуки по-прежнему не запускаются в режиме bare, если вы передаёте их через `--settings` или в [`hooks/hooks.json`](https://code.claude.com/docs/ru/plugins/components#hooks) либо [ключе манифеста `hooks`](https://code.claude.com/docs/ru/plugins/manifest-reference#hooks) плагина, загружаемого с помощью флага. Не используйте режим bare для запуска, которому они нужны.

Режим bare также ограничивает происходящее во время работы сессии:

* **MCP-серверы**: подключаются только серверы, переданные в командной строке, например с помощью `--mcp-config`. В интерактивной сессии Claude Code также пропускает автоматическое подключение к IDE, если вы не передадите `--ide`.
* **Системные напоминания**: Claude получает ваши промпты и результаты инструментов без [системных напоминаний](https://code.claude.com/docs/ru/glossary.md#system-reminder), которые Claude Code добавил бы к ним. Например, Claude не сообщается, когда файл, отредактированный им ранее, изменяется на диске, и он не получает список доступных скиллов, включая скиллы из папки `--add-dir`.
* **Фоновые задачи**: Claude не может запускать фоновые команды или фоновых субагентов, а другие функции, которые отключает [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](https://code.claude.com/docs/ru/env-vars), тоже отключены. Команда, достигшая своего [таймаута](https://code.claude.com/docs/ru/tools-reference.md#timeout-and-output-limits), останавливается, а не [переходит в фоновый режим](https://code.claude.com/docs/ru/tools-reference.md#background-commands).

До v2.1.286 эти ограничения действовали лишь частично: интерактивная сессия `--bare` подключала те же MCP-серверы, что и обычная сессия, каждая сессия `--bare` отправляла системные напоминания, а фоновые задачи оставались доступными.

> [!NOTE]
>
> `--bare` — рекомендуемый режим для вызовов из скриптов и SDK, и в будущем выпуске он станет режимом по умолчанию для `-p`.

### Фоновые задачи при завершении

После того как Claude завершает свой ход и stdin закрывается, запуск `claude -p` может оставаться открытым, ожидая фоновую работу, которую начал Claude.

Если только не выполняется фоновая команда, запущенная основным диалогом, по умолчанию Claude Code останавливает всё, что ещё выполняется, после 10 минут непрерывного ожидания в простое и отбрасывает частичный результат. Чтобы изменить 10-минутный предел, задайте [`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`](https://code.claude.com/docs/ru/env-vars) или установите значение `0`, чтобы ждать без предела.

Запуск ожидает фоновую работу, такую как фоновые команды, субагенты и workflow, наблюдения Monitor и ожидающие пробуждения `/loop`:

* **[Фоновые команды](https://code.claude.com/docs/ru/tools-reference.md#background-commands)**: для команды, запущенной основным диалогом, например dev-сервера или сборки в режиме наблюдения, запуск ждёт, пока команда не завершится или не достигнет своего [ограничения по времени](https://code.claude.com/docs/ru/tools-reference.md#time-limit-for-background-commands). Затем Claude делает ещё один ход с результатом. Пока команда выполняется, 10-минутный предел не прерывает ожидание.
* **Фоновые [субагенты](https://code.claude.com/docs/ru/sub-agents.md) и workflow**: запуск остаётся открытым, пока каждый из них не завершится или пока 10-минутный предел не прервёт ожидание.
* **Наблюдения [Monitor](https://code.claude.com/docs/ru/tools-reference.md#monitor-tool)**: запуск ждёт, пока у наблюдения не истечёт таймаут или пока 10-минутный предел не прервёт ожидание — в зависимости от того, что наступит раньше. Во время ожидания Claude продолжает реагировать на то, что сообщает наблюдение. По умолчанию таймаут наблюдения истекает через пять минут после того, как Claude его запускает.
* **Ожидающие пробуждения**: в запуске, промпт которого вы передали как текст, а не через `--input-format stream-json`, если Claude запланировал [пробуждение `/loop` в собственном темпе](https://code.claude.com/docs/ru/scheduled-tasks#let-claude-choose-the-interval), запуск ждёт срабатывания каждого пробуждения и выполняет его итерацию, пока [цикл не завершится](https://code.claude.com/docs/ru/scheduled-tasks.md#stop-a-loop), даже после истечения 10-минутного предела.

Когда stderr является терминалом и запуск ожидает уже пять секунд, Claude Code выводит в stderr строку, которая начинается с `Waiting for background work to finish` и называет ожидаемую работу. При [выводе `json` или `stream-json`](#get-structured-output) эта строка выводится только тогда, когда stdout не является терминалом, поэтому JSON, который читает ваш скрипт, никогда её не содержит.

Если запуск достигает предела [`--max-budget-usd`](https://code.claude.com/docs/ru/cli-reference#cli-flags), Claude Code останавливает оставшуюся фоновую работу вместо ожидания.

Когда фоновая работа запускает ещё один ход, запуск выводит результат каждого хода при выводе по умолчанию `text` и результат последнего хода при выводе `json`. До v2.1.295 при выводе `text` запуск тоже выводил только результат последнего хода.

#### Дайте длительной команде субагента больше времени

Когда длительная команда субагента [переходит в фоновый режим](https://code.claude.com/docs/ru/tools-reference.md#foreground-commands-that-move-to-the-background) по истечении таймаута, запуск `claude -p` может завершиться с кодом 0 до того, как команда завершится.

Чтобы увеличить таймаут по умолчанию сверх времени выполнения команды, задайте [`BASH_DEFAULT_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars), например `BASH_DEFAULT_TIMEOUT_MS=300000 claude -p "<prompt>"` для пяти минут. Для команды фонового субагента, выполняющейся дольше 10 минут, также увеличьте [10-минутный предел](#background-tasks-at-exit).

#### Работа MCP при завершении неинтерактивного запуска

Запуск `claude -p` не ожидает работу MCP в фоновом режиме:

* **[Задачи MCP](https://code.claude.com/docs/ru/mcp.md#mcp-tasks-that-run-on-the-server)**: на удалённом сервере задание продолжает выполняться. Чтобы снова отслеживать его, [возобновите эту сессию](https://code.claude.com/docs/ru/mcp.md#exit-clear-or-resume-while-an-mcp-task-runs), а не запускайте разовый `claude -p "<prompt>"`.
* **Вызовы MCP, перемещённые [автоматическим переводом в фон](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls)**: результат вызова теряется.

### Остановка запуска с помощью SIGTERM

Если вы останавливаете запуск `claude -p` с помощью SIGTERM, например через `kill` или из супервизора процессов, Claude Code завершает работу с кодом 143. Claude Code оставляет выполнявшийся ход незавершённым и не записывает для него результат. Чтобы вместо этого завершить ход, отправьте SIGINT или вызовите `interrupt()` из Agent SDK перед остановкой процесса.

При получении SIGTERM Claude Code завершает дерево процессов любой ещё выполняющейся команды Bash. Затем Claude Code запускает [хуки `SessionEnd`](https://code.claude.com/docs/ru/hooks#sessionend) и завершает работу. Во время завершения Claude Code не начинает новых вызовов инструментов, не отправляет новых запросов к модели и не запускает никаких хуков, кроме `SessionEnd`. Если в момент поступления сигнала запуск выполнял команду или ожидал ответа на запрос разрешения, Claude Code обрабатывает этот шаг следующим образом:

* **Выполнение команды**: Claude Code записывает команду в сессии как принудительно завершённую.
* **Ожидание ответа на запрос разрешения**: если вы отправляете процессу SIGTERM, Claude Code оставляет запрос без ответа. Если ваша программа закрывает сессию через Agent SDK, SDK завершает ввод Claude Code до отправки какого-либо сигнала, и Claude Code отменяет запрос, как только ввод завершается.

Когда вы [возобновляете сессию](#continue-conversations), Claude Code оставляет прерванный ход как есть, и диалог направляет ваш следующий промпт. Чтобы вместо этого Claude Code продолжал прерванный ход при возобновлении, задайте [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1`](https://code.claude.com/docs/ru/env-vars).

### Если рабочий каталог удалён

Если рабочий каталог сессии `claude -p` или Agent SDK удаляется во время сессии, сессия продолжает работать. Когда ход начинается в отсутствие каталога, Claude Code выдаёт [предупреждающее сообщение](https://code.claude.com/docs/ru/agent-sdk/typescript.md#sdkinformationalmessage) в выводе `stream-json`, а shell-команды завершаются с ошибкой, пока каталог снова не появится.

## Примеры

Эти примеры демонстрируют распространённые паттерны CLI. Если команда указывает файл, например `auth.py` или `build-error.txt`, замените его файлом из вашего проекта. В CI или других скриптовых окружениях добавьте [`--bare`](#start-faster-with-bare-mode), чтобы Claude Code запустился без загрузки хуков, плагинов, автоматической памяти или `CLAUDE.md` хоста.

### Передача данных через Claude

Неинтерактивный режим читает stdin, поэтому вы можете передавать данные на вход и перенаправлять ответ на выход.

Этот пример передаёт лог сборки в Claude и записывает объяснение в файл:

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

С `--output-format json` данные ответа включают `total_cost_usd` и разбивку затрат по моделям, поэтому вызывающие скрипты могут отслеживать расходы без обращения к [панели использования](https://code.claude.com/docs/ru/costs.md). Когда вы продолжаете более ранний диалог с `--continue` или `--resume`, запуск сообщает общую сумму диалога, [включая расходы более ранних запусков](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#accumulate-costs-across-multiple-calls). Обе цифры являются [оценками на стороне клиента](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md) и могут отличаться от вашего фактического счёта.

> [!NOTE]
>
> Данные, передаваемые через stdin, ограничены 10 МБ. Если вы превысите лимит, Claude Code завершится с понятной ошибкой и ненулевым статусом. Для работы с большими входными данными запишите содержимое в файл и укажите путь к файлу в вашем промпте вместо передачи данных через pipe.

Если Claude Code не может прочитать stdin, например потому что процесс, который его запустил, отключил свой конец, Claude Code выводит предупреждение в stderr и продолжает работу с промптом из командной строки.

### Добавление Claude в скрипт сборки

Вы можете обернуть неинтерактивный вызов в скрипт, чтобы использовать Claude как линтер или рецензента для конкретного проекта.

Этот скрипт `package.json` передаёт diff относительно `main` в Claude и просит его сообщить об опечатках. Передача diff означает, что Claude не нужно разрешение Bash для его чтения, а экранированные двойные кавычки делают скрипт переносимым на Windows:

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

Запустите его с помощью `npm run lint:claude`.

### Получение структурированного вывода

Используйте `--output-format` для управления тем, как возвращаются ответы:

* `text` (по умолчанию): простой текстовый вывод
* `json`: структурированный JSON с результатом, ID сессии и метаданными
* `stream-json`: JSON с разделением по строкам для потоковой передачи в реальном времени

Этот пример возвращает сводку проекта в виде JSON с метаданными сессии, с текстовым результатом в поле `result`:

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

Чтобы получить вывод, соответствующий определённой схеме, используйте `--output-format json` с `--json-schema` и определением [JSON Schema](https://json-schema.org/). Ответ включает метаданные о запросе (ID сессии, использование и т. д.) со структурированным выводом в поле `structured_output`.

Этот пример извлекает имена функций и возвращает их как массив строк:

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Если значение не является допустимой JSON Schema, `claude` завершается с `Error: --json-schema is not a valid JSON Schema`, за которым следует диагностика валидатора. Claude Code принимает схемы, использующие ключевое слово `format`, такие как `"format": "email"`, но рассматривает `format` как аннотацию и не применяет его.

Если запуск завершается без допустимого структурированного вывода, например потому что Claude отклонил запрос, в ответе нет поля `structured_output`. Прежде чем ваш скрипт будет использовать `structured_output`, проверьте, что это поле присутствует.

> [!TIP]
>
> Используйте инструмент, такой как [jq](https://jqlang.org/), для разбора ответа и извлечения определённых полей:
>
> ```bash theme={null}
> # Extract the text result
> claude -p "Summarize this project" --output-format json | jq -r '.result'
>
> # Extract structured output
> claude -p "Extract function names from auth.py" \
>   --output-format json \
>   --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
>   | jq '.structured_output'
> ```

### Потоковая передача ответов

Используйте `--output-format stream-json` с `--verbose` и `--include-partial-messages` для получения токенов по мере их генерации. Каждая строка — это объект JSON, представляющий событие:

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

Последняя строка потока — это сообщение `result` с итоговым текстом ответа, стоимостью и метаданными сессии.

Если ваш потребитель читает поток медленно, Claude Code перед завершением ждёт, пока очередь вывода опустеет, масштабируя ожидание в зависимости от того, сколько ещё осталось в очереди, максимум 30 секунд.

Следующий пример использует [jq](https://jqlang.org/) для фильтрации текстовых дельт и отображения только потокового текста. Флаг `-r` выводит необработанные строки (без кавычек), а `-j` объединяет их без переводов строк, поэтому токены выводятся непрерывно:

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Для программной потоковой передачи с обратными вызовами и объектами сообщений см. [Потоковая передача ответов в реальном времени](https://code.claude.com/docs/ru/agent-sdk/streaming-output.md) в документации Agent SDK.

#### Отслеживание сообщений субагентов

Сообщения от [субагентов](https://code.claude.com/docs/ru/sub-agents.md) и от скиллов, которые [работают в субагенте](https://code.claude.com/docs/ru/skills.md#run-skills-in-a-subagent), появляются в потоке как сообщения `assistant` и `user`. Их поле `parent_tool_use_id` указывает, к какому запуску относится каждое из них. Сообщения из основного диалога содержат `null` в этом поле.

Первое сообщение от разветвлённого скилла или от субагента, работающего на [переднем плане](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background), — это сообщение `user`, содержащее промпт или содержимое скилла, которое им управляет. После этого первого сообщения Claude Code выдаёт:

* **По умолчанию**: блоки `tool_use` и `tool_result` запуска.
* **С [`--forward-subagent-text`](https://code.claude.com/docs/ru/cli-reference#cli-flags) или [`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`](https://code.claude.com/docs/ru/env-vars)**: также текстовые блоки и блоки размышлений запуска, чтобы вы могли восстановить транскрипт каждого запуска.

Когда вы включаете любой из этих параметров, Claude Code пересылает сообщения от [субагентов на каждом уровне вложенности](https://code.claude.com/docs/ru/sub-agents.md#let-subagents-spawn-their-own-subagents), независимо от того, был ли каждый из них порождён инструментом Agent или запущен как разветвлённый скилл. В `parent_tool_use_id` сообщения вложенного субагента содержат ID вызова инструмента Agent или Skill, который его запустил, поэтому вы можете перестроить полное дерево вложенности, следуя этим ID.

Запуск, который Claude начинает вызовом инструмента, содержит ID этого вызова инструмента. У разветвлённого скилла, который вы запускаете, передавая `/<skill-name>` в качестве промпта, нет вызова инструмента, поэтому его сообщения вместо этого содержат значение `forked-command-` и поступают после его завершения. Найдите способ запуска в первом столбце:

| Как начинается запуск | `parent_tool_use_id` | Когда поступают его сообщения |
| :- | :- | :- |
| Claude вызывает инструмент Agent из основного диалога | ID этого блока `tool_use` инструмента Agent | Пока субагент работает |
| Claude вызывает инструмент Skill для разветвлённого скилла из основного диалога | ID этого блока `tool_use` инструмента Skill | Пока разветвлённый скилл работает |
| Вы передаёте `/<skill-name>` в качестве промпта | Значение, начинающееся с `forked-command-` | Вместе и по порядку после завершения разветвлённого скилла |

Для разветвлённого скилла, запущенного из промпта, сопоставляйте `parent_tool_use_id` по префиксу `forked-command-`, потому что имя после него может отличаться от того, которое вы ввели.

Если каких-то из этих сообщений нет в вашем потоке, сверьте версию Claude Code с этими минимальными требованиями:

* **Разветвлённый скилл, который Claude запускает инструментом Skill из основного диалога**: версия 2.1.86 или новее для его блоков `tool_use` и `tool_result` и версия 2.1.265 или новее для его первого сообщения `user`, а также текстовых блоков и блоков размышлений
* **Сообщения субагентов, которых порождает разветвлённый скилл, и разветвлённых скиллов, запущенных внутри субагента или другого разветвлённого скилла**: версия 2.1.275 или новее
* **Сообщения разветвлённого скилла, который вы запускаете, передавая `/<skill-name>` в качестве промпта**: версия 2.1.287 или новее

#### Обработка повторных попыток API

Когда запрос к API завершается ошибкой, допускающей повторную попытку, Claude Code выдаёт событие `system/api_retry` перед повторной попыткой. В версии 2.1.246 или новее, когда `401` или `403` отклоняет учётные данные [`apiKeyHelper`](https://code.claude.com/docs/ru/settings-reference#apikeyhelper), Claude Code делает первые две повторные попытки молча, без события, а начиная с третьей последовательной повторной попытки выдаёт событие как обычно. Молчаливые повторные попытки всё равно учитываются в `attempt`. Вы можете использовать событие для отображения хода повторных попыток в вашем собственном интерфейсе.

| Поле | Тип | Описание |
| - | - | - |
| `type` | `"system"` | тип сообщения |
| `subtype` | `"api_retry"` | идентифицирует это как событие повторной попытки |
| `attempt` | целое число | номер текущей попытки, начиная с 1 |
| `max_retries` | целое число | общее число повторных попыток, разрешённых для причины этого сбоя |
| `retry_delay_ms` | целое число | миллисекунды до следующей попытки |
| `error_status` | целое число или null | код состояния HTTP неудачной попытки или `null`, когда попытка не получила HTTP-ответ от API |
| `no_response` | объект, опционально | присутствует, только когда неудачная попытка [не получила заголовки ответа вовремя](https://code.claude.com/docs/ru/errors.md#no-response-from-api). `waited_ms` — это время ожидания этой попытки, а `retry_wait_ms` — время ожидания повторной попытки. Требует Claude Code версии 2.1.261 или новее |
| `error` | строка | категория ошибки: `authentication_failed`, `oauth_org_not_allowed`, `account_on_hold`, `billing_error`, `rate_limit`, `overloaded`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `cloud_credential_error` или `unknown` |
| `uuid` | строка | уникальный идентификатор события |
| `session_id` | строка | сессия, к которой относится событие |

#### Чтение метаданных сессии

Событие `system/init` сообщает метаданные сессии, включая модель, инструменты, MCP-серверы и загруженные плагины. Это первое событие в потоке, если ему не предшествуют события запуска:

* События `plugin_install`, когда задана [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](https://code.claude.com/docs/ru/env-vars).
* [События `hook_started`, `hook_progress` и `hook_response`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkhookstartedmessage), пока выполняется настроенный хук [`SessionStart`](https://code.claude.com/docs/ru/hooks#sessionstart) или [`Setup`](https://code.claude.com/docs/ru/hooks#setup). Они передаются в потоке по мере их создания хуком.

Событие также содержит опциональный массив строк `capabilities`, называющих поведения протокола, которые реализует эта версия Claude Code, такие как `interrupt_receipt_v1` или `interrupt_cancel_queued_v1`. Проверяйте его для обнаружения возможностей вместо сравнения строк версий и игнорируйте значения, которые вы не распознаёте. См. [`SDKSystemMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdksystemmessage) для списка возможностей.

#### Сбой CI, когда плагин или MCP-сервер не загружается

Используйте поля плагинов в событии `system/init`, чтобы обнаружить плагин, который не загрузился:

| Поле | Тип | Описание |
| - | - | - |
| `plugins` | массив | плагины, которые успешно загрузились, каждый с `name` и `path` |
| `plugin_errors` | массив | ошибки загрузки плагинов, каждая с `plugin`, `type` и `message`. Включает неудовлетворённые версии зависимостей и ошибки загрузки `--plugin-dir`, такие как отсутствующий путь или недопустимый архив. Плагин, который не загрузился, отсутствует в `plugins`. Ключ опускается, когда ошибок нет |

Когда не удаётся загрузить сам каталог или архив `--plugin-dir`, его запись `plugin_errors` включает разрешённый абсолютный путь в виде `path`. Используйте его, чтобы определить, какое из нескольких значений `--plugin-dir` не загрузилось. Поле `path` требует Claude Code версии 2.1.283 или новее.

Используйте поля MCP-серверов так же. Когда вы передаёте [`--mcp-config`](https://code.claude.com/docs/ru/cli-reference#cli-flags) с `-p`, Claude Code перед первым ходом ждёт серверы, которые ещё подключаются, в пределах таймаута запуска [`MCP_TIMEOUT`](https://code.claude.com/docs/ru/env-vars), по умолчанию 30 секунд. Удалённый сервер с [кэшированным списком инструментов](https://code.claude.com/docs/ru/agent-sdk/mcp.md#connection-timing) пропускает ожидание, показывает `pending` в `system/init` и подключается при первом вызове инструмента. В [самостоятельно размещённом окружении](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#connection-timing) вместо этого применяется более короткое ожидание. Ожидание требует Claude Code версии 2.1.221 или новее.

Claude Code проверяет каждую запись `--mcp-config` при запуске и пропускает записи, которые не прошли проверку, например запись `url` без `type`. Запуск продолжается и завершается без ошибок, поэтому проверяйте эти поля, чтобы обнаружить сервер, который так и не загрузился:

| Поле | Тип | Описание |
| - | - | - |
| `mcp_servers` | массив | MCP-серверы в сессии, каждый с `name` и `status` |
| `mcp_server_errors` | массив | записи `--mcp-config`, пропущенные при проверке конфигурации, каждая с `name`, `type` и `message`. `type` — это категория пропуска, такая как `unknown_type`, `url_missing_type`, `invalid_config` или `reserved_name`; рассматривайте значения, которые вы не распознаёте, как общий пропуск. Затронутые серверы отсутствуют в `mcp_servers`. Ключ опускается, когда ошибок нет, поэтому проверка в CI может завершаться сбоем при непустом массиве |

Когда вы запускаете команду вручную в терминале, Claude Code также выводит в stderr предупреждение при запуске, например `Warning: 1 MCP server skipped due to invalid config:`, за которым следует причина для каждой пропущенной записи.

Когда вы перенаправляете stderr или когда его перехватывает программа, такая как CI runner или хост SDK, Claude Code не выводит предупреждение. Он сообщает о пропущенных записях только в поле `mcp_server_errors`.

#### Отслеживание установки плагинов

Когда задана [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](https://code.claude.com/docs/ru/env-vars), Claude Code выдаёт события `system/plugin_install` во время установки плагинов из маркетплейсов перед первым ходом. Используйте их для отображения хода установки в вашем собственном UI.

| Поле | Тип | Описание |
| - | - | - |
| `type` | `"system"` | тип сообщения |
| `subtype` | `"plugin_install"` | идентифицирует это как событие установки плагина |
| `status` | `"started"`, `"installed"`, `"failed"` или `"completed"` | `started` и `completed` обрамляют всю установку; `installed` и `failed` сообщают об отдельных маркетплейсах |
| `name` | строка, опционально | имя маркетплейса, присутствует в `installed` и `failed` |
| `error` | строка, опционально | сообщение об ошибке, присутствует в `failed` |
| `uuid` | строка | уникальный идентификатор события |
| `session_id` | строка | сессия, к которой относится событие |

### Автоматическое подтверждение инструментов

Используйте `--allowedTools`, чтобы разрешить Claude использовать определённые инструменты без запроса. Перечисление `Read` и `Edit` позволяет Claude читать и редактировать файлы без запроса разрешения, кроме чтения по [сетевым путям](https://code.claude.com/docs/ru/permissions.md#network-paths). Перечисление `Bash` делает то же самое для shell-команд, за исключением запуска, который начинается в [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#how-auto-mode-evaluates-actions): там Claude Code отбрасывает голую запись `Bash` как слишком широкое разрешающее правило, и вместо этого авторежим оценивает каждую команду. Этот пример запускает набор тестов и исправляет сбои, указав эти три инструмента:

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

Вызовы инструментов, которые вы не перечислили, выполняются, если они не требуют подтверждения. В запуске `claude -p` в [режиме Manual](https://code.claude.com/docs/ru/permission-modes.md#available-modes) вызов, требующий подтверждения, отклоняется, если его ничто не подтверждает, например [хук `PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest) или [`--permission-prompt-tool`](https://code.claude.com/docs/ru/cli-reference#cli-flags). В Claude Code версии 2.1.302 или новее запуски `claude -p` начинаются в режиме Manual, когда [режим разрешений ничем не задан](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-non-interactive-run-starts-in).

Чтобы задать базовый уровень для всей сессии вместо перечисления отдельных инструментов, передайте [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) с помощью `--permission-mode`, например `auto`, `dontAsk` или `acceptEdits`:

* **`auto`**: передайте `--permission-mode auto`, чтобы большинство действий проверял классификатор вместо вас
* **`dontAsk`**: Claude Code отклоняет каждый вызов, который иначе вызвал бы запрос, что полезно для строго ограниченных запусков в CI, хотя установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) всё же может подтверждать некоторые из этих вызовов. Чтобы узнать, какие вызовы может подтверждать мод, см. [Расширение разрешений с помощью хуков](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

  Действия, не требующие подтверждения в режиме Manual, по-прежнему выполняются, например чтение файлов в ваших рабочих каталогах и [набор команд только для чтения](https://code.claude.com/docs/ru/permissions.md#read-only-commands). Действия, охваченные вашими записями `--allowedTools` или правилами `permissions.allow`, также выполняются. `AskUserQuestion`, инструменты коннекторов, [для которых ваша организация установила `ask`](https://code.claude.com/docs/ru/mcp#organization-controls-on-connector-tools), MCP-инструменты, помеченные [`requiresUserInteraction`](https://code.claude.com/docs/ru/mcp#require-approval-for-a-specific-tool), и [чтение по сетевым путям](https://code.claude.com/docs/ru/permissions.md#network-paths) отклоняются, даже когда совпадает разрешающее правило
* **`acceptEdits`**: Claude записывает файлы без запроса, и Claude Code автоматически подтверждает распространённые команды файловой системы, такие как `mkdir`, `touch`, `mv` и `cp`. [Действия, которые ни один режим не подтверждает автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves), по-прежнему действуют. Помимо набора команд только для чтения, другие shell-команды и сетевые запросы по-прежнему требуют записи `--allowedTools` или правила `permissions.allow`. См. [что `acceptEdits` подтверждает автоматически](https://code.claude.com/docs/ru/permission-modes#auto-approve-file-edits-with-acceptedits-mode) для полного списка

Этот пример применяет исправления линтера с `acceptEdits` в качестве базового уровня:

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### Отключение запросов разрешений в автоматических запусках

Передайте `--permission-prompts none`, когда отвечать на запросы разрешений некому, например в запланированном задании. Флаг важнее всего, когда у вашего запуска есть хост разрешений: приложение Agent SDK с [обратным вызовом `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) или MCP-инструмент, который вы передаёте с [`--permission-prompt-tool`](https://code.claude.com/docs/ru/cli-reference#cli-flags). Без этого флага или настройки [`permissions.denyInsteadOfPrompting`](https://code.claude.com/docs/ru/settings-reference#permissions-denyinsteadofprompting) ваш запуск ждёт, пока этот хост ответит на каждый запрос разрешения.

С флагом ваш запуск не обращается к хосту и не ждёт его. Всё, что вызвало бы запрос, отклоняется, если это не разрешает хук `PermissionRequest`; Claude сообщается, что подтвердить запрос некому и что повторять попытку не нужно, и запуск продолжается. В запуске `-p` без хоста эти запросы отклоняются в любом случае, а флаг дополнительно сообщает Claude не повторять их. Правила разрешений, [хуки `PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest) и заданный вами режим разрешений по-прежнему решают судьбу каждого вызова в первую очередь; Claude Code отклоняет только те запросы, которые ничто другое не разрешает.

> [!NOTE]
>
> Флаг `--permission-prompts none` действует в течение одного запуска. Чтобы отклонять вызовы, которые ждали бы ответа на запрос разрешения, и в последующих запусках, установите для [`permissions.denyInsteadOfPrompting`](https://code.claude.com/docs/ru/settings-reference#permissions-denyinsteadofprompting) значение `true` в ваших пользовательских или управляемых настройках.

Этот пример выполняет автоматическое задание в [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode). Классификатор проверяет каждое действие как обычно, а Claude Code отклоняет всё, что иначе привело бы к запросу:

```bash theme={null}
claude -p "Update the dependency pins and run the tests" --permission-mode auto --permission-prompts none
```

С `--permission-prompts none` Claude Code удаляет инструменты, которым нужен ответ от человека, такие как [`AskUserQuestion`](https://code.claude.com/docs/ru/tools-reference#askuserquestion-tool-behavior), поэтому Claude не может их вызвать. Любой [запрос MCP elicitation](https://code.claude.com/docs/ru/mcp.md#respond-to-mcp-elicitation-requests), на который не отвечает ни один [хук `Elicitation`](https://code.claude.com/docs/ru/hooks#elicitation), отменяется.

С `--output-format stream-json` отклонения появляются как системные сообщения `permission_denied`, а итоговое сообщение результата перечисляет их в `permission_denials`.

> [!NOTE]
>
> Флаг `--permission-prompts` требует Claude Code версии 2.1.259 или новее. Более ранние версии отклоняют его с ошибкой неизвестного параметра.

### Создание коммита

Этот пример просматривает проиндексированные изменения и создаёт коммит с подходящим сообщением:

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Флаг `--allowedTools` использует [синтаксис правил разрешений](https://code.claude.com/docs/ru/settings-reference.md#permission-rule-syntax). Благодаря завершающему ` *` правило `Bash(git diff *)` совпадает с `git diff` как с аргументами, так и без них. Пробел перед `*` важен: без него `Bash(git diff*)` также совпадал бы с `git diff-index`.

> [!NOTE]
>
> Поддержка команд в режиме `-p` отличается:
>
> * Вызываемые пользователем [скиллы](https://code.claude.com/docs/ru/skills.md) и пользовательские команды работают. Включите `/skill-name` в строку промпта, и Claude Code развернёт её перед запуском.
> * Встроенные команды, которые работают только в интерфейсе терминала, такие как `/login`, недоступны.
> * `/model`, `/effort`, `/fast`, `/color` и `/rename` принимают значение как аргумент, например `/model sonnet`, а `/mcp` без аргумента выводит текстовую сводку состояния серверов. Эти формы следуют [примечаниям о доступности](https://code.claude.com/docs/ru/commands.md#all-commands) каждой команды.
> * Чтобы изменить настройку, передайте `key=value` в `/config`, например `/config verbose=true`.
> * `/output-style <style>` переключает [стили вывода](https://code.claude.com/docs/ru/output-styles.md), а `/output-style` без аргумента выводит их список. Требует Claude Code версии 2.1.269 или новее.

### Настройка системного промпта

Используйте `--append-system-prompt`, чтобы добавить инструкции, сохранив поведение Claude Code по умолчанию. Этот пример передаёт diff PR в Claude и поручает ему проверить код на уязвимости безопасности. Сохраните его как shell-скрипт, например `review.sh`:

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

В скрипте `"$1"` обозначает первый аргумент, который вы передаёте в командной строке. Запустите `bash review.sh 123`, и оболочка заменит `"$1"` на `123`, поэтому скрипт получит diff для PR 123. Claude Code выводит рецензию в виде JSON, с текстом в поле `result`.

См. [флаги системного промпта](https://code.claude.com/docs/ru/cli-reference.md#system-prompt-flags) для дополнительных параметров, включая `--system-prompt` для полной замены промпта по умолчанию. Если вы заменяете его, запуск также начинается без [снимка состояния git](https://code.claude.com/docs/ru/settings-reference.md#includegitinstructions).

### Продолжение диалогов

Используйте `--continue` для продолжения самого последнего диалога или `--resume` с ID сессии для продолжения определённого диалога. В Claude Code версии 2.1.257 или новее при передаче `--continue` Claude Code открывает [фоновую сессию](https://code.claude.com/docs/ru/sessions.md#where-the-session-picker-looks), которая завершилась, но не ту, которая ещё выполняется. Этот пример запускает рецензию, а затем отправляет последующие промпты:

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Если вы ведёте несколько диалогов, сохраните ID сессии, чтобы возобновить определённый:

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

Вы можете запускать эти две команды из разных каталогов: Claude Code [находит сессию по её ID](https://code.claude.com/docs/ru/sessions.md#where-the-session-picker-looks) в любом проекте на этой машине.

Вместо ID сессии вы можете передать `--resume` абсолютный путь к [файлу транскрипта](https://code.claude.com/docs/ru/sessions.md#where-transcripts-are-stored) `.jsonl` сессии, и Claude Code продолжит диалог, сохранённый в этом файле.

## Следующие шаги

* [Agent SDK quickstart](https://code.claude.com/docs/ru/agent-sdk/quickstart.md): создайте своего первого агента с помощью Python или TypeScript
* [CLI reference](https://code.claude.com/docs/ru/cli-reference.md): все флаги и параметры CLI
* [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md): используйте Agent SDK в рабочих процессах GitHub
* [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md): используйте Agent SDK в конвейерах GitLab
