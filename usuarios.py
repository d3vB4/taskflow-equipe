import uuid  # Para gerar IDs únicos
import getpass # Para esconder a senha
import re # Para validar email
from utils import arquivos # Importa o trabalho do Dev 4

# (Card 8) Constante para o nome do arquivo
ARQUIVO_USUARIOS = "usuarios.json"

# --- (Card 11) Funções de Validação ---

def _validar_email(email: str) -> bool:
    """Valida se um email está em um formato básico correto."""
    # Expressão regular simples para validar email
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)

def _validar_login_disponivel(login: str, todos_usuarios: list) -> bool:
    """Verifica se um login já existe na lista de usuários."""
    for u in todos_usuarios:
        if u['login'] == login:
            return False # Não está disponível
    return True # Está disponível

def _buscar_usuario_por_login(login: str, todos_usuarios: list):
    """Busca e retorna um usuário pelo login."""
    for u in todos_usuarios:
        if u['login'] == login:
            return u
    return None

# --- (Card 9) Função de Cadastro ---

def cadastrar_usuario() -> bool:
    """
    Processo completo de cadastro de um novo usuário.
    Pede os dados, valida e salva no JSON.
    """
    print("--- Novo Cadastro ---")
    nome = input("Nome completo: ")
    email = input("Email: ")
    login = input("Login (mín. 4 caracteres): ")
    
    # Validações
    if not nome:
        print("Erro: O nome não pode ficar em branco.")
        return False
        
    if not _validar_email(email):
        print("Erro: Formato de email inválido.")
        return False

    if len(login) < 4:
        print("Erro: O login deve ter pelo menos 4 caracteres.")
        return False

    # (Card 18) Carrega dados usando o módulo de arquivos
    todos_usuarios = arquivos.carregar_dados(ARQUIVO_USUARIOS)
    
    if not _validar_login_disponivel(login, todos_usuarios):
        print("Erro: Este login já está em uso. Tente outro.")
        return False

    # Senha
    senha = getpass.getpass("Senha (mín. 6 caracteres): ")
    if len(senha) < 6:
        print("Erro: A senha deve ter pelo menos 6 caracteres.")
        return False
    senha_confirma = getpass.getpass("Confirme a senha: ")

    if senha != senha_confirma:
        print("Erro: As senhas não coincidem.")
        return False
        
    # (Card 8) Estrutura do usuário
    novo_usuario = {
        "id": str(uuid.uuid4()), # Gera um ID único
        "nome": nome,
        "email": email,
        "login": login,
        "senha": senha, # ATENÇÃO: Em um app real, isso DEVE ser hasheado (ex: hashlib)
        "data_cadastro": str(uuid.uuid4()) # Simula uma data
    }
    
    todos_usuarios.append(novo_usuario)
    
    # (Card 18) Salva dados usando o módulo de arquivos
    if arquivos.salvar_dados(todos_usuarios, ARQUIVO_USUARIOS):
        return True
    else:
        print("Erro: Falha ao salvar o novo usuário.")
        return False

# --- (Card 10) Função de Login ---

def realizar_login():
    """
    Processo de login. Pede credenciais e valida.
    
    Returns:
        dict: O dicionário do usuário logado, se o login for bem-sucedido.
        None: Se o login falhar.
    """
    login = input("Login: ")
    senha = getpass.getpass("Senha: ")

    todos_usuarios = arquivos.carregar_dados(ARQUIVO_USUARIOS)
    
    usuario_encontrado = _buscar_usuario_por_login(login, todos_usuarios)
    
    if usuario_encontrado:
        # ATENÇÃO: Em um app real, compararíamos o hash da senha
        if usuario_encontrado['senha'] == senha:
            # Retorna o dicionário completo do usuário para o main.py
            return usuario_encontrado 
            
    return None # Falha no login (usuário não encontrado ou senha errada)

# --- (Card 12) Funções de Consulta (Opcionais) ---

def buscar_usuario_por_id(user_id: str):
    """Busca e retorna um usuário pelo seu ID."""
    todos_usuarios = arquivos.carregar_dados(ARQUIVO_USUARIOS)
    for u in todos_usuarios:
        if u['id'] == user_id:
            return u
    return None