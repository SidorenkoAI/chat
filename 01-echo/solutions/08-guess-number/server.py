import random
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

    secret = random.randint(1, 100)
    attempts = 0
    print(f"Загадано число: {secret}")

    for line in incoming:
        text = line.rstrip("\n").strip()
        if not text.isdigit():
            reply = "Это не число, попробуй ещё раз"
        else:
            attempts += 1
            guess = int(text)
            if guess < secret:
                reply = "Больше!"
            elif guess > secret:
                reply = "Меньше!"
            else:
                reply = f"Угадал за {attempts} попыток! Загадываю новое число."
                secret = random.randint(1, 100)
                attempts = 0
                print(f"Загадано число: {secret}")
        conn.sendall((reply + "\n").encode("utf-8"))

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    main()
