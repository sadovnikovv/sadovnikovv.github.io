> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Отмотка изменений файлов с помощью checkpointing

> Отслеживайте изменения файлов во время сеансов агента и восстанавливайте файлы в любое предыдущее состояние

File checkpointing отслеживает изменения файлов, внесённые через инструменты [Write](https://code.claude.com/docs/ru/tools-reference.md#write-tool-behavior), [Edit](https://code.claude.com/docs/ru/tools-reference.md#edit-tool-behavior) и [NotebookEdit](https://code.claude.com/docs/ru/tools-reference.md#notebookedit-tool-behavior) во время сеанса агента, позволяя вам отмотать файлы в любое предыдущее состояние. Чтобы увидеть, как отмотка восстанавливает файл, перейдите к [интерактивному примеру](#try-it-out).

> [!WARNING]
>
> `rewindFiles()` не отменяет изменения, которые `sed -i` или другая команда Bash внесла в файл, если только этот файл не был изменён в основном диалоге таким инструментом, как Write или Edit. Правки [субагентов](https://code.claude.com/docs/ru/agent-sdk/subagents.md) не отслеживаются, тогда как правки [скилла с `context: fork`](https://code.claude.com/docs/ru/skills#run-skills-in-a-subagent), работающего на переднем плане, отслеживаются.

## Как работает checkpointing

Когда вы включаете file checkpointing, SDK создаёт резервные копии файлов перед их изменением через инструменты Write, Edit или NotebookEdit. Каждый промпт, с которого начинается ход, является checkpoint, а UUID его пользовательского сообщения служит точкой восстановления.

> [!NOTE]
>
> File rewinding восстанавливает файлы на диске в предыдущее состояние. Это не отматывает саму беседу. История беседы и контекст остаются нетронутыми после вызова `rewindFiles()` (TypeScript) или `rewind_files()` (Python).

Когда вы отматываете к checkpoint, Claude Code удаляет файлы, которые он создал, и восстанавливает файлы, которые он изменил, до их содержимого в этот момент. Claude Code пропускает отслеживаемый путь, который является символической ссылкой, жёсткой ссылкой или другим нерегулярным файлом. Он также пропускает отслеживаемый файл, родительский каталог которого больше не разрешается в его местоположение во время checkpoint, или чей резервную копию он не может безопасно прочитать. [`RewindFilesResult`](https://code.claude.com/docs/ru/agent-sdk/typescript#rewindfilesresult) подсчитывает каждый пропущенный путь в своём поле `skippedLinks`. Пропуск требует Claude Code v2.1.216 или позже; до v2.1.216 rewind писал и удалял через ссылки на отслеживаемых путях.

## Реализация checkpointing

Чтобы использовать file checkpointing, включите его в ваших параметрах, захватите UUID checkpoint из потока ответов, затем вызовите `rewindFiles()` (TypeScript) или `rewind_files()` (Python) когда вам нужно восстановить.

Примеры в этом разделе используют приглашение "Refactor the authentication module". Запустите их в проекте, который содержит модуль аутентификации, или измените приглашение на имена файлов, которые существуют в вашем проекте, чтобы вы могли наблюдать изменения файлов и видеть, как отмотка восстанавливает их.

Этот пример включает checkpointing, захватывает UUID checkpoint и ID сеанса из потока ответов, затем возобновляет сеанс позже для отмотки файлов. Пронумерованные комментарии примера соответствуют шагам, которые следуют ниже.

```python Python theme={null}
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


async def main():
    # Step 1: Enable checkpointing
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",  # Auto-accept file edits without prompting
        extra_args={
            "replay-user-messages": None
        },  # Required to receive checkpoint UUIDs in the response stream
    )

    checkpoint_id = None
    session_id = None

    # Run the query and capture checkpoint UUID and session ID
    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        # Step 2: Capture checkpoint UUID from the first user message
        async for message in client.receive_response():
            if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
                checkpoint_id = message.uuid
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    # Step 3: Later, rewind by resuming the session with an empty prompt
    if checkpoint_id and session_id:
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")  # Empty prompt to open the connection
            async for message in client.receive_response():
                await client.rewind_files(checkpoint_id)
                break
        print(f"Rewound to checkpoint: {checkpoint_id}")


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  // Step 1: Enable checkpointing
  const opts = {
    enableFileCheckpointing: true,
    permissionMode: "acceptEdits" as const, // Auto-accept file edits without prompting
    extraArgs: { "replay-user-messages": null } // Required to receive checkpoint UUIDs in the response stream
  };

  const response = query({
    prompt: "Refactor the authentication module",
    options: opts
  });

  let checkpointId: string | undefined;
  let sessionId: string | undefined;

  // Step 2: Capture checkpoint UUID from the first user message
  try {
    for await (const message of response) {
      if (message.type === "user" && message.uuid && !checkpointId) {
        checkpointId = message.uuid;
      }
      if ("session_id" in message && !sessionId) {
        sessionId = message.session_id;
      }
    }
  } catch (error) {
    // A single-shot query() throws after yielding an error result. If the
    // failure was an error result, sessionId and checkpointId were already
    // captured by the loop above; connection or process failures yield no
    // result message.
    console.error(`Session ended with an error: ${error}`);
  }

  // Step 3: Later, rewind by resuming the session with an empty prompt
  if (checkpointId && sessionId) {
    const rewindQuery = query({
      prompt: "", // Empty prompt to open the connection
      options: { ...opts, resume: sessionId }
    });

    for await (const msg of rewindQuery) {
      await rewindQuery.rewindFiles(checkpointId);
      break;
    }
    console.log(`Rewound to checkpoint: ${checkpointId}`);
  }
}

main();
```

**1. Включение checkpointing**

Настройте параметры SDK для включения checkpointing и получения UUID checkpoint:

| Параметр | Python | TypeScript | Описание |
| - | - | - | - |
| Включить checkpointing | `enable_file_checkpointing=True` | `enableFileCheckpointing: true` | Отслеживает изменения файлов для отмотки |
| Получить UUID checkpoint | `extra_args={"replay-user-messages": None}` | `extraArgs: { 'replay-user-messages': null }` | Требуется для получения UUID пользовательских сообщений в потоке |

Основной пример в разделе [Реализация checkpointing](#implement-checkpointing) также устанавливает режим разрешений на `acceptEdits`, который одобряет редактирование файлов агентом без приглашения. Для получения дополнительной информации см. [Режимы разрешений](https://code.claude.com/docs/ru/agent-sdk/permissions.md#permission-modes).

**2. Захват UUID checkpoint и ID сеанса**

При установленном параметре `replay-user-messages` пользовательское сообщение для каждого промпта, начинающего ход, имеет UUID, который служит чекпоинтом. Пользовательские сообщения, содержащие результаты инструментов, тоже имеют UUID, но он не является чекпоинтом.

Для большинства случаев использования захватите UUID первого пользовательского сообщения (`message.uuid`); отмотка к нему восстанавливает отслеживаемые файлы в их исходное состояние. Чтобы сохранить несколько checkpoint и отмотать к промежуточным состояниям, см. [Несколько точек восстановления](#multiple-restore-points).

Захват ID сеанса (`message.session_id`) является необязательным; вам он нужен только если вы хотите отмотать позже, после завершения потока. Если вы вызываете `rewindFiles()` немедленно, пока всё ещё обрабатываете сообщения (как это делает пример в [Checkpoint перед рискованными операциями](#checkpoint-before-risky-operations)), вы можете пропустить захват ID сеанса.

**3. Отмотка файлов**

Чтобы отмотать после завершения потока, возобновите сеанс с пустым приглашением и вызовите `rewind_files()` (Python) или `rewindFiles()` (TypeScript) с вашим UUID checkpoint. Включите checkpointing в параметрах возобновленного сеанса также, и вызовите отмотку изнутри цикла ответов. Вы также можете отмотать во время потока. См. [Checkpoint перед рискованными операциями](#checkpoint-before-risky-operations) для этого паттерна.

Если вы захватили ID сеанса и UUID checkpoint, вы также можете отмотать из CLI. Эта команда требует исполняемого файла `claude`, который поставляется с [установкой Claude Code](https://code.claude.com/docs/ru/setup.md). SDK включает checkpointing для вас, но когда вы запускаете `claude -p` напрямую, вы должны установить переменную окружения `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING`:

```bash theme={null}
CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true claude -p --resume <session-id> --rewind-files <checkpoint-uuid>
```

Флаг `--rewind-files` не отображается в выводе `claude --help`, но CLI принимает его, как показано. Когда отмотка успешна, команда выводит `Files rewound to state at message <checkpoint-uuid>` и завершается без отправки приглашения.

## Общие паттерны

Эти паттерны показывают различные способы захвата и использования UUID checkpoint в зависимости от вашего случая использования.

### Checkpoint перед рискованными операциями

Этот паттерн сохраняет только самый последний UUID чекпоинта и обновляет его при каждом промпте, который начинает ход. Если что-то пойдёт не так во время обработки, вы можете немедленно отмотать к последнему безопасному состоянию и выйти из цикла.

Перед запуском этого примера замените `your_revert_condition` (Python) или `yourRevertCondition` (TypeScript) на вашу собственную проверку, такую как обнаружение ошибок или сбой валидации; заполнитель не определён в примере.

```python Python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, UserMessage


async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    safe_checkpoint = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        async for message in client.receive_response():
            # Update checkpoint at each prompt you send; a tool result isn't one
            # This overwrites the previous checkpoint. Only keep the latest
            if (
                isinstance(message, UserMessage)
                and message.uuid
                and message.tool_use_result is None
                and message.parent_tool_use_id is None
            ):
                safe_checkpoint = message.uuid

            # Decide when to revert based on your own logic
            # For example: error detection, validation failure, or user input
            if your_revert_condition and safe_checkpoint:
                await client.rewind_files(safe_checkpoint)
                # Exit the loop after rewinding, files are restored
                break


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  const response = query({
    prompt: "Refactor the authentication module",
    options: {
      enableFileCheckpointing: true,
      permissionMode: "acceptEdits" as const,
      extraArgs: { "replay-user-messages": null }
    }
  });

  let safeCheckpoint: string | undefined;

  for await (const message of response) {
    // Update checkpoint at each prompt you send; a tool result isn't one
    // This overwrites the previous checkpoint. Only keep the latest
    if (message.type === "user" && "isReplay" in message && message.isReplay && message.uuid) {
      safeCheckpoint = message.uuid;
    }

    // Decide when to revert based on your own logic
    // For example: error detection, validation failure, or user input
    if (yourRevertCondition && safeCheckpoint) {
      await response.rewindFiles(safeCheckpoint);
      // Exit the loop after rewinding, files are restored
      break;
    }
  }
}

main();
```

### Несколько точек восстановления

Если Claude вносит изменения на протяжении нескольких промптов, вы можете захотеть отмотать к определённой точке, а не полностью назад. Например, если ваш первый промпт рефакторит файл, а второй добавляет тесты, отмотайте к чекпоинту второго промпта, чтобы сохранить рефакторинг и отменить тесты.

Этот паттерн сохраняет UUID каждого чекпоинта в массиве с метаданными. После завершения сессии вы можете отмотать к любому предыдущему чекпоинту:

```python Python theme={null}
import asyncio
from dataclasses import dataclass
from datetime import datetime
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


# Store checkpoint metadata for better tracking
@dataclass
class Checkpoint:
    id: str
    description: str
    timestamp: datetime


async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    checkpoints = []
    session_id = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")

        async for message in client.receive_response():
            if (
                isinstance(message, UserMessage)
                and message.uuid
                and message.tool_use_result is None
                and message.parent_tool_use_id is None
            ):
                checkpoints.append(
                    Checkpoint(
                        id=message.uuid,
                        description=f"After turn {len(checkpoints) + 1}",
                        timestamp=datetime.now(),
                    )
                )
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    # Later: rewind to any checkpoint by resuming the session
    if checkpoints and session_id:
        target = checkpoints[0]  # Pick any checkpoint
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")  # Empty prompt to open the connection
            async for message in client.receive_response():
                await client.rewind_files(target.id)
                break
        print(f"Rewound to: {target.description}")


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Store checkpoint metadata for better tracking
interface Checkpoint {
  id: string;
  description: string;
  timestamp: Date;
}

async function main() {
  const opts = {
    enableFileCheckpointing: true,
    permissionMode: "acceptEdits" as const,
    extraArgs: { "replay-user-messages": null }
  };

  const response = query({
    prompt: "Refactor the authentication module",
    options: opts
  });

  const checkpoints: Checkpoint[] = [];
  let sessionId: string | undefined;

  try {
    for await (const message of response) {
      if (message.type === "user" && "isReplay" in message && message.isReplay && message.uuid) {
        checkpoints.push({
          id: message.uuid,
          description: `After turn ${checkpoints.length + 1}`,
          timestamp: new Date()
        });
      }
      if ("session_id" in message && !sessionId) {
        sessionId = message.session_id;
      }
    }
  } catch (error) {
    // A single-shot query() throws after yielding an error result. If the
    // failure was an error result, sessionId and the checkpoints array were
    // already populated by the loop above; connection or process failures
    // yield no result message.
    console.error(`Session ended with an error: ${error}`);
  }

  // Later: rewind to any checkpoint by resuming the session
  if (checkpoints.length > 0 && sessionId) {
    const target = checkpoints[0]; // Pick any checkpoint
    const rewindQuery = query({
      prompt: "", // Empty prompt to open the connection
      options: { ...opts, resume: sessionId }
    });

    for await (const msg of rewindQuery) {
      await rewindQuery.rewindFiles(target.id);
      break;
    }
    console.log(`Rewound to: ${target.description}`);
  }
}

main();
```

## Попробуйте

Этот полный пример создаёт небольшой служебный файл, просит агента добавить комментарии к документации, показывает вам изменения, затем спрашивает, хотите ли вы отмотать.

Прежде чем начать, убедитесь, что у вас установлен [Claude Agent SDK](https://code.claude.com/docs/ru/agent-sdk/quickstart.md).

**1. Создание тестового файла**

Создайте новый файл с именем `utils.py` (Python) или `utils.ts` (TypeScript) и вставьте следующий код:

```python utils.py theme={null}
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```typescript utils.ts theme={null}
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}
```

**2. Запуск интерактивного примера**

Создайте новый файл с именем `try_checkpointing.py` (Python) или `try_checkpointing.ts` (TypeScript) в том же каталоге, что и ваш служебный файл, и вставьте следующий код.

Этот скрипт просит Claude добавить комментарии к документации в ваш служебный файл, затем даёт вам возможность отмотать и восстановить оригинал.

```python try_checkpointing.py theme={null}
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    UserMessage,
    ResultMessage,
)


async def main():
    # Configure the SDK with checkpointing enabled
    # - enable_file_checkpointing: Track file changes for rewinding
    # - permission_mode: Auto-accept file edits without prompting
    # - extra_args: Required to receive user message UUIDs in the stream
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )

    checkpoint_id = None  # Store the user message UUID for rewinding
    session_id = None  # Store the session ID for resuming

    print("Running agent to add doc comments to utils.py...\n")

    # Run the agent and capture checkpoint data from the response stream
    async with ClaudeSDKClient(options) as client:
        await client.query("Add doc comments to utils.py")

        async for message in client.receive_response():
            # Capture the first user message UUID - this is our restore point
            if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
                checkpoint_id = message.uuid
            # Capture the session ID so we can resume later
            if isinstance(message, ResultMessage):
                session_id = message.session_id

    print("Done! Open utils.py to see the added doc comments.\n")

    # Ask the user if they want to rewind the changes
    if checkpoint_id and session_id:
        response = input("Rewind to remove the doc comments? (y/n): ")

        if response.lower() == "y":
            # Resume the session with an empty prompt, then rewind
            async with ClaudeSDKClient(
                ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
            ) as client:
                await client.query("")  # Empty prompt opens the connection
                async for message in client.receive_response():
                    await client.rewind_files(checkpoint_id)  # Restore files
                    break

            print(
                "\n✓ File restored! Open utils.py to verify the doc comments are gone."
            )
        else:
            print("\nKept the modified file.")


asyncio.run(main())
```

```typescript try_checkpointing.ts theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";
import * as readline from "readline";

async function main() {
  // Configure the SDK with checkpointing enabled
  // - enableFileCheckpointing: Track file changes for rewinding
  // - permissionMode: Auto-accept file edits without prompting
  // - extraArgs: Required to receive user message UUIDs in the stream
  const opts = {
    enableFileCheckpointing: true,
    permissionMode: "acceptEdits" as const,
    extraArgs: { "replay-user-messages": null }
  };

  let sessionId: string | undefined; // Store the session ID for resuming
  let checkpointId: string | undefined; // Store the user message UUID for rewinding

  console.log("Running agent to add doc comments to utils.ts...\n");

  // Run the agent and capture checkpoint data from the response stream
  const response = query({
    prompt: "Add doc comments to utils.ts",
    options: opts
  });

  try {
    for await (const message of response) {
      // Capture the first user message UUID - this is our restore point
      if (message.type === "user" && message.uuid && !checkpointId) {
        checkpointId = message.uuid;
      }
      // Capture the session ID so we can resume later
      if ("session_id" in message) {
        sessionId = message.session_id;
      }
    }
  } catch (error) {
    // A single-shot query() throws after yielding an error result. If the
    // failure was an error result, checkpointId and sessionId were already
    // captured by the loop above; connection or process failures yield no
    // result message.
    console.error(`Session ended with an error: ${error}`);
  }

  console.log("Done! Open utils.ts to see the added doc comments.\n");

  // Ask the user if they want to rewind the changes
  if (checkpointId && sessionId) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const answer = await new Promise<string>((resolve) => {
      rl.question("Rewind to remove the doc comments? (y/n): ", resolve);
    });
    rl.close();

    if (answer.toLowerCase() === "y") {
      // Resume the session with an empty prompt, then rewind
      const rewindQuery = query({
        prompt: "", // Empty prompt opens the connection
        options: { ...opts, resume: sessionId }
      });

      for await (const msg of rewindQuery) {
        await rewindQuery.rewindFiles(checkpointId); // Restore files
        break;
      }

      console.log("\n✓ File restored! Open utils.ts to verify the doc comments are gone.");
    } else {
      console.log("\nKept the modified file.");
    }
  }
}

main();
```

**3. Запуск примера**

Запустите скрипт из того же каталога, что и ваш служебный файл.

> [!TIP]
>
> Откройте ваш служебный файл (`utils.py` или `utils.ts`) в вашей IDE или редакторе перед запуском скрипта. Вы увидите, как файл обновляется в реальном времени, когда агент добавляет комментарии к документации, затем вернётся к оригиналу, когда вы выберете отмотку.

> [tab] Python
>
> ```bash theme={null}
> python try_checkpointing.py
> ```

> [tab] TypeScript
>
> ```bash theme={null}
> npx tsx try_checkpointing.ts
> ```

Вы увидите, как агент добавляет комментарии к документации, затем появится приглашение, спрашивающее, хотите ли вы отмотать. Если вы выберете да, файл будет восстановлен в его исходное состояние.

## Ограничения

File checkpointing имеет следующие ограничения:

| Ограничение | Описание |
| - | - |
| Изменения командами Bash | Откат не отменяет изменения, внесённые командой Bash, за исключением файлов, которые основной диалог уже редактировал с помощью инструмента, такого как Write или Edit |
| Правки субагента | Правки, которые применяет [субагент](https://code.claude.com/docs/ru/agent-sdk/subagents.md), не отслеживаются, за исключением скилла с `context: fork`, работающего на переднем плане. Откат отменяет их только в тех файлах, которые основной диалог уже редактировал; для отката остальных используйте git |
| Один сеанс | Checkpoints привязаны к сеансу, который их создал |
| Только содержимое файла | Создание, перемещение или удаление каталогов не отменяется отмоткой |
| Локальные файлы | Удалённые или сетевые файлы не отслеживаются |

## Troubleshooting

### Параметры checkpointing не распознаны

Если `enableFileCheckpointing` или `rewindFiles()` недоступны, вы можете использовать старую версию SDK.

**Решение**: Обновитесь до последней версии SDK:

* **Python**: `pip install --upgrade claude-agent-sdk`
* **TypeScript**: `npm install @anthropic-ai/claude-agent-sdk@latest`

### Пользовательские сообщения не имеют UUID

Если `message.uuid` имеет значение `undefined` или отсутствует, вы не получаете UUID checkpoint.

**Причина**: Параметр `replay-user-messages` не установлен.

**Решение**: Добавьте `extra_args={"replay-user-messages": None}` (Python) или `extraArgs: { 'replay-user-messages': null }` (TypeScript) в ваши параметры.

### Ошибка "No file checkpoint found for this message"

Эта ошибка возникает, когда данные checkpoint не существуют для указанного UUID пользовательского сообщения.

**Частые причины**:

* File checkpointing не был включён в исходном сеансе (`enable_file_checkpointing` или `enableFileCheckpointing` не был установлен на `true`)
* Сеанс не был должным образом завершён перед попыткой возобновления и отмотки
* UUID взят из пользовательского сообщения, содержащего результат инструмента, которое не является чекпоинтом

**Решение**: Убедитесь, что `enable_file_checkpointing=True` (Python) или `enableFileCheckpointing: true` (TypeScript) был установлен в исходном сеансе, затем используйте паттерн, показанный в примерах: захватите UUID первого пользовательского сообщения, полностью завершите сеанс, затем возобновите с пустым приглашением и вызовите `rewindFiles()` один раз.

### Ошибка "File rewinding is not enabled"

Эта ошибка возникает, когда вы пытаетесь выполнить неинтерактивную отмотку без включённого checkpointing: запуск простой команды `claude -p` с `--rewind-files`, или запуск сеанса SDK, включая возобновленный, чьи параметры не включают checkpointing. SDK устанавливает переменную окружения `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING` внутренне только когда `enable_file_checkpointing` (Python) или `enableFileCheckpointing` (TypeScript) включены в сеансе, выполняющем отмотку; простой CLI никогда её не устанавливает.

**Решение**: Для простого CLI установите переменную окружения при запуске команды:

```bash theme={null}
CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true claude -p --resume <session-id> --rewind-files <checkpoint-uuid>
```

Для SDK установите `enable_file_checkpointing=True` (Python) или `enableFileCheckpointing: true` (TypeScript) в возобновленном сеансе, как это делается в примерах на этой странице.

### Ошибка "ProcessTransport is not ready for writing"

Эта ошибка возникает, когда вы вызываете `rewindFiles()` или `rewind_files()` после завершения итерации по ответу. Соединение с процессом CLI закрывается при завершении цикла.

**Решение**: Возобновите сеанс с пустым приглашением, затем отмотайте в новом запросе. Основной пример в разделе [Implement checkpointing](#implement-checkpointing) показывает вызов возобновления и отмотки на обоих языках, в комментарии, отмеченном как Step 3.

## Следующие шаги

* **[Sessions](https://code.claude.com/docs/ru/agent-sdk/sessions.md)**: узнайте, как возобновлять сеансы, что требуется для отмотки после завершения потока. Охватывает ID сеансов, возобновление бесед и разветвление сеансов.
* **[Permissions](https://code.claude.com/docs/ru/agent-sdk/permissions.md)**: настройте, какие инструменты может использовать Claude и как одобряются изменения файлов. Полезно, если вы хотите больше контроля над тем, когда происходят правки.
* **[TypeScript SDK reference](https://code.claude.com/docs/ru/agent-sdk/typescript.md)**: полный справочник API, включая все параметры для `query()` и метода `rewindFiles()`.
* **[Python SDK reference](https://code.claude.com/docs/ru/agent-sdk/python.md)**: полный справочник API, включая все параметры для `ClaudeAgentOptions` и метода `rewind_files()`.
