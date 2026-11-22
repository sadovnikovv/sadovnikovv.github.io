> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Тестирование мода

> Напишите автоматизированные тесты для мода Claude Code, которые вызывают события, подменяют ответы Claude Code и нажимают кнопки, без сессии, входа или сети.

Вы можете написать автоматизированные тесты для мода и запустить их из оболочки с помощью [`claude plugin test`](https://code.claude.com/docs/ru/plugins/mods/reference#commands). Тест вызывает события, которые обрабатывают ваши хуки, и проверяет, что сделали хуки, чтобы вы поймали проблему до того, как она попадёт в сессию. Первый пример тестирует мод из раздела [Создание мода](https://code.claude.com/docs/ru/plugins/mods/create.md).

## Напишите тест

Тест загружает ваш мод, отправляет события через его hooks так, как это делал бы Claude Code, и проверяет, что сделали hooks, без сеанса, входа или сети. Вы запускаете тесты из своей оболочки с помощью `claude plugin test`, и каждый файл теста импортирует набор для тестирования, библиотеку тестирования в модуле `claude-code/testing`.

Дайте каждому файлу теста имя, заканчивающееся на `.test.ts`, например `first-mod.test.ts`, и сохраните его где угодно в директории плагина. Каждый файл теста должен содержать по крайней мере один `test()`, иначе запуск завершится с ошибкой `declares no test(): nothing ran`. Файл теста может импортировать собственные файлы вашего мода и вспомогательные файлы `.ts` соседних уровней, поэтому вы можете модульно тестировать простые функции, такие как правила игры, без набора.

Этот тест выполняет два вызова инструментов, запускает команду `/tally` из [Create a mod](https://code.claude.com/docs/ru/plugins/mods/create.md) и проверяет, что ответ учитывает оба. Его первая строка — это [stub](#stub-what-claude-code-would-answer), который отвечает на вызовы инструментов вместо Claude Code. Сохраните его как `first-mod/tests/first-mod.test.ts`:

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

В вашей оболочке запустите тесты из директории `first-mod`:

```bash theme={null}
claude plugin test
```

Вывод называет каждый тест и прошёл ли он, с временем выполнения, которое варьируется от запуска к запуску:

```text theme={null}
tests/first-mod.test.ts:
(pass) /tally reports the tool calls the mod has seen [22.87ms]

 1 pass
 0 fail
Ran 1 test across 1 file. [0.19s]
```

Каждый `$.tool.call` прошёл через hook [`tool.call`](https://code.claude.com/docs/ru/plugins/mods/reference#tools) вашего мода, который добавил один к его счётчику и передал вызов дальше stub. Никакой `ls` не запустился и никакой файл не был прочитан. `$.command.run` затем перешёл к hook [`command.run`](https://code.claude.com/docs/ru/plugins/mods/reference#commands-and-configuration) вашего мода, и `answer` — это объект, который вернул этот hook.

Команда выходит со статусом 1, когда тест не пройден, поэтому она работает в CI. Если ваши собственные моды не могут загружаться в оболочке, которая её запускает, она выводит строку, начинающуюся с `claude plugin test: hooks modules are turned off` с причиной и выходит со статусом 1.

### Stub что Claude Code ответит бы

В тесте не запускаются модель, хранилище или инструмент, поэтому везде, где ваш мод ожидает ответ от Claude Code, тест предоставляет ответ с помощью stub. Функция теста получает два аргумента для этого:

* **`$`**: собственный `$` теста, который действует как Claude Code. Это не [mods API](https://code.claude.com/docs/ru/plugins/mods/reference.md#mods-api-methods), который получает хук. Каждый из его методов вызывает событие с тем же именем, отправляет его через хуки вашего мода и разрешается в результат: `$.tool.call({ tool: 'Bash', command: 'ls' })` вызывает `tool.call`. `$.command.run`, `$.prompt.submit`, `$.session.start` и `$.turn.complete` работают так же, а `$.classic.Stop` и другие методы `$.classic` вызывают [событие хука настроек](https://code.claude.com/docs/ru/plugins/mods/events.md#hook-the-settings-hook-events). Тест не может напрямую вызвать метод mods API, такой как `ui.close`. Вызовите его через ваш мод, например нажав кнопку, которая закрывает панель.
* **`on`**: вызовите её для регистрации stub, которые являются hooks, отвечающими в место Claude Code. Назовите stub для вызова mods API без `$.`, поэтому stub, зарегистрированный как `store.get`, отвечает на `$.store.get` вашего мода. Когда ваш мод вызывает [`$.model.complete`](https://code.claude.com/docs/ru/plugins/mods/api#call-a-model) или [`$.store.get`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state), stub предоставляет ответ.

Этот пример stub вызова модели. Hook принадлежит моду с именем `grader` и обрабатывает команду `/grade`, которая отправляет предложение модели и сообщает, начинается ли ответ с `PASS`. Файл содержит только hook под тестом, поэтому моду также нужны `plugin.json` и `hooks.json`, как в [Create a mod](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself). Чтобы ввести `/grade` в сеансе, моду также нужно [зарегистрировать команду](https://code.claude.com/docs/ru/plugins/mods/api.md#add-a-command):

```javascript grader/hooks/register.js theme={null}
export function register(on) {
  on('command.run', { command: 'grade' }, async ($, e) => {
    // e.args is the text typed after /grade
    const reply = await $.model.complete({
      model: 'haiku',
      system: 'Grade the sentence. Start your reply with PASS or FAIL.',
      prompt: e.args,
    })
    const passed = reply.isAnswered && reply.text.startsWith('PASS')
    return { text: passed ? 'Passed' : 'Try again' }
  })
}
```

Этот тест stub вызова модели для проверки того, что делает hook с проходящим ответом:

```typescript grader/tests/grader.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

test('a passing grade is reported', async ($, on) => {
  // Answer the mod's $.model.complete call with a fixed reply, so no model runs
  on('model.complete', () => ({
    value: {
      isAnswered: true,
      text: 'PASS\nNice sentence.',
      usage: { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 },
    },
  }))

  // Run /grade, which makes the mod call the model
  const answer = await $.command.run({ command: 'grade', args: 'The cat sat on the mat.' })
  expect(answer.text).toBe('Passed')
})
```

Тест проходит, потому что `reply` hook — это объект под `value`, чей `text` начинается с `PASS`. Чтобы проверить другую ветвь, добавьте второй тест, чей stub возвращает `text`, начинающийся с `FAIL`, и ожидайте `Try again`.

Stub для вызова mods API возвращает объект с полем `value`, которое содержит то, во что разрешается вызов в вашем моде: `{ value: 7 }` заставляет `$.store.get` разрешиться в `7`. Stub для одного из событий Claude Code, такого как [`turn.step`](https://code.claude.com/docs/ru/plugins/mods/reference#turns) или `tool.call`, возвращает собственный результат этого события, такой как `{ result: 'ok' }`. `$.session.send` и `$.prompt.fill` также принимают результат своего события, как показано в таблице. [Look up what a stub returns](#look-up-what-a-stub-returns) показывает, какую форму принимает каждое распространённое имя. Следующие ошибки означают, что stub неправильный или отсутствует. Вывод непройденного теста включает блок с заголовком `the engine reported:`, и каждая ошибка появляется там:

* `returned neither { value } nor { deny }`: stub для вызова mods API вернул простое значение, из-за чего тест не проходит
* `no implementation for` с последующим именем: ваш мод сделал этот вызов и никакой stub не отвечает на него

Набор также экспортирует готовые mock для часов, хранилища, переменных окружения и строк, добавляемых в диалог:

* **`mock.clock(on)`**: отвечает на [`$.clock`](https://code.claude.com/docs/ru/plugins/mods/api#run-work-in-the-background) и возвращает mock часов, которые ваш тест продвигает, поэтому тест таймера не ждёт.
* **`mock.store(on, { count: 7 })`**: отвечает на `$.store` из хранилища, которое начинается с этих записей. Он ничего не возвращает, поэтому чтобы проверить, что сохранил ваш мод, напишите два `store` stub сами, как это делает [drawing test](#test-a-drawing).
* **`mock.env(on, { CI: 'true' })`**: отвечает на `$.env.get` из этих переменных.
* **`mock.session(on)`**: возвращает mock сессии, чей метод `appended()` перечисляет строки, добавленные вашим модом с помощью [`$.session.append`](https://code.claude.com/docs/ru/plugins/mods/reference#session), начиная с самых старых; требуется Claude Code v2.1.293 или новее.

### Следуйте правилам набора для тестирования

* **Зарегистрируйте каждый stub перед первым вызовом теста на `$`.** Вызов `on` после этого выбрасывает ошибку, такую как `on("ui.render") after the test first called $`.

* **[`session.start`](https://code.claude.com/docs/ru/plugins/mods/reference#session) не запускается сам по себе.** Каждый тест начинается со свежезагруженного модуля, ни один из хуков которого ещё не вызван, поэтому переменные уровня модуля содержат свои начальные значения. Если хук зависит от того, что настраивает `session.start`, сначала вызовите это событие:

  ```typescript theme={null}
  // Answer the event after your hook passes it on with next(e)
  on('session.start', () => ({ cwd: '/work' }))
  // Answer the $.command.register call your hook makes
  on('command.register', () => ({ value: undefined }))
  // Fire the event, which runs your session.start hook
  await $.session.start({ surface: 'terminal', isInteractive: true, cwd: '/work' })
  ```

  Второй stub отвечает на вызов `$.command.register`, который делает hook `session.start`, такой как [tutorial's](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself). Без него этот вызов отклоняется с `no implementation for command.register` и набор пропускает ваш hook, поэтому ничего после вызова в hook не запускается. Тест не завершается неудачей в этой точке. Пропущенный hook указан под `the engine reported:` только если позже проверка завершится неудачей.

* **Зарегистрируйте stub для `ui.render`, чтобы выбрать, что возвращает `next(e)`.** Когда ваш хук [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface) возвращает `next(e)`, например чтобы ничего не рисовать, пока Claude неактивен, [монтирование](#test-a-drawing) проходит успешно и без stub. Чтобы `next(e)` возвращал выбранный вами элемент, зарегистрируйте stub, который возвращает его как простые данные:

  ```typescript theme={null}
  // Stands for what Claude Code would draw at the site
  on('ui.render', () => ({ type: 'Text', props: {}, children: ['drawn by Claude Code'] }))
  ```

  Там, где место [может отрисовать этот элемент](https://code.claude.com/docs/ru/plugins/mods/interface.md#change-what-claude-code-already-draws), `ui.find({ type: 'Text' })` возвращает его, когда ваш хук вернул `next(e)`. В v2.1.323 или новее для полосы (band) передайте имя вашего мода вторым аргументом в `on`, как в `{ plugin: 'my-mod' }`. Без него stub не отвечает на ваш `next(e)`. До v2.1.321 монтирование завершается неудачей с `no implementation for ui.render`, если только вы не зарегистрируете stub.

* **Stub для `turn.step` — это асинхронный генератор**, и тест читает поток до конца, чтобы получить результат:

  ```typescript theme={null}
  on('turn.step', async function* ($, e) {
    // Each yield is one piece of the model's streamed reply
    yield { kind: 'text', index: 0, text: 'ok' }
    // The return value is the result of the whole request
    return { turnId: e.turnId, index: e.index, answer: 'ok', toolUses: [], stopReason: 'end_turn', usage: null }
  })

  // Fire one request to the model, which runs your turn.step hook
  const stream = $.turn.step({ turnId: 't', index: 0, model: 'claude-test', messageCount: 1 })
  // Read every piece until the stream says it's done
  let step = await stream.next()
  while (step.done !== true) step = await stream.next()
  const result = step.value
  ```

  Когда цикл заканчивается, `result` — это объект, который вернул stub, после того как ваш hook `turn.step` имел возможность его изменить. Здесь `result.answer` — это `'ok'`.

* **Выполняйте вызов инструмента, передавая имя инструмента и аргументы как поля**, например `await $.tool.call({ tool: 'Bash', command: 'ls' })`, и зарегистрируйте stub `tool.call`, который возвращает `{ result }`.

### Посмотрите, что возвращает stub

Каждый вызов mods API, который ваш мод делает в тесте, нуждается в stub, который отвечает вместо Claude Code, кроме нескольких, на которые набор отвечает сам: вызовы [`$.ui.invalidate`](https://code.claude.com/docs/ru/plugins/mods/interface#redraw-when-something-changes), [`$.state`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state) и `$.session.append`. Для вызовов `$.clock` используйте `mock.clock(on)`, иначе `$.clock.now()` вашего мода завершится неудачей с `no implementation for clock.now`.

Эта таблица перечисляет те, которые моды используют чаще всего. Первый столбец — это вызов, который делает ваш мод, или событие, которое он передаёт с `next(e)`. Второй — это функция для передачи `on` под этим именем, поэтому строка `$.store.get` становится `on('store.get', ($, e) => ({ value: saved.get(e.key) }))`. `'...'` в stub отмечает текст для вас, чтобы заполнить:

| Ваш мод вызывает или передаёт | Stub |
| :- | :- |
| `$.command.register`, `$.tool.register`, `$.ui.toast`, `$.ui.log`, `$.ui.status`, `$.ui.close`, `$.store.set` | `() => ({ value: undefined })`. Для `ui.toast` и `ui.log` текст — это `e.text`. |
| `$.store.get` | `($, e) => ({ value: saved.get(e.key) })` |
| `$.fs.read` | `($, e) => ({ value: e.path.endsWith('notes.md') ? '# Notes' : '' })`. `e.path` приходит как абсолютный путь, поэтому сравнивайте с `endsWith`. |
| `$.ui.open` | `() => ({ value: { isPlaced: true } })` |
| `$.ui.ask` | Stub `tool.call`, потому что вопрос достигает его как вызов инструмента `AskUserQuestion`: `($, e) => ({ result: { answers: { [e.questions[0].question]: 'Run it' } } })`. Сначала проверьте `e.tool`, если ваш мод передаёт другие tool call. |
| `$.model.complete` | `() => ({ value: { isAnswered: true, text: '...', usage } })` |
| `$.process.run` | `($, e) => ({ value: { exitCode: 0, stdout: '...', stderr: '' } })`. `e.argv` — это список аргументов и `e.init` содержит `cwd` и `timeoutMs`. |
| Любой вызов mods API, который должен завершиться неудачей | `() => ({ deny: 'the reason' })`, что делает вызов отклонённым в вашем моде. Stub, который выбрасывает, пропускается вместо этого. |
| `session.start` | `() => ({ cwd: '/work' })` |
| `turn.start` | `($, e) => ({ turnId: e.turnId })` |
| `tool.call` | `() => ({ result: '...' })` |
| `turn.complete` | `() => ({ text: '' })`. Вызывайте его с помощью `$.turn.complete({ turnId, answer, durationMs, isAborted: false, usage: null })`. |
| `prompt.submit` | `($, e) => ({ text: e.text })` |
| `prompt.fill` | `() => ({ isFilled: true })` |
| `$.prompt.read` | `() => ({ value: { text: '...', cursor: 0 } })` |
| `$.ui.copy` | `() => ({ value: { isCopied: true } })` |
| `$.ui.notify` | `() => ({ value: { isSent: true, channel: 'terminal_bell' } })`. Текст — это `e.text`, а заголовок — `e.title`. |
| `$.session.messages` | `() => ({ value: [{ role: 'assistant', text: '...', toolUses: [] }] })` |
| `$.session.id`, `$.agent.list` | `() => ({ value: 'abc123' })`, `() => ({ value: [] })` |
| `session.send` | `() => ({ isDelivered: true })`. `e.to` приходит как строка даже когда ваш мод передал `{ sessionId }`. |
| `session.receive` | `($, e) => ({ text: e.text })`. Вызывайте его с помощью `$.session.receive({ origin: { kind: 'peer-send-message' }, text })`. |
| `ui.render` | `() => ({ type: 'Text', props: {}, children: ['...'] })`. Для полосы (band) см. matcher в разделе [Следуйте правилам набора для тестирования](#follow-the-test-kit’s-rules). |

### Проверьте результат с помощью `expect`

У `expect` есть собственный набор утверждений, например `toEqual` и `toHaveLength`, которые ставятся после проверяемого значения, как в `expect(answer.text).toBe('ok')`. Полный список можно найти, поискав `type Matchers` в файле `claude-code/index.d.ts` среди [типов для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build). Поставьте `.not` перед утверждением, чтобы проверить обратное. Чтобы проверить, с чем завершается промис, поставьте `.resolves` или `.rejects` сразу после `expect(...)` и используйте `await` для этой строки, как в `await expect(promise).rejects.toThrow()`.

Когда `expect` не выполняется внутри stub или хука, который вы передали в `on` как обычную функцию, а не как асинхронный генератор, тест не проходит. Движок пропускает этот хук, а вывод ошибки называет его, например `in the test's store.set hook`.

## Тестируйте таймер

Мод, который запускает работу на таймере, нуждается в clock, который тест контролирует, поэтому тест может продвигать время вперёд вместо ожидания. `const clock = mock.clock(on)` возвращает mock clock, который начинается с `0` и движется только когда ваш тест его движет. Чтобы начать в другое время, передайте его в миллисекундах, как в `mock.clock(on, { now: 5000 })`. Clock имеет эти методы:

| Метод | Что он делает |
| :- | :- |
| `await clock.advance(1000)` | Продвигает время вперёд на столько миллисекунд и запускает каждый таймер, который наступает |
| `await clock.set(5000)` | Продвигает время вперёд до этого значения, как `advance` |
| `clock.now()` | Возвращает время, которое разрешает `$.clock.now()` вашего мода |
| `await clock.settle()` | Запускает таймеры, которые уже наступили, такие как цепь нулевой задержки `$.clock.after` вызовов, без продвижения времени |
| `await clock.sleep(2000)` | Внутри stub, делает этот stub ответом только после того, как тест продвинулся так далеко, что это то, как вы имитируете медленную модель или процесс |

Этот hook принадлежит моду с именем `countdown` и обрабатывает команду `/countdown`, которая принимает количество секунд, запускает таймер `$.clock.every` в одну секунду и показывает toast на нуле. Как с `grader`, файл содержит только тестируемый hook и не регистрирует команду:

```javascript countdown/hooks/register.js theme={null}
export function register(on) {
  on('command.run', { command: 'countdown' }, async ($, e) => {
    // e.args is the text typed after /countdown
    let left = Number(e.args)
    const timer = $.clock.every(1000, () => {
      left -= 1
      if (left === 0) {
        timer.cancel()
        $.ui.toast('Time is up')
      }
    })
    // Print nothing in the transcript
    return {}
  })
}
```

Этот тест запускает `/countdown 3` и движет mock clock, поэтому он проверяет три секунды поведения без ожидания трёх секунд:

```typescript countdown/tests/countdown.test.ts theme={null}
import { expect, mock, test } from 'claude-code/testing'

test('the countdown ends with a toast', async ($, on) => {
  // Answer every $.clock call from a clock the test controls
  const clock = mock.clock(on)
  // Collect the text of each toast the mod shows
  const toasts: string[] = []
  on('ui.toast', ($, e) => {
    toasts.push(e.text)
    return { value: undefined }
  })

  await $.command.run({ command: 'countdown', args: '3' })
  // After two seconds the timer has fired twice, and no toast is due
  await clock.advance(2000)
  expect(toasts).toEqual([])
  // The third second brings the count to zero
  await clock.advance(1000)
  expect(toasts).toEqual(['Time is up'])
})
```

Первый `expect` показывает, что toast не приходит рано, и второй показывает, что он приходит один раз. Каждый `advance` разрешается после того, как таймеры, которые наступили, запустились, поэтому проверка на следующей строке видит их эффект.

## Тестируйте рисунок

Тест может нарисовать один из [render sites](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) вашего мода, затем нажать, ввести текст в и найти элементы, которые он нарисовал. `$.ui.mount` рисует сайт через hook `ui.render` вашего мода и возвращает handle с методом для каждого из них. Чтобы охватить несколько приложений в одном тесте, установите `surface` на приложение для рисования. Этот тест открывает панель из [Build a pane with tabs](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-pane-with-tabs), переключает вкладки, нажимает кнопку и проверяет счётчик в терминале и приложении Desktop:

```typescript hello-tabs/tests/hello-tabs.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

// What Claude Code passes to a ui.render hook for this pane, apart from the app
const PANE = {
  plugin: 'hello-tabs',
  component: 'Pane',
  requestId: 'hello-tabs',
  viewport: { columns: 100, rows: 30 },
  props: {
    title: 'Hello tabs',
    isFocused: true,
    bodyColumns: 60,
    placement: 'inline',
    scroll: { offset: 0, bodyRows: 10 },
    view: {},
  },
} as const

test('the second tab counts presses and saves the count', async ($, on) => {
  // Stub $.store with a Map, so the test can read what the mod saved
  const saved = new Map<string, unknown>()
  on('store.get', ($, e) => ({ value: saved.get(e.key) }))
  on('store.set', ($, e) => {
    saved.set(e.key, e.value)
    return { value: undefined }
  })

  // Draw the pane once for each app
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    // Press the buttons by the key the mod gave them
    await ui.press({ key: 'tab-two' })
    await ui.press({ key: 'more' })
    // The second tab's count line is in the drawing
    expect(await ui.find({ type: 'Text', text: /^Count: \d+$/ })).toBeDefined()
    await ui.unmount()
  }

  // One press in each app makes two
  expect(saved.get('count')).toBe(2)
})
```

В вашей оболочке запустите `claude plugin test` из директории `hello-tabs`. Тест проходит, когда оба приложения рисуют строку счётчика и мод сохранил `2`. Счётчик переносится из первого приложения во второе, потому что оба mount используют один и тот же загруженный модуль.

Handle, который возвращает `$.ui.mount`, имеет эти методы, которые адресуют элементы по `key`, который вы им дали:

| Метод | Что он делает |
| :- | :- |
| `press({ key: 'more' })` | Нажимает `Button` с этим key |
| `input({ key: 'new-note', text: 'buy milk' })` | Вводит текст в `Input` с этим key и нажимает Enter. Добавьте `kind: 'change'` для ввода без отправки. Для поля с `rows` текст может содержать `\n`. |
| `select({ key: 'size', value: 'large' })` | Выбирает опцию с этим значением в `Select` с этим key |
| `keepsBeneath()` | В тесте без заглушки `ui.render` разрешается в `true`, когда рисунок включает то, что вернул `next(e)`, и в `false`, когда ваш хук это опустил. В тесте, который регистрирует такую заглушку, используйте `find`, чтобы найти то, что нарисовала заглушка. Требуется Claude Code v2.1.321 или новее. |
| `find({ key: 'more' })` или `find({ type: 'Text', text: 'Count: 2' })` | Возвращает первый совпадающий элемент как `{ type, props, children }` или `undefined`. `text` может быть строкой или регулярным выражением. |
| `unmount()` | Удаляет рисунок |

Каждый метод разрешается после того, как ваш обработчик завершился, поэтому вы можете проверить результат на следующей строке. Установите `props` на то, что Claude Code передал бы для этого сайта. Таблица [render sites](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites) перечисляет props каждого сайта, и [типы для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build) имеют их типы.

Чтобы обнаружить [дерево элементов](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-tree-from-elements), которое недопустимо для приложения, указанного в `surface`, проверьте с помощью `find` наличие элемента, который добавляет ваш хук. Тест не проверяет, как приложение отрисовывает дерево, поэтому также посмотрите новый макет в реальной сессии.

### Тестируйте рисунок после `/clear`

Каждый тест начинается с каждого значения `$.state` на его значении по умолчанию, что то, как `/clear` их оставляет. Чтобы тестировать, что делает ваш мод дальше, пропустите `session.start`, вызовите `classic.SessionStart` с `source: 'clear'` и проверьте, что рисует ваш мод.

Этот тест проверяет модуль из [Load a saved value again after `/clear`](https://code.claude.com/docs/ru/plugins/mods/interface#load-a-saved-value-again-after-clear). Добавьте его в файл из [Test a drawing](#test-a-drawing), где определён `PANE`. Первый тест этого файла ожидает, что кнопка сохранит счётчик, как кнопка в [Save from more than one session](https://code.claude.com/docs/ru/plugins/mods/interface.md#save-from-more-than-one-session):

```typescript hello-tabs/tests/hello-tabs.test.ts theme={null}
test('the saved count comes back after /clear', async ($, on) => {
  // The store already holds a count of 7
  on('store.get', () => ({ value: 7 }))
  // Answer the event after your hook passes it on with next(e)
  on('classic.SessionStart', () => ({}))

  // Fire the event that follows /clear, which runs your hook
  await $.classic.SessionStart({ source: 'clear' })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  await ui.press({ key: 'tab-two' })
  // The pane shows the stored count, not the default of 0
  expect(await ui.find({ type: 'Text', text: 'Count: 7' })).toBeDefined()
})
```

Тест проходит, когда ваш hook `classic.SessionStart` скопировал сохранённый `7` в `$.state` перед тем, как панель нарисовалась. Без этого hook в вашем модуле, панель рисует `Count: 0`, `find` возвращает `undefined` и тест завершается неудачей на `toBeDefined`.

## Тестируйте мод политики

Мод, который ваша организация перечисляет в [`prependPlugins`](https://code.claude.com/docs/ru/plugins/mods/admin), может отказать другому моду перед его загрузкой. Чтобы тестировать один, установите уровень вашего мода и дайте тесту второй мод для вашего, чтобы допустить или отказать:

* **`tier`**: вызовите его один раз в верхней части файла теста, как в `tier('prepend')`, чтобы загрузить ваш мод как `prepend`, `append` или `builtin`, его место в [порядке запуска модов](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in). Без него ваш мод загружается как `user`.
* **`plugins`**: передайте `test` объект опций перед телом теста. Его массив `plugins` содержит моды, которые вы пишете встроенными, каждый с `name` и функцией `register`. Чтобы загрузить один где-то кроме `user`, добавьте `tier` к нему.

Этот файл теста первым загружает [мод политики со страницы администратора](https://code.claude.com/docs/ru/plugins/mods/admin.md#enforce-a-policy-with-a-mod-of-your-own). Он проверяет, что мод политики останавливает мод, который запускает процесс, и допускает тот, который не запускает:

```typescript acme-guard/tests/guard.test.ts theme={null}
import { expect, test, tier } from 'claude-code/testing'

// Load the mod under test ahead of every other mod
tier('prepend')

// A second mod whose code calls $.process.run, which the policy blocks
const runner = {
  name: 'runner',
  register(on) {
    on('tool.call', async ($, e, next) => {
      await $.process.run(['ls'])
      return { result: 'runner answered' }
    })
  },
}

// A second mod that calls nothing the policy blocks
const reader = {
  name: 'reader',
  register(on) {
    on('tool.call', async ($, e, next) => {
      return { result: 'reader answered' }
    })
  },
}

test('refuses a mod that starts a process', { plugins: [runner] }, async ($, on) => {
  on('tool.call', () => ({ result: 'claude code answered' }))
  let message = ''
  try {
    // The first call on $ loads the mods, so the refusal is thrown here
    await $.tool.call({ tool: 'Bash', command: 'ls' })
  } catch (error) {
    message = error.message
  }
  // "hooks module left out" on v2.1.326 or later, "refused" on earlier versions
  expect(message).toMatch(/^runner: (hooks module left out|refused) by acme-guard/)
})

test('admits a mod that starts no process', { plugins: [reader] }, async ($, on) => {
  on('tool.call', () => ({ result: 'claude code answered' }))
  const out = await $.tool.call({ tool: 'Bash', command: 'ls' })
  // The answer comes from reader, which shows that it loaded
  expect(out).toEqual({ result: 'reader answered' })
})
```

В вашей оболочке запустите `claude plugin test` из директории `acme-guard`. Оба теста проходят с policy mod, как показано на странице admin.

Kit загружает каждый мод при первом вызове теста на `$`. Когда ваш мод останавливает один из них, этот вызов выбрасывает исключение, и в сообщении названы оба мода. Во втором тесте ничего не остановлено, поэтому `reader` отвечает на вызов инструмента до того, как он достигнет заглушки.

## Следующие шаги

* [Troubleshoot a mod](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md): узнайте, почему мод ничего не делает в сеансе
* [Mods reference](https://code.claude.com/docs/ru/plugins/mods/reference.md): каждое событие input и result для написания stubs
