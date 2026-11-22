> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Microsoft Foundry

> Узнайте о настройке Claude Code через Microsoft Foundry, включая установку, конфигурацию и устранение неполадок.

**Deploying Claude Code across your organization?** Talk to sales about enterprise plans, SSO, and centralized billing.

View plans
Contact sales

## Предварительные требования

Перед настройкой Claude Code с Microsoft Foundry убедитесь, что у вас есть:

* Подписка Azure с доступом к Microsoft Foundry
* Разрешения RBAC для создания ресурсов и развертываний Microsoft Foundry
* Azure CLI установлен и настроен (опционально - требуется только если у вас нет другого механизма для получения учетных данных)

> [!NOTE]
>
> Если вы развертываете Claude Code для нескольких пользователей, [закрепите версии вашей модели](#4-pin-model-versions) перед развертыванием.

## Установка

### Подготовка ресурса Microsoft Foundry

Сначала создайте ресурс Claude в Azure:

1. Перейдите на [портал Microsoft Foundry](https://ai.azure.com/)
2. Создайте новый ресурс, отметив имя вашего ресурса
3. Создайте развёртывания для моделей Claude, отметив имя развёртывания, которое вы даёте каждому; вы установите эти имена как переменные модели на шаге 4:

   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

   При настройке развёртывания вы также выбираете его [вариант размещения](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options), который определяет, выполняется ли вывод на Azure или на инфраструктуре Anthropic.

### Настройка учётных данных Azure

Claude Code поддерживает три метода аутентификации для Microsoft Foundry. Выберите метод, который лучше всего соответствует вашим требованиям безопасности:

* [API-ключ](#use-an-api-key): вы копируете ключ на портале Microsoft Foundry и устанавливаете его как `ANTHROPIC_FOUNDRY_API_KEY`
* [Microsoft Entra ID](#use-microsoft-entra-id): Claude Code получает токены через цепочку учётных данных по умолчанию Azure SDK, например из сессии `az login`, поэтому хранить API-ключ не нужно
* [Bearer-токен](#use-a-bearer-token): другой процесс получает токен доступа Microsoft Entra ID, и вы передаёте его в `ANTHROPIC_FOUNDRY_AUTH_TOKEN`

> [!NOTE]
>
> При использовании Microsoft Foundry команда `/logout` недоступна, так как аутентификация обрабатывается через учётные данные Azure.

#### Использование API-ключа

Скопируйте ключ на портале Microsoft Foundry, затем установите его как переменную окружения:

1. Перейдите к вашему ресурсу на портале Microsoft Foundry
2. Откройте раздел **Endpoints and keys**
3. Скопируйте **API Key**
4. Установите переменную окружения, заменив `your-azure-api-key` на скопированный ключ:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

#### Использование Microsoft Entra ID

Оставьте `ANTHROPIC_FOUNDRY_API_KEY` и `ANTHROPIC_FOUNDRY_AUTH_TOKEN` неустановленными. Тогда Claude Code использует Azure SDK [цепочку учётных данных по умолчанию](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
Это поддерживает различные методы аутентификации локальных и удалённых рабочих нагрузок.

На локальном компьютере войдите с помощью Azure CLI:

```bash theme={null}
az login
```

О ролях, необходимых вашей учётной записи, см. [Конфигурация Azure RBAC](#azure-rbac-configuration).

#### Использование Bearer-токена

Claude Code отправляет значение `ANTHROPIC_FOUNDRY_AUTH_TOKEN` в каждом запросе в качестве заголовка `Authorization: Bearer`. Используйте этот вариант, когда другой процесс, такой как хост-приложение или скрипт входа, уже получил для вас токен доступа.

Установите переменную на токен Bearer, выданный Microsoft Entra ID для вашего ресурса:

```bash theme={null}
export ANTHROPIC_FOUNDRY_AUTH_TOKEN=your-entra-access-token
```

`ANTHROPIC_FOUNDRY_AUTH_TOKEN` имеет приоритет над `ANTHROPIC_FOUNDRY_API_KEY` и над цепочкой учётных данных по умолчанию.

### Настройка Claude Code

Установите следующие переменные окружения для включения интеграции Microsoft Foundry:

```bash theme={null}
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

Установите в `ANTHROPIC_FOUNDRY_RESOURCE` только имя ресурса, например `my-resource`. Claude Code [отклоняет URL или имя хоста](https://code.claude.com/docs/ru/errors.md#anthropic-foundry-resource-must-be-a-foundry-resource-name) при отправке сообщения.

### Закрепление версий моделей

> [!WARNING]
>
> Закрепите конкретные версии моделей для каждого развёртывания. Без закрепления псевдонимы моделей, такие как `sonnet` и `opus`, разрешаются во встроенное значение Claude Code по умолчанию для Microsoft Foundry. Это значение по умолчанию может отставать от последнего выпуска и может быть ещё недоступно в вашей учётной записи.
>
> Если в вашем ресурсе нет развёртывания для значения по умолчанию, Claude Code переключается на более старую модель или запрос завершается ошибкой. При переключении отображается сообщение, начинающееся с `Switched to <fallback> because <model> is not available`. При создании развёртываний Azure выберите конкретную версию модели вместо "автоматического обновления до последней версии".

Установите переменные модели в соответствии с именами развёртываний, которые вы создали на шаге 1.

Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` на Microsoft Foundry разрешается в Opus 4.6. Установите его на идентификатор более новой модели Opus, такой как Opus 4.8:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Фоновые задачи, такие как генерация заголовков сессий, используют небольшую/быструю модель, обычно модель класса Haiku. На Microsoft Foundry Claude Code по умолчанию использует основную модель, потому что не каждая учётная запись имеет развёртывание Haiku. Чтобы использовать Haiku для фоновых задач, установите `ANTHROPIC_DEFAULT_HAIKU_MODEL` на развёртывание Haiku, доступное в вашей учётной записи, как показано выше.

Для получения текущих и устаревших идентификаторов моделей см. [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Полный список переменных окружения см. в разделе [Конфигурация модели](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments).

[Кэширование промптов](https://code.claude.com/docs/ru/prompt-caching.md) включено автоматически. Чтобы запросить TTL кэша в 1 час вместо стандартного 5-минутного, установите следующую переменную; записи кэша с TTL в 1 час выставляются по более высокому тарифу:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

Чтобы установить разные TTL для вашего основного диалога и для запросов, которые Claude Code делает вне его, [выберите TTL самостоятельно](https://code.claude.com/docs/ru/prompt-caching.md#choose-the-ttl-yourself).

### Запуск Claude Code

С установленными переменными окружения запустите Claude Code из каталога вашего проекта:

```bash theme={null}
claude
```

Claude Code читает `CLAUDE_CODE_USE_FOUNDRY` и другие переменные Microsoft Foundry из окружения и подключается к вашему ресурсу Azure при первом промпте. В отличие от Amazon Bedrock и Google Cloud's Agent Platform, Microsoft Foundry не имеет интерактивного мастера установки, поэтому переменные окружения на шагах 3 и 4 являются единственным путём конфигурации.

Чтобы проверить вашу установку, запустите `/status` внутри Claude Code. Строка поставщика API показывает `Microsoft Foundry` вместе с именем ресурса или базовым URL-адресом, который вы настроили.

## Конфигурация Azure RBAC

Если вы проходите аутентификацию с помощью Microsoft Entra ID или выданного им Bearer-токена, назначьте своему удостоверению роль `Foundry User` или `Cognitive Services User` в вашем ресурсе Foundry. Роль `Foundry User` может по-прежнему отображаться под своим прежним названием — `Azure AI User`.

Если эти роли не соответствуют вашим потребностям, см. [документацию Microsoft Foundry RBAC](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry), чтобы узнать о пользовательских ролях.

## Контекстное окно на 1M токенов

В Microsoft Foundry модели Fable, Sonnet 5 и более поздние, а также Opus 4.7 и более поздние по умолчанию работают с [контекстным окном на 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model). Суффикс `[1m]` для этого не требуется, если Claude Code может определить, какую модель обслуживает ваше развёртывание.

> [!NOTE]
>
> Claude Code определяет модель по имени развёртывания в ваших переменных модели. Назовите каждое развёртывание по идентификатору его модели, например `claude-opus-4-8`, или сопоставьте модель с именем вашего развёртывания с помощью [`modelOverrides`](https://code.claude.com/docs/ru/model-config#override-model-ids-per-version).

Эта запись в `settings.json` сообщает Claude Code, что развёртывание с именем `team-opus-prod` обслуживает Opus 4.8:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-8": "team-opus-prod"
  }
}
```

Чтобы вместо этого сохранить окно размером 200K, задайте [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](https://code.claude.com/docs/ru/model-config#turn-off-1m-context).

Если Claude Code не удаётся сопоставить имя развёртывания с моделью, он по умолчанию предполагает окно на 1M, поэтому [укажите реальный размер окна](https://code.claude.com/docs/ru/model-config.md#correct-the-window-for-a-gateway-or-custom-model-id), если развёрнутая модель принимает меньше. До версии v2.1.323 Claude Code по умолчанию предполагал окно на 200K, поэтому в этих версиях добавьте `[1m]` к имени в ваших переменных модели, если модель принимает 1M.

Opus 4.6 и Sonnet 4.6 получают окно на 1M, если добавить `[1m]` к имени развёртывания в `ANTHROPIC_DEFAULT_OPUS_MODEL` или `ANTHROPIC_DEFAULT_SONNET_MODEL`, как описано в разделе [Закрепление моделей для сторонних развёртываний](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments). До версии v2.1.287 моделям Fable, а также Opus 4.7 и более поздним в Microsoft Foundry тоже требовался этот суффикс, а без него они по умолчанию работали с окном размером 200K.

## Устранение неполадок

Если вы получаете ошибку "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Настройте Entra ID в среде или установите `ANTHROPIC_FOUNDRY_API_KEY`.

Если запросы завершаются с ошибками повторного подключения на первом запросе:

* Проверьте, что `ANTHROPIC_FOUNDRY_RESOURCE` установлен на ваше фактическое имя ресурса, а не на заполнитель. Claude Code создает URL конечной точки из этого значения, поэтому неправильное имя указывает на хост, который не существует.

## Дополнительные ресурсы

* [Документация Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Модели Microsoft Foundry](https://ai.azure.com/explore/models)
* [Цены Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
