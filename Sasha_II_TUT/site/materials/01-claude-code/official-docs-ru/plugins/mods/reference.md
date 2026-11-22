> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник по модам

> Полный справочник по модам Claude Code: структура модуля хуков, события, методы API модов, точки отрисовки, элементы по интерфейсам, ограничения и настройки.

Здесь можно найти любое событие, которое может обрабатывать [мод](https://code.claude.com/docs/ru/plugins/mods/overview.md), любой метод API модов, который он может вызвать, и любую точку отрисовки, в которой он может рисовать. Записи охватывают CLI Claude Code и приложение Desktop по состоянию на v2.1.290, а также расширение VS Code по состоянию на v2.1.299. Для каждой записи указаны имя и однострочное описание, а также ссылка на раздел руководства с пояснениями, если такой раздел есть.

> [!NOTE]
>
> Полный справочник — это [TypeScript-декларации Claude Code для модов](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts), в которых описаны все события, методы и элементы с примерами. Копия на GitHub может быть старше установленной у вас версии Claude Code. Если они расходятся, доверяйте [копии, которую Claude Code записывает для вашей версии](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build).

## Файлы

Мод — это каталог плагина со следующими файлами:

| Файл | Обязателен | Содержимое |
| :- | :- | :- |
| `.claude-plugin/plugin.json` | Да | [Манифест](https://code.claude.com/docs/ru/plugins/manifest-reference.md) плагина. Моды не добавляют обязательных полей. |
| `hooks/hooks.json` | Да | `modules`: массив с одним путём к модулю хуков относительно этого файла, например `"modules": ["./register.js"]`. Может также содержать [хуки настроек](https://code.claude.com/docs/ru/hooks.md) в поле `hooks`. |
| Модуль хуков, например [`hooks/register.js`](https://code.claude.com/docs/ru/plugins/mods/create#write-a-mod-yourself) | Да | Точка входа мода. Экспортирует `register(on, options)`. Имеет расширение `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts` или `.tsx`. Является ES-модулем. |
| [`types/index.d.ts`](https://code.claude.com/docs/ru/plugins/mods/interface#declare-the-values), если только поле `types` в манифесте не указывает другой путь | Когда мод использует `$.state` или добавляет пространство имён в API модов | Объявляет значения `PluginState` и любое пространство имён, которое добавляет мод. Чтобы не указывать `types` в манифесте, требуется версия v2.1.299 или новее. |
| Файлы, имена которых заканчиваются на `.test.ts` или `.test.tsx` | Нет | Тесты, которые запускает [`claude plugin test`](https://code.claude.com/docs/ru/plugins/mods/test#write-a-test) |

`register` получает `on` и `options`. `options` содержит значения полей [`userConfig`](https://code.claude.com/docs/ru/plugins/components#user-configuration), объявленных в манифесте, с подставленными значениями по умолчанию.

## Функция хука

Мод регистрирует каждый из своих хуков, то есть обработчиков событий, вызывая `on` внутри `register`. `on` принимает имя события, необязательный [matcher](https://code.claude.com/docs/ru/plugins/mods/events.md#filter-which-events-a-hook-handles), то есть фильтр по полям события, и сам хук, например `on('tool.call', { tool: 'Bash' }, async ($, e, next) => next(e))`. `on` возвращает регистрацию с одним методом, `.catch(handler)`, который задаёт [обработчик ошибок](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails) хука.

| Аргумент | Что это |
| :- | :- |
| [`$`](https://code.claude.com/docs/ru/plugins/mods/events#how-a-hook-handles-an-event) | API модов: все методы из раздела [Методы API модов](#mods-api-methods). Записывайте каждый вызов полностью, пространство имён и затем метод, например `$.fs.read('notes.md')`. |
| [`e`](https://code.claude.com/docs/ru/plugins/mods/events#how-a-hook-handles-an-event) | Входные данные события в виде глубоко замороженных простых данных. Чтобы изменить их, передайте копию в `next`. |
| [`next(e)`](https://code.claude.com/docs/ru/plugins/mods/events#how-a-hook-handles-an-event) | Следующий обработчик, как в middleware. Запускает хуки, идущие после этого, а затем поведение Claude Code. Разрешается в результат события. |
| [`next.signal`](https://code.claude.com/docs/ru/plugins/mods/api#stop-background-work) | `AbortSignal`, который прерывается, когда событие отменено |
| `next.origin` | `{ plugin, tier }` того, кто инициировал событие. Сам Claude Code — это `{ plugin: 'engine', tier: 'core' }`. `tier` мода — это его группа приоритета в [порядке запуска модов](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in): `prepend`, `user`, `append` или `builtin`. |
| `next.budget` | Ограничение времени хука в миллисекундах: `next.budget.ms` — всё ограничение, а `next.budget.remainingMs` — оставшееся на данный момент время |
| `next.to(e, tier)` | Переходит к более позднему уровню: `append`, `builtin` или `core`. `next.to(e, 'append')` пропускает моды, установленные пользователем. Вызвать его может только мод из `prependPlugins` или `appendPlugins`. |
| `next.error` | Только в обработчике `.catch`. `kind` — это `throw` или `timeout`, а `message` — текст ошибки. |
| `next.called` | Только в обработчике `.catch`. `true`, если хук вызвал `next`. |

## События

События сгруппированы по тому, к чему они относятся; для каждого указано, когда оно срабатывает и что может вернуть хук на него. Хуки на `turn.step` и `process.spawn` — асинхронные генераторы, остальные хуки — асинхронные функции.

В последнем столбце каждой таблицы используется сокращённая запись. `next(e)` передаёт событие дальше без изменений. `next({ ...e, text })` передаёт дальше копию с изменённым указанным полем, например `next({ ...e, text: e.text.trim() })`. Объект отвечает на событие без вызова `next`, а слово вроде `reason` обозначает строку, которую вы пишете, например `{ deny: 'Use the file tools.' }`.

### Инструменты

События инструментов срабатывают вокруг каждого вызова инструмента, который делает Claude, — от описания, которое читает Claude, до решения о том, будет ли вызов выполнен:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`tool.call`](https://code.claude.com/docs/ru/plugins/mods/events#guard-or-change-a-tool-call) | Инструмент вот-вот запустится | `next(e)`, `{ deny: reason }` или `{ result }` |
| [`tool.check`](https://code.claude.com/docs/ru/plugins/mods/events#where-settings-hooks-run-in-the-order) | Claude Code решает, может ли вызов инструмента выполниться, после хуков `tool.call` и `PreToolUse`. `next(e)` разрешается в решение, к которому пришли правила, режим разрешений и эти хуки. | `next(e)` или `{ decision }`, где `decision` равно `allow`, `ask` или `deny`, с необязательным `reason` |
| `tool.describe` | Один раз для каждого инструмента, когда его описание впервые отправляется Claude. Второй раз для инструмента MCP, когда Claude загружает его через [поиск инструментов](https://code.claude.com/docs/ru/mcp.md#scale-with-mcp-tool-search); при этом `e.description` содержит текст, который Claude читает для загруженного инструмента. | `{ description }`, при необходимости с `isDeferred`, равным `true`, чтобы поместить инструмент за поиск инструментов, или `false`, чтобы загрузить его сразу. Добавьте [`breakPromptCache: true`](#break-prompt-cache), чтобы отправить изменённое описание на следующем ходе. |

#### Поля агента и организации в `tool.check`

В хуке `tool.check` читайте эти поля, чтобы отличить вызов субагента от вызова основного диалога и узнать, требует ли ваша организация подтверждения для инструмента коннектора:

* **`e.agentId`**: задано, когда вызов делает [субагент](https://code.claude.com/docs/ru/sub-agents.md) или [участник команды, работающий в том же процессе](https://code.claude.com/docs/ru/agent-teams.md#choose-a-display-mode), и отсутствует, когда вызов делает основной диалог
* **`e.ceiling`**: `ask` для инструмента коннектора, для которого ваша организация установила `ask`, в [сессиях, где эта настройка доходит до Claude Code](https://code.claude.com/docs/ru/mcp.md#organization-controls-on-connector-tools)

В `tool.check` поля `e.agentId` и `e.ceiling` требуют Claude Code v2.1.290 или новее.

#### Поле `e.isReadOnly` в `tool.check`

В хуке `tool.check` поле `e.isReadOnly` равно `true`, когда инструмент сообщает, что этот вызов выполняется только для чтения. В противном случае поле отсутствует, а не равно `false`. Значение — это собственное сообщение инструмента, поэтому прочитайте раздел [Проверка того, выполняется ли вызов инструмента только для чтения](https://code.claude.com/docs/ru/plugins/mods/events.md#check-whether-a-tool-call-is-read-only), прежде чем подтверждать вызов только на основании этого поля.

В `tool.check` поле `e.isReadOnly` требует Claude Code v2.1.304 или новее.

### Промпты и то, что читает Claude

События промптов охватывают текст, который вводит пользователь, и текст, который Claude Code отправляет Claude сам, например системный промпт и напоминания:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`prompt.submit`](https://code.claude.com/docs/ru/plugins/mods/events#rewrite-or-add-to-a-prompt) | Промпт отправлен | `next({ ...e, text })`, `next({ ...e, context })` или `{ drop: reason }` |
| `prompt.fill`, `prompt.suggest` | Текст вот-вот попадёт в поле промпта как черновик или как приглушённая подсказка | `next(e)` с изменённым текстом |
| `prompt.edit` | Пользователь редактирует поле промпта | `next(e)` |
| `prompt.autocomplete` | Пользователь вводит текст в поле промпта, и у курсора заканчивается слово. `e.token` — это слово. Claude Code не ждёт хук: его собственные строки автодополнения показываются первыми. | `{ suggestions }` — список строк `{ text, label, description }`, которые показываются под собственными строками Claude Code. Выбор строки записывает её `text` поверх слова. |
| `prompt.compose` | Claude Code формирует системный промпт | `{ sections }` — список `{ id, text, scope }` в порядке отправки |
| [`prompt.section`](https://code.claude.com/docs/ru/plugins/mods/events#rewrite-or-add-to-a-prompt) | Один раз для каждого именованного раздела системного промпта. `e.name` — это `id` раздела в `prompt.compose`. | `{ text }` или `{ text: null }`, чтобы пропустить раздел. Добавьте [`breakPromptCache: true`](#break-prompt-cache), чтобы отправить изменённый раздел на следующем ходе. |
| [`prompt.context`](https://code.claude.com/docs/ru/plugins/mods/events#rewrite-or-add-to-a-prompt) | Один раз для каждого диалога, для контекста, отправляемого с первым сообщением | `{ blocks }` |
| `prompt.attachment` | Claude Code добавляет собственное сообщение для Claude, например напоминание. `e.type` указывает вид, а для видов, объявленных в типах, `e.detail` содержит факты, на основе которых написан текст. | `{ text }` или `{ text: null }`, чтобы пропустить его |
| `prompt.mention` | Claude Code вот-вот прочитает файл, упомянутый в промпте через @. Требуется Claude Code v2.1.290 или новее. | `next({ ...e, path })`, чтобы прочитать другой файл, или `{ deny: reason }` |
| [`skill.prompt`](https://code.claude.com/docs/ru/plugins/mods/events#rewrite-or-add-to-a-prompt) | Текст скилла раскрывается для Claude | `{ text }` |
| `attribution.text` | Claude Code составляет текст атрибуции для коммита или pull request | `{ text }` |

#### Поля источника и frontmatter в `skill.prompt`

В хуке `skill.prompt` можно читать эти поля наряду с именем скилла в `e.skill` и текстом, который читает Claude, в `e.text`:

| Поле | Тип | Что содержит |
| :- | :- | :- |
| `e.source` | string | Кто предоставляет скилл: `policySettings`, `userSettings` или `projectSettings` для скилла в корпоративном, личном или проектном [расположении](https://code.claude.com/docs/ru/skills.md#where-skills-live) соответственно. Другие источники дают слово вроде `plugin`, `mcp`, `syncedSkills` или `built-in`. |
| `e.pluginName` | string | Имя плагина для скилла, у которого `e.source` равно `plugin` |
| `e.path` | string | Абсолютный путь к файлу `SKILL.md` скилла или к его файлу `.md` для скилла, написанного как [файл команды](https://code.claude.com/docs/ru/skills.md#where-skills-live). Отсутствует, если у скилла нет файла на этой машине, как у встроенного скилла. |
| `e.frontmatter` | object | Frontmatter файла скилла в виде простых данных |
| `e.frontmatterProblem` | string | Причина, по которой в `e.frontmatter` отсутствует frontmatter файла или один из его ключей, например `is a list or a single value, not a table`. Отсутствует, если `e.frontmatter` содержит весь frontmatter или у скилла его нет. |

Хук может передать изменённые `text` или `frontmatter` в `next`: хуки после него читают оба поля, а Claude читает итоговый `text`. Хук, который изменяет любое другое поле, [завершается ошибкой](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails).

В `skill.prompt` поля `e.source`, `e.pluginName`, `e.path`, `e.frontmatter` и `e.frontmatterProblem` требуют Claude Code v2.1.299 или новее.

#### Отправка изменённого раздела системного промпта или описания инструмента с помощью `breakPromptCache`

Чтобы изменить раздел или описание инструмента в текущем диалоге, вызовите `$.ui.invalidate('prompt.section')` или `$.ui.invalidate('tool.describe')`, чтобы ваш хук запустился снова. Верните из него `{ text, breakPromptCache: true }` или `{ description, breakPromptCache: true }`. Без этого поля Claude продолжает читать текст, [сохранённый вместе с диалогом](https://code.claude.com/docs/ru/cli-reference.md#system-prompt-flags-in-resumed-conversations), для раздела или инструмента, загруженного сразу, до начала нового диалога или [сжатия контекста](https://code.claude.com/docs/ru/prompt-caching.md#compacting-the-conversation).

Изменённый текст доходит до Claude на следующем ходе, а [кэш промптов](https://code.claude.com/docs/ru/prompt-caching.md) начинается заново, поэтому этот ход выполняется медленнее и обходится дороже. Это поле требует Claude Code v2.1.321 или новее. С v2.1.299 до v2.1.321 текущий диалог получал изменённый текст на следующем ходе.

### Команды и конфигурация

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`command.run`](https://code.claude.com/docs/ru/plugins/mods/api#add-a-command) | Команда вот-вот запустится | `{ text }`, `{}` или `next(e)` |
| `command.describe` | Один раз для каждой команды, для списка команд | `{ description, argumentHint, isHidden }` |
| `config.set` | Строка `/config` вот-вот изменится | `next({ ...e, value })` или `{ deny: reason }` |
| `config.describe` | Один раз для каждой строки `/config` | `{ label, description, isHidden }` |
| [`settings.read`](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-hook) | Мод вызывает [`$.settings.read`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) или Claude Code формирует объединённые настройки сессии. Для собственного чтения Claude Code и для `e.layers` требуется Claude Code v2.1.304 или новее | `next(e)`, `{ value }` или `{ deny: reason }` |

#### `e.layers` и `e.source` в `settings.read`

* **`e.layers`**: по одному объекту `{ source, settings }` для каждого используемого источника, содержащего настройки, начиная с самого низкого [приоритета](https://code.claude.com/docs/ru/settings.md#settings-precedence). См. [Что получает хук `settings.read`](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-receives).
* **`e.source`**: единственный источник, который запросил мод, например `$.settings.read({ source: 'policy' })`. Отсутствует при собственном чтении Claude Code и при чтении объединённых настроек

### Ходы

События ходов отслеживают один ответ от начала до конца, включая каждый запрос к модели в его рамках:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`turn.start`](https://code.claude.com/docs/ru/plugins/mods/events#follow-a-turn) | Начинается ход | `next(e)` |
| [`turn.step`](https://code.claude.com/docs/ru/plugins/mods/events#follow-a-turn) | Один запрос вот-вот отправится модели | `yield* next(e)` или `next({ ...e, model })`, `next({ ...e, effort })` |
| [`turn.complete`](https://code.claude.com/docs/ru/plugins/mods/events#follow-a-turn) | Ход завершился | `next(e)` или `{ text }`, чтобы показать строку под ответом |

### Сессия

События сессии отмечают запуск, завершение и сжатие сессии, а также обмен сообщениями с другими сессиями:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`session.start`](https://code.claude.com/docs/ru/plugins/mods/api#add-a-command-or-a-tool) | Один раз для каждого загруженного мода, перед первым промптом, и снова после перезагрузки этого мода. Не срабатывает после `/clear`, `/resume` или `/branch`. | `next(e)` |
| `session.end` | Сессия завершается или выполняется `/clear`, `/resume` либо `/branch`. `e.reason` — это `clear`, `resume`, `logout`, `prompt_input_exit` или `other`. `/branch` сообщает `resume`. | `next(e)` |
| `session.compact` | Диалог вот-вот будет сжат | `{ skip: reason }` |
| [`session.receive`](https://code.claude.com/docs/ru/plugins/mods/api#send-and-receive-messages-between-sessions), [`session.send`](https://code.claude.com/docs/ru/plugins/mods/api#send-and-receive-messages-between-sessions) | Сообщение приходит от другого агента или сессии либо вот-вот будет отправлено другому агенту или сессии. См. [Отправка и получение сообщений между сессиями](https://code.claude.com/docs/ru/plugins/mods/api.md#send-and-receive-messages-between-sessions). | `{ consumed: reason }` для `receive`, `{ isDelivered: false, reason }` для `send` |
| `session.append` | Один раз для каждой строки, которую сохраняет диалог, например промпта, блока ответа, результата инструмента или уведомления, перед её сохранением | `next({ ...e, message })` с изменённым `message.content`, чтобы переписать текстовые блоки строки или `content` блока `tool_result` в ней |
| `session.attach`, `session.detach` | Другое приложение подключается к сессии или отключается от неё | `next(e)` |
| `session.measure` | После каждого хода, а также когда меняется процент использования лимита тарифа | `next(e)` |

### Субагенты

События субагентов срабатывают, когда тип субагента предлагается Claude и когда субагент или участник команды агентов вот-вот запустится:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| `agent.offer` | Тип субагента предлагается Claude | `{ isOffered: false }`, чтобы скрыть его |
| `agent.spawn` | Субагент или участник [команды агентов](https://code.claude.com/docs/ru/agent-teams.md) вот-вот запустится, либо субагент, который завершил работу или был остановлен, вот-вот снова запустится. Для участника команды `e.isTeammate` равно `true`. Для возобновлённого запуска задано `e.resume`. | `next({ ...e, model })`, чтобы выбрать модель того, кто запускается, или `{ deny: reason }` |

Ваш хук `agent.spawn` также запускается, когда субагент, который завершил работу или был остановлен, вот-вот снова запустится, например когда Claude отправляет ему сообщение с помощью инструмента [`SendMessage`](https://code.claude.com/docs/ru/sub-agents#resume-subagents). В этом событии `e.resume` равно `{ agentId }`. Если ваш хук подсчитывает субагентов, пропускайте события, в которых задано `e.resume`, чтобы возобновлённый субагент не учитывался повторно.

Верните `{ deny: reason }`, чтобы отклонить возобновлённый запуск. Запуск не начинается, и субагент остаётся в прежнем состоянии. Если запуск запросил вызов `SendMessage`, Claude читает в качестве результата этого вызова `a plugin declined the resume:`, за которым следует ваша причина. Если для возобновлённого запуска вы передаёте в `next` изменённое событие, например с другой `model`, Claude Code игнорирует это изменение.

> [!NOTE]
>
> Событие для возобновлённого запуска требует Claude Code v2.1.299 или новее. До v2.1.299 ваш хук `agent.spawn` не запускался при возобновлении субагента. В этих версиях, чтобы отклонять вызовы `SendMessage`, которые возобновляют субагента, сопоставляйте этот инструмент в хуке [`tool.call`](https://code.claude.com/docs/ru/plugins/mods/events#guard-or-change-a-tool-call).

### Интерфейс

События интерфейса срабатывают, когда Claude Code рисует точку отрисовки и когда пользователь использует элемент управления, нарисованный модом. В разделе [Рисование в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md) показано, что возвращает хук `ui.render`:

| Событие | Срабатывает, когда |
| :- | :- |
| [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/interface#pick-where-to-draw) | [Точка отрисовки](#render-sites) вот-вот будет нарисована |
| `ui.resolve` | Загружаются моды, один раз для каждого приложения, точки отрисовки и мода. Результат — таблица элементов, которую читает `$.ui.resolve(e)`. |
| [`ui.press`](https://code.claude.com/docs/ru/plugins/mods/interface#respond-to-presses-and-typing), [`ui.input`](https://code.claude.com/docs/ru/plugins/mods/interface#respond-to-presses-and-typing), [`ui.select`](https://code.claude.com/docs/ru/plugins/mods/interface#respond-to-presses-and-typing) | Используется `Button`, `Input` или `Select`, нарисованный модом |
| `ui.focus`, `ui.scroll` | Вот-вот изменится элемент управления в фокусе или позиция прокрутки панели или полосы |
| `ui.close` | Панель вот-вот закроется. `e.id` — это панель, а `e.origin.kind` — `plugin`, `person` или `unload`. |
| [`ui.message`](https://code.claude.com/docs/ru/plugins/mods/interface#build-a-tree-from-elements) | Элемент `Client` отправляет данные своему моду |
| [`ui.fault`](https://code.claude.com/docs/ru/plugins/mods/interface#redraw-when-something-changes) | Элемент `Client`, нарисованный вашим модом, не удалось загрузить, отрисовать или запустить. `e.phase` — это `load`, `render` или `run`, а `e.reason` — сообщение об ошибке. Требуется Claude Code v2.1.289 или новее. |

### Другие моды

Эти события позволяют моду воздействовать на другие моды при их загрузке: отклонить мод или изменить получаемый им API модов:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| [`plugin.register`](https://code.claude.com/docs/ru/plugins/mods/admin#enforce-a-policy-with-a-mod-of-your-own) | Модуль хуков вот-вот загрузится. `e.uses` перечисляет его события, вызовы API модов, переменные окружения и состояние в том виде, в каком их выводит `claude plugin validate`. Каждый вызов записан без префикса `$.`, например `fs.read`. | `{ refuse: reason }` |
| `engine.create` | Для этого мода строится API модов | Изменённый API модов, чтобы добавить пространство имён. Мод вне [уровня](#the-hook-function) `user` также может скрыть его. |

Когда хук другого мода вызывает метод пространства имён, которое вы добавили в `engine.create`, вызовы `$` вашего метода выполняются в контексте этого хука, пока все хуки на этом событии не вернут результат. Например, относительный путь разрешается относительно рабочего каталога этого хука, а `$.prompt.submit` отклоняется, пока ход ожидает этот хук. Вызовы, которые ваш метод делает после этого, выполняются в собственном контексте вашего мода.

### Телеметрия

События телеметрии срабатывают для записей об использовании, которые логирует Claude Code:

| Событие | Срабатывает, когда | Хук может вернуть |
| :- | :- | :- |
| `telemetry.log`, `telemetry.mark` | Запись телеметрии вот-вот будет записана в лог или отмечено одно использование функции. В устанавливаемом моде задайте хуку телеметрии фильтр `{ to: 'collector' }`, например `on('telemetry.log', { to: 'collector' }, hook)`. Без фильтра мод не проходит `claude plugin validate`. `*` не соответствует этим событиям. | `next(e)` или `{ deny: reason }` |

### События хуков настроек

Каждое [событие хука настроек](https://code.claude.com/docs/ru/hooks.md#hook-events) — это событие с именем `classic.<Event>`, например `classic.Stop` или `classic.PostToolUse`. `e` — это JSON, который хук получает через stdin.

### Вызовы API модов

Каждый [метод API модов](#mods-api-methods) также является событием, названным по его пространству имён и методу, например `fs.read`, `model.complete` или `ui.open`. Хук на такое событие может вернуть `next(e)`, `{ deny: reason }` или `{ value }`.

Некоторые из этих событий срабатывают и для собственных действий Claude Code, поэтому, прежде чем отклонять такое событие, проверьте, равно ли `next.origin.plugin` значению `engine`.

#### Поля собственных запросов `http.fetch` Claude Code

В хуке `http.fetch` значение [`next.origin`](#the-hook-function), равное `{ plugin: 'engine', tier: 'core' }`, отмечает один из собственных запросов Claude Code, например запрос к модели, а не вызов `$.http.fetch` мода. Там, где загружен [встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), ваш хук не получает эти события, за исключением случаев, когда ваш мод [считается модом вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods).

В этих событиях `e.init` и `value`, в которое разрешается `next(e)`, могут содержать, среди прочего, следующие поля:

| Поле | Что означает |
| :- | :- |
| `e.init.compress` | Задано, когда Claude Code сжимает тело после вашего хука. `e.init.body` содержит несжатое тело. Чтобы отправить тело без сжатия, вызовите `next({ ...e, init: { ...e.init, compress: undefined } })`. |
| `value.isStreaming` | Равно `true`, потому что Claude Code сам читает тело ответа, поэтому `value.text` пусто. Вместо этого читайте `value.status` и `value.headers`. Чтобы ответить собственным `text`, верните `value` без `isStreaming`. |

Эти события и поля требуют Claude Code v2.1.321 или новее.

## Методы API модов

API модов — это аргумент `$`, который получает каждый хук. Его методы сгруппированы по пространствам имён, например `$.ui`. В этой таблице методы каждого пространства имён перечислены по имени, поэтому `open` в строке `$.ui` — это вызов `$.ui.open(...)`. В руководствах показано использование распространённых методов, а в [типах для вашей сборки](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build) каждый метод документирован с примером.

| Пространство имён | Методы |
| :- | :- |
| `$.plugin` | `name`, `root`: имя и каталог этого плагина |
| [`$.ui`](https://code.claude.com/docs/ru/plugins/mods/interface#pick-where-to-draw) | `resolve`, `invalidate`, `open`, `close`, `panes`, [`place`](https://code.claude.com/docs/ru/plugins/mods/interface#place-a-row-in-the-transcript), `focus`, `scroll`, `toast`, `notify`, `status`, `log`, `notice`, `ask`, `copy`, `selection`, `blit`, `view`. `view` требует Claude Code v2.1.300 или более поздней версии, а `place` — v2.1.314 или более поздней версии. |
| [`$.theme`](https://code.claude.com/docs/ru/plugins/mods/interface#put-a-backdrop-behind-the-conversation) | `set`, `clear`: задать фон, который будет отрисовывать приложение Desktop или мобильное приложение, и убрать этот фон. Требует Claude Code v2.1.319 или более поздней версии. |
| [`$.command`](https://code.claude.com/docs/ru/plugins/mods/api#add-a-command) | `register`, `run`, `list` |
| [`$.tool`](https://code.claude.com/docs/ru/plugins/mods/api#add-a-tool) | `register`, `call`, `check`, `list`. Когда `call` требует подтверждения человеком, например если хук или ваша организация отвечает на него `ask`, он завершается с результатом `{ deny: "<tool> wasn't run: this call needs a person's approval, and a mod's own call can't ask for it." }`, где `<tool>` — имя инструмента. |
| `$.agent` | `register`, `spawn`, `list`. `list()` возвращает субагентов и участников команды агентов этой сессии, у каждого из которых есть `status` со значением `pending`, `running`, `waiting`, `idle`, `completed`, `failed` или `killed`, причём `idle` и `waiting` требуют Claude Code v2.1.289 или более поздней версии. |
| [`$.model`](https://code.claude.com/docs/ru/plugins/mods/api#call-a-model) | `complete`, `fork`, `classify` |
| [`$.prompt`](https://code.claude.com/docs/ru/plugins/mods/api#start-a-turn-from-a-background-job) | `submit`, `read`, `fill`, `suggest`, `compose`. Claude читает текст из `submit({ text })` после предложения, называющего ваш мод отправителем. `submit({ text, asUser: true })` отправляет текст как собственные слова пользователя, без этого предложения. |
| `$.turn` | `abort` |
| [`$.session`](https://code.claude.com/docs/ru/plugins/mods/api#send-and-receive-messages-between-sessions) | `messages`, `cwd`, `root`, `model`, `turns`, `id`, `repo`, `surfaces`, `usage`, `version`, `compact`, `send`, `append`, `authorize`. `usage()` возвращает `{ startedAt, context, rateLimits, cost }`: `context` содержит `tokens`, `window` и `percent`, а `rateLimits` — это список `{ kind, percentUsed, resetsAt }`. |
| `$.config` | `list`, `set` |
| [`$.settings`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `read` |
| [`$.env`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `get`, `set` |
| [`$.fs`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `read`, `write`, `list`, `exists`, `stat`, `ancestors`. `write` не атомарен: он заменяет содержимое файла на месте, поэтому другой процесс может прочитать частично записанный файл. Храните данные, которые изменяют несколько сессий, в `$.store`. |
| [`$.store`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state) | `get`, `set`, `delete`, `keys`. Хранилище «ключ–значение», общее для всех сессий на машине. См. [Сохранение из нескольких сессий](https://code.claude.com/docs/ru/plugins/mods/interface.md#save-from-more-than-one-session). |
| [`$.state`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-a-value-in-\$-state) | Реактивное состояние: `get`, `set`, со вспомогательными функциями `atom`, `read`, `update`, `derive` и `memberOf`, импортируемыми из `claude-code` |
| [`$.clock`](https://code.claude.com/docs/ru/plugins/mods/api#run-work-in-the-background) | `now`, `sleep`, `after`, `every` |
| [`$.http`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `fetch` |
| [`$.process`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `run`, `spawn` |
| [`$.mcp`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) | `call`, `connect`. `connect(server)` подключает MCP-сервер, указанный в манифесте вашего собственного плагина. |
| `$.audio` | `play`, `speak` |
| `$.telemetry` | `log`, `mark`. Запись отправляется, только если вызов делает Claude Code или встроенный мод. |

## Точки отрисовки

Точка отрисовки — это точка расширения в интерфейсе Claude Code. Каждая строка — это значение `e.component` в хуке `ui.render` с полями `e.props` и приложениями, которые её отрисовывают. `e.surface` указывает приложение, которое выполняет отрисовку, например `terminal`, `desktop` или `vscode`. В разделе [Изменение того, что уже рисует Claude Code](https://code.claude.com/docs/ru/plugins/mods/interface.md#change-what-claude-code-already-draws) показано, что хук может делать в точке отрисовки, с примером для каждого варианта.

Для отрисовки в расширении VS Code требуется расширение версии 2.1.299 или новее. Сессии, которая [не получает флаги функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching), требуется версия 2.1.304 или новее. В разделе [Рисование в расширении VS Code](https://code.claude.com/docs/ru/plugins/mods/interface.md#draw-in-the-vs-code-extension) перечислено, что расширение рисует иначе.

| Точка | `e.props` | `e.requestId` | Отрисовывается в |
| :- | :- | :- | :- |
| [`Pane`](https://code.claude.com/docs/ru/plugins/mods/interface#pick-where-to-draw) | `title`, `isFocused`, `bodyColumns`, `placement`, `scroll`, `view` | `id` панели | Terminal, Desktop, VS Code |
| [`AbovePrompt`](https://code.claude.com/docs/ru/plugins/mods/interface#pick-where-to-draw) | `hasSurvey`, [`isCollapsed`](https://code.claude.com/docs/ru/plugins/mods/interface#when-the-user-collapses-the-band), `isWorking`, `maxRows`, `bodyColumns`, `scroll`, `view` | Один экземпляр | Terminal, Desktop |
| `AbovePromptList`, стопка строк `AbovePrompt` | `rows` — список с одним `{ plugin, tree }` для строки каждого мода, а также пропсы `AbovePrompt` | Один экземпляр | Terminal, Desktop. Требуется Claude Code v2.1.323 или новее. |
| [`Placed`](https://code.claude.com/docs/ru/plugins/mods/interface#place-a-row-in-the-transcript) | `id`, `plugin`, `onScreen` | `requestId`, который вернул `$.ui.place` | Terminal |
| [`Backdrop`](https://code.claude.com/docs/ru/plugins/mods/interface#put-a-backdrop-behind-the-conversation) | `scene`, `plugin`, `glass`, `overrideColorScheme`. До v2.1.323 `scene` назывался `id`, а `overrideColorScheme` — `colorScheme`. | `backdrop` | Интерфейсы `desktop` и `mobile`. Ваш хук запускается, когда приложение Desktop или мобильное приложение запрашивает отрисовку фона. |
| `UserMessage` | `text`, `origin`, `isExpanded` и `task` или `from` в зависимости от источника | id отрисованной строки | Terminal, Desktop, VS Code |
| `AssistantMessage` | Текст ответа | id отрисованной строки | Terminal, Desktop, VS Code |
| `ToolUse`, `ToolResult`, `ToolGroup` | Имя, входные данные и результат инструмента | id вызова инструмента | Terminal, Desktop, VS Code |
| `CommandOutput` | `command`, `text` | id отрисованной строки | Terminal, Desktop |
| [`AskUserQuestion`](https://code.claude.com/docs/ru/plugins/mods/interface#change-what-claude-code-already-draws) | Вопрос и варианты | id вызова инструмента | Terminal, Desktop, VS Code |
| `ToolProgress` | `kind` | id вызова инструмента | Terminal |
| [`Spinner`](https://code.claude.com/docs/ru/plugins/mods/interface#change-what-claude-code-already-draws) | `word`, `message`, `suffix`, `mode` | id агента | Terminal, Desktop, VS Code |
| `TurnDuration` | `word`, `durationMs` | id отрисованной строки | Terminal |
| `InfoNotice` | `text`, `command` | `text` уведомления с префиксом `notice:` | Terminal |
| `SessionMode` | `modes` | Один экземпляр | Terminal, Desktop |
| `PromptHint` | `isDraft`, `isWorking`, `hint` | Один экземпляр | Terminal, Desktop |

`e.viewport` содержит `columns`, `rows` и `isFullscreen`. В терминале и в приложении Desktop он отсутствует, пока приложение не измерило своё окно. Там его `rows` — это высота всего окна, а не вашей панели. В расширении VS Code он присутствует всегда.

Чтобы подогнать дерево под точку отрисовки, читайте в хуке следующие пропсы:

* **Ширина `Pane` или полосы**: рисуйте по `e.props.bodyColumns`
* **Высота `Pane` рядом с транскриптом**: когда `e.props.placement` равно `'dock'`, `e.props.scroll.bodyRows` — это число строк, которые панель отводит под ваше дерево
* **Высота `Pane` над промптом**: когда `e.props.placement` равно `'inline'`, панель растёт вместе с вашим деревом до предела, а `bodyRows` — это этот предел. Чтобы запросить другой предел, см. [поле `rows` в `$.ui.open`](https://code.claude.com/docs/ru/plugins/mods/interface#open-a-pane-at-the-right-time).

Дерево, которое выше панели, прокручивается целиком.

## Элементы

Элементы — это строительные блоки дерева, которое возвращает хук `ui.render`, и вы получаете их из `$.ui.resolve(e)`. В разделе [Построение дерева из элементов](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-tree-from-elements) показаны распространённые элементы и то, как их рисует терминал, а в [галерее интерфейса](https://code.claude.com/docs/ru/plugins/mods/gallery.md) есть снимки экрана большинства из них. Галочка означает, что приложение умеет рисовать элемент.

| Элемент | Основные пропсы | Terminal | Desktop | VS Code |
| :- | :- | :-: | :-: | :-: |
| [`Box`](https://code.claude.com/docs/ru/plugins/mods/interface#build-a-tree-from-elements) | `key`, flex-раскладка, [`gap`, `padding`, `margin`](#box-spacing-steps), `width`, `height`, `minWidth`, `minHeight`, [`borderStyle`](#box-border-styles), `borderColor`, `borderDimColor`, `backgroundColor`, `position`, `top`, `left`, `right`, `bottom`, `overflow`, `display`, `hover` | ✓ | ✓ | ✓ |
| [`Text`](https://code.claude.com/docs/ru/plugins/mods/interface#build-a-tree-from-elements) | `color`, `backgroundColor`, [`bold`](#text-bold), `italic`, `underline`, `strikethrough`, `dimColor`, `inverse`, `wrap`, [`size`, `weight`, `mono`, `tabular`](#text-typography), `hover` | ✓ | ✓ | ✓ |
| [`Button`](https://code.claude.com/docs/ru/plugins/mods/interface#respond-to-presses-and-typing) | `key`, `label`, `children`, `onPress`, `hotkey`, `plain`, `dimColor`, `autoFocus`, `action`, `variant`, `role`, `hover` | ✓ | ✓ | ✓ |
| [`Link`](https://code.claude.com/docs/ru/plugins/mods/interface#link-in-the-desktop-app) | `href`, `label`. См. [Ограничения](#limits). | ✓ | ✓ | ✓ |
| [`Code`](https://code.claude.com/docs/ru/plugins/mods/gallery#show-code-and-changes) | `source`, `language`, `path`, `startLine`, `format`, `wrap` | ✓ | ✓ | ✓ |
| `Markdown` | `text`, `key`, `dimColor`, `onLinkPress`, `pressableLinks` | ✓ | ✓ | ✓ |
| [`Input`](https://code.claude.com/docs/ru/plugins/mods/interface#take-typed-input-and-draw-a-row-for-each-item) | `key`, `label`, `placeholder`, `value`, `submitLabel`, [`rows`](https://code.claude.com/docs/ru/plugins/mods/gallery#input), `onSubmit`, `onInput`, `autoFocus` | ✓ | ✓ | ✓ |
| `Select` | `key`, `label`, `options`, `value`, `onSelect`, `autoFocus` | ✓ | ✓ | ✓ |
| `Svg` | `source` с SVG-разметкой до 131 072 символов, текст `alt`, `width`, `height` и `isInteractive` | | ✓ | ✓ |
| [`Client`](https://code.claude.com/docs/ru/plugins/mods/interface#build-a-tree-from-elements) | `module`, `key`, `props`, `width`, `height`, `flexGrow` | ✓ | ✓ | |
| [`Raster`](https://code.claude.com/docs/ru/plugins/mods/interface#draw-a-grid-of-colored-cells) | `key`, `columns` до 512, `rows` до 256, `cells`. См. [Рисование сетки цветных ячеек](https://code.claude.com/docs/ru/plugins/mods/interface.md#draw-a-grid-of-colored-cells). | ✓ | | |
| `Image` | `key`, `source`, например байты PNG или RGBA до 2 МиБ либо путь к файлу, `columns` и `rows` до 255, а также текст `alt`. См. [какие терминалы его рисуют](https://code.claude.com/docs/ru/plugins/mods/gallery.md#image-and-client). | ✓ | | |

Дополнительные правила для `Button`:

* **`action`**: указывает одно из собственных [действий сочетаний клавиш](https://code.claude.com/docs/ru/keybindings.md) Claude Code, и сочетание, назначенное пользователем для этого действия, нажимает кнопку, если это аккорд или клавиша с модификатором
* **Цифровые горячие клавиши на полосе**: цифровой `hotkey` на кнопке в полосе также срабатывает, когда пользователь вводит только эту цифру в пустой промпт и делает паузу
* **Свёрнутая полоса**: пока полоса [свёрнута](https://code.claude.com/docs/ru/plugins/mods/interface.md#when-the-user-collapses-the-band), ни привязка `action`, ни горячая клавиша не нажимают кнопку в ней
* **Две кнопки с одной горячей клавишей**: если две ваши кнопки в одной отрисовке указывают один и тот же `hotkey`, он достаётся более поздней. О кнопке другого мода с той же клавишей см. [Горячие клавиши не работают](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#hotkeys-do-nothing).
* **`variant`**: `primary` или `secondary`, любое другое значение вызывает исключение. В терминале кнопка `primary` рисуется акцентным цветом, если она не `plain`.
* **`role`**: `dismiss` помечает кнопку закрытия, любое другое значение вызывает исключение. Само закрытие выполняйте в своём `onPress`. В полосе, содержащей текст и ряд кнопок, приложение Desktop может нарисовать первую кнопку `dismiss` в ряду как собственный элемент управления закрытием. Терминал рисует кнопку так же, как без `role`.

`Button` может содержать `children` вместо `label`:

* **Чем могут быть дочерние элементы**: строки и элементы `Text`, например имя, за которым следует приглушённая деталь, или цветная плашка. Claude Code отклоняет любые другие элементы внутри `Button`.
* **Имя кнопки**: `label` задаёт имя кнопки и по умолчанию равен тексту её дочерних элементов. Задайте `key` или `label` для кнопки, дочерние элементы которой не являются одной строкой.
* **В терминале**: дочерние элементы рисуются на месте метки, а нажатие в любом месте на них считается одним нажатием, поэтому каждую строку списка можно сделать одной кнопкой
* **В приложении Desktop и расширении VS Code**: кнопка рисует свой `label`

> [!NOTE]
>
> `Button` с дочерними элементами, отличными от одной строки, требует Claude Code v2.1.295 или более поздней версии.

`autoFocus` на любом элементе управления принимает только `true`, поэтому, чтобы отключить его, опустите этот проп.

Расширение VS Code игнорирует некоторые пропсы элементов и рисует элемент так, как если бы вы их не указали:

* **`Box`**: `position` вместе с его `top`, `left`, `right` и `bottom`, `alignSelf`, `borderDimColor` и `hover`
* **`Text`**: `size`, `mono`, `tabular` и `hover`
* **`Button`**: `hotkey`, `plain`, `autoFocus`, `action` и `hover`, поэтому там пользователь нажимает кнопку щелчком или клавишей Enter, когда кнопка в фокусе. Расширение также игнорирует `variant` и `role`.
* **`Code`**: `language`, `path`, `startLine`, `format` и `wrap`, поэтому код рисуется без цветов и номеров строк, а блок с `format: 'diff'` показывает необработанный текст diff
* **`Input` и `Select`**: `autoFocus`, а также `rows` у `Input`
* **`Svg`**: `isInteractive`

### Стили рамки `Box`

Чтобы нарисовать рамку вокруг `Box`, задайте для его `borderStyle` одно из этих имён, например `borderStyle: 'round'`. В каждой строке указано, что терминал рисует для этого имени, и показан верхний край рамки.

| `borderStyle` | Что рисует терминал | Верхний край |
| :- | :- | :- |
| `'single'` | Тонкие линии с прямыми углами | `┌──┐` |
| `'double'` | Двойные линии | `╔══╗` |
| `'round'` | Тонкие линии со скруглёнными углами | `╭──╮` |
| `'bold'` | Толстые линии | `┏━━┓` |
| `'singleDouble'` | Тонкие линии сверху и снизу, двойные линии по бокам | `╓──╖` |
| `'doubleSingle'` | Двойные линии сверху и снизу, тонкие линии по бокам | `╒══╕` |
| `'classic'` | ASCII-символы `+`, `-` и `\|` | `+--+` |
| `'arrow'` | Стрелки, указывающие внутрь `Box` | `↘↓↓↙` |
| `'dashed'` | Пунктирные линии с пустыми углами | `╌╌` |
| `'quote'` | Полоса `▎` вдоль левой стороны и пустые ячейки на остальных трёх сторонах | Пусто |

`Box`, у которого `borderStyle` указывает любое другое имя, например `'rounded'`, рисуется без рамки.

### Шаги отступов `Box`

Пропсы отступов `Box` — это `gap`, `columnGap`, `rowGap`, `padding`, `margin`, а также формы `padding` и `margin` для одной стороны и одной оси, например `paddingX` и `marginTop`. Каждый из них принимает число ячеек терминала, например `gap: 1`, или имя шага, например `gap: 'md'`. В терминале и расширении VS Code каждый шаг равен следующему числу ячеек:

| Шаг | Ячеек по горизонтали | Ячеек по вертикали |
| :- | :- | :- |
| `'xs'` | 1 | 0 |
| `'sm'` | 1 | 0 |
| `'md'` | 2 | 1 |
| `'lg'` | 3 | 1 |
| `'xl'` | 4 | 2 |

Если задать для `gap`, `padding` или `margin` шаг, он применяется сразу и по горизонтали, и по вертикали. Например, в терминале и расширении VS Code `padding: 'md'` означает две ячейки с каждой стороны и одну строку сверху и снизу.

Имена шагов требуют Claude Code v2.1.299 или более поздней версии. В более ранних выпусках дерево, в котором используется имя шага, не рисуется.

### Типографские пропсы `Text`

Задайте `size`, `weight`, `mono` или `tabular` для `Text`, чтобы запросить у приложения, рисующего ваше дерево, размер текста, насыщенность, моноширинный шрифт или цифры одинаковой ширины. Прежде чем полагаться на проп, проверьте, что делают с ним терминал и расширение VS Code. Если приложение игнорирует заданный вами проп, ваше дерево всё равно рисуется там, а текст выглядит так, как если бы вы этот проп не указали.

| Проп | Значения | В терминале | В расширении VS Code |
| :- | :- | :- | :- |
| `size` | `'caption'`, `'footnote'`, `'body'`, `'heading'` или `'title'` | Игнорируется: в терминале один размер текста | Игнорируется |
| `weight` | `'regular'`, `'medium'`, `'semibold'` или `'bold'` | `semibold` и `bold` рисуются полужирным текстом | `semibold` и `bold` рисуются полужирным текстом |
| `mono` | `true`, чтобы запросить моноширинный шрифт приложения | Игнорируется: терминал всегда моноширинный | Игнорируется, поэтому текст сохраняет собственный шрифт расширения |
| `tabular` | `true`, чтобы запросить цифры одинаковой ширины, чтобы число, обновляемое на месте, или столбец чисел оставались выровненными | Игнорируется: цифры в терминале и так занимают одну ячейку | Игнорируется |

Эти четыре пропса требуют Claude Code v2.1.299 или более поздней версии. В более ранних выпусках дерево, в котором задан `size`, `weight`, `mono` или `tabular`, не рисуется.

#### Замена `bold` на `weight`

`bold` для `Text` объявлен устаревшим в пользу `weight`, но по-прежнему работает. Чтобы заменить его для `Text` без `weight`, измените `bold: true` на `weight: 'semibold'` — в Claude Code v2.1.299 или более поздней версии результат будет тем же.

В выпусках до v2.1.299 дерево, в котором задан `weight`, не рисуется. Если задать для `Text` и `bold`, и `weight`, `bold` не действует.

## Ограничения

Хуки и вызовы API модов выполняются с ограничениями по времени и размеру. Claude Code пропускает хук, превысивший ограничение по времени. Дерево, превышающее ограничение по вложенности, числу элементов, ячейкам `Raster` или байтам `Image`, [не отрисовывается](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#a-pane-or-band-is-empty).

| Ограничение | Значение |
| :- | :- |
| Собственное время выполнения хука для одного события, без учёта времени внутри `next` или вызова API модов, кроме `$.clock.sleep` | 10 секунд или 50 миллисекунд для хука `prompt.edit` |
| Время выполнения обработчика `.catch` | 1 секунда |
| Все хуки `session.end` вместе | Столько же, сколько [бюджет хука SessionEnd](https://code.claude.com/docs/ru/hooks.md#sessionend-input), — 1,5 секунды, если вы его не измените; отсчёт начинается после завершения хуков `SessionEnd` из ваших настроек |
| Таймаут `$.process.run` | 30 секунд по умолчанию, не более 10 минут |
| `stdout` и `stderr` для `$.process.run` | По 4 МиБ каждый. `isStdoutTruncated` или `isStderrTruncated` имеет значение `true`, если соответствующий поток был обрезан. |
| `maxTokens` для `$.model.complete` | 1024 по умолчанию, до 64 000 или предела вывода модели |
| `$.fs.read` и `$.fs.write` | 4 МиБ на один файл |
| Тело запроса `$.http.fetch` | 4 МиБ, считается в символах. Вызов с более длинным телом отклоняется. |
| Тело ответа `$.http.fetch` | 4 МиБ. `text` содержит первые 4 МиБ, а остальное не считывается. Если заголовок `Content-Length` объявляет больший размер, вызов вместо этого отклоняется с причиной, оканчивающейся на `is over the 4194304-byte limit`, за исключением случая, когда последний запрос после всех перенаправлений использует метод `HEAD`. Исключение для `HEAD` требует Claude Code v2.1.296 или новее. |
| Один вызов `$.http.fetch`, включая перенаправления и тело | 30 секунд |
| Перенаправления, по которым проходит один вызов `$.http.fetch` | 5 |
| Причина `drop` хука или причина `deny` для `config.set` | 4 096 символов. Конец более длинной причины обрезается, а drop или deny всё равно применяется. Обрезка требует Claude Code v2.1.292 или новее; в более ранних версиях хук вместо этого [завершается с ошибкой](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails). |
| Текст в одном дереве | Отрисовываются первые 100 000 символов |
| `language` или `path` элемента `Code`, `value` варианта `Select` или `module` элемента `Client` | 10 000 символов. Если значение длиннее, хук `ui.render`, вернувший его, [завершается с ошибкой](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails). |
| `href` элемента `Link` | 2 048 символов. Если он длиннее, хук `ui.render`, вернувший его, [завершается с ошибкой](https://code.claude.com/docs/ru/plugins/mods/events.md#handle-a-hook-that-fails). |
| Глубина вложенности одного дерева | 32 уровня ниже корневого элемента |
| Элементы и текстовые дочерние узлы в одном дереве | 20 000 |
| Ячейки `Raster` в одном дереве: `columns` каждого `Raster`, умноженные на его `rows` | 262 144 |
| Строки над промптом, расположенные одна над другой | Элементы, ячейки `Raster` и байты `Image` суммируются по всем строкам и сравниваются с ограничениями для одного дерева |
| Байты PNG или RGBA всех элементов `Image` в одном дереве | 2 МиБ |
| `$.store` | 4 МиБ JSON в сумме |
| `$.session.messages()` | Последние 4 096 записей |
| Перерисовки `$.ui.invalidate('ui.render')` | Ограничены 10 в секунду или 30 в терминале для видимой панели, развёрнутой полосы и строки подсказки под промптом. Более частые вызовы объединяются. |
| `$.ui.toast` | Показывается 4 секунды, если не передать `{ timeoutMs }`. В [классическом рендерере](https://code.claude.com/docs/ru/fullscreen.md#enable-fullscreen-rendering) более новое всплывающее уведомление мода может [заменить его более старое уведомление](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#a-toast-doesn’t-appear), которое отображается или ожидает показа. |
| Панель, открытая без запроса пользователя | Размещается начиная со 144 столбцов терминала, со 110 — после того как пользователь однажды её открыл |
| Строки из `$.ui.place`, которые один мод одновременно имеет в диалоге | 500. При достижении ограничения вызов с новым `id` разрешается в `{ isPlaced: false, reason: 'a plugin holds at most 500 placed rows' }`. |
| Глубина вложенности аргументов вызова API модов | 28 000 уровней. При превышении вызов отклоняется с сообщением, оканчивающимся на `nesting deeper than 28000 levels is not supported`. Требуется Claude Code v2.1.299 или новее. |
| Глубина вложенности изменённого события, переданного в `next`, за пределами [хуков на основе асинхронных генераторов](#events), например хука на `turn.step` | 28 000 уровней. При превышении `next` отклоняется с сообщением, оканчивающимся на `nesting deeper than 28000 levels is not supported`. Требуется Claude Code v2.1.299 или новее. |
| Глубина вложенности возвращаемого значения хука, за пределами `ui.render`, `ui.resolve` и хуков на основе асинхронных генераторов | 28 000 уровней. При превышении результат хука отклоняется, а [уведомление, сообщающее об этом](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing), содержит `nesting deeper than 28000 levels is not supported`. Требуется Claude Code v2.1.299 или новее. |
| Области видимости, такие как функции, блоки и циклы, вложенные друг в друга в одном файле модуля хуков | 2 000 |
| Имена команд, инструментов, типов субагентов и панелей, `id` размещённой строки и `scene` фона | Буквы, цифры, `_` и `-`, до 64 символов |
| Один тест `claude plugin test` | 5 секунд, если тест не задаёт `timeoutMs` |

## Настройки и переменные окружения

Ниже перечислены настройки и переменные окружения, влияющие на моды. В столбце «Где» указано, из какого файла настроек или окружения читается каждая из них:

| Имя | Где | Что делает |
| :- | :- | :- |
| `CLAUDE_CODE_PLUGIN_DIRS` | Окружение или `env` в `~/.claude/settings.json` | Каталоги плагинов для загрузки так же, как это делает `--plugin-dir`, — для приложений, которым нельзя передать флаг. Абсолютные пути, разделённые `:`, или `;` в Windows. |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH` | Окружение | Перезагружаются ли моды при сохранении. Значения по умолчанию и допустимые значения см. в [справочнике по переменным окружения](https://code.claude.com/docs/ru/env-vars.md) |
| `prependPlugins`, `appendPlugins` | Управляемые настройки. Пользовательские настройки — только на машине без управляемых настроек и без файла [`managed-mcp.json`](https://code.claude.com/docs/ru/managed-mcp#deploy-managed-mcp-json), в сессии, учётные данные которой получены не через `/login` Team или Enterprise. | Списки id плагинов, например `acme-guard@acme-tools`. Моды из `prependPlugins` выполняются перед каждым модом, установленным пользователем, а моды из `appendPlugins` — после, в указанном порядке. См. [Порядок запуска модов](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in). |
| `allowManagedModsOnly` | Управляемые настройки, как [опция встроенного стража](https://code.claude.com/docs/ru/plugins/mods/admin.md#set-options-on-the-built-in-guard) | Свои хуки запускают только моды, которые [считаются модами вашей организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods), и моды, встроенные в Claude Code. Хуки настроек пользователей продолжают работать. |
| `allowModsToOverrideDenyRules` | Управляемые настройки, как [опция встроенного стража](https://code.claude.com/docs/ru/plugins/mods/admin.md#set-options-on-the-built-in-guard) | Позволяет моду, установленному пользователем, одобрить вызов инструмента в обход большинства [исходов, которые по умолчанию остаются в силе](https://code.claude.com/docs/ru/permissions.md#precedence-among-rules-hooks-and-mods), включая правило `deny` |
| `allowManagedHooksOnly` | Управляемые настройки | Блокирует хуки и установленные моды, не принадлежащие вашей организации. См. [что продолжает работать](https://code.claude.com/docs/ru/settings-reference.md#what-runs-under-allowmanagedhooksonly). |
| `disableAllHooks` | Любой файл настроек | В управляемых настройках не выполняется ни один мод или хук из установленного плагина. В ваших собственных настройках то, чем управляет ваша организация, продолжает работать. См. [`disableAllHooks`](https://code.claude.com/docs/ru/settings-reference#disableallhooks). |
| `disableSideloadFlags` | Управляемые настройки | Отклоняет `--plugin-dir` и `--plugin-url` при запуске |
| `pluginConfigs` | Пользовательские или управляемые настройки | Содержит значения `userConfig` для мода с ключом по id плагина, например `acme-guard@acme-tools`, или по его имени и `@inline`, например `first-mod@inline`, для мода, загруженного с `--plugin-dir` |

`sec-default@builtin` — это страж, встроенный в Claude Code, который отображается как `cc-plugin-sec-default` в `/plugin` и в отладочном логе. [Там, где он загружается](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), он выполняется перед каждым модом, установленным человеком. Если задан управляемый `prependPlugins`, страж загружается, только если этот список его называет, на указанной позиции.

Его исходный код находится в [каталоге `mods/sec-default` репозитория Claude Code](https://github.com/anthropics/claude-code/tree/main/mods/sec-default).

## Команды

Эти команды и флаги загружают, проверяют и тестируют мод. Команды `claude` выполняются в вашей оболочке, а команды `/` — в промпте Claude Code. В таблице `<directory>` обозначает путь, который вы вводите, например `claude plugin validate ./first-mod`. Квадратные скобки обозначают необязательный аргумент.

| Команда | Что делает |
| :- | :- |
| [`/plugin`](https://code.claude.com/docs/ru/plugins/mods/overview#see-which-mods-a-session-loaded) | Показывает под своими вкладками строку вида `1 mod active · first-mod`, когда загружен мод, не являющийся встроенным |
| [`claude plugin validate <directory>`](https://code.claude.com/docs/ru/plugins/mods/create#check-what-claude-code-reads-from-your-mod) | Читает манифест и модуль хуков плагина и сообщает об ошибках, обрабатываемых событиях и вызовах API модов. `--strict` считает предупреждения ошибками, а `--json` выводит машиночитаемый отчёт. |
| [`claude plugin test [directory]`](https://code.claude.com/docs/ru/plugins/mods/test#write-a-test) | Запускает все файлы в каталоге (или в текущем каталоге, если он не указан), имена которых заканчиваются на `.test.ts` или `.test.tsx`. Завершается с кодом 1, если тест не проходит. |
| [`claude --plugin-dir <directory>`](https://code.claude.com/docs/ru/plugins/mods/create#write-a-mod-yourself) | Загружает каталог плагина на одну сессию и перезагружает его модуль хуков при сохранении. Повторите флаг, чтобы загрузить несколько. |
| `/reload-plugins` | Перезагружает плагины при запуске |
