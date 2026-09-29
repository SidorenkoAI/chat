import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

clients = []
clients_lock = threading.Lock()


def broadcast(text: str) -> None:
    with clients_lock:
        for conn in clients:
            conn.sendall((text + "\n").encode("utf-8"))


def handle_client(conn: socket.socket, addr) -> None:
    print(f"Подключился клиент {addr}")
    with clients_lock:
        clients.append(conn)

    incoming = conn.makefile("r", encoding="utf-8", newline="\n")
    try:
        for line in incoming:
            text = line.rstrip("\n")
            print(f"{addr}: {text}")
            broadcast(f"{addr}: {text}")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"Клиент {addr} отключился")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер слушает {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
