> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code с моделями Claude в Google Cloud (под управлением Anthropic)

> Настройте Claude Code для использования Claude API, который Anthropic предоставляет через ваш проект Google Cloud, с учётными данными Google Cloud, IAM и биллингом через Marketplace.

Модели Claude в Google Cloud (под управлением Anthropic) — это Claude API, который работает под управлением Anthropic и доступен через ваш проект Google Cloud. Чтобы использовать его из Claude Code, войдите в Google Cloud и задайте три переменные окружения.

> [!NOTE]
>
> Google Cloud также предлагает Claude через Agent Platform от Google Cloud (ранее Vertex AI), которой управляет Google. Если вы используете Agent Platform, следуйте вместо этого инструкциям из раздела [Claude Code на Agent Platform от Google Cloud](https://code.claude.com/docs/ru/google-vertex-ai.md). Чтобы узнать, какое из предложений вы используете, см. [Which offering are you using?](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview#which-offering-are-you-using)

Прежде чем начать, [установите Claude Code](https://code.claude.com/docs/ru/setup.md#install-claude-code) версии 2.1.307 или новее. Чтобы проверить версию, выполните `claude --version` в оболочке. Чтобы обновить, выполните `claude update`.

## Предварительные требования

* Проект Google Cloud, в котором завершена [настройка аккаунта](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account)
* [Роль IAM](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) `roles/claude.user` в этом проекте для каждого аккаунта Google или сервисного аккаунта, от имени которого запускается Claude Code
* ID вашего проекта и ваш [ID рабочего пространства](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id), который начинается с `wrkspc_`
* [gcloud CLI](https://cloud.google.com/sdk/docs/install), если вы входите с аккаунтом Google, а не с файлом ключа сервисного аккаунта

## Настройка Claude Code

**1. Создайте Application Default Credentials**

> [tab] Аккаунт Google
>
> Выполните эту команду в оболочке и войдите с аккаунтом Google, у которого есть роль `roles/claude.user`:
>
> ```bash theme={null}
> gcloud auth application-default login
> ```
>
> Выполните её, даже если вы уже выполняли `gcloud auth login`.
>
> Если задана переменная `GOOGLE_APPLICATION_CREDENTIALS`, удалите её. Пока эта переменная задана, Claude Code использует указанный в ней файл и игнорирует учётные данные, сохранённые командой.

> [tab] Файл ключа сервисного аккаунта
>
> В оболочке или CI-задании, в котором запускается Claude Code, задайте `GOOGLE_APPLICATION_CREDENTIALS` равной пути к [файлу ключа сервисного аккаунта](https://docs.cloud.google.com/iam/docs/keys-create-delete). О других источниках учётных данных см. [how to authenticate](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication).

**2. Добавьте переменные в настройки**

Добавьте три переменные в блок `env` вашего [файла пользовательских настроек](https://code.claude.com/docs/ru/settings.md) `~/.claude/settings.json`. Если файла не существует, создайте его со следующим содержимым:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD": "1",
    "ANTHROPIC_GOOGLE_CLOUD_PROJECT": "my-project-id",
    "ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID": "wrkspc_01ABCDEFGHIJKLMN"
  }
}
```

Укажите ID своего проекта и [ID рабочего пространства](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) вместо `my-project-id` и значения `wrkspc_`. Чтобы вместо этого настроить отдельную оболочку или CI-задание, задайте те же три переменные в этом окружении.

Входить в аккаунт Anthropic или выходить из него не нужно.

**3. Запустите Claude Code и проверьте провайдера**

Выполните `claude` в оболочке, затем выполните `/status` в промпте Claude Code. Строка `API provider` содержит `on Google Cloud`, а следующие за ней строки показывают ваши `Workspace ID`, `GCP project` и `GCP location`. Чтобы вывести те же строки из оболочки или CI-задания, выполните [`claude auth status --text`](https://code.claude.com/docs/ru/cli-reference).

Если вы видите `on Google Cloud`, отправьте промпт или выполните `claude -p "hello"` в CI-задании. Ответ подтверждает, что ваши учётные данные и роль IAM работают. Если вы этого не видите или Claude Code показывает ошибку, [устраните неполадки настройки провайдера](#troubleshooting).

### Настройка Claude Code для команды

Поместите блок `env` из шага 2 раздела [Настройка Claude Code](#set-up-claude-code) в файл [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md) на компьютере каждого разработчика. Выдайте каждому разработчику роль `roles/claude.user` в проекте и попросите каждого выполнить `gcloud auth application-default login` на своём компьютере.

## Закрепление версий моделей

Если вы выполняете развёртывание для команды, [закрепите ID моделей](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments), чтобы обновление Claude Code не переводило всех сразу на более новую модель. Добавьте эти переменные в блок `env`, содержащий три переменные из раздела [Настройка Claude Code](#set-up-claude-code):

```json theme={null}
{
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "claude-fable-5-1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001"
  }
}
```

Вместо примеров значений укажите нужные вам ID моделей Claude API из [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## Переменные окружения

| Переменная | Обязательна | Описание |
| - | - | - |
| `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` | Да | Задайте `1`, чтобы отправлять запросы к моделям в Модели Claude в Google Cloud (под управлением Anthropic) |
| `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` | Да, если только вы не задали `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | Ваш ID рабочего пространства |
| `ANTHROPIC_GOOGLE_CLOUD_PROJECT` | Рекомендуется | ID вашего проекта Google Cloud. Без неё Claude Code использует `GOOGLE_CLOUD_PROJECT` |
| `ANTHROPIC_GOOGLE_CLOUD_LOCATION` | Нет | [Location](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution) в URL запроса. По умолчанию `global` |
| `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | Нет | Заменяет базовый URL, который Claude Code формирует из проекта, location и ID рабочего пространства, например адресом [LLM-шлюза](https://code.claude.com/docs/ru/llm-gateway). Claude Code добавляет путь API, например `/v1/messages` |
| `CLAUDE_CODE_SKIP_ANTHROPIC_GOOGLE_CLOUD_AUTH` | Нет | Задайте `1`, если шлюз сам добавляет учётные данные Google, чтобы Claude Code не отправлял токен доступа Google |

## Недоступные функции Claude Code

При использовании Claude Models on Google Cloud (Anthropic managed) недоступны следующие функции:

* [Быстрый режим](https://code.claude.com/docs/ru/fast-mode.md): его нельзя включить с помощью `/fast` или настройки `fastMode`
* [Remote Control](https://code.claude.com/docs/ru/remote-control.md) и [облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md)
* [MCP-коннекторы из claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai)
* [Каналы](https://code.claude.com/docs/ru/channels.md)
* [Команды `/design-sync` и `/import`](https://code.claude.com/docs/ru/commands#all-commands)
* [Настройки, управляемые сервером](https://code.claude.com/docs/ru/server-managed-settings.md). Чтобы применять настройки для вашей команды, используйте вместо этого [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md) на каждом компьютере

Чтобы увидеть другие функции, которые недоступны или поддерживаются частично, выберите вкладку **Google Cloud (Anthropic managed)** в [сводке доступности функций](https://code.claude.com/docs/ru/feature-availability.md#summary-by-provider).

## Устранение неполадок

Если Claude Code просит вас войти или строка `API provider` в `/status` не содержит `on Google Cloud`:

* Убедитесь, что `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` имеет значение `1`
* Убедитесь, что `claude --version` выводит 2.1.307 или новее
* Удалите `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_FOUNDRY` и `CLAUDE_CODE_USE_ANTHROPIC_AWS` из оболочки и ваших [файлов настроек](https://code.claude.com/docs/ru/settings.md#find-or-create-your-settings-files)

`CLAUDE_CODE_USE_VERTEX` можно оставить заданной. После изменения переменной перезапустите Claude Code. Если `/status` не отражает изменение, см. [Заданное значение игнорируется](https://code.claude.com/docs/ru/settings.md#a-value-you-set-is-ignored).

### `No workspace ID found`

Задайте `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` равной вашему [ID рабочего пространства](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id), затем перезапустите Claude Code. Игнорируйте упомянутый в сообщении параметр конструктора `workspaceId`: он предназначен для тех, кто вызывает SDK Anthropic из собственного кода.

### `No project was given`

Задайте `ANTHROPIC_GOOGLE_CLOUD_PROJECT` равной ID вашего проекта Google Cloud, затем перезапустите Claude Code.

### `Could not load Google Cloud credentials`

Повторите шаг 1 раздела [Настройка Claude Code](#set-up-claude-code), используя новый ключ, если вы используете файл ключа сервисного аккаунта.

### `Google Cloud credentials expired or invalid`

Если сообщение предлагает обновить учётные данные Google Cloud, повторите шаг 1 раздела [Настройка Claude Code](#set-up-claude-code). При использовании файла ключа сервисного аккаунта используйте новый ключ.

### `Google Cloud authentication failed`

Выполните шаги для [`Google Cloud credentials expired or invalid`](#google-cloud-credentials-expired-or-invalid). Если это не устранит ошибку:

* **Проект**: в `/status` убедитесь, что в строке `GCP project` указан ваш проект. Если указан другой проект или такой строки нет, следуйте инструкциям для [`No project was given`](#no-project-was-given)
* **Рабочее пространство**: в `/status` убедитесь, что строка `Workspace ID` показывает ваш ID рабочего пространства. Если показан другой, следуйте инструкциям для [`No workspace ID found`](#no-workspace-id-found)
* **Роль IAM**: убедитесь, что у аккаунта Google или сервисного аккаунта, от имени которого запускается Claude Code, есть роль `roles/claude.user` или `roles/claude.admin` в проекте из строки `GCP project`. Чтобы выдать роль, используйте [команду выдачи роли для сервиса](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#before-making-api-calls) или попросите администратора проекта выдать её
* **Сервис**: убедитесь, что сервис `claude.googleapis.com` включён в проекте из строки `GCP project`. Чтобы включить его, выполните [шаги настройки аккаунта для сервиса](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account) или попросите администратора проекта включить его

## Связанные ресурсы

* [Модели Claude в Google Cloud (под управлением Anthropic)](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed): настройка аккаунта, роли IAM, биллинг, хранение данных и поддержка функций
* [Обзор корпоративного развёртывания](https://code.claude.com/docs/ru/third-party-integrations.md): другие способы развёртывания Claude Code, а также настройка прокси и шлюза
* [Конфигурация моделей](https://code.claude.com/docs/ru/model-config.md): псевдонимы моделей, закрепление версии модели и ограничение набора моделей, которые могут выбирать пользователи
