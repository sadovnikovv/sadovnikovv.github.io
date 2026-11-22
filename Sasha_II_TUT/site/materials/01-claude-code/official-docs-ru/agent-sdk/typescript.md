> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник Agent SDK - TypeScript

> Полный справочник API для TypeScript Agent SDK, включая все функции, типы и интерфейсы.

## Установка

```bash theme={null}
npm install @anthropic-ai/claude-agent-sdk
```

> [!NOTE]
>
> SDK поставляется с нативным бинарным файлом Claude Code для вашей платформы в качестве опциональной зависимости, такой как `@anthropic-ai/claude-agent-sdk-darwin-arm64`. Большинство установок не требуют отдельной установки Claude Code. Версия SDK отслеживает версию упакованного Claude Code. SDK v0.3.191 поставляется с Claude Code v2.1.191, поэтому функция на этой странице, которая требует определённую версию Claude Code, нуждается в выпуске SDK с тем же номером патча или позже. Если ваш менеджер пакетов пропускает опциональные зависимости, SDK выбросит ошибку `Native CLI binary for <platform>-<arch> not found`; установите [`pathToClaudeCodeExecutable`](#options) на отдельно установленный бинарный файл `claude` вместо этого.
>
> Если ваш менеджер пакетов не применяет поле `libc` npm, как это делает Yarn 1.x, вы получите оба пакета платформы glibc и musl на Linux, примерно удвоив размер установки. На Agent SDK v0.2.141 или позже SDK всё ещё запускает правильный вариант. Чтобы освободить место в образе контейнера, удалите пакет платформы, который не соответствует libc, где работает ваше приложение; для среды выполнения glibc на x64 это `rm -rf node_modules/@anthropic-ai/claude-agent-sdk-linux-x64-musl`. На машине разработки удаление временное, так как Yarn переустанавливает пакет при следующем изменении зависимостей.

### Компиляция в единый исполняемый файл

Когда вы компилируете приложение в единый исполняемый файл с помощью `bun build --compile`, SDK не может разрешить упакованный бинарный файл CLI во время выполнения. `require.resolve` не работает внутри виртуальной файловой системы `$bunfs` скомпилированного исполняемого файла, поэтому SDK выбросит ошибку `Native CLI binary for <platform>-<arch> not found`.

Чтобы обойти это, встройте бинарный файл платформы как файловый ресурс, извлеките его на реальный путь при запуске с помощью `extractFromBunfs()` и передайте этот путь в [`pathToClaudeCodeExecutable`](#options).

Вспомогательная функция `extractFromBunfs()` требует `@anthropic-ai/claude-agent-sdk` версии 0.3.144 или позже. Пример ниже выполняет сборку для macOS на Apple Silicon:

```typescript theme={null}
import binPath from "@anthropic-ai/claude-agent-sdk-darwin-arm64/claude" with { type: "file" };
import { extractFromBunfs } from "@anthropic-ai/claude-agent-sdk/extract";
import { query } from "@anthropic-ai/claude-agent-sdk";

const cliPath = extractFromBunfs(binPath);

for await (const message of query({
  prompt: "Hello",
  options: { pathToClaudeCodeExecutable: cliPath },
})) {
  console.log(message);
}
```

`extractFromBunfs()` копирует встроенный бинарный файл из виртуальной файловой системы скомпилированного исполняемого файла в каталог временных файлов для каждого пользователя и возвращает реальный путь. Вне скомпилированного исполняемого файла он возвращает входной путь без изменений, поэтому тот же код работает в разработке без модификации.

Каждый скомпилированный исполняемый файл содержит бинарный файл одной платформы. Совместите пакет платформы в импорте с вашим `--target`:

* Для кросс-компиляции установите пакет несовпадающей платформы, например `npm install @anthropic-ai/claude-agent-sdk-linux-x64 --force`.
* На Windows подпуть бинарного файла — это `claude.exe`, например `@anthropic-ai/claude-agent-sdk-win32-x64/claude.exe`.

### Импортируйте запись `/core` при объединении Agent SDK

Если ваше приложение объединяет Agent SDK вместе со своими собственными зависимостями, импортируйте из `@anthropic-ai/claude-agent-sdk/core` вместо корня пакета. Запись `/core` требует TypeScript Agent SDK версии 0.3.282 или позже, и её типы требуют TypeScript 5.0 или позже.

Чтобы код, который загружает ваше приложение, оставался небольшим, запись `/core` опускает некоторые корневые экспорты:

* **Экспортируется**: те же `query()`, `startup()`, [`prewarm()`](#prewarm), `tool()`, `createSdkMcpServer()` и `resolveSettings()`, что и в корневой записи, вместе с функциями, которые переименовывают, помечают и удаляют сессии, `AbortError`, константы времени выполнения и все типы. Импорт альфа-версии `prewarm()` из `/core` требует Agent SDK версии 0.3.314 или позже.
* **Опущено**: корневые экспорты, включая класс `InMemorySessionStore` и вспомогательные функции, которые перечисляют, читают, разветвляют, импортируют и суммируют сессии. Если вам нужна одна из них, используйте корневую запись вместо этого.

Корневая запись встраивает свои собственные копии `zod` и `@modelcontextprotocol/sdk`. Запись `/core` импортирует их из вашего `node_modules` в диапазонах, которые объявляют `peerDependencies` Agent SDK, поэтому пакет, который уже их включает, не несёт вторую копию. Импортируйте либо из корня, либо из `/core` в данном процессе, но не из обоих: это отдельные пакеты, и загрузка обоих даёт вам две копии классов и состояния Agent SDK.

## Функции

### `query()`

Основная функция для взаимодействия с Claude Code. Создаёт асинхронный генератор, который потоком передаёт сообщения по мере их поступления.

```typescript theme={null}
function query({
  prompt,
  options
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query;
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `prompt` | `string \| AsyncIterable<`[`SDKUserMessage`](#sdkusermessage)`>` | Входной промпт в виде строки или асинхронного итерируемого объекта для потокового режима |
| `options` | [`Options`](#options) | Опциональный объект конфигурации (см. тип Options ниже) |

#### Возвращаемое значение

Возвращает объект [`Query`](#query-object), который расширяет `AsyncGenerator<`[`SDKMessage`](#sdkmessage)`, void>` дополнительными методами.

### `startup()`

Предварительно разогревает подпроцесс CLI, запуская его и завершая инициализационное рукопожатие до того, как промпт будет доступен. Возвращённый дескриптор [`WarmQuery`](#warmquery) принимает промпт позже и записывает его в уже готовый процесс, поэтому первый вызов `query()` разрешается без затрат на запуск подпроцесса и инициализацию в строке. Если вы ещё не знаете рабочий каталог сессии, используйте вместо этого [`prewarm()`](#prewarm).

```typescript theme={null}
function startup(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<WarmQuery>;
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `options` | [`Options`](#options) | Опциональный объект конфигурации. Аналогичен параметру `options` функции `query()` |
| `initializeTimeoutMs` | `number` | Максимальное время в миллисекундах для ожидания инициализации подпроцесса. По умолчанию `60000`. Если инициализация не завершится вовремя, промис отклонится с ошибкой таймаута |

Медленные [командные хуки](https://code.claude.com/docs/ru/hooks.md#command-hook-fields) [SessionStart](https://code.claude.com/docs/ru/hooks.md#sessionstart) и [Setup](https://code.claude.com/docs/ru/hooks.md#setup) получают дополнительное время, только если `initializeTimeoutMs` не задан:

* **Если вы оставите его незаданным:** время выполнения этих хуков не учитывается в 60-секундном значении по умолчанию, в сумме до 10 минут, поэтому инициализация может занять не более 11 минут.
* **Если вы зададите значение, включая `60000`:** это значение является пределом, даже пока выполняется хук.

Для дополнительного времени требуется TypeScript Agent SDK v0.3.304 или позже.

#### Возвращаемое значение

Возвращает `Promise<`[`WarmQuery`](#warmquery)`>`, который разрешается после того, как подпроцесс запущен и завершил инициализационное рукопожатие.

Из сообщений [`hook_progress`](#sdkhookprogressmessage), которые хук `SessionStart` или `Setup` отправляет до завершения рукопожатия, вы получаете только самое новое, содержащее весь вывод хука на данный момент. `startup()` удерживает это сообщение, сообщение хука [`hook_started`](#sdkhookstartedmessage) и всё остальное, что подпроцесс отправляет до завершения рукопожатия. Удержанные сообщения доходят до вас, как только вы вызываете `.query()` на `WarmQuery` и перебираете результат.

#### Пример

Вызовите `startup()` рано, например при загрузке приложения, затем вызовите `.query()` на возвращённом дескрипторе, когда промпт будет готов. Это выносит запуск подпроцесса и инициализацию из критического пути.

```typescript theme={null}
import { startup } from "@anthropic-ai/claude-agent-sdk";

// Оплатите стоимость запуска заранее
const warm = await startup({ options: { maxTurns: 3 } });

// Позже, когда промпт готов, это происходит мгновенно
for await (const message of warm.query("What files are here?")) {
  console.log(message);
}
```

### `prewarm()`

*Альфа.* Запускает процесс Claude Code как запасной до того, как вы узнаете, какую сессию он будет обслуживать, чтобы вы могли привязать его к сессии позже с помощью [`claim()`](#spareprocess). Требуется TypeScript Agent SDK v0.3.282 или позже.

Используйте `prewarm()`, когда ваше приложение загружается до того, как пользователь выберет папку.

```typescript theme={null}
function prewarm(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<SpareProcess>;
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `options` | [`Options`](#options) | Опциональный объект конфигурации того же типа, который принимает `startup()` |
| `initializeTimeoutMs` | `number` | Максимальное время в миллисекундах для ожидания инициализации запасного процесса. По умолчанию `60000`. Если инициализация не завершится вовремя, промис отклонится с ошибкой таймаута |

`prewarm()` учитывает время, затраченное на хуки [Setup](https://code.claude.com/docs/ru/hooks.md#setup), в `initializeTimeoutMs`, даже если вы оставите его незаданным. Чтобы дать медленным хукам Setup больше времени, задайте большее значение.

#### Возвращаемое значение

Возвращает `Promise<`[`SpareProcess`](#spareprocess)`>`, который разрешается, как только запасной процесс готов к привязке.

Промис отклоняется, если вы запрашиваете `resume`, `continue` или `forkSession` в `options`, потому что у запасного процесса ещё нет сессии.

#### Как работает запасной процесс

* **Где ждёт запасной процесс:** в приватном временном каталоге внутри вашего каталога конфигурации Claude Code или в `options.cwd`, если вы задали его в `prewarm()`.
* **Если ваш [`spawnClaudeCodeProcess`](#options) запускает Claude Code на другой машине или в контейнере:** передайте в `prewarm()` `options.cwd`, который там существует, потому что временный каталог по умолчанию создаётся на вашей машине.
* **Память:** каждый запасной процесс занимает примерно 230–260 МБ во время ожидания.
* **Что не происходит до вызова `claim()`:**
  * Переход в рабочий каталог, который вы передаёте в `claim()`
  * Выполнение хуков SessionStart
  * Запуск stdio MCP-серверов
  * Загрузка CLAUDE.md и контекста git
* **Что привязка не может изменить:** такие параметры, как `mcpServers`, `hooks`, `canUseTool`, `settingSources` и `plugins`, сохраняют свои значения из `prewarm()`. В [`SpareProcess`](#spareprocess) перечислено, что может задать привязка.
* **Если сессиям нужны разные значения этих параметров:** держите отдельный запасной процесс для каждого набора значений.

#### Пример

Выполните предварительный разогрев при загрузке приложения, затем привяжите запасной процесс, когда пользователь начинает сессию:

```typescript theme={null}
import { prewarm } from "@anthropic-ai/claude-agent-sdk";

// При загрузке приложения, до того как папка сессии известна
const spare = await prewarm({ options: { maxTurns: 3 } });

// Позже, когда пользователь начинает сессию в папке
const claimedQuery = spare.claim({
  prompt: "What files are here?",
  options: { cwd: "/path/to/project" },
});

spare.claimed.catch((error: Error) => {
  // Если сообщение не начинается с "option_not_applied", промпт не выполнился:
  // начните эту сессию с query() вместо этого
  console.error("Claim failed:", error.message);
});

try {
  for await (const message of claimedQuery) {
    console.log(message);
  }
} catch (error) {
  // После отклонённой привязки привязанный запрос выбрасывает исключение, как только выдаст результат с ошибкой
  console.error(`Session ended with an error: ${error}`);
}
```

### `tool()`

Создаёт типобезопасное определение инструмента MCP для использования с MCP-серверами SDK.

```typescript theme={null}
function tool<Schema extends AnyZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: InferShape<Schema>, extra: unknown) => Promise<CallToolResult>,
  extras?: { annotations?: ToolAnnotations; searchHint?: string; alwaysLoad?: boolean }
): SdkMcpToolDefinition<Schema>;
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `name` | `string` | Имя инструмента |
| `description` | `string` | Описание того, что делает инструмент |
| `inputSchema` | `Schema extends AnyZodRawShape` | Схема Zod, определяющая входные параметры инструмента (поддерживает Zod 3 и Zod 4) |
| `handler` | `(args, extra) => Promise<`[`CallToolResult`](#calltoolresult)`>` | Асинхронная функция, которая выполняет логику инструмента |
| `extras` | `{ annotations?: `[`ToolAnnotations`](#toolannotations)`; searchHint?: string; alwaysLoad?: boolean }` | Опциональные дополнительные параметры. `annotations` предоставляет клиентам поведенческие подсказки MCP. `searchHint` — это однострочная фраза о возможностях, показываемая в списке отложенных инструментов, когда активен [поиск инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md). `alwaysLoad: true` сохраняет полную схему этого инструмента в начальном промпте вместо её откладывания |

#### `ToolAnnotations`

Определено в `@modelcontextprotocol/sdk/types.js`. Все поля являются опциональными подсказками; клиенты не должны полагаться на них при принятии решений, связанных с безопасностью.

| Поле | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `title` | `string` | `undefined` | Удобочитаемое название инструмента |
| `readOnlyHint` | `boolean` | `false` | Если `true`, инструмент не изменяет свою среду |
| `destructiveHint` | `boolean` | `true` | Если `true`, инструмент может выполнять деструктивные обновления. Явно задайте `destructiveHint: true` для любого инструмента, который вы помечаете как [`always_ask`](#mcpservertoolpolicy), иначе классификатор авторежима может одобрять вызовы этого инструмента вместо вашего обратного вызова `canUseTool`. Оставить `destructiveHint` незаданным недостаточно, потому что при обработке вызовов `always_ask` Claude Code считает незаданный `destructiveHint` равным `false`, хотя по умолчанию в спецификации MCP используется `true` |
| `idempotentHint` | `boolean` | `false` | Если `true`, повторные вызовы с одинаковыми аргументами не имеют дополнительного эффекта (имеет смысл только когда `readOnlyHint` равен `false`) |
| `openWorldHint` | `boolean` | `true` | Если `true`, инструмент взаимодействует с внешними сущностями (например, веб-поиск). Если `false`, область инструмента закрыта (например, инструмент памяти) |

```typescript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const searchTool = tool(
  "search",
  "Search the web",
  { query: z.string() },
  async ({ query }) => {
    return { content: [{ type: "text", text: `Results for: ${query}` }] };
  },
  { annotations: { readOnlyHint: true, openWorldHint: true } }
);
```

### `createSdkMcpServer()`

Создаёт экземпляр MCP-сервера, который работает в том же процессе, что и ваше приложение.

```typescript theme={null}
function createSdkMcpServer(options: {
  name: string;
  version?: string;
  instructions?: string;
  tools?: Array<SdkMcpToolDefinition<any>>;
  alwaysLoad?: boolean;
  timeout?: number;
}): McpSdkServerConfigWithInstance;
```

#### Параметры

| Параметр | Тип | Описание |
| :- | :- | :- |
| `options.name` | `string` | Имя MCP-сервера |
| `options.version` | `string` | Опциональная строка версии |
| `options.instructions` | `string` | Опциональные инструкции сервера, возвращаемые из `initialize` и предоставляемые модели как блок инструкций MCP |
| `options.tools` | `Array<SdkMcpToolDefinition>` | Массив определений инструментов, созданных с помощью [`tool()`](#tool) |
| `options.alwaysLoad` | `boolean` | Когда `true`, инструменты этого сервера остаются в начальном промпте, а не откладываются за [поиском инструментов](https://code.claude.com/docs/ru/agent-sdk/tool-search.md). Сочетается с `alwaysLoad` для отдельного инструмента в [`tool()`](#tool) |
| `options.timeout` | `number` | Таймаут в миллисекундах для вызовов инструментов этого сервера. Claude Code применяет его к этому серверу вместо [`MCP_TOOL_TIMEOUT`](https://code.claude.com/docs/ru/env-vars). Передайте целое число не менее 1000. Claude Code игнорирует другие значения. Требуется TypeScript Agent SDK v0.3.248 или позже |

### `listSessions()`

Обнаруживает и перечисляет прошлые сессии с облегчёнными метаданными. Фильтруйте по каталогу проекта или перечисляйте сессии во всех проектах.

```typescript theme={null}
function listSessions(options?: ListSessionsOptions): Promise<SDKSessionInfo[]>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `options.dir` | `string` | `undefined` | Каталог, для которого перечисляются сессии. Если опущено, возвращает сессии во всех проектах |
| `options.limit` | `number` | `undefined` | Максимальное количество возвращаемых сессий |
| `options.includeWorktrees` | `boolean` | `true` | Когда `dir` находится внутри git-репозитория, включать сессии из всех путей worktree |

#### Тип возврата: `SDKSessionInfo`

| Свойство | Тип | Описание |
| :- | :- | :- |
| `sessionId` | `string` | Уникальный идентификатор сессии (UUID) |
| `summary` | `string` | Отображаемое название: пользовательское название, самый последний промпт, автоматически сгенерированное резюме или первый промпт |
| `lastModified` | `number` | Время последнего изменения в миллисекундах с начала эпохи |
| `fileSize` | `number \| undefined` | Размер файла сессии в байтах. Заполняется только для локального хранилища JSONL |
| `customTitle` | `string \| undefined` | Пользовательское название сессии, если оно установлено, например с помощью `--name`, `/rename`, вывода `sessionTitle` хука или [`renameSession()`](#renamesession). В противном случае — сгенерированное ИИ название сессии, если оно у сессии есть |
| `firstPrompt` | `string \| undefined` | Первый значимый пользовательский промпт в сессии |
| `gitBranch` | `string \| undefined` | Git-ветка в конце сессии |
| `cwd` | `string \| undefined` | Рабочий каталог сессии |
| `tag` | `string \| undefined` | Установленный пользователем тег сессии (см. [`tagSession()`](#tagsession)) |
| `createdAt` | `number \| undefined` | Время создания в миллисекундах с начала эпохи, из временной метки первой записи |

#### Пример

Выведите 10 самых последних сессий для проекта. Результаты отсортированы по `lastModified` в убывающем порядке, поэтому первый элемент является самым новым. Опустите `dir` для поиска во всех проектах.

```typescript theme={null}
import { listSessions } from "@anthropic-ai/claude-agent-sdk";

const sessions = await listSessions({ dir: "/path/to/project", limit: 10 });

for (const session of sessions) {
  console.log(`${session.summary} (${session.sessionId})`);
}
```

### `getSessionMessages()`

Читает сообщения пользователя и ассистента из транскрипта прошлой сессии.

```typescript theme={null}
function getSessionMessages(
  sessionId: string,
  options?: GetSessionMessagesOptions
): Promise<SessionMessage[]>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `sessionId` | `string` | обязательно | UUID сессии для чтения (см. `listSessions()`) |
| `options.dir` | `string` | `undefined` | Каталог проекта, в котором искать сессию. Если опущено, ищет во всех проектах |
| `options.limit` | `number` | `undefined` | Максимальное количество возвращаемых сообщений |
| `options.offset` | `number` | `undefined` | Количество сообщений, пропускаемых с начала |
| `options.includeSystemMessages` | `boolean` | `false` | Когда `true`, вместе с сообщениями пользователя и ассистента также возвращаются системные сообщения, например границы сжатия |

#### Тип возврата: `SessionMessage`

| Свойство | Тип | Описание |
| :- | :- | :- |
| `type` | `"user" \| "assistant" \| "system"` | Роль сообщения. `"system"` появляется только когда `options.includeSystemMessages` равно `true` |
| `uuid` | `string` | Уникальный идентификатор сообщения |
| `session_id` | `string` | Сессия, к которой принадлежит это сообщение |
| `message` | `unknown` | Необработанные данные сообщения из транскрипта |
| `parent_tool_use_id` | `string \| null` | Для сообщений субагента — `tool_use_id` вызова инструмента `Agent` или `Skill`, который запустил субагента. `null` для сообщений основной сессии и более старых сессий |
| `parent_agent_id` | `string \| null` | Для сообщений от [вложенного субагента](https://code.claude.com/docs/ru/sub-agents.md#let-subagents-spawn-their-own-subagents) — `agentId` субагента, который его запустил. `null` для сообщений основной сессии, сообщений от субагентов верхнего уровня и более старых сессий. Требуется Claude Code v2.1.202 или позже |

#### Пример

```typescript theme={null}
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";

const [latest] = await listSessions({ dir: "/path/to/project", limit: 1 });

if (latest) {
  const messages = await getSessionMessages(latest.sessionId, {
    dir: "/path/to/project",
    limit: 20
  });

  for (const msg of messages) {
    console.log(`[${msg.type}] ${msg.uuid}`);
  }
}
```

### `getSessionInfo()`

Читает метаданные одной сессии по ID без сканирования всего каталога проекта.

```typescript theme={null}
function getSessionInfo(
  sessionId: string,
  options?: GetSessionInfoOptions
): Promise<SDKSessionInfo | undefined>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `sessionId` | `string` | обязательно | UUID искомой сессии |
| `options.dir` | `string` | `undefined` | Путь к каталогу проекта. Если опущено, ищет во всех каталогах проектов |

Возвращает [`SDKSessionInfo`](#return-type-sdksessioninfo) или `undefined`, если сессия не найдена.

### `renameSession()`

Переименовывает сессию, добавляя запись пользовательского названия. Повторные вызовы безопасны; действует самое последнее название.

```typescript theme={null}
function renameSession(
  sessionId: string,
  title: string,
  options?: SessionMutationOptions
): Promise<void>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `sessionId` | `string` | обязательно | UUID сессии для переименования |
| `title` | `string` | обязательно | Новое название. Должно быть непустым после удаления пробелов |
| `options.dir` | `string` | `undefined` | Путь к каталогу проекта. Если опущено, ищет во всех каталогах проектов |

### `tagSession()`

Помечает сессию тегом. Передайте `null` для очистки тега. Повторные вызовы безопасны; действует самый последний тег.

```typescript theme={null}
function tagSession(
  sessionId: string,
  tag: string | null,
  options?: SessionMutationOptions
): Promise<void>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `sessionId` | `string` | обязательно | UUID сессии для пометки |
| `tag` | `string \| null` | обязательно | Строка тега или `null` для очистки |
| `options.dir` | `string` | `undefined` | Путь к каталогу проекта. Если опущено, ищет во всех каталогах проектов |

### `forkSession()`

Копирует транскрипт сессии в новую сессию, чтобы вы могли направить диалог в другую сторону, а исходная сессия осталась без изменений. Чтобы создать ответвление от более ранней точки диалога, передайте `upToMessageId`.

```typescript theme={null}
function forkSession(
  sessionId: string,
  options?: ForkSessionOptions
): Promise<ForkSessionResult>;
```

#### Параметры

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `sessionId` | `string` | обязательно | UUID сессии, от которой создаётся ответвление |
| `options.dir` | `string` | `undefined` | Путь к каталогу проекта. Если опущено, ищет во всех каталогах проектов |
| `options.upToMessageId` | `string` | `undefined` | Скопировать транскрипт до сообщения с этим `uuid` включительно: значение из [`getSessionMessages()`](#getsessionmessages) или `uuid`, который вы задали для потокового [`SDKUserMessage`](#sdkusermessage). Если опущено, копируется весь транскрипт |
| `options.title` | `string` | `undefined` | Название ответвления. Если опущено, SDK формирует его из исходной сессии с добавлением `(fork)` |

Возвращает `{ sessionId }` — UUID новой сессии. Передайте его как [`resume`](#options), чтобы продолжить ответвление. Ответвление не включает [файловые чекпоинты](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) исходной сессии, поэтому его нельзя откатить к чекпоинту, созданному до ответвления.

`forkSession()` выбрасывает исключение, когда:

* `sessionId` не является UUID
* сессия не найдена или не содержит сообщений
* `upToMessageId` не соответствует ни одному сообщению в транскрипте

### `resolveSettings()`

Вычисляет действующие настройки Claude Code для заданного каталога, используя тот же механизм объединения, что и CLI, без запуска Claude CLI. Используйте эту функцию, чтобы проверить, какую конфигурацию увидит вызов `query()`, прежде чем его выполнять.

> [!NOTE]
>
> Эта функция находится в альфа-версии, и её API может измениться до стабилизации.

Снимок отличается от того, что применяет живая сессия `query()`:

* **`policyHelper`**: `resolveSettings()` читает источники MDM, включая macOS plist и Windows HKLM/HKCU, но не выполняет настроенный администратором подпроцесс `policyHelper`.
* **Настройки, управляемые сервером**: `resolveSettings()` не загружает [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md#fetch-and-caching-behavior). Передайте их как `options.serverManagedSettings`, чтобы включить их.
* **`defaultMode`**: снимок возвращает `permissions.defaultMode` как есть из каждого уровня, поэтому он может включать значения `'auto'` и `'bypassPermissions'` из настроек проекта и локальных настроек, которые [живая сессия игнорирует](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in).

```typescript theme={null}
function resolveSettings(
  options?: ResolveSettingsOptions
): Promise<ResolvedSettings>;
```

#### Параметры

`resolveSettings()` принимает один объект параметров. Все поля опциональны.

| Параметр | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `options.cwd` | `string` | `process.cwd()` | Каталог, относительно которого вычисляются настройки проекта и локальные настройки |
| `options.settingSources` | [`SettingSource`](#settingsource)`[]` | Все источники | Какие источники файловой системы загружать. Передайте `[]`, чтобы пропустить пользовательские, проектные и локальные настройки. [Политика, управляемая на конечных устройствах](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms), загружается во всех случаях. `resolveSettings()` включает настройки, управляемые сервером, только когда вы передаёте `options.serverManagedSettings` |
| `options.managedSettings` | `Settings` | `undefined` | Настройки уровня политики, предоставленные встраивающим хостом. Следует тем же правилам, что и [`managedSettings` в `Options`](#options), за исключением того, что `resolveSettings()` не выполняет настроенный [`policyHelper`](https://code.claude.com/docs/ru/settings-reference#policyhelper), поэтому снимок может включать настройки, которые живая сессия отбрасывает |
| `options.serverManagedSettings` | `Settings` | `undefined` | Данные настроек, управляемых сервером, из `/api/claude_code/settings`. Неограничивающие ключи проходят без фильтрации |

#### Тип возврата: `ResolvedSettings`

`resolveSettings()` возвращает объект, описывающий объединённые настройки и источник, который предоставил каждый ключ.

| Свойство | Тип | Описание |
| :- | :- | :- |
| `effective` | `Settings` | Объединённые настройки после применения всех включённых источников в порядке приоритета |
| `provenance` | `Partial<Record<keyof Settings, ProvenanceEntry>>` | Для каждого ключа верхнего уровня в `effective` — какой источник предоставил значение |
| `sources` | `Array<{ source, settings, path?, policyOrigin? }>` | Необработанные настройки каждого источника, упорядоченные от самого низкого к самому высокому приоритету |

#### Пример

Пример ниже вычисляет настройки для каталога проекта и выводит источник, который задаёт период очистки. На машине, где ни один файл настроек не устанавливает `cleanupPeriodDays`, обе выведенные строки показывают `undefined` в качестве значения, что является ожидаемым результатом, а не ошибкой.

```typescript theme={null}
import { resolveSettings } from "@anthropic-ai/claude-agent-sdk";

const { effective, provenance } = await resolveSettings({
  cwd: "/path/to/project",
  settingSources: ["user", "project", "local"],
});

console.log(`Cleanup period: ${effective.cleanupPeriodDays} days`);
console.log(`Set by: ${provenance.cleanupPeriodDays?.source}`);
```

### `matchDeniedModels()`

Сообщает, какие из моделей `models` блокирует список [`deniedModels`](https://code.claude.com/docs/ru/settings-reference#deniedmodels). `denied` содержит по одному булеву значению на каждую модель: `true`, если какая-либо запись её блокирует. `warnings` помечает проигнорированные входные данные и записи, которые блокируют больше или меньше, чем кажется. Значение `false` не означает, что модель разрешена, потому что Claude Code также проверяет псевдонимы и переопределения моделей. Эта функция находится в альфа-версии и требует Agent SDK v0.3.323 или позже.

```typescript theme={null}
function matchDeniedModels(
  models: readonly string[],
  deniedModels: readonly string[] | undefined
): Promise<{ denied: boolean[]; warnings: string[] }>;
```

## Типы

### `Options`

Объект конфигурации для функции `query()`.

| Свойство | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `abortController` | `AbortController` | `new AbortController()` | Контроллер для отмены операций |
| `additionalDirectories` | `string[]` | `[]` | Дополнительные каталоги, к которым Claude может получить доступ. SDK передаёт каждую запись в Claude Code как `--add-dir`, поэтому при источнике настроек `project` Claude Code также [загружает скиллы, команды и субагентов из этого каталога](https://code.claude.com/docs/ru/permissions.md#additional-directories-grant-file-access-not-configuration) |
| `agent` | `string` | `undefined` | Имя агента для основного потока. Агент должен быть определён в параметре `agents` или в настройках |
| `agents` | `Record<string, [`AgentDefinition`](#agentdefinition)>` | `undefined` | Программное определение субагентов |
| `agentProgressSummaries` | `boolean` | `false` | При значении `true` генерирует однострочные сводки о ходе работы субагентов и передаёт их в событиях [`task_progress`](#sdktaskprogressmessage) через поле `summary`. Применяется к субагентам переднего плана и фоновым субагентам |
| `allowDangerouslySkipPermissions` | `boolean` | `false` | Разрешает обход разрешений. Требуется при использовании `permissionMode: 'bypassPermissions'` — при запуске или позже через `setPermissionMode()`. О взаимодействии с `permissionMode: 'plan'` см. [режим планирования](https://code.claude.com/docs/ru/agent-sdk/permissions.md#plan-mode-plan) |
| `allowedTools` | `string[]` | `[]` | Инструменты, которые автоматически одобряются без запроса, за исключением чтения из [сетевых путей](https://code.claude.com/docs/ru/permissions.md#network-paths). Это не ограничивает Claude только этими инструментами. Если указать здесь один из [инструментов отслеживания задач](https://code.claude.com/docs/ru/agent-sdk/todo-tracking.md#model-availability), Claude Code также включит их для сессии. Остальные неперечисленные инструменты обрабатываются через `permissionMode` и `canUseTool`. Для блокировки инструментов используйте `disallowedTools`. См. [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules) |
| `betas` | [`SdkBeta`](#sdkbeta)`[]` | `[]` | Включить бета-функции |
| `canUseTool` | [`CanUseTool`](#canusetool) | `undefined` | Пользовательская функция разрешений, вызываемая только тогда, когда [процесс проверки разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated) доходит до запроса. Не вызывается для вызовов, автоматически одобренных через `allowedTools`, правила разрешения или `permissionMode`. Правило разрешения не одобряет заранее [действия, которые не одобряет автоматически ни один режим](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). Подробнее см. [`CanUseTool`](#canusetool) |
| `continue` | `boolean` | `false` | Продолжить последний диалог |
| `cwd` | `string` | `process.cwd()` | Текущий рабочий каталог |
| `debug` | `boolean` | `false` | Включить режим отладки для процесса Claude Code |
| `debugFile` | `string` | `undefined` | Записывать отладочные логи в указанный файл. Неявно включает режим отладки |
| `disallowedTools` | `string[]` | `[]` | Запрещаемые инструменты. Имя без уточнений, например `"Bash"`, удаляет инструмент из контекста Claude. Правило с областью действия, например `"Bash(rm *)"`, оставляет инструмент доступным и запрещает соответствующие вызовы во всех режимах разрешений, включая `bypassPermissions`, для команды [в том виде, как она написана](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits). См. [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#allow-and-deny-rules) |
| `effort` | `'low' \| 'medium' \| 'high' \| 'xhigh' \| 'max'` | `undefined` | Управляет тем, сколько усилий Claude вкладывает в ответ. Работает совместно с адаптивным мышлением, определяя глубину размышлений. См. [настройка уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) |
| `enableFileCheckpointing` | `boolean` | `false` | Включить отслеживание изменений файлов для отката. См. [Чекпоинты файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) |
| `env` | `Record<string, string \| undefined>` | `process.env` | Переменные окружения. Если параметр задан, он заменяет окружение подпроцесса, а не объединяется с `process.env`, поэтому передавайте `{ ...process.env, YOUR_VAR: 'value' }`, чтобы сохранить унаследованные переменные, такие как `PATH`. Пример этого шаблона см. в разделе [Обработка медленных или зависших ответов API](#handle-slow-or-stalled-api-responses), а переменные, которые читает базовый CLI, — в разделе [Переменные окружения](https://code.claude.com/docs/ru/env-vars.md). Задайте `CLAUDE_AGENT_SDK_CLIENT_APP`, чтобы идентифицировать ваше приложение в заголовке User-Agent |
| `executable` | `'bun' \| 'deno' \| 'node'` | Определяется автоматически | Используемая среда выполнения JavaScript |
| `executableArgs` | `string[]` | `[]` | Аргументы, передаваемые исполняемому файлу |
| `extraArgs` | `Record<string, string \| null>` | `{}` | Дополнительные аргументы |
| `fallbackModel` | `string` | `undefined` | Модель, используемая при сбое основной модели. Принимает список через запятую. О порядке и ограничении см. [Цепочки резервных моделей](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains). Рекомендации см. в разделе [Выбор модели](https://code.claude.com/docs/ru/agent-sdk/configuration.md#choose-a-model) |
| `forkSession` | `boolean` | `false` | При возобновлении через `resume` создаёт ответвление с новым ID сессии вместо продолжения исходной сессии |
| `forwardSubagentText` | `boolean` | `false` | Пересылать текст и блоки размышлений субагентов как сообщения ассистента и пользователя с заданным `parent_tool_use_id`, чтобы потребители могли отображать вложенный транскрипт. Без этого параметра Claude Code опускает текст и блоки размышлений субагента, работающего на [переднем плане](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background). О вложенных субагентах, скиллах с `context: fork` и версии Claude Code, необходимой для каждого случая, см. [Отслеживание сообщений субагентов](https://code.claude.com/docs/ru/headless.md#follow-subagent-messages) |
| `hooks` | `Partial<Record<`[`HookEvent`](#hookevent)`, `[`HookCallbackMatcher`](#hookcallbackmatcher)`[]>>` | `{}` | Колбэки хуков для событий |
| `includeHookEvents` | `boolean` | `false` | Включать события жизненного цикла хуков в поток сообщений как [`SDKHookStartedMessage`](#sdkhookstartedmessage), [`SDKHookProgressMessage`](#sdkhookprogressmessage) и [`SDKHookResponseMessage`](#sdkhookresponsemessage). События жизненного цикла для хуков `SessionStart` и `Setup` включаются всегда и не требуют этого параметра. Некоторые события хуков, такие как `Notification`, `SessionEnd`, `PreCompact` и `PostCompact`, никогда не создают `SDKHookStartedMessage`, даже с этим параметром. Для этих событий Claude Code по-прежнему отправляет `SDKHookProgressMessage`, пока командный хук, работающий дольше секунды, выдаёт вывод, и отправляет `SDKHookResponseMessage` только при завершении хука, [работающего в фоне](https://code.claude.com/docs/ru/hooks.md#run-hooks-in-the-background) |
| `includePartialMessages` | `boolean` | `false` | Включать события частичных сообщений |
| `loadTimeoutMs` | `number` | `60000` | *Альфа.* Таймаут в миллисекундах для каждого вызова `sessionStore.load()` и `sessionStore.listSubkeys()` при материализации во время возобновления. Если адаптер не завершит операцию в течение этого времени, запрос завершается с ошибкой, а не зависает. Игнорируется, если `sessionStore` не задан |
| `managedSettings` | `Settings` | `undefined` | Настройки уровня политики, которые ваш хост-процесс передаёт в запускаемую сессию. На машинах с управляемыми настройками, развёрнутыми администратором, Claude Code игнорирует их, если только управляемый источник администратора с наивысшим приоритетом не задаёт `parentSettingsBehavior: 'merge'`, и никогда не объединяет их, пока [`policyHelper`](https://code.claude.com/docs/ru/settings-reference#policyhelper) предоставляет управляемые настройки. Объединённые значения проходят через фильтр, пропускающий только ограничения; о том, что пропускает фильтр, и о блокировках `allowManaged*Only` см. [Ограничение родительских настроек](https://code.claude.com/docs/ru/claude-apps-gateway#restrict-parent-settings). Хост, задающий [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](https://code.claude.com/docs/ru/env-vars), вместо этого получает три ключа непосредственно из этих данных: свою [конфигурацию модели](https://code.claude.com/docs/ru/model-config.md#restrict-model-selection) в Claude Code v2.1.222 или новее, [`modelPricing`](https://code.claude.com/docs/ru/settings-reference#modelpricing), если ни один управляемый источник его не задаёт, в v2.1.246 или новее, и запись `ENABLE_TOOL_SEARCH` в env в v2.1.247 или новее |
| `maxBudgetUsd` | `number` | `undefined` | Остановить запрос, когда оценка стоимости на стороне клиента достигнет этого значения в USD. Оценка может превысить это значение, поэтому [оставляйте запас](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#budget-headroom). Учитываются только собственные расходы вызова; итоги, восстановленные из возобновлённой сессии, не учитываются. Оговорки о точности и поведении при сбросе см. в разделе [Отслеживание затрат и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md) |
| `maxThinkingTokens` | `number` | `undefined` | *Устарело:* используйте `thinking`. Максимальное число токенов для процесса мышления |
| `maxTurns` | `number` | `undefined` | Максимальное количество агентных [ходов](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#turns-and-messages) |
| `mcpServers` | `Record<string, [`McpServerConfig`](#mcpserverconfig)>` | `{}` | Конфигурации MCP-серверов |
| `model` | `string` | Значение по умолчанию из CLI | Псевдоним модели Claude или полное имя модели. См. [допустимые значения и идентификаторы для конкретных провайдеров](https://code.claude.com/docs/ru/model-config.md#available-models) |
| `onElicitation` | `(request: ElicitationRequest, options: { signal: AbortSignal }) => Promise<ElicitationResult>` | `undefined` | Колбэк для обработки запросов elicitation от MCP. Вызывается, когда MCP-сервер запрашивает ввод пользователя и ни один хук не обработал запрос раньше. Если колбэк не указан, необработанные запросы elicitation автоматически отклоняются |
| `outputFormat` | `{ type: 'json_schema', schema: JSONSchema }` | `undefined` | Определяет формат вывода результатов агента. Подробнее см. [Структурированный вывод](https://code.claude.com/docs/ru/agent-sdk/structured-outputs.md) |
| `outputStyle` | `string` | `undefined` | Не является полем `Options`. Вместо этого задайте `outputStyle` во встроенном объекте [`settings`](https://code.claude.com/docs/ru/settings) или в файле настроек. См. [Активация стиля вывода](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#activate-an-output-style) |
| `pathToClaudeCodeExecutable` | `string` | Определяется автоматически из встроенного нативного бинарного файла | Путь к исполняемому файлу Claude Code. Нужен, только если необязательные зависимости были пропущены при установке или ваша платформа не входит в число поддерживаемых |
| `permissionMode` | [`PermissionMode`](#permissionmode) | `undefined` | Режим разрешений для сессии. Если вы его не укажете и ничто другое не задаёт режим разрешений, например настройка [`permissions.defaultMode`](https://code.claude.com/docs/ru/settings-reference#permissions-defaultmode), сессия запускается в режиме `default`. См. [Режимы разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#permission-modes) |
| `permissionPromptToolName` | `string` | `undefined` | Имя MCP-инструмента для запросов разрешений |
| `permissionPrompts` | `'host' \| 'none'` | `'host'` | Кто отвечает на запросы разрешений: `'host'` направляет их в ваш колбэк [`canUseTool`](#canusetool) или в инструмент `permissionPromptToolName`, а `'none'` [отклоняет вызовы, которые потребовали бы запроса](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated). Требуется Claude Code v2.1.259 или новее |
| `persistSession` | `boolean` | `true` | При значении `false` отключает сохранение сессии на диск. Такие сессии нельзя возобновить позже |
| `planModeInstructions` | `string` | `undefined` | Пользовательские инструкции рабочего процесса для режима планирования. Когда `permissionMode` равен `'plan'`, эта строка заменяет стандартное тело рабочего процесса режима планирования. CLI по-прежнему обрамляет её преамбулой, обеспечивающей режим только для чтения, и завершающим блоком протокола ExitPlanMode |
| `plugins` | [`SdkPluginConfig`](#sdkpluginconfig)`[]` | `[]` | Загрузка пользовательских плагинов из локальных путей. Подробнее см. [Плагины](https://code.claude.com/docs/ru/agent-sdk/plugins.md) |
| `projectConfigRoot` | `string` | `undefined` | Абсолютный путь к доверенному checkout, worktree которого является `cwd`. Claude Code читает настройки проекта, `.mcp.json`, а также команды, агентов, скиллы, рабочие процессы, routines и стили вывода проекта из `.claude/` в этом каталоге вместо `cwd` и устанавливает `CLAUDE_PROJECT_DIR` равным этому каталогу. Хуки, вспомогательные скрипты, такие как `apiKeyHelper`, и stdio MCP-серверы запускаются с этим каталогом в качестве рабочего. Файлы `CLAUDE.md` и `.claude/rules/` по-прежнему загружаются из `cwd`. Требуется Claude Code v2.1.275 или новее |
| `promptSuggestions` | `boolean` | `false` | Включить предложения промптов. После хода Claude Code отправляет сообщение `prompt_suggestion` с предсказанным следующим промптом пользователя. Для некоторых ходов Claude Code не генерирует предложений, например когда ваш аккаунт близок к лимиту использования или достиг его. См. [Когда Claude Code пропускает предложения](https://code.claude.com/docs/ru/interactive-mode.md#when-claude-code-skips-suggestions) |
| `resume` | `string` | `undefined` | ID сессии для возобновления |
| `resumeDropsTurn` | `string` | `undefined` | Вместе с `resumeSessionAt`: UUID промпта хода, который усекающее возобновление должно отбросить. Claude Code отказывает в возобновлении, если отбрасываемый диапазон содержит что-либо, не относящееся к этому ходу, например поглощённые сообщения из очереди или уведомления о задачах, и указывает флаг `--resume-drops-turn` в сообщении об отказе. Эту пару читают только Agent SDK и возобновления в режиме print. Требуется Claude Code v2.1.223 или новее |
| `resumeSessionAt` | `string` | `undefined` | Возобновить сессию с сообщения с указанным UUID |
| `sandbox` | [`SandboxSettings`](#sandboxsettings) | `undefined` | Программная настройка поведения песочницы. Подробнее см. [Настройки песочницы](#sandboxsettings) |
| `sessionId` | `string` | Генерируется автоматически | Использовать конкретный UUID для сессии вместо автоматически сгенерированного |
| `sessionStore` | [`SessionStore`](https://code.claude.com/docs/ru/agent-sdk/session-storage#the-sessionstore-interface) | `undefined` | Зеркалирование транскриптов сессий во внешнее хранилище, чтобы другой хост мог их возобновить. См. [Сохранение сессий во внешнем хранилище](https://code.claude.com/docs/ru/agent-sdk/session-storage.md) |
| `sessionStoreFlush` | `'batched' \| 'eager'` | `'batched'` | *Альфа.* Режим сброса для `sessionStore`. Игнорируется, если `sessionStore` не задан |
| `settings` | `string \| Settings` | `undefined` | Встроенный объект [настроек](https://code.claude.com/docs/ru/settings.md), путь к файлу настроек или встроенная строка JSON. Заполняет уровень настроек флагов в [порядке приоритета](https://code.claude.com/docs/ru/settings.md#settings-precedence). Изменяется во время выполнения через [`applyFlagSettings()`](#applyflagsettings) |
| `settingSources` | [`SettingSource`](#settingsource)`[]` | Значения CLI по умолчанию (все источники) | Определяет, какие настройки из файловой системы загружать. Передайте `[]`, чтобы отключить пользовательские, проектные и локальные настройки. [Политика, управляемая на конечных устройствах](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms), загружается в любом случае; настройки, управляемые сервером, загружаются, когда сессия аутентифицируется с учётными данными организации в [подходящей конфигурации](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability). См. [Использование функций Claude Code](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#what-settingsources-does-not-control) |
| `skills` | `string[] \| 'all'` | `undefined` | Скиллы, доступные в сессии. Передайте `'all'`, чтобы включить все обнаруженные скиллы, или список имён скиллов. Передавайте только точные имена. В Agent SDK v0.3.221 или новее SDK отклоняет некорректные имена и имена с подстановочными символами с ошибкой ещё до запуска процесса Claude Code. Если параметр задан, SDK автоматически добавляет инструмент Skill в `allowedTools`. Если вы также передаёте `tools`, включите `'Skill'` в этот список. См. [Скиллы](https://code.claude.com/docs/ru/agent-sdk/skills.md) |
| `spawnClaudeCodeProcess` | `(options: SpawnOptions) => SpawnedProcess` | `undefined` | Пользовательская функция для запуска процесса Claude Code. Используйте её, чтобы запускать Claude Code в виртуальных машинах, контейнерах или удалённых средах |
| `stderr` | `(data: string) => void` | `undefined` | Колбэк для вывода stderr |
| `strictMcpConfig` | `boolean` | `false` | Использовать серверы, переданные в `mcpServers`, и игнорировать `.mcp.json` проекта, пользовательские настройки, MCP-серверы из плагинов и [коннекторы claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai) |
| `systemPrompt` | `string \| string[] \| { type: 'custom'; prompt: string \| string[]; snapshot?: boolean } \| { type: 'preset'; preset: 'claude_code'; append?: string; excludeDynamicSections?: boolean; snapshot?: boolean }` | `undefined` (минимальный промпт) | Конфигурация системного промпта. Передайте строку для пользовательского промпта или `{ type: 'preset', preset: 'claude_code' }`, чтобы использовать системный промпт Claude Code. Передайте массив строк с экспортируемой константой `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` между статической частью и частью, зависящей от запроса, чтобы [кэшировать статическую часть пользовательского промпта](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#cache-the-static-part-of-a-custom-prompt). При использовании объектной формы пресета добавьте `append`, чтобы дополнить его инструкциями, и задайте `excludeDynamicSections: true`, чтобы перенести контекст, зависящий от сессии, в первое сообщение пользователя для [лучшего повторного использования кэша промптов на разных машинах](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#improve-prompt-caching-across-users-and-machines). Задайте `snapshot: false`, чтобы пересобирать промпт при каждом запросе вместо [повторного использования промпта, записанного сессией при первом запросе](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#change-the-prompt-of-an-existing-session). Чтобы задать `snapshot` для пользовательского промпта, используйте форму `{ type: 'custom', prompt }`. Форма `{ type: 'custom' }` и поле `snapshot` требуют TypeScript Agent SDK v0.3.257 или новее |
| `taskBudget` | `{ total: number }` | `undefined` | *Альфа.* Бюджет задачи в токенах на стороне API. Если он задан, модели сообщается оставшийся бюджет токенов, чтобы она могла распределять использование инструментов и завершить работу до достижения лимита |
| `thinking` | [`ThinkingConfig`](#thinkingconfig) | `{ type: 'adaptive' }` для поддерживаемых моделей | Управляет поведением мышления/рассуждений Claude. Доступные варианты см. в [`ThinkingConfig`](#thinkingconfig) |
| `title` | `string` | `undefined` | Отображаемый заголовок сессии. При возобновлении через `resume` или `continue` приоритет имеет сохранённый заголовок возобновляемой сессии; чтобы переименовать существующую сессию, используйте [`renameSession()`](#renamesession) |
| `toolAliases` | `Record<string, string>` | `undefined` | Сопоставляет имена встроенных инструментов с именами MCP-инструментов, чтобы Claude вызывал вашу MCP-реализацию вместо встроенной. Например, `{ Bash: 'mcp__workspace__bash' }` |
| `toolConfig` | [`ToolConfig`](#toolconfig) | `undefined` | Конфигурация поведения встроенных инструментов. Подробнее см. [`ToolConfig`](#toolconfig) |
| `tools` | `string[] \| { type: 'preset'; preset: 'claude_code' }` | `undefined` | Конфигурация инструментов. Передайте массив имён инструментов или используйте пресет, чтобы получить инструменты Claude Code по умолчанию |
| `verbatimPrompts` | `boolean` | `false` | Доставлять каждый промпт в том виде, как он написан. SDK отправляет каждое сообщение пользователя с `client_composed: true`. Что Claude Code пропускает для таких сообщений, см. в описании [`client_composed`](#sdkusermessage). Используйте этот параметр, когда текст промпта включает содержимое, которое конечный пользователь не вводил. Для управления на уровне отдельных ходов оставьте его выключенным и задавайте `client_composed` для отдельных потоковых сообщений. Требуется TypeScript Agent SDK v0.3.280 или новее и Claude Code v2.1.248 или новее; версия Claude Code, входящая в состав этих версий SDK, удовлетворяет требованию к Claude Code |

#### Обработка медленных или зависших ответов API

Подпроцесс CLI читает несколько переменных окружения, которые управляют таймаутами API и обнаружением зависаний. Передавайте их через параметр `env`:

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const result = query({
  prompt: "Analyze this code",
  options: {
    env: {
      ...process.env,
      API_TIMEOUT_MS: "120000",
      CLAUDE_CODE_MAX_RETRIES: "2",
      CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS: "120000",
    },
  },
});
```

* [`API_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars): сколько каждая попытка запроса может ждать заголовков ответа, в миллисекундах. Переменная не ограничивает длительность потокового ответа после получения заголовков. По умолчанию `600000`. Применяется к основному циклу и ко всем субагентам.
* `CLAUDE_CODE_MAX_RETRIES`: максимальное количество повторных попыток API. По умолчанию `10`, не более `15`. Каждая повторная попытка получает собственное окно `API_TIMEOUT_MS`.

  Для автоматических запусков, которым нужно пережидать более длительные сбои, задайте [`CLAUDE_CODE_RETRY_WATCHDOG=1`](https://code.claude.com/docs/ru/errors#tune-retry-behavior): эта переменная бесконечно повторяет попытки при временных ошибках нехватки мощностей и, в Claude Code v2.1.199 или новее, повышает значение по умолчанию для других временных ошибок до `300` и снимает ограничение на эту переменную.
* `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`: сторожевой таймер зависаний для субагентов. Пока включён сторожевой таймер потока, значение по умолчанию равно `CLAUDE_STREAM_IDLE_TIMEOUT_MS` плюс 5 минут, что составляет `600000`, если вы не увеличили эту переменную. При выключенном сторожевом таймере потока значение по умолчанию — `600000`. До v2.1.257 значение по умолчанию всегда было `600000`.

  Таймер сбрасывается при каждом событии потока. При зависании Claude Code прерывает субагента и сообщает о зависании родителю. Для фонового субагента он также помечает задачу как неудавшуюся и прикладывает частичный результат, если он есть.
* `CLAUDE_ENABLE_STREAM_WATCHDOG` вместе с `CLAUDE_STREAM_IDLE_TIMEOUT_MS`: сторожевой таймер потока, который прерывает запрос, когда заголовки уже получены, но тело ответа перестаёт передаваться. Сторожевой таймер включён по умолчанию для всех провайдеров; задайте `CLAUDE_ENABLE_STREAM_WATCHDOG=0`, чтобы отключить его. `CLAUDE_STREAM_IDLE_TIMEOUT_MS` по умолчанию равен `300000` и не может быть меньше этого значения. О том, что Claude Code делает после прерывания в зависимости от того, насколько далеко продвинулся ответ, см. [Автоматические повторные попытки](https://code.claude.com/docs/ru/errors.md#automatic-retries).

  Пока сторожевой таймер ожидает ответа, который шлюз за `ANTHROPIC_BASE_URL` удерживает открытым с помощью keep-alive пингов, хост, задавший `includePartialMessages`, продолжает получать [события потока](#sdkpartialassistantmessage) `ping`, поэтому воспринимайте эти кадры как признак активности, а не завершайте сессию по таймауту из-за отсутствия данных. До v2.1.257 эти кадры прекращались через 5 минут после последнего реального события потока.

### Объект `Query`

Интерфейс, возвращаемый функцией `query()`.

```typescript theme={null}
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<SDKControlInterruptResponse | undefined>;
  rewindFiles(
    userMessageId: string,
    options?: { dryRun?: boolean }
  ): Promise<RewindFilesResult>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
  setModel(model?: string): Promise<void>;
  setMaxThinkingTokens(maxThinkingTokens: number | null): Promise<void>;
  applyFlagSettings(settings: {
    [K in keyof Settings]?: K extends 'effortLevel'
      ? 'low' | 'medium' | 'high' | 'xhigh' | 'max' | null
      : Settings[K] | null;
  }): Promise<void>;
  updateSettings(
    source: 'localSettings' | 'userSettings',
    settings: Record<string, unknown>,
  ): Promise<void>;
  initializationResult(): Promise<SDKControlInitializeResponse>;
  reinitialize(): Promise<SDKControlInitializeResponse>;
  supportedCommands(): Promise<SlashCommand[]>;
  supportedModels(): Promise<ModelInfo[]>;
  supportedAgents(): Promise<AgentInfo[]>;
  mcpServerStatus(): Promise<McpServerStatus[]>;
  getContextUsage(opts?: {
    detail?: 'summary' | 'full';
  }): Promise<SDKControlGetContextUsageResponse>;
  readFile(
    path: string,
    options?: { maxBytes?: number; encoding?: 'utf-8' | 'base64' }
  ): Promise<SDKControlReadFileResponse | null>;
  reloadPlugins(options?: {
    holdOnCacheImpact?: boolean;
    addPlugins?: SdkPluginConfig[];
  }): Promise<SDKControlReloadPluginsResponse>;
  reloadSkills(): Promise<SDKControlReloadSkillsResponse>;
  reloadOutputStyles(): Promise<SDKControlReloadOutputStylesResponse>;
  seedReadState(path: string, mtime: number): Promise<void>;
  accountInfo(): Promise<AccountInfo>;
  reconnectMcpServer(serverName: string): Promise<void>;
  toggleMcpServer(serverName: string, enabled: boolean): Promise<void>;
  setMcpServers(servers: Record<string, McpServerConfig>): Promise<McpSetServersResult>;
  setMcpPermissionModeOverride(
    serverName: string,
    mode: 'default' | 'auto' | null
  ): Promise<{ warning?: string }>;
  readMcpResource(serverName: string, uri: string): Promise<SDKControlMcpReadResourceResponse>;
  streamInput(stream: AsyncIterable<SDKUserMessage>): Promise<void>;
  stopTask(taskId: string): Promise<void>;
  backgroundTasks(toolUseId?: string): Promise<boolean>;
  close(): void;
}
```

#### Методы

| Метод | Описание |
| :- | :- |
| `interrupt()` | Прерывает запрос. Доступен только в режиме потокового ввода. Когда CLI объявляет возможность `interrupt_receipt_v1` в [`SDKSystemMessage.capabilities`](#sdksystemmessage), разрешается значением [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse) со списком сообщений, ожидавших обработки в момент поступления прерывания. В CLI до v2.1.205 разрешается значением `undefined` |
| `rewindFiles(userMessageId, options?)` | Восстанавливает файлы до состояния на момент указанного сообщения пользователя. Передайте `{ dryRun: true }` для предварительного просмотра изменений. Требует `enableFileCheckpointing: true`. См. [Чекпоинты файлов](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md) |
| `setPermissionMode()` | Изменяет режим разрешений (доступен только в режиме потокового ввода) |
| `setModel()` | Изменяет модель (доступен только в режиме потокового ввода). Передача `undefined` или строки `"default"` сбрасывает модель на [модель Claude Code по умолчанию](https://code.claude.com/docs/ru/model-config.md). Сессия в режиме `auto` [переключается в режим `default`](https://code.claude.com/docs/ru/agent-sdk/permissions#auto-mode-auto), если новая модель не поддерживает авторежим |
| `setMaxThinkingTokens()` | *Устарело:* используйте параметр `thinking`. Изменяет максимальное число токенов мышления. Передайте `null`, чтобы отменить предыдущие вызовы и восстановить параметр `thinking` или `maxThinkingTokens`, с которым была запущена сессия |
| `applyFlagSettings(settings)` | Объединяет настройки с уровнем настроек флагов сессии во время выполнения (доступен только в режиме потокового ввода). См. [`applyFlagSettings()`](#applyflagsettings) |
| `updateSettings(source, settings)` | Записывает один ключ из разрешённого списка в локальный файл настроек проекта или в ваш пользовательский файл настроек, чтобы значение сохранялось для последующих сессий. См. [`updateSettings()`](#updatesettings). Требуется TypeScript SDK v0.3.257 или новее, который включает Claude Code v2.1.257 |
| `initializationResult()` | Возвращает полный результат инициализации, включая поддерживаемые команды, модели, информацию об аккаунте и конфигурацию стиля вывода |
| `reinitialize()` | Повторно отправляет управляющий запрос `initialize` работающему CLI и возвращает свежий результат вместо кэшированного результата первого подключения. Используйте его после разрыва транспорта, например при повторном подключении к сессии после обрыва связи, чтобы ожидающие запросы разрешений снова попали в ваш колбэк `canUseTool`. Сделайте колбэк идемпотентным для каждого ID запроса, потому что запрос, ответ на который был потерян, отправляется повторно. Требуется Claude Code v2.1.195 или новее |
| `supportedCommands()` | Возвращает доступные команды. Начиная с Agent SDK v0.3.216 список отражает изменения команд в ходе сессии; см. [`SDKCommandsChangedMessage`](#sdkcommandschangedmessage) |
| `supportedModels()` | Возвращает доступные модели с информацией для отображения |
| `supportedAgents()` | Возвращает доступных субагентов как [`AgentInfo`](#agentinfo)`[]` |
| `mcpServerStatus()` | Возвращает статус подключённых MCP-серверов как [`McpServerStatus`](#mcpserverstatus)`[]` |
| `getContextUsage(opts?)` | Возвращает [`SDKControlGetContextUsageResponse`](#sdkcontrolgetcontextusageresponse) с разбивкой использования контекстного окна сессии по категориям, скиллам и инструментам. При значении `detail` по умолчанию включает данные, которые `/context` показывает в интерактивной сессии, вычисленные с помощью API-запросов подсчёта токенов, не появляющихся в потоке сообщений; см. [как обрабатываются эти запросы](#sdkcontrolgetcontextusageresponse). [Параметр `detail`](#sdkcontrolgetcontextusageresponse) требует Agent SDK v0.3.257 или новее |
| `readFile(path, options?)` | Читает файл из файловой системы сессии. Claude Code разрешает путь относительно `cwd`; в разделе [Что может читать `readFile()`](#what-readfile-can-read) перечислены файлы, которые он отдаёт. Передайте `{ maxBytes }`, чтобы изменить ограничение на чтение (по умолчанию 1 МБ, максимум 10 МБ), и `{ encoding: 'base64' }` для бинарных файлов, например изображений. Разрешается значением [`SDKControlReadFileResponse`](#sdkcontrolreadfileresponse) или `null` при отказе в разрешении, отсутствии файла или ошибке транспорта. Требуется TypeScript SDK v0.2.121 или новее |
| `reloadPlugins(options?)` | Перезагружает плагины с диска, чтобы плагины, установленные или изменённые в середине сессии, стали доступны работающей сессии. Разрешается с [`SDKControlReloadPluginsResponse`](#sdkcontrolreloadpluginsresponse), в котором перечислены команды, субагенты, плагины сессии и статус MCP-серверов. Требуется Agent SDK v0.2.85 или новее. [Параметр `holdOnCacheImpact`](#sdkcontrolreloadpluginsresponse) требует Agent SDK v0.3.268 или новее. [Параметр `addPlugins`](#load-more-plugin-folders-with-addplugins) требует Agent SDK v0.3.301 или новее |
| `reloadSkills()` | Перезагружает скиллы с диска, чтобы скиллы, которые вы добавляете или редактируете в ходе сессии, стали доступны работающей сессии. Разрешается значением [`SDKControlReloadSkillsResponse`](#sdkcontrolreloadskillsresponse) со списком скиллов, доступных после перезагрузки. Требуется Agent SDK v0.3.163 или новее |
| `reloadOutputStyles()` | Повторно читает [стили вывода](https://code.claude.com/docs/ru/output-styles.md) с диска, чтобы файл стиля, который вы добавляете или редактируете в ходе сессии, стал доступен работающей сессии. Разрешается значением [`SDKControlReloadOutputStylesResponse`](#sdkcontrolreloadoutputstylesresponse) со списком имён стилей, доступных после перезагрузки. Требуется Agent SDK v0.3.261 или новее |
| `seedReadState(path, mtime)` | Помечает файл как уже прочитанный, чтобы последующий Edit не завершился ошибкой `File has not been read yet`. См. [`seedReadState()`](#seedreadstate). Требуется TypeScript SDK v0.2.83 или новее |
| `accountInfo()` | Возвращает информацию об аккаунте |
| `reconnectMcpServer(serverName)` | Переподключает MCP-сервер по имени. Если имя также совпадает с записью в файле настроек, например `.mcp.json` или `~/.claude.json`, Claude Code переподключает сервер, который вы настроили через [`mcpServers`](#options) или `setMcpServers()`, а не запись из файла настроек. Такой порядок разрешения имён требует Claude Code v2.1.257 или новее |
| `toggleMcpServer(serverName, enabled)` | Включает или отключает MCP-сервер по имени с тем же порядком разрешения имён, что и `reconnectMcpServer()`. Отключение сервера разрывает соединение с ним и удаляет его инструменты. О версии Claude Code, необходимой для каждого типа сервера, см. [`toggleMcpServer()`](#togglemcpserver) |
| `setMcpServers(servers)` | Заменяет MCP-серверы, которыми управляет этот метод: серверы, добавленные через него, и [внутрипроцессные SDK-серверы](#createsdkmcpserver). Разрешается значением [`McpSetServersResult`](#mcpsetserversresult), в котором указано, какие серверы были добавлены и удалены, а также ошибки; в этом разделе также сказано, какие другие серверы остаются подключёнными |
| `setMcpPermissionModeOverride(serverName, mode)` | Переопределяет режим разрешений для инструментов одного MCP-сервера более строгим режимом, чем у сессии, или очищает переопределение значением `null`. Доступен только в режиме потокового ввода. См. [`setMcpPermissionModeOverride()`](#setmcppermissionmodeoverride). Требуется TypeScript SDK v0.3.187 или новее |
| `readMcpResource(serverName, uri)` | *Альфа.* Читает один ресурс MCP Apps `ui://` с подключённого MCP-сервера, чтобы ваше приложение могло отобразить виджет инструмента. Разрешается значением [`SDKControlMcpReadResourceResponse`](#sdkcontrolmcpreadresourceresponse). Требуется TypeScript Agent SDK v0.3.280 или новее |
| `streamInput(stream)` | Передаёт входные сообщения в запрос потоком для многоходовых диалогов |
| `stopTask(taskId)` | Останавливает выполняющуюся фоновую задачу по ID |
| `backgroundTasks(toolUseId?)` | Переводит в фон работающие команды Bash и субагентов, которых ожидает ход, так же как нажатие Ctrl+B в интерактивном терминале. См. [`backgroundTasks()`](#backgroundtasks). Требуется TypeScript SDK v0.2.139 или новее |
| `close()` | Закрывает запрос и завершает базовый процесс. Принудительно завершает запрос и освобождает все ресурсы |

#### `setMcpPermissionModeOverride()`

Переопределяет режим разрешений для инструментов одного MCP-сервера более строгим режимом, чем у сессии, или очищает переопределение значением `null`. Используйте, когда сессия работает в режиме, пропускающем запросы для каждого действия, но инструменты одного сервера всё же должны проверяться. Требуется TypeScript SDK v0.3.187 или новее.

Передайте в качестве `mode` одно из трёх значений:

* `'default'`: Claude Code оценивает вызовы инструментов этого сервера так же, как в [ручном режиме](https://code.claude.com/docs/ru/permission-modes.md#available-modes).
* `'auto'`: Claude Code направляет вызовы инструментов этого сервера через классификатор [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode). Claude Code отклоняет это значение, если классификатор недоступен для сессии.
* `null`: очищает переопределение.

Переопределение действует, только пока сессия находится в режиме, пропускающем запросы для каждого действия: `bypassPermissions` или `auto`. В любом другом режиме сессии Claude Code игнорирует переопределение, поэтому оно никогда не расширяет то, что разрешено сессии.

Промис разрешается значением `{ warning }`, если сервер с таким именем пока неизвестен. Claude Code всё равно сохраняет переопределение и применяет его, как только подключится сервер с точно таким же именем, поэтому предупреждение служит проверкой на опечатки, а не признаком сбоя.

Доступен только в режиме потокового ввода — то же ограничение, что и у `setModel()` и `setPermissionMode()`.

#### `seedReadState()`

Помечает файл как уже прочитанный, чтобы последующий Edit не завершился ошибкой `File has not been read yet`. Используйте, когда ваше приложение удалило из контекста диалога более ранний результат `Read`, а Claude следующим шагом будет редактировать этот файл. Требуется TypeScript SDK v0.2.83 или новее.

Передайте в `mtime` время изменения файла на момент того более раннего чтения в целых миллисекундах с начала эпохи, например `Math.floor(stat.mtimeMs)`. Если файл на диске изменился после этого времени, Claude Code пропускает пометку.

Промис разрешается независимо от того, был ли файл помечен, поэтому разрешённый промис не сообщает, что именно произошло.

#### `backgroundTasks()`

Переводит в фон работающие команды Bash и субагентов, которых ожидает ход, так же как нажатие Ctrl+B в интерактивном терминале. Передайте `toolUseId` вызова инструмента, чтобы перевести в фон только команду Bash или субагента, запущенных этим вызовом, или опустите его, чтобы перевести в фон все задачи переднего плана. Требуется TypeScript SDK v0.2.139 или новее.

Каждый переведённый в фон вызов инструмента сразу возвращается к Claude с результатом о выполнении в фоне, ход продолжается, а Claude Code отправляет [`SDKTaskNotificationMessage`](#sdktasknotificationmessage), когда задача завершится.

В сессии, где фоновые задачи включены, промис разрешается логическим значением:

* **`true`**: задача была переведена в фон или вы не указали `toolUseId`.
* **`false`**: переданный вами `toolUseId` не соответствует ни одной задаче переднего плана.

Если фоновые задачи отключены для сессии, например с помощью [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](https://code.claude.com/docs/ru/env-vars), промис вместо этого отклоняется и ничего не переводится в фон.

#### `applyFlagSettings()`

Изменяет [настройки](https://code.claude.com/docs/ru/settings.md) работающей сессии без перезапуска запроса. Используйте этот метод, когда в ходе сессии нужно изменить настройку, для которой нет отдельного сеттера, например ужесточить `permissions` после того, как агент прочитал недоверенные входные данные. `setModel()` и `setPermissionMode()` — это отдельные сеттеры для этих двух ключей; `applyFlagSettings()` — общая форма, принимающая любое подмножество ключей настроек, и передача `model` здесь работает так же, как `setModel()`.

В ходе сессии действуют только некоторые ключи:

* **Применяются на следующем ходе**: `ultracode`, `permissions`, `hooks`, `skillOverrides`, `fastMode`, `agent`. Смена `agent` также применяет переопределение модели и хуки этого агента на следующем ходе. Его системный промпт применяется на следующем ходе. В сессии, которая [повторно использует записанный системный промпт](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#change-the-prompt-of-an-existing-session), он применяется после сжатия сессии.
* **Применяются в течение текущего хода**: `model`. Если вы переключаете `model`, пока Claude работает над ходом, ответ, который Claude уже генерирует, завершается на старой модели, а остальная часть хода, начиная со следующего обращения Claude Code к модели, использует новую. Субагенты сохраняют собственную модель. До v2.1.212 переключение в середине хода вступало в силу только со следующего хода.
* **Применяется к следующему ходу**: `effortLevel`. Уровень применяется со следующего обращения Claude Code к модели. Если [смена effort сохраняет кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md#changing-effort-level), как в Claude Opus 5.5 с API-ключом или подпиской Claude, ожидайте применения на следующем ходе.
* **Не действуют в ходе сессии**: параметры системного промпта. Они определяются один раз при запуске, поэтому работающая сессия сохраняет исходное значение, хотя вызов завершается успешно. Чтобы изменить их, запустите новую сессию.

`effortLevel` принимает название [уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level). Он также принимает `"ultracode"`, что запрашивает уровень effort `xhigh` с включённым [ultracode](https://code.claude.com/docs/ru/workflows.md#let-claude-decide-with-ultracode). `applyFlagSettings()` объявляет `effortLevel` без этого значения, поэтому в TypeScript для того же результата передавайте `{ ultracode: true, effortLevel: "xhigh" }` или только ключ [`ultracode`](https://code.claude.com/docs/ru/settings-reference#ultracode), чтобы включить ultracode при текущем уровне effort сессии. Значение `ultracode` требует Claude Code v2.1.203 или новее и принимается только `applyFlagSettings()`, но не ключом `effortLevel` в файле настроек. До v2.1.284 один лишь ключ `ultracode` также устанавливал уровень `xhigh`.

Значения записываются в уровень флаговых настроек и объединяются поверх того, что задал при запуске встроенный параметр `settings` функции `query()`. Это тот же уровень, который [раздел о приоритете на этой странице](#settings-precedence) называет программными параметрами. Исключение — `effortLevel`: переданный вами уровень заменяет уровень из `--effort` или настроек, включая управляемые настройки, как показывает [порядок определения effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level).

Последовательные вызовы выполняют поверхностное объединение ключей верхнего уровня. Второй вызов с `{ permissions: {...} }` заменяет весь объект `permissions` из предыдущего вызова, а не объединяется с ним глубоко.

Чтобы сбросить ключ, заданный через `applyFlagSettings()`, передайте `null` для этого ключа. Большинство ключей затем сначала возвращаются к значению, которое параметр `settings` функции `query()` задал при запуске, а затем к источникам с более низким приоритетом. Сброшенный `model` возвращается к [модели Claude Code по умолчанию](https://code.claude.com/docs/ru/model-config.md), даже если `model` задан в файле настроек. Передача `undefined` ни на что не влияет, потому что сериализация JSON отбрасывает это значение.

Помимо `model`, ещё три ключа сбрасывают состояние сессии вместо возврата к предыдущим значениям:

* `effortLevel: null` возвращает сессию к уровню effort модели по умолчанию, а не к параметру `effort` функции `query()` или к `effortLevel` из файла настроек.
* `agent: null` запускает основной поток без агента, начиная со следующего хода, вместо восстановления параметра `agent` функции `query()` или `agent` из файла настроек. Если сброшенный агент применял собственную модель, сессия возвращается к модели, определённой при запуске.
* `ultracode: null` отключает ultracode, как и `false`, вместо восстановления значения `ultracode` из файла настроек. Сессия сохраняет текущий уровень effort, поэтому, чтобы изменить его, передайте `effortLevel` в том же вызове.

Доступен только в режиме потокового ввода — то же ограничение, что и у `setModel()` и `setPermissionMode()`.

В примере ниже активная модель переключается в ходе сессии, а затем переопределение сбрасывается, так что модель возвращается к [модели Claude Code по умолчанию](https://code.claude.com/docs/ru/model-config.md).

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const q = query({ prompt: messageStream });

// Override the model for the rest of the session
await q.applyFlagSettings({ model: "claude-opus-4-6" });

// Later: clear the override; the model resets to Claude Code's default
await q.applyFlagSettings({ model: null });
```

> [!NOTE]
>
> `applyFlagSettings()` доступен только в TypeScript. Python SDK не предоставляет эквивалентного метода.

#### `updateSettings()`

Записывает один ключ из разрешённого списка в файл настроек на диске, чтобы значение сохранялось для последующих сессий, загружающих этот источник. Каждый источник принимает один ключ со строковым значением:

* **`"localSettings"`**: принимает `outputStyle` и объединяет его с локальным файлом настроек проекта `.claude/settings.local.json`. Новый стиль вступает в силу со следующего запроса сессии.
* **`"userSettings"`**: принимает `effortLevel` и сохраняет его как [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) по умолчанию для текущей модели сессии в разделе [`modelSettings`](https://code.claude.com/docs/ru/settings-reference#modelsettings) вашего пользовательского файла настроек. Передача `max` ничего не записывает, потому что `max` действует только в рамках сессии. В любом случае работающая сессия сохраняет свой текущий уровень effort, поэтому, если вы хотите изменить и его, вызовите [`applyFlagSettings()`](#applyflagsettings). Этот источник требует TypeScript SDK v0.3.277 или новее, который включает Claude Code v2.1.277.

Вызов отклоняется, если запрос содержит любой другой ключ, если сессия работает через удалённый транспорт и если [`settingSources`](#options) сессии исключают указанный вами источник. Удаление ключа не поддерживается.

#### `toggleMcpServer()`

Отключение сервера разрывает соединение с ним и удаляет его инструменты из сессии. Для серверов, добавленных в ходе сессии, и для внутрипроцессных серверов это зависит от версии Claude Code:

* Сервер stdio, SSE или HTTP, добавленный в ходе сессии через `setMcpServers()`: удаление его инструментов требует Claude Code v2.1.285 или новее.
* Внутрипроцессный сервер, созданный с помощью [`createSdkMcpServer()`](#createsdkmcpserver), независимо от того, передали ли вы его в `mcpServers` или через `setMcpServers()`: разрыв соединения с ним и удаление его инструментов требуют Claude Code v2.1.286 или новее. Отключение такого сервера также приводит к ошибке для его ещё выполняющихся вызовов инструментов, поэтому Claude сразу получает результат с ошибкой для каждого из них, не дожидаясь возврата из вашего обработчика.

### `WarmQuery`

Дескриптор, возвращаемый [`startup()`](#startup). Подпроцесс уже запущен и инициализирован, поэтому вызов `query()` на этом дескрипторе записывает промпт непосредственно в готовый процесс без задержки на запуск.

```typescript theme={null}
interface WarmQuery extends AsyncDisposable {
  query(prompt: string | AsyncIterable<SDKUserMessage>): Query;
  close(): void;
}
```

#### Методы

| Метод | Описание |
| :- | :- |
| `query(prompt)` | Отправляет промпт в предварительно разогретый подпроцесс и возвращает [`Query`](#query-object). Может быть вызван только один раз для каждого `WarmQuery` |
| `close()` | Закрывает подпроцесс без отправки промпта. Используйте его, чтобы отбросить разогретый запрос, который больше не нужен |

`WarmQuery` реализует `AsyncDisposable`, поэтому его можно использовать с `await using` для автоматической очистки.

### `SpareProcess`

*Альфа.* Дескриптор, возвращаемый [`prewarm()`](#prewarm): запущенный процесс Claude Code, который ещё не привязан к сессии и может быть занят один раз. Требуется TypeScript Agent SDK v0.3.282 или новее.

```typescript theme={null}
interface SpareProcess extends AsyncDisposable {
  claim(params: {
    prompt: string | AsyncIterable<SDKUserMessage>;
    options: ClaimOptions;
  }): Query;
  readonly claimed: Promise<{ cwd: string; sessionId: string; parkedMs?: number; sdkMcpSettled: boolean }>;
  readonly exited: Promise<void>;
  close(): void;
}
```

#### Члены

| Член | Описание |
| :- | :- |
| `claim({ prompt, options })` | Привязывает резервный процесс к сессии в `options.cwd` и отправляет её первое сообщение. Синхронно возвращает [`Query`](#query-object), как и `query()`. Может быть вызван только один раз |
| `claimed` | Разрешается значением с рабочим каталогом и ID сессии, как только Claude Code принимает привязку. Отклоняется, если Claude Code отказывает в привязке, если процесс завершился или был закрыт раньше, а также — с сообщением, начинающимся с `option_not_applied`, — если сессия работает без запрошенных вами `model` или `maxThinkingTokens` |
| `exited` | Завершается, когда процесс завершается, независимо от того, был ли он привязан. Замените резервный процесс, который завершился до привязки |
| `close()` | Завершает процесс. До привязки это отбрасывает резервный процесс и отклоняет `claimed` |

`options.cwd` обязателен. При привязке также можно задать `additionalDirectories`, `model`, `permissionMode`, `maxThinkingTokens`, наложение настроек флагов в `settings`, `appendSystemPrompt`, `title`, `agents` и токены для отдельной сессии в `env`.

Claude Code может отказать в привязке, например для несуществующей папки или папки, настройки проекта которой задают `env`, `agent` или `model`. После отказа промпт, который `claim()` уже отправил, получает результат с ошибкой, текст которой начинается с `not_claimed`, после чего возвращённый запрос выбрасывает исключение. Оберните цикл запроса в блок try, чтобы продолжить работу после исключения. Когда `claimed` отклоняется с сообщением, начинающимся с `option_not_applied`, сессия работает без запрошенных вами `model` или `maxThinkingTokens`. После любого другого отклонения ваш промпт не выполнялся, поэтому запустите сессию через `query()`.

### `SDKControlInitializeResponse`

Тип возвращаемого значения `initializationResult()`. Содержит данные инициализации сессии.

```typescript theme={null}
type SDKControlInitializeResponse = {
  commands: SlashCommand[];
  agents: AgentInfo[];
  output_style: string;
  available_output_styles: string[];
  models: ModelInfo[];
  account: AccountInfo;
  fast_mode_state?: "off" | "cooldown" | "on";
  fast_mode_disabled_reason?: FastModeDisabledReason;
  hooks_applied?: boolean;
  sdk_mcp_manifests_parked?: Record<
    string,
    | "parked"
    | "already_connected"
    | "protocol_version_mismatch"
    | "malformed"
    | "not_honoured"
  >;
  claude_code_version?: string;
};
```

`hooks_applied` сообщает, зарегистрировал ли Claude Code хуки `hooks`, переданные в запросе `initialize`. SDK отправляет этот запрос один раз при запуске сессии и повторно при каждом вызове [`reinitialize()`](#query-object). Поле требует Agent SDK v0.3.238 или новее.

Claude Code опускает это поле, если запрос не содержал хуков. Если запрос содержал хуки, значение зависит от того, является ли запрос первой инициализацией сессии, а для повторной — от того, каким путём он достиг сессии:

* `true`: Claude Code зарегистрировал хуки. Первая инициализация сессии возвращает это значение. Повторная инициализация, отправленная через stdin CLI, также возвращает `true`. В этом случае хуки из нового запроса заменяют зарегистрированные ранее.
* `false`: Claude Code проигнорировал хуки. Повторная инициализация, отправленная в удалённую сессию, возвращает это значение, поэтому второй клиент, присоединившийся к сессии, не может заменить хуки, зарегистрированные первым клиентом.

До Agent SDK v0.3.238 ответ никогда не содержал этого поля, а Claude Code игнорировал `hooks` при каждой повторной инициализации.

Поле запроса `sdkMcpServerManifests` и поле ответа `sdk_mcp_manifests_parked` предназначены для внутрипроцессных [SDK MCP-серверов](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md), созданных вами с помощью [`createSdkMcpServer()`](#createsdkmcpserver). Ваше приложение не задаёт и не читает ни одно из этих полей.

`claude_code_version` — версия Claude Code процесса, выполняющего ходы сессии. Это то же значение, что содержится в init-сообщении [`SDKSystemMessage`](#sdksystemmessage), поэтому вы можете узнать версию CLI до первого хода.

* Поле требует Agent SDK v0.3.296 или новее, который включает Claude Code v2.1.296.
* Если поле равно `undefined` и вы задали `pathToClaudeCodeExecutable`, укажите в нём Claude Code v2.1.296 или новее.

Ответ всегда сообщает `fast_mode_state`, а когда что-то блокирует [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md), вместе с ним в `fast_mode_disabled_reason` передаётся код причины, чтобы вы могли объяснить заблокированное состояние, а не вычислять доступность заново. Оба поведения требуют Claude Code v2.1.219 или новее. До v2.1.219 ответ опускал `fast_mode_state`, когда быстрый режим был недоступен, и никогда не содержал причины. Коды причин и их значения см. в описании [`fast_mode_disabled_reason`](#sdkresultmessage) в сообщении с результатом.

Обёртка управляющего ответа на успешный `initialize` также содержит массив `pending_permission_requests`. Это поле находится в самой обёртке ответа, а не в данных `SDKControlInitializeResponse` выше. Каждая запись — это полное сообщение `control_request` той же структуры `{ type: "control_request", request_id, request }`, которую сессия передаёт для запросов разрешений во время работы.

Массив перечисляет запросы разрешений, которые этот процесс Claude Code отправил и которые ещё не разрешены. SDK читает массив за вас и передаёт каждую запись в ваш колбэк [`canUseTool`](#canusetool) — так же, как при повторной доставке, которую [`reinitialize()`](#query-object) запускает после разрыва транспорта. Обрабатывайте повторяющиеся ID запросов идемпотентно, потому что запись может повторять запрос, который колбэк уже получил до обрыва соединения.

Массив всегда присутствует в успешном ответе на `initialize` и пуст, если у этого процесса нет неразрешённых запросов разрешений. Требуется Claude Code v2.1.268 или новее. Более ранние версии могли опускать это поле, поэтому, если вы разбираете протокол самостоятельно, считайте отсутствие поля признаком более старого CLI, а не доказательством того, что ожидающих запросов нет.

### `SDKControlInterruptResponse`

Квитанция о прерывании: значение, которым разрешается [`interrupt()`](#query-object) в CLI, объявляющем возможность `interrupt_receipt_v1` в [`SDKSystemMessage.capabilities`](#sdksystemmessage). Требуется Claude Code v2.1.205 или новее. Более ранние CLI отвечают на прерывание пустыми данными об успехе, поэтому `interrupt()` разрешается значением `undefined`.

```typescript theme={null}
type SDKControlInterruptResponse = {
  still_queued: string[];
  cancelled?: string[];
};
```

`still_queued` перечисляет UUID сообщений пользователя, ожидавших обработки в момент поступления прерывания: сообщения, всё ещё находящиеся в очереди, а также сообщения, которые Claude Code уже забрал из очереди для следующего хода. После начала первого хода сессии Claude Code обрабатывает перечисленные сообщения после прерывания, если вы предварительно их не отмените, и может объединить несколько из них в один ход. Если вы прерываете до начала первого хода, Claude Code прерывает этот ход сразу после его начала, и перечисленные сообщения в этом ходе не получают ответа.

Используйте квитанцию, чтобы решить, нужно ли что-то отправить повторно. Перечисленное сообщение, которое вы не отменили, попадает в диалог независимо от того, получит ли оно ответ, поэтому его повторная отправка доставит его Claude дважды.

Интерпретируйте список с учётом следующих оговорок:

* В списке появляются только сообщения, поставленные в очередь с UUID. Пустой массив не означает, что больше ничего не будет выполнено.
* В списке есть только сообщения основного потока. Сообщения, адресованные субагенту, в него не входят.
* Список может содержать UUID, которые ваш клиент никогда не отправлял, например триггеры [запланированных задач в рамках сессии](https://code.claude.com/docs/ru/scheduled-tasks.md). Игнорируйте незнакомые UUID, а не считайте их ошибкой.

Клиент, который работает с управляющим протоколом CLI напрямую, а не через `interrupt()`, может задать `cancel_queued: true` в управляющем запросе `interrupt`. Claude Code v2.1.219 и новее объявляет поддержку с помощью возможности `interrupt_cancel_queued_v1` в [`SDKSystemMessage.capabilities`](#sdksystemmessage); более старые CLI игнорируют это поле, и сообщения в очереди выполняются как обычно. Такое прерывание также отменяет все сообщения, которые иначе были бы перечислены в `still_queued`: квитанция перечисляет их в `cancelled`, `still_queued` пуст, и ни одно из них не выполняется.

На список `cancelled` распространяются те же оговорки, что и на `still_queued`. Метод `interrupt()` никогда не отправляет `cancel_queued`, поэтому квитанции, которыми он разрешается, не содержат `cancelled`.

Квитанция — это снимок, сделанный в момент обработки прерывания, и при чистом прерывании она приходит раньше [`SDKResultMessage`](#sdkresultmessage) прерванного хода. Читайте квитанцию, а не проверяйте очередь после этого результата: цикл сразу запускает следующий ход из очереди, поэтому очередь, которую вы проверяете после результата, уже изменилась.

### `SDKControlGetContextUsageResponse`

Тип возвращаемого значения [`getContextUsage()`](#query-object). При значении `detail` по умолчанию ответ включает данные, которые Claude Code отображает для команды `/context` в интерактивной сессии. Помимо количества токенов, эти данные содержат поля отображения, такие как `color` и `gridRows`, которые Claude Code использует для отрисовки сетки использования `/context`.

Необязательный аргумент `detail` метода определяет, как Claude Code подсчитывает каждую категорию. Аргумент `detail` требует Agent SDK v0.3.257 или новее.

* **`'full'`**: значение по умолчанию. Claude Code подсчитывает каждую категорию с помощью API-запросов [подсчёта токенов](https://platform.claude.com/docs/en/build-with-claude/token-counting). Эти запросы не появляются в потоке сообщений, поэтому отслеживание стоимости, основанное на чтении потока, их не увидит. В Anthropic API подсчёт токенов не тарифицируется.
* **`'summary'`**: передайте `{ detail: 'summary' }`, чтобы получить ответ на основе данных об использовании из последнего ответа и локальных оценок. Запросы подсчёта токенов не отправляются, а значения по категориям являются приблизительными.

Если вместо вызова метода вы отправляете `/context` как промпт, Claude Code прикрепляет данные [`SDKContextUsage`](#sdkcontextusage) к полю `context_usage` сообщения ассистента, которое доставляет результат. Это поле требует Agent SDK v0.3.232 или новее.

В `SDKControlGetContextUsageResponse` поля `categories[].id`, `mcpInstructions`, а также поля `pluginId` и `path` записей `agents` и `skills.skillFrontmatter` требуют Agent SDK v0.3.304 или новее.

```typescript theme={null}
type SDKControlGetContextUsageResponse = {
  categories: {
    id?:
      | "system_prompt"
      | "system_tools"
      | "mcp_tools"
      | "mcp_instructions"
      | "mcp_tools_deferred"
      | "system_tools_deferred"
      | "custom_agents"
      | "memory_files"
      | "skills"
      | "messages"
      | "autocompact_buffer"
      | "compact_buffer"
      | "free_space";
    name: string;
    tokens: number;
    color: string;
    isDeferred?: boolean;
    kind: "used" | "free" | "buffer" | "deferred";
  }[];
  totalTokens: number;
  maxTokens: number;
  rawMaxTokens: number;
  percentage: number;
  gridRows: {
    color: string;
    isFilled: boolean;
    categoryName: string;
    tokens: number;
    percentage: number;
    squareFullness: number;
  }[][];
  model: string;
  memoryFiles: {
    path: string;
    type: string;
    tokens: number;
  }[];
  mcpTools: {
    name: string;
    serverName: string;
    tokens: number;
    isLoaded?: boolean;
  }[];
  mcpInstructions?: {
    serverName: string;
    tokens: number;
  }[];
  deferredBuiltinTools?: {
    name: string;
    tokens: number;
    isLoaded: boolean;
  }[];
  systemTools?: {
    name: string;
    tokens: number;
  }[];
  systemPromptSections?: {
    name: string;
    tokens: number;
  }[];
  agents: {
    agentType: string;
    source: string;
    pluginId?: string;
    path?: string;
    tokens: number;
  }[];
  slashCommands?: {
    totalCommands: number;
    includedCommands: number;
    tokens: number;
  };
  skills?: {
    totalSkills: number;
    includedSkills: number;
    tokens: number;
    skillFrontmatter: {
      name: string;
      source: string;
      pluginName?: string;
      pluginId?: string;
      path?: string;
      tokens: number;
    }[];
  };
  autoCompactThreshold?: number;
  isAutoCompactEnabled: boolean;
  messageBreakdown?: {
    toolCallTokens: number;
    toolResultTokens: number;
    attachmentTokens: number;
    assistantMessageTokens: number;
    userMessageTokens: number;
    redirectedContextTokens: number;
    unattributedTokens: number;
    toolCallsByType: {
      name: string;
      callTokens: number;
      resultTokens: number;
    }[];
    attachmentsByType: {
      name: string;
      tokens: number;
    }[];
  };
  apiUsage: {
    input_tokens: number;
    output_tokens: number;
    cache_creation_input_tokens: number;
    cache_read_input_tokens: number;
  } | null;
};
```

Распределение токенов читайте из полей-коллекций:

* `categories` содержит итоговые значения по категориям. Поле `kind` каждой записи классифицирует строку с помощью тех же значений, что и [`SDKContextUsageCategory`](#sdkcontextusagecategory). Классифицируйте строки по нему, а не по отображаемому `name`. Поле требует Agent SDK v0.3.268 или новее.
* `mcpTools` и `agents` распределяют токены по отдельным MCP-инструментам и субагентам.
* `memoryFiles` перечисляет каждый загруженный файл памяти с его стоимостью.
* `skills.skillFrontmatter` распределяет токены списка скиллов по каждому включённому скиллу. Значения для отдельных скиллов измеряют запись каждого скилла в списке в том виде, в каком Claude Code её фактически отправляет, и она может быть короче полного frontmatter скилла. Сравните `skills.totalSkills` с `skills.includedSkills`, чтобы узнать, попали ли в список все обнаруженные скиллы.

`totalTokens` — текущее использование контекста сессии, а `maxTokens` — окно, относительно которого измеряется это использование. Это контекстное окно модели или меньшее окно автосжатия, если оно применяется. `rawMaxTokens` содержит то же значение, что и `maxTokens`, а `percentage` — это `totalTokens` в виде округлённого процента от этого окна. `apiUsage` содержит данные об использовании из последнего ответа API, а не накопленный итог по сессии.

Claude Code не заполняет необязательные диагностические поля `deferredBuiltinTools`, `systemTools` и `systemPromptSections`, поэтому ожидайте, что они будут отсутствовать, хотя тип их объявляет.

#### Поиск строки по ID, токенов инструкций сервера или плагина и файла элемента

Инструкции MCP-серверов — это заметки по использованию, которые предоставляют подключённые серверы и которые Claude Code добавляет в контекст; строка `mcp_instructions` в `categories` подсчитывает их токены. Используйте следующие поля [`getContextUsage()`](#query-object), чтобы выбрать одну строку `categories` по `id`, разбить токены `mcp_instructions` по серверам или найти плагин и файл, стоящие за элементом агента или скилла:

| Поле | Где находится | Что содержит |
| :- | :- | :- |
| `id` | Каждая строка `categories` | Идентификатор строки, одно из значений, перечисленных в [типе ответа](#sdkcontrolgetcontextusageresponse), например `mcp_instructions`. Сопоставляйте по `id`, чтобы выбрать одну строку, или по `kind`, чтобы сгруппировать строки. Более поздняя версия Claude Code может отправить значение, которого нет в установленных у вас типах, поэтому считайте нераспознанный `id` отсутствующим |
| `mcpInstructions` | Ответ | Один элемент `{ serverName, tokens }` для каждого подключённого MCP-сервера, предоставляющего инструкции, или пустой массив, если таких нет. Значения `tokens` — оценки, сумма которых равна `tokens` строки `mcp_instructions`. `serverName` — это `name`, которое [`mcpServerStatus()`](#query-object) сообщает для этого сервера |
| `pluginId` | Элементы `agents` и `skills.skillFrontmatter` | Указывает плагин, из которого получен элемент, в виде ID формата `name@marketplace`; отсутствует для элемента, не полученного из плагина. Если плагин получен не из маркетплейса, часть после `@` указывает [его происхождение](https://code.claude.com/docs/ru/plugins/loading.md#find-where-a-plugin-came-from), например `inline` для плагина, загруженного через опцию [`plugins`](#options) |
| `path` | Элементы `agents` и `skills.skillFrontmatter` | Абсолютный путь к файлу, определяющему агента или скилл, на машине, где работает Claude Code. Поле отсутствует, если элемент не определяется файлом, например для агента из опции [`agents`](#options) или скилла, встроенного в Claude Code |

В качестве примера сопоставления по `id` этот фрагмент находит строку `mcp_instructions`:

```typescript theme={null}
// q is the Query object that query() returned
const usage = await q.getContextUsage();
// undefined if no connected server supplies instructions
const row = usage.categories.find((c) => c.id === "mcp_instructions");
```

### `SDKControlReadFileResponse`

Тип возвращаемого значения [`readFile()`](#query-object).

```typescript theme={null}
type SDKControlReadFileResponse = {
  contents: string;
  absPath: string;
  truncated?: boolean;
  encoding?: 'base64';
};
```

`contents` содержит текст файла или данные в base64, если вы запросили `encoding: 'base64'`; в этом случае поле `encoding` ответа имеет значение `'base64'`. `absPath` — разрешённый абсолютный путь. `truncated` устанавливается, если файл был длиннее ограничения `maxBytes` и содержимое было обрезано на этом пределе.

#### Что может читать `readFile()`

`readFile()` отдаёт более узкий набор файлов, чем инструмент Read:

* Обычный файл внутри одного из рабочих каталогов сессии, таких как `cwd` и `additionalDirectories`
* Некоторые собственные файлы Claude Code для сессии, например результаты инструментов

Правила запрета и запроса для `Read` по-прежнему блокируют соответствующий путь, а широкое правило разрешения для `Read` не открывает `readFile()` доступ к остальной файловой системе. Для всего остального вызов разрешается значением `null`.

### `SDKControlReloadPluginsResponse`

Тип возвращаемого значения [`reloadPlugins()`](#query-object).

```typescript theme={null}
type SDKControlReloadPluginsResponse = {
  commands: SlashCommand[];
  agents: AgentInfo[];
  plugins: {
    name: string;
    path: string;
    source?: string;
    version?: string;
  }[];
  mcpServers: McpServerStatus[];
  error_count: number;
  held?: boolean;
  cache_impact?: {
    mcp_servers_added: string[];
    mcp_servers_removed: string[];
    lsp_tool_change: ("adds" | "may-add" | "removes" | "may-remove") | null;
  };
};
```

Поля-коллекции описывают сессию после вызова:

* `commands`, `agents` и `mcpServers`: команды, субагенты и статусы MCP-серверов сессии в тех же структурах, которые возвращают `supportedCommands()`, `supportedAgents()` и `mcpServerStatus()`. `supportedAgents()` продолжает возвращать список, полученный при инициализации, поэтому набор после перезагрузки читайте из `agents` здесь
* `plugins`: каждый загруженный плагин с его `name` и `path` установки. `version` повторяет то, что объявлено в манифесте плагина, и контролируется автором плагина, поэтому проверяйте его, прежде чем доверять. Поле опускается, если манифест не объявляет версию
* `error_count`: количество ошибок при загрузке плагинов

Передайте `{ holdOnCacheImpact: true }` в `reloadPlugins()`, чтобы задержать перезагрузку, которая сделала бы недействительным кэш промптов диалога, вместо её применения. Claude Code выполняет ту же проверку, которую интерактивная команда `/reload-plugins` делает, прежде чем [предупредить о стоимости для кэша](https://code.claude.com/docs/ru/prompt-caching.md#enabling-or-disabling-a-plugin). Параметр требует Agent SDK v0.3.268 или новее. Исполняемый файл Claude Code старше v2.1.268, например тот, на который вы указываете через `pathToClaudeCodeExecutable`, игнорирует этот параметр и применяет перезагрузку.

Если вы передаёте этот параметр, читайте `held`, чтобы узнать, что произошло:

* `true`: перезагрузка не была применена, и поля-коллекции описывают сессию в её текущем состоянии. `cache_impact` сообщает, что изменило бы применение. Чтобы всё равно применить перезагрузку, вызовите `reloadPlugins()` снова без этого параметра.
* `false`: проверка не обнаружила влияния на кэш, и перезагрузка была применена.
* Отсутствует: вы не передали этот параметр, или исполняемый файл Claude Code старше v2.1.268 и применил перезагрузку.

`cache_impact` присутствует только вместе с `held: true`. `mcp_servers_added` и `mcp_servers_removed` называют MCP-серверы плагинов, которые перезагрузка зарегистрировала бы или удалила, в виде имён с областью действия `plugin:<plugin>:<server>`. Эти имена задаются авторами плагинов, поэтому проверяйте их перед отображением. `lsp_tool_change` сообщает, добавило бы или удалило применение инструмент LSP, либо равно `null`, если не произошло бы ни того, ни другого. Формы с `may-` означают, что проверка не смогла полностью увидеть ожидающий набор плагинов.

#### Загрузка дополнительных папок плагинов с помощью `addPlugins`

Чтобы загрузить папки плагинов, которых не было в параметре [`plugins`](#options) при запуске, передайте их в `reloadPlugins()` как `addPlugins` — список записей [`SdkPluginConfig`](#sdkpluginconfig) с абсолютным `path`. Claude Code загружает новые папки и перезагружает существующие плагины сессии за один проход. MCP-серверы каждого добавленного плагина тоже подключаются, если только вы не установили [`skipMcpDiscovery`](#sdkpluginconfig) в записи этой папки. Требуется Agent SDK v0.3.301 или новее и Claude Code v2.1.301 или новее.

Этот пример добавляет одну папку в работающий запрос `q` и выводит путь установки каждого плагина, загруженного сессией, когда вызов возвращается:

```typescript theme={null}
const result = await q.reloadPlugins({
  addPlugins: [{ type: "local", path: "/opt/my-app/plugins/reports" }]
});

console.log(result.plugins.map((plugin) => plugin.path));
```

Если папка загрузилась, выведенный список содержит `/opt/my-app/plugins/reports`, а команды и субагенты плагина появляются в `result.commands` и `result.agents`.

Добавленная папка остаётся частью сессии. Когда вы снова вызываете `reloadPlugins()`, Claude Code перезагружает её вместе с другими плагинами, и передавать её в `addPlugins` повторно не нужно.

##### Когда `reloadPlugins()` не загружает папки `addPlugins`

Если `reloadPlugins()` отклоняется, ни одна из папок `addPlugins` не добавляется, поэтому при повторной попытке снова передайте их в `addPlugins`. Если отклонение вызвано одной из следующих причин, сессия сохраняет уже имевшиеся плагины:

* **Относительный `path` или некорректная запись**: сообщение об ошибке гласит `add_plugins must be a list of { type: "local", path } entries with absolute paths`. Claude Code отклоняет весь список из-за одной неверной записи, поэтому передавайте каждую запись как `{ type: "local", path }` с абсолютным `path`
* **Администратор включил [`disableSideloadFlags`](https://code.claude.com/docs/ru/settings-reference#disablesideloadflags) в ваших управляемых настройках**: сообщение гласит `reload_plugins add_plugins is disabled by managed settings (disableSideloadFlags)`. Чтобы загрузить папку, попросите этого администратора удалить настройку
* **[Песочницу](https://code.claude.com/docs/ru/sandboxing.md) не удалось пересобрать**: при включённой [изоляции в песочнице](#sandboxsettings) Claude Code пересобирает конфигурацию песочницы, чтобы shell-команды в песочнице не могли записывать в добавляемые вами папки. Сообщение гласит `the sandbox could not be rebuilt to keep shell commands out of this folder`. Убедитесь, что ваши [настройки песочницы](#sandboxsettings) по-прежнему образуют допустимую конфигурацию

Если вы передаёте `holdOnCacheImpact` и вызов разрешается с [`held: true`](#sdkcontrolreloadpluginsresponse), папки `addPlugins` не добавляются. Чтобы добавить их всё равно, снова вызовите `reloadPlugins()` с тем же списком `addPlugins` и без `holdOnCacheImpact`.

Если вызов разрешается без `held: true`, а папка всё равно отсутствует в `result.plugins`, начните с проверки следующих причин:

* **Папка не существует или её плагин не удалось загрузить**: `result.error_count` равно `1` или больше. Папка всё равно остаётся частью сессии. Исправив папку, снова вызовите `reloadPlugins()`, чтобы загрузить её, на этот раз не указывая её в `addPlugins`
* **Исполняемый файл Claude Code старше v2.1.301**: исполняемый файл старше v2.1.301 игнорирует `addPlugins` и перезагружает только плагины, которые уже были в сессии. Проверьте `claude_code_version` в [сообщении init](#sdksystemmessage) и запустите исполняемый файл версии v2.1.301 или новее

### `SDKControlReloadSkillsResponse`

Тип возвращаемого значения [`reloadSkills()`](#query-object).

```typescript theme={null}
type SDKControlReloadSkillsResponse = {
  skills: SlashCommand[];
};
```

`skills` перечисляет скиллы, доступные после перезагрузки, в той же структуре [`SlashCommand`](#slashcommand), которую возвращает `supportedCommands()`.

### `SDKControlReloadOutputStylesResponse`

Тип возвращаемого значения [`reloadOutputStyles()`](#query-object).

```typescript theme={null}
type SDKControlReloadOutputStylesResponse = {
  available_output_styles: string[];
};
```

`available_output_styles` перечисляет имена встроенных и пользовательских стилей вывода, доступных после перезагрузки.

### `SDKControlMcpReadResourceResponse`

Тип возвращаемого значения [`readMcpResource()`](#query-object), содержащий результат `resources/read` MCP-сервера. Требуется TypeScript Agent SDK v0.3.280 или новее.

```typescript theme={null}
type SDKControlMcpReadResourceResponse = {
  contents: {
    uri: string;
    mimeType?: string;
    text?: string;
    blob?: string;
    _meta?: Record<string, unknown>;
  }[];
};
```

Передайте в `readMcpResource()` имя сервера в том виде, в каком его сообщает `mcpServerStatus()`, и URI `ui://`, например `ui.resourceUri`, который инструмент объявляет в своём [`_meta`](#mcpserverstatus). Вызов отклоняется для любой другой схемы URI, для [SDK MCP-сервера](#createsdkmcpserver), который ваше приложение размещает само, и для неподключённого сервера. Метод доступен, когда [`capabilities`](#sdksystemmessage) init-сообщения включают `mcp_read_resource_v1`.

Каждая запись `contents` — это один элемент содержимого в том виде, в каком его отправил сервер, за исключением ключей `_meta` с префиксом `com.anthropic/`, который зарезервирован для Claude Code. `blob` содержит данные в base64 для бинарного элемента, а `_meta` — собственное поле `_meta` элемента, в которое сервер MCP Apps помещает `ui.csp` и `ui.permissions` ресурса.

Содержимое представляет собой недоверенный сторонний HTML, поэтому отображайте его в песочнице.

### `AgentDefinition`

Конфигурация субагента, определённого программно.

```typescript theme={null}
type AgentDefinition = {
  description: string;
  tools?: string[];
  disallowedTools?: string[];
  prompt: string;
  model?: string;
  mcpServers?: AgentMcpServerSpec[];
  skills?: string[];
  initialPrompt?: string;
  maxTurns?: number;
  autoCompactWindow?: number;
  background?: boolean;
  omitClaudeMd?: boolean;
  memory?: "user" | "project" | "local";
  effort?: "low" | "medium" | "high" | "xhigh" | "max" | number;
  permissionMode?: PermissionMode;
  criticalSystemReminder_EXPERIMENTAL?: string;
};
```

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `description` | Да | Описание на естественном языке того, когда следует использовать этого агента |
| `tools` | Нет | Массив имён разрешённых инструментов. Если не указан, наследуются все [инструменты, доступные субагентам](https://code.claude.com/docs/ru/sub-agents.md#available-tools). Чтобы предварительно загрузить скиллы в контекст агента, используйте поле `skills`, а не указывайте здесь `'Skill'` |
| `disallowedTools` | Нет | Массив имён инструментов, явно запрещённых для этого агента. Также принимаются шаблоны уровня MCP-сервера: `mcp__server` или `mcp__server__*` удаляет все инструменты этого сервера, а `mcp__*` удаляет все MCP-инструменты любого сервера |
| `prompt` | Да | Системный промпт агента |
| `model` | Нет | Переопределение модели для этого агента. Принимает псевдоним, например `'fable'`, `'opus'`, `'sonnet'`, `'haiku'`, `'inherit'`, или полный ID модели. `'inherit'` использует модель агента, который запустил этого агента. Если вы опускаете `model`, Claude Code выбирает модель в соответствии с [порядком выбора модели субагента](https://code.claude.com/docs/ru/sub-agents.md#choose-a-model) |
| `mcpServers` | Нет | Спецификации MCP-серверов для этого агента |
| `skills` | Нет | Массив имён скиллов для предварительной загрузки в контекст агента |
| `initialPrompt` | Нет | Автоматически отправляется как первый ход пользователя, когда этот агент работает в качестве агента основного потока |
| `maxTurns` | Нет | Максимальное число ходов агента (циклов обращения к API) до остановки |
| `autoCompactWindow` | Нет | Уменьшает [окно автосжатия](https://code.claude.com/docs/ru/sub-agents.md#subagent-auto-compact-window) для этого агента, когда он работает как субагент, до числа токенов от `100000` до `1000000`. Требуется TypeScript Agent SDK v0.3.296 или новее |
| `background` | Нет | Запускать этого агента при вызове как неблокирующую фоновую задачу |
| `omitClaudeMd` | Нет | Исключить пользовательские, проектные и локальные файлы CLAUDE.md из начального контекста этого агента; файлы управляемой политики по-прежнему загружаются. Используйте для агентов, получающих всё необходимое из промпта инструмента Agent. Игнорируется, когда этот агент работает как агент основного потока. Требуется TypeScript Agent SDK v0.3.271 или новее |
| `memory` | Нет | Источник памяти для этого агента: `'user'`, `'project'` или `'local'` |
| `effort` | Нет | Уровень effort рассуждений для этого агента. Принимает название уровня или целое число |
| `permissionMode` | Нет | Режим разрешений для выполнения инструментов в этом агенте. Когда он применяется, определяют [правила наследования для субагентов](https://code.claude.com/docs/ru/agent-sdk/permissions.md#available-modes). См. [`PermissionMode`](#permissionmode) |
| `criticalSystemReminder_EXPERIMENTAL` | Нет | Экспериментальное: критически важное напоминание, добавляемое в системный промпт |

### `AgentMcpServerSpec`

Определяет MCP-серверы, доступные субагенту. Может быть именем сервера (строкой, ссылающейся на сервер из конфигурации `mcpServers` родителя) или встроенной записью конфигурации сервера, сопоставляющей имена серверов с конфигурациями.

```typescript theme={null}
type AgentMcpServerSpec = string | Record<string, McpServerConfigForProcessTransport>;
```

Где `McpServerConfigForProcessTransport` — это `McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig`.

### `SettingSource`

Определяет, из каких источников конфигурации в файловой системе SDK загружает настройки.

```typescript theme={null}
type SettingSource = "user" | "project" | "local";
```

| Значение | Описание | Расположение |
| :- | :- | :- |
| `'user'` | Глобальные пользовательские настройки | `~/.claude/settings.json` |
| `'project'` | Общие настройки проекта (под контролем версий) | `.claude/settings.json` |
| `'local'` | Локальные настройки проекта, добавляются в gitignore, когда Claude Code сохраняет в них настройку | `.claude/settings.local.json` |

#### Поведение по умолчанию

Если `settingSources` не указан или равен `undefined`, `query()` загружает те же настройки из файловой системы, что и Claude Code CLI: пользовательские, проектные и локальные. Сведения о входных данных, которые считываются независимо от этого параметра, и о том, как их отключить, см. в разделе [Что не контролирует settingSources](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#what-settingsources-does-not-control).

#### Зачем использовать settingSources

**Отключение настроек из файловой системы:**

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Do not load user, project, or local settings from disk
const result = query({
  prompt: "Analyze this code",
  options: { settingSources: [] }
});
```

**Загрузка только определённых источников настроек:**

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Load only project settings, ignore user and local
const result = query({
  prompt: "Run CI checks",
  options: {
    settingSources: ["project"] // Only .claude/settings.json
  }
});
```

Чтобы загрузить инструкции проекта из CLAUDE.md, включите `"project"` в `settingSources`. О том, как загрузка CLAUDE.md взаимодействует с параметрами системного промпта, см. в разделе [Изменение системных промптов](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md#claude-md-files-for-project-level-instructions).

#### Приоритет настроек

Когда загружается несколько источников, настройки объединяются в следующем порядке приоритета (от высшего к низшему):

1. Локальные настройки (`.claude/settings.local.json`)
2. Настройки проекта (`.claude/settings.json`)
3. Пользовательские настройки (`~/.claude/settings.json`)

Программные параметры, такие как `agents`, `allowedTools` и `settings`, переопределяют пользовательские, проектные и локальные файловые настройки. Если настройка управляемой политики и программный параметр задают один и тот же ключ, применяется управляемое значение, за исключениями, например `effortLevel`, переданного в [`applyFlagSettings()`](#applyflagsettings).

### `PermissionMode`

```typescript theme={null}
type PermissionMode =
  | "default" // Standard permission behavior
  | "acceptEdits" // Auto-accept file edits
  | "bypassPermissions" // Bypass permission checks; explicit ask rules still prompt
  | "plan" // Planning mode - Claude explores and plans
  | "dontAsk" // Don't prompt for permissions, deny if not pre-approved
  | "auto"; // A model classifier reviews actions such as shell commands and network requests
```

### `CanUseTool`

Тип пользовательской функции разрешений для управления использованием инструментов.

Функция заменяет интерактивный запрос разрешения. SDK вызывает `canUseTool`, когда [процесс оценки разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated) приводит к запросу. Вызовы, одобренные одним из следующих способов, выполняются без вызова `canUseTool`:

* Вызов, который одобряет запись `allowedTools` или правило разрешения в настройках
* Вызов, который одобряет режим разрешений, например редактирование файла в режиме `acceptEdits`

Чтобы проверять такие вызовы, используйте [хук `PreToolUse`](https://code.claude.com/docs/ru/agent-sdk/hooks), который выполняется и для них.

Разрешающее правило не одобряет заранее [действия, которые не одобряются автоматически ни в одном режиме](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves); о том, какие из них доходят до callback-функции и что происходит в режимах `dontAsk` и `auto`, см. в разделе [Как оцениваются разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated).

```typescript theme={null}
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: {
    signal: AbortSignal;
    suggestions?: PermissionUpdate[];
    blockedPath?: string;
    mcpServer?: { name: string; source: string };
    decisionReason?: string;
    defaultToNo?: boolean;
    suppressAlwaysAllowRule?: boolean;
    toolUseID: string;
    agentID?: string;
    requestId: string;
  }
) => Promise<PermissionResult | null>;
```

| Параметр | Тип | Описание |
| :- | :- | :- |
| `signal` | `AbortSignal` | Срабатывает, если операцию следует прервать |
| `suggestions` | [`PermissionUpdate`](#permissionupdate)`[]` | Предлагаемые обновления разрешений, чтобы пользователю больше не задавался запрос для этого инструмента. Запросы Bash могут включать предложение с [местом назначения](#permissionupdatedestination) `localSettings`, поэтому возврат его в `updatedPermissions` записывает правило в `.claude/settings.local.json`, и оно сохраняется между сессиями. |
| `blockedPath` | `string` | Путь к файлу, вызвавшему запрос разрешения, если применимо |
| `mcpServer` | `{ name: string; source: string }` | Для инструмента `mcp__*` — MCP-сервер, который его предоставляет, и источник определения этого сервера, с полями [`McpServerProvenance`](#mcpserverprovenance). Отсутствует для других инструментов. Требуется Agent SDK v0.3.274 или новее |
| `decisionReason` | `string` | Объясняет, почему был вызван этот запрос разрешения |
| `defaultToNo` | `boolean` | Если `true`, одно случайное нажатие клавиши не должно одобрять этот запрос: открывайте запрос с фокусом на варианте отказа, не выбирайте одобрение заранее и не предлагайте сочетание клавиш для одобрения одним нажатием. Требуется Agent SDK v0.3.268 или новее |
| `suppressAlwaysAllowRule` | `boolean` | Если `true`, не предлагайте для этого запроса постоянный вариант «всегда разрешать». Требуется Agent SDK v0.3.268 или новее |
| `toolUseID` | `string` | Уникальный идентификатор этого конкретного вызова инструмента в сообщении ассистента |
| `agentID` | `string` | Если выполняется внутри субагента — ID субагента |
| `requestId` | `string` | `request_id` конверта `control_request`. `control_response`, который ваше приложение отправляет вне SDK, например подписанным HTTP POST, должен повторять это значение, чтобы процесс Claude Code мог сопоставить ответ с запросом |

Обычно callback-функция разрешает запрос, возвращая [`PermissionResult`](#permissionresult), который SDK записывает обратно через свой транспорт как `control_response`. Возвращайте `null` только тогда, когда ваше приложение уже отправило `control_response` для этого запроса по собственному каналу, повторив `requestId`; в этом случае SDK не записывает ответ в свой транспорт. Возврат `null` в любом другом случае оставляет вызов инструмента заблокированным на неопределённый срок, поскольку `control_response` так и не отправляется, а у запросов разрешений нет таймаута.

Параметр `requestId` и возвращаемое значение `null` требуют Claude Code v2.1.199 или новее.

### `PermissionResult`

Результат проверки разрешения.

```typescript theme={null}
type PermissionResult =
  | {
      behavior: "allow";
      updatedInput?: Record<string, unknown>;
      updatedPermissions?: PermissionUpdate[];
      toolUseID?: string;
    }
  | {
      behavior: "deny";
      message: string;
      interrupt?: boolean;
      toolUseID?: string;
    };
```

Если вы возвращаете `allow` с более чем 4 096 элементами в `updatedPermissions`, Claude Code считает результат недействительным и отклоняет вызов инструмента. Каждое обновление считается одним элементом, как и каждая запись в его списке `rules` или `directories`. Сообщение об отказе заканчивается на `updatedPermissions may hold at most 4096 updates, rules and directories in all.` Чтобы вызов был разрешён, возвращайте не более 4 096 элементов.

### `ToolConfig`

Конфигурация поведения встроенных инструментов.

```typescript theme={null}
type ToolConfig = {
  askUserQuestion?: {
    previewFormat?: "markdown" | "html";
  };
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `askUserQuestion.previewFormat` | `'markdown' \| 'html'` | Включает поле `preview` в вариантах [`AskUserQuestion`](https://code.claude.com/docs/ru/agent-sdk/user-input#question-format) и задаёт формат его содержимого. Если не задано, Claude не выводит превью |

### `McpServerConfig`

Конфигурация MCP-серверов.

```typescript theme={null}
type McpServerConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfigWithInstance;
```

#### `McpStdioServerConfig`

```typescript theme={null}
type McpStdioServerConfig = {
  type?: "stdio";
  command: string;
  args?: string[];
  env?: Record<string, string>;
};
```

#### `McpSSEServerConfig`

```typescript theme={null}
type McpSSEServerConfig = {
  type: "sse";
  url: string;
  headers?: Record<string, string>;
};
```

#### `McpHttpServerConfig`

```typescript theme={null}
type McpHttpServerConfig = {
  type: "http";
  url: string;
  headers?: Record<string, string>;
};
```

#### `McpSdkServerConfigWithInstance`

Конфигурация внутрипроцессного MCP-сервера. Это то, что возвращает [`createSdkMcpServer()`](#createsdkmcpserver), плюс необязательный список `tools` из добавляемых вами записей [`McpServerToolPolicy`](#mcpservertoolpolicy).

```typescript theme={null}
type McpSdkServerConfigWithInstance = {
  type: "sdk";
  name: string;
  timeout?: number;
  tools?: McpServerToolPolicy[];
  instance: McpServer;
};
```

Чтобы требовать подтверждения для вызовов одного из инструментов сервера или запрещать их, добавьте запись политики с именем инструмента. Разверните то, что возвращает `createSdkMcpServer()`, в объект внутри `mcpServers` и поместите запись в список `tools` этого объекта, потому что параметр `tools` функции принимает определения инструментов, а не записи политики. Список политик требует Agent SDK v0.3.301 или новее, а в [`McpServerToolPolicy`](#mcpservertoolpolicy) описано, что делает каждое значение `permission_policy`.

В этом скрипте подстановочный знак в `allowedTools` заранее одобряет все инструменты сервера `records`, но `delete_record` помечен как `always_ask`, поэтому вызовы к нему всё равно попадают в `canUseTool`. Благодаря аннотации `destructiveHint: true` вызов по-прежнему доходит до обратного вызова, если сессия работает в режиме `auto`, где иначе его мог бы одобрить [классификатор](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) авторежима.

```typescript theme={null}
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const deleteRecord = tool(
  "delete_record",
  "Delete a customer record by ID",
  { id: z.string() },
  async ({ id }) => ({ content: [{ type: "text", text: `Deleted record ${id}` }] }),
  { annotations: { destructiveHint: true } }
);

const records = createSdkMcpServer({ name: "records", tools: [deleteRecord] });

for await (const message of query({
  prompt: "Delete customer record 42",
  options: {
    mcpServers: {
      // Spread the returned config and add the policy list beside it
      records: {
        ...records,
        tools: [{ name: "delete_record", permission_policy: "always_ask" as const }]
      }
    },
    allowedTools: ["mcp__records__*"],
    canUseTool: async (toolName, input) => {
      console.log(`Approval requested for ${toolName}`);
      return { behavior: "allow", updatedInput: input };
    }
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

Когда Claude вызывает `delete_record`, скрипт выводит `Approval requested for mcp__records__delete_record`.

Чтобы изменить или снять политику инструмента во время работы сессии, передайте конфигурацию сервера с новым значением `tools` в [`setMcpServers()`](#mcpsetserversresult). Переданное значение `tools` вступает в силу со следующего вызова Claude к инструментам этого сервера:

* **Список с записями**: записи заменяют текущие политики
* **Пустой список**: все политики сервера очищаются
* **Нет ключа `tools`**: текущие политики сохраняются

Включите в этот вызов другие ваши внутрипроцессные серверы и любой сервер, добавленный предыдущим вызовом `setMcpServers()`, иначе вызов отключит их.

#### `McpServerToolPolicy`

Одна запись в списке `tools` конфигурации [`McpSdkServerConfigWithInstance`](#mcpsdkserverconfigwithinstance), которая называет один из инструментов сервера и задаёт политику разрешений для вызовов этого инструмента. Список требует Agent SDK v0.3.301 или новее и Claude Code v2.1.301 или новее. Более старый исполняемый файл Claude Code, например тот, на который вы указываете через `pathToClaudeCodeExecutable`, игнорирует список. В этом случае `always_ask` и `always_deny` не применяются, и каждый вызов проходит через [процесс оценки разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated).

```typescript theme={null}
type McpServerToolPolicy = {
  name: string;
  permission_policy?: "always_allow" | "always_ask" | "always_deny";
  org_max_permission?: "allow" | "ask" | "blocked";
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | `string` | Простое имя инструмента в том виде, в каком оно передано в [`tool()`](#tool), без префикса `mcp__<server>__` |
| `permission_policy` | `'always_allow' \| 'always_ask' \| 'always_deny'` | Политика подтверждения для вызовов инструмента: [`always_ask` или `always_deny`](#permission-policy-values). `always_allow` игнорируется на внутрипроцессном сервере: чтобы заранее одобрить инструмент, укажите его вместо этого в [`allowedTools`](#options) |
| `org_max_permission` | `'allow' \| 'ask' \| 'blocked'` | Потолок для отдельного инструмента, который задаёт администратор организации. Игнорируется на внутрипроцессном сервере, поэтому не задавайте его |

##### Значения `permission_policy`

Выберите `always_ask`, чтобы самостоятельно подтверждать каждый вызов, или `always_deny`, чтобы полностью заблокировать инструмент:

* **`always_ask`**: каждый вызов инструмента [требует подтверждения](https://code.claude.com/docs/ru/agent-sdk/permissions.md#how-permissions-are-evaluated), даже если его покрывает запись `allowedTools` или разрешающее правило. Вызов направляется в вашу callback-функцию `canUseTool` или инструмент [`permissionPromptToolName`](#options), если только он не будет решён раньше. [Мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) в загружаемом вами плагине [может одобрить его первым](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods). В остальных случаях в режиме `dontAsk` он отклоняется, а в [режимах `auto`, `plan` и `bypassPermissions`](#permission-modes-that-can-approve-an-always_ask-call) он может быть одобрен до того, как дойдёт до вашей callback-функции
* **`always_deny`**: Claude Code удаляет инструмент из контекста Claude в любом режиме разрешений, включая `bypassPermissions`. Удаление требует Claude Code v2.1.324 или новее

Если вы не передаёте ни `canUseTool`, ни `permissionPromptToolName` или устанавливаете [`permissionPrompts`](#options) в `'none'`, вызов `always_ask`, который не был решён раньше, отклоняется, если его не разрешит [хук `PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest).

##### Режимы разрешений, которые могут одобрить вызов `always_ask`

В режимах `auto`, `plan` и `bypassPermissions` вызов инструмента, помеченного [`always_ask`](#permission-policy-values), может быть одобрен до того, как достигнет вашего обратного вызова `canUseTool`.

* **`auto`**: [классификатор](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) авторежима проверяет вызов и может его разрешить. Чтобы каждый вызов доходил до вашей callback-функции в режиме `auto`, установите `destructiveHint: true` в [аннотациях](#toolannotations) инструмента
* **`plan`**: пока [авторежим доступен](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) для сессии, вызовы инструмента `always_ask` с аннотацией `readOnlyHint: true` направляются в классификатор авторежима, который может их разрешить. Вызовы других инструментов `always_ask` доходят до вашей callback-функции. Чтобы вызовы инструмента только для чтения тоже доходили до вашей callback-функции, добавьте `destructiveHint: true` в аннотации этого инструмента наряду с `readOnlyHint: true`. Либо установите [`useAutoModeDuringPlan`](https://code.claude.com/docs/ru/settings-reference#useautomodeduringplan) в `false`, что отключает классификатор во время планирования
* **`bypassPermissions`**: когда переменная окружения [`CLAUDE_CODE_REMOTE`](https://code.claude.com/docs/ru/env-vars#variables) равна `true`, как в [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md), вызов одобряется без вашей callback-функции, независимо от аннотаций инструмента. В любом другом месте вызов доходит до вашей callback-функции. Чтобы он доходил до вашей callback-функции и в облачной сессии, запускайте сессию вместо этого в режиме `default` или `acceptEdits`

В режимах `auto` и `plan` явно устанавливайте `destructiveHint` в `true`. Для вызовов `always_ask` Claude Code считает незаданный `destructiveHint` равным `false`, хотя значение по умолчанию, указанное в [`ToolAnnotations`](#toolannotations), — `true`.

#### `McpClaudeAIProxyServerConfig`

```typescript theme={null}
type McpClaudeAIProxyServerConfig = {
  type: "claudeai-proxy";
  url: string;
  id: string;
};
```

### `SdkPluginConfig`

Конфигурация для загрузки плагинов в SDK.

```typescript theme={null}
type SdkPluginConfig = {
  type: "local";
  path: string;
  skipMcpDiscovery?: boolean;
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `type` | `'local'` | Должно быть `'local'` (в настоящее время поддерживаются только локальные плагины) |
| `path` | `string` | Путь к каталогу плагина. Относительный путь разрешается относительно параметра [`cwd`](#options) при запуске сессии. Путь должен быть абсолютным, когда вы загружаете плагин во время сессии с помощью [`addPlugins`](#load-more-plugin-folders-with-addplugins) |
| `skipMcpDiscovery` | `boolean` | Если `true`, SDK загружает скиллы, хуки, агентов и команды из этого плагина, но не читает его `.mcp.json` или `mcpServers` из манифеста. Задайте этот параметр, если MCP-подключениями плагина управляет ваше приложение. |

**Пример:**

```typescript theme={null}
plugins: [
  { type: "local", path: "./my-plugin" },
  { type: "local", path: "/absolute/path/to/plugin" }
];
```

Полную информацию о создании и использовании плагинов см. в разделе [Плагины](https://code.claude.com/docs/ru/agent-sdk/plugins.md).

## Типы сообщений

### `SDKMessage`

Тип объединения всех возможных сообщений, возвращаемых запросом.

```typescript theme={null}
type SDKMessage =
  | SDKAssistantMessage
  | SDKUserMessage
  | SDKUserMessageReplay
  | SDKResultMessage
  | SDKSystemMessage
  | SDKPartialAssistantMessage
  | SDKCompactBoundaryMessage
  | SDKStatusMessage
  | SDKLocalCommandOutputMessage
  | SDKHookStartedMessage
  | SDKHookProgressMessage
  | SDKHookResponseMessage
  | SDKPluginInstallMessage
  | SDKToolProgressMessage
  | SDKAuthStatusMessage
  | SDKTaskNotificationMessage
  | SDKTaskStartedMessage
  | SDKTaskProgressMessage
  | SDKTaskUpdatedMessage
  | SDKBackgroundTasksChangedMessage
  | SDKThinkingTokensMessage
  | SDKSessionStateChangedMessage
  | SDKWorkerShuttingDownMessage
  | SDKCommandsChangedMessage
  | SDKNotificationMessage
  | SDKFilesPersistedEvent
  | SDKToolUseSummaryMessage
  | SDKMemoryRecallMessage
  | SDKRateLimitEvent
  | SDKElicitationCompleteMessage
  | SDKPermissionDeniedMessage
  | SDKPromptSuggestionMessage
  | SDKAPIRetryMessage
  | SDKControlRequestProgressMessage
  | SDKModelRefusalFallbackMessage
  | SDKModelRefusalNoFallbackMessage
  | SDKMirrorErrorMessage
  | SDKInformationalMessage
  | SDKConversationResetMessage;
```

Три сообщения в этом объединении сообщают о ходе управляющих запросов и об отказах модели. У каждого из них `type: "system"`, поэтому различайте их по `subtype`, указанному для каждого:

* `SDKControlRequestProgressMessage`, `subtype: "control_request_progress"`: сообщает о ходе выполнения длительного управляющего запроса, отправленного вашим клиентом. `request_id` связывает сообщение с этим запросом, а `status` равен `"started"` или `"api_retry"`. Требуется Agent SDK v0.3.203 или новее.
* `SDKModelRefusalFallbackMessage`, `subtype: "model_refusal_fallback"`: отправляется, когда модель завершает поток отказом и ход повторяется на резервной модели. Содержит `original_model` и `fallback_model`. Требуется Agent SDK v0.3.170 или новее.
* `SDKModelRefusalNoFallbackMessage`, `subtype: "model_refusal_no_fallback"`: отправляется, когда модель завершает поток отказом и повторная попытка не выполняется, например потому что резервная модель не настроена. Содержит `original_model`. Требуется Agent SDK v0.3.193 или новее.

### `SDKAssistantMessage`

Сообщение ответа ассистента.

```typescript theme={null}
type SDKAssistantMessage = {
  type: "assistant";
  uuid: UUID;
  session_id: string;
  message: BetaMessage; // From Anthropic SDK
  parent_tool_use_id: string | null;
  error?: SDKAssistantMessageError;
  aborted?: true;
  agent_id?: string;
  timestamp?: string;
  context_usage?: SDKContextUsage;
  usage_report?: SDKUsageReport;
  user_message_uuid?: string;
  user_message_uuids?: string[];
  resume_reason?: string;
  supersedes?: UUID[];
};
```

Поле `message` — это [`BetaMessage`](https://platform.claude.com/docs/en/api/messages/create) из Anthropic SDK. Оно включает поля, такие как `id`, `content`, `model`, `stop_reason` и `usage`.

`SDKAssistantMessageError` — это одно из следующих значений: `'authentication_failed'`, `'oauth_org_not_allowed'`, `'account_on_hold'`, `'billing_error'`, `'rate_limit'`, `'overloaded'`, `'invalid_request'`, `'model_not_found'`, `'server_error'`, `'max_output_tokens'`, `'cloud_credential_error'` или `'unknown'`. Четыре из этих значений означают больше, чем говорят их названия:

* `'model_not_found'`: выбранная модель не существует или недоступна для вашей учётной записи или развёртывания
* `'overloaded'`: появляется в [событиях `api_retry`](https://code.claude.com/docs/ru/headless#handle-api-retries), когда API возвращает 529, потому что сервер перегружен. Когда HTTP 529 завершает ход, сообщение ассистента содержит `'server_error'`. Ответ 429 из-за исчерпания вашей квоты — это `'rate_limit'`
* `'account_on_hold'`: [ваша учётная запись заморожена](https://code.claude.com/docs/ru/errors.md#your-account-is-on-hold)
* `'cloud_credential_error'`: Claude Code не смог получить пригодные учётные данные AWS или Google Cloud на машине, на которой он работает, поэтому запрос не достиг поставщика облачных услуг. Обычная причина — истёкший или никогда не завершённый вход в облако на этой машине, хотя временно недоступный сервис учётных данных сообщает то же значение. См. [Could not load AWS or Google Cloud credentials](https://code.claude.com/docs/ru/errors.md#could-not-load-aws-or-google-cloud-credentials). Требует TypeScript Agent SDK v0.3.267 или позже, который включает Claude Code v2.1.267

`aborted` имеет значение `true`, когда прерывание или отмена усекли сообщение ассистента до завершения потока: сообщение не имеет `stop_reason`, и содержимое может заканчиваться посередине слова. Это поле отсутствует в нормально завершённых сообщениях. Требует Agent SDK v0.3.214 или позже.

`supersedes` перечисляет UUID более ранних сообщений, которые заменяет это сообщение. Удаляйте эти сообщения из отображения, когда приходит это сообщение.

`agent_id` идентифицирует субагента, создавшего сообщение, и отсутствует у сообщений основного потока. Значение совпадает с `task_id` в событии [`task_started`](#sdktaskstartedmessage) и других событиях задачи этого субагента и не меняется, когда субагент [возобновляется](https://code.claude.com/docs/ru/agent-sdk/subagents.md#resume-subagents). В сообщениях от [вложенного субагента](https://code.claude.com/docs/ru/sub-agents.md#let-subagents-spawn-their-own-subagents) оно указывает на вложенного субагента, а не на субагента, который его запустил. Поле требует Agent SDK v0.3.292 или новее.

Сопоставляйте сообщения субагента с событиями его задачи по `agent_id`, а не по паре `parent_tool_use_id` сообщения и `tool_use_id` события задачи. Когда вызов инструмента возобновляет субагента, события задачи несут `tool_use_id` этого вызова, а сообщения сохраняют `parent_tool_use_id` вызова инструмента, который впервые запустил субагента, поэтому эти значения перестают совпадать.

Claude Code задаёт `user_message_uuid` и `user_message_uuids` в первом сообщении ассистента в ходе при условиях, описанных в [`user_message_uuid`](#user_message_uuid). Когда ход продолжает другой ход, прерванный перезапуском, сообщения ассистента, несущие эти поля, несут также [`resume_reason`](#resume_reason).

`timestamp` — это время в формате ISO 8601, когда содержимое сообщения закончило генерироваться в процессе, который его создал. Значение берётся с часов этой машины, поэтому используйте его только для отображения и не упорядочивайте сообщения по нему. Один ход API может создать несколько сообщений ассистента с одинаковым `message.id`, каждое со своим `timestamp`. Когда это поле отсутствует, используйте время получения сообщения.

`context_usage` — это структурированная копия отчёта `/context`, типизированная как [`SDKContextUsage`](#sdkcontextusage); требует Agent SDK v0.3.232 или позже. Когда вы отправляете `/context` как промпт, Claude Code доставляет отчёт как сообщение ассистента, чьё `message.content` содержит таблицу markdown, и прикрепляет `context_usage` к этому же сообщению. Claude Code не устанавливает это поле ни в каком другом сообщении ассистента, а более ранние версии доставляют таблицу `/context` без него, поэтому читайте разбивку из поля, когда оно присутствует, и используйте текст markdown, когда его нет.

`usage_report` — структурированная копия отчёта `/usage` с типом [`SDKUsageReport`](#sdkusagereport); требуется Agent SDK v0.3.273 или новее. Когда вы отправляете `/usage` в качестве промпта, Claude Code доставляет отчёт как сообщение ассистента, у которого `message.content` содержит текст. Он прикрепляет `usage_report` к этому же сообщению, только если сессия удовлетворяет всем следующим условиям:

* Сессия аутентифицируется с помощью учётных данных claude.ai
* Учётные данные указывают известный тип тарифа или содержат scope `user:profile`
* Учётная запись не находится на биллинге по фактическому использованию

Токен `claude setup-token`, переданный как `CLAUDE_CODE_OAUTH_TOKEN`, по умолчанию не подходит, потому что содержит только scope `user:inference`. Другие сессии, например сессии с API-ключом, доставляют текст без этого поля, как и более ранние версии. Читайте отчёт из поля, когда оно есть, и используйте текст, когда его нет.

### `SDKUserMessage`

Сообщение пользовательского ввода.

```typescript theme={null}
type SDKUserMessage = {
  type: "user";
  uuid?: UUID;
  session_id?: string;
  agent_id?: string;
  message: MessageParam; // From Anthropic SDK
  pasted_content?: MessageParam["content"][];
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  shouldQuery?: boolean;
  client_composed?: true;
  tool_use_result?: unknown;
  priority?: "now" | "next" | "later";
  origin?: SDKMessageOrigin;
  inline_pastes?: string[];
};
```

Установите `pasted_content` для отправки содержимого, которое пользователь вставил в ваш интерфейс ввода промпта, а не напечатал, — одна запись на вставку, каждая является строкой или массивом блоков содержимого. Claude Code добавляет текст каждой записи после напечатанного текста по порядку и может обернуть каждую вставку в теги `<pasted_content>`. Блоки, отличные от текста, игнорируются, поэтому отправляйте изображения и документы в `message.content`. Требует Agent SDK v0.3.277 или позже.

Задайте `inline_pastes`, чтобы сообщить Claude Code, какие части `message.content` пользователь вставил, а не набрал, — по одной строке на каждую вставку. Текст промпта остаётся там, где его поместил пользователь. Claude Code может обернуть каждую перечисленную вставку в теги `<pasted_content>` на её месте, чтобы Claude мог отличить вставленный материал от собственных слов пользователя. Оборачиваются только вставки в последнем текстовом блоке промпта. Требуется TypeScript Agent SDK v0.3.280 или новее.

У каждого поля вставки есть ограничение размера:

* `pasted_content`: если записей вместе с блоками содержимого внутри них больше 1000, Claude Code игнорирует всё поле.
* `inline_pastes`: Claude Code использует первые 100 непустых записей и игнорирует остальные.

Задайте `shouldQuery`, `client_composed` или `priority`, чтобы изменить то, как Claude Code обрабатывает отправленное вами сообщение:

* `shouldQuery`: установите его в `false`, чтобы добавить сообщение в транскрипт без запуска хода ассистента. Сообщение удерживается и объединяется со следующим пользовательским сообщением, которое запускает ход. Используйте это для внедрения контекста, например вывода команды, которую вы запустили вне основного канала, не тратя на это вызов модели.
* `client_composed`: установите значение `true`, чтобы Claude Code доставил текст сообщения в том виде, в каком он написан. Тогда Claude Code не раскрывает упоминания `@path` и не выполняет как команду текст, начинающийся с `/`. Пока включён параметр [`verbatimPrompts`](#options), SDK устанавливает это поле в каждом сообщении. Требуется TypeScript Agent SDK v0.3.280 или новее и Claude Code v2.1.248 или новее.
* `priority`: управляет тем, когда сообщение, отправленное вами во время выполняющегося хода, доходит до Claude:
  * `'next'` или отсутствие поля `priority`: Claude читает сообщение в том же ходе, как только завершатся выполняемые вызовы инструментов. Если ход завершится раньше, сообщение начинает следующий ход.
  * `'later'`: Claude Code удерживает сообщение до завершения хода и отправляет его как новый ход.
  * `'now'` с [`origin: { kind: "human" }`](#sdkmessageorigin): в Claude Code v2.1.286 или новее работа, которая может продолжаться в фоне, переносится туда, и Claude читает сообщение в том же ходе. К переносимой работе относятся shell-команды, субагенты и вызовы инструментов MCP. В v2.1.287 или новее к ней также относятся вызовы WebFetch и WebSearch. Когда Claude только пишет ответ или выполняемую им работу нельзя перенести, Claude Code вместо этого прерывает ход, и Claude читает сообщение следующим.
  * `'now'` без такого origin: Claude Code прерывает ход, и Claude читает сообщение следующим.

Это сообщение, отправленное во время выполняющегося хода, просит Claude сменить направление, не теряя shell-команду, которая всё ещё выполняется:

```typescript theme={null}
const message: SDKUserMessage = {
  type: "user",
  message: { role: "user", content: "Skip the integration tests and summarize what you have so far" },
  parent_tool_use_id: null,
  priority: "now",
  origin: { kind: "human" },
};
```

Пользовательское сообщение, созданное субагентом, например `tool_result` для одного из его собственных вызовов инструментов, содержит `agent_id`. См. [`SDKAssistantMessage`](#sdkassistantmessage), где определены это поле и требования к версии.

В сообщении, содержащем блок `tool_result`, `tool_use_result` — это структурированный объект вывода инструмента, а не текст, отправленный модели. Его форма зависит от инструмента, указанного в соответствующем блоке `tool_use`, поэтому поле имеет тип `unknown`; встроенные формы перечислены в разделе [Типы вывода инструментов](#tool-output-types). Следующие результаты требуют обработки помимо их указанной формы:

* Инструмент `Agent`: `tool_use_result` имеет тип [`AgentOutput`](#agent-2). Отображайте результат на его основе, а не разбирая текст `tool_result`. Поле `content` результата `completed` содержит отчёт субагента или — для субагента, чей отчёт передаётся через вызов инструмента `SubagentHandback`, — короткую заметку об этой передаче вместо отчёта. В [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) в Claude Code v2.1.271 или новее каждый субагент, выдающий результат `completed`, отчитывается таким образом, если только он не является [форком](https://code.claude.com/docs/ru/sub-agents.md#fork-the-current-conversation), и Claude получает отчёт отдельным сообщением от субагента.
* Вызов WebFetch или WebSearch, который Claude Code перенёс в фон, чтобы доставить сообщение `'now'`: в пользовательском сообщении, содержащем `tool_result` этого вызова, `tool_use_result` имеет значение `{ detachedToolCall: true }`. Вызов всё ещё выполняется, и Claude получит его результат после завершения. Второго `tool_result` для этого `tool_use_id` не последует, поэтому, если ваше приложение отображает строку для каждого вызова инструмента, пометьте эту строку как перенесённую в фон при получении этого сообщения. Требуется Claude Code v2.1.287 или новее.
* Инструмент MCP, результат которого содержит блоки `resource_link`: `tool_use_result` — объект с массивом `resourceLinks` из записей [`SDKMcpResourceLink`](#sdkmcpresourcelink). Claude получает каждую ссылку в виде строки текста в блоке `tool_result`, поэтому считывайте `resourceLinks`, чтобы отобразить файлы, возвращённые сервером, вместо разбора этого текста. Claude Code опускает `resourceLinks`, когда в результате нет ссылок, а также в результатах от субагентов, хранит не более 50 ссылок на результат и прекращает добавлять ссылки, когда массив достигает 64 КиБ сериализованного JSON. Для `resourceLinks` требуется Agent SDK v0.3.257 или новее.
* Инструмент MCP, возвращающий [`structuredContent`](#calltoolresult): `tool_use_result` — объект, член `structuredContent` которого содержит то, что отправил сервер, а член `content` — значение [`McpOutput`](#mcpoutput). Результаты от субагентов не содержат `structuredContent`.
* Инструмент MCP, чей `structuredContent` сериализуется в JSON длиной более 1 048 576 символов: Claude Code не включает `structuredContent` в `tool_use_result` и устанавливает вместо него `structuredContentOmitted: true`, чтобы ваше приложение могло отличить отброшенный объект от инструмента, который его не отправлял. Остальные члены, такие как `content` и `resourceLinks`, остаются, и то, что получает Claude, не меняется. Это ограничение применяет Claude Code v2.1.287 или новее. Два вида инструментов отличаются:
  * Инструменты из [внутрипроцессных серверов SDK](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md) освобождены от ограничения и доставляют объект целиком.
  * Инструмент, чья запись в `tools/list` объявляет [ресурс MCP Apps `ui://`](#mcpserverstatus), имеет ограничение в 8 388 608 символов в Claude Code v2.1.295 или новее, а версии до v2.1.295 освобождают его от ограничения.

### `SDKUserMessageReplay`

Воспроизведённое пользовательское сообщение с обязательным UUID.

```typescript theme={null}
type SDKUserMessageReplay = {
  type: "user";
  uuid: UUID;
  session_id: string;
  message: MessageParam;
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  client_composed?: true;
  tool_use_result?: unknown;
  origin?: SDKMessageOrigin;
  isReplay: true;
};
```

Пользовательский ход, внедрённый извне сессии, то есть такой, чей [`origin`](#sdkmessageorigin) имеет вид `peer` или `channel`, поступает в поток как воспроизведение независимо от того, был ли он доставлен во время активного хода или запустил новый ход, пока сессия была неактивна. До v2.1.207 внедрённый ход, доставленный, пока сессия была неактивна, не создавал сообщения в потоке и появлялся только при повторном чтении транскрипта.

### `SDKResultMessage`

Финальное сообщение результата.

```typescript theme={null}
type SDKResultMessage =
  | {
      type: "result";
      subtype: "success";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      api_error_status?: number | null;
      num_turns: number;
      result: string;
      stop_reason: string | null;
      ttft_ms?: number;
      ttft_stream_ms?: number;
      time_to_request_ms?: number;
      user_message_uuid?: string;
      user_message_uuids?: string[];
      resume_reason?: string;
      local_command?: string;
      request_sent_wall_ms?: number;
      first_content_frame_ms?: number;
      first_stream_post_ms?: number;
      first_stream_post_ack_ms?: number;
      first_stream_post_queue_wait_ms?: number;
      first_stream_post_queued_behind?: "durable_post" | "ephemeral_post" | "retry_backoff" | "hold" | "none";
      first_stream_post_wall_ms?: number;
      first_text_post_ms?: number;
      first_text_post_queue_wait_ms?: number;
      first_text_post_queued_behind?: "durable_post" | "ephemeral_post" | "retry_backoff" | "hold" | "none";
      first_text_post_wall_ms?: number;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      queued_turn_count?: number;
      structured_output?: unknown;
      deferred_tool_use?: { id: string; name: string; input: Record<string, unknown> };
      terminal_reason?: TerminalReason;
      result_index?: number;
      fast_mode_state?: FastModeState;
      fast_mode_disabled_reason?: FastModeDisabledReason;
      origin?: SDKMessageOrigin;
    }
  | {
      type: "result";
      subtype:
        | "error_max_turns"
        | "error_during_execution"
        | "error_max_budget_usd"
        | "error_max_structured_output_retries";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      stop_reason: string | null;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      queued_turn_count?: number;
      errors: string[];
      startup_failure_reason?: SDKStartupFailureReason;
      user_message_uuid?: string;
      user_message_uuids?: string[];
      resume_reason?: string;
      terminal_reason?: TerminalReason;
      result_index?: number;
      fast_mode_state?: FastModeState;
      fast_mode_disabled_reason?: FastModeDisabledReason;
      origin?: SDKMessageOrigin;
    };
```

Несколько полей в результате содержат диагностические детали, выходящие за рамки `subtype`:

* `api_error_status`: код состояния HTTP ошибки API, которая завершила диалог. Отсутствует или равен `null`, когда ход завершился без ошибки API.
* `ttft_ms`: время до первого токена в миллисекундах, измеренное при поступлении первого полного сообщения ассистента. Присутствует только в ветви успеха.
* `ttft_stream_ms`: время в миллисекундах до первого события потока `message_start`, когда открывается поток ответа. Меньше, чем `ttft_ms`; разница между ними — это время, потраченное на потоковую передачу первого сообщения. Присутствует только в ветви успеха.
* `time_to_request_ms`: время в миллисекундах от начала хода до отправки Claude Code запроса к API. Присутствует только в варианте успеха. Требуется Claude Code v2.1.162 или новее.
* `user_message_uuid`: `uuid` отправленного вами сообщения, на которое ответил этот ход. См. [`user_message_uuid`](#user_message_uuid), чтобы узнать, какие результаты его содержат.
* `user_message_uuids`: `uuid` каждого отправленного вами сообщения, на которое Claude Code ответил в этом ходе. См. [`user_message_uuids`](#user_message_uuids).
* `resume_reason`: причина, по которой этот ход продолжает ход, прерванный перезапуском. Присутствует в обеих ветвях. См. [`resume_reason`](#resume_reason).
* `local_command`: имя команды, которую выполнил ход, в результате успеха хода, завершённого командой без входа в цикл агента, например `/compact`. Имя приводится к строчным буквам и подчёркиваниям, поэтому `/reload-plugins` сообщает `reload_plugins`. Команда, которую предоставляет MCP-сервер, и встроенная `/mcp` сообщают `mcp`. Команда, которую вы определили сами, сообщает `custom`. Аргументы никогда не включаются. Отсутствует в каждом ходе, который вошёл в цикл агента, и при отправках, не запустивших команду. Требует Agent SDK v0.3.268 или позже.
* `request_sent_wall_ms`: миллисекунды эпохи, в которые Claude Code отправил запрос API, для сопоставления с серверными временными метками. Присутствует только вместе с [`user_message_uuid`](#user_message_uuid), в результате успеха с `is_error` равным false, чей ход отправил запрос API.
* `first_content_frame_ms`: время в миллисекундах до первого события потока `content_block_start` или `content_block_delta`, считая блоки размышлений содержимым. Присутствует только в ветви успеха, когда `is_error` имеет значение false. Требует Agent SDK v0.3.260 или позже.
* `first_stream_post_ms`, `first_stream_post_ack_ms`, `first_stream_post_wall_ms`: тайминги загрузки первого события потока хода. Claude Code записывает их только в сессиях, которые он транслирует на claude.ai, например в [облачных сессиях](https://code.claude.com/docs/ru/claude-code-on-the-web.md), и результаты, которые выдаёт `query()`, их не содержат. Требует Agent SDK v0.3.260 или позже.
* `usage`: только основной цикл агента. Исключает вызовы субагентов и вспомогательных моделей и в сессиях с потоковым вводом считается за ход. Для учёта токенов и затрат предпочитайте `modelUsage`.
* `modelUsage`: итоги по моделям для каждого вызова модели, сделанного через конвейер запросов во время этого вызова `query()`, включая основной цикл, субагентов и внутренние вызовы, такие как сжатие контекста и агенты Workflow. Вспомогательные вызовы вне этого конвейера, такие как классификатор разрешений и запросы подсчёта токенов, исключены. Вызов, который возобновляет сессию, также учитывает [итоги по моделям, восстановленные из более ранних вызовов сессии](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#accumulate-costs-across-multiple-calls). В сессиях с потоковым вводом итоги накапливаются по ходам, поэтому читайте последний результат, а не суммируйте по результатам. См. [Отслеживание затрат в режиме потоковой передачи входных данных](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#track-costs-in-streaming-input-mode) о сбросах и [Восстановление итогов после сбоя сеанса](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#recover-totals-after-a-session-crash) об обнулённых результатах.
* `total_cost_usd`: кумулятивная оценочная стоимость в USD, охватывающая те же вызовы, что и `modelUsage`, и сбрасываемая в тех же точках. Вызов, который возобновляет сессию, также учитывает [итоги, восстановленные из более ранних вызовов сессии](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#accumulate-costs-across-multiple-calls). Это оценка, а не выписка по счёту. См. [Отслеживание затрат и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md) о предостережениях по точности.
* `queued_turn_count`: количество отправленных вами сообщений с `origin: { kind: "human" }`, которые всё ещё ожидают, когда Claude Code создал результат. См. [`queued_turn_count`](#queued_turn_count), чтобы узнать, что означают `0` и отсутствующее поле.
* `result_index`: позиция этого результата в порядке доставки запуска, считая от 0 по всем результатам, которые записывает процесс. Присутствует в обеих ветвях. Результат, запись которого не удалась, всё равно занимает свой номер, поэтому разрыв в последовательности означает, что результат был потерян. Требует Agent SDK v0.3.268 или позже.
* `startup_failure_reason`: почему Claude Code отказался запускаться, в результате `error_during_execution`, который он записывает перед выходом при известной ошибке запуска. См. [`startup_failure_reason`](#startup_failure_reason) о значениях и о том, какие ошибки его содержат. Требует Agent SDK v0.3.274 или позже.
* `terminal_reason`: почему цикл завершился. Одно из значений: `"completed"`, `"max_turns"`, `"tool_deferred"`, `"aborted_streaming"`, `"aborted_tools"`, `"hook_stopped"`, `"stop_hook_prevented"`, `"background_requested"`, `"blocking_limit"`, `"rapid_refill_breaker"`, `"prompt_too_long"`, `"image_error"`, `"model_error"`, `"api_error"`, `"malformed_tool_use_exhausted"`, `"budget_exhausted"`, `"structured_output_retry_exhausted"`, `"tool_deferred_unavailable"` или `"turn_setup_failed"`.
* `fast_mode_state`: одно из значений `"on"`, `"off"` или `"cooldown"`.
* `fast_mode_disabled_reason`: почему [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) сейчас недоступен. Отсутствует, когда ничто не блокирует быстрый режим, хотя запрос всё равно может выполняться на стандартной скорости. Во время периода охлаждения после ограничения частоты запросов быстрого режима Claude Code сообщает `fast_mode_state: "cooldown"` без кода причины и повторно включает быстрый режим, когда период охлаждения истекает. Требует Claude Code v2.1.219 или позже.

Используйте код причины, чтобы объяснить в вашем собственном интерфейсе, почему быстрый режим отключён, вместо того чтобы заново определять доступность. Каждый код называет проверку, которая заблокировала быстрый режим:

| Код причины | Значение |
| - | - |
| `free` | Учётная запись не имеет платной подписки или кредитов использования, которые требует быстрый режим |
| `preference` | Организация отключила быстрый режим |
| `extra_usage_disabled` | Кредиты использования отключены для учётной записи |
| `network_error` | [Проверка доступности](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-behind-proxies-and-llm-gateways) не смогла связаться с `api.anthropic.com` |
| `unknown` | Claude Code не смог определить доступность |
| `not_first_party` | Сессия использует провайдера, который не предлагает быстрый режим |
| `disabled_by_env` | Установлена переменная [`CLAUDE_CODE_DISABLE_FAST_MODE`](https://code.claude.com/docs/ru/env-vars) или регион модели в [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-on-agent-platform) не предлагает быстрый режим |
| `model_not_allowed` | Модель быстрого режима отсутствует в списке разрешённых моделей [`availableModels`](https://code.claude.com/docs/ru/model-config#restrict-model-selection) организации или провайдер отказал в быстром режиме для модели сессии |
| `sdk_opt_in_required` | Сессия не включила быстрый режим: передайте `fastMode: true` в опции [`settings`](#options) или через [`applyFlagSettings()`](#applyflagsettings) |
| `pending` | Проверка доступности ещё не завершена |

Та же пара полей присутствует в [`SDKSystemMessage`](#sdksystemmessage) и в [`SDKControlInitializeResponse`](#sdkcontrolinitializeresponse), поэтому вы можете прочитать состояние быстрого режима перед первым ходом.

Поле `origin` содержит [`SDKMessageOrigin`](#sdkmessageorigin), который Claude Code назначил сообщению пользователя, вызвавшему этот результат, а не копию отправленного вами `origin`. К результатам с `origin: { kind: "task-notification" }` относятся:

* **Синтетические последующие ходы**: когда SDK внедряет синтетический последующий ход, например для завершившейся фоновой задачи, итоговый `SDKResultMessage` несёт этот вид
* **Сработавшие запланированные задачи и сообщения из других сессий**: облачные запланированные задачи, чей триггер сработал, и проверенные сервером сообщения из ваших других сессий также приходят с этим видом, каждый с `subkind`, описанным в разделе [Подвиды task-notification](#task-notification-subkinds)

Проверяйте `kind`, чтобы отличить результаты, отвечающие на ваш промпт, от внедрённых последующих ходов, прежде чем маршрутизировать или скрывать их. Если ваше приложение [объявляет запланированные запуски](#declare-a-scheduled-run), их результаты тоже несут `kind: "task-notification"`, поэтому не скрывайте результаты только на основании `kind`.

Когда несколько завершений фоновых задач ставятся в очередь вместе, Claude Code может ответить на них в одном ходе, а не в отдельном ходе для каждого. Каждое завершение всё равно создаёт свой результат с этим происхождением. Все завершения, на которые Claude Code отвечает вместе, кроме последнего, по порядку создают пустые результаты с `num_turns: 0`, а результат последнего содержит ход, который отвечает на них все.

`origin` отсутствует, когда Claude Code его не назначил, например:

* В ходе, который вы начинаете сообщением без `origin` и без [`isSynthetic`](#sdkusermessage)
* В результатах, отправленных до любого хода пользователя, например при ошибках запуска

Когда хук `PreToolUse` возвращает `permissionDecision: "defer"`, результат имеет `stop_reason: "tool_deferred"`, а `deferred_tool_use` содержит `id`, `name` и `input` ожидающего инструмента. Читайте это поле, чтобы показать запрос в вашем собственном интерфейсе, затем возобновите работу с тем же `session_id`, чтобы продолжить. См. [Defer a tool call for later](https://code.claude.com/docs/ru/hooks.md#defer-a-tool-call-for-later) о полном цикле.

#### `user_message_uuid`

`uuid` [`SDKUserMessage`](#sdkusermessage), на которое отвечает ход, возвращаемый обратно, чтобы вы могли сопоставить ответ Claude Code с отправленным вами сообщением. Claude Code возвращает `uuid`, только если вы установили его в сообщении. Это поле необязательно в `SDKUserMessage`, а строковый промпт, переданный в `query()`, его не содержит.

На какое из ваших сообщений отвечает ход, зависит от того, как ход начался:

* **Обычное отправленное вами сообщение**, то есть без `isSynthetic: true`: ход отвечает на это сообщение на протяжении всего своего выполнения. Когда вы отправляете несколько сообщений почти одновременно, Claude Code может объединить их в один ход, и тогда поле содержит только `uuid` последнего сообщения. Чтобы сопоставить ответ с любым из объединённых сообщений, используйте [`user_message_uuids`](#user_message_uuids).
* **Сообщение, отправленное вами с `isSynthetic: true`**: ход сначала отвечает на это сообщение. Если Claude Code подхватит ваше обычное сообщение между вызовами инструментов, с этого момента ход отвечает на подхваченное сообщение. Возврат `uuid` синтетического сообщения требует Agent SDK v0.3.265 или позже; более ранние версии ничего не возвращают в синтетических ходах.
* **Промпт, который Claude Code генерирует для продолжения прерванного хода при [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](https://code.claude.com/docs/ru/env-vars)**: когда последний промпт прерванного хода — это обычное отправленное вами сообщение, открыло ли оно ход или Claude Code подхватил его во время хода, продолжающий ход сначала отвечает на это сообщение. [`resume_reason`](#resume_reason) позволяет отличить фреймы продолжающего хода от фреймов прерванной попытки. Когда последний промпт не является вашим обычным сообщением, продолжающий ход сначала не отвечает ни на одно ваше сообщение. Если Claude Code подхватывает ваше обычное сообщение между вызовами инструментов, с этого момента ход отвечает на подхваченное сообщение. Возврат промпта прерванного хода требует Agent SDK v0.3.268 или новее.
* **Любой другой промпт, который Claude Code сгенерировал сам**: ход сначала не отвечает ни на одно ваше сообщение, и его кадры не содержат возвращаемого значения. Если Claude Code подхватит ваше обычное сообщение между вызовами инструментов, с этого момента ход отвечает на это сообщение. Возврат при подхвате требует Agent SDK v0.3.265 или позже; более ранние версии ничего не возвращают в этих ходах.

Claude Code возвращает `uuid` сообщения, на которое дан ответ, в трёх видах кадров:

* **Результат**: каждый результат хода, который ответил на отправленное вами сообщение. В Agent SDK v0.3.265 или позже его содержит каждый такой результат. До v0.3.265 результат успеха хода, запущенного обычным сообщением, не содержал его, когда ход не отправил запрос API или завершился отложенным вызовом инструмента. До v0.3.246 его не содержали и результаты ошибок, а до v0.3.216 — все результаты.
* **Первый ответ хода**: первое [сообщение ассистента](#sdkassistantmessage), а при `includePartialMessages` также первое [событие потока](#sdkpartialassistantmessage), чей `event.type` не является `ping`, чтобы вы могли привязать ответ до поступления результата. Возврат в первом ответе требует Agent SDK v0.3.246 или позже. До v0.3.269 при `includePartialMessages` Claude Code устанавливал его только в этом первом событии потока или в первом сообщении ассистента, если ход ничего не передавал потоком. Когда сообщение, на которое отвечает ход, меняется посреди хода, первый ответ после изменения также содержит это поле в Agent SDK v0.3.265 или позже; более ранние версии устанавливают его в одном кадре ответа за ход.
* **Каждый кадр [`thinking_tokens`](#sdkthinkingtokensmessage) хода**: чтобы вы могли отнести прогресс размышлений к отправленному вами сообщению, не дожидаясь первого ответа хода. Требует Agent SDK v0.3.260 или позже.

Claude Code опускает это поле в следующих случаях:

* Кадры ответа, кроме этих первых ответов
* Кадры субагентов
* Ходы, которые не отвечают ни на одно ваше сообщение или отвечают на сообщение, отправленное вами без `uuid`
* Результаты, которые не отвечают ни на одно ваше сообщение, например обнулённый результат после сбоя рабочего процесса

Когда хук [`UserPromptSubmit`](https://code.claude.com/docs/ru/hooks#userpromptsubmit) блокирует сообщение, которое начинает собственный ход, или останавливает его с помощью `continue: false`, вы всё равно получаете результат для этого сообщения. Это успешный результат с `is_error: false` и `num_turns: 0`, его `result` — это [сообщение о блокировке](https://code.claude.com/docs/ru/hooks.md#what-a-blocked-prompt-leaves-behind) или [сообщение об остановке](https://code.claude.com/docs/ru/hooks.md#json-output), и он возвращает `uuid` сообщения по тем же правилам, что и любой другой результат. У результата нет `terminal_reason`, и ничто в нём, кроме текста `result`, не указывает, что ход завершил хук. Сообщение, которое хук блокирует во время выполнения другого хода, может не получить результата: см. [`user_message_uuids`](#user_message_uuids).

#### `user_message_uuids`

`uuid` каждого отправленного вами сообщения, на которое Claude Code ответил в этом ходе. Когда вы отправляете несколько сообщений почти одновременно, Claude Code может объединить их в один ход, и тогда `user_message_uuid` называет только последнее из них. Чтобы сопоставить ответ с любым из объединённых сообщений, ищите `uuid` этого сообщения в любом месте этого списка. Требует Agent SDK v0.3.259 или позже.

Claude Code устанавливает список вместе с `user_message_uuid` в каждом кадре ответа, который содержит это поле, и в результате. Полный набор кадров хода, которые возвращают `uuid` сообщения, на которое дан ответ, и требуемую для каждого версию см. в [`user_message_uuid`](#user_message_uuid). Список всегда содержит `user_message_uuid` и включает не более 64 записей.

Когда Claude Code подхватывает обычное сообщение, отправленное вами во время выполнения хода, он добавляет `uuid` этого сообщения в список результата. Когда хук [`UserPromptSubmit`](https://code.claude.com/docs/ru/hooks#userpromptsubmit) блокирует сообщение при подхвате, Claude Code вместо этого отбрасывает его: сообщение никогда не доходит до Claude и не сохраняется для последующего хода. Вы не получаете для него результата, и его `uuid` не появляется ни в одном списке результатов. Если хук может блокировать сообщения, задайте таймаут ожидания результата, который перечисляет сообщение, отправленное вами во время выполнения хода.

Это справедливо, когда вывод хука — только блокировка. Если вывод устанавливает `continue: false`, даже рядом с `decision: "block"`, или хук является промпт-хуком, который отвечает [`ok: false`](https://code.claude.com/docs/ru/hooks#response-schema) без `continueOnBlock: true`, Claude Code останавливает сообщение, а не отбрасывает его. Сообщение ждёт собственного хода, вы получаете для него результат, а его текст остаётся в диалоге, поэтому Claude видит его в следующем ходе.

Если первый ответ или результат содержит `user_message_uuid` без списка, он получен от более ранней версии Claude Code, поэтому используйте одиночное поле.

#### `resume_reason`

Причина, по которой этот ход продолжает ход, прерванный перезапуском. Claude Code задаёт это поле в ходе, продолжающем прерванный ход при [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](https://code.claude.com/docs/ru/env-vars), чтобы вы могли отличить ответ и результат продолжающего хода от ответа и результата прерванной попытки. Требуется Agent SDK v0.3.268 или новее.

Claude Code устанавливает это поле в двух видах кадров:

* **Результат продолжающего хода**: в ветвях success и error одинаково, независимо от того, несёт ли результат `user_message_uuid`.
* **Фреймы ответа продолжающего хода**: те, что несут [`user_message_uuid`](#user_message_uuid).

Значение — короткий токен в нижнем регистре, например `interrupted_turn`.

#### `queued_turn_count`

Количество отправленных вами сообщений с [`origin: { kind: "human" }`](#sdkmessageorigin), которые всё ещё ожидают в очереди команд, когда Claude Code создал результат. Требует Agent SDK v0.3.242 или позже.

Что означают `0` и отсутствующее поле:

* **`0`**: Claude Code не считает сообщения, отправленные вами без этого `origin`, и не считает уведомления задач, поэтому следующий ход всё ещё может последовать.
* **Отсутствует**: финальный результат, который Claude Code выдаёт после сбоя или фатальной ошибки запуска, опускает это поле и [может содержать обнулённые итоги](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#recover-totals-after-a-session-crash).

#### `startup_failure_reason`

Почему Claude Code отказался запускаться, чтобы ваше приложение могло предложить исправление вместо повторной попытки. Claude Code устанавливает его в результате `error_during_execution`, который он записывает перед выходом при известной ошибке запуска. Этот результат содержит обнулённые итоги, а его массив `errors` содержит сообщение об ошибке. Во всех остальных результатах поле отсутствует. Требуется Agent SDK v0.3.274 или новее.

Установите `CLAUDE_CODE_STARTUP_FAILURE_RESULTS` в `1` в [`env`](#options), чтобы получать этот результат для каждого значения `SDKStartupFailureReason`. Без этой переменной Claude Code записывает результат только для следующих ошибок, а остальные завершаются выводом в stderr, ненулевым кодом выхода и без сообщения результата:

* Возобновление, которое Claude Code останавливает, потому что [не может вернуть сессию в её worktree](https://code.claude.com/docs/ru/worktrees.md#the-session-resumes-outside-its-worktree), с `worktree_unverified` или `worktree_resume_refused`. В том разделе сказано, какая ошибка содержит какое значение.
* Отклонённое [`continue`](#options) диалога, который удерживает фоновая сессия, с `session_held_by_background`. Для отклонённого [`resume`](#options) такого диалога Claude Code записывает результат, только когда переменная установлена.
* Запуск, который Claude Code отклоняет, потому что включён [`failIfUnavailable`](#sandboxsettings) и песочница не может запуститься, с `sandbox_required_unavailable`.
* Запуск, который Claude Code отклоняет, потому что `~/.claude.json` не является допустимым JSON, со значением `config_file_invalid`.

Тип `SDKStartupFailureReason` перечисляет значения, которые может принимать `startup_failure_reason`:

```typescript theme={null}
type SDKStartupFailureReason =
  | "org_pin_api_key_conflict"
  | "provider_not_allowed"
  | "org_verify_failed"
  | "org_pin_mismatch"
  | "managed_settings_invalid"
  | "remote_settings_required_unavailable"
  | "gateway_signin_required"
  | "gateway_access_denied"
  | "proxy_invalid"
  | "temp_dir_unusable"
  | "cwd_unavailable"
  | "shell_tool_missing"
  | "session_held_by_background"
  | "worktree_resume_refused"
  | "worktree_unverified"
  | "cli_version_too_old"
  | "bypass_root"
  | "org_config_required_unavailable"
  | "org_config_refused"
  | "sandbox_required_unavailable"
  | "config_file_invalid";
```

Каждое значение называет один отказ:

| Значение | Что остановило сессию |
| :- | :- |
| `org_pin_api_key_conflict` | Управляемые настройки [требуют входа через Anthropic или облачный шлюз](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization), а вместо этого настроены API-ключ Anthropic, токен аутентификации или `apiKeyHelper` |
| `provider_not_allowed` | Управляемые настройки [перечисляют поставщиков API, которых может использовать эта машина](https://code.claude.com/docs/ru/settings-reference.md#allowedproviders), а сессия настроена на поставщика, отсутствующего в списке, или на эндпоинт, который настройки не закрепляют. Требует Claude Code v2.1.285 или позже |
| `org_verify_failed` | Не удалось проверить организацию входа на соответствие закреплению, например из-за сбоя сети или отозванного токена |
| `org_pin_mismatch` | Вход принадлежит организации, которую закрепление не разрешает |
| `managed_settings_invalid` | Не удалось прочитать управляемые настройки политики, закрепление не называет организацию, или [управляемые ограничения моделей](https://code.claude.com/docs/ru/errors.md#managed-settings-block-the-default-model) не оставляют разрешённой модели для варианта Default |
| `remote_settings_required_unavailable` | Не удалось загрузить управляемые настройки, которые требует организация |
| `gateway_signin_required` | [Облачный шлюз](https://code.claude.com/docs/ru/claude-apps-gateway) завершил этот вход |
| `gateway_access_denied` | Запрос управляемых настроек к облачному шлюзу вернул 403; этот случай описан в [таблице устранения неполадок](https://code.claude.com/docs/ru/claude-apps-gateway-deploy.md#troubleshooting) шлюза |
| `proxy_invalid` | Настройка прокси не является полным URL |
| `temp_dir_unusable` | Временный каталог пользователя небезопасен или его не удалось создать |
| `cwd_unavailable` | Рабочий каталог был удалён, перемещён или не может быть прочитан |
| `shell_tool_missing` | В Windows нет доступного инструмента оболочки: Git Bash отсутствует, а PowerShell отсутствует или отключён через `CLAUDE_CODE_USE_POWERSHELL_TOOL` |
| `session_held_by_background` | Диалог, который нужно возобновить или продолжить, выполняется как [фоновая сессия](https://code.claude.com/docs/ru/agent-view.md) |
| `worktree_resume_refused` | Worktree сессии не прошёл проверки безопасности, или возобновление было запущено изнутри него. `errors` сообщает, продолжится ли повторный запуск того же возобновления без worktree |
| `worktree_unverified` | Worktree сессии сейчас не удалось проверить, и повторная попытка может оказаться успешной |
| `cli_version_too_old` | Эта версия Claude Code ниже минимальной, которую требует Anthropic |
| `bypass_root` | Режим разрешений bypass был запрошен при работе от имени root |
| `org_config_required_unavailable` | Сессии для запуска нужны политики и управляемые настройки организации, а их не удалось загрузить, например из-за сетевого сбоя или ошибки сервера Anthropic. Требуется Agent SDK v0.3.293 или новее |
| `org_config_refused` | Anthropic отказался предоставить политики и управляемые настройки организации для этого входа, например потому что срок действия входа истёк или он был отозван, или организация не разрешает Claude Code для этой учётной записи. Требуется Agent SDK v0.3.293 или новее |
| `sandbox_required_unavailable` | [`failIfUnavailable`](#sandboxsettings) включён, и песочница не может запуститься. Текст в `errors` заканчивается на `Set sandbox.failIfUnavailable=false to allow unsandboxed execution.` Требуется Agent SDK v0.3.314 или новее |
| `config_file_invalid` | `~/.claude.json` не является допустимым JSON. Claude Code оставляет файл без изменений, поэтому повторная попытка завершается так же, пока кто-нибудь не исправит файл. `errors` называет файл и сообщает, как его восстановить или исправить. См. [Configuration error in \~/.claude.json](https://code.claude.com/docs/ru/errors.md#configuration-error-in-claude-json). Требуется TypeScript Agent SDK v0.3.318 или новее и Claude Code v2.1.318 или новее |

### `SDKSystemMessage`

Сообщение инициализации системы.

```typescript theme={null}
type SDKSystemMessage = {
  type: "system";
  subtype: "init";
  uuid: UUID;
  session_id: string;
  agents?: string[];
  apiKeySource: ApiKeySource;
  betas?: string[];
  claude_code_version: string;
  cwd: string;
  tools: string[];
  mcp_servers: {
    name: string;
    status: string;
    source?: string;
  }[];
  model: string;
  permissionMode: PermissionMode;
  slash_commands: string[];
  terminal_slash_commands?: string[];
  output_style: string;
  skills: string[];
  plugins: { name: string; path: string }[];
  plugin_errors?: {
    plugin: string;
    type: string;
    message: string;
    path?: string;
  }[];
  fast_mode_state?: FastModeState;
  fast_mode_disabled_reason?: FastModeDisabledReason;
  effort?: "low" | "medium" | "high" | "xhigh" | "max" | null;
  capabilities?: string[];
};
```

`fast_mode_state` сообщает состояние [быстрого режима](https://code.claude.com/docs/ru/fast-mode.md) сессии. Когда что-то блокирует быстрый режим, `fast_mode_disabled_reason` называет проверку, которая его заблокировала; это поле требует Claude Code v2.1.219 или позже. Коды причин и их значения см. в описании [`fast_mode_disabled_reason`](#sdkresultmessage) в сообщении результата.

`terminal_slash_commands` называет записи в `slash_commands`, чей интерфейс привязан к локальному терминалу, например `exit`. Вы можете отправлять их как любую другую запись в `slash_commands`; это поле существует, чтобы удалённый или мобильный клиент мог скрыть их из своих меню команд. Это поле присутствует, только когда оно непустое, и требует Agent SDK v0.3.229 или позже.

* `source` в каждой записи `mcp_servers`: откуда взялось определение сервера, с теми же значениями, что и `source` в [`McpServerStatus`](#mcpserverstatus). Требует Agent SDK v0.3.274 или позже.
* `effort`: [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level), установленный для следующего хода сессии, или `null`, когда Claude Code не отправляет уровень. Claude Code устанавливает это поле только в сообщении инициализации, которое отправляет клиентам [Remote Control](https://code.claude.com/docs/ru/remote-control.md), и опускает его в сообщении инициализации, которое читает ваше приложение. Требуется Agent SDK v0.3.234 или новее.

Массив `capabilities` называет поведения протокола, которые реализует этот CLI, чтобы вы могли определять поддержку функций вместо сравнения строк `claude_code_version`. Это открытый набор: игнорируйте значения, которые вы не распознаёте, и проверяйте конкретную возможность, на поведение которой вы полагаетесь. Это поле требует Claude Code v2.1.205 или позже и отсутствует в более ранних CLI.

| Возможность | Значение |
| - | - |
| `interrupt_receipt_v1` | [`interrupt()`](#query-object) разрешается с квитанцией [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse), в которой перечислены сообщения, ожидавшие обработки на момент поступления прерывания |
| `interrupt_cancel_queued_v1` | Управляющий запрос `interrupt` учитывает `cancel_queued: true`, отменяя сообщения, которые квитанция в противном случае перечислила бы в `still_queued`, и перечисляя их вместо этого в `cancelled`. См. [`SDKControlInterruptResponse`](#sdkcontrolinterruptresponse). Требует Claude Code v2.1.219 или позже |
| `sdk_mcp_manifests` | Управляющий запрос `initialize` принимает `sdkMcpServerManifests` — результаты рукопожатия MCP, полученные от ваших внутрипроцессных [MCP-серверов SDK](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md). Claude Code объявляет эту возможность в v2.1.286 или новее |
| `sdk_mcp_tools_list_changed` | Уведомление `tools/list_changed` от [MCP-сервера SDK](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md) заставляет Claude Code заново получить список инструментов этого сервера, чтобы инструмент, добавленный сервером посреди сессии, стал доступен Claude. Claude Code объявляет эту возможность в v2.1.286 или новее |

Массив `plugin_errors` перечисляет ошибки загрузки плагинов. Запись описывает либо плагин, который не загрузился и отсутствует в `plugins`, либо плагин, который загрузился без одной из своих частей, например без файла хуков. Ключ опускается, когда ошибок нет. `SDKSystemMessage` объявляет `plugin_errors` в Agent SDK v0.3.283 или позже.

Когда сам каталог или архив из вашей [опции `plugins`](#options) не загружается, поле `plugin` записи содержит позиционный тег, например `inline[0]`, вместо имени плагина. Это происходит, например, когда путь не существует или манифест недействителен. Сопоставляйте такую запись с вашей опцией по её полю `path`.

В таблице ниже перечислены поля каждой записи `plugin_errors`.

| Поле | Тип | Описание |
| - | - | - |
| `plugin` | `string` | ID плагина с ошибкой или позиционный тег, например `inline[0]`, когда не загрузился сам каталог или архив плагина |
| `type` | `string` | Категория ошибки из открытого набора, например `path-not-found` или `manifest-validation-error`. Рассматривайте нераспознанное значение как общую ошибку |
| `message` | `string` | Отображаемый текст с описанием ошибки |
| `path` | `string` | Присутствует, только когда не загрузился сам каталог или архив плагина. Его абсолютный путь; относительный путь из вашей опции `plugins` разрешается относительно опции [`cwd`](#options) |

### `SDKPartialAssistantMessage`

Частичное сообщение при потоковой передаче (только когда `includePartialMessages` равно true).

Поле `parent_tool_use_id` всегда равно `null`: события потока выдаются только для основной сессии. Для определения принадлежности субагентам используйте полные сообщения, которые содержат [`agent_id`](#sdkassistantmessage) и `parent_tool_use_id`, или включите [`forwardSubagentText`](#options), чтобы получать текст и размышления субагентов в виде полных сообщений.

```typescript theme={null}
type SDKPartialAssistantMessage = {
  type: "stream_event";
  event: BetaRawMessageStreamEvent; // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
  ttft_ms?: number; // Time to first token in ms, present only on message_start events
  user_message_uuid?: string;
  user_message_uuids?: string[];
  resume_reason?: string;
};
```

Claude Code задаёт `user_message_uuid` и `user_message_uuids` в первом событии потока хода, отличном от ping, и снова — когда меняется сообщение, на которое отвечает ход, при условиях, описанных в [`user_message_uuid`](#user_message_uuid). Когда ход продолжает ход, прерванный перезапуском, события потока, несущие эти поля, несут также [`resume_reason`](#resume_reason).

### `SDKCompactBoundaryMessage`

Сообщение, обозначающее границу сжатия контекста диалога.

```typescript theme={null}
type SDKCompactBoundaryMessage = {
  type: "system";
  subtype: "compact_boundary";
  uuid: UUID;
  session_id: string;
  compact_metadata: {
    trigger: "manual" | "auto";
    pre_tokens: number;
  };
};
```

### `SDKInformationalMessage`

Общий текстовый баннер, выдаваемый циклом. Содержит предупреждения, уведомления и другие строки состояния, не являющиеся ошибками, которые выдаёт Claude Code, а также обратную связь хуков, например причину блокировки хуком `UserPromptSubmit`.

В Claude Code v2.1.227 или позже [`systemMessage`](https://code.claude.com/docs/ru/hooks#json-output) хука может поступить как это сообщение, при этом каждая строка начинается с префикса с именем хука, например `PostToolUse:Bash says:`. В [разделе каждого события](https://code.claude.com/docs/ru/hooks.md#hook-events) на странице хуков сказано, как отображается вывод.

Выполняйте рендеринг `content` как простого текста с заданным `level`.

```typescript theme={null}
type SDKInformationalMessage = {
  type: "system";
  subtype: "informational";
  content: string;
  level: "info" | "notice" | "suggestion" | "warning";
  tool_use_id?: string;
  prevent_continuation?: boolean;
  tag?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKWorkerShuttingDownMessage`

Выдаётся при корректном завершении рабочего процесса, чтобы удалённые клиенты могли показать, почему рабочий процесс завершился, вместо ожидания таймаута heartbeat. `reason` — это короткая строка в snake\_case, устанавливаемая CLI хоста, например `"host_exit"` или `"remote_control_disabled"`. Реагируйте на это сообщение только при потоковой передаче в реальном времени. Возобновлённая сессия воспроизводит прошлые экземпляры этого сообщения, поэтому в этом случае игнорируйте их.

```typescript theme={null}
type SDKWorkerShuttingDownMessage = {
  type: "system";
  subtype: "worker_shutting_down";
  reason: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKPluginInstallMessage`

Событие прогресса установки плагинов. Выдаётся, когда установлена переменная [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](https://code.claude.com/docs/ru/env-vars), чтобы ваше приложение Agent SDK могло отслеживать установку плагинов из маркетплейса перед первым ходом. Статусы `started` и `completed` обрамляют установку в целом. Статусы `installed` и `failed` сообщают об отдельных маркетплейсах и включают `name`.

```typescript theme={null}
type SDKPluginInstallMessage = {
  type: "system";
  subtype: "plugin_install";
  status: "started" | "installed" | "failed" | "completed";
  name?: string;
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKPermissionDeniedMessage`

Событие потока, выдаваемое, когда система разрешений отклоняет вызов инструмента без интерактивного запроса разрешения. Используйте его, чтобы показывать отказ в вашем интерфейсе в момент его возникновения, а не только по следующему за ним результату инструмента с `is_error`. О каких отказах сообщает событие, зависит от того, как запуск обрабатывает запросы разрешений:

* **С обратным вызовом [`canUseTool`](#canusetool)** и значением по умолчанию [`permissionPrompts: 'host'`](#options): запросы разрешений поступают в ваш обратный вызов, а это событие сообщает об отказах, которые Claude Code принимает самостоятельно, не вызывая его.
* **Без обоих**: простой запуск `-p` или `query()`, где не заданы ни `canUseTool`, ни `permissionPromptToolName`, отклоняет любой вызов инструмента, который потребовал бы запроса, если только его не разрешает [хук `PermissionRequest`](https://code.claude.com/docs/ru/hooks-guide#limitations), и это событие сообщает об этих отказах, а также о тех, которые Claude Code принимает самостоятельно. До v2.1.223 Claude Code не выдавал это событие в запусках без обратного вызова.
* **С инструментом запроса разрешений MCP**, заданным через `permissionPromptToolName` или флаг [`--permission-prompt-tool`](https://code.claude.com/docs/ru/cli-reference#cli-flags), и значением по умолчанию `permissionPrompts: 'host'`: Claude Code вообще не выдаёт это событие, даже для отказов по правилам, которые он принимает самостоятельно.
* **С [`permissionPrompts: 'none'`](#options)**: Claude Code отклоняет вызовы, которые потребовали бы запроса разрешения, даже когда также заданы `canUseTool` или инструмент запроса разрешений MCP, и это событие сообщает об этих отказах, а также об отказах, которые Claude Code принимает самостоятельно. Требует Claude Code v2.1.259 или позже.

В любой конфигурации это событие пропускает отказы, принятые на пути хука `PreToolUse`, — независимо от того, отклонил ли вызов сам хук или правило запрета переопределило решение хука разрешить или запросить подтверждение. Кроме того, событие выдаётся по принципу best-effort: иногда Claude Code записывает отказ без выдачи этого события, поэтому авторитетной записью является `permission_denials` в [сообщении результата](#sdkresultmessage).

```typescript theme={null}
type SDKPermissionDeniedMessage = {
  type: "system";
  subtype: "permission_denied";
  tool_name: string;
  tool_use_id: string;
  agent_id?: string;
  decision_reason_type?: string;
  decision_reason?: string;
  message: string;
  uuid: UUID;
  session_id: string;
};
```

| Поле | Тип | Описание |
| - | - | - |
| `tool_name` | `string` | Имя инструмента, в вызове которого было отказано |
| `tool_use_id` | `string` | ID блока `tool_use`, на который отвечает этот отказ |
| `agent_id` | `string` | ID субагента, когда отклонённый вызов возник внутри субагента. Повторяет поле в `can_use_tool` для маршрутизации на стороне хоста |
| `decision_reason_type` | `string` | Дискриминатор компонента, принявшего решение, например `"rule"`, `"mode"`, `"classifier"` или `"asyncAgent"` |
| `decision_reason` | `string` | Понятная человеку причина от компонента, принявшего решение, если доступна |
| `message` | `string` | Сообщение об отказе, возвращённое модели в `tool_result` |

### `SDKPermissionDenial`

Информация об отклонённом использовании инструмента.

```typescript theme={null}
type SDKPermissionDenial = {
  tool_name: string;
  tool_use_id: string;
  tool_input: Record<string, unknown>;
};
```

### `SDKContextUsage`

Структурированная форма отчёта `/context`, передаваемая как `context_usage` в [`SDKAssistantMessage`](#sdkassistantmessage), которое доставляет результат `/context`. Agent SDK v0.3.232 и позже экспортируют этот тип. В отличие от [`SDKControlGetContextUsageResponse`](#sdkcontrolgetcontextusageresponse), он содержит только данные, необходимые для отображения разбивки использования, без полей отображения, таких как `color` и `gridRows`. Claude Code вычисляет отчёт с помощью запросов API для подсчёта токенов, которые не появляются в потоке сообщений; см. [как обрабатываются эти запросы](#sdkcontrolgetcontextusageresponse).

```typescript theme={null}
type SDKContextUsage = {
  model: string;
  total_tokens: number;
  raw_max_tokens: number;
  percentage: number;
  over_limit?: {
    tokens_over: number;
    kind: "hard_limit" | "compaction_window";
  };
  categories: SDKContextUsageCategory[];
  mcp_tools: {
    name: string;
    server_name: string;
    tokens: number;
  }[];
  memory_files: {
    path: string;
    type: string;
    tokens: number;
  }[];
  agents: {
    agent_type: string;
    source: string;
    tokens: number;
  }[];
  skills?: {
    name: string;
    source: string;
    plugin_name?: string;
    tokens: number;
  }[];
};
```

В таблице перечислено, что Claude Code помещает в каждое поле. Поля от `model` до `over_limit` описывают сессию в целом, а поля-коллекции относят токены к отдельным элементам.

| Поле | Тип | Описание |
| - | - | - |
| `model` | `string` | Модель основного цикла, для которой Claude Code вычислил использование, а не модель субагента |
| `total_tokens` | `number` | Оценка Claude Code количества используемых токенов. Не ограничивается размером окна, поэтому может превышать `raw_max_tokens`, когда сессия превышает лимит |
| `raw_max_tokens` | `number` | Контекстное окно модели или меньшее [окно автосжатия](https://code.claude.com/docs/ru/model-config.md#context-window-and-auto-compaction), когда оно применяется, например заданное вами или граница 200K, которую Claude Code применяет к некоторым моделям с окном в 1M токенов. Claude Code измеряет `total_tokens` относительно этого окна |
| `percentage` | `number` | `total_tokens` как округлённый процент от `raw_max_tokens`, поэтому может превышать 100, когда сессия превышает лимит |
| `over_limit` | `object` | Присутствует, только когда `total_tokens` превышает `raw_max_tokens`. `tokens_over` — это величина превышения, а `kind` сообщает, как Claude Code определил окно |
| `categories` | [`SDKContextUsageCategory`](#sdkcontextusagecategory)`[]` | Одна запись на строку разбивки использования по категориям |
| `mcp_tools` | `object[]` | Токены, отнесённые к каждому инструменту MCP, с его полным именем, например `mcp__linear__create_issue`, и его `server_name` |
| `memory_files` | `object[]` | Токены, отнесённые к каждому загруженному файлу памяти, с его `path` и меткой источника, например `Project` или `User`, в `type` |
| `agents` | `object[]` | Токены, отнесённые к каждому определению пользовательского субагента, с идентификатором источника, например `projectSettings`, `userSettings` или `plugin`. Встроенные субагенты не перечисляются |
| `skills` | `object[]` | Токены, отнесённые к каждому скиллу в списке скиллов, с идентификатором источника и, для скиллов плагинов, именем плагина в `plugin_name`. Отсутствует, когда никакие скиллы не вносят токенов |

`over_limit.kind` фиксирует, как Claude Code определил окно, а не то, примет ли API следующий запрос:

* `hard_limit`: окно — это то, что Claude Code считает собственным лимитом модели, за пределами которого API отклоняет запросы
* `compaction_window`: окно — это окно политики сжатия контекста, которое может совпадать или не совпадать с лимитом модели

Claude Code развивает этот тип аддитивно, добавляя новые данные как необязательные поля, а не изменяя структуру существующих. Читайте известные вам поля и игнорируйте те, которые вы не распознаёте.

### `SDKContextUsageCategory`

Одна строка разбивки использования `/context` по категориям.

```typescript theme={null}
type SDKContextUsageCategory = {
  name: string;
  tokens: number;
  kind: "used" | "free" | "buffer" | "deferred";
};
```

В таблице перечислено, что Claude Code помещает в каждое поле строки.

| Поле | Тип | Описание |
| - | - | - |
| `name` | `string` | Отображаемое имя строки в том виде, в каком его выводит `/context`, например `Messages`. Классифицируйте строки по `kind`, а не по имени |
| `tokens` | `number` | Количество токенов строки. Строки могут содержать ноль токенов |
| `kind` | `string` | Что представляет строка: `used`, `free`, `buffer` или `deferred` |

Каждое значение `kind` указывает, что представляют собой токены строки:

* `used`: содержимое, занимающее контекстное окно
* `free`: оставшаяся часть окна
* `buffer`: резерв для сжатия контекста
* `deferred`: схемы инструментов, которые Claude Code держит вне окна и исключает из расчёта использования; перечисляются для информации

### `SDKUsageReport`

Структурированная форма отчёта `/usage`, передаваемая как `usage_report` в [`SDKAssistantMessage`](#sdkassistantmessage), который доставляет результат `/usage`. Agent SDK v0.3.273 и новее экспортируют этот тип. Тип экспериментальный: его форма может измениться.

```typescript theme={null}
type SDKUsageReport = {
  session: {
    total_cost_usd: number;
    total_api_duration_ms: number;
    total_duration_ms: number;
    total_lines_added: number;
    total_lines_removed: number;
    model_usage: { [modelName: string]: ModelUsage };
  };
  rate_limits: {
    limits:
      | {
          kind: string;
          group: string;
          percent: number;
          resets_at: string | null;
          scope?: {
            model?: { display_name: string } | null;
            surface?: { display_name: string } | null;
          } | null;
          severity: string;
          is_active: boolean;
        }[]
      | null;
    extra_usage?: {
      is_enabled: boolean;
      monthly_limit: number | null;
      used_credits: number | null;
      utilization: number | null;
      currency?: string | null;
    } | null;
  } | null;
};
```

Поля верхнего уровня — `session` и `rate_limits`:

* `session`: текущие итоги стоимости и использования Claude Code, считанные из того же реестра, что и `total_cost_usd` и `modelUsage` в [`SDKResultMessage`](#sdkresultmessage). Каждая запись `model_usage` — это [`ModelUsage`](#modelusage).
* `rate_limits`: строки использования тарифа в `limits` и расход кредитов использования в `extra_usage`. Равно `null`, когда Claude Code не удалось получить данные об использовании тарифа, например когда OAuth-токен сессии не имеет scope `user:profile`.

Claude Code вычисляет `session.total_cost_usd` локально по количеству токенов, поэтому это оценка, а не то, что выставляется по вашему тарифу. Расход кредитов использования, сообщаемый сервером, — это отдельный блок `extra_usage`. Оговорки о точности см. в разделе [Отслеживание затрат и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md).

`limits` содержит строки использования сервера в том виде, в каком их отправил сервер: какие счётчики применяются, их область действия, метки, серьёзность и порядок определяет сервер, поэтому отображайте строки дословно.

* Пустой массив означает, что сервер не сообщил ни об одном счётчике.
* `null` означает, что у Claude Code нет строк для отчёта.

Каждая строка `limits` описывает один счётчик использования:

| Поле | Тип | Описание |
| - | - | - |
| `kind` | `string` | Вид счётчика на сервере, например `session`, `weekly_all` или `weekly_scoped`. Классифицируйте строку по нему, а не по метке |
| `group` | `string` | Группа строк на сервере, например `session` или `weekly`. Строки отображаются сгруппированными по ней в порядке сервера |
| `percent` | `number` | Доля использованного окна, 0–100 |
| `resets_at` | `string \| null` | Временная метка ISO 8601, когда окно сбрасывается |
| `scope` | `object \| null` | Необязательное. Для чего предназначена строка с областью действия — для модели или интерфейса, с отображаемой меткой сервера |
| `severity` | `string` | Оценка строки сервером для цвета счётчика, например `normal`, `warning` или `critical` |
| `is_active` | `boolean` | `true` в строке, которую сервер выбирает для показа в индикаторе с одним значением |

До Agent SDK v0.3.277 тип объявлял `severity` и `is_active` как необязательные и допускающие null, и строка могла прийти без них.

`extra_usage` — расход и лимит [кредитов использования](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) за расчётный период по данным сервера; присутствует, когда у тарифа есть кредиты использования. Суммы указаны в минимальных единицах `currency`, для USD — в центах.

* `monthly_limit` равно `null`, когда у этой учётной записи нет собственного лимита расходов. В тарифах Team и Enterprise не отображайте `null` как безлимит.
* `is_enabled` равно `false`, пока кредиты не могут оплачивать запросы.

### `SDKMessageOrigin`

Происхождение сообщения с ролью пользователя. Отображается как `origin` в [`SDKUserMessage`](#sdkusermessage). [`SDKResultMessage`](#sdkresultmessage) для хода содержит `origin`, назначенный Claude Code, поэтому вы можете определить, что инициировало этот ход.

```typescript theme={null}
type SDKMessageOrigin =
  | { kind: "human" }
  | { kind: "channel"; server: string }
  | {
      kind: "peer";
      from: string;
      fromMode?: "bypass" | "prompting";
      name?: string;
      fromSession?: string;
      senderTaskId?: string;
      body?: string;
      verifiedPeerPid?: number;
    }
  | {
      kind: "task-notification";
      subkind?: "scheduled-trigger" | "peer-send-message";
      fireReason?: string;
      runId?: string;
    }
  | { kind: "coordinator" }
  | { kind: "auto-continuation" }
  | { kind: "unclassified" };
```

Ваше приложение может устанавливать следующие виды `origin` в отправляемом сообщении:

* `{ kind: "human" }`: то, что ввёл пользователь
* `{ kind: "task-notification", subkind: "scheduled-trigger" }`: [объявленный вами запуск по расписанию](#declare-a-scheduled-run)

Остальные виды оставьте Claude Code и серверам Anthropic. Если вы установите один из этих видов, Claude по умолчанию воспринимает сообщение как пользовательское.

Чтобы отправить текст, который пользователь не писал, например загруженную страницу или вывод другого агента, отправьте его отдельным сообщением с [`isSynthetic`](#sdkusermessage), установленным в `true`, и без `origin`. Также установите [`client_composed`](#sdkusermessage) в `true`, чтобы текст, начинающийся с `/`, не выполнялся как команда.

| `kind` | Значение |
| - | - |
| `human` | Прямой ввод от конечного пользователя. Если ваше приложение пересылает введённое пользователем как пользовательское сообщение, установите его `origin` в `{ kind: "human" }`. Без этого `origin` Claude всё равно воспринимает сообщение как пользовательское, но проверки, требующие промпта, введённого человеком, например [ключевое слово рабочего процесса `ultracode`](https://code.claude.com/docs/ru/workflows#ask-for-a-workflow-in-your-prompt), не принимают такое сообщение. |
| `channel` | Сообщение, поступившее по [каналу](https://code.claude.com/docs/ru/channels.md). `server` — это имя исходного MCP-сервера. |
| `peer` | Сообщение от другого агента Claude Code: [участника команды](https://code.claude.com/docs/ru/agent-teams.md) в том же процессе или [однорангового узла из другой сессии](https://code.claude.com/docs/ru/cross-session-messaging.md) — другой вашей сессии Claude Code. [Десктопное приложение](https://code.claude.com/docs/ru/desktop.md#work-across-sessions), которое передаёт такие сообщения между вашими сессиями, объявляет этот вид с [`fromMode`](#peer-origin-fields). Чтобы передать вывод другого агента из собственного приложения, вместо этого установите `isSynthetic` и `client_composed`. Семантику каждого поля и модель доверия см. в разделе [Поля происхождения peer](#peer-origin-fields). |
| `task-notification` | Синтетический ход, внедрённый для доставки, которая поступает без нового промпта пользователя, например для завершённой фоновой задачи; см. [`SDKTaskNotificationMessage`](#sdktasknotificationmessage) об этом варианте. Промпт, который ваше приложение [объявляет запланированным запуском](#declare-a-scheduled-run), также имеет этот вид. Необязательный `subkind` указывает, что вызвало уведомление. См. [Подвиды уведомлений задач](#task-notification-subkinds). |
| `coordinator` | Сообщение от координатора команды в [команде агентов](https://code.claude.com/docs/ru/agent-teams.md). |
| `auto-continuation` | Синтетический ход, внедрённый, когда сессия продолжается без нового пользовательского ввода, например результат команды, который запускает промпт продолжения. |
| `unclassified` | Сообщение, помеченное как исходящее не от пользователя, например [`SDKUserMessage`](#sdkusermessage), отправленное вами с `isSynthetic: true`. Требуется Claude Code v2.1.223 или более поздней версии. |

### Подвиды уведомлений задач

Когда Claude Code доставляет уведомление задачи в сессию, он устанавливает `subkind` в `origin` уведомления, если серверы Anthropic проверили, откуда пришло это уведомление. Он также устанавливает `subkind`, когда ваше приложение само [объявляет сообщение запланированным запуском](#declare-a-scheduled-run), что требует TypeScript Agent SDK v0.3.280 или позже. `subkind` требует Claude Code v2.1.213 или позже и принимает одно из двух значений:

* `scheduled-trigger`: уведомление представляет собой сохранённый промпт [облачной запланированной задачи](https://code.claude.com/docs/ru/routines.md), доставленный потому, что сработал один из триггеров задачи: её расписание, её [API-триггер](https://code.claude.com/docs/ru/routines.md#add-an-api-trigger), её [триггер GitHub](https://code.claude.com/docs/ru/routines.md#add-a-github-trigger) или **Run now**. Промпт, который ваше приложение [объявляет как запланированный запуск](#declare-a-scheduled-run), тоже имеет это значение. Claude Code представляет такие сообщения модели как назначенную сессии задачу с уведомлением, отличным от [уведомления, которое несут другие уведомления о задачах](#sdktasknotificationmessage).
* `peer-send-message`: уведомление — это сообщение, которое другая ваша сессия отправила с помощью серверного инструмента `send_message`, используемого [облачными сессиями](https://code.claude.com/docs/ru/claude-code-on-the-web.md) для обмена сообщениями друг с другом (а не [межсессионного инструмента `SendMessage`](https://code.claude.com/docs/ru/cross-session-messaging)), причём серверы Anthropic проверили, что обе сессии принадлежат одной и той же закрытой группе сессий. Требует Claude Code v2.1.224 или позже. Доставка `send_message`, которую серверы так не проверили, не получает подвида.

Все остальные уведомления задач не имеют `subkind`. Сюда относятся [активность PR](https://code.claude.com/docs/ru/claude-code-on-the-web.md#how-claude-responds-to-pr-activity), доставленная в сессию, и фоновые события, такие как завершённая задача. Сообщения от [межсессионного инструмента `SendMessage`](https://code.claude.com/docs/ru/cross-session-messaging) вообще не являются уведомлениями задач: поступают ли они из сессии на той же машине или через серверы Anthropic с другой машины, Claude Code присваивает им `kind: "peer"` и [поля происхождения peer](#peer-origin-fields).

`fireReason` указывает, почему сработало уведомление `scheduled-trigger`, в виде короткого токена в нижнем регистре, например `scheduled`, `manual`, `retry`, `catch_up` или `api`. Серверы Anthropic устанавливают его для доставок [облачной запланированной задачи](https://code.claude.com/docs/ru/routines.md), а ваше приложение устанавливает его, когда объявляет запланированный запуск. Если ни одна из сторон его не передала, поле отсутствует. Требуется TypeScript Agent SDK v0.3.280 или новее.

Фоновая задача может выполняться более одного раза под одним и тем же `task_id`, например когда Claude [возобновляет субагента](https://code.claude.com/docs/ru/agent-sdk/subagents.md#resume-subagents). Каждый запуск имеет собственный [`run_id`](#sdktaskstartedmessage). Когда уведомление о запуске поступает в вашу сессию как пользовательское сообщение, `runId` в origin `task-notification` этого сообщения содержит то же значение. Уведомление может прийти после того, как начался следующий запуск задачи, и всё равно будет содержать ID более раннего запуска. Чтобы определить, к какому запуску относится ход, сравнивайте `runId`, а не `task_id`. Требуется TypeScript Agent SDK v0.3.292 или новее.

#### Объявление запланированного запуска

Если ваше приложение запускает промпты по собственному расписанию, объявляйте каждый запуск, чтобы Claude Code представлял ход модели как запланированную задачу, а не как живой ввод пользователя. Запустите сессию с `CLAUDE_CODE_HOST_SCHEDULED_RUN`, установленной в `1` в [`env`](#options), затем отправьте [`SDKUserMessage`](#sdkusermessage) запуска с `origin: { kind: "task-notification", subkind: "scheduled-trigger", fireReason: "scheduled" }` и без `isSynthetic`. Claude Code игнорирует объявление в процессе, запущенном без этой переменной. Он также игнорирует его в процессе, окружение которого содержит [`CLAUDECODE`](https://code.claude.com/docs/ru/env-vars) или `CLAUDE_CODE_CHILD_SESSION`. Claude Code сохраняет `fireReason`, только когда значение состоит из 1–32 строчных букв или подчёркиваний. Требует TypeScript Agent SDK v0.3.280 или позже.

### Поля происхождения peer

Происхождение `peer` определяет, какой агент отправил сообщение: [участник команды](https://code.claude.com/docs/ru/agent-teams.md), работающий в том же процессе и отправляющий сообщение в `main` с помощью `SendMessage`, или [одноранговый узел из другой сессии](https://code.claude.com/docs/ru/cross-session-messaging.md) — другая ваша сессия Claude Code. Для одноранговых узлов из других сессий требуется Claude Code v2.1.224 или новее на macOS и Linux; требования для нативной Windows см. в разделе [доступность межсессионного обмена сообщениями](https://code.claude.com/docs/ru/cross-session-messaging.md#availability). Одноранговый узел из другой сессии может работать на той же машине или на [другой вашей машине](https://code.claude.com/docs/ru/cross-session-messaging.md#message-sessions-on-other-machines), если его сообщение поступает через [Remote Control](https://code.claude.com/docs/ru/remote-control.md).

* `from`: имя участника команды или адрес отправителя для межсессионного пира. Для [одностороннего сообщения с другой машины](https://code.claude.com/docs/ru/cross-session-messaging.md#message-sessions-on-other-machines) у отправителя нет адреса для ответа, и `from` равно `"unknown"`. Значение задаётся отправителем; проверенной идентичностью является `verifiedPeerPid`.
* `fromMode`: класс разрешений отправляющей сессии, `bypass` или `prompting`. Claude Code считывает его в принимающей сессии, когда применяет [средства управления входящими сообщениями](https://code.claude.com/docs/ru/cross-session-messaging.md#control-inbound-messages). Требуется Agent SDK v0.3.234 или более поздней версии.
* `senderTaskId`: ID задачи участника команды. Отсутствует для межсессионного пира.
* `name`: отображаемое имя отправителя, нормализованное Claude Code: он удаляет управляющие, форматирующие и суррогатные кодовые точки Unicode, а также разделители строк и абзацев, затем обрезает пробелы и ограничивает результат 64 кодовыми точками с многоточием. Требует Claude Code v2.1.205 или позже.
* `body`: декодированное тело сообщения с удалённой peer-обёрткой, побайтово совпадающее с тем, что видит модель. Присутствует для одиночного сообщения участника команды и отсутствует, когда несколько сообщений объединены; для узла из другой сессии присутствует, только если ход состоит ровно из одной peer-обёртки, сформированной Claude Code. Отображайте `name` и `body` вместо повторного разбора текста сообщения. До версии v2.1.299 объединённые сообщения сохраняли `body` первого сообщения. Требуется Claude Code v2.1.205 или новее.
* `fromSession`: ID сессии отправителя, которую может открыть хост; устанавливается хостом отправителя, чтобы ваш интерфейс мог ссылаться на отправляющую сессию. Как и `from`, это значение заявлено отправителем: используйте его только как цель навигации и не рассматривайте как доказательство идентичности отправителя. Требует Claude Code v2.1.216 или позже.
* `verifiedPeerPid`: ID процесса, который подключился к сокету межсессионного обмена сообщениями этой сессии, проверенный ядром и прочитанный из самого соединения, а не из данных сообщения. Используйте его, а не `from`, для идентификации отправителя: `from` может подделать любой процесс того же пользователя. Поле отсутствует, когда Claude Code не может его проверить, например в Windows или при поступлении не через сокет, поэтому отсутствие значения означает, что отправитель не проверен. Для ретранслируемого трафика оно идентифицирует ретранслятор, а не автора сообщения, а ID процессов могут переиспользоваться, поэтому рассматривайте его как сведения о происхождении, а не как токен аутентификации. Требует Claude Code v2.1.216 или позже.

## Типы hooks

Для полного руководства по использованию хуков с примерами и общими паттернами см. [руководство по хукам](https://code.claude.com/docs/ru/agent-sdk/hooks.md).

### `HookEvent`

Доступные события hooks.

```typescript theme={null}
type HookEvent =
  | "PreToolUse"
  | "PostToolUse"
  | "PostToolUseFailure"
  | "PostToolBatch"
  | "Notification"
  | "UserPromptSubmit"
  | "UserPromptExpansion"
  | "SessionStart"
  | "SessionEnd"
  | "Stop"
  | "StopFailure"
  | "SubagentStart"
  | "SubagentStop"
  | "PreCompact"
  | "PostCompact"
  | "PreModelSwitch"
  | "PostModelSwitch"
  | "PermissionRequest"
  | "PermissionDenied"
  | "Setup"
  | "TeammateIdle"
  | "TaskCreated"
  | "TaskCompleted"
  | "Elicitation"
  | "ElicitationResult"
  | "ConfigChange"
  | "DirectoryAdded"
  | "WorktreeCreate"
  | "WorktreeRemove"
  | "InstructionsLoaded"
  | "CwdChanged"
  | "FileChanged"
  | "MessageDisplay";
```

### `HookCallback`

Тип функции обратного вызова hook.

```typescript theme={null}
type HookCallback = (
  input: HookInput, // Объединение всех типов входных данных hook
  toolUseID: string | undefined,
  options: { signal: AbortSignal }
) => Promise<HookJSONOutput>;
```

### `HookCallbackMatcher`

Конфигурация hook с опциональным matcher.

```typescript theme={null}
interface HookCallbackMatcher {
  matcher?: string;
  hooks: HookCallback[];
  timeout?: number; // Timeout в секундах для всех hooks в этом matcher
  onFailure?: "continue" | "block"; // "block" блокирует действие, если обратный вызов завершается с ошибкой
}
```

Чтобы определить, на что распространяется `onFailure`, см. [Блокировка действия при сбое обратного вызова](https://code.claude.com/docs/ru/agent-sdk/hooks.md#block-the-action-when-a-callback-fails).

### `HookInput`

Тип объединения всех типов входных данных hook.

```typescript theme={null}
type HookInput =
  | PreToolUseHookInput
  | PostToolUseHookInput
  | PostToolUseFailureHookInput
  | PostToolBatchHookInput
  | PermissionDeniedHookInput
  | NotificationHookInput
  | UserPromptSubmitHookInput
  | UserPromptExpansionHookInput
  | SessionStartHookInput
  | SessionEndHookInput
  | StopHookInput
  | StopFailureHookInput
  | SubagentStartHookInput
  | SubagentStopHookInput
  | PreCompactHookInput
  | PostCompactHookInput
  | PreModelSwitchHookInput
  | PostModelSwitchHookInput
  | PermissionRequestHookInput
  | SetupHookInput
  | TeammateIdleHookInput
  | TaskCreatedHookInput
  | TaskCompletedHookInput
  | ElicitationHookInput
  | ElicitationResultHookInput
  | ConfigChangeHookInput
  | InstructionsLoadedHookInput
  | DirectoryAddedHookInput
  | WorktreeCreateHookInput
  | WorktreeRemoveHookInput
  | CwdChangedHookInput
  | FileChangedHookInput
  | MessageDisplayHookInput;
```

### `BaseHookInput`

Базовый интерфейс, который расширяют все типы входных данных hook.

```typescript theme={null}
type BaseHookInput = {
  session_id: string;
  transcript_path: string;
  cwd: string;
  prompt_id?: string;
  permission_mode?: string;
  effort?: { level: string };
  agent_id?: string;
  agent_type?: string;
};
```

Поле `prompt_id` — это UUID, идентифицирующий пользовательский запрос, который в настоящий момент обрабатывается. Он совпадает с [атрибутом `prompt.id` на событиях OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage#event-correlation-attributes) и отсутствует до первого ввода пользователя. Требуется Claude Code v2.1.196 или позже.

#### `PreToolUseHookInput`

```typescript theme={null}
type PreToolUseHookInput = BaseHookInput & {
  hook_event_name: "PreToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  mcp_server?: McpServerProvenance;
};
```

`mcp_server` присутствует, когда инструмент поступает с сервера MCP; см. [`McpServerProvenance`](#mcpserverprovenance). Входные данные `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` и `PermissionDenied` содержат то же поле. Это поле требует Agent SDK v0.3.274 или позже.

#### `PostToolUseHookInput`

```typescript theme={null}
type PostToolUseHookInput = BaseHookInput & {
  hook_event_name: "PostToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_response: unknown;
  tool_use_id: string;
  duration_ms?: number;
  mcp_server?: McpServerProvenance;
};
```

#### `PostToolUseFailureHookInput`

```typescript theme={null}
type PostToolUseFailureHookInput = BaseHookInput & {
  hook_event_name: "PostToolUseFailure";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  error: string;
  is_interrupt?: boolean;
  duration_ms?: number;
  mcp_server?: McpServerProvenance;
};
```

#### `PostToolBatchHookInput`

Срабатывает один раз после того, как каждый вызов инструмента в пакете разрешится, перед следующим запросом модели. `tool_response` содержит сериализованное содержимое `tool_result`, которое видит модель; форма отличается от структурированного объекта `Output` в `PostToolUseHookInput`.

```typescript theme={null}
type PostToolBatchHookInput = BaseHookInput & {
  hook_event_name: "PostToolBatch";
  tool_calls: PostToolBatchToolCall[];
};

type PostToolBatchToolCall = {
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  tool_response?: unknown;
};
```

#### `PermissionDeniedHookInput`

```typescript theme={null}
type PermissionDeniedHookInput = BaseHookInput & {
  hook_event_name: "PermissionDenied";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  reason: string;
  mcp_server?: McpServerProvenance;
};
```

#### `NotificationHookInput`

```typescript theme={null}
type NotificationHookInput = BaseHookInput & {
  hook_event_name: "Notification";
  message: string;
  title?: string;
  notification_type: string;
};
```

#### `UserPromptSubmitHookInput`

```typescript theme={null}
type UserPromptSubmitHookInput = BaseHookInput & {
  hook_event_name: "UserPromptSubmit";
  prompt: string;
  session_title?: string;
};
```

#### `UserPromptExpansionHookInput`

```typescript theme={null}
type UserPromptExpansionHookInput = BaseHookInput & {
  hook_event_name: "UserPromptExpansion";
  expansion_type: "slash_command" | "mcp_prompt";
  command_name: string;
  command_args: string;
  command_source?: string;
  prompt: string;
};
```

#### `SessionStartHookInput`

```typescript theme={null}
type SessionStartHookInput = BaseHookInput & {
  hook_event_name: "SessionStart";
  source: "startup" | "resume" | "clear" | "compact" | "fork";
  agent_type?: string;
  model?: string;
  session_title?: string;
};
```

#### `SessionEndHookInput`

```typescript theme={null}
type SessionEndHookInput = BaseHookInput & {
  hook_event_name: "SessionEnd";
  reason: ExitReason; // Строка из массива EXIT_REASONS
};
```

#### `StopHookInput`

```typescript theme={null}
type StopHookInput = BaseHookInput & {
  hook_event_name: "Stop";
  stop_hook_active: boolean;
  last_assistant_message?: string;
  background_tasks?: BackgroundTaskSummary[];
  session_crons?: SessionCronSummary[];
};
```

#### `StopFailureHookInput`

```typescript theme={null}
type StopFailureHookInput = BaseHookInput & {
  hook_event_name: "StopFailure";
  error: SDKAssistantMessageError;
  error_details?: string;
  last_assistant_message?: string;
};
```

#### `SubagentStartHookInput`

```typescript theme={null}
type SubagentStartHookInput = BaseHookInput & {
  hook_event_name: "SubagentStart";
  agent_id: string;
  agent_type: string;
};
```

#### `SubagentStopHookInput`

```typescript theme={null}
type SubagentStopHookInput = BaseHookInput & {
  hook_event_name: "SubagentStop";
  stop_hook_active: boolean;
  agent_id: string;
  agent_transcript_path: string;
  agent_type: string;
  last_assistant_message?: string;
  background_tasks?: BackgroundTaskSummary[];
  session_crons?: SessionCronSummary[];
};

type BackgroundTaskSummary = {
  id: string;
  type: string;
  status: string;
  description: string;
  command?: string;
  agent_type?: string;
  server?: string;
  tool?: string;
  name?: string;
};

type SessionCronSummary = {
  id: string;
  schedule: string;
  recurring: boolean;
  prompt: string;
};
```

#### `PreCompactHookInput`

```typescript theme={null}
type PreCompactHookInput = BaseHookInput & {
  hook_event_name: "PreCompact";
  trigger: "manual" | "auto";
  custom_instructions: string | null;
};
```

#### `PostCompactHookInput`

```typescript theme={null}
type PostCompactHookInput = BaseHookInput & {
  hook_event_name: "PostCompact";
  trigger: "manual" | "auto";
  compact_summary: string;
};
```

#### `PreModelSwitchHookInput`

Срабатывает перед тем, как запрошенное переключение модели вступит в силу. `context_tokens` и поля после него оценивают, какие затраты на повторную отправку разговора новой модели. Для полного описания полей и семантики блокирования см. [PreModelSwitch](https://code.claude.com/docs/ru/hooks.md#premodelswitch).

```typescript theme={null}
type PreModelSwitchHookInput = BaseHookInput & {
  hook_event_name: "PreModelSwitch";
  from_model: string;
  to_model: string;
  requested_model: string | null;
  source: "command" | "picker" | "sdk";
  context_tokens: number;
  prompt_cache_warm: boolean;
  cache_ttl: "5m" | "1h";
  estimated_cache_write_usd: number;
  pricing: "configured" | "catalog" | "default";
};
```

#### `PostModelSwitchHookInput`

Срабатывает после изменения модели сессии. Он содержит те же поля, что и `PreModelSwitchHookInput`, с двумя дополнительными значениями `source`. См. [PostModelSwitch](https://code.claude.com/docs/ru/hooks.md#postmodelswitch).

```typescript theme={null}
type PostModelSwitchHookInput = BaseHookInput & {
  hook_event_name: "PostModelSwitch";
  from_model: string;
  to_model: string;
  requested_model: string | null;
  source: "command" | "picker" | "sdk" | "auto" | "resume";
  context_tokens: number;
  prompt_cache_warm: boolean;
  cache_ttl: "5m" | "1h";
  estimated_cache_write_usd: number;
  pricing: "configured" | "catalog" | "default";
};
```

#### `PermissionRequestHookInput`

```typescript theme={null}
type PermissionRequestHookInput = BaseHookInput & {
  hook_event_name: "PermissionRequest";
  tool_name: string;
  tool_input: unknown;
  permission_suggestions?: PermissionUpdate[];
  mcp_server?: McpServerProvenance;
};
```

#### `SetupHookInput`

```typescript theme={null}
type SetupHookInput = BaseHookInput & {
  hook_event_name: "Setup";
  trigger: "init" | "maintenance";
};
```

#### `TeammateIdleHookInput`

```typescript theme={null}
type TeammateIdleHookInput = BaseHookInput & {
  hook_event_name: "TeammateIdle";
  teammate_name: string;
  /** @deprecated с версии v2.1.178. Содержит имя команды, полученное из сессии; будет удалено. */
  team_name: string;
};
```

#### `TaskCreatedHookInput`

```typescript theme={null}
type TaskCreatedHookInput = BaseHookInput & {
  hook_event_name: "TaskCreated";
  task_id: string;
  task_subject: string;
  task_description?: string;
  teammate_name?: string;
  /** @deprecated с версии v2.1.178. Содержит имя команды, полученное из сессии; будет удалено. */
  team_name?: string;
};
```

#### `TaskCompletedHookInput`

```typescript theme={null}
type TaskCompletedHookInput = BaseHookInput & {
  hook_event_name: "TaskCompleted";
  task_id: string;
  task_subject: string;
  task_description?: string;
  teammate_name?: string;
  /** @deprecated с версии v2.1.178. Содержит имя команды, полученное из сессии; будет удалено. */
  team_name?: string;
};
```

#### `ElicitationHookInput`

```typescript theme={null}
type ElicitationHookInput = BaseHookInput & {
  hook_event_name: "Elicitation";
  mcp_server_name: string;
  message: string;
  mode?: "form" | "url";
  url?: string;
  elicitation_id?: string;
  requested_schema?: Record<string, unknown>;
};
```

#### `ElicitationResultHookInput`

```typescript theme={null}
type ElicitationResultHookInput = BaseHookInput & {
  hook_event_name: "ElicitationResult";
  mcp_server_name: string;
  elicitation_id?: string;
  mode?: "form" | "url";
  action: "accept" | "decline" | "cancel";
  content?: Record<string, unknown>;
};
```

#### `ConfigChangeHookInput`

```typescript theme={null}
type ConfigChangeHookInput = BaseHookInput & {
  hook_event_name: "ConfigChange";
  source:
    | "user_settings"
    | "project_settings"
    | "local_settings"
    | "policy_settings"
    | "skills";
  file_path?: string;
};
```

#### `InstructionsLoadedHookInput`

```typescript theme={null}
type InstructionsLoadedHookInput = BaseHookInput & {
  hook_event_name: "InstructionsLoaded";
  file_path: string;
  memory_type: "User" | "Project" | "Local" | "Managed";
  load_reason:
    | "session_start"
    | "nested_traversal"
    | "path_glob_match"
    | "include"
    | "compact";
  globs?: string[];
  trigger_file_path?: string;
  parent_file_path?: string;
};
```

#### `DirectoryAddedHookInput`

```typescript theme={null}
type DirectoryAddedHookInput = BaseHookInput & {
  hook_event_name: "DirectoryAdded";
  directory: string;
  source: "slash_command" | "register_repo_root";
};
```

`directory` — это абсолютный путь к добавленной директории. `source` — это `"slash_command"`, когда `/add-dir` добавил её, и `"register_repo_root"`, когда это сделал запрос управления SDK.

#### `WorktreeCreateHookInput`

```typescript theme={null}
type WorktreeCreateHookInput = BaseHookInput & {
  hook_event_name: "WorktreeCreate";
  name: string;
};
```

#### `WorktreeRemoveHookInput`

```typescript theme={null}
type WorktreeRemoveHookInput = BaseHookInput & {
  hook_event_name: "WorktreeRemove";
  worktree_path: string;
};
```

#### `CwdChangedHookInput`

```typescript theme={null}
type CwdChangedHookInput = BaseHookInput & {
  hook_event_name: "CwdChanged";
  old_cwd: string;
  new_cwd: string;
};
```

#### `FileChangedHookInput`

```typescript theme={null}
type FileChangedHookInput = BaseHookInput & {
  hook_event_name: "FileChanged";
  file_path: string;
  event: "change" | "add" | "unlink";
};
```

#### `MessageDisplayHookInput`

```typescript theme={null}
type MessageDisplayHookInput = BaseHookInput & {
  hook_event_name: "MessageDisplay";
  turn_id: string;
  message_id: string;
  index: number;
  final: boolean;
  delta: string;
};
```

### `HookJSONOutput`

Возвращаемое значение hook.

```typescript theme={null}
type HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput;
```

#### `AsyncHookJSONOutput`

```typescript theme={null}
type AsyncHookJSONOutput = {
  async: true;
  asyncTimeout?: number;
};
```

#### `SyncHookJSONOutput`

```typescript theme={null}
type SyncHookJSONOutput = {
  continue?: boolean;
  suppressOutput?: boolean;
  stopReason?: string;
  decision?: "approve" | "block";
  systemMessage?: string;
  /**
   * Терминальная escape-последовательность (например OSC 9 / OSC 777 desktop-notification)
   * для Claude Code, которую нужно выдать от вашего имени. Разрешены только notification/title OSCs
   * (0, 1, 2, 9, 99, 777) и BEL; значение, содержащее что-либо ещё, игнорируется целиком. Только интерактивный CLI
   * выдаёт его; SDK игнорирует это поле.
   */
  terminalSequence?: string;
  reason?: string;
  hookSpecificOutput?:
    | {
        hookEventName: "PreToolUse";
        permissionDecision?: "allow" | "deny" | "ask" | "defer";
        permissionDecisionReason?: string;
        updatedInput?: Record<string, unknown>;
        additionalContext?: string;
      }
    | {
        hookEventName: "UserPromptSubmit";
        additionalContext?: string;
        sessionTitle?: string;
        /** Когда decision — "block", исходный промпт не включается в сообщение блокировки. */
        suppressOriginalPrompt?: boolean;
      }
    | {
        hookEventName: "UserPromptExpansion";
        additionalContext?: string;
      }
    | {
        hookEventName: "SessionStart";
        additionalContext?: string;
        initialUserMessage?: string;
        sessionTitle?: string;
        watchPaths?: string[];
        /**
         * Повторно сканировать директории скиллов и команд после завершения хуков SessionStart,
         * чтобы скиллы, установленные хуком, были доступны в той же сессии.
         */
        reloadSkills?: boolean;
      }
    | {
        hookEventName: "Setup";
        additionalContext?: string;
      }
    | {
        hookEventName: "PreModelSwitch";
        /**
         * Тот же контракт, что и PreToolUse: "allow" продолжает, "deny" отменяет
         * переключение, "ask" просит пользователя подтвердить. Только /model в
         * интерактивной сессии показывает этот запрос; каждый другой интерфейс,
         * включая запросы set_model, рассматривает "ask" как отказ.
         */
        permissionDecision?: "allow" | "deny" | "ask";
        permissionDecisionReason?: string;
      }
    | {
        hookEventName: "PostModelSwitch";
        /** Достигает модели со следующим запросом, который обслуживает новая модель. */
        additionalContext?: string;
      }
    | {
        hookEventName: "SubagentStart";
        additionalContext?: string;
      }
    | {
        hookEventName: "PostToolUse";
        additionalContext?: string;
        /**
         * Краткая заметка о результате этого вызова инструмента для классификатора
         * разрешений в авторежиме. Ограничена 2000 символами, общая для
         * всех хуков, которые отвечают на один и тот же вызов; учитывается только при
         * синхронных ответах хука. Не копируйте в неё ненадёжный вывод инструмента.
         */
        classifierContext?: string;
        updatedToolOutput?: unknown;
        /** @deprecated Используйте `updatedToolOutput`, который работает для всех инструментов. */
        updatedMCPToolOutput?: unknown;
      }
    | {
        hookEventName: "PostToolUseFailure";
        additionalContext?: string;
      }
    | {
        hookEventName: "PostToolBatch";
        additionalContext?: string;
      }
    | {
        hookEventName: "Stop";
        additionalContext?: string;
      }
    | {
        hookEventName: "SubagentStop";
        additionalContext?: string;
      }
    | {
        hookEventName: "PermissionDenied";
        retry?: boolean;
      }
    | {
        hookEventName: "Notification";
        additionalContext?: string;
      }
    | {
        hookEventName: "PermissionRequest";
        decision:
          | {
              behavior: "allow";
              updatedInput?: Record<string, unknown>;
              updatedPermissions?: PermissionUpdate[];
            }
          | {
              behavior: "deny";
              message?: string;
              interrupt?: boolean;
            };
      }
    | {
        hookEventName: "Elicitation";
        action?: "accept" | "decline" | "cancel";
        content?: Record<string, unknown>;
      }
    | {
        hookEventName: "ElicitationResult";
        action?: "accept" | "decline" | "cancel";
        content?: Record<string, unknown>;
      }
    | {
        hookEventName: "CwdChanged";
        watchPaths?: string[];
      }
    | {
        hookEventName: "FileChanged";
        watchPaths?: string[];
      }
    | {
        hookEventName: "WorktreeCreate";
        worktreePath: string;
      }
    | {
        hookEventName: "MessageDisplay";
        /** Текст, отображаемый вместо delta. Опустите (или верните delta без изменений), чтобы отобразить исходный. */
        displayContent?: string;
      };
};
```

## Типы входных данных инструментов

Документация схем входных данных для встроенных инструментов Claude Code. Эти типы экспортируются из `@anthropic-ai/claude-agent-sdk/sdk-tools` и могут быть использованы для типобезопасного взаимодействия с инструментами.

Для инструмента `StructuredOutput` здесь нет типа: Claude Code строит его схему входных данных из схемы, которую вы передаёте в `outputFormat`, поэтому экспортировать нечего фиксированного. О том, как этот вызов выглядит в вашем потоке сообщений, см. [Распознавание вызова инструмента StructuredOutput](https://code.claude.com/docs/ru/agent-sdk/structured-outputs.md#recognize-the-structuredoutput-tool-call).

### `ToolInputSchemas`

Объединение типов входных данных инструментов, экспортируемое из `@anthropic-ai/claude-agent-sdk/sdk-tools`; члены включают:

```typescript theme={null}
type ToolInputSchemas =
  | AgentInput
  | ArtifactInput
  | AskUserQuestionInput
  | BashInput
  | CronCreateInput
  | CronDeleteInput
  | CronListInput
  | EnterPlanModeInput
  | EnterWorktreeInput
  | ExitPlanModeInput
  | ExitWorktreeInput
  | FileEditInput
  | FileReadInput
  | FileWriteInput
  | GlobInput
  | GrepInput
  | ListMcpResourcesInput
  | McpInput
  | MonitorInput
  | NotebookEditInput
  | ProjectsInput
  | PushNotificationInput
  | ReadMcpResourceDirInput
  | ReadMcpResourceInput
  | RefreshMcpToolsInput
  | RemoteTriggerInput
  | ReportFindingsInput
  | ScheduleWakeupInput
  | ShowOnboardingRolePickerInput
  | TaskCreateInput
  | TaskGetInput
  | TaskListInput
  | TaskStopInput
  | TaskUpdateInput
  | TodoWriteInput
  | WebFetchInput
  | WebSearchInput
  | WorkflowInput;
```

### Agent

**Имя инструмента:** `Agent`. Предыдущее имя `Task` всё ещё принимается как псевдоним, когда этот инструмент доступен в сессии.

Массив `tools` в сообщении инициализации [`SDKSystemMessage`](#sdksystemmessage) перечисляет этот инструмент как `Task` для обратной совместимости.

> [!NOTE]
>
> Поле `mode` объявлено устаревшим и игнорируется в Claude Code v2.1.212 или позже. Субагент работает либо в режиме разрешений родительской сессии, либо в режиме [`permissionMode`](#agentdefinition) из своего определения, а [правила наследования для субагентов](https://code.claude.com/docs/ru/agent-sdk/permissions.md#available-modes) решают, в каком из них.

```typescript theme={null}
type AgentInput = {
  description: string;
  prompt: string;
  subagent_type?: string;
  model?: "sonnet" | "opus" | "haiku" | "fable";
  effort?: "low" | "medium" | "high" | "xhigh" | "max";
  run_in_background?: boolean;
  name?: string;
  team_name?: string; // Deprecated; ignored
  mode?: "acceptEdits" | "auto" | "bypassPermissions" | "default" | "dontAsk" | "plan"; // Deprecated; ignored. The subagent inheritance rules decide a subagent's permission mode
  isolation?: "worktree" | "remote";
};
```

Запускает нового агента для автономной обработки сложных многошаговых задач.

### AskUserQuestion

**Имя инструмента:** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionInput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
  answers?: Record<string, string>;
  annotations?: Record<string, { preview?: string; notes?: string }>;
  metadata?: { source?: string };
};
```

Задаёт пользователю уточняющие вопросы во время выполнения. См. [Обработка подтверждений и пользовательского ввода](https://code.claude.com/docs/ru/agent-sdk/user-input.md#handle-clarifying-questions) для деталей использования.

### Bash

**Имя инструмента:** `Bash`

```typescript theme={null}
type BashInput = {
  command: string;
  timeout?: number; // milliseconds. Foreground: capped at 600000 by default, higher values are clamped. With run_in_background (Claude Code v2.1.285 or later): the background time limit, 1800000 when omitted, capped at 7200000 unless raised
  description?: string;
  run_in_background?: boolean;
  dangerouslyDisableSandbox?: boolean;
};
```

Выполняет команды Bash с опциональным таймаутом и фоновым выполнением. Рабочий каталог сохраняется между командами, включая команды, запущенные в более поздних ходах многоходовой сессии; состояние оболочки, такое как экспортированные переменные окружения, не сохраняется. Об ограничениях на то, какие изменения каталога переносятся, см. [Что сохраняется между командами](https://code.claude.com/docs/ru/tools-reference.md#what-persists-between-commands). О том, что определяет верхний предел для команд переднего плана, см. [Таймаут и лимиты вывода](https://code.claude.com/docs/ru/tools-reference.md#timeout-and-output-limits). О лимите времени для фоновых команд см. [Лимит времени для фоновых команд](https://code.claude.com/docs/ru/tools-reference.md#time-limit-for-background-commands).

### Monitor

**Имя инструмента:** `Monitor`

```typescript theme={null}
type MonitorInput = {
  description: string;
  timeout_ms: number;
  command?: string;
  ws?: {
    url: string;
    protocols?: string[];
  };
};
```

Запускает фоновый источник и доставляет каждое событие Claude, чтобы он мог реагировать без опроса: `command` запускает скрипт и выдаёт одно событие на строку stdout, а `ws` открывает WebSocket и выдаёт одно событие на текстовый фрейм. Укажите ровно один из `command` или `ws`. Источник `ws` требует Claude Code v2.1.195 или позже.

`timeout_ms` — это крайний срок наблюдения в миллисекундах:

* **Значение по умолчанию и ограничения**: по умолчанию он равен 300000 и принимает значения до 3600000. Эффективный крайний срок составляет максимум 1800000, то есть 30 минут, поэтому большее принятое значение сокращается до него
* **По достижении крайнего срока**: наблюдение заканчивается, и Claude получает одно уведомление, чтобы он мог начать новое наблюдение, если оно ему всё ещё нужно
* **Обязательность в типе**: экспортированный тип отмечает `timeout_ms` как обязательный, потому что схема заполняет значение по умолчанию; вызов, который его опускает, проходит валидацию

Когда Monitor запускает команду, он следует тем же правилам разрешений, что и Bash. О разрешениях для WebSocket, поведении и доступности у провайдеров см. [справочник по инструменту Monitor](https://code.claude.com/docs/ru/tools-reference.md#monitor-tool).

### TaskOutput

Удалён в Claude Code v2.1.277 вместе с его типом `TaskOutputInput`. Ранее получал вывод выполняющейся или завершённой фоновой задачи; теперь Claude читает выходной файл фоновой задачи с помощью `Read`.

Запись `disallowedTools` или правило запрета, которое всё ещё называет `TaskOutput`, игнорируется без предупреждения.

### Edit

**Имя инструмента:** `Edit`

```typescript theme={null}
type FileEditInput = {
  file_path: string;
  old_string: string;
  new_string: string;
  replace_all?: boolean;
};
```

Выполняет точные замены строк в файлах.

### Read

**Имя инструмента:** `Read`

```typescript theme={null}
type FileReadInput = {
  file_path: string;
  offset?: number;
  limit?: number;
  pages?: string;
  allow_large?: boolean;
};
```

Читает файлы из локальной файловой системы, включая текст, изображения, PDF и Jupyter notebooks.

* Используйте `pages` для диапазонов страниц PDF (например, `"1-5"`).
* `allow_large` позволяет Claude прочитать текстовый файл сверх [обычных ограничений размера](https://code.claude.com/docs/ru/tools-reference.md#large-files), когда в контекстном окне сессии есть место. Требует Agent SDK v0.3.296 или позже, который включает Claude Code v2.1.296.

Для PDF Claude получает содержимое файла внутри содержимого `tool_result` вызова Read. Чтение, которое возвращает [вывод](#tool-output-types) `pdf`, содержит блок сводки `text`, за которым следует блок `document`. Чтение, которое возвращает вывод `parts`, содержит блок сводки `text`, за которым следует один блок на каждую извлечённую страницу: блок `image` или блок `text`, называющий страницу, когда Claude Code не смог отобразить её как изображение. До Agent SDK v0.3.242 Claude Code доставлял содержимое файла как отдельное сообщение `user` после результата инструмента.

### Write

**Имя инструмента:** `Write`

```typescript theme={null}
type FileWriteInput = {
  file_path: string;
  content: string;
};
```

Записывает файл в локальную файловую систему, перезаписывая его, если он существует.

### Glob

**Имя инструмента:** `Glob`

```typescript theme={null}
type GlobInput = {
  pattern: string;
  path?: string;
};
```

Быстрое сопоставление паттернов файлов, которое работает с кодовой базой любого размера.

### Grep

**Имя инструмента:** `Grep`

```typescript theme={null}
type GrepInput = {
  pattern: string;
  path?: string;
  glob?: string;
  type?: string;
  output_mode?: "content" | "files_with_matches" | "count";
  "-i"?: boolean;
  "-o"?: boolean; // print only the matched parts of each line; requires output_mode: "content"
  "-n"?: boolean;
  "-B"?: number;
  "-A"?: number;
  "-C"?: number;
  context?: number;
  head_limit?: number;
  offset?: number;
  multiline?: boolean;
};
```

Инструмент поиска на основе ripgrep с поддержкой регулярных выражений.

### TaskStop

**Имя инструмента:** `TaskStop`

```typescript theme={null}
type TaskStopInput = {
  task_id?: string;
  shell_id?: string; // Deprecated: use task_id
};
```

Останавливает выполняющуюся фоновую задачу или оболочку по ID. Начиная с v2.1.198, `task_id` также принимает участника команды агентов или именованного фонового агента по ID агента или имени.

### NotebookEdit

**Имя инструмента:** `NotebookEdit`

```typescript theme={null}
type NotebookEditInput = {
  notebook_path: string;
  cell_id?: string;
  new_source: string;
  cell_type?: "code" | "markdown";
  edit_mode?: "replace" | "insert" | "delete";
};
```

Редактирует ячейки в файлах Jupyter notebook.

### WebFetch

**Имя инструмента:** `WebFetch`

```typescript theme={null}
type WebFetchInput = {
  url: string;
  prompt: string;
  offset?: number;
};
```

Получает содержимое по URL и обрабатывает его с помощью модели AI.

`offset` — это число символов, которые нужно пропустить от начала страницы. Claude устанавливает его, чтобы продолжить чтение длинной страницы. Это поле требует Agent SDK v0.3.290 или позже.

### WebSearch

**Имя инструмента:** `WebSearch`

```typescript theme={null}
type WebSearchInput = {
  query: string;
  allowed_domains?: string[];
  blocked_domains?: string[];
};
```

Выполняет поиск в вебе и возвращает отформатированные результаты.

### Workflow

**Имя инструмента:** `Workflow`

```typescript theme={null}
type WorkflowInput = {
  script?: string;
  name?: string;
  scriptPath?: string;
  args?: unknown; // any JSON value; the published typings render this as an object map
  resumeFromRunId?: string;
  title?: string; // ignored; the script's meta block sets the title
  description?: string; // ignored; the script's meta block sets the description
};
```

Запускает [динамический workflow](https://code.claude.com/docs/ru/workflows.md): скрипт, который оркестрирует множество субагентов в фоне и возвращает один консолидированный результат. Инструмент `Workflow` доступен в Agent SDK v0.3.149 и позже. Требуется хотя бы один из `script`, `name` или `scriptPath`.

| Поле | Тип | Описание |
| - | - | - |
| `script` | `string` | Встроенный скрипт workflow. Должен начинаться с `export const meta = { name, description }` как литерала, за которым следует тело скрипта с использованием `agent()`, `parallel()`, `pipeline()` и `phase()`. Опциональный массив `phases` в `meta` группирует агентов по именованным этапам в представлении прогресса |
| `name` | `string` | Имя встроенного workflow или workflow, сохранённого в `.claude/workflows/`. Разрешается в скрипт |
| `scriptPath` | `string` | Путь к файлу скрипта workflow на диске, например `scriptPath`, который вернул предыдущий запуск. Имеет приоритет над `script` и `name`. Claude Code отклоняет `scriptPath` с ошибкой, если инструменты сессии не включают `Read` |
| `args` | `unknown` | Входное значение, доступное скрипту как глобальная переменная `args`, для параметризованных именованных workflow, таких как исследовательский вопрос или список путей к файлам. Передавайте массивы и объекты как фактические значения JSON, а не как JSON-кодированную строку |
| `resumeFromRunId` | `string` | Run ID предыдущего вызова `Workflow` для возобновления. Завершённые вызовы `agent()` с неизменёнными входными данными обычно возвращают кэшированные результаты; остальные выполняются заново. В разделе [Возобновление после паузы](https://code.claude.com/docs/ru/workflows.md#resume-after-a-pause) описано, какие завершённые вызовы выполняются повторно. Только в той же сессии |
| `title` | `string` | Игнорируется; заголовок задаёт блок `meta` скрипта |
| `description` | `string` | Игнорируется; описание задаёт блок `meta` скрипта |

### TodoWrite

**Имя инструмента:** `TodoWrite`

```typescript theme={null}
type TodoWriteInput = {
  todos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

Создаёт структурированный список задач для отслеживания прогресса и управляет им.

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
> См. [Доступность модели](https://code.claude.com/docs/ru/agent-sdk/todo-tracking.md#model-availability), чтобы включить эту возможность.

### TaskCreate

**Имя инструмента:** `TaskCreate`

```typescript theme={null}
type TaskCreateInput = {
  subject: string;
  description: string;
  activeForm?: string;
  metadata?: Record<string, unknown>;
};
```

Создаёт одну задачу и возвращает назначенный ей ID.

### TaskUpdate

**Имя инструмента:** `TaskUpdate`

```typescript theme={null}
type TaskUpdateInput = {
  taskId: string;
  status?: "pending" | "in_progress" | "completed" | "deleted";
  subject?: string;
  description?: string;
  activeForm?: string;
  addBlocks?: string[];
  addBlockedBy?: string[];
  owner?: string;
  metadata?: Record<string, unknown>;
};
```

Частично обновляет одну задачу по ID. Установите `status` в `"deleted"`, чтобы удалить её.

### TaskGet

**Имя инструмента:** `TaskGet`

```typescript theme={null}
type TaskGetInput = {
  taskId: string;
};
```

Возвращает полные сведения об одной задаче или `null`, если ID не найден.

### TaskList

**Имя инструмента:** `TaskList`

```typescript theme={null}
type TaskListInput = {};
```

Возвращает снимок всех задач в текущем списке.

### ExitPlanMode

**Имя инструмента:** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeInput = {
  /** Deprecated: no longer used. */
  allowedPrompts?: Array<{
    tool: "Bash";
    prompt: string;
  }>;
  [k: string]: unknown;
};
```

Выходит из режима планирования. Поле `allowedPrompts` объявлено устаревшим и игнорируется; Claude Code всё ещё принимает его, чтобы существующие вызывающие стороны и транскрипты проходили валидацию. До v2.1.205 оно запрашивало разрешения Bash на основе промптов для реализации плана.

### ListMcpResources

**Имя инструмента:** `ListMcpResourcesTool`

```typescript theme={null}
type ListMcpResourcesInput = {
  server?: string;
};
```

Перечисляет доступные ресурсы MCP с подключённых серверов.

### ReadMcpResource

**Имя инструмента:** `ReadMcpResourceTool`

```typescript theme={null}
type ReadMcpResourceInput = {
  server: string;
  uri: string;
};
```

Читает определённый ресурс MCP с сервера.

### EnterWorktree

**Имя инструмента:** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeInput = {
  name?: string;
  path?: string;
};
```

Создаёт временный git worktree для изолированной работы и входит в него. Передайте `path`, чтобы переключиться в существующий worktree вместо создания нового. При первом входе целевой каталог должен быть зарегистрированным worktree текущего репозитория или, в многорепозиторном рабочем пространстве, репозитория, вложенного в него; из сессии worktree он должен находиться в `.claude/worktrees/` репозитория сессии. `name` и `path` являются взаимоисключающими.

### ExitWorktree

**Имя инструмента:** `ExitWorktree`

```typescript theme={null}
type ExitWorktreeInput = {
  action: "keep" | "remove";
  discard_changes?: boolean;
};
```

Выходит из текущего git worktree и возвращается в исходный рабочий каталог. Действие `keep` оставляет worktree и ветку на диске, а `remove` удаляет оба. `discard_changes` должно быть `true` при удалении worktree, в котором есть незафиксированные файлы или коммиты без слияния.

### EnterPlanMode

**Имя инструмента:** `EnterPlanMode`

```typescript theme={null}
type EnterPlanModeInput = {};
```

Входит в режим планирования, в котором Claude исследует задачу и представляет план перед внесением изменений.

### CronCreate

**Имя инструмента:** `CronCreate`

```typescript theme={null}
type CronCreateInput = {
  cron: string;
  prompt: string;
  recurring?: boolean;
  durable?: boolean;
};
```

Планирует запуск промпта по расписанию cron из 5 полей в локальном времени. Установите `recurring` в `false`, чтобы он сработал один раз при следующем совпадении. Задачи по умолчанию ограничены сессией, а возобновление с `--resume` или `--continue` восстанавливает задачи, срок действия которых не истёк. См. [Запланированные задачи в рамках сессии](https://code.claude.com/docs/ru/scheduled-tasks.md).

Установка `durable` в `true` запрашивает сохранение в `.claude/scheduled_tasks.json`, чтобы задача пережила перезапуски. Долговременное планирование доступно не в каждой сессии: когда оно недоступно, Claude Code принимает `durable: true`, но создаёт задачу только для текущей сессии. Проверьте поле `durable` в выводе, чтобы узнать, была ли задача сохранена.

### CronDelete

**Имя инструмента:** `CronDelete`

```typescript theme={null}
type CronDeleteInput = {
  id: string;
};
```

Удаляет запланированную задачу cron по ID, возвращённому `CronCreate`.

### CronList

**Имя инструмента:** `CronList`

```typescript theme={null}
type CronListInput = {};
```

Перечисляет запланированные задачи cron: долговременные задачи из `.claude/scheduled_tasks.json` и задачи только для текущей сессии.

### ScheduleWakeup

**Имя инструмента:** `ScheduleWakeup`

```typescript theme={null}
type ScheduleWakeupInput = {
  delaySeconds?: number;
  reason?: string;
  prompt?: string;
  noop?: boolean;
  stop?: boolean;
};
```

Планирует одноразовое пробуждение, которое запускает заданный промпт после задержки. Этот инструмент лежит в основе команды `/loop` с самостоятельным темпом. Среда выполнения ограничивает `delaySeconds` диапазоном от 60 до 3600 секунд. Поля `delaySeconds`, `reason`, `prompt` и `noop` обязательны, если `stop` не равно true. `noop: true` сообщает о пробуждении, при котором ничего не изменилось. Установка `stop: true` отменяет ожидающее пробуждение и завершает `/loop` с самостоятельным темпом. Поле `stop` требует Claude Code v2.1.202 или позже. См. [строку ScheduleWakeup в справочнике по инструментам](https://code.claude.com/docs/ru/tools-reference.md).

### RemoteTrigger

**Имя инструмента:** `RemoteTrigger`

```typescript theme={null}
type RemoteTriggerInput = {
  action:
    | "list"
    | "get"
    | "create"
    | "update"
    | "run"
    | "create_webhook_trigger"
    | "list_runs"
    | "get_run_log";
  trigger_id?: string;
  session_id?: string;
  cursor?: string;
  body?: {
    [k: string]: unknown;
  };
};
```

Управляет [облачными запланированными задачами](https://code.claude.com/docs/ru/routines.md), ранее называвшимися routines: запланированными и запускаемыми по триггеру запусками Claude Code, размещёнными в облаке. Этот инструмент лежит в основе команды `/schedule`. `trigger_id` обязателен для действий `get`, `update`, `run` и `list_runs`. `body` обязателен для `create`, `update` и `create_webhook_trigger` и опционален для `run`.

Каждое из действий `create_webhook_trigger`, `list_runs` и `get_run_log` требует минимальной версии Claude Code:

* **`create_webhook_trigger`**: присоединяет источник событий к существующей запланированной задаче, например [событие GitHub](https://code.claude.com/docs/ru/routines.md#add-a-github-trigger), которое её запускает. `body` указывает источник, события и задачу для запуска. Требует Claude Code v2.1.225 или позже.
* **`list_runs` и `get_run_log`**: `list_runs` перечисляет недавние запуски запланированной задачи, а `get_run_log` читает лог одного запуска. `session_id` указывает запуск для чтения из результата `list_runs`, а `cursor` позволяет постранично перебирать результаты любого из этих действий. Оба действия требуют Claude Code v2.1.227 или позже.

Этот инструмент доступен, только когда сессия аутентифицирована с учётной записью claude.ai на плане с включёнными облачными запланированными задачами. Он отсутствует, когда политика вашей организации отключает [облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md). В Claude Code v2.1.227 или позже инструмент также отсутствует, когда Owner [отключил запланированные задачи для организации](https://code.claude.com/docs/ru/routines.md#routines-are-disabled-by-your-organizations-policy).

### PushNotification

**Имя инструмента:** `PushNotification`

```typescript theme={null}
type PushNotificationInput = {
  message: string;
  status: "proactive";
};
```

Отправляет пользователю проактивное push-уведомление. Держите `message` короче 200 символов, потому что мобильные операционные системы обрезают более длинный текст. См. [строку PushNotification в справочнике по инструментам](https://code.claude.com/docs/ru/tools-reference.md) о доступности у провайдеров; доставка push-уведомлений проходит через инфраструктуру, размещённую Anthropic, которая недоступна из Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform или Microsoft Foundry.

### REPL

Удалён в v2.1.275. До v2.1.274 включительно экспериментальный инструмент `REPL` можно было включить с помощью `CLAUDE_CODE_REPL=1` в опции [`env`](#options).

### ReportFindings

**Имя инструмента:** `ReportFindings`

```typescript theme={null}
type ReportFindingsInput = {
  level?: "low" | "medium" | "high" | "xhigh" | "max";
  findings: Array<{
    file: string;
    line?: number;
    summary: string;
    failure_scenario: string;
    short_summary?: string;
    category?: string;
    verdict?: "CONFIRMED" | "PLAUSIBLE";
    outcome?: "fixed" | "skipped" | "no_change_needed";
  }>;
};
```

Сообщает о результатах код-ревью в виде структурированного списка, чтобы Claude Code мог отобразить их, а не выводить как текст. Результаты упорядочены от наиболее серьёзных, максимум 32 за вызов, и массив пуст, если ни один результат не остался после проверки. Требует Claude Code v2.1.196 или позже.

`level` опционален и содержит уровень effort, который Claude сообщает для ревью. Claude Code не сравнивает его с уровнем, на котором выполнялось ревью, поэтому они могут различаться.

Каждый результат содержит следующие поля:

* `file`: путь относительно репозитория к файлу, в котором находится результат. Опциональный `line` — это строка (нумерация с 1), к которой он привязан.
* `summary`: утверждение о дефекте в одно предложение. `failure_scenario` описывает конкретные входные данные и состояние, которые приводят к неправильному выводу или сбою.
* `short_summary`: опциональная сжатая метка длиной не более 60 символов для компактного отображения. Требует Claude Code v2.1.212 или позже.
* `category`: опциональный короткий слаг типа результата в формате kebab-case, например `correctness` или `test-coverage`. Требует Claude Code v2.1.199 или позже.
* `verdict`: устанавливается, когда выполнялся проход верификации; отсутствует при ревью только с встроенной проверкой.
* `outcome`: устанавливается только при повторном сообщении после применения исправлений.

### Artifact

**Имя инструмента:** `Artifact`

```typescript theme={null}
type ArtifactInput = {
  action?: "publish" | "list";
  file_path?: string;
  favicon?: string;
  icon?: string;
  limit?: number;
  scope?: "mine" | "shared" | "all";
  title?: string;
  description?: string;
  label?: string;
  url?: string;
  force?: boolean;
  capabilities?: Record<string, unknown>;
  contract?: "latest" | string;
};
```

Публикует локальный файл `.html` или `.md` как размещённую страницу артефакта или перечисляет опубликованные артефакты пользователя. Опустите `action` или передайте `"publish"`, чтобы опубликовать `file_path`, который обязателен для действия публикации. Каждое поле ниже относится к публикации:

* `icon`: одно короткое общее слово для значка артефакта на вкладке браузера, например `chart` или `map`. Claude включает его при первой публикации и опускает при обновлении, что сохраняет сохранённый значок артефакта.
* `favicon`: устаревшее, и Claude его опускает.
* `title`: задаёт название опубликованной страницы на вкладке браузера и в галерее, когда в HTML-файле нет тега `<title>`.
* `url`: указывает существующий артефакт, который нужно обновить на месте вместо создания нового.

`force` — это крайняя мера перезаписи, которая отбрасывает более новую версию, опубликованную другой сессией. При конфликте неудачная публикация возвращает более новое содержимое; Claude переносит свои изменения на это содержимое или повторно читает артефакт и публикует снова. Передавайте `force`, только когда пользователь явно просит отбросить эту версию.

Передайте `"list"`, чтобы перечислить опубликованные артефакты пользователя; его могут сопровождать только `limit` и `scope`. `scope` по умолчанию равен `"mine"`, что перечисляет артефакты, которыми владеет пользователь; `"shared"` перечисляет артефакты, которыми другие люди поделились с пользователем, а `"all"` перечисляет и те, и другие.

`limit` задаёт максимальное число артефактов, возвращаемых в списке, от 1 до 200. Значение `limit` больше 50 требует Agent SDK v0.3.292 или позже. Без `limit` список возвращает до 25 артефактов.

* `capabilities`: возможности среды выполнения, которые использует опубликованная страница, с ключами по названию возможности, например [коннекторы, которые может вызывать страница](https://code.claude.com/docs/ru/artifacts.md#pull-live-data-with-mcp-connectors). Сервис артефактов проверяет объявление и отклоняет публикацию, которая указывает возможность, недоступную учётной записи, или задаёт для неё недопустимую конфигурацию. Передайте `{}`, чтобы очистить сохранённое объявление, и опустите поле при повторном развёртывании, чтобы сохранить его. Требует Agent SDK v0.3.235 или позже.
* `contract`: версия среды выполнения, с которой работает опубликованная страница. Опустите её, чтобы сохранить текущую версию артефакта, передайте `"latest"` для обновления или передайте конкретную версию для закрепления или отката. Требует Agent SDK v0.3.235 или позже.

Типы экспортируются, но в сессиях Agent SDK инструмент по умолчанию отключён. Публикация также требует выполнения всех условий из [таблицы доступности артефактов](https://code.claude.com/docs/ru/artifacts.md#availability), которым сессии, аутентифицированные с помощью API-ключа, не удовлетворяют.

### Projects

**Имя инструмента:** `Projects`

```typescript theme={null}
type ProjectsInput = {
  method:
    | "project_info"
    | "project_read"
    | "project_search"
    | "project_write"
    | "project_delete";
  path?: string;
  content?: string;
  local_path?: string;
  present_to_user?: boolean;
  query?: string;
  n?: number;
};
```

Читает и записывает Project claude.ai, присоединённый к сессии. Выбирает операцию по `method`:

* `project_info`: возвращает метаданные проекта и список документов.
* `project_read`: читает один документ по `path`.
* `project_search`: выполняет запрос к базе знаний проекта с помощью `query`. `n` ограничивает число совпадений и по умолчанию равно `5`.
* `project_write`: создаёт или заменяет документ по `path` из ровно одного из источников: `content`, содержащего встроенный текст, или `local_path`, указывающего файл внутри рабочего каталога. `present_to_user: true` отмечает записанный документ как итоговый результат, который пользователю нужно увидеть.
* `project_delete`: удаляет документ по `path`.

### ReadMcpResourceDir

**Имя инструмента:** `ReadMcpResourceDirTool`

```typescript theme={null}
type ReadMcpResourceDirInput = {
  server: string;
  uri: string;
};
```

Перечисляет непосредственных потомков ресурса-каталога на MCP-сервере. Можно использовать только с сервером, который объявил поддержку перечисления каталогов; перечисление не рекурсивное. Перечисление каталогов включено не в каждой сессии: когда оно отключено, вызов возвращает пустой список `resources`, а поле `error` сообщает, что перечисление каталогов не включено.

### RefreshMcpTools

**Имя инструмента:** `RefreshMcpTools`

```typescript theme={null}
type RefreshMcpToolsInput = {
  server?: string; // refresh only this server; omit to refresh all connected servers
};
```

Повторно запрашивает список инструментов подключённых MCP-серверов и применяет любые изменения. Типы экспортируются, но Claude Code регистрирует инструмент, только когда вы устанавливаете `CLAUDE_CODE_ENABLE_REFRESH_MCP_TOOLS=1` в опции [`env`](#options), и только в сессиях хотя бы с одним MCP-сервером. Требует Claude Code v2.1.211 или позже.

### ShowOnboardingRolePicker

**Имя инструмента:** `ShowOnboardingRolePicker`

```typescript theme={null}
type ShowOnboardingRolePickerInput = {};
```

Отображает кликабельный ряд чипов выбора роли во время онбординга Cowork, чтобы пользователь мог выбрать свою роль и получить установленный соответствующий плагин. Не принимает аргументов; список ролей определяется клиентом. Вызов блокируется до ответа пользователя.

### McpInput

**Имя инструмента:** динамические имена инструментов MCP вида `mcp__<server>__<tool>`

```typescript theme={null}
type McpInput = {
  [k: string]: unknown;
};
```

Аргументы инструментов MCP — это открытый объект: каждый сервер определяет собственные параметры, поэтому тип не накладывает ограничений на имена полей или значения. Поля, которые принимает конкретный инструмент, смотрите в собственной схеме инструментов сервера.

## Типы вывода инструментов

Документация схем вывода для встроенных инструментов Claude Code. Эти типы экспортируются из `@anthropic-ai/claude-agent-sdk/sdk-tools` и представляют фактические данные ответа, возвращаемые каждым инструментом.

### `ToolOutputSchemas`

Объединение типов вывода инструментов, экспортируемое из `@anthropic-ai/claude-agent-sdk/sdk-tools`; в него входят:

```typescript theme={null}
type ToolOutputSchemas =
  | AgentOutput
  | ArtifactOutput
  | AskUserQuestionOutput
  | BashOutput
  | CronCreateOutput
  | CronDeleteOutput
  | CronListOutput
  | EnterPlanModeOutput
  | EnterWorktreeOutput
  | ExitPlanModeOutput
  | ExitWorktreeOutput
  | FileEditOutput
  | FileReadOutput
  | FileWriteOutput
  | GlobOutput
  | GrepOutput
  | ListMcpResourcesOutput
  | McpOutput
  | MonitorOutput
  | NotebookEditOutput
  | ProjectsOutput
  | PushNotificationOutput
  | ReadMcpResourceDirOutput
  | ReadMcpResourceOutput
  | RefreshMcpToolsOutput
  | RemoteTriggerOutput
  | ReportFindingsOutput
  | ScheduleWakeupOutput
  | ShowOnboardingRolePickerOutput
  | TaskCreateOutput
  | TaskGetOutput
  | TaskListOutput
  | TaskStopOutput
  | TaskUpdateOutput
  | TodoWriteOutput
  | WebFetchOutput
  | WebSearchOutput
  | WorkflowOutput;
```

### Agent

**Имя инструмента:** `Agent`. Прежнее имя `Task` по-прежнему принимается как псевдоним, если этот инструмент доступен в сессии.

```typescript theme={null}
type AgentOutput =
  | {
      status: "completed";
      agentId: string;
      agentType?: string;
      content: Array<{ type: "text"; text: string; citations?: unknown[] | null }>;
      resolvedModel?: string;
      modelsUsed?: string[];
      totalToolUseCount: number;
      totalDurationMs: number;
      totalTokens: number;
      usage: {
        input_tokens: number;
        output_tokens: number;
        cache_creation_input_tokens: number | null;
        cache_read_input_tokens: number | null;
        server_tool_use: {
          web_search_requests: number;
          web_fetch_requests: number;
        } | null;
        service_tier: string | null;
        cache_creation: {
          ephemeral_1h_input_tokens: number;
          ephemeral_5m_input_tokens: number;
        } | null;
        inference_geo?: string | null;
        speed?: string | null;
        iterations?: unknown;
        output_tokens_details?: {
          thinking_tokens?: number | null;
        } | null;
        fallback_credit?: unknown;
      };
      toolStats?: {
        readCount: number;
        searchCount: number;
        bashCount: number;
        editFileCount: number;
        linesAdded: number;
        linesRemoved: number;
        otherToolCount: number;
        frameCount?: number;
      };
      prompt: string;
      worktreePath?: string;
      worktreeBranch?: string;
    }
  | {
      status: "async_launched";
      isAsync?: true;
      agentId: string;
      description: string;
      resolvedModel?: string;
      modelsUsed?: string[];
      prompt: string;
      outputFile: string;
      canReadOutputFile?: boolean;
    }
  | {
      status: "remote_launched";
      taskId: string;
      sessionUrl: string;
      description: string;
      prompt: string;
      outputFile: string;
    };
```

Возвращает результат работы субагента. Варианты различаются по полю `status`: `"completed"` для завершённых задач, `"async_launched"` для фоновых задач и `"remote_launched"` для задач, которые Claude Code отправил в облачную сессию; в этом случае `sessionUrl` ссылается на эту сессию, а `taskId` её идентифицирует.

В варианте `completed` поле `resolvedModel` указывает модель, с которой начал работу субагент; она может отличаться от запрошенного входного параметра `model`, если действует [`availableModels`](https://code.claude.com/docs/ru/model-config#restrict-model-selection) или другое переопределение. Для этого поля требуется Claude Code v2.1.174 или новее. В варианте `async_launched` оно указывает модель, которая использовалась в момент перевода задачи в фоновый режим.

`modelsUsed` перечисляет модели, которые использовал субагент, по порядку. Поле присутствует только в том случае, если во время выполнения произошла смена модели, и модель появляется в списке повторно, если выполнение снова переключилось на неё. В варианте `async_launched` список охватывает модели, использованные до перевода в фоновый режим. Как для `modelsUsed`, так и для поведения `resolvedModel` при переводе в фоновый режим требуется Claude Code v2.1.212 или новее.

Если Claude Code [сохранил изолированный worktree субагента](https://code.claude.com/docs/ru/worktrees.md#isolate-subagents-with-worktrees), поле `worktreePath` в результате `completed` указывает, где его найти. `worktreeBranch` — его ветка; поле присутствует, если Claude Code создал worktree с помощью git.

Claude Code заполняет `usage` и `totalTokens` на основе последнего запроса субагента к API, а не всего выполнения, поэтому `usage.service_tier` — это строка уровня обслуживания, которую API сообщил для этого запроса. Если поле `usage.output_tokens_details.thinking_tokens` присутствует, оно содержит количество выходных токенов этого запроса, которые были токенами мышления. Для поля `output_tokens_details` требуется TypeScript SDK v0.3.228 или новее, в состав которого входит Claude Code v2.1.228. Для поля `fallback_credit` требуется TypeScript SDK v0.3.285 или новее, в состав которого входит Claude Code v2.1.285.

`usage.output_tokens_details` по смыслу соответствует [`Usage.output_tokens_details`](#usage), но ограничено этим последним запросом, при этом здесь каждый его уровень необязателен. Проверяйте как объект, так и поле, например `usage.output_tokens_details?.thinking_tokens ?? 0`, а не обращайтесь к нему напрямую.

До v2.1.207 опубликованный тип был уже. В нём отсутствовали `worktreePath`, `worktreeBranch`, `citations`, `toolStats.frameCount`, а также поля использования `inference_geo`, `speed` и `iterations`, а `service_tier` имел тип `"standard" | "priority" | "batch"`. Поля, помеченные в типе как необязательные, могут отсутствовать в результатах, записанных более ранними версиями.

### AskUserQuestion

**Имя инструмента:** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionOutput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
  answers: Record<string, string>;
  response?: string;
  annotations?: Record<string, { preview?: string; notes?: string }>;
  afkTimeoutMs?: number;
};
```

Возвращает заданные вопросы и ответы пользователя. Поле `response` устанавливается, если пользователь ввёл ответ в свободной форме вместо ответов на структурированные вопросы; если оно присутствует, Claude получает «The user responded: …» вместо списка ответов по каждому вопросу.

### Bash

**Имя инструмента:** `Bash`

```typescript theme={null}
type BashOutput = {
  stdout: string;
  stderr: string;
  rawOutputPath?: string;
  interrupted: boolean;
  isImage?: boolean;
  backgroundTaskId?: string;
  backgroundedByUser?: boolean;
  timedOutAfterMs?: number;
  backgroundCwdHint?: string;
  backgroundEndsWithFinalResponse?: true;
  dangerouslyDisableSandbox?: boolean;
  returnCodeInterpretation?: string;
  noOutputExpected?: boolean;
  structuredContent?: unknown[];
  persistedOutputPath?: string;
  persistedOutputSize?: number;
  staleReadFileStateHint?: string;
  ghRateLimitHint?: string;
  gitOperation?: {
    commit?: { sha: string; kind: "committed" | "amended" | "cherry-picked"; branch?: string };
    push?: { branch: string };
    branch?: { ref: string; action: "merged" | "rebased" };
    pr?: {
      number: number;
      url?: string;
      action: "created" | "edited" | "merged" | "commented" | "closed" | "reopened" | "ready" | "draft" | "auto-merge-enabled" | "auto-merge-disabled";
    };
  };
};
```

Поля `stdout`, `stderr` и `backgroundTaskId` содержат:

| Поле | Что содержит |
| - | - |
| `stdout` | stdout и stderr команды, объединённые в один чередующийся поток |
| `stderr` | Уведомления, добавляемые самим инструментом, например о сбросе рабочего каталога оболочки, а не stderr команды |
| `backgroundTaskId` | Присутствует для фоновых команд |

`timedOutAfterMs` — таймаут в миллисекундах; устанавливается, если команда достигла таймаута и была переведена в фоновый режим, а не запущена в нём явно. `backgroundCwdHint` устанавливается, если фоновая команда содержала встроенную команду смены каталога, например `cd`, `pushd`, `popd` или `chdir`, и сообщает, что рабочий каталог сессии не изменился. Для обоих полей требуется Claude Code v2.1.210 или новее.

Если фоновая команда принадлежит субагенту, работающему на переднем плане, команда [завершается, когда завершается выполнение этого субагента](https://code.claude.com/docs/ru/tools-reference.md#when-a-background-command-stops). Claude Code устанавливает для таких команд `backgroundEndsWithFinalResponse` в значение `true` и опускает это поле, если команда переживает ход, как это происходит с командами, запущенными основным диалогом или фоновыми субагентами. Для этого поля требуется Claude Code v2.1.227 или новее.

Claude Code устанавливает `gitOperation.commit.branch` в значение ветки, указанной в итоговой строке коммита git, и опускает это поле для коммита, сделанного в состоянии detached HEAD. Для этого поля требуется Agent SDK v0.3.227 или новее. Claude Code сообщает о команде `gh pr reopen` как о действии PR `reopened`; для этого требуется Agent SDK v0.3.234 или новее.

### Monitor

**Имя инструмента:** `Monitor`

```typescript theme={null}
type MonitorOutput = {
  taskId: string;
  timeoutMs: number;
  persistent?: boolean;
};
```

Возвращает идентификатор фоновой задачи для запущенного монитора. Используйте этот идентификатор с `TaskStop`, чтобы досрочно отменить наблюдение.

### Edit

**Имя инструмента:** `Edit`

```typescript theme={null}
type FileEditOutput = {
  filePath: string;
  oldString: string;
  newString: string;
  originalFile: string | null;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  userModified: boolean;
  replaceAll: boolean;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
    repository?: string | null;
  };
};
```

Возвращает структурированный diff операции редактирования.

### Read

**Имя инструмента:** `Read`

```typescript theme={null}
type FileReadOutput =
  | {
      type: "text";
      file: {
        filePath: string;
        content: string;
        numLines: number;
        startLine: number;
        totalLines: number;
        /** True when a whole-file read was auto-paginated because it exceeded the token cap (the content is a partial first page). */
        truncatedByTokenCap?: boolean;
      };
    }
  | {
      type: "image";
      file: {
        base64: string;
        type: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
        originalSize: number;
        dimensions?: {
          originalWidth?: number;
          originalHeight?: number;
          displayWidth?: number;
          displayHeight?: number;
        };
      };
    }
  | {
      type: "notebook";
      file: {
        filePath: string;
        cells: unknown[];
      };
    }
  | {
      type: "pdf";
      file: {
        filePath: string;
        base64: string;
        originalSize: number;
      };
    }
  | {
      type: "parts";
      file: {
        filePath: string;
        originalSize: number;
        count: number;
        outputDir: string;
      };
      /** Document page number of the first extracted page; labels the page images in the tool_result content. */
      firstPage?: number;
      /** In-process only: the page-image bytes are delivered as image blocks in the tool_result content and aren't retained on the emitted tool_use_result, so this key is absent there. */
      pages?: {
        base64: string;
        mediaType: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
        error?: string;
      }[];
    }
  | {
      type: "file_unchanged";
      file: {
        filePath: string;
      };
      /** Set when the dedup matched a startup-seeded entry (CLAUDE.md / nested memory) rather than a prior Read tool_result. */
      source?: "seeded";
    };
```

Возвращает содержимое файла в формате, соответствующем типу файла. Варианты различаются по полю `type`.

### Write

**Имя инструмента:** `Write`

```typescript theme={null}
type FileWriteOutput = {
  type: "create" | "update";
  filePath: string;
  content: string;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  originalFile: string | null;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
    repository?: string | null;
  };
  userModified?: boolean;
};
```

Возвращает результат записи со структурированной информацией diff. Содержимое `originalFile` и `structuredPatch` зависит от записи:

* Для вновь созданного файла `originalFile` равно null, а `structuredPatch` пусто
* При перезаписи `originalFile` содержит прежнее содержимое, за исключением случаев, когда это содержимое больше примерно 10 МБ: тогда Claude Code пропускает diff и возвращает `originalFile` равным null и пустой `structuredPatch`
* `structuredPatch` также пусто, если запись ничего не изменила или построение diff превысило таймаут

### Glob

**Имя инструмента:** `Glob`

```typescript theme={null}
type GlobOutput = {
  durationMs: number;
  numFiles: number;
  filenames: string[];
  truncated: boolean;
  totalMatches?: number;
  countIsComplete?: boolean;
};
```

Возвращает пути к файлам, соответствующие glob-шаблону, отсортированные по времени изменения.

Для `totalMatches` и `countIsComplete` требуется Claude Code v2.1.191 или новее. `totalMatches` сообщает количество совпавших файлов до усечения. Если `countIsComplete` равно false, `totalMatches` является нижней границей, поскольку лежащий в основе поиск усёк собственный вывод.

### Grep

**Имя инструмента:** `Grep`

```typescript theme={null}
type GrepOutput = {
  mode?: "content" | "files_with_matches" | "count";
  numFiles: number;
  filenames: string[];
  content?: string;
  numLines?: number;
  numMatches?: number;
  totalFiles?: number;
  totalLines?: number;
  appliedLimit?: number;
  appliedOffset?: number;
  timedOut?: boolean;
};
```

Возвращает результаты поиска. Форма зависит от `mode`: список файлов, содержимое с совпадениями или количество совпадений. В режиме `count` поля `numFiles` и `numMatches` являются итогами по всему набору результатов, а не по странице пагинации. До v2.1.208 параметры `head_limit` или `offset`, усекавшие перечисленные записи, усекали и эти итоги.

Для `totalFiles` требуется Claude Code v2.1.208 или новее; поле сообщает общее количество результатов до пагинации с помощью `head_limit` и `offset` в режиме `files_with_matches`. Для `totalLines` требуется Claude Code v2.1.210 или новее; поле сообщает общее количество строк до пагинации в режиме `content`. Для `timedOut` требуется Claude Code v2.1.317 или новее; поле равно `true`, если время поиска истекло, поэтому результаты могут быть неполными.

### TaskStop

**Имя инструмента:** `TaskStop`

```typescript theme={null}
type TaskStopOutput = {
  message: string;
  task_id: string;
  task_type: string;
  command?: string;
};
```

Возвращает подтверждение после остановки фоновой задачи.

### NotebookEdit

**Имя инструмента:** `NotebookEdit`

```typescript theme={null}
type NotebookEditOutput = {
  new_source: string;
  old_source?: string;
  cell_id?: string;
  cell_type: "code" | "markdown";
  language: string;
  edit_mode: string;
  error?: string;
  notebook_path: string;
  original_file: string;
  updated_file: string;
};
```

Возвращает результат редактирования блокнота с исходным и обновлённым содержимым файла.

### WebFetch

**Имя инструмента:** `WebFetch`

```typescript theme={null}
type WebFetchOutput = {
  bytes: number;
  code: number;
  codeText: string;
  result: string;
  durationMs: number;
  url: string;
  artifactRead?: {
    slug: string;
    ver?: string;
    seeded?: false;
  };
};
```

Возвращает полученное содержимое с HTTP-статусом и метаданными.

`artifactRead` — собственная запись Claude Code о чтении артефакта; присутствует, только если Claude получил артефакт, в который сессия может публиковать. Claude Code считывает её при возобновлении сессии, чтобы последующая публикация основывалась на правильной версии; вашему коду не нужно ничего с ней делать. `slug` указывает артефакт, `ver` — версия, зафиксированная при чтении (отсутствует, если версия не была зафиксирована), а `seeded: false` помечает чтение, при котором полный исходный код не дошёл до Claude. Для поля `seeded` требуется Agent SDK v0.3.239 или новее.

### WebSearch

**Имя инструмента:** `WebSearch`

```typescript theme={null}
type WebSearchOutput = {
  query: string;
  results: Array<
    | {
        tool_use_id: string;
        content: Array<{ title: string; url: string }>;
      }
    | string
  >;
  durationSeconds: number;
  searchCount?: number;
};
```

Возвращает результаты поиска в интернете.

### Workflow

**Имя инструмента:** `Workflow`

```typescript theme={null}
type WorkflowOutput = {
  status: "async_launched" | "remote_launched";
  taskId: string;
  taskType?: "local_workflow" | "remote_agent";
  workflowName?: string;
  runId?: string;
  summary?: string;
  transcriptDir?: string;
  scriptPath?: string;
  sessionUrl?: string; // set when the workflow launched as a cloud session
  warning?: string;
  error?: string;
};
```

Возвращается сразу после того, как инструмент принял вызов. Итоговый результат поступает позже в виде завершения задачи. Проверьте `error`, прежде чем считать запуск начавшимся: скрипт, не прошедший проверку синтаксиса, возвращает `status: "async_launched"` с установленным `error` и никогда не выполняется.

| Поле | Тип | Описание |
| - | - | - |
| `status` | `"async_launched" \| "remote_launched"` | Инструмент принял вызов. `"async_launched"` для запусков внутри процесса, `"remote_launched"` для запусков, отправленных в облачную сессию вместо выполнения внутри процесса |
| `taskId` | `string` | Идентификатор фоновой задачи для запуска |
| `taskType` | `"local_workflow" \| "remote_agent"` | Тип зарегистрированной фоновой задачи, соответствующий варианту `status` |
| `workflowName` | `string` | Значение `meta.name` из скрипта workflow |
| `runId` | `string` | Идентификатор запуска workflow, который нужно передать как `resumeFromRunId` при последующем вызове. Отсутствует для запусков `remote_launched`, где дескриптором возобновления служит URL облачной сессии |
| `summary` | `string` | Однострочное описание того, что делает workflow |
| `transcriptDir` | `string` | Каталог, в который во время выполнения записываются транскрипты субагентов |
| `scriptPath` | `string` | Путь к сохранённому скрипту workflow для этого запуска. Отредактируйте его и передайте обратно как `scriptPath`, чтобы перезапустить без повторной отправки скрипта |
| `sessionUrl` | `string` | URL облачной сессии; устанавливается, если `status` равен `"remote_launched"` |
| `warning` | `string` | Неблокирующее предупреждение, например о расхождении локального состояния git с отправленной веткой, которую клонирует облачная сессия |
| `error` | `string` | Устанавливается, если скрипт не прошёл проверку синтаксиса. Если поле присутствует, запуск не начался, несмотря на статус запуска |

### TodoWrite

**Имя инструмента:** `TodoWrite`

```typescript theme={null}
type TodoWriteOutput = {
  oldTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
  newTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

Возвращает предыдущий и обновлённый списки задач.

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
> Чтобы включить эту возможность, см. [Доступность моделей](https://code.claude.com/docs/ru/agent-sdk/todo-tracking.md#model-availability).

### TaskCreate

**Имя инструмента:** `TaskCreate`

```typescript theme={null}
type TaskCreateOutput = {
  task: {
    id: string;
    subject: string;
  };
};
```

Возвращает созданную задачу с присвоенным ей идентификатором.

### TaskUpdate

**Имя инструмента:** `TaskUpdate`

```typescript theme={null}
type TaskUpdateOutput = {
  success: boolean;
  taskId: string;
  updatedFields: string[];
  error?: string;
  statusChange?: {
    from: string;
    to: string;
  };
};
```

Возвращает результат обновления, включая сведения о том, какие поля изменились.

### TaskGet

**Имя инструмента:** `TaskGet`

```typescript theme={null}
type TaskGetOutput = {
  task: {
    id: string;
    subject: string;
    description: string;
    status: "pending" | "in_progress" | "completed";
    blocks: string[];
    blockedBy: string[];
  } | null;
};
```

Возвращает полную запись задачи или `null`, если идентификатор не найден.

### TaskList

**Имя инструмента:** `TaskList`

```typescript theme={null}
type TaskListOutput = {
  tasks: Array<{
    id: string;
    subject: string;
    status: "pending" | "in_progress" | "completed";
    owner?: string;
    blockedBy: string[];
  }>;
};
```

Возвращает снимок всех задач в текущем списке.

### ExitPlanMode

**Имя инструмента:** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeOutput = {
  plan: string | null;
  isAgent: boolean;
  filePath?: string;
  hasTaskTool?: boolean;
  planWasEdited?: boolean;
  awaitingLeaderApproval?: boolean;
  requestId?: string;
};
```

Возвращает состояние плана после выхода из режима планирования.

### ListMcpResources

**Имя инструмента:** `ListMcpResourcesTool`

```typescript theme={null}
type ListMcpResourcesOutput = Array<{
  uri: string;
  name: string;
  mimeType?: string;
  description?: string;
  server: string;
}>;
```

Возвращает массив доступных ресурсов MCP.

### ReadMcpResource

**Имя инструмента:** `ReadMcpResourceTool`

```typescript theme={null}
type ReadMcpResourceOutput = {
  contents: Array<{
    uri: string;
    mimeType?: string;
    text?: string;
    blobSavedTo?: string;
  }>;
  error?: string;
};
```

Возвращает содержимое запрошенного ресурса MCP.

### EnterWorktree

**Имя инструмента:** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeOutput = {
  worktreePath: string;
  worktreeBranch?: string;
  message: string;
};
```

Возвращает информацию о git worktree.

### ExitWorktree

**Имя инструмента:** `ExitWorktree`

```typescript theme={null}
type ExitWorktreeOutput = {
  action: "keep" | "remove";
  originalCwd: string;
  worktreePath: string;
  worktreeBranch?: string;
  tmuxSessionName?: string;
  discardedFiles?: number;
  discardedCommits?: number;
  message: string;
};
```

Возвращает выполненное действие и сведения о worktree, из которого был выполнен выход.

### EnterPlanMode

**Имя инструмента:** `EnterPlanMode`

```typescript theme={null}
type EnterPlanModeOutput = {
  message: string;
};
```

Возвращает подтверждение входа в режим планирования.

### CronCreate

**Имя инструмента:** `CronCreate`

```typescript theme={null}
type CronCreateOutput = {
  id: string;
  humanSchedule: string;
  recurring: boolean;
  durable?: boolean; // true when persisted to .claude/scheduled_tasks.json; false when session-only
  nextFireAt?: number;
};
```

Возвращает идентификатор задания, понятное человеку описание расписания и время следующего запуска. `nextFireAt` указывает это время в миллисекундах от эпохи с уже применённым [джиттером](https://code.claude.com/docs/ru/scheduled-tasks.md#jitter), то есть это момент, на который назначен запуск задания. Для этого поля требуется TypeScript Agent SDK v0.3.299 или новее и Claude Code v2.1.299 или новее.

### CronDelete

**Имя инструмента:** `CronDelete`

```typescript theme={null}
type CronDeleteOutput = {
  id: string;
};
```

Возвращает идентификатор удалённого задания.

### CronList

**Имя инструмента:** `CronList`

```typescript theme={null}
type CronListOutput = {
  jobs: {
    id: string;
    cron: string;
    humanSchedule: string;
    prompt: string;
    recurring?: boolean;
    durable?: boolean;
    nextFireAt?: number;
  }[];
};
```

Возвращает запланированные задания cron: постоянные задания из `.claude/scheduled_tasks.json` и задания текущей сессии, существующие только в её рамках. Задание, существующее только в рамках сессии, содержит `durable: false`; у заданий, считанных с диска, это поле отсутствует.

`nextFireAt` — время следующего запуска задания в миллисекундах от эпохи с учётом [джиттера](https://code.claude.com/docs/ru/scheduled-tasks.md#jitter). Ни одно значение не бывает раньше момента вызова `CronList`: задание, время которого [прошло без запуска](https://code.claude.com/docs/ru/scheduled-tasks.md#how-scheduled-tasks-run), содержит время вызова. Для этого поля требуется TypeScript Agent SDK v0.3.299 или новее и Claude Code v2.1.299 или новее.

### ScheduleWakeup

**Имя инструмента:** `ScheduleWakeup`

```typescript theme={null}
type ScheduleWakeupOutput = {
  scheduledFor: number;
  clampedDelaySeconds: number;
  wasClamped: boolean;
  stopped?: boolean;
  cancelledWakeups?: number;
};
```

Возвращает момент срабатывания пробуждения в виде метки времени в миллисекундах от эпохи, фактически использованную задержку и сведения о том, была ли запрошенная задержка ограничена. Поле `stopped` равно `true`, если вызов завершил цикл с помощью `stop: true`. Для него требуется Claude Code v2.1.202 или новее. Поле `cancelledWakeups` содержит количество ожидающих пробуждений, отменённых вызовом `stop: true`. Значение 0 означает, что ожидающих пробуждений не было; повторяющийся cron `/loop` вызовом `stop: true` не отменяется. Для него требуется Claude Code v2.1.206 или новее.

### RemoteTrigger

**Имя инструмента:** `RemoteTrigger`

```typescript theme={null}
type RemoteTriggerOutput = {
  status: number;
  json: string;
  summary?: string;
};
```

Возвращает статус и тело ответа API для операции с триггером.

### PushNotification

**Имя инструмента:** `PushNotification`

```typescript theme={null}
type PushNotificationOutput = {
  message: string;
  pushSent?: boolean;
  localSent?: boolean;
  disabledReason?: "config_off" | "user_present" | "no_transport";
  sentAt?: string;
};
```

Возвращает сведения о доставке, в том числе о том, было ли отправлено push-уведомление или локальное уведомление, и почему доставка была пропущена.

### ReportFindings

**Имя инструмента:** `ReportFindings`

```typescript theme={null}
type ReportFindingsOutput = {
  count: number;
  level?: "low" | "medium" | "high" | "xhigh" | "max";
  findings: Array<{
    file: string;
    line?: number;
    summary: string;
    failure_scenario: string;
    short_summary?: string;
    category?: string;
    verdict?: "CONFIRMED" | "PLAUSIBLE";
    outcome?: "fixed" | "skipped" | "no_change_needed";
  }>;
};
```

Возвращает количество сообщённых находок, значение `level`, переданное Claude, и находки, возвращённые обратно для тела результата. Требуется Claude Code v2.1.196 или новее. Для возвращаемого поля `short_summary` требуется Claude Code v2.1.212 или новее.

### Artifact

**Имя инструмента:** `Artifact`

```typescript theme={null}
type ArtifactOutput =
  | {
      url: string;
      path: string;
      title?: string;
      version?: string;
      capabilities?: unknown;
      stored?: {
        contract: string;
        capabilities?: Record<string, unknown>;
      };
      warnings?: string[];
      contract?: string;
      updated?: boolean;
      liveSubscription?: string;
    }
  | {
      artifacts: Array<{
        title: string;
        url: string;
        updatedAt?: string;
        rel?: "mine" | "shared";
      }>;
      truncated?: boolean;
      total?: number;
      total_at_least?: true;
      scope?: "shared" | "all";
    };
```

Для действия публикации возвращает `url` опубликованной страницы и локальный `path`, который был опубликован; `updated` равно true, если публикация повторно развернула существующий артефакт, а `warnings` содержит предупреждения, возникшие при публикации. Действие получения списка вместо этого возвращает строки `artifacts`, а `truncated` устанавливается, если артефактов больше, чем запрошенный лимит. В списках, область действия которых отличается от `"mine"`, каждая строка содержит `rel`, указывающее, принадлежит ли артефакт пользователю или им поделились с пользователем, а поле `scope` в выводе фиксирует, какая нестандартная область действия сформировала список; в списках по умолчанию оба поля отсутствуют.

Результат получения списка также сообщает `total` — количество артефактов, соответствующих области действия списка, включая те, что выходят за пределы `limit`. Если установлено `total_at_least`, это число является нижней границей, и артефактов может быть больше. Для обоих полей требуется Agent SDK v0.3.292 или новее.

### Projects

**Имя инструмента:** `Projects`

```typescript theme={null}
type ProjectsOutput =
  | {
      method: "project_info";
      notice?: string;
      name: string;
      description: string;
      instructions: string;
      docs: Array<{ path: string; created_at: string | null }>;
      files?: Array<{
        path: string;
        file_kind: string;
        created_at: string | null;
      }>;
      sync_sources?: Array<{
        type: string | null;
        config: Record<string, unknown>;
      }>;
      knowledge: {
        knowledge_size: number;
        max_knowledge_size: number;
      };
    }
  | {
      method: "project_read";
      notice?: string;
      path: string;
      file_kind?: string;
      content?: string;
      local_file?: string;
      created_at: string | null;
    }
  | {
      method: "project_search";
      notice?: string;
      rag: boolean;
      hits?: Array<{ name?: string; doc_uuid?: string; text?: string }>;
      docs?: string[];
    }
  | {
      method: "project_write";
      notice?: string;
      path: string;
      doc_uuid: string;
      replaced: boolean;
      present_to_user?: boolean;
      local_path?: string;
    }
  | {
      method: "project_delete";
      notice?: string;
      path: string;
      deleted: boolean;
    };
```

Варианты различаются по полю `method`, как и во входных данных. `project_read` возвращает небольшие текстовые документы непосредственно в `content`, а более крупные документы записывает по пути `local_file`; `project_search` возвращает RAG-результаты `hits` с `rag: true`, если индекс проекта доступен, а в противном случае возвращает список путей `docs`.

### ReadMcpResourceDir

**Имя инструмента:** `ReadMcpResourceDirTool`

```typescript theme={null}
type ReadMcpResourceDirOutput = {
  resources: Array<{
    uri: string;
    name: string;
    mimeType?: string;
  }>;
  error?: string;
};
```

Возвращает непосредственные дочерние элементы ресурса-каталога. Подкаталоги отображаются с mimeType `"inode/directory"`; `error` содержит понятное человеку сообщение, если серверу не удалось получить список содержимого каталога.

### RefreshMcpTools

**Имя инструмента:** `RefreshMcpTools`

```typescript theme={null}
type RefreshMcpToolsOutput = Array<{
  server: string;
  status: "refreshed" | "error" | "not_connected";
  toolCount?: number; // tools now available from this server
  added?: string[]; // tool names this refresh added
  removed?: string[]; // tool names this refresh removed
  error?: string; // why the refresh failed or the server was unavailable
}>;
```

Возвращает по одной записи на сервер: `refreshed` означает, что повторно запрошенный список инструментов был применён, `error` означает, что повторный запрос завершился ошибкой и был сохранён прежний набор инструментов, а `not_connected` означает, что у сервера нет активного подключения для запроса.

### ShowOnboardingRolePicker

**Имя инструмента:** `ShowOnboardingRolePicker`

```typescript theme={null}
type ShowOnboardingRolePickerOutput = {
  role?: string;
  dismissed?: boolean;
};
```

Возвращает выбор пользователя: `role`, если пользователь выбрал роль из предложенных вариантов или ввёл её, и `dismissed: true`, если пользователь закрыл окно выбора. Пустой объект означает, что пользователь одобрил вызов, не выбрав роль.

### McpOutput

**Имя инструмента:** динамические имена инструментов MCP вида `mcp__<server>__<tool>`

```typescript theme={null}
type McpOutput =
  | string
  | {
      type: string;
      [k: string]: unknown;
    }[]
  | {
      [k: string]: unknown;
    };
```

Результаты инструментов MCP возвращаются в виде строки или массива блоков содержимого в зависимости от сервера. Завершающая ветка с простым объектом в экспортируемом типе является артефактом генерации схемы. Для результата, который также содержит `structuredContent` или ссылки на ресурсы, см. [`tool_use_result`](#sdkusermessage), где это значение хранится в члене `content`. Во время выполнения значение также может быть `undefined`, хотя экспортируемый тип этого не отражает.

## Типы разрешений

### `PermissionUpdate`

Операции для обновления разрешений.

```typescript theme={null}
type PermissionUpdate =
  | {
      type: "addRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "replaceRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "setMode";
      mode: PermissionMode;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "addDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    };
```

### `PermissionBehavior`

```typescript theme={null}
type PermissionBehavior = "allow" | "deny" | "ask";
```

### `PermissionUpdateDestination`

```typescript theme={null}
type PermissionUpdateDestination =
  | "userSettings" // Глобальные пользовательские настройки
  | "projectSettings" // Настройки проекта для каждой директории
  | "localSettings" // Локальные настройки проекта
  | "session" // Только текущая сессия
  | "cliArg"; // Аргумент CLI
```

### `PermissionRuleValue`

```typescript theme={null}
type PermissionRuleValue = {
  toolName: string;
  ruleContent?: string;
};
```

## Другие типы

### `ApiKeySource`

Источник API-ключа для запросов сессии; передаётся как `apiKeySource` в инициализирующем сообщении [`SDKSystemMessage`](#sdksystemmessage).

```typescript theme={null}
type ApiKeySource =
  | "ANTHROPIC_API_KEY"
  | "apiKeyHelper"
  | "/login managed key"
  | "none"
  | "user"
  | "project"
  | "org"
  | "temporary"
  | "oauth";
```

Claude Code сообщает одно из четырёх значений:

| Значение | Используемый ключ |
| - | - |
| `ANTHROPIC_API_KEY` | Ключ из переменной окружения `ANTHROPIC_API_KEY` |
| `apiKeyHelper` | Ключ, возвращённый вашей командой [`apiKeyHelper`](https://code.claude.com/docs/ru/settings-reference#apikeyhelper) |
| `/login managed key` | Ключ, который Claude Code сохранил при входе с [учётной записью Claude Console](https://code.claude.com/docs/ru/authentication.md#claude-console-authentication) |
| `none` | API-ключа нет. Сессия проходит аутентификацию другим способом, например через вход в claude.ai, Bearer-токен или облачного провайдера |

В Agent SDK v0.3.234 и более поздних версиях тип перечисляет эти четыре значения. Тип также сохраняет `user`, `project`, `org`, `temporary` и `oauth`, чтобы старый код продолжал компилироваться, но Claude Code их не сообщает.

### `SdkBeta`

Доступные бета-функции, которые можно включить с помощью параметра `betas`. Подробнее см. в разделе [Beta headers](https://platform.claude.com/docs/en/api/beta-headers).

```typescript theme={null}
type SdkBeta = "context-1m-2025-08-07";
```

> [!WARNING]
>
> В Claude API бета-функция `context-1m-2025-08-07` выведена из эксплуатации для Claude Sonnet 4.5 и Claude Sonnet 4. Если вы всё ещё передаёте её с любой из этих моделей, запросы, превышающие стандартное контекстное окно в 200K токенов, возвращают ошибку, поэтому удалите её из `betas`. Чтобы запустить сессию с контекстным окном в 1M токенов, задайте в `model` модель, которая [по умолчанию работает с окном 1M](https://code.claude.com/docs/ru/model-config.md#extended-context), например `claude-sonnet-5-5` или `claude-opus-5-5`. Для модели, которая получает 1M только через вариант `[1m]`, добавьте суффикс к ID модели, например `claude-opus-4-6[1m]`.

### `SlashCommand`

Информация о доступной команде.

```typescript theme={null}
type SlashCommand = {
  name: string;
  description: string;
  argumentHint: string;
  aliases?: string[];
  builtin?: boolean;
};
```

`builtin` имеет значение `true` в записи, когда команда принадлежит самому Claude Code и ввод `/name` запускает её. Поле отсутствует для команды, определённой пользователем, проектом, плагином или MCP-сервером, а также для встроенной команды, которую один из них [заменяет по имени](https://code.claude.com/docs/ru/skills.md#resolve-skills-that-share-a-name). Требуется Agent SDK v0.3.277 или более поздняя версия.

### `ModelInfo`

Информация о доступной модели.

```typescript theme={null}
type ModelInfo = {
  value: string;
  resolvedModel?: string;
  displayName: string;
  description: string;
  supportsEffort?: boolean;
  supportedEffortLevels?: ("low" | "medium" | "high" | "xhigh" | "max")[];
  supportsAdaptiveThinking?: boolean;
  supportsFastMode?: boolean;
  supportsAutoMode?: boolean;
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `value` | `string` | Идентификатор модели для передачи в вызовах API |
| `resolvedModel` | `string \| undefined` | ID модели, в который разрешается `value` этой записи, например `claude-sonnet-5-5` для записи с псевдонимом `sonnet`. Требуется Claude Code v2.1.197 или более поздняя версия. |
| `displayName` | `string` | Понятное человеку отображаемое имя |
| `description` | `string` | Описание возможностей модели |
| `supportsEffort` | `boolean \| undefined` | Поддерживает ли модель уровни effort |
| `supportedEffortLevels` | `("low" \| "medium" \| "high" \| "xhigh" \| "max")[] \| undefined` | Уровни effort, которые принимает эта модель |
| `supportsAdaptiveThinking` | `boolean \| undefined` | Поддерживает ли модель адаптивное мышление, при котором Claude сам решает, когда и сколько размышлять |
| `supportsFastMode` | `boolean \| undefined` | Поддерживает ли модель быстрый режим |
| `supportsAutoMode` | `boolean \| undefined` | Поддерживает ли модель авторежим |

### `AgentInfo`

Информация о доступном субагенте, которого можно вызвать через инструмент Agent.

```typescript theme={null}
type AgentInfo = {
  name: string;
  description: string;
  model?: string;
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | `string` | Идентификатор типа агента (например, `"Explore"`, `"general-purpose"`) |
| `description` | `string` | Описание того, когда использовать этого агента |
| `model` | `string \| undefined` | Модель, которую использует этот агент: псевдоним или ID модели либо `'inherit'` для модели родителя. Если значение `undefined`, Claude Code выбирает модель в [порядке выбора модели для субагента](https://code.claude.com/docs/ru/sub-agents.md#choose-a-model) |

### `McpServerProvenance`

MCP-сервер, предоставляющий инструмент `mcp__*`, и источник определения этого сервера. Входные данные хуков [`PreToolUse`](#pretoolusehookinput), `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` и `PermissionDenied` передают его как `mcp_server`, а параметры [`CanUseTool`](#canusetool) — как `mcpServer`. И там, и там он отсутствует для инструментов, которые не поступают от MCP-сервера.

```typescript theme={null}
type McpServerProvenance = {
  name: string;
  source: string;
};
```

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | `string` | Имя, под которым зарегистрирован сервер; то же значение, которое сообщает для него [`mcpServerStatus()`](#query-object) |
| `source` | `string` | Откуда взято определение сервера: `sdk`, `plugin` или область действия конфигурации |

`source` принимает одно из следующих значений. Набор открыт, поэтому считайте незнакомое значение настроенным источником, но никогда не `sdk`:

* **`sdk`**: внутрипроцессный сервер, зарегистрированный вашим приложением. Зарегистрировать его может только хост-приложение SDK, поэтому настроенный сервер никогда не сообщает `sdk`, каким бы ни было его имя.
* **`plugin`**: сервер, предоставляемый [плагином](https://code.claude.com/docs/ru/agent-sdk/plugins.md). Его `name` имеет ограниченную форму `plugin:<plugin-name>:<server-name>`, описанную в разделе [MCP-серверы, предоставляемые плагинами](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers).
* **Область действия конфигурации**: `user`, `project`, `local`, `dynamic`, `managed`, `enterprise`, `claudeai` или `agent`. Сервер из `.mcp.json` сообщает `project`, а раздел [Области действия установки MCP](https://code.claude.com/docs/ru/mcp.md#mcp-installation-scopes) определяет `local`, `project` и `user`. Серверы, которые ваше приложение передаёт в [параметре `mcpServers`](#options), кроме внутрипроцессных серверов SDK, сообщают `dynamic`.

Принимайте решения о доверии на основе `source`, а не `name` или префикса имени инструмента `mcp__<server>__`. Для любого источника, кроме `sdk`, `name` — недоверенный текст: экранируйте его перед отображением.

`McpServerProvenance` и поля, которые его передают, требуют Agent SDK v0.3.274 или более поздней версии.

### `McpServerStatus`

Статус подключённого MCP-сервера.

```typescript theme={null}
type McpServerStatus = {
  name: string;
  status: "connected" | "failed" | "needs-auth" | "pending" | "disabled";
  serverInfo?: {
    name: string;
    version: string;
  };
  error?: string;
  config?: McpServerStatusConfig;
  scope?: string;
  source?: string;
  tools?: {
    name: string;
    description?: string;
    annotations?: {
      readOnly?: boolean;
      destructive?: boolean;
      openWorld?: boolean;
    };
    _meta?: Record<string, unknown>;
  }[];
};
```

Используйте `source`, чтобы решить, насколько доверять серверу, а `_meta` в каждой записи `tools` — чтобы найти UI-ресурс, который сервер прикрепил к этому инструменту:

* **`source`**: откуда взято определение сервера; значения те же, что у `source` в [`McpServerProvenance`](#mcpserverprovenance). Принимайте решения о доверии на основе `source`, а не `name`, потому что только ваш собственный внутрипроцессный сервер сообщает `sdk`, под каким бы именем ни был зарегистрирован любой другой сервер. Если вы не распознаёте значение `source`, обращайтесь с этим сервером так же, как с любым сервером, чей `source` не равен `sdk`. Требуется Agent SDK v0.3.274 или более поздняя версия
* **`_meta`**: объект `ui` и строка `ui/resourceUri` из `_meta`, которые сервер объявил для инструмента. Все остальные ключи `_meta` Claude Code не передаёт. `ui/resourceUri` — более старое написание `ui.resourceUri` на верхнем уровне. Когда сервер прикрепляет к инструменту [UI-ресурс MCP Apps](https://code.claude.com/docs/ru/mcp.md#reference-mcp-resources), `ui.resourceUri` или `ui/resourceUri` содержит URI ресурса вида `ui://`. Получите этот URI с помощью [`readMcpResource()`](#query-object) и отрисуйте ресурс в своём приложении. Требуется Agent SDK v0.3.280 или более поздняя версия

Claude Code отправляет `_meta` только тогда, когда массив [`capabilities`](#sdksystemmessage) сообщения `system` с подтипом `init` содержит `mcp_tool_ui_meta_v1`. Включать `mcp_tool_ui_meta_v1` самостоятельно не нужно.

#### Когда `_meta.ui` инструмента содержит только `visibility`

Если ваш сервер объявляет `ui.resourceUri` для инструмента, но `_meta.ui`, которое получает ваше приложение, содержит только `visibility`, значит объект `ui`, отправленный сервером, не прошёл одну из проверок Claude Code. Сравните `_meta` в ответе `tools/list` вашего сервера с проверками для каждого ключа:

* **`ui`**: доходит до вашего приложения без изменений, включая любые члены, кроме `resourceUri` и `visibility`, если пройдены все три проверки:

  * `resourceUri` отсутствует или является строкой, начинающейся с `ui://`
  * `visibility` отсутствует или содержит только `"model"` и `"app"`
  * Весь объект при сериализации в JSON занимает не более 4096 символов

  Если какая-либо проверка не пройдена, ваше приложение получает в лучшем случае `ui`, единственный член которого — массив `visibility` с записями `"model"` и `"app"`, перечисленными сервером.
* **`ui/resourceUri`**: доходит до вашего приложения, если это строка, начинающаяся с `ui://`, длиной не более 4096 символов. В противном случае Claude Code отбрасывает его

Когда у Claude Code не остаётся ни члена `ui`, ни строки `ui/resourceUri` для отправки, запись `tools` вообще не содержит `_meta`.

### `McpServerStatusConfig`

Конфигурация MCP-сервера, возвращаемая `mcpServerStatus()`. Это объединение всех типов транспорта MCP-серверов.

```typescript theme={null}
type McpServerStatusConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfig
  | McpClaudeAIProxyServerConfig;
```

Подробнее о каждом типе транспорта см. в [`McpServerConfig`](#mcpserverconfig).

### `AccountInfo`

Информация об учётной записи аутентифицированного пользователя.

```typescript theme={null}
type AccountInfo = {
  email?: string;
  organization?: string;
  subscriptionType?: string;
  tokenSource?: string;
  apiKeySource?: string;
};
```

### `ModelUsage`

Статистика использования по каждой модели, возвращаемая в сообщениях с результатом. Значение `costUSD` — оценка на стороне клиента. Оговорки, касающиеся биллинга, см. в разделе [Отслеживание стоимости и использования](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md).

```typescript theme={null}
type ModelUsage = {
  inputTokens: number;
  outputTokens: number;
  thinkingTokens?: number;
  cacheReadInputTokens: number;
  cacheCreationInputTokens: number;
  webSearchRequests: number;
  costUSD: number;
  contextWindow: number;
  maxOutputTokens: number;
  canonicalModel?: string;
  provider?: string;
  costBasis?: 'list' | 'managed' | 'unknown';
};
```

`thinkingTokens` подсчитывает токены размышлений, сгенерированные этой моделью. `outputTokens` уже включает их, поэтому не складывайте эти два значения. Поле отсутствует, пока не будет выполнен ход в версии Claude Code, которая его записывает, поэтому возобновлённая сессия, начатая в более ранней версии, сообщает частичный подсчёт. `thinkingTokens` требует Agent SDK v0.3.257 или более поздней версии.

Поля `canonicalModel` и `provider` требуют Claude Code v2.1.218 или более поздней версии. `canonicalModel` — канонический ID модели, который используется при поиске цены; он может отличаться от исходной строки модели, служащей ключом записи, например когда эта строка — ID конкретного провайдера или псевдоним.

`provider` указывает бэкенд API, обслуживший модель, например `firstParty`, `bedrock`, `vertex`, `foundry`, `anthropicAws`, `mantle` или `gateway`.

`costBasis` указывает таблицу цен, по которой был тарифицирован последний запрос модели: `list` для прейскурантной цены, `managed` для таблицы [`modelPricing`](https://code.claude.com/docs/ru/settings-reference#modelpricing) или `unknown`, если ни одна из них не совпала с ID модели. Поле требует Claude Code v2.1.246 или более поздней версии.

### `ConfigScope`

```typescript theme={null}
type ConfigScope = "local" | "user" | "project";
```

### `NonNullableUsage`

Версия [`Usage`](#usage), в которой все допускающие null поля сделаны не допускающими null, кроме `fallback_credit`, который по-прежнему может быть `null`.

```typescript theme={null}
type NonNullableUsage = {
  [K in keyof Usage]: K extends "fallback_credit"
    ? Usage[K]
    : NonNullable<Usage[K]>;
};
```

### `Usage`

Статистика использования токенов. Это тип `BetaUsage` из `@anthropic-ai/sdk`.

```typescript theme={null}
type Usage = {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens: number | null;
  cache_read_input_tokens: number | null;
  cache_creation: {
    ephemeral_5m_input_tokens: number;
    ephemeral_1h_input_tokens: number;
  } | null;
  server_tool_use: BetaServerToolUsage | null;
  service_tier: "standard" | "priority" | "batch" | null;
  speed: "standard" | "fast" | null;
  inference_geo: string | null;
  iterations: BetaIterationsUsage | null;
  output_tokens_details: BetaOutputTokensDetails | null;
  fallback_credit: BetaFallbackCreditUsage | null;
};
```

`BetaServerToolUsage`, `BetaIterationsUsage`, `BetaOutputTokensDetails` и `BetaFallbackCreditUsage` определены в `@anthropic-ai/sdk`.

`output_tokens_details` разбивает тарифицируемый вывод по категориям. Сейчас оно содержит одно поле, `thinking_tokens: number`, которое подсчитывает выходные токены, сгенерированные моделью как внутренние рассуждения, включая разделители блоков размышлений. Поле `output_tokens_details` требует TypeScript SDK v0.3.228 или более поздней версии, которая включает Claude Code v2.1.228.

* **Биллинг**: используйте эту разбивку для наблюдаемости, а не для биллинга. `output_tokens` остаётся авторитетным итогом, а `output_tokens - thinking_tokens` приблизительно соответствует выводу без рассуждений.
* **Что охватывает подсчёт**: необработанные рассуждения модели, которые могут быть длиннее текста размышлений, возвращаемого в теле ответа. API вычисляет значение повторной токенизацией этого необработанного текста, поэтому оно может отличаться от точного числа сгенерированных моделью токенов на несколько токенов.
* **Потоковая передача**: в потоковых сообщениях ассистента эта разбивка, как и `output_tokens`, является заглушкой `message_start` и не содержит реального значения, поэтому считывайте её из `usage` сообщения с результатом, как описано в разделе [Чтение выходных токенов из сообщения с результатом](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#read-output-tokens-from-the-result-message). В сообщении с результатом `thinking_tokens` равно `0`, если модель или провайдер не сообщает разбивку.
* **Случаи `null`**: само `output_tokens_details` равно `null` в сообщениях ассистента, которые синтезирует Claude Code, например в сообщениях об ошибках API.

Содержит ли `Usage` поле `fallback_credit`, зависит от установленной версии `@anthropic-ai/sdk`, в которой оно появилось в 0.115.0.

### `CallToolResult`

Тип результата инструмента MCP (из `@modelcontextprotocol/sdk/types.js`). `structuredContent` — JSON-объект, который можно вернуть вместе с `content`, включая блоки изображений. См. [Возврат структурированных данных](https://code.claude.com/docs/ru/agent-sdk/custom-tools.md#return-structured-data).

```typescript theme={null}
type CallToolResult = {
  content: Array<{
    type: "text" | "image" | "audio" | "resource" | "resource_link";
    // Дополнительные поля зависят от типа
  }>;
  structuredContent?: Record<string, unknown>;
  isError?: boolean;
};
```

### `SDKMcpResourceLink`

Один файл, возвращённый инструментом MCP по ссылке. Claude Code строит каждую запись из блока `resource_link` в результате инструмента и передаёт список как `resourceLinks` в [`SDKUserMessage.tool_use_result`](#sdkusermessage) или как `resource_links` в [`SDKTaskNotificationMessage`](#sdktasknotificationmessage), если вызов завершился в фоне. Требуется Agent SDK v0.3.257 или более поздняя версия.

```typescript theme={null}
type SDKMcpResourceLink = {
  uri: string;
  name: string;
  title?: string;
  description?: string;
  mimeType?: string;
  size?: number;
  annotations?: Record<string, unknown>;
};
```

Claude Code отбрасывает блок, у которого `uri` или `name` не является строкой, и опускает необязательное поле, значение которого не соответствует указанному типу.

| Поле | Тип | Описание |
| :- | :- | :- |
| `uri` | `string` | URI ресурса в том виде, в каком его вернул сервер |
| `name` | `string` | Имя, которое сервер дал ресурсу |
| `title` | `string \| undefined` | Отображаемый заголовок, если сервер его задал |
| `description` | `string \| undefined` | Описание, если сервер его задал |
| `mimeType` | `string \| undefined` | MIME-тип, если сервер его задал |
| `size` | `number \| undefined` | Размер в байтах, если сервер его задал |
| `annotations` | `Record<string, unknown> \| undefined` | Объект аннотаций MCP блока, если сервер его задал |

### `ThinkingConfig`

Управляет поведением мышления/рассуждений Claude. Имеет приоритет над устаревшим `maxThinkingTokens`.

```typescript theme={null}
type ThinkingDisplay = "summarized" | "omitted";

type ThinkingConfig =
  | { type: "adaptive"; display?: ThinkingDisplay } // Модель сама определяет, когда и сколько рассуждать (Opus 4.6+)
  | { type: "enabled"; budgetTokens?: number; display?: ThinkingDisplay } // Фиксированный бюджет токенов мышления
  | { type: "disabled" }; // Отключает мышление там, где это позволяют модель и провайдер
```

О `disabled` см. раздел [где нельзя отключить мышление](https://code.claude.com/docs/ru/model-config.md#where-you-cant-turn-thinking-off).

Необязательное поле `display` определяет, возвращается ли текст размышлений как `"summarized"` или `"omitted"`. В Claude Opus 4.7 и более поздних версиях значение API по умолчанию — `"omitted"`, поэтому задайте `"summarized"`, чтобы получать содержимое размышлений в блоках `thinking`. У таких провайдеров, как Amazon Bedrock и Agent Platform от Google Cloud, Claude Code не передаёт `display` для распознаваемых им более ранних моделей. Это Opus 4.6, Sonnet 4.6, Haiku 4.5 и более ранние модели, которые используют своё значение по умолчанию.

### `SpawnedProcess`

Интерфейс для пользовательского запуска процессов (используется с параметром `spawnClaudeCodeProcess`). `ChildProcess` уже удовлетворяет этому интерфейсу.

```typescript theme={null}
interface SpawnedProcess {
  stdin: Writable;
  stdout: Readable;
  readonly killed: boolean;
  readonly exitCode: number | null;
  kill(signal: NodeJS.Signals): boolean;
  on(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  on(event: "error", listener: (error: Error) => void): void;
  once(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  once(event: "error", listener: (error: Error) => void): void;
  off(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  off(event: "error", listener: (error: Error) => void): void;
}
```

### `SpawnOptions`

Параметры, передаваемые пользовательской функции запуска.

```typescript theme={null}
interface SpawnOptions {
  command: string;
  args: string[];
  cwd?: string;
  env: Record<string, string | undefined>;
  signal: AbortSignal;
}
```

> [!NOTE]
>
> Поле `signal` сообщает вашей функции запуска, когда нужно завершить процесс. Передайте его как параметр `signal` в `spawn()` из Node или передайте его в свой обработчик завершения ВМ или контейнера.
>
> Этот сигнал срабатывает не в момент прерывания [`Options.abortController`](#options). Сначала SDK закрывает stdin процесса и ждёт около двух секунд, чтобы CLI мог корректно завершиться, и только затем прерывает этот сигнал. Чтобы реагировать сразу в момент прерывания вызывающей стороной, подпишитесь на собственный `Options.abortController.signal`, на который ваша функция запуска может ссылаться из охватывающей области видимости.

### `McpSetServersResult`

Результат операции `setMcpServers()`.

```typescript theme={null}
type McpSetServersResult = {
  added: string[];
  removed: string[];
  errors: Record<string, string>;
};
```

Промис `setMcpServers()` разрешается после того, как вновь добавленные серверы stdio, HTTP и SSE подключатся или завершатся неудачей, поэтому инструменты подключившихся серверов доступны на следующем ходе.

При вызове `setMcpServers()` Claude Code применяет следующие правила:

* **Серверы, не названные в вызове**: вне [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) Claude Code отключает серверы, добавленные предыдущим вызовом `setMcpServers()`, и внутрипроцессные серверы SDK и перечисляет их в `removed`. Остальные серверы продолжают работать и не перечисляются в `removed`, в том числе серверы stdio, HTTP и SSE из параметра [`mcpServers`](#options), серверы из файлов настроек и серверы, предоставляемые плагинами.
* **Серверы stdio, HTTP и SSE, добавленные предыдущим вызовом `setMcpServers()`**: вне облачной сессии сервер, который вы снова называете с идентичной конфигурацией, сохраняет своё подключение и инструменты. Он не появляется ни в `added`, ни в `removed`. Если вы передаёте изменённую конфигурацию, Claude Code переподключает сервер с этой конфигурацией и перечисляет его в `added`, а не в `removed`.
* **Серверы stdio, HTTP и SSE, названные в вызове, которые не добавлял ни один предыдущий вызов**: вне облачной сессии Claude Code добавляет сервер и перечисляет его в `added` или в `errors`, если отклоняет сервер.
* **Внутрипроцессные серверы SDK, названные в вызове**: сервер, уже зарегистрированный через `mcpServers` или предыдущий вызов, сохраняет свой запущенный экземпляр и таймаут. Если вы передаёте для него [список политик `tools`](#mcpsdkserverconfigwithinstance), даже пустой, вы заменяете его политики; в противном случае они сохраняются. Чтобы запустить новый экземпляр вне облачной сессии, не указывайте сервер в одном вызове и укажите его в следующем.
* **Встроенные серверы, которые CLI запустил при старте**: если вызов называет один из них, Claude Code отбрасывает эту запись и сообщает о ней в `errors`.
* **Серверы stdio, HTTP или SSE, имя которых совпадает с сервером из области действия установки MCP, например `.mcp.json`**: под этим именем сессия использует инструменты вашего сервера, а не [сервера из области действия установки](https://code.claude.com/docs/ru/mcp.md#mcp-installation-scopes). До Claude Code v2.1.305 Claude Code мог отключить ваш сервер и подключить сервер из области действия установки, когда ваше приложение [перезагружало плагины](#query-object).

`added` перечисляет серверы, которые Claude Code добавил или заменил, независимо от того, подключились ли они. Сервер, который не удалось подключить, появляется и в `added`, и в `errors`: текст ошибки находится в `errors`, а в [`mcpServerStatus()`](#methods) есть строка со статусом `failed`. До Claude Code v2.1.257 сервер, попытка подключения которого выбрасывала исключение, сообщался только в `errors`.

Значение в `errors`, начинающееся с `Blocked by enterprise`, означает, что сервер отклонила политика, а не что не удалось подключиться:

* `Blocked by enterprise policy (allowedMcpServers/deniedMcpServers)`: сервера нет в `added`. Ему соответствует запись [`deniedMcpServers`](https://code.claude.com/docs/ru/managed-mcp#policy-based-control-with-allowlists-and-denylists), либо задан список `allowedMcpServers`, в котором его нет. Если этот список находится в файле настроек, который вы загружаете через [`settingSources`](#options), отредактируйте файл. Если он находится в управляемых настройках, попросите администраторов изменить его.
* `Blocked by enterprise managed policy`: сервер есть в `added`, а в `mcpServerStatus()` у него строка со статусом `failed`. Спросите администратора, какая политика его блокирует.

### `RewindFilesResult`

Результат операции `rewindFiles()`.

```typescript theme={null}
type RewindFilesResult = {
  canRewind: boolean;
  error?: string;
  filesChanged?: string[];
  insertions?: number;
  deletions?: number;
  skippedLinks?: number;
};
```

`skippedLinks` подсчитывает отслеживаемые пути, которые откат отказался восстановить или удалить из соображений безопасности ссылок: символическая ссылка, жёсткая ссылка или другой нерегулярный файл по отслеживаемому пути, родительский каталог, который больше не разрешается в то место, на которое указывал при создании чекпоинта, или резервная копия, которую не удалось безопасно прочитать. Поле требует Claude Code v2.1.216 или более поздней версии. Вызов предварительного просмотра `rewindFiles(userMessageId, { dryRun: true })` никогда его не задаёт.

### `SDKStatusMessage`

Сообщение об обновлении статуса (например, о сжатии).

```typescript theme={null}
type SDKStatusMessage = {
  type: "system";
  subtype: "status";
  status: "compacting" | null;
  permissionMode?: PermissionMode;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskNotificationMessage`

Уведомление о том, что фоновая задача завершилась, завершилась с ошибкой или была остановлена. К фоновым задачам относятся команды Bash с `run_in_background`, наблюдения [Monitor](#monitor) и фоновые субагенты. О полях `run_id` и `ambient` см. [`SDKTaskStartedMessage`](#sdktaskstartedmessage), где они определены вместе с требованиями к версии.

```typescript theme={null}
type SDKTaskNotificationMessage = {
  type: "system";
  subtype: "task_notification";
  task_id: string;
  run_id?: string;
  tool_use_id?: string;
  status: "completed" | "failed" | "stopped";
  reason?: "worker_restart";
  output_file: string;
  summary: string;
  ambient?: boolean;
  usage?: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  resource_links?: SDKMcpResourceLink[];
  uuid: UUID;
  session_id: string;
};
```

`reason` задаётся, когда задача завершается по причине, отличной от её собственного завершения, сбоя или остановки, и требует Agent SDK v0.3.273 или более поздней версии. Claude Code задаёт его только в сессиях, подключающихся через claude.ai: в облачных сессиях, включая сессии на самостоятельно размещённых раннерах, и в сессиях Remote Control. Локальный вызов `query()` никогда его не задаёт. Его единственное значение, `worker_restart`, означает, что процесс Claude Code, выполнявший задачу, перезапустился. Уведомление имеет статус `"stopped"`, поэтому считайте задачу ни завершённой, ни завершившейся с ошибкой.

Когда Claude Code [переводит длительный вызов инструмента MCP в фон](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls), блок `tool_result` для этого вызова содержит только заглушку, а реальный результат вызова приходит в этом уведомлении. Сопоставляйте уведомление с вызовом по `tool_use_id`. В уведомлении со статусом `completed` поле `resource_links` перечисляет файлы, возвращённые инструментом по ссылке, в виде записей [`SDKMcpResourceLink`](#sdkmcpresourcelink) с теми же ограничениями в 50 ссылок и 64 КиБ, что и у [`tool_use_result.resourceLinks`](#sdkusermessage). Claude Code опускает `resource_links`, если в результате не было ссылок, а также в уведомлениях о задачах, не являющихся вызовами инструментов MCP. `resource_links` требует Agent SDK v0.3.257 или более поздней версии.

Claude Code добавляет в начало каждого уведомления о задаче, которое он отправляет модели, предупреждение, за исключением доставок с [подтипом `scheduled-trigger`](#task-notification-subkinds), которые вместо этого оформлены как назначенная задача. В предупреждении указано, что ввода от человека не было, поэтому модель не воспринимает уведомление как инструкцию или подтверждение пользователя.

Чтобы распознать ход с уведомлением о задаче, проверяйте `origin.kind === "task-notification"` в [`SDKUserMessage`](#sdkusermessage) или [`SDKResultMessage`](#sdkresultmessage), а не сопоставляйте текст предупреждения. Если нужно знать, что его вызвало, считайте `subkind` из того же поля. До v2.1.205 Claude Code не добавлял предупреждение к уведомлениям, поступавшим, пока сессия простаивала.

### `SDKToolUseSummaryMessage`

Сводка использования инструментов в диалоге.

```typescript theme={null}
type SDKToolUseSummaryMessage = {
  type: "tool_use_summary";
  summary: string;
  preceding_tool_use_ids: string[];
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookStartedMessage`

Отправляется, когда хук начинает выполняться.

Claude Code доставляет это сообщение, [`SDKHookProgressMessage`](#sdkhookprogressmessage) и [`SDKHookResponseMessage`](#sdkhookresponsemessage) в поток сообщений немедленно, в том числе пока хук `SessionStart` или `Setup` ещё выполняется во время запуска сессии. Claude Code с v2.1.169 по v2.1.203 доставлял эти сообщения одним пакетом после завершения хука `SessionStart` или `Setup`; v2.1.204 восстановил доставку в реальном времени.

Если вы запускаете сессию с помощью [`startup()`](#startup), эти сообщения поступают к вам, когда вы вызываете `.query()` и итерируете результат.

```typescript theme={null}
type SDKHookStartedMessage = {
  type: "system";
  subtype: "hook_started";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookProgressMessage`

Отправляется во время выполнения хука и содержит вывод stdout/stderr.

```typescript theme={null}
type SDKHookProgressMessage = {
  type: "system";
  subtype: "hook_progress";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  stdout: string;
  stderr: string;
  output: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookResponseMessage`

Отправляется, когда хук завершает выполнение.

```typescript theme={null}
type SDKHookResponseMessage = {
  type: "system";
  subtype: "hook_response";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  output: string;
  stdout: string;
  stderr: string;
  exit_code?: number;
  outcome: "success" | "error" | "cancelled";
  uuid: UUID;
  session_id: string;
};
```

### `SDKToolProgressMessage`

Периодически отправляется во время выполнения инструмента для индикации прогресса.

```typescript theme={null}
type SDKToolProgressMessage = {
  type: "tool_progress";
  tool_use_id: string;
  tool_name: string;
  parent_tool_use_id: string | null;
  elapsed_time_seconds: number;
  task_id?: string;
  heartbeat?: boolean;
  subagent_type?: string;
  subagent_retry?: {
    agent_id: string;
    attempt: number;
    max_retries: number;
    retry_delay_ms: number;
    error_status: number | null;
    error_category: string;
  };
  uuid: UUID;
  session_id: string;
};
```

Пока вызов инструмента выполняется в основном диалоге, Claude Code каждые 30 секунд отправляет сообщение `tool_progress` с `heartbeat: true`. Каждый такой сигнал активности содержит имя инструмента и прошедшее время в секундах, поэтому вы можете отличить длительный вызов от зависшей сессии. Claude Code не отправляет сигналы активности для вызовов инструментов внутри субагента. Поле `heartbeat` требует Agent SDK v0.3.214 или более поздней версии. До v2.1.257 Claude Code также не отправлял сигналы активности для вызова инструмента Agent на переднем плане.

В Agent SDK v0.3.323 и более поздних версиях сигнал активности, у которого `tool_use_id` начинается с `hook-`, поступает от длительно выполняющегося хука, а не от вызова инструмента. Его `tool_name` — имя события хука, например `PreToolUse`.

В сообщениях `tool_progress` для инструмента Agent, не являющихся сигналами активности, `subagent_type` указывает тип выполняющегося субагента, например `general-purpose`. `subagent_retry` присутствует, пока этот субагент выжидает интервал после ошибки API, например ограничения частоты запросов или перегрузки; на каждую повторную попытку приходится одно сообщение. Оба поля требуют Agent SDK v0.3.214 или более поздней версии.

Чтобы отрисовать индикатор повторной попытки на основе `subagent_retry`:

* Отслеживайте индикатор по `parent_tool_use_id`, который уникален для каждого субагента. `tool_use_id` общий для параллельных субагентов из одного хода ассистента, поэтому при отслеживании по нему обновление одного субагента может сбросить индикатор другого.
* Сбрасывайте индикатор, когда для того же `parent_tool_use_id` приходит следующее сообщение `tool_progress` без `subagent_retry` и без `heartbeat: true` или когда приходит сообщение с результатом инструмента. Кадры с `heartbeat: true` сообщают только о том, что процесс жив, поэтому при их получении сохраняйте индикатор. При постоянных повторных попытках `attempt` может превышать `max_retries`, поэтому не выводите условие сброса из счётчиков.
* Рассматривайте `error_category` как токен для выбора собственного текста сообщения, а не как отображаемый текст. Возможные значения: `rate_limit`, `overloaded`, `authentication_failed`, `server_error`, `cloud_credential_error` и `unknown`. Обрабатывайте незнакомое значение так же, как `unknown`, потому что в будущих выпусках могут появиться новые значения.

### `SDKAuthStatusMessage`

Отправляется во время процессов аутентификации.

```typescript theme={null}
type SDKAuthStatusMessage = {
  type: "auth_status";
  isAuthenticating: boolean;
  output: string[];
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskStartedMessage`

Отправляется, когда начинается задача. `task_type` указывает вид задачи, например `"local_bash"` для команд Bash и наблюдений [Monitor](#monitor), `"local_agent"` для субагентов, `"mcp_task"` для [фоновых вызовов инструментов MCP](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls) или `"remote_agent"`.

```typescript theme={null}
type SDKTaskStartedMessage = {
  type: "system";
  subtype: "task_started";
  task_id: string;
  run_id?: string;
  tool_use_id?: string;
  description: string;
  task_type?: string;
  is_backgrounded?: boolean;
  spawn_depth?: number;
  parent_task_id?: string;
  ambient?: boolean;
  uuid: UUID;
  session_id: string;
};
```

`run_id` идентифицирует один запуск задачи. Когда задача снова запускается под тем же `task_id`, например [субагент, которого Claude возобновляет](https://code.claude.com/docs/ru/agent-sdk/subagents.md#resume-subagents), новый запуск получает новый `run_id`. Поле требует Agent SDK v0.3.292 или более поздней версии. Используйте его, чтобы различать запуски одной задачи:

* **Сопоставление сообщений с запуском**: сообщения `task_started`, [`task_progress`](#sdktaskprogressmessage), [`task_updated`](#sdktaskupdatedmessage) и [`task_notification`](#sdktasknotificationmessage) одного запуска содержат одинаковый `run_id`. Его содержит и запись запуска в каждом [`SDKBackgroundTasksChangedMessage`](#sdkbackgroundtaskschangedmessage), а также [`runId`](#task-notification-subkinds) в origin пользовательского сообщения, доставляющего уведомление о запуске.
* **Обнаружение запоздавшего сообщения**: при сравнении как обычных строк ID запусков одной задачи сортируются в порядке начала запусков, поэтому сообщение, чей `run_id` сортируется раньше отображаемого запуска, относится к более раннему запуску. Помимо этого сравнения считайте значение непрозрачным.
* **Возврат к `task_id`**: если сообщение не содержит `run_id`, например `task_notification`, которое возобновлённая сессия отправляет, чтобы закрыть задачу, запущенную прежним процессом, относите его к задаче по `task_id`.

Например, эти три сообщения, сокращённые до идентифицирующих полей, получены от фонового субагента, которого Claude возобновил один раз. Два сообщения `task_started` имеют общий `task_id`, а уведомление, завершившее первый запуск, содержит ID первого запуска:

```json theme={null}
{"subtype": "task_started", "task_id": "a5c2e8f41b09d7a36", "run_id": "0mubbs7i8-6f0c2d41"}
{"subtype": "task_notification", "task_id": "a5c2e8f41b09d7a36", "run_id": "0mubbs7i8-6f0c2d41", "status": "completed"}
{"subtype": "task_started", "task_id": "a5c2e8f41b09d7a36", "run_id": "0mubc18m1-b7719e05"}
```

`ambient` имеет значение `true` для задач, не являющихся частью работы сессии, например задач, которые Claude Code выполняет для собственной работы. Наблюдатели за обновлениями в реальном времени также являются фоновыми служебными задачами, включая наблюдателей, о которых попросил пользователь. Исключайте такие задачи из индикаторов активности. Поле требует Agent SDK v0.3.247 или более поздней версии.

`ambient` также присутствует в [`SDKTaskNotificationMessage`](#sdktasknotificationmessage) и в записях [`SDKBackgroundTasksChangedMessage`](#sdkbackgroundtaskschangedmessage).

`is_backgrounded` и `spawn_depth` описывают, как Claude Code запустил задачу. Оба поля требуют Agent SDK v0.3.238 или более поздней версии.

* `is_backgrounded`: Claude Code задаёт его для задач `"local_agent"` и `"local_bash"`. `true` означает, что задача выполняется в фоне. `false` означает, что задача выполняется на переднем плане, а вызов инструмента, запустивший её, остаётся заблокированным, пока задача не завершится или не перейдёт в фон.
* `spawn_depth`: Claude Code задаёт его только для задач `"local_agent"`. Субагент, порождённый основным потоком, имеет глубину `1`. Субагент, порождённый субагентом глубины `1`, имеет глубину `2` и так далее.

[Возобновлённый субагент](https://code.claude.com/docs/ru/agent-sdk/subagents.md#resume-subagents) всегда сообщает `is_backgrounded: true`, потому что Claude Code выполняет каждого возобновлённого субагента в фоне. Когда задача переднего плана позже переходит в фон, Claude Code сообщает новое значение `is_backgrounded` в сообщении [`task_updated`](#sdktaskupdatedmessage), а не отправляет второе `task_started`.

`parent_task_id` содержит `task_id` субагента, запустившего эту задачу. Используйте его, чтобы группировать каждую задачу под запустившим её субагентом. Claude Code задаёт его для задач субагентов, Bash и [Monitor](#monitor). Поле требует Agent SDK v0.3.292 или более поздней версии. Оно отсутствует, когда:

* Задачу запустил основной поток
* Claude Code больше не отслеживает родительскую задачу
* Задачу запустил [участник команды](https://code.claude.com/docs/ru/agent-teams.md) или агент внутри рабочего процесса

Родителем может быть задача переднего плана или уже завершившаяся задача, поэтому считайте незнакомый ID отсутствием родителя.

### `SDKTaskProgressMessage`

Периодически отправляется, пока выполняется субагент или фоновая задача. О поле `run_id` см. [`SDKTaskStartedMessage`](#sdktaskstartedmessage), где оно определено вместе с требованием к версии.

Для задачи субагента поле `summary` содержит сгенерированную моделью сводку прогресса и заполняется, только если включён параметр [`agentProgressSummaries`](#options). Для [вызова инструмента MCP, переведённого в фон](https://code.claude.com/docs/ru/mcp.md#automatic-backgrounding-of-long-tool-calls), `summary` содержит последний прогресс, сообщённый MCP-сервером, и не зависит от этого параметра.

```typescript theme={null}
type SDKTaskProgressMessage = {
  type: "system";
  subtype: "task_progress";
  task_id: string;
  run_id?: string;
  tool_use_id?: string;
  description: string;
  subagent_type?: string;
  usage: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  last_tool_name?: string;
  summary?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskUpdatedMessage`

Отправляется при изменении состояния фоновой задачи, например при переходе из `running` в `completed`. Объединяйте `patch` с локальной картой задач, ключом которой служит `task_id`. Поле `end_time` — метка времени Unix в миллисекундах, сравнимая с `Date.now()`. О поле `run_id` см. [`SDKTaskStartedMessage`](#sdktaskstartedmessage), где оно определено вместе с требованием к версии.

```typescript theme={null}
type SDKTaskUpdatedMessage = {
  type: "system";
  subtype: "task_updated";
  task_id: string;
  run_id?: string;
  patch: {
    status?: "pending" | "running" | "completed" | "failed" | "killed";
    description?: string;
    end_time?: number;
    total_paused_ms?: number;
    error?: string;
    is_backgrounded?: boolean;
  };
  uuid: UUID;
  session_id: string;
};
```

### `SDKBackgroundTasksChangedMessage`

Отправляется при каждом изменении набора активных фоновых задач: задача запускается, завершается или принудительно останавливается; агент переднего плана переводится в фон; или изменяется поле задачи `description`, `ambient` или `parent_task_id`. О полях `run_id` и `parent_task_id` в каждой записи см. [`SDKTaskStartedMessage`](#sdktaskstartedmessage), где они определены вместе с требованиями к версии.

Массив `tasks` — полный набор активных задач. Заменяйте любой кэшированный набор содержимым каждого сообщения, а не сопоставляйте события `task_started` и `task_notification`, чтобы следующее изменение состава исправило любое пропущенное событие.

Когда задача завершается, её [`task_updated`](#sdktaskupdatedmessage) и [`task_notification`](#sdktasknotificationmessage) приходят до `background_tasks_changed`, исключающего её из списка. В остальном порядок относительно событий отдельных задач не определён.

При запуске ничего не отправляется. Сбрасывайте набор до пустого каждый раз, когда процесс CLI сессии запускается или перезапускается, и позвольте следующему изменению состава заполнить его.

Когда вы отправляете повторный управляющий запрос `initialize` работающей сессии, например с помощью [`reinitialize()`](#query-object) после разрыва транспорта, Claude Code отправляет вслед за ответом снимок текущего набора активных задач, даже если он пуст. Таким образом, переподключающийся хост узнаёт, что выполняется, не дожидаясь следующего изменения состава. До Agent SDK v0.3.239 Claude Code не отправлял снимок после повторного `initialize`.

Требуется Claude Code v2.1.203 или более поздняя версия.

```typescript theme={null}
type SDKBackgroundTasksChangedMessage = {
  type: "system";
  subtype: "background_tasks_changed";
  tasks: {
    task_id: string;
    run_id?: string;
    task_type: string;
    subagent_type?: string;
    description: string;
    parent_task_id?: string;
    ambient?: boolean;
  }[];
  uuid: UUID;
  session_id: string;
};
```

`subagent_type` указывает тип субагента в записях, у которых [`task_type`](#sdktaskstartedmessage) равен `"local_agent"`, например `general-purpose` или имя пользовательского субагента. Поле требует Agent SDK v0.3.293 или более поздней версии.

### `SDKThinkingTokensMessage`

Отправляется, пока Claude создаёт блок размышлений, в том числе отредактированный. `estimated_tokens` — текущая оценка числа токенов размышлений, сгенерированных к этому моменту в текущем блоке, а `estimated_tokens_delta` — приращение, передаваемое этим кадром. Используйте эти оценки для отображения прогресса.

Если модель или провайдер сообщает разбивку, итоговое значение для цикла агента верхнего уровня — это [`usage.output_tokens_details.thinking_tokens`](#usage) сообщения с результатом, которое [не включает токены субагентов](https://code.claude.com/docs/ru/agent-sdk/cost-tracking.md#get-the-total-cost-of-a-query).

Требуется Claude Code v2.1.153 или более поздняя версия.

```typescript theme={null}
type SDKThinkingTokensMessage = {
  type: "system";
  subtype: "thinking_tokens";
  estimated_tokens: number;
  estimated_tokens_delta: number;
  user_message_uuid?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKSessionStateChangedMessage`

Отправляется, когда Claude Code сообщает состояние сессии. Чтобы получать эти сообщения, задайте [`CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS=1`](https://code.claude.com/docs/ru/env-vars#variables). Claude Code может сообщать одно и то же состояние несколько раз, поэтому воспринимайте сообщение как текущее состояние сессии, а не как переход.

Поле `state` содержит одно из следующих значений:

* `running`: сессия работает.
* `idle`: Claude Code ожидает ваш следующий промпт.
* `requires_action`: сессия заблокирована в ожидании ответа на запрос, отправленный вашему хосту, например на запрос разрешения.

Сообщение `idle` хода и его сообщение `result` могут прийти в любом порядке. Чтобы изменить, ждёт ли `idle` фоновую работу, например фонового субагента или запуск [рабочего процесса](https://code.claude.com/docs/ru/workflows.md), см. [`CLAUDE_CODE_BG_TASKS_REPORT_RUNNING`](https://code.claude.com/docs/ru/env-vars#variables).

```typescript theme={null}
type SDKSessionStateChangedMessage = {
  type: "system";
  subtype: "session_state_changed";
  state: "idle" | "running" | "requires_action";
  uuid: UUID;
  session_id: string;
};
```

### `SDKFilesPersistedEvent`

Отправляется, когда чекпоинты файлов сохраняются на диск.

```typescript theme={null}
type SDKFilesPersistedEvent = {
  type: "system";
  subtype: "files_persisted";
  files: { filename: string; file_id: string }[];
  failed: { filename: string; error: string }[];
  processed_at: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKRateLimitEvent`

Отправляется, когда сессия сталкивается с ограничением частоты запросов.

```typescript theme={null}
type SDKRateLimitEvent = {
  type: "rate_limit_event";
  rate_limit_info: {
    status: "allowed" | "allowed_warning" | "rejected";
    resetsAt?: number;
    utilization?: number;
    errorCode?: "credits_required";
    canUserPurchaseCredits?: boolean;
    hasChargeableSavedPaymentMethod?: boolean;
    overageEnabled?: boolean;
  };
  uuid: UUID;
  session_id: string;
};
```

Когда `errorCode` равен `"credits_required"`, отказ исходит от подписки claude.ai, включённое использование которой исчерпано, и сессия не может продолжиться, пока пользователь не купит кредиты использования. `canUserPurchaseCredits` указывает, может ли аутентифицированный пользователь купить кредиты для учётной записи, а `hasChargeableSavedPaymentMethod` — есть ли сохранённый способ оплаты. Все три поля отсутствуют в событиях ограничения частоты запросов, не являющихся отказами из-за отсутствия кредитов. Требуется Claude Code v2.1.181 или более поздняя версия.

В предупреждении о лимите использования тарифа, когда `status` равен `"allowed_warning"`, `overageEnabled` сообщает, включены ли для учётной записи [кредиты использования](https://code.claude.com/docs/ru/costs.md#add-usage-credits-to-your-subscription). Требуется Claude Code v2.1.295 или более поздняя версия.

### `SDKLocalCommandOutputMessage`

Claude Code не отправляет сообщения этого типа. Когда вы отправляете команду, например `/context` или `/usage`, в качестве промпта, её вывод приходит как [`SDKAssistantMessage`](#sdkassistantmessage).

```typescript theme={null}
type SDKLocalCommandOutputMessage = {
  type: "system";
  subtype: "local_command_output";
  content: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKCommandsChangedMessage`

Отправляется, когда набор доступных команд меняется во время сессии, например когда Claude Code обнаруживает скиллы при переходе агента в подкаталог. Массив `commands` — полный обновлённый список, поэтому заменяйте любой кэшированный список команд этими данными. Вызов [`supportedCommands()`](#query-object) после этого сообщения возвращает тот же обновлённый список, поскольку метод отслеживает последнее обновление; для этого требуется Agent SDK v0.3.216 или более поздняя версия. В более ранних версиях SDK `supportedCommands()` возвращает снимок, сделанный при инициализации, и никогда не отражает изменения во время сессии.

Claude Code также отправляет это сообщение, когда [промпты](https://code.claude.com/docs/ru/mcp.md#use-mcp-prompts-as-commands) MCP-сервера добавляются в список или удаляются из него, например когда сервер завершает подключение после начала сессии. Для этого требуется Claude Code v2.1.281 или более поздняя версия.

```typescript theme={null}
type SDKCommandsChangedMessage = {
  type: "system";
  subtype: "commands_changed";
  commands: SlashCommand[];
  uuid: UUID;
  session_id: string;
};
```

### `SDKPromptSuggestionMessage`

Отправляется после хода, если включён параметр [`promptSuggestions`](#options) и Claude Code сгенерировал предложение для этого хода. Содержит предсказанный следующий промпт пользователя. О ходах, для которых предложение не создаётся, см. [Когда Claude Code пропускает предложения](https://code.claude.com/docs/ru/interactive-mode.md#when-claude-code-skips-suggestions).

```typescript theme={null}
type SDKPromptSuggestionMessage = {
  type: "prompt_suggestion";
  suggestion: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKConversationResetMessage`

Отправляется, когда диалог сессии заменяется без завершения сессии. В вызове `query()` это сообщение создают только `/clear` и его псевдонимы. Подключите пустой транскрипт под `new_conversation_id` и отбросьте любой кэшированный заголовок сессии.

```typescript theme={null}
type SDKConversationResetMessage = {
  type: "conversation_reset";
  new_conversation_id: UUID;
  uuid: UUID;
  session_id: string;
  trigger?: "clear" | "plan_mode_exit" | "fresh_session" | "onboarding";
  user_message_uuid?: string;
  timestamp?: string;
};
```

Необязательные поля описывают сброс:

* `trigger`: что привело к отбрасыванию диалога. Сбрасывайте транскрипт при каждом сообщении `conversation_reset`, в том числе когда это поле отсутствует или содержит незнакомое значение.
* `user_message_uuid`: `uuid` пользовательского сообщения, содержавшего `/clear`. Используйте его, чтобы сопоставить сброс с этим сообщением.
* `timestamp`: когда произошёл сброс, в виде строки ISO 8601 в UTC. Используйте его для отображения, а не для упорядочивания сообщений.

Поля `trigger`, `user_message_uuid` и `timestamp` требуют Claude Code v2.1.281 или более поздней версии.

Опубликованные типизации SDK объявляют `SDKConversationResetMessage` в Claude Code v2.1.203 и более поздних версиях. До v2.1.203 `SDKMessage` ссылался на этот тип, не объявляя его, поэтому сужение по `type === "conversation_reset"` не проходило проверку типов при отключённом `skipLibCheck`.

### `BUILTIN_TOOL_NAMES` и `LEGACY_TOOL_NAME_ALIASES`

Используйте эти две константы для проверки имён инструментов, которые вводят пользователи вашего приложения. Обе записывают каждое имя так, как вы пишете его в правилах разрешений, matcher хуков и параметрах `tools` и `disallowedTools`. Импортируйте их из `@anthropic-ai/claude-agent-sdk` или из `@anthropic-ai/claude-agent-sdk/core`. Они требуют Agent SDK v0.3.301 или более поздней версии и находятся в статусе альфа.

Объявления типов SDK задают для `BUILTIN_TOOL_NAMES` тип readonly-кортежа, а для `LEGACY_TOOL_NAME_ALIASES` — тип записи, сопоставляющей строку строке:

```typescript theme={null}
const BUILTIN_TOOL_NAMES: readonly ["Agent", /* ...more names... */ "Write"];
const LEGACY_TOOL_NAME_ALIASES: Readonly<Record<string, string>>;
```

* **`BUILTIN_TOOL_NAMES`**: имена встроенных инструментов Claude Code в алфавитном порядке, например `Agent`, `Bash` и `Read`. Имена инструментов MCP не включены. Поскольку тип является кортежем строковых литералов, `(typeof BUILTIN_TOOL_NAMES)[number]` даёт тип-объединение этих имён
* **`LEGACY_TOOL_NAME_ALIASES`**: прежние имена инструментов, которые по-прежнему принимаются правилами разрешений, matcher хуков и параметрами `tools` и `disallowedTools`. Каждый ключ — прежнее имя, а его значение — текущее: например, `Task` сопоставляется с `Agent`, а `KillShell` и `KillBash` — с `TaskStop`

Подтвердить имя можно любой из двух проверок: `BUILTIN_TOOL_NAMES` включает его или `Object.hasOwn(LEGACY_TOOL_NAME_ALIASES, name)` возвращает `true`. Имя, не прошедшее обе проверки, всё равно может быть допустимым, потому что `BUILTIN_TOOL_NAMES` не включает инструменты MCP и некоторые встроенные инструменты. Если вы составляете список запретов на основе `BUILTIN_TOOL_NAMES`, Claude по-прежнему сможет использовать инструменты, не вошедшие в константу. Чтобы запретить все инструменты, задайте вместо этого [`disallowedTools: ["*"]`](https://code.claude.com/docs/ru/agent-sdk/permissions#allow-and-deny-rules).

Наличие имени в `BUILTIN_TOOL_NAMES` не означает, что у сессии есть этот инструмент: `TodoWrite` присутствует в списке, хотя он [отключён по умолчанию](https://code.claude.com/docs/ru/tools-reference.md). Чтобы узнать, какие инструменты есть у сессии, прочитайте массив `tools` её [`SDKSystemMessage`](#sdksystemmessage). Этот массив включает инструменты MCP и перечисляет инструмент Agent как `Task`, поэтому перед сравнением с `BUILTIN_TOOL_NAMES` сопоставьте каждое имя через `LEGACY_TOOL_NAME_ALIASES`.

### `AbortError`

Пользовательский класс ошибки для операций прерывания.

```typescript theme={null}
class AbortError extends Error {}
```

`AbortError` — единственный класс ошибок в типизированном API SDK. Другие сбои, например завершение процесса Claude Code или ошибка его запуска, отклоняют итерацию сообщений с ошибками, у которых нет класса SDK для сопоставления. В разделе [Устранение неполадок](https://code.claude.com/docs/ru/agent-sdk/troubleshooting.md) эти ошибки перечислены по тексту сообщения вместе с причиной и способом исправления для каждой.

## Конфигурация Sandbox

### `SandboxSettings`

Конфигурация для поведения sandbox. Используйте это для включения sandboxing команд и программной конфигурации ограничений сети.

```typescript theme={null}
type SandboxSettings = {
  enabled?: boolean;
  failIfUnavailable?: boolean;
  autoAllowBashIfSandboxed?: boolean;
  excludedCommands?: string[];
  allowUnsandboxedCommands?: boolean;
  network?: SandboxNetworkConfig;
  filesystem?: SandboxFilesystemConfig;
  ignoreViolations?: Record<string, string[]>;
  enableWeakerNestedSandbox?: boolean;
  allowNestedUserNamespaces?: boolean;
  ripgrep?: { command: string; args?: string[] };
};
```

| Свойство | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `enabled` | `boolean` | `false` | Включите режим sandbox для выполнения команд |
| `failIfUnavailable` | `boolean` | `true` | Остановитесь при запуске, если `enabled` имеет значение `true`, но sandbox не может запуститься. Установите `false` для возврата к выполнению без sandbox с предупреждением на stderr |
| [`autoAllowBashIfSandboxed`](https://code.claude.com/docs/ru/settings-reference#sandbox-autoallowbashifsandboxed) | `boolean` | `false` | Автоматически одобряйте команды Bash, когда sandbox включён. Значение по умолчанию `false` требует Agent SDK v0.3.324 или новее |
| `excludedCommands` | `string[]` | `[]` | Команды, которые обходят ограничения sandbox, такие как `['docker *']`. Они работают без sandbox автоматически без участия модели; [`sandbox.excludedCommands`](https://code.claude.com/docs/ru/settings-reference#sandbox-excludedcommands) описывает, когда применяется запись |
| `allowUnsandboxedCommands` | `boolean` | `true` | Разрешите модели запрашивать выполнение команд вне sandbox. Когда `true`, модель может установить `dangerouslyDisableSandbox` в входных данных tool, что переходит к [системе разрешений](#permissions-fallback-for-unsandboxed-commands) |
| `network` | [`SandboxNetworkConfig`](#sandboxnetworkconfig) | `undefined` | Конфигурация sandbox, специфичная для сети |
| `filesystem` | [`SandboxFilesystemConfig`](#sandboxfilesystemconfig) | `undefined` | Конфигурация sandbox, специфичная для файловой системы, для ограничений чтения/записи |
| `ignoreViolations` | `Record<string, string[]>` | `undefined` | Нарушения, которые не нужно включать в отчёт о нарушениях песочницы. Каждый ключ соответствует части команды или `*` для любой команды, а каждое значение перечисляет текст для поиска в строке нарушения: `{ "*": ['/etc/hosts'] }` скрывает нарушения, в которых упоминается `/etc/hosts`. См. [`sandbox.ignoreViolations`](https://code.claude.com/docs/ru/settings-reference#sandbox-ignoreviolations) |
| `enableWeakerNestedSandbox` | `boolean` | `false` | Включите более слабый вложенный sandbox для совместимости |
| `allowNestedUserNamespaces` | `boolean` | `false` | Разрешите командам в песочнице на Linux и WSL2 создавать пользовательские пространства имён (user namespaces). Прежде чем установить значение `true`, прочитайте [`sandbox.allowNestedUserNamespaces`](https://code.claude.com/docs/ru/settings-reference#sandbox-allownestedusernamespaces), где описаны инструменты, которым это нужно, и граница безопасности, которую вы отключаете. Требует Claude Code v2.1.305 или позже |
| `ripgrep` | `{ command: string; args?: string[] }` | `undefined` | Конфигурация пользовательского бинарного файла ripgrep для окружений sandbox |

> [!NOTE]
>
> Sandbox зависит от поддержки платформы и, на Linux, инструментов, таких как `bubblewrap` и `socat`. Когда `enabled` имеет значение `true` и sandbox не может запуститься, `query()` сообщает сообщение `result` с `subtype: "error_during_execution"` и причину в `errors`. Для одного вызова сообщения `query()` SDK выбрасывает после выдачи этого результата ошибки, поэтому оберните цикл в блок try для продолжения после него. Смотрите [Handle the result](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#handle-the-result) для контракта ошибки.
>
> Для выполнения без sandbox вместо этого установите `failIfUnavailable: false`.

#### Пример использования

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

try {
  for await (const message of query({
    prompt: "Build and test my project",
    options: {
      sandbox: {
        enabled: true,
        autoAllowBashIfSandboxed: true,
        network: {
          allowLocalBinding: true
        }
      }
    }
  })) {
    if ("result" in message) console.log(message.result);
  }
} catch (error) {
  // A single-shot query() throws after yielding an error result,
  // such as when the sandbox can't start (failIfUnavailable defaults to true).
  console.log(`Session ended with an error: ${error}`);
}
```

> [!WARNING]
>
> **Безопасность Unix socket:** Опция `allowUnixSockets` может предоставить доступ к системным сервисам, которые выходят за пределы sandbox. Например, разрешение `/var/run/docker.sock` фактически предоставляет полный доступ к хост-системе через Docker API, обходя изоляцию sandbox. Разрешайте только Unix sockets, которые строго необходимы, и поймите последствия безопасности каждого.

### `SandboxNetworkConfig`

Конфигурация, специфичная для сети, для режима sandbox. Эти параметры применяются к sandboxed Bash командам, когда `enabled` имеет значение `true` в родительском [`SandboxSettings`](#sandboxsettings). Они не ограничивают инструмент WebFetch, который использует [правила разрешений](https://code.claude.com/docs/ru/permissions.md#webfetch) вместо этого.

```typescript theme={null}
type SandboxNetworkConfig = {
  allowedDomains?: string[];
  deniedDomains?: string[];
  strictAllowlist?: boolean;
  allowManagedDomainsOnly?: boolean;
  allowLocalBinding?: boolean;
  allowUnixSockets?: string[];
  allowAllUnixSockets?: boolean;
  httpProxyPort?: number;
  socksProxyPort?: number;
};
```

| Свойство | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `allowedDomains` | `string[]` | `[]` | Имена доменов, к которым процессы в sandbox могут получить доступ |
| `deniedDomains` | `string[]` | `[]` | Имена доменов, к которым процессы в sandbox не могут получить доступ. Имеет приоритет над `allowedDomains` |
| `strictAllowlist` | `boolean` | `false` | Запретите sandboxed командам доступ к хостам вне [сетевого allowlist](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) вместо запроса. Применяется только для sandboxed команд; встроенные инструменты, такие как WebFetch, не контролируются этим. Учитывается только из пользовательских, управляемых или CLI `--settings` параметров; параметры проекта игнорируются. Требует Claude Code v2.1.219 или позже |
| `allowManagedDomainsOnly` | `boolean` | `false` | Только управляемые параметры. Когда установлено в [управляемых параметрах](https://code.claude.com/docs/ru/managed-settings.md), только записи `allowedDomains` и правила разрешения `WebFetch(domain:...)` из управляемых параметров учитываются, а записи разрешения из пользовательских, проектных или локальных параметров игнорируются. Из SDK передайте это через опцию [`managedSettings`](#options) |
| `allowLocalBinding` | `boolean` | `false` | Разрешите процессам привязываться к локальным портам (например, для dev серверов) |
| `allowUnixSockets` | `string[]` | `[]` | Пути Unix socket, к которым процессы могут получить доступ (например, Docker socket) |
| `allowAllUnixSockets` | `boolean` | `false` | Разрешите доступ ко всем Unix sockets, а на Linux — и к сокетам виртуальных машин (`AF_VSOCK`) |
| `httpProxyPort` | `number` | `undefined` | Порт HTTP прокси для сетевых запросов |
| `socksProxyPort` | `number` | `undefined` | Порт SOCKS прокси для сетевых запросов |

> [!NOTE]
>
> Встроенный прокси sandbox применяет `allowedDomains` на основе запрашиваемого имени хоста. По умолчанию прокси не завершает и не проверяет трафик TLS, поэтому такие методы, как [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting), потенциально могут обойти `allowedDomains`. Смотрите [Ограничения безопасности Sandboxing](https://code.claude.com/docs/ru/sandboxing.md#security-limitations) для деталей и [Безопасное развёртывание](https://code.claude.com/docs/ru/agent-sdk/secure-deployment.md#traffic-forwarding) для конфигурации прокси, завершающего TLS.

### `SandboxFilesystemConfig`

Конфигурация, специфичная для файловой системы, для режима sandbox.

```typescript theme={null}
type SandboxFilesystemConfig = {
  allowWrite?: string[];
  denyWrite?: string[];
  denyRead?: string[];
};
```

| Свойство | Тип | По умолчанию | Описание |
| :- | :- | :- | :- |
| `allowWrite` | `string[]` | `[]` | Паттерны путей файлов для разрешения доступа на запись |
| `denyWrite` | `string[]` | `[]` | Паттерны путей файлов для запрещения доступа на запись. Чтобы заблокировать запись из песочницы в файл в рабочем каталоге сессии, укажите его абсолютный путь. |
| `denyRead` | `string[]` | `[]` | Паттерны путей файлов для запрещения доступа на чтение |

### Fallback разрешений для команд вне Sandbox

Когда `allowUnsandboxedCommands` включён, модель может запросить выполнение команд вне sandbox, установив `dangerouslyDisableSandbox: true` во входных данных tool. Эти запросы переходят к существующей системе разрешений, что означает, что ваш обработчик `canUseTool` вызывается, позволяя вам реализовать пользовательскую логику авторизации.

Ваши записи `excludedCommands` вместо этого автоматически обходят sandbox без участия модели; [`sandbox.excludedCommands`](https://code.claude.com/docs/ru/settings-reference#sandbox-excludedcommands) описывает, когда применяется запись.

В примере ниже `isCommandAuthorized` служит заместителем для проверки авторизации, которую вы определяете.

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Deploy my application",
  options: {
    sandbox: {
      enabled: true,
      allowUnsandboxedCommands: true // Модель может запросить выполнение вне sandbox
    },
    permissionMode: "default",
    canUseTool: async (tool, input) => {
      // Проверьте, запрашивает ли модель обход sandbox
      if (tool === "Bash" && input.dangerouslyDisableSandbox) {
        // Модель запрашивает выполнение этой команды вне sandbox
        console.log(`Unsandboxed command requested: ${input.command}`);

        if (isCommandAuthorized(input.command)) {
          return { behavior: "allow" as const, updatedInput: input };
        }
        return {
          behavior: "deny" as const,
          message: "Command not authorized for unsandboxed execution"
        };
      }
      return { behavior: "allow" as const, updatedInput: input };
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

> [!WARNING]
>
> Команды, работающие с `dangerouslyDisableSandbox: true`, имеют полный доступ к системе. Убедитесь, что ваш обработчик `canUseTool` тщательно проверяет эти запросы.
>
> Если `permissionMode` установлен на `bypassPermissions` и `allowUnsandboxedCommands` включён, модель может автономно выполнять команды вне sandbox без запросов одобрения, кроме [действий, которые ни один режим не одобряет автоматически](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves). Эта комбинация фактически позволяет модели молча выходить из изоляции sandbox.

## См. также

* [Обзор SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) - Общие концепции SDK
* [Справочник Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md) - Документация Python SDK
* [Справочник CLI](https://code.claude.com/docs/ru/cli-reference.md) - Интерфейс командной строки
* [Общие рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md) - Пошаговые руководства
