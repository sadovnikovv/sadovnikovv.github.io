> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Находите ошибки в pull request на GitHub с помощью Code Review: Claude проводит ревью каждого изменения, проверяет свои результаты и оставляет встроенные комментарии. Для планов Team и Enterprise

С Code Review Claude проводит ревью pull request в ваших репозиториях GitHub. Несколько агентов читают каждое изменение вместе с окружающим кодом и ищут такие проблемы, как логические ошибки, уязвимости безопасности или нарушенные граничные случаи. Прежде чем о результатах будет сообщено, этап верификации сверяет их с кодом.

Результаты поступают в виде встроенных комментариев на соответствующих строках, ранжированные по [степени серьёзности](https://code.claude.com/docs/ru/code-review-pull-requests.md#severity-levels), вместе со сводкой и check run на pull request. Ревью никогда не одобряет и не блокирует pull request, поэтому решение о слиянии остаётся за вашей командой.

![Схема ревью в четыре этапа. Pull request на GitHub передаётся нескольким агентам, которые параллельно ведут поиск на инфраструктуре Anthropic. Этап верификации отбрасывает ложные срабатывания, оставшиеся результаты дедуплицируются и ранжируются по степени серьёзности, а ревью публикует встроенные комментарии, сводку и check run обратно на GitHub.](https://mintcdn.com/claude-code/gLJVaPQEgKC8ZyUD/images/code-review-pipeline.svg?fit=max\&auto=format\&n=gLJVaPQEgKC8ZyUD\&q=85\&s=0351c96df9efa3105172eb00a672f130)

> [!NOTE]
>
> Code Review использует ИИ для ревью кода и может пропустить ошибки, уязвимости безопасности или другие проблемы. Ревью без результатов не означает, что ваш код не содержит ошибок или безопасен.

Чтобы включить Code Review, пользователь с ролью Owner в вашей организации Claude выполняет инструкции из раздела [Настройка Code Review](https://code.claude.com/docs/ru/code-review-setup.md). Claude также может проводить ревью кода без этого сервиса. Запустите [`/code-review`](https://code.claude.com/docs/ru/code-review-local) в своей сессии Claude Code на любом плане или [сравните все варианты](#compare-ways-to-get-a-review).

## Доступность

Прежде чем настраивать Code Review, убедитесь, что ваша организация соответствует требованиям:

* **Планы**: [Team и Enterprise](https://code.claude.com/docs/ru/feature-availability.md)
* **Хостинги кода**: репозитории, размещённые на GitHub, включая [GitHub Enterprise Server](https://code.claude.com/docs/ru/github-enterprise-server.md) и GitHub Enterprise Cloud с резидентностью данных. Для резидентности данных попросите пользователя с ролью Owner выполнить [настройку администратора GitHub Enterprise Server](https://code.claude.com/docs/ru/github-enterprise-server.md#admin-setup) и указать имя хоста `ghe.com` вашего предприятия.
* **Хранение данных**: Code Review недоступен для организаций с включённым [Zero Data Retention](https://code.claude.com/docs/ru/zero-data-retention.md) или с применённой [конфигурацией HIPAA](https://code.claude.com/docs/ru/hipaa-setup.md), и на него не распространяется Business Associate Agreement (BAA) Anthropic.
* **Ключи шифрования**: Code Review пока недоступен для организаций, использующих ключи шифрования, управляемые клиентом (CMEK).
* **Облачные провайдеры**: вам нужна организация Claude на одном из этих планов, даже если ваши разработчики используют Claude Code через Amazon Bedrock, Google Cloud's Agent Platform или Microsoft Foundry

## Настройка и использование Code Review

Выберите страницу в зависимости от того, что вам нужно сделать:

> [card] [Настройка Code Review](https://code.claude.com/docs/ru/code-review-setup.md)
>
> Проверьте требования, установите Claude GitHub App и выберите репозитории, уровень ревью и момент запуска ревью

> [card] [Кастомизация Code Review](https://code.claude.com/docs/ru/code-review-customize.md)
>
> Настройте, что помечается, с помощью файлов `REVIEW.md` и `CLAUDE.md` в вашем репозитории

> [card] [Чтение и запрос ревью на pull request](https://code.claude.com/docs/ru/code-review-pull-requests.md)
>
> Читайте результаты и их степени серьёзности и запрашивайте повторное ревью с помощью комментария

> [card] [Устранение неполадок Code Review](https://code.claude.com/docs/ru/code-review-troubleshooting.md)
>
> Исправьте ревью, которое не запустилось, завершилось сбоем или было пропущено из-за бюджета

> [card] [Стоимость и использование Code Review](https://code.claude.com/docs/ru/code-review-costs.md)
>
> Узнайте, как тарифицируются ревью, оцените расходы, установите ежемесячный лимит расходов и отслеживайте активность ревью

## Как работают ревью

По умолчанию Code Review сосредоточен на корректности: ошибках, которые нарушат работу production, а не на предпочтениях форматирования или отсутствии покрытия тестами. Чтобы изменить то, что он помечает, [добавьте файлы с руководствами](https://code.claude.com/docs/ru/code-review-customize.md) в ваш репозиторий.

Ревью выполняется на инфраструктуре Anthropic в четыре этапа:

1. **Поиск**: несколько агентов параллельно изучают diff и окружающий код.
2. **Верификация**: этап верификации сверяет кандидатов в результаты с кодом и отфильтровывает ложные срабатывания.
3. **Ранжирование**: оставшиеся результаты дедуплицируются и ранжируются по степени серьёзности.
4. **Публикация**: ревью публикует свои результаты на pull request.

Каждое ревью оставляет на pull request следующее:

* **Результаты**: встроенные комментарии на соответствующих строках со сводкой в теле ревью
* **Check run**: с именем **Claude Code Review**, с результатами, перечисленными в его [подробностях](https://code.claude.com/docs/ru/code-review-pull-requests.md#check-run-output). Check run не завершается со статусом сбоя.
* **Заметка вместо результатов**: публикуется, когда заголовок check run гласит **Code review found no issues**

Code Review сам выбирает модели Claude, на которых выполняются ревью, и его настройки администратора не предлагают выбора модели. Чтобы сделать ревью более или менее тщательными, измените [уровень ревью](#review-levels).

После того как пользователь с ролью Owner включит Code Review, у каждого репозитория появляется настройка [момента запуска ревью](https://code.claude.com/docs/ru/code-review-setup.md#set-when-reviews-run): один раз при открытии pull request, после каждого push или только по запросу. Независимо от выбранного варианта, любой пользователь с доступом на запись к репозиторию может оставить комментарий `@claude review` на pull request, чтобы [запустить ревью](https://code.claude.com/docs/ru/code-review-pull-requests.md#comment-commands).

### Уровни ревью

Уровень ревью определяет, насколько тщательным будет каждое ревью, и более тщательное ревью стоит дороже:

* **Quick**: более лёгкий проход. Самый быстрый уровень с наименьшей стоимостью.
* **Standard**: сбалансированные глубина, скорость и стоимость. Уровень по умолчанию.
* **Deep**: самый тщательный проход. Занимает больше всего времени и стоит дороже всего.

Пользователь с ролью Owner [выбирает один уровень для организации](https://code.claude.com/docs/ru/code-review-setup.md#set-the-default-review-level) и может задать отдельному репозиторию собственный уровень, например Quick для рутинной кодовой базы и Deep для критически важной. О том, что ещё влияет на стоимость каждого ревью, см. [Стоимость и использование Code Review](https://code.claude.com/docs/ru/code-review-costs.md).

### К чему у ревью есть доступ

Ревью получает доступ к вашему репозиторию через Claude GitHub App, которое пользователь с ролью Owner [устанавливает во время настройки](https://code.claude.com/docs/ru/code-review-setup.md#turn-on-code-review):

* **Где оно выполняется**: на инфраструктуре Anthropic, в управляемом окружении. Ревью не выполняются в [self-hosted окружениях](https://code.claude.com/docs/ru/self-hosted-environments).
* **Что оно читает и записывает**: внутри ревью доступ к вашему репозиторию только для чтения, и ревью не отправляет коммиты. На pull request оно публикует комментарии и [check run](https://code.claude.com/docs/ru/code-review-pull-requests.md#check-run-output), разрешает собственные более ранние ветки комментариев и может отреагировать на команду в комментарии с помощью 👀. Само приложение обладает [более широким набором разрешений](https://code.claude.com/docs/ru/github-actions.md#github-app-permissions), который используется и другими функциями Claude.
* **Как оно изучает ваш код**: ревью работает, читая diff и окружающий код, без сборки или запуска вашего кода.

### Кто управляет ревью

* **Кто может его запустить**: там, где ревью запускаются автоматически, открытие pull request или push в него запускает ревью, [кроме черновиков и форков](https://code.claude.com/docs/ru/code-review-pull-requests.md#review-drafts-and-pull-requests-from-forks). После некоторых push Code Review вместо этого [сохраняет предыдущий результат](https://code.claude.com/docs/ru/code-review-pull-requests.md#when-a-push-keeps-the-earlier-result). [Команда в комментарии](https://code.claude.com/docs/ru/code-review-pull-requests.md#comment-commands) запускает ревью, только если она исходит от человека с доступом на запись к репозиторию.
* **Каким инструкциям оно следует**: `REVIEW.md` из базовой ветки или ветки по умолчанию и [никогда не из изменений самого pull request](https://code.claude.com/docs/ru/code-review-customize.md#which-branch-review-md-is-read-from).

## Сравнение способов получить ревью

Чтобы найти доступные вам варианты, сопоставьте столбец **Кто может использовать** с вашим планом и хостингом кода:

| Вариант | Что запускает ревью | Где выполняется | Кто может использовать |
| :- | :- | :- | :- |
| [Code Review](#how-reviews-work) | Активность в pull request в соответствии с настройками каждого репозитория или комментарий `@claude review` | Инфраструктура Anthropic | Организации на плане Team или Enterprise с репозиториями GitHub, после того как пользователь с ролью Owner его включит |
| [`/code-review`](https://code.claude.com/docs/ru/code-review-local) | Вы запускаете команду на своей ветке | Ваша сессия Claude Code | Кто угодно, на любом плане |
| [Ultrareview](https://code.claude.com/docs/ru/ultrareview.md) | Вы запускаете его из Claude Code | Облачная песочница | Требуется вход с аккаунтом claude.ai. О том, где он недоступен, см. [Ultrareview](https://code.claude.com/docs/ru/ultrareview.md) |
| Claude в вашем собственном CI, с [GitHub Actions](https://code.claude.com/docs/ru/github-actions.md) или [GitLab CI/CD](https://code.claude.com/docs/ru/gitlab-ci-cd.md) | События вашего конвейера, например каждый pull request или merge request | Ваши собственные раннеры CI | Любой, у кого есть API-ключ Claude или учётные данные облачного провайдера, на GitHub или GitLab |
| Ваш собственный ревьюер в виде [субагента](https://code.claude.com/docs/ru/sub-agents.md) или [скилла](https://code.claude.com/docs/ru/skills.md) | Вы или Claude вызываете его во время сессии | Там, где вы запускаете Claude Code | Любой, кто его напишет |

## Связанные ресурсы

* [GitHub Enterprise Server](https://code.claude.com/docs/ru/github-enterprise-server.md): используйте Code Review с self-hosted экземпляром GitHub
* [Разрешения GitHub App](https://code.claude.com/docs/ru/github-actions.md#github-app-permissions): полный набор разрешений, который запрашивает Claude GitHub App
* [How Anthropic secures its AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle): как автоматизированная проверка встраивается в качестве одного из уровней безопасного процесса разработки Anthropic
