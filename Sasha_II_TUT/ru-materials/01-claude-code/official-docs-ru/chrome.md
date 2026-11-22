> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Использование Claude Code с Chrome

> Подключите Claude Code к браузеру Chrome для тестирования веб-приложений, отладки с помощью логов консоли, автоматизации заполнения форм и извлечения данных со страниц.

Claude Code интегрируется с [расширением Claude in Chrome для браузера](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn), чтобы предоставить вам возможности автоматизации браузера из CLI или [расширения VS Code](https://code.claude.com/docs/ru/vs-code.md#automate-browser-tasks-with-chrome). Создавайте свой код, а затем тестируйте и отлаживайте его в браузере без переключения контекста.

Claude открывает новые вкладки для задач браузера и использует состояние входа вашего браузера, поэтому он может получить доступ к любому сайту, на который вы уже вошли. Действия браузера выполняются в видимом окне Chrome в реальном времени. Когда Claude встречает страницу входа или CAPTCHA, он приостанавливается и просит вас обработать это вручную.

Расширение собирает вкладки, которые открывает Claude, в группу вкладок Chrome, привязанную к вашей сессии. В локальных сессиях то, закроет ли Claude Code эту группу при завершении сессии, зависит от способа её завершения:

* Когда вы вводите `/clear`, Claude Code закрывает группу вместе с открытыми страницами, если только не продолжает выполняться работа, которая сохраняется после очистки
* Когда вы переключаете сессии с помощью такой команды, как `/resume`, выходите из Claude Code или выполняете `/clear`, пока продолжает выполняться работа, которая сохраняется после очистки, Claude Code закрывает группу только в том случае, если в ней нет ничего, кроме пустых новых вкладок, поэтому страницы, которые вы, возможно, ещё читаете, остаются открытыми

> [!NOTE]
>
> Интеграция с Chrome работает с Google Chrome и Microsoft Edge. Claude Code также обнаруживает расширение и настраивает подключение в других браузерах на основе Chromium, включая Brave, Arc, Vivaldi и Opera. Интеграция с Chrome не поддерживается в Windows Subsystem for Linux (WSL).

## Возможности

С подключенным Chrome вы можете объединять действия браузера с задачами кодирования в единый рабочий процесс:

* **Живая отладка**: читайте ошибки консоли и состояние DOM напрямую, а затем исправьте код, который их вызвал
* **Проверка дизайна**: создайте пользовательский интерфейс на основе макета Figma, а затем откройте его в браузере, чтобы проверить соответствие
* **Тестирование веб-приложений**: тестируйте валидацию форм, проверяйте визуальные регрессии или проверяйте потоки пользователей
* **Аутентифицированные веб-приложения**: взаимодействуйте с Google Docs, Gmail, Notion или любым приложением, в которое вы вошли, без коннекторов API
* **Извлечение данных**: извлекайте структурированную информацию со страниц и сохраняйте её локально
* **Автоматизация задач**: автоматизируйте повторяющиеся задачи браузера, такие как ввод данных, заполнение форм или многосайтовые рабочие процессы
* **Загрузка файлов**: прикрепляйте файлы с вашего компьютера к полям загрузки на веб-страницах
* **Запись сессии**: записывайте взаимодействия браузера в виде GIF-файлов для документирования или обмена информацией о том, что произошло

## Предварительные требования

Перед использованием Claude Code с Chrome вам необходимо:

* [Google Chrome](https://www.google.com/chrome/), [Microsoft Edge](https://www.microsoft.com/edge) или другой браузер на основе Chromium, например Brave, Arc, Vivaldi или Opera
* Расширение [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) версии 1.0.36 или выше, доступное в Chrome Web Store
* [Claude Code](https://code.claude.com/docs/ru/quickstart.md#step-1-install-claude-code)
* Прямой план Anthropic (Pro, Max, Ultra, Team или Enterprise)

Для интеграции с Chrome также требуется вход с помощью `/login`. Если вы проходите аутентификацию с помощью API-ключа или долгоживущего токена из [`claude setup-token`](https://code.claude.com/docs/ru/authentication#generate-a-long-lived-token), Claude Code оставляет интеграцию с Chrome выключенной, даже если вы передаёте `--chrome`. Расширение браузера не может пройти аутентификацию с этими учётными данными.

> [!NOTE]
>
> Интеграция с Chrome недоступна через сторонних поставщиков, таких как Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry. Если вы получаете доступ к Claude исключительно через стороннего поставщика, вам нужна отдельная учётная запись claude.ai для использования этой функции.

### Доступность Chrome при HIPAA или нулевом хранении данных

В организациях Enterprise, где включён HIPAA, Claude in Chrome по умолчанию отключён, и [Owner](https://code.claude.com/docs/ru/server-managed-settings.md#access-control) может включить его в [**Organization settings > Claude in Chrome**](https://claude.ai/admin-settings/browser-extension). Ваше соглашение с деловым партнёром (Business Associate Agreement, BAA) с Anthropic не распространяется на данные, отправляемые на сторонние сайты через Claude in Chrome. Список соответствующих требованиям сервисов (Eligible Services) см. в [руководстве по внедрению](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide).

Если в вашей организации для Claude Code включено [нулевое хранение данных (Zero Data Retention, ZDR)](https://code.claude.com/docs/ru/zero-data-retention.md), Claude in Chrome недоступен в Claude Code. Он остаётся выключенным, даже если Owner включил его в **Organization settings > Claude in Chrome** или вы передаёте `--chrome`. `/chrome` сообщает `Claude in Chrome is disabled by your organization's policy`. Вы по-прежнему можете использовать расширение вне Claude Code там, где это разрешает ваша организация.

## Начало работы в CLI

**1. Запустите Claude Code с Chrome**

Запустите Claude Code с флагом `--chrome`:

```bash theme={null}
claude --chrome
```

При первом запуске с Chrome Claude Code показывает одноразовое диалоговое окно, которое знакомит с интеграцией и объясняет, как работают разрешения для сайтов. Нажмите Enter, чтобы продолжить.

Чтобы включить Chrome для будущих сессий без флага, см. раздел [Включение Chrome по умолчанию](#enable-chrome-by-default).

**2. Попросите Claude использовать браузер**

В этом примере Claude переходит на страницу, взаимодействует с ней и сообщает о том, что обнаружил, — всё это прямо из вашего терминала или редактора:

```text wrap theme={null}
Go to code.claude.com/docs, click on the search box,
type "hooks", and tell me what results appear
```

Если Claude Code запрашивает разрешение перед действием в браузере, подтвердите его. Диалоговое окно начинается с `Claude in Chrome wants to` и предлагает вариант разрешить все действия на этом сайте на время сессии. Claude открывает новую вкладку и приступает к задаче.

Выполните `/chrome` в любой момент, чтобы проверить статус подключения, управлять разрешениями, переподключить расширение или выбрать, какой из подключённых браузеров использовать. Интеграция работает, если на панели статуса отображаются `Status: Enabled` и `Extension: Installed`.

Если подключено несколько браузеров, вы выбираете, какой из них использует Claude. Если действие в браузере начинается до того, как вы сделали выбор, Claude предложит выбрать браузер. Чтобы позже переключить браузер, выполните `/chrome` и выберите **Select browser…**. Claude продолжает использовать выбранный вами браузер, даже когда подключается другой.

Для VS Code см. раздел [автоматизация браузера в VS Code](https://code.claude.com/docs/ru/vs-code.md#automate-browser-tasks-with-chrome).

### Установка расширения по запросу Claude

Когда Claude нужен ваш браузер в интерактивной сессии, а Claude Code не обнаруживает расширение, Claude Code показывает запрос на установку с заголовком «Claude wants to use your browser». Claude Code задаёт этот вопрос не более одного раза за сессию.

Запрос предлагает три варианта:

* **Install extension**: открывает страницу установки расширения в браузере и запускает пошаговую настройку. Claude Code ожидает завершения установки, подключает расширение и включает инструменты браузера в той же сессии. Когда подключение готово, выберите «Continue with browser tools», и Claude продолжит задачу в вашем браузере. Вы можете выйти из настройки, выбрав «Continue without browser tools», и завершить её позже с помощью `/chrome`.
* **Not now**: продолжает задачу без инструментов браузера. Claude Code может спросить снова в одной из следующих сессий.
* **Don't ask again**: отключает запрос в будущих сессиях. Вы по-прежнему можете настроить интеграцию в любое время с помощью `/chrome`.

Две управляемые политики MCP отключают этот запрос:

* Если ваша организация блокирует MCP-сервер `claude-in-chrome` с помощью [управляемой настройки `deniedMcpServers`](https://code.claude.com/docs/ru/managed-mcp#policy-based-control-with-allowlists-and-denylists), Claude Code не показывает запрос на установку.
* Если ваша организация развёртывает файл [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp#exclusive-control-with-managed-mcp-json), не [разрешив Claude in Chrome наряду с управляемым набором](https://code.claude.com/docs/ru/managed-mcp.md#allow-claude-in-chrome-alongside-the-managed-set), Claude Code не показывает запрос на установку.

### Включение Chrome по умолчанию

Чтобы подключать Chrome, не передавая `--chrome` каждый раз, выполните `/chrome` в сессии CLI и выберите пункт включения по умолчанию. В [расширении VS Code](https://code.claude.com/docs/ru/vs-code.md#automate-browser-tasks-with-chrome) введите `/chrome` в поле промпта и включите переключатель включения по умолчанию. Они используют одну общую настройку, поэтому её включение в любом из мест включает её как для CLI, так и для VS Code.

Если настройка включена и используется Claude Code версии 2.1.287 или новее, каждая сессия VS Code подключается к вашему браузеру при запуске, поэтому Claude может использовать его ещё до того, как вы введёте `@browser`. В более ранних версиях или при отключённой настройке сессия VS Code подключается, когда вы вводите `@browser`.

Claude Code запускается в обычном режиме, если Chrome не запущен.

> [!NOTE]
>
> Включение Chrome по умолчанию увеличивает использование контекста, поскольку инструменты браузера и инструкции к ним загружаются всегда. Если вы заметили возросшее потребление контекста, отключите настройку и подключайтесь только при необходимости — с помощью `--chrome` в CLI или введя [`@browser`](https://code.claude.com/docs/ru/vs-code#automate-browser-tasks-with-chrome) в поле промпта VS Code.

### Ответ на диалоговое окно при запуске

Если при запуске `claude` появляется диалоговое окно «Claude in Chrome extension detected», ваш ответ изменяет [настройку включения по умолчанию](#enable-chrome-by-default):

* **Yes, use my browser**: включает настройку и подключает эту сессию
* **No, keep browser tools off** или Esc: отключает настройку, и Claude Code перестаёт предлагать настроить Chrome

Чтобы изменить свой ответ для последующих сессий, выполните `/chrome`.

### Управление разрешениями для сайтов

Разрешения на уровне сайтов наследуются от расширения Chrome. Управляйте разрешениями в настройках расширения Chrome, чтобы контролировать, на каких сайтах Claude может просматривать страницы, нажимать и вводить текст. В [авторежиме](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), когда классификатор авторежима сам одобряет обращение браузера к сайту, расширение пропускает собственную проверку для этого сайта при данном обращении, если только ваши правила разрешений не запрещают Claude in Chrome доступ к какому-либо сайту.

### Запросы разрешений в сессиях VS Code

В сессии VS Code, когда Claude Code запрашивает подтверждение перед действием в браузере, запрос появляется в виде карточки на панели чата. Если действие направлено на сайт, который вы не разрешили, карточка также предлагает разрешить этот сайт.

В сессии, которая подключилась к вашему браузеру при запуске, потому что включена [настройка включения по умолчанию](#enable-chrome-by-default), Claude Code запрашивает подтверждение перед действиями в браузере на сайте, который вы не разрешили, в режимах Manual, Edit automatically, Auto и Bypass permissions. В режимах Auto и Bypass permissions это действует, пока вы не введёте `@browser` в этой сессии.

### Инструменты браузера в режиме планирования

В [режиме планирования](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode) запрос разрешения появляется перед тем, как Claude записывает GIF или открывает новую вкладку. В интерактивной сессии CLI, если [режим bypass permissions доступен](https://code.claude.com/docs/ru/permission-modes.md#skip-all-checks-with-bypasspermissions-mode) и [получение feature-флагов](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching) отключено, эти вызовы выполняются без запроса.

Вызов `tabs_context_mcp` также требует подтверждения, если он задаёт `createIfEmpty`, как и вызов `browser_batch`, включающий любое из этих действий.

## Примеры рабочих процессов

Эти примеры показывают распространённые способы объединения действий браузера с задачами кодирования. Выполните `/mcp`, выберите `claude-in-chrome`, затем выберите **View tools**, чтобы увидеть полный список доступных инструментов браузера.

### Тестирование локального веб-приложения

При разработке веб-приложения попросите Claude проверить, что ваши изменения работают правильно:

```text wrap theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude переходит на ваш локальный сервер, взаимодействует с формой и сообщает, что он наблюдает.

### Отладка с помощью логов консоли

Claude может читать вывод консоли, чтобы помочь диагностировать проблемы. Скажите Claude, какие шаблоны искать, а не просите весь вывод консоли, так как логи могут быть многословными:

```text wrap theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude читает сообщения консоли и может фильтровать по определённым шаблонам или типам ошибок.

### Автоматизация заполнения форм

Ускорьте повторяющиеся задачи ввода данных:

```text wrap theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude читает ваш локальный файл, переходит по веб-интерфейсу и вводит данные для каждой записи.

### Загрузка файлов на веб-страницы

Claude может прикреплять файлы с вашего компьютера к полям загрузки на странице. Claude Code читает файл и отправляет его содержимое в браузер, поэтому загрузка работает как в локальных, так и в удалённых сессиях.

В этом примере к форме прикрепляется файл лога:

```text wrap theme={null}
Open the bug tracker at bugs.example.com, create a new issue,
and attach logs/session.log to it
```

Если Claude отказывается прикрепить файл или загрузка завершается неудачей, проверьте следующие причины:

* **Разрешения**: Claude может загрузить файл, только если сессии разрешено его читать, поэтому [правила разрешений](https://code.claude.com/docs/ru/settings-reference.md#permission-settings), запрещающие доступ `Read` к файлу, также блокируют его загрузку.
* **Размер**: одна загрузка может включать до 10 МБ файлов в сумме.
* **Жёсткие ссылки**: Claude отказывается загружать файлы с несколькими жёсткими ссылками, что часто встречается в хранилищах менеджеров пакетов, таких как `node_modules`. Скопируйте файл и загрузите копию.
* **Имена, связанные с учётными данными**: Claude отказывается загружать файл, если его имя или папка относятся к тем, в которых хранятся учётные данные, например `.env`, файл `.pem` или `.key`, либо что-либо внутри `.ssh`. Требуется Claude Code v2.1.293 или новее.

### Создание контента в Google Docs

Используйте Claude для прямого написания в ваших документах без настройки API:

```text wrap theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude открывает документ, нажимает в редактор и вводит контент. Это работает с любым веб-приложением, в которое вы вошли: Gmail, Notion, Sheets и многое другое.

### Извлечение данных со страниц

Извлекайте структурированную информацию с веб-сайтов:

```text wrap theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude переходит на страницу, читает контент и компилирует данные в структурированный формат.

### Запуск многосайтовых рабочих процессов

Координируйте задачи на нескольких веб-сайтах:

```text wrap theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude работает на разных вкладках, чтобы собрать информацию и завершить рабочий процесс.

### Запись демо-GIF

Создавайте общедоступные записи взаимодействий браузера:

```text wrap theme={null}
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude записывает последовательность взаимодействий и сохраняет её как GIF-файл. Запись захватывает всё, что видно в браузере, включая данные учётной записи на страницах, где выполнен вход, поэтому просмотрите её, прежде чем делиться ею за пределами вашей команды.

### Сохранение скриншотов на диск

Попросите Claude сохранить скриншот в виде файла:

```text wrap theme={null}
Take a screenshot of the checkout page and save it to disk
```

Claude сохраняет изображение на диск и сообщает путь к файлу.

## Устранение неполадок

### Расширение не обнаружено

Если Claude Code не может обнаружить расширение Chrome:

1. Убедитесь, что расширение Chrome установлено и включено в `chrome://extensions`
2. Убедитесь, что Claude Code обновлён, выполнив `claude --version`
3. Проверьте, что Chrome запущен
4. Выполните `/chrome` и выберите "Reconnect extension", чтобы переустановить соединение
5. Если проблема сохраняется, перезагрузите Claude Code и Chrome

При первом включении интеграции с Chrome, Claude Code устанавливает файл конфигурации хоста собственного обмена сообщениями. Chrome читает этот файл при запуске, поэтому если расширение не обнаружено при первой попытке, перезагрузите Chrome, чтобы подобрать новую конфигурацию.

Claude Code открывает вкладку браузера с предложением подключить расширение только при этой первой установке. Claude Code не открывает её повторно, когда последующая сессия перезаписывает файл конфигурации, например после переключения сборок или каталогов конфигурации.

Если соединение по-прежнему не удаётся, убедитесь, что файл конфигурации хоста существует в:

Для Chrome:

* **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: проверьте `HKCU\Software\Google\Chrome\NativeMessagingHosts\` в реестре Windows

Для Edge:

* **macOS**: `~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: проверьте `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\` в реестре Windows

Другие браузеры на основе Chromium читают тот же файл из собственного каталога конфигурации, названного по имени браузера. Например, Brave в macOS использует `~/Library/Application Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/`, а в Windows у каждого браузера есть собственный раздел реестра, например `HKCU\Software\BraveSoftware\Brave-Browser\NativeMessagingHosts\`.

### Настройки проекта не могут включить Chrome

Это предупреждение в терминале означает, что проект, в котором вы работаете, попытался включить интеграцию с Chrome, но Claude Code этого не разрешил:

```text wrap theme={null}
Claude Code ignored CLAUDE_CODE_ENABLE_CFC in this project's settings: a project can't turn on Claude in Chrome. To turn it on yourself, run /chrome or start with --chrome.
```

Файл `.claude/settings.json` или `.claude/settings.local.json` проекта задаёт для [`CLAUDE_CODE_ENABLE_CFC`](https://code.claude.com/docs/ru/env-vars#variables) значение `1` в блоке `env`, чтобы включить интеграцию с Chrome. Claude Code не применил эту настройку, поэтому интеграция с Chrome в этой сессии отключена, и у Claude нет инструментов браузера.

Claude Code пропускает эту настройку, потому что эти файлы хранятся в каталоге проекта, а репозиторий, который вы извлекаете, не должен иметь возможности подключить Claude к вашему браузеру.

Вы можете продолжать работу как есть. Если вам нужны инструменты браузера или вы хотите убрать предупреждение, сделайте одно из следующего:

* **Чтобы получить инструменты браузера сейчас**: выйдите и запустите Claude Code заново с помощью `claude --chrome` в оболочке.
* **Чтобы получить инструменты браузера в последующих сессиях**: выполните `/chrome` в промпте Claude Code и выберите [**Enabled by default**](#enable-chrome-by-default). Это применяется к сессиям, которые вы запустите после этого, а не к текущей.
* **Чтобы убрать предупреждение без инструментов браузера**: удалите строку `CLAUDE_CODE_ENABLE_CFC` из файла настроек проекта.

### Браузер не отвечает

Если команды браузера Claude перестают работать:

1. Проверьте, не блокирует ли модальное диалоговое окно (alert, confirm, prompt) страницу. Диалоговые окна JavaScript блокируют события браузера и препятствуют получению команд Claude. Закройте диалоговое окно вручную, а затем скажите Claude продолжить.
2. Попросите Claude создать новую вкладку и повторить попытку
3. Перезагрузите расширение Chrome, отключив и повторно включив его в `chrome://extensions`

### Разрыв соединения во время длительных сессий

Service worker расширения Chrome может перейти в режим ожидания во время продолжительных сессий, что нарушает соединение. Если инструменты браузера перестают работать после периода неактивности, выполните `/chrome` и выберите "Reconnect extension".

При выполнении `/chrome` проверьте строку `Status`. Если в ней указано "Not connected", собственное соединение текущей сессии с Chrome не удалось. Выберите "Reconnect extension", чтобы перезапустить это соединение. После успешного подключения в Chrome откроется страница переподключения расширения. До версии v2.1.290 пункт "Reconnect extension" только открывал эту страницу и не перезапускал неудавшееся соединение, поэтому если в более ранней версии инструменты браузера не возвращаются, обновите Claude Code.

### Расширение авторизовано в другой организации

Если вы состоите более чем в одной организации claude.ai, в расширении должен быть выполнен вход в ту же организацию, что и в Claude Code. Если они различаются, инструменты браузера Claude возвращают "Browser extension is not connected", даже если оба используют одну и ту же учётную запись claude.ai.

Чтобы узнать, в какую организацию выполнен вход в Claude Code, выполните [`/status`](https://code.claude.com/docs/ru/commands) в промпте Claude Code и посмотрите строку `Organization`.

> [!WARNING]
>
> Если вы выйдете из расширения, вы потеряете сохранённые в нём ярлыки и запланированные задачи. Сначала попробуйте другие способы решения из раздела [Распространённые сообщения об ошибках](#common-error-messages).

Чтобы сменить организацию расширения, выйдите из учётной записи в настройках расширения, затем войдите снова и выберите организацию, которую показывает `/status`.

### Проблемы, специфичные для Windows

На Windows вы можете столкнуться с:

* **Конфликты именованных каналов (EADDRINUSE)**: если другой процесс использует тот же именованный канал, перезагрузите Claude Code. Закройте все остальные сессии Claude Code, которые могут использовать Chrome.
* **Ошибки хоста собственного обмена сообщениями**: если хост собственного обмена сообщениями падает при запуске, попробуйте переустановить Claude Code, чтобы восстановить конфигурацию хоста.
* **Страницы настройки не открываются**: обновите Claude Code. До версии v2.1.211 вкладка браузера с предложением подключить расширение могла не открываться в Windows.

### Распространённые сообщения об ошибках

Это наиболее часто встречающиеся ошибки и способы их решения:

| Ошибка | Причина | Решение |
| - | - | - |
| "Browser extension is not connected" | Расширение не установлено или не запущено в Chrome, в расширении выполнен вход в другую учётную запись или организацию claude.ai, чем в Claude Code, или список разрешённых IP-адресов вашей организации отклоняет подключение к `bridge.claudeusercontent.com` | Убедитесь, что в расширении выполнен вход в ту же учётную запись claude.ai и ту же [организацию](#extension-signed-in-to-a-different-organization), что и в Claude Code, перезагрузите Chrome и Claude Code, затем выполните `/chrome` для переподключения. Если ваша организация использует список разрешённых IP-адресов и ошибка сохраняется, см. [Списки разрешённых IP-адресов организации и исходящий трафик через прокси](https://code.claude.com/docs/ru/network-config.md#organization-ip-allowlists-and-proxy-egress) |
| Расширение отображается как "Not detected" в `/chrome` | Расширение Chrome не установлено или отключено | Установите или включите расширение в `chrome://extensions` |
| "No tab available" | Claude попытался действовать до того, как вкладка была готова | Попросите Claude создать новую вкладку и повторить попытку |
| "Receiving end does not exist" | Service worker расширения перешёл в режим ожидания | Выполните `/chrome` и выберите "Reconnect extension" |
| "No browsers are connected" | Chrome не открыт с расширением, в котором выполнен вход в ту же учётную запись и организацию claude.ai, что и в Claude Code, или Claude Code не может подключиться к `bridge.claudeusercontent.com` | Убедитесь, что Chrome открыт и в расширении выполнен вход в ту же учётную запись claude.ai и ту же [организацию](#extension-signed-in-to-a-different-organization), что и в Claude Code. Если это так, проверьте, что ваша сеть позволяет Claude Code подключаться к `bridge.claudeusercontent.com`, указанному в разделе [Требования к сетевому доступу](https://code.claude.com/docs/ru/network-config.md#network-access-requirements) |

## See also

* [Использование компьютера](https://code.claude.com/docs/ru/computer-use.md): управление собственными приложениями macOS, когда задача не может быть выполнена в браузере
* [Использование Claude Code в VS Code](https://code.claude.com/docs/ru/vs-code.md#automate-browser-tasks-with-chrome): автоматизация браузера в расширении VS Code
* [Справочник CLI](https://code.claude.com/docs/ru/cli-reference.md): флаги командной строки, включая `--chrome`
* [Распространённые рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md): дополнительные способы использования Claude Code
* [Данные и конфиденциальность](https://code.claude.com/docs/ru/data-usage.md): как Claude Code обрабатывает ваши данные
* [Начало работы с Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome): полная документация расширения Chrome, включая сочетания клавиш, планирование и разрешения
