> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Устранение неполадок Agent SDK

> Исправьте ошибки Agent SDK: Claude Code CLI не запускается или завершается, ваш генератор промптов выбрасывает исключение, сообщение инструмента слишком велико или результат приходит без структурированного вывода.

Эта страница охватывает ошибки Agent SDK при запуске CLI, выходе процесса CLI, крупных вызовах инструментов и результатах, потоковом вводе и структурированных выводах. Записи на этой странице соответствуют ошибке, которую вы видите. Каждая указывает причину и что делать.

Симптомы, связанные с функцией, такие как несрабатывающий хук или неиспользуемый скилл, имеют раздел устранения неполадок на странице этой функции. Найдите свой симптом в этой таблице, чтобы перейти к разделу или странице, которые его охватывают:

| Симптом | Перейти к |
| :- | :- |
| Скиллы не найдены, скилл не используется, ошибка `Invalid skill name` | [Устранение неполадок скиллов](https://code.claude.com/docs/ru/agent-sdk/skills.md#troubleshooting) |
| MCP-сервер показывает статус `failed`, инструменты не вызываются, инструмент отсутствует в MCP-сервере SDK, таймауты соединения, вывод инструмента превышает максимально допустимое количество токенов | [Устранение неполадок MCP](https://code.claude.com/docs/ru/agent-sdk/mcp.md#troubleshooting) |
| Плагин не загружается, скиллы плагина не отображаются | [Устранение неполадок плагинов](https://code.claude.com/docs/ru/agent-sdk/plugins.md#troubleshooting) |
| Claude не делегирует задачи субагентам, агенты на основе файловой системы не загружаются | [Устранение неполадок субагентов](https://code.claude.com/docs/ru/agent-sdk/subagents.md#troubleshooting) |
| Параметры чекпоинтов не распознаются, пользовательские сообщения без UUID, `No file checkpoint found`, `File rewinding is not enabled`, `ProcessTransport is not ready for writing` | [Устранение неполадок чекпоинтов файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md#troubleshooting) |
| Хук не срабатывает, matcher фильтрует не так, как ожидается, таймаут хука, инструмент неожиданно заблокирован, изменённые входные данные не применяются, хуки сессии недоступны в Python, запросы разрешений субагентов множатся, рекурсивные циклы хуков с субагентами, `systemMessage` не отображается в выводе | [Исправление распространённых проблем](https://code.claude.com/docs/ru/agent-sdk/hooks.md#fix-common-issues) на странице хуков |
| Агент, который работает на вашей машине, не работает в развёрнутом сервисе или контейнере | [Устранение сбоев развёртывания](https://code.claude.com/docs/ru/agent-sdk/hosting.md#troubleshoot-deployment-failures) |
| `Not logged in`, `Invalid API key`, `API Error`, `429`, `There's an issue with the selected model` | [Справочник по ошибкам](https://code.claude.com/docs/ru/errors.md#find-your-error) |
| `CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `Claude Code process exited with code N`, `Claude Code returned an error result`, `CLIJSONDecodeError`, `structured_output` имеет значение `None` | [Запуск CLI](#cli-startup), [Выход процесса CLI](#cli-process-exit), [Крупные вызовы инструментов и результаты](#large-tool-calls-and-results) и [Структурированные выводы](#structured-outputs) на этой странице |
| `Operation aborted`, `Claude Code process aborted by user`, `Prompt stream failed; closing stdin` или цикл `query()` в Python, который останавливается без исключения до того, как будут получены ответы на все ваши сообщения | [Потоковый ввод](#streaming-input) на этой странице |
| `Image could not be processed` | [Image could not be processed](#image-could-not-be-processed) на этой странице |

## Запуск CLI

### CLINotFoundError: Claude Code not found

Python SDK запускает Claude Code CLI как подпроцесс. Когда он не может найти исполняемый файл `claude`, подключение завершается с ошибкой `CLINotFoundError`:

```
Claude Code not found at: /your/configured/path
```

Сообщение включает настроенный путь, когда вы устанавливаете `ClaudeAgentOptions(cli_path=...)` и он указывает на отсутствующий файл. Без `cli_path` SDK ищет в вашем `PATH` и в общих местах установки, и сообщение включает инструкции по установке для вашей платформы.

Чтобы исправить это:

* Установите Claude Code, если он не установлен. Смотрите [Установка Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code) для команды на вашей платформе.
* Если вы установили `cli_path`, убедитесь, что файл существует и это исполняемый файл `claude`.
* Если вы полагаетесь на разрешение `PATH`, убедитесь, что `claude --version` работает в той же среде, в которой работает ваше приложение. Процессы, которые вы запускаете вне вашей оболочки, например из IDE или менеджера служб, часто работают с другим `PATH`.

TypeScript SDK ищет CLI в своем встроенном пакете платформы и в пути, который вы установили в `pathToClaudeCodeExecutable`. Сопоставьте сообщение, которое вы видите:

* `Native CLI binary for <platform>-<arch> not found`: встроенный пакет платформы отсутствует, чаще всего потому, что установка пропустила дополнительные зависимости. Переустановите `@anthropic-ai/claude-agent-sdk` без пропуска дополнительных зависимостей или укажите `pathToClaudeCodeExecutable` на [собственную установку](https://code.claude.com/docs/ru/setup.md#install-claude-code). В однофайловом исполняемом файле, созданном с помощью `bun build --compile`, то же сообщение имеет другую причину и исправление. Смотрите [Компиляция в один исполняемый файл](https://code.claude.com/docs/ru/agent-sdk/typescript.md#compile-to-a-single-executable).
* `Claude Code native binary not found at <path>` или `Claude Code executable not found at <path>. Is options.pathToClaudeCodeExecutable set?`: файл по разрешённому пути отсутствует или процесс не может получить к нему доступ. Убедитесь, что файл существует по этому пути и что процесс может получить к нему доступ.

### CLIConnectionError: Refusing to execute batch script

В Windows подключение завершается с ошибкой `CLIConnectionError`, когда путь CLI, который использует Python SDK, является пакетным скриптом `.bat` или `.cmd`, включая прокладку `claude.cmd`, которую создаёт установка npm:

```
Refusing to execute batch script 'C:\\Users\\you\\AppData\\Roaming\\npm\\claude.cmd': Windows runs .bat/.cmd files via cmd.exe, which can execute commands injected through CLI arguments, and no reliable escaping for cmd.exe exists. Use a native claude executable instead: install Claude Code natively (irm https://claude.ai/install.ps1 | iex), point ClaudeAgentOptions(cli_path=...) at a claude.exe, or install the claude-agent-sdk wheel for a platform that bundles claude.exe (e.g. Windows x64).
```

Отказ является преднамеренным усилением безопасности, а не сломанной установкой. Windows запускает пакетные скрипты, переписывая spawn в вызов `cmd.exe /c`, и `cmd.exe` переанализирует всю командную строку во время выполнения, поэтому значение аргумента может выполнить внедрённые команды.

Большинство установок Windows никогда не достигают этой ошибки. Колесо Windows x64 `claude-agent-sdk` содержит `claude.exe`, и SDK предпочитает встроенный CLI, затем любой собственный `claude.exe`, который он может обнаружить, прежде чем вернуться к пакетной прокладке. Вы видите отказ в двух случаях:

* Вы установили `ClaudeAgentOptions(cli_path=...)` на файл `.bat` или `.cmd`, например прокладку npm `claude.cmd`.
* Ваша установка не имеет встроенного или собственного `claude.exe`, например исходная установка на ARM64 Windows, где единственный `claude` в вашем `PATH` — это прокладка npm.

Чтобы исправить это, дайте SDK собственный исполняемый файл вместо пакетного скрипта:

* Если вы установили `ClaudeAgentOptions(cli_path=...)`, укажите его на `claude.exe` или удалите опцию. SDK пропускает обнаружение, пока установлен `cli_path`, поэтому собственная установка одна не может вступить в силу.
* Установите Claude Code собственно в PowerShell: `irm https://claude.ai/install.ps1 | iex`
* На x64 Windows установите колесо `claude-agent-sdk`, которое содержит `claude.exe`.

До `claude-agent-sdk` 0.2.124 Python SDK запускал пакетные скрипты через `cmd.exe` без этой проверки.

### CLIConnectionError: Failed to start Claude Code

SDK нашёл файл по разрешённому пути, но не смог его запустить. Python вызывает эти сбои как `CLIConnectionError`. TypeScript отклоняет итерацию сообщения с ошибкой, не имеющей класса SDK. Таблица ниже сопоставляет каждое сообщение с тем, что оно вам говорит. Сопоставьте сообщение, которое вы видите:

| Сообщение | SDK | Что это вам говорит |
| - | - | - |
| `Failed to start Claude Code: <detail>` | Python | Остаток сообщения — это собственная ошибка операционной системы |
| `Claude Code executable at <path> exists but failed to launch` | TypeScript | Скрипт по настроенному пути не может работать |
| `Claude Code native binary at <path> exists but failed to launch` | TypeScript | Двоичный файл не может работать, с предложением libc, добавленным к сообщению |
| `Failed to spawn Claude Code process: <detail>` | TypeScript | Любой другой сбой запуска |

В обоих SDK обычная причина — разрешённый путь, который указывает на что-то, что не может работать, например текстовый файл, каталог или файл без разрешения на выполнение. Прочитайте предложение libc сообщения о собственном двоичном файле как одну возможную причину.

Чтобы исправить это в любом SDK:

* Убедитесь, что настроенный путь указывает на сам исполняемый файл `claude` и что файл имеет разрешение на выполнение.
* Если вам не нужен пользовательский путь, удалите `cli_path` в Python или `pathToClaudeCodeExecutable` в TypeScript, чтобы SDK нашёл CLI самостоятельно, предпочитая его встроенную копию.
* Когда неработающий двоичный файл — это встроенная копия SDK в образе контейнера, переустановите SDK во время сборки образа, чтобы встроенный двоичный файл соответствовал платформе контейнера, или перестройте образ для архитектуры, на которой он работает. Обычная причина — двоичный файл, который не соответствует архитектуре или libc контейнера, или файл, который потерял разрешение на выполнение при сборке образа.

### CLIConnectionError: Not connected

Вызов метода `ClaudeSDKClient` в Python до подключения клиента или после его отключения вызывает `CLIConnectionError` с этим сообщением:

```
Not connected. Call connect() first.
```

Сделайте то, что говорит сообщение. Либо вызовите `await client.connect()` перед любым другим методом клиента, либо откройте клиент с помощью `async with ClaudeSDKClient() as client:`, который подключается при входе.

## Выход процесса CLI

Записи в этом разделе означают, что процесс Claude Code завершился, пока ваше приложение его использовало. Какую ошибку вы видите, зависит от языка SDK и от того, сообщил ли CLI об ошибке перед выходом.

### ProcessError: Command failed with exit code

Python SDK вызывает `ProcessError`, когда процесс Claude Code завершается с ненулевым кодом:

```
Command failed with exit code 1 (exit code: 1)
Error output: Check stderr output for details
```

Сообщение указывает код выхода дважды, а строка `Error output` — это фиксированный текст, а не вывод ошибки вашего процесса. Тот же фиксированный текст заполняет атрибут `stderr` исключения. Атрибут `exit_code` исключения содержит код. Чтобы захватить то, что CLI фактически написал в stderr, передайте обратный вызов `stderr` в `ClaudeAgentOptions` и логируйте то, что он получает.

Простой `ProcessError` означает, что CLI завершился без сообщения об ошибке. Когда CLI сообщил об ошибке, SDK вместо этого вызывает [`ResultError`](https://code.claude.com/docs/ru/agent-sdk/python#resulterror), рассмотренный в [Claude Code returned an error result](#claude-code-returned-an-error-result). `ResultError` является подклассом `ProcessError`, поэтому `except ProcessError` ловит оба. Чтобы обработать их по-разному, поместите предложение `except ResultError` первым.

До `claude-agent-sdk` 0.2.140 Python SDK вызывал выходы с результатом ошибки как простое `Exception` вместо `ResultError`.

### Claude Code process exited with code N

Обёртки IDE также печатают это сообщение, и [справочник ошибок](https://code.claude.com/docs/ru/errors.md#claude-code-process-exited-with-code-n) охватывает его для VS Code и других средств запуска. Эта запись охватывает то, что получает ваш код TypeScript SDK. SDK отображает ненулевой выход CLI как простую `Error`, которая отклоняет цикл `for await` над сообщениями `query()`. Нет класса ошибки SDK для перехвата, поэтому оберните цикл в `try`/`catch` и сопоставьте сообщение:

```
Claude Code process exited with code 1. stderr: <tail of the CLI's stderr>
```

Когда CLI писал в stderr, сообщение заканчивается хвостом этого. Чтобы захватить полный поток, передайте обратный вызов `stderr` в параметры запроса. Процесс, убитый сигналом, сообщает `Claude Code process terminated by signal <name>` в той же форме.

### Claude Code returned an error result

Оба SDK заменяют ошибку выхода процесса этим сообщением, когда CLI сообщил об ошибке перед выходом:

```
Claude Code returned an error result: <the CLI's own error report>
```

Текст после двоеточия — это отчёт CLI о том, что пошло не так, поэтому начните с него, а не с самого выхода. Python вызывает это как [`ResultError`](https://code.claude.com/docs/ru/agent-sdk/python#resulterror), атрибут `data` которого содержит полный результат ошибки. TypeScript отклоняет цикл сообщений простой `Error`, несущей ту же форму сообщения.

## Большие вызовы инструментов и их результаты

### CLIJSONDecodeError: JSON message exceeded maximum buffer size

Python SDK выдаёт эту ошибку, когда одно сообщение от Claude Code длиннее значения параметра [`max_buffer_size`](https://code.claude.com/docs/ru/agent-sdk/python#claudeagentoptions), которое по умолчанию равно 1 048 576 символам. В тексте ошибки они называются байтами:

```text theme={null}
Failed to decode JSON: JSON message exceeded maximum buffer size of 1048576 bytes...
```

Например, PDF-файлы, снимки экрана и текстовые файлы могут порождать сообщения, достигающие этого предела:

* **PDF-файлы и снимки экрана**: когда Claude читает целиком PDF-файл размером около 393 КБ или больше с помощью инструмента Read, результат инструмента может достичь предела, поскольку он содержит base64-представление файла дважды. Результат инструмента со снимком экрана, полученный от Read или от инструмента MCP, также содержит base64 дважды.
* **Текстовые файлы**: сообщения от инструментов Edit и Write могут достичь предела на файле размером значительно меньше 1 МБ в зависимости от того, какая часть файла изменяется.

Чтобы устранить ошибку, задайте больший предел в `ClaudeAgentOptions`:

```python theme={null}
options = ClaudeAgentOptions(max_buffer_size=64 * 1024 * 1024)
```

Этого значения достаточно для снимка экрана и для чтения через Read целого PDF-файла вплоть до предела Read в 20 МБ. Если ошибка возникает снова, например при Edit очень большого файла, задайте более высокое значение.

Любые изменения, уже внесённые инструментом, сохраняются, и вызов инструмента, сообщение которого оказалось слишком длинным, мог внести такое изменение. Чтобы продолжить прерванную работу:

1. Если у вас открыт `ClaudeSDKClient`, вызовите `disconnect()`. После этой ошибки клиент больше не получает сообщений, но Claude Code продолжает работать и всё ещё может вносить изменения.
2. Запустите новый `query()` или `ClaudeSDKClient` с увеличенным пределом и [`continue_conversation=True`](https://code.claude.com/docs/ru/agent-sdk/sessions#continue-resume-and-fork), что выберет самую последнюю сессию в рабочем каталоге. Чтобы выбрать конкретную сессию, задайте `resume` равным `data["session_id"]` из инициализирующего [`SystemMessage`](https://code.claude.com/docs/ru/agent-sdk/python#systemmessage).

## Потоковый ввод

### Operation aborted

В TypeScript ваш цикл `for await` по `query()` выбрасывает одно из этих сообщений как `AbortError`. Любое из них означает, что запрос был прерван:

```text theme={null}
Operation aborted
Claude Code process aborted by user
```

Проверьте следующие причины:

* **Ваш код прервал запрос**: если ваш код вызывает `abort()` у `AbortController`, который вы передали в качестве параметра [`abortController`](https://code.claude.com/docs/ru/agent-sdk/typescript#options), цикл выбрасывает одну из этих ошибок. Если вы не планировали прерывание, проверьте, где ваш код вызывает `abort()`.
* **Ваш асинхронный генератор выбросил исключение**: ошибка не содержит собственного сообщения об ошибке вашего генератора. Чтобы увидеть это сообщение, оберните тело генератора в `try`/`catch`, запишите перехваченную ошибку в лог и выбросьте её повторно. Затем исправьте ошибку, которую вы записали в лог.

### Prompt stream failed; closing stdin

В Python, когда асинхронный генератор, который вы передали в функцию `query()`, выбрасывает исключение, ваш цикл `async for` по `query()` завершается без исключения. SDK записывает эту строку в лог с уровнем `ERROR`. Если вы не настроили логирование, Python выводит строку в stderr:

```text theme={null}
Prompt stream failed; closing stdin: <your exception's message>
```

Чтобы увидеть трассировку стека исключения, оберните тело генератора в `try`/`except`. Запишите исключение в лог вместе с трассировкой стека и выбросьте его снова. Затем исправьте исключение, которое вы записали в лог.

### Image could not be processed

Когда у блока изображения в вашем сообщении нет объекта `source`, никакая ошибка до вашего кода не доходит. Вместо изображения Claude получает следующее текстовое примечание:

```text theme={null}
[Image could not be processed: image block has no source object]
```

Claude отвечает без изображения. Убедитесь, что у каждого блока изображения есть объект `source`, как в разделе [Отправка последующего сообщения с изображением](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md#send-a-follow-up-with-an-image).

## Структурированные выходы

### structured\_output is None but the result says success

Сообщение результата может заканчиваться `subtype: "success"`, пока `structured_output` равен `None` в Python или `undefined` в TypeScript. Запуск завершается, но проверенный выход не существует.

Рассматривайте этот результат как сбой в коде приложения. Раздел [Error handling](https://code.claude.com/docs/ru/agent-sdk/structured-outputs.md#error-handling) показывает этот паттерн для обоих SDK. Затем проверьте следующие причины:

* **Запрос, который Claude отклонил**: чтобы обнаружить этот случай в коде, проверьте, равен ли `stop_reason` в сообщении результата значению `"refusal"`. О том, что попробовать дальше, см. [Отказ по Usage Policy](https://code.claude.com/docs/ru/errors.md#usage-policy-refusal).
* **Схема, которую не может удовлетворить никакой выход**: например, строка, у которой `minLength` больше, чем `maxLength`. Если `structured_output` повторно отсутствует со схемой, которую вы считаете правильной, поищите ограничения, противоречащие друг другу. Если таких нет, упрощайте схему до тех пор, пока выходы не начнут проходить проверку, а затем возвращайте ограничения по одному.

## Сообщить о новой проблеме

Если ваша ошибка не охвачена здесь, проверьте открытые проблемы или создайте новую в репозиториях SDK: [claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript/issues) или [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python/issues). Включите полный текст ошибки и версию вашего SDK.
