> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Установка и управление плагинами

> Установите плагины Claude Code из маркетплейса на любой поверхности, которую вы используете, выберите область установки и обновляйте или удаляйте их позже.

Установка плагина добавляет его skills, agents, hooks и MCP серверы в Claude Code на вашу машину.

Эта страница предназначена для всех, кто использует плагины на своей машине или аккаунте, будь то в терминале, настольном приложении, IDE или облачной сессии: она охватывает установку, выбор области, добавление маркетплейсов и поддержание плагинов в актуальном состоянии.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Вы используете claude.ai chat или Cowork, а не Claude Code**: см. [Плагины на claude.ai и в Cowork](https://claude.com/docs/plugins/overview)
> * **Claude Code вывел ошибку**: найдите её в [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md)

Начните с [Установка плагина](#install-a-plugin). Если кто-то отправил вам команду установки, чьё имя `@` не является `claude-plugins-official`, сначала [добавьте этот маркетплейс](#add-a-marketplace).

## Установка плагина

В качестве примера этот раздел устанавливает [`commit-commands`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) из [официального маркетплейса Anthropic](https://code.claude.com/docs/ru/plugins/anthropic-marketplaces.md), который добавляет команды для коммитов, пушей и открытия pull requests.

Те же шаги устанавливают любой другой плагин: замените его имя и имя его маркетплейса везде, где появляются `commit-commands` и `claude-plugins-official`. Если этот плагин поступает из другого маркетплейса, сначала [добавьте маркетплейс](#add-a-marketplace).

Выберите вкладку для того места, где вы запускаете Claude Code.

> [tab] Terminal
>
> Запустите Claude Code с помощью `claude` в вашем проекте, затем:
>
> **1. Откройте детали плагина с помощью команды установки**
>
> Запустите `/plugin install` с именем плагина и маркетплейса. В сессии эта команда не устанавливает сразу: она открывает панель `/plugin` с деталями этого плагина, чтобы вы могли его просмотреть и сначала выбрать область.
>
> ```text theme={null}
> /plugin install commit-commands@claude-plugins-official
> ```
>
> Чтобы вместо этого просмотреть список, запустите `/plugin` без имени плагина: панель откроется на вкладке **Discover**, которая перечисляет плагины из ваших маркетплейсов, и вы можете вводить для поиска, затем нажать **Enter** на плагине, чтобы открыть его детали.
>
> **2. Просмотрите, что добавляет плагин**
>
> Панель деталей показывает описание плагина. Она также может показывать:
>
> * **Will install**: команды, agents, skills, hooks и MCP и LSP серверы, которые добавляет плагин.
> * **Last updated**: показывается для плагина в официальном маркетплейсе Anthropic.
> * **Context cost**: для плагина в официальном маркетплейсе Anthropic две оценки токенов. **Every turn** — это то, что плагин добавляет к каждому отправляемому вами сообщению, а **When invoked** — это то, что его skills и agents добавляют после того, как Claude их загружает. Оценки появляются, когда вы открываете плагин, назвав его маркетплейс, как это делает команда шага 1, или со вкладки **Marketplaces**. Панель деталей, которую вы достигаете из списка **Discover**, их не показывает.
>
> Плагины из локального или пользовательского маркетплейса могут вместо этого показывать `Components will be discovered at installation`.
>
> Плагин может запускать hooks и MCP серверы, поэтому прочитайте панель перед установкой. См. [Plugin security and trust](https://code.claude.com/docs/ru/plugins/security.md).
>
> **3. Выберите область**
>
> Выберите один из трёх вариантов установки:
>
> * **Install for you (user scope)**: вы получаете плагин в каждом проекте на этой машине
> * **Install for all collaborators on this repository (project scope)**: он включен для всех, кто работает в этом репозитории
> * **Install for you, in this repo only (local scope)**: вы получаете его только в этом репозитории
>
> [Выберите область установки](#choose-an-install-scope) говорит, в какой файл настроек записывается каждый из них и какой применяется, когда один и тот же плагин установлен в нескольких местах.
>
> После выбора области Claude Code устанавливает плагин вместе с любыми зависимостями, которые он объявляет, затем выводит сводку установки.
>
> **4. Прочитайте сводку установки**
>
> Последнее предложение сводки говорит вам, доступен ли плагин в этой сессии прямо сейчас:
>
> * **Active now**: `Plugin is now active.` Перезагрузка не требуется.
> * **Active, but a server needs setup**: `Plugin is now active.` сопровождается `Its bundled MCP server needs configuration before it can start`. [Bundled MCP server](https://code.claude.com/docs/ru/plugins/components.md#include-a-packaged-mcpb-server) плагина не может запуститься, пока вы не зададите его параметры. Выберите плагин на вкладке **Installed** в `/plugin` и выберите **Configure**, чтобы задать параметры сервера.
> * **Reload needed**: `Run /reload-plugins to apply.` Панель закрывается, и Claude Code запускает эту перезагрузку для вас. Если перезагрузка [инвалидирует кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md#enabling-or-disabling-a-plugin), она предупреждает и вместо этого оставляет плагин в ожидании. Запустите `/reload-plugins --force`, чтобы активировать его в любом случае, что стоит один некэшированный запрос.
> * **Load failed**: `The plugin couldn't be loaded`. Откройте вкладку **Errors** в `/plugin`, чтобы узнать причину, затем см. [After install: plugin not working](https://code.claude.com/docs/ru/plugins/troubleshooting.md#plugin-installed-but-not-working).
>
> **5. Подтвердите, что плагин работает**
>
> Введите `/` и найдите скиллы плагина под его именем в форме `/<plugin>:<skill>`. Для `commit-commands` появляется `/commit-commands:commit`. Два других места также перечисляют плагин:
>
> * Откройте вкладку **Installed** в `/plugin`, которая перечисляет плагин с его областью.
> * В вашей оболочке запустите `claude plugin list`, который выводит тот же список с строками `Version`, `Scope` и `Status`.
>
> Если `/commit-commands:commit` не появляется, см. [After install: plugin not working](https://code.claude.com/docs/ru/plugins/troubleshooting.md#plugin-installed-but-not-working).
>
> Установка из любого другого маркетплейса требует одного дополнительного шага: [добавьте маркетплейс](#add-a-marketplace). Claude Code добавляет официальный маркетплейс Anthropic для вас в первый раз, когда вы запускаете интерактивную сессию терминала, поэтому пример пропускает этот шаг. Если вы нашли плагин на [claude.com/marketplace](https://claude.com/marketplace), его кнопка **Claude Code** копирует команду установки в её [форме оболочки](#install-from-your-shell), `claude plugin install <name>@claude-plugins-official`.

> [tab] Desktop app
>
> В локальной или SSH сессии на вкладке **Code** настольного приложения:
>
> **1. Откройте браузер плагинов**
>
> Нажмите кнопку **+** рядом с полем промпта и выберите **Add plugins**. Если в меню **+** отображается **Plugins** вместо **Add plugins**, выберите **Plugins**, затем **Browse plugins**. Если **Browse plugins** отсутствует, выберите **Manage plugins**. Браузер плагинов откроется с плагинами из ваших маркетплейсов.
>
> **2. Выберите плагин**
>
> Найдите `commit-commands` и выберите его.
>
> **3. Выберите область действия**
>
> Выберите [область действия](#choose-an-install-scope): ваш пользовательский аккаунт, этот проект или только локально.
>
> Чтобы позже включить, отключить или удалить плагин, см. [Install plugins in the desktop app](https://code.claude.com/docs/ru/desktop.md#install-plugins).

> [tab] VS Code
>
> На панели Claude Code в VS Code:
>
> **1. Откройте Manage plugins**
>
> Введите `/plugins` в поле подсказки, чтобы открыть **Manage plugins**.
>
> **2. Установите плагин**
>
> На вкладке **Plugins** найдите `commit-commands` и нажмите **Install**. Если вкладка не перечисляет плагины, сначала добавьте `anthropics/claude-plugins-official` на вкладке **Marketplaces**.
>
> **3. Выберите область**
>
> Выберите [область](#choose-an-install-scope): **Install for you**, **Install for this project** или **Install locally**.
>
> Ваши изменения применяются к открытым сессиям без перезагрузки. См. [Manage plugins in VS Code](https://code.claude.com/docs/ru/vs-code.md#manage-plugins).

> [tab] Cloud session
>
> [Облачная сессия](https://code.claude.com/docs/ru/cloud-environments.md), включая [браузер на claude.ai/code](https://code.claude.com/docs/ru/claude-code-on-the-web.md), не имеет браузера плагинов и не загружает плагины, которые вы установили на своей машине, или те, которые включены в `.claude/settings.json` вашего репозитория. Для плагинов, которые ваша организация распространяет через управляемые настройки, см. [Manage plugins for your organization](https://code.claude.com/docs/ru/plugins/org.md).
>
> См. [какие части вашей настройки также доступны в облачной сессии](https://code.claude.com/docs/ru/cloud-environments.md#what-carries-over-from-your-setup) для остальной части вашей настройки.

### Выберите область установки

Область установки плагина определяет, кто получает плагин и какой файл настроек записывает его как включённый:

* **User scope**: плагин включен для вас в каждом проекте на этой машине. Запись идёт в `enabledPlugins` в `~/.claude/settings.json`.
* **Project scope**: плагин включен для всех, кто работает в этом репозитории. Запись идёт в `.claude/settings.json`, который вы коммитите. Коммит этой записи включает плагин для ваших соавторов, но не загружает его на их машины. Каждый соавтор также один раз для каждого клона запускает `claude plugin install <name>@<marketplace> --scope project`; см. [Enabled in project settings but not installed](https://code.claude.com/docs/ru/plugins/loading.md#enabled-in-project-settings-but-not-installed).
* **Local scope**: плагин включен для вас только в этом репозитории. Запись идёт в `.claude/settings.local.json`.

Некоторые плагины установлены их автором на запуск в отключённом состоянии через поле [`defaultEnabled`](https://code.claude.com/docs/ru/plugins/manifest-reference#defaultenabled). Такой плагин установлен, но остаётся отключённым, пока вы не включите его с помощью `claude plugin enable <name>` в вашей оболочке или со вкладки **Installed** в `/plugin` в сессии.

Когда один и тот же плагин установлен в нескольких областях, локальная настройка переопределяет настройку проекта, а настройка проекта переопределяет пользовательскую настройку. См. [Find where a plugin is enabled](https://code.claude.com/docs/ru/plugins/loading.md#find-where-a-plugin-is-enabled) для полного правила.

Терминал, локальные сессии настольного приложения и расширение VS Code на одном компьютере читают одни и те же файлы настроек, поэтому плагин, который вы устанавливаете в пользовательской области в любом из них, доступен в двух других.

### JetBrains, неинтерактивные запуски и Agent SDK

Некоторые места, где вы запускаете Claude Code, не имеют собственного браузера плагинов:

* **JetBrains IDEs**: плагин JetBrains запускает Claude Code в терминале IDE, поэтому используйте шаги вкладки **Terminal** там.
* **`claude -p` и другие неинтерактивные запуски**: `/plugin` не запускается, и Claude отвечает `/plugin isn't available in this environment.` Плагины, которые вы уже установили, загружаются. Устанавливайте и управляйте ими из вашей оболочки с помощью [`claude plugin` команд](#install-from-your-shell).
* **Agent SDK**: загружайте плагины через опцию плагина SDK. См. [Load plugins in the Agent SDK](https://code.claude.com/docs/ru/agent-sdk/plugins.md).

Если Claude Code сообщает, что плагин, включённый в `.claude/settings.json` репозитория, не установлен, см. [Enabled in project settings but not installed](https://code.claude.com/docs/ru/plugins/loading.md#enabled-in-project-settings-but-not-installed).

> [!TIP]
>
> Если вы автор плагина, тестирующий копию вашего плагина на диске, запустите Claude Code из вашей оболочки с `--plugin-dir`, чтобы загрузить его для одной сессии вместо установки. См. [Flags that load a plugin for one session](https://code.claude.com/docs/ru/plugins/cli-reference.md#flags-that-load-a-plugin-for-one-session).

### Плагины из вашего аккаунта claude.ai

Ваш аккаунт claude.ai — это отдельный источник плагинов, наряду с маркетплейсами, из которых вы устанавливаете:

* **Что приходит**: каждый плагин, который вы включаете для своего аккаунта claude.ai, и каждый плагин, который ваша организация включает для своих членов. В сессии терминала они синхронизируются в фоне каждый раз, когда вы запускаете Claude Code, подписавшись с этим аккаунтом; в сессиях Cowork они загружаются при запуске сессии.
* **Где вы их видите**: в `/plugin` и `claude plugin list` под ID `<name>@synced`. Вы можете отключить один в своей области, если ваша организация этого не требует.
* **Что не идёт в другую сторону**: плагины, которые вы устанавливаете с помощью `/plugin` или `claude plugin install`, остаются на этой машине и не добавляются в ваш аккаунт claude.ai.

Для синхронизации времени, требований входа и отключения синхронизации см. [Plugins synced from claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins).

### Установка из вашей оболочки

Запустите `claude plugin install` в вашей оболочке, чтобы установить плагин без запуска сессии Claude Code, например из скрипта настройки.

* **Область**: пользовательская область по умолчанию. Передайте `--scope project` или `--scope local`, чтобы изменить её.
* **Когда плагины загружаются**: плагины, которые он устанавливает, загружаются в следующий раз, когда вы запускаете Claude Code, или когда вы запускаете `/reload-plugins` в уже открытой сессии.
* **Маркетплейс на новой машине**: на машине, где никто ещё не открывал интерактивную сессию Claude Code, официальный маркетплейс не зарегистрирован, поэтому скрипт, который устанавливает из него, запускает `claude plugin marketplace add anthropics/claude-plugins-official` перед установкой. См. [Add and install from your shell](#add-and-install-from-your-shell).

```bash theme={null}
claude plugin install formatter@your-org --scope project
```

Команда выводит `Successfully installed plugin: formatter@your-org (scope: project)` при завершении.

Некоторые плагины устанавливаются путём запуска команды, которую называет их маркетплейс, называемой [`command` source](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source). Claude Code показывает вам эту команду и просит вас принять её перед запуском. Скрипт не имеет никого, кто ответит на этот запрос, поэтому передайте `--yes` там, чтобы принять его.

Остальные флаги `claude plugin install` см. в [plugin install](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-install).

## Добавление маркетплейса

Вам нужен этот раздел только когда плагин, который вы хотите, не находится в официальном маркетплейсе Anthropic, например один, который опубликовал коллега, или один из маркетплейса сообщества Anthropic.

Маркетплейс — это каталог плагинов, и Claude Code должен знать о маркетплейсе, прежде чем вы сможете установить из него. Вы добавляете маркетплейс один раз. После этого его плагины появляются на вкладке **Discover** и устанавливаются с помощью `/plugin install <plugin>@<marketplace>` в сессии или `claude plugin install <plugin>@<marketplace>` в вашей оболочке, где `<marketplace>` — это имя, под которым маркетплейс зарегистрирован. Чтобы сделать оба в один шаг, см. [Add a marketplace and install in one command](#add-a-marketplace-and-install-in-one-command).

В сессии Claude Code запустите `/plugin marketplace add`, за которым следует источник маркетплейса: репозиторий GitHub, репозиторий git на любом хосте, локальный каталог или файл, или размещённый `marketplace.json`.

| Источник | Что вы вводите | Пример |
| :- | :- | :- |
| Репозиторий GitHub | `owner/repo`. Добавьте `#ref`, чтобы закрепить ветку или тег. | `/plugin marketplace add anthropics/claude-plugins-official`, или `/plugin marketplace add your-org/plugins#v1.2.0`, чтобы закрепить тег `v1.2.0` |
| Репозиторий Git на любом хосте | Полный URL клонирования. Добавьте `#ref`, чтобы закрепить ветку или тег. | `/plugin marketplace add https://gitlab.example.com/your-group/your-marketplace.git#v1.0.0` |
| Локальный каталог или файл | Относительный или абсолютный путь к каталогу, который содержит `.claude-plugin/marketplace.json`, или к самому JSON файлу. Начните относительный путь с `./` или `../`, потому что Claude Code читает голый `name/name` как репозиторий GitHub. | `/plugin marketplace add ./my-marketplace` |
| Размещённый `marketplace.json` | Его URL `https://` | `/plugin marketplace add https://example.com/marketplace.json` |

Из вашей оболочки `claude plugin marketplace add` принимает те же источники.

> [!TIP]
>
> `/plugin market` также работает как более короткая форма `/plugin marketplace`.

Включайте префикс `https://` на каждый URL или используйте форму `git@host:path` для SSH. Если вы введёте голый `gitlab.example.com/your-group/your-marketplace.git`, Claude Code прочитает его как сокращение GitHub `owner/repo` и отклонит его.

Когда команда успешна, она выводит `Successfully added marketplace: <name>`, и плагины маркетплейса появляются на вкладке **Discover** в следующий раз, когда вы откроете `/plugin`, без необходимости перезагрузки. Если она не удаётся, сопоставьте сообщение об ошибке в [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md#add-a-marketplace).

### Добавление маркетплейса и установка в одной команде

Чтобы установить плагин из маркетплейса, который вы ещё не добавили, назовите источник маркетплейса с помощью `--marketplace` в команде установки — в сессии или из вашей оболочки. Источник принимает [те же формы, что и `/plugin marketplace add`](#add-a-marketplace), такие как GitHub `owner/repo`, URL git или локальный путь. Дайте имя плагина само по себе, без суффикса `@marketplace`.

#### Добавление и установка в сессии

Запустите `/plugin install` в сессии Claude Code с плагином и источником. Требуется Claude Code v2.1.275 или позже. В сессии источник не может содержать пробелы.

```text theme={null}
/plugin install deploy-helper --marketplace your-org/plugins
```

Если вы ещё не добавили этот маркетплейс, Claude Code показывает разрешённый источник и просит вас подтвердить перед добавлением. После добавления маркетплейса детали плагина открываются и вы выбираете [область установки](#install-a-plugin). Если источник совпадает с маркетплейсом, который вы уже добавили, Claude Code пропускает подтверждение и открывает детали плагина в этом маркетплейсе.

#### Добавление и установка из оболочки

В вашей оболочке, не запуская сессию, запустите `claude plugin install` с плагином и источником. Требуется Claude Code v2.1.292 или позже.

```bash theme={null}
claude plugin install deploy-helper --marketplace your-org/plugins
```

Команда оболочки добавляет маркетплейс без шага подтверждения. Маркетплейс, который вы уже добавили из этого источника, используется повторно. Новый добавляется с теми же [проверками политики организации](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install), что и `claude plugin marketplace add`, и объявляется в ваших пользовательских настройках, даже если вы передаёте `--scope project`.

Если вы ещё не добавили этот маркетплейс, команда выводит `Successfully added marketplace: <name> (declared in user settings)`, а затем [устанавливает плагин](#install-from-your-shell).

### Добавление приватного маркетплейса

Приватный маркетплейс — это один в репозитории, для которого вам нужны учётные данные для клонирования, на GitHub или любом другом хосте git. Вы добавляете его с помощью той же команды `/plugin marketplace add` или `claude plugin marketplace add`, что и публичный. Claude Code клонирует его с учётными данными git, уже находящимися на вашей машине, и никогда не запрашивает, поэтому каждый способ подключения имеет требование:

* **HTTPS**: применяются ваши помощники учётных данных git, поэтому доступ, который вы установили с помощью `gh auth login`, macOS Keychain или `git-credential-store`, работает. Запросы git и программы askpass отключены, включая заданную в `GIT_ASKPASS`, поэтому клонирование завершается с ошибкой вместо запроса, когда git пришлось бы запросить учётные данные.
* **SSH**: хост должен уже находиться в вашем файле `known_hosts` и ключ должен работать без запроса парольной фразы. Если ваша настройка git называет программу SSH в `GIT_SSH_COMMAND`, `GIT_SSH` или `core.sshCommand` конфигурации git, Claude Code запускает эту программу.
* **Сокращение GitHub `owner/repo`**: Claude Code проверяет, аутентифицирует ли ваш ключ SSH на `github.com`, затем клонирует по SSH, если это так, и по HTTPS, если нет. Установите [`CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`](https://code.claude.com/docs/ru/env-vars#variables), чтобы пропустить эту проверку и всегда клонировать по HTTPS.

Те же учётные данные применяются, когда вы запускаете `/plugin install`, `/plugin marketplace update` и `claude plugin update`.

На хосте GitHub Enterprise Server см. [Plugin marketplaces on GHES](https://code.claude.com/docs/ru/github-enterprise-server.md#plugin-marketplaces-on-ghes) для учётных данных, которые требует каждая операция.

Если ваша организация регистрирует маркетплейс для вас через управляемые настройки, вы не добавляете его сами. См. [Pre-install and require plugins](https://code.claude.com/docs/ru/plugins/org.md#pre-install-and-require-plugins).

### Добавление маркетплейса из claude.ai

В сессиях терминала, где [плагины синхронизируются из вашего аккаунта claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), claude.ai также может перечислять маркетплейсы плагинов для вас, такие как библиотека плагинов вашей организации и ваши собственные загрузки claude.ai. Вы добавляете один из них по его имени, а не по источнику. Добавление маркетплейса из claude.ai требует Claude Code v2.1.273 или позже.

Добавьте маркетплейс claude.ai из панели `/plugin` или из вашей оболочки:

* **Внутри сессии**: запустите `/plugin` и перейдите на вкладку **Marketplaces**, которая перечисляет маркетплейсы из claude.ai. Выберите один там, чтобы добавить его.
* **Из вашей оболочки**: запустите `claude plugin marketplace list`, который выводит их в разделе `From claude.ai:`. Затем запустите `claude plugin marketplace add` с флагом `--claudeai` и именем, показанным в списке.

Например, эта команда добавляет маркетплейс с именем `claudeai-organization-library`:

```bash theme={null}
claude plugin marketplace add --claudeai claudeai-organization-library
```

Claude Code регистрирует маркетплейс под локальным именем, которое начинается с `claudeai-`, полученным из имени, которое claude.ai перечисляет под ним. Например, маркетплейс, перечисленный как "Organization library", становится `claudeai-organization-library`. Устанавливайте его плагины по этому имени, например с помощью `claude plugin install <plugin>@claudeai-organization-library`.

Если вы выходите или входите в другую организацию claude.ai, маркетплейс остаётся настроенным, но не показывает плагины, и плагины, которые вы уже установили из него, продолжают загружаться.

Раздел `From claude.ai:` также может перечислять маркетплейсы на основе git, общие через claude.ai, и выводит источник для каждого из них. Добавляйте их по этому источнику, как в [Add a marketplace](#add-a-marketplace), а не с `--claudeai`.

## Управление установленными плагинами

Вкладка **Installed** в `/plugin` перечисляет ваши плагины с действиями для включения, отключения, обновления или удаления каждого. В сессии Claude Code запустите `/plugin` и нажмите **Tab**, чтобы достичь её, или запустите `/plugin enable`, `/plugin disable` или `/plugin uninstall`, чтобы открыть панель и сделать это изменение там. Отключённые плагины сгруппированы под свёрнутым заголовком в нижней части списка. Используйте эти клавиши на списке:

* Введите для фильтрации по имени или описанию.
* Нажмите **Space**, чтобы включить или отключить выбранный плагин, и **f**, чтобы добавить его в избранное.
* Нажмите **Enter**, чтобы открыть детали плагина.

Меню деталей плагина предлагает **Disable plugin** или **Enable plugin**, **Update now** и **Uninstall**. Для плагинов, которые принимают настройки, появляются ещё два элемента, и плагин может показать оба:

* **Configure options**: показывается, когда манифест плагина объявляет [параметры `userConfig`](https://code.claude.com/docs/ru/plugins/manifest-reference#user-configuration). Открывает диалог для этих параметров
* **Configure**: показывается, когда плагин включает [упакованный MCP сервер](https://code.claude.com/docs/ru/plugins/components.md#include-a-packaged-mcpb-server). Устанавливает собственные параметры `user_config` этого сервера

Вкладка также может показывать плагины в области **Managed**. Ваша организация установила их через [управляемые настройки](https://code.claude.com/docs/ru/settings.md#settings-files), и вы не можете включить, отключить или удалить их здесь.

Для синхронизированного плагина, который ваша организация требует на claude.ai, см. [Manage plugins synced from claude.ai](#manage-plugins-synced-from-claude-ai).

Когда вы закрываете панель `/plugin` с ожидающими изменениями, которые вы сделали в ней, Claude Code запускает `/reload-plugins` для вас, чтобы применить их. Если перезагрузка [инвалидирует кэш подсказок](https://code.claude.com/docs/ru/prompt-caching.md#enabling-or-disabling-a-plugin), она предупреждает и оставляет изменения в ожидании. Запустите `/reload-plugins --force`, чтобы применить их в любом случае.

### Управление плагинами, синхронизированными из claude.ai

Вкладка **Installed** в `/plugin` также перечисляет [плагины, синхронизированные из вашего аккаунта claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), с `synced` в качестве их источника. Синхронизированные плагины появляются в сессиях терминала на Claude Code v2.1.273 или позже.

* **Включить или отключить**: используйте вкладку **Installed**, если ваша организация не отметила плагин как обязательный.
* **Удалить**: отключите плагин на claude.ai.

Когда Claude Code синхронизирует добавленный, обновлённый или удалённый плагин в интерактивную сессию, вы видите `Plugins changed. Run /reload-plugins to activate.` Запустите `/reload-plugins`, чтобы загрузить изменение в этой сессии, или оставьте его на следующий раз, когда вы запустите Claude Code.

### Удаление плагина, который включает проект

Когда вы выбираете **Uninstall** для плагина, который этот репозиторий `.claude/settings.json` включает, будь то со вкладки **Installed** или с `/plugin uninstall`, Claude Code спрашивает, отключить ли его для вас или удалить для всех:

* **Disable for me**: нажмите **y**. Claude Code записывает `false` для плагина в вашем `.claude/settings.local.json` и оставляет его установленным для проекта.
* **Uninstall for everyone**: нажмите **u**. Claude Code удаляет плагин из общего `.claude/settings.json`.

### Посмотрите, что добавляет установленный плагин к вашим сессиям

В вашей оболочке запустите `claude plugin details <name>` для установленного плагина. Строка `Always-on` — это количество токенов, которые плагин добавляет к каждой сессии, где он включен, и строки для каждого компонента показывают, какой skill или agent вносит наибольший вклад. Для полного вывода и того, что означает каждая цифра, см. [Measure what a plugin costs](https://code.claude.com/docs/ru/plugins/measure.md#measure-what-a-plugin-costs).

### Найдите плагины, которые вы больше не используете

На вкладке **Installed** в `/plugin` плагины, которые вы установили сами и не использовали недавно, появляются под заголовком **Not used recently**, и детали каждого плагина показывают строку **Last used**. Используйте этот заголовок и эту строку, чтобы найти плагины, которые всё ещё добавляют стартовые и контекстные затраты, затем отключите или удалите их.

### Плагины с зависимостями

Плагин может объявить другие плагины, от которых он зависит. Когда вы устанавливаете, отключаете или удаляете такой плагин из маркетплейса, Claude Code действует на эти зависимости тоже:

* **Install**: Claude Code также устанавливает и включает объявленные зависимости плагина в той же области. Сообщение об успехе их перечисляет.
* **Enable**: Claude Code также включает зависимости плагина, которые установлены, но отключены. Если объявленная зависимость не установлена, включение не удаётся и сообщение говорит вам установить её сначала.
* **Disable**: когда другой включённый плагин всё ещё нуждается в том, который вы назвали, Claude Code отказывает и выводит цепную команду, которая отключает оба в правильном порядке.
* **Uninstall**: автоустановленные зависимости остаются, пока вы не запустите `claude plugin prune` в вашей оболочке; см. [plugin prune](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-prune).

Если вы загрузили плагин с `--plugin-dir` вместо этого, см. [Test a plugin and its dependency locally](https://code.claude.com/docs/ru/plugins/dependencies.md#test-a-plugin-and-its-dependency-locally).

### Управление плагинами из вашей оболочки

Вы также можете управлять плагинами без запуска сессии Claude Code. В вашей оболочке запустите `claude plugin install`, `enable`, `disable` или `uninstall` как обычные команды терминала; они изменяют те же настройки, что и панель `/plugin`. Каждый принимает `--scope`, чтобы нацелиться на одну область, и использует область по умолчанию, когда вы её опускаете:

* `enable` и `disable` действуют на наиболее специфичную область, чьи настройки уже перечисляют плагин.
* `install` и `uninstall` действуют на пользовательскую область.

Например, эти команды отключают и повторно включают плагин, затем удаляют его в области проекта:

```bash theme={null}
claude plugin disable formatter@your-org
claude plugin enable formatter@your-org
claude plugin uninstall formatter@your-org --scope project
```

## Поддержание плагинов в актуальном состоянии

Плагины обновляются автоматически, когда маркетплейс, из которого они поступают, имеет включённое автообновление. После запуска сессии Claude Code обновляет эти маркетплейсы и обновляет копии плагинов на диске, которые вы установили из них.

Запущенная сессия сохраняет версии, которые она уже загрузила. После обновления вы видите `Plugin updated: <name> · Run /reload-plugins to apply`, и следующая сессия автоматически загружает новые версии.

Это значения по умолчанию для автообновления для каждого вида маркетплейса:

* **On by default**: `claude-plugins-official` и другие [официальные имена маркетплейсов](https://code.claude.com/docs/ru/plugins/security.md#official-marketplace-names), кроме `knowledge-work-plugins` и `first-party-plugins`, плюс [маркетплейсы, добавленные из claude.ai](#add-from-claude-ai).
* **Off by default**: каждый другой маркетплейс, включая маркетплейс сообщества, маркетплейсы третьих сторон и локальные маркетплейсы разработки.

Для того, когда запускается автообновление, какие плагины оно пропускает и переменные окружения, которые его отключают, см. [When auto-update runs](https://code.claude.com/docs/ru/plugins/loading.md#when-auto-update-runs).

### Включение или отключение автообновления для маркетплейса

В сессии Claude Code запустите `/plugin` и перейдите на вкладку **Marketplaces**. Выберите маркетплейс, затем выберите **Enable auto-update** или **Disable auto-update**.

### Обновление плагинов сейчас

Чтобы обновить один плагин, во время сессии откройте его на вкладке **Installed** в `/plugin` и выберите **Update now**, или в вашей оболочке запустите `claude plugin update <plugin>@<marketplace>`.

Команды, которая обновляет все плагины сразу, нет. Чтобы сразу обновить плагины, установленные вами из одного маркетплейса, перейдите на вкладку **Marketplaces** в `/plugin`, выберите маркетплейс и выберите **Update marketplace**. Это обновляет список маркетплейса, обновляет плагины, которые вы установили из него, и сообщает о каждом плагине, который он оставил для самостоятельного обновления. Плагин с [источником `command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source) или с записью маркетплейса, в которой задана команда `headersHelper`, таким способом не обновляется, поэтому вы обновляете его из его представления на вкладке **Installed** или с помощью `claude plugin update <plugin>@<marketplace>`.

Если вы запускаете `claude plugin marketplace update` в вашей оболочке без имени, команда обновляет списки всех маркетплейсов, но оставляет установленные вами плагины в их текущих версиях.

### Автообновление из приватного маркетплейса

Для приватного маркетплейса см. [What background auto-update does with credentials](https://code.claude.com/docs/ru/plugins/host-marketplace.md#what-background-auto-update-does-with-credentials) для того, как фоновые автообновления аутентифицируются по SSH и HTTPS, и [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md#add-a-marketplace) для сообщений, которые вы видите, когда они не удаются.

## Управление маркетплейсами

Вкладка **Marketplaces** в `/plugin` перечисляет каждый маркетплейс, который вы зарегистрировали, вместе с его источником. Выберите один, чтобы просмотреть его плагины, обновить его список, включить или отключить автообновление или удалить его.

Вы также можете перечислять, обновлять и удалять маркетплейсы с помощью команд, из вашей оболочки или внутри сессии:

| Действие | В вашей оболочке | Внутри сессии |
| :- | :- | :- |
| Перечислить маркетплейсы | `claude plugin marketplace list` | `/plugin marketplace list` |
| Обновить список маркетплейса | `claude plugin marketplace update <name>` | `/plugin marketplace update <name>` |
| Удалить маркетплейс | `claude plugin marketplace remove <name>` | `/plugin marketplace remove <name>` |

Когда вы удаляете маркетплейс, Claude Code удаляет каждый плагин, который вы установили из него, и удаляет их записи `enabledPlugins` из ваших файлов настроек. Вкладка **Marketplaces** называет эти плагины перед тем, как попросить вас подтвердить.

## Следующие шаги

* [Маркетплейсы Anthropic](https://code.claude.com/docs/ru/plugins/anthropic-marketplaces.md): чем отличаются официальный маркетплейс и маркетплейсы сообщества и где просмотреть каждый из них
* [Plugin loading reference](https://code.claude.com/docs/ru/plugins/loading.md): почему плагин загрузился, не загрузился или не изменился после обновления
* [Plugin security and trust](https://code.claude.com/docs/ru/plugins/security.md): что просмотреть перед установкой плагина из маркетплейса, который вы не знаете
* [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md): установка и сообщения об ошибках маркетплейса с их исправлениями
* [Create a plugin](https://code.claude.com/docs/ru/plugins/create.md): создайте свой собственный
