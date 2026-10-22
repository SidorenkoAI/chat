import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555
LOG_PATH = "dialog.txt"

log_lock = threading.Lock()


def log_line(who: str, text: str) -> None:
    # Пишут два потока: без блокировки строки могли бы перемешаться.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_lock:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{now}] {who}: {text}\n")


def receive_loop(conn: socket.socket) -> None:
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        log_line("Клиент", text)
        print(f"\nКлиент: {text}\n> ", end="")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер слушает {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    threading.Thread(target=receive_loop, args=(conn,), daemon=True).start()

    while True:
        text = input("> ")
        log_line("Сервер", text)
        conn.sendall((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
