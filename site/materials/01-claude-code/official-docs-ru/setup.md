> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Расширенная настройка

> Системные требования, установка для конкретной платформы, управление версиями и удаление Claude Code.

На этой странице рассматриваются системные требования, детали установки для конкретной платформы, обновления и удаление. Для пошагового руководства по вашему первому сеансу см. [краткое руководство](https://code.claude.com/docs/ru/quickstart.md). Если вы никогда раньше не использовали терминал, см. [руководство по терминалу](https://code.claude.com/docs/ru/terminal-guide).

## Системные требования

Claude Code работает на следующих платформах и конфигурациях:

* **Операционная система**:
  * macOS 13.0+
  * Windows 10 1809+ или Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Оборудование**: 4 ГБ+ ОЗУ, процессор x64 или ARM64
* **Сеть**: требуется подключение в Интернет. См. [конфигурация сети](https://code.claude.com/docs/ru/network-config.md#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell или CMD.
* **Местоположение**: [поддерживаемые Anthropic страны](https://www.anthropic.com/supported-countries)

### Дополнительные зависимости

* **ripgrep**: обычно включен в Claude Code. Если поиск не работает, см. [устранение неполадок поиска](https://code.claude.com/docs/ru/troubleshooting.md#search-and-discovery-issues).
* **Git**: необязательно. Если git установлен, для [`claude plugin eval`](https://code.claude.com/docs/ru/plugin-evals#requirements) требуется версия 2.31 или новее. Для [загрузки локального репозитория в облачную сессию](https://code.claude.com/docs/ru/claude-code-on-the-web.md#send-local-repositories-without-github) из macOS, Linux или WSL требуется git 2.31 или новее. Выполните `git --version`, чтобы узнать вашу версию.

## Установка Claude Code

> [!TIP]
>
> Предпочитаете графический интерфейс? [Приложение Desktop](https://code.claude.com/docs/ru/desktop-quickstart.md) позволяет использовать Claude Code без терминала. Загрузите его для [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs), [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs) или [Linux](https://code.claude.com/docs/ru/desktop-linux.md).

Для установки Claude Code откройте терминал и выполните команду для вашей системы. Если вы раньше не использовали терминал, [руководство по терминалу](https://code.claude.com/docs/ru/terminal-guide) показывает, как его открыть и вставить команду.

> [tab] Встроенная установка (рекомендуется)
>
> **macOS, Linux, WSL:**
>
> ```bash theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null}
> curl -fsSL https://claude.ai/install.sh | bash
> ```
>
> В Windows приглашение командной строки показывает `PS C:\`, когда вы находитесь в PowerShell, и `C:\` без `PS`, когда вы находитесь в CMD.
>
> **Windows PowerShell:**
>
> ```powershell theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null}
> irm https://claude.ai/install.ps1 | iex
> ```
>
> **Windows CMD:**
>
> ```batch theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null}
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
> ```bash theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null}
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
> ```powershell theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null} theme={null}
> winget install Anthropic.ClaudeCode
> ```
>
> > [!NOTE]
> >
> > Установки WinGet не обновляются автоматически. Периодически запускайте `winget upgrade Anthropic.ClaudeCode` чтобы получить последние функции и исправления безопасности.

Вы также можете установить с помощью [apt, dnf или apk](https://code.claude.com/docs/ru/setup.md#install-with-linux-package-managers) на Debian, Fedora, RHEL и Alpine.

После завершения установки откройте терминал в проекте, над которым вы хотите работать, и запустите Claude Code:

```bash theme={null}
claude
```

Claude Code открывает интерактивный сеанс в вашем терминале.

Если вы столкнулись с какими-либо проблемами во время установки, см. [Устранение неполадок при установке и входе](https://code.claude.com/docs/ru/troubleshoot-install.md).

### Настройка в Windows

Вы можете запустить Claude Code изначально в Windows или внутри WSL. Выберите в зависимости от того, где находятся ваши проекты и какие функции вам нужны:

| Опция | Требует | [Sandboxing](https://code.claude.com/docs/ru/sandboxing.md) | Когда использовать |
| - | - | - | - |
| [Native Windows](#install-on-native-windows) | Нет; [Git for Windows](https://git-scm.com/downloads/win) опционально | Не поддерживается | Встроенные проекты и инструменты Windows |
| [WSL 2](#install-in-wsl) | WSL 2 включен | Поддерживается | Цепочки инструментов Linux или изолированное выполнение команд |
| [WSL 1](#install-in-wsl) | WSL 1 включен | Не поддерживается | Если WSL 2 недоступен |

#### Установка в нативной Windows

Выполните [команду установки](#install-claude-code) из PowerShell или CMD. Вам не нужно запускать от имени администратора. Установка [Git for Windows](https://git-scm.com/downloads/win) опциональна. Она предоставляет Git Bash, который нужен [инструменту Bash](https://code.claude.com/docs/ru/tools-reference.md#bash-tool-behavior) и [инструменту Monitor](https://code.claude.com/docs/ru/tools-reference.md#monitor-tool).

Независимо от того, устанавливаете ли вы из PowerShell или CMD, это влияет только на то, какую команду установки вы выполняете. Ваша подсказка показывает `PS C:\Users\YourName>` в PowerShell и `C:\Users\YourName>` без `PS` в CMD. Если вы новичок в терминале, [руководство по терминалу](https://code.claude.com/docs/ru/terminal-guide#windows) проходит через каждый шаг.

После установки запустите `claude` из любого терминала.

* **Без Git for Windows**, Claude Code запускает команды оболочки через [инструмент PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool).
* **С Git for Windows**, Claude Code использует Git Bash для [инструмента Bash](https://code.claude.com/docs/ru/tools-reference.md#bash-tool-behavior). Если Claude Code не может найти Git Bash, установите путь в вашем [файле settings.json](https://code.claude.com/docs/ru/settings.md):

  ```json theme={null}
  {
    "env": {
      "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
    }
  }
  ```

Когда установлен Git for Windows, инструмент PowerShell доступен наряду с Bash: включен по умолчанию для учетных записей claude.ai и Console, и включен с помощью `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` в сеансах Amazon Bedrock, Google Cloud's Agent Platform и Microsoft Foundry. Установите его на `0`, чтобы отключить инструмент. См. [инструмент PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool) для настройки и ограничений.

#### Установка в WSL

Откройте ваш дистрибутив WSL и выполните установщик Linux из [инструкций установки](#install-claude-code). Вы устанавливаете и запускаете `claude` внутри терминала WSL, а не из PowerShell или CMD.

### Alpine Linux и дистрибутивы на основе musl

На Alpine и других дистрибутивах на основе musl [команда установки](#install-claude-code) требует `bash` и `curl`, а самому Claude Code требуется `bash` или `zsh`. Alpine не включает `bash` или `curl` по умолчанию, поэтому документированная команда установки завершается ошибкой `not found`, пока вы их не установите.

Этот пример устанавливает необходимые пакеты на Alpine:

```bash theme={null}
apk add bash curl
```

## Проверка установки

После установки убедитесь, что Claude Code работает:

```bash theme={null}
claude --version
```

Успешная установка выводит номер версии, например `2.1.211 (Claude Code)`.

Если это не сработает с ошибкой `command not found` или другой ошибкой, см. [Устранение неполадок при установке и входе](https://code.claude.com/docs/ru/troubleshoot-install.md).

Для более подробной проверки установки и конфигурации выполните [`claude doctor`](https://code.claude.com/docs/ru/troubleshooting#get-more-help):

```bash theme={null}
claude doctor
```

`claude doctor` выводит диагностику установки и параметров только для чтения без запуска сеанса, включая проверку здоровья установки, ошибки валидации файла параметров и любые предупреждения с предложенными исправлениями.

## Аутентификация

Claude Code требует учетную запись Pro, Max, Ultra, Team, Enterprise или Console. Бесплатный план claude.ai не включает доступ к Claude Code. Вы также можете использовать Claude Code с поставщиком API третьей стороны, таким как [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md) или [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md).

После установки войдите, выполнив `claude` и следуя инструкциям в браузере. Если вы установили переменную окружения `ANTHROPIC_API_KEY` и одобрите ключ, когда Claude Code спросит, использовать ли его, Claude Code пропустит запрос на вход. См. [Аутентификация](https://code.claude.com/docs/ru/authentication.md) для всех типов учетных записей и параметров настройки команды.

## Обновление Claude Code

Встроенные установки автоматически обновляются в фоновом режиме. Вы можете [настроить канал выпуска](#configure-release-channel) для управления тем, получаете ли вы обновления немедленно или по отложенному стабильному расписанию, или [отключить автоматические обновления](#disable-auto-updates) полностью. Установки Homebrew, WinGet и [менеджер пакетов Linux](#install-with-linux-package-managers) требуют ручного обновления по умолчанию.

### Автоматические обновления

Claude Code проверяет наличие обновлений при запуске и периодически во время работы. Обновления загружаются и устанавливаются в фоновом режиме, а затем вступают в силу при следующем запуске Claude Code.

Выполните `claude doctor` в оболочке, чтобы увидеть результат последней попытки обновления, зафиксированной Claude Code. Если во встроенной установке команда сообщает о неудачной попытке, см. раздел [`Auto-update failed` в нижней строке сессии](https://code.claude.com/docs/ru/troubleshoot-install#auto-update-failed), чтобы узнать, что делать дальше.

На macOS и Linux встроенный установщик управляет средством запуска в `~/.local/bin/claude` как символической ссылкой в `~/.local/share/claude/versions/`. Если вы замените это средство запуска своим собственным скриптом или символической ссылкой, автоматическое обновление и `claude update` оставляют его на месте: новые версии по-прежнему устанавливаются в каталог `versions/`, и ваше средство запуска решает, какая версия запускается.

С пользовательским средством запуска Claude Code также сохраняет каждую установленную версию на диске, потому что не может определить, какая версия нужна средству запуска. `claude doctor` сообщает о средстве запуска, которое встроенный установщик не создал.

Чтобы позволить Claude Code снова управлять средством запуска, удалите `~/.local/bin/claude` и выполните `claude update`.

Если глобальная установка npm не может автоматически обновляться, потому что глобальный каталог npm не доступен для записи, Claude Code показывает одноразовое уведомление при запуске, и `claude doctor` перечисляет доступные исправления. Подробнее см. в разделе [ошибки разрешений при установке](https://code.claude.com/docs/ru/troubleshoot-install.md#permission-errors-during-installation).

> [!NOTE]
>
> Установки Homebrew, WinGet, apt, dnf и apk не обновляются автоматически по умолчанию; см. ниже, чтобы согласиться для Homebrew и WinGet. Чтобы обновить Homebrew вручную, выполните `brew upgrade claude-code` или `brew upgrade claude-code@latest`, в зависимости от того, какой cask вы установили. Для WinGet выполните `winget upgrade Anthropic.ClaudeCode`. Для менеджеров пакетов Linux см. команды обновления в разделе [Install with Linux package managers](#install-with-linux-package-managers).
>
> Чтобы Claude Code выполнил команду обновления для вас на Homebrew или WinGet, установите [`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`](https://code.claude.com/docs/ru/env-vars) на `1`. Claude Code затем выполняет обновление в фоновом режиме, когда доступна новая версия, и показывает приглашение перезагрузки при успехе. Обновление затрагивает только пакет Claude Code и не влияет на другое программное обеспечение, которое вы установили.
>
> На WinGet обновление может не удаться, пока Claude Code работает, потому что Windows блокирует исполняемый файл. В этом случае Claude Code показывает команду ручного обновления вместо этого. apt, dnf и apk продолжают требовать ручного обновления, потому что эти команды требуют повышенных привилегий.
>
> **Известная проблема:** Claude Code может уведомить вас об обновлениях до того, как новая версия будет доступна в этих менеджерах пакетов. Если обновление не удается, подождите и повторите попытку позже.
>
> Homebrew сохраняет старые версии на диске после обновлений. Периодически выполняйте `brew cleanup` для освобождения дискового пространства.

### Настройка канала выпуска

Управляйте каналом выпуска, который Claude Code использует для автоматических обновлений и `claude update`, с помощью параметра `autoUpdatesChannel`:

* `"latest"`, по умолчанию: получайте новые функции сразу же после их выпуска
* `"stable"`: используйте версию, которая обычно имеет возраст около одной недели, пропуская выпуски с серьезными регрессиями

Настройте это через `/config` → **Auto-update channel**, или добавьте в [файл settings.json](https://code.claude.com/docs/ru/settings.md):

```json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

С этой настройкой встроенная установка обновляется до стабильной версии, даже если эта версия старше вашей. Чтобы избежать понижения версии, также [закрепите минимальную версию](#pin-a-minimum-version).

Только что выпущенная модель может требовать версию Claude Code новее той, которую предоставляет канал stable. Чтобы использовать эту модель прямо сейчас, перейдите на канал latest.

Для развертываний в масштабах предприятия вы можете обеспечить согласованный канал выпуска во всей организации, используя [управляемые параметры](https://code.claude.com/docs/ru/managed-settings.md).

Установки Homebrew выбирают канал по имени cask вместо этого параметра: `claude-code` отслеживает стабильный и `claude-code@latest` отслеживает последний.

Установки из репозиториев apt, dnf и apk выбирают канал по репозиторию вместо этого параметра. Чтобы переключить канал, следуйте инструкциям в разделе [Установка с помощью менеджеров пакетов Linux](#install-with-linux-package-managers).

### Закрепление минимальной версии

Чтобы перевести встроенную установку на [канал выпуска](#configure-release-channel) `"stable"` без понижения версии, установите для [`minimumVersion`](https://code.claude.com/docs/ru/settings-reference#minimumversion) значение версии, которую вы используете. Фоновые автоматические обновления и `claude update` отказываются устанавливать любую версию ниже минимальной.

Задайте минимум в `/config`, чтобы Claude Code подставил вашу текущую версию, или в файле настроек, чтобы ввести номер самостоятельно:

* **В `/config`**: переключите **Auto-update channel** на stable, затем выберите вариант, позволяющий остаться на текущей версии. Если вы переключитесь обратно на latest в `/config`, Claude Code очистит минимум.
* **В [файле настроек](https://code.claude.com/docs/ru/settings.md)**: выполните `claude --version` в оболочке и установите для `minimumVersion` номер в начале вывода. В том же изменении установите для `autoUpdatesChannel` значение `"stable"`.

Этот `~/.claude/settings.json` переключает установку версии 2.1.323 на stable:

```json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.323"
}
```

Установка остаётся на версии 2.1.323, пока канал stable не предоставит более новую версию.

#### Установка ограничений версий для организации

В [управляемых настройках](https://code.claude.com/docs/ru/managed-settings.md) `minimumVersion` обеспечивает минимум на уровне организации, который настройки пользователя и проекта не могут переопределить.

Закрепление `minimumVersion` только ограничивает обновления. Чтобы заставить Claude Code отказаться запускаться вне диапазона версий, используйте вместо этого управляемые настройки `requiredMinimumVersion` и `requiredMaximumVersion`. См. [`requiredMinimumVersion`](https://code.claude.com/docs/ru/settings-reference#requiredminimumversion) и [`requiredMaximumVersion`](https://code.claude.com/docs/ru/settings-reference#requiredmaximumversion).

### Отключение автоматических обновлений

Установите `DISABLE_AUTOUPDATER` на `"1"` в ключе `env` файла [`settings.json`](https://code.claude.com/docs/ru/settings-reference#all-settings):

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

На встроенной или npm установке подтвердите, что изменение вступило в силу, выполнив `claude doctor` и проверив, что строка `Auto-updates` показывает `disabled (set by env: DISABLE_AUTOUPDATER)` вместо `enabled`.

`DISABLE_AUTOUPDATER` только останавливает фоновую проверку; `claude update` и `claude install` по-прежнему работают. Чтобы заблокировать все пути обновления, включая ручные обновления, установите [`DISABLE_UPDATES`](https://code.claude.com/docs/ru/env-vars) вместо этого. Используйте это, когда вы распространяете Claude Code через свои собственные каналы и вам нужно, чтобы пользователи оставались на версии, которую вы предоставляете.

### Ручное обновление

Чтобы применить обновление немедленно без ожидания следующей проверки в фоновом режиме, выполните:

```bash theme={null}
claude update
```

Когда обновление устанавливается, команда выводит строку, которая заканчивается на `to version <new version>`. Если вы уже находитесь на самой новой версии, она сообщает `Claude Code is up to date (<version>)`. Установки, управляемые Homebrew, WinGet или apk, сообщают `Claude is up to date!` вместо этого.

## Расширенные параметры установки

Эти параметры предназначены для установки определенной версии, менеджеров пакетов Linux, npm, сетевого хранилища и проверки целостности двоичного файла.

### Установка определенной версии

Встроенный установщик принимает либо конкретный номер версии, либо канал выпуска (`latest` или `stable`). Канал, который вы выбираете во время установки, становится вашим значением по умолчанию для автоматических обновлений. См. [настройка канала выпуска](#configure-release-channel) для получения дополнительной информации.

Для установки последней версии (по умолчанию):

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> curl -fsSL https://claude.ai/install.sh | bash
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> irm https://claude.ai/install.ps1 | iex
> ```

> [tab] Windows CMD
>
> ```batch theme={null}
> curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
> ```

Для установки стабильной версии:

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> curl -fsSL https://claude.ai/install.sh | bash -s stable
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
> ```

> [tab] Windows CMD
>
> ```batch theme={null}
> curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
> ```

Для установки определенного номера версии:

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
> ```

> [tab] Windows CMD
>
> ```batch theme={null}
> curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
> ```

Чтобы подтвердить установленную версию, выполните `claude --version`: команда выводит точную версию, которую вы передали, например `2.1.89 (Claude Code)`.

### Установка с менеджерами пакетов Linux

Claude Code публикует подписанные репозитории apt, dnf и apk. Каждый репозиторий предлагает два канала: `stable` предоставляет версию, которая обычно примерно на неделю старше, пропуская выпуски с серьезными регрессиями, и `latest` предоставляет каждый выпуск сразу же после его выхода. Приведенные ниже команды настраивают канал `stable`, который подходит большинству пользователей; каждая вкладка также показывает URL репозитория `latest`. Установки менеджеров пакетов не обновляются автоматически через Claude Code; обновления поступают через ваш обычный рабочий процесс обновления системы.

Все репозитории подписаны с помощью [ключа подписи выпуска Claude Code](#binary-integrity-and-code-signing). Перед доверием к ключу проверьте его, как описано в каждой вкладке.

> [tab] apt
>
> Для Debian и Ubuntu. Команды установки ниже загружают ключ подписи с помощью `curl` и проверяют его с помощью `gpg`, которые свежие установки Debian и Ubuntu могут не включать. Если любая команда сообщает `command not found`, сначала установите оба:
>
> ```bash theme={null}
> sudo apt install curl gnupg
> ```
>
> Загрузите ключ подписи:
>
> ```bash theme={null}
> sudo install -d -m 0755 /etc/apt/keyrings
> sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
>   -o /etc/apt/keyrings/claude-code.asc
> ```
>
> Если эта загрузка не удается, `apt update` позже не удается с `NO_PUBKEY BAA929FF1A7ECACE`. Подтвердите, что ключ загружен и принадлежит Anthropic перед продолжением:
>
> ```bash theme={null}
> gpg --show-keys /etc/apt/keyrings/claude-code.asc
> ```
>
> Единственный отпечаток, который выводит gpg, должен быть `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`. Если gpg сообщает, что файл не может быть открыт или не содержит действительных данных OpenPGP, загрузка не удалась или вернула неправильное содержимое. Убедитесь, что ваша сеть может достичь `downloads.claude.ai`, затем повторно выполните команду загрузки.
>
> Зарегистрируйте репозиторий на канале `stable` и установите:
>
> ```bash theme={null}
> echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
>   | sudo tee /etc/apt/sources.list.d/claude-code.list
> sudo apt update
> sudo apt install claude-code
> ```
>
> Чтобы вместо этого использовать канал `latest`, оба пути URL и имя suite изменяются. Используйте эту строку `deb`:
>
> ```bash theme={null}
> echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/latest latest main" \
>   | sudo tee /etc/apt/sources.list.d/claude-code.list
> ```
>
> Для обновления позже выполните `sudo apt update && sudo apt upgrade claude-code`.

> [tab] dnf
>
> Для Fedora и RHEL. Следующие команды настраивают канал `stable`:
>
> ```bash theme={null}
> sudo tee /etc/yum.repos.d/claude-code.repo <<'EOF'
> [claude-code]
> name=Claude Code
> baseurl=https://downloads.claude.ai/claude-code/rpm/stable
> enabled=1
> gpgcheck=1
> gpgkey=https://downloads.claude.ai/keys/claude-code.asc
> EOF
> sudo dnf install claude-code
> ```
>
> Чтобы вместо этого использовать канал `latest`, установите `baseurl` на репозиторий `latest`:
>
> ```ini theme={null}
> baseurl=https://downloads.claude.ai/claude-code/rpm/latest
> ```
>
> dnf загружает ключ при первой установке и предлагает вам подтвердить отпечаток. Проверьте, что он совпадает с `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE` перед принятием.
>
> Для обновления позже выполните `sudo dnf upgrade claude-code`.

> [tab] apk
>
> Для Alpine Linux. Следующие команды настраивают канал `stable`:
>
> ```sh theme={null}
> wget -O /etc/apk/keys/claude-code.rsa.pub \
>   https://downloads.claude.ai/keys/claude-code.rsa.pub
> echo "https://downloads.claude.ai/claude-code/apk/stable" >> /etc/apk/repositories
> apk add bash claude-code
> ```
>
> Чтобы переключиться на канал `latest`, удалите строку репозитория `stable` и добавьте репозиторий `latest`:
>
> ```sh theme={null}
> sed -i '\|downloads.claude.ai/claude-code/apk/stable|d' /etc/apk/repositories
> echo "https://downloads.claude.ai/claude-code/apk/latest" >> /etc/apk/repositories
> ```
>
> Проверьте загруженный ключ с помощью `sha256sum /etc/apk/keys/claude-code.rsa.pub`, который должен сообщить `395759c1f7449ef4cdef305a42e820f3c766d6090d142634ebdb049f113168b6`.
>
> Для обновления позже выполните `apk update && apk upgrade claude-code`.

### Установка с npm

> [!NOTE]
>
> Если `npm --version` в вашей оболочке выводит версию, начинающуюся с `12`, вместо этого следуйте инструкциям в разделе [Исправление установки npm 12](https://code.claude.com/docs/ru/troubleshoot-install.md#fix-an-npm-12-install). Не выполняйте установку с `sudo`. Claude Code запускает npm без `sudo`, когда обновляет себя, поэтому установка, требующая `sudo`, не может обновляться автоматически.

Вы также можете установить Claude Code как глобальный пакет npm. Пакет npm требует [Node.js 22 или позже](https://nodejs.org/en/download). На более старой версии Node.js npm по умолчанию выводит предупреждение `EBADENGINE` и завершает установку, а не прерывает её с ошибкой. Установленный `claude` всё равно работает, так как пакет загружает встроенный двоичный файл, который не использует ваш Node.js во время выполнения.

```bash theme={null}
npm install -g @anthropic-ai/claude-code@latest
```

Пакет npm устанавливает тот же встроенный двоичный файл, что и автономный установщик. npm получает двоичный файл через дополнительную зависимость для каждой платформы, такую как `@anthropic-ai/claude-code-darwin-arm64`, и шаг postinstall связывает его на место. Установленный двоичный файл `claude` сам по себе не вызывает Node.

Поддерживаемые платформы установки npm: `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64` и `win32-arm64`. Ваш менеджер пакетов должен разрешать дополнительные зависимости. См. [устранение неполадок](https://code.claude.com/docs/ru/troubleshoot-install.md#native-binary-not-found-after-npm-install), если двоичный файл отсутствует после установки.

Для обновления установки npm выполните `npm install -g @anthropic-ai/claude-code@latest`. Избегайте `npm update -g`, который соблюдает диапазон semver из исходной установки и может не переместить вас на самый новый выпуск.

> [!WARNING]
>
> НЕ используйте `sudo npm install -g`, так как это может привести к проблемам с разрешениями и рискам безопасности. Если вы столкнулись с ошибками разрешений, см. [устранение неполадок ошибок разрешений](https://code.claude.com/docs/ru/troubleshoot-install.md#permission-errors-during-installation).

### Установка в сетевое хранилище

Работающая сессия считывает части исполняемого файла Claude Code с диска в процессе работы, а не только при запуске. Если файл становится недоступным для чтения посреди сессии, например потому что он был усечен или удален в сетевом хранилище, сессия аварийно завершается. В Linux ваша оболочка сообщает об этом как `Bus error`.

Когда домашние каталоги находятся в сетевом хранилище, например домашний каталог NFS, подключенный на нескольких машинах, организуйте установки так, чтобы исполняемый файл каждой сессии оставался доступным для чтения до завершения сессии:

* **Устанавливайте на локальный диск**: размещайте двоичный файл в локальной файловой системе каждой машины, например с помощью [менеджера пакетов Linux](#install-with-linux-package-managers) или собственных инструментов развёртывания. Пользовательский префикс npm и каталог встроенного установщика по умолчанию `~/.local/share/claude/versions/` оба находятся в домашнем каталоге.
* **Храните каждую версию в отдельном каталоге**: обновление установки npm на месте с помощью `npm install -g` удаляет предыдущий двоичный файл. В хранилище, общем для нескольких машин, это удаляет файл, который всё ещё выполняют сессии на других машинах. Устанавливайте каждую новую версию рядом со старыми и переводите на неё пользователей.
* **Удаляйте старую версию, только когда ни одна машина не может её ещё выполнять**: машина не видит процессы, запущенные на других машинах, поэтому проверки запущенных процессов перед удалением недостаточно.
* **Отключите собственные обновления Claude Code**: задайте [`DISABLE_UPDATES`](https://code.claude.com/docs/ru/env-vars) и устанавливайте новые версии с помощью собственных инструментов. В противном случае автоматическое обновление установки npm на одной машине выполняет то же обновление на месте и удаляет двоичный файл, который выполняют сессии на других машинах. Одной настройки `DISABLE_AUTOUPDATER` недостаточно, поскольку пользователи всё ещё могут выполнить `claude update` и `claude install`. См. [Отключение автоматических обновлений](#disable-auto-updates).

Встроенный установщик самостоятельно удаляет старые версии из `~/.local/share/claude/versions/`, что важно, когда этот каталог находится в общем хранилище. Помимо версии, на которую указывает лаунчер, и любой версии, которую выполняет сессия на той же машине, он сохраняет две самые новые версии и удаляет остальные. Сессия на другой машине, выполняющая удалённую версию, теряет свой двоичный файл. С [пользовательским лаунчером](#auto-updates) Claude Code сохраняет все установленные версии и оставляет очистку вам.

### Целостность двоичного файла и подпись кода

Каждый выпуск публикует `manifest.json`, содержащий контрольные суммы SHA256 для каждого двоичного файла платформы. Манифест подписан ключом GPG Anthropic, поэтому проверка подписи на манифесте транзитивно проверяет каждый двоичный файл, который он указывает.

#### Проверка подписи манифеста

Шаги 1-3 требуют оболочки POSIX с `gpg` и `curl`. В Windows выполните их в Git Bash или WSL. Шаг 4 включает опцию PowerShell.

**1. Загрузка и импорт открытого ключа**

Ключ подписи выпуска опубликован по фиксированному URL.

```bash theme={null}
curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
```

Отобразите отпечаток импортированного ключа.

```bash theme={null}
gpg --fingerprint security@anthropic.com
```

Подтвердите, что вывод включает этот отпечаток:

```text theme={null}
31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
```

**2. Загрузка манифеста и подписи**

Установите `VERSION` на выпуск, который вы хотите проверить.

```bash theme={null}
REPO=https://downloads.claude.ai/claude-code-releases
VERSION=2.1.89
curl -fsSLO "$REPO/$VERSION/manifest.json"
curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
```

**3. Проверка подписи**

Проверьте отделенную подпись против манифеста.

```bash theme={null}
gpg --with-fingerprint --verify manifest.json.sig manifest.json
```

Действительный результат сообщает `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`. При настройках по умолчанию `gpg` также выводит `WARNING: This key is not certified with a trusted signature!` для вновь импортированного ключа. Это ожидается. Строка `Good signature` подтверждает, что криптографическая проверка прошла.

Чтобы убедиться, что манифест подписан ключом Anthropic, сравните строку `Primary key fingerprint` в конце вывода с отпечатком, указанным на этой странице в шаге 1. Если они совпадают и вывод не содержит `BAD signature`, перейдите к шагу 4. В противном случае не используйте этот манифест.

**4. Проверка двоичного файла против манифеста**

Сравните контрольную сумму SHA256 двоичного файла со значением, указанным в `platforms.<platform>.checksum` в `manifest.json`. Приведенные ниже команды предполагают двоичный файл `claude` в текущем каталоге. Чтобы вместо этого проверить установленный встроенный двоичный файл, выполните команду для `~/.local/share/claude/versions/VERSION`, заменив VERSION на выпуск, который вы установили на шаге 2.

> [tab] Linux
>
> ```bash theme={null}
> sha256sum claude
> ```

> [tab] macOS
>
> ```bash theme={null}
> shasum -a 256 claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
> ```

> [!NOTE]
>
> Подписи манифеста доступны для выпусков начиная с `2.1.89`. Более ранние выпуски публикуют контрольные суммы в `manifest.json` без отделенной подписи.

#### Подписи кода платформы

В дополнение к подписанному манифесту отдельные двоичные файлы несут подписи кода, специфичные для платформы, где это поддерживается.

* **macOS**: подписано "Anthropic PBC" и заверено Apple. Проверьте с помощью `codesign --verify --verbose ./claude`.
* **Windows**: подписано "Anthropic, PBC". Проверьте с помощью `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: двоичные файлы не подписаны индивидуально кодом. Если вы загружаете непосредственно из корзины `claude-code-releases` или используете встроенный установщик, проверьте целостность с помощью подписи манифеста выше. Если вы устанавливаете с помощью [apt, dnf или apk](#install-with-linux-package-managers), ваш менеджер пакетов автоматически проверяет подписи, используя ключ подписи репозитория.

## Удаление Claude Code

Чтобы удалить Claude Code, следуйте инструкциям для вашего метода установки. Если `claude` все еще работает после этого, у вас, вероятно, есть вторая установка или оставшийся псевдоним оболочки из старого установщика. См. [Проверка конфликтующих установок](https://code.claude.com/docs/ru/troubleshoot-install.md#check-for-conflicting-installations), чтобы найти и удалить его.

### Удаление встроенной установки

Удалите двоичный файл Claude Code и файлы версии:

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> rm -f ~/.local/bin/claude
> rm -rf ~/.local/share/claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
> Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
> ```

### Удаление с помощью Homebrew

Удалите cask Homebrew, который вы установили. Если вы установили стабильный cask:

```bash theme={null}
brew uninstall --cask claude-code
```

Если вы установили последний cask:

```bash theme={null}
brew uninstall --cask claude-code@latest
```

### Удаление с помощью WinGet

Удалите пакет WinGet:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Удаление с помощью apt, dnf или apk

Удалите пакет и конфигурацию репозитория:

> [tab] apt
>
> ```bash theme={null}
> sudo apt remove claude-code
> sudo rm /etc/apt/sources.list.d/claude-code.list /etc/apt/keyrings/claude-code.asc
> ```

> [tab] dnf
>
> ```bash theme={null}
> sudo dnf remove claude-code
> sudo rm /etc/yum.repos.d/claude-code.repo
> ```

> [tab] apk
>
> ```sh theme={null}
> apk del claude-code
> sed -i '\|downloads.claude.ai/claude-code/apk|d' /etc/apk/repositories
> rm /etc/apk/keys/claude-code.rsa.pub
> ```

### Удаление с помощью npm

Удалите глобальный пакет npm:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Удаление файлов конфигурации

> [!WARNING]
>
> Удаление файлов конфигурации удалит все ваши параметры, разрешенные инструменты, конфигурации MCP server и историю сеансов.

Расширение VS Code, плагин JetBrains и приложение Desktop также записывают в `~/.claude/`. Если какое-либо из них все еще установлено, каталог будет пересоздан при следующем запуске. Чтобы полностью удалить Claude Code, удалите [расширение VS Code](https://code.claude.com/docs/ru/vs-code.md#uninstall-the-extension), плагин JetBrains и приложение Desktop перед удалением этих файлов.

Чтобы удалить параметры Claude Code и кэшированные данные:

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> # Удаление пользовательских параметров и состояния
> rm -rf ~/.claude
> rm ~/.claude.json
>
> # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
> rm -rf .claude
> rm -f .mcp.json
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> # Удаление пользовательских параметров и состояния
> Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
> Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force
>
> # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
> Remove-Item -Path ".claude" -Recurse -Force
> Remove-Item -Path ".mcp.json" -Force
> ```
