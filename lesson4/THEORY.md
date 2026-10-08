# Урок 4. Структура проекта — теория и разбор кода

Функциональность сегодня не меняется: это тот же многопользовательский чат из урока 3. Меняется **устройство кода**. Мы раскладываем программу по папкам и файлам так, как это делают в настоящих проектах, — чтобы дальше (база данных, пароли, шифрование) код не превратился в кашу.

## Зачем это нужно

Пока в проекте два файла по 40 строк, всё помещается в голове. Но скоро добавятся база данных, регистрация, шифрование — и два файла станут огромными. Сейчас удачный момент навести порядок: кода мало, переделка безопасна.

Что мы делаем:
- выносим **общий код** сервера и клиента (правила отправки/получения строк, настройки) в отдельный пакет `common`;
- превращаем сервер в **класс** `ChatServer`;
- заменяем `print` на модуль **`logging`**;
- добавляем **параметры командной строки** через `argparse`, чтобы запускать сервер на другом порту без правки кода.

## Новая структура

```
04-project-structure/
    requirements.txt
    common/
        __init__.py
        config.py        # настройки по умолчанию
        protocol.py      # как отправлять и читать сообщения
    server/
        __init__.py
        __main__.py      # точка входа: разбор аргументов, запуск
        core.py          # логика сервера (класс ChatServer)
    client/
        __init__.py
        __main__.py      # точка входа клиента
```

## Подробный разбор: что такое пакет

**Модуль** — это один `.py`-файл. **Пакет** — это папка с модулями, в которой лежит файл `__init__.py` (он может быть пустым). Пакет можно импортировать так же, как модуль:

```python
from common.protocol import send_line   # из пакета common, модуля protocol, взять функцию send_line
```

Точка в `common.protocol` означает «модуль `protocol` внутри пакета `common`» — примерно как путь к файлу `common/protocol.py`.

Файл `__init__.py` помечает папку как пакет. В современных версиях Python можно обойтись и без него, но с ним проще и понятнее — поэтому добавляем всегда.

## Шаг 1. `common/config.py` — настройки

```python
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5555
```

Раньше адрес и порт были записаны прямо в `server.py` и `client.py` — дважды. Если бы мы захотели сменить порт, пришлось бы помнить про оба места. Теперь они в **одном** месте, а сервер и клиент их импортируют. Слово `DEFAULT` («по умолчанию») — потому что дальше их можно будет переопределить при запуске.

## Шаг 2. `common/protocol.py` — правила обмена сообщениями

```python
import socket
from collections.abc import Iterator


def send_line(sock: socket.socket, text: str) -> None:
    sock.sendall((text + "\n").encode("utf-8"))


def iter_lines(sock: socket.socket) -> Iterator[str]:
    reader = sock.makefile("r", encoding="utf-8", newline="\n")
    for line in reader:
        yield line.rstrip("\n")
```

**Протокол** — это договорённость о том, как стороны общаются. Наша договорённость: «сообщение — строка текста в UTF-8, в конце `\n`». Раньше эти правила были размазаны по коду сервера и клиента. Теперь они в одном файле, и если мы захотим их поменять (а на уроке 5 захотим!), менять придётся только здесь.

- `send_line(sock, text)` — отправить одно сообщение: добавить `\n`, перевести в байты, отправить всё.
- `from collections.abc import Iterator` и `-> Iterator[str]` — только аннотация типа: «функция выдаёт строки одну за другой».
- `iter_lines(sock)` — **генератор** (см. подробный разбор ниже): выдаёт полученные строки по одной, уже без `\n`.

## Подробный разбор: генераторы и `yield`

Обычная функция возвращает результат один раз через `return` и заканчивается. Функция с `yield` — **генератор** — работает иначе: каждый раз, дойдя до `yield`, она **отдаёт** очередное значение и **замирает** до следующего запроса.

```python
for text in iter_lines(conn):
    print(text)
```

Как это работает:
1. цикл `for` просит у генератора следующее значение;
2. генератор выполняется до `yield`, отдаёт строку и замирает;
3. тело цикла печатает строку;
4. цикл просит следующее — генератор «просыпается» с того же места и ждёт новую строку из сокета.

Зачем так сложно? Чтобы тот, кто использует `iter_lines`, писал простой `for` и не думал про `makefile`, кодировки и `rstrip`. Все эти детали спрятаны внутри.

## Шаг 3. `server/core.py` — класс `ChatServer`

### 3.1. Импорты и логгер

```python
import logging
import socket
import threading

from common.protocol import iter_lines, send_line

logger = logging.getLogger("server")
```

- `logging` — стандартный модуль для записи журнала работы программы (логов).
- `from common.protocol import iter_lines, send_line` — берём наши общие функции из пакета `common`.
- `logging.getLogger("server")` — создаём **логгер** с именем `"server"`. Через него будем писать сообщения вместо `print`.

### 3.2. Класс и конструктор

```python
class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients: list[socket.socket] = []
        self.lock = threading.Lock()
```

- `class ChatServer:` — объявляем класс, «чертёж» сервера.
- `__init__` — **конструктор**: вызывается автоматически, когда создаём объект `ChatServer("127.0.0.1", 5555)`.
- `self` — ссылка на сам создаваемый объект. `self.host = host` значит «запомнить адрес внутри этого объекта».
- `self.clients` и `self.lock` — список клиентов и блокировка. На уроке 3 это были глобальные переменные модуля, теперь — **поля объекта**.

### 3.3. Рассылка всем

```python
    def broadcast(self, text: str) -> None:
        with self.lock:
            for conn in self.clients:
                send_line(conn, text)
```

То же, что на уроке 3, только вместо глобальных `clients`/`clients_lock` — `self.clients`/`self.lock`, а вместо ручного `sendall(...encode...)` — наша функция `send_line`.

### 3.4. Обработка одного клиента

```python
    def handle_client(self, conn: socket.socket, addr) -> None:
        logger.info("Подключился клиент %s", addr)
        with self.lock:
            self.clients.append(conn)

        try:
            for text in iter_lines(conn):
                logger.info("%s: %s", addr, text)
                self.broadcast(f"{addr}: {text}")
        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            logger.info("Клиент %s отключился", addr)
```

Логика та же, что на уроке 3:
- добавить клиента в список под блокировкой;
- в цикле читать его сообщения (теперь через генератор `iter_lines`) и рассылать всем;
- в `finally` — обязательно убрать клиента и закрыть соединение, что бы ни случилось.

Новое — `logger.info("Подключился клиент %s", addr)`. Вместо f-строки используется `%s`: логгер сам подставит значение `addr` на место `%s`. Так принято в `logging` — подстановка происходит, только если сообщение действительно будет записано.

### 3.5. Запуск сервера

```python
    def run(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        logger.info("Сервер слушает %s:%s", self.host, self.port)

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
```

Всё как раньше. Обрати внимание на `target=self.handle_client` — в поток передаётся **метод объекта**. Python сам «привяжет» к нему `self`, поэтому в `args` передаём только `conn` и `addr`.

## Подробный разбор: почему класс лучше глобальных переменных

На уроке 3 список клиентов был глобальной переменной модуля. Это работает, пока сервер один. А если в одной программе нужно **два** сервера — например, две «комнаты» чата на разных портах? С глобальными переменными оба сервера делили бы один список клиентов, и сообщения из одной комнаты попадали бы в другую.

С классом каждый объект `ChatServer` хранит **свой** список и **свою** блокировку:

```python
room1 = ChatServer("127.0.0.1", 5555)
room2 = ChatServer("127.0.0.1", 5556)   # у room2 свои clients, никак не связанные с room1
```

## Шаг 4. `server/__main__.py` — точка входа

```python
import argparse
import logging

from common.config import DEFAULT_HOST, DEFAULT_PORT
from server.core import ChatServer


def main():
    parser = argparse.ArgumentParser(description="Сервер чата")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    ChatServer(args.host, args.port).run()


if __name__ == "__main__":
    main()
```

Этот файл только **запускает** сервер, вся логика — в `core.py`. Построчно:

- `argparse.ArgumentParser(description="Сервер чата")` — создаём «разборщик» параметров командной строки. `description` покажется в справке по `python -m server --help`.
- `parser.add_argument("--host", default=DEFAULT_HOST)` — объявляем параметр `--host`. Если его не указать, будет значение по умолчанию из конфига.
- `parser.add_argument("--port", type=int, default=DEFAULT_PORT)` — параметр `--port`; `type=int` превращает текст из командной строки в число.
- `args = parser.parse_args()` — разбираем то, что написали при запуске. Результат: `args.host` и `args.port`.
- `logging.basicConfig(...)` — один раз настраиваем логирование:
  - `level=logging.INFO` — показывать сообщения уровня INFO и важнее (WARNING, ERROR); DEBUG — скрывать;
  - `format=...` — как выглядит строка лога: `%(asctime)s` — дата и время, `%(levelname)s` — уровень, `%(message)s` — сам текст.
- `ChatServer(args.host, args.port).run()` — создаём объект сервера и запускаем.

## Подробный разбор: `__main__.py` и `python -m`

Если в пакете есть файл с особым именем `__main__.py`, весь пакет можно запустить командой:

```bash
python -m server
```

`-m` значит «запусти модуль/пакет по имени». Python найдёт папку `server` **в текущей директории**, выполнит её `__main__.py`, а текущую директорию добавит в пути поиска модулей — поэтому внутри сработает `from common.config import ...`.

Отсюда главное правило: **запускать из папки урока**, где лежат и `server`, и `common`. Иначе будет `ModuleNotFoundError: No module named 'common'`.

## Подробный разбор: `logging` вместо `print`

| `print` | `logging` |
|---|---|
| просто текст | автоматически время и уровень важности |
| всё одинаково важно | уровни: DEBUG < INFO < WARNING < ERROR |
| чтобы убрать отладочный вывод — удалять строки | меняешь `level` в одном месте |
| только в консоль | можно направить в файл, не трогая остальной код |

## Шаг 5. `client/__main__.py`

```python
import argparse
import logging
import socket
import threading

from common.config import DEFAULT_HOST, DEFAULT_PORT
from common.protocol import iter_lines, send_line

logger = logging.getLogger("client")


def receive_loop(sock: socket.socket) -> None:
    for text in iter_lines(sock):
        print(f"\n{text}\n> ", end="")


def main():
    parser = argparse.ArgumentParser(description="Клиент чата")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    logger.info("Подключились к %s:%s", args.host, args.port)

    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    while True:
        text = input("> ")
        send_line(sock, text)


if __name__ == "__main__":
    main()
```

Это клиент из урока 3, но:
- адрес и порт берутся из аргументов командной строки (`args.host`, `args.port`), а по умолчанию — из общего конфига;
- приём — через генератор `iter_lines`, отправка — через `send_line`;
- сообщение о подключении — через логгер.

Сообщения чата по-прежнему печатаются через `print`: это **интерфейс** программы для человека, а не журнал её работы.

## Шаг 6. `requirements.txt`

Файл со списком внешних библиотек проекта (для `pip install -r requirements.txt`). Пока их нет — весь код на стандартной библиотеке, — но файл заведён заранее: на уроке 9 в нём появится первая зависимость.

## Как запустить и проверить

В терминале PyCharm (вкладка **Terminal** внизу), **из папки урока**:

```bash
python -m server
python -m client
```

Каждую команду — в отдельной вкладке терминала (кнопка `+`). Запуск на другом порту без правки кода:

```bash
python -m server --port 6000
python -m client --port 6000
```

Если хочется запускать кнопкой Run: **Run → Edit Configurations → + → Python**, переключить «Script path» на **Module name**, указать `server` и в **Working directory** — папку урока.

## Что дальше: Git и GitHub

Теперь проект устроен как настоящий, и его пора начать **сохранять по-настоящему**: хранить историю изменений и копию в интернете. Для этого есть отдельная пошаговая инструкция с нуля: [GIT.md](GIT.md). В ней мы учимся заводить репозиторий на GitHub и делать два главных действия: `commit` и `push`.

## Частые ошибки

- **`ModuleNotFoundError: No module named 'common'`** — запускаешь не из папки урока. Сделай `cd` в папку, где лежат `common`, `server`, `client`.
- **`ModuleNotFoundError: No module named 'server'`** при запуске `python server/__main__.py` — так запускать нельзя, только `python -m server`.
- **Импорт не работает, хотя папка на месте** — проверь, что в ней есть `__init__.py`.
