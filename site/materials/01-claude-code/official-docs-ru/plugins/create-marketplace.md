> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Создание marketplace

> Создайте plugin marketplace из файла marketplace.json и протестируйте его локально перед размещением.

Plugin marketplace — это каталог или репозиторий с файлом `.claude-plugin/marketplace.json`, который содержит список ваших плагинов и указывает, откуда их загружать. Вы отправляете каталог на хост git, и любой, у кого есть доступ, регистрирует его в Claude Code одной командой и устанавливает ваши плагины из него.

Создавайте собственный marketplace, когда вы хотите, чтобы выбранная вами группа, например ваша команда или организация, устанавливала ваши плагины и продолжала получать ваши обновления из каталога, который вы контролируете. Репозиторий может быть приватным, он может содержать столько плагинов, сколько вам нужно, и администратор может [требовать его на каждой машине](https://code.claude.com/docs/ru/plugins/org.md).

> [!NOTE]
>
> Эти случаи рассмотрены на других страницах:
>
> * **Совместное использование одного плагина с несколькими людьми**: отправьте им каталог плагина или его `.zip`. См. [Совместное использование плагина без marketplace](https://code.claude.com/docs/ru/plugins/publish.md#share-a-plugin-without-a-marketplace).
> * **Предложение плагина всем**: отправьте его в community marketplace Anthropic. См. [Отправка в community marketplace](https://code.claude.com/docs/ru/plugins/publish.md#submit-to-anthropics-directory).
> * **Использование плагина самостоятельно**: загрузите его с помощью `--plugin-dir` или сохраните в каталог skills. См. [Разработка без marketplace](https://code.claude.com/docs/ru/plugins/create.md#develop-without-a-marketplace).

Начните с [Создание marketplace](#create-a-marketplace), чтобы создать его на своей машине и установить плагин из него, затем [добавьте больше записей плагинов](#add-plugin-entries).

## Create a marketplace

Следующие шаги создают marketplace на вашей машине, добавляют плагин в него, регистрируют его в Claude Code и устанавливают плагин из него. Это весь цикл, и это тот же цикл, через который проходят ваши пользователи после того, как вы разместите marketplace где-то, где они смогут его достичь. Запустите каждую команду в своей оболочке из каталога, где вы хотите создать `my-marketplace/`.

Вам нужен плагин для списка. Пример использует `my-first-plugin` из [Создание вашего первого плагина](https://code.claude.com/docs/ru/plugins/create.md#create-your-first-plugin), плагин с одним skill, который вы запускаете как `/my-first-plugin:hello`; создайте его сначала, если у вас еще нет плагина. Чтобы использовать свой плагин, замените его каталог и его `name` везде, где в шагах говорится `my-first-plugin`. О том, что может содержать каталог плагина, см. [обозреватель каталога плагина](https://code.claude.com/docs/ru/plugins/components.md#explore-the-plugin-directory).

**1. Настройка каталога marketplace**

Marketplace — это каталог с файлом `.claude-plugin/marketplace.json`, плюс плагины, которые он содержит. Создайте каталог marketplace и его папку `.claude-plugin/`, затем скопируйте ваш плагин в `plugins/`:

```bash theme={null}
mkdir -p my-marketplace/.claude-plugin my-marketplace/plugins
cp -r my-first-plugin my-marketplace/plugins/
```

Проверьте, что плагин действителен в его текущем расположении, чтобы любая последующая ошибка была о marketplace, а не о плагине:

```bash theme={null}
claude plugin validate ./my-marketplace/plugins/my-first-plugin
```

Последняя строка вывода читается `✔ Validation passed`.

**2. Создание файла marketplace**

Сохраните `marketplace.json` в `my-marketplace/.claude-plugin/marketplace.json`. Файл требует `name`, `owner` и массив `plugins`.

Каждый объект в `plugins` — это запись плагина и требует `name` и `source`. Напишите `source` записи как путь от корня marketplace. Корень — это `my-marketplace/`, каталог, который содержит `.claude-plugin/`.

```json my-marketplace/.claude-plugin/marketplace.json theme={null}
{
  "name": "my-marketplace",
  "description": "Plugins for my team",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "my-first-plugin",
      "source": "./plugins/my-first-plugin",
      "description": "A greeting plugin to learn the basics"
    }
  ]
}
```

**3. Валидация marketplace**

Запустите `claude plugin validate` на каталоге marketplace, чтобы проверить синтаксис JSON, требуемые поля и каждую запись плагина в его `.claude-plugin/marketplace.json`.

```bash theme={null}
claude plugin validate ./my-marketplace
```

Для файла, написанного на шаге 2, последняя строка вывода читается `✔ Validation passed`.

**4. Добавление marketplace и установка плагина**

Зарегистрируйте каталог как marketplace.

```bash theme={null}
claude plugin marketplace add ./my-marketplace
```

Команда выводит `✔ Successfully added marketplace: my-marketplace (declared in user settings)`, что означает, что marketplace записан в ваш файл пользовательских настроек.

Установите плагин. ID установки — это `name` записи, `@` и `name` marketplace.

```bash theme={null}
claude plugin install my-first-plugin@my-marketplace
```

Команда выводит `✔ Successfully installed plugin: my-first-plugin@my-marketplace (scope: user)`.

Внутри сеанса `/plugin marketplace add ./my-marketplace` регистрирует marketplace таким же образом. `/plugin install my-first-plugin@my-marketplace` открывает детали плагина в панели `/plugin`, где вы его устанавливаете. Для этого потока см. [Установка и управление плагинами](https://code.claude.com/docs/ru/plugins/install.md).

**5. Подтверждение загрузки плагина**

Список установленных плагинов.

```bash theme={null}
claude plugin list
```

Вывод содержит `my-first-plugin@my-marketplace` с `Status: ✔ enabled`.

Чтобы увидеть, что загрузил плагин, покажите его детали.

```bash theme={null}
claude plugin details my-first-plugin
```

Раздел `Component inventory` читается `Skills (1)  hello`.

Чтобы запустить skill, начните сеанс и введите `/my-first-plugin:hello`. Claude приветствует вас. Команда имеет имя плагина в качестве префикса, как и каждый skill плагина.

## Add plugin entries

Каждый плагин, который вы распространяете, — это один объект в массиве `plugins` файла `marketplace.json`. Чтобы добавить второй плагин, добавьте второй объект. Эти поля охватывают большинство записей:

* `name`: идентификатор, который люди вводят перед `@` при установке. [Записи плагинов](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries) указывает символы, которые может использовать имя.
* `source`: откуда Claude Code загружает плагин. Напишите строку относительного пути для плагина внутри каталога marketplace, как в [пошаговом руководстве](#create-a-marketplace), или объект source для плагина вне его. См. [Выбор источника плагина](#choose-a-plugin-source).
* `description`: строка, которую люди видят рядом с плагином при просмотре вашего marketplace в `/plugin`.

Полный список полей см. в разделе [Записи плагинов](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries), где также описаны поля [`plugin.json`](https://code.claude.com/docs/ru/plugins/manifest-reference), которые может задавать запись, и случаи, когда они применяются.

## Rules for plugin entries

Большинство неудачных установок из нового marketplace происходят из-за относительного пути, написанного из неправильного каталога, или из-за имени записи, которое отличается от `name` в `plugin.json` плагина.

### Write relative paths from the marketplace root

Корень marketplace — это каталог, который содержит `.claude-plugin/`. В [пошаговом руководстве](#create-a-marketplace) это `my-marketplace/`, поэтому `source` записи — это `"./plugins/my-first-plugin"`. Путь не начинается внутри `.claude-plugin/`, поэтому не используйте `..` для выхода из него.

Путь с `..` и путь к отсутствующему каталогу не работают в разных командах:

* **Путь с `..`**: `claude plugin validate` сообщает о записи как недействительной. Сообщение начинается с `Path contains "..": ./../plugins/my-first-plugin`.
* **Путь к каталогу, который не существует**: `claude plugin validate` проходит. `claude plugin install` не работает с `Source path does not exist: <path>`, и `<path>` — это абсолютное расположение, которое проверил Claude Code.

### Keep the entry name and the manifest name the same

Plugin marketplace имеет запись `name` в `marketplace.json` и `name` в его собственном `plugin.json`, называемый именем манифеста. Каждое имя появляется в разных местах:

* **Имя записи**: ID установки, `<entry-name>@<marketplace>`. Это то, что люди вводят для установки, что показывает `claude plugin list`, и ключ, который Claude Code записывает под [`enabledPlugins`](https://code.claude.com/docs/ru/settings-reference#enabledplugins) в их файле настроек.
* **Имя манифеста**: префикс на skills плагина и имя, которое принимает `claude plugin details`.

Когда два имени отличаются и кто-то устанавливает по имени манифеста, Claude Code сообщает `Plugin "<manifest-name>" not found in marketplace "<marketplace>"`. Держите два имени одинаковыми. Для получения дополнительной информации о том, как Claude Code использует два имени, см. [Справочник по загрузке плагинов](https://code.claude.com/docs/ru/plugins/loading.md#find-where-a-plugin-came-from).

### Не допускайте неиспользуемые подмодули в клон

Когда кто-то добавляет ваш маркетплейс, Claude Code клонирует репозиторий и загружает только те подмодули git, которые содержат файлы плагинов. Требуется Claude Code v2.1.295 или более поздней версии.

Вы определяете, какие подмодули загружает Claude Code, тем, где размещаете каждый плагин:

* **Плагин в подкаталоге**: Claude Code загружает подмодули внутри каталога плагина и подмодуль, который его содержит. Поместите подмодуль, который нужен вашему плагину, внутрь каталога плагина, а ненужный держите за его пределами
* **Плагин в корне маркетплейса**: Claude Code загружает все подмодули репозитория, как только один из файлов плагина ссылается на путь внутри любого из них. Если в вашем репозитории есть большой подмодуль, который использует только ваша сборка, переместите плагин в подкаталог

Если плагин в корне запускает файл из подмодуля, явно пропишите путь к файлу в конфигурации хука или сервера плагина, например `${CLAUDE_PLUGIN_ROOT}/vendor/tool/run.sh`. Claude Code читает эти пути, чтобы определить, нужны ли плагину подмодули. Он не видит путь, который скрипт формирует во время выполнения.

Полное правило см. в разделе [Подмодули Git в репозитории маркетплейса](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#git-submodules-in-the-marketplace-repository).

## Choose a plugin source

Каждая запись плагина в `marketplace.json` имеет `source`, который говорит Claude Code, откуда загружать этот плагин. Выберите источник по тому, где хранятся файлы плагина. Таблица содержит источники, которые используют большинство владельцев marketplace.

| Source | Use it when | Minimal `source` value |
| :- | :- | :- |
| Relative path | Файлы плагина находятся внутри самого каталога marketplace | `"./plugins/my-first-plugin"` |
| `github` | Плагин — это собственный репозиторий GitHub | `{ "source": "github", "repo": "your-org/my-first-plugin" }` |
| `git-subdir` | Плагин — это подкаталог какого-то другого репозитория, например monorepo | `{ "source": "git-subdir", "url": "your-org/monorepo", "path": "tools/my-first-plugin" }` |

В источнике `git-subdir` `url` принимает URL git или сокращение GitHub `owner/repo`.

Плагин также может поступать из одного из этих типов источников:

* `url`: git репозиторий по URL на любом хосте
* `archive`: zip файл, загруженный через HTTPS
* `npm`: npm пакет
* `command`: каталог, созданный путем запуска команды на машине, где установлен плагин

Для полей каждого типа источника и для привязки источника на основе git к `ref` или `sha`, см. [Источники плагинов](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-sources).

## Validate and test

По мере добавления плагинов запускайте `claude plugin validate ./my-marketplace` в своей оболочке после каждого редактирования и устанавливайте из marketplace на своей машине перед тем, как поделиться им. Валидация и установка выявляют разные проблемы.

### Problems that validation reports

`claude plugin validate` читает только файлы внутри каталога marketplace. Он сообщает:

* Ошибки синтаксиса JSON, как `json: Invalid JSON syntax: <reason>`
* Отсутствующие требуемые поля, такие как `owner: Invalid input`
* Имя marketplace или плагина, которое нарушает правила именования в [справочнике marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#top-level-fields)
* Относительный `source`, содержащий `..`
* Неизвестные поля на верхнем уровне или в записи плагина, как предупреждения
* Проблемы в `plugin.json` каждого плагина с относительным путем, как `plugins[N] plugin.json → <field>: <message>`

Для каждого сообщения, которое может вывести `validate`, см. [Сообщения валидации](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#validation-messages). Для его флагов и кодов выхода см. [`plugin validate`](https://code.claude.com/docs/ru/plugins/cli-reference#plugin-validate).

### Problems that surface when you add or install

Проблемы, которые `claude plugin validate` не сообщает, появляются при добавлении marketplace или установке из него:

* **При добавлении marketplace**: точные [официальные имена marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#reserved-names), такие как `claude-plugins-official`, проходят валидацию. Когда вы добавляете marketplace с одним из этих имен, Claude Code отказывает ему с сообщением, которое начинается с `The name '<name>' is reserved for official Anthropic marketplaces`.
* **При установке плагина**:
  * Claude Code сначала загружает источник `github`, `git-subdir` или другой удаленный источник при установке плагина, поэтому неправильный `repo` или `path` появляется тогда.
  * Относительный `source`, чей каталог не существует, также не работает при установке, с `Source path does not exist: <path>`.

### Test an edit to a plugin

В [пошаговом руководстве](#create-a-marketplace) вы добавили `my-marketplace` из локального каталога с относительным путем `source`. С этой настройкой Claude Code читает файлы плагина непосредственно из `my-marketplace/plugins/`. Ваши изменения вступают в силу при следующем запуске сеанса или при запуске `/reload-plugins` в сеансе, без изменения `version` плагина.

Люди, которые устанавливают из вашего размещенного marketplace, получают копию в кэше плагина вместо этого. О том, как они получают новую версию, см. [Держите пользователей в курсе](https://code.claude.com/docs/ru/plugins/host-marketplace.md#keep-users-up-to-date).

### Remove the marketplace to start over

Чтобы удалить все и начать заново, запустите `claude plugin marketplace remove my-marketplace` в своей оболочке. Команда удаляет marketplace и удаляет его плагины.

## Host your marketplace

После того как вы сможете установить плагин из маркетплейса на своей машине, как в разделе [Создание маркетплейса](#create-a-marketplace), отправьте каталог маркетплейса на Git-хостинг. Перед отправкой задайте маркетплейсу `name` верхнего уровня, который другие авторы вряд ли выберут, потому что у пользователя [не может быть двух маркетплейсов с одинаковым именем](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#marketplace-file).

Ваши товарищи по команде затем запускают `claude plugin marketplace add <owner>/<repo>` в своей оболочке для репозитория GitHub или ту же команду с URL репозитория. Затем они устанавливают плагин по имени, как в [пошаговом руководстве](#create-a-marketplace).

Для доступа к приватному репозиторию, обновлений, версионирования и переименования или удаления записей см. [Размещение и поддержка marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md).

## Следующие шаги

* [Размещение и поддержка marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md): выберите хост, держите пользователей в курсе и безопасно переименовывайте или удаляйте плагины
* [Справочник Marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md): поля `marketplace.json` и типы источников
* [Управление плагинами для вашей организации](https://code.claude.com/docs/ru/plugins/org.md): требуйте ваш marketplace и его плагины на каждой машине
* [Предложение плагинов по релевантности](https://code.claude.com/docs/ru/plugins/relevance.md): настройте Claude Code так, чтобы он предлагал плагин из вашего marketplace, когда сеанс соответствует критериям
