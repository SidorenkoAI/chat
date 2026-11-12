"""Первый сайт на Flask: несколько страниц, страница с текущим временем
и страница, адрес которой содержит имя пользователя."""

import threading
from datetime import datetime

from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# Счётчик живёт вне функции, поэтому не обнуляется между запросами.
# Но он хранится в памяти программы — после перезапуска сайта снова 0.
visits = 0
# Каждый запрос Flask обслуживает в своём потоке. Без замка два одновременных
# запроса могли бы прочитать одно и то же число, и одно посещение потерялось бы.
visits_lock = threading.Lock()


@app.route("/")
def index():
    global visits  # без global Python решил бы, что visits — новая переменная внутри функции
    with visits_lock:
        visits += 1
        count = visits
    return f"""
    <h1>Школьный чат</h1>
    <p>Скоро здесь будет веб-версия нашего чата. А пока — первый сайт на Flask.</p>
    <ul>
      <li><a href="/about">О чате</a></li>
      <li><a href="/time">Который час?</a></li>
      <li><a href="/user/Аня">Страница Ани</a> — подставьте в адрес своё имя</li>
    </ul>
    <p><small>Эту страницу открыли {count} раз</small></p>
    """


@app.route("/about")
def about():
    return """
    <h1>О чате</h1>
    <p>Чат написан на Python. Сервер — на сокетах (уроки 1–10),
    сайт — на Flask (уроки 19–25).</p>
    <p><a href="/">← На главную</a></p>
    """


@app.route("/time")
def show_time():
    # Эта функция выполняется при КАЖДОМ запросе: обновите страницу — время изменится
    now = datetime.now().strftime("%H:%M:%S")
    return f"<h1>Сейчас {now}</h1><p><a href=\"/\">← На главную</a></p>"


@app.route("/user/<name>")
def user(name):
    # name — кусок адреса: для /user/Аня это "Аня".
    # escape() превращает < и > в безопасные &lt; и &gt; — см. «Безопасность» в THEORY.md
    return f"<h1>Привет, {escape(name)}!</h1><p><a href=\"/\">← На главную</a></p>"


if __name__ == "__main__":
    app.run(debug=True)
