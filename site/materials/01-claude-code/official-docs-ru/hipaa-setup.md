> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка Claude Code (local mode) для организации с HIPAA-конфигурацией

> Подготовьте компьютеры разработчиков к работе Claude Code (local mode) с HIPAA-конфигурацией. Рассматриваются версии, сетевой доступ, управляемые настройки и локальные данные.

HIPAA-конфигурация — это настройка организации в планах Claude Enterprise для организаций, которые работают с защищённой медицинской информацией (PHI) и заключили с Anthropic [Business Associate Agreement (BAA)](https://support.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers). Она применяется к Claude Code (local mode) и Cowork (local mode) и ограничивает функции в обоих продуктах.

> [!NOTE]
>
> «(local mode)» означает локальную сессию, а не [облачную сессию](https://code.claude.com/docs/ru/claude-code-on-the-web.md). Локальные сессии выполняются в одном из следующих мест:
>
> * Claude Code в терминале
> * Claude Code на вкладке Code в Claude Desktop
> * Cowork в Claude Desktop
>
> Расширения Claude Code для VS Code и JetBrains не входят в (local mode). Они продолжают работать с применённой HIPAA-конфигурацией, но ваше BAA на них не распространяется. Полный список Eligible Services см. в [Implementation Guide](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide).

Эта страница предназначена для IT-администратора или администратора безопасности, который подготавливает компьютеры разработчиков. Саму конфигурацию применяет Primary Owner вашей организации Claude. В статье [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731) объясняется, что включает ваше BAA, как применяется конфигурация и как запланировать дату её применения.

Если участники вашей организации также используют Cowork, выполните также инструкции из раздела [Настройка Cowork (local mode) для организации с HIPAA-конфигурацией](https://claude.com/docs/cowork/hipaa-setup). В нём описаны политика Claude Desktop и локальные данные Cowork.

В таблице показано, когда выполнять каждую часть настройки:

| Когда | Что делать |
| :- | :- |
| До применения конфигурации | [Подготовьте компьютеры](#prepare-computers-before-the-hipaa-configuration-is-applied): проверьте, как подключаются разработчики, обновите приложения, разрешите сетевой доступ, разверните управляемые настройки и ограничьте вход в Claude Desktop |
| После применения | Вкладка Code отключена, пока Owner не включит её снова. [Проверьте конфигурацию на компьютере](#confirm-the-configuration-on-a-computer) |
| Постоянно | [Управляйте данными локальных сессий](#manage-local-session-data) |

## Подготовка компьютеров до применения HIPAA-конфигурации

Рекомендуем начать с задач из этого раздела и завершить их до применения конфигурации.

### Проверьте, как разработчики входят в систему и подключаются

HIPAA-конфигурация действует только в сессиях, где разработчик входит с учётной записью Claude Enterprise, а Claude Code подключается напрямую к Claude API. При любом другом подключении разработчики могут продолжать использовать Claude Code, но [HIPAA-конфигурация](#what-developers-see-in-claude-code) к нему не применяется.

В таблице показано, какие подключения подходят. Чтобы узнать, распространяется ли ваше BAA на сессию из строки «Нет», см. [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731).

| Как подключается Claude Code | Подходит для HIPAA-конфигурации |
| :- | :- |
| Учётная запись Claude Enterprise с прямым подключением к Claude API | Да |
| Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, Claude Platform on AWS или [Claude apps gateway](https://code.claude.com/docs/ru/claude-apps-gateway) | Нет |
| [LLM-шлюз](https://code.claude.com/docs/ru/llm-gateway) или любой другой пользовательский `ANTHROPIC_BASE_URL` | Нет |
| `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper` на компьютере без входа в Claude Enterprise | Нет |
| API-ключ Claude Console или [федеративные учётные данные](https://code.claude.com/docs/ru/authentication.md#anthropic-profiles-and-federation-credentials) | Нет. Эти сессии принадлежат организации Claude Console, у которой собственное соглашение и собственные настройки |

#### Проверьте, как подключается компьютер

Откройте терминал на компьютере, выполните `claude` и введите `/status` в промпте. На вкладке **Status** отображаются следующие строки:

| Строка | Когда появляется |
| :- | :- |
| `Login method` и `Organization` | Сессия выполнена со входом в учётную запись claude.ai. Для учётной записи Claude Enterprise в `Login method` указано `Claude Enterprise account`, а в `Organization` — ваша организация |
| `API provider` | Только когда сессия использует облачного провайдера или Claude apps gateway |
| `Anthropic base URL` | Только когда задан `ANTHROPIC_BASE_URL` |

Если компьютер использует подключение, не подходящее для HIPAA-конфигурации, вы можете с помощью [управляемых настроек](#deploy-managed-settings) заблокировать облачных провайдеров, шлюзы и учётные данные, заданные через `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper`.

### Обновите Claude Code и Claude Desktop

HIPAA-конфигурация требует Claude Code v2.1.285 или новее и Claude Desktop v2.19675.0 или новее. Если ваша организация использует и терминал, и [приложение Claude Desktop](https://code.claude.com/docs/ru/desktop.md), обновите оба.

Чтобы узнать установленную версию Claude Code, выполните эту команду в терминале. Она одинакова в Bash, Zsh и PowerShell:

```bash theme={null}
claude --version
```

Поддерживаемая установка выводит `2.1.285 (Claude Code)` или большее число.

Чтобы узнать установленную версию Claude Desktop, см. [Проверка версии](https://code.claude.com/docs/ru/desktop.md#check-your-version).

#### Что видят разработчики на более старой версии

Для организаций с HIPAA-конфигурацией серверы Anthropic отклоняют запросы от версий старше минимальной. Anthropic со временем повышает минимальную версию, и вам ничего не нужно настраивать.

| Приложение | Что видит разработчик на более старой версии |
| :- | :- |
| Claude Code | Каждый запрос завершается с [`API Error`](https://code.claude.com/docs/ru/errors#claude-code-does-not-support-this-model), в которой сказано, что версия старше минимальной, требуемой политикой вашей организации |
| Claude Desktop | Диалоговое окно **Update required**, которое сообщает разработчику, что нужно обновить Claude Desktop, чтобы продолжить пользоваться вкладкой **Code** |

Чтобы разработчики оставались на поддерживаемой версии, [поддерживайте Claude Code в актуальном состоянии](https://code.claude.com/docs/ru/setup.md#update-claude-code). Для Claude Desktop см. [Обновление Claude Desktop](https://claude.com/docs/cowork/hipaa-setup#update-claude-desktop).

### Разрешите сетевой доступ

Разрешите хосты из этой таблицы в вашем прокси и брандмауэре по HTTPS на порту 443. Разрешайте каждый хост целиком, а не отдельные пути.

| Хост | Требуется для |
| :- | :- |
| `api.anthropic.com` | Запросов к Claude API, телеметрии и политики организации, которая сообщает Claude Code, что HIPAA-конфигурация включена |
| `claude.ai`, `claude.com`, `platform.claude.com` | Входа в систему и обновления токенов |
| `sso.claude.com` | Входа в систему, если ваша организация использует единый вход |
| `downloads.claude.ai` | Нативного установщика и его обновлений |
| `mcp-proxy.anthropic.com` | [Коннекторов из claude.ai](https://code.claude.com/docs/ru/mcp.md#use-mcp-servers-from-claude-ai) |

В этой таблице перечислены хосты, которые нужны нативной установке Claude Code в терминале для входа, работы и обновления. Остальные перечислены на следующих страницах:

* **Другие способы установки и дополнительные функции**: в разделе [Требования к сетевому доступу](https://code.claude.com/docs/ru/network-config.md#network-access-requirements) перечислены хосты, на которых установки через npm и Homebrew проверяют обновления, а также хосты для таких функций, как установка плагинов
* **Вкладка Code и Cowork**: в разделе [Требования к сетевому доступу Desktop](https://code.claude.com/docs/ru/desktop.md#network-access-requirements) перечислены дополнительные хосты, необходимые Claude Desktop
* **Прокси, которые инспектируют TLS**: в разделе [Пользовательские сертификаты CA](https://code.claude.com/docs/ru/network-config.md#custom-ca-certificates) показано, как настроить доверие к сертификату вашего прокси

Сессии, проходящие через корпоративный HTTPS-прокси, по-прежнему подходят для HIPAA-конфигурации, если прокси может обращаться к хостам из таблицы.

Claude Code узнаёт, что у вашей организации есть HIPAA-конфигурация, получая политику организации с `api.anthropic.com` при запуске и затем примерно каждый час, пока сессия используется. Политика — это запись о статусе HIPAA вашей организации и вытекающих из него ограничениях функций.

Чтобы проверить, получил ли конкретный компьютер политику, см. [Проверка конфигурации на компьютере](#confirm-the-configuration-on-a-computer).

### Разверните управляемые настройки

С помощью [управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md) вы можете направлять разработчиков на вход с учётной записью Claude Enterprise, блокировать облачных провайдеров и шлюзы, а также задавать, сколько дней каждый компьютер хранит данные локальных сессий. Настройки применяются независимо от того, действует ли HIPAA-конфигурация.

Настройки в этом разделе — это пример, который мы рекомендуем в качестве отправной точки. Ваша организация несёт ответственность за определение потребностей собственной среды и за подтверждение того, что её конфигурация им соответствует.

В следующем примере задаются четыре ключа, которые можно добавить в [управляемые настройки](https://code.claude.com/docs/ru/managed-settings.md#choose-a-delivery-mechanism), развёртываемые вашей организацией:

```json theme={null}
{
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "allowedProviders": ["anthropic"],
  "cleanupPeriodDays": 30
}
```

Более полный `managed-settings.json` с изоляцией в песочнице, списком разрешённых сетевых адресов, защитой учётных данных и хранением локальных данных см. в файлах `settings-hipaa.json` и `README-hipaa.md` в [репозитории примеров настроек](https://github.com/anthropics/claude-code/tree/main/examples/settings).

#### Что делает каждый ключ

В таблице показано, какое значение задать для каждого ключа и что Claude Code для него обеспечивает.

| Ключ | Задайте значение | Что обеспечивает Claude Code |
| :- | :- | :- |
| [`forceLoginMethod`](https://code.claude.com/docs/ru/settings-reference#forceloginmethod) | `"claudeai"` | Claude Code направляет разработчиков на вход через claude.ai вместо Claude Console |
| [`forceLoginOrgUUID`](https://code.claude.com/docs/ru/settings-reference#forceloginorguuid) | ID вашей организации, который [Owner](https://code.claude.com/docs/ru/server-managed-settings.md#access-control) может скопировать в [настройках администратора claude.ai](https://claude.ai/admin-settings/organization) | Claude Code завершает работу при запуске, если вход в claude.ai принадлежит другой организации |
| [`allowedProviders`](https://code.claude.com/docs/ru/settings-reference#allowedproviders) | `["anthropic"]` | Claude Code отказывается запускаться с облачным провайдером или шлюзом |
| [`cleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#cleanupperioddays) | Количество дней, в течение которых ваша политика хранения записей позволяет компьютеру хранить данные сессий | Каждый компьютер удаляет старые данные сессий по истечении одинакового количества дней |

> [!WARNING]
>
> Проверьте значение `forceLoginOrgUUID` перед развёртыванием. Если оно не совпадает с ID вашей организации, Claude Code будет завершать работу при запуске у каждого разработчика, входящего с учётной записью claude.ai.

HIPAA-конфигурация не ограничивает `cleanupPeriodDays`, поэтому разработчик может увеличить это значение в своих настройках. Если вы задаёте его в управляемых настройках, Claude Code игнорирует значение разработчика.

Если задан `forceLoginMethod` или `forceLoginOrgUUID`, Claude Code также отклоняет сессии, которые проходят аутентификацию с помощью `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` или `apiKeyHelper`.

#### Убедитесь, что настройки загружены

На компьютере с настройками выполните `claude`, войдите с учётной записью Claude Enterprise и введите `/status`. В строке `Setting sources` указано `Enterprise managed settings`, а за ним в скобках источник, например `(file)`, а в строке `Allowed providers` — `Anthropic API (managed allowedProviders)`. Если в `Setting sources` этого нет или строка `Allowed providers` отсутствует, см. [Проверка действия политики](https://code.claude.com/docs/ru/managed-settings.md#check-that-a-policy-is-in-force).

#### Сессии, которые ключи управляемых настроек не блокируют

Даже после развёртывания этих ключей некоторые сессии всё равно могут выполняться без HIPAA-конфигурации:

* **Вход через Claude Console и федеративные учётные данные**: `forceLoginOrgUUID` проверяет только вход через claude.ai. В разделе [Ограничение входа вашей организацией](https://code.claude.com/docs/ru/authentication.md#restrict-login-to-your-organization) перечислено, что Claude Code проверяет для каждого способа входа и типа учётных данных.
* **Серверные управляемые настройки**: если ваша организация также использует [серверные управляемые настройки](https://code.claude.com/docs/ru/server-managed-settings.md), попросите Owner добавить туда те же ключи. В разделе [Как Claude Code объединяет управляемые источники](https://code.claude.com/docs/ru/managed-settings.md#how-claude-code-combines-managed-sources) объясняется, какой источник применяется.
* **Версии старше v2.1.285**: эти версии игнорируют `allowedProviders`, поэтому они по-прежнему могут запускаться с облачным провайдером или шлюзом. Чтобы версии с v2.1.163 по v2.1.284 отказывались запускаться, вы можете добавить [`requiredMinimumVersion`](https://code.claude.com/docs/ru/settings-reference#requiredminimumversion) со значением `"2.1.285"` в те же управляемые настройки, что и [ключи из примера](#deploy-managed-settings). Версии до v2.1.163 игнорируют как `requiredMinimumVersion`, так и `allowedProviders`, поэтому [обновите эти компьютеры](#update-claude-code-and-claude-desktop).

Чтобы узнать, распространяется ли ваше BAA на сессию, выполняемую без HIPAA-конфигурации, см. [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731).

### Ограничьте вход в Claude Desktop

Если разработчики используют вкладку Code в Claude Desktop, также задайте `forceLoginOrgUUID` в политике Claude Desktop, как описано в разделе [Ограничение входа вашей организацией](https://code.claude.com/docs/ru/desktop.md#restrict-sign-in-to-your-organization). Развёртывание `forceLoginMethod` и `forceLoginOrgUUID` в управляемых настройках не меняет экран входа Claude Desktop.

## Проверка конфигурации на компьютере

Выполните эту проверку на одном управляемом компьютере после применения конфигурации к вашей организации.

**1. Перезапустите Claude Code**

Завершите все запущенные сессии, откройте терминал и выполните `claude`. Запущенная используемая сессия получает конфигурацию примерно в течение часа без перезапуска. При перезапуске Claude Code получает её сразу.

**2. Проверьте уведомление при запуске**

Убедитесь, что при запуске Claude Code выводит `Per your organization's policy, some features are limited · /status for details`.

**3. Проверьте нижнюю панель**

Убедитесь, что тег `HIPAA configured` отображается справа на нижней панели, под промптом. До v2.1.286 тег выглядел как `HIPAA`.

**4. Выполните /status**

Введите `/status` в промпте. Убедитесь, что на вкладке **Status** в строке `Organization configuration` указано `HIPAA`.

**5. Проверьте Claude Desktop**

Применение HIPAA-конфигурации отключает вкладку Code для вашей организации. Если ваша организация её использует, попросите Owner перейти в [**Organization settings > Claude Code**](https://claude.ai/admin-settings/claude-code) и включить переключатель **Desktop**. Для Cowork см. [Проверка HIPAA-конфигурации в Claude Desktop](https://claude.com/docs/cowork/hipaa-setup#confirm-the-hipaa-configuration-in-claude-desktop).

Перезагрузите Claude Desktop или войдите снова. Убедитесь, что в строке заголовка отображается метка **HIPAA configured**. На Mac откройте боковую панель, чтобы её увидеть.

Если `HIPAA` отсутствует в `/status`, проверьте следующие причины по порядку:

1. **Неверная учётная запись или подключение**: убедитесь, что `/status` показывает вашу организацию в строке `Organization` и не показывает строк `API provider` или `Anthropic base URL`. В разделе [Проверьте, как разработчики входят в систему и подключаются](#check-how-developers-sign-in-and-connect) перечислены способы входа и подключения, не подходящие для конфигурации.
2. **Заблокировано получение политики**: найдите в `/status` строку `Organization policy`, в которой указана причина. Вне сессии выполните `claude doctor` и прочитайте ту же строку: в ней сказано, откуда Claude Code загрузил политику или почему политика не загрузилась. Разрешите `api.anthropic.com` в вашем прокси, затем перезапустите Claude Code.
3. **Конфигурация ещё не применена**: спросите у Primary Owner, применил ли он конфигурацию.

## Что видят разработчики в Claude Code

При применённой конфигурации HIPAA некоторые функции Claude Code отключены или работают в терминале иначе. В таблице перечислены изменения, о которых разработчики, скорее всего, спросят вас. В [таблице доступности функций HIPAA](https://support.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers) перечислены все функции Claude Code и Cowork, включая те, которые Owner может снова включить.

| Что замечает разработчик | Почему |
| :- | :- |
| Инструмент WebFetch недоступен | WebFetch отключён. Веб-поиск по-прежнему работает |
| `--cloud`, `/teleport` и [Remote Control](https://code.claude.com/docs/ru/remote-control.md) отклоняются | [Облачные сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) и Remote Control отключены |
| `/feedback` и `/bug` недоступны | Отправка отзывов отключена |
| Claude не может опубликовать [артефакт](https://code.claude.com/docs/ru/artifacts.md) | Публикация артефактов отключена |
| Инструменты MCP загружаются в контекст заранее | [MCP Tool Search](https://code.claude.com/docs/ru/mcp.md#configure-tool-search) отключён. Ни `ENABLE_TOOL_SEARCH`, ни управляемые настройки не включают его снова |
| MCP-сервер или хук, который читает `ANTHROPIC_API_KEY`, перестаёт проходить аутентификацию | Claude Code [удаляет учётные данные Anthropic](#anthropic-credentials-in-commands-hooks-and-mcp-servers) из запускаемых им процессов |
| Ограничения сохраняются после `/login` в другую организацию | Статус HIPAA действует до перезапуска Claude Code |

### Учётные данные Anthropic в командах, хуках и MCP-серверах

При применённой конфигурации HIPAA Claude Code удаляет учётные данные, которые он использует для обращения к Anthropic, такие как `ANTHROPIC_API_KEY` и `ANTHROPIC_AUTH_TOKEN`, из окружения запускаемых им shell-команд, хуков и MCP-серверов.

Конфигурация HIPAA не удаляет учётные данные облачных провайдеров или GitHub, поэтому команда, которая выполняет push в GitHub или обращается к другому сервису, по-прежнему работает с доступом этого разработчика. Ваше соглашение BAA с Anthropic не распространяется на данные, которые такая команда туда отправляет. Полный список Eligible Services см. в [Implementation Guide](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide).

Чтобы ограничить, какие команды и хосты может использовать Claude, см. [правила разрешений](https://code.claude.com/docs/ru/permissions.md) и [песочницу](https://code.claude.com/docs/ru/sandboxing.md).

## Управление данными локальных сессий

Claude Code (local mode) и Cowork (local mode) хранят данные сессий на компьютере каждого разработчика. Защита и удаление этих данных — ответственность вашей организации.

### Данные Claude Code

В разделе [Данные приложения](https://code.claude.com/docs/ru/claude-directory.md#application-data) перечислено, что Claude Code (local mode) хранит на компьютере, что его процедура очистки удаляет по истечении `cleanupPeriodDays` и что остаётся, пока кто-то это не удалит. На той же странице указано, что отличается в организации с применённой HIPAA-конфигурацией.

Процедура очистки выполняется только тогда, когда кто-то запускает Claude Code, поэтому компьютер, на котором его никто не запускает, сохраняет свои данные.

### Данные вкладки Code

Вкладка Code хранит данные в следующих местах:

* **Транскрипты**: в `~/.claude/projects/`, вместе с транскриптами терминала. В разделе [Автоматическая очистка](https://code.claude.com/docs/ru/claude-directory.md#cleaned-up-automatically) указано, когда процедура очистки их удаляет.
* **Папка данных Claude Desktop**: `~/Library/Application Support/Claude` в macOS. В Windows — `%APPDATA%\Claude` или `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude` для установщика, загруженного с сайта Anthropic, поэтому проверьте оба пути. При применённой HIPAA-конфигурации Claude Desktop удаляет локальные сессии вкладки Code, неактивные дольше `cleanupPeriodDays`, включая помеченные звёздочкой. Он удаляет их только во время своей работы. Claude Desktop обрабатывает worktree удалённой сессии одним из следующих способов:
  * **Нет незафиксированных изменений, сессия не помечена звёздочкой и не закреплена, и никакая другая сессия не использует этот worktree**: Claude Desktop удаляет worktree
  * **Любой другой случай**: worktree остаётся на компьютере

В Windows `~` означает `%USERPROFILE%`.

### Данные Cowork

В разделе [Управление данными Cowork на каждом компьютере](https://claude.com/docs/cowork/hipaa-setup#manage-cowork-data-on-each-computer) перечислено, где Cowork (local mode) хранит данные и что удаляет Claude Desktop.

### Немедленное удаление данных сессий

Если вашей организации нужно удалить данные сессий разработчика до того, как их удалит процедура очистки, большую их часть можно удалить одной командой. Войдите на компьютер как этот разработчик, откройте любую оболочку и выполните команду для установленной версии Claude Code.

В Claude Code v2.1.288 или более поздней версии выполните `claude purge`:

```bash theme={null}
claude purge --all --yes
```

В версиях с v2.1.126 по v2.1.287 выполните `claude project purge`, которая принимает те же флаги:

```bash theme={null}
claude project purge --all --yes
```

Любая из этих команд удаляет транскрипты и автоматическую память всех проектов, записи в `tasks/`, `debug/` и `file-history/`, `history.jsonl`, а также записи проектов в `~/.claude.json`. Без `--yes` она выводит план и сначала запрашивает подтверждение.

После очистки остаются другие пути, которые могут содержать содержимое сессий, например вставленный текст в `paste-cache/`. В разделе [Очистка локальных данных](https://code.claude.com/docs/ru/claude-directory.md#clear-local-data) перечислены пути, которые можно удалить вручную. Чтобы полностью очистить компьютер, например перед передачей другому сотруднику, [сотрите с него данные](#offboard-a-developer).

### Отключение разработчика

Удаление места или учётной записи разработчика ничего не удаляет на его компьютере, и `/logout` также не удаляет данные сессий. Чтобы удалить их все, вы можете стереть данные с компьютера с помощью вашего инструмента управления устройствами.

## Связанные ресурсы

* [Настройка Cowork (local mode) для организации с HIPAA-конфигурацией](https://claude.com/docs/cowork/hipaa-setup)
* [Развёртывание управляемых настроек](https://code.claude.com/docs/ru/managed-settings.md)
* [Пример настроек для HIPAA](https://github.com/anthropics/claude-code/tree/main/examples/settings)
* [Корпоративная сетевая конфигурация](https://code.claude.com/docs/ru/network-config.md)
* [Нулевое хранение данных](https://code.claude.com/docs/ru/zero-data-retention.md)
* [Юридические вопросы и соответствие требованиям](https://code.claude.com/docs/ru/legal-and-compliance.md)
* [Использование данных](https://code.claude.com/docs/ru/data-usage.md)
