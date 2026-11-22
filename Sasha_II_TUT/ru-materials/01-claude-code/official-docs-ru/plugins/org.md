> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Управление плагинами Claude Code для вашей организации

> Контролируйте, какие плагины Claude Code устанавливает и разрешает на каждой машине в вашей организации через управляемые параметры.

Управляемые параметры позволяют вам решать, какие плагины Claude Code устанавливает и разрешает на каждой машине в вашей организации. Пользователи не могут их переопределить. Вы доставляете их либо как [управляемые параметры сервера](https://code.claude.com/docs/ru/server-managed-settings.md) из консоли администратора claude.ai, либо как управляемые параметры конечной точки через MDM или файл `managed-settings.json`. Большинство элементов управления на этой странице вступают в силу только из управляемых параметров.

Эта страница предназначена для администраторов и управляет Claude Code.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Установка плагинов для себя**: начните с [Установка плагинов](https://code.claude.com/docs/ru/plugins/install.md)
> * **Контроль, какие плагины члены могут использовать в claude.ai и Cowork**: см. [Управление плагинами для вашей организации](https://claude.com/docs/plugins/admin) на claude.com
> * **Развертывание одного плагина в claude.ai, Cowork и Claude Code вместе**: см. [Выберите маршрут развертывания](https://claude.com/docs/plugins/org-rollout#choose-a-rollout-route) на claude.com
> * **Страница плагинов в параметрах администратора claude.ai**: [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) включает плагины для учетных записей claude.ai членов, и они достигают Claude Code как [синхронизированные плагины](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins). Это не устанавливает ни один из ключей на этой странице

Разделы следуют порядку, который обычно принимают развертывания: [требуют плагины](#pre-install-and-require-plugins) для всех или по репозиторию, [заполняют контейнеры и CI](#seed-containers-and-ci), [ограничивают](#restrict-what-users-can-install) то, что пользователи могут добавить самостоятельно, [устанавливают политику обновления](#set-update-policy), затем [проверяют](#audit-and-review) то, что установлено. Чтобы просмотреть каждый ключ политики в одном месте, см. [матрицу управления](#control-matrix).

## Pre-install and require plugins

Marketplace — это каталог плагинов, который Claude Code получает из репозитория git, URL-адреса или локального пути. После регистрации marketplace на машине Claude Code может устанавливать плагины из него.

Чтобы установить плагины для флота, установите два ключа вместе в [управляемые параметры](https://code.claude.com/docs/ru/managed-settings.md), файл политики или политику, доставляемую сервером, которую каждая машина в вашей организации читает: `extraKnownMarketplaces` регистрирует marketplace на каждой машине, а `enabledPlugins` называет плагины для установки и включения из него. [Выберите механизм доставки](#choose-a-delivery-mechanism) охватывает, как управляемые параметры достигают каждой машины.

### Choose a delivery mechanism

Управляемые параметры достигают машины через один из трех механизмов доставки:

* **Server-managed settings**: установите ключи плагина как JSON в [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code). Требует роль [Owner](https://code.claude.com/docs/ru/server-managed-settings.md#access-control) в вашей организации Claude. Облачная сессия получает эти параметры перед установкой плагинов.
* **MDM policies**: на macOS доставьте plist, чьи ключи верхнего уровня являются ключами параметров. На Windows сохраните весь документ JSON как строку в значение реестра. Домен plist и ключ реестра находятся в [Где каждый механизм хранит политику](https://code.claude.com/docs/ru/managed-settings.md#where-each-mechanism-stores-the-policy).
* **Managed settings file**: поместите `managed-settings.json` в системный путь платформы. Вы также можете добавить файлы в каталог drop-in `managed-settings.d/` рядом с ним. Пути файлов для каждой платформы находятся в [Где каждый механизм хранит политику](https://code.claude.com/docs/ru/managed-settings.md#where-each-mechanism-stores-the-policy), а правила слияния drop-in находятся в [Разделить файловую политику между командами](https://code.claude.com/docs/ru/managed-settings.md#split-a-file-based-policy-across-teams).

Используйте управляемые параметры сервера, если у вас есть организация Claude for Teams или Enterprise на claude.ai и ваши устройства не все находятся под MDM. В противном случае используйте политику MDM или файл управляемых параметров. Для компромисса см. [Выбор между управляемыми параметрами сервера и конечной точки](https://code.claude.com/docs/ru/server-managed-settings.md#choose-between-server-managed-and-endpoint-managed-settings).

#### Which managed source applies on a machine

По умолчанию на машине применяется только один из этих трех источников. Claude Code использует первый, который доставляет ключ политики, проверяя сначала управляемые параметры сервера, затем политики MDM, затем файл управляемых параметров. Если управляемые параметры сервера доставляют даже один несвязанный ключ политики, Claude Code игнорирует ключи плагина в политике MDM или файле управляемых параметров на этой машине, кроме [ключей, которые он читает из каждого источника](https://code.claude.com/docs/ru/managed-settings.md#keys-read-from-every-admin-source).

Чтобы применить каждый источник вместо этого, установите [`managedSourcesBehavior`](https://code.claude.com/docs/ru/managed-settings#compose-every-managed-source) на `"merge"`.

[Как Claude Code объединяет управляемые источники](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources) также перечисляет ключи, которые Claude Code читает из каждого источника в обоих режимах.

### Require a marketplace and its plugins

Добавьте marketplace под `extraKnownMarketplaces`, ключ по собственному `name` marketplace из его `marketplace.json`. Затем добавьте каждый плагин под `enabledPlugins` как `plugin-name@marketplace-name`. Каждая запись marketplace содержит объект `source` с полем `source`, называющим тип, например `github`. Этот пример управляемых параметров регистрирует marketplace организации и принудительно включает два плагина из него:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": { "source": "github", "repo": "your-org/your-marketplace" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "code-formatter@your-marketplace": true,
    "deploy-helper@your-marketplace": true
  }
}
```

После того как параметры достигнут машины, Claude Code регистрирует marketplace и устанавливает два плагина в начале следующей сессии пользователя. Пользователи видят их в `/plugin`, и отключение одного в своей области не останавливает его загрузку, потому что управляемые параметры имеют приоритет над всеми остальными областями.

Чтобы заблокировать плагин во всех областях и скрыть его из списка marketplace, установите его на `false` в управляемом `enabledPlugins` вместо этого.

Отрегулируйте поля `autoUpdate` и `source` для вашего marketplace:

* **`autoUpdate`**: `true` сохраняет marketplace и его плагины обновляющимися в фоновом режиме, а `false` отключает это. См. [Установка политики обновления](#set-update-policy).
* **`source`**: `github` — один из нескольких типов источников. Источник `git` принимает `url` для GitLab или внутреннего хоста, а источник `url` принимает адрес размещенного `marketplace.json`. Каждая форма источника находится в [справочнике marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md).

Если marketplace — это приватный репозиторий git, каждому пользователю нужен доступ на чтение к нему. Клонирование marketplace на основе git работает с git на машине пользователя, используя сохраненные учетные данные и без подсказок. Для пользователей без учетных записей на хосте git используйте [seed](#seed-containers-and-ci) вместо этого.

Управляемая запись также переопределяет запись marketplace с тем же именем или копию `--plugin-dir` из другого источника:

* **Marketplaces**: управляемая запись marketplace заменяет запись с более низким приоритетом с тем же именем, и поля двух записей не объединяются.
* **`--plugin-dir` copies**: `--plugin-dir` загружает плагин из локального каталога для одной сессии. Для того, что происходит, когда имя этой копии совпадает с плагином, который ваш управляемый `enabledPlugins` называет, см. [Конфликты имен](https://code.claude.com/docs/ru/plugins/loading.md#name-conflicts).

Официальный marketplace Anthropic `claude-plugins-official` не требует записи `extraKnownMarketplaces` когда `enabledPlugins` устанавливает один из его плагинов на `true`. Эта запись `name@claude-plugins-official` объявляет marketplace сама по себе, где бы эти ключи ни применялись. Если вы не включаете ни один из его плагинов и все еще хотите, чтобы он был зарегистрирован на каждой машине, дайте ему явную запись, как это делает [Разрешить официальный marketplace и ваш собственный](#allow-the-official-marketplace-and-your-own).

### Require plugins per repository

Чтобы охватить участников одного репозитория вместо всего флота, установите `extraKnownMarketplaces` и `enabledPlugins` в `.claude/settings.json` этого репозитория. Записи `extraKnownMarketplaces` применяются только в папке, которую участник доверил, и в недоверенной папке Claude Code игнорирует их без сообщения:

* **Interactive sessions**: Claude Code регистрирует marketplace только после того, как участник примет [диалог доверия рабочей области](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) для этой папки.
* **[Non-interactive `-p` runs](https://code.claude.com/docs/ru/headless)**: записи применяются только в папке, доверие которой пользователь уже принял интерактивно, или чей флаг `hasTrustDialogAccepted` вы установили в `~/.claude.json`.

Задание `enabledPlugins` в репозитории не устанавливает плагин. После регистрации маркетплейса попросите каждого участника выполнить `claude plugin install <name>@<marketplace> --scope project`. Пока они этого не сделают, на вкладке **Errors** в `/plugin` может отображаться `Plugin "<name>" is enabled in project settings but isn't installed here` или [`not cached`](https://code.claude.com/docs/ru/plugins/troubleshooting#plugin-not-cached-at). Участникам не нужна установка, если локальный маркетплейс типа `directory` или `file` указывает плагин с [`source` в виде относительного пути](https://code.claude.com/docs/ru/plugins/marketplace-reference#plugin-sources).

Если вы используете локальный источник `directory` или `file` с относительным путем, путь разрешается относительно основного checkout вашего репозитория. Когда вы запускаете Claude Code из git worktree, путь все еще указывает на основной checkout, поэтому все worktrees совместно используют одно и то же местоположение marketplace.

Чтобы развернуть пакет плагинов с зависимостями, поместите плагин пакета в `enabledPlugins`, как описано в [Зависимости плагинов](https://code.claude.com/docs/ru/plugins/dependencies.md).

### When each surface applies the plugin keys

Таблица показывает, когда каждый вид сессии Claude Code применяет `extraKnownMarketplaces` и `enabledPlugins`, из управляемых параметров и из `.claude/settings.json` репозитория. Для Desktop app и расширений IDE см. [Установка плагина](https://code.claude.com/docs/ru/plugins/install.md#install-a-plugin).

| Surface | Managed `extraKnownMarketplaces` and `enabledPlugins` | Repository `.claude/settings.json` |
| :- | :- | :- |
| Terminal, interactive | Applied at session start on every machine that receives the settings | `extraKnownMarketplaces` applied after trust; `enabledPlugins` applied at session start |
| `-p` and CI | Applied at session start, with installs running in the background | `extraKnownMarketplaces` in trusted folders only; `enabledPlugins` applied |
| Cloud sessions | In an Anthropic-hosted environment, only server-managed settings reach the session, which waits for them before it installs plugins. MDM policies and managed settings files stay on the user's machine. For a self-hosted environment, see [Where and when a policy applies](https://code.claude.com/docs/ru/managed-settings.md#where-and-when-a-policy-applies) | See the **Cloud session** tab under [Install a plugin](https://code.claude.com/docs/ru/plugins/install.md#install-a-plugin) |

В запуске `-p` или CI marketplaces и плагины устанавливаются в фоновом режиме, поэтому плагин может отсутствовать в первом повороте. Установите `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1`, чтобы запуск ждал установки перед своим первым запросом.

### Confirm the rollout

Проверьте, что marketplace и плагины прибыли на машину или в запуск CI:

* **На одной машине**: запустите Claude Code и запустите `/plugin`. Marketplace и плагины перечислены.
* **В CI**: запустите `claude -p` с `--output-format stream-json --verbose`. Событие `init` перечисляет загруженные плагины под `plugins`.

## Seed containers and CI

Для образов контейнеров и CI runners, которые не могут клонировать во время выполнения, предварительно заполните каталог плагинов во время сборки и укажите `CLAUDE_CODE_PLUGIN_SEED_DIR` на него. Claude Code регистрирует marketplaces seed при запуске и загружает кэши плагинов из seed на месте, без клонирования.

Seed также служит пользователям, у которых нет учетной записи на хосте git.

> [!NOTE]
>
> В средах CI/CD настройте помощник учетных данных git перед установкой плагинов из приватных репозиториев. На GitHub Actions экспортируйте токен с доступом на чтение к репозиторию marketplace как `GH_TOKEN`, затем запустите `gh auth setup-git`. Токен рабочего процесса по умолчанию может получить доступ только к репозиторию самого рабочего процесса, поэтому приватный marketplace в другом репозитории требует личного токена доступа или токена приложения.

**1. Install into the seed at build time**

Установите `CLAUDE_CODE_PLUGIN_CACHE_DIR` на путь seed, чтобы marketplace и плагины устанавливались туда вместо `~/.claude/plugins`:

```bash theme={null}
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/your-marketplace
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin install code-formatter@your-marketplace
```

Seed имеет тот же макет, что и `~/.claude/plugins`: `known_marketplaces.json`, `marketplaces/<name>/`, и `cache/<marketplace>/<plugin>/<version>/`. Вы можете смонтировать seed по другому пути, чем вы его построили.

**2. Point the runtime at the seed**

Установите `CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed` в окружении контейнера. Чтобы использовать несколько seeds, разделите их пути с `:` на Unix или `;` на Windows. Claude Code использует первый seed, который содержит данный marketplace или кэш плагина.

**3. Enable the plugins**

Плагины в seed не включены сами по себе. Установите `enabledPlugins` для каждого плагина seed, который вы хотите загрузить, в управляемые параметры или в `.claude/settings.json` репозитория.

Чтобы проверить seed, запустите `claude -p` с `--output-format stream-json --verbose` в образе. В списке `plugins` события `init` значение `path` каждого загруженного плагина находится внутри seed, например `/opt/claude-seed/cache/your-marketplace/code-formatter/1.0.0`.

Seed marketplaces следуют этим правилам:

* **Read-only**: Claude Code никогда не пишет в seed и принудительно отключает `autoUpdate` для seed marketplaces.
* **Сборка из объявленного источника**: если пользовательские или управляемые настройки объявляют имя маркетплейса seed в `extraKnownMarketplaces`, собирайте seed из этого источника и `ref`.
* **Отказ**: когда настройки репозитория включают плагин seed, пользователи отказываются от него с помощью `claude plugin disable`, а не удаляя маркетплейс.
* **Update and remove fail**: `claude plugin marketplace update <name>` и `remove` без `--scope` на seed marketplace не работают с сообщением, которое называет каталог seed.
* **Policy still applies**: [allowlist и blocklist](#restrict-what-users-can-install) проверяют записанный источник seed marketplace тоже. Разрешите источник, из которого вы построили seed.

Для флотов без исходящего доступа git объедините seed с источниками marketplace `directory` или `file` на общем монтировании. Установите `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` также, что также отключает [автоматическое обновление плагина](https://code.claude.com/docs/ru/plugins/loading.md#when-auto-update-runs). Если доступен прокси, см. [Конфигурация прокси](https://code.claude.com/docs/ru/network-config.md#proxy-configuration) для переменных, которые нужно установить.

## Restrict what users can install

Управляемый allowlist `strictKnownMarketplaces` и blocklist `blockedMarketplaces` решают, из каких источников marketplace могут поступать плагины. Источник marketplace — это репозиторий git, URL-адрес или локальный путь, который Claude Code получает из него. Оба списка совпадают с источником marketplace, из которого поступает плагин, а не с собственной записью плагина внутри этого marketplace.

Для обычной блокировки, которая разрешает официальный marketplace и ваш собственный, см. [Разрешить официальный marketplace и ваш собственный](#allow-the-official-marketplace-and-your-own). Объедините его с [`disableSideloadFlags`](#control-matrix), чтобы пользователи не могли загружать плагины из локального каталога или URL-адреса.

Оба списка применяются перед загрузкой чего-либо и снова при запуске сессии:

* **Before a download**: списки применяются, когда пользователь добавляет marketplace и при каждой установке, обновлении, обновлении и автоматическом обновлении.
* **At session start**: списки применяются снова к плагинам, которые уже установлены, поэтому установленный плагин, чей источник marketplace больше не совпадает, не загружается. `/plugin` перечисляет его с `Marketplace "<name>" is not in the allowed marketplace list` или `Marketplace "<name>" is blocked by enterprise policy`.

Где два списка применяются, зависит от того, где вы их установили:

* **Консоль администратора claude.ai**: Claude Code применяет оба списка в сессиях, которые [читают управляемые настройки с сервера](https://code.claude.com/docs/ru/managed-settings.md#where-and-when-a-policy-applies). claude.ai также проверяет их, когда кто-либо в вашей организации добавляет маркетплейс из Git-репозитория на claude.ai или из **Customize** в приложении Desktop вне его вкладки Code.

  Это касается как маркетплейса, который участник добавляет для своей учётной записи, так и маркетплейса, добавленного для всей организации в разделе [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=marketplaces). claude.ai отклоняет репозиторий, который не допускается списком разрешённых или указан в списке запрещённых. Он не перепроверяет маркетплейс, добавленный в любом из этих мест до того, как вы задали списки, и не проверяет загруженные плагины.
* **A managed settings file, OS-level policy, or other managed source**: Claude Code применяет оба списка, где он читает этот источник. claude.ai не читает его.

Пока установлен какой-либо allowlist, или blocklist называет любой источник, кроме [`skills-dir`](#blocklist-with-blockedmarketplaces), плагин, чей marketplace Claude Code не может найти, не загружается. `/plugin` показывает ошибку политики для него, а не ошибку не найдено. Обычный случай — устаревшая запись `enabledPlugins` для marketplace, который никто не регистрировал.

### Control matrix

Таблица перечисляет каждый ключ политики плагина, что он применяет, и что он не может делать.

| Key | What it enforces | What it can't do |
| :- | :- | :- |
| `strictKnownMarketplaces` | Allowlist источников marketplace. `[]` блокирует каждый источник, включая официальный marketplace. Alias: `allowedMarketplaces` | Не регистрирует marketplace, не ограничивает записи внутри разрешенного marketplace или не блокирует `--plugin-dir` |
| `blockedMarketplaces` | Blocklist источников marketplace, проверяется перед allowlist | Не блокирует marketplace, уже зарегистрированный из источника, который он не совпадает |
| `syncClaudeAiPlugins` | Установите `false`, чтобы остановить Claude Code загрузку и загрузку плагинов [синхронизированных из claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins) для учетной записи каждого пользователя. Требует Claude Code v2.1.273 или позже | Не отключает один синхронизированный плагин. Для этого установите `"<name>@synced": false` в [`enabledPlugins`](https://code.claude.com/docs/ru/settings-reference#enabledplugins) |
| `enabledPlugins` | `true` принудительно включает, `false` блокирует во всех областях и скрывает плагин | Не устанавливает плагин, чей marketplace не зарегистрирован или не разрешен |
| `disableSideloadFlags` | При запуске отклоняет `--plugin-dir`, `--plugin-url`, `--agents`, параметр Agent SDK `plugins` и папки, указанные в переменной [`CLAUDE_CODE_PLUGIN_DIRS`](https://code.claude.com/docs/ru/env-vars#variables), а также `--mcp-config`, если только каждый сервер в нём не является внутрипроцессной записью `type: "sdk"`. Отклоняет папки плагинов, которые приложение Agent SDK добавляет во время сессии с помощью [`addPlugins`](https://code.claude.com/docs/ru/agent-sdk/typescript#load-more-plugin-folders-with-addplugins) | Не ограничивает `.mcp.json`, `claude mcp add` и серверы, предоставляемые через SDK. Используйте вместе с [`allowedMcpServers`](https://code.claude.com/docs/ru/managed-mcp) |
| `disableCommandPluginSources` | Блокирует плагины с источником `command` от установки, обновления или загрузки. Источник `command` — это тот, чей каталог плагина создается путем запуска команды на машине. Когда не установлено, принимает значение `allowManagedHooksOnly` | Не влияет на другие типы источников |
| `allowManagedHooksOnly` | Ограничивает, какие hooks работают. См. [`allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#allowmanagedhooksonly) | Не доверяет hooks из плагинов, которые пользователи включают сами |
| `strictPluginOnlyCustomization` | Блокирует скиллы, агентов, хуки и MCP-серверы из пользовательских и проектных источников. Также прекращает загрузку [плагинов из каталога скиллов](#keep-skills-directory-plugins-loading). Задайте `true`, чтобы охватить все четыре типа, или массив из значений `skills`, `agents`, `hooks` и `mcp`, например `["skills", "hooks"]`, чтобы охватить некоторые из них | Не ограничивает, какие плагины устанавливают пользователи, и не отклоняет флаги CLI для сторонней загрузки (sideload) плагинов, агентов и MCP-серверов. Используйте вместе с `strictKnownMarketplaces` и `disableSideloadFlags` |
| `pluginSuggestionMarketplaces` | Маркетплейсы, плагины которых могут появляться в терминале как предложения для установки. См. [Рекомендация плагинов](#recommend-plugins) | Не влияет на встроенные подсказки |
| `pluginTrustMessage` | Добавляет ваш текст к предупреждению доверия, которое `/plugin` показывает перед установкой плагина | Не изменяет собственный текст предупреждения |
| `allowedChannelPlugins` | Заменяет список плагинов по умолчанию, разрешенных для отправки сообщений канала. Требует `channelsEnabled: true` | См. [Ограничить, какие плагины канала могут работать](https://code.claude.com/docs/ru/channels.md#restrict-which-channel-plugins-can-run) |
| [`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL=1`](https://code.claude.com/docs/ru/env-vars) | Останавливает интерактивные сессии терминала от автоматической регистрации официального marketplace | Не удаляет marketplace, уже зарегистрированный. Allowlist и blocklist управляют той же автоматической регистрацией без него. Машина, которая запустилась один раз с установленным, не возобновляет автоматическую регистрацию после того, как вы его отключите |
| [`allowManagedModsOnly`](https://code.claude.com/docs/ru/plugins/mods/admin#stop-user-installed-mods-from-loading) | Запрещает каждому установленному [моду](https://code.claude.com/docs/ru/plugins/mods/overview.md), который не [считается модом вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods), запускать свои хуки | Не препятствует установке плагина, содержащего мод. Для этого используйте ключи маркетплейсов из этой таблицы |

Каждый ключ в таблице является управляемым параметром, кроме `enabledPlugins`, `syncClaudeAiPlugins`, `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` и `allowManagedModsOnly`:

* **`enabledPlugins`**: вы можете установить его в любой области, и управляемые параметры его блокируют.
* **`syncClaudeAiPlugins`**: каждый пользователь также может установить его в своих собственных пользовательских или локальных параметрах. См. его [область в справочнике параметров](https://code.claude.com/docs/ru/settings-reference.md#syncclaudeaiplugins).
* **`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`**: это переменная окружения, которую вы доставляете через управляемый блок `env`, показанный под [Отключить обновления для всего флота](#turn-updates-off-for-the-whole-fleet).
* **`allowManagedModsOnly`**: это опция встроенного плагина, которую вы устанавливаете под `pluginConfigs` в управляемых параметрах. См. [Остановить загрузку пользовательских установленных mods](https://code.claude.com/docs/ru/plugins/mods/admin.md#stop-user-installed-mods-from-loading).

Каждый ключ параметров здесь имеет запись в [справочнике параметров](https://code.claude.com/docs/ru/settings-reference.md).

#### Aliases for the marketplace keys

`strictKnownMarketplaces` также может быть написан как `allowedMarketplaces`, а `extraKnownMarketplaces` также может быть написан как `additionalMarketplaces`.

* **Version**: aliases требуют Claude Code v2.1.232 или позже, и старые клиенты их игнорируют. В файле, который читает смешанный флот, сохраняйте канонические имена.
* **Both spellings set**: когда файл устанавливает оба написания, применяется значение канонического ключа.

### Allowlist with `strictKnownMarketplaces`

Установите allowlist на список этих объектов источника. Большинство записей совпадают точно, записи `hostPattern` и `pathPattern` совпадают как регулярные выражения, и подстановочные знаки владельца `github` совпадают по владельцу:

* **`github`**: `{ "source": "github", "repo": "your-org/approved-plugins" }`, с опциональными `ref` и `path`.
* **`github` owner wildcard**: `{ "source": "github", "repo": "your-org/*" }` совпадает с каждым репозиторием под этим владельцем. `*` должен стоять за всем именем репозитория. Claude Code игнорирует записи, такие как `*/plugins` и `your-org/tools-*`, как недействительные, поэтому они ничему не совпадают. Требует Claude Code v2.1.223 или позже.
* **`git`**: `{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }`, с опциональными `ref` и `path`.
* **`url`**: `{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }`, с опциональными `headers`.
* **`file` and `directory`**: `{ "source": "file", "path": "/opt/marketplace/marketplace.json" }` или `{ "source": "directory", "path": "/opt/marketplace/plugins" }`, с абсолютными путями.
* **`hostPattern`**: `{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }`, совпадает с хостом источников `github`, `git` и `url`. Шаблон совпадает в любом месте имени хоста, поэтому закрепите его с `^` и `$`, как показано, чтобы совпадать со всем хостом. Источник `github` всегда считается `github.com`. Используйте запись `hostPattern` для GitHub Enterprise Server или хоста GitLab, где разработчики создают свои собственные marketplaces. [Страница GHES](https://code.claude.com/docs/ru/github-enterprise-server.md#allowlist-ghes-marketplaces-in-managed-settings) имеет отработанный пример.
* **`pathPattern`**: `{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }`, совпадает с `path` источников `file` и `directory`. Шаблон совпадает в любом месте пути, поэтому начните его с `^`, чтобы закрепить префикс каталога. `".*"` разрешает каждый локальный путь.
* **`skills-dir`**: `{ "source": "skills-dir" }` не соответствует ни одному маркетплейсу. О том, что делает эта запись, см. [Сохранение загрузки плагинов из каталога скиллов](#keep-skills-directory-plugins-loading).

#### How entries match

Запись `url` совпадает по своему значению `url`; `headers` не сравниваются. Для записей `github` и `git`, `repo` или `url`, `ref` и `path` должны все совпадать или отсутствовать с обеих сторон:

* Запись без `ref` не охватывает источник с `ref: "main"`.
* Запись для `your-org/your-marketplace` не охватывает URL `git`, который клонирует тот же репозиторий.
* Косая черта в конце, суффикс `.git` или `ssh://` вместо `https://` — это другое значение. Когда marketplace может быть клонирован более чем одним URL-адресом, предпочитайте запись `hostPattern`.

Записи с подстановочным знаком владельца следуют точным правилам для `ref` и совпадают с любым `path` внутри репозитория, если запись не закрепляет один. Сопоставление подстановочных знаков чувствительно к регистру в allowlist.

#### Keep skills-directory plugins loading

Плагины из каталога скиллов — это плагины, которые пользователи хранят в `~/.claude/skills/` или в `.claude/skills/` проекта, в папках, содержащих `.claude-plugin/plugin.json`. Если вы зададите какой-либо список разрешённых без записи `{ "source": "skills-dir" }`, они перестанут загружаться. Если вы зафиксируете любой тип настройки с помощью [`strictPluginOnlyCustomization`](https://code.claude.com/docs/ru/settings-reference#strictpluginonlycustomization), они перестанут загружаться независимо от наличия этой записи. Список разрешённых не применяется к обычным [скиллам](https://code.claude.com/docs/ru/skills.md), то есть к `SKILL.md` без такого манифеста.

#### Marketplaces hosted on claude.ai

Allowlist и blocklist совпадают с [marketplace, размещенным на claude.ai](https://code.claude.com/docs/ru/plugins/install.md#add-from-claude-ai), по его хосту. Чтобы разрешить или заблокировать один, добавьте запись `hostPattern`, которая совпадает с `claude.ai`, в `strictKnownMarketplaces` или `blockedMarketplaces`. На allowlist такая запись допускает ваши marketplaces claude.ai организации и marketplaces claude.ai по умолчанию, но не marketplace, состоящий из собственных загрузок claude.ai члена или тот, чья область claude.ai не указал. Требует Claude Code v2.1.273 или позже.

#### Lock every source out

Пустой allowlist, `[]`, блокирует каждый источник marketplace, включая официальный marketplace.

Эта блокировка не охватывает плагины [синхронизированные из claude.ai](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), которые Claude Code загружает из учетной записи каждого пользователя, а не из marketplace. Чтобы остановить и те, установите [`syncClaudeAiPlugins`](https://code.claude.com/docs/ru/settings-reference#syncclaudeaiplugins) на `false` в управляемых параметрах или отключите Skills для вашей организации на claude.ai.

### Blocklist with `blockedMarketplaces`

`blockedMarketplaces` принимает те же объекты источника, что и [`strictKnownMarketplaces`](#allowlist-with-strictknownmarketplaces), и проверяется первым, поэтому источник в обоих списках блокируется. Сопоставление blocklist шире, чем сопоставление allowlist:

* URL-адреса Git канонизируются, поэтому формы `git@` и `https://`, суффиксы `.git` и косые черты в конце одного репозитория `github.com` все совпадают с одной записью.
* Запись `github` также блокирует эквивалентный URL `git`, и наоборот.
* Для записи `owner/*`, сравнение владельца не чувствительно к регистру.
* Запись без `ref` или `path` блокирует каждый ref и path репозиториев, которые она совпадает.

Эта запись блокирует каждый репозиторий под одним владельцем GitHub:

```json theme={null}
{
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted-org/*" }
  ]
}
```

Записи `url` в `blockedMarketplaces` также применяются, когда пользователь добавляет URL репозитория `https://`, который Claude Code [клонирует, а не получает](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-marketplace-add), например простой URL репозитория `github.com` или `gitlab.com`. Пользователь не может добавить этот URL, если запись его называет. Сопоставление игнорирует суффикс `.git` и любой ref, который пользователь добавляет после `#`. Требует Claude Code v2.1.232 или позже.

Запись `{ "source": "skills-dir" }` здесь останавливает [плагины skills-directory](#keep-skills-directory-plugins-loading) от загрузки, из обоих `~/.claude/skills/` и `.claude/skills/` проекта.

Blocklist, который называет только эту запись, не считается активным ограничением, поэтому он не [останавливает плагины, чей marketplace Claude Code не может найти](#restrict-what-users-can-install) от загрузки.

### Allow the official marketplace and your own

Большинство организаций разрешают официальный marketplace и свой собственный, и регистрируют оба, чтобы каждая машина имела их. Эта политика управляемых параметров разрешает оба marketplace, регистрирует оба, принудительно включает два плагина и отклоняет `--plugin-dir`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" },
    { "source": "github", "repo": "your-org/*" },
    { "source": "skills-dir" }
  ],
  "extraKnownMarketplaces": {
    "claude-plugins-official": {
      "source": { "source": "github", "repo": "anthropics/claude-plugins-official" }
    },
    "your-marketplace": {
      "source": { "source": "github", "repo": "your-org/your-marketplace" }
    }
  },
  "enabledPlugins": {
    "code-formatter@your-marketplace": true,
    "deploy-helper@your-marketplace": true
  },
  "disableSideloadFlags": true
}
```

На машине с этой политикой добавление любого источника вне списка, например `/plugin marketplace add https://example.com/other-marketplace.git`, не работает с сообщением, содержащим `is blocked by enterprise policy`, за которым следуют разрешенные источники. `claude --plugin-dir ./x` выходит с сообщением, называющим `disableSideloadFlags`.

Если удалить из этого списка разрешённых запись `{ "source": "skills-dir" }`, [плагины из каталога скиллов](#keep-skills-directory-plugins-loading) перестанут загружаться.

Регистрируйте оба marketplace с явными записями `extraKnownMarketplaces`, как эта политика делает, а не полагаясь на allowlist или на официальный marketplace, регистрирующий себя:

* **Allowlist не регистрирует ничего**: запись `extraKnownMarketplaces` делает, и она сама должна пройти allowlist. Claude Code отказывает регистрировать управляемый marketplace, чей источник allowlist не совпадает.
* **Официальный marketplace регистрирует себя только в интерактивной сессии терминала**: даже там он регистрируется только, когда allowlist это разрешает. Запуск `-p` или терминал, подключенный к облачной сессии, никогда его не регистрирует.
* **Заблокированная попытка запоминается**: если машина когда-либо работала под политикой, которая блокировала официальный marketplace, Claude Code записывает заблокированную попытку и не повторяет попытку после изменения политики. Блокировка `[]` — это одна такая политика. Эта машина регистрирует его снова только через запись `extraKnownMarketplaces`, такую как в этой политике, запись `enabledPlugins` для одного из его плагинов или ручное `/plugin marketplace add`.

## Set update policy

Вы можете установить политику обновления для каждого marketplace, для всего флота или для каждой группы пользователей через каналы выпуска.

### Turn auto-update on or off per marketplace

Автоматическое обновление плагина работает в фоновом режиме после запуска для marketplaces, у которых оно включено. Для того, какие marketplaces имеют его включенным по умолчанию, см. [Когда автоматическое обновление работает](https://code.claude.com/docs/ru/plugins/loading.md#when-auto-update-runs). Чтобы решить для флота, установите `"autoUpdate": true` или `false` на управляемой записи `extraKnownMarketplaces`:

* Если управляемая запись устанавливает поле, Claude Code отклоняет переключение `/plugin` пользователя с ошибкой, которая начинается с `Auto-update for '<name>' is set by`.
* Если управляемая запись оставляет поле неустановленным, переключение пользователя сохраняется.

### Turn updates off for the whole fleet

Чтобы отключить автоматическое обновление плагина для каждого marketplace, установите `DISABLE_AUTOUPDATER` в управляемом блоке `env`, как это делает этот пример. Та же переменная также останавливает собственные обновления Claude Code:

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

Чтобы остановить собственные обновления Claude Code, но сохранить автоматическое обновление плагина, добавьте `"FORCE_AUTOUPDATE_PLUGINS": "1"` в тот же блок. Другие [переменные окружения, которые останавливают автоматическое обновление плагина](https://code.claude.com/docs/ru/plugins/loading.md#when-auto-update-runs), работают так же.

`DISABLE_AUTOUPDATER` не охватывает плагины с источником [`command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source). Claude Code повторно запускает команду каждого включенного при каждой сессии и устанавливает вывод, когда он изменился. Для того, что останавливает эти запуски, см. [Когда источник команды повторно запускается](https://code.claude.com/docs/ru/plugins/loading.md#when-a-command-source-re-runs).

### Assign release channels to user groups

Чтобы запустить стабильные и ранние каналы доступа, разместите два marketplace, которые указывают на разные refs одних и тех же плагинов. Затем дайте каждой группе пользователей свой собственный marketplace через отдельные управляемые настройки конечной точки или политику шлюза. В плане Enterprise вы также можете использовать управляемые настройки сервера из консоли администратора.

* Развертывайте отдельные [управляемые параметры конечной точки](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms), такие как файл управляемых параметров или профиль MDM, на устройства каждой группы. Чтобы проверить, применяется ли файл или профиль для каждой группы на устройстве, которое также имеет источник на уровне организации, см. [Как Claude Code объединяет управляемые источники](https://code.claude.com/docs/ru/managed-settings.md#precedence-within-the-managed-tier).
* Определите по одной [политике шлюза Claude apps](https://code.claude.com/docs/ru/claude-apps-gateway-config.md#managed) для каждой группы. По умолчанию шлюз применяет первую политику, правило сопоставления которой подходит пользователю, поэтому упорядочите политики так, чтобы каждый пользователь попадал в политику своей группы. Карта `extraKnownMarketplaces` этой политики не объединяется с картами других политик, поэтому перечислите в ней все маркетплейсы, которые нужны группе, а не только маркетплейс ее канала.
* В плане Enterprise [задайте каждой группе собственную конфигурацию](https://code.claude.com/docs/ru/server-managed-settings.md#give-groups-different-settings) в консоли администратора. Конфигурация группы не объединяется с конфигурацией на уровне организации, поэтому поместите все настройки, которые нужны группе, в собственную конфигурацию группы, включая каждый маркетплейс.

С любым из этих механизмов стабильная группа получает эту настройку:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": { "source": "github", "repo": "your-org/stable-tools" }
    }
  }
}
```

Группа раннего доступа получает `latest-tools` вместо этого. Чтобы установить два marketplace, см. [Запустить каналы выпуска](https://code.claude.com/docs/ru/plugins/host-marketplace.md#run-release-channels).

## Recommend plugins

Владельцы Marketplace могут прикреплять сигналы `relevance` к записям, чтобы Claude Code предлагал плагин, когда проект совпадает.

Предложения из marketplace появляются только, когда он зарегистрирован на машине пользователя, вы перечисляете его имя в `pluginSuggestionMarketplaces` в управляемых параметрах, и вы объявляете его источник в той же политике. Объявите источник либо как запись `extraKnownMarketplaces` marketplace, либо как запись allowlist. Официальный marketplace требует только имя. См. [Включить предложения в управляемых параметрах](https://code.claude.com/docs/ru/plugins/relevance.md#enable-suggestions-in-managed-settings).

> [!NOTE]
>
> В диалоге облачной сессии Claude может предлагать плагины независимо от того, задали ли вы `pluginSuggestionMarketplaces`. Чтобы отключить эти предложения, см. [Отключение предложений плагинов](https://code.claude.com/docs/ru/claude-code-on-the-web.md#turn-off-plugin-suggestions).

## Audit and review

События OpenTelemetry и Analytics API говорят вам, что ваш флот устанавливает и запускает.

Для того, что плагин может запустить на машине и что каждый уровень доверия разрешает, прочитайте [Безопасность плагина](https://code.claude.com/docs/ru/plugins/security.md) перед тем, как вы одобрите marketplace.

### OpenTelemetry events

`claude_code.plugin_installed` записывает каждую установку, и `claude_code.plugin_loaded` записывает каждый включенный плагин при запуске сессии. Оба события редактируют или опускают имена плагинов и marketplace третьих сторон, если вы не установите `OTEL_LOG_TOOL_DETAILS=1`, как показано в [Редактированные имена плагинов в вашем бэкенде](https://code.claude.com/docs/ru/plugins/measure.md#redacted-plugin-names-in-your-backend). Списки полей находятся под [Событие установки плагина](https://code.claude.com/docs/ru/monitoring-usage.md#plugin-installed-event) и [Событие загрузки плагина](https://code.claude.com/docs/ru/monitoring-usage.md#plugin-loaded-event).

### Analytics API

На плане Enterprise `GET /v1/organizations/analytics/plugins` возвращает подсчеты установки и вызова для каждого плагина, в день, по Claude Code и Cowork. Вы можете группировать подсчеты по пользователю или группе RBAC. Активность плагина, которая достигает Anthropic без имени плагина, появляется в одной совокупной строке `third-party`. См. [справочник конечной точки](https://platform.claude.com/docs/en/api/admin/analytics/plugins/list) и [Доступ к данным программно](https://code.claude.com/docs/ru/analytics.md#access-data-programmatically) для ключа, который ему нужен.

## Plan for what managed settings can't enforce

Эти запросы из проверок безопасности не имеют выделенного ключа в текущей схеме параметров. Ближайшие существующие элементы управления:

* **Назначение для отдельных пользователей или групп**: каждый ключ плагина применяется к каждому пользователю, который получает настройки. Для политики на уровне групп доставляйте каждой группе собственные настройки, как описано в разделе [Назначение каналов выпуска группам пользователей](#assign-release-channels-to-user-groups).
* **Restricting entries inside an allowed marketplace**: allowlist совпадает с источниками marketplace. Чтобы заблокировать один плагин из разрешенного marketplace, установите его на `false` в управляемом `enabledPlugins`.
* **Hiding `/plugin`**: нет ключа, который отключает команду. Ближайший эквивалент объединяет allowlist, называющий только ваш marketplace, управляемые записи `enabledPlugins` для плагинов, которые вы поставляете, и `disableSideloadFlags`.
* **Gating `--plugin-dir` through the allowlist**: allowlist не охватывает `--plugin-dir`. `disableSideloadFlags` делает.
* **Enforcing the claude.ai plugin toggles through these keys**: [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) не устанавливает ключи на этой странице. Что члены и ваша организация включают там достигает CLI как [синхронизированные плагины](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins), которые имеют свои собственные элементы управления.

## Troubleshoot policy

Если политика плагина не ведет себя как ожидается на машине, сначала проверьте эти симптомы:

* **The managed file didn't parse**: когда `managed-settings.json` не является действительным JSON, Claude Code отказывается запускаться и печатает [ошибку, называющую файл](https://code.claude.com/docs/ru/errors.md#managed-settings-document-could-not-be-parsed). Файл, который анализирует, но имеет одну недействительную запись, сохраняет остальную часть своей политики. См. [Недействительные записи в управляемых параметрах](https://code.claude.com/docs/ru/managed-settings.md#invalid-entries-in-managed-settings).
* **The managed source didn't load**: запустите `/status` и ищите `Enterprise managed settings` в строке `Setting sources`. Если его нет, источник не загрузился.
* **A user reports `blocked by enterprise policy`**: сообщение называет marketplace или его источник. Для allowlist он также перечисляет разрешенные источники. Записи, обращенные к пользователю, находятся на [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md).
* **A plugin the user disabled in `~/.claude/settings.json` still loads**: другой источник параметров повторно включил его, такой как управляемая запись `enabledPlugins`, которая принудительно включает его. `/plugin` и `claude plugin list` показывают `Disabled in ~/.claude/settings.json but still loads` с этим источником параметров.

## Next steps

* [Marketplace reference](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#marketplace-sources): значения `source`, которые `extraKnownMarketplaces`, `strictKnownMarketplaces` и `blockedMarketplaces` принимают
* [Host and maintain a marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md): запустите marketplace, на который указывает ваша политика
* [Plugin security and trust](https://code.claude.com/docs/ru/plugins/security.md): что плагин может делать на машине и как просмотреть один перед установкой
* [Manage mods for your organization](https://code.claude.com/docs/ru/plugins/mods/admin.md): отключите или ограничьте mods, плагины, которые запускают JavaScript внутри Claude Code
* [Server-managed settings](https://code.claude.com/docs/ru/server-managed-settings.md): доставляйте эти ключи из консоли администратора claude.ai
* [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md#blocked-by-your-organization): сообщения, которые пользователи видят, когда политика их блокирует
