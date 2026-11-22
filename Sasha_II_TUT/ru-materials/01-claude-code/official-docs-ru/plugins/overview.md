> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор plugins

> Узнайте, что такое Claude Code plugin, когда вам нужен plugin вместо отдельного skill или MCP server, и какую страницу прочитать для установки или создания plugin.

Claude Code plugin — это директория skills, agents, hooks, MCP servers или других компонентов, которые Claude Code устанавливает и загружает как одну единицу. Большинство plugins поступают из marketplace, который представляет собой каталог, в котором перечислены plugins и указано, где получить каждый из них. Вы также можете загрузить plugin из папки, которую вам дал кто-то другой, или [создать свой собственный](https://code.claude.com/docs/ru/plugins/create.md).

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Вы используете чат claude.ai или Cowork, а не Claude Code**: см. [Плагины на claude.ai и в Cowork](https://claude.com/docs/plugins/overview)
> * **Вы создали MCP-сервер и хотите добавить его в каталог Anthropic**: см. [Публикация в каталоге](https://claude.com/docs/directory/publish)
> * **Вы хотите использовать Claude Code внутри VS Code или JetBrains IDE**: для этого служат расширение VS Code или плагин JetBrains, а не плагин Claude Code. См. [Использование Claude Code в VS Code](https://code.claude.com/docs/ru/vs-code.md) или [JetBrains IDE](https://code.claude.com/docs/ru/jetbrains.md)

Чтобы попробовать plugin прямо сейчас, запустите `/plugin` в сеансе терминала Claude Code и установите один из вкладки **Discover**, на которой перечислены plugins из ваших marketplaces. Оттуда:

* [Установка и управление plugins](https://code.claude.com/docs/ru/plugins/install.md): полные шаги установки, области действия и другие поверхности
* [Создание plugin](https://code.claude.com/docs/ru/plugins/create.md): создайте свой собственный
* [Решите, нужен ли вам plugin](#decide-whether-you-need-a-plugin): является ли plugin правильным инструментом для того, что вы хотите

## Поймите, что такое plugin

Plugin — это директория компонентов, обычно с манифестом. Манифест, JSON-файл в `.claude-plugin/plugin.json`, дает plugin его имя и может добавить версию, описание и другие [метаданные](https://code.claude.com/docs/ru/plugins/manifest-reference.md). Компоненты — это то, что plugin добавляет в Claude Code, например:

* [**Skills**](https://code.claude.com/docs/ru/plugins/components.md#skills): инструкции `SKILL.md`, которые Claude загружает при необходимости, и которые вы также можете запустить как команду
* [**Agents**](https://code.claude.com/docs/ru/plugins/components.md#agents): определения подагентов, которым Claude может делегировать
* [**Hooks**](https://code.claude.com/docs/ru/plugins/components.md#hooks): команды, которые Claude Code запускает в точках своего жизненного цикла, например после каждого редактирования
* [**Модуль хуков**](https://code.claude.com/docs/ru/plugins/mods/overview.md): хуки, написанные как функции JavaScript, которые также могут рисовать панели и добавлять команды. Плагин, в котором он есть, называется модом. Некоторые моды [встроены в Claude Code](https://code.claude.com/docs/ru/plugins/mods/overview.md#mods-built-into-claude-code).
* [**MCP servers**](https://code.claude.com/docs/ru/plugins/components.md#mcp-servers): серверы инструментов, к которым Claude Code подключается, пока plugin включен

На этой диаграмме показан plugin с именем `my-plugin`, который содержит skill, agent, hooks и MCP server, и что вы получаете от каждого файла после загрузки plugin.

![Диаграмма в двух столбцах, соединенных пятью прямыми стрелками. Слева — директория plugin с именем my-plugin, содержащая манифест в .claude-plugin/plugin.json, skills/review/SKILL.md, agents/reviewer.md, hooks/hooks.json, .mcp.json и другие компоненты. Справа — то, что каждый файл дает вам в вашем сеансе: манифест устанавливает имя plugin, my-plugin; skill запускается как /my-plugin:review; файл agent — это подагент, которому Claude может делегировать; файл hooks содержит hooks, которые запускаются на событиях жизненного цикла; и .mcp.json добавляет MCP server, который дает Claude инструменты.](https://mintcdn.com/claude-code/2Q_GtOEovg5qaBem/images/plugin-directory.svg?fit=max\&auto=format\&n=2Q_GtOEovg5qaBem\&q=85\&s=f623b64e82713b830e48174f0a922888)

Типы компонентов, которые может содержать плагин, с примером каждого см. в разделе [Компоненты плагинов](https://code.claude.com/docs/ru/plugins/components.md). Чтобы увидеть, где находится каждая часть в директории плагина, используйте [обозреватель плагина](https://code.claude.com/docs/ru/plugins/components.md#explore-the-plugin-directory) на этой странице.

### Решите, нужен ли вам plugin

Skills, подагенты, hooks и MCP servers работают самостоятельно, без plugin. Skill, который вы сохраняете в `~/.claude/skills/`, например, доступен в каждом проекте на вашем компьютере. Чтобы установить один самостоятельно, см. [Skills](https://code.claude.com/docs/ru/skills.md), [Subagents](https://code.claude.com/docs/ru/sub-agents.md), [Hooks](https://code.claude.com/docs/ru/hooks-guide.md) или [MCP](https://code.claude.com/docs/ru/mcp.md).

Используйте plugin, когда вы хотите упаковать несколько skills, подагентов, hooks или MCP servers как одну единицу. Установите один, чтобы получить настройку, которую создал кто-то другой, с одной командой и обновлениями из его marketplace. Создайте один, чтобы дать вашу собственную настройку товарищам по команде, установить его во многих проектах или опубликовать версионные релизы.

### Что включенный plugin добавляет в ваши сеансы

Включенный plugin является частью каждого сеанса, а не только сеансов, в которых вы его используете. Это имеет несколько последствий, о которых стоит знать перед установкой:

* **Контекст и использование**: для каждого skill, agent и команды, которые [Claude может вызвать самостоятельно](https://code.claude.com/docs/ru/skills.md#control-who-invokes-a-skill), имя и описание находятся в контексте Claude на каждом ходу, чтобы Claude знал об их существовании. Эти токены учитываются в вашем использовании и оставляют меньше места в [контекстном окне](https://code.claude.com/docs/ru/context-window.md) даже в сеансах, где ничего из plugin не запускается. Полный текст skill или agent загружается только при его использовании. То, что MCP servers plugin добавляют за ход, следует [MCP tool search](https://code.claude.com/docs/ru/mcp.md#scale-with-mcp-tool-search).
* **Процессы**: MCP servers, которые определяет plugin, работают параллельно с каждым сеансом, в котором он включен, и его hooks срабатывают при их событиях.
* **Разрешения**: то, что запускает plugin, запускается от вас. См. [Plugin security and trust](https://code.claude.com/docs/ru/plugins/security.md) для того, что нужно проверить в первую очередь.

Вы можете проверить отпечаток plugin на каждом этапе:

* **Перед установкой**: откройте plugin из вкладки **Marketplaces** в `/plugin`. Plugins в официальном marketplace Anthropic показывают там оценку **Context cost**.
* **После установки**: [Measure what a plugin costs](https://code.claude.com/docs/ru/plugins/measure.md#measure-what-a-plugin-costs) показывает, как прочитать отпечаток plugin, и группа **Not used recently** вкладки **Installed** перечисляет plugins, которые вы можете отключить.
* **Чтобы остановить его без удаления**: отключите plugin с помощью `/plugin` или в вашей оболочке `claude plugin disable`. См. [Manage installed plugins](https://code.claude.com/docs/ru/plugins/install.md#manage-installed-plugins).

## Получайте plugins из marketplace

Marketplace — это репозиторий или директория с файлом `.claude-plugin/marketplace.json`, который перечисляет plugins и указывает, где получить каждый из них. Это каталог, а не размещенный магазин. Вы добавляете marketplace один раз, затем устанавливаете plugins из него по имени, например `commit-commands@claude-plugins-official`.

> [!NOTE]
>
> Marketplace plugin — это не [Claude Marketplace](https://claude.com/marketplace). Claude Marketplace — это веб-сайт на claude.com/marketplace, где вы просматриваете plugins, connectors, партнерские продукты и партнеров услуг. Это не marketplace, который вы добавляете с помощью `/plugin marketplace add`.

Claude Code добавляет официальный маркетплейс Anthropic при первом запуске интерактивной сессии в терминале, если это не блокирует [управляемая политика](https://code.claude.com/docs/ru/plugins/org.md#allow-the-official-marketplace-and-your-own). Claude Code не добавляет маркетплейс сообщества Anthropic самостоятельно. Чтобы различать маркетплейсы Anthropic, прочитайте [Маркетплейсы Anthropic](https://code.claude.com/docs/ru/plugins/anthropic-marketplaces.md). Чтобы увидеть, что перечисляет официальный маркетплейс, откройте вкладку **Discover** в `/plugin` в сессии или просмотрите [Claude Marketplace](https://claude.com/marketplace/plugins).

На этой диаграмме показан путь от marketplace к вашему сеансу. Marketplace перечисляет plugin, вы устанавливаете этот plugin, и Claude Code загружает его компоненты.

![Диаграмма пути marketplace в трех ящиках, слева направо. Marketplace, каталог plugins, перечисляет plugin. Plugin — это одна директория, установленная как единица, содержащая skills, agents, hooks, MCP servers и другие компоненты. Вы устанавливаете plugin в Claude Code, который загружает его компоненты.](https://mintcdn.com/claude-code/2Q_GtOEovg5qaBem/images/plugins-model.svg?fit=max\&auto=format\&n=2Q_GtOEovg5qaBem\&q=85\&s=4196344954b7c2e27fc0bd6a9a1113a1)

[Install and manage plugins](https://code.claude.com/docs/ru/plugins/install.md#install-a-plugin) содержит шаги установки для каждого места, где вы запускаете Claude Code. Пока вы разрабатываете plugin, вам не нужен marketplace: загружайте его прямо из его папки с помощью `--plugin-dir`, как показано в [Develop without a marketplace](https://code.claude.com/docs/ru/plugins/create.md#develop-without-a-marketplace).

### Сделайте установленный plugin доступным в вашем сеансе

Прежде чем plugin, который вы установили, даст вам skill, который вы можете запустить, он должен присутствовать на каждом из этих уровней:

* **Settings**: ваши settings перечисляют marketplaces, которые вы добавили, и plugins, которые включены.
* **Disk**: `~/.claude/plugins/` содержит то, что Claude Code загрузил и установил.
* **Session**: plugins загружаются при запуске или когда вы [reload plugins](https://code.claude.com/docs/ru/plugins/loading.md#check-which-stage-a-plugin-reached).

Прочитайте [Plugin loading reference](https://code.claude.com/docs/ru/plugins/loading.md) для правил на каждом уровне, включая то, какой файл settings имеет приоритет и где находятся файлы на диске.

## Отличайте marketplace Anthropic от marketplace третьих сторон

Имя marketplace помещает его в один из трех уровней. Claude Code принимает официальные и community имена только для marketplaces, полученных из репозиториев `github.com/anthropics/`:

* **Официальные**: маркетплейсы с одним из [официальных имён маркетплейсов](https://code.claude.com/docs/ru/plugins/security.md#official-marketplace-names) Anthropic, включая `claude-plugins-official` и `claude-code-plugins`.
* **Community**: marketplaces с одним из community имен Anthropic, например `claude-community`. [Identify Anthropic's marketplaces by name](https://code.claude.com/docs/ru/plugins/security.md#marketplace-tiers) их перечисляет.
* **Third-party**: все остальные marketplaces. Marketplace, который публикует ваш коллега или ваша организация, является third-party.

Независимо от уровня, plugin, который вы устанавливаете, может запускать код с вашими привилегиями пользователя. Прочитайте [Plugin security and trust](https://code.claude.com/docs/ru/plugins/security.md) для того, как проверить plugin перед его установкой.

Через [managed settings](https://code.claude.com/docs/ru/settings.md#settings-files) организация может добавить в список разрешений или заблокировать marketplaces, принудительно установить plugins и отключить загрузку только для сеанса. Прочитайте [Manage plugins for your organization](https://code.claude.com/docs/ru/plugins/org.md) для этих элементов управления.

## Поймите области действия установки

Когда вы устанавливаете plugin, вы выбираете область действия, и область действия определяет, для кого включен plugin:

* **User scope**: включен для вас в каждом проекте на этом компьютере
* **Project scope**: включен для всех, кто работает в этом репозитории, через committed `.claude/settings.json`. Каждый сотрудник все еще [устанавливает его на своей машине](https://code.claude.com/docs/ru/plugins/loading.md#enabled-in-project-settings-but-not-installed)
* **Local scope**: включен для вас только в этом репозитории

Plugin, который вы устанавливаете в области действия пользователя в терминале, локальных сеансах настольного приложения или расширении VS Code, доступен в двух других на этом компьютере, потому что все три читают одни и те же файлы settings. См. [Choose an install scope](https://code.claude.com/docs/ru/plugins/install.md#choose-an-install-scope) для того, как выбрать один.

Облачный сеанс, включая сеанс в браузере на claude.ai/code, не загружает plugins в ваши локальные settings. Для шагов установки в терминале, VS Code и настольном приложении, а также для того, что загружает облачный сеанс, см. [Install a plugin](https://code.claude.com/docs/ru/plugins/install.md#install-a-plugin).

> [!NOTE]
>
> Тот же формат plugin также устанавливается на claude.ai и в Cowork, где загружается другой набор компонентов. Для этих поверхностей см. [Plugins на claude.ai и в Cowork](https://claude.com/docs/plugins/overview) на claude.com и его [таблицу поддержки компонентов](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app).

## Следующие шаги

Большинство людей начинают с установки plugin из официального marketplace Anthropic, который Claude Code добавляет при первом запуске интерактивного сеанса терминала. Запустите `/plugin` в сеансе терминала для его просмотра или следуйте [Install and manage plugins](https://code.claude.com/docs/ru/plugins/install.md), который также охватывает настольное приложение и VS Code. Чтобы увидеть, что находится в этом marketplace перед открытием Claude Code, просмотрите [Claude Marketplace](https://claude.com/marketplace/plugins) в Интернете.

Чтобы создать свой собственный, [Create a plugin](https://code.claude.com/docs/ru/plugins/create.md) начинается с пустой директории и заканчивается рабочим plugin.

После установки или создания plugin эти страницы охватывают то, что дальше:

* **Поделитесь тем, что вы создали**: [Publish and distribute a plugin](https://code.claude.com/docs/ru/plugins/publish.md), через ваш собственный marketplace или [Anthropic's directory](https://code.claude.com/docs/ru/plugins/publish.md#submit-to-anthropics-directory)
* **Проверьте, работает ли он и используется ли**: [Test plugins with evals](https://code.claude.com/docs/ru/plugin-evals.md) и [Measure plugin cost and usage](https://code.claude.com/docs/ru/plugins/measure.md)
* **Запустите marketplace для вашей команды**: [Create a marketplace](https://code.claude.com/docs/ru/plugins/create-marketplace.md), затем [Host and maintain a marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md)
* **Установите политику plugin для организации**: [Manage plugins for your organization](https://code.claude.com/docs/ru/plugins/org.md)
* **Исправьте проблему**: [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md)
