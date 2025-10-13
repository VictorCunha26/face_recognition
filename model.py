
import datetime
from pydantic import BaseModel

class Alunos(BaseModel):
    id_aluno : str
    nome_aluno : str
    data_horario : datetime