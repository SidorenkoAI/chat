import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5555
RETRIES = 10


def receive_loop(sock: socket.socket) -> None:
    incoming = sock.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        print(f"\nСервер: {text}\n> ", end="")


def connect_with_retries() -> socket.socket | None:
    for attempt in range(1, RETRIES + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((HOST, PORT))
            return sock
        except ConnectionRefusedError:
            sock.close()
            print(f"Сервер недоступен (попытка {attempt}/{RETRIES}), жду секунду...")
            time.sleep(1)
    return None


def main():
    sock = connect_with_retries()
    if sock is None:
        print("Не удалось подключиться к серверу.")
        return
    print("Соединение установлено. Остановить клиента — Ctrl+C.")

    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    while True:
        text = input("> ")
        sock.sendall((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
