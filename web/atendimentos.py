"""
Módulo de gerenciamento de atendimentos
"""

import json
import os
from datetime import datetime
from uuid import uuid4

ARQUIVO_ATENDIMENTOS = "atendimentos.json"


def _carregar_atendimentos():
    """Carrega todos os atendimentos do arquivo JSON."""
    if not os.path.exists(ARQUIVO_ATENDIMENTOS):
        return []
    
    try:
        with open(ARQUIVO_ATENDIMENTOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def _salvar_atendimentos(atendimentos):
    """Salva todos os atendimentos no arquivo JSON."""
    try:
        with open(ARQUIVO_ATENDIMENTOS, 'w', encoding='utf-8') as f:
            json.dump(atendimentos, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False


def _gerar_senha():
    """Gera uma senha numérica sequencial para o atendimento."""
    atendimentos = _carregar_atendimentos()
    
    # Atendimentos de hoje
    hoje = datetime.now().strftime("%d/%m/%Y")
    atendimentos_hoje = [a for a in atendimentos if a.get('data_checkin', '').startswith(hoje)]
    
    # Próximo número
    return len(atendimentos_hoje) + 1


def criar_atendimento(cpf, nome_paciente, medico_id, especialidade):
    """
    Cria um novo atendimento.
    
    Returns:
        dict: Dados do atendimento criado
    """
    atendimentos = _carregar_atendimentos()
    
    token = str(uuid4())
    senha = _gerar_senha()
    
    # Calcula posição na fila (atendimentos aguardando + em atendimento)
    atendimentos_ativos = [
        a for a in atendimentos 
        if a.get('status') in ['aguardando', 'em_atendimento']
    ]
    posicao_fila = len(atendimentos_ativos) + 1
    
    novo_atendimento = {
        'token': token,
        'senha': f"{senha:03d}",  # Formato: 001, 002, etc
        'cpf': cpf,
        'nome_paciente': nome_paciente,
        'medico_id': medico_id,
        'especialidade': especialidade,
        'data_checkin': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'status': 'aguardando',
        'etapa_atual': 'recepcao',
        'posicao_fila': str(posicao_fila)
    }
    
    atendimentos.append(novo_atendimento)
    _salvar_atendimentos(atendimentos)
    
    return novo_atendimento


def obter_atendimento(token):
    """
    Busca um atendimento pelo token.
    
    Args:
        token: Token único do atendimento
    
    Returns:
        dict: Dados do atendimento ou None se não encontrado
    """
    atendimentos = _carregar_atendimentos()
    
    for atendimento in atendimentos:
        if atendimento.get('token') == token:
            return atendimento
    
    return None


def atualizar_status_atendimento(token, status, etapa_atual):
    """
    Atualiza o status e etapa atual de um atendimento.
    
    Args:
        token: Token do atendimento
        status: Novo status (aguardando, em_atendimento, concluido)
        etapa_atual: Etapa atual (recepcao, medico, farmacia, enfermagem, concluido)
    """
    atendimentos = _carregar_atendimentos()
    
    for atendimento in atendimentos:
        if atendimento.get('token') == token:
            atendimento['status'] = status
            atendimento['etapa_atual'] = etapa_atual
            
            if status == 'concluido':
                atendimento['data_conclusao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            break
    
    _salvar_atendimentos(atendimentos)


def calcular_tempo_estimado(posicao_fila):
    """
    Calcula o tempo estimado de atendimento baseado na posição da fila.
    
    Args:
        posicao_fila: Posição na fila (int)
    
    Returns:
        str: Tempo estimado formatado
    """
    # Estimativa: 15 minutos por pessoa
    minutos = posicao_fila * 15
    
    if minutos < 60:
        return f"{minutos} minutos"
    else:
        horas = minutos // 60
        mins = minutos % 60
        if mins == 0:
            return f"{horas}h"
        return f"{horas}h {mins}min"


def listar_atendimentos_ativos():
    """
    Lista todos os atendimentos que não foram concluídos.
    
    Returns:
        list: Lista de atendimentos ativos
    """
    atendimentos = _carregar_atendimentos()
    return [
        a for a in atendimentos 
        if a.get('status') != 'concluido'
    ]


def recalcular_fila():
    """
    Recalcula a posição na fila de todos os atendimentos ativos.
    """
    atendimentos = _carregar_atendimentos()
    atendimentos_ativos = [
        a for a in atendimentos 
        if a.get('status') in ['aguardando', 'em_atendimento']
    ]
    
    # Ordena por data de check-in
    atendimentos_ativos.sort(key=lambda x: x.get('data_checkin', ''))
    
    # Atualiza posições
    for i, atendimento in enumerate(atendimentos_ativos, 1):
        for a in atendimentos:
            if a.get('token') == atendimento.get('token'):
                a['posicao_fila'] = str(i)
                break
    
    _salvar_atendimentos(atendimentos)