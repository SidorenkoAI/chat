import logging
import socket
import threading

from common.config import MAX_USERNAME_LENGTH
from common.protocol import iter_json, send_json

logger = logging.getLogger("server")


class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients: dict[str, socket.socket] = {}
        self.lock = threading.Lock()

    def broadcast(self, obj: dict) -> None:
        with self.lock:
            for conn in self.clients.values():
                send_json(conn, obj)

    def handle_client(self, conn: socket.socket, addr) -> None:
        messages = iter_json(conn)

        try:
            join = next(messages)
        except StopIteration:
            conn.close()
            return

        username = join.get("username", "").strip()
        if len(username) > MAX_USERNAME_LENGTH:
            send_json(conn, {"type": "error", "text": f"Ник длиннее {MAX_USERNAME_LENGTH} символов"})
            conn.close()
            return

        with self.lock:
            if not username or username in self.clients:
                send_json(conn, {"type": "error", "text": "Имя занято или пустое"})
                conn.close()
                return
            self.clients[username] = conn

        logger.info("%s подключился (%s)", username, addr)
        self.broadcast({"type": "system", "text": f"{username} присоединился к чату"})

        try:
            for msg in messages:
                if msg["type"] == "message":
                    self.broadcast({"type": "message", "from": username, "text": msg["text"]})
                elif msg["type"] == "who":
                    with self.lock:
                        online = list(self.clients.keys())
                    send_json(conn, {"type": "who_reply", "users": online})
        finally:
            with self.lock:
                self.clients.pop(username, None)
            conn.close()
            logger.info("%s отключился", username)
            self.broadcast({"type": "system", "text": f"{username} вышел из чата"})

    def run(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        logger.info("Сервер слушает %s:%s", self.host, self.port)

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
