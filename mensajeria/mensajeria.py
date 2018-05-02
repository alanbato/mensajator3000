# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "mensajeria.sqlite")
)
test_config = None
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile("config.py", silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")


@app.route("/enviar", methods=["GET", "POST"])
def envio():
    if request.method == "POST":
        data = request.get_json(force=True, silent=True)
        sender = data["uEnviador"]
        receiver = data["uRecibidor"]
        message = data["uContenido"]
        response = {"status": "success"}
        try:
            database = db.get_db()
            database.execute(
                "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
                (sender, receiver, message),
            )
            database.commit()
        except:
            raise

            response["status"] = "error"
        return jsonify(response)

    else:
        return render_template("new_message.html")


@app.route("/leer", methods=["GET", "POST"])
def leer():
    if request.method == "POST":
        user = request.form["user_name"]
        print(user)
        database = db.get_db()
        messages = database.execute(
            "SELECT sender, content FROM messages WHERE receiver = ?", (user,)
        ).fetchall()
        if messages:
            return render_template("inbox.html", user=user, messages=messages)

        else:
            return render_template("inbox_select.html", vacio=True)

    else:
        return render_template("inbox_select.html", vacio=False)


db.init_app(app)

if __name__ == "__main__":
    app.run()
