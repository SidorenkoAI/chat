"""Чат без JavaScript: сообщения отправляются обычной HTML-формой."""

import threading
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

MAX_NAME = 30
MAX_TEXT = 500
MAX_MESSAGES = 50  # храним и показываем только последние сообщения

# Сообщения живут в памяти программы: после перезапуска сайта чат пустой.
messages = []
# Каждый запрос Flask обслуживает в своём потоке. Если два человека отправят
# сообщение одновременно, два потока полезут в один список — нужен замок (урок 3).
lock = threading.Lock()


def render_chat(name="", text="", error=None, status=200):
    """Страница чата. name и text — что подставить в поля формы."""
    with lock:
        shown = list(messages)  # копия: шаблон будет читать её уже без замка
    return render_template("index.html", messages=shown, name=name, text=text, error=error), status


@app.route("/")
def index():
    # Имя приходит в адресе: /?name=Аня — его подставит redirect после отправки
    return render_chat(name=request.args.get("name", ""))


@app.route("/send", methods=["POST"])
def send():
    # Данные формы: request.form — «почти словарь» {имя поля: что в нём написано}
    name = request.form.get("name", "").strip()
    text = request.form.get("text", "").strip()

    # Браузер проверяет required сам, но запрос можно отправить и в обход формы.
    # Поэтому проверяем ещё раз на сервере.
    if not name or not text:
        return render_chat(name, text, error="Нужно написать имя и сообщение", status=400)
    if len(name) > MAX_NAME:
        return render_chat(name, text, error=f"Имя длиннее {MAX_NAME} символов", status=400)

    with lock:
        messages.append({"author": name, "text": text, "time": datetime.now().strftime("%H:%M")})
        del messages[:-MAX_MESSAGES]  # оставить только последние MAX_MESSAGES

    # После POST — перенаправление на обычную страницу чата (см. «POST → redirect → GET»)
    return redirect(url_for("index", name=name))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
