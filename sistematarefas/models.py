from sistematarefas import database
from datetime import datetime

class Tarefas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_tarefa = database.Column(database.String, unique=True, nullable=False)
    custo = database.Column(database.Float, nullable=False)
    data_limite = database.Column(database.DateTime, nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.nome_tarefa}>'