> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройка режима auto

> Сообщите классификатору режима auto, каким репозиториям, бакетам и доменам доверяет ваша организация, задайте собственные правила блокировки и разрешения и проверьте свою конфигурацию.

[Режим auto](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) позволяет Claude Code работать без обычных запросов разрешений, маршрутизируя вызовы инструментов через классификатор, который блокирует все необратимое, деструктивное или направленное вне вашего окружения. Правила отказа и явного запроса оцениваются перед классификатором и по-прежнему блокируют или запрашивают. Используйте блок настроек `autoMode`, чтобы сообщить этому классификатору, какие репозитории, бакеты и домены доверяет ваша организация, чтобы он перестал блокировать обычные внутренние операции.

> [!NOTE]
>
> Эта страница является справочником по конфигурации. Включение и отключение режима auto рассматривается на странице Permission modes:
>
> * **Переключение на режим auto во время сеанса или выход из него**: см. [Переключение режимов разрешений](https://code.claude.com/docs/ru/permission-modes.md#switch-permission-modes)
> * **Запуск сеанса в режиме auto**: см. [Запуск в другом режиме разрешений](https://code.claude.com/docs/ru/permission-modes.md#start-in-a-different-mode)

Режим auto доступен всем пользователям на каждом поставщике, включая Anthropic API, [Claude Platform on AWS](https://code.claude.com/docs/ru/claude-platform-on-aws.md), Amazon Bedrock, Agent Platform Google Cloud, Microsoft Foundry и сеансы [шлюза приложений Claude](https://code.claude.com/docs/ru/claude-apps-gateway). Если Claude Code сообщает, что режим auto недоступен для вашей учетной записи, проверьте [полные требования](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode), которые также охватывают поддерживаемые модели и управление на уровне организации на планах Team и Enterprise.

По умолчанию классификатор доверяет только рабочему каталогу и настроенным удаленным репозиториям текущего репозитория. Действия, такие как отправка в исходный контроль вашей компании или запись в командный облачный бакет, блокируются до тех пор, пока вы не добавите их в `autoMode.environment`.

На этой странице рассматривается, как:

* [Добавить контрольную точку человека](#add-a-human-checkpoint) для отправок и запросов на слияние с помощью `permissions.ask`
* [Определить доверенную инфраструктуру](#define-trusted-infrastructure) с помощью `autoMode.environment`
* [Создать записи окружения](#generate-environment-entries) с помощью `/auto-mode-setup`
* [Просмотреть отказы](#review-denials) чтобы знать, что добавить дальше

## Общие границы

По умолчанию в авторежиме Claude может без запроса подтверждения отправлять изменения (push) в репозиторий, в котором вы работаете, включая его ветку по умолчанию. Он также может создавать там pull request, когда этого требует ваша задача. Некоторые push и pull request [блокируются](https://code.claude.com/docs/ru/permission-modes.md#what-the-classifier-blocks-by-default), например push с секретом или pull request в другой репозиторий.

Если вы хотите контрольную точку человека перед командами push и pull request от Claude, добавьте правила разрешений: [рецепты ниже](#add-a-human-checkpoint) сохраняют автоматический режим включённым для всего остального.

### Добавить контрольную точку человека

Наиболее прямой механизм — это [`permissions.ask`](https://code.claude.com/docs/ru/permissions#permission-rule-syntax). Приведённые ниже правила ask оцениваются перед классификатором, поэтому по умолчанию вы увидите запрос разрешения. Добавьте правила в ваши [настройки](https://code.claude.com/docs/ru/settings.md#where-settings-live):

```json theme={null}
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(gh pr create *)"
    ]
  }
}
```

Эти правила соответствуют командам, которые начинаются с `git push` или `gh pr create`. Push, который Claude пишет другим способом, например `git -C <dir> push` или `git -c <key>=<value> push`, [не соответствует правилу](https://code.claude.com/docs/ru/permissions.md#bash-rule-limits), поэтому он не проверяется. Для контрольной точки, которая проверяет полный текст команды, добавьте [hook PreToolUse](https://code.claude.com/docs/ru/hooks.md#pretooluse).

Выберите механизм, который соответствует тому, насколько строгой должна быть граница:

| Граница | Механизм | Поведение в автоматическом режиме |
| :- | :- | :- |
| Запрос перед действием | `permissions.ask` | По умолчанию запрашивает подтверждение для команды, которая соответствует правилу с областью действия контента, подобному рецепту выше. Классификатор не может автоматически одобрить соответствующее действие. |
| Никогда не запускать действие | `permissions.deny` | Блокирует перед консультацией классификатора. Ни классификатор, ни намерение пользователя не могут переопределить это. |
| Одноразовая граница для этого сеанса | Укажите это в разговоре, например "не отправляй, пока я не проверю" | Классификатор блокирует соответствующие действия, но граница может быть потеряна, если [компактирование контекста](https://code.claude.com/docs/ru/costs.md#reduce-token-usage) удалит сообщение, в котором она была указана. Используйте правило ask или deny для гарантии долговечности. |

## Где классификатор читает конфигурацию

Классификатор читает то же содержимое [CLAUDE.md](https://code.claude.com/docs/ru/memory.md), которое загружает сам Claude, поэтому инструкция вроде "никогда не делайте force push" в файле CLAUDE.md вашего проекта управляет как Claude, так и классификатором одновременно. Начните с этого файла для соглашений проекта и правил поведения.

Для правил, которые применяются ко всем проектам, таких как доверенная инфраструктура или организационные правила запрета, используйте блок настроек `autoMode`. Классификатор читает `autoMode` из следующих областей:

| Область | Файл | Используется для |
| :- | :- | :- |
| Один разработчик | `~/.claude/settings.json` | Личная доверенная инфраструктура |
| Организация | [Управляемые настройки](https://code.claude.com/docs/ru/server-managed-settings.md) | Доверенная инфраструктура, распределённая всем разработчикам |
| Флаг `--settings` или Agent SDK | Встроенный JSON | Переопределения для каждого вызова для автоматизации |

Классификатор не читает `autoMode` из настроек проекта в `.claude/settings.json` или `.claude/settings.local.json`. Оба файла находятся в директории репозитория, поэтому проверенный репозиторий или шаг сборки могли бы иначе внедрить свои собственные правила разрешения. Переместите любой блок `autoMode` из `.claude/settings.local.json` в `~/.claude/settings.json`.

Записи из каждой области объединяются. Разработчик может расширить `environment`, `allow`, `soft_deny` и `hard_deny` личными записями, но не может удалить записи, которые предоставляют управляемые настройки. Поскольку правила разрешения действуют как исключения из правил мягкой блокировки внутри классификатора, запись `allow`, добавленная разработчиком, может переопределить запись организационного `soft_deny`: комбинация является аддитивной, а не жёсткой границей политики.

> [!NOTE]
>
> Классификатор — это вторая проверка, которая выполняется после [системы разрешений](https://code.claude.com/docs/ru/permissions.md). Для действий, которые никогда не должны выполняться независимо от намерения пользователя или конфигурации классификатора, используйте `permissions.deny` в управляемых настройках, что блокирует действие до того, как классификатор будет проверен, и не может быть переопределено.

## Определение доверенной инфраструктуры

Для большинства организаций `autoMode.environment` — это единственное поле, которое вам нужно установить. Оно сообщает классификатору, какие репозитории, бакеты и домены являются доверенными: классификатор использует это для определения того, что означает "внешний", поэтому любой пункт назначения, не указанный в списке, является потенциальной целью утечки данных.

`claude auto-mode defaults` выводит три вида записей окружения.

* **Context slots**: описывают вашу организацию, стек и позицию безопасности, чтобы классификатор читал другие правила в вашем контексте. Каждый по умолчанию имеет значение `None configured` или консервативное предположение, указанное рядом:
  * **Organization**
  * **Primary use of Claude Code**: по умолчанию разработка программного обеспечения
  * **Cloud provider(s)**
  * **Repository visibility**: репозиторий считается приватным, если только его удаленный хост и имя не указывают иное, или классификатор читает проверку видимости ранее в разговоре, показывающую, что он публичный.

    В запросах классификатора, отправляемых самим Claude Code, классификатор читает ваши сообщения и команды, которые выполняет Claude, но не их вывод. Доказательство должно быть чем-то, что классификатор может прочитать, например вашим собственным сообщением, в котором репозиторий назван публичным; вывод `gh repo view` сам по себе не достигает его.
  * **Internal sharing / snippet hosting**: публичные сервисы вставок и gist рассматриваются как находящиеся вне границы доверия, пока вы не назовёте один из них
  * **Org-specific CLIs**
  * **Secrets management**
  * **CI/CD deploy targets**
  * **Network posture**
  * **Host containment**: по умолчанию обычная машина разработчика или CI runner с открытым интернетом. Если Claude Code работает в контейнере, виртуальной машине или поде с allow-list исходящих соединений или соседями, которых он не должен трогать, назовите разрешённые хосты, должен ли быть доступен эндпоинт метаданных облака и какой облачный проект, кластер или реестр использует задача и под какой идентичностью. Пока эта запись не назовёт эту идентичность, классификатор [блокирует](https://code.claude.com/docs/ru/permission-modes.md#what-the-classifier-blocks-by-default) запросы на учётные данные самого хоста. Требует Claude Code v2.1.257 или позже
  * **Protected deployment namespaces / environments**: использует значение по умолчанию для Sensitive remote targets, пока вы их не назовёте
  * **Data retention / declassification**
* **Trust slots**: назовите то, что классификатор рассматривает как находящееся внутри вашей границы. Слоты — это Trusted repo, Source control, Trusted internal domains, Trusted cloud buckets, Key internal services и Internal package registry. Записи репозитория и управления исходным кодом по умолчанию указывают на рабочий репозиторий и его настроенные удаленные хосты. Каждый другой слот доверия по умолчанию имеет значение `None configured`, поэтому ничего больше не является доверенным, пока вы это не добавите. Видимость репозитория охватывает только конфиденциальный материал: приватный репозиторий является приемлемым пунктом назначения для конфиденциального материала, но сделание репозитория приватным никогда не очищает секреты или личные или доверенные данные в нем, и классификатор рассматривает содержимое, перенесенное, переориентированное или впервые прочитанное из-за пределов рабочего репозитория, как не собственную работу этого репозитория.
* **Sensitivity slots**: назовите то, что защитные правила рассматривают как высокий риск. Слоты — это Sensitive data locations & audiences, Sensitive remote targets и Protected IaC scopes. По умолчанию хост или пространство имён считается чувствительной удалённой целью, если `prod` или `production` является отдельным словом в его имени. Например, `prod-db` считается таковой, а `webprod01` — нет.

Чтобы добавить свои собственные записи наряду с значениями по умолчанию, включите буквальную строку `"$defaults"` в массив. Записи по умолчанию вставляются в эту позицию, поэтому ваши пользовательские записи могут идти до или после них.

Следующий пример сохраняет записи по умолчанию и добавляет репозитории, бакеты, домены и сервисы организации.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}
```

После сохранения настроек запустите `claude auto-mode config`, чтобы [подтвердить, что правила](#inspect-the-defaults-and-your-effective-config) включают ваши записи.

Записи — это проза, а не regex или шаблоны инструментов. Классификатор читает их как правила на естественном языке. Пишите их так, как вы описали бы вашу инфраструктуру новому инженеру. Тщательный раздел окружения охватывает:

* **Organization**: название вашей компании и для чего в основном используется Claude Code, например разработка программного обеспечения, автоматизация инфраструктуры или инженерия данных
* **Source control**: каждая организация GitHub, GitLab или Bitbucket, в которую разработчики отправляют код
* **Cloud providers and trusted buckets**: имена бакетов или префиксы, из которых Claude должен иметь возможность читать и писать
* **Trusted internal domains**: имена хостов для API, панелей управления и сервисов внутри вашей сети, например `*.internal.example.com`
* **Key internal services**: CI, реестры артефактов, внутренние индексы пакетов, инструменты для работы с инцидентами
* **Internal package registry**: приватный npm, PyPI или другой реестр, через который должны маршрутизироваться установки, поэтому установки, которые обходят его для публичного реестра, блокируются
* **Sensitive data locations & audiences**: бакеты, базы данных или пути, которые содержат личные данные, конфиденциальные бизнес-данные, учетные данные, регулируемые данные или аналогичный чувствительный материал, и аудитории, с которыми данные в каждом месте могут быть общими, поэтому классификатор защищает эти места вместо угадывания из содержимого.
* **Sensitive remote targets**: пространства имён, хосты или контейнеры, которые считаются производством
* **Protected IaC scopes**: ресурсы инфраструктуры, применение или уничтожение которых всегда должно требовать от вас назвать изменение
* **Additional context**: ограничения регулируемой отрасли, многотенантная инфраструктура или требования соответствия, которые влияют на то, что классификатор должен рассматривать как рискованное

Полезный начальный шаблон: заполните поля в скобках и удалите любые строки, которые не применяются.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}
```

Вам не нужно заполнять все сразу. Разумный план развертывания: начните с значений по умолчанию и добавьте организацию управления исходным кодом и ключевые внутренние сервисы, что решает наиболее распространенные ложные срабатывания, такие как отправка в собственные репозитории. Затем добавьте доверенные домены и облачные бакеты. Заполните остальное по мере возникновения блокировок.

## Генерирование записей окружения с помощью `/auto-mode-setup`

Запустите `/auto-mode-setup`, чтобы Claude Code создал черновик записей `autoMode.environment` и иногда также [записей правил](#override-the-block-and-allow-rules) на основе вашего проекта и недавних сеансов в нём. Если вы примете черновик, Claude Code запишет его в `~/.claude/settings.json`.

> [!NOTE]
>
> `/auto-mode-setup` доступна в планах Pro, Max, Ultra, Team и Enterprise, а также с API-ключом Claude Console. В плане Pro, Max, Ultra или Team требуется версия 2.1.228 или новее, а на нативной Windows — версия 2.1.233 или новее. В плане Enterprise или с API-ключом Claude Console требуется версия 2.1.283 или новее. Если команда отсутствует в вашей сессии, см. [`/auto-mode-setup` возвращает "Unknown command"](#auto-mode-setup-returns-unknown-command).

### Что читает `/auto-mode-setup`

Если `~/.claude/settings.json` уже содержит записи `autoMode`, Claude Code начинает с вопроса о том, добавить ли записи в ваш список окружения или заменить его, и в любом случае сохраняет написанные вами правила. Затем Claude Code спрашивает, как вы используете этот проект, и предлагает два необязательных сканирования перед тем, как начать сканирование. При сканировании Claude Code всегда читает эти источники:

* `CLAUDE.md`, `README.md`, файлы конфигурации и git remotes вашего проекта
* Ваши параметры `autoMode` и `permissions.allow`
* Имена хостов, бакетов и команд из команд, которые Claude запустил в ваших недавних сеансах в этом проекте, никогда ваши сообщения

Два необязательных сканирования добавляют по одному источнику каждое:

* Первое слово каждой команды в истории вашей оболочки
* Удалённые хосты и имена репозиториев в вашем домашнем каталоге

### Проверка и сохранение черновика

Claude Code сканирует в фоновом режиме, затем показывает вам черновик. Вы принимаете или отклоняете его целиком, поэтому отредактируйте `~/.claude/settings.json` впоследствии, чтобы отрегулировать отдельные записи. Когда вы принимаете, Claude Code записывает черновик и согласовывает его с параметрами, которые у вас уже есть:

* Если вы решили добавить записи в список `environment` в `~/.claude/settings.json`, любая запись `"$defaults"` в нём сохраняется. Если вы решили заменить этот список, эта запись теряется, поэтому добавьте `"$defaults"` обратно, если вам нужны записи по умолчанию
* Claude Code включает `"$defaults"` в каждый из списков `allow`, `soft_deny` и `hard_deny`, к которым черновик добавляет записи, если вы уже не написали список `allow` без него, поэтому [встроенные правила](#override-the-block-and-allow-rules), которые вы не заменили, остаются в силе
* После сохранения Claude Code предлагает удалить правила `permissions.allow` в `~/.claude/settings.json`, которые автоматический режим игнорирует, такие как `Bash(*)`, или которые автоматически одобряют деструктивные команды

Затем запустите `claude auto-mode config`, чтобы [увидеть результат](#inspect-the-defaults-and-your-effective-config).

### Отключение `/auto-mode-setup`

Когда автоматический режим заблокировал несколько действий и у вас всё ещё нет записей `autoMode.environment`, Claude Code показывает диалоговое окно с названием "Teach auto mode about your environment?" в конце хода и предлагает запустить `/auto-mode-setup` для вас. Чтобы остановить предложение, но сохранить команду, выберите **Don't show again** в этом диалоговом окне.

Чтобы отключить как команду, так и предложение, добавьте эту запись [`skillOverrides`](https://code.claude.com/docs/ru/skills#override-skill-visibility-from-settings) в `~/.claude/settings.json`:

```json theme={null}
{
  "skillOverrides": {
    "auto-mode-setup": "off"
  }
}
```

`/auto-mode-setup` — это встроенная команда, а не [bundled skill](https://code.claude.com/docs/ru/skills.md#bundled-skills), поэтому эта запись `skillOverrides` всё ещё применяется к ней, но [`disableBundledSkills`](https://code.claude.com/docs/ru/settings-reference#disablebundledskills) не отключает её.

### `/auto-mode-setup` возвращает "Unknown command"

Если при вводе `/auto-mode-setup` в промпте Claude Code выводится `Unknown command: /auto-mode-setup`, проверьте следующие причины:

* **Первая сессия после установки или обновления**: начните новую сессию. Если команда отсутствует и там, см. [конфигурации, в которых последующие сессии тоже запускаются без неё](https://code.claude.com/docs/ru/env-vars.md#first-session-after-an-install-or-upgrade).
* **Устаревшая версия**: выполните `claude --version` в вашей оболочке. Если версия ниже [минимальной для вашего плана](#generate-environment-entries), [обновите Claude Code](https://code.claude.com/docs/ru/setup.md#update-claude-code).
* **Телеметрия отключена, сторонний провайдер или шлюз приложений Claude**: до версии 2.1.304 команда недоступна в [сессиях, где получение флагов функций отключено](https://code.claude.com/docs/ru/env-vars.md#features-that-need-feature-flag-fetching). Если ваша сессия относится к ним, [обновите Claude Code](https://code.claude.com/docs/ru/setup.md#update-claude-code) до версии 2.1.304 или новее.

В [облачной сессии](https://code.claude.com/docs/ru/claude-code-on-the-web.md) команда вместо этого выводит `/auto-mode-setup isn't available in this environment.` Запустите её в интерактивной сессии в вашем терминале.

## Переопределить правила блокировки и разрешения

Чтобы дополнить встроенные правила классификатора, задайте любое из трех дополнительных полей и включите в его список буквальную строку `"$defaults"`:

* `autoMode.hard_deny`: действия, которые нужно блокировать, даже когда пользователь сам о них просит
* `autoMode.soft_deny`: деструктивные действия, которые намерение пользователя может отменить
* `autoMode.allow`: исключения из правил мягкой блокировки

Каждое из них — это массив описаний на прозе, читаемых как правила на естественном языке. Для инструментов на основе паттернов с жесткими блокировками, которые работают перед классификатором, используйте [`permissions.deny`](https://code.claude.com/docs/ru/permissions).

> [!NOTE]
>
> В сессии [Code Mode](https://code.claude.com/docs/ru/code-mode.md#permission-checks) классификатор применяет `hard_deny` и `soft_deny` к каждому фрагменту кода целиком, до того как код будет выполнен. Чтобы заблокировать конкретный вызов инструмента, который делает код, используйте правило `permissions.deny`.

Внутри классификатора приоритет работает в четыре уровня:

* Правила `hard_deny` блокируют безусловно. Намерение пользователя и исключения `allow` не применяются.
* Правила `soft_deny` блокируют далее. Намерение пользователя и исключения `allow` могут переопределить эти правила.
* Правила `allow` затем переопределяют совпадающие правила `soft_deny` как исключения.
* Явное намерение пользователя переопределяет оставшиеся мягкие блокировки: если сообщение пользователя прямо и конкретно описывает точное действие, которое Claude собирается выполнить, классификатор разрешает его даже когда совпадает правило `soft_deny`.

Общие запросы не считаются явным намерением. Просьба Claude "очистить репо" не авторизует force-push, но просьба Claude "force-push эту ветку" авторизует.

Чтобы ослабить, добавьте в `allow`, когда классификатор повторно помечает обычный паттерн, который исключения по умолчанию не охватывают. Чтобы усилить, добавьте в `soft_deny` для деструктивных рисков, специфичных для вашего окружения, которые пропускают значения по умолчанию, или в `hard_deny` для действий, которые нужно блокировать, даже когда пользователь сам о них просит.

Следующий пример сохраняет значения по умолчанию во всех четырех списках и добавляет правила, специфичные для организации, в каждый из них.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "$defaults",
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "$defaults",
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Running terraform apply in infra/terraform/prod/ needs an explicit request: production infrastructure changes go through the review workflow"
    ],
    "hard_deny": [
      "$defaults",
      "Never send repository contents to third-party code-review APIs"
    ]
  }
}
```

> [!CAUTION]
>
> Включайте `"$defaults"` в каждый задаваемый вами список, чтобы не потерять ни одного из [встроенных правил](#inspect-the-defaults-and-your-effective-config), которые он содержит.

Каждый раздел оценивается независимо, поэтому установка только `environment` оставляет списки `allow`, `soft_deny` и `hard_deny` по умолчанию нетронутыми.

## Редактирование правил из `/permissions`

Чтобы просмотреть и отредактировать правила классификатора и записи `environment` без открытия файла настроек, запустите [`/permissions`](https://code.claude.com/docs/ru/permissions#manage-permissions) в CLI и выберите вкладку **Auto mode**. Вкладка требует Claude Code версии 2.1.246 или более поздней версии и появляется только когда [авторежим доступен](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode) для вашей сессии.

Claude Code показывает записи из [управляемых параметров](https://code.claude.com/docs/ru/server-managed-settings.md) или флага `--settings` как доступные только для чтения и сохраняет каждое внесённое вами изменение на вкладке в `~/.claude/settings.json`.

> [!NOTE]
>
> В десктопном приложении у `/permissions` нет вкладки **Auto mode**. В локальной сессии, сессии WSL или SSH отредактируйте [блок `autoMode`](#where-the-classifier-reads-configuration) в `~/.claude/settings.json` на машине или в дистрибутиве WSL, где выполняется сессия.

## Приостановка правил разрешения для оболочки

В авторежиме Claude Code отбрасывает [широкие правила разрешения](https://code.claude.com/docs/ru/permission-modes.md#how-the-classifier-evaluates-actions), такие как `Bash(*)`. По умолчанию узкие правила разрешения Bash и PowerShell, такие как `Bash(npm test)`, остаются в силе. Claude Code разрешает их до запуска классификатора, за исключением случаев, когда команда содержит [разрешённые домены для отдельных команд](https://code.claude.com/docs/ru/sandboxing.md#per-command-allowed-domains-in-auto-mode). Узкое правило всё ещё может пропустить деструктивный аргумент без того, чтобы классификатор его увидел, например путь скрипта или флаг, который префикс правила не предусмотрел.

Установите `autoMode.classifyAllShell` в значение `true`, чтобы приостановить ваши правила разрешения Bash и PowerShell, пока активен авторежим, а также в [режиме планирования, когда классификатор проверяет команды](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode). В сессии [Code Mode](https://code.claude.com/docs/ru/code-mode.md#permission-checks) классификатор проверяет код, который запускает команды, даже если эта настройка включена.

```json theme={null}
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

В авторежиме и режиме планирования команды, которые одобрило бы только правило разрешения, выполняются дольше, потому что каждая из них ждёт решения классификатора.

## Проверьте значения по умолчанию и вашу эффективную конфигурацию

Подкоманды `claude auto-mode` помогают вам проверить, валидировать и сбросить вашу конфигурацию.

Выведите правила `environment`, `allow`, `soft_deny` и `hard_deny`, встроенные в Claude Code:

```bash theme={null}
claude auto-mode defaults
```

Чтобы прочитать полный текст одного правила без передачи через `jq`, передайте `--label` с началом метки правила, например `claude auto-mode defaults --label 'Git Destructive'`. Сопоставление выполняется без учёта регистра по префиксу метки каждого правила, а разделы без совпадений выводятся как пустые списки.

> [!NOTE]
>
> Если `/status` в авторежиме показывает [`Auto mode server`](https://code.claude.com/docs/ru/permission-modes#server-side-classifier-review) как `Enabled`, встроенные правила сервера могут отличаться от этого вывода, и ни одна подкоманда `claude auto-mode` их не выводит.

Выведите четыре списка с вашими настройками, применёнными там, где они заданы, и значениями по умолчанию в остальных случаях:

```bash theme={null}
claude auto-mode config
```

Оба `defaults` и `config` выводят четыре списка правил как один объект JSON, с каждым правилом как строка прозы. Это усечённый пример:

```json theme={null}
{
  "allow": [
    ...
    "Test Artifacts: Hardcoded test API keys, placeholder credentials in examples, or hardcoding test cases. Placeholder means authored as a placeholder — a file or value copied from a real secret or sensitive path is never a test artifact (see Sensitive-Source Provenance).",
    ...
  ],
  "soft_deny": [
    "Git Destructive [named+specifics — **must name:** the destructive operation and its target]: Force pushing (`git push --force`), deleting remote branches, tags, or releases, or rewriting remote history. Also `git commit --amend` when the commit being rewritten is not the agent's own unpushed work: either no prior `git commit` is visible (HEAD pre-dates the session), or a `git push` of the current branch is visible after the most recent commit (it has been pushed). Clears when the user asked to amend/reword/fixup, or when it is a message-only reword (`--amend -m …`, nothing newly staged) of a commit the agent visibly created this session.",
    ...
  ],
  "hard_deny": [...],
  "environment": [
    ...
    "**Trusted repo**: The git repository the agent started in (its working directory) and its configured remote(s). When the repo's public/private visibility is given — by the Repository visibility entry or the user's own message — use it to scope what is OK to commit or push there: confidential material is fine in a private repo; in a public one, only that repo's own work is — and content ported, repointed, or first read from outside this session's repo is not its own work, whoever directed the port. Visibility scopes confidential material only: secrets and sensitive data (personal & entrusted) are never cleared into any repo by its visibility (see Definitions).",
    ...
  ]
}
```

Получите отзыв ИИ о ваших пользовательских записях `allow`, `soft_deny`, `hard_deny` и `environment`:

```bash theme={null}
claude auto-mode critique
```

Если вы написали пользовательские правила, `claude auto-mode critique` проверяет их и отмечает записи, которые неоднозначны, избыточны или могут вызвать ложные срабатывания.

Чтобы отменить ваши настройки и вернуться к встроенным значениям по умолчанию, запустите подкоманду reset, которая удаляет раздел `autoMode` из вашего файла пользовательских настроек:

```bash theme={null}
claude auto-mode reset
```

Команда суммирует то, что будет удалено, и спрашивает `Reset auto mode configuration to defaults?` перед записью; передайте `--yes`, чтобы пропустить подтверждение. Reset изменяет только `~/.claude/settings.json`: правила `autoMode` из [управляемых параметров](https://code.claude.com/docs/ru/server-managed-settings.md) или флага `--settings` по-прежнему применяются.

## Проверка отклонённых действий

> [!NOTE]
>
> В десктопном приложении у `/permissions` нет вкладки **Recently blocked**. Чтобы позволить Claude повторить попытку действия, которое вы действительно намеревались выполнить, [назовите это действие и его подробности](https://code.claude.com/docs/ru/permission-modes.md#approvals-you-state-in-conversation) в следующем сообщении.

Чтобы позволить Claude повторить попытку заблокированного действия, используйте вкладку **Recently blocked** в `/permissions`:

**1. Откройте вкладку**

Выполните `/permissions` в своей сессии, чтобы открыть диалоговое окно разрешений, затем выберите вкладку **Recently blocked**.

**2. Проверьте действие**

Выделите строку действия и прочитайте его команду или ввод под списком. Ориентируйтесь на команду или ввод, а не на описание строки, которое написал Claude или инструмент.

**3. Подтвердите действие**

Нажмите `r`, чтобы подтвердить действие и позволить Claude повторить попытку.

**4. Закройте диалоговое окно**

Нажмите `Esc`, чтобы закрыть диалоговое окно и применить подтверждение. Если Claude работал, когда вы открыли `/permissions`, отправьте сообщение после того, как Claude закончит, чтобы Claude повторил попытку действия. В противном случае ничего отправлять не нужно: Claude сразу продолжит работу и может повторить попытку. Если он этого не сделает, назовите действие в следующем сообщении, как описано в разделе [Подтверждения, которые вы даёте в диалоге](https://code.claude.com/docs/ru/permission-modes.md#approvals-you-state-in-conversation).

Подтверждение действия не добавляет правило разрешений. В авторежиме повторная попытка действия снова проходит проверку, поэтому оно может быть снова заблокировано. Чтобы пропускать команду и в дальнейшем, [добавьте правило `allow`](#fix-a-denial-with-an-allow-rule-an-environment-entry-or-a-retry).

Если вы не хотите, чтобы Claude сразу повторил попытку, вы можете подтвердить действие на потом, отозвать подтверждение или закрыть диалоговое окно, отменив подтверждения:

* **Подтвердить на потом**: нажмите `Enter` на строке, затем `Esc`. Строка исчезнет с вкладки, и Claude сможет повторить попытку действия после вашего следующего сообщения, когда закончит работу. Если вы также нажали `r` на другой строке, строка, на которой вы нажали `Enter`, останется на вкладке, и Claude не будет сообщено об этом действии. Подтвердите эту строку при следующем посещении или нажмите `r` на обеих
* **Отозвать подтверждение**: до нажатия `Esc` нажмите `Enter` на строке, независимо от того, подтвердили вы её с помощью `Enter` или `r`
* **Закрыть диалоговое окно и отменить подтверждения**: дважды нажмите `Ctrl+C`

Подтвердить действие на вкладке нельзя, если его строка не может показать всю команду или ввод или если у действия нет строки:

* **В строке написано `This row can't be approved here`**: если вы действительно хотели выполнить это действие, скажите об этом Claude в следующем сообщении, и Claude может попробовать снова
* **Строки нет, а в диалоге есть `Not run` или ошибка классификатора**: классификатор авторежима не вынес вердикта. Чтобы узнать, как выполнить действие, прочитайте [Auto mode cannot determine the safety of an action](https://code.claude.com/docs/ru/errors.md#auto-mode-cannot-determine-the-safety-of-an-action)

### Исправить отклонение с помощью правила allow, записи окружения или повтора

Уведомления выглядят как `bash blocked by auto mode · /permissions · Auto mode: [Data Exfiltration]`. Чтобы увидеть команду или URL, стоящие за уведомлением, используйте вкладку **Recently blocked**, хук или диалог:

* **Вкладка Recently blocked**: выделите строку действия. В [режиме экранного диктора](https://code.claude.com/docs/ru/accessibility.md) все команды и вводы отображаются перед списком.
* **Хук**: чтобы программно захватить точный ввод отклонений, добавьте [хук `PermissionDenied`](https://code.claude.com/docs/ru/hooks#permissiondenied), который получает его как `tool_input`. Если ваш хук читает `reason`, учитывайте, что префикса `Auto mode:` не будет, а вместо `No reason provided` будет текст, например `Blocked by classifier`.
* **Диалог**: найдите вызов инструмента. Если вызов отображается сокращённым или свёрнутым в строку сводки, нажмите `Ctrl+O`, чтобы открыть [средство просмотра транскрипта](https://code.claude.com/docs/ru/interactive-mode.md#transcript-viewer).

Текст под вызовом говорит вам, есть ли что-то для исправления. Тусклая строка `Not run · auto mode's check had no usable answer` или текст, который сообщает о проблеме с самим классификатором, такой как `Auto mode could not evaluate this action`, означает, что Claude Code заблокировал вызов без вердикта от классификатора. Для строки `Not run` нажмите `Ctrl+O`, чтобы прочитать полное сообщение, затем см. [Auto mode cannot determine the safety of an action](https://code.claude.com/docs/ru/errors.md#auto-mode-cannot-determine-the-safety-of-an-action) или [The server returned no safety verdict](https://code.claude.com/docs/ru/errors.md#the-server-returned-no-safety-verdict), чтобы узнать, что делать.

В противном случае строка `Blocked by auto mode` означает, что классификатор посчитал вызов небезопасным. Чтобы пропустить вызов, выполните шаг, соответствующий тому, к чему Claude пытался обратиться или что пытался сделать:

* Пункт назначения, который Claude нужен на протяжении всей задачи, такой как реестр пакетов, внутренний домен или хост репозитория: добавьте его в `autoMode.environment`.
* Команда, которую вы хотите разрешить с этого момента: добавьте правило `allow`.
* Одноразовое действие, которое вы действительно намеревались выполнить: укажите это намерение в следующем сообщении и позвольте Claude повторить попытку.

Вы можете добавить запись окружения или правило `allow` из вкладки [**Auto mode** диалога `/permissions`](#edit-rules-from-permissions).

Текст в квадратных скобках указывает, с чем совпал классификатор. Если это правило, встроенное в Claude Code, передайте его название без скобок в [`claude auto-mode defaults --label`](#inspect-the-defaults-and-your-effective-config), чтобы прочитать полный текст.

### Исправить `Destructive or Unwanted Actions` и другие отклонения по политике

Если в отклонении указано одно из этих названий, [серверный классификатор](https://code.claude.com/docs/ru/permission-modes.md#server-side-classifier-review) заблокировал вызов и указал в качестве причины общую политику:

* `[Destructive or Unwanted Actions]`
* `[Unauthorized Access]`
* `[Undermining Oversight]`
* `[Unsanctioned Communication]`

Название политики — это лишь категория, и `claude auto-mode defaults` не выводит её текст. Прочитайте заблокированный вызов в диалоге или выполните `/permissions` в сессии терминала и посмотрите в разделе **Recently blocked**. Если это то, что вы хотели, чтобы Claude сделал, дайте классификатору больше контекста:

* **Только для этого вызова**: скажите Claude сделать это, назвав действие и его цель, например «перезапиши `data/seed.json`»
* **Для пункта назначения, которому вы доверяете, например реестра пакетов**: добавьте его в [`autoMode.environment`](#define-trusted-infrastructure)
* **Для рутинного действия, которое вы хотите разрешить с этого момента**: опишите его в записи [`autoMode.allow`](#override-the-block-and-allow-rules)

После добавления записи попросите Claude повторить попытку, чтобы классификатор снова проверил вызов.

### Исправить повторяющиеся отклонения

Повторяющиеся отклонения для одного и того же пункта назначения обычно означают, что классификатору не хватает контекста. Добавьте этот пункт назначения в `autoMode.environment` или [запустите `/auto-mode-setup`](#generate-environment-entries), чтобы Claude Code составил записи, затем запустите `claude auto-mode config`, чтобы подтвердить, что изменение вступило в силу.

## См. также

* [Режимы разрешений](https://code.claude.com/docs/ru/permission-modes.md#eliminate-prompts-with-auto-mode): что такое автоматический режим, что он блокирует по умолчанию и какие сеансы начинаются в нём
* [Управляемые параметры](https://code.claude.com/docs/ru/server-managed-settings.md): развёртывание конфигурации `autoMode` в вашей организации
* [Разрешения](https://code.claude.com/docs/ru/permissions.md): правила разрешения, запроса и отказа, которые применяются до запуска классификатора
* [Все параметры](https://code.claude.com/docs/ru/settings-reference.md#automode): каждый ключ параметров, включая `autoMode`
