> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Claude Platform on AWS

> Настройте Claude Code для использования API Claude, управляемого Anthropic, с аутентификацией AWS, контролем доступа IAM и биллингом через AWS Marketplace.

Claude Platform on AWS — это API Claude, управляемый Anthropic, с аутентификацией AWS, контролем доступа IAM и биллингом через AWS Marketplace. Запросы поступают непосредственно в API Anthropic, поэтому вы получаете те же модели и функции API, что и в [Claude API](https://platform.claude.com/docs) по тому же графику выпусков. Вы проходите аутентификацию с помощью учётных данных AWS или API-ключа рабочего пространства и оплачиваете использование через AWS Marketplace.

Используйте это руководство, чтобы направить Claude Code на рабочее пространство, которое вы уже подготовили через Claude Platform on AWS. Для подписки AWS и настройки рабочего пространства, которые предшествуют этому, см. [документацию Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws).

> [!NOTE]
>
> Подписка через AWS Marketplace подготавливает новую организацию Anthropic, привязанную к вашей учётной записи AWS. Эта организация отделена от любой организации, которая у вас уже есть в Anthropic, и учётные данные не передаются между ними. Используйте идентификатор рабочего пространства и API-ключи из организации, связанной с AWS, а не из ранее существующей учётной записи Claude Console.

Некоторые функции Claude Code недоступны или работают иначе на Claude Platform on AWS. См. [матрицу доступности функций](https://code.claude.com/docs/ru/feature-availability.md#summary-by-provider) и [функции, которым требуется получение флагов функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching).

## Предварительные требования

Перед настройкой Claude Code вам потребуется:

* Активная подписка Claude Platform on AWS через AWS Marketplace
* Рабочая область в вашей организации Anthropic, связанной с AWS, с ее идентификатором рабочей области
* Субъект IAM с разрешением на вызов сервиса Anthropic или ключ API, ограниченный рабочей областью
* Учетные данные AWS в вашей среде, в `~/.aws/credentials` или от присоединенной роли IAM, если вы хотите аутентификацию SigV4. AWS CLI требуется только для потока входа SSO.

## Настройка

### Настройте учетные данные AWS

Claude Code поддерживает два метода аутентификации для Claude Platform on AWS. Выберите метод, который соответствует тому, как ваша команда управляет доступом:

* [Учётные данные AWS с SigV4](#use-aws-credentials-with-sigv4): аутентификация в качестве субъекта IAM с учётными данными из стандартной цепочки учётных данных AWS
* [API-ключ рабочего пространства](#use-a-workspace-api-key): аутентификация с помощью долгоживущего ключа, который вы создаёте в консоли AWS

#### Использование учётных данных AWS с SigV4

Claude Code подписывает запросы с помощью SigV4, используя стандартную цепочку учетных данных AWS: переменные окружения, общие учетные данные в `~/.aws/credentials`, роли IAM, сеансы AWS SSO и любые другие источники, которые поддерживает AWS SDK.

Для локального использования войдите с помощью AWS CLI перед запуском Claude Code. Пример ниже использует профиль SSO, но любой метод, который создает учетные данные в стандартных местоположениях, работает.

```bash theme={null}
aws sso login --profile my-profile
export AWS_PROFILE=my-profile
```

Для CI и автоматизации дайте средству выполнения роль IAM с разрешением на вызов сервиса Anthropic и установите `AWS_REGION`. Цепочка учетных данных автоматически подхватывает роль.

Если ваши учётные данные SSO истекают во время сессии, настройте [`awsAuthRefresh`](https://code.claude.com/docs/ru/amazon-bedrock#advanced-credential-configuration), чтобы Claude Code повторно запустил вашу команду входа и повторил попытку вместо сбоя. Добавьте команду в ваш [файл настроек](https://code.claude.com/docs/ru/settings.md), например `~/.claude/settings.json`:

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile my-profile"
}
```

Claude Code также запускает эту команду при запуске, когда не может проверить ваши существующие учётные данные AWS, и показывает вывод команды на панели `Authentication` до завершения входа.

С настроенным `awsAuthRefresh` запустите `/login`, выберите **3rd-party platform**, затем выберите **Claude Platform on AWS · refresh credentials** в разделе **Using 3rd-party platforms**. Claude Code запускает настроенную команду и повторно читает ваши учетные данные AWS без перезагрузки.

#### Использование API-ключа рабочего пространства

Ключ API рабочей области — это долгоживущий секрет, полезный, когда вы не хотите управлять федеративными учетными данными AWS. Создайте его в консоли AWS в разделе **Claude Platform on AWS → API keys** и установите его как `ANTHROPIC_AWS_API_KEY`:

```bash theme={null}
export ANTHROPIC_AWS_API_KEY=sk-ant-xxxxx
```

Ключ отправляется как `x-api-key` и имеет приоритет над SigV4, поэтому любые учетные данные AWS в вашей среде игнорируются. Ключи API из отдельной организации Claude Console здесь не будут работать.

Обращайтесь с ключами API рабочей области как с любыми другими производственными учетными данными. [Файл пользовательских настроек](https://code.claude.com/docs/ru/settings.md) блок `env` — это удобный способ ограничить ключ вашей машиной без глобального экспорта.

> [!NOTE]
>
> Команды `/login` и `/logout` не подписывают вас на подписку Claude.ai для Claude Platform on AWS. Аутентификация выполняется через ваши учетные данные AWS или ключ API рабочей области.

### Настройте Claude Code

Установите переменные окружения, которые направляют Claude Code через Claude Platform on AWS вместо API Anthropic по умолчанию.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export AWS_REGION=us-east-1
```

`ANTHROPIC_AWS_WORKSPACE_ID` является обязательным. Claude Code отправляет его при каждом запросе как заголовок `anthropic-workspace-id`. Замените пример значения `wrkspc_01ABCDEFGHIJKLMN` на ваш собственный идентификатор рабочей области из вашей настройки Claude Platform on AWS.

Claude Code вычисляет базовый URL как `https://aws-external-anthropic.{region}.api.aws` из региона AWS, который он разрешает с [той же приоритетностью, что и Amazon Bedrock](https://code.claude.com/docs/ru/amazon-bedrock.md#3-configure-claude-code). Чтобы переопределить URL напрямую, установите `ANTHROPIC_AWS_BASE_URL`.

Claude Platform on AWS является добровольным, даже если учетные данные AWS присутствуют в вашей среде. Amazon Bedrock и Microsoft Foundry имеют приоритет в маршрутизации поставщиков, поэтому отмените установку `CLAUDE_CODE_USE_BEDROCK` и `CLAUDE_CODE_USE_FOUNDRY`, если они установлены.

### Закрепите версии моделей

Claude Platform on AWS использует те же идентификаторы моделей, что и прямой API Claude.

Псевдонимы по умолчанию `fable`, `opus`, `sonnet` и `haiku` разрешаются во встроенные значения по умолчанию Claude Code для Claude Platform on AWS, которые могут отставать от последнего выпуска. Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` разрешается в Opus 5.5. До версии v2.1.280 он разрешался в Opus 5 с версии v2.1.219.

Если вы развертываете Claude Code для команды, явно закрепите идентификаторы моделей, чтобы новый выпуск не переместил всех сразу:

```bash theme={null}
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5
```

Полный список идентификаторов моделей и псевдонимов см. в разделе [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Для других переменных, связанных с моделями, см. [Конфигурация модели](https://code.claude.com/docs/ru/model-config.md).

[Prompt caching](https://code.claude.com/docs/ru/prompt-caching.md) включен автоматически. Чтобы запросить TTL кэша на 1 час вместо стандартного 5 минут, установите `ENABLE_PROMPT_CACHING_1H=1`. API выставляет счета за записи кэша на 1 час по более высокому тарифу. Ознакомьтесь с [ценами на prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) для получения информации о тарифах.

Чтобы установить разные TTL для вашего основного разговора и для запросов, которые Claude Code делает вне его, [выберите TTL самостоятельно](https://code.claude.com/docs/ru/prompt-caching.md#choose-the-ttl-yourself).

### Запустите и проверьте

Запустите Claude Code и подтвердите маршрутизацию:

```bash theme={null}
claude
```

Баннер при запуске показывает `Claude Platform on AWS`, когда поставщик активен. Запустите `/status` для проверки деталей: строка `API provider` читает `Claude Platform on AWS`, и вывод включает ваш `Workspace ID`, `AWS region` и `Claude Platform on AWS base URL`, если вы установили переопределение.

## Используйте Agent SDK

[Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) читает те же переменные окружения, что и CLI, поэтому любая программа, которая порождает подпроцесс Claude Code, может нацеливаться на Claude Platform on AWS, экспортируя `CLAUDE_CODE_USE_ANTHROPIC_AWS`, `ANTHROPIC_AWS_WORKSPACE_ID` и либо `ANTHROPIC_AWS_API_KEY`, либо учетные данные AWS перед вызовом.

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

process.env.CLAUDE_CODE_USE_ANTHROPIC_AWS = "1";
process.env.ANTHROPIC_AWS_WORKSPACE_ID = "wrkspc_01ABCDEFGHIJKLMN";
process.env.AWS_REGION = "us-east-1";

for await (const msg of query({ prompt: "What's in this repo?" })) {
  console.log(msg);
}
```

Этот пример полагается на окружающую цепочку учетных данных AWS для SigV4. Чтобы вместо этого аутентифицироваться с помощью ключа API рабочей области, установите `ANTHROPIC_AWS_API_KEY` таким же образом. Для более широкой поверхности Agent SDK см. [Обзор Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md).

## Маршрутизация через корпоративный прокси

Чтобы маршрутизировать трафик через прокси или [LLM gateway](https://code.claude.com/docs/ru/llm-gateway), установите `ANTHROPIC_AWS_BASE_URL` на адрес прокси. Claude Code отправляет запросы на этот URL с теми же заголовками рабочей области и аутентификации, поэтому любой шлюз, который пересылает их без изменений, работает.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

Если ваш шлюз подписывает запросы сам, установите `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1`, чтобы Claude Code отправлял неподписанные запросы и позволял шлюзу добавлять заголовки SigV4 перед пересылкой в AWS. Если шлюз требует свой собственный токен, установите его в `ANTHROPIC_AUTH_TOKEN`.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

## Troubleshooting

Запустите `/status`, чтобы увидеть разрешенного поставщика и любой явно настроенный идентификатор рабочей области, регион, переопределение базового URL и параметр пропуска аутентификации. Это самый быстрый способ подтвердить, что Claude Code нацелен на Claude Platform on AWS вообще.

### `403 Forbidden` или `AccessDenied` при каждом запросе

Субъект IAM, который разрешил Claude Code, вероятно, не имеет разрешения на вызов сервиса Anthropic в вашей рабочей области. Проверьте роль, присоединенную к вашему профилю AWS или средству выполнения, которое запустило Claude Code, и убедитесь, что оно имеет действия `aws-external-anthropic`, задокументированные в [справочнике действий IAM](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions).

Если вы установили `ANTHROPIC_AWS_API_KEY`, ключ имеет приоритет над SigV4, и устаревший ключ создает ту же ошибку. Создайте ключ заново в консоли AWS в разделе **Claude Platform on AWS → API keys** или отмените установку переменной, чтобы вернуться к вашим учетным данным AWS.

### Запросы не выполняются с ошибкой отсутствующей рабочей области

`ANTHROPIC_AWS_WORKSPACE_ID` вероятно не установлен или пуст. Каждый запрос Claude Platform on AWS должен включать идентификатор рабочей области. Он не подразумевается вашими учетными данными AWS. Найдите идентификатор в разделе **Workspaces** на странице сервиса консоли AWS и экспортируйте его перед запуском Claude Code.

### Запросы по-прежнему идут на `api.anthropic.com`

`CLAUDE_CODE_USE_ANTHROPIC_AWS` вероятно не установлен или установлен на значение, которое не анализируется как истинное. Установите его на `1` и запустите `/status`, чтобы подтвердить разрешенного поставщика. Если также установлены `CLAUDE_CODE_USE_BEDROCK` или `CLAUDE_CODE_USE_FOUNDRY`, они имеют приоритет над Claude Platform on AWS.

## Дополнительные ресурсы

Подписка Claude Platform on AWS, настройка рабочей области и IAM, которые предшествуют настройке Claude Code, рассматриваются в документации платформы:

* [Обзор Claude Platform on AWS](https://platform.claude.com/docs/ru/build-with-claude/claude-platform-on-aws): подписка, настройка рабочей области и справочник продукта
* [Справочник действий IAM](https://platform.claude.com/docs/ru/api/claude-platform-on-aws-iam-actions): разрешения и управляемые политики
