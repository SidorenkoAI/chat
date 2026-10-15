# Эталонные решения к заданиям урока 5

Каждая папка — полная, самостоятельно запускаемая копия кода урока с **одним** применённым заданием (см. [EXERCISES.md](../EXERCISES.md)). Изменены только файлы, указанные в таблице; остальные совпадают с кодом урока.

Запуск: открыть терминал в папке решения, `python -m server`, затем в других вкладках терминала `python -m client`.

| Папка | Задание | Изменённые файлы |
|---|---|---|
| [01-help-command](01-help-command) | Команда `/help` | `client/__main__.py` |
| [02-nick-length](02-nick-length) | Ограничение длины ника | `common/config.py`, `server/core.py` |
| [03-unknown-message-types](03-unknown-message-types) | Сервер не падает от странных сообщений | `server/core.py` |
| [04-nick-command](04-nick-command) | Команда `/nick` — смена ника | `client/__main__.py`, `server/core.py` |
| [05-message-time](05-message-time) | Время в сообщениях | `client/__main__.py`, `server/core.py` |
| [06-join-ok](06-join-ok) | Честный вход: ждём ответа сервера | `client/__main__.py`, `server/core.py` |
| [07-me-command](07-me-command) | Команда `/me` | `client/__main__.py`, `server/core.py` |
| [08-anti-spam](08-anti-spam) | Защита от спама | `common/config.py`, `server/core.py` |
