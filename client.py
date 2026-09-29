import socket
import threading

HOST = "127.0.0.1"
PORT = 5555


def receive_loop(sock: socket.socket) -> None:
    incoming = sock.makefile("r", encoding="utf-8", newline="\n")
    for line in incoming:
        text = line.rstrip("\n")
        print(f"\n{text}\n> ", end="")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("Соединение установлено. Остановить клиента — Ctrl+C.")

    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    while True:
        text = input("> ")
        sock.sendall((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
