# Шрифты

Локальные кириллические подмножества Noto, чтобы сайт не ходил в Google Fonts.

| Файл | Что это |
|---|---|
| `sans-regular.woff2` | Noto Sans, кириллица, 400 |
| `sans-700.woff2` | Noto Sans, кириллица, 700 |
| `serif-regular.woff2` | Noto Serif, кириллица, 400 (≈ variable: покрывает 400 и 700) |
| `mono-regular.woff2` | Noto Sans Mono, кириллица, 400 (покрывает 400 и 700) |
| `fonts.css` | `@font-face` для всех файлов |
| `LICENSE-OFL.txt` | SIL OFL 1.1 |

Источник — CSS Google Fonts, блок `/* cyrillic */`:
<https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&family=Noto+Serif:wght@400;700&family=Noto+Sans+Mono:wght@400;700&display=swap>

У Noto Serif Google отдаёт один файл на 400 и 700 (переменный шрифт),
у Noto Sans — разные, поэтому для него лежат два файла.

Если файл не загрузится, браузер откатится на шрифты из fallback-списка
в `css/style.css`.
