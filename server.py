import socket
#comment
HOST = ''
PORT = 9090
users = {}

f = open('users.txt', encoding='utf-8')
for s in f:
    data = s.split()
    name = data[0]
    password = data[1]
    users[name] = password

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

authorized = {}
def changePass(addr, text):
    # Ожидаем формат: CHANGE_PASS <старыйпароль> <новый пароль>
    oldPass = text.split()[1]
    newPass = text.split()[2]
    name = authorized[addr]
    if oldPass == users[name]:
        server.sendto('верный пароль'.encode('utf-8'), addr)
        users[name] = newPass
        with open('users.txt', encoding='utf-8', mode='w') as f:
            for name in users:
                print(f'{name} {users[name]}', file=f)

def checkAcess():
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

def privet(addr):
    mes = '''Привет! Для начала общения нужно авторизоваться
            Список доступных команд: help/'''
    server.sendto(mes.encode('utf-8'), addr)

def help(addr):
    mes = '''
        reg/ Регистрация
        auth/ Авторизация 
    '''
    server.sendto(mes.encode('utf-8'), addr)

def cmdRouter(text, addr):
    if text == 'help/':
        help(addr)
    elif text == 'auth/':
        checkAcess()
    else:
        privet(addr)

print(f'Сервер запущен на {HOST}:{PORT}')
while True:
    data, addr = server.recvfrom(1024)
    text = data.decode('utf-8', errors='replace')

    # Если клиент ещё не авторизован
    if addr not in authorized:
        cmdRouter(text, addr)
        continue  # пока не авторизован — ничего не пересылаем
    # Клиент авторизован
    if text.split()[0] == 'CHANGE_PASS':
        changePass(addr, text)
        continue

    username = authorized[addr]
    out = f'{username}: {text}'.encode('utf-8')
    # Рассылаем всем авторизованным, кроме отправителя
    for client_addr in list(authorized.keys()):
        if client_addr == addr:
            continue
        server.sendto(out, client_addr)
