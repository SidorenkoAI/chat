import argparse
import logging
import threading

from common.config import DEFAULT_HOST
from server.core import ChatServer


def main():
    parser = argparse.ArgumentParser(description="Несколько независимых серверов в одной программе")
    parser.add_argument("ports", nargs="+", type=int, help="порты, например: 5555 5556")
    parser.add_argument("--host", default=DEFAULT_HOST)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    servers = [ChatServer(args.host, port) for port in args.ports]
    for server in servers[:-1]:
        threading.Thread(target=server.run, daemon=True).start()
    servers[-1].run()


if __name__ == "__main__":
    main()
