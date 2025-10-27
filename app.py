# app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for
import subprocess
from flask_cors import CORS
from database import Database
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')  # estática servida pelo Flask

@app.route("/reconhecer")
def reconhecer():
    subprocess.Popen(["python", "identificar.py"])
    return jsonify({"status": "iniciado"})

# UPLOAD DE IMAGE

UPLOAD_FOLDER = 'faces'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Criando a pasta se ela não existir

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#ROTA

@app.route('/upload', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo selecionado", 400

    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return f"Arquivo {file.filename} salvo em faces/"


@app.route('/alunos')
def alunos():
    db = Database()
    db.conectar()
    try:
        dados = db.executar("SELECT nome_aluno, data_horario FROM alunos")
    except Exception as e:
        dados = []
        print(f"Erro ao buscar alunos: {e}")
    finally:
        db.desconectar()

    return render_template('alunos.html', alunos=dados)

app.run(port=5000)