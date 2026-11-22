> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник Marketplace

> Полный справочник по полям marketplace.json, записям плагинов и объектам источников плагинов и marketplace, с указанием того, где каждый из них действителен.

`marketplace.json` — это файл, который определяет marketplace плагинов. Он содержит имя marketplace, его владельца и одну запись для каждого плагина. Источник плагина каждой записи указывает, откуда Claude Code загружает этот плагин.

Источник marketplace — это отдельный объект, который указывает, откуда Claude Code загружает сам файл marketplace. Вы пишете его в параметрах, или Claude Code создаёт его при запуске `claude plugin marketplace add`.

Этот справочник предназначен для разработчиков marketplace, которым нужно точное имя или значение поля, и для администраторов, которым нужно знать, какие значения `source` действительны в [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces), [`strictKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#strictknownmarketplaces) и [`blockedMarketplaces`](https://code.claude.com/docs/ru/plugins/org#restrict-what-users-can-install).

> [!NOTE]
>
> Эти случаи рассмотрены на других страницах:
>
> * **Создание или размещение marketplace**: см. [Создание marketplace](https://code.claude.com/docs/ru/plugins/create-marketplace.md) и [Размещение и поддержка marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md)
> * **Рецепты списков разрешений и запретов**: см. [Управление плагинами для вашей организации](https://code.claude.com/docs/ru/plugins/org.md)

Найдите раздел для того, что вы пишете или читаете:

* **Файл marketplace**: [Поля верхнего уровня](#top-level-fields) и [Записи плагинов](#plugin-entries)
* **`source` записи**: [Источники плагинов](#plugin-sources)
* **Объект `source` в параметрах**: [Источники marketplace](#marketplace-sources)
* **Вывод из [`claude plugin validate <path>`](https://code.claude.com/docs/ru/plugins/cli-reference)**: [Сообщения валидации](#validation-messages), которые сопоставляют каждое сообщение с полем, которое оно называет

## Файл маркетплейса

Сохраните файл маркетплейса по пути `.claude-plugin/marketplace.json` в каталоге вашего маркетплейса. Если вы храните файл в другом месте репозитория, пользователям придётся объявить маркетплейс в [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces) с указанием `path` в его источнике, поскольку у `claude plugin marketplace add` нет такой опции.

Каталог, содержащий `.claude-plugin/`, называется корнем маркетплейса, и все относительные источники плагинов разрешаются относительно него, а не относительно `.claude-plugin/`.

Каждый пользователь регистрирует один маркетплейс на одно значение `name`, поэтому у пользователя не может быть одновременно зарегистрировано два маркетплейса с одинаковым именем.

Claude Code игнорирует неизвестный ключ верхнего уровня или ключ записи плагина, а не отклоняет его, поэтому опечатка загружается без каких-либо сообщений. `claude plugin validate` сообщает о каждом неизвестном ключе как о предупреждении.

### Зарезервированные имена

Вы не можете дать своему маркетплейсу ни одно из следующих имён:

* **Имена официального marketplace**: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `life-sciences`, `knowledge-work-plugins`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins` и `claude-tag-plugins`. Зарезервированы, если только marketplace не поступает из источника `github` или `git` [marketplace source](#marketplace-sources) под `github.com/anthropics/`.
* **Имена community marketplace**: `claude-community`, `claude-plugins-community` и `healthcare`. Зарезервированы по тому же правилу, что и официальные имена.
* **Имена директории плагинов**: `anthropic-plugin-directory` и `claude-plugin-directory`. Зарезервированы по тому же правилу, что и официальные имена.
* **Имена, выдающие себя за официальный marketplace**: имена такие как `official-claude-plugins` или `claude-plugins-v2`, и любое имя, содержащее символ, отличный от ASCII. Ошибка: `Marketplace name impersonates an official Anthropic/Claude marketplace`. Управляющий символ или символ двунаправленного форматирования в имени также сообщает `Marketplace name cannot contain control or bidirectional-formatting characters`. Marketplace, уже зарегистрированный под таким именем, перестаёт загружаться, вместе с его плагинами.
* **Другое написание зарезервированного имени**: имя, которое отличается от зарезервированного имени только конечной точкой, или символом, отличным от подчёркивания, вместо дефиса, поэтому `claude.code.plugins` считается `claude-code-plugins`. Добавление marketplace завершается ошибкой [`is another spelling of "<reserved>", a reserved marketplace name`](https://code.claude.com/docs/ru/errors#marketplace-name-is-another-spelling-of-a-reserved-name), и marketplace, уже зарегистрированный под одним, перестаёт загружаться. Эта проверка требует Claude Code v2.1.280 или позже.
* **Имена, которые Claude Code использует для плагинов, которые не поступают из marketplace**: `inline` для плагинов, загруженных с [`--plugin-dir`](https://code.claude.com/docs/ru/cli-reference), `builtin` для встроенных плагинов, `skills-dir` для плагинов, автоматически загруженных из [`.claude/skills/`](https://code.claude.com/docs/ru/skills), и `synced` для плагинов, синхронизированных с вашего аккаунта claude.ai. `claude-plugin-test` также зарезервирован. `skills-dir` также появляется как `{"source": "skills-dir"}` в `strictKnownMarketplaces` и `blockedMarketplaces`, описанные в разделе [Source values valid only in policy lists](#source-values-valid-only-in-policy-lists).
* **Имена членов, которые есть у каждого объекта JavaScript**: `constructor`, `hasOwnProperty`, `isPrototypeOf`, `propertyIsEnumerable`, `toLocaleString`, `toString` и `valueOf`. `claude plugin marketplace add` отклоняет маркетплейс, использующий одно из них, с ошибкой [`Claude Code reserves this name and cannot register a marketplace under it`](https://code.claude.com/docs/ru/plugins/troubleshooting#claude-code-reserves-this-name). Эта проверка требует Claude Code v2.1.296 или позже.
* **Имена, начинающиеся с `claudeai-`**: зарезервированы для marketplace, размещённых на claude.ai. `claude plugin marketplace add` отказывает любому другому marketplace, который использует один с `Cannot add marketplace "<name>": names starting with "claudeai-" are reserved for marketplaces hosted on claude.ai`.
* **Папка загрузки зарегистрированного GitHub marketplace, `<owner>-<repo>`**: Claude Code загружает marketplace, добавленный из источника `github`, например `acme/x-tools`, через папку с именем `acme-x-tools`, каким бы ни было собственное `name` этого marketplace. Пока этот marketplace зарегистрирован под именем, отличным от `acme-x-tools`, `claude plugin marketplace add` отказывает другому marketplace с именем `acme-x-tools` после его загрузки и сообщает `Can't use the marketplace name "acme-x-tools"`. Эта проверка требует Claude Code v2.1.290 или позже.

Когда зарегистрированный маркетплейс перестаёт загружаться из-за того, что его имя имитирует официальное, `claude plugin list` и `/plugin` сообщают `Claude Code refuses the marketplace name "<name>"`. Сообщение предлагает удалить маркетплейс. Удаление маркетплейса также деинсталлирует его плагины и стирает их данные, параметры и секреты. Для этого именованного сообщения об отказе требуется Claude Code v2.1.282 или новее.

Если файл настроек объявляет маркетплейс встроенно, сообщение предлагает переименовать его запись, прежде чем удалять старое имя. Описание шагов см. в разделе [Claude Code отклоняет имя маркетплейса](https://code.claude.com/docs/ru/errors.md#claude-code-refuses-the-marketplace-name). Сообщение перечисляет эти шаги в Claude Code v2.1.292 или новее.

## Поля верхнего уровня

Таблица перечисляет каждый ключ, который Claude Code читает из `marketplace.json`. `name`, `owner` и `plugins` являются обязательными.

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | string | Идентификатор маркетплейса: буквы, цифры, `.`, `_` и `-`, начинается с буквы или цифры, без `..`. `claude plugin validate` отклоняет любое другое имя, потому что Claude Code [не может устанавливать плагины из маркетплейса с таким именем](https://code.claude.com/docs/ru/plugins/troubleshooting.md#cannot-install-plugins-from-a-marketplace-with-this-name). Пользователи вводят это имя после `@` в [идентификаторе плагина](https://code.claude.com/docs/ru/plugins/loading.md#find-where-a-plugin-came-from), например `my-plugin@my-marketplace`, при установке плагина. См. [Зарезервированные имена](#reserved-names) |
| `owner` | object | Информация о разработчике. `name` обязателен; `email` и `url` опциональны |
| `plugins` | array | [Записи плагинов](#plugin-entries). Каждая запись проверяется отдельно, поэтому одна неверная запись не приводит к отказу marketplace |
| `$schema` | string | URL JSON Schema для автодополнения редактора. Игнорируется при загрузке |
| `description` | string | Описание Marketplace, показываемое пользователям. `claude plugin validate` предупреждает, когда оно отсутствует |
| `version` | string | Версия манифеста Marketplace |
| `metadata.description`, `metadata.version` | string | Альтернативное местоположение для `description` и `version` |
| `metadata.pluginRoot` | string | Каталог, под которым разрешаются имена источников плагинов без префикса. См. [Источник плагина с относительным путём](#relative-path-plugin-source). Требует Claude Code v2.1.239 или позже |
| `forceRemoveDeletedPlugins` | boolean | Когда `true`, плагин, который вы удаляете из `plugins`, удаляется на машинах пользователей. См. [Размещение и поддержка marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md) |
| `allowCrossMarketplaceDependenciesOn` | array of strings | Имена marketplace, чьи плагины могут быть установлены как зависимости плагинов этого marketplace. При установке плагина применяется только список в собственном marketplace этого плагина для всей цепочки зависимостей. См. [Зависимости плагинов](https://code.claude.com/docs/ru/plugins/dependencies.md) |
| `renames` | object | Карта от бывшего `name` плагина к его текущему имени или к `null` для удалённого плагина. См. [Размещение и поддержка маркетплейса](https://code.claude.com/docs/ru/plugins/host-marketplace.md) |

## Записи плагинов

Каждый объект в массиве `plugins` верхнего уровня `marketplace.json` называет плагин и указывает, откуда его загружать. `name` и `source` являются обязательными.

Помимо [полей для списка в каталоге](https://code.claude.com/docs/ru/plugins/manifest-reference.md#directory-listing-fields), запись также принимает каждое [поле `plugin.json`](https://code.claude.com/docs/ru/plugins/manifest-reference), такое как `description`, `version`, `author`, `commands` и `hooks`. Для того, когда эти поля применяются, см. [Как запись объединяется с plugin.json](#entry-and-plugin-json).

Таблица перечисляет собственные поля записи и поля манифеста, чьё значение изменяется в записи.

| Поле | Тип | Описание |
| :- | :- | :- |
| `name` | string | Идентификатор плагина: буквы, цифры, `.`, `_` и `-`, начинающиеся с буквы или цифры. `claude plugin validate` не проходит другие имена, которые Claude Code не может установить. Пользователи вводят его перед `@` при установке, даже когда собственный `plugin.json` плагина устанавливает другой `name` |
| `source` | string or object | Откуда загружать плагин. См. [Источники плагинов](#plugin-sources) |
| `description` | string | Показывается в списках и деталях [`/plugin`](https://code.claude.com/docs/ru/plugins/install) |
| `version` | string | Строка версии для плагина. Когда `plugin.json` также устанавливает `version`, `plugin.json` имеет приоритет и `claude plugin validate` предупреждает. См. [Справочник загрузки плагинов](https://code.claude.com/docs/ru/plugins/loading.md) |
| `category` | string | Свободная категория для организации каталога |
| `tags` | array of strings | Свободные теги для поиска |
| `strict` | boolean | По умолчанию `true`. Является ли `plugin.json` определяющим источником компонентов плагина. См. [Строгий режим](#strict-mode) |
| `relevance` | object | Сигналы, которые говорят Claude Code, когда предложить плагин. См. [Рекомендация плагинов для вашей организации](https://code.claude.com/docs/ru/plugins/relevance.md) |
| `dependencies` | array | Плагины, которые должны быть включены, чтобы этот работал. Каждый элемент — это `"name"`, `"name@marketplace"` или объект. См. [Зависимости плагинов](https://code.claude.com/docs/ru/plugins/dependencies.md) |
| `engines` | object | Версии Claude Code, на которых работает плагин, в виде [диапазона semver](https://github.com/npm/node-semver#ranges) под ключом `claude-code`, например `"engines": { "claude-code": ">=2.1.400" }`. Требует Claude Code v2.1.323 или позже. Чтобы маркетплейс продолжал работать на версиях с v2.0.15 по v2.1.75, не указывайте `engines` ни в одной записи. Эти версии отклоняют весь `marketplace.json`, если хотя бы одна запись содержит это поле |
| `defaultEnabled` | boolean | По умолчанию `true`. Включен ли плагин по умолчанию, когда пользователь не установил его в [`enabledPlugins`](https://code.claude.com/docs/ru/settings-reference#enabledplugins). Значение записи имеет приоритет над `plugin.json` |
| `displayName` | string | Читаемое имя, показываемое в пользовательском интерфейсе. Когда ни запись, ни `plugin.json` плагина не устанавливают его, пользователи видят `name` плагина |
| `metadata` | object | Свободный объект для ваших собственных полей. Claude Code не читает его |
| `headers` | object | HTTP-заголовки, которые Claude Code отправляет при загрузке [архива](#archive-plugin-source) этой записи. Заголовок, установленный здесь, заменяет заголовок с тем же именем из [`headers`](#fields-by-type) источника маркетплейса. Требует Claude Code v2.1.238 или позже |
| `headersHelper` | string | Команда, которая выводит заголовки загрузки архива этой записи как один объект JSON для учётных данных, которые истекают. Запись также должна установить [`"strict": false`](#strict-mode). Требует Claude Code v2.1.238 или позже. См. [Аутентификация загрузок архивов](https://code.claude.com/docs/ru/plugins/host-marketplace.md#authenticate-archive-downloads) |

### Как запись объединяется с plugin.json

Поля записи применяются по-разному к загруженному плагину, который имеет свой собственный `.claude-plugin/plugin.json`, и к тому, который его не имеет:

* **Нет `plugin.json`**: запись является манифестом независимо от `strict`. Применяется каждое поле манифеста, которое принимает запись, включая [`mcpServers`, `lspServers`, `userConfig` и `channels`](https://code.claude.com/docs/ru/plugins/manifest-reference).
* **`plugin.json` присутствует**: `plugin.json` является манифестом. [Строгий режим](#strict-mode) решает, объединяются ли шесть полей компонентов записи, `commands`, `agents`, `skills`, `hooks`, `outputStyles` и `themes`, с ним или отклоняются как конфликт. Поля записи `mcpServers`, `lspServers`, `userConfig` и `channels` не применяются. Объявите их в `plugin.json`.

#### Хуки в записи

Напишите `hooks` записи как встроенный объект, который сопоставляет имена событий хуков с массивами matcher. Если вы напишете путь к файлу или массив вместо этого, `claude plugin validate` пройдёт. Эти хуки никогда не запускаются, и Claude Code сообщает об ошибке `not yet supported in a marketplace entry` для плагина. Поместите хуки на основе файлов в собственный [`hooks/hooks.json`](https://code.claude.com/docs/ru/plugins/components) плагина или `plugin.json`.

#### Поля отображения

Как запись, так и собственный `plugin.json` плагина могут устанавливать поля отображения `displayName`, `description`, `author`, `homepage`, `repository`, `license` и `keywords`. Пользователи видят эти значения в списках и деталях плагинов до и после установки:

* Для поля, которое вы устанавливаете в записи, пользователи видят значение записи, даже когда `plugin.json` устанавливает другое.
* Для поля, которое запись оставляет неустановленным, пользователи видят значение `plugin.json`.

До установки Claude Code может читать `plugin.json` только для записей с [источником с относительным путём](#relative-path-plugin-source), чьи файлы плагинов находятся внутри самого маркетплейса. Для записи с любым другим типом источника пользователи видят только собственные поля записи до установки плагина.

### Строгий режим

`strict` решает, что происходит, когда загруженный плагин имеет свой собственный `plugin.json` и запись также объявляет любое из [полей компонентов](#entry-and-plugin-json): `commands`, `agents`, `skills`, `hooks`, `outputStyles` или `themes`. При `strict: true`, по умолчанию, Claude Code добавляет поля компонентов записи к `plugin.json`, кроме `hooks`, чьи matcher заменяют matcher манифеста для каждого события. При `strict: false` запись, которая объявляет любое поле компонента, является конфликтом, и плагин не загружается. Таблица показывает каждую комбинацию `strict`, `plugin.json` и полей компонентов записи.

| `strict` | `plugin.json` | Поля компонентов записи | Результат |
| :- | :- | :- | :- |
| любой | отсутствует | любой | Запись является манифестом |
| `true`, по умолчанию | присутствует | любой | `plugin.json` является авторитетом. Claude Code добавляет поля компонентов записи к нему, кроме `hooks`, чьи matcher [заменяют matcher манифеста для каждого события](https://code.claude.com/docs/ru/plugins/manifest-reference.md#how-entry-fields-combine-with-plugin-json) |
| `false` | присутствует | нет | `plugin.json` является манифестом, как с `true` |
| `false` | присутствует | один или более | Конфликт. Плагин не загружается с `Plugin <name> has conflicting manifests: both plugin.json and marketplace entry specify components` |

## Источники плагинов

`source` записи плагина указывает, откуда Claude Code загружает этот плагин. Это либо строка относительного пути, либо объект, чей собственный ключ `source` называет тип, поэтому запись выглядит как `"source": { "source": "github", "repo": "your-org/formatter" }`.

Таблица перечисляет каждый тип источника плагина и его поля.

| Тип | Поля | Примечания |
| :- | :- | :- |
| Относительный путь | сама строка | Каталог внутри marketplace, разрешённый от корня marketplace. Должен начинаться с `./`, если только вы не напишете [имя без префикса под `metadata.pluginRoot`](#relative-path-plugin-source). `"."` само по себе означает сам корень |
| `github` | `repo`, `ref`, `sha` | Репозиторий GitHub в форме `owner/repo` |
| `url` | `url`, `ref`, `sha` | Любой git-репозиторий по URL |
| `git-subdir` | `url`, `path`, `ref`, `sha` | Один подкаталог git-репозитория, загруженный с помощью разреженного извлечения (sparse checkout) |
| `npm` | `package`, `version`, `registry` | Пакет из npm-реестра или ссылка на tarball, загруженные с вашим npm-клиентом и распакованные без запуска скриптов установки |
| `archive` | `url`, `sha256` | Zip-архив через HTTPS |
| `command` | `command`, `timeout`, `mode` | Каталог, выведенный командой, которую Claude Code запускает на машине пользователя |

Имена `url` и `github` также являются типами [источника marketplace](#marketplace-sources), где `url` означает прямую ссылку на файл `marketplace.json` вместо git-репозитория. `git` существует только как источник marketplace, и `npm` существует как оба. `git-subdir`, `archive` и `command` существуют только как источники плагинов.

Используйте относительный путь для плагина в подкаталоге самого репозитория marketplace. Используйте `git-subdir` для подкаталога какого-то другого репозитория.

Источники `github`, `url` и `git-subdir` совместно используют поля `ref` и `sha`:

* **`ref`**: ветка или тег. По умолчанию ветка репозитория по умолчанию.
* **`sha`**: полный 40-символьный SHA коммита в нижнем регистре. Когда вы устанавливаете оба `ref` и `sha`, Claude Code проверяет `sha`. На большинстве git-хостов, включая GitHub, GitLab и Bitbucket, это означает, что установка успешна, даже если ветка или тег, названные `ref`, были удалены выше по течению, пока коммит всё ещё достижим из репозитория. Некоторые серверы, такие как AWS CodeCommit, не поддерживают загрузку коммитов по SHA. На этих серверах `ref` всё ещё должен существовать и закреплённый коммит должен быть достижим из него.

Для того, как каждый тип загружается, кэшируется и версионируется, см. [Справочник загрузки плагинов](https://code.claude.com/docs/ru/plugins/loading.md).

### Источник плагина с относительным путём

Путь разрешается от корня marketplace. `./plugins/formatter` — это `<root>/plugins/formatter`, даже хотя файл marketplace находится в `<root>/.claude-plugin/`.

Путь, содержащий `..`, не проходит валидацию. На macOS и Linux Claude Code отказывает в записи пути, содержащей обратную косую черту где-либо после начального `./`, поэтому напишите путь с прямыми косыми чертами.

```json theme={null}
{ "name": "formatter", "source": "./plugins/formatter" }
```

Относительный путь разрешается только, когда Claude Code имеет файлы marketplace, поэтому проверьте тип [источника marketplace](#marketplace-sources):

* **`github`, `git`, `file` и `directory`**: Claude Code имеет файлы marketplace.
* **`url`**: Claude Code загружает только `marketplace.json`, поэтому относительные пути не могут разрешаться. Дайте каждому плагину источник объекта вместо этого, такой как `github` или `git-subdir`.
* **`settings`**: относительные пути отклоняются сразу.

#### Подмодули Git в репозитории маркетплейса

Когда Claude Code клонирует репозиторий маркетплейса, он загружает только те подмодули git, которые содержат файлы плагинов. Требует Claude Code v2.1.295 или позже.

Более ранние версии загружают все подмодули, включая вложенные. Если в репозитории есть большой подмодуль, Claude Code может при его загрузке превысить [таймаут клонирования](https://code.claude.com/docs/ru/plugins/troubleshooting.md#git-clone-timed-out-after-120s).

Для плагина в подкаталоге, таком как `./plugins/formatter`, Claude Code загружает подмодуль в следующих случаях:

* **Плагин находится внутри подмодуля**: подмодуль является каталогом плагина или каталогом выше него
* **Подмодуль находится внутри плагина**: подмодуль находится где-либо внутри каталога плагина
* **Символическая ссылка указывает внутрь подмодуля**: цель ссылки, закоммиченной в репозиторий, находится в подмодуле

Плагин в корне маркетплейса с `"source": "./"` получает либо все подмодули репозитория, либо ни одного. Claude Code загружает все подмодули, когда что-либо из следующего указывает на какой-либо подмодуль:

* **Каталог компонентов**: каталог в корне, содержащий компоненты плагина, такой как `skills/`, `hooks/` или `bin/`
* **Путь в конфигурации плагина**: путь в записи плагина в маркетплейсе, в его `plugin.json` или в файле конфигурации, таком как `.mcp.json` или `hooks/hooks.json`
* **Символическая ссылка**: ссылка, закоммиченная в репозиторий
* **Текст в файлах плагина**: путь подмодуля, такой как `vendor/tool`, записанный в файле конфигурации или в файле внутри каталога компонентов

Если ничто из этого не указывает на подмодуль, Claude Code не загружает для этого плагина ни одного подмодуля. Репозиторий, который одновременно является проектом и плагином, часто содержит подмодули, используемые только сборкой проекта, и это правило их исключает.

Claude Code также загружает все подмодули, когда не может определить, какие из них содержат файлы плагинов, например:

* **`SKILL.md` в корне**: в этом случае весь репозиторий является каталогом одного скилла
* **Файл, который Claude Code не может прочитать**: файл маркетплейса, один из файлов конфигурации плагина или `.gitmodules`

Если вы добавляете маркетплейс с `--sparse` или его источник задаёт `sparsePaths`, Claude Code извлекает только указанные там каталоги и не загружает ни одного подмодуля. Более ранние версии поступают так же.

Чтобы исключить из клона подмодуль, который не используется вашими плагинами, см. [Исключение неиспользуемых подмодулей из клона](https://code.claude.com/docs/ru/plugins/create-marketplace.md#keep-unused-submodules-out-of-the-clone).

#### Имена без префикса под pluginRoot

Имя без префикса — это одно имя каталога без `/`, такое как `"formatter"`. Чтобы писать имена без префикса вместо путей `./`, установите [`metadata.pluginRoot`](#top-level-fields) на каталог, под которым они разрешаются. С `"pluginRoot": "./plugins"`, `"source": "formatter"` разрешается в `./plugins/formatter`. Требует Claude Code v2.1.239 или позже.

`metadata.pluginRoot` имеет эти ограничения:

* Он сам должен быть относительным путём внутри marketplace.
* Он не влияет на источник, который уже начинается с `./`.
* Источник, содержащий `/`, такой как `team-a/formatter`, не является именем без префикса и всё ещё нуждается в префиксе `./`, даже когда установлен `metadata.pluginRoot`.

### Источник плагина github

`repo` принимает `owner/repo`. `ref` и `sha` опциональны.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "github",
    "repo": "your-org/formatter",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

### Источник плагина url

`url` — это полный git URL: `https://`, `http://`, `file://` или `git@`. Суффикс `.git` не требуется, поэтому URL Azure DevOps и AWS CodeCommit работают как написано. Этот тип не принимает сокращение `owner/repo`.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "url",
    "url": "https://gitlab.example.com/your-group/formatter.git",
    "ref": "main"
  }
}
```

### Источник плагина git-subdir

`url` принимает полный git URL или сокращение GitHub `owner/repo`. `path` — это подкаталог, который содержит плагин, и Claude Code извлекает только этот подкаталог. При использовании URL `https` или SSH Claude Code запрашивает у сервера частичный клон, поэтому с хоста, поддерживающего частичные клоны, плагин из большого монорепозитория устанавливается без загрузки остальной части репозитория.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/your-org/monorepo.git",
    "path": "tools/formatter"
  }
}
```

### Источник плагина npm

Источник `npm` принимает эти поля:

* `package`: имя пакета в реестре, такое как `@your-org/formatter`, имя с добавленной версией, такое как `@your-org/formatter@2.0.0`, или ссылка `https` на tarball-файл пакета
* `version`: версия, диапазон semver или dist-tag, используемые, когда `package` — это имя пакета без добавленной версии. Опустите его, чтобы загрузить `latest`
* `registry`: URL реестра для пакета, который не находится в реестре по умолчанию

Claude Code загружает пакет с вашим npm-клиентом. Скрипты установки пакета, такие как `preinstall` или `postinstall`, никогда не запускаются, и его зависимости не устанавливаются во время загрузки. Если пакет имеет поддерживаемый файл блокировки рядом с его `package.json`, Claude Code устанавливает эти [зависимости пакетов Node.js](https://code.claude.com/docs/ru/plugins/loading.md#node-js-package-dependencies) в отдельном шаге, также с отключёнными скриптами.

Claude Code проверяет значение `package` перед любой загрузкой. Отклонённое значение приводит к сбою установки с сообщением, в котором указаны значение и причина. К отклоняемым значениям относятся:

* **Git-адрес, путь к папке или `file:`, или псевдоним `npm:`**: используйте [источник `github`, `url` или `git-subdir`](#plugin-sources) для git-репозитория, относительный путь для папки в маркетплейсе и собственное имя пакета для псевдонима
* **Ссылка на tarball на github.com, gist.github.com, gitlab.com, bitbucket.org или git.sr.ht**: отклоняется, даже если ссылка — это загрузка релиза GitHub, если только это не ссылка на npm-реестр GitLab под `gitlab.com/api/v4/`
* **Ссылка на tarball через `http`**: отклоняется, если только она не указывает на собственный npm-реестр по умолчанию устанавливающего пользователя

URL `registry` должен использовать `https`, если только это не собственный npm-реестр по умолчанию устанавливающего пользователя. С любым другим реестром `http` установка завершается сбоем до того, как npm обратится к нему.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "npm",
    "package": "@your-org/formatter",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

### Источник плагина archive

`url` должен использовать `https://` и не может указывать на хост обратной связи, локальной связи или облачных метаданных. Для размера, тайм-аута, перенаправления и ограничений на извлечение при загрузке см. [Оставайтесь в пределах ограничений загрузки для размещённых файлов](https://code.claude.com/docs/ru/plugins/host-marketplace.md#stay-within-the-download-limits-for-hosted-files).

Корень плагина может быть в верхней части zip или на один каталог ниже.

`sha256` — это дайджест архива как 64 шестнадцатеричных символа, прописные или строчные. Когда вы его устанавливаете, Claude Code отказывает в загрузке, которая не совпадает.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "archive",
    "url": "https://artifacts.example.com/formatter-2.0.0.zip",
    "sha256": "6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1"
  }
}
```

### Источник плагина command

Используйте источник `command`, когда инструмент, установленный на машине пользователя, производит каталог плагина, такой как IDE, которая отображает свой плагин для цепочки инструментов, которую выбрал пользователь. Claude Code запускает команду, когда пользователь устанавливает или обновляет плагин, и [снова один раз за сеанс](https://code.claude.com/docs/ru/plugins/loading.md#when-a-command-source-re-runs), поэтому пользователи получают изменённый вывод инструмента без переустановки.

Источник `command` принимает эти поля:

* `command`: команда оболочки, которая выводит абсолютный путь каталога плагина как одну строку и выходит 0. Claude Code показывает пользователям всю строку для проверки перед её запуском. Напишите её как печатаемый ASCII, максимум 500 символов, без прогона из четырёх или более пробелов.
* `timeout`: целое число секунд от 1 до 600. По умолчанию 60.
* `mode`: `copy`, по умолчанию, или `link`. См. [Режим копирования и режим ссылки](#copy-mode-and-link-mode).

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "command",
    "command": "my-tool claude-plugin-path",
    "timeout": 120
  }
}
```

Для того, как пользователи принимают команду, см. [Установка из вашей оболочки](https://code.claude.com/docs/ru/plugins/install.md#install-from-your-shell). Для того, что пользователи видят после того, как вы её измените, см. [Изменение команды источника command](https://code.claude.com/docs/ru/plugins/host-marketplace.md#change-the-command-of-a-command-source). Администраторы отключают источники command с [`disableCommandPluginSources`](https://code.claude.com/docs/ru/settings-reference#disablecommandpluginsources).

#### Что должна делать команда

Напишите команду, чтобы соответствовать этим требованиям:

* **Оболочка и рабочий каталог**: Claude Code запускает команду через `sh` или через `cmd.exe` на Windows из домашнего каталога пользователя. Дайте абсолютный путь или команду на `PATH`.
* **Вывод**: выведите ровно одну строку на stdout, абсолютный путь каталога плагина, и выйдите 0 в течение `timeout` секунд.
* **Содержимое каталога**: каталог содержит полный плагин к моменту выхода команды. Путь может отличаться от одного запуска к другому.

#### Вывод, который приводит к отказу установки или обновления

Установка или обновление не удаётся, когда команда выходит с ненулевым кодом, работает дольше `timeout` или выводит что-либо, кроме одного абсолютного пути. Это также не удаётся, когда выведённый каталог является одним из этих:

* **Нет содержимого плагина**: выведённый каталог не имеет содержимого плагина на его верхнем уровне, такого как каталог `.claude-plugin/` или каталог `skills/`, `commands/`, `agents/` или `hooks/`.
* **Собственный каталог сеанса**: выведённый каталог — это тот, в котором был запущен Claude Code, или один из его родителей.
* **Сетевой путь**: на Windows выведённый путь — это путь UNC.
* **Слишком большой для копирования**: в режиме копирования каталог больше 256 МиБ или имеет более 20 000 записей.

#### Режим копирования и режим ссылки

`mode` решает, копирует ли Claude Code выведённый каталог или использует его на месте:

* **`copy`**: Claude Code копирует каталог в кэш плагина и выводит [версию плагина](https://code.claude.com/docs/ru/plugins/loading.md#how-claude-code-computes-the-version) из хэша скопированных файлов. Ваш инструмент может удалить или переписать каталог после выхода команды. Повторный запуск, который производит идентичные файлы, считается актуальным.
* **`link`**: Claude Code заполняет запись кэша плагина ссылкой на каждую запись верхнего уровня выведённого каталога и загружает файлы на месте. Ничего не копируется, содержимое файлов не хэшируется, и ограничения размера не применяются. Используйте его для каталога, слишком большого для копирования, такого как экспорт отображённого SDK.

Плагин в режиме ссылки имеет эти требования:

* **Держите каталог на месте**: Claude Code загружает плагин через ссылки при каждом запуске, поэтому выведённый каталог должен оставаться там, где он находится, пока плагин остаётся установленным.
* **Выведите другой путь, чтобы сигнализировать о новом содержимом**: версия поступает из реального пути выведённого каталога и его записей верхнего уровня, а не из файлов внутри них.
* **Держите символические ссылки верхнего уровня внутри каталога**: установка не удаётся, если запись верхнего уровня — это символическая ссылка, которая указывает вне выведённого каталога.
* **Включите `node_modules`**: Claude Code пропускает [установку зависимостей пакетов Node.js](https://code.claude.com/docs/ru/plugins/loading.md#node-js-package-dependencies) для плагина в режиме ссылки, поэтому выведите каталог, который уже содержит пакеты, которые нужны плагину.
* **Сеансы, запущенные внутри каталога**: сеанс, запущенный в выведённом каталоге или где-либо ниже, не загружает плагин.
* **Не на Windows**: Claude Code отказывает в установке плагина в режиме ссылки на Windows. Объявите `"mode": "copy"` там.

## Источники Marketplace

Источник marketplace указывает, откуда Claude Code загружает `marketplace.json`. CLI создаёт один для вас при добавлении marketplace, и вы пишете один сами в параметрах:

* **[`claude plugin marketplace add`](https://code.claude.com/docs/ru/plugins/cli-reference)**: Claude Code создаёт источник из строки, которую вы передаёте.
* **[`extraKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#extraknownmarketplaces)**: вы пишете источник сами как объект `source`.
* **[`strictKnownMarketplaces`](https://code.claude.com/docs/ru/settings-reference#strictknownmarketplaces) и [`blockedMarketplaces`](https://code.claude.com/docs/ru/plugins/org#restrict-what-users-can-install)**: администраторы пишут источники в этих двух списках политик. `strictKnownMarketplaces` — это список разрешений, а `blockedMarketplaces` — это список запретов.

Имена типов `url`, `git` и `github` означают что-то другое в источнике marketplace, чем в [источнике плагина](#plugin-sources):

| Имя типа | Как источник marketplace | Как источник плагина |
| :- | :- | :- |
| `url` | Прямая ссылка на файл `marketplace.json` с полями `url`, `headers` и `headersHelper` | Git-репозиторий для клонирования с полями `url`, `ref` и `sha` |
| `git` | Git-репозиторий для клонирования с полями `url`, `ref`, `path` и `sparsePaths` | Не существует |
| `github` | Репозиторий GitHub с полями `repo`, `ref`, `path` и `sparsePaths` | Репозиторий GitHub с полями `repo`, `ref` и `sha`, и без `path` |

Таблица перечисляет каждый тип источника marketplace с его полями, вводом `claude plugin marketplace add`, который его производит, и что он делает в каждом из трёх ключей параметров.

| Тип | Поля | Ввод `marketplace add` | `extraKnownMarketplaces` | `strictKnownMarketplaces` | `blockedMarketplaces` |
| :- | :- | :- | :- | :- | :- |
| `url` | `url`, `headers`, `headersHelper` | URL `http://` или `https://`, который не совпадает с формой git | Загружается | Разрешает тот же URL | Блокирует тот же URL |
| `github` | `repo`, `ref`, `path`, `sparsePaths` | `owner/repo`, `owner/repo@ref` или `owner/repo#ref` | Загружается | Разрешает тот же `repo`, `ref` и `path`. `repo` может быть `owner/*` | Блокирует то же самое и URL `git` к тому же репозиторию |
| `git` | `url`, `ref`, `path`, `sparsePaths` | URL `user@host:path` или URL `http://` или `https://`, который заканчивается на `.git`, содержит `/_git/` или называет репозиторий github.com или gitlab.com. `#ref` закрепляет ref | Загружается | Разрешает тот же URL, `ref` и `path` | Блокирует то же самое и другие написания того же репозитория github.com |
| `npm` | `package` | Не производится | Не загружается: `NPM marketplace sources not yet implemented` | Анализирует, но ничего не совпадает, потому что ничего не регистрирует marketplace `npm` | Анализирует, но ничего не совпадает |
| `file` | `path` | Путь к файлу `.json` | Загружается | Разрешает тот же путь | Блокирует тот же путь |
| `directory` | `path` | Путь к каталогу | Загружается | Разрешает тот же путь | Блокирует тот же путь |
| `settings` | `name`, `plugins`, `owner` | Не производится | Загружается | Разрешает запись с тем же `name` и идентичными `plugins` | Блокирует то же самое `name` |
| `skills-dir` | нет | Не производится | Не загружается: `Unsupported marketplace source type` | Разрешает [плагины каталога skills](https://code.claude.com/docs/ru/plugins/org.md#keep-skills-directory-plugins-loading). См. [Значения источников, действительные только в списках политик](#source-values-valid-only-in-policy-lists) | Останавливает загрузку плагинов каталога skills |
| `hostPattern` | `hostPattern` | Не производится | Не загружается: `Unsupported marketplace source type` | Разрешает источники `github`, `git` и `url`, чей хост совпадает | Блокирует эти источники |
| `pathPattern` | `pathPattern` | Не производится | Не загружается: `Unsupported marketplace source type` | Разрешает источники `file` и `directory`, чей `path` совпадает | Блокирует эти источники |

### Поля по типам

Таблица перечисляет каждое поле источника marketplace, которое имеет значение по умолчанию, ограничение или значение, специфичное для его типа.

| Поле | Типы | Описание |
| :- | :- | :- |
| `url` | `url` | Ссылка на файл `marketplace.json`. Claude Code загружает только этот файл, поэтому плагины marketplace не могут использовать [источники с относительными путями](#relative-path-plugin-source). См. [Оставайтесь в пределах лимитов загрузки для размещённых файлов](https://code.claude.com/docs/ru/plugins/host-marketplace.md#stay-within-the-download-limits-for-hosted-files) для ограничений размера, тайм-аута и перенаправления |
| `url` | `git` | Git-репозиторий для клонирования |
| `headers` | `url` | Карта HTTP-заголовков, которые Claude Code отправляет с загрузкой, для аутентифицированных хостов |
| `headersHelper` | `url` | Команда, которая выводит заголовки, чьи значения слишком недолговечны, чтобы их перечислять в `headers`. Требует Claude Code v2.1.238 или позже. См. [Аутентификация загрузок архивов](https://code.claude.com/docs/ru/plugins/host-marketplace.md#authenticate-archive-downloads) |
| `repo` | `github` | В `marketplace add` и `extraKnownMarketplaces`, `repo` должен называть один репозиторий. `marketplace add` отклоняет `owner/*` как неверное сокращение `owner/repo`; в `extraKnownMarketplaces` Claude Code берёт его буквально и клон не удаётся |
| `ref` | `github`, `git` | Ветка, тег или полный SHA в нижнем регистре коммита в ветке или теге. По умолчанию ветка репозитория по умолчанию. SHA требует Claude Code v2.1.324 или позже и отклоняется для marketplace с [зарезервированным именем](#reserved-names), например `claude-plugins-official` |
| `path` | `github`, `git` | Путь файла marketplace внутри репозитория. По умолчанию `.claude-plugin/marketplace.json` |
| `path` | `file` | Сам файл marketplace. Claude Code читает его на месте и берёт каталог на два уровня выше как корень marketplace, поэтому держите файл в `<root>/.claude-plugin/marketplace.json` |
| `path` | `directory` | Корень marketplace, каталог, который содержит `.claude-plugin/marketplace.json` |
| `sparsePaths` | `github`, `git` | Массив каталогов для разреженного извлечения, такой как `[".claude-plugin", "plugins"]`. `claude plugin marketplace add --sparse` устанавливает его |
| `skipLfs` | `github`, `git` | Принимается и не имеет эффекта. См. [Держите файлы плагинов вне Git LFS](https://code.claude.com/docs/ru/plugins/host-marketplace.md#keep-plugin-files-out-of-git-lfs) |
| `name` | `settings` | Должен равняться ключу `extraKnownMarketplaces` и не может быть [зарезервированным именем](#reserved-names) |
| `plugins` | `settings` | Встроенный каталог без размещённого файла. Каждый элемент принимает `name`, `source`, `description`, `version`, `strict`, `headers` и `headersHelper`. Напишите `source` каждого элемента как тип объекта, потому что относительный путь не имеет репозитория для разрешения |

Чтобы обновления и автообновления не уводили marketplace `github` или `git` с проверенного вами коммита, задайте в `ref` полный SHA этого коммита, как в этом источнике:

```json theme={null}
{ "source": "github", "repo": "acme-corp/plugins", "ref": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0" }
```

Сначала обновите Claude Code на каждой машине, потому что версии до v2.1.324 не могут загрузить marketplace, закреплённый таким образом. Запись плагина с собственным удалённым источником всё ещё может обновляться, поэтому закрепите и эту запись, например с помощью [`sha`](#plugin-sources) в источнике `github`, `url` или `git-subdir`.

### Значения источников, действительные только в списках политик

`hostPattern`, `pathPattern`, `skills-dir` и форма `owner/*` из `repo` действительны только в двух списках политик, `strictKnownMarketplaces` и `blockedMarketplaces`:

* **`hostPattern` и `pathPattern`**: регулярные выражения, которые Claude Code тестирует против источника перед загрузкой из него.
* **`skills-dir`**: не источник. Если вы задаёте `strictKnownMarketplaces` без записи `{"source": "skills-dir"}`, [плагины каталога skills](https://code.claude.com/docs/ru/plugins/org.md#keep-skills-directory-plugins-loading) перестают загружаться. Если вы блокируете любой тип кастомизации с помощью [`strictPluginOnlyCustomization`](https://code.claude.com/docs/ru/settings-reference#strictpluginonlycustomization), они перестают загружаться независимо от того, присутствует ли эта запись.
* **`owner/*`**: как значение `repo` из `github`, совпадает с каждым репозиторием ровно под этим владельцем GitHub. Требует Claude Code v2.1.223 или позже.

Для порядка совпадения, точной семантики `ref` и рецептов см. [Управление плагинами для вашей организации](https://code.claude.com/docs/ru/plugins/org.md).

### Объекты источников в параметрах

Значение `extraKnownMarketplaces` — это карта от имени marketplace к объекту с `source`. Эта запись регистрирует marketplace из git-репозитория в его ветке `main`:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/your-org/your-marketplace.git",
        "ref": "main"
      }
    }
  }
}
```

`strictKnownMarketplaces` и `blockedMarketplaces` — это массивы объектов источников. Этот список разрешений допускает одного владельца GitHub и один внутренний хост:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "your-org/*" },
    { "source": "hostPattern", "hostPattern": "^git\\.example\\.com$" }
  ]
}
```

## Сообщения валидации

`claude plugin validate <path>` принимает корень маркетплейса или сам файл маркетплейса. Чтобы этот файл был [проверен как маркетплейс](https://code.claude.com/docs/ru/plugins/cli-reference.md#validate-a-manifest-file), а не как манифест плагина, назовите его `marketplace.json`. Для кодов выхода и `--strict` см. [plugin validate](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-validate).

Сообщение называет запись плагина по её индексу, написанному как `plugins.1.source` или `plugins[1].source`.

Сообщение с префиксом индекса записи и `plugin.json →`, такое как `plugins[2] plugin.json →`, касается собственных файлов этого плагина. [`claude plugin validate` сообщает об ошибках](https://code.claude.com/docs/ru/plugins/troubleshooting#claude-plugin-validate-reports-errors) перечисляет эти сообщения с их исправлениями.

Предупреждения, которые упоминают имена флагов Claude Desktop, которые Claude Desktop отклоняет.

Таблица сопоставляет сообщения уровня marketplace с полем, которое каждое касается.

| Сообщение | Уровень | Поле |
| :- | :- | :- |
| `Marketplace must have a name` | Ошибка | `name` пуст |
| `Marketplace name cannot contain spaces. Use kebab-case (e.g., "my-marketplace")` | Ошибка | `name` |
| `Marketplace name cannot contain path separators (/ or \), ".." sequences, or be "."` | Ошибка | `name` |
| `Marketplace name impersonates an official Anthropic/Claude marketplace` | Ошибка | `name`. См. [Зарезервированные имена](#reserved-names) |
| `Marketplace name cannot contain control or bidirectional-formatting characters` | Ошибка | `name` содержит управляющий символ, такой как escape или новая строка, или символ двунаправленного форматирования Unicode |
| `Marketplace name "inline" is reserved for --plugin-dir session plugins`, и варианты `builtin`, `skills-dir`, `synced` и `claude-plugin-test` | Ошибка | `name` |
| `Author name cannot be empty` | Ошибка | `owner.name` |
| `Plugin name cannot contain spaces. Use kebab-case (e.g., "my-plugin")` | Ошибка | `plugins[i].name` |
| `Plugin name cannot contain control or bidirectional-formatting characters` | Ошибка | `plugins[i].name` |
| `Plugin name "x" is reserved: it passes as one of Anthropic's own` | Ошибка | `plugins[i].name`. См. манифест [`name`](https://code.claude.com/docs/ru/plugins/manifest-reference#name) для зарезервированных имён |
| `Plugin name "x" reads as one of Anthropic's own` | Предупреждение | `plugins[i].name` |
| `Claude Code cannot install plugins from marketplace "x". Each part of a plugin id (plugin@marketplace) may use only the letters a-z and A-Z, digits, ".", "_" and "-", and must start with a letter or digit. Change the marketplace's "name".` | Ошибка | `name` |
| `Claude Code cannot install plugin "x". Each part of a plugin id (plugin@marketplace) may use only the letters a-z and A-Z, digits, ".", "_" and "-", and must start with a letter or digit. Change this entry's "name".` | Ошибка | `plugins[i].name` |
| `Duplicate plugin name "x" found in marketplace` | Ошибка | Две записи совместно используют `name` |
| `Must be a version range such as ">=2.1.0"; got "<value>". It will be ignored at load time.` | Ошибка | `plugins[i].engines.claude-code` |
| `plugins.i.source: Invalid input` | Ошибка | `source` записи не совпадает с типом. См. [Неверный ввод на источнике](#invalid-input-on-a-source) |
| `plugins.i.source: Invalid string: must start with "./"` | Ошибка | `source` с относительным путём без ведущего `./`. До v2.1.285 эта ошибка выводила вместо этого `Invalid input` |
| `plugins[i].source: Path contains "..": <path>` | Ошибка | Относительный `source`, который выходит за пределы корня marketplace |
| `source.source: 'unsupported' is a parse-time placeholder and cannot be authored` | Ошибка | `plugins[i].source` |
| `Plugin "x" sets headersHelper but is not "strict": false` | Ошибка | `plugins[i].headersHelper`, на записи `archive` |
| `chain does not resolve (<reason>) — target must be a name in plugins[], a key in renames, or null` | Ошибка | `renames.<old>` |
| `target "x" is not a valid plugin name (PluginIdSchema)` | Ошибка | `renames.<old>` |
| `Unknown field 'x'. Claude Code ignores it at load time.` | Предупреждение | Названный ключ на верхнем уровне, под `metadata`, в записи или под `relevance` записи |
| `'engines' must be an object such as { "claude-code": ">=2.1.0" }; got <type>. It will be ignored at load time.` | Предупреждение | `plugins[i].engines` |
| `Marketplace has no plugins defined` | Предупреждение | `plugins` пуст |
| `Plugin "x" sets headers/headersHelper, which only apply to "archive" sources; they have no effect on this entry.` | Предупреждение | `plugins[i].headers` или `plugins[i].headersHelper`, на записи, чей `source` не является `archive` |
| `Plugin "x" fetches its archive with a headersHelper but sets no sha256 pin` | Предупреждение | `plugins[i].source.sha256` |
| `Header "x" is a request-routing/identity header that catalog entries may not set; Claude Code drops it at download time.` | Предупреждение | `plugins[i].headers.<name>` |
| `Local source "x" is or traverses a symlink, so <path> was not read` | Предупреждение | `plugins[i].source` |
| `No marketplace description provided. Adding a description helps users understand what this marketplace offers` | Предупреждение | `description` |
| `Entry declares version "x" but <path>/plugin.json says "y". At install time, plugin.json wins` | Предупреждение | `plugins[i].version`, на записи с относительным путём |
| `'relevance' must be an object containing topic and signals; got <type>. It will be ignored at load time.` | Предупреждение | `plugins[i].relevance` |
| `'metadata' must be a free-form object; got <type>. It will be ignored at load time.` | Предупреждение | `plugins[i].metadata` |
| `'experimental' must be an object containing component declarations; got <type>. It will be ignored at load time.` | Предупреждение | `plugins[i].experimental` |
| `Marketplace name "x" is reserved in Claude Desktop` | Предупреждение | `name` — это `org`, `org-provisioned` или `unknown`. Claude Desktop отклоняет marketplace |
| `Marketplace name "x" is not accepted by Claude Desktop (letters, digits, ".", "_", "-"; must start alphanumeric; max 128 chars)` | Предупреждение | `name`. Claude Desktop отклоняет marketplace |
| `Plugin name "x" is not accepted by Claude Desktop (letters, digits, ".", "_", "-"; must start alphanumeric; max 128 chars)` | Предупреждение | `plugins[i].name`. Claude Desktop отбрасывает запись |

### Неверный ввод на источнике

`Invalid input` на `source` означает, что объект не совпадал с типом источника. Проверьте эти причины:

* `npm` `package`, содержащий `..`
* Тип `source`, который не является одним из [источников плагинов](#plugin-sources)
* Известный тип с отсутствующим обязательным полем или неправильного типа, такой как `github` без `repo`

Относительный путь, который не начинается с `./`, кроме `"."` или [имени без префикса под `metadata.pluginRoot`](#relative-path-plugin-source), завершается ошибкой `Invalid string: must start with "./"`. До v2.1.285 он выводил `Invalid input`, как и причины выше.

### Сбои, которые валидация не ловит

`claude plugin validate` не сообщает о каждом сбое. Запись `hooks`, написанная как путь к файлу или массив, проходит валидацию, и ошибка появляется только при загрузке плагина, как описывает [Hooks в записи](#hooks-in-an-entry). Ошибки загрузки `source` также появляются только после установки, а не при валидации.

[`claude plugin list`](https://code.claude.com/docs/ru/plugins/cli-reference) показывает плагин, который не загрузился, с его ошибкой, и [Устранение неполадок плагинов](https://code.claude.com/docs/ru/plugins/troubleshooting.md) охватывает строки загрузки.

## Следующие шаги

* [Создание marketplace](https://code.claude.com/docs/ru/plugins/create-marketplace.md): создайте marketplace из этих полей и установите его локально
* [Размещение и поддержка marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md): где поместить файл и как пользователи получают изменения
* [Справочник манифеста плагина](https://code.claude.com/docs/ru/plugins/manifest-reference.md): поля `plugin.json`, которые запись может переопределить
* [Управление плагинами для вашей организации](https://code.claude.com/docs/ru/plugins/org.md): рецепты списков разрешений и запретов, которые используют эти значения источников
