> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Перехватывайте и контролируйте поведение агента с помощью hooks

> Перехватывайте и настраивайте поведение агента в ключевых точках выполнения с помощью hooks

Hooks — это функции обратного вызова, которые выполняют ваш код в ответ на события агента, такие как вызов инструмента, начало сеанса или остановка выполнения. С помощью hooks вы можете:

* **Блокировать опасные операции** перед их выполнением, такие как деструктивные команды shell или несанкционированный доступ к файлам
* **Логировать и аудировать** вызовы инструментов для соответствия требованиям, отладки или аналитики
* **Преобразовывать входные и выходные данные** для санитизации данных, внедрения учетных данных или перенаправления путей файлов
* **Требовать одобрение человека** для чувствительных действий, таких как запись в базу данных или вызовы API
* **Отслеживать жизненный цикл сеанса** для управления состоянием, очистки ресурсов или отправки уведомлений

## Как работают хуки

**1. Срабатывает событие**

Во время выполнения агента что-то происходит, и SDK генерирует событие: инструмент вот-вот будет вызван (`PreToolUse`), инструмент вернул результат (`PostToolUse`), субагент запустился или остановился, агент простаивает или выполнение завершилось. См. [полный список событий](#available-hooks).

**2. SDK собирает зарегистрированные хуки**

SDK проверяет наличие хуков, зарегистрированных для этого типа события. Сюда входят callback-хуки, которые вы передаете в `options.hooks`, и хуки shell-команд из файлов настроек, если включена соответствующая запись [`settingSources`](https://code.claude.com/docs/ru/agent-sdk/typescript#settingsource) или [`setting_sources`](https://code.claude.com/docs/ru/agent-sdk/python#settingsource), что по умолчанию так и есть для параметров `query()`.

**3. Фильтрация запускаемых хуков с помощью matcher**

Если у хука есть паттерн [`matcher`](#matchers) (например, `"Write|Edit"`), SDK проверяет его на соответствие цели события (например, имени инструмента). Хуки без matcher запускаются для каждого события этого типа.

**4. Выполняются функции обратного вызова**

[Функция обратного вызова](#callback-functions) каждого подходящего хука получает информацию о том, что происходит: имя инструмента, его аргументы, ID сессии и другие детали, специфичные для события.

**5. Ваш callback возвращает решение**

После выполнения любых операций (логирование, вызовы API, валидация) ваш callback возвращает [объект вывода](#outputs), который сообщает агенту, что делать: разрешить операцию, заблокировать ее, изменить входные данные или внедрить контекст в диалог.

Этот пример регистрирует хук `PreToolUse` (шаг 1) с matcher `"Write|Edit"` (шаг 3), поэтому callback срабатывает для инструментов Write и Edit. При срабатывании callback получает входные данные инструмента (шаг 4), проверяет, указывает ли путь файла на файл `.env`, и возвращает `permissionDecision: "deny"` для блокировки операции (шаг 5):

```python Python theme={null}
import asyncio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
)


# Define a hook callback that receives tool call details
async def protect_env_files(input_data, tool_use_id, context):
    # Extract the file path from the tool's input arguments
    file_path = input_data["tool_input"].get("file_path", "")
    file_name = file_path.split("/")[-1]

    # Block the operation if targeting a .env file
    if file_name.lower() == ".env":
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }

    # Return empty object to allow the operation
    return {}


async def main():
    options = ClaudeAgentOptions(
        hooks={
            # Register the hook for PreToolUse events
            # The matcher filters to only Write and Edit tool calls
            "PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Create a .env file with the standard local development database configuration")
        async for message in client.receive_response():
            # Filter for assistant and result messages
            if isinstance(message, (AssistantMessage, ResultMessage)):
                print(message)


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query, HookCallback, PreToolUseHookInput } from "@anthropic-ai/claude-agent-sdk";

// Define a hook callback with the HookCallback type
const protectEnvFiles: HookCallback = async (input, toolUseID, { signal }) => {
  // Cast input to the specific hook type for type safety
  const preInput = input as PreToolUseHookInput;

  // Cast tool_input to access its properties (typed as unknown in the SDK)
  const toolInput = preInput.tool_input as Record<string, unknown>;
  const filePath = toolInput?.file_path as string;
  const fileName = filePath?.split("/").pop();

  // Block the operation if targeting a .env file
  if (fileName?.toLowerCase() === ".env") {
    return {
      hookSpecificOutput: {
        hookEventName: preInput.hook_event_name,
        permissionDecision: "deny",
        permissionDecisionReason: "Cannot modify .env files"
      }
    };
  }

  // Return empty object to allow the operation
  return {};
};

for await (const message of query({
  prompt: "Create a .env file with the standard local development database configuration",
  options: {
    hooks: {
      // Register the hook for PreToolUse events
      // The matcher filters to only Write and Edit tool calls
      PreToolUse: [{ matcher: "Write|Edit", hooks: [protectEnvFiles] }]
    }
  }
})) {
  // Filter for assistant and result messages
  if (message.type === "assistant" || message.type === "result") {
    console.log(message);
  }
}
```

Хук отклоняет вызов Write или Edit, у которого `file_path` заканчивается на `/.env`, в любом регистре букв. В Windows `file_path` использует обратные косые черты, например `C:\project\.env`, и этот хук разрешает вызов Write или Edit для `C:\project\.env`.

> [!WARNING]
>
> Matcher `Write|Edit` ограничивает действие этого хука инструментами Write и Edit. Если Claude запишет `.env` с помощью команды Bash, хук не запустится. Чтобы заблокировать запись через Bash в файл там, где [работает песочница](https://code.claude.com/docs/ru/sandboxing.md), см. конфигурацию песочницы для [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#sandbox-configuration) или [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#sandbox-configuration).

## Доступные hooks

SDK предоставляет hooks для различных этапов выполнения агента. Некоторые hooks доступны в обоих SDK, в то время как другие доступны только в TypeScript.

| Hook Event | Python SDK | TypeScript SDK | Что его срабатывает | Пример использования |
| - | - | - | - | - |
| `PreToolUse` | Да | Да | Запрос вызова инструмента (может блокировать или изменять) | Блокировать опасные команды shell |
| `PostToolUse` | Да | Да | Результат выполнения инструмента | Логировать изменения файлов в журнал аудита |
| `PostToolUseFailure` | Да | Да | Ошибка выполнения инструмента | Обработать или логировать ошибки инструмента |
| `PostToolBatch` | Нет | Да | Полный пакет вызовов инструментов разрешается, один раз за пакет перед следующим вызовом модели | Внедрить соглашения один раз для всего пакета |
| [`UserPromptSubmit`](https://code.claude.com/docs/ru/hooks#userpromptsubmit) | Да | Да | Отправляется промпт, включая ход, который Claude Code начинает самостоятельно | Внедрить дополнительный контекст в промпты |
| [`UserPromptExpansion`](https://code.claude.com/docs/ru/hooks#userpromptexpansion) | Нет | Да | Команда, введённая пользователем, или MCP приглашение, расширяется в приглашение перед тем, как она достигнет Claude. Не срабатывает, когда Claude вызывает skill самостоятельно | Заблокировать команду от прямого вызова или добавить контекст при вводе skill |
| `MessageDisplay` | Нет | Да | Сообщение ассистента с текстом завершается, один раз за сообщение с полным текстом сообщения | Скрыть или переформатировать отображаемый текст без изменения стенограммы |
| `Stop` | Да | Да | Остановка выполнения агента | Сохранить состояние сеанса перед выходом |
| `StopFailure` | Нет | Да | Ход завершается с ошибкой API вместо нормальной остановки | Логировать сбои или отправлять оповещения |
| `SubagentStart` | Да | Да | Инициализация подагента | Отслеживать порождение параллельных задач |
| `SubagentStop` | Да | Да | Завершение подагента | Агрегировать результаты из параллельных задач |
| `PreCompact` | Да | Да | Запрос сжатия разговора | Архивировать полную стенограмму перед суммированием |
| `PostCompact` | Нет | Да | Сжатие разговора завершается | Логировать созданное резюме |
| [`PreModelSwitch`](https://code.claude.com/docs/ru/hooks#premodelswitch) | Нет | Да | Запрошенное переключение модели, перед тем как оно произойдёт (может блокировать) | Заблокировать переключение на конкретную модель |
| [`PostModelSwitch`](https://code.claude.com/docs/ru/hooks#postmodelswitch) | Нет | Да | Модель сеанса изменяется, включая автоматический откат | Дать Claude рекомендации, специфичные для модели, для новой модели |
| `PermissionRequest` | Да | Да | Вызов инструмента требует решения о разрешении | Пользовательская обработка разрешений |
| `PermissionDenied` | Нет | Да | Автоматический режим отклоняет вызов инструмента, включая отклонения без вердикта классификатора | Логировать отклонения или сообщить модели, что она может повторить попытку; Claude Code игнорирует `retry: true` для отклонений без вердикта. См. [PermissionDenied](https://code.claude.com/docs/ru/hooks.md#permissiondenied) |
| `SessionStart` | Нет | Да | Инициализация сеанса | Инициализировать логирование и телеметрию |
| `SessionEnd` | Нет | Да | Завершение сеанса | Очистить временные ресурсы |
| `Notification` | Да | Да | Сообщения о статусе агента | Отправить обновления статуса агента в Slack или PagerDuty |
| `Setup` | Нет | Да | Настройка/обслуживание сеанса | Запустить задачи инициализации |
| `TeammateIdle` | Нет | Да | Товарищ по команде становится неактивным | Переназначить работу или уведомить |
| `TaskCreated` | Нет | Да | Задача создана через инструмент `TaskCreate` | Применять соглашения об именовании задач |
| [`TaskCompleted`](https://code.claude.com/docs/ru/hooks#taskcompleted) | Нет | Да | Задача отмечена как завершённая | Требовать прохождения тестов перед закрытием задачи |
| `Elicitation` | Нет | Да | MCP сервер запрашивает ввод пользователя во время задачи | Программно отвечать на запросы ввода MCP |
| `ElicitationResult` | Нет | Да | Пользователь отвечает на запрос MCP | Изменить или заблокировать ответ перед его возвратом на сервер |
| `ConfigChange` | Нет | Да | Файл конфигурации изменился | Динамически перезагрузить настройки |
| `InstructionsLoaded` | Нет | Да | Файл `CLAUDE.md` или файл правил загружается в контекст | Проверять, какие файлы инструкций загружаются |
| `WorktreeCreate` | Нет | Да | Git worktree создан | Отслеживать изолированные рабочие пространства |
| `WorktreeRemove` | Нет | Да | Удаляется worktree, созданный хуком `WorktreeCreate` | Очистить ресурсы рабочего пространства |
| `CwdChanged` | Нет | Да | Рабочий каталог изменяется во время сеанса | Перезагрузить переменные окружения для каждого каталога |
| `FileChanged` | Нет | Да | Отслеживаемый файл изменяется, создаётся или удаляется | Перезагрузить конфигурацию при изменении файлов проекта |
| `DirectoryAdded` | Нет | Да | Рабочий каталог добавляется во время сеанса | Установить зависимости для репозитория, добавленного во время сеанса |

## Настройка хуков

Чтобы настроить хук, передайте его в поле `hooks` ваших параметров агента (`ClaudeAgentOptions` в Python, объект `options` в TypeScript). Этот фрагмент предполагает, что вы уже определили callback хука, например `protect_env_files` в Python или `protectEnvFiles` в TypeScript из примера выше:

```python Python theme={null}
options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[my_callback])]}
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Your prompt")
    async for message in client.receive_response():
        print(message)
```

```typescript TypeScript theme={null}
for await (const message of query({
  prompt: "Your prompt",
  options: {
    hooks: {
      PreToolUse: [{ matcher: "Bash", hooks: [myCallback] }]
    }
  }
})) {
  console.log(message);
}
```

Опция `hooks` — это словарь (Python) или объект (TypeScript), где:

* **Ключи**: [имена событий хуков](#available-hooks), такие как `'PreToolUse'`, `'PostToolUse'` и `'Stop'`
* **Значения**: массивы [matchers](#matchers), каждый содержащий необязательный паттерн фильтра и ваши [функции обратного вызова](#callback-functions)

### Matchers

Используйте matchers для фильтрации, когда срабатывают ваши callbacks. Поле `matcher` сопоставляется с разными значениями в зависимости от типа события хука. Например, хуки на основе инструментов сопоставляются с именем инструмента, в то время как хуки `Notification` сопоставляются с типом уведомления.

SDK matchers следуют тем же правилам, что и [matchers в файлах настроек](https://code.claude.com/docs/ru/hooks.md#matcher-patterns). Этот раздел документирует пути оценки точной строки и регулярного выражения, требования к версиям и значения matcher для каждого типа события.

| Опция | Тип | По умолчанию | Описание |
| - | - | - | - |
| `matcher` | `string` | `undefined` | Паттерн, сопоставляемый с полем фильтра события, следуя [правилам для matchers в файлах настроек](https://code.claude.com/docs/ru/hooks.md#matcher-patterns). Для хуков инструментов это имя инструмента. Встроенные инструменты включают `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `Agent` и другие. Полный список см. в [Tool Input Types](https://code.claude.com/docs/ru/agent-sdk/typescript.md#tool-input-types). MCP инструменты используют паттерн `mcp__<server>__<action>`, где `<server>` — это ключ, который вы используете в конфигурации `mcpServers`, записанный так, как описано в [соглашении об именовании инструментов](https://code.claude.com/docs/ru/agent-sdk/mcp.md#tool-naming-convention). |
| `hooks` | `HookCallback[]` | - | Обязательно. Массив функций обратного вызова для выполнения, когда паттерн совпадает |
| `timeout` | `number` | `undefined` | Таймаут в секундах. Если опущен, Claude Code применяет [таймаут события по умолчанию](#hook-timeout). Ваши SDK callbacks следуют значениям по умолчанию хука `command` |
| `onFailure` | `"continue" \| "block"` | `undefined` | Что происходит при сбое callback. Установите `"block"`, чтобы [блокировать действие при сбое callback](#block-the-action-when-a-callback-fails). В Python используйте `on_failure` |

Используйте паттерн `matcher` для нацеливания на конкретные инструменты, когда это возможно. С matcher `'Bash'` ваши callbacks запускаются для команд Bash. В Claude Code версии 2.1.314 или позже они также запускаются в `PreToolUse` и `PermissionRequest` для команд Monitor, которые они [могут отклонить, но не одобрить](https://code.claude.com/docs/ru/hooks.md#match-monitor-commands). Без matcher они запускаются для каждого возникновения события.

### Функции обратного вызова

#### Входные данные

Каждый callback хука получает три аргумента:

* **Входные данные:** типизированный объект, содержащий детали события. Каждый тип хука имеет свою форму входных данных. Например, `PreToolUseHookInput` включает `tool_name` и `tool_input`, в то время как `NotificationHookInput` включает `message`. См. полные определения типов в справочниках [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#hookinput) и [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#hookinput) SDK.
  * Все входные данные хуков содержат `session_id`, `cwd` и `hook_event_name`.
  * `agent_id` и `agent_type` заполняются, когда хук срабатывает внутри субагента. В TypeScript они находятся на базовом входе хука и доступны для всех типов хуков. В Python они являются необязательными полями на `PreToolUse`, `PostToolUse`, `PostToolUseFailure` и `PermissionRequest`, и обязательными полями на `SubagentStart` и `SubagentStop`.
* **ID использования инструмента** (`str | None` / `string | undefined`): коррелирует события `PreToolUse` и `PostToolUse` для одного и того же вызова инструмента.
* **Контекст:** в TypeScript содержит свойство `signal` (`AbortSignal`) для отмены. В Python этот аргумент зарезервирован для будущего использования.

#### Выходные данные

Ваш callback возвращает объект с двумя категориями полей:

* **Поля верхнего уровня** принимаются для каждого события: `systemMessage` показывает сообщение пользователю, и `continue` (`continue_` в Python) определяет, продолжает ли агент работать после этого хука. Некоторые события отбрасывают их или доставляют их в другое место. Раздел каждого [события](https://code.claude.com/docs/ru/hooks.md#hook-events) на странице хуков говорит, где они попадают.
* **`hookSpecificOutput`** контролирует текущую операцию. Поля, которые вы устанавливаете внутри, зависят от типа события хука:
  * Для хуков `PreToolUse` здесь вы устанавливаете `permissionDecision` (`"allow"`, `"deny"`, `"ask"` или `"defer"`), `permissionDecisionReason` и `updatedInput`. Если вы вернете `"defer"`, ход завершается сообщением с результатом, у которого `stop_reason` равен `"tool_deferred"`, чтобы вы могли [возобновить вызов позже](https://code.claude.com/docs/ru/hooks.md#defer-a-tool-call-for-later).
  * Для хуков `PostToolUse` вы можете установить `additionalContext` для добавления информации к результату инструмента. Чтобы заменить выходные данные инструмента перед тем, как Claude их увидит, установите `updatedToolOutput`, который работает для встроенных инструментов и инструментов MCP в обоих SDK. Более старое поле `updatedMCPToolOutput` заменяет только выходные данные MCP инструмента.
  * В TypeScript SDK callback `PostToolUse` может также возвращать `classifierContext`, краткую заметку о результате вызова инструмента для классификатора разрешений [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode). Поскольку ваш callback работает в собственном процессе вашего приложения, классификатор может учитывать заявление пользователя, которое вы передаете в заметке, как намерение пользователя. Поле требует TypeScript Agent SDK версии 0.3.236 или позже. В разделе [Аннотирование результата для классификатора авторежима](https://code.claude.com/docs/ru/hooks.md#annotate-a-result-for-the-auto-mode-classifier) описаны ограничение по длине, правило только синхронного выполнения и то, что не следует помещать в заметку.

Возвращайте `{}` для разрешения операции без изменений. SDK callback-хуки используют тот же формат вывода JSON, что и [хуки shell-команд Claude Code](https://code.claude.com/docs/ru/hooks.md#json-output), который документирует каждое поле и опцию, специфичную для события. Для определений типов SDK см. справочники [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#synchookjsonoutput) и [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#synchookjsonoutput) SDK.

> [!NOTE]
>
> Когда несколько хуков `PreToolUse` возвращают разные [решения](https://code.claude.com/docs/ru/hooks.md#pretooluse-decision-control), `deny` имеет приоритет над `defer`, который имеет приоритет над `ask`, который имеет приоритет над `allow`.

#### Асинхронный вывод

По умолчанию агент ждет, пока ваш хук вернется, прежде чем продолжить. Если ваш хук выполняет побочный эффект, такой как логирование или отправка webhook, и ему не нужно влиять на поведение агента, вы можете вернуть асинхронный вывод вместо этого. Это говорит агенту продолжить немедленно без ожидания завершения хука. В этом фрагменте `send_to_logging_service` в Python и `sendToLoggingService` в TypeScript служат заменой для любой функции логирования, которую вы определяете:

```python Python theme={null}
async def async_hook(input_data, tool_use_id, context):
    # Start a background task, then return immediately
    asyncio.create_task(send_to_logging_service(input_data))
    return {"async_": True, "asyncTimeout": 30000}
```

```typescript TypeScript theme={null}
const asyncHook: HookCallback = async (input, toolUseID, { signal }) => {
  // Start a background task, then return immediately
  sendToLoggingService(input).catch(console.error);
  return { async: true, asyncTimeout: 30000 };
};
```

| Поле | Тип | Описание |
| - | - | - |
| `async` | `true` | Сигнализирует асинхронный режим. Агент продолжает без ожидания. В Python используйте `async_` для избежания зарезервированного ключевого слова. |
| `asyncTimeout` | `number` | Необязательный таймаут в миллисекундах для фоновой операции |

> [!NOTE]
>
> Асинхронные выходы не могут блокировать, изменять или внедрять контекст в операцию, так как агент уже продолжил. Используйте их только для побочных эффектов, таких как логирование, метрики или уведомления.

### Блокировка действия при сбое callback

Для большинства событий, если callback выбрасывает исключение или возвращает вывод, не прошедший валидацию, действие выполняется, а ваше приложение получает предупреждение [`SDKInformationalMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkinformationalmessage), у которого `tag` равен `hook_callback_failed`. В этом случае аварийно завершившаяся защита `PreToolUse` пропускает вызов инструмента в обычный процесс проверки разрешений. Callback, который ничего не возвращает, например ветка кода без `return`, также считается сбойным. В Python читайте `tag` из `SystemMessage.data`.

Чтобы вместо этого блокировать действие, установите для matcher `onFailure: "block"` в TypeScript или `on_failure="block"` в Python. Требуется TypeScript Agent SDK версии 0.3.317 или позже либо Python Agent SDK версии 0.2.177 или позже. Этот пример блокирует вызов Bash при сбое `check_policy` в Python или `checkPolicy` в TypeScript:

```python Python theme={null}
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_policy], on_failure="block")
        ]
    }
)
```

```typescript TypeScript theme={null}
import type { Options } from "@anthropic-ai/claude-agent-sdk";

const options: Options = {
  hooks: {
    PreToolUse: [{ matcher: "Bash", hooks: [checkPolicy], onFailure: "block" }]
  }
};
```

Чтобы проверить это, заставьте callback выбросить ошибку и попросите Claude выполнить команду Bash. Результат инструмента содержит `failed; blocking because onFailure is "block"`, а Claude не видит текст вашей ошибки.

Возвращайте `{}`, когда у callback нет решения. При установленном `"block"` ветка кода без `return` блокирует действие. Callback, который перехватывает собственную ошибку и возвращает `{}`, не считается сбойным, поэтому позвольте ошибке распространиться из защитного callback.

#### События с другим поведением

Эти события не всегда блокируются при установленном `"block"`:

* **`Stop`, `SubagentStop`, `TaskCompleted` и `TeammateIdle`**: эти события игнорируют опцию, поэтому действие выполняется.
* **`PermissionRequest`**: блокировка учитывается, только если она поступает до ответа вашего callback `canUseTool`.
* **`PostToolUse`**: инструмент уже выполнен, поэтому Claude получает сбой в качестве обратной связи.

Callback, превысивший свой таймаут, ведет себя согласно разделу [Таймаут хука](#hook-timeout). При установленном `"block"` таймаут также блокирует `PreCompact`, `Elicitation` и `WorktreeCreate`.

#### Ошибки запуска для `onFailure`

При установленном `"block"` запрос завершается ошибкой при запуске и не отправляет промпт, если не может соблюсти опцию:

* **Claude Code не поддерживает опцию**: ошибка содержит `does not honor`. Обновите Claude Code или удалите опцию.
* **Сессия уже была запущена и не зарегистрировала ваши хуки**: ошибка содержит `did not register your hooks`. Начните новую сессию.

## Примеры

Несколько примеров в этом разделе показывают только функцию callback. Чтобы запустить один из них, зарегистрируйте callback под соответствующим событием в поле `hooks` ваших параметров, как показано в [Настройка hooks](#configure-hooks).

### Изменение входных данных инструмента

Этот пример перехватывает вызовы инструмента Write и переписывает аргумент `file_path`, добавляя к нему префикс `/sandbox`. Callback возвращает `updatedInput` с измененным путем и `permissionDecision: 'allow'` для автоматического одобрения переписанной операции:

```python Python theme={null}
async def redirect_to_sandbox(input_data, tool_use_id, context):
    if input_data["hook_event_name"] != "PreToolUse":
        return {}

    if input_data["tool_name"] == "Write":
        original_path = input_data["tool_input"].get("file_path", "")
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "allow",
                "updatedInput": {
                    **input_data["tool_input"],
                    "file_path": f"/sandbox{original_path}",
                },
            }
        }
    return {}
```

```typescript TypeScript theme={null}
const redirectToSandbox: HookCallback = async (input, toolUseID, { signal }) => {
  if (input.hook_event_name !== "PreToolUse") return {};

  const preInput = input as PreToolUseHookInput;
  const toolInput = preInput.tool_input as Record<string, unknown>;
  if (preInput.tool_name === "Write") {
    const originalPath = toolInput.file_path as string;
    return {
      hookSpecificOutput: {
        hookEventName: preInput.hook_event_name,
        permissionDecision: "allow",
        updatedInput: {
          ...toolInput,
          file_path: `/sandbox${originalPath}`
        }
      }
    };
  }
  return {};
};
```

> [!NOTE]
>
> Используйте `updatedInput` с `permissionDecision: 'allow'` для автоматического одобрения измененного входа или `permissionDecision: 'ask'` для отображения его пользователю. Если вы опустите `permissionDecision`, измененный вход все равно применяется и проходит через обычную оценку разрешений. С `'defer'` `updatedInput` игнорируется. Всегда возвращайте новый объект вместо мутирования оригинального `tool_input`.

Чтобы подтвердить перенаправление, установите префикс на путь, в который вы можете писать, например `./sandbox` или `/tmp/sandbox` (macOS не позволяет создавать корневой каталог `/sandbox`), затем попросите агента написать файл: результат инструмента Write в потоке сообщений указывает путь с вашим префиксом sandbox вместо того, который запросил Claude.

### Добавление контекста и блокировка инструмента

Этот пример отклоняет вызовы инструментов, у которых `file_path` начинается с `/etc`, и объясняет причину как модели, так и пользователю:

* `permissionDecision: 'deny'` останавливает вызов инструмента.
* `permissionDecisionReason` сообщает модели причину.
* `systemMessage` показывает пользователю, что произошло.

```python Python theme={null}
async def block_etc_writes(input_data, tool_use_id, context):
    file_path = input_data["tool_input"].get("file_path", "")

    if file_path.startswith("/etc"):
        return {
            # Top-level field: message shown to the user
            "systemMessage": "Remember: system directories like /etc are protected.",
            # hookSpecificOutput: block the operation
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Writing to /etc is not allowed",
            },
        }
    return {}
```

```typescript TypeScript theme={null}
const blockEtcWrites: HookCallback = async (input, toolUseID, { signal }) => {
  const preInput = input as PreToolUseHookInput;
  const toolInput = preInput.tool_input as Record<string, unknown>;
  const filePath = toolInput?.file_path as string;

  if (filePath?.startsWith("/etc")) {
    return {
      // Top-level field: message shown to the user
      systemMessage: "Remember: system directories like /etc are protected.",
      // hookSpecificOutput: block the operation
      hookSpecificOutput: {
        hookEventName: preInput.hook_event_name,
        permissionDecision: "deny",
        permissionDecisionReason: "Writing to /etc is not allowed"
      }
    };
  }
  return {};
};
```

Чтобы подтвердить блокировку, зарегистрируйте callback под `PreToolUse` с matcher `Write|Edit` и попросите агента создать файл в `/etc`: результат инструмента Write в потоке сообщений содержит `Writing to /etc is not allowed`, и файл не создается.

### Автоматическое одобрение конкретных инструментов

По умолчанию агент может запросить разрешение перед использованием определенных инструментов. Этот пример автоматически одобряет инструменты файловой системы только для чтения (Read, Glob, Grep), возвращая `permissionDecision: 'allow'`, позволяя им запускаться без подтверждения пользователя, за исключением чтения из [сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths), и оставляя все остальные инструменты подлежащими обычным проверкам разрешений:

```python Python theme={null}
async def auto_approve_read_only(input_data, tool_use_id, context):
    if input_data["hook_event_name"] != "PreToolUse":
        return {}

    read_only_tools = ["Read", "Glob", "Grep"]
    if input_data["tool_name"] in read_only_tools:
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "allow",
                "permissionDecisionReason": "Read-only tool auto-approved",
            }
        }
    return {}
```

```typescript TypeScript theme={null}
const autoApproveReadOnly: HookCallback = async (input, toolUseID, { signal }) => {
  if (input.hook_event_name !== "PreToolUse") return {};

  const preInput = input as PreToolUseHookInput;
  const readOnlyTools = ["Read", "Glob", "Grep"];
  if (readOnlyTools.includes(preInput.tool_name)) {
    return {
      hookSpecificOutput: {
        hookEventName: preInput.hook_event_name,
        permissionDecision: "allow",
        permissionDecisionReason: "Read-only tool auto-approved"
      }
    };
  }
  return {};
};
```

### Регистрация нескольких hooks

Когда событие срабатывает, соответствующие хуки выполняются параллельно. Для решений о разрешениях применяется наиболее ограничивающий результат. `deny` одного хука блокирует вызов инструмента. Поскольку порядок завершения недетерминирован, пишите каждый хук так, чтобы он действовал независимо, а не полагался на то, что другой хук уже выполнился.

Пример ниже регистрирует три независимые проверки, каждую с [опущенным matcher](https://code.claude.com/docs/ru/hooks.md#matcher-patterns). Имена хуков в нем, такие как `audit_logger` в Python или `auditLogger` в TypeScript, служат заменой для callbacks, которые вы определяете:

```python Python theme={null}
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(hooks=[authorization_check]),
            HookMatcher(hooks=[input_validator]),
            HookMatcher(hooks=[audit_logger]),
        ]
    }
)
```

```typescript TypeScript theme={null}
const options = {
  hooks: {
    PreToolUse: [
      { hooks: [authorizationCheck] },
      { hooks: [inputValidator] },
      { hooks: [auditLogger] }
    ]
  }
};
```

### Фильтрация с помощью multi-tool matchers

Используйте multi-tool matchers для совместного использования одного callback для связанных инструментов. Этот пример регистрирует три matcher с разными областями, и каждый hook, который он называет, служит заменой для callback, который вы определяете:

* Точный список с разделением вертикальной чертой (`Write|Edit|NotebookEdit`) запускает `file_security_hook` для инструментов Write, Edit и NotebookEdit.
* Regex (`^mcp__`) срабатывает `mcp_audit_hook` для любого MCP инструмента, имя которого начинается с `mcp__`.
* Опущенный matcher запускает `global_logger` без фильтрации по имени инструмента.

```python Python theme={null}
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            # Match file modification tools
            HookMatcher(matcher="Write|Edit|NotebookEdit", hooks=[file_security_hook]),
            # Match all MCP tools
            HookMatcher(matcher="^mcp__", hooks=[mcp_audit_hook]),
            # Match everything (no matcher)
            HookMatcher(hooks=[global_logger]),
        ]
    }
)
```

```typescript TypeScript theme={null}
const options = {
  hooks: {
    PreToolUse: [
      // Match file modification tools
      { matcher: "Write|Edit|NotebookEdit", hooks: [fileSecurityHook] },

      // Match all MCP tools
      { matcher: "^mcp__", hooks: [mcpAuditHook] },

      // Match everything (no matcher)
      { hooks: [globalLogger] }
    ]
  }
};
```

### Отслеживание активности подагента

Используйте hooks `SubagentStop` для мониторинга, когда подагенты завершают свою работу. См. полный тип входных данных в справочниках [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#hookinput) и [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#hookinput) SDK. Этот пример логирует сводку каждый раз, когда подагент завершается:

```python Python theme={null}
async def subagent_tracker(input_data, tool_use_id, context):
    # Log subagent details when it finishes
    print(f"[SUBAGENT] Completed: {input_data['agent_id']}")
    print(f"  Transcript: {input_data['agent_transcript_path']}")
    print(f"  Tool use ID: {tool_use_id}")
    print(f"  Stop hook active: {input_data.get('stop_hook_active')}")
    return {}


options = ClaudeAgentOptions(
    hooks={"SubagentStop": [HookMatcher(hooks=[subagent_tracker])]}
)
```

```typescript TypeScript theme={null}
import { HookCallback, SubagentStopHookInput } from "@anthropic-ai/claude-agent-sdk";

const subagentTracker: HookCallback = async (input, toolUseID, { signal }) => {
  // Cast to SubagentStopHookInput to access subagent-specific fields
  const subInput = input as SubagentStopHookInput;

  // Log subagent details when it finishes
  console.log(`[SUBAGENT] Completed: ${subInput.agent_id}`);
  console.log(`  Transcript: ${subInput.agent_transcript_path}`);
  console.log(`  Tool use ID: ${toolUseID}`);
  console.log(`  Stop hook active: ${subInput.stop_hook_active}`);
  return {};
};

const options = {
  hooks: {
    SubagentStop: [{ hooks: [subagentTracker] }]
  }
};
```

Чтобы подтвердить срабатывание hook, зарегистрируйте callback и попросите агента делегировать небольшую задачу подагенту, например список файлов в текущем каталоге: когда подагент завершится, callback выведет строки `[SUBAGENT] Completed:` с ID подагента и путем к транскрипту.

### Выполнение HTTP запросов из hooks

Hooks могут выполнять асинхронные операции, такие как HTTP запросы. Ловите ошибки внутри вашего hook вместо того, чтобы позволить им распространяться.

Этот пример отправляет webhook после завершения каждого инструмента, логируя, какой инструмент запустился и когда. Hook ловит ошибки из неудачного webhook:

```python Python theme={null}
import asyncio
import json
import urllib.request
from datetime import datetime


def _send_webhook(tool_name):
    """Synchronous helper that POSTs tool usage data to an external webhook."""
    data = json.dumps(
        {
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.example.com/webhook",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req)


async def webhook_notifier(input_data, tool_use_id, context):
    # Only fire after a tool completes (PostToolUse), not before
    if input_data["hook_event_name"] != "PostToolUse":
        return {}

    try:
        # Run the blocking HTTP call in a thread to avoid blocking the event loop
        await asyncio.to_thread(_send_webhook, input_data["tool_name"])
    except Exception as e:
        # Log the error but don't raise
        print(f"Webhook request failed: {e}")

    return {}
```

```typescript TypeScript theme={null}
import { query, HookCallback, PostToolUseHookInput } from "@anthropic-ai/claude-agent-sdk";

const webhookNotifier: HookCallback = async (input, toolUseID, { signal }) => {
  // Only fire after a tool completes (PostToolUse), not before
  if (input.hook_event_name !== "PostToolUse") return {};

  try {
    await fetch("https://api.example.com/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tool: (input as PostToolUseHookInput).tool_name,
        timestamp: new Date().toISOString()
      }),
      // Pass signal so the request cancels if the hook times out
      signal
    });
  } catch (error) {
    // Handle cancellation separately from other errors
    if (error instanceof Error && error.name === "AbortError") {
      console.log("Webhook request cancelled");
    }
    // Don't re-throw
  }

  return {};
};

// Register as a PostToolUse hook
for await (const message of query({
  prompt: "Refactor the auth module",
  options: {
    hooks: {
      PostToolUse: [{ hooks: [webhookNotifier] }]
    }
  }
})) {
  console.log(message);
}
```

Чтобы подтвердить срабатывание hook, укажите URL webhook на конечную точку, которую вы можете отслеживать, и отправьте запрос, который использует инструмент: hook отправляет POST с именем инструмента и временной меткой после завершения каждого инструмента.

### Перенаправление уведомлений в Slack

Используйте hooks `Notification` для получения системных уведомлений от агента и перенаправления их во внешние сервисы. В сеансах SDK Claude Code запускает этот hook для следующих типов уведомлений:

* [`permission_prompt`](https://code.claude.com/docs/ru/hooks#notification) один раз, когда запрос разрешения ждал около шести секунд на вашем callback [`canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input). Требуется TypeScript Agent SDK v0.3.233 или позже, или Python Agent SDK v0.2.139 или позже
* `elicitation_complete` и `elicitation_response` для потоков запроса пользователя
* `plugin_notification`, когда [мод](https://code.claude.com/docs/ru/plugins/mods/api.md#show-something-without-starting-a-turn) вызывает `$.ui.notify`

Claude Code выдает другие типы, такие как `idle_prompt`, `auth_success` и `elicitation_dialog`, из интерактивного пользовательского интерфейса, который сеансы SDK не запускают.

Каждое уведомление включает поле `message` с описанием, понятным человеку, и опционально `title`.

Этот пример перенаправляет каждое уведомление в канал Slack. Требуется [URL входящего webhook Slack](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/), который вы создаете, добавляя приложение в ваше рабочее пространство Slack и включая входящие webhooks:

```python Python theme={null}
import asyncio
import json
import urllib.request

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher


def _send_slack_notification(message):
    """Synchronous helper that sends a message to Slack via incoming webhook."""
    data = json.dumps({"text": f"Agent status: {message}"}).encode()
    req = urllib.request.Request(
        "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req)


async def notification_handler(input_data, tool_use_id, context):
    try:
        # Run the blocking HTTP call in a thread to avoid blocking the event loop
        await asyncio.to_thread(_send_slack_notification, input_data.get("message", ""))
    except Exception as e:
        print(f"Failed to send notification: {e}")

    # Return empty object. Notification hooks don't modify agent behavior
    return {}


async def main():
    options = ClaudeAgentOptions(
        hooks={
            # Register the hook for Notification events (no matcher needed)
            "Notification": [HookMatcher(hooks=[notification_handler])],
        },
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Analyze this codebase")
        async for message in client.receive_response():
            print(message)


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query, HookCallback, NotificationHookInput } from "@anthropic-ai/claude-agent-sdk";

// Define a hook callback that sends notifications to Slack
const notificationHandler: HookCallback = async (input, toolUseID, { signal }) => {
  // Cast to NotificationHookInput to access the message field
  const notification = input as NotificationHookInput;

  try {
    // POST the notification message to a Slack incoming webhook
    await fetch("https://hooks.slack.com/services/YOUR/WEBHOOK/URL", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: `Agent status: ${notification.message}`
      }),
      // Pass signal so the request cancels if the hook times out
      signal
    });
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      console.log("Notification cancelled");
    } else {
      console.error("Failed to send notification:", error);
    }
  }

  // Return empty object. Notification hooks don't modify agent behavior
  return {};
};

// Register the hook for Notification events (no matcher needed)
for await (const message of query({
  prompt: "Analyze this codebase",
  options: {
    hooks: {
      Notification: [{ hooks: [notificationHandler] }]
    }
  }
})) {
  console.log(message);
}
```

Когда срабатывает событие `Notification`, hook отправляет `message` уведомления с префиксом `Agent status:` в канал, на который указывает ваш webhook.

## Исправление распространенных проблем

### Хук не срабатывает

* Проверьте, что имя события хука правильное и чувствительно к регистру (`PreToolUse`, а не `preToolUse`)
* Проверьте, что ваш паттерн matcher точно совпадает с именем инструмента
* Убедитесь, что хук находится под правильным типом события в `options.hooks`
* Для хуков, не связанных с инструментами, которые поддерживают matcher, таких как `Notification` и `SubagentStop`, matcher сопоставляется с другими полями, а `Stop` полностью игнорирует matcher (см. [паттерны matcher](https://code.claude.com/docs/ru/hooks.md#matcher-patterns))
* Хуки могут не срабатывать, когда агент достигает лимита [`max_turns`](https://code.claude.com/docs/ru/agent-sdk/python#claudeagentoptions), потому что сессия заканчивается до того, как хуки смогут выполниться

### Matcher не фильтрует как ожидается

Matcher сопоставляется только с именами инструментов, а не с путями файлов или другими аргументами. Для фильтрации по пути файла проверьте `tool_input.file_path` внутри вашего хука:

```typescript theme={null}
const myHook: HookCallback = async (input, toolUseID, { signal }) => {
  const preInput = input as PreToolUseHookInput;
  const toolInput = preInput.tool_input as Record<string, unknown>;
  const filePath = toolInput?.file_path as string;
  if (!filePath?.endsWith(".md")) return {}; // Skip non-markdown files
  // Process markdown files...
  return {};
};
```

### Таймаут хука

Claude Code запускает каждый callback с таймаутом, который вы устанавливаете в секундах с помощью поля `timeout` в его `HookMatcher`. Если вы его не устанавливаете, Claude Code использует значение по умолчанию для события: 600 секунд для большинства событий, 30 секунд для `UserPromptSubmit`, `PreModelSwitch` и `PostModelSwitch` и 10 секунд для `MessageDisplay`. Claude Code запускает callbacks `SessionEnd` во время завершения работы в рамках более короткого [бюджета таймаута SessionEnd](https://code.claude.com/docs/ru/hooks.md#sessionend-input), по умолчанию 1,5 секунды.

Когда callback превышает свой таймаут, Claude Code отменяет его и отбрасывает его выходные данные, и сессия продолжается, а не зависает. Что происходит дальше, зависит от события:

* `PreToolUse`: Claude Code блокирует вызов инструмента. Если все остальные хуки ничего не вернули или вернули только решение `allow`, результат инструмента сообщает Claude, что хук не ответил до истечения таймаута, и ход продолжается. Если другой ваш хук уже отклонил вызов, его отказ все равно доходит до Claude: результат инструмента содержит причину, указанную этим хуком, а за ней может следовать текст о таймауте.

  До версии 2.1.210 Claude Code сообщал Claude о таймауте как об отклонении пользователем, из-за чего автоматические сессии останавливались и ждали ввода.
* `PostToolUse` и `PostToolUseFailure`: Claude Code сохраняет результат инструмента, и ход продолжается.
* `UserPromptSubmit` и [`UserPromptExpansion`](https://code.claude.com/docs/ru/hooks#userpromptexpansion): Claude Code блокирует промпт с сообщением, указывающим хук и таймаут, и сессия продолжается. До версии 2.1.208 Claude Code завершал запрос с `error_during_execution`, когда у callback на этих событиях истекал таймаут.
* `Stop` и `SubagentStop`: callback с истекшим таймаутом считается не вернувшим решения. Агент или субагент останавливается так, как если бы этот callback это разрешил, а решение ваших других хуков на этом событии по-прежнему применяется. До Claude Code версии 2.1.273 callback `Stop` или `SubagentStop` с истекшим таймаутом считался неудачным запуском хука, и Claude Code отбрасывал решения ваших других хуков на этом событии.
* `SessionStart`: callback с истекшим таймаутом считается не вернувшим выходных данных, и сессия продолжается с выходными данными ваших других хуков `SessionStart`.
* `PreModelSwitch`: Claude Code блокирует переключение модели. Хук, который не отвечает, не одобрил переключение.
* Другие события, такие как `Notification`, `PreCompact` и `PostModelSwitch`: Claude Code записывает сбой в лог и продолжает работу. С [`onFailure: "block"`](#block-the-action-when-a-callback-fails) таймаут на `PreCompact`, `Elicitation` или `WorktreeCreate` блокирует действие.

Когда у callback `Stop` или `SessionStart` впервые истекает таймаут в основной сессии, Claude Code также добавляет в поток сообщений [`SDKInformationalMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkinformationalmessage) о том, что приложение, управляющее сессией, не ответило. Последующие таймауты не повторяют это сообщение, пока ваше приложение остается неотвечающим.

Если вы прерываете запрос во время ожидания callback, Claude Code отменяет ожидающий вызов инструмента. До версии 2.1.208 вызов инструмента мог все же выполниться, если вы прерывали запрос во время ожидания callback `PreToolUse`.

Если вашему callback нужно больше времени, установите более высокий `timeout` в его `HookMatcher`. В TypeScript используйте `AbortSignal` из третьего аргумента callback для корректной обработки отмены при срабатывании таймаута.

### Инструмент заблокирован неожиданно

* Проверьте все хуки `PreToolUse` на возвращение `permissionDecision: 'deny'`
* Добавьте логирование в ваши хуки, чтобы увидеть, какие `permissionDecisionReason` они возвращают
* Проверьте, что паттерны matcher не слишком широкие: пустой matcher соответствует всем инструментам

### Измененные входные данные не применяются

* Убедитесь, что `updatedInput` находится внутри `hookSpecificOutput`, а не на верхнем уровне:

  ```typescript theme={null}
  return {
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      updatedInput: { command: "new command" }
    }
  };
  ```

* Не объединяйте `updatedInput` с `permissionDecision: 'defer'`, так как это отбрасывает измененные входные данные. Опускать `permissionDecision` допустимо: измененные входные данные все равно применяются через обычную оценку разрешений. Вы также можете вернуть `'allow'` для автоматического одобрения измененных входных данных или `'ask'`, чтобы показать их пользователю для подтверждения

* Включите `hookEventName` в `hookSpecificOutput`, чтобы указать, к какому типу хука относится вывод

### Хуки сессии недоступны в Python

`SessionStart` и `SessionEnd` можно зарегистрировать как callback-хуки SDK в TypeScript, но они недоступны в Python SDK, потому что его тип `HookEvent` их не включает. В Python они доступны только как [хуки shell-команд](https://code.claude.com/docs/ru/hooks.md#hook-events), определенные в файлах настроек, таких как `.claude/settings.json`. То, какие файлы настроек загружает ваше приложение SDK, зависит от [`setting_sources`](https://code.claude.com/docs/ru/agent-sdk/python#settingsource) или [`settingSources`](https://code.claude.com/docs/ru/agent-sdk/typescript#settingsource). Если вы задаете этот параметр, включите источник, который содержит хуки:

```python Python theme={null}
options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads .claude/settings.json including hooks
)
```

```typescript TypeScript theme={null}
const options = {
  settingSources: ["project"] // Loads .claude/settings.json including hooks
};
```

Чтобы вместо этого запускать логику инициализации как callback Python SDK, используйте первое сообщение из `client.receive_response()` в качестве триггера.

### Запросы разрешений субагентов множатся

При порождении нескольких субагентов каждый из них может запрашивать разрешения отдельно для своих собственных вызовов инструментов. Чтобы избежать повторных запросов, используйте хуки `PreToolUse` для автоматического одобрения конкретных инструментов или настройте правила разрешений, которые субагенты [наследуют от родительского диалога](https://code.claude.com/docs/ru/sub-agents.md#permission-modes).

### Рекурсивные циклы хуков с субагентами

Хук `UserPromptSubmit`, который порождает субагентов, может создать бесконечные циклы, если эти субагенты вызывают срабатывание того же хука. Чтобы предотвратить это:

* Используйте общую переменную или состояние сессии для отслеживания того, находитесь ли вы уже внутри субагента
* Ограничьте хуки, чтобы они запускались только для сессии агента верхнего уровня

### systemMessage не появляется в выводе

Поле `systemMessage` показывает сообщение пользователю, а не модели. В Claude Code версии 2.1.227 или новее `systemMessage` хука может появиться в потоке сообщений как [`SDKInformationalMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkinformationalmessage). Появится ли оно, зависит от события. В [разделе каждого события](https://code.claude.com/docs/ru/hooks.md#hook-events) на странице хуков описано, как выводится результат. Чтобы вместо этого передать контекст модели, верните [`additionalContext`](https://code.claude.com/docs/ru/hooks#add-context-for-claude).

До версии 2.1.227 SDK выводил выходные данные хука в поток сообщений только для хуков `SessionStart` и `Setup`. Для любого другого события выходные данные появлялись только в событиях жизненного цикла, которые добавляет [`includeHookEvents`](https://code.claude.com/docs/ru/agent-sdk/typescript#options) (`include_hook_events` в Python). В описании этого параметра указано, какие события жизненного цикла порождает каждое событие хука.

Если вам нужно надежно передавать решения хуков в ваше приложение, логируйте их отдельно или используйте выделенный канал вывода.

## Связанные ресурсы

* [Справочник hooks Claude Code](https://code.claude.com/docs/ru/hooks.md): полные схемы входных/выходных данных JSON, документация событий и паттерны matcher
* [Руководство hooks Claude Code](https://code.claude.com/docs/ru/hooks-guide.md): примеры hooks команд shell и пошаговые инструкции
* [Справочник TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md): типы hooks, определения входных/выходных данных и параметры конфигурации
* [Справочник Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md): типы hooks, определения входных/выходных данных и параметры конфигурации
* [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md): контролируйте, что может делать ваш агент
* [Пользовательские инструменты](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md): создавайте инструменты для расширения возможностей агента
