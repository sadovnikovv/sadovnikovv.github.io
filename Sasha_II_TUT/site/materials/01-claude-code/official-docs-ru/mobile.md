> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на мобильном устройстве

> Запускайте, отслеживайте и управляйте задачами Claude Code со своего телефона с помощью приложения Claude для iOS и Android.

Приложение Claude для [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) и [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) является клиентом для сеансов Claude Code, а не местом, где выполняется код. С вашего телефона вы можете получить доступ к [облачным сеансам](#start-and-monitor-cloud-sessions) и [проектам](https://code.claude.com/docs/ru/claude-projects.md) в облаке, к сеансу, работающему на вашем собственном компьютере через [Remote Control](#continue-a-local-session-with-remote-control), или к приложению Desktop через [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch).

> [!NOTE]
>
> Claude Code не имеет отдельного мобильного приложения: облачные сеансы и Remote Control находятся на вкладке **Code** в приложении Claude, а Dispatch — это задача, которой вы отправляете сообщения в приложении.

## Получить приложение

**1. Загрузите приложение Claude**

Установите приложение Claude для [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) или [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude). На iPad установите то же приложение iOS.

> [!TIP]
>
> Запустите `/mobile` в сеансе Claude Code, чтобы отобразить QR-код для [claude.ai/mobile](https://claude.ai/mobile), который открывает правильный магазин приложений для вашего телефона. `/ios` и `/android` делают то же самое.

**2. Войдите в систему**

Войдите с той же учётной записью claude.ai и организацией, которые вы используете для Claude Code. Облачные сеансы и Remote Control требуют учётную запись claude.ai, поэтому они недоступны с ключом API Anthropic Console или от стороннего поставщика, такого как Amazon Bedrock.

**3. Откройте вкладку Code**

Нажмите **Code** в навигации приложения, чтобы получить доступ к своим сеансам, или откройте [claude.ai/code/new](https://claude.ai/code/new) на своём телефоне, чтобы запустить новый сеанс Code в приложении. Если вы не видите вкладку Code, ваш план или организация могут не включать эти функции; см. [доступность по плану подписки](https://code.claude.com/docs/ru/feature-availability.md#availability-by-subscription-plan).

## Работайте со своего телефона

Из приложения вы можете запускать облачные сеансы, открывать проект, управлять сеансом Claude Code, работающим на вашем компьютере, или отправлять Dispatch задачу. Приложение одинаково для каждого; они отличаются тем, где происходит работа.

| Функция | Что вы подключаете | Когда использовать |
| :- | :- | :- |
| [Cloud sessions](https://code.claude.com/docs/ru/claude-code-on-the-web.md) | Сеанс на облачной инфраструктуре, управляемой Anthropic по умолчанию | Ваш репозиторий находится на GitHub и задача должна продолжаться после того, как вы отложите телефон. См. [краткое руководство веб-версии](https://code.claude.com/docs/ru/web-quickstart.md) для настройки. |
| [Projects](https://code.claude.com/docs/ru/claude-projects.md) | Беседа, в которой Claude координирует параллельные потоки работы и отчитывается | У вас есть поток связанной работы, а не одна задача, и вы хотите увидеть, какие потоки завершены или требуют вас. |
| [Remote Control](https://code.claude.com/docs/ru/remote-control.md) | Сеанс Claude Code, работающий на вашем компьютере | Работе нужна ваша локальная файловая система, инструменты или MCP серверы. |
| [Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch) | Приложение Desktop на вашем компьютере | Вы хотите отправить задачу и позволить Dispatch решить, как её запустить. Требуется план Pro, Max или Ultra. |

Если ваш компьютер будет выключен, используйте облачные сеансы или проект, которые работают в облаке и продолжают работу с закрытым ноутбуком. Remote Control и Dispatch управляют вашей собственной машиной, поэтому она должна оставаться включённой с запущенным Claude Code или приложением Desktop. Если ваша машина перейдёт в режим сна во время сеанса Remote Control, Claude Code переподключится, когда она вернётся в сеть.

Для более полного сравнения см. [работа, когда вы находитесь вдали от терминала](https://code.claude.com/docs/ru/platforms.md#work-when-you-are-away-from-your-terminal).

Облачные сеансы и Remote Control работают на вкладке **Code**. Для Dispatch, которому вы отправляете сообщения как задачу в приложении, см. [сеансы из Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch).

### Запуск и мониторинг облачных сеансов

Облачные сеансы запускают задачи на облачной инфраструктуре, управляемой Anthropic по умолчанию, поэтому сеанс продолжается после того, как вы отложите телефон. На вкладке Code выберите репозиторий и ветку, опишите задачу и отправьте её. Сеансы сохраняются на всех устройствах: задача, которую вы запустили на ноутбуке, готова к проверке со своего телефона, а задача, которую вы запустили со своего телефона, ждёт вас, когда вы вернётесь к своему столу.

Откройте сеанс в приложении, чтобы проверить прогресс, ответить на вопросы Claude или направить его в новом направлении. Вы также можете попросить Claude [следить за pull request](https://code.claude.com/docs/ru/claude-code-on-the-web.md#auto-fix-pull-requests) и исправлять сбои CI или комментарии к проверке по мере их поступления. Чтобы подключить GitHub и настроить свою среду, следуйте [краткому руководству веб-версии](https://code.claude.com/docs/ru/web-quickstart.md), и см. [Use Claude Code in the cloud](https://code.claude.com/docs/ru/claude-code-on-the-web.md) для всего, что могут делать облачные сеансы.

### Продолжите локальный сеанс с Remote Control

Remote Control подключает приложение Claude к сеансу Claude Code, работающему на вашей машине, поэтому выполнение кода и доступ к файловой системе остаются локальными, пока вы управляете сеансом со своего телефона. Запустите сеанс на вашем компьютере с помощью `claude remote-control` или запустите `/remote-control` в уже открытом сеансе. Затем отсканируйте QR-код, который может отобразить терминал, или откройте приложение Claude, нажмите **Code** и выберите сеанс из списка. См. [подключение с другого устройства](https://code.claude.com/docs/ru/remote-control.md#connect-from-another-device) для каждого варианта.

Когда вы добавляете вложение в приложение Claude, оно также достигает локального сеанса:

* **Фотографии**: Claude видит прикреплённые фотографии непосредственно как часть вашего сообщения. Claude Code также сохраняет каждую фотографию в `~/.claude/uploads/` и сообщает Claude путь к сохранённому файлу, поэтому Claude может скопировать изображение в файлы, которые он создаёт.
* **Другие файлы**: Claude Code загружает их на вашу машину и передаёт их Claude как ссылки на файлы `@`.

Требования, режимы вызова и устранение неполадок см. в [обзоре Remote Control](https://code.claude.com/docs/ru/remote-control.md).

### Получайте push-уведомления

Когда Remote Control активен, Claude может отправлять push-уведомления на ваш телефон, когда долгая задача завершается или когда ему нужно решение от вас. Вы также можете попросить об уведомлении в своём промпте, например `notify me when the tests finish`. См. [мобильные push-уведомления](https://code.claude.com/docs/ru/remote-control.md#mobile-push-notifications) для двух переключателей `/config` и устранения неполадок доставки.

Dispatch отправляет своё собственное уведомление, когда сеанс Code, который он создал, завершается или требует вашего одобрения, описано в [сеансах из Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch).

## Ограничения

Мобильный клиент охватывает большую часть того, что нужно сеансу, с несколькими ограничениями:

* **Команды только для локального использования**: команды, которые работают только в интерфейсе терминала, такие как `/plugin` и `/resume`, не работают из приложения. [Ограничения Remote Control](https://code.claude.com/docs/ru/remote-control.md#limitations) перечисляют команды, которые работают с мобильного устройства, и как их поведение отличается.
* **Режимы разрешений**: облачные сессии предлагают Accept edits, Plan и Auto, а сессии Remote Control предлагают Manual, Accept edits, Plan и Auto. Вы не можете выбрать Bypass permissions из приложения ни в одном случае. См. [переключение режимов разрешений](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes), чтобы узнать, когда доступен Auto.
* **Планы Dispatch**: Dispatch требует план Pro, Max или Ultra и недоступен для Team или Enterprise.

## Связанные ресурсы

* [Платформы и интеграции](https://code.claude.com/docs/ru/platforms.md): сравните каждую поверхность, на которой работает Claude Code
* [Claude Code в веб-версии](https://code.claude.com/docs/ru/claude-code-on-the-web.md): как работают облачные сеансы и как перемещать работу на терминал и с терминала
* [Настройка облачных сред](https://code.claude.com/docs/ru/cloud-environments.md): уровни сетевого доступа, переменные окружения и скрипты настройки для облачных сеансов
* [Remote Control](https://code.claude.com/docs/ru/remote-control.md): продолжите локальный сеанс с любого устройства
* [Сеансы из Dispatch](https://code.claude.com/docs/ru/desktop.md#sessions-from-dispatch): как задачи Dispatch становятся сеансами Code в приложении Desktop
* [Channels](https://code.claude.com/docs/ru/channels.md): спросите Claude что-нибудь со своего телефона через Telegram, Discord или iMessage, пока работа выполняется на вашей машине
* [Claude Code в Slack](https://code.claude.com/docs/ru/slack.md): делегируйте задачи кодирования из своего рабочего пространства Slack, упомянув `@Claude`
