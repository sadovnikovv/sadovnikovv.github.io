> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Устранение неполадок мода

> Узнайте, почему мод Claude Code ничего не делает: сопоставьте симптом или сообщение с его причиной, посмотрите сообщения об отказе и прочитайте лог отладки.

Когда модуль мода или один из его хуков дает сбой, Claude Code пропускает его и сессия продолжается, поэтому неработающий мод может выглядеть как мод, который ничего не делает. Начните с проверки того, что Claude Code прочитал из вашего мода и где он сообщает о проблеме, затем найдите симптом или сообщение, которое у вас есть.

## Узнайте, почему мод ничего не делает

Когда мод ничего не делает, проверьте, что Claude Code читает из файлов мода, и строку, которую он пишет, когда что-то пропускает. Для первого запустите [`claude plugin validate`](https://code.claude.com/docs/ru/plugins/mods/create#check-what-claude-code-reads-from-your-mod) в вашей оболочке с директорией мода, как в `claude plugin validate ./first-mod`. Это ловит неправильно написанное событие, неправильный манифест и модуль, который Claude Code не может прочитать, без запуска сессии.

Когда модуль не загружается, hook пропускается или другой мод отказывает вашему, Claude Code пишет одну строку, которая называет ваш мод. Где вы читаете эту строку, зависит от сеанса:

* **Сессия, которая горячо перезагружает директорию плагина**: тусклая строка в транскрипте. Это интерактивная сессия, которую вы запустили с `--plugin-dir`, или сессия, где [включена горячая перезагрузка](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod) для модов, которые написал Claude.
* **Любая другая интерактивная сессия, например та, которая запускает мод, установленный вами из маркетплейса**: [лог отладки](#read-the-debug-log). Чтобы получить его, запустите сессию с `claude --debug`.
* **Запуск `claude -p` с `--plugin-dir`**: stderr в формате вывода текста по умолчанию. Отказ другого мода идет в лог отладки.

## Проверьте, могут ли загружаться моды

Чтобы проверить, позволяет ли ваша установка вообще загружать моды, без установки одного, запустите `claude plugin test` в вашей оболочке из директории, которая не содержит мода. Вам не нужен сеанс. Сообщение, которое оно печатает, говорит вам о состоянии:

| Сообщение включает | Что это означает |
| :- | :- |
| `no hooks module to load` | Моды могут загружаться. Команда не нашла мода для тестирования в этой директории. |
| `hooks modules are turned off here` | Настройка препятствует вашим модам: `disableAllHooks` в ваших собственных настройках или политика вашей организации |
| `hooks modules are turned off in this process: the rollout switch served off` | Anthropic отключила установленные моды удаленно. |
| `hooks modules are turned off in this process: the rollout switch was saved off by an earlier session` | Команда использовала значение, сохраненное более ранней сессией, которое может быть устаревшим. Запустите `claude` один раз, чтобы обновить его, затем снова выполните команду. |

Организация также может установить `allowManagedModsOnly`, чтобы разрешить только свои моды, что эта команда не сообщает. В этом случае Claude Code отклоняет мод, который вы устанавливаете, и [сообщение говорит почему](https://code.claude.com/docs/ru/plugins/mods/troubleshoot.md#messages-from-the-built-in-guard).

## Мод не загружается

Ничего, что добавляет мод, не появляется: нет команды, нет рисунка и нет изменения в поведении.

### Ваша версия слишком старая

См. [какую версию использовать и как проверить свою](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off).

### Строка `mods active` не называет мод

Ничего, что добавляет мод, не появляется, и [строка `mods active`](https://code.claude.com/docs/ru/plugins/mods/overview#see-which-mods-a-session-loaded) в `/plugin` не называет его. Модуль hooks не загрузился. Когда Claude Code отказала ему, журнал отладки имеет строку, которая начинается с `hooks module`, имени мода и `not loaded:`, как в `hooks module first-mod@inline not loaded: disableAllHooks in managed settings` для мода, загруженного с `--plugin-dir`.

Прочитайте причину после двоеточия. Раздел [сообщения об отказе](#refusal-messages) перечисляет каждое. Если журнал не имеет такой строки, пройдите через другие записи в этой группе.

Некоторые настройки останавливают мод, оставляя остальную часть его плагина работающей. Раздел [Включение и отключение модов](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off) называет их.

### Запуск `claude -p` печатает `hooks module not loaded`

Строка начинается с имени мода и идет в stderr. Модуль hooks был отказан. Неинтерактивный запуск не имеет стенограммы, поэтому сообщение идет в stderr.

Прочитайте причину после двоеточия. Раздел [сообщения об отказе](#refusal-messages) перечисляет каждое.

### Сообщения об отказе

Каждое из них следует за `hooks module`, именем мода и `not loaded:` в журнале отладки.

| Сообщение начинается с | Что это означает |
| :- | :- |
| `hooks modules are turned off for installed plugins in this process: the rollout switch served off` | Anthropic отключила установленные моды удаленно. |
| `hooks modules are turned off for installed plugins in this process: the rollout switch was saved off by an earlier session` | Сессия использовала значение, сохраненное более ранней сессией, которое может быть устаревшим. Запустите Claude Code снова, чтобы обновить его. |
| `disableAllHooks in managed settings` | Ваша организация отключила hooks из установленных плагинов |
| `only managed plugins and built-in plugins run` | `allowManagedHooksOnly` установлен или `disableAllHooks` установлен в файле параметров, отличном от управляемых параметров |
| `installed plugins that are not managed load no hooks module in this mode (--bare)` | Вы запустили Claude Code с `--bare` |
| `another plugin of that name loads first` | Другой включенный плагин имеет то же имя, что и ваш мод, и [удерживает это имя](https://code.claude.com/docs/ru/plugins/loading.md#hooks-when-two-enabled-plugins-share-a-name), поэтому ваш модуль хуков не загружается |

### Сообщения от встроенной защиты

Там, где загружается [встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default), он может отклонить мод или один из его ответов. Некоторые сообщения называют опцию, которую администратор вашей организации задает для изменения правила.

| Сообщение содержит | Что это означает | Где оно появляется |
| :- | :- | :- |
| `mods are limited to your organization's by policy (allowManagedModsOnly)` | Ваша организация разрешает только [свои моды](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods), поэтому ваш был отклонен | Лог отладки, а также транскрипт в [сессии, которая выполняет горячую перезагрузку директории плагина](#find-out-why-a-mod-does-nothing) |
| `tried to lift a deny rule in your settings` | Хук [`tool.check`](https://code.claude.com/docs/ru/plugins/mods/reference#tools) вашего мода одобрил вызов, который отклоняет правило `deny`. Вызов остается отклоненным. | Транскрипт и лог отладки, один раз для каждого мода в сессии. При запуске `claude -p` — лог отладки. |
| `the rules and hooks in your settings could not be checked for this call, so it is refused` | Страж дал сбой при проверке вызова, который одобрил мод, поэтому он отклонил этот вызов | Причина, которую Claude читает для отклоненного вызова |

### `validate` проходит и не перечисляет строку `hooks`

`hooks/hooks.json` не имеет ключа `modules` или ключ неправильно написан.

Добавьте `"modules": ["./register.js"]`.

### `hooks module did not load`

Строка начинается с имени мода, затем `hooks module did not load:` и причина, которая указывает файл и строку при синтаксической ошибке. Claude Code не смог загрузить модуль, например потому что его код верхнего уровня выбросил исключение.

Исправьте ошибку, которую называет причина.

Если причина заканчивается на `; the version loaded before is unloaded`, ни одна версия мода сейчас не работает. Когда вы исправите ошибку, выполните [`/reload-plugins`](https://code.claude.com/docs/ru/plugins/cli-reference#reload-plugins) в сессии, чтобы снова загрузить мод. Если вы установили мод, а не написали его, попросите его автора исправить ошибку.

### `options do not fit plugin.json userConfig`

Строка начинается с имени мода, затем `hooks module did not load: options do not fit plugin.json userConfig:` и причина. Опция не проходит проверку по своему полю [`userConfig`](https://code.claude.com/docs/ru/plugins/components#user-configuration), например число выше `max` поля, или обязательное поле не имеет значения.

Установите или измените значение. Конец строки называет его запись `pluginConfigs` в `settings.json`.

### `code nested too deep to scan: more than 2000 scopes`

Строка начинается с имени мода, затем `hooks module did not load:`, файл и `code nested too deep to scan: more than 2000 scopes`. Файл в модуле хуков не может вкладывать области видимости, такие как функции, блоки и циклы, глубже чем на [2 000 уровней](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits). [`claude plugin validate`](https://code.claude.com/docs/ru/plugins/mods/create#check-what-claude-code-reads-from-your-mod) сообщает ту же причину.

Перепишите код так, чтобы его области видимости были вложены менее глубоко.

### `the engine ran out of stack linking the file and its imports`

Код в модуле хуков вложен слишком глубоко или его цепочка импортов слишком длинная, чтобы Claude Code мог его загрузить. Строка начинается с имени мода и `hooks module did not load:`, затем указывает имя файла и эту причину.

Просмотрите этот файл и файлы, к которым ведут его импорты, найдите наиболее глубоко вложенную часть и перепишите её так, чтобы вложенность была меньше, или сократите цепочку импортов. Если мод написали не вы, попросите его автора исправить это.

### `the parser stopped` или `the engine ran out of stack loading the file`

Код в одном из файлов модуля хуков вложен настолько глубоко, что Claude Code исчерпал стек при его чтении. Строка начинается с имени мода и `hooks module did not load:`, затем указывает имя этого файла и одну из следующих причин:

* `code nested too deep to scan (the parser stopped: <message>)`
* `the engine ran out of stack loading the file (code nested too deep): <message>`

Причина не указывает номер строки и не сообщает, какой именно код вложен, поэтому самостоятельно просмотрите файл и найдите его наиболее глубоко вложенную часть. Перепишите эту часть так, чтобы вложенность была меньше. Если вы установили мод, а не написали его, попросите об этом его автора.

### Ни один мод не загружается в директории, которую вы открыли впервые

Вы не ответили на приглашение доверия для директории.

Запустите интерактивный сеанс в этой директории с `claude` и примите приглашение доверия, которое оно открывает.

### Ни один установленный плагин не загружается вообще

Вы запустили Claude Code с `--safe-mode`.

Запустите без флага.

### Claude Code перестает предлагать включить горячую перезагрузку

Claude пишет мод в интерактивной сессии, ничего не загружается, и Claude Code больше не спрашивает, [включить ли горячую перезагрузку](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod). Если вопрос трижды завершается без выбранного ответа, горячая перезагрузка остается отключенной. Например, вопрос завершается так, когда вы задали [`askUserQuestionTimeout`](https://code.claude.com/docs/ru/settings-reference#askuserquestiontimeout) и время истекает до вашего ответа. Эта настройка применяется здесь, потому что Claude Code задает вопрос в том же [диалоге вопросов, который использует `AskUserQuestion`](https://code.claude.com/docs/ru/tools-reference#question-auto-continue-timeout). Вопрос, который вы закрываете сами, не засчитывается в эти три.

Чтобы запустить мод, [скопируйте его директорию из папки модов](https://code.claude.com/docs/ru/plugins/mods/create.md#use-the-mod-in-other-sessions), затем в оболочке запустите новую сессию с `--plugin-dir`, как в `claude --plugin-dir ~/mods/git-branch`.

## Hook пропускается или мод выгружается

### `hook skipped`

Строка называет мод и событие, затем содержит `hook skipped:` и причину, как в `first-mod: tool.call hook skipped: threw Error: boom`. Хук выбросил исключение, превысил свое [ограничение по времени](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits) или вернул результат неправильной формы. Строка появляется один раз для каждого события и вида сбоя до перезагрузки мода.

Исправьте ошибку. Журнал отладки имеет строку для каждого возникновения.

### `no command.run hook answered it`

Вы запускаете команду, которую добавил ваш мод, и ответ называет мод и команду, как в `first-mod registered /tally but no command.run hook answered it`, затем говорит вам добавить hook. Claude Code выводит этот ответ, когда команда достигает конца цепи без ответа, что происходит в двух случаях:

* **Ни один hook не ответил на команду**: модуль не имеет `command.run` hook, [фильтр](https://code.claude.com/docs/ru/plugins/mods/events.md#filter-which-events-a-hook-handles) hook называет другую команду или hook вернул `next(e)`
* **Claude Code пропустила hook**: [`hook skipped`](#hook-skipped) перечисляет причины. Передача `focus: false` в [`$.ui.open`](https://code.claude.com/docs/ru/plugins/mods/interface#open-a-pane-at-the-right-time) — один из способов туда попасть.

Если модуль уже имеет hook, который описывает ответ, ищите строку `hook skipped`, которая называет `command.run`, что дает причину. [Тест](https://code.claude.com/docs/ru/plugins/mods/test.md), который запускает команду, не проходит по той же причине.

### `it crashed the hooks worker`

Строка начинается с имени мода, как в `first-mod was unloaded: it crashed the hooks worker`. Установленные моды используют один рабочий поток. Рабочий перестал отвечать или упал, и Claude Code проследила это до этого мода и выгрузила его. Hook, который блокирует поток, например цикл, который никогда не ожидает, является одной из причин.

Исправьте hook.

### `its session.start ran again in a fresh copy`

Строка начинается с имени мода и называет вызов `$.prompt.submit`, `$.command.run` или `$.agent.spawn`, как в `first-mod: its session.start ran again in a fresh copy; the $.prompt.submit call it had already made was not made again`. Claude Code снова загрузила модуль мода, например после того как рабочий поток хуков упал и был заменен, и в свежей копии выполнился хук [`session.start`](https://code.claude.com/docs/ru/plugins/mods/reference#session). Вызов, названный в строке, вернул результат своего первого выполнения вместо повторного выполнения, поэтому ваш мод не отправляет промпт, не запускает команду и не запускает субагента дважды. Остальная часть хука выполнилась как обычно.

Исправлять ничего не нужно.

До v2.1.292 вызов выполнялся второй раз, поэтому промпт отправлялся, команда запускалась или субагент запускался дважды.

### `This mod's change didn't load` или `the earlier version is no longer running`

Изменение в [моде, который Claude написала в этой сессии](https://code.claude.com/docs/ru/plugins/mods/create.md#ask-claude-for-a-mod), не удалось загрузить. Строка в транскрипте начинается с имени мода и заканчивается причиной:

* `This mod's change didn't load, so the earlier version is still running: <reason>.`
* `This mod didn't load, and the earlier version is no longer running: <reason>.`

Claude не видит эту строку, поэтому вставьте ее в свое следующее сообщение, когда попросите Claude исправить проблему.

### `reload failed`

Сопоставьте строку, чтобы узнать, загружена ли еще последняя рабочая версия вашего мода:

* `reload failed, the previous version stays loaded: <reason>`: ваш мод продолжает выполнять свою последнюю рабочую версию. Если ваше изменение по-прежнему не загрузится при следующей перезагрузке всех плагинов в Claude Code, например когда вы запустите `/reload-plugins`, последняя рабочая версия выгрузится.
* `reload failed: <reason>`: запустите `/plugin` в промпте Claude Code и расширьте терминал, если [строка `mods active`](https://code.claude.com/docs/ru/plugins/mods/overview#see-which-mods-a-session-loaded) обрезает имена. Если она называет мод, его последняя рабочая версия все еще загружена. Если не называет или такой строки нет, не загружена ни одна версия.

Исправьте то, что указано в причине, и сохраните изменение. Строка `reloaded` показывает, что оно загрузилось.

### `$.agent.register refused: the hooks module that made the call is no longer loaded`

Строка начинается с имени вашего мода, как в `first-mod: $.agent.register refused: the hooks module that made the call is no longer loaded (it was reloaded or removed)`, и агент не регистрируется. Ваш мод был перезагружен или выгружен до вызова. Перезагрузка загружает свежую копию модуля хуков, а этот вызов пришел из кода, который все еще выполнялся в старой копии, например из хука, который еще не вернул результат.

Если этот хук не перехватывает отказ, он завершается сбоем, и Claude Code [пропускает его](#hook-skipped). Чтобы зарегистрировать агента из копии, которая остается загруженной, выполните вызов в своем хуке [`session.start`](https://code.claude.com/docs/ru/plugins/mods/reference#session), который снова выполняется в каждой свежей копии после перезагрузки.

### `mods that run in the hooks worker are off for this session`

Строка читает `hooks: mods that run in the hooks worker are off for this session: it crashed 3 times`. Рабочий остановился три раза и Claude Code не смогла проследить остановки до одного мода, поэтому она выгрузила каждый мод, который не встроен, включая моды, которые устанавливает ваша организация. Эта строка достигает стенограммы в каждом интерактивном сеансе.

Запустите `/reload-plugins` для их перезагрузки.

## Вызов инструмента отказан

Мод загрузился и его hooks работают, и вызов инструмента, который он коснулся, отказан.

### `a hook changed this call's input after the model wrote it`

В автоматическом режиме отказанный вызов инструмента дает эту причину. Hook изменила входные данные вызова инструмента после того, как [классификатор на стороне сервера](https://code.claude.com/docs/ru/permission-modes.md#server-side-classifier-review) его рассмотрел, поэтому этот обзор не охватывает то, что будет запущено. Hook может быть [`tool.call`](https://code.claude.com/docs/ru/plugins/mods/reference#tools) мода или [`turn.step`](https://code.claude.com/docs/ru/plugins/mods/reference#turns) hook или [`PreToolUse`](https://code.claude.com/docs/ru/hooks#pretooluse) hook параметров. Сообщение не говорит, какой.

Сообщение говорит Claude выдать вызов еще раз, как записано. Если это также отказано, hook изменяет входные данные каждый раз, поэтому отключите мод или hook или выйдите из автоматического режима и одобрите вызов сами.

> [!NOTE]
>
> В [некоторых интерактивных сессиях терминала и сессиях VS Code](https://code.claude.com/docs/ru/hooks.md#pretooluse-updatedinput-in-auto-mode) такой же отказ сопровождается причиной `a hook changed this call's input after auto mode reviewed it`. Повторный вызов в этом случае содержит первое изменение мода, и хук `tool.call` всё равно выполняется для него, но дальнейшее изменение отбрасывается. Вам не нужно менять свой мод, если только Claude не сообщит в своём ответе, что [авторежим не смог проверить вызов](https://code.claude.com/docs/ru/errors.md#hook-changed-input-after-review).

### Сообщение о правилах deny в ваших параметрах

`tried to lift a deny rule in your settings` и `the rules and hooks in your settings could not be checked for this call, so it is refused` — оба сообщения исходят от встроенного стража.

Посмотрите их в [Сообщения от встроенной защиты](#messages-from-the-built-in-guard).

## После остановки хода появляется всплывающее уведомление

### `Stopped: type a message to continue; a mod cannot resume work after Stop`

Это всплывающее уведомление означает, что после того, как вы остановили ход, например клавишей Esc, мод попытался самостоятельно начать работу, и Claude Code не позволил ему это сделать. Ничего исправлять не нужно. После вашего следующего сообщения моды снова смогут начинать работу, и [часть этой работы вернётся](https://code.claude.com/docs/ru/plugins/mods/api.md#work-your-mod-started-before-the-interruption) сама по себе. Если то, что вы ожидали от мода, не вернётся, попросите об этом снова или повторно выполните команду мода.

Если вы написали этот мод, см. раздел [Вызовы и фоновая работа после того, как пользователь прерывает ход](https://code.claude.com/docs/ru/plugins/mods/api.md#calls-and-background-work-after-the-user-interrupts-a-turn).

## Рисунок не появляется или не отвечает

Мод загрузился, и его панель, полоса, всплывающее уведомление или элементы управления не ведут себя так, как вы ожидаете.

### Полоса другого мода отображается, а ваша нет

Каждый мод, который рисует над промптом, получает собственную строку, поэтому если вашей нет, а строка другого мода отображается, проверьте следующие причины:

* **Ваше дерево не проходит валидацию**: [запишите лог отладки](#read-the-debug-log), найдите в нем [`ui.render hook skipped`](#a-pane-or-band-is-empty) или [`does not validate`](#ui-render-refused) и исправьте то, что названо в строке.
* **Строки вместе превышают ограничение**: [запишите лог отладки](#read-the-debug-log) и найдите в нем `past the limits of the band`. Строки [используют общие ограничения одного дерева](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits), поэтому нарисуйте дерево меньшего размера или попросите авторов других модов сделать это.
* **Другой мод скрывает вашу строку или рисует поверх нее**: если в логе нет ни одной из этих строк, [отключите](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off) другие моды по одному. Если ваша строка вернется, попросите автора этого мода изменить его.

До v2.1.323 все моды использовали один общий рисунок в полосе. Мод, который выполнялся [до вашего](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in), заменял ваш рисунок, когда возвращал дерево, в котором нет результата `next(e)`. Обновите Claude Code или попросите автора этого мода внести следующие изменения:

* **Сохраните рисунки модов после него**: поместите результат `await next(e)` среди дочерних элементов `Box` в его дереве
* **Сохраните дерево валидным**: не задавайте этому `Box` или любому `Box` вокруг него проп `width`, `height`, `minWidth`, `minHeight`, `position`, `top`, `left`, `right`, `bottom`, `display` или `overflow`

### Панель или полоса пуста или показывает обычное содержимое Claude Code

[Дерево](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-tree-from-elements), которое вернул ваш хук, не прошло валидацию. Строка [`hook skipped`](#hook-skipped) [в транскрипте или логе отладки](#find-out-why-a-mod-does-nothing) называет ваш мод и причину, как в этой строке для `Box` в панели:

```text theme={null}
first-mod: ui.render hook skipped: returned the wrong shape (a tree Pane refuses: Box prop "flexDirection" must be one of row, column, row-reverse, column-reverse)
```

Исправьте то, что названо в причине. Если причина обрезана, [запишите лог отладки](#read-the-debug-log) и найдите в нем `a hook returned a tree that does not validate`, чтобы прочитать остальное.

Если же строка сообщает `refused:` сразу после имени точки, как в `ui.render (Pane) refused:`, см. [Строка `ui.render` сообщает `refused`](#ui-render-refused).

### Строка `ui.render` сообщает `refused`

`ui.render (<site>) refused:` или `ui.render (<site>): the chain settled on a tree that does not validate` в [логе отладки](#read-the-debug-log) означает, что [дерево](https://code.claude.com/docs/ru/plugins/mods/interface.md#build-a-tree-from-elements) в этой точке превышает [ограничение размера](https://code.claude.com/docs/ru/plugins/mods/reference.md#limits). Любая из этих строк называет [точку отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites), а затем причину.

Измените моды, которые рисуют в этой точке, чтобы их хуки [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface) возвращали деревья меньшего размера, или попросите их авторов сделать это. Если строка транскрипта начинается с `hooks`, у нескольких загруженных модов есть хук `ui.render` для этой точки, поэтому проверьте дерево каждого из этих модов. Для строк над промптом, которые вместе не укладываются в ограничения полосы, строка выглядит так:

```text theme={null}
hooks: ui.render (AbovePrompt) refused: a row past the limits of the band; nothing was drawn
```

Несмотря на такое окончание, строки, которые укладываются в ограничения, все равно отрисовываются.

До v2.1.307 строка `refused:` для любой точки сообщала о любом дереве, которое не прошло валидацию, а для `Pane` и `AbovePrompt` она заканчивалась на `; the engine drew its own`. В этих выпусках исправьте то, что названо в причине.

### `needs a key`, `is drawn twice` или `key each once`

У элемента в дереве, которое возвращает ваш хук `ui.render`, нет допустимого [`key`](https://code.claude.com/docs/ru/plugins/mods/interface#which-controls-need-a-key), или два элемента используют один и тот же. Найдите полученное сообщение:

* **`<Input> needs a key` или `<Select> needs a key`**: у элемента нет пропа `key`, или его `key` пуст или не является строкой, как в `key: 3`. Задайте ему в качестве `key` непустую строку.
* **`<Button> needs a key`**: задайте кнопке непустую строку в качестве `key`
* **`is drawn twice; each takes its own key`**: у двух элементов того вида, который назван в сообщении, одинаковый `key`, как в `Input "size" is drawn twice; each takes its own key`. Задайте каждому элементу собственный `key`.
* **`key each once` от `press` в [тесте](https://code.claude.com/docs/ru/plugins/mods/test.md#test-a-drawing)**: в рисунке больше одной кнопки с переданным вами ключом. Кнопки с одинаковой подписью и без пропа `key` используют эту подпись как общий ключ. Задайте каждой кнопке собственный `key`.

### Строка `ui.render` сообщает `threw while drawn`

Строка называет [точку отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites), затем сообщает `threw while drawn:` и ошибку, как в `first-mod: ui.render (ToolUse) threw while drawn: <error>; the engine drew its own`. Claude Code столкнулся с этой ошибкой при отрисовке дерева, которое вернул ваш хук [`ui.render`](https://code.claude.com/docs/ru/plugins/mods/reference#interface), или при отрисовке точки из [`props`, которые ваш хук передал в `next`](https://code.claude.com/docs/ru/plugins/mods/interface#change-what-claude-code-already-draws). Окончание `the engine drew its own` означает, что точка показывает обычное содержимое Claude Code.

Прочитайте ошибку и исправьте значение в вашем хуке, которое ее вызвало.

До v2.1.289 эта ошибка в строке транскрипта завершала сессию с [`Claude Code exited after an unrecoverable interface error`](https://code.claude.com/docs/ru/errors#exited-after-an-unrecoverable-interface-error).

### `the module failed without a message`

[`Client`](https://code.claude.com/docs/ru/plugins/mods/interface#when-a-client-fails) завершился с ошибкой без сообщения, например `throw new Error()`. Строка на его месте выглядит как `my-mod: Client client/spinner.js: the module failed without a message`.

Найдите throw в коде вашего `Client` и задайте ошибке сообщение. Тогда строка покажет это сообщение.

До v2.1.289 строка вместо этого показывала `Error` в качестве причины.

### `$.ui.open` работает и панель не появляется

Вызов не поступил от чего-то, что сделал пользователь, и терминал уже, чем [ширина, необходимая этой панели](https://code.claude.com/docs/ru/plugins/mods/interface.md#when-a-pane-waits-for-a-wider-terminal).

Откройте панель из команды или кнопки или проверьте результат `isPlaced` вызова. См. [Откройте панель в нужное время](https://code.claude.com/docs/ru/plugins/mods/interface.md#open-a-pane-at-the-right-time).

### Всплывающее уведомление не появляется

Ваш мод вызывает [`$.ui.toast`](https://code.claude.com/docs/ru/plugins/mods/api#show-something-without-starting-a-turn) в интерактивной сессии терминала, а вы не видите уведомление. Чтобы убедиться, что вызов выполнился, найдите в [логе отладки](#read-the-debug-log) строку с именем вашего мода и текстом уведомления, как в `$.ui.toast (first-mod): build finished`. Затем проверьте такие причины:

* **Строки для вызова нет**: найдите строку, которая объясняет, почему Claude Code отклонил вызов, как в `first-mod: $.ui.toast dropped: timeoutMs is a whole number of ms, 1 to 60000`.
* **Панель удерживает уведомления**: ваш или другой мод передал [`holdToasts`](https://code.claude.com/docs/ru/plugins/mods/interface#hold-toasts-behind-a-dialog) при открытии отображаемой панели. Закройте панель, чтобы прекратить удержание. Если панель ваша и должна оставаться открытой, удалите `holdToasts` из ее вызова `$.ui.open` и откройте панель снова.
* **Уведомление находится под промптом**: в [классическом рендерере](https://code.claude.com/docs/ru/fullscreen.md#enable-fullscreen-rendering) посмотрите справа под промптом. Уведомление там - это одна строка, начинающаяся с имени мода, а не блок в правом верхнем углу.
* **Ваш мод показал более новое уведомление**: в классическом рендерере более новое уведомление от вашего мода может заменить то, которое отображается или ожидает отображения. В логе отладки есть еще одна строка для старого уведомления, которая заканчивается на `gave way, cut short`, если оно отображалось, или на `gave way, unseen`, если оно так и не появилось. Чтобы показать оба сообщения, поместите их в одно уведомление.
* **Время уведомления истекло до отрисовки**: в полноэкранной отрисовке Claude Code отрисовывает не более трех уведомлений одновременно, поэтому время уведомления может истечь до его отрисовки. В логе отладки есть еще одна строка для этого уведомления, которая заканчивается на `left the stack, never drawn`. Когда ваш мод показывает несколько уведомлений сразу, поместите сообщения в одно уведомление.

До v2.1.290 Claude Code отбрасывал уведомление, показанное в течение двух секунд после последнего уведомления, которое он отобразил для вашего мода, и строка лога отладки для отброшенного уведомления сообщала `within 2000ms of the last; dropped`.

### Полоса показывает `plugin panel hidden`

Полоса [свернута](https://code.claude.com/docs/ru/plugins/mods/interface.md#when-the-user-collapses-the-band). Она сворачивается, когда вы нажимаете Ctrl+X, затем Ctrl+A, или клавиши, которые вы назначили вместо них, а в [полноэкранной отрисовке](https://code.claude.com/docs/ru/fullscreen.md) - когда вы щелкаете `[-]` в ее первой строке. Она остается свернутой, пока вы не развернете ее или снова не запустите Claude Code, и все это время ни горячая клавиша, ни привязка `action` не нажимает кнопки в ней.

Чтобы развернуть полосу, нажмите клавиши, указанные в строке, по умолчанию Ctrl+X, затем Ctrl+A, или в полноэкранной отрисовке щелкните строку.

### Горячие клавиши ничего не делают

Ваша панель или полоса не имеет фокуса клавиатуры, ваша кнопка находится в свернутой полосе, другой мод использует ту же клавишу, или рисунок находится в расширении VS Code.

* **Нет фокуса клавиатуры**: нажмите Ctrl+X затем Tab или в [полноэкранной отрисовке](https://code.claude.com/docs/ru/fullscreen.md) щелкните панель или полосу. Чтобы панель получала фокус при открытии, откройте ее с `focus: true` из команды.
* **Кнопка находится в свернутой полосе**: полоса показывает одну тусклую строку, начинающуюся с `▸ plugin panel hidden`. Нажмите клавиши, указанные в строке, по умолчанию Ctrl+X, затем Ctrl+A, чтобы [развернуть ее](#plugin-panel-hidden).
* **Строка другого мода в полосе использует ту же горячую клавишу**: в терминале нажатие клавиши не нажимает ни одну из кнопок. Чтобы проверить это, [отключайте](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off) другие моды, которые рисуют строки, по одному, пока клавиша не заработает. Измените `hotkey` вашей кнопки или попросите автора этого мода изменить свою.
* **В расширении VS Code, где у кнопок нет горячих клавиш**: щелкните кнопку или нажмите Enter на ней, когда она получит фокус

### Рисунок работает в терминале и не в приложении Desktop или VS Code

Либо это приложение не отрисовывает точку отрисовки или элемент, либо сессия относится к тем, в которых расширение VS Code ничего не отрисовывает для модов. Другие хуки мода по-прежнему выполняются. Проверьте такие причины:

* **Точка отрисовки или элемент не отрисовываются в этом приложении**: найдите вашу точку в таблице [точек отрисовки](https://code.claude.com/docs/ru/plugins/mods/reference.md#render-sites), а ваши элементы - в таблице [элементов](https://code.claude.com/docs/ru/plugins/mods/reference.md#elements). Для элемента, которого нет в приложении, проверьте `e.surface` в хуке и верните дерево, которое приложение может отрисовать.
* **Расширение VS Code старше 2.1.299**: панель чата отрисовывает содержимое модов начиная с [версии расширения](https://code.claude.com/docs/ru/vs-code.md#install-the-extension) 2.1.299. Проверьте версию в представлении Extensions в VS Code и обновите расширение там.
* **Расширение старше 2.1.304, и сессия не загружает флаги функций**: обновите расширение или вместо этого запустите `claude` во встроенном терминале VS Code. Сессии в Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry пропускают эту загрузку. О других сессиях, которые ее пропускают, например о сессии через [шлюз приложений Claude](https://code.claude.com/docs/ru/claude-apps-gateway), см. [Функции, которым нужна загрузка флагов функций](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching).

## Правка или значение потеряны

Мод работает, но внесённого вами изменения или сохранённого им значения нет.

### Ваши правки не вступают в силу

Вы редактируете установленный плагин. Claude Code запускает кэшированную копию установленной версии.

Ведите разработку с `--plugin-dir`, указывающим на вашу рабочую копию, например `claude --plugin-dir ./first-mod`, — тогда мод перезагружается при сохранении.

### Значение сбрасывается при перезагрузке модуля

Переменные уровня модуля инициализируются заново при каждой перезагрузке.

[Храните значение в `$.state` или `$.store`](https://code.claude.com/docs/ru/plugins/mods/interface#keep-state).

### Значение сбрасывается после `/clear`, `/resume` или `/branch`

Значение сбрасывается, или сохранённое значение заменяется значением по умолчанию. Каждая из этих команд сбрасывает `$.state` к значениям по умолчанию, а `session.start` повторно не срабатывает.

[Загрузите сохранённое значение снова](https://code.claude.com/docs/ru/plugins/mods/interface.md#load-a-saved-value-again-after-clear) в хуке `classic.SessionStart`.

### Ключ, который возвращает ваш хук `settings.read`, не вступает в силу

Если вы возвращаете правила разрешений или `env` при [собственном чтении Claude Code](https://code.claude.com/docs/ru/plugins/mods/events.md#settings-read-hook), эти правила не проверяются при вызовах инструментов, а записи `env` не становятся переменными окружения. Используйте для того и другого [файл настроек](https://code.claude.com/docs/ru/settings.md) или [`$.env.set`](https://code.claude.com/docs/ru/plugins/mods/api#reach-files-processes-and-the-network) для `env`.

Для другого ключа проверьте, [какие моды получают `settings.read` и с какой версии](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-hook), затем найдите в [логе отладки](#read-the-debug-log) `settings.read` и поищите одну из следующих строк:

| Строка лога | Значение и действие |
| :- | :- |
| `settings.read hook skipped` после имени вашего мода | Ваш хук завершился с ошибкой. [Исправьте ошибку, о которой сообщает строка](#hook-skipped). |
| `settings.read bypassed by cc-plugin-sec-default` в строке, где перед ним указано имя вашего мода | [Встроенный страж](https://code.claude.com/docs/ru/plugins/mods/admin.md#know-what-happens-by-default) не стал запускать ваш хук. Попросите администратора вашей организации [установить мод как один из модов организации](https://code.claude.com/docs/ru/plugins/mods/admin.md#install-your-organizations-mods). |
| `settings.read: the answer for <key> is no value the key can hold` | Claude Code отклонил значение, которое хук вернул для этого ключа. Это может быть ваш хук или хук другого мода. Выполните [действие для вашего случая](#settings-read-key-refused). |
| `settings.read: the merge never settles for <key>` | Ключи, указанные в строке, сохраняют значения из источников настроек. Задайте их в файле настроек. |
| `answered settings.read without next()` после имени мода | Это затрагивает ваш хук, если указанный мод [выполняется раньше вашего](https://code.claude.com/docs/ru/plugins/mods/events.md#the-order-mods-run-in). В этом случае ваш хук не выполнился при этом чтении. [Отключите этот мод](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off) или, если его развернула ваша организация, попросите об этом её администратора. |
| `settings.read: refused to the engine` | Ваше значение не применилось, потому что в собственном чтении Claude Code было отказано. [Выясните, кто отказал](#settings-read-refused). |

Если ни одна строка не объясняет ситуацию с ключом, проверьте моды, выполняющиеся раньше вашего, на наличие хука `settings.read`, который [изменяет этот ключ](https://code.claude.com/docs/ru/plugins/mods/events.md#settings-read-example). Отключите такой мод или попросите об этом администратора вашей организации. Если такого хука нет, задайте ключ в файле настроек.

### `the answer for <key> is no value the key can hold`

Эта строка [лога отладки](#read-the-debug-log) означает, что Claude Code отклонил значение, которое хук [`settings.read`](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-hook) вернул для указанного ключа, и только для этого ключа:

```text theme={null}
settings.read: the answer for <key> is no value the key can hold; the settings' own value stands
```

Значение, возвращённое для указанного ключа, не соответствует схеме этого ключа, например по типу или по диапазону.

* **Ваше значение не соответствует схеме ключа**: верните значение, допустимое согласно записи этого ключа в [справочнике настроек](https://code.claude.com/docs/ru/settings-reference.md).
* **Ваше значение подходит**: неподходящее значение пришло из хука `settings.read` другого мода. Чтобы найти этот мод, выполните [шаги по поочерёдному отключению модов](#settings-read-refused). Ищите в каждом новом логе эту строку вместо `refused to the engine`.

Пока значение не подходит, ключ сохраняет значение, объединённое из источников настроек до ответа какого-либо хука. В строке оно называется собственным значением настроек.

### `settings.read: refused to the engine`

Эта строка появляется в [логе отладки](#read-the-debug-log), когда в [собственном чтении Claude Code](https://code.claude.com/docs/ru/plugins/mods/events.md#settings-read-hook) отказано, и Claude Code отбрасывает значения всех хуков. Когда хук `settings.read` отказывает в этом чтении с помощью [`{ deny: reason }`](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-returns), строка содержит причину, указанную этим хуком:

```text theme={null}
settings.read: refused to the engine (engine: $.settings.read: <reason>); the settings' own values stand
```

Найдите в своём коде причину, указанную в скобках:

* **Текст есть в вашем коде**: в чтении отказал ваш хук. Сделайте так, чтобы он возвращал `{ value }`, когда [`next.origin`](https://code.claude.com/docs/ru/plugins/mods/events#settings-read-origin) указывает на собственное чтение Claude Code.
* **Её нет в вашем коде**: [отключайте](https://code.claude.com/docs/ru/plugins/mods/overview.md#turn-mods-on-or-off) другие свои моды по одному. Если мод развернула ваша организация, попросите её администратора отключить его. После каждого отключения:
  1. Запустите сессию из оболочки командой `claude --debug-file ./settings-read-2.log`, добавив флаги, с которыми она была запущена. Каждый раз используйте новый путь.
  2. Найдите в этом файле `refused to the engine`. Если строка есть, отключите следующий мод. Если нет — в чтении отказал последний отключённый вами мод, поэтому оставьте его отключённым.

Если строка остаётся, а других модов не осталось, задайте ключи, которые возвращает ваш хук, в [файле настроек](https://code.claude.com/docs/ru/settings.md). Его значения действуют, пока в чтении отказано.

## Прочитайте лог отладки

В логе отладки есть строка для каждого модуля, который Claude Code загружает или отклоняет, для каждого хука, завершившегося сбоем, и для каждого отклонённого результата, поэтому именно туда стоит смотреть, когда транскрипт ничего не показывает. Чтобы записать лог, запустите Claude Code в оболочке с `--debug` или с `--debug-file <path>`, чтобы выбрать место назначения:

```bash theme={null}
claude --debug-file ./mod-debug.log --plugin-dir ./first-mod
```

В другом терминале следите за файлом и фильтруйте по имени вашего мода:

```bash theme={null}
tail -f ./mod-debug.log | grep first-mod
```

Для загруженного мода есть строка, в которой указано его имя и перечислены события, которые он обрабатывает. Мод, загруженный с `--plugin-dir`, отображается под своим именем, за которым следует `@inline`:

```text theme={null}
hooks module first-mod@inline loaded (worker, environment 2, tier user); events: session.start,tool.call,command.run,ui.render
```

Чтобы записать собственные строки в лог, вызовите [`$.ui.log`](https://code.claude.com/docs/ru/plugins/mods/api#show-something-without-starting-a-turn) со вторым аргументом, как в `$.ui.log('message', { to: 'debug' })`. Без второго аргумента `$.ui.log` добавляет тусклую строку в транскрипт.

## Следующие шаги

* [Протестируйте мод](https://code.claude.com/docs/ru/plugins/mods/test.md): ловите проблемы до того, как они достигнут сеанса
* [Устранение неполадок плагинов](https://code.claude.com/docs/ru/plugins/troubleshooting.md): проблемы с установкой и загрузкой плагина, которые не специфичны для модов
