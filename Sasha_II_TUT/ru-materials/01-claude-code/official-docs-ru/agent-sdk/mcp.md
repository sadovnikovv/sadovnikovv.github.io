> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Подключение к внешним инструментам с помощью MCP

> Настройте MCP серверы для расширения вашего агента внешними инструментами. Охватывает типы транспорта, поиск инструментов для больших наборов инструментов, аутентификацию и обработку ошибок.

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) — это открытый стандарт для подключения AI агентов к внешним инструментам и источникам данных. С помощью MCP ваш агент может запрашивать базы данных, интегрироваться с API, такими как Slack и GitHub, и подключаться к другим сервисам без написания пользовательских реализаций инструментов.

MCP серверы могут работать как локальные процессы, подключаться через HTTP или выполняться непосредственно в вашем приложении SDK.

> [!NOTE]
>
> На этой странице рассматривается конфигурация MCP для Agent SDK. Чтобы добавить MCP серверы в Claude Code CLI так, чтобы они загружались в каждом проекте, см. [Области установки MCP](https://code.claude.com/docs/ru/mcp.md#mcp-installation-scopes).

## Быстрый старт

Этот пример подключается к MCP серверу [документации Claude Code](https://code.claude.com/docs) с использованием [HTTP транспорта](#http%2Fsse-servers) и использует [`allowedTools`](#allow-mcp-tools) с подстановочным знаком для разрешения всех инструментов с сервера.

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the docs MCP server to explain what hooks are in Claude Code",
  options: {
    mcpServers: {
      "claude-code-docs": {
        type: "http",
        url: "https://code.claude.com/docs/mcp"
      }
    },
    allowedTools: ["mcp__claude-code-docs__*"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "claude-code-docs": {
                "type": "http",
                "url": "https://code.claude.com/docs/mcp",
            }
        },
        allowed_tools=["mcp__claude-code-docs__*"],
    )

    async for message in query(
        prompt="Use the docs MCP server to explain what hooks are in Claude Code",
        options=options,
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

Агент подключается к серверу документации, ищет информацию о hooks и возвращает результаты.

## Добавить MCP сервер

Вы можете настроить MCP серверы в коде при вызове `query()`, или в файле `.mcp.json`, загруженном через [`settingSources`](#from-a-config-file).

### Добавление сервера в коде

Передайте MCP серверы непосредственно в опции `mcpServers`. Этот пример запускает локальный файловый MCP сервер для `/Users/me/projects`. Замените этот путь на директорию на вашей машине:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List files in my project",
  options: {
    mcpServers: {
      filesystem: {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
      }
    },
    allowedTools: ["mcp__filesystem__*"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "/Users/me/projects",
                ],
            }
        },
        allowed_tools=["mcp__filesystem__*"],
    )

    async for message in query(prompt="List files in my project", options=options):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

### Добавление сервера из файла конфигурации

Создайте файл `.mcp.json` в корне вашего проекта. Файл загружается, когда включен источник настроек `project`, что происходит по умолчанию для опций `query()`. Если вы явно установите `settingSources`, включите `"project"` для загрузки этого файла. Замените `/Users/me/projects` на директорию на вашей машине:

```json theme={null}
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    }
  }
}
```

## Время подключения

Claude Code начинает подключать ваши MCP-серверы при запуске сессии и отправляет [сообщение инициализации](#error-handling), как только заканчивается ожидание первого хода, если оно есть. Сколько первый ход ждёт сервер, зависит от того, где вы его настроили. Если вы задали `permissionPromptToolName`, первый ход всегда ждёт сервер этого инструмента, до `MCP_TIMEOUT`, независимо от того, где вы его настроили.

Для сервера в `options.mcpServers` найдите его тип в первом столбце, чтобы узнать, сколько первый ход его ждёт.

| Тип сервера | Задерживает первый ход? | Тайм-аут ожидания первого хода |
| :- | :- | :- |
| Сервер stdio или HTTP/SSE сервер без кэшированного списка инструментов | Да, до подключения | [`MCP_TIMEOUT`](https://code.claude.com/docs/ru/env-vars), по умолчанию 30 секунд; подключение завершается ошибкой в этот момент |
| Удалённый сервер с кэшированным списком инструментов, сохранённый Claude Code из предыдущего подключения | Нет; кэшированные инструменты доступны с первого хода | Нет; подключается при первом вызове инструмента, и это отложенное подключение имеет собственный тайм-аут |
| In-process [SDK сервер](#sdk-mcp-servers) | Да, до подключения и получения списка инструментов | [`MCP_TIMEOUT`](https://code.claude.com/docs/ru/env-vars), по умолчанию 30 секунд, за попытку подключения; подключение завершается ошибкой в этот момент |

Кэшированный список инструментов есть у сервера, только когда включён [кэш обнаружения MCP](https://code.claude.com/docs/ru/mcp.md#server-status-detail).

Серверы из [файлов настроек](#from-a-config-file), таких как `.mcp.json`, или из плагинов часто всё ещё показывают `pending` в сообщении инициализации. Сколько первый ход их ждёт, зависит от `options.mcpServers` и поиска инструментов:

* **`options.mcpServers` содержит сервер stdio, HTTP или SSE**: первый ход ждёт также ожидающие серверы из файлов настроек и плагинов, до `MCP_TIMEOUT`.
* **Иначе, когда `ANTHROPIC_BASE_URL` указывает на [шлюз](https://code.claude.com/docs/ru/mcp.md#tool-search-through-a-gateway), а [`ENABLE_TOOL_SEARCH`](https://code.claude.com/docs/ru/mcp#configure-tool-search) не задана**: первый ход ждёт до 2 секунд каждый ожидающий сервер из файлов настроек и плагинов.
* **Иначе, с включённым [поиском инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md), что является значением по умолчанию**: первый ход ждёт до 2 секунд и только ожидающие серверы, для которых задано [`alwaysLoad: true`](https://code.claude.com/docs/ru/mcp#exempt-a-server-from-deferral) или которые вы [назвали](#named-servers). Остальные продолжают подключаться в фоновом режиме, и Claude [получает доступ к их инструментам](https://code.claude.com/docs/ru/mcp.md#tool-availability), как только они подключатся.
* **Иначе, с отключённым поиском инструментов**: первый ход ждёт до 2 секунд каждый ожидающий сервер из файлов настроек и плагинов. Поиск инструментов отключён, когда его отключает ваше [значение `ENABLE_TOOL_SEARCH` или модель](https://code.claude.com/docs/ru/agent-sdk/tool-search#configure-tool-search), или когда вы исключаете инструмент `ToolSearch`, например через `disallowedTools`.

### Названные серверы

Вы называете сервер, указав любой из его инструментов, например `mcp__github__list_issues` или `mcp__github__*`, в [`allowedTools`](#allow-mcp-tools) или в правиле `permissions.allow` в опции `settings`. [Хук `mcp_tool`](https://code.claude.com/docs/ru/hooks#mcp-tool-hook-fields) также называет сервер, который он вызывает, когда вы настраиваете его на событие отправки промпта, использования инструмента, разрешения, субагента, задачи, elicitation или worktree. До версии 2.1.284 указание сервера не влияло на ожидание первого хода.

### Самостоятельная настройка ожидания первого хода

Чтобы задать ожидание первого хода самостоятельно, установите `CLAUDE_CODE_MCP_STARTUP_WAIT_MS` в [опции `env`](https://code.claude.com/docs/ru/agent-sdk/configuration#set-environment-variables), например `CLAUDE_CODE_MCP_STARTUP_WAIT_MS: "5000"`. Тогда первый ход ждёт ожидающие серверы из файлов настроек и плагинов до указанного количества миллисекунд, независимо от того, включён ли поиск инструментов. Тот же предел заменяет ожидание `MCP_TIMEOUT` для серверов stdio, HTTP и SSE в `options.mcpServers`.

Три ожидания действуют при любом заданном значении, включая `0`:

* **Сервер `permissionPromptToolName`**: до `MCP_TIMEOUT`.
* **In-process [SDK-сервер](#sdk-mcp-servers)**: до `MCP_TIMEOUT` за попытку подключения.
* **Всё ещё подключающийся [названный сервер](#named-servers)**: не менее 2 секунд, поэтому значение ниже `2000` не сокращает его ожидание.

Установите переменную в `0`, чтобы пропустить ожидание для всех остальных серверов. Серверы, которые всё ещё ожидают, когда ожидание заканчивается, продолжают подключаться в фоновом режиме. `CLAUDE_CODE_MCP_STARTUP_WAIT_MS` требует Claude Code версии 2.1.274 или новее.

### Ожидание серверов при запуске

Две настройки заставляют ждать сам запуск, до того как Claude Code отправит сообщение инициализации:

* **[`MCP_CONNECTION_NONBLOCKING`](https://code.claude.com/docs/ru/env-vars) со значением `0`**: запуск ждёт всю партию подключений, по умолчанию до 5 секунд. Чтобы изменить этот предел, задайте [`MCP_CONNECT_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars) в миллисекундах. Серверы, которые всё ещё ожидают при достижении предела, продолжают подключаться в фоновом режиме.
* **`alwaysLoad: true` в конфигурации сервера**: запуск ждёт инструменты этого сервера до того же предела, чтобы на первом ходе они были доступны с полными схемами, [исключёнными из отложенной загрузки поиска инструментов](https://code.claude.com/docs/ru/mcp.md#exempt-a-server-from-deferral). Удалённый сервер с кэшированным списком инструментов предоставляет их без подключения и без задержки запуска.

Сообщение инициализации сообщает статус каждого сервера на момент, когда Claude Code его отправляет.

## Разрешить инструменты MCP

Инструменты MCP требуют явного разрешения перед тем, как Claude сможет их использовать. Без разрешения Claude увидит, что инструменты доступны, но не сможет их вызывать.

### Соглашение об именовании инструментов

Инструменты MCP именуются как `mcp__<server-name>__<tool-name>`, где `<server-name>` — это имя, под которым вы регистрируете сервер, например его ключ в `mcpServers`.

Символы в имени сервера, такие как `.` и пробелы, заменяются на `_`. В этой таблице показано полное имя инструмента `list_issues` для двух ключей сервера:

| Ключ в `mcpServers` | Полное имя инструмента |
| :- | :- |
| `github` | `mcp__github__list_issues` |
| `my.server` | `mcp__my_server__list_issues` |

Используйте полные имена инструментов в `allowedTools` и в [правилах разрешений MCP](https://code.claude.com/docs/ru/permissions.md#mcp). Для сервера, который предоставляет [плагин](https://code.claude.com/docs/ru/agent-sdk/plugins.md), `<server-name>` принимает [форму с областью плагина](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers) и начинается с `plugin_`.

### Автоматическое одобрение с allowedTools

Используйте `allowedTools` для автоматического одобрения определённых инструментов MCP:

```typescript TypeScript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      // your servers
    },
    allowedTools: [
      "mcp__github__*", // All tools from the github server
      "mcp__db__query", // Only the query tool from db server
      "mcp__slack__send_message" // Only send_message from slack server
    ]
  }
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        # your servers
    },
    allowed_tools=[
        "mcp__github__*",  # All tools from the github server
        "mcp__db__query",  # Only the query tool from db server
        "mcp__slack__send_message",  # Only send_message from slack server
    ],
)
```

Подстановочные знаки (`*`) позволяют вам разрешить все инструменты с сервера без перечисления каждого отдельно.

> [!NOTE]
>
> **Предпочитайте `allowedTools` режимам разрешений для доступа MCP.** `permissionMode: "acceptEdits"` не одобряет автоматически инструменты MCP (только редактирование файлов и команды Bash файловой системы). `permissionMode: "bypassPermissions"` одобряет автоматически инструменты MCP, но также отключает большинство других запросов безопасности, что шире, чем необходимо; см. [Как оцениваются разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated) для запросов, которые остаются. Подстановочный знак в `allowedTools` предоставляет ровно тот сервер MCP, который вам нужен, и ничего больше. См. [Режимы разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#permission-modes) для полного сравнения.

### Обнаружение доступных инструментов

Чтобы увидеть, какие инструменты предоставляет сервер MCP, проверьте документацию сервера или проверьте массив `tools` в инициализирующем сообщении `system`. Имена инструментов MCP начинаются с `mcp__`.

Claude Code выдаёт инициализирующее сообщение после [ожидания подключения на первом ходу](#connection-timing) для серверов, переданных в `options.mcpServers`, поэтому массив `tools` содержит инструменты `mcp__` каждого сервера, который подключился к этому моменту, плюс те, у которых есть [кэшированный список инструментов](#connection-timing), которые подключаются при первом использовании. Инструменты любого другого сервера, который ещё не подключился, отсутствуют; см. [Обработка ошибок](#error-handling) для чтения статуса каждого сервера.

Этот фильтр выводит имена инструментов MCP:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const options = {
  mcpServers: {
    // your servers
  },
};

for await (const message of query({ prompt: "...", options })) {
  if (message.type === "system" && message.subtype === "init") {
    const mcpTools = message.tools.filter((name) => name.startsWith("mcp__"));
    console.log("Available MCP tools:", mcpTools);
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            # your servers
        },
    )
    async for message in query(prompt="...", options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            mcp_tools = [t for t in message.data.get("tools", []) if t.startswith("mcp__")]
            print("Available MCP tools:", mcp_tools)


asyncio.run(main())
```

Вы также можете попросить Claude перечислить инструменты, доступные с сервера.

## Типы транспорта

MCP серверы взаимодействуют с вашим агентом, используя различные протоколы транспорта. Проверьте документацию сервера, чтобы узнать, какой транспорт он поддерживает:

* Если в документации указана **команда для запуска** (например, `npx @modelcontextprotocol/server-filesystem`), используйте stdio
* Если в документации указан **URL**, используйте HTTP или SSE
* Если вы создаёте свои собственные инструменты в коде, используйте SDK MCP сервер

### stdio серверы

Локальные процессы, которые взаимодействуют через stdin/stdout. Используйте это для MCP-серверов, которые вы запускаете на одной машине. Для формата `.mcp.json` используйте те же поля, показанные в разделе [Добавление сервера из файла конфигурации](#from-a-config-file). В коде передайте команду и её аргументы. Замените `/Users/me/projects` на директорию на вашей машине:

```typescript TypeScript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      filesystem: {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
      }
    },
    allowedTools: ["mcp__filesystem__read_file", "mcp__filesystem__list_directory"]
  }
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/Users/me/projects",
            ],
        }
    },
    allowed_tools=["mcp__filesystem__read_file", "mcp__filesystem__list_directory"],
)
```

### HTTP/SSE серверы

Используйте HTTP или SSE для облачных MCP серверов и удалённых API. Для формата `.mcp.json` используйте те же поля, что и в примере в [HTTP headers for remote servers](#http-headers-for-remote-servers), с `"type": "sse"` для SSE сервера. В коде передайте URL сервера:

```typescript TypeScript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      "remote-api": {
        type: "sse",
        url: "https://api.example.com/mcp/sse",
        headers: {
          Authorization: `Bearer ${process.env.API_TOKEN}`
        }
      }
    },
    allowedTools: ["mcp__remote-api__*"]
  }
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        "remote-api": {
            "type": "sse",
            "url": "https://api.example.com/mcp/sse",
            "headers": {"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
        }
    },
    allowed_tools=["mcp__remote-api__*"],
)
```

Для потокового HTTP транспорта используйте `"type": "http"` вместо этого. В `.mcp.json` и других JSON файлах конфигурации `"streamable-http"` принимается как псевдоним для `"http"`. Тип `McpHttpServerConfig` в SDK объявляет только `"http"`, поэтому используйте `"http"` для серверов, которые вы передаёте в коде.

### SDK MCP серверы

Определите пользовательские инструменты непосредственно в коде вашего приложения вместо запуска отдельного процесса сервера. Подробности реализации см. в [custom tools guide](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md).

SDK MCP сервер, зарегистрированный запросом управления [`initialize`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkcontrolinitializeresponse), начинает подключаться сразу же после обработки запроса Claude Code.

## Поиск инструментов MCP

Когда у вас настроено много инструментов MCP, определения инструментов могут занимать значительную часть вашего контекстного окна. Поиск инструментов решает эту проблему, скрывая определения инструментов из контекста и загружая только те, которые Claude нужны для каждого хода.

Поиск инструментов включен по умолчанию. Дополнительную информацию о параметрах конфигурации, лучших практиках и использовании поиска инструментов с пользовательскими инструментами SDK см. в разделе [Поиск инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md).

## Аутентификация

Большинство серверов MCP требуют аутентификации для доступа к внешним сервисам. Передавайте учетные данные через переменные окружения в конфигурации сервера.

### Передача учетных данных через переменные окружения

Используйте поле `env` для передачи ключей API, токенов и других учетных данных на сервер MCP:

> [tab] В коде
>
> ```typescript TypeScript hidelines={1,-1} theme={null}
> const _ = {
>   options: {
>     mcpServers: {
>       "api-server": {
>         command: "npx",
>         args: ["-y", "@your-org/api-mcp-server"],
>         env: {
>           API_KEY: process.env.API_KEY
>         }
>       }
>     },
>     allowedTools: ["mcp__api-server__*"]
>   }
> };
> ```
>
> ```python Python theme={null}
> options = ClaudeAgentOptions(
>     mcp_servers={
>         "api-server": {
>             "command": "npx",
>             "args": ["-y", "@your-org/api-mcp-server"],
>             "env": {"API_KEY": os.environ["API_KEY"]},
>         }
>     },
>     allowed_tools=["mcp__api-server__*"],
> )
> ```

> [tab] .mcp.json
>
> ```json theme={null}
> {
>   "mcpServers": {
>     "api-server": {
>       "command": "npx",
>       "args": ["-y", "@your-org/api-mcp-server"],
>       "env": {
>         "API_KEY": "${API_KEY}"
>       }
>     }
>   }
> }
> ```
>
> Синтаксис `${API_KEY}` раскрывает переменные окружения во время выполнения.

### HTTP-заголовки для удаленных серверов

Для HTTP и SSE серверов передавайте заголовки аутентификации непосредственно в конфигурации сервера:

> [tab] В коде
>
> ```typescript TypeScript hidelines={1,-1} theme={null}
> const _ = {
>   options: {
>     mcpServers: {
>       "secure-api": {
>         type: "http",
>         url: "https://api.example.com/mcp",
>         headers: {
>           Authorization: `Bearer ${process.env.API_TOKEN}`
>         }
>       }
>     },
>     allowedTools: ["mcp__secure-api__*"]
>   }
> };
> ```
>
> ```python Python theme={null}
> options = ClaudeAgentOptions(
>     mcp_servers={
>         "secure-api": {
>             "type": "http",
>             "url": "https://api.example.com/mcp",
>             "headers": {"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
>         }
>     },
>     allowed_tools=["mcp__secure-api__*"],
> )
> ```

> [tab] .mcp.json
>
> ```json theme={null}
> {
>   "mcpServers": {
>     "secure-api": {
>       "type": "http",
>       "url": "https://api.example.com/mcp",
>       "headers": {
>         "Authorization": "Bearer ${API_TOKEN}"
>       }
>     }
>   }
> }
> ```
>
> Синтаксис `${API_TOKEN}` раскрывает переменные окружения во время выполнения.

Полный рабочий пример удаленного сервера с аутентификацией через заголовки см. в разделе [Список проблем из репозитория](#list-issues-from-a-repository).

### Аутентификация OAuth2

[Спецификация MCP поддерживает OAuth 2.1](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) для авторизации. SDK не открывает браузер и не запускает интерактивный поток OAuth. Когда настроенный сервер возвращает запрос авторизации, а у Claude Code нет токена для отправки, SDK сообщает для сервера статус `needs-auth` или `failed`:

* **`needs-auth`**: Claude Code не нашёл входа, который можно использовать для этого сервера. Передайте токен в `headers` или перед запуском [войдите из интерактивной сессии Claude Code](https://code.claude.com/docs/ru/mcp.md#authenticate-with-remote-mcp-servers) на том же компьютере.
* **`failed`** с полем `error` в записи [`McpServerStatus`](https://code.claude.com/docs/ru/agent-sdk/typescript#mcpserverstatus), которое начинается с `Couldn't read the stored credentials` или `A request to MCP server`: Claude Code не смог прочитать своё хранилище учётных данных. О том, что делать, см. [Couldn't read the stored credentials for MCP server](https://code.claude.com/docs/ru/errors.md#couldnt-read-the-stored-credentials-for-mcp-server). До Claude Code v2.1.307 в случае заблокированной связки ключей входа на Mac вместо этого сообщался статус `needs-auth`.

В любом случае запуск агента продолжается без инструментов этого сервера. Массив `mcp_servers` [системного инициализирующего сообщения](https://code.claude.com/docs/ru/agent-sdk/typescript.md#sdksystemmessage) может по-прежнему показывать `pending` для этого сервера при его отправке. Чтобы подтвердить, требуются ли серверу учётные данные, опросите `mcpServerStatus()` в TypeScript SDK или [`get_mcp_status()`](https://code.claude.com/docs/ru/agent-sdk/python#methods) в Python.

Для предоставления учетных данных завершите поток OAuth в своем приложении и передайте полученный токен доступа в `headers` сервера:

```typescript TypeScript theme={null}
// После завершения потока OAuth в вашем приложении.
// Реализуйте getAccessTokenFromOAuthFlow для вашего поставщика OAuth.
const accessToken = await getAccessTokenFromOAuthFlow();

const options = {
  mcpServers: {
    "oauth-api": {
      type: "http",
      url: "https://api.example.com/mcp",
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }
  },
  allowedTools: ["mcp__oauth-api__*"]
};
```

```python Python theme={null}
# После завершения потока OAuth в вашем приложении.
# Реализуйте get_access_token_from_oauth_flow для вашего поставщика OAuth.
access_token = await get_access_token_from_oauth_flow()

options = ClaudeAgentOptions(
    mcp_servers={
        "oauth-api": {
            "type": "http",
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": f"Bearer {access_token}"},
        }
    },
    allowed_tools=["mcp__oauth-api__*"],
)
```

## Примеры

### Список проблем из репозитория

Этот пример подключается к удалённому [серверу GitHub MCP](https://github.com/github/github-mcp-server) для получения списка последних проблем. Пример включает отладочное логирование для проверки подключения MCP и вызовов инструментов.

Перед запуском создайте [личный токен доступа GitHub](https://github.com/settings/personal-access-tokens) с правами на чтение репозиториев, которые вы хотите запросить, и установите его как переменную окружения:

```bash theme={null}
export GITHUB_TOKEN=YOUR_GITHUB_PAT
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "List the 3 most recent issues in anthropics/claude-code",
  options: {
    mcpServers: {
      github: {
        type: "http",
        url: "https://api.githubcopilot.com/mcp/",
        headers: {
          Authorization: `Bearer ${process.env.GITHUB_TOKEN}`
        }
      }
    },
    allowedTools: ["mcp__github__list_issues"]
  }
})) {
  // Verify MCP server connected successfully
  if (message.type === "system" && message.subtype === "init") {
    console.log("MCP servers:", message.mcp_servers);
  }

  // Log when Claude calls an MCP tool
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "tool_use" && block.name.startsWith("mcp__")) {
        console.log("MCP tool called:", block.name);
      }
    }
  }

  // Print the final result
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
import asyncio
import os
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    AssistantMessage,
)


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "github": {
                "type": "http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers": {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
            }
        },
        allowed_tools=["mcp__github__list_issues"],
    )

    async for message in query(
        prompt="List the 3 most recent issues in anthropics/claude-code",
        options=options,
    ):
        # Verify MCP server connected successfully
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print("MCP servers:", message.data.get("mcp_servers"))

        # Log when Claude calls an MCP tool
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "name") and block.name.startswith("mcp__"):
                    print("MCP tool called:", block.name)

        # Print the final result
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

В строке `MCP servers:` статус `connected` для `github` подтверждает, что токен работает. Если Claude Code имеет [кэшированный список инструментов](#connection-timing) для сервера, статус может отображаться как `pending`, и сервер подключится при первом вызове инструмента. Если статус `failed` или `needs-auth`, см. [Обработка ошибок](#error-handling) перед тем, как доверять результату, так как Claude может вернуться к встроенным инструментам, когда сервер недоступен.

### Запрос к базе данных

Этот пример использует [DBHub](https://github.com/bytebase/dbhub) для запроса к базе данных Postgres. Агент автоматически обнаруживает схему базы данных, пишет SQL-запрос и возвращает результаты.

Инструмент `execute_sql` DBHub выполняет любой SQL, который выдаёт агент, включая операции записи, если вы это не ограничите. Установка `readonly = true` в [файле конфигурации DBHub](https://dbhub.ai/config/toml) заставляет DBHub отклонять операторы `INSERT`, `UPDATE`, `DELETE` и DDL, поэтому пример не может изменять ваши данные, даже если агент выдаст операцию записи. DBHub разрешает `${DATABASE_URL}` из переменных окружения процесса при загрузке конфига, поэтому строка подключения остаётся вне файла. Создайте этот файл `dbhub.toml` рядом с вашим скриптом:

```toml dbhub.toml theme={null}
[[sources]]
id = "production"
dsn = "${DATABASE_URL}"

[[tools]]
name = "execute_sql"
source = "production"
readonly = true
```

Затем скрипт указывает DBHub на файл конфигурации вместо прямой передачи строки подключения. Перед запуском установите переменную окружения `DATABASE_URL` на вашу строку подключения. Замените значения-заполнители на детали вашей базы данных:

```bash theme={null}
export DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  // Natural language query - Claude writes the SQL
  prompt: "How many users signed up last week? Break it down by day.",
  options: {
    mcpServers: {
      postgres: {
        command: "npx",
        // dbhub.toml sets readonly = true, so execute_sql rejects writes
        args: ["-y", "@bytebase/dbhub", "--config", "dbhub.toml"]
      }
    },
    allowedTools: ["mcp__postgres__execute_sql"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "postgres": {
                "command": "npx",
                # dbhub.toml sets readonly = true, so execute_sql rejects writes
                "args": [
                    "-y",
                    "@bytebase/dbhub",
                    "--config",
                    "dbhub.toml",
                ],
            }
        },
        allowed_tools=["mcp__postgres__execute_sql"],
    )

    # Natural language query - Claude writes the SQL
    async for message in query(
        prompt="How many users signed up last week? Break it down by day.",
        options=options,
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

## Обработка ошибок

MCP серверы могут не подключиться по различным причинам: процесс сервера может быть не установлен, учетные данные могут быть неверными или удаленный сервер может быть недоступен.

Claude Code отправляет сообщение `system` с подтипом `init` в начале каждого запроса. Это сообщение включает статус подключения для каждого MCP сервера. Поле `status` может быть `"pending"`, `"connected"`, `"failed"`, `"needs-auth"` или `"disabled"`. Claude Code отправляет сообщение init после [первого ожидания подключения](#connection-timing) для серверов, переданных в `options.mcpServers`, поэтому такой сервер, который подключился в течение ожидания, показывает `"connected"`.

В сообщении init не рассматривайте `"pending"` как ошибку само по себе. Это может означать любое из следующего:

* Сервер еще не подключился. См. [как долго Claude Code ждет его перед первым ходом](#connection-timing)
* Список инструментов сервера был [получен из кэша](#connection-timing), с подключением при первом использовании
* Срок подключения истек. Такой сервер сообщает `"pending"` или `"failed"` в зависимости от времени

Проверьте `"failed"` или `"needs-auth"` для обнаружения серверов, которые не будут пригодны для использования:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

try {
  for await (const message of query({
    prompt: "Process data",
    options: {
      mcpServers: {
        // Replace dataServer with your server configuration
        "data-processor": dataServer
      }
    }
  })) {
    if (message.type === "system" && message.subtype === "init") {
      const unavailableServers = message.mcp_servers.filter(
        (s) => s.status === "failed" || s.status === "needs-auth"
      );

      if (unavailableServers.length > 0) {
        console.warn("Unavailable MCP servers:", unavailableServers);
      }
    }

    if (message.type === "result" && message.subtype === "error_during_execution") {
      console.error("Execution failed");
    }
  }
} catch (error) {
  // A single-shot query() throws after yielding an error result. If the
  // failure was an error result, the error subtype branch above has
  // already run; a failure to start or reach the Claude Code process
  // yields no result message. MCP servers that fail to connect don't
  // throw: use the status check above, and note that servers still
  // "pending" at init need a later status check.
  console.log(`Session ended with an error: ${error}`);
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, ResultMessage


async def main():
    # Replace data_server with your server configuration
    options = ClaudeAgentOptions(mcp_servers={"data-processor": data_server})

    try:
        async for message in query(prompt="Process data", options=options):
            if isinstance(message, SystemMessage) and message.subtype == "init":
                unavailable_servers = [
                    s
                    for s in message.data.get("mcp_servers", [])
                    if s.get("status") in ("failed", "needs-auth")
                ]

                if unavailable_servers:
                    print(f"Unavailable MCP servers: {unavailable_servers}")

            if (
                isinstance(message, ResultMessage)
                and message.subtype == "error_during_execution"
            ):
                print("Execution failed")
    except Exception as error:
        # A single-shot query() raises after yielding an error result. If the
        # failure was an error result, the error subtype branch above has
        # already run; a failure to start or reach the Claude Code process
        # yields no result message. MCP servers that fail to connect don't
        # raise: use the status check above, and note that servers still
        # "pending" at init need a later status check.
        print(f"Session ended with an error: {error}")


asyncio.run(main())
```

Статус удаленного сервера также может измениться после того, как он сообщит `"connected"`. Когда соединение с ним разрывается во время сеанса, Claude Code переводит сервер обратно в `"pending"` во время [переподключения](https://code.claude.com/docs/ru/mcp.md#automatic-reconnection). Последующий вызов `mcpServerStatus()` в TypeScript или [`ClaudeSDKClient.get_mcp_status()`](https://code.claude.com/docs/ru/agent-sdk/python#methods) в Python может затем сообщить `"pending"` для сервера, который вы видели подключенным ранее, без каких-либо изменений конфигурации с вашей стороны.

После пяти неудачных попыток переподключения сервер сообщает `"failed"` или `"needs-auth"`, когда ему требуется повторная авторизация. HTTP- или SSE-сервер в состоянии `"failed"` может вернуться в `"connected"` без какого-либо вызова с вашей стороны, поскольку после временной ошибки Claude Code продолжает [повторять попытки в фоновом режиме](https://code.claude.com/docs/ru/mcp.md#mid-session-drops-of-a-remote-server). Для повторной попытки вручную вызовите [`reconnectMcpServer()`](https://code.claude.com/docs/ru/agent-sdk/typescript#methods) в TypeScript или [`ClaudeSDKClient.reconnect_mcp_server()`](https://code.claude.com/docs/ru/agent-sdk/python#methods) в Python.

## Troubleshooting

### Server shows "failed" status

Check the `init` message to see which servers failed to connect:

```typescript TypeScript theme={null}
if (message.type === "system" && message.subtype === "init") {
  for (const server of message.mcp_servers) {
    if (server.status === "failed") {
      console.error(`Server ${server.name} failed to connect`);
    }
  }
}
```

```python Python theme={null}
if isinstance(message, SystemMessage) and message.subtype == "init":
    for server in message.data.get("mcp_servers", []):
        if server.get("status") == "failed":
            print(f"Server {server['name']} failed to connect")
```

A `"pending"` status doesn't mean the server failed. See [Обработка ошибок](#error-handling) for the cases it covers at init. To get updated statuses later in the session, call the query's `mcpServerStatus()` method in the TypeScript SDK, or [`ClaudeSDKClient.get_mcp_status()`](https://code.claude.com/docs/ru/agent-sdk/python#methods) in Python.

Common causes:

* **Missing environment variables**: Ensure required tokens and credentials are set. For stdio servers, check the `env` field matches what the server expects.
* **Server not installed**: For `npx` commands, verify the package exists and Node.js is in your PATH.
* **Invalid connection string**: For database servers, verify the connection string format and that the database is accessible.
* **Network issues**: For remote HTTP/SSE servers, check the URL is reachable and any firewalls allow the connection.

### Tools not being called

If Claude sees tools but doesn't use them, check that you've granted permission with `allowedTools`:

```typescript TypeScript hidelines={1,-1} theme={null}
const _ = {
  options: {
    mcpServers: {
      // your servers
    },
    allowedTools: ["mcp__servername__*"] // Auto-approve calls from this server
  }
};
```

```python Python theme={null}
options = ClaudeAgentOptions(
    mcp_servers={
        # your servers
    },
    allowed_tools=["mcp__servername__*"],  # Auto-approve calls from this server
)
```

### Инструмент отсутствует в SDK MCP-сервере

В TypeScript SDK, если входную схему инструмента невозможно преобразовать в JSON Schema, сервер, созданный с помощью [`createSdkMcpServer()`](https://code.claude.com/docs/ru/agent-sdk/typescript#createsdkmcpserver), не включает этот инструмент в список своих инструментов. В этот момент SDK выдаёт предупреждение. В Node.js это предупреждение процесса с кодом `CLAUDE_SDK_MCP_TOOL_SCHEMA_UNCONVERTIBLE`, и оно начинается с такого текста:

```text theme={null}
Tool "<name>" on SDK MCP server "<server>" was left out of the server's tool list, because its input schema cannot be converted to JSON Schema
```

Далее в предупреждении приводится сообщение об ошибке преобразования, если оно есть, а затем указывается, что следует проверить и изменить.

До версии TypeScript Agent SDK v0.3.286 одна непреобразуемая схема приводила к сбою всего списка инструментов сервера без этого предупреждения, поэтому ни один из инструментов этого сервера не попадал к Claude.

### Connection timeouts

MCP server connections time out after 30 seconds by default. To change how long a running tool call may take, set [`MCP_TOOL_TIMEOUT`](https://code.claude.com/docs/ru/env-vars). If your server takes longer to start, the connection fails. Raise the connection limit with the [`MCP_TIMEOUT`](https://code.claude.com/docs/ru/env-vars) environment variable, in milliseconds. For servers that need more startup time, also consider:

* Using a lighter-weight server if available
* Pre-warming the server before starting your agent
* Checking server logs for slow initialization causes

In TypeScript, you can set the tool-call limit for a single [SDK MCP server](#sdk-mcp-servers) by passing [`timeout` to `createSdkMcpServer()`](https://code.claude.com/docs/ru/agent-sdk/typescript#createsdkmcpserver).

### Tool output exceeds maximum allowed tokens

SDK применяет те же ограничения на вывод MCP, что и Claude Code. Когда успешный результат инструмента без изображений превышает 25 000 токенов, Claude Code сохраняет вывод в файл и заменяет результат инструмента сообщением об ошибке с путём к этому файлу, чтобы агент мог прочитать вывод по частям.

Чтобы изменить лимит токенов, задайте переменную окружения [`MAX_MCP_OUTPUT_TOKENS`](https://code.claude.com/docs/ru/env-vars). Если инструмент не объявляет `anthropic/maxResultSizeChars`, успешный текстовый результат длиннее 50 000 символов сохраняется в файл независимо от лимита токенов. Полное описание поведения, включая то, как сервер объявляет эту аннотацию, см. в разделе [Ограничения и предупреждения вывода MCP](https://code.claude.com/docs/ru/mcp.md#mcp-output-limits-and-warnings).

## Связанные ресурсы

* **[Руководство по пользовательским инструментам](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md)**: Создайте собственный MCP сервер, который работает в процессе вашего приложения SDK
* **[Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md)**: Контролируйте, какие MCP инструменты может использовать ваш агент, с помощью `allowedTools` и `disallowedTools`
* **[Справочник TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md)**: Полный справочник API, включая параметры конфигурации MCP
* **[Справочник Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md)**: Полный справочник API, включая параметры конфигурации MCP
* **[Каталог MCP серверов](https://github.com/modelcontextprotocol/servers)**: Просмотрите доступные MCP серверы для баз данных, API и многого другого
