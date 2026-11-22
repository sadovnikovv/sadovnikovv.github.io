> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Устранение неполадок при установке и входе

> Исправьте ошибки command not found, PATH, прав доступа, сети и аутентификации при установке или входе в Claude Code.

Если установка не удалась или вы не можете войти, найдите вашу ошибку ниже. Для проблем во время выполнения после того, как Claude Code заработал, см. [Устранение неполадок](https://code.claude.com/docs/ru/troubleshooting.md). Для проблем конфигурации, таких как неприменение настроек или несрабатывание хуков, см. [Отладка конфигурации](https://code.claude.com/docs/ru/debug-your-config.md).

## Найдите вашу ошибку

Сопоставьте сообщение об ошибке или симптом, который вы видите, с исправлением:

| Что вы видите | Решение |
| :- | :- |
| `command not found: claude` или `'claude' is not recognized` | [Исправьте ваш PATH](#command-not-found-claude-after-installation) |
| `Native installation exists but ... is not in your PATH` | [Добавьте каталог установки в ваш PATH](#verify-your-path) |
| `INFO: Could not find files for the given pattern(s).` от `where.exe claude` | [Проверьте, установлен ли Claude Code](#check-for-conflicting-installations) |
| `zsh: permission denied: /Users/you/.zshrc` или `bash: /home/you/.bashrc: Permission denied` | [Сделайте файл конфигурации оболочки доступным для записи](#permission-denied-when-adding-to-your-path) |
| `syntax error near unexpected token '<'` | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `< was unexpected at this time` в CMD | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `The term 'System.Xml.XmlDocument' is not recognized` | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `curl: (22) The requested URL returned error: 403` | [Install script returned 403](#install-script-returns-html-instead-of-a-shell-script) |
| `curl: (23)` или `curl: (56) Failure writing output to destination` | [Проверьте подключение или используйте альтернативный установщик](#curl-56-failure-writing-output-to-destination) |
| `Killed` во время установки на Linux | [Освободите память или добавьте пространство подкачки](#install-killed-on-low-memory-linux-servers) |
| `Installation was killed before it could finish` | [Освободите память, затем повторно запустите установщик](#installation-was-killed-before-it-could-finish) |
| `Raw mode is not supported` во время установки | [Повторно запустите установщик](#raw-mode-is-not-supported-during-install) |
| `EACCES: permission denied` во время установки | [Исправьте права доступа к каталогу установки](#permission-errors-during-installation) |
| `TLS connect error` или `SSL/TLS secure channel` | [Обновите сертификаты CA](#tls-or-ssl-connection-errors) |
| `CRYPT_E_NO_REVOCATION_CHECK` или `CRYPT_E_REVOCATION_OFFLINE` | [Обойдите заблокированные проверки отзыва](#tls-or-ssl-connection-errors) |
| `Failed to fetch version` или невозможно достичь сервера загрузки | [Проверьте параметры сети и прокси](#check-network-connectivity), а при ошибке сертификата [настройте корпоративные сертификаты CA](#tls-or-ssl-connection-errors) |
| `The connection dropped while downloading the update` или `Download timed out: exceeded the total deadline` | [Запустите обновление повторно или настройте прокси](#the-connection-dropped-while-downloading-the-update) |
| `Release verification failed for Claude Code` | [Запустите `claude update` или `claude install` повторно](#release-verification-failed) |
| `Auto-update failed · Run claude doctor` красным цветом в нижней строке сессии | [Запустите `claude update` из вашей оболочки](#auto-update-failed) |
| `irm is not recognized` или `The token '&&' is not a valid statement separator` | [Используйте правильную команду для вашей оболочки](#wrong-install-command-on-windows) |
| `Cask 'claude-code' is unavailable: No Cask with this name exists` | [Обновите Homebrew](#homebrew-cask-unavailable-or-outdated) |
| `Cask 'claude-code@latest' is not installed` | [Обновите установленный вами cask](#cask-is-not-installed) |
| `'bash' is not recognized as the name of a cmdlet` | [Используйте команду установщика Windows](#wrong-install-command-on-windows) |
| `A parameter cannot be found that matches parameter name 'fsSL'` | [Используйте команду установщика Windows](#wrong-install-command-on-windows) |
| `Claude Code on Windows requires either Git for Windows (for bash) or PowerShell` | [Установите оболочку](#claude-code-on-windows-requires-either-git-for-windows-for-bash-or-powershell) |
| `Claude Code does not support 32-bit Windows` | [Откройте Windows PowerShell, а не запись x86](#claude-code-does-not-support-32-bit-windows) |
| `The process cannot access the file ... because it is being used by another process` | [Очистите папку загрузок и повторите попытку](#the-process-cannot-access-the-file-during-windows-install) |
| `Error loading shared library` | [Неправильный вариант двоичного файла для вашей системы](#linux-musl-or-glibc-binary-mismatch) |
| `Illegal instruction` | [Несоответствие архитектуры или набора инструкций процессора](#illegal-instruction) |
| `cannot execute binary file: Exec format error` в WSL | [WSL1 native-binary regression](#exec-format-error-on-wsl1) |
| `Bus error` или `oh no: Bun has crashed` во время работы сессии | [Сохраните исполняемый файл доступным для чтения](#bus-error-while-a-session-is-running) |
| Установщик PowerShell завершается, но `claude` не найден или показывает старую версию | [Добавьте каталог установки в ваш PATH](#verify-your-path), затем откройте новый терминал |
| `dyld: Symbol not found`, `dyld: cannot load` или `Abort trap` на macOS | [Несовместимость двоичного файла](#dyld-cannot-load-on-macos) |
| `claude update` зависает после `Checking for updates`, или `claude doctor` зависает без вывода | [Переместите каталог по пути конфигурации оболочки](#claude-update-or-claude-doctor-hangs) |
| `Invoke-Expression` или `iex` ошибки парсинга цитирования HTML-тегов или CSS, или `ParserError` с `ParseException` | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script) |
| `running scripts is disabled on this system` или `PSSecurityException` | [Разрешите npm shims запускаться](#running-scripts-is-disabled-on-this-system) |
| `Error: claude native binary not installed` | [Завершите установку npm](#native-binary-not-found-after-npm-install) |
| `npm error code ENOTEMPTY` во время обновления или переустановки | [Удалите оставшийся каталог пакета](#npm-enotempty-during-update-or-reinstall) |
| `'claude' is not recognized` сразу после обновления на Windows | [Восстановите `claude.exe` из его резервной копии](#claude-exe-missing-after-an-update-on-windows) |
| На Windows команда установки выводит текст скрипта и ничего не устанавливается | [Запустите полную команду установки](#wrong-install-command-on-windows) |
| `App unavailable in region` | Claude Code недоступен в вашей стране. См. [поддерживаемые страны](https://www.anthropic.com/supported-countries). |
| `unable to get local issuer certificate` | [Настройте корпоративные сертификаты CA](#tls-or-ssl-connection-errors) |
| `OAuth error` или `403 Forbidden` | [Исправьте аутентификацию](#login-and-authentication) |
| `Claude Code access has not been granted for this account` | [Получите роль, которая включает Claude Code](#claude-code-access-has-not-been-granted-for-this-account) |
| `Unable to connect to Anthropic services` во время установки | См. [Unable to connect to Anthropic services](https://code.claude.com/docs/ru/errors.md#unable-to-connect-to-anthropic-services) в справочнике ошибок |
| `Could not load the default credentials` или `Could not load credentials from any providers` | [Учётные данные Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry](#bedrock-agent-platform-or-foundry-credentials-not-loading) |
| `ChainedTokenCredential authentication failed` или `CredentialUnavailableError` | [Учётные данные Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry](#bedrock-agent-platform-or-foundry-credentials-not-loading) |
| `API Error: 500`, `529 Overloaded`, `429` или другие ошибки 4xx и 5xx, не указанные выше | См. [справочник ошибок](https://code.claude.com/docs/ru/errors.md) |

Если вашей проблемы нет в списке, выполните диагностические проверки ниже, чтобы сузить причину.

> [!TIP]
>
> Если вы предпочитаете полностью избежать терминала, [Claude Code Desktop app](https://code.claude.com/docs/ru/desktop-quickstart.md) позволяет вам установить и использовать Claude Code через графический интерфейс. Загрузите его для [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) или [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs) и начните кодировать без какой-либо настройки командной строки. На Linux установите приложение с помощью apt, следуя [инструкциям по установке Linux](https://code.claude.com/docs/ru/desktop-linux.md).

## Запустите диагностические проверки

### Проверьте подключение к сети

Установщик загружает с `downloads.claude.ai`. Убедитесь, что вы можете его достичь:

> [tab] macOS/Linux
>
> ```bash theme={null}
> curl -sI https://downloads.claude.ai/claude-code-releases/latest
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> curl.exe -sI https://downloads.claude.ai/claude-code-releases/latest
> ```
>
> PowerShell создаёт псевдоним `curl` на `Invoke-WebRequest`, который отклоняет флаги `-sI`, поэтому вызовите `curl.exe` явно.

Вы достигли сервера, если первая строка показывает статус `200`. Вы видите `HTTP/2 200` на macOS и Linux, и `HTTP/1.1 200 OK` из `curl.exe`, включённого в Windows. Другие результаты указывают на причину:

* `403`: обычно прокси или сетевой фильтр, блокирующий хост, или Claude Code [недоступен в вашем регионе](https://www.anthropic.com/supported-countries)
* `5xx`: обычно временная проблема с сервисом; подождите несколько минут и повторите попытку

Если вы не видите вывода или установщик показывает `Could not resolve host` или таймаут соединения, значит, соединение не удалось установить. Проверьте следующие причины:

* Корпоративные брандмауэры или прокси, блокирующие `downloads.claude.ai`
* Региональные ограничения сети: попробуйте VPN или альтернативную сеть
* Проблемы TLS/SSL: см. [Ошибки соединения TLS или SSL](#tls-or-ssl-connection-errors)

Если вы находитесь за корпоративным прокси, установите `HTTPS_PROXY` и `HTTP_PROXY` на адрес вашего прокси перед установкой. Попросите URL прокси у вашей IT-команды, если вы его не знаете, или проверьте параметры прокси вашего браузера.

Этот пример устанавливает обе переменные прокси, а затем запускает установщик через ваш прокси:

> [tab] macOS/Linux
>
> ```bash theme={null}
> export HTTP_PROXY=http://proxy.example.com:8080
> export HTTPS_PROXY=http://proxy.example.com:8080
> curl -fsSL https://claude.ai/install.sh | bash
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> $env:HTTP_PROXY = 'http://proxy.example.com:8080'
> $env:HTTPS_PROXY = 'http://proxy.example.com:8080'
> irm https://claude.ai/install.ps1 | iex
> ```

### Проверьте ваш PATH

Если установка прошла успешно, но вы получаете ошибку `command not found` или `not recognized` при запуске `claude`, директория установки не находится в вашем PATH. Ваша оболочка ищет программы в директориях, указанных в PATH, и установщик размещает `claude` в `~/.local/bin/claude` на macOS/Linux или `%USERPROFILE%\.local\bin\claude.exe` на Windows.

Установщик обнаруживает этот случай и сообщает о нём в разделе `Setup notes:` своего вывода: `Native installation exists but ~/.local/bin is not in your PATH.` на macOS и Linux или `Native installation exists but C:\Users\you\.local\bin is not in your PATH.` на Windows. Вместе с этим примечанием он выводит способ исправления, но сам не изменяет PATH.

> [!NOTE]
>
> Расширение [VS Code](https://code.claude.com/docs/ru/vs-code.md) не размещает `claude` в этом месте. Оно содержит приватную копию CLI внутри директории расширения для своей собственной панели чата и не добавляет её в PATH. Если вы установили только расширение, `~/.local/bin/claude` не будет существовать. Запустите [автономную установку](https://code.claude.com/docs/ru/setup.md), чтобы использовать `claude` из терминала, а затем продолжите ниже.

Сначала проверьте, что программа вообще существует, затем проверьте, находится ли её папка в вашем PATH. Исправление PATH постоянное, поэтому его достаточно применить один раз. Выберите вкладку вашей платформы и выполните её команды там: в терминале на macOS и Linux или в PowerShell или Command Prompt на Windows.

> [tab] macOS/Linux
>
> Проверьте, что установщик разместил программу на месте:
>
> ```bash theme={null}
> ls -la ~/.local/bin/claude
> ```
>
> * **`No such file or directory`**: встроенной установки нет. Если вы не устанавливали Claude Code другим способом, например через npm, Homebrew или менеджер пакетов Linux, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code). Если вы установили его другим способом, см. [Проверьте наличие конфликтующих установок](#check-for-conflicting-installations).
> * **Информация о файле**: программа на месте. Далее проверьте ваш PATH.
>
> Перечислите записи PATH и отфильтруйте по папке установки:
>
> ```bash theme={null}
> echo $PATH | tr ':' '\n' | grep -Fx "$HOME/.local/bin"
> ```
>
> Если это выводит `/Users/you/.local/bin` или `/home/you/.local/bin`, директория находится в вашем PATH и вы можете перейти к [Проверьте наличие конфликтующих установок](#check-for-conflicting-installations). Если вывода нет, добавьте её в конфигурацию вашей оболочки с помощью двух команд для вашей оболочки. Команда `echo` сохраняет настройку для каждого нового терминала, а `source` применяет её к текущему окну. Команда `echo` ничего не выводит при успешном выполнении.
>
> Для Zsh, по умолчанию на macOS:
>
> ```bash theme={null}
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
> source ~/.zshrc
> ```
>
> Для Bash на Linux, где это по умолчанию на большинстве дистрибутивов:
>
> ```bash theme={null}
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
> source ~/.bashrc
> ```
>
> Для Bash на macOS добавьте строку в `~/.bash_profile` вместо этого. Terminal на macOS запускает Bash как оболочку входа, которая игнорирует `~/.bashrc` и читает только первый из `~/.bash_profile`, `~/.bash_login` или `~/.profile`, который существует. Если у вас уже есть `~/.bash_login` или `~/.profile` и нет `~/.bash_profile`, поместите строку в этот файл, а не создавайте `~/.bash_profile`:
>
> ```bash theme={null}
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
> source ~/.bash_profile
> ```
>
> Или закройте и снова откройте ваш терминал.
>
> Если команда `echo` выводит `permission denied`, см. [`permission denied` при добавлении в PATH](#permission-denied-when-adding-to-your-path).
>
> Для других оболочек, таких как fish или Nushell, добавьте `~/.local/bin` в ваш PATH, используя синтаксис конфигурации вашей оболочки, а затем перезагрузите ваш терминал.
>
> Проверьте, что исправление сработало:
>
> ```bash theme={null}
> claude --version
> ```
>
> Если `claude` по-прежнему не найден, проверьте следующие причины:
>
> * **Терминал был открыт до изменения**: уже открытое окно сохраняет старый PATH, а терминал внутри редактора получает PATH от редактора. Откройте новое окно или закройте и снова откройте редактор.
> * **Строка не была сохранена**: выполните `grep -n '.local/bin' ~/.zshrc`, подставив имя файла вашей оболочки. Если строка есть, команда выведет её вместе с номером строки. Если ничего не выводится, снова выполните две команды для PATH.
> * **Строка попала в файл другой оболочки**: выполните `echo $0`, чтобы узнать вашу оболочку, затем выполните две команды для PATH для этой оболочки.

> [tab] Windows PowerShell
>
> Проверьте, что установщик разместил программу на месте:
>
> ```powershell theme={null}
> Test-Path "$env:USERPROFILE\.local\bin\claude.exe"
> ```
>
> * **`False`**: встроенной установки нет. Если вы не устанавливали Claude Code другим способом, например через npm или WinGet, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code). Если вы установили его другим способом, см. [Проверьте наличие конфликтующих установок](#check-for-conflicting-installations).
> * **`True`**: программа на месте. Далее проверьте ваш PATH.
>
> Перечислите записи PATH и отфильтруйте по папке установки:
>
> ```powershell theme={null}
> $env:PATH -split ';' | Select-String '\.local\\bin'
> ```
>
> Если это выводит `C:\Users\you\.local\bin`, директория находится в вашем PATH и вы можете перейти к [Проверьте наличие конфликтующих установок](#check-for-conflicting-installations). Если вывода нет, добавьте директорию установки в ваш User PATH:
>
> ```powershell theme={null}
> $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
> [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
> ```
>
> Перезагрузите ваш терминал, чтобы изменение вступило в силу.
>
> Проверьте, что исправление сработало:
>
> ```powershell theme={null}
> claude --version
> ```
>
> Если `claude` по-прежнему не найден в новом терминале, проверьте следующие причины:
>
> * **Терминал работает внутри редактора**: он получает PATH от редактора, поэтому закройте и снова откройте редактор.
> * **Изменение не было сохранено**: выполните `[Environment]::GetEnvironmentVariable('PATH', 'User')` и найдите `.local\bin` в выведенном PATH. Если его нет, снова выполните две команды.

> [tab] Windows CMD
>
> Проверьте, что установщик разместил программу на месте:
>
> ```batch theme={null}
> dir "%USERPROFILE%\.local\bin\claude.exe"
> ```
>
> * **`File Not Found` или `The system cannot find the path specified.`**: встроенной установки нет. Если вы не устанавливали Claude Code другим способом, например через npm или WinGet, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code). Если вы установили его другим способом, см. [Проверьте наличие конфликтующих установок](#check-for-conflicting-installations).
> * **Информация о `claude.exe`**: программа на месте. Далее проверьте ваш PATH.
>
> Перечислите записи PATH и отфильтруйте по папке установки:
>
> ```batch theme={null}
> echo %PATH% | findstr /i "local\bin"
> ```
>
> Если вывода нет, откройте System Settings, перейдите в Environment Variables и добавьте `%USERPROFILE%\.local\bin` в вашу переменную User PATH. Перезагрузите ваш терминал.
>
> Проверьте, что исправление сработало:
>
> ```batch theme={null}
> claude --version
> ```
>
> Если `claude` по-прежнему не найден в новом терминале, учтите, что терминал внутри редактора получает PATH от редактора, поэтому также закройте и снова откройте редактор.

### Проверьте наличие конфликтующих установок

Несколько установок Claude Code могут вызвать несоответствия версий или неожиданное поведение. Проверьте, что установлено:

> [tab] macOS/Linux
>
> Перечислите все бинарные файлы `claude`, найденные в вашем PATH:
>
> ```bash theme={null}
> which -a claude
> ```
>
> Если это выводит `claude not found`, строку `no claude in` или ничего, значит `claude` нет в вашем PATH. Следующие проверки покажут, установлен ли он вообще.
>
> Проверьте три места, откуда может поступить бинарный файл `claude`. `~/.local/bin/claude` — это встроенный установщик, `~/.claude/local/` — это устаревшая локальная установка npm, созданная старыми версиями Claude Code, и список глобального npm показывает установку `-g`:
>
> ```bash theme={null}
> ls -la ~/.local/bin/claude
> ```
>
> Встроенная установка показывает символическую ссылку в `~/.local/share/claude/versions/`. Скрипт или символическая ссылка, которую вы создали сами в этом пути, — это пользовательский запускатель, который [автоматическое обновление оставляет на месте](https://code.claude.com/docs/ru/setup.md#auto-updates).
>
> Если какая-либо команда `ls` выводит `No such file or directory`, это не ошибка. Это означает, что ничего не установлено в этом месте, поэтому переходите к следующей проверке.
>
> ```bash theme={null}
> ls -la ~/.claude/local/
> ```
>
> ```bash theme={null}
> npm -g ls @anthropic-ai/claude-code 2>/dev/null
> ```
>
> Если `ls -la ~/.local/bin/claude` вывела `No such file or directory`, встроенной установки нет. Если вы не устанавливали Claude Code другим способом, например через npm, Homebrew или менеджер пакетов Linux, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code). Если `~/.local/bin/claude` существует, но `which -a claude` его не показала, папка не находится в вашем PATH: см. [Проверьте ваш PATH](#verify-your-path).

> [tab] Windows PowerShell
>
> Перечислите все бинарные файлы `claude`, найденные в вашем PATH:
>
> ```powershell theme={null}
> where.exe claude
> ```
>
> Если это выводит `INFO: Could not find files for the given pattern(s).`, значит `claude` нет в вашем PATH.
>
> Проверьте, разместил ли встроенный установщик бинарный файл:
>
> ```powershell theme={null}
> Test-Path "$env:USERPROFILE\.local\bin\claude.exe"
> ```
>
> * **`True`**: встроенная установка на месте. Если `where.exe` ничего не нашла, её папка не находится в вашем PATH: см. [Проверьте ваш PATH](#verify-your-path).
> * **`False`**: встроенной установки нет. Если вы не устанавливали Claude Code другим способом, например через npm или WinGet, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code).

Если вы найдёте несколько установок, оставьте только одну. Встроенная установка в `~/.local/bin/claude` на macOS/Linux или `%USERPROFILE%\.local\bin\claude.exe` на Windows рекомендуется. Удалите лишние:

Удалите глобальную установку npm:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

Удалите устаревшую локальную установку npm:

> [tab] macOS/Linux
>
> ```bash theme={null}
> rm -rf ~/.claude/local
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\local"
> ```

Удалите установку Homebrew на macOS. Если вы установили cask `claude-code@latest`, замените это имя:

```bash theme={null}
brew uninstall --cask claude-code
```

Удалите установку WinGet на Windows:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Проверьте разрешения директорий

Если установка завершается ошибкой из-за прав доступа, в сообщении указывается путь, который не удалось создать или в который не удалось выполнить запись. На Windows установка записывает файлы в `%USERPROFILE%`, которое по умолчанию доступно для записи вашим пользователем, поэтому этот раздел редко применяется там.

На macOS и Linux установка записывает файлы в следующие места:

* `~/.claude/downloads/`: куда команда установки помещает загруженный бинарный файл
* `~/.local/bin/`: запускатель `claude`
* `~/.local/share/claude/`: каждая загружаемая версия
* `~/.local/state/claude/`: файлы блокировки
* `~/.cache/claude/`: промежуточные загрузки
* [`~/.claude.json`](https://code.claude.com/docs/ru/claude-directory): ваш глобальный файл конфигурации, в котором установщик записывает способ установки

Если вы задали `XDG_DATA_HOME`, `XDG_STATE_HOME` или `XDG_CACHE_HOME`, установка использует их вместо `~/.local/share`, `~/.local/state` и `~/.cache`. Если вы задали [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars), глобальный файл конфигурации находится в этом каталоге, а не в вашем домашнем каталоге.

Проверьте, доступны ли директории для записи:

```bash theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

Если какая-либо директория недоступна для записи, создайте директорию установки и установите вашего пользователя в качестве владельца:

```bash theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### Проверьте, работает ли бинарный файл

Если `claude --version` выводит версию, но `claude` падает или зависает при запуске, запустите эти проверки, чтобы сузить причину. Если `claude --version` говорит command not found, сначала перейдите к [Проверьте ваш PATH](#verify-your-path); команды ниже предполагают, что `claude` находится в вашем PATH.

Подтвердите, что бинарный файл существует и исполняемый:

> [tab] macOS/Linux
>
> ```bash theme={null}
> ls -la "$(command -v claude)"
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> Get-Command claude | Select-Object Source
> ```

На Linux проверьте отсутствующие общие библиотеки. Если `ldd` показывает отсутствующие библиотеки, вам может потребоваться установить системные пакеты. На Alpine Linux и других дистрибутивах на основе musl см. [Несоответствие бинарного файла Linux musl или glibc](#linux-musl-or-glibc-binary-mismatch).

```bash theme={null}
ldd "$(command -v claude)" | grep "not found"
```

Подтвердите, что бинарный файл может выполняться:

```bash theme={null}
claude --version
```

## Распространённые проблемы установки

Это наиболее часто встречающиеся проблемы установки и их решения.

### Install script returns HTML instead of a shell script

Команда установки завершается с одной из этих ошибок, если загруженное ею содержимое не является скриптом установки.

**Bash или Zsh**: ошибка цитирует первую строку возвращённой страницы.

```text theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

**PowerShell, ошибки парсинга**: ошибки указывают на возвращённую страницу, а `iex` пытается запустить HTML и CSS как PowerShell.

```text theme={null}
iex : At line:1 char:2310
+ ... igin="anonymous"/><script type="text/javascript">!function(o,c){var n ...
Missing argument in parameter list.
...
```

Формулировка варьируется в зависимости от версии PowerShell и языка системы: вы можете увидеть `Missing expression after unary operator '--'` или `ParserError` с `ParseException` вместо этого. HTML-теги или CSS в цитируемом тексте идентифицируют этот сбой. Если вы загружаете с `-OutFile install.ps1` вместо этого, сохранённый файл — это та же веб-страница, поэтому это тоже не помогает.

**PowerShell, `System.Xml.XmlDocument`**: вместо цитирования страницы ошибка называет этот тип.

```text theme={null}
System.Xml.XmlDocument : The term 'System.Xml.XmlDocument' is not recognized as the name of a cmdlet, function, script
file, or operable program.
```

Когда `irm` может разобрать ответ как XML, он возвращает XML-объект вместо текста, и `iex` затем пытается запустить имя типа этого объекта как команду. Скрипт установки — это код PowerShell, и он не разбирается как XML, поэтому эта ошибка также означает, что ответ был чем-то иным, а не скриптом. Формулировка вокруг имени типа варьируется в зависимости от версии PowerShell и языка системы, но сам `System.Xml.XmlDocument` остаётся неизменным, поэтому ориентируйтесь на имя типа.

**CMD**: вы видите эту ошибку, за которой следует HTML возвращённой страницы.

```text theme={null}
< was unexpected at this time.

C:\Users\you><!DOCTYPE html>...
```

Первая строка отображается на языке вашей системы, поэтому ищите следующий за ней HTML.

**403 без страницы**: в зависимости от того, как был маршрутизирован запрос, curl сообщает статус 403 без HTML-тела.

```text theme={null}
curl: (22) The requested URL returned error: 403
```

Всё это означает, что URL установки вернул веб-страницу, XML-документ или статус ошибки вместо скрипта установки. Если вывод ошибки цитирует "App unavailable in region", Claude Code недоступен в вашей стране. См. [поддерживаемые страны](https://www.anthropic.com/supported-countries).

Простой 403 без тела часто имеет ту же причину, но это также может быть вызвано корпоративным прокси или брандмауэром, блокирующим загрузку. Если вы находитесь в поддерживаемой стране и всё ещё видите 403, пройдите через [Проверка подключения к сети](#check-network-connectivity) перед попыткой альтернативных установщиков ниже, так как они обращаются к тем же хостам.

В противном случае это может произойти из-за проблем с сетью, региональной маршрутизации или временного сбоя сервиса.

**Решения:**

1. **Повторите попытку через несколько минут**: проблема часто временная. Подождите и попробуйте исходную команду снова.

2. **Используйте альтернативный метод установки**: в отличие от нативной установки, установка через Homebrew или WinGet [по умолчанию не обновляется автоматически](https://code.claude.com/docs/ru/setup.md#auto-updates).

   На macOS установите через Homebrew:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   На Windows установите через WinGet:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

   Затем запустите `claude --version` для подтверждения: команда выводит номер версии, такой как `2.1.211 (Claude Code)`. Если оболочка сообщает, что `claude` не найден, откройте новое окно терминала и повторите попытку: сессия, из которой вы установили, сохраняет свой старый `PATH`.

### `command not found: claude` after installation

Установка завершилась, но `claude` не работает. Точная ошибка варьируется в зависимости от платформы:

| Платформа | Сообщение об ошибке |
| :- | :- |
| macOS | `zsh: command not found: claude` |
| Linux | `bash: claude: command not found` |
| Windows CMD | `'claude' is not recognized as an internal or external command` |
| PowerShell | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

На Windows, если ошибка появилась сразу после обновления Claude Code, см. [восстановление `claude.exe` из резервной копии](#claude-exe-missing-after-an-update-on-windows).

В противном случае см. [Проверка вашего PATH](#verify-your-path) для исправления на каждой платформе.

### `permission denied` when adding to your PATH

Если команда `echo`, которая добавляет `~/.local/bin` в ваш PATH, выводит `zsh: permission denied: /Users/you/.zshrc` или `bash: /home/you/.bashrc: Permission denied`, ваш пользователь не может записывать в этот файл, и ничего не было сохранено. В терминале проверьте, кто владеет файлом, подставив имя файла вашей оболочки вместо `~/.zshrc`:

```bash theme={null}
ls -l ~/.zshrc
```

Третье поле вывода — это владелец.

* **Владелец — другой пользователь, например `root`**: станьте владельцем с помощью `sudo chown $(whoami) ~/.zshrc`, что требует прав администратора.
* **Владелец — вы**: файл доступен только для чтения. Сделайте его доступным для записи с помощью `chmod u+w ~/.zshrc`.

Затем снова выполните две команды PATH для вашей оболочки из раздела [Проверка вашего PATH](#verify-your-path).

### `curl: (56) Failure writing output to destination`

Команда `curl ... | bash` загружает скрипт и передаёт его в Bash для выполнения. Эта ошибка и связанная с ней `curl: (23) Failure writing output to destination` означают, что Bash не получил полный скрипт. Код выхода 56 указывает, что сама загрузка была прервана, а код выхода 23 указывает, что curl не смог записать полученное в канал, обычно потому что Bash завершился рано.

Проверьте, что вы можете достичь `downloads.claude.ai` с проверкой в [Проверка подключения к сети](#check-network-connectivity). Если вы достигли сервера, исходный сбой был вероятно временным; повторите команду установки. Вы также можете [попробовать альтернативный метод установки](https://code.claude.com/docs/ru/setup.md#install-claude-code).

### Homebrew cask unavailable or outdated

Homebrew сообщает `Error: Cask 'claude-code' is unavailable: No Cask with this name exists`, когда ваша локальная копия индекса Homebrew cask предшествует публикации cask. Обновите индекс и повторите попытку:

```bash theme={null}
brew update
brew install --cask claude-code
```

Если Homebrew устанавливает более старую версию Claude Code, чем вы ожидаете, обычно причина в том же устаревшем индексе. Cask `claude-code` отслеживает стабильный канал и обычно отстаёт на неделю от последнего выпуска; для самой новой версии запустите вместо этого `brew install --cask claude-code@latest`. См. [Настройка канала выпуска](https://code.claude.com/docs/ru/setup.md#configure-release-channel) для различия между двумя cask.

### `Cask 'claude-code@latest' is not installed`

Homebrew предлагает два cask: `claude-code` и `claude-code@latest`. Запуск `brew upgrade --cask claude-code@latest`, когда установлен не этот cask, выводит `Error: Cask 'claude-code@latest' is not installed.` Чтобы узнать, какой cask у вас установлен, выполните в терминале:

```bash theme={null}
brew list --cask | grep claude-code
```

Обновите тот cask, который выведет команда. Если она ничего не выводит, не установлен ни один из cask.

### TLS or SSL connection errors

Ошибки такие как эти означают, что TLS handshake не удался:

* `curl: (35) TLS connect error`
* `schannel: next InitializeSecurityContext failed`
* PowerShell's `Could not create SSL/TLS secure channel`
* PowerShell's `Could not establish trust relationship for the SSL/TLS secure channel`

При ошибках `CRYPT_E_NO_REVOCATION_CHECK` или `CRYPT_E_REVOCATION_OFFLINE` перейдите к шагу 4.

**Решения:**

1. **Обновите сертификаты CA вашей системы**:

   На Ubuntu/Debian:

   ```bash theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   На macOS системный curl использует хранилище доверия Keychain; обновление самого macOS обновляет корневые сертификаты.

2. **В Windows PowerShell 5.1 включите TLS 1.2**:
   ```powershell theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   ```
   Затем запустите установщик в том же окне:
   ```powershell theme={null}
   irm https://claude.ai/install.ps1 | iex
   ```

3. **Проверьте помехи прокси или брандмауэра**: корпоративные прокси, выполняющие TLS inspection, могут вызвать эти ошибки, включая `unable to get local issuer certificate`, `unable to verify the first certificate` и `SELF_SIGNED_CERT_IN_CHAIN`. Настройте загрузку установщика так, чтобы она доверяла CA вашего корпоративного прокси:

   > [tab] macOS/Linux
   >
   > Задайте `CURL_CA_BUNDLE` для загрузок `curl` в скрипте установки и [`NODE_EXTRA_CA_CERTS`](https://code.claude.com/docs/ru/network-config#custom-ca-certificates) для команды `claude install`, которую скрипт затем запускает. Если у вас нет PEM-файла с корневым сертификатом CA вашего прокси, попросите его у вашей IT-команды. В этом примере обеим переменным задаётся файл CA вашего прокси, а скрипт запускается в том же терминале:
   >
   > ```bash theme={null}
   > export CURL_CA_BUNDLE=/path/to/corporate-ca.pem
   > export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   > curl -fsSL https://claude.ai/install.sh | bash
   > ```
   >
   > Если установка всё ещё завершается одной из этих ошибок сертификатов, попросите у вашей IT-команды файл, содержащий как публичные корневые сертификаты, так и полную цепочку CA вашего прокси. Затем укажите этот файл в обеих переменных.

   > [tab] Windows PowerShell
   >
   > Установщик PowerShell загружается через .NET, который проверяет TLS в хранилище сертификатов Windows. Попросите вашу IT-команду добавить сертификат CA прокси в хранилище Windows, если его там ещё нет, затем запустите установщик:
   >
   > ```powershell theme={null}
   > irm https://claude.ai/install.ps1 | iex
   > ```

   Для самого Claude Code после установки установите `NODE_EXTRA_CA_CERTS` так, чтобы запросы API доверяли тому же пакету:

   > [tab] macOS/Linux
   >
   > ```bash theme={null}
   > export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   > ```

   > [tab] Windows PowerShell
   >
   > ```powershell theme={null}
   > $env:NODE_EXTRA_CA_CERTS = 'C:\path\to\corporate-ca.pem'
   > ```

4. **На Windows обойдите заблокированные проверки отзыва**. Ошибки `CRYPT_E_NO_REVOCATION_CHECK (0x80092012)` и `CRYPT_E_REVOCATION_OFFLINE (0x80092013)` означают, что curl достиг сервера, но ваша сеть блокирует поиск отзыва сертификата, что распространено за корпоративными брандмауэрами. Если не удаётся команда `curl`, которая загружает `install.cmd`, запустите её снова из Command Prompt с добавленным `--ssl-revoke-best-effort`:
   ```batch theme={null}
   curl --ssl-revoke-best-effort -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
   ```
   Когда собственные загрузки скрипта сталкиваются с теми же ошибками, он автоматически повторяет их с проверкой отзыва best-effort, поэтому флаг нужен только в команде, которую вы запускаете сами. Проверка best-effort допускает недостижимый сервер отзыва, но всё ещё отклоняет сертификат, который известен как отозванный, соответствуя тому, как браузеры обрабатывают отзыв. Вы также можете полностью избежать проверки отзыва curl, запустив установщик PowerShell из PowerShell, который загружается через .NET и не падает, когда сервер отзыва недоступен:
   ```powershell theme={null}
   irm https://claude.ai/install.ps1 | iex
   ```
   Вы также можете установить с `winget install Anthropic.ClaudeCode`, что полностью избегает curl.

### `Failed to fetch version from downloads.claude.ai`

Причина указана в конце сообщения. Если это ошибка сертификата, например `unable to verify the first certificate`, см. [Ошибки подключения TLS или SSL](#tls-or-ssl-connection-errors). При любой другой причине см. [Проверка подключения к сети](#check-network-connectivity).

### The connection dropped while downloading the update

Соединение с сервером загрузки закрылось, пока `claude install` или `claude update` загружал бинарный файл Claude Code, и повторные попытки не помогли. Claude Code повторяет загрузку, когда соединение обрывается, передача зависает или загруженный файл не проходит проверку контрольной суммы, — всего до трёх попыток. Завершённая HTTP-ошибка, например 404, не повторяется, потому что сервер уже ответил. До v2.1.202 один оборванный разрыв соединения сразу приводил к сбою загрузки с голой ошибкой `aborted` без повторной попытки.

```text theme={null}
The connection dropped while downloading the update (attempt 3/3: aborted). Check your network — proxies sometimes cut off large downloads.
```

Текст в скобках указывает, какая попытка не удалась, и исходную сетевую ошибку. `claude update` выводит перед этим сообщением `Failed to install native update`.

Загрузка, которая остаётся подключённой, но не завершается в течение 10 минут, вместо этого завершается с ошибкой `Download timed out: exceeded the total deadline`. Claude Code не повторяет загрузку, превысившую время ожидания, потому что соединение, слишком медленное, чтобы уложиться в срок, не уложится в него и при немедленной повторной попытке. Шаги ниже применимы к обоим сообщениям.

Прокси или шлюз может закрыть длительную передачу до её завершения, а бинарный файл Claude Code — это объёмная загрузка.

**Что делать:**

* Снова запустите `claude update`. В остальном исправной сети загрузка обычно успешно выполняется при следующем запуске. В случае сообщения о превышении времени ожидания запустите команду снова из более быстрой или менее ограниченной сети.
* Если ваша сеть требует прокси, задайте `HTTPS_PROXY` перед запуском установщика или `claude update`. См. [Проверка подключения к сети](#check-network-connectivity).
* Если корпоративный прокси продолжает закрывать передачу, попросите вашу сетевую команду разрешить полную загрузку с `downloads.claude.ai`. См. [Требования к сетевому доступу](https://code.claude.com/docs/ru/network-config.md#network-access-requirements).
* Запустите `claude doctor` из вашей оболочки для диагностики установки

### Release verification failed for Claude Code

Это сообщение от `claude update` или `claude install` означает, что Claude Code не смог подтвердить подлинность выпуска, который собирался установить, поэтому ничего не было установлено. Любая уже установленная у вас версия продолжает работать.

```text theme={null}
Release verification failed for Claude Code <version> (<reason>). The update was not installed.
```

Выполните действие, соответствующее значению в скобках в вашем сообщении:

* **Значение, начинающееся с `sidecar_fetch_`**: снова запустите ту же команду из вашей оболочки. `claude update` выполнен успешно, если выводит строку, заканчивающуюся на `to version <new version>`, а `claude install` выполнен успешно, если выводит `Claude Code successfully installed!`.
* **Любое другое значение**: попробуйте выполнить ту же команду позже

При любом значении, если сообщение повторяется, [сообщите о проблеме](#still-stuck) и приложите полное сообщение.

### `Auto-update failed · Run claude doctor` in the session footer

Эта красная строка означает, что Claude Code попытался обновиться в фоновом режиме, и обновление не было установлено. Вы можете продолжать работу, ничего не предпринимая.

Строка отсылает вас к `claude doctor`, чья строка `Last update attempt: failed (install_failed)` указывает дату, но не причину. Чтобы завершить обновление или узнать, почему оно не удалось, вместо этого выполните `claude update` в вашей оболочке. Если и эта установка завершится ошибкой, найдите ошибку, которую выводит `claude update`, в разделе [Поиск вашей ошибки](#find-your-error).

### Wrong install command on Windows

Если вы видите `'irm' is not recognized`, `The token '&&' is not a valid statement separator`, `A parameter cannot be found that matches parameter name 'fsSL'` или `'bash' is not recognized as the name of a cmdlet`, вы скопировали команду установки для другой оболочки или операционной системы. Если команда выводит текст скрипта вместо установки чего-либо, вы запустили только её часть.

* **`irm` не распознан**: вы находитесь в CMD, а не PowerShell. У вас есть два варианта:

  Откройте PowerShell, найдя "PowerShell" в меню Start, затем запустите исходную команду установки:

  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  Или оставайтесь в CMD и используйте вместо этого установщик CMD:

  ```batch theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` не является допустимым разделителем операторов**: вы находитесь в PowerShell, но запустили команду установщика CMD. Используйте установщик PowerShell:
  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

* **`A parameter cannot be found that matches parameter name 'fsSL'`**: вы запустили установщик macOS/Linux `curl -fsSL ... | bash` в Windows PowerShell, где `curl` является псевдонимом для `Invoke-WebRequest` и отклоняет флаги `-fsSL`. Используйте вместо этого установщик PowerShell:
  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

* **`bash` не распознан**: вы запустили установщик macOS/Linux на Windows. Используйте вместо этого установщик PowerShell:
  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

* **Команда выводит текст скрипта вместо установки**: вы запустили часть команды, отвечающую за загрузку, без части, которая его выполняет. `irm https://claude.ai/install.ps1` само по себе выводит загруженный скрипт в терминал. Передайте его в `iex` для запуска:

  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  В CMD `curl -fsSL https://claude.ai/install.cmd` без `-o` выводит пакетный скрипт вместо его сохранения. Запустите полную команду:

  ```batch theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

Какой бы установщик вы ни использовали, подтвердите, что он сработал: откройте новый терминал и запустите `claude --version`, который выводит номер версии, такой как `2.1.211 (Claude Code)`.

### `running scripts is disabled on this system`

Установка или запуск Claude Code через npm на Windows может завершиться ошибкой `SecurityError`:

```text theme={null}
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
...
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
```

Та же ошибка называет `claude.ps1`, когда вы запускаете `claude` после установки npm. Политика выполнения PowerShell блокирует скрипты-лаунчеры `.ps1`, которые npm создаёт для своих команд. Политика применяется к файлам скриптов, поэтому она не влияет на установщик PowerShell `irm https://claude.ai/install.ps1 | iex`, который запускает загруженный текст напрямую.

**Решения:**

1. **Разрешите локально созданные скрипты для вашего пользователя**, затем повторите попытку:
   ```powershell theme={null}
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. **Вызовите вместо этого лаунчер `.cmd`**: `npm.cmd` и `claude.cmd` делают то же самое, и политика их не охватывает.
3. **Используйте [установщик PowerShell](https://code.claude.com/docs/ru/setup.md#install-claude-code)** вместо npm. Он устанавливает бинарный файл, а не скрипт `.ps1`.

### `The process cannot access the file` during Windows install

Если установщик PowerShell завершается ошибкой `Failed to download binary: The process cannot access the file ... because it is being used by another process`, установщик не смог записать в `%USERPROFILE%\.claude\downloads`. Это обычно означает, что предыдущая попытка установки всё ещё работает, или антивирусное программное обеспечение сканирует частично загруженный бинарный файл в этой папке.

Закройте любые другие окна PowerShell, запускающие установщик, и дождитесь завершения сканирования антивирусом. Затем удалите папку загрузок и запустите установщик снова:

```powershell theme={null}
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\downloads"
irm https://claude.ai/install.ps1 | iex
```

### `claude.exe` missing after an update on Windows

Если ваш терминал сообщает `'claude' is not recognized` сразу после обновления Claude Code на Windows, проверьте, содержит ли `%USERPROFILE%\.local\bin` по-прежнему `claude.exe`. Если этот каталог вообще не находится в вашем PATH, см. вместо этого [Проверка вашего PATH](#verify-your-path). Для обновления на Windows Claude Code переименовывает существующий `claude.exe` в резервную копию и перемещает новую версию на его место. Если перемещение новой версии на место не удаётся и Claude Code также не может переименовать резервную копию обратно, каталог сохраняет резервную копию, но не содержит `claude.exe`.

Резервная копия — это файл в том же каталоге, имя которого начинается с `claude.exe.old.` с последующей числовой меткой времени. Запустите следующее в PowerShell, чтобы переименовать самую новую резервную копию обратно в `claude.exe`:

```powershell theme={null}
Get-ChildItem "$env:USERPROFILE\.local\bin\claude.exe.old.*" | Sort-Object Name | Select-Object -Last 1 | Rename-Item -NewName claude.exe
```

Затем запустите `claude --version` для подтверждения исправления. Восстановленный `claude.exe` выводит номер версии.

Если нет файла `claude.exe.old.*`, или `claude` всё ещё не работает после переименования, переустановите вместо этого:

```powershell theme={null}
irm https://claude.ai/install.ps1 | iex
```

До v2.1.281 Claude Code мог удалить резервную копию, пока `claude.exe` всё ещё отсутствовал.

### Install killed on low-memory Linux servers

Сообщение `Killed` во время установки обычно означает, что механизм Linux out-of-memory (OOM) killer завершил шаг `claude install`, потому что в системе закончилась свободная память. Это распространено на небольших VPS и облачных экземплярах. Скрипт установки сообщает причину и завершается с кодом выхода 137. В этом примере номер строки и ID процесса варьируются в зависимости от выпуска и запуска:

```text theme={null}
Setting up Claude Code...
bash: line 183: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
Installation was killed before it could finish (exit code 137). This usually means the system ran out of memory.
Claude Code needs roughly 512MB of free memory to install. Free up memory, then run this script again.
```

Установка требует примерно 512 МБ свободной памяти, а запуск Claude Code требует больше. См. [системные требования](https://code.claude.com/docs/ru/setup.md#system-requirements).

**Решения:**

1. **Добавьте пространство подкачки**, если ваш сервер имеет ограниченную оперативную память. Подкачка использует дисковое пространство как переполнение памяти, позволяя установке завершиться даже при низкой физической оперативной памяти.

   Создайте файл подкачки размером 2 ГБ и включите его:

   ```bash theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   Затем повторите установку:

   ```bash theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Закройте другие процессы**, чтобы освободить память перед установкой.

3. **Используйте больший экземпляр**, если возможно. Claude Code требует по крайней мере 4 ГБ оперативной памяти.

### Installation was killed before it could finish

Скрипт установки сообщает, когда шаг `claude install` завершается сигналом. В Linux код выхода 137 означает, что процесс получил SIGKILL, и на хосте с малым объёмом памяти это обычно механизм ядра out-of-memory (OOM) killer. Скрипт выводит это объяснение и завершается с кодом выхода 137:

```text theme={null}
Installation was killed before it could finish (exit code 137). This usually means the system ran out of memory.
Claude Code needs roughly 512MB of free memory to install. Free up memory, then run this script again.
```

Для любого другого фатального сигнала, а также для кода выхода 137 на macOS скрипт выводит `Installation was killed before it could finish (exit code <N>)` с фактическим кодом выхода и опускает объяснение о нехватке памяти. Это сообщение исходит от скрипта установки, который используют macOS и Linux, и он также охватывает установки внутри WSL; нативные скрипты установки для Windows никогда его не выводят. До v2.1.200 скрипт завершался, выводя лишь голую строку оболочки `Killed`.

**Что делать:**

* Остановите другие процессы, чтобы освободить память, затем снова запустите установщик
* Добавьте пространство подкачки или перейдите на более крупный экземпляр. Команды для файла подкачки см. в разделе [Install killed on low-memory Linux servers](#install-killed-on-low-memory-linux-servers).

### Install hangs in Docker

При установке Claude Code в контейнер Docker установка от root в `/` может вызвать зависания.

**Решения:**

1. **Задайте рабочий каталог** перед запуском установщика. При запуске из `/` установщик сканирует всю файловую систему, что вызывает чрезмерное использование памяти. Установка `WORKDIR` ограничивает сканирование небольшим каталогом:
   ```dockerfile theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Выделите Docker больше памяти**, если используете Docker Desktop. Контейнеры сборки разделяют память, выделенную виртуальной машине Docker Desktop, поэтому откройте **Settings > Resources** в Docker Desktop, увеличьте лимит памяти и снова запустите сборку.

### `Raw mode is not supported` during install

Когда [настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md) вашей организации включают изменения, которые требуют [подтверждения безопасности](https://code.claude.com/docs/ru/server-managed-settings.md#security-approval-dialogs), версии Claude Code до 2.1.246 пытаются показать диалог подтверждения во время `claude install`. Диалогу нужен терминал на stdin. Когда установщик запускает `claude install` из канала, как это делает `curl -fsSL https://claude.ai/install.sh | bash`, stdin — это канал, а не терминал, поэтому установка завершается ошибкой, содержащей `Raw mode is not supported`.

Claude Code v2.1.246 и более поздние версии не показывают диалог во время `claude install` или `claude update`. Команда запускается с настройками, которые вы подтвердили в последний раз, и Claude Code показывает диалог в вашей следующей интерактивной сессии. Если конфигурация запуска вашей организации [ожидает получения настроек](https://code.claude.com/docs/ru/server-managed-settings.md#enforce-fail-closed-startup), например когда она задаёт `forceRemoteSettingsRefresh`, диалог всё ещё появляется во время этих команд, и установка, запущенная из канала, всё ещё завершается ошибкой.

В любой другой конфигурации повторный запуск установщика позволяет обойти эту ошибку, потому что скрипт запускает команду `install` последнего выпуска, даже когда вы просите его установить более старую версию. Снова запустите команду для вашей платформы:

> [tab] macOS/Linux
>
> ```bash theme={null}
> curl -fsSL https://claude.ai/install.sh | bash
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> irm https://claude.ai/install.ps1 | iex
> ```

`claude --version` выводит версию, установленную при повторном запуске.

### `claude update` or `claude doctor` hangs

`claude update` и `claude doctor` сканируют ваши файлы конфигурации оболочки на предмет устаревшего псевдонима `claude`: `~/.zshrc`, `~/.bashrc` и `~/.config/fish/config.fish`, плюс на macOS первый существующий из `~/.bash_profile`, `~/.bash_login` или `~/.profile`. Если вы задали `ZDOTDIR`, файлом Zsh вместо этого является `$ZDOTDIR/.zshrc`. Когда один из этих путей является каталогом, Claude Code пропускает его, и обе команды завершаются нормально. До v2.1.214 каталог по одному из этих путей заставлял обе команды зависать и оставлял раздел System diagnostics в `/status` пустым. `claude doctor` зависал без вывода; `claude update` зависал сразу после вывода `Checking for updates`.

Если вы столкнулись с зависанием на более ранней версии, найдите каталог. В выводе этой команды строка, начинающаяся с `d`, отмечает этот путь как каталог. Строка `No such file or directory` означает, что по этому пути ничего не существует и он не является причиной:

```bash theme={null}
ls -ld ~/.zshrc ~/.bashrc ~/.bash_profile ~/.bash_login ~/.profile ~/.config/fish/config.fish
```

Переместите каталог в другое место или обновитесь до v2.1.214 или более поздней версии. Так как `claude update` зависает на затронутых версиях, обновитесь вместо этого, повторно запустив [скрипт установки](https://code.claude.com/docs/ru/setup.md#install-claude-code).

### Claude Desktop overrides the `claude` command on Windows

Если вы установили старую версию Claude Desktop, она может зарегистрировать `Claude.exe` в каталоге `WindowsApps`, который имеет приоритет в PATH над Claude Code CLI. Запуск `claude` открывает приложение Desktop вместо CLI.

Обновите Claude Desktop до последней версии, чтобы исправить эту проблему.

### Claude Code on Windows requires either Git for Windows (for bash) or PowerShell

Git for Windows является опциональным. Claude Code использует [инструмент PowerShell](https://code.claude.com/docs/ru/tools-reference.md#powershell-tool) при отсутствии Git Bash, поэтому эта ошибка означает, что ни одна оболочка не была найдена.

**Если PowerShell отсутствует в вашем PATH**, его местоположение по умолчанию — `C:\Windows\System32\WindowsPowerShell\v1.0\`. Добавьте этот каталог в ваш `PATH` или установите [PowerShell 7](https://aka.ms/powershell), который предоставляет `pwsh`.

**Чтобы вместо этого установить Git for Windows**, загрузите его с [git-scm.com/downloads/win](https://git-scm.com/downloads/win). Во время установки выберите "Add to PATH." Перезапустите терминал после установки. Его установка включает инструмент Bash, полезный при работе со скриптами и инструментами на основе Bash.

**Если Git уже установлен**, но Claude Code не может его найти, сравните его местоположение с местами, которые Claude Code проверяет. Когда `CLAUDE_CODE_GIT_BASH_PATH` не задан, Claude Code ищет `bash.exe` в этом порядке:

1. Местоположения установки по умолчанию `C:\Program Files\Git` и `C:\Program Files (x86)\Git`.
2. `git` в вашем `PATH`, используя `bin\bash.exe` из этой установки Git.

На шаге 2 Claude Code пропускает `git`, который находится в папке, из которой вы запустили Claude Code, или ниже неё в пути, который содержит `node_modules` или папку виртуального окружения, такую как `.venv` или `env`, например `C:\dev\env\myproject\Git`, когда вы запустили из `C:\dev\env\myproject`. Это предотвращает запуск Claude Code исполняемого файла, который туда поместил проект. Если ваш Git находится в подобном месте, укажите на него в `CLAUDE_CODE_GIT_BASH_PATH`.

**Чтобы указать Claude Code на конкретную установку Git**, найдите её, запустив `where.exe git` в PowerShell, затем задайте путь `bin\bash.exe` из этой установки как `CLAUDE_CODE_GIT_BASH_PATH` в вашем [файле settings.json](https://code.claude.com/docs/ru/settings.md):

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**Если `CLAUDE_CODE_GIT_BASH_PATH` указывает на правильный путь и файл существует**, но Claude Code всё ещё не использует его, сначала проверьте имя файла. Claude Code принимает только файл с именем `bash.exe`, `sh.exe`, `bash` или `sh`; при любом другом имени, например у лаунчера `git-bash.exe` из Git for Windows, он игнорирует переменную и автоматически определяет Git Bash, как если бы она не была задана, записывая в журнал предупреждение, видимое с `--debug`. Несуществующий путь приводит к тому же резервному варианту и предупреждению. До v2.1.219 Claude Code использовал любой существующий файл как оболочку без проверки его имени и завершался при запуске с `Claude Code was unable to find CLAUDE_CODE_GIT_BASH_PATH path`, когда путь не существовал.

Если имя файла правильное, может вмешиваться программное обеспечение для защиты эндпоинтов, такое как AppLocker, политики ограничения программного обеспечения Group Policy или агенты EDR. Попросите вашу IT-команду добавить в список разрешённых `claude.exe` и порождаемые им процессы, включая `cmd.exe` и `bash.exe`, в вашей политике защиты эндпоинтов.

### Claude Code does not support 32-bit Windows

Windows включает две записи PowerShell в меню Start: `Windows PowerShell` и `Windows PowerShell (x86)`. Запись x86 запускается как 32-битный процесс и вызывает эту ошибку даже на 64-битной машине. Чтобы проверить, какой у вас случай, запустите это в том же окне, в котором возникла ошибка:

```powershell theme={null}
[Environment]::Is64BitOperatingSystem
```

Если это выводит `True`, ваша операционная система в порядке. Закройте окно, откройте `Windows PowerShell` без суффикса x86 и запустите команду установки снова.

Если это выводит `False`, вы используете 32-битное издание Windows. Claude Code требует 64-битную операционную систему. См. [системные требования](https://code.claude.com/docs/ru/setup.md#system-requirements).

### Linux musl or glibc binary mismatch

Если вы видите ошибки об отсутствующих общих библиотеках вроде `ld-linux-x86-64.so.2` или `ld-linux-aarch64.so.1` после установки, установщик мог загрузить неправильный вариант бинарного файла для вашей системы.

```text theme={null}
Error loading shared library ld-linux-x86-64.so.2: No such file or directory
```

**Решения:**

1. **Проверьте, какой libc использует ваша система**:
   ```bash theme={null}
   ldd --version 2>&1 | head -1
   ```
   Вывод, упоминающий `GNU libc` или `GLIBC`, означает glibc. Вывод, упоминающий `musl`, означает musl.

2. **Если вы на glibc, но получили бинарный файл musl**, удалите установку и переустановите. Вы также можете вручную загрузить правильный бинарный файл, используя манифест в `https://downloads.claude.ai/claude-code-releases/{VERSION}/manifest.json`. Создайте [GitHub issue](https://github.com/anthropics/claude-code/issues) с выводом `ldd --version` и `ls /lib/libc.musl*`.

3. **Если вы на musl, но получили бинарный файл glibc**, [удалите установку](https://code.claude.com/docs/ru/setup.md#uninstall-claude-code). На Alpine Linux сначала установите пакеты, перечисленные в разделе [Alpine Linux setup](https://code.claude.com/docs/ru/setup.md#alpine-linux-and-musl-based-distributions). Затем выполните [команду установки](https://code.claude.com/docs/ru/setup.md#install-claude-code), которая установит бинарный файл musl.

### `Illegal instruction`

Если запуск `claude` или установщика выводит `Illegal instruction`, нативный бинарный файл использует инструкции CPU, которые ваш процессор не поддерживает. Есть две отдельные причины.

**Несоответствие архитектуры.** Установщик загрузил неправильный бинарный файл, например x86 на ARM-сервере. Проверьте с помощью `uname -m` на macOS или Linux или `$env:PROCESSOR_ARCHITECTURE` в PowerShell. Если результат не совпадает с полученным вами бинарным файлом, [создайте GitHub issue](https://github.com/anthropics/claude-code/issues) с выводом.

**Отсутствующий набор инструкций AVX.** Если ваша архитектура правильная, но вы всё ещё видите `Illegal instruction`, ваш CPU вероятно не поддерживает AVX или другую инструкцию, которую требует бинарный файл. Это затрагивает примерно процессоры Intel и AMD до 2013 года, а также виртуальные машины, где гипервизор не передаёт AVX гостю.

На VPS или VM запустите `grep -m1 -ow avx /proc/cpuinfo`; пустой результат означает, что AVX недоступен гостю.

Обходного пути для нативного бинарного файла нет; следите за статусом в [issue #50384](https://github.com/anthropics/claude-code/issues/50384) и при сообщении о проблеме указывайте модель вашего CPU из `grep -m1 "model name" /proc/cpuinfo` на Linux или `sysctl -n machdep.cpu.brand_string` на macOS.

Альтернативные методы установки загружают тот же нативный бинарный файл и не устранят ни одну из причин.

### `dyld: cannot load` on macOS

Если вы видите `dyld: Symbol not found`, `dyld: cannot load` или `Abort trap: 6` во время установки, бинарный файл несовместим с вашей версией macOS или оборудованием.

Ошибка `Symbol not found`, которая ссылается на `libicucore`, означает, что ваша версия macOS старше, чем поддерживает бинарный файл:

```text theme={null}
dyld: Symbol not found: _ubrk_clone
  Referenced from: claude-darwin-x64 (which was built for Mac OS X 13.0)
  Expected in: /usr/lib/libicucore.A.dylib
```

Загрузчик может вместо этого отклонить команды загрузки бинарного файла, что также означает, что ваша версия macOS слишком старая:

```text theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Решения:**

1. **Проверьте вашу версию macOS**: Claude Code требует macOS 13.0 или более позднюю версию. Откройте меню Apple и выберите About This Mac, чтобы проверить вашу версию.

2. **Обновите macOS**, если у вас старая версия. Бинарный файл использует команды загрузки и системные библиотеки, которые старые версии macOS не поддерживают. Альтернативные методы установки, такие как Homebrew, загружают тот же бинарный файл и не устранят эту ошибку.

### `Bus error` while a session is running

Если запущенная сессия завершается и ваша оболочка выводит `Bus error`, одна из возможных причин в том, что Claude Code больше не мог прочитать собственный исполняемый файл с диска. Например, во время работы сессии файл был усечён или удалён в сетевом хранилище.

Перед сообщением оболочки среда выполнения Claude Code может вывести отчёт о сбое, который включает `panic(main thread): Bus error at address` и `oh no: Bun has crashed. This indicates a bug in Bun, not your code.` Если исполняемый файл стал нечитаемым, сбой вызван нечитаемым файлом, а не ошибкой в Bun. Отчёт также может отсутствовать, если среда выполнения не смогла прочитать и код, который его выводит.

Чтобы продолжить, начните новую сессию. Если Claude Code установлен в сетевом хранилище, следуйте инструкциям из раздела [Установка в сетевое хранилище](https://code.claude.com/docs/ru/setup.md#install-on-network-storage), чтобы обновления не удаляли бинарный файл, который всё ещё нужен запущенным сессиям.

### `Exec format error` on WSL1

Если запуск `claude` в WSL выводит `cannot execute binary file: Exec format error`, вы используете WSL1 и столкнулись с известной регрессией нативного бинарного файла, отслеживаемой в [issue #38788](https://github.com/anthropics/claude-code/issues/38788). Заголовки программы бинарного файла изменились таким образом, что загрузчик WSL1 не может их обработать.

Самое чистое исправление — преобразовать ваш дистрибутив в WSL2 из PowerShell:

```powershell theme={null}
wsl --set-version <DistroName> 2
```

Если вам нужно оставаться на WSL1, вызывайте бинарный файл через динамический компоновщик. Добавьте эту функцию в `~/.bashrc` внутри WSL, заменив путь, если ваш домашний каталог отличается:

```bash theme={null}
claude() {
  /lib64/ld-linux-x86-64.so.2 "$(readlink -f "$HOME/.local/bin/claude")" "$@"
}
```

Затем запустите `source ~/.bashrc` и повторите `claude`.

### npm install errors in WSL

Эти проблемы актуальны, если вы установили Claude Code с помощью `npm install -g` внутри WSL. Если вы использовали [нативный установщик](https://code.claude.com/docs/ru/setup.md), пропустите этот раздел. На npm 12 выполняйте установку так, как описано в разделе [Исправление установки через npm 12](#fix-an-npm-12-install).

**Проблемы определения ОС или платформы.** Если npm сообщает о несоответствии платформы во время установки, сначала запустите `npm config set os linux`, затем установите с помощью `npm install -g @anthropic-ai/claude-code@latest --force`. Не используйте `sudo`.

**`exec: node: not found` при запуске `claude`.** Ваша среда WSL вероятно использует установку Node.js для Windows. Проверьте с помощью `which npm` и `which node`: пути, начинающиеся с `/mnt/c/`, — это бинарные файлы Windows, в то время как пути Linux начинаются с `/usr/`. Чтобы исправить это, установите Node через менеджер пакетов вашего дистрибутива Linux или через [`nvm`](https://github.com/nvm-sh/nvm).

**Конфликты версий nvm.** Если у вас установлен nvm как в WSL, так и в Windows, переключение версий Node в WSL может сломаться, потому что WSL импортирует Windows PATH по умолчанию и Windows nvm имеет приоритет. Наиболее распространённая причина — nvm не загружен в вашей оболочке. Добавьте загрузчик nvm в `~/.bashrc` или `~/.zshrc`:

```bash theme={null}
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Или загрузите его в вашей текущей сессии:

```bash theme={null}
source ~/.nvm/nvm.sh
```

Если nvm загружен, но пути Windows всё ещё имеют приоритет, явно добавьте ваш путь Linux Node в начало:

```bash theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

> [!WARNING]
>
> Избегайте отключения импорта Windows PATH через `appendWindowsPath = false`, так как это нарушает возможность вызывать исполняемые файлы Windows из WSL. Аналогично, избегайте удаления Node.js из Windows, если вы используете его для разработки под Windows.

### Permission errors during installation

Если нативный установщик завершается ошибками прав доступа, целевой каталог может быть недоступен для записи. См. [Проверка прав доступа к каталогу](#check-directory-permissions).

Если вы ранее установили через npm и получаете ошибки прав доступа, специфичные для npm, переключитесь на нативный установщик:

```bash theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

### Native binary not found after npm install

Пакет npm `@anthropic-ai/claude-code` загружает нативный бинарный файл как опциональную зависимость для конкретной платформы, например `@anthropic-ai/claude-code-darwin-arm64`. `claude` остаётся скриптом-заполнителем, пока не выполнится шаг postinstall пакета `@anthropic-ai/claude-code`, который заменяет заполнитель этим бинарным файлом. Если либо загрузка, либо шаг postinstall пропущены, заполнитель остаётся на месте, и запуск `claude` на macOS и Linux выводит:

```text theme={null}
Error: claude native binary not installed.

Either postinstall did not run (--ignore-scripts, some pnpm configs)
or the platform-native optional dependency was not downloaded
(--omit=optional).

Run the postinstall manually (adjust path for local vs global install):
  node node_modules/@anthropic-ai/claude-code/install.cjs

Or reinstall without --ignore-scripts / --omit=optional.
```

На Windows `bin/claude.exe` — это тот же скрипт-заполнитель оболочки, а не реальный исполняемый файл, поэтому PowerShell и CMD вместо вывода этого сообщения сообщают, что не могут запустить файл.

Проверьте следующие причины:

* **npm 12 по умолчанию пропускает шаг postinstall.** Когда вы устанавливаете или обновляете Claude Code с помощью npm 12, npm всё равно завершает установку, не выполняя этот шаг. См. [Исправление установки через npm 12](#fix-an-npm-12-install).
* **Опциональные зависимости отключены.** Удалите `--omit=optional` из вашей команды npm install, `--no-optional` из pnpm или `--ignore-optional` из yarn и проверьте, что `.npmrc` не задаёт `optional=false`. Затем переустановите. Нативный бинарный файл поставляется только как опциональная зависимость, поэтому резервного варианта на JavaScript при её пропуске нет, и повторный запуск `install.cjs` не может поместить на место бинарный файл, который никогда не был загружен.
* **Скрипты установки отключены.** `--ignore-scripts` и некоторые конфигурации pnpm пропускают шаг postinstall, но всё равно загружают пакет платформы. Запустите `node node_modules/@anthropic-ai/claude-code/install.cjs`, как предлагает сообщение, или переустановите без флага. Если postinstall вообще не может запуститься в вашей среде, `node node_modules/@anthropic-ai/claude-code/cli-wrapper.cjs` находит загруженный пакет и запускает его ценой дополнительного процесса Node при каждом запуске. Если обёртка вместо этого выводит `Could not find native binary package`, пакет платформы никогда не был загружен, поэтому сначала устраните описанную выше причину с опциональными зависимостями.
* **Неподдерживаемая платформа.** Предварительно собранные бинарные файлы опубликованы для `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64` и `win32-arm64`. Claude Code не поставляет бинарный файл для других платформ; см. [системные требования](https://code.claude.com/docs/ru/setup.md#system-requirements). На FreeBSD установщик сообщает, что платформа не поддерживается. До v2.1.205 он рассматривал FreeBSD как Linux и загружал бинарный файл, который не мог работать.
* **В корпоративном зеркале npm отсутствуют пакеты платформ.** Убедитесь, что ваш реестр зеркалирует все восемь пакетов платформ `@anthropic-ai/claude-code-*` в дополнение к мета-пакету.

#### Исправление установки через npm 12

Если `claude` выводит `Error: claude native binary not installed.` после установки или обновления через npm либо на Windows оболочка не может его запустить, выполните `npm --version`. Версия, начинающаяся с `12`, означает, что npm пропустил шаг postinstall Claude Code, который помещает бинарный файл на место, если только ваша конфигурация npm не разрешает этот шаг. Для любой другой версии проверьте [другие причины](#native-binary-not-found-after-npm-install).

Чтобы исправить установку через npm 12, переключитесь на нативный установщик или разрешите этот шаг:

* **Переключитесь на нативный установщик**: [установите с помощью нативного установщика](https://code.claude.com/docs/ru/setup.md#install-claude-code), затем [удалите пакет npm](https://code.claude.com/docs/ru/setup.md#uninstall-with-npm). После этого обновления не используют npm, поэтому ошибка не вернётся.
* **Останьтесь на npm**: для глобальной установки через npm добавьте Claude Code в `allow-scripts` в пользовательской конфигурации npm. Тогда npm будет запускать скрипты установки Claude Code при каждой последующей установке и обновлении, а также в установках проектов, чей `package.json` не задаёт `allowScripts`.

  Используйте нативный установщик для локальной установки в `~/.claude/local`. Также используйте его, если скрипты вашего `package.json` вызывают `npm install` и вы запускаете их с помощью pnpm 9, pnpm 10, Yarn 1 или другого инструмента, который передаёт им эту настройку. На npm 12.1 и более поздних версиях такие установки могут завершаться ошибкой `EALLOWSCRIPTS` после сохранения настройки.

  1. Если `npm --version` вывел 12.0.x, обновите npm до 12.1 или более поздней версии, например с помощью `npm install -g npm@latest`. На 12.0.x установки проектов, которые запускает инструмент `npx` или скрипт `npm run`, могут завершаться ошибкой `EALLOWSCRIPTS` после сохранения настройки.

  2. Выполните `npm config get allow-scripts` и запишите все перечисленные пакеты, потому что следующая команда заменяет всё значение целиком. Сохраните настройку, указав эти пакеты внутри кавычек, например `"allow-scripts=@anthropic-ai/claude-code,<package>"`:

     ```bash theme={null}
     npm config set "allow-scripts=@anthropic-ai/claude-code" --location=user
     ```

  3. Переустановите:

     ```bash theme={null}
     npm install -g @anthropic-ai/claude-code@latest
     ```

     Если эта команда или шаг 1 завершается ошибкой `EACCES`, переключитесь на нативный установщик вместо повторного запуска с `sudo`. Claude Code запускает npm без `sudo` при самообновлении, поэтому автоматические обновления завершались бы той же ошибкой.

  4. Если `claude --version` не выводит номер версии, проверьте [другие причины](#native-binary-not-found-after-npm-install).

  Чтобы отменить изменения, снова задайте список без `@anthropic-ai/claude-code` или удалите весь список с помощью `npm config delete allow-scripts --location=user`. На npm 12 ошибка после этого вернётся при следующем обновлении.

### npm `ENOTEMPTY` error during update or reinstall

Когда вы запускаете `npm install -g @anthropic-ai/claude-code@latest` поверх существующей установки, npm может завершиться ошибкой при перемещении старого каталога пакета:

```text theme={null}
npm error code ENOTEMPTY
npm error syscall rename
npm error path /home/you/.nvm/versions/node/v22.13.1/lib/node_modules/@anthropic-ai/claude-code
npm error dest /home/you/.nvm/versions/node/v22.13.1/lib/node_modules/@anthropic-ai/.claude-code-tVWAnUUt
npm error errno -39
npm error ENOTEMPTY: directory not empty, rename '...'
```

Строка `npm error path` называет каталог, который npm не смог переместить. Удалите этот каталог и все оставшиеся рядом с ним каталоги `.claude-code-*`, которые могли остаться после ранее прерванных запусков. Команды ниже находят ваш глобальный каталог пакетов с помощью `npm root -g`; если каталог, который называет строка `npm error path`, не находится внутри каталога, который выводит `npm root -g`, например потому что вы переключили версии Node с помощью nvm, удалите вместо этого каталоги, которые называет ошибка:

> [tab] macOS/Linux
>
> ```bash theme={null}
> rm -rf "$(npm root -g)/@anthropic-ai/claude-code"
> ```
>
> Затем удалите все оставшиеся временные каталоги. Если Zsh выводит `no matches found`, удалять было нечего:
>
> ```bash theme={null}
> rm -rf "$(npm root -g)/@anthropic-ai/.claude-code-"*
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> Remove-Item -Recurse -Force "$(npm root -g)/@anthropic-ai/claude-code", "$(npm root -g)/@anthropic-ai/.claude-code-*"
> ```

Затем переустановите. На npm 12 следуйте инструкциям из раздела [Исправление установки через npm 12](#fix-an-npm-12-install). В противном случае выполните:

```bash theme={null}
npm install -g @anthropic-ai/claude-code@latest
```

Проверьте с помощью `claude --version`, который выводит номер версии, такой как `2.1.211 (Claude Code)`.

## Вход и аутентификация

Эти разделы решают проблемы входа, ошибки OAuth и проблемы с токенами.

### Сброс вашего входа

Когда вход не удаётся и причина не очевидна, чистая повторная аутентификация разрешает большинство случаев:

1. Запустите `/logout`, чтобы полностью выйти
2. Закройте Claude Code
3. Перезагрузитесь с `claude` и завершите процесс аутентификации снова

Если браузер не открывается автоматически во время входа, нажмите `c`, чтобы скопировать URL OAuth в буфер обмена, затем вставьте его в браузер вручную. Это также работает, когда URL переносится на несколько строк в узком или SSH терминале и не может быть нажат напрямую.

### OAuth error: Invalid code

Если вы видите `OAuth error: Invalid code. Please make sure the full code was copied`, код входа истёк или был усечён во время копирования-вставки.

**Решения:**

* Нажмите Enter, чтобы повторить попытку и завершить вход быстро после открытия браузера
* Введите `c`, чтобы скопировать полный URL, если браузер не открывается автоматически
* Если используете удалённую/SSH сессию, браузер может открыться на неправильной машине. Скопируйте URL, отображаемый в терминале, и откройте его в вашем локальном браузере вместо этого.

### 403 Forbidden after login

Если вы видите `API Error: 403 Request not allowed` после входа:

* **Пользователи Claude Pro/Max/Ultra**: проверьте, что ваша подписка активна на [claude.ai/settings](https://claude.ai/settings)
* **Пользователи Anthropic Console**: подтвердите, что ваша учётная запись имеет роль "Claude Code" или "Developer". Администраторы назначают её на странице Members в Console по адресу [platform.claude.com/settings/members](https://platform.claude.com/settings/members).
* **За прокси**: корпоративные прокси могут помешать запросам API. См. [network configuration](https://code.claude.com/docs/ru/network-config.md) для настройки прокси.

### Claude Code access has not been granted for this account

Если страница входа показывает `Authorization failed` с сообщением `Claude Code access has not been granted for this account. Contact your administrator.` после того как вы вошли из Claude Code, ваша организация Claude Enterprise установила вашу роль на Custom и ни одна из [custom roles](https://support.claude.com/en/articles/13930452) назначенных вашим группам не предоставляет Claude Code. На роли Custom вы получаете доступ только из этих пользовательских ролей, поэтому ничего, что вы измените в Claude Code, не разрешит эту ошибку.

Чтобы получить доступ:

1. Попросите владельца вашей организации Claude назначить пользовательскую роль, которая предоставляет доступ Claude Code одной из ваших групп, или изменить вашу роль с Custom на стандартную роль, такую как User. Владельцы управляют ролями в [role settings](https://claude.ai/admin-settings/roles) организации.
2. После того как владелец внесёт изменение, запустите `claude` и войдите снова.

### This organization has been disabled with an active subscription

Если вы видите `API Error: 400 ... "This organization has been disabled"` несмотря на активную подписку Claude, переменная окружения `ANTHROPIC_API_KEY` переопределяет вашу подписку. Это обычно происходит, когда старый API-ключ от предыдущего работодателя или проекта всё ещё установлен в вашем профиле оболочки.

Когда `ANTHROPIC_API_KEY` присутствует и вы его одобрили, Claude Code использует этот ключ вместо учётных данных OAuth вашей подписки. В неинтерактивном режиме с флагом `-p` ключ всегда используется, когда присутствует. См. [authentication precedence](https://code.claude.com/docs/ru/authentication.md#authentication-precedence) для полного порядка разрешения.

Чтобы использовать вашу подписку вместо этого, отмените установку переменной окружения и удалите её из вашего профиля оболочки:

> [tab] macOS/Linux
>
> ```bash theme={null}
> unset ANTHROPIC_API_KEY
> claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> Remove-Item Env:ANTHROPIC_API_KEY
> claude
> ```

Проверьте `~/.zshrc`, `~/.bashrc` или `~/.profile` на строки `export ANTHROPIC_API_KEY=...` и удалите их, чтобы сделать изменение постоянным. На Windows проверьте ваш профиль PowerShell в `$PROFILE` и ваши переменные окружения User на `ANTHROPIC_API_KEY`. Запустите `/status` внутри Claude Code, чтобы подтвердить, какой метод аутентификации активен.

### OAuth login fails in WSL2, SSH, or containers

Если браузер не открывается или браузер выполняет вход, а затем показывает ошибку подключения для адреса `localhost`, вы можете завершить вход, не устраняя ни одну из этих проблем. Вместо этого войдите через отдельный URL входа, который терминал показывает над приглашением для вставки:

**1. Скопируйте URL входа**

В интерактивном приглашении входа нажмите `c`, чтобы скопировать URL, или выделите его в терминале. При использовании `claude auth login` скопируйте URL, который выводит эта команда.

**2. Войдите через этот URL**

Откройте URL в браузере на вашей локальной машине и войдите. После этого браузер покажет код вместо возврата на `localhost`.

**3. Вставьте код**

Вставьте этот код в терминал в приглашение, которое начинается с `Paste code here`.

Если вставка кода в интерактивное приглашение ничего не делает, привязка вставки вашего терминала вероятно не достигает поля ввода. Попробуйте альтернативное сочетание клавиш вставки вашего терминала, часто правый клик или Shift+Insert в Windows Terminal, или используйте `claude auth login` вместо этого, который читает вставленный код из стандартного ввода:

```bash theme={null}
claude auth login
```

Этот резервный вариант также применяется на нативном Windows или любом терминале, где вставка в интерактивное приглашение не удаётся.

В WSL2, если браузер не открылся, вы также можете позволить Claude Code в следующий раз открыть ваш браузер Windows, установив переменную окружения `BROWSER` на путь к этому браузеру:

```bash theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

### Not logged in or token expired

Если Claude Code предлагает вам войти снова после сессии, ваш токен OAuth может истечь.

Запустите `/login`, чтобы повторно аутентифицироваться. Если это происходит часто, проверьте, что ваши системные часы точны, так как валидация токена зависит от правильных временных меток.

Параллельные сессии на одной машине используют общий сохранённый вход и координируют его обновление, так что только один процесс обновляет токен одновременно. О том, что делают другие сессии после того, как вы снова войдёте в одной из них, см. [Not logged in](https://code.claude.com/docs/ru/errors.md#not-logged-in).

До версии 2.1.211 пробуждение машины из режима сна могло привести к тому, что две сессии обновляли один и тот же токен, что отзывало сохранённый вход и предлагало каждой открытой сессии войти снова одновременно.

На macOS Claude Code сохраняет учётные данные в Keychain входа. Когда Keychain отклоняет запись, например когда он заблокирован в SSH сессии или его пароль не синхронизирован с паролем вашей учётной записи, Claude Code сохраняет ваш вход в открытый текстовый файл `~/.claude/.credentials.json` вместо этого. Вход в Console, который создаёт API-ключ, не удаётся до тех пор, пока Keychain снова не станет доступным для записи.

Чтобы сделать Keychain доступным для записи снова и переместить ваш вход обратно в зашифрованный Keychain:

**1. Проверьте доступ Keychain**

Запустите `claude doctor`, чтобы проверить доступ Keychain. Когда Keychain отклоняет запись, отчёт содержит предупреждение, которое начинается с `macOS Keychain is not writable`, за которым следует предложенное исправление. Когда отчёт не содержит предупреждение Keychain, Keychain доступен для записи и вы можете перейти к последнему шагу.

**2. Разблокируйте Keychain**

```bash theme={null}
security unlock-keychain ~/Library/Keychains/login.keychain-db
```

Введите пароль Keychain, когда команда его запросит, затем запустите `claude doctor` снова. Когда разблокировка сработала, отчёт больше не содержит предупреждение Keychain.

**3. Пересинхронизируйте пароль Keychain, если разблокировка не помогает**

Откройте Keychain Access, выберите keychain `login` и выберите **Edit > Change Password for Keychain "login"**, чтобы пересинхронизировать его с паролем вашей учётной записи. Затем запустите `claude doctor` снова. Переходите к следующему шагу, когда отчёт больше не содержит предупреждение Keychain.

**4. Выйдите и войдите снова**

Когда Keychain снова доступен для записи, Claude Code перемещает учётные данные обратно при следующей записи учётных данных. Чтобы сделать это сейчас, запустите `/logout` и затем `/login`. Выход удаляет все сохранённые учётные данные, включая содержимое открытого текстового файла, сохранённые входы MCP-серверов и значения секретов плагинов, поэтому ожидайте повторной авторизации MCP-серверов и повторного ввода секретов плагинов после этого. Вход снова сохраняет ваш вход в Keychain.

#### Вход не удаётся при домашнем каталоге в сети

Когда запрос завершается ошибкой `API Error: 401`, а ваш [каталог конфигурации](https://code.claude.com/docs/ru/claude-directory.md) находится в сетевой файловой системе, проверьте, не заполнена ли эта файловая система или ваша квота в ней. Если места не осталось, Claude Code не может сохранить новый или обновлённый вход в открытый текстовый [файл `.credentials.json`](https://code.claude.com/docs/ru/authentication#credential-management), при этом `claude auth login` всё равно может вывести `Login successful.`

**1. Освободите место в файловой системе**

Удалите ненужные файлы в файловой системе, где находится `~/.claude` или каталог, заданный в [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars).

**2. Войдите снова**

Запустите `/login` в промпте Claude Code или `claude auth login` в вашей оболочке.

До версии 2.1.318, когда Claude Code сохранял файл входа в заполненной сетевой файловой системе, он мог заменить ещё действительный сохранённый вход пустым файлом. После этого последующие команды сообщали `Not logged in`.

### Bedrock, Agent Platform, or Foundry credentials not loading

Если вы настроили Claude Code для использования облачного провайдера и видите `Could not load credentials from any providers` на Amazon Bedrock, `Could not load the default credentials` на Google Cloud's Agent Platform или `ChainedTokenCredential authentication failed` на Microsoft Foundry, ваш CLI облачного провайдера вероятно не аутентифицирован в текущей оболочке.

Для Amazon Bedrock подтвердите, что ваши учётные данные AWS действительны:

```bash theme={null}
aws sts get-caller-identity
```

Для Google Cloud's Agent Platform подтвердите, что `ANTHROPIC_VERTEX_PROJECT_ID` и `CLOUD_ML_REGION` установлены в вашей оболочке, затем установите учётные данные приложения по умолчанию:

```bash theme={null}
gcloud auth application-default login
```

Для Microsoft Foundry подтвердите, что `ANTHROPIC_FOUNDRY_API_KEY` установлен, или войдите с Azure CLI, чтобы цепь учётных данных по умолчанию могла найти вашу учётную запись:

```bash theme={null}
az login
```

Если учётные данные работают в вашем терминале, но не в расширении VS Code или JetBrains, процесс IDE вероятно не унаследовал вашу среду оболочки. Установите переменные окружения провайдера в собственных настройках IDE или запустите IDE из терминала, где они уже экспортированы.

См. [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md) или [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md) для полной настройки провайдера.

## Still stuck

Если ничего из вышеперечисленного не разрешает вашу проблему:

1. Проверьте [GitHub repository](https://github.com/anthropics/claude-code/issues) на известные проблемы или откройте новую с вашей операционной системой, командой установки, которую вы запустили, и полным выводом ошибки
2. Если `claude --version` работает, но что-то ещё не так, запустите `claude doctor` для автоматического диагностического отчёта
3. Если вы можете запустить сессию, используйте `/feedback` внутри Claude Code, чтобы сообщить о проблеме
4. Если проблема связана с вашей учётной записью, а не с установкой, например с циклом входа, неузнанной подпиской или отключённой организацией, свяжитесь с поддержкой Anthropic: войдите на [claude.ai](https://claude.ai) (пользователи Console: [platform.claude.com](https://platform.claude.com)), нажмите на ваши инициалы в нижнем левом углу и выберите **Get help**. Полный процесс см. в разделе [How to get support](https://support.claude.com/en/articles/9015913-how-to-get-support).
