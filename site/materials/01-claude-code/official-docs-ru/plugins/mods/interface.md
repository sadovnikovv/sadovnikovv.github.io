> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Рисование в интерфейсе с помощью мода

> Рисуйте панели, полосу над промптом, кнопки и текстовые поля из мода Claude Code, обрабатывайте нажатия и ввод, и сохраняйте состояние между перерисовками и сессиями.

Мод может рисовать свой собственный интерфейс в Claude Code и изменять части интерфейса, которые уже рисует Claude Code. Каждое место, где мод может рисовать, называется [сайтом рендеринга](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites), например панель, полоса над промптом или спиннер. Claude Code вызывает событие [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface) каждый раз, когда собирается рисовать сайт рендеринга, и ваш хук для этого события возвращает то, что нужно рисовать там.

На этой карте показано, где мод может рисовать в сессии терминала:

![Карта сессии терминала Claude Code в полноэкранном режиме отрисовки. Мод может добавить панель в виде боковой панели справа, всплывающее уведомление в правом верхнем углу транскрипта, строку лога в транскрипте, полосу над промптом и строку состояния под промптом. Мод может перерисовывать сообщения, строки вызовов инструментов и спиннер. Промпт принадлежит самому Claude Code.](https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-screen-map.svg?fit=max\&auto=format\&n=dgiVO_Od1X1faduV\&q=85\&s=5fda26b6609c62b68c6f9e528c1590ea)

В более узком терминале панель находится над промптом вместо того, чтобы находиться рядом с транскриптом.

Создайте свой [первый мод](https://code.claude.com/docs/ru/plugins/mods/create.md) перед тем, как начать здесь. Начните с рабочего примера, который создает панель с двумя вкладками и счетчиком, затем прочитайте раздел для каждой части, которую вы хотите изменить.

> [!NOTE]
>
> Чтобы найти одно свойство или ограничение, см. [справку](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites).

## Создание панели с вкладками

В этом разделе вы создаете мод, который добавляет команду `/hello-tabs`, и команда открывает панель. Панель — это боковая панель рядом с транскриптом в широком полноэкранном терминале или обрамленная область над промптом в противном случае. Эта панель показывает две вкладки, и вторая вкладка имеет кнопку, которая добавляет единицу к счетчику. Счет остается там после перезагрузки Claude Code.

Готовый мод выглядит так. Запись открывает панель, переключается на вторую вкладку, нажимает кнопку несколько раз и возвращается на первую вкладку:

<video autoPlay muted loop playsInline controls src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-hello-tabs-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=49d520094d87b5b44bfe50fa49677f06" aria-label="The /hello-tabs command is typed at the Claude Code prompt and a framed pane opens above it, with '1: One' and '2: Two' across the top and the text 'This is the first tab.' The second tab shows an 'Add one' button beside 'Count: 1', and the count rises to 3. The pane then returns to the first tab." />

Вкладки — это две кнопки в ряду. Мод отслеживает, какая из них активна, и рисует содержимое этой вкладки под рядом.

**1. Создание плагина**

Мод — это плагин с манифестом, `hooks.json`, который указывает на ваш код, и файл кода. [Создание мода](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself) объясняет каждый из них. Создайте каталог с именем `hello-tabs` с каталогами `.claude-plugin` и `hooks` внутри него, затем сохраните первые два файла.

Сохраните манифест как `hello-tabs/.claude-plugin/plugin.json`:

```json hello-tabs/.claude-plugin/plugin.json theme={null}
{
  "name": "hello-tabs",
  "version": "0.1.0",
  "description": "Opens a pane with two tabs and a counter",
  "author": { "name": "Your Name" }
}
```

Назовите точку входа в `hello-tabs/hooks/hooks.json`:

```json hello-tabs/hooks/hooks.json theme={null}
{
  "modules": ["./register.js"]
}
```

**2. Написание кода**

В этом списке указано, что делает каждый хук, в том порядке, в котором они появляются в коде:

* Добавляет команду `/hello-tabs` и загружает счет, сохраненный предыдущей сессией
* Открывает панель при запуске этой команды
* Рисует содержимое панели: ряд вкладок и тело открытой вкладки

Две переменные уровня модуля, `tab` и `count`, содержат состояние панели.

Сохраните это как `hello-tabs/hooks/register.js`:

```javascript hello-tabs/hooks/register.js theme={null}
// The pane's id, used to open the pane and to recognize it when drawing
const PANE = 'hello-tabs'

// What the pane shows: which tab is open, and the counter's value
let tab = 'one'
let count = 0

export function register(on) {
  // Runs before your first prompt, and again after a reload
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'hello-tabs', description: 'Open the hello-tabs pane' })
    // Load the count an earlier session saved, if there is one
    const saved = await $.store.get('count')
    if (typeof saved === 'number') count = saved
    return next(e)
  })

  // Runs when you type /hello-tabs
  on('command.run', { command: 'hello-tabs' }, async ($) => {
    // Open the pane, give it the keyboard, and let Esc close it
    await $.ui.open({ id: PANE, title: 'Hello tabs', focus: true, closeOnEscape: true })
    // Print nothing in the transcript
    return {}
  })

  // Runs each time Claude Code draws a pane
  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    // Leave other mods' panes alone
    if (e.requestId !== PANE) return next(e)
    // Get the elements this app can draw
    const { Box, Text, Button } = $.ui.resolve(e)
    // Ask Claude Code to run this hook again
    const redraw = () => $.ui.invalidate('ui.render')

    // One tab: a button that switches to its tab when pressed
    const tabButton = (name, label, hotkey) =>
      Button({
        key: 'tab-' + name,
        label,
        hotkey,
        plain: true,
        // Dim the tab that isn't open
        dimColor: tab !== name,
        onPress: () => {
          tab = name
          redraw()
        },
      })

    // What goes under the tabs, depending on which one is open
    const body =
      tab === 'one'
        ? [Text({ children: ['This is the first tab.'] })]
        : [
            Box({
              flexDirection: 'row',
              columnGap: 2,
              children: [
                Button({
                  key: 'more',
                  label: 'Add one',
                  hotkey: 'a',
                  onPress: async () => {
                    count += 1
                    redraw()
                    // Save the count so it's there after a restart
                    await $.store.set('count', count)
                  },
                }),
                Text({ children: ['Count: ' + count] }),
              ],
            }),
          ]

    // The whole pane: the row of tabs, a blank line, then the body
    return Box({
      flexDirection: 'column',
      children: [
        Box({
          flexDirection: 'row',
          columnGap: 3,
          children: [tabButton('one', 'One', '1'), tabButton('two', 'Two', '2')],
        }),
        Text({ children: [' '] }),
        ...body,
      ],
    })
  })
}
```

Каждый хук также делает что-то, что код не делает явным:

* **[`session.start`](https://code.claude.com/docs/ru/plugins/mods/reference#session)** также читает сохраненный счет из [`$.store`](#keep-state), хранилища ключ-значение, которое сохраняется между сессиями.
* **[`command.run`](https://code.claude.com/docs/ru/plugins/mods/api#add-a-command)** только сообщает Claude Code, что панель существует. Открытие панели ничего не рисует само по себе: Claude Code затем вызывает `ui.render`, чтобы спросить, что в ней находится.
* **`ui.render`** возвращает дерево элементов, `Box`, который содержит другие боксы, текст и кнопки, и создает его заново из `tab` и `count` каждый раз, когда он запускается.

Нажатие кнопки запускает ее обратный вызов `onPress`, который изменяет переменную и вызывает `redraw`. Claude Code затем запускает хук `ui.render` снова, и хук создает новое дерево из новых значений. Каждое интерактивное рисование использует этот цикл рендеринга: обратный вызов изменяет состояние, и хук рисует снова из нового состояния.

**3. Открытие панели**

В вашей оболочке запустите Claude Code с помощью `claude --plugin-dir ./hello-tabs`. В промпте Claude Code запустите `/hello-tabs`. Панель открывается с `1: One` и `2: Two` в верхней части. Нажмите `2`, затем нажмите `a`, горячую клавишу для **Add one**, несколько раз. Счет растет.

**4. Проверка того, что счет был сохранен**

Нажмите Esc, чтобы закрыть панель, затем выйдите из сессии. В вашей оболочке запустите Claude Code снова с той же командой `claude --plugin-dir ./hello-tabs`, и в промпте Claude Code запустите `/hello-tabs`. Счет находится там, где вы его оставили.

Чтобы очистить счет, попросите мод вызвать `$.store.delete('count')`. [Сохранение состояния](#keep-state) охватывает, как долго длится каждый вид значения.

## Выбор места для рисования

Чтобы выбрать точку отрисовки, в которой рисует хук `ui.render`, передайте фильтр, называемый [matcher](https://code.claude.com/docs/ru/plugins/mods/events.md#filter-which-events-a-hook-handles), в качестве второго аргумента для `on`. `{ component: 'Pane' }` запускает хук только для панелей. В хуке `e.component` называет точку отрисовки, `e.surface` говорит, какое приложение рисует, а `e.props` содержит собственные данные точки отрисовки. Для панели `e.requestId` — это `id`, с которым вы ее открыли.

Панель и полоса пусты, пока мод их не заполнит. Выберите вкладку, чтобы увидеть, что представляет собой каждая из них и как в ней рисовать:

> [tab] Pane
>
> Панель — это боковая панель рядом с транскриптом в широком полноэкранном терминале или обрамленная область над промптом в противном случае. При открытии нескольких панелей каждая получает вкладку, которая показывает ее название.
>
> Панель появляется, когда ваш мод вызывает `$.ui.open` с `id`, который вы выбираете, как в `$.ui.open({ id: 'hello-tabs' })`. [Открытие панели в нужное время](#open-a-pane-at-the-right-time) охватывает другие поля и случаи, когда панель ждет более широкого терминала.
>
> Чтобы рисовать в вашей панели, отфильтруйте по `{ component: 'Pane' }` и проверьте, что `e.requestId` — это ваш `id`.

> [tab] Band above the prompt
>
> Полоса — это полоса прямо над полем ввода промпта. Каждый мод, который рисует в ней, получает собственную строку, и строки располагаются сверху вниз в [порядке запуска модов](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in).
>
> Чтобы нарисовать строку вашего мода, отфильтруйте по `{ component: 'AbovePrompt' }` и верните [дерево](#build-a-tree-from-elements). Чтобы ничего не рисовать, верните `next(e)`.
>
> До v2.1.323 все моды использовали в полосе один общий рисунок, и ваше дерево заменяло то, что рисовали моды после вашего. Чтобы поддерживать и эти версии, поместите результат `await next(e)` среди дочерних элементов [`Box`, который остается корректным](https://code.claude.com/docs/ru/plugins/mods/troubleshoot#another-mods-band-shows-and-yours-doesnt). В v2.1.323 или новее этот дочерний элемент не рисует строки других модов.

Мод также может [поместить собственную строку в транскрипт](#place-a-row-in-the-transcript).

### Изменение того, что уже рисует Claude Code

Claude Code рисует большую часть своего интерфейса сам: сообщения, строки вызовов инструментов, спиннер и многое другое. Каждая из этих частей также является сайтом рендеринга, поэтому мод может изменить ее стиль или заменить ее. Чтобы изменить одну из них, отфильтруйте ваш хук `ui.render` по ее имени из этой таблицы:

| Сайт | Что это такое |
| :- | :- |
| `UserMessage`, `AssistantMessage` | Сообщение в транскрипте |
| `ToolUse`, `ToolResult`, `ToolGroup` | Строка вызова инструмента, его результат и свернутая группа вызовов |
| `CommandOutput` | Строка, которую напечатала команда |
| `AskUserQuestion` | Диалог, который Claude открывает, чтобы задать вам вопрос |
| `Spinner`, `ToolProgress`, `TurnDuration` | Строки состояния для хода: строка, которая анимируется, пока Claude работает, строка текущего прогресса работающего инструмента и строка, которая закрывает ход |
| `InfoNotice`, `SessionMode`, `PromptHint` | Строки состояния под логотипом, метки режима в нижнем колонтитуле и строка подсказки под промптом |

`Pane`, `AskUserQuestion`, `Spinner`, `UserMessage`, `AssistantMessage` и точки отрисовки вызовов инструментов работают в терминале, приложении Desktop и расширении VS Code. Таблица [точек отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) указывает, где вызывается каждая из остальных.

На сайте, который Claude Code уже рисует, ваш хук может изменить деталь, заменить рисование или оставить его в покое. Выберите вкладку, чтобы увидеть каждый из вариантов, применяемый к спиннеру. Примеры читают переменную `calls`, которую подсчитывает другой хук, как в [учебном моде](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself).

> [tab] Change a detail
>
> Чтобы сохранить рисование Claude Code и изменить одну его часть, передайте `next` копию события с измененными `props`. Этот хук изменяет текст после слова спиннера:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
>   // Keep Claude Code's spinner, and change the text after its word
>   return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
> })
> ```
>
> Спиннер сохраняет свою анимацию и свое слово, и ваш текст следует за словом:
>
> ```text theme={null}
> Thinking · tool calls: 2…
> ```

> [tab] Replace the drawing
>
> Чтобы нарисовать что-то свое на месте сайта, верните дерево и не вызывайте `next`. Этот хук рисует одну строку текста там, где был бы спиннер:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e) => {
>   const { Text } = $.ui.resolve(e)
>   // No call to next, so this line is drawn in the spinner's place
>   return Text({ children: ['Claude has made ' + calls + ' tool calls'] })
> })
> ```
>
> Пока Claude работает, показывается ваша строка, а спиннер Claude Code не показывается:
>
> ```text theme={null}
> Claude has made 2 tool calls
> ```

> [tab] Leave it alone
>
> Чтобы оставить сайт таким, каким его рисует Claude Code, верните `next(e)`. Хук часто делает это для одних событий и не делает для других. Этот хук оставляет спиннер в покое, пока нечего считать:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
>   // Nothing to show yet, so pass the event on unchanged
>   if (calls === 0) return next(e)
>   return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
> })
> ```
>
> До первого вызова инструмента спиннер выглядит так, как он выглядит без мода:
>
> ```text theme={null}
> Thinking…
> ```

На этих сайтах `next(e)` возвращает ссылку на рисование Claude Code, `{ type: 'engine', ref }`, если только мод, который запускается после вашего, не вернул собственное дерево. Чтобы изменить то, что находится в этом рисовании, передайте `next` копию события с другими props, как это сделано на вкладке **Change a detail**. Вы можете вернуть ссылку как есть или поместить ее в `Box` рядом с собственными элементами:

```javascript theme={null}
on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
  const { Box, Text } = $.ui.resolve(e)
  const theirs = await next(e)
  return Box({ flexDirection: 'column', children: [theirs, Text({ children: ['under the spinner'] })] })
})
```

Пока Claude работает, спиннер анимируется как прежде, а под ним появляется `under the spinner`.

Запрос разрешения не является точкой отрисовки, поэтому мод не может изменить то, что он показывает. Диалог вопроса, `AskUserQuestion`, является точкой отрисовки, поэтому мод может изменить этот диалог, когда Claude задает вопрос. Дерево для диалога должно содержать ссылку ровно один раз, а ваши элементы — над ней. В противном случае Claude Code рисует собственный диалог.

### Открытие панели в нужное время

Панель появляется только тогда, когда ваш мод ее открывает. То, как и когда вы ее открываете, определяет, получает ли она фокус клавиатуры, сколько места она запрашивает и появляется ли она вообще в узком терминале.

Чтобы открыть панель, вызовите [`$.ui.open`](https://code.claude.com/docs/ru/plugins/mods/reference#mods-api-methods) с `id`, который вы выбираете. `id` — это имя панели: ваш хук `ui.render` проверяет его, и вы передаете его снова, чтобы закрыть панель. Если у другого мода уже открыта панель с этим `id`, вызов завершается отклонением.

```javascript theme={null}
await $.ui.open({ id: 'hello-tabs', title: 'Hello tabs', focus: true })
```

Чтобы закрыть панель, вызовите `$.ui.close` с `id`, с которым вы ее открыли:

```javascript theme={null}
await $.ui.close({ id: 'hello-tabs' })
```

Помимо `id`, `$.ui.open` принимает эти необязательные поля:

| Поле | Что оно делает |
| :- | :- |
| `title` | Метка вкладки панели, когда открыто несколько панелей |
| `focus` | Запрашивает [фокус клавиатуры](#know-which-keys-your-mod-can-receive) |
| `closeOnEscape` | Позволяет закрыть панель клавишей Esc |
| `holdToasts` | В терминале удерживает всплывающие уведомления, пока показывается именно эта панель. См. [Удержание всплывающих уведомлений за диалогом](#hold-toasts-behind-a-dialog). |
| `rows` | Высота, которую нужно запросить, когда панель находится над промптом. По умолчанию треть пространства. |
| `columns` | Ширина, которую нужно запросить, когда панель находится рядом с транскриптом, — не более 45% ширины терминала. Если пользователь уже изменил размер панели рядом с транскриптом в этой или более ранней сессии, панели открываются там с заданной им шириной. К этой ширине применяется тот же предел в 45%. |

[Расширение VS Code](#draw-in-the-vs-code-extension) игнорирует `rows` и `columns` и определяет размер панели само.

`focus`, `closeOnEscape` и `holdToasts` являются необязательными и принимают только `true`. Чтобы не задавать одно из них, опустите его. Передача `false` выбрасывает ошибку, такую как `ui.open: focus is true or left out`. Чтобы установить одно из них условно, добавляйте поле только тогда, когда условие выполняется. Этот вызов запрашивает фокус клавиатуры, только когда `items` не пусто:

```javascript theme={null}
const pane = { id: 'hello-tabs', title: 'Hello tabs' }
await $.ui.open(items.length > 0 ? { ...pane, focus: true } : pane)
```

Чтобы позволить команде открыть панель, пока Claude работает, добавьте `immediate: true` при [регистрации команды](https://code.claude.com/docs/ru/plugins/mods/api.md#add-a-command). Без этого команда, введенная во время хода, ждет конца хода.

#### Удержание всплывающих уведомлений за диалогом

Передайте `holdToasts: true` в `$.ui.open`, когда панель — это диалог, на который пользователь отвечает и который затем покидает, чтобы всплывающие уведомления не появлялись, пока он принимает решение. В терминале удержание длится, пока показывается именно эта панель, а всплывающее уведомление, вызванное в это время, ждет окончания удержания.

Claude Code удерживает всплывающие уведомления других модов и собственные кратковременные уведомления, а также те, которые ваш мод вызывает с помощью [`$.ui.toast`](https://code.claude.com/docs/ru/plugins/mods/api#show-something-without-starting-a-turn). Не задавайте это поле для панели, которая остается открытой, чтобы пользователь продолжал их видеть.

#### Когда панель ждет более широкого терминала

Панель, которую ваш мод открывает без запроса, не появляется в узком терминале, поэтому она не может захватить маленький экран. Появится ли она, зависит от того, что ее открыло:

* **Открыто чем-то, что сделал пользователь**, например командой, которую он запустил, или кнопкой, которую он нажал, — панель появляется при любой ширине
* **Открыто вашим модом, действующим самостоятельно**, например из таймера или хука [`turn.start`](https://code.claude.com/docs/ru/plugins/mods/events#follow-a-turn), — панель появляется только в терминале шириной не менее 144 столбцов. После того как пользователь сам открыл эту панель хотя бы раз, достаточно 110 столбцов.

Когда панель появляется, `$.ui.open` разрешается в `{ isPlaced: true }`. Когда панель ждет, `isPlaced` имеет значение `false`, а `reason` — это строка, объясняющая причину. Ожидающая панель появляется, когда пользователь ее открывает или расширяет терминал. Чтобы сообщить, что что-то доступно, не открывая панель, вызовите `$.ui.toast('Your message')`, который показывает всплывающее уведомление.

### Рисование в расширении VS Code

В расширении VS Code то, что рисует мод, появляется на панели чата в расширении версии 2.1.299 или новее. Сессии, которая [не получает флаги функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), например сессии в Amazon Bedrock, требуется версия 2.1.304 или новее. В хуке `ui.render` для панели чата `e.surface` имеет значение `vscode`. Чтобы проверить, какие точки отрисовки и элементы рисует панель чата и какие пропсы она игнорирует, см. таблицы [точек отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) и [элементов](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements).

Чтобы мод работал на панели чата так же, как в терминале, учитывайте следующие различия:

* **Панели**: на панели чата шириной 800 пикселей или больше панели закрепляются рядом с диалогом, `e.props.placement` имеет значение `'dock'`, а `e.viewport.isFullscreen` — `true`. На более узкой панели чата панели рисуются над полем промпта, `placement` имеет значение `'inline'`, а панель показывает 12 строк, прежде чем начать прокрутку.
* **Всплывающие уведомления и строки состояния**: они располагаются в одном стеке прямо над полем промпта вместе с панелями, когда панель чата узкая, по одной строке состояния на мод. Стек скрывается, пока показывается запрос разрешения или диалоговое окно.
* **Метки**: панель чата обрамляет то, что мод рисует или переписывает, и помечает это именем плагина, например **From the token-chart plugin** или **Edited by the token-chart plugin**.
* **Клавиатура**: у кнопок нет горячих клавиш, поэтому пользователь нажимает кнопку мышью или нажимает Enter, когда она получила фокус.
* **Фокус клавиатуры**: панель чата выполняет запрос панели `focus: true` только тогда, когда панель чата находится в фокусе, Claude бездействует и не ожидает ответа на вопрос, а поле промпта пусто.
* **Диалоговое окно вопроса**: в `AskUserQuestion` панель чата сохраняет собственную карточку вопроса и рисует ваши элементы над ней. Пропсы, которые вы передаете в `next`, не изменяют карточку.
* **Предложения промпта**: `$.prompt.suggest` разрешается с `isShown: false` и ничего не показывает, потому что панель чата оставляет бледный текст предложения в поле промпта для собственных предложений Claude.
* **Ограничения текста**: панель чата обрезает строку состояния до 200 символов или двух строк, а всплывающее уведомление — до 500 символов.

### Размещение строки в транскрипте

Строка — это строка, которую ваш мод добавляет в транскрипт в терминале после последнего сообщения. Она остается на этом месте по мере продолжения диалога, и Claude ее не видит. `$.ui.place` требует Claude Code v2.1.314 или новее.

**1. Разместите строку**

Вызовите [`$.ui.place`](https://code.claude.com/docs/ru/plugins/mods/reference#mods-api-methods) с `id`. `id` — это имя, которое вы придумываете для строки, например `build-status`. Оно может содержать от 1 до 64 букв, цифр, символов `_` или `-`, и каждой строке, которая есть у вашего мода в транскрипте, нужен собственный `id`.

**2. Нарисуйте строку**

Нарисуйте строку в точке отрисовки [`Placed`](https://code.claude.com/docs/ru/plugins/mods/reference#render-sites).

Этот пример добавляет команду `/build-status`. Когда пользователь запускает команду, мод добавляет строку, которая показывает `Build: passing`. Текст зафиксирован, чтобы пример был коротким, поэтому настоящий мод рисовал бы собственный результат:

```javascript theme={null}
export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'build-status', description: 'Show the build status' })
    return next(e)
  })

  on('command.run', { command: 'build-status' }, async ($) => {
    const placed = await $.ui.place({ id: 'build-status' })
    // Where nothing draws the row, reply with text instead
    return placed.isPlaced ? {} : { text: 'Build: passing' }
  })

  on('ui.render', { component: 'Placed' }, async ($, e, next) => {
    // This hook runs for every mod's rows, and another mod can use the same id
    if (e.props.plugin !== $.plugin.name || e.props.id !== 'build-status') return next(e)
    const { Text } = $.ui.resolve(e)
    return Text({ children: ['Build: passing'] })
  })
}
```

Чтобы попробовать пример, поместите этот код в [мод](https://code.claude.com/docs/ru/plugins/mods/create.md). В сессии терминала запустите `/build-status` в промпте Claude Code. `Build: passing` появится как строка в конце транскрипта.

Вызов не всегда показывает строку, а строка может позже исчезнуть, поэтому обрабатывайте в своем моде следующие случаи:

* **Результат**: `{ isPlaced: true, requestId }`, когда терминал рисует строку. В противном случае `isPlaced` имеет значение `false`, а `reason` объясняет причину, например `no attached surface draws placed rows yet`. Одна из причин — [ограничение на количество строк](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits), которые мод может иметь одновременно.
* **Повторный вызов с тем же `id`**: пока первая строка еще находится в транскрипте, вызов не добавляет строку и разрешается с `requestId` этой строки. Чтобы изменить то, что показывает строка, [перерисуйте строку](#redraw-when-something-changes).
* **Когда строка исчезает**: когда диалог заканчивается, когда пользователь откатывается назад за эту строку или, вне [полноэкранной отрисовки](https://code.claude.com/docs/ru/fullscreen.md), когда диалог сжимается. `--resume` не возвращает строку. Чтобы снова показать строку, вызовите `$.ui.place` еще раз.

### Размещение фона за диалогом

> [!NOTE]
>
> `$.theme.set` и `$.theme.clear` заменяют `$.ui.backdrop`, который был удален в Claude Code v2.1.319. Замените `$.ui.backdrop({ id: 'your-backdrop' })` на вызов `$.theme.set`, подобный вызову в примере этого раздела, а `$.ui.backdrop(undefined)` — на `$.theme.clear()`, который удаляет фон любого мода.

Чтобы разместить фон за диалогом в приложении Desktop или мобильном приложении, вызовите [`$.theme.set`](https://code.claude.com/docs/ru/plugins/mods/reference#mods-api-methods) с `backdrop`, а затем нарисуйте фон в точке отрисовки [`Backdrop`](https://code.claude.com/docs/ru/plugins/mods/reference#render-sites). Чтобы убрать фон, вызовите `$.theme.clear()`. Терминал фон не рисует. `$.theme.set` и `$.theme.clear` требуют Claude Code v2.1.319 или новее.

Этот пример требует Claude Code v2.1.323 или новее, поэтому сначала [проверьте свою версию](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off). Мод устанавливает фон при запуске сессии, рисует фон и добавляет команду `/plain`, которая убирает фон:

```javascript theme={null}
export function register(on) {
  // Neither a reload of this mod nor --resume keeps the backdrop, so set it here
  on('session.start', async ($, e, next) => {
    await $.theme.set({ backdrop: { scene: 'night-sky' }, overrideColorScheme: 'dark' })
    await $.command.register({ name: 'plain', description: 'Take the backdrop off' })
    return next(e)
  })

  on('ui.render', { component: 'Backdrop' }, async ($, e, next) => {
    // This hook runs for every mod's backdrop, and another mod can use the same scene
    if (e.props.plugin !== $.plugin.name || e.props.scene !== 'night-sky') return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return Box({ backgroundColor: 'blue', children: [Text({ children: ['Night sky'] })] })
  })

  on('command.run', { command: 'plain' }, async ($) => {
    const cleared = await $.theme.clear()
    return { text: cleared.reason }
  })
}
```

> [!NOTE]
>
> До v2.1.323 пишите `id` вместо `scene` в вызове `$.theme.set` и в `e.props`, а `overrideColorScheme` переместите внутрь `backdrop` как `colorScheme`.

Чтобы попробовать пример, поместите этот код в [мод](https://code.claude.com/docs/ru/plugins/mods/create.md) и запустите сессию в приложении Desktop или мобильном приложении. Чтобы убрать фон, запустите `/plain` в промпте Claude Code. Транскрипт покажет `the theme is cleared` после имени мода, например `night-sky: the theme is cleared` для мода с именем `night-sky`.

Проверьте, что принимает `backdrop`, что сообщает вам результат вызова и что могут изменить другие моды:

* **Поля `backdrop`**: `scene` — это [имя](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits), которое вы выбираете для фона, рисуемого вашим хуком. Об остальных полях и `overrideColorScheme` см. [типы для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build).
* **Рисуется ли фон**: `$.theme.set` разрешается с `isDrawn: true`, когда приложение Desktop или мобильное приложение, подключенное к сессии, сообщает, что рисует фоны. В противном случае `isDrawn` имеет значение `false`, а `reason` объясняет причину.
* **Одна тема на каждую сессию**: мод, вызывающий `$.theme.set`, заменяет фон и [цвета](#change-the-colors-of-the-desktop-app) сессии, а мод, вызывающий `$.theme.clear()`, удаляет их, независимо от того, какой мод их установил. Вызывайте `$.theme.clear()` только тогда, когда об этом просит пользователь.

### Изменение цветов приложения Desktop

Чтобы изменить цвета вкладки Code в приложении Desktop с помощью мода, [попросите Claude создать такой мод](#ask-claude-for-a-colors-mod) или [напишите его сами](#write-a-colors-mod-yourself). Оба способа требуют Claude Code v2.1.324 или новее на вкладке Code, поэтому сначала [проверьте версию там](https://code.claude.com/docs/ru/desktop.md#claude-code-version-in-the-code-tab). Claude Code в терминале сохраняет собственные цвета.

#### Запрос мода с цветами у Claude

**1. Опишите цвета**

Запустите локальную сессию на вкладке Code и скажите Claude, какие цвета вам нужны. Например, введите `make a mod that makes the app cream in light mode and dark brown in dark mode`. Claude напишет файлы мода.

**2. Одобрите мод**

Ответьте на вопросы, которые Claude Code задает о файлах мода и горячей перезагрузке. О том, что делает каждый ответ, см. [Запрос мода у Claude](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod).

**3. Проверьте цвета**

Вкладка Code меняет цвета, когда мод загружается. Чтобы скорректировать цвет, скажите Claude, что изменить. Если ничего не меняется, см. [Исправление отсутствующих цветов мода](#fix-missing-mod-colors-in-the-desktop-app).

#### Самостоятельное написание мода с цветами

`makeColors` — это функция, которая создает тему из нескольких шестнадцатеричных цветов. Следующие шаги создают мод с именем `paper`, который ее использует.

**1. Попросите Claude скопировать makeColors**

Запустите локальную сессию на вкладке Code и введите `copy make-colors.js and make-colors.d.ts from your plugin-authoring skill into ~/.claude/skills/paper/hooks/`. Убедитесь, что оба файла находятся в этом каталоге.

**2. Сохраните манифест и hooks.json**

Из раздела [Самостоятельное написание мода](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself) сохраните `.claude-plugin/plugin.json` и `hooks/hooks.json` в `~/.claude/skills/paper/` и замените `first-mod` на `paper` в обоих файлах. Мод [в `~/.claude/skills/`](https://code.claude.com/docs/ru/plugins/create#scaffold-a-plugin-that-loads-every-session) загружается при запуске сессии.

**3. Напишите код**

Сохраните этот файл как `~/.claude/skills/paper/hooks/register.js`. При запуске сессии код вызывает `$.theme.set` с цветами для светлого и темного режимов:

```javascript theme={null}
import { makeColors } from './make-colors.js'

const { theme } = makeColors({
  label: 'Paper',
  // surface-0 is the background, text-primary is the main text, and text-muted is the faint text
  light: {
    gray: { anchors: { 'surface-0': '#efe6d3', 'text-primary': '#2a241d', 'text-muted': '#6a5f50' } },
  },
  dark: {
    gray: { anchors: { 'surface-0': '#1f1a15', 'text-primary': '#f0e7d7', 'text-muted': '#aca08d' } },
  },
})

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.theme.set({ colors: theme })
    return next(e)
  })
}
```

Чтобы использовать собственные цвета, замените шестнадцатеричные значения другими шестизначными шестнадцатеричными цветами.

**4. Проверьте цвета**

Запустите новую локальную сессию на вкладке Code. Со значениями из примера фон становится кремовым в светлом режиме и темно-коричневым в темном режиме. Если ничего не меняется, см. [Исправление отсутствующих цветов мода](#fix-missing-mod-colors-in-the-desktop-app).

### Исправление отсутствующих цветов мода в приложении Desktop

Если вы используете [стороннего провайдера](https://code.claude.com/docs/ru/third-party-integrations.md) вместо аккаунта Claude в [Claude Desktop v5.11492.5 или более ранней версии](https://code.claude.com/docs/ru/desktop.md#check-your-version), вкладка Code сохраняет собственные цвета, поэтому пропустите эти проверки. В остальных случаях, если цвета мода не появляются на вкладке Code или исчезают, проверьте следующие причины:

* **Старая версия**: [обновите приложение Desktop](https://code.claude.com/docs/ru/desktop.md#claude-code-version-in-the-code-tab), перезапустите его и запустите новую локальную сессию на вкладке Code. Если мод написал Claude, попросите его об этом там снова.
* **Мод не загружен**: если мод написал Claude, узнайте, когда он загружается, в разделе [Запрос мода у Claude](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod). Если вы написали его сами, сравните свои файлы и их пути с разделом [Самостоятельное написание мода с цветами](#write-a-colors-mod-yourself).
* **Отклоненная тема**: попросите Claude выполнить вызов [`makeColors`](#write-a-colors-mod-yourself) из мода. Если вызов выбрасывает ошибку или в его списке `problems` есть запись, начинающаяся с `Desktop won't paint this theme`, попросите Claude исправить тему. Если вы установили мод, отправьте то, что нашел Claude, его автору.
* **Другой вызов `$.theme`**: когда любой мод в сессии вызывает `$.theme.set` или `$.theme.clear()`, цвета и [фон](#put-a-backdrop-behind-the-conversation) из более раннего вызова исчезают. В собственном моде передавайте `colors` и `backdrop` в одном и том же вызове `$.theme.set`. Используйте одновременно только один мод, задающий тему.

### Удаление цветов мода из приложения Desktop

Чтобы убрать цвета мода с вкладки Code, сначала отключите мод. Мод, который все еще включен, может снова задать свои цвета.

**1. Отключите мод**

* **Мод написал Claude**: переместите его каталог из [папки модов](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod) той сессии, в которой Claude его написал.
* **Вы поместили мод в `~/.claude/skills/`**: переместите его каталог, например `~/.claude/skills/paper/`, в место за пределами `~/.claude/skills/`.
* **Вы установили мод**: в приложении Desktop [отключите или удалите его плагин](https://code.claude.com/docs/ru/desktop.md#install-plugins) в разделе **Manage plugins**. Если вы не видите **Manage plugins** и у вас есть [CLI](https://code.claude.com/docs/ru/quickstart.md), вы можете [отключить или удалить плагин из маркетплейса в своей оболочке](https://code.claude.com/docs/ru/plugins/install.md#manage-plugins-from-your-shell).

**2. Запустите новую сессию**

Запустите новую локальную сессию на вкладке Code.

**3. Удалите оставшиеся цвета**

Если цвета все еще на месте, откройте **Settings** на вкладке Code и найдите там `code appearance`. Откройте результат и выберите **Remove colors**.

## Создание дерева из элементов

То, что возвращает хук `ui.render`, — это дерево элементов: описание того, что рисовать, состоящее из боксов, текста и элементов управления, вложенных друг в друга. Вы описываете рисование, и Claude Code рисует его в том приложении, которое открыто у пользователя: в терминале, приложении Desktop или расширении VS Code.

Чтобы получить элементы, вызовите `$.ui.resolve(e)` в вашем хуке, как в `const { Box, Text, Button } = $.ui.resolve(e)`. Каждый элемент — это функция. Вы передаете ей свойства, и вы помещаете элементы и строки, которые идут внутри него, в `children`.

Выберите вкладку, чтобы увидеть каждый из самых распространенных элементов и то, как терминал его рисует:

> [tab] Text
>
> `Text` рисует строку с необязательным стилем, таким как `bold` и `color`:
>
> ```javascript theme={null}
> Text({ children: ['This is the first tab.'] })
> ```
>
> ```text theme={null}
> This is the first tab.
> ```

> [tab] Box
>
> `Box` расставляет то, что находится внутри него, в ряд или столбец. Этот помещает кнопку и строку текста рядом, два столбца отдельно:
>
> ```javascript theme={null}
> Box({
>   flexDirection: 'row',
>   columnGap: 2,
>   children: [
>     Button({ key: 'more', label: 'Add one', onPress: addOne }),
>     Text({ children: ['Count: 0'] }),
>   ],
> })
> ```
>
> ```text theme={null}
> [ Add one ]  Count: 0
> ```

> [tab] Button
>
> `Button` — это элемент управления, который пользователь может нажать. Он запускает ваш обратный вызов `onPress`. С `plain: true` он не имеет скобок и показывает его горячую клавишу:
>
> ```javascript theme={null}
> Button({ key: 'more', label: 'Add one', onPress: addOne })
> Button({ key: 'tab-one', label: 'One', hotkey: '1', plain: true, onPress: showTabOne })
> ```
>
> ```text theme={null}
> [ Add one ]
> 1: One
> ```

> [tab] Input
>
> `Input` — это текстовое поле. Он запускает ваш обратный вызов `onSubmit` с текстом, когда пользователь нажимает Enter:
>
> ```javascript theme={null}
> Input({
>   key: 'new-note',
>   label: 'Note',
>   placeholder: 'Type a note and press Enter',
>   value: '',
>   submitLabel: 'add',
>   onSubmit: addNote,
> })
> ```
>
> ```text theme={null}
> Note: Type a note and press Enter
> ```
>
> Задайте для `rows` значение 2 или больше, чтобы получить [поле, вмещающее несколько строк](https://code.claude.com/docs/ru/plugins/mods/gallery.md#input).

В [галерее интерфейсов](https://code.claude.com/docs/ru/plugins/mods/gallery.md) есть примеры и снимки экрана большинства элементов. В этой таблице перечислены основные элементы:

| Элемент | Что он рисует | Где |
| :- | :- | :- |
| `Box` | Контейнер flex. Принимает пропсы макета, такие как `flexDirection`, [`borderStyle`](https://code.claude.com/docs/ru/plugins/mods/reference#box-border-styles) и `width`. Пропсы отступов, такие как `columnGap` и `padding`, принимают число или [имя шага](https://code.claude.com/docs/ru/plugins/mods/reference.md#box-spacing-steps) от `'xs'` до `'xl'`. | Везде |
| `Text` | Стилизованный текст. Принимает `color`, `bold`, `dimColor`, `italic`, `wrap` и другие, такие как [`weight`](https://code.claude.com/docs/ru/plugins/mods/reference#text-typography). `color` — это ключ темы или цвет, такой как `'red'`. `wrap` — это `'wrap'`, `'truncate'`, `'truncate-start'`, `'truncate-middle'` или `'truncate-end'`. | Везде |
| `Button` | Элемент управления, который вызывает `onPress` | Везде |
| `Link`, `Code`, `Markdown` | Ссылка с `href` и необязательной `label`, блок кода и текст, отформатированный так, как ответы Claude. `Markdown` принимает свое содержимое в свойстве `text`, а не в `children`, и нуждается в `key`, когда вы передаете `onLinkPress`. | Везде |
| `Input`, `Select` | Текстовое поле и выпадающий список | Терминал, Desktop, VS Code |
| `Svg` | Документ SVG | Desktop, VS Code |
| `Client` | Область, нарисованная вторым вашим файлом, для анимации и ввода указателем. Этот файл не получает API модов. Он обращается к вашим хукам путем отправки данных, которые поступают как событие `ui.message`. Если он не загружается, не рисует или не выполняется, ваши хуки получают событие [`ui.fault`](https://code.claude.com/docs/ru/plugins/mods/reference#interface). | Терминал, Desktop |
| `Raster`, `Image` | [Сетка цветных ячеек](#draw-a-grid-of-colored-cells) и изображение | Терминал |

Если ваш модуль — это файл `.tsx` или `.jsx`, вы можете написать дерево как JSX. Сначала деструктурируйте элементы из `$.ui.resolve(e)`.

Если ваш рисунок не отображается, проверьте его дерево на наличие пропа, который элемент не принимает, или дочернего элемента там, где его быть не должно. Хук, который возвращает такое дерево, [завершается сбоем](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails), а [строка `hook skipped`](https://code.claude.com/docs/ru/plugins/mods/troubleshoot#a-pane-or-band-is-empty) называет ваш мод и правило, которое нарушило дерево. Для `Text` в панели с пропом `bogusProp` эта строка выглядит так:

```text theme={null}
my-mod: ui.render hook skipped: returned the wrong shape (a tree Pane refuses: Text prop "bogusProp" is not allowed)
```

### `Link` в приложении Desktop и VS Code

В приложении Desktop и расширении VS Code `Link` отображается как обычный текст, если его `href` не соответствует следующим требованиям:

* **Схема и хост**: URL `https:` или URL `http://localhost`, например `http://localhost:3000`
* **Без `@`**: записывайте `@` в пути или запросе как `%40`
* **Написание**: то, что возвращает `new URL(href).href`, за исключением отсутствующего `/` после хоста. Это исключает хост в верхнем регистре, пробел и `:443` в URL `https:`.

В терминале эти требования не действуют.

### Когда `Client` завершается сбоем

В терминале, когда файл, который запускает `Client`, завершается сбоем, тусклая строка, например `my-mod: Client client/spinner.js: boom`, занимает место `Client`, а остальная часть вашего рисунка по-прежнему отображается.

Если ваш мод обрабатывает [`ui.fault`](https://code.claude.com/docs/ru/plugins/mods/reference#interface), Claude Code затем [рисует сайт заново](#when-claude-code-redraws-without-being-asked).

### Рисование сетки цветных ячеек

Для тепловой карты, спарклайна или игровой доски в терминале нарисуйте один `Raster`, а не `Box` для каждой ячейки. `Raster` принимает `key`, его размер в `columns` и `rows`, и `cells` — строку base64, которая упаковывает каждую ячейку. Каждая ячейка — это три числа: кодовая точка символа, его цвет и цвет фона. Цвет — это 24-битное значение RGB в шестнадцатеричной записи, например `0xc62828` для красного. Значение `0x01000000`, на единицу выше этого диапазона, означает цвет терминала по умолчанию.

Приложения, кроме терминала, не имеют `Raster`, поэтому проверьте `e.surface` и нарисуйте текст там. Это тело панели рисует тепловую карту три на два:

```javascript theme={null}
// The value that means "use the terminal's default color"
const DEFAULT_COLOR = 0x01000000

// Pack rows of [character, color] pairs into the one string a Raster takes
// One cell is three numbers: the character's code point, its color, and its background
function cellsOf(rows) {
  const numbers = rows.flat().flatMap(([char, color]) => [char.codePointAt(0), color, DEFAULT_COLOR])
  return new Uint8Array(Uint32Array.from(numbers).buffer).toBase64()
}

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  // Draw only in the pane opened with the id 'heat'
  if (e.requestId !== 'heat') return next(e)
  const { Box, Text, Raster } = $.ui.resolve(e)
  // Two rows of three cells, each a block character and its color
  const rows = [
    [['█', 0x2e7d32], ['█', 0xf9a825], ['█', 0xc62828]],
    [['█', 0x2e7d32], ['█', 0x2e7d32], ['█', 0xf9a825]],
  ]
  if (e.surface !== 'terminal') {
    return Text({ children: ['The heat map needs the terminal.'] })
  }
  return Box({
    flexDirection: 'column',
    children: [Raster({ key: 'grid', columns: 3, rows: 2, cells: cellsOf(rows) })],
  })
})
```

В терминале панель показывает сетку:

![A pane in the terminal that holds a small grid of colored blocks, two rows of three. The top row is green, amber, and red. The bottom row is green, green, and amber.](https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-heat-map.svg?fit=max\&auto=format\&n=dgiVO_Od1X1faduV\&q=85\&s=b91bcce3bad74bc851149133d4acc5d5)

Массив `rows` — это часть, которую вы бы изменили, и `cellsOf` превращает его в упакованную строку. Хук рисует только в панели, чей `id` — это `heat`, поэтому откройте один с `$.ui.open({ id: 'heat' })` из команды, как пример [`hello-tabs`](#build-a-pane-with-tabs) открывает свою панель.

Каждый символ должен быть шириной в одну ячейку. Чтобы анимировать `Raster`, который уже на экране, вызовите `$.ui.blit` с `id` панели как `requestId`, `key` `Raster`, тем же размером и новыми ячейками. Для этого примера это `$.ui.blit({ requestId: 'heat', key: 'grid', columns: 3, rows: 2, cells: cellsOf(newRows) })`. Он перерисовывает только этот элемент без повторного запуска вашего хука `ui.render`.

## Ответ на нажатия и ввод

Когда пользователь нажимает кнопку, вводит текст в поле или выбирает из списка, который нарисовал ваш мод, Claude Code вызывает обратный вызов этого элемента управления, который выполняется в вашем модуле. Каждый элемент управления принимает свои собственные обратные вызовы:

* **`Button`**: принимает `onPress(e)`, где `e.surface` — это приложение, из которого пришло нажатие
* **`Input`**: принимает `onSubmit(value)` и `onInput(value)`
* **`Select`**: принимает `onSelect(value)` с его выборами в `options`, список по крайней мере одного выбора с уникальными значениями, такой как `[{ value: 'sm', label: 'Small' }, { value: 'lg', label: 'Large' }]`

### Каким элементам управления нужен `key`

Дайте каждому `Input` и `Select` проп `key`, например `key: 'size'`. `Button` может обойтись без `key`, если у него есть проп `label` или единственный строковый дочерний элемент. Тогда его ключом служит значение `label` или эта строка.

Тесты и другие моды определяют элемент управления по его ключу:

* **Тесты**: [тест](https://code.claude.com/docs/ru/plugins/mods/test.md#test-a-drawing) нажимает или вводит текст в элемент управления по его ключу.
* **Другие моды**: Claude Code запускает [`ui.press`, `ui.input` или `ui.select`](https://code.claude.com/docs/ru/plugins/mods/reference#interface) с ключом элемента управления в `e.element` до того, как выполнить обратный вызов этого элемента управления. Хук другого мода также может [выполняться для этого события](https://code.claude.com/docs/ru/plugins/mods/events.md#hook-other-mods-drawings-and-controls). Этот хук видит, что пользователь ввел в ваш `Input`, и может изменить этот текст или не дать вашему обратному вызову выполниться. API модов не дает этому моду метода для нажатия ваших кнопок.

Если сообщение говорит `needs a key` или `is drawn twice`, [найдите причину по этому сообщению](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#needs-a-key).

### Фокус клавиатуры и горячие клавиши

Ваш мод никогда не читает клавиатуру сам. Пользователь нажимает клавишу, Claude Code решает, для какого из ваших элементов управления она предназначена, и запускается обратный вызов этого элемента управления. Кроме [горячей клавиши цифры на полосе или привязки `action`](https://code.claude.com/docs/ru/plugins/mods/reference#elements), это происходит только пока ваша панель или полоса имеет фокус клавиатуры. Остальное время клавиши идут в промпт.

В [расширении VS Code](#draw-in-the-vs-code-extension) у кнопок нет горячих клавиш: пользователь щелкает по кнопке или нажимает на ней Enter и вводит текст в поля.

#### Как панель получает фокус клавиатуры

Панель получает фокус клавиатуры, когда:

* Ваш мод открывает ее с `focus: true` из команды или нажатия
* Пользователь нажимает Ctrl+X, затем Tab
* Пользователь щелкает по ней, для чего в терминале нужен [полноэкранный рендеринг](https://code.claude.com/docs/ru/fullscreen.md)

Claude Code предоставляет `focus: true` только пока промпт пуст и ничто другое не имеет фокус клавиатуры. Панель, которая открывается, пока пользователь печатает, не берет его нажатия клавиш.

#### Что делает каждая клавиша

Эта таблица перечисляет, что делает клавиша, пока ваша панель или полоса имеет фокус клавиатуры:

| Клавиша | Что она делает |
| :- | :- |
| Tab | Переходит к следующему элементу управления |
| Up и Down | Перемещаются между элементами управления, пока ваше рисование подходит. Когда панель или полоса имеет больше строк, чем может показать, они прокручивают ее. В `Input` в терминале они [перемещают между строками поля](https://code.claude.com/docs/ru/plugins/mods/gallery.md#input), а с его первой или последней строки переходят к элементу управления перед ним или после него. |
| Enter | Нажимает сфокусированный `Button`, отправляет сфокусированный `Input` или выбирает в `Select` |
| Горячая клавиша кнопки | Нажимает эту кнопку. Пока `Input` имеет фокус, каждая печатаемая клавиша идет в поле. |
| Page Up, Page Down, Home и End | Прокручивают вашу панель или полосу, когда в ней больше строк, чем она может показать |
| Ctrl+X, затем клавиша со стрелкой | Изменяет размер вашей панели. Left или Up дают ей больше места, а Right или Down возвращают место обратно. Панель рядом с транскриптом перестает расширяться на 45% ширины терминала. |
| Ctrl+X, затем X | Закрывает вашу панель, даже пока одно из ее полей имеет фокус |
| Ctrl+X, затем Ctrl+A | [Сворачивает полосу](#when-the-user-collapses-the-band) до одной строки, пока в ней рисует мод, или снова разворачивает ее. Эти клавиши работают и тогда, когда фокус находится в промпте. |
| Esc | Возвращает фокус клавиатуры в промпт. С `closeOnEscape: true`, он также закрывает панель. |

Мод не может привязать Tab или клавиши со стрелками к чему-либо еще, поэтому игра управляется с помощью `w`, `a`, `s` и `d`.

#### Установка горячей клавиши и первого фокуса

* **`hotkey`**: чтобы позволить пользователю нажать `Button` одной клавишей, дайте ему `hotkey` одной цифры или одной строчной буквы, как в `hotkey: 'a'`
* **`autoFocus`**: чтобы выбрать, какой элемент управления имеет фокус при открытии панели, добавьте `autoFocus: true` к нему. В [расширении VS Code](#draw-in-the-vs-code-extension) `autoFocus` ничего не делает: элемент управления рисуется так, как если бы вы его не указали, и вам не нужно ничего менять. Проп принимает только `true`, поэтому не указывайте его для остальных элементов управления.

То, как горячая клавиша показывается, зависит от кнопки и приложения:

| Кнопка | В терминале | В приложении Desktop | В расширении VS Code |
| :- | :- | :- | :- |
| С скобками, по умолчанию | `[ Add one ]`, без показанной горячей клавиши | Метка с маленькой клавишей рядом | Метка, а горячая клавиша ничего не делает |
| С `plain: true` | `1: One` | Метка с маленькой клавишей рядом | Метка, а горячая клавиша ничего не делает |

В терминале назовите клавишу в метке кнопки в скобках или используйте `plain: true`, чтобы пользователь мог видеть, что нажать. [Справка элементов](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements) имеет другие правила `Button`: `action`, горячие клавиши цифр на полосе и две кнопки на одной горячей клавише.

#### Когда пользователь сворачивает полосу

В терминале, пока мод рисует в полосе, пользователь может свернуть полосу до одной строки, чтобы она не мешала:

* **Щелкнуть `[-]`**: пока полоса развернута, Claude Code рисует эту отметку у правого края ее первой строки. В [полноэкранном рендеринге](https://code.claude.com/docs/ru/fullscreen.md) пользователь щелкает по ней, чтобы свернуть полосу.
* **Нажать Ctrl+X, затем Ctrl+A**: это работает независимо от того, где находится фокус клавиатуры — в промпте, в полосе или в панели. Пользователь может [привязать к этому другие клавиши](https://code.claude.com/docs/ru/keybindings.md#above-prompt-actions) через действие `abovePrompt:toggle`.

Свернутая полоса скрывает все, что моды рисуют в ней, и вместо этого показывает одну тусклую строку, в которой названы клавиши для ее разворачивания в соответствии с привязками пользователя:

```text theme={null}
▸ plugin panel hidden · ctrl+x ctrl+a or click to show
```

Те же клавиши, а в полноэкранном рендеринге — щелчок по этой строке, снова разворачивают полосу. До этого ничто не нажимает кнопки в ней: ни горячая клавиша, ни цифра, введенная в пустой промпт, ни сочетание клавиш для [`action`](https://code.claude.com/docs/ru/plugins/mods/reference#elements) кнопки. Если полоса имеет фокус клавиатуры в момент, когда пользователь ее сворачивает, фокус возвращается в промпт, а Ctrl+X, затем Tab пропускает полосу, пока она свернута.

Полоса остается свернутой, пока пользователь ее не развернет, даже после `/clear`, и снова разворачивается при следующем запуске Claude Code. Ваш мод не может развернуть ее. Не делайте полосу единственным местом, где ваш мод показывает то, на что пользователь должен ответить. Чтобы показывать это в другом месте только пока полоса свернута, читайте `e.props.isCollapsed` в вашем хуке `ui.render`, который продолжает выполняться. `isCollapsed` требует Claude Code v2.1.321 или новее.

### Получение введенного текста и рисование строки для каждого элемента

Многие панели — это текстовое поле со списком под ним. Пример в этом разделе — панель заметок: вы вводите заметку и нажимаете Enter, чтобы добавить ее, и каждая заметка имеет кнопку `x`, которая удаляет ее. С двумя добавленными заметками терминал рисует панель таким образом:

```text theme={null}
╭────────────────────────────────────────────────────────✕─╮
│ Note: Type a note and press Enter ⏎ add                  │
│ x buy milk │
│ x call bob │
╰──────────────────────────────────────────────────────────╯
```

`✕` на верхней границе — это собственная отметка Claude Code для закрытия панели.

Пример использует следующие техники:

* **Получение введенного текста**: `Input` вызывает `onSubmit(value)` с текстом поля, когда пользователь нажимает Enter, и `onInput(value)` при каждом изменении
* **Рисование списка**: отобразите ваши данные в одну строку каждый, и дайте каждой кнопке строки свой собственный `key`

Этот хук рисует содержимое панели:

```javascript theme={null}
// The list the pane draws
let notes = []

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  // Draw only in the pane opened with the id 'notes'
  if (e.requestId !== 'notes') return next(e)
  const { Box, Text, Button, Input } = $.ui.resolve(e)
  const redraw = () => $.ui.invalidate('ui.render')

  return Box({
    flexDirection: 'column',
    children: [
      Input({
        key: 'new-note',
        label: 'Note',
        placeholder: 'Type a note and press Enter',
        // The text the field starts with
        value: '',
        submitLabel: 'add',
        autoFocus: true,
        // Runs when you press Enter in the field
        onSubmit: async (value) => {
          // Ignore an empty line
          if (!value.trim()) return
          notes = [...notes, value.trim()]
          redraw()
          await $.store.set('notes', notes)
        },
      }),
      // One row for each note: a delete button, then the note's text
      ...notes.map((note, i) =>
        Box({
          flexDirection: 'row',
          columnGap: 1,
          children: [
            Button({
              // A key of its own, so each row's button can be told apart
              key: 'delete-' + i,
              label: 'x',
              plain: true,
              onPress: async () => {
                notes = notes.filter((_, j) => j !== i)
                redraw()
                await $.store.set('notes', notes)
              },
            }),
            Text({ children: [note] }),
          ],
        }),
      ),
    ],
  })
})
```

Чтобы попробовать панель:

* **Добавить заметку**: введите строку и нажмите Enter. Строка появляется как новая строка, и поле очищается.
* **Удалить заметку**: нажимайте Tab, пока кнопка `x` заметки не получит фокус, затем нажмите Enter. `x` — это метка кнопки, а не горячая клавиша, поэтому ввод буквы не нажимает ее.

Каждое изменение следует тому же циклу рендеринга, что и `hello-tabs`: обратный вызов изменяет `notes`, вызывает `redraw` и сохраняет список в `$.store`. Если ваш хук снова рисует панель, пока пользователь вводит заметку, поле сохраняет его текст, пока хук каждый раз передает одно и то же `value`. Чтобы заменить его текст своим, передайте другое `value`.

Пример сохраняет заметки и не загружает их. Чтобы вернуть их в следующей сессии, прочитайте их в хуке `session.start`, как `hello-tabs` читает `count`.

Следующие свойства составляют строку поля, `Note: Type a note and press Enter ⏎ add`:

| Свойство | В примере | Что это такое |
| :- | :- | :- |
| `label` | `Note` | Текст перед полем. Терминал рисует `: ` после него. |
| `placeholder` | `Type a note and press Enter` | Тусклый текст, который показывается, пока поле пусто |
| `value` | `''` | Текст, с которого начинается поле. Здесь он пуст, поэтому показывается `placeholder`. |
| `submitLabel` | `add` | Слово после `⏎`, которое говорит, что делает Enter |

Отправка `Input` не запускает ход, если ваш обратный вызов не вызывает [`$.prompt.submit`](https://code.claude.com/docs/ru/plugins/mods/api#start-a-turn-from-a-background-job).

## Перерисовка сайта

Рисование — это снимок: оно показывает то, что ваш хук `ui.render` вернул в последний раз, когда хук запустился. Чтобы показать что-то новое, хук должен запуститься снова. Claude Code запускает его снова для некоторых изменений, и ваш мод просит остальное.

### Когда Claude Code перерисовывает без запроса

Claude Code запускает ваш хук `ui.render` снова, когда пропсы сайта изменяются или ширина терминала изменяется. Когда `Client` в сайте завершается сбоем и ваш мод обрабатывает [`ui.fault`](https://code.claude.com/docs/ru/plugins/mods/reference#interface), Claude Code запускает хук ещё раз после того, как ваши хуки `ui.fault` вернут результат, чтобы ваш хук `ui.render` мог исключить этот `Client`. Он не запускает хук на таймере и не может сказать, когда переменная в вашем модуле изменяется.

### Перерисовка при изменении ваших данных

Чтобы ваши сайты были нарисованы снова после изменения ваших собственных данных, вызовите `$.ui.invalidate('ui.render')`. Эта панель считает нажатия. Обратный вызов кнопки изменяет `count`, затем просит перерисовку:

```javascript theme={null}
let count = 0

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  if (e.requestId !== 'counter') return next(e)
  const { Box, Text, Button } = $.ui.resolve(e)
  return Box({
    flexDirection: 'row',
    columnGap: 2,
    children: [
      Button({
        key: 'more',
        label: 'Add one',
        onPress: () => {
          count += 1
          // The data changed, so ask Claude Code to draw the pane again
          $.ui.invalidate('ui.render')
        },
      }),
      Text({ children: ['Count: ' + count] }),
    ],
  })
})
```

Каждое нажатие поднимает число в панели. Пример [`hello-tabs`](#build-a-pane-with-tabs) оборачивает тот же вызов в свою функцию `redraw`.

Значение, которое вы сохраняете в [`$.state`](#keep-a-value-in-\$-state), не нуждается в вызове, потому что написание значения перерисовывает сайты, которые его читают.

### Перерисовка на таймере

Чтобы сохранить часы, обратный отсчет или значение извне сессии в актуальном состоянии, перерисовывайте по расписанию. Запустите таймер в хуке `session.start` модуля. Если модуль уже имеет один, как `hello-tabs`, добавьте строку [`$.clock.every`](https://code.claude.com/docs/ru/plugins/mods/api#run-work-in-the-background) к нему:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  // Every 1000 milliseconds, ask Claude Code to draw your sites again
  $.clock.every(1000, () => $.ui.invalidate('ui.render'))
  return next(e)
})
```

Теперь Claude Code запускает ваш хук `ui.render` раз в секунду. Таймер останавливается после перезагрузки модуля, и новый экземпляр модуля запускает собственный таймер.

### Как часто сайт может перерисовываться

Claude Code ограничивает частоту перерисовок сайта, поэтому ваш мод может вызывать `$.ui.invalidate` так часто, как изменяются его данные. О том, как часто может перерисовываться каждый сайт, см. [таблицу лимитов](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits).

Вызовы, которые приходят быстрее, чем лимит, объединяются в одну перерисовку. Эта перерисовка запускает ваш хук один раз, и хук читает ваши данные такими, какие они есть в этот момент, поэтому показывается последнее значение и значения между ними не показываются. Анимация не может работать быстрее, чем лимит.

## Сохранение состояния

От того, где мод хранит значение, зависит, как долго оно существует: пока модуль не перезагрузится, пока сессия не закончится или от одной сессии к другой. Выбирайте по тому, как долго значение должно существовать:

| Сохраняйте это в | Это длится до | Используйте это для |
| :- | :- | :- |
| Переменная уровня модуля | Модуль перезагружается, что происходит каждый раз, когда вы сохраняете файл во время разработки | Значения, которые вы можете потерять, как `tab` в `hello-tabs` |
| `$.state` | Сессия заканчивается, или пользователь запускает `/clear`, `/resume` или `/branch` | Значения, от которых зависит отрисовка и которые должны пережить перезагрузку |
| `$.store` | Ваш мод удаляет его, или ни одна сессия не читает и не пишет в хранилище в течение [`cleanupPeriodDays`](https://code.claude.com/docs/ru/settings-reference#cleanupperioddays). Хранилище — это хранилище ключ-значение, сохраненное как собственный файл JSON вашего плагина в `~/.claude/plugins/store/`. | Настройки, история, все, что пользователь ожидает найти в следующий раз |

`$.store.get(key)` разрешается в значение или `undefined`, а `$.store.set(key, value)` принимает любое значение JSON.

### Сохранение значения в `$.state`

`$.state` хранит значения на протяжении сессии и выполняет перерисовку за вас. Это реактивное состояние: хук `ui.render`, который читает значение, подписывается на него, поэтому Claude Code перерисовывает это место каждый раз, когда вы записываете значение, и вам не нужно вызывать `$.ui.invalidate`. Значение в `$.state` также переживает перезагрузку модуля, чего переменная не делает.

Чтобы настроить его, объявите ваши значения, укажите в манифесте путь к объявлению, затем определите и используйте каждое значение. Примеры перемещают `count` из `hello-tabs` в `$.state`.

#### Объявление значений

Объявите значения в файле объявления типов. Внешний ключ — это имя вашего плагина, а каждая запись под ним — это значение и его тип. Сохраните это как `hello-tabs/types/index.d.ts`:

```typescript hello-tabs/types/index.d.ts theme={null}
declare module 'claude-code' {
  interface PluginState {
    'hello-tabs': {
      tab: 'one' | 'two'
      count: number
    }
  }
}
```

#### Указание манифеста на объявление

Чтобы `claude plugin validate` мог проверить ваш код по этому файлу, добавьте в манифест поле `types` с его путем:

```json hello-tabs/.claude-plugin/plugin.json theme={null}
{
  "name": "hello-tabs",
  "version": "0.1.0",
  "description": "Opens a pane with two tabs and a counter",
  "author": { "name": "Your Name" },
  "types": "./types/index.d.ts"
}
```

#### Определение, чтение и запись значения

В вашем модуле определите каждое значение со значением по умолчанию, прочитайте его при отрисовке и запишите его из обратного вызова. `atom` задает имя значения и его значение по умолчанию, `read` возвращает его, а `update` записывает его. Эти три помощника вызывают `$.state.get` и `$.state.set` за вас:

```javascript theme={null}
import { atom, read, update } from 'claude-code'

// At the top of the module: name the value and give its default
const count = atom({ plugin: 'hello-tabs', key: 'count' }, 0)

// In the ui.render hook: read the value to draw it
const n = await read($, count)

// In a Button: write a new value from the old one
onPress: () => update($, count, (value) => value + 1)
```

Поскольку хук `ui.render` прочитал `count`, Claude Code запускает хук снова каждый раз, когда кнопка записывает его.

К коду применяются следующие правила:

* **Пишите `plugin` и `key` как строковые литералы**: `claude plugin validate` читает их из вашего исходного кода
* **Храните результат каждого вызова `atom` в `const`**: если вы объявите `count` с помощью `let`, валидация завершится ошибкой `takes a source the scan can read`
* **Объявите каждое значение в файле объявления типов**: в противном случае валидация завершится ошибкой `hello-tabs.count is not declared`
* **Записывайте из обратного вызова или хука другого события**: хук `ui.render` может читать состояние, но не может записывать его, поэтому записывайте из `onPress`, `onSubmit` или хука для другого события

#### Изменение `hello-tabs` для использования `$.state`

Чтобы переместить `count` в `hello-tabs` в `$.state`, измените каждую строку, которая его использует:

* **В верхней части модуля**: добавьте строку `import` и замените `let count = 0` на строку `atom`
* **В хуке `ui.render`**: добавьте строку `read` перед `tabButton` и отрисуйте `'Count: ' + n` в `Text`
* **В кнопке Add one**: замените `onPress` на вариант из раздела [Сохранение из более чем одной сессии](#save-from-more-than-one-session), который сохраняет счетчик, а также записывает его
* **В хуке `session.start`**: замените две строки, которые читают `saved`, на вызов `loadCount` из раздела [Повторная загрузка сохраненного значения после `/clear`](#load-a-saved-value-again-after-clear)

Оставьте `redraw` для кнопок вкладок, потому что `tab` по-прежнему является переменной.

### Повторная загрузка сохраненного значения после `/clear`

Если ваш мод копирует сохраненное значение из `$.store` в `$.state` при `session.start`, он должен скопировать его снова после `/clear`, `/resume` или `/branch`. Эти команды сбрасывают каждое значение `$.state` к значению по умолчанию, а `session.start` повторно не срабатывает. [`classic.SessionStart`](https://code.claude.com/docs/ru/plugins/mods/events#hook-the-settings-hook-events) же срабатывает после каждой из них, с `e.source`, установленным в `clear`, `resume` или `fork`, поэтому скопируйте значение снова в хуке на это событие. В противном случае ваша отрисовка покажет значение по умолчанию, а обратный вызов, который сохраняет значение `$.state`, запишет значение по умолчанию поверх того, что вы сохранили.

Этот код загружает `count` из обоих хуков. Он основан на версии `hello-tabs` с `$.state`, где `count` — это атом, а `update` импортирован. Поместите `loadCount` выше `register` и добавьте вызов `loadCount` в уже имеющийся у вас хук `session.start`. `classic.SessionStart` также срабатывает при запуске и после сжатия контекста, которое не сбрасывает `$.state`, поэтому фильтр по `source` ограничивает хук тремя сбросами:

```javascript theme={null}
// Copy the saved count from $.store into $.state, or 0 if nothing is saved
async function loadCount($) {
  const saved = Number((await $.store.get('count')) ?? 0)
  await update($, count, () => saved)
}

// Runs before your first prompt, and again after a reload
on('session.start', async ($, e, next) => {
  await loadCount($)
  return next(e)
})

// Runs again after /clear, /resume, and /branch, which reports fork
on('classic.SessionStart', { source: ['clear', 'resume', 'fork'] }, async ($, e, next) => {
  await loadCount($)
  return next(e)
})
```

С обоими хуками панель показывает после `/clear` сохраненный счетчик, а не `0`, и следующее нажатие **Add one** прибавляет к сохраненному счетчику.

`loadCount` записывает сохраненное значение поверх того, что находится в `$.state`, а `session.start` срабатывает снова каждый раз, когда модуль перезагружается. Чтобы хранилище не отставало, сохраняйте при каждом изменении, как это делает кнопка **Add one**.

Чтобы проверить перезагрузку без сессии, [протестируйте отрисовку после `/clear`](https://code.claude.com/docs/ru/plugins/mods/test#test-a-drawing-after-clear).

### Сохранение из более чем одной сессии

Все сессии на вашем компьютере, которые запускают ваш мод, используют одно общее `$.store`. `get`, за которым следует `set`, не является атомарной операцией. Когда две сессии каждая читают значение, изменяют его и записывают обратно, возникает гонка, и вторая запись заменяет первую.

Чтобы сделать это менее вероятным:

* **Дайте каждому элементу собственный ключ**: `set` изменяет только свой ключ, поэтому сессии, которые записывают разные ключи, не перезаписывают друг друга
* **Читайте повторно прямо перед записью**: для значения, которое изменяют несколько сессий, выполните `get` для ключа в обратном вызове и сформируйте новое значение на его основе, а не на основе копии, загруженной при `session.start`. Запись другой сессии все равно будет потеряна, если она произойдет между вашими `get` и `set`.

Эта кнопка прибавляет единицу к тому, что сейчас содержится в хранилище, затем обновляет отрисовку:

```javascript theme={null}
onPress: async () => {
  // Read what the store holds now, which another session may have changed
  const saved = Number((await $.store.get('count')) ?? 0)
  // Save the new count, then show it
  await $.store.set('count', saved + 1)
  await update($, count, () => saved + 1)
}
```

Если вторая сессия нажала свою кнопку три раза с момента запуска этой сессии, это нажатие покажет и сохранит счетчик, который включает эти три нажатия.

## Следующие шаги

* [Реагирование на события](https://code.claude.com/docs/ru/plugins/mods/events.md): питайте ваше рисование из вызовов инструментов и ходов
* [Использование API модов](https://code.claude.com/docs/ru/plugins/mods/api.md): питайте ваше рисование из таймеров и вызовов модели
* [Тестирование рисования](https://code.claude.com/docs/ru/plugins/mods/test.md#test-a-drawing): нажимайте ваши кнопки из теста, на более чем одной поверхности
* [Сайты рендеринга](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) и [элементы](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements): свойства каждого сайта и свойства каждого элемента
