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
