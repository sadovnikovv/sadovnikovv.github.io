> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Google Cloud's Agent Platform

> Узнайте о настройке Claude Code через Google Cloud's Agent Platform, ранее известную как Vertex AI, включая установку, конфигурацию IAM и устранение неполадок.

**Deploying Claude Code across your organization?** Talk to sales about enterprise plans, SSO, and centralized billing.

View plans
Contact sales

> [!NOTE]
>
> На этой странице описан один из двух способов использования Claude через ваш проект Google Cloud: Google Cloud's Agent Platform, ранее известная как Vertex AI, которой управляет Google. Если вы используете Claude Models on Google Cloud (под управлением Anthropic), вместо этого следуйте [её странице настройки Claude Code](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md). Чтобы узнать, какой из вариантов вы используете, см. [Which offering are you using?](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview#which-offering-are-you-using)

## Предварительные требования

Перед настройкой Claude Code с Google Cloud's Agent Platform, ранее известной как Vertex AI, убедитесь, что у вас есть:

* Учетная запись Google Cloud Platform (GCP) с включенной биллингом
* Проект GCP с включенным API Google Cloud's Agent Platform
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.6)
* Установленный и настроенный Google Cloud SDK (`gcloud`)
* Квота, выделенная в нужном регионе GCP

Чтобы войти со своими учетными данными Google Cloud's Agent Platform, следуйте инструкциям [Вход с Google Cloud's Agent Platform](#sign-in-with-agent-platform) ниже. Чтобы развернуть Claude Code для команды, используйте шаги [ручной установки](#set-up-manually) и [закрепите версии ваших моделей](#5-pin-model-versions) перед развертыванием.

## Вход с Agent Platform

Если у вас есть учетные данные Google Cloud и вы хотите начать использовать Claude Code через Agent Platform Google Cloud, мастер входа проведет вас через этот процесс. Вы выполняете предварительные требования на стороне GCP один раз для каждого проекта; мастер обрабатывает сторону Claude Code.

**1. Включите модели Claude в вашем проекте GCP**

[Включите API Agent Platform Google Cloud](#1-enable-agent-platform-api) для вашего проекта, затем запросите доступ к моделям Claude, которые вам нужны, в [Model Garden Agent Platform Google Cloud](https://console.cloud.google.com/vertex-ai/model-garden). См. [Конфигурация IAM](#iam-configuration) для разрешений, которые требуются вашей учетной записи.

**2. Запустите Claude Code и выберите Agent Platform Google Cloud**

Запустите `claude`. В приглашении входа выберите **3rd-party platform**, затем **Google Vertex AI**, метку, которую мастер входа все еще использует для Agent Platform Google Cloud. Если вы уже вошли, запустите `/login` для открытия того же меню.

**3. Следуйте подсказкам мастера**

Выберите способ аутентификации в Google Cloud: Application Default Credentials из `gcloud`, файл ключа сервисного аккаунта или учетные данные, уже находящиеся в вашей среде. Мастер обнаруживает ваш проект и регион, проверяет, какие модели Claude может вызывать ваш проект, и позволяет вам их закрепить. Результат сохраняется в блок `env` вашего [файла пользовательских настроек](https://code.claude.com/docs/ru/settings.md), поэтому вам не нужно самостоятельно экспортировать переменные окружения.

После входа запустите `/setup-vertex` в любое время, чтобы снова открыть мастер и изменить учетные данные, проект, регион или закрепления моделей. Шаг закрепления модели начинается с ваших текущих закрепленных моделей. Мастер записывает данные в `~/.claude/settings.json` или в `$CLAUDE_CONFIG_DIR/settings.json`, когда установлена переменная [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/ru/env-vars#variables).

## Конфигурация региона

Claude Code поддерживает Google Cloud's Agent Platform [глобальные](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), многорегиональные и региональные конечные точки. Установите `CLOUD_ML_REGION` на `global`, многорегиональное местоположение, такое как `eu` или `us`, или конкретный регион, такой как `us-east5`. Claude Code выбирает правильное имя хоста Google Cloud's Agent Platform для каждой формы, включая хосты `aiplatform.eu.rep.googleapis.com` и `aiplatform.us.rep.googleapis.com` для многорегиональных местоположений.

> [!NOTE]
>
> Google Cloud's Agent Platform может не поддерживать модели Claude Code по умолчанию на каждом типе конечной точки. Доступность моделей варьируется в зависимости от [конкретных регионов](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), многорегиональных местоположений и [глобальных конечных точек](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Вам может потребоваться переключиться на поддерживаемое местоположение или указать поддерживаемую модель.

## Ручная установка

Чтобы настроить Google Cloud's Agent Platform через переменные окружения вместо мастера, например в CI или при развертывании в масштабах предприятия, следуйте приведенным ниже шагам.

### Включите API Agent Platform

Включите API Agent Platform Google Cloud в вашем проекте GCP. Замените `YOUR-PROJECT-ID` на ID вашего проекта GCP здесь и на этапе конфигурации ниже:

```bash theme={null}
# Установите ID вашего проекта
gcloud config set project YOUR-PROJECT-ID

# Включите API Agent Platform
gcloud services enable aiplatform.googleapis.com
```

### Запросите доступ к модели

Запросите доступ к моделям Claude в Google Cloud's Agent Platform:

1. Перейдите в [Google Cloud's Agent Platform Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Найдите модели "Claude"
3. Запросите доступ к нужным моделям Claude (например, Claude Sonnet 4.6)
4. Дождитесь одобрения (может занять 24-48 часов)

### Настройте учетные данные GCP

Claude Code использует стандартную аутентификацию Google Cloud.

Для получения дополнительной информации см. [документацию по аутентификации Google Cloud](https://cloud.google.com/docs/authentication).

Claude Code поддерживает [Федерацию рабочих нагрузок на основе сертификатов X.509](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) через ту же цепочку Application Default Credentials. Установите `GOOGLE_APPLICATION_CREDENTIALS` на путь к файлу конфигурации учетных данных.

> [!NOTE]
>
> Claude Code адресует запросы Google Cloud's Agent Platform проекту в `ANTHROPIC_VERTEX_PROJECT_ID`, даже если `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` или файл учетных данных, на который ссылается `GOOGLE_APPLICATION_CREDENTIALS`, содержит другой проект.

#### Расширенная конфигурация учетных данных

Claude Code поддерживает автоматическое обновление учетных данных GCP через параметр `gcpAuthRefresh`. Добавьте его в [файл параметров](https://code.claude.com/docs/ru/settings.md) Claude Code, например `~/.claude/settings.json`. Когда Claude Code обнаруживает, что ваши учетные данные GCP истекли или не могут быть загружены, он запускает настроенную команду для получения новых учетных данных перед повторной попыткой запроса.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

Перед запуском команды Claude Code запрашивает маркер доступа с вашими текущими учетными данными, чтобы подтвердить, что они действительно истекли, и пропускает команду, когда они все еще работают.

Если проверка не завершится в течение пяти секунд, Claude Code также пропускает команду и запускает ее только после того, как запрос завершится с ошибкой учетных данных. До версии 2.1.261 проверка, которая истекла по времени, считалась истекшими учетными данными, поэтому команда могла открыть ваш браузер при запуске, даже если ваши учетные данные были еще действительны.

Claude Code показывает вывод команды, но не может отправлять интерактивный ввод команде. Это хорошо работает для потоков аутентификации на основе браузера, где CLI показывает URL, и вы завершаете аутентификацию в браузере. Команда обновления истекает через три минуты, если аутентификация не завершена. Если вы установите `gcpAuthRefresh` в параметрах проекта, таких как `.claude/settings.json`, Claude Code запускает его в соответствии с тем же [правилом доверия рабочей области, что и hooks в файлах параметров](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder), которое включает сеансы `-p` в папках, которым вы никогда не доверяли.

### Настройте Claude Code

Установите следующие переменные окружения:

```bash theme={null}
# Включите интеграцию Agent Platform
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Опционально: переопределите URL конечной точки Agent Platform для пользовательских конечных точек или шлюзов
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Когда CLOUD_ML_REGION=global, переопределите регион для моделей, которые не поддерживают глобальные конечные точки
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Большинство версий моделей имеют соответствующую переменную `VERTEX_REGION_CLAUDE_*`. Полный список см. в [справочнике переменных окружения](https://code.claude.com/docs/ru/env-vars.md#variables). Проверьте [Google Cloud's Agent Platform Model Garden](https://console.cloud.google.com/vertex-ai/model-garden), чтобы определить, какие модели поддерживают глобальные эндпоинты, а какие только региональные.

Если значение региона не похоже на имя региона или местоположения, Claude Code рассматривает его как неустановленное. Например, Claude Code рассматривает значение, содержащее косую черту, точку или пробел, как неустановленное. Claude Code откатывается на другой источник для каждой переменной:

* `VERTEX_REGION_CLAUDE_*`: Claude Code откатывается на `CLOUD_ML_REGION`.
* `CLOUD_ML_REGION`: Claude Code откатывается на `us-east5`.

[Кэширование запросов](https://code.claude.com/docs/ru/prompt-caching.md) включается автоматически. Чтобы отключить его, установите `DISABLE_PROMPT_CACHING=1`. Чтобы запросить TTL кэша на 1 час вместо стандартного 5-минутного, установите `ENABLE_PROMPT_CACHING_1H=1`; записи кэша с TTL на 1 час тарифицируются по более высокому тарифу. Чтобы установить разные TTL для вашего основного разговора и для запросов, которые Claude Code делает вне его, [выберите TTL самостоятельно](https://code.claude.com/docs/ru/prompt-caching.md#choose-the-ttl-yourself).

Чтобы повысить ваши лимиты скорости, обратитесь в поддержку Google Cloud. При использовании Google Cloud's Agent Platform команда `/logout` недоступна, так как аутентификация обрабатывается через учетные данные Google Cloud.

Claude Code выбирает между [поиском инструментов MCP](https://code.claude.com/docs/ru/mcp.md#scale-with-mcp-tool-search) и предварительной загрузкой по поколению модели:

* **Claude Opus 4.5, Sonnet 4.5, Haiku 4.5 и позже**: Claude Code включает поиск инструментов по умолчанию.
* **Более ранние модели**: Claude Code загружает определения инструментов MCP заранее, потому что их стеки обслуживания Agent Platform отклоняют требуемый бета-заголовок. Установка `ENABLE_TOOL_SEARCH=true` не переопределяет это.

Установите `ENABLE_TOOL_SEARCH=false`, чтобы отключить поиск инструментов на каждой модели.

### Закрепите версии моделей

> [!WARNING]
>
> Закрепите конкретные версии моделей при развертывании для нескольких пользователей. Без закрепления псевдонимы моделей, такие как `sonnet` и `opus`, разрешаются в встроенное значение по умолчанию Claude Code для Google Cloud's Agent Platform, которое может отставать от последнего выпуска и может быть еще не включено в вашем проекте. Claude Code [откатывается](#startup-model-checks) на предыдущую версию или модель более низкого уровня при запуске, когда значение по умолчанию недоступно, но закрепление позволяет вам контролировать, когда ваши пользователи переходят на новую модель.

Установите эти переменные окружения на конкретные ID моделей Google Cloud's Agent Platform.

Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` на Google Cloud's Agent Platform разрешается в Opus 5.5, а без `ANTHROPIC_DEFAULT_SONNET_MODEL` псевдоним `sonnet` разрешается в Sonnet 4.5. Этот пример закрепляет каждый псевдоним на конкретную версию:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Для текущих и устаревших ID моделей см. [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Полный список переменных окружения см. в разделе [Конфигурация моделей](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments).

Claude Code использует эти модели по умолчанию, когда переменные закрепления не установлены:

| Тип модели | Значение по умолчанию |
| :- | :- |
| Основная модель | `claude-opus-5-5` |
| Малая/быстрая модель | `claude-sonnet-4-5@20250929` |

До версии 2.1.280 основная модель на Google Cloud's Agent Platform по умолчанию была Opus 5, и псевдоним `opus` разрешался в Opus 5 с версии 2.1.219.

Фоновые задачи, такие как генерация названия сеанса, используют малую/быструю модель, обычно модель класса Haiku. На Google Cloud's Agent Platform Claude Code использует модель Sonnet по умолчанию для фоновых задач, потому что Haiku может быть не включен в каждом проекте или регионе. Два выбора изменяют, какая модель их выполняет:

* Когда вы выбираете основную модель с помощью `--model`, `ANTHROPIC_MODEL` или параметра `model`, фоновые задачи используют эту модель. Когда Claude Code запускает сеанс на модели, которую вы установили с помощью [`ANTHROPIC_DEFAULT_MODEL`](https://code.claude.com/docs/ru/model-config#set-a-default-model-for-new-sessions), фоновые задачи используют эту модель тоже. Установка `ANTHROPIC_DEFAULT_OPUS_MODEL` без `ANTHROPIC_DEFAULT_SONNET_MODEL` также считается выбором, потому что встроенная модель Sonnet может быть не включена в проекте, который управляет своим собственным Opus.
* Чтобы использовать Haiku для фоновых задач, установите `ANTHROPIC_DEFAULT_HAIKU_MODEL` на ID модели, который доступен в вашем проекте.

> [!WARNING]
>
> Модели Opus имеют более высокую цену за токен, чем модели Sonnet, поэтому если вы не закрепите основную модель, тарификация будет производиться по тарифу Opus. Чтобы использовать Sonnet 4.5 в качестве основной модели, установите `ANTHROPIC_MODEL` на его полный ID модели. Развертывание, которое управляет значением по умолчанию с помощью `ANTHROPIC_DEFAULT_SONNET_MODEL` и не устанавливает `ANTHROPIC_DEFAULT_OPUS_MODEL`, сохраняет свою управляемую модель Sonnet в качестве значения по умолчанию.

Для дальнейшей настройки моделей:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

### Проверьте вашу конфигурацию

Запустите Claude Code и выполните `/status`, чтобы подтвердить установку. Строка `API provider` показывает `Google Vertex AI`, а строки `GCP project`, `Default region` и `Model` показывают ID вашего проекта, регион и разрешенную модель. Если строка provider отсутствует, переменные окружения не достигают процесса. Подтвердите, что они экспортированы в оболочке, где вы запустили `claude`, или установите их в блоке `env` вашего [файла параметров](https://code.claude.com/docs/ru/settings.md).

## Проверки моделей при запуске

Когда Claude Code запускается с настроенной Agent Platform от Google Cloud, он проверяет, доступны ли в вашем проекте модели, которые он собирается использовать.

Возможно, вы закрепили версию модели, которая старше текущей версии по умолчанию в Claude Code. Если ваш проект может вызывать более новую версию, Claude Code предложит обновить закреплённую версию:

* **Если вы согласитесь**: Claude Code запишет новый идентификатор модели в ваш [файл пользовательских настроек](https://code.claude.com/docs/ru/settings.md) и перезапустится
* **Если вы откажетесь**: Claude Code запомнит ваш выбор до следующей смены версии по умолчанию

Для закреплённой версии в блоке `env` [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md) Claude Code не выполняет проверку и не предлагает обновление. Если предложение обновления всё равно появляется для этой закреплённой версии, обновите Claude Code до версии 2.1.314 или новее. До версии 2.1.314 управляемая закреплённая версия оставалась в силе после вашего согласия, поэтому предложение появлялось снова при следующем запуске.

Если вы не закрепили модель и текущая модель по умолчанию недоступна в вашем проекте, Claude Code использует резервный вариант для текущей сессии и показывает уведомление. Сначала он пробует более ранние версии модели по умолчанию, а если модель по умолчанию относится к Opus и ни одна версия Opus не доступна, переключается на модель Sonnet по умолчанию. Резервный вариант не сохраняется. Включите более новую модель в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) или [закрепите версию](#5-pin-model-versions), чтобы сделать выбор постоянным.

### Запуск сессии на конкретной модели

Когда вы запускаете сессию на конкретной версии Sonnet или Opus, например с помощью `--model`, `ANTHROPIC_MODEL` или [настройки `model`](https://code.claude.com/docs/ru/settings-reference#model), эта версия выступает закреплённой моделью по умолчанию для сессии для соответствующего псевдонима `sonnet` или `opus`. Claude Code пропускает проверку доступности встроенной модели по умолчанию, которую заменяет ваша модель, и запускается на настроенной вами модели без уведомления о резервном варианте.

Когда вы запускаете сессию на псевдониме модели, например `opus`, или на идентификаторе модели, который Claude Code не распознаёт, это значение не считается закреплением.

### Запомненные отказы в доступе к моделям

Когда проверки моделей при запуске обнаруживают модель, которую ваш проект не может вызвать, Claude Code может запомнить отказ на этом компьютере на срок до одного дня. Если с последней проверки прошло десять минут, Claude Code при запуске заново проверяет запомненный отказ для текущей модели по умолчанию. Благодаря этому модель по умолчанию, которую ваш администратор снова включил, возвращается. Чтобы отключить это запоминание, установите [`CLAUDE_CODE_SKIP_MODEL_ACCESS_MEMORY=1`](https://code.claude.com/docs/ru/env-vars).

### Когда ваша организация применяет список разрешённых моделей

Если вы задали [`enforceAvailableModels`](https://code.claude.com/docs/ru/model-config#enforce-the-allowlist-for-the-default-model) в управляемых настройках, проверки моделей при запуске используют только модели, разрешённые вашим списком `availableModels`. Для этого требуется Claude Code версии 2.1.287 или новее. Список без `enforceAvailableModels` не ограничивает эти проверки.

Проверки сравнивают каждую запись с идентификатором модели, который они отправили бы в Agent Platform, поэтому указывайте в списке именно такие идентификаторы. Этот пример разрешает Opus 4.8 и Sonnet 4.5:

```json theme={null}
{
  "availableModels": ["claude-opus-4-8", "claude-sonnet-4-5@20250929"],
  "enforceAvailableModels": true
}
```

О псевдонимах, префиксах версий и записях `modelOverrides` см. [Закрепление моделей для сторонних развёртываний](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments).

### Когда модель отключается во время сессии

Когда Agent Platform отклоняет модель вашей сессии как недоступную в вашем проекте или регионе, Claude Code переключает сессию на другую модель, и вы можете продолжать работу. Вы увидите сообщение, которое начинается с `Switched to <fallback> because <model> is not available`. Это происходит, например, когда администратор отключает модель в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) или она не предоставляется в вашем регионе.

Если вы настроили [цепочку резервных моделей](https://code.claude.com/docs/ru/model-config.md#fallback-model-chains), Claude Code вместо этого переключается на настроенную вами резервную модель. Без цепочки запрос завершается ошибкой, например в таких случаях:

* Ваша сессия работает на закреплённой модели или на выбранной вами конкретной версии
* Ни одна из [моделей, которые пробует Claude Code](#startup-model-checks), не доступна. В [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#enable-auto-mode-on-bedrock-agent-platform-or-foundry) Claude Code переключается только на модель, которую авторежим поддерживает на Agent Platform.

Чтобы продолжить работу, выполните `/model` в сессии и нажмите `s` на модели, доступной в вашем проекте и регионе; при этом ваша модель по умолчанию не изменится.

Чтобы отклонённые запросы завершались ошибкой, а не приводили к переключению, установите [`CLAUDE_CODE_DISABLE_MODEL_ACCESS_FALLBACK=1`](https://code.claude.com/docs/ru/env-vars). Если вы настроили цепочку резервных моделей, удалите и её, поскольку Claude Code всё равно переключится на эту резервную модель.

## Конфигурация IAM

Назначьте роль `roles/aiplatform.user`, которая включает требуемые разрешения:

* `aiplatform.endpoints.predict` - требуется для вызова модели и подсчета токенов

Для более строгих разрешений создайте пользовательскую роль только с указанными выше разрешениями.

Для получения дополнительной информации см. [документацию Google Cloud Agent Platform IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

> [!NOTE]
>
> Создайте выделенный проект GCP для Claude Code, чтобы упростить отслеживание затрат и контроль доступа.

## Контекстное окно с 1M токенов

Модели Fable, Sonnet 5 и более поздние версии, а также Opus 4.7 и более поздние версии по умолчанию работают с [контекстным окном с 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model) на платформе Agent Platform Google Cloud, без необходимости добавлять суффикс `[1m]`. Чтобы вместо этого сохранить окно 200K, установите [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](https://code.claude.com/docs/ru/model-config#turn-off-1m-context).

Opus 4.6 и Sonnet 4.6 получают окно 1M при выборе их варианта `[1m]`. [Мастер установки](#sign-in-with-agent-platform) предлагает опцию контекстного окна с 1M при закреплении моделей. Чтобы вместо этого включить его для вручную закреплённой модели, добавьте `[1m]` к ID модели. Подробности см. в разделе [Закрепите модели для развёртываний третьих сторон](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments), включая способы использования окна 1M без изменения закрепления.

До версии v2.1.287 модели Fable, а также Opus 4.7 и более поздние версии по умолчанию работали с окном 200K на платформе Agent Platform Google Cloud и получали окно 1M через суффикс `[1m]`.

## Устранение неполадок

Если вы столкнулись с ошибками "Could not load the default credentials":

* Запустите `gcloud auth application-default login` для установки Application Default Credentials
* Установите `GOOGLE_APPLICATION_CREDENTIALS` на путь файла ключа сервисного аккаунта
* См. [Configure GCP credentials](#3-configure-gcp-credentials) для всех вариантов

Если вы столкнулись с проблемами квоты:

* Проверьте текущие квоты или запросите увеличение квоты через [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Если вы столкнулись с ошибками "model not found" 404:

* Подтвердите, что модель включена в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Проверьте, что модель доступна в указанном вами местоположении. Некоторые модели предлагаются только на `global` или многорегиональных местоположениях, таких как `eu` и `us`, а не в конкретных регионах
* Если вы используете `CLOUD_ML_REGION=global`, проверьте, что ваши модели поддерживают глобальные эндпоинты в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) в разделе "Supported features". Для моделей, которые не поддерживают глобальные эндпоинты, либо:
  * Укажите поддерживаемую модель через `ANTHROPIC_MODEL` или `ANTHROPIC_DEFAULT_HAIKU_MODEL`, либо
  * Установите регион или многорегиональное местоположение с помощью переменной `VERTEX_REGION_CLAUDE_*` для соответствующей модели, указанной в [справочнике по переменным окружения](https://code.claude.com/docs/ru/env-vars.md#variables)

Если вы столкнулись с ошибками 429:

* Для региональных конечных точек убедитесь, что основная модель и малая/быстрая модель поддерживаются в выбранном регионе
* Рассмотрите возможность переключения на `CLOUD_ML_REGION=global` для лучшей доступности

## Дополнительные ресурсы

* [Документация Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai/docs)
* [Цены Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai/pricing)
* [Квоты и лимиты Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai/docs/quotas)
