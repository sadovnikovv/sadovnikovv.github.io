> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Все параметры

> Полный справочник по каждому ключу settings.json в Claude Code: где находится каждый ключ, его тип и значение по умолчанию, а также готовый к использованию пример и индекс всех ключей.

[Back to index](#all-settings)

На этой справочной странице перечислены все ключи, которые Claude Code читает из файла параметров, а также [небольшая группа ключей](#global-config-settings), которые он хранит в `~/.claude.json`. Чтобы выбрать файл или проверить приоритет, начните с [Settings files and precedence](https://code.claude.com/docs/ru/settings.md).

## Индекс настроек

Каждый ключ ниже ссылается на его запись. Область действия указывает [файлы](https://code.claude.com/docs/ru/settings.md#settings-files-and-who-they-affect), в которых он может находиться: `User` — это `~/.claude/settings.json`, `Project` — это `.claude/settings.json`, `Local` — это `.claude/settings.local.json`, а `Managed` — это [то, что развёртывает ваша организация](https://code.claude.com/docs/ru/managed-settings.md). `Any file` означает все четыре, а `Global config` означает [`~/.claude.json`](#global-config-settings).

| Key | Description | Topic | Scope |
| :- | :- | :- | :- |
| [`advisorModel`](#advisormodel) | Выберите, какая модель отвечает, когда Claude использует [инструмент советника](https://code.claude.com/docs/ru/advisor.md) | Model and responses | Any file |
| [`agent`](#agent) | Начинайте каждую сессию как именованный [субагент](https://code.claude.com/docs/ru/sub-agents.md) с его промптом, инструментами и моделью | Agents, sessions, and worktrees | Any file |
| [`agentPushNotifEnabled`](#agentpushnotifenabled) | Позвольте Claude отправить [push-уведомление на ваш телефон](https://code.claude.com/docs/ru/remote-control.md#mobile-push-notifications), когда он решит это сделать | Remote, desktop, and notifications | Any file |
| [`allowAllClaudeAiMcps`](#allowallclaudeaimcps) | Загружайте [коннекторы claude.ai](https://code.claude.com/docs/ru/mcp.md), которые Claude Code получает сам, наряду с развёрнутым [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp#exclusive-control-with-managed-mcp-json) | MCP | Managed |
| [`allowClaudeInChromeWithManagedMcp`](#allowclaudeinchromewithmanagedmcp) | Позвольте встроенному серверу [Claude in Chrome](https://code.claude.com/docs/ru/chrome.md) работать наряду с развёрнутым [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp#exclusive-control-with-managed-mcp-json) | MCP | Managed |
| [`allowedChannelPlugins`](#allowedchannelplugins) | Замените список разрешённых по умолчанию [плагинов каналов](https://code.claude.com/docs/ru/channels.md#restrict-which-channel-plugins-can-run), которые могут отправлять сообщения | Plugins and skills | Managed |
| [`allowedHttpHookUrls`](#allowedhttphookurls) | Ограничьте, какие URL-адреса могут использовать [HTTP-хуки](https://code.claude.com/docs/ru/hooks.md) | Hooks and automation | Any file |
| [`allowedMcpServers`](#allowedmcpservers) | Создайте список разрешённых [MCP-серверов](https://code.claude.com/docs/ru/mcp.md), которые могут добавлять пользователи | MCP | Any file |
| [`allowedProviders`](#allowedproviders) | Ограничьте, какие [поставщики API](https://code.claude.com/docs/ru/third-party-integrations.md) может использовать машина | Authentication and providers | Managed |
| [`allowManagedHooksOnly`](#allowmanagedhooksonly) | Запускайте только [хуки](https://code.claude.com/docs/ru/hooks.md), которые развёртывает ваша организация | Hooks and automation | Managed |
| [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly) | Сделайте управляемый список разрешённых серверов [MCP](https://code.claude.com/docs/ru/mcp.md) единственным применяемым | MCP | Managed |
| [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | Сделайте [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) единственным источником настроек для [правил разрешений](https://code.claude.com/docs/ru/permissions.md#managed-settings) | Permission settings | Managed |
| [`alwaysThinkingEnabled`](#alwaysthinkingenabled) | Отключите [расширенное мышление](https://code.claude.com/docs/ru/model-config.md#extended-thinking) для каждой сессии | Model and responses | Any file |
| [`apiKeyHelper`](#apikeyhelper) | Создайте [учётные данные API](https://code.claude.com/docs/ru/authentication.md#credential-management) с помощью вашей собственной команды | Authentication and providers | Any file |
| [`askUserQuestionTimeout`](#askuserquestiontimeout) | Позвольте неотвеченному вопросу [автоматически продолжиться](https://code.claude.com/docs/ru/tools-reference.md#question-auto-continue-timeout) после времени простоя | Interface and terminal | User or managed |
| [`appendPlugins`](#appendplugins) | Запускайте [моды](https://code.claude.com/docs/ru/plugins/mods/admin.md) вашей организации после каждого мода, который устанавливает пользователь | Plugins and skills | User or managed |
| [`attribution`](#attribution) | Настройте атрибуцию, которую Claude Code добавляет к коммитам и pull request'ам | Git and attribution | Any file |
| [`attribution.commit`](#attribution-commit) | Измените или скройте трейлер, который Claude Code добавляет к коммитам | Git and attribution | Any file |
| [`attribution.pr`](#attribution-pr) | Измените или скройте строку атрибуции в описаниях pull request'ов | Git and attribution | Any file |
| [`attribution.sessionUrl`](#attribution-sessionurl) | Опустите ссылку на сессию claude.ai из [облачных](https://code.claude.com/docs/ru/claude-code-on-the-web.md) и [Remote Control](https://code.claude.com/docs/ru/remote-control.md) коммитов | Git and attribution | Any file |
| [`autoCompactEnabled`](#autocompactenabled) | Отключите или включите [автоматическое сжатие контекста](https://code.claude.com/docs/ru/context-window.md) | Memory and context | Any file |
| [`autoCompactWindow`](#autocompactwindow) | Установите, насколько заполненным становится контекст перед тем, как Claude Code [сжимает](https://code.claude.com/docs/ru/context-window.md) его | Memory and context | Any file |
| [`autoConnectIde`](#autoconnectide) | Автоматически подключайтесь к работающей [VS Code](https://code.claude.com/docs/ru/vs-code.md) или [JetBrains](https://code.claude.com/docs/ru/jetbrains.md#from-external-terminals) IDE из внешнего терминала | Global config settings | Global config |
| [`autoContinueAtUsageLimit`](#autocontinueatusagelimit) | Ждите в открытой сессии и [автоматически продолжайте задачу](https://code.claude.com/docs/ru/interactive-mode.md#wait-for-a-usage-limit-to-reset) после сброса лимита использования claude.ai | Interface and terminal | User or managed |
| [`autoInstallIdeExtension`](#autoinstallideextension) | Позвольте `/ide` устанавливать [расширение IDE](https://code.claude.com/docs/ru/vs-code.md#install-the-extension) из внешнего терминала | Global config settings | Global config |
| [`autoMemoryDirectory`](#automemorydirectory) | Сохраняйте [автоматическую память](https://code.claude.com/docs/ru/memory.md#auto-memory) в выбранном вами каталоге | Memory and context | Any file |
| [`autoMemoryEnabled`](#automemoryenabled) | Отключите или включите [автоматическую память](https://code.claude.com/docs/ru/memory.md#auto-memory) | Memory and context | Any file |
| [`autoMode`](#automode) | Добавьте свои собственные правила разрешения и запрета к классификатору [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) | Permission settings | User or managed |
| [`autoMode.classifyAllShell`](#automode-classifyallshell) | Отправляйте каждую shell-команду через [классификатор авторежима](https://code.claude.com/docs/ru/permission-modes.md#what-the-classifier-blocks-by-default), даже те, которые соответствуют узкому правилу разрешения | Permission settings | User or managed |
| [`autoScrollEnabled`](#autoscrollenabled) | [Следите за новым выводом](https://code.claude.com/docs/ru/fullscreen.md#auto-follow) в нижней части при полноэкранном отображении | Interface and terminal | Any file |
| [`autoUpdatesChannel`](#autoupdateschannel) | Следуйте стабильному [каналу выпуска](https://code.claude.com/docs/ru/setup.md#configure-release-channel) вместо последнего | Updates and versioning | Any file |
| [`availableModels`](#availablemodels) | [Ограничьте, какие модели](https://code.claude.com/docs/ru/model-config.md#restrict-model-selection) люди могут выбирать | Model and responses | Any file |
| [`availableModelsMatch`](#availablemodelsmatch) | Сделайте каждую запись ID модели `availableModels` [разрешающей только версию, которую она называет](https://code.claude.com/docs/ru/model-config.md#block-specific-models-or-versions) | Model and responses | Managed |
| [`awaySummaryEnabled`](#awaysummaryenabled) | Отключите [краткое описание сессии](https://code.claude.com/docs/ru/interactive-mode.md#session-recap), показываемое при возврате к терминалу | Remote, desktop, and notifications | Any file |
| [`awsAuthRefresh`](#awsauthrefresh) | Обновляйте истёкшие [учётные данные Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md#advanced-credential-configuration) в `.aws` с помощью вашей собственной команды | Authentication and providers | Any file |
| [`awsCredentialExport`](#awscredentialexport) | Предоставляйте [учётные данные Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md#advanced-credential-configuration) как JSON из вашей собственной команды | Authentication and providers | Any file |
| [`axScreenReader`](#axscreenreader) | Отображайте [вывод, удобный для программ чтения с экрана](https://code.claude.com/docs/ru/accessibility.md) | Interface and terminal | User or managed |
| [`bashEditDiffEnabled`](#basheditdiffenabled) | Записывайте [файлы, которые изменились во время выполнения команды Bash](https://code.claude.com/docs/ru/hooks.md#bash) в каждом режиме разрешений | Interface and terminal | User or managed |
| [`bashOutputMaxChars`](#bashoutputmaxchars) | Установите, сколько [вывода](https://code.claude.com/docs/ru/tools-reference.md#output-limits) успешной команды Claude получает встроенным образом | Memory and context | Any file |
| [`blockedMarketplaces`](#blockedmarketplaces) | Блокируйте источники [маркетплейса плагинов](https://code.claude.com/docs/ru/plugins/overview.md) для вашей организации | Plugins and skills | Managed |
| [`browserExternalPageTools`](#browserexternalpagetools) | Отключите инструменты Claude на внешних страницах в [настольной](https://code.claude.com/docs/ru/desktop.md) панели Browser | Tools | Managed |
| [`channelsEnabled`](#channelsenabled) | Разрешите [каналы](https://code.claude.com/docs/ru/channels.md#enable-channels-for-your-organization) для вашей организации | Plugins and skills | Managed |
| [`claudeInChromeDefaultEnabled`](#claudeinchromedefaultenabled) | Включайте [интеграцию с Chrome](https://code.claude.com/docs/ru/chrome.md) при запуске сессии в интерактивном CLI и расширении VS Code | Global config settings | Global config |
| [`claudeMd`](#claudemd) | Внедрите организационные [инструкции CLAUDE.md](https://code.claude.com/docs/ru/memory.md#deploy-organization-wide-claude-md) из управляемых настроек | Memory and context | Managed |
| [`claudeMdExcludes`](#claudemdexcludes) | Пропускайте определённые [файлы CLAUDE.md](https://code.claude.com/docs/ru/memory.md#exclude-specific-claude-md-files) при загрузке памяти | Memory and context | Any file |
| [`cleanupPeriodDays`](#cleanupperioddays) | Выберите, сколько дней Claude Code хранит [транскрипты](https://code.claude.com/docs/ru/data-usage.md#data-retention) перед их удалением | Privacy and telemetry | Any file |
| [`companyAnnouncements`](#companyannouncements) | Показывайте объявления вашей организации при запуске | Interface and terminal | Any file |
| [`copyFullResponse`](#copyfullresponse) | Сделайте так, чтобы [`/copy`](https://code.claude.com/docs/ru/commands) копировала полный ответ без отображения средства выбора | Global config settings | Global config |
| [`copyOnSelect`](#copyonselect) | Отключите автоматическое копирование текста, который вы выбираете мышью в [полноэкранном отображении](https://code.claude.com/docs/ru/fullscreen.md#use-the-mouse) и представлении агента | Global config settings | Global config |
| [`crossSessionInbound`](#crosssessioninbound) | Выберите, доставляет ли Claude Code [сообщения из ваших других сессий](https://code.claude.com/docs/ru/cross-session-messaging.md#control-inbound-messages), показывает уведомление без их доставки или отклоняет их | Agents, sessions, and worktrees | Any file |
| [`defaultShell`](#defaultshell) | Выберите, запускается ли Bash или PowerShell для shell-команд, которые вы вводите с префиксом [`!`](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix) | Interface and terminal | Any file |
| [`defaultToAgentsView`](#defaulttoagentsview) | Открывайте [представление агента](https://code.claude.com/docs/ru/agent-view.md) вместо нового диалога при запуске `claude` без аргументов | Global config settings | Global config |
| [`deniedMcpServers`](#deniedmcpservers) | Блокируйте определённые [MCP-серверы](https://code.claude.com/docs/ru/mcp.md) по URL, команде или имени | MCP | Any file |
| [`deniedModels`](#deniedmodels) | [Блокируйте определённые модели](https://code.claude.com/docs/ru/model-config.md#block-specific-models-or-versions), даже те, которые разрешает `availableModels` | Model and responses | Managed |
| [`desktopSessionCleanupPeriodDays`](#desktopsessioncleanupperioddays) | Установите возрастной лимит в днях для [транскриптов Claude Desktop и Cowork](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically) | Privacy and telemetry | User or managed |
| [`dialogExpiry`](#dialogexpiry) | Установите, как долго Claude Code ждёт, пока [Remote Control](https://code.claude.com/docs/ru/remote-control.md) или хост SDK ответит на переданное диалоговое окно, прежде чем отменить его | Interface and terminal | User or managed |
| [`diffTool`](#difftool) | Выберите, открываются ли предложенные Claude изменения файлов в средстве просмотра diff [VS Code](https://code.claude.com/docs/ru/vs-code.md) или [JetBrains](https://code.claude.com/docs/ru/jetbrains.md#features) или остаются в терминале | Global config settings | Global config |
| [`disableAgentView`](#disableagentview) | Отключите фоновые агенты и [представление агента](https://code.claude.com/docs/ru/agent-view.md) | Agents, sessions, and worktrees | Any file |
| [`disableAllHooks`](#disableallhooks) | Отключите [хуки](https://code.claude.com/docs/ru/hooks.md), пользовательскую [строку состояния](https://code.claude.com/docs/ru/statusline.md) и пользовательскую команду [предложения файлов `@`](https://code.claude.com/docs/ru/interactive-mode#quick-commands) одновременно | Hooks and automation | Any file |
| [`disableArtifact`](#disableartifact) | Устарело; используйте `enableArtifact` для отключения [инструмента Artifact](https://code.claude.com/docs/ru/artifacts.md) | Remote, desktop, and notifications | Any file |
| [`disableAutoMode`](#disableautomode) | Удалите [авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) из цикла режимов разрешений | Permission settings | Any file |
| [`disableBrowserExternalNavigation`](#disablebrowserexternalnavigation) | Ограничьте [настольную](https://code.claude.com/docs/ru/desktop.md) панель Browser только localhost для людей и Claude | Tools | Managed |
| [`disableBundledSkills`](#disablebundledskills) | Отключите [скиллы](https://code.claude.com/docs/ru/skills.md#bundled-skills) и [рабочие процессы](https://code.claude.com/docs/ru/workflows.md), включённые в Claude Code | Plugins and skills | Any file |
| [`disableClaudeAiConnectors`](#disableclaudeaiconnectors) | Отключите [коннекторы claude.ai](https://code.claude.com/docs/ru/mcp.md#disable-claude-ai-connectors), чтобы Claude Code их не получал | MCP | Any file |
| [`disableCommandPluginSources`](#disablecommandpluginsources) | Блокируйте [плагины](https://code.claude.com/docs/ru/plugins/overview.md), которые устанавливаются путём выполнения команды, объявленной маркетплейсом | Plugins and skills | Managed |
| [`disableDeepLinkRegistration`](#disabledeeplinkregistration) | Запретите Claude Code регистрировать обработчик [`claude-cli://`](https://code.claude.com/docs/ru/deep-links) | Remote, desktop, and notifications | Any file |
| [`disableDesktopLocalSessions`](#disabledesktoplocalsessions) | Отключите [сессии Desktop Code](https://code.claude.com/docs/ru/desktop.md#local-sessions-on-managed-devices), которые работают на устройстве, оставляя SSH к другим хостам и облако | Remote, desktop, and notifications | Managed |
| [`disabledMcpjsonServers`](#disabledmcpjsonservers) | Отклоняйте определённые серверы из [`.mcp.json`](https://code.claude.com/docs/ru/mcp#project-scope) проекта | MCP | Any file |
| [`disableMobileSimulatorTools`](#disablemobilesimulatortools) | Блокируйте инструменты Claude в [настольной](https://code.claude.com/docs/ru/desktop.md) панели iOS Simulator | Tools | Managed |
| [`disableRemoteControl`](#disableremotecontrol) | Отключите [Remote Control](https://code.claude.com/docs/ru/remote-control.md) везде, где он может запуститься | Remote, desktop, and notifications | Any file |
| [`disableRemotePreviewScripts`](#disableremotepreviewscripts) | Отключите скрипты в HTML-предпросмотрах [настольного](https://code.claude.com/docs/ru/desktop.md#preview-html-files-in-ssh-and-wsl-sessions) приложения в сессиях SSH и WSL | Remote, desktop, and notifications | Managed |
| [`disableSideloadFlags`](#disablesideloadflags) | Отклоняйте флаги CLI, которые загружают [плагины](https://code.claude.com/docs/ru/plugins/overview.md), [субагенты](https://code.claude.com/docs/ru/sub-agents.md) и [MCP-серверы](https://code.claude.com/docs/ru/mcp.md) в обход установки | Enterprise and managed settings | Managed |
| [`disableSkillShellExecution`](#disableskillshellexecution) | Запретите [скиллам](https://code.claude.com/docs/ru/skills.md) и пользовательским командам встроенное выполнение shell-команд | Plugins and skills | Any file |
| [`disableWorkflows`](#disableworkflows) | Отключите [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md) для всех; используйте `enableWorkflows` для себя | Hooks and automation | Any file |
| [`editorMode`](#editormode) | Используйте [сочетания клавиш vim](https://code.claude.com/docs/ru/interactive-mode.md#vim-editor-mode) в поле ввода промпта | Interface and terminal | Any file |
| [`effortLevel`](#effortlevel) | Установите [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) по умолчанию для моделей без собственного сохранённого уровня | Model and responses | Any file |
| [`emojiCompletionEnabled`](#emojicompletionenabled) | Отключите [предложения и замену эмодзи `:shortcode:`](https://code.claude.com/docs/ru/interactive-mode#emoji-shortcodes) в поле ввода промпта | Interface and terminal | Any file |
| [`enableAllProjectMcpServers`](#enableallprojectmcpservers) | Одобряйте каждый сервер в файлах проекта [`.mcp.json`](https://code.claude.com/docs/ru/mcp#project-server-approvals-and-workspace-trust) без запроса подтверждения | MCP | Any file |
| [`enableArtifact`](#enableartifact) | Отключите [инструмент Artifact](https://code.claude.com/docs/ru/artifacts.md) с помощью `false` в любом файле; ни один файл не может его включить обратно | Remote, desktop, and notifications | Any file |
| [`enabledMcpjsonServers`](#enabledmcpjsonservers) | Одобрите определённые серверы из [`.mcp.json`](https://code.claude.com/docs/ru/mcp#project-server-approvals-and-workspace-trust) проекта | MCP | Any file |
| [`enabledPlugins`](#enabledplugins) | Включайте или отключайте отдельные [плагины](https://code.claude.com/docs/ru/plugins/overview.md) для каждой области действия | Plugins and skills | Any file |
| [`enableWorkflows`](#enableworkflows) | Включайте или отключайте [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md) вопреки умолчанию вашего плана | Hooks and automation | Any file |
| [`enforceAvailableModels`](#enforceavailablemodels) | Держите [выбор по умолчанию в `/model`](https://code.claude.com/docs/ru/model-config#enforce-the-allowlist-for-the-default-model) в пределах вашего списка разрешённых моделей `availableModels` | Model and responses | Any file |
| [`env`](#env) | Установите [переменные окружения](https://code.claude.com/docs/ru/env-vars.md#in-settings-files) для каждой сессии и её подпроцессов | Memory and context | Any file |
| [`externalEditorContext`](#externaleditorcontext) | Показывайте последний ответ Claude как комментарии при нажатии [Ctrl+G](https://code.claude.com/docs/ru/interactive-mode.md#general-controls) для редактирования | Global config settings | Global config |
| [`extraKnownMarketplaces`](#extraknownmarketplaces) | Зарегистрируйте [маркетплейсы](https://code.claude.com/docs/ru/plugins/overview.md) для репозитория или организации | Plugins and skills | Any file |
| [`fallbackModel`](#fallbackmodel) | Назовите [резервные модели](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains) на случай перегрузки основной | Model and responses | Any file |
| [`fastMode`](#fastmode) | Включите [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) для сессий, где он доступен | Model and responses | Any file |
| [`fastModePerSessionOptIn`](#fastmodepersessionoptin) | Требуйте, чтобы люди включали [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) в каждой сессии | Model and responses | Any file |
| [`feedbackDrafts`](#feedbackdrafts) | Контролируйте, ставит ли Claude в очередь [черновики обратной связи](https://code.claude.com/docs/ru/tools-reference.md#sendfeedback-tool-behavior) для вашего рассмотрения | Privacy and telemetry | User or managed |
| [`feedbackSurveyRate`](#feedbacksurveyrate) | Измените частоту появления [опроса качества сессии](https://code.claude.com/docs/ru/data-usage.md#session-quality-surveys) | Privacy and telemetry | Any file |
| [`fileCheckpointingEnabled`](#filecheckpointingenabled) | Отключите или включите снимки файлов, которые [`/rewind`](https://code.claude.com/docs/ru/checkpointing) восстанавливает | Memory and context | Any file |
| [`fileSuggestion`](#filesuggestion) | Предоставляйте [автодополнение файлов `@`](https://code.claude.com/docs/ru/interactive-mode#quick-commands) из вашей собственной команды | Interface and terminal | Any file |
| [`footerLinksRegexes`](#footerlinksregexes) | Превратите ID задач или рецензий в выводе в [кликабельные ссылки](https://code.claude.com/docs/ru/statusline.md#clickable-links) под полем ввода | Interface and terminal | User or managed |
| [`forceLoginGatewayUrl`](#forcelogingatewayurl) | Установите [URL шлюза](https://code.claude.com/docs/ru/claude-apps-gateway#set-the-gateway-url), к которому подключается экран входа | Authentication and providers | User or managed |
| [`forceLoginMethod`](#forceloginmethod) | [Ограничьте вход](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization) на claude.ai, Claude Console или [облачный шлюз](https://code.claude.com/docs/ru/claude-apps-gateway) | Authentication and providers | Any file |
| [`forceLoginOrgUUID`](#forceloginorguuid) | [Привяжите входы claude.ai к вашей организации](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization); это обеспечивают только управляемые настройки | Authentication and providers | Any file |
| [`forceRemoteSettingsRefresh`](#forceremotesettingsrefresh) | Блокируйте запуск до тех пор, пока [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md), не будут заново получены | Enterprise and managed settings | Managed |
| [`gatewayInternalNetworks`](#gatewayinternalnetworks) | Позвольте `/login` достичь [облачного шлюза](https://code.claude.com/docs/ru/claude-apps-gateway#allow-a-gateway-on-public-address-space-you-own) в общедоступном пространстве IPv4, которое ваша организация использует внутри | Authentication and providers | Managed |
| [`gcpAuthRefresh`](#gcpauthrefresh) | Обновляйте [учётные данные Google Cloud](https://code.claude.com/docs/ru/google-vertex-ai.md#advanced-credential-configuration) с помощью вашей собственной команды | Authentication and providers | Any file |
| [`hooks`](#hooks) | Запускайте свои собственные команды как [хуки](https://code.claude.com/docs/ru/hooks.md) в точках жизненного цикла Claude Code | Hooks and automation | Any file |
| [`httpHookAllowedEnvVars`](#httphookallowedenvvars) | Ограничьте, какие переменные окружения [HTTP-хуки](https://code.claude.com/docs/ru/hooks.md) могут помещать в заголовки | Hooks and automation | Any file |
| [`idleCompaction`](#idlecompaction) | Запретите Claude Code сжимать длинный диалог, от которого вы отошли | Memory and context | Any file |
| [`includeCoAuthoredBy`](#includecoauthoredby) | Устарело; используйте `attribution` для скрытия или изменения атрибуции коммитов и PR | Git and attribution | Any file |
| [`includeGitInstructions`](#includegitinstructions) | Удалите встроенные инструкции для коммитов и PR из контекста Claude | Git and attribution | Any file |
| [`inputNeededNotifEnabled`](#inputneedednotifenabled) | Получайте [push-уведомление](https://code.claude.com/docs/ru/remote-control.md#mobile-push-notifications), когда Claude ждёт вас | Remote, desktop, and notifications | Any file |
| [`isolatePeerMachines`](#isolatepeermachines) | Спрашивать вас перед тем, как Claude [отправит сообщение одной из ваших сессий на другой машине](https://code.claude.com/docs/ru/cross-session-messaging.md#require-approval-for-cross-machine-messages) | Agents, sessions, and worktrees | Any file |
| [`keybindingFlavor`](#keybindingflavor) | Устарело и не имеет эффекта; сочетания клавиш для редактирования слов всегда [следуют соглашениям readline](https://code.claude.com/docs/ru/interactive-mode.md#make-ctrl-w-delete-back-to-whitespace) | Interface and terminal | Any file |
| [`language`](#language) | Попросите Claude отвечать на языке, отличном от английского | Model and responses | Any file |
| [`leftArrowOpensAgents`](#leftarrowopensagents) | Отключите сочетание клавиш `←`, которое [переводит сессию в фон и открывает представление агента](https://code.claude.com/docs/ru/agent-view.md#switch-sessions-without-leaving-the-terminal) | Global config settings | Global config |
| [`managedMcpServers`](#managedmcpservers) | Предоставляйте удалённые [MCP-серверы](https://code.claude.com/docs/ru/managed-mcp.md#provide-servers-through-managed-settings) каждому пользователю наряду с теми, которые они добавляют | MCP | Managed |
| [`managedSourcesBehavior`](#managedsourcesbehavior) | Объединяйте каждый [управляемый источник](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources), который вы развёртываете, вместо использования только одного с наивысшим приоритетом | Enterprise and managed settings | Managed |
| [`maxEffortLevel`](#maxeffortlevel) | Ограничьте [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) для всех моделей или для каждой модели отдельно, у любого поставщика | Model and responses | Any file |
| [`maxProseWidth`](#maxprosewidth) | Ограничьте ширину прозы в ответах Claude в широком терминале | Interface and terminal | Any file |
| [`minimumVersion`](#minimumversion) | Не позволяйте [автоматическим обновлениям](https://code.claude.com/docs/ru/setup.md#pin-a-minimum-version) устанавливать версии ниже заданной | Updates and versioning | Any file |
| [`model`](#model) | Измените [модель](https://code.claude.com/docs/ru/model-config.md#set-a-default-model-for-new-sessions), с которой Claude Code начинает | Model and responses | Any file |
| [`modelOverrides`](#modeloverrides) | [Сопоставьте ID моделей](https://code.claude.com/docs/ru/model-config.md#override-model-ids-per-version) с ID вашего поставщика, такими как Bedrock ARN | Model and responses | Any file |
| [`modelPicker`](#modelpicker) | Выберите, какие модели перечисляет [средство выбора `/model`](https://code.claude.com/docs/ru/model-config#available-models), в вашем собственном порядке и с вашими собственными метками | Model and responses | User or managed |
| [`modelPricing`](#modelpricing) | Сообщайте расходы по контрактным ставкам вашей организации вместо прейскурантной цены | Model and responses | Managed |
| [`modelSettings`](#modelsettings) | Сохраняйте для каждой модели [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) или [окно автосжатия](https://code.claude.com/docs/ru/model-config.md#set-the-auto-compact-window) либо ограничивайте effort одной модели | Model and responses | Any file |
| [`otelHeadersHelper`](#otelheadershelper) | Создавайте ротирующие заголовки [OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md#dynamic-headers) с помощью вашей собственной команды | Authentication and providers | Any file |
| [`outputStyle`](#outputstyle) | Измените роль, тон и формат вывода Claude с помощью [стиля вывода](https://code.claude.com/docs/ru/output-styles.md) | Model and responses | Any file |
| [`parentSettingsBehavior`](#parentsettingsbehavior) | Применяйте или отбрасывайте ограничения, которые [хост SDK или IDE](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy) передаёт при развёртывании [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md) | Enterprise and managed settings | Managed |
| [`permissionExplainerEnabled`](#permissionexplainerenabled) | Удалено в v2.1.257 вместе с объяснением команды по `Ctrl+E` в запросах разрешений для shell-команд | Global config settings | Global config |
| [`permissions`](#permissions) | Задает правила allow, ask и deny, а также [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) по умолчанию | Permission settings | Any file |
| [`permissions.additionalDirectories`](#permissions-additionaldirectories) | Дайте Claude доступ к файлам в [каталогах вне текущего](https://code.claude.com/docs/ru/permissions.md#working-directories) | Permission settings | Any file |
| [`permissions.allow`](#permissions-allow) | Одобряйте перечисленные [использования инструментов](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax) без запроса подтверждения | Permission settings | Any file |
| [`permissions.ask`](#permissions-ask) | Всегда запрашивайте подтверждение перед перечисленными [использованиями инструментов](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax) | Permission settings | Any file |
| [`permissions.blockReadsOutsideWorkingDirectories`](#permissions-blockreadsoutsideworkingdirectories) | Заставьте файловые инструменты отказываться от чтения вне [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories) в каждом режиме разрешений | Permission settings | Any file |
| [`permissions.blockWritesOutsideWorkingDirectories`](#permissions-blockwritesoutsideworkingdirectories) | Заставьте инструменты `Write`, `Edit` и `NotebookEdit` отказываться от путей вне [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories) в каждом режиме разрешений, за исключением [некоторых собственных файлов Claude Code](#what-the-write-block-refuses-and-what-stays-writable) | Permission settings | Any file |
| [`permissions.defaultMode`](#permissions-defaultmode) | Устанавливает [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in) по умолчанию для новых сессий | Permission settings | Any file |
| [`permissions.deny`](#permissions-deny) | Блокируйте перечисленные [использования инструментов](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax), включая чтение файлов, содержащих секреты | Permission settings | Any file |
| [`permissions.denyInsteadOfPrompting`](#permissions-denyinsteadofprompting) | Отклоняйте вызовы инструментов, которые ожидали бы [запроса разрешения](https://code.claude.com/docs/ru/permissions.md#permission-system), чтобы сессия, за которой никто не следит, продолжала работать | Permission settings | User or managed |
| [`permissions.disableBypassPermissionsMode`](#permissions-disablebypasspermissionsmode) | Запретите кому-либо входить в [режим bypassPermissions](https://code.claude.com/docs/ru/permission-modes.md#skip-all-checks-with-bypasspermissions-mode) | Permission settings | Any file |
| [`plansDirectory`](#plansdirectory) | Выберите, где [режим планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode) записывает файлы плана | Memory and context | Any file |
| [`pluginConfigs`](#pluginconfigs) | Сохраняйте ответы, которые вы дали в диалоговом окне конфигурации [плагина](https://code.claude.com/docs/ru/plugins/overview.md) | Plugins and skills | User or managed |
| [`pluginSuggestionMarketplaces`](#pluginsuggestionmarketplaces) | Выберите, какие [маркетплейсы](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install) могут выводить предложения по установке плагинов в `/plugin` | Plugins and skills | Managed |
| [`pluginTrustMessage`](#plugintrustmessage) | Добавьте свой собственный текст к предупреждению о доверии [плагину](https://code.claude.com/docs/ru/plugins/overview.md) | Plugins and skills | Managed |
| [`policyHelper`](#policyhelper) | Запустите исполняемый файл, который вычисляет [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md#compute-the-policy-with-a-helper-program) при запуске | Enterprise and managed settings | Managed |
| [`policyHelper.path`](#policyhelper-path) | Назовите [вспомогательный исполняемый файл](https://code.claude.com/docs/ru/managed-settings.md#compute-the-policy-with-a-helper-program), который запускает Claude Code | Enterprise and managed settings | Managed |
| [`policyHelper.refreshIntervalMs`](#policyhelper-refreshintervalms) | Повторно запускайте [вспомогательную программу](https://code.claude.com/docs/ru/managed-settings.md#compute-the-policy-with-a-helper-program) в фоне с заданным интервалом | Enterprise and managed settings | Managed |
| [`policyHelper.timeoutMs`](#policyhelper-timeoutms) | Установите, как долго Claude Code ждёт [вспомогательную программу](https://code.claude.com/docs/ru/managed-settings.md#compute-the-policy-with-a-helper-program) | Enterprise and managed settings | Managed |
| [`preferredNotifChannel`](#preferrednotifchannel) | Выберите [звонок терминала или уведомление рабочего стола](https://code.claude.com/docs/ru/terminal-config.md#get-a-terminal-bell-or-notification) для завершения задачи | Remote, desktop, and notifications | Any file |
| [`prefersReducedMotion`](#prefersreducedmotion) | [Уменьшите или отключите](https://code.claude.com/docs/ru/accessibility.md#accessibility-settings) анимацию спиннера, мерцания и вспышки | Interface and terminal | Any file |
| [`prependPlugins`](#prependplugins) | Запускайте [моды](https://code.claude.com/docs/ru/plugins/mods/admin.md) вашей организации перед каждым модом, который устанавливает пользователь | Plugins and skills | User or managed |
| [`processWrapper`](#processwrapper) | Запускайте фоновые процессы Claude Code через [корпоративный запускатель](https://code.claude.com/docs/ru/corporate-launcher.md) на macOS и Linux | Agents, sessions, and worktrees | User or managed |
| [`promptCacheTtl`](#promptcachettl) | Выберите [время жизни кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime) для основного диалога | Model and responses | Any file |
| [`promptSuggestionEnabled`](#promptsuggestionenabled) | Скройте серые [предложения промптов](https://code.claude.com/docs/ru/interactive-mode.md#prompt-suggestions) в поле ввода | Interface and terminal | Any file |
| [`prStatusFooterEnabled`](#prstatusfooterenabled) | Отключите значок [статуса ревью PR](https://code.claude.com/docs/ru/interactive-mode.md#pr-review-status) в нижней панели промпта и стоящую за ним проверку pull request | Global config settings | Global config |
| [`prUrlTemplate`](#prurltemplate) | Направляйте ссылки на PR во внутренний инструмент код-ревью вместо github.com | Git and attribution | Any file |
| [`remote.defaultEnvironmentId`](#remote-defaultenvironmentid) | Выберите [облачную среду](https://code.claude.com/docs/ru/cloud-environments.md) по умолчанию для `claude --cloud`; самостоятельно размещённый ID `ccpool_` считывается только из пользовательских и управляемых настроек и `--settings` | Remote, desktop, and notifications | Any file |
| [`remoteControlAtStartup`](#remotecontrolatstartup) | Подключайте [Remote Control](https://code.claude.com/docs/ru/remote-control.md#enable-remote-control-for-all-sessions) автоматически при запуске сессии | Remote, desktop, and notifications | Any file |
| [`requiredMaximumVersion`](#requiredmaximumversion) | [Отказывайте в запуске](https://code.claude.com/docs/ru/setup.md#pin-a-minimum-version) на версии новее, чем позволяет ваша организация | Updates and versioning | Managed |
| [`requiredMinimumVersion`](#requiredminimumversion) | [Отказывайте в запуске](https://code.claude.com/docs/ru/setup.md#pin-a-minimum-version) на версии старше, чем требует ваша организация | Updates and versioning | Managed |
| [`respectGitignore`](#respectgitignore) | Исключайте игнорируемые git файлы из [средства выбора файлов `@`](https://code.claude.com/docs/ru/interactive-mode#quick-commands) | Interface and terminal | Any file |
| [`respondToBashCommands`](#respondtobashcommands) | Запретите Claude отвечать после выполнения [shell-команды с `!`](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix) | Interface and terminal | Any file |
| [`sandbox`](#sandbox) | [Изолируйте команды Bash](https://code.claude.com/docs/ru/sandboxing.md) от вашей файловой системы и сети на macOS, Linux и WSL2 | Sandbox settings | Any file |
| [`sandbox.allowAppleEvents`](#sandbox-allowappleevents) | Позвольте [изолированным](https://code.claude.com/docs/ru/sandboxing.md) командам отправлять Apple Events на macOS | Sandbox settings | User or managed |
| [`sandbox.allowNestedUserNamespaces`](#sandbox-allownestedusernamespaces) | Позвольте [изолированным](https://code.claude.com/docs/ru/sandboxing.md#chromium-or-rootless-podman-fails-inside-the-sandbox-on-linux) командам создавать пространства имён пользователей на Linux и WSL2 | Sandbox settings | User or managed |
| [`sandbox.allowUnsandboxedCommands`](#sandbox-allowunsandboxedcommands) | Позвольте Claude повторить попытку выполнения заблокированной команды вне [песочницы](https://code.claude.com/docs/ru/sandboxing.md#the-unsandboxed-retry-escape-hatch) или запретите это | Sandbox settings | Any file |
| [`sandbox.autoAllowBashIfSandboxed`](#sandbox-autoallowbashifsandboxed) | Запускайте [изолированные](https://code.claude.com/docs/ru/sandboxing.md#auto-allow-mode) команды без запроса разрешения | Sandbox settings | Any file |
| [`sandbox.bwrapPath`](#sandbox-bwrappath) | Укажите [песочнице](https://code.claude.com/docs/ru/sandboxing.md) двоичный файл bubblewrap вне `PATH` | Sandbox settings | Managed |
| [`sandbox.credentials`](#sandbox-credentials) | Скройте или замаскируйте файлы учётных данных и переменные внутри [песочницы](https://code.claude.com/docs/ru/sandboxing.md#protect-credentials) | Sandbox settings | Any file |
| [`sandbox.credentials.allowPlaintextInject`](#sandbox-credentials-allowplaintextinject) | Позвольте [замаскированным учётным данным](https://code.claude.com/docs/ru/sandboxing.md#mask-credentials) достигать простых HTTP-сервисов в доверенных тестовых сетях | Sandbox settings | User or managed |
| [`sandbox.credentials.awsPairs`](#sandbox-credentials-awspairs) | Свяжите переменные ключей AWS с пользовательскими именами в одни учётные данные для [повторного подписания](https://code.claude.com/docs/ru/sandboxing.md#re-sign-aws-requests) | Sandbox settings | User or managed |
| [`sandbox.credentials.envVars`](#sandbox-credentials-envvars) | Удалите или замаскируйте переменную окружения внутри [песочницы](https://code.claude.com/docs/ru/sandboxing.md#mask-environment-variables) | Sandbox settings | Any file |
| [`sandbox.credentials.files`](#sandbox-credentials-files) | Блокируйте или маскируйте чтение файла учётных данных внутри [песочницы](https://code.claude.com/docs/ru/sandboxing.md#mask-credential-files) | Sandbox settings | Any file |
| [`sandbox.credentials.sigv4`](#sandbox-credentials-sigv4) | Выберите, будут ли потоковые, предварительно подписанные или [запросы AWS SigV4A](https://code.claude.com/docs/ru/sandboxing.md#re-sign-aws-requests) завершаться ошибкой или пропускаться | Sandbox settings | User or managed |
| [`sandbox.enabled`](#sandbox-enabled) | Включите [изоляцию Bash в песочнице](https://code.claude.com/docs/ru/sandboxing.md#get-started) на macOS, Linux и WSL2 | Sandbox settings | Any file |
| [`sandbox.enableWeakerNestedSandbox`](#sandbox-enableweakernestedsandbox) | Запускайте Linux-[песочницу](https://code.claude.com/docs/ru/sandboxing.md) внутри непривилегированного контейнера | Sandbox settings | Any file |
| [`sandbox.enableWeakerNetworkIsolation`](#sandbox-enableweakernetworkisolation) | Позвольте `gh`, `gcloud` и `terraform` проверять TLS за MITM-прокси внутри [песочницы](https://code.claude.com/docs/ru/sandboxing.md#go-based-clis-fail-tls-verification-on-macos) на macOS | Sandbox settings | Any file |
| [`sandbox.excludedCommands`](#sandbox-excludedcommands) | Назовите команды, которые Claude Code может запускать вне [песочницы](https://code.claude.com/docs/ru/sandboxing.md) | Sandbox settings | Any file |
| [`sandbox.failIfUnavailable`](#sandbox-failifunavailable) | Отказывайте в запуске, когда [песочница](https://code.claude.com/docs/ru/sandboxing.md) не может запуститься, вместо работы без изоляции, за исключением среды, размещённой Anthropic | Sandbox settings | Any file |
| [`sandbox.filesystem`](#sandbox-filesystem) | Контролируйте, какие пути [изолированные](https://code.claude.com/docs/ru/sandboxing.md#filesystem-isolation) команды могут читать и записывать | Sandbox settings | Any file |
| [`sandbox.filesystem.allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly) | Запретите разработчикам повторно открывать [пути чтения, которые заблокировала ваша организация](https://code.claude.com/docs/ru/sandboxing.md#keep-developers-from-widening-the-policy) | Sandbox settings | Managed |
| [`sandbox.filesystem.allowRead`](#sandbox-filesystem-allowread) | Повторно откройте чтение внутри области, которую блокирует [`denyRead`](#sandbox-filesystem-denyread) | Sandbox settings | Any file |
| [`sandbox.filesystem.allowWrite`](#sandbox-filesystem-allowwrite) | Добавьте пути, в которые [изолированные](https://code.claude.com/docs/ru/sandboxing.md) команды могут записывать | Sandbox settings | Any file |
| [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread) | Запретите [изолированным](https://code.claude.com/docs/ru/sandboxing.md) командам читать определённые пути | Sandbox settings | Any file |
| [`sandbox.filesystem.denyWrite`](#sandbox-filesystem-denywrite) | Запретите [изолированным](https://code.claude.com/docs/ru/sandboxing.md) командам записывать в определённые пути | Sandbox settings | Any file |
| [`sandbox.filesystem.disabled`](#sandbox-filesystem-disabled) | [Отключите изоляцию файловой системы](https://code.claude.com/docs/ru/sandboxing.md#disable-filesystem-isolation) при сохранении изоляции сети | Sandbox settings | User or managed |
| [`sandbox.ignoreViolations`](#sandbox-ignoreviolations) | Заглушите отчёты о нарушениях для путей, которые команда, как ожидается, будет проверять | Sandbox settings | Any file |
| [`sandbox.network`](#sandbox-network) | Контролируйте, к каким хостам, портам и сокетам обращаются [изолированные](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) команды | Sandbox settings | Any file |
| [`sandbox.network.allowAllUnixSockets`](#sandbox-network-allowallunixsockets) | Позвольте [изолированным](https://code.claude.com/docs/ru/sandboxing.md) командам подключаться к любому Unix-сокету | Sandbox settings | Any file |
| [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) | Предварительно разрешите домены, чтобы [изолированные](https://code.claude.com/docs/ru/sandboxing.md) команды не запрашивали их | Sandbox settings | Any file |
| [`sandbox.network.allowLocalBinding`](#sandbox-network-allowlocalbinding) | Позвольте [изолированным](https://code.claude.com/docs/ru/sandboxing.md) командам прослушивать сетевые порты и подключаться к localhost на macOS | Sandbox settings | Any file |
| [`sandbox.network.allowMachLookup`](#sandbox-network-allowmachlookup) | Позвольте [изолированным](https://code.claude.com/docs/ru/sandboxing.md) инструментам macOS, таким как iOS Simulator или Playwright, достигать своих XPC-сервисов | Sandbox settings | Any file |
| [`sandbox.network.allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) | Ограничьте сетевой список разрешённых доменов [управляемыми настройками](https://code.claude.com/docs/ru/sandboxing.md#keep-developers-from-widening-the-policy) | Sandbox settings | Managed |
| [`sandbox.network.allowUnixSockets`](#sandbox-network-allowunixsockets) | Перечислите пути Unix-сокетов, которые [изолированные](https://code.claude.com/docs/ru/sandboxing.md) команды могут использовать на macOS | Sandbox settings | Any file |
| [`sandbox.network.deniedDomains`](#sandbox-network-denieddomains) | Блокируйте домены для [изолированных](https://code.claude.com/docs/ru/sandboxing.md) команд, даже внутри разрешённого подстановочного шаблона | Sandbox settings | Any file |
| [`sandbox.network.httpProxyPort`](#sandbox-network-httpproxyport) | Направляйте HTTP-трафик [песочницы](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration) через ваш собственный прокси | Sandbox settings | Any file |
| [`sandbox.network.socksProxyPort`](#sandbox-network-socksproxyport) | Направляйте SOCKS-трафик [песочницы](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration) через ваш собственный прокси | Sandbox settings | Any file |
| [`sandbox.network.strictAllowlist`](#sandbox-network-strictallowlist) | Отказывайте хостам вне [списка разрешённых](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) вместо запроса | Sandbox settings | User or managed |
| [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate) | Пусть прокси [песочницы](https://code.claude.com/docs/ru/sandboxing.md#network-isolation) завершает TLS, чтобы он мог читать HTTPS-запросы | Sandbox settings | User or managed |
| [`sandbox.ripgrep`](#sandbox-ripgrep) | Используйте свой собственный двоичный файл ripgrep внутри [песочницы](https://code.claude.com/docs/ru/sandboxing.md) | Sandbox settings | User or managed |
| [`sandbox.socatPath`](#sandbox-socatpath) | Укажите прокси [песочницы](https://code.claude.com/docs/ru/sandboxing.md) двоичный файл `socat` вне `PATH` | Sandbox settings | Managed |
| [`showClearContextOnPlanAccept`](#showclearcontextonplanaccept) | Показывайте опцию "очистить контекст" на [экране принятия плана](https://code.claude.com/docs/ru/permission-modes.md#review-and-approve-a-plan) | Interface and terminal | Any file |
| [`showThinkingSummaries`](#showthinkingsummaries) | Смотрите сводки [размышлений](https://code.claude.com/docs/ru/model-config.md#extended-thinking) Claude вместо свёрнутой заглушки | Model and responses | Any file |
| [`showTurnDuration`](#showturnduration) | Скройте длительность "Cooked for" после каждого ответа | Interface and terminal | Any file |
| [`skillListingBudgetFraction`](#skilllistingbudgetfraction) | Зарезервируйте больше или меньше контекста для [списка скиллов](https://code.claude.com/docs/ru/skills.md#skill-descriptions-are-cut-short) | Memory and context | Any file |
| [`skillListingMaxDescChars`](#skilllistingmaxdescchars) | Ограничьте длину описания каждого скилла в [списке скиллов](https://code.claude.com/docs/ru/skills.md#skill-descriptions-are-cut-short) | Memory and context | Any file |
| [`skillOverrides`](#skilloverrides) | [Скройте или сверните скилл](https://code.claude.com/docs/ru/skills.md#override-skill-visibility-from-settings) без редактирования его SKILL.md | Plugins and skills | Any file |
| [`skipAutoPermissionPrompt`](#skipautopermissionprompt) | Пропустите одноразовое уведомление, которое Claude Code показывает при первом входе в [авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) самостоятельно, а не через встроенное значение по умолчанию | Permission settings | User or managed |
| [`skipDangerousModePermissionPrompt`](#skipdangerousmodepermissionprompt) | Пропустите диалоговое окно подтверждения перед [режимом bypassPermissions](https://code.claude.com/docs/ru/permission-modes.md#skip-all-checks-with-bypasspermissions-mode) | Permission settings | User, local, or managed |
| [`skipWebFetchPreflight`](#skipwebfetchpreflight) | Пропустите [проверку имени хоста WebFetch](https://code.claude.com/docs/ru/tools-reference.md#webfetch-tool-behavior), когда Anthropic недоступен | Privacy and telemetry | Any file |
| [`spellcheck`](#spellcheck) | Подчёркивайте неправильно написанные слова в поле ввода промпта с помощью [средства проверки орфографии](https://code.claude.com/docs/ru/interactive-mode.md#check-spelling-as-you-type), которое вы устанавливаете | Interface and terminal | User or managed |
| [`spinnerTipsEnabled`](#spinnertipsenabled) | Скройте советы в спиннере, пока Claude работает | Interface and terminal | Any file |
| [`spinnerTipsOverride`](#spinnertipsoverride) | Добавьте свои собственные советы к ротации спиннера или замените встроенные советы | Interface and terminal | Any file |
| [`spinnerVerbs`](#spinnerverbs) | Добавьте или замените глаголы, показываемые во время выполнения хода | Interface and terminal | Any file |
| [`sshConfigs`](#sshconfigs) | Добавьте [SSH-подключения](https://code.claude.com/docs/ru/desktop.md#pre-configure-ssh-connections-for-your-team) в средство выбора среды Desktop | Remote, desktop, and notifications | User or managed |
| [`sshHostAllowlist`](#sshhostallowlist) | Ограничьте, к каким хостам могут подключаться [SSH-сессии Desktop](https://code.claude.com/docs/ru/desktop.md#restrict-which-ssh-hosts-users-can-connect-to) | Remote, desktop, and notifications | Managed |
| [`sshHostCommands`](#sshhostcommands) | Добавьте [SSH-подключения, хост которых определяется командой](https://code.claude.com/docs/ru/desktop.md#create-an-ssh-connection-from-a-command), в средство выбора среды Desktop | Remote, desktop, and notifications | User or managed |
| [`statusLine`](#statusline) | Запустите свою собственную команду для отображения [строки состояния](https://code.claude.com/docs/ru/statusline.md) под промптом | Interface and terminal | Any file |
| [`strictKnownMarketplaces`](#strictknownmarketplaces) | Создайте список разрешённых источников [маркетплейсов](https://code.claude.com/docs/ru/plugins/overview.md), которые пользователи могут добавлять и из которых могут устанавливать | Plugins and skills | Managed |
| [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) | Блокируйте [скиллы](https://code.claude.com/docs/ru/skills.md), [агенты](https://code.claude.com/docs/ru/sub-agents.md), [хуки](https://code.claude.com/docs/ru/hooks.md) и [MCP-серверы](https://code.claude.com/docs/ru/mcp.md) из пользовательских и проектных источников | Plugins and skills | Managed |
| [`strictPluginOnlyCustomization.agents`](#strictpluginonlycustomization-agents) | Блокируйте [агенты](https://code.claude.com/docs/ru/sub-agents.md) из пользовательских и проектных источников | Plugins and skills | Managed |
| [`strictPluginOnlyCustomization.hooks`](#strictpluginonlycustomization-hooks) | Блокируйте [хуки](https://code.claude.com/docs/ru/hooks.md) из пользовательских и проектных источников | Plugins and skills | Managed |
| [`strictPluginOnlyCustomization.mcp`](#strictpluginonlycustomization-mcp) | Блокируйте [MCP-серверы](https://code.claude.com/docs/ru/mcp.md) из пользовательских и проектных источников | Plugins and skills | Managed |
| [`strictPluginOnlyCustomization.skills`](#strictpluginonlycustomization-skills) | Блокируйте [скиллы](https://code.claude.com/docs/ru/skills.md) из пользовательских и проектных источников | Plugins and skills | Managed |
| [`subagentPromptCacheTtl`](#subagentpromptcachettl) | Выберите [время жизни кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime) для субагентов и других запросов вне основного диалога | Model and responses | Any file |
| [`switchModelsOnFlag`](#switchmodelsonflag) | Переключайте модели автоматически или приостанавливайте работу, когда [классификатор безопасности](https://code.claude.com/docs/ru/model-config.md#ask-before-switching) помечает запрос | Model and responses | Any file |
| [`syncClaudeAiPlugins`](#syncclaudeaiplugins) | Прекратите загрузку [плагинов, включённых в вашей учётной записи claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), и скачивание новых | Plugins and skills | User, local, or managed |
| [`syncClaudeAiSkills`](#syncclaudeaiskills) | Прекратите загрузку [скиллов, включённых в вашей учётной записи claude.ai](https://code.claude.com/docs/ru/skills.md#how-synced-skills-behave), и скачивание новых | Plugins and skills | User, local, or managed |
| [`syntaxHighlightingDisabled`](#syntaxhighlightingdisabled) | Отключите подсветку синтаксиса в diff и блоках кода | Interface and terminal | Any file |
| [`taskOutputMaxChars`](#taskoutputmaxchars) | Удалено в v2.1.277 вместе с инструментом `TaskOutput`, размер вывода которого оно определяло | Memory and context | Any file |
| [`teammateDefaultModel`](#teammatedefaultmodel) | Удалено в v2.1.234; см. [Укажите участников команды и модели](https://code.claude.com/docs/ru/agent-teams.md#specify-teammates-and-models), чтобы узнать, как Claude Code выбирает модель участника команды | Global config settings | Global config |
| [`teammateMode`](#teammatemode) | Выберите, как [отображаются участники команды агентов](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode) | Agents, sessions, and worktrees | Any file |
| [`terminalProgressBarEnabled`](#terminalprogressbarenabled) | Скройте полосу прогресса терминала в терминалах, которые её поддерживают | Interface and terminal | Any file |
| [`terminalTitleFromRename`](#terminaltitlefromrename) | Запретите [`/rename`](https://code.claude.com/docs/ru/sessions#name-your-sessions) и `--name` изменять название вкладки терминала | Interface and terminal | Any file |
| [`theme`](#theme) | Выберите [цветовую тему](https://code.claude.com/docs/ru/terminal-config.md#match-the-color-theme) интерфейса, встроенную или пользовательскую | Interface and terminal | Any file |
| [`timeFormat`](#timeformat) | Показывайте время в интерфейсе в 12-часовом или 24-часовом формате, в UTC или с шаблоном strftime | Interface and terminal | Any file |
| [`timeZone`](#timezone) | Показывайте время в интерфейсе в часовом поясе, отличном от вашего системного | Interface and terminal | Any file |
| [`tui`](#tui) | Выберите [полноэкранный](https://code.claude.com/docs/ru/fullscreen.md) или классический рендерер терминала | Interface and terminal | Any file |
| [`ultracode`](#ultracode) | Пусть Claude планирует [рабочий процесс](https://code.claude.com/docs/ru/workflows.md#let-claude-decide-with-ultracode) для каждой существенной задачи без отдельной просьбы | Model and responses | Any file |
| [`useAutoModeDuringPlan`](#useautomodeduringplan) | Позвольте классификатору [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) проверять shell-команды в [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode); установите `false`, чтобы вместо этого получать запросы подтверждения | Permission settings | User, local, or managed |
| [`verbose`](#verbose) | Показывайте [полный вывод инструментов](https://code.claude.com/docs/ru/cli-reference.md#cli-flags) вместо усечённых сводок; `viewMode` имеет приоритет, когда установлены оба | Interface and terminal | Any file |
| [`viewMode`](#viewmode) | Начинайте каждую сессию в [представлении по умолчанию, подробном или сфокусированном](https://code.claude.com/docs/ru/cli-reference.md#cli-flags) | Interface and terminal | Any file |
| [`vimInsertModeRemaps`](#viminsertmoderemaps) | Сопоставьте двухклавишную [последовательность режима INSERT](https://code.claude.com/docs/ru/interactive-mode.md#remap-insert-mode-key-sequences), такую как `jj`, с Escape | Interface and terminal | User or managed |
| [`voice`](#voice) | Включите [голосовую диктовку](https://code.claude.com/docs/ru/voice-dictation.md) и выберите режим удержания или нажатия | Interface and terminal | Any file |
| [`voiceEnabled`](#voiceenabled) | Включите [голосовую диктовку](https://code.claude.com/docs/ru/voice-dictation.md) с помощью более старой однокнопочной формы | Interface and terminal | Any file |
| [`wheelScrollAccelerationEnabled`](#wheelscrollaccelerationenabled) | Отключите [ускорение прокрутки колесом мыши](https://code.claude.com/docs/ru/fullscreen.md#mouse-wheel-scrolling) при полноэкранном отображении | Interface and terminal | Any file |
| [`workflowKeywordTriggerEnabled`](#workflowkeywordtriggerenabled) | Позвольте слову `ultracode` в промпте запускать [рабочий процесс](https://code.claude.com/docs/ru/workflows.md); установите `false`, чтобы вводить его без запуска | Hooks and automation | Any file |
| [`workflowSizeGuideline`](#workflowsizeguideline) | Установите количество агентов, к которому Claude стремится в [динамических рабочих процессах](https://code.claude.com/docs/ru/workflows.md) | Hooks and automation | Any file |
| [`worktree`](#worktree) | Настройте, как Claude Code создаёт git [worktrees](https://code.claude.com/docs/ru/worktrees.md) | Agents, sessions, and worktrees | Any file |
| [`worktree.baseRef`](#worktree-baseref) | Создавайте новые [worktrees](https://code.claude.com/docs/ru/worktrees.md) от удалённой ветки по умолчанию или вашего локального HEAD | Agents, sessions, and worktrees | Any file |
| [`worktree.bgIsolation`](#worktree-bgisolation) | Позвольте фоновым сессиям редактировать рабочую копию без [worktree](https://code.claude.com/docs/ru/worktrees.md) | Agents, sessions, and worktrees | Any file |
| [`worktree.location`](#worktree-location) | Выберите, где [SSH-сессии Desktop](https://code.claude.com/docs/ru/desktop.md#ssh-sessions) создают свои worktrees на удалённой машине | Agents, sessions, and worktrees | User |
| [`worktree.sparsePaths`](#worktree-sparsepaths) | Извлекайте только необходимые вам каталоги в каждом [worktree](https://code.claude.com/docs/ru/worktrees.md) | Agents, sessions, and worktrees | Any file |
| [`worktree.symlinkDirectories`](#worktree-symlinkdirectories) | Создавайте символические ссылки на большие каталоги в каждом [worktree](https://code.claude.com/docs/ru/worktrees.md) вместо их дублирования | Agents, sessions, and worktrees | Any file |
| [`wslInheritsWindowsSettings`](#wslinheritswindowssettings) | Пусть WSL читает [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) из цепочки политик Windows | Enterprise and managed settings | Managed |

## Модель и ответы

Выберите, какие модели использует Claude Code и как он отвечает. О том, как эти настройки взаимодействуют с командой `/model` и переменными окружения, см. [Конфигурация модели](https://code.claude.com/docs/ru/model-config.md).

### `advisorModel`

Выберите модель, которая отвечает, когда Claude вызывает серверный [инструмент advisor](https://code.claude.com/docs/ru/advisor.md). Удалите значение, чтобы отключить advisor. Advisor должен быть не менее способным, чем ваша основная модель. Допустимые сочетания и то, что происходит при выборе недопустимой модели, описаны в разделе [Выбор модели advisor](https://code.claude.com/docs/ru/advisor.md#choose-an-advisor-model).

Обычно этот ключ не редактируют вручную. Выполните `/advisor`, чтобы открыть окно выбора, в котором показаны текущий выбор, модели, которые могут выступать в роли advisor, и вариант **No advisor**. Claude Code сохраняет ваш выбор в этот ключ в `~/.claude/settings.json`. Если вы делаете выбор из клиента [Remote Control](https://code.claude.com/docs/ru/remote-control.md) или в сессии, подключённой к удалённому исполнителю, выбор применяется только к этой сессии и не изменяет этот ключ.

Если ваша учётная запись требует [согласия на использование кредитов использования](https://code.claude.com/docs/ru/advisor.md#fable-advisor-and-usage-credits), сначала дайте его, выполнив `/model fable`. Пока вы этого не сделаете, выбор Fable в `/advisor` ничего не сохраняет, и Claude Code предлагает сначала выполнить `/model fable`.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, один из псевдонимов `"fable"`, `"opus"` или `"sonnet"`, которые разрешаются в текущую версию по умолчанию соответствующего семейства моделей в Claude Code, либо полный ID модели, например `"claude-opus-5-5"`
* **По умолчанию**: не задано, поэтому advisor отключён
* **Переопределения для сессии**: `--advisor` имеет приоритет над этим ключом для одной сессии. [`CLAUDE_CODE_DISABLE_ADVISOR_TOOL`](https://code.claude.com/docs/ru/env-vars) отключает advisor, и этот ключ не может снова его включить

```json settings.json theme={null}
{
  "advisorModel": "opus"
}
```

Ключ не действует у провайдеров, где advisor [недоступен](https://code.claude.com/docs/ru/advisor.md#requirements), например Amazon Bedrock. На Claude Platform on AWS или [Claude Models on Google Cloud (Anthropic managed)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md) для ключа требуется Claude Code v2.1.300 или новее. Для `"fable"` требуется [доступ к Fable](https://code.claude.com/docs/ru/advisor.md#choose-an-advisor-model).

### `alwaysThinkingEnabled`

Отключите [расширенное мышление](https://code.claude.com/docs/ru/model-config.md#extended-thinking) для всех сессий, установив значение `false`. Мышление включено по умолчанию, поэтому `true` ничего не меняет. Большинство пользователей задают это через `/config`, а не редактируя файл.

На моделях, которые всегда используют мышление, таких как Opus 5.5, Sonnet 5.5, Haiku 5.5 и модели Fable, значение `false` не действует. У [сторонних провайдеров](https://code.claude.com/docs/ru/third-party-integrations.md) Claude Code не передаёт параметр `thinking` вместо того, чтобы отключать мышление, поэтому модели с адаптивными рассуждениями всё равно могут использовать мышление. Когда мышление отключено в Anthropic API, Claude Code отправляет effort `high` вместо более высокого уровня моделям, которые, как ему известно, [не принимают такое сочетание](https://code.claude.com/docs/ru/errors.md#effort-isnt-available-with-thinking-turned-off), например Opus 5.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: не действует; мышление уже включено
  * `false`: Claude Code отключает расширенное мышление для всех сессий
* **По умолчанию**: не задано, поэтому мышление включено для моделей, которые его поддерживают
* **Переопределения для сессии**: [`MAX_THINKING_TOKENS`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом для одной сессии: `0` отключает мышление с теми же ограничениями модели и провайдера, что и `false`, а положительное значение включает мышление, даже если этот ключ равен `false`. На моделях с адаптивными рассуждениями само число игнорируется

```json settings.json theme={null}
{
  "alwaysThinkingEnabled": false
}
```

### `availableModels`

Ограничьте, какие модели пользователи могут выбирать для основной сессии, [субагентов](https://code.claude.com/docs/ru/sub-agents.md), [скиллов](https://code.claude.com/docs/ru/skills.md) и [advisor](https://code.claude.com/docs/ru/advisor.md). Управляемый список ограничивает `/model`, `--model` и ключ `model` в собственных файлах разработчика; модель вне списка выбрать нельзя. При сопоставлении по префиксу, используемом по умолчанию, это само по себе не затрагивает вариант Default; для этого используйте его вместе с [`enforceAvailableModels`](#enforceavailablemodels).

* **Область действия**: [`Any file`](#scopes). Разверните его в управляемых настройках, чтобы применить принудительно для организации.
* **Тип**: массив псевдонимов или ID моделей
* **По умолчанию**: не задано, поэтому доступны все модели

В этом примере пользователи могут выбирать только модели Sonnet и Haiku:

```json settings.json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

Запись с ID модели, например `"claude-opus-5"`, также разрешает более поздние версии, которые его расширяют, например Opus 5.5. Чтобы заблокировать одну из этих версий, используйте [`deniedModels`](#deniedmodels). Чтобы каждая запись с ID модели разрешала только указанную в ней версию, используйте [`availableModelsMatch`](#availablemodelsmatch). См. [Ограничение выбора модели](https://code.claude.com/docs/ru/model-config.md#restrict-model-selection). Об ID сторонних провайдеров см. [Закрепление моделей для сторонних развёртываний](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments).

### `availableModelsMatch`

Выберите, как записи [`availableModels`](#availablemodels) сопоставляются с ID моделей. По умолчанию запись с ID модели также разрешает более поздние версии, которые его расширяют, поэтому `"claude-opus-5"` разрешает Opus 5.5. При значении `"exact"` каждая запись с ID модели разрешает только указанную в ней версию, поэтому более новая версия этой модели остаётся заблокированной, пока вы не добавите её в список. Требуется Claude Code v2.1.283 или новее.

* **Область действия**: [`Managed`](#scopes). Claude Code игнорирует ключ в пользовательских, проектных и локальных настройках, а также в `--settings`, с предупреждением
* **Тип**: строка, одно из значений:
  * `"prefix"`: запись с ID модели разрешает свою версию и любой ID модели, который расширяет его ещё одним сегментом
  * `"exact"`: запись с ID модели разрешает только указанную в ней версию, поэтому `"claude-opus-5"` разрешает Opus 5, но не `claude-opus-5-5`. Запись вроде `"claude-opus-4-5"` также разрешает свой ID модели Anthropic с датой `claude-opus-4-5-20251101`. Псевдоним семейства, например `"opus"`, по-прежнему разрешает всё семейство, а записи `best`, `opusplan` и `default` игнорируются
* **По умолчанию**: `"prefix"`

В этом примере разрешены Opus 5 и Sonnet 5 и никакие более поздние выпуски этих моделей:

```json managed-settings.json theme={null}
{
  "availableModels": ["claude-opus-5", "claude-sonnet-5"],
  "availableModelsMatch": "exact"
}
```

При значении `"exact"` вариант Default также ограничивается перечисленными моделями, если в списке указана хотя бы одна модель или семейство. См. [Блокировка отдельных моделей или версий](https://code.claude.com/docs/ru/model-config.md#block-specific-models-or-versions).

### `deniedModels`

Блокируйте отдельные модели — со списком разрешённых моделей [`availableModels`](#availablemodels) или без него, и даже если этот список их разрешает. Claude Code скрывает заблокированную модель в окне выбора `/model`, и эту модель нельзя выбрать нигде, где применяется `availableModels`. Сессия с вариантом Default также не запускает заблокированную модель, как описано в разделе [Блокировка отдельных моделей или версий](https://code.claude.com/docs/ru/model-config.md#block-specific-models-or-versions). Требуется Claude Code v2.1.283 или новее.

* **Область действия**: [`Managed`](#scopes). Claude Code игнорирует ключ в пользовательских, проектных и локальных настройках, а также в `--settings`, с предупреждением
* **Тип**: массив псевдонимов или ID моделей
  * Псевдоним семейства, например `"opus"`, блокирует все модели этого семейства
  * ID модели, например `"claude-opus-5-5"`, блокирует эту версию в любом написании, включая ID с датами и ID конкретных провайдеров
  * ID модели без минорной версии, например `"claude-opus-5"`, также блокирует более поздние минорные версии, например Opus 5.5. Укажите `"claude-opus-5-0"`, чтобы заблокировать только Opus 5
  * Записи `best`, `opusplan` и `default` игнорируются
* **По умолчанию**: не задано, поэтому ни одна модель не заблокирована

В этом примере разрешены модели Opus и Sonnet, а Opus 5.5 заблокирована:

```json managed-settings.json theme={null}
{
  "availableModels": ["opus", "sonnet"],
  "deniedModels": ["claude-opus-5-5"]
}
```

См. [Блокировка отдельных моделей или версий](https://code.claude.com/docs/ru/model-config.md#block-specific-models-or-versions).

### `effortLevel`

Задайте [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) по умолчанию для моделей, для которых вы не сохранили уровень. Более низкие уровни быстрее и дешевле на простых задачах, а более высокие обеспечивают более глубокие рассуждения на сложных задачах.

Когда вы выполняете `/effort low`, `medium`, `high` или `xhigh` в интерактивной сессии на своём компьютере, Claude Code сохраняет уровень для активной модели в [`modelSettings`](#modelsettings), а не записывает этот ключ. До v2.1.251 команда `/effort` записывала этот ключ.

В пределах одного файла настроек Claude Code использует сохранённый уровень модели, а не этот ключ. Приоритет между файлами описан в [`modelSettings`](#modelsettings).

В сессии, подключённой к удалённому исполнителю, при запуске с `-p` и в Agent SDK `/effort` применяется только к этой сессии. В разделе [Настройка уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) перечислены варианты интерактивного выбора, которые также применяются только к этой сессии. Сообщение, которое выводит `/effort`, указывает, что именно произошло.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"low"`: минимум рассуждений, для коротких, чётко ограниченных задач, чувствительных к задержке и не чувствительных к уровню интеллекта модели
  * `"medium"`: сокращает расход токенов для работы, чувствительной к стоимости, где допустимо пожертвовать частью интеллекта
  * `"high"`: баланс между расходом токенов и интеллектом
  * `"xhigh"`: более глубокие рассуждения при большем расходе токенов
* **По умолчанию**: не задано
* **Переопределения для сессии**: `--effort` имеет приоритет над этим ключом для одной сессии, а [`CLAUDE_CODE_EFFORT_LEVEL`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над обоими

```json settings.json theme={null}
{
  "effortLevel": "xhigh"
}
```

В вашем файле пользовательских настроек, `~/.claude/settings.json`, этот ключ — это старая форма, которую `/effort` записывала до того, как стала сохранять уровни для каждой модели, и он продолжает применяться там, где применялся раньше: к Opus 5, Fable 5.1 и более ранним моделям. Opus 5.5 и модели, выпущенные после неё, игнорируют его и начинают со своего уровня по умолчанию, пока вы не сохраните для них уровень, который `/effort` записывает в [`modelSettings`](#modelsettings). В проектных, локальных и управляемых настройках, а также с `--settings` этот ключ применяется ко всем моделям.

### `enforceAvailableModels`

В окне выбора `/model` есть вариант **Default**, а в разделе [настройка модели `default`](https://code.claude.com/docs/ru/model-config#default-model-setting) описано, в какую модель он разрешается. Список разрешённых моделей [`availableModels`](#availablemodels) ограничивает модели, которые можно указать по имени, но при [сопоставлении по префиксу](#availablemodelsmatch), используемом по умолчанию, он не переназначает модель по умолчанию для вашего типа учётной записи, поэтому **Default** всё ещё может разрешиться в модель вне списка. Этот ключ закрывает этот пробел. Требуется Claude Code v2.1.175 или новее.

Если ваша организация развёртывает какие-либо управляемые настройки, Claude Code читает этот ключ только из управляемого источника и игнорирует его в других ваших файлах.

О том, как этот ключ применяется к проверкам модели при запуске, см. [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md#when-your-organization-enforces-a-model-allowlist) и [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md#when-your-organization-enforces-a-model-allowlist).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: когда **Default** разрешился бы в модель вне `availableModels`, Claude Code разрешает его в первую доступную модель из списка
  * `false`: этот ключ не меняет то, как разрешается **Default**
* **По умолчанию**: `false`

В этом примере выбор по имени ограничен моделями Sonnet и Haiku, а **Default** разрешается в первую из них, которая доступна:

```json settings.json theme={null}
{
  "availableModels": ["sonnet", "haiku"],
  "enforceAvailableModels": true
}
```

Этот ключ не действует, если `availableModels` не задан или пуст. См. [Применение списка разрешённых моделей к модели Default](https://code.claude.com/docs/ru/model-config.md#enforce-the-allowlist-for-the-default-model). Требуется Claude Code v2.1.175 или новее.

### `fallbackModel`

Укажите резервные модели, которые Claude Code будет пробовать по порядку, когда ваша основная модель перегружена или недоступна. Claude Code переключается на следующую доступную модель в цепочке до конца хода и показывает уведомление. Без цепочки Claude Code повторяет попытку с той же моделью, а затем показывает ошибку сервера, и вы сами повторяете попытку или переключаете модель.

Переключение означает один ход с холодным [кэшем промптов](https://code.claude.com/docs/ru/prompt-caching.md#switching-models) на резервной модели; ваше следующее сообщение снова сначала пробует основную модель.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: массив псевдонимов или ID моделей; `"default"` раскрывается в модель по умолчанию
* **По умолчанию**: не задано, поэтому неудавшийся запрос не повторяется на другой модели
* **Переопределения для сессии**: `--fallback-model` имеет приоритет над этим ключом для одной сессии

В этом примере при сбое основной модели сначала пробуется Sonnet 5, затем Haiku 5.5:

```json settings.json theme={null}
{
  "fallbackModel": ["claude-sonnet-5", "claude-haiku-5-5"]
}
```

В отличие от большинства настроек-массивов, этот ключ не объединяется между файлами настроек: всю цепочку задаёт файл с наивысшим приоритетом, в котором он определён. Если ваш проектный файл задаёт `["claude-sonnet-5"]`, а пользовательский — `["claude-haiku-4-5"]`, цепочка будет только `["claude-sonnet-5"]`. Claude Code сохраняет из списка не более трёх различных разрешённых моделей и игнорирует остальные. См. [Цепочки резервных моделей](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains).

### `fastMode`

Включите [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) для сессий, где он доступен, — для интерактивной работы, например быстрой итерации или отладки в реальном времени, когда вам нужна скорость при более высокой стоимости за токен. Обычно этот ключ не редактируют вручную. Выполнение `/fast` записывает `fastMode: true` в `~/.claude/settings.json`, а повторное выполнение для отключения быстрого режима удаляет ключ.

В Anthropic API быстрый режим поддерживают только Fable 5.2, Opus 5.5, Opus 5 и Opus 4.8. Выполнение `/fast` на другой модели переключает вас на Opus, а переключение на неподдерживаемую модель отключает быстрый режим. См. [Переключение моделей при включённом быстром режиме](https://code.claude.com/docs/ru/fast-mode.md#switch-models-while-fast-mode-is-on). В Google Cloud's Agent Platform [`/fast` вместо этого переключает вас на Fable 5.2](https://code.claude.com/docs/ru/fast-mode#use-fast-mode-on-agent-platform) и не записывает этот ключ, а Claude Code игнорирует сохранённое значение `true`.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code включает быстрый режим для сессий, где он доступен. На Fable 5.2 также нужно [выполнить `/fast` при использовании Fable 5.2](https://code.claude.com/docs/ru/fast-mode#switch-models-while-fast-mode-is-on)
  * `false`: быстрый режим остаётся выключенным
* **По умолчанию**: не задано, поэтому быстрый режим выключен
* **Переопределения для сессии**: [`CLAUDE_CODE_DISABLE_FAST_MODE`](https://code.claude.com/docs/ru/env-vars) отключает быстрый режим для одной сессии, и этот ключ не может снова его включить

```json settings.json theme={null}
{
  "fastMode": true
}
```

### `fastModePerSessionOptIn`

Обычно выполнение `/fast` сохраняет [`fastMode`](#fastmode) в пользовательские настройки человека, поэтому новые сессии на поддерживаемой модели начинаются с включённым быстрым режимом. На Fable 5.2 это происходит, только если быстрый режим был [включён при использовании Fable 5.2](https://code.claude.com/docs/ru/fast-mode.md#switch-models-while-fast-mode-is-on). Чтобы каждому пользователю нужно было выполнять `/fast` в каждой сессии, где он нужен, установите этот ключ в `true`. Claude Code оставляет ключ `fastMode` в файле пользователя, поэтому отключение этого ключа восстанавливает прежнее поведение.

Владельцы на тарифах Team или Enterprise могут развернуть его на всю организацию через [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md). Когда ключ задан в управляемых настройках, `/fast on` отклоняется вне интерактивных сессий в терминале и сообщает, что ваша организация отключила быстрый режим. Это касается [неинтерактивного режима](https://code.claude.com/docs/ru/headless.md), [расширения VS Code](https://code.claude.com/docs/ru/vs-code.md) и [облачных сессий](https://code.claude.com/docs/ru/claude-code-on-the-web.md).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: сохранённое `fastMode: true` больше не включает быстрый режим при запуске сессии, поэтому каждый пользователь выполняет `/fast` в каждой сессии, где он нужен; `fastMode: true`, переданное через `--settings`, по-прежнему учитывается для этой сессии, если этот ключ не задан в управляемых настройках
  * `false`: сохранённое `fastMode: true` работает так, как описано в [`fastMode`](#fastmode)
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

См. [Требование явного включения в каждой сессии](https://code.claude.com/docs/ru/fast-mode.md#require-per-session-opt-in).

### `language`

Сделайте так, чтобы Claude по умолчанию отвечал на языке, отличном от английского. Фиксированного списка для ответов нет: Claude Code передаёт значение Claude дословно как инструкцию всегда отвечать на этом языке, поэтому подходит любое название языка, которое Claude может прочитать. Claude Code не проверяет значение, поэтому название с опечаткой дойдёт до Claude в том виде, в каком написано, а не вызовет ошибку. Это же значение задаёт язык для [голосового ввода](https://code.claude.com/docs/ru/voice-dictation.md#change-the-dictation-language), у которого как раз есть фиксированный список [поддерживаемых языков диктовки](https://code.claude.com/docs/ru/voice-dictation.md#change-the-dictation-language), и для автоматически создаваемых названий сессий.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, любое название языка, например `"japanese"`, `"spanish"` или `"french"`; Claude Code его не проверяет
* **По умолчанию**: не задано; названия сессий в этом случае соответствуют языку вашего диалога

```json settings.json theme={null}
{
  "language": "japanese"
}
```

### `maxEffortLevel`

Ограничьте [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level), который может использовать сессия, оставив доступными более низкие уровни. Любой более высокий уровень выполняется на уровне ограничения, в том числе уровень из `/effort`, окна выбора `/model`, `--effort`, [`CLAUDE_CODE_EFFORT_LEVEL`](https://code.claude.com/docs/ru/env-vars), поля `effort` во frontmatter скилла или субагента либо собственного уровня модели по умолчанию. Claude Code сам применяет ограничение перед каждым запросом, поэтому оно действует у любого провайдера, включая Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry. Требуется Claude Code v2.1.267 или новее.

* **Область действия**: [`Any file`](#scopes). Разверните его в управляемых настройках, чтобы применить принудительно для организации. Если ограничение задано в нескольких областях действия, применяется самое низкое, поэтому ограничение, заданное в одной области действия, нельзя повысить из другой
* **Тип**: строка, одно из значений `"low"`, `"medium"`, `"high"`, `"xhigh"` или `"max"`. Значение `"max"` не задаёт ограничения
* **По умолчанию**: не задано, поэтому ограничение не применяется
* **Ограничения для отдельных моделей**: добавьте `maxEffortLevel` в запись модели в [`modelSettings`](#modelsettings). Эта запись заменяет этот ключ для данной модели только в пределах источника настроек, который задаёт оба, например ваших пользовательских настроек или одного [управляемого источника](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources). Укажите там `"max"`, чтобы исключить модель из ограничения этого источника; Claude Code по-прежнему применяет ограничения из других источников

В этом примере все модели ограничены уровнем `medium`, а Sonnet 4.6 исключена:

```json settings.json theme={null}
{
  "maxEffortLevel": "medium",
  "modelSettings": {
    "claude-sonnet-4-6": {
      "maxEffortLevel": "max"
    }
  }
}
```

Если ваша организация также задаёт для модели [ограничение effort](https://code.claude.com/docs/ru/model-config.md#organization-effort-limits), применяется меньшее из двух ограничений.

### `model`

Задайте модель, которую использует каждая новая сессия, чтобы не выбирать её через `/model` каждый раз. Если задать её здесь, это не мешает переключаться посреди сессии. Если ваш администратор задал [модель организации по умолчанию](https://code.claude.com/docs/ru/model-config.md#organization-default-model), переопределяющую выбор пользователя, вы получаете эту модель, даже если задали этот ключ в пользовательских, проектных или локальных настройках.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, псевдоним модели или полный ID модели
* **По умолчанию**: не задано, поэтому Claude Code использует модель по умолчанию для вашей учётной записи
* **Переопределения для сессии**: `--model` имеет приоритет над [`ANTHROPIC_MODEL`](https://code.claude.com/docs/ru/env-vars), и оба имеют приоритет над этим ключом для одной сессии, в том числе над управляемым `model`; список [`availableModels`](#availablemodels) по-прежнему применяется к выбору

```json settings.json theme={null}
{
  "model": "claude-sonnet-5"
}
```

Значение здесь имеет приоритет над [`ANTHROPIC_DEFAULT_MODEL`](https://code.claude.com/docs/ru/model-config#set-a-default-model-for-new-sessions), который Claude Code использует, только когда модель не выбрана ничем другим.

### `modelOverrides`

Сопоставьте ID моделей Anthropic с ID моделей конкретного провайдера, например ARN профилей инференса Amazon Bedrock. Тогда каждая запись в окне выбора модели при вызове API провайдера использует сопоставленное значение. Администраторы используют это на [Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry](https://code.claude.com/docs/ru/model-config.md#override-model-ids-per-version), чтобы направлять каждую версию модели на конкретный профиль инференса, имя версии или развёртывание для целей управления, распределения затрат или региональной маршрутизации.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект, сопоставляющий ID модели с ID модели провайдера
* **По умолчанию**: не задано

В этом примере все вызовы Opus 4.6 направляются на указанный профиль инференса Bedrock:

```json settings.json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-1:123456789012:inference-profile/example"
  }
}
```

См. [Переопределение ID моделей для каждой версии](https://code.claude.com/docs/ru/model-config.md#override-model-ids-per-version).

### `modelPicker`

Перечислите модели, которые предлагает окно выбора `/model`, в том порядке, в котором вы их записываете, и под выбранными вами метками, чтобы в окне выбора были модели, которые использует ваша организация, — после встроенного набора или вместо него. Значение `model` каждой строки берётся дословно, поэтому оно принимает всё, что принимает `--model`: псевдоним, например `opus`, ID модели Anthropic или ID в формате провайдера для Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry или LLM-шлюза. Требуется Claude Code v2.1.242 или новее.

* **Область действия**: [`User or managed`](#scopes). Claude Code читает ключ из управляемых настроек, `--settings` и пользовательских настроек и игнорирует его в проектных и локальных настройках, чтобы клонированный вами репозиторий не мог переименовать пункты окна выбора. Весь набор задаёт тот из этих трёх источников с наивысшим приоритетом, в котором задан ключ, и Claude Code никогда не объединяет наборы из двух источников.
* **Тип**: объект с массивом строк `options` и необязательным Boolean `replaceBuiltInOptions`
* **По умолчанию**: не задано, поэтому окно выбора показывает встроенный набор

В этом примере после встроенного набора добавляются два развёртывания Bedrock под названиями, знакомыми вашей команде:

```json managed-settings.json theme={null}
{
  "modelPicker": {
    "options": [
      { "model": "us.anthropic.claude-opus-4-8", "label": "Opus (production)" },
      {
        "model": "us.anthropic.claude-sonnet-4-6",
        "label": "Sonnet (production)",
        "description": "Day-to-day work"
      }
    ]
  }
}
```

#### Поля для `modelPicker`

Ключ принимает два поля: одно для самих строк и одно, определяющее, заменяют ли они встроенный набор или дополняют его.

| Поле | Тип | Что делает |
| :- | :- | :- |
| `options` | массив строк, каждая с обязательным `model` и необязательными `label`, `description` и `behavesAs` | Строки, которые показывает окно выбора, в этом порядке, за исключением того, что неактивная строка перемещается вниз. Без `label` Claude Code озаглавливает строку встроенным названием известной ему модели или, в противном случае, ID модели, а без `description` пишет общую вторую строку |
| `replaceBuiltInOptions` | Boolean, по умолчанию `false` | Установите `true`, чтобы показывать только эти строки, **Default** и строку для модели, которую уже использует сессия. Оставьте незаданным, чтобы добавить эти строки после встроенного набора |

Запись в `options` также может содержать необязательную строку `behavesAs` рядом со своим `model`, для чего требуется v2.1.257 или новее. Укажите в ней ID модели, которая уже известна вашей версии Claude Code, например `claude-opus-4-8`, в записи, чей `model` новее вашей версии. Тогда Claude Code применяет к записи возможности и значения effort по умолчанию этой известной модели, вместо того чтобы считать её модель неизвестной. Метка записи и ID модели, который Claude Code отправляет в запросах, не меняются.

При включённом `replaceBuiltInOptions` Claude Code скрывает все остальные строки: встроенный набор, строки, которые он добавляет для записей [`availableModels`](#availablemodels), модели, найденные при [обнаружении через шлюз](https://code.claude.com/docs/ru/llm-gateway-protocol.md#model-discovery), и [`ANTHROPIC_CUSTOM_MODEL_OPTION`](https://code.claude.com/docs/ru/model-config#add-a-custom-model-option). При выключенном Claude Code пропускает указанную модель, которая уже есть во встроенном наборе. Метка меняет то, что показывает окно выбора, а не то, какую модель запускает Claude Code.

Список разрешённых моделей [`availableModels`](#availablemodels) по-прежнему применяется к этим строкам. Прежде чем добавлять указанную модель в список разрешённых, прочитайте раздел [Поведение при объединении](https://code.claude.com/docs/ru/model-config.md#merge-behavior): конкретный ID модели сужает шаблонную запись её семейства. Claude Code также проверяет каждую строку на соответствие сессии, прежде чем показать окно выбора:

* **Удалена**: строка, которую Claude Code не может обслужить, например выведенная из эксплуатации модель или модель, к которой у вашей организации нет доступа
* **Неактивна**: строка, которую вы пока не можете выбрать, показывается с указанием причины
* **Не осталось ни одной строки**: Claude Code сохраняет встроенный набор, отфильтрованный по списку разрешённых моделей как обычно

Claude Code удаляет строку, которую не может разобрать, и сохраняет остальные. См. [Исправление повреждённого файла настроек](https://code.claude.com/docs/ru/settings.md#fix-a-broken-settings-file).

### `modelPricing`

Отображайте расходы по тарифам, которые платит ваша организация, а не по прейскуранту. Задайте это, если у вашей организации есть договорные тарифы, чтобы суммы в долларах, которые видят разработчики, совпадали с вашим счётом. Claude Code применяет тарифы в `/usage`, [строке состояния](https://code.claude.com/docs/ru/statusline.md), `total_cost_usd` в Agent SDK, ограничении [`--max-budget-usd`](https://code.claude.com/docs/ru/cli-reference) и в метрике и событиях стоимости [OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md). Тарифы указываете вы: Claude Code не считывает их из вашего договора или Claude Console. Требуется Claude Code v2.1.242 или новее.

* **Область действия**: [`Managed`](#scopes). Разверните ключ через настройки, управляемые сервером, политику MDM, файл `managed-settings.json` или [вспомогательную программу политики](https://code.claude.com/docs/ru/managed-settings.md#compute-the-policy-with-a-helper-program). Claude Code игнорирует его в пользовательских, проектных и локальных настройках, в `--settings` и в Windows в доступном пользователю для записи [реестре HKCU](https://code.claude.com/docs/ru/managed-settings.md#where-each-mechanism-stores-the-policy). При использовании настроек, управляемых сервером, каждая сессия показывает расходы по прейскуранту, пока [получение настроек](https://code.claude.com/docs/ru/server-managed-settings.md#fetch-and-caching-behavior) этой сессии не подтвердит настройку. Хост-приложение, которое встраивает Claude Code и задаёт [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](https://code.claude.com/docs/ru/env-vars), может передать собственную таблицу через параметр SDK [`managedSettings`](https://code.claude.com/docs/ru/agent-sdk/typescript#options), которую Claude Code использует, только если ни один управляемый источник не задаёт ключ, и только в Claude Code v2.1.246 или новее.
* **Тип**: объект с необязательным `multiplier` и необязательной картой `overrides`
* **По умолчанию**: не задано, поэтому Claude Code показывает расходы по прейскуранту, если хост-приложение не передаёт таблицу

Задайте только `multiplier` для фиксированной скидки или наценки, только `overrides` для тарифов по отдельным моделям или оба.

В этом примере задаются договорные тарифы для Sonnet 4.6, а затем каждая сумма, включая строку Sonnet, уменьшается на 15%:

```json managed-settings.json theme={null}
{
  "modelPricing": {
    "multiplier": 0.85,
    "overrides": {
      "claude-sonnet-4-6": {
        "input": 2.4,
        "output": 12,
        "cacheRead": 0.24,
        "cacheWrite": 3
      }
    }
  }
}
```

Задайте `multiplier` больше 1, но не более 10, чтобы увеличить каждую сумму. Для наценки требуется Claude Code v2.1.271 или новее. Более ранние версии игнорируют `multiplier` больше 1 с предупреждением и сохраняют остальную часть настройки.

Порядок действий, в том числе как убедиться, что тарифы действуют, описан в разделе [Отображение расходов по договорным тарифам](https://code.claude.com/docs/ru/costs.md#report-spend-at-your-contracted-rates).

#### Поля для `modelPricing`

| Поле | Тип | Что делает |
| :- | :- | :- |
| `multiplier` | число больше 0 и не более 10 | Масштабирует каждую стоимость, которую вычисляет Claude Code, независимо от того, покрывает ли её строка `overrides`. Значение меньше 1 — скидка, больше 1 — наценка |
| `overrides` | карта ID модели на объект тарифов с `input`, `output`, `cacheRead` и `cacheWrite`, каждый от 0 до 10000 | Тарифы в долларах США за миллион токенов для этой модели, все четыре обязательны. `cacheWrite` охватывает записи в кэш как на пять минут, так и на один час. См. [К каким моделям применяется строка](#which-models-a-modelpricing-row-applies-to) |

Claude Code использует тарифы строки точно в том виде, в каком вы их записали, не добавляя надбавку за быстрый режим или [тариф для инференса только в США](https://platform.claude.com/docs/en/about-claude/pricing). Если вы также задали `multiplier`, Claude Code применяет его поверх тарифов строки. Claude Code удаляет строку с тарифом, который не может разобрать, или `multiplier`, который не может разобрать, и сохраняет остальное; см. [Исправление повреждённого файла настроек](https://code.claude.com/docs/ru/settings.md#fix-a-broken-settings-file).

#### К каким моделям применяется строка `modelPricing`

Claude Code определяет, к каким моделям применяется строка, по её ключу:

* **ID встроенной модели**: ключ, который сам Claude Code использует для встроенной модели, будь то собственный ID модели, например `claude-sonnet-4-6`, или её ID в Bedrock, Agent Platform или Foundry. Claude Code применяет строку ко всем ID снимков с датами и ID конкретных провайдеров этой модели.
* **Любой другой ключ**: ключ, который не является ID встроенной модели, например псевдоним модели в шлюзе. Claude Code применяет строку только к этому одному ID. Когда ID модели точно совпадает с одним из ваших ключей и также подпадает под строку с ключом ID встроенной модели, Claude Code использует точное совпадение.
* **Профиль инференса приложения Bedrock**: как только Claude Code определил модель, на которую направляет профиль, через вашу карту [`modelOverrides`](#modeloverrides) или [поиск `bedrock:GetInferenceProfile`](https://code.claude.com/docs/ru/amazon-bedrock#iam-configuration), Claude Code применяет к профилю строку этой модели.

### `modelSettings`

Сохраняйте [уровень effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) для каждой используемой модели. Требуется Claude Code v2.1.251 или новее.

В интерактивной сессии на вашем компьютере, когда вы сохраняете `low`, `medium`, `high` или `xhigh` как значение по умолчанию с помощью `/effort` или ползунка effort в окне выбора `/model`, Claude Code записывает этот уровень сюда для используемой модели, поэтому вам редко приходится редактировать этот ключ самостоятельно. Когда вы выбираете один из этих уровней в [окне выбора модели расширения VS Code](https://code.claude.com/docs/ru/vs-code.md#use-the-prompt-box), Claude Code сохраняет его сюда таким же образом. В записи [`effortLevel`](#effortlevel) перечислены сессии, в которых `/effort` применяется только к этой сессии.

Отредактируйте ключ вручную, чтобы изменить или удалить сохранённый уровень.

`effortLevel` модели здесь имеет приоритет над `effortLevel` верхнего уровня ([`effortLevel`](#effortlevel)) в том же файле настроек. Между файлами Claude Code определяет значение для каждой модели отдельно: решает [файл настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence) с наивысшим приоритетом, в котором задан либо `effortLevel` для этой модели, либо `effortLevel` верхнего уровня, который [применяется к этой модели](#effortlevel), поэтому `effortLevel` в управляемых настройках имеет приоритет над уровнем, сохранённым в пользовательских настройках. В разделе [Настройка уровня effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level) перечислено, что ещё может переопределить сохранённый уровень, например `--effort` при запуске.

Чтобы ограничить effort одной модели, а не задать её уровень, добавьте поле [`maxEffortLevel`](#maxeffortlevel) в запись этой модели. Для этого поля требуется Claude Code v2.1.267 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект, сопоставляющий имя модели с объектом, содержащим любые из этих полей:
  * `effortLevel`: одно из значений `"low"`, `"medium"`, `"high"` или `"xhigh"`
  * [`maxEffortLevel`](#maxeffortlevel): наивысший уровень effort, на котором может работать модель
  * `autoCompactWindow`: число токенов от `100000` до `1000000` или `"auto"` для окна, настроенного для модели. [`/autocompact`](https://code.claude.com/docs/ru/model-config#set-the-auto-compact-window) сохраняет значение сюда. Для этой модели значение имеет приоритет над [`autoCompactWindow`](#autocompactwindow) верхнего уровня в том же файле настроек. Требуется Claude Code v2.1.288 или новее
* **По умолчанию**: не задано

Claude Code записывает каждую запись под каноническим именем модели, например `claude-opus-5-5`, и сопоставляет с этой же записью псевдоним модели, ID с суффиксом даты, `[1m]` и распознанные ID конкретных провайдеров.

В этом примере Opus 5.5 остаётся на уровне `high`, а другие модели используют собственные сохранённые уровни или уровни по умолчанию:

```json settings.json theme={null}
{
  "modelSettings": {
    "claude-opus-5-5": {
      "effortLevel": "high"
    }
  }
}
```

Выполните `/effort auto`, чтобы очистить сохранённый уровень для используемой модели. Claude Code оставляет другие записи и любой `effortLevel` верхнего уровня без изменений.

### `outputStyle`

Выберите [стиль вывода](https://code.claude.com/docs/ru/output-styles.md) по имени. Стиль вывода — это сохранённый набор инструкций, который меняет роль, тон и формат вывода Claude, например встроенные стили Explanatory и Learning или стиль, который вы написали сами.

Если изменить этот ключ во время сессии, Claude использует новый стиль начиная с вашего следующего сообщения. О том, во что это сообщение обходится с точки зрения кэширования промптов, см. [Изменение стиля вывода](https://code.claude.com/docs/ru/prompt-caching.md#changing-output-style). До v2.1.251 изменение применялось только после выполнения `/clear` или запуска новой сессии.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, имя [встроенного](https://code.claude.com/docs/ru/output-styles.md#built-in-output-styles) или [пользовательского](https://code.claude.com/docs/ru/output-styles.md#create-a-custom-output-style) стиля вывода
* **По умолчанию**: не задано, поэтому Claude Code использует стиль по умолчанию

В этом примере выбран встроенный стиль Explanatory, который добавляет обучающие пояснения между задачами:

```json settings.json theme={null}
{
  "outputStyle": "Explanatory"
}
```

### `promptCacheTtl`

Выберите, как долго [кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md) хранит основной диалог. Этот ключ применяется к вашим ходам в интерактивном режиме, с `-p` и в Agent SDK, а также к вспомогательным запросам, которые Claude Code выполняет вместе с ними. Время жизни в один час сохраняет кэш «тёплым» на протяжении более длинных перерывов, а API [тарифицирует каждую запись в кэш по более высокой ставке](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing), чем при времени жизни в пять минут. Требуется Claude Code v2.1.242 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"5m"`: кэш хранится пять минут
  * `"1h"`: кэш хранится один час
* **По умолчанию**: не задано, поэтому каждый запрос основного диалога получает [своё время жизни по умолчанию](https://code.claude.com/docs/ru/prompt-caching.md#which-ttl-each-request-gets)
* **Переопределения для сессии**: [`FORCE_PROMPT_CACHING_5M`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над всем остальным, затем [`CLAUDE_CODE_PROMPT_CACHE_TTL`](https://code.claude.com/docs/ru/env-vars), затем этот ключ и в последнюю очередь [`ENABLE_PROMPT_CACHING_1H`](https://code.claude.com/docs/ru/env-vars)

В этом примере основной диалог использует время жизни в один час, а субагенты остаются на пяти минутах:

```json settings.json theme={null}
{
  "promptCacheTtl": "1h",
  "subagentPromptCacheTtl": "5m"
}
```

О стоимости каждого времени жизни см. [Время жизни кэша](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime).

### `showThinkingSummaries`

Просматривайте сводки [расширенного мышления](https://code.claude.com/docs/ru/model-config.md#extended-thinking) Claude в интерактивных сессиях. Задайте это, если хотите видеть полные сводки при раскрытии размышлений с помощью `Ctrl+O`. Если значение не задано или равно `false`, Anthropic API скрывает блоки размышлений, и Claude Code показывает свёрнутую заглушку.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: вы видите полные сводки размышлений при их раскрытии с помощью `Ctrl+O`
  * `false`: Anthropic API скрывает блоки размышлений, и Claude Code показывает свёрнутую заглушку
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "showThinkingSummaries": true
}
```

Скрытие меняет только то, что вы видите, а не то, что генерирует модель. Чтобы сократить расходы на мышление, вместо этого [уменьшите бюджет или отключите мышление](https://code.claude.com/docs/ru/model-config.md#extended-thinking).

### `subagentPromptCacheTtl`

Выберите, как долго [кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md) хранит запросы, которые Claude Code выполняет вне основного диалога. Этот ключ применяется к [субагентам](https://code.claude.com/docs/ru/sub-agents.md), [рабочим процессам](https://code.claude.com/docs/ru/workflows.md) и собственным фоновым и вспомогательным запросам Claude Code, например для сжатия контекста и названий сессий. Время жизни в один час сохраняет кэш «тёплым» на протяжении более длинных перерывов, а API [тарифицирует каждую запись в кэш по более высокой ставке](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing), чем при времени жизни в пять минут. Требуется Claude Code v2.1.242 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"5m"`: кэш хранится пять минут
  * `"1h"`: кэш хранится один час
* **По умолчанию**: не задано, поэтому каждый из этих запросов получает [своё время жизни по умолчанию](https://code.claude.com/docs/ru/prompt-caching.md#which-ttl-each-request-gets)
* **Переопределения для сессии**: [`FORCE_PROMPT_CACHING_5M`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над всем остальным, затем [`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`](https://code.claude.com/docs/ru/env-vars), затем этот ключ, затем [`ENABLE_PROMPT_CACHING_1H`](https://code.claude.com/docs/ru/env-vars), который запрашивает время жизни в один час для каждого запроса. О том, какое место занимает значение из собственного frontmatter субагента, см. [Самостоятельный выбор TTL](https://code.claude.com/docs/ru/prompt-caching.md#choose-the-ttl-yourself)

В этом примере субагенты и другие запросы вне основного диалога получают время жизни в один час:

```json settings.json theme={null}
{
  "subagentPromptCacheTtl": "1h"
}
```

Этот ключ охватывает запросы, которые не охватывает [`promptCacheTtl`](#promptcachettl), поэтому задайте оба, чтобы выбрать время жизни для каждого запроса, который выполняет Claude Code. О том, чем кэш субагента отличается от кэша основного диалога, см. [Субагенты и кэш](https://code.claude.com/docs/ru/prompt-caching.md#subagents-and-the-cache).

### `switchModelsOnFlag`

Выберите, что происходит, когда [классификатор безопасности помечает запрос](https://code.claude.com/docs/ru/model-config.md#automatic-model-fallback): переключиться на резервную модель и продолжить или приостановиться, чтобы вы могли выбрать между переключением и редактированием промпта.

* **Область действия**: [`Any file`](#scopes). В `/config` отображается как **Switch models when a message is flagged** с вариантами **Switch automatically** и **Ask each time**.
* **Тип**: Boolean
  * `true`: Claude Code переключается на резервную модель и продолжает
  * `false`: в интерактивной сессии Claude Code приостанавливается, чтобы вы могли выбрать между переключением и редактированием промпта; там, где диалоговое окно показать нельзя, например при запуске с `-p`, помеченный запрос завершается ошибкой
* **По умолчанию**: не задано. Claude Code переключается автоматически, хотя в интерактивной сессии может [сначала спросить](https://code.claude.com/docs/ru/model-config.md#ask-before-switching)

```json settings.json theme={null}
{
  "switchModelsOnFlag": false
}
```

См. [Запрос перед переключением](https://code.claude.com/docs/ru/model-config.md#ask-before-switching).

### `ultracode`

Запускайте сессии с включённым [ultracode](https://code.claude.com/docs/ru/workflows.md#let-claude-decide-with-ultracode). Когда он включён, Claude планирует рабочий процесс для каждой существенной задачи, не дожидаясь вашей просьбы. Claude планирует рабочие процессы, только если для вас включены [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md) и ваша модель поддерживает effort `xhigh`. Ключ не меняет уровень effort сессии: ultracode работает на том уровне, который использует сессия. Claude Code читает этот ключ, но никогда его не записывает: `/effort ultracode` включает ultracode только для текущей сессии.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: сессии запускаются с включённым ultracode, если для вас включены динамические рабочие процессы и ваша модель поддерживает `xhigh`
  * `false`: сессии запускаются с выключенным ultracode
* **По умолчанию**: не задано, поэтому ultracode выключен
* **Переопределения для сессии**: `/effort ultracode` включает ultracode для одной сессии без этого ключа, а `/effort ultracode off` выключает его для одной сессии, когда этот ключ равен `true`. Флаг `--effort ultracode` также включает его для одной сессии с effort `xhigh`

```json settings.json theme={null}
{
  "ultracode": true
}
```

Уровень effort сессии определяется [`effortLevel`](#effortlevel), [`modelSettings`](#modelsettings) и другими [источниками effort](https://code.claude.com/docs/ru/model-config.md#adjust-effort-level), а [ограничение effort](https://code.claude.com/docs/ru/model-config.md#organization-effort-limits), например [`maxEffortLevel`](#maxeffortlevel), понижает этот уровень, не выключая ultracode. Для этого и для формы `/effort ultracode off` требуется Claude Code v2.1.284 или новее. До v2.1.284 `ultracode: true` запускал сессию с effort `xhigh`, а ограничение effort ниже `xhigh` оставляло ultracode выключенным. Управляющий запрос `apply_flag_settings` в Agent SDK также принимает этот ключ.

## Настройки разрешений

Решите, что Claude может делать без запроса, какой режим разрешений используется по умолчанию для новых сессий и что позволяет классификатор авторежима. Синтаксис правил и модель разрешений см. в разделе [Настройка разрешений](https://code.claude.com/docs/ru/permissions.md).

### `allowManagedPermissionRulesOnly`

Сделайте управляемые настройки единственным источником правил разрешений среди настроек. Claude Code затем игнорирует правила `allow`, `ask` и `deny` в пользовательских, проектных, локальных файлах и файлах `--settings`, игнорирует `--allowedTools`, скрывает варианты «всегда разрешать» в запросах разрешений и прекращает сохранение новых правил.

Когда применяются [родительские настройки от хоста встраивания](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy), Claude Code рассматривает их как часть управляемого уровня. Он отбрасывает их правила `allow` и `additionalDirectories` и сохраняет их правила `deny` и `ask`, кроме правил `Read` и `Edit`, шаблон которых начинается с `!`. Хост не может исключить пути из управляемых правил с помощью правила `!`, независимо от того, установлен ли этот ключ.

Правила `--disallowedTools` и правила `deny` и `ask` текущей сессии по-прежнему применяются, в том числе после перезагрузки настроек Claude Code посреди сессии. Они только ограничивают, поэтому не могут расширить то, что разрешают управляемые правила. До версии 2.1.257 Claude Code отбрасывал эти правила командной строки и сессии при первой перезагрузке настроек.

О том, что может исключить шаблон `!` в правиле `--disallowedTools` или в правиле сессии, см. [Правила Read и Edit](https://code.claude.com/docs/ru/permissions.md#read-and-edit).

Когда вы устанавливаете этот ключ, Claude Code v2.1.282 или новее также игнорирует frontmatter [`allowed-tools`](https://code.claude.com/docs/ru/skills#pre-approve-tools-for-a-skill) в скиллах и файлах `.claude/commands/` из следующих источников:

* Каталог `.claude/` репозитория
* Ваши каталоги `~/.claude/skills/` и `~/.claude/commands/`, включая [скиллы, синхронизированные из claude.ai](https://code.claude.com/docs/ru/skills.md#where-synced-skills-load)
* Каталог, добавленный через `--add-dir`
* [Плагины, объявленные манифестом `.claude-plugin`](https://code.claude.com/docs/ru/plugins/loading#plugins-shared-through-a-repository), внутри `~/.claude/skills/` или `.claude/skills/` проекта
* Плагины, загруженные только для одной сессии, идентификаторы которых оканчиваются на [`@inline`](https://code.claude.com/docs/ru/plugins/loading#find-where-a-plugin-came-from), когда выполняются все следующие условия:
  * Сессия является [сессией Code](https://code.claude.com/docs/ru/desktop.md#environment-configuration) или [сессией Cowork](https://code.claude.com/docs/ru/managed-settings.md#where-and-when-a-policy-applies), кроме облачной сессии, для которой само приложение Claude Desktop запускает Claude Code
  * Ключ задан в ваших управляемых настройках, а не только в [родительских настройках](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy) хоста встраивания
  * Сессия работает на Claude Code v2.1.305 или новее

Скиллы из управляемых настроек и встроенные скиллы сохраняют свои `allowed-tools`. Плагины `@inline` вне этих сессий Desktop также сохраняют свои, кроме плагина с именем [`anthropic-skills`](https://code.claude.com/docs/ru/skills#names-reserved-for-synced-skills). Поле `disallowed-tools` скилла по-прежнему применяется. О том, что видит разработчик, когда Claude Code игнорирует это поле, см. [Когда применяются только управляемые правила разрешений](https://code.claude.com/docs/ru/skills.md#when-only-managed-permission-rules-apply).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: Boolean
  * `true`: управляемые настройки становятся единственным источником правил разрешений среди настроек
  * `false`: Claude Code применяет правила разрешений из пользовательских, проектных, локальных файлов и файлов `--settings` в дополнение к управляемым
* **По умолчанию**: не установлено, поэтому Claude Code применяет правила разрешений из пользовательских, проектных и локальных настроек, а также из `--settings`, в дополнение к управляемым

```json managed-settings.json theme={null}
{
  "allowManagedPermissionRulesOnly": true
}
```

Этот ключ не фиксирует список разрешённых MCP-серверов; для этого установите [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly). См. [Настройки только для управляемого уровня](https://code.claude.com/docs/ru/managed-settings.md#managed-only-settings).

### `autoMode`

Добавьте собственные правила к тому, что блокирует и разрешает классификатор [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode). Используйте его, чтобы сообщить классификатору, каким репозиториям, бакетам и доменам доверяет ваша организация, чтобы он перестал блокировать рутинные внутренние операции. Классификатор поставляется со [встроенными разрешающими и запрещающими правилами](https://code.claude.com/docs/ru/auto-mode-config.md#inspect-the-defaults-and-your-effective-config). Включайте буквальную строку `"$defaults"` в каждый задаваемый вами массив, чтобы ваши правила добавлялись к встроенным. Если её опустить, ваши правила [могут заменить встроенные](https://code.claude.com/docs/ru/auto-mode-config.md#override-the-block-and-allow-rules).

* **Область действия**: [`User or managed`](#scopes)
* **Тип**: объект с массивами правил в свободной форме `environment`, `allow`, `soft_deny` и `hard_deny`, а также Boolean [`classifyAllShell`](#automode-classifyallshell)
* **По умолчанию**: не установлено, поэтому классификатор использует только свои [встроенные правила](https://code.claude.com/docs/ru/auto-mode-config.md#inspect-the-defaults-and-your-effective-config)

Этот пример сохраняет встроенные правила `soft_deny` и добавляет ещё одно, которое блокирует `terraform apply`:

```json settings.json theme={null}
{
  "autoMode": {
    "soft_deny": ["$defaults", "Never run terraform apply"]
  }
}
```

Когда один и тот же массив задан в нескольких из этих файлов, Claude Code объединяет записи. О формате правил и о том, как применяется каждый массив, см. [Настройка авторежима](https://code.claude.com/docs/ru/auto-mode-config.md).

### `autoMode.classifyAllShell`

Отправляйте каждую команду Bash и PowerShell через классификатор авторежима, пока авторежим активен. По умолчанию авторежим приостанавливает только разрешающие правила, которые могут запускать произвольный код: правила на весь инструмент и правила с подстановочными знаками, такие как `Bash(*)`, а также префиксы интерпретаторов или обёрток оболочки, такие как `Bash(python *)`. Команда, которой соответствует любое другое разрешающее правило, например `Bash(npm test)`, минует классификатор, если только у неё нет [разрешённых доменов для отдельной команды](https://code.claude.com/docs/ru/sandboxing.md#per-command-allowed-domains-in-auto-mode). Когда команда минует классификатор, деструктивный аргумент, который префикс правила не предусмотрел, может пройти незамеченным. Установка этого ключа приостанавливает все разрешающие правила для оболочки на время сессии, чтобы классификатор видел каждую команду. Требуется Claude Code v2.1.193 или новее.

* **Область действия**: [`User or managed`](#scopes). Читается везде, где читается [`autoMode`](#automode).
* **Тип**: Boolean
  * `true`: пока авторежим активен, Claude Code отправляет каждую команду Bash и PowerShell через классификатор и приостанавливает ваши разрешающие правила для оболочки; вне авторежима правила по-прежнему применяются
  * `false`: авторежим приостанавливает только разрешающие правила, которые могут запускать произвольный код, такие как `Bash(*)` и `Bash(python *)`; команда, которой соответствует любое другое разрешающее правило, минует классификатор, если только у неё нет [разрешённых доменов для отдельной команды](https://code.claude.com/docs/ru/sandboxing.md#per-command-allowed-domains-in-auto-mode), а все остальные shell-команды проходят через него
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

В сессии Code Mode этот ключ работает иначе. См. [Приостановка разрешающих правил для оболочки](https://code.claude.com/docs/ru/auto-mode-config.md#route-all-shell-commands-through-the-classifier).

### `disableAutoMode`

Удалите [авторежим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) из цикла `Shift+Tab`. Любая сессия, которая в противном случае [начиналась бы в авторежиме](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in), будь то из-за `--permission-mode auto`, файла настроек или встроенного значения по умолчанию, вместо этого начинается в `default`. Администраторы задают этот ключ в управляемых настройках, чтобы запретить разработчикам своей организации использовать авторежим.

* **Область действия**: [`Any file`](#scopes). Наиболее полезен в [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md), где пользователи не могут его переопределить. Также принимается внутри `permissions` как `permissions.disableAutoMode`.
* **Тип**: строка `"disable"`
* **По умолчанию**: не установлено

```json settings.json theme={null}
{
  "disableAutoMode": "disable"
}
```

### `permissions`

Управляйте тем, какие инструменты Claude может использовать без запроса, какие вызывают запрос подтверждения, а какие заблокированы. Также задайте [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) по умолчанию для новых сессий. Все ключи `permissions.*` ниже вложены в этот объект.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект с `allow`, `ask`, `deny`, `additionalDirectories`, `blockReadsOutsideWorkingDirectories`, `blockWritesOutsideWorkingDirectories`, `defaultMode`, `denyInsteadOfPrompting`, `disableBypassPermissionsMode` и `disableAutoMode`
* **По умолчанию**: не установлено

Этот пример разрешает команды `npm run` без запроса, запрашивает подтверждение перед `git push`, блокирует чтение `.env` и запускает сессии в `acceptEdits`:

```json settings.json theme={null}
{
  "permissions": {
    "allow": ["Bash(npm run *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)"],
    "defaultMode": "acceptEdits"
  }
}
```

Три массива правил используют один синтаксис; см. [Синтаксис правил разрешений](#permission-rule-syntax) в разделе `permissions.allow`. О том, как объединяются правила разрешений из разных файлов, см. [как правила разрешений объединяются между областями действия](https://code.claude.com/docs/ru/permissions.md#settings-precedence); о том, как объединяются ключи настроек в целом, см. [Приоритет настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence) в руководстве по настройкам.

### `useAutoModeDuringPlan`

Выберите, использует ли Claude Code классификатор авторежима для проверки shell-команд в режиме планирования. При значении по умолчанию `true` классификатор проверяет каждую команду во время планирования, когда авторежим доступен, и вы не видите запроса, за исключением [удалений критических путей](https://code.claude.com/docs/ru/permission-modes.md#critical-paths). Установите `false`, чтобы получать запрос разрешения для каждой команды вне встроенного набора команд только для чтения. Отображается в `/config` как **Use auto mode during plan**.

* **Область действия**: [`User, local, or managed`](#scopes).
  * Значение `false` в любом из этих файлов или в `--settings` отключает его, если только вы не исключите этот пользовательский или локальный файл с помощью такого параметра, как [`--setting-sources`](https://code.claude.com/docs/ru/cli-reference#cli-flags). Игнорирование исключённого файла требует Claude Code v2.1.314 или новее
* **Тип**: Boolean
  * `true`: то же, что и отсутствие значения; когда авторежим доступен, классификатор проверяет shell-команды во время планирования
  * `false`: вы получаете запрос разрешения для каждой команды вне встроенного набора команд только для чтения
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "useAutoModeDuringPlan": false
}
```

### `permissions.allow`

Перечислите использования инструментов, которые Claude Code одобряет без запроса. В правиле MCP `*` может встречаться только в имени инструмента после префикса `mcp__<server>__`, например `mcp__github__get_*`; в имени сервера он встречаться не может.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: массив строк правил разрешений
* **По умолчанию**: не установлено
* **Переопределения для отдельной сессии**: `--allowedTools` добавляет разрешающие правила на одну сессию, а запрещающее правило из любого файла настроек по-прежнему блокирует указанный в нём инструмент

Этот пример разрешает `git diff` и позволяет Claude Code читать ваш `.zshrc` без запроса:

```json settings.json theme={null}
{
  "permissions": {
    "allow": ["Bash(git diff *)", "Read(~/.zshrc)"]
  }
}
```

Claude Code применяет правила `allow` из `.claude/settings.json` проекта только после того, как вы подтвердите [диалоговое окно доверия рабочему пространству](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust) для этой папки.

#### Синтаксис правил разрешений

Правила разрешений имеют формат `Tool` или `Tool(specifier)`. Claude Code сначала проверяет правила `deny`, затем `ask`, затем `allow`, и решение принимает первое совпадение, независимо от того, насколько конкретно каждое правило; см. [порядок проверки правил разрешений](https://code.claude.com/docs/ru/permissions.md#manage-permissions).

Каждая строка показывает одну форму правила и то, чему она соответствует.

| Правило | Чему соответствует |
| :- | :- |
| `Bash` | Каждая команда Bash |
| `Bash(npm run *)` | Команды, начинающиеся с `npm run` |
| `Read(./.env)` | Чтение файла `.env` |
| `WebFetch(domain:example.com)` | Запросы на загрузку с example.com |

Полный синтаксис правил, включая поведение подстановочных знаков, шаблоны для конкретных инструментов в правилах Read, Edit, WebFetch, MCP и Agent, а также ограничения безопасности шаблонов Bash, см. в разделе [Синтаксис правил разрешений](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax).

### `permissions.ask`

Перечислите использования инструментов, для которых у вас запрашивается подтверждение даже в режиме разрешений, который иначе одобрил бы их, например `acceptEdits` или `bypassPermissions`. В режиме `dontAsk` Claude Code отклоняет соответствующее использование инструмента вместо запроса.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: массив строк правил разрешений
* **По умолчанию**: не установлено

```json settings.json theme={null}
{
  "permissions": {
    "ask": ["Bash(git push *)"]
  }
}
```

### `permissions.deny`

Перечислите использования инструментов, которые Claude Code блокирует. Используйте этот ключ для файлов, содержащих API-ключи, секреты или значения окружения: Claude Code исключает соответствующие файлы из обнаружения файлов и результатов поиска, запрещает их чтение и блокирует [инструменты Edit и Write](https://code.claude.com/docs/ru/permissions.md#read-and-edit) для соответствующих путей.

Запрещающие правила Read и Edit применяются к встроенным файловым инструментам Claude, к файловым командам, которые Claude Code распознаёт в Bash, таким как `cat`, `head`, `tail`, `sed` и `tee`, и к целям [перенаправлений](https://code.claude.com/docs/ru/permissions.md#redirections) Bash, таких как `> file` и `< file`; они не применяются к команде, которая читает файлы, не называя их, например `grep -r pattern .`, или к произвольным подпроцессам, поэтому для принудительного контроля на уровне ОС [включите песочницу](https://code.claude.com/docs/ru/sandboxing.md).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: массив строк правил разрешений
* **По умолчанию**: не установлено
* **Переопределения для отдельной сессии**: `--disallowedTools` добавляет запрещающие правила на одну сессию наряду с этим ключом

Этот пример запрещает чтение файлов `.env`, каталога `secrets` и файла учётных данных, а также блокирует команды `curl`:

```json settings.json theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Bash(curl *)"
    ]
  }
}
```

Имена инструментов поддерживают glob-шаблоны, поэтому `"*"` запрещает все инструменты, а `"mcp__*"` запрещает все MCP-инструменты. Claude Code игнорирует запрещающее правило для инструмента [`EndConversation`](https://code.claude.com/docs/ru/tools-reference#endconversation-tool-behavior), пока Claude доступен хотя бы один другой инструмент. Запрещающее правило `Bash` сопоставляется с командой в том виде, в каком её пишет Claude, поэтому `Bash(curl *)` не останавливает `/usr/bin/curl` или `sh -c 'curl …'`; см. [чему не соответствует правило Bash](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits). Этот ключ заменяет устаревшую конфигурацию `ignorePatterns`.

### `permissions.additionalDirectories`

Предоставьте Claude доступ к файлам в каталогах за пределами того, в котором вы начали работу, в качестве дополнительных [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories). Большая часть конфигурации `.claude/` из этих каталогов [не обнаруживается](https://code.claude.com/docs/ru/permissions.md#additional-directories-grant-file-access-not-configuration).

* **Область действия**: [`Any file`](#scopes), с [ограничениями на доступ на запись в песочнице](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox), который дают записи из проектных и локальных настроек
* **Тип**: массив путей к каталогам
* **По умолчанию**: не установлено
* **Переопределения для отдельной сессии**: `--add-dir` и `/add-dir` добавляют каталоги на одну сессию наряду с этим ключом

```json settings.json theme={null}
{
  "permissions": {
    "additionalDirectories": ["../docs/"]
  }
}
```

Как и правила `allow`, записи в `.claude/settings.json` проекта вступают в силу только после того, как вы подтвердите [диалоговое окно доверия рабочему пространству](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust) для этой папки.

### `permissions.blockReadsOutsideWorkingDirectories`

Заставьте файловые инструменты Claude отказывать в чтении за пределами ваших [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories) в любом режиме разрешений, включая `bypassPermissions`. Claude Code отклоняет вызовы `Read`, `Grep`, `Glob` и `LSP` для таких путей и сообщает Claude, чтобы он попросил вас добавить каталог с помощью `/add-dir`. Файлы, которые нужны самому Claude Code, остаются доступными для чтения, например ваши скиллы, плагины, правила, агенты, команды и файл памяти `CLAUDE.md` в `~/.claude/`. Требуется Claude Code v2.1.257 или новее.

Shell-команды Claude Code не отклоняет таким же образом:

* В разделе [Действия, которые не одобряет автоматически ни один режим](https://code.claude.com/docs/ru/permission-modes.md#actions-no-mode-auto-approves) описано, когда shell-команда, читающая такой путь, вызывает запрос к вам
* В разделе [Команды в песочнице при действующей блокировке](#sandboxed-commands-under-the-block) описано, что может читать команда в песочнице

Команда Bash, которую парсер оболочки не может отследить, например команда, которая меняет каталог более одного раза или запускает подоболочку, вызывает запрос к вам даже в авторежиме и в режиме `bypassPermissions`. Запрос появляется, даже если команда не называет ни одного пути за пределами рабочих каталогов. Этот запрос не появляется, когда команда выполняется в [песочнице](https://code.claude.com/docs/ru/sandboxing.md) и песочница обеспечивает блокировку.

Claude Code также записывает сюда `true`, когда вы выбираете блокировку такого чтения в [запросе авторежима перед первым чтением за пределами рабочих каталогов](https://code.claude.com/docs/ru/permission-modes.md#first-read-outside-the-working-directories).

* **Область действия**: [`Any file`](#scopes). Значение `true` в любом файле применяется, поэтому репозиторий может включить блокировку для себя, но не может снять вашу.
* **Тип**: Boolean
  * `true`: файловые инструменты Claude отказывают в чтении за пределами рабочих каталогов
  * `false`: то же, что и отсутствие значения; блокировка всё равно применяется, если другой файл устанавливает `true`
* **По умолчанию**: не установлено, поэтому чтение за пределами рабочих каталогов подчиняется вашему [режиму разрешений](https://code.claude.com/docs/ru/permission-modes.md)

```json settings.json theme={null}
{
  "permissions": {
    "blockReadsOutsideWorkingDirectories": true
  }
}
```

Чтобы снять блокировку, удалите ключ из всех файлов настроек, которые его устанавливают, затем перезапустите каждую запущенную сессию.

Каталоги, которые вы добавляете с помощью `--add-dir`, `/add-dir` или `additionalDirectories` в пользовательских или управляемых настройках, считаются рабочими каталогами для блокировки. Каталоги, добавленные только в настройках репозитория, не считаются: те, что указаны в `.claude/settings.json`, и те, что указаны в `.claude/settings.local.json`, если только git не сообщает, что этот файл не отслеживается. В каталоге, который не является git-репозиторием, или когда git отслеживает этот файл, Claude Code рассматривает `.claude/settings.local.json` как настройки репозитория, поэтому каталоги, которые должны оставаться доступными для чтения, указывайте в пользовательских настройках.

Когда [`autoMemoryDirectory`](#automemorydirectory) задан в `.claude/settings.json` проекта или в `.claude/settings.local.json`, [рассматриваемом как предоставленный репозиторием](https://code.claude.com/docs/ru/permissions.md#when-your-local-settings-file-needs-trust), Claude Code не загружает [автоматическую память](https://code.claude.com/docs/ru/memory.md#storage-location) из этого каталога и ничего в него не сохраняет.

#### Команды в песочнице при действующей блокировке

Когда [изоляция в песочнице](https://code.claude.com/docs/ru/sandboxing.md) включена, блокировка также распространяется на команды в песочнице. Claude Code запрещает им чтение вашего домашнего каталога и других корневых каталогов, содержащих пользовательские файлы: `/Users`, `/home`, `/root`, `/Volumes`, `/mnt`, `/media`, `/run/media` и `/srv`. Затем он снова открывает рабочие каталоги, [worktree](https://code.claude.com/docs/ru/worktrees.md), которые Claude Code создаёт в сессии, временный каталог сессии и те части `~/.claude`, которые нужны командам, например скиллы и плагины. Пока блокировка действует, записи `allowRead` и `allowWrite` из настроек репозитория не учитываются.

Когда рабочий каталог сессии является связанным [git worktree](https://code.claude.com/docs/ru/worktrees.md), в том числе таким, в который Claude Code перешёл посреди сессии, общий каталог `.git` репозитория остаётся доступным для чтения и записи командам в песочнице, чтобы git продолжал там работать.

В следующих случаях блокировка не распространяется на команды в песочнице, тогда как файловые инструменты Claude продолжают её соблюдать:

* Изоляция файловой системы отключена через [`sandbox.filesystem.disabled`](#sandbox-filesystem-disabled)
* Установлен [`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly)
* Путь к каталогу, в котором вы запустили Claude Code, содержит glob-символ, например `*`, `?` или `[`

При действующей блокировке Claude Code снова открывает командам в песочнице ваши глобальные файлы конфигурации git, чтобы `git` сохранял ваши идентификационные данные и настройки:

* `~/.gitconfig`
* Файлы `config`, `ignore` и `attributes` в `$XDG_CONFIG_HOME/git`, который по умолчанию равен `~/.config/git`
* Файлы, на которые ваша глобальная конфигурация git ссылается через `[include]`, `[includeIf]`, `core.excludesFile` или `core.attributesFile`

Claude Code оценивает каждый файл отдельно. Когда файл находится там, куда команда в песочнице может писать, напрямую или через символическую ссылку, Claude Code не открывает снова файлы, на которые он ссылается.

В Linux и WSL2 файл конфигурации, являющийся символической ссылкой, может оставаться недоступным для чтения по собственному пути, и тогда `git` работает без него. `~/.git-credentials` и `$XDG_CONFIG_HOME/git/credentials` остаются заблокированными.

Если снова открытый файл содержит секрет, например токен `http.extraHeader`, добавьте его путь в [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread). Запись `denyRead`, охватывающая файл, всегда имеет приоритет над этим повторным открытием.

### `permissions.blockWritesOutsideWorkingDirectories`

Заставьте инструменты `Write`, `Edit` и `NotebookEdit` отказывать в работе с путями за пределами ваших [рабочих каталогов](https://code.claude.com/docs/ru/permissions.md#working-directories) в любом режиме разрешений, включая `bypassPermissions`, за исключением [некоторых собственных файлов Claude Code](#what-the-write-block-refuses-and-what-stays-writable). Ключ не ограничивает shell-команды, MCP-инструменты или программы, которые запускают хуки. Чтобы ограничить, куда пишут shell-команды, включите [изоляцию в песочнице](https://code.claude.com/docs/ru/sandboxing.md). Требуется Claude Code v2.1.314 или новее.

Когда ключ включён, Claude Code также удаляет инструменты `EnterWorktree` и `ExitWorktree` или отклоняет их вызовы. Чтобы продолжить работу в worktree, следуйте инструкциям из раздела [У Claude нет инструмента `EnterWorktree`](https://code.claude.com/docs/ru/worktrees#claude-has-no-enterworktree-tool).

* **Область действия**: [`Any file`](#scopes). Значение `true` в любом файле, который загружает сессия, применяется, поэтому репозиторий может включить блокировку для себя, но не может снять вашу. В [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) Claude Code может не применять этот ключ, поскольку файловые инструменты работают в контейнере, который сам является границей.
* **Тип**: Boolean
  * `true`: включает блокировку
  * `false`: то же, что и отсутствие значения; блокировка всё равно применяется, если другой файл устанавливает `true`
* **По умолчанию**: не установлено, поэтому запись за пределами рабочих каталогов подчиняется вашему [режиму разрешений](https://code.claude.com/docs/ru/permission-modes.md). Блокировка также включена, пока Claude Code не может прочитать объект `permissions` в ваших [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md#keys-that-fail-closed).

```json settings.json theme={null}
{
  "permissions": {
    "blockWritesOutsideWorkingDirectories": true
  }
}
```

Чтобы проверить блокировку, попросите Claude с помощью инструмента Write создать файл за пределами ваших рабочих каталогов, например `~/block-test.txt`, если ваш домашний каталог не входит в их число. Claude Code отклонит вызов, а в сообщении об отказе будет сказано, что [настройка блокирует запись за пределами рабочих каталогов](https://code.claude.com/docs/ru/errors.md#setting-blocks-writes-outside-the-working-directories).

Чтобы снять блокировку, удалите ключ из всех файлов настроек, которые его устанавливают, затем перезапустите Claude Code.

#### Что запрещает блокировка записи и что остаётся доступным для записи

Некоторые собственные файлы Claude Code остаются доступными для записи, например файлы планов, [scratchpad](https://code.claude.com/docs/ru/claude-directory.md#session-scratchpad-directory), каталог `tmp` [фоновой сессии](https://code.claude.com/docs/ru/agent-view.md) и файлы `.md` в [автоматической памяти](https://code.claude.com/docs/ru/memory.md#storage-location) этого проекта.

Помимо ваших собственных файлов за пределами рабочих каталогов, блокировка запрещает запись в:

* **Файлы настроек Claude Code**: Claude Code [отклоняет такую запись](https://code.claude.com/docs/ru/errors.md#writes-to-claude-code-settings-files-are-blocked) и внутри рабочих каталогов, поскольку файл настроек может снять блокировку. Редактируйте файлы настроек самостоятельно.
* **Каталог, который добавляют только настройки репозитория**: каталог, который [`additionalDirectories`](#permissions-additionaldirectories) перечисляет только в `.claude/settings.json` или в `.claude/settings.local.json`, если только git не сообщает, что этот файл не отслеживается
* **Worktree субагента**: редактирование файлов субагентом с [`isolation: worktree`](https://code.claude.com/docs/ru/worktrees#isolate-subagents-with-worktrees) отклоняется, когда его worktree находится за пределами рабочих каталогов
* **Автоматическую память в каталоге, выбранном репозиторием**: каталог, который [`autoMemoryDirectory`](#automemorydirectory) указывает в настройках репозитория

Запись в файлы настроек остаётся запрещённой, что бы вы ни добавили. Чтобы разрешить запись в любом из остальных случаев, [добавьте рабочий каталог](#let-one-directory-through-the-read-or-write-block). `/add-dir` требует существующего каталога, поэтому для worktree субагентов укажите каталог `.claude/worktrees` в корне репозитория.

#### Пропуск одного каталога через блокировку чтения или записи

Чтобы Claude мог обращаться к одному каталогу за пределами проекта, пока `blockReadsOutsideWorkingDirectories` или `blockWritesOutsideWorkingDirectories` имеет значение `true`, добавьте его как рабочий каталог. Выполните `/add-dir <directory>` в сессии, передайте `--add-dir <directory>` при запуске Claude Code или укажите его в `additionalDirectories` в пользовательских или управляемых настройках. Никакое [разрешающее правило](https://code.claude.com/docs/ru/permissions.md#read-and-edit) не пропускает файловые инструменты Claude через любую из этих блокировок.

### `permissions.defaultMode`

Задайте [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) по умолчанию для новых сессий. Если оставить ключ не установленным, применяется [встроенный режим по умолчанию](https://code.claude.com/docs/ru/permission-modes.md#which-mode-a-session-starts-in) для вашего интерфейса.

* **Область действия**: [`Any file`](#scopes). `auto` и `bypassPermissions` не вступают в силу из проектных или локальных настроек, поэтому задавайте их в `~/.claude/settings.json`. До версии 2.1.257 `bypassPermissions` вступал в силу из любого файла. Для диалогов, которые запускает расширение VS Code, Claude Code читает только пользовательские, управляемые значения и значения `--settings`.
* **Тип**: строка, одно из значений:
  * `"default"`: Claude Code без запроса выполняет только чтение
  * `"acceptEdits"`: Claude Code также без запроса выполняет редактирование файлов и распространённые команды файловой системы, такие как `mkdir` и `mv`
  * `"plan"`: Claude Code читает и планирует, но блокирует редактирование, пока вы не утвердите план
  * `"auto"`: Claude Code работает без рутинных запросов; перед выполнением таких действий, как shell-команды и сетевые запросы, фоновый классификатор проверяет, что они соответствуют вашей задаче
  * `"dontAsk"`: Claude Code автоматически отклоняет каждый вызов, который иначе потребовал бы запроса, хотя установленный вами [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md) по-прежнему может одобрить [некоторые из этих вызовов](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods). Чтение файлов внутри ваших рабочих каталогов, другие действия, не требующие подтверждения, и заранее разрешённые инструменты по-прежнему выполняются, за исключением чтения по [сетевым путям](https://code.claude.com/docs/ru/permissions.md#network-paths)
  * `"bypassPermissions"`: Claude Code выполняет всё без запроса
  * `"manual"`: псевдоним для `"default"`
* **По умолчанию**: не установлено
* **Переопределения для отдельной сессии**: `--permission-mode` и его эквивалент `--dangerously-skip-permissions` для `bypassPermissions` имеют приоритет над этим ключом на одну сессию

```json settings.json theme={null}
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

Правила разрешений действуют поверх любого режима: правила `deny` блокируют в каждом режиме, включая `bypassPermissions`. См. [Режимы разрешений](https://code.claude.com/docs/ru/permission-modes.md). В облачных сессиях Claude Code учитывает из этого ключа только `acceptEdits`, `plan`, `default` и `auto`. О диалогах, которые запускает расширение VS Code, см. [какую настройку расширение читает для начального режима разрешений](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes).

### `permissions.denyInsteadOfPrompting`

Установите значение `true`, чтобы сессия продолжала работать, когда некому ответить на запрос разрешения. Claude Code отклоняет вызов инструмента, который иначе ожидал бы ответа на запрос, и ход продолжается. Требуется Claude Code v2.1.319 или новее.

Вызов выполняется, если его одобряет разрешающее правило, ваш [режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) или классификатор авторежима. Чтобы разрешить большинство вызовов, которые иначе потребовали бы запроса, отвечайте из [хука `PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest).

* **Область действия**: [`User or managed`](#scopes), а также `--settings`. Репозиторий не может установить его за вас.
* **Тип**: Boolean
  * `true`: Claude Code отклоняет вызовы, которые иначе потребовали бы запроса
  * `false`: то же, что и отсутствие значения; вызовы всё равно отклоняются, если другой из этих источников устанавливает `true`
* **По умолчанию**: не установлено, поэтому вызов, требующий подтверждения, вызывает запрос к вам

Этот пример в `~/.claude/settings.json` запускает сессии в авторежиме и отклоняет всё, что всё равно привело бы к запросу:

```json settings.json theme={null}
{
  "permissions": {
    "defaultMode": "auto",
    "denyInsteadOfPrompting": true
  }
}
```

Ключ действует в запусках с `-p`, интерактивных сессиях в терминале, [расширении VS Code](https://code.claude.com/docs/ru/vs-code.md), локальных сессиях в [приложении Desktop](https://code.claude.com/docs/ru/desktop.md), [субагентах](https://code.claude.com/docs/ru/sub-agents.md) и [командах агентов](https://code.claude.com/docs/ru/agent-teams.md). Чтобы вместо этого отклонять то, что вызвало бы запрос, только в одном [неинтерактивном](https://code.claude.com/docs/ru/headless.md) запуске, передайте [`--permission-prompts none`](https://code.claude.com/docs/ru/headless#turn-off-permission-prompts-in-unattended-runs) вместе с `-p`.

#### Что ещё останавливает `denyInsteadOfPrompting`

Когда настройка включена, Claude Code также прекращает следующие запросы ответа:

* **Инструменты вопросов и планов**: Claude Code исключает [`AskUserQuestion`](https://code.claude.com/docs/ru/tools-reference#askuserquestion-tool-behavior), `EnterPlanMode` и `ExitPlanMode`, поэтому сессия в режиме планирования не может выйти из него самостоятельно. Участник команды агентов сохраняет `EnterPlanMode` и `ExitPlanMode`
* **MCP elicitation**: Claude Code отменяет [запрос elicitation](https://code.claude.com/docs/ru/mcp.md#respond-to-mcp-elicitation-requests), если только на него не отвечает [хук `Elicitation`](https://code.claude.com/docs/ru/hooks#elicitation)
* **Хосты разрешений**: Claude Code не обращается к вашему [обратному вызову `canUseTool`](https://code.claude.com/docs/ru/agent-sdk/user-input) или [`--permission-prompt-tool`](https://code.claude.com/docs/ru/cli-reference#cli-flags). Чтобы одобрять вызовы из кода, отвечайте из хука `PermissionRequest`. Некоторые вызовы отклоняются ещё до обращения к какому-либо хуку, например [удаление критического пути](https://code.claude.com/docs/ru/permission-modes.md#critical-path-removals-in-each-permission-mode) в режиме `auto`, которое не охватывает ни одно правило ask.
* **Уведомление о биллинге классификатора**: там, где [уведомление о тарифицируемых запросах классификатора](https://code.claude.com/docs/ru/auto-mode-classifier-billing.md) открыло бы диалоговое окно, Claude Code не показывает его и отклоняет действия, которым нужны эти запросы

Сессия по-прежнему может ожидать ответа в [диалоговом окне доверия рабочему пространству](https://code.claude.com/docs/ru/permissions.md#project-allow-rules-and-workspace-trust) и [подтверждения MCP-серверов проекта](https://code.claude.com/docs/ru/mcp.md#project-server-approvals-and-workspace-trust). Ответьте на оба, прежде чем оставлять сессию работать.

#### Сообщения от `denyInsteadOfPrompting`

Эти сообщения информируют об отклонённых вызовах. Это не запросы, поэтому ничто не ожидает вашего ответа.

Отказ, который читает Claude, может начинаться с этого текста:

```text theme={null}
Permission for this tool use was denied. It requires approval, and this session has no approval surface
```

В выводе `stream-json` [запуски, которые выдают сообщение `permission_denied`](https://code.claude.com/docs/ru/agent-sdk/typescript#sdkpermissiondeniedmessage), сообщают такое значение `decision_reason`:

```text theme={null}
no approval surface in this session; permission request denied automatically
```

В авторежиме при включённой настройке ход завершается после 20 вызовов подряд, которые заблокировал классификатор или отклонила [проверка безопасности](https://code.claude.com/docs/ru/errors.md#auto-mode-cannot-determine-the-safety-of-an-action), и вы видите это сообщение:

```text theme={null}
20 actions were refused and no work went ahead in between, so Claude stopped.
```

Запуск с `-p` сообщает об этом ходе как об `error_during_execution`.

### `permissions.disableBypassPermissionsMode`

Запретите кому-либо входить в режим `bypassPermissions`. Claude Code тогда отклоняет флаг `--dangerously-skip-permissions` и игнорирует `permissionMode: bypassPermissions` в [определении агента](https://code.claude.com/docs/ru/sub-agents.md#permission-modes), поэтому субагент работает в режиме разрешений родительской сессии.

* **Область действия**: [`Any file`](#scopes). Обычно задаётся в [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md) для соблюдения политики организации.
* **Тип**: строка `"disable"`
* **По умолчанию**: не установлено
* **Переопределения для отдельной сессии**: этот ключ имеет приоритет над `--dangerously-skip-permissions`, который Claude Code отклоняет, пока ключ установлен

```json settings.json theme={null}
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

До версии 2.1.223 Claude Code применял режим разрешений из frontmatter даже при отключённом обходе.

### `skipAutoPermissionPrompt`

Пропустите одноразовое уведомление с описанием [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), которое Claude Code показывает, когда вы впервые сами входите в авторежим, например через собственные настройки или переключатель режимов, а не когда встроенное значение по умолчанию запускает в нём сессию. Claude Code показывает это уведомление один раз, а затем запоминает, что оно было показано, поэтому этот ключ имеет значение только там, где уведомление ещё не появлялось.

* **Область действия**: [`User or managed`](#scopes). Репозиторий не может установить его за вас.
* **Тип**: Boolean
  * `true`: Claude Code пропускает уведомление
  * `false`: то же, что и отсутствие значения; уведомление появляется один раз, если только другой из этих файлов не устанавливает `true`
* **По умолчанию**: не установлено, поэтому уведомление появляется один раз

```json settings.json theme={null}
{
  "skipAutoPermissionPrompt": true
}
```

### `skipDangerousModePermissionPrompt`

Пропустите диалоговое окно подтверждения, которое Claude Code показывает перед входом сессии в режим `bypassPermissions`, будь то из-за `--dangerously-skip-permissions` или `defaultMode: "bypassPermissions"`. Claude Code записывает сюда `true` в ваших пользовательских настройках, когда вы один раз подтверждаете это диалоговое окно.

* **Область действия**: [`User, local, or managed`](#scopes), а также файлы, переданные с помощью `--settings`. [Фоновые сессии](https://code.claude.com/docs/ru/permission-modes.md#bypass-permissions-ignored-in-a-background-session) учитывают только пользовательские и управляемые настройки. Недоверенный репозиторий не может пропустить диалоговое окно за вас.
* **Тип**: Boolean
  * `true`: Claude Code пропускает диалоговое окно подтверждения перед входом сессии в режим `bypassPermissions`
  * `false`: то же, что и отсутствие значения; диалоговое окно появляется, если только другой из этих файлов не устанавливает `true`
* **По умолчанию**: не установлено, поэтому диалоговое окно появляется

```json settings.json theme={null}
{
  "skipDangerousModePermissionPrompt": true
}
```

## Настройки песочницы

Изолируйте команды, которые выполняет Claude, от вашей файловой системы, сети и учётных данных. Информацию о том, как работает песочница и требования к платформе, см. в разделе [Sandboxing](https://code.claude.com/docs/ru/sandboxing.md).

### `sandbox`

Изолируйте команды Bash, которые выполняет Claude, от вашей файловой системы и сети с помощью [sandboxing](https://code.claude.com/docs/ru/sandboxing.md). Включите песочницу с помощью `enabled`, затем сузьте или расширьте то, к чему могут обращаться изолированные команды, с помощью подобъектов `filesystem`, `network` и `credentials`. Песочница работает на macOS, Linux и WSL2.

* **Scope**: [`Any file`](#scopes)
* **Тип**: объект с ключами `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `excludedCommands`, `allowUnsandboxedCommands`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`, `allowNestedUserNamespaces`, `bwrapPath`, `socatPath`, `ignoreViolations` и `ripgrep`, а также объектами `filesystem`, `network` и `credentials`
* **Default**: не установлено, поэтому Claude Code выполняет команды без песочницы

Это включает песочницу, пропускает запросы разрешений для изолированных команд, запускает `docker` вне песочницы, открывает два дополнительных пути записи, скрывает файл учётных данных AWS и предварительно разрешает GitHub и npm:

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

Когда управляемые настройки задают логический ключ, такой как `enabled` или `failIfUnavailable`, это значение переопределяет всё, что устанавливает разработчик. Claude Code объединяет ключи-массивы во всех областях действия настроек, которые загружает сессия, поэтому разработчик может добавлять записи; см. [Keep developers from widening the policy](https://code.claude.com/docs/ru/sandboxing.md#keep-developers-from-widening-the-policy) для блокировок, доступных только в управляемых настройках. Чтобы требовать песочницу для организации, см. [Enforce sandboxing with managed settings](https://code.claude.com/docs/ru/sandboxing.md#enforce-sandboxing-with-managed-settings).

### `sandbox.enabled`

Включите [sandboxing](https://code.claude.com/docs/ru/sandboxing.md) для команд Bash. Когда вы выбираете режим на панели `/sandbox`, Claude Code записывает этот ключ в `.claude/settings.local.json` для текущего проекта; установите его в `~/.claude/settings.json`, чтобы изолировать каждый проект.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: Boolean
  * `true`: Claude Code изолирует команды Bash
  * `false`: команды Bash выполняются без изоляции
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true
  }
}
```

На Linux и WSL2 песочнице требуются `bubblewrap` и `socat`; см. [Set up Linux and WSL2](https://code.claude.com/docs/ru/sandboxing.md#set-up-linux-and-wsl2). Когда песочница не может запуститься, Claude Code выполняет команды без изоляции, если вы также не установите [`failIfUnavailable`](#sandbox-failifunavailable).

### `sandbox.failIfUnavailable`

Заставляет Claude Code завершаться с ошибкой при запуске, когда `sandbox.enabled` равно `true`, но песочница не может запуститься, потому что платформа её не поддерживает или проверка зависимостей не проходит. Без этого ключа Claude Code выполняет команды без песочницы. Этой настройкой могут пользоваться управляемые развёртывания, которым песочница нужна как барьер безопасности.

На платформе, которую песочница не поддерживает, Claude Code не запускается при включённом ключе. См. [Enforce sandboxing with managed settings](https://code.claude.com/docs/ru/sandboxing.md#enforce-sandboxing-with-managed-settings).

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Тип**: Boolean
  * `true`: Claude Code завершается с ошибкой при запуске, когда `sandbox.enabled` равно `true`, но песочница не может запуститься. Если песочница проходит эту проверку, а затем не может инициализироваться, сессия продолжает работать. В этом случае Claude Code [отклоняет каждую команду, которая должна выполняться в песочнице](https://code.claude.com/docs/ru/sandboxing.md#commands-refused-with-sandbox-is-required). Сессия в среде, размещённой Anthropic, всё равно может запуститься с предупреждением и не применяет ваши правила `sandbox.filesystem` и `sandbox.network`
  * `false`: Claude Code выполняет команды без песочницы, когда песочница не может запуститься
* **Default**: `false`

Этот пример включает песочницу на управляемых компьютерах и задаёт `failIfUnavailable` значение `true`:

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true
  }
}
```

См. [Enforce sandboxing with managed settings](https://code.claude.com/docs/ru/sandboxing.md#enforce-sandboxing-with-managed-settings).

### `sandbox.autoAllowBashIfSandboxed`

Позволяет Claude Code выполнять команды Bash в песочнице без запроса разрешения. Команды, которые не могут выполняться в песочнице, по-прежнему проходят обычную процедуру проверки разрешений. Правила `deny` и правила `ask` с ограничением по содержимому, такие как `Bash(git push *)`, по-прежнему действуют, но голое правило ask `Bash` для команд в песочнице пропускается. Чтобы задать значение `true` в управляемых настройках, добавьте ключ в блок `sandbox` вашего [источника управляемых настроек с наивысшим приоритетом](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources).

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code выполняет изолированные команды Bash без запроса разрешения, за исключением случаев, описанных в разделе [Auto-allow mode](https://code.claude.com/docs/ru/sandboxing.md#auto-allow-mode); `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` отключает автоматическое разрешение
  * `false`: изолированные команды проходят обычный поток разрешений, поэтому решают ваши правила разрешений и режим разрешений. Вкладка **Mode** в `/sandbox` называет это режимом обычных разрешений
* **По умолчанию**: `false`. До версии v2.1.324 значением по умолчанию было `true`

Чтобы песочница оставалась включённой, а команды в песочнице выполнялись без запроса разрешения, задайте оба ключа в блоке `sandbox`:

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

См. [Auto-allow mode](https://code.claude.com/docs/ru/sandboxing.md#auto-allow-mode), чтобы узнать, о чём всё ещё запрашивает режим автоматического разрешения и как он ведёт себя в режиме планирования.

### `sandbox.excludedCommands`

Перечислите команды, которые Claude Code выполняет вне песочницы, например инструменты, которые не работают в ней. Каждая запись использует тот же синтаксис, что и содержимое [правила разрешений](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax) `Bash(...)`: точная команда, префикс, такой как `docker *`, или шаблон с подстановкой. Шаблон без подстановки означает точное совпадение, поэтому `docker` совпадает только с `docker` без аргументов.

Ваши записи выводят вызов Bash из песочницы, только когда они охватывают каждую команду в нём, и некоторые формы вызова остаются изолированными даже тогда. Одна лишь запись `docker *` не выводит `npm ci && docker build .` из песочницы.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: array of command patterns
* **Default**: не установлено, поэтому ни одна команда не исключена

```json settings.json theme={null}
{
  "sandbox": {
    "excludedCommands": ["docker *"]
  }
}
```

Claude Code сохраняет вызов Bash в изоляции, когда он имеет одну из этих форм, среди прочих:

* Команда, начинающаяся с `sudo`, `eval` или `xargs`
* `cd`, `pushd` или `popd`, где бы они ни появлялись в вызове
* Подстановка команды, подоболочка или блок управления потоком, такой как `if` или `for`
* Перенаправление, такое как `docker build . > build.log` или heredoc `<<EOF`, кроме перенаправления, которое только дублирует файловый дескриптор, как `2>&1`
* Имя команды, которое поступает из переменной
* `git clone`, `git init`, `git worktree add`, `git worktree move` или `git bundle create` с аргументом пути, который является абсолютным, начинается с `~` или содержит сегмент `..`

Например, `cd build && docker compose up` остаётся изолированным при записи `docker *`, и добавление записи `cd` этого не меняет. При записи `git *` команда `git clone <url> vendor/lib` выполняется вне песочницы, но `git clone <url> ~/tools` остаётся изолированной. Клонирование записывает целое дерево файлов, возможно исполняемых, туда, куда указывает путь назначения.

Исключённые команды по-прежнему проходят обычный поток разрешений. Исключение — это удобство, а не граница безопасности: когда инструменту нужно писать только в определённое место, [`filesystem.allowWrite`](#sandbox-filesystem-allowwrite) оставляет его в песочнице.

Записи из областей действия настроек, которые загружает сессия, объединяются в один список, если только песочница не является [обязательной по требованию администратора](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox). Пока это так, Claude Code игнорирует записи в `.claude/settings.json` и `.claude/settings.local.json`, чтобы клонированный репозиторий не мог вывести команды из песочницы. Записи в управляемых настройках, `--settings` и вашем `~/.claude/settings.json` по-прежнему применяются, и никакая блокировка управляемых настроек не распространяется на этот список.

### `sandbox.allowUnsandboxedCommands`

Позвольте Claude повторить попытку выполнения команды вне песочницы с параметром `dangerouslyDisableSandbox` после того, как песочница её заблокирует. Когда значение равно `false`, Claude Code игнорирует этот параметр. Тогда, пока песочница работает, команды, которые выполняет Claude, изолируются, если они не совпадают с записью [`excludedCommands`](#sandbox-excludedcommands). Вкладка **Overrides** в `/sandbox` показывает это состояние как **Strict sandbox mode**. Значение `false` в управляемых настройках включает строгий режим песочницы для разработчиков, на которых они распространяются.

* **Scope**: [`Any file`](#scopes), с [ограничением для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode)
* **Type**: Boolean
  * `true`: Claude может повторить попытку выполнения команды вне песочницы с параметром `dangerouslyDisableSandbox` после того, как песочница её заблокирует
  * `false`: Claude Code игнорирует этот параметр, поэтому, пока песочница работает, команды, которые выполняет Claude, изолируются, если они не совпадают с записью `excludedCommands`
* **Default**: `true`

Это обеспечивает строгий режим песочницы для всех, на кого распространяются управляемые настройки:

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

Значение `false` из управляемых настроек или `--settings` также делает песочницу [обязательной по требованию администратора](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox). Значение `false` в ваших пользовательских настройках имеет приоритет над значением `true` проекта, но не делает песочницу обязательной по требованию администратора. Приоритет над значением проекта требует Claude Code v2.1.285 или более поздней версии.

Кто подтверждает повторную попытку без изоляции, зависит от вашего режима разрешений и правил разрешения. См. [The unsandboxed retry escape hatch](https://code.claude.com/docs/ru/sandboxing.md#the-unsandboxed-retry-escape-hatch).

Чтобы узнать, когда команды, которые вы вводите сами в [`!` shell-mode prompt](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix), выполняются в изоляции, см. [strict sandbox mode](https://code.claude.com/docs/ru/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode).

### `sandbox.filesystem`

Управляйте тем, какие пути могут читать и записывать изолированные команды. По умолчанию они могут писать в рабочий каталог, временный каталог пользователя и каталоги, которые вы добавляете с помощью `--add-dir`, `/add-dir` или `permissions.additionalDirectories`, и могут читать остальную часть файловой системы, включая файлы учётных данных. Расширьте или сузьте это с помощью четырёх списков путей или отключите слой файловой системы с помощью `disabled`. См. [Filesystem isolation](https://code.claude.com/docs/ru/sandboxing.md#filesystem-isolation) для получения информации о границах по умолчанию.

* **Scope**: [`Any file`](#scopes)
* **Type**: object с массивами `allowWrite`, `denyWrite`, `denyRead` и `allowRead`, плюс логические значения `allowManagedReadPathsOnly` и `disabled`
* **Default**: не установлено, поэтому применяются границы чтения и записи по умолчанию

Это позволяет изолированным командам писать в каталог сборки и ваш kubeconfig, а также скрывает файл учётных данных AWS:

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    }
  }
}
```

Claude Code применяет эти списки на границе песочницы ОС, поэтому они распространяются на каждый подпроцесс, который запускает изолированная команда, например `kubectl`, `terraform` или `npm`. Claude Code добавляет ваши [permission rules](https://code.claude.com/docs/ru/sandboxing.md#permission-rules) в те же списки: правила `Edit` allow и deny — в `allowWrite` и `denyWrite`, правила `Read` deny — в `denyRead`, а правила `WebFetch(domain:...)` allow и deny — в списки доменов [`network`](#sandbox-network).

Если не действует блокировка, Claude Code объединяет эти списки во всех файлах настроек, которые загружает сессия. [`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly) ограничивает `allowRead` записями из управляемых настроек, а [`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) делает то же самое для разрешённых доменов. [Блокировки репозитория](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox) исключают записи из файлов настроек репозитория.

[Configure sandboxing](https://code.claude.com/docs/ru/sandboxing.md#configure-sandboxing) описывает источники, которые вы исключаете с помощью `--setting-sources`. Когда вы редактируете список во время сессии, Claude Code [применяет изменение к работающей сессии](https://code.claude.com/docs/ru/settings.md#when-edits-take-effect).

#### Префиксы путей песочницы

Пути в `allowWrite`, `denyWrite`, `denyRead`, `allowRead` и [`credentials.files`](#sandbox-credentials-files) разрешаются по их префиксу:

| Prefix | Meaning | Example |
| :- | :- | :- |
| `/` | Абсолютный путь от корня файловой системы | `/tmp/build` остаётся `/tmp/build` |
| `~/` | Относительно домашнего каталога | `~/.kube` становится `$HOME/.kube` |
| `./` или без префикса | Относительно корня проекта для настроек проекта или относительно `~/.claude` для пользовательских настроек | `./output` в `.claude/settings.json` разрешается в `<project-root>/output` |

Префикс `//path` для абсолютных путей также работает. Если вы используете одиночный слэш `/path`, ожидая разрешения относительно проекта, переключитесь на `./path`. Этот синтаксис отличается от [Read and Edit permission rules](https://code.claude.com/docs/ru/permissions.md#read-and-edit), которые используют `//path` для абсолютного пути и `/path` для пути относительно проекта: пути файловой системы песочницы используют стандартные соглашения, поэтому `/tmp/build` — это абсолютный путь.

Claude Code удаляет конечный слэш из пути каталога, поэтому `~/.aws` и `~/.aws/` совпадают с одним и тем же каталогом. До v2.1.224 Claude Code передавал конечный слэш в песочницу, и Claude всё ещё мог читать или записывать пути под записью `denyRead` или `denyWrite`, написанной с ним.

##### Где подстановочные знаки работают в путях песочницы

Подстановочные знаки `*`, `?` и `**` работают во всех четырёх списках путей `sandbox.filesystem` в macOS и в меньшем числе мест в Linux и WSL2:

| Список `sandbox.filesystem` | Что работает в Linux и WSL2 | Пример, который не работает в Linux и WSL2 | Что написать вместо этого |
| :- | :- | :- | :- |
| `denyRead`, `allowRead` | Работает завершающий `/**`, поэтому `~/build/**` охватывает тот же каталог, что и `~/build`. Любой другой подстановочный знак работает только после имени первого каталога в [полном пути](#sandbox-path-prefixes) записи. | `/**/*.pem` в `denyRead` ничего не охватывает, поэтому не блокирует чтение | `/srv/**/*.pem`, по одной записи для каждого каталога верхнего уровня |
| `allowWrite`, `denyWrite` | Работает только завершающий `/**`, поэтому `~/build/**` охватывает тот же каталог, что и `~/build` | `./src/*` охватывает только файл или каталог в `src`, который сам называется `*`, и ничего, если такого нет | `./src`, который охватывает всё внутри `src`, или по одной записи для каждого пути |

В `~/keys/*.pem` подстановочный знак стоит после имени первого каталога, которым при домашнем каталоге `/home/alice` является `home`:

```text theme={null}
~/keys/*.pem              the entry
/home/alice/keys/*.pem    its full path
 ^^^^                     the first directory name, home
```

В Linux и WSL2 вкладка **Config** панели `/sandbox` в сессии предупреждает о правилах разрешений `Edit`, содержащих подстановочный знак, отличный от завершающего `/**`. Такие подстановочные знаки не работают для команд в песочнице. Добавьте каждый путь, который должно охватывать правило, или содержащий их каталог в `allowWrite` для разрешающего правила или в `denyWrite` для запрещающего.

##### Имена каталогов с квадратными, фигурными или круглыми скобками

Чтобы разрешить или заблокировать каталог, имя которого содержит квадратные скобки, напишите имя как есть, например `./app/[slug]`. В этой записи `[slug]` — это настоящее имя каталога вместе со скобками:

```text theme={null}
app/
└── [slug]/
    └── page.tsx
```

Такая запись охватывает всё внутри каталога, поэтому не добавляйте завершающий `/**`. В macOS, а также в Linux и WSL2 каталог `app/[slug]` должен существовать в момент запуска команды в песочнице.

* **Квадратные скобки, например `[slug]`**: во всех списках в macOS, а также в `denyRead` и `allowRead` в Linux и WSL2 скобки в `./app/[slug]` также являются шаблоном. Тогда запись также соответствует любому пути внутри `app`, имя которого состоит из одного символа из `slug`, например `app/s` или `app/g`. Если эта запись находится в `allowRead` или в `allowWrite` в macOS, команды в песочнице также получают доступ к этим путям. Переименуйте те, к которым у них не должно быть доступа.
* **Квадратные скобки, например `[user-id]` или `[post-id]`, где символ слева от дефиса при сортировке идёт после символа справа**: `./app/[user-id]` охватывает только каталог с точно таким именем во всех списках на всех платформах. До v2.1.304 команды в песочнице в Linux и WSL2 не запускались, пока `denyRead` или `allowRead` содержали такую запись.
* **Фигурные и круглые скобки**: это обычные символы, поэтому `~/data/{keys,tokens}` охватывает один каталог с именем `{keys,tokens}`, а не два варианта. Чтобы охватить `~/data/keys` и `~/data/tokens`, добавьте каждый отдельной записью.

### `sandbox.filesystem.allowWrite`

Добавьте пути, куда изолированные команды могут писать, помимо рабочего каталога, временного каталога пользователя и каталогов, которые вы добавили с помощью `--add-dir`, `/add-dir` или `permissions.additionalDirectories`. Используйте это, когда подпроцессу, такому как `kubectl` или инструмент сборки, нужно писать вне проекта.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: array of path strings, using the [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: не установлено, поэтому изолированные команды могут писать в рабочий каталог, временный каталог пользователя, каталоги, которые вы добавили с помощью `--add-dir` или `/add-dir`, и каталоги в [`permissions.additionalDirectories`](#permissions-additionaldirectories)

Это позволяет сборке писать в `/tmp/build` и позволяет `kubectl` обновлять ваш kubeconfig:

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"]
    }
  }
}
```

В Linux и WSL2 запись для пути, который ещё не существует, не действует, поэтому сначала создайте путь.

Claude Code объединяет записи `allowWrite` и пути из ваших правил разрешений `Edit(...)` allow во всех областях действия настроек, которые загружает сессия, исключая записи из настроек репозитория, пока включён [`permissions.blockReadsOutsideWorkingDirectories`](#sandboxed-commands-under-the-block). [Блокировки репозитория](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox) тоже могут исключать записи репозитория. Запись `allowWrite` не может снять защиту с [protected path](https://code.claude.com/docs/ru/sandboxing.md#protected-paths).

### `sandbox.filesystem.denyWrite`

Запретите изолированным командам запись в определённые пути, включая пути внутри каталога, который в остальном доступен для записи.

* **Scope**: [`Any file`](#scopes)
* **Type**: array of path strings, using the [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: не установлено

Это не позволяет изолированным командам изменять системную конфигурацию или устанавливать двоичные файлы:

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyWrite": ["/etc", "/usr/local/bin"]
    }
  }
}
```

Claude Code объединяет записи во всех областях действия настроек, которые загружает сессия, и добавляет пути из ваших правил разрешений `Edit(...)` deny.

### `sandbox.filesystem.denyRead`

Запретите изолированным командам чтение определённых путей, например файлов учётных данных, которые политика чтения по умолчанию в противном случае раскрыла бы. Чтобы защитить файл учётных данных и сохранить возможность использовать его через прокси песочницы, используйте вместо этого [`sandbox.credentials`](#sandbox-credentials).

* **Scope**: [`Any file`](#scopes)
* **Type**: array of path strings, using the [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: не установлено, поэтому изолированные команды сохраняют [default read access](https://code.claude.com/docs/ru/sandboxing.md#filesystem-isolation), который включает файлы учётных данных, такие как `~/.aws/credentials`

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/.aws/credentials"]
    }
  }
}
```

Claude Code объединяет записи во всех областях действия настроек, которые загружает сессия, и добавляет пути из ваших правил разрешений `Read(...)` deny. Когда [`filesystem.disabled`](#sandbox-filesystem-disabled) имеет значение `true`, Claude Code не применяет эти записи.

### `sandbox.filesystem.allowRead`

Повторно откройте чтение для определённых путей внутри области, которую блокирует [`denyRead`](#sandbox-filesystem-denyread), чтобы организовать доступ на чтение только к рабочей области. Точная запись или запись с подстановкой в `denyRead` остаётся заблокированной внутри более широкого `allowRead`, как показывает [overlap table](https://code.claude.com/docs/ru/sandboxing.md#configure-sandboxing). Когда запись `denyRead` с подстановкой, такая как `~/**/.env`, совпадает с каталогом, Claude Code блокирует также чтение его содержимого. До v2.1.236 на macOS Claude Code повторно открывал пути, совпавшие с записью `denyRead` с подстановкой, везде, где их охватывала более широкая запись `allowRead`, и оставлял содержимое совпавшего каталога доступным для чтения.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: array of path strings, using the [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: не установлено

Это блокирует чтение вашего домашнего каталога, кроме самого проекта:

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Claude Code разрешает запись `.` в корень проекта в настройках проекта и в `~/.claude` в пользовательских настройках. Claude Code объединяет записи во всех файлах настроек, которые загружает сессия, если не установлен [`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly), и исключает записи из настроек репозитория, пока включён [`permissions.blockReadsOutsideWorkingDirectories`](#sandboxed-commands-under-the-block). [Блокировки репозитория](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox) тоже могут исключать записи репозитория.

### `sandbox.filesystem.allowManagedReadPathsOnly`

Учитывайте только записи [`allowRead`](#sandbox-filesystem-allowread), которые поступают из управляемых настроек, чтобы разработчики не могли повторно открыть доступ на чтение к путям, которые заблокировала ваша организация. Claude Code по-прежнему объединяет записи `denyRead` из всех областей действия настроек, которые загружает сессия.

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code учитывает только записи `allowRead` из управляемых настроек
  * `false`: записи `allowRead` из других файлов настроек могут объединяться
* **Default**: `false`

Это блокирует чтение домашнего каталога, повторно открывает `~/work` и не позволяет разработчикам повторно открыть что-либо ещё:

```json managed-settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["~/work"],
      "allowManagedReadPathsOnly": true
    }
  }
}
```

См. [Keep developers from widening the policy](https://code.claude.com/docs/ru/sandboxing.md#keep-developers-from-widening-the-policy).

### `sandbox.filesystem.disabled`

Пропускает изоляцию файловой системы, сохраняя сетевую изоляцию. Команды в песочнице получают неограниченный доступ на чтение и запись к файловой системе хоста, а их исходящий сетевой трафик остаётся ограниченным [`network.allowedDomains`](#sandbox-network-alloweddomains). Используйте этот параметр, когда песочница нужна вам для контроля того, куда подключаются команды, а не того, что они записывают.

* **Scope**: [`User or managed`](#scopes). Когда управляемые настройки вообще настраивают `sandbox.filesystem` или содержат запись `sandbox.credentials.files` с `"mode": "deny"`, установить её могут только управляемые настройки.
* **Type**: Boolean
  * `true`: Claude Code пропускает изоляцию файловой системы и сохраняет изоляцию сети
  * `false`: изоляция файловой системы остаётся включённой
* **Default**: `false`, поэтому изоляция файловой системы остаётся включённой

Это оставляет файловую систему открытой и ограничивает исходящий сетевой трафик GitHub и npm:

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "disabled": true
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

Когда этот уровень отключён, Claude Code не применяет записи `denyRead` и записи `deny` в `credentials.files`, тогда как записи `credentials.envVars` и применённые записи `mask` продолжают работать. Полный список источников, которые могут задать этот ключ, и описание того, что меняется при отключённой изоляции, см. в разделе [Отключение изоляции файловой системы](https://code.claude.com/docs/ru/sandboxing.md#disable-filesystem-isolation).

### `sandbox.ignoreViolations`

Отключите отчёты о нарушениях песочницы для путей, к которым команда, как вы ожидаете, будет обращаться и получать отказ, например для инструмента, который проверяет `/etc/hosts` при запуске, чтобы эти отказы не отображались как нарушения и не попадали в то, что видит Claude. Песочница по-прежнему блокирует доступ; подавляется только отчёт. Ключи — это подстроки для сопоставления с командой, где `*` совпадает с любой командой, а значения — это подстроки нарушения, которое нужно игнорировать для этой команды, например путь файловой системы.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: object mapping a command substring to an array of violation substrings, usually paths
* **Default**: не установлено, поэтому сообщается о каждом нарушении

```json settings.json theme={null}
{
  "sandbox": {
    "ignoreViolations": {
      "*": ["/etc/hosts"]
    }
  }
}
```

### `sandbox.enableWeakerNestedSandbox`

Запустите песочницу Linux внутри непривилегированного контейнера Docker, где bubblewrap не может смонтировать новый `/proc`. Вместо этого внутренняя песочница монтирует через bind-mount существующий `/proc` контейнера, что раскрывает информацию о процессах, которую новое монтирование скрыло бы. Это снижает безопасность; используйте это, только когда внешний контейнер уже обеспечивает необходимую вам изоляцию.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: Boolean
  * `true`: внутренняя песочница монтирует через bind-mount существующий `/proc` контейнера вместо монтирования нового
  * `false`: песочница монтирует новый `/proc`, что не работает в непривилегированном контейнере Docker
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNestedSandbox": true
  }
}
```

Только Linux и WSL2. См. [Bubblewrap fails to start inside a container](https://code.claude.com/docs/ru/sandboxing.md#bubblewrap-fails-to-start-inside-a-container).

### `sandbox.enableWeakerNetworkIsolation`

Позвольте изолированным командам на macOS обращаться к системной службе доверия TLS, `com.apple.trustd.agent`. Инструментам на основе Go, таким как `gh`, `gcloud` и `terraform`, это нужно для проверки сертификатов TLS, когда вы используете [`network.httpProxyPort`](#sandbox-network-httpproxyport) с MITM-прокси и пользовательским ЦС. Это снижает безопасность, открывая потенциальный путь утечки данных через службу доверия.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: Boolean
  * `true`: изолированные команды на macOS могут обращаться к `com.apple.trustd.agent`
  * `false`: изолированные команды на macOS не могут обращаться к системной службе доверия TLS
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNetworkIsolation": true
  }
}
```

Если вы не используете MITM-прокси, вместо этого перечислите проблемные инструменты в [`excludedCommands`](#sandbox-excludedcommands); см. [Go-based CLIs fail TLS verification on macOS](https://code.claude.com/docs/ru/sandboxing.md#go-based-clis-fail-tls-verification-on-macos).

### `sandbox.allowAppleEvents`

Позвольте изолированным командам на macOS отправлять Apple Events, которые нужны `open`, `osascript` и инструментам, открывающим URL-адреса в браузере; без этого они завершаются с ошибкой `-600`. Это снимает изоляцию выполнения кода: изолированные команды могут запускать другие приложения без изоляции и без запроса пользователю, а также отправлять команды AppleScript работающим приложениям, таким как Terminal, с учётом запроса согласия на автоматизацию macOS для каждого приложения (TCC).

* **Scope**: [`User or managed`](#scopes)
* **Type**: Boolean
  * `true`: изолированные команды на macOS могут отправлять Apple Events
  * `false`: изолированные команды на macOS не могут отправлять Apple Events, поэтому `open` и `osascript` завершаются с ошибкой `-600`
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "allowAppleEvents": true
  }
}
```

Чтобы сохранить изоляцию и всё же запускать один такой инструмент, добавьте его вместо этого в [`excludedCommands`](#sandbox-excludedcommands). См. [Apple Events on macOS](https://code.claude.com/docs/ru/sandboxing.md#security-limitations).

### `sandbox.allowNestedUserNamespaces`

Позволяет командам в песочнице в Linux и WSL2 создавать пространства имён пользователей, которые нужны собственной песочнице Chromium и Electron, вложенному bubblewrap и `unshare`. Если вы установите этот ключ в `true`, вы отключите границу безопасности: код из команды в песочнице может в итоге выполняться вне песочницы. Для rootless Podman или Buildah используйте вместо этого [`excludedCommands`](#sandbox-excludedcommands), поскольку песочница останавливает их и другими способами. Требуется Claude Code v2.1.305 или новее.

* **Область действия**: [`User or managed`](#scopes). Значение `true` учитывается из `~/.claude/settings.json`, JSON, переданного с помощью `--settings`, или [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md). Claude Code игнорирует `true` в `.claude/settings.json` или `.claude/settings.local.json` проекта. В сессии, где [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](https://code.claude.com/docs/ru/env-vars#variables) установлено в `1`, Claude Code игнорирует `true` из любого источника. Значение `false` учитывается из любого файла согласно [приоритету настроек](https://code.claude.com/docs/ru/settings.md#settings-precedence).
* **Тип**: логический
  * `true`: команды в песочнице могут создавать пространства имён пользователей
  * `false`: этот ключ ничего дополнительно не разрешает, и действует поведение песочницы по умолчанию
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "allowNestedUserNamespaces": true
  }
}
```

При включённом ключе не полагайтесь ни на какие ограничения песочницы, включая [защищённые пути](https://code.claude.com/docs/ru/sandboxing.md#protected-paths) и записи [`credentials.files`](#sandbox-credentials-files), чтобы остановить вредоносную команду. В [режиме автоматического разрешения](https://code.claude.com/docs/ru/sandboxing.md#auto-allow-mode) такая команда может выполниться без запроса разрешения. Если в вашей организации есть служба безопасности, проконсультируйтесь с ней, прежде чем включать этот ключ.

Чтобы найти решение для вашего инструмента, см. [Chromium или rootless Podman не работают внутри песочницы в Linux](https://code.claude.com/docs/ru/sandboxing.md#chromium-or-rootless-podman-fails-inside-the-sandbox-on-linux).

### `sandbox.ripgrep`

Укажите песочнице собственный двоичный файл ripgrep вместо того, который использует Claude Code, например когда вашей платформе нужен иначе собранный `rg`.

* **Scope**: [`User or managed`](#scopes)
* **Type**: object с `command` — путём к двоичному файлу ripgrep, и необязательным `args` — массивом аргументов, добавляемых в начало
* **Default**: не установлено, поэтому песочница использует тот же двоичный файл ripgrep, что и Claude Code. Это встроенный двоичный файл, если вы не установите [`USE_BUILTIN_RIPGREP`](https://code.claude.com/docs/ru/env-vars) в `0`

```json settings.json theme={null}
{
  "sandbox": {
    "ripgrep": {
      "command": "/usr/local/bin/rg"
    }
  }
}
```

### `sandbox.bwrapPath`

Укажите песочнице двоичный файл bubblewrap, установленный вне `PATH`, например поставляемую копию на изолированном от сети хосте. Claude Code использует этот путь как для проверки зависимостей при запуске, так и при обёртывании каждой изолированной команды.

* **Scope**: [`Managed`](#scopes). Claude Code читает его только из управляемых настроек, чтобы пользовательский, проектный или локальный файл не мог указать песочнице другой двоичный файл.
* **Type**: string, an absolute path; Claude Code drops a relative path and falls back to `PATH` lookup
* **Default**: не установлено, поэтому Claude Code находит `bwrap` в `PATH`

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "bwrapPath": "/opt/admin/bwrap"
  }
}
```

Только Linux и WSL2.

### `sandbox.socatPath`

Укажите сетевому прокси песочницы двоичный файл `socat`, установленный вне `PATH`.

* **Scope**: [`Managed`](#scopes)
* **Type**: string, an absolute path; Claude Code drops a relative path and falls back to `PATH` lookup
* **Default**: не установлено, поэтому Claude Code находит `socat` в `PATH`

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "socatPath": "/opt/admin/socat"
  }
}
```

Только Linux и WSL2.

### `sandbox.credentials`

Объявите файлы учётных данных и переменные окружения, которые нужно [защитить от изолированных команд](https://code.claude.com/docs/ru/sandboxing.md#protect-credentials). Каждая запись указывает файл `path` или переменную `name` и `mode`: `deny` скрывает учётные данные внутри песочницы, а `mask` показывает изолированным командам заполнитель, в то время как [sandbox proxy](https://code.claude.com/docs/ru/sandboxing.md#mask-credentials) подставляет реальное значение в исходящих запросах. Claude Code защищает только перечисленные вами записи; встроенного списка запрещённых учётных данных нет.

* **Scope**: [`Any file`](#scopes). Claude Code учитывает записи `mask`, `allowPlaintextInject`, `awsPairs` и `sigv4` только из пользовательских настроек, управляемых настроек и флага `--settings`.
* **Type**: object с `files`, `envVars`, `allowPlaintextInject`, `awsPairs` и `sigv4`
* **Default**: не установлено, поэтому никакие учётные данные не защищены

Это скрывает файл учётных данных AWS и удаляет `GITHUB_TOKEN` из изолированных команд:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [{ "path": "~/.aws/credentials", "mode": "deny" }],
      "envVars": [{ "name": "GITHUB_TOKEN", "mode": "deny" }]
    }
  }
}
```

Защита файла `deny` является частью слоя файловой системы, поэтому она не действует, когда вы [disable filesystem isolation](https://code.claude.com/docs/ru/sandboxing.md#disable-filesystem-isolation); защита переменных окружения по-прежнему действует.

#### Недействительные записи учётных данных в управляемых настройках

Когда запись `sandbox.credentials` в управляемых настройках не проходит проверку, Claude Code продолжает защищать учётные данные, где это возможно:

* Запись в `files` или `envVars`, у которой по-прежнему действительный `path` или `name` и `mode` со значением `mask` или `deny`, например запись, шаблон `extract` которой не содержит группы захвата, понижается до `mode: "deny"` с предупреждением, поэтому учётные данные остаются заблокированными, а не замаскированными, пока вы не исправите запись. Пониженная запись `files` закрепляет [`filesystem.disabled`](https://code.claude.com/docs/ru/sandboxing#disable-filesystem-isolation) так же, как явная запись `deny`, а предупреждение отмечает, что её блокировка чтения не применяется, если управляемые настройки отключают изоляцию файловой системы.
* Запись с неизвестным `mode` или недействительным `path` или `name` удаляется.
* В каждом случае выводится предупреждение; независимо от того, понижена запись или удалена, остальные действительные записи по-прежнему применяются.

Действует в v2.1.191 и более поздних версиях; до v2.1.221 каждая недействительная запись удалялась. Для других управляемых ключей с обработкой на уровне отдельных полей см. [Invalid entries in managed settings](https://code.claude.com/docs/ru/managed-settings.md#invalid-entries-in-managed-settings).

### `sandbox.credentials.files`

Защитите файлы или каталоги учётных данных от изолированных команд. С `"mode": "deny"` Claude Code блокирует чтение пути внутри песочницы — та же блокировка чтения, что и у [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread). С `"mode": "mask"` изолированные команды на Linux и WSL2 читают копию файла с сигнальным значением, а прокси песочницы подставляет реальное значение в исходящих запросах к `injectHosts` этой записи; на macOS файл вместо этого недоступен для чтения внутри песочницы. `"mode": "mask"` требует Claude Code v2.1.221 или более поздней версии.

* **Scope**: [`Any file`](#scopes). Claude Code отбрасывает записи `mask` из проектного `.claude/settings.json` и локального `.claude/settings.local.json`.
* **Type**: array of objects, each with `path` and a `mode` of `"deny"` or `"mask"`, plus the optional [mask fields for files](#mask-fields-for-files)
* **Default**: не установлено, поэтому никакие файлы учётных данных не защищены

Это скрывает файл учётных данных AWS и маскирует файл хостов `gh`, подставляя реальное значение только в запросах к `api.github.com`:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.config/gh/hosts.yml", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

Пути используют те же [prefixes](#sandbox-path-prefixes), что и настройки `sandbox.filesystem.*`, и Claude Code объединяет массивы из всех областей действия настроек, которые загружает сессия. [Protect credentials](https://code.claude.com/docs/ru/sandboxing.md#protect-credentials) описывает, что по-прежнему применяется из источников, которые вы исключаете с помощью `--setting-sources`. Записи `mask` требуют Claude Code v2.1.221 или более поздней версии.

Подстановка `mask` работает только через прокси песочницы, поэтому установите [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate) или [`allowPlaintextInject`](#sandbox-credentials-allowplaintextinject) для тестовых сетей с обычным HTTP. `mask` применяется к одному файлу, поэтому перечислите каждый файл учётных данных отдельно. Claude Code принимает, но игнорирует поля `mask` в записи `deny`. [Mask credentials](https://code.claude.com/docs/ru/sandboxing.md#mask-credentials) описывает, какие источники настроек учитываются, а [Mask credential files](https://code.claude.com/docs/ru/sandboxing.md#mask-credential-files) — когда запись откатывается к `deny`.

#### Поля маски для файлов

Запись `mask` принимает эти необязательные поля. Без `extract` или `decode` Claude Code заменяет всё содержимое файла одним сигнальным значением. На macOS с включённой изоляцией файловой системы Claude Code применяет запись `mask` как `deny` до запуска `extract` или `decode`; см. [Mask credential files](https://code.claude.com/docs/ru/sandboxing.md#mask-credential-files).

| Field | Type | What it does |
| :- | :- | :- |
| `extract` | string, a regular expression with at least one capturing group | Маскирует только текст, захваченный группой 1 каждого совпадения, чтобы остальная часть файла оставалась пригодной для разбора. Если также установлен `decode`, Claude Code проверяет каждый захват как возможный JWT вместо прямой замены. Требует v2.1.221 или более поздней версии |
| `onExtractNoMatch` | `"warn"`, `"deny"` или `"error"`; default `"warn"` | Что происходит, когда `extract` или `decode` не находит ничего для маскирования. `warn` оставляет файл доступным для чтения как есть внутри песочницы, `deny` делает его недоступным для чтения, а `error` останавливает настройку песочницы, пока вы не исправите конфигурацию. Claude Code рассматривает `deny` как `error`, когда блокировка чтения не будет применяться, потому что вы [disable filesystem isolation](https://code.claude.com/docs/ru/sandboxing.md#disable-filesystem-isolation) или запись [`sandbox.filesystem.allowRead`](#sandbox-filesystem-allowread) повторно открывает путь. Требует v2.1.221 или более поздней версии; случай `decode` требует v2.1.224 или более поздней версии |
| `decode` | the string `"jwt"` | Находит JSON Web Tokens (JWT) в файле с помощью встроенного шаблона или с помощью `extract`, если он установлен, проверяет каждого кандидата и заменяет его структурно корректным поддельным токеном, чтобы код внутри песочницы, который декодирует токен, продолжал работать. Когда ни один кандидат не проходит проверку, результат определяет `onExtractNoMatch`. Требует v2.1.224 или более поздней версии |
| `maskClaims` | array of strings, at least one claim name; requires `decode` | Маскирует только указанные утверждения (claims) верхнего уровня полезной нагрузки внутри каждого проверенного JWT и пересобирает токен вокруг изменённой полезной нагрузки, чтобы другие утверждения оставались доступными для чтения. Когда ни одно из указанных утверждений не совпадает, результат определяет `onExtractNoMatch`. Требует v2.1.224 или более поздней версии |
| `maskDuplicates` | Boolean, default `false` | Также заменяет дословные копии каждого замаскированного значения в других местах файла, например секрет, вставленный в комментарий. Claude Code сопоставляет необработанные подстроки, поэтому используйте это только для длинных секретов с высокой энтропией. Учитывается, только когда установлен `extract` или `decode`. Требует v2.1.221 или более поздней версии |
| `injectHosts` | array of strings, each a host that [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) also admits | Сужает набор хостов, для которых прокси песочницы подставляет реальное значение. Если не установлено, прокси подставляет его в запросах к каждому хосту в `sandbox.network.allowedDomains`. Требует v2.1.221 или более поздней версии |

Это маскирует только значение `oauth_token` в файле хостов `gh`, заменяет все другие его копии в файле, делает файл недоступным для чтения, если шаблон ничего не находит, и подставляет реальный токен только в запросах к `api.github.com`:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [
        {
          "path": "~/.config/gh/hosts.yml",
          "mode": "mask",
          "extract": "oauth_token:\\s*(\\S+)",
          "maskDuplicates": true,
          "onExtractNoMatch": "deny",
          "injectHosts": ["api.github.com"]
        }
      ]
    }
  }
}
```

### `sandbox.credentials.envVars`

Защитите переменные окружения от изолированных команд. С `"mode": "deny"` Claude Code удаляет переменную из окружения изолированных команд. С `"mode": "mask"` изолированные команды видят сигнальное значение, уникальное для сессии, а прокси песочницы подставляет реальное значение в исходящих запросах к `injectHosts` этой записи, поэтому такие инструменты, как `gh` и `npm`, продолжают проходить аутентификацию, никогда не получая реальных учётных данных.

* **Scope**: [`Any file`](#scopes). Claude Code отбрасывает записи `mask` из проектного `.claude/settings.json` и локального `.claude/settings.local.json`.
* **Type**: array of objects, each with `name` and a `mode` of `"deny"` or `"mask"`, plus the optional [mask fields for environment variables](#mask-fields-for-environment-variables)
* **Default**: не установлено, поэтому никакие переменные окружения не защищены

Это удаляет `NPM_TOKEN` из изолированных команд и маскирует `GITHUB_TOKEN`, подставляя реальное значение только в запросах к `api.github.com`:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "envVars": [
        { "name": "NPM_TOKEN", "mode": "deny" },
        { "name": "GITHUB_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

`name` должно начинаться с буквы или подчёркивания и содержать только буквы, цифры и подчёркивания. Claude Code объединяет массивы из всех областей действия настроек, которые загружает сессия, и применяет `deny`, когда одна и та же переменная встречается с обоими режимами. [Protect credentials](https://code.claude.com/docs/ru/sandboxing.md#protect-credentials) описывает, что по-прежнему применяется из источников, которые вы исключаете с помощью `--setting-sources`.

Подстановка `mask` работает только через прокси песочницы, поэтому установите [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate) или [`allowPlaintextInject`](#sandbox-credentials-allowplaintextinject) для тестовых сетей с обычным HTTP; см. [Mask credentials](https://code.claude.com/docs/ru/sandboxing.md#mask-credentials). Claude Code принимает, но игнорирует поля `mask` в записи `deny`.

#### Поля маски для переменных окружения

Запись `mask` принимает эти необязательные поля. Без `extract` или `decode` Claude Code заменяет всё значение одним сигнальным значением. `extract` и `decode` нельзя комбинировать в одной записи.

| Field | Type | What it does |
| :- | :- | :- |
| `extract` | string, a regular expression with at least one capturing group | Маскирует только текст, захваченный группой 1 каждого совпадения, например пароль внутри строки подключения `DATABASE_URL`, чтобы остальная часть значения оставалась пригодной для разбора. Требует v2.1.224 или более поздней версии |
| `onExtractNoMatch` | `"warn"`, `"deny"` или `"error"`; default `"warn"`. В записи с `decode` принимается только `"warn"` | Что происходит, когда `extract` ничего не находит. `warn` передаёт переменную без маскирования, `deny` удаляет её внутри песочницы, а `error` останавливает настройку песочницы, пока вы не исправите конфигурацию. Требует v2.1.224 или более поздней версии |
| `decode` | the string `"jwt"` | Проверяет, что всё значение является JWT, и заменяет его структурно корректным поддельным токеном, чтобы код внутри песочницы, который декодирует токен, продолжал работать; прокси подставляет весь реальный токен в исходящем трафике. Значение, не прошедшее проверку, передаётся без маскирования с предупреждением. Требует v2.1.224 или более поздней версии |
| `maskClaims` | array of strings, at least one claim name; requires `decode` | Маскирует только указанные утверждения (claims) верхнего уровня полезной нагрузки внутри декодированного JWT и пересобирает токен вокруг изменённой полезной нагрузки, чтобы другие утверждения оставались доступными для чтения. Когда ни одно из указанных утверждений не совпадает, переменная передаётся без маскирования с предупреждением. Требует v2.1.224 или более поздней версии |
| `injectHosts` | array of strings, each a host that [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) also admits | Сужает набор хостов, для которых прокси песочницы подставляет реальное значение. Если не установлено, прокси подставляет его в запросах к каждому хосту в `sandbox.network.allowedDomains`. Указывайте IPv6-адрес назначения как сжатый адрес без скобок, например `"::1"`, а не в форме со скобками; см. [IPv6 destinations in `injectHosts`](https://code.claude.com/docs/ru/sandboxing#ipv6-destinations-in-injecthosts) |

Это маскирует только пароль внутри `DATABASE_URL`, удаляет переменную, если шаблон ничего не находит, и маскирует JWT в `SERVICE_JWT`, оставляя доступными для чтения все утверждения, кроме `api_key`:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "envVars": [
        {
          "name": "DATABASE_URL",
          "mode": "mask",
          "extract": "://[^:]+:([^@]+)@",
          "onExtractNoMatch": "deny"
        },
        {
          "name": "SERVICE_JWT",
          "mode": "mask",
          "decode": "jwt",
          "maskClaims": ["api_key"]
        }
      ]
    }
  }
}
```

### `sandbox.credentials.allowPlaintextInject`

Разрешите подстановку `mask` в обычных HTTP-запросах, а также в HTTPS с терминированием TLS. При обычном HTTP подлинность вышестоящего сервера не проверяется, а учётные данные передаются в открытом виде, поэтому оставляйте это отключённым за пределами доверенных тестовых сетей.

* **Scope**: [`User or managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code разрешает подстановку `mask` в обычных HTTP-запросах, а также в HTTPS с терминированием TLS
  * `false`: Claude Code разрешает подстановку `mask` только в HTTPS с терминированием TLS
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "allowPlaintextInject": true
    }
  }
}
```

### `sandbox.credentials.awsPairs`

Сгруппируйте замаскированные переменные окружения, которые образуют один набор учётных данных AWS, для [SigV4 re-signing](https://code.claude.com/docs/ru/sandboxing.md#re-sign-aws-requests), когда ваши учётные данные хранятся в переменных с нестандартными именами. Claude Code автоматически связывает стандартную тройку `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` и `AWS_SESSION_TOKEN`, когда вы маскируете их значения целиком, поэтому этот ключ нужен только для других имён. Требует Claude Code v2.1.224 или более поздней версии.

* **Scope**: [`User or managed`](#scopes)
* **Type**: array of objects, each with `accessKeyIdVar`, `secretAccessKeyVar`, and optionally `sessionTokenVar`, naming `sandbox.credentials.envVars` entries
* **Default**: не установлено, поэтому связывается только стандартная тройка

Это связывает три переменные с пользовательскими именами в один набор учётных данных AWS для повторного подписания:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "awsPairs": [
        {
          "accessKeyIdVar": "MY_KEY_ID",
          "secretAccessKeyVar": "MY_SECRET_KEY",
          "sessionTokenVar": "MY_SESSION_TOKEN"
        }
      ]
    }
  }
}
```

Каждая указанная переменная должна быть записью `mask` со значением целиком в [`sandbox.credentials.envVars`](#sandbox-credentials-envvars), без `extract` или `decode`, и может занимать только один слот среди всех пар. Также действуют следующие правила:

* Прокси повторно подписывает запросы к хостам, перечисленным в `injectHosts` записи идентификатора ключа доступа
* Когда установлен `sessionTokenVar`, прокси отправляет реальный токен как `x-amz-security-token` в повторно подписанных запросах
* Указание любой из стандартных переменных в паре заменяет автоматическое связывание

### `sandbox.credentials.sigv4`

Выберите, что прокси песочницы делает с формами запросов AWS, которые он [не может повторно подписать](https://code.claude.com/docs/ru/sandboxing.md#re-sign-aws-requests): `streaming` — для потоковых загрузок aws-chunked, `presigned` — для предварительно подписанных URL-адресов и `sigv4a` — для асимметричных подписей SigV4A. Это применяется только к запросам, подписанным с помощью заполнителя идентификатора ключа доступа замаскированной пары. Требует Claude Code v2.1.224 или более поздней версии.

* **Scope**: [`User or managed`](#scopes)
* **Type**: object с `streaming`, `presigned` и `sigv4a`, каждый из которых имеет одно из значений:
  * `"deny"`: прокси завершает запрос с ошибкой
  * `"passthrough"`: прокси пересылает запрос, подписанный замаскированным заполнителем, поэтому инструмент получает собственный отказ AWS
* **Default**: не установлено, поэтому каждая форма имеет значение `"deny"`

Это пересылает потоковые загрузки вместо того, чтобы завершать их с ошибкой на прокси:

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "sigv4": {
        "streaming": "passthrough"
      }
    }
  }
}
```

С `deny` прокси завершает запрос с ошибкой. С `passthrough` прокси пересылает запрос с подписью, вычисленной из замаскированного заполнителя, поэтому AWS его отклоняет, и вызывающий инструмент получает собственный ответ AWS вместо ошибки прокси.

### `sandbox.network`

Управляйте тем, к каким хостам, портам и сокетам могут обращаться изолированные команды. Песочница направляет исходящий трафик через прокси, который применяет эти списки; см. [Network isolation](https://code.claude.com/docs/ru/sandboxing.md#network-isolation), чтобы узнать, как прокси принимает решения и когда он запрашивает разрешение.

* **Scope**: [`Any file`](#scopes). `strictAllowlist`, `allowManagedDomainsOnly` и `tlsTerminate` читаются из меньшего числа источников, как указано в их описаниях.
* **Type**: object с подключами ниже
* **Default**: не установлено, поэтому никакие домены не разрешены заранее, и ваш режим разрешений определяет, [что происходит с каждым новым хостом](https://code.claude.com/docs/ru/sandboxing.md#hosts-outside-your-allowed-domains)

Это заранее разрешает GitHub и npm, блокирует `uploads.github.com` и позволяет командам привязываться к localhost:

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "deniedDomains": ["uploads.github.com"],
      "allowLocalBinding": true
    }
  }
}
```

Claude Code объединяет подключи-массивы во всех областях действия настроек, поэтому проект может добавлять домены к вашему пользовательскому списку, если не действует [блокировка репозитория](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox). [Правила разрешений](https://code.claude.com/docs/ru/sandboxing.md#permission-rules) `WebFetch(domain:...)` allow и deny пополняют те же списки разрешённых и запрещённых доменов.

### `sandbox.network.allowUnixSockets`

Перечислите пути Unix-сокетов, к которым изолированные команды могут подключаться на macOS. Claude Code игнорирует этот список на Linux и WSL2, где фильтр seccomp не может проверять пути сокетов; там используйте вместо этого [`allowAllUnixSockets`](#sandbox-network-allowallunixsockets).

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: array of strings, each a socket path
* **Default**: не установлено, поэтому песочница macOS блокирует все Unix-сокеты

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"]
    }
  }
}
```

Путь сокета может предоставлять широкий доступ: например, разрешение `/var/run/docker.sock` позволяет изолированной команде управлять демоном Docker. См. [Security limitations](https://code.claude.com/docs/ru/sandboxing.md#security-limitations).

### `sandbox.network.allowAllUnixSockets`

Позвольте изолированным командам подключаться к любым Unix-сокетам. На Linux и WSL2 [seccomp filter](https://code.claude.com/docs/ru/sandboxing.md#set-up-linux-and-wsl2) песочницы блокирует вызовы `socket(AF_UNIX, ...)`, поэтому это единственный способ разрешить там Unix-сокеты. Когда фильтр отсутствует, о чём `/sandbox` сообщает на вкладке Dependencies, песочница не блокирует вызовы Unix-сокетов. См. [Set up Linux and WSL2](https://code.claude.com/docs/ru/sandboxing.md#set-up-linux-and-wsl2), чтобы узнать, откуда берётся фильтр.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Тип**: логический
  * `true`: команды в песочнице могут подключаться к любому Unix-сокету. В Linux и WSL2 они также могут подключаться к сокетам виртуальных машин — семейству адресов `AF_VSOCK`
  * `false`: песочница блокирует подключения к Unix-сокетам: в macOS — кроме путей из `allowUnixSockets`, а в Linux и WSL2 — через фильтр seccomp, если он присутствует
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowAllUnixSockets": true
    }
  }
}
```

На WSL2 `true` также снова открывает сокет interop, который запускает двоичные файлы Windows, такие как `cmd.exe` и `powershell.exe`.

### `sandbox.network.allowLocalBinding`

Позвольте изолированным командам на macOS прослушивать сетевые порты, например для запуска сервера разработки, и подключаться к любому порту на localhost. Команда, которая прослушивает адрес, отличный от loopback, принимает подключения с других машин. Ключ не действует на Linux и WSL2, где у каждой изолированной команды есть собственный интерфейс loopback. Чтобы обратиться к серверу на хосте из Linux или WSL2, см. [A command fails to reach a server on localhost](https://code.claude.com/docs/ru/sandboxing.md#a-command-fails-to-reach-a-server-on-localhost).

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: Boolean
  * `true`: изолированные команды на macOS могут прослушивать любой локальный адрес и подключаться к любому порту на localhost
  * `false`: изолированные команды на macOS не могут прослушивать порт или напрямую подключаться к серверам на localhost
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowLocalBinding": true
    }
  }
}
```

### `sandbox.network.allowMachLookup`

Перечисляет дополнительные имена служб XPC и Mach, которые может искать песочница macOS. Инструментам, взаимодействующим через XPC, например iOS Simulator или Playwright, нужно, чтобы их службы были перечислены здесь. Команды в песочнице могут обращаться за пределы песочницы к каждой перечисленной вами службе, и песочница [не ограничивает то, что эти службы делают для этих команд](https://code.claude.com/docs/ru/sandboxing.md#security-limitations).

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox)
* **Type**: array of strings, each a service name; a single trailing `*` matches a prefix, and `"*"` alone matches every service
* **Default**: не установлено

Эта конфигурация разрешает все службы с префиксом `com.apple.CoreSimulator.`:

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowMachLookup": ["com.apple.CoreSimulator.*"]
    }
  }
}
```

### `sandbox.network.allowedDomains`

Заранее разрешите домены для исходящего трафика изолированных команд, чтобы песочница не запрашивала для них разрешение. Подстановки, такие как `*.example.com`, совпадают с поддоменами, а необязательный суффикс `:port` ограничивает запись одним портом; запись без порта совпадает с любым портом.

* **Scope**: [`Any file`](#scopes), с [ограничениями для настроек проекта и локальных настроек](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox). Только управляемые настройки, когда установлен [`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly).
* **Type**: array of strings, each a domain, wildcard pattern, or IP literal, with an optional `:port` suffix
* **Default**: не установлено, поэтому ваш режим разрешений определяет, [что происходит с каждым новым хостом](https://code.claude.com/docs/ru/sandboxing.md#hosts-outside-your-allowed-domains)

Это заранее разрешает GitHub на любом порту, все поддомены npm и один хост API только на порту 443:

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "api.example.com:443"]
    }
  }
}
```

Записывайте IPv6-литералы в скобках, с необязательным портом: `"[::1]"` разрешает любой порт, а `"[::1]:443"` — один порт. Форма со скобками требует Claude Code v2.1.229 или более поздней версии. См. [IPv6 addresses in domain lists](https://code.claude.com/docs/ru/sandboxing.md#ipv6-addresses-in-domain-lists).

### `sandbox.network.deniedDomains`

Заблокируйте домены для исходящего трафика изолированных команд, используя тот же синтаксис подстановок, портов и IPv6, что и [`allowedDomains`](#sandbox-network-alloweddomains). Запрещённый домен остаётся заблокированным, даже когда с ним также совпадает запись `allowedDomains`.

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings, each a domain, wildcard pattern, or IP literal, with an optional `:port` suffix
* **Default**: не установлено

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "deniedDomains": ["sensitive.cloud.example.com"]
    }
  }
}
```

Claude Code объединяет этот список из всех источников настроек, которые загружает сессия, даже когда установлен `allowManagedDomainsOnly`, поэтому разработчик всегда может ужесточить список запрещённых доменов. Для IPv6-литералов см. [IPv6 addresses in domain lists](https://code.claude.com/docs/ru/sandboxing.md#ipv6-addresses-in-domain-lists).

Запись с конечной точкой, которая обозначает полностью определённое доменное имя, например `example.com.`, блокирует те же подключения, что и `example.com`.

### `sandbox.network.strictAllowlist`

Запретите изолированным командам доступ к хостам вне списка разрешённых доменов вместо запроса подтверждения. Список разрешённых доменов — это [`allowedDomains`](#sandbox-network-alloweddomains) плюс домены из правил `WebFetch(domain:...)` allow, или только записи управляемых настроек, когда установлен [`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly). [Locks that apply without an admin-required sandbox](https://code.claude.com/docs/ru/sandboxing.md#locks-that-apply-without-an-admin-required-sandbox) описывает записи репозитория. Требует Claude Code v2.1.219 или более поздней версии.

* **Scope**: [`User or managed`](#scopes). Репозиторий не может его включить или отключить.
* **Type**: Boolean
  * `true`: Claude Code запрещает изолированным командам доступ к хостам вне списка разрешённых доменов
  * `false`: если другой доверенный файл настроек не устанавливает `true`, Claude Code решает судьбу хоста вне списка разрешённых доменов в зависимости от режима разрешений, а не отказывает сразу: в авторежиме он проверяет хост по [per-command allowed domains](https://code.claude.com/docs/ru/sandboxing.md#per-command-allowed-domains-in-auto-mode) команды, в режиме `dontAsk` отказывает, в режиме `bypassPermissions` и в интерактивных терминальных сессиях режима планирования, где доступен обход, разрешает, а в остальных случаях спрашивает вас
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "strictAllowlist": true
    }
  }
}
```

Claude Code применяет это только к изолированным командам; внутрипроцессные инструменты, такие как `WebFetch`, по-прежнему следуют своим [permission rules](https://code.claude.com/docs/ru/sandboxing.md#permission-rules). Когда любой из учитываемых источников устанавливает значение `true`, оно остаётся включённым. См. [Network isolation](https://code.claude.com/docs/ru/sandboxing.md#network-isolation). Требует Claude Code v2.1.219 или более поздней версии.

### `sandbox.network.allowManagedDomainsOnly`

Ограничьте сетевой список разрешённых доменов тем, что определяют управляемые настройки. Тогда Claude Code учитывает только `allowedDomains` и правила `WebFetch(domain:...)` allow из управляемых настроек, игнорирует домены из пользовательских, проектных, локальных настроек и `--settings` и автоматически блокирует неразрешённый домен вместо запроса.

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code учитывает только `allowedDomains` и правила `WebFetch(domain:...)` allow из управляемых настроек и блокирует неразрешённый домен вместо запроса
  * `false`: домены из других файлов настроек могут объединяться в список разрешённых доменов
* **Default**: `false`

Это ограничивает список разрешённых доменов GitHub и npm и игнорирует любые домены, которые добавляют разработчики:

```json managed-settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowManagedDomainsOnly": true,
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

Пока ключ имеет значение `true`, песочница является [обязательной по требованию администратора](https://code.claude.com/docs/ru/sandboxing.md#repository-settings-under-an-admin-required-sandbox), и только управляемые настройки могут задать [порт прокси](#sandbox-network-httpproxyport).

Запрещённые домены по-прежнему объединяются из всех источников, которые загружает сессия. См. [Keep developers from widening the policy](https://code.claude.com/docs/ru/sandboxing.md#keep-developers-from-widening-the-policy).

### `sandbox.network.httpProxyPort`

Укажите песочнице ваш собственный HTTP-прокси вместо того, который запускает Claude Code. Организации делают это, чтобы проверять HTTPS-трафик, применять собственные правила фильтрации или записывать запросы в лог. Ваш прокси берёт на себя фильтрацию, и Claude Code перестаёт применять свои списки доменов и сетевые запросы разрешений к трафику, отправляемому туда. Если не установлено, Claude Code запускает собственный прокси для HTTP-трафика.

* **Scope**: [`Any file`](#scopes), если [другие настройки песочницы не ограничивают, какие файлы могут задавать порт](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration)
* **Type**: number, a local TCP port
* **Default**: не установлено, поэтому Claude Code запускает собственный прокси

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080
    }
  }
}
```

Также установите [`socksProxyPort`](#sandbox-network-socksproxyport), если ваш прокси должен обрабатывать и SOCKS-трафик; если установлен только один из двух, Claude Code по-прежнему запускает собственный прокси для другого протокола. См. [Custom proxy configuration](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration).

### `sandbox.network.socksProxyPort`

Укажите песочнице ваш собственный SOCKS5-прокси вместо того, который запускает Claude Code. Ваш прокси берёт на себя фильтрацию, и Claude Code перестаёт применять свои списки доменов и сетевые запросы разрешений к трафику, отправляемому туда. Если не установлено, Claude Code запускает собственный прокси для SOCKS-трафика.

* **Scope**: [`Any file`](#scopes), если [другие настройки песочницы не ограничивают, какие файлы могут задавать порт](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration)
* **Type**: number, a local TCP port
* **Default**: не установлено, поэтому Claude Code запускает собственный прокси

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "socksProxyPort": 8081
    }
  }
}
```

См. [Custom proxy configuration](https://code.claude.com/docs/ru/sandboxing.md#custom-proxy-configuration).

### `sandbox.network.tlsTerminate`

Заставьте прокси песочницы терминировать TLS, чтобы он мог читать содержимое HTTPS-запросов. Это экспериментальная функция, и она необходима для [credential substitution](https://code.claude.com/docs/ru/sandboxing.md#mask-credentials) `mask`. Установите `{}`, чтобы создать эфемерный центр сертификации для сессии, или установите `caCertPath` и `caKeyPath`, чтобы использовать собственный.

* **Scope**: [`User or managed`](#scopes). Репозиторий не может её включить или предоставить центр сертификации.
* **Type**: object с необязательными строками `caCertPath` и `caKeyPath`, каждая из которых — путь к файлу
* **Default**: не установлено, поэтому прокси не терминирует и не проверяет TLS

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "tlsTerminate": {}
    }
  }
}
```

Когда её устанавливают несколько учитываемых источников, Claude Code использует значение из источника с наивысшим приоритетом: управляемые настройки, затем флаг `--settings`, затем пользовательские настройки.

## Память и контекст

Контролируйте, что Claude Code загружает в контекст, как он выполняет компактизацию и где хранит память и планы. См. [Управление контекстом](https://code.claude.com/docs/ru/context-window.md) и [Память](https://code.claude.com/docs/ru/memory.md).

### `autoCompactEnabled`

Позвольте Claude Code [автоматически компактизировать беседу](https://code.claude.com/docs/ru/context-window.md#when-your-context-fills-up) при приближении контекста к лимиту. Отображается в `/config` как **Auto-compact**, и переключение его там записывает этот ключ в ваши пользовательские параметры.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code автоматически компактизирует беседу при приближении контекста к лимиту
  * `false`: Claude Code не выполняет автоматическую компактизацию
* **Default**: `true`
* **Per-session overrides**: [`DISABLE_AUTO_COMPACT`](https://code.claude.com/docs/ru/env-vars) отключает автоматическую компактизацию на одну сессию; какой бы из двух параметров её ни отключил, другой не может её включить обратно

```json settings.json theme={null}
{
  "autoCompactEnabled": false
}
```

Ручная команда `/compact` продолжает работать, пока автосжатие отключено. Если вы отключите автосжатие, [сжатие в режиме простоя](#idlecompaction) тоже отключится.

### `autoCompactWindow`

Установите, насколько полным становится окно контекста перед тем, как Claude Code [автоматически выполняет компактизацию](https://code.claude.com/docs/ru/context-window.md#when-your-context-fills-up).

* **Scope**: [`Any file`](#scopes)
* **Type**: количество токенов от `100000` до `1000000`. Claude Code ограничивает значение окном контекста вашей модели; [обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview) перечисляет окно каждой модели
* **Default**: не установлено, поэтому Claude Code выбирает окно, оптимизированное для вашей модели
* **Per-session overrides**: [`--autocompact`](https://code.claude.com/docs/ru/cli-reference#cli-flags) имеет приоритет над этим ключом на одну сессию, а [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над обоими, если только Claude Code не [игнорирует значение переменной](https://code.claude.com/docs/ru/model-config.md#claude_code_auto_compact_window-values)

```json settings.json theme={null}
{
  "autoCompactWindow": 500000
}
```

Команда [`/autocompact`](https://code.claude.com/docs/ru/commands#all-commands) сохраняет окно для текущей модели в [`modelSettings`](#modelsettings), и это значение имеет приоритет над этим ключом в том же файле для этой модели. [Установка окна автосжатия](https://code.claude.com/docs/ru/model-config.md#set-the-auto-compact-window) описывает, как взаимодействуют команда, флаг, переменная и настройка.

### `autoMemoryDirectory`

Сохраняйте [автоматическую память](https://code.claude.com/docs/ru/memory.md#storage-location) в выбранном вами каталоге вместо стандартного каталога для каждого проекта.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, абсолютный путь каталога или путь с префиксом `~/`
* **Default**: не установлено, поэтому Claude Code использует `~/.claude/projects/<project>/memory/`

```json settings.json theme={null}
{
  "autoMemoryDirectory": "~/my-memory-dir"
}
```

Из параметров проекта или локальных параметров Claude Code соблюдает этот ключ в соответствии с тем же [правилом доверия рабочей области, что и для hooks](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder), поскольку клонированный репозиторий может предоставить эти файлы.

### `autoMemoryEnabled`

Включите или отключите [автоматическую память](https://code.claude.com/docs/ru/memory.md#enable-or-disable-auto-memory). Когда `false`, Claude не читает и не записывает в каталог автоматической памяти. Вы также можете переключить её с помощью `/memory` во время сессии, что записывает этот ключ в ваши пользовательские параметры.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: то же самое, что и не установлено; автоматическая память остаётся включённой, если что-то, имеющее приоритет над этим ключом, не отключит её на сессию, например `--bare`, безопасный режим или `CLAUDE_CODE_DISABLE_AUTO_MEMORY`
  * `false`: Claude не читает и не записывает в каталог автоматической памяти
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_AUTO_MEMORY`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом на одну сессию в любом направлении

```json settings.json theme={null}
{
  "autoMemoryEnabled": false
}
```

### `bashOutputMaxChars`

Установите, сколько символов вывода успешной команды Bash или PowerShell [Claude получает встроенным образом](https://code.claude.com/docs/ru/tools-reference.md#output-limits). Когда вывод превышает лимит, Claude Code сохраняет его в файл, и Claude получает краткий предпросмотр плюс путь к файлу. Увеличьте лимит, когда вывод команды, такой как подробная сборка или полный журнал набора тестов, регулярно превышает значение по умолчанию и вы хотите, чтобы Claude прочитал его без открытия файла. Требуется Claude Code v2.1.261 или позже.

* **Scope**: [`Any file`](#scopes)
* **Type**: количество символов, положительное целое число. Claude Code ограничивает значение диапазоном `4000` на `128000`
* **Default**: не установлено, поэтому Claude получает до 30 000 символов встроенным образом

```json settings.json theme={null}
{
  "bashOutputMaxChars": 100000
}
```

Когда вы устанавливаете этот ключ, Claude Code игнорирует переменную окружения [`BASH_MAX_OUTPUT_LENGTH`](https://code.claude.com/docs/ru/env-vars).

### `claudeMd`

Внедрите инструкции в стиле CLAUDE.md как управляемую организацией память без развёртывания отдельного файла. Claude Code загружает текст как запись управляемой памяти перед файлами CLAUDE.md пользователя и проекта.

* **Scope**: [`Managed`](#scopes)
* **Type**: строка, текст файла CLAUDE.md; напишите его так, как вы бы написали файл, включая Markdown, с разрывами строк как `\n`
* **Default**: не установлено

Этот пример развёртывает два правила как короткий список Markdown:

```json managed-settings.json theme={null}
{
  "claudeMd": "# Engineering rules\n\n- Always run make lint before committing.\n- Never push directly to main."
}
```

См. [Развёртывание CLAUDE.md на уровне организации](https://code.claude.com/docs/ru/memory.md#deploy-organization-wide-claude-md).

### `claudeMdExcludes`

Пропускайте определённые файлы `CLAUDE.md` при загрузке Claude Code [памяти](https://code.claude.com/docs/ru/memory.md#exclude-specific-claude-md-files). В большом монорепозитории используйте его для пропуска файлов CLAUDE.md из других команд, которые не относятся к вашей работе; [Исключение нерелевантных файлов CLAUDE.md](https://code.claude.com/docs/ru/large-codebases.md#exclude-irrelevant-claude-md-files) в руководстве по большим кодовым базам проходит через этот случай. Шаблоны совпадают с абсолютными путями файлов.

* **Scope**: [`Any file`](#scopes)
* **Type**: массив строк, каждая из которых является шаблоном glob или абсолютным путём
* **Default**: не установлено, поэтому Claude Code загружает каждый найденный файл CLAUDE.md

```json settings.json theme={null}
{
  "claudeMdExcludes": ["**/vendor/**/CLAUDE.md"]
}
```

Исключения применяются только к файлам памяти пользователя, проекта и локальной памяти; файлы CLAUDE.md управляемой политики не могут быть исключены.

### `env`

Установите переменные окружения для каждой сессии и для подпроцессов, которые Claude Code запускает из неё. Большинство переменных в [справочнике переменных окружения](https://code.claude.com/docs/ru/env-vars.md) могут быть здесь, что позволяет применить одну к каждой сессии или развернуть её в вашей команде. Параметры проекта и локальные параметры не могут устанавливать [некоторые из них](#variables-claude-code-ignores-in-env).

* **Scope**: [`Any file`](#scopes)
* **Type**: объект, отображающий имена переменных на строковые значения
* **Default**: не установлено

Этот пример отключает автоматическую компактизацию и маршрутизирует запросы API через прокси:

```json settings.json theme={null}
{
  "env": {
    "DISABLE_AUTO_COMPACT": "1",
    "ANTHROPIC_BASE_URL": "https://proxy.example.com"
  }
}
```

#### Как значения `env` взаимодействуют с вашей оболочкой

* Значение здесь перезаписывает ту же переменную, экспортированную в вашей оболочке, и когда более одного файла настроек устанавливает переменную, применяется [наиболее приоритетный](https://code.claude.com/docs/ru/settings.md#settings-precedence). [Переменные, которые Claude Code игнорирует в `env`](#variables-claude-code-ignores-in-env) перечисляет исключения.
* Когда приложение Claude Desktop или раннер [самостоятельно размещённой среды](https://code.claude.com/docs/ru/self-hosted-environments) запускает сессию, вместо этого приоритет имеет среда запуска, которую он создаёт. Claude Code игнорирует значение `env` из файла настроек для переменной, которую эта среда уже устанавливает. [Лог отладки](https://code.claude.com/docs/ru/debug-your-config.md) может назвать игнорируемую переменную.
* Чтобы отменить экспорт оболочки, установите переменную на `""`. Claude Code рассматривает пустое значение как не установленное для выбора поставщика, и подпроцессы наследуют пустое значение.
* `NO_COLOR` и `FORCE_COLOR`, установленные здесь, достигают только подпроцессов. Чтобы изменить цвета собственного интерфейса Claude Code, установите их в вашей оболочке перед запуском `claude`.
* Значения здесь представляют собой простой текст в файле параметров и достигают каждого подпроцесса, который запускает Claude Code. Для токена OTLP, который ротируется, используйте [`otelHeadersHelper`](#otelheadershelper); для учётных данных API используйте [`apiKeyHelper`](#apikeyhelper).

#### Когда Claude Code применяет значения `env`

* Из пользовательских параметров, `--settings` и управляемых параметров: при запуске и снова в работающей сессии, когда сохранённое изменение изменяет объединённый `env`.
* Из параметров проекта и локальных параметров: после того, как вы доверяете рабочей области, или при запуске в режиме `-p`, который никогда не показывает диалог доверия, и снова, когда сохранённое изменение изменяет объединённый `env`.
* Переменные, которые Claude Code классифицирует как безопасные, такие как выбор модели, тайм-ауты и лимиты, и переключатели функций: при запуске из каждого файла параметров, кроме [переменных, которые параметры проекта и локальные параметры не могут устанавливать](#variables-claude-code-ignores-in-env).
* После того, как вы [переместите сессию с помощью `/cd`](https://code.claude.com/docs/ru/permissions#move-the-session-to-another-directory) на v2.1.246 или позже: значения `env` нового каталога проекта и локальные, поверх предыдущего каталога.

#### Переменные, которые Claude Code игнорирует в `env`

* Настройки проекта и локальные настройки не могут задавать переменные, которые не должен контролировать извлечённый репозиторий; задавайте их вместо этого в оболочке, пользовательских настройках или управляемых настройках. Claude Code отбрасывает каждую такую переменную, за исключением нескольких значений, отключающих телеметрию, и записывает в лог предупреждение, которое можно увидеть с помощью `claude --debug`. К ним относятся:

  * Переменные, определяющие, где Claude Code хранит или записывает собственные файлы: `CLAUDE_CONFIG_DIR`, `CLAUDE_CODE_TMPDIR` и переменные каталогов операционной системы, такие как `HOME`, `TMPDIR`, `TMP`, `TEMP` и семейство `XDG_*`.
  * Переменные Windows, определяющие программы и общесистемную конфигурацию для процессов, которые запускает Claude Code, такие как `SystemRoot`, `ComSpec`, `ProgramData`, `LOCALAPPDATA`, `PATHEXT`, `PSModulePath` и семейство `ProgramFiles`.
  * Переменные, экспортирующие содержимое сессии: [`OTEL_LOG_RAW_API_BODIES`](https://code.claude.com/docs/ru/env-vars#variables) и пара переменных подробной бета-трассировки `ENABLE_BETA_TRACING_DETAILED` и `BETA_TRACING_ENDPOINT`.
  * Переменные [экспортера OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage.md), которые включают телеметрию, определяют, куда она отправляется, или определяют, какое содержимое она собирает:

    * `CLAUDE_CODE_ENABLE_TELEMETRY`, а также пара переменных бета-версии расширенной телеметрии `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` и `ENABLE_ENHANCED_TELEMETRY_BETA`
    * Селекторы экспортеров `OTEL_LOGS_EXPORTER`, `OTEL_METRICS_EXPORTER` и `OTEL_TRACES_EXPORTER`
    * Переменные содержимого `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_CONTENT` и `OTEL_LOG_TOOL_DETAILS`
    * Переменные `OTEL_EXPORTER_OTLP_*`, имена которых заканчиваются на `_ENDPOINT`, `_HEADERS`, `_PROTOCOL`, `_CERTIFICATE`, `_CLIENT_KEY` или `_INSECURE`, в общей форме и в формах для отдельных сигналов, например `OTEL_EXPORTER_OTLP_ENDPOINT` и `OTEL_EXPORTER_OTLP_METRICS_HEADERS`
    * `OTEL_EXPORTER_PROMETHEUS_HOST` и `OTEL_EXPORTER_PROMETHEUS_PORT`

    Только эти значения всё ещё применяются из параметров проекта и локальных параметров, потому что они отключают что-то: `none` для трёх селекторов exporter и значение off, такое как `0` для `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_CONTENT` и `OTEL_LOG_TOOL_DETAILS`. Такое значение переопределяет ту же переменную в ваших пользовательских параметрах, но не ту, которую среда, из которой вы запускаете Claude Code, файл `--settings` или управляемые параметры устанавливают.

    Когда файл параметров проекта или локальных параметров устанавливает переменную в этой группе, локальная интерактивная сессия показывает уведомление при запуске. Запустите `/status` или `claude doctor`, чтобы увидеть, какие из них Claude Code игнорировал и какие отключили телеметрию; оба перечисляют имена, никогда значения. Неинтерактивный запуск с `-p` или сессия Agent SDK не показывает уведомление, поэтому проверьте, что ваш сборщик всё ещё получает данные после обновления. Если нет, установите переменные в ваши пользовательские параметры, управляемые параметры, среду задания или файл, который вы передаёте с помощью `--settings`.

    Игнорирование этой группы в настройках проекта и локальных настройках требует Claude Code v2.1.282 или новее.
  * Переменные, которые изменяют способ запуска или синхронизации Claude Code, такие как `CLAUDE_CODE_PROCESS_WRAPPER`, `CLAUDE_CODE_SYNC_SKILLS`, `CLAUDE_CODE_SYNC_PLUGINS`, `CLAUDE_CODE_PLUGIN_CACHE_DIR` и `CLAUDE_CODE_PLUGIN_SEED_DIR`.
  * Переменные, задающие ваш вход в claude.ai, такие как [`CLAUDE_CODE_OAUTH_TOKEN`, `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` и `CLAUDE_CODE_OAUTH_SCOPES`](https://code.claude.com/docs/ru/env-vars#variables).
  * Переменная [режима экранного диктора](https://code.claude.com/docs/ru/accessibility.md) `CLAUDE_AX_SCREEN_READER` и другие переменные, имена которых начинаются с `CLAUDE_AX_`, например [`CLAUDE_AX_STARTUP_QUIET_MS`](https://code.claude.com/docs/ru/env-vars#variables).
  * [`CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars#variables), которая задаёт таймер для диалогового окна, оставшегося без ответа.
  * [`CLAUDE_CODE_DISABLE_ATTACHMENTS`](https://code.claude.com/docs/ru/env-vars#variables), которая отключает обработку вложений.
  * [`CLAUDE_CODE_DISABLE_FILE_MENTIONS`](https://code.claude.com/docs/ru/env-vars#variables), которая не даёт Claude Code раскрывать упоминания файлов и каталогов через `@`.

  До v2.1.251 параметры проекта и локальные параметры могли также устанавливать переменные в этом списке, которые выбирают, где Claude Code записывает свои файлы или которые экспортируют содержимое сессии, кроме `HOME` и `XDG_CONFIG_HOME`. До v2.1.290 они также могли устанавливать переменные таймеров диалоговых окон и `CLAUDE_CODE_DISABLE_ATTACHMENTS`.
* Включить [Code Mode](https://code.claude.com/docs/ru/code-mode.md) с помощью [`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`](https://code.claude.com/docs/ru/env-vars#variables) можно из оболочки, пользовательских настроек или файла `--settings`, но не из управляемых настроек, настроек проекта или локальных настроек. Если `0` задан в любом из первых трёх источников или в управляемых настройках, Code Mode остаётся отключённым независимо от того, что задано в других местах. Если управляемые настройки содержат `1`, задайте собственное значение `1` в пользовательских настройках, потому что `1` в оболочке игнорируется
* Переменные идентификации, которыми владеют среды хостинга Claude Code, такие как `CLAUDE_CODE_REMOTE` и `CLAUDE_CODE_ACCOUNT_UUID`, игнорируются из каждого файла.
* [`CLAUDE_CODE_MESSAGING_SOCKET` и `CLAUDE_CODE_MESSAGING_TOKEN`](https://code.claude.com/docs/ru/env-vars#variables), которые Claude Code экспортирует сам, игнорируются из каждого файла. Игнорирование переменной сокета требует Claude Code v2.1.224 или позже, а игнорирование токена требует v2.1.228 или позже.
* [`CLAUDE_CODE_PROJECT_DIR_NAME`](https://code.claude.com/docs/ru/sessions#name-the-project-directory-yourself), которую Claude Code читает только из среды запуска, игнорируется из каждого файла; требует v2.1.234 или позже.
* [`CLAUDE_CODE_RESTRICTED`](https://code.claude.com/docs/ru/env-vars#variables), которую Claude Code читает только из среды запуска, игнорируется из каждого файла.
* [`CLAUDE_CODE_DISABLE_POWERSHELL_CMD_RM_DENY`](https://code.claude.com/docs/ru/env-vars#variables), которую Claude Code читает только из среды запуска, игнорируется из каждого файла. Переменная требует Claude Code v2.1.283 или позже.
* [`CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT`, `CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT`, `CLAUDE_CODE_DISABLE_INLINE_SHELL_RM_PROMPT` и `CLAUDE_CODE_DISABLE_MOUNTED_DRIVE_RM_PROMPT`](https://code.claude.com/docs/ru/env-vars#variables), которые Claude Code читает только из среды запуска, игнорируются в любом файле.
* [`CLAUDE_CODE_EVEN_MORE_DANGEROUSLY_SKIP_PERMISSIONS`](https://code.claude.com/docs/ru/env-vars#variables), которую Claude Code читает только из среды запуска, игнорируется в любом файле.
* [`CLAUDE_CODE_WARN_DISK_FREE_GIB` и `CLAUDE_CODE_WARN_MEMORY_FREE_GIB`](https://code.claude.com/docs/ru/env-vars#variables), которые Claude Code читает только из среды запуска, игнорируются в любом файле. Эти переменные требуют Claude Code v2.1.304 или новее.

### `fileCheckpointingEnabled`

Позвольте Claude Code создавать снимки файлов перед каждым редактированием, чтобы [`/rewind`](https://code.claude.com/docs/ru/checkpointing) мог их восстановить. Отображается в `/config` как **Rewind code (checkpoints)**, и переключение его там записывает этот ключ в ваши пользовательские параметры.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code создаёт снимки файлов перед каждым редактированием, чтобы `/rewind` мог их восстановить
  * `false`: Claude Code не создаёт снимки файлов, поэтому `/rewind` не может их восстановить
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`](https://code.claude.com/docs/ru/env-vars) отключает checkpointing на одну сессию; какой бы из двух параметров его ни отключил, другой не может его включить обратно

```json settings.json theme={null}
{
  "fileCheckpointingEnabled": false
}
```

В запуске `-p` или сессии Agent SDK Claude Code игнорирует этот ключ. SDK включает checkpointing с помощью своей опции `enableFileCheckpointing`, и простой запуск `-p` требует `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true`. См. [File checkpointing в Agent SDK](https://code.claude.com/docs/ru/agent-sdk/file-checkpointing.md).

### `idleCompaction`

Сжатие в режиме простоя [сжимает](https://code.claude.com/docs/ru/context-window.md#what-survives-compaction) длинный диалог, от которого вы отошли. Тогда ваше следующее сообщение отправляет сводку вместо всего диалога. После сжатия в диалоге отображается уведомление:

* **Терминал**: строка, начинающаяся с `Compacted while idle, before the prompt cache expired`
* **[Панель чата VS Code](#idle-compaction-in-vs-code-and-the-desktop-app)**: уведомление, содержащее `a summary written while you were away`
* **[Настольное приложение](#idle-compaction-in-vs-code-and-the-desktop-app)**: то же уведомление внутри строки, метка которой содержит `Claude Code notice`. Если вы не видите эту строку или её текст, переключитесь в [режим просмотра Verbose](https://code.claude.com/docs/ru/desktop.md#switch-view-modes).

Сжатие в режиме простоя включено по умолчанию для диалогов, которые соответствуют всем следующим условиям:

* **Сессия**: вы находитесь в интерактивной сессии терминала, в панели чата расширения VS Code или на вкладке Code настольного приложения, если сессия выполняется на вашем компьютере или через SSH
* **Автосжатие**: [`autoCompactEnabled`](#autocompactenabled) включён
* **Кэш промптов**: диалог использует [часовой TTL кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md#which-ttl-each-request-gets)
* **Размер**: контекст диалога достиг порога токенов, который вы можете [изменить](#change-the-idle-compaction-threshold) со значения по умолчанию 200 000
* **Время простоя**: с момента последнего запроса прошло около часа, и до этого момента ваш компьютер не переходит в спящий режим

Чтобы отключить сжатие в режиме простоя, установите этот ключ в `false`.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code сжимает простаивающие диалоги, которые соответствуют условиям
  * `false`: Claude Code не выполняет сжатие, пока ваша сессия простаивает
* **Default**: `true`
* **Per-session overrides**: [`DISABLE_AUTO_COMPACT`](https://code.claude.com/docs/ru/env-vars) отключает сжатие в режиме простоя вместе с автосжатием

```json settings.json theme={null}
{
  "idleCompaction": false
}
```

Чтобы отключить или включить сжатие в режиме простоя прямо в сессии терминала, запустите `/config` и измените строку **Idle compaction**. Ваш выбор сохраняется в пользовательских настройках и применяется сразу. Эта строка требует Claude Code v2.1.302 или позже. Если вы используете одну из этих версий, а `/config` не показывает эту строку, проверьте следующие причины:

* **Ключ задан в другом источнике настроек**: значение в управляемых настройках, флаге `--settings` или файле настроек проекта или локальных настроек переопределяет ваши пользовательские настройки. Измените ключ в этом источнике
* **Флаги функций недоступны в версии до v2.1.314**: там, где Claude Code не может [получать флаги функций от Anthropic](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), сжатие в режиме простоя не выполняется, поэтому отключать нечего

Ключ требует Claude Code v2.1.290 или позже. В более ранней версии, которая игнорирует этот ключ, отключите [`autoCompactEnabled`](#autocompactenabled), чтобы остановить сжатие в режиме простоя.

#### Изменение порога сжатия в режиме простоя

Установите в [`CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`](https://code.claude.com/docs/ru/env-vars) количество токенов, которого должен достичь контекст диалога, чтобы к нему применялось сжатие в режиме простоя. Используйте положительное целое число. Значения ниже `100000` повышаются до `100000` — минимального порога.

При значении по умолчанию диалог с контекстным окном 200K автоматически сжимается до того, как достигнет 200 000 токенов. Этот пример снижает порог до 150 000, чтобы такие диалоги соответствовали условию:

```json settings.json theme={null}
{
  "env": {
    "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS": "150000"
  }
}
```

#### Сжатие в режиме простоя в VS Code и настольном приложении

Подобное уведомление означает, что Claude Code [заменил ваш предыдущий диалог сводкой](https://code.claude.com/docs/ru/context-window.md#what-survives-compaction), с которой теперь работает Claude:

```text theme={null}
Compacted using a summary written while you were away · turn off with "idleCompaction": false in settings.json
```

Вам не нужно ничего делать. Чтобы отключить сжатие в режиме простоя, установите `idleCompaction` в `false` в `~/.claude/settings.json` на компьютере или в дистрибутиве WSL, где выполняется сессия, или в другом [файле настроек](https://code.claude.com/docs/ru/settings.md#settings-files-and-who-they-affect).

### `plansDirectory`

Выберите, где Claude Code хранит файлы плана, которые он записывает в [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode). Claude Code разрешает путь относительно корня проекта.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, путь относительно корня проекта
* **Default**: не установлено, поэтому Claude Code использует `~/.claude/plans`

```json settings.json theme={null}
{
  "plansDirectory": "./plans"
}
```

Claude Code хранит планы в `~/.claude/plans` вместо заданного вами каталога, например, в следующих случаях:

* **Вне корня проекта**: путь разрешается за пределами корня проекта, как в случае `"../plans"`.
* **Обратная косая черта в macOS, Linux и WSL**: разрешённый путь содержит обратную косую черту, как в пути в стиле Windows `"docs\\plans"`. Пишите `"docs/plans"` — такой путь работает и в Windows.

### `skillListingBudgetFraction`

Каждый ход Claude видит [список ваших skills](https://code.claude.com/docs/ru/skills.md#skill-descriptions-are-cut-short) с их описаниями, и Claude Code ограничивает этот список долей окна контекста. Когда список превышает лимит, Claude Code сохраняет имя каждого skill, но отбрасывает описания наименее используемых skills, поэтому Claude всё ещё может вызывать эти skills, но менее вероятно выбрать один самостоятельно. Увеличьте этот ключ, чтобы сохранить больше описаний видимыми за счёт большего контекста за ход.

* **Scope**: [`Any file`](#scopes)
* **Type**: число, доля больше `0` и не более `1`
* **Default**: `0.01`, что резервирует 1% окна контекста

```json settings.json theme={null}
{
  "skillListingBudgetFraction": 0.02
}
```

Чтобы увидеть, сколько контекста использует список и какие skills вносят наибольший вклад, запустите `/doctor`.

### `skillListingMaxDescChars`

Каждый ход Claude видит [список ваших skills](https://code.claude.com/docs/ru/skills.md#skill-descriptions-are-cut-short), который показывает текст `description` и `when_to_use` каждого skill. Этот ключ ограничивает, сколько символов этого текста Claude Code показывает для каждого skill; более длинный текст обрезается на лимите.

* **Scope**: [`Any file`](#scopes)
* **Type**: количество символов, положительное целое число
* **Default**: `1536`

```json settings.json theme={null}
{
  "skillListingMaxDescChars": 2048
}
```

Увеличьте его, чтобы сохранить длинные описания нетронутыми за счёт большего контекста за ход; уменьшите его, чтобы вместить больше skills под [`skillListingBudgetFraction`](#skilllistingbudgetfraction).

### `taskOutputMaxChars`

> [!WARNING]
>
> Удалено в v2.1.277 вместе с инструментом `TaskOutput`, который он определял. Установка этого параметра не влияет на текущие версии. Claude читает [файл вывода](https://code.claude.com/docs/ru/tools-reference.md#background-commands) фонового задания с помощью `Read` вместо этого.

До v2.1.276 вы устанавливали этот ключ на количество символов вывода [фонового задания](https://code.claude.com/docs/ru/tools-reference.md#background-commands), которое Claude получал встроенным образом, когда читал задание с помощью инструмента `TaskOutput`.

## Интерфейс и терминал

Изменяйте внешний вид и поведение Claude Code в терминале: тему, режим редактора, строку состояния, спиннер, уведомления внутри сессии и специальные возможности. См. [Настройка терминала](https://code.claude.com/docs/ru/terminal-config.md).

### `askUserQuestionTimeout`

Позволяет диалоговому окну [`AskUserQuestion`](https://code.claude.com/docs/ru/tools-reference), оставшемуся без ответа, автоматически продолжить работу после периода бездействия, отправив те варианты, которые вы уже выбрали. Задайте этот параметр, если вы отходите и хотите, чтобы Claude продолжал без вас. При значении по умолчанию вопросы ждут, пока вы на них не ответите. О том, когда таймер приостанавливается или вообще не запускается, см. [Таймаут автопродолжения вопроса](https://code.claude.com/docs/ru/tools-reference.md#question-auto-continue-timeout).

* **Область действия**: [`User or managed`](#scopes)
* **Тип**: строка, одно из значений `"60s"`, `"5m"`, `"10m"` или `"never"`
* **По умолчанию**: `"never"`

```json settings.json theme={null}
{
  "askUserQuestionTimeout": "5m"
}
```

Отображается в `/config` как **Question auto-continue timeout** и записывает этот ключ в пользовательские настройки; Claude Code скрывает эту строку, когда ключ задан управляемыми настройками или флагом `--settings`.

### `autoContinueAtUsageLimit`

После того как лимит использования claude.ai останавливает вашу сессию, Claude Code ожидает в открытой сессии и автоматически продолжает задачу после сброса лимита. См. [Отключение автоматического продолжения](https://code.claude.com/docs/ru/interactive-mode.md#turn-automatic-continue-off). Требуется Claude Code v2.1.234 или новее.

* **Область действия**: [`User or managed`](#scopes). Считывается только из пользовательских настроек, `--settings` и управляемых настроек. Если ни один из этих источников не задаёт ключ, файл настроек проекта или локальный файл настроек, задающий его, отключает функцию, а не игнорируется.
* **Тип**: Boolean
  * `true`: после того как лимит использования claude.ai останавливает вашу сессию, Claude Code ожидает в открытой сессии и автоматически продолжает задачу после сброса лимита
  * `false`: Claude Code не начинает ожидание самостоятельно. Вы по-прежнему можете [запустить ожидание сами](https://code.claude.com/docs/ru/interactive-mode.md#start-a-wait-yourself) из меню вариантов, связанных с лимитом использования
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "autoContinueAtUsageLimit": false
}
```

Отображается в `/config` как **Continue automatically at usage limit** и записывает этот ключ в пользовательские настройки; Claude Code скрывает эту строку, когда ключ задан управляемыми настройками или флагом `--settings`.

### `autoScrollEnabled`

Следовать за новым выводом к нижней части диалога в [полноэкранном режиме отображения](https://code.claude.com/docs/ru/fullscreen.md).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: диалог следует за новым выводом к нижней части
  * `false`: вы остаётесь там, куда прокрутили, пока Claude продолжает работать; запросы разрешений по-прежнему появляются под транскриптом
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "autoScrollEnabled": false
}
```

Отображается в `/config` как **Auto-scroll**, когда включён полноэкранный режим отображения, и записывает этот ключ в пользовательские настройки.

### `axScreenReader`

Выводить текст, удобный для программ экранного доступа: простой текст без декоративных рамок и анимаций. Режим экранного доступа использует классический рендерер, поэтому настройка `tui` не действует, пока он активен; подключённые [фоновые сессии](https://code.claude.com/docs/ru/agent-view.md) по-прежнему отображаются в полноэкранном режиме.

* **Область действия**: [`User or managed`](#scopes). Ключ также можно задать в файле, передаваемом через `--settings`. Claude Code игнорирует ключ в настройках проекта и локальных настройках, поэтому ни репозиторий, ни ваш собственный `.claude/settings.local.json` не могут включить или отключить режим экранного доступа.
* **Тип**: Boolean
  * `true`: Claude Code выводит простой текст без декоративных рамок и анимаций, используя классический рендерер
  * `false`: Claude Code отображает интерфейс обычным образом
* **По умолчанию**: не задано, поэтому режим экранного доступа отключён
* **Переопределения для отдельной сессии**: [`--ax-screen-reader`](https://code.claude.com/docs/ru/cli-reference#cli-flags) имеет приоритет над [`CLAUDE_AX_SCREEN_READER`](https://code.claude.com/docs/ru/env-vars), и оба имеют приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "axScreenReader": true
}
```

### `bashEditDiffEnabled`

Определяет, будет ли Claude Code фиксировать, какие файлы в Git-репозитории изменились во время выполнения команды Bash. Когда он их фиксирует, вы видите их diff в терминале после команды, а ваши [хуки PostToolUse для Bash](https://code.claude.com/docs/ru/hooks.md#bash) получают список изменённых файлов.

Файл в списке не всегда изменён именно этой командой. Там также может оказаться изменение, внесённое другой программой или другим вызовом Bash во время выполнения команды.

Установите ключ в `true`, чтобы фиксировать их во всех режимах разрешений. Требуется Claude Code v2.1.269 или новее.

* **Область действия**: [`User or managed`](#scopes). Значение `true` учитывается только из ваших пользовательских настроек, JSON, переданного через `--settings`, или [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md), поэтому `true` в файлах репозитория `.claude/settings.json` или `.claude/settings.local.json` не может включить фиксацию. Значение `false` в любом из этих файлов репозитория всё же отключает её, если только файл с [более высоким приоритетом](https://code.claude.com/docs/ru/settings.md#settings-precedence) не задаёт `true`.
* **Тип**: Boolean
* **По умолчанию**: не задано, поэтому Claude Code фиксирует изменения в авторежиме и режиме `bypassPermissions`, когда направляет Claude редактировать файлы через Bash
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_BASH_EDIT_DIFF`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "bashEditDiffEnabled": true
}
```

### `companyAnnouncements`

Показывать пользователям объявления вашей организации при запуске. Если вы укажете больше одного, Claude Code выбирает одно случайным образом для каждой сессии; при самом первом запуске у человека показывается первая запись.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: массив строк
* **По умолчанию**: не задано, поэтому объявления не показываются

```json settings.json theme={null}
{
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.example.com"
  ]
}
```

### `defaultShell`

Определяет, будет ли Bash или PowerShell выполнять shell-команды, которые вы вводите с [префиксом `!`](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix) в поле ввода, — те, которые Claude Code выполняет напрямую и добавляет в сессию.

`"powershell"` работает, только пока включён [инструмент PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool). Инструмент включён по умолчанию в Windows без Git Bash, а также в Windows с Git Bash для учётных записей claude.ai и Console. В сессиях Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry, а также в macOS, Linux и WSL установите `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`, чтобы включить инструмент. Установите эту переменную в `0`, чтобы отключить инструмент.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"bash"`: Claude Code выполняет ваши команды `!` в Bash
  * `"powershell"`: Claude Code выполняет ваши команды `!` в PowerShell
* **По умолчанию**: `"bash"` или `"powershell"` в Windows, когда Bash недоступен

```json settings.json theme={null}
{
  "defaultShell": "powershell"
}
```

Если указанная оболочка недоступна, Claude Code использует другую: `"powershell"` переключается на Bash, когда инструмент PowerShell отключён, а `"bash"` переключается на PowerShell, когда Bash не установлен.

### `dialogExpiry`

Задаёт крайний срок для диалоговых окон, которые Claude Code [перенаправляет удалённому клиенту](https://code.claude.com/docs/ru/remote-control.md#limitations), например хосту Remote Control или SDK, а также для диалогового окна подтверждения [задержанного межсессионного сообщения](https://code.claude.com/docs/ru/cross-session-messaging.md#control-inbound-messages). В Claude Code v2.1.236 или новее тот же крайний срок ограничивает запрос согласия на [кредиты использования Fable](https://code.claude.com/docs/ru/model-config.md#fable-and-usage-credits), появляющийся посреди сессии, в которой у терминала может никого не быть. Если ответ не поступает до истечения срока, Claude Code закрывает диалоговое окно и продолжает с вариантом по умолчанию, не предполагающим действий. Требуется Claude Code v2.1.224 или новее.

* **Область действия**: [`User or managed`](#scopes)
* **Тип**: строка, одно из значений `"60s"`, `"5m"`, `"10m"` или `"never"`, которое отключает крайний срок
* **По умолчанию**: `"5m"`
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "dialogExpiry": "10m"
}
```

Запросы разрешений и вопросы [`AskUserQuestion`](https://code.claude.com/docs/ru/tools-reference#askuserquestion-tool-behavior) используют собственные механизмы и не подчиняются этому крайнему сроку. Отображается в `/config` как **Dialog expiry** и записывает этот ключ в пользовательские настройки; для этой строки требуется Claude Code v2.1.232 или новее, и Claude Code скрывает её, когда ключ задан управляемыми настройками или флагом `--settings`.

### `editorMode`

Выбор режима сочетаний клавиш для поля ввода промпта.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"normal"`: стандартные сочетания клавиш в поле ввода промпта
  * `"vim"`: редактирование в стиле vim с режимами NORMAL, INSERT и VISUAL
* **По умолчанию**: `"normal"`

```json settings.json theme={null}
{
  "editorMode": "vim"
}
```

Отображается в `/config` как **Editor mode** и записывает этот ключ в пользовательские настройки.

### `emojiCompletionEnabled`

Показывать подсказки эмодзи, когда вы вводите `:` и короткий код в поле ввода промпта, и заменять завершённый короткий код, например `:heart:`, на соответствующий эмодзи. Установите `false`, чтобы отключить и то, и другое.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code показывает подсказки эмодзи после `:` и заменяет завершённый короткий код на эмодзи
  * `false`: Claude Code не предлагает эмодзи и не заменяет короткие коды
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "emojiCompletionEnabled": false
}
```

См. [Короткие коды эмодзи](https://code.claude.com/docs/ru/interactive-mode.md#emoji-shortcodes).

### `fileSuggestion`

Запускать собственную команду для автодополнения путей к файлам после `@` вместо встроенных подсказок файлов. Встроенные подсказки используют быстрый обход файловой системы; для большого монорепозитория может подойти лучше индексация под конкретный проект, например заранее построенный индекс файлов.

* **Область действия**: [`Any file`](#scopes). При действии [ограничений для строки состояния и подсказок файлов](#status-line-and-file-suggestion-gates) Claude Code отключает команду или выполняет только управляемое значение и без предупреждения пропускает ваше.
* **Тип**: объект с полями `type`, всегда `"command"`, и `command` — shell-командой для запуска
* **По умолчанию**: не задано, поэтому Claude Code использует встроенные подсказки файлов

```json settings.json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

После сохранения введите в промпте `@`, а затем часть пути: подсказки будут браться из вывода вашей команды.

#### Ввод и вывод команды

Claude Code запускает команду с теми же переменными окружения, что и [хуки](https://code.claude.com/docs/ru/hooks.md), включая `CLAUDE_PROJECT_DIR`, и перестаёт ждать через пять секунд. Команда получает JSON через stdin с полем `query`, содержащим то, что вы уже ввели:

```json theme={null}
{"query": "src/comp"}
```

Выводите в stdout пути к файлам, разделённые переводом строки. Claude Code показывает не более 15:

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

Следующий скрипт считывает запрос и передаёт его индексу файлов репозитория:

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
# Replace your-repo-file-index with your own file search command
your-repo-file-index --query "$query" | head -20
```

### `footerLinksRegexes`

Отображать дополнительные кликабельные значки в нижней панели под полем ввода, когда регулярное выражение совпадает с выводом хода: результатами инструментов, включая содержимое файлов и загруженные страницы, и собственными ответами Claude. Используйте это, чтобы превращать идентификаторы, которые выводят CLI проекта, например инструменты ревью и трекеры задач, в ссылки в сессии.

* **Область действия**: [`User or managed`](#scopes)
* **Тип**: массив объектов, в каждом из которых `type` имеет значение `"regex"`, есть регулярное выражение `pattern`, шаблон `url` и необязательное поле `label`; плейсхолдеры `{name}` в `url` и `label` заполняются из именованных групп захвата в `pattern`
* **По умолчанию**: не задано, поэтому значки не отображаются

Этот пример находит ключи задач, такие как `PROJ-1234`, и строит каждую ссылку из захваченного ключа:

```json settings.json theme={null}
{
  "footerLinksRegexes": [
    {
      "type": "regex",
      "pattern": "\\b(?<key>PROJ-\\d+)\\b",
      "url": "https://issues.example.com/browse/{key}",
      "label": "{key}"
    }
  ]
}
```

С такой конфигурацией, когда `PROJ-1234` появляется в результате инструмента или в ответе Claude, в нижней панели появляется значок `PROJ-1234`, ссылающийся на `https://issues.example.com/browse/PROJ-1234`.

#### Ограничения значков

URL, метка и количество значков для каждой записи ограничены следующим образом:

| Ограничение | Поведение |
| :- | :- |
| Источник URL | Захваченные значения кодируются для URL, и построенный URL должен иметь тот же буквальный источник (origin), что и шаблон. Захват может заполнить сегмент пути или значение параметра запроса, но не может изменить, куда ведёт ссылка |
| Длина URL | Построенные URL длиннее 2048 символов отбрасываются |
| Схема URL | Должна быть `https`, `http` или распознаваемой схемой глубоких ссылок редактора или рабочего пространства: `vscode`, `vscode-insiders`, `cursor`, `windsurf`, `zed`, `jetbrains`, `idea`, `slack`, `linear`, `notion`, `figma` |
| Метка | По умолчанию — совпавший текст; усекается до 28 экранных столбцов |
| Количество значков | Отображается не более 5 значков. Самый старый вытесняется новыми совпадениями, а `/clear` удаляет их |

Когда ход завершается, Claude Code сопоставляет регулярное выражение `pattern` каждой записи с выводом хода в основном потоке, поэтому медленное регулярное выражение блокирует интерфейс, пока не завершится. Вложенные квантификаторы, такие как `(a+)+$`, на определённых входных данных могут выполняться экспоненциально долго и зависать сессию, поэтому делайте каждый `pattern` линейным и избегайте вложенных `+` или `*`.

Значки нижней панели отображаются вместе с [пользовательской строкой состояния](https://code.claude.com/docs/ru/statusline.md), если она настроена; ни одно не заменяет другое. Используйте строку состояния для строки, управляемой скриптом, которая вычисляет собственное содержимое на основе данных сессии, а значки нижней панели — чтобы превращать идентификаторы из диалога в ссылки без скрипта.

### `keybindingFlavor`

> [!WARNING]
>
> Объявлен устаревшим начиная с v2.1.261 и ни на что не влияет. Клавиши редактирования слов в промпте всегда [следуют соглашениям readline](https://code.claude.com/docs/ru/interactive-mode.md#make-ctrl-w-delete-back-to-whitespace), как в Bash. Claude Code по-прежнему принимает `keybindingFlavor`, поэтому файл настроек, задающий его, остаётся валидным.

В версиях с v2.1.238 по v2.1.260 значение `"readline"` заставляло `Ctrl+W` удалять текст до предыдущего пробельного символа, а не только предыдущее слово.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, `"classic"` или `"readline"`
* **По умолчанию**: не задано

### `maxProseWidth`

Ограничивает ширину текста в ответах Claude, чтобы строки оставались удобочитаемыми в широком терминале. Абзацы, заголовки, списки и цитаты переносятся в пределах этого числа столбцов, а таблицы и блоки кода сохраняют полную ширину терминала. Требуется Claude Code v2.1.282 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: число столбцов терминала, целое число, минимум `40`. Claude Code игнорирует любые другие значения
* **По умолчанию**: не задано, поэтому текст переносится по краю терминала

```json settings.json theme={null}
{
  "maxProseWidth": 80
}
```

### `prefersReducedMotion`

Уменьшить или отключить анимации интерфейса, такие как спиннер, мерцание и эффекты вспышки. Отображается в `/config` как **Reduce motion**.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code уменьшает или отключает анимации интерфейса, такие как спиннер, мерцание и эффекты вспышки
  * `false`: то же, что и отсутствие значения; Claude Code показывает свои анимации
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "prefersReducedMotion": true
}
```

### `promptSuggestionEnabled`

Показывать или скрывать [подсказки промптов](https://code.claude.com/docs/ru/interactive-mode.md#prompt-suggestions) — серые предсказания, которые появляются в поле ввода промпта. Установите `false` или отключите **Prompt suggestions** в `/config`, чтобы скрыть их.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: вы видите подсказки промптов в поле ввода промпта
  * `false`: Claude Code скрывает подсказки промптов
* **По умолчанию**: `true`
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "promptSuggestionEnabled": false
}
```

Для подсказок промптов нужна учётная запись claude.ai или Console с включённой телеметрией. В Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry, а также при отключённой телеметрии, например через [`DISABLE_TELEMETRY`](https://code.claude.com/docs/ru/env-vars), этот ключ не действует, и включить подсказки может только `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=1`.

### `respectGitignore`

Определяет, исключает ли средство выбора файлов `@` файлы, соответствующие шаблонам `.gitignore`. Отображается в `/config` как **Respect .gitignore in file picker**.

* **Область действия**: [`Any file`](#scopes). Если ни один файл настроек не задаёт этот ключ, Claude Code использует `respectGitignore` из `~/.claude.json`, куда его записывает переключатель в `/config`.
* **Тип**: Boolean
  * `true`: средство выбора файлов `@` исключает файлы, соответствующие шаблонам `.gitignore`
  * `false`: средство выбора файлов `@` включает файлы, соответствующие шаблонам `.gitignore`
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "respectGitignore": false
}
```

### `respondToBashCommands`

Определяет, отвечает ли Claude после того, как вы выполните shell-команду с [префиксом `!`](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix) в поле ввода. По умолчанию Claude Code добавляет вывод команды в диалог, и Claude на него отвечает. Установите этот ключ в `false`, чтобы добавлять вывод в контекст без ответа — так вы сможете выполнить несколько команд и спросить о них вместе.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code добавляет вывод команды в диалог, и Claude на него отвечает
  * `false`: Claude Code добавляет вывод в контекст без ответа
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "respondToBashCommands": false
}
```

См. [Режим оболочки с префиксом `!`](https://code.claude.com/docs/ru/interactive-mode#shell-mode-with-prefix).

### `showClearContextOnPlanAccept`

Когда Claude завершает план в [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#review-and-approve-a-plan), он показывает меню подтверждения. Планирование может использовать много контекста, поэтому этот ключ добавляет в это меню первый вариант, **Yes, clear context and …**, который утверждает план, очищает контекст диалога и начинает реализацию, опираясь только на план. Оставшаяся часть метки называет режим разрешений, в котором продолжится сессия, и показывает, какую часть контекста использовало планирование.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: меню подтверждения плана получает первый вариант, **Yes, clear context and …**, который утверждает план и очищает контекст диалога
  * `false`: меню подтверждения плана не показывает вариант очистки контекста
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "showClearContextOnPlanAccept": true
}
```

### `showTurnDuration`

Показывать или скрывать сообщение о длительности хода после каждого ответа, например «Cooked for 1m 6s · done 6:05 PM». Время после «done» показывает, когда ход завершился; [`timeFormat`](#timeformat) и [`timeZone`](#timezone) управляют его форматом и часовым поясом. Отображается в `/config` как **Show turn duration**.

* **Область действия**: [`Any file`](#scopes). Значение в `~/.claude.json` из более старой версии применяется, если ни один файл настроек не задаёт этот ключ.
* **Тип**: Boolean
  * `true`: вы видите сообщение о длительности хода после каждого ответа
  * `false`: Claude Code скрывает сообщение о длительности хода
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "showTurnDuration": false
}
```

### `spellcheck`

Подчёркивать слова с ошибками в поле ввода промпта по мере ввода, используя установленную вами программу проверки орфографии. Claude Code проверяет только текст в поле ввода. В разделе [Проверка орфографии по мере ввода](https://code.claude.com/docs/ru/interactive-mode.md#check-spelling-as-you-type) описаны установка aspell, hunspell или ispell и то, что проверяет программа проверки. Требуется Claude Code v2.1.235 или новее.

* **Область действия**: [`User or managed`](#scopes). Блок из уровня с наивысшим приоритетом, который его задаёт, применяется целиком.
* **Тип**: объект с полями `enabled` (Boolean), `checker` (`"aspell"`, `"hunspell"`, `"ispell"` или `"auto"`), `language` (строка, передаётся программе проверки как имя словаря) и `color` (строка: название цвета терминала, `#rrggbb`, `rgb(r,g,b)`, `ansi256(n)` или `ansi:<name>`)
* **По умолчанию**: не задано, поэтому проверка орфографии отключена; `checker` по умолчанию `"auto"` — первая из трёх программ, найденная в `PATH`; `language` по умолчанию — собственный словарь программы проверки; `color` по умолчанию — цвет ошибок из темы

```json settings.json theme={null}
{
  "spellcheck": { "enabled": true, "language": "en_GB" }
}
```

### `spinnerTipsEnabled`

Пока Claude работает, строка спиннера поочерёдно показывает короткие советы о возможностях Claude Code, например «Use Plan Mode to prepare for a complex request before making changes. Press Shift+Tab twice to enable.» Установите этот ключ в `false`, чтобы скрыть их. Отображается в `/config` как **Show tips**.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: вы видите советы в спиннере, пока Claude работает
  * `false`: Claude Code скрывает советы в спиннере
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "spinnerTipsEnabled": false
}
```

### `spinnerTipsOverride`

Добавить собственные советы к [советам в спиннере](#spinnertipsenabled), которые Claude Code показывает, пока Claude работает, или заменить встроенные советы своими. Claude Code включает ваши советы в ту же ротацию, что и встроенные.

Если вы установите [`spinnerTipsEnabled`](#spinnertipsenabled) в `false`, Claude Code скроет все советы, включая ваши.

* **Область действия**: [`Any file`](#scopes). Claude Code учитывает объекты советов, `tipsFile`, `label` и `excludeDefault` из пользовательских настроек, флага `--settings` и управляемых настроек; из настроек проекта и локальных настроек он считывает только простые строковые советы.
* **Тип**: объект с полями `tips`, `tipsFile`, `label` и `excludeDefault`, каждое необязательное
* **По умолчанию**: не задано, поэтому Claude Code показывает только встроенные советы

Для объектов советов, `tipsFile`, `label` и правила из строки «Область действия» о том, что настройки проекта и локальные настройки добавляют только простые строки, требуется Claude Code v2.1.247 или новее.

Каждая запись `tips` — это простая строка или объект со следующими полями:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `id` | Да | До 64 букв, цифр, `.`, `_` или `-`. Claude Code привязывает к нему историю показов совета, поэтому период ожидания совета сохраняется при изменении порядка списка. Из двух записей с одинаковым id Claude Code использует первую |
| `text` | Да | Совет — одна строка длиной до 500 символов. Claude Code удаляет escape-последовательности ANSI и управляющие символы и сжимает пробельные символы |
| `cooldownSessions` | Нет | Количество сессий, которое Claude Code ждёт перед повторным показом совета, от `0` до `1000`, по умолчанию `0` |
| `priority` | Нет | Порядок среди советов, которые не показывались одинаково долго; больший приоритет идёт первым, от `-10` до `10`, по умолчанию `0` |

Claude Code считывает простую строку как совет с этими значениями по умолчанию и id на основе позиции, поэтому её история показов сбрасывается при изменении порядка списка. Задайте совету `id`, чтобы сохранять его историю при правках.

Claude Code считывает не более 200 советов из `tips` и `tipsFile` в сумме и отбрасывает недопустимую запись с отладочным предупреждением вместо того, чтобы отклонять файл настроек.

Используйте оставшиеся поля, чтобы указать файл советов, задать префикс и скрыть встроенные советы:

* `tipsFile`: абсолютный путь или путь вида `~/` к локальному JSON-файлу, содержащему массив таких же записей или объект с массивом `tips`, размером до 256 KB. Claude Code считывает файл один раз за процесс, поэтому ваши правки загружаются при следующем запуске. Его нельзя задать через [серверные управляемые настройки](https://code.claude.com/docs/ru/server-managed-settings.md); разворачивайте там встроенные `tips` или разверните путь в файле `managed-settings.json` на диске.
* `label`: префикс, который Claude Code показывает перед советами из пользовательских настроек, `--settings` и управляемых настроек, до 40 символов. По умолчанию — `Tip`, тот же префикс, что и у встроенных советов; советы из настроек проекта и локальных настроек всегда используют его.
* `excludeDefault`: установите `true`, чтобы скрыть встроенные советы и показывать только ваши. Если Claude Code не может загрузить ни одного вашего совета, например потому что `tipsFile` не существует или все записи недопустимы, он сохраняет встроенную ротацию вместо пустого спиннера.

Если ключ задан в нескольких файлах настроек, Claude Code показывает советы из всех них, а `tipsFile`, `label` и `excludeDefault` берёт из того источника — управляемых настроек, флага `--settings` или пользовательских настроек, — который имеет наивысший приоритет среди задающих каждое из этих полей.

Этот пример в ваших пользовательских настройках добавляет в ротацию простой строковый совет и совет-объект с префиксом `Acme tip`:

```json settings.json theme={null}
{
  "spinnerTipsOverride": {
    "label": "Acme tip",
    "tips": [
      "Run /review before opening a PR",
      {
        "id": "gateway-errors",
        "text": "Seeing 5xx errors? Check the gateway status page first",
        "cooldownSessions": 5,
        "priority": 2
      }
    ]
  }
}
```

Каждое поле в примере меняет одну особенность того, как Claude Code показывает советы:

* `label`: Claude Code показывает оба совета как `Acme tip: ...` вместо `Tip: ...`.
* Простая строка: Claude Code присваивает ей значения по умолчанию, поэтому она может появиться снова уже в следующей сессии.
* `id`: Claude Code привязывает историю показов второго совета к `gateway-errors`, поэтому его период ожидания сохраняется после добавления или изменения порядка советов.
* `cooldownSessions`: после того как Claude Code покажет совет `gateway-errors`, он не покажет его снова в течение пяти сессий.
* `priority`: когда совет `gateway-errors` и другой совет не показывались одинаковое число сессий, например когда ни один из них ещё не был показан, Claude Code сначала показывает `gateway-errors`. Простая строка имеет приоритет по умолчанию, `0`.

Пока Claude работает, Claude Code показывает ваши советы в спиннере с вашим префиксом, например `Acme tip: Run /review before opening a PR`.

### `spinnerVerbs`

Пока ход выполняется, спиннер показывает сменяющийся глагол, например «Accomplishing», «Architecting» или «Baking». Используйте этот ключ, чтобы добавить в эту ротацию собственные глаголы или заменить встроенный список своим.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект с массивом строк `verbs` и полем `mode`, одно из значений:
  * `"append"`: Claude Code добавляет ваши глаголы к встроенному набору
  * `"replace"`: Claude Code показывает только ваши глаголы
* **По умолчанию**: не задано, поэтому Claude Code использует встроенные глаголы

Этот пример добавляет два глагола к встроенному набору:

```json settings.json theme={null}
{
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting"]
  }
}
```

В режиме `"replace"` с пустым массивом `verbs` Claude Code сохраняет встроенные глаголы.

### `statusLine`

Запускать собственную команду для отображения [строки состояния](https://code.claude.com/docs/ru/statusline.md) под промптом с контекстной информацией, такой как модель, стоимость или ветка git. Необязательные поля настраивают отступы, добавляют периодический перезапуск и скрывают встроенный индикатор режима vim, когда ваш скрипт сам отображает `vim.mode`.

* **Область действия**: [`Any file`](#scopes). Когда включён [`allowManagedHooksOnly`](#allowmanagedhooksonly) или [`disableAllHooks`](#disableallhooks) задан вне управляемых настроек, выполняется только значение из управляемых настроек.
* **Тип**: объект, где `type` имеет значение `"command"` и есть строка `command`, а также необязательные `padding` — число символов, `refreshInterval` — число секунд, минимум `1`, и `hideVimModeIndicator` — Boolean
* **По умолчанию**: не задано, поэтому строки состояния нет

Этот пример выводит название модели и использование контекста и добавляет два символа горизонтального отступа:

```json settings.json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'",
    "padding": 2
  }
}
```

Для примера требуется установленный [`jq`](https://jqlang.org/), и он выполняется в оболочке. Аналоги для PowerShell и Git Bash см. в разделе [Настройка в Windows](https://code.claude.com/docs/ru/statusline.md#windows-configuration); полную настройку см. в разделе [Ручная настройка строки состояния](https://code.claude.com/docs/ru/statusline.md#manually-configure-a-status-line).

### `syntaxHighlightingDisabled`

Claude Code раскрашивает код в соответствии с языком в diff, блоках кода и предпросмотрах файлов, которые он показывает в терминале, с помощью встроенного средства подсветки. Установите этот ключ в `true`, чтобы показывать их как простой текст, например если цвета конфликтуют с темой вашего терминала или замедляют программу экранного доступа.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code отключает подсветку синтаксиса в diff, блоках кода и предпросмотрах файлов
  * `false`: Claude Code подсвечивает синтаксис
* **По умолчанию**: `false`

```json settings.json theme={null}
{
  "syntaxHighlightingDisabled": true
}
```

### `terminalProgressBarEnabled`

Некоторые терминалы могут показывать индикатор прогресса на вкладке или на панели задач для запущенной в них программы. Пока Claude работает, Claude Code сообщает терминалу состояние «в процессе», поэтому из другой вкладки или окна видно, занята ли ещё сессия. Индикатор остаётся видимым после окончания хода, пока ещё выполняются [фоновые субагенты](https://code.claude.com/docs/ru/sub-agents.md#run-subagents-in-foreground-or-background) или [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md), и исчезает, когда сессия простаивает.

Claude Code сообщает это состояние только в терминалах, поддерживающих индикатор: ConEmu, Ghostty 1.2.0 или новее и iTerm2 3.6.6 или новее. Установите этот ключ в `false`, чтобы Claude Code перестал его сообщать. Отображается в `/config` как **Terminal progress bar**.

* **Область действия**: [`Any file`](#scopes). Значение в `~/.claude.json` из более старой версии применяется, если ни один файл настроек не задаёт этот ключ.
* **Тип**: Boolean
  * `true`: вы видите индикатор прогресса в терминалах, которые его поддерживают
  * `false`: Claude Code скрывает индикатор прогресса в терминале
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "terminalProgressBarEnabled": false
}
```

### `terminalTitleFromRename`

Claude Code задаёт заголовок вкладки вашего терминала. По умолчанию он использует заголовок, сгенерированный на основе диалога, а как только вы дадите сессии [имя](https://code.claude.com/docs/ru/sessions.md#name-your-sessions) с помощью `/rename` или `--name`, вкладка вместо этого показывает это имя. Установите этот ключ в `false`, чтобы сохранять на вкладке сгенерированный заголовок даже после того, как вы назовёте сессию. Само имя при этом всё равно применяется, поэтому `/resume <name>` и средство выбора сессий находят её.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: заголовок вкладки терминала показывает заданное вами имя сессии
  * `false`: вкладка сохраняет заголовок, который Claude Code генерирует на основе вашего диалога
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "terminalTitleFromRename": false
}
```

Чтобы Claude Code вообще не обновлял заголовок терминала, установите вместо этого [`CLAUDE_CODE_DISABLE_TERMINAL_TITLE`](https://code.claude.com/docs/ru/env-vars) в `1`.

### `theme`

Выбор цветовой темы интерфейса. Отображается в `/config` как **Theme**.

* **Область действия**: [`Any file`](#scopes). Значение в `~/.claude.json` из более старой версии применяется, если ни один файл настроек не задаёт этот ключ.
* **Тип**: строка, одно из значений:
  * `"auto"`: соответствует светлому или тёмному фону вашего терминала
  * `"dark"`: тёмная тема
  * `"light"`: светлая тема
  * `"dark-daltonized"`: тёмная тема с цветами, подходящими для людей с нарушениями цветового зрения
  * `"light-daltonized"`: светлая тема с цветами, подходящими для людей с нарушениями цветового зрения
  * `"dark-ansi"`: тёмная тема, использующая только палитру цветов ANSI вашего терминала
  * `"light-ansi"`: светлая тема, использующая только палитру цветов ANSI вашего терминала
  * `"custom:<slug>"` или `"custom:<plugin-name>:<slug>"`: пользовательская тема из `~/.claude/themes/` или из плагина
* **По умолчанию**: `"dark"`

```json settings.json theme={null}
{
  "theme": "light-daltonized"
}
```

См. [Создание пользовательской темы](https://code.claude.com/docs/ru/terminal-config.md#create-a-custom-theme).

### `timeFormat`

Определяет, как Claude Code записывает время, которое он показывает в интерфейсе, например `done 6:05 PM` в конце каждого сообщения о длительности хода и метки времени в [средстве просмотра транскрипта](https://code.claude.com/docs/ru/interactive-mode.md#transcript-viewer). Чтобы выбрать готовый вариант, выполните `/config` и задайте **Time format**. Требуется Claude Code v2.1.257 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"auto"`: то же, что и отсутствие значения; каждое время сохраняет свой встроенный формат, который в сообщении о длительности хода следует вашей локали
  * `"12-hour"`: 12-часовой формат
  * `"24-hour"`: 24-часовой формат
  * `"24-hour-utc"`: 24-часовой формат в UTC с `Z` после минут, например `18:05Z`; для этого варианта Claude Code игнорирует [`timeZone`](#timezone)
  * Шаблон strftime, например `"%H:%M"`: Claude Code записывает каждое время по шаблону. Любое значение, содержащее `%`, является шаблоном, а любое другое значение вне готовых вариантов считается `"auto"`
* **По умолчанию**: `"auto"`

```json settings.json theme={null}
{
  "timeFormat": "24-hour"
}
```

`/config` предлагает только готовые варианты, поэтому чтобы использовать шаблон strftime, добавьте ключ в файл настроек. Этот пример показывает каждое время в двузначном 24-часовом формате:

```json settings.json theme={null}
{
  "timeFormat": "%H:%M"
}
```

После этого сообщение о длительности хода и средство просмотра транскрипта показывают время, например `18:05`. В средстве просмотра транскрипта шаблон задаёт всю метку времени целиком, поэтому добавьте директивы даты, если хотите видеть там дату. Этот пример ставит дату перед временем:

```json settings.json theme={null}
{
  "timeFormat": "%Y-%m-%d %H:%M"
}
```

После этого в тех же местах показывается время, например `2026-09-01 18:05`.

### `timeZone`

Показывать время в интерфейсе в часовом поясе, отличном от системного. Задайте [имя часового пояса IANA](https://www.iana.org/time-zones), например `"UTC"` или `"Europe/Dublin"`. Время, которым управляет [`timeFormat`](#timeformat), тогда показывается в этом поясе. Если `timeFormat` имеет значение `"24-hour-utc"`, время остаётся в UTC, и Claude Code игнорирует этот ключ. В `/config` нет строки для этого ключа, поэтому задайте его в файле настроек. Требуется Claude Code v2.1.257 или новее.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, имя часового пояса IANA. Если Claude Code не распознаёт имя, он использует системный часовой пояс
* **По умолчанию**: не задано, поэтому время показывается в системном часовом поясе

```json settings.json theme={null}
{
  "timeZone": "Europe/Dublin"
}
```

### `tui`

Выбор рендерера пользовательского интерфейса терминала. Используйте `"fullscreen"` для [рендерера альтернативного экрана](https://code.claude.com/docs/ru/fullscreen.md) без мерцания с виртуализированной прокруткой или `"default"` для классического рендерера основного экрана. Выполнение `/tui fullscreen` или `/tui default` записывает этот ключ за вас.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"default"`: классический рендерер основного экрана
  * `"fullscreen"`: рендерер альтернативного экрана без мерцания с виртуализированной прокруткой
* **По умолчанию**: не задано, поэтому Claude Code [выбирает рендерер за вас](https://code.claude.com/docs/ru/fullscreen.md#fullscreen-by-default)
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_NO_FLICKER`](https://code.claude.com/docs/ru/env-vars) и [`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`](https://code.claude.com/docs/ru/env-vars) имеют приоритет над этим ключом в рамках одной сессии: `CLAUDE_CODE_NO_FLICKER=1` включает полноэкранный режим, а `CLAUDE_CODE_NO_FLICKER=0` или `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` отключает его; если заданы обе переменные, Claude Code отключает его

```json settings.json theme={null}
{
  "tui": "fullscreen"
}
```

В tmux `-CC` или при подключении по SSH к Windows Claude Code сохраняет классический рендерер, если вы не установите `CLAUDE_CODE_NO_FLICKER=1`. Фоновые сессии, открытые из [представления агентов](https://code.claude.com/docs/ru/agent-view.md), всегда используют полноэкранный рендерер независимо от этой настройки.

### `verbose`

По умолчанию транскрипт сворачивает каждый вызов инструмента в краткую сводку, например команду, которую выполнил Claude, и количество строк её вывода, а чтобы увидеть подробности, вы нажимаете `Ctrl+O` и переключаете весь транскрипт в развёрнутый вид. Установите этот ключ в `true`, чтобы показывать полные входные и выходные данные каждого вызова инструмента прямо по ходу выполнения, что полезно при отладке хука, MCP-сервера или длинной shell-команды. Отображается в `/config` как **Verbose output**.

* **Область действия**: [`Any file`](#scopes). Значение в `~/.claude.json` из более старой версии применяется, если ни один файл настроек не задаёт этот ключ.
* **Тип**: Boolean
  * `true`: вы видите полный вывод инструментов
  * `false`: вы видите сокращённые сводки вывода инструментов
* **По умолчанию**: `false`
* **Переопределения для отдельной сессии**: [`--verbose`](https://code.claude.com/docs/ru/cli-reference#cli-flags) имеет приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "verbose": true
}
```

Значение [`viewMode`](#viewmode) или сохранённый выбор `/focus` переопределяет этот ключ в каждой сессии.

### `viewMode`

Задаёт вид транскрипта, в котором запускается Claude Code: `"default"`, `"verbose"` или `"focus"`. Если значение задано, оно переопределяет как сохранённый выбор `/focus`, так и настройку [`verbose`](#verbose).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, одно из значений:
  * `"default"`: обычный транскрипт с сокращённым выводом инструментов
  * `"verbose"`: транскрипт с полным выводом инструментов
  * `"focus"`: только ваш последний промпт, однострочная сводка вызовов инструментов со статистикой изменений и итоговый ответ. Для режима фокуса нужен [полноэкранный рендерер](#tui)
* **По умолчанию**: не задано, поэтому применяются настройка `verbose` и ваш последний выбор `/focus`
* **Переопределения для отдельной сессии**: [`--verbose`](https://code.claude.com/docs/ru/cli-reference#cli-flags) имеет приоритет над этим ключом в рамках одной сессии

```json settings.json theme={null}
{
  "viewMode": "focus"
}
```

### `vimInsertModeRemaps`

Сопоставляет двухклавишные последовательности режима INSERT с клавишей Escape в [режиме редактора vim](https://code.claude.com/docs/ru/interactive-mode.md#vim-editor-mode). Каждый ключ — это ровно два печатаемых символа, набираемых последовательно, и `"<Esc>"` — единственная поддерживаемая цель; Claude Code игнорирует другие записи.

* **Область действия**: [`User or managed`](#scopes). Репозиторий не может переназначать ваши нажатия клавиш.
* **Тип**: объект, сопоставляющий двухсимвольную последовательность с `"<Esc>"`
* **По умолчанию**: не задано

```json settings.json theme={null}
{
  "vimInsertModeRemaps": {
    "jj": "<Esc>"
  }
}
```

Не действует, если `editorMode` не равен `"vim"`. См. [Переназначение последовательностей клавиш в режиме INSERT](https://code.claude.com/docs/ru/interactive-mode.md#remap-insert-mode-key-sequences).

### `voice`

Включает [голосовой ввод](https://code.claude.com/docs/ru/voice-dictation.md) и определяет поведение клавиши диктовки. Claude Code записывает этот объект за вас, когда вы выполняете `/voice`.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект с полем `enabled` типа Boolean, `autoSubmit` типа Boolean, которое применяется только в режиме удержания, и `mode`, одно из значений:
  * `"hold"`: вы удерживаете клавишу диктовки во время речи и отпускаете её, чтобы остановить
  * `"tap"`: вы нажимаете клавишу один раз, чтобы начать запись, и ещё раз, чтобы отправить
* **По умолчанию**: не задано, поэтому диктовка отключена; если `enabled` равно `true`, а `mode` не задан, Claude Code использует `"hold"`

Этот пример включает диктовку и настраивает клавишу так, чтобы одно нажатие начинало запись, а повторное — отправляло:

```json settings.json theme={null}
{
  "voice": {
    "enabled": true,
    "mode": "tap"
  }
}
```

`autoSubmit` отправляет промпт, когда вы отпускаете клавишу в режиме удержания. Для голосового ввода требуется учётная запись claude.ai.

### `voiceEnabled`

> [!WARNING]
>
> Объявлен устаревшим начиная с v2.1.92, когда его заменил объект [`voice`](#voice). Claude Code по-прежнему считывает его, чтобы старые файлы настроек продолжали работать, но в новых конфигурациях следует задавать `voice.enabled`.

Включает голосовой ввод с помощью единственного значения Boolean — формы, существовавшей до объекта `voice`. Если заданы оба, применяется `voice.enabled`.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: голосовой ввод включён, если вы вошли с учётной записью claude.ai и политика вашей организации разрешает голосовой ввод, если только не задано `voice.enabled`
  * `false`: голосовой ввод отключён, если только не задано `voice.enabled`
* **По умолчанию**: не задано

```json settings.json theme={null}
{
  "voiceEnabled": true
}
```

### `wheelScrollAccelerationEnabled`

Ускорять прокрутку колёсиком мыши при быстрой прокрутке в [полноэкранном режиме отображения](https://code.claude.com/docs/ru/fullscreen.md#mouse-wheel-scrolling). Установите `false` для постоянной скорости прокрутки на каждый щелчок колёсика.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code ускоряет прокрутку колёсиком мыши при быстрой прокрутке
  * `false`: Claude Code прокручивает с постоянной скоростью на каждый щелчок колёсика
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "wheelScrollAccelerationEnabled": false
}
```

## Git и атрибуция

Управляйте атрибуцией, которую Claude Code добавляет к коммитам и pull request'ам, и тем, как она работает с git.

### `attribution`

Настройте атрибуцию, которую Claude Code добавляет к git коммитам и pull request'ам. По умолчанию коммиты получают [git trailer](https://git-scm.com/docs/git-interpret-trailers) такой как `Co-Authored-By`; описания pull request'ов получают простой текст. Установите каждую часть отдельно с помощью подключей ниже.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект со строками `commit` и `pr` и логическим значением `sessionUrl`, или `false` для скрытия всей атрибуции. Значение `false` требует Claude Code v2.1.281 или позже; более ранние версии его отклоняют и [пропускают весь файл пользователя, проекта или локальных параметров](https://code.claude.com/docs/ru/settings.md#fix-a-broken-settings-file), который его содержит
* **По умолчанию**: не установлено, поэтому Claude Code использует стандартную атрибуцию, показанную под каждым подключом

Чтобы скрыть всю атрибуцию, установите `attribution` в `false`. В файле параметров, который также читают более ранние версии, установите [`commit`](#attribution-commit) и [`pr`](#attribution-pr) в пустые строки и [`sessionUrl`](#attribution-sessionurl) в `false` вместо этого.

Этот пример заменяет атрибуцию коммита, удаляет атрибуцию pull request'а и убирает ссылку на сеанс:

```json settings.json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": "",
    "sessionUrl": false
  }
}
```

После того как вы установите `commit` или `pr`, Claude Code игнорирует устаревший параметр `includeCoAuthoredBy` и использует текст по умолчанию для того из двух, который вы оставили без установки.

Claude Code сообщает Claude, что ваши собственные инструкции об атрибуции, такие как CLAUDE.md или правило [memory](https://code.claude.com/docs/ru/memory.md), имеют приоритет над этими строками коммита и PR, если только строка не установлена в [управляемых параметрах](https://code.claude.com/docs/ru/managed-settings.md).

### `includeCoAuthoredBy`

> [!WARNING]
>
> Устарело с версии v2.0.62, когда [`attribution`](#attribution) его заменила. Claude Code по-прежнему его читает, но новые конфигурации должны устанавливать `attribution`.

Используйте [`attribution`](#attribution) вместо этого, который заменяет этот ключ и позволяет вам изменять или скрывать trailer коммита, текст pull request'а и ссылку на сеанс отдельно. Claude Code по-прежнему соблюдает `includeCoAuthoredBy: false` из файлов параметров, которые предшествуют `attribution`, но игнорирует его после того как вы установите `attribution.commit` или `attribution.pr`.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: логическое значение
  * `true`: то же самое, что и не установлено; Claude Code добавляет trailer коммита и текст атрибуции pull request'а
  * `false`: Claude Code опускает как trailer коммита, так и текст атрибуции pull request'а, если только `attribution` не устанавливает `commit` или `pr`, в этом случае применяются правила [`attribution`](#attribution)
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "includeCoAuthoredBy": false
}
```

Чтобы скрыть всю атрибуцию, см. [`attribution`](#attribution).

### `includeGitInstructions`

Claude Code предоставляет Claude две связанные с git части контекста: встроенные инструкции по написанию коммитов и pull request'ов в описании инструмента Bash и снимок состояния git вашего репозитория. Снимок содержит текущую ветку, основную ветку, вывод `git status` и недавние коммиты. Claude Code читает его при запуске разговора.

Установите этот ключ в `false`, чтобы исключить оба, например когда вы используете свои собственные skills рабочего процесса git.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: логическое значение
  * `true`: Claude Code включает встроенные инструкции рабочего процесса коммита и pull request'а и снимок состояния git. Облачные сеансы никогда не включают снимок
  * `false`: Claude Code исключает оба
* **По умолчанию**: `true`
* **Переопределения для каждого сеанса**: [`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом для одного сеанса

```json settings.json theme={null}
{
  "includeGitInstructions": false
}
```

Если вы заменяете системный промпт в [неинтерактивном режиме](https://code.claude.com/docs/ru/headless.md) или в Agent SDK, сессия запускается без снимка, даже если этот ключ имеет значение `true`:

* **Запуски с `-p`**: вы заменяете промпт, когда передаёте [`--system-prompt`](https://code.claude.com/docs/ru/cli-reference#system-prompt-flags) или `--system-prompt-file`. Вы также заменяете его, когда запускаете пользовательского агента с собственным промптом, выбранного с помощью [`--agent`](https://code.claude.com/docs/ru/sub-agents#invoke-subagents-explicitly) или настройки [`agent`](#agent). Вне [режима bare](https://code.claude.com/docs/ru/headless.md#start-faster-with-bare-mode), чтобы сохранить снимок, запускайте без пользовательского агента и добавляйте свои инструкции с помощью [`--append-system-prompt`](https://code.claude.com/docs/ru/cli-reference#system-prompt-flags) вместо замены промпта.
* **[Agent SDK](https://code.claude.com/docs/ru/agent-sdk/modifying-system-prompts.md)**: вы заменяете промпт пользовательским системным промптом или пользовательским агентом основного потока. Если вы не задаёте системный промпт, SDK использует свой минимальный промпт по умолчанию, и сессия также запускается без снимка. Вне [режима bare](https://code.claude.com/docs/ru/headless.md#start-faster-with-bare-mode), чтобы сохранить снимок, используйте пресет `claude_code` без пользовательского `agent`.

### `prUrlTemplate`

Направьте ссылки PR, которые Claude Code отображает, в значке нижнего колонтитула и в сводках результатов инструментов, на внутренний инструмент проверки кода вместо `github.com`. Claude Code подставляет `{host}`, `{owner}`, `{repo}`, `{number}` и `{url}` из URL PR. Ссылки на [GitLab merge request](https://code.claude.com/docs/ru/interactive-mode.md#gitlab-merge-requests) на обеих поверхностях сохраняют свой URL GitLab.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка, шаблон URL с использованием любого из пяти заполнителей
* **По умолчанию**: не установлено

```json settings.json theme={null}
{
  "prUrlTemplate": "https://reviews.example.com/{owner}/{repo}/pull/{number}"
}
```

Claude Code применяет шаблон только к ссылкам, которые он отображает сам; номер PR, который Claude пишет в сообщении, такой как `#123`, остается таким, как его написал Claude. URL, который не имеет формы `/pull/<number>`, остается без изменений.

### `attribution.commit`

Установите текст атрибуции, который Claude Code добавляет к git коммитам, включая любые trailers. Установите его в пустую строку, чтобы скрыть атрибуцию коммита.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка
* **По умолчанию**: не установлено, поэтому Claude Code добавляет `Co-Authored-By: <name> <noreply@anthropic.com>`. Имя — это модель в использовании при создании коммита, такая как `Claude Sonnet 5`. Когда [subagent](https://code.claude.com/docs/ru/sub-agents.md) создает коммит, trailer указывает модель subagent'а.
  * Когда Claude Code распознает модель как модель Claude, но не может подтвердить её точную версию, он пишет только `Claude`.
  * Когда он не может сопоставить ID модели с какой-либо моделью Claude, такой как модель третьей стороны, обслуживаемая через пользовательский [`ANTHROPIC_BASE_URL`](https://code.claude.com/docs/ru/env-vars), он пишет `Claude Code`.

Этот пример заменяет trailer по умолчанию пользовательской строкой и пользовательским trailer'ом `Co-Authored-By`:

```json settings.json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>"
  }
}
```

### `attribution.pr`

Установите текст атрибуции, который Claude Code добавляет к описаниям pull request'ов. Установите его в пустую строку, чтобы скрыть атрибуцию pull request'а.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: строка
* **По умолчанию**: не установлено, поэтому Claude Code добавляет `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

```json settings.json theme={null}
{
  "attribution": {
    "pr": ""
  }
}
```

### `attribution.sessionUrl`

Выберите, добавляет ли Claude Code ссылку на сеанс claude.ai при коммите или открытии pull request'а из [облачного](https://code.claude.com/docs/ru/claude-code-on-the-web.md) или [Remote Control](https://code.claude.com/docs/ru/remote-control.md) сеанса. Claude Code добавляет ссылку как trailer `Claude-Session` на коммитах и как ссылку в описаниях pull request'ов. Установите его в `false`, чтобы опустить ссылку.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: логическое значение
  * `true`: Claude Code добавляет ссылку на сеанс claude.ai при коммите или открытии pull request'а из облачного или Remote Control сеанса
  * `false`: Claude Code опускает ссылку
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "attribution": {
    "sessionUrl": false
  }
}
```

## Хуки и автоматизация

Регистрируйте хуки, ограничивайте, какие хуки запускаются, и управляйте рабочими процессами. События хуков и их данные описаны в [справочнике хуков](https://code.claude.com/docs/ru/hooks.md).

### `allowedHttpHookUrls`

Ограничьте, какие URL-адреса могут быть целью [HTTP-хуков](https://code.claude.com/docs/ru/hooks.md#http-hook-fields). Задайте этот ключ в управляемых настройках, чтобы он распространялся на хуки, которые развёртывает ваша организация, или в любом файле настроек, чтобы он распространялся на другие хуки. Claude Code запускает такой хук, только если его URL соответствует шаблону из списка, объединённого по всем файлам настроек.

* **Область действия**: [`Any file`](#scopes). Массивы объединяются между файлами настроек.
* **Тип**: массив шаблонов URL-адресов с `*` в качестве подстановочного символа
* **По умолчанию**: не установлено, поэтому разрешены любые URL-адреса

Этот пример разрешает любой URL-адрес под `https://hooks.example.com/` и любой URL-адрес `http://localhost`:

```json settings.json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

Сопоставление имён хостов не зависит от регистра и рассматривает `hooks.example.com.` с конечной точкой, которая обозначает полное доменное имя, так же, как `hooks.example.com`, что соответствует тому, как это делает DNS.

В параметре `managedSettings` Agent SDK Claude Code игнорирует список, содержащий записи, поэтому вместо этого передавайте его в [параметре `settings`](https://code.claude.com/docs/ru/agent-sdk/typescript#options) SDK. См. [что делает пустой список в родительских настройках](https://code.claude.com/docs/ru/claude-apps-gateway#how-hook-and-skill-keys-in-parent-settings-take-effect).

### `allowManagedHooksOnly`

Ограничьте выполнение хуков только хуками, которые развёртывает ваша организация.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: Boolean
  * `true`: запускаются только управляемые хуки, а также хуки Agent SDK и хуки из плагинов, которые ваши управляемые настройки принудительно включают. См. [Что запускается при `allowManagedHooksOnly`](#what-runs-under-allowmanagedhooksonly)
  * `false`: запускаются хуки из всех областей действия настроек и всех плагинов
* **По умолчанию**: не установлено, поэтому запускаются хуки из всех областей действия настроек и всех плагинов

```json managed-settings.json theme={null}
{
  "allowManagedHooksOnly": true
}
```

#### Что запускается при `allowManagedHooksOnly`

Когда вы устанавливаете это значение в `true`, Claude Code изменяет, какие хуки и похожие на хуки команды загружаются:

* **Запускаются управляемые хуки и хуки SDK**: хуки из управляемых настроек и хуки, которые [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) регистрирует в процессе
* **Запускаются хуки принудительно включённых плагинов**: хуки из плагинов, которые ваши управляемые настройки принудительно включают через [`enabledPlugins`](#enabledplugins). Claude Code сопоставляет полный ID `plugin@marketplace`, поэтому плагин с тем же именем из другого маркетплейса остаётся заблокированным. Это позволяет вам распространять проверенные хуки через маркетплейс организации, блокируя всё остальное. [Mod](https://code.claude.com/docs/ru/plugins/mods/overview.md) в таком плагине загружается, только если он [считается модом вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods)
* **Мониторы из других плагинов блокируются**: [мониторы](https://code.claude.com/docs/ru/plugins/components.md#monitors) плагина не запускаются, если плагин не включён принудительно. Требуется Claude Code v2.1.310 или новее
* **Всё остальное блокируется**: пользовательские, проектные и локальные хуки, хуки и mods из других установленных плагинов, а также хуки, объявленные во frontmatter агента. [Mods, встроенные в Claude Code](https://code.claude.com/docs/ru/plugins/mods/overview.md#mods-built-into-claude-code), продолжают работать. Чтобы блокировать только mods пользователей, установите вместо этого [`allowManagedModsOnly`](https://code.claude.com/docs/ru/plugins/mods/admin#set-options-on-the-built-in-guard).
* **Плагины с источником-командой отключаются**: Claude Code также отключает плагины с [источником `command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source), включая плагины, принудительно включённые в управляемых `enabledPlugins`, если вы явно не установите [`disableCommandPluginSources`](#disablecommandpluginsources) в `false`
* **Команды `headersHelper` маркетплейсов блокируются**: Claude Code также блокирует [команды `headersHelper`](https://code.claude.com/docs/ru/plugins/host-marketplace#authenticate-archive-downloads) маркетплейсов, если [`disableCommandPluginSources`](#disablecommandpluginsources) явно не установлен в `false`, за исключением маркетплейса, который объявлен в самих управляемых настройках. Требуется Claude Code v2.1.238 или новее
* **Строка состояния и предложение файлов ограничиваются управляемыми настройками**: Claude Code читает [`statusLine`](https://code.claude.com/docs/ru/statusline) и [`fileSuggestion`](#filesuggestion) только из управляемых настроек, следуя [правилам для строки состояния и предложения файлов](#status-line-and-file-suggestion-gates)

Команда [`/goal`](https://code.claude.com/docs/ru/goal) не может запуститься, пока этот ключ установлен, потому что она зависит от хуков.

### `disableAllHooks`

Отключите [хуки](https://code.claude.com/docs/ru/hooks.md#disable-or-remove-hooks), любую пользовательскую [строку состояния](https://code.claude.com/docs/ru/statusline.md) и любую пользовательскую команду [предложения файлов](#filesuggestion). Используйте это, чтобы временно отключить всё это, не удаляя из ваших настроек.

* **Область действия**: [`Any file`](#scopes). Только управляемые настройки могут отключать управляемые хуки.
* **Тип**: Boolean
  * `true`: Claude Code отключает хуки, любую пользовательскую строку состояния и любую пользовательскую команду предложения файлов
  * `false`: хуки, строка состояния и команда предложения файлов запускаются
* **По умолчанию**: не установлено, поэтому хуки запускаются

```json settings.json theme={null}
{
  "disableAllHooks": true
}
```

Охват зависит от того, в каком файле находится ключ:

* **В управляемых настройках**: Claude Code отключает каждый настроенный хук, включая управляемые, и продолжает запускать хуки, которые [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) регистрирует в процессе
* **В параметре `managedSettings` Agent SDK**: на компьютере, где администратор развёртывает управляемые настройки, Claude Code игнорирует этот ключ, если только администратор не [разрешит встраивающему хосту добавлять политику](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy). Там, где ключ действует, останавливаются пользовательские, проектные, локальные хуки и хуки плагинов, а также все хуки в параметре `settings` SDK. Управляемые хуки администратора, хуки [принудительно включённых](#enabledplugins) плагинов и ваши [функции обратного вызова хуков SDK](https://code.claude.com/docs/ru/agent-sdk/hooks.md) продолжают запускаться. Требуется Claude Code v2.1.309 или новее.
* **В любом другом файле настроек**: Claude Code отключает пользовательские, проектные, локальные хуки и хуки плагинов; управляемые хуки, хуки Agent SDK и хуки из плагинов, принудительно включённых в управляемых [`enabledPlugins`](#enabledplugins), продолжают запускаться

Ключ также останавливает [mods](https://code.claude.com/docs/ru/plugins/mods/overview.md) — плагины, код которых регистрирует хуки:

* **В управляемых настройках**: останавливаются mods во всех установленных плагинах, включая mods вашей организации
* **В любом другом файле настроек**: останавливаются установленные вами mods, а [mods вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods) продолжают работать

Mods, встроенные в Claude Code, продолжают работать в обоих случаях. У каждого из них есть [собственный переключатель](https://code.claude.com/docs/ru/plugins/mods/overview.md#mods-built-into-claude-code).

Чтобы хуки Agent SDK продолжали запускаться, когда этот ключ задан в управляемых настройках, требуется Claude Code v2.1.242 или новее.

Команда [`/goal`](https://code.claude.com/docs/ru/goal) не может запуститься, пока хуки отключены, а меню `/hooks` показывает уведомление вместо ваших хуков.

#### Правила для строки состояния и предложения файлов

Claude Code принимает два решения для `statusLine` и `fileSuggestion` в следующем порядке:

* **Полностью отключено**: когда управляемые настройки устанавливают `disableAllHooks` или когда папка не является доверенной согласно тому же [правилу доверия рабочему пространству, что и для хуков в файлах настроек](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder)
* **Ограничено управляемыми настройками**: когда установлен [`allowManagedHooksOnly`](#allowmanagedhooksonly), когда `disableAllHooks` имеет значение `true` вне управляемых настроек после применения [приоритета настроек](https://code.claude.com/docs/ru/hooks.md#disable-or-remove-hooks) или когда вы запускаете Claude Code с `--safe-mode`

При ограничении Claude Code использует управляемое значение, если оно развёрнуто. В противном случае он без предупреждения пропускает ваше значение: строка состояния отключается, а автодополнение `@` возвращается к встроенному предложению файлов.

### `disableWorkflows`

Отключите [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md#turn-workflows-off) и встроенные команды рабочих процессов для всех, на кого распространяются ваши настройки, например для организации через управляемые настройки. Чтобы включить или отключить рабочие процессы только для себя, используйте вместо этого [`enableWorkflows`](#enableworkflows), который переключатель **Dynamic workflows** в `/config` записывает в ваши пользовательские настройки.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code отключает динамические рабочие процессы и встроенные команды рабочих процессов для всех, на кого распространяются ваши настройки
  * `false`: то же, что и отсутствие значения; включены ли рабочие процессы, тогда определяется [`enableWorkflows`](#enableworkflows) и значением по умолчанию вашего плана
* **По умолчанию**: `false`
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_DISABLE_WORKFLOWS`](https://code.claude.com/docs/ru/env-vars) отключает рабочие процессы на одну сессию; какой бы из двух механизмов их ни отключил, другой не может включить их обратно

```json settings.json theme={null}
{
  "disableWorkflows": true
}
```

### `enableWorkflows`

Включите или отключите [динамические рабочие процессы](https://code.claude.com/docs/ru/workflows.md) для себя, когда значение по умолчанию вашего плана вам не подходит. Отображается в `/config` как **Dynamic workflows**; этот переключатель записывает ключ в ваши пользовательские настройки и снова удаляет его, когда вы возвращаетесь к значению по умолчанию вашего плана. Чтобы отключить рабочие процессы для всех через управляемые настройки, используйте вместо этого [`disableWorkflows`](#disableworkflows).

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code включает для вас динамические рабочие процессы
  * `false`: Claude Code отключает для вас динамические рабочие процессы
* **По умолчанию**: не установлено, поэтому рабочие процессы включены, если только вы не на плане Pro, где они отключены
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_DISABLE_WORKFLOWS`](https://code.claude.com/docs/ru/env-vars) отключает рабочие процессы на одну сессию, и значение `true` здесь не может включить их обратно, пока эта переменная установлена

```json settings.json theme={null}
{
  "enableWorkflows": true
}
```

[`disableWorkflows`](#disableworkflows) и политика рабочих процессов вашей организации также имеют приоритет: `enableWorkflows: true` не может включить рабочие процессы обратно, пока какой-либо источник их отключает. Claude Code скрывает строку в `/config`, пока источник, отличный от ваших пользовательских настроек, устанавливает `enableWorkflows` или устанавливает `disableWorkflows` в `true`.

### `hooks`

Запускайте собственные команды, промпты, агентов, HTTP-запросы или инструменты MCP в качестве [хуков](https://code.claude.com/docs/ru/hooks.md) в определённых точках жизненного цикла Claude Code, например перед вызовом инструмента или при запуске сессии; в [справочнике хуков](https://code.claude.com/docs/ru/hooks.md#hook-events) перечислены все события, их данные и коды выхода. Каждое событие сопоставляется со списком групп matcher, и каждая группа перечисляет обработчики, которые запускаются, когда matcher срабатывает.

* **Область действия**: [`Any file`](#scopes). Хуки из разных файлов объединяются, а не заменяют друг друга, и хуки из управляемых настроек нельзя удалить из других файлов.
* **Тип**: объект, ключами которого являются [события хуков](https://code.claude.com/docs/ru/hooks.md#hook-events); каждое значение — массив групп `{ "matcher", "hooks" }`, записи `hooks` которых имеют `type` со значением `"command"`, `"prompt"`, `"agent"`, `"http"` или `"mcp_tool"`
* **По умолчанию**: не установлено, поэтому хуки не запускаются

Этот пример запускает скрипт перед каждым вызовом инструмента Bash:

```json settings.json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/check-bash.sh" }
        ]
      }
    ]
  }
}
```

Описание всех событий, шаблонов matcher и полей обработчиков см. в [справочнике хуков](https://code.claude.com/docs/ru/hooks.md#configuration). Чтобы отключить хуки, см. [`disableAllHooks`](#disableallhooks); чтобы ограничить хуки только теми, которые развёртывает ваша организация, см. [`allowManagedHooksOnly`](#allowmanagedhooksonly).

### `httpHookAllowedEnvVars`

[HTTP-хук](https://code.claude.com/docs/ru/hooks.md#http-hook-fields) может подставить значение переменной окружения в заголовок запроса, например в заголовок `Authorization: Bearer $HOOK_TOKEN`, но только для переменных, которые хук перечисляет в собственном `allowedEnvVars`.

Задайте этот ключ в управляемых настройках, чтобы он распространялся на хуки, которые развёртывает ваша организация, или в любом файле настроек, чтобы он распространялся на другие хуки. Такой хук может использовать переменную, только если её называют и его собственный `allowedEnvVars`, и список этого ключа, объединённый по всем файлам настроек.

* **Область действия**: [`Any file`](#scopes). Массивы объединяются между файлами настроек.
* **Тип**: массив имён переменных окружения
* **По умолчанию**: не установлено, поэтому применяется собственный список `allowedEnvVars` каждого хука

Этот пример ограничивает подстановку в заголовки переменными `MY_TOKEN` и `HOOK_SECRET`:

```json settings.json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

В параметре `managedSettings` Agent SDK Claude Code игнорирует список, содержащий записи, поэтому вместо этого передавайте его в [параметре `settings`](https://code.claude.com/docs/ru/agent-sdk/typescript#options) SDK. См. [что делает пустой список в родительских настройках](https://code.claude.com/docs/ru/claude-apps-gateway#how-hook-and-skill-keys-in-parent-settings-take-effect).

### `workflowKeywordTriggerEnabled`

Выберите, запускает ли ввод ключевого слова `ultracode` в промпте [динамический рабочий процесс](https://code.claude.com/docs/ru/workflows.md#ask-for-a-workflow-in-your-prompt). Установите `false`, чтобы вводить это слово, не запуская рабочий процесс.

* **Область действия**: [`Any file`](#scopes). Отображается в `/config` как **Ultracode keyword trigger**.
* **Тип**: Boolean
  * `true`: ввод `ultracode` в промпте запускает динамический рабочий процесс
  * `false`: вы можете вводить это слово, не запуская рабочий процесс
* **По умолчанию**: `true`

```json settings.json theme={null}
{
  "workflowKeywordTriggerEnabled": false
}
```

Настройка усилия `ultracode`, `/workflows` и сохранённые команды рабочих процессов не затрагиваются.

### `workflowSizeGuideline`

Задайте [количество агентов, к которому стремится Claude](https://code.claude.com/docs/ru/workflows.md#set-a-size-guideline) в создаваемых им динамических рабочих процессах. Claude Code передаёт значение Claude как рекомендацию, а не как жёсткий предел: `"small"` запрашивает менее 5 агентов, `"medium"` — менее 10, а `"large"` — менее 50. Выберите `"small"`, если хотите ограничить расходы рабочего процесса.

* **Область действия**: [`Any file`](#scopes). Значение из файла настроек имеет приоритет над выбором **Dynamic workflow size** в `/config`, который Claude Code хранит в `~/.claude.json`, и Claude Code скрывает эту строку, пока ключ задан в файле настроек.
* **Тип**: строка, одно из значений:
  * `"unrestricted"`: рекомендации нет, поэтому Claude подбирает размер рабочего процесса под задачу
  * `"small"`: Claude стремится использовать менее 5 агентов
  * `"medium"`: Claude стремится использовать менее 10 агентов
  * `"large"`: Claude стремится использовать менее 50 агентов
* **По умолчанию**: `"medium"` или `"small"`, если вы вошли с планом Pro и используете Claude Code v2.1.271 или новее

```json settings.json theme={null}
{
  "workflowSizeGuideline": "small"
}
```

## Плагины и скиллы

Включайте плагины, регистрируйте маркетплейсы, ограничивайте источники плагинов, разрешённые в организации, и управляйте тем, какие скиллы загружаются. Об установке и создании плагинов см. [Плагины](https://code.claude.com/docs/ru/plugins/overview.md).

### `disableBundledSkills`

Отключает [скиллы](https://code.claude.com/docs/ru/skills.md) и рабочие процессы, входящие в состав Claude Code. Claude Code полностью удаляет встроенные скиллы и рабочие процессы, а встроенные команды, такие как `/init`, по-прежнему можно ввести, но они скрыты от модели.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code удаляет встроенные скиллы и рабочие процессы и скрывает от модели встроенные команды, такие как `/init`
  * `false`: встроенные скиллы загружаются
* **По умолчанию**: не задано, поэтому встроенные скиллы загружаются
* **Переопределения для отдельной сессии**: [`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`](https://code.claude.com/docs/ru/env-vars) со значением `1` отключает встроенные скиллы для одной сессии; какой бы из двух способов их ни отключил, другой не может включить их обратно

```json settings.json theme={null}
{
  "disableBundledSkills": true
}
```

Скиллы из плагинов, `.claude/skills/` и `.claude/commands/` не затрагиваются. `/doctor` по-прежнему можно ввести, как и встроенные команды; чтобы скрыть её, задайте вместо этого [`DISABLE_DOCTOR_COMMAND`](https://code.claude.com/docs/ru/env-vars).

### `disableSkillShellExecution`

Отключает встроенное выполнение команд оболочки для блоков `` !`...` `` и ` ```! ` в [скиллах](https://code.claude.com/docs/ru/skills.md) и пользовательских командах из источников пользователя, проекта, плагина или дополнительного каталога. Claude Code заменяет каждую команду на `[shell command execution disabled by policy]` вместо её выполнения.

* **Область действия**: [`Any file`](#scopes). Значение `true` в управляемых настройках нельзя переопределить значением `false` в другом месте.
* **Тип**: Boolean
  * `true`: Claude Code заменяет каждую встроенную shell-команду на `[shell command execution disabled by policy]` вместо её выполнения
  * `false`: встроенные shell-команды выполняются
* **По умолчанию**: не задано, поэтому встроенные shell-команды выполняются

```json settings.json theme={null}
{
  "disableSkillShellExecution": true
}
```

Встроенные скиллы и скиллы, развёрнутые через управляемые настройки, не затрагиваются.

### `skillOverrides`

Скрывает или сворачивает [скилл](https://code.claude.com/docs/ru/skills.md#override-skill-visibility-from-settings) без редактирования его `SKILL.md`. Claude Code применяет значение, указанное под именем каждого скилла, к списку скиллов, который видит Claude, и к вашему автодополнению `/`.

* **Область действия**: [`Any file`](#scopes). Меню `/skills` записывает в `.claude/settings.local.json`.
* **Тип**: объект, сопоставляющий имя скилла с одним из значений:
  * `"on"`: Claude видит скилл, и вы можете ввести `/name`
  * `"name-only"`: Claude видит скилл по имени без его описания
  * `"user-invocable-only"`: Claude не видит скилл, но вы по-прежнему можете ввести `/name`
  * `"off"`: Claude не видит скилл, и `/name` скрыт из автодополнения
* **По умолчанию**: не задано, поэтому каждый скилл имеет значение `"on"`

В этом примере `legacy-context` показывается Claude только по имени, а `deploy` скрывается от Claude и из автодополнения `/`:

```json settings.json theme={null}
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

Переопределения не применяются к скиллам плагинов, которыми вы управляете через `/plugin`.

В управляемых настройках и файлах, переданных с `--settings`, ключ для псевдонима встроенного скилла, например `checkup` для `/doctor`, также применяется к скиллу; см. [как ключи псевдонимов сочетаются с ключами для собственного имени скилла](https://code.claude.com/docs/ru/skills.md#override-skill-visibility-from-settings).

### `syncClaudeAiSkills`

Отключает загрузку [скиллов, включённых для вашей учётной записи claude.ai](https://code.claude.com/docs/ru/skills.md#how-synced-skills-behave). Claude Code загружает их в `~/.claude/skills/synced/` в [сессиях терминала, где вы входите с учётной записью claude.ai](https://code.claude.com/docs/ru/skills.md#where-synced-skills-load), интерактивных или неинтерактивных, а также в сессиях Cowork и облачных сессиях. Задайте `false`, чтобы остановить эту загрузку и прекратить загрузку уже синхронизированных скиллов. Claude Code учитывает только `false`: `true` равнозначно отсутствию значения и не включает синхронизацию там, где она иначе отключена.

* **Область действия**: [`User, local, or managed`](#scopes), а также файлы, переданные с `--settings`.
* **Тип**: Boolean
  * `false`: Claude Code прекращает загружать синхронизированные скиллы и прекращает загружать те, что уже находятся в `~/.claude/skills/synced/`. В пользовательских или управляемых настройках он также перемещает их в `~/.claude/skills/.trash/`
  * `true`: то же, что и отсутствие значения
* **По умолчанию**: не задано, поэтому сессии, в которых выполнен вход с учётной записью claude.ai, синхронизируют ваши скиллы

В этом примере компьютеру запрещается загружать скиллы учётной записи в любой сессии:

```json settings.json theme={null}
{
  "syncClaudeAiSkills": false
}
```

### `syncClaudeAiPlugins`

Отключает загрузку [плагинов, включённых для вашей учётной записи claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins). Claude Code загружает их в `~/.claude/plugins/synced/` в начале сессий терминала, где вы входите с учётной записью claude.ai, и в сессиях Cowork, и загружает каждый как `<name>@synced`. Задайте `false`, чтобы остановить эту загрузку и прекратить загрузку уже синхронизированных плагинов. Claude Code учитывает только `false`: `true` равнозначно отсутствию значения и не включает синхронизацию там, где она иначе отключена. Требуется Claude Code v2.1.273 или новее.

* **Область действия**: [`User, local, or managed`](#scopes), а также файлы, переданные с `--settings`.
* **Тип**: Boolean
  * `false`: Claude Code прекращает загружать синхронизированные плагины и прекращает загружать те, что уже находятся в `~/.claude/plugins/synced/`. В пользовательских или управляемых настройках он также перемещает их в `~/.claude/plugins/.trash/`
  * `true`: то же, что и отсутствие значения
* **По умолчанию**: не задано, поэтому сессии, в которых выполнен вход с учётной записью claude.ai, синхронизируют ваши плагины

Чтобы отключить один синхронизированный плагин, а не все, задайте `"<name>@synced": false` в [`enabledPlugins`](#enabledplugins).

В этом примере компьютеру запрещается загружать плагины учётной записи в любой сессии:

```json settings.json theme={null}
{
  "syncClaudeAiPlugins": false
}
```

### `allowedChannelPlugins`

Выбирает, какие плагины [каналов](https://code.claude.com/docs/ru/channels.md) могут отправлять сообщения в сессии вашей организации. Если ключ задан, Claude Code использует ваш список вместо стандартного списка разрешённых плагинов Anthropic; каждая запись указывает плагин и маркетплейс, из которого он получен.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: массив объектов, каждый со строками `marketplace` и `plugin`. Вместо объекта запись может быть строкой `"plugin@marketplace"`, например `"telegram@claude-plugins-official"`, которую Claude Code рассматривает как эквивалентный объект. Строковая форма требует Claude Code v2.1.267 или новее; более ранние версии отклоняют всё значение `allowedChannelPlugins`, если оно её содержит
* **По умолчанию**: не задано, поэтому Claude Code использует стандартный список разрешённых плагинов Anthropic

В этом примере каналы включаются и разрешается только плагин Telegram из официального маркетплейса Anthropic:

```json managed-settings.json theme={null}
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "telegram" }
  ]
}
```

Пустой массив блокирует все плагины каналов.

Этот ключ вступает в силу, когда каналы проходят проверку [`channelsEnabled`](#channelsenabled) для учётной записи: в планах Team и Enterprise, а также для учётных записей Console с управляемыми настройками это означает `channelsEnabled: true`. См. [Ограничение плагинов каналов, которые могут запускаться](https://code.claude.com/docs/ru/channels.md#restrict-which-channel-plugins-can-run).

### `blockedMarketplaces`

Блокирует источники маркетплейсов плагинов для вашей организации. Claude Code проверяет список блокировки при добавлении маркетплейса, а также при установке, обновлении, повторной загрузке и автообновлении плагинов, поэтому маркетплейс, добавленный кем-либо до того, как вы задали политику, тоже нельзя использовать для получения плагинов. Заблокированные источники проверяются до загрузки, поэтому они никогда не попадают в файловую систему.

Если вы задаёте этот ключ в [консоли администратора claude.ai](https://code.claude.com/docs/ru/server-managed-settings.md), claude.ai также применяет его, когда кто-либо в вашей организации добавляет маркетплейс из git-репозитория на claude.ai, как описано в разделе [Как работают ограничения](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: массив объектов источников маркетплейсов в тех же формах, что и для [`strictKnownMarketplaces`](#allowed-source-types)
* **По умолчанию**: не задано, поэтому ни один маркетплейс не заблокирован

В этом примере блокируется один репозиторий GitHub как источник маркетплейса:

```json managed-settings.json theme={null}
{
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted/plugins" }
  ]
}
```

Запись `github` может использовать [форму с подстановочным знаком владельца](#owner-wildcards) `"owner/*"`, чтобы заблокировать все репозитории этого владельца GitHub; для этого требуется Claude Code v2.1.223 или новее. Добавьте `{ "source": "skills-dir" }`, чтобы Claude Code перестал загружать [плагины `@skills-dir`](https://code.claude.com/docs/ru/plugins/loading#plugins-shared-through-a-repository) как из `~/.claude/skills/`, так и из `.claude/skills/` проекта, не ограничивая ни один маркетплейс. См. [Ограничения управляемых маркетплейсов](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install).

### `channelsEnabled`

Разрешает [каналы](https://code.claude.com/docs/ru/channels.md) для вашей организации. В планах claude.ai Team и Enterprise Claude Code блокирует каналы, пока вы не зададите значение `true`. Для учётных записей [Anthropic Console](https://code.claude.com/docs/ru/authentication.md#claude-console-authentication), которые проходят аутентификацию с помощью API-ключа, каналы разрешены по умолчанию. Если ваша организация развёртывает управляемые настройки, Claude Code блокирует каналы и для таких учётных записей, пока вы не зададите этому ключу значение `true`.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code разрешает каналы для вашей организации
  * `false`: то же, что и отсутствие значения; блокируются ли каналы, зависит от вашего плана, как указано в пункте «По умолчанию»
* **По умолчанию**: не задано; каналы блокируются в планах Team и Enterprise и для учётных записей Console с управляемыми настройками и разрешены в планах Pro, Max и Ultra и для учётных записей Console без управляемых настройок

```json managed-settings.json theme={null}
{
  "channelsEnabled": true
}
```

Чтобы ограничить, какие плагины могут регистрироваться как каналы после их включения, задайте [`allowedChannelPlugins`](#allowedchannelplugins). См. [Корпоративные средства управления](https://code.claude.com/docs/ru/channels.md#enterprise-controls).

### `disableCommandPluginSources`

Блокирует [источник плагинов `command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source), который устанавливает плагин, запуская объявленную маркетплейсом команду на компьютере пользователя. Если вы задаёте значение `true`, Claude Code никогда не запускает эту команду, не устанавливает и не обновляет плагины из источника command и прекращает загружать уже установленные. Задайте `false`, чтобы явно разрешить их. Всякий раз, когда ключ блокирует источники command, независимо от того, задали ли вы `true` или оставили значение незаданным при [`allowManagedHooksOnly`](#allowmanagedhooksonly), он также блокирует [команды `headersHelper`](https://code.claude.com/docs/ru/plugins/host-marketplace#authenticate-archive-downloads) маркетплейсов, за исключением маркетплейса, который объявлен в самих управляемых настройках. Требуется Claude Code v2.1.229 или новее, а блокировка `headersHelper` требует v2.1.238 или новее.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code никогда не запускает объявленную маркетплейсом команду, не устанавливает и не обновляет плагины из источника command и прекращает загружать уже установленные
  * `false`: Claude Code явно разрешает плагины из источника command
* **По умолчанию**: не задано, поэтому Claude Code следует [`allowManagedHooksOnly`](#allowmanagedhooksonly): у организации, которая ограничивает выполнение хуков управляемыми настройками, источники command тоже отключены. Приложение, передающее [`disableAllHooks: true`](#disableallhooks) в параметре `managedSettings` Agent SDK, само по себе не отключает источники command.

```json managed-settings.json theme={null}
{
  "disableCommandPluginSources": true
}
```

Требуется Claude Code v2.1.229 или новее.

### `pluginSuggestionMarketplaces`

Указывает маркетплейсы, плагины которых могут появляться как контекстные предложения установки — в подсказках индикатора загрузки и закреплёнными вверху вкладки **Discover** в `/plugin`. Встроенная собственная подсказка frontend-design не затрагивается. Предложения формируются на основе объявления `relevance` каждого плагина в его записи маркетплейса.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: массив имён маркетплейсов
* **По умолчанию**: не задано, поэтому предложения, объявленные маркетплейсами, не показываются

```json managed-settings.json theme={null}
{
  "pluginSuggestionMarketplaces": ["acme-corp-plugins"]
}
```

Имя вступает в силу, только если маркетплейс зарегистрирован на компьютере и его зарегистрированный источник также объявлен в тех же управляемых настройках — либо как запись [`extraKnownMarketplaces`](#extraknownmarketplaces) для этого имени, либо как запись [`strictKnownMarketplaces`](#strictknownmarketplaces). Claude Code игнорирует маркетплейс, зарегистрированный из другого источника под именем из списка разрешённых. Официальный маркетплейс освобождён от требования к источнику: достаточно добавить в список разрешённых только его имя, поскольку это имя может быть зарегистрировано только из официального источника Anthropic. См. [Предложение плагинов по контексту](https://code.claude.com/docs/ru/plugins/relevance.md).

### `pluginTrustMessage`

Добавляет собственный текст вашей организации к предупреждению о доверии плагинам, которое Claude Code показывает перед установкой, например чтобы подтвердить, что плагины из вашего внутреннего маркетплейса проверены.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: строка
* **По умолчанию**: не задано, поэтому Claude Code показывает только стандартное предупреждение

```json managed-settings.json theme={null}
{
  "pluginTrustMessage": "All plugins from our marketplace are approved by IT"
}
```

### `strictKnownMarketplaces`

Ограничивает, какие источники маркетплейсов плагинов пользователи вашей организации могут добавлять и из каких могут устанавливать плагины. Claude Code применяет список разрешённых при добавлении маркетплейса, а также при установке, обновлении, повторной загрузке и автообновлении плагинов, до любых сетевых операций или операций с файловой системой, поэтому маркетплейс, добавленный кем-либо до того, как вы задали политику, нельзя использовать для получения плагинов, как только его источник перестаёт соответствовать списку. Заблокированные пользователи видят ошибку с указанием управляемой политики.

Если вы задаёте этот ключ в [консоли администратора claude.ai](https://code.claude.com/docs/ru/server-managed-settings.md), claude.ai также применяет его, когда кто-либо в вашей организации добавляет маркетплейс из git-репозитория на claude.ai, как описано в разделе [Как работают ограничения](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: массив объектов источников маркетплейсов; см. [Разрешённые типы источников](#allowed-source-types)
* **По умолчанию**: не задано, поэтому пользователи могут добавлять любой маркетплейс. Пустой массив означает полную блокировку всех источников маркетплейсов, включая официальный маркетплейс Anthropic

В этом примере разрешаются два репозитория GitHub, один из которых закреплён за ref `v2.0`, и один размещённый URL `marketplace.json`:

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" },
    { "source": "url", "url": "https://plugins.example.com/marketplace.json" }
  ]
}
```

Этот ключ также можно записать как `allowedMarketplaces`; в разделе [Псевдонимы ключей маркетплейсов](#marketplace-key-aliases) описано, как Claude Code обрабатывает псевдоним и какая версия его принимает. Этот ключ является политикой-ограничителем: он определяет, что пользователи могут добавлять, но ничего не регистрирует. Чтобы ограничить и предварительно зарегистрировать маркетплейсы в одном файле, см. [Сочетание с `extraKnownMarketplaces`](#combine-with-extraknownmarketplaces). Описание с точки зрения пользователя см. в разделе [Ограничения управляемых маркетплейсов](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install).

#### Разрешённые типы источников

Ниже для каждого типа источника показана одна запись списка разрешённых и принимаемые ею поля. Большинство типов сопоставляются точно; `hostPattern` и `pathPattern` сопоставляются по регулярному выражению, а записи `github` могут использовать [подстановочный знак владельца](#owner-wildcards).

| Источник | Пример записи | Поля |
| :- | :- | :- |
| `github` | `{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }` | `repo` обязательно; `ref` — ветка, тег или SHA коммита; `path` — подкаталог |
| `git` | `{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git", "ref": "production" }` | `url` обязательно; `ref` и `path` — как для `github` |
| `url` | `{ "source": "url", "url": "https://plugins.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }` | `url` обязательно; `headers` добавляет HTTP-заголовки для доступа с аутентификацией |
| `file` | `{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }` | `path` обязательно — абсолютный путь к файлу `marketplace.json` |
| `directory` | `{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }` | `path` обязательно — абсолютный путь к каталогу, содержащему `.claude-plugin/marketplace.json` |
| `hostPattern` | `{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }` | `hostPattern` обязательно — регулярное выражение, сопоставляемое с любой частью хоста маркетплейса; привяжите его с помощью `^` и `$`, чтобы сопоставлять весь хост |
| `pathPattern` | `{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }` | `pathPattern` обязательно — регулярное выражение, сопоставляемое с любой частью `path` источников `file` и `directory`; начните его с `^`, чтобы закрепить префикс |
| `skills-dir` | `{ "source": "skills-dir" }` | Нет полей |

Для некоторых типов источников действуют правила, выходящие за рамки таблицы:

* **`url`**: маркетплейс по URL загружает только файл `marketplace.json`, и Claude Code не получает файлы плагинов с этого сервера по относительному пути, поэтому его плагины должны использовать [источник плагина](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-sources), отличный от относительного пути, например URL архива, который может находиться на том же хосте. Для плагинов с относительными путями используйте вместо этого маркетплейс на основе Git. См. [Плагины с относительными путями не работают в маркетплейсах на основе URL](https://code.claude.com/docs/ru/plugins/troubleshooting.md#plugins-with-relative-paths-fail-in-url-based-marketplaces).
* **`hostPattern`**: используйте его, чтобы разрешить все маркетплейсы на внутреннем сервере GitHub Enterprise или GitLab, не перечисляя каждый репозиторий. Claude Code сопоставляет источники `github` с `github.com`, берёт имя хоста из источников `url`, а из источников `git` — в зависимости от формы [git URL](https://git-scm.com/docs/git-clone#_git_urls):

  * URL со схемой, например `https://` или `ssh://`: имя хоста в URL.
  * SSH-адрес без схемы в форме git `user@host:path`, например `git@git.example.com:tools/plugins.git`: хост между `@` и `:`, то есть хост, к которому подключается git.
  * Любая другая форма без схемы: хоста нет, поэтому ни одна запись `hostPattern` в `strictKnownMarketplaces` с ней не совпадает. Для `hostPattern` в `blockedMarketplaces` Claude Code извлекает хост из более широкого набора форм, поэтому запись списка блокировки всё же может совпасть с такой формой. До v2.1.234 `hostPattern` в `strictKnownMarketplaces` также совпадал с некоторыми формами, которые git не считает SSH-адресами.

  У источников `file` и `directory` нет хоста, и они никогда не совпадают с записью `hostPattern`.
* **`pathPattern`**: используйте его, чтобы разрешить маркетплейсы в файловой системе наряду с записями `hostPattern` для сетевых источников. `".*"` разрешает любой локальный путь; более узкий шаблон, например `"^/opt/approved/"`, ограничивает разрешение одним каталогом.
* **`skills-dir`**: любой список разрешённых, даже пустой, заставляет Claude Code прекратить загрузку [плагинов `@skills-dir`](https://code.claude.com/docs/ru/plugins/loading#plugins-shared-through-a-repository) как из `~/.claude/skills/`, так и из `.claude/skills/` проекта. Чтобы продолжить их загрузку, добавьте запись `{ "source": "skills-dir" }` и оставьте [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) незаданным. Эта запись не имеет смысла за пределами этого ключа и `blockedMarketplaces`.

#### Подстановочные знаки владельца

Запись `github`, у которой значение `repo` равно `"<owner>/*"`, совпадает со всеми репозиториями этого владельца GitHub. Подстановочные знаки владельца требуют Claude Code v2.1.223 или новее и работают только в `strictKnownMarketplaces` и `blockedMarketplaces`. Везде, где ещё встречается источник `github`, например в `extraKnownMarketplaces` или `/plugin marketplace add`, значение `repo` должно указывать один репозиторий. До v2.1.223 Claude Code сравнивал запись буквально, поэтому запись списка разрешённых не совпадала ни с одним репозиторием, а запись списка блокировки ничего не блокировала; записи с одним репозиторием применяются во всех версиях.

Эта запись разрешает любой репозиторий маркетплейса в организации `acme-corp`:

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/*" }
  ]
}
```

Подстановочным знаком может быть только вся позиция имени репозитория целиком. Claude Code игнорирует такие записи, как `*`, `*/plugins` или `acme-corp/tools-*`, как недопустимые, поэтому они не совпадают ни с одним репозиторием.

Правила сопоставления в двух настройках различаются:

| Правило | `strictKnownMarketplaces` | `blockedMarketplaces` |
| - | - | - |
| Совпадающие варианты записи источника | Только форма `owner/repo`. Git URL, клонирующий тот же репозиторий, не совпадает | Любой вариант записи, включая git URL, которые указывают на тот же репозиторий github.com |
| Регистр владельца | С учётом регистра | Без учёта регистра |
| `ref` | Следует правилам точных записей: запись с `ref` совпадает только с источниками с точно таким же ref, а запись без него совпадает только с источниками, в которых ref не указан | Запись без `ref` блокирует все ref совпадающих с ней репозиториев |
| `path` | Менее строго, чем правила точных записей: запись с `path` требует точно такого же значения, а запись без него совпадает с любым путём внутри репозитория | Запись без `path` блокирует все пути совпадающих с ней репозиториев |

#### Точное сопоставление

Для всех типов источников, кроме записей `github` с подстановочным знаком владельца и сопоставляемых по регулярному выражению записей `hostPattern` и `pathPattern`, Claude Code разрешает добавление пользователем, только если источник маркетплейса точно совпадает с записью. Для источников на основе git — `github` и `git` — точное сопоставление включает необязательные поля:

* `repo` или `url` должны совпадать точно
* Поле `ref` должно совпадать точно, либо оба значения должны быть не определены
* Поле `path` должно совпадать точно, либо оба значения должны быть не определены

Например, Claude Code рассматривает каждую пару ниже как два разных источника:

* `{ "source": "github", "repo": "acme-corp/plugins" }` и `{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }`
* `{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }` и `{ "source": "github", "repo": "acme-corp/plugins" }`

#### Разрешение только официального маркетплейса

Чтобы разрешить официальный маркетплейс Anthropic и ничего больше, укажите его репозиторий:

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" }
  ]
}
```

С этой записью Claude Code сохраняет доступность уже зарегистрированного официального маркетплейса, а на новом компьютере автоматически регистрирует маркетплейс при первом запуске интерактивной сессии терминала. Автоматическая регистрация чаще всего не срабатывает в следующих случаях:

* Неинтерактивные среды, которые запускаются до первой интерактивной сессии терминала на компьютере.
* Компьютеры, на которых Claude Code запускался только через расширение VS Code.
* Компьютеры, на которых Claude Code уже запускал интерактивную сессию терминала при политике, блокировавшей маркетплейс, например при полной блокировке пустым массивом. Claude Code записывает заблокированную попытку и не повторяет попытку после изменения политики.

На таких компьютерах добавьте маркетплейс в [`extraKnownMarketplaces`](#extraknownmarketplaces) в том же `managed-settings.json`, чтобы Claude Code зарегистрировал его автоматически, или выполните `claude plugin marketplace add anthropics/claude-plugins-official`.

#### Сочетание с `extraKnownMarketplaces`

Эти два ключа выполняют разные задачи. В этой таблице они сравниваются:

| Аспект | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| - | - | - |
| Назначение | Применение политики организации | Удобство для команды |
| Файл настроек | Только управляемые настройки | Любой файл настроек |
| Поведение | Блокирует добавления, не входящие в список разрешённых | Регистрирует отсутствующие маркетплейсы |
| Когда применяется | До сетевых операций и операций с файловой системой | Сразу — из пользовательских или управляемых настроек; после диалога доверия рабочему пространству — для файлов репозитория |
| Можно ли переопределить | Нет, наивысший приоритет | Да, настройками с более высоким приоритетом |
| Формат источника | Непосредственно объект источника | Именованный маркетплейс с вложенным объектом `source` |

Чтобы и ограничить, и предварительно зарегистрировать маркетплейс для всех пользователей, задайте оба ключа в `managed-settings.json`:

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Если задан только `strictKnownMarketplaces`, пользователи по-прежнему могут сами добавить разрешённый маркетплейс с помощью `/plugin marketplace add`. Официальный маркетплейс Anthropic — единственный, который Claude Code регистрирует автоматически, и только если список разрешённых это допускает. В разделе [Разрешение только официального маркетплейса](#allow-only-the-official-marketplace) перечислены компьютеры, на которых регистрация не срабатывает.

### `strictPluginOnlyCustomization`

Блокирует скиллы, агентов, хуки и MCP-серверы из пользовательских и проектных источников. Сочетайте его с [`strictKnownMarketplaces`](#strictknownmarketplaces), чтобы выбрать, из каких маркетплейсов пользователи могут устанавливать плагины. Добавьте [`disableSideloadFlags`](#disablesideloadflags), чтобы отклонять флаги CLI, которые подгружают плагины, агентов и MCP-серверы для одного запуска.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: `true`, чтобы заблокировать их все, или массив с названиями блокируемых из `"skills"`, `"agents"`, `"hooks"` и `"mcp"`
* **По умолчанию**: не задано, поэтому ничего не заблокировано

В этом примере блокируются скиллы и хуки, а агенты и MCP-серверы остаются незаблокированными:

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
```

Если вы блокируете любой интерфейс, Claude Code также прекращает загружать [плагины из каталога скиллов](https://code.claude.com/docs/ru/plugins/loading.md#skills-directory-plugins-blocked-by-managed-settings) — папки плагинов, которые пользователи хранят в `~/.claude/skills/` или `.claude/skills/`. Пользователи размещают эти папки сами, а не устанавливают из маркетплейса, поэтому при этой настройке Claude Code рассматривает их как пользовательскую настройку.

В четырёх записях подключей ниже перечислено, что ещё блокирует каждый интерфейс и что по-прежнему загружается. Claude Code игнорирует нераспознанные названия интерфейсов, а не считает файл настроек ошибочным, поэтому вы можете добавлять новые названия интерфейсов до того, как обновятся все клиенты.

### `strictPluginOnlyCustomization.skills`

Блокирует интерфейс `skills`. Claude Code прекращает загружать скиллы из `~/.claude/skills/` и `.claude/skills/`, пользовательские команды из `~/.claude/commands/` и `.claude/commands/`, скиллы и команды из каталогов `--add-dir`, а также скиллы, синхронизированные из вашей учётной записи claude.ai. Он продолжает загружать встроенные скиллы, скиллы в каталоге управляемой политики и скиллы из плагинов, кроме [плагинов из каталога скиллов](https://code.claude.com/docs/ru/plugins/loading.md#skills-directory-plugins-blocked-by-managed-settings).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: строка `"skills"` в массиве [`strictPluginOnlyCustomization`](#strictpluginonlycustomization)
* **По умолчанию**: не заблокировано

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["skills"]
}
```

### `strictPluginOnlyCustomization.agents`

Блокирует интерфейс `agents`. Claude Code прекращает загружать агентов из `~/.claude/agents/`, `.claude/agents/` и каталогов `--add-dir`. Он продолжает загружать встроенных агентов, агентов в каталоге управляемой политики и агентов из плагинов, кроме [плагинов из каталога скиллов](https://code.claude.com/docs/ru/plugins/loading.md#skills-directory-plugins-blocked-by-managed-settings).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: строка `"agents"` в массиве [`strictPluginOnlyCustomization`](#strictpluginonlycustomization)
* **По умолчанию**: не заблокировано

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["agents"]
}
```

### `strictPluginOnlyCustomization.hooks`

Блокирует интерфейс `hooks`:

* **Перестают выполняться**:
  * Хуки из пользовательского, проектного и локального `settings.json`
  * Хуки во frontmatter скиллов, пользовательских команд и агентов из тех источников, которые заблокировала бы блокировка [`skills`](#strictpluginonlycustomization-skills) или [`agents`](#strictpluginonlycustomization-agents)
* **Продолжают выполняться**: хуки в управляемых настройках и хуки из плагинов, кроме [плагинов из каталога скиллов](https://code.claude.com/docs/ru/plugins/loading.md#skills-directory-plugins-blocked-by-managed-settings)

Скиллы, пользовательские команды и агенты, хуки во frontmatter которых перестают выполняться, по-прежнему загружаются, пока их собственный интерфейс не заблокирован.

Личный или проектный [скилл](https://code.claude.com/docs/ru/skills.md#where-skills-live), объявляющий `hooks` в своём frontmatter, также теряет предварительное одобрение [`allowed-tools`](https://code.claude.com/docs/ru/skills#pre-approve-tools-for-a-skill), поэтому ваши пользователи получают запросы разрешения для инструментов, перечисленных в этом поле. Когда такой скилл выполняется в субагенте через [`context: fork`](https://code.claude.com/docs/ru/skills#run-skills-in-a-subagent), он сохраняет предварительное одобрение. Скилл, не объявляющий `hooks`, тоже сохраняет предварительное одобрение.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: строка `"hooks"` в массиве [`strictPluginOnlyCustomization`](#strictpluginonlycustomization)
* **По умолчанию**: не заблокировано

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["hooks"]
}
```

### `strictPluginOnlyCustomization.mcp`

Блокирует интерфейс `mcp`. Claude Code прекращает загружать MCP-серверы из `~/.claude.json` и `.mcp.json`. Он продолжает загружать серверы из [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp), серверы из [`managedMcpServers`](#managedmcpservers) и MCP-серверы из плагинов, кроме [плагинов из каталога скиллов](https://code.claude.com/docs/ru/plugins/loading.md#skills-directory-plugins-blocked-by-managed-settings).

* **Область действия**: [`Managed`](#scopes)
* **Тип**: строка `"mcp"` в массиве [`strictPluginOnlyCustomization`](#strictpluginonlycustomization)
* **По умолчанию**: не заблокировано

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["mcp"]
}
```

### `enabledPlugins`

Включает или отключает отдельные [плагины](https://code.claude.com/docs/ru/plugins/overview.md) по ключу `plugin-name@marketplace-name`. Плагин, для которого нет записи ни на одном уровне, использует своё значение [`defaultEnabled`](https://code.claude.com/docs/ru/plugins/manifest-reference#fields). Когда вы включаете или отключаете плагин с помощью `/plugin` или `claude plugin enable`, Claude Code записывает этот ключ за вас.

* **Область действия**: [`Any file`](#scopes)
* **Тип**: объект, сопоставляющий `plugin-name@marketplace-name` со значением Boolean
* **По умолчанию**: не задано, поэтому каждый плагин следует своему значению `defaultEnabled`

В этом примере включаются два плагина из маркетплейса `team-tools` и отключается один из `personal`:

```json settings.json theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

Каждый уровень служит своей цели:

* **Пользовательские настройки**: ваши личные предпочтения по плагинам
* **Настройки проекта**: плагины, включённые для всех в репозитории. Это не устанавливает их, поэтому каждый пользователь [устанавливает их сам](https://code.claude.com/docs/ru/plugins/org.md#require-plugins-per-repository).
* **Локальные настройки**: переопределения для отдельного компьютера, которые исключаются из Git через gitignore, когда Claude Code сохраняет туда настройку
* **Управляемые настройки**: политика на уровне всей организации. Плагин со значением `false` здесь блокируется от установки на любом уровне и скрывается из маркетплейса

Настройки проекта имеют приоритет над пользовательскими настройками, поэтому значение `false` для плагина в `~/.claude/settings.json` не отключает плагин, который включён в `.claude/settings.json` проекта. Чтобы отказаться от плагина, включённого проектом, на своём компьютере, задайте ему значение `false` в `.claude/settings.local.json`. Плагины, принудительно включённые управляемыми настройками, нельзя отключить таким способом, поскольку управляемые настройки переопределяют локальные.

### `extraKnownMarketplaces`

Регистрирует дополнительные маркетплейсы плагинов по имени, чтобы пользователи, открывающие репозиторий, или все, на кого распространяются ваши управляемые настройки, получали маркетплейс без самостоятельного добавления. Claude Code регистрирует каждый маркетплейс, который ему ещё не известен. Установится ли плагин из него, указанный в [`enabledPlugins`](#enabledplugins), зависит от источника плагина и от того, какой файл его включает; правила приведены в разделе [Включён в настройках проекта, но не установлен](https://code.claude.com/docs/ru/plugins/loading.md#enabled-in-project-settings-but-not-installed).

* **Область действия**: [`Any file`](#scopes). Claude Code учитывает записи в `.claude/settings.json` или `.claude/settings.local.json` репозитория только после того, как вы примете диалог доверия рабочему пространству для этой папки; в папке, которой вы не доверяете, включая запуск `-p` в ней, он игнорирует их без сообщения.
* **Тип**: объект, сопоставляющий имя маркетплейса с объектом, содержащим объект `source` и необязательное значение Boolean `autoUpdate`
* **По умолчанию**: не задано

В этом примере регистрируются маркетплейс GitHub и маркетплейс из git URL на собственном сервере:

```json settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

В разделе [Что выполняется до того, как вы доверитесь папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) проверка доверия сравнивается с другим содержимым, которое может предоставить репозиторий. Этот ключ также можно записать как `additionalMarketplaces`; см. [Псевдонимы ключей маркетплейсов](#marketplace-key-aliases).

Задайте `"autoUpdate": true` рядом с `source`, чтобы Claude Code обновлял этот маркетплейс и его установленные плагины в фоновом режиме после запуска. Если значение не указано, для `claude-plugins-official` и большинства других официальных маркетплейсов Anthropic по умолчанию используется `true`, а для сторонних маркетплейсов — `false`. См. [Настройка автообновлений](https://code.claude.com/docs/ru/plugins/install.md#keep-plugins-updated).

Если несколько файлов настроек определяют запись маркетплейса под одним и тем же именем, Claude Code целиком использует запись из [файла с наивысшим приоритетом](https://code.claude.com/docs/ru/settings.md#settings-precedence). Эта запись заменяет запись с более низким приоритетом и не наследует ни одного из её полей, поэтому переопределение не может объединить учётные данные `source.headers` из одного файла с URL, контролируемым другим файлом. До v2.1.228 Claude Code объединял одноимённые записи поле за полем, поэтому запись в файле с более высоким приоритетом могла наследовать поля, которые она не задавала, включая `headers` другого файла.

#### Типы источников маркетплейсов

Объект `source` принимает одну из следующих форм:

* **`github`**: репозиторий GitHub, с `repo`
* **`git`**: любой git URL, с `url`
* **`url`**: прямой URL к файлу `marketplace.json`, с `url` и необязательными `headers` и `headersHelper` для доступа с аутентификацией. `headersHelper` указывает команду, которая выводит заголовки, значения которых слишком недолговечны, чтобы перечислить их в `headers`, и требует Claude Code v2.1.238 или новее
* **`file`**: локальный путь к файлу `marketplace.json`, с `path`
* **`directory`**: локальный путь в файловой системе, с `path`. Используйте его для разработки или для маркетплейса, который ваша организация [развёртывает на каждом компьютере](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods).
* **`settings`**: встроенный маркетплейс, объявленный непосредственно в файле настроек без размещённого репозитория, с `name` и `plugins`

Тип источника `git` работает с любым сервисом хостинга git, включая GitLab и Bitbucket на собственных серверах. Claude Code клонирует репозиторий с той же аутентификацией, которую использовал бы `git clone` на этом компьютере: с настроенными помощниками учётных данных или SSH-ключами. Токен провайдера, например `GITHUB_TOKEN`, вступает в силу через помощник учётных данных, который его считывает. Подробности настройки см. в разделе [Частные репозитории](https://code.claude.com/docs/ru/plugins/host-marketplace.md#grant-access-to-a-private-marketplace).

Для источников `github` и `git` Claude Code никогда не загружает содержимое [Git LFS](https://git-lfs.com) при клонировании репозитория маркетплейса для его добавления или обновления. Файлы, отслеживаемые LFS, извлекаются как файлы-указатели, а вывод добавления или обновления сообщает, сколько их.

Поле `skipLfs` внутри объекта `source` принимается, но не действует. До v2.1.274 Claude Code загружал содержимое LFS, если только вы не задавали `"skipLfs": true`.

Для источника `url` задайте `headersHelper` внутри объекта `source`, когда учётные данные в `headers` истекают и новые должна выдавать команда. Требуется Claude Code v2.1.238 или новее. О том, что должна выводить команда и где Claude Code её запускает, см. [Написание команды headersHelper](https://code.claude.com/docs/ru/plugins/host-marketplace.md#write-the-headershelper-command), а о случаях, когда Claude Code её не запускает, — [Когда Claude Code пропускает команду headersHelper](https://code.claude.com/docs/ru/plugins/host-marketplace.md#when-claude-code-skips-a-headershelper-command-or-drops-its-output). Когда вы задаёте `headersHelper` для URL маркетплейса `https://`, Claude Code запускает команду в двух случаях, повторно используя вывод одного запуска в течение до 60 секунд:

* Перед каждым получением `marketplace.json` этого маркетплейса, включая последующее обновление. Claude Code отправляет выведенные заголовки вместе с этим получением.
* Перед каждой загрузкой архива плагина с источника (origin) URL маркетплейса, то есть с той же схемой, хостом и портом. Claude Code отправляет вывод вместе с этой загрузкой, и никакая другая загрузка заголовков не получает.

Claude Code игнорирует любой `headersHelper`, заданный в `.claude/settings.json` или `.claude/settings.local.json` каталога, добавленного вами с помощью [`--add-dir`](https://code.claude.com/docs/ru/permissions#what-runs-before-you-trust-a-folder), — как для источника `url`, так и для встроенной записи плагина — и отправляет только фиксированные `headers`, заданные в этом файле. Другие файлы настроек описаны в разделе [Как пользователи принимают команду headersHelper](https://code.claude.com/docs/ru/plugins/host-marketplace.md#how-users-accept-a-headershelper-command).

Плагины, перечисленные в источнике `settings`, должны ссылаться на внешние источники, такие как GitHub или npm, а `name` должно совпадать с ключом маркетплейса. Каждый плагин по-прежнему нужно отдельно включить в `enabledPlugins`. В этом примере один плагин объявляется встроенно:

```json settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

Запись плагина в `source: 'settings'`, собственный `source` которой — [`archive`](https://code.claude.com/docs/ru/plugins/marketplace-reference#archive-plugin-source), может задавать `headers` для загрузки архива. Если значение, которое вы поместили бы в `headers`, недолговечно, например токен, который ваш реестр выпускает по запросу, задайте вместо этого команду `headersHelper`. Запись может задавать оба поля. Оба поля требуют Claude Code v2.1.238 или новее.

Claude Code отправляет `headers` записи и всё, что выводит команда, вместе с загрузкой архива этого плагина и ни с какой другой загрузкой. Claude Code запускает команду, только когда пользователь [устанавливает или обновляет этот плагин отдельно](https://code.claude.com/docs/ru/plugins/host-marketplace.md#how-users-accept-a-headershelper-command). Ещё три правила зависят от того, в каком файле находится запись:

* **`strict`**: в отличие от записи в `marketplace.json` маркетплейса, записи в настройках не нужен `"strict": false`, поскольку файл настроек не содержит полей манифеста для встраивания. См. [Строгий режим](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#strict-mode).
* **Доверие к папке**: для записи в `.claude/settings.json` или `.claude/settings.local.json` проекта Claude Code запускает команду только после того, как пользователь также [доверился этой папке](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder).
* **Фильтр заголовков**: Claude Code удаляет [имена заголовков маршрутизации запросов и идентификации клиента](https://code.claude.com/docs/ru/plugins/host-marketplace.md#when-claude-code-skips-a-headershelper-command-or-drops-its-output) из записи в `.claude/settings.json` или `.claude/settings.local.json` проекта, поскольку эти файлы может предоставить репозиторий. Claude Code применяет тот же фильтр к записи каталога и к записи в настройках каталога `--add-dir` и не применяет никакого фильтра к записи в ваших пользовательских настройках, файле `--settings` или управляемых настройках.

#### Псевдонимы ключей маркетплейсов

В Claude Code v2.1.232 или новее можно записывать `extraKnownMarketplaces` как `additionalMarketplaces`, а `strictKnownMarketplaces` как `allowedMarketplaces`. Claude Code обрабатывает каждый псевдоним следующим образом:

* Более ранние версии игнорируют псевдоним, поэтому сохраняйте каноническое написание в файле, который читают и более старые версии, например в файле управляемых настроек для парка компьютеров со смешанными версиями Claude Code.
* В любом файле настроек, принимающем канонический ключ, Claude Code читает псевдоним точно так же, как канонический ключ.
* Claude Code может переписать `additionalMarketplaces` на `extraKnownMarketplaces` при обновлении файла.
* Если вы задаёте оба написания в одном файле, Claude Code использует каноническое значение и игнорирует псевдоним.

### `pluginConfigs`

Хранит нечувствительные ответы, которые вы даёте в диалоге конфигурации [`userConfig`](https://code.claude.com/docs/ru/plugins/manifest-reference#user-configuration) плагина, по ключу ID плагина. Claude Code записывает этот ключ в ваши пользовательские настройки, когда вы заполняете диалог, поэтому редактировать его вручную не нужно. Чувствительные параметры Claude Code вместо этого хранит в macOS Keychain, а если Keychain отклоняет запись, использует `~/.claude/.credentials.json`; на платформах без поддерживаемого хранилища ключей он хранит их в `~/.claude/.credentials.json`.

* **Область действия**: [`User or managed`](#scopes)
* **Тип**: объект, сопоставляющий ID плагина с объектом, содержащим поле `options`, которое сопоставляет имя каждого параметра со строкой, числом, значением Boolean или массивом строк, и необязательное поле `mcpServers` со значениями пользовательской конфигурации для каждого сервера в той же форме
* **По умолчанию**: не задано

В этом примере хранится параметр `api_endpoint` для плагина `deployer` из `acme-tools`:

```json settings.json theme={null}
{
  "pluginConfigs": {
    "deployer@acme-tools": {
      "options": {
        "api_endpoint": "https://api.example.com"
      }
    }
  }
}
```

Встроенные плагины хранят свои параметры под тем же ключом с суффиксом `@builtin`. Например, настройка [**Project instructions**](https://code.claude.com/docs/ru/memory.md#choose-which-instruction-files-load), определяющая, читает ли Claude Code файлы `AGENTS.md`, — это `pluginConfigs["cc-plugin-agents-md@builtin"].options.instructionFiles`. До v2.1.285 ID плагина был `agents-md@builtin`. Более поздние версии читают запись под любым из этих ID.

Claude Code игнорирует проектные и локальные записи, поскольку подставляет эти значения в конфигурации хуков, MCP и LSP плагинов, а клонированный репозиторий не должен иметь возможности их предоставлять.

### `prependPlugins`

Перечисляет управляемые плагины, [моды](https://code.claude.com/docs/ru/plugins/mods/overview.md) которых выполняются перед каждым модом, установленным пользователем, в указанном порядке. Задавая этот ключ в управляемых настройках, укажите в списке `sec-default@builtin`, чтобы сохранить встроенный страж. В управляемых настройках Claude Code пропускает ID, плагин которого не считается плагином вашей организации. Об этих условиях и о том, как два ключа порядка работают вместе, см. [Установка модов вашей организации и задание порядка](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods).

* **Область действия**: [`User or managed`](#scopes). Claude Code читает ключ из управляемых настроек. Из пользовательских настроек он читает ключ только на компьютере без управляемых настроек и без файла `managed-mcp.json`, в сессии, учётные данные которой не являются `/login` Team или Enterprise. Он игнорирует ключ в проектных и локальных настройках, а также в файле `--settings`.
* **Тип**: массив строк `plugin-name@marketplace-name`
* **По умолчанию**: не задано

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-guard@acme-tools": true },
  "prependPlugins": ["acme-guard@acme-tools", "sec-default@builtin"]
}
```

### `appendPlugins`

Перечисляет управляемые плагины, [моды](https://code.claude.com/docs/ru/plugins/mods/overview.md) которых выполняются после каждого мода, установленного пользователем, в указанном порядке. ID, указанный и в `prependPlugins`, и в `appendPlugins`, добавляется в начало. В управляемых настройках Claude Code пропускает ID, плагин которого не [считается плагином вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods).

* **Область действия**: [`User or managed`](#scopes). Claude Code читает ключ из управляемых настроек. Из пользовательских настроек он читает ключ только на компьютере без управляемых настроек и без файла `managed-mcp.json`, в сессии, учётные данные которой не являются `/login` Team или Enterprise. Он игнорирует ключ в проектных и локальных настройках, а также в файле `--settings`.
* **Тип**: массив строк `plugin-name@marketplace-name`
* **По умолчанию**: не задано

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-audit@acme-tools": true },
  "appendPlugins": ["acme-audit@acme-tools"]
}
```

## MCP

Контролируйте, к каким серверам MCP подключается Claude Code и какие разрешает организация. См. [Подключение к внешним инструментам с помощью MCP](https://code.claude.com/docs/ru/mcp.md) и [Управляемая конфигурация MCP](https://code.claude.com/docs/ru/managed-mcp.md).

### `allowAllClaudeAiMcps`

Загружайте [соединители claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai), которые Claude Code получает сам, наряду с развёрнутым `managed-mcp.json`. Без этого ключа `managed-mcp.json` получает исключительный контроль над серверами MCP и подавляет эти соединители.

* **Scope**: [`Managed`](#scopes). Пользователи не могут повторно включить соединители, которые исключительный контроль подавил.
* **Type**: Boolean
  * `true`: Claude Code загружает соединители claude.ai наряду с развёрнутым `managed-mcp.json`
  * `false`: развёрнутый `managed-mcp.json` получает исключительный контроль над серверами MCP и подавляет соединители claude.ai, [которые Claude Code получает сам](https://code.claude.com/docs/ru/mcp.md#how-connectors-reach-claude-code)
* **Default**: `false`, поэтому развёрнутый `managed-mcp.json` подавляет соединители claude.ai, которые Claude Code получает сам

```json managed-settings.json theme={null}
{
  "allowAllClaudeAiMcps": true
}
```

[`allowedMcpServers`](#allowedmcpservers) и [`deniedMcpServers`](#deniedmcpservers) по-прежнему применяются к соединителям, которые загружает этот ключ. Соединители, доставленные в [облачный сеанс](https://code.claude.com/docs/ru/claude-code-on-the-web.md), хост которого содержит `managed-mcp.json`, например самостоятельно размещённый runner, остаются подавленными. См. [Разрешить соединители claude.ai наряду с управляемым набором](https://code.claude.com/docs/ru/managed-mcp.md#allow-claude-ai-connectors-alongside-the-managed-set).

### `allowClaudeInChromeWithManagedMcp`

Позволяйте встроенному серверу [Claude в Chrome](https://code.claude.com/docs/ru/chrome.md) работать наряду с развёрнутым `managed-mcp.json`. Без этого ключа развёрнутый `managed-mcp.json` блокирует Claude в Chrome в сеансах терминала. Требует Claude Code версии 2.1.282 или позже.

* **Scope**: [`Managed`](#scopes), только из собственных управляемых параметров устройства: развёрнутого MDM plist или ключа реестра HKLM, или системного файла `managed-settings.json`. Claude Code игнорирует его в управляемых параметрах сервера, в пользовательском реестре HKCU и в пользовательских или проектных параметрах.
* **Type**: Boolean
  * `true`: встроенный сервер Claude в Chrome может работать наряду с развёрнутым `managed-mcp.json`
  * `false`: развёрнутый `managed-mcp.json` блокирует Claude в Chrome в сеансах терминала
* **Default**: `false`, поэтому развёрнутый `managed-mcp.json` блокирует Claude в Chrome в сеансах терминала

```json managed-settings.json theme={null}
{
  "allowClaudeInChromeWithManagedMcp": true
}
```

Запись [`deniedMcpServers`](#deniedmcpservers) для `claude-in-chrome` по-прежнему блокирует сервер с этим ключом включённым. См. [Разрешить Claude в Chrome наряду с управляемым набором](https://code.claude.com/docs/ru/managed-mcp.md#allow-claude-in-chrome-alongside-the-managed-set).

### `allowedMcpServers`

Создайте список разрешённых серверов MCP, которые люди могут добавлять. Claude Code блокирует любой сервер, который не соответствует записи, где бы он ни был определён, включая серверы плагинов, серверы, переданные с `--mcp-config`, и серверы из claude.ai.

Встроенные серверы, такие как Claude в Chrome, сервер `ide`, к которому Claude Code подключается в работающей IDE [VS Code](https://code.claude.com/docs/ru/vs-code.md#the-built-in-ide-mcp-server) или [JetBrains](https://code.claude.com/docs/ru/jetbrains.md#the-built-in-ide-mcp-server), и серверы, которые сам CLI настраивает, освобождены от списка разрешений, и список запретов по-прежнему применяется к ним. На Claude Code версии 2.1.268 или позже, инструменты Slack сеанса [Claude Tag](https://code.claude.com/docs/ru/claude-tag.md) также освобождены от списка разрешений, и список запретов по-прежнему применяется к ним. Внутрипроцессные серверы `type: "sdk"` освобождены от обоих списков; [приложение, которое запустило сеанс](https://code.claude.com/docs/ru/mcp.md#how-connectors-reach-claude-code), регистрирует их.

Серверы, которые доставляет ваша организация, также освобождены от списка разрешённых серверов, но список запрещённых серверов к ним по-прежнему применяется. Освобождение охватывает каждую запись [`managedMcpServers`](#managedmcpservers) и любую запись [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp#exclusive-control-with-managed-mcp-json), значения которой [не используют расширение `${VAR}` за пределами `env`](https://code.claude.com/docs/ru/managed-mcp#how-allowlists-and-denylists-apply-to-the-managed-set). Полный порядок проверки см. в разделе [Как оценивается сервер](https://code.claude.com/docs/ru/managed-mcp.md#how-a-server-is-evaluated). До версии 2.1.259 серверы из `managed-mcp.json` также должны были соответствовать списку.

* **Scope**: [`Any file`](#scopes). Записи из каждого файла объединяются в один список разрешений, если не установлен [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly). Разверните его в управляемых параметрах, чтобы обеспечить его.
* **Type**: массив объектов, каждый ровно с одним ключом. Используйте `serverName` — строку, ограниченную буквами, цифрами, дефисами и подчёркиваниями; `serverCommand` — массив из команды и её аргументов, сопоставляемый точно; или `serverUrl` — шаблон URL с подстановочными знаками `*`
* **Default**: не установлено, поэтому каждый сервер разрешён; пустой массив блокирует каждый сервер, который добавляют пользователи

Этот пример разрешает только сервер stdio, который запускает указанная команда `npx`:

```json settings.json theme={null}
{
  "allowedMcpServers": [
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] }
  ]
}
```

Запись [`deniedMcpServers`](#deniedmcpservers) имеет приоритет, поэтому сервер в обоих списках блокируется. Как только список содержит любую запись `serverCommand`, сервер stdio должен совпадать с записью `serverCommand`, и как только он содержит любую запись `serverUrl`, удалённый сервер должен совпадать с записью `serverUrl`: совпадение `serverName` больше не допускает этот вид сервера. См. [Управление на основе политики со списками разрешений и запретов](https://code.claude.com/docs/ru/managed-mcp.md#policy-based-control-with-allowlists-and-denylists).

### `allowManagedMcpServersOnly`

Сделайте управляемый список разрешений единственным применяемым. Claude Code затем читает [`allowedMcpServers`](#allowedmcpservers) только из управляемых параметров и игнорирует списки разрешений в пользовательских, проектных и локальных параметрах; [`deniedMcpServers`](#deniedmcpservers) по-прежнему объединяется из каждой области параметров, поэтому пользователи могут по-прежнему блокировать серверы для себя. Администраторы устанавливают это так, чтобы собственные параметры пользователя не могли расширить то, что разрешает управляемый список разрешений.

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code читает `allowedMcpServers` только из управляемых параметров и игнорирует списки разрешений в пользовательских, проектных и локальных параметрах
  * `false`: списки разрешений из каждой области параметров объединяются
* **Default**: `false`, поэтому списки разрешений из каждой области параметров объединяются

Этот пример блокирует список разрешений для управляемых параметров и разрешает только сервер с именем `github`:

```json managed-settings.json theme={null}
{
  "allowManagedMcpServersOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" }
  ]
}
```

Пользователи могут по-прежнему добавлять серверы MCP самостоятельно; загружаются только серверы, которые совпадают с управляемым списком разрешений. См. [Ограничить список разрешений только управляемыми параметрами](https://code.claude.com/docs/ru/managed-mcp.md#restrict-the-allowlist-to-managed-settings-only).

### `deniedMcpServers`

Блокируйте определённые серверы MCP. Claude Code отказывается загружать совпадающий сервер, где бы он ни был определён, включая серверы плагинов, серверы, переданные с `--mcp-config`, серверы из `managed-mcp.json`, серверы из [`managedMcpServers`](#managedmcpservers) и соединители claude.ai, [которые он получает сам](https://code.claude.com/docs/ru/mcp.md#how-connectors-reach-claude-code). Внутрипроцессные серверы `type: "sdk"` освобождены; приложение, которое запустило сеанс, регистрирует их.

* **Scope**: [`Any file`](#scopes). Записи из каждого файла объединяются в один список запретов, и [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly) это не меняет. Разверните его в управляемых параметрах, чтобы обеспечить его.
* **Type**: массив объектов, каждый с ровно одним ключом: `serverName`, строка, поэтому отображаемое имя соединителя claude.ai, такое как `"claude.ai Slack"`, работает; `serverCommand`, массив команды и её аргументов, совпадающих точно; или `serverUrl`, шаблон URL с подстановочными знаками `*`
* **Default**: не установлено, поэтому ни один сервер не блокируется; пустой массив также ничего не блокирует

```json settings.json theme={null}
{
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ]
}
```

Список запретов имеет приоритет над [`allowedMcpServers`](#allowedmcpservers), поэтому сервер в обоих списках блокируется. См. [Управление на основе политики со списками разрешений и запретов](https://code.claude.com/docs/ru/managed-mcp.md#policy-based-control-with-allowlists-and-denylists).

### `disableClaudeAiConnectors`

Отключите [соединители MCP claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai), [которые Claude Code получает сам](https://code.claude.com/docs/ru/mcp.md#how-connectors-reach-claude-code), чтобы он ни получал, ни подключал их. `true` в любом файле параметров применяется: проверенный в репозитории проект `.claude/settings.json` может отказать репозиторию в этих соединителях, но проектный уровень `false` не может переопределить пользовательский или управляемый уровень `true`.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code ни получает, ни подключает эти соединители
  * `false`: то же самое, что и не установлено; Claude Code получает ваши соединители, если другой файл параметров или `ENABLE_CLAUDEAI_MCP_SERVERS` их не отключает
* **Default**: `false`, поэтому Claude Code получает ваши соединители
* **Per-session overrides**: [`ENABLE_CLAUDEAI_MCP_SERVERS`](https://code.claude.com/docs/ru/env-vars), установленный на `false`, отключает соединители на один сеанс; какой бы из двух их ни отключил, другой не может их включить обратно

```json settings.json theme={null}
{
  "disableClaudeAiConnectors": true
}
```

Серверы, которые вы явно передаёте с `--mcp-config`, не затрагиваются. Чтобы блокировать отдельные соединители вместо всех, используйте [`deniedMcpServers`](#deniedmcpservers). См. [Отключить соединители claude.ai](https://code.claude.com/docs/ru/mcp.md#disable-claude-ai-connectors).

### `disabledMcpjsonServers`

Отклоняйте определённые серверы, определённые в файле `.mcp.json` проекта, чтобы Claude Code никогда их не подключал и не просил вас их одобрить. Отклонение в любом файле параметров применяется, включая проект `.claude/settings.json`, проверенный в репозитории.

* **Scope**: [`Any file`](#scopes)
* **Type**: массив строк, имена серверов, как они появляются в `.mcp.json`
* **Default**: не установлено

```json settings.json theme={null}
{
  "disabledMcpjsonServers": ["filesystem"]
}
```

Claude Code записывает этот ключ в `.claude/settings.local.json`, когда вы отклоняете сервер в диалоговом окне одобрения. `claude mcp get <name>` показывает отклонённый сервер как `✘ Rejected (see disabledMcpjsonServers in settings)`. Отклонение имеет приоритет над [`enabledMcpjsonServers`](#enabledmcpjsonservers) и [`enableAllProjectMcpServers`](#enableallprojectmcpservers).

### `enableAllProjectMcpServers`

Одобряйте каждый сервер MCP, определённый в файлах проекта `.mcp.json`, без подсказки. Claude Code записывает этот ключ в `.claude/settings.local.json`, когда вы выбираете одобрение всех серверов в диалоговом окне одобрения.

* **Scope**: [`Any file`](#scopes). В папке, диалоговое окно доверия которой вы не приняли, Claude Code соблюдает его из пользовательских параметров, управляемых параметров и `--settings` и игнорирует его в общем файле проекта, как в сеансе, так и для `claude mcp list` и `claude mcp get`; [Одобрения серверов проекта и доверие рабочей области](https://code.claude.com/docs/ru/mcp.md#project-server-approvals-and-workspace-trust) говорит, когда неотслеживаемый `.claude/settings.local.json` также считается.
* **Type**: Boolean
  * `true`: Claude Code одобряет каждый сервер MCP, определённый в файлах проекта `.mcp.json`, без подсказки
  * `false`: Claude Code просит вас одобрить каждый сервер. В доверенной папке `false` в файле с более высоким приоритетом переопределяет `true` в файле с более низким приоритетом; в папке, которой вы не доверяете, `true` в любом соблюдаемом файле достаточно
* **Default**: не установлено, поэтому Claude Code просит вас одобрить каждый сервер

```json settings.json theme={null}
{
  "enableAllProjectMcpServers": true
}
```

Запись [`disabledMcpjsonServers`](#disabledmcpjsonservers) по-прежнему отклоняет сервер.

### `enabledMcpjsonServers`

Одобряйте определённые серверы, определённые в файлах проекта `.mcp.json`, чтобы Claude Code подключал их без вопросов. Claude Code записывает этот ключ в `.claude/settings.local.json`, когда вы одобряете сервер в диалоговом окне одобрения.

* **Scope**: [`Any file`](#scopes). В папке, диалоговое окно доверия которой вы не приняли, Claude Code соблюдает его из пользовательских параметров, управляемых параметров и `--settings` и игнорирует его в общем файле проекта, как в сеансе, так и для `claude mcp list` и `claude mcp get`; [Одобрения серверов проекта и доверие рабочей области](https://code.claude.com/docs/ru/mcp.md#project-server-approvals-and-workspace-trust) говорит, когда неотслеживаемый `.claude/settings.local.json` также считается.
* **Type**: массив строк, имена серверов, как они появляются в `.mcp.json`
* **Default**: не установлено

Этот пример одобряет серверы `memory` и `github` из `.mcp.json` проекта:

```json settings.json theme={null}
{
  "enabledMcpjsonServers": ["memory", "github"]
}
```

Запись [`disabledMcpjsonServers`](#disabledmcpjsonservers) по-прежнему отклоняет сервер.

### `managedMcpServers`

Предоставляйте удалённые серверы MCP каждому пользователю из управляемых параметров. Пользователи сохраняют серверы, которые они добавляют сами, и не могут редактировать или удалять те, которые вы предоставляете. Требует Claude Code версии 2.1.259 или позже.

* **Scope**: [`Managed`](#scopes). Claude Code удаляет ключ с предупреждением в пользовательских, проектных и локальных параметрах и не читает его в вкладке Code приложения Claude Desktop при развёртывании третьей стороной или в сеансах Cowork приложения, где Claude Desktop сам предоставляет и блокирует серверы MCP этих сеансов.
* **Type**: объект, ключ которого — имя сервера. Каждая запись имеет форму `.mcp.json` для сервера `http` или `sse`: требуемый `https://` `url` и опционально `headers`, `oauth` и другие параметры HTTP и SSE. Claude Code удаляет записи, которые не прошли проверку, и [Что может содержать запись](https://code.claude.com/docs/ru/managed-mcp.md#what-an-entry-can-contain) перечисляет условия
* **Default**: не установлено, поэтому управляемые параметры не предоставляют серверы

Этот пример предоставляет один HTTP-сервер с именем `search`:

```json managed-settings.json theme={null}
{
  "managedMcpServers": {
    "search": {
      "type": "http",
      "url": "https://search.example.com/mcp"
    }
  }
}
```

Для приоритета, как предоставленные серверы объединяются с `managed-mcp.json` и списками разрешений и запретов, и что видят пользователи, см. [Предоставлять серверы через управляемые параметры](https://code.claude.com/docs/ru/managed-mcp.md#provide-servers-through-managed-settings).

## Агенты, сессии и worktrees

Установите агента по умолчанию, управляйте участниками команды и обменом сообщениями между сессиями, а также настройте worktrees. См. [Субагенты](https://code.claude.com/docs/ru/sub-agents.md) и [Worktrees](https://code.claude.com/docs/ru/worktrees.md).

### `agent`

Запустите основной поток как именованный [субагент](https://code.claude.com/docs/ru/sub-agents.md#invoke-subagents-explicitly), чтобы Claude Code применил системный промпт, ограничения инструментов и модель этого субагента к вашей сессии. Один и тот же ключ устанавливает агента по умолчанию для сессий, которые вы отправляете из `claude agents`.

* **Scope**: [`Any file`](#scopes)
* **Type**: string, имя встроенного или пользовательского агента
* **Default**: не установлено
* **Per-session overrides**: `--agent` имеет приоритет над этим ключом для одной сессии

```json settings.json theme={null}
{
  "agent": "code-reviewer"
}
```

### `crossSessionInbound`

Выберите, что эта сессия делает с [сообщениями, поступающими из ваших других сессий Claude Code](https://code.claude.com/docs/ru/cross-session-messaging.md#control-inbound-messages). Когда ни одно значение не применяется, Claude Code решает для каждого сообщения на основе классов режима разрешений двух сессий.

* **Scope**: [`Any file`](#scopes). Значение проекта или локальное значение применяется только в том случае, если оно строже, чем значение управляемых настроек, флага `--settings` или пользовательских настроек.
* **Type**: string, один из:
  * `"accept"`: Claude Code доставляет сообщение Claude
  * `"hold"`: Claude Code показывает уведомление о сообщении без его доставки
  * `"refuse"`: Claude Code отбрасывает сообщение
* **Default**: не установлено, поэтому Claude Code решает для каждого сообщения

```json settings.json theme={null}
{
  "crossSessionInbound": "hold"
}
```

Claude Code сначала читает управляемые настройки, затем флаг `--settings`, затем пользовательские настройки и применяет первое найденное значение. `refuse` строже, чем `hold`, а `hold` строже, чем `accept`. Когда ни один из доверенных источников не устанавливает значение, проектное или локальное `hold` или `refuse` все еще применяется, заменяя решение по умолчанию для каждого сообщения. В сессиях с обменом сообщениями между сессиями этот ключ появляется в `/config` как **Messages from your other sessions**, который записывает его в пользовательские настройки; строка требует Claude Code v2.1.232 или позже, и Claude Code скрывает её, пока флаг `--settings` или управляемые настройки устанавливают ключ.

Claude Code [предупреждает](https://code.claude.com/docs/ru/errors.md#crosssessioninbound-must-be-one-of-accept-hold-refuse) при установке значения, которое он не распознает. Пока это значение присутствует в пользовательском, проектном, локальном или файле `--settings`, Claude Code удерживает входящие сообщения, даже когда источник, который имеет приоритет, устанавливает `accept`. `refuse`, установленный другим источником, все еще применяется. Исправьте или удалите значение, чтобы снять удержание.

Когда неузнанное значение находится в [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md), Claude Code вместо этого рассматривает его как `refuse` до тех пор, пока администратор не исправит его. До v2.1.248 Claude Code игнорировал неузнанное значение без предупреждения.

### `disableAgentView`

Отключите [фоновых агентов и представление агентов](https://code.claude.com/docs/ru/agent-view.md): `claude agents`, `--bg`, `/background` и супервизора по требованию. Установите его в [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md), чтобы применить его для организации.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code отключает `claude agents`, `--bg`, `/background` и супервизора по требованию
  * `false`: представление агентов доступно
* **Default**: не установлено, поэтому представление агентов доступно
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_AGENT_VIEW`](https://code.claude.com/docs/ru/env-vars) отключает представление агентов для одной сессии; какой бы из двух его ни отключил, другой не может его снова включить

```json settings.json theme={null}
{
  "disableAgentView": true
}
```

### `isolatePeerMachines`

Требуйте вашего явного подтверждения перед тем, как `SendMessage` Claude достигнет одну из ваших сессий за пределами этой машины; см. [Require approval for cross-machine messages](https://code.claude.com/docs/ru/cross-session-messaging.md#require-approval-for-cross-machine-messages). Запрос подтверждения появляется даже в режиме [`bypassPermissions`](https://code.claude.com/docs/ru/permission-modes#skip-all-checks-with-bypasspermissions-mode).

* **Scope**: [`Any file`](#scopes). `true` из любой области действия применяется, поэтому зафиксированный в репозитории файл проекта может включить требование, но не отключить его.
* **Type**: Boolean
  * `true`: Claude Code запрашивает ваше подтверждение перед тем, как `SendMessage` Claude достигнет одну из ваших сессий за пределами этой машины
  * `false`: сообщения между машинами не вызывают запрос
* **Default**: не установлено, поэтому сообщения между машинами не вызывают запрос

```json settings.json theme={null}
{
  "isolatePeerMachines": true
}
```

Подтверждение `SendMessage` между машинами требует Claude Code v2.1.224 или позже.

### `processWrapper`

На macOS и Linux поместите команду корпоративного лаунчера перед [фоновыми процессами, которые запускает Claude Code](https://code.claude.com/docs/ru/corporate-launcher.md#what-the-launcher-covers). Claude Code запускает лаунчер с добавленной собственной командной строкой, поэтому лаунчер должен выполнить exec в Claude Code; см. [Run Claude Code behind a corporate launcher](https://code.claude.com/docs/ru/corporate-launcher.md) для контракта лаунчера. Требуется Claude Code v2.1.210 или позже.

* **Scope**: [`User or managed`](#scopes)
* **Type**: string, команда лаунчера как префикс argv, например абсолютный путь с необязательными аргументами
* **Default**: не установлено, поэтому фоновые процессы запускаются без обёртки
* **Per-session overrides**: [`CLAUDE_CODE_PROCESS_WRAPPER`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом для одной сессии

```json settings.json theme={null}
{
  "processWrapper": "/opt/corp/launcher --profile claude"
}
```

Claude Code игнорирует лаунчер на Windows и запускает каждый процесс без обёртки. Требуется Claude Code v2.1.210 или позже.

### `teammateMode`

Выберите, где Claude Code показывает участников [команды агентов](https://code.claude.com/docs/ru/agent-teams.md): внутри вашей основной панели терминала или в разделённых панелях, когда ваш терминал их поддерживает. См. [Choose a display mode](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode).

* **Scope**: [`Any file`](#scopes). Claude Code также читает значение, оставленное в `~/.claude.json` старыми версиями.
* **Type**: string, один из:
  * `"in-process"`: участники команды работают внутри вашей основной панели терминала
  * `"auto"`: разделённые панели, когда вы работаете внутри tmux, или внутри iTerm2 с `it2` в вашем `PATH` или установленным tmux; в противном случае в процессе
  * `"tmux"`: разделённые панели с использованием tmux или iTerm2, определяемые по вашему терминалу
  * `"iterm2"`: собственные разделённые панели iTerm2 через CLI `it2`
* **Default**: `"in-process"`
* **Per-session overrides**: `--teammate-mode` имеет приоритет над этим ключом для одной сессии

```json settings.json theme={null}
{
  "teammateMode": "auto"
}
```

### `worktree`

Настройте, как Claude Code создаёт и управляет [git worktrees](https://code.claude.com/docs/ru/worktrees.md) для `--worktree`, инструмента `EnterWorktree` и изолированных субагентов и фоновых сессий.

* **Scope**: [`Any file`](#scopes)
* **Type**: object с `baseRef`, `symlinkDirectories`, `sparsePaths` и `bgIsolation`
* **Default**: не установлено

Этот пример ответвляет новые worktrees от вашего текущего `HEAD` и создаёт символические ссылки на `node_modules` в каждом из них:

```json settings.json theme={null}
{
  "worktree": {
    "baseRef": "head",
    "symlinkDirectories": ["node_modules"]
  }
}
```

Чтобы скопировать игнорируемые git файлы, такие как `.env`, в новые worktrees, добавьте файл [`.worktreeinclude`](https://code.claude.com/docs/ru/worktrees#copy-gitignored-files-into-worktrees) в корень вашего проекта вместо настройки.

### `worktree.baseRef`

Выберите, от какого ref ответвляются новые worktrees. `"fresh"` ответвляется от `origin/<default-branch>` для чистого дерева, соответствующего удалённому; `"head"` ответвляется от вашего текущего локального `HEAD`, поэтому неотправленные коммиты и состояние ветки функции присутствуют в worktree.

* **Scope**: [`Any file`](#scopes)
* **Type**: string, один из:
  * `"fresh"`: новые worktrees ответвляются от `origin/<default-branch>`
  * `"head"`: новые worktrees ответвляются от вашего текущего локального `HEAD`, включая неотправленные коммиты
* **Default**: `"fresh"`

```json settings.json theme={null}
{
  "worktree": {
    "baseRef": "head"
  }
}
```

Внутри связанного worktree `"head"` разрешается в `HEAD` этого worktree, а не в основной checkout.

### `worktree.symlinkDirectories`

Создайте символические ссылки на каталоги из основного репозитория в каждом worktree, чтобы не дублировать большие каталоги на диске.

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings, пути каталогов относительно корня репозитория
* **Default**: не установлено, поэтому Claude Code не создаёт символические ссылки на каталоги

Этот пример создаёт символические ссылки на `node_modules` и `.cache` из основного репозитория в каждом новом worktree:

```json settings.json theme={null}
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"]
  }
}
```

### `worktree.sparsePaths`

Извлекайте только перечисленные каталоги в каждом worktree через git sparse-checkout. Claude Code записывает на диск только эти каталоги плюс файлы на уровне корня, что быстрее в больших монорепозиториях; см. [Check out only the directories you need](https://code.claude.com/docs/ru/large-codebases.md#check-out-only-the-directories-you-need).

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings, пути каталогов относительно корня репозитория
* **Default**: не установлено, поэтому каждый worktree извлекает всё дерево

Включите `.claude` в список, чтобы каждый worktree также содержал `.claude/settings.json` и `.claude/rules/` репозитория. Этот пример извлекает только `.claude`, `packages/my-app` и `shared/utils`, плюс файлы на уровне корня, в каждом worktree:

```json settings.json theme={null}
{
  "worktree": {
    "sparsePaths": [".claude", "packages/my-app", "shared/utils"]
  }
}
```

Пока существует разреженный worktree, git включает `extensions.worktreeConfig` в общем `.git/config` репозитория.

### `worktree.bgIsolation`

Выберите, как [фоновые сессии](https://code.claude.com/docs/ru/agent-view.md#how-file-edits-are-isolated) изолируют свои редактирования файлов. Если вы перевели сессию в фоновый режим с помощью `←` или `/background`, эта сессия редактирует файлы на месте независимо от значения этого ключа. С `"worktree"` Claude Code блокирует `Edit` и `Write` в основном checkout до тех пор, пока сессия не вызовет `EnterWorktree`; с `"none"` фоновые задания редактируют рабочую копию напрямую. Установите `"none"` для репозитория, где git worktrees непрактичны.

* **Scope**: [`Any file`](#scopes)
* **Type**: string, один из:
  * `"worktree"`: Claude Code блокирует `Edit` и `Write` в основном checkout до тех пор, пока сессия не вызовет `EnterWorktree`
  * `"none"`: фоновые задания редактируют рабочую копию напрямую
* **Default**: `"worktree"`

```json settings.json theme={null}
{
  "worktree": {
    "bgIsolation": "none"
  }
}
```

Вне git-репозитория [хук `WorktreeCreate`](https://code.claude.com/docs/ru/worktrees#non-git-version-control), который завершается с ошибкой, снимает блокировку, чтобы сессия могла редактировать рабочий каталог на месте.

### `worktree.location`

Выберите папку на удалённой машине, в которой [сессии Desktop по SSH](https://code.claude.com/docs/ru/desktop.md#choose-where-ssh-session-worktrees-go) создают свои worktrees, вместо `<project-root>/.claude/worktrees/`. Этот ключ читает только настольное приложение: `--worktree`, инструмент `EnterWorktree`, изолированные субагенты и фоновые сессии его игнорируют. Требуется Claude Desktop v1.44121.0 или позже.

* **Scope**: [`User`](#scopes), в `~/.claude/settings.json` на удалённой машине
* **Type**: string, абсолютный путь или путь, начинающийся с `~/`
* **Default**: не установлено, поэтому worktrees размещаются внутри проекта

Этот пример задаёт папку `~/worktrees`:

```json settings.json theme={null}
{
  "worktree": {
    "location": "~/worktrees"
  }
}
```

Значение **Worktree folder**, заданное для SSH-подключения в Desktop, имеет приоритет. Если ваша организация ограничивает папки, которые могут использовать сессии, Desktop размещает worktrees внутри проекта.

## Удалённое управление, настольное приложение и уведомления

Настройте удалённое управление, облачные среды, настольное приложение и уведомления, которые Claude Code отправляет, когда вам нужна помощь. См. [Удалённое управление](https://code.claude.com/docs/ru/remote-control.md).

### `agentPushNotifEnabled`

Разрешить Claude отправлять push-уведомление на ваш телефон, когда он решит, что его стоит отправить, например, когда завершится длительная задача. В локальной сессии Claude может отправить его, пока подключён [Remote Control](https://code.claude.com/docs/ru/remote-control.md). Отображается в `/config` как **Push when Claude decides**.

* **Scope**: [`Any file`](#scopes). Claude Code также читает значение, оставленное в `~/.claude.json` старыми версиями.
* **Type**: Boolean
  * `true`: Claude может отправлять push-уведомление на ваш телефон, когда он решит, что оно стоит отправить
  * `false`: Claude не отправляет эти уведомления
* **Default**: `false`

```json settings.json theme={null}
{
  "agentPushNotifEnabled": true
}
```

Одного этого ключа недостаточно, чтобы получать уведомления. Чтобы настроить их, выполните шаги из раздела [Mobile push notifications](https://code.claude.com/docs/ru/remote-control.md#mobile-push-notifications).

Если вы запускаете сессии через сервер [`claude remote-control`](https://code.claude.com/docs/ru/remote-control#start-a-remote-control-session), они следуют значению, сохранённому в вашей учётной записи, а не этому ключу. Чтобы изменить это значение, выполните `/config` в сессии Claude Code в терминале и включите или отключите **Push when Claude decides**. Если переключатель уже показывает нужное вам значение, измените его и верните обратно, чтобы Claude Code сохранил это значение в вашей учётной записи.

### `awaySummaryEnabled`

Показывать однострочный краткий обзор сеанса, когда вы вернётесь в терминал после нескольких минут отсутствия. Установите значение `false` или отключите **Session recap** в `/config`, чтобы отключить краткий обзор.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: вы видите однострочный краткий обзор сеанса, когда вернётесь после нескольких минут отсутствия
  * `false`: Claude Code не показывает краткий обзор
* **Default**: не установлено, поэтому краткий обзор включён
* **Per-session overrides**: [`CLAUDE_CODE_ENABLE_AWAY_SUMMARY`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом для одного сеанса в любом направлении

```json settings.json theme={null}
{
  "awaySummaryEnabled": false
}
```

Claude Code никогда не показывает краткий обзор в неинтерактивном режиме.

### `disableArtifact`

> [!WARNING]
>
> Устарело и заменено на [`enableArtifact`](#enableartifact). Claude Code по-прежнему учитывает `disableArtifact: true` как эквивалент `enableArtifact: false` и игнорирует `disableArtifact: false`.

Используйте [`enableArtifact`](#enableartifact) вместо этого, чтобы отключить инструмент [Artifact](https://code.claude.com/docs/ru/artifacts.md), который публикует выходные данные сеанса как приватную веб-страницу на claude.ai. Когда вы отключаете строку **Artifacts** в `/config`, Claude Code записывает `enableArtifact` в ваши пользовательские настройки и очищает этот ключ.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code отключает инструмент Artifact для каждого сеанса, к которому применяется файл, и ни один другой файл не включает его обратно
  * `false`: игнорируется; чтобы оставить инструмент включённым, удалите ключ
* **Default**: не установлено, поэтому инструмент следует [доступности](https://code.claude.com/docs/ru/artifacts.md#availability) вашей учётной записи
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_ARTIFACT`](https://code.claude.com/docs/ru/env-vars) установленный на `1` отключает инструмент для одного сеанса

```json settings.json theme={null}
{
  "disableArtifact": true
}
```

[Disable artifacts](https://code.claude.com/docs/ru/artifacts.md#disable-artifacts) перечисляет все способы отключения инструмента.

### `disableDeepLinkRegistration`

Запретить Claude Code регистрировать обработчик протокола `claude-cli://` в операционной системе. [Deep links](https://code.claude.com/docs/ru/deep-links.md) позволяют внешним инструментам открывать сессию Claude Code с предзаполненным промптом. Установите это в окружениях, где регистрация обработчика протокола ограничена или управляется отдельно.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка `"disable"`
* **Default**: не установлено, поэтому Claude Code регистрирует обработчик

```json settings.json theme={null}
{
  "disableDeepLinkRegistration": "disable"
}
```

### `disableDesktopLocalSessions`

Отключить сессии Code, которые работают на устройстве в [настольном приложении](https://code.claude.com/docs/ru/desktop.md#local-sessions-on-managed-devices), для развёртываний, где разработчики должны работать на удалённых машинах через SSH. Когда ключ установлен в `true`, пользователи видят на вкладке Code следующее:

* **Список выбора окружения**: запись для компьютера пользователя неактивна и недоступна для выбора, с подсказкой **Disabled by your organization**. На Windows запись WSL неактивна таким же образом, хотя то, работают ли сессии WSL на управляемом устройстве вообще, [регулируется отдельно](https://code.claude.com/docs/ru/admin-setup.md#wsl-sessions-in-claude-code-desktop).
* **Новые сессии**: по умолчанию используют первое [SSH-соединение](https://code.claude.com/docs/ru/desktop.md#ssh-sessions), если оно настроено
* **Сессии на устройстве**: приложение отказывается запускать или возобновлять сессию на устройстве, включая SSH-соединение обратно на ту же машину
* **SSH-сессии на другие хосты и облачные сессии**: не затрагиваются

Настольное приложение читает этот ключ; терминальный CLI его игнорирует. Требуется Claude Desktop v1.37937.0 или новее.

* **Scope**: [`Managed`](#scopes). По умолчанию настольное приложение читает ключ из [одного управляемого источника](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources).
* **Type**: Boolean; только JSON Boolean `true` имеет эффект
  * `true`: настольное приложение не предлагает сеансы Code на устройстве; существующие локальные сеансы остаются в списке, но не могут продолжаться
  * `false`: локальные сеансы остаются доступными
* **Default**: не установлено, поэтому локальные сеансы доступны

```json managed-settings.json theme={null}
{
  "disableDesktopLocalSessions": true
}
```

Настольное приложение игнорирует любое другое значение, и значение, которое не является Boolean, такое как строка `"true"` или `1`, также регистрирует предупреждение. Используйте его вместе с [`sshConfigs`](#sshconfigs), чтобы пользователи попадали на рабочее соединение, и с [`sshHostAllowlist`](#sshhostallowlist), чтобы ограничить, какие хосты они могут достичь. См. [Local sessions on managed devices](https://code.claude.com/docs/ru/desktop.md#local-sessions-on-managed-devices).

Claude Desktop предоставляет сеансы Code с политикой, полученной из конфигурации вашего настольного приложения, например список разрешённых исходящих соединений, изоляция файловой системы и ограничения MCP в развёртываниях третьих сторон. Claude Code игнорирует эти родительские настройки всякий раз, когда присутствует [источник администратора](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources): управляемые сервером настройки, политика MDM или уровня ОС, или файл управляемых настроек. Развёртывание этого ключа через один из них на устройстве, которое не имело ни одного раньше, как в развёртываниях третьих сторон, поэтому останавливает применение политик, полученных из настольного приложения. [Let an embedding host add policy](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy) охватывает, когда родительские настройки всё ещё могут объединяться; это применяется к любому ключу, который вы развёртываете таким образом, не только к этому.

### `disableRemoteControl`

Отключить [Удалённое управление](https://code.claude.com/docs/ru/remote-control.md): Claude Code затем отказывает в `claude remote-control`, флаге `--remote-control`, автозапуске и переключателе в сеансе, и сообщает, что политика вашей организации это отключила. Поместите это в [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) для принудительного применения MDM на каждом устройстве.

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code отказывает в `claude remote-control`, флаге `--remote-control`, автозапуске и переключателе в сеансе
  * `false`: Удалённое управление остаётся доступным
* **Default**: `false`

```json settings.json theme={null}
{
  "disableRemoteControl": true
}
```

### `disableRemotePreviewScripts`

Запретить выполнение скриптов, когда пользователи [просматривают HTML-файл](https://code.claude.com/docs/ru/desktop.md#preview-html-files-in-ssh-and-wsl-sessions) из сессии SSH или WSL в настольном приложении. Внешний просмотр веб-страниц на панели Browser не затрагивается.

Настольное приложение читает этот ключ; терминальный CLI его игнорирует. Требуется Claude Desktop v5.1231.0 или новее. Более ранние версии игнорируют ключ: чтобы остановить скрипты в них, также установите [`disableBrowserExternalNavigation`](#disablebrowserexternalnavigation), который заодно отключает и внешний просмотр веб-страниц.

* **Scope**: [`Managed`](#scopes). Настольное приложение не читает ключ с удалённой машины или из дистрибутива WSL.
* **Type**: Boolean; действует только JSON Boolean `true`
  * `true`: предпросмотр HTML в сессиях SSH и WSL не выполняет скрипты
  * `false`: ключ не отключает скрипты
* **Default**: не установлено, поэтому ключ ни на что не влияет

Если компьютер, на котором работает настольное приложение, не получает никаких других управляемых настроек Claude Code, также установите [`parentSettingsBehavior`](#parentsettingsbehavior) в `"merge"` в создаваемых вами управляемых настройках. На Windows, если вы создаёте файл управляемых настроек, пользователи также теряют сессии WSL, пока вы [не разрешите их](https://code.claude.com/docs/ru/admin-setup.md#wsl-sessions-in-claude-code-desktop). [Turn off scripts in SSH and WSL previews for your organization](https://code.claude.com/docs/ru/desktop.md#turn-off-scripts-in-ssh-and-wsl-previews-for-your-organization) объясняет оба момента и указывает, где задать ключ.

Этот пример показывает только сам ключ в том виде, в каком вы добавили бы его в управляемые настройки, которые компьютер уже получает:

```json managed-settings.json theme={null}
{
  "disableRemotePreviewScripts": true
}
```

Настольное приложение игнорирует любое другое значение, а значение, которое не является Boolean, например строка `"true"` или `1`, также приводит к записи предупреждения в лог.

### `enableArtifact`

Отключить инструмент [Artifact](https://code.claude.com/docs/ru/artifacts.md), который публикует выходные данные сессии как приватную веб-страницу на claude.ai. Когда вы отключаете строку **Artifacts** в `/config`, Claude Code записывает этот ключ в ваши пользовательские настройки, поэтому вы обычно не редактируете его вручную.

* **Scope**: [`Any file`](#scopes). Каждый файл может отключить инструмент, и ни один не может включить его обратно.
* **Type**: Boolean
  * `false`: Claude Code отключает инструмент Artifact для каждого сеанса, к которому применяется файл
  * `true`: то же самое, что оставить ключ не установленным, потому что он никогда не переопределяет `false` из другого файла, из [`CLAUDE_CODE_DISABLE_ARTIFACT`](https://code.claude.com/docs/ru/env-vars) или из [параметра администратора](https://code.claude.com/docs/ru/artifacts.md#manage-artifacts-for-your-organization) вашей организации
* **Default**: не установлено, поэтому инструмент следует [доступности](https://code.claude.com/docs/ru/artifacts.md#availability) вашей учётной записи

```json settings.json theme={null}
{
  "enableArtifact": false
}
```

Пока источник, отличный от ваших собственных пользовательских настроек, держит инструмент отключённым, Claude Code скрывает строку **Artifacts** в `/config`, потому что включение её там не изменит ничего. [Disable artifacts](https://code.claude.com/docs/ru/artifacts.md#disable-artifacts) перечисляет все способы отключения инструмента.

### `inputNeededNotifEnabled`

Получать push-уведомление на ваш телефон, когда запрос разрешения или вопрос ожидает вашего ввода. В локальной сессии Claude Code отправляет эти уведомления, только пока подключён [Remote Control](https://code.claude.com/docs/ru/remote-control.md). Отображается в `/config` как **Push when actions required**.

* **Scope**: [`Any file`](#scopes). Claude Code также читает значение, оставленное в `~/.claude.json` старыми версиями.
* **Type**: Boolean
* **Default**: `false`

```json settings.json theme={null}
{
  "inputNeededNotifEnabled": true
}
```

Одного этого ключа недостаточно, чтобы получать уведомления. Чтобы настроить их, выполните шаги из раздела [Mobile push notifications](https://code.claude.com/docs/ru/remote-control.md#mobile-push-notifications).

### `preferredNotifChannel`

Выберите, как Claude Code уведомляет вас, когда задача завершена или ожидает запрос разрешения. [Уведомления мода](https://code.claude.com/docs/ru/plugins/mods/api.md#show-something-without-starting-a-turn) используют ту же настройку. Отображается в `/config` как **Local notifications**.

* **Scope**: [`Any file`](#scopes). Claude Code также читает значение, оставленное в `~/.claude.json` старыми версиями.
* **Type**: строка, одна из:
  * `"auto"`: Claude Code отправляет уведомление рабочего стола, когда обнаруживает iTerm2, Ghostty или Kitty, звонит в колокол в Terminal.app только когда его звуковой колокол отключён, и ничего не делает в других местах
  * `"terminal_bell"`: Claude Code звонит в символ колокола в любом терминале
  * `"iterm2"`: Claude Code отправляет уведомление рабочего стола iTerm2
  * `"iterm2_with_bell"`: Claude Code отправляет уведомление рабочего стола iTerm2 и звонит в колокол
  * `"kitty"`: Claude Code отправляет уведомление рабочего стола Kitty
  * `"ghostty"`: Claude Code отправляет уведомление рабочего стола Ghostty
  * `"notifications_disabled"`: Claude Code не отправляет уведомление
* **Default**: `"auto"`

```json settings.json theme={null}
{
  "preferredNotifChannel": "terminal_bell"
}
```

С `"auto"` Claude Code отправляет уведомление рабочего стола, когда обнаруживает iTerm2, Ghostty или Kitty. В Terminal.app он звонит в символ колокола только когда вы отключили звуковой колокол Terminal, и в других терминалах ничего не делает. Установите `"terminal_bell"`, чтобы звонить в символ колокола в любом терминале. См. [Get a terminal bell or notification](https://code.claude.com/docs/ru/terminal-config.md#get-a-terminal-bell-or-notification).

### `remote.defaultEnvironmentId`

Выберите [облачное окружение](https://code.claude.com/docs/ru/cloud-environments.md) по умолчанию для облачных сеансов, которые вы создаёте из CLI, например с `claude --cloud`. Claude Code записывает этот ключ в ваши пользовательские настройки, когда вы выбираете окружение с помощью [`/remote-env`](https://code.claude.com/docs/ru/cloud-environments#select-an-environment-from-the-cli).

* **Scope**: [`Any file`](#scopes). Для ID самостоятельно размещённого окружения, пользовательских или управляемых настроек, или флага `--settings` только.
* **Type**: строка, ID окружения, такой как `env_...` или `ccpool_...`
* **Default**: не установлено, поэтому Claude Code использует размещённое Anthropic окружение, когда ваш список имеет одно, и в противном случае первое окружение в вашем списке, которое не является [окружением моста Удалённого управления](https://code.claude.com/docs/ru/cloud-environments.md#the-default-environment), или первое окружение, когда каждое является окружением моста
* **Per-session overrides**: `--environment` имеет приоритет над этим ключом для одного облачного сеанса, который он создаёт

```json settings.json theme={null}
{
  "remote": {
    "defaultEnvironmentId": "env_0123abcd"
  }
}
```

ID размещённого Anthropic окружения, который начинается с `env_`, следует стандартному приоритету настроек, поэтому значение в проектных настройках репозитория переопределяет ваш выбор на уровне пользователя. ID [самостоятельно размещённого окружения](https://code.claude.com/docs/ru/self-hosted-environments), который начинается с `ccpool_`, учитывается только из пользовательских настроек, управляемых настроек и флага `--settings`; Claude Code игнорирует один в проектных или локальных настройках репозитория, и `/remote-env` показывает, какое значение он игнорировал, поэтому проверенный файл не может направить сеансы на самостоятельно размещённое окружение, которое вы не выбрали.

### `remoteControlAtStartup`

Подключить [Удалённое управление](https://code.claude.com/docs/ru/remote-control.md) автоматически, когда начинается каждый интерактивный сеанс, вместо ожидания `/remote-control`. Установите значение `true`, чтобы включить автоподключение, `false`, чтобы отключить его. Отображается в `/config` как **Enable Remote Control for all sessions**.

* **Scope**: [`Any file`](#scopes). Claude Code также читает значение, оставленное в `~/.claude.json` старыми версиями.
* **Type**: Boolean
  * `true`: Claude Code подключает Удалённое управление автоматически, когда начинается каждый интерактивный сеанс
  * `false`: Claude Code ждёт `/remote-control`
* **Default**: не установлено, поэтому применяется [автоподключение по умолчанию](https://code.claude.com/docs/ru/remote-control.md#enable-remote-control-for-all-sessions)
* **Per-session overrides**: `--remote-control` включает Удалённое управление для одного сеанса даже когда этот ключ `false`, и ни один флаг не отключает его для одного сеанса

```json settings.json theme={null}
{
  "remoteControlAtStartup": true
}
```

Claude Code игнорирует `true` из проектных или локальных настроек, поэтому репозиторий может отключить автоподключение для его checkout, но не может включить его. Для полного поведения для каждой области видимости см. [Enable Remote Control for all sessions](https://code.claude.com/docs/ru/remote-control.md#enable-remote-control-for-all-sessions) и [ключи безопасности, где применяется более строгое значение](https://code.claude.com/docs/ru/settings.md#security-keys-where-the-stricter-value-applies).

### `sshConfigs`

Добавить SSH-соединения в список выбора окружения [Desktop](https://code.claude.com/docs/ru/desktop.md#pre-configure-ssh-connections-for-your-team). Администраторы используют `sshConfigs` для распространения общих соединений в команде. Пользователи могут выбрать управляемое соединение и [задать для него собственную **Worktree folder**](https://code.claude.com/docs/ru/desktop.md#set-the-worktree-folder-on-an-existing-connection). Изменять другие его поля или удалять его в приложении они не могут.

* **Scope**: [`User or managed`](#scopes). Настольное приложение читает этот ключ. По умолчанию оно читает управляемые соединения из [одного управляемого источника](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources).
* **Type**: массив объектов, каждый с обязательными `id`, `name` и `sshHost` и опциональными `sshPort` и `sshIdentityFile`
* **Default**: не установлено

Этот пример добавляет одно соединение с именем `Dev VM`, которое подключается к `user@dev.example.com`:

```json settings.json theme={null}
{
  "sshConfigs": [
    {
      "id": "dev-vm",
      "name": "Dev VM",
      "sshHost": "user@dev.example.com"
    }
  ]
}
```

### `sshHostAllowlist`

Ограничить хосты, к которым может подключиться [SSH-сеанс Desktop](https://code.claude.com/docs/ru/desktop.md#restrict-which-ssh-hosts-users-can-connect-to). Только приложение Desktop читает этот ключ; CLI не читает. Шаблоны нечувствительны к регистру: `*` соответствует любому хосту, `*.example.com` соответствует `example.com` и каждому поддомену, и всё остальное является точным совпадением с именем хоста после разрешения `~/.ssh/config`. Пустой массив отключает SSH-сеансы.

В Claude Desktop v3.1623.0 или новее [промежуточные хосты (jump hosts)](https://code.claude.com/docs/ru/desktop.md#allow-jump-hosts) сессии также должны соответствовать шаблону.

* **Scope**: [`Managed`](#scopes). По умолчанию Desktop читает ключ из [одного управляемого источника](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources).
* **Type**: массив шаблонов имён хостов
* **Default**: не установлено, поэтому разрешены любые хосты

Этот пример разрешает `devboxes.example.com` и его поддомены, плюс точный хост `bastion.example.com`:

```json managed-settings.json theme={null}
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

Значение, которое Desktop не может прочитать как список хостов, например `true` или объект, считается пустым массивом, пока вы его не исправите, за исключением `null`, который считается неустановленным значением. Требуется Claude Desktop v2.26454.0 или позже.

Если вы установите [`managedSourcesBehavior`](#managedsourcesbehavior) в `"merge"` в источнике с наивысшим приоритетом, Desktop объединяет списки из всех [источников администратора](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources) и разрешает хост, который соответствует любому из них. Если вы установите пустой массив в одном источнике, SSH-сессии остаются включёнными для хостов, перечисленных в другом источнике.

### `sshHostCommands`

Добавить в список выбора окружения [Desktop](https://code.claude.com/docs/ru/desktop.md#create-an-ssh-connection-from-a-command) SSH-соединения, хост которых определяется командой. Когда вы создаёте соединение или создаёте для него ещё одну машину, Desktop запускает команду этой записи на вашем компьютере и подключается к хосту, который выводит команда.

Требуется Claude Desktop v3.6556.0 или новее на macOS или Linux либо v4.16336.0 или новее на Windows, с входом в учётную запись Claude. На Windows Desktop также должен [подключаться через клиент OpenSSH](https://code.claude.com/docs/ru/desktop.md#use-your-ssh-configuration).

* **Scope**: [`User or managed`](#scopes). Только настольное приложение читает этот ключ. Управляемые записи оно читает из [одного файла управляемых настроек или политики MDM](https://code.claude.com/docs/ru/desktop.md#distribute-commands-to-your-team) на компьютере и игнорирует этот ключ в [управляемых сервером настройках](https://code.claude.com/docs/ru/server-managed-settings.md).
* **Type**: массив объектов, каждый с обязательными `id`, `name` и `command` и опциональными `sshIdentityFile` и `startDirectory`. Desktop не интерпретирует `command` как синтаксис оболочки, поэтому конвейеры и переменные не работают: [записывайте её как программу и её аргументы](https://code.claude.com/docs/ru/desktop.md#write-the-command).
* **Default**: не установлено

Этот пример добавляет одно соединение с именем `Dev box`, где `acme-dev create` обозначает ваш собственный инструмент:

```json settings.json theme={null}
{
  "sshHostCommands": [
    {
      "id": "devbox",
      "name": "Dev box",
      "command": "acme-dev create"
    }
  ]
}
```

На Windows простое имя, такое как `acme-dev`, не работает, поэтому [начинайте команду с полного пути к программе](https://code.claude.com/docs/ru/desktop.md#write-the-command-on-windows).

До Claude Code v2.1.307 инструмент Edit отклонял изменение, добавлявшее этот ключ в корректный файл настроек, с ошибкой `Unrecognized field: sshHostCommands`. В этих версиях добавьте ключ в текстовом редакторе; Claude Code загружает файл, содержащий этот ключ. В Desktop учитывается [версия Claude Code на вкладке Code](https://code.claude.com/docs/ru/desktop.md#claude-code-version-in-the-code-tab), а не версия в вашем терминале.

## Аутентификация и поставщики

Предоставляйте учётные данные через вспомогательные скрипты и, для организаций, принудительно установите метод входа или организацию. См. [Аутентификация](https://code.claude.com/docs/ru/authentication.md).

### `allowedProviders`

Перечислите сервисы, через которые машина может обращаться к Claude, такие как Anthropic API, Amazon Bedrock или LLM-шлюз. Сессия на поставщике, который не указан в списке, отклоняется при запуске, при входе и когда она в следующий раз обращается к API, поэтому переключение на неуказанного поставщика во время сессии также отклоняется. [Сообщение об отказе](https://code.claude.com/docs/ru/errors.md#managed-settings-dont-allow-this-api-provider) указывает, что выбрало поставщика и какие шаги предпринять для продолжения. Требуется Claude Code v2.1.285 или позже.

* **Scope**: [`Managed`](#scopes). Список, который устанавливают собственные источники администратора машины, политики MDM и файлы управляемых настроек, продолжает применяться, когда управляемые сервером настройки также предоставляют свой: сессия может тогда использовать только поставщиков из обоих списков, поэтому управляемый сервером список может сузить то, что разрешает машина, но никогда не расширить это. Какой из источников машины с `allowedProviders` учитывается, определяется тем, [как Claude Code объединяет управляемые источники](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources). Список, доставленный только через управляемые сервером настройки, достигает только тех сессий, которые [получают управляемые сервером настройки](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability).
* **Type**: массив строк, каждая из которых — одно из следующих значений:
  * `"anthropic"`: Anthropic API на собственном хосте Anthropic, через вход claude.ai или Console или API-ключ. Объедините это с [`forceLoginMethod`](#forceloginmethod) или [`forceLoginOrgUUID`](#forceloginorguuid), чтобы также ограничить вход. Cowork в Desktop [на машине пользователя](https://code.claude.com/docs/ru/managed-settings.md#where-and-when-a-policy-applies) считается `"anthropic"`, когда выполнен вход в claude.ai, поэтому без этого значения в списке машины Cowork [отклоняется при запуске](https://code.claude.com/docs/ru/errors.md#managed-settings-dont-allow-this-api-provider). Чтобы Cowork мог запускаться, добавьте это значение, что также открывает этот список для прямых сессий Anthropic.
  * `"bedrock"`: [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md)
  * `"vertex"`: [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md), ранее Vertex AI
  * `"foundry"`: [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md)
  * `"anthropicAws"`: [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md)
  * `"anthropicGoogleCloud"`: [Claude Models on Google Cloud (Anthropic managed)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md)
  * `"mantle"`: [эндпоинт Mantle](https://code.claude.com/docs/ru/amazon-bedrock.md#use-the-mantle-endpoint) Amazon Bedrock. Сессия, которая [запускает Mantle вместе с Invoke API](https://code.claude.com/docs/ru/amazon-bedrock.md#run-mantle-alongside-the-invoke-api), использует обоих поставщиков, поэтому перечислите для неё `"bedrock"` и `"mantle"` вместе
  * `"customEndpoint"`: Anthropic API или API облачного поставщика, отправляемые на другой хост, например [LLM-шлюз](https://code.claude.com/docs/ru/llm-gateway), указанный в `ANTHROPIC_BASE_URL` или в переменной эндпоинта поставщика, такой как `ANTHROPIC_BEDROCK_BASE_URL`. Claude Code допускает это только для точного значения, которое закрепляет управляемый блок [`env`](#env)
  * `"gateway"`: вход через [Cloud gateway](https://code.claude.com/docs/ru/claude-apps-gateway)
* **Default**: не установлено, поэтому можно использовать любого поставщика

```json managed-settings.json theme={null}
{
  "allowedProviders": ["anthropic", "bedrock"]
}
```

Запись каждого облачного поставщика означает собственный сервис этого поставщика, включая его региональные, FIPS и приватные эндпоинты.

Запись, которую Claude Code не распознаёт как имя поставщика, отбрасывается с уведомлением, а остальная часть списка остаётся в силе. С пустым списком или списком, каждая запись которого не распознана, Claude Code отклоняет всех поставщиков и не запускается на машине.

#### Эндпоинты, которым нужен pin в управляемом `env`

Pin — это значение переменной эндпоинта, установленное в управляемом блоке [`env`](#env). Когда сессия отправляет трафик поставщика куда-то, кроме собственного сервиса этого поставщика, Claude Code допускает это, только если значение сессии совпадает с pin. Pin нужен следующим эндпоинтам:

* **Сессии `"customEndpoint"`**: переменная, которая указывает хост, например `ANTHROPIC_BASE_URL`
* **Amazon Bedrock**: переменные AWS SDK `AWS_ENDPOINT_URL`, `AWS_ENDPOINT_URL_BEDROCK` и `AWS_ENDPOINT_URL_BEDROCK_RUNTIME`, когда они указывают за пределы собственного сервиса Bedrock. Сессия остаётся под `"bedrock"`, а не `"customEndpoint"`
* **URL входа через шлюз**: сессия остаётся под `"gateway"`, и [`forceLoginGatewayUrl`](#forcelogingatewayurl) также считается pin

Какие блоки `env` считаются pin, зависит от того, где установлен список:

* **Источник администратора на машине устанавливает список**: учитываются только блоки `env` собственных источников администратора машины
* **Список устанавливают только управляемые сервером настройки**: значение `env` в этих управляемых сервером настройках также учитывается

Список не оценивает переменные учётных данных и арендатора облачного поставщика или сетевой путь, такие как `HTTPS_PROXY` и настройки сертификатов. Установите их для всего парка машин в управляемом блоке `env`.

### `apiKeyHelper`

Запустите собственную команду для создания учётных данных, которые Claude Code отправляет с запросами к модели. Claude Code запускает команду через системную оболочку, `/bin/sh` на macOS и Linux и `cmd` на Windows, и отправляет её вывод как в заголовке `X-Api-Key`, так и в `Authorization: Bearer`. Используйте это для динамических или ротируемых учётных данных, таких как краткосрочные токены, полученные из хранилища.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, командная строка оболочки
* **Default**: не установлено, поэтому Claude Code не запускает помощник

```json settings.json theme={null}
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}
```

Claude Code кэширует значение и повторно запускает команду в следующих случаях:

* После истечения времени жизни кэша, пять минут по умолчанию или интервал, который вы установили с помощью [`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`](https://code.claude.com/docs/ru/env-vars).
* Когда запрос к API Anthropic, напрямую или через [LLM-шлюз](https://code.claude.com/docs/ru/llm-gateway), завершается с ошибкой `401` или `403`.
* Когда запрос через LLM-шлюз завершается с ошибкой `401`, но не `403`, и вы установили [`CLAUDE_CODE_SKIP_VERTEX_AUTH`](https://code.claude.com/docs/ru/env-vars) для Google Cloud's Agent Platform, `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` для Claude Platform on AWS или `CLAUDE_CODE_SKIP_MANTLE_AUTH` для Amazon Bedrock Mantle. Требуется Claude Code v2.1.318 или позже.
* Перед отправкой запроса к API Anthropic, напрямую или через LLM-шлюз, когда кэшированный вывод — это JWT, который истёк после того, как помощник его создал. Требуется Claude Code v2.1.246 или позже.

Последние три случая применяются, только когда вывод помощника — это учётные данные, которые отправляет Claude Code, и `ANTHROPIC_AUTH_TOKEN` не установлен.

В интерактивных сессиях, когда команда поступает из настроек проекта или локальных настроек, Claude Code не запускает её до тех пор, пока вы не примете запрос доверия к рабочему пространству. См. [Управление учётными данными](https://code.claude.com/docs/ru/authentication.md#credential-management).

### `awsAuthRefresh`

Запустите собственную команду, такую как `aws sso login`, для обновления учётных данных в вашем каталоге `.aws`, когда те, которые есть у Claude Code для [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), перестают работать. Claude Code сначала проверяет текущие учётные данные через STS и запускает команду, только когда эта проверка не проходит, затем читает обновлённый каталог `.aws`.

Когда проверка одновременно не проходит в нескольких процессах Claude Code, использующих одну и ту же команду и учётные данные, например в отдельных терминалах или окнах IDE, один процесс запускает команду, а остальные ждут результата этого запуска, не запуская команду сами. Процесс, который прождал 60 секунд с ожидающим запросом, запускает команду сам. Чтобы отключить это, установите [`CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK`](https://code.claude.com/docs/ru/env-vars) в `1`.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, командная строка оболочки
* **Default**: не установлено, поэтому Claude Code не обновляет учётные данные AWS за вас

```json settings.json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile"
}
```

Используйте этот ключ, когда ваш процесс обновления записывает в `.aws`; используйте [`awsCredentialExport`](#awscredentialexport), когда он вместо этого выводит учётные данные. См. [расширенную конфигурацию учётных данных](https://code.claude.com/docs/ru/amazon-bedrock.md#advanced-credential-configuration).

### `awsCredentialExport`

Запустите собственную команду, которая выводит учётные данные AWS в формате JSON, чтобы Claude Code мог вызывать [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md) с учётными данными, которые не находятся в вашем каталоге `.aws`. Claude Code принимает форму вывода `aws sts` и плоскую форму `aws configure export-credentials` и ограничивает учётные данные своим собственным клиентом Bedrock, поэтому команды оболочки, которые запускает Claude, по-прежнему видят ваши окружающие учётные данные.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, командная строка оболочки
* **Default**: не установлено, поэтому Claude Code использует окружающую цепочку учётных данных AWS

```json settings.json theme={null}
{
  "awsCredentialExport": "/bin/generate_aws_grant.sh"
}
```

В отличие от [`awsAuthRefresh`](#awsauthrefresh), Claude Code всегда запускает эту команду, когда она установлена, без предварительной проверки окружающих учётных данных. См. [расширенную конфигурацию учётных данных](https://code.claude.com/docs/ru/amazon-bedrock.md#advanced-credential-configuration).

### `forceLoginMethod`

Ограничьте, с каким типом учётной записи люди могут входить: `"claudeai"` для входа через claude.ai или `"console"` для входа через Claude Console. Установите `"gateway"`, чтобы направлять людей на [облачный шлюз](https://code.claude.com/docs/ru/claude-apps-gateway) вместо входа первой стороны. Администраторы устанавливают это в управляемых настройках и сочетают с [`forceLoginOrgUUID`](#forceloginorguuid), чтобы входы разработчиков в claude.ai оставались внутри одной организации.

Если вы установите значение `"claudeai"` в любом файле настроек, Claude Code также перестаёт предлагать [вход в Console без ключа](https://code.claude.com/docs/ru/authentication.md#sign-in-without-an-api-key) в сессиях, к которым применяется этот файл. Если установлено только `"console"`, люди по-прежнему могут перейти ко входу без ключа после неудачной попытки входа. Чтобы Claude Code перестал его предлагать, см. [Прекращение предложения входа без ключа на управляемых машинах](https://code.claude.com/docs/ru/authentication.md#stop-offering-the-keyless-sign-in-on-managed-machines), где также перечислено, что ещё изменяет `forceLoginOrgUUID`.

* **Scope**: [`Any file`](#scopes). Claude Code учитывает `"gateway"` из тех же источников, что и [`forceLoginGatewayUrl`](#forcelogingatewayurl), и рассматривает его как неустановленное значение во всех остальных.
* **Type**: строка, одно из значений:
  * `"claudeai"`: вход через claude.ai
  * `"console"`: вход через Claude Console
  * `"gateway"`: Claude Code направляет людей на облачный шлюз вместо входа первой стороны
* **Default**: не установлено, поэтому люди выбирают метод входа сами

```json settings.json theme={null}
{
  "forceLoginMethod": "claudeai"
}
```

Каждый путь входа первой стороны применяет ограничение, включая [расширение VS Code](https://code.claude.com/docs/ru/vs-code.md), Agent SDK, `claude setup-token` и `/install-github-app`, за исключением интерактивного экрана входа в терминале, доступного через `/login` или первоначальную настройку, который предварительно выбирает метод без его принудительного применения. До v2.1.212 ограничение применялось только при входе через терминал. См. [Ограничить вход вашей организацией](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization), чтобы узнать, как обрабатываются каждый путь входа, учётные данные окружения и сторонние поставщики.

Когда управляемый источник на машине устанавливает `"gateway"`, Claude Code не использует оставшийся вход, API-ключ или учётные данные `apiKeyHelper`. См. [Политика администратора требует вход через облачный шлюз](https://code.claude.com/docs/ru/errors.md#administrator-policy-requires-a-cloud-gateway-sign-in), чтобы узнать, какое сообщение выдаёт каждый из них. Если вы выбираете облачного поставщика через `CLAUDE_CODE_USE_BEDROCK` или аналогичную переменную окружения, сессии не требуется вход через шлюз. До v2.1.261 Claude Code использовал оставшийся вход на таких машинах.

### `forceLoginGatewayUrl`

Установите URL шлюза, к которому подключается экран облачного шлюза `/login`, чтобы люди попадали на ваш [облачный шлюз](https://code.claude.com/docs/ru/claude-apps-gateway) без ввода его адреса. На экране нет поля URL: если этот ключ установлен, экран показывает URL вашего шлюза и подключается, когда человек нажимает Enter; без него экран предлагает обратиться к IT-администратору.

В управляемых настройках либо этот ключ, либо `forceLoginMethod: "gateway"` делает машину доступной только через шлюз, за исключением сессий, которые выбирают облачного поставщика с помощью `CLAUDE_CODE_USE_*`. Тогда `/login` открывается на экране облачного шлюза без выбора метода входа. См. [Политика администратора требует вход через облачный шлюз](https://code.claude.com/docs/ru/errors.md#administrator-policy-requires-a-cloud-gateway-sign-in), чтобы узнать, что происходит с оставшимся входом первой стороны или API-ключом. Установите оба ключа, чтобы экран подключался, а не показывал ошибку.

* **Scope**: [`User or managed`](#scopes). Читается из управляемого источника на машине: `managed-settings.json`, plist macOS или реестра Windows HKLM, или помощника политики. На машине, где нет ни одного из них, Claude Code v2.1.295 или позже также читает его из [пользовательских настроек](https://code.claude.com/docs/ru/claude-apps-gateway#set-the-gateway-url-in-user-settings). Claude Code игнорирует его в HKCU и управляемых сервером настройках.
* **Type**: строка, полный URL, включая схему
* **Default**: не установлено, поэтому экран облачного шлюза показывает ошибку с предложением обратиться к IT-администратору

```json managed-settings.json theme={null}
{
  "forceLoginGatewayUrl": "https://claude-gateway.example.com"
}
```

Если значение не является действительным URL, экран входа сообщает об этом, а остальная часть файла управляемых настроек по-прежнему применяется. См. [Установить URL шлюза](https://code.claude.com/docs/ru/claude-apps-gateway#set-the-gateway-url).

### `forceLoginOrgUUID`

Из управляемого источника требуйте, чтобы входы с учётной записью claude.ai принадлежали одной организации Anthropic, указанной как один UUID, или любой из нескольких организаций, указанных как массив. Из любого файла настроек Claude Code также использует один UUID для предварительного выбора этой организации во время входа в claude.ai или Claude Console и ничего не выбирает предварительно для массива. Если вы установите ключ в любом файле настроек, Claude Code также перестаёт предлагать [вход в Console без ключа](https://code.claude.com/docs/ru/authentication.md#sign-in-without-an-api-key) в сессиях, к которым применяется этот файл, и вместо этого создаёт API-ключ.

* **Scope**: [`Any file`](#scopes). В файле настроек, который не является управляемым источником, Claude Code не проверяет, к какой организации относится вход, а один UUID предварительно выбирает организацию во время входа.
* **Type**: строка, один UUID, или массив строк, несколько UUID
* **Default**: не установлено, поэтому может входить любая организация

Этот пример принимает входы из любой из двух организаций без предварительного выбора одной из них:

```json managed-settings.json theme={null}
{
  "forceLoginOrgUUID": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]
}
```

Если управляемый источник устанавливает пустой массив или значение, которое не является строкой или массивом строк, пользователи, входящие с учётной записью Anthropic, не могут запустить Claude Code или завершить вход. Они видят сообщение, в котором указан `forceLoginOrgUUID` и предлагается обратиться к администратору. [`policyHelper`](#policyhelper), который выдаёт значение неправильного типа, вместо этого [завершает свой запуск с ошибкой](#helper-failures).

См. [Ограничить вход вашей организацией](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization), чтобы узнать, как Claude Code обрабатывает входы в Claude Console, другие пути входа и учётные данные окружения.

### `gatewayInternalNetworks`

Объявите публичные блоки IPv4, из которых ваша организация нумерует свою внутреннюю сеть, чтобы `/login` принимал [облачный шлюз](https://code.claude.com/docs/ru/claude-apps-gateway) в них. Требуется Claude Code v2.1.268 или позже.

Без этого ключа `/login` подключается к любому шлюзу на приватном адресе и больше ни к чему. С ним `/login` также принимает шлюз внутри указанного блока, только через прямое соединение. Собственный адрес машины в этом соединении также должен находиться внутри того же блока.

* **Scope**: [`Managed`](#scopes). Читается только из источника на машине: `managed-settings.json`, plist macOS или реестра Windows HKLM, или помощника политики. Claude Code игнорирует его в HKCU и управляемых сервером настройках.
* **Type**: массив строк, не более четырёх блоков IPv4 CIDR, каждый от `/8` до `/32`, не пересекающихся друг с другом и ни один из которых не пересекается с приватным пространством.
* **Default**: не установлено, поэтому `/login` принимает только шлюзы на приватных адресах

```json managed-settings.json theme={null}
{
  "gatewayInternalNetworks": ["203.0.113.0/24"]
}
```

Замените диапазон для документации в примере на ваш собственный блок. Claude Code отклоняет диапазоны для документации, диапазоны, которые локально используют клиенты VPN и NAT64, и зарезервированное пространство, из которого не нумеруется ни одна сеть, например многоадресное.

Если запись недействительна или значение не является списком строк, `/login` называет проблему и отклоняет любой новый вход через шлюз на машине до тех пор, пока вы не исправите значение. Существующие входы продолжают работать. См. [Разрешить шлюз в принадлежащем вам публичном адресном пространстве](https://code.claude.com/docs/ru/claude-apps-gateway#allow-a-gateway-on-public-address-space-you-own), чтобы узнать полные правила и то, что видят разработчики.

### `gcpAuthRefresh`

Запустите собственную команду для обновления Google Cloud Application Default Credentials, когда Claude Code обнаруживает, что они истекли или не могут быть загружены, чтобы запросы к [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md) продолжали работать без повторной аутентификации вручную.

Когда несколько процессов Claude Code, использующих одну и ту же команду и учётные данные, например в отдельных терминалах или окнах IDE, одновременно обнаруживают, что учётные данные истекли, один процесс запускает команду, а остальные ждут результата этого запуска, не запуская команду сами. Процесс, который прождал 60 секунд с ожидающим запросом, запускает команду сам. Чтобы отключить это, установите [`CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK`](https://code.claude.com/docs/ru/env-vars) в `1`.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, командная строка оболочки
* **Default**: не установлено, поэтому ошибка учётных данных Claude Code предлагает вам самостоятельно выполнить `gcloud auth application-default login`

```json settings.json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login"
}
```

См. [расширенную конфигурацию учётных данных](https://code.claude.com/docs/ru/google-vertex-ai.md#advanced-credential-configuration).

### `otelHeadersHelper`

Запустите собственную команду для создания заголовков, которые Claude Code отправляет с экспортами OpenTelemetry, для бэкендов с ротируемыми токенами. Claude Code запускает её при старте и затем периодически и ожидает в stdout объект JSON со строковыми значениями заголовков.

* **Scope**: [`Any file`](#scopes)
* **Type**: строка, путь к исполняемому файлу или командная строка оболочки
* **Default**: не установлено, поэтому Claude Code не добавляет заголовки, созданные помощником

```json settings.json theme={null}
{
  "otelHeadersHelper": "/bin/generate_otel_headers.sh"
}
```

Установите интервал обновления с помощью [`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`](https://code.claude.com/docs/ru/env-vars). См. [Динамические заголовки](https://code.claude.com/docs/ru/monitoring-usage.md#dynamic-headers), чтобы узнать требования к скрипту и что происходит, когда помощник завершается с ошибкой.

## Обновления и версионирование

Выберите канал обновления и, для организаций, закрепите версии, которые люди могут запускать. См. [Обновление Claude Code](https://code.claude.com/docs/ru/setup.md#update-claude-code).

### `autoUpdatesChannel`

Выберите, какой [канал выпуска](https://code.claude.com/docs/ru/setup.md#configure-release-channel) следуют фоновые автоматические обновления и `claude update`. Установите `"stable"` для версии, которая обычно имеет возраст около одной недели и пропускает выпуски с серьёзными регрессиями, или `"latest"` для самого последнего выпуска.

* **Область действия**: [`Any file`](#scopes). Установите это в управляемых параметрах, чтобы применить один канал во всей организации.
* **Тип**: строка, одно из:
  * `"latest"`: обновления следуют самому последнему выпуску
  * `"stable"`: обновления следуют версии, которая обычно имеет возраст около одной недели и пропускает выпуски с серьёзными регрессиями
* **По умолчанию**: не установлено, поэтому Claude Code следует `"latest"`

```json settings.json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Claude Code записывает `"stable"` в ваши пользовательские параметры, когда вы выбираете это в разделе **Auto-update channel** в `/config`, и удаляет ключ, когда вы переключаетесь обратно на latest там. `claude install stable` и `claude install latest` также сохраняют выбранный вами канал. Переключение с `"latest"` на `"stable"` в `/config` спрашивает, разрешить ли понижение версии или остаться на текущей версии; остаток устанавливает [`minimumVersion`](#minimumversion). Установки Homebrew игнорируют этот ключ: пакет `claude-code` отслеживает stable, а `claude-code@latest` отслеживает latest, и `claude update` полагается на `brew upgrade`. Чтобы полностью отключить автоматические обновления, установите [`DISABLE_AUTOUPDATER`](https://code.claude.com/docs/ru/setup#disable-auto-updates) в `env`.

### `minimumVersion`

Не позволяйте фоновым автоматическим обновлениям и `claude update` устанавливать какую-либо версию ниже заданной вами. Claude Code записывает этот ключ за вас, когда вы решаете остаться на текущей версии при переключении каналов в `/config`. Claude Code очищает ключ, когда вы переключаетесь обратно на `"latest"` в `/config`.

* **Область действия**: [`Any file`](#scopes). Установите этот ключ в управляемых настройках, чтобы закрепить минимум на уровне организации, который пользовательские и проектные настройки не могут переопределить.
* **Тип**: строка, номер версии, такой как `"2.1.323"`; значение, которое не является допустимой версией, игнорируется
* **По умолчанию**: не установлено, поэтому обновления могут установить любую версию, которую предлагает канал

Этот пример следует стабильному каналу и отказывается устанавливать любую версию ниже 2.1.323:

```json settings.json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.323"
}
```

Этот ключ только ограничивает обновления. Чтобы заставить Claude Code отказаться запускаться ниже версии, используйте вместо этого [`requiredMinimumVersion`](#requiredminimumversion). См. [Закрепить минимальную версию](https://code.claude.com/docs/ru/setup.md#pin-a-minimum-version).

### `requiredMaximumVersion`

Установите самую новую версию Claude Code, которую разрешает запускать ваша организация. Когда запущенная версия новее, Claude Code выходит при запуске и сообщает пользователю установить одобренную версию через утверждённый вашей организацией метод; `claude install <version>` также может работать. Требует Claude Code v2.1.163 или позже.

* **Область действия**: [`Managed`](#scopes). Claude Code не выдаёт предупреждение, когда игнорирует ключ в других местах.
* **Тип**: строка, номер версии, такой как `"2.1.150"`; значение, которое не является допустимой версией, игнорируется
* **По умолчанию**: не установлено, поэтому потолок не применяется

```json managed-settings.json theme={null}
{
  "requiredMaximumVersion": "2.1.150"
}
```

В нативных установках и установках через npm фоновые автоматические обновления и `claude update` пропускают версии выше потолка. `claude update`, `claude install` и `claude doctor` продолжают работать выше потолка, чтобы пользователи могли восстановиться. Объедините это с [`requiredMinimumVersion`](#requiredminimumversion), чтобы применить диапазон.

Когда обновляется приложение для рабочего стола, его собственная копия Claude Code может оказаться новее потолка, и тогда [локальные сессии на вкладке Code не запускаются](https://code.claude.com/docs/ru/desktop.md#version-above-your-organizations-limit). Чтобы эта копия не менялась в macOS и Windows, [отключите автоматические обновления приложения для рабочего стола](https://code.claude.com/docs/ru/desktop.md#device-management-policies). Microsoft Store по-прежнему обновляет установку, выполненную из него.

### `requiredMinimumVersion`

Установите самую старую версию Claude Code, которую разрешает запускать ваша организация. Когда запущенная версия старше, Claude Code выходит при запуске и сообщает пользователю обновиться через утверждённый вашей организацией метод. Проверка выполняется только при запуске, поэтому уже запущенный сеанс продолжает работу. Требует Claude Code v2.1.163 или позже.

* **Область действия**: [`Managed`](#scopes). Claude Code не выдаёт предупреждение, когда игнорирует ключ в других местах.
* **Тип**: строка, номер версии, такой как `"2.1.150"`; значение, которое не является допустимой версией, игнорируется
* **По умолчанию**: не установлено, поэтому пол не применяется

```json managed-settings.json theme={null}
{
  "requiredMinimumVersion": "2.1.150"
}
```

`claude update`, `claude install` и `claude doctor` продолжают работать ниже пола, чтобы пользователи могли восстановиться. В отличие от [`minimumVersion`](#minimumversion), который только предотвращает понижение версии, этот ключ блокирует запуск. Объедините это с [`requiredMaximumVersion`](#requiredmaximumversion), чтобы применить диапазон.

## Tools

Отключите определённые инструменты в [приложении Claude Code для рабочего стола](https://code.claude.com/docs/ru/desktop.md). Терминальный CLI игнорирует эти ключи. Для самих инструментов см. [Инструменты, доступные Claude](https://code.claude.com/docs/ru/tools-reference.md).

### `browserExternalPageTools`

Запретите Claude использовать свои инструменты для чтения или действия на внешних страницах в [панели Browser](https://code.claude.com/docs/ru/desktop.md#browse-external-sites) приложения для рабочего стола. Люди в вашей организации по-прежнему могут открывать внешние сайты самостоятельно, а локальные предпросмотры dev-сервера продолжают работать с инструментами Claude. Приложение для рабочего стола читает этот ключ; терминальный CLI игнорирует его.

* **Scope**: [`Managed`](#scopes)
* **Type**: string, `"disabled"`; приложение для рабочего стола также принимает `"disable"`, в любом случае
* **Default**: не установлено, поэтому инструменты Claude работают на внешних страницах

```json managed-settings.json theme={null}
{
  "browserExternalPageTools": "disabled"
}
```

Любое другое значение оставляет инструменты Claude включёнными, и непустая строка, которая не является одним из двух принятых значений, регистрирует предупреждение. Чтобы заблокировать внешние сайты для людей и Claude одновременно, установите [`disableBrowserExternalNavigation`](#disablebrowserexternalnavigation) вместо этого. См. [Ограничить внешний просмотр для вашей организации](https://code.claude.com/docs/ru/desktop.md#restrict-external-browsing-for-your-organization).

### `disableBrowserExternalNavigation`

Отключите внешний просмотр в [панели Browser](https://code.claude.com/docs/ru/desktop.md#browse-external-sites) приложения для рабочего стола для людей и Claude одновременно. Предпросмотры localhost dev-сервера продолжают работать. HTML-предпросмотры в сессиях SSH и WSL по-прежнему открываются, но в них [не выполняются скрипты](https://code.claude.com/docs/ru/desktop.md#turn-off-scripts-in-ssh-and-wsl-previews-for-your-organization). Приложение для рабочего стола читает этот ключ; терминальный CLI игнорирует его.

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean; только JSON Boolean `true` вступает в силу
  * `true`: приложение для рабочего стола отключает внешний просмотр в панели Browser для людей и Claude одновременно; предпросмотры localhost продолжают работать
  * `false`: внешний просмотр остаётся включённым
* **Default**: не установлено, поэтому внешний просмотр включён

```json managed-settings.json theme={null}
{
  "disableBrowserExternalNavigation": true
}
```

Приложение для рабочего стола игнорирует любое другое значение, и значение, которое не является Boolean, такое как строка `"true"` или `1`, также регистрирует предупреждение. Чтобы оставить внешний просмотр включённым, но отключить инструменты Claude на внешних страницах, установите [`browserExternalPageTools`](#browserexternalpagetools) вместо этого. См. [Ограничить внешний просмотр для вашей организации](https://code.claude.com/docs/ru/desktop.md#restrict-external-browsing-for-your-organization).

Если компьютер, на котором работает приложение для рабочего стола, не получает других управляемых настроек Claude Code, также установите [`parentSettingsBehavior`](#parentsettingsbehavior) в значение `"merge"` в создаваемых вами управляемых настройках. В Windows, если вы создаёте файл управляемых настроек, пользователи также теряют сессии WSL, пока вы [не разрешите их](https://code.claude.com/docs/ru/admin-setup.md#wsl-sessions-in-claude-code-desktop). Причины описаны в разделе [Отключение скриптов в предпросмотрах SSH и WSL для вашей организации](https://code.claude.com/docs/ru/desktop.md#turn-off-scripts-in-ssh-and-wsl-previews-for-your-organization).

### `disableMobileSimulatorTools`

Заблокируйте инструменты Claude для [панели iOS Simulator](https://code.claude.com/docs/ru/desktop-ios-simulator.md#turn-off-simulator-access) приложения для рабочего стола. Люди сохраняют ручное использование панели; удаляется только доступ Claude, и никто не может включить его обратно из приложения. Приложение для рабочего стола читает этот ключ; терминальный CLI игнорирует его.

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean; только JSON Boolean `true` вступает в силу
  * `true`: приложение для рабочего стола блокирует инструменты Claude для панели iOS Simulator
  * `false`: инструменты симулятора Claude следуют переключателю настроек каждого человека в приложении для рабочего стола
* **Default**: не установлено, поэтому инструменты симулятора Claude следуют переключателю настроек каждого человека в приложении для рабочего стола

```json managed-settings.json theme={null}
{
  "disableMobileSimulatorTools": true
}
```

Приложение для рабочего стола игнорирует любое другое значение, и значение, которое не является Boolean, такое как строка `"true"` или `1`, также регистрирует предупреждение.

## Конфиденциальность и телеметрия

Контролируйте, как долго Claude Code хранит данные сеанса и что он отправляет. Переключатели, которые отключают метрики использования и отчеты об ошибках, являются переменными окружения, а не ключами параметров: установите `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING` или `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` в ключе [`env`](#env) или в оболочке. [Услуги телеметрии](https://code.claude.com/docs/ru/data-usage.md#telemetry-services) описывает, что отключает каждый из них. Два исключения отключаются из файла параметров: [`feedbackDrafts`](#feedbackdrafts) ниже для отзывов, составленных Claude, и [`feedbackSurveyRate`](#feedbacksurveyrate) ниже для опроса сеанса.

### `cleanupPeriodDays`

Установите, сколько дней Claude Code хранит [стенограммы сеансов и другие данные приложения](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically) перед их удалением. Claude Code выполняет удаление как фоновую очистку после запуска сеанса, при условии, что он может безопасно определить период хранения. Очистка удаляет стенограммы без отображения сообщения, поэтому сеанс, который вы не использовали дольше, чем период хранения, больше не появляется в средстве выбора [`/resume`](https://code.claude.com/docs/ru/sessions#resume-a-session).

По умолчанию Claude Code хранит транскрипты сессий, которые вы запустили или последними продолжили в Claude Desktop или Cowork, дольше этого периода, даже если вы сами задали этот ключ. Этот период [всё же применяется к ним в некоторых случаях](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically), например в конфигурации HIPAA. До v2.1.248 Claude Code удалял их по истечении этого периода.

* **Область**: [`Any file`](#scopes)
* **Тип**: количество дней, целое число, минимум `1`
* **По умолчанию**: `30`

```json settings.json theme={null}
{
  "cleanupPeriodDays": 20
}
```

Установка `0` не пройдет проверку, поэтому выберите большое значение, например `3650` для длительного хранения. Чтобы остановить Claude Code от записи стенограмм вообще, см. [Хранилище в виде простого текста](https://code.claude.com/docs/ru/claude-directory.md#plaintext-storage).

### `desktopSessionCleanupPeriodDays`

Установите ограничение по возрасту в днях для транскриптов сессий, которые вы запустили или последними продолжили в Claude Desktop или Cowork. Без этого ключа Claude Code [хранит эти транскрипты независимо от возраста](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically), за исключением таких случаев, как сессия, которую вы удалили в Claude Desktop. Требуется Claude Code v2.1.248 или более поздней версии.

Claude Code удаляет каждый транскрипт, как только он становится старше как этого ограничения, так и [`cleanupPeriodDays`](#cleanupperioddays), поэтому при `cleanupPeriodDays` со значением по умолчанию 30 значение `7` все равно сохраняет их 30 дней. В разделе [Автоматическая очистка](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically) перечислены случаи, когда вместо этого применяется `cleanupPeriodDays`, а Claude Code игнорирует этот ключ.

* **Область**: [`User or managed`](#scopes). Claude Code также читает ключ из файла, который вы передаете с `--settings`, и игнорирует его в параметрах проекта и локальных параметрах.
* **Тип**: количество дней, целое число, минимум `0`
* **По умолчанию**: `0`, что не устанавливает ограничение по возрасту

```json settings.json theme={null}
{
  "desktopSessionCleanupPeriodDays": 90
}
```

### `feedbackDrafts`

Контролируйте [отзывы, составленные Claude](https://code.claude.com/docs/ru/tools-reference.md#sendfeedback-tool-behavior): может ли Claude ставить в очередь черновики отзывов для вашего рассмотрения и показывает ли Claude Code карточку, когда Claude ставит один в очередь.

* **Область**: [`User or managed`](#scopes)
* **Тип**: строка, одна из `"notify"`, `"quiet"` или `"off"`
  * `"notify"`: Claude Code показывает карточку над приглашением, когда Claude ставит черновик в очередь, до [трех карточек в сеансе](https://code.claude.com/docs/ru/tools-reference.md#what-you-see-when-claude-drafts) по умолчанию
  * `"quiet"`: Claude составляет черновики без карточки. Вы видите количество поставленных в очередь черновиков в нижнем колонтитуле приглашения и рассматриваете их в `/feedback`
  * `"off"`: Claude Code удаляет инструмент SendFeedback, поэтому Claude не может ставить черновики в очередь
* **По умолчанию**: `"notify"`
* **Переопределения для каждого сеанса**: [`CLAUDE_CODE_SEND_FEEDBACK`](https://code.claude.com/docs/ru/env-vars) установленный на `0` отключает функцию для одного сеанса

```json settings.json theme={null}
{
  "feedbackDrafts": "quiet"
}
```

Появляется в `/config` как **Claude-drafted feedback**, который записывает этот ключ в ваши пользовательские параметры. Вы видите строку `/config` только в сеансах [где Claude может составлять отзывы](https://code.claude.com/docs/ru/tools-reference.md#sessions-without-claude-drafted-feedback); установка `"off"` не скрывает его, поэтому вы можете снова включить функцию из той же строки. Значение в управляемых параметрах имеет приоритет над вашим пользовательским параметром, поэтому когда администратор устанавливает этот ключ, строка показывает управляемое значение, и его изменение не имеет эффекта. Claude Code игнорирует этот ключ в параметрах проекта и локальных параметрах.

### `feedbackSurveyRate`

Установите вероятность того, что [опрос качества сеанса](https://code.claude.com/docs/ru/data-usage.md#session-quality-surveys) появится, когда сеанс имеет право на него. Установите `0`, чтобы опрос не появлялся.

* **Область**: [`Any file`](#scopes)
* **Тип**: число между `0` и `1`
* **По умолчанию**: не установлено, поэтому Claude Code использует скорость, которую Anthropic устанавливает удаленно, или встроенную скорость `0.005` на Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry, которые не получают удаленную конфигурацию
* **Переопределения для каждого сеанса**: [`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`](https://code.claude.com/docs/ru/env-vars) установленный на `1` отключает опрос для одного сеанса независимо от скорости, которую устанавливает этот ключ

```json settings.json theme={null}
{
  "feedbackSurveyRate": 0.05
}
```

Та же скорость применяется к опросу в расширении VS Code.

### `skipWebFetchPreflight`

Пропустите [проверку безопасности домена WebFetch](https://code.claude.com/docs/ru/data-usage.md#webfetch-domain-safety-check), которая отправляет каждое запрашиваемое имя хоста на `api.anthropic.com` перед выборкой. Установите `true` в окружениях, которые блокируют трафик к Anthropic, таких как Amazon Bedrock, Google Cloud's Agent Platform или развертывания Microsoft Foundry с ограничивающим исходящим трафиком.

* **Область**: [`Any file`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code пропускает проверку безопасности домена WebFetch
  * `false`: проверка выполняется перед первой выборкой для каждого имени хоста в сеансе и снова для имени хоста, чья более ранняя проверка была заблокирована или не удалась
* **По умолчанию**: не установлено, поэтому проверка выполняется перед первой выборкой для каждого имени хоста в сеансе

```json settings.json theme={null}
{
  "skipWebFetchPreflight": true
}
```

С пропущенной проверкой WebFetch пытается использовать любой URL без консультации со списком блокировки, поэтому объедините его с [правилами разрешений `WebFetch`](https://code.claude.com/docs/ru/permissions#webfetch), если вам нужно ограничить, какие домены может достичь Claude.

## Корпоративные и управляемые настройки

Ключи, которые организация использует для вычисления, обновления и объединения управляемых настроек. См. [Настройка управляемых настроек](https://code.claude.com/docs/ru/admin-setup.md).

### `disableSideloadFlags`

Отклонять при запуске флаги CLI `--plugin-dir`, `--plugin-url`, `--agents` и `--mcp-config`, с помощью которых пользователи иначе могли бы обойти [`strictKnownMarketplaces`](#strictknownmarketplaces) для одного запуска. Claude Code завершает работу с ошибкой, в которой перечислены отклонённые флаги. В [облачных сессиях](https://code.claude.com/docs/ru/claude-code-on-the-web.md) Claude Code вместо этого запускает сессию и отбрасывает все переданные сервером записи `--mcp-config`, кроме внутрипроцессных записей `type: "sdk"` и инструментов Slack в сессии [Claude Tag](https://code.claude.com/docs/ru/claude-tag.md). Требуется Claude Code v2.1.193 или новее.

* **Область действия**: [`Managed`](#scopes)
* **Тип**: Boolean
  * `true`: Claude Code отклоняет `--plugin-dir`, `--plugin-url`, `--agents` и `--mcp-config` при запуске и завершает работу с ошибкой, в которой они перечислены. В облачных сессиях он вместо этого запускает сессию и отбрасывает все переданные сервером записи `--mcp-config`, кроме внутрипроцессных записей `type: "sdk"` и инструментов Slack в сессии Claude Tag
  * `false`: Claude Code принимает эти флаги
* **По умолчанию**: `false`

```json managed-settings.json theme={null}
{
  "disableSideloadFlags": true
}
```

Claude Code по-прежнему принимает `--mcp-config`, если все его серверы являются внутрипроцессными записями `type: "sdk"`, поэтому Agent SDK и расширение VS Code продолжают работать. Пользователи по-прежнему могут добавлять серверы с помощью `claude mcp add` или файла `.mcp.json`; для управления отдельными серверами также задайте [`allowedMcpServers`](https://code.claude.com/docs/ru/managed-mcp). Требуется Claude Code v2.1.193 или новее.

`disableSideloadFlags` также отклоняет папки плагинов из следующих источников:

* **Переменная окружения [`CLAUDE_CODE_PLUGIN_DIRS`](https://code.claude.com/docs/ru/env-vars#variables)**: если переменная указывает папку плагина, Claude Code завершает работу при запуске с ошибкой, в которой названа переменная и сказано, что её нужно удалить. Требуется Claude Code v2.1.280 или новее
* **Параметр Agent SDK [`addPlugins`](https://code.claude.com/docs/ru/agent-sdk/typescript#load-more-plugin-folders-with-addplugins)**: когда приложение передаёт папки плагинов в `reloadPlugins()` через `addPlugins`, этот вызов завершается ошибкой. Сессия продолжает работать с уже загруженными плагинами. Требуется Claude Code v2.1.301 или новее

В облачных сессиях Claude Code также игнорирует переданные сервером обновления MCP в ходе сессии — механизм, стоящий за конфигурацией облачных сессий и вызовами SDK `setMcpServers()`, которые доходят до этих сессий. Внутрипроцессные записи `type: "sdk"` и инструменты Slack в сессии Claude Tag здесь также остаются исключением. До v2.1.268 как это отбрасывание, так и отбрасывание при запуске также удаляли инструменты Slack в сессии Claude Tag. До v2.1.239 переданный сервером `--mcp-config` блокировал запуск облачной сессии.

Настольное приложение само управляет некоторыми плагинами, включая плагины, синхронизированные с claude.ai, и плагины, которые ваша организация развёртывает через приложение. Если вы развёртываете этот ключ на устройство через MDM, политику на уровне ОС или файл управляемых настроек, настольное приложение не передаёт эти плагины следующим сессиям на этом устройстве:

* **[Сессии Code на компьютере пользователя](https://code.claude.com/docs/ru/desktop.md#environment-configuration)**: они также запускаются без скиллов, включённых для учётной записи пользователя на claude.ai. Плагины, которые Claude Code устанавливает из маркетплейсов, указанных в ваших управляемых настройках, по-прежнему загружаются. В [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) MCP-серверы из плагинов, которые вы развёртываете в каталог `org-plugins` устройства, также остаются доступными, потому что настольное приложение подключается к ним само. До Claude Desktop v1.37937.0 эти сессии вместо этого завершались сбоем при запуске.
* **[Сессии Cowork на компьютере пользователя](https://code.claude.com/docs/ru/managed-settings.md#where-and-when-a-policy-applies)**: скиллы внутри этих плагинов и скиллы, включённые для учётной записи пользователя на claude.ai, остаются доступными. В [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) MCP-серверы из плагинов, которые вы развёртываете в каталог `org-plugins` устройства, также остаются доступными, потому что настольное приложение подключается к ним само. До Claude Desktop v1.44121.0 эти сессии вместо этого завершались сбоем при запуске.

### `forceRemoteSettingsRefresh`

Блокировать запуск CLI, пока Claude Code заново не получит [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md). Если получить их не удаётся, Claude Code завершает работу, а не продолжает с кэшированными настройками или без них. Задайте этот ключ, если ваша среда не допускает даже короткого промежутка времени, когда сессия работает без управляемой политики.

Если ключ не задан, Claude Code не блокирует запуск ради получения настроек, хотя, когда разработчик входит в систему при запуске, он ждёт получения настроек до пяти секунд. [Anthropic может требовать наличия этих настроек](https://code.claude.com/docs/ru/server-managed-settings.md#fetch-and-caching-behavior), и тогда запуск без них блокируется. Сессия Cloud gateway ждёт и завершает работу, если шлюз недоступен.

* **Область действия**: [`Managed`](#scopes). Claude Code учитывает значение `true` из любого управляемого источника, контролируемого администратором, даже если это не источник с наивысшим приоритетом.
* **Тип**: Boolean
  * `true`: Claude Code блокирует запуск, пока заново не получит настройки, управляемые сервером, и завершает работу, если получить их не удалось
  * `false`: если Anthropic не требует наличия настроек, Claude Code не блокирует запуск ради их получения, хотя при запуске со входом в систему ждёт их получения до пяти секунд
* **По умолчанию**: `false`

```json managed-settings.json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

Задайте его в профиле MDM или в файле управляемых настроек, чтобы обеспечить безопасный отказ при запуске (fail-closed) ещё до поступления первых данных от сервера. Claude Code выполняет эту проверку только в сессиях, которые получают настройки, управляемые сервером, поэтому сессия, которая [их не получает](https://code.claude.com/docs/ru/server-managed-settings.md#platform-availability), запускается без ожидания. Подкоманды `claude auth` освобождены от проверки, чтобы пользователи могли повторно пройти аутентификацию, если получение настроек не удаётся из-за истёкших учётных данных. См. [Обеспечение безопасного отказа при запуске](https://code.claude.com/docs/ru/server-managed-settings.md#enforce-fail-closed-startup).

### `managedSourcesBehavior`

Выберите, применяет ли Claude Code только [управляемый источник](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources) с наивысшим приоритетом из тех, что предоставляет ваша организация, или объединяет все предоставляемые ею источники администратора. По умолчанию Claude Code берёт источник с наивысшим приоритетом, содержащий [ключ политики](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources), и игнорирует остальные. Ключ политики — это любой ключ настроек, кроме этого и `wslInheritsWindowsSettings`. При поведении по умолчанию, как только настройки, управляемые сервером, или политика MDM передают ключ политики, файл `managed-settings.json` вносит только [ключи, которые Claude Code читает из каждого источника администратора](https://code.claude.com/docs/ru/managed-settings.md#keys-read-from-every-admin-source). При значении `"merge"` каждый предоставляемый вами источник администратора вносит свои ключи в единую объединённую политику. Требуется Claude Code v2.1.242 или новее.

Задавайте `"merge"` только там, где каждый источник, [стоящий по рангу](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources) ниже вашего самого приоритетного, находится под контролем администратора, потому что Claude Code тогда добавляет в политику записи из нижестоящего источника, например правила `permissions.allow`.

* **Область действия**: [`Managed`](#scopes). Claude Code читает этот ключ из источника с наивысшим приоритетом, содержащего либо этот ключ, либо ключ политики, и игнорирует этот ключ во всех источниках ниже по рангу, поэтому нижестоящий источник не может сам включить объединение с вышестоящим источником. Ни реестр Windows HKCU, ни [родительские настройки от встраивающего хоста](https://code.claude.com/docs/ru/managed-settings.md#let-an-embedding-host-add-policy) в объединении не участвуют.
* **Тип**: string, одно из значений:
  * `"first-wins"`: политику предоставляет источник с наивысшим приоритетом, содержащий ключ политики, а нижестоящие источники вносят только [ключи, которые Claude Code читает из каждого источника администратора](https://code.claude.com/docs/ru/managed-settings.md#keys-read-from-every-admin-source)
  * `"merge"`: каждый предоставляемый вами источник администратора вносит свои ключи, которые объединяются по приведённым ниже правилам
* **По умолчанию**: `"first-wins"`

Передавайте этот ключ в источнике с наивысшим приоритетом из тех, что вы развёртываете. Компьютеру, который никогда не получает настройки, управляемые сервером, этот ключ нужен также в профиле MDM, потому что Claude Code читает ключ из источника с наивысшим приоритетом, содержащего его или ключ политики. Файл `managed-settings.json` — источник администратора с самым низким рангом, поэтому у заданного в нём `"merge"` нет нижестоящего источника для объединения. В настройках, управляемых сервером, ключ выглядит так:

```json theme={null}
{
  "managedSourcesBehavior": "merge"
}
```

При `"merge"` Claude Code объединяет каждый ключ в зависимости от его вида. В этой таблице приведено правило для каждого вида. В строках «Списки разрешённых значений для ограничений», «Значения, берущиеся целиком» и «Чтение только из источника с наивысшим приоритетом» перечислены все охватываемые ими ключи, а в остальных строках приведены примеры:

| Вид ключа | Как Claude Code его объединяет | Ключи |
| :- | :- | :- |
| Списки | Объединяет записи из всех источников | [`permissions.allow`](#permissions-allow), [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) и другие ключи-списки |
| Блокировки | Применяет самое строгое значение, заданное любым источником. Если ни один источник не задаёт строгое значение, применяет менее строгое значение только из самого приоритетного источника | [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly), [`permissions.disableBypassPermissionsMode`](#permissions-disablebypasspermissionsmode) и другие логические или перечислимые блокировки |
| Списки разрешённых значений для ограничений | Берёт список целиком из самого приоритетного источника, который его задаёт, не добавляя записи из нижестоящих источников. Если самый приоритетный источник его не задаёт, берёт его целиком из следующего источника ниже | [`availableModels`](#availablemodels), [`allowedMcpServers`](#allowedmcpservers), [`allowedProviders`](#allowedproviders), [`strictKnownMarketplaces`](#strictknownmarketplaces), [`allowedChannelPlugins`](#allowedchannelplugins) и цепочка [`fallbackModel`](#fallbackmodel) |
| Значения, берущиеся целиком | Берёт значение целиком из самого приоритетного источника, который его задаёт, не объединяя записи или поля из нижестоящих источников. Если самый приоритетный источник его не задаёт, берёт его целиком из следующего источника ниже | [`sandbox.credentials.awsPairs`](#sandbox-credentials-awspairs), [`sandbox.ripgrep`](#sandbox-ripgrep) |
| Предоставляемые MCP-серверы | Объединяет имена серверов из всех источников. Если два источника задают одинаковое имя, применяет запись из вышестоящего источника целиком | [`managedMcpServers`](#managedmcpservers) |
| Чтение только из источника с наивысшим приоритетом | Читает ключ только из источника с наивысшим приоритетом, содержащего ключ политики, поэтому значение нижестоящего источника игнорируется, даже если самый приоритетный источник не задаёт никакого значения | [`apiKeyHelper`](#apikeyhelper), [`awsAuthRefresh`](#awsauthrefresh), [`awsCredentialExport`](#awscredentialexport), [`gcpAuthRefresh`](#gcpauthrefresh), [`otelHeadersHelper`](#otelheadershelper), `proxyAuthHelper`, [`parentSettingsBehavior`](#parentsettingsbehavior), [`modelPicker`](#modelpicker), [`policyHelper`](#policyhelper), [`permissions.defaultMode`](#permissions-defaultmode) |
| `env` | [Объединяется по отдельным переменным во всех источниках администратора](https://code.claude.com/docs/ru/managed-settings.md#keys-read-from-every-admin-source) как при `"first-wins"`, так и при `"merge"` | [`env`](#env) |
| Все остальные ключи | Берёт значение из самого приоритетного источника, который его задаёт | [`cleanupPeriodDays`](#cleanupperioddays), [`model`](#model) |

Получение `sandbox.credentials.awsPairs` и `sandbox.ripgrep` целиком требует Claude Code v2.1.257 или новее.

Для некоторых ключей действует дополнительное условие, которое не отражено в таблице:

* **[`policyHelper`](#policyhelper)**: Claude Code учитывает его, только если самый приоритетный источник, содержащий ключ политики, — это политика MDM или файл управляемых настроек, поэтому при настройках, управляемых сервером, он не применяется.
* **[`modelOverrides`](#modeloverrides)**: работает в паре с `availableModels`. Claude Code берёт `modelOverrides` из самого приоритетного источника, который его задаёт, если только вышестоящий источник не задаёт `availableModels` без `modelOverrides`. В этом случае он игнорирует `modelOverrides` из всех источников.
* **[`forceLoginGatewayUrl`](#forcelogingatewayurl), [`gatewayInternalNetworks`](#gatewayinternalnetworks) и значение `"gateway"` ключа [`forceLoginMethod`](#forceloginmethod)**: Claude Code никогда не читает ни один из них из настроек, управляемых сервером, поэтому значение там не применяется и не скрывает значение, заданное в политике MDM или файле управляемых настроек. Из источников администратора на компьютере их предоставляет только самый высокий по рангу источник, содержащий ключ политики, независимо от того, присутствуют ли также настройки, управляемые сервером.
* **[`forceLoginOrgUUID`](#forceloginorguuid) и значения `"claudeai"` и `"console"` ключа [`forceLoginMethod`](#forceloginmethod)**: какое значение применяется, смотрите в разделе [Какой управляемый источник предоставляет ключи входа](https://code.claude.com/docs/ru/managed-settings.md#which-managed-source-supplies-login-keys), а не в таблице.
* **[`allowedProviders`](#allowedproviders)**: после применения правила из таблицы результат по-прежнему ограничивается собственным списком компьютера, как указано в примечании об области действия в описании этого ключа.

Чтобы проверить, какие источники были объединены на компьютере, выполните `/status` и [посмотрите строку `Setting sources`](https://code.claude.com/docs/ru/managed-settings#read-the-source-in-/status).

### `parentSettingsBehavior`

Выберите, применяет ли Claude Code управляемые настройки, предоставленные процессом встраивающего хоста, например Agent SDK или расширением IDE, если также присутствует уровень управляемых настроек, развёрнутый администратором. При `"first-wins"` Claude Code отбрасывает настройки, предоставленные хостом; при `"merge"` он применяет их под уровнем администратора через фильтр, пропускающий только ограничения. Задайте `"merge"`, когда хосту нужно передавать собственные ограничения запускаемым им сессиям, например когда Claude Desktop передаёт список разрешённых исходящих адресов шлюза.

* **Область действия**: [`Managed`](#scopes). Claude Code читает его из управляемого источника с наивысшим приоритетом, контролируемого администратором.
* **Тип**: string, одно из значений:
  * `"first-wins"`: Claude Code отбрасывает настройки, предоставленные хостом, если присутствует уровень управляемых настроек, развёрнутый администратором
  * `"merge"`: Claude Code применяет настройки, предоставленные хостом, под уровнем администратора через фильтр, пропускающий только ограничения
* **По умолчанию**: `"first-wins"`

```json managed-settings.json theme={null}
{
  "parentSettingsBehavior": "merge"
}
```

Этот ключ не действует, если уровня управляемых настроек, развёрнутого администратором, нет: тогда настройки хоста применяются как единственный управляемый уровень, по-прежнему отфильтрованные до ограничивающих значений. Об ограничениях фильтра и о том, как взаимодействуют управляемые источники, см. [Родительские настройки от встраивающих хостов](https://code.claude.com/docs/ru/managed-settings.md#parent-settings-from-embedding-hosts) и [Ограничение родительских настроек](https://code.claude.com/docs/ru/claude-apps-gateway#restrict-parent-settings).

### `policyHelper`

Запускать развёрнутый вами исполняемый файл, который вычисляет управляемые настройки при запуске, чтобы вы могли формировать политику на основе состояния устройства, идентичности или удалённого сервиса, а не статического файла. Claude Code запускает хелпер до того, как примет первый промпт, и использует выведенные им настройки как управляемые настройки сессии.

* **Область действия**: [`Managed`](#scopes). Читается из plist macOS, реестра Windows HKLM или файла управляемых настроек. Claude Code читает ключ из управляемого источника с наивысшим приоритетом, содержащего [ключ политики](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources), и запускает хелпер, только если этот источник — один из этих трёх; он игнорирует ключ в настройках, управляемых сервером, в реестре HKCU и в родительских настройках, предоставленных хостом.
* **Тип**: объект с полями `path`, `timeoutMs` и `refreshIntervalMs`
* **По умолчанию**: не задано, поэтому хелпер не запускается

Если настройки, управляемые сервером, передают политику при запуске, они имеют приоритет над источником хелпера, и хелпер не запускается.

Если при последующем получении настроек выясняется, что настройки, управляемые сервером, удалены, Claude Code запускает хелпер в этот момент, а не ждёт следующего запуска. Его вывод определяет поведение до конца сессии, а неудачный запуск завершает сессию с тем же сообщением, что и [неудачный запуск при старте](#helper-failures).

В этом примере хелпер запускается с таймаутом 5 секунд и перезапускается каждые пять минут:

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000,
    "refreshIntervalMs": 300000
  }
}
```

#### Формирование вывода хелпера

Claude Code запускает хелпер без аргументов, устанавливает `CLAUDE_CODE_VERSION` в его окружении и читает из stdout JSON-конверт размером не более 1 MiB.

Поместите настройки под ключ `managedSettings`. Голый объект настроек без ключа `managedSettings` разбирается с неопределённым `managedSettings` и ничего не применяет, причём Claude Code не сообщает об ошибке:

```json theme={null}
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  }
}
```

Когда хелпер выводит `managedSettings`, этот объект становится единственным источником управляемых настроек для данного запуска: Claude Code игнорирует источники MDM, файла и HKCU, читает [ключи, общие для всех источников](https://code.claude.com/docs/ru/managed-settings.md#keys-read-from-every-admin-source), только из вывода хелпера и никогда не объединяет [родительские настройки](https://code.claude.com/docs/ru/managed-settings.md#parent-settings-from-embedding-hosts).

Проверка `forceRemoteSettingsRefresh` при запуске выполняется до хелпера и читает любой источник администратора. Хелпер, который завершается с кодом `0` и выводит конверт без `managedSettings`, не вносит управляемых настроек, и остальные источники применяются как обычно.

#### Сбои хелпера

Запуск хелпера завершается неудачей, если:

* `path` нарушает правила, описанные в [`policyHelper.path`](#policyhelper-path).
* По пути `path` нет обычного файла. Claude Code проверяет наличие файла перед запуском хелпера в рамках того же лимита `timeoutMs`, поэтому неотвечающий сетевой диск может привести к неудачному запуску.
* Хелпер завершается с ненулевым кодом, всё ещё работает по истечении `timeoutMs` или вообще не запускается, например потому что не является исполняемым.
* Хелпер записывает в stdout или stderr более 1 MiB.
* stdout не является одним JSON-объектом, или его `managedSettings` содержит [нарушение схемы, которое Claude Code не может исправить](https://code.claude.com/docs/ru/managed-settings.md#find-entries-claude-code-dropped).

Если запуск при старте завершается неудачей, Claude Code выводит причину и отказывается запускаться. После ненулевого кода завершения причина включает stderr хелпера или его stdout, если stderr пуст. После таймаута в причине указывается лимит `timeoutMs`, но не приводится никакой вывод хелпера. Отказ распространяется на интерактивные сессии, `claude -p`, сессии Agent SDK, [фоновые сессии](https://code.claude.com/docs/ru/agent-view.md) и большинство подкоманд.

Этот отказ преднамеренный, поэтому хелпер, которому нужна устойчивость к сбоям, должен отдавать данные из собственного кэша и завершаться с кодом `0`.

Если фоновое обновление завершается неудачей, Claude Code сохраняет в силе последнюю успешно полученную политику, а `/status` показывает неудачное обновление с его причиной, пока обновление не пройдёт успешно. Каждое обновление выполняется с тем же `timeoutMs` и по тем же правилам сбоев, что и запуск при старте.

С флагом `--debug` Claude Code записывает stderr хелпера от каждого запуска в [лог отладки](https://code.claude.com/docs/ru/debug-your-config.md).

Claude Code сообщает о недопустимом значении `policyHelper` как об [отброшенной записи](https://code.claude.com/docs/ru/managed-settings.md#find-entries-claude-code-dropped) и запускает сессию с остальными управляемыми настройками, не запуская хелпер. К недопустимым значениям относятся путь, указанный голой строкой, и `timeoutMs` ниже [своего минимума](#policyhelper-timeoutms).

Чтобы отключить хелпер, удалите ключ из источника, который его задаёт.

### `policyHelper.path`

Укажите исполняемый файл хелпера, который запускает Claude Code. О том, что происходит, если путь нарушает приведённые ниже правила, см. [Сбои хелпера](#helper-failures).

* **Область действия**: [`Managed`](#scopes). Читается из plist macOS, реестра Windows HKLM или файла управляемых настроек — там же, где читается [`policyHelper`](#policyhelper).
* **Тип**: string, абсолютный путь в нормализованной форме, без сегментов `.` или `..`; в Windows — путь с буквой диска или UNC-путь, оканчивающийся на `.exe`
* **По умолчанию**: нет; обязателен, если задан `policyHelper`

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy"
  }
}
```

### `policyHelper.timeoutMs`

Задайте, сколько Claude Code ждёт хелпер, прежде чем считать запуск неудачным. Запуск, завершившийся по таймауту, считается неудачным так же, как ненулевой код завершения, поэтому при старте Claude Code отказывается запускаться.

* **Область действия**: [`Managed`](#scopes). Читается из plist macOS, реестра Windows HKLM или файла управляемых настроек — там же, где читается [`policyHelper`](#policyhelper).
* **Тип**: integer, миллисекунды, минимум `1000`
* **По умолчанию**: `10000`

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000
  }
}
```

### `policyHelper.refreshIntervalMs`

Заставить Claude Code периодически перезапускать хелпер в фоновом режиме, чтобы изменения политики доходили до работающей сессии. Если обновление проходит успешно, его вывод заменяет предыдущие управляемые настройки без перезапуска; если обновление завершается неудачей, Claude Code сохраняет уже имеющуюся политику.

* **Область действия**: [`Managed`](#scopes). Читается из plist macOS, реестра Windows HKLM или файла управляемых настроек — там же, где читается [`policyHelper`](#policyhelper).
* **Тип**: integer, миллисекунды: `0`, чтобы отключить обновление, иначе не менее `60000`
* **По умолчанию**: не задано, поэтому Claude Code запускает хелпер один раз при старте

В этом примере хелпер перезапускается каждые пять минут:

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "refreshIntervalMs": 300000
  }
}
```

### `wslInheritsWindowsSettings`

Заставить Claude Code в WSL читать управляемые настройки из цепочки политик Windows, в которой HKLM и файл управляемых настроек Windows имеют приоритет над `/etc/claude-code`, а HKCU стоит ниже. Пока цепочка включена, Claude Code читает `/etc/claude-code` только тогда, когда [нет документа администратора Windows](https://code.claude.com/docs/ru/managed-settings.md#present-admin-documents) ни в значении реестра HKLM, ни в папке `C:\Program Files\ClaudeCode\`. Задайте этот ключ, чтобы распространить политику, которую вы уже развёртываете в Windows, на сессии WSL на том же компьютере, чтобы они следовали тем же правилам, что и сессии хоста. Claude Code учитывает его, только если он задан в ключе реестра HKLM или в файле управляемых настроек либо дополнительном файле (drop-in) в `C:\Program Files\ClaudeCode\` — для записи в оба места требуются права администратора Windows.

* **Область действия**: [`Managed`](#scopes). В источнике Windows, контролируемом администратором.
* **Тип**: Boolean
  * `true`: Claude Code в WSL читает управляемые настройки из цепочки политик Windows и читает `/etc/claude-code` только при отсутствии документа администратора Windows
  * `false`: WSL читает только `/etc/claude-code`
* **По умолчанию**: `false`, поэтому WSL читает только `/etc/claude-code`

```json managed-settings.json theme={null}
{
  "wslInheritsWindowsSettings": true
}
```

После того как источник администратора включает цепочку, политика HKCU присоединяется к ней в WSL, только если HKCU тоже задаёт этот ключ как `true`. Эта копия сама по себе цепочку не включает. Источник Windows, содержащий только этот ключ со значением `true` или `false`, не считается источником политики, поэтому политику по-прежнему предоставляет источник с более низким приоритетом. В нативной Windows этот ключ не действует.

Claude Code распознаёт `true` и `false` как в кавычках, так и без них, а `null` воспринимает как удаление ключа. Источник Windows, контролируемый администратором, содержащий любое другое значение, считается [присутствующим документом администратора](https://code.claude.com/docs/ru/managed-settings.md#present-admin-documents) с включённой цепочкой: ни `/etc/claude-code`, ни HKCU не применяются, а при запуске выводится предупреждение с названием ключа. Значение HKLM или файл в папке Windows, которые существуют, но не могут быть прочитаны, также не позволяют применить `/etc/claude-code` независимо от того, включена ли цепочка. Требуется Claude Code v2.1.282 или новее.

## Глобальные параметры конфигурации

Сохраняйте эти ключи в `~/.claude.json`, а не в файле параметров. Claude Code игнорирует их везде в других местах. Claude Code и `/config` записывают большинство из них за вас, и вы также можете редактировать их вручную.

### `autoConnectIde`

Подключайтесь к запущенной IDE автоматически при запуске Claude Code из внешнего терминала. Отображается в `/config` как **Auto-connect to IDE (external terminal)** при запуске Claude Code вне терминала VS Code или JetBrains.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code подключается к запущенной IDE автоматически при запуске из внешнего терминала
  * `false`: Claude Code не подключается автоматически из внешнего терминала; внутри терминала VS Code или JetBrains, или с `--ide`, он все еще подключается
* **Default**: `false`
* **Per-session overrides**: [`CLAUDE_CODE_AUTO_CONNECT_IDE`](https://code.claude.com/docs/ru/env-vars) имеет приоритет над этим ключом для одного сеанса в любом направлении

```json ~/.claude.json theme={null}
{
  "autoConnectIde": true
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `autoInstallIdeExtension`

Позволяет [`/ide`](https://code.claude.com/docs/ru/commands) устанавливать расширение Claude Code IDE в запущенный VS Code, Cursor или Devin Desktop, когда вы выполняете команду из внешнего терминала. Claude Code не устанавливает и не обновляет расширение при запуске `claude`. До v2.1.318 Claude Code устанавливает или обновляет расширение при запуске `claude` в терминале одного из этих редакторов, если только этот ключ не имеет значение `false`.

Отображается в `/config` как **Auto-install IDE extension** при запуске Claude Code внутри терминала VS Code или JetBrains.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: `/ide` устанавливает расширение
  * `false`: `/ide` не устанавливает расширение
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](https://code.claude.com/docs/ru/env-vars) установленный на `1` пропускает установку для одного сеанса даже когда этот ключ имеет значение `true`

```json ~/.claude.json theme={null}
{
  "autoInstallIdeExtension": false
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `claudeInChromeDefaultEnabled`

Запускайте каждую интерактивную сессию CLI с включенной [интеграцией Chrome](https://code.claude.com/docs/ru/chrome.md), без необходимости передавать `--chrome` каждый раз. Если вы запустите [`claude remote-control`](https://code.claude.com/docs/ru/remote-control), сессия, которую он запускает для одного из ваших потоков [проекта](https://code.claude.com/docs/ru/claude-projects.md), также следует этому ключу, за исключением режима `bypassPermissions`. В Claude Code v2.1.287 или более поздней версии этот ключ также применяется к сессиям в [расширении VS Code](https://code.claude.com/docs/ru/vs-code.md#automate-browser-tasks-with-chrome): см. [Enable Chrome by default](https://code.claude.com/docs/ru/chrome.md#enable-chrome-by-default).

Запуск `/chrome` и выбор **Enabled by default** устанавливает этот ключ за вас, как и ответ в [диалоговом окне «Claude in Chrome extension detected»](https://code.claude.com/docs/ru/chrome.md#answer-the-startup-dialog). Отображается в `/config` как **Claude in Chrome enabled by default**.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code включает интеграцию Chrome при запуске интерактивной сессии CLI, как это происходит при передаче `--chrome`. В расширении VS Code сессии подключаются к браузеру при запуске
  * `false`: интерактивные сессии CLI запускаются с отключенной интеграцией Chrome, и Claude Code прекращает [предлагать ее настройку](https://code.claude.com/docs/ru/chrome.md#install-the-extension-when-claude-asks). Передайте `--chrome`, чтобы включить ее для одной интерактивной сессии. В расширении VS Code сессия подключается, когда вы вводите `@browser`, как и в случае, когда ключ не задан
* **Default**: unset, поэтому интеграция Chrome отключена и Claude Code все еще может предложить ее настройку
* **Per-session overrides**: `--chrome` и [`--no-chrome`](https://code.claude.com/docs/ru/cli-reference) имеют приоритет над этим ключом для одного интерактивного сеанса

```json ~/.claude.json theme={null}
{
  "claudeInChromeDefaultEnabled": true
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `copyFullResponse`

Делайте так, чтобы [`/copy`](https://code.claude.com/docs/ru/commands) копировала полный ответ каждый раз, без показа средства выбора. Выбор **Always copy full response** в этом средстве выбора устанавливает этот ключ в `true`. Отображается в `/config` как **Skip the /copy picker**.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: `/copy` копирует полный ответ без показа средства выбора
  * `false`: когда ответ содержит блоки кода или цитаты, `/copy` показывает средство выбора, где вы выбираете один блок или полный ответ
* **Default**: `false`

```json ~/.claude.json theme={null}
{
  "copyFullResponse": true
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `copyOnSelect`

Копируйте текст в буфер обмена автоматически при завершении выделения текста мышью в [полноэкранном режиме](https://code.claude.com/docs/ru/fullscreen.md#use-the-mouse) или [представлении агента](https://code.claude.com/docs/ru/agent-view.md). Отображается в `/config` как **Copy on select** во время включения полноэкранного режима.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code копирует текст в буфер обмена при завершении выделения
  * `false`: выделение текста оставляет буфер обмена без изменений, и вы [копируете выделение с помощью сочетания клавиш](https://code.claude.com/docs/ru/fullscreen.md#use-the-mouse) вместо этого
* **Default**: `true`

```json ~/.claude.json theme={null}
{
  "copyOnSelect": false
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `defaultToAgentsView`

Открывайте [представление агента](https://code.claude.com/docs/ru/agent-view.md) вместо нового разговора при запуске `claude` без аргументов. Отображается в `/config` как **Open agents view by default**, если представление агента не [отключено](#disableagentview).

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: `claude` без аргументов открывает представление агента, если представление агента не [отключено](#disableagentview)
  * `false`: `claude` без аргументов запускает новый разговор
* **Default**: `false`

```json ~/.claude.json theme={null}
{
  "defaultToAgentsView": true
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `diffTool`

Выбирайте, где Claude Code показывает diff изменения `Edit` или `Write`, которое оно предлагает, когда подключена IDE [VS Code](https://code.claude.com/docs/ru/vs-code.md) или [JetBrains](https://code.claude.com/docs/ru/jetbrains.md#features): `"auto"` открывает его в средстве просмотра diff IDE, `"terminal"` сохраняет его в терминале. Отображается в `/config` как **Diff tool** только когда Claude Code подключен к IDE VS Code или JetBrains.

* **Scope**: [`Global config`](#scopes)
* **Type**: string, один из:
  * `"auto"`: Claude Code открывает diff в средстве просмотра diff IDE при подключении IDE VS Code или JetBrains
  * `"terminal"`: Claude Code сохраняет diff в терминале
* **Default**: `"auto"`

```json ~/.claude.json theme={null}
{
  "diffTool": "terminal"
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `externalEditorContext`

При нажатии `Ctrl+G` Claude Code открывает подсказку, которую вы печатаете, в вашем [внешнем редакторе](https://code.claude.com/docs/ru/interactive-mode.md#general-controls). Когда этот ключ включен, буфер редактора начинается с предыдущего ответа Claude в виде строк комментариев `#`, чтобы вы могли прочитать его во время написания, и Claude Code удаляет эти строки при сохранении. Отображается в `/config` как **Show last response in external editor**.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: буфер редактора начинается с предыдущего ответа Claude в виде строк комментариев `#`, которые Claude Code удаляет при сохранении
  * `false`: буфер редактора открывается только с вашей подсказкой
* **Default**: `false`

```json ~/.claude.json theme={null}
{
  "externalEditorContext": true
}
```

Когда это включено, буфер, который открывает Claude Code, выглядит так, и только текст ниже строки маркера отправляется как ваша подсказка:

```text theme={null}
# ─── Claude's last response (for reference; removed on save) ───
# I added the retry loop to fetchUser in src/api.ts and a test
# for the timeout case. Want me to wire the same retry into
# fetchOrders?
# ─── Write your reply below this line ──────────────────────────

Yes, and cap it at three attempts.
```

Claude Code сохраняет последние 50 строк ответа и отмечает срез с помощью `# … (earlier output truncated)`.

Claude Code игнорирует этот ключ в `settings.json`.

### `leftArrowOpensAgents`

Нажимайте `←` на пустой подсказке, чтобы [отправить сеанс в фоновый режим и открыть представление агента](https://code.claude.com/docs/ru/agent-view.md#switch-sessions-without-leaving-the-terminal). Установите этот ключ на `false`, чтобы отключить сочетание клавиш. Отображается в `/config` как **← opens agents**, когда представление агента доступно.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: нажатие `←` на пустой подсказке в сеансе, который вы запустили в терминале, отправляет его в фоновый режим и открывает представление агента
  * `false`: Claude Code отключает сочетание клавиш; в сеансе, который вы [присоединили из представления агента](https://code.claude.com/docs/ru/agent-view.md#attach-to-a-session), `←` на пустой подсказке все еще отсоединяет
* **Default**: `true`

```json ~/.claude.json theme={null}
{
  "leftArrowOpensAgents": false
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `permissionExplainerEnabled`

> [!WARNING]
>
> Удалено в v2.1.257 вместе с объяснением команды `Ctrl+E` на подсказках разрешений Bash и PowerShell. Установка этого параметра не влияет на текущие версии.

До версии v2.1.256 вы могли нажать `Ctrl+E` на подсказке разрешения Bash или PowerShell, чтобы увидеть созданное моделью объяснение команды, и установить этот ключ на `false`, чтобы отключить это сочетание клавиш.

* **Scope**: [`Global config`](#scopes). На v2.1.256 и более ранних версиях.
* **Type**: Boolean
* **Default**: `true`

### `prStatusFooterEnabled`

Показывайте значок в нижнем колонтитуле подсказки для открытого запроса на слияние или запроса на объединение текущей ветви с цветной подчеркиванием, которое показывает его [статус](https://code.claude.com/docs/ru/interactive-mode.md#pr-review-status). Отображается в `/config` как **Show PR status footer**.

* **Scope**: [`Global config`](#scopes)
* **Type**: Boolean
  * `true`: нижний колонтитул показывает значок при условиях в [PR review status](https://code.claude.com/docs/ru/interactive-mode.md#pr-review-status)
  * `false`: Claude Code пропускает проверку запроса на слияние и запроса на объединение нижнего колонтитула и не показывает этот значок. Сеанс, который вы [присоединили из представления агента](https://code.claude.com/docs/ru/agent-view.md#attach-to-a-session), все еще может показать простую ссылку на запрос на слияние [связанный с ним](https://code.claude.com/docs/ru/agent-view.md#pull-request-status)
* **Default**: `true`

```json ~/.claude.json theme={null}
{
  "prStatusFooterEnabled": false
}
```

Claude Code игнорирует этот ключ в `settings.json`.

### `teammateDefaultModel`

> [!WARNING]
>
> Удалено в v2.1.234 вместе с его строкой `/config` **Default teammate model**. Установка этого параметра не влияет на текущие версии.

До версии v2.1.233 вы устанавливали этот ключ на модель для товарищей по команде [агентской команды](https://code.claude.com/docs/ru/agent-teams.md#specify-teammates-and-models), для которых ваша подсказка не указала модель: псевдоним, такой как `"sonnet"`, или `null`, чтобы следовать модели лидера. Для модели, которую Claude Code выбирает для таких товарищей по команде сейчас, см. [укажите товарищей по команде и модели](https://code.claude.com/docs/ru/agent-teams.md#specify-teammates-and-models).

* **Scope**: [`Global config`](#scopes). На v2.1.233 и более ранних версиях.
* **Type**: string, псевдоним модели или полный ID модели, или `null`
* **Default**: unset

## См. также

* [Настройка разрешений](https://code.claude.com/docs/ru/permissions.md): синтаксис правил, режимы разрешений и доверие рабочей области
* [Переменные окружения](https://code.claude.com/docs/ru/env-vars.md): каждая переменная `CLAUDE_*`, `ANTHROPIC_*` и переменная поставщика, которую читает Claude Code
* [Инструменты, доступные Claude](https://code.claude.com/docs/ru/tools-reference.md): встроенные инструменты и какие требуют одобрения
* [Примеры файлов настроек](https://code.claude.com/docs/ru/settings-example.md): личный файл, командный файл и управляемый файл организации
* [Настройка управляемых параметров](https://code.claude.com/docs/ru/admin-setup.md): как организации решают, что применять
* [Развертывание управляемых параметров](https://code.claude.com/docs/ru/managed-settings.md): механизмы доставки, приоритет в управляемом уровне и недопустимые записи в управляемых параметрах
* [Отладка конфигурации](https://code.claude.com/docs/ru/debug-your-config.md): `claude doctor` и диалог ошибки параметров
