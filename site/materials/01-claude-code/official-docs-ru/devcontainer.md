> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Контейнеры разработки

> Запустите Claude Code внутри контейнера разработки для согласованных, изолированных сред во всей вашей команде.

[Контейнер разработки](https://containers.dev/), или dev container, позволяет вам определить идентичную, изолированную среду, которую каждый инженер в вашей команде может запустить. С установленным Claude Code в этом контейнере команды, которые запускает Claude, выполняются внутри него, а не на хост-машине, при этом редактирование файлов вашего проекта отображается в локальном репозитории по мере работы.

На этой странице рассматривается [установка Claude Code в контейнер разработки](#add-claude-code-to-your-dev-container), а затем набор самостоятельных тем конфигурации: сохранение аутентификации при перестроении, применение политики организации, ограничение исходящего сетевого трафика и запуск без запросов разрешений. Прочитайте те, которые соответствуют вашей конфигурации.

> [!WARNING]
>
> Хотя контейнер разработки обеспечивает существенную защиту, ни одна система полностью не защищена от всех атак.
> При выполнении с `--dangerously-skip-permissions` контейнеры разработки не предотвращают утечку данных из вредоносного проекта, включая учетные данные Claude Code, хранящиеся в [`~/.claude`](https://code.claude.com/docs/ru/claude-directory).
> Используйте контейнеры разработки только при разработке с доверенными репозиториями и отслеживайте деятельность Claude.
> Избегайте монтирования хост-секретов, таких как `~/.ssh` или файлы облачных учетных данных, в контейнер; предпочитайте токены с областью действия репозитория или краткосрочные токены.

> [accordion] Как контейнеры разработки работают с вашим редактором
>
> ![Диаграмма, показывающая редактор на хосте, подключающийся к Docker контейнеру разработки. Claude Code, терминал и инструменты сборки работают внутри контейнера. Репозиторий хоста привязан к контейнеру как рабочее пространство.](https://mintcdn.com/claude-code/YvJyjZfd9yMihr0i/images/devcontainer-architecture.svg?fit=max\&auto=format\&n=YvJyjZfd9yMihr0i\&q=85\&s=9017b1d16a446c6cc37ba562f35b9aae)
>
> Контейнер разработки работает как Docker контейнер, либо на вашей машине, либо на облачном хосте, таком как GitHub Codespaces. Редактор, поддерживающий спецификацию Dev Containers, такой как VS Code, GitHub Codespaces, JetBrains IDE или Cursor, подключается к этому контейнеру: вы просматриваете и редактируете файлы в редакторе как обычно, но интегрированный терминал, языковые серверы и инструменты сборки все работают внутри контейнера, а не на вашем хосте. Редакторы без поддержки контейнеров разработки, такие как простой Vim, не являются частью этого рабочего процесса.
>
> Claude Code работает внутри контейнера, поэтому он видит те же файлы, зависимости и инструменты, что и остальная часть цепочки инструментов вашего проекта. В VS Code вы можете использовать либо [панель расширения Claude Code](https://code.claude.com/docs/ru/vs-code.md), либо запустить `claude` в интегрированном терминале; оба работают внутри контейнера и используют одну и ту же конфигурацию `~/.claude`.

## Добавление Claude Code в контейнер разработки

Claude Code устанавливается в любой контейнер разработки через [Claude Code Dev Container Feature](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code).

Параметры работают с любым инструментом, поддерживающим спецификацию Dev Containers, таким как VS Code, GitHub Codespaces или JetBrains IDEs. Шаги ниже используют VS Code в качестве примера.

Когда вы открываете контейнер в VS Code или Codespaces, функция также добавляет расширение Claude Code VS Code; другие редакторы игнорируют эту часть.

> [!TIP]
>
> Новичок в контейнерах разработки? [Учебное пособие VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/tutorial) проходит через установку Docker, расширения и открытие вашего первого контейнера. Для более полного усиленного примера с брандмауэром и постоянными томами см. [Попробуйте контейнер-образец](#try-the-reference-container).

**1. Создание или обновление devcontainer.json**

Сохраните следующее как `.devcontainer/devcontainer.json` в вашем репозитории или добавьте блок `features` в ваш существующий файл.

Тег версии в конце, такой как `:1.0`, закрепляет скрипт установки функции, а не выпуск Claude Code. Функция устанавливает последнюю версию Claude Code, и Claude Code автоматически обновляется внутри контейнера по умолчанию.

Чтобы закрепить версию CLI или отключить автоматическое обновление, см. [Применение политики организации](#enforce-organization-policy).

```json .devcontainer/devcontainer.json theme={null}
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {}
  }
}
```

Замените строку `image` на базовый образ вашего проекта или удалите ее, если ваш существующий файл использует Dockerfile.

Функция Claude Code устанавливает Node.js сама, когда базовый образ его не предоставляет. Если эта установка не удается и сборка останавливается с `Failed to install Node.js and npm`, добавьте `"ghcr.io/devcontainers/features/node:1": {}` в блок `features` выше функции Claude Code и перестройте.

**2. Перестроение контейнера**

Откройте палитру команд VS Code с помощью `Cmd+Shift+P` на Mac или `Ctrl+Shift+P` на Windows и Linux и запустите **Dev Containers: Rebuild Container**.

Для других инструментов следуйте действию перестроения этого инструмента: см. [перестроение в GitHub Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace), [Dev Containers CLI](https://github.com/devcontainers/cli) или документацию контейнеров разработки вашей IDE.

**3. Вход в Claude Code**

Откройте терминал в перестроенном контейнере и запустите `claude`, затем следуйте подсказке аутентификации.

То, что вы видите в подсказке аутентификации, зависит от вашего поставщика:

* **Anthropic**: вход через браузер с вашей учетной записью Claude или Anthropic Console
* **[Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry](https://code.claude.com/docs/ru/third-party-integrations.md)**: Claude Code использует учетные данные вашего облачного поставщика без подсказки браузера

Для облачных поставщиков передавайте учетные данные в контейнер как переменные окружения через `containerEnv`, секрет Codespaces или удостоверение рабочей нагрузки вашего облака, а не монтируйте файлы учетных данных с хоста. См. [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md) или [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md) для цепочки учетных данных, которую читает Claude Code.

См. [Выбор поставщика API](https://code.claude.com/docs/ru/admin-setup.md#choose-your-api-provider), чтобы решить, какой путь подходит вашей организации.

> [!NOTE]
>
> Для входа через Anthropic: если браузер не открывается или выполняет вход, а затем показывает ошибку подключения к `localhost`, используйте URL для входа, показанный над запросом на вставку кода в терминале. Скопируйте его в браузер, выполните вход там, затем вставьте код, показанный браузером, в этот запрос. Если вставка ничего не делает, см. [OAuth login fails in WSL2, SSH, or containers](https://code.claude.com/docs/ru/troubleshoot-install.md#oauth-login-fails-in-wsl2-ssh-or-containers).

## Сохранение аутентификации и параметров при перестроении

По умолчанию домашний каталог контейнера отбрасывается при перестроении, поэтому инженеры должны снова входить каждый раз. Claude Code хранит свой токен аутентификации, настройки пользователя и историю сессий в каталоге [`~/.claude`](https://code.claude.com/docs/ru/claude-directory). Данные вашей учетной записи, личные MCP-серверы и доверие для каждого проекта он хранит в отдельном файле вне этого каталога: [`~/.claude.json`](https://code.claude.com/docs/ru/settings-reference#global-config-settings).

Чтобы сохранить и каталог, и файл, смонтируйте именованный том в `~/.claude` и установите [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars) на тот же путь, чтобы Claude Code писал `.claude.json` внутри тома. Следующий пример монтирует том и устанавливает `CLAUDE_CONFIG_DIR` для контейнера, чей `remoteUser` — это `node`:

```json devcontainer.json theme={null}
"mounts": [
  "source=claude-code-config,target=/home/node/.claude,type=volume"
],
"containerEnv": {
  "CLAUDE_CONFIG_DIR": "/home/node/.claude"
}
```

Замените `/home/node` на домашний каталог `remoteUser` вашего контейнера. Если вы уже установили `containerEnv`, например в [Enforce organization policy](#enforce-organization-policy), добавьте `CLAUDE_CONFIG_DIR` в этот объект вместо добавления второго.

> [!NOTE]
>
> Если Claude Code повторяет первоначальную настройку после каждого перестроения, несмотря на смонтированный том, убедитесь, что `containerEnv` в `devcontainer.json` устанавливает `CLAUDE_CONFIG_DIR` на путь монтирования тома. Без `CLAUDE_CONFIG_DIR` файл `~/.claude.json` остается в домашнем каталоге и отбрасывается при перестроении вместе с записью о том, что вы завершили настройку.

Чтобы изолировать состояние для каждого проекта, а не делиться одним томом во всех репозиториях, включите переменную `${devcontainerId}` в имя источника. [Справочная конфигурация](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json) использует `source=claude-code-config-${devcontainerId}` для этой цели.

В GitHub Codespaces `~/.claude` сохраняется при остановке и запуске codespace, но очищается при перестроении контейнера, поэтому конфигурация выше применяется и там.

Чтобы перенести аутентификацию между codespaces, сохраните `ANTHROPIC_API_KEY` или `CLAUDE_CODE_OAUTH_TOKEN` из [`claude setup-token`](https://code.claude.com/docs/ru/authentication#generate-a-long-lived-token) как [секрет Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces). Codespaces автоматически делает секреты доступными как переменные окружения внутри контейнера.

## Применение политики организации

Контейнер разработки — это удобное место для применения политики организации, потому что один и тот же образ и конфигурация работают на машине каждого инженера.

Claude Code читает `/etc/claude-code/managed-settings.json` на Linux и применяет его с наивысшим приоритетом в [иерархии параметров](https://code.claude.com/docs/ru/settings.md#settings-precedence), поэтому значения там переопределяют все, что инженер устанавливает в `~/.claude` или в каталоге `.claude/` проекта. Скопируйте файл на место из вашего Dockerfile:

```dockerfile Dockerfile theme={null}
RUN mkdir -p /etc/claude-code
COPY managed-settings.json /etc/claude-code/managed-settings.json
```

Поскольку Dockerfile находится в репозитории, любой, у кого есть доступ на запись, может изменить или удалить этот шаг. Для политики, которую инженеры не могут обойти, редактируя файлы репозитория, доставляйте управляемые параметры через [параметры, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md) или ваш MDM вместо этого. См. [файлы управляемых параметров](https://code.claude.com/docs/ru/managed-settings.md#delivery-mechanisms) для доступных ключей и других путей доставки.

Чтобы установить [переменные окружения](https://code.claude.com/docs/ru/env-vars.md), которые применяются к каждому сеансу Claude Code в контейнере, добавьте их в `containerEnv` в вашем `devcontainer.json`. Следующий пример отказывается от телеметрии и отчетов об ошибках и предотвращает автоматическое обновление Claude Code после установки:

```json devcontainer.json theme={null}
"containerEnv": {
  "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
  "DISABLE_AUTOUPDATER": "1"
}
```

`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` также отключает оценку флагов функций, от которых зависят [Remote Control](https://code.claude.com/docs/ru/remote-control.md#requirements) и другие [функции, требующие получения флагов функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), поэтому сеансы в контейнере не могут их использовать.

Функция Dev Container Feature всегда устанавливает последний выпуск Claude Code. Чтобы закрепить определенную версию Claude Code для воспроизводимых сборок, установите ее из вашего Dockerfile с помощью `npm install -g @anthropic-ai/claude-code@X.Y.Z` вместо использования функции и установите `DISABLE_AUTOUPDATER` в `1` в `containerEnv`.

Для полного списка элементов управления политикой, включая правила разрешений, ограничения инструментов и списки разрешений серверов MCP, см. [Настройка Claude Code для вашей организации](https://code.claude.com/docs/ru/admin-setup.md).

Чтобы сделать [серверы MCP](https://code.claude.com/docs/ru/mcp.md) доступными внутри контейнера, определите их в [области проекта](https://code.claude.com/docs/ru/mcp.md#mcp-installation-scopes) в файле `.mcp.json` в корне репозитория, чтобы они были зарегистрированы вместе с конфигурацией контейнера разработки. Установите любые двоичные файлы, от которых зависят локальные серверы stdio, в вашем Dockerfile и добавьте домены удаленных серверов в ваш список разрешений сети.

## Ограничение исходящего сетевого трафика

Вы можете ограничить исходящий трафик контейнера только доменами, которые нужны Claude Code. См. [Требования к сетевому доступу](https://code.claude.com/docs/ru/network-config.md#network-access-requirements) для доменов вывода и аутентификации и [Услуги телеметрии](https://code.claude.com/docs/ru/data-usage.md#telemetry-services) для дополнительных соединений телеметрии и отчетов об ошибках и способов их отключения.

Контейнер-образец включает скрипт [`init-firewall.sh`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh), который ограничивает исходящий трафик только пунктам назначения, которые разрешает скрипт. Запуск брандмауэра внутри контейнера требует дополнительных разрешений, поэтому образец добавляет возможности `NET_ADMIN` и `NET_RAW` через `runArgs`. Скрипт брандмауэра и эти возможности не требуются для самого Claude Code: вы можете их не включать и вместо этого полагаться на ваши собственные элементы управления сетью.

## Запуск без запросов разрешений

Поскольку контейнер запускает Claude Code как непривилегированный пользователь и ограничивает выполнение команд контейнером, вы можете передать `--dangerously-skip-permissions` для автоматического выполнения. CLI отклоняет этот флаг при запуске от root, поэтому подтвердите, что `remoteUser` установлен на непривилегированную учетную запись.

Пропуск запросов разрешений удаляет вашу возможность просмотреть вызовы инструментов перед их запуском. Claude все еще может изменять любой файл в привязанном рабочем пространстве, который отображается непосредственно на вашем хосте, и достичь всего, что позволяет политика сети контейнера. Объедините этот флаг с [ограничениями исходящего сетевого трафика](#restrict-network-egress) выше, чтобы ограничить то, что может достичь обойденный сеанс.

Если вы хотите меньше подсказок без отключения проверок безопасности, рассмотрите вместо этого [автоматический режим](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), который имеет классификатор для проверки действий перед их запуском. Чтобы предотвратить использование инженерами `--dangerously-skip-permissions` вообще, установите `permissions.disableBypassPermissionsMode` на `"disable"` в [управляемых параметрах](https://code.claude.com/docs/ru/settings-reference.md#permission-settings).

## Попробуйте контейнер-образец

Репозиторий [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/.devcontainer) включает пример контейнера разработки, который объединяет CLI, брандмауэр исходящего трафика, постоянные тома и оболочку на основе Zsh. Он предоставляется как рабочий пример, а не как поддерживаемый базовый образ; используйте его, чтобы увидеть, как части подходят друг к другу, прежде чем применять их к вашей собственной конфигурации.

**1. Установка предварительных условий**

Установите VS Code и [расширение Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

**2. Клонирование образца**

Клонируйте [репозиторий Claude Code](https://github.com/anthropics/claude-code) и откройте его в VS Code.

**3. Повторное открытие в контейнере**

Когда будет предложено, нажмите **Reopen in Container**, или запустите **Dev Containers: Reopen in Container** из палитры команд.

**4. Запуск Claude Code**

После завершения сборки контейнера откройте терминал с помощью `` Ctrl+` `` и запустите `claude` для входа и запуска вашего первого сеанса.

Чтобы использовать эту конфигурацию с вашим собственным проектом, скопируйте каталог `.devcontainer/` в ваш репозиторий и отрегулируйте Dockerfile для вашей цепочки инструментов, или вернитесь к [Добавление Claude Code в контейнер разработки](#add-claude-code-to-your-dev-container), чтобы добавить только функцию в уже имеющуюся установку.

Справочная конфигурация состоит из трех файлов. Ни один из них не требуется при добавлении Claude Code в ваш собственный контейнер разработки через функцию, но они показывают один способ объединения частей.

| Файл | Назначение |
| - | - |
| [`devcontainer.json`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json) | Монтирование томов, возможности `runArgs`, расширения VS Code и `containerEnv` |
| [`Dockerfile`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) | Базовый образ, инструменты разработки и установка Claude Code |
| [`init-firewall.sh`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh) | Ограничивает исходящий сетевой трафик только разрешенными назначениями |

## Следующие шаги

После того как Claude Code работает в вашем контейнере разработки, страницы ниже охватывают остальную часть развертывания организации: выбор пути аутентификации, доставка управляемой политики вне репозитория, мониторинг использования и понимание того, что Claude Code хранит и отправляет.

* [Настройка Claude Code для вашей организации](https://code.claude.com/docs/ru/admin-setup.md): выбор поставщика аутентификации, решение о том, как политика достигает устройств, и планирование развертывания
* [Параметры, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md): доставка управляемой политики из консоли администратора claude.ai, чтобы инженеры не могли обойти ее, редактируя файлы репозитория
* [Мониторинг использования и аудит деятельности](https://code.claude.com/docs/ru/monitoring-usage.md): экспорт метрик OpenTelemetry и просмотр того, что запускает ваша команда
* [Требования к сетевому доступу](https://code.claude.com/docs/ru/network-config.md#network-access-requirements): полный список доменов для прокси и брандмауэров
* [Услуги телеметрии и отказ](https://code.claude.com/docs/ru/data-usage.md#telemetry-services): что Claude Code отправляет по умолчанию и переменные окружения, которые это отключают
* [Изучение каталога `.claude`](https://code.claude.com/docs/ru/claude-directory): что содержит монтирование тома, включая учетные данные, параметры и историю сеанса
* [Среды Bash sandbox](https://code.claude.com/docs/ru/sandbox-environments.md): сравнение контейнеров разработки со встроенной Bash sandbox, пользовательскими контейнерами и виртуальными машинами
* [Модель безопасности](https://code.claude.com/docs/ru/security.md): как система разрешений Claude Code, sandboxing и защита от внедрения подсказок работают вместе
* [Режимы разрешений](https://code.claude.com/docs/ru/permission-modes.md): полный диапазон от Plan Mode к автоматическому режиму к обходу и когда использовать каждый
