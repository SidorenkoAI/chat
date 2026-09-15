import socket

HOST = ''
PORT = 9090
users = {'Руслан': 'Heckfy', 'Артём': 'Fhn`v', 'Михаил': 'Vb[fbk', 'Анастасия': 'Fyfcnfcbz', 'Ксения': 'Rctybz', 'Антон': 'Fynjy'}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

authorized = {}

print(f'Сервер запущен на {HOST}:{PORT}')

while True:
    data, addr = server.recvfrom(1024)
    text = data.decode('utf-8', errors='replace')

    # Если клиент ещё не авторизован
    if addr not in authorized:
        # Ожидаем формат: AUTH <username> <password>
        parts = text.split()

        if len(parts) == 3 and parts[0] == 'AUTH':
            username, password = parts[1], parts[2]
            if username in users:
                if password == users[username]:
                    authorized[addr] = username
                    server.sendto(b'AUTH_OK', addr)
                    print(f'Авторизован: {username} ({addr})')
                else:
                    server.sendto('AUTH_FAIL "Неверный пароль"'.encode('utf-8'), addr)
                    print(f'Неверный пароль от {addr}')
            else:
                server.sendto('AUTH_FAIL "Неверный логин"'.encode('utf-8'), addr)
                print(f'Неверный логин {addr}')
        else:
            server.sendto('Требуется авторизация в формате AUTH <username> <password>'.encode('utf-8'), addr)

        continue  # пока не авторизован — ничего не пересылаем

    # Клиент авторизован
    username = authorized[addr]
    out = f'{username}: {text}'.encode('utf-8')

    # Рассылаем всем авторизованным, кроме отправителя
    for client_addr in list(authorized.keys()):
        if client_addr == addr:
            continue
        server.sendto(out, client_addr)
