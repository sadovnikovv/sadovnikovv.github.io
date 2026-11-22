> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник манифеста плагина

> Полный справочник по plugin.json: поля с типами и значениями по умолчанию, принятые формы путей и схемы userConfig и переменных окружения.

Манифест плагина — это файл `plugin.json` в директории `.claude-plugin/` плагина. Он содержит метаданные плагина и значения [`userConfig`](#user-configuration), которые Claude Code запрашивает у пользователя. Он также объявляет любой компонент, который вы определяете встроенным образом или храните вне его [расположения по умолчанию](#standard-layout).

Этот справочник предназначен для создателей плагинов и для владельцев маркетплейсов, которые размещают поля компонентов в записи маркетплейса.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Обучение созданию плагина**: начните с [Создание плагина](https://code.claude.com/docs/ru/plugins/create.md)
> * **Что каждый компонент делает во время выполнения**: см. [Компоненты плагина](https://code.claude.com/docs/ru/plugins/components.md)

Начните с раздела, который соответствует тому, что вы ищете:

* Поле: таблица [Поля](#fields) дает тип каждого поля, является ли оно обязательным, его значение по умолчанию и что оно принимает. [Правила путей](#path-rules) охватывает префикс `./` и содержание для каждого пути компонента
* Опция `userConfig` или запись `channels`: схемы [Конфигурация пользователя](#user-configuration) и [Каналы](#channels)
* `${CLAUDE_PLUGIN_ROOT}` или другая переменная, на которую может ссылаться плагин: [Переменные окружения](#environment-variables)
* Где находятся файлы каждого компонента: [Стандартное расположение](#standard-layout)
* Сообщение от `claude plugin validate`: на [странице устранения неполадок](https://code.claude.com/docs/ru/plugins/troubleshooting.md) перечислены все сообщения с их исправлениями и ссылками на соответствующие разделы этой страницы

## Файл манифеста

Манифест является необязательным. Без него Claude Code загружает компоненты, которые находит в [стандартном расположении](#standard-layout). Имя плагина затем берется из записи маркетплейса или из имени директории при загрузке плагина с помощью `--plugin-dir`.

Напишите манифест, когда вам нужны метаданные, компонент вне его директории по умолчанию, `userConfig` или встроенное определение компонента.

Сохраните манифест в `.claude-plugin/plugin.json` в корне плагина. Поместите все остальные файлы плагина в корень плагина, а не внутри `.claude-plugin/`. Это включает `skills/`, `commands/` и `hooks/`.

Следующий пример устанавливает большинство ключей в таблице [Поля](#fields). Он проходит проверку в директории плагина, которая содержит каждый указанный путь.

```json theme={null}
{
  "name": "deploy-tools",
  "displayName": "Deploy Tools",
  "version": "1.2.0",
  "description": "Deployment commands, a review agent, and a status monitor",
  "author": {
    "name": "Example Team",
    "email": "dev@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://example.com/docs/deploy-tools",
  "repository": "https://github.com/example/deploy-tools",
  "license": "MIT",
  "keywords": ["deployment", "ci"],
  "defaultEnabled": true,
  "dependencies": ["secrets-vault"],
  "metadata": { "catalogId": "cat-123" },
  "skills": ["./extra-skills/"],
  "commands": {
    "status": {
      "source": "./commands/status.md",
      "description": "Show the current deployment status"
    },
    "about": {
      "content": "Explain what the deploy-tools plugin provides.",
      "description": "Describe this plugin"
    }
  },
  "agents": ["./agents/reviewer.md"],
  "hooks": "./config/extra-hooks.json",
  "mcpServers": {
    "deploy-api": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  },
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./config/monitors.json"
  },
  "userConfig": {
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token for the deployment API",
      "sensitive": true
    }
  }
}
```

### Нераспознанные поля

Нераспознанный ключ верхнего уровня удаляется, а нераспознанный ключ внутри опции `userConfig`, записи `channels`, конфигурации `lspServers` или записи `monitors` отклоняется:

* **Поля верхнего уровня**: поле удаляется и плагин загружается. `claude plugin validate` сообщает о каждом нераспознанном поле верхнего уровня как о предупреждении
* **Строгие объекты**: опции `userConfig`, записи `channels`, конфигурации `lspServers` и записи `monitors` являются строгими. Неизвестный ключ внутри одного из них — это ошибка, и плагин не загружается

### Проверка манифеста

`claude plugin validate` — это авторитетная проверка манифеста. Запустите его из вашей оболочки для директории плагина:

```bash theme={null}
claude plugin validate ./my-plugin
```

Команда сообщает один из этих результатов:

* **`Validation passed`**: манифест загружается
* **`Validation passed with warnings`**: манифест загружается, но валидатор нашел что-то для исправления, например неизвестное поле верхнего уровня, которое Claude Code удаляет, `name`, который не в kebab-case, или отсутствующие `version`, `description` или `author`. Передайте `--strict`, чтобы превратить предупреждения в ошибки в CI
* **`Validation failed`**: манифест имеет несоответствие типов, путь, который отсутствует или выходит за пределы корня плагина, или неизвестный ключ внутри опции `userConfig`, записи `channels`, конфигурации `lspServers` или записи `monitors`. Claude Code сообщает о той же проблеме при загрузке плагина

Команда также проверяет каждую запись MCP-сервера, которую плагин объявляет в `.mcp.json`, в файле `.json`, который называет [`mcpServers`](#mcpservers), или встроенную в `plugin.json`. Эти проверки MCP требуют Claude Code v2.1.281 или более поздней версии и включают:

* **Ошибки**: запись, которую Claude Code удалит при загрузке плагина, ссылка `${user_config.KEY}` на опцию, которую манифест не объявляет, и удаленный `url`, который не является действительным абсолютным URL
* **Предупреждения**: URL `http://` или `ws://` на хост, не являющийся loopback, и значение заголовка, которое выглядит как буквальные учетные данные

## Поля

В таблице перечислены ключи верхнего уровня в `plugin.json`. `name` — единственный обязательный ключ. Если имя поля является ссылкой, в связанном разделе приведены полные правила для него.

Для ключей компонентов, таких как `commands` и `hooks`, [Формы путей компонентов](#component-path-forms) показывает каждую принятую форму с примером, и каждый путь следует [правилам путей](#path-rules) для префикса `./`, расширений и содержания.

| Поле | Тип | Описание |
| :- | :- | :- |
| `$schema` | String | URL JSON Schema для автодополнения редактора. Claude Code игнорирует его при загрузке |
| [`name`](#name) | String | Идентификатор плагина, обязательный. Используйте kebab-case. Каждый компонент находится в пространстве имен под ним |
| [`displayName`](#displayname) | String | Имя, показываемое в UI вместо `name` |
| [`version`](#version) | String | Строка версии. Установка ее удерживает пользователей на этой версии, пока вы не измените ее |
| `description` | String | Краткое объяснение того, что предоставляет плагин |
| `author` | Object | `name`, который является обязательным, плюс необязательные `email` и `url` |
| `homepage` | String | URL документации. Должен анализироваться как URL, иначе плагин не загружается |
| `repository` | String | URL исходного репозитория. Не проверяется |
| `license` | String | Идентификатор SPDX, такой как `MIT` или `Apache-2.0` |
| `keywords` | Array of strings | Теги обнаружения |
| [`metadata`](#metadata) | Object | Объект произвольной формы для ваших собственных данных. Claude Code не читает его |
| [`icon`](#directory-listing-fields) | String | Значок для страницы плагина в каталоге Anthropic. Claude Code не читает его |
| [`documentationUrl`](#directory-listing-fields) | String | Ссылка на документацию для страницы плагина в каталоге Anthropic. Claude Code не читает его |
| [`supportUrl`](#directory-listing-fields) | String | Ссылка на поддержку для страницы плагина в каталоге Anthropic. Claude Code не читает его |
| [`privacyPolicyUrl`](#directory-listing-fields) | String | Ссылка на политику конфиденциальности для страницы плагина в каталоге Anthropic. Claude Code не читает его |
| [`termsOfServiceUrl`](#directory-listing-fields) | String | Ссылка на условия использования для страницы плагина в каталоге Anthropic. Claude Code не читает его |
| [`defaultEnabled`](#defaultenabled) | Boolean | Включен ли плагин при запуске, когда пользователь не установил его. По умолчанию `true` |
| `engines` | Object | Версии Claude Code, на которых работает плагин, в виде [диапазона semver](https://github.com/npm/node-semver#ranges) под ключом `claude-code`, например `"engines": { "claude-code": ">=2.1.400" }`. Требуется Claude Code v2.1.323 или новее. Чтобы плагин продолжал работать в версиях с v2.0.15 по v2.1.75, не указывайте `engines`. Эти версии отклоняют манифест с ошибкой `Unrecognized key`, если в нем есть это поле |
| [`dependencies`](#dependencies) | Array of strings or objects | Плагины, которые должны быть включены для работы этого |
| [`userConfig`](#user-configuration) | Object | Значения, которые Claude Code запрашивает у пользователя при включении плагина |
| `types` | Path | Файл `.d.ts`, который объявляет значения `$.state` и существительные `$` [mod](https://code.claude.com/docs/ru/plugins/mods/reference.md#files) |
| [`channels`](#channels) | Array of objects | Каналы сообщений, которые предоставляет плагин, каждый привязан к одному из его MCP серверов |
| `skills` | Path, or array of paths | Директории для сканирования skills, каждая — директория папок `<name>/SKILL.md` или одна папка, содержащая `SKILL.md` напрямую. `"."` обозначает корень плагина. Добавляет к сканированию по умолчанию `skills/` |
| [`commands`](#commands) | Path, array of paths, or object | Плоские файлы команд `.md`, директории с ними или объект-карта имени команды на `source` или `content`. Заменяет сканирование по умолчанию `commands/` |
| `agents` | Path, or array of paths | Файлы агентов `.md`. Директории не принимаются. Заменяет сканирование по умолчанию `agents/` |
| [`hooks`](#hooks) | Path, object, or array of either | Файлы hook `.json` или встроенная конфигурация hook. Загружаются вместе с `hooks/hooks.json` |
| [`mcpServers`](#mcpservers) | Path, object, or array of either | Файлы конфигурации MCP `.json`, пакеты `.mcpb` или `.dxt`, или встроенные конфигурации серверов с ключами по имени. Загружаются вместе с `.mcp.json`; имя сервера, объявленное позже, заменяет более раннее |
| [`lspServers`](#lspservers) | Path, object, or array of either | Файлы конфигурации LSP `.json` или встроенные конфигурации серверов с ключами по имени. Загружаются вместе с `.lsp.json` |
| `outputStyles` | Path, or array of paths | Файлы стилей вывода или директории. Заменяет сканирование по умолчанию `output-styles/` |
| `workflows` | Path, or array of paths | Файлы [Workflow](https://code.claude.com/docs/ru/workflows.md#distribute-a-workflow-in-a-plugin) `.js` или директории. Заменяет сканирование по умолчанию `workflows/` |
| `experimental` | Object | Контейнер для `themes`, `monitors` и `evals`, чья форма манифеста может еще измениться |
| `experimental.themes` | Path, or array of paths | Файлы тем или директории. Заменяет сканирование по умолчанию `themes/`. Ключ `themes` верхнего уровня все еще загружается с предупреждением `claude plugin validate` |
| [`experimental.monitors`](#monitors) | Path, or inline array | Файл `.json`, содержащий массив monitors, или сам массив. По умолчанию `monitors/monitors.json`. Ключ `monitors` верхнего уровня все еще загружается с предупреждением `claude plugin validate`. Мониторы [не запускаются с флагом `-p`](https://code.claude.com/docs/ru/plugins/components#monitors) |
| `experimental.evals` | Path, or array of paths | Директория, которая содержит [eval cases](https://code.claude.com/docs/ru/plugin-evals.md#use-a-different-eval-directory) плагина, когда это не директория по умолчанию `evals/`. `claude plugin eval --eval-dir` переопределяет ее |

В столбце Type путь — это строка относительно корня плагина, например `"./custom/commands"`.

### `name`

Идентификатор плагина. Он должен быть непустым, без пробелов, `@`, `:`, разделителей пути, управляющих символов или символов двунаправленного форматирования; используйте kebab-case.

Claude Code помещает каждый компонент в пространство имен под ним, поэтому агент `reviewer` в плагине `deploy-tools` появляется как `deploy-tools:reviewer`.

`claude plugin validate` также проверяет, что имя не проходит как один из собственных плагинов Anthropic. Проверка игнорирует регистр и рассматривает любой набор разделителей как один:

| Имя | Результат |
| :- | :- |
| Начинается с `claude-`, `anthropic-`, `anthropics-` или `cc-plugin-` | Ошибка |
| Это `claude`, `anthropic`, `anthropics`, `claude-code` или `claude-mods` | Ошибка |
| Ставит `official` рядом с `claude` или `anthropic`, например `official-claude-tools` | Ошибка |
| Имеет `claude`, `anthropic` или `anthropics` как целое слово где-либо еще, например `mcp-for-claude` | Предупреждение |

Ошибка читается как `Plugin name "<name>" is reserved: it passes as one of Anthropic's own`, а предупреждение читается как `Plugin name "<name>" reads as one of Anthropic's own`. `claude plugin init` и `claude plugin tag` отказывают в имени, которое вызывает ошибку. Claude Code все еще устанавливает и загружает плагин, имя которого они отказывают.

### `displayName`

Имя, показываемое в UI вместо `name`. Оно может содержать пробелы и любой регистр, и оно не используется для пространства имен или поиска.

Для плагина, установленного из маркетплейса, `displayName` в [записи маркетплейса](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries) имеет приоритет над этим значением.

### `version`

Строка версии, не проверяемая против semver. Установка ее закрепляет плагин на этой версии, пока вы не измените ее; см. [Версии и обновления](https://code.claude.com/docs/ru/plugins/loading.md#versions-and-updates). Плагин с [`command` source](https://code.claude.com/docs/ru/plugins/marketplace-reference), плагин из [маркетплейса, размещенного на claude.ai](https://code.claude.com/docs/ru/plugins/install.md#add-from-claude-ai), и плагин [загруженный на месте](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk) из маркетплейса, добавленного по локальному пути, не закреплены этим полем.

### `metadata`

Объект произвольной формы для ваших собственных данных, таких как поля каталога или прав. Claude Code не читает его.

### Поля для страницы в каталоге

Каталог Anthropic считывает поля `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl` и `termsOfServiceUrl` из `plugin.json` для страницы вашего плагина, когда вы [отправляете плагин](https://code.claude.com/docs/ru/plugins/publish.md#submit-to-anthropics-directory). Claude Code игнорирует их при загрузке. Задавайте их только в `plugin.json`. В [записи маркетплейса](#marketplace-entries-and-the-manifest) `claude plugin validate` сообщает о каждом из них как о неизвестном поле.

Укажите в `icon` путь к файлу изображения внутри плагина, например `./logo.png`, а в каждом из четырех полей URL — URL вида `https://`.

> [!NOTE]
>
> `claude plugin validate` не сообщает об этих полях в `plugin.json` как о неизвестных в Claude Code v2.1.281 или позже. Более ранние версии выводят предупреждение `Unknown field` для каждого из них, поэтому запуск с `--strict` в этих версиях завершается ошибкой.

### `defaultEnabled`

Включен ли плагин при запуске, когда пользователь не установил его в [`enabledPlugins`](https://code.claude.com/docs/ru/settings-reference#enabledplugins). По умолчанию `true`. Плагин, от которого зависит включенный плагин, запускается включенным независимо. То же поле в записи маркетплейса переопределяет это.

После того как запись `enabledPlugins` пользователя написана, она сохраняется при обновлениях плагина, поэтому изменение `defaultEnabled` в более позднем выпуске не изменяет параметр для существующего пользователя.

### `dependencies`

Плагины, которые должны быть включены для работы этого. Каждая запись — это `"name"`, `"name@marketplace"` или `{ "name": "...", "marketplace": "...", "version": "..." }`. Простые имена разрешаются против собственного маркетплейса этого плагина. См. [ограничения зависимостей](https://code.claude.com/docs/ru/plugins/dependencies.md).

## Формы путей компонентов

Каждый ключ компонента принимает путь относительно корня плагина. `hooks`, `mcpServers`, `lspServers` и `experimental.monitors` также принимают встроенную конфигурацию, `commands` также принимает объект-карту, и `mcpServers` также принимает пути пакетов MCP и URL. Примеры, которые следуют, показывают каждую принятую форму один раз. Для того, что каждый компонент делает во время выполнения, см. [Компоненты плагина](https://code.claude.com/docs/ru/plugins/components.md).

### Поля только с путями

`agents`, `skills`, `outputStyles`, `workflows` и `experimental.themes` принимают один путь или массив путей. Записи `agents` должны быть файлами `.md`, а записи `skills` должны быть директориями. Остальные три принимают директорию или файл.

```json theme={null}
{
  "agents": ["./custom-agents/reviewer.md", "./custom-agents/tester.md"],
  "skills": ["./extra-skills/", "."],
  "outputStyles": "./styles/"
}
```

### `commands`

`commands` принимает путь, массив путей или объект-карту. Путь обозначает плоский файл команды `.md` или директорию. В объект-карте каждый ключ становится именем команды после префикса плагина. Например, `"about"` в плагине `deploy-tools` запускается как `/deploy-tools:about`.

Каждое значение устанавливает ровно один из `source` или `content`, и запись, которая устанавливает оба или ни один, не проходит проверку. Остальные поля в этой таблице являются необязательными:

| Поле | Тип | Описание |
| :- | :- | :- |
| `source` | string | Путь к файлу Markdown команды относительно корня плагина |
| `content` | string | Встроенный Markdown для тела команды вместо `source` |
| `description` | string | Описание, показываемое для команды |
| `argumentHint` | string | Подсказка аргумента, показываемая после имени команды, например `[file]` |
| `model` | string | Модель по умолчанию для команды |
| `allowedTools` | array of strings | Инструменты, которые команда может использовать без запроса |

Эта карта объявляет одну команду из файла и одну из встроенного содержимого:

```json theme={null}
{
  "commands": {
    "status": { "source": "./commands/status.md", "argumentHint": "[env]" },
    "about": { "content": "Explain what this plugin provides." }
  }
}
```

### `hooks`

`hooks` принимает путь файла `.json`, встроенный объект hooks в той же форме, что и [`hooks` в `settings.json`](https://code.claude.com/docs/ru/hooks#configuration), или массив, смешивающий оба. Для событий hook и полей обработчика см. [справочник hooks](https://code.claude.com/docs/ru/hooks.md#hook-events).

Файл хуков оборачивает карту событий в ключ верхнего уровня `"hooks"` — это та же форма, которую использует [`hooks/hooks.json`](https://code.claude.com/docs/ru/plugins/components#hooks). Файл, содержащий только карту событий без этой обёртки, не загружается. Встроенный объект — это сама карта событий, без обёртки.

Claude Code объединяет все, что вы объявляете, с `hooks/hooks.json`, когда этот файл существует. Этот массив загружает один файл хуков и объявляет один встроенный хук `PostToolUse`:

```json theme={null}
{
  "hooks": [
    "./config/extra-hooks.json",
    {
      "PostToolUse": [
        {
          "matcher": "Write|Edit",
          "hooks": [
            { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.sh" }
          ]
        }
      ]
    }
  ]
}
```

Файл, указанный в этом массиве, содержит обёртку `"hooks"` вокруг собственной карты событий:

```json config/extra-hooks.json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/check-command.sh" }
        ]
      }
    ]
  }
}
```

### `mcpServers`

`mcpServers` принимает путь файла `.json`, путь пакета MCP или URL, встроенную карту или массив, смешивающий их. Для полей конфигурации сервера см. [MCP серверы, предоставляемые плагином](https://code.claude.com/docs/ru/mcp.md#plugin-provided-mcp-servers).

Claude Code загружает `.mcp.json` в корне плагина первым, затем каждую объявленную форму по порядку. Имя сервера, объявленное позже, заменяет более раннее.

Значение `mcpServers` принимает одну из этих форм:

| Форма | Пример значения | Что делает Claude Code |
| :- | :- | :- |
| Путь файла `.json` | `"./mcp/servers.json"` | Читает файл как карту `mcpServers` |
| Путь пакета MCP | `"./bundle.mcpb"` | Извлекает пакет `.mcpb` или `.dxt` в `mcpb/` внутри [корневого каталога плагинов](https://code.claude.com/docs/ru/plugins/loading.md#find-plugins-on-disk) и читает его конфигурацию сервера |
| URL пакета MCP | `"https://example.com/server.mcpb"` | Загружает пакет, затем извлекает и читает его тем же способом |
| Встроенная карта | `{ "deploy-api": { "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"] } }` | Использует карту как конфигурации серверов с ключами по имени |

Путь пакета или URL должен заканчиваться на `.mcpb` или `.dxt`. Любое другое расширение не проходит проверку.

### `lspServers`

`lspServers` принимает путь файла `.json`, встроенную карту имени сервера на конфигурацию или массив любого из них.

Claude Code загружает `.lsp.json` в корне плагина первым, затем каждую объявленную конфигурацию по порядку. Имя сервера, объявленное позже, заменяет более раннее.

Каждая конфигурация сервера — это строгий объект с этими полями. Неизвестный ключ не проходит проверку.

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `command` | Yes | Бинарный файл языкового сервера. Без пробелов, если значение не начинается с `/`; поместите аргументы в `args` |
| `extensionToLanguage` | Yes | Карта расширения файла на ID языка LSP, по крайней мере одна запись. Ключи начинаются с точки, например `".go"` |
| `args` | No | Аргументы, передаваемые серверу |
| `transport` | No | Транспорт связи: `stdio` (по умолчанию) или `socket`. Claude Code принимает `socket`, но запускает каждый сервер через stdio, поэтому правила протокола stdout применяются ко всем серверам |
| `env` | No | Переменные окружения для процесса сервера |
| `initializationOptions` | No | Опции, отправляемые в запросе инициализации |
| `settings` | No | Параметры, отправляемые `workspace/didChangeConfiguration` |
| `workspaceFolder` | No | Путь папки рабочего пространства для сервера |
| `startupTimeout` | No | Миллисекунды для ожидания запуска, положительное целое число |
| `shutdownTimeout` | No | Миллисекунды для ожидания корректного завершения, положительное целое число. Когда истекает время ожидания, Claude Code завершает процесс сервера. Если не установлено, время ожидания не применяется |
| `requestTimeout` | No | Миллисекунды для ожидания ответа сервера на запрос, положительное целое число. По умолчанию `60000`, поэтому запрос, на который сервер так и не ответил, завершается ошибкой через 60 секунд. Требуется версия v2.1.288 или новее |
| `restartOnCrash` | No | Перезапускать ли сервер после сбоя. По умолчанию `true`. Установите `false`, чтобы оставить упавший сервер остановленным вместо перезапуска |
| `maxRestarts` | No | Попытки перезапуска перед отказом, ноль или больше |
| `diagnostics` | No | Отправлять ли диагностику в контекст после редактирования. По умолчанию `true` |

Эта встроенная конфигурация запускает `gopls` для файлов `.go`:

```json theme={null}
{
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": { ".go": "go" }
    }
  }
}
```

Для языковых серверов, которые Anthropic публикует как плагины, и того, как серверы ведут себя во время выполнения, см. [Интеллект кода](https://code.claude.com/docs/ru/plugins/code-intelligence.md).

### `monitors`

`experimental.monitors` принимает путь файла `.json` или встроенный массив. Когда вы опускаете ключ, Claude Code загружает `monitors/monitors.json`, если он существует.

Каждая запись — это строгий объект с этими полями.

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `name` | Yes | Идентификатор, уникальный в пределах плагина |
| `command` | Yes | Команда оболочки, которую Claude Code запускает как постоянный фоновый процесс в директории работы сеанса |
| `description` | Yes | Краткое резюме, показываемое в панели задач и сводках уведомлений |
| `when` | No | С `"always"`, по умолчанию, монитор запускается при запуске сеанса и при перезагрузке плагина. С `"on-skill-invoke:<skill>"`, он запускается в первый раз, когда запускается этот skill |

Этот встроенный массив объявляет один монитор, который запускается в первый раз, когда запускается skill `deploy`:

```json theme={null}
{
  "experimental": {
    "monitors": [
      {
        "name": "deploy-status",
        "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh",
        "description": "Deployment status changes",
        "when": "on-skill-invoke:deploy"
      }
    ]
  }
}
```

Команда монитора `command` не может ссылаться на `${user_config.*}`. См. [Поля, которые работают через оболочку](#fields-that-run-through-a-shell).

## Правила путей

Каждый путь компонента в манифесте относителен корню плагина и должен начинаться с `./`. Путь, такой как `commands/foo.md`, не проходит проверку. `skills` и `mcpServers` каждый принимают одну форму вне этого правила:

* **`skills`**: также принимает `"."`. Оба `"."` и `"./"` обозначают корень плагина
* **`mcpServers`**: также принимает URL пакета `https://`

`experimental.evals` не является путем компонента, поэтому правила этого раздела на него не распространяются, и вместо этого `claude plugin eval` проверяет значение при запуске. Оно указывает директорию внутри корня плагина, например `"quality/evals"`, с префиксом `./` или без него. Если задан массив, используется только первый элемент. О том, какие значения допустимы и что происходит с непригодным значением, см. [Использование другой директории для eval](https://code.claude.com/docs/ru/plugin-evals.md#use-a-different-eval-directory).

### Содержание и существование

Каждый путь компонента должен разрешаться внутри корня плагина и должен существовать. `claude plugin validate` проверяет пути под каждым ключом компонента:

* **Содержание**: путь, который разрешается вне корня плагина, не загружается, и вкладка `/plugin` **Errors** показывает `<component> path escapes plugin directory: <path>`. Путь, содержащий `..`, — обычный случай, и `claude plugin validate` сообщает об ошибке `Path contains ".." which could be a path traversal attempt`. Для файла `mcpServers` или `lspServers` сообщение [`path not read`](https://code.claude.com/docs/ru/errors#server-file-path-not-read) означает, что путь абсолютный или содержит `..`
* **Существование**: путь, который не существует, не загружается, и вкладка `/plugin` **Errors** показывает `<component> path not found: <path>`. `claude plugin validate` сообщает об ошибке `Path not found`

Для путей `outputStyles`, `lspServers`, `monitors` и `themes` проверка `claude plugin validate` требует Claude Code v2.1.283 или более поздней версии.

### Как каждый ключ объединяется с его расположением по умолчанию

Каждый ключ компонента либо заменяет его расположение по умолчанию, добавляет к нему, либо объединяется с ним:

* **Заменяет по умолчанию**: `commands`, `agents`, `outputStyles`, `workflows`, `experimental.themes`, `experimental.monitors`. Когда вы устанавливаете `commands`, директория по умолчанию `commands/` не сканируется. Чтобы сохранить по умолчанию и добавить больше, перечислите его явно: `"commands": ["./commands/", "./extras/"]`
* **Добавляет к по умолчанию**: `skills`. Директория `skills/` все еще сканируется, и перечисленные директории загружаются вместе с ней
* **Объединяет**: `hooks`, `mcpServers`, `lspServers`. Файл по умолчанию загружается первым, и то, что объявляет манифест, объединяется в него, как описано в [Формы путей компонентов](#component-path-forms)

Если плагин имеет папку по умолчанию, такую как `commands/`, и также устанавливает ключ манифеста, который ее заменяет, Claude Code загружает пути манифеста, а не папку. `claude plugin list` и интерфейс `/plugin` затем показывают предупреждение `Default <folder>/ folder is ignored because the manifest sets "<key>"`.

Чтобы избежать предупреждения, установите ключ на путь внутри этой папки: `"commands": ["./commands/deploy.md"]` обозначает файл в папке по умолчанию и не производит предупреждение.

## Конфигурация пользователя

`userConfig` объявляет значения, которые Claude Code запрашивает у пользователя при включении плагина, поэтому пользователи не редактируют `settings.json` сами.

Ключи — это идентификаторы, состоящие из букв, цифр и подчеркиваний, и не могут начинаться с цифры.

Каждое значение — это строгий объект с этими полями. Неизвестный ключ не проходит проверку.

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `type` | Yes | Один из `string`, `number`, `boolean`, `directory` или `file` |
| `title` | Yes | Метка, показываемая в диалоге конфигурации |
| `description` | Yes | Справочный текст, показываемый под полем |
| `required` | No | Если `true`, диалог конфигурации не принимает пустое значение |
| `default` | No | Значение, используемое, когда пользователь ничего не предоставляет: строка, число, логическое значение или массив строк |
| `options` | No | Для `string`, значения, которые принимает поле, показываемые как выбор в `/config`. См. [Ограничить поле фиксированными опциями](#limit-a-field-to-fixed-options). Требует Claude Code v2.1.271 или позже |
| `multiple` | No | Для `string`, позволяет массив строк |
| `sensitive` | No | Если `true`, маскирует ввод и сохраняет значение в безопасном хранилище вместо `settings.json` |
| `min` / `max` | No | Границы для `number` |

Каждая опция каждого включенного плагина также появляется как строка в панели `/config`, кроме `sensitive` опций и `multiple` списков. Строки `/config` требуют Claude Code v2.1.269 или позже.

Этот `userConfig` объявляет конечную точку и замаскированный токен:

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

### Ограничить поле фиксированными опциями

Установите `options` на поле `userConfig`, чтобы пользователи выбирали его значение из фиксированного списка.

Чтобы ограничить поле `tone` тремя опциями, перечислите их в `options` и установите `default` на одну из них:

```json theme={null}
{
  "userConfig": {
    "tone": {
      "type": "string",
      "title": "Tone",
      "description": "Voice for generated replies",
      "options": ["neutral", "warm", "formal"],
      "default": "neutral"
    }
  }
}
```

Если вы объявляете `options` на любом поле, пользователи на версиях Claude Code до v2.1.271 не могут загрузить плагин.

`options` применяется к полю `string`, которое не является `multiple` или `sensitive`. Установите `default` на одно из перечисленных значений или установите `required: true`, чтобы пользователь выбрал одно. Каждая опция — это простая метка от 1 до 64 символов, и `claude plugin validate`, который вы запускаете в вашей оболочке, сообщает обо всем остальном, что он отклоняет. Плагин, чьи `options` нарушают эти правила, не загружается.

### Где сохраняются значения

Нечувствительные значения сохраняются в [`pluginConfigs`](https://code.claude.com/docs/ru/settings-reference#pluginconfigs) в `settings.json` пользователя. Чувствительные значения идут в безопасное хранилище учетных данных платформы вместо этого. На [странице параметров](https://code.claude.com/docs/ru/settings-reference.md#pluginconfigs) указано, из каких файлов параметров читается `pluginConfigs`.

### Ссылка на сохраненное значение

Ссылайтесь на сохраненное значение, где плагин его нужен, в одной из двух форм:

* **`${user_config.KEY}`**: подставляется в конфигурацию MCP сервера, конфигурацию LSP сервера, [exec-form](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form) hook `args` и содержимое skill и agent. В содержимом skill и agent подставляются только нечувствительные значения, и чувствительное значение там становится заполнителем
* **`CLAUDE_PLUGIN_OPTION_<KEY>`**: экспортируется в процессы hook для каждой опции, с `<KEY>` в верхнем регистре. Shell-form hook читает `$CLAUDE_PLUGIN_OPTION_API_TOKEN` для `api_token`

### Поля, которые работают через оболочку

Shell-form hook команды, команды монитора и MCP [`headersHelper`](https://code.claude.com/docs/ru/mcp#use-dynamic-headers-for-custom-authentication) отклоняют `${user_config.*}`. Компонент, который ссылается на него в одном из этих полей, не работает с [ошибкой](https://code.claude.com/docs/ru/errors.md#plugin-command-references-user-config) вместо запуска, потому что значение поля передается оболочке, которая переанализирует подставленное значение.

Таблица показывает, как значение может достичь каждого из этих полей вместо этого.

| Поле | Как значение может достичь его |
| :- | :- |
| Shell-form hook команды | Используйте [exec form](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form) с `args` или читайте `CLAUDE_PLUGIN_OPTION_<KEY>` из окружения hook |
| Команды монитора | Не через Claude Code. Процессы монитора не получают `CLAUDE_PLUGIN_OPTION_<KEY>`, поэтому скрипт монитора должен получить значение самостоятельно |
| MCP `headersHelper` | Не через Claude Code. Окружение помощника содержит `CLAUDE_PLUGIN_ROOT`, `CLAUDE_CODE_MCP_SERVER_NAME` и `CLAUDE_CODE_MCP_SERVER_URL`, но не значения опций, поэтому скрипт помощника должен получить значение самостоятельно |

## Каналы

`channels` объявляет каналы сообщений, которые предоставляет плагин, такие как мост к приложению чата. Когда вы объявляете один, Claude Code может запросить конфигурацию канала при включении плагина. Для того, как сервер внедряет сообщения, см. [справочник каналов](https://code.claude.com/docs/ru/channels-reference.md#package-as-a-plugin).

Каждая запись — это строгий объект, привязанный к одному из MCP серверов плагина, с этими полями:

| Поле | Обязательное | Описание |
| :- | :- | :- |
| `server` | Yes | Ключ MCP сервера в `mcpServers` этого плагина, к которому привязан канал |
| `displayName` | No | Имя, показываемое в заголовке диалога конфигурации. По умолчанию имя сервера |
| `userConfig` | No | Опции для запроса, в той же форме, что и [верхнего уровня `userConfig`](#user-configuration). Сохраненные значения подставляются в ссылки `${user_config.KEY}` в `env` сервера |

Этот манифест привязывает канал к MCP серверу `telegram` плагина и запрашивает токен бота, который подставляется в `env` сервера:

```json theme={null}
{
  "mcpServers": {
    "telegram": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": { "BOT_TOKEN": "${user_config.bot_token}" }
    }
  },
  "channels": [
    {
      "server": "telegram",
      "displayName": "Telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        }
      }
    }
  ]
}
```

## Переменные окружения

Claude Code предоставляет три переменные пути компонентам плагина. Ссылайтесь на них как `${NAME}` в полях, перечисленных в [Где каждая переменная разрешается](#where-each-variable-resolves), и читайте их как переменные окружения в процессах, которые их получают.

| Переменная | Разрешается в | Используйте для |
| :- | :- | :- |
| `${CLAUDE_PLUGIN_ROOT}` | Абсолютный путь установленной версии плагина | Скрипты, бинарные файлы и файлы конфигурации, поставляемые с плагином |
| `${CLAUDE_PLUGIN_DATA}` | `~/.claude/plugins/data/<id>/`, создается при первой ссылке и сохраняется при обновлениях плагина. `<id>` — это идентификатор плагина с каждым символом, отличным от буквы, цифры, `_` или `-`, замененным на `-` | Установленные зависимости, такие как `node_modules`, сгенерированный код и кэши |
| `${CLAUDE_PROJECT_DIR}` | Корень проекта | Скрипты и файлы конфигурации, локальные для проекта |

`${CLAUDE_PLUGIN_ROOT}` изменяется при обновлении плагина, поэтому не записывайте состояние туда. Для того, где корень перемещается и когда старая директория очищается, см. [страницу загрузки](https://code.claude.com/docs/ru/plugins/loading.md).

По умолчанию Claude Code удаляет директорию `${CLAUDE_PLUGIN_DATA}` при удалении плагина из последнего места, где он установлен. Для `--keep-data` и других случаев, когда она сохраняется, см. [удаление плагина](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-uninstall).

### Где каждая переменная разрешается

В каждом компоненте плагина ссылки `${...}` разрешаются встроенным образом в определенных полях, и некоторые компоненты также получают переменные в окружении их процесса:

| Компонент плагина | Поля, где `${...}` разрешается | Экспортируется в процесс |
| :- | :- | :- |
| Hook команды | Где угодно в `command` и `args` | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR` и `CLAUDE_PLUGIN_OPTION_<KEY>` |
| Monitor команды | Где угодно в `command` | Не экспортируется |
| MCP `stdio` серверы | `command`, `args`, `env` | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR` |
| MCP `http`, `sse`, `ws` серверы | `url`, `headers`, `headersHelper` | Не применимо |
| LSP серверы | `command`, `args`, `env`, `workspaceFolder` | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR` |
| Skill, команда и содержимое агента | Где угодно в теле Markdown | Не применимо |

Переменные отсутствуют в окружении команд, которые Claude запускает через инструмент Bash, в основном сеансе или в подагенте. В содержимом skill, команды и агента напишите ссылку `${...}` в теле Markdown вместо этого, и Claude Code подставляет путь встроенным образом при загрузке содержимого.

### Кавычки и разделители пути

Сохраняйте каждый подставленный путь одним аргументом:

* **Hook команды**: используйте [exec form](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form) с `args`, чтобы каждый путь был одним аргументом без кавычек
* **Shell-form hooks и monitor команды**: оберните переменную в двойные кавычки, чтобы путь с пробелами оставался одним словом

Если вы оставите одну из этих переменных вне кавычек в shell-form команде в файле hooks, `claude plugin validate` выдаст предупреждение, если только hook не устанавливает [`shell`](https://code.claude.com/docs/ru/hooks#command-hook-fields) на `"powershell"`.

Этот shell-form hook запускает скрипт, поставляемый с плагином:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

На Windows большинство подставленных путей используют прямые слэши, например `C:/Users/you/...`. Собственные обратные слэши сохраняются в [хуке в exec form](https://code.claude.com/docs/ru/hooks.md#exec-form-and-shell-form) и в хуке, который выполняется через PowerShell — оболочку по умолчанию на Windows, когда Git Bash не установлен.

## Стандартное расположение

Каждый тип компонента имеет расположение по умолчанию в корне плагина, используемое, когда манифест не указывает иное.

| Компонент | Расположение по умолчанию | Содержимое |
| :- | :- | :- |
| Манифест | `.claude-plugin/plugin.json` | Метаданные и конфигурация плагина. Необязательно |
| Skills | `skills/` | Один `<name>/SKILL.md` на skill. Плагин с `SKILL.md` в корне, без `skills/` и без ключа `skills` загружается как один skill |
| Команды | `commands/` | Плоские файлы команд Markdown. Предпочитайте `skills/` для новых плагинов |
| Агенты | `agents/` | Файлы Markdown агентов. Подпапки являются частью [имени агента](https://code.claude.com/docs/ru/plugins/components.md#agents) |
| Hooks | `hooks/hooks.json` | Конфигурация hook |
| MCP серверы | `.mcp.json` | Определения MCP сервера |
| LSP серверы | `.lsp.json` | Конфигурации LSP сервера |
| Стили вывода | `output-styles/` | Файлы стилей вывода Markdown |
| Workflows | `workflows/` | Файлы Workflow `.js` |
| Темы | `themes/` | Файлы темы JSON |
| Мониторы | `monitors/monitors.json` | Массив мониторов |
| Исполняемые файлы | `bin/` | Файлы здесь находятся на `PATH` инструмента Bash при включении плагина, поэтому Claude запускает их как простые команды. claude.ai и Cowork не устанавливают плагин, который имеет эту директорию, включая тот, который вы [распространяете через параметры организации claude.ai](https://claude.com/docs/plugins/org-sync#keep-executables-out-of-the-top-level-bin-directory) |

Плагин, который использует расположения по умолчанию, плюс папку `scripts/`, которую вызывают его хуки, расположен следующим образом:

```text theme={null}
deploy-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── deploy/
│       └── SKILL.md
├── commands/
│   └── status.md
├── agents/
│   └── reviewer.md
├── hooks/
│   └── hooks.json
├── monitors/
│   └── monitors.json
├── output-styles/
│   └── terse.md
├── themes/
│   └── dracula.json
├── workflows/
│   └── release-audit.js
├── bin/
│   └── deploy-tool
├── scripts/
│   └── format.sh
├── .mcp.json
└── .lsp.json
```

Чтобы щелкнуть по этому расположению и прочитать, что делает каждый файл, откройте [обозреватель плагинов](https://code.claude.com/docs/ru/plugins/components.md#explore-the-plugin-directory).

`CLAUDE.md` в корне плагина не загружается как контекст, и `claude plugin validate` предупреждает, когда находит его. Чтобы включить инструкции, которые загружаются в контекст Claude, поместите их в skill.

## Записи маркетплейса и манифест

[Запись маркетплейса](https://code.claude.com/docs/ru/plugins/marketplace-reference.md) принимает [свои собственные поля](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries), включая `strict`, а также каждое поле на этой странице, кроме [полей листинга в каталоге](#directory-listing-fields).

Поле `strict` решает, может ли запись добавлять компоненты к плагину, который имеет свой `plugin.json`. По умолчанию `true`.

### Как поля записи объединяются с `plugin.json`

Запись либо служит манифестом, добавляет компоненты к нему, либо конфликтует с ним:

* **Нет `plugin.json`**: запись — это манифест, независимо от `strict`. Hooks записи загружаются только в встроенной форме объекта. Для пути файла или массива там вкладка `/plugin` **Errors** показывает ошибку `not yet supported in a marketplace entry`
* **`plugin.json` присутствует, `strict` не установлен или `true`**: Claude Code загружает манифест и добавляет `commands`, `agents`, `skills`, `outputStyles` и `themes` записи к нему. Для `hooks`, matchers записи для события заменяют matchers манифеста для того же события, и события, которые объявляет только манифест, сохраняют свои
* **`plugin.json` присутствует, `strict: false`**: запись, которая объявляет любой из `commands`, `agents`, `skills`, `hooks`, `outputStyles` или `themes`, — это конфликт, и плагин не загружается с `Plugin <name> has conflicting manifests`

Когда [запись маркетплейса, чей `source` — корень маркетплейса](https://code.claude.com/docs/ru/plugins/marketplace-reference), перечисляет определенные поддиректории `skills`, загружаются только эти поддиректории, и директория по умолчанию `skills/` плагина не сканируется. Ключ `skills` в манифесте вместо этого [добавляет к по умолчанию](#how-each-key-combines-with-its-default-location).

### Приоритет метаданных

Некоторые поля метаданных имеют фиксированный приоритет независимо от `strict`:

* **`defaultEnabled` и поля отображения**: `defaultEnabled` записи и ее [поля отображения](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#entry-and-plugin-json), такие как `displayName`, переопределяют манифеста
* **`version`**: `version` манифеста переопределяет запись
* **`name`**: когда запись перечисляет плагин под другим `name`, чем манифест, `enabledPlugins` использует имя записи, и компоненты находятся в пространстве имен под именем манифеста

Для полной таблицы приоритета см. [Строгий режим](https://code.claude.com/docs/ru/plugins/marketplace-reference.md).

## Следующие шаги

* [Добавить компоненты к плагину](https://code.claude.com/docs/ru/plugins/components.md): что каждый компонент делает во время выполнения, с примером, который проходит проверку
* [Справочник маркетплейса](https://code.claude.com/docs/ru/plugins/marketplace-reference.md): поля записи, которые маркетплейс может установить для вашего плагина
* [Справочник команд плагина](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-validate): флаги и вывод `claude plugin validate`
* [Устранение неполадок плагинов](https://code.claude.com/docs/ru/plugins/troubleshooting.md#claude-plugin-validate-reports-errors): каждое сообщение проверки с его исправлением
