> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Реагировать на события с помощью мода

> Обрабатывайте события Claude Code из мода: наблюдайте, переписывайте или отвечайте на вызовы инструментов, подсказки и ходы, фильтруйте события, которые обрабатывает hook, и планируйте для других модов.

Hook — это обработчик события: функция, которую Claude Code запускает при возникновении именованного события. Claude Code генерирует событие в каждой точке, где он собирается действовать, например, когда он запускает инструмент, отправляет подсказку, отправляет запрос к модели или начинает или завершает сеанс. Ваш hook запускается перед тем, как Claude Code действует, поэтому он может наблюдать событие, переписать его или ответить на него вместо Claude Code. Вы регистрируете hook с помощью [`on(eventName, handler)`](https://code.claude.com/docs/ru/plugins/mods/reference#the-hook-function).

Создайте свой [первый мод](https://code.claude.com/docs/ru/plugins/mods/create.md) перед тем, как начать здесь. Для каждого события и его точных полей см. [справочник](https://code.claude.com/docs/ru/plugins/mods/reference.md#events) или прочитайте [типы для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build).

## Как hook обрабатывает событие

Hook находится между событием и тем, что Claude Code сделает с ним, поэтому он может наблюдать событие, переписать его или ответить на него сам. Он получает три аргумента: [mods API](https://code.claude.com/docs/ru/plugins/mods/api.md) как `$`, событие как `e` и следующий обработчик как `next`. Обработчики события образуют цепочку middleware. `next(e)` вызывает следующий обработчик, который является hook другого мода или, в конце цепочки, собственным поведением Claude Code, и разрешается в результат. То, что ваш hook делает с `next`, определяет, какой из трёх вариантов он выполняет.

### Наблюдать событие

Чтобы наблюдать событие без его изменения, выполните свою работу и верните `next(e)`. Этот hook регистрирует каждый инструмент, который Claude собирается использовать:

```javascript theme={null}
on('tool.call', async ($, e, next) => {
  // Запускается перед запуском инструмента
  $.ui.log('Claude is about to use ' + e.tool)
  // Передайте событие дальше без изменений
  return next(e)
})
```

Перед запуском каждого инструмента в расшифровке появляется тусклая строка, такая как `● my-mod: Claude is about to use Bash`, где `my-mod` — это имя вашего плагина. Инструмент запускается так же, как без мода.

Чтобы действовать после события, `await next(e)`, выполните свою работу и верните результат. Этот hook регистрирует каждый инструмент после его запуска:

```javascript theme={null}
on('tool.call', async ($, e, next) => {
  // Позвольте инструменту запуститься и дождитесь его результата
  const result = await next(e)
  // Запускается после запуска инструмента
  $.ui.log(e.tool + ' finished')
  // Верните результат без изменений
  return result
})
```

Строка теперь появляется после завершения каждого инструмента. Claude читает один и тот же результат в любом случае, потому что hook возвращает то, в чём разрешился `next(e)`.

### Переписать событие

Чтобы изменить то, на что действует Claude Code, например текст промпта, вызовите `next` с изменённой копией события. Само событие неизменяемо: оно заморожено на каждой глубине, и присваивание полю выбрасывает исключение. Этот хук обрезает каждый промпт перед его отправкой:

```javascript theme={null}
on('prompt.submit', async ($, e, next) => {
  // Передайте копию события с изменённым текстом
  return next({ ...e, text: e.text.trim() })
})
```

Более поздние обработчики и Claude Code получают обрезанную подсказку и никогда не видят оригинал. Вы также можете изменить результат: `await next(e)`, затем верните копию результата с заменённым полем.

### Ответить на событие

Чтобы обработать событие самостоятельно, верните результат без вызова `next`. Это короткозамыкает цепочку, поэтому более поздние моды и собственное поведение Claude Code не запускаются. Этот hook отказывает в каждой команде Bash:

```javascript theme={null}
on('tool.call', { tool: 'Bash' }, async () => {
  // Нет вызова next, поэтому команда никогда не запускается
  return { deny: 'Bash is turned off in this project. Use the file tools.' }
})
```

Когда Claude пытается выполнить команду Bash, команда не запускается, и Claude читает текст `deny` как результат инструмента. Каждое событие имеет свою форму результата, которую [справочник событий](https://code.claude.com/docs/ru/plugins/mods/reference.md#events) перечисляет.

### Фильтровать события, которые обрабатывает hook

Чтобы запустить hook только для некоторых событий, передайте фильтр в качестве второго аргумента `on`. Claude Code называет фильтр matcher. Это объект, чьи поля сравниваются с полями события, и hook запускается только когда каждое поле совпадает. Поле может быть значением, массивом допустимых значений или регулярным выражением.

Каждая строка в этом примере регистрирует одну и ту же функцию, `hook`, для более узкого набора вызовов инструментов:

```javascript theme={null}
// Строка совпадает с одним значением: только вызовы Bash
on('tool.call', { tool: 'Bash' }, hook)
// Массив совпадает с любым значением в нём: вызовы Edit и Write
on('tool.call', { tool: ['Edit', 'Write'] }, hook)
// Регулярное выражение совпадает по шаблону: каждый инструмент одного сервера MCP
on('tool.call', { tool: /^mcp__github__/ }, hook)
```

`hook` запускается один раз для вызова Bash, Edit или Write и один раз для вызова инструмента, имя которого начинается с `mcp__github__`. Вызов любого другого инструмента, такого как Read, не совпадает ни с одним из трёх, поэтому `hook` не запускается для него.

Имя события может быть подстановочным символом. `'classic.*'` совпадает с каждым [событием хуков настроек](#hook-the-settings-hook-events). `'*'` совпадает с каждым событием, кроме [событий телеметрии](https://code.claude.com/docs/ru/plugins/mods/reference.md#telemetry), которые указываются по собственному имени и с фильтром `{ to: 'collector' }`.

Регистрируйте каждое событие один раз для каждого matcher. Если вы вызовете `on` дважды для `session.start` без matcher, модуль не загружается с ошибкой `on("session.start") is registered twice without a matcher`. Поместите всё, что ваш мод делает при запуске сеанса, в один hook.

#### Хуки на отрисовку и элементы управления других модов

Чтобы повесить хук на элементы управления, панели или строку над промптом другого мода, передайте matcher с `plugin`. Используйте имя мода без его маркетплейса, например `{ plugin: 'other-mod' }`, или `{ plugin: '*' }` для всех модов. Без `plugin` хук на `ui.press`, `ui.input`, `ui.select` или `ui.focus` не запускается для элементов управления других модов, а хук `ui.render` пропускает их панели и их строки над промптом.

Хук на подстановочный символ без matcher, например `on('*', hook)` или `on('ui.*', hook)`, по-прежнему запускается для каждого мода. Подстановочному символу с matcher тоже нужен `plugin`.

> [!NOTE]
>
> `{ plugin: '*' }` требует Claude Code v2.1.323 или более поздней версии. До v2.1.323 хук без `plugin` запускался для каждого мода, а хук с `{ plugin: '*' }` не запускался. Чтобы совпадать с каждым модом в обеих версиях, используйте `{ plugin: /./ }` для `ui.press`, `ui.input` и `ui.select`. Для `ui.focus` и `ui.render` используйте `on('ui.*', hook)` и проверяйте имя события в `next.event`, например `if (next.event !== 'ui.focus') return next(e)`.

## Подключиться к тому, что делает Claude

Обрабатывайте эти события, чтобы видеть или изменять вызов инструмента, промпт, ход или чтение настроек по мере их возникновения. Описание каждого события и того, что может вернуть хук, см. в [справочнике событий](https://code.claude.com/docs/ru/plugins/mods/reference.md#events).

### Защитить или изменить вызов инструмента

Хук `tool.call` видит каждый инструмент, который Claude собирается использовать, поэтому он может отказать в вызове, изменить его аргументы или пропустить его. `tool.call` срабатывает, когда Claude Code собирается запустить инструмент, включая вызовы, которые делает субагент, и вызовы инструментов MCP. `e.tool` — это имя инструмента, а аргументы инструмента — это поля `e`, например `e.command` для Bash. Когда вы вызываете `next(e)`, Claude Code выполняет проверку разрешений, а затем запускает инструмент.

Этот хук отказывает в команде Bash, которая выполняет force-push, и объясняет Claude почему:

```javascript theme={null}
// The matcher limits the hook to Bash calls, so e.command is the shell command
on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
  if (/git push .*--force/.test(e.command)) {
    // Returning without calling next answers the event, so the command never runs
    return { deny: 'Force pushes are not allowed in this repository. Push to a new branch instead.' }
  }
  // Every other command goes on to the permission check and then to Bash
  return next(e)
})
```

Когда Claude пытается выполнить `git push --force`, команда не запускается и запрос разрешения не появляется, потому что хук не вызывает `next`. Claude читает текст `deny` как результат инструмента, поэтому пишите его как инструкцию, по которой Claude может действовать. Любая другая команда Bash выполняется так же, как без мода.

Если этот хук выбрасывает исключение или превышает время ожидания, Claude Code пропускает его, и команда выполняется так же, как без мода. Чтобы вместо этого отказать в команде, [добавьте к хуку обработчик `.catch`](#handle-a-hook-that-fails).

Чтобы действовать после запуска инструмента, выполните `await next(e)`, сделайте свою работу и верните то, что дал вам `next`. Этот хук записывает в лог каждый файл `.mdx`, который изменяет Claude, с помощью [`$.ui.log`](https://code.claude.com/docs/ru/plugins/mods/api#show-something-without-starting-a-turn), который добавляет в транскрипт тусклую строку, которую Claude не читает:

```javascript theme={null}
on('tool.call', { tool: ['Edit', 'Write'] }, async ($, e, next) => {
  // Wait for the permission check and the tool, and keep what they produced
  const result = await next(e)
  // A refused call comes back as { deny }, and a failed one has isError set
  const changed = !result.deny && !result.isError
  if (changed && e.file_path.endsWith('.mdx')) $.ui.log('Claude changed ' + e.file_path)
  // Return the result as it came, so Claude reads what the tool returned
  return result
})
```

После того как Claude редактирует или записывает файл `.mdx`, тусклая строка в транскрипте называет этот файл. Для файлов другого типа, а также для вызовов, в которых было отказано или которые завершились ошибкой, ничего не записывается. Представление Claude о вызове не меняется, потому что хук возвращает полученный результат.

Ваш хук также может изменить вызов, повторить его, ответить на него самостоятельно или скрыть его результат:

* **Изменить вызов**: передайте изменённые аргументы в `next`.
* **Повторить попытку вызова**: снова вызовите `next(e)`. Хук, который видит `isError` в первом результате, может запустить инструмент второй раз и вернуть этот результат.
* **Ответить на вызов самостоятельно**: верните объект с полем `result`, не вызывая `next`, а для встроенного инструмента придайте `result` ту форму, которую имеет собственный результат этого инструмента в [типах для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build). Запрос разрешения не появляется и инструмент не запускается, поэтому возвращённый вами результат — это всё, что Claude узнает о произошедшем.
* **Скрыть результат от Claude**: верните `{ deny: reason }` после `await next(e)`. Claude читает вашу причину вместо того, что вернул `next`. Если инструмент был запущен, deny скрывает его результат от Claude и не отменяет ничего из того, что сделал инструмент. Если инструмент был запущен и выполнился успешно, причина следует за примечанием вида `Bash ran, and a plugin withheld its result:`.

Хуки в [управляемых настройках](https://code.claude.com/docs/ru/server-managed-settings.md) вашей организации запускаются раньше любого хука `tool.call` мода. Если управляемый хук блокирует вызов, ни один хук `tool.call` мода для этого вызова не запускается.

#### Удерживать вызов инструмента, пока пользователь не решит

Хук может приостановить вызов инструмента и спросить пользователя, что делать, прежде чем вызов продолжится. Хук `tool.call` может выполнить `await` перед вызовом `next` или возвратом, и до этого момента вызов инструмента остаётся в ожидании. Чтобы задать вопрос пользователю, вызовите `$.ui.ask`. Он показывает ваш вопрос над пронумерованным списком ваших вариантов в диалоговом окне, которое Claude использует, чтобы что-то у вас спросить, и разрешается в метку, которую выбрал пользователь. После ваших вариантов диалоговое окно добавляет строку для ввода другого ответа и строку **Chat about this**.

Шаблон `RISKY` в этом примере совпадает с `rm -r`, `rm -rf`, `git reset --hard` и `git push` с `--force` и пропускает другие варианты написания, например `git push -f`. Этот модуль спрашивает, прежде чем запустить команду Bash, совпадающую с шаблоном:

```javascript theme={null}
const RISKY = /\brm\s+-rf?\b|\bgit\s+reset\s+--hard\b|\bgit\s+push\b.*--force/

export function register(on) {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    // Let every other command through without a question
    if (!RISKY.test(e.command)) return next(e)
    // Start from the safe answer, so a question nobody answers refuses the command
    let answer = 'Refuse'
    try {
      // The tool call waits here until the user picks one of the two labels
      answer = await $.ui.ask('Run this command? ' + e.command, ['Run it', 'Refuse'])
    } catch {
      // The user dismissed the question, or this is a claude -p run with nobody to ask
    }
    if (answer !== 'Run it') {
      // Answer without calling next, so the command doesn't run
      return { deny: 'The user declined this command. Ask before trying a different approach.' }
    }
    return next(e)
  })
}
```

Когда Claude пытается выполнить команду, например `rm -rf build`, появляется вопрос с этой командой, и команда ждёт ответа:

* **Пользователь выбирает Run it**: хук вызывает `next(e)`, и после этого всё равно выполняется обычная проверка разрешений
* **Пользователь выбирает Refuse**: команда не запускается, и Claude читает текст `deny`
* **Пользователь вводит ответ**: `$.ui.ask` разрешается во введённый текст. Хук сравнивает его с `Run it`, поэтому любой другой текст приводит к отказу в команде.
* **Никто не отвечает**: `$.ui.ask` отклоняется, когда пользователь закрывает вопрос или выбирает **Chat about this**, а также при запуске `claude -p`, поэтому блок `catch` оставляет ответ равным `Refuse`

Держите ожидание внутри вызова mods API, например `$.ui.ask`, потому что это время не учитывается в [ограничении времени](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits) хука. Время, потраченное на ожидание вашего собственного promise, учитывается.

Claude Code пропускает хук, превысивший время ожидания, поэтому удерживаемая команда будет выполнена. Чтобы вместо этого отказать в ней, присоедините [обработчик `.catch`](#handle-a-hook-that-fails) к регистрации, которую возвращает `on`. Этот обработчик не связан с блоком `catch` внутри хука.

#### Одобрение или отклонение вызова инструмента до вопроса пользователю

Чтобы решить, может ли выполняться вызов инструмента, обработайте [`tool.check`](https://code.claude.com/docs/ru/plugins/mods/reference#tools) — событие, в котором Claude Code принимает это решение.

Для фиксированной команды или пути используйте [правило разрешений](https://code.claude.com/docs/ru/permissions.md#permission-rule-syntax), например `Bash(npm test)`, которое не требует кода. Обрабатывайте `tool.check`, когда решение зависит от того, что верно в данный момент, например от текущей ветки Git или значения, записанного другим хуком.

* **Что возвращать**: чтобы принять решение о вызове самостоятельно, верните собственный объект, например `{ decision: 'allow' }` или `{ decision: 'deny', reason }`. Чтобы оставить решение без изменений, верните то, что даёт вам `await next(e)`.
* **Что даёт `await next(e)`**: собственное решение Claude Code в виде объекта, у которого `decision` равно `allow`, `ask` или `deny`. Пока выполняется `next(e)`, запрос разрешения не появляется.
* **Аргументы**: `e.input` содержит аргументы инструмента, например `command` для Bash
* **Когда срабатывает `tool.check`**: после запуска [хуков `PreToolUse`](https://code.claude.com/docs/ru/hooks#pretooluse) и до запроса разрешения, классификатора [авторежима](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) или хука [`PermissionRequest`](https://code.claude.com/docs/ru/hooks#permissionrequest)

Этот хук отклоняет `git push`, пока текущая ветка — `main`:

```javascript theme={null}
on('tool.check', { tool: 'Bash' }, async ($, e, next) => {
  // Claude Code's own decision
  const decided = await next(e)
  if (!e.input.command.includes('git push')) return decided
  const branch = await $.process.run(['git', 'branch', '--show-current'])
  if (branch.stdout.trim() !== 'main') return decided
  return { decision: 'deny', reason: 'Push from a branch other than main' }
})
```

Хук отклоняет `git push` на `main` и пропускает все остальные вызовы:

* **На `main`**: хук возвращает `deny`, даже если правило разрешает `git push`
* **На другой ветке, а также для других команд**: вызов получает то же решение, что и без мода
* **Хук выбрасывает исключение или превышает время ожидания**: вызов также получает то же решение, что и без мода. Чтобы вместо этого отказать в вызове, [добавьте обработчик `.catch`](#handle-a-hook-that-fails), который возвращает `{ decision: 'deny', reason: 'the reason' }`.

Хук сопоставляет текст команды, поэтому рассматривайте его как напоминание для Claude. Чтобы заблокировать push в `main` для всех, защитите ветку на своём Git-хостинге.

> [!NOTE]
>
> Хук `tool.check` также может вернуть `allow` или `ask`. В [режиме планирования](https://code.claude.com/docs/ru/permissions.md#hook-approvals-in-plan-mode) для вызова, который не является вызовом только для чтения, например редактирования файла, ваш хук может ужесточить решение, возвращаемое `next(e)`, но не может ослабить его. О правилах разрешений и решениях хуков `PreToolUse`, которые `allow` вашего хука не может заменить, см. [Расширение разрешений с помощью хуков](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

#### Проверить, является ли вызов инструмента вызовом только для чтения

В хуке [`tool.check`](#approve-or-refuse-a-tool-call-before-the-user-is-asked) `e.isReadOnly` равно `true`, когда инструмент сообщает, что вызов выполняется только для чтения. В противном случае поле отсутствует, а не равно `false`. Для `e.isReadOnly` требуется Claude Code v2.1.304 или новее.

Некоторые инструменты, такие как Read, Grep, Glob и WebSearch, сообщают о каждом вызове как о вызове только для чтения. Bash и инструменты MCP сообщают о вызове как о вызове только для чтения в следующих случаях:

* **Bash**: команда проходит встроенную в Claude Code [проверку команд только для чтения](https://code.claude.com/docs/ru/permissions.md#read-only-commands)
* **Инструмент MCP**: сервер задаёт аннотации `readOnlyHint` инструмента значение `true`

Это значение — собственное сообщение инструмента, поэтому не одобряйте вызов только на основании этого поля. Например, вызовы WebFetch и Agent сообщаются как вызовы только для чтения, хотя [WebFetch](https://code.claude.com/docs/ru/tools-reference.md#webfetch-tool-behavior) запрашивает URL, а [Agent](https://code.claude.com/docs/ru/tools-reference.md#agent-tool-behavior) запускает субагента, который выполняет собственные инструменты.

Этот хук возвращает `ask` для каждого вызова `mcp__github__`, который не является вызовом только для чтения и ещё не был отклонён:

```javascript theme={null}
on('tool.check', { tool: /^mcp__github__/ }, async ($, e, next) => {
  const decided = await next(e)
  // Read-only calls and denied calls pass through unchanged
  if (e.isReadOnly || decided.decision === 'deny') return decided
  return { decision: 'ask', reason: 'This tool can change the GitHub repository' }
})
```

#### Отфильтровать хук `tool.check` по тому, является ли вызов вызовом только для чтения

Чтобы ограничить вызовы, которые обрабатывает ваш хук, по [`e.isReadOnly`](#check-whether-a-tool-call-is-read-only), используйте [matcher](#filter-which-events-a-hook-handles) для вызовов только для чтения и тело хука для остальных:

* **Только вызовы только для чтения**: добавьте `isReadOnly: true` в matcher, как в `on('tool.check', { tool: 'Bash', isReadOnly: true }, hook)`
* **Вызовы, не являющиеся вызовами только для чтения**: проверяйте `e.isReadOnly` в теле хука, как это делает [пример `mcp__github__`](#check-whether-a-tool-call-is-read-only). Если указать `isReadOnly: false` в matcher, ваш хук никогда не запустится.

### Переписать промпт или дополнить его

Хук `prompt.submit` видит каждый промпт до начала хода, поэтому он может переписать текст или дополнить его. `e.text` — это то, что было введено.

| Чтобы сделать это | Верните это |
| :- | :- |
| Переписать промпт. Транскрипт и ваша [история промптов](https://code.claude.com/docs/ru/interactive-mode.md#command-history) показывают новый текст. | `next({ ...e, text: newText })` |
| Добавить после промпта текст, который читает только Claude | `next({ ...e, context: [...(e.context ?? []), extraText] })` |
| Не допустить отправки промпта | `{ drop: 'the reason' }` |

Этот хук добавляет для Claude имя текущей ветки всякий раз, когда промпт упоминает pull request:

```javascript theme={null}
on('prompt.submit', async ($, e, next) => {
  // Pass on a prompt that doesn't mention a pull request as it is
  if (!/\bPR\b|pull request/i.test(e.text)) return next(e)
  const git = await $.process.run(['git', 'branch', '--show-current'])
  // Outside a git repository the command fails, so there's no branch to add
  if (git.exitCode !== 0) return next(e)
  // Keep any context an earlier hook added, and add one more line for Claude
  return next({ ...e, context: [...(e.context ?? []), 'Current branch: ' + git.stdout.trim()] })
})
```

Когда вы отправляете промпт, например `open a PR for this change`, ваше сообщение в транскрипте выглядит так же, а Claude после него также читает строку вида `Current branch: feature/auth`. Промпт, который не упоминает pull request, проходит без изменений, и `git` не запускается.

Чтобы остановить промпт, верните `{ drop: 'the reason' }`, не вызывая `next`. Текст возвращается в поле ввода промпта пользователя, и он видит `Prompt dropped by a hook:`, а затем вашу причину, поэтому адресуйте причину ему. Промпт всё равно проходит в следующих случаях:

* **Ваш хук возвращает `drop` после того, как его вызов `next(e)` уже пропустил промпт**: ход всё равно выполняется, а хук [завершается ошибкой](#handle-a-hook-that-fails) с сообщением, содержащим `a drop after its next() was answered`
* **Ваш хук выбрасывает исключение или превышает время ожидания**: Claude Code пропускает его и отправляет промпт. [Добавьте обработчик `.catch`](#handle-a-hook-that-fails), чтобы сбой не приводил к отправке промпта, который хук остановил бы.

[Другие события](https://code.claude.com/docs/ru/plugins/mods/reference.md#prompts-and-what-claude-reads) охватывают остальное, что читает Claude: `prompt.section` для каждого раздела системного промпта, `prompt.context` для контекста, отправляемого с первым сообщением, и `skill.prompt` для текста скилла. Чтобы изменить раздел после начала диалога, см. [Отправка изменённого раздела системного промпта или описания инструмента](https://code.claude.com/docs/ru/plugins/mods/reference.md#break-prompt-cache). В хуке `skill.prompt` вы также можете прочитать, [из какого плагина или файла получен скилл](https://code.claude.com/docs/ru/plugins/mods/reference.md#skill-prompt-fields).

### Следить за ходом

Ход — это всё, что Claude делает в ответ на один промпт. Обрабатывайте `turn.start`, `turn.step` и `turn.complete`, чтобы следить за ходом:

| Событие | Когда срабатывает | Что может сделать хук |
| :- | :- | :- |
| `turn.start` | Начинается ход | Наблюдать. `e.turnId` идентифицирует ход в двух других событиях. |
| `turn.step` | Claude Code собирается отправить один запрос к модели. В ходе с вызовами инструментов их несколько. `e.agentId` задан для запроса субагента. | Прочитать использование токенов каждого запроса, отправить его другой модели с помощью `next({ ...e, model })` или ответить без вызова модели |
| `turn.complete` | Ход завершился, включая ход, прерванный пользователем, — в этом случае `e.isAborted` равно `true`. `e.answer` — финальный текст Claude, `e.durationMs` — сколько времени это заняло, а `e.usage` — итоговое количество токенов за ход. Ход субагента вызывает его с заданным `e.agentId`. | Наблюдать или вернуть объект с полем `text`, например `{ text: 'Done in 12 seconds' }`, чтобы показать строку под ответом |

Пишите хук `turn.step` как асинхронный генератор, потому что событие потоковое. `yield* next(e)` передаёт ответ дальше по мере его поступления и вычисляется в итоговый результат. Этот хук записывает в лог, какую часть каждого запроса Claude API обслужил из [кэша промптов](https://code.claude.com/docs/ru/prompt-caching.md):

```javascript theme={null}
// function* makes the hook a generator, which can pass the response on piece by piece
on('turn.step', async function* ($, e, next) {
  // Send the request, forward each piece as it arrives, and keep the finished result
  const result = yield* next(e)
  // Skip a result that reports no token counts
  if (result.usage) {
    $.ui.log('cache read ' + result.usage.cache_read_input_tokens + ' · wrote ' + result.usage.cache_creation_input_tokens)
  }
  // Return the result unchanged, so the turn continues as usual
  return result
})
```

Ответ Claude выводится на экран потоком так же, как без мода. После завершения каждого запроса тусклая строка в транскрипте показывает количество токенов, прочитанных из кэша, и количество записанных в него. В ходе с вызовами инструментов несколько запросов, поэтому он добавляет несколько строк.

`result.usage` содержит количество токенов, которое Claude API сообщает для запроса, а также `model`, которая ответила: `input_tokens`, `output_tokens`, `cache_read_input_tokens` и `cache_creation_input_tokens`. Хук запускается и для запросов субагентов, поэтому проверяйте `e.agentId`, если вам нужен только основной диалог.

Чтобы увидеть вызовы инструментов, которые API выполнил сам во время запроса, например вызовы [инструмента advisor](https://code.claude.com/docs/ru/advisor.md), читайте `result.serverToolUses`. Claude Code не выполняет эти вызовы, поэтому для них не срабатывает ни один хук `tool.call` или `tool.check`. Поле отсутствует, если в ответе нет таких вызовов, и для него требуется Claude Code v2.1.290 или новее.

#### Отправить запрос другой модели

Если запрос `turn.step` завершается ошибкой модели, когда `model` — это псевдоним, например `haiku`, обновитесь до Claude Code v2.1.309 или новее либо используйте полный идентификатор модели. До v2.1.309 псевдоним отправлялся в том виде, в каком был записан.

Чтобы отправить запрос другой модели, передайте в `next` событие с изменённым `model`, как в `yield* next({ ...e, model: 'haiku' })`.

### Изменить чтение настроек или отказать в нём

Используйте хук `settings.read`, чтобы изменить чтение настроек или отказать в нём — как чтение модом, так и собственное чтение Claude Code:

* **Чтение модом**: мод вызывает [`$.settings.read`](https://code.claude.com/docs/ru/plugins/mods/api#read-one-source-or-one-key).
* **Собственное чтение Claude Code**: ваш хук впервые запускается, когда Claude Code объединяет настройки сессии, после загрузки модов сессии. Ваш хук запускается снова при изменении настроек или загруженных плагинов.

Проверьте, какие моды получают это событие, и свою версию Claude Code:

* **Встроенный страж**: там, где загружается [встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), он может пропускать этот хук в моде, который вы устанавливаете или загружаете с помощью `--plugin-dir`. Чтобы проверить это, найдите в [отладочном логе](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#read-the-debug-log) `settings.read bypassed by cc-plugin-sec-default`. Если строка с этим текстом называет ваш мод, попросите администратора вашей организации [установить мод как один из модов организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods).
* **Версия**: для срабатывания события при собственном чтении Claude Code и для поля `e.layers` требуется Claude Code v2.1.304 или новее.

#### Что получает хук `settings.read`

| Поле | Тип | Что содержит |
| :- | :- | :- |
| `e.layers` | массив | Один объект `{ source, settings }` для каждого используемого источника, содержащего настройки, начиная с источника с наименьшим [приоритетом](https://code.claude.com/docs/ru/settings.md#settings-precedence): `plugin`, `user`, `project`, `local`, `flag`, `policy`. Пуст в `claude plugin test`. |
| `e.source` | строка | Единственный источник, который запросил мод, как в `$.settings.read({ source: 'policy' })`. В этом случае `e.layers` содержит только этот слой. Отсутствует при собственном чтении Claude Code и при любом другом чтении объединённых настроек. |

В `e.layers` слой `plugin` содержит настройки, которые предоставляют включённые плагины, и является только именем слоя, а не значением `source`, которое можно передать в `$.settings.read`. `flag` содержит настройки, переданные с помощью `--settings`, а `policy` — управляемые настройки.

#### Отличить собственное чтение Claude Code от чтения модом

Проверьте [`next.origin`](https://code.claude.com/docs/ru/plugins/mods/reference#the-hook-function):

* **Собственное чтение Claude Code**: `{ plugin: 'engine', tier: 'core' }`
* **Чтение модом**: `plugin` — это имя вызывающего мода

#### Что может вернуть хук `settings.read`

Верните результат [`next(e)`](#settings-read-next) без изменений, чтобы оставить чтение как есть, или верните одно из следующих значений:

| Возвращаемое значение | При [собственном чтении Claude Code](#settings-read-hook) | При чтении модом |
| :- | :- | :- |
| `{ value }` | Для каждого изменённого ключа вы заменяете всё его значение в объединённых настройках сессии, если ваше значение [соответствует схеме ключа](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#settings-read-key-refused) | Вызов этого мода разрешается в ваш `value` или в запрошенный им `key`, взятый из вашего `value`, поэтому возвращайте целый объект, а не массив |
| `{ deny: reason }` | Сессия сохраняет настройки в том виде, в каком они были объединены до ответа любого хука, а [отладочный лог записывает ваш `reason`](https://code.claude.com/docs/ru/plugins/mods/troubleshoot#settings-read-refused) | Вызов этого мода отклоняется с `<calling mod>: $.settings.read: <reason>` |

При собственном чтении Claude Code формируйте свой `{ value }` на основе [`value` из `next(e)`](#settings-read-next), поскольку ключ, который вы опустите, окажется не задан. Если Claude Code читает ключ, например `env`, из каждого источника отдельно, его изменение в вашем `value` [ни на что не влияет](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#settings-read-key-no-effect).

#### Что `next(e)` даёт хуку `settings.read`

`next(e)` разрешается в `{ value }` или в `{ deny }`:

* **`{ value }`**: `value` — это объединённые настройки или настройки одного источника, если задано [`e.source`](#settings-read-receives). Если хук, который [запускается после вашего](#the-order-mods-run-in), вернул собственный `{ value }`, вы получаете вместо этого `value` того хука.
* **`{ deny }`**: хук, который запускается после вашего, отказал в чтении. Верните этот `{ deny }` без изменений.

#### Изменить одну настройку из хука `settings.read`

Сначала проверьте, [какие моды получают это событие и начиная с какой версии](#settings-read-hook).

Чтобы изменить один ключ, разверните `value` из [`next(e)`](https://code.claude.com/docs/ru/plugins/mods/reference#the-hook-function) и задайте этот ключ, как этот хук делает с [`spinnerTipsEnabled`](https://code.claude.com/docs/ru/settings-reference#spinnertipsenabled). Хук не проверяет [`next.origin`](#settings-read-origin), поэтому он изменяет ключ как при [собственном чтении Claude Code](#settings-read-hook), так и при чтении модом объединённых настроек:

```javascript theme={null}
on('settings.read', async ($, e, next) => {
  const read = await next(e)
  // Pass through a read of one source, so that only the merged settings change.
  // Pass through a { deny } from a later hook too: it has no value.
  if (e.source || !read.value) return read
  // Keep every other key and change this one
  return { value: { ...read.value, spinnerTipsEnabled: false } }
})
```

Если при собственном чтении Claude Code ваш хук возвращает значение вне схемы ключа, например строку, только этот ключ сохраняет значение, объединённое до ответа любого хука. В этом случае отладочный лог сообщает [`the answer for <key> is no value the key can hold`](https://code.claude.com/docs/ru/plugins/mods/troubleshoot#settings-read-key-refused). Если ваше значение подходит, а ключ всё равно не меняется, см. [почему ключ не вступает в силу](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#settings-read-key-no-effect).

### Обработка событий хуков настроек

Хуки настроек — это хуки типов command, HTTP, prompt и agent, которые вы настраиваете в файлах настроек. Каждое [событие хука настроек](https://code.claude.com/docs/ru/hooks.md#hook-events), например `Stop`, `SessionEnd` или `PostToolUse`, также является событием с именем `classic.`, за которым следует имя события хука настроек, например `classic.Stop`. `e` — это JSON, который хук настроек получает на stdin, включая `transcript_path`. Там, где загружается [встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), [хук на эти события в моде, который вы устанавливаете, не запускается](https://code.claude.com/docs/ru/plugins/mods/admin.md#hooks-the-guard-passes-over).

Этот хук использует `Stop`, которое срабатывает, когда Claude заканчивает отвечать, чтобы записать в лог, где сохранён транскрипт сессии:

```javascript theme={null}
on('classic.Stop', async ($, e, next) => {
  // e has the same fields a Stop hook in a settings file reads from stdin
  $.ui.log('Transcript saved at ' + e.transcript_path)
  // Pass the event on, so Stop hooks in your settings files still run
  return next(e)
})
```

Каждый раз, когда Claude заканчивает отвечать, тусклая строка в транскрипте показывает путь к файлу транскрипта. Хук возвращает `next(e)`, поэтому он наблюдает за событием и никак не меняет то, как завершается ход.

## Запускаться рядом с другими модами

Несколько модов могут обрабатывать одно и то же событие, и любой из них может дать сбой. Если ваш мод блокирует вызовы инструментов, проверьте его позицию в цепочке и что происходит, когда его хук даёт сбой.

### Порядок, в котором запускаются моды

Хуки на одно и то же событие образуют одну цепочку middleware. Каждый `next` мода вызывает хук следующего мода, и последний `next` достигает собственного поведения Claude Code. Первый мод является самым внешним: он видит событие перед другими и результат после них, и он решает, запускаются ли другие вообще. Более поздний мод не может остановить более ранний от просмотра события.

Claude Code упорядочивает цепочку по тому, откуда берётся каждый мод:

1. Встроенный страж `sec-default@builtin`, мод, встроенный в Claude Code, который `/plugin` перечисляет как `cc-plugin-sec-default`, где [он загружается](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), моды, которые ваша организация перечисляет в [`prependPlugins`](https://code.claude.com/docs/ru/plugins/mods/admin#install-your-organizations-mods), а затем любой другой мод, который считается модом вашей организации и не находится в `appendPlugins`
2. Моды, которые вы устанавливаете
3. Моды, которые ваша организация перечисляет в `appendPlugins`
4. Другие моды, встроенные в Claude Code

Среди модов, которые вы устанавливаете, мод запускается перед модами, которые он перечисляет в `dependencies` в своём манифесте. В одном модуле хуки запускаются в порядке, в котором `register` вызвал `on`.

#### Где хуки настроек запускаются в порядке

Хуки `PreToolUse`, настроенные в файлах настроек, также запускаются во время вызова инструмента в фиксированных точках цепочки модов:

* **Хуки `PreToolUse` из управляемых настроек**: запускаются перед хуком `tool.call` первого мода. Когда управляемый хук блокирует вызов, ни один хук `tool.call` мода не запускается для этого вызова.
* **Хуки `PreToolUse` из каждого другого файла настроек и из `hooks/hooks.json` плагинов**: запускаются после того, как последний мод вызовет `next`, как часть собственного поведения Claude Code. Мод, который отвечает на `tool.call` без вызова `next`, не позволяет им запускаться, и мод, который вызывает `next`, видит их решение в результате, который он возвращает.

[`tool.check`](#approve-or-refuse-a-tool-call-before-the-user-is-asked) срабатывает после того, как хуки `PreToolUse` отработали. Чтобы узнать, какие правила разрешений и решения хуков `PreToolUse` не может заменить `allow` хука `tool.check`, см. раздел [Расширение разрешений с помощью хуков](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods).

### Обработать хук, который даёт сбой

Хук, который даёт сбой, не нарушает сессию, и вы можете решить, что происходит вместо этого. Когда хук без обработчика `.catch` выбрасывает исключение, превышает таймаут или возвращает результат неправильной формы, что происходит дальше, зависит от того, вызвал ли он `next`:

* **Он дал сбой перед вызовом `next`**: Claude Code пропускает его, и следующий обработчик запускается на его месте
* **Он дал сбой после разрешения `next`**: этот результат остаётся в силе, и ничего не запускается второй раз

Одна строка называет мод, событие и причину, такую как `my-mod: tool.call hook skipped: threw Error: boom`. Где вы это читаете, зависит от сессии, как перечислено в разделе [Узнать, почему мод ничего не делает](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing). Хук `ui.render`, чьё [дерево не проходит валидацию](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-tree-from-elements), считается хуком, который вернул результат неправильной формы.

Чтобы хук, который блокирует вызовы, при сбое закрывал доступ (fail closed), добавьте обработчик ошибок `.catch`, который отвечает на его месте. Здесь `guard` — это ваша хук-функция, а обработчик проверяет [`next.called`](https://code.claude.com/docs/ru/plugins/mods/reference#the-hook-function), чтобы узнать, вызвал ли `guard` уже `next`, когда дал сбой:

```javascript theme={null}
// on returns a registration, and .catch attaches a handler to that one hook
on('tool.call', { tool: 'Bash' }, guard).catch(async ($, e, next) => {
  // guard had already called next, so return what came back
  if (next.called) return next(e)
  // next.error.kind says why the handler was asked, such as 'throw' or 'timeout'
  return { deny: 'The command guard failed, so this command was not run: ' + next.error.kind }
})
```

Когда `guard` выбрасывает исключение или превышает таймаут при вызове Bash, Claude Code вызывает обработчик с тем же событием:

* **`guard` дал сбой до того, как вызвал `next`**: команда не запускается, и Claude читает текст `deny` с видом сбоя в конце
* **`guard` дал сбой после того, как вызвал `next`**: `next(e)` обработчика разрешается в результат, который дал вызов `guard`, без повторного запуска команды, и Claude читает этот результат

У обработчика есть собственное, более короткое [ограничение по времени](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits). Если сам обработчик выбрасывает исключение или превышает таймаут, Claude Code пропускает хук так, как если бы у него не было обработчика. Если `guard` не вызывал `next`, команда затем выполняется так, как выполнялась бы без мода.

Такая же форма обработчика подходит для стража на `prompt.submit` или `config.set`. Когда `next.called` равно false, верните отказ, который [справочник событий](https://code.claude.com/docs/ru/plugins/mods/reference.md#events) указывает для этого события: `{ drop: 'the reason' }` для `prompt.submit`, `{ deny: 'the reason' }` для `config.set`.

На `tool.check` и `plugin.register` отказ, возвращённый после того, как `next` разрешился, всё равно действует, поэтому возвращайте его без проверки `next.called`:

* **`tool.check`**: верните `{ decision: 'deny', reason: 'the reason' }`
* **`plugin.register`**: верните `{ refuse: 'the reason' }`. В версии v2.1.326 и новее весь плагин другого мода тогда не загружается. Чтобы остановить только мод, см. раздел [Отклонять моды, когда ваша проверка даёт сбой](https://code.claude.com/docs/ru/plugins/mods/admin.md#refuse-mods-when-your-check-fails).

На `tool.call` значение `deny`, возвращённое после того, как `next` разрешился, [скрывает результат от Claude](#guard-or-change-a-tool-call).

## Следующие шаги

* [Использовать mods API](https://code.claude.com/docs/ru/plugins/mods/api.md): добавлять команды и инструменты, вызывать модель и запускать работу по таймеру
* [Рисовать в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md): показывать то, что собирают ваши hooks, в панели или над подсказкой
* [Тестировать мод](https://code.claude.com/docs/ru/plugins/mods/test.md): вызывать любое из этих событий из теста
* [Справочник модов](https://code.claude.com/docs/ru/plugins/mods/reference.md): каждое событие, каждый метод mods API и ограничения
