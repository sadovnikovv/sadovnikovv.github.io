# Связка Claude Code + OmniRoute: практическое объяснение

*Разбор на основе официальной русской документации OmniRoute (папка `docs-ru`) и вашего файла `cc.txt`. Дата: 18.11.2026.*

---

## 1. Что происходит: схема

```
Claude Code (CLI)
      │  запросы к Anthropic Messages API
      ▼
http://localhost:20128  ← OmniRoute (локальный шлюз)
      │  выбирает провайдера и модель
      ▼
DeepSeek / Claude / GPT / Gemini / GLM / локальные модели ...
```

Claude Code «из коробки» умеет разговаривать только с API Anthropic. OmniRoute притворяется таким API: принимает запросы на `/v1/messages` и перенаправляет их тому провайдеру, который вы выбрали (или автоматически — по квотам и доступности).

**Зачем это нужно:**

- один адрес и один ключ вместо десятка API-ключей;
- можно переключать модели без переустановки клиента;
- автоматический fallback при исчерпании квоты;
- учёт расходов и токенов в одном месте.

**Что важно понимать:** OmniRoute — отдельная программа. Если она не запущена, Claude Code не сможет подключиться, даже если все переменные окружения заданы правильно.

---

## 2. Как Claude Code подключается к шлюзу

Claude Code читает несколько переменных окружения. Ключевые:

| Переменная | Зачем нужна | Пример |
|---|---|---|
| `ANTHROPIC_BASE_URL` | Адрес шлюза. Claude Code сам добавляет `/v1/messages`, поэтому суффикс `/v1` в адресе **не нужен**. | `http://localhost:20128` |
| `ANTHROPIC_AUTH_TOKEN` | Ваш ключ доступа OmniRoute. Уходит в заголовке `Authorization: Bearer ...`. | `sk-...` (ключ из панели OmniRoute) |
| `ANTHROPIC_API_KEY` | Альтернативный способ передать ключ (заголовок `x-api-key`). Если заданы оба, побеждает `ANTHROPIC_AUTH_TOKEN`. | — |
| `ANTHROPIC_MODEL` | Принудительно выбрать модель, минуя `/model`. | `combo/DeepSeek` |
| `ANTHROPIC_SMALL_FAST_MODEL` | Модель для служебных быстрых задач (заголовки, короткие ответы). | `combo/DeepSeek` |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Отключает необязательный трафик (телеметрия, лишние запросы). | `1` |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | Разрешает список моделей из `/v1/models` в `/model`. | `1` |

Переменные читаются **один раз при запуске**. Изменили — перезапустите `claude`.

---

## 3. Разбор вашего `cc.txt`

Файл `cc.txt` — это PowerShell-обёртка запуска. По строкам:

```powershell
Set-Location "C:\Users\SMDWORKS\Downloads\Sasha_II_TUT"

$env:ANTHROPIC_BASE_URL = "http://localhost:20128"
```
Указываем Claude Code, что API находится на локальном порту 20128 — там слушает OmniRoute.

```powershell
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:CLAUDE_CODE_OAUTH_TOKEN -ErrorAction SilentlyContinue
```
Убираем конкурирующие способы авторизации. Если оставить старый `ANTHROPIC_API_KEY` или OAuth-токен, Claude Code может пойти не туда и получить 401.

```powershell
$env:ANTHROPIC_AUTH_TOKEN = 'sk-...'
```
Ключ доступа к OmniRoute. **В реальном файле он лежит открытым текстом** — см. раздел 6.

```powershell
$env:ANTHROPIC_MODEL = "combo/DeepSeek"
$env:ANTHROPIC_SMALL_FAST_MODEL = "combo/DeepSeek"
```
Фиксируем модель: `combo/DeepSeek` — это имя модели/комбо внутри OmniRoute, а не у Anthropic. Если в панели OmniRoute такой модели нет, будет ошибка «model not found». `combo/...` обычно означает автоматическую комбинацию провайдеров.

```powershell
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"
```
Отключаем необязательные сетевые запросы — меньше шума и расходов.

```powershell
$env:CLAUDE_CODE_AUTO_MODE_SERVER = "0"
```
Отключаем серверный режим авто-режима (связан с разрешениями/телеметрией).

```powershell
claude --model "combo/DeepSeek" --permission-mode auto
```
Запуск Claude Code с явной моделью и режимом разрешений `auto`.

> ⚠️ **Про `--permission-mode auto`:** этот режим снижает количество подтверждений. Для первых запусков безопаснее `--permission-mode default`, чтобы видеть, какие команды агент собирается выполнить. Переходите на `auto`, только когда освоитесь и работаете в отдельной папке.

---

## 4. Как проверить связку по шагам

### Шаг 1. Запущен ли OmniRoute

Обычно:

```powershell
omniroute
```

или через Docker:

```powershell
docker run -d --name omniroute -p 20128:20128 diegosouzapw/omniroute:latest
```

Панель управления: `http://localhost:20128`.

### Шаг 2. Есть ли ключ

В панели: **Dashboard → API-ключи** (`http://localhost:20128/dashboard/api-manager`). Создайте ключ и сохраните — он показывается один раз. Это ключ **для клиентов** (Claude Code), а не ключ вышестоящего провайдера.

### Шаг 3. Отвечает ли API

```powershell
curl.exe -H "Authorization: Bearer sk-ВАШ_КЛЮЧ" http://localhost:20128/v1/models
```

Должен вернуться список моделей. Если здесь ошибка — проблема в OmniRoute, а не в Claude Code.

### Шаг 4. Запуск Claude Code

```powershell
.\cc.txt
```
или вручную:

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:20128"
$env:ANTHROPIC_AUTH_TOKEN="sk-ВАШ_КЛЮЧ"
$env:ANTHROPIC_MODEL="combo/DeepSeek"
claude
```

Проверка внутри Claude Code:

```
/status
```
Должно быть видно, что используется нестандартный base URL и выбранная модель.

---

## 5. Частые проблемы

| Симптом | Вероятная причина | Что делать |
|---|---|---|
| `Connection refused` / `ECONNREFUSED` | OmniRoute не запущен или слушает другой порт | Запустить `omniroute`, проверить `http://localhost:20128` |
| `401 Unauthorized` | Неверный ключ, старый `ANTHROPIC_API_KEY`, лишние кавычки | Пересоздать ключ, удалить конкурирующие переменные, перезапустить терминал |
| `404 Not Found` | В `ANTHROPIC_BASE_URL` добавлен `/v1` или `/v1/messages` | Оставить только `http://localhost:20128` |
| `model not found` | В OmniRoute нет модели `combo/DeepSeek` | Открыть панель → проверить точное имя модели или включить discovery |
| Ответы пустые/обрываются | Исчерпана квота провайдера, сработал fallback | Посмотреть логи OmniRoute, сменить модель/провайдера |
| `429 Too Many Requests` | Лимит бесплатного провайдера | Подождать, включить auto-fallback, подключить другого провайдера |
| Claude Code «забывает» настройки | Переменные не попали в текущую сессию | Запускать из одного скрипта, перезапустить терминал |
| TLS/SSL ошибки | Корпоративный прокси или MITM | Отключить перехват для localhost, проверить настройки прокси |

Больше диагностики — в `docs-ru/docs/guides/TROUBLESHOOTING.md` (72 КБ, машинный перевод).

---

## 6. Безопасность

1. **В `cc.txt` лежит боевой токен открытым текстом.** Любой, кто получил файл, получил доступ к вашему шлюзу.
2. **Не коммитьте `cc.txt` в git.** Добавьте его в `.gitignore` или держите вне репозитория.
3. **Ротируйте ключ**, если файл кому-то отправляли (в мессенджер, в архив, в чат ИИ).
4. **Лучше хранить ключ в переменной пользователя** или в менеджере секретов, а не в скрипте:
   ```powershell
   [Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN","sk-...","User")
   ```
5. **Проверяйте, куда ведёт `ANTHROPIC_BASE_URL`.** Если это чужой сервер, вы отправляете ему весь код и контекст.
6. **`--permission-mode auto`** даёт агенту больше свободы. Работайте в отдельной папке и с бэкапами.

---

## 7. Где читать дальше (в этой папке)

| Файл | Что внутри |
|---|---|
| `docs-ru/docs/getting-started/QUICK-START.md` | Установка OmniRoute за 3 минуты |
| `docs-ru/docs/guides/CLAUDE-CODE-CONFIGURATION.md` | Полная официальная инструкция по связке с Claude Code |
| `docs-ru/docs/guides/USER_GUIDE.md` | Пользовательское руководство (82 КБ) |
| `docs-ru/docs/guides/CLI-INTEGRATIONS.md` | Интеграции с CLI-инструментами |
| `docs-ru/docs/guides/COST_TRACKING.md` | Учёт токенов и расходов |
| `docs-ru/docs/guides/TROUBLESHOOTING.md` | Диагностика проблем |
| `docs-ru/docs/getting-started/FREE-TIERS-GUIDE.md` | Бесплатные тарифы и ограничения |
| `docs-ru/docs/getting-started/AUTO-COMBO-GUIDE.md` | Как работают автоматические комбинации моделей |

> Переводы OmniRoute машинные: смысл передан, но формулировки местами корявые. Если что-то непонятно — сверяйтесь с английским оригиналом в репозитории `cheaper-inference/OmniRoute` (`docs/guides/...`).
