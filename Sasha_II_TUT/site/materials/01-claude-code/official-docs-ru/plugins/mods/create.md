> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Создание мода

> Попросите Claude написать мод Claude Code из описания или напишите его сами, чтобы подсчитывать вызовы инструментов и добавить команду. Изучите цикл перезагрузки и валидации.

Мод — это [плагин](https://code.claude.com/docs/ru/plugins/overview.md) Claude Code с файлом входа, называемым модулем хуков: файл JavaScript или TypeScript, функции которого Claude Code вызывает при возникновении событий. Чтобы создать мод:

* **Попросите Claude написать его**: [опишите, что вы хотите](#ask-claude-for-a-mod) в сеансе Claude Code
* **Напишите его сами**: [следуйте руководству](#write-a-mod-yourself), чтобы узнать, как работает код мода. Вам не нужны Node.js, бандлер или этап сборки, потому что Claude Code загружает файлы `.js` и `.ts` напрямую.

Если вы еще не решили, является ли мод правильным инструментом, сначала прочитайте [сравнение на странице обзора](https://code.claude.com/docs/ru/plugins/mods/overview.md#compare-mods-settings-hooks-skills-and-mcp-servers).

> [!NOTE]
>
> Используйте Claude Code v2.1.287 или более позднюю версию. В вашей оболочке выполните `claude --version`, чтобы проверить. Чтобы узнать, могут ли моды загружаться для вас, см. [Проверка возможности загрузки модов](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#check-whether-mods-can-load).

## Попросите Claude написать мод

Опишите нужный вам мод в интерактивном сеансе Claude Code, и Claude напишет его. Claude работает из встроенного [skill](https://code.claude.com/docs/ru/skills.md) с именем `plugin-authoring`, который сообщает ему, где написать мод, какие события и методы есть в вашей версии, и как загружается мод. Claude может загрузить skill, когда вы попросите мод, или вы можете загрузить его сами, выполнив `/plugin-authoring` в приглашении Claude Code.

В [режимах разрешений](https://code.claude.com/docs/ru/permission-modes.md) `auto` и `bypassPermissions` Claude Code [может загрузить мод, не спрашивая вас](#sessions-that-skip-the-approval). Чтобы сначала получить запрос, запустите новую сессию в режиме `default` или `acceptEdits` либо [переключитесь](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes) на любой из этих режимов, прежде чем попросить первый мод в сессии. В [некоторых сессиях](#sessions-that-cant-load) мод не может загрузиться.

**1. Опишите мод**

Попросите мод своими словами, например `make a mod that shows the current git branch above the prompt`. Claude пишет мод в отдельном каталоге в папке модов сеанса, которая находится в `~/.claude/dev-mods/`, за которой следует ID сеанса. Полный путь мода выглядит как `~/.claude/dev-mods/3f2a9c1e-5b7d-4e8a-9c21-6d0f4b8a7e13/git-branch/`.

> [!NOTE]
>
> В [режимах разрешений](https://code.claude.com/docs/ru/permission-modes.md) `default` и `acceptEdits` Claude Code просит вас одобрить каждый из файлов мода перед тем, как Claude его создаст, потому что папка модов — это [защищённый путь](https://code.claude.com/docs/ru/permission-modes.md#protected-paths). Одобрите каждый файл по мере его появления.

**2. Одобрите мод**

Когда Claude сохраняет первый файл, Claude Code спрашивает, следует ли включить горячую перезагрузку для сессии. Горячая перезагрузка запускает моды, написанные Claude в этой сессии, и подхватывает каждое последующее изменение. Вы не увидите этот вопрос в сессии, которая [загружает новые моды, не спрашивая](#sessions-that-skip-the-approval) или [не может их загрузить](#sessions-that-cant-load).

Выберите один из этих ответов:

* **Turn them on**: моды в папке модов сессии загружаются при завершении хода и перезагружаются в конце каждого хода, который их изменяет. Ваш ответ действует для сессии, в том числе после её возобновления.
* **Not now**: пока ничего не загружается. Файлы остаются там, где их написал Claude, и моды загружаются при следующем запуске этой сессии. Чтобы мод никогда не загружался, удалите его каталог.

**3. Проверьте, что мод загрузился**

Выполните `/plugin` в приглашении Claude Code и нажимайте Tab, пока не будет выбрана вкладка **Installed**. Она перечисляет мод, и вы можете отключить его там.

**4. Попробуйте мод**

Используйте то, что вы просили. Для примера промпта текущее имя ветки появляется над полем промпта. Если мод не делает то, что вы хотели, скажите Claude, что изменить. Мод перезагружается в конце каждого хода, который изменяет его файлы, поэтому вы можете попробовать изменение сразу после завершения Claude.

Если строка транскрипта, начинающаяся с имени мода, сообщает, что [изменение не загрузилось](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#this-mods-change-didnt-load), вставьте эту строку в следующее сообщение, когда будете просить Claude исправить проблему. Claude не видит эту строку, если вы её не вставите.

### Используйте мод в других сеансах

Мод, написанный Claude, загружается только в сеансе, который его создал, и Claude Code удаляет папку модов этого сеанса после того, как она старше [`cleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#cleanupperioddays). Чтобы сохранить мод, скопируйте его каталог из папки модов в место по вашему выбору, например `~/mods/git-branch`. Затем выберите, как его загружать:

* **В сеансе, который вы запускаете**: в вашей оболочке выполните `claude --plugin-dir ~/mods/git-branch`
* **Для других людей**: [добавьте его на маркетплейс](#share-your-mod), чтобы они могли его установить

### Сессии, которые загружают мод, не спрашивая

Claude Code может включить горячую перезагрузку, не спрашивая, в режимах `auto` и `bypassPermissions`, и моды загружаются при завершении хода.

Когда вы возобновляете сессию, интерактивно или с `claude -p`, моды, уже находящиеся в её папке модов, [могут загрузиться](#sessions-that-cant-load), не спрашивая. Чтобы мод не загружался при возобновлении, удалите его каталог.

### Сессии, где мод, написанный Claude, не может загрузиться

Мод, написанный Claude, не загружается в следующих случаях, и Claude Code не спрашивает, загружать ли его:

* **Никого нет, чтобы одобрить**: сессия находится в [режиме `dontAsk`](https://code.claude.com/docs/ru/permission-modes), или это запуск `claude -p`, который пишет мод, в режиме `default` или `acceptEdits`, который не может показать вам вопрос о горячей перезагрузке.
* **Интерактивная сессия, где рабочее пространство не доверено**: вы не приняли запрос доверия для каталога
* **Моды отключены**: вы запустили с `--safe-mode` или `--bare`, вы задали `disableAllHooks`, или [управляемые настройки](https://code.claude.com/docs/ru/plugins/mods/admin.md#choose-how-much-to-allow) вашей организации это блокируют

## Напишите мод сами

В этом руководстве вы создаёте мод с именем `first-mod`, который подсчитывает вызовы инструментов, которые делает Claude, показывает счётчик рядом со спиннером во время работы Claude и добавляет команду `/tally`, которая его выводит. Затем вы читаете объявления типов, которые Claude Code пишет рядом с вашим модом, и выполняете `claude plugin validate`. Вместе они показывают вам события и методы, которые предлагает ваша версия, и что Claude Code читает из вашего кода.

Эта запись показывает готовый мод. Спиннер подсчитывает вызовы инструментов, `/tally` выводит счётчик, и редактирование кода вступает в силу во время работы сеанса:

<video autoPlay muted loop playsInline controls src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-first-mod-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=eb561134afa90375777408453ba51c77" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. The spinner reads 'Thinking · tool calls: 1' and the count rises as Claude works. The /tally command prints 'first-mod: Claude has made 3 tool calls since this mod loaded'. A line says first-mod reloaded and lists its four hooks. On the next prompt the spinner reads 'Thinking · tools used: 1'." />

Вы пишете три файла:

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
* **`register.js`**: ваш код, называемый модулем hooks

**1. Создайте каталог плагина**

Создайте два каталога, которые содержат файлы:

> [tab] Bash или Zsh
>
> ```bash theme={null}
> mkdir -p first-mod/.claude-plugin first-mod/hooks
> ```

> [tab] PowerShell
>
> ```powershell theme={null}
> New-Item -ItemType Directory -Force first-mod\.claude-plugin, first-mod\hooks
> ```

**2. Напишите манифест**

Мод — это плагин, и моду нужен [манифест](https://code.claude.com/docs/ru/plugins/manifest-reference.md). Манифест этого мода не имеет специальных полей. Сохраните это как `first-mod/.claude-plugin/plugin.json`:

```json first-mod/.claude-plugin/plugin.json theme={null}
{
  "name": "first-mod",
  "version": "0.1.0",
  "description": "Counts Claude's tool calls, shows the count beside the spinner, and adds a /tally command",
  "author": { "name": "Your Name" }
}
```

**3. Скажите Claude Code, где находится ваш код**

Когда Claude Code загружает плагин, он читает `hooks/hooks.json` плагина. Ключ `modules` в этом файле указывает путь к вашему коду, и его наличие делает плагин модом. Перечислите один путь, относительный к `hooks.json`. Здесь он указывает на `register.js`, который вы напишете на следующем шаге.

Сохраните это как `first-mod/hooks/hooks.json`:

```json first-mod/hooks/hooks.json theme={null}
{
  "description": "The first-mod hooks module",
  "modules": ["./register.js"]
}
```

**4. Напишите код**

Этот файл — это код мода, называемый модулем hooks. Когда мод загружается, Claude Code вызывает функцию `register`, которую экспортирует файл, и передаёт ей функцию с именем [`on`](https://code.claude.com/docs/ru/plugins/mods/reference#the-hook-function). Каждый вызов `on` регистрирует обработчик события, называемый hook, для события, которое он называет.

Сохраните это как `first-mod/hooks/register.js`:

```javascript first-mod/hooks/register.js theme={null}
// The count, shared by the hooks below
let calls = 0

// Claude Code calls this once when the mod loads
export function register(on) {
  // Runs when the session starts, before your first prompt
  on('session.start', async ($, e, next) => {
    // Add the /tally command
    await $.command.register({
      name: 'tally',
      description: 'Show how many tool calls Claude has made',
    })
    // Let the session start as usual
    return next(e)
  })

  // Runs each time Claude is about to use a tool
  on('tool.call', async ($, e, next) => {
    calls += 1
    // Ask Claude Code to draw the interface again, so the new count shows
    $.ui.invalidate('ui.render')
    // Let the tool run as usual
    return next(e)
  })

  // Runs when you type /tally, and only then, because of the matcher
  on('command.run', { command: 'tally' }, async () => {
    // The text to print in the transcript
    return { text: 'Claude has made ' + calls + ' tool calls since this mod loaded' }
  })

  // Runs each time Claude Code draws the spinner
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    // Keep Claude Code's spinner, with the count added after its word
    return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
  })
}
```

Файл хранит счётчик в `calls` и регистрирует четыре hook:

* **[`session.start`](https://code.claude.com/docs/ru/plugins/mods/reference#session)** запускается при запуске сеанса, перед вашим первым приглашением, и снова каждый раз, когда мод перезагружается. Он добавляет команду `/tally` в Claude Code.
* **[`tool.call`](https://code.claude.com/docs/ru/plugins/mods/reference#tools)** запускается каждый раз, когда Claude собирается использовать инструмент. Он добавляет один к `calls` и просит Claude Code нарисовать интерфейс снова.
* **[`command.run`](https://code.claude.com/docs/ru/plugins/mods/reference#commands-and-configuration)** запускается, когда вы вводите `/tally`. Он возвращает текст для вывода.
* **[`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface)** запускается каждый раз, когда Claude Code рисует спиннер. Он добавляет счётчик после слова спиннера.

[Как работает пример мода](#how-the-example-mod-works) объясняет три аргумента, которые принимает каждый hook, и что каждый из них возвращает.

**5. Загрузите мод**

Запустите Claude Code с флагом `--plugin-dir`, который загружает каталог плагина для одного сеанса без его установки:

```bash theme={null}
claude --plugin-dir ./first-mod
```

**6. Попробуйте мод**

Попросите Claude сделать что-то, что требует нескольких вызовов инструментов, например `list the files here and read the README`. Пока Claude работает, слово спиннера сопровождается счётчиком, который растёт, как в `Thinking · tool calls: 2…`. Когда Claude закончит, введите `/tally` и нажмите Enter. Транскрипт показывает `first-mod: Claude has made 2 tool calls since this mod loaded` с вашим собственным счётчиком. Claude Code ставит имя плагина перед текстом команды.

Чтобы проверить команду без интерактивного сеанса, выполните её в неинтерактивном режиме:

```bash theme={null}
claude -p "/tally" --plugin-dir ./first-mod
```

```text theme={null}
first-mod: Claude has made 0 tool calls since this mod loaded
```

Если `/tally` не в списке команд, модуль не загрузился. См. [Узнайте, почему мод ничего не делает](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing).

**7. Измените код во время работы сеанса**

Оставьте сеанс открытым. В `register.js` измените `' · tool calls: '` на `' · tools used: '` в hook `ui.render` и сохраните. Выделенная строка — это та, которая изменяется:

```javascript first-mod/hooks/register.js {4} theme={null}
  // Runs each time Claude Code draws the spinner
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    // Keep Claude Code's spinner, with the count added after its word
    return next({ ...e, props: { ...e.props, suffix: ' · tools used: ' + calls + '…' } })
  })
```

Строка в транскрипте говорит, что `first-mod` перезагрузился и перечисляет его hooks, и следующий спиннер использует новый текст, как в `Thinking · tools used: 1…`.

### Как работает пример мода

Каждая функция, которую вы передаёте `on`, — это hook, который является обработчиком события. Claude Code передаёт каждому hook одни и те же три аргумента:

* **API модов**, названный `$`: каждый метод, который мод может вызвать, чтобы выйти за пределы себя, в [пространствах имён](https://code.claude.com/docs/ru/plugins/mods/reference.md#mods-api-methods) таких как `$.ui` и `$.command`
* **Событие**, названное `e`: [входные данные события](https://code.claude.com/docs/ru/plugins/mods/reference.md#events) как простые данные, такие как имя и аргументы вызова инструмента
* **Следующий обработчик**, названный [`next`](https://code.claude.com/docs/ru/plugins/mods/events#how-a-hook-handles-an-event): функция, которая передаёт событие другим модам, а затем собственному поведению Claude Code, и возвращает результат

Хуки в `first-mod` обрабатывают свои события следующими способами:

* **Observe**: hook `session.start` регистрирует команду, и hook `tool.call` подсчитывает вызов и просит перерисовку. Оба возвращают `next(e)`, поэтому сеанс запускается и инструмент работает как обычно.
* **Answer**: hook `command.run` возвращает свой собственный результат и никогда не вызывает `next`. Второй аргумент `on`, `{ command: 'tally' }`, — это фильтр, называемый [matcher](https://code.claude.com/docs/ru/plugins/mods/events.md#filter-which-events-a-hook-handles), поэтому hook запускается только для `/tally`.
* **Rewrite**: hook `ui.render` вызывает `next` с копией `e`, чей `suffix` содержит счётчик, поэтому Claude Code рисует свой обычный спиннер с вашим текстом после слова

Claude Code следит за каталогом, загруженным с `--plugin-dir`, и горячо перезагружает модуль хуков при изменении файла в нём. Каждая перезагрузка запускает `register` снова, поэтому `calls` возвращается к `0` и `/tally` начинает считать снова. Чтобы сохранить значение между перезагрузками, см. [Сохранение состояния](https://code.claude.com/docs/ru/plugins/mods/interface.md#keep-state).

## Продолжайте работать над модом

После загрузки мода вы можете попросить Claude изменить его, проверить ваш код против определений типов для вашей версии, перечислить события и вызовы, которые Claude Code находит в нём, и протестировать его.

### Измените мод с помощью Claude

Чтобы изменить мод, который у вас уже есть, запустите сеанс с `--plugin-dir`, указывающим на каталог мода, чтобы то, что пишет Claude, загружалось в том же сеансе:

```bash theme={null}
claude --plugin-dir ./first-mod
```

Затем попросите изменение, например `add a /tally-reset command to this mod that sets the tally back to zero`. Claude редактирует модуль hooks, выполняет `claude plugin validate` и исправляет то, что он сообщает. Каталог, который вы загружаете с `--plugin-dir`, — это [защищённый путь](https://code.claude.com/docs/ru/permission-modes.md#protected-paths), поэтому в режимах `default` и `acceptEdits` вас просят одобрить каждое редактирование Claude мода. Таблица защищённых путей даёт результат для других режимов разрешений.

Файлы, которые Claude сохраняет во время его хода, перезагружаются при завершении хода, поэтому вы можете попробовать `/tally-reset` сразу после завершения Claude.

### Получите определения типов для вашей версии

Когда Claude Code загружает мод из `--plugin-dir` в интерактивной сессии или мод, который [Claude написал для вас](#ask-claude-for-a-mod), он записывает файлы объявлений TypeScript в каталог `.claude-plugin/types/` мода. Они описывают точные события, методы API модов и элементы в версии Claude Code, которую вы запускаете, поэтому ваш редактор может автодополнять и проверять типы ваших хуков. Каталог содержит эти файлы:

| Путь | Что он объявляет |
| :- | :- |
| `claude-code/index.d.ts` | Каждое событие и его входные данные и результат, каждое пространство имён API модов и метод, и элементы, которые каждая поверхность может рисовать |
| `claude-code-tools/index.d.ts` | Входные данные встроенных инструментов и результаты, поэтому проверка `e.tool === 'Bash'` сужает `e` |
| `claude-code-mcp/index.d.ts` | Входные данные инструментов MCP, которые были подключены в последний раз, когда вы сохранили файл в модо |
| `index.d.ts` в каталоге, названном в честь плагина | Что этот плагин добавляет в API модов. Есть один каталог для каждого плагина, который ваш `plugin.json` перечисляет в `dependencies`. |
| `tsconfig.json` | Параметры компилятора, которые подходят для модуля hooks |

Если ваш мод не имеет собственного `tsconfig.json`, Claude Code добавляет один в корень мода, который расширяет сгенерированный, поэтому ваш редактор и `tsc -p ./first-mod` проверяют тип мода без дополнительной настройки.

События и методы могут изменяться между выпусками, поэтому доверяйте этим файлам больше, чем любой странице, включая эту, когда они не согласны.

`claude-code/index.d.ts` — это самый полный справочник для вашей сборки, с комментарием и примером для каждого метода API модов. Чтобы что-то найти, поищите в файле его имя, например `'tool.call'`.

### Проверьте, что Claude Code читает из вашего мода

Чтобы увидеть ваш мод так, как Claude Code его видит, без запуска вашего кода или запуска сеанса, используйте `claude plugin validate`. Он проверяет манифест и выполняет тот же статический анализ на исходном коде модуля hooks, который Claude Code выполняет при загрузке мода. В вашей оболочке выполните его на каталоге мода:

```bash theme={null}
claude plugin validate ./first-mod
```

Для `first-mod` вывод включает эти строки.

```text theme={null}
  ❯ ./register.js hooks: session.start, tool.call, command.run{command=tally}, ui.render{component=Spinner}
  ❯ ./register.js calls: $.command.register, $.ui.invalidate

✔ Validation passed
```

Найдите в строке `hooks:` события, на которые ваш модуль устанавливает хуки, каждое с его фильтром в фигурных скобках, а в строке `calls:` — каждый метод API модов, который он вызывает. Если ваш модуль читает или устанавливает переменные окружения, ищите также строки `env reads:` и `env writes:`, а если он использует [`$.state`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state) — строки `state reads:` и `state writes:`. Вы также видите по одной строке для каждого хука, который может отклонить действие, например `gating hook without .catch: tool.call`, которая сообщает, есть ли у этого хука [обработчик `.catch`](https://code.claude.com/docs/ru/plugins/mods/events#handle-a-hook-that-fails).

Если событие, которое вы хотели обработать, отсутствует в строках `hooks:`, Claude Code также не будет вызывать этот хук. Обычная причина — неправильное написание имени события, которое команда сообщает как ошибку, такую как `"tool.calls" is not an event`.

Следуйте этим правилам, чтобы статический анализ мог найти каждый hook и вызов:

* Напишите каждый вызов API модов полностью: `$`, пространство имён, затем метод, как в `$.store.get('notes')`. Вы можете передать `$` функции, объявленной на верхнем уровне того же файла, и для функции вашей с именем `loadNotes` строка `calls:` затем читает `$.store.get (via loadNotes)`. Передача `$` методу, функции, определённой внутри хука, или функции, которую вы импортируете из другого из ваших файлов, не проходит валидацию. Функции `read` и `update`, которые использует [`$.state`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state), — это импорты, которые могут её принять. Не присваивайте `$` или одно из его пространств имён переменной, не деструктурируйте его и не индексируйте его с вычисленным именем. `const ui = $.ui` не проходит с `$.ui is used as a value`.
* Напишите имя события в каждом вызове `on` как строковый литерал, например `'tool.call'`. Переменная или цикл по списку имён не проходит с `the event name passed to on() is not a string literal`.
* Внутри `register` не объявляйте вторую переменную или параметр с именем `on`. Валидация не проходит с `"on" is declared again (shadowed)`.
* Импортируйте только из файлов внутри каталога плагина, по относительному пути. Единственный разрешённый голый импорт — это `claude-code`, для типов и нескольких помощников.
* Используйте объявления `import` в верхней части файла, как в `import { name } from './file.js'`. Динамический `import()` не проходит с `a dynamic import(); a hooks module imports its own files with an import declaration`.
* Напишите каждый файл как модуль ES, с `import`, а не `require`. [Справочник](https://code.claude.com/docs/ru/plugins/mods/reference.md#files) перечисляет расширения файлов, которые загружает Claude Code.

### Протестируйте мод

Вы можете написать автоматизированные тесты для мода и запустить их из вашей оболочки с `claude plugin test`, без сессии, входа или сети. Тест вызывает события, которые обрабатывают ваши хуки, и проверяет, что сделали хуки.

Этот тест вызывает два вызова инструментов, запускает `/tally` и проверяет, что ответ считает оба. Сохраните это как `first-mod/tests/first-mod.test.ts`:

```typescript first-mod/tests/first-mod.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

test('/tally reports the tool calls the mod has seen', async ($, on) => {
  // Answer each tool call in Claude Code's place, so no tool runs
  on('tool.call', () => ({ result: 'ok' }))

  // Fire two tool calls, which the mod's tool.call hook counts
  await $.tool.call({ tool: 'Bash', command: 'ls' })
  await $.tool.call({ tool: 'Read', file_path: 'README.md' })

  // Run /tally and check the text its hook returns
  const answer = await $.command.run({ command: 'tally', args: '' })
  expect(answer.text).toBe('Claude has made 2 tool calls since this mod loaded')
})
```

В вашей оболочке выполните тесты из каталога `first-mod`:

```bash theme={null}
claude plugin test
```

Вывод называет каждый тест и прошёл ли он, с временем, которое варьируется от запуска к запуску:

```text theme={null}
tests/first-mod.test.ts:
(pass) /tally reports the tool calls the mod has seen [22.87ms]

 1 pass
 0 fail
Ran 1 test across 1 file. [0.19s]
```

[Протестируйте мод](https://code.claude.com/docs/ru/plugins/mods/test.md) охватывает заглушку вызова модели или хранилища, и тестирование таймеров и рисунков.

## Поделитесь своим модом

Мод — это плагин, поэтому вы версионируете его в манифесте, и люди устанавливают и обновляют его с помощью команд `/plugin`. Способ распространения зависит от того, для кого он предназначен:

* **Несколько человек**: отправьте им каталог плагина или его `.zip`-архив. См. [Поделиться плагином без маркетплейса](https://code.claude.com/docs/ru/plugins/publish.md#share-a-plugin-without-a-marketplace)
* **Ваша команда**: добавьте его в [собственный маркетплейс](https://code.claude.com/docs/ru/plugins/publish.md#publish-through-your-own-marketplace), например в приватный репозиторий с отдельным каталогом для каждого плагина. Чтобы добавить этот маркетплейс для всех, кто работает в репозитории, [зарегистрируйте его в настройках репозитория](https://code.claude.com/docs/ru/plugins/host-marketplace.md#register-the-marketplace-for-everyone-in-a-repository)
* **Вся ваша организация**: администратор может [установить моды вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods) через управляемые настройки
* **Кто угодно**: сделайте репозиторий вашего маркетплейса публичным или [отправьте плагин в каталог Anthropic](https://code.claude.com/docs/ru/plugins/publish.md#submit-to-anthropics-directory)

Перед этим проверьте `name` плагина: `claude plugin validate` не проходит имя, которое [выглядит как одно из собственных Anthropic](https://code.claude.com/docs/ru/plugins/manifest-reference.md#name), например то, которое начинается с `claude-`. События и методы могут изменяться между выпусками, поэтому ваш README — это место, где нужно сказать, какую версию Claude Code вы тестировали.

Продолжайте разработку против каталога с `--plugin-dir`, а не против установленной копии. Claude Code кэширует установленный плагин по версии, поэтому ваши редактирования не достигают установленной копии, пока вы не повысите версию и не установите снова.

## Следующие шаги

* [Рисуйте в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md): откройте панель, рисуйте над приглашением и добавляйте кнопки и текстовые поля
* [Реагируйте на события](https://code.claude.com/docs/ru/plugins/mods/events.md): hook вызовы инструментов, приглашения и ходы
* [Используйте API модов](https://code.claude.com/docs/ru/plugins/mods/api.md): добавляйте команды и инструменты, вызывайте модель и запускайте работу по таймеру
* [Протестируйте мод](https://code.claude.com/docs/ru/plugins/mods/test.md): заглушка того, что Claude Code ответит, и тестирование таймеров и рисунков
* [Устраняйте неполадки мода](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md): причины, по которым мод ничего не делает, и журнал отладки
* [Прочитайте исходный код встроенных модов](https://code.claude.com/docs/ru/plugins/mods/overview.md#read-the-source-of-built-in-mods): полные плагины, каждый со своим модулем hooks и тестами
