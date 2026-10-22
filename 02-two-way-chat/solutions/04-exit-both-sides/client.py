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


def receive_loop(sock: socket.socket, connected: threading.Event) -> None:
    incoming = sock.makefile("r", encoding="utf-8", newline="\n")
    try:
        for line in incoming:
            text = line.rstrip("\n")
            if text == "/exit":
                break
            print(f"\nСервер: {text}\n> ", end="")
    except OSError:
        pass
    if connected.is_set():
        connected.clear()
        print("\nСобеседник вышел из чата. Нажмите Enter, чтобы завершить.")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("Соединение установлено. Команда /exit — выход.")

    connected = threading.Event()
    connected.set()
    threading.Thread(target=receive_loop, args=(sock, connected), daemon=True).start()

    while connected.is_set():
        text = input("> ")
        if not connected.is_set():
            break
        if text == "/exit":
            connected.clear()
            sock.sendall("/exit\n".encode("utf-8"))
            break
        sock.sendall((text + "\n").encode("utf-8"))

    close_connection(sock)
    print("Соединение закрыто.")


if __name__ == "__main__":
    main()
