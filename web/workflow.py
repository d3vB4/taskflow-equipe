"""
Módulo de gerenciamento de workflow de atendimentos
"""

import sys
import os
from uuid import uuid4

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tarefas


def criar_workflow_automatico(atendimento_token, nome_paciente, medico_id, medico_nome):
    """
    Cria o workflow inicial.
    ALTERAÇÃO: Cria apenas a tarefa de Recepção como PENDENTE.
    O médico só será acionado após a validação da recepção.
    """
    todas_tarefas = tarefas._carregar_tarefas()
    
    # 1. Tarefa de Recepção (Check-in Pendente)
    tarefa_recepcao = {
        "id": str(uuid4()),
        "titulo": f"Recepção - {nome_paciente}",
        "descricao": f"Check-in realizado. Validar dados e encaminhar para Dr(a) {medico_nome}.",
        "responsavel": "sistema",
        "setor": "recepção",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_PENDENTE,  # AGORA É PENDENTE
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": None,
        "atendimento_token": atendimento_token
    }
    
    todas_tarefas.append(tarefa_recepcao)
    tarefas._salvar_tarefas(todas_tarefas)


def adicionar_tarefa_medico(atendimento_token, nome_paciente, especialidade, responsavel_id=None):
    """
    Adiciona tarefa do médico ao workflow.
    Aceita um responsavel_id específico agora.
    """
    todas_tarefas = tarefas._carregar_tarefas()
    
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": f"Consulta - {nome_paciente}",
        "descricao": f"Consulta médica em {especialidade}",
        "responsavel": responsavel_id if responsavel_id else "sistema", # Usa o médico específico se houver
        "setor": "médico",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_PENDENTE,
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": None,
        "atendimento_token": atendimento_token
    }
    
    todas_tarefas.append(nova_tarefa)
    tarefas._salvar_tarefas(todas_tarefas)


def adicionar_tarefa_farmacia(atendimento_token, nome_paciente):
    """Adiciona tarefa da farmácia ao workflow."""
    todas_tarefas = tarefas._carregar_tarefas()
    
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": f"Farmácia - {nome_paciente}",
        "descricao": f"Separação e dispensação de medicamentos para {nome_paciente}",
        "responsavel": "sistema",
        "setor": "farmácia",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_PENDENTE,
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": None,
        "atendimento_token": atendimento_token
    }
    
    todas_tarefas.append(nova_tarefa)
    tarefas._salvar_tarefas(todas_tarefas)


def adicionar_tarefa_enfermagem(atendimento_token, nome_paciente):
    """Adiciona tarefa da enfermagem ao workflow."""
    todas_tarefas = tarefas._carregar_tarefas()
    
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": f"Enfermagem - {nome_paciente}",
        "descricao": f"Administração de medicamentos e cuidados finais para {nome_paciente}",
        "responsavel": "sistema",
        "setor": "enfermagem",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_PENDENTE,
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": None,
        "atendimento_token": atendimento_token
    }
    
    todas_tarefas.append(nova_tarefa)
    tarefas._salvar_tarefas(todas_tarefas)


def obter_tarefas_atendimento(atendimento_token):
    todas_tarefas = tarefas._carregar_tarefas()
    
    tarefas_atendimento = [
        t for t in todas_tarefas 
        if t.get('atendimento_token') == atendimento_token
    ]
    
    ordem_setores = {'recepção': 1, 'recepcao': 1, 'médico': 2, 'medico': 2, 'farmácia': 3, 'farmacia': 3, 'enfermagem': 4}
    tarefas_atendimento.sort(key=lambda x: ordem_setores.get(x.get('setor', '').lower(), 99))
    
    return tarefas_atendimento


def calcular_progresso(atendimento_token):
    tarefas_atendimento = obter_tarefas_atendimento(atendimento_token)
    if not tarefas_atendimento: return 0
    
    # Se só tem recepção pendente, progresso é baixo
    if len(tarefas_atendimento) == 1 and tarefas_atendimento[0]['status'] != tarefas.STATUS_CONCLUIDA:
        return 10

    total = len(tarefas_atendimento)
    concluidas = len([t for t in tarefas_atendimento if t.get('status') == tarefas.STATUS_CONCLUIDA])
    return int((concluidas / total) * 100)


def obter_etapa_atual(atendimento_token):
    tarefas_atendimento = obter_tarefas_atendimento(atendimento_token)
    for tarefa in tarefas_atendimento:
        if tarefa.get('status') == tarefas.STATUS_PENDENTE:
            return tarefa.get('setor', '').lower()
    return 'concluido'