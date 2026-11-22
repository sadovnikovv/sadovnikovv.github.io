> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Отправка сообщений работающему агенту

> Отправляйте дополнительные сообщения и изображения в одну сессию Agent SDK с помощью потокового ввода, читайте каждый ответ и прерывайте ответ, чтобы перенаправить Claude.

Потоковый ввод держит сессию Agent SDK открытой, чтобы ваше приложение могло отправлять ей более одного сообщения во время её работы. Вы также можете прикреплять изображения к сообщению и останавливать ответ на полпути, чтобы перенаправить Claude.

> [!NOTE]
>
> Потоковый ввод относится к сообщениям, которые вы отправляете. Чтобы показывать ответ Claude по мере его генерации, см. [Потоковая передача ответов в реальном времени](https://code.claude.com/docs/ru/agent-sdk/streaming-output.md).

## Выбор между одноразовым и потоковым вводом

Выбирайте потоковый ввод для приложения, которое ведёт диалог с Claude, например для чат-интерфейса. Используйте потоковый ввод, чтобы прикреплять изображения к сообщению, прерывать ответ или [переключать модель или режим разрешений](https://code.claude.com/docs/ru/agent-sdk/configuration.md#change-configuration-mid-session) во время работы сессии.

Одноразовый вызов передаёт одну строку промпта в `query()`. Вызов завершается после того, как Claude на неё ответит. Одноразовый режим подходит для одной задачи, например для serverless-функции. Чтобы продолжить после завершения такого вызова, начните новый вызов, который возобновляет сессию. Подробнее см. [Продолжение, возобновление и ветвление](https://code.claude.com/docs/ru/agent-sdk/sessions.md#continue-resume-and-fork).

## Отправка более одного сообщения в сессию

* **TypeScript**: напишите [асинхронный генератор](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function%2A), который выдаёт объекты [`SDKUserMessage`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkusermessage), и передайте его как `prompt` в `query()`. Пусть генератор между выдачами ожидает следующего сообщения от вашего пользователя.
* **Python**: откройте `ClaudeSDKClient` и передавайте каждое сообщение в `client.query()`. Для текстового сообщения передайте строку. Чтобы прикрепить изображение, передайте [асинхронный генератор](https://docs.python.org/3/glossary.html#term-asynchronous-generator), который выдаёт словари пользовательских сообщений.

Чтобы Claude отвечал на каждое сообщение отдельным ответом, дождитесь [сообщения результата](#read-each-response) предыдущего ответа, прежде чем отправлять следующее:

* **TypeScript**: пусть ваш генератор ожидает promise. Разрешите его в цикле `for await` по `query()`, когда придёт сообщение результата.
* **Python**: вызовите `client.query()` со следующим сообщением после завершения цикла [`receive_response()`](https://code.claude.com/docs/ru/agent-sdk/python#claudesdkclient).

> [!NOTE]
>
> Сообщение, отправленное во время вызовов инструментов, доходит до Claude после завершения этих вызовов инструментов. Затем Claude отвечает на него и на ваше предыдущее сообщение в одном ответе. Если ход завершится раньше, Claude начнёт для него новый ход. Подробнее см. [Ходы и бюджет](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#turns-and-budget).

### Отправка дополнительного сообщения с изображением

Этот пример отправляет текстовый вопрос, затем дополнительное сообщение с изображением и выводит ответ Claude на каждое из них. Перед запуском сохраните PNG-изображение как `diagram.png` в рабочем каталоге:

```typescript TypeScript theme={null}
import { readFile } from "node:fs/promises";
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

let firstResponseDone!: () => void;
const firstResponseFinished = new Promise<void>((resolve) => {
  firstResponseDone = resolve;
});

async function* messages(): AsyncGenerator<SDKUserMessage> {
  yield {
    type: "user",
    message: {
      role: "user",
      content: "Explain in two sentences what a message queue does.",
    },
    parent_tool_use_id: null,
  };

  await firstResponseFinished;

  const image = await readFile("diagram.png");
  yield {
    type: "user",
    message: {
      role: "user",
      content: [
        { type: "text", text: "Describe this image in one sentence." },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: image.toString("base64"),
          },
        },
      ],
    },
    parent_tool_use_id: null,
  };
}

let responses = 0;
for await (const message of query({ prompt: messages() })) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
  } else if (message.type === "result") {
    responses += 1;
    console.log(`Response ${responses} finished: ${message.subtype}`);
    if (responses === 1) {
      firstResponseDone();
    }
  }
}
```

```python Python theme={null}
import asyncio
import base64
from pathlib import Path

from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, TextBlock


async def image_message():
    image_data = base64.b64encode(Path("diagram.png").read_bytes()).decode()
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in one sentence."},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
            ],
        },
    }


async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Explain in two sentences what a message queue does.")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 1 finished: {message.subtype}")

        await client.query(image_message())
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 2 finished: {message.subtype}")


asyncio.run(main())
```

При запуске любой из версий пример выводит `Response 1 finished: success` и `Response 2 finished: success`.

Если Claude не увидел ваше изображение, см. [Image could not be processed](https://code.claude.com/docs/ru/agent-sdk/troubleshooting.md#image-could-not-be-processed).

### Передача сообщений из чат-интерфейса в TypeScript

Передавайте сообщения пользователя в генератор промптов через очередь:

* **`pushMessage()`**: обработчик ввода вашего интерфейса вызывает эту функцию для каждого сообщения, отправленного пользователем.
* **`closeInput()`**: обработчик вызывает эту функцию, когда пользователь закрывает чат.
* **`userMessages()`**: генератор, который вы передаёте как `prompt` в `query()`.

`pushMessage()` добавляет каждое сообщение в массив, а генератор читает из этого массива. Когда массив пуст, генератор ожидает, пока не придёт сообщение или не закроется чат:

```typescript theme={null}
import type { SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

const pending: string[] = [];
let wake: (() => void) | null = null;
let closed = false;

// The interface's input handler calls this with each message the user sends.
function pushMessage(text: string): void {
  pending.push(text);
  wake?.();
}

// The interface calls this when the user closes the chat.
function closeInput(): void {
  closed = true;
  wake?.();
}

async function* userMessages(): AsyncGenerator<SDKUserMessage> {
  while (true) {
    const text = pending.shift();
    if (text !== undefined) {
      yield { type: "user", message: { role: "user", content: text }, parent_tool_use_id: null };
    } else if (closed) {
      return;
    } else {
      await new Promise<void>((resolve) => (wake = resolve));
      wake = null;
    }
  }
}
```

Сообщения, добавленные во время ответа, могут оказаться в одном ответе. Чтобы выбрать, когда Claude прочитает сообщение, добавленное во время ответа, задайте поле [`priority`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkusermessage) этого сообщения.

## Чтение каждого ответа

Claude завершает каждый ответ сообщением результата.

* **TypeScript**: цикл `for await` по `query()` выдаёт сообщения каждого ответа по порядку. Цикл завершается после сообщения результата последнего ответа, когда ваш генератор вернул управление. Чтобы сопоставить результат с сообщениями, на которые он отвечает, задайте `uuid` каждому отправляемому сообщению и прочитайте [`user_message_uuids`](https://code.claude.com/docs/ru/agent-sdk/typescript#user_message_uuids) результата.
* **Python**: запускайте цикл `receive_response()` для каждого ответа, поскольку каждый цикл останавливается после следующего [`ResultMessage`](https://code.claude.com/docs/ru/agent-sdk/python#resultmessage). Клиент сохраняет контекст диалога от одного сообщения к другому. Подробнее см. [Автоматическое управление сессиями](https://code.claude.com/docs/ru/agent-sdk/sessions.md#automatic-session-management).

Поле `subtype` сообщения результата сообщает, как завершился ответ, например `success` или `error_during_execution`.

Если последний ответ завершается результатом ошибки:

* **TypeScript**: цикл по `query()` выдаёт этот результат, а затем выбрасывает исключение. Оберните цикл в `try`/`catch`, чтобы обработать исключение. Чтобы продолжить диалог после исключения, начните новый вызов `query()`, который [возобновляет сессию](https://code.claude.com/docs/ru/agent-sdk/sessions.md#continue-resume-and-fork). Пока у вашего генератора ещё есть сообщения для отправки, результат ошибки для более раннего ответа не выбрасывает исключение.
* **Python**: `receive_response()` у `ClaudeSDKClient` выдаёт результат ошибки, не выбрасывая исключение.

О значении каждого подтипа результата см. [Обработка результата](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#handle-the-result).

## Прерывание ответа Claude

Чтобы остановить ответ на полпути и оставить сессию открытой, вызовите `interrupt()` у объекта, который выполняет сессию:

* **TypeScript**: передайте асинхронный генератор как `prompt`, сохраните [объект `Query`](https://code.claude.com/docs/ru/agent-sdk/typescript#query-object), возвращаемый `query()`, и вызовите у него `interrupt()`.
* **Python**: вызовите `interrupt()` у `ClaudeSDKClient`. Если цикл `receive_response()` читает ответ, этот цикл завершается на `ResultMessage` прерванного ответа. Отправляйте следующее сообщение после получения этого результата.

Если вызвать `interrupt()` во время ответа, этот ответ завершается результатом `error_during_execution`. Сообщения, отправленные до прерывания и ещё не прочитанные Claude, всё равно дойдут до Claude после завершения прерванного ответа. О том, что делает цикл TypeScript, когда последний ответ является результатом ошибки, см. [Чтение каждого ответа](#read-each-response).

Этот пример просит Claude написать длинное эссе. Пример вызывает `interrupt()` через три секунды после начала сессии, а затем, когда прерванный ответ завершится, отправляет второе сообщение в ту же сессию:

```typescript TypeScript theme={null}
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";

let firstResponseDone!: () => void;
const firstResponseFinished = new Promise<void>((resolve) => {
  firstResponseDone = resolve;
});

async function* messages(): AsyncGenerator<SDKUserMessage> {
  yield {
    type: "user",
    message: {
      role: "user",
      content: "Write a 2,000-word essay on the history of the printing press.",
    },
    parent_tool_use_id: null,
  };

  await firstResponseFinished;

  yield {
    type: "user",
    message: {
      role: "user",
      content: "In one sentence, what is a prime number?",
    },
    parent_tool_use_id: null,
  };
}

const conversation = query({ prompt: messages() });

let responses = 0;
for await (const message of conversation) {
  if (message.type === "system" && message.subtype === "init" && responses === 0) {
    setTimeout(async () => {
      await conversation.interrupt();
      console.log("Interrupt sent");
    }, 3000);
  } else if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "text") {
        console.log(block.text);
      }
    }
  } else if (message.type === "result") {
    responses += 1;
    console.log(`Response ${responses} finished: ${message.subtype}`);
    if (responses === 1) {
      firstResponseDone();
    }
  }
}
```

```python Python theme={null}
import asyncio

from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, TextBlock


async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Write a 2,000-word essay on the history of the printing press.")
        await asyncio.sleep(3)
        await client.interrupt()
        print("Interrupt sent")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 1 finished: {message.subtype}")

        await client.query("In one sentence, what is a prime number?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Response 2 finished: {message.subtype}")


asyncio.run(main())
```

При запуске любой из версий первый ответ останавливается посреди эссе, и пример выводит `Response 1 finished: error_during_execution`. Затем Claude отвечает на второе сообщение. Вывод завершается строкой `Response 2 finished: success`.

## Следующие шаги

* [Потоковая передача ответов в реальном времени](https://code.claude.com/docs/ru/agent-sdk/streaming-output.md): показывайте текст и вызовы инструментов по мере их генерации Claude
* [Обработка подтверждений и пользовательского ввода](https://code.claude.com/docs/ru/agent-sdk/user-input.md): отвечайте на запросы разрешений и уточняющие вопросы Claude
* [Изменение конфигурации посреди сессии](https://code.claude.com/docs/ru/agent-sdk/configuration.md#change-configuration-mid-session): переключайте модель или режим разрешений во время работы сессии
* [Объект `Query`](https://code.claude.com/docs/ru/agent-sdk/typescript#query-object) в TypeScript и [`ClaudeSDKClient`](https://code.claude.com/docs/ru/agent-sdk/python#claudesdkclient) в Python: методы, которые отправляют сообщения в работающую сессию или управляют ею
* [Работа с сессиями](https://code.claude.com/docs/ru/agent-sdk/sessions.md): возобновляйте, продолжайте или ветвите диалог
