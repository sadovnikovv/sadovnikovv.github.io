> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор модов

> Добавляйте панели, команды и правила вызова инструментов в Claude Code с помощью мода. Узнайте, что может делать мод, как его создать или установить, и где работают моды.

Мод — это [плагин](https://code.claude.com/docs/ru/plugins/overview.md), который изменяет внешний вид и поведение Claude Code. Он состоит из обработчиков событий на JavaScript или TypeScript: Claude Code вызывает один из них при возникновении события, например при вызове инструмента, отправке подсказки или отрисовке части интерфейса, и обработчик может наблюдать за событием, изменять его или брать его под контроль. Используйте мод для добавления собственной функции в Claude Code, например панели, которая показывает, насколько заполнен ваш контекст после каждого запроса. Информацию о файлах в моде и полный пример см. в разделе [Как работает мод](#how-a-mod-works).

> [!NOTE]
>
> Существующие [hooks](https://code.claude.com/docs/ru/hooks.md) Claude Code также работают на событиях в виде команды оболочки, HTTP-запроса или подсказки, которые вы настраиваете в файле параметров. Обработчики мода — это функции, которые работают внутри Claude Code. Claude Code вызывает оба типа hooks: на этих страницах «hook» означает обработчик мода, а тип из файла параметров — это «settings hook».

## Что может делать мод

Settings hooks, skills, строки состояния и серверы MCP работают вне Claude Code: каждый из них запускает скрипт или предоставляет Claude текст или инструменты. Мод работает внутри Claude Code, поэтому он может делать то, что они не могут:

* **Нарисовать интерфейс, который вы можете использовать**: панель рядом с транскриптом или полоса над подсказкой с вкладками, кнопками и текстовыми полями. См. [Рисование в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md).
* **Перерисовать собственный интерфейс Claude Code**: заменить или переоформить части, которые рисует сам Claude Code, такие как строка вызова инструмента, спиннер или диалог, в котором Claude задает вопросы. См. [Изменение того, что уже рисует Claude Code](https://code.claude.com/docs/ru/plugins/mods/interface.md#change-what-claude-code-already-draws).
* **Вмешаться в вызов инструмента или запрос**: например, удержать вызов инструмента, пока вы задаете пользователю вопрос, ответить без запуска инструмента или отправить один запрос другой модели. См. [Охрана или изменение вызова инструмента](https://code.claude.com/docs/ru/plugins/mods/events.md#guard-or-change-a-tool-call) и [Следование за ходом](https://code.claude.com/docs/ru/plugins/mods/events.md#follow-a-turn).
* **Запустить собственный код на команде**: `/command`, который запускает вашу функцию сразу же, без хода Claude, даже если Claude работает. См. [Добавление команды или инструмента](https://code.claude.com/docs/ru/plugins/mods/api.md#add-a-command-or-a-tool).
* **Обмен данными между hooks**: hooks мода совместно используют переменные в его файле, поэтому то, что записывает один hook, может показать другой. Например, один hook может считать вызовы инструментов, а другой показывает счетчик рядом со спиннером, или один может читать использование токенов каждого запроса, а другой отображает его на графике в панели. См. [Реакция на события](https://code.claude.com/docs/ru/plugins/mods/events.md).

Моды работают в CLI Claude Code, на вкладке Code приложения Claude Desktop и в расширении VS Code. См. [Где работают моды](#where-mods-run), чтобы понять, как они ведут себя в других местах, например в `claude -p` и облачных сессиях. Если хук настроек, скилл или MCP-сервер уже делает то, что вам нужно, [сравните их](#compare-mods-settings-hooks-skills-and-mcp-servers) перед написанием мода. Для управления модами для организации см. [Управление модами для вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md).

## Получение мода

Чтобы начать работу с модом:

* **Используйте уже имеющийся**: некоторые собственные функции Claude Code являются модами, например `/diff`. См. [Моды, встроенные в Claude Code](#mods-built-into-claude-code).
* **Создайте свой**: опишите, что вам нужно, в сессии Claude Code, и Claude напишет мод. См. [Попросите Claude создать мод](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod). Чтобы узнать, как устроен код мода, [напишите его самостоятельно](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself).
* **Установите готовый**: см. [Установка или обновление мода](#install-or-update-a-mod) или [попробуйте пример мода](#try-a-sample-mod)

### Установка или обновление мода

> [!WARNING]
>
> Мод — это код, который выполняется с вашими разрешениями. Он может читать и записывать ваши файлы, запускать процессы и выполнять сетевые запросы. Устанавливайте моды только от авторов и из маркетплейсов, которым вы доверяете. См. [Как решить, доверять ли моду](#decide-whether-to-trust-a-mod).

Мод устанавливается как плагин из маркетплейса. Укажите имя плагина, `@` и имя маркетплейса. Эти примеры устанавливают плагин с именем `token-chart` из маркетплейса с именем `your-org`:

* В сессии Claude Code выполните `/plugin install token-chart@your-org`.
* В оболочке выполните `claude plugin install token-chart@your-org`.

В разделе [Установка плагинов](https://code.claude.com/docs/ru/plugins/install.md) рассматриваются маркетплейсы, области действия, расширение VS Code и приложение Desktop, а также [поддержание плагинов в актуальном состоянии](https://code.claude.com/docs/ru/plugins/install.md#keep-plugins-updated) — всё это без изменений применимо к плагину, содержащему мод.

Если вы устанавливаете или обновляете мод из оболочки, пока сессия открыта, выполните `/reload-plugins` в этой сессии, чтобы загрузить его. В противном случае он загрузится при следующем запуске Claude Code.

### Попробуйте пример мода

Anthropic публикует примеры модов в [каталоге `claude-code/mods` репозитория `claude-code-playground`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods). Каждый из них — это полноценный плагин, а в его README описано, как он был создан. Репозиторий предоставляет их как есть, без поддержки.

* [`token-weather`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/token-weather): отображает прогноз вашего контекстного окна над промптом
* [`blast-radius`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius): перехватывает рискованную shell-команду, например `rm -rf` или принудительный push, до её выполнения и показывает, что она изменит, с кнопками для продолжения или отмены
* [`replay-theater`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater): добавляет команду `/replay`, которая пошагово показывает правки файлов, внесённые Claude за последний ход

Пример мода выполняется с вашими разрешениями. Чтобы узнать, что он делает, перед его загрузкой, [просмотрите список его хуков и вызовов](#list-what-a-mod-does-before-you-install-one).

Чтобы попробовать мод, клонируйте репозиторий и [загрузите каталог мода на одну сессию](https://code.claude.com/docs/ru/plugins/create.md#load-a-directory-or-archive-for-one-session) с помощью `--plugin-dir`. Чтобы убедиться, что мод загрузился, [проверьте, какие моды загрузила сессия](#see-which-mods-a-session-loaded).

Чтобы сохранить мод, [добавьте каталог `claude-code/mods` вашего клона в качестве маркетплейса](https://code.claude.com/docs/ru/plugins/install#add-a-marketplace), а затем установите мод из `claude-code-playground-mods`. Маркетплейс указывает на ваш клон, поэтому мод перестанет загружаться, если вы переместите или удалите клон.

## Решите, доверять ли моду

Мод — это код, который работает с вашими разрешениями внутри Claude Code. Устанавливайте моды только от авторов и [маркетплейсов, которым вы доверяете](https://code.claude.com/docs/ru/plugins/security.md).

### Что может достичь мод

Мод работает с вашими разрешениями, поэтому перед установкой знайте, к чему у него есть доступ. После загрузки мод может:

* **Действовать на вашей машине от вашего имени**: читать и писать файлы в любом месте, где может ваша учетная запись пользователя, запускать программы и делать сетевые запросы
* **Читать ваши секреты**: переменные окружения и файлы настроек, включая API-ключ, который вы храните в любом из них
* **Видеть вашу сессию**: каждый промпт, который вы отправляете, и каждый вызов инструмента, который делает Claude
* **Изменять вашу сессию**: переписывать промпт или вызов инструмента, отправлять промпт так, как если бы вы его набрали, или отправлять сообщение в другую из ваших сессий
* **Действовать без вашего разрешения**: одобрить вызов инструмента перед тем, как вас спросят
* **Потратить вашу квоту**: вызвать модель в рамках вашего плана или с вашим API-ключом

Моды не изолируются в песочнице. Если вы включите [изоляцию в песочнице](https://code.claude.com/docs/ru/sandboxing.md), песочница изолирует команды Bash, которые запускает Claude, а процесс, запущенный модом, работает вне её.

Мод может подтвердить [многие вызовы инструментов](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods), которые остановили бы ваши правила `deny` или `ask` или ваши хуки `PreToolUse`, если этому не препятствует [встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default). Когда встроенный страж загружен, по умолчанию пользовательский мод не может этого сделать. В локальной сессии терминала наличие `cc-plugin-sec-default` на вкладке **Installed** в `/plugin` означает, что страж загружен.

Мод может переоформить большую часть интерфейса Claude Code, но не запрос разрешения. Он не может изменить то, что вам показывает запрос.

### Перечислите, что делает мод перед установкой

Перед установкой мода вы можете перечислить, какие события он обрабатывает и что он просит Claude Code делать, например читать файл или делать сетевой запрос, без его запуска. Сначала получите файлы плагина, например клонировав его репозиторий. Затем в вашей оболочке запустите `claude plugin validate` в каталоге плагина:

```bash theme={null}
claude plugin validate ./some-mod
```

Строки `hooks:` и `calls:` в выводе перечисляют события, которые обрабатывает мод, и что он просит Claude Code делать. [Просмотр того, что может делать мод](https://code.claude.com/docs/ru/plugins/mods/admin.md#review-what-a-mod-can-do) показывает вывод и какие вызовы искать.

## Включение или отключение модов

Моды включены по умолчанию. В терминале используйте Claude Code v2.1.287 или позже. Приложение Desktop включает собственную копию Claude Code, и моды работают в нём начиная с v2.1.286. Проверьте версию там, где вы используете моды:

* **Терминал**: в вашей оболочке запустите `claude --version`. Если ваша версия старше, [обновите Claude Code](https://code.claude.com/docs/ru/setup.md#update-claude-code).
* **Приложение Desktop**: в локальной сессии на вкладке Code введите `/status` и посмотрите строку **Claude Code**, в которой показана версия, например `2.1.286`. Если ваша версия старше, [обновите приложение Desktop](https://code.claude.com/docs/ru/desktop.md#claude-code-version-in-the-code-tab).

Чтобы отключить моды, выберите, сколько их остановить и на как долго. Чтобы включить их обратно, отмените то же изменение:

* **Один мод**: отключите или удалите его плагин со [вкладки **Installed** в `/plugin`](https://code.claude.com/docs/ru/plugins/install#manage-installed-plugins)
* **Каждый установленный мод, для одной сессии**: запустите Claude Code с [`--safe-mode`](https://code.claude.com/docs/ru/cli-reference#cli-flags), что также отключает ваши другие настройки
* **Каждый мод, который вы установили, в каждой сессии**: задайте [`"disableAllHooks": true`](https://code.claude.com/docs/ru/settings-reference#disableallhooks) в `~/.claude/settings.json`. Ваши хуки из настроек и пользовательская строка состояния также остановятся. То, чем управляет ваша организация, продолжает работать.

Если вы используете Claude Code через организацию, администратор также может ограничить, какие моды загружаются. Администраторы начинают с [Остановка загрузки модов, установленных пользователем](https://code.claude.com/docs/ru/plugins/mods/admin.md#stop-user-installed-mods-from-loading).

`disableAllHooks` и параметр вашей организации `allowManagedModsOnly` останавливают мод, но оставляют остальную часть его плагина на месте: плагин остаётся установленным, а его скиллы, команды, агенты и MCP-серверы загружаются. Другие настройки и флаги действуют шире. В разделах [`disableAllHooks`](https://code.claude.com/docs/ru/settings-reference#disableallhooks) и [Что работает при `allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#what-runs-under-allowmanagedhooksonly) перечислено, как каждый из них влияет на плагин и его хуки из настроек.

Чтобы узнать, могут ли моды загружаться для вас, см. [Проверка, могут ли загружаться моды](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#check-whether-mods-can-load).

> [!NOTE]
>
> Если вы задали `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` во время раннего доступа, удалите эту переменную. Claude Code v2.1.287 и позже игнорирует её, поэтому значение `0` не отключает моды.

### Посмотрите, какие моды загрузила сессия

Чтобы увидеть, какие моды загрузила сессия терминала, запустите `/plugin` в промпте Claude Code. Тусклая строка под вкладками показывает количество и имена, например `1 mod active · first-mod`. Если мод, который вы установили, не указан там, см. [Узнайте, почему мод ничего не делает](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing).

## Как работает мод

Мод — это [плагин](https://code.claude.com/docs/ru/plugins/overview.md), чей код регистрирует обработчики событий, называемые хуками. Claude Code запускает хук при возникновении его события, например когда Claude вызывает инструмент или когда рисуется спиннер. Небольшой мод состоит из трех файлов:

```text theme={null}
first-mod/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── register.js
```

* **`plugin.json`**: [манифест](https://code.claude.com/docs/ru/plugins/manifest-reference.md) плагина
* **`hooks.json`**: [указывает на ваш файл кода](https://code.claude.com/docs/ru/plugins/mods/reference.md#files)
* **`register.js`**: [ваш код](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself), называемый модулем хуков. Он сообщает Claude Code, на каких событиях запускать ваши функции.

Ниже приведён полный файл `register.js`. Он подсчитывает вызовы инструментов, которые делает Claude, и показывает счётчик рядом со спиннером, пока Claude работает, например `Thinking · tool calls: 3…`.

```javascript hooks/register.js theme={null}
// The count, shared by the two hooks below
let calls = 0

// Claude Code calls this once when the mod loads
export function register(on) {
  // Runs each time Claude is about to use a tool
  on('tool.call', async ($, e, next) => {
    calls += 1
    // Ask Claude Code to draw the interface again, so the new count shows
    $.ui.invalidate('ui.render')
    // Let the tool run as usual
    return next(e)
  })

  // Runs each time Claude Code draws the spinner
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    // Keep Claude Code's spinner, with the count added after its word
    return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
  })
}
```

Файл регистрирует два хука, и оба используют переменную `calls` в верхней части:

* **Хук [`tool.call`](https://code.claude.com/docs/ru/plugins/mods/reference#tools)** запускается каждый раз, когда Claude собирается использовать инструмент. Он добавляет единицу к `calls`, просит Claude Code перерисовать интерфейс и позволяет инструменту работать как обычно.
* **Хук [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface)** запускается каждый раз, когда Claude Code рисует спиннер. Он сохраняет собственный спиннер Claude Code и добавляет счетчик после слова.

Эта запись показывает мод в действии. Смотрите на строку спиннера над полем промпта: пока Claude выводит содержимое каталога и читает два файла, в ней отображается `Thinking · tool calls: 1…`, затем `2…`, затем `3…`.

<video autoPlay muted loop playsInline controls src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-overview-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=00a18aa0743b59a700f0275ce226e6d1" aria-label="В сессии Claude Code вводится и отправляется промпт 'list the files here and read the README'. Пока Claude работает, спиннер показывает 'Thinking · tool calls: 1', затем 2, затем 3, пока Claude выводит список файлов и читает два из них." />

### Что хук может делать с событием

Claude Code запускает ваш хук перед тем, как отреагировать на событие, поэтому хук решает, что произойдет дальше. Он может:

* **Наблюдать**: отметить, что происходит, и позволить событию продолжиться без изменений, как делает хук `tool.call` в примере
* **Переписать**: изменить событие перед его продолжением, как делает хук `ui.render`, когда добавляет счетчик к спиннеру
* **Ответить**: обработать событие самостоятельно, чтобы обычное поведение не запускалось, например отказать в выполнении команды

Чтобы делать что-либо вне собственного кода, например рисовать, добавлять команду, вызывать модель, читать файл, запускать процесс или выполнять сетевой запрос, хук вызывает API модов. У хука нет другого способа делать эти вещи, поэтому Claude Code может [перечислить, что делает мод](#list-what-a-mod-does-before-you-install-one), до того как вы его установите.

Код для каждого варианта см. в разделе [Реакция на события](https://code.claude.com/docs/ru/plugins/mods/events.md#how-a-hook-handles-an-event). Что может вызывать хук, см. в разделе [Использование API модов](https://code.claude.com/docs/ru/plugins/mods/api.md).

### Где работают моды

Хуки мода работают в каждом типе сессии, которая загружает плагин, независимо от того, какой провайдер обслуживает модель, включая Amazon Bedrock, Agent Platform от Google Cloud и Microsoft Foundry. С рисованием все ограниченнее: то, что рисует мод, отображается в терминале, приложении Desktop и расширении VS Code. В этой таблице перечислены все места, где вы можете запустить Claude Code:

| Где вы запускаете Claude Code | Хуки работают | То, что рисует мод, отображается |
| :- | :- | :- |
| `claude` в терминале, включая встроенный терминал редактора и плагин JetBrains | Да | Да |
| Вкладка Code приложения Desktop, кроме сессии WSL | Да | Да, кроме элементов, которые [таблица элементов](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements) отмечает как только для терминала |
| [Сессия WSL](https://code.claude.com/docs/ru/desktop-wsl.md) в приложении Desktop | Нет, потому что плагины недоступны в сессиях WSL | Нет |
| Панель чата расширения VS Code | Да | Да, с версией расширения 2.1.299 или новее. Сессии, которая [не получает флаги функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), например сессии в Amazon Bedrock, нужна версия 2.1.304 или новее. Таблицы [точек отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) и [элементов](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements) отмечают, что рисует панель. |
| `claude -p` и [Agent SDK](https://code.claude.com/docs/ru/agent-sdk/overview.md) | Да | Нет |
| [Remote Control](https://code.claude.com/docs/ru/remote-control.md) из claude.ai или мобильного приложения | Да, в сессии на вашей машине | В терминале на вашей машине |
| [Облачная сессия](https://code.claude.com/docs/ru/claude-code-on-the-web.md) | Да, для плагина, который [попадает в облачную сессию](https://code.claude.com/docs/ru/cloud-environments.md#what-carries-over-from-your-setup) | Нет |

Мод, который рисует, может проверить, в каком приложении он работает, и там, где ничего не рисуется, перейти на строку в транскрипте или текстовый ответ команды.

## Управление модами для вашей организации

Администраторы решают, работают ли моды и какие из них, через [управляемые параметры](https://code.claude.com/docs/ru/managed-settings.md). [Управление модами для вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md) охватывает, что происходит по умолчанию, как просмотреть мод и как применить политику с помощью собственного мода.

## Сравнение модов, хуков настроек, скиллов и серверов MCP

Моды, хуки настроек, скиллы и серверы MCP перекрываются. Эта таблица показывает, что это такое и когда выбрать каждый.

| | Мод | Хук настроек | Скилл | Сервер MCP |
| :- | :- | :- | :- | :- |
| Что это | Функции в плагине, которые Claude Code вызывает в своем собственном процессе | Команда оболочки, HTTP-запрос или промпт, который Claude Code запускает при событии жизненного цикла | Файл `SKILL.md` с инструкциями, которые читает Claude | Внешний процесс или сервис, который предоставляет Claude инструменты |
| Что он может изменить | Вызовы инструментов, промпты, команды, ходы и то, что рисует интерфейс | Продолжится ли вызов инструмента или промпт, аргументы и результат вызова инструмента, а также контекст, добавленный для Claude | Что знает и делает Claude | Какие инструменты есть у Claude |
| Может ли он рисовать в интерфейсе | Да | Нет | Нет | Нет |
| Что вы пишете | JavaScript или TypeScript | Скрипт и запись в `settings.json` | Markdown | Сервер на любом языке |
| Выберите его, когда | Вы хотите панель, полосу над промптом, пользовательскую команду или переписать событие | Вы хотите заблокировать, разрешить или записать в лог событие с помощью скрипта, который у вас уже есть | Вы постоянно вставляете одни и те же инструкции в чат | Claude нужно обращаться к внешней системе |

Каждый из остальных имеет свою собственную страницу: [Хуки](https://code.claude.com/docs/ru/hooks.md), [Скиллы](https://code.claude.com/docs/ru/skills.md) и [MCP](https://code.claude.com/docs/ru/mcp.md). Плагин может содержать их все, поэтому мод может поставляться в одном плагине со скиллом и сервером MCP.

## Моды, встроенные в Claude Code

Некоторые собственные функции Claude Code — это моды. Чтобы увидеть те, которые есть в вашей сессии, запустите `/plugin` в промпте Claude Code и перейдите на вкладку **Installed**, где они перечислены в разделе **Built-in**. Вы не можете обновлять или удалять встроенный мод. Строка [`mods active`](#see-which-mods-a-session-loaded) не включает встроенные моды.

В этой таблице перечислены некоторые записи **Built-in** по имени, которое показывает `/plugin`:

| Имя в `/plugin` | Что он делает | Где он включен | Как его отключить |
| :- | :- | :- | :- |
| `cc-plugin-agents-md` | Загружает `AGENTS.md` как инструкции проекта | Каждая сессия, кроме [тех, которые не могут читать `AGENTS.md`](https://code.claude.com/docs/ru/memory#when-agents-md-support-is-unavailable) | Отключите его в `/plugin` или [выберите, какие файлы инструкций загружаются](https://code.claude.com/docs/ru/memory.md#choose-which-instruction-files-load) |
| `cc-plugin-diff` | Берет на себя [`/diff`](https://code.claude.com/docs/ru/interactive-mode#review-changes-with-%2Fdiff) и отрисовывает его панель | Интерактивные сессии в терминале | Отключите его в `/plugin`. `/diff` останется, и на него будет отвечать встроенная версия команды Claude Code. |
| `cc-plugin-plugin-authoring` | Дает Claude [скилл `plugin-authoring`](https://code.claude.com/docs/ru/plugins/mods/create#ask-claude-for-a-mod) для написания модов. Он содержит скилл и не содержит кода мода. | Если Anthropic не отключила установленные моды удаленно | Отключите его в `/plugin` |
| `cc-plugin-sec-default` | Защищает то, чем управляет ваша организация, от модов, которые устанавливает пользователь | [Где загружается защита](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default) | Никак. Администратор [задает порядок](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods) в управляемых настройках |
| `cc-plugin-telemetry` | Отправляет записи аналитики, которые записывают в лог Claude Code и его встроенные моды | Везде, где включена собственная аналитика Claude Code | Отключите его в `/plugin` или отключите аналитику, например с помощью [`DISABLE_TELEMETRY`](https://code.claude.com/docs/ru/env-vars) |
| `cc-plugin-you-should-know` | [You should know](https://code.claude.com/docs/ru/interactive-mode.md#you-should-know-suggestions): вспомогательный агент показывает заметку над промптом, когда находит что-то, что вы могли упустить | Отключено, пока вы [не включите его](https://code.claude.com/docs/ru/interactive-mode.md#you-should-know-suggestions) | Отключите его в `/plugin` |

Для плагина **Built-in**, которого нет в таблице, [откройте его сведения в `/plugin`](https://code.claude.com/docs/ru/plugins/install#manage-installed-plugins), чтобы прочитать, что он делает, или отключить его.

Настройки и флаги, которые останавливают установленные моды, такие как `disableAllHooks`, `--bare` и `--safe-mode`, не останавливают встроенные моды.

### Прочитайте исходный код встроенных модов

Исходный код некоторых из этих модов общедоступен в [каталоге `mods` репозитория Claude Code](https://github.com/anthropics/claude-code/tree/main/mods). Каждый из них — это полноценный плагин с модулем хуков и тестами:

* [`diff`](https://github.com/anthropics/claude-code/tree/main/mods/diff): панель `/diff` с кнопками, привязанными к действиям клавиатуры, и прокруткой, которую мод обрабатывает сам
* [`agents-md`](https://github.com/anthropics/claude-code/tree/main/mods/agents-md): загружает `AGENTS.md` как инструкции проекта с опцией [`userConfig`](https://code.claude.com/docs/ru/plugins/components#user-configuration)
* [`sec-default`](https://github.com/anthropics/claude-code/tree/main/mods/sec-default): защита, описанная в разделе [Знайте, что происходит по умолчанию](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), образец мода, который применяет политику
* [`telemetry`](https://github.com/anthropics/claude-code/tree/main/mods/telemetry): добавляет методы, которые могут вызывать другие моды, и поставляет их типы

## Следующие шаги

* [Создание мода](https://code.claude.com/docs/ru/plugins/mods/create.md): создайте один, который считает вызовы инструментов, показывает счетчик рядом со спиннером и добавляет команду, и узнайте цикл редактирования и перезагрузки
* [Рисование в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md): панели, полоса над промптом, кнопки, текстовые поля и состояние
* [Реакция на события](https://code.claude.com/docs/ru/plugins/mods/events.md): вызовы инструментов, промпты, ходы и порядок, в котором работают моды
* [Использование API модов](https://code.claude.com/docs/ru/plugins/mods/api.md): команды, инструменты, вызовы моделей, таймеры и файлы
* [Тестирование мода](https://code.claude.com/docs/ru/plugins/mods/test.md): автоматизированные тесты, которые работают без сессии
* [Устранение неполадок мода](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md): причины, по которым мод ничего не делает, и лог отладки
* [Управление модами для вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md): значения по умолчанию, управляемые настройки, просмотр мода и моды политики
* [Справочник модов](https://code.claude.com/docs/ru/plugins/mods/reference.md): события, методы, элементы и ограничения
