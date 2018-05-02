from flask import Flask, render_template
from db import get_db, close_db


@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")


@app.route("/enviar", methods=["GET", "POST"])
def envio():
    if request.method == "POST":
        sender = request.form["uEnviador"]
        receiver = request.form["uRecibidor"]
        message = request.form["uContenido"]
        database = get_db()
        database.execute(
            "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
            (sender, receiver, message),
        )
        database.commit()

    return render_template("new_message.html")


@app.route("/leer", methods=["GET", "POST"])
def leer():
    if request.method == "POST":
        user = request.form['user_name']
        database = get_db()
        messages = database.execute(
            "SELECT FROM messages (sender, content) WHERE receiver = ?",
            user
        ).fetchall()
        if messages is None:
            render_template('inbox_select.html', vacio=True)
        else:
            render_template('inbox.html', user=user, messages=messages)
    else:
        render_template('inbox_select.html', vacio=False)


if __name__ == "__main__":
    app.run()
