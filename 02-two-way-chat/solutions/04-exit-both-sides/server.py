import socket
import threading

HOST = "127.0.0.1"
PORT = 5555


def close_connection(sock: socket.socket) -> None:
    # shutdown закрывает соединение, даже пока жив объект из makefile(),
    # и заодно будит поток приёма, который ждёт данных.
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    sock.close()


def receive_loop(conn: socket.socket, connected: threading.Event) -> None:
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    try:
        for line in incoming:
            text = line.rstrip("\n")
            if text == "/exit":
                break
            print(f"\nКлиент: {text}\n> ", end="")
    except OSError:
        pass
    if connected.is_set():
        connected.clear()
        print("\nСобеседник вышел из чата. Нажмите Enter, чтобы завершить.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер слушает {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    connected = threading.Event()
    connected.set()
    threading.Thread(target=receive_loop, args=(conn, connected), daemon=True).start()

    print("Команда /exit — выход.")
    while connected.is_set():
        text = input("> ")
        if not connected.is_set():
            break
        if text == "/exit":
            connected.clear()
            conn.sendall("/exit\n".encode("utf-8"))
            break
        conn.sendall((text + "\n").encode("utf-8"))

    close_connection(conn)
    server_socket.close()
    print("Соединение закрыто.")


if __name__ == "__main__":
    main()
