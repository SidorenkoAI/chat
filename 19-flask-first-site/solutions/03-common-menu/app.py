"""Первый сайт на Flask: несколько страниц, страница с текущим временем
и страница, адрес которой содержит имя пользователя."""

from datetime import datetime

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


def page(title, body):
    """Собрать полную HTML-страницу: заголовок вкладки, общее меню и содержимое.

    Чтобы добавить пункт меню, достаточно поменять его здесь — в одном месте.
    """
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{title} — Школьный чат</title>
</head>
<body>
  <nav>
    <a href="/">Главная</a> ·
    <a href="/about">О чате</a> ·
    <a href="/time">Который час?</a>
  </nav>
  <hr>
  {body}
</body>
</html>"""


@app.route("/")
def index():
    return page("Главная", """
    <h1>Школьный чат</h1>
    <p>Скоро здесь будет веб-версия нашего чата. А пока — первый сайт на Flask.</p>
    <p>Попробуйте <a href="/user/Аня">страницу Ани</a> — и подставьте в адрес своё имя.</p>
    """)


@app.route("/about")
def about():
    return page("О чате", """
    <h1>О чате</h1>
    <p>Чат написан на Python. Сервер — на сокетах (уроки 1–10),
    сайт — на Flask (уроки 19–25).</p>
    """)


@app.route("/time")
def show_time():
    # Эта функция выполняется при КАЖДОМ запросе: обновите страницу — время изменится
    now = datetime.now().strftime("%H:%M:%S")
    return page("Время", f"<h1>Сейчас {now}</h1>")


@app.route("/user/<name>")
def user(name):
    # name — кусок адреса: для /user/Аня это "Аня".
    # escape() превращает < и > в безопасные &lt; и &gt; — см. «Безопасность» в THEORY.md
    safe_name = escape(name)
    return page(safe_name, f"<h1>Привет, {safe_name}!</h1>")


if __name__ == "__main__":
    app.run(debug=True)
