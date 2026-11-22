> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор

> Claude Code — это агентский инструмент кодирования, который читает вашу кодовую базу, редактирует файлы, выполняет команды и интегрируется с вашими инструментами разработки. Доступен в вашем терминале, IDE, приложении для рабочего стола и браузере.

Claude Code — это AI-помощник по кодированию, который помогает вам создавать функции, исправлять ошибки и автоматизировать задачи разработки. Он понимает всю вашу кодовую базу и может работать с несколькими файлами и инструментами для выполнения задач.

## Начало работы

Claude Code работает на нескольких платформах: в терминале, расширениях IDE, настольном приложении и в веб-версии. Выберите одну из вкладок ниже, чтобы начать. Большинство платформ требуют [подписку Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) или учетную запись [Anthropic Console](https://platform.claude.com/). Terminal CLI, VS Code и JetBrains также поддерживают [сторонних поставщиков](https://code.claude.com/docs/ru/third-party-integrations.md).

> [tab] Terminal
>
> Полнофункциональный CLI для работы с Claude Code прямо в вашем терминале. Редактируйте файлы, выполняйте команды и управляйте всем проектом из командной строки.
>
> Для установки Claude Code откройте терминал и выполните команду для вашей системы. Если вы раньше не использовали терминал, [руководство по терминалу](https://code.claude.com/docs/ru/terminal-guide) показывает, как его открыть и вставить команду.
>
> > [tab] Встроенная установка (рекомендуется)
> >
> > **macOS, Linux, WSL:**
> >
> > ```bash theme={null}
> > curl -fsSL https://claude.ai/install.sh | bash
> > ```
> >
> > В Windows приглашение командной строки показывает `PS C:\`, когда вы находитесь в PowerShell, и `C:\` без `PS`, когда вы находитесь в CMD.
> >
> > **Windows PowerShell:**
> >
> > ```powershell theme={null}
> > irm https://claude.ai/install.ps1 | iex
> > ```
> >
> > **Windows CMD:**
> >
> > ```batch theme={null}
> > curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
> > ```
> >
> > Команда установки не показывает прогресс во время загрузки Claude Code. Когда установщик завершит работу, откройте новое окно терминала и выполните `claude --version`. Работающая установка выводит номер версии. Если ваша оболочка говорит, что `claude` не найден или не распознан, каталог установки еще не находится в вашем PATH: см. [Исправьте ваш PATH](https://code.claude.com/docs/ru/troubleshoot-install.md#command-not-found-claude-after-installation).
> >
> > Если вы видите `The token '&&' is not a valid statement separator`, вы находитесь в PowerShell, а не в CMD. Если вы видите `'irm' is not recognized as an internal or external command`, вы находитесь в CMD, а не в PowerShell.
> >
> > Если команда установки завершается с ошибкой `syntax error near unexpected token '<'`, `403` или любой другой ошибкой, см. [Устранение неполадок при установке](https://code.claude.com/docs/ru/troubleshoot-install.md#find-your-error), чтобы сопоставить ошибку с исправлением и для альтернативных методов установки.
> >
> > [Git for Windows](https://git-scm.com/downloads/win) рекомендуется на встроенной Windows, чтобы Claude Code мог использовать инструмент Bash. Если Git for Windows не установлен, Claude Code использует PowerShell в качестве инструмента оболочки. Установки WSL не требуют Git for Windows.
> >
> > > [!NOTE]
> > >
> > > Встроенные установки автоматически обновляются в фоновом режиме, чтобы вы всегда использовали последнюю версию.
>
> > [tab] Homebrew
> >
> > ```bash theme={null}
> > brew install --cask claude-code
> > ```
> >
> > Homebrew предлагает два пакета. `claude-code` отслеживает канал стабильного выпуска, который обычно отстает примерно на неделю и пропускает выпуски с серьезными регрессиями. `claude-code@latest` отслеживает последний канал и получает новые версии сразу после их выпуска.
> >
> > > [!NOTE]
> > >
> > > Установки Homebrew не обновляются автоматически. Запустите `brew upgrade claude-code` или `brew upgrade claude-code@latest`, в зависимости от того, какой пакет вы установили, чтобы получить последние функции и исправления безопасности.
>
> > [tab] WinGet
> >
> > ```powershell theme={null}
> > winget install Anthropic.ClaudeCode
> > ```
> >
> > > [!NOTE]
> > >
> > > Установки WinGet не обновляются автоматически. Периодически запускайте `winget upgrade Anthropic.ClaudeCode` чтобы получить последние функции и исправления безопасности.
>
> Вы также можете установить с помощью [apt, dnf или apk](https://code.claude.com/docs/ru/setup.md#install-with-linux-package-managers) на Debian, Fedora, RHEL и Alpine.
>
> Затем запустите Claude Code в любом проекте. Замените `your-project` на путь к каталогу проекта на вашей машине:
>
> ```bash theme={null}
> cd your-project
> claude
> ```
>
> При первом использовании Claude Code предложит вам войти. Если вы установили переменную окружения `ANTHROPIC_API_KEY` и одобрите ключ, когда Claude Code спросит, использовать ли его, Claude Code пропустит запрос на вход. [Перейти к быстрому старту →](https://code.claude.com/docs/ru/quickstart.md)
>
> > [!TIP]
> >
> > Смотрите [расширенную настройку](https://code.claude.com/docs/ru/setup.md) для опций установки, ручных обновлений или инструкций по удалению. Посетите [troubleshooting установки](https://code.claude.com/docs/ru/troubleshoot-install.md), если у вас возникли проблемы.

> [tab] VS Code
>
> Расширение VS Code предоставляет встроенные различия, @-упоминания, просмотр плана и историю разговоров прямо в вашем редакторе.
>
> * [Установить для VS Code](vscode:extension/anthropic.claude-code)
> * [Установить для Cursor](cursor:extension/anthropic.claude-code)
>
> Или найдите "Claude Code" в представлении Extensions (`Cmd+Shift+X` на Mac, `Ctrl+Shift+X` на Windows/Linux). После установки откройте Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), введите "Claude Code" и выберите **Open in New Tab**.
>
> [Начните работу с VS Code →](https://code.claude.com/docs/ru/vs-code.md#get-started)

> [tab] Desktop app
>
> Автономное приложение для запуска Claude Code вне вашей IDE или терминала. Просматривайте различия визуально, запускайте несколько сеансов рядом, планируйте повторяющиеся задачи и запускайте облачные сеансы.
>
> Загрузите и установите:
>
> * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel и Apple Silicon)
> * [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
> * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)
> * На Ubuntu или Debian, где приложение находится в бета-версии, установите его с помощью apt, следуя [инструкциям по установке Linux](https://code.claude.com/docs/ru/desktop-linux.md)
>
> После установки запустите Claude, войдите и нажмите вкладку **Code** для начала кодирования. Приложение включает Claude Code, поэтому вам не нужно устанавливать CLI отдельно. Требуется [платная подписка](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing).
>
> [Узнайте больше о приложении для рабочего стола →](https://code.claude.com/docs/ru/desktop-quickstart.md)

> [tab] Web
>
> Запустите Claude Code в вашем браузере без локальной настройки. Запускайте долгоживущие задачи и возвращайтесь, когда они будут готовы, работайте с репозиториями, которые у вас нет локально, или запускайте несколько задач параллельно. Для более длительной работы создайте [проект](https://code.claude.com/docs/ru/claude-projects.md) и позвольте Claude координировать параллельные сеансы для вас. Доступно на настольных браузерах и [приложении Claude для iOS и Android](https://code.claude.com/docs/ru/mobile.md).
>
> Начните кодирование на [claude.ai/code](https://claude.ai/code).
>
> [Начните работу →](https://code.claude.com/docs/ru/web-quickstart.md)

> [tab] JetBrains
>
> Плагин для IntelliJ IDEA, PyCharm, WebStorm и других IDE JetBrains с интерактивным просмотром различий и совместным использованием контекста выделения.
>
> Установите [плагин Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) из JetBrains Marketplace и перезагрузите вашу IDE. Плагин требует Claude Code CLI, установленный отдельно; см. [шаги настройки JetBrains](https://code.claude.com/docs/ru/jetbrains.md#installation).
>
> [Начните работу с JetBrains →](https://code.claude.com/docs/ru/jetbrains.md)

## Что вы можете делать

Вот некоторые способы использования Claude Code:

> [accordion] Автоматизируйте работу, которую вы постоянно откладываете
>
> Claude Code справляется с утомительными задачами, которые съедают ваш день: написание тестов для непроверенного кода, исправление ошибок lint по всему проекту, разрешение конфликтов слияния, обновление зависимостей и написание заметок о выпуске.
>
> ```bash theme={null}
> claude "write tests for the auth module, run them, and fix any failures"
> ```

> [accordion] Создавайте функции и исправляйте ошибки
>
> Опишите то, что вы хотите, на простом языке. Claude Code планирует подход, пишет код в нескольких файлах и проверяет, что он работает.
>
> Для ошибок вставьте сообщение об ошибке или опишите симптом. Claude Code отслеживает проблему через вашу кодовую базу, определяет основную причину и реализует исправление. Смотрите [common workflows](https://code.claude.com/docs/ru/common-workflows.md) для получения дополнительных примеров.

> [accordion] Создавайте коммиты и pull requests
>
> Claude Code работает непосредственно с git. Он подготавливает изменения, пишет сообщения коммитов, создает ветки и открывает pull requests.
>
> ```bash theme={null}
> claude "commit my changes with a descriptive message"
> ```
>
> В CI вы можете автоматизировать код-ревью и сортировку проблем с помощью [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) или [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md).

> [accordion] Подключите свои инструменты с помощью MCP
>
> [Model Context Protocol (MCP)](https://code.claude.com/docs/ru/mcp.md) — это открытый стандарт для подключения инструментов AI к внешним источникам данных. С помощью MCP Claude Code может читать ваши документы дизайна в Google Drive, обновлять задачи в Jira, извлекать данные из Slack или использовать ваши собственные пользовательские инструменты. [Быстрый старт MCP](https://code.claude.com/docs/ru/mcp-quickstart.md) подключает ваш первый сервер от начала до конца.

> [accordion] Настройте с помощью инструкций, скиллов и хуков
>
> [`CLAUDE.md`](https://code.claude.com/docs/ru/memory) — это файл markdown, который вы добавляете в корень вашего проекта, и Claude Code читает его в начале каждой сессии. Используйте его для установки стандартов кодирования, архитектурных решений, предпочитаемых библиотек и контрольных списков проверки. Если в вашем репозитории уже есть `AGENTS.md` для других агентов кодирования, Claude Code [может читать его](https://code.claude.com/docs/ru/memory.md#agents-md) вместо `CLAUDE.md`. Claude также создает [автоматическую память](https://code.claude.com/docs/ru/memory.md#auto-memory) по мере работы, сохраняя знания между сессиями без необходимости что-либо писать.
>
> Создавайте [skills](https://code.claude.com/docs/ru/skills.md) для упаковки повторяемых рабочих процессов, которые ваша команда может использовать, например `/review-pr` или `/deploy-staging`.
>
> [Hooks](https://code.claude.com/docs/ru/hooks.md) позволяют вам запускать команды shell до или после действий Claude Code, например автоматическое форматирование после каждого редактирования файла или запуск lint перед коммитом.

> [accordion] Запустите агентов параллельно и создавайте пользовательских агентов
>
> Запустите [несколько агентов Claude Code](https://code.claude.com/docs/ru/sub-agents.md), которые работают над разными частями задачи одновременно. Главный агент координирует работу, назначает подзадачи и объединяет результаты.
>
> Для запуска нескольких полных сеансов параллельно и наблюдения за ними с одного экрана используйте [background agents](https://code.claude.com/docs/ru/agent-view.md). Для полностью пользовательских рабочих процессов [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) позволяет вам создавать собственных агентов, работающих на инструментах и возможностях Claude Code, с полным контролем над оркестровкой, доступом к инструментам и разрешениями.

> [accordion] Передавайте, создавайте скрипты и автоматизируйте с помощью CLI
>
> Claude Code является составным и следует философии Unix. Передавайте в него логи, запускайте его в CI или объединяйте его с другими инструментами:
>
> ```bash theme={null}
> # Анализируйте недавний вывод логов
> tail -200 app.log | claude -p "Slack me if you see any anomalies"
>
> # Автоматизируйте переводы в CI
> claude -p "translate new strings into French and raise a PR for review"
>
> # Массовые операции по файлам
> git diff main --name-only | claude -p "review these changed files for security issues"
> ```
>
> Смотрите [CLI reference](https://code.claude.com/docs/ru/cli-reference.md) для полного набора команд и флагов.

> [accordion] Планируйте повторяющиеся задачи
>
> Запускайте Claude по расписанию для автоматизации работы, которая повторяется: утренние проверки PR, анализ сбоев CI в ночное время, еженедельные аудиты зависимостей или синхронизация документов после слияния PR.
>
> * [Облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md), ранее называвшиеся routines, работают в облаке, поэтому они продолжают работать даже когда ваш компьютер выключен. Они также могут срабатывать при вызовах API или событиях GitHub. Создавайте их из веб-версии, приложения Desktop или запустив `/schedule` в CLI.
> * [Запланированные задачи Desktop](https://code.claude.com/docs/ru/desktop-scheduled-tasks.md) работают на вашей машине с прямым доступом к вашим локальным файлам и инструментам
> * [`/loop`](https://code.claude.com/docs/ru/scheduled-tasks) повторяет промпт в сессии CLI для быстрого опроса

> [accordion] Работайте откуда угодно
>
> Сессии не привязаны к одному интерфейсу. Перемещайте работу между ними по мере изменения вашего контекста:
>
> * Отойдите от своего стола и продолжайте работать со своего телефона или любого браузера с помощью [Remote Control](https://code.claude.com/docs/ru/remote-control.md)
> * Отправьте сообщение [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch) с задачей со своего телефона и откройте сеанс Desktop, который он создает
> * Запустите долгоживущую задачу в [веб-версии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) или [приложении Claude для мобильных устройств](https://code.claude.com/docs/ru/mobile.md), затем перенесите ее в свой терминал с помощью `claude --teleport`. Teleport требует подписку claude.ai.
> * Запустите `/desktop` для продолжения вашего текущего сеанса терминала в [приложении Desktop](https://code.claude.com/docs/ru/desktop.md), где вы можете просмотреть различия визуально. Передача `/desktop` требует подписку claude.ai. Доступно на macOS и x64 Windows.
> * Маршрутизируйте задачи из командного чата: упомяните `@Claude` в [Slack](https://code.claude.com/docs/ru/slack.md) с отчетом об ошибке и получите pull request обратно

## Используйте Claude Code везде

Каждая [поверхность](https://code.claude.com/docs/ru/glossary.md#surface) подключается к одному и тому же базовому механизму Claude Code, поэтому ваши файлы CLAUDE.md, параметры и MCP servers работают на всех них.

Помимо сред [Terminal](https://code.claude.com/docs/ru/quickstart.md), [VS Code](https://code.claude.com/docs/ru/vs-code.md), [JetBrains](https://code.claude.com/docs/ru/jetbrains.md), [Desktop](https://code.claude.com/docs/ru/desktop.md) и [Web](https://code.claude.com/docs/ru/claude-code-on-the-web.md) выше, Claude Code интегрируется с CI/CD, чатом и рабочими процессами браузера:

| Что я хочу сделать | Лучший вариант |
| - | - |
| Продолжить локальный сеанс со своего телефона или другого устройства | [Remote Control](https://code.claude.com/docs/ru/remote-control.md) |
| Отправить события из Telegram, Discord, iMessage или моих собственных webhooks в сеанс | [Channels](https://code.claude.com/docs/ru/channels.md) |
| Начать задачу локально, продолжить на мобильном | [`claude --cloud`](https://code.claude.com/docs/ru/claude-code-on-the-web#from-terminal-to-cloud), затем [мобильное приложение Claude](https://code.claude.com/docs/ru/mobile.md) |
| Запускать Claude по регулярному расписанию | [Облачные запланированные задачи](https://code.claude.com/docs/ru/routines.md) или [Запланированные задачи Desktop](https://code.claude.com/docs/ru/desktop-scheduled-tasks.md) |
| Автоматизировать проверки PR и сортировку проблем | [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) или [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md) |
| Получить автоматическую проверку кода на каждый PR | [GitHub Code Review](https://code.claude.com/docs/ru/code-review.md) |
| Маршрутизировать отчеты об ошибках из Slack в pull requests | [Slack](https://code.claude.com/docs/ru/slack.md) |
| Отладить живые веб-приложения | [Chrome](https://code.claude.com/docs/ru/chrome.md) |
| Создавайте пользовательских агентов для ваших собственных рабочих процессов | [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) |

## Следующие шаги

После установки Claude Code эти руководства помогут вам углубиться.

* [Quickstart](https://code.claude.com/docs/ru/quickstart.md): пройдите через вашу первую реальную задачу, от изучения кодовой базы до коммита исправления
* [Сохраняйте инструкции и воспоминания](https://code.claude.com/docs/ru/memory.md): дайте Claude постоянные инструкции с файлами CLAUDE.md и auto memory
* [Common workflows](https://code.claude.com/docs/ru/common-workflows.md) и [best practices](https://code.claude.com/docs/ru/best-practices.md): шаблоны для получения максимума от Claude Code
* [Claude Academy](https://academy.claude.com/): бесплатные самостоятельные курсы, включая [Claude Code 101](https://academy.claude.com/courses/claude-code-101) и [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action)
* [A harness for every task](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code): как команда Claude Code использует [dynamic workflows](https://code.claude.com/docs/ru/workflows.md) для организации подагентов в масштабе
* [Settings](https://code.claude.com/docs/ru/settings.md): настройте Claude Code для вашего рабочего процесса
* [Troubleshooting](https://code.claude.com/docs/ru/troubleshooting.md): решения для распространенных проблем
* [code.claude.com](https://code.claude.com/): демонстрации, цены и детали продукта
