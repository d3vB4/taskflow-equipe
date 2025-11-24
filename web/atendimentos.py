import os
import json
from datetime import datetime
from uuid import uuid4

ARQUIVO_ATENDIMENTOS = "atendimentos.txt"

def _carregar_atendimentos():
    if not os.path.exists(ARQUIVO_ATENDIMENTOS):
        return []
    try:
        with open(ARQUIVO_ATENDIMENTOS, 'r', encoding='utf-8') as f:
            return [json.loads(linha) for linha in f if linha.strip()]
    except:
        return []

def _salvar_atendimento(dados):
    with open(ARQUIVO_ATENDIMENTOS, 'a', encoding='utf-8') as f:
        f.write(json.dumps(dados) + '\n')

def criar_atendimento(cpf, nome_paciente, medico_id, especialidade):
    atendimentos = _carregar_atendimentos()
    hoje = datetime.now().strftime('%Y%m%d')
    
    # Gera senha sequencial diária
    sequencia = len([a for a in atendimentos if a.get('data_checkin', '').startswith(datetime.now().strftime('%d/%m/%Y'))]) + 1
    senha = f"{hoje[-4:]}-{sequencia:03d}"
    
    token = str(uuid4())
    
    novo = {
        'token': token,
        'senha': senha,
        'cpf': cpf,
        'nome_paciente': nome_paciente,
        'medico_id': medico_id,
        'especialidade': especialidade,
        'data_checkin': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'status': 'em_andamento',
        'posicao_fila': sequencia # Simplificação
    }
    
    _salvar_atendimento(novo)
    return novo

def obter_atendimento(token):
    atendimentos = _carregar_atendimentos()
    for a in atendimentos:
        if a['token'] == token:
            return a
    return None

def atualizar_status_atendimento(token, status, etapa):
    # Em um sistema real com BD SQL seria update. 
    # Com TXT append-only, não vamos reescrever tudo para simplificar o exemplo.
    pass

def calcular_tempo_estimado(posicao):
    # Lógica fictícia: 15 min por pessoa na frente
    return f"{posicao * 15} minutos"