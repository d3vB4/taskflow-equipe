"""
Modelo de Médico
Gerencia cadastro e disponibilidade de médicos
"""

import os
import sys

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils import arquivos

MEDICOS_FILE = 'medicos.txt'

# Especialidades disponíveis
ESPECIALIDADES = [
    "Cardiologia",
    "Pediatria",
    "Clínico Geral",
    "Ortopedia",
    "Dermatologia",
    "Ginecologia",
    "Oftalmologia",
    "Otorrinolaringologia"
]


def listar_medicos_disponiveis(especialidade=None):
    """
    Lista médicos disponíveis, opcionalmente filtrados por especialidade
    
    Args:
        especialidade: Filtrar por especialidade (opcional)
        
    Returns:
        Lista de dicionários com dados dos médicos
    """
    medicos = arquivos.carregar_dados(MEDICOS_FILE)
    
    # Filtra apenas disponíveis
    medicos_disponiveis = [m for m in medicos if m.get('disponivel') == 'true']
    
    # Filtra por especialidade se fornecida
    if especialidade:
        medicos_disponiveis = [
            m for m in medicos_disponiveis 
            if m.get('especialidade') == especialidade
        ]
    
    return medicos_disponiveis


def obter_medico(medico_id):
    """
    Busca médico por ID
    
    Args:
        medico_id: ID do médico
        
    Returns:
        Dicionário com dados do médico ou None
    """
    medicos = arquivos.carregar_dados(MEDICOS_FILE)
    
    for medico in medicos:
        if medico.get('id') == medico_id:
            return medico
    
    return None


def cadastrar_medico(nome, especialidade, crm, disponivel=True):
    """
    Cadastra novo médico
    
    Args:
        nome: Nome completo do médico
        especialidade: Especialidade médica
        crm: Número do CRM
        disponivel: Se está disponível para atendimento
        
    Returns:
        Dicionário com dados do médico criado
    """
    from uuid import uuid4
    
    medicos = arquivos.carregar_dados(MEDICOS_FILE)
    
    novo_medico = {
        'id': str(uuid4())[:8],  # ID curto
        'nome': nome,
        'especialidade': especialidade,
        'crm': crm,
        'disponivel': 'true' if disponivel else 'false'
    }
    
    medicos.append(novo_medico)
    arquivos.salvar_dados(medicos, MEDICOS_FILE)
    
    return novo_medico


def atualizar_disponibilidade(medico_id, disponivel):
    """
    Atualiza disponibilidade do médico
    
    Args:
        medico_id: ID do médico
        disponivel: True ou False
        
    Returns:
        True se atualizou, False se não encontrou
    """
    medicos = arquivos.carregar_dados(MEDICOS_FILE)
    
    for medico in medicos:
        if medico.get('id') == medico_id:
            medico['disponivel'] = 'true' if disponivel else 'false'
            arquivos.salvar_dados(medicos, MEDICOS_FILE)
            return True
    
    return False


def criar_medicos_exemplo():
    """Cria médicos de exemplo para demonstração"""
    medicos_exemplo = [
        {
            'id': 'med001',
            'nome': 'Dr. Carlos Silva',
            'especialidade': 'Cardiologia',
            'crm': '12345-SP',
            'disponivel': 'true'
        },
        {
            'id': 'med002',
            'nome': 'Dra. Ana Santos',
            'especialidade': 'Pediatria',
            'crm': '67890-SP',
            'disponivel': 'true'
        },
        {
            'id': 'med003',
            'nome': 'Dr. João Oliveira',
            'especialidade': 'Clínico Geral',
            'crm': '11111-SP',
            'disponivel': 'true'
        },
        {
            'id': 'med004',
            'nome': 'Dra. Maria Costa',
            'especialidade': 'Ortopedia',
            'crm': '22222-SP',
            'disponivel': 'true'
        },
        {
            'id': 'med005',
            'nome': 'Dr. Pedro Alves',
            'especialidade': 'Dermatologia',
            'crm': '33333-SP',
            'disponivel': 'false'
        }
    ]
    
    arquivos.salvar_dados(medicos_exemplo, MEDICOS_FILE)
    return medicos_exemplo
