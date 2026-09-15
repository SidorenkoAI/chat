import socket
import threading
def read_sok():
     while 1:
         data = sok.recv(1024)
         print(data.decode('utf-8'))

sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sok.connect(('localhost', 9090))

potok = threading.Thread(target=read_sok)
potok.start()
while 1:
     mes = input()
     sok.send(mes.encode('utf-8'))