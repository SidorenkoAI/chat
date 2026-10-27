import argparse
import logging

from common.config import DEFAULT_HOST, DEFAULT_PORT
from server.core import ChatServer


def main():
    parser = argparse.ArgumentParser(description="Сервер чата")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--log-file", help="дополнительно писать логи в этот файл")
    args = parser.parse_args()

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
    )
    ChatServer(args.host, args.port).run()


if __name__ == "__main__":
    main()
