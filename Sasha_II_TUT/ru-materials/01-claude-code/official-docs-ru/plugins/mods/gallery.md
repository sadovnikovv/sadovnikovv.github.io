> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Галерея элементов интерфейса для модов

> Посмотрите, какие элементы интерфейса может отрисовывать мод Claude Code: текст, кнопки, поля, Markdown, код и diff, — с примерами кода и снимками экрана терминала.

Мод строит свой интерфейс из элементов: текста, блоков, кнопок, полей и нескольких элементов, которые форматируют содержимое за вас. Примеры на этой странице показывают код, отрисовывающий элемент, и к большинству из них приложен снимок экрана с результатом на панели терминала, поэтому элемент можно выбрать по его внешнему виду.

Чтобы разобраться, как работает отрисовка, начните с раздела [Отрисовка в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md). Основные свойства элементов и приложения, которые отрисовывают каждый из них, описаны в [справочнике по элементам](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements). В [объявлениях типов](https://code.claude.com/docs/ru/plugins/mods/create.md#get-the-types-for-your-build) перечислены все свойства.

## Попробуйте пример

Примеры на этой странице — это фрагменты, а не готовые моды. Каждый из них — код одного элемента и всего, что в него вложено.

Чтобы посмотреть пример в своём терминале, создайте небольшой мод, следуя этим шагам, и вставьте в него пример. Мод добавляет команду `/gallery`, которая открывает панель и отрисовывает в ней пример. [Панель](https://code.claude.com/docs/ru/plugins/mods/interface.md#pick-where-to-draw) — это боковая область рядом с транскриптом в широком полноэкранном терминале, а в остальных случаях — область в рамке над промптом.

**1. Создайте мод**

Создайте каталог `gallery`, а внутри него — каталоги `.claude-plugin` и `hooks`. Назначение файлов объясняется в разделе [Создание мода](https://code.claude.com/docs/ru/plugins/mods/create.md#write-a-mod-yourself).

Сохраните манифест как `gallery/.claude-plugin/plugin.json`:

```json gallery/.claude-plugin/plugin.json theme={null}
{
  "name": "gallery",
  "version": "0.1.0",
  "description": "Opens a pane that draws one sample",
  "author": { "name": "Your Name" }
}
```

Укажите точку входа в `gallery/hooks/hooks.json`:

```json gallery/hooks/hooks.json theme={null}
{
  "modules": ["./register.js"]
}
```

Сохраните код как `gallery/hooks/register.js`. Он добавляет команду `/gallery`, которая открывает панель, и отрисовывает в ней `Plain text`:

```javascript gallery/hooks/register.js theme={null}
// Stands in for your own callback in the samples that take one
const noop = () => {}
// The Select sample keeps its choice here
let picked = 'md'

// The Raster sample packs its cells with this function
const DEFAULT_COLOR = 0x01000000
function cellsOf(rows) {
  const numbers = rows.flat().flatMap(([char, color]) => [char.codePointAt(0), color, DEFAULT_COLOR])
  return new Uint8Array(Uint32Array.from(numbers).buffer).toBase64()
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'gallery', description: 'Open the sample pane' })
    return next(e)
  })

  on('command.run', { command: 'gallery' }, async ($) => {
    await $.ui.open({ id: 'gallery', focus: true, closeOnEscape: true })
    return {}
  })

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    if (e.requestId !== 'gallery') return next(e)
    const { Box, Text, Button, Input, Select, Link, Markdown, Code, Raster, Svg } = $.ui.resolve(e)
    // Replace the element after return with a sample
    return Text({ children: ['Plain text'] })
  })
}
```

**2. Запустите мод**

В оболочке запустите Claude Code из каталога, содержащего `gallery`:

```bash theme={null}
claude --plugin-dir ./gallery
```

В промпте Claude Code выполните `/gallery`. Откроется панель с текстом `Plain text`.

**3. Подставьте пример**

Скопируйте пример с этой страницы. В `register.js` вставьте его вместо `Text({ children: ['Plain text'] })`, чтобы он шёл после `return`, и сохраните файл. Claude Code перезагружает модуль при каждом сохранении, поэтому снова выполните `/gallery`, чтобы увидеть новый пример.

## Выберите элемент

Примеры сгруппированы по тому, что вы хотите вывести на экран:

* **[Вывод текста](#show-text)**: `Text`, `Markdown` и `Link`
* **[Вывод кода и изменений](#show-code-and-changes)**: `Code`
* **[Компоновка элементов](#arrange-elements)**: `Box`
* **[Ввод данных](#take-input)**: `Button`, `Input` и `Select`
* **[Рисование изображений](#draw-pictures)**: `Raster`, `Svg`, `Image` и `Client`

## Вывод текста

Текст на экран выводят три элемента: `Text` — с вашим собственным оформлением, `Markdown` — для уже отформатированного содержимого и `Link` — для URL.

### `Text`

`Text` отрисовывает строку с заданными вами стилями. В этом примере показаны обычный текст и восемь стилей, каждый на отдельной строке:

```javascript theme={null}
Box({
  flexDirection: 'column',
  children: [
    Text({ children: ['Plain text'] }),
    Text({ bold: true, children: ['bold'] }),
    Text({ italic: true, children: ['italic'] }),
    Text({ underline: true, children: ['underline'] }),
    Text({ strikethrough: true, children: ['strikethrough'] }),
    Text({ dimColor: true, children: ['dimColor'] }),
    Text({ inverse: true, children: ['inverse'] }),
    Text({ color: 'red', children: ["color: 'red'"] }),
    Text({ backgroundColor: 'blue', children: ["backgroundColor: 'blue'"] }),
  ],
})
```

![Панель с девятью строками текста, каждая из которых названа по своему стилю: обычный, bold, italic, underline, strikethrough, dimColor серым цветом, inverse, color red и backgroundColor blue.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-text-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=90724ce3953d9347b61b6a9266fda451)

`dimColor` отрисовывает текст серым цветом. `backgroundColor` заливает фон только по ширине текста.

### `Markdown`

`Markdown` форматирует текст так же, как форматируются ответы Claude. Передавайте содержимое в `text`, а не в `children`:

```javascript theme={null}
Markdown({
  text: '## Release notes\n\nThis build has **two** fixes and one `flag`:\n\n- Faster start\n- Fewer prompts\n\n> Quoted text',
})
```

![Панель с жирным заголовком Release notes, затем предложение с одним жирным словом и одним цветным словом кода, список из двух пунктов и цитата курсивом с чертой слева.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-markdown-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=e40eacc4e3fbe06eb003f4463f552ec1)

Заголовок отрисовывается жирным шрифтом без знаков `#`. Встроенный код отрисовывается цветом без обратных кавычек. Цитата отрисовывается курсивом с чертой слева.

### `Link`

`Link` отрисовывает подпись, а за ней — её URL:

```javascript theme={null}
Link({ href: 'https://code.claude.com/docs', label: 'Claude Code docs' })
```

![Панель с одной строкой: подпись Claude Code docs, а затем URL серым цветом.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-link-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=8217bd2dfb561a8ba57023c6d89ea977)

Терминал отрисовывает URL как текст после подписи. Откроется ли он по щелчку, зависит от терминала пользователя.

## Вывод кода и изменений

`Code` отрисовывает исходный текст с подсветкой синтаксиса в цветах самого Claude Code или diff. В расширении VS Code `Code` показывает свой `source` как обычный текст, без цветов, номеров строк и подсветки diff, которые видны на этих снимках экрана.

### `Code`

Укажите язык в `language` или передайте `path`, чтобы Claude Code определил язык по нему. С `startLine` строки нумеруются начиная с этого числа:

```javascript theme={null}
Code({
  language: 'javascript',
  startLine: 1,
  source: "const name = 'mods'\nconsole.log('hello ' + name)",
})
```

![Панель с двумя пронумерованными строками JavaScript с подсветкой синтаксиса.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-code-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=4e13f5d506d3fdcc59d6d9524f48d2a9)

Цвета берутся из темы пользователя.

### `Code` в виде diff

С `format: 'diff'` в `source` передаются один или несколько фрагментов (hunks) в формате unified diff:

```javascript theme={null}
Code({
  format: 'diff',
  source: '@@ -1,3 +1,3 @@\n # Mods\n-A mod is a plugin.\n+A mod is a plugin that runs code.\n Read on.',
})
```

![Панель с diff из четырёх строк. Удалённая строка подсвечена красным, добавленная — зелёным, у каждой указан номер строки. В добавленной строке слова that runs code подсвечены ярче.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-diff-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=4f12c9f7229ceccd9b4f47479a7235dd)

Вместо строки `@@` Claude Code отрисовывает номера строк. Если удалённая и добавленная строки похожи, изменившиеся слова подсвечиваются ярче.

## Компоновка элементов

### `Box`

`Box` располагает своё содержимое в строку или в столбец и может отрисовывать рамку. В этом примере над блоком в рамке размещается строка слов:

```javascript theme={null}
Box({
  flexDirection: 'column',
  gap: 1,
  children: [
    Box({
      flexDirection: 'row',
      columnGap: 4,
      children: [Text({ children: ['a row'] }), Text({ children: ['of three'] }), Text({ children: ['items'] })],
    }),
    Box({
      borderStyle: 'round',
      paddingX: 1,
      children: [Text({ children: ["borderStyle: 'round'"] })],
    }),
  ],
})
```

![Панель с тремя словами в строку на расстоянии четырёх столбцов друг от друга, затем пустая строка, затем скруглённая рамка вокруг одной строки текста. Рамка занимает всю ширину панели.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-box-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=cb9263bb02f5c8afb6e5b8450e0cdadc)

Рамка растягивается на всю ширину панели.

## Ввод данных

`Button`, `Input` и `Select` — это элементы управления: пользователь переходит между ними клавишей Tab и работает с тем, на котором находится фокус. Какие клавиши до них доходят, описано в разделе [Фокус клавиатуры и горячие клавиши](https://code.claude.com/docs/ru/plugins/mods/interface.md#know-which-keys-your-mod-can-receive).

Откройте панель с `focus: true`, чтобы она попыталась получить фокус клавиатуры. Вводимые буквы попадают в `Input`, как только на нём оказывается фокус. Как выбрать поле, которое получит фокус при открытии панели, описано в разделе [Горячая клавиша и первый фокус](https://code.claude.com/docs/ru/plugins/mods/interface.md#set-a-hotkey-and-the-first-focus).

### `Button`

Кнопка вызывает `onPress`. В этом примере показаны кнопка по умолчанию, кнопка `plain` с горячей клавишей и приглушённая кнопка:

```javascript theme={null}
Box({
  flexDirection: 'column',
  children: [
    Button({ key: 'save', label: 'Save', onPress: noop }),
    Button({ key: 'next', label: 'Next', hotkey: 'n', plain: true, onPress: noop }),
    Button({ key: 'skip', label: 'Skip', dimColor: true, onPress: noop }),
  ],
})
```

![Панель с тремя кнопками, по одной в строке: Save в скобках, n: Next без скобок с цветной буквой n и Skip в скобках серым цветом.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-button-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=8c638c15e12d9736f327dfcaa797b512)

Кнопка с фокусом отрисовывается в инверсных цветах. Здесь пользователь дважды нажал Tab:

![Те же три кнопки, вторая из которых, n: Next, отрисована в инверсных цветах.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-button-plain-focused-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=a6224e58d10752a894615047d9824ad9)

### `Input`

`Input` — это текстовое поле, которое по умолчанию содержит одну строку и вызывает `onSubmit`, когда пользователь нажимает Enter:

```javascript theme={null}
Input({
  key: 'title',
  label: 'Title',
  placeholder: 'Type a title and press Enter',
  value: '',
  submitLabel: 'save',
  onSubmit: noop,
})
```

Без фокуса поле показывает подпись и текст-заполнитель:

![Панель с одной строкой: подпись Title, затем текст-заполнитель Type a title and press Enter серым цветом.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-input-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=7d580be1aaf5507032e1962b9167d725)

С фокусом подпись становится жирной, появляется курсор, а после `⏎` отображается `submitLabel`:

![То же поле с жирной подписью, блочным курсором на первой букве текста-заполнителя и знаком возврата, за которым следует слово save.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-input-focused-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=dcfcce0174480cc624d06c8521734fe7)

Ввод заменяет текст-заполнитель:

![То же поле с введёнными буквами Rel, за которыми следуют знак возврата и слово save.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-input-typed-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=4eb6d4443763a21415dad4e426bc747a)

Задайте для `rows` значение 2 или больше для поля, которое содержит несколько строк, например для заметки или сообщения коммита:

```javascript theme={null}
Input({
  key: 'note',
  label: 'Note',
  placeholder: 'Write a note',
  rows: 4,
  onSubmit: noop,
})
```

Строки отрисовывают терминал и приложение Desktop. В расширении VS Code поле содержит одну строку. Для `rows` требуется Claude Code v2.1.301 или новее. В более ранних версиях поле содержит одну строку.

Поле занимает заданное количество строк, даже если оно пустое, но не больше высоты панели или полосы, в которой оно отрисовано. Пока на поле находится фокус, более длинный текст прокручивается внутри него.

* В терминале Enter по-прежнему отправляет ввод. Там пользователь начинает новую строку, вводя обратную косую черту и затем нажимая Enter, или нажимая Shift+Enter, если [эмулятор терминала это поддерживает](https://code.claude.com/docs/ru/terminal-config.md#enter-multiline-prompts). Это те же клавиши, что и в промпте.
* В терминале клавиши Up и Down перемещают между строками поля. С первой и последней строки они переводят к предыдущему или следующему элементу управления.
* `onSubmit` и `onInput` получают весь текст, строки которого объединены через `\n`.

### `Select`

`Select` позволяет пользователю выбрать один из нескольких вариантов и вызывает `onSelect` со значением `value` выбранного варианта:

```javascript theme={null}
Select({
  key: 'format',
  label: 'Format',
  value: picked,
  options: [
    { value: 'md', label: 'Markdown' },
    { value: 'html', label: 'HTML' },
    { value: 'txt', label: 'Plain text' },
  ],
  onSelect: (value) => {
    picked = value
  },
})
```

В закрытом состоянии он показывает подпись и текущий вариант:

![Панель с одной строкой: подпись Format, текущий вариант Markdown и маленькая стрелка вниз.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-select-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=4e3b18268ffd87d2cad06442e6d661a9)

В открытом состоянии он показывает список вариантов и выделяет один из них:

![Открытый список выбора с тремя вариантами под подписью. Второй вариант, HTML, отрисован в инверсных цветах.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-select-moved-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=deb6ce0a49d213235feedaa79ac658c0)

После того как пользователь выберет вариант, список закрывается:

![Список выбора снова закрыт, и текущим вариантом теперь показан HTML.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-select-picked-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=f065ab5bc479868f03088dc736f17097)

## Рисование изображений

### `Raster`

`Raster` — это сетка цветных символьных ячеек для тепловой карты, спарклайна или игрового поля. Его отрисовывает терминал. В этом примере используется функция `cellsOf` из начального модуля, которая упаковывает ячейки в строку, принимаемую `Raster`. Подробнее см. в разделе [Отрисовка сетки цветных ячеек](https://code.claude.com/docs/ru/plugins/mods/interface.md#draw-a-grid-of-colored-cells):

```javascript theme={null}
Raster({
  key: 'grid',
  columns: 3,
  rows: 2,
  cells: cellsOf([
    [['█', 0x2e7d32], ['█', 0xf9a825], ['█', 0xc62828]],
    [['█', 0x2e7d32], ['█', 0x2e7d32], ['█', 0xf9a825]],
  ]),
})
```

![Панель с небольшой сеткой цветных блоков в две строки по три: зелёный, янтарный и красный, затем зелёный, зелёный и янтарный.](https://mintcdn.com/claude-code/EXkwf0kKMewZsyod/images/mods-el-raster-light.png?fit=max\&auto=format\&n=EXkwf0kKMewZsyod\&q=85\&s=5ed719481d3dd45b568bab696e57bf16)

`Raster` округляет каждый цвет до более ограниченной палитры, поэтому `0x2e7d32` отрисовывается как `#337733`.

### `Svg`

`Svg` отрисовывает SVG-документ в приложении Desktop и расширении VS Code:

```javascript theme={null}
Svg({
  alt: 'Three bars of rising height',
  width: 120,
  height: 60,
  source:
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60"><rect x="10" y="40" width="20" height="20" fill="#2e7d32"/><rect x="50" y="25" width="20" height="35" fill="#f9a825"/><rect x="90" y="5" width="20" height="55" fill="#c62828"/></svg>',
})
```

В терминале панель, которая возвращает только `Svg`, открывается пустой. Чтобы отрисовать там что-то другое, проверьте [`e.surface`](https://code.claude.com/docs/ru/plugins/mods/interface#pick-where-to-draw) и верните другое дерево.

### `Image` и `Client`

Для `Image` и `Client` примеров здесь нет. `Image` отрисовывает PNG или необработанные пиксели в терминале. `Client` — это область, которую отрисовывает ваш второй файл, для анимации и ввода указателем. Их пропсы перечислены в [справочнике по элементам](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements).

`Image` отрисовывается как картинка в следующих терминалах:

* kitty 0.28 или новее
* Ghostty
* iTerm2 3.5 или новее. Для отрисовки в iTerm2 требуется Claude Code v2.1.305 или новее.

В любом другом терминале пользователь увидит вместо картинки приглушённый текст `alt` элемента `Image`. Пишите текст `alt`, который понятен сам по себе, поскольку он также отображается, помимо прочего, в следующих случаях:

* **GNU screen**: сессия, запущенная внутри screen, в любом терминале.
* **tmux**: сессия, запущенная внутри tmux, для которой не выполнено одно из [требований для отрисовки внутри tmux](#draw-an-image-inside-tmux).
* **Фоновые сессии**: любая [фоновая сессия](https://code.claude.com/docs/ru/agent-view.md), из какого бы терминала к ней ни подключались.
* **iTerm2 без полноэкранной отрисовки**: в iTerm2 картинка отрисовывается только при [полноэкранной отрисовке](https://code.claude.com/docs/ru/fullscreen.md) и не отрисовывается, если для [`CLAUDE_CODE_ALT_SCREEN_FULL_REPAINT`](https://code.claude.com/docs/ru/env-vars) установлено значение `1`. Чтобы увидеть картинку, выполните `/tui fullscreen` в промпте Claude Code и не устанавливайте эту переменную.
* **Путь к файлу в качестве источника в iTerm2 или tmux**: в iTerm2 и внутри tmux элемент `Image`, у которого `source` указывает `file`, показывает текст `alt` вместо картинки. Если у вашего мода есть пользователи iTerm2 или tmux, передавайте картинку в base64 в `source.png` или `source.rgba`, а не как путь в `source.file`.

Если пользователи вашего мода видят приглушённый текст в терминале, который отрисовывает изображения протокола графики kitty с плейсхолдерами Unicode, они могут установить для [`CLAUDE_CODE_FORCE_TERMINAL_IMAGES`](https://code.claude.com/docs/ru/env-vars) значение `1`. Не следует устанавливать её внутри GNU screen, внутри tmux старше 3.3, во всплывающем окне tmux или при выключенной опции tmux `allow-passthrough`. В этих случаях пользователи не увидят картинку, а вместо текста `alt` увидят рамку.

#### Отрисовка `Image` внутри tmux

Если `Image` показывает текст `alt` внутри tmux, проверьте следующие требования, а также [другие случаи отображения текста `alt`](#image-and-client), например фоновую сессию:

* Claude Code v2.1.310 или новее
* tmux 3.3 или новее
* Claude Code запущен в панели tmux, а не во всплывающем окне tmux
* tmux запущен внутри kitty 0.28 или новее, Ghostty или iTerm2 3.5 или новее
* Опции tmux `focus-events` и `allow-passthrough` имеют значение `on`. Внутри kitty или Ghostty `allow-passthrough` также может иметь значение `all`.
* Внутри iTerm2 tmux запущен [без `-CC`](https://code.claude.com/docs/ru/fullscreen#use-with-tmux), [полноэкранная отрисовка](https://code.claude.com/docs/ru/fullscreen.md) включена, а `CLAUDE_CODE_ALT_SCREEN_FULL_REPAINT` не установлена.
* Внутри iTerm2 окно tmux не больше окна iTerm2. Чтобы проверить это, выполните `tmux display-message -p '#{window_bigger}'` в этом окне tmux. Если команда выводит `1`, подгоните размер окна tmux, затем перезапустите Claude Code.
* Автор мода передаёт картинку как байты `png` или `rgba`, а не как путь `file`. Если вы используете мод, который написали не вы, и остальные требования выполнены, попросите его автора проверить это требование.

Для каждой опции tmux, которая ещё не установлена как требуется, выполните соответствующую команду в оболочке:

```bash theme={null}
tmux set -g allow-passthrough on
tmux set -g focus-events on
```

Затем отключитесь от tmux, подключитесь снова и перезапустите Claude Code. Перезапускайте его снова каждый раз, когда подключаетесь к tmux из другого терминала. Чтобы сохранить обе опции после перезапуска сервера tmux, также [добавьте обе строки в `~/.tmux.conf`](https://code.claude.com/docs/ru/terminal-config#configure-tmux).

## Где ещё может отрисовывать мод

Все примеры отрисовываются на панели. Мод также может отрисовывать в других местах и вызывать Claude Code, чтобы тот что-то показал за него:

* **Панель и полоса**: [Выбор места для отрисовки](https://code.claude.com/docs/ru/plugins/mods/interface.md#pick-where-to-draw)
* **Собственные строки Claude Code, например индикатор загрузки**: [Изменение того, что уже отрисовывает Claude Code](https://code.claude.com/docs/ru/plugins/mods/interface.md#change-what-claude-code-already-draws)
* **Всплывающее уведомление, строка состояния и строка лога**: [Показать что-то, не начиная ход](https://code.claude.com/docs/ru/plugins/mods/api.md#show-something-without-starting-a-turn)
* **Диалог с вопросом**: [Удержание вызова инструмента до решения пользователя](https://code.claude.com/docs/ru/plugins/mods/events.md#hold-a-tool-call-until-the-user-decides)

## Дальнейшие шаги

* [Отрисовка в интерфейсе](https://code.claude.com/docs/ru/plugins/mods/interface.md): пошаговое создание панели с вкладками
* [Тестирование отрисовки](https://code.claude.com/docs/ru/plugins/mods/test.md#test-a-drawing): нажатие ваших кнопок из теста
* [Справочник по элементам](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements): основные свойства каждого элемента и приложения, которые его отрисовывают
