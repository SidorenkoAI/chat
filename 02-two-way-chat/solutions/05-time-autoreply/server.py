import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

send_lock = threading.Lock()


def send_line(conn: socket.socket, text: str) -> None:
    # В сокет теперь пишут два потока — главный и поток приёма.
    with send_lock:
        conn.sendall((text + "\n").encode("utf-8"))


def receive_loop(conn: socket.socket) -> None:
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        if text == "/time":
            now = datetime.now().strftime("%H:%M:%S")
            send_line(conn, f"Время на сервере: {now}")
            continue
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
        send_line(conn, text)


if __name__ == "__main__":
    main()
