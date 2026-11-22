> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник Agent SDK - Python

> Полный справочник API для Python Agent SDK, включая все функции, типы и классы.

## Установка

Установите пакет в виртуальное окружение. На недавних установках Debian, Ubuntu и Homebrew Python запуск `pip install` для системного Python завершается ошибкой `error: externally-managed-environment`.

```bash theme={null}
python3 -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk
```

Для uv, Windows PowerShell и настройки API-ключа см. раздел [Настройка в быстром старте Agent SDK](https://code.claude.com/docs/ru/agent-sdk/quickstart.md#setup).

## Выбор между `query()` и `ClaudeSDKClient`

Python SDK предоставляет два способа взаимодействия с Claude Code:

| Функция | `query()` | `ClaudeSDKClient` |
| :- | :- | :- |
| **Сеанс** | Создает новый сеанс по умолчанию | Повторно использует один и тот же сеанс |
| **Разговор** | Один обмен | Несколько обменов в одном контексте |
| **Соединение** | Управляется автоматически | Ручное управление |
| **Потоковый ввод** | ✅ Поддерживается | ✅ Поддерживается |
| **Прерывания** | ❌ Не поддерживается | ✅ Поддерживается |
| **Hooks** | ✅ Поддерживается | ✅ Поддерживается |
| **Пользовательские инструменты** | ✅ Поддерживается | ✅ Поддерживается |
| **Продолжить чат** | Ручное через `continue_conversation` или `resume` | ✅ Автоматическое |
| **Вариант использования** | Одноразовые задачи | Непрерывные разговоры |

Используйте `ClaudeSDKClient` для интерактивных приложений, таких как интерфейсы чата, или когда следующее действие зависит от ответа Claude.

## Функции

> [!NOTE]
>
> Блоки сигнатур и голые фрагменты `async for` / `async with` на этой странице являются иллюстративными. Чтобы их запустить, оберните тело в `async def main(): ...` и вызовите `asyncio.run(main())`.

### `query()`

Создает новый сеанс для каждого взаимодействия с Claude Code по умолчанию. Возвращает асинхронный итератор, который выдает сообщения по мере их поступления. Каждый вызов `query()` начинается с нуля без памяти о предыдущих взаимодействиях, если вы не передадите `continue_conversation=True` или `resume` в [`ClaudeAgentOptions`](#claudeagentoptions). См. [Sessions](https://code.claude.com/docs/ru/agent-sdk/sessions.md).

```python theme={null}
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None
) -> AsyncIterator[Message]
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `prompt` | `str \| AsyncIterable[dict]` | Входная подсказка в виде строки или асинхронного итератора для режима потоковой передачи |
| `options` | `ClaudeAgentOptions \| None` | Объект дополнительной конфигурации (по умолчанию `ClaudeAgentOptions()`, если None) |
| `transport` | `Transport \| None` | Дополнительный пользовательский транспорт для связи с процессом CLI |

#### Возвращаемое значение

Возвращает `AsyncIterator[Message]`, который выдает сообщения из разговора.

#### Пример - С параметрами

```python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode="acceptEdits",
    )

    async for message in query(prompt="Create a Python web server", options=options):
        print(message)


asyncio.run(main())
```

### `tool()`

Декоратор для определения MCP tools с проверкой типов.

```python theme={null}
def tool(
    name: str,
    description: str,
    input_schema: type | dict[str, Any],
    annotations: ToolAnnotations | None = None
) -> Callable[[Callable[[Any], Awaitable[dict[str, Any]]]], SdkMcpTool[Any]]
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `name` | `str` | Уникальный идентификатор инструмента |
| `description` | `str` | Понятное описание того, что делает инструмент |
| `input_schema` | `type \| dict[str, Any]` | Схема, определяющая входные параметры инструмента. См. [Input schema options](#input-schema-options) |
| `annotations` | [`ToolAnnotations`](#toolannotations)` \| None` | Дополнительные аннотации MCP tool, предоставляющие подсказки поведения клиентам |

#### Варианты схемы ввода

1. **Простое сопоставление типов** (рекомендуется):

   ```python theme={null}
   {"text": str, "count": int, "enabled": bool}
   ```

2. **Формат JSON Schema** (для сложной валидации):
   ```python theme={null}
   {
       "type": "object",
       "properties": {
           "text": {"type": "string"},
           "count": {"type": "integer", "minimum": 0},
       },
       "required": ["text"],
   }
   ```

3. **Класс TypedDict**: типизированная схема, ключи `NotRequired` которой не включаются в `required`.

   * **Python 3.11 и новее**: импортируйте `TypedDict` и `NotRequired` из `typing`.
   * **Python 3.10**: в `typing` нет `NotRequired`. Импортируйте `TypedDict` и `NotRequired` из `typing_extensions`, который SDK устанавливает на Python 3.10.

   ```python theme={null}
   from typing import Annotated, Any, NotRequired, TypedDict
   from claude_agent_sdk import tool


   class ForecastArgs(TypedDict):
       latitude: Annotated[float, "Latitude coordinate"]
       hours: NotRequired[Annotated[int, "How many hours of forecast to return"]]


   @tool("get_forecast", "Get the hourly forecast for a location", ForecastArgs)
   async def get_forecast(args: dict[str, Any]) -> dict[str, Any]:
       hours = args.get("hours", 12)
       return {"content": [{"type": "text", "text": f"{hours}-hour forecast for {args['latitude']}"}]}
   ```

В формах простого сопоставления и TypedDict оберните тип в `Annotated[type, "description"]`, чтобы задать описание поля.

#### Возвращаемое значение

Функция-декоратор, которая оборачивает реализацию инструмента и возвращает экземпляр `SdkMcpTool`.

#### Пример

```python theme={null}
from claude_agent_sdk import tool
from typing import Any


@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}
```

#### `ToolAnnotations`

Подсказки поведения для инструмента, передаваемые как аргумент `annotations` функции [`tool()`](#tool). `ToolAnnotations` расширяет `mcp.types.ToolAnnotations` SDK MCP с полем `maxResultSizeChars`, и вы можете писать каждую подсказку в camelCase или snake\_case: `ToolAnnotations(readOnlyHint=True)` и `ToolAnnotations(read_only_hint=True)` эквивалентны. Чтобы прочитать подсказку обратно из объекта, используйте написание, объявленное в установленном у вас пакете `mcp`: `.readOnlyHint` в `mcp` 1.x и `.read_only_hint` в 2.x, тогда как `.maxResultSizeChars` работает в обоих. Вы также можете передать простой `mcp.types.ToolAnnotations` везде, где SDK принимает аннотации.

Имена snake\_case и типизированное поле `maxResultSizeChars` требуют Python Agent SDK 0.2.140 или позже. Версии 0.1.31 по 0.2.139 переэкспортируют `mcp.types.ToolAnnotations` без изменений. В версиях 0.1.55 по 0.2.139 вы все еще можете передать `maxResultSizeChars` как аргумент ключевого слова: класс MCP принимает дополнительные поля, и SDK пересылает значение в Claude Code.

Все поля являются дополнительными. Клиенты не должны полагаться на подсказки для решений безопасности.

| Поле | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `title` | `str \| None` | `None` | Понятное название инструмента |
| `readOnlyHint` | `bool \| None` | `False` | Если `True`, инструмент не изменяет свою среду |
| `destructiveHint` | `bool \| None` | `True` | Если `True`, инструмент может выполнять деструктивные обновления (имеет смысл только когда `readOnlyHint` равен `False`) |
| `idempotentHint` | `bool \| None` | `False` | Если `True`, повторные вызовы с одинаковыми аргументами не имеют дополнительного эффекта (имеет смысл только когда `readOnlyHint` равен `False`) |
| `openWorldHint` | `bool \| None` | `True` | Если `True`, инструмент взаимодействует с внешними сущностями (например, веб-поиск). Если `False`, область инструмента закрыта (например, инструмент памяти) |
| `maxResultSizeChars` | `int \| None` | `None` | Количество символов, до которого Claude Code сохраняет текстовый результат этого инструмента встроенным в разговор вместо сохранения в файл, до 500 000. Результаты, содержащие изображения, не затрагиваются. Параметр Claude Code, а не подсказка MCP: SDK отправляет его в `_meta` инструмента как `anthropic/maxResultSizeChars`. См. [Повысить лимит для конкретного инструмента](https://code.claude.com/docs/ru/mcp.md#raise-the-limit-for-a-specific-tool) |

```python theme={null}
from claude_agent_sdk import tool, ToolAnnotations
from typing import Any


@tool(
    "search",
    "Search the web",
    {"query": str},
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
)
async def search(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Results for: {args['query']}"}]}
```

### `create_sdk_mcp_server()`

Создайте встроенный MCP server, который работает в вашем приложении Python.

```python theme={null}
def create_sdk_mcp_server(
    name: str,
    version: str = "1.0.0",
    tools: list[SdkMcpTool[Any]] | None = None
) -> McpSdkServerConfig
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `name` | `str` | - | Уникальный идентификатор сервера |
| `version` | `str` | `"1.0.0"` | Строка версии сервера |
| `tools` | `list[SdkMcpTool[Any]] \| None` | `None` | Список функций инструментов, созданных с помощью декоратора `@tool` |

#### Возвращаемое значение

Возвращает объект `McpSdkServerConfig`, который можно передать в `ClaudeAgentOptions.mcp_servers`.

#### Пример

```python theme={null}
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions


@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}


@tool("multiply", "Multiply two numbers", {"a": float, "b": float})
async def multiply(args):
    return {"content": [{"type": "text", "text": f"Product: {args['a'] * args['b']}"}]}


calculator = create_sdk_mcp_server(
    name="calculator",
    version="2.0.0",
    tools=[add, multiply],  # Pass decorated functions
)

# Use with Claude
options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add", "mcp__calc__multiply"],
)
```

### `list_sessions()`

Выводит список прошлых сеансов с метаданными. Фильтруйте по каталогу проекта или выводите сеансы во всех проектах. Синхронно; возвращается немедленно.

```python theme={null}
def list_sessions(
    directory: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    include_worktrees: bool = True
) -> list[SDKSessionInfo]
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `directory` | `str \| None` | `None` | Каталог для вывода сеансов. Если опущено, возвращает сеансы во всех проектах |
| `limit` | `int \| None` | `None` | Максимальное количество возвращаемых сеансов |
| `offset` | `int` | `0` | Количество сеансов для пропуска с начала отсортированных результатов. Используйте с `limit` для разбиения на страницы |
| `include_worktrees` | `bool` | `True` | Когда `directory` находится внутри репозитория git, включайте сеансы из всех путей worktrees |

#### Тип возвращаемого значения: `SDKSessionInfo`

| Свойство | Тип | Описание |
| :- | :- | :- |
| `session_id` | `str` | Уникальный идентификатор сеанса |
| `summary` | `str` | Отображаемое название: пользовательское название, самый последний запрос, автоматически созданное резюме или первый запрос |
| `last_modified` | `int` | Время последнего изменения в миллисекундах с начала эпохи |
| `file_size` | `int \| None` | Размер файла сеанса в байтах (`None` для удаленных хранилищ) |
| `custom_title` | `str \| None` | Название сеанса, установленное пользователем |
| `first_prompt` | `str \| None` | Первая значимая подсказка пользователя в сеансе |
| `git_branch` | `str \| None` | Ветка Git в конце сеанса |
| `cwd` | `str \| None` | Рабочий каталог для сеанса |
| `tag` | `str \| None` | Тег сеанса, установленный пользователем (см. [`tag_session()`](#tag_session)) |
| `created_at` | `int \| None` | Время создания сеанса в миллисекундах с начала эпохи |

#### Пример

Выведите 10 самых последних сеансов для проекта. Результаты отсортированы по `last_modified` в убывающем порядке, поэтому первый элемент - самый новый. Опустите `directory`, чтобы искать во всех проектах.

```python theme={null}
from claude_agent_sdk import list_sessions

for session in list_sessions(directory="/path/to/project", limit=10):
    print(f"{session.summary} ({session.session_id})")
```

### `get_session_messages()`

Извлекает сообщения из прошлого сеанса. Синхронно; возвращается немедленно.

```python theme={null}
def get_session_messages(
    session_id: str,
    directory: str | None = None,
    limit: int | None = None,
    offset: int = 0
) -> list[SessionMessage]
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `session_id` | `str` | обязательно | ID сеанса для извлечения сообщений |
| `directory` | `str \| None` | `None` | Каталог проекта для поиска. Если опущено, ищет во всех проектах |
| `limit` | `int \| None` | `None` | Максимальное количество возвращаемых сообщений |
| `offset` | `int` | `0` | Количество сообщений для пропуска с начала |

#### Тип возвращаемого значения: `SessionMessage`

| Свойство | Тип | Описание |
| :- | :- | :- |
| `type` | `Literal["user", "assistant"]` | Роль сообщения |
| `uuid` | `str` | Уникальный идентификатор сообщения |
| `session_id` | `str` | Идентификатор сеанса |
| `message` | `Any` | Необработанное содержимое сообщения |
| `parent_tool_use_id` | `str \| None` | Для сообщений подагента, ID блока tool-use `Agent`, который его создал. `None` для сообщений основного сеанса и более старых сеансов |
| `parent_agent_id` | `str \| None` | Для сообщений от [вложенного подагента](https://code.claude.com/docs/ru/sub-agents.md#let-subagents-spawn-their-own-subagents), ID агента родительского подагента. `None` для сообщений основного сеанса, сообщений подагента верхнего уровня и более старых сеансов. Требует Python Agent SDK 0.2.140 или позже |

#### Пример

```python theme={null}
from claude_agent_sdk import list_sessions, get_session_messages

sessions = list_sessions(limit=1)
if sessions:
    messages = get_session_messages(sessions[0].session_id)
    for msg in messages:
        print(f"[{msg.type}] {msg.uuid}")
```

### `get_session_info()`

Читает метаданные для одного сеанса по ID без сканирования полного каталога проекта. Синхронно; возвращается немедленно.

```python theme={null}
def get_session_info(
    session_id: str,
    directory: str | None = None,
) -> SDKSessionInfo | None
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `session_id` | `str` | обязательно | UUID сеанса для поиска |
| `directory` | `str \| None` | `None` | Путь каталога проекта. Если опущено, ищет во всех каталогах проектов |

Возвращает [`SDKSessionInfo`](#return-type-sdksessioninfo) или `None`, если сеанс не найден.

#### Пример

Найдите метаданные одного сеанса без сканирования каталога проекта. Полезно, когда у вас уже есть ID сеанса из предыдущего запуска.

```python theme={null}
from claude_agent_sdk import get_session_info

info = get_session_info("550e8400-e29b-41d4-a716-446655440000")
if info:
    print(f"{info.summary} (branch: {info.git_branch}, tag: {info.tag})")
```

### `rename_session()`

Переименовывает сеанс, добавляя запись с пользовательским названием. Повторные вызовы безопасны; побеждает самое последнее название. Синхронно.

```python theme={null}
def rename_session(
    session_id: str,
    title: str,
    directory: str | None = None,
) -> None
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `session_id` | `str` | обязательно | UUID сеанса для переименования |
| `title` | `str` | обязательно | Новое название. Должно быть непустым после удаления пробелов |
| `directory` | `str \| None` | `None` | Путь каталога проекта. Если опущено, ищет во всех каталогах проектов |

Вызывает `ValueError`, если `session_id` не является допустимым UUID или `title` пуст; `FileNotFoundError`, если сеанс не найден.

#### Пример

Переименуйте самый последний сеанс, чтобы его было легче найти позже. Новое название появляется в [`SDKSessionInfo.custom_title`](#return-type-sdksessioninfo) при последующих чтениях.

```python theme={null}
from claude_agent_sdk import list_sessions, rename_session

sessions = list_sessions(directory="/path/to/project", limit=1)
if sessions:
    rename_session(sessions[0].session_id, "Refactor auth module")
```

### `tag_session()`

Помечает сеанс. Передайте `None` для очистки тега. Повторные вызовы безопасны; побеждает самый последний тег. Синхронно.

```python theme={null}
def tag_session(
    session_id: str,
    tag: str | None,
    directory: str | None = None,
) -> None
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `session_id` | `str` | обязательно | UUID сеанса для пометки |
| `tag` | `str \| None` | обязательно | Строка тега или `None` для очистки. Очищается от Unicode перед сохранением |
| `directory` | `str \| None` | `None` | Путь каталога проекта. Если опущено, ищет во всех каталогах проектов |

Вызывает `ValueError`, если `session_id` не является допустимым UUID или `tag` пуст после очистки; `FileNotFoundError`, если сеанс не найден.

#### Пример

Пометьте сеанс, затем отфильтруйте по этому тегу при последующем чтении. Передайте `None` для очистки существующего тега.

```python theme={null}
from claude_agent_sdk import list_sessions, tag_session

# Tag the most recent session
sessions = list_sessions(directory="/path/to/project", limit=1)
if sessions:
    tag_session(sessions[0].session_id, "needs-review")

# Later: find all sessions with that tag
for session in list_sessions(directory="/path/to/project"):
    if session.tag == "needs-review":
        print(session.summary)
```

### `fork_session()`

Копирует транскрипт сессии в новую сессию, чтобы вы могли направить диалог в другую сторону, а исходная сессия осталась без изменений. Чтобы создать ответвление от более ранней точки диалога, передайте `up_to_message_id`. Синхронно.

```python theme={null}
def fork_session(
    session_id: str,
    directory: str | None = None,
    up_to_message_id: str | None = None,
    title: str | None = None,
) -> ForkSessionResult
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `session_id` | `str` | обязательно | UUID сессии для форка |
| `directory` | `str \| None` | `None` | Путь каталога проекта. Если опущено, ищет во всех каталогах проектов |
| `up_to_message_id` | `str \| None` | `None` | Копировать транскрипт до сообщения с этим UUID включительно, например `uuid` из [`get_session_messages()`](#get_session_messages). Если опущено, копирует весь транскрипт |
| `title` | `str \| None` | `None` | Название форка. Если опущено, SDK формирует его из исходной сессии с добавлением `(fork)` |

Возвращает `ForkSessionResult`, в котором `session_id` — это UUID новой сессии. Передайте его как [`resume`](#claudeagentoptions), чтобы продолжить форк. Форк не включает [чекпоинты файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) исходной сессии, поэтому вы не сможете откатить его к чекпоинту, созданному до форка.

`fork_session()` вызывает:

* `ValueError`: `session_id` или `up_to_message_id` не является допустимым UUID
* `ValueError`: в сессии нет сообщений, или `up_to_message_id` не соответствует ни одному сообщению в транскрипте
* `FileNotFoundError`: сессия не найдена

#### Пример

Создайте форк самой последней сессии с новым названием, затем возобновите форк. Исходная сессия сохраняет собственную историю.

```python theme={null}
from claude_agent_sdk import fork_session, list_sessions

sessions = list_sessions(directory="/path/to/project", limit=1)
if sessions:
    forked = fork_session(sessions[0].session_id, title="Try the OAuth approach")
    print(forked.session_id)  # pass as ClaudeAgentOptions(resume=...) to continue the fork
```

## Классы

### `ClaudeSDKClient`

**Поддерживает сеанс разговора через несколько обменов.** Это эквивалент Python того, как функция `query()` TypeScript SDK работает внутри - она создает объект клиента, который может продолжать разговоры. См. [сравнение с `query()`](#choosing-between-query-and-claudesdkclient).

```python theme={null}
class ClaudeSDKClient:
    def __init__(self, options: ClaudeAgentOptions | None = None, transport: Transport | None = None)
    async def connect(self, prompt: str | AsyncIterable[dict] | None = None) -> None
    async def query(self, prompt: str | AsyncIterable[dict], session_id: str = "default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def set_permission_mode(self, mode: PermissionMode) -> None
    async def set_model(self, model: str | None = None) -> None
    async def rewind_files(self, user_message_id: str) -> None
    async def get_mcp_status(self) -> McpStatusResponse
    async def get_context_usage(self) -> ContextUsageResponse
    async def reconnect_mcp_server(self, server_name: str) -> None
    async def toggle_mcp_server(self, server_name: str, enabled: bool) -> None
    async def stop_task(self, task_id: str) -> None
    async def get_server_info(self) -> dict[str, Any] | None
    async def disconnect(self) -> None
```

#### Методы

| Метод | Описание |
| :- | :- |
| `__init__(options)` | Инициализируйте клиент с дополнительной конфигурацией |
| `connect(prompt)` | Подключитесь к Claude с дополнительной начальной подсказкой или потоком сообщений |
| `query(prompt, session_id)` | Отправьте новый запрос в режиме потоковой передачи |
| `receive_messages()` | Получайте все сообщения от Claude как асинхронный итератор |
| `receive_response()` | Получайте сообщения до и включая ResultMessage |
| `interrupt()` | Отправьте сигнал прерывания (работает только в режиме потоковой передачи) |
| `set_permission_mode(mode)` | Измените режим разрешений для текущего сеанса |
| `set_model(model)` | Измените модель для текущей сессии. Передайте `None` для сброса на [модель по умолчанию Claude Code](https://code.claude.com/docs/ru/model-config.md). Сессия в режиме `auto` [переключается в режим `default`](https://code.claude.com/docs/ru/agent-sdk/permissions#auto-mode-auto), если новая модель не поддерживает авторежим |
| `rewind_files(user_message_id)` | Восстановите файлы в их состояние в указанном пользовательском сообщении. Требует `enable_file_checkpointing=True`. См. [Чекпоинты файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) |
| `get_mcp_status()` | Получите статус всех настроенных MCP servers. Возвращает [`McpStatusResponse`](#mcpstatusresponse) |
| `get_context_usage()` | Получите разбивку использования контекстного окна по категориям, скиллам и инструментам. Включает данные, которые `/context` показывает в интерактивной сессии. Возвращает [`ContextUsageResponse`](#contextusageresponse). Для вычисления разбивки Claude Code делает несколько запросов API подсчета токенов, которые не отображаются в потоке сообщений; см. [как эти запросы обрабатываются](#contextusageresponse) |
| `reconnect_mcp_server(server_name)` | Повторите попытку подключения к MCP server, который не удался или был отключен |
| `toggle_mcp_server(server_name, enabled)` | Включите или отключите MCP server в середине сеанса. Отключение удаляет его инструменты |
| `stop_task(task_id)` | Остановите выполняющуюся фоновую задачу. [`TaskNotificationMessage`](#tasknotificationmessage) со статусом `"stopped"` следует в потоке сообщений |
| `get_server_info()` | Получите информацию об инициализации сервера, включая доступные команды и стили вывода |
| `disconnect()` | Отключитесь от Claude |

#### Поддержка менеджера контекста

Клиент можно использовать как асинхронный менеджер контекста для автоматического управления соединением:

```python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient


async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Hello Claude")
        async for message in client.receive_response():
            print(message)


asyncio.run(main())
```

> **Важно:** При итерации по сообщениям избегайте использования `break` для раннего выхода, так как это может вызвать проблемы с очисткой asyncio. Вместо этого позвольте итерации завершиться естественным образом или используйте флаги для отслеживания, когда вы нашли то, что вам нужно.

#### Пример - Продолжение разговора

```python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage


async def main():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")

        # Process response
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up question - the session retains the previous context
        await client.query("What's the population of that city?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Another follow-up - still in the same conversation
        await client.query("What are some famous landmarks there?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")


asyncio.run(main())
```

#### Пример - Потоковый ввод с ClaudeSDKClient

`query()` также принимает асинхронный итерируемый объект словарей пользовательских сообщений, поэтому вы можете собрать подсказку во время отправки или включить блоки содержимого, такие как изображения. Claude Code начинает отвечать на первое полученное сообщение сразу же по его прибытии, не дожидаясь завершения итерируемого объекта, и `receive_response()` останавливается на `ResultMessage`, который завершает этот ответ. Поместите все, что Claude должен прочитать перед ответом, в одно сообщение, как это делает этот генератор, и свяжите каждый вызов `query()` с его собственным циклом `receive_response()`.

```python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient


async def message_stream():
    """Assemble the prompt at send time and yield it as one user message."""
    readings = {"Temperature": "25°C", "Humidity": "60%"}
    data = ", ".join(f"{name}: {value}" for name, value in readings.items())
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": f"Analyze the following sensor data and describe any patterns you see: {data}",
        },
    }


async def main():
    async with ClaudeSDKClient() as client:
        # Stream input to Claude
        await client.query(message_stream())

        # Process response
        async for message in client.receive_response():
            print(message)

        # Follow-up in same session
        await client.query("Should we be concerned about these readings?")

        async for message in client.receive_response():
            print(message)


asyncio.run(main())
```

#### Пример - Использование прерываний

```python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ResultMessage


async def interruptible_task():
    options = ClaudeAgentOptions(allowed_tools=["Bash"], permission_mode="acceptEdits")

    async with ClaudeSDKClient(options=options) as client:
        # Start a long-running task
        await client.query("Count from 1 to 100 slowly, using the bash sleep command")

        # Let it run for a bit
        await asyncio.sleep(2)

        # Interrupt the task
        await client.interrupt()
        print("Task interrupted!")

        # Drain the interrupted task's messages (including its ResultMessage)
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                print(f"Interrupted task: terminal_reason={message.terminal_reason!r}")
                # terminal_reason is "aborted_streaming" or "aborted_tools"
                # for interrupted turns

        # Send a new command
        await client.query("Just say hello instead")

        # Now receive the new response
        async for message in client.receive_response():
            if isinstance(message, ResultMessage) and message.subtype == "success":
                print(f"New result: {message.result}")


asyncio.run(interruptible_task())
```

> [!NOTE]
>
> **Поведение буфера после прерывания:** `interrupt()` отправляет сигнал остановки, но не очищает буфер сообщений. Сообщения, уже созданные прерванной задачей, включая ее `ResultMessage`, остаются в потоке. Вы должны слить их с помощью `receive_response()` перед чтением ответа на новый запрос. Если вы отправите новый запрос сразу после `interrupt()` и вызовете `receive_response()` только один раз, вы получите сообщения прерванной задачи, а не ответ на новый запрос.

#### Пример - Расширенное управление разрешениями

```python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


async def custom_permission_handler(
    tool_name: str, input_data: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Custom logic for tool permissions."""

    # Block writes to system directories
    if tool_name == "Write" and input_data.get("file_path", "").startswith("/system/"):
        return PermissionResultDeny(
            message="System directory write not allowed", interrupt=True
        )

    # Redirect sensitive file operations
    if tool_name in ["Write", "Edit"] and "config" in input_data.get("file_path", ""):
        safe_path = f"./sandbox/{input_data['file_path']}"
        return PermissionResultAllow(
            updated_input={**input_data, "file_path": safe_path}
        )

    # Allow everything else
    return PermissionResultAllow(updated_input=input_data)


async def main():
    # Don't also list the gated tools in allowed_tools: allow rules approve calls before can_use_tool runs
    options = ClaudeAgentOptions(can_use_tool=custom_permission_handler)

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Update the system config file")

        async for message in client.receive_response():
            # Will use sandbox path instead
            print(message)


asyncio.run(main())
```

## Типы

> [!NOTE]
>
> **`@dataclass` vs `TypedDict`:** Этот SDK использует два вида типов. Классы, украшенные `@dataclass` (такие как `ResultMessage`, `AgentDefinition`, `TextBlock`), являются экземплярами объектов во время выполнения и поддерживают доступ к атрибутам: `msg.result`. Классы, определённые с помощью `TypedDict` (такие как `ThinkingConfigEnabled`, `McpStdioServerConfig`, `SyncHookJSONOutput`), являются **простыми словарями во время выполнения** и требуют доступа по ключам: `config["budget_tokens"]`, а не `config.budget_tokens`. Синтаксис вызова `ClassName(field=value)` работает для обоих, но только dataclasses создают объекты с атрибутами.

### `SdkMcpTool`

Определение инструмента SDK MCP, созданного с помощью декоратора `@tool`.

```python theme={null}
@dataclass
class SdkMcpTool(Generic[T]):
    name: str
    description: str
    input_schema: type[T] | dict[str, Any]
    handler: Callable[[T], Awaitable[dict[str, Any]]]
    annotations: ToolAnnotations | None = None
```

| Свойство | Тип | Описание |
| :- | :- | :- |
| `name` | `str` | Уникальный идентификатор инструмента |
| `description` | `str` | Описание, понятное человеку |
| `input_schema` | `type[T] \| dict[str, Any]` | Схема для валидации входных данных |
| `handler` | `Callable[[T], Awaitable[dict[str, Any]]]` | Асинхронная функция, которая обрабатывает выполнение инструмента |
| `annotations` | [`ToolAnnotations`](#toolannotations)` \| None` | Дополнительные аннотации инструмента (например `readOnlyHint`, `destructiveHint`, `openWorldHint`, `maxResultSizeChars`) |

### `Transport`

Абстрактный базовый класс для пользовательских реализаций транспорта. Используйте это для связи с процессом Claude через пользовательский канал (например, удалённое соединение вместо локального подпроцесса).

> [!WARNING]
>
> Это низкоуровневый внутренний API. Интерфейс может измениться в будущих версиях. Пользовательские реализации должны быть обновлены в соответствии с любыми изменениями интерфейса.

```python theme={null}
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class Transport(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def write(self, data: str) -> None: ...

    @abstractmethod
    def read_messages(self) -> AsyncIterator[dict[str, Any]]: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    def is_ready(self) -> bool: ...

    @abstractmethod
    async def end_input(self) -> None: ...
```

| Метод | Описание |
| :- | :- |
| `connect()` | Подключить транспорт и подготовить к связи |
| `write(data)` | Записать необработанные данные (JSON + новая строка) в транспорт |
| `read_messages()` | Асинхронный итератор, который выдаёт разобранные JSON-сообщения |
| `close()` | Закрыть соединение и очистить ресурсы |
| `is_ready()` | Возвращает `True`, если транспорт может отправлять и получать |
| `end_input()` | Закрыть входной поток (например, закрыть stdin для транспортов подпроцесса) |

Импорт: `from claude_agent_sdk import Transport`

### `ClaudeAgentOptions`

Конфигурационный dataclass для запросов Claude Code.

```python theme={null}
@dataclass
class ClaudeAgentOptions:
    tools: list[str] | ToolsPreset | None = None
    allowed_tools: list[str] = field(default_factory=list)
    system_prompt: str | SystemPromptPreset | SystemPromptCustom | SystemPromptFile | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    strict_mcp_config: bool = False
    permission_mode: PermissionMode | None = None
    continue_conversation: bool = False
    resume: str | None = None
    session_id: str | None = None
    max_turns: int | None = None
    max_budget_usd: float | None = None
    disallowed_tools: list[str] = field(default_factory=list)
    model: str | None = None
    fallback_model: str | None = None
    betas: list[SdkBeta] = field(default_factory=list)
    output_format: dict[str, Any] | None = None
    permission_prompt_tool_name: str | None = None
    cwd: str | Path | None = None
    cli_path: str | Path | None = None
    settings: str | None = None
    add_dirs: list[str | Path] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, str | None] = field(default_factory=dict)
    max_buffer_size: int | None = None
    debug_stderr: Any = sys.stderr  # Deprecated
    stderr: Callable[[str], None] | None = None
    can_use_tool: CanUseTool | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    user: str | None = None
    include_partial_messages: bool = False
    include_hook_events: bool = False
    forward_subagent_text: bool = False
    verbatim_prompts: bool = False
    fork_session: bool = False
    resume_session_at: str | None = None
    resume_drops_turn: str | None = None
    agents: dict[str, AgentDefinition] | None = None
    setting_sources: list[SettingSource] | None = None
    skills: list[str] | Literal["all"] | None = None
    sandbox: SandboxSettings | None = None
    plugins: list[SdkPluginConfig] = field(default_factory=list)
    max_thinking_tokens: int | None = None  # Deprecated: use thinking instead
    thinking: ThinkingConfig | None = None
    effort: EffortLevel | None = None
    enable_file_checkpointing: bool = False
    session_store: SessionStore | None = None
    session_store_flush: SessionStoreFlushMode = "batched"
    load_timeout_ms: int = 60_000
    task_budget: TaskBudget | None = None
```

| Свойство | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `tools` | `list[str] \| ToolsPreset \| None` | `None` | Конфигурация инструментов. Используйте `{"type": "preset", "preset": "claude_code"}` для инструментов Claude Code по умолчанию |
| `allowed_tools` | `list[str]` | `[]` | Инструменты для автоматического одобрения без запроса разрешения, за исключением чтения по [сетевым путям](https://code.claude.com/docs/ru/permissions.md#network-paths). Это не ограничивает Claude только этими инструментами. Если вы укажете здесь один из [инструментов отслеживания задач](https://code.claude.com/docs/ru/agent-sdk/todo-tracking.md#model-availability), Claude Code также включает их для сессии. Остальные неуказанные инструменты передаются на обработку `permission_mode` и `can_use_tool`. Используйте `disallowed_tools` для блокировки инструментов. См. [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules) |
| `system_prompt` | `str \| SystemPromptPreset \| SystemPromptCustom \| SystemPromptFile \| None` | `None` | Конфигурация системного промпта. Передайте строку для пользовательского промпта, `{"type": "preset", "preset": "claude_code"}` для системного промпта Claude Code с необязательным `"append"`, `{"type": "custom", "prompt": "..."}` для пользовательского промпта, который также может задать `"snapshot"`, или `{"type": "file", "path": "..."}` для загрузки большого промпта с диска. См. [`SystemPromptPreset`](#systempromptpreset), [`SystemPromptCustom`](#systempromptcustom) и [`SystemPromptFile`](#systempromptfile) |
| `mcp_servers` | `dict[str, McpServerConfig] \| str \| Path` | `{}` | Конфигурации MCP-серверов или путь к файлу конфигурации |
| `strict_mcp_config` | `bool` | `False` | При значении `True` используются серверы, переданные в `mcp_servers`, а файл `.mcp.json` проекта, пользовательские настройки, MCP-серверы, предоставляемые плагинами, и [коннекторы claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai) игнорируются. Соответствует флагу CLI `--strict-mcp-config` |
| `permission_mode` | `PermissionMode \| None` | `None` | Режим разрешений для использования инструментов |
| `continue_conversation` | `bool` | `False` | Продолжить самый последний диалог |
| `resume` | `str \| None` | `None` | ID сессии для возобновления |
| `session_id` | `str \| None` | `None` | Использовать определённый ID сессии вместо автоматически сгенерированного. Должен быть действительным UUID. Нельзя сочетать с `continue_conversation` или `resume`, если не задан также `fork_session` |
| `max_turns` | `int \| None` | `None` | Максимальное количество агентских [ходов](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#turns-and-messages) |
| `max_budget_usd` | `float \| None` | `None` | Остановить запрос, когда оценка стоимости на стороне клиента достигнет этого значения в USD. Оценка может превысить это значение, поэтому [оставьте запас](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#budget-headroom). Учитывает только расходы самого вызова; итоги, восстановленные из возобновлённой сессии, не учитываются. Об оговорках по точности и поведении сброса см. [Отслеживание затрат и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md) |
| `disallowed_tools` | `list[str]` | `[]` | Инструменты для запрета. Простое имя, такое как `"Bash"`, удаляет инструмент из контекста Claude. Правило с уточнением, такое как `"Bash(rm *)"`, оставляет инструмент доступным и запрещает соответствующие вызовы в каждом режиме разрешений, включая `bypassPermissions`, для команды [в том виде, как она написана](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits). См. [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules) |
| `enable_file_checkpointing` | `bool` | `False` | Включить отслеживание изменений файлов для перемотки. См. [Чекпоинты файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) |
| `model` | `str \| None` | `None` | Псевдоним модели Claude или полное имя модели. См. [допустимые значения и ID, специфичные для поставщика](https://code.claude.com/docs/ru/model-config.md#available-models) |
| `fallback_model` | `str \| None` | `None` | Резервная модель, используемая при сбое основной модели. Принимает список, разделённый запятыми. Рекомендации см. в разделе [Выбор модели](https://code.claude.com/docs/ru/agent-sdk/configuration.md#choose-a-model) |
| `betas` | `list[SdkBeta]` | `[]` | Бета-функции для включения. См. [`SdkBeta`](#sdkbeta) для доступных опций |
| `output_format` | `dict[str, Any] \| None` | `None` | Формат вывода для структурированных ответов (например, `{"type": "json_schema", "schema": {...}}`). Подробнее см. [Структурированные выходы](https://code.claude.com/docs/ru/agent-sdk/structured-outputs.md) |
| `permission_prompt_tool_name` | `str \| None` | `None` | Имя инструмента MCP для запросов разрешения |
| `cwd` | `str \| Path \| None` | `None` | Текущий рабочий каталог |
| `cli_path` | `str \| Path \| None` | `None` | Пользовательский путь к исполняемому файлу Claude Code CLI |
| `settings` | `str \| None` | `None` | Путь к файлу настроек или встроенная строка JSON |
| `add_dirs` | `list[str \| Path]` | `[]` | Дополнительные каталоги, к которым Claude может получить доступ. SDK передаёт каждую запись в Claude Code как `--add-dir`, поэтому с источником настроек `project` Claude Code также [загружает скиллы, команды и субагентов каталога](https://code.claude.com/docs/ru/permissions.md#additional-directories-grant-file-access-not-configuration) |
| `env` | `dict[str, str]` | `{}` | Переменные окружения, объединённые поверх унаследованного окружения процесса. См. [Переменные окружения](https://code.claude.com/docs/ru/env-vars.md) для переменных, которые читает базовый CLI, и [Обработка медленных или зависших ответов API](#handle-slow-or-stalled-api-responses) для переменных, связанных с таймаутами. Установите `CLAUDE_AGENT_SDK_CLIENT_APP` для идентификации вашего приложения в заголовке User-Agent |
| `extra_args` | `dict[str, str \| None]` | `{}` | Дополнительные аргументы CLI для передачи непосредственно в CLI |
| `max_buffer_size` | `int \| None` | `None` | Максимальная длина отдельного сообщения, которое SDK принимает от CLI, в символах. При `None` используется 1 048 576. Более длинное сообщение вызывает [`CLIJSONDecodeError`](#clijsondecodeerror) |
| `debug_stderr` | `Any` | `sys.stderr` | *Устарело* - SDK игнорирует это значение. Используйте обратный вызов `stderr` для вывода stderr CLI |
| `stderr` | `Callable[[str], None] \| None` | `None` | Функция обратного вызова для вывода stderr из CLI |
| `can_use_tool` | [`CanUseTool`](#canusetool) ` \| None` | `None` | Обратный вызов разрешений инструмента, вызываемый только тогда, когда [процесс проверки разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated) доходит до запроса разрешения. Не вызывается для вызовов, автоматически одобренных `allowed_tools`, правилами разрешения или `permission_mode`. Правило разрешения не одобряет заранее [действия, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). Подробнее см. [`CanUseTool`](#canusetool) |
| `hooks` | `dict[HookEvent, list[HookMatcher]] \| None` | `None` | Конфигурации хуков для перехвата событий |
| `user` | `str \| None` | `None` | На платформах POSIX учётная запись пользователя ОС, под которой работает подпроцесс Claude Code. Claude Code сохраняет окружение родительского процесса, включая `HOME`, и работает в `cwd` |
| `include_partial_messages` | `bool` | `False` | Включить события потоковой передачи частичных сообщений. Когда включено, выдаются сообщения [`StreamEvent`](#streamevent) |
| `include_hook_events` | `bool` | `False` | Включить события жизненного цикла хуков в поток сообщений как объекты `HookEventMessage` |
| `forward_subagent_text` | `bool` | `False` | Пересылать текстовые блоки и блоки размышлений субагента в поток сообщений. Без этой опции Claude Code опускает текстовые блоки и блоки размышлений субагента, который выполняется [на переднем плане](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background). О вложенных субагентах, скиллах с `context: fork` и версии Claude Code, необходимой в каждом случае, см. [Отслеживание сообщений субагентов](https://code.claude.com/docs/ru/headless.md#follow-subagent-messages). Требует Python Agent SDK 0.2.140 или новее |
| `verbatim_prompts` | `bool` | `False` | Доставлять каждый промпт в том виде, как он написан. SDK отправляет каждое пользовательское сообщение с `client_composed`, установленным в `True`. Что Claude Code пропускает для таких сообщений, см. в [`client_composed`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkusermessage). Используйте эту опцию, когда текст вашего промпта включает содержимое, которое конечный пользователь не вводил. Для управления на уровне отдельных ходов оставьте её отключённой и вместо этого устанавливайте `"client_composed": True` для отдельных потоковых сообщений. Пока опция включена, SDK перезаписывает любое заданное вами значение `client_composed`. Требует Python Agent SDK 0.2.158 или новее и Claude Code v2.1.248 или новее; CLI, поставляемый с этими версиями SDK, удовлетворяет требованию к Claude Code |
| `fork_session` | `bool` | `False` | При возобновлении с `resume` создать ответвление с новым ID сессии вместо продолжения исходной сессии |
| `resume_session_at` | `str \| None` | `None` | При возобновлении загрузить диалог только до сообщения с этим UUID включительно. Используйте с `resume` и обычно с `fork_session`, чтобы создать ответвление с более ранней точки. Требует Python Agent SDK 0.2.137 или новее |
| `resume_drops_turn` | `str \| None` | `None` | UUID пользовательского промпта, ход которого отбрасывается усечением `resume_session_at`. Если задано, CLI отказывает в возобновлении, если отброшенный диапазон содержит записи, не относящиеся к этому ходу. Требует Python Agent SDK 0.2.137 или новее и Claude Code v2.1.223 или новее; CLI, поставляемый с этими версиями SDK, удовлетворяет требованию к Claude Code |
| `agents` | `dict[str, AgentDefinition] \| None` | `None` | Программно определённые субагенты |
| `plugins` | `list[SdkPluginConfig]` | `[]` | Загрузить пользовательские плагины из локальных путей. Подробнее см. [Плагины](https://code.claude.com/docs/ru/agent-sdk/plugins.md) |
| `sandbox` | [`SandboxSettings`](#sandboxsettings) ` \| None` | `None` | Программно настроить поведение песочницы. Подробнее см. [Настройки песочницы](#sandboxsettings) |
| `setting_sources` | `list[SettingSource] \| None` | `None` (CLI defaults: all sources) | Управляет тем, какие настройки файловой системы загружать. Передайте `[]`, чтобы отключить пользовательские, проектные и локальные настройки. Если `skills` задан, а это поле не задано, загружаются только пользовательские и проектные источники. Задайте `setting_sources` явно, чтобы сохранить локальные настройки. Политика, управляемая на конечном устройстве, загружается в любом случае; настройки, управляемые сервером, извлекаются, когда сессия аутентифицируется с учётными данными организации в [подходящей конфигурации](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability). О входных данных, которые читаются независимо от этой опции, см. [Что settingSources не контролирует](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#what-settingsources-does-not-control) |
| `skills` | `list[str] \| Literal["all"] \| None` | `None` | Скиллы, доступные для сессии. Передайте `"all"`, чтобы включить все обнаруженные скиллы, или список имён скиллов. Передавайте только точные имена. SDK отклоняет некорректные имена и имена с подстановочными знаками с ошибкой `ValueError` до запуска процесса Claude Code; эта проверка требует Python Agent SDK 0.2.129 или новее. Если задано, SDK автоматически добавляет инструмент Skill в `allowed_tools`. Если вы также передаёте `tools`, включите `"Skill"` в этот список. См. [Скиллы](https://code.claude.com/docs/ru/agent-sdk/skills.md) |
| `max_thinking_tokens` | `int \| None` | `None` | *Устарело* - Максимальное количество токенов для блоков размышлений. Используйте вместо этого `thinking` |
| `thinking` | [`ThinkingConfig`](#thinkingconfig) ` \| None` | `None` | Управляет поведением расширенного мышления. Имеет приоритет над `max_thinking_tokens` |
| `effort` | [`EffortLevel`](#effortlevel) ` \| None` | `None` | Уровень effort, определяющий глубину мышления. См. [настройку уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) |
| `session_store` | [`SessionStore`](https://code.claude.com/docs/ru/agent-sdk/session-storage#the-sessionstore-interface) ` \| None` | `None` | Зеркалировать транскрипты сессий во внешний бэкенд, чтобы другой хост мог их возобновить. См. [Сохранение сессий во внешнем хранилище](https://code.claude.com/docs/ru/agent-sdk/session-storage.md) |
| `session_store_flush` | `Literal["batched", "eager"]` | `"batched"` | Когда сбрасывать зеркалируемые записи транскрипта в `session_store`. `"batched"` сбрасывает один раз за ход или при заполнении буфера; `"eager"` запускает фоновый сброс после каждого кадра. Игнорируется, когда `session_store` равен `None` |
| `load_timeout_ms` | `int` | `60000` | Таймаут на каждый вызов `session_store.load()` и `list_subkeys()` во время материализации при возобновлении, в миллисекундах |
| `task_budget` | `TaskBudget \| None` | `None` | Бюджет токенов на стороне API. Отправляется как `output_config.task_budget` с бета-заголовком `task-budgets-2026-03-13`. Передайте `{"total": <int>}`. |

#### Обработка медленных или зависших ответов API

Подпроцесс CLI читает несколько переменных окружения, которые управляют таймаутами API и обнаружением зависаний. Передайте их через `ClaudeAgentOptions.env`:

```python theme={null}
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    env={
        "API_TIMEOUT_MS": "120000",
        "CLAUDE_CODE_MAX_RETRIES": "2",
        "CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS": "120000",
    },
)
```

* [`API_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars): сколько времени каждая попытка запроса может ожидать заголовков ответа, в миллисекундах. Не ограничивает продолжительность потокового ответа после получения заголовков. По умолчанию `600000`. Применяется к основному циклу и всем субагентам.
* `CLAUDE_CODE_MAX_RETRIES`: максимальное количество повторных попыток API. По умолчанию `10`, ограничено значением `15`. Каждая повторная попытка получает собственное окно `API_TIMEOUT_MS`.

  Для автоматических запусков, которым нужно пережидать более длительные сбои, установите [`CLAUDE_CODE_RETRY_WATCHDOG=1`](https://code.claude.com/docs/ru/errors#tune-retry-behavior): эта настройка бесконечно повторяет попытки при временных ошибках нехватки ёмкости и, в Claude Code v2.1.199 или новее, повышает значение по умолчанию для других временных ошибок до `300` и снимает ограничение с этой переменной.
* `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`: сторож зависаний для субагентов. Пока включён сторож потока, значение по умолчанию равно `CLAUDE_STREAM_IDLE_TIMEOUT_MS` плюс 5 минут, что составляет `600000`, если вы не увеличите эту переменную. Когда сторож потока отключён, значение по умолчанию — `600000`. До v2.1.257 значение по умолчанию всегда было `600000`.

  Таймер сбрасывается при каждом событии потока. При зависании Claude Code прерывает субагента и сообщает о зависании родителю. Для фонового субагента он также помечает задачу как неудавшуюся и прикрепляет любой частичный результат.
* `CLAUDE_ENABLE_STREAM_WATCHDOG` вместе с `CLAUDE_STREAM_IDLE_TIMEOUT_MS`: сторож потока, который прерывает запрос, когда заголовки уже получены, но тело ответа перестало передаваться. Сторож включён по умолчанию для всех поставщиков; установите `CLAUDE_ENABLE_STREAM_WATCHDOG=0`, чтобы его отключить. `CLAUDE_STREAM_IDLE_TIMEOUT_MS` по умолчанию равно `300000` и не может быть меньше этого минимума. Что делает Claude Code после прерывания в зависимости от того, насколько продвинулся ответ, описано в разделе [Автоматические повторные попытки](https://code.claude.com/docs/ru/errors.md#automatic-retries).

  Пока сторож ожидает ответ, который шлюз за `ANTHROPIC_BASE_URL` удерживает открытым с помощью keep-alive пингов, хост, установивший `include_partial_messages`, продолжает получать сообщения `ping` [`StreamEvent`](#streamevent). Воспринимайте эти кадры как признак активности, а не завершайте сессию по таймауту из-за отсутствия данных. До v2.1.257 эти кадры прекращались через 5 минут после последнего реального события потока.

### `OutputFormat`

Конфигурация для валидации структурированного вывода. Передайте это как `dict` в поле `output_format` в `ClaudeAgentOptions`:

```python theme={null}
# Ожидаемая форма dict для output_format
{
    "type": "json_schema",
    "schema": {...},  # Ваше определение JSON Schema
}
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `type` | Да | Должно быть `"json_schema"` для валидации JSON Schema |
| `schema` | Да | Определение JSON Schema для валидации вывода |

### `SystemPromptPreset`

Конфигурация для использования предустановленного системного промпта Claude Code с необязательными дополнениями.

```python theme={null}
class SystemPromptPreset(TypedDict):
    type: Literal["preset"]
    preset: Literal["claude_code"]
    append: NotRequired[str]
    exclude_dynamic_sections: NotRequired[bool]
    snapshot: NotRequired[bool]
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `type` | Да | Должно быть `"preset"` для использования предустановленного системного промпта |
| `preset` | Да | Должно быть `"claude_code"` для использования системного промпта Claude Code |
| `append` | Нет | Дополнительные инструкции, добавляемые к предустановленному системному промпту |
| `exclude_dynamic_sections` | Нет | Перенести контекст, специфичный для пользователя, например расположение автоматической памяти, из системного промпта в первое пользовательское сообщение. Улучшает повторное использование кэша промптов между пользователями и машинами. См. [Изменение системных промптов](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#improve-prompt-caching-across-users-and-machines) |
| `snapshot` | Нет | Установите `False`, чтобы пересобирать системный промпт при каждом запросе вместо [повторного использования промпта, записанного сессией при первом запросе](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#change-the-prompt-of-an-existing-session). Требует `claude-agent-sdk` v0.2.153 или новее |

### `SystemPromptCustom`

Пользовательский системный промпт в форме объекта, эквивалентный передаче строки в `system_prompt`, который также может задавать `snapshot`. Требует `claude-agent-sdk` v0.2.153 или новее.

```python theme={null}
class SystemPromptCustom(TypedDict):
    type: Literal["custom"]
    prompt: str
    snapshot: NotRequired[bool]
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `type` | Да | Должно быть `"custom"` |
| `prompt` | Да | Текст системного промпта. Передаётся в CLI как аргумент командной строки, поэтому действуют [ограничения длины командной строки](#systempromptfile) |
| `snapshot` | Нет | То же, что [`SystemPromptPreset.snapshot`](#systempromptpreset), применительно к `prompt` |

### `SystemPromptFile`

Конфигурация для загрузки пользовательского системного промпта из файла вместо передачи его строкой. SDK сопоставляет это с флагом CLI [`--system-prompt-file`](https://code.claude.com/docs/ru/cli-reference#system-prompt-flags). Используйте форму с файлом, когда промпт большой: строковый `system_prompt` SDK передаёт в argv подпроцесса CLI, что подпадает под ограничения длины командной строки ОС ещё до того, как SDK отправит какой-либо запрос к API. В Linux отдельный аргумент длиннее примерно 128 КБ приводит к сбою при запуске процесса с ошибкой `Argument list too long`. В Windows вся командная строка ограничена примерно 32 КБ, поэтому строковая форма даёт сбой при ещё меньшем размере.

```python theme={null}
class SystemPromptFile(TypedDict):
    type: Literal["file"]
    path: str
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `type` | Да | Должно быть `"file"` для загрузки промпта с диска |
| `path` | Да | Путь к файлу, содержащему системный промпт |

### `SettingSource`

Определяет, из каких источников конфигурации в файловой системе SDK загружает настройки.

```python theme={null}
SettingSource = Literal["user", "project", "local"]
```

| Значение | Описание | Местоположение |
| :- | :- | :- |
| `"user"` | Глобальные пользовательские настройки | `~/.claude/settings.json` |
| `"project"` | Общие настройки проекта (под контролем версий) | `.claude/settings.json` |
| `"local"` | Локальные настройки проекта, добавляемые в gitignore, когда Claude Code сохраняет в них настройку | `.claude/settings.local.json` |

#### Поведение по умолчанию

Когда `setting_sources` опущен или равен `None` и `skills` не задан, `query()` загружает те же настройки файловой системы, что и CLI Claude Code: пользовательские, проектные и локальные. Если `skills` задан, текущее значение по умолчанию описано в строке [`setting_sources`](#claudeagentoptions). Политика, управляемая на конечном устройстве, загружается во всех случаях; настройки, управляемые сервером, извлекаются, когда сессия аутентифицируется с учётными данными организации в [подходящей конфигурации](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability). Дополнительную информацию см. в разделе [Что settingSources не контролирует](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#what-settingsources-does-not-control).

#### Зачем использовать setting\_sources

**Отключить настройки файловой системы:**

```python theme={null}
# Не загружать пользовательские, проектные или локальные настройки с диска
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Analyze this code",
        options=ClaudeAgentOptions(
            setting_sources=[]
        ),
    ):
        print(message)


asyncio.run(main())
```

> [!NOTE]
>
> В Python SDK 0.1.59 и более ранних версиях пустой список обрабатывался так же, как отсутствие опции, поэтому `setting_sources=[]` не отключал настройки файловой системы. Обновитесь до более новой версии, если вам нужно, чтобы пустой список вступал в силу. TypeScript SDK это не затрагивает.

**Загрузить только определённые источники настроек:**

```python theme={null}
# Загрузить только настройки проекта, игнорировать пользовательские и локальные
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Run CI checks",
        options=ClaudeAgentOptions(
            setting_sources=["project"]  # Только .claude/settings.json
        ),
    ):
        print(message)


asyncio.run(main())
```

**Приложения только на SDK:**

```python theme={null}
# Определить всё программно.
# Передайте [], чтобы отказаться от источников настроек файловой системы.
import asyncio
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, query


async def main():
    async for message in query(
        prompt="Review this PR",
        options=ClaudeAgentOptions(
            setting_sources=[],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Reviews code changes",
                    prompt="You are a code reviewer. Report issues in the diff.",
                ),
            },
            allowed_tools=["Read", "Grep", "Glob"],
        ),
    ):
        print(message)


asyncio.run(main())
```

Чтобы загрузить инструкции проекта из CLAUDE.md, включите `"project"` в `setting_sources`. О том, как загрузка CLAUDE.md взаимодействует с опциями системного промпта, см. [Изменение системных промптов](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#claude-md-files-for-project-level-instructions).

#### Приоритет настроек

Когда загружается несколько источников, настройки объединяются в следующем порядке приоритета (от наивысшего к наименьшему):

1. Локальные настройки (`.claude/settings.local.json`)
2. Настройки проекта (`.claude/settings.json`)
3. Пользовательские настройки (`~/.claude/settings.json`)

Программные опции, такие как `agents`, `allowed_tools` и `settings`, переопределяют пользовательские, проектные и локальные настройки файловой системы. Управляемые настройки политики имеют приоритет над программными опциями.

### `AgentDefinition`

Конфигурация для субагента, определённого программно.

```python theme={null}
@dataclass
class AgentDefinition:
    description: str
    prompt: str
    tools: list[str] | None = None
    disallowedTools: list[str] | None = None
    model: str | None = None
    skills: list[str] | None = None
    memory: Literal["user", "project", "local"] | None = None
    mcpServers: list[str | dict[str, Any]] | None = None
    initialPrompt: str | None = None
    maxTurns: int | None = None
    background: bool | None = None
    effort: EffortLevel | int | None = None
    permissionMode: PermissionMode | None = None
```

| Поле | Обязательно | Описание |
| :- | :- | :- |
| `description` | Да | Описание на естественном языке, когда использовать этого агента |
| `prompt` | Да | Системный промпт агента |
| `tools` | Нет | Массив имён разрешённых инструментов. Если опущено, наследуются все [инструменты, доступные субагентам](https://code.claude.com/docs/ru/sub-agents.md#available-tools) |
| `disallowedTools` | Нет | Массив имён инструментов, удаляемых из набора инструментов агента. Также принимаются шаблоны на уровне MCP-сервера: `mcp__server` или `mcp__server__*` удаляет все инструменты этого сервера, а `mcp__*` удаляет все инструменты MCP с любого сервера |
| `model` | Нет | Переопределение модели для этого агента. Принимает псевдоним, такой как `"sonnet"`, `"opus"`, `"haiku"` или `"inherit"`, или полный ID модели. Если опущено, Claude Code выбирает модель в соответствии с [порядком выбора модели для субагентов](https://code.claude.com/docs/ru/sub-agents.md#choose-a-model) |
| `skills` | Нет | Список имён скиллов для предварительной загрузки в контекст агента при запуске. Неуказанные скиллы по-прежнему можно вызвать через инструмент Skill |
| `memory` | Нет | Источник памяти для этого агента: `"user"`, `"project"` или `"local"` |
| `mcpServers` | Нет | MCP-серверы, доступные этому агенту. Каждая запись — это имя сервера или встроенный dict `{name: config}` |
| `initialPrompt` | Нет | Автоматически отправляется как первый ход пользователя, когда этот агент работает как агент основного потока |
| `maxTurns` | Нет | Максимальное количество агентских ходов до остановки агента |
| `background` | Нет | Запускать этого агента как неблокирующую фоновую задачу при вызове |
| `effort` | Нет | Уровень effort рассуждений для этого агента. Принимает именованный уровень или целое число. См. [`EffortLevel`](#effortlevel) |
| `permissionMode` | Нет | Режим разрешений для выполнения инструментов в этом агенте. Когда он применяется, определяют [правила наследования для субагентов](https://code.claude.com/docs/ru/agent-sdk/permissions.md#available-modes). См. [`PermissionMode`](#permissionmode) |

> [!NOTE]
>
> Имена полей `AgentDefinition` используют camelCase, например `disallowedTools`, `permissionMode` и `maxTurns`. Эти имена напрямую соответствуют формату передачи данных, общему с TypeScript SDK. Это отличается от `ClaudeAgentOptions`, где для эквивалентных полей верхнего уровня используется принятый в Python snake\_case, например `disallowed_tools` и `permission_mode`. Поскольку `AgentDefinition` является dataclass, передача ключевого аргумента в snake\_case вызывает `TypeError` при создании объекта.

### `PermissionMode`

Режимы разрешений для управления выполнением инструментов.

```python theme={null}
PermissionMode = Literal[
    "default",  # Стандартное поведение разрешений
    "acceptEdits",  # Автоматически принимать изменения файлов
    "plan",  # Режим планирования - Claude исследует и планирует
    "dontAsk",  # Отклонять всё, что не одобрено заранее, вместо запроса
    "bypassPermissions",  # Обходить проверки разрешений; явные правила ask всё равно запрашивают (используйте с осторожностью)
    "auto",  # Классификатор модели проверяет действия, такие как shell-команды и сетевые запросы
]
```

### `EffortLevel`

Уровни effort, определяющие глубину мышления.

```python theme={null}
EffortLevel = Literal[
    "low",  # Минимальное мышление, самые быстрые ответы
    "medium",  # Умеренное мышление
    "high",  # Глубокие рассуждения
    "xhigh",  # Расширенные рассуждения; на моделях без поддержки переключается на "high"
    "max",  # Максимальный effort
]
```

### `CanUseTool`

Псевдоним типа для функций обратного вызова разрешений инструментов.

```python theme={null}
CanUseTool = Callable[
    [str, dict[str, Any], ToolPermissionContext], Awaitable[PermissionResult]
]
```

Обратный вызов получает:

* `tool_name`: Имя вызываемого инструмента
* `input_data`: Входные параметры инструмента
* `context`: `ToolPermissionContext` с дополнительной информацией

Возвращает `PermissionResult` (либо `PermissionResultAllow`, либо `PermissionResultDeny`).

Обратный вызов заменяет интерактивный запрос разрешения. SDK вызывает `can_use_tool`, когда [процесс проверки разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated) приводит к запросу разрешения. Вызовы, одобренные любым из следующих способов, выполняются без вызова `can_use_tool`:

* Вызов, который одобряет запись в `allowed_tools` или правило разрешения в настройках
* Вызов, который одобряет режим разрешений, например изменение файла в режиме `acceptEdits`

Чтобы проверять такие вызовы, используйте [хук `PreToolUse`](https://code.claude.com/docs/ru/agent-sdk/hooks), который выполняется и для них.

Правило разрешения не одобряет заранее [действия, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves); о том, какие из них доходят до обратного вызова и что происходит в режимах `dontAsk` и `auto`, см. [Как проверяются разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated).

### `ToolPermissionContext`

Контекстная информация, передаваемая обратным вызовам разрешений инструментов.

```python theme={null}
@dataclass
class ToolPermissionContext:
    signal: Any | None = None  # Future: abort signal support
    suggestions: list[PermissionUpdate] = field(default_factory=list)
    tool_use_id: str | None = None
    agent_id: str | None = None
    blocked_path: str | None = None
    decision_reason: str | None = None
    title: str | None = None
    display_name: str | None = None
    description: str | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `signal` | `Any \| None` | Зарезервировано для будущей поддержки сигнала прерывания |
| `suggestions` | `list[PermissionUpdate]` | Предлагаемые CLI обновления разрешений. Запросы разрешения для Bash могут включать предложение с назначением `localSettings`, поэтому его возврат в `updated_permissions` записывает правило в `.claude/settings.local.json`, и оно сохраняется между сессиями. |
| `tool_use_id` | `str \| None` | Идентификатор конкретного вызова инструмента, к которому относится этот запрос. Всегда заполняется при передаче в `can_use_tool` |
| `agent_id` | `str \| None` | ID субагента, если вызов исходит от субагента; `None` для основного агента |
| `blocked_path` | `str \| None` | Путь к файлу, который вызвал запрос разрешения, если применимо. Например, когда команда Bash пытается обратиться к пути за пределами разрешённых каталогов |
| `decision_reason` | `str \| None` | Причина, по которой был вызван этот запрос разрешения. Передаётся из `permissionDecisionReason` хука PreToolUse, когда хук вернул `"ask"` |
| `title` | `str \| None` | Полное предложение запроса разрешения, например `Claude wants to read foo.txt`. Если присутствует, используйте как основной текст запроса |
| `display_name` | `str \| None` | Короткое именное словосочетание для действия инструмента, например `Read file`, подходящее для надписей на кнопках |
| `description` | `str \| None` | Понятный человеку подзаголовок для интерфейса разрешений |

### `PermissionResult`

Тип объединения для результатов обратного вызова разрешений.

```python theme={null}
PermissionResult = PermissionResultAllow | PermissionResultDeny
```

### `PermissionResultAllow`

Результат, указывающий, что вызов инструмента должен быть разрешён.

```python theme={null}
@dataclass
class PermissionResultAllow:
    behavior: Literal["allow"] = "allow"
    updated_input: dict[str, Any] | None = None
    updated_permissions: list[PermissionUpdate] | None = None
```

| Поле | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `behavior` | `Literal["allow"]` | `"allow"` | Должно быть "allow" |
| `updated_input` | `dict[str, Any] \| None` | `None` | Изменённые входные данные для использования вместо исходных |
| `updated_permissions` | `list[PermissionUpdate] \| None` | `None` | Применяемые обновления разрешений |

Если вы возвращаете `PermissionResultAllow` с более чем 4 096 элементами в `updated_permissions`, Claude Code считает результат недопустимым и отклоняет вызов инструмента. Каждый [`PermissionUpdate`](#permissionupdate) считается одним элементом, как и каждая запись в его списке `rules` или `directories`. Сообщение об отклонении заканчивается текстом `updatedPermissions may hold at most 4096 updates, rules and directories in all.` Чтобы избежать отклонения, возвращайте не более 4 096 элементов.

### `PermissionResultDeny`

Результат, указывающий, что вызов инструмента должен быть отклонён.

```python theme={null}
@dataclass
class PermissionResultDeny:
    behavior: Literal["deny"] = "deny"
    message: str = ""
    interrupt: bool = False
```

| Поле | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `behavior` | `Literal["deny"]` | `"deny"` | Должно быть "deny" |
| `message` | `str` | `""` | Сообщение, объясняющее, почему инструмент был отклонён |
| `interrupt` | `bool` | `False` | Следует ли прервать текущее выполнение |

### `PermissionUpdate`

Конфигурация для программного обновления разрешений.

```python theme={null}
@dataclass
class PermissionUpdate:
    type: Literal[
        "addRules",
        "replaceRules",
        "removeRules",
        "setMode",
        "addDirectories",
        "removeDirectories",
    ]
    rules: list[PermissionRuleValue] | None = None
    behavior: Literal["allow", "deny", "ask"] | None = None
    mode: PermissionMode | None = None
    directories: list[str] | None = None
    destination: (
        Literal["userSettings", "projectSettings", "localSettings", "session"] | None
    ) = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `type` | `Literal[...]` | Тип операции обновления разрешений |
| `rules` | `list[PermissionRuleValue] \| None` | Правила для операций добавления/замены/удаления |
| `behavior` | `Literal["allow", "deny", "ask"] \| None` | Поведение для операций на основе правил |
| `mode` | `PermissionMode \| None` | Режим для операции setMode |
| `directories` | `list[str] \| None` | Каталоги для операций добавления/удаления каталогов |
| `destination` | `Literal[...] \| None` | Где применить обновление разрешений |

### `PermissionRuleValue`

Правило для добавления, замены или удаления при обновлении разрешений.

```python theme={null}
@dataclass
class PermissionRuleValue:
    tool_name: str
    rule_content: str | None = None
```

### `ToolsPreset`

Предустановленная конфигурация инструментов для использования набора инструментов Claude Code по умолчанию.

```python theme={null}
class ToolsPreset(TypedDict):
    type: Literal["preset"]
    preset: Literal["claude_code"]
```

### `ThinkingConfig`

Управляет поведением расширенного мышления. Объединение трёх конфигураций:

```python theme={null}
ThinkingDisplay = Literal["summarized", "omitted"]


class ThinkingConfigAdaptive(TypedDict):
    type: Literal["adaptive"]
    display: NotRequired[ThinkingDisplay]


class ThinkingConfigEnabled(TypedDict):
    type: Literal["enabled"]
    budget_tokens: int
    display: NotRequired[ThinkingDisplay]


class ThinkingConfigDisabled(TypedDict):
    type: Literal["disabled"]


ThinkingConfig = ThinkingConfigAdaptive | ThinkingConfigEnabled | ThinkingConfigDisabled
```

| Вариант | Поля | Описание |
| :- | :- | :- |
| `adaptive` | `type`, `display` | Claude адаптивно решает, когда думать |
| `enabled` | `type`, `budget_tokens`, `display` | Включить мышление с определённым бюджетом токенов |
| `disabled` | `type` | Отключить мышление [там, где это позволяют модель и поставщик](https://code.claude.com/docs/ru/model-config.md#where-you-cant-turn-thinking-off) |

Необязательное поле `display` определяет, возвращается ли текст размышлений в виде `"summarized"` или `"omitted"`. В Claude Opus 4.7 и новее значение API по умолчанию — `"omitted"`, поэтому установите `"summarized"`, чтобы получать содержимое размышлений в выходных данных [`ThinkingBlock`](#thinkingblock). У таких поставщиков, как Amazon Bedrock и Google Cloud's Agent Platform, Claude Code не передаёт `display` для распознаваемых им более ранних моделей. Это Opus 4.6, Sonnet 4.6, Haiku 4.5 и более ранние модели, которые используют своё значение по умолчанию.

Поскольку это классы `TypedDict`, во время выполнения они являются простыми словарями. Можно либо создавать их как dict-литералы, либо вызывать класс как конструктор; в обоих случаях получается `dict`. Обращайтесь к полям через `config["budget_tokens"]`, а не `config.budget_tokens`:

```python theme={null}
from claude_agent_sdk import ClaudeAgentOptions, ThinkingConfigEnabled

# Вариант 1: dict-литерал (рекомендуется, импорт не требуется)
options = ClaudeAgentOptions(thinking={"type": "enabled", "budget_tokens": 20000})

# Вариант 2: в стиле конструктора (возвращает простой dict)
config = ThinkingConfigEnabled(type="enabled", budget_tokens=20000)
print(config["budget_tokens"])  # 20000
# config.budget_tokens вызовет AttributeError
```

### `TaskBudget`

Бюджет задачи на стороне API в токенах, используемый с полем `task_budget` в `ClaudeAgentOptions`.

```python theme={null}
class TaskBudget(TypedDict):
    total: int
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `total` | `int` | Общий бюджет токенов для задачи |

Поскольку это `TypedDict`, передавайте его как простой dict, например `ClaudeAgentOptions(task_budget={"total": 50000})`.

### `SdkBeta`

Литеральный тип для бета-функций SDK.

```python theme={null}
SdkBeta = Literal["context-1m-2025-08-07"]
```

Используйте с полем `betas` в `ClaudeAgentOptions` для включения бета-функций.

> [!WARNING]
>
> В Claude API бета-версия `context-1m-2025-08-07` выведена из эксплуатации для Claude Sonnet 4.5 и Claude Sonnet 4. Если вы всё ещё передаёте её с любой из этих моделей, запросы, превышающие стандартное контекстное окно в 200K токенов, возвращают ошибку, поэтому удалите её из `betas`. Чтобы запустить сессию с контекстным окном в 1M токенов, установите в `model` модель, которая [по умолчанию работает с окном в 1M](https://code.claude.com/docs/ru/model-config.md#extended-context), например `claude-sonnet-5-5` или `claude-opus-5-5`. Для модели, которая поддерживает 1M только через свой вариант `[1m]`, добавьте этот суффикс к ID модели, как в `claude-opus-4-6[1m]`.

### `McpSdkServerConfig`

Конфигурация для SDK MCP-серверов, созданных с помощью `create_sdk_mcp_server()`.

```python theme={null}
class McpSdkServerConfig(TypedDict):
    type: Literal["sdk"]
    name: str
    instance: Any  # MCP Server instance
```

### `McpServerConfig`

Тип объединения для конфигураций MCP-серверов.

```python theme={null}
McpServerConfig = (
    McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig
)
```

#### `McpStdioServerConfig`

```python theme={null}
class McpStdioServerConfig(TypedDict):
    type: NotRequired[Literal["stdio"]]  # Optional for backwards compatibility
    command: str
    args: NotRequired[list[str]]
    env: NotRequired[dict[str, str]]
```

#### `McpSSEServerConfig`

```python theme={null}
class McpSSEServerConfig(TypedDict):
    type: Literal["sse"]
    url: str
    headers: NotRequired[dict[str, str]]
```

#### `McpHttpServerConfig`

```python theme={null}
class McpHttpServerConfig(TypedDict):
    type: Literal["http"]
    url: str
    headers: NotRequired[dict[str, str]]
```

### `McpServerStatusConfig`

Конфигурация MCP-сервера в том виде, в котором её возвращает [`get_mcp_status()`](#methods). Это объединение всех транспортных вариантов [`McpServerConfig`](#mcpserverconfig) плюс доступный только в выходных данных вариант `claudeai-proxy` для серверов, проксируемых через claude.ai.

```python theme={null}
McpServerStatusConfig = (
    McpStdioServerConfig
    | McpSSEServerConfig
    | McpHttpServerConfig
    | McpSdkServerConfigStatus
    | McpClaudeAIProxyServerConfig
)
```

`McpSdkServerConfigStatus` — это сериализуемая форма [`McpSdkServerConfig`](#mcpsdkserverconfig), содержащая только поля `type` (`"sdk"`) и `name` (`str`); внутрипроцессный `instance` опущен. `McpClaudeAIProxyServerConfig` имеет поля `type` (`"claudeai-proxy"`), `url` (`str`) и `id` (`str`).

### `McpStatusResponse`

Ответ от [`ClaudeSDKClient.get_mcp_status()`](#methods). Содержит список статусов серверов под ключом `mcpServers`.

```python theme={null}
class McpStatusResponse(TypedDict):
    mcpServers: list[McpServerStatus]
```

### `McpServerStatus`

Статус подключённого MCP-сервера, содержащийся в [`McpStatusResponse`](#mcpstatusresponse).

```python theme={null}
class McpServerStatus(TypedDict):
    name: str
    status: McpServerConnectionStatus  # "connected" | "failed" | "needs-auth" | "pending" | "disabled"
    serverInfo: NotRequired[McpServerInfo]
    error: NotRequired[str]
    config: NotRequired[McpServerStatusConfig]
    scope: NotRequired[str]
    tools: NotRequired[list[McpToolInfo]]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | `str` | Имя сервера |
| `status` | `str` | Одно из значений `"connected"`, `"failed"`, `"needs-auth"`, `"pending"` или `"disabled"` |
| `serverInfo` | `dict` (необязательно) | Имя и версия сервера (`{"name": str, "version": str}`) |
| `error` | `str` (необязательно) | Сообщение об ошибке, если серверу не удалось подключиться |
| `config` | [`McpServerStatusConfig`](#mcpserverstatusconfig) (необязательно) | Конфигурация сервера. Та же структура, что и у [`McpServerConfig`](#mcpserverconfig) (stdio, SSE, HTTP или SDK), плюс вариант `claudeai-proxy` для серверов, подключённых через claude.ai |
| `scope` | `str` (необязательно) | Область действия конфигурации |
| `tools` | `list` (необязательно) | Инструменты, предоставляемые этим сервером, каждый с полями `name`, `description` и `annotations` |

### `ContextUsageResponse`

Ответ от [`ClaudeSDKClient.get_context_usage()`](#methods). Ответ включает данные, которые Claude Code отображает для команды `/context` в интерактивной сессии. Помимо количества токенов, эти данные содержат поля отображения, такие как `color` и `gridRows`, которые Claude Code использует для отрисовки сетки использования `/context`.

Claude Code формирует эти данные, отправляя несколько запросов к API [подсчёта токенов](https://platform.claude.com/docs/en/build-with-claude/token-counting). Эти запросы не отображаются в потоке сообщений, поэтому отслеживание стоимости, основанное на чтении потока, их не увидит. В Anthropic API подсчёт токенов не тарифицируется.

```python theme={null}
class ContextUsageResponse(TypedDict):
    categories: list[ContextUsageCategory]
    totalTokens: int
    maxTokens: int
    rawMaxTokens: int
    percentage: float
    model: str
    isAutoCompactEnabled: bool
    memoryFiles: list[dict[str, Any]]
    mcpTools: list[dict[str, Any]]
    agents: list[dict[str, Any]]
    gridRows: list[list[dict[str, Any]]]
    autoCompactThreshold: NotRequired[int]
    deferredBuiltinTools: NotRequired[list[dict[str, Any]]]
    systemTools: NotRequired[list[dict[str, Any]]]
    systemPromptSections: NotRequired[list[dict[str, Any]]]
    slashCommands: NotRequired[dict[str, Any]]
    skills: NotRequired[dict[str, Any]]  # skill usage with frontmatter breakdown
    messageBreakdown: NotRequired[dict[str, Any]]  # message tokens by type
    apiUsage: NotRequired[dict[str, Any] | None]
```

Каждая запись `ContextUsageCategory` содержит `name`, `tokens`, `color` и необязательный флаг `isDeferred`. `totalTokens` — это текущее использование контекста в сессии, а `maxTokens` — окно, относительно которого измеряется это использование. Этим окном является контекстное окно модели или меньшее окно автосжатия, если оно применяется, а `rawMaxTokens` содержит то же значение, что и `maxTokens`. `apiUsage` содержит данные об использовании из последнего ответа API, а не накопленный итог для сессии. Claude Code не заполняет необязательные ключи `deferredBuiltinTools`, `systemTools` и `systemPromptSections`, поэтому рассчитывайте на их отсутствие, даже несмотря на то, что тип их объявляет.

### `SdkPluginConfig`

Конфигурация для загрузки плагинов в SDK.

```python theme={null}
class SdkPluginConfig(TypedDict):
    type: Literal["local"]
    path: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `type` | `Literal["local"]` | Должно быть `"local"` (в настоящее время поддерживаются только локальные плагины) |
| `path` | `str` | Абсолютный или относительный путь к каталогу плагина |

**Пример:**

```python theme={null}
plugins = [
    {"type": "local", "path": "./my-plugin"},
    {"type": "local", "path": "/absolute/path/to/plugin"},
]
```

Полную информацию о создании и использовании плагинов см. в разделе [Плагины](https://code.claude.com/docs/ru/agent-sdk/plugins.md).

## Типы сообщений

### `Message`

Тип объединения всех возможных сообщений.

```python theme={null}
Message = (
    UserMessage
    | AssistantMessage
    | SystemMessage
    | ResultMessage
    | StreamEvent
    | RateLimitEvent
    | ConversationResetMessage
)
```

### `UserMessage`

Сообщение пользовательского ввода.

```python theme={null}
@dataclass
class UserMessage:
    content: str | list[ContentBlock]
    uuid: str | None = None
    parent_tool_use_id: str | None = None
    tool_use_result: dict[str, Any] | None = None
    origin: MessageOrigin | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `content` | `str \| list[ContentBlock]` | Содержимое сообщения как текст или блоки содержимого |
| `uuid` | `str \| None` | Уникальный идентификатор сообщения |
| `parent_tool_use_id` | `str \| None` | ID использования инструмента, если это сообщение является ответом результата инструмента |
| `tool_use_result` | `dict[str, Any] \| None` | Данные результата инструмента, если применимо |
| `origin` | `MessageOrigin \| None` | Происхождение этого сообщения, заполняется при внедренных ходах, таких как уведомления о задачах и сообщения от коллег. `None`, когда CLI не атрибутировал его. Требуется Python Agent SDK 0.2.137 или позже |

SDK передает `tool_use_result` из CLI без изменений. Для инструмента на внешнем MCP сервере, результат которого содержит блоки `resource_link`, словарь имеет ключ `resourceLinks`, содержащий список словарей с ключами типа TypeScript [`SDKMcpResourceLink`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkmcpresourcelink). Claude получает каждую ссылку как строку текста в результате инструмента. Для отображения файлов, возвращенных сервером, читайте `resourceLinks` вместо анализа этого текста. Ключ `resourceLinks` требует Python Agent SDK 0.2.150 или позже и Claude Code v2.1.257 или позже; CLI, поставляемый с этой версией SDK, удовлетворяет требованию Claude Code.

CLI опускает ключ, когда результат не содержит ссылок и при результатах от подагентов. CLI сохраняет максимум 50 ссылок на результат и прекращает добавление ссылок, когда список достигает 64 КиБ сериализованного JSON. Инструмент, который вы определяете внутри процесса с помощью [`tool()`](#tool), никогда не создает ключ, потому что SDK преобразует его блоки `resource_link` в текст перед тем, как CLI увидит результат.

### `AssistantMessage`

Сообщение ответа помощника с блоками содержимого.

```python theme={null}
@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str
    parent_tool_use_id: str | None = None
    error: AssistantMessageError | None = None
    usage: dict[str, Any] | None = None
    message_id: str | None = None
    stop_reason: str | None = None
    session_id: str | None = None
    uuid: str | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `content` | `list[ContentBlock]` | Список блоков содержимого в ответе |
| `model` | `str` | Модель, которая создала ответ |
| `parent_tool_use_id` | `str \| None` | ID использования инструмента, если это вложенный ответ |
| `error` | [`AssistantMessageError`](#assistantmessageerror) ` \| None` | Тип ошибки, если ответ столкнулся с ошибкой |
| `usage` | `dict[str, Any] \| None` | Использование токенов для каждого сообщения (те же ключи, что и [`ResultMessage.usage`](#resultmessage)) |
| `message_id` | `str \| None` | ID сообщения API. Несколько сообщений из одного хода имеют одинаковый ID |
| `stop_reason` | `str \| None` | Причина остановки из API (например `end_turn`, `tool_use`) |
| `session_id` | `str \| None` | ID сеанса, к которому принадлежит это сообщение |
| `uuid` | `str \| None` | Уникальный идентификатор сообщения в пределах транскрипта сеанса |

### `AssistantMessageError`

Возможные типы ошибок для сообщений помощника.

```python theme={null}
AssistantMessageError = Literal[
    "authentication_failed",
    "billing_error",
    "rate_limit",
    "invalid_request",
    "server_error",
    "unknown",
]
```

Базовый процесс CLI может выдавать типы ошибок, которые этот Literal не перечисляет, такие как `max_output_tokens`. SDK передает значение без изменений, поэтому обрабатывайте строки вне этого списка так же, как вы обрабатываете `unknown`. Тип TypeScript [`SDKAssistantMessageError`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkassistantmessage) перечисляет полный набор значений, которые может выдать CLI.

### `SystemMessage`

Системное сообщение с метаданными.

```python theme={null}
@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]
```

Подтипы, у которых нет собственного dataclass, поступают как `SystemMessage`. Чтобы отслеживать состояние сессии между ходами, установите [`CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS=1`](https://code.claude.com/docs/ru/env-vars#variables) и читайте `message.data["state"]` в каждом сообщении, у которого `subtype` равен `session_state_changed`. [`SDKSessionStateChangedMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdksessionstatechangedmessage) перечисляет состояния, которые оно может содержать. Чтобы читать их, выполняйте итерацию с помощью `receive_messages()`: `receive_response()` останавливается на `ResultMessage`, а сообщение `session_state_changed` может следовать после этого результата.

### `ResultMessage`

Финальное сообщение результата с информацией о стоимости и использовании.

```python theme={null}
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    stop_reason: str | None = None
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    structured_output: Any = None
    model_usage: dict[str, ModelUsage] | None = None
    permission_denials: list[Any] | None = None
    deferred_tool_use: DeferredToolUse | None = None
    errors: list[str] | None = None
    api_error_status: int | None = None
    uuid: str | None = None
    terminal_reason: str | None = None
    origin: MessageOrigin | None = None
```

Поле `subtype` определяет, какие другие поля заполнены. Это одно из `"success"`, `"error_during_execution"`, `"error_max_turns"`, `"error_max_budget_usd"` или `"error_max_structured_output_retries"`. Dataclass Python объединяет все варианты в одну форму, поэтому поля, которые не применяются к возвращаемому подтипу, имеют значение `None`.

Несколько полей содержат диагностические детали о том, как разговор закончился:

* `is_error`: `True`, когда диалог закончился в состоянии ошибки. Всегда `True` на подтипах `error_*`. На `subtype="success"` это `True` в трех случаях. Проверьте `stop_reason`, чтобы различить их:
  * `"refusal"`: модель отказалась отвечать. Прочитайте текст отказа в `result` или в предшествующем `AssistantMessage`, если `result` пуст.
  * `"tool_deferred_unavailable"`: [отложенный инструмент](https://code.claude.com/docs/ru/hooks.md#defer-a-tool-call-for-later) больше не был доступен, когда вы возобновили сессию, например потому что его MCP-сервер не был подключен. В двух случаях ниже промпт, который вы отправляете после возобновления, считается так же, как промпт, переданный вместе с возобновлением:
    * Без промпта: по умолчанию вызов всё ещё ожидает выполнения. Сделайте инструмент доступным и снова возобновите сессию без промпта, и вызов выполнится первым.
    * С промптом: по умолчанию промпт не доходит до Claude, и вызов всё ещё ожидает выполнения. Чтобы продолжить без инструмента, [отбросьте вызов](https://code.claude.com/docs/ru/hooks.md#resume-when-a-deferred-tool-is-unavailable).
  * Любое другое значение: ход завершился ошибкой, о которой Claude Code сообщил вместо ответа модели, например ошибкой API. Причину смотрите в `terminal_reason`, сообщение — в `result`, а HTTP-статус — в `api_error_status`, если API его вернул.
* `api_error_status`: код состояния HTTP завершающей ошибки API. `None`, когда ход закончился без ошибки. Заполняется только на `subtype="success"`.
* `result`: текст финального сообщения помощника на `subtype="success"` или `None` на подтипах `error_*`. Когда `subtype="success"` и `is_error=True`, это содержит строку ошибки API, если она доступна, но может быть пустой, поэтому проверьте `api_error_status` и предыдущее содержимое `AssistantMessage` для деталей.
* `errors`: строки ошибок уровня цикла, такие как сообщение о максимальных ходах. Заполняется только на подтипах `error_*`.
* `terminal_reason`: почему цикл запроса закончился, например `"completed"`, `"max_turns"`, `"api_error"`, `"aborted_streaming"` или `"aborted_tools"`. Значение `"aborted_streaming"` или `"aborted_tools"` означает, что ход был прерван до завершения. Частые причины - [`interrupt()`](#claudesdkclient) и callback разрешения, возвращающий [`PermissionResultDeny`](#permissionresultdeny) с `interrupt=True`. `None` на версиях CLI, которые предшествуют полю, на результатах локальных команд, таких как `/voice` или `/usage`, которые обходят цикл запроса, или на синтезированных результатах ошибок, выданных при критическом отказе сеанса. Зеркалирует [`SDKResultMessage.terminal_reason`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkresultmessage) TypeScript SDK, который перечисляет полный набор значений.
* `origin`: происхождение пользовательского сообщения, которое запустило этот ход. Требуется Python Agent SDK 0.2.137 или позже. Не подавляйте результат, опираясь только на `kind`. В [режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md) проверьте `origin`, чтобы узнать, запустил ли ход ваш собственный промпт:
  * **Ваш собственный промпт**: `origin` равен `None` или `{"kind": "human"}`
  * **Уведомление фоновой задачи**: `origin["kind"]` равен `"task-notification"`. Результат такого хода также может содержать ответ Claude на сообщение, которое вы отправили, пока ход выполнял инструменты.

Когда несколько фоновых задач завершаются почти одновременно, Claude Code может ответить на их уведомления за один ход, а не за отдельный ход на каждое. Вы всё равно получаете по одному `ResultMessage` на каждое уведомление, по порядку, и у каждого из них `origin` имеет `kind`, равный `"task-notification"`. У всех, кроме последнего, `num_turns` равен `0`, а `result` пуст, а последний содержит ход, который отвечает на все из них.

Словарь `usage` охватывает только основной цикл агента и исключает подагентов и другие вложенные или вспомогательные вызовы модели. В [режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md) значения указаны за ход. Предпочитайте `model_usage` для учета токенов и стоимости. Словарь `usage` содержит следующие ключи, если они присутствуют:

| Ключ | Тип | Описание |
| - | - | - |
| `input_tokens` | `int` | Входные токены, потребленные циклом агента верхнего уровня. [Токены подагента не включены](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#get-the-total-cost-of-a-query); используйте `model_usage` для учета всего дерева. |
| `output_tokens` | `int` | Выходные токены, созданные циклом агента верхнего уровня. Токены подагента не включены. |
| `cache_creation_input_tokens` | `int` | Токены, используемые для создания новых записей кэша. |
| `cache_read_input_tokens` | `int` | Токены, прочитанные из существующих записей кэша. |

Словарь `model_usage` отображает имена моделей на использование для каждой модели. Он охватывает каждый вызов модели, сделанный через конвейер запроса: основной цикл, подагентов и внутренние вызовы, такие как компактирование и агентов Workflow. Вспомогательные вызовы вне этого конвейера, такие как классификатор разрешений и запросы подсчета токенов, исключены из `model_usage`. Рассматривайте `model_usage` как оценку, а не как выписку по счету.

В [режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md) `model_usage` и `total_cost_usd` являются кумулятивными по ходам, поэтому читайте последний результат вместо суммирования по результатам. Вызов, который возобновляет сеанс, также учитывает [итоги, восстановленные из более ранних вызовов сеанса](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#accumulate-costs-across-multiple-calls). См. [Отслеживание затрат в режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#track-costs-in-streaming-input-mode) для сбросов и [Восстановление итогов после сбоя сеанса](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#recover-totals-after-a-session-crash) для обнуленных результатов.

Каждое значение в `model_usage` - это TypedDict `ModelUsage`, импортируемый через `from claude_agent_sdk.types import ModelUsage`. Его ключи используют camelCase, потому что SDK передает значение без изменений из базового процесса CLI, соответствуя типу TypeScript [`ModelUsage`](https://code.claude.com/docs/ru/agent-sdk/typescript#modelusage):

| Ключ | Тип | Описание |
| - | - | - |
| `inputTokens` | `int` | Входные токены для этой модели. |
| `outputTokens` | `int` | Выходные токены для этой модели. |
| `cacheReadInputTokens` | `int` | Токены чтения кэша для этой модели. |
| `cacheCreationInputTokens` | `int` | Токены создания кэша для этой модели. |
| `webSearchRequests` | `int` | Запросы веб-поиска, сделанные этой моделью. |
| `thinkingTokens` | `int` | Токены мышления, созданные этой моделью, уже подсчитанные в `outputTokens`. Отсутствуют до тех пор, пока ход не запустится на версии Claude Code, которая его записывает, и не объявлены в TypedDict, поэтому читайте его с `.get()`. Требуется Python Agent SDK 0.2.150 или позже, чей поставляемый CLI его записывает. |
| `costUSD` | `float` | Предполагаемая стоимость в USD для этой модели, вычисленная на стороне клиента. См. [Отслеживание затрат и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md) для предостережений выставления счетов. |
| `contextWindow` | `int` | Размер окна контекста для этой модели. |
| `maxOutputTokens` | `int` | Максимальный лимит выходных токенов для этой модели. |
| `canonicalModel` | `str` | Канонический ID модели, используемый для поиска цены. Может отличаться от необработанной строки модели, по которой индексируется запись, такой как ID или псевдоним, специфичный для поставщика. Не всегда присутствует. |
| `provider` | `str` | Поставщик API, который обслуживал эту модель, такой как `firstParty`, `bedrock`, `vertex`, `foundry`, `anthropicAws`, `mantle` или `gateway`. Не всегда присутствует. |
| `costBasis` | `str` | Таблица цен, по которой была рассчитана стоимость последнего запроса этой модели: `list` для прейскурантной цены, `managed` для таблицы [`modelPricing`](https://code.claude.com/docs/ru/settings-reference#modelpricing) или `unknown`, если ни одна из них не соответствует ID модели. Не всегда присутствует и не объявлено в TypedDict, поэтому читайте его с помощью `.get()`. Требуется Claude Code v2.1.246 или позже. |

### `StreamEvent`

Событие потока для частичных обновлений сообщений во время потоковой передачи. Получается только когда `include_partial_messages=True` в `ClaudeAgentOptions`. Импортируйте через `from claude_agent_sdk.types import StreamEvent`.

```python theme={null}
@dataclass
class StreamEvent:
    uuid: str
    session_id: str
    event: dict[str, Any]  # The raw Claude API stream event
    parent_tool_use_id: str | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `uuid` | `str` | Уникальный идентификатор для этого события |
| `session_id` | `str` | Идентификатор сеанса |
| `event` | `dict[str, Any]` | Необработанные данные события потока Claude API |
| `parent_tool_use_id` | `str \| None` | Всегда `None`. События потока выдаются только для основного сеанса. Для атрибуции подагента используйте полные сообщения, такие как [`AssistantMessage`](#assistantmessage) |

### `RateLimitEvent`

Выдается при изменении статуса ограничения скорости (например, с `"allowed"` на `"allowed_warning"`). Используйте это для предупреждения пользователей перед достижением жесткого лимита или для отката, когда статус `"rejected"`.

```python theme={null}
@dataclass
class RateLimitEvent:
    rate_limit_info: RateLimitInfo
    uuid: str
    session_id: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `rate_limit_info` | [`RateLimitInfo`](#ratelimitinfo) | Текущее состояние ограничения скорости |
| `uuid` | `str` | Уникальный идентификатор события |
| `session_id` | `str` | Идентификатор сеанса |

### `RateLimitInfo`

Состояние ограничения скорости, переносимое [`RateLimitEvent`](#ratelimitevent).

```python theme={null}
RateLimitStatus = Literal["allowed", "allowed_warning", "rejected"]
RateLimitType = Literal[
    "five_hour", "seven_day", "seven_day_opus", "seven_day_sonnet", "overage"
]


@dataclass
class RateLimitInfo:
    status: RateLimitStatus
    resets_at: int | None = None
    rate_limit_type: RateLimitType | None = None
    utilization: float | None = None
    overage_status: RateLimitStatus | None = None
    overage_resets_at: int | None = None
    overage_disabled_reason: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `status` | `RateLimitStatus` | Текущий статус, один из `"allowed"`, `"allowed_warning"` или `"rejected"`. `"allowed_warning"` означает приближение к лимиту; `"rejected"` означает, что лимит был достигнут |
| `resets_at` | `int \| None` | Временная метка Unix, когда окно ограничения скорости сбрасывается |
| `rate_limit_type` | `RateLimitType \| None` | Какое окно ограничения скорости применяется |
| `utilization` | `float \| None` | Доля потребленного ограничения скорости (0,0 до 1,0) |
| `overage_status` | `RateLimitStatus \| None` | Статус использования переплаты по мере использования, если применимо |
| `overage_resets_at` | `int \| None` | Временная метка Unix, когда окно переплаты сбрасывается |
| `overage_disabled_reason` | `str \| None` | Почему переплата недоступна, если статус `"rejected"` |
| `raw` | `dict[str, Any]` | Полный необработанный словарь из CLI, включая поля, не смоделированные выше |

### `ConversationResetMessage`

Выдается при замене разговора без завершения соединения, например после `/clear`. См. [Отслеживание затрат в режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#track-costs-in-streaming-input-mode) для того, как сброс влияет на текущие итоги на последующих объектах `ResultMessage`. Требуется Python Agent SDK 0.2.137 или позже.

```python theme={null}
@dataclass
class ConversationResetMessage:
    new_conversation_id: str
    uuid: str
    session_id: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `new_conversation_id` | `str` | Непрозрачный идентификатор для свежего разговора. Не `session_id` последующих сообщений; читайте это из следующего сообщения |
| `uuid` | `str` | Уникальный идентификатор сообщения |
| `session_id` | `str` | ID сеанса, который был сброшен. Сообщения после сброса содержат новый `session_id` |

### `TaskStartedMessage`

Выдается при запуске фоновой задачи. Фоновая задача - это все, что отслеживается вне основного хода: фоновая команда Bash, наблюдение [Monitor](#monitor), субагент, порожденный через инструмент Agent, или удаленный агент. Это именование не связано с переименованием инструмента `Task` на `Agent`.

```python theme={null}
@dataclass
class TaskStartedMessage(SystemMessage):
    task_id: str
    description: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    task_type: str | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `task_id` | `str` | Уникальный идентификатор для задачи |
| `description` | `str` | Описание задачи |
| `uuid` | `str` | Уникальный идентификатор сообщения |
| `session_id` | `str` | Идентификатор сеанса |
| `tool_use_id` | `str \| None` | Связанный ID использования инструмента |
| `task_type` | `str \| None` | Какой вид фоновой задачи: `"local_bash"` для фонового Bash и наблюдений Monitor, `"local_agent"` для субагентов, `"mcp_task"` для [фоновых вызовов инструментов MCP](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls) или `"remote_agent"` |

### `TaskUsage`

Данные токенов и времени для фоновой задачи.

```python theme={null}
class TaskUsage(TypedDict):
    total_tokens: int
    tool_uses: int
    duration_ms: int
```

### `TaskProgressMessage`

Выдается периодически с обновлениями прогресса для выполняющейся фоновой задачи.

```python theme={null}
@dataclass
class TaskProgressMessage(SystemMessage):
    task_id: str
    description: str
    usage: TaskUsage
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    last_tool_name: str | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `task_id` | `str` | Уникальный идентификатор для задачи |
| `description` | `str` | Описание текущего статуса |
| `usage` | `TaskUsage` | Использование токенов для этой задачи до сих пор |
| `uuid` | `str` | Уникальный идентификатор сообщения |
| `session_id` | `str` | Идентификатор сеанса |
| `tool_use_id` | `str \| None` | Связанный ID использования инструмента |
| `last_tool_name` | `str \| None` | Имя последнего инструмента, который использовала задача |

### `TaskNotificationMessage`

Выдается при завершении, сбое или остановке фоновой задачи. Фоновые задачи включают команды Bash `run_in_background`, наблюдения Monitor и фоновые подагенты.

```python theme={null}
@dataclass
class TaskNotificationMessage(SystemMessage):
    task_id: str
    status: TaskNotificationStatus  # "completed" | "failed" | "stopped"
    output_file: str
    summary: str
    uuid: str
    session_id: str
    tool_use_id: str | None = None
    usage: TaskUsage | None = None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `task_id` | `str` | Уникальный идентификатор для задачи |
| `status` | `TaskNotificationStatus` | Один из `"completed"`, `"failed"` или `"stopped"` |
| `output_file` | `str` | Путь к файлу вывода задачи |
| `summary` | `str` | Резюме результата задачи |
| `uuid` | `str` | Уникальный идентификатор сообщения |
| `session_id` | `str` | Идентификатор сеанса |
| `tool_use_id` | `str \| None` | Связанный ID использования инструмента |
| `usage` | `TaskUsage \| None` | Финальное использование токенов для задачи |

Когда CLI [перемещает длительный вызов инструмента MCP в фон](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls), результат инструмента для этого вызова содержит только заполнитель, и реальный результат вызова поступает в это сообщение. При уведомлении `"completed"` для такого вызова CLI добавляет ключ `resource_links`, перечисляющий файлы, возвращенные инструментом по ссылке, с теми же записями и ограничениями, что и ключ `resourceLinks` на [`UserMessage.tool_use_result`](#usermessage). Ключ `resource_links` требует Python Agent SDK 0.2.150 или позже и Claude Code v2.1.257 или позже; CLI, поставляемый с этой версией SDK, удовлетворяет требованию Claude Code.

Dataclass не имеет поля для `resource_links`. Читайте его из словаря `data`, который сообщение наследует от [`SystemMessage`](#systemmessage): `message.data.get("resource_links")`. Сопоставьте уведомление с вызовом, используя `tool_use_id`. CLI опускает ключ, когда результат не содержал ссылок и при уведомлениях для задач, которые не являются вызовами инструментов MCP.

## Типы блоков содержимого

### `ContentBlock`

Тип объединения всех блоков содержимого.

```python theme={null}
ContentBlock = (
    TextBlock
    | ThinkingBlock
    | ToolUseBlock
    | ToolResultBlock
    | ServerToolUseBlock
    | ServerToolResultBlock
)
```

### `TextBlock`

Блок содержимого текста.

```python theme={null}
@dataclass
class TextBlock:
    text: str
```

### `ThinkingBlock`

Блок содержимого мышления (для моделей с возможностью мышления).

```python theme={null}
@dataclass
class ThinkingBlock:
    thinking: str
    signature: str
```

### `ToolUseBlock`

Блок запроса использования инструмента.

```python theme={null}
@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]
```

### `ToolResultBlock`

Блок результата выполнения инструмента.

```python theme={null}
@dataclass
class ToolResultBlock:
    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
```

## Типы ошибок

Типы ниже определяют, что ваш код перехватывает. Для записей, привязанных к сообщениям об ошибках, которые эти типы вызывают, с причиной и исправлением для каждого, см. [Troubleshooting](https://code.claude.com/docs/ru/agent-sdk/troubleshooting.md).

### `ClaudeSDKError`

Базовый класс исключения для всех ошибок SDK.

```python theme={null}
class ClaudeSDKError(Exception):
    """Base error for Claude SDK."""
```

Когда одноразовый `query()` заканчивается результатом ошибки, например ошибкой превышения лимита ходов, SDK вызывает [`ResultError`](#resulterror).

### `CLINotFoundError`

Вызывается, когда Claude Code CLI не установлен или не найден.

```python theme={null}
class CLINotFoundError(CLIConnectionError):
    def __init__(
        self, message: str = "Claude Code not found", cli_path: str | None = None
    ):
        """
        Args:
            message: Error message (default: "Claude Code not found")
            cli_path: Optional path to the CLI that was not found
        """
```

### `CLIConnectionError`

Вызывается, когда соединение с Claude Code не удается.

```python theme={null}
class CLIConnectionError(ClaudeSDKError):
    """Failed to connect to Claude Code."""
```

### `ProcessError`

Вызывается, когда процесс Claude Code не работает.

```python theme={null}
class ProcessError(ClaudeSDKError):
    def __init__(
        self, message: str, exit_code: int | None = None, stderr: str | None = None
    ):
        self.exit_code = exit_code
        self.stderr = stderr
```

### `ResultError`

Вызывается, когда процесс Claude Code завершается, потому что запуск закончился [сообщением результата](#resultmessage) с ошибкой, таким как ошибка превышения лимита ходов или ошибка API. `ResultError` является подклассом `ProcessError`, поэтому существующий обработчик `except ProcessError` также его перехватывает. Его атрибуты содержат поля этого сообщения результата, поэтому вы можете разветвляться в зависимости от причины сбоя запуска без анализа текста сообщения. Требуется Python Agent SDK версии 0.2.140 или позже.

```python theme={null}
class ResultError(ProcessError):
    subtype: str | None  # "error_max_turns", "error_during_execution", ...; "success" when the run ended on a failed request
    errors: list[str]  # an empty list when the result message reported none
    result: str | None
    api_error_status: int | None
    terminal_reason: str | None  # "max_turns", "api_error", ...; check after data["stop_reason"], before subtype
    session_id: str | None
    data: dict[str, Any]  # the raw result message payload
```

Чтобы различить сбои, сначала проверьте `data["stop_reason"]`, затем `terminal_reason`, затем `subtype`. Отклоненный ответ имеет `stop_reason` `"refusal"`, обычно с `subtype` `"success"`; его `terminal_reason` не выделяет его и может иметь значение `"completed"` или `"api_error"`. Неудавшийся финальный запрос имеет `subtype` `"success"` и причину в `terminal_reason`, например `"api_error"` для ошибки API. Когда запуск достигает установленного вами лимита, такого как `max_turns` или `max_budget_usd`, вы получаете подтип `error_*`.

### `CLIJSONDecodeError`

Вызывается, когда разбор JSON не удается или когда одно сообщение от CLI длиннее `max_buffer_size`. Чтобы увеличить лимит и продолжить остановленную работу, см. [Большие вызовы инструментов и результаты](https://code.claude.com/docs/ru/agent-sdk/troubleshooting.md#large-tool-calls-and-results).

```python theme={null}
class CLIJSONDecodeError(ClaudeSDKError):
    def __init__(self, line: str, original_error: Exception):
        """
        Args:
            line: The line that failed to parse
            original_error: The original JSON decode exception
        """
        self.line = line
        self.original_error = original_error
```

## Типы hooks

Для полного руководства по использованию hooks с примерами и общими шаблонами см. [Hooks guide](https://code.claude.com/docs/ru/agent-sdk/hooks.md).

### `HookEvent`

Поддерживаемые типы событий hooks.

```python theme={null}
HookEvent = Literal[
    "PreToolUse",  # Called before tool execution
    "PostToolUse",  # Called after tool execution
    "PostToolUseFailure",  # Called when a tool execution fails
    "UserPromptSubmit",  # Called when a prompt is submitted
    "Stop",  # Called when stopping execution
    "SubagentStop",  # Called when a subagent stops
    "PreCompact",  # Called before message compaction
    "Notification",  # Called for notification events
    "SubagentStart",  # Called when a subagent starts
    "PermissionRequest",  # Called when a permission decision is needed
]
```

> [!NOTE]
>
> TypeScript SDK поддерживает дополнительные события hooks, которые еще недоступны в Python. См. [таблицу доступности hooks](https://code.claude.com/docs/ru/agent-sdk/hooks.md#available-hooks) для поддержки по SDK.

### `HookCallback`

Определение типа для функций обратного вызова hooks.

```python theme={null}
HookCallback = Callable[[HookInput, str | None, HookContext], Awaitable[HookJSONOutput]]
```

Параметры:

* `input`: Строго типизированные входные данные хука с дискриминированными объединениями на основе `hook_event_name` (см. [`HookInput`](#hookinput))
* `tool_use_id`: Дополнительный идентификатор использования инструмента (для hooks, связанных с инструментами)
* `context`: Контекст hooks с дополнительной информацией

Возвращает [`HookJSONOutput`](#hookjsonoutput).

### `HookContext`

Информация контекста, передаваемая в обратные вызовы hooks.

```python theme={null}
class HookContext(TypedDict):
    signal: Any | None  # Future: abort signal support
```

### `HookMatcher`

Конфигурация для сопоставления hooks с определенными событиями или инструментами.

```python theme={null}
@dataclass
class HookMatcher:
    matcher: str | None = (
        None  # Tool name or pattern to match (e.g., "Bash", "Write|Edit")
    )
    hooks: list[HookCallback] = field(
        default_factory=list
    )  # List of callbacks to execute
    timeout: float | None = (
        None  # Timeout in seconds. When omitted, the per-event default applies:
        # 600 for most events, 30 for UserPromptSubmit
    )
    on_failure: Literal["continue", "block"] | None = (
        None  # "block" blocks the action when a callback fails
    )
```

Чтобы решить, на что должен распространяться `on_failure`, см. [Блокировка действия при сбое обратного вызова](https://code.claude.com/docs/ru/agent-sdk/hooks.md#block-the-action-when-a-callback-fails).

### `HookInput`

Тип объединения всех типов ввода hooks. Фактический тип зависит от поля `hook_event_name`.

```python theme={null}
HookInput = (
    PreToolUseHookInput
    | PostToolUseHookInput
    | PostToolUseFailureHookInput
    | UserPromptSubmitHookInput
    | StopHookInput
    | SubagentStopHookInput
    | PreCompactHookInput
    | NotificationHookInput
    | SubagentStartHookInput
    | PermissionRequestHookInput
)
```

### `BaseHookInput`

Базовые поля, присутствующие во всех типах ввода hooks.

```python theme={null}
class BaseHookInput(TypedDict):
    session_id: str
    transcript_path: str
    cwd: str
    permission_mode: NotRequired[str]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `session_id` | `str` | Текущий идентификатор сеанса |
| `transcript_path` | `str` | Путь к файлу стенограммы сеанса |
| `cwd` | `str` | Текущий рабочий каталог |
| `permission_mode` | `str` (опционально) | Текущий режим разрешений |

### `PreToolUseHookInput`

Входные данные для событий hooks `PreToolUse`.

```python theme={null}
class PreToolUseHookInput(BaseHookInput):
    hook_event_name: Literal["PreToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["PreToolUse"]` | Всегда "PreToolUse" |
| `tool_name` | `str` | Имя инструмента, который вот-вот будет выполнен |
| `tool_input` | `dict[str, Any]` | Входные параметры для инструмента |
| `tool_use_id` | `str` | Уникальный идентификатор для этого использования инструмента |
| `agent_id` | `str` (опционально) | Идентификатор подагента, присутствует, когда hooks срабатывает внутри подагента |
| `agent_type` | `str` (опционально) | Тип подагента, присутствует, когда hooks срабатывает внутри подагента |

### `PostToolUseHookInput`

Входные данные для событий hooks `PostToolUse`.

```python theme={null}
class PostToolUseHookInput(BaseHookInput):
    hook_event_name: Literal["PostToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_response: Any
    tool_use_id: str
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["PostToolUse"]` | Всегда "PostToolUse" |
| `tool_name` | `str` | Имя выполненного инструмента |
| `tool_input` | `dict[str, Any]` | Использованные входные параметры |
| `tool_response` | `Any` | Ответ от выполнения инструмента |
| `tool_use_id` | `str` | Уникальный идентификатор для этого использования инструмента |
| `agent_id` | `str` (опционально) | Идентификатор подагента, присутствует, когда hooks срабатывает внутри подагента |
| `agent_type` | `str` (опционально) | Тип подагента, присутствует, когда hooks срабатывает внутри подагента |

### `PostToolUseFailureHookInput`

Входные данные для событий hooks `PostToolUseFailure`. Вызывается, когда выполнение инструмента не удается.

```python theme={null}
class PostToolUseFailureHookInput(BaseHookInput):
    hook_event_name: Literal["PostToolUseFailure"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    error: str
    is_interrupt: NotRequired[bool]
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["PostToolUseFailure"]` | Всегда "PostToolUseFailure" |
| `tool_name` | `str` | Имя инструмента, который не удался |
| `tool_input` | `dict[str, Any]` | Использованные входные параметры |
| `tool_use_id` | `str` | Уникальный идентификатор для этого использования инструмента |
| `error` | `str` | Сообщение об ошибке из неудачного выполнения |
| `is_interrupt` | `bool` (опционально) | True, когда ошибка достигла Claude Code как прерывание, а не как ошибка, которую сообщил инструмент. Отмена выполняющегося инструмента с помощью `interrupt()` не срабатывает этот hooks; результат инструмента содержит сообщение о прерывании вместо этого |
| `agent_id` | `str` (опционально) | Идентификатор подагента, присутствует, когда hooks срабатывает внутри подагента |
| `agent_type` | `str` (опционально) | Тип подагента, присутствует, когда hooks срабатывает внутри подагента |

### `UserPromptSubmitHookInput`

Входные данные для событий hooks `UserPromptSubmit`.

```python theme={null}
class UserPromptSubmitHookInput(BaseHookInput):
    hook_event_name: Literal["UserPromptSubmit"]
    prompt: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["UserPromptSubmit"]` | Всегда "UserPromptSubmit" |
| `prompt` | `str` | Отправленный промпт |

### `StopHookInput`

Входные данные для событий hooks `Stop`.

```python theme={null}
class StopHookInput(BaseHookInput):
    hook_event_name: Literal["Stop"]
    stop_hook_active: bool
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["Stop"]` | Всегда "Stop" |
| `stop_hook_active` | `bool` | Активен ли hooks остановки |

### `SubagentStopHookInput`

Входные данные для событий hooks `SubagentStop`.

```python theme={null}
class SubagentStopHookInput(BaseHookInput):
    hook_event_name: Literal["SubagentStop"]
    stop_hook_active: bool
    agent_id: str
    agent_transcript_path: str
    agent_type: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["SubagentStop"]` | Всегда "SubagentStop" |
| `stop_hook_active` | `bool` | Активен ли hooks остановки |
| `agent_id` | `str` | Уникальный идентификатор подагента |
| `agent_transcript_path` | `str` | Путь к файлу стенограммы подагента |
| `agent_type` | `str` | Тип подагента |

### `PreCompactHookInput`

Входные данные для событий hooks `PreCompact`.

```python theme={null}
class PreCompactHookInput(BaseHookInput):
    hook_event_name: Literal["PreCompact"]
    trigger: Literal["manual", "auto"]
    custom_instructions: str | None
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["PreCompact"]` | Всегда "PreCompact" |
| `trigger` | `Literal["manual", "auto"]` | Что вызвало уплотнение |
| `custom_instructions` | `str \| None` | Пользовательские инструкции для уплотнения |

### `NotificationHookInput`

Входные данные для событий hooks `Notification`.

```python theme={null}
class NotificationHookInput(BaseHookInput):
    hook_event_name: Literal["Notification"]
    message: str
    title: NotRequired[str]
    notification_type: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["Notification"]` | Всегда "Notification" |
| `message` | `str` | Содержимое сообщения уведомления |
| `title` | `str` (опционально) | Название уведомления |
| `notification_type` | `str` | Тип уведомления |

### `SubagentStartHookInput`

Входные данные для событий hooks `SubagentStart`.

```python theme={null}
class SubagentStartHookInput(BaseHookInput):
    hook_event_name: Literal["SubagentStart"]
    agent_id: str
    agent_type: str
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["SubagentStart"]` | Всегда "SubagentStart" |
| `agent_id` | `str` | Уникальный идентификатор подагента |
| `agent_type` | `str` | Тип подагента |

### `PermissionRequestHookInput`

Входные данные для событий hooks `PermissionRequest`. Позволяет hooks программно обрабатывать решения разрешений.

```python theme={null}
class PermissionRequestHookInput(BaseHookInput):
    hook_event_name: Literal["PermissionRequest"]
    tool_name: str
    tool_input: dict[str, Any]
    permission_suggestions: NotRequired[list[Any]]
    agent_id: NotRequired[str]
    agent_type: NotRequired[str]
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `hook_event_name` | `Literal["PermissionRequest"]` | Всегда "PermissionRequest" |
| `tool_name` | `str` | Имя инструмента, запрашивающего разрешение |
| `tool_input` | `dict[str, Any]` | Входные параметры для инструмента |
| `permission_suggestions` | `list[Any]` (опционально) | Предложенные обновления разрешений из CLI |
| `agent_id` | `str` (опционально) | Идентификатор подагента, присутствует, когда hooks срабатывает внутри подагента |
| `agent_type` | `str` (опционально) | Тип подагента, присутствует, когда hooks срабатывает внутри подагента |

### `HookJSONOutput`

Тип объединения для возвращаемых значений обратного вызова hooks.

```python theme={null}
HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput
```

#### `SyncHookJSONOutput`

Синхронный вывод hooks с полями управления и решения.

```python theme={null}
class SyncHookJSONOutput(TypedDict):
    # Control fields
    continue_: NotRequired[bool]  # Whether to proceed (default: True)
    suppressOutput: NotRequired[bool]  # Has no effect
    stopReason: NotRequired[str]  # Message when continue is False

    # Decision fields
    decision: NotRequired[Literal["block"]]
    systemMessage: NotRequired[str]  # Warning message for user
    reason: NotRequired[str]  # Feedback for Claude

    # Hook-specific output
    hookSpecificOutput: NotRequired[HookSpecificOutput]
```

> [!NOTE]
>
> Используйте `continue_` (с подчеркиванием) в коде Python. Он автоматически преобразуется в `continue` при отправке в CLI.

#### `HookSpecificOutput`

Дискриминированное объединение типов вывода `TypedDict`, специфичных для событий. Поле `hookEventName` определяет, какие поля допустимы. Полные сведения о доступных полях для каждого события хука см. в разделе [Управление выполнением с помощью хуков](https://code.claude.com/docs/ru/agent-sdk/hooks.md#outputs).

```python theme={null}
class PreToolUseHookSpecificOutput(TypedDict):
    hookEventName: Literal["PreToolUse"]
    permissionDecision: NotRequired[Literal["allow", "deny", "ask", "defer"]]
    permissionDecisionReason: NotRequired[str]
    updatedInput: NotRequired[dict[str, Any]]
    additionalContext: NotRequired[str]


class PostToolUseHookSpecificOutput(TypedDict):
    hookEventName: Literal["PostToolUse"]
    additionalContext: NotRequired[str]
    updatedToolOutput: NotRequired[Any]
    updatedMCPToolOutput: NotRequired[Any]  # MCP tools only. Prefer updatedToolOutput, which works for all tools


class PostToolUseFailureHookSpecificOutput(TypedDict):
    hookEventName: Literal["PostToolUseFailure"]
    additionalContext: NotRequired[str]


class UserPromptSubmitHookSpecificOutput(TypedDict):
    hookEventName: Literal["UserPromptSubmit"]
    additionalContext: NotRequired[str]


class NotificationHookSpecificOutput(TypedDict):
    hookEventName: Literal["Notification"]
    additionalContext: NotRequired[str]


class SubagentStartHookSpecificOutput(TypedDict):
    hookEventName: Literal["SubagentStart"]
    additionalContext: NotRequired[str]


class PermissionRequestHookSpecificOutput(TypedDict):
    hookEventName: Literal["PermissionRequest"]
    decision: dict[str, Any]


HookSpecificOutput = (
    PreToolUseHookSpecificOutput
    | PostToolUseHookSpecificOutput
    | PostToolUseFailureHookSpecificOutput
    | UserPromptSubmitHookSpecificOutput
    | NotificationHookSpecificOutput
    | SubagentStartHookSpecificOutput
    | PermissionRequestHookSpecificOutput
)
```

#### `AsyncHookJSONOutput`

Асинхронный вывод hooks, который откладывает выполнение hooks.

```python theme={null}
class AsyncHookJSONOutput(TypedDict):
    async_: Literal[True]  # Set to True to defer execution
    asyncTimeout: NotRequired[int]  # Timeout in milliseconds
```

> [!NOTE]
>
> Используйте `async_` (с подчеркиванием) в коде Python. Он автоматически преобразуется в `async` при отправке в CLI.

### Пример использования hooks

Этот пример регистрирует два хука: один блокирует опасные команды Bash, такие как `rm -rf /`, а другой записывает в лог всё использование инструментов для аудита. Благодаря [matcher `Bash`](https://code.claude.com/docs/ru/agent-sdk/hooks#matchers) хук безопасности выполняется при вызовах инструмента Bash. У хука логирования нет matcher, поэтому он срабатывает для каждого инструмента.

```python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, HookContext
from typing import Any


async def validate_bash_command(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Validate and potentially block dangerous bash commands."""
    if input_data["tool_name"] == "Bash":
        command = input_data["tool_input"].get("command", "")
        if "rm -rf /" in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Dangerous command blocked",
                }
            }
    return {}


async def log_tool_use(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
) -> dict[str, Any]:
    """Log all tool usage for auditing."""
    print(f"Tool used: {input_data.get('tool_name')}")
    return {}


options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="Bash", hooks=[validate_bash_command], timeout=120
            ),  # 2 min for validation
            HookMatcher(
                hooks=[log_tool_use]
            ),  # Applies to all tools (per-event default timeout)
        ],
        "PostToolUse": [HookMatcher(hooks=[log_tool_use])],
    }
)

async def main():
    async for message in query(prompt="Analyze this codebase", options=options):
        print(message)


asyncio.run(main())
```

## Типы ввода/вывода инструментов

Документация схем ввода/вывода для встроенных инструментов Claude Code. Хотя Python SDK не экспортирует их как типы, они представляют структуру входов и выходов инструментов в сообщениях.

Каждый показанный вывод — это значение, которое вы читаете из [`UserMessage.tool_use_result`](#usermessage) для этого инструмента. Названия ключей появляются точно так, как их выдает Claude Code. Ключ, аннотированный `| None` с комментарием "present when" или "optional", опускается, когда он не применяется.

### Agent

**Имя инструмента:** `Agent`. Предыдущее имя `Task` по-прежнему принимается как псевдоним, когда этот инструмент доступен в сессии.

Список `tools` в инициализации [`SystemMessage`](#systemmessage) сообщает об этом инструменте как `Task` для обратной совместимости.

**Ввод:**

```python theme={null}
{
    "description": str,  # Краткое описание задачи (3-5 слов)
    "prompt": str,  # Задача для выполнения агентом
    "subagent_type": str | None,  # Тип специализированного агента для использования
    "model": "sonnet" | "opus" | "haiku" | "fable" | None,  # Переопределение модели для этого агента
    "effort": "low" | "medium" | "high" | "xhigh" | "max" | None,  # Уровень усилий рассуждения для этого агента
    "run_in_background": bool | None,  # По умолчанию, если не указано: вызов из вашего основного агента запускает нового агента в фоне, а вызов из субагента ожидает его
    "name": str | None,  # Имя для порожденного агента
    "team_name": str | None,  # Устарело; игнорируется
    "mode": "acceptEdits" | "auto" | "bypassPermissions" | "default" | "dontAsk" | "plan" | None,  # Устарело; игнорируется. Правила наследования субагента определяют режим разрешений субагента
    "isolation": "worktree" | "remote" | None,  # Режим изоляции для изменений агента
}
```

Запускает нового агента для автономной обработки сложных многошаговых задач.

Когда Claude не указывает `run_in_background` в вызове `Agent`, по умолчанию ваш основной агент не ждет нового агента, а субагент ждет:

* **Из вашего основного агента**: новый агент выполняется в фоне, и результат имеет `status: "async_launched"`. Чтобы вместо этого ваш основной агент ждал нового агента, см. [Выбор того, ждет ли Claude субагентов](https://code.claude.com/docs/ru/agent-sdk/subagents.md#choose-whether-claude-waits-for-subagents).
* **Из одного из ваших субагентов**: вызывающий субагент [ждет нового агента](https://code.claude.com/docs/ru/sub-agents.md#let-subagents-spawn-their-own-subagents). Вместо этого новый агент выполняется в фоне, если в его определении [`background`](#agentdefinition) установлено в `True` или если вы [отключаете режим fork](https://code.claude.com/docs/ru/sub-agents.md#turn-fork-mode-on-or-off), установив `CLAUDE_CODE_FORK_SUBAGENT` в `0`.

До Python SDK v0.2.169 агенты, запущенные вашими субагентами, также по умолчанию выполнялись в фоне. Этот выпуск — первый, который поставляется с Claude Code v2.1.302 или позже.

**Вывод (статус: `"completed"`):**

```python theme={null}
{
    "status": "completed",
    "agentId": str,  # ID агента, который был запущен
    "agentType": str | None,  # Тип субагента, который обработал задачу
    "content": [  # Блоки содержимого результата
        {
            "type": "text",
            "text": str,
            "citations": list | None,
        }
    ],
    "resolvedModel": str | None,  # Модель, на которой запустился субагент
    "modelsUsed": list[str] | None,  # Модели, использованные по порядку, с коллапсированными последовательными повторениями
    "totalToolUseCount": int,  # Количество вызовов инструментов, которые сделал агент
    "totalDurationMs": int,  # Длительность выполнения в миллисекундах
    "totalTokens": int,  # Количество токенов из финального запроса API, не из всего запуска
    "usage": {  # Статистика использования токенов
        "input_tokens": int,
        "output_tokens": int,
        "cache_creation_input_tokens": int | None,
        "cache_read_input_tokens": int | None,
        "server_tool_use": {"web_search_requests": int, "web_fetch_requests": int} | None,
        "service_tier": str | None,
        "cache_creation": {"ephemeral_1h_input_tokens": int, "ephemeral_5m_input_tokens": int} | None,
        "inference_geo": str | None,
        "speed": str | None,
        "iterations": Any | None,
        "output_tokens_details": {"thinking_tokens": int | None} | None,
        "fallback_credit": Any | None,
    },
    "toolStats": {  # Совокупная активность инструментов для запуска
        "readCount": int,
        "searchCount": int,
        "bashCount": int,
        "editFileCount": int,
        "linesAdded": int,
        "linesRemoved": int,
        "otherToolCount": int,
        "frameCount": int | None,
    } | None,
    "prompt": str,  # Промпт, который запустил агент
    "worktreePath": str | None,  # Присутствует, когда Claude Code сохранил worktree субагента
    "worktreeBranch": str | None,  # Присутствует, когда Claude Code создал этот worktree с git
}
```

**Вывод (статус: `"async_launched"`):**

```python theme={null}
{
    "status": "async_launched",
    "isAsync": bool | None,  # True при фоновых запусках
    "agentId": str,  # ID запущенного агента
    "description": str,  # Описание задачи
    "resolvedModel": str | None,  # Модель, используемая при переходе в фоновый режим
    "modelsUsed": list[str] | None,  # Модели, использованные перед фоновым режимом, по порядку, с коллапсированными последовательными повторениями
    "prompt": str,  # Промпт, который запускает агент
    "outputFile": str,  # Путь файла, где записывается вывод агента
    "canReadOutputFile": bool | None,  # Может ли выходной файл быть прочитан напрямую
}
```

**Вывод (статус: `"remote_launched"`):**

```python theme={null}
{
    "status": "remote_launched",
    "taskId": str,  # ID отправленной задачи
    "sessionUrl": str,  # Ссылка на облачную сессию
    "description": str,  # Описание задачи
    "prompt": str,  # Промпт, который запускает агент
    "outputFile": str,  # Путь файла, где записывается вывод агента
}
```

Возвращает результат от субагента. Вывод различается по полю `status`: `"completed"` для завершенных задач, `"async_launched"` для фоновых задач и `"remote_launched"` для задач, которые Claude Code отправил в облачную сессию, где `sessionUrl` ссылается на эту сессию и `taskId` ее идентифицирует. Если Claude Code [сохранил изолированный worktree субагента](https://code.claude.com/docs/ru/worktrees.md#isolate-subagents-with-worktrees), `worktreePath` в варианте `completed` — это место, где его найти, и `worktreeBranch` — это его ветка, когда Claude Code создал worktree с git.

В варианте `completed`, `resolvedModel` называет модель, на которой запустился субагент, которая может отличаться от запрошенного входа `model`, когда применяется [`availableModels`](https://code.claude.com/docs/ru/model-config#restrict-model-selection) или другое переопределение. Это поле требует Claude Code v2.1.174 или позже. В варианте `async_launched`, `resolvedModel` называет модель, используемую, когда агент перешел в фоновый режим, поэтому обмен, произошедший перед фоновым режимом, отражается там. Поле `modelsUsed` в обоих вариантах перечисляет использованные модели по порядку, с коллапсированными последовательными повторениями; оно устанавливается только при обмене модели во время выполнения. `modelsUsed` и поведение `resolvedModel` во время фонового режима требуют Claude Code v2.1.212 или позже.

Claude Code заполняет `usage` и `totalTokens` из финального запроса API субагента, не из всего запуска. Когда присутствует, `thinking_tokens` под `output_tokens_details` в `usage` — это количество выходных токенов этого запроса, которые были токенами мышления. Ключ `output_tokens_details` требует Python SDK v0.2.136 или позже, который поставляется с Claude Code v2.1.228. Ключ `fallback_credit` требует Python SDK v0.2.162 или позже, который поставляется с Claude Code v2.1.285.

### AskUserQuestion

**Имя инструмента:** `AskUserQuestion`

Задает пользователю уточняющие вопросы во время выполнения. См. [Обработка подтверждений и ввода пользователя](https://code.claude.com/docs/ru/agent-sdk/user-input.md#handle-clarifying-questions) для деталей использования.

**Ввод:**

```python theme={null}
{
    "questions": [  # Вопросы для пользователя (1-4 вопроса)
        {
            "question": str,  # Полный вопрос для пользователя
            "header": str,  # Очень короткая метка, отображаемая как чип/тег (макс 12 символов)
            "options": [  # Доступные варианты (2-4 варианта)
                {
                    "label": str,  # Текст отображения для этого варианта (1-5 слов)
                    "description": str,  # Объяснение того, что означает этот вариант
                    "preview": str | None,  # Содержимое предпросмотра, отображаемое при фокусировке на варианте
                }
            ],
            "multiSelect": bool,  # Установите значение true, чтобы разрешить множественный выбор
        }
    ],
    "answers": dict[str, str] | None,
    # Ответы пользователя, заполненные системой разрешений. Ответы с множественным выбором
    # — это строка, объединенная запятыми из выбранных меток; список меток принимается
    # на входе и приводится к этой форме
    "annotations": dict[str, dict] | None,
    # Аннотации для каждого вопроса от пользователя, ключ — текст вопроса.
    # Каждое значение может содержать "preview" (содержимое предпросмотра выбранного варианта)
    # и "notes" (свободные заметки по выбору)
    "metadata": dict | None,  # Метаданные аналитики, такие как {"source": "remember"}; не отображается пользователю
}
```

**Вывод:**

```python theme={null}
{
    "questions": [  # Вопросы, которые были заданы
        {
            "question": str,
            "header": str,
            "options": [{"label": str, "description": str, "preview": str | None}],
            "multiSelect": bool,
        }
    ],
    "answers": dict[str, str],  # Сопоставляет текст вопроса со строкой ответа
    # Ответы с множественным выбором разделены запятыми
    "response": str | None,
    # Свободный ответ, введенный вместо ответа на вопросы; когда установлено,
    # Claude получает "The user responded: ..." вместо списка ответов
    "annotations": dict[str, dict] | None,  # Аннотации "preview" и "notes" для каждого вопроса из выборов пользователя
    "afkTimeoutMs": int | None,  # Установлено, когда диалог автоматически разрешился после этого количества миллисекунд неактивности пользователя; отсутствует, когда пользователь ответил
}
```

### Bash

**Имя инструмента:** `Bash`

Для информации о том, что устанавливает потолок переднего плана, см. [Таймаут и ограничения вывода](https://code.claude.com/docs/ru/tools-reference.md#timeout-and-output-limits). Для ограничения времени фонового режима см. [Ограничение времени для фоновых команд](https://code.claude.com/docs/ru/tools-reference.md#time-limit-for-background-commands).

**Ввод:**

```python theme={null}
{
    "command": str,  # Команда для выполнения
    "timeout": int | None,  # Миллисекунды. Передний план: ограничен 600000 по умолчанию, более высокие значения зажимаются. С run_in_background (Claude Code v2.1.285 или позже): ограничение времени фонового режима, 1800000 при пропуске, ограничено 7200000, если не повышено
    "description": str | None,  # Четкое, краткое описание (5-10 слов)
    "run_in_background": bool | None,  # Установите значение true для выполнения в фоне
}
```

**Вывод:**

```python theme={null}
{
    "stdout": str,  # Вывод команды; stdout и stderr поступают объединенными в этот один чередующийся поток
    "stderr": str,  # Уведомления, которые добавляет сам инструмент, не stderr команды
    "interrupted": bool,  # Была ли команда прервана
    "isImage": bool | None,  # Содержит ли stdout данные изображения
    "backgroundTaskId": str | None,  # ID фоновой задачи, если команда выполняется в фоне
}
```

### Monitor

**Имя инструмента:** `Monitor`

Запускает фоновый источник и доставляет каждое событие в Claude, чтобы он мог реагировать без опроса: `command` запускает скрипт и выдает одно событие на строку stdout, а `ws` открывает WebSocket и выдает одно событие на текстовый фрейм. Укажите ровно один из `command` или `ws`.

Источник `ws` требует Claude Code v2.1.195 или позже. Когда Monitor запускает команду, он следует тем же правилам разрешений, что и Bash. См. [Справочник инструмента Monitor](https://code.claude.com/docs/ru/tools-reference.md#monitor-tool) для информации о разрешениях WebSocket, поведении и доступности поставщика.

**Ввод:**

```python theme={null}
{
    "command": str | None,  # Скрипт оболочки; каждая строка stdout является событием, выход завершает наблюдение
    "ws": dict | None,  # Источник WebSocket: {"url": str, "protocols": list[str] | None}; каждый текстовый фрейм является событием
    "description": str,  # Краткое описание, показываемое в уведомлениях
    "timeout_ms": int | None,  # Срок в миллисекундах (по умолчанию 300000, макс 3600000; эффективный срок составляет максимум 1800000)
}
```

**Вывод:**

```python theme={null}
{
    "taskId": str,  # ID фоновой задачи мониторинга
    "timeoutMs": int,  # Эффективный срок наблюдения в миллисекундах
    "persistent": bool | None,  # False: каждое наблюдение имеет срок
}
```

### Edit

**Имя инструмента:** `Edit`

**Ввод:**

```python theme={null}
{
    "file_path": str,  # Абсолютный путь к файлу для изменения
    "old_string": str,  # Текст для замены
    "new_string": str,  # Текст для замены на
    "replace_all": bool | None,  # Заменить все вхождения (по умолчанию False)
}
```

**Вывод:**

```python theme={null}
{
    "filePath": str,  # Файл, который был отредактирован
    "oldString": str,  # Текст, который был заменен
    "newString": str,  # Текст, который его заменил
    "originalFile": str | None,  # Содержимое файла перед редактированием
    "structuredPatch": [  # Diff-блоки для изменения
        {
            "oldStart": int,
            "oldLines": int,
            "newStart": int,
            "newLines": int,
            "lines": list[str],
        }
    ],
    "userModified": bool,  # Изменил ли пользователь предложенное редактирование перед его принятием
    "replaceAll": bool,  # Были ли заменены все вхождения
    "gitDiff": {  # Необязательное резюме git diff для файла
        "filename": str,
        "status": "modified" | "added",
        "additions": int,
        "deletions": int,
        "changes": int,
        "patch": str,
        "repository": str | None,  # GitHub owner/repo, когда доступно
    } | None,
}
```

### Read

**Имя инструмента:** `Read`

**Ввод:**

```python theme={null}
{
    "file_path": str,  # Абсолютный путь к файлу для чтения
    "offset": int | None,  # Номер строки для начала чтения
    "limit": int | None,  # Количество строк для чтения
}
```

Вывод принимает одну из следующих форм в зависимости от того, что прочитал Claude. Проверьте ключ `type`, чтобы их различить.

**Вывод (type: `"text"`):**

```python theme={null}
{
    "type": "text",
    "file": {
        "filePath": str,  # Файл, который был прочитан
        "content": str,  # Возвращенное содержимое
        "numLines": int,  # Количество строк в возвращенном содержимом
        "startLine": int,  # Номер строки, с которой начинается содержимое
        "totalLines": int,  # Общее количество строк в файле
        "truncatedByTokenCap": bool | None,  # Присутствует и True, когда чтение всего файла превысило лимит токенов и содержимое — это первая страница
    },
}
```

**Вывод (type: `"image"`):**

```python theme={null}
{
    "type": "image",
    "file": {
        "base64": str,  # Данные изображения в кодировке Base64
        "type": "image/jpeg" | "image/png" | "image/gif" | "image/webp",  # MIME-тип изображения
        "originalSize": int,  # Исходный размер файла в байтах
        "dimensions": {  # Необязательная информация о размерах для сопоставления координат
            "originalWidth": int | None,  # Необязательно; исходная ширина в пикселях
            "originalHeight": int | None,  # Необязательно; исходная высота в пикселях
            "displayWidth": int | None,  # Необязательно; ширина после изменения размера
            "displayHeight": int | None,  # Необязательно; высота после изменения размера
        } | None,
    },
}
```

**Вывод (type: `"notebook"`):**

```python theme={null}
{
    "type": "notebook",
    "file": {
        "filePath": str,  # Записная книжка, которая была прочитана
        "cells": list,  # Ячейки записной книжки
    },
}
```

**Вывод (type: `"pdf"`):**

```python theme={null}
{
    "type": "pdf",
    "file": {
        "filePath": str,  # PDF, который был прочитан
        "base64": str,  # Данные PDF в кодировке Base64
        "originalSize": int,  # Размер файла в байтах
    },
}
```

**Вывод (type: `"parts"`):**

```python theme={null}
{
    "type": "parts",
    "file": {
        "filePath": str,  # PDF, который был прочитан
        "originalSize": int,  # Размер файла в байтах
        "count": int,  # Количество страниц, извлеченных как изображения
        "outputDir": str,  # Каталог, содержащий извлеченные изображения страниц
    },
    "firstPage": int | None,  # Необязательный номер страницы документа первой извлеченной страницы
}
```

**Вывод (type: `"file_unchanged"`):**

```python theme={null}
{
    "type": "file_unchanged",  # Файл не изменился с момента последнего чтения Claude в этой сессии, поэтому содержимое не повторяется
    "file": {
        "filePath": str,
    },
    "source": "seeded" | None,  # Присутствует, когда более ранняя копия поступила из файла CLAUDE.md или памяти, загруженного при запуске, а не из вызова Read
}
```

### Write

**Имя инструмента:** `Write`

**Ввод:**

```python theme={null}
{
    "file_path": str,  # Абсолютный путь к файлу для записи
    "content": str,  # Содержимое для записи в файл
}
```

**Вывод:**

```python theme={null}
{
    "type": "create" | "update",  # Создала ли запись новый файл или перезаписала существующий
    "filePath": str,  # Файл, который был записан
    "content": str,  # Содержимое, которое было записано
    "structuredPatch": [  # Diff-блоки; пусто для нового файла, когда ничего не изменилось или когда Claude Code пропустил diff
        {
            "oldStart": int,
            "oldLines": int,
            "newStart": int,
            "newLines": int,
            "lines": list[str],
        }
    ],
    "originalFile": str | None,  # Предыдущее содержимое; None для нового файла или когда предыдущее содержимое было слишком большим для включения
    "gitDiff": {  # Необязательное резюме git diff для файла
        "filename": str,
        "status": "modified" | "added",
        "additions": int,
        "deletions": int,
        "changes": int,
        "patch": str,
        "repository": str | None,  # GitHub owner/repo, когда доступно
    } | None,
    "userModified": bool | None,  # Необязательно; изменил ли пользователь предложенное содержимое перед его принятием
}
```

### Glob

**Имя инструмента:** `Glob`

**Ввод:**

```python theme={null}
{
    "pattern": str,  # Шаблон glob для сопоставления файлов
    "path": str | None,  # Каталог для поиска (по умолчанию текущий каталог)
}
```

**Вывод:**

```python theme={null}
{
    "durationMs": int,  # Время, затраченное на выполнение поиска, в миллисекундах
    "numFiles": int,  # Количество возвращенных путей после любого усечения
    "filenames": list[str],  # Совпадающие пути файлов
    "truncated": bool,  # Были ли результаты усечены на лимите 100 файлов
    "totalMatches": int | None,  # Необязательное общее количество совпадающих файлов перед усечением; нижняя граница, когда countIsComplete равно False
    "countIsComplete": bool | None,  # Необязательно; является ли totalMatches точным
}
```

`totalMatches` и `countIsComplete` требуют Claude Code v2.1.191 или позже.

### Grep

**Имя инструмента:** `Grep`

**Ввод:**

```python theme={null}
{
    "pattern": str,  # Шаблон регулярного выражения
    "path": str | None,  # Файл или каталог для поиска
    "glob": str | None,  # Шаблон glob для фильтрации файлов
    "type": str | None,  # Тип файла для поиска
    "output_mode": str | None,  # "content", "files_with_matches" или "count"
    "-i": bool | None,  # Поиск без учета регистра
    "-n": bool | None,  # Показать номера строк
    "-B": int | None,  # Строки для отображения перед каждым совпадением
    "-A": int | None,  # Строки для отображения после каждого совпадения
    "-C": int | None,  # Строки для отображения до и после
    "context": int | None,  # Строки для отображения до и после; -C является псевдонимом
    "-o": bool | None,  # Печать только совпадающих частей каждой строки
    "head_limit": int | None,  # Ограничить вывод первыми N строками/записями
    "offset": int | None,  # Пропустить первые N строк/записей перед применением head_limit
    "multiline": bool | None,  # Включить многострочный режим
}
```

**Вывод:**

```python theme={null}
{
    "mode": "content" | "files_with_matches" | "count" | None,  # Использованный режим вывода
    "numFiles": int,  # Количество файлов в результате; всегда 0 в режиме content
    "filenames": list[str],  # Совпадающие файлы в режиме files_with_matches; пусто в других режимах
    "content": str | None,  # Совпадающие строки в режиме content или подсчеты для каждого файла в режиме count
    "numLines": int | None,  # Количество строк в содержимом, присутствует в режиме content
    "numMatches": int | None,  # Общее количество совпадений, присутствует в режиме count
    "totalFiles": int | None,  # Необязательное общее количество перед head_limit и offset в режиме files_with_matches
    "totalLines": int | None,  # Необязательное общее количество перед head_limit и offset в режиме content
    "appliedLimit": int | None,  # Присутствует, когда head_limit усек результат
    "appliedOffset": int | None,  # Присутствует, когда был применен offset
    "timedOut": bool | None,  # True, когда время поиска истекло, поэтому результаты могут быть неполными
}
```

Grep возвращает эту форму dict в каждом режиме вывода. Какие необязательные ключи присутствуют, зависит от `output_mode`.

`totalFiles` требует Claude Code v2.1.208 или позже. `totalLines` требует Claude Code v2.1.210 или позже. `timedOut` требует Claude Code v2.1.317 или позже.

### NotebookEdit

**Имя инструмента:** `NotebookEdit`

**Ввод:**

```python theme={null}
{
    "notebook_path": str,  # Абсолютный путь к записной книжке Jupyter
    "cell_id": str | None,  # ID ячейки для редактирования
    "new_source": str,  # Новый исходный код для ячейки
    "cell_type": "code" | "markdown" | None,  # Тип ячейки
    "edit_mode": "replace" | "insert" | "delete" | None,  # Тип операции редактирования
}
```

**Вывод:**

```python theme={null}
{
    "new_source": str,  # Исходный код, записанный в ячейку
    "old_source": str | None,  # Предыдущий исходный код ячейки, присутствует для replace и delete
    "cell_id": str | None,  # ID отредактированной ячейки, когда доступно
    "cell_type": "code" | "markdown",  # Тип ячейки
    "language": str,  # Язык программирования записной книжки
    "edit_mode": str,  # Использованный режим редактирования
    "error": str | None,  # Сообщение об ошибке, когда операция не удалась
    "notebook_path": str,  # Файл записной книжки
    "original_file": str,  # Содержимое записной книжки перед редактированием
    "updated_file": str,  # Содержимое записной книжки после редактирования
}
```

### WebFetch

**Имя инструмента:** `WebFetch`

**Ввод:**

```python theme={null}
{
    "url": str,  # URL для получения содержимого
    "prompt": str,  # Промпт для запуска на полученном содержимом
    "offset": int | None,  # Количество символов, пропускаемых от начала страницы. Требует Python Agent SDK 0.2.164 или позже
}
```

**Вывод:**

```python theme={null}
{
    "bytes": int,  # Размер полученного содержимого в байтах
    "code": int,  # Код ответа HTTP
    "codeText": str,  # Текст кода ответа HTTP
    "result": str,  # Обработанный результат от применения промпта к содержимому
    "durationMs": int,  # Время получения и обработки содержимого в миллисекундах
    "url": str,  # URL, который был получен
}
```

### WebSearch

**Имя инструмента:** `WebSearch`

**Ввод:**

```python theme={null}
{
    "query": str,  # Поисковый запрос для использования
    "allowed_domains": list[str] | None,  # Включать результаты только с этих доменов
    "blocked_domains": list[str] | None,  # Никогда не включать результаты с этих доменов
}
```

**Вывод:**

```python theme={null}
{
    "query": str,  # Поисковый запрос
    "results": list[str | {"tool_use_id": str, "content": list[{"title": str, "url": str}]}],
    "durationSeconds": float,  # Длительность поиска в секундах
}
```

### TodoWrite

**Имя инструмента:** `TodoWrite`

> [!NOTE]
>
> Следующие инструменты доступны по умолчанию только на моделях Claude Opus 4.7, Claude Sonnet 4.6, Claude Haiku 4.5 и более ранних моделях. На всех остальных моделях, включая идентификаторы моделей, которые Claude Code не распознает, они недоступны, если вы не согласитесь на их использование:
>
> * `TodoWrite`
> * `TaskCreate`
> * `TaskGet`
> * `TaskUpdate`
> * `TaskList`
>
> Везде, где доступны инструменты, Claude Code предоставляет четыре инструмента Task, или `TodoWrite` вместо них, когда вы устанавливаете `CLAUDE_CODE_ENABLE_TASKS=0`.
>
> Этот набор по умолчанию применяется в Claude Code v2.1.268 и более поздних версиях, которые TypeScript Agent SDK поставляет начиная с версии v0.3.268.
>
> См. [Доступность модели](https://code.claude.com/docs/ru/agent-sdk/todo-tracking.md#model-availability) для подключения.

**Ввод:**

```python theme={null}
{
    "todos": [
        {
            "content": str,  # Описание задачи
            "status": "pending" | "in_progress" | "completed",  # Статус задачи
            "activeForm": str,  # Активная форма описания
        }
    ]
}
```

**Вывод:**

```python theme={null}
{
    "oldTodos": [  # Список задач перед обновлением
        {
            "content": str,
            "status": "pending" | "in_progress" | "completed",
            "activeForm": str,
        }
    ],
    "newTodos": [  # Список задач после обновления
        {
            "content": str,
            "status": "pending" | "in_progress" | "completed",
            "activeForm": str,
        }
    ],
}
```

### TaskCreate

**Имя инструмента:** `TaskCreate`

**Ввод:**

```python theme={null}
{
    "subject": str,  # Краткое название задачи
    "description": str,  # Подробное описание задачи
    "activeForm": str | None,  # Метка в настоящем времени, показываемая во время выполнения
    "metadata": dict | None,  # Произвольные метаданные вызывающей стороны
}
```

**Вывод:**

```python theme={null}
{
    "task": {"id": str, "subject": str},  # Созданная задача с назначенным ID
}
```

### TaskUpdate

**Имя инструмента:** `TaskUpdate`

**Ввод:**

```python theme={null}
{
    "taskId": str,  # ID задачи для обновления
    "status": Literal["pending", "in_progress", "completed", "deleted"] | None,
    "subject": str | None,
    "description": str | None,
    "activeForm": str | None,
    "addBlocks": list[str] | None,  # ID задач, которые эта задача теперь блокирует
    "addBlockedBy": list[str] | None,  # ID задач, которые теперь блокируют эту задачу
    "owner": str | None,
    "metadata": dict | None,
}
```

**Вывод:**

```python theme={null}
{
    "success": bool,
    "taskId": str,
    "updatedFields": list[str],  # Названия полей, которые изменились
    "error": str | None,
    "statusChange": {"from": str, "to": str} | None,
}
```

### TaskGet

**Имя инструмента:** `TaskGet`

**Ввод:**

```python theme={null}
{
    "taskId": str,  # ID задачи для чтения
}
```

**Вывод:**

```python theme={null}
{
    "task": {
        "id": str,
        "subject": str,
        "description": str,
        "status": Literal["pending", "in_progress", "completed"],
        "blocks": list[str],
        "blockedBy": list[str],
    } | None,  # None, когда ID не найден
}
```

### TaskList

**Имя инструмента:** `TaskList`

**Ввод:**

```python theme={null}
{}
```

**Вывод:**

```python theme={null}
{
    "tasks": [
        {
            "id": str,
            "subject": str,
            "status": Literal["pending", "in_progress", "completed"],
            "owner": str | None,
            "blockedBy": list[str],
        }
    ],
}
```

### TaskOutput

Удалено в Claude Code v2.1.277. Ранее получало вывод из запущенной или завершенной фоновой задачи, с `BashOutput`, принимаемым как псевдоним; Claude читает выходной файл фоновой задачи с помощью `Read` вместо этого.

Запись `disallowed_tools` или правило отказа, которое по-прежнему называет любое имя, игнорируется без предупреждения.

### TaskStop

**Имя инструмента:** `TaskStop`. Предыдущие имена `KillShell` и `KillBash` по-прежнему можно использовать в правилах разрешений, в matcher хуков и в параметрах `tools`, `allowed_tools` и `disallowed_tools`.

**Ввод:**

```python theme={null}
{
    "task_id": str | None,  # ID фоновой задачи для остановки
    "shell_id": str | None,  # Устарело: используйте task_id вместо этого
}
```

**Вывод:**

```python theme={null}
{
    "message": str,  # Сообщение о статусе операции
    "task_id": str,  # ID остановленной задачи
    "task_type": str,  # Тип остановленной задачи
    "command": str | None,  # Команда или описание остановленной задачи
}
```

### ExitPlanMode

**Имя инструмента:** `ExitPlanMode`

**Ввод:**

```python theme={null}
{
    "plan": str  # План для запуска пользователем на одобрение
}
```

**Вывод:**

```python theme={null}
{
    "plan": str | None,  # План, который был представлен пользователю
    "isAgent": bool,  # True, когда субагент вызвал инструмент
    "filePath": str | None,  # Присутствует, когда план был сохранен в файл
    "hasTaskTool": bool | None,  # Необязательно; доступен ли инструмент Agent в текущем контексте
    "planWasEdited": bool | None,  # Присутствует и True, когда пользователь отредактировал план перед одобрением
    "awaitingLeaderApproval": bool | None,  # Присутствует и True, когда товарищ по команде отправил план руководителю команды на одобрение
    "requestId": str | None,  # Необязательный ID этого запроса на одобрение
}
```

### ListMcpResources

**Имя инструмента:** `ListMcpResourcesTool`

**Ввод:**

```python theme={null}
{
    "server": str | None  # Необязательное имя сервера для фильтрации ресурсов
}
```

Результат — это список, а не dict, поэтому `tool_use_result` содержит `list` для этого инструмента.

**Вывод:**

```python theme={null}
[  # Одна запись на ресурс
    {
        "uri": str,  # URI ресурса
        "name": str,  # Имя ресурса
        "mimeType": str | None,  # Необязательный MIME-тип
        "description": str | None,  # Необязательное описание
        "server": str,  # Сервер, предоставляющий этот ресурс
    }
]
```

### ReadMcpResource

**Имя инструмента:** `ReadMcpResourceTool`

**Ввод:**

```python theme={null}
{
    "server": str,  # Имя сервера MCP
    "uri": str,  # URI ресурса для чтения
}
```

**Вывод:**

```python theme={null}
{
    "contents": [
        {
            "uri": str,  # URI ресурса
            "mimeType": str | None,  # Необязательный MIME-тип
            "text": str | None,  # Текстовое содержимое или примечание о двоичном содержимом
            "blobSavedTo": str | None,  # Присутствует, когда Claude Code сохранил двоичное содержимое на диск; путь сохраненного файла
        }
    ],
    "error": str | None,  # Присутствует, когда сервер не смог прочитать ресурс
}
```

## Построение интерфейса непрерывного разговора

Следующий пример сохраняет один `ClaudeSDKClient` подключённым на протяжении нескольких ходов, поэтому Claude помнит предыдущие сообщения. Введите `new` для отключения и повторного подключения для новой сессии или `exit` для завершения разговора.

```python theme={null}
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
)
import asyncio


class ConversationSession:
    """Maintains a single conversation session with Claude."""

    def __init__(self, options: ClaudeAgentOptions | None = None):
        self.client = ClaudeSDKClient(options)
        self.turn_count = 0

    async def start(self):
        await self.client.connect()
        print("Starting conversation session. Claude will remember context.")
        print(
            "Commands: 'exit' to quit, 'interrupt' to stop current task, 'new' for new session"
        )

        while True:
            user_input = input(f"\n[Turn {self.turn_count + 1}] You: ")

            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "interrupt":
                await self.client.interrupt()
                print("Task interrupted!")
                continue
            elif user_input.lower() == "new":
                # Disconnect and reconnect for a fresh session
                await self.client.disconnect()
                await self.client.connect()
                self.turn_count = 0
                print("Started new conversation session (previous context cleared)")
                continue

            # Send message - the session retains all previous messages
            await self.client.query(user_input)
            self.turn_count += 1

            # Process response
            print(f"[Turn {self.turn_count}] Claude: ", end="")
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="")
            print()  # New line after response

        await self.client.disconnect()
        print(f"Conversation ended after {self.turn_count} turns.")


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"], permission_mode="acceptEdits"
    )
    session = ConversationSession(options)
    await session.start()


# Example conversation:
# Turn 1 - You: "Create a file called hello.py"
# Turn 1 - Claude: "I'll create a hello.py file for you..."
# Turn 2 - You: "What's in that file?"
# Turn 2 - Claude: "The hello.py file I just created contains..." (remembers!)
# Turn 3 - You: "Add a main function to it"
# Turn 3 - Claude: "I'll add a main function to hello.py..." (knows which file!)

asyncio.run(main())
```

## Обработка ошибок

Следующий пример оборачивает вызов `query()` в обработчики для четырех из [типов ошибок](#error-types), которые вызывает SDK.

Этот пример перехватывает [`ResultError`](#resulterror), что требует Python Agent SDK версии 0.2.140 или позже.

```python theme={null}
import asyncio

from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    ResultError,
    CLIJSONDecodeError,
)


async def main():
    try:
        async for message in query(prompt="Hello"):
            print(message)
    except CLINotFoundError:
        print(
            "Claude Code CLI not found. Try reinstalling: pip install --force-reinstall claude-agent-sdk"
        )
    # Catch ResultError before ProcessError, which it subclasses. Its message
    # carries the error text. A refusal and a failed final request both usually
    # arrive with subtype "success", so check stop_reason, then terminal_reason.
    except ResultError as e:
        if e.data.get("stop_reason") == "refusal":
            print(f"Model declined to respond: {e}")
        elif e.terminal_reason == "api_error":
            print(f"API request failed: {e}")
        else:
            print(f"Query ended with an error result ({e.terminal_reason or e.subtype}): {e}")
    except ProcessError as e:
        print(f"Process failed with exit code: {e.exit_code}")
    except CLIJSONDecodeError as e:
        print(f"Failed to parse response: {e}")


asyncio.run(main())
```

## Конфигурация Sandbox

### `SandboxSettings`

Конфигурация для поведения sandbox. Используйте это для включения sandboxing команд и программной настройки ограничений сети.

```python theme={null}
class SandboxSettings(TypedDict, total=False):
    enabled: bool
    autoAllowBashIfSandboxed: bool
    excludedCommands: list[str]
    allowUnsandboxedCommands: bool
    network: SandboxNetworkConfig
    ignoreViolations: SandboxIgnoreViolations
    enableWeakerNestedSandbox: bool
```

| Property | Type | Default | Description |
| :- | :- | :- | :- |
| `enabled` | `bool` | `False` | Включить режим sandbox для выполнения команд |
| [`autoAllowBashIfSandboxed`](https://code.claude.com/docs/ru/settings-reference#sandbox-autoallowbashifsandboxed) | `bool` | `False` | Автоматически одобрять команды Bash, когда sandbox включен. Значение по умолчанию `False` требует Python SDK v0.2.182 или новее |
| `excludedCommands` | `list[str]` | `[]` | Команды, которые обходят ограничения sandbox, такие как `["docker *"]`. Они выполняются без sandbox автоматически без участия модели; [`sandbox.excludedCommands`](https://code.claude.com/docs/ru/settings-reference#sandbox-excludedcommands) описывает, когда применяется запись |
| `allowUnsandboxedCommands` | `bool` | `True` | Разрешить модели запрашивать выполнение команд вне sandbox. Когда `True`, модель может установить `dangerouslyDisableSandbox` в входных данных инструмента, что переходит к [системе разрешений](#permissions-fallback-for-unsandboxed-commands) |
| `network` | [`SandboxNetworkConfig`](#sandboxnetworkconfig) | `None` | Конфигурация sandbox для сети |
| `ignoreViolations` | [`SandboxIgnoreViolations`](#sandboxignoreviolations) | `None` | Настройка того, какие нарушения sandbox игнорировать |
| `enableWeakerNestedSandbox` | `bool` | `False` | Включить более слабый вложенный sandbox для совместимости |

> [!NOTE]
>
> Sandbox зависит от поддержки платформы и, на Linux, инструментов, таких как `bubblewrap` и `socat`. По умолчанию, когда `enabled` имеет значение `True`, но sandbox не может запуститься, команды выполняются без sandbox с предупреждением на stderr. Это поведение отличается от TypeScript SDK, где `failIfUnavailable` по умолчанию имеет значение `true`.
>
> Установите `"failIfUnavailable": True` в настройках песочницы, чтобы вместо этого остановить выполнение. Если задан `failIfUnavailable`, `query()` вызывает исключение [`ResultError`](#resulterror), когда песочница не может запуститься, поэтому оберните цикл `async for` в блок `try`. Причина указана в списке `errors` исключения. SDK передаёт `failIfUnavailable` в Claude Code вместе с объявленными полями `SandboxSettings`.

Чтобы запретить командам в песочнице запись в файл, укажите его абсолютный путь в [`denyWrite`](https://code.claude.com/docs/ru/settings-reference#sandbox-filesystem-denywrite) в настройках песочницы, например `"filesystem": {"denyWrite": ["/home/user/project/.env"]}`. SDK передаёт `filesystem` в Claude Code вместе с объявленными полями `SandboxSettings`. После запуска песочница блокирует запись по каждому указанному вами абсолютному пути.

#### Пример использования

```python theme={null}
import asyncio

from claude_agent_sdk import query, ClaudeAgentOptions

sandbox_settings = {
    "enabled": True,
    "autoAllowBashIfSandboxed": True,
    "failIfUnavailable": True,
    "network": {"allowLocalBinding": True},
}


async def main():
    try:
        async for message in query(
            prompt="Build and test my project",
            options=ClaudeAgentOptions(sandbox=sandbox_settings),
        ):
            print(message)
    except Exception as error:
        # query() raises, for example, when failIfUnavailable is set
        # and the sandbox can't start.
        print(f"Session ended with an error: {error}")


asyncio.run(main())
```

> [!WARNING]
>
> **Безопасность Unix socket**: Опция `allowUnixSockets` может предоставить доступ к системным сервисам, которые выходят за пределы sandbox. Например, разрешение `/var/run/docker.sock` фактически предоставляет полный доступ к хост-системе через Docker API, обходя изоляцию sandbox. Разрешайте только Unix sockets, которые строго необходимы, и поймите последствия безопасности каждого.

### `SandboxNetworkConfig`

Конфигурация для сети в режиме sandbox. Эти параметры применяются к sandboxed Bash командам, когда `enabled` имеет значение `True` в родительском [`SandboxSettings`](#sandboxsettings). Они не ограничивают инструмент WebFetch, который использует [правила разрешений](https://code.claude.com/docs/ru/permissions.md#webfetch) вместо этого.

```python theme={null}
class SandboxNetworkConfig(TypedDict, total=False):
    allowedDomains: list[str]
    deniedDomains: list[str]
    allowManagedDomainsOnly: bool
    allowUnixSockets: list[str]
    allowAllUnixSockets: bool
    allowLocalBinding: bool
    allowMachLookup: list[str]
    httpProxyPort: int
    socksProxyPort: int
```

| Property | Type | Default | Description |
| :- | :- | :- | :- |
| `allowedDomains` | `list[str]` | `[]` | Имена доменов, к которым могут получить доступ процессы в sandbox |
| `deniedDomains` | `list[str]` | `[]` | Имена доменов, к которым процессы в sandbox не могут получить доступ. Имеет приоритет над `allowedDomains` |
| `allowManagedDomainsOnly` | `bool` | `False` | Только управляемые параметры: когда установлено в управляемых параметрах, игнорировать `allowedDomains` и `WebFetch(domain:...)` правила разрешений из источников неуправляемых параметров. Не имеет эффекта при установке через параметры SDK |
| `allowUnixSockets` | `list[str]` | `[]` | Только macOS: пути Unix socket, к которым могут получить доступ процессы, например Docker socket. Игнорируется на Linux |
| `allowAllUnixSockets` | `bool` | `False` | Разрешить доступ ко всем Unix sockets, а на Linux — к сокетам VM (`AF_VSOCK`) |
| `allowLocalBinding` | `bool` | `False` | Разрешить процессам привязываться к локальным портам (например, для dev серверов) |
| `allowMachLookup` | `list[str]` | `[]` | Только macOS: имена сервисов XPC/Mach для разрешения. Поддерживает завершающий подстановочный знак |
| `httpProxyPort` | `int` | `None` | Порт HTTP прокси для сетевых запросов |
| `socksProxyPort` | `int` | `None` | Порт SOCKS прокси для сетевых запросов |

> [!NOTE]
>
> Встроенный прокси sandbox применяет список разрешённых доменов сети на основе запрашиваемого имени хоста. По умолчанию прокси не завершает и не проверяет трафик TLS, поэтому такие методы, как [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting), потенциально могут обойти список разрешённых доменов. См. [Ограничения безопасности sandboxing](https://code.claude.com/docs/ru/sandboxing.md#security-limitations) для деталей и [Безопасное развертывание](https://code.claude.com/docs/ru/agent-sdk/secure-deployment.md#traffic-forwarding) для настройки прокси, завершающего TLS.

### `SandboxIgnoreViolations`

Нарушения, которые не нужно включать в отчёт песочницы о нарушениях. Каждый ключ соответствует части команды или `*` для всех команд, а каждое значение перечисляет текст для поиска в строке нарушения: `{"*": ["/etc/hosts"]}` скрывает нарушения, в которых упоминается `/etc/hosts`. Соответствующий доступ по-прежнему блокируется. См. [`sandbox.ignoreViolations`](https://code.claude.com/docs/ru/settings-reference#sandbox-ignoreviolations).

```python theme={null}
SandboxIgnoreViolations = dict[str, list[str]]
```

### Fallback системы разрешений для команд без Sandbox

Когда `allowUnsandboxedCommands` включен, модель может запросить выполнение команд вне sandbox, установив `dangerouslyDisableSandbox: True` во входных данных инструмента. Эти запросы переходят к существующей системе разрешений, что означает, что ваш обработчик `can_use_tool` будет вызван, позволяя вам реализовать пользовательскую логику авторизации.

Ваши записи `excludedCommands` вместо этого выводят команду из sandbox без участия модели; [`sandbox.excludedCommands`](https://code.claude.com/docs/ru/settings-reference#sandbox-excludedcommands) описывает, когда применяется запись.

Следующий пример регистрирует каждый запрос без sandbox и отклоняет его, если только ваша собственная логика авторизации не разрешит это:

```python theme={null}
import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


def is_command_authorized(command: str | None) -> bool:
    # Replace with your own authorization logic
    return False



async def can_use_tool(
    tool: str, input: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Check if the model is requesting to bypass the sandbox
    if tool == "Bash" and input.get("dangerouslyDisableSandbox"):
        # The model is requesting to run this command outside the sandbox
        print(f"Unsandboxed command requested: {input.get('command')}")

        if is_command_authorized(input.get("command")):
            return PermissionResultAllow()
        return PermissionResultDeny(
            message="Command not authorized for unsandboxed execution"
        )
    return PermissionResultAllow()


# Required: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}


async def prompt_stream():
    yield {
        "type": "user",
        "message": {"role": "user", "content": "Deploy my application"},
    }


async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            sandbox={
                "enabled": True,
                "allowUnsandboxedCommands": True,  # Model can request unsandboxed execution
            },
            permission_mode="default",
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        print(message)


asyncio.run(main())
```

> [!WARNING]
>
> Команды, выполняемые с `dangerouslyDisableSandbox: True`, имеют полный доступ к системе. Убедитесь, что ваш обработчик `can_use_tool` тщательно проверяет эти запросы.
>
> Если `permission_mode` установлен на `bypassPermissions` и `allowUnsandboxedCommands` включен, модель может автономно выполнять команды вне sandbox без запросов одобрения, кроме [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). Эта комбинация фактически позволяет модели молча выходить из изоляции sandbox.

## См. также

* [Обзор SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) - Общие концепции SDK
* [Справочник TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md) - Документация TypeScript SDK
* [Пользовательские инструменты](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md) - Определение внутрипроцессных инструментов MCP, которые может вызывать Claude
* [Справочник CLI](https://code.claude.com/docs/ru/cli-reference.md) - Интерфейс командной строки
* [Общие рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md) - Пошаговые руководства
