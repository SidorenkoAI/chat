import socket

HOST = "127.0.0.1"
PORT = 5555


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер слушает {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    # makefile() превращает сокет в файлоподобный объект: можно читать строки
    # через for, а не вручную собирать байты из recv().
    incoming = conn.makefile("r", encoding="utf-8", newline="\n")

    for line in incoming:
        text = line.rstrip("\n")
        print(f"Получено: {text}")
        conn.sendall((text + "\n").encode("utf-8"))

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
