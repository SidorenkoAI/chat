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
