import random
import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

PHRASES = [
    "Интересно!",
    "Расскажи подробнее",
    "Ха-ха, смешно",
    "Согласен",
    "Хм, не уверен",
    "А ты как думаешь?",
]

send_lock = threading.Lock()


def send_line(conn: socket.socket, text: str) -> None:
    with send_lock:
        conn.sendall((text + "\n").encode("utf-8"))


def receive_loop(conn: socket.socket) -> None:
    bot_enabled = False
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        if text == "/bot on":
            bot_enabled = True
            send_line(conn, "[бот] Бот включён")
            continue
        if text == "/bot off":
            bot_enabled = False
            send_line(conn, "[бот] Бот выключен")
            continue
        print(f"\nКлиент: {text}\n> ", end="")
        if bot_enabled:
            send_line(conn, f"[бот] {random.choice(PHRASES)}")


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
