> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Доступность функций

> Сравните, какие функции Claude Code доступны в каждом плане подписки Anthropic, в Anthropic Console и у облачных поставщиков, таких как Amazon Bedrock и Google Cloud.

CLI Claude Code и всё, что работает локально, функционирует одинаково у каждого поставщика. Инструкции по настройке для каждого поставщика см. в разделе [Обзор развёртывания для предприятий](https://code.claude.com/docs/ru/third-party-integrations.md). Чтобы сразу перейти к тому, что отсутствует у вашего поставщика, см. вкладки [сводки по поставщикам](#summary-by-provider).

В таблицах ниже ✓ означает доступно, ✗ означает недоступно, а «See note» ссылается на сноску для частичной поддержки. Квалификатор после ✓ сужает доступность до этого подмножества, а «Admin-enabled» означает, что функция отключена до тех пор, пока администратор организации её не включит.

## Доступность по поставщику модели

Способ аутентификации определяет, какие функции может использовать Claude Code. Для единого списка того, что отсутствует у вашего поставщика, см. вкладки [сводки по поставщикам](#summary-by-provider). Чтобы найти свой столбец в таблицах:

* **Подписка Claude**: вы входите с учётной записью claude.ai в плане Pro, Max, Ultra, Team или Enterprise
* **Anthropic Console**: вы аутентифицируетесь с помощью ключа API Anthropic или [входите в учётную запись Console без ключа](https://code.claude.com/docs/ru/authentication.md#sign-in-without-an-api-key)
* **Amazon Bedrock**: вы используете модели Claude из каталога моделей Amazon Bedrock и устанавливаете `CLAUDE_CODE_USE_BEDROCK`. [Конечная точка Mantle](https://code.claude.com/docs/ru/amazon-bedrock.md#use-the-mantle-endpoint) (`CLAUDE_CODE_USE_MANTLE`) охватывается этим столбцом
* **Claude Platform на AWS**: вы приобрели Claude через AWS Marketplace, но вызываете API Anthropic и устанавливаете `CLAUDE_CODE_USE_ANTHROPIC_AWS`
* **Google Cloud (Anthropic managed)**: вы используете [Claude Models on Google Cloud (Anthropic managed)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md) и устанавливаете `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD`. Вы обращаетесь к Claude API, которым управляет Anthropic, через свой проект Google Cloud. Чтобы различить два предложения Google Cloud, см. [Каким предложением вы пользуетесь?](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview#which-offering-are-you-using)
* **Google Cloud (Google managed)**: управляется Google в рамках Google Cloud's Agent Platform, ранее Vertex AI; вы устанавливаете `CLAUDE_CODE_USE_VERTEX` и используете Claude Models on Google Cloud (Google managed)
* **Microsoft Foundry**: управляется Anthropic; вы устанавливаете `CLAUDE_CODE_USE_FOUNDRY`

### Функции, доступные у каждого поставщика

Они работают у каждого поставщика:

* [CLI](https://code.claude.com/docs/ru/quickstart.md) и [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md)
* Расширения [VS Code](https://code.claude.com/docs/ru/vs-code.md) и [JetBrains](https://code.claude.com/docs/ru/jetbrains.md)
* [Subagents](https://code.claude.com/docs/ru/sub-agents.md), [hooks](https://code.claude.com/docs/ru/hooks-guide.md), [commands](https://code.claude.com/docs/ru/commands.md) и [skills](https://code.claude.com/docs/ru/skills.md)
* [Память CLAUDE.md](https://code.claude.com/docs/ru/memory.md), [plugins](https://code.claude.com/docs/ru/plugins/overview.md) и [MCP servers](https://code.claude.com/docs/ru/mcp.md)
* [Checkpoints](https://code.claude.com/docs/ru/checkpointing.md), [sandboxing](https://code.claude.com/docs/ru/sandboxing.md) и [Workflows](https://code.claude.com/docs/ru/workflows.md)
* [Метрики OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md) и [управляемый файл параметров](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms)

Они имеют различия, зависящие от поставщика:

* **MCP-серверы**: [коннекторы из claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai) загружаются только когда ваша подписка claude.ai является активным методом аутентификации. [Поиск инструментов](https://code.claude.com/docs/ru/mcp.md#configure-tool-search) не поддерживается на [развёртываниях Microsoft Foundry, размещённых на Azure](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options). На Google Cloud (Google managed) поиск инструментов не поддерживается на моделях более ранних, чем Claude Opus 4.5, Claude Sonnet 4.5 и Claude Haiku 4.5
* **Субагенты**: когда родительский диалог работает на Fable, встроенный [субагент Explore](https://code.claude.com/docs/ru/sub-agents.md#built-in-subagents) работает на Opus при использовании подписки Claude, учётной записи Anthropic Console или [LLM-шлюза](https://code.claude.com/docs/ru/llm-gateway), доступ к которому осуществляется через `ANTHROPIC_BASE_URL`. У других провайдеров, включая Claude Platform on AWS, он работает на Fable
* **[Команды](https://code.claude.com/docs/ru/commands.md#all-commands)**:
  * `/design-sync` и `/import` с его формой подкоманды `claude import` недоступны у облачных поставщиков, а также через [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway#availability-and-limitations)
  * `/voice` требует учётную запись claude.ai
  * `/list-agents` и его псевдоним `/peers` доступны только в сессиях, где [включена передача сообщений между сессиями](https://code.claude.com/docs/ru/cross-session-messaging.md#availability)

### Функции, требующие подписку Claude

Они требуют входа с учётной записью claude.ai и недоступны с ключом API Anthropic Console или от поставщика третьей стороны:

* [Облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) и Claude Code на мобильном устройстве
* [Claude Code в Slack](https://code.claude.com/docs/ru/slack.md): планы Pro, Max и Ultra
* [Claude Code Desktop](https://code.claude.com/docs/ru/desktop.md)
* [Облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md) (`/schedule`)
* [Ultrareview](https://code.claude.com/docs/ru/ultrareview.md)
* [Code Review](https://code.claude.com/docs/ru/code-review.md): планы Team и Enterprise
* [Remote Control](https://code.claude.com/docs/ru/remote-control.md)
* [Расширение Chrome](https://code.claude.com/docs/ru/chrome.md)
* [Computer use](https://code.claude.com/docs/ru/computer-use.md): планы Pro, Max и Ultra
* [Артефакты](https://code.claude.com/docs/ru/artifacts.md): планы Pro, Max, Ultra, Team и Enterprise
* [Voice dictation](https://code.claude.com/docs/ru/voice-dictation.md)

Desktop — частичное исключение: [маршрутизация шлюза может быть настроена в приложении или администратором](https://code.claude.com/docs/ru/llm-gateway-connect.md#desktop-app). [Claude Desktop на 3P](https://claude.com/docs/third-party/claude-desktop/overview) также запускает вкладку Code на Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry или самостоятельно размещённом LLM-шлюзе. Он также запускает вкладку Code на [Claude API](https://claude.com/docs/third-party/claude-desktop/claude-api) с API-ключом Anthropic Console. Для доступности этих функций по плану см. [Доступность по плану подписки](#availability-by-subscription-plan).

### Возможности CLI, которые различаются по поставщикам

Эти функции работают в локальном CLI, но зависят от возможности на стороне сервера, которую не каждый поставщик предоставляет.

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Подписка Claude</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform на AWS</th>
      <th>Google Cloud (Anthropic managed)</th>
      <th>Google Cloud (Google managed)</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Web search](https://code.claude.com/docs/ru/tools-reference.md#websearch-tool-behavior)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>✓</td>
      <td>См. примечание <sup>[1](#fn1)</sup></td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[Быстрый режим](https://code.claude.com/docs/ru/fast-mode.md)</td>
      <td>✓ ([включено владельцем](https://code.claude.com/docs/ru/fast-mode.md#enable-fast-mode-for-your-organization) для Team и Enterprise)</td>
      <td>✓ (для Opus 5 и 4.8 требуется подготовленный доступ)</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✓ ([Fable 5.2, с условиями](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-on-agent-platform))</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Авторежим](https://code.claude.com/docs/ru/auto-mode-config.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>См. примечание <sup>[2](#fn2)</sup></td>
      <td>✓</td>
      <td>✓</td>
      <td>См. примечание <sup>[2](#fn2)</sup></td>
      <td>См. примечание <sup>[2](#fn2)</sup></td>
    </tr>

    <tr>
      <td>[Advisor](https://code.claude.com/docs/ru/advisor.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓ (Claude Code v2.1.300 или более поздней версии)</td>
      <td>✓ (Claude Code v2.1.300 или более поздней версии)</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Code Mode](https://code.claude.com/docs/ru/code-mode.md)</td>
      <td>✓ (экспериментально, [действуют требования](https://code.claude.com/docs/ru/code-mode.md#requirements))</td>
      <td>✓ (экспериментально, [действуют требования](https://code.claude.com/docs/ru/code-mode.md#requirements))</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md)</td>
      <td>✓ <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
      <td>✓ (одна машина) <sup>[5](#fn5)</sup></td>
    </tr>

    <tr>
      <td>[Каналы](https://code.claude.com/docs/ru/channels.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[GitHub Actions](https://code.claude.com/docs/ru/github-actions.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✓</td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
    </tr>
  </tbody>
</table>

### Администрирование и аналитика

Элементы управления на уровне организации и видимость использования.

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Подписка Claude</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform на AWS</th>
      <th>Google Cloud (Anthropic managed)</th>
      <th>Google Cloud (Google managed)</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Панель управления аналитики и API](https://code.claude.com/docs/ru/analytics.md)</td>
      <td>✓ (панель управления: Team и Enterprise; API: Enterprise)</td>
      <td>✓ <sup>[4](#fn4)</sup></td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md)</td>
      <td>✓ (Team и Enterprise)</td>
      <td>См. [Доступность платформы](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability)</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md)</td>
      <td>✓ (квалифицированные Enterprise аккаунты)</td>
      <td>✓ (квалифицированные аккаунты)</td>
      <td>См. примечание <sup>[3](#fn3)</sup></td>
      <td>✓ (квалифицированные аккаунты)</td>
      <td>✓ (по запросу)</td>
      <td>См. примечание <sup>[3](#fn3)</sup></td>
      <td>См. примечание <sup>[3](#fn3)</sup></td>
    </tr>
  </tbody>
</table>

<sup>1</sup> На Google Cloud (Google managed) веб-поиск доступен для Opus 4, Sonnet 4, Haiku 4.5 и более поздних моделей.\

<sup>2</sup> На этих поставщиках авторежим поддерживает только Claude Sonnet 5 или более поздние версии, Opus 4.7 или более поздние версии, Haiku 5.5 и модели Fable. См. [Конфигурация авторежима](https://code.claude.com/docs/ru/auto-mode-config.md). Для режима разрешений, в котором сессия начинается на этих поставщиках, см. [В каком режиме начинается сессия](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in).\

<sup>3</sup> В соответствии с вашим соглашением с поставщиком облачных услуг.\

<sup>4</sup> Только панель управления и API. [Contribution metrics](https://code.claude.com/docs/ru/analytics.md#enable-contribution-metrics) требует организацию claude.ai Team или Enterprise.\

<sup>5</sup> Требует Claude Code v2.1.224 или более поздней версии на macOS и Linux, включая Linux внутри WSL 2. На нативной Windows требует Claude Code v2.1.234 или более поздней версии. При аутентификации с помощью API-ключа передача сообщений доступна только на одной машине. На Amazon Bedrock, Claude Platform на AWS, Google Cloud (Anthropic managed), Google Cloud (Google managed) и Microsoft Foundry передача сообщений доступна только на одной машине и требует Claude Code v2.1.248 или более поздней версии. Claude может найти ваши [облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) и ваши сессии на других машинах только из сессии, подключённой к [Remote Control](https://code.claude.com/docs/ru/remote-control.md). Для подключения вам нужен вход в claude.ai и выполнение других [требований Remote Control](https://code.claude.com/docs/ru/remote-control.md#requirements). См. [Передача сообщений сессиям на других машинах](https://code.claude.com/docs/ru/cross-session-messaging.md#message-sessions-on-other-machines).

> [!NOTE]
>
> Если вы аутентифицируетесь через [LLM-шлюз](https://code.claude.com/docs/ru/llm-gateway), доступность функций соответствует базовому поставщику, на который шлюз перенаправляет запросы, за исключением функций, которые сам Claude Code отключает. Когда `ANTHROPIC_BASE_URL` указывает на хост, отличный от `api.anthropic.com`, Claude Code отключает такие функции, как [Remote Control](https://code.claude.com/docs/ru/remote-control.md#requirements) и [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability), независимо от того, куда перенаправляет шлюз. Некоторые функции, такие как [Advisor](https://code.claude.com/docs/ru/advisor.md#requirements), работают, только если шлюз перенаправляет запросы без изменений.
>
> Для информации о том, как запросы, которые отправляет Claude Code, различаются между шлюзом в формате Amazon Bedrock или Agent Platform, шлюзом `ANTHROPIC_BASE_URL` и входом в Claude apps gateway, см. [поведение клиента по методу подключения](https://code.claude.com/docs/ru/llm-gateway-protocol.md#how-the-connection-method-changes-client-behavior).

### Сводка по поставщикам

Каждая вкладка содержит список того, что недоступно или частично поддерживается у этого поставщика, с альтернативами, где они существуют. См. также [различия, зависящие от поставщика](#features-available-on-every-provider). На Amazon Bedrock, Google Cloud (Google managed), Microsoft Foundry и Claude Platform на AWS отчёты об ошибках и телеметрия для Anthropic отключены по умолчанию. См. [поведение по умолчанию по поставщику API](https://code.claude.com/docs/ru/data-usage.md#default-behaviors-by-api-provider) для информации о том, какой трафик всё ещё достигает Anthropic и как отказаться.

> [tab] Amazon Bedrock
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription), плюс [веб-поиск](https://code.claude.com/docs/ru/tools-reference.md#websearch-tool-behavior), [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md), [Advisor](https://code.claude.com/docs/ru/advisor.md), [Каналы](https://code.claude.com/docs/ru/channels.md), [Code Mode](https://code.claude.com/docs/ru/code-mode.md), [панель управления аналитики](https://code.claude.com/docs/ru/analytics.md), [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) и [команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands).
>
> **Частичная поддержка:**
>
> * [Desktop](https://code.claude.com/docs/ru/desktop.md): только через [Claude Desktop на 3P](https://claude.com/docs/third-party/claude-desktop/overview)
> * [Авторежим](https://code.claude.com/docs/ru/auto-mode-config.md): только Sonnet 5 или более поздние версии, Opus 4.7 или более поздние версии, Haiku 5.5 и модели Fable
> * [Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md): между вашими сеансами на этой машине только <sup>[5](#fn5)</sup>
> * [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md): в соответствии с вашим соглашением AWS
>
> **Альтернативы:** для планирования используйте [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) вместо `/schedule`. Для облачных сеансов используйте [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) или [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md). Для веб-поиска используйте инструмент [WebFetch](https://code.claude.com/docs/ru/tools-reference.md#webfetch-tool-behavior) с конкретным URL.

> [tab] Claude Platform на AWS
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription), плюс [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md), [Каналы](https://code.claude.com/docs/ru/channels.md), [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md), [Code Mode](https://code.claude.com/docs/ru/code-mode.md), [панель управления аналитики](https://code.claude.com/docs/ru/analytics.md), [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) и [команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands).
>
> **Доступно здесь, но не на Amazon Bedrock:** [веб-поиск](https://code.claude.com/docs/ru/tools-reference.md#websearch-tool-behavior), а также [Advisor](https://code.claude.com/docs/ru/advisor.md) в Claude Code v2.1.300 или более поздней версии.
>
> **Частичная поддержка:**
>
> * [Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md): между вашими сеансами на этой машине только <sup>[5](#fn5)</sup>
>
> **Альтернативы:** для планирования используйте [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) вместо `/schedule`. Для облачных сеансов используйте [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md).

> [tab] Google Cloud (Anthropic managed)
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription), плюс [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md), [Каналы](https://code.claude.com/docs/ru/channels.md), [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md), [Code Mode](https://code.claude.com/docs/ru/code-mode.md), [панель управления аналитики](https://code.claude.com/docs/ru/analytics.md), [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) и [команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands).
>
> **Доступно здесь, но не на Google Cloud (Google managed):** [Advisor](https://code.claude.com/docs/ru/advisor.md) в Claude Code v2.1.300 или более поздней версии.
>
> **Частичная поддержка:**
>
> * [Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md): только между вашими сессиями на этой машине <sup>[5](#fn5)</sup>
> * [Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#data-retention): доступно по запросу. Обратитесь к представителю Anthropic, ведущему вашу учётную запись
>
> **Альтернативы:** для планирования используйте [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) вместо `/schedule`.

> [tab] Google Cloud (Google managed)
>
> Если вы устанавливаете `CLAUDE_CODE_USE_VERTEX`, чтобы использовать Claude Code с Google Cloud's Agent Platform, вы используете этого поставщика.
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription), плюс [Advisor](https://code.claude.com/docs/ru/advisor.md), [Каналы](https://code.claude.com/docs/ru/channels.md), [Code Mode](https://code.claude.com/docs/ru/code-mode.md), [панель управления аналитики](https://code.claude.com/docs/ru/analytics.md), [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) и [команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands).
>
> **Частичная поддержка:**
>
> * [Desktop](https://code.claude.com/docs/ru/desktop.md): через [управляемые параметры](https://claude.com/docs/third-party/claude-desktop/configuration) или [Claude Desktop на 3P](https://claude.com/docs/third-party/claude-desktop/overview)
> * [Веб-поиск](https://code.claude.com/docs/ru/tools-reference.md#websearch-tool-behavior): Opus 4, Sonnet 4, Haiku 4.5 и более поздние модели
> * [Быстрый режим](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-on-agent-platform): Fable 5.2 в регионах `global`, `us` и `eu` или стандартная скорость, если Agent Platform отклоняет быстрый режим
> * [Авторежим](https://code.claude.com/docs/ru/auto-mode-config.md): только Sonnet 5 или более поздние версии, Opus 4.7 или более поздние версии, Haiku 5.5 и модели Fable
> * [Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md): между вашими сеансами на этой машине только <sup>[5](#fn5)</sup>
> * [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md): в соответствии с вашим соглашением Google Cloud
>
> **Альтернативы:** для планирования используйте [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) вместо `/schedule`. Для облачных сеансов используйте [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) или [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md).

> [tab] Microsoft Foundry
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription), плюс [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md), [Advisor](https://code.claude.com/docs/ru/advisor.md), [Каналы](https://code.claude.com/docs/ru/channels.md), [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md), [Code Mode](https://code.claude.com/docs/ru/code-mode.md), [панель управления аналитики](https://code.claude.com/docs/ru/analytics.md), [server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) и [команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands).
>
> **Частичная поддержка:**
>
> * [Desktop](https://code.claude.com/docs/ru/desktop.md): только через [Claude Desktop на 3P](https://claude.com/docs/third-party/claude-desktop/overview)
> * [Авторежим](https://code.claude.com/docs/ru/auto-mode-config.md): только Sonnet 5 или более поздние версии, Opus 4.7 или более поздние версии, Haiku 5.5 и модели Fable
> * [Cross-session messaging](https://code.claude.com/docs/ru/cross-session-messaging.md): между вашими сеансами на этой машине только <sup>[5](#fn5)</sup>
> * [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md): в соответствии с вашим соглашением Azure
>
> **Альтернативы:** для планирования используйте [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) вместо `/schedule`. Для облачных сеансов используйте [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md).

> [tab] Anthropic Console
>
> **Недоступно:** все [функции, требующие подписку Claude](#features-that-require-a-claude-subscription).
>
> Всё в разделе [Возможности CLI, которые различаются по поставщикам](#cli-capabilities-that-vary-by-provider) доступно, за исключением того, что [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) с Claude Opus 5 или Claude Opus 4.8 требует [подготовленный доступ](https://code.claude.com/docs/ru/fast-mode.md#enable-fast-mode-for-your-organization). [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md), которые вы настраиваете в организации claude.ai Team или Enterprise, не применяются к сессии, которая аутентифицируется с помощью API-ключа Console. См. [Доступность платформы](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability), чтобы узнать, как охватить такие сессии.
>
> **Частичная поддержка:**
>
> * [Desktop](https://code.claude.com/docs/ru/desktop.md): через [Claude Desktop на 3P с Claude API](https://claude.com/docs/third-party/claude-desktop/claude-api)

## Доступность по плану подписки

Если вы аутентифицируетесь через облачного провайдера или API-ключ Anthropic Console, этот раздел к вам не применяется. Когда вы входите с учётной записью claude.ai, ваш план определяет, какие из приведённых ниже функций доступны.

В организациях Enterprise с применённой [конфигурацией HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md) некоторые функции из этой таблицы отключены.

| Функция | Pro | Max | Ultra | Team | Enterprise |
| :- | :- | :- | :- | :- | :- |
| [Cloud sessions](https://code.claude.com/docs/ru/claude-code-on-the-web.md) | ✓ | ✓ | ✓ | ✓ | ✓ <sup>[6](#fn6)</sup> |
| [Облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md) | ✓ | ✓ | ✓ | ✓ | ✓ |
| [Remote Control](https://code.claude.com/docs/ru/remote-control.md) | ✓ | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Channels](https://code.claude.com/docs/ru/channels.md) | ✓ | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Computer use](https://code.claude.com/docs/ru/computer-use.md) | ✓ | ✓ | ✓ | ✗ | ✗ |
| Dispatch ([Desktop](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch)) | ✓ | ✓ | ✓ | ✗ | ✗ |
| [Code Review](https://code.claude.com/docs/ru/code-review.md) | ✗ | ✗ | ✗ | ✓ | ✓ |
| [Artifacts](https://code.claude.com/docs/ru/artifacts.md) | ✓ | ✓ | ✓ | ✓ | ✓ |
| [Analytics dashboard and contribution metrics](https://code.claude.com/docs/ru/analytics.md) | ✗ | ✗ | ✗ | ✓ | ✓ |
| [Enterprise Analytics API](https://code.claude.com/docs/ru/analytics.md#access-data-programmatically) | ✗ | ✗ | ✗ | ✗ | ✓ |
| [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md) | ✗ | ✗ | ✗ | ✓ | ✓ |
| [SSO](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) | ✗ | ✗ | ✗ | ✓ | ✓ |
| SCIM | ✗ | ✗ | ✗ | ✗ | ✓ |
| [Compliance API](https://platform.claude.com/docs/en/api/compliance) | ✗ | ✗ | ✗ | ✗ | ✓ |
| [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md) | ✗ | ✗ | ✗ | ✗ | ✓ <sup>[7](#fn7)</sup> |

<sup>6</sup> На Enterprise требуется премиум-место или место Chat + Claude Code. См. [Cloud sessions](https://code.claude.com/docs/ru/claude-code-on-the-web.md).\

<sup>7</sup> Не включено в стандартный план Enterprise. Требует отдельного включения Anthropic для квалифицированных аккаунтов. См. [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md).

Для информации о ценах и полного сравнения планов см. [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) и [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

### План Ultra

Ultra — это новое название плана Max 20x, а Max — новое название Max 5x. Чтобы узнать, какой у вас план, проверьте свою подписку на claude.ai.

В Claude Code планы Max и Ultra имеют одинаковые функции, указанные в столбцах Max и Ultra [таблицы доступности](#availability-by-subscription-plan). Информацию о лимитах использования и ценах см. на [странице цен Claude](https://claude.com/pricing).

## Доступность моделей

Для информации о том, какие модели Claude и размеры контекстного окна доступны для каждого поставщика и региона, см. [Model configuration](https://code.claude.com/docs/ru/model-config.md) и [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Vision, PDF input и extended thinking — это возможности модели, а не функции Claude Code, и работают у каждого поставщика, который предлагает модель. [Prompt caching](https://code.claude.com/docs/ru/prompt-caching.md) работает одинаково у большинства поставщиков; на Amazon Bedrock поддержка варьируется в зависимости от модели.

## Связанные ресурсы

* [Обзор развёртывания для предприятий](https://code.claude.com/docs/ru/third-party-integrations.md): сравните аутентификацию, выставление счётов и регионы у поставщиков
* Руководства по настройке поставщиков: [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Claude Platform на AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md), [Claude Models в Google Cloud (под управлением Anthropic)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md), [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md)
* [Platforms and integrations](https://code.claude.com/docs/ru/platforms.md): где работает Claude Code, включая CLI, Desktop, расширения IDE, веб, мобильные устройства и CI/CD
