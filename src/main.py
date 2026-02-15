import os
from flask import Flask, render_template
from src.api.routes import api
from src.obd.obd_reader import start_obd_reader
from src.ai.online_trainer import start_online_training

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.register_blueprint(api, url_prefix="/api")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    start_online_training()
    start_obd_reader()
    app.run(host="0.0.0.0", port=5000, debug=False)
