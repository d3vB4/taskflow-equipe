import os

# (Card 18) Módulo de Persistência TXT

def carregar_dados(nome_arquivo: str) -> list:
    """
    Carrega uma lista de dados de um arquivo TXT.
    Cada linha representa um registro no formato: campo1|campo2|campo3|...

    Args:
        nome_arquivo (str): O nome do arquivo (ex: 'usuarios.txt').

    Returns:
        list: Uma lista de dicionários com os dados.
              Retorna uma lista vazia se o arquivo não for encontrado.
    """
    if not os.path.exists(nome_arquivo):
        # Se o arquivo não existe, retorna lista vazia sem criar o arquivo
        return []
        
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        if not linhas:
            return []
        
        # A primeira linha contém os cabeçalhos (nomes dos campos)
        cabecalhos = linhas[0].strip().split('|')
        
        dados = []
        # Cada linha seguinte é um registro
        for linha in linhas[1:]:
            linha = linha.strip()
            if not linha:  # Ignora linhas vazias
                continue
                
            valores = linha.split('|')
            
            # Cria um dicionário com os cabeçalhos e valores
            registro = {}
            for i, cabecalho in enumerate(cabecalhos):
                if i < len(valores):
                    # Converte 'None' string para None real
                    registro[cabecalho] = None if valores[i] == 'None' else valores[i]
                else:
                    registro[cabecalho] = None
            
            dados.append(registro)
        
        return dados
        
    except IOError as e:
        print(f"Erro ao carregar o arquivo {nome_arquivo}: {e}")
        return []
    except Exception as e:
        print(f"Erro ao processar o arquivo {nome_arquivo}: {e}")
        return []

def salvar_dados(dados: list, nome_arquivo: str) -> bool:
    """
    Salva uma lista de dados em um arquivo TXT.
    Cada linha representa um registro no formato: campo1|campo2|campo3|...

    Args:
        dados (list): A lista de dicionários a ser salva.
        nome_arquivo (str): O nome do arquivo (ex: 'usuarios.txt').

    Returns:
        bool: True se os dados foram salvos, False se ocorreu um erro.
    """
    try:
        # Validação de entrada
        if not isinstance(dados, list):
            print(f"Erro: dados deve ser uma lista, recebido {type(dados)}")
            return False
            
        if not isinstance(nome_arquivo, str):
            print(f"Erro: nome_arquivo deve ser string, recebido {type(nome_arquivo)}")
            return False
        
        if not dados:
            # Se a lista está vazia, cria apenas o arquivo vazio
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                pass
            return True
        
        # Pega os cabeçalhos (chaves) do primeiro registro
        cabecalhos = list(dados[0].keys())
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            # Escreve a linha de cabeçalho
            f.write('|'.join(cabecalhos) + '\n')
            
            # Escreve cada registro
            for registro in dados:
                valores = []
                for cabecalho in cabecalhos:
                    valor = registro.get(cabecalho, 'None')
                    # Converte None para string 'None'
                    valores.append(str(valor) if valor is not None else 'None')
                
                f.write('|'.join(valores) + '\n')
        
        return True
        
    except IOError as e:
        print(f"Erro ao salvar dados em {nome_arquivo}: {e}")
        return False
    except Exception as e:
        print(f"Erro ao processar dados para salvar: {e}")
        import traceback
        traceback.print_exc()
        return False