"""Первый сайт на Flask: несколько страниц, страница с текущим временем
и страница, адрес которой содержит имя пользователя."""

import random
from datetime import datetime

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>Школьный чат</h1>
    <p>Скоро здесь будет веб-версия нашего чата. А пока — первый сайт на Flask.</p>
    <ul>
      <li><a href="/about">О чате</a></li>
      <li><a href="/time">Который час?</a></li>
      <li><a href="/user/Аня">Страница Ани</a> — подставьте в адрес своё имя</li>
      <li><a href="/dice">Бросить кубик</a></li>
    </ul>
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


# Грани кубика: FACES[0] — единица, FACES[5] — шестёрка
FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]


@app.route("/dice")
def dice():
    # Как и /time, страница собирается заново при каждом запросе — каждый раз новый бросок
    number = random.randint(1, 6)
    return f"""
    <h1 style="font-size: 80px">{FACES[number - 1]}</h1>
    <p>Выпало: <b>{number}</b></p>
    <p><a href="/dice">Бросить ещё раз</a> · <a href="/">На главную</a></p>
    """


@app.route("/user/<name>")
def user(name):
    # name — кусок адреса: для /user/Аня это "Аня".
    # escape() превращает < и > в безопасные &lt; и &gt; — см. «Безопасность» в THEORY.md
    return f"<h1>Привет, {escape(name)}!</h1><p><a href=\"/\">← На главную</a></p>"


if __name__ == "__main__":
    app.run(debug=True)
