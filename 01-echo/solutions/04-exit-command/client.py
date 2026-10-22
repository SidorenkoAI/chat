import socket

HOST = "127.0.0.1"
PORT = 5555


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    incoming = sock.makefile("r", encoding="utf-8", newline="\n")

    print("Соединение установлено. Команда /exit — выход.")
    while True:
        text = input("> ")
        if text == "/exit":
            break
        sock.sendall((text + "\n").encode("utf-8"))
        reply = incoming.readline().rstrip("\n")
        print(f"Эхо: {reply}")

    sock.close()
    print("Соединение закрыто.")


if __name__ == "__main__":
    main()
