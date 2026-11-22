> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник самостоятельно размещаемых окружений

> Полный справочник по самостоятельно размещаемому runner и orchestrator: флаги CLI, переменные окружения и метрики Prometheus.

> [!NOTE]
>
> Самостоятельно размещаемые окружения находятся в публичной бета-версии на планах Team и Enterprise; [Owner](https://code.claude.com/docs/ru/cloud-environments.md#organization-shared-environments) включает их, активируя **Allow self-hosted environments** на [странице администратора **Cloud environments**](https://claude.ai/admin-settings/cloud-environments). Эта страница является справочником по флагам и метрикам; см. [quickstart](https://code.claude.com/docs/ru/self-hosted-environments-quickstart.md) для настройки и [Deploy to production](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md) для рецептов флота.

Эта страница является справочником для двух процессов, которые вы запускаете в [самостоятельно размещаемом окружении](https://code.claude.com/docs/ru/self-hosted-environments): runner, который выполняет Claude Code [cloud sessions](https://code.claude.com/docs/ru/claude-code-on-the-web.md) на ваших хостах, и опциональный orchestrator автомасштабирования, который запускает runners по мере поступления sessions в очередь. Каждый имеет свою таблицу флагов. Оба работают на хостах Linux или macOS, для которых значения по умолчанию, такие как `/workspace` и `~/.claude`, предполагаются. Запустите `claude self-hosted-runner --help` для авторитетного списка на вашей установленной версии.

Серии метрик и несколько полей API по-прежнему используют `pool` для того, что эти страницы называют окружением; оба термина обозначают одно и то же. ID окружения — это поле `pool_id` с формой `ccpool_...`: везде, где эти страницы показывают идентификатор `pool`, он обозначает окружение. Флаги CLI и переменные окружения пишут его как `environment`, например `--environment-secret-file`; устаревшие написания `pool` по-прежнему работают, как описывает строка [`--environment-secret-file`](#runner-cli-flags).

## Флаги CLI Runner

Большинство флагов имеют соответствующую переменную окружения. Когда установлены оба, флаг имеет приоритет. Флаги длительности принимают минуты или секунды в CLI, но связанная переменная окружения всегда в миллисекундах, обозначаемая суффиксом `_MS`, и столбец Default показывает единицу флага: `--exit-if-unused-min 10` эквивалентно `SELF_HOSTED_RUNNER_IDLE_SHUTDOWN_MS=600000`, а значение Helm вроде `SELF_HOSTED_RUNNER_STARTUP_TIMEOUT_MS: "15"` означает 15 миллисекунд, а не 15-минутное значение по умолчанию.

| Флаг | Переменная окружения | По умолчанию | Описание |
| :- | :- | :- | :- |
| `--api-url <url>` | none | `https://api.anthropic.com` | URL базы API. Переопределяйте только для тестирования. |
| `--base-dir <path>` | `SELF_HOSTED_RUNNER_BASE_DIR` | `/workspace`; на Windows отсутствует | Каталог для извлечённых репозиториев и рабочих каталогов для каждого сеанса. Runner должен иметь доступ на запись к этому пути или его родительскому каталогу. Runner создает каталог при запуске и выходит с `cannot create or write to base directory`, когда не может создать или записать в него. До v2.1.225 runner создавал каталог при запуске первого сеанса, поэтому непригодный путь приводил к сбою сеансов, а не запуска. На Windows, который не является поддерживаемым хостом runner, нет значения по умолчанию: runner выходит при запуске, если вы не передадите флаг и не установите переменную. Используйте одно и то же значение на каждом runner в среде. См. [Держите базовый каталог и емкость идентичными на всех runners](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#keep-the-base-directory-and-capacity-identical-across-runners). |
| `--capacity <n>` | none | `1` | Максимальное количество одновременных сеансов, которые обрабатывает этот runner. Все сеансы принадлежат одному заблокированному [owner](https://code.claude.com/docs/ru/self-hosted-environments#key-concepts). Используйте одно и то же значение на каждом runner в среде; см. [Держите базовый каталог и емкость идентичными на всех runners](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#keep-the-base-directory-and-capacity-identical-across-runners). |
| `--client-label <label>` | `SELF_HOSTED_RUNNER_CLIENT_LABEL` | имя хоста хоста | Метка, которую runner отправляет при регистрации. Runner также сообщает её как метку `client_label` [`claude_code_self_hosted_runner_info`](#prometheus-metrics). Требует Claude Code v2.1.248 или позже. |
| `--configure-git` | `SELF_HOSTED_RUNNER_CONFIGURE_GIT=1` | off | При запуске запишите глобальную идентификацию git, включите подписание коммитов Anthropic, включите переговоры git push и установите hooks коммитов, которые добавляют трейлер `Co-authored-by:`. Переговоры push требуют Claude Code v2.1.257 или позже. См. [Configure git](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#configure-git). |
| `--confine-repo-settings <mode>` | `SELF_HOSTED_RUNNER_CONFINE_REPO_SETTINGS` | `warn` | Устанавливает режим защиты, которая помечает сеанс, когда параметры репозитория, зафиксированные в коммите, пытаются предоставить доступ на запись или чтение вне собственного рабочего пространства этого сеанса, установить переменные окружения или переопределить позицию sandbox или hooks оператора, например `sandbox.enabled: false` или `disableAllHooks`. По умолчанию `warn` регистрирует нарушение и все еще запускает сеанс, `enforce` отказывает в сеансе, а `off` отключает сканирование. См. [Harden your deployment](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#harden-your-deployment). |
| `--debug-token-dir <path>` | `SELF_HOSTED_RUNNER_DEBUG_TOKEN_DIR` | unset | Запишите живые токены на диск для проверки. Только для отладки; не используйте в production. |
| `--defer-shutdown-max-min <n>` | `SELF_HOSTED_RUNNER_DEFER_SHUTDOWN_MAX_MS` | `0` | При первом `SIGTERM` или `SIGINT` продолжайте обслуживать уже подключенные сеансы вместо их осушения, затем отпустите все еще подключенное через N минут и выйдите. Повысьте timeout остановки вашего хоста перед установкой этого. См. [Defer the drain past the first signal](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#defer-the-drain-past-the-first-signal). `0` отключает. Требует Claude Code v2.1.238 или позже. |
| `--drain-grace-sec <n>` | `SELF_HOSTED_RUNNER_DRAIN_GRACE_MS` | `0` | До тех пор, пока runner не получит сигнал завершения или не достигнет времени выхода на пенсию, контролирует, когда runner выходит после завершения активных сеансов: `0` выходит немедленно без опроса на дополнительные, а положительное значение держит runner живым и повторно опрашивает очередь заблокированного owner в течение этого количества секунд, за счет изоляции контейнера для каждого сеанса, описанной в [разделе hardening](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#harden-your-deployment). После первого сигнала, который вы отложили с помощью [`--defer-shutdown-max-min`](https://code.claude.com/docs/ru/self-hosted-environments-deploy#defer-the-drain-past-the-first-signal), runner выходит, как только он не содержит сеансов, независимо от того, что вы установили здесь. |
| `--drain-marker-file <path>` | `SELF_HOSTED_RUNNER_DRAIN_MARKER_FILE` | unset | Файл маркера, который ваш хост записывает для объявления корректного осушения перед отправкой `SIGTERM`. Когда файл существует в начале осушения, runner сообщает о своем выходе в Anthropic как об осушении хоста, а не как о простом сигнале завершения. Само осушение, включая удержание `--drain-wait-sec`, работает так же, как без флага. Назовите путь на локальной файловой системе, в которую сеансы не могут писать. Требует Claude Code v2.1.271 или позже. |
| `--drain-wait-sec <n>` | `SELF_HOSTED_RUNNER_DRAIN_WAIT_MS` | `0` | После начала осушения, которое происходит на `SIGTERM`, если вы не установили [`--defer-shutdown-max-min`](https://code.claude.com/docs/ru/self-hosted-environments-deploy#defer-the-drain-past-the-first-signal), ждите до N секунд для завершения текущего хода каждого сеанса и фоновых задач перед завершением дочернего процесса. Во время этого ожидания runner считает фоновую задачу, которая только что завершилась, все еще работающей до тех пор, пока не начнется следующий ход, который читает её результат, в течение максимум окна [`SELF_HOSTED_RUNNER_BG_RESULT_GRACE_MS`](#environment-variable-only-settings). [Также повысьте таймаут остановки](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#let-running-turns-finish-before-a-restart). |
| `--environment-secret-file <path>` | `SELF_HOSTED_RUNNER_ENVIRONMENT_SECRET` | required | Путь к файлу, содержащему секрет среды, или, для runner, порожденных [orchestrator](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners), одноразовый JWT работного заказа. `SELF_HOSTED_RUNNER_ENVIRONMENT_SECRET` несет значение секрета напрямую, а не путь к файлу. Старый флаг `--pool-secret-file` и переменная `SELF_HOSTED_RUNNER_POOL_SECRET` по-прежнему работают и выводят уведомление об устаревании в stderr; сборки runner программы предварительного просмотра старше 2.1.216 распознают только эти старые имена. |
| `--exec-path <path>` | `SELF_HOSTED_RUNNER_EXEC_PATH` | собственный бинарный файл | Бинарный файл или скрипт-обертка для порождения для каждого сеанса. См. [Wrapper scripts](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#wrapper-scripts). |
| `--exit-if-unused-min <n>` | `SELF_HOSTED_RUNNER_IDLE_SHUTDOWN_MS` | `0` | Выйдите после N минут опроса, если работа так ни разу и не была назначена, для уменьшения масштаба при автомасштабировании. `0` отключает. |
| `--git-host-rewrite <from>=<to>` | none | unset | Переписать URL источников `https://<from>/...` на `https://<to>/...` перед клонированием для разделенного DNS горизонта. Повторяемо; только флаг. |
| `--git-ssh-rewrite <host>` | none | unset | Переписать URL источников `https://<host>/...` на `git@<host>:...` перед клонированием для хостов git только с SSH. Повторяемо; только флаг. |
| `--health-port <port>` | `SELF_HOSTED_RUNNER_HEALTH_PORT` | `8080` | Порт для слушателя `/healthz` и `/metrics`. Установите `0` для отключения. |
| `--hold-idle-file <path>` | `SELF_HOSTED_RUNNER_HOLD_IDLE_FILE` | unset | Файл, который ваш хост постоянно изменяет, чтобы удерживать простаивающую сессию на runner. См. [Keep an idle session while its processes run](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#keep-an-idle-session-while-its-processes-run). Требует Claude Code v2.1.311 или новее. |
| `--hooks-dir <path>` | `SELF_HOSTED_RUNNER_HOOKS_DIR` | unset | Каталог скриптов hooks жизненного цикла. См. [Lifecycle hooks](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#lifecycle-hooks). |
| `--host-config-snapshot <mode>` | `SELF_HOSTED_RUNNER_HOST_CONFIG_SNAPSHOT` | `disk` | Где runner хранит снимок при запуске [каталога конфигурации хоста](#environment-variable-only-settings), который он засевает каждый сеанс. `disk` копирует снимок в каталог, принадлежащий runner, под `--base-dir` и при каждом запуске сеанса проверяет каждый файл по дайджесту в памяти. Если файл в копии был изменен, сеанс не удается и runner отказывает в сеансах, пока вы не перезагрузите его. `memory` держит весь снимок на куче, ограниченный 64 МиБ; сверх лимита сеансы запускаются без конфигурации хоста и показывают уведомление об этом. Когда runner не может записать снимок на диск, он регистрирует сбой и использует `memory` для этого запуска. Требует Claude Code v2.1.271 или позже. |
| `--kill-session-after-min <n>` | `SELF_HOSTED_RUNNER_MAX_LIFETIME_MS` | `0` | Ограничьте сеанс N минутами настенного времени как предел безопасности для зависших сеансов. На v2.1.260 или позже runner отпускает сеанс, который достигает лимита, чтобы он мог возобновиться при следующем сообщении пользователя, и завершает его только если он все еще на runner, когда окончится окно благодати [`SELF_HOSTED_RUNNER_MAX_LIFETIME_GRACE_MS`](#environment-variable-only-settings). До v2.1.260 runner завершал сеанс на лимите. См. [Some sessions don't count as idle](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#some-sessions-don%E2%80%99t-count-as-idle) для деталей и как выбрать значение. `0` отключает. |
| `--lock-to-account <id>` | `SELF_HOSTED_RUNNER_LOCK_TO_ACCOUNT` | unset | Предварительно заблокируйте runner на конкретный аккаунт при запуске вместо блокировки при первом сеансе. Принимает адрес электронной почты или ID `user_...` в организации среды. Предварительно заблокированный runner никогда не подхватывает сеансы канала Claude Tag, у которых нет аккаунта. |
| `--log-file <path>` | `SELF_HOSTED_RUNNER_LOG_FILE` | unset | Зеркалируйте логи runner в файл в дополнение к stdout и stderr, созданный с разрешениями `0600`. Требуется для `self-hosted-runner doctor` для локального отслеживания логов. |
| `--log-level <level>` | none | `info` | `info` или `debug` |
| `--max-hold-min <n>` | `SELF_HOSTED_RUNNER_MAX_HOLD_MS` | `1440` | При использовании `--hold-idle-file` всё равно отпускает удерживаемую сессию через N минут после того, как она стала простаивать. Значение, меньшее или равное `--release-idle-session-min`, ничего не удерживает. `0` отключает удержание. Требует Claude Code v2.1.311 или новее. |
| `--post-session-hook-timeout-sec <n>` | `SELF_HOSTED_RUNNER_POST_SESSION_HOOK_TIMEOUT_MS` | `60` | Бюджет для [`post-session` hook](https://code.claude.com/docs/ru/self-hosted-environments-configuration#post-session) при завершении каждого сеанса, включая завершение runner |
| `--proxy-authorization-command <command>` | `SELF_HOSTED_RUNNER_PROXY_AUTHORIZATION_COMMAND` | unset | Команда shell, которую runner запускает для каждого подключения к вашему прокси выхода, используя его обрезанный stdout как значение заголовка `Proxy-Authorization`. Требует `HTTPS_PROXY` или `HTTP_PROXY`, и не может быть объединен с `--proxy-authorization-file`. См. [Authenticate to an egress proxy](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#authenticate-to-an-egress-proxy). Требует Claude Code v2.1.238 или позже. |
| `--proxy-authorization-file <path>` | `SELF_HOSTED_RUNNER_PROXY_AUTHORIZATION_FILE` | unset | Файл, который runner читает для каждого подключения к вашему прокси выхода, используя его обрезанное содержимое как значение заголовка `Proxy-Authorization`. Используйте этот флаг для токена, который другой процесс ротирует на месте. Несет те же требования, что и `--proxy-authorization-command`, и не может быть объединен с ним. См. [Authenticate to an egress proxy](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#authenticate-to-an-egress-proxy). Требует Claude Code v2.1.238 или позже. |
| `--push-outcome-on-release` | `SELF_HOSTED_RUNNER_PUSH_OUTCOME_ON_RELEASE` | off | При завершении сессии по инициативе runner, например при осушении или отпуске при простое, runner отправляет основные ветки сессии с новыми коммитами в `origin` перед удалением рабочего пространства. Выполняется по мере возможности; добавляет 30 секунд к бюджету завершения. Для возобновления с них требуется git 2.29 или новее. Ограничьте круг тех, кто может выполнять push в refs `claude/*`; см. [Возобновлённые сессии теряют неотправленную работу](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#resumed-sessions-lose-unpushed-work). Репозитории хука `checkout` не отправляются; делайте их снимки из [хука `post-session`](https://code.claude.com/docs/ru/self-hosted-environments-configuration#post-session). |
| `--release-idle-session-min <n>` | `SELF_HOSTED_RUNNER_SESSION_IDLE_MS` | `0` | Отпускает слот сессии после N минут неактивности после завершения хода или когда сессия ожидает действия пользователя. [Некоторые сессии не считаются простаивающими](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#some-sessions-don’t-count-as-idle), поэтому используйте вместе с `--kill-session-after-min`. Завершённая фоновая задача держит сессию занятой в течение максимум окна [`SELF_HOSTED_RUNNER_BG_RESULT_GRACE_MS`](#environment-variable-only-settings). Чтобы отложить отпуск, задайте [`--hold-idle-file`](https://code.claude.com/docs/ru/self-hosted-environments-deploy#keep-an-idle-session-while-its-processes-run). `0` отключает. |
| `--remove-session-state [bool]` | `SELF_HOSTED_RUNNER_REMOVE_SESSION_STATE` | off | Удалите каталоги сеанса для каждого сеанса под `<base-dir>/_sessions/` когда сеанс заканчивается на этом runner, независимо от результата. [Reuse a pre-warmed checkout](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#reuse-a-pre-warmed-checkout) описывает, что они содержат и кто может их читать, когда они остаются. Удаление является лучшим усилием: каталоги для каждого сеанса остаются на месте, когда runner убивается или достигает крайнего срока осушения перед запуском очистки. С флагом включенным, логи отладки неудачного или прерванного сеанса не сохраняются на диск. Требует Claude Code v2.1.268 или позже. |
| `--retire-at <epoch-seconds>` | `SELF_HOSTED_RUNNER_RETIRE_AT` | unset | Выведите runner на пенсию в абсолютный временной штамп Unix в секундах для инфраструктуры, которая убивает runner в известное время; [Runner lifecycle](https://code.claude.com/docs/ru/self-hosted-environments#runner-lifecycle) описывает последовательность отпуска и как определить размер маржи. Значения до 2001 или после года 5138 отклоняются флагом и игнорируются переменной окружения. |
| `--server-auto-mode-lists <mode>` | `SELF_HOSTED_RUNNER_SERVER_AUTO_MODE_LISTS` | `no-allow` | Какие из списков правил классификатора [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), которые управляющий уровень отправляет вместе с сессией, могут применяться к этой сессии: `all`, `no-allow` или `none`. Что применяет каждое значение, см. в разделе [Списки правил авторежима](#auto-mode-rule-lists). Недопустимое значение останавливает runner при запуске. Требуется Claude Code v2.1.295 или новее. |
| `--session-stop-grace-sec <n>` | `SELF_HOSTED_RUNNER_SESSION_STOP_GRACE_MS` | `5` | Как долго ждать чистого выхода процесса Claude после завершения сеанса перед принудительным завершением. Повысьте значение, если собственные hooks `SessionEnd` дочернего процесса нуждаются в большем времени. |
| `--startup-timeout-min <n>` | `SELF_HOSTED_RUNNER_STARTUP_TIMEOUT_MS` | `15` | Сколько ждать дочерний процесс, который не инициализировался, прежде чем освободить слот сессии. С какого момента начинается отсчёт и какие сессии продолжают работать, см. в разделе [Таймаут запуска сессии](#session-startup-timeout). `0` отключает таймаут. |
| `--trust-workspace [bool]` | `SELF_HOSTED_RUNNER_TRUST_WORKSPACE` | on | Посейте сохраняемое доверие для путей репозитория каждого сеанса, чтобы зафиксированные в репо `permissions.allow` и `additionalDirectories` были соблюдены. Установите `false` для отпуска зафиксированных в репо грантов разрешений и вместо этого настройте правила разрешения в `settings.json` конфигурации хоста; параметры `sandbox.*` зафиксированные в репо все еще применяются в любом случае, поэтому [защита repo-settings](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#harden-your-deployment) сканирует их независимо от этого флага. |
| `--use-anthropic-git-proxy` | `CLAUDE_RUNNER_USE_GIT_PROXY=1` | off | Клонирует репозитории на github.com через [прокси git Anthropic](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#use-the-anthropic-git-proxy) вместо управляемой клиентом аутентификации git. Требует `--capacity 1` и git 2.32 или новее; в противном случае runner отказывается запускаться. Также требует Claude Code v2.1.267 или новее. Заменяет флаги перезаписи. |

Большинство флагов длительности имеют максимум, выбранный для сохранения каждого timeout в потолке 32-битного таймера runtime примерно 24,85 дня. Флаги `--*-min` ограничены 10080 минутами, 7 дней; `--drain-grace-sec` на 604800 секунд, также 7 дней; и `--drain-wait-sec` на 86400 секунд, 24 часа. `--session-stop-grace-sec` и `--post-session-hook-timeout-sec` не ограничены. Превышение лимита ведет себя по-разному в зависимости от поверхности:

* **Флаг**: запуск не удается с ошибкой.
* **Переменная окружения**: runner зажимает значение до потолка таймера вместо его отклонения.

### Таймаут запуска сессии

Если сессия потеряла свой слот во время хода, например `/code-review`, обновите runner и дочерний бинарный файл до v2.1.309 или новее. С v2.1.299 по v2.1.308 runner освобождал сессию, даже посреди хода, если таймаут запуска истекал без сообщения `user` или `assistant`.

С `--startup-timeout-min <n>` runner освобождает слот сессии, если её дочерний процесс не инициализировался в течение `<n>` минут после клонирования. Во время хода, начавшегося до инициализации дочернего процесса, сессия сохраняет свой слот, пока не пройдёт `<n>` минут без единой строки в [канале активности](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#keep-stdin-and-file-descriptor-3-attached) дочернего процесса. После инициализации дочернего процесса runner сбрасывает этот отсчёт, и освобождением управляет `--release-idle-session-min`. Чтобы ограничить сессию, дочерний процесс которой жив, но завис, задайте `--kill-session-after-min`.

### Списки правил авторежима

`--server-auto-mode-lists` позволяет решить, какие правила классификатора [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), поступающие извне runner, применяются к сессиям на ваших runner. Управляющий уровень Anthropic может отправлять списки правил вместе с сессией и просить runner применить их. Некоторые записи могут быть правилами, написанными администратором вашей организации. Списки называются `environment`, `soft_deny` и `allow`:

* **`environment`**: запись может заставить классификатор разрешать как больше, так и меньше.
* **`soft_deny`**: запись блокирует действие, если только пользователь явно не попросил о нём или не применяется исключение `allow`.
* **`allow`**: исключения для записей `soft_deny`.

Значение флага определяет, какие списки применяет runner:

* **`no-allow`**: значение по умолчанию. Применяет `environment` и `soft_deny` и не применяет `allow`. Запись `environment` по-прежнему может заставить классификатор разрешать больше, поэтому значение по умолчанию не исключает всех ослаблений.
* **`all`**: применяет все три списка.
* **`none`**: не применяет ни один из них. Выберите `none`, чтобы исключить любые ослабления из этих списков. При этом также отбрасываются ограничения `soft_deny`.

Никакая настройка runner не заставляет управляющий уровень просить runner применить списки. Если он не просит, сессии не получают ни одного списка, что бы вы ни установили. Чтобы узнать, что произошло, запустите runner с `--log-level debug`. Тогда для каждой сессии runner записывает в лог строку, содержащую `the server asked this runner to apply`, или строку, содержащую `the server did not ask this runner to apply the auto mode lists it sends`.

## Флаги CLI Orchestrator

Подкоманда `self-hosted-runner orchestrator`, которая порождает [on-demand runners](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners), принимает `--api-url`, `--environment-secret-file`, `--hooks-dir`, `--health-port` и `--log-level` с теми же значениями по умолчанию, что и runner и, где флаг runner имеет один, ту же переменную окружения, за исключением того, что `--hooks-dir` требуется и должен содержать hook `spawn-runner`. Он также принимает свои собственные флаги:

| Флаг | По умолчанию | Описание |
| :- | :- | :- |
| `--hook-concurrency <n>` | `4` | Максимальное число хуков `spawn-runner`, работающих параллельно. Также ограничивает количество запросов на порождение, забираемых за один опрос. Orchestrator проверяет наличие новых запросов на порождение только после завершения всех запущенных им хуков, поэтому один медленный хук задерживает следующие хуки этого orchestrator. |
| `--hook-timeout <sec>` | `60` | Завершите дерево процессов hook после этого количества секунд. Timeout плюс его 5-секундная благодать убийства должны оставаться ниже `--expected-spawn-seconds`; orchestrator обеспечивает это при запуске. |
| `--expected-spawn-seconds <sec>` | `120` | Ожидаемое время p99 с момента получения orchestrator запроса на порождение до регистрации runner, включая любое ожидание свободных ресурсов на вашей платформе. Сервер допускает диапазон от 10 до 3600. Отправляется при каждом опросе как аренда на стороне сервера: если ни один runner не зарегистрируется до её истечения, сессия предлагается повторно с новым ID заказа. Все реплики должны использовать одно и то же значение. |
| `--min-idle <n>` | `0` | Держите по крайней мере N свободных слотов сеанса в режиме ожидания, активно порождая резервные runner. `0` отключает предварительное прогревание. Объедините с `--exit-if-unused-min` runner, чтобы избыточные резервные runner восстановили себя. |
| `--shutdown-drain-sec <n>` | `0` | При получении `SIGTERM` прекратить опрос запросов на порождение и дать запущенным хукам `spawn-runner` и любому опросу, ещё не получившему ответа, до указанного числа секунд на завершение, после чего остановить всё оставшееся. При `0` остановка происходит немедленно. Максимум `3600`, что orchestrator проверяет при запуске. Чтобы выбрать значение, см. [Подбор `--shutdown-drain-sec` и таймаута остановки orchestrator](https://code.claude.com/docs/ru/self-hosted-environments-configuration#size-shutdown-drain-sec-and-the-supervisors-stop-timeout-for-the-orchestrator). Требуется Claude Code v2.1.299 или новее. |
| `--debug-dir <path>` | unset | Запишите рабочий заказ каждого запроса на порождение и stderr hook на диск. Только для отладки; никогда не устанавливайте в production. |

### Флаги SCM connector

Соединитель SCM недоступен, поэтому оставьте флаги в этом разделе неустановленными. Если вы установите `--scm-connector-host`, соединение не открывается, и orchestrator продолжает его переподключать. Runners по-прежнему запускаются по мере поступления сеансов в очередь.

Соединитель — это постоянное подключение WebSocket от orchestrator к плоскости управления Anthropic. Он разработан для того, чтобы позволить размещенным предсеансовым потокам, таким как средство выбора репозитория и средство разрешения ветви или ссылки, достичь хоста GitHub Enterprise Server, который маршрутизируется только изнутри вашей сети. См. [Network requirements](https://code.claude.com/docs/ru/github-enterprise-server.md#network-requirements) на странице GitHub Enterprise Server для получения информации о том, что требуется этим потокам.

| Флаг | По умолчанию | Описание |
| :- | :- | :- |
| `--scm-connector-host <host[:port]>` | unset | Имя хоста GitHub Enterprise Server для перенаправления запросов. Порт по умолчанию `443`. |
| `--scm-connector-id <n>` | required with `--scm-connector-host` | Числовой ID подключения GitHub Enterprise Server вашей организации. |
| `--scm-connector-provider <slug>` | `ghe` | Сегмент пути, идентифицирующий поставщика, соответствующий `^[a-z0-9-]{1,32}$`. |
| `--scm-connector-ca-file <path>` | unset | Дополнительный пакет CA в формате PEM для подключений TLS к хосту GitHub Enterprise Server. |
| `--scm-connector-host-rewrite <from>=<to_host:to_port>` | unset | Только для сквозного тестирования: перенаправляет подключение TCP, сохраняя заголовок Host и TLS SNI как `--scm-connector-host`. |

При каждой попытке подключения orchestrator отправляет свой существующий секрет окружения, и он автоматически переподключается с экспоненциальной задержкой, ограниченной 30 секундами плюс jitter.

## Параметры только для переменных окружения

Эти параметры runner читаются только из окружения и охватывают поведение, которое большинство развертываний оставляют по умолчанию:

| Переменная окружения | По умолчанию | Описание |
| :- | :- | :- |
| `SELF_HOSTED_RUNNER_BG_RESULT_GRACE_MS` | `30000` | Как долго runner считает сеанс занятым после завершения фоновой задачи, пока не начнется следующий ход, который читает результат. Строки [`--drain-wait-sec` и `--release-idle-session-min`](#runner-cli-flags) описывают, где применяется удержание при осушении и отпуске при простое, и [Runner lifecycle](https://code.claude.com/docs/ru/self-hosted-environments#runner-lifecycle) описывает, где оно применяется при выходе на пенсию `--retire-at`. `0` или непригодное значение возвращается к значению по умолчанию, поэтому удержание не может быть отключено. Требует Claude Code v2.1.228 или позже. |
| `SELF_HOSTED_RUNNER_HOST_CONFIG_DIR` | `~/.claude` | Каталог, захваченный в снимок запуска runner и посеянный в `CLAUDE_CONFIG_DIR` каждого сеанса; изменения на диске применяются после перезагрузки runner. Установка переменной также перемещает, где runner читает `.claude.json` для [MCP seeding](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#mcp-servers), поэтому установка её, включая её собственное значение по умолчанию, перемещает этот поиск; укажите на пустой каталог для полного отключения посева. |
| `SELF_HOSTED_RUNNER_MAX_LIFETIME_GRACE_MS` | `900000` | Как долго runner ждет после того, как сеанс достигает своего лимита `--kill-session-after-min`, чтобы текущий ход завершился или отпуск завершился, перед завершением сеанса |
| `SELF_HOSTED_RUNNER_POST_TURN_SETTLE_MS` | `7000` | Ограничение на то, как долго runner считает сеанс занятым для осушения `--drain-wait-sec` после завершения хода, пока процесс сеанса сообщает об окончании хода в Anthropic. `0` или непригодное значение возвращается к значению по умолчанию, поэтому удержание не может быть отключено. Требует Claude Code v2.1.275 или позже. |
| `SELF_HOSTED_RUNNER_SIGKILL_GRACE_MS` | `30000` | Как долго runner ждет, пока ОС доставит `SIGKILL` дочернему процессу, застрявшему в неперерываемом I/O, перед выходом самого себя. Минимум `--post-session-hook-timeout-sec` плюс 15 секунд, и 30 больше, когда установлен `--push-outcome-on-release`, поэтому эффективный минимум составляет 75 секунд при значениях по умолчанию. |
| `CLAUDE_RUNNER_DISABLE_RENEWAL_WARNING` | unset | Когда `1`, runner не публикует в сессии сообщение `The server has refused to renew this session's access to the model`. После каждого отказа он ждёт следующего запланированного продления, чтобы запросить снова. Требует Claude Code v2.1.319 или позже. |
| `CLAUDE_RUNNER_FETCH_DEPTH` | `50` | Глубина выборки Git для свежих клонов. Установите положительное целое число или `full` или `0` для полной выборки. Для клона, который уже находится в рабочем пространстве, см. [Повторное использование заранее подготовленного checkout](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#reuse-a-pre-warmed-checkout). |
| `CLAUDE_RUNNER_FETCH_SERVER_PROGRESS_CAP_MS` | `600000` | Как долго в миллисекундах, в рамках одной попытки, выборка git может ждать первых данных, пока собственные показатели прогресса сервера git продолжают расти, например когда сервер подготавливает pack для большого репозитория. `0` или `off` отключает ожидание: тогда такая выборка прерывается через две минуты без данных. Любое другое целое число ограничивается диапазоном от `120000` до `1800000`, то есть от 2 до 30 минут. Требует Claude Code v2.1.295 или позже. |
| `CLAUDE_RUNNER_SKIP_GIT_VERIFY` | unset | Когда `1`, пропустите проверку наличия `.git` после запуска hook `checkout`. Установите это, когда ваш hook материализует источник, не являющийся git. |
| `FORCE_AUTOUPDATE_PLUGINS` | unset | Когда `1`, позвольте маркетплейсам плагинов автоматически обновляться, несмотря на то, что бинарный файл закреплен |
| `CLAUDE_CODE_DISABLE_ARTIFACT` | unset | Когда `1`, отключите инструмент Artifact в сеансах независимо от параметра администратора организации и удалите требование к исходящему трафику на `*.frame.claudeusercontent.com` |

## Телеметрия

Дочерние процессы сеанса отправляют операционную телеметрию в Anthropic, если вы её не отключите. Никакой код или содержимое репозитория не отправляется. Установите переменные телеметрии на процесс runner; runner переустанавливает их после применения переменных окружения, предоставленных сервером, поэтому параметр оператора всегда имеет приоритет.

Один элемент управления специфичен для самостоятельно размещаемых сред: `CLAUDE_CODE_BYOC_ENABLE_DATADOG=1` выбирает метрики операционной деятельности Datadog, которые по умолчанию отключены в самостоятельно размещаемых средах. Общие элементы управления телеметрией Claude Code, `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `DISABLE_ERROR_REPORTING` и `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, применяются к дочерним процессам сессии, как задокументировано в [справочнике переменных окружения](https://code.claude.com/docs/ru/env-vars.md). [`CLAUDE_CODE_DISABLE_FEATURE_FLAGS`](https://code.claude.com/docs/ru/env-vars#variables) связан, но отличается: установка `CLAUDE_CODE_DISABLE_FEATURE_FLAGS=1` отключает выборку флагов функций, и телеметрия остается включенной, если также не установлен `DISABLE_TELEMETRY`. `CLAUDE_CODE_DISABLE_FEATURE_FLAGS` требует Claude Code v2.1.319 или более поздней версии.

`CLAUDE_CODE_ENABLE_TELEMETRY` не связан: он включает экспорт OpenTelemetry на ваш собственный сборщик, как описано в [Monitoring](https://code.claude.com/docs/ru/monitoring-usage.md), и не контролирует аналитику Anthropic.

## Конечная точка здоровья

Runner обслуживает `GET /healthz` на настроенном порту здоровья после того, как зарегистрируется и завершит проверки при запуске. С этого момента ответ — `200 OK` всякий раз, когда процесс живой, независимо от состояния цикла опроса, поэтому зонд HTTP на этом эндпоинте обнаруживает только мертвый процесс. Тело JSON описывает текущее состояние:

```json theme={null}
{
  "status": "ok",
  "runner_id": "ccrunner_...",
  "active_sessions": 2,
  "last_poll_at": "2026-03-31T18:04:11.220Z",
  "last_poll_age_ms": 842
}
```

Настройте оповещения по `last_poll_age_ms`, но не используйте это значение в зонде живости; для этого зонда опирайтесь на код состояния HTTP. Значение отражает время с момента последнего успешного опроса, поэтому оно также растет, пока runner не может связаться с Anthropic. Оба `last_poll_at` и `last_poll_age_ms` равны `null` до первого успешного опроса. Чтобы отловить опросы, которые завершаются ошибкой с самого начала, также настройте оповещения по метрике `claude_code_self_hosted_runner_poll_errors_total`, указанной в разделе [Метрики Prometheus](#prometheus-metrics).

Собственный `/healthz` orchestrator на его порту здоровья всегда возвращает `200`. Тело несет поле `connected`, сообщающее, успешен ли последний опрос, плюс количество очереди порождения для каждого состояния в `queue_counts`. Чтобы узнать, почему `connected` равно `false`, прочитайте поле верхнего уровня `last_error`, которое сбрасывается в `null` при каждом успешном опросе. Ограничьте готовность и оповещение на `connected` вместо кода состояния.

Когда [SCM connector](#scm-connector-flags) настроен, тело `/healthz` orchestrator также несет `scm_connector_connected` и объект `scm_connector` с `connected`, `last_connected_at`, `last_error`, `reconnects` и `requests_forwarded`. Оба поля равны `null`, когда `--scm-connector-host` не установлен.

## Метрики Prometheus

Каждый runner отдаёт метрики Prometheus по `GET /metrics` на том же порту, что и `/healthz`. Основные серии:

| Серия | Примечания |
| :- | :- |
| `claude_code_self_hosted_runner_info{runner_id,version,client_label}` | Всегда `1`; полезна для инвентаризации парка и обнаружения расхождения версий |
| `claude_code_self_hosted_runner_capacity` | Настроенное значение `--capacity` |
| `claude_code_self_hosted_runner_active_sessions` | Сессии, выполняющиеся в данный момент |
| `claude_code_self_hosted_runner_locked_account{email}` | Появляется, как только runner закреплён за пользователем и выдан токен сессии с утверждением `act.email`. Серия отсутствует на runner, закреплённом за агентом Claude Tag, поскольку его токены сессий не содержат `act.email`. Значение метки — email учётной записи; если ваше хранилище метрик доступно для чтения широкому кругу лиц, удаляйте или хешируйте метку при сборе, например с помощью `metric_relabel_configs` в Prometheus. |
| `claude_code_self_hosted_runner_last_poll_age_seconds` | Секунды с момента последнего успешного опроса. Настройте оповещение, если значение превышает 60. |
| `claude_code_self_hosted_runner_poll_errors_total{error_kind}` | Накопительное число сбоев PollWork по типам: `transport`, `timeout`, `5xx`, `429` или `4xx`. Все пять серий присутствуют с момента запуска процесса; настройте оповещение на `rate(...[5m]) > 0`. |
| `claude_code_self_hosted_runner_sessions_started_total{client_platform}` | Дочерние процессы сессий, запущенные за время жизни runner, по одной серии на источник сессии, например `web_claude_ai`, `ios`, `android`, `desktop_app` или `claude_code_cli`, либо `unknown`, если сервер его не передал. Сессии Slack помечаются либо `claude_in_slack`, либо `claude-in-slack` в зависимости от того, какая интеграция Slack их создала, поэтому сопоставляйте оба варианта селектором с регулярным выражением, например `{client_platform=~"claude[-_]in[-_]slack"}`. Используйте `sum()` для получения общего значения по парку. |
| `claude_code_self_hosted_runner_sessions_completed_total{client_platform}` | Сессии, завершившиеся штатно, с такими же метками. Понятие шире, чем просто штатный выход: что именно учитывается, см. в разделе [семантика счётчиков жизненного цикла сессий](#session-lifecycle-counter-semantics). |
| `claude_code_self_hosted_runner_sessions_failed_total{client_platform}` | Сессии, завершившиеся сбоем, с такими же метками. Та же оговорка: см. [семантика счётчиков жизненного цикла сессий](#session-lifecycle-counter-semantics). |
| `claude_code_self_hosted_runner_sessions_interrupted_total{client_platform}` | Сессии, которые runner завершил по эксплуатационной причине, а не по итогу самой сессии, с такими же метками. См. [семантика счётчиков жизненного цикла сессий](#session-lifecycle-counter-semantics). |
| `claude_code_self_hosted_runner_initializing_sessions` | Сессии, находящиеся в фазе инициализации: от назначения до события init дочернего процесса |
| `claude_code_self_hosted_runner_session_init_duration_seconds` | Гистограмма длительности инициализации сессий |
| `claude_code_self_hosted_runner_session_init_errors_total` | Сессии, завершившиеся сбоем до достижения init: сбой хука checkout, подготовки git, выдачи токена или падение дочернего процесса до init |
| `claude_code_self_hosted_runner_session_start_hook_errors_total` | Хуки `SessionStart`, сообщившие об ошибке, по одному на каждое неудачное выполнение хука |
| `claude_code_self_hosted_runner_session_idle_seconds{session_id,client_platform}` | Gauge для каждой сессии: секунды с момента перехода сессии в режим простоя. Полезна для завершения сессий, зависших на неотвеченном запросе разрешения. |

Оркестратор отдаёт собственные серии по `GET /metrics` на том же порту, что и его `/healthz`:

| Серия | Примечания |
| :- | :- |
| `claude_code_self_hosted_orchestrator_info{version,pool_id,orchestrator_uuid,hostname}` | Всегда `1` |
| `claude_code_self_hosted_orchestrator_connected` | `1`, если последний опрос завершился успешно; падает до `0` после любого неудачного опроса, независимо от типа сбоя |
| `claude_code_self_hosted_orchestrator_last_poll_age_seconds` | Секунды с момента последней попытки опроса, успешной или нет, в отличие от одноимённой метрики runner, которая отсчитывается от последнего успешного опроса; используйте вместе с `connected`, чтобы отлавливать неудачные опросы. Цикл опроса оркестратора ожидает выполнения хуков, поэтому настраивайте оповещение на значение выше `--hook-timeout` плюс запас, около 90 секунд при значениях по умолчанию, а не на фиксированные 60. |
| `claude_code_self_hosted_orchestrator_poll_errors_total{error_kind}` | Накопительное число сбоев PollSpawnHints по типам: `transport`, `timeout`, `5xx`, `429` или `4xx`. Все пять серий присутствуют с момента запуска процесса; настройте оповещение на `rate(...[5m]) > 0`. |
| `claude_code_self_hosted_orchestrator_queue_pending_sessions` | Запросы на запуск, которые можно забрать прямо сейчас |
| `claude_code_self_hosted_orchestrator_queue_backing_off_sessions` | Запросы на запуск, находящиеся в задержке перед повторной попыткой после сбоя хука, допускающего повторную попытку |
| `claude_code_self_hosted_orchestrator_queue_circuit_broken_sessions` | Сессии, запуск которых заблокирован. Каждая остаётся заблокированной, пока пользователь не отправит ей новое сообщение или Owner не повторит попытку на вкладке **Activity** окружения. Значение может оставаться выше нуля после устранения причины. Настройте оповещение, если значение выше нуля. |
| `claude_code_self_hosted_orchestrator_pool_pending_sessions` | Общее число сессий, ожидающих runner для этого окружения. Агрегат по всему окружению, одинаковый на каждом экземпляре оркестратора: используйте `MAX`, а не `SUM` по экземплярам. |
| `claude_code_self_hosted_orchestrator_pool_active_sessions` | Сессии, в данный момент назначенные работающему runner в этом окружении. Агрегат по всему окружению, одинаковый на каждом экземпляре оркестратора: используйте `MAX`, а не `SUM` по экземплярам. |
| `claude_code_self_hosted_orchestrator_spawn_hooks_total{result}` | Накопительные результаты хука `spawn-runner`: `ok`, `retryable`, `non_retryable`. Учитывает вызовы хука оркестратором, а не дочерние процессы сессий, которые запускают runner: несопоставима с `sessions_started_total`, поскольку ёмкость больше единицы, тёплые пулы и повторный запуск runner для той же сессии приводят к расхождению этих значений. |
| `claude_code_self_hosted_orchestrator_spawn_hook_duration_seconds` | Гистограмма длительности выполнения хука |
| `claude_code_self_hosted_orchestrator_warm_hints_dispatched_total` | Резервные запросы на запуск, отправленные с момента запуска процесса |
| `claude_code_self_hosted_orchestrator_session_queue_wait_seconds` | Гистограмма времени в секундах, которое каждая сессия провела в очереди, прежде чем оркестратор забрал её для запуска; записывается по метке времени ожидания в очереди, которую плоскость управления передаёт с запросом на запуск каждой сессии. Используйте для оповещений по p50/p99 времени в очереди. Запуски для предварительного прогрева не учитываются. |
| `claude_code_self_hosted_orchestrator_clock_skew_seconds` | Расхождение часов (локальное минус серверное); диагностическая метрика, появляется после измерения |
| `claude_code_self_hosted_orchestrator_scm_connector_connected` | `1`, когда WebSocket [коннектора SCM](#scm-connector-flags) открыт; `0` во время подключения или задержки перед повторной попыткой. Отсутствует, если `--scm-connector-host` не задан. |
| `claude_code_self_hosted_orchestrator_scm_connector_requests_forwarded_total` | Накопительное число HTTP-запросов, проксированных на настроенный хост SCM с момента запуска процесса. Отсутствует, если `--scm-connector-host` не задан. |

Для автомасштабирования выберите серию, соответствующую вашему подходу к масштабированию, и отфильтруйте её, прежде чем передавать в механизм масштабирования:

* **Масштабирование по глубине очереди**: передавайте в HPA или KEDA `claude_code_self_hosted_orchestrator_pool_pending_sessions`, а не `queue_pending_sessions`.
* **Масштабирование по ёмкости**: масштабируйте по отношению `active_sessions` runner к `capacity`.
* **Фильтрация по `connected`**: фильтруйте запрос условием `claude_code_self_hosted_orchestrator_connected == 1` для каждого экземпляра, чтобы устаревшее значение отключённой реплики не попадало в механизм масштабирования.

Во время полного сбоя опроса, когда все реплики отключены, отфильтрованный запрос не возвращает данных. HPA сохраняет текущее число реплик при отсутствии метрики, однако Prometheus scaler в KEDA со значением по умолчанию `ignoreNullValues: "true"` интерпретирует пустой результат как ноль и уменьшает число реплик; задайте `ignoreNullValues: "false"` в ScaledObject, при необходимости вместе с минимальным числом реплик `fallback`.

Следующий `PodMonitor` для Prometheus Operator охватывает оба процесса. Он выбирает поды по метке `app.kubernetes.io/part-of: claude-code-self-hosted-runner` и именованному порту `health`, которые задаёт [рецепт для Kubernetes](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#kubernetes); скорректируйте пространства имён в соответствии с вашим развёртыванием:

```yaml theme={null}
# Example Prometheus Operator PodMonitor for the Claude Code self-hosted
# runner + orchestrator. Adjust the namespace and label selectors to match
# your deployment. Both the runner and the orchestrator serve /metrics on
# their --health-port (default 8080).
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: claude-code-self-hosted-runner
  namespace: monitoring
spec:
  namespaceSelector:
    matchNames:
      - claude-runners
  selector:
    matchExpressions:
      # Matches the runner Deployment from the Kubernetes recipe, plus any
      # on-demand runner Jobs and orchestrator pods you label the same way
      # and give a named 'health' containerPort.
      - key: app.kubernetes.io/part-of
        operator: In
        values: [claude-code-self-hosted-runner]
  podMetricsEndpoints:
    - port: health
      path: /metrics
      interval: 30s
```

### Примеры правил оповещений

Эти примеры правил оповещений — отправная точка; настройте пороговые значения под размер вашего парка:

```yaml theme={null}
# Example Prometheus alert rules for the Claude Code self-hosted runner
# + orchestrator. Tune thresholds for your fleet size and SLOs.
groups:
  - name: claude-code-self-hosted-runner
    rules:
      - alert: ClaudeRunnerPollStale
        expr: claude_code_self_hosted_runner_last_poll_age_seconds > 60
        for: 2m
        labels: {severity: warning}
        annotations:
          summary: "Runner {{ $labels.pod }} has not polled in >60s"
      - alert: ClaudeRunnerVersionDrift
        expr: count(count by (version) (claude_code_self_hosted_runner_info)) > 1
        for: 30m
        labels: {severity: info}
        annotations:
          summary: "Runners are running mixed versions"
      - alert: ClaudeRunnerInitErrorsHigh
        expr: sum by (namespace) (increase(claude_code_self_hosted_runner_session_init_errors_total[10m])) > 3
        for: 5m
        labels: {severity: warning}
        annotations:
          summary: "Sessions are failing before init (checkout hook / git / token / pre-init crash)"
      - alert: ClaudeRunnerPollErrors
        expr: sum by (pod) (rate(claude_code_self_hosted_runner_poll_errors_total[5m])) > 0
        for: 2m
        labels: {severity: warning}
        annotations:
          summary: "Runner {{ $labels.pod }}: PollWork failing ({{ $value | humanize }}/s over 5m)"
      - alert: ClaudeRunnerSessionStartHookErrors
        expr: sum by (namespace) (increase(claude_code_self_hosted_runner_session_start_hook_errors_total[10m])) > 3
        for: 5m
        labels: {severity: warning}
        annotations:
          summary: "SessionStart hooks are failing"

  - name: claude-code-self-hosted-orchestrator
    rules:
      - alert: ClaudeOrchestratorDisconnected
        expr: claude_code_self_hosted_orchestrator_connected == 0
        for: 2m
        labels: {severity: critical}
        annotations:
          summary: "Orchestrator {{ $labels.pod }} cannot reach the Anthropic control plane"
      - alert: ClaudeOrchestratorPollStale
        expr: claude_code_self_hosted_orchestrator_last_poll_age_seconds > 90
        for: 2m
        labels: {severity: warning}
        annotations:
          summary: "Orchestrator {{ $labels.pod }} has not polled in >90s (poll loop waits on hook execution)"
      - alert: ClaudeOrchestratorCircuitBroken
        expr: max by (namespace) (claude_code_self_hosted_orchestrator_queue_circuit_broken_sessions and on (instance) max_over_time(claude_code_self_hosted_orchestrator_connected[2m]) == 1) > 0
        for: 1m
        labels: {severity: critical}
        annotations:
          summary: "Sessions blocked from spawning: {{ $value }}. Read each one's error in the Activity tab, fix the cause, then select Retry"
      - alert: ClaudeOrchestratorPollErrors
        expr: sum by (pod) (rate(claude_code_self_hosted_orchestrator_poll_errors_total[5m])) > 0
        for: 2m
        labels: {severity: warning}
        annotations:
          summary: "Orchestrator {{ $labels.pod }}: PollSpawnHints failing ({{ $value | humanize }}/s over 5m)"
      - alert: ClaudeOrchestratorSpawnHookFailing
        expr: sum by (pod) (increase(claude_code_self_hosted_orchestrator_spawn_hooks_total{result!="ok"}[5m])) > 3
        for: 5m
        labels: {severity: warning}
        annotations:
          summary: "Orchestrator {{ $labels.pod }}: >3 spawn-runner hook failures in 5m"
```

### Оповещения о потере runner и ожидающих сессиях

Чтобы получать оповещения о потере runner, ожидании сессий или недоступности оркестратора, загрузите эти правила оповещений Prometheus вместе с [примерами правил оповещений](#sample-alert-rules):

* **[Фиксированный парк](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#scale-the-fleet)**: `ClaudeRunnersBelowFloor`
* **[Runner по требованию](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners)**: `ClaudeOrchestratorSessionsWaiting`, `ClaudeOrchestratorQueueWaitHigh` и `ClaudeOrchestratorAbsent`

#### Оповещение о потере runner в фиксированном парке

`ClaudeRunnersBelowFloor` срабатывает, когда в течение 10 минут зарегистрированных runner, с которых собираются метрики, остаётся меньше минимального порога:

```yaml theme={null}
groups:
  # Fixed fleets only. With on-demand runners the count follows demand,
  # so ClaudeRunnersBelowFloor would fire whenever demand is low.
  - name: claude-code-self-hosted-fixed-fleet-capacity
    rules:
      - alert: ClaudeRunnersBelowFloor
        expr: (count(claude_code_self_hosted_runner_info{namespace="claude-runners"}) or vector(0)) < 2
        for: 10m
        labels: {severity: critical, namespace: claude-runners}
        annotations:
          summary: "Runners registered and scraped: {{ $value }}, below the floor. Check the runner workloads first, then the scrape targets if all are running."
```

* **Минимальный порог**: задайте `2` в `expr` примерно равным половине числа реплик с округлением вверх. При трёх репликах оставьте `2`, и оповещение сработает, когда останется один runner или ни одного.
* **Пространство имён**: замените `claude-runners` в matcher и в `labels` и скопируйте оповещение для каждого дополнительного пространства имён. Если у ваших целей нет метки `namespace`, удалите matcher и метку, иначе оповещение получит 0 и сработает.
* **`ClaudeRunnerPollStale` и `ClaudeRunnerPollErrors`**: оставьте их загруженными из [примеров правил оповещений](#sample-alert-rules), поскольку `ClaudeRunnersBelowFloor` по-прежнему учитывает runner, который не может выполнить опрос

#### Оповещение об ожидании сессиями runner по требованию

`ClaudeOrchestratorSessionsWaiting` срабатывает, когда число сессий, ожидающих runner, остаётся выше 0 в течение 10 минут. `ClaudeOrchestratorQueueWaitHigh` срабатывает, когда более 1% ожиданий в очереди за последние 10 минут превысили 160 секунд и это сохраняется в течение 5 минут:

```yaml theme={null}
groups:
  # On-demand runners only. Needs no edit for the namespace.
  - name: claude-code-self-hosted-on-demand-capacity
    rules:
      - alert: ClaudeOrchestratorSessionsWaiting
        expr: |
          max by (namespace) (
            claude_code_self_hosted_orchestrator_pool_pending_sessions
            and on (instance)
            max_over_time(claude_code_self_hosted_orchestrator_connected[2m]) == 1
          ) > 0
        for: 10m
        labels: {severity: warning}
        annotations:
          summary: "Sessions waiting for a runner: {{ $value }}, above the threshold for 10 minutes. Check claude_code_self_hosted_orchestrator_spawn_hooks_total by result, then runner workloads that don't start."
      - alert: ClaudeOrchestratorQueueWaitHigh
        expr: |
          histogram_quantile(0.99, sum by (namespace, le) (
            rate(claude_code_self_hosted_orchestrator_session_queue_wait_seconds_bucket[10m])
          )) > 160
        for: 5m
        labels: {severity: warning}
        annotations:
          summary: "Over 1% of queue waits in the last 10 minutes exceeded 160 seconds. Check whether ClaudeOrchestratorDisconnected is firing, then claude_code_self_hosted_orchestrator_spawn_hooks_total by result and claude_code_self_hosted_orchestrator_spawn_hook_duration_seconds."
```

* **Порог**: если какая-то сессия ожидает постоянно, поднимите `> 0` в `ClaudeOrchestratorSessionsWaiting` выше значения, которое вы обычно наблюдаете
* **`ClaudeOrchestratorDisconnected`**: оставьте его загруженным из [примеров правил оповещений](#sample-alert-rules), поскольку `ClaudeOrchestratorSessionsWaiting` перестаёт срабатывать примерно через 2 минуты после отключения последнего оркестратора в пространстве имён

#### Оповещение о недоступности оркестратора

Чтобы узнавать о недоступности самого [оркестратора](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners), загрузите `ClaudeOrchestratorAbsent`. Оно срабатывает, когда в течение 5 минут метрики не собираются ни с одного оркестратора в пространстве имён:

```yaml theme={null}
groups:
  # On-demand runners only. Replace claude-runners with the orchestrator's namespace.
  - name: claude-code-self-hosted-on-demand-orchestrator
    rules:
      - alert: ClaudeOrchestratorAbsent
        expr: absent(claude_code_self_hosted_orchestrator_connected{namespace="claude-runners"})
        for: 5m
        labels: {severity: critical}
        annotations:
          summary: "No orchestrator has been scraped for 5 minutes. If it's down, no on-demand runner starts, and sessions wait. Check the orchestrator workload first, then its scrape target if it's running."
```

* **Пространство имён**: замените `claude-runners` на пространство имён оркестратора и скопируйте оповещение для каждого дополнительного пространства имён, в котором работает оркестратор. Если у ваших целей нет метки `namespace`, удалите matcher, иначе оповещение сработает через 5 минут и не отключится.
* **Серверы Prometheus, которые не собирают метрики оркестратора**: не включайте это оповещение в их файлы правил, поскольку на таком сервере оно срабатывает через 5 минут и не отключается
* **Не полагайтесь на другие оповещения оркестратора**: они читают метрики, которые отдаёт сам оркестратор. `ClaudeOrchestratorSessionsWaiting`, `ClaudeOrchestratorQueueWaitHigh` и [примеры правил оповещений](#sample-alert-rules) для оркестратора перестают срабатывать примерно в течение 10 минут после отказа оркестратора.

### Проброс метрик дочерних процессов сессий

Каждая сессия выполняется в собственном дочернем процессе со своими метриками OpenTelemetry; при `--capacity` больше единицы runner изменяет способ публикации этих дочерних метрик. Если задать `OTEL_METRICS_EXPORTER=prometheus` на хосте runner и `CLAUDE_CODE_ENABLE_TELEMETRY=1` в окружении сессии, например из вашего [скрипта-обёртки](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#wrapper-scripts) или в собственном окружении runner, которое наследуют сессии, то инструменты типа counter и gauge каждого дочернего процесса будут повторно опубликованы на собственном эндпоинте `/metrics` runner рядом с сериями самого runner. Runner перенастраивает экспортёр дочернего процесса на отправку по OTLP в приёмник на порту health, доступный только через loopback, помечает каждую серию метками `session_id` и `client_platform` и удаляет серии сессии, когда эта сессия завершается. Гистограммы не пробрасываются, а дочерняя метрика, имя которой конфликтовало бы с собственным префиксом runner, отбрасывается.

При значении по умолчанию `--capacity 1` эта перенастройка не применяется: дочерний процесс сессии, как обычно, открывает собственный эндпоинт Prometheus на порту 9464.

#### Сопоставление метрик сессии с метриками runner

Чтобы узнать, во что обошлись простаивающие сессии, соедините метрику runner `claude_code_self_hosted_runner_session_idle_seconds` с метрикой стоимости Claude Code по `ccr_session_id`. Метрика runner не содержит этой метки, поэтому добавьте её с помощью `label_replace`, как в этом запросе:

```text theme={null}
sum by (ccr_session_id) (claude_code_cost_usage_total)
and on (ccr_session_id)
label_replace(
  claude_code_self_hosted_runner_session_idle_seconds > 600,
  "ccr_session_id", "cse_$1", "session_id", "session_(.*)"
)
```

Запрос возвращает по одному результату на каждую сессию, простаивающую более десяти минут: стоимость в долларах США, которую её процесс Claude Code насчитал на данный момент. Чтобы соединить другую метрику Claude Code, замените `claude_code_cost_usage_total` в запросе. Запрос работает при любом значении `--capacity`.

* **`session_id`**: на порту 9464 эта метка у метрик Claude Code содержит собственный [`session.id`](https://code.claude.com/docs/ru/monitoring-usage#standard-attributes) Claude Code, который не совпадает ни с одной серией runner. Соединение по ней ничего не возвращает, поэтому соединяйте по `ccr_session_id`.
* **У метрик Claude Code нет `ccr_session_id`**: убедитесь, что [`OTEL_METRICS_INCLUDE_SESSION_ID`](https://code.claude.com/docs/ru/monitoring-usage#metrics-cardinality-control) не задана как `false`

### Семантика счётчиков жизненного цикла сессий

Счётчики `sessions_started_total`, `sessions_completed_total`, `sessions_failed_total` и `sessions_interrupted_total` классифицируют каждую сессию по тому, как она завершилась. Каждый запущенный дочерний процесс сессии увеличивает `sessions_started_total` в момент запуска, и ровно один из остальных трёх счётчиков увеличивается при выходе, поэтому `sessions_started_total` минус сумма остальных трёх равна числу дочерних процессов сессий, выполняющихся в данный момент.

* `completed`: сессия завершилась штатно. Сюда относятся: самостоятельный выход дочернего процесса с кодом `0`; архивация или удаление сессии, пока дочерний процесс ещё был подключён; штатное освобождение слота runner: освобождение сессии по таймауту простоя, по времени вывода из эксплуатации или по лимиту `--kill-session-after-min`; таймаут запуска; либо снятие назначения на стороне сервера, которое цикл опроса заметил до выхода дочернего процесса. Увеличивает `sessions_completed_total`.
* `failed`: дочерний процесс самостоятельно завершился с ненулевым кодом — из-за падения или сбоя настройки после запуска. Увеличивает `sessions_failed_total`.
* `interrupted`: runner завершил дочерний процесс по эксплуатационной причине, которая не является ни успехом сессии, ни ошибкой runner, например при выводе из работы (drain) или при завершении сессии, которая всё ещё находилась на runner по истечении окна отсрочки [`SELF_HOSTED_RUNNER_MAX_LIFETIME_GRACE_MS`](#environment-variable-only-settings) после её лимита `--kill-session-after-min`. Поэтапный перезапуск в Kubernetes с отправкой `SIGTERM` — один из примеров вывода из работы. Увеличивает `sessions_interrupted_total`.

До версии v2.1.260 runner завершал каждую сессию, достигшую лимита `--kill-session-after-min`, и учитывал её в `sessions_interrupted_total`.

Переменная `CLAUDE_RUNNER_EXIT_REASON` [хука `post-session`](https://code.claude.com/docs/ru/self-hosted-environments-configuration#post-session) классифицирует штатные передачи иначе. Хук сообщает о них как об `interrupted`, поскольку runner остановил дочерний процесс: это освобождение, таймаут запуска, снятие назначения сервером, а также архивация или удаление, которые первым заметил опрос. Эти счётчики записывают те же события как `completed`, поскольку слот был освобождён штатно.

Если сверять получение хуков непосредственно с `sessions_completed_total`, число завершений окажется заниженным. Используйте хук для гарантий на уровне отдельных сессий, а счётчики — для агрегированных показателей.

В одноразовом окружении, с `--capacity 1` и значением по умолчанию `--drain-grace-sec 0`, каждый процесс runner завершается через мгновение после окончания его единственной сессии. `sessions_completed_total`, `sessions_failed_total` и `sessions_interrupted_total` увеличиваются только в конце сессии, непосредственно перед этим выходом, поэтому сбор метрик Prometheus каждые 15–60 секунд редко успевает зафиксировать приращение до того, как серии runner исчезнут; именно эти три счётчика окончания сессии далее в этом разделе называются терминальными. `sessions_started_total` увеличивается при запуске и остаётся видимым на протяжении всей сессии, поэтому он надёжно появляется, однако в одноразовом окружении он скорее отражает «сессии, выполняющиеся в данный момент», чем накопительное значение.

Для соответствующей цели используйте серии из этой таблицы вместо терминальных счётчиков:

| Цель | Что использовать |
| :- | :- |
| Пропускная способность | `claude_code_self_hosted_orchestrator_spawn_hooks_total{result="ok"}` — счётчик на долгоживущем оркестраторе, который увеличивается один раз на каждое успешное выполнение хука `spawn-runner` и сохраняет смысл при использовании `rate()`. Он учитывает вызовы хука, а не сессии, поэтому предварительный прогрев и повторные запуски для одной и той же сессии приводят к расхождению с числом сессий. |
| Загрузка | `sum(claude_code_self_hosted_runner_active_sessions)` относительно `sum(claude_code_self_hosted_runner_capacity)`; обе метрики — gauge, корректные при каждом сборе независимо от времени жизни runner |
| Очередь | `claude_code_self_hosted_orchestrator_pool_pending_sessions` для глубины очереди и `claude_code_self_hosted_orchestrator_queue_circuit_broken_sessions` с оповещением, если значение выше нуля |
| Сбои | `claude_code_self_hosted_runner_sessions_failed_total`, по мере возможности: реальные падения после запуска его увеличивают, а `rate()` имеет смысл на runner, которые переживают свои сессии при `--drain-grace-sec` больше `0`. В одноразовом окружении существует та же проблема окна сбора, что и у остальных терминальных счётчиков, поэтому любое ненулевое значение, которое вы всё же увидите, стоит расследовать. Сбои до запуска, например сбой хука checkout, подготовки git или выдачи токена, отражаются только в `session_init_errors_total`. |

Строки `orchestrator_*` существуют только в окружениях, использующих [оркестратор по требованию](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners). В фиксированном парке, runner которого переживают свои сессии при `--drain-grace-sec` больше `0`, используйте `sum(rate(claude_code_self_hosted_runner_sessions_started_total[5m]))` для пропускной способности; в одноразовом парке у этой серии та же проблема окна сбора, что и у терминальных счётчиков, поэтому полагайтесь на число сессий в очереди. Проверяйте очередь на вкладке **Activity** окружения на [странице администрирования **Cloud environments**](https://claude.ai/admin-settings/cloud-environments): runner не экспортируют серию глубины очереди.

Для отчётности по итогам отдельных сессий используйте [хук `post-session`](https://code.claude.com/docs/ru/self-hosted-environments-configuration#post-session): он срабатывает при каждом завершении сессии, для которой был запущен дочерний процесс, за исключением внезапного завершения runner, например при вытеснении VM, в соответствии с [собственным контрактом хука](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#post-session).

## Что дальше

* [Self-hosted environments](https://code.claude.com/docs/ru/self-hosted-environments): среда, runner и модель сеанса; [quickstart](https://code.claude.com/docs/ru/self-hosted-environments-quickstart.md) и [Deploy to production](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md) содержат настройку и операции
* [Customize sessions](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md): скрипты-обертки, hooks жизненного цикла и on-demand runner
* [Verify session identity](https://code.claude.com/docs/ru/self-hosted-environments-identity.md): токен сеанса, его претензии и как его проверить
