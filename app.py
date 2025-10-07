# app.py
from flask import Flask, render_template, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')  # estática servida pelo Flask

@app.route("/reconhecer")
def reconhecer():
    subprocess.Popen(["python", "identificar.py"])
    return jsonify({"status": "iniciado"})

app.run(port=5000)
