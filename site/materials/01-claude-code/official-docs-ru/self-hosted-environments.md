> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Самостоятельно размещаемые окружения

> Запускайте сеансы Claude Code в облаке на инфраструктуре, которой вы управляете: настройте самостоятельно размещаемое окружение, разверните runners и маршрутизируйте сеансы на собственные вычислительные ресурсы.

> [!NOTE]
>
> Самостоятельно размещаемые окружения находятся в публичной бета-версии для планов Team и Enterprise и отключены по умолчанию. Смотрите [Доступность и ограничения](#availability-and-limitations) для пути включения и того, что исключено.

Самостоятельно размещаемое окружение выполняет облачные сессии Claude Code на инфраструктуре, которой управляет ваша организация. [Облачная сессия](https://code.claude.com/docs/ru/claude-code-on-the-web.md) — это любая сессия, которая выполняется не на машине разработчика. Разработчики запускают их из claude.ai, мобильных и настольных приложений, терминала с помощью [`claude --cloud`](https://code.claude.com/docs/ru/claude-code-on-the-web#from-terminal-to-cloud) и [облачных запланированных задач](https://code.claude.com/docs/ru/routines.md). По умолчанию облачные сессии выполняются на инфраструктуре Anthropic.

В самостоятельно размещаемом окружении эти же сессии выполняются внутри вашей сети. В остальном опыт разработчика остается прежним, за исключением различий, описанных в разделе [Доступность и ограничения](#availability-and-limitations), и [известных проблем](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#known-issues-and-limitations) на странице развертывания.

* Если ваша команда не использует облачные сессии, здесь нечего настраивать: сессии в терминале или IDE всегда выполняются на собственной машине разработчика
* Чтобы запустить Claude Code на собственной постоянно работающей машине и управлять ею с других устройств, используйте [Remote Control](https://code.claude.com/docs/ru/remote-control.md), который также доступен на планах Pro, Max и Ultra
* Когда вы будете готовы к настройке, переходите прямо к [быстрому старту](https://code.claude.com/docs/ru/self-hosted-environments-quickstart.md); чтобы сначала проверить позицию безопасности, начните с [Развертывание в production](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md)

Чтобы узнать, как работает самостоятельное размещение и когда его выбирать, прочитайте разделы [Как работают самостоятельно размещаемые окружения](#how-self-hosted-environments-work) и [Зачем использовать самостоятельное размещение](#why-self-host).

## Как работают самостоятельно размещаемые окружения

Самостоятельное размещение состоит из трех частей:

* **Environment**: именованное место назначения, на которое можно отправлять облачные сеансы. Ваша организация создает окружения в параметрах администратора claude.ai, и каждое группирует набор runners.
* **Runner**: программа, работающая на хостах внутри вашей сети. Runners выполняют сеансы; идея такая же, как у self-hosted CI runner.
* **Session**: одна задача Claude Code, запущенная разработчиком.

Когда разработчик запускает облачную сессию, интерфейс запуска сессии показывает средство выбора окружения, в котором перечислены окружения, размещаемые Anthropic, наряду с любыми созданными вашей организацией. Если они выбирают ваше, плоскость управления Anthropic помещает сессию в очередь вашего окружения, где runner берёт её в работу, клонирует репозиторий, выбранный разработчиком, и запускает процесс Claude Code на вашем хосте для её выполнения. Runner аутентифицируется на вашем git-хосте с учётными данными, которые вы настраиваете; [Настройка git](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#configure-git) описывает варианты. Сессии достигают ваших внутренних сервисов изнутри вашей сети, и вашего git-хоста таким же образом, когда он внутренний; трафик к Anthropic (опрос очереди, поток событий сессии и по умолчанию вывод модели) — это исходящий HTTPS к `api.anthropic.com`, а короткий список дополнительных хостов, к которым могут обращаться сессии, приведён в разделе [Требования к сети](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#network-requirements). Anthropic никогда не подключается к вашей сети.

![Architecture diagram of a self-hosted environment: your network boundary contains a runner, two Claude Code session processes inside it, and your git host, with api.anthropic.com outside holding queue, session stream, and inference. The runner polls the queue and reaches the git host, each session process opens its own stream, inference, and git connections, and every connection is outbound from your network, with none inbound.](https://mintcdn.com/claude-code/Y0sJ2uDoOVbOVZrQ/images/self-hosted-network-paths.svg?fit=max\&auto=format\&n=Y0sJ2uDoOVbOVZrQ\&q=85\&s=8056103fc1c5564c7f0ef219d260b99d)

Два поля Claude Code на диаграмме — это процессы сеанса: один runner, выполняющий два сеанса одновременно, до его настроенной емкости. Runner служит одному [владельцу](#key-concepts) за раз и закрепляется за этим владельцем, когда берёт в работу свой первый сеанс, поэтому проверенный код никогда не смешивается между владельцами; [Жизненный цикл runner](#runner-lifecycle) охватывает правило.

Вы можете запустить runners самостоятельно и держать их работающими, или запустить [автомасштабирующийся оркестратор](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners) — второй процесс, который вы размещаете и который запускает runners по мере постановки сессий в очередь. В любом случае вы настраиваете окружение один раз, и оно появляется в средстве выбора в каждом поддерживаемом интерфейсе.

## Доступность и ограничения

Проверьте это перед планированием развертывания:

* **Plans**: публичная бета для организаций Team и Enterprise. Самостоятельно размещаемые окружения отключены по умолчанию; [Owner](https://code.claude.com/docs/ru/cloud-environments.md#organization-shared-environments) включает **Allow self-hosted environments** на [странице администратора **Cloud environments**](https://claude.ai/admin-settings/cloud-environments), что требует [cloud sessions](https://code.claude.com/docs/ru/claude-code-on-the-web.md) для включения для организации.
* **Zero Data Retention and HIPAA**: недоступно для организаций с включенным [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md) или с примененной [конфигурацией HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md).
* **Model inference**: сессии используют Anthropic API, если только вы не настроите раннер для [отправки запросов модели в Amazon Bedrock или Google Cloud's Agent Platform](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#send-model-requests-to-bedrock-or-agent-platform). В обоих случаях содержимое сессий передается в Anthropic. На раннере, настроенном таким образом, [управляемые сервером настройки](https://code.claude.com/docs/ru/server-managed-settings.md) и политики организации из claude.ai не применяются к сессиям.
* **Surfaces**: сессии, запущенные из [claude.ai/code](https://claude.ai/code), мобильных и настольных приложений, [облачных запланированных задач](https://code.claude.com/docs/ru/routines.md) и терминала с помощью [`claude --cloud`](https://code.claude.com/docs/ru/claude-code-on-the-web#from-terminal-to-cloud) или [`--environment` dispatch](https://code.claude.com/docs/ru/self-hosted-environments-testing#run-the-test-loop), могут работать в самостоятельно размещаемых окружениях. Сессии [Claude Tag](https://claude.com/docs/claude-tag/overview) тоже могут работать в них, но Claude пока не может использовать [Access bundles](https://claude.com/docs/claude-tag/concepts/glossary#access-bundle) в этих сессиях. Сессии [Claude Security](https://code.claude.com/docs/ru/claude-security.md) и [Code Review](https://code.claude.com/docs/ru/code-review.md) пока не направляются в них. Поддержка этих двух интерфейсов появится отдельно.
* **Repositories**: сессии извлекают репозитории из GitHub или GitHub Enterprise Server. Сессии, запущенные с помощью `--environment` dispatch, также могут использовать другой git-хост:
  * **GitHub**: смотрите [Варианты аутентификации GitHub](https://code.claude.com/docs/ru/claude-code-on-the-web.md#github-authentication-options).
  * **GitHub Enterprise Server**: смотрите его [требования к сети](https://code.claude.com/docs/ru/github-enterprise-server.md#network-requirements).
  * **Another git host**: смотрите [требования для запуска сессии с `--environment`](https://code.claude.com/docs/ru/self-hosted-environments-deploy#start-a-session-on-a-repository-outside-github).
* **Billing**: сеансы в самостоятельно размещаемом окружении потребляют использование Claude Code вашей организации так же, как сеансы в окружениях, размещаемых Anthropic.

## Почему самостоятельное размещение

Большинство команд лучше обслуживаются окружениями, размещаемыми Anthropic, которые не требуют инфраструктуры для запуска или обслуживания. Самостоятельное размещение предназначено для команд, чьи требования к сети, инструментам или соответствию требуют сохранения выполнения сеанса на инфраструктуре, которой они управляют. Если это вы, планируйте оперативное владение, которое оно несет: вы создаете и поддерживаете образ runner, управляете флотом и контролируете его сеть.

В обмен самостоятельное размещение дает вам доступ к сети, пользовательские инструменты и контроль соответствия:

* **Network access**: сеансы работают внутри вашей сети и могут достичь внутренних сервисов, баз данных и реестров без их раскрытия в общедоступный интернет
* **Custom tooling**: предварительно установите компиляторы, SDK и внутренние CLI в образ runner, чтобы каждый сеанс начинался готовым к сборке
* **Соответствие требованиям**: извлечённые копии репозиториев и артефакты сборки остаются на инфраструктуре, которой вы управляете. Содержимое сессий по-прежнему отправляется на `api.anthropic.com`.

## Окружения, runners и сеансы

Окружения управляются на странице **Cloud environments** в параметрах администратора claude.ai; runners — это процессы, которые вы запускаете и управляете на собственной инфраструктуре.

### Ключевые концепции

Эти термины появляются на всех страницах self-hosted:

| Термин | Что это |
| :- | :- |
| Environment | Именованная группа ваших runners, созданная в параметрах claude.ai. Сеансы маршрутизируются на окружение, а не на отдельный runner. |
| Environment secret | Единственное общее учетное данные, которое runners используют для аутентификации и регистрации в окружении. Показано один раз при создании окружения, помечено как **environment key** в пользовательском интерфейсе администратора. |
| Runner | Долгоживущий процесс, который вы развертываете. Runner регистрируется в окружении, получает токен runner и опрашивает сеансы. |
| Session | Одна задача Claude Code, запущенная из claude.ai, мобильного приложения или другого интерфейса Anthropic, например запланированной задачи или агента. Каждая сессия работает как дочерний процесс Claude Code, порождаемый runner. |

В полях API, утверждениях токенов и названиях метрик окружение отображается как `pool`, а ID окружения — это `pool_id`. [Справка](https://code.claude.com/docs/ru/self-hosted-environments-reference.md) отображает два написания, включая устаревшие названия флагов `pool`.

Runner служит одному владельцу за раз. Первый сеанс, который runner берёт в работу, закрепляет runner за владельцем этого сеанса, и runner затем запускает сеансы только для этого владельца, до настроенной емкости. Кто владелец, зависит от того, как был запущен сеанс:

* **Сеансы, запущенные пользователем**: владелец — это учетная запись этого пользователя.
* **Сеансы канала Claude Tag**: Claude запускает их без прикрепленной учетной записи пользователя, поэтому владелец — это [агент Claude Tag](https://claude.com/docs/claude-tag/concepts/glossary#agent-identity), который запустил сеанс. Каждый сеанс канала, который запускает этот агент, имеет одного владельца, кто бы ни отправил сообщение Slack, поэтому runner, закреплённый за ним, обслуживает сеансы, которые разные люди запустили, когда вы запускаете его с `--capacity` выше одного или с положительным `--drain-grace-sec`.

Минимальный размер флота — это количество владельцев, которых вы ожидаете быть активными одновременно, считая пользователей и агентов Claude Tag.

### Жизненный цикл сеанса

Когда разработчик запускает сеанс и выбирает ваше окружение, плоскость управления Anthropic помещает сеанс в очередь окружения. Отсюда:

1. Runner со свободной емкостью требует сеанс и держит аренду на нем.
2. Runner клонирует репозиторий в свой рабочий каталог и порождает дочерний процесс Claude Code.
3. Дочерний процесс передает события обратно по HTTPS, пока runner продолжает опрашивать; каждый опрос обновляет аренду и служит сердцебиением.
4. Если runner прекращает опрос, его аренда истекает примерно через 60 секунд. После этого серверу может потребоваться несколько минут, а иногда и больше, чтобы повторно поставить сессию в очередь для другого runner.

Runner дает каждому запросу опроса 10 секунд. Когда запрос истекает, теряется или получает ответ, который runner не может разобрать, runner продолжает служить своим активным сеансам и повторяет попытку через секунду или две вместо ожидания следующего запланированного опроса. Например, перехватывающий прокси, который отвечает на опрос своей собственной страницей, производит ответ, который runner не может разобрать. Каждый раз, когда другой запрос не удается одним из этих способов, runner удваивает промежуток перед следующей повторной попыткой, до 20 секунд, и сокращает промежуток, когда аренда близка к истечению.

### Жизненный цикл runner

Первый сеанс, который runner берёт в работу, закрепляет runner за владельцем этого сеанса, и runner запускает до `--capacity` одновременных сеансов для этого владельца. Пока runner имеет активные сеансы и не получил сигнал завершения или не достиг времени выхода, runner продолжает забирать из очереди работу владельца, за которым он закреплён. Что происходит после их завершения, зависит от [`--drain-grace-sec`](https://code.claude.com/docs/ru/self-hosted-environments-reference#runner-cli-flags):

* **По умолчанию `0`**: runner выходит, как только его активные сеансы завершаются, без опроса дополнительно, поэтому оркестратор, под которым вы его развертываете, такой как Kubernetes, может перезапустить его со свежим диском, готовым служить любому владельцу.
* **При положительном значении**: runner продолжает опрашивать очередь владельца, за которым он закреплён в течение этого количества секунд перед выходом.

Этот жизненный цикл изолирует проверенный код каждого владельца без необходимости runner удалять состояние диска между владельцами.

То, как ваша инфраструктура останавливает runner, решает, нужен ли вам `--retire-at`. Убийство, которое доставляет `SIGTERM`, не требует флага: runner дренирует как [Timing shutdown](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#shutdown-timing) описывает, или продолжает служить сеансам, которые он уже держит, когда вы устанавливаете [`--defer-shutdown-max-min`](https://code.claude.com/docs/ru/self-hosted-environments-deploy#defer-the-drain-past-the-first-signal). Если ваша инфраструктура вместо этого уничтожает хосты в известное время по стене без сигнала, или с периодом благодати слишком коротким для дренирования, такой как ограничение времени жизни песочницы или отзыв spot-instance, передайте `--retire-at <epoch-seconds>` установленный на несколько минут раньше этого времени. В момент выхода:

1. Runner перестает принимать новую работу.
2. Runner освобождает каждую активную сессию тем же способом, который использует флаг [`--release-idle-session-min`](https://code.claude.com/docs/ru/self-hosted-environments-reference#runner-cli-flags), поэтому сессия возобновляется на новом runner, когда пользователь отправляет следующее сообщение. Когда runner освобождает каждую сессию, зависит от её состояния:
   * Runner освобождает сессию, находящуюся в середине хода, после завершения этого хода. Сначала он ждёт, пока процесс сессии сообщит Anthropic о завершении хода, но не дольше [`SELF_HOSTED_RUNNER_POST_TURN_SETTLE_MS`](https://code.claude.com/docs/ru/self-hosted-environments-reference#environment-variable-only-settings). До версии v2.1.280 runner освобождал сессию сразу после завершения хода.
   * Когда ход завершается, оставляя работающие фоновые задачи, runner ждёт их до 60 секунд, а затем освобождает сессию, даже если они ещё выполняются. Если задачи завершились, но последующий ход, который читает их результаты, ещё не запустился, runner удерживает сессию до завершения этого хода и ждёт начала этого хода не дольше [`SELF_HOSTED_RUNNER_BG_RESULT_GRACE_MS`](https://code.claude.com/docs/ru/self-hosted-environments-reference#environment-variable-only-settings).
3. Runner выходит 0 после выпуска всех его сеансов.

Ход, который переживает убийство, все еще потерян; [Timing shutdown](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#shutdown-timing) охватывает размер маржи. Без `--retire-at`, убийство хоста без сигнала неотличимо от краха: плоскость управления записывает потерянного worker вместо чистого выпуска, и сеанс повторно ставится в очередь другому runner.

### Сетевые пути

Runner и его сеансы делают несколько видов исходящего соединения, и входящее соединение от Anthropic не требуется:

* **Control plane**: runner опрашивает `api.anthropic.com` для работы и публикует события прогресса установки и отказа, все исходящие HTTPS. Опрос служит сердцебиением runner.
* **Git**: runner клонирует репозитории с вашего git-хоста и отправляет на него изменения по HTTPS или SSH, аутентифицируясь с помощью учётных данных, которые предоставляет ваше развёртывание. Варианты, включая учётные данные, выпускаемые для каждой сессии, описаны в разделе [Настройка git](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#configure-git). При использовании [git-прокси Anthropic](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#use-the-anthropic-git-proxy) git-трафик для репозиториев на github.com вместо этого проходит через `api.anthropic.com`.
* **Session child**: дочерний процесс Claude Code удерживает поток событий сессии к `api.anthropic.com` и выполняет собственные исходящие вызовы для инференса модели и для команд git, запускаемых во время сессии. В сессии, использующей [git под управлением Anthropic](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#use-the-anthropic-git-proxy), дочерний процесс открывает WebSocket-соединение к `api.anthropic.com`, по которому передаётся трафик `git` и `gh` для github.com.
* **SCM connector**: дополнительный [SCM connector](https://code.claude.com/docs/ru/self-hosted-environments-reference.md#scm-connector-flags) оркестратора недоступен, поэтому его туннель не открывается. Туннель — это WebSocket-соединение с `api.anthropic.com`.

Полный список исходящих адресов см. в разделе [Требования к сети](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#network-requirements). [Диаграмма выше](#how-self-hosted-environments-work) показывает эти пути, за исключением дополнительного SCM connector и соединения git под управлением Anthropic.

По умолчанию инференс модели использует Anthropic API. Плоскость управления передаёт эндпоинт API каждой сессии, и сессия аутентифицируется с помощью выданного Anthropic токена OAuth с областью действия сессии. Чтобы вместо этого отправлять запросы к модели в собственную облачную учётную запись, см. раздел [Отправка запросов к модели в Bedrock или Agent Platform](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#send-model-requests-to-bedrock-or-agent-platform).

Корпоративные прокси выхода поддерживаются. Runner и дополнительный [автомасштабирующийся оркестратор](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#on-demand-runners) соблюдают прокси и переменные mTLS, описанные в [Конфигурация сети](https://code.claude.com/docs/ru/network-config.md), такие как `HTTPS_PROXY` и `NO_PROXY`; установите их в окружение каждого процесса. Переменные охватывают вызовы плоскости управления, WebSocket [SCM connector](https://code.claude.com/docs/ru/self-hosted-environments-reference.md#scm-connector-flags) оркестратора и встроенный клон для HTTPS remotes, и сеансы наследуют их от runner. Потоковая передача сеанса использует события, отправляемые сервером, по HTTPS, поэтому прокси в пути не должен буферизировать ответы.

* **Аутентификация на прокси**: если ваш прокси также требует заголовок `Proxy-Authorization`, runner может добавлять его к каждому соединению, которое он открывает к прокси; см. раздел [Аутентификация на прокси для исходящего трафика](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#authenticate-to-an-egress-proxy).
* **Долгоживущие ответы**: если runner берёт сессию в работу, но Claude так и не отвечает на её первое сообщение, причиной может быть ваш прокси. См. раздел [Сессия взята в работу, но Claude так и не отвечает на её первое сообщение](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md#when-a-sessions-first-message-is-never-answered).

## Что остается на вашей инфраструктуре

Рабочие копии репозиториев, артефакты сборки, секреты и любые файлы, которые сессия создает или изменяет, остаются на машинах, которые вы предоставляете. Сам диалог, включая промпты, ответы и результаты инструментов, передается на `api.anthropic.com`, и Anthropic хранит транскрипт сессии, чтобы вы могли возобновить сессию из другого [поддерживаемого интерфейса](#availability-and-limitations). Когда раннер [отправляет запросы к модели в Amazon Bedrock или Google Cloud's Agent Platform](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md#send-model-requests-to-bedrock-or-agent-platform), диалог по-прежнему передается на `api.anthropic.com` в потоке событий сессии.

Самостоятельно размещаемое окружение перемещает выполнение сеанса в вашу сеть. Плоскость управления остается размещаемой Anthropic: оркестрация сеанса, очередь и интерфейс claude.ai продолжают работать на инфраструктуре Anthropic.

## Начало работы

Страницы самостоятельно размещаемых окружений организованы по тому, что вы делаете:

* [Quickstart](https://code.claude.com/docs/ru/self-hosted-environments-quickstart.md): установите Claude Code, создайте окружение, запустите runner и маршрутизируйте свой первый сеанс
* [Deploy to production](https://code.claude.com/docs/ru/self-hosted-environments-deploy.md): усиление безопасности, сетевой выход, учетные данные git, рецепты Kubernetes и Compose, известные проблемы и устранение неполадок
* [Customize sessions](https://code.claude.com/docs/ru/self-hosted-environments-configuration.md): скрипты-обертки для учетных данных для каждого сеанса, hooks жизненного цикла, runners по требованию, MCP servers и разрешения
* [Test end to end](https://code.claude.com/docs/ru/self-hosted-environments-testing.md): дымовой тест CI, который проверяет образ runner перед его продвижением
* [Reference](https://code.claude.com/docs/ru/self-hosted-environments-reference.md): каждый флаг CLI, переменная окружения, метрика и конечная точка здоровья
* [Verify session identity](https://code.claude.com/docs/ru/self-hosted-environments-identity.md): проверьте токен сеанса из ваших собственных сервисов перед предоставлением доступа
