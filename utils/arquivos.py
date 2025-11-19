import json
import os

# (Card 18) Módulo de Persistência JSON

def carregar_dados(nome_arquivo: str) -> list:
    """
    Carrega uma lista de dados de um arquivo JSON.

    Args:
        nome_arquivo (str): O nome do arquivo (ex: 'usuarios.json').

    Returns:
        list: Uma lista de dicionários com os dados.
              Retorna uma lista vazia se o arquivo não for encontrado
              ou se contiver um JSON inválido.
    """
    if not os.path.exists(nome_arquivo):
        # Se o arquivo não existe, cria um vazio e retorna lista vazia
        salvar_dados([], nome_arquivo)
        return []
        
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Garante que sempre retornamos uma lista
            return dados if isinstance(dados, list) else []
    except json.JSONDecodeError:
        print(f"Aviso: Arquivo '{nome_arquivo}' está corrompido ou vazio. Iniciando com dados limpos.")
        return [] # Retorna lista vazia se o JSON for inválido
    except IOError as e:
        print(f"Erro ao carregar o arquivo {nome_arquivo}: {e}")
        return []

def salvar_dados(dados: list, nome_arquivo: str) -> bool:
    """
    Salva uma lista de dados em um arquivo JSON.

    Args:
        dados (list): A lista de dicionários a ser salva.
        nome_arquivo (str): O nome do arquivo (ex: 'usuarios.json').

    Returns:
        bool: True se os dados foram salvos, False se ocorreu um erro.
    """
    try:
        # 'w' (write) apaga o conteúdo anterior e escreve o novo
        # 'indent=4' formata o JSON para ficar legível
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Erro ao salvar dados em {nome_arquivo}: {e}")
        return False
    except TypeError as e:
        print(f"Erro de tipo ao tentar salvar dados: {e}")
        return False