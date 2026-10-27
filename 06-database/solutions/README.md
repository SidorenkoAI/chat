# Эталонные решения к заданиям урока 6

Каждая папка — полная, самостоятельно запускаемая копия кода урока с **одним** применённым заданием (см. [EXERCISES.md](../EXERCISES.md)). Изменены только файлы, указанные в таблице; остальные совпадают с кодом урока.

Запуск: открыть терминал в папке решения, `python -m server`, затем в других вкладках терминала `python -m client`.

| Папка | Задание | Изменённые файлы |
|---|---|---|
| [01-history-time](01-history-time) | Время в истории | `client/__main__.py`, `db/storage.py` |
| [02-end-of-history](02-end-of-history) | «Конец истории» | `server/core.py` |
| [03-count-on-start](03-count-on-start) | Счётчик сообщений при старте | `db/storage.py`, `server/core.py` |
| [04-history-command](04-history-command) | Команда `/history N` | `client/__main__.py`, `common/config.py`, `server/core.py` |
| [05-search](05-search) | Поиск: `/search слово` | `client/__main__.py`, `db/storage.py`, `server/core.py` |
| [06-stats](06-stats) | Статистика: `/stats` | `client/__main__.py`, `db/storage.py`, `server/core.py` |
| [07-last-seen](07-last-seen) | «Был в сети»: `/lastseen ник` | `client/__main__.py`, `db/storage.py`, `server/core.py` |
| [08-export-csv](08-export-csv) | Экспорт истории в CSV | `db/storage.py`, `export_history.py` (новый) |

Если решение меняет структуру таблиц (07), перед запуском удалите старый `chat.db` в папке решения.
