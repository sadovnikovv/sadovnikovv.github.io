> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Начало работы с настольным приложением

> Установите настольное приложение Claude, откройте вкладку Code и начните свой первый сеанс Claude Code в папке проекта на вашем компьютере.

Настольное приложение предоставляет вам Claude Code с графическим интерфейсом. Вы можете попросить Claude работать с кодом в папке на вашем компьютере, а затем самостоятельно просмотреть изменения без использования терминала.

Claude Code находится на вкладке **Code** в верхней части боковой панели приложения. На этой странице описывается установка приложения и начало вашей первой сессии на этой вкладке. Claude Code требует [подписку Pro, Max, Ultra, Team или Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).

> [card] [Скачать для macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)
>
> Универсальная сборка для Intel и Apple Silicon

> [card] [Скачать для Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)
>
> Для процессоров x64

> [card] [Получить Claude для Linux (бета)](https://code.claude.com/docs/ru/desktop-linux.md)
>
> apt или .deb для Ubuntu и Debian

Для Windows ARM64 скачайте [установщик ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). На Linux установите с помощью apt; см. [Claude Desktop на Linux](https://code.claude.com/docs/ru/desktop-linux.md).

> [!NOTE]
>
> Следующие случаи рассматриваются на других страницах:
>
> * **Уже настроено**: см. [Использование Claude Code Desktop](https://code.claude.com/docs/ru/desktop.md) для всех возможностей вкладки Code
> * **Хотите `claude` в вашем терминале**: [установите CLI](https://code.claude.com/docs/ru/quickstart.md) отдельно
> * **Используете чат или Cowork**: см. [Центр справки Claude](https://support.claude.com/)
> * **Нужна дополнительная информация об установке или развёртывании настольного приложения**: см. [статьи поддержки Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop)

## Установка

**1. Установка и вход в систему**

На macOS и Windows загрузите установщик по ссылкам выше и запустите его. На Linux следуйте инструкциям по установке в разделе [Claude Desktop на Linux](https://code.claude.com/docs/ru/desktop-linux.md). Запустите Claude из папки Applications на macOS, из меню Start на Windows или из средства запуска приложений на Linux, затем войдите со своей учетной записью Anthropic.

**2. Откройте вкладку Code**

Нажмите на вкладку **Code** в верхней части боковой панели. Если на вкладках отображаются только значки, наведите курсор на один из них, чтобы увидеть его название. Если после нажатия на **Code** появляется запрос или ошибка, воспользуйтесь соответствующим решением:

* **Запрос на обновление**: вам необходимо сначала [подписаться на платный план](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade)
* **Запрос на вход в систему онлайн**: завершите вход и перезапустите приложение
* **Ошибка 403**: см. [устранение неполадок аутентификации](https://code.claude.com/docs/ru/desktop.md#403-or-authentication-errors-in-the-code-tab)

Настольное приложение включает Claude Code, поэтому вам не нужно устанавливать Node.js или CLI для использования вкладки Code.

## Начните свой первый сеанс

С открытой вкладкой Code выберите проект и дайте Claude что-нибудь сделать.

**1. Выберите окружение и папку**

В [строке под полем ввода промпта](https://code.claude.com/docs/ru/desktop.md#start-a-session) нажмите первый элемент управления — селектор окружения — и выберите верхний пункт в группе **Local**. Затем нажмите элемент управления папкой проекта рядом с селектором окружения, выберите **Open folder…** и укажите директорию вашего проекта.

Если в новой сессии под полем ввода промпта не отображается окружение, у вас более ранняя версия интерфейса. См. [Проверьте, какая у вас версия интерфейса](https://code.claude.com/docs/ru/desktop.md#check-which-layout-you-have).

> [!TIP]
>
> Начните с небольшого проекта, который вы хорошо знаете. Это самый быстрый способ увидеть, что может делать Claude Code.

Вы также можете выбрать:

* **Cloud**: Запускайте сеансы в облаке, которые продолжают работу даже если вы закроете приложение. См. [Use Claude Code in the cloud](https://code.claude.com/docs/ru/claude-code-on-the-web.md) для информации о том, как работают облачные сеансы.
* **SSH**: Подключитесь к удаленной машине через SSH, например к вашим собственным серверам, облачным виртуальным машинам или контейнерам разработки. Сначала [добавьте подключение](https://code.claude.com/docs/ru/desktop.md#ssh-sessions). Desktop автоматически устанавливает Claude Code на удаленную машину при первом подключении. Выполняющаяся задача может [продолжать работу, пока Desktop отключен](https://code.claude.com/docs/ru/desktop.md#keep-a-task-running-while-desktop-is-disconnected), но при использовании аккаунта Claude она может остановиться, когда истечет срок ее входа в систему.
* **WSL** (Windows): Запустите сессию внутри [WSL 2 дистрибутива](https://code.claude.com/docs/ru/desktop-wsl.md); Claude Code, инструменты и git выполняются на стороне Linux с собственными путями.

**2. Выберите модель**

Выберите модель в селекторе моделей ближе к правому краю строки под полем ввода промпта. См. [models](https://code.claude.com/docs/ru/model-config.md#available-models) для сравнения доступных моделей. Вы можете изменить модель позже в селекторе моделей.

**3. Скажите Claude, что делать**

Введите, что вы хотите, чтобы Claude сделал:

* `Find a TODO comment and fix it`
* `Add tests for the main function`
* `Create a CLAUDE.md with instructions for this codebase`

[Сессия](https://code.claude.com/docs/ru/desktop.md#work-in-parallel-with-sessions) — это диалог с Claude о вашем коде. Каждая сессия отслеживает свой собственный контекст и изменения.

**4. Проверьте и примите изменения**

Проверьте ваш [режим разрешений](https://code.claude.com/docs/ru/desktop.md#choose-a-permission-mode) в строке под полем ввода промпта, чтобы узнать, ждет ли Claude вашего подтверждения:

* **Auto или Accept edits**: Claude применяет изменения файлов, и появляется индикатор, такой как `+12 -1`, чтобы вы могли просмотреть их в [представлении diff](https://code.claude.com/docs/ru/desktop.md#review-changes-with-diff-view)
* **Manual**: Claude предлагает каждое изменение и ждет вашего подтверждения перед его применением

В режиме Manual вы увидите:

1. Diff, показывающий точно, что изменится
2. Кнопки для подтверждения или отклонения каждого изменения
3. Обновления в реальном времени по мере того, как Claude работает над вашим запросом

## Что дальше?

Вы сделали первое редактирование. Полный справочник по всем возможностям Desktop см. в разделе [Use Claude Code Desktop](https://code.claude.com/docs/ru/desktop.md). Вот несколько вещей, которые стоит попробовать дальше.

**Прерывание и управление.** Вы можете перенаправить Claude в любой момент. Нажмите кнопку остановки, чтобы прервать немедленно, или введите исправление и нажмите **Enter**, чтобы отправить его без остановки выполняемого действия. В любом случае вам не нужно ждать завершения или начинать заново.

**Предоставьте Claude больше контекста.** Введите `@filename` в поле промпта, чтобы добавить конкретный файл в диалог. Чем больше контекста у Claude, тем лучше результаты. См. [Add files and context](https://code.claude.com/docs/ru/desktop.md#add-files-and-context-to-prompts).

**Используйте skills для повторяющихся задач.** Введите `/` или нажмите **+** → **Slash commands**, чтобы просмотреть [built-in commands](https://code.claude.com/docs/ru/commands.md), [custom skills](https://code.claude.com/docs/ru/skills.md) и skills плагинов. Skills — это многократно используемые подсказки, которые вы можете вызывать всякий раз, когда они вам нужны, например контрольные списки проверки кода или этапы развертывания.

**Проверьте изменения перед фиксацией.** После редактирования файлов Claude появляется индикатор `+12 -1`. Нажмите на него, чтобы открыть [diff view](https://code.claude.com/docs/ru/desktop.md#review-changes-with-diff-view), просмотрите изменения файл за файлом и оставляйте комментарии к конкретным строкам. Claude читает ваши комментарии и вносит исправления. Чтобы Claude сам проверил изменения, введите [`/code-review`](https://code.claude.com/docs/ru/desktop#review-your-code) в поле промпта.

**Отрегулируйте объем контроля.** Ваш [permission mode](https://code.claude.com/docs/ru/desktop.md#choose-a-permission-mode) определяет, сколько Claude может делать без запроса одобрения:

* **Auto**: классификатор проверяет действия в фоновом режиме и блокирует рискованные вместо того, чтобы просить вас.
* **Manual**: Claude запрашивает разрешение перед редактированием файлов или запуском команд.
* **Accept edits**: Claude автоматически принимает редактирование файлов для более быстрой итерации.
* **Plan**: Claude предлагает подход без редактирования каких-либо файлов, что полезно перед крупным рефакторингом.

**Добавьте плагины для дополнительных возможностей.** Установите [плагины](https://code.claude.com/docs/ru/desktop.md#install-plugins), которые добавляют скиллы, агентов, MCP-серверы и многое другое.

**Организуйте рабочее пространство.** Перетащите панели чата, diff, терминала, файла и браузера в любой нужный вам макет. Откройте терминал с помощью **Ctrl+\`**, чтобы запускать команды параллельно с вашей сессией, или нажмите на путь файла, чтобы открыть его. См. [Arrange your workspace](https://code.claude.com/docs/ru/desktop.md#arrange-your-workspace).

**Предпросмотр вашего приложения.** Когда вы запускаете сервер разработки на рабочем столе, ваше приложение открывается в панели Browser, которая также может [открывать внешние сайты](https://code.claude.com/docs/ru/desktop.md#browse-external-sites). Claude может просматривать работающее приложение, тестировать конечные точки, проверять журналы и повторять итерации на основе того, что он видит. См. [Preview your app](https://code.claude.com/docs/ru/desktop.md#preview-your-app).

**Отслеживайте ваш pull request.** После открытия PR Claude Code отслеживает результаты проверок CI и может автоматически исправлять сбои. См. [Monitor pull request status](https://code.claude.com/docs/ru/desktop.md#monitor-pull-request-status).

**Поставьте Claude по расписанию.** Установите [scheduled tasks](https://code.claude.com/docs/ru/desktop-scheduled-tasks.md) для автоматического запуска Claude на регулярной основе: ежедневная проверка кода каждое утро, еженедельный аудит зависимостей или брифинг, который извлекает данные из ваших подключенных инструментов.

**Масштабируйте, когда будете готовы.** Откройте [параллельные сессии](https://code.claude.com/docs/ru/desktop.md#work-in-parallel-with-sessions) на боковой панели, чтобы работать над несколькими задачами одновременно, при желании каждая в своем Git worktree, и откройте [панель задач](https://code.claude.com/docs/ru/desktop.md#watch-background-tasks), чтобы наблюдать за субагентами и фоновыми командами, которые запускает сессия. Откройте [боковой чат](https://code.claude.com/docs/ru/desktop.md#ask-a-side-question-without-derailing-the-session), чтобы задать вопрос без отвлечения основного потока. Отправьте [долгие задачи в облако](https://code.claude.com/docs/ru/desktop.md#run-long-running-tasks-in-the-cloud), чтобы работа продолжалась, даже если вы закроете приложение, или [перенесите уже начатую сессию в облако](https://code.claude.com/docs/ru/desktop.md#continue-in-another-surface), если задача займет больше времени, чем ожидалось. [Подключите внешние инструменты](https://code.claude.com/docs/ru/desktop.md#extend-claude-code), такие как GitHub, Slack и Linear, чтобы объединить ваш рабочий процесс.

## Что дальше

* [Используйте Claude Code Desktop](https://code.claude.com/docs/ru/desktop.md): режимы разрешений, параллельные сеансы, представление различий, соединители и конфигурация для предприятий
* [Переходите с CLI?](https://code.claude.com/docs/ru/desktop.md#coming-from-the-cli): запустите Desktop и CLI в одном проекте и сравните функции, эквиваленты флагов и то, что недоступно в Desktop
* [Troubleshooting](https://code.claude.com/docs/ru/desktop.md#troubleshooting): решения распространённых ошибок и проблем с настройкой
* [Best practices](https://code.claude.com/docs/ru/best-practices.md): советы по написанию эффективных подсказок и максимальному использованию Claude Code
* [Common workflows](https://code.claude.com/docs/ru/common-workflows.md): учебные материалы по отладке, рефакторингу, тестированию и многому другому
