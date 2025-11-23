import os

def salvar_dados(nome_arquivo: str) -> None:
    if not os.path.exists(nome_arquivo):
        # Se o arquivo não existe, cria um vazio e retorna lista vazia
        salvar_dados([], nome_arquivo)
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

def carregar_dados(dados: list,nome_arquivo: str) -> bool:
    try:
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
        print(f'Erro ao tentar processar dados para salvar: {e}')
        return []