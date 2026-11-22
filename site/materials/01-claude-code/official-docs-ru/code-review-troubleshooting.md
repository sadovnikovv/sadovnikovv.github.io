> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Устранение неполадок Code Review

> Исправьте ситуации, когда Code Review не запустился, завершился с ошибкой или был пропущен из-за бюджета, найдите недостающие замечания и решите проблемы с настройкой и `REVIEW.md`.

Если [Code Review](https://code.claude.com/docs/ru/code-review.md) ведёт себя на pull request не так, как вы ожидаете, начните с check run **Claude Code Review**. Его заголовок показывает, на каком этапе остановилось ревью.

## Проверьте, на каком этапе остановилось ревью

Найдите check run **Claude Code Review** в вашем pull request, затем сопоставьте его заголовок с одним из распространённых вариантов:

| Заголовок check run | Что это означает | Что делать |
| :- | :- | :- |
| **Code review queued...** или **Code review in progress...** | Ревью ещё не завершилось | Дождитесь изменения заголовка |
| **Code review found no issues** | Ревью завершилось и не опубликовало замечаний | Если это не первое ревью этого pull request, найдите в тексте ревью количество [замечаний, которые ревью не включило](https://code.claude.com/docs/ru/code-review-pull-requests.md#what-a-later-review-covers). В остальных случаях — ничего |
| Заголовок, сообщающий, что найдены проблемы | Ревью завершилось с замечаниями | Если вы не видите их в diff, см. [Поиск проблем, которые не отображаются как встроенные комментарии](#find-issues-that-aren’t-showing-as-inline-comments) |
| **Code review skipped — no new changes** | Автоматическое ревью не запустилось для вашего последнего push | Чтобы всё равно получить ревью, оставьте комментарий `@claude review` |
| **Code review not repeated — earlier findings still open** | Автоматическое ревью не запустилось для вашего последнего push, а важные замечания из предыдущего ревью всё ещё открыты | Отправьте исправление через push или, чтобы всё равно получить ревью, оставьте комментарий `@claude review`. См. [Когда push сохраняет предыдущий результат](https://code.claude.com/docs/ru/code-review-pull-requests.md#when-a-push-keeps-the-earlier-result) |
| **Code review failed** или **Code review timed out** | Ревью не завершилось | Чтобы запустить его снова, см. [Повторный запуск ревью, завершившегося с ошибкой или по тайм-ауту](#retrigger-a-failed-or-timed-out-review) |
| **Code review declined** | Ревью не запускалось | Прочитайте сводку check run. Если в ней упоминается бюджет или лимит расходов, см. [Ревью не запустилось, и в PR отображается сообщение о бюджете](#review-didn’t-run-and-the-pr-shows-a-budget-message) |
| Check run отсутствует | Ревью не запускалось | Оставьте комментарий `@claude review`. Если после этого check run не появился, см. [Команда в комментарии не запустила ревью](#a-comment-command-didn’t-start-a-review) |

## Ревью не запустилось

Проверьте эти случаи, если check run **Claude Code Review** не появляется или если Claude публикует комментарий о том, что ревью было пропущено.

### Команда в комментарии не запустила ревью

После того как вы оставили комментарий `@claude review`, найдите в pull request check run **Claude Code Review** с заголовком **Code review queued...** или **Code review in progress...**. Реакция 👀 на ваш комментарий не подтверждает, что ревью будет выполнено. Если check run не появился, проверьте каждую из следующих причин:

* **Code Review не включён для этого репозитория**: Claude не публикует ни комментария, ни check run в ответ на команду. Попросите Owner [добавить репозиторий](https://code.claude.com/docs/ru/code-review-setup.md#add-more-repositories).
* **Комментарий не соответствует условию**: это был встроенный комментарий или текст ревью, а не новый комментарий верхнего уровня, либо команда стояла не в начале комментария. Редактирование более раннего комментария вместо публикации нового также не учитывается, а pull request должен быть открыт. Ознакомьтесь с [условиями для команд в комментариях](https://code.claude.com/docs/ru/code-review-pull-requests.md#comment-commands) и опубликуйте новый комментарий, который им соответствует.
* **У вас нет прав на запись**: вам нужно разрешение write, maintain или admin в репозитории. Для pull request из форка учитывается разрешение в базовом репозитории. Если pull request не ваш, Claude может ответить [подсказкой](https://code.claude.com/docs/ru/code-review-setup.md#turn-tip-comments-on-or-off): "No review was started: manual reviews can only be requested by someone with write access to this repository." Попросите оставить комментарий кого-то, у кого есть права на запись.
* **Бюджет исчерпан**: Claude публикует комментарий, начинающийся с "⚠️ Code review skipped". См. [Ревью не запустилось, и в PR отображается сообщение о бюджете](#review-didn’t-run-and-the-pr-shows-a-budget-message).

### Ревью не запустилось, и в PR отображается сообщение о бюджете

Когда бюджета вашей организации недостаточно для ревью, Code Review пропускает его, а Claude публикует в pull request комментарий, начинающийся с "⚠️ Code review skipped". В некоторых из этих случаев также появляется check run с заголовком **Code review declined**.

Комментарий содержит ссылку на [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage), где администратор может восстановить бюджет. По формулировке можно понять, какой лимит был достигнут:

* **"has reached its monthly code review spending cap"**: достигнут [ежемесячный лимит расходов на Code Review](https://code.claude.com/docs/ru/code-review-costs.md#limit-your-spend). Ревью возобновятся в начале следующего расчётного периода. Чтобы получить их раньше, попросите администратора повысить лимит.
* **"has no extra usage available to pay for this review"**: баланс [кредитов использования](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) вашей организации исчерпан или достигнут её общий ежемесячный лимит расходов. Попросите администратора пополнить кредиты или повысить этот лимит.
* **"is too low to start another review"**: остаток бюджета или баланса меньше ожидаемой стоимости одного ревью. Попросите администратора повысить лимит или пополнить кредиты.

После восстановления бюджета оставьте в pull request комментарий `@claude review`, чтобы получить пропущенное ревью. Действуют [условия для команд в комментариях](https://code.claude.com/docs/ru/code-review-pull-requests.md#comment-commands), поэтому у автора комментария должны быть права на запись.

## Повторный запуск ревью, завершившегося с ошибкой или по тайм-ауту

Если в сводке check run указано "The review session was interrupted before it could finish. A new review of this commit has been queued automatically.", ничего делать не нужно. Такое ревью автоматически повторяется один раз.

В остальных случаях, когда заголовок check run — **Code review failed** или **Code review timed out**, запустите ревью снова с помощью комментария или повторного запуска:

* **Оставьте комментарий `@claude review`**: опубликуйте его как комментарий верхнего уровня в pull request. Это запускает новое ревью без подписки pull request на будущие push.
* **Нажмите Re-run**: если pull request не [из форка](https://code.claude.com/docs/ru/code-review-pull-requests.md#review-drafts-and-pull-requests-from-forks), нажмите **Re-run** у проверки **Claude Code Review** на вкладке **Checks** в GitHub. Повторный запуск охватывает текущий головной коммит pull request и также не подписывает pull request.

## Поиск проблем, которые не отображаются как встроенные комментарии

Если заголовок check run сообщает, что найдены проблемы, но вы не видите встроенных комментариев ревью в diff, посмотрите в других местах, где отображаются замечания:

* **Details в check run**: нажмите **Details** рядом с проверкой **Claude Code Review** на вкладке **Checks**. Таблица серьёзности содержит замечания с файлом, строкой и кратким описанием независимо от того, был ли принят встроенный комментарий.
* **Аннотации в Files changed**: откройте вкладку **Files changed** в PR. Замечание, привязанное к строке, но не опубликованное как встроенный комментарий, отображается там как аннотация к соответствующим строкам.
* **Текст ревью**: замечания без привязки к месту в коде или выходящие за пределы текущего diff отображаются под заголовком **Additional findings** в тексте ревью.

## Check run упоминает REVIEW\.md

Вот четыре сообщения, которые check run может содержать о `REVIEW.md`:

* **"This review applied the repository's review instructions (REVIEW\.md) from its default branch, which is not protected against direct pushes."**: ревью прочитало только корневой файл. О том, что меняет защита ветки, см. [Из какой ветки читается REVIEW.md](https://code.claude.com/docs/ru/code-review-customize.md#which-branch-review-md-is-read-from).
* **"were not applied to this review: branch protection could not be confirmed"**: ревью не прочитало ни одного `REVIEW.md`.
* **"they link to a file this pull request modifies, or carry more links than the review checks"**: ревью пропустило корневой `REVIEW.md` или указанное в сообщении количество файлов `REVIEW.md` в подкаталогах. Проверьте пропущенный файл на каждую из причин. Для корневого `REVIEW.md` также проверьте [файлы, которые он включает](https://code.claude.com/docs/ru/code-review-customize.md#include-other-files-in-review-md):
  * **Слишком много ссылок**: файл содержит более 64 ссылок Markdown. Сократите число ссылок до [64 или меньше](https://code.claude.com/docs/ru/code-review-customize.md#include-other-files-in-review-md).
  * **Ссылка, которую ревью не может разобрать**: файл содержит некорректную ссылку Markdown. Исправьте или удалите эту ссылку.
  * **Ссылка на изменённый файл**: файл ссылается на файл или папку, которые изменяет этот pull request, и ревью не смогло исключить только строки с этой ссылкой. Запишите правило непосредственно в `REVIEW.md`.
* **"include line(s) in the root REVIEW\.md were skipped on this review"**: ваш корневой `REVIEW.md` был применён, но файлы, указанные в этих строках, — нет. Проверьте списки в разделе [Включение других файлов в REVIEW.md](https://code.claude.com/docs/ru/code-review-customize.md#include-other-files-in-review-md), а для скилла — в разделе [Включение файла скилла](https://code.claude.com/docs/ru/code-review-customize.md#include-a-skill-file).

## Проблемы с настройкой

Эти случаи возникают у Owner при [настройке Code Review](https://code.claude.com/docs/ru/code-review-setup.md).

### Репозиторий не отображается в Add a repository

Сначала найдите репозиторий по имени, поскольку диалог не загружает длинный список полностью. Диалог показывает репозиторий, только если у Claude GitHub App есть к нему доступ. Нажмите **Install GitHub App** и предоставьте приложению доступ к репозиторию. Если ни один репозиторий не отображается, **Install GitHub App** — это кнопка в диалоге. В противном случае она находится внизу меню фильтра организаций GitHub в диалоге.

### В тестовом pull request не появляется check run

Убедитесь, что **Allow code review** включён, что репозиторий указан в списке **Repositories** в разделе **Code review** и что у Claude GitHub App есть к нему доступ. Автоматические ревью пропускают черновые pull request, а для репозитория с режимом **Manual (@claude review)** для запуска первого ревью нужен комментарий `@claude review`.

## Связанные ресурсы

* [Просмотр и запрос ревью в pull request](https://code.claude.com/docs/ru/code-review-pull-requests.md): что означают замечания и check run, а также команды в комментариях
* [Настройка Code Review](https://code.claude.com/docs/ru/code-review-setup.md): для Owner — включение Code Review и управление репозиториями
* [Стоимость и использование Code Review](https://code.claude.com/docs/ru/code-review-costs.md): лимиты расходов, стоящие за сообщением о бюджете
* [Кастомизация Code Review](https://code.claude.com/docs/ru/code-review-customize.md): какую копию `REVIEW.md` читает ревью
