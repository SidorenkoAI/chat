import socket
import threading

HOST = "127.0.0.1"
PORT = 5555


def receive_loop(conn: socket.socket) -> None:
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        print(f"\nКлиент: {text}\n> ", end="")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер слушает {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    # Чтение сокета блокирует поток, поэтому приём сообщений выносим в
    # отдельный поток, а в главном потоке спокойно ждём ввода с клавиатуры.
    threading.Thread(target=receive_loop, args=(conn,), daemon=True).start()

    while True:
        text = input("> ")
        conn.sendall((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
