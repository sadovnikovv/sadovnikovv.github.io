> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор Agent SDK

> Создавайте производственные AI-агентов с Claude Code как библиотеку

Агент — это приложение, которое выполняет задачу, планируя собственные шаги и вызывая инструменты, которые читают файлы, запускают команды или редактируют код. Agent SDK предоставляет вам те же инструменты, [цикл агента](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md) и управление контекстом, которые питают Claude Code, программируемые на Python и TypeScript.

## Сравнение Agent SDK с другими инструментами Claude

Agent SDK, CLI, Client SDK и Managed Agents отличаются тем, кто запускает агента, что входит в комплект и как вы его используете. Найдите строку, которая соответствует тому, как вы хотите создавать и запускать свой агент.

| Что вы хотите | Используйте | Что вы получаете |
| - | - | - |
| Встроить агента Claude Code в собственное приложение Python или TypeScript, в процессе, который вы контролируете | **Agent SDK** | Библиотека, которая запускает бинарный файл Claude Code, с [возможностями](#capabilities) Claude Code, такими как встроенные инструменты, разрешения, сессии и hooks. |
| Выполнять интерактивную разработку или запускать одноразовые задачи из терминала | [**Claude Code CLI**](https://code.claude.com/docs/ru/overview.md) | Интерфейс терминала, созданный для ежедневного интерактивного использования. |
| Вызывать Claude API непосредственно из собственного кода | [**Client SDK**](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) | Прямой доступ к Claude API из любого из языков Client SDK. Вы сами пишете цикл инструментов или позволяете бета-версии [tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) Client SDK управлять им. |
| Разместить агента в Anthropic, настроенного через Claude API | [**Managed Agents**](https://platform.claude.com/docs/en/managed-agents/overview) | Размещённая оболочка агента, которая запускает цикл агента, с сессиями в управляемой Anthropic облачной песочнице или [самостоятельно размещённой песочнице](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) на вашей собственной инфраструктуре. Используйте её из [SDK для вашего языка](https://platform.claude.com/docs/en/managed-agents/quickstart#install-the-sdk), CLI `ant` или REST API. |

Чтобы запустить тот же цикл агента из языка, отличного от Python или TypeScript, [запустите CLI как подпроцесс](https://code.claude.com/docs/ru/headless.md) с флагом `-p` и `--output-format json`.

## Возможности

Эти возможности Claude Code доступны в SDK:

| Возможность | Что она делает | Узнайте больше |
| - | - | - |
| Встроенные инструменты | Читать, писать, редактировать файлы, запускать команды и искать в веб-сети | [Справочник инструментов](https://code.claude.com/docs/ru/tools-reference.md) |
| Hooks | Запускать пользовательский код в ключевых точках жизненного цикла агента | [Hooks](https://code.claude.com/docs/ru/agent-sdk/hooks.md) |
| Subagents | Создавать специализированных агентов для сосредоточенных подзадач | [Subagents](https://code.claude.com/docs/ru/agent-sdk/subagents.md) |
| MCP | Подключать внешние инструменты и источники данных через Model Context Protocol | [MCP](https://code.claude.com/docs/ru/agent-sdk/mcp.md) |
| Permissions | Контролировать, какие инструменты запускаются автоматически, какие требуют одобрения | [Permissions](https://code.claude.com/docs/ru/agent-sdk/permissions.md) |
| Sessions | Сохранять контекст между обменами, возобновлять или разветвлять позже | [Sessions](https://code.claude.com/docs/ru/agent-sdk/sessions.md) |
| Skills, commands, и memory | Загружать автоматически из `.claude/` вашего проекта и из `~/.claude/`, как в Claude Code | [Skills](https://code.claude.com/docs/ru/agent-sdk/skills.md), [Commands](https://code.claude.com/docs/ru/agent-sdk/skills.md#commands-in-agent-sdk-sessions), [Memory](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md), [Загрузка конфигурации](https://code.claude.com/docs/ru/agent-sdk/claude-code-features.md) |
| Plugins | Упаковывать skills, агентов, hooks и MCP серверы, и загружать их по локальному пути | [Plugins](https://code.claude.com/docs/ru/agent-sdk/plugins.md) |

## Начало работы

Следуйте [Quickstart](https://code.claude.com/docs/ru/agent-sdk/quickstart.md), чтобы установить SDK, установить ваш API ключ и создать вашего первого агента, который находит и исправляет ошибки в существующем коде.

> [!NOTE]
>
> Если не было предварительного одобрения, Anthropic не разрешает сторонним разработчикам предлагать вход через claude.ai или ограничения скорости для своих продуктов, включая агентов, созданных на основе Claude Agent SDK. Вместо этого используйте методы аутентификации по API ключу, описанные в [Quickstart](https://code.claude.com/docs/ru/agent-sdk/quickstart.md).

## Журнал изменений

Просмотрите полный журнал изменений для обновлений SDK, исправлений ошибок и новых функций:

* **TypeScript SDK**: [просмотреть CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
* **Python SDK**: [просмотреть CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

## Сообщение об ошибках

Если вы столкнулись с ошибками или проблемами с Agent SDK:

* **TypeScript SDK**: [сообщить об ошибках на GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
* **Python SDK**: [сообщить об ошибках на GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

## Рекомендации по брендингу

Для партнеров, интегрирующих Claude Agent SDK, использование брендинга Claude является необязательным. При ссылке на Claude в вашем продукте:

**Разрешено:**

* "Claude Agent", предпочтительно для раскрывающихся меню
* "Claude", когда находится в меню, уже помеченном как "Agents"
* "\{YourAgentName} Powered by Claude", если у вас есть существующее имя агента

**Не разрешено:**

* "Claude Code" или "Claude Code Agent"
* ASCII-арт с брендингом Claude Code или визуальные элементы, которые имитируют Claude Code

Ваш продукт должен сохранять свой собственный брендинг и не должен выглядеть как Claude Code или любой продукт Anthropic. Для вопросов о соответствии брендингу свяжитесь с командой Anthropic [sales team](https://www.anthropic.com/contact-sales).

## Лицензия и условия

Использование Claude Agent SDK регулируется [Коммерческими условиями обслуживания Anthropic](https://www.anthropic.com/legal/commercial-terms), включая случаи, когда вы используете его для питания продуктов и услуг, которые вы предоставляете своим собственным клиентам и конечным пользователям, за исключением случаев, когда конкретный компонент или зависимость покрыты другой лицензией, как указано в файле LICENSE этого компонента.

## Следующие шаги

Эти ресурсы содержат более глубокие технические детали и примеры проектов для разработки с помощью Agent SDK.

* [Быстрый старт](https://code.claude.com/docs/ru/agent-sdk/quickstart.md): создайте своего первого агента, который находит и исправляет ошибки
* [Руководство по миграции](https://code.claude.com/docs/ru/agent-sdk/migration-guide.md): перейдите с пакетов Claude Code SDK на Agent SDK
* [Цикл агента](https://code.claude.com/docs/ru/agent-sdk/agent-loop.md): как Claude планирует, вызывает инструменты и решает, когда задача завершена
* [Примеры агентов](https://github.com/anthropics/claude-agent-sdk-demos): демонстрационные приложения для локальной разработки
* [TypeScript SDK](https://code.claude.com/docs/ru/agent-sdk/typescript.md): полная справка API TypeScript и примеры
* [Python SDK](https://code.claude.com/docs/ru/agent-sdk/python.md): полная справка API Python и примеры
* [Дизайн агентского каркаса](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code): как команда Claude Code использует динамические рабочие процессы для одновременной организации множества подагентов
