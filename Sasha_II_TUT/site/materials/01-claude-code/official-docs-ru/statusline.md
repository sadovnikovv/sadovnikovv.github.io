> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка строки состояния

> Настройте пользовательскую строку состояния для мониторинга использования контекстного окна, затрат и статуса git в Claude Code

Строка состояния — это настраиваемая панель в нижней части Claude Code, которая запускает любой скрипт оболочки, который вы настроите. Она получает данные сеанса в формате JSON через stdin и отображает всё, что выводит ваш скрипт, предоставляя вам постоянный, видимый с первого взгляда обзор использования контекста, затрат, статуса git или чего-либо ещё, что вы хотите отслеживать.

Строки состояния полезны, когда вы:

* Хотите отслеживать использование контекстного окна во время работы
* Нужно отслеживать затраты сеанса
* Работаете в нескольких сеансах и нужно их различать
* Хотите, чтобы ветка git и статус всегда были видны

Строка состояния отображается в собственной строке над встроенными значками нижнего колонтитула и не заменяет их. С настроенной пользовательской строкой состояния Claude Code перестаёт показывать некоторые подсказки нижнего колонтитула, например `? for shortcuts` и подсказку `hold space to speak` [голосовой диктовки](https://code.claude.com/docs/ru/voice-dictation.md). Чтобы добавить интерактивные значки ссылок в нижний колонтитул, когда в диалоге появляется ID, без написания скрипта, вместо этого настройте [`footerLinksRegexes`](https://code.claude.com/docs/ru/settings-reference#footerlinksregexes).

Вот пример [многострочной строки состояния](#display-multiple-lines), которая отображает информацию git в первой строке и цветовую полосу контекста во второй.

![Многострочная строка состояния, показывающая имя модели, каталог, ветку git в первой строке и полосу прогресса использования контекста с затратами и продолжительностью во второй строке](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-multiline.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=a9d0a2fe8e446d80b1abc46da3f93270)

На этой странице описано [настройка базовой строки состояния](#set-up-a-status-line), объясняется [как данные передаются](#how-status-lines-work) из Claude Code в ваш скрипт, перечисляются [все поля, которые вы можете отображать](#available-data), и предоставляются [готовые примеры](#examples) для распространённых паттернов, таких как статус git, отслеживание затрат и полосы прогресса.

## Настройка строки состояния

Используйте [команду `/statusline`](#use-the-%2Fstatusline-command) для автоматического создания скрипта Claude Code, или [вручную создайте скрипт](#manually-configure-a-status-line) и добавьте его в ваши настройки.

### Использование команды /statusline

Команда `/statusline` принимает инструкции на естественном языке, описывающие то, что вы хотите отображать. Claude Code генерирует файл скрипта в `~/.claude/` и автоматически обновляет ваши настройки:

```text theme={null}
/statusline show model name and context percentage with a progress bar
```

Одобрите запросы на редактирование файла, если Claude Code попросит разрешение во время настройки.

### Ручная настройка строки состояния

Добавьте поле `statusLine` в ваши пользовательские настройки (`~/.claude/settings.json`, где `~` — это ваш домашний каталог) или [настройки проекта](https://code.claude.com/docs/ru/settings.md#where-settings-live). Установите `type` на `"command"` и укажите `command` на путь скрипта или встроенную команду оболочки. Для полного пошагового руководства по созданию скрипта см. [Построение строки состояния пошагово](#build-a-status-line-step-by-step).

```json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

Поле `command` запускается в оболочке, поэтому вы также можете использовать встроенные команды вместо файла скрипта. Этот пример использует `jq` для разбора входных данных JSON и отображения имени модели и процента контекста:

```json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

Необязательное поле `padding` добавляет дополнительное горизонтальное расстояние (в символах) к содержимому строки состояния. По умолчанию `0`. Это заполнение добавляется к встроенному расстоянию интерфейса, поэтому оно управляет относительным отступом, а не абсолютным расстоянием от края терминала.

Необязательное поле `refreshInterval` повторно запускает вашу команду каждые N секунд в дополнение к [обновлениям, управляемым событиями](#how-status-lines-work). Минимум — `1`. Установите это, когда ваша строка состояния отображает данные на основе времени, такие как часы, или когда фоновые подагенты изменяют состояние git, пока основной сеанс неактивен. Оставьте это не установленным, чтобы запускать только при событиях.

Необязательное поле `hideVimModeIndicator` подавляет встроенный текст `-- INSERT --` под приглашением. Установите это на `true`, когда ваш скрипт отображает [`vim.mode`](#available-data) самостоятельно, чтобы режим не отображался дважды.

### Отключение строки состояния

Запустите `/statusline` и попросите её удалить или очистить вашу строку состояния (например, `/statusline delete`, `/statusline clear`, `/statusline remove it`). Вы также можете вручную удалить поле `statusLine` из вашего settings.json.

## Построение строки состояния пошагово

Это пошаговое руководство показывает, что `/statusline` настраивает для вас путём ручного создания строки состояния, которая отображает текущую модель, рабочий каталог и процент использования контекстного окна.

> [!NOTE]
>
> Запуск [`/statusline`](#use-the-%2Fstatusline-command) с описанием того, что вы хотите, настраивает всё это автоматически.

Эти примеры используют скрипты Bash, которые работают на macOS и Linux. На Windows см. [Конфигурация Windows](#windows-configuration) для примеров PowerShell и Git Bash.

![Строка состояния, показывающая имя модели, каталог и процент контекста](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-quickstart.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=88a7eab9c1038dd098ee8e284d96b7e6)

**1. Создайте скрипт, который читает JSON и выводит результат**

Claude Code отправляет данные JSON в ваш скрипт через stdin. Этот скрипт использует [`jq`](https://jqlang.org/), парсер JSON командной строки, который вам может потребоваться установить, для извлечения имени модели, каталога и процента контекста, а затем выводит отформатированную строку.

Сохраните это в `~/.claude/statusline.sh` (где `~` — это ваш домашний каталог, например `/Users/username` на macOS или `/home/username` на Linux):

```bash theme={null}
#!/bin/bash
# Read JSON data that Claude Code sends to stdin
input=$(cat)

# Extract fields using jq
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
# The "// 0" provides a fallback if the field is null
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Output the status line - ${DIR##*/} extracts just the folder name
echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
```

**2. Сделайте его исполняемым**

Отметьте скрипт как исполняемый, чтобы ваша оболочка могла его запустить:

```bash theme={null}
chmod +x ~/.claude/statusline.sh
```

**3. Добавьте в настройки**

Скажите Claude Code запустить ваш скрипт как строку состояния. Добавьте эту конфигурацию в `~/.claude/settings.json`, которая устанавливает `type` на `"command"` (означает «запустить эту команду оболочки») и указывает `command` на ваш скрипт:

```json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

Ваша строка состояния появляется в нижней части интерфейса. Claude Code автоматически перезагружает настройки и запускает ваш скрипт сразу же после сохранения файла.

## Как работают строки состояния

Claude Code запускает ваш скрипт с [данными сессии JSON](#available-data) на stdin и отображает всё, что скрипт выводит в stdout.

> [!NOTE]
>
> Строка состояния работает локально и не потребляет токены API. Она временно скрывается во время определённых взаимодействий с пользовательским интерфейсом, включая меню справки и запросы разрешений.

### Когда обновляется строка состояния

Ваш скрипт запускается один раз при запуске сессии, включая случаи, когда вы возобновляете её. После этого он запускается снова, когда:

* Поступает новое сообщение ассистента
* Завершается `/compact`
* Изменяется режим разрешений
* Переключается режим Vim
* Вы изменяете `command` в настройках `statusLine`
* Истекает таймер [`refreshInterval`](#manually-configure-a-status-line), если вы его установили
* Окно [ограничения частоты запросов](#rate-limit-usage) в данных, которые последними получил ваш скрипт, достигает времени `resets_at`
* Тёплый [кэш промптов](#prompt-cache-fields) в данных, которые последними получил ваш скрипт, достигает времени `expires_at`

Claude Code дебаунсит обновления на 300 мс, поэтому быстрые изменения объединяются вместе и ваш скрипт запускается один раз после того, как изменения прекратятся. Изменение самой `command` пропускает дебаунс: Claude Code запускает новую команду сразу же. Если новое обновление срабатывает, пока ваш скрипт всё ещё работает, Claude Code отменяет выполняющийся скрипт. Если вы отредактируете свой скрипт, изменения появятся в следующий раз, когда триггер обновления его повторно запустит.

Триггеры, управляемые событиями, могут затихнуть, когда основная сессия неактивна, например, пока координатор ждёт фоновых субагентов. Чтобы сегменты на основе времени или из внешних источников оставались актуальными во время периодов неактивности, установите [`refreshInterval`](#manually-configure-a-status-line), чтобы также повторно запускать команду по фиксированному таймеру.

### Что может выводить ваш скрипт

Ваш скрипт может выводить не только одну строку простого текста:

* **Несколько строк**: каждый оператор `echo` или `print` отображается как отдельная строка. См. [пример многострочности](#display-multiple-lines).
* **Цвета**: используйте [коды экранирования ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors), такие как `\033[32m` для зелёного (терминал должен их поддерживать). См. [пример статуса git](#git-status-with-colors).
* **Ссылки**: используйте [последовательности экранирования OSC 8](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC) для создания кликабельного текста (Cmd+клик на macOS, Ctrl+клик на Windows/Linux). Требуется терминал, поддерживающий гиперссылки, такой как iTerm2, Kitty или WezTerm. См. [пример кликабельных ссылок](#clickable-links).

### Размер вывода в соответствии с терминалом

Claude Code захватывает вывод вашего скрипта вместо прямого подключения к терминалу, поэтому `tput cols` и определение ширины на уровне языка не могут прочитать размер терминала изнутри скрипта. Вместо этого читайте переменные окружения `COLUMNS` и `LINES`. Claude Code устанавливает эти значения в соответствии с текущими размерами терминала перед запуском вашего скрипта.

## Доступные данные

Claude Code отправляет следующие поля JSON в ваш скрипт через stdin:

| Поле | Описание |
| - | - |
| `model.id`, `model.display_name` | Текущий идентификатор модели и отображаемое имя |
| `cwd`, `workspace.current_dir` | Текущий рабочий каталог. Оба поля содержат одно и то же значение; `workspace.current_dir` предпочтительнее для согласованности с `workspace.project_dir`. |
| `workspace.project_dir` | Каталог, в котором был запущен Claude Code, который может отличаться от `cwd`, если рабочий каталог изменяется во время сеанса |
| `workspace.added_dirs` | Дополнительные каталоги, добавленные через `/add-dir` или `--add-dir`. Пустой массив, если ничего не было добавлено |
| `workspace.git_worktree` | Имя Git worktree, когда текущий каталог находится внутри связанного worktree, созданного с помощью `git worktree add`. Отсутствует в основном рабочем дереве. Заполняется для любого git worktree, в отличие от `worktree.*`, который присутствует только во время сеанса в [worktree сеансе](https://code.claude.com/docs/ru/worktrees.md) |
| `workspace.repo.host`, `workspace.repo.owner`, `workspace.repo.name` | Идентификация репозитория, проанализированная из удалённого хранилища `origin`, например `"github.com"`, `"anthropics"`, `"claude-code"`. Отсутствует вне git репозитория или когда удалённое хранилище `origin` не настроено. Для проекта gitlab.com, вложенного в подгруппы, `owner` — это полный путь пространства имён с косыми чертами, например `"group/subgroup"`. До версии 2.1.260 `workspace.repo` отсутствовал для этих проектов |
| `cost.total_cost_usd` | Предполагаемая стоимость сессии в USD, вычисляется на клиенте по цене списка, если не действует таблица [`modelPricing`](https://code.claude.com/docs/ru/settings-reference#modelpricing). Может отличаться от вашего фактического счёта. Сбрасывается на \$0 при запуске новой сессии с помощью `/clear` |
| `cost.total_duration_ms` | Общее реальное время, в течение которого сеанс работал, в миллисекундах. Накапливается при возобновлении и не включает время, когда сеанс не работает |
| `cost.total_api_duration_ms` | Общее время, потраченное на ожидание ответов API в миллисекундах |
| `cost.total_lines_added`, `cost.total_lines_removed` | Строки кода, которые были изменены |
| `context_window.total_input_tokens`, `context_window.total_output_tokens` | Количество токенов, находящихся в контекстном окне, из последнего ответа API. Входные данные включают чтение и запись кэша |
| `context_window.context_window_size` | Максимальный размер контекстного окна в токенах |
| `context_window.used_percentage` | Предварительно рассчитанный процент использованного контекстного окна |
| `context_window.remaining_percentage` | Предварительно рассчитанный процент оставшегося контекстного окна |
| `context_window.current_usage` | Подсчёты токенов из последнего вызова API, описанные в [полях контекстного окна](#context-window-fields) |
| `exceeds_200k_tokens` | Превышает ли общее количество токенов (входные, кэшированные и выходные токены в сумме) из последнего ответа API 200k. Это фиксированный порог независимо от фактического размера контекстного окна. |
| `fast_mode` | Включен ли [быстрый режим](https://code.claude.com/docs/ru/fast-mode.md) для сеанса |
| `effort.level` | Уровень effort рассуждений, установленный для сессии (`low`, `medium`, `high`, `xhigh` или `max`), а не уровень, установленный скиллом, субагентом или `ultrathink`. Если вы установите уровень, который модель не поддерживает, здесь отображается уровень, с которым Claude Code фактически работал. Изменённый вами уровень отображается здесь ещё до того, как он [вступит в силу](https://code.claude.com/docs/ru/model-config.md#when-a-new-effort-level-starts). Если уровень задан в `CLAUDE_CODE_EFFORT_LEVEL`, здесь отображается этот уровень. Отсутствует, когда текущая модель не поддерживает параметр effort |
| `thinking.enabled` | Включено ли расширенное мышление для сеанса |
| `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` | Процент лимита скорости за 5 часов или 7 дней, потреблённый от 0 до 100 |
| `rate_limits.five_hour.resets_at`, `rate_limits.seven_day.resets_at` | Секунды эпохи Unix, когда окно лимита скорости за 5 часов или 7 дней сбрасывается |
| `rate_limits.spend_limit.used_percentage`, `rate_limits.spend_limit.resets_at` | За шлюзом Claude apps — какую часть лимита расходов вы использовали и когда сбрасывается его период. См. [поля лимита расходов](#spend-limit-fields). Требуется Claude Code v2.1.251 или позже |
| `rate_limits.spend_limit.used_usd`, `rate_limits.spend_limit.limit_usd`, `rate_limits.spend_limit.period` | Ваши предполагаемые расходы и ваш лимит в долларах США, а также период лимита. Эти поля могут отсутствовать. См. [поля лимита расходов](#spend-limit-fields). Требуется v2.1.284 или позже как для Claude Code, так и для шлюза |
| `prompt_cache` | Статистика [prompt cache](https://code.claude.com/docs/ru/prompt-caching.md) сеанса для основного разговора: коэффициент попаданий, промахи и является ли кэш тёплым. Смотрите [поля prompt cache](#prompt-cache-fields) для каждого поля. Отсутствует до первого ответа API основного разговора. Требуется Claude Code v2.1.251 или позже |
| `session_id` | Уникальный идентификатор сеанса |
| `session_name` | Имя сеанса. Использует пользовательское имя, установленное с флагом `--name` или `/rename`, когда оно существует, в противном случае — автоматически сгенерированный заголовок сеанса. [Имя отображения по умолчанию](https://code.claude.com/docs/ru/sessions.md#name-your-sessions), например `my-app-3f`, не заполняет это поле. Отсутствует, когда сеанс не имеет ни пользовательского имени, ни автоматически сгенерированного заголовка |
| `prompt_id` | UUID, идентифицирующий промпт пользователя, который в настоящее время обрабатывается. Совпадает с атрибутом [`prompt.id` на событиях OpenTelemetry](https://code.claude.com/docs/ru/monitoring-usage#event-correlation-attributes). Отсутствует до первого ввода пользователя |
| `transcript_path` | Путь к файлу стенограммы разговора |
| `version` | Версия Claude Code |
| `output_style.name` | Имя текущего стиля вывода |
| `vim.mode` | Текущий режим vim (`NORMAL`, `INSERT`, `VISUAL` или `VISUAL LINE`), когда [режим vim](https://code.claude.com/docs/ru/interactive-mode.md#vim-editor-mode) включен |
| `agent.name` | Имя агента при запуске с флагом `--agent` или настроенными параметрами агента |
| `pr.number`, `pr.url` | Открытый pull request для текущей ветки. Отражает значок PR в нижней строке состояния. В репозитории с удалённым хранилищем GitLab Claude Code заполняет эти поля из открытого [merge request](https://code.claude.com/docs/ru/interactive-mode.md#gitlab-merge-requests) ветки, поэтому `pr.number` — это номер merge request. Данные merge request требуют Claude Code v2.1.234 или позже. Отсутствует, когда не в git репозитории, до тех пор пока не будет найден pull request или merge request, или после того как он будет объединён или закрыт |
| `pr.review_state` | Статус проверки открытого PR: `approved`, `pending`, `changes_requested` или `draft`. Может быть независимо отсутствующим даже когда `pr` присутствует |
| `pr.kind` | `mr`, когда `pr` описывает [GitLab merge request](https://code.claude.com/docs/ru/interactive-mode.md#gitlab-merge-requests). Отсутствует для GitHub pull requests, поэтому скрипты, написанные до этого поля, продолжают работать. Для merge request Claude Code устанавливает `review_state` на `approved`, когда GitLab сообщает, что он готов к объединению, `pending` для любого другого открытого состояния и `draft` для черновика. Требуется Claude Code v2.1.234 или позже |
| `worktree.name` | Имя активного worktree. Присутствует только во время сеанса в [worktree сеансе](https://code.claude.com/docs/ru/worktrees.md) |
| `worktree.path` | Абсолютный путь к каталогу worktree |
| `worktree.branch` | Имя ветки Git для worktree (например, `"worktree-my-feature"`). Отсутствует для worktrees на основе hooks |
| `worktree.original_cwd` | Каталог, в котором находился Claude перед входом в worktree |
| `worktree.original_branch` | Ветка Git, проверенная перед входом в worktree. Отсутствует для worktrees на основе hooks |

> [accordion] Полная схема JSON
>
> Ваша команда строки состояния получает эту структуру JSON через stdin:
>
> ```json theme={null}
> {
>   "cwd": "/current/working/directory",
>   "session_id": "abc123...",
>   "session_name": "my-session",
>   "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
>   "transcript_path": "/path/to/transcript.jsonl",
>   "model": {
>     "id": "claude-opus-5-5",
>     "display_name": "Opus"
>   },
>   "workspace": {
>     "current_dir": "/current/working/directory",
>     "project_dir": "/original/project/directory",
>     "added_dirs": [],
>     "git_worktree": "feature-xyz",
>     "repo": {
>       "host": "github.com",
>       "owner": "anthropics",
>       "name": "claude-code"
>     }
>   },
>   "version": "2.1.90",
>   "output_style": {
>     "name": "default"
>   },
>   "cost": {
>     "total_cost_usd": 0.01234,
>     "total_duration_ms": 45000,
>     "total_api_duration_ms": 2300,
>     "total_lines_added": 156,
>     "total_lines_removed": 23
>   },
>   "context_window": {
>     "total_input_tokens": 15500,
>     "total_output_tokens": 1200,
>     "context_window_size": 200000,
>     "used_percentage": 8,
>     "remaining_percentage": 92,
>     "current_usage": {
>       "input_tokens": 8500,
>       "output_tokens": 1200,
>       "cache_creation_input_tokens": 5000,
>       "cache_read_input_tokens": 2000
>     }
>   },
>   "exceeds_200k_tokens": false,
>   "prompt_cache": {
>     "warm": true,
>     "caching_observed": true,
>     "ttl": "1h",
>     "expires_at": 1738429200,
>     "requests": 14,
>     "misses": 2,
>     "expected_rebuilds": 1,
>     "hit_ratio": 0.91,
>     "cache_write_tokens": 352000,
>     "miss_recache_tokens": 310200,
>     "last_miss_at": 1738425230,
>     "last_miss_cause": {
>       "causes": ["tools_changed"],
>       "tools_added": 2,
>       "tools_removed": 0
>     },
>     "miss_causes": {
>       "tools_changed": 2
>     },
>     "recache_tokens_if_cold": 45000
>   },
>   "fast_mode": false,
>   "effort": {
>     "level": "high"
>   },
>   "thinking": {
>     "enabled": true
>   },
>   "rate_limits": {
>     "five_hour": {
>       "used_percentage": 23.5,
>       "resets_at": 1738425600
>     },
>     "seven_day": {
>       "used_percentage": 41.2,
>       "resets_at": 1738857600
>     },
>     "spend_limit": {
>       "used_percentage": 62.8,
>       "resets_at": 1740787200,
>       "used_usd": 314.12,
>       "limit_usd": 500,
>       "period": "monthly"
>     }
>   },
>   "vim": {
>     "mode": "NORMAL"
>   },
>   "agent": {
>     "name": "security-reviewer"
>   },
>   "pr": {
>     "number": 1234,
>     "url": "https://github.com/anthropics/claude-code/pull/1234",
>     "review_state": "pending"
>   },
>   "worktree": {
>     "name": "my-feature",
>     "path": "/path/to/.claude/worktrees/my-feature",
>     "branch": "worktree-my-feature",
>     "original_cwd": "/path/to/project",
>     "original_branch": "main"
>   }
> }
> ```
>
> **Поля, которые могут отсутствовать** (не присутствуют в JSON):
>
> * `session_name`: появляется, когда пользовательское имя было установлено с `--name` или `/rename`, или после того как существует автоматически сгенерированный заголовок сеанса. Имя отображения по умолчанию, например `my-app-3f`, не заполняет это поле
> * `prompt_id`: появляется только после первого ввода пользователя
> * `workspace.git_worktree`: появляется только когда текущий каталог находится внутри связанного git worktree
> * `workspace.repo`: появляется только внутри git репозитория с настроенным удалённым хранилищем `origin`
> * `effort`: появляется только когда текущая модель поддерживает параметр reasoning effort
> * `vim`: появляется только когда режим vim включен
> * `agent`: появляется только при запуске с флагом `--agent` или настроенными параметрами агента
> * `pr`: появляется только пока открытый PR или GitLab merge request найден для текущей ветки, и удаляется после того как он будет объединён или закрыт. `pr.review_state` и `pr.kind` могут быть независимо отсутствующими
> * `worktree`: появляется только во время сеанса в [worktree сеансе](https://code.claude.com/docs/ru/worktrees.md). Когда присутствует, `branch` и `original_branch` также могут отсутствовать для worktrees на основе hooks
> * `rate_limits`: появляется только для подписчиков claude.ai Pro, Max и Ultra или за шлюзом Claude apps, который устанавливает лимит расходов для вас. Даже в этом случае поле появляется только после первого ответа API в сессии. Каждое окно (`five_hour`, `seven_day`, `spend_limit`) может быть независимо отсутствующим, и Claude Code удаляет окно после того как его время `resets_at` пройдёт. Используйте `jq -r '.rate_limits.five_hour.used_percentage // empty'` для корректной обработки отсутствия.
> * `prompt_cache`: появляется после первого ответа API основного разговора. Смотрите [поля prompt cache](#prompt-cache-fields)
>
> **Поля, которые могут быть `null`**:
>
> * `context_window.current_usage`: `null` перед первым вызовом API в сеансе и снова после `/compact` до следующего вызова API, который его переполнит
> * `context_window.used_percentage`, `context_window.remaining_percentage`: могут быть `null` в начале сеанса
>
> Обрабатывайте отсутствующие поля с условным доступом и нулевые значения с резервными значениями по умолчанию в ваших скриптах.

### Поля контекстного окна

Объект `context_window` описывает живое контекстное окно из последнего ответа API.

* **Совокупные итоги** (`total_input_tokens`, `total_output_tokens`): токены, находящиеся в контекстном окне. `total_input_tokens` — это сумма `input_tokens`, `cache_creation_input_tokens` и `cache_read_input_tokens`; `total_output_tokens` — это выходные токены из последнего ответа. Оба равны `0` перед первым ответом API.
* **Использование по компонентам** (`current_usage`): те же подсчёты токенов, разбитые по категориям. Используйте это, когда вам нужны попадания в кэш отдельно от свежего входа.

Объект `current_usage` содержит:

* `input_tokens`: входные токены в текущем контексте
* `output_tokens`: выходные токены, которые были сгенерированы
* `cache_creation_input_tokens`: токены, записанные в кэш
* `cache_read_input_tokens`: токены, прочитанные из кэша

Для получения информации о том, что означают поля кэша и как они выставляются счётом, см. [проверка производительности кэша](https://code.claude.com/docs/ru/prompt-caching.md#check-cache-performance).

Поле `used_percentage` рассчитывается только из входных токенов: `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. Оно не включает `output_tokens`.

Если вы рассчитываете процент контекста вручную из `current_usage`, используйте ту же формулу только для входных данных, чтобы соответствовать `used_percentage`.

Объект `current_usage` равен `null` перед первым вызовом API в сеансе и снова сразу после `/compact` до следующего вызова API, который его переполнит.

### Поля лимита расходов

За [шлюзом Claude apps с лимитами расходов](https://code.claude.com/docs/ru/claude-apps-gateway-spend-limits.md#usage-warnings-in-claude-code) объект `rate_limits.spend_limit` описывает лимит расходов, который применяется к вам. Он появляется после первого ответа API в сессии и требует Claude Code v2.1.251 или позже. Ваш скрипт получает его поля по разным графикам:

* `used_percentage` и `resets_at`: приходят с каждым ответом, поэтому присутствуют всегда, когда присутствует `spend_limit`. `used_percentage` варьируется от 0 до 100 или выше 100, когда вы превышаете лимит, а `resets_at` — это секунды эпохи Unix, когда сбрасывается период лимита.
* `used_usd`, `limit_usd` и `period`: ваши предполагаемые расходы на данный момент и ваш лимит в долларах США, а также период, на который распространяется лимит: `daily`, `weekly` или `monthly`. Шлюз [вычисляет `used_usd` на основе подсчётов токенов](https://code.claude.com/docs/ru/claude-apps-gateway-spend-limits#how-requests-are-priced), поэтому это оценка, а не выставленная к оплате сумма. Claude Code получает их от шлюза отдельным запросом примерно каждые пять минут, пока вы отправляете запросы. Суммы в долларах могут быть примерно на пять минут старше, чем `used_percentage`, поэтому эти значения могут ненадолго расходиться. Требуется v2.1.284 или позже как для Claude Code, так и для шлюза.

Считайте `used_usd`, `limit_usd` и `period` необязательными, даже когда `spend_limit` присутствует, потому что ваш скрипт получает процент раньше них. Считывайте каждое из них с резервным вариантом в скрипте, например `jq -r '.rate_limits.spend_limit.used_usd // empty'`. До Claude Code v2.1.295 они оставались отсутствующими, если вы установили `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, что отключало этот запрос.

### Поля prompt cache

Объект `prompt_cache` суммирует, как основной разговор сеанса использует [prompt cache](https://code.claude.com/docs/ru/prompt-caching.md). Claude Code вычисляет его из подсчётов токенов кэша в ответах API, поэтому он работает на каждом поставщике.

Объект появляется после первого ответа API основного разговора. Claude Code не учитывает запросы подагентов в этой статистике. Требуется Claude Code v2.1.251 или позже.

Таблица перечисляет каждое поле с его значением. Временные метки — это секунды эпохи Unix, то же самое, что и `rate_limits.*.resets_at`. Строка состояния обычно показывает одно или два из них; `warm` и `hit_ratio` наиболее прямо суммируют состояние кэша.

| Поле | Описание |
| - | - |
| `warm` | Находится ли кэшированный префикс всё ещё в пределах своего TTL. `false`, когда последний ответ не сообщил о токенах кэша, даже если `caching_observed` равен `true` |
| `caching_observed` | Сообщил ли какой-либо ответ в этом сеансе о токенах кэша. `false` означает, что prompt caching отключен, или ваш поставщик или шлюз его не сообщает |
| `ttl` | [Время жизни кэша](https://code.claude.com/docs/ru/prompt-caching.md#cache-lifetime) текущего кэшированного префикса: `"5m"` или `"1h"` |
| `expires_at` | Когда кэшированный префикс выходит из своего TTL и становится холодным, в секундах эпохи. `null`, когда последний ответ не сообщил о токенах кэша |
| `requests` | Запросы API, записанные для основного разговора в этом сеансе |
| `misses` | Запросы, которые переобработали содержимое, которое кэш уже содержал: более 5% и по крайней мере 2000 токенов того, что запрос мог бы прочитать из кэша, без компактирования или очистки результатов инструментов, чтобы объяснить недостаток чтений из кэша |
| `expected_rebuilds` | Перестройки кэша, которые последовали за компактированием или очисткой старых результатов инструментов |
| `hit_ratio` | Токены чтения кэша как доля всех входных токенов в этом сеансе, от 0 до 1. Знаменатель учитывает чтения кэша, записи кэша и некэшированный вход. `null`, пока все эти подсчёты равны нулю |
| `cache_write_tokens` | Все токены, записанные в кэш в этом сеансе, включая начальную запись первого запроса |
| `miss_recache_tokens` | Токены, записанные в кэш запросами, которые учитываются как промахи |
| `last_miss_at` | Когда произошёл последний промах, в секундах эпохи. `null`, пока в сеансе нет промахов |
| `last_miss_cause` | Что Claude Code определил как вероятную причину последнего промаха, описанную в разделе [Причина последнего промаха](#last-miss-cause). Требуется Claude Code v2.1.260 или позже |
| `miss_causes` | Сколько диагностированных промахов этого сеанса имели каждую причину, ключ по тем же названиям причин, что и `last_miss_cause`. Требуется Claude Code v2.1.260 или позже |
| `recache_tokens_if_cold` | Токены, которые следующий запрос переполнит в кэш, если кэш к тому времени стал холодным. `null` сразу после компактирования или очистки старых результатов инструментов, до следующего запроса, который записывает размер переписанного разговора |

Claude Code показывает ту же статистику в терминале на строке [`/usage` команды `Prompt cache (main)`](https://code.claude.com/docs/ru/costs#prompt-cache-statistics).

#### Причина последнего промаха

Объект `last_miss_cause` сообщает, что Claude Code определил как вероятную причину самого последнего промаха. Его массив `causes` содержит одно или несколько названий причин, таких как `tools_changed`, `system_prompt_changed`, `ttl_expired_5m` или `likely_server_side`. Объект равен `null` до первого промаха сеанса и снова всякий раз, когда Claude Code не может определить причину самого последнего промаха. Требуется Claude Code v2.1.260 или позже.

Две причины добавляют подсчёты к объекту:

* `tools_added` и `tools_removed`: с `tools_changed`, сколько инструментов было добавлено в запрос или удалено из него
* `system_char_delta`: с `system_prompt_changed`, изменение длины системного приглашения в символах

## Примеры

Эти примеры показывают распространённые паттерны строк состояния. Чтобы использовать любой пример:

1. Сохраните скрипт в файл, например `~/.claude/statusline.sh` (или `.py`/`.js`)
2. Сделайте его исполняемым: `chmod +x ~/.claude/statusline.sh`
3. Добавьте путь в ваши [настройки](#manually-configure-a-status-line)

Примеры Bash используют [`jq`](https://jqlang.org/) для разбора JSON. Python и Node.js имеют встроенный разбор JSON.

### Использование контекстного окна

Отобразите текущую модель и использование контекстного окна с визуальной полосой прогресса. Каждый скрипт читает JSON из stdin, извлекает поле `used_percentage` и строит 10-символьную полосу, где заполненные блоки (▓) представляют использование:

![Строка состояния, показывающая имя модели и полосу прогресса с процентом](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-context-window-usage.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=f3918a549912dc47e90f2b69e68bc847)

```bash Bash theme={null}
#!/bin/bash
# Read all of stdin into a variable
input=$(cat)

# Extract fields with jq, "// 0" provides fallback for null
MODEL=$(echo "$input" | jq -r '.model.display_name')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Build progress bar: printf -v creates a run of spaces, then
# ${var// /▓} replaces each space with a block character
BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
[ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

echo "[$MODEL] $BAR $PCT%"
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys

# json.load reads and parses stdin in one step
data = json.load(sys.stdin)
model = data['model']['display_name']
# "or 0" handles null values
pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)

# String multiplication builds the bar
filled = pct * 10 // 100
bar = '▓' * filled + '░' * (10 - filled)

print(f"[{model}] {bar} {pct}%")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
// Node.js reads stdin asynchronously with events
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;
    // Optional chaining (?.) safely handles null fields
    const pct = Math.floor(data.context_window?.used_percentage || 0);

    // String.repeat() builds the bar
    const filled = Math.floor(pct * 10 / 100);
    const bar = '▓'.repeat(filled) + '░'.repeat(10 - filled);

    console.log(`[${model}] ${bar} ${pct}%`);
});
```

### Статус git с цветами

Показывает ветку git с цветовыми индикаторами для подготовленных и изменённых файлов. Этот скрипт использует [коды экранирования ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) для цветов терминала: `\033[32m` — зелёный, `\033[33m` — жёлтый и `\033[0m` — сброс на значение по умолчанию.

![Строка состояния, показывающая модель, каталог, ветку git и цветные индикаторы для подготовленных и изменённых файлов](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-git-context.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=f13c190724d9ec7188c17cd2f98b7bf4)

Каждый скрипт проверяет, является ли текущий каталог репозиторием git, подсчитывает подготовленные и изменённые файлы и отображает цветные индикаторы:

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')

GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
    MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

    GIT_STATUS=""
    [ "$STAGED" -gt 0 ] && GIT_STATUS="${GREEN}+${STAGED}${RESET}"
    [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

    echo -e "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH $GIT_STATUS"
else
    echo "[$MODEL] 📁 ${DIR##*/}"
fi
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys, subprocess, os

data = json.load(sys.stdin)
model = data['model']['display_name']
directory = os.path.basename(data['workspace']['current_dir'])

GREEN, YELLOW, RESET = '\033[32m', '\033[33m', '\033[0m'

try:
    subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
    branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
    staged_output = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
    modified_output = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
    staged = len(staged_output.split('\n')) if staged_output else 0
    modified = len(modified_output.split('\n')) if modified_output else 0

    git_status = f"{GREEN}+{staged}{RESET}" if staged else ""
    git_status += f"{YELLOW}~{modified}{RESET}" if modified else ""

    print(f"[{model}] 📁 {directory} | 🌿 {branch} {git_status}")
except:
    print(f"[{model}] 📁 {directory}")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;
    const dir = path.basename(data.workspace.current_dir);

    const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RESET = '\x1b[0m';

    try {
        execSync('git rev-parse --git-dir', { stdio: 'ignore' });
        const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
        const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
        const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;

        let gitStatus = staged ? `${GREEN}+${staged}${RESET}` : '';
        gitStatus += modified ? `${YELLOW}~${modified}${RESET}` : '';

        console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} ${gitStatus}`);
    } catch {
        console.log(`[${model}] 📁 ${dir}`);
    }
});
```

### Отслеживание затрат и продолжительности

Отслеживайте затраты API вашего сеанса и прошедшее время. Поле `cost.total_cost_usd` накапливает стоимость всех вызовов API в текущем сеансе. Поле `cost.total_duration_ms` измеряет общее прошедшее время с момента начала сеанса, а `cost.total_api_duration_ms` отслеживает только время, потраченное на ожидание ответов API.

Каждый скрипт форматирует стоимость как валюту и преобразует миллисекунды в минуты и секунды:

![Строка состояния, показывающая имя модели, стоимость сеанса и продолжительность](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-cost-tracking.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=925f7024c3b38be0f0eca63564bfb52f)

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

COST_FMT=$(printf '$%.2f' "$COST")
DURATION_SEC=$((DURATION_MS / 1000))
MINS=$((DURATION_SEC / 60))
SECS=$((DURATION_SEC % 60))

echo "[$MODEL] 💰 $COST_FMT | ⏱️ ${MINS}m ${SECS}s"
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
model = data['model']['display_name']
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

duration_sec = duration_ms // 1000
mins, secs = duration_sec // 60, duration_sec % 60

print(f"[{model}] 💰 ${cost:.2f} | ⏱️ {mins}m {secs}s")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;
    const cost = data.cost?.total_cost_usd || 0;
    const durationMs = data.cost?.total_duration_ms || 0;

    const durationSec = Math.floor(durationMs / 1000);
    const mins = Math.floor(durationSec / 60);
    const secs = durationSec % 60;

    console.log(`[${model}] 💰 $${cost.toFixed(2)} | ⏱️ ${mins}m ${secs}s`);
});
```

### Отображение нескольких строк

Ваш скрипт может выводить несколько строк для создания более богатого отображения.

![Многострочная строка состояния, показывающая имя модели, каталог, ветку git в первой строке и полосу прогресса использования контекста с затратами и продолжительностью во второй строке](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-multiline.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=a9d0a2fe8e446d80b1abc46da3f93270)

Этот пример объединяет несколько методов: цвета на основе порогов (зелёный ниже 70%, жёлтый 70-89%, красный 90%+), полосу прогресса и информацию о ветке git. Каждый оператор `print` или `echo` создаёт отдельную строку:

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'

# Pick bar color based on context usage
if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
else BAR_COLOR="$GREEN"; fi

FILLED=$((PCT / 10)); EMPTY=$((10 - FILLED))
printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
BAR="${FILL// /█}${PAD// /░}"

MINS=$((DURATION_MS / 60000)); SECS=$(((DURATION_MS % 60000) / 1000))

BRANCH=""
git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"

echo -e "${CYAN}[$MODEL]${RESET} 📁 ${DIR##*/}$BRANCH"
COST_FMT=$(printf '$%.2f' "$COST")
echo -e "${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys, subprocess, os

data = json.load(sys.stdin)
model = data['model']['display_name']
directory = os.path.basename(data['workspace']['current_dir'])
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

CYAN, GREEN, YELLOW, RED, RESET = '\033[36m', '\033[32m', '\033[33m', '\033[31m', '\033[0m'

bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
filled = pct // 10
bar = '█' * filled + '░' * (10 - filled)

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

try:
    branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True, stderr=subprocess.DEVNULL).strip()
    branch = f" | 🌿 {branch}" if branch else ""
except:
    branch = ""

print(f"{CYAN}[{model}]{RESET} 📁 {directory}{branch}")
print(f"{bar_color}{bar}{RESET} {pct}% | {YELLOW}${cost:.2f}{RESET} | ⏱️ {mins}m {secs}s")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;
    const dir = path.basename(data.workspace.current_dir);
    const cost = data.cost?.total_cost_usd || 0;
    const pct = Math.floor(data.context_window?.used_percentage || 0);
    const durationMs = data.cost?.total_duration_ms || 0;

    const CYAN = '\x1b[36m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m', RESET = '\x1b[0m';

    const barColor = pct >= 90 ? RED : pct >= 70 ? YELLOW : GREEN;
    const filled = Math.floor(pct / 10);
    const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);

    const mins = Math.floor(durationMs / 60000);
    const secs = Math.floor((durationMs % 60000) / 1000);

    let branch = '';
    try {
        branch = execSync('git branch --show-current', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
        branch = branch ? ` | 🌿 ${branch}` : '';
    } catch {}

    console.log(`${CYAN}[${model}]${RESET} 📁 ${dir}${branch}`);
    console.log(`${barColor}${bar}${RESET} ${pct}% | ${YELLOW}$${cost.toFixed(2)}${RESET} | ⏱️ ${mins}m ${secs}s`);
});
```

### Кликабельные ссылки

Этот пример создаёт кликабельную ссылку на ваш репозиторий GitHub. Удерживайте Cmd (macOS) или Ctrl (Windows/Linux) и нажмите, чтобы открыть ссылку в браузере.

![Строка состояния, показывающая кликабельную ссылку на репозиторий GitHub](https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/statusline-links.png?fit=max\&auto=format\&n=HDAmBwgbrZVk0pOt\&q=85\&s=4778a144a28cb498c99d5fa018bb374a)

Каждый скрипт получает URL удалённого репозитория, преобразует формат SSH в HTTPS и оборачивает имя репозитория в коды экранирования OSC 8. Версия Bash использует `printf '%b'`, которая более надёжно интерпретирует экранирующие последовательности, чем `echo -e` в разных оболочках:

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')

# Convert git SSH URL to HTTPS
REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

if [ -n "$REMOTE" ]; then
    REPO_NAME=$(basename "$REMOTE")
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    # printf %b interprets escape sequences reliably across shells
    printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
else
    echo "[$MODEL]"
fi
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys, subprocess, re, os

data = json.load(sys.stdin)
model = data['model']['display_name']

# Get git remote URL
try:
    remote = subprocess.check_output(
        ['git', 'remote', 'get-url', 'origin'],
        stderr=subprocess.DEVNULL, text=True
    ).strip()
    # Convert SSH to HTTPS format
    remote = re.sub(r'^git@github\.com:', 'https://github.com/', remote)
    remote = re.sub(r'\.git$', '', remote)
    repo_name = os.path.basename(remote)
    # OSC 8 escape sequences
    link = f"\033]8;;{remote}\a{repo_name}\033]8;;\a"
    print(f"[{model}] 🔗 {link}")
except:
    print(f"[{model}]")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;

    try {
        let remote = execSync('git remote get-url origin', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
        // Convert SSH to HTTPS format
        remote = remote.replace(/^git@github\.com:/, 'https://github.com/').replace(/\.git$/, '');
        const repoName = path.basename(remote);
        // OSC 8 escape sequences
        const link = `\x1b]8;;${remote}\x07${repoName}\x1b]8;;\x07`;
        console.log(`[${model}] 🔗 ${link}`);
    } catch {
        console.log(`[${model}]`);
    }
});
```

### Использование лимита скорости

Отобразите в строке состояния использование ограничения частоты запросов подписки claude.ai или ваши расходы относительно лимита расходов шлюза приложений Claude. Для подписчиков объект `rate_limits` может содержать скользящее окно `five_hour` и еженедельное окно `seven_day`. Каждое окно предоставляет `used_percentage` (от 0 до 100) и `resets_at` (секунды эпохи Unix, когда окно сбрасывается). За шлюзом считывайте объект `spend_limit`, описанный в разделе [поля лимита расходов](#spend-limit-fields).

Объект `rate_limits` присутствует только для подписчиков claude.ai Pro, Max и Ultra или за шлюзом приложений Claude с лимитами расходов, и только после первого ответа API. Каждый скрипт корректно обрабатывает отсутствующие поля, а за шлюзом выводит `spend: $314.12 / $500` или `spend: 63%`, пока поля в долларах отсутствуют:

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
# "// empty" produces no output when rate_limits is absent
FIVE_H=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
WEEK=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

LIMITS=""
[ -n "$FIVE_H" ] && LIMITS="5h: $(printf '%.0f' "$FIVE_H")%"
[ -n "$WEEK" ] && LIMITS="${LIMITS:+$LIMITS }7d: $(printf '%.0f' "$WEEK")%"

# Behind a Claude apps gateway: dollars when the gateway reports them, else the percentage
SPEND_PCT=$(echo "$input" | jq -r '.rate_limits.spend_limit.used_percentage // empty')
SPEND_USD=$(echo "$input" | jq -r '.rate_limits.spend_limit | select(.used_usd != null) | "$\(.used_usd) / $\(.limit_usd)"')
[ -n "$SPEND_PCT" ] && LIMITS="${LIMITS:+$LIMITS }spend: ${SPEND_USD:-$(printf '%.0f' "$SPEND_PCT")%}"

[ -n "$LIMITS" ] && echo "[$MODEL] | $LIMITS" || echo "[$MODEL]"
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
model = data['model']['display_name']

parts = []
rate = data.get('rate_limits', {})
five_h = rate.get('five_hour', {}).get('used_percentage')
week = rate.get('seven_day', {}).get('used_percentage')

if five_h is not None:
    parts.append(f"5h: {five_h:.0f}%")
if week is not None:
    parts.append(f"7d: {week:.0f}%")

# Behind a Claude apps gateway: dollars when the gateway reports them, else the percentage
spend = rate.get('spend_limit', {})
if spend.get('used_percentage') is not None:
    if spend.get('used_usd') is not None:
        parts.append(f"spend: ${spend['used_usd']} / ${spend['limit_usd']}")
    else:
        parts.append(f"spend: {spend['used_percentage']:.0f}%")

if parts:
    print(f"[{model}] | {' '.join(parts)}")
else:
    print(f"[{model}]")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;

    const parts = [];
    const fiveH = data.rate_limits?.five_hour?.used_percentage;
    const week = data.rate_limits?.seven_day?.used_percentage;

    if (fiveH != null) parts.push(`5h: ${Math.round(fiveH)}%`);
    if (week != null) parts.push(`7d: ${Math.round(week)}%`);

    // Behind a Claude apps gateway: dollars when the gateway reports them, else the percentage
    const spend = data.rate_limits?.spend_limit;
    if (spend?.used_percentage != null) {
        parts.push(spend.used_usd != null
            ? `spend: $${spend.used_usd} / $${spend.limit_usd}`
            : `spend: ${Math.round(spend.used_percentage)}%`);
    }

    console.log(parts.length ? `[${model}] | ${parts.join(' ')}` : `[${model}]`);
});
```

### Кэширование дорогостоящих операций

Ваш скрипт строки состояния запускается часто во время активных сеансов. Команды, такие как `git status` или `git diff`, могут быть медленными, особенно в больших репозиториях. Этот пример кэширует информацию git во временный файл и обновляет её только каждые 5 секунд.

Имя файла кэша должно быть стабильным во время вызовов строки состояния в рамках сеанса, но уникальным для разных сеансов, чтобы одновременные сеансы в разных репозиториях не читали состояние git друг друга. Идентификаторы на основе процесса, такие как `$$`, `os.getpid()` или `process.pid`, изменяются при каждом вызове и нарушают кэш. Вместо этого используйте `session_id` из входных данных JSON: он стабилен в течение жизни сеанса и уникален для каждого сеанса.

Каждый скрипт проверяет, отсутствует ли файл кэша или он старше 5 секунд, перед запуском команд git:

```bash Bash theme={null}
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
SESSION_ID=$(echo "$input" | jq -r '.session_id')

CACHE_FILE="/tmp/statusline-git-cache-$SESSION_ID"
CACHE_MAX_AGE=5  # seconds

cache_is_stale() {
    [ ! -f "$CACHE_FILE" ] || \
    # stat -c %Y (Linux) or stat -f %m (macOS) prints the file's last-modified
    # time. The Linux form must run first: on Linux, the macOS form prints a
    # filesystem report to stdout before failing, and that output would be
    # captured by the command substitution and break the arithmetic.
    [ $(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
}

if cache_is_stale; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        BRANCH=$(git branch --show-current 2>/dev/null)
        STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
    else
        echo "||" > "$CACHE_FILE"
    fi
fi

IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

if [ -n "$BRANCH" ]; then
    echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
else
    echo "[$MODEL] 📁 ${DIR##*/}"
fi
```

```python Python theme={null}
#!/usr/bin/env python3
import json, sys, subprocess, os, time

data = json.load(sys.stdin)
model = data['model']['display_name']
directory = os.path.basename(data['workspace']['current_dir'])
session_id = data['session_id']

CACHE_FILE = f"/tmp/statusline-git-cache-{session_id}"
CACHE_MAX_AGE = 5  # seconds

def cache_is_stale():
    if not os.path.exists(CACHE_FILE):
        return True
    return time.time() - os.path.getmtime(CACHE_FILE) > CACHE_MAX_AGE

if cache_is_stale():
    try:
        subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
        branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        staged = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
        modified = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
        staged_count = len(staged.split('\n')) if staged else 0
        modified_count = len(modified.split('\n')) if modified else 0
        with open(CACHE_FILE, 'w') as f:
            f.write(f"{branch}|{staged_count}|{modified_count}")
    except:
        with open(CACHE_FILE, 'w') as f:
            f.write("||")

with open(CACHE_FILE) as f:
    branch, staged, modified = f.read().strip().split('|')

if branch:
    print(f"[{model}] 📁 {directory} | 🌿 {branch} +{staged} ~{modified}")
else:
    print(f"[{model}] 📁 {directory}")
```

```javascript Node.js theme={null}
#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
    const data = JSON.parse(input);
    const model = data.model.display_name;
    const dir = path.basename(data.workspace.current_dir);
    const sessionId = data.session_id;

    const CACHE_FILE = `/tmp/statusline-git-cache-${sessionId}`;
    const CACHE_MAX_AGE = 5; // seconds

    const cacheIsStale = () => {
        if (!fs.existsSync(CACHE_FILE)) return true;
        return (Date.now() / 1000) - fs.statSync(CACHE_FILE).mtimeMs / 1000 > CACHE_MAX_AGE;
    };

    if (cacheIsStale()) {
        try {
            execSync('git rev-parse --git-dir', { stdio: 'ignore' });
            const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
            const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
            const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
            fs.writeFileSync(CACHE_FILE, `${branch}|${staged}|${modified}`);
        } catch {
            fs.writeFileSync(CACHE_FILE, '||');
        }
    }

    const [branch, staged, modified] = fs.readFileSync(CACHE_FILE, 'utf8').trim().split('|');

    if (branch) {
        console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} +${staged} ~${modified}`);
    } else {
        console.log(`[${model}] 📁 ${dir}`);
    }
});
```

### Конфигурация Windows

На Windows Claude Code запускает команды строки состояния через Git Bash, когда Git Bash установлен, или через PowerShell, когда Git Bash отсутствует.

Git Bash обрабатывает неэкранированные обратные слэши как символы экранирования, поэтому путь в стиле Windows, такой как `C:\Users\username\script.mjs`, достигает средства запуска скрипта с удалёнными разделителями и команда не выполняется без видимой ошибки. Записывайте пути к файлам в строке `command` с прямыми слэшами, как показано в примерах ниже. Сокращение `~` также работает и расширяется до вашего домашнего каталога Windows.

Чтобы запустить скрипт PowerShell как вашу строку состояния, вызовите его через `powershell`. Это работает независимо от того, маршрутизирует ли Claude Code команду через Git Bash или PowerShell:

```json settings.json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File C:/Users/username/.claude/statusline.ps1"
  }
}
```

```powershell statusline.ps1 theme={null}
$input_json = $input | Out-String | ConvertFrom-Json
$cwd = $input_json.cwd
$model = $input_json.model.display_name
$used = $input_json.context_window.used_percentage
$dirname = Split-Path $cwd -Leaf

if ($used) {
    Write-Host "$dirname [$model] ctx: $used%"
} else {
    Write-Host "$dirname [$model]"
}
```

Или запустите скрипт Bash напрямую, когда Git Bash установлен:

```json settings.json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

```bash statusline.sh theme={null}
#!/usr/bin/env bash
input=$(cat)
cwd=$(echo "$input" | grep -o '"cwd":"[^"]*"' | cut -d'"' -f4)
model=$(echo "$input" | grep -o '"display_name":"[^"]*"' | cut -d'"' -f4)
dirname="${cwd##*[/\\]}"
echo "$dirname [$model]"
```

## Советы

* **Тестирование с макетными входными данными**: `echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/home/user/project"},"context_window":{"used_percentage":25},"session_id":"test-session-abc"}' | ./statusline.sh`
* **Сохраняйте вывод коротким**: строка состояния имеет ограниченную ширину, поэтому длинный вывод может быть обрезан или неправильно обёрнут
* **Кэшируйте медленные операции**: ваш скрипт запускается часто во время активных сеансов, поэтому команды, такие как `git status`, могут вызвать задержку. См. [пример кэширования](#cache-expensive-operations) для того, как это обработать.

Проекты сообщества, такие как [ccstatusline](https://github.com/sirmalloc/ccstatusline) и [starship-claude](https://github.com/martinemde/starship-claude), предоставляют предварительно построенные конфигурации с темами и дополнительными функциями.

## Устранение неполадок

Если строка состояния пустая, начните с раздела [Строка состояния не отображается](#status-line-not-appearing). Папка, которой вы не доверяете, и скрипт, завершающийся с ошибкой, также оставляют её пустой, как описано в разделах [Требуется доверие рабочего пространства](#workspace-trust-required) и [Ошибки скрипта или зависания](#script-errors-or-hangs).

### Строка состояния не отображается

Если вы настроили строку состояния, но внизу интерфейса ничего не отображается, выполните следующие проверки:

* Убедитесь, что ваш скрипт исполняемый: `chmod +x ~/.claude/statusline.sh`
* Проверьте, что ваш скрипт выводит в stdout, а не stderr
* Запустите ваш скрипт вручную, чтобы убедиться, что он выводит результат
* В Windows с установленным Git Bash обратные слэши в пути `command` вероятно будут использованы как символы экранирования перед запуском скрипта. Используйте прямые слэши в пути. См. [Конфигурация Windows](#windows-configuration).
* Если `disableAllHooks` установлен на `true` вне управляемых настроек после применения [приоритета настроек](https://code.claude.com/docs/ru/hooks.md#disable-or-remove-hooks), Claude Code запускает только `statusLine` из управляемых настроек, и без управляемого `statusLine` строка состояния отключена. Удалите эту настройку или установите её на `false` в файле, который её устанавливает, чтобы повторно включить. См. [`disableAllHooks`](https://code.claude.com/docs/ru/settings-reference#disableallhooks).
* Если ваша организация устанавливает `allowManagedHooksOnly` в управляемых настройках, ваша пользовательская строка состояния исчезает без предупреждения: вы можете получить строку состояния только из значения `statusLine` в этих управляемых настройках. См. [что запускается под `allowManagedHooksOnly`](https://code.claude.com/docs/ru/settings-reference#what-runs-under-allowmanagedhooksonly) для полного поведения и спросите у вашего администратора, применяется ли эта настройка к вам.
* Запустите `claude --debug`, чтобы записать stderr вашего скрипта при каждом вызове строки состояния и его код выхода при первом вызове в сессии
* Попросите Claude прочитать ваш файл настроек и выполнить команду `statusLine` напрямую, чтобы выявить ошибки

### Строка состояния показывает `--` или пустые значения

Поля могут быть `null` до завершения первого ответа API, поэтому обрабатывайте значения null в вашем скрипте с резервными вариантами, такими как `// 0` в jq. Перезапустите Claude Code, если значения остаются пустыми после нескольких сообщений.

### Процент контекста показывает неожиданные значения

Строка состояния сообщает количества из последнего ответа API, в то время как `/context` добавляет оценку для сообщений, добавленных с момента этого ответа, поэтому `/context` может показывать более высокие значения до следующего ответа. Используйте `used_percentage` для простейшего точного состояния контекста. Формулу, по которой вычисляется `used_percentage`, см. в разделе [Поля контекстного окна](#context-window-fields).

### Ссылки OSC 8 не кликабельны

Будет ли ссылка кликабельной, зависит от вашего терминала, от того, обнаруживает ли Claude Code в нём поддержку гиперссылок, от того, удаляют ли SSH или tmux управляющую последовательность, и от того, как ваш скрипт её выводит:

* Убедитесь, что ваш терминал поддерживает гиперссылки OSC 8 (iTerm2, Kitty, WezTerm)

* Terminal.app не поддерживает кликабельные ссылки

* Если текст ссылки отображается, но не кликабелен, Claude Code может не обнаружить поддержку гиперссылок в вашем терминале. Установите переменную окружения `FORCE_HYPERLINK` для переопределения обнаружения перед запуском Claude Code:

  ```bash theme={null}
  FORCE_HYPERLINK=1 claude
  ```

  В PowerShell сначала установите переменную в текущей сессии:

  ```powershell theme={null}
  $env:FORCE_HYPERLINK = "1"; claude
  ```

* Сессии SSH и tmux могут удалять последовательности OSC в зависимости от конфигурации

* Если последовательности экранирования отображаются как буквальный текст, например `\e]8;;`, используйте `printf '%b'` вместо `echo -e` для более надёжной обработки экранирования

### Глюки отображения с последовательностями экранирования

Сложные последовательности экранирования (цвета ANSI, ссылки OSC 8) могут иногда вызывать искажённый вывод, если они перекрываются с другими обновлениями пользовательского интерфейса. Многострочные строки состояния с кодами экранирования более подвержены проблемам отображения, чем однострочный простой текст.

Если вы видите повреждённый текст, попробуйте упростить ваш скрипт до простого текстового вывода.

### Требуется доверие рабочего пространства

Пока вы не примете диалог доверия рабочего пространства, строка состояния остаётся пустой. Поскольку `statusLine` выполняет команду оболочки, Claude Code запускает её под тем же [правилом доверия рабочего пространства, что и хуки в файлах настроек](https://code.claude.com/docs/ru/permissions.md#what-runs-before-you-trust-a-folder). Достаточно принять диалог для папки или для родительского каталога, чьё доверие распространяется на неё.

До этого `claude --debug` записывает в лог `Status line command skipped: workspace trust not accepted`. Перезапустите Claude Code и примите диалог доверия, чтобы включить её.

### Ошибки скрипта или зависания

Claude Code отображает вывод вашего скрипта только после того, как скрипт завершится с кодом 0:

* Скрипты, которые выходят с ненулевыми кодами или не выводят результат, вызывают пустую строку состояния
* Медленные скрипты блокируют обновление строки состояния до их завершения. Держите скрипты быстрыми, чтобы избежать устаревшего вывода.
* Если новое обновление срабатывает, пока медленный скрипт работает, выполнение скрипта отменяется
* Протестируйте ваш скрипт независимо с макетными входными данными перед его настройкой

### Уведомления делят строку со строкой состояния

Вне [полноэкранного отображения](https://code.claude.com/docs/ru/fullscreen.md) Claude Code показывает уведомления на той же строке, что и ваша строка состояния. При полноэкранном отображении Claude Code выделяет уведомлениям отдельную строку.

* Системные уведомления, такие как ошибки MCP-сервера и автоматические обновления, отображаются на правой стороне строки. Временные уведомления, такие как предупреждение о низком контексте, также циклически сменяются в этой области.
* Включение подробного режима добавляет в эту область счётчик токенов, который показывает размер вашего контекста согласно последнему ответу API, а не [счётчик за ход рядом со спиннером](https://code.claude.com/docs/ru/costs.md#read-the-token-count-beside-the-spinner)
* На узких терминалах эти уведомления могут обрезать вывод вашей строки состояния
