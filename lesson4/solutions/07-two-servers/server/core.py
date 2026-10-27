import logging
import socket
import threading

from common.protocol import iter_lines, send_line

logger = logging.getLogger("server")


class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients: list[socket.socket] = []
        self.lock = threading.Lock()

    def broadcast(self, text: str) -> None:
        with self.lock:
            for conn in self.clients:
                send_line(conn, text)

    def handle_client(self, conn: socket.socket, addr) -> None:
        logger.info("Подключился клиент %s", addr)
        with self.lock:
            self.clients.append(conn)

        try:
            for text in iter_lines(conn):
                logger.info("%s: %s", addr, text)
                self.broadcast(f"{addr}: {text}")
        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            logger.info("Клиент %s отключился", addr)

    def run(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        logger.info("Сервер слушает %s:%s", self.host, self.port)

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
