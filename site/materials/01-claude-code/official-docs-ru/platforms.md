> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Платформы и интеграции

> Выберите, где запустить Claude Code и что к нему подключить. Сравните CLI, Desktop, VS Code, JetBrains, веб, мобильные приложения и интеграции, такие как Chrome, Slack и CI/CD.

Claude Code запускает один и тот же базовый движок везде, но каждая поверхность оптимизирована для разного способа работы. Эта страница поможет вам выбрать правильную платформу для вашего рабочего процесса и подключить инструменты, которые вы уже используете.

## Где запустить Claude Code

Выберите платформу в зависимости от того, как вы предпочитаете работать и где находится ваш проект.

| Платформа | Лучше всего для | Что вы получаете |
| :- | :- | :- |
| [CLI](https://code.claude.com/docs/ru/quickstart.md) | Рабочие процессы терминала, скриптинг, удалённые серверы | Полный набор функций, [Agent SDK](https://code.claude.com/docs/ru/headless.md), [использование компьютера](https://code.claude.com/docs/ru/computer-use.md) на macOS (Pro, Max и Ultra), сторонние поставщики |
| [Desktop](https://code.claude.com/docs/ru/desktop.md) | Визуальный просмотр, параллельные сессии, управляемая установка | Средство просмотра различий, предпросмотр приложения, [использование компьютера](https://code.claude.com/docs/ru/desktop.md#let-claude-use-your-computer) и [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch) на Pro, Max и Ultra |
| [VS Code](https://code.claude.com/docs/ru/vs-code.md) | Работа внутри VS Code без переключения на терминал | Встроенные различия, интегрированный терминал, контекст файла |
| [JetBrains](https://code.claude.com/docs/ru/jetbrains.md) | Работа внутри IntelliJ, PyCharm, WebStorm или других IDE JetBrains | Средство просмотра различий, совместное использование выделения, сеанс терминала |
| [Web](https://code.claude.com/docs/ru/claude-code-on-the-web.md) | Долгосрочные задачи, которые не требуют большого управления, или работа, которая должна продолжаться, когда вы не в сети | Облако, по умолчанию управляемое Anthropic; продолжается после отключения |
| [Mobile](https://code.claude.com/docs/ru/mobile.md) | Запуск и мониторинг задач вдали от вашего компьютера | Облачные сессии из приложения Claude для iOS и Android, [Remote Control](https://code.claude.com/docs/ru/remote-control.md) для локальных сессий, [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch) на Desktop на Pro, Max и Ultra |

CLI — это наиболее полная поверхность для работы, ориентированной на терминал: скриптинг и Agent SDK доступны только в CLI. Сторонние поставщики также работают в [VS Code](https://code.claude.com/docs/ru/vs-code.md#use-third-party-providers) и в [JetBrains](https://code.claude.com/docs/ru/feature-availability.md#features-available-on-every-provider), который запускает CLI в терминале вашей IDE. Корпоративные развёртывания [Desktop](https://code.claude.com/docs/ru/desktop.md) поддерживают Google Cloud's Agent Platform, и Desktop поддерживает [поставщиков шлюза](https://code.claude.com/docs/ru/llm-gateway-connect.md#desktop-app); для Amazon Bedrock или Microsoft Foundry используйте CLI или расширение IDE, или [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview), который запускает вкладку Code на этих поставщиках. Desktop и расширения IDE обменивают некоторые функции, доступные только в CLI, на визуальный просмотр и более тесную интеграцию с редактором. Веб работает в облаке, поэтому задачи продолжают выполняться после отключения. Mobile — это тонкий клиент для этих же облачных сеансов или для локального сеанса через Remote Control, и может отправлять задачи на Desktop с помощью Dispatch.

Вы можете смешивать поверхности в одном проекте. Конфигурация, память проекта и MCP серверы совместно используются на локальных поверхностях.

## Подключите ваши инструменты

Интеграции позволяют Claude работать с сервисами вне вашей кодовой базы.

| Интеграция | Что она делает | Используйте для |
| :- | :- | :- |
| [Chrome](https://code.claude.com/docs/ru/chrome.md) | Управляет вашим браузером с вашими авторизованными сеансами | Тестирование веб-приложений, заполнение форм, автоматизация сайтов без API |
| [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) | Запускает Claude в вашем конвейере CI | Автоматические проверки PR, сортировка проблем, запланированное обслуживание |
| [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md) | То же самое, что GitHub Actions для GitLab | Автоматизация, управляемая CI на GitLab |
| [Code Review](https://code.claude.com/docs/ru/code-review.md) | Автоматически проверяет каждый PR | Выявление ошибок перед проверкой человеком |
| [Slack](https://code.claude.com/docs/ru/slack.md) | Отвечает на упоминания `@Claude` в ваших каналах от имени вашей собственной учётной записи | Превращение отчётов об ошибках в pull requests из чата команды на планах Pro, Max и Ultra |
| [Claude Tag](https://claude.com/docs/claude-tag) | Запускает `@Claude` как общую идентификацию вашей организации с настроенным администратором доступом | Общий доступ команды на планах Team и Enterprise вместо сеансов Slack для каждого пользователя |

Для интеграций, не указанных здесь, [MCP серверы](https://code.claude.com/docs/ru/mcp.md) и [соединители](https://code.claude.com/docs/ru/desktop.md#connect-external-tools) позволяют подключить почти всё: Linear, Notion, Google Drive или ваши собственные внутренние API.

## Работайте, когда вы вдали от вашего терминала

Claude Code предлагает несколько способов работы, когда вы находитесь не у терминала. Они отличаются тем, что запускает работу, где работает Claude, и сколько настроек вам нужно выполнить.

| | Триггер | Claude работает на | Настройка | Лучше всего для |
| :- | :- | :- | :- | :- |
| [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch) | Отправьте задачу из мобильного приложения Claude | Ваша машина (Desktop) | [Свяжите мобильное приложение с Desktop](https://support.claude.com/en/articles/13947068) | Делегирование работы, когда вас нет, минимальная настройка |
| [Remote Control](https://code.claude.com/docs/ru/remote-control.md) | Управляйте запущенной сессией из [claude.ai/code](https://claude.ai/code) или мобильного приложения Claude | Ваша машина (CLI, Desktop или VS Code) | Запустите [`claude remote-control` или `/remote-control`](https://code.claude.com/docs/ru/remote-control#start-a-remote-control-session) | Управление текущей работой с другого устройства |
| [Channels](https://code.claude.com/docs/ru/channels.md) | Отправляйте события из приложения чата, такого как Telegram или Discord, или с вашего собственного сервера | Ваша машина (CLI) | [Установите плагин канала](https://code.claude.com/docs/ru/channels.md#quickstart) или [создайте свой](https://code.claude.com/docs/ru/channels-reference.md) | Реагирование на внешние события, такие как сбои CI или сообщения в чате |
| [Slack](https://code.claude.com/docs/ru/slack.md) | Упомяните `@Claude` в канале команды | Облако Anthropic | [Установите приложение Slack](https://code.claude.com/docs/ru/slack.md#setting-up-claude-code-in-slack) с включенным [Claude Code в веб-версии](https://code.claude.com/docs/ru/claude-code-on-the-web.md), в планах Pro, Max и Ultra | PR и рецензии из чата команды |
| [Self-hosted environments](https://code.claude.com/docs/ru/self-hosted-environments) | Запустите [облачную сессию](https://code.claude.com/docs/ru/claude-code-on-the-web.md) и выберите окружение вашей организации | Инфраструктура вашей организации | [Разверните runners](https://code.claude.com/docs/ru/self-hosted-environments-quickstart.md), в планах Team и Enterprise | Облачные сессии, которые должны работать внутри вашей сети |
| [Scheduled tasks](https://code.claude.com/docs/ru/scheduled-tasks.md) | Установите расписание | [CLI](https://code.claude.com/docs/ru/scheduled-tasks.md), [Desktop](https://code.claude.com/docs/ru/desktop-scheduled-tasks.md) или [облако](https://code.claude.com/docs/ru/routines.md) | Выберите частоту | Повторяющаяся автоматизация, такая как ежедневные проверки |

Если вы не уверены, с чего начать, [установите CLI](https://code.claude.com/docs/ru/quickstart.md) и запустите его в каталоге проекта. Если вы предпочитаете не использовать терминал, [Desktop](https://code.claude.com/docs/ru/desktop-quickstart.md) предоставляет вам тот же движок с графическим интерфейсом.

## Связанные ресурсы

### Платформы

* [Быстрый старт CLI](https://code.claude.com/docs/ru/quickstart.md): установка и запуск вашей первой команды в терминале
* [Desktop](https://code.claude.com/docs/ru/desktop.md): визуальный просмотр различий, параллельные сеансы, использование компьютера и Dispatch
* [VS Code](https://code.claude.com/docs/ru/vs-code.md): расширение Claude Code внутри вашего редактора
* [JetBrains](https://code.claude.com/docs/ru/jetbrains.md): расширение для IntelliJ, PyCharm и других IDE JetBrains
* [Web](https://code.claude.com/docs/ru/claude-code-on-the-web.md): облачные сеансы из вашего браузера на claude.ai/code, которые продолжают работать при отключении
* [Projects](https://code.claude.com/docs/ru/claude-projects.md): один разговор, в котором Claude координирует множество облачных сеансов для выполнения работы и отправляет отчёты
* [Mobile](https://code.claude.com/docs/ru/mobile.md): приложение Claude для [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) и [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) для запуска и мониторинга задач вдали от вашего компьютера

### Интеграции

* [Chrome](https://code.claude.com/docs/ru/chrome.md): автоматизация задач браузера с вашими авторизованными сеансами
* [Computer use](https://code.claude.com/docs/ru/computer-use.md): позвольте Claude открывать приложения и управлять вашим экраном на macOS
* [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md): запуск Claude в вашем конвейере CI
* [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md): то же самое для GitLab
* [Code Review](https://code.claude.com/docs/ru/code-review.md): автоматическая проверка при каждом pull request
* [Slack](https://code.claude.com/docs/ru/slack.md): отправка задач из чата команды и получение PR обратно в планах Pro, Max и Ultra
* [Claude Tag](https://claude.com/docs/claude-tag): запуск `@Claude` как общей идентификации вашей организации в планах Team и Enterprise

### Удалённый доступ

* [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch): отправьте задачу со своего телефона, и она может создать сеанс Desktop
* [Remote Control](https://code.claude.com/docs/ru/remote-control.md): управляйте работающим сеансом со своего телефона или браузера
* [Channels](https://code.claude.com/docs/ru/channels.md): отправляйте события из приложений чата или ваших собственных серверов в сеанс
* [Варианты планирования](https://code.claude.com/docs/ru/scheduled-tasks.md#compare-scheduling-options): запускайте промпты по повторяющемуся расписанию
