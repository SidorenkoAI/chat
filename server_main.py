from server import Server

server = Server(port=9090)
server.start()
while True:
    text, addr = server.recive()

    if addr:
        server.sendAll(text, addr)