import argparse
import logging
import socket
import threading

from common.config import DEFAULT_HOST, DEFAULT_PORT
from common.protocol import iter_json, send_json

logger = logging.getLogger("client")


def receive_loop(messages) -> None:
    for msg in messages:
        if msg["type"] == "message":
            print(f"\n{msg['from']}: {msg['text']}\n> ", end="")
        elif msg["type"] == "history":
            print(f"\n[история] {msg['from']}: {msg['text']}\n> ", end="")
        elif msg["type"] == "system":
            print(f"\n* {msg['text']}\n> ", end="")
        elif msg["type"] == "who_reply":
            print(f"\nОнлайн: {', '.join(msg['users'])}\n> ", end="")
        elif msg["type"] == "stats_reply":
            if not msg["top"]:
                print("\nСообщений пока нет\n> ", end="")
            else:
                lines = [f"  {i}. {name} — {count}" for i, (name, count) in enumerate(msg["top"], start=1)]
                print("\nСамые активные:\n" + "\n".join(lines) + "\n> ", end="")
        elif msg["type"] == "error":
            print(f"\nОшибка: {msg['text']}\n> ", end="")


def main():
    parser = argparse.ArgumentParser(description="Клиент чата")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    username = input("Ваш ник: ").strip()
    send_json(sock, {"type": "join", "username": username})

    messages = iter_json(sock)
    threading.Thread(target=receive_loop, args=(messages,), daemon=True).start()

    print("Соединение установлено. Команда /who — список пользователей онлайн.")
    while True:
        text = input("> ")
        if text == "/who":
            send_json(sock, {"type": "who"})
        elif text == "/stats":
            send_json(sock, {"type": "stats"})
        else:
            send_json(sock, {"type": "message", "text": text})


if __name__ == "__main__":
    main()
