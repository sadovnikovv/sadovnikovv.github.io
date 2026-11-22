> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Расширение агентов с помощью скиллов

> Управляйте тем, какие скиллы Claude может вызывать в сессиях Claude Agent SDK, вызывайте команды по имени и создавайте скиллы, которые обнаруживаются вашими сессиями

Agent Skills расширяют Claude специализированными возможностями, которые Claude вызывает, когда они уместны. Скиллы упаковываются в файлы `SKILL.md`, содержащие инструкции, описания и необязательные вспомогательные ресурсы. На этой странице также рассматриваются [команды в сессиях Agent SDK](#commands-in-agent-sdk-sessions).

Дополнительную информацию о скиллах, включая преимущества, архитектуру и рекомендации по их созданию, см. в [обзоре Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## Как skills работают с Agent SDK

При использовании Claude Agent SDK skills:

* **Определяются как артефакты файловой системы**: вы создаёте каждый skill как файл `SKILL.md` в его собственном каталоге, например `.claude/skills/<name>/SKILL.md`
* **Загружаются из файловой системы**: SDK загружает skills из расположений файловой системы, управляемых `settingSources` (TypeScript) или `setting_sources` (Python)
* **Автоматически обнаруживаются**: после загрузки параметров файловой системы SDK обнаруживает метаданные skill при запуске из пользовательских и проектных каталогов и загружает полное содержимое, когда Claude вызывает skill
* **Вызываются моделью**: Claude автономно выбирает, когда их использовать, на основе контекста
* **Вызываются пользователем**: вы отправляете skill напрямую, отправляя `/<name>` в подсказку. См. [Команды в сеансах Agent SDK](#commands-in-agent-sdk-sessions)
* **Ограничиваются через опцию `skills`**: обнаруженные skills включены по умолчанию. Передайте список имён skills, `"all"` или `[]` для управления тем, какие skills может вызывать Claude

В отличие от subagents, которые вы можете определить в [опции `agents`](https://code.claude.com/docs/ru/agent-sdk/subagents#programmatic-definition-recommended), вы создаёте skills как файлы на диске. SDK не предоставляет программный API для их регистрации.

> [!NOTE]
>
> Skills обнаруживаются через источники параметров файловой системы. С параметрами `query()` по умолчанию SDK загружает пользовательские и проектные источники, поэтому skills в `~/.claude/skills/`, `<cwd>/.claude/skills/` и `.claude/skills/` в любом родительском каталоге `<cwd>` вплоть до корня репозитория доступны. Проектный источник также охватывает `<dir>/.claude/skills/` в каждом каталоге, который вы передаёте через `additionalDirectories` (TypeScript) или `add_dirs` (Python), потому что SDK передаёт эти каталоги в Claude Code как [`--add-dir`](https://code.claude.com/docs/ru/skills#skills-from-additional-directories). Если вы явно установите `settingSources`, включите `'project'` для сохранения skills проекта и добавленного каталога и `'user'` для сохранения ваших личных skills, или используйте [опцию `plugins`](https://code.claude.com/docs/ru/agent-sdk/plugins) для загрузки skills из определённого пути.

## Использование скиллов с Agent SDK

Установите опцию `skills` в `query()`, чтобы управлять тем, какие скиллы Claude может вызывать в сессии. Если опция опущена, обнаруженные скиллы включены и инструмент Skill доступен, что соответствует поведению CLI. Передайте `"all"`, чтобы Claude мог вызывать каждый обнаруженный скилл, список имён скиллов, чтобы разрешить только их, или `[]`, чтобы Claude не мог вызывать ни один.

Например, чтобы позволить Claude вызывать только два скилла с указанными именами:

```python Python theme={null}
options = ClaudeAgentOptions(skills=["pdf", "docx"])
```

```typescript TypeScript theme={null}
const options = { skills: ["pdf", "docx"] };
```

### Настройка скиллов в сессии

Когда вы устанавливаете `skills`, SDK автоматически добавляет инструмент Skill в `allowedTools`. Если вы также передаёте явный список `tools`, включите `"Skill"` в этот список, чтобы Claude мог вызывать скиллы.

После настройки Claude автоматически обнаруживает скиллы в файловой системе и вызывает их, когда они относятся к запросу пользователя.

Следующий пример включает каждый обнаруженный скилл в сессии и предварительно одобряет инструменты, которые обычно нужны скиллам. Пример устанавливает `cwd` на текущий рабочий каталог процесса, поэтому запускайте его из проекта, в котором есть каталог `.claude/skills/` в текущем каталоге или в любом родительском каталоге вплоть до корня репозитория:

```python Python theme={null}
import asyncio
import os

from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        cwd=os.getcwd(),  # .claude/skills/ here or in a parent directory
        setting_sources=["user", "project"],  # Load skills from filesystem
        skills="all",  # Let Claude invoke every discovered skill
        allowed_tools=["Read", "Write", "Bash"],
    )

    async for message in query(
        prompt="Help me process this PDF document", options=options
    ):
        print(message)


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Help me process this PDF document",
  options: {
    cwd: process.cwd(), // .claude/skills/ here or in a parent directory
    settingSources: ["user", "project"], // Load skills from filesystem
    skills: "all", // Let Claude invoke every discovered skill
    allowedTools: ["Read", "Write", "Bash"]
  }
})) {
  console.log(message);
}
```

### Подтверждение загрузки скиллов

В начале потока SDK выдаёт системное сообщение с подтипом `init`. Проверьте его массив `skills`, чтобы убедиться, что ваши скиллы загружены, прежде чем Claude начнёт работу. Массив включает скиллы, вызываемые пользователем, которые вы определили с полем frontmatter `description` или `when_to_use`, а также [встроенные скиллы, входящие в Claude Code](https://code.claude.com/docs/ru/skills.md#bundled-skills).

Массив содержит только скиллы, вызываемые пользователем. Скилл с [`user-invocable: false`](https://code.claude.com/docs/ru/skills#control-who-invokes-a-skill) в frontmatter загружается и остаётся доступным для Claude, но не появляется в массиве. Массив содержит одни и те же скиллы независимо от того, находятся ли они в вашем списке `skills`.

### Разрешение только определённых скиллов

Чтобы позволить Claude вызывать только определённые скиллы, передайте их имена в списке `skills`:

* **Ваши собственные скиллы**: имя каталога скилла
* **Скиллы плагинов**: `plugin:skill`
* **Конфликты имён в `additionalDirectories` или `add_dirs`**: скилл в одном из этих каталогов получает [имя с префиксом](https://code.claude.com/docs/ru/skills.md#how-a-skill-gets-its-command-name), если его имя конфликтует с корпоративным, личным или проектным скиллом либо со скиллом в каталоге, добавленном ранее. Указывайте его под этим именем. Если скилл `verify` есть в `../api` и `../web`, добавленных в таком порядке, и других скиллов `verify` нет, укажите их как `verify` и `web:verify`. Требуется Claude Code v2.1.309 или новее

Список принимает только точные имена скиллов. Если запись не может работать как точное имя, `query()` отклоняет список до начала сессии. См. [Ошибка неверного имени скилла](#invalid-skill-name-error), где описаны правила имён и ошибка, которую выдаёт каждый SDK.

Модель не видит неуказанные скиллы, и инструмент Skill их отклоняет, при этом их файлы остаются на диске и по-прежнему доступны через Read и Bash. Ограничение списка не ограничивает [отправку по имени](#dispatch-commands-by-name).

Чтобы позволить Claude вызывать каждый обнаруженный скилл, передайте `skills: "all"` вместо подстановочного знака.

## Команды в сеансах Agent SDK

Этот раздел — документация команд SDK. Команда — это всё, что вы запускаете, отправляя `/<name>` в подсказку. Записи на поверхности команд отличаются тем, что их поддерживает:

* **Встроенные команды**: выполняют логику, закодированную в процесс Claude Code, который запускает SDK, например `/compact`
* **Встроенные skills**: артефакты подсказок, включённые в Claude Code, например `/code-review`
* **Ваши skills**: артефакты подсказок, которые вы создаёте, каждый — каталог, содержащий файл `SKILL.md`. Имя skill, который можно вызывать пользователем, автоматически присоединяется к поверхности, поэтому отправка вашего собственного `/security-check` и запуск встроенного работают одинаково
* **Файлы пользовательских команд**: более старая форма артефакта с тем же поведением, плоские файлы Markdown в `.claude/commands/`, имена файлов которых становятся именами команд. Skills — их рекомендуемый преемник

По умолчанию как вы, так и Claude можете вызывать любой skill. Вы можете ограничить любой путь через [frontmatter](https://code.claude.com/docs/ru/skills.md#control-who-invokes-a-skill) skill. Для определений команды и skill см. записи глоссария [Команда](https://code.claude.com/docs/ru/glossary.md#command) и [Skill](https://code.claude.com/docs/ru/glossary.md#skill). См. [Команды в Claude Code](https://code.claude.com/docs/ru/commands.md) для каждой встроенной и [Расширьте Claude с помощью skills](https://code.claude.com/docs/ru/skills.md) для полного руководства по обеим формам артефактов.

### Обнаружение доступных команд

Вы можете отправлять команды, которые работают без интерактивного терминала, через SDK. Сообщение `system/init` содержит доступные в вашем сеансе в его поле `slash_commands`. Команды, которые требуют интерактивного терминала, такие как `/theme` и `/terminal-setup`, не появляются в списке. Получите доступ к полю при запуске вашего сеанса:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Hello Claude",
  options: { maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "init") {
    console.log("Available commands:", message.slash_commands);
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage


async def main():
    async for message in query(prompt="Hello Claude", options=ClaudeAgentOptions(max_turns=1)):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print("Available commands:", message.data["slash_commands"])


asyncio.run(main())
```

Выведенный список смешивает встроенные команды, встроенные skills, ваши skills, которые можно вызывать пользователем, и файлы `.claude/commands/`:

```text theme={null}
Available commands: ["clear", "compact", "context", "usage", "code-review", "verify", "security-check", ...]
```

Skill с [`user-invocable: false`](https://code.claude.com/docs/ru/skills#control-who-invokes-a-skill) в его frontmatter не появляется в этом списке или в массиве `skills` из [Подтверждение загрузки skills](#confirm-skills-loaded). Сеансы, которые настраивают [MCP серверы](https://code.claude.com/docs/ru/agent-sdk/mcp.md), также могут предоставлять [MCP подсказки как команды](https://code.claude.com/docs/ru/mcp.md#use-mcp-prompts-as-commands).

### Отправка команд по имени

Отправьте команду, включив её в строку подсказки, так же как вы отправляете обычный текст. Отправка не зависит от опции `skills`. Отправка `/<name>` запускает skill, который можно вызывать пользователем, даже когда ваш список `skills` его опускает. Команды, которые действуют на историю разговора, такие как `/compact`, требуют предыдущих сообщений для работы.

`/<name>`, который не совпадает ни с командой в сеансе, ни со встроенной командой Claude Code, не приводит к сбою запроса. Claude Code отправляет подсказку Claude как обычное сообщение с примечанием о том, что команда не была выполнена, поэтому запрос использует ход модели и возвращает ответ Claude. До версии 2.1.274 `/<name>`, который ничему не соответствовал, возвращал `Unknown command: /<name>` как результат без хода модели.

`/<name>`, который совпадает со встроенной командой Claude Code, которая недоступна в сеансе, такой как `/theme`, возвращает `/theme isn't available in this environment.` как результат без хода модели.

> [!NOTE]
>
> Когда команда достигает лимита `maxTurns` / `max_turns`, запрос завершается результатом ошибки вместо `success`. Описание контракта результата ошибки см. в разделе [Обработка результата](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md#handle-the-result). Если ваша команда может достичь лимита, сделайте одно из следующего:
>
> * Установите `maxTurns` достаточно высоким, чтобы работа успела завершиться.
> * Оберните цикл `query()` в `try`/`catch` в TypeScript или `try`/`except` в Python.

### Сжатие истории с помощью `/compact`

Команда `/compact` уменьшает размер истории вашего разговора путём суммирования старых сообщений при сохранении важного контекста. Сжатие требует существующего разговора с достаточным количеством предыдущих сообщений для суммирования. Этот пример сначала имеет разговор, затем сжимает его и читает системное сообщение `compact_boundary`, которое сообщает результат:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

// Compaction needs existing history, so have a conversation first
try {
  for await (const message of query({
    prompt: "Explain what this project does",
    options: { maxTurns: 2 }
  })) {
    if (message.type === "result" && message.subtype === "success") {
      console.log(message.result);
    }
  }
} catch (error) {
  // A single-shot query() throws after yielding an error result,
  // so the follow-up query below still runs.
  console.error(`Session ended with an error: ${error}`);
}

// Compact the same conversation
for await (const message of query({
  prompt: "/compact",
  options: { continue: true, maxTurns: 1 }
})) {
  if (message.type === "system" && message.subtype === "compact_boundary") {
    console.log("Compaction completed");
    console.log("Pre-compaction tokens:", message.compact_metadata.pre_tokens);
    console.log("Trigger:", message.compact_metadata.trigger);
    // Example output:
    // Compaction completed
    // Pre-compaction tokens: 1842
    // Trigger: manual
  }
}
```

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage


async def main():
    # Compaction needs existing history, so have a conversation first
    try:
        async for message in query(
            prompt="Explain what this project does",
            options=ClaudeAgentOptions(max_turns=2),
        ):
            if isinstance(message, ResultMessage) and message.subtype == "success":
                print(message.result)
    except Exception as error:
        # A single-shot query() raises after yielding an error result,
        # so the follow-up query below still runs.
        print(f"Session ended with an error: {error}")

    # Compact the same conversation
    async for message in query(
        prompt="/compact",
        options=ClaudeAgentOptions(continue_conversation=True, max_turns=1),
    ):
        if isinstance(message, SystemMessage) and message.subtype == "compact_boundary":
            print("Compaction completed")
            print("Pre-compaction tokens:", message.data["compact_metadata"]["pre_tokens"])
            print("Trigger:", message.data["compact_metadata"]["trigger"])
            # Example output:
            # Compaction completed
            # Pre-compaction tokens: 1842
            # Trigger: manual


asyncio.run(main())
```

> [!NOTE]
>
> Сообщение `compact_boundary` поступает только при выполнении сжатия. Если нечего суммировать, `/compact` сообщает причину вместо выдачи ошибки. Запуск всё ещё заканчивается результатом `success` и без сообщения `compact_boundary`, и текст результата содержит причину, например `Not enough messages to compact.` после одного короткого обмена. Свежий одноразовый вызов `query()` начинается с пустого контекста, поэтому используйте этот паттерн в сеансе с предыдущими ходами, например в [режиме потокового ввода](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md) или при возобновлении сеанса.

### Сброс контекста с помощью `/clear`

Команда `/clear` сбрасывает разговор в пустой контекст, поэтому последующие подсказки начинаются без предыдущей истории разговора. Предыдущий разговор остаётся на диске. Вы можете вернуться к этому разговору, передав его ID сеанса в [опцию `resume`](https://code.claude.com/docs/ru/agent-sdk/sessions#resume-by-id).

`/clear` полезна в [режиме потокового ввода](https://code.claude.com/docs/ru/agent-sdk/streaming-vs-single-mode.md), где вы отправляете несколько подсказок через одно соединение. Для одноразовых вызовов `query()` каждый вызов уже начинается с пустого контекста, поэтому отправка `/clear` не имеет практического эффекта. Вместо этого запустите новый `query()`.

## Создание skills

Создайте каждый skill как каталог, содержащий файл `SKILL.md` с YAML frontmatter и содержимым Markdown. Поле `description` определяет, когда Claude вызывает ваш skill.

**Пример структуры каталога**:

```text theme={null}
.claude/skills/security-check/
└── SKILL.md
```

### Выберите уровень обнаружения

Сохраняйте skills на одном из двух наиболее распространённых [уровней обнаружения](https://code.claude.com/docs/ru/skills.md#where-skills-live):

* **Project skills**: `.claude/skills/`, доступны только в текущем проекте
* **Personal skills**: `~/.claude/skills/`, доступны во всех ваших проектах

Если у вас есть существующие файлы пользовательских команд в `.claude/commands/`, они продолжают работать. Файл команды в `.claude/commands/deploy.md` создаёт `/deploy` и работает так же, как skill в `.claude/skills/deploy/SKILL.md`. Если файл команды и skill имеют одно имя, см. [Разрешение skills, которые имеют одно имя](https://code.claude.com/docs/ru/skills.md#resolve-skills-that-share-a-name) для того, какой из них запускается. SDK загружает файлы `.claude/commands/` и `~/.claude/commands/` из тех же двух областей, что и skills. См. [Расширьте Claude с помощью skills](https://code.claude.com/docs/ru/skills.md) для полного руководства по обеим формам артефактов.

### Создайте и отправьте ваш первый skill

Чтобы увидеть полный поток, создайте `.claude/skills/security-check/SKILL.md`:

```markdown theme={null}
---
name: security-check
description: Run a security vulnerability scan
---

Analyze the codebase for security vulnerabilities including:
- SQL injection risks
- XSS vulnerabilities
- Exposed credentials
- Insecure configurations
```

После создания файла skill доступен через SDK. Claude вызывает его, когда запрос соответствует его описанию, и вы можете отправить его напрямую:

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "/security-check",
  options: { maxTurns: 10 }
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
    async for message in query(
        prompt="/security-check", options=ClaudeAgentOptions(max_turns=10)
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

Успешный запуск заканчивается результатом `success`, текст которого содержит результаты сканирования. Для небольшого приложения Express с внедрёнными проблемами текст результата начинается:

```text theme={null}
**Security scan of `app.js` — 4 findings (most severe first):**

1. **SQL Injection** (line 8) — `req.query.name` is concatenated directly into the SQL string. Trivially exploitable (`' OR '1'='1`, `'; DROP TABLE users;--`). **Fix:** use parameterized queries, e.g. `db.query("SELECT * FROM users WHERE name = ?", [req.query.name], cb)`.
...
```

Имя skill также появляется в массиве `slash_commands` сообщения init.

> [!NOTE]
>
> Claude Code включает встроенные skills `code-review` и `verify`. Если вы назовёте файл `.claude/commands/` в честь одного из них, например `.claude/commands/code-review.md`, файл команды затеняет встроенный skill и `slash_commands` содержит имя один раз.

## Предварительное одобрение инструментов для skills

> [!NOTE]
>
> В сессиях SDK вы можете предварительно одобрить инструменты для project или personal skill с помощью поля frontmatter [`allowed-tools`](https://code.claude.com/docs/ru/skills#pre-approve-tools-for-a-skill) этого skill или с помощью опции `allowedTools` (`allowed_tools` в Python) в конфигурации вашего запроса. Если ваша организация задает [`allowManagedPermissionRulesOnly`](https://code.claude.com/docs/ru/settings-reference#allowmanagedpermissionrulesonly) в управляемых настройках, Claude Code игнорирует оба способа. Skills [синхронизированные из claude.ai](https://code.claude.com/docs/ru/skills.md#how-claude-code-handles-the-frontmatter-of-a-synced-skill) следуют своим собственным правилам frontmatter.

Skills запускаются с инструментами сессии. Пример ниже предварительно одобряет `Read`, `Grep` и `Glob` с `allowedTools` (`allowed_tools` в Python), поэтому Claude может проверять файлы при запуске [skill security-check](#create-and-dispatch-your-first-skill) без остановки для подтверждения:

```python Python theme={null}
import asyncio

from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Load skills from filesystem
    skills="all",
    allowed_tools=["Read", "Grep", "Glob"],
)


async def main():
    async for message in query(prompt="Check this project for security issues", options=options):
        print(message)


asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Check this project for security issues",
  options: {
    settingSources: ["user", "project"], // Load skills from filesystem
    skills: "all",
    allowedTools: ["Read", "Grep", "Glob"]
  }
})) {
  console.log(message);
}
```

В потоке вызов skill появляется как использование инструмента Skill, за которым следуют вызовы Read на файлы проекта. Запуск заканчивается результатом `success`, текст которого содержит результаты.

Список предварительно одобряет названные инструменты, а не ограничивает остальные. Для полного потока разрешений, включая режимы разрешений и обратный вызов `canUseTool`, см. [Разрешения](https://code.claude.com/docs/ru/agent-sdk/permissions.md).

## Troubleshooting

### Skills не найдены

**Проверьте конфигурацию settingSources**: SDK обнаруживает skills через источники параметров `user` и `project`. Если вы явно установите `settingSources`/`setting_sources` и опустите эти источники, SDK не загружает skills:

```python Python theme={null}
# Skills not loaded: setting_sources excludes user and project
options = ClaudeAgentOptions(setting_sources=[], skills="all")

# Skills loaded: user and project sources included
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],
    skills="all",
)
```

```typescript TypeScript theme={null}
// Skills not loaded: settingSources excludes user and project
const optionsWithoutSkills = {
  settingSources: [],
  skills: "all"
};

// Skills loaded: user and project sources included
const optionsWithSkills = {
  settingSources: ["user", "project"],
  skills: "all"
};
```

Для того, какие каталоги skills загружает каждый источник, см. [таблицу источников файловой системы](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md#control-filesystem-settings-with-settingsources). Для получения дополнительной информации о `settingSources`/`setting_sources` см. [справочник TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md#settingsource) или [справочник Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md#settingsource).

**Проверьте рабочий каталог**: SDK загружает skills из `.claude/skills/` в опции `cwd` и в каждом родительском каталоге вплоть до корня репозитория. Убедитесь, что `cwd` указывает на каталог, содержащий `.claude/skills/`, или ниже него в пределах одного репозитория:

```python Python theme={null}
# Ensure your cwd points to the directory containing .claude/skills/
options = ClaudeAgentOptions(
    cwd="/path/to/project",  # .claude/skills/ here or in a parent directory
    setting_sources=["user", "project"],  # Loads skills from these sources
    skills="all",
)
```

```typescript TypeScript theme={null}
// Ensure your cwd points to the directory containing .claude/skills/
const options = {
  cwd: "/path/to/project", // .claude/skills/ here or in a parent directory
  settingSources: ["user", "project"], // Loads skills from these sources
  skills: "all"
};
```

Полный паттерн см. в разделе [Использование skills с Agent SDK](#use-skills-with-the-agent-sdk).

**Проверьте расположение файловой системы**:

```bash theme={null}
# Check project skills
ls .claude/skills/*/SKILL.md

# Check personal skills
ls ~/.claude/skills/*/SKILL.md
```

### Skill не используется

**Проверьте опцию `skills`**: если вы передали список `skills`, подтвердите, что имя skill включено. Когда Claude пытается вызвать неуказанный skill, инструмент Skill возвращает `Skill <name> is not in this session's skills allowlist`. Добавьте имя в ваш список или отправьте skill напрямую, отправив `/<name>` в подсказку, что работает без указания.

**Проверьте описание**: убедитесь, что оно конкретно и включает соответствующие ключевые слова. См. [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions) для рекомендаций по написанию эффективных описаний.

### Ошибка неверного имени skill

Когда имя в вашем списке `skills` не может работать как точное имя skill, `query()` отклоняет список перед запуском процесса Claude Code. Имена, которые вызывают отклонение, включают:

* Пустое имя
* Имя, содержащее скобки, запятые или управляющие символы
* Имя, дополненное пробелом
* Форма подстановочного знака, такая как голый `*` или суффикс `:*`

Каждый SDK выводит отклонение по-разному:

> [tab] TypeScript
>
> TypeScript SDK выдаёт `Error`, указывающую правило, которое нарушила запись. Например, `skills: ["docs:*"]` выдаёт:
>
> ```text theme={null}
> Invalid skill name "docs:*": wildcard-suffix names are not allowed; list each skill by its exact name.
> ```
>
> Пустое имя сообщает `Skill names must be non-empty strings.`
>
> До TypeScript Agent SDK 0.3.221 SDK не выполнял эту проверку.

> [tab] Python
>
> Python SDK выдаёт `ValueError`, указывающую правило, которое нарушила запись. Например, `skills=["docs:*"]` выдаёт:
>
> ```text theme={null}
> ValueError: Invalid skill name 'docs:*': wildcard-suffix names are not allowed; list each skill by its exact name.
> ```
>
> Пустое имя сообщает `Skill names must be non-empty strings`.
>
> До Python Agent SDK 0.2.129 SDK не выполнял эту проверку.

### Дополнительное troubleshooting

Для общего troubleshooting skills, такого как ошибки синтаксиса YAML и отладка, см. [раздел troubleshooting Claude Code skills](https://code.claude.com/docs/ru/skills.md#troubleshooting).

## Следующие шаги

[Руководство Claude Code skills](https://code.claude.com/docs/ru/skills.md) охватывает разработку в глубину. Его рекомендации применяются к сеансам SDK. Начните с этих разделов:

* [Справочник Frontmatter](https://code.claude.com/docs/ru/skills.md#frontmatter-reference): каждое поддерживаемое поле
* [Передача аргументов в скиллы](https://code.claude.com/docs/ru/skills.md#pass-arguments-to-skills): `$ARGUMENTS`, `$0` и `$1`. [Полная таблица подстановок](https://code.claude.com/docs/ru/skills.md#available-string-substitutions) добавляет именованные аргументы и переменные `${CLAUDE_*}`
* [Внедрение динамического контекста](https://code.claude.com/docs/ru/skills.md#inject-dynamic-context): строки `` !`command` ``, которые запускаются перед тем, как Claude увидит содержимое skill
* [Выберите, где загружаются skills](https://code.claude.com/docs/ru/skills.md#where-skills-live): каждое расположение skill, пространство имён плагина и какой skill запускается, когда два имеют одно имя

## Связанные ресурсы

* [Команды в Claude Code](https://code.claude.com/docs/ru/commands.md): полная поверхность команд, включая каждую встроенную
* [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): концептуальный обзор, преимущества и архитектура
* [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): рекомендации по разработке для эффективных skills
* [Agent Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction): примеры skills и шаблоны
* [Subagents в SDK](https://code.claude.com/docs/ru/agent-sdk/subagents.md): похожие агенты на основе файловой системы с программными опциями
* [Обзор SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md): общие концепции SDK
* [Справочник TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md): полная документация API
* [Справочник Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md): полная документация API
