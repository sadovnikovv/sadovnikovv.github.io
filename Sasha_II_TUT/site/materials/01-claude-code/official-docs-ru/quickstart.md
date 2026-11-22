> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Быстрый старт

> Установите Claude Code в терминале, войдите в систему и используйте CLI, чтобы изучить кодовую базу и внести первое изменение в код.

Это руководство по быстрому старту посвящено Claude Code в терминале: установке CLI, входу в систему в первой сессии и использованию инструмента для типичных задач разработки в вашем собственном проекте.

## Перед началом

Убедитесь, что у вас есть:

* Открытый терминал или командная строка
* Проект кода для работы
* [Подписка Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq) (Pro, Max, Ultra, Team или Enterprise), учётная запись [Claude Console](https://platform.claude.com/) или доступ через [поддерживаемого облачного провайдера](https://code.claude.com/docs/ru/third-party-integrations.md)

> [!NOTE]
>
> Эти случаи рассматриваются на других страницах:
>
> * **Вы никогда раньше не использовали терминал**: начните с [руководства по терминалу](https://code.claude.com/docs/ru/terminal-guide)
> * **Вы хотите использовать Claude Code не в терминале**: Claude Code также доступен в [веб-версии](https://claude.ai/code), как [настольное приложение](https://code.claude.com/docs/ru/desktop.md), в [VS Code](https://code.claude.com/docs/ru/vs-code.md) и [JetBrains IDEs](https://code.claude.com/docs/ru/jetbrains.md), в [Slack](https://code.claude.com/docs/ru/slack.md) и в CI/CD с [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) и [GitLab](https://code.claude.com/docs/ru/gitlab-ci-cd.md). Смотрите [все интерфейсы](https://code.claude.com/docs/ru/overview.md#use-claude-code-everywhere).

## Шаг 1: Установите Claude Code

Для установки Claude Code откройте терминал и выполните команду для вашей системы. Если вы раньше не использовали терминал, [руководство по терминалу](https://code.claude.com/docs/ru/terminal-guide) показывает, как его открыть и вставить команду.

> [tab] Встроенная установка (рекомендуется)
>
> **macOS, Linux, WSL:**
>
> ```bash theme={null}
> curl -fsSL https://claude.ai/install.sh | bash
> ```
>
> В Windows приглашение командной строки показывает `PS C:\`, когда вы находитесь в PowerShell, и `C:\` без `PS`, когда вы находитесь в CMD.
>
> **Windows PowerShell:**
>
> ```powershell theme={null}
> irm https://claude.ai/install.ps1 | iex
> ```
>
> **Windows CMD:**
>
> ```batch theme={null}
> curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
> ```
>
> Команда установки не показывает прогресс во время загрузки Claude Code. Когда установщик завершит работу, откройте новое окно терминала и выполните `claude --version`. Работающая установка выводит номер версии. Если ваша оболочка говорит, что `claude` не найден или не распознан, каталог установки еще не находится в вашем PATH: см. [Исправьте ваш PATH](https://code.claude.com/docs/ru/troubleshoot-install.md#command-not-found-claude-after-installation).
>
> Если вы видите `The token '&&' is not a valid statement separator`, вы находитесь в PowerShell, а не в CMD. Если вы видите `'irm' is not recognized as an internal or external command`, вы находитесь в CMD, а не в PowerShell.
>
> Если команда установки завершается с ошибкой `syntax error near unexpected token '<'`, `403` или любой другой ошибкой, см. [Устранение неполадок при установке](https://code.claude.com/docs/ru/troubleshoot-install.md#find-your-error), чтобы сопоставить ошибку с исправлением и для альтернативных методов установки.
>
> [Git for Windows](https://git-scm.com/downloads/win) рекомендуется на встроенной Windows, чтобы Claude Code мог использовать инструмент Bash. Если Git for Windows не установлен, Claude Code использует PowerShell в качестве инструмента оболочки. Установки WSL не требуют Git for Windows.
>
> > [!NOTE]
> >
> > Встроенные установки автоматически обновляются в фоновом режиме, чтобы вы всегда использовали последнюю версию.

> [tab] Homebrew
>
> ```bash theme={null}
> brew install --cask claude-code
> ```
>
> Homebrew предлагает два пакета. `claude-code` отслеживает канал стабильного выпуска, который обычно отстает примерно на неделю и пропускает выпуски с серьезными регрессиями. `claude-code@latest` отслеживает последний канал и получает новые версии сразу после их выпуска.
>
> > [!NOTE]
> >
> > Установки Homebrew не обновляются автоматически. Запустите `brew upgrade claude-code` или `brew upgrade claude-code@latest`, в зависимости от того, какой пакет вы установили, чтобы получить последние функции и исправления безопасности.

> [tab] WinGet
>
> ```powershell theme={null}
> winget install Anthropic.ClaudeCode
> ```
>
> > [!NOTE]
> >
> > Установки WinGet не обновляются автоматически. Периодически запускайте `winget upgrade Anthropic.ClaudeCode` чтобы получить последние функции и исправления безопасности.

Вы также можете установить с помощью [apt, dnf или apk](https://code.claude.com/docs/ru/setup.md#install-with-linux-package-managers) на Debian, Fedora, RHEL и Alpine.

Чтобы подтвердить, что установка прошла успешно, выполните:

```bash theme={null}
claude --version
```

Команда выводит номер версии, за которым следует `(Claude Code)`.

## Шаг 2: Начните свою первую сессию

Откройте терминал в любом каталоге проекта и запустите Claude Code:

```bash theme={null}
cd /path/to/your/project
claude
```

Замените `/path/to/your/project` на путь к проекту, над которым вы хотите работать.

При первом использовании Claude Code предложит вам войти в систему. Для подписки Claude или учётных записей Console следуйте инструкциям, чтобы завершить аутентификацию в браузере. Если вы задали переменную окружения `ANTHROPIC_API_KEY` и подтвердили использование ключа, когда Claude Code спросит об этом, Claude Code пропустит запрос на вход.

Вы можете войти, используя любой из следующих типов учётных записей:

* [Claude Pro, Max, Ultra, Team или Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login) (рекомендуется)
* [Claude Console](https://platform.claude.com/) (доступ к API с предоплаченными кредитами). При первом входе в Console автоматически создаётся рабочее пространство «Claude Code» для централизованного отслеживания расходов.
* [Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry](https://code.claude.com/docs/ru/third-party-integrations.md) (корпоративные облачные провайдеры)
* Самостоятельно размещённый [шлюз приложений Claude](https://code.claude.com/docs/ru/claude-apps-gateway), если ваша организация его использует: администратор заранее настраивает URL шлюза, и `/login` сразу открывается на экране **Cloud gateway**, где вы можете войти с помощью корпоративного SSO

После входа ваши учётные данные сохраняются, и вам не придётся входить повторно. Подробнее читайте в разделе [Управление учётными данными](https://code.claude.com/docs/ru/authentication.md#credential-management).

Появится промпт Claude Code, над которым отображаются версия, текущая модель и рабочий каталог. Введите `/help`, чтобы увидеть доступные команды, или `/resume`, чтобы продолжить предыдущий диалог. Чтобы позже сменить учётную запись или пройти аутентификацию повторно, введите `/login` внутри запущенной сессии.

## Шаг 3: Задайте свой первый вопрос

Попробуйте одну из этих команд:

```text wrap theme={null}
what does this project do?
```

Claude проанализирует ваши файлы и предоставит краткое описание. Вы также можете задавать более конкретные вопросы:

```text wrap theme={null}
what technologies does this project use?
```

```text wrap theme={null}
where is the main entry point?
```

```text wrap theme={null}
explain the folder structure
```

Вы также можете спросить Claude о его собственных возможностях:

```text wrap theme={null}
what can Claude Code do?
```

```text wrap theme={null}
how do I create custom skills in Claude Code?
```

```text wrap theme={null}
can Claude Code work with Docker?
```

> [!NOTE]
>
> Claude Code читает файлы вашего проекта по мере необходимости. Вам не нужно вручную добавлять контекст.

## Шаг 4: Внесите первое изменение в код

Попробуйте выполнить небольшую задачу:

```text wrap theme={null}
add a hello world function to the main file
```

Claude Code найдёт подходящий файл и покажет вам изменение. Если он запросит подтверждение перед внесением изменения, выберите **Yes**, чтобы одобрить его.

[Режим разрешений](https://code.claude.com/docs/ru/permission-modes.md) сессии определяет, какие действия Claude может выполнять, не спрашивая вас заранее. Нажмите `Shift+Tab` в любой момент, чтобы переключить режим разрешений текущей сессии.

## Шаг 5: Используйте Git с Claude Code

Claude Code превращает операции Git в диалог:

```text wrap theme={null}
what files have I changed?
```

```text wrap theme={null}
commit my changes with a descriptive message
```

Вы также можете использовать промпты для более сложных операций Git:

```text wrap theme={null}
create a new branch called feature/quickstart
```

```text wrap theme={null}
show me the last 5 commits
```

```text wrap theme={null}
help me resolve merge conflicts
```

## Шаг 6: Исправьте ошибку или добавьте функцию

Опишите, что вы хотите, на естественном языке:

```text wrap theme={null}
add input validation to the user registration form
```

Или исправьте существующие проблемы:

```text wrap theme={null}
there's a bug where users can submit empty forms - fix it
```

## Шаг 7: Попробуйте другие распространённые рабочие процессы

Попробуйте ещё несколько промптов. Вы можете попросить Claude выполнить рефакторинг кода, написать тесты, обновить документацию или проверить ваши изменения:

```text wrap theme={null}
refactor the authentication module to use async/await instead of callbacks
```

```text wrap theme={null}
write unit tests for the calculator functions
```

```text wrap theme={null}
update the README with installation instructions
```

```text wrap theme={null}
review my changes and suggest improvements
```

> [!TIP]
>
> Общайтесь с Claude так же, как с отзывчивым коллегой. Опишите, чего вы хотите достичь, и Claude поможет вам в этом.

## Основные команды

Вот наиболее важные команды для ежедневного использования, сгруппированные по месту их запуска.

### Команды оболочки

Запускайте их из вашего терминала, чтобы запустить или возобновить Claude Code.

| Команда | Что она делает | Пример |
| - | - | - |
| `claude` | Запустить интерактивный режим | `claude` |
| `claude "task"` | Запустить интерактивный режим с начальным приглашением | `claude "fix the build error"` |
| `claude -p "query"` | Запустить одноразовый запрос, затем выйти | `claude -p "explain this function"` |
| `claude -c` | Продолжить самый последний разговор в текущем каталоге | `claude -c` |
| `claude -r` | Возобновить предыдущий разговор | `claude -r` |

Смотрите [справочник CLI](https://code.claude.com/docs/ru/cli-reference.md) для полного списка команд оболочки.

### Команды сессии

Запускайте их внутри Claude Code после его запуска.

| Команда | Что она делает | Пример |
| - | - | - |
| `/clear` | Начать новый диалог. Вернуться к предыдущему можно с помощью `/resume`. | `/clear` |
| `/help` | Показать доступные команды | `/help` |
| `/exit` или Ctrl+D дважды | Выйти из Claude Code | `/exit` |

Смотрите [справочник команд](https://code.claude.com/docs/ru/commands.md) для полного списка команд сессии.

## Советы для начинающих

Для большего, смотрите [лучшие практики](https://code.claude.com/docs/ru/best-practices.md) и [типичные рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md).

> [accordion] Будьте конкретны в своих запросах
>
> Вместо: "исправить ошибку"
>
> Попробуйте: "исправить ошибку входа, когда пользователи видят пустой экран после ввода неправильных учетных данных"

> [accordion] Используйте пошаговые инструкции
>
> Разбейте сложные задачи на этапы:
>
> ```text wrap theme={null}
> 1. создать новую таблицу базы данных для профилей пользователей
> 2. создать конечную точку API для получения и обновления профилей пользователей
> 3. создать веб-страницу, которая позволяет пользователям просматривать и редактировать свою информацию
> ```

> [accordion] Позвольте Claude сначала исследовать
>
> Перед внесением изменений позвольте Claude понять ваш код:
>
> ```text wrap theme={null}
> проанализировать схему базы данных
> ```
>
> ```text wrap theme={null}
> создать панель управления, показывающую продукты, которые чаще всего возвращаются нашими клиентами из Великобритании
> ```

> [accordion] Сэкономьте время с помощью ярлыков
>
> * Введите `/` для просмотра всех команд и skills
> * Используйте Tab для завершения команды
> * Нажмите ↑ для истории команд
> * Нажмите `Shift+Tab` для переключения режимов разрешений

## Что дальше?

Теперь, когда вы изучили основы, исследуйте более продвинутые функции:

* [Как работает Claude Code](https://code.claude.com/docs/ru/how-claude-code-works.md): поймите агентный цикл, встроенные инструменты и то, как Claude Code взаимодействует с вашим проектом
* [Лучшие практики](https://code.claude.com/docs/ru/best-practices.md): получайте лучшие результаты с эффективными запросами и настройкой проекта
* [Типичные рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md): пошаговые руководства для типичных задач
* [Расширьте Claude Code](https://code.claude.com/docs/ru/features-overview.md): настройте с помощью CLAUDE.md, скиллов, хуков, MCP и многого другого

См. [расширенную настройку](https://code.claude.com/docs/ru/setup.md), чтобы узнать о вариантах установки, ручном обновлении или инструкциях по удалению.

## Получение помощи

* **В Claude Code**: Введите `/help` или спросите "how do I" вопрос
* **Документация**: Просмотрите другие руководства на этом сайте
* **Курсы**: Пройдите [Claude Code 101](https://academy.claude.com/courses/claude-code-101) и другие бесплатные самостоятельные курсы на [Claude Academy](https://academy.claude.com/)
* **Сообщество**: Присоединитесь к [серверу Discord](https://www.anthropic.com/discord) для советов и поддержки
