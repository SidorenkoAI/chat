import socket
class Server():
    def __init__(self, port):
        self.HOST = ''
        self.PORT = port
        self.users = {}
        self.authorized = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def updateUsers(self):
        f = open('users.txt', encoding='utf-8')
        for s in f:
            data = s.split()
            name = data[0]
            password = data[1]
            self.users[name] = password
        f.close()

    def start(self):
        self.server.bind((self.HOST, self.PORT))
        self.updateUsers()
        print(f'Сервер запущен на {self.HOST}:{self.PORT}')

    def changePass(self, addr, text):
        #!!ПЕРЕДЕЛАТЬ
        oldPass = text.split()[1]
        newPass = text.split()[2]
        name = authorized[addr]
        if oldPass == users[name]:
            server.sendto('верный пароль'.encode('utf-8'), addr)
            users[name] = newPass
            with open('users.txt', encoding='utf-8', mode='w') as f:
                for name in users:
                    print(f'{name} {users[name]}', file=f)

    def auth(self, text, addr):
        parts = text.split()
        if len(parts) == 3:
            username, password = parts[1], parts[2]
            if username in self.users:
                if password == self.users[username]:
                    self.authorized[addr] = username
                    self.server.sendto(b'AUTH_OK', addr)
                    print(f'Авторизован: {username} ({addr})')
                else:
                    self.server.sendto('AUTH_FAIL "Неверный пароль"'.encode('utf-8'), addr)
                    print(f'Неверный пароль от {addr}')
            else:
                self.server.sendto('AUTH_FAIL "Неверный логин"'.encode('utf-8'), addr)
                print(f'Неверный логин {addr}')
        else:
            self.server.sendto('Требуется авторизация в формате AUTH <username> <password>'.encode('utf-8'), addr)

    def privet(self, addr):
        mes = '''Привет! Для начала общения нужно авторизоваться
                Список доступных команд: help/'''
        self.server.sendto(mes.encode('utf-8'), addr)

    def help(self, addr):
        mes = '''
            reg/   Регистрация  (reg/ <name> <pass>)
            auth/  Авторизация  (auth/ <name> <pass>)
            help/  Помощь  
        '''
        self.server.sendto(mes.encode('utf-8'), addr)

    def reg(self, text, addr):
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
                self.updateUsers()
                mes = '''
                        Вы зарегистрированы!
                        '''
            else:
                mes = '''
                        Такой пользователь уже зарегистрирован..
                        '''
        self.server.sendto(mes.encode('utf-8'), addr)

    def cmdRouter(self, text, addr):
        if text == 'help/':
            self.help(addr)
        elif text.split()[0] == 'auth/':
            self.auth(text, addr)
        elif text.split()[0] == 'reg/':
            self.reg(text, addr)
        else:
            self.privet(addr)

    def recive(self):
        data, addr = self.server.recvfrom(1024)
        text = data.decode('utf-8', errors='replace')
        if addr not in self.authorized:
            self.cmdRouter(text, addr)
            return (False, False)

        return (text, addr)

    def sendAll(self, text, addr):
        out = f'{self.authorized[addr]}: {text}'.encode('utf-8')
        # Рассылаем всем авторизованным, кроме отправителя
        for client_addr in list(self.authorized.keys()):
            if client_addr == addr:
                continue
            self.server.sendto(out, client_addr)
