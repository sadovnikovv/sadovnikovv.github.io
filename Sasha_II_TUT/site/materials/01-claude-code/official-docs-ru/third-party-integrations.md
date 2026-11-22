> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор корпоративного развертывания

> Узнайте, как Claude Code может интегрироваться с различными сторонними сервисами и инфраструктурой для удовлетворения требований корпоративного развертывания.

Организации могут развертывать Claude Code непосредственно через Anthropic или через поставщика облачных услуг. Эта страница поможет вам выбрать правильную конфигурацию.

**Deploying Claude Code across your organization?** Talk to sales about enterprise plans, SSO, and centralized billing.

View plans
Contact sales

## Сравнение вариантов развертывания

Для большинства организаций Claude for Teams или Claude for Enterprise обеспечивает лучший опыт. Члены команды получают доступ как к Claude Code, так и к Claude в веб-версии с одной подпиской, централизованным выставлением счетов и без необходимости настройки инфраструктуры.

**Claude for Teams** — это самообслуживаемое решение, которое включает функции сотрудничества, инструменты администратора, SSO, управление выставлением счетов и [управляемые параметры сервера](https://code.claude.com/docs/ru/server-managed-settings.md) для конфигурации Claude Code на уровне организации. Лучше всего подходит для небольших команд, которым нужно быстро начать работу.

**Claude for Enterprise** добавляет захват домена, разрешения на основе ролей и доступ к API соответствия требованиям. Лучше всего подходит для крупных организаций с требованиями безопасности и соответствия требованиям.

Узнайте больше о [планах Team](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) и [планах Enterprise](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Варианты развертывания, сравниваемые ниже, охватывают место, где выполняется вывод модели. Для запуска сеансов [Claude Code в веб-версии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) на вычислительных ресурсах, которыми управляет ваша организация, см. [самостоятельно размещаемые окружения](https://code.claude.com/docs/ru/self-hosted-environments).

Если ваша организация имеет специфические требования к инфраструктуре, сравните варианты ниже:

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform, ранее Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Лучше всего подходит для</td>
      <td>Большинства организаций (рекомендуется)</td>
      <td>Отдельных разработчиков</td>
      <td>Развертываний, собственных для AWS</td>
      <td>Выставление счетов AWS Marketplace с функциями Claude API</td>
      <td>Развертываний, собственных для GCP</td>
      <td>Развертываний, собственных для Azure</td>
    </tr>

    <tr>
      <td>Выставление счетов</td>
      <td>**Teams:** подписка за место с доступной оплатой по мере использования, см. [цены](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=third_party_pricing#team-&-enterprise)\
      **Enterprise:** [Свяжитесь с отделом продаж](https://claude.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=third_party_enterprise)</td>
      <td>Оплата по мере использования</td>
      <td>Оплата по мере использования через AWS</td>
      <td>Оплата по мере использования через AWS Marketplace</td>
      <td>Оплата по мере использования через GCP</td>
      <td>Оплата по мере использования через Azure</td>
    </tr>

    <tr>
      <td>Регионы</td>
      <td>Поддерживаемые [страны](https://www.anthropic.com/supported-countries)</td>
      <td>Поддерживаемые [страны](https://www.anthropic.com/supported-countries)</td>
      <td>Несколько AWS [регионов](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Несколько регионов AWS</td>
      <td>Несколько GCP [регионов](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Несколько Azure [регионов](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
    </tr>

    <tr>
      <td>Аутентификация</td>
      <td>claude.ai SSO или электронная почта</td>
      <td>API ключ или [вход в Console без него](https://code.claude.com/docs/ru/authentication.md#sign-in-without-an-api-key)</td>
      <td>API ключ или учетные данные AWS</td>
      <td>API ключ или учетные данные AWS</td>
      <td>Учетные данные GCP</td>
      <td>API ключ или Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Отслеживание затрат</td>
      <td>Панель использования</td>
      <td>Панель использования</td>
      <td>AWS Cost Explorer</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Включает Claude в веб-версии</td>
      <td>Да</td>
      <td>Нет</td>
      <td>Нет</td>
      <td>Нет</td>
      <td>Нет</td>
      <td>Нет</td>
    </tr>

    <tr>
      <td>Функции Enterprise</td>
      <td>Управление командой, SSO, мониторинг использования</td>
      <td>Нет</td>
      <td>Политики IAM, CloudTrail</td>
      <td>Политики IAM, CloudTrail</td>
      <td>Роли IAM, Cloud Audit Logs</td>
      <td>Политики RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Для подробного сравнения функций, доступных в каждом варианте, см. [Доступность функций](https://code.claude.com/docs/ru/feature-availability.md).

Выберите вариант развертывания для просмотра инструкций по настройке:

* [Claude for Teams или Enterprise](https://code.claude.com/docs/ru/authentication.md#claude-for-teams-or-enterprise)
* [Anthropic Console](https://code.claude.com/docs/ru/authentication.md#claude-console-authentication)
* [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway), самостоятельно размещаемый шлюз, который добавляет вход через IdP перед Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry или Anthropic API
* [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md)
* [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md)
* [Claude Models on Google Cloud (под управлением Anthropic)](https://code.claude.com/docs/ru/claude-models-on-google-cloud-anthropic-managed.md)
* [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md)
* [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md)

Для Amazon Bedrock и Google Vertex AI вы также можете запустить `claude` и выбрать **3rd-party platform** в приглашении входа для запуска интерактивного мастера настройки.

## Настройка прокси и шлюзов

Большинство организаций могут использовать поставщика облачных услуг напрямую без дополнительной конфигурации. Однако вам может потребоваться настроить корпоративный прокси или шлюз LLM, если ваша организация имеет специфические требования к сети или управлению. Это разные конфигурации, которые можно использовать вместе:

* **Корпоративный прокси**: маршрутизирует трафик через прокси HTTP/HTTPS. Используйте это, если ваша организация требует, чтобы весь исходящий трафик проходил через прокси-сервер для мониторинга безопасности, соответствия требованиям или обеспечения политики сети. Настройте с помощью переменных окружения `HTTPS_PROXY` или `HTTP_PROXY`. Узнайте больше в разделе [Конфигурация корпоративной сети](https://code.claude.com/docs/ru/network-config.md).
* **Шлюз LLM**: сервис, который находится между Claude Code и поставщиком облачных услуг для обработки аутентификации и маршрутизации. Используйте это, если вам нужно централизованное отслеживание использования между командами, пользовательское ограничение скорости или бюджеты, или централизованное управление аутентификацией. Настройте с помощью переменных окружения `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, `ANTHROPIC_AWS_BASE_URL`, `ANTHROPIC_VERTEX_BASE_URL` или `ANTHROPIC_FOUNDRY_BASE_URL`. Узнайте больше в разделе [Шлюзы LLM](https://code.claude.com/docs/ru/llm-gateway).

Для переменных окружения для каждого поставщика, которые маршрутизируют Amazon Bedrock, Microsoft Foundry или Google Cloud's Agent Platform через шлюз LLM, см. раздел [маршрутизация к поставщику облачных услуг через шлюз](https://code.claude.com/docs/ru/llm-gateway-connect.md#route-to-a-cloud-provider-through-a-gateway). Запустите `/status` в Claude Code для проверки того, какой поставщик, базовый URL и прокси использует сеанс.

Если ваша организация использует [ключи шифрования, управляемые клиентом](https://platform.claude.com/docs/en/manage-claude/cmek) (CMEK) и маршрутизирует Claude Code через шлюз LLM или пользовательский `ANTHROPIC_BASE_URL`, CMEK не применяется к операционной телеметрии Claude Code в этих сеансах. Чтобы отключить телеметрию для каждого разработчика, доставьте `DISABLE_TELEMETRY` через управляемые параметры, как показано в разделе [Отключение телеметрии для вашей организации](https://code.claude.com/docs/ru/managed-settings.md#turn-telemetry-off-for-your-organization).

## Лучшие практики для организаций

### Инвестируйте в документацию и память

Инвестируйте в документацию, чтобы Claude Code понимал вашу кодовую базу. Организации могут развёртывать файлы CLAUDE.md на нескольких уровнях. См. [где могут находиться файлы CLAUDE.md](https://code.claude.com/docs/ru/memory.md#choose-where-to-put-claude-md-files) и [как развернуть организационный файл CLAUDE.md](https://code.claude.com/docs/ru/memory.md#deploy-organization-wide-claude-md).

### Упростите развертывание

Если у вас есть пользовательская среда разработки, создание способа установки Claude Code «в один клик» является ключом к расширению внедрения в организации.

### Начните с управляемого использования

Поощряйте новых пользователей попробовать Claude Code для вопросов и ответов по кодовой базе, или на небольших исправлениях ошибок или запросах функций. Попросите Claude Code составить план. Проверьте предложения Claude и дайте обратную связь, если что-то не так. Со временем, по мере того как пользователи лучше поймут эту новую парадигму, они будут более эффективны в том, чтобы позволить Claude Code работать более агентивно.

### Закрепите версии моделей для поставщиков облачных услуг

Если вы развертываете через [Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/ru/google-vertex-ai.md), [Microsoft Foundry](https://code.claude.com/docs/ru/microsoft-foundry.md) или [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md), закрепите конкретные версии моделей, используя `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` и `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Без закрепления, псевдонимы моделей разрешаются на встроенное значение по умолчанию Claude Code для этого поставщика, что может отставать от последнего выпуска и может быть еще не включено в вашей учетной записи. Закрепление позволяет вам контролировать, когда ваши пользователи переходят на новую модель. См. раздел [Конфигурация модели](https://code.claude.com/docs/ru/model-config.md#pin-models-for-third-party-deployments) для получения информации о том, что делает каждый поставщик, когда значение по умолчанию недоступно.

### Настройте политики безопасности

Команды безопасности могут настроить управляемые разрешения для того, что Claude Code может и не может делать, которые не могут быть переопределены локальной конфигурацией. [Узнайте больше](https://code.claude.com/docs/ru/security.md).

Чтобы ограничить, какие из этих вариантов развертывания может использовать управляемая машина, установите [`allowedProviders`](https://code.claude.com/docs/ru/settings-reference#allowedproviders) в управляемых параметрах. Например, `["bedrock"]` разрешает Amazon Bedrock и ничего больше; флот Bedrock, который также включает конечную точку Mantle, также указывает `"mantle"`. Запись указывает, какие переменные конечной точки также требуют управляемого закрепления `env`. Требуется Claude Code v2.1.285 или более поздняя версия.

> [!NOTE]
>
> Если в Desktop выполнен вход в claude.ai, сессия Cowork на компьютере пользователя считается как [`"anthropic"`](https://code.claude.com/docs/ru/settings-reference#allowedproviders). Если вы не включите это значение в список в политике MDM или файле управляемых настроек, такая сессия будет отклонена. Если оно включено, сессии, отправляемые напрямую в Anthropic, также проходят проверку по этому списку.

### Используйте MCP для интеграций

MCP — это отличный способ предоставить Claude Code больше информации, такую как подключение к системам управления тикетами или логам ошибок. Пусть одна центральная команда настроит MCP-серверы и добавит конфигурацию `.mcp.json` в кодовую базу, чтобы все пользователи получали выгоду. [Узнайте больше](https://code.claude.com/docs/ru/mcp.md).

## Следующие шаги

После того как вы выбрали вариант развертывания и настроили доступ для вашей команды:

1. **Развертывание в вашей команде**: поделитесь инструкциями по установке и попросите членов команды [установить Claude Code](https://code.claude.com/docs/ru/setup.md) и аутентифицироваться с помощью своих учетных данных.
2. **Настройте общую конфигурацию**: создайте [файл CLAUDE.md](https://code.claude.com/docs/ru/memory.md) в ваших репозиториях, чтобы помочь Claude Code понять вашу кодовую базу и стандарты кодирования.
3. **Настройте разрешения**: просмотрите [параметры безопасности](https://code.claude.com/docs/ru/security.md) для определения того, что Claude Code может и не может делать в вашей среде.
