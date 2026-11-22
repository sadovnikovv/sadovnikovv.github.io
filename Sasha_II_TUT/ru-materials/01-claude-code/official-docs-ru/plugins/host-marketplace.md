> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Размещение и поддержка маркетплейса

> Опубликуйте маркетплейс плагинов, где пользователи смогут его найти, предоставьте доступ к приватному маркетплейсу и выпускайте обновления и переименования без нарушения установок.

Размещение маркетплейса означает размещение вашего каталога `marketplace.json` в месте, где другие люди смогут добавить его с помощью `/plugin marketplace add`, установить его плагины и продолжать получать ваши изменения после их публикации.

Эта страница предназначена для человека, который управляет маркетплейсом.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Вы еще не написали файл каталога**: начните с [Создание маркетплейса](https://code.claude.com/docs/ru/plugins/create-marketplace.md)
> * **Вы администратор, требующий, ограничивающий или предварительно устанавливающий маркетплейсы на машинах вашей организации**: прочитайте [Управление плагинами для вашей организации](https://code.claude.com/docs/ru/plugins/org.md)

Начните с [Размещение вашего маркетплейса](#host-your-marketplace), чтобы выбрать хост и команду, которую запустят ваши пользователи. Прочитайте [Держите пользователей в курсе](#keep-users-up-to-date) перед вашим первым выпуском. Прочитайте [Переименование или удаление плагина](#rename-or-remove-a-plugin) перед изменением `name` плагина.

## Host your marketplace

Вы можете разместить marketplace на GitHub, на другом git-хосте, как размещенный URL `marketplace.json` или в каталоге на общей файловой системе. Отправьте пользователям команду добавления для вашего хоста и скажите им, что им нужно на их машине:

| Хост | Пользователи запускают в сеансе Claude Code | Что нужно пользователям |
| :- | :- | :- |
| GitHub | `/plugin marketplace add your-org/your-marketplace` | `git`, и для приватного репозитория доступ, описанный в [Grant access to a private marketplace](#grant-access-to-a-private-marketplace) |
| GitLab, Bitbucket, GitHub Enterprise Server или другой git-хост | `/plugin marketplace add https://gitlab.example.com/team/plugins.git` | `git` и доступ к хосту с их машины. Отправьте полный URL, потому что сокращение `owner/repo` всегда означает github.com |
| Размещенный URL `marketplace.json` | `/plugin marketplace add https://plugins.example.com/marketplace.json` | HTTPS доступ к URL. Пользователям не нужен `git` для самого каталога |
| Каталог на общей файловой системе | `/plugin marketplace add /Volumes/shared/claude-plugins` | Доступ на чтение к пути |

Чтобы закрепить ветку или тег marketplace GitHub или git-URL, скажите пользователям добавить `#<ref>`, как в `your-org/your-marketplace#stable`. [Справочник команд плагинов](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-marketplace-add) перечисляет все формы, которые команда принимает.

Успешное добавление выводит `Successfully added marketplace: your-marketplace`. Claude Code берет это имя из поля `name` в вашем `marketplace.json`, а не из имени репозитория.

Затем пользователи устанавливают плагин по `name` его записи и `name` marketplace, как в `/plugin install code-formatter@your-marketplace`.

### Register the marketplace for everyone in a repository

Чтобы поделиться marketplace со всеми, кто работает в одном репозитории, запустите `claude plugin marketplace add your-org/your-marketplace --scope project` там один раз из вашей оболочки и зафиксируйте `.claude/settings.json`, который он создает. Claude Code затем регистрирует marketplace для каждого товарища по команде, который [доверяет папке](https://code.claude.com/docs/ru/plugins/org.md#require-plugins-per-repository).

### Avoid relative-path entries in a URL-hosted marketplace

Когда пользователи добавляют ваш marketplace как простой URL `marketplace.json`, Claude Code загружает только этот файл. Запись в вашем массиве `plugins`, чей `source` является относительным путем, таким как `./plugins/formatter`, затем не работает при установке с [`its marketplace entry path does not stay inside the marketplace directory`](https://code.claude.com/docs/ru/plugins/troubleshooting#plugins-with-relative-paths-fail-in-url-based-marketplaces). Дайте каждой записи источник, который можно получить самостоятельно, такой как репозиторий `github` или URL `archive`, или разместите marketplace в git-репозитории, чтобы Claude Code клонировал все дерево.

### Stay within the download limits for hosted files

Когда пользователи добавляют ваш marketplace как URL `marketplace.json` или устанавливают запись с источником [`archive`](https://code.claude.com/docs/ru/plugins/marketplace-reference#archive-plugin-source), Claude Code загружает файл с вашего сервера. Загрузка не удается при превышении лимитов в этой таблице, поэтому размер ваших файлов и настройка вашего сервера должны оставаться в пределах них.

| Файл | Наибольшая загрузка | Время ответа вашего сервера | Перенаправления |
| :- | :- | :- | :- |
| `marketplace.json` из источника marketplace типа `url` | 5 МиБ | 10 секунд | Перенаправление на другой источник должно использовать `https://` и не может указывать на хост loopback, link-local или cloud-metadata, поэтому перенаправление с `https://` на `http://` не удается |
| Zip из источника плагина типа `archive` | 256 МиБ | 120 секунд | Максимум пять. Каждая цель перенаправления должна использовать `https://` и не может указывать на хост loopback, link-local или cloud-metadata |

Запрос, который перенаправление отправляет на другой источник, не содержит ни одного из заголовков, которые вы настроили на источнике marketplace или записи плагина.

После загрузки архива установка не удается, когда zip превышает любой из этих лимитов извлечения:

* **Записи**: 100 000 файлов и каталогов
* **Размер файла**: 512 МиБ для любого одного файла, несжатого
* **Общий размер**: 1 ГиБ несжатого
* **Коэффициент сжатия**: несжатое содержимое в 50 раз больше размера zip

### Edit plugins in place on a shared directory

Когда пользователи добавляют ваш marketplace из общего каталога, Claude Code читает плагины с источниками относительных путей непосредственно из этого каталога вместо их копирования. Пользователи видят ваши правки при следующем запуске сеанса или запуске `/reload-plugins`, без шага обновления или увеличения версии.

### Keep plugin files out of Git LFS

Держите файлы, которые нужны вашим плагинам, вне [Git LFS](https://git-lfs.com). Когда пользователи добавляют marketplace, размещенный в git-репозитории, или устанавливают основанный на git плагин, который он перечисляет, Claude Code клонирует этот marketplace или репозиторий плагина на их машину. Клон никогда не загружает содержимое LFS, поэтому отслеживаемые LFS файлы приходят как файлы указателей.

### Share files within a marketplace with symlinks

Чтобы поделиться файлами между вашим плагином и другими частями того же marketplace, создайте символические ссылки внутри каталога вашего плагина. Когда Claude Code копирует плагин в его кэш, он обрабатывает каждую символическую ссылку по тому, где разрешается цель:

* **В собственном каталоге плагина**: символическая ссылка сохраняется как относительная символическая ссылка в кэше, поэтому она продолжает разрешаться скопированной цели во время выполнения.
* **В другом месте в том же marketplace**: символическая ссылка разыменовывается. Содержимое цели копируется в кэш на его место. Это позволяет каталогу `skills/` мета-плагина ссылаться на навыки, определенные другими плагинами в marketplace.
* **Вне marketplace**: символическая ссылка пропускается в целях безопасности.

Для плагинов, установленных из локального пути, или из [`command` источника](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source), чей `mode` является стандартным `copy`, Claude Code сохраняет только символические ссылки, которые разрешаются в собственном каталоге плагина, и пропускает все остальные.

Следующая команда создает ссылку из плагина marketplace на общий навык, определенный соседним плагином. На Windows используйте `mklink /D` из повышенной командной строки или включите режим разработчика:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

## Distribute through organization settings

На плане Team или Enterprise вы также можете распространять marketplace через [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) на claude.ai вместо размещения его где-то, где пользователи добавляют его сами. Organization sync читает репозиторий через подключение GitHub или GitLab вашей организации на claude.ai, поэтому учетные данные git ваших пользователей не задействованы.

Organization sync более строг к репозиторию, чем `/plugin marketplace add`:

* **Репозиторий Marketplace**: на github.com и gitlab.com он должен быть приватным или внутренним
* **Источники плагинов**: organization sync принимает только некоторые [типы источников](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-sources)
* **Каталог `bin/` верхнего уровня**: claude.ai отклоняет плагин, который его имеет, и синхронизирует остальную часть marketplace. Сообщение об ошибке начинается с `Plugin contains a top-level bin/ directory`. Держите исполняемые файлы в другом каталоге, таком как `scripts/`, и ссылайтесь на них как `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` из ваших hooks или конфигов MCP сервера

[Sync your organization's plugins from a repository](https://claude.com/docs/plugins/org-sync) на claude.com содержит список принятых источников, настройку GitLab и ошибку `bin/`, а [Manage plugins for your organization](https://claude.com/docs/plugins/admin) охватывает рабочий процесс администратора.

## Grant access to a private marketplace

Когда пользователь добавляет, устанавливает из или обновляет ваш marketplace, Claude Code запускает `git` на их машине с отключенными интерактивными подсказками и полагается на любые учетные данные, которые эта машина уже держит. Claude Code не имеет собственного git токена, и `marketplace.json` не имеет поля для него.

Вы выбираете, работает ли клон по SSH или HTTPS по форме команды добавления, которую вы отправляете пользователям:

* **GitHub `owner/repo`**: Claude Code проверяет `ssh -T git@github.com` и клонирует по SSH, когда проверка успешна. Если проверка не удается, или сам SSH клон не удается, он клонирует по HTTPS. Пользователи на машинах без ключа GitHub SSH могут установить `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`, чтобы пропустить проверку и клонировать по HTTPS.
* **`git@host:path.git`**: SSH.
* **`https://example.com/repo.git`**: HTTPS.

Скажите пользователям, что нужно каждому протоколу на их машине:

* **SSH**: ключ должен работать без подсказки парольной фразы, например потому что он загружен в `ssh-agent`. Хост должен уже быть в `known_hosts`.
* **HTTPS**: Claude Code оставляет git credential helper пользователя включённым, но запрещает ему выводить запросы и не запускает программы askpass, например заданную в `GIT_ASKPASS`. Учётные данные, которые helper уже хранит, работают; те, которые ему пришлось бы запросить, не работают. На GitHub сохранить их можно командой `gh auth login`, за которой следует `gh auth setup-git`.

Для хоста GitHub Enterprise Server пользователям нужен доступ git к этому хосту с их машины. Смотрите [Plugin marketplaces on GHES](https://code.claude.com/docs/ru/github-enterprise-server.md#plugin-marketplaces-on-ghes) для того, что каждой поверхности Claude Code нужно, чтобы достичь marketplace, размещенного на GHES.

Если вы распространяете через **Organization settings > Plugins & skills** на claude.ai вместо этого, учетные данные git ваших пользователей не задействованы. Смотрите [Distribute through organization settings](#distribute-through-organization-settings).

### Serve users who have no git-host account

Пользователи без учетной записи git-хоста могут добавить marketplace, который вы обслуживаете, как URL `marketplace.json` или из общего каталога, но они могут устанавливать только плагины, чьи источники записей они также могут достичь. Запись, которая указывает на приватный репозиторий `github`, все еще не работает при установке для них, потому что Claude Code получает его с тем же неинтерактивным `git`, который он использует для marketplace, размещенного на git.

Эти источники записей не нуждаются в учетной записи git:

* **`archive`**: zip-архив, загружаемый по HTTPS. Пользователям не нужны ни `git`, ни учётная запись, только сетевой доступ к URL. Закрепите каждый архив с помощью `sha256`, чтобы Claude Code отклонял изменённую загрузку. Чтобы передавать учётные данные при загрузке, см. [Аутентификация загрузок архивов](#authenticate-archive-downloads).
* **Публичный git-репозиторий**: Claude Code клонирует публичный источник `url` или `git-subdir` по HTTPS без учётных данных, если в записи указан URL `https://`. Для источника `github` или источника `git-subdir`, записанного как `owner/repo`, попросите пользователей без SSH-ключа GitHub установить `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.

Оставьте `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` в своих инструкциях, даже если `claude plugin install` без этой переменной успешно выполняется из оболочки на машине без SSH-ключа. Для источника `github` эта команда может самостоятельно переключиться на HTTPS, выведя `SSH not configured, cloning via HTTPS`. Установки через `/plugin` внутри сессии и обновления плагинов не переключаются, поэтому без этой переменной они завершаются ошибкой у пользователей, у которых нет SSH-ключа GitHub.

Для команды в одной сети marketplace `directory` на общей файловой системе также работает без учетных записей git. Пользователям нужен только доступ на чтение к пути.

### What background auto-update does with credentials

Background auto-update — это автоматическое обновление Claude Code для marketplaces и установленных плагинов после запуска сеанса. Оно отключено для вашего marketplace, пока пользователь или администратор его не включит, как описано в [Keep users up to date](#keep-users-up-to-date).

Когда оно включено для приватного marketplace, фоновая проверка новых коммитов использует помощников учетных данных git, настроенных пользователем, и никогда не подсказывает. Каждый вид удаленного и помощника дает другой результат:

* **SSH удаленные**: ключ, загруженный в `ssh-agent`, аутентифицирует проверку.
* **HTTPS удаленные с сохраненными учетными данными**: помощник, который может предоставить сохраненные учетные данные без подсказки, аутентифицирует проверку. Git Credential Manager, помощник macOS Keychain и `git-credential-store` работают таким образом, как только они держат учетные данные для хоста.
* **HTTPS удаленные с помощником, который нужно подсказать**: помощник не может ответить в фоне. Обновление не удается тихо и существующий checkout остается на месте, поэтому плагины пользователя продолжают работать из последнего синхронизированного состояния.

После проверки Claude Code делает одно из следующего:

* **Checkout актуален**: Claude Code оставляет его как есть.
* **Проверка находит новые коммиты, или не удается, потому что не может достичь или аутентифицировать удаленное**: Claude Code клонирует marketplace снова и заменяет существующий checkout новым клоном. Если этот клон не удается, существующий checkout остается на месте. Повторный клон может [истечь по времени на больших репозиториях](https://code.claude.com/docs/ru/plugins/troubleshooting.md#git-clone-timed-out-after-120s).

Чтобы держать приватный marketplace актуальным, пользователь может сделать одно из следующего:

* **Сохранить учетные данные**: сначала войдите в помощника учетных данных, чтобы он держал учетные данные для хоста. Для GitHub запустите `gh auth login`, затем `gh auth setup-git`.
* **Держать checkout при сбое**: если пользователь установит `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`, Claude Code держит существующий checkout без попытки повторного клона, когда фоновая проверка не может достичь или аутентифицировать удаленное. Плагины продолжают работать из последнего синхронизированного состояния.

Если пользователь установит `GITHUB_TOKEN` или другой токен поставщика в окружении, это само по себе не аутентифицирует фоновую проверку. Токен вступает в силу через помощника учетных данных, такого как помощник `gh` CLI, который читает `GH_TOKEN` и `GITHUB_TOKEN`.

## Roll out to a whole company

Развертывание плагина в компании включает вас как владельца marketplace, администратора, который контролирует управляемые параметры, и каждого человека, который использует Claude Code. Вы можете запустить развертывание без администратора, в этом случае каждый человек добавляет marketplace и устанавливает плагин сам.

| Кто | Что они делают | Где это рассматривается |
| :- | :- | :- |
| Вы, владелец marketplace | Держите каталог в репозитории, который может читать только компания, отправьте команду добавления для вашего хоста и скажите, что каждому человеку нужно на его машине | [Host your marketplace](#host-your-marketplace) и [Grant access to a private marketplace](#grant-access-to-a-private-marketplace) |
| Администратор | Регистрирует marketplace и включает его плагины для всех с `extraKnownMarketplaces` и `enabledPlugins` в управляемых параметрах, и устанавливает `autoUpdate` там | [Require a marketplace and its plugins](https://code.claude.com/docs/ru/plugins/org.md#require-a-marketplace-and-its-plugins) и [Set update policy](https://code.claude.com/docs/ru/plugins/org.md#set-update-policy) |
| Каждый человек | Нужен доступ на чтение к приватному git репозиторию, с учетными данными уже сохраненными на их машине. Без администратора они также запускают команды добавления и установки | [Add a private marketplace](https://code.claude.com/docs/ru/plugins/install.md#add-a-private-marketplace) |

Для людей, у которых нет учетной записи git-хоста, эти разделы каждый охватывают один способ их достичь:

* **Источники записей, которые не нуждаются в учетной записи git**: [Serve users who have no git-host account](#serve-users-who-have-no-git-host-account)
* **Предварительно заполненный каталог плагинов**: [Seed containers and CI](https://code.claude.com/docs/ru/plugins/org.md#seed-containers-and-ci), который также служит пользователям, у которых нет учетной записи git-хоста
* **claude.ai organization settings**: [Distribute through organization settings](#distribute-through-organization-settings), где учетные данные git ваших пользователей не задействованы

## Keep users up to date

Ваши изменения достигают пользователей через background auto-update, как только оно включено для вашего marketplace, или когда пользователи обновляют плагин сами. В обоих случаях пользователь получает новую копию плагина только когда его вычисленная версия изменяется, как описано в [Release a new version](#release-a-new-version).

### Turn on auto-update

Background auto-update отключен для вашего marketplace по умолчанию, и `marketplace.json` не имеет поля для его включения. Пользователь или администратор включает его:

* **Скажите пользователям включить его**: каждый пользователь идет в **Marketplaces** в `/plugin`, выбирает ваш marketplace и выбирает **Enable auto-update**.
* **Попросите администратора установить его**: если администратор установит `"autoUpdate": true` на записи `extraKnownMarketplaces` вашего marketplace в управляемых параметрах, оно включено для всех, кто получает эти параметры. Смотрите [Set update policy](https://code.claude.com/docs/ru/plugins/org.md#set-update-policy).

Без auto-update пользователи получают ваши изменения, когда они запускают `/plugin marketplace update <name>` в сеансе или `claude plugin update <plugin>@<name>` в оболочке.

Для того, что пользователи видят, когда обновление их достигает, смотрите [When auto-update runs](https://code.claude.com/docs/ru/plugins/loading.md#when-auto-update-runs).

### Release a new version

Чтобы выпустить новую версию пользователям, измените `version` плагина. Пользователи получают новую копию только когда вычисленная версия плагина отличается от той, которая у них есть. Эта версия поступает из `plugin.json` сначала, затем из записи marketplace, согласно [Versions and updates](https://code.claude.com/docs/ru/plugins/loading.md#versions-and-updates).

Плагин, который пользователи [загружают на месте](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk) из маркетплейса, добавленного ими по локальному пути, не контролируется `version`. Он загружает ваши текущие файлы при каждом запуске сессии, независимо от того, что говорит его строка версии.

Для каждой установки, кроме загрузки на месте или из источника `command`, либо увеличьте `version` при каждом выпуске, либо опустите его:

* **Увеличьте `version` при каждом выпуске**: пользователи остаются на своей кэшированной копии, пока строка не изменится. Если вы установите `"version": "1.0.0"` и отправите новые коммиты без изменения его, пользователи их не получат.
* **Опустите `version`**: пользователи отслеживают ваши коммиты вместо этого. Оставьте `version` вне обоих `plugin.json` и записи marketplace.

Не устанавливайте `version` в обоих `plugin.json` и записи marketplace. Если вы это сделаете, Claude Code использует значение `plugin.json` без предупреждения, и `claude plugin validate` сообщает о несоответствии как `Entry declares version "<a>" but <path>/plugin.json says "<b>"`.

### Hold users on one version

Чтобы удержать пользователей на определённой версии, выберите, какой ref, коммит или тег они получают:

* **`ref` и `sha` на записи плагина**: `ref` называет ветку или тег и `sha` называет коммит для источника `github`, `url` или `git-subdir`. Смотрите [Plugin sources](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-sources).
* **`#<ref>` на команде добавления**: пользователи, которые добавляют `your-org/your-marketplace#stable`, получают эту ветку или тег каталога. Для двух линий выпуска одновременно, смотрите [Run release channels](#run-release-channels).
* **`<plugin>--v<version>` теги**: диапазон версий зависимости разрешается против этих тегов. Смотрите [Release a plugin that others depend on](https://code.claude.com/docs/ru/plugins/dependencies.md#tag-plugin-releases-for-version-resolution).

[Release a new version](#release-a-new-version) говорит, когда измененная запись достигает пользователей.

### Change the command of a command source

Если вы измените `command` источника [`command`](https://code.claude.com/docs/ru/plugins/marketplace-reference#command-plugin-source), или переключите его `mode`, каждый пользователь должен принять новую команду перед тем, как Claude Code ее запустит. Claude Code запускает только точную команду, которую пользователь принял, когда установил или последний раз обновил плагин.

После того как копия marketplace пользователя подхватит изменение, этот пользователь видит следующее:

* **Нет больше фоновых запусков**: [однократный запуск в сеансе](https://code.claude.com/docs/ru/plugins/loading.md#when-a-command-source-re-runs) команды останавливается для этого пользователя, поэтому новый вывод инструмента не достигает их.
* **Запись на вкладке `/plugin` Errors**: запись показывает новую команду и команду `claude plugin update` для запуска.

Скажите пользователям запустить команду `claude plugin update`, которую показывает эта запись, в терминале. Claude Code показывает им новую команду и просит ее принять.

## Run release channels

Чтобы предложить стабильные и ранние дорожки доступа, разместите два маркетплейса, чьи записи указывают на разные refs одного плагина, и позвольте каждому пользователю добавить тот, который он хочет.

Дайте двум файлам `marketplace.json` разные значения `name`. Claude Code идентифицирует marketplace по его `name`, поэтому пользователь не может иметь два marketplace с одинаковым именем, зарегистрированные одновременно.

С этими двумя каталогами пользователи, которые добавляют `stable-tools`, устанавливают `code-formatter` из ветки `stable`, и пользователи, которые добавляют `latest-tools`, устанавливают его из `latest`:

```json theme={null}
{
  "name": "stable-tools",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": { "source": "github", "repo": "your-org/code-formatter", "ref": "stable" } }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": { "source": "github", "repo": "your-org/code-formatter", "ref": "latest" } }
  ]
}
```

Дайте двум refs разные версии `plugin.json`, или опустите `version`, чтобы SHA коммита их различал. Обновления обнаруживаются путем сравнения версий, поэтому ref, который движется без изменения версии, оставляет пользователей на кэшированной копии.

Чтобы назначить каналы группам пользователей вместо того, чтобы позволить пользователям выбирать, администратор дает каждой группе соответствующую запись `extraKnownMarketplaces`, как описано в [Set update policy](https://code.claude.com/docs/ru/plugins/org.md#set-update-policy).

## Переименование или удаление плагина

`name` плагина — это его идентификатор. Пользователи ссылаются на него в ключах настроек `enabledPlugins` и `pluginConfigs` и в `/plugin install`, поэтому его изменение нарушает каждую существующую установку.

Чтобы изменить метку, которую пользователи видят в `/plugin`, без нарушения чего-либо, установите `displayName` в `plugin.json` и оставьте `name` без изменений.

### Миграция пользователей с помощью карты переименований

Когда вы должны изменить `name`, добавьте карту верхнего уровня `renames` в `marketplace.json`, чтобы Claude Code перенёс существующих пользователей вместо того, чтобы сообщать об ошибке [`Plugin "<name>" not found in marketplace`](https://code.claude.com/docs/ru/plugins/troubleshooting#plugin-not-found-in-marketplace). Сделайте то же самое, когда вы удаляете запись из `plugins`.

Сопоставьте каждое прежнее имя с его текущим именем или с `null`, когда плагин удалён. Этот marketplace переименовывает `formatter` в `code-formatter` и записывает, что `legacy-linter` был удалён:

```json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": "./plugins/code-formatter" }
  ],
  "renames": {
    "formatter": "code-formatter",
    "legacy-linter": null
  }
}
```

После того как вы отправите изменения, пользователь, у которого всё ещё включено старое имя, увидит один из этих результатов:

* **Переименованная запись**: плагин загружается под своим новым именем. `claude plugin list` и детали плагина в `/plugin` показывают `Renamed to "code-formatter" in the "your-marketplace" marketplace` один раз, и Claude Code переписывает старый ключ на новый в `enabledPlugins` и `pluginConfigs` в пользовательских, проектных и локальных областях настроек.
* **Запись `null`**: старый ключ удаляется из этих областей и пользователь видит `Removed from the "your-marketplace" marketplace`.
* **Включено в управляемые настройки**: плагин всё ещё загружается под своим новым именем, но Claude Code не может переписать управляемые настройки, поэтому уведомление повторяется до тех пор, пока администратор не обновит `enabledPlugins` там.

Для marketplace, который пользователи добавили из репозитория git или URL, переименованный плагин сообщает об ошибке [`Plugin "<name>" not cached at <path>`](https://code.claude.com/docs/ru/plugins/troubleshooting#plugin-not-cached-at) до тех пор, пока пользователь не запустит `/plugin install code-formatter@your-marketplace` один раз в сеансе.

Рассматривайте `renames` как историю только для добавления. Сохраняйте старые записи после того, как все перейдут. Когда вы переименуете снова, добавьте вторую запись вместо редактирования первой, потому что Claude Code следует цепочке от самого старого имени.

В вашей оболочке запустите `claude plugin validate .` после редактирования карты. Она отклоняет цепочку, которая циклится или заканчивается где-либо, кроме `null` или имени в `plugins`, с ошибкой `renames.<name>: chain does not resolve`.

### Удаление удалённых плагинов с машин пользователей

Чтобы удалить удалённый плагин с машин пользователей вместо того, чтобы оставить копию, установите `"forceRemoveDeletedPlugins": true` на верхнем уровне `marketplace.json`. Без этого поля удалённый плагин остаётся установленным и сообщает об ошибке `Plugin "<name>" not found in marketplace` при загрузке сеанса. С ним Claude Code выполняет следующее при каждом запуске сеанса:

1. Сравнивает то, что пользователи установили из вашего marketplace, с записями и картой `renames`, и рассматривает любой плагин, который ни указан в списке, ни переименован, как удалённый.
2. Удаляет каждый удалённый плагин из пользовательской, проектной и локальной областей. Плагины, которые установили только управляемые настройки, остаются на месте.
3. Перечисляет каждый удалённый плагин под заголовком **Flagged** в `/plugin` со статусом `Removed from marketplace`.

## Authenticate archive downloads

Чтобы аутентифицировать загрузку [`archive`](https://code.claude.com/docs/ru/plugins/marketplace-reference#archive-plugin-source), такую как загрузка из приватного реестра, установите HTTP заголовки, которые Claude Code отправляет с ней. Вы можете установить `headers` в одном из этих мест:

* **Источник `url` marketplace**: источник `url`, из которого вы зарегистрировали marketplace, такой как запись [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces).
* **Запись плагина**: на Claude Code v2.1.238 или позже, вы можете установить его на записи `marketplace.json` плагина вместо этого, рядом с `source`.

В любом месте установите команду `headersHelper` вместо `headers`, когда значение недолговечно, такое как токен, который ваш реестр генерирует по запросу. Claude Code запускает команду и отправляет объект JSON, который она выводит, как заголовки этого места. Требует Claude Code v2.1.238 или позже.

[Справочник marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries) перечисляет поля записи `headers` и `headersHelper`.

Место, которое вы выбираете, решает, какие загрузки получают заголовки и когда Claude Code запускает команду:

| Место | Загрузки, которые получают заголовки | Когда Claude Code запускает `headersHelper`, установленный там |
| :- | :- | :- |
| Источник `url` Marketplace | Загрузки архива на происхождении URL marketplace, означая ту же схему, хост и порт | Перед каждой выборкой `marketplace.json` marketplace и перед каждой загрузкой архива на этом происхождении. Claude Code переиспользует вывод одного запуска до 60 секунд |
| Запись плагина | Только загрузка этой записи | Только когда пользователь устанавливает или обновляет этот один плагин сам по себе и [принимает команду](#how-users-accept-a-headershelper-command) |

Где оба места устанавливают заголовок с одинаковым именем, Claude Code отправляет значение записи. В одном месте заголовок, который команда выводит, переопределяет заголовок с одинаковым именем, указанный в `headers`.

### Add a headersHelper to a plugin entry

Эта запись устанавливает `headersHelper` рядом с `source`. Она также устанавливает [`"strict": false`](https://code.claude.com/docs/ru/plugins/marketplace-reference#strict-mode), что Claude Code требует от записи `marketplace.json`, которая устанавливает `headersHelper`:

```json theme={null}
{
  "name": "my-plugin",
  "description": "Formatting commands for internal services",
  "strict": false,
  "source": {
    "source": "archive",
    "url": "https://registry.example.com/plugins/my-plugin-2.1.0.zip"
  },
  "headersHelper": "/opt/bin/mint-registry-token.sh"
}
```

Чтобы проверить запись, запустите `claude plugin install my-plugin@your-marketplace` в вашей оболочке. Claude Code показывает вам команду и URL архива и загружает zip после того как вы принимаете.

### Write the headersHelper command

Независимо от того, устанавливаете ли вы `headersHelper` на источник `url` marketplace или на запись плагина, напишите команду, чтобы соответствовать этим требованиям:

* **Текст команды**: максимум 500 символов печатного ASCII, без запуска четырех или более пробелов.
* **Вывод**: выведите один объект JSON имен заголовков и строковых значений на stdout, затем выйдите 0 в течение 10 секунд.
* **Оболочка и рабочий каталог**: Claude Code запускает команду через `sh`, или через `cmd.exe` на Windows. Рабочий каталог — это каталог конфигурации, который является `~/.claude` или [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars#variables). Дайте абсолютный путь или команду на `PATH`, потому что относительный путь разрешается против этого каталога, а не проекта пользователя.
* **Переменные, которые Claude Code удаляет**: когда команда установлена в записи `marketplace.json`, или в проектном `.claude/settings.json` или `.claude/settings.local.json`, Claude Code удаляет из окружения каждую переменную, чье имя выглядит как учетные данные, по [тому же правилу, которое оно применяет к MCP `headersHelper`](https://code.claude.com/docs/ru/mcp#which-variables-a-helper-can-read). `ANTHROPIC_API_KEY` и `MY_REGISTRY_TOKEN` оба удаляются, поэтому имейте команду, читающую свои учетные данные из файла или хранилища учетных данных. Это удаление не применяется к команде, установленной в пользовательских параметрах, файле `--settings` или управляемых параметрах.
* **Переменные, которые Claude Code устанавливает**: `CLAUDE_CODE_MARKETPLACE_URL` и `CLAUDE_CODE_MARKETPLACE_NAME` для команды источника `url`, и `CLAUDE_CODE_PLUGIN_NAME` и `CLAUDE_CODE_PLUGIN_ARCHIVE_URL` для команды записи. `CLAUDE_CODE_MARKETPLACE_NAME` не установлена при первой выборке после того как пользователь добавляет marketplace по URL, потому что эта выборка — это то, что поставляет имя.

Команда, которая чеканит токен носителя, выводит объект, подобный этому:

```json theme={null}
{"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9"}
```

### When Claude Code skips a headersHelper command or drops its output

Команда `headersHelper` не запускается, или заголовки из `headers` или из вывода команды удаляются, когда применяется одно из следующего:

* **Команда не удается**: если команда выходит ненулевой, работает более 10 секунд, или выводит что-либо, кроме объекта JSON строковых значений, выборка или загрузка, для которой команда была запущена, не происходит.
* **URL Marketplace не начинается с `https://`**: команда этого источника `url` не запускается, и запросы несут только заголовки, указанные в его поле `headers`.
* **Перенаправление оставляет происхождение**: когда загрузка перенаправляется с происхождения URL архива, перенаправленный запрос не несет значения `headers` или вывод команды ни от источника `url` marketplace, ни от записи плагина.
* **Запись устанавливает заголовок маршрутизации или идентификации**: Claude Code удаляет имена маршрутизации запросов и идентификации клиента, такие как `Host`, `Cookie` и `X-Forwarded-*`, из `headers` записи и вывода команды, и держит имена аутентификации, такие как `Authorization`. Каждая запись `marketplace.json` фильтруется таким образом. Для встроенной записи плагина в параметрах, смотрите [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces).
* **Команда установлена в параметрах каталога `--add-dir`**: команда игнорируется, на источнике `url` и на [встроенной записи плагина](https://code.claude.com/docs/ru/settings-reference.md#extraknownmarketplaces) одинаково, и только `headers` этого файла отправляются.
* **Управляемые параметры блокируют команду**: установка [`disableCommandPluginSources`](https://code.claude.com/docs/ru/settings-reference#disablecommandpluginsources) на `true` блокирует команды `headersHelper`, и [`allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#allowmanagedhooksonly) блокирует их тоже, если `disableCommandPluginSources` явно не `false`. Под любым блоком Claude Code все еще запускает команду для marketplace, который сами управляемые параметры объявляют.

### How users accept a headersHelper command

Пользователь принимает команду записи плагина каждый раз, когда устанавливает или обновляет этот плагин отдельно. Claude Code показывает команду и URL архива и запускает команду только после того, как пользователь её примет.

Пользователи могут установить или обновить плагин в сессии Claude Code в терминале, в своей оболочке без запущенной сессии или в расширении VS Code:

* **Сессия в терминале**: из собственного представления плагина в `/plugin`.
* **Оболочка**: с помощью `claude plugin install` или `claude plugin update`.
* **Расширение VS Code**: из [диалога **Manage plugins**](https://code.claude.com/docs/ru/vs-code.md#manage-plugins) в версии расширения 2.1.290 или более поздней.

В неинтерактивной оболочке передайте [`--yes`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-install), чтобы принять команду. Чтобы принять только команду, которую предыдущий запуск `--json` отобразил, передайте [`--accept-command`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-install) с `sha256`, который запуск сообщил.

Claude Code запускает только ту команду, которую показал, и только для того URL архива, который показал. Если за это время команда записи или URL архива изменились, Claude Code отказывает в установке или обновлении. Изменение одной лишь строки запроса не учитывается, за исключением расширения VS Code или использования `--accept-command`.

### Installs and updates that refuse a command instead of asking

На любой операции, кроме установки или обновления одного плагина, Claude Code ни не запускает команду записи, ни не загружает ее архив. Плагин остается на его установленной версии или остается неустановленным, и пользователь видит один из этих результатов:

* **Установка нескольких плагинов одновременно, из предложения плагина, или как зависимость другого плагина**: Claude Code отказывает плагину, который имеет команду, и направляет пользователя к собственному представлению этого плагина в `/plugin`. Другие плагины в массовой установке все еще устанавливаются. Плагин, который зависит от отказанного плагина, не устанавливается, пока пользователь не установит отказанный плагин сам по себе.
* **Background auto-update, или запуск сеанса для плагина, чей архив никогда не был загружен**: Claude Code перечисляет плагин на вкладке `/plugin` Errors, чтобы пользователь знал, чтобы установить или обновить его сам.

### When a marketplace `url` source's command runs

Вы объявляете команду `headersHelper` источника `url` marketplace в файле параметров, такой как запись [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces), вместо каталога, который marketplace публикует. Claude Code поэтому не просит пользователя принять его при каждой установке или обновлении. Вместо этого файл параметров, который объявляет его, решает, когда Claude Code запускает его:

| Файл параметров | Когда Claude Code запускает команду |
| :- | :- |
| Пользовательские параметры, файл `--settings` или файл управляемых параметров на машине | Без запроса, включая во время фонового обновления marketplace |
| Проектный `.claude/settings.json` или `.claude/settings.local.json` | Только после того как пользователь принимает [диалог доверия рабочей области](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) для этой папки самой. Сеанс `-p` или SDK не считается принятием его, и ни доверие, предоставленное родительской папке |
| Управляемые параметры сервера | В интерактивном сеансе, только после того как пользователь одобряет доставленные параметры в [диалоге одобрения безопасности](https://code.claude.com/docs/ru/server-managed-settings.md#security-approval-dialogs) |

Для [встроенной записи плагина](https://code.claude.com/docs/ru/settings-reference.md#extraknownmarketplaces) в одном из этих файлов Claude Code требует того же доверия папки или одобрения параметров, что и для команды уровня marketplace в этом файле, и пользователь также принимает команду записи при каждой установке или обновлении.

## Depend on and recommend other plugins

Запись может объявить зависимости от других плагинов.

* **Диапазоны версий**: зависимость может нести диапазон semver.
* **Кросс-marketplace зависимости**: зависимость от другого marketplace устанавливается только когда ваш marketplace перечисляет этот marketplace в `allowCrossMarketplaceDependenciesOn`.

Для диапазонов версий, соглашение git-тега `<plugin>--v<version>`, против которого они разрешаются, и кросс-marketplace доверие, смотрите [Plugin dependencies](https://code.claude.com/docs/ru/plugins/dependencies.md).

Чтобы Claude Code предлагал плагин, когда проект ему соответствует, добавьте в запись блок `relevance` с сигналами, которые идентифицируют проект. Пользователи видят эти предложения только в том случае, если администратор указал ваш маркетплейс в `pluginSuggestionMarketplaces`. О сигналах и шаге включения см. [Релевантность плагинов](https://code.claude.com/docs/ru/plugins/relevance.md).

## Work around what a marketplace can't do

Некоторые вещи, которые владельцы просят, не имеют поля в `marketplace.json`. Вот ближайший вариант для каждого:

* **Ограничить то, что еще устанавливают пользователи**: список разрешений marketplace — это управляемый параметр, `strictKnownMarketplaces`. Смотрите [Restrict what users can install](https://code.claude.com/docs/ru/plugins/org.md#restrict-what-users-can-install).
* **Установить или включить плагин без того, чтобы пользователь просил**: ни одно поле записи не устанавливает плагин. Управляемый `enabledPlugins` делает это для флота; смотрите [Pre-install and require plugins](https://code.claude.com/docs/ru/plugins/org.md#pre-install-and-require-plugins).
* **Показать разные записи разным пользователям**: записи не несут поле аудитории, и каждый пользователь, который добавляет marketplace, видит весь каталог. Разместите отдельные marketplaces для отдельных аудиторий.
* **Отметить плагин устаревшим**: нет состояния устаревания. Вариант — удалить запись, сопоставить ее имя с `null` в `renames` и опционально установить `forceRemoveDeletedPlugins`.
* **Включить auto-update для ваших пользователей**: каждый пользователь включает его в **Marketplaces** в `/plugin`, или администратор устанавливает `autoUpdate` в управляемых параметрах. Смотрите [Turn on auto-update](#turn-on-auto-update).
* **Нести git учетные данные**: ни одно поле marketplace не держит git токен. Доступ к marketplace или плагину, размещенному на git, следует настройке git пользователя, согласно [Grant access to a private marketplace](#grant-access-to-a-private-marketplace). Для источников `archive`, запись может установить [`headers` или `headersHelper`](#authenticate-archive-downloads) вместо этого.

## Next steps

* [Marketplace reference](https://code.claude.com/docs/ru/plugins/marketplace-reference.md): поля `marketplace.json`, типы источников и сообщения валидации
* [Manage plugins for your organization](https://code.claude.com/docs/ru/plugins/org.md): требуйте, ограничивайте или заполняйте ваш marketplace на машинах вашей организации
* [Plugin dependencies](https://code.claude.com/docs/ru/plugins/dependencies.md): отмечайте выпуски, чтобы плагины, которые зависят от вашего, могли разрешать версии
* [Troubleshoot plugins](https://code.claude.com/docs/ru/plugins/troubleshooting.md): ошибки, которые видят ваши пользователи при добавлении или обновлении из вашего marketplace
