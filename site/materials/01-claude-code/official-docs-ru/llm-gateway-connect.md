> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Подключение Claude Code к шлюзу LLM

> Направьте Claude Code на шлюз LLM вашей организации. Проверьте, уже ли администратор его настроил, или установите базовый URL и учетные данные самостоятельно, затем проверьте соединение и исправьте ошибки шлюза.

[Шлюз LLM](https://code.claude.com/docs/ru/llm-gateway) — это прокси, который ваша организация запускает между Claude Code и поставщиком модели. Когда ваша организация использует его, Claude Code аутентифицируется на шлюзе с учетными данными, которые выдает ваша организация, вместо вашего личного входа claude.ai.

Эта страница предназначена для разработчиков, запускающих Claude Code через шлюз, который управляет их организация. Она охватывает два пути: [проверка того, уже ли администратор его настроил для вас](#check-for-an-existing-configuration), и [самостоятельная настройка](#configure-claude-code-yourself), если он этого не сделал.

> [!NOTE]
>
> * Чтобы развернуть шлюз для вашей организации, см. [Развертывание шлюза LLM](https://code.claude.com/docs/ru/llm-gateway-rollout.md)
> * Для информации о том, что Claude Code отправляет на шлюз, см. [справочник протокола шлюза](https://code.claude.com/docs/ru/llm-gateway-protocol.md)

## Проверка существующей конфигурации

Администраторы могут распространять адрес шлюза и учетные данные через [управляемые параметры](https://code.claude.com/docs/ru/managed-settings.md), управление устройствами или [`apiKeyHelper`](#rotate-credentials-with-apikeyhelper), чтобы Claude Code подхватил их при запуске без каких-либо действий с вашей стороны. Чтобы проверить, уже ли ваша организация это сделала:

**1. Запустите Claude Code**

Запустите `claude`. Если он открывается на экран входа вместо сеанса, учетные данные шлюза не были распространены; [настройте его самостоятельно](#configure-claude-code-yourself) ниже.

**2. Проверьте вкладку Status**

Если Claude Code запустил сеанс без отображения экрана входа, запустите `/status`, откройте вкладку **Status** и проверьте две строки:

* `Anthropic base URL`: эта строка появляется только при установке адреса шлюза. Если ее нет, Claude Code не указан на шлюз; [настройте его самостоятельно](#configure-claude-code-yourself) ниже.
* `Auth token` или `API key`: строка, называющая `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY` или `apiKeyHelper`, подтверждает, что учетные данные шлюза активны. Строка `Login method`, называющая учетную запись claude.ai, означает, что учетные данные не были распространены; [установите их самостоятельно](#set-the-credential-variable).

**3. Отправьте тестовое сообщение**

Закройте меню `/status` и отправьте любой запрос в Claude Code. Обычный ответ от Claude без ошибок подтверждает, что соединение с шлюзом работает.

Если обе строки в меню `/status` выглядят правильно, но сообщение Claude не проходит, см. [таблицу устранения неполадок](#troubleshoot-gateway-errors).

## Самостоятельная настройка Claude Code

Чтобы самостоятельно настроить Claude Code для шлюза, вам нужны от команды шлюза:

* Базовый URL шлюза
* Учетные данные: строка ключа или токена, или команда, которая их получает
  * Если команда шлюза не указала, какой тип учетных данных это, раздел [переменная учетных данных](#set-the-credential-variable) ниже охватывает, что попробовать

Разделы ниже охватывают конфигурацию по порядку:

* [Установка переменной учетных данных](#set-the-credential-variable) и [установка базового URL](#set-the-base-url-and-credential): две переменные, которые нужны каждому соединению с шлюзом
* [Проверка соединения](#verify-the-connection): подтвердите, что оно работает, прежде чем что-либо сохранять
* [Настройка каждой поверхности](#configure-each-surface): если вы используете поверхность, отличную от CLI Claude Code, такую как VS Code, см., как настроить ее с учетными данными шлюза
* [Дополнительная конфигурация](#additional-configuration): переменные, которые некоторым шлюзам нужны помимо базового URL и учетных данных, такие как пользовательский заголовок, помощник учетных данных, обнаружение модели, базовый URL в формате поставщика или отключение трафика вне пути шлюза. Устанавливайте их только если администратор их назвал или ваша сеть ограничивает исходящий трафик

### Установка переменной учетных данных

Чтобы аутентифицировать Claude Code на шлюзе, установите ваши учетные данные в переменную окружения. Какая переменная зависит от того, что вам сказала команда шлюза:

| Установите учетные данные в | Используйте когда |
| :- | :- |
| `ANTHROPIC_AUTH_TOKEN` | Команда шлюза сказала "bearer token" или "Authorization header" |
| `ANTHROPIC_API_KEY` | Команда шлюза сказала "API key" или "x-api-key" |
| [`apiKeyHelper`](#rotate-credentials-with-apikeyhelper) | Учетные данные ротируются или поступают из хранилища |

Если вам не сказали, какой тип, используйте `ANTHROPIC_AUTH_TOKEN`; [запрос проверки](#verify-the-connection) ниже показывает, как определить, нужно ли переключиться.

### Установка базового URL и учетных данных

Установите базовый URL шлюза и переменную учетных данных, которую вы выбрали выше, как переменные окружения. Примеры используют `ANTHROPIC_AUTH_TOKEN`; замените его на `ANTHROPIC_API_KEY`, если это [переменная, которую вы выбрали](#set-the-credential-variable). Вы можете установить их [в вашей оболочке](#set-as-shell-environment-variables), что длится один сеанс терминала, или [в файле параметров Claude Code](#set-in-a-settings-file), что сохраняется везде, где работает Claude Code.

Для вашего первого соединения начните с экспорта оболочки и запустите [запрос проверки](#verify-the-connection) перед перемещением значений в файл параметров.

#### Установка как переменные окружения оболочки

Замените значения на те, которые вам дала команда шлюза:

> [tab] Bash или Zsh
>
> ```bash theme={null}
> export ANTHROPIC_BASE_URL=https://llm-gateway.example.com
> export ANTHROPIC_AUTH_TOKEN=sk-gateway-key
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_BASE_URL = "https://llm-gateway.example.com"
> $env:ANTHROPIC_AUTH_TOKEN = "sk-gateway-key"
> ```

Экспорты оболочки применяются только к этому сеансу терминала и программам, запущенным из него. Редактор, запущенный с док-станции или меню "Пуск", их не увидит. Чтобы они сохранялись в новых терминалах, добавьте те же строки в профиль вашей оболочки, такой как `~/.zshrc`, `~/.bashrc` или ваш PowerShell `$PROFILE`.

Если вы экспортируете шлюз только в вашей оболочке, он не надежно достигает фоновых агентов, размещенных [супервизором](https://code.claude.com/docs/ru/agent-view.md#how-background-sessions-are-hosted); см. [как каждый фоновый сеанс получает свой шлюз](https://code.claude.com/docs/ru/agent-view.md#llm-gateway). Используйте файл параметров для любого шлюза, через который фоновые агенты должны всегда маршрутизироваться.

#### Установка в файле параметров

Чтобы конфигурация применялась везде, где работает Claude Code, включая [фоновых агентов](https://code.claude.com/docs/ru/agent-view.md#how-background-sessions-are-hosted), установите переменные в блоке `env` [файла параметров](https://code.claude.com/docs/ru/settings.md) вместо того, чтобы полагаться на вашу оболочку. Файлы параметров имеют разные области:

* `~/.claude/settings.json` применяется ко всем вашим проектам. На Windows путь — `%USERPROFILE%\.claude\settings.json`
* `.claude/settings.local.json` применяется к одному проекту. Claude Code добавляет его в ваш глобальный gitignore при сохранении параметра там; если вы создаете его вручную или позволяете Claude написать его, сначала добавьте его в gitignore самостоятельно, чтобы случайно не зафиксировать ваши учетные данные

> [!WARNING]
>
> Не помещайте учетные данные в `.claude/settings.json` проекта. Этот файл фиксируется и совместно используется со всеми, кто клонирует репозиторий.

Блок `env` выглядит одинаково в любом файле:

```json theme={null}
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://llm-gateway.example.com",
    "ANTHROPIC_AUTH_TOKEN": "sk-gateway-key"
  }
}
```

Когда и экспорт оболочки, и блок `env` файла параметров устанавливают одну и ту же переменную, применяется значение файла параметров. Запустите `/status`, чтобы увидеть, какой базовый URL и источник учетных данных использует Claude Code.

### Проверка соединения

С переменными, экспортированными в вашей оболочке, отправьте однотокенный запрос на шлюз напрямую. Это подтверждает, что URL и учетные данные работают, прежде чем вы откроете Claude Code, поэтому сбой указывает на шлюз, а не на вашу конфигурацию. Команды ниже читают переменные оболочки, поэтому им нужны [экспорты оболочки](#set-as-shell-environment-variables) даже если вы также поместили значения в файл параметров.

> [tab] Bash или Zsh
>
> ```bash theme={null}
> curl -sS -w '\n%{http_code}\n' -X POST "$ANTHROPIC_BASE_URL/v1/messages" \
>   -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
>   -H "anthropic-version: 2023-06-01" \
>   -H "content-type: application/json" \
>   -d '{"model": "claude-sonnet-4-6", "max_tokens": 1, "messages": [{"role": "user", "content": "."}]}'
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> Invoke-RestMethod -Method Post -Uri "$env:ANTHROPIC_BASE_URL/v1/messages" `
>   -Headers @{ "Authorization" = "Bearer $env:ANTHROPIC_AUTH_TOKEN"; "anthropic-version" = "2023-06-01" } `
>   -ContentType "application/json" `
>   -Body '{"model": "claude-sonnet-4-6", "max_tokens": 1, "messages": [{"role": "user", "content": "."}]}'
> ```

Если ваш шлюз ожидает ключи в заголовке `x-api-key`, замените заголовок `Authorization` на `x-api-key: $ANTHROPIC_API_KEY` в команде Bash или запись таблицы хеша `"Authorization"` на `"x-api-key" = "$env:ANTHROPIC_API_KEY"` в команде PowerShell.

Ответ JSON, начинающийся с `{"id":"msg_` и включающий поле `"content":[...]`, означает, что шлюз доступен и учетные данные работают. Ошибка, называющая неизвестную модель, все еще доказывает, что URL и учетные данные работают, так как шлюз аутентифицировал запрос перед отклонением имени модели; вам не нужно находить модель, которую обслуживает ваш шлюз, для этого теста. `401` означает, что учетные данные были отклонены: если вы угадали переменную, переключитесь на другую и переэкспортируйте.

#### Подтверждение в Claude Code

Запустите `claude` из той же оболочки, чтобы он унаследовал экспорты, отправьте сообщение и запустите `/status`.

На вкладке **Status** строка `Anthropic base URL` должна показывать адрес вашего шлюза, что подтверждает маршрутизацию запросов туда; если строки нет, переменная не достигла сеанса. Строка `Auth token` или `API key`, называющая переменную, которую вы установили, подтверждает, что учетные данные шлюза активны, а не сохраненный вход claude.ai.

Если сообщение не проходит или `/status` не показывает URL шлюза, см. [таблицу устранения неполадок](#troubleshoot-gateway-errors) ниже.

### Как переменная учетных данных отображается на заголовок

Каждая переменная отправляет учетные данные в другом HTTP-заголовке: `ANTHROPIC_AUTH_TOKEN` в `Authorization: Bearer`, `ANTHROPIC_API_KEY` в `x-api-key` и `apiKeyHelper` в обоих. Учетные данные в неправильной переменной достигают шлюза в заголовке, который он не читает, и запрос не проходит с `401`. Если запрос проверки вернул `401`, переключитесь на другую переменную и попробуйте снова.

### Конфликты с существующим входом

Ваши запросы используют переменную учётных данных шлюза, а не сохранённый вход claude.ai. С `ANTHROPIC_AUTH_TOKEN` переменная имеет приоритет немедленно. С `ANTHROPIC_API_KEY` вам один раз в интерактивном режиме предлагается одобрить ключ, прежде чем он вступит в силу.

Запустите `/status`, чтобы подтвердить, какой источник учетных данных активен. Если при запуске показывается предупреждение о конфликте аутентификации, называющее два источника, см. первую строку [таблицы устранения неполадок](#troubleshoot-gateway-errors), чтобы узнать, какой из них отбросить. Чтобы очистить сохраненный вход, чтобы остались только учетные данные шлюза, запустите `/logout`.

## Настройка каждой поверхности

CLI читает переменные окружения и файлы параметров выше. Другие поверхности — это расширение VS Code, настольное приложение, GitHub Actions, Agent SDK и облачные поверхности, такие как Slack и веб; разделы ниже охватывают, достигают ли эти параметры каждую.

### Расширение VS Code

Установите переменные шлюза для [расширения VS Code](https://code.claude.com/docs/ru/vs-code.md) в `claudeCode.environmentVariables` в собственных параметрах пользователя VS Code, открытых командой **Preferences: Open User Settings (JSON)**. Расширение проверяет учетные данные из этого параметра перед запуском, поэтому это надежное место для учетных данных шлюза; значения в `~/.claude/settings.json` достигают порожденного процесса, но не проверку входа самого расширения.

```json theme={null}
{
  "claudeCode.environmentVariables": [
    { "name": "ANTHROPIC_BASE_URL", "value": "https://llm-gateway.example.com" },
    { "name": "ANTHROPIC_AUTH_TOKEN", "value": "sk-gateway-key" }
  ]
}
```

### Настольное приложение

Настольное приложение читает маршрутизацию шлюза из [конфигурации сторонних поставщиков](https://claude.com/docs/third-party/claude-desktop/gateway), а не из `ANTHROPIC_BASE_URL` или `settings.json`. Эта конфигурация может поступить от вашей организации или из формы в самом приложении:

* **Распределено администратором**: если ваша организация [развернула конфигурацию](https://code.claude.com/docs/ru/llm-gateway-rollout.md#distribute-through-managed-settings), настольное приложение маршрутизирует через шлюз без каких-либо действий с вашей стороны
* **Настроено локально**: для устройств без распределенной администратором конфигурации откройте Help → Troubleshooting → Включить режим разработчика, который перезагружает приложение с меню Developer. Затем откройте Developer → Configure Third-Party Inference и введите базовый URL вашего шлюза. Распределенная администратором конфигурация имеет приоритет и делает эту форму доступной только для чтения

При активной конфигурации шлюза средство выбора окружения не предлагает размещённые в облаке окружения Anthropic, и [Remote Control](https://code.claude.com/docs/ru/remote-control.md) недоступен.

Сессии SSH с конфигурацией шлюза находятся в бета-версии и требуют Claude Desktop v1.40609.0 или новее. Перед подключением проверьте список разрешённых хостов и адрес шлюза:

* **Разрешённые хосты**: сессии SSH по умолчанию отключены. Чтобы включить их, вы или ваш администратор указываете разрешённые хосты в ключе [`sshHostAllowlist`](https://claude.com/docs/third-party/claude-desktop/configuration#sshhostallowlist) конфигурации сторонних поставщиков
* **Адрес шлюза**: удалённый компьютер подключается к шлюзу самостоятельно, поэтому шлюз по адресу `localhost` на вашем компьютере не работает для сессий SSH

См. [Удалённые сессии SSH в Claude Desktop со сторонними поставщиками](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions). Вы также можете запустить CLI на удалённом хосте, установив там [`ANTHROPIC_BASE_URL` и учётные данные шлюза](#set-the-base-url-and-credential).

Если настольное приложение показывает `Gateway was unreachable`, приложение не смогло достичь настроенный базовый URL при запуске; проверьте URL и сетевой путь с помощью [теста curl выше](#verify-the-connection).

### GitHub Actions

[Claude Code GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) читает `ANTHROPIC_BASE_URL` и `ANTHROPIC_CUSTOM_HEADERS` из блока `env` рабочего процесса. Передайте учетные данные как вход `anthropic_api_key` действия; действие устанавливает его как `ANTHROPIC_API_KEY`, поэтому он достигает шлюза в заголовке `x-api-key`.

Для шлюза `x-api-key` установите базовый URL в `env` и передайте ключ шлюза как вход:

```yaml theme={null}
env:
  ANTHROPIC_BASE_URL: https://llm-gateway.example.com

steps:
  - uses: anthropics/claude-code-action@v1
    with:
      anthropic_api_key: ${{ secrets.GATEWAY_API_KEY }}
```

Для шлюза bearer-token передайте один и тот же секрет как вход `anthropic_api_key` и `ANTHROPIC_AUTH_TOKEN` в блоке `env` рабочего процесса. Действие требует `anthropic_api_key`, `CLAUDE_CODE_OAUTH_TOKEN` или федерацию рабочей нагрузки перед запуском Claude Code, и оно не читает `ANTHROPIC_AUTH_TOKEN`, поэтому вход удовлетворяет эту проверку запуска. Переменная окружения помещает ключ в заголовок `Authorization`, который читает шлюз; копия в `x-api-key` игнорируется:

```yaml theme={null}
env:
  ANTHROPIC_BASE_URL: https://llm-gateway.example.com
  ANTHROPIC_AUTH_TOKEN: ${{ secrets.GATEWAY_API_KEY }}

steps:
  - uses: anthropics/claude-code-action@v1
    with:
      anthropic_api_key: ${{ secrets.GATEWAY_API_KEY }}
```

Для других вариантов аутентификации действия, включая `CLAUDE_CODE_OAUTH_TOKEN` и федерацию рабочей нагрузки, см. [Claude Code GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) и [README](https://github.com/anthropics/claude-code-action#readme) действия.

### Agent SDK

[Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) не имеет опций, специфичных для шлюза; он передает переменные окружения процессу Claude Code, который он порождает. Каждый SDK принимает опцию `env`, которая устанавливает окружение порожденного процесса, и SDK TypeScript и Python обрабатывают это по-разному:

* TypeScript: порожденный процесс по умолчанию наследует родительское окружение, но установка `options.env` полностью заменяет окружение. Распределите `process.env` в него, чтобы сохранить переменные шлюза.
* Python: `ClaudeAgentOptions(env=...)` объединяется поверх унаследованного окружения, поэтому переменные шлюза, установленные в родительском процессе, проходят без распределения.

```ts TypeScript theme={null}
const result = query({
  prompt: "...",
  options: {
    env: {
      ...process.env,
      ANTHROPIC_BASE_URL: "https://llm-gateway.example.com",
      ANTHROPIC_AUTH_TOKEN: process.env.GATEWAY_KEY,
    },
  },
})
```

```python Python theme={null}
options = ClaudeAgentOptions(
    env={
        "ANTHROPIC_BASE_URL": "https://llm-gateway.example.com",
        "ANTHROPIC_AUTH_TOKEN": os.environ["GATEWAY_KEY"],
    }
)
```

### Slack, облачные сеансы и Remote Control

[Claude Code в Slack](https://code.claude.com/docs/ru/slack.md) и [облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) не являются частью развёртывания шлюза. Переменные шлюза, установленные в конфигурации окружения облачной сессии, не применяются. Если ваш трафик должен оставаться на шлюзе, не включайте эти интерфейсы для таких пользователей.

[Remote Control](https://code.claude.com/docs/ru/remote-control.md) и [голосовая диктовка](https://code.claude.com/docs/ru/voice-dictation.md) полагаются на идентичность claude.ai: Remote Control — для связи активной сессии с вашей учётной записью, а голосовая диктовка — для доступа к эндпоинту транскрипции claude.ai. Они недоступны, пока активны `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper`. Remote Control также отключён, пока `ANTHROPIC_BASE_URL` указывает на хост, не принадлежащий Anthropic, поэтому входа с claude.ai самого по себе недостаточно.

Чтобы восстановить любую из этих функций, войдите с claude.ai и отмените установку переменных шлюза, которые проверяет эта функция. Раздел Remote Control в `claude doctor` называет то, что в настоящее время блокирует Remote Control.

* Голосовая диктовка: отмените установку учетных данных шлюза
* Remote Control: отмените установку учетных данных шлюза и `ANTHROPIC_BASE_URL`

## Дополнительная конфигурация

Эти настройки охватывают случаи, выходящие за рамки базового URL и учётных данных. Задавайте их, только если этого требуют инструкции вашего администратора, правила исходящего трафика вашей сети или [таблица устранения неполадок](#troubleshoot-gateway-errors).

### Отправка дополнительных заголовков

Некоторые шлюзы маршрутизируют или помечают запросы с помощью пользовательского заголовка в дополнение к учётным данным, например идентификатора арендатора или ключа маршрутизации. Чтобы отправить такой заголовок, задайте [`ANTHROPIC_CUSTOM_HEADERS`](https://code.claude.com/docs/ru/env-vars), указав по одной паре `Name: Value` на строку. В примере ниже добавляется заголовок маршрутизации с именем `X-Org-Route`:

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export ANTHROPIC_CUSTOM_HEADERS="X-Org-Route: prod"
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_CUSTOM_HEADERS = "X-Org-Route: prod"
> ```

Вы также можете задать `ANTHROPIC_CUSTOM_HEADERS` в блоке `env` файла настроек. Используйте там `\n` между парами, поскольку строки JSON не могут занимать несколько строк:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Org-Route: prod\nX-Tenant: example"
  }
}
```

Подобные имена заголовков маршрутизации и арендатора относятся к [заголовкам, требующим подтверждения](https://code.claude.com/docs/ru/server-managed-settings.md#environment-variables-and-the-approval-dialog). Если заголовки берутся из файла настроек проекта, Claude Code применяет их согласно [правилам применения значений `env`](https://code.claude.com/docs/ru/settings-reference#when-claude-code-applies-env-values).

### Добавление моделей шлюза в меню выбора модели

При включённом обнаружении моделей Claude Code при запуске запрашивает у шлюза список его моделей и добавляет эти имена в меню выбора `/model` наряду со встроенными вариантами. Если вы или ваш администратор задали `replaceBuiltInOptions` в наборе [`modelPicker`](https://code.claude.com/docs/ru/settings-reference#modelpicker), Claude Code скрывает и обнаруженные имена. При этом сохраняется строка для модели, которая уже используется в сессии.

Включите обнаружение, если ваш шлюз предоставляет имена моделей, которых нет во встроенном списке Claude Code, и вы хотите выбирать их в меню. Если вы используете встроенные модели, обнаружение вам не нужно; кроме того, ваш администратор мог уже включить его через управляемые настройки.

Чтобы включить его, задайте `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` в своей оболочке или в блоке `env` файла `~/.claude/settings.json`.

Обнаруженные модели отображаются как дополнительные пункты `/model`. Для каждого пункта показывается описание, которое ваш шлюз предоставляет для модели, или `From gateway`, если шлюз его не предоставляет.

Чтобы убедиться, что обнаружение выполнилось, запустите `claude --debug` и найдите строки `[gatewayDiscovery]` в отладочном логе `~/.claude/debug/<session-id>.txt`. При первом успешном обнаружении Claude Code записывает в лог, сколько моделей он кэшировал, и повторно делает запись только при изменении списка шлюза. Там же отображаются `404`, таймаут или перенаправление. О том, когда выполняется обнаружение, что оно отфильтровывает и в каком формате шлюзы должны отдавать ответ, см. [справочник по обнаружению моделей](https://code.claude.com/docs/ru/llm-gateway-protocol.md#model-discovery).

### Ротация учётных данных с помощью apiKeyHelper

`apiKeyHelper` — это команда, которую Claude Code запускает для получения учётных данных шлюза вместо их чтения из статической переменной окружения.

Используйте вспомогательную команду, если срок действия учётных данных истекает по расписанию, они поступают из хранилища секретов или команды SSO либо если администратор велел вам её настроить. Если ваши учётные данные — это фиксированная строка, которую вы задаёте один раз, вам достаточно [переменной учётных данных](#set-the-credential-variable), и этот раздел можно пропустить.

Вспомогательная команда — это любая shell-команда, которая выводит текущие учётные данные в stdout. Claude Code запускает её через системную оболочку, поэтому в Windows это может быть исполняемый файл или вызов PowerShell. Команда должна выводить только учётные данные и ничего больше. В Claude Code v2.1.227 и более поздних версиях баннер или строка лога, выведенные вместе с ключом, приводят к [сбою вспомогательной команды](https://code.claude.com/docs/ru/errors.md#your-apikeyhelper-script-is-failing). Напишите скрипт, сделайте его исполняемым и укажите его в `apiKeyHelper` в вашем [файле настроек](https://code.claude.com/docs/ru/settings.md):

> [tab] Bash or Zsh
>
> Например, скрипт, читающий из хранилища секретов:
>
> ```bash theme={null}
> #!/bin/bash
> vault kv get -field=api_key secret/llm-gateway/claude-code
> ```
>
> Укажите путь к нему в `~/.claude/settings.json`:
>
> ```json theme={null}
> {
>   "apiKeyHelper": "~/bin/get-gateway-key.sh"
> }
> ```

> [tab] PowerShell
>
> Например, скрипт, читающий из хранилища секретов:
>
> ```powershell theme={null}
> vault kv get -field=api_key secret/llm-gateway/claude-code
> ```
>
> Укажите вызов PowerShell в `%USERPROFILE%\.claude\settings.json`, экранировав обратные косые черты в строке JSON:
>
> ```json theme={null}
> {
>   "apiKeyHelper": "powershell -NoProfile -File C:\\scripts\\get-gateway-key.ps1"
> }
> ```

По умолчанию Claude Code кэширует вывод вспомогательной команды на пять минут и снова запускает её по истечении срока жизни кэша. Чтобы изменить срок жизни, задайте `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` в миллисекундах, например `CLAUDE_CODE_API_KEY_HELPER_TTL_MS=900000` для 15 минут.

Другие случаи, в которых Claude Code повторно запускает вспомогательную команду, описаны в разделе [`apiKeyHelper`](https://code.claude.com/docs/ru/settings-reference#apikeyhelper).

Значение вспомогательной команды отправляется в заголовках `Authorization` и `x-api-key`, поэтому оно работает независимо от того, какой заголовок читает ваш шлюз.

### Отключение трафика вне шлюза

Шлюз передаёт запросы к модели, но Claude Code также отправляет необязательный фоновый трафик в обход шлюза — в Anthropic и сторонние сервисы, такие как GitHub: проверки версий, телеметрию, заметки о выпусках и аналогичные запросы. В сети, где исходящий трафик разрешён только к шлюзу, эти запросы завершаются неудачей и могут отображаться как заблокированные подключения в мониторинге исходящего трафика.

Чтобы отключить этот трафик, задайте `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` вместе с переменными шлюза — в тех же экспортах оболочки или в блоке `env` файла настроек:

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"
> ```

У этой переменной следующие эффекты и ограничения:

* Она отключает автообновления, поэтому предусмотрите другой способ обновления, например через менеджер пакетов или управляемое распространение.
* Она подавляет проверку доступности [быстрого режима](https://code.claude.com/docs/ru/fast-mode.md). Если при использовании Anthropic API команда `/fast` после этого сообщает, что быстрый режим недоступен, см. раздел [использование быстрого режима за прокси и LLM-шлюзами](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-behind-proxies-and-llm-gateways), чтобы восстановить быстрый режим.
* Она не влияет на [обнаружение моделей шлюза](#add-gateway-models-to-the-model-picker), которое обращается только к вашему шлюзу. До v2.1.257 эта переменная также останавливала обновление результатов обнаружения, поэтому в меню выбора оставался ранее кэшированный список.
* [Проверка безопасности доменов](https://code.claude.com/docs/ru/data-usage.md#webfetch-domain-safety-check) инструмента WebFetch не затрагивается и по-прежнему обращается к `api.anthropic.com`. Отключите её отдельно с помощью `skipWebFetchPreflight: true` в [настройках](https://code.claude.com/docs/ru/settings.md), если ваша сеть блокирует этот хост.
* Каждый поток телеметрии и управляющая им переменная описаны в разделе [сервисы телеметрии](https://code.claude.com/docs/ru/data-usage.md#telemetry-services).

### Маршрутизация к облачному провайдеру через шлюз

Эти конфигурации направляют Claude Code на шлюз через специфичную для провайдера переменную базового URL вместо `ANTHROPIC_BASE_URL`. Шлюзы Amazon Bedrock и Google Cloud's Agent Platform принимают нативные форматы запросов этих провайдеров; шлюзы Microsoft Foundry и Claude Platform on AWS принимают формат Anthropic Messages. На маршрутах Amazon Bedrock и Google Cloud's Agent Platform Claude Code также ограничивает отправляемые бета-заголовки и поля запроса набором, который принимает данный провайдер. О том, что получает ваш шлюз на каждом маршруте, см. [руководство по совместимости шлюзов](https://code.claude.com/docs/ru/llm-gateway-protocol.md).

Используйте их, только если команда, отвечающая за шлюз, явно назвала Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry или Claude Platform on AWS. Если [проверочный запрос](#verify-the-connection) выше вернул JSON, этот раздел можно пропустить.

Задайте блок для провайдера, названного командой, отвечающей за шлюз. Переменные пропуска аутентификации в блоках Amazon Bedrock, Google Cloud's Agent Platform и Claude Platform on AWS указывают Claude Code не подписывать запросы учётными данными облачного провайдера, поскольку они хранятся на шлюзе. Если шлюзу также нужен собственный токен, место, куда его указать, зависит от провайдера:

* **Amazon Bedrock, Google Cloud's Agent Platform или Claude Platform on AWS**: добавьте `ANTHROPIC_AUTH_TOKEN` после блока. Claude Code отправляет его на шлюз в заголовке `Authorization: Bearer`. Для учётных данных с другой схемой или в другом заголовке используйте вместо этого [`ANTHROPIC_CUSTOM_HEADERS`](#send-additional-headers). В любом случае оставьте переменную пропуска аутентификации заданной, поскольку без неё Claude Code удаляет любой заголовок `Authorization`, который добавили бы `ANTHROPIC_AUTH_TOKEN`, [`apiKeyHelper`](#rotate-credentials-with-apikeyhelper) или `ANTHROPIC_CUSTOM_HEADERS`.
* **Microsoft Foundry**: используйте `ANTHROPIC_FOUNDRY_API_KEY`, как показано в [его блоке](#microsoft-foundry)

#### Amazon Bedrock

Не задавайте `AWS_BEARER_TOKEN_BEDROCK`, если шлюз выдаёт собственные учётные данные. Если вы её зададите, Claude Code отправит этот [API-ключ Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md#2-configure-aws-credentials) в заголовке `Authorization` вместо токена вашего шлюза, даже если задана `CLAUDE_CODE_SKIP_BEDROCK_AUTH`.

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export ANTHROPIC_BEDROCK_BASE_URL=https://llm-gateway.example.com/bedrock
> export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
> export CLAUDE_CODE_USE_BEDROCK=1
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_BEDROCK_BASE_URL = "https://llm-gateway.example.com/bedrock"
> $env:CLAUDE_CODE_SKIP_BEDROCK_AUTH = "1"
> $env:CLAUDE_CODE_USE_BEDROCK = "1"
> ```

#### Google Cloud's Agent Platform

Замените идентификатор проекта и регион своими значениями. Claude Code включает оба значения в путь каждого запроса, который отправляет на шлюз:

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export ANTHROPIC_VERTEX_BASE_URL=https://llm-gateway.example.com/vertex
> export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
> export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
> export CLAUDE_CODE_USE_VERTEX=1
> export CLOUD_ML_REGION=us-east5
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_VERTEX_BASE_URL = "https://llm-gateway.example.com/vertex"
> $env:ANTHROPIC_VERTEX_PROJECT_ID = "your-gcp-project-id"
> $env:CLAUDE_CODE_SKIP_VERTEX_AUTH = "1"
> $env:CLAUDE_CODE_USE_VERTEX = "1"
> $env:CLOUD_ML_REGION = "us-east5"
> ```

Этот блок охватывает маршрутизацию и аутентификацию. Переопределения регионов и закрепление моделей из [настройки Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md#4-configure-claude-code) действуют и через шлюз:

* **Регионы для отдельных моделей**: если ваш шлюз обслуживает некоторые модели из региона, отличного от `CLOUD_ML_REGION`, задайте для каждой соответствующую переменную `VERTEX_REGION_CLAUDE_*`, например `VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1`. Точные имена приведены в [справочнике по переменным окружения](https://code.claude.com/docs/ru/env-vars.md).
* **Версии моделей**: закрепите `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` и `ANTHROPIC_DEFAULT_HAIKU_MODEL`, как описано в разделе [Закрепление версий моделей](https://code.claude.com/docs/ru/google-vertex-ai.md#5-pin-model-versions). Задание `ANTHROPIC_DEFAULT_HAIKU_MODEL` также переводит на эту модель фоновые задачи, например генерацию названий сессий; в том же разделе объясняется, какая модель выполняет их в противном случае.
* **Возможности моделей**: если вы закрепляете идентификатор модели, который ваша версия Claude Code не распознаёт, такие функции, как уровни effort или расширенное мышление, могут остаться для неё отключёнными. Объявите, что поддерживает модель, с помощью [`ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES`](https://code.claude.com/docs/ru/model-config#customize-pinned-model-display-and-capabilities) и её аналогов для Sonnet и Haiku.

#### Microsoft Foundry

Укажите учётные данные шлюза в `ANTHROPIC_FOUNDRY_API_KEY`; они отправляются на шлюз в заголовке `x-api-key`. Шлюзу, ожидающему Bearer-токен, можно вместо этого передать [`ANTHROPIC_FOUNDRY_AUTH_TOKEN`](https://code.claude.com/docs/ru/env-vars). Claude Code отправляет это значение в заголовке `Authorization: Bearer`, и оно имеет приоритет над `ANTHROPIC_FOUNDRY_API_KEY`, если заданы обе переменные. Требуется Claude Code v2.1.203 или более поздней версии.

Для шлюза, который подставляет собственный заголовок `Authorization`, задайте `CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1` и оставьте обе переменные учётных данных незаданными. Тогда Claude Code отправляет запросы без учётных данных Azure и сохраняет заголовок `Authorization`, который вы передаёте, например через `ANTHROPIC_CUSTOM_HEADERS`.

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export ANTHROPIC_FOUNDRY_BASE_URL=https://llm-gateway.example.com/foundry
> export ANTHROPIC_FOUNDRY_API_KEY=sk-gateway-key
> export CLAUDE_CODE_USE_FOUNDRY=1
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_FOUNDRY_BASE_URL = "https://llm-gateway.example.com/foundry"
> $env:ANTHROPIC_FOUNDRY_API_KEY = "sk-gateway-key"
> $env:CLAUDE_CODE_USE_FOUNDRY = "1"
> ```

#### Claude Platform on AWS

Об идентификаторе рабочего пространства см. [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md).

> [tab] Bash or Zsh
>
> ```bash theme={null}
> export ANTHROPIC_AWS_BASE_URL=https://llm-gateway.example.com/anthropic-aws
> export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
> export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
> export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> $env:ANTHROPIC_AWS_BASE_URL = "https://llm-gateway.example.com/anthropic-aws"
> $env:ANTHROPIC_AWS_WORKSPACE_ID = "wrkspc_01ABCDEFGHIJKLMN"
> $env:CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH = "1"
> $env:CLAUDE_CODE_USE_ANTHROPIC_AWS = "1"
> ```

#### Проверка маршрута провайдера

Запустите `claude` из оболочки, в которой вы задали блок, и выполните `/status`. С блоком Amazon Bedrock на вкладке **Status** отображаются строки такого вида:

```text theme={null}
API provider: Amazon Bedrock
Bedrock base URL: https://llm-gateway.example.com/bedrock
AWS auth skipped
```

Остальные блоки выводят такие же строки под названиями своих провайдеров, например `Vertex base URL` и `GCP auth skipped` для Google Cloud's Agent Platform; блок Microsoft Foundry показывает строку о пропуске аутентификации, только если вы задали `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`. Если вы также выполняете маршрутизацию через корпоративный прокси, строка `Proxy` показывает URL прокси. Если строка базового URL отсутствует, переменная не попала в сессию.

## Устранение неполадок с ошибками шлюза

Это наиболее распространенные ошибки при запуске Claude Code через шлюз, с причиной на стороне шлюза и исправлением:

| Ошибка | Причина | Исправление |
| :- | :- | :- |
| Предупреждение при запуске, называющее два источника учётных данных и заканчивающееся на `auth may not work as expected`. Более старые версии показывают `Auth conflict: Both a token (SOURCE) and an API key (SOURCE) are set` вместо этого. | Учётные данные шлюза и сохраненный вход активны одновременно | Отмените установку переменной, чтобы использовать сохраненный вход, или запустите `/logout`, чтобы использовать учётные данные шлюза |
| Ошибки `401`, называющие недействительный или неузнанный токен | Учетные данные не являются теми, которые выдал шлюз, или они находятся в заголовке, который шлюз не читает | Подтвердите, что переменная соответствует вашему типу учетных данных в [таблице учетных данных](#set-the-credential-variable), и перевыпустите ключ на шлюзе, если он был отозван |
| `Your apiKeyHelper script is failing`, или `apiKeyHelper failed:` на stderr в неинтерактивном режиме | Команда в параметре [`apiKeyHelper`](https://code.claude.com/docs/ru/settings-reference#apikeyhelper) не выдала пригодный ключ, поэтому запросы содержат заполнитель ключа | Запустите команду напрямую, чтобы увидеть, почему она не работает, и повторно аутентифицируйтесь у поставщика учетных данных, если он сообщает об истекшем сеансе; см. [справочник по ошибкам](https://code.claude.com/docs/ru/errors.md#your-apikeyhelper-script-is-failing) |
| `Connection refused — a firewall or proxy may be blocking it (ConnectionRefused)` когда ничто не отвечает по адресу, или `Can't reach the API server — check your internet or DNS (ENOTFOUND)` когда имя хоста не разрешается, часто после молчаливой паузы, пока Claude Code [повторяет с отступом](https://code.claude.com/docs/ru/errors.md#automatic-retries). Код в скобках варьируется; [Unable to connect to API](https://code.claude.com/docs/ru/errors.md#unable-to-connect-to-api) охватывает варианты кодов и более раннюю формулировку | Ничто не ответило на базовый URL: адрес неправильный, или VPN или брандмауэр блокирует путь к шлюзу | Запустите [тест curl выше](#verify-the-connection), который немедленно не проходит с той же причиной, и подтвердите URL и сетевой путь с командой шлюза |
| `API returned an empty or malformed response (HTTP 200)` | Шлюз или промежуточный прокси вернул ответ, отличный от API, часто HTML-ошибку или страницу входа | Протестируйте с [запросом curl выше](#verify-the-connection); исправьте маршрут шлюза, который возвращает что-то иное, чем ответ Claude API. [Справочник по ошибкам](https://code.claude.com/docs/ru/errors.md#api-returned-an-empty-or-malformed-response) объясняет детали, которые сообщает сообщение |
| Ошибки `400`, называющие `context_management`, `Extra inputs are not permitted` или другие неузнанные поля | Шлюз пересылает запросы на вышестоящий сервис, который отклоняет поля, которые Claude Code отправляет на эндпоинты формата Anthropic | Установите `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`, что подавляет большинство полей предварительного выпуска; см. [передача функций](https://code.claude.com/docs/ru/llm-gateway-protocol.md#feature-pass-through). Некоторые бета-версии не управляются этим флагом; для них установите соответствующую переменную поставщика `CLAUDE_CODE_USE_*`, чтобы Claude Code отправлял только то, что этот поставщик принимает. Шаги, зависящие от того, какое поле указано в сообщении, см. в разделе [Extra inputs are not permitted](https://code.claude.com/docs/ru/errors.md#extra-inputs-are-not-permitted) |
| Ошибки `400`, называющие `thinking` или `adaptive`, такие как `Input tag 'adaptive' found` | Сборка вышестоящей модели не принимает адаптивное рассуждение, которое Claude Code запрашивает для Claude Opus 4.6, Claude Sonnet 4.6, Claude Haiku 5.5, Claude Fable 5 и более поздних моделей | Обновите вышестоящий сервис шлюза. На Opus 4.6 и Sonnet 4.6 вместо этого работает `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Переменные возможностей [конфигурации модели](https://code.claude.com/docs/ru/model-config.md) применяются только к конфигурациям поставщика, таким как `CLAUDE_CODE_USE_BEDROCK` и `CLAUDE_CODE_USE_VERTEX`, а не за шлюзом `ANTHROPIC_BASE_URL` |
| Ошибки `400`, указывающие контекст или лимит токена в собственных словах шлюза, такие как `ContextWindowExceededError` или `prompt token count of N exceeds the limit of M` | Шлюз применяет меньший контекст, чем собственное окно модели, и переписывает ошибку вышестоящего, поэтому Claude Code не распознает это как [слишком длинную ошибку](https://code.claude.com/docs/ru/errors.md#prompt-is-too-long) и не выполняет автоматическое сжатие и повтор | Запустите `/compact`, чтобы восстановить сеанс. Чтобы предотвратить это, установите `CLAUDE_CODE_AUTO_COMPACT_WINDOW` на лимит шлюза; Claude Code зажимает значение как минимум на 100 000 токенов и максимум на контекстное окно модели, поэтому лимит шлюза ниже 100 000 не может быть согласован, и `/compact` остается восстановлением там. Также установите `CLAUDE_CODE_MAX_OUTPUT_TOKENS` ниже лимита вывода модели шлюза |
| Ошибки `400` на каждом запросе, в собственных словах шлюза отклоняющие входную схему инструмента или его `pattern`, на Claude Code v2.1.265 через v2.1.267 | При постепенном развертывании на этих версиях схема [инструмента Artifact](https://code.claude.com/docs/ru/artifacts.md#availability) содержит регулярное выражение с классами символов Unicode `\p{...}`. API Anthropic его принимает, но шлюз или вышестоящий, который проверяет `pattern` каждой схемы инструмента с помощью собственного механизма regex, отклоняет весь запрос | Обновитесь до v2.1.268 или позже, которая не отправляет регулярное выражение. На затронутой версии [отключите артефакты](https://code.claude.com/docs/ru/artifacts.md#disable-artifacts), что удаляет инструмент и его схему из запросов |
| Ошибки `400` на каждом запросе, в собственных словах шлюза отклоняющие неузнанный тип инструмента, такие как `Input tag 'advisor_20260301'`, на Claude Code v2.1.275 | При постепенном развертывании на этой версии запросы содержат запись [инструмента advisor](https://code.claude.com/docs/ru/advisor.md) даже с отключенным advisor. API Anthropic его принимает, но шлюз или вышестоящий, который проверяет типы инструментов, отклоняет весь запрос; тот, который [пересылает поля тела запроса без изменений](https://code.claude.com/docs/ru/llm-gateway-protocol.md#forward-as-open-lists), пропускает его без влияния. Запись является объявлением, которое не содержит содержимого разговора | Обновитесь до v2.1.276 или позже, которая не отправляет запись за шлюзом `ANTHROPIC_BASE_URL`, если вы не включите advisor. На v2.1.275 установите [`CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1`](https://code.claude.com/docs/ru/env-vars), что удаляет запись из запросов |
| Модели отсутствуют в средстве выбора `/model` | Имена моделей шлюза отсутствуют во встроенном списке Claude Code, или Claude Code показывает [`modelPicker`](https://code.claude.com/docs/ru/settings-reference#modelpicker) набор, который заменяет встроенные параметры | Включите [обнаружение модели шлюза](#add-gateway-models-to-the-model-picker) или добавьте имена с переменными [конфигурации модели](https://code.claude.com/docs/ru/model-config.md). Если Claude Code показывает заменяющий набор `modelPicker`, добавьте модели шлюза в него, или попросите администратора добавить их, когда управляемые параметры его предоставляют |
| `/fast` сообщает `Fast mode unavailable due to network connectivity issues`, в то время как запросы вывода работают | Проверка доступности [быстрого режима](https://code.claude.com/docs/ru/fast-mode.md) идёт непосредственно на `api.anthropic.com` и не следует `ANTHROPIC_BASE_URL`, поэтому заблокированный прямой исходящий трафик не проходит проверку | Добавьте `api.anthropic.com` в список разрешённых доменов, если исходящий трафик заблокирован, или установите переменную пропуска. См. [использование быстрого режима за прокси и LLM-шлюзами](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-behind-proxies-and-llm-gateways) |
| `/fast` сообщает `Fast mode is currently unavailable` в сессии, которая аутентифицируется с помощью выданного шлюзом ключа в `ANTHROPIC_API_KEY` | Пока `ANTHROPIC_BASE_URL` указывает на ваш шлюз, а ключ не соответствует формату API-ключа Anthropic, Claude Code не отправляет проверку доступности [быстрого режима](https://code.claude.com/docs/ru/fast-mode.md). При отсутствии закэшированной ранее успешной проверки он считает быстрый режим недоступным | Установите `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS=1`; см. [использование быстрого режима за прокси и LLM-шлюзами](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-behind-proxies-and-llm-gateways) |
| `/fast` сообщает `Fast mode has been disabled by your organization` в сессии, аутентифицированной с помощью `ANTHROPIC_AUTH_TOKEN`, даже если в организации включён быстрый режим | Проверка доступности требует входа в claude.ai или API-ключа; при наличии только Bearer-токена Claude Code считает быстрый режим отключённым, не отправляя проверку | Установите `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1`; см. [использование быстрого режима за прокси и LLM-шлюзами](https://code.claude.com/docs/ru/fast-mode.md#use-fast-mode-behind-proxies-and-llm-gateways) |
| `/feedback` сохраняет локальный файл в сессии, которая использует `ANTHROPIC_BASE_URL` | За шлюзом `ANTHROPIC_AUTH_TOKEN` и ключ, не соответствующий формату API-ключа Anthropic, не являются учётными данными Anthropic. Без таких учётных данных Claude Code записывает отчёт в локальный архив в `~/.claude/feedback-bundles/` вместо того, чтобы отправить его | Отправьте файл представителю вашего аккаунта Anthropic или приложите его к запросу в службу поддержки. См. [сервисы телеметрии](https://code.claude.com/docs/ru/data-usage.md#telemetry-services) |
| Claude Code просит вас войти, даже если [тест curl](#verify-the-connection) успешен | CLI не имеет собственных учетных данных: достижимый базовый URL не является одним, и в интерактивном сеансе блок `env` в `.claude/settings.json` или `.claude/settings.local.json` проекта применяется только после мастера первого запуска и [подсказки доверия](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder) | Установите `ANTHROPIC_AUTH_TOKEN` где-то, где Claude Code читает перед первоначальной настройкой: экспорт оболочки, блок `env` в `~/.claude/settings.json` или управляемые параметры |
| `ANTHROPIC_API_KEY` установлен, но игнорируется, без подсказки | Ключ требует одобрения один раз в интерактивных сеансах, и ранее отклоненный ключ игнорируется без повторного запроса | Включите его под `/config` с опцией `Use custom API key` |
| `This machine's managed settings require a first-party login`, или [`Administrator policy requires a Cloud gateway sign-in`](https://code.claude.com/docs/ru/errors#administrator-policy-requires-a-cloud-gateway-sign-in) когда управляемые параметры устанавливают `forceLoginMethod` на `"gateway"` или также устанавливают `forceLoginGatewayUrl` | Управляемые параметры включают `forceLoginMethod` или `forceLoginOrgUUID`, которые не могут сосуществовать с `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper` | Администратор должен удалить `forceLoginMethod`, `forceLoginOrgUUID` и `forceLoginGatewayUrl` из управляемых параметров, чтобы использовать учетные данные шлюза, или удалить учетные данные шлюза и использовать вход, который требуют управляемые параметры. Эти два не могут быть объединены |
| `403` с телом HTML, такое как `403 Forbidden`, когда собственные журналы шлюза не показывают полученный запрос | Веб-приложение брандмауэра или обратный прокси перед шлюзом заблокировал тело запроса перед тем, как оно достигло шлюза. Подсказки Claude Code включают теги в стиле XML и исходный код, которые соответствуют правилам тела межсайтового скриптинга, поэтому короткий тест curl проходит, а реальный сеанс нет | Исключите путь `/v1/messages` шлюза из проверки тела запроса. На AWS WAF это управляемое правило `CrossSiteScripting_Body`; на nginx с ModSecurity это эквивалентные правила тела OWASP CRS |
| Ошибки сертификата или TLS, такие как `SSL certificate verification failed` или `Self-signed certificate detected`, когда [тест curl](#verify-the-connection) успешен | Среда выполнения Claude Code не доверяет тому же центру сертификации, что и `curl`. Обычно за корпоративными прокси-серверами проверки TLS | Установите `NODE_EXTRA_CA_CERTS` на путь пакета CA; см. [хранилище сертификатов CA](https://code.claude.com/docs/ru/network-config.md#ca-certificate-store) |

Если Claude Code повторно просит вас войти после удаления конфигурации шлюза, причина обычно в хранилище учетных данных, а не в шлюзе; см. [ошибки аутентификации](https://code.claude.com/docs/ru/errors.md#authentication-errors).

## Связанные ресурсы

* [Обзор шлюзов LLM](https://code.claude.com/docs/ru/llm-gateway): что такое шлюз и как он взаимодействует с подписками claude.ai
* [Развертывание шлюза LLM для вашей организации](https://code.claude.com/docs/ru/llm-gateway-rollout.md): контрольный список, обращенный к администратору, для развертывания и распределения конфигурации шлюза
* [Справочник протокола шлюза](https://code.claude.com/docs/ru/llm-gateway-protocol.md): что Claude Code отправляет на шлюз, включая заголовки и поля, которые шлюз должен пересылать
* [Параметры](https://code.claude.com/docs/ru/settings.md): где находятся файлы параметров и как читается блок `env`
* [Аутентификация](https://code.claude.com/docs/ru/authentication.md): как переменные учетных данных, `apiKeyHelper` и вход OAuth взаимодействуют
