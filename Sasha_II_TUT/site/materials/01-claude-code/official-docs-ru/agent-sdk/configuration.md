> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка вашего агента

> Настройте сеансы Agent SDK: составьте объект параметров, установите модель, окружение и ограничения, и найдите страницу каждого параметра функции.

Сеанс Agent SDK читает конфигурацию из файлов настроек, переменных окружения и объекта `options`, который вы передаёте при его запуске. На этой странице показано, как составить объект `options` и какие файлы настроек и переменные окружения его контролируют.

Для каждого параметра его типа и значения по умолчанию см. ссылки [`Options`](https://code.claude.com/docs/ru/agent-sdk/typescript#options) (TypeScript) и [`ClaudeAgentOptions`](https://code.claude.com/docs/ru/agent-sdk/python#claudeagentoptions) (Python).

## Передача параметров в сеанс

Каждый вызов `query()` принимает объект параметров: `Options` в TypeScript, `ClaudeAgentOptions` в Python. Каждое поле является необязательным, и сеанс, запущенный без параметров, работает с значениями по умолчанию SDK. Пример ниже настраивает сеанс только для чтения, который суммирует открытые TODO проекта. Пары читаются как TypeScript / Python, где написание отличается:

* **`model`**: выбирает модель
* **`allowedTools` / `allowed_tools`**: предварительно одобряет список инструментов только для чтения
* **`maxTurns` / `max_turns`**: ограничивает количество ходов
* **`cwd`**: устанавливает рабочий каталог

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Summarize the open TODOs in this repo",
  options: {
    model: "claude-sonnet-5",
    allowedTools: ["Read", "Glob", "Grep"],
    maxTurns: 8,
    cwd: "/path/to/repo",
  },
})) {
  if (message.type === "result" && message.subtype === "success" && !message.is_error) {
    console.log(message.result);
  }
}
```

```python Python theme={null}
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

async def main():
    options = ClaudeAgentOptions(
        model="claude-sonnet-5",
        allowed_tools=["Read", "Glob", "Grep"],
        max_turns=8,
        cwd="/path/to/repo",
    )

    async for message in query(
        prompt="Summarize the open TODOs in this repo",
        options=options,
    ):
        if isinstance(message, ResultMessage) and not message.is_error:
            print(message.result)

asyncio.run(main())
```

Укажите `cwd` на один из ваших собственных проектов и запустите пример. Сводка открытых TODO этого проекта выводится при поступлении сообщения результата.

`allowedTools` (TypeScript) или `allowed_tools` (Python) предварительно одобряет перечисленные инструменты, поэтому вызовы к ним выполняются без остановки для одобрения. Инструменты вне списка остаются доступными. Когда Claude вызывает инструмент, не указанный в списке, режим разрешений определяет, будет ли вызов выполнен. Для получения дополнительной информации см. [Правила разрешения и запрета](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules).

## Загрузка файлов настроек

Файлы настроек предоставляют конфигурацию за пределами объекта параметров. Два параметра контролируют способ их загрузки:

* **`settingSources` / `setting_sources`**: контролирует, какие источники файловой системы загружаются: пользователь, проект и локальный. Файлы настроек и файлы CLAUDE.md поступают через эти источники.
* **`settings`**: загружает путь файла настроек или встроенную строку JSON на любом языке, и TypeScript также принимает объект настроек. Какую бы форму вы ни передали, она переопределяет пользовательские, проектные и локальные настройки файловой системы; только управляемые политики имеют более высокий приоритет. Ссылки документируют полный порядок приоритета в разделе [Приоритет настроек](https://code.claude.com/docs/ru/agent-sdk/typescript.md#settings-precedence) для TypeScript и [Приоритет настроек](https://code.claude.com/docs/ru/agent-sdk/python.md#settings-precedence) для Python.

Передайте `[]` для отключения пользовательских, проектных и локальных настроек. Для получения дополнительной информации см. [Использование функций Claude Code в SDK](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md).

## Выбор модели

Если параметр `model`, ваши настройки или окружение не выбирают модель, новый сеанс запускается на [модели по умолчанию Claude Code](https://code.claude.com/docs/ru/model-config.md#default-model-setting). Для порядка этих источников см. [Установка вашей модели](https://code.claude.com/docs/ru/model-config.md#setting-your-model). Установите `model` для закрепления определённой модели или выберите меньшую для более быстрых и дешёвых агентов. Значение принимает псевдоним модели или полное имя модели; псевдонимы и версии, на которые они разрешаются, перечислены в разделе [Псевдонимы моделей](https://code.claude.com/docs/ru/model-config.md#model-aliases).

Установите `fallbackModel` (TypeScript) или `fallback_model` (Python) для указания резервной модели. Когда основная модель перегружена или недоступна, сеанс переключается на резервную. Основная модель повторяется в начале каждого хода пользователя, поэтому сеанс возвращается к ней после окончания сбоя.

На обоих языках параметр принимает одну модель или разделённый запятыми список резервных копий. Для порядка и ограничения цепи см. [Цепи резервных моделей](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains). В TypeScript резервная копия, равная `model`, вызывает ошибку при запуске.

Примеры ниже показывают список резервных копий в TypeScript и одну резервную копию в Python:

```typescript TypeScript theme={null}
const options = {
  model: "claude-fable-5",
  fallbackModel: "claude-opus-5,claude-sonnet-5",
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    model="claude-fable-5",
    fallback_model="claude-opus-5",
)
```

> [!NOTE]
>
> Параметры запроса [Messages API](https://platform.claude.com/docs/en/api/messages) `temperature`, `top_p` и `max_tokens` не имеют полей в объекте параметров ни на одном языке. Установите [уровень усилий](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#effort-level) или [ограничение расходов](#limit-turns-and-spend) вместо этого, или вызовите Messages API, когда вам нужны эти параметры напрямую.

## Установка переменных окружения

Параметр `env` устанавливает переменные окружения для процесса Claude Code, который запускает ваш сеанс. Различаются ли ваши значения заменяют унаследованное окружение или объединяются с ним в зависимости от языка:

* **TypeScript**: `env` заменяет окружение подпроцесса
* **Python**: SDK объединяет ваши значения с унаследованным окружением, и ваши значения переопределяют унаследованные

В TypeScript распределите `process.env` в `env` для сохранения унаследованных переменных, таких как `PATH`, `HOME` и `ANTHROPIC_API_KEY`. Когда вы оставляете `env` неустановленным, подпроцесс наследует ваше окружение на обоих языках.

Пример маршрутизирует трафик API через шлюз путём установки `ANTHROPIC_BASE_URL`.

```typescript TypeScript theme={null}
const options = {
  env: { ...process.env, ANTHROPIC_BASE_URL: "https://gateway.example.com" },
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    env={"ANTHROPIC_BASE_URL": "https://gateway.example.com"},
)
```

Переменные, которые вы передаёте, также могут настраивать сам Claude Code. Для переменных, которые читает процесс Claude Code, см. [Переменные окружения](https://code.claude.com/docs/ru/env-vars.md). Для настройки тайм-аутов API и обнаружения зависания таким образом следуйте разделу Handle slow or stalled API responses в [справочнике TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#handle-slow-or-stalled-api-responses) или [справочнике Python](https://code.claude.com/docs/ru/agent-sdk/python.md#handle-slow-or-stalled-api-responses).

## Установка рабочего каталога

Установите `cwd` для запуска сеанса в определённом каталоге. Когда вы оставляете `cwd` неустановленным, сеанс запускается в рабочем каталоге вашего процесса. Ни один SDK не имеет установщика для `cwd`. Для запуска в другом каталоге запустите другой сеанс с этим `cwd`.

Claude Code читает рабочий каталог для определения:

* **Настройки проекта и hooks**: какие [настройки и hooks проекта загружаются](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md)
* **Skills**: где [обнаруживаются skills сеанса](https://code.claude.com/docs/ru/agent-sdk/skills.md)
* **Хранилище сеанса**: какому проекту [принадлежит сохранённый сеанс](https://code.claude.com/docs/ru/agent-sdk/session-storage.md)

Чтобы позволить инструментам получать доступ к файлам вне рабочего каталога, добавьте пути с помощью `additionalDirectories` (TypeScript) или `add_dirs` (Python). Для области этого разрешения см. [Дополнительные каталоги предоставляют доступ к файлам, а не конфигурацию](https://code.claude.com/docs/ru/permissions.md#additional-directories-grant-file-access-not-configuration).

## Ограничение ходов и расходов

Ограничьте ходы и расходы с помощью `maxTurns` / `max_turns` и `maxBudgetUsd` / `max_budget_usd`. Оба ограничения отключены, когда не установлены. Когда сессия достигает ограничения, запуск заканчивается сообщением результата. Подтип результата — `error_max_turns` для ограничения ходов и `error_max_budget_usd` для ограничения расходов. Одноразовый и потоковый ввод обрабатывают результат ограничения по-разному:

* **Одноразовый `query()`**: SDK выдаёт результат ограничения, а затем вызывает исключение, поэтому оберните цикл в блок try для продолжения после ошибки
* **Потоковый ввод**: сессия остаётся активной после результата ограничения, и счётчик максимальных ходов начинается заново для каждого сообщения в очереди. Общий бюджет накапливается по сообщениям, и как только расходы достигают ограничения, более поздние сообщения в том же диалоге заканчиваются тем же результатом бюджета. [`/clear`](https://code.claude.com/docs/ru/agent-sdk/cost-tracking) начинает бюджет заново.
* **Потоковый ввод в TypeScript**: цикл выбрасывает исключение, когда последний ответ заканчивается результатом с ошибкой, например `error_max_turns`. Оберните цикл в блок try, чтобы продолжить после него.

Два ограничения обрабатывают `0` по-разному:

* **`maxTurns` / `max_turns`**: `0` запускает сеанс без ограничения ходов, то же самое, что оставить параметр неустановленным
* **`maxBudgetUsd` / `max_budget_usd`**: CLI отклоняет `0` как недопустимую сумму при запуске, и сеанс никогда не запускается

Для получения дополнительной информации об обоих ограничениях, включая расходы подагентов, см. [Ходы и бюджет](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#turns-and-budget).

## Изменение конфигурации во время сеанса

Когда вы запускаете сеанс с [потоковым вводом](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md), вы можете переключать его модель и режим разрешений во время его работы. Где вы вызываете установщики, зависит от языка:

* **TypeScript**: методы на объекте, который возвращает `query()`
* **Python**: методы на [`ClaudeSDKClient`](https://code.claude.com/docs/ru/agent-sdk/python#claudesdkclient), так как `query()` возвращает простой итератор без методов управления

Оба языка имеют одинаковые установщики:

* **`setModel()` / `set_model()`**: переключает модель. Вызовите её без модели для переключения на [модель по умолчанию Claude Code](https://code.claude.com/docs/ru/model-config.md#default-model-setting) вместо `model`, которую вы передали в параметрах. Если сессия находится в авторежиме и вы переключаетесь на модель, которую авторежим не поддерживает, сессия переходит в режим `default`. Чтобы вернуться в авторежим, см. [Авторежим (`auto`)](https://code.claude.com/docs/ru/agent-sdk/permissions#auto-mode-auto).
* **`setPermissionMode()` / `set_permission_mode()`**: переключает режим разрешений

TypeScript также имеет `applyFlagSettings()` и `updateSettings()`:

* **`applyFlagSettings()`**: применяет настройки во время выполнения, как в `await session.applyFlagSettings({ effortLevel: "high" })`. Метод принимает ключи файла настроек, а не поля параметров, поэтому проверьте [справочник `applyFlagSettings()`](https://code.claude.com/docs/ru/agent-sdk/typescript#applyflagsettings) для схемы и для того, какие ключи вступают в силу во время сеанса.
* **`updateSettings()`**: записывает один разрешённый ключ в файл настроек. [Справочник `updateSettings()`](https://code.claude.com/docs/ru/agent-sdk/typescript#updatesettings) называет ключ, который принимает каждый источник, и минимальные версии.
  * Передайте `"localSettings"` для записи в файл локальных настроек проекта, как в `await session.updateSettings("localSettings", { outputStyle: "Explanatory" })`. Записанный ключ вступает в силу при следующем запросе сеанса и сохраняется для более поздних сеансов, которые загружают настройки `local`.
  * Передайте `"userSettings"` для записи `effortLevel`, единственного ключа, который принимает этот источник. Claude Code сохраняет его как уровень усилий по умолчанию для текущей модели сеанса, и усилия работающего сеанса не изменяются.

Пример ниже запускает двухходовой сеанс, изменяет конфигурацию между ходами и выводит модель, которая ответила на каждый ход. В TypeScript поток подсказок удерживает второе сообщение до тех пор, пока установщики не будут запущены, и второй ход выполняется на новой модели.

```typescript TypeScript theme={null}
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

function userMessage(text: string): SDKUserMessage {
  return { type: "user", message: { role: "user", content: text }, parent_tool_use_id: null };
}

// Hold the second prompt until the setters have run.
let startSecondTurn!: () => void;
const secondTurnReady = new Promise<void>((resolve) => {
  startSecondTurn = resolve;
});

async function* turnPrompts(): AsyncGenerator<SDKUserMessage, void> {
  yield userMessage("Reply with exactly: ready");
  await secondTurnReady;
  yield userMessage("Reply with exactly: done");
}

const session = query({
  prompt: turnPrompts(),
  options: {
    model: "claude-sonnet-5",
  },
});

let turnModel = "";
let completedTurns = 0;

for await (const message of session) {
  if (message.type === "assistant") {
    turnModel = message.message.model;
  } else if (message.type === "result") {
    completedTurns += 1;
    if (completedTurns === 1) {
      console.log(`First turn model: ${turnModel}`);
      await session.setModel("claude-opus-5");
      await session.setPermissionMode("acceptEdits");
      startSecondTurn();
    } else {
      console.log(`Second turn model: ${turnModel}`);
      break;
    }
  }
}
```

```python Python theme={null}
import asyncio

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient

async def main():
    options = ClaudeAgentOptions(model="claude-sonnet-5")

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Reply with exactly: ready")
        first_model = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                first_model = message.model

        await client.set_model("claude-opus-5")
        await client.set_permission_mode("acceptEdits")

        await client.query("Reply with exactly: done")
        second_model = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                second_model = message.model

    print(f"First turn model: {first_model}")
    print(f"Second turn model: {second_model}")

asyncio.run(main())
```

На Claude API программа выводит `First turn model: claude-sonnet-5`, затем `Second turn model: claude-opus-5` после переключения.

> [!NOTE]
>
> Каждая модель имеет свой собственный кэш подсказок, поэтому после переключения во время сеанса следующий запрос пересчитывает полный разговор без кэша по ставкам новой модели. Для получения дополнительной информации см. [Переключение моделей](https://code.claude.com/docs/ru/prompt-caching.md#switching-models).

## Настройка конкретных функций

Таблица ниже сопоставляет каждый параметр с функцией, которую он настраивает. Для параметров, которые эта страница не охватывает, см. [справочники TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#options) и [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#claudeagentoptions). Если вы знаете вашу цель, но не знаете, какой параметр её обслуживает, начните с [Выбор правильной функции](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#choose-the-right-feature).

| TypeScript | Python | Контролирует | Охватывается в |
| - | - | - | - |
| `permissionMode` | `permission_mode` | Что агент может делать без одобрения | [Настройка разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md) |
| `allowedTools` | `allowed_tools` | Какие вызовы инструментов предварительно одобрены | [Настройка разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md) |
| `canUseTool` | `can_use_tool` | Ваш обратный вызов одобрения для вызовов инструментов | [Обработка запросов одобрения инструментов](https://code.claude.com/docs/ru/agent-sdk/user-input.md#handle-tool-approval-requests) |
| `systemPrompt` | `system_prompt` | Инструкции агента | [Изменение системных подсказок](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md) |
| `settingSources` | `setting_sources` | Какие настройки файловой системы загружаются | [Использование функций Claude Code в SDK](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md) |
| `mcpServers` | `mcp_servers` | Серверы внешних инструментов | [Подключение к внешним инструментам с MCP](https://code.claude.com/docs/ru/agent-sdk/mcp.md) |
| `agents` | `agents` | Определения подагентов | [Подагенты](https://code.claude.com/docs/ru/agent-sdk/subagents.md) |
| `hooks` | `hooks` | Обратные вызовы в точках жизненного цикла | [Hooks](https://code.claude.com/docs/ru/agent-sdk/hooks.md) |
| `skills` | `skills` | Какие skills загружаются | [Расширение агентов с помощью skills](https://code.claude.com/docs/ru/agent-sdk/skills.md) |
| `plugins` | `plugins` | Какие plugins загружаются | [Plugins](https://code.claude.com/docs/ru/agent-sdk/plugins.md) |
| `outputFormat` | `output_format` | Схемы структурированного вывода | [Структурированные выводы](https://code.claude.com/docs/ru/agent-sdk/structured-outputs.md) |
| `resume` | `resume` | Продолжение сохранённого сеанса | [Сеансы](https://code.claude.com/docs/ru/agent-sdk/sessions.md) |
| `forkSession` | `fork_session` | Ветвление сеанса | [Сеансы](https://code.claude.com/docs/ru/agent-sdk/sessions.md) |
| `sessionStore` | `session_store` | Внешнее сохранение сеанса | [Хранилище сеанса](https://code.claude.com/docs/ru/agent-sdk/session-storage.md) |
| `enableFileCheckpointing` | `enable_file_checkpointing` | Редактируемые файлы с возможностью отката | [File checkpointing](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) |
| `effort` | `effort` | Сколько работы Claude вкладывает в ответы | [Уровень усилий](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#effort-level) |
| `sandbox` | `sandbox` | Поведение sandbox для выполнения инструментов | [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#sandbox-configuration) и [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#sandbox-configuration) справочники, с контекстом развёртывания в [Безопасное развёртывание](https://code.claude.com/docs/ru/agent-sdk/secure-deployment.md) |

## Следующие шаги

Чтобы увидеть конфигурацию, составленную в рабочих агентов:

* **[Quickstart](https://code.claude.com/docs/ru/agent-sdk/quickstart.md)**: создайте и запустите первого агента от начала до конца
* **[Примеры](https://code.claude.com/docs/ru/agent-sdk/examples.md)**: найдите полный, запускаемый проект или управляемый рецепт Claude Cookbook, который соответствует тому, что вы хотите создать
* **[Изоляция мультитенантности](https://code.claude.com/docs/ru/agent-sdk/hosting.md#multi-tenant-isolation)**: изолируйте настройки и память каждого тенанта с помощью `settingSources` / `setting_sources`, `env` и `cwd`
