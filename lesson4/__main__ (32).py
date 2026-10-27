import argparse
import logging

from client.core import ChatClient
from common.config import DEFAULT_HOST, DEFAULT_PORT


def main():
    parser = argparse.ArgumentParser(description="Клиент чата")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    ChatClient(args.host, args.port).run()


if __name__ == "__main__":
    main()
