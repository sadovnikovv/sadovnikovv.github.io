> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Рекомендуйте plugins для вашей организации

> Добавьте блок relevance к записям marketplace plugins, чтобы Claude Code предлагал их, когда работа пользователя совпадает, и разрешите marketplace в управляемых параметрах.

Claude Code может предложить установку plugin из marketplace вашей организации, когда сеанс пользователя совпадает с сигналами, которые вы определяете для этого plugin. Сигналы включают рабочий каталог, файлы, которые прочитал Claude, и команды, которые запустил Claude. Вы определяете их, добавляя блок `relevance` к записи plugin в `marketplace.json`.

Оператор маркетплейса пишет записи `relevance`. Затем администратор добавляет маркетплейс в список разрешённых в управляемых настройках. В терминале пользователи не видят предложений из маркетплейса, пока он не будет добавлен в список разрешённых.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Вы хотите установить плагины**: см. [Установка и управление плагинами](https://code.claude.com/docs/ru/plugins/install.md)
> * **Вы хотите отключить предложения**: см. [Понимание того, как работает relevance плагинов](#understand-how-plugin-relevance-works), а для предложений, которые Claude делает в диалоге облачной сессии, — [Отключение предложений плагинов](https://code.claude.com/docs/ru/claude-code-on-the-web.md#turn-off-plugin-suggestions)

Начните с разделов для вашей роли:

* **Операторы marketplace**: прочитайте [как работают предложения](#understand-how-plugin-relevance-works), затем [добавьте relevance к записи plugin](#add-relevance-to-a-plugin-entry) и [проверьте ваш marketplace](#validate-your-marketplace)
* **Администраторы**: [включите предложения в управляемых параметрах](#enable-suggestions-in-managed-settings)

## Понимание того, как работает relevance plugin

Каждая запись plugin в `marketplace.json` может включать объект `relevance`. Объект называет тему и один или несколько сигналов. Сигнал — это шаблон, который Claude Code проверяет в текущем сеансе, например рабочий каталог или файлы, которые прочитал Claude.

Сопоставление сигналов происходит локально на машине пользователя и не добавляет сетевой трафик. Claude Code не сообщает, какие сигналы совпали или их значения Anthropic или оператору marketplace.

Когда сигнал совпадает и plugin еще не установлен, Claude Code предлагает plugin в этих местах:

* **Spinner tip**: сообщение с командой `/plugin install` появляется под спиннером, пока Claude отвечает.
* **Уведомление при запуске сеанса**: если сигнал `cwd` совпадает с рабочим каталогом, однострочное уведомление появляется перед тем, как пользователь отправит первое сообщение.
* **Вкладка `/plugin` Discover**: plugin закреплен в верхней части списка Discover.

[Предпросмотр того, что видит пользователь](#preview-what-the-user-sees) показывает точный текст каждого и как часто они повторяются.

Claude Code никогда не устанавливает plugin автоматически. Пользователь всегда подтверждает.

Spinner tip и уведомление при запуске сеанса оба перестают появляться, когда пользователь или проект устанавливает [`spinnerTipsEnabled`](https://code.claude.com/docs/ru/settings-reference#spinnertipsenabled) на `false`, или когда [`spinnerTipsOverride`](https://code.claude.com/docs/ru/settings-reference#spinnertipsoverride) с `excludeDefault` заменяет встроенные советы. Закрепление на вкладке Discover не зависит от обоих параметров.

## Добавление relevance к записи plugin

Добавьте объект `relevance` к записи plugin в вашем `marketplace.json`. Следующий пример объявляет, что plugin `terraform-helpers` актуален, когда Claude читает файл `.tf` или запускает `terraform`:

```json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Org" },
  "plugins": [
    {
      "name": "terraform-helpers",
      "source": "./plugins/terraform-helpers",
      "description": "Your organization's Terraform conventions and helpers",
      "relevance": {
        "topic": "Terraform",
        "signals": {
          "cli": ["terraform"],
          "filesRead": ["**/*.tf"]
        }
      }
    }
  ]
}
```

Пока ни один из его сигналов не совпадает, plugin сохраняет свою нормальную позицию в списке Discover и не появляется как spinner tip.

Чтобы проверить блок перед публикацией, [проверьте ваш marketplace](#validate-your-marketplace).

## Справочник полей

Объект `relevance` и его вложенный объект `signals` принимают поля в следующих таблицах.

Более старые клиенты по-прежнему загружают marketplace, который использует поля `relevance`, которые они не распознают, потому что неизвестные поля под `relevance` и `relevance.signals` игнорируются во время загрузки. Распознанное поле, значение которого превышает его лимит в [справочнике полей](#field-reference), делает недействительной всю запись plugin, и пользователи не могут установить этот plugin из marketplace, пока вы его не исправите; `claude plugin validate` сообщает те же лимиты.

### `relevance`

| Поле | Тип | Описание |
| :- | :- | :- |
| `topic` | string | Необязательно. Фраза, которая заполняет "Working with *topic*?" в spinner tip. По умолчанию имя plugin с каждым сегментом дефиса с заглавной буквы. Максимум 64 символа. |
| `signals` | object | Сопоставители, которые определяют, когда plugin актуален. Claude Code предлагает plugin только если установлен хотя бы один сигнал. См. [`relevance.signals`](#relevance-signals). |

`topic` часто является названием продукта, например `Terraform`. Используйте домен, такой как `design`, когда имя plugin не звучит естественно как тема.

### `relevance.signals`

Объект `signals` принимает следующие поля.

| Поле | Тип | Описание | Лимит |
| :- | :- | :- | :- |
| `cwd` | array of strings | Glob-шаблоны, сопоставленные с рабочим каталогом сеанса. См. [сопоставление рабочего каталога](#working-directory-matching). | 10 шаблонов по 256 символов каждый |
| `cli` | array of strings | Имена команд из shell-команд, которые Claude запустил в этом сеансе, например `["terraform"]`. Точное совпадение. См. [сопоставление имен команд](#command-name-matching). | 10 записей по 64 символа каждая |
| `hosts` | array of strings | Имена хостов, видимые в URL-адресах `http://` или `https://` в Bash-командах в этом сеансе, например `["registry.terraform.io"]`. Только голое имя хоста в нижнем регистре: без схемы, порта или пути. Точное совпадение без учета регистра. | 20 записей по 128 символов каждая |
| `filesRead` | array of strings | Glob-шаблоны, сопоставленные с путями файлов, которые Claude прочитал в этом сеансе, например `["**/*.tf"]`. Нормализовано прямой косой чертой и без учета регистра. | 10 шаблонов по 256 символов каждый |
| `manifestDeps` | array of objects | Зависимости, объявленные в манифестах пакетов, которые Claude прочитал в этом сеансе. Каждая запись — это `{ "file": "...", "pattern": "..." }`, где оба значения — регулярные выражения. См. [сопоставление зависимостей манифеста](#manifest-dependency-matching). | 10 записей, каждое значение максимум 256 символов. Файлы манифеста размером более 512 КБ пропускаются |

Сигналы `filesRead` и `manifestDeps` также совпадают с файлами, которые Claude написал или отредактировал в этом сеансе, и с файлами памяти `CLAUDE.md` проекта, загруженными автоматически.

#### Сопоставление рабочего каталога

`cwd` — единственный сигнал, который может совпадать при запуске сеанса, до того как пользователь отправит первое сообщение.

Claude Code сопоставляет каждый шаблон `cwd` следующим образом:

* Шаблон сопоставляется с рабочим каталогом как абсолютный путь. Когда сеанс находится внутри git-репозитория, он также сопоставляется с путем рабочего каталога относительно корня репозитория.
* Сопоставление нормализовано прямой косой чертой и без учета регистра.
* Каждый шаблон совпадает с самим каталогом и всем, что находится под ним, поэтому `infra`, `infra/` и `infra/**` ведут себя одинаково.

#### Сопоставление имен команд

Claude Code записывает одно имя команды для каждой shell-команды, которую запускает Claude: первый токен после любых назначений переменных окружения в начале и `sudo`. Составные команды вносят только свою ведущую команду, поэтому `cd infra && terraform plan` записывает `cd`, а не `terraform`.

#### Сопоставление зависимостей манифеста

Каждая запись `manifestDeps` объединяет две строки источника JavaScript `RegExp`:

* `file`: сопоставляется без учета регистра с путем файла манифеста. Путь обычно абсолютный, поэтому привяжите шаблон в конце, а не в начале. Пути не нормализуются по разделителям для этого сигнала, поэтому пути Windows используют обратные косые черты.
* `pattern`: сопоставляется с учетом регистра с содержимым этого файла.

Следующий пример использует `manifestDeps` для предложения вашего plugin после того, как Claude прочитал `package.json`, который зависит от npm-пакета вашего SDK, названного здесь `your-sdk`.

```json theme={null}
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "relevance": {
    "signals": {
      "manifestDeps": [
        {
          "file": "[/\\\\]package\\.json$",
          "pattern": "\"your-sdk\"\\s*:"
        }
      ]
    }
  }
}
```

В этом примере шаблон `file` использует `[/\\\\]`, чтобы он совпадал как с прямой косой чертой, так и с обратной косой чертой в разделителях пути, и `\\.`, чтобы точка была буквальной. В JSON каждая обратная косая черта в регулярном выражении написана дважды.

## Проверка вашего marketplace

В вашей оболочке запустите `claude plugin validate` для каталога вашего marketplace, чтобы проверить блок `relevance` перед публикацией:

```bash theme={null}
claude plugin validate ./my-marketplace
```

Валидатор сообщает об ошибках и предупреждениях в блоке `relevance`, включая следующие:

* Сообщает об неизвестных ключах под `relevance` и `relevance.signals` как предупреждения
* Отмечает значение `relevance`, которое не является объектом
* Отклоняет запись `signals.hosts`, которая включает схему, порт или путь

Каждый результат выводится с путем поля, которое его касается, и вывод заканчивается на `Validation passed`, `Validation passed with warnings` или `Validation failed`.

## Включение предложений в управляемых параметрах

В терминале пользователи не видят предложений из маркетплейса, пока администратор не добавит его в список разрешённых в [управляемых настройках](https://code.claude.com/docs/ru/plugins/org.md), даже когда его `marketplace.json` объявляет `relevance`.

Чтобы разрешить marketplace, отредактируйте ваши управляемые параметры следующим образом:

* Добавьте имя marketplace в `pluginSuggestionMarketplaces`.
* Для любого marketplace, отличного от официального marketplace Anthropic, также объявите источник marketplace, либо как запись этого имени в [`extraKnownMarketplaces`](https://code.claude.com/docs/ru/plugins/org#require-a-marketplace-and-its-plugins), либо как запись в [`strictKnownMarketplaces`](https://code.claude.com/docs/ru/plugins/org#allowlist-with-strictknownmarketplaces).

На машине, где marketplace не зарегистрирован или зарегистрирован под разрешенным именем из другого источника, предложения из него не появляются. Проверка источника предотвращает регистрацию несвязанного источника под разрешенным именем для получения предложений его plugins по всей вашей организации.

Следующий `managed-settings.json` регистрирует marketplace организации из GitHub-репозитория и включает его предложения:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": {
        "source": "github",
        "repo": "your-org/your-marketplace"
      }
    }
  },
  "pluginSuggestionMarketplaces": ["your-marketplace"]
}
```

Имя официального marketplace может регистрироваться только из официального источника Anthropic, поэтому ему не требуется объявление источника. Для официального marketplace разрешите только имя:

```json theme={null}
{
  "pluginSuggestionMarketplaces": ["claude-plugins-official"]
}
```

## Предпросмотр того, что видит пользователь

Когда сигнал `relevance` plugin совпадает во время сеанса, совет под спиннером читается:

```text theme={null}
Working with Terraform? Install the terraform-helpers plugin:
/plugin install terraform-helpers@your-marketplace
```

Когда сигнал `cwd` совпадает при запуске сеанса, однострочное уведомление читается:

```text theme={null}
plugin suggestion: terraform-helpers@your-marketplace · /plugin
```

На вкладке `/plugin` Discover plugin закреплен над другими результатами с аннотацией, которая называет совпадающий сигнал, такой как `suggested for this directory` или `suggested for terraform commands`.

Claude Code ограничивает, как часто он предлагает данный plugin:

* Предложение появляется максимум один раз каждые три сеанса в совокупности spinner tip и уведомления при запуске сеанса.
* Уведомление при запуске сеанса перестает появляться после того, как spinner tip и уведомление показали plugin в совокупности два раза.
* Ни spinner tip, ни уведомление при запуске сеанса не повторяются после установки plugin.
* Вкладка Discover закрепляет plugin в первый раз, когда пользователь открывает вкладку, пока сигналы plugin совпадают. Claude Code записывает это в `~/.claude.json`, поэтому каждый раз, когда пользователь позже открывает `/plugin` на этой машине, plugin появляется в нормальном порядке.

## См. также

* [Размещение marketplace](https://code.claude.com/docs/ru/plugins/host-marketplace.md): запустите marketplace, который размещает ваши plugins
* [Справочник Marketplace](https://code.claude.com/docs/ru/plugins/marketplace-reference.md#plugin-entries): каждое поле, которое принимает запись plugin
* [Рекомендуйте ваш plugin из вашего CLI](https://code.claude.com/docs/ru/plugins/cli-hints.md): предложите пользователям из вашего собственного CLI вместо сигналов сеанса Claude Code
* [Управление plugins для вашей организации](https://code.claude.com/docs/ru/plugins/org.md): `extraKnownMarketplaces`, `strictKnownMarketplaces` и остальные ключи политики plugin
