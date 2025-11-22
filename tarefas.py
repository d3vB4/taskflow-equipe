from uuid import uuid4
from datetime import datetime

tarefas = []


def _data_atual():
    # Retorna a data atual no formato dd/mm/yyyy.
    return datetime.now().strftime("%d/%m/%Y")



tarefa = {
     "id": "uuid",
     "titulo": "string",
     "descricao": "string",
     "responsavel": "user_id",
     "prazo": "dd/mm/yyyy",
     "status": "pendente|concluida",
     "data_criacao": "dd/mm/yyyy",
     "data_conclusao": "dd/mm/yyyy ou None"
        }

# Funções para manipulação de tarefas

# Função para criar uma nova tarefa
def criar_tarefa(titulo, descricao, responsavel, prazo):
    nova_tarefa = {
        "id": str(uuid4()), # Gera um ID único para a tarefa
        "titulo": titulo,
        "descricao": descricao,
        "responsavel": responsavel,
        "prazo": prazo,
        "status": "pendente",
        "data_criacao": _data_atual(), # Define a data de criação como a data atual
        "data_conclusao": None
    }

    tarefas.append(nova_tarefa) # Adiciona a nova tarefa à lista de tarefas
    return nova_tarefa # Retorna a nova tarefa criada


#Função para listar todas as tarefas
def listar_tarefas(incluir_concluidas=True):
    pass

def editar_tarefa(id_tarefa, **novos_dados):
    pass

def concluir_tarefa(id_tarefa):
    pass

def excluir_tarefa(id_tarefa):
    pass