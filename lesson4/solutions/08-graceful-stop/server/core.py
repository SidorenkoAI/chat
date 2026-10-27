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
        self.server_socket: socket.socket | None = None

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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        # На Windows Ctrl+C не прерывает accept(), пока тот ждёт подключения:
        # таймаут раз в секунду возвращает управление Python.
        self.server_socket.settimeout(1.0)
        logger.info("Сервер слушает %s:%s", self.host, self.port)

        while True:
            try:
                conn, addr = self.server_socket.accept()
            except TimeoutError:
                continue
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def stop(self) -> None:
        logger.info("Останавливаю сервер...")
        # Не вызываем broadcast(): он сам берёт self.lock, а повторно взять
        # ту же блокировку нельзя — программа зависла бы навсегда.
        with self.lock:
            for conn in self.clients:
                try:
                    send_line(conn, "Сервер отключается")
                    conn.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
        if self.server_socket is not None:
            self.server_socket.close()
