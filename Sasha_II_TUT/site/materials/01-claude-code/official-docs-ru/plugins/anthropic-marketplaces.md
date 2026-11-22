> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Маркетплейсы Anthropic

> Официальный и общественный маркетплейсы плагинов Anthropic для Claude Code: их названия, репозитории, способы добавления каждого и где просматривать их плагины.

Anthropic публикует два маркетплейса плагинов общего назначения для Claude Code: [официальный](https://github.com/anthropics/claude-plugins-official) и [общественный](https://github.com/anthropics/claude-plugins-community). Каждый из них представляет собой каталог плагинов в собственном репозитории GitHub. Когда вы устанавливаете плагин из одного из них в сессии Claude Code, вы вводите название маркетплейса после `@`, например `/plugin install commit-commands@claude-plugins-official`.

Используйте эту страницу, чтобы различать два маркетплейса и узнать, где проверить, есть ли нужный плагин в официальном маркетплейсе.

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Как установить плагин**: см. [Установка плагинов](https://code.claude.com/docs/ru/plugins/install.md)
> * **Неудачная установка**: см. [Устранение неполадок с плагинами](https://code.claude.com/docs/ru/plugins/troubleshooting.md)

Перейдите к нужной части страницы:

* Чтобы различать два маркетплейса по репозиторию, названию маркетплейса и способу получения каждого, см. [Маркетплейсы Anthropic](#anthropic’s-marketplaces).
* Чтобы найти плагин в официальном маркетплейсе, см. [Поиск плагинов в официальном маркетплейсе](#find-plugins-in-the-official-marketplace).

## Маркетплейсы Anthropic

Маркетплейс — это каталог плагинов, который репозиторий определяет в своём файле `.claude-plugin/marketplace.json`. Официальный и общественный маркетплейсы берутся каждый из своего репозитория GitHub. Anthropic также публикует тематические маркетплейсы, такие как `anthropics/skills` и `anthropics/knowledge-work-plugins`, которые вы добавляете в сессии Claude Code с помощью `/plugin marketplace add <owner>/<repo>`.

В этой таблице указаны репозиторий и название каждого маркетплейса — именно название вы вводите после `@`, когда устанавливаете плагин из этого маркетплейса. Название общественного маркетплейса — `claude-community`, а не название его репозитория.

| | Официальный | Общественный |
| :- | :- | :- |
| Репозиторий | [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) | [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) |
| Название маркетплейса | `claude-plugins-official` | `claude-community` |
| Что в нём | Плагины, которые поддерживает Anthropic, а также плагины от партнёров и других авторов | Сторонние плагины, которые их авторы отправили в Anthropic |
| Как его получить | Claude Code добавляет его при первом запуске интерактивной сессии в терминале, если это не заблокировано [управляемой политикой](https://code.claude.com/docs/ru/plugins/org.md#allow-the-official-marketplace-and-your-own) или `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`. Если он отсутствует, см. [Маркетплейс `claude-plugins-official` не найден](https://code.claude.com/docs/ru/plugins/troubleshooting#marketplace-claude-plugins-official-not-found) | Вы добавляете его в сессии Claude Code с помощью `/plugin marketplace add anthropics/claude-plugins-community` |

Если вы написали плагин и хотите, чтобы другие могли его установить, см. [Публикация плагина](https://code.claude.com/docs/ru/plugins/publish.md) — там рассказывается о собственном маркетплейсе и отправке в каталог Anthropic.

### Устаревший маркетплейс `claude-code-plugins`

> [!WARNING]
>
> Маркетплейс `claude-code-plugins` в `anthropics/claude-code` объявлен устаревшим. Чтобы добавить плагин, выполните `claude plugin install <plugin>@claude-plugins-official` в своей оболочке и пропустите любой шаг руководства, в котором выполняется `/plugin marketplace add anthropics/claude-code`.

Если у вас не установлен один из двух плагинов ниже, вы можете оставить свои плагины из `claude-code-plugins` и сам маркетплейс как есть. Они обновляются из репозитория `claude-plugins-official`.

* **`ralph-wiggum`**: этот плагин теперь называется `ralph-loop`, и его команды начинаются с `/ralph-loop:`. Если эти команды недоступны, выполните `claude plugin install ralph-loop@claude-plugins-official` в своей оболочке.
* **`claude-opus-4-5-migration`**: этот плагин выведен из эксплуатации, поэтому удалите его, выполнив `claude plugin uninstall claude-opus-4-5-migration@claude-code-plugins` в своей оболочке.

Если какой-либо другой плагин перестал работать, см. [Плагин установлен, но не работает](https://code.claude.com/docs/ru/plugins/troubleshooting.md#plugin-installed-but-not-working).

## Поиск плагинов в официальном маркетплейсе

По умолчанию Claude Code сам добавляет официальный маркетплейс `claude-plugins-official`. Большая часть того, что в нём представлено, поступает от партнёров и других авторов, а не от Anthropic: поставщики инструментов публикуют плагины, подключающие Claude Code к их сервисам, а Anthropic поддерживает меньший набор собственных плагинов, таких как `commit-commands`, `code-review`, `feature-dev` и [плагины языковых серверов](https://code.claude.com/docs/ru/plugins/code-intelligence.md). Каталог часто меняется, поэтому на этой странице он не приводится.

Чтобы узнать, что в нём есть, используйте вкладку **Discover** в `/plugin` в сессии Claude Code, где доступен поиск, или просмотрите [Claude Marketplace](https://claude.com/marketplace/plugins) в интернете.

## Просмотр и установка из маркетплейсов Anthropic

Искать плагин в маркетплейсах Anthropic можно в Claude Code, в интернете или на GitHub:

* **В Claude Code, просматривая список**: выполните `/plugin` в интерактивной сессии. Вкладка **Discover** показывает плагины из ваших маркетплейсов.
* **В Claude Code, по названию**: выполните `/plugin install <name>` в сессии — команда ищет это название в ваших маркетплейсах. Если плагин есть в одном из них, его сведения открываются на панели `/plugin`, и ничего не устанавливается, пока вы не выберете там [область действия установки](https://code.claude.com/docs/ru/plugins/install.md#install-a-plugin) и не подтвердите её. Если его нет, вы увидите `Plugin "<name>" not found in any marketplace`.
* **В интернете**: ищите по полному каталогу на [Claude Marketplace](https://claude.com/marketplace/plugins), где показано количество установок, а некоторые плагины отмечены как **Anthropic verified**.
* **На GitHub**: откройте `.claude-plugin/marketplace.json` в репозитории маркетплейса, например [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official). Этот файл и есть сам каталог.

Каталог Anthropic существует отдельно от этих маркетплейсов. Каталог — это перечень на claude.ai. Плагин, добавленный из каталога на claude.ai, попадает в Claude Code через [синхронизацию аккаунта](https://code.claude.com/docs/ru/plugins/loading.md#synced-plugins). Чтобы разместить там собственный плагин, см. [Отправка в каталог Anthropic](https://code.claude.com/docs/ru/plugins/publish.md#submit-to-anthropics-directory).

Чтобы установить плагин из настольного приложения или из скрипта либо узнать, что загружает облачная сессия, см. [Установка плагинов](https://code.claude.com/docs/ru/plugins/install.md).

### Добавление общественного маркетплейса

Общественный маркетплейс не зарегистрирован, пока вы не добавите его. В сессии Claude Code выполните `/plugin marketplace add anthropics/claude-plugins-community`, затем устанавливайте с суффиксом `@claude-community`.

Если `claude-plugins-official` отсутствует на вкладке **Marketplaces** в `/plugin`, добавьте его тем же способом с помощью `/plugin marketplace add anthropics/claude-plugins-official`.

Об ошибках `not found` и маркетплейсах, которые не удаётся добавить, см. [Устранение неполадок с плагинами](https://code.claude.com/docs/ru/plugins/troubleshooting.md#install-a-plugin).

## Сторонние маркетплейсы

Многих популярных плагинов нет ни в одном маркетплейсе Anthropic. Они находятся в собственных маркетплейсах их авторов — обычно это репозиторий GitHub с файлом `.claude-plugin/marketplace.json` в корне.

Anthropic не проверяет сторонние маркетплейсы, поэтому перед добавлением такого маркетплейса прочитайте [Безопасность и доверие к плагинам](https://code.claude.com/docs/ru/plugins/security.md).

Чтобы использовать сторонний маркетплейс, добавьте его репозиторий в сессии Claude Code с помощью `/plugin marketplace add <owner>/<repo>`, затем устанавливайте с помощью `/plugin install <plugin>@<marketplace-name>`. Название маркетплейса — это поле `name` в этом `marketplace.json`, и Claude Code выводит его после добавления маркетплейса.

О других способах добавления маркетплейса см. [Добавление маркетплейса](https://code.claude.com/docs/ru/plugins/install.md#add-a-marketplace).

## Дальнейшие шаги

* [Установка плагинов и управление ими](https://code.claude.com/docs/ru/plugins/install.md): установите плагин из одного из этих маркетплейсов и выберите область действия
* [Безопасность и доверие к плагинам](https://code.claude.com/docs/ru/plugins/security.md): что плагин может делать на вашем компьютере и как проверить его перед установкой
* [Плагины анализа кода](https://code.claude.com/docs/ru/plugins/code-intelligence.md): установите один из плагинов языковых серверов из официального маркетплейса
* [Создание маркетплейса](https://code.claude.com/docs/ru/plugins/create-marketplace.md): запустите собственный маркетплейс наряду с маркетплейсами Anthropic
