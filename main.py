from fastapi import FastAPI
from model import Alunos
from database import Database

app = FastAPI()

@app.post('/alunos/')
def cadastrar(alunos: Alunos):
    with Database() as db:
        sql = "INSERT INTO alunos (nome_aluno, data_horario) VALUES (%s, %s)"
        db.executar(sql, (alunos.nome_aluno, alunos.data_horario))
    return {"mensagem": "Presença registrada com sucesso!", "alunos": alunos}