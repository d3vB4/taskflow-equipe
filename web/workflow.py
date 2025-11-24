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
    Cria o workflow completo de 4 tarefas automaticamente.
    
    Args:
        atendimento_token: Token do atendimento
        nome_paciente: Nome do paciente
        medico_id: ID do médico
        medico_nome: Nome do médico
    """
    # Carrega tarefas existentes
    todas_tarefas = tarefas._carregar_tarefas()
    
    # 1. Tarefa de Recepção (já criada automaticamente)
    tarefa_recepcao = {
        "id": str(uuid4()),
        "titulo": f"Recepção - {nome_paciente}",
        "descricao": f"Check-in do paciente {nome_paciente}. Aguardando confirmação da recepção.",
        "responsavel": "sistema",
        "setor": "recepção",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_CONCLUIDA,  # Já concluída no check-in
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": tarefas._data_atual(),
        "atendimento_token": atendimento_token
    }
    
    # 2. Tarefa do Médico
    tarefa_medico = {
        "id": str(uuid4()),
        "titulo": f"Consulta Médica - {nome_paciente}",
        "descricao": f"Atendimento médico com {medico_nome}. Aguardando consulta.",
        "responsavel": medico_id,
        "setor": "médico",
        "prazo": tarefas._data_atual(),
        "status": tarefas.STATUS_PENDENTE,
        "data_criacao": tarefas._data_atual(),
        "data_conclusao": None,
        "atendimento_token": atendimento_token
    }
    
    # Adiciona as tarefas iniciais
    todas_tarefas.extend([tarefa_recepcao, tarefa_medico])
    tarefas._salvar_tarefas(todas_tarefas)


def adicionar_tarefa_medico(atendimento_token, nome_paciente, especialidade):
    """Adiciona tarefa do médico ao workflow."""
    todas_tarefas = tarefas._carregar_tarefas()
    
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": f"Consulta - {nome_paciente}",
        "descricao": f"Consulta médica em {especialidade}",
        "responsavel": "sistema",
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
    """
    Retorna todas as tarefas de um atendimento específico.
    
    Args:
        atendimento_token: Token do atendimento
    
    Returns:
        list: Lista de tarefas do atendimento
    """
    todas_tarefas = tarefas._carregar_tarefas()
    
    tarefas_atendimento = [
        t for t in todas_tarefas 
        if t.get('atendimento_token') == atendimento_token
    ]
    
    # Ordena por ordem de criação (setor)
    ordem_setores = {
        'recepção': 1,
        'recepcao': 1,
        'médico': 2,
        'medico': 2,
        'farmácia': 3,
        'farmacia': 3,
        'enfermagem': 4
    }
    
    tarefas_atendimento.sort(key=lambda x: ordem_setores.get(x.get('setor', '').lower(), 99))
    
    return tarefas_atendimento


def calcular_progresso(atendimento_token):
    """
    Calcula o progresso percentual do atendimento.
    
    Args:
        atendimento_token: Token do atendimento
    
    Returns:
        int: Percentual de conclusão (0-100)
    """
    tarefas_atendimento = obter_tarefas_atendimento(atendimento_token)
    
    if not tarefas_atendimento:
        return 0
    
    total = len(tarefas_atendimento)
    concluidas = len([t for t in tarefas_atendimento if t.get('status') == tarefas.STATUS_CONCLUIDA])
    
    return int((concluidas / total) * 100)


def obter_etapa_atual(atendimento_token):
    """
    Retorna a etapa atual do atendimento.
    
    Args:
        atendimento_token: Token do atendimento
    
    Returns:
        str: Nome da etapa atual (recepcao, medico, farmacia, enfermagem, concluido)
    """
    tarefas_atendimento = obter_tarefas_atendimento(atendimento_token)
    
    # Procura a primeira tarefa pendente
    for tarefa in tarefas_atendimento:
        if tarefa.get('status') == tarefas.STATUS_PENDENTE:
            return tarefa.get('setor', '').lower()
    
    # Se todas estão concluídas
    return 'concluido'


def obter_proxima_tarefa_pendente(usuario_setor):
    """
    Retorna a próxima tarefa pendente para um setor específico.
    
    Args:
        usuario_setor: Setor do usuário (médico, farmácia, enfermagem)
    
    Returns:
        dict: Tarefa pendente ou None
    """
    todas_tarefas = tarefas._carregar_tarefas()
    
    # Normaliza o setor
    setor_normalizado = usuario_setor.lower()
    
    # Filtra tarefas pendentes do setor
    tarefas_pendentes = [
        t for t in todas_tarefas 
        if t.get('setor', '').lower() == setor_normalizado 
        and t.get('status') == tarefas.STATUS_PENDENTE
        and t.get('atendimento_token')  # Só tarefas do workflow
    ]
    
    # Ordena por data de criação
    tarefas_pendentes.sort(key=lambda x: x.get('data_criacao', ''))
    
    return tarefas_pendentes[0] if tarefas_pendentes else None