# Эталонные решения к заданиям урока 4

Каждая папка — полная, самостоятельно запускаемая копия кода урока с **одним** применённым заданием (см. [EXERCISES.md](../EXERCISES.md)). Изменены только файлы, указанные в таблице; остальные совпадают с кодом урока.

Запуск: открыть терминал в папке решения, `python -m server`, затем в других вкладках терминала `python -m client`.

| Папка | Задание | Изменённые файлы |
|---|---|---|
| [01-log-level](01-log-level) | Флаг `--log-level` | `server/__main__.py`, `server/core.py` |
| [02-shared-log-format](02-shared-log-format) | Общий формат логов | `client/__main__.py`, `common/config.py`, `server/__main__.py` |
| [03-log-file](03-log-file) | Логи в файл: флаг `--log-file` | `server/__main__.py` |
| [04-handle-message-method](04-handle-message-method) | Метод `handle_message` | `server/core.py` |
| [05-client-class](05-client-class) | Класс `ChatClient` | `client/__main__.py`, `client/core.py` (новый) |
| [06-max-clients](06-max-clients) | Флаг `--max-clients` | `server/__main__.py`, `server/core.py` |
| [07-two-servers](07-two-servers) | Две комнаты в одной программе | `run_two_servers.py` (новый) |
| [08-graceful-stop](08-graceful-stop) | Метод `stop()` и корректная остановка | `server/__main__.py`, `server/core.py` |
| [09-robust-broadcast](09-robust-broadcast) | Надёжный `broadcast` | `server/core.py` |
