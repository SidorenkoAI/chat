import json
import socket
from collections.abc import Iterator


def send_json(sock: socket.socket, obj: dict) -> None:
    line = json.dumps(obj, ensure_ascii=False)
    sock.sendall((line + "\n").encode("utf-8"))


def iter_json(sock: socket.socket) -> Iterator[dict]:
    reader = sock.makefile("r", encoding="utf-8", newline="\n")
    for line in reader:
        line = line.rstrip("\n")
        if line:
            yield json.loads(line)
