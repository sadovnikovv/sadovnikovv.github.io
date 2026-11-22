> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Предоставьте Claude пользовательские инструменты

> Определите пользовательские инструменты с помощью встроенного MCP-сервера Agent SDK, чтобы Claude мог вызывать ваши функции, обращаться к вашим API и выполнять операции, специфичные для вашей области.

Пользовательские инструменты расширяют Agent SDK, позволяя вам определять собственные функции, которые Claude может вызывать во время разговора. Используя встроенный MCP-сервер SDK, вы можете предоставить Claude доступ к базам данных, внешним API, логике, специфичной для вашей области, или любым другим возможностям, которые требует ваше приложение.

## Краткая справка

| Если вы хотите... | Сделайте это |
| :- | :- |
| Определить инструмент | Используйте [`@tool`](https://code.claude.com/docs/ru/agent-sdk/python#tool) (Python) или [`tool()`](https://code.claude.com/docs/ru/agent-sdk/typescript#tool) (TypeScript) с именем, описанием, схемой и обработчиком. См. [Создание пользовательского инструмента](#create-a-custom-tool). |
| Сделать параметр необязательным | Объявите его необязательным в схеме и примените значение по умолчанию в обработчике. См. [Как сделать параметр необязательным](#make-a-parameter-optional). |
| Зарегистрировать инструмент с Claude | Оберните в `create_sdk_mcp_server` / `createSdkMcpServer` и передайте в `mcpServers` в `query()`. См. [Вызов пользовательского инструмента](#call-a-custom-tool). |
| Предварительно одобрить инструмент | Добавьте в разрешённые инструменты. См. [Настройка разрешённых инструментов](#configure-allowed-tools). |
| Требовать подтверждения для вызовов инструмента или заблокировать инструмент | В TypeScript SDK добавьте `permission_policy` для инструмента в объект конфигурации, который возвращает `createSdkMcpServer()`. См. [Требование подтверждения для определённых инструментов](#require-approval-for-specific-tools). |
| Удалить встроенный инструмент из контекста Claude | Передайте массив `tools`, содержащий только встроенные инструменты, которые вы хотите. См. [Настройка разрешённых инструментов](#configure-allowed-tools). |
| Позволить Claude вызывать инструменты параллельно | Установите `readOnlyHint: true` на инструментах без побочных эффектов. См. [Добавление аннотаций инструментов](#add-tool-annotations). |
| Контролировать сообщение об ошибке, которое читает Claude | Верните `isError: true` для составления сообщения вместо выброса необработанного исключения. См. [Обработка ошибок](#handle-errors). |
| Вернуть изображения или файлы | Используйте блоки `image` или `resource` в массиве содержимого. См. [Возврат изображений и ресурсов](#return-images-and-resources). |
| Вернуть результат в формате машиночитаемого JSON | Установите `structuredContent` на результат. См. [Возврат структурированных данных](#return-structured-data). |
| Масштабировать до множества инструментов | Используйте [поиск инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md) для загрузки инструментов по требованию. |

## Создание пользовательского инструмента

Инструмент определяется четырьмя частями, передаваемыми в качестве аргументов вспомогательной функции [`tool()`](https://code.claude.com/docs/ru/agent-sdk/typescript#tool) в TypeScript или декоратору [`@tool`](https://code.claude.com/docs/ru/agent-sdk/python#tool) в Python:

* **Name:** уникальный идентификатор, который Claude использует для вызова инструмента.
* **Description:** описание того, что делает инструмент. Claude читает это, чтобы решить, когда его вызывать.
* **Input schema:** аргументы, которые принимает инструмент; объявляются по-разному в зависимости от языка:
  * **TypeScript**: [Zod schema](https://zod.dev/). `args` обработчика получают свои типы из неё. Вызовите `.describe()` для поля, чтобы задать ему описание, которое видит Claude.
  * **Python**: словарь, отображающий имена на типы, например `{"latitude": float}`, который SDK преобразует в JSON Schema для вас. Оберните тип в `Annotated`, например `{"latitude": Annotated[float, "Latitude coordinate"]}`, чтобы задать полю описание, которое видит Claude. Декоратор также принимает полный словарь [JSON Schema](https://json-schema.org/understanding-json-schema/about) непосредственно, когда вам нужны перечисления, диапазоны, необязательные поля или вложенные объекты.
* **Handler:** асинхронная функция, которая запускается, когда Claude вызывает инструмент. Она получает проверенные аргументы и должна возвращать объект с:
  * `content` (обязательно): массив блоков результатов, каждый с `type` равным `"text"`, `"image"`, `"audio"`, `"resource"` или `"resource_link"`. Смотрите [Return images and resources](#return-images-and-resources) для блоков, отличных от текста.
  * `structuredContent` (необязательно): объект JSON, содержащий результат как машиночитаемые данные, возвращаемые вместе с `content`. Смотрите [Return structured data](#return-structured-data).
  * `isError` (необязательно): установите значение `true`, чтобы сигнализировать об ошибке инструмента, чтобы Claude мог на неё реагировать. Смотрите [Handle errors](#handle-errors).

После определения инструмента оберните его в сервер с помощью [`createSdkMcpServer`](https://code.claude.com/docs/ru/agent-sdk/typescript#createsdkmcpserver) (TypeScript) или [`create_sdk_mcp_server`](https://code.claude.com/docs/ru/agent-sdk/python#create_sdk_mcp_server) (Python). Сервер работает внутри процесса вашего приложения, а не как отдельный процесс.

Примеры на Python на этой странице, выполняющие HTTP-запросы, используют [httpx](https://www.python-httpx.org/). Добавьте его с помощью менеджера пакетов, который использует ваш проект:

> [tab] Python (uv)
>
> ```bash theme={null}
> uv add httpx
> ```

> [tab] Python (pip)
>
> ```bash theme={null}
> pip install httpx
> ```

### Пример инструмента Weather

Этот пример определяет инструмент `get_temperature` и оборачивает его в MCP-сервер, не передавая сервер в `query`. Чтобы запустить инструмент, смотрите [Call a custom tool](#call-a-custom-tool).

```python Python theme={null}
from typing import Annotated, Any
import httpx
from claude_agent_sdk import tool, create_sdk_mcp_server


# Define a tool: name, description, input schema, handler
@tool(
    "get_temperature",
    "Get the current temperature at a location",
    {
        "latitude": Annotated[float, "Latitude coordinate"],
        "longitude": Annotated[float, "Longitude coordinate"],
    },
)
async def get_temperature(args: dict[str, Any]) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": args["latitude"],
                "longitude": args["longitude"],
                "current": "temperature_2m",
                "temperature_unit": "fahrenheit",
            },
        )
        data = response.json()

    # Return a content array - Claude sees this as the tool result
    return {
        "content": [
            {
                "type": "text",
                "text": f"Temperature: {data['current']['temperature_2m']}°F",
            }
        ]
    }


# Wrap the tool in an in-process MCP server
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature],
)
```

```typescript TypeScript theme={null}
import { tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

// Define a tool: name, description, input schema, handler
const getTemperature = tool(
  "get_temperature",
  "Get the current temperature at a location",
  {
    latitude: z.number().describe("Latitude coordinate"), // .describe() adds a field description Claude sees
    longitude: z.number().describe("Longitude coordinate")
  },
  async (args) => {
    // args is typed from the schema: { latitude: number; longitude: number }
    const response = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${args.latitude}&longitude=${args.longitude}&current=temperature_2m&temperature_unit=fahrenheit`
    );
    const data: any = await response.json();

    // Return a content array - Claude sees this as the tool result
    return {
      content: [{ type: "text", text: `Temperature: ${data.current.temperature_2m}°F` }]
    };
  }
);

// Wrap the tool in an in-process MCP server
const weatherServer = createSdkMcpServer({
  name: "weather",
  version: "1.0.0",
  tools: [getTemperature]
});
```

Смотрите справку [`tool()`](https://code.claude.com/docs/ru/agent-sdk/typescript#tool) TypeScript или справку [`@tool`](https://code.claude.com/docs/ru/agent-sdk/python#tool) Python для полных деталей параметров, включая форматы входных JSON Schema и структуру возвращаемого значения.

### Как сделать параметр необязательным

Чтобы сделать параметр необязательным, объявите его необязательным в схеме и примените значение по умолчанию в обработчике:

* **TypeScript**: добавьте `.optional()` к полю Zod.
* **Python**: словарная схема требует наличия каждого ключа. Используйте форму JSON Schema, не включайте параметр в `required` и читайте его с помощью `args.get()`. Для типизированной схемы с необязательными ключами смотрите [TypedDict class](https://code.claude.com/docs/ru/agent-sdk/python.md#input-schema-options).

[Инструмент `get_precipitation_chance`](#add-more-tools) показывает оба паттерна.

### Вызов пользовательского инструмента

Чтобы вызвать пользовательский инструмент, выполните следующие шаги:

1. Передайте созданный вами MCP-сервер в `query` через опцию `mcpServers`.
2. Перечислите [полностью квалифицированное имя](https://code.claude.com/docs/ru/agent-sdk/mcp.md#tool-naming-convention) инструмента в `allowedTools`, чтобы [заранее одобрить](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules) его вызовы. Это имя имеет вид `mcp__{server_name}__{tool_name}`, где `{server_name}` — это ключ, который вы задаёте серверу в `mcpServers`. Если ключ содержит такие символы, как `.` или пробелы, замените их на `_`, когда записываете `{server_name}`.

Эти фрагменты повторно используют `weatherServer` из [примера инструмента Weather](#weather-tool-example), чтобы спросить Claude о погоде в определённом месте.

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"weather": weather_server},
        allowed_tools=["mcp__weather__get_temperature"],
    )

    async for message in query(
        prompt="What's the temperature in San Francisco?",
        options=options,
    ):
        # ResultMessage is the final message after all tool calls complete
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "What's the temperature in San Francisco?",
  options: {
    mcpServers: { weather: weatherServer },
    allowedTools: ["mcp__weather__get_temperature"]
  }
})) {
  // "result" is the final message after all tool calls complete
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

Объедините этот фрагмент с определениями инструмента и сервера из [примера инструмента Weather](#weather-tool-example) в одном файле, `weather.py` или `weather.ts`, затем запустите его из терминала:

> [tab] TypeScript
>
> ```bash theme={null}
> npx tsx weather.ts
> ```

> [tab] Python (uv)
>
> ```bash theme={null}
> uv run weather.py
> ```

> [tab] Python (pip)
>
> Активируйте виртуальное окружение, в котором вы установили SDK, затем выполните:
>
> ```bash theme={null}
> python weather.py
> ```

Claude вызывает `get_temperature`, и скрипт выводит однострочный ответ с текущей температурой в Сан-Франциско.

### Добавление дополнительных инструментов

Сервер содержит столько инструментов, сколько вы перечислите в его массиве `tools`. Если на сервере более одного инструмента, вы можете перечислить каждый в `allowedTools` отдельно или использовать подстановочный знак `mcp__weather__*`, чтобы охватить каждый инструмент, который сервер предоставляет.

Пример ниже определяет второй инструмент, `get_precipitation_chance`, и заменяет определение `weatherServer` из [примера инструмента Weather](#weather-tool-example) на то, которое перечисляет оба инструмента в массиве.

```python Python theme={null}
# Define a second tool for the same server
@tool(
    "get_precipitation_chance",
    "Get the hourly precipitation probability for a location",
    {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"},
            "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 24,
                "description": "How many hours of forecast to return",
            },
        },
        # 'hours' is left out of required, so Claude can omit it
        "required": ["latitude", "longitude"],
    },
)
async def get_precipitation_chance(args: dict[str, Any]) -> dict[str, Any]:
    # 'hours' isn't in required - read it with .get() to fall back to a default
    hours = args.get("hours", 12)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": args["latitude"],
                "longitude": args["longitude"],
                "hourly": "precipitation_probability",
                "forecast_days": 1,
            },
        )
        data = response.json()
    chances = data["hourly"]["precipitation_probability"][:hours]

    return {
        "content": [
            {
                "type": "text",
                "text": f"Next {hours} hours: {'%, '.join(map(str, chances))}%",
            }
        ]
    }


# Rebuild the server with both tools in the array
weather_server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_temperature, get_precipitation_chance],
)
```

```typescript TypeScript theme={null}
// Define a second tool for the same server
const getPrecipitationChance = tool(
  "get_precipitation_chance",
  "Get the hourly precipitation probability for a location",
  {
    latitude: z.number(),
    longitude: z.number(),
    hours: z
      .number()
      .int()
      .min(1)
      .max(24)
      .optional() // .optional() lets Claude omit the parameter
      .describe("How many hours of forecast to return")
  },
  async (args) => {
    const hours = args.hours ?? 12; // Apply the default in the handler
    const response = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${args.latitude}&longitude=${args.longitude}&hourly=precipitation_probability&forecast_days=1`
    );
    const data: any = await response.json();
    const chances = data.hourly.precipitation_probability.slice(0, hours);

    return {
      content: [{ type: "text", text: `Next ${hours} hours: ${chances.join("%, ")}%` }]
    };
  }
);

// Rebuild the server with both tools in the array
const weatherServer = createSdkMcpServer({
  name: "weather",
  version: "1.0.0",
  tools: [getTemperature, getPrecipitationChance]
});
```

[Tool search](https://code.claude.com/docs/ru/agent-sdk/tool-search.md) включен по умолчанию и откладывает SDK MCP инструменты: Claude видит имя каждого инструмента в компактном списке и загружает его полную схему по требованию. С отключённым поиском инструментов каждый инструмент в этом массиве потребляет пространство контекстного окна на каждом ходу. В TypeScript передайте `alwaysLoad: true` в аргументе `extras` функции [`tool()`](https://code.claude.com/docs/ru/agent-sdk/typescript#tool) или в опциях [`createSdkMcpServer()`](https://code.claude.com/docs/ru/agent-sdk/typescript#createsdkmcpserver), чтобы сохранить полную схему инструмента в начальном приглашении.

### Добавление аннотаций инструмента

[Tool annotations](https://modelcontextprotocol.io/docs/concepts/tools#tool-annotations) — это необязательные метаданные, описывающие поведение инструмента. Передайте их в качестве пятого аргумента вспомогательной функции `tool()` в TypeScript или через аргумент ключевого слова `annotations` для декоратора `@tool` в Python. Все поля подсказок являются логическими значениями.

| Field | Default | Meaning |
| :- | :- | :- |
| `readOnlyHint` | `false` | Инструмент не изменяет свою среду. Контролирует, может ли инструмент вызываться параллельно с другими инструментами только для чтения. |
| `destructiveHint` | `true` | Инструмент может выполнять деструктивные обновления. Явно установите значение `true` для любого инструмента, который вы [помечаете как `always_ask`](#require-approval-for-specific-tools). |
| `idempotentHint` | `false` | Повторные вызовы с одинаковыми аргументами не имеют дополнительного эффекта. |
| `openWorldHint` | `true` | Инструмент достигает систем вне вашего процесса. |

Аннотации — это метаданные, а не принуждение. Инструмент, отмеченный как `readOnlyHint: true`, всё ещё может писать на диск, если это то, что делает обработчик. Держите аннотацию точной для обработчика.

Этот пример добавляет `readOnlyHint` к инструменту `get_temperature` из [примера инструмента Weather](#weather-tool-example).

```python Python theme={null}
from claude_agent_sdk import tool, ToolAnnotations


@tool(
    "get_temperature",
    "Get the current temperature at a location",
    {"latitude": float, "longitude": float},
    annotations=ToolAnnotations(
        readOnlyHint=True
    ),  # Lets Claude batch this with other read-only calls
)
async def get_temperature(args):
    return {"content": [{"type": "text", "text": "..."}]}
```

```typescript TypeScript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

tool(
  "get_temperature",
  "Get the current temperature at a location",
  { latitude: z.number(), longitude: z.number() },
  async (args) => ({ content: [{ type: "text", text: `...` }] }),
  { annotations: { readOnlyHint: true } } // Lets Claude batch this with other read-only calls
);
```

Смотрите `ToolAnnotations` в справке [TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#toolannotations) или [Python](https://code.claude.com/docs/ru/agent-sdk/python.md#toolannotations).

## Управление доступом к инструментам

[Пример инструмента weather](#weather-tool-example) зарегистрировал сервер и перечислил инструменты в `allowedTools`. В этом разделе рассматривается, как ограничить доступ, когда у вас есть несколько инструментов или вы хотите ограничить встроенные инструменты. Информацию о том, как конструируются имена инструментов, см. в разделе [Вызов пользовательского инструмента](#call-a-custom-tool).

### Настройка разрешённых инструментов

С помощью опций `tools`, `allowedTools` и `disallowedTools` вы управляете двумя уровнями:

* **Доступность**: появляется ли инструмент в контексте Claude. Чтобы изменить её, используйте опцию `tools` или укажите простое имя встроенного инструмента, например `"Bash"`, в `disallowedTools`.
* **Разрешение**: одобряет ли Claude Code вызов, когда Claude его выполняет. Чтобы изменить его, используйте `allowedTools` или правило `disallowedTools` с областью действия, например `"Bash(rm *)"`.

| Опция | Уровень | Эффект |
| :- | :- | :- |
| `tools: ["Read", "Grep"]` | Доступность | Только перечисленные встроенные инструменты находятся в контексте Claude. Неперечисленные встроенные инструменты удаляются. Инструменты MCP не затрагиваются. |
| `tools: []` | Доступность | Все встроенные инструменты удаляются. Claude может использовать только ваши инструменты MCP. |
| разрешённые инструменты | Разрешение | Перечисленные инструменты одобрены заранее, за исключением [вызовов, которые не одобряет ни одно правило разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#calls-an-allow-rule-never-approves). Вызовы инструментов, не включённых в список, проходят через [поток разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md). |
| запрещённые инструменты | Оба | Простое имя встроенного инструмента, такое как `"Bash"`, удаляет инструмент из контекста Claude. Правило с областью действия, такое как `"Bash(rm *)"`, оставляет инструмент в контексте и отклоняет вызовы, которые совпадают с ним [как написано](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits). |

Чтобы удалить встроенный инструмент из контекста Claude, опустите его из `tools` или перечислите его простое имя в `disallowedTools` (TypeScript) или `disallowed_tools` (Python). Полный порядок оценки см. в разделе [Настройка разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated).

### Требование подтверждения для определённых инструментов

Установите для `permission_policy` инструмента значение `always_ask`, и `allowedTools` перестанет одобрять вызовы этого инструмента, поэтому они смогут доходить до вашего обратного вызова [`canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input), даже если инструмент указан в списке. Вместо этого установите `always_deny`, чтобы [заблокировать инструмент](https://code.claude.com/docs/ru/agent-sdk/typescript.md#permission-policy-values). Это поле доступно только в TypeScript и требует Agent SDK v0.3.301 или более поздней версии.

Поместите запись политики в массив `tools` объекта конфигурации, который возвращает `createSdkMcpServer()`, а не в опцию `tools`, которую вы передаёте в эту функцию. Этот пример разворачивает `weatherServer` из [примера инструмента weather](#weather-tool-example) и добавляет массив `tools`, назначающий `get_temperature` политику `always_ask`:

```typescript TypeScript theme={null}
options: {
  mcpServers: {
    weather: {
      ...weatherServer,
      tools: [{ name: "get_temperature", permission_policy: "always_ask" as const }]
    }
  },
  allowedTools: ["mcp__weather__get_temperature"],
  permissionMode: "default",
  canUseTool: async (toolName, input) => {
    console.log(`Approval requested for ${toolName}`);
    return { behavior: "allow", updatedInput: input };
  }
}
```

Чтобы опробовать политику, замените `options` в скрипте из раздела [Вызов пользовательского инструмента](#call-a-custom-tool) на `options` из этого примера, а затем запустите скрипт из терминала. Скрипт выведет `Approval requested for mcp__weather__get_temperature`, а затем ответ Claude о температуре. Полный скрипт см. в [справочнике по TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#mcpsdkserverconfigwithinstance).

Если вы используете [режим разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#permission-modes) `auto` или `plan`, установите `destructiveHint: true` в [аннотациях](#add-tool-annotations) инструмента, чтобы вызовы инструмента по-прежнему доходили до вашего обратного вызова. В противном случае [классификатор авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) может одобрить некоторые вызовы `always_ask` при [условиях, перечисленных в справочнике по TypeScript](https://code.claude.com/docs/ru/agent-sdk/typescript.md#permission-modes-that-can-approve-an-always_ask-call), и одобренный им вызов не дойдёт до вашего обратного вызова. Устанавливайте эту подсказку явно, поскольку неустановленный `destructiveHint` для вызовов `always_ask` считается равным `false`, а не принимает значение `true` по умолчанию.

## Обработка ошибок

Ошибка обработчика не останавливает цикл агента. MCP-сервер SDK в процессе перехватывает необработанные исключения и возвращает их как результаты ошибок, поэтому то, как вы сообщаете об ошибке, определяет, что читает Claude, а не то, завершится ли запрос неудачей:

| Что происходит | Результат |
| :- | :- |
| Обработчик выбрасывает необработанное исключение | MCP-сервер преобразует его в результат ошибки, содержащий исходное сообщение об исключении. Claude видит это сообщение, и цикл агента продолжается. |
| Обработчик перехватывает ошибку и возвращает `isError: true` (TS) / `"is_error": True` (Python) | Claude видит сообщение, которое вы составили. Вы можете добавить контекст, которого не хватает исходному исключению, например какой запрос не удался или что попробовать вместо этого. |

В обоих случаях Claude может повторить попытку, попробовать другой инструмент или объяснить сбой. Перехватывайте ошибки самостоятельно, когда исходное сообщение об исключении недостаточно для того, чтобы Claude мог действовать.

Приведённый ниже пример перехватывает два вида сбоев внутри обработчика и составляет сообщение об ошибке, которое читает Claude. Статус HTTP, отличный от 200, перехватывается из ответа и возвращается как результат ошибки. Ошибка сети или неверный JSON перехватываются окружающим блоком `try/except` (Python) или `try/catch` (TypeScript) и также возвращаются как результат ошибки. В обоих случаях Claude получает сообщение, которое описывает сбой вместо простой строки исключения.

```python Python theme={null}
import json
import httpx
from typing import Any
from claude_agent_sdk import tool


@tool(
    "fetch_data",
    "Fetch data from an API",
    {"endpoint": str},  # Simple schema
)
async def fetch_data(args: dict[str, Any]) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(args["endpoint"])
            if response.status_code != 200:
                # Return the failure as a tool result so Claude can react to it.
                # is_error marks this as a failed call rather than odd-looking data.
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"API error: {response.status_code} {response.reason_phrase}",
                        }
                    ],
                    "is_error": True,
                }

            data = response.json()
            return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
    except Exception as e:
        # Composes the message Claude reads. An uncaught exception would
        # reach Claude as the raw str(e) with no context.
        return {
            "content": [{"type": "text", "text": f"Failed to fetch data: {str(e)}"}],
            "is_error": True,
        }
```

```typescript TypeScript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

tool(
  "fetch_data",
  "Fetch data from an API",
  {
    endpoint: z.string().url().describe("API endpoint URL")
  },
  async (args) => {
    try {
      const response = await fetch(args.endpoint);

      if (!response.ok) {
        // Return the failure as a tool result so Claude can react to it.
        // isError marks this as a failed call rather than odd-looking data.
        return {
          content: [
            {
              type: "text",
              text: `API error: ${response.status} ${response.statusText}`
            }
          ],
          isError: true
        };
      }

      const data = await response.json();
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2)
          }
        ]
      };
    } catch (error) {
      // Composes the message Claude reads. An uncaught throw would
      // reach Claude as the raw error message with no context.
      return {
        content: [
          {
            type: "text",
            text: `Failed to fetch data: ${error instanceof Error ? error.message : String(error)}`
          }
        ],
        isError: true
      };
    }
  }
);
```

## Возврат изображений и ресурсов

Массив `content` в результате инструмента принимает блоки `text`, `image`, `audio`, `resource` и `resource_link`. Вы можете смешивать их в одном ответе. В TypeScript SDK сохраняет аудиоблоки на диск, и Claude получает текстовый блок с сохранённым путём файла; в Python SDK удаляет аудиоблоки из результата инструмента и регистрирует предупреждение.

Claude получает каждый блок ссылки на ресурс как текстовый блок, содержащий имя ссылки, URI и описание. В TypeScript ваше приложение также получает сами ссылки как [`resourceLinks`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkmcpresourcelink) в `tool_use_result` сообщения пользователя; в Python SDK преобразует их в текст перед тем, как CLI увидит результат, поэтому ключ Python [`resourceLinks`](https://code.claude.com/docs/ru/agent-sdk/python#usermessage) никогда не создаётся для встроенных инструментов.

### Изображения

Блок изображения содержит байты изображения встроенными, закодированными в base64. Поля URL нет. Чтобы вернуть изображение, которое находится по URL, получите его в обработчике, прочитайте байты ответа и закодируйте их в base64 перед возвратом. Изображение PNG, JPEG, GIF или WebP поступает в Claude как визуальный ввод; изображение любого другого типа сохраняется на диск, и Claude получает его путь к файлу в виде текста.

| Поле | Тип | Примечания |
| :- | :- | :- |
| `type` | `"image"` | |
| `data` | `string` | Байты в кодировке Base64. Только raw base64, без префикса `data:image/...;base64,` |
| `mimeType` | `string` | Обязательно. Например `image/png`, `image/jpeg`, `image/webp`, `image/gif` |

```python Python theme={null}
import base64
import httpx
from claude_agent_sdk import tool


# Define a tool that fetches an image from a URL and returns it to Claude
@tool("fetch_image", "Fetch an image from a URL and return it to Claude", {"url": str})
async def fetch_image(args):
    async with httpx.AsyncClient() as client:  # Fetch the image bytes
        response = await client.get(args["url"])

    return {
        "content": [
            {
                "type": "image",
                "data": base64.b64encode(response.content).decode(
                    "ascii"
                ),  # Base64-encode the raw bytes
                "mimeType": response.headers.get(
                    "content-type", "image/png"
                ),  # Read MIME type from the response
            }
        ]
    }
```

```typescript TypeScript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

tool(
  "fetch_image",
  "Fetch an image from a URL and return it to Claude",
  {
    url: z.string().url()
  },
  async (args) => {
    const response = await fetch(args.url); // Fetch the image bytes
    const buffer = Buffer.from(await response.arrayBuffer()); // Read into a Buffer for base64 encoding
    const mimeType = response.headers.get("content-type") ?? "image/png";

    return {
      content: [
        {
          type: "image",
          data: buffer.toString("base64"), // Base64-encode the raw bytes
          mimeType
        }
      ]
    };
  }
);
```

### Ресурсы

Блок ресурса встраивает фрагмент содержимого, идентифицируемый URI. Фактическое содержимое находится в поле `text` или `blob` блока. Используйте это, когда ваш инструмент создаёт сгенерированный файл или запись из внешней системы.

| Поле | Тип | Примечания |
| :- | :- | :- |
| `type` | `"resource"` | |
| `resource.uri` | `string` | Идентификатор содержимого. Любая схема URI |
| `resource.text` | `string` | Содержимое, если это текст. Укажите это или `blob`, но не оба |
| `resource.blob` | `string` | Содержимое в кодировке base64, если это двоичные данные. Только TypeScript: Python SDK удаляет двоичные ресурсы из результата инструмента и регистрирует предупреждение |
| `resource.mimeType` | `string` | Необязательно |

Этот пример показывает блок ресурса, возвращаемый из обработчика инструмента. SDK не читает из URI примера `file:///tmp/report.md`.

```typescript TypeScript theme={null}
return {
  content: [
    {
      type: "resource",
      resource: {
        uri: "file:///tmp/report.md", // Label for Claude to reference, not a path the SDK reads
        mimeType: "text/markdown",
        text: "# Report\n..." // The actual content, inline
      }
    }
  ]
};
```

```python Python theme={null}
return {
    "content": [
        {
            "type": "resource",
            "resource": {
                "uri": "file:///tmp/report.md",  # Not a path the SDK reads
                "mimeType": "text/markdown",
                "text": "# Report\n...",  # The actual content, inline
            },
        }
    ]
}
```

Эти формы блоков происходят из типа MCP `CallToolResult`. Полное определение см. в [спецификации MCP](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool-result).

## Возврат структурированных данных

`structuredContent` — это необязательный объект JSON в результате, отдельный от массива `content`. Используйте его для возврата необработанных значений, которые Claude может читать как точные поля вместо их анализа из текстовой строки или изображения. Для обработчиков на Python см. раздел [Структурированное содержимое в Python](#structured-content-in-python).

Когда обработчик TypeScript `tool()` устанавливает `structuredContent`, Claude получает JSON плюс блоки изображений и ресурсов из `content`, а текстовые блоки в `content` до Claude не доходят. Пример ниже отображает диаграмму как блок изображения и возвращает точки данных за ней в `structuredContent` из того же обработчика. В фрагменте `chartPngBuffer` — это `Buffer`, содержащий отрендеренные байты PNG.

```typescript TypeScript theme={null}
return {
  content: [
    {
      type: "image",
      data: chartPngBuffer.toString("base64"),
      mimeType: "image/png"
    }
  ],
  structuredContent: {
    series: "temperature_2m",
    unit: "fahrenheit",
    points: [62.1, 63.4, 65.0, 64.2]
  }
};
```

> [!NOTE]
>
> Декоратор Python `@tool` передает только `content` и `is_error` из словаря возврата обработчика. Чтобы вернуть `structuredContent` из Python, запустите [автономный MCP сервер](https://code.claude.com/docs/ru/agent-sdk/mcp.md) вместо встроенного SDK сервера.

## Пример: конвертер единиц

Этот инструмент преобразует значения между единицами длины, температуры и веса. Пользователь может попросить "конвертировать 100 километров в мили" или "сколько это 72°F в Цельсиях", и Claude выбирает правильный тип единиц и единицы из запроса.

Это демонстрирует два паттерна:

* **Enum schemas:** `unit_type` ограничен фиксированным набором значений. В TypeScript используйте `z.enum()`. В Python словарь schema не поддерживает enums, поэтому требуется полный JSON Schema словарь.
* **Обработка неподдерживаемого ввода:** когда пара преобразования не найдена, обработчик возвращает `isError: true`, чтобы Claude мог сообщить пользователю, что пошло не так, вместо того чтобы рассматривать сбой как нормальный результат.

```python Python theme={null}
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server


# z.enum() в TypeScript становится ограничением "enum" в JSON Schema.
# Словарь schema не имеет эквивалента, поэтому требуется полный JSON Schema.
@tool(
    "convert_units",
    "Convert a value from one unit to another",
    {
        "type": "object",
        "properties": {
            "unit_type": {
                "type": "string",
                "enum": ["length", "temperature", "weight"],
                "description": "Category of unit",
            },
            "from_unit": {
                "type": "string",
                "description": "Unit to convert from, e.g. kilometers, fahrenheit, pounds",
            },
            "to_unit": {"type": "string", "description": "Unit to convert to"},
            "value": {"type": "number", "description": "Value to convert"},
        },
        "required": ["unit_type", "from_unit", "to_unit", "value"],
    },
)
async def convert_units(args: dict[str, Any]) -> dict[str, Any]:
    conversions = {
        "length": {
            "kilometers_to_miles": lambda v: v * 0.621371,
            "miles_to_kilometers": lambda v: v * 1.60934,
            "meters_to_feet": lambda v: v * 3.28084,
            "feet_to_meters": lambda v: v * 0.3048,
        },
        "temperature": {
            "celsius_to_fahrenheit": lambda v: (v * 9) / 5 + 32,
            "fahrenheit_to_celsius": lambda v: (v - 32) * 5 / 9,
            "celsius_to_kelvin": lambda v: v + 273.15,
            "kelvin_to_celsius": lambda v: v - 273.15,
        },
        "weight": {
            "kilograms_to_pounds": lambda v: v * 2.20462,
            "pounds_to_kilograms": lambda v: v * 0.453592,
            "grams_to_ounces": lambda v: v * 0.035274,
            "ounces_to_grams": lambda v: v * 28.3495,
        },
    }

    key = f"{args['from_unit']}_to_{args['to_unit']}"
    fn = conversions.get(args["unit_type"], {}).get(key)

    if not fn:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Unsupported conversion: {args['from_unit']} to {args['to_unit']}",
                }
            ],
            "is_error": True,
        }

    result = fn(args["value"])
    return {
        "content": [
            {
                "type": "text",
                "text": f"{args['value']} {args['from_unit']} = {result:.4f} {args['to_unit']}",
            }
        ]
    }


converter_server = create_sdk_mcp_server(
    name="converter",
    version="1.0.0",
    tools=[convert_units],
)
```

```typescript TypeScript theme={null}
import { tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const convert = tool(
  "convert_units",
  "Convert a value from one unit to another",
  {
    unit_type: z.enum(["length", "temperature", "weight"]).describe("Category of unit"),
    from_unit: z
      .string()
      .describe("Unit to convert from, e.g. kilometers, fahrenheit, pounds"),
    to_unit: z.string().describe("Unit to convert to"),
    value: z.number().describe("Value to convert")
  },
  async (args) => {
    type Conversions = Record<string, Record<string, (v: number) => number>>;

    const conversions: Conversions = {
      length: {
        kilometers_to_miles: (v) => v * 0.621371,
        miles_to_kilometers: (v) => v * 1.60934,
        meters_to_feet: (v) => v * 3.28084,
        feet_to_meters: (v) => v * 0.3048
      },
      temperature: {
        celsius_to_fahrenheit: (v) => (v * 9) / 5 + 32,
        fahrenheit_to_celsius: (v) => ((v - 32) * 5) / 9,
        celsius_to_kelvin: (v) => v + 273.15,
        kelvin_to_celsius: (v) => v - 273.15
      },
      weight: {
        kilograms_to_pounds: (v) => v * 2.20462,
        pounds_to_kilograms: (v) => v * 0.453592,
        grams_to_ounces: (v) => v * 0.035274,
        ounces_to_grams: (v) => v * 28.3495
      }
    };

    const key = `${args.from_unit}_to_${args.to_unit}`;
    const fn = conversions[args.unit_type]?.[key];

    if (!fn) {
      return {
        content: [
          {
            type: "text",
            text: `Unsupported conversion: ${args.from_unit} to ${args.to_unit}`
          }
        ],
        isError: true
      };
    }

    const result = fn(args.value);
    return {
      content: [
        {
          type: "text",
          text: `${args.value} ${args.from_unit} = ${result.toFixed(4)} ${args.to_unit}`
        }
      ]
    };
  }
);

const converterServer = createSdkMcpServer({
  name: "converter",
  version: "1.0.0",
  tools: [convert]
});
```

После определения сервера передайте его в `query` так же, как в примере с погодой. Этот пример отправляет три разных запроса в цикле, чтобы показать, как один и тот же инструмент обрабатывает разные типы единиц. Для каждого ответа он проверяет объекты `AssistantMessage` (которые содержат вызовы инструментов, которые Claude сделал во время этого хода) и выводит каждый `ToolUseBlock` перед выводом финального текста `ResultMessage`. Это позволяет вам увидеть, когда Claude использует инструмент, а когда отвечает из собственных знаний.

Поскольку [tool search](https://code.claude.com/docs/ru/agent-sdk/tool-search.md) включен по умолчанию, вывод также может включать вызов `ToolSearch`, когда Claude загружает отложенную schema инструмента.

```python Python theme={null}
import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    ResultMessage,
    AssistantMessage,
    ToolUseBlock,
)


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"converter": converter_server},
        allowed_tools=["mcp__converter__convert_units"],
    )

    prompts = [
        "Convert 100 kilometers to miles.",
        "What is 72°F in Celsius?",
        "How many pounds is 5 kilograms?",
    ]

    for prompt in prompts:
        try:
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, ToolUseBlock):
                            print(f"[tool call] {block.name}({block.input})")
                elif isinstance(message, ResultMessage) and message.subtype == "success":
                    print(f"Q: {prompt}\nA: {message.result}\n")
        except Exception as error:
            # A single-shot query() raises after yielding an error result. Only success
            # results are printed above, so handle the failure here and continue with
            # the next prompt.
            print(f"Call failed: {error}")


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const prompts = [
  "Convert 100 kilometers to miles.",
  "What is 72°F in Celsius?",
  "How many pounds is 5 kilograms?"
];

for (const prompt of prompts) {
  try {
    for await (const message of query({
      prompt,
      options: {
        mcpServers: { converter: converterServer },
        allowedTools: ["mcp__converter__convert_units"]
      }
    })) {
      if (message.type === "assistant") {
        for (const block of message.message.content) {
          if (block.type === "tool_use") {
            console.log(`[tool call] ${block.name}`, block.input);
          }
        }
      } else if (message.type === "result" && message.subtype === "success") {
        console.log(`Q: ${prompt}\nA: ${message.result}\n`);
      }
    }
  } catch (error) {
    // A single-shot query() throws after yielding an error result. Only success
    // results are logged above, so handle the failure here and continue with
    // the next prompt.
    console.error(`Call failed: ${error}`);
  }
}
```

## Следующие шаги

Вы можете комбинировать паттерны на этой странице на одном сервере: один сервер может содержать инструмент базы данных, инструмент шлюза API и средство визуализации изображений рядом друг с другом.

Отсюда:

* Если ваш сервер вырастет до десятков инструментов, см. [поиск инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md) для отложенной загрузки их до момента, когда Claude их потребует.
* Для подключения к внешним MCP серверам (файловая система, GitHub, Slack) вместо создания собственных, см. [Подключение MCP серверов](https://code.claude.com/docs/ru/agent-sdk/mcp.md).
* Для управления тем, какие инструменты запускаются автоматически в сравнении с требующими одобрения, см. [Настройка разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md).
