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
    dados_row = []  # Lista temporária para os objetos Row
    dados_dict = [] # Lista final de dicionários
    
    db.conectar()
    try:
        # 1. Executa a busca (retorna objetos sqlite3.Row)
        dados_row = db.executar("SELECT nome_aluno, data_horario FROM alunos")
        
        if dados_row:
            # 2. CONVERSÃO: Converte cada Row para um dicionário Python padrão
            for row in dados_row:
                dados_dict.append(dict(row))
        
        # 'dados_dict' é a lista que será usada no template
        
    except Exception as e:
        dados_dict = [] # Garante que, em caso de erro, a lista seja vazia
        print(f"Erro ao buscar alunos: {e}")
        
    finally:
        db.desconectar()

    # Passa a lista de dicionários convertidos
    return render_template('alunos.html', alunos=dados_dict)

app.run(port=5000)