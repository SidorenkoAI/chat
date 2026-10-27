import logging
import socket
import threading

from common.protocol import iter_lines, send_line

logger = logging.getLogger("client")


class ChatClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        logger.info("Подключились к %s:%s", self.host, self.port)

    def receive_loop(self) -> None:
        for text in iter_lines(self.sock):
            print(f"\n{text}\n> ", end="")

    def send(self, text: str) -> None:
        send_line(self.sock, text)

    def run(self) -> None:
        self.connect()
        threading.Thread(target=self.receive_loop, daemon=True).start()
        while True:
            self.send(input("> "))
