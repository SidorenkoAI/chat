import logging
import socket
import threading

from common.config import HISTORY_LIMIT
from common.protocol import iter_json, send_json
from db.storage import get_connection, load_history, save_message

logger = logging.getLogger("server")


class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients: dict[str, socket.socket] = {}
        self.lock = threading.Lock()
        self.db = get_connection()

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
        with self.lock:
            if not username or username in self.clients:
                send_json(conn, {"type": "error", "text": "Имя занято или пустое"})
                conn.close()
                return
            self.clients[username] = conn

        logger.info("%s подключился (%s)", username, addr)

        with self.lock:
            history = load_history(self.db, HISTORY_LIMIT)
        for from_user, text, created_at in history:
            send_json(conn, {"type": "history", "from": from_user, "text": text, "at": created_at})
        if history:
            send_json(conn, {"type": "system", "text": "— конец истории —"})

        self.broadcast({"type": "system", "text": f"{username} присоединился к чату"})

        try:
            for msg in messages:
                if msg["type"] == "message":
                    with self.lock:
                        save_message(self.db, username, msg["text"])
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
