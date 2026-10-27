import socket
from collections.abc import Iterator


def send_line(sock: socket.socket, text: str) -> None:
    sock.sendall((text + "\n").encode("utf-8"))


def iter_lines(sock: socket.socket) -> Iterator[str]:
    reader = sock.makefile("r", encoding="utf-8", newline="\n")
    for line in reader:
        yield line.rstrip("\n")
