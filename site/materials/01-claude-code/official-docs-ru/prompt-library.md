> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Библиотека промптов

> Копируйте и вставляйте промпты для Claude Code, отсортированные по задачам и ролям.

Это библиотека промптов для копирования в Claude Code. Используйте её, чтобы изучить новые способы работы или когда вы не знаете, с чего начать.

Промпты собраны из различных руководств Anthropic, включая [Типичные рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md), [Лучшие практики](https://code.claude.com/docs/ru/best-practices.md) и [Как команды Anthropic используют Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code). Это отправные точки, а не готовые скрипты. Откройте **Почему это работает** под любым промптом, чтобы увидеть закономерность, стоящую за ним, и написать свой собственный.

## Что делает эти промпты работающими

Промпты выше имеют несколько общих закономерностей. Их распознавание помогает вам адаптировать любой промпт здесь к вашей собственной задаче.

**Опишите результат, а не шаги.** Скажите, что вы хотите, и позвольте Claude найти файлы. Промпт ниже работает без указания ни одного пути файла.

```text wrap theme={null}
add rate limiting to the public API and make sure existing tests still pass
```

**Дайте ему способ проверить свою работу.** Спросите запустить, протестировать, сравнить или проверить в одном промпте, чтобы Claude повторял вместо остановки после одной попытки. Чтобы проверить завершённое изменение против работающего приложения, запустите [`/verify`](https://code.claude.com/docs/ru/skills#run-and-verify-your-app).

```text wrap theme={null}
write the migration, run it against the dev database, and confirm the schema matches
```

**Укажите на ссылку.** Назовите существующий файл, тест или паттерн для соответствия, чтобы новый код был согласован с тем, что у вас уже есть.

```text wrap theme={null}
add a settings page that follows the same layout as the profile page
```

**Укажите измеримую цель.** Когда цель — производительность или покрытие, дайте метрику и пороговое значение, чтобы завершение было однозначным.

```text wrap theme={null}
get the bundle size under 200KB and show me what you removed
```

**Дайте ему артефакт.** Вставьте ошибки, логи, скриншоты и вывод плана прямо в промпт, или введите `@`, чтобы ссылаться на файл. Claude читает источник вместо вашего описания.

```text wrap theme={null}
why is the build failing? @build.log
```

**Скажите, как вы хотите ответ.** Назовите формат, длину или аудиторию, чтобы объяснение соответствовало тому, как вы его будете использовать. Чтобы сделать формат по умолчанию для каждого ответа, установите [стиль вывода](https://code.claude.com/docs/ru/output-styles.md).

```text wrap theme={null}
explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser
```

Для подробнее о каждом паттерне, см. [лучшие практики](https://code.claude.com/docs/ru/best-practices.md).

## Откуда они берутся

Эти промпты основаны на паттернах из опубликованных ресурсов Anthropic. Каждая карточка ссылается на свой источник:

* [Типичные рабочие процессы](https://code.claude.com/docs/ru/common-workflows.md): пошаговые руководства для основных задач
* [Лучшие практики](https://code.claude.com/docs/ru/best-practices.md): паттерны промптирования и настройка проекта
* [Как команды Anthropic используют Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code): реальные рабочие процессы из команд инженерии, продукта, дизайна и данных, с глубокими погружениями в [legal](https://claude.com/blog/how-anthropic-uses-claude-legal), [marketing](https://claude.com/blog/how-anthropic-uses-claude-marketing) и [cybersecurity](https://claude.com/blog/how-anthropic-uses-claude-cybersecurity)
* [Руководство по масштабированию агентного кодирования](https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf): руководство по внедрению на уровне предприятия

Для видеопрохождений этих паттернов, см. бесплатный курс [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action) на [Claude Academy](https://academy.claude.com/).

## Связанные ресурсы

Промпты на этой странице — это отправные точки. Как только один работает для вашего проекта, следующий шаг — сделать его повторяемым: сохраните его как [skill](https://code.claude.com/docs/ru/skills.md), чтобы кто-либо из вашей команды мог запустить его как `/command`, и запишите соглашения, которые Claude изучил, в [CLAUDE.md](https://code.claude.com/docs/ru/memory.md), чтобы каждая сессия начиналась с этого контекста вместо того, чтобы Claude переучивался. Для более крупных или рискованных изменений [режим плана](https://code.claude.com/docs/ru/permission-modes.md#analyze-before-you-edit-with-plan-mode) показывает вам список файлов перед любыми редактированиями.

Если вы вводите Claude Code в команду, см. [администрирование](https://code.claude.com/docs/ru/admin-setup.md) для управляемых параметров и политики, и [затраты и использование](https://code.claude.com/docs/ru/costs.md) для того, как эта работа выставляется в счёт в вашем плане.
