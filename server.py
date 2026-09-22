import socket

HOST = ''
PORT = 9090
users = {}
authorized = {}
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

def updateUsers():
    global users
    f = open('users.txt', encoding='utf-8')
    for s in f:
        data = s.split()
        name = data[0]
        password = data[1]
        users[name] = password
    f.close()

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

def auth(text, addr):
    parts = text.split()
    if len(parts) == 3:
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
        reg/   Регистрация  (reg/ <name> <pass>)
        auth/  Авторизация  (auth/ <name> <pass>)
        help/  Помощь  
    '''
    server.sendto(mes.encode('utf-8'), addr)

def reg(text, addr):
    if text == 'reg/':
        mes = '''
                Введите имя и пароль в формате
                reg/ <name> <pass>
                '''
    else:
        name = text.split()[1]
        pword = text.split()[2]
        if name not in users:
            with open('users.txt', encoding='utf-8', mode='a') as f:
               print(f'{name} {pword}', file=f)
            updateUsers()
            mes = '''
                    Вы зарегистрированы!
                    '''
        else:
            mes = '''
                    Такой пользователь уже зарегистрирован..
                    '''
    server.sendto(mes.encode('utf-8'), addr)

def cmdRouter(text, addr):
    if text == 'help/':
        help(addr)
    elif text.split()[0] == 'auth/':
        auth(text, addr)
    elif text.split()[0] == 'reg/':
        reg(text, addr)
    else:
        privet(addr)

print(f'Сервер запущен на {HOST}:{PORT}')
updateUsers()
while True:
    data, addr = server.recvfrom(1024)
    text = data.decode('utf-8', errors='replace')

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
