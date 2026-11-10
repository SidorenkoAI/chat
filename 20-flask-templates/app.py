"""Страница чата из шаблона: Flask подставляет в HTML данные из Python."""

from flask import Flask, render_template

app = Flask(__name__)

ME = "Аня"  # «кто я» — пока просто константа. Вход по паролю будет в уроке 23.

# Пока сообщения — просто список в программе. На следующем уроке их будут
# добавлять через форму, а в уроке 23 они придут из базы данных чата.
# У системных сообщений нет автора (None).
MESSAGES = [
    {"author": None, "text": "Боря присоединился к чату", "time": "10:14"},
    {"author": "Боря", "text": "Привет всем!", "time": "10:15"},
    {"author": "Аня", "text": "Привет! Кто сделал домашку по алгебре?", "time": "10:16"},
    {"author": "Вова", "text": "Я сделал. А как в HTML сделать текст <b>жирным</b>?", "time": "10:18"},
]

ONLINE = ["Аня", "Боря", "Вова"]


@app.route("/")
def index():
    # render_template находит файл в папке templates/ и подставляет в него данные
    return render_template("index.html", me=ME, messages=MESSAGES, online=ONLINE)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
