> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Рекомендуйте ваш plugin из вашего CLI

> Предложите пользователям Claude Code установить ваш plugin из официального marketplace, отправив тег claude-code-hint из вашего CLI или SDK.

Если вы поддерживаете CLI или SDK, ваш инструмент может предложить пользователям Claude Code установить ваш plugin. Когда ваш CLI обнаружит, что он работает внутри Claude Code, он должен записать однострочный тег `<claude-code-hint />` в stderr. Claude Code удаляет строку из вывода инструментов Bash и PowerShell перед тем, как модель увидит вывод, а затем показывает пользователю одноразовое предложение об установке.

Эта страница применяется только если ваш plugin указан в `claude-plugins-official` или другом marketplace с одним из [официальных названий marketplace Anthropic](https://code.claude.com/docs/ru/plugins/security.md#official-marketplace-names). Сообщество marketplace, `claude-community`, не входит в их число.

> [!NOTE]
>
> Чтобы опубликовать plugin, см. [Опубликуйте и распространяйте plugin](https://code.claude.com/docs/ru/plugins/publish.md).

## Отправьте подсказку

Отправляйте тег только когда установлены `CLAUDECODE` или `CLAUDE_CODE_CHILD_SESSION`, чтобы он не появлялся, когда человек запускает ваш CLI напрямую.

Claude Code устанавливает `CLAUDECODE=1` в командах, которые он запускает через инструменты Bash и PowerShell, и в командах hook. На v2.1.172 и более поздних версиях он также устанавливает `CLAUDE_CODE_CHILD_SESSION=1` там. Переменные отличаются тем, какие процессы их переносят:

* **`CLAUDECODE`**: устанавливается каждой версией Claude Code. IDE расширения также устанавливают его в своих интегрированных терминалах, поэтому проверка только `CLAUDECODE` также отправляет тег, когда человек запускает ваш CLI самостоятельно в одном из этих терминалов
* **`CLAUDE_CODE_CHILD_SESSION`**: устанавливается только в подпроцессах, которые сам запускает Claude Code. Используйте его, когда вы можете требовать v2.1.172 или более позднюю версию

[Справочник переменных окружения](https://code.claude.com/docs/ru/env-vars.md) содержит подробности.

Следующие примеры проверяют `CLAUDECODE` для наибольшего охвата и отправляют подсказку для plugin с именем `example-cli` в официальном marketplace:

```javascript Node.js theme={null}
if (process.env.CLAUDECODE) {
  process.stderr.write(
    '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />\n',
  )
}
```

```python Python theme={null}
import os, sys

if os.environ.get("CLAUDECODE"):
    print(
        '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />',
        file=sys.stderr,
    )
```

```go Go theme={null}
if os.Getenv("CLAUDECODE") != "" {
    fmt.Fprintln(os.Stderr,
        `<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />`)
}
```

```shell Shell theme={null}
if [ -n "$CLAUDECODE" ]; then
  printf '%s\n' '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />' >&2
fi
```

Замените `example-cli` на имя вашего plugin в официальном marketplace.

Вы можете отправлять подсказку при каждом вызове, потому что Claude Code предлагает для каждого plugin один раз.

Чтобы проверить отправителя, запустите `CLAUDECODE=1 example-cli` в терминале и подтвердите, что строка тега появляется на stderr, затем запустите `example-cli` без переменной и подтвердите, что ничего лишнего не печатается.

## Формат подсказки

Тег должен занимать свою собственную строку; Claude Code игнорирует тег, встроенный в середину строки.

Тег принимает три атрибута, все обязательны:

| Атрибут | Описание |
| :- | :- |
| `v` | Версия протокола. `1` — единственное поддерживаемое значение |
| `type` | Вид подсказки. `plugin` — единственное поддерживаемое значение |
| `value` | Идентификатор plugin в форме `name@marketplace` |

Значения могут быть заключены в двойные кавычки или без кавычек; значение без кавычек не может содержать пробелы.

Claude Code удаляет строку из вывода даже когда `v` или `type` не распознаны.

## Проверьте, когда появляется подсказка

Подсказка появляется только в интерактивных сеансах терминала. В запусках `claude -p`, в запусках подагента и в выводе команд hook тег удаляется и подсказка не показывается. Все эти проверки также должны пройти:

* **Официальный и устанавливаемый**: `value` называет plugin, который Claude Code находит в своей локальной копии официального marketplace, который еще не установлен, и который не блокирует никакая политика
* **Аналитика включена**: сеанс, где аналитика Claude Code отключена, никогда не предлагает, например, с установленными `DISABLE_TELEMETRY`, `DO_NOT_TRACK` или `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, или на поставщике третьей стороны, таком как Amazon Bedrock, где применяется [автоматический отказ от телеметрии](https://code.claude.com/docs/ru/data-usage.md#default-behaviors-by-api-provider)
* **Ограничения частоты**: одна подсказка за сеанс, одна подсказка когда-либо за plugin независимо от ответа пользователя, и ни одна после того, как на этой машине было предложено 100 plugin
* **Не отключено**: пользователь не выбрал **Нет, и больше не показывать подсказки об установке plugin**
* **Локальный, посещаемый сеанс**: рабочее пространство сеанса является локальным, а не в облаке или на удаленной машине, и сеанс не работает без присмотра. Например, сеанс, запущенный с `--cloud`, один, обслуживающий Remote Control, или товарищ по команде агентов никогда не предлагает

## Предпросмотр того, что видит пользователь

Когда проверки в [Проверьте, когда появляется подсказка](#check-when-the-prompt-appears) пройдены, Claude Code показывает диалог **Рекомендация plugin** следующим образом:

```text theme={null}
─────────────────────────────────────────────────────────────
  Рекомендация plugin

    Команда example-cli предлагает установить plugin.

    Plugin: example-cli
    Marketplace: claude-plugins-official
    Описание: Официальная интеграция для развертываний example-cli

    Вы хотите установить его?
    ❯ 1. Да, установить
      2. Нет
      3. Нет, и больше не показывать подсказки об установке plugin

─────────────────────────────────────────────────────────────
```

Диалог называет первое слово команды shell, которую запустил Claude, поэтому пользователи могут заметить несоответствие. Каждый ответ имеет один эффект:

* **Да, установить**: устанавливает plugin в [область пользователя](https://code.claude.com/docs/ru/plugins/install.md)
* **Нет, и больше не показывать подсказки об установке plugin**: отключает будущие подсказки для этого пользователя
* **Нет ответа в течение 30 секунд**: считается как **Нет**

## Следующие шаги

* [Опубликовать и распространить плагин](https://code.claude.com/docs/ru/plugins/publish.md): маршруты для распространения плагина, включая официальный marketplace, который требует подсказка
* [Справочник команд плагина](https://code.claude.com/docs/ru/plugins/cli-reference.md#plugin-install): команда оболочки, которая устанавливает тот же плагин вне сеанса
