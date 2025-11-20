def salvar_dados(arquivo_destino: str, lista_dados: list[str]) -> None:
    # Função responsável por escrever a lista no arquivo
    try:
        with open(arquivo_destino, 'w', encoding='utf-8') as f:
            linhas = [dados + '\n' for dados in lista_dados]
            f.writelines(linhas)
        print(f"Dados salvos com sucesso em '{arquivo_destino}'") 
    except IOError as e:
        print(f"Ocorreu um erro ao tentar salvar o arquivo: {e}")

def carregar_dados(arquivo_destino: str) -> list[str]:
    # Lê o arquivo e retorna os dados em uma lista.
    # Retorna lista vazia [] se o arquivo não existir.
    try:
        with open(arquivo_destino, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            listaTarefas = [dados.strip() for dados in linhas if len(dados.strip()) > 0]
        
        print(f"Dados carregados com sucesso de '{arquivo_destino}'")
        return listaTarefas
    
    except FileNotFoundError:
        print(f"O arquivo '{arquivo_destino}' não foi encontrado. Retornando lista vazia.")
        return []
    
    except IOError as e:
        print(f'Erro ao carregar arquivo: {e}')
        return []