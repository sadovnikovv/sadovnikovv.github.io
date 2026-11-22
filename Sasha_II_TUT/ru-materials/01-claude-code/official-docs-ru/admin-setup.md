> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка Claude Code для вашей организации

> Карта решений для администраторов, развертывающих Claude Code, охватывающая поставщиков API, управляемые параметры, принудительное применение политики, мониторинг использования и обработку данных.

Claude Code обеспечивает соблюдение политики организации через управляемые параметры, которые имеют приоритет над локальной конфигурацией разработчика. Вы доставляете эти параметры из консоли администратора Claude, вашей системы управления мобильными устройствами (MDM) или файла на диске. Параметры контролируют, какие инструменты, команды, серверы и сетевые назначения может достичь Claude.

На этой странице рассматриваются решения по развертыванию по порядку. Каждая строка ссылается на раздел ниже и на справочную страницу для этой области.

> [!NOTE]
>
> SSO, подготовка SCIM и назначение мест настраиваются на уровне учетной записи Claude. См. [Руководство администратора Claude Enterprise](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide) и [назначение мест](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan) для этих шагов.

| Решение | Что вы выбираете | Справка |
| :- | :- | :- |
| [Выберите поставщика API](#choose-your-api-provider) | Где Claude Code аутентифицируется и как это выставляется счетом | [Authentication](https://code.claude.com/docs/ru/authentication.md), [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md), [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md) |
| [Решите, как параметры достигают устройств](#decide-how-settings-reach-devices) | Как управляемая политика достигает машин разработчиков | [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md), [Delivery mechanisms](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms) |
| [Решите, что принудительно применять](#decide-what-to-enforce) | Какие инструменты, команды и интеграции разрешены | [Permissions](https://code.claude.com/docs/ru/permissions.md), [Sandboxing](https://code.claude.com/docs/ru/sandboxing.md) |
| [Настройте видимость использования](#set-up-usage-visibility) | Как вы отслеживаете расходы и внедрение | [Analytics](https://code.claude.com/docs/ru/analytics.md), [Monitoring](https://code.claude.com/docs/ru/monitoring-usage.md), [Costs](https://code.claude.com/docs/ru/costs.md) |
| [Проверьте обработку данных](#review-data-handling) | Хранение данных и статус соответствия | [Data usage](https://code.claude.com/docs/ru/data-usage.md), [Security](https://code.claude.com/docs/ru/security.md) |

## Выберите поставщика API

Claude Code подключается к Claude через одного из нескольких поставщиков API. Ваш выбор влияет на выставление счетов, аутентификацию, какой статус соответствия вы наследуете и какие функции Claude Code доступны вашим разработчикам.

| Поставщик | Выберите это, когда |
| :- | :- |
| Claude for Teams / Enterprise | Вы хотите Claude Code и claude.ai в одной подписке на одного пользователя без инфраструктуры для запуска. Это рекомендация по умолчанию. |
| Claude Console | Вы ориентированы на API или хотите выставление счетов по мере использования |
| Amazon Bedrock | Вы хотите наследовать существующие элементы управления соответствием AWS и выставление счетов |
| Google Cloud's Agent Platform | Вы хотите наследовать существующие элементы управления соответствием GCP и выставление счетов |
| Microsoft Foundry | Вы хотите наследовать существующие элементы управления соответствием Azure и выставление счетов |

Некоторые функции Claude Code требуют учётной записи claude.ai. [Облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md), [облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md), [Code Review](https://code.claude.com/docs/ru/code-review.md), [Remote Control](https://code.claude.com/docs/ru/remote-control.md) и [расширение Chrome](https://code.claude.com/docs/ru/chrome.md) недоступны только через API-ключи Console или учётные данные поставщика облачных услуг. Если вы развёртываете через Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry, спланируйте, нужны ли разработчикам также места Claude for Teams или Enterprise. На каждой странице функции указаны требования к плану.

Для полного сравнения поставщиков, охватывающего аутентификацию, регионы и паритет функций, см. [обзор развертывания предприятия](https://code.claude.com/docs/ru/third-party-integrations.md). Настройка аутентификации каждого поставщика находится в [Authentication](https://code.claude.com/docs/ru/authentication.md).

Требования прокси и брандмауэра в [Network configuration](https://code.claude.com/docs/ru/network-config.md) применяются независимо от поставщика. Если вы хотите единую конечную точку перед несколькими поставщиками или централизованное логирование запросов, см. [LLM gateway](https://code.claude.com/docs/ru/llm-gateway).

## Решите, как настройки достигают устройств

Управляемые настройки определяют политику организации. Claude Code проверяет четыре источника в таблице ниже в порядке приоритета. [Как Claude Code объединяет управляемые источники](https://code.claude.com/docs/ru/managed-settings.md#precedence-within-the-managed-tier) указывает, какие из них применяются, что изменяет помощник политики и как составить каждый источник. Таблица — это карта решений.

| Механизм | Доставка | Приоритет | Платформы |
| :- | :- | :- | :- |
| Server-managed | Консоль администратора claude.ai или самостоятельно размещённый [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway) для входов через шлюз | Наивысший | Все |
| plist / registry policy | macOS: `com.anthropic.claudecode` plist Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` | Высокий | macOS, Windows |
| File-based managed | macOS: `/Library/Application Support/ClaudeCode/managed-settings.json` Linux и WSL: `/etc/claude-code/managed-settings.json` Windows: `C:\Program Files\ClaudeCode\managed-settings.json` | Средний | Все |
| Windows user registry | `HKCU\SOFTWARE\Policies\ClaudeCode` | Наименьший | Только Windows |

Claude Code получает настройки, управляемые сервером, при запуске и обновляет их каждый час во время сессии, без необходимости развёртывания инфраструктуры эндпоинтов. Доставка через консоль администратора claude.ai требует плана Claude for Teams или Enterprise. Развёртывания на Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry могут получить ту же удалённую доставку, запустив [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway), или вместо этого использовать один из механизмов на основе файлов или уровня ОС.

Если ваша организация использует несколько поставщиков, настройте [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md), для пользователей claude.ai плюс [резервный вариант на основе файлов или plist/registry](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms), чтобы другие пользователи по-прежнему получали управляемую политику.

Расположения plist и HKLM registry работают с любым поставщиком и устойчивы к несанкционированному изменению, потому что требуют привилегий администратора для записи. Реестр пользователя Windows в HKCU доступен для записи без повышения прав, поэтому рассматривайте его как удобный вариант по умолчанию, а не как канал принудительного применения.

По умолчанию WSL читает только путь Linux в `/etc/claude-code`. Чтобы распространить вашу политику реестра Windows и `C:\Program Files\ClaudeCode` на WSL на той же машине, задайте [`wslInheritsWindowsSettings: true`](https://code.claude.com/docs/ru/settings-reference#wslinheritswindowssettings) в одном из этих источников Windows, доступных только администратору.

Какой бы механизм вы ни выбрали, управляемые значения имеют приоритет над настройками пользователя и проекта, за исключением нескольких чувствительных к безопасности [исключений](https://code.claude.com/docs/ru/settings.md#exceptions-to-managed-settings-precedence). Настройки-массивы, такие как `permissions.allow` и `permissions.deny`, объединяют записи из [настроек с более низким приоритетом](https://code.claude.com/docs/ru/settings.md#lists-merge-instead-of-overriding) с [применяемыми управляемыми настройками](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources), поэтому разработчики могут расширять управляемые списки, но не удалять из них. Для `fallbackModel`, `availableModels` и [`modelPicker`](https://code.claude.com/docs/ru/settings-reference#modelpicker) управляемое значение заменяет нижние слои, а не объединяется с ними.

### Сессии WSL в Claude Code Desktop

В Windows [Claude Code Desktop может запускать сессии Code внутри дистрибутива WSL 2](https://code.claude.com/docs/ru/desktop-wsl.md). Процесс Claude Code сессии работает внутри дистрибутива, поэтому он определяет управляемые настройки через описанный выше путь обнаружения WSL: источники, доступные только в Windows, не достигают его, если не развёрнут `wslInheritsWindowsSettings: true`.

Claude Desktop по умолчанию отключает сессии WSL на устройствах, которые он определяет как управляемые организацией, например когда существует `C:\Program Files\ClaudeCode\managed-settings.json`. Чтобы включить их, разверните политику реестра Windows, для которой требуется Claude Desktop v1.19367.0 или более поздняя версия:

* Создайте значение с именем `disableWslSessions` в `HKLM\SOFTWARE\Policies\Claude` и задайте для него строку `REG_SZ` `false` или `REG_DWORD` `0`. Это значение находится под ключом политики Claude Desktop, отдельно от ключа `ClaudeCode`, который содержит управляемые настройки. Разверните значение в HKLM, что требует привилегий администратора для записи. Значение в HKCU не включает сессии WSL.
* Оставьте `C:\Program Files\ClaudeCode\managed-settings.json` на месте, если вы его развёртываете. После того как `disableWslSessions` имеет значение `false` в HKLM, Desktop разрешает сессии WSL, даже если этот файл присутствует.

Desktop читает политику каждый раз, когда начинается сессия WSL, поэтому вам не нужно перезапускать приложение после её развёртывания.

Если устройство по-прежнему отказывает в сессиях WSL, откройте **Help > Troubleshooting > Show Logs in File Explorer** в Claude Desktop на этом устройстве — это сохранит копию папки логов в Downloads. Найдите `[wslPolicyGate] denying WSL session` в `main.log` в этой копии. Причина отказа указана в скобках, например `(cli-file-present)`.

После включения сессий WSL распространите на них управляемые настройки:

* Разверните `wslInheritsWindowsSettings: true` через реестр HKLM или файл `C:\Program Files\ClaudeCode`, чтобы сессии WSL наследовали ту же политику, что и сессии хоста.
* Проверьте, запустив `/status` внутри сессии WSL и прочитав строку `Setting sources`. Чтобы интерпретировать то, что она перечисляет, см. [Прочитайте источник в /status](https://code.claude.com/docs/ru/managed-settings.md#read-the-source-in-/status).

Если сессия WSL запускается на устройстве со списком [`allowedWorkspaceFolders`](https://claude.com/docs/third-party/claude-desktop/configuration#allowedworkspacefolders) в Claude Desktop, запись `~` означает домашний каталог внутри дистрибутива.

Процессы внутри служебной виртуальной машины WSL 2 не видны датчикам обнаружения угроз на эндпоинтах на стороне Windows. Чтобы наблюдать активность процессов и файлов внутри дистрибутива, обратитесь к руководству по WSL от вашего поставщика средств обнаружения угроз на эндпоинтах, чтобы найти датчик Linux, который можно запустить внутри дистрибутива, и необходимые ему исключения. [Телеметрия выполнения инструментов OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md) Claude Code передаётся одинаково для сессий WSL и нативных сессий.

## Решите, что нужно применять

Управляемые параметры могут заблокировать инструменты, изолировать выполнение в песочнице, ограничить серверы MCP и источники плагинов, а также контролировать, какие hooks выполняются. Каждая строка — это поверхность управления с ключами параметров, которые её контролируют.

| Управление | Что это делает | Ключевые параметры |
| :- | :- | :- |
| [Правила разрешений](https://code.claude.com/docs/ru/permissions.md) | Разрешить, запросить или запретить определённые инструменты и команды | `permissions.allow`, `permissions.deny` |
| [Блокировка разрешений](https://code.claude.com/docs/ru/permissions.md#managed-only-settings) | Сделать управляемые параметры [единственным источником правил разрешений](https://code.claude.com/docs/ru/settings-reference.md#allowmanagedpermissionrulesonly). Отключить `--dangerously-skip-permissions` | `allowManagedPermissionRulesOnly`, `permissions.disableBypassPermissionsMode` |
| [Начальный режим разрешений](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in) | Выберите режим разрешений, в котором начинаются сеансы терминала ваших разработчиков, вместо встроенного начального режима разрешений, или удалите режим авто. [Переключение режимов разрешений](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes) указывает, когда расширение VS Code читает `defaultMode`, который вы устанавливаете | `permissions.defaultMode`, `permissions.disableAutoMode` |
| [Песочница](https://code.claude.com/docs/ru/sandboxing.md) | Изоляция файловой системы и сети на уровне ОС с allowlist доменов | `sandbox.enabled`, `sandbox.network.allowedDomains` |
| [Управляемая политика CLAUDE.md](https://code.claude.com/docs/ru/memory.md#deploy-organization-wide-claude-md) | Инструкции по поведению для Claude на уровне организации, а не правило, принудительно применяемое клиентом | Файл по пути управляемой политики |
| [Управление сервером MCP](https://code.claude.com/docs/ru/managed-mcp.md) | Ограничить, какие серверы MCP пользователи могут добавлять или подключать, развернуть фиксированный набор или предоставить удалённые серверы каждому пользователю наряду с их собственными | `allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`, `managedMcpServers` или развёрнутый файл `managed-mcp.json` |
| [Управление маркетплейсом плагинов](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install) | Ограничить, из каких источников маркетплейса пользователи могут добавлять и устанавливать плагины, и отклонять флаги CLI, которые загружают плагины, агентов и MCP-серверы для одного запуска. Блокировать [источники плагинов `command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source) и задать список разрешённых маркетплейсов, плагины которых могут предлагаться в терминале | `strictKnownMarketplaces`, `blockedMarketplaces`, `disableSideloadFlags`, `disableCommandPluginSources`, `pluginSuggestionMarketplaces` |
| [Блокировка настройки](https://code.claude.com/docs/ru/settings-reference.md#strictpluginonlycustomization) | Заблокировать скиллы, агентов, хуки и MCP-серверы из пользовательских и проектных источников. Блокировка скиллов также останавливает синхронизацию [скиллов, которые ваши разработчики включают на claude.ai](https://code.claude.com/docs/ru/skills.md#where-synced-skills-load) | `strictPluginOnlyCustomization` |
| [Отключить синхронизацию claude.ai](https://code.claude.com/docs/ru/settings-reference.md#syncclaudeaiskills) | Остановить Claude Code от загрузки [skills](https://code.claude.com/docs/ru/skills.md#how-synced-skills-behave) и [плагинов](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), которые ваши разработчики включают на claude.ai. Если вы отключите Skills для вашей организации на claude.ai, Claude Code останавливает синхронизацию обоих, и на v2.1.273 или позже это также удаляет те, которые он уже синхронизировал. Чтобы остановить один из них без отключения Skills, установите его ключ на `false` в управляемых параметрах | `syncClaudeAiSkills`, `syncClaudeAiPlugins` |
| [Ограничения hooks](https://code.claude.com/docs/ru/settings-reference.md#allowmanagedhooksonly) | Ограничить, какие hooks выполняются, и ограничить URL-адреса HTTP hooks; см. [что выполняется под `allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#what-runs-under-allowmanagedhooksonly) для полного списка эффектов | `allowManagedHooksOnly`, `allowedHttpHookUrls` |
| [Принудительный вход](https://code.claude.com/docs/ru/settings-reference.md#forceloginmethod) | Ограничить вход определённым методом или организацией Anthropic. Ограничение метода применяется во всём расширении VS Code, Agent SDK, `claude setup-token` и `/install-github-app`, а интерактивный экран входа терминала, доступный через `/login` или первоначальную настройку, предварительно выбирает метод без его принудительного применения; Claude Code проверяет организацию для входов в учётную запись claude.ai в терминале, расширении VS Code и Agent SDK, и не проверяет её для входов в Claude Console или для входа через [gateway](https://code.claude.com/docs/ru/claude-apps-gateway). До версии 2.1.212 только входы в терминал применяли любой из ключей. Когда установлено, сеансы, аутентифицированные через `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper`, блокируются при запуске; облачные сеансы поставщиков не затрагиваются, если только одно из этих учётных данных или ключ API, сохранённый более ранним входом в Claude Console, также не присутствует | `forceLoginMethod`, `forceLoginOrgUUID` |
| [Ограничения поставщика](https://code.claude.com/docs/ru/settings-reference.md#allowedproviders) | Ограничить, какие поставщики API может использовать машина. Сеанс на поставщике, который не указан в списке, отклоняется при запуске, при входе и когда он в следующий раз обращается к API. Требуется Claude Code v2.1.285 или позже | `allowedProviders` |
| [Отключить представление агента](https://code.claude.com/docs/ru/agent-view.md#how-background-sessions-are-hosted) | Отключить `claude agents`, `--bg`, `/background` и супервизор по требованию | `disableAgentView` |
| [Настройка корпоративного запускателя](https://code.claude.com/docs/ru/corporate-launcher.md) | Добавить префикс к [супервизору фонового агента](https://code.claude.com/docs/ru/agent-view.md#how-background-sessions-are-hosted), его рабочим процессам и [другим охватываемым фоновым процессам](https://code.claude.com/docs/ru/corporate-launcher.md#what-the-launcher-covers) с требуемым корпоративным запускателем вместо отключения представления агента | `processWrapper` |
| [Ограничения модели](https://code.claude.com/docs/ru/model-config.md#restrict-model-selection) | `availableModels` фильтрует, какие модели появляются в средстве выбора. Добавление `enforceAvailableModels` также ограничивает автоматически выбранную модель по умолчанию. См. [охват поверхности](https://code.claude.com/docs/ru/model-config.md#surface-coverage) для того, как этот параметр достигает CLI, веб-интерфейса и IDE | `availableModels`, `enforceAvailableModels` |
| [Ограничение усилий](https://code.claude.com/docs/ru/settings-reference.md#maxeffortlevel) | Ограничить [уровень усилий](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) для всех моделей сразу или для каждой модели отдельно, у любого поставщика | `maxEffortLevel` |
| [Минимальная версия](https://code.claude.com/docs/ru/settings-reference.md#minimumversion) | Предотвратить автоматическое обновление от установки ниже минимума на уровне организации | `minimumVersion` |
| [Требуемый диапазон версий](https://code.claude.com/docs/ru/settings-reference.md#requiredminimumversion) | Отказать в запуске вообще, когда работающая версия находится вне одобренного организацией диапазона. Сильнее, чем `minimumVersion`, который только блокирует понижения версии | `requiredMinimumVersion`, `requiredMaximumVersion` |
| [Отказ от телеметрии](https://code.claude.com/docs/ru/data-usage.md#telemetry-services) | Отключить метрики использования, привязанные к Anthropic, отчёты об ошибках и опросы на каждом устройстве | `env` с `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, установленным на `1`; связанный раздел содержит переменные по категориям |

Если ваши члены входят через claude.ai или Anthropic API и вы находитесь на плане Claude Enterprise, вы также можете управлять моделями из параметров администратора вашей организации без развёртывания чего-либо:

* [Ограничения модели организации](https://code.claude.com/docs/ru/model-config.md#organization-model-restrictions): отключить отдельные модели. Применяется на стороне сервера.
* [Модель организации по умолчанию](https://code.claude.com/docs/ru/model-config.md#organization-default-model): задать, на какой модели начинаются новые сессии. Участники по-прежнему могут переключать модели. Чтобы вернуть их к вашей модели по умолчанию, включите переопределение, описанное в этом разделе. Чтобы ограничить, какие модели они могут выбирать, используйте [ограничения моделей организации](https://code.claude.com/docs/ru/model-config.md#organization-model-restrictions).
* [Ограничения усилий организации](https://code.claude.com/docs/ru/model-config.md#organization-effort-limits): ограничить уровни усилий по ролям. Применяется на стороне сервера.

Ни один из этих элементов управления не достигает сеансов на Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry или [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md). На этих поставщиках используйте вместо этого управляемые параметры: `availableModels` для ограничений, `model` для значения по умолчанию и [`maxEffortLevel`](https://code.claude.com/docs/ru/settings-reference#maxeffortlevel) для ограничения усилий.

[Облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) имеют собственные интерфейсы администрирования на claude.ai:

* **Страница облачных сред**: владельцы создают [среды, общие для организации](https://code.claude.com/docs/ru/cloud-environments.md#organization-shared-environments), которые задают [уровень сетевого доступа](https://code.claude.com/docs/ru/cloud-environments.md#network-access), переменные окружения и скрипт настройки для облачных сессий участников.
* **Среда по умолчанию**: владельцы выбирают среду организации по умолчанию отдельно на [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
* **Страница Git providers**: см. [Подключённые учётные записи GitHub](#connected-github-accounts), чтобы узнать об учётных записях GitHub, связанных с вашей организацией.

Правила разрешений и песочница охватывают разные уровни. Запрет WebFetch блокирует инструмент fetch Claude, но если Bash разрешён, `curl` и `wget` всё ещё могут достичь любого URL-адреса. Песочница закрывает этот пробел с помощью allowlist доменов сети, применяемого на уровне ОС.

Для модели угроз, которую защищают эти элементы управления, см. [Безопасность](https://code.claude.com/docs/ru/security.md).

### Подключённые учётные записи GitHub

В планах Team и Enterprise в разделе GitHub страницы [**Organization settings > Git providers**](https://claude.ai/admin-settings/source-control) перечислены организации GitHub и личные учётные записи, связанные с вашей организацией Claude через [Claude GitHub App](https://github.com/apps/claude). Claude Code, [Claude Tag](https://claude.com/docs/claude-tag/admins/configure-github) и Claude Security используют общий список. Чтобы открыть эту страницу, требуется [роль Owner](https://code.claude.com/docs/ru/server-managed-settings.md#access-control) в вашей организации Claude. Роль Admin не может её открыть.

Связать учётную запись можно на странице Git providers или подключив GitHub к Claude:

* **Подключение владельцем**: владелец (Owner) нажимает **Connect** в этом разделе или **Add organization**, если учётная запись уже подключена, и устанавливает Claude GitHub App в организацию GitHub. Для связывания организации этим способом нужен владелец (Owner) вашей организации Claude, который также является владельцем организации GitHub.
* **Подключение участником**: когда участник подключает свою учётную запись GitHub к Claude, например при [настройке облачных сессий](https://code.claude.com/docs/ru/web-quickstart.md#connect-github), Claude связывает учётные записи GitHub, которыми владеет этот участник и в которых уже установлено Claude GitHub App. Это может включать его личную учётную запись и организации GitHub, которыми он владеет.

Строка с пометкой **Not linked** появляется из-за вашего собственного входа в GitHub. Это учётная запись, которую вы видите на GitHub и в которой установлено Claude GitHub App.

Чтобы отвязать учётную запись от вашей организации Claude, откройте меню её строки и выберите **Unlink from this workspace**. При отвязывании Claude GitHub App остаётся установленным на GitHub, и учётная запись снова будет связана, когда один из её владельцев в следующий раз подключит GitHub к Claude. Чтобы она не была связана снова, удалите Claude GitHub App из этой учётной записи на GitHub.

В планах Enterprise типы действий [Compliance API](https://platform.claude.com/docs/en/api/compliance/activities/list) для связывания и отвязывания — `github_app_installation_linked` и `github_app_installation_unlinked`.

## Настройте видимость использования

Выберите мониторинг на основе того, что вам нужно сообщить. Панели управления, API и элементы управления расходами различаются между планами Claude for Teams или Enterprise и организациями Claude Console, поэтому перед планированием отчётности проверьте столбец «Доступность».

| Возможность | Что вы получаете | Доступность | С чего начать |
| :- | :- | :- | :- |
| Usage monitoring | Экспорт OpenTelemetry сеансов, инструментов и токенов | Все поставщики | [Monitoring usage](https://code.claude.com/docs/ru/monitoring-usage.md) |
| Analytics dashboard | Метрики принятия и вклада с таблицей лидеров на Teams / Enterprise; метрики использования и расходов для каждого пользователя на Console | Teams / Enterprise на [claude.ai/analytics](https://claude.ai/analytics/claude-code), Console на [platform.claude.com/claude-code](https://platform.claude.com/claude-code) | [Analytics](https://code.claude.com/docs/ru/analytics.md) |
| Programmatic reporting | Данные об использовании и затратах для каждого пользователя через API | [Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) для Enterprise, [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api) для Console | [Costs](https://code.claude.com/docs/ru/costs.md#manage-costs-for-your-organization) |
| Spend controls | Ограничения расходов и ограничения частоты запросов | Настройки организации для Teams / Enterprise, ограничения Workspace для Console; в сторонних облаках — средства контроля бюджета облака или [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway) с [ограничениями расходов](https://code.claude.com/docs/ru/claude-apps-gateway-spend-limits.md) для каждого пользователя | [Costs](https://code.claude.com/docs/ru/costs.md#manage-costs-for-your-organization) |

На Teams и Enterprise данные об использовании и расходах для каждого пользователя поступают из [отчёта о расходах](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans) в параметрах аналитики вашей организации, а не из панели аналитики. Облачные поставщики раскрывают расходы через AWS Cost Explorer, GCP Billing или Azure Cost Management. Для планирования корпоративных бюджетов в Claude chat, Claude Code и Cowork см. [руководство по потреблению Claude Enterprise](https://support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide).

## Проверьте обработку данных

На планах Team, Enterprise, Claude API и облачных поставщиков Anthropic не обучает модели на вашем коде или промптах. Ваш поставщик API определяет хранение и статус соответствия.

| Тема | Что нужно знать | С чего начать |
| :- | :- | :- |
| Data usage policy | Что собирает Anthropic, как долго это хранится, что никогда не используется для обучения | [Data usage](https://code.claude.com/docs/ru/data-usage.md) |
| Zero Data Retention (ZDR) | Ничего не хранится после завершения запроса. Доступно для соответствующих требованиям аккаунтов на Claude for Enterprise | [Zero data retention](https://code.claude.com/docs/ru/zero-data-retention.md) |
| HIPAA configuration | Для организаций Claude for Enterprise, в которых включён HIPAA. Некоторые функции Claude Code (локальный режим) отключены, а другие выключены по умолчанию | [Set up Claude Code (local mode) for a HIPAA-ready organization](https://code.claude.com/docs/ru/hipaa-setup.md) |
| Security architecture | Сетевая модель, шифрование, аутентификация, журнал аудита | [Security](https://code.claude.com/docs/ru/security.md) |

Если вам нужно логирование аудита на уровне запроса или маршрутизация трафика по чувствительности данных, рекомендуем поместить шлюз между разработчиками и вашим поставщиком: самостоятельно размещённый [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway) записывает журнал аудита для каждого запроса с идентификацией IdP, или вы можете использовать другой [LLM gateway](https://code.claude.com/docs/ru/llm-gateway). Сессии, проходящие через шлюз, не подходят для конфигурации HIPAA. В разделе [Проверьте, как разработчики входят и подключаются](https://code.claude.com/docs/ru/hipaa-setup.md#check-how-developers-sign-in-and-connect) перечислены способы входа и подключения, которые подходят. Для нормативных требований и сертификаций см. [Legal and compliance](https://code.claude.com/docs/ru/legal-and-compliance.md).

## Проверьте и подключите

После настройки управляемых параметров попросите разработчика запустить `/status` внутри Claude Code. На вкладке **Status** строка `Setting sources` показывает `Enterprise managed settings`, за которой следует источник в скобках; [Проверка активных параметров](https://code.claude.com/docs/ru/managed-settings.md#verify-enforcement) содержит список меток.

Поделитесь этими ресурсами, чтобы помочь разработчикам начать работу:

* [Quickstart](https://code.claude.com/docs/ru/quickstart.md): пошаговое руководство первого сеанса от установки до работы с проектом
* [Common workflows](https://code.claude.com/docs/ru/common-workflows.md): шаблоны для повседневных задач, таких как проверка кода, рефакторинг и отладка
* [Claude Code 101](https://academy.claude.com/courses/claude-code-101) и [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action): бесплатные самостоятельные курсы на [Claude Academy](https://academy.claude.com/)

Для проблем с входом направьте разработчиков на [troubleshooting аутентификации](https://code.claude.com/docs/ru/troubleshoot-install.md#login-and-authentication). Наиболее распространенные исправления:

* Запустите `/logout`, а затем `/login` для переключения учетных записей
* Запустите `claude update`, если отсутствует опция аутентификации предприятия
* Перезагрузите терминал после обновления

Если разработчик видит "You haven't been added to your organization yet," его место не включает доступ к Claude Code и должно быть обновлено в консоли администратора.

## Следующие шаги

После выбора поставщика и механизма доставки переходите к подробной конфигурации:

* [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md): доставка управляемой политики из консоли администратора Claude
* [All settings](https://code.claude.com/docs/ru/settings-reference.md): каждый ключ параметра, расположение файла и пример
* [Which value Claude Code uses](https://code.claude.com/docs/ru/settings.md#which-value-claude-code-uses): правила приоритета для управляемых, проектных, локальных и пользовательских параметров
* [Manage plugins for your organization](https://code.claude.com/docs/ru/plugins/org.md): установка общих плагинов на каждый компьютер через управляемые настройки
* [Monorepos and large repos](https://code.claude.com/docs/ru/large-codebases.md): шаблоны конфигурации для каждого каталога для организаций, развертывающих в монорепозиторий
* [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md), [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md): развертывание для конкретного поставщика
* [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide): SSO, SCIM, управление местами и сценарий развертывания
