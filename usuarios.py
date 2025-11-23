import uuid # Para gerar IDs únicos
import hashlib # Para hash de senhas
import unicodedata # Para normalização de strings

# Agora armazena múltiplos usuários por id
usuarios = {}

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome: str | None = None, login: str | None = None, email: str | None = None, senha: str | None = None, setor: str | None = None) -> dict:
    # Solicita os dados do usuário se não fornecidos
    nome = input("Nome: ") if nome is None else nome
    login = input("Login: ") if login is None else login
    email = input("Email: ") if email is None else email
    senha = input("Senha: ") if senha is None else senha
    setor = input("Setor (Recepçao, Enfermagem, Medico, Farmacia): ") if setor is None else setor 

   # Valida os parâmetros obrigatórios 
   
    missing = [k for k, v in(("nome", nome), ("login", login), ("email", email), ("senha", senha), ("setor", setor)) if not v]
    if missing:
        raise ValueError(
            "Parâmetros ausentes para cadastrar_usuario: "
            f"{', '.join(missing)}. Use cadastrar_usuario(nome, login, email, senha, setor)."
        )

     # Normaliza e valida o setor
    def _normalize(s: str) -> str:
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower().strip()
      ## Validação do setor
    allowed = {
        'recepcao': 'recepção',
        'enfermagem': 'enfermagem',
        'medicos': 'médicos',
        'farmacias': 'farmácias',
    }
    setor_normalizado = None
    if setor:
        key = _normalize(setor)
        if key not in allowed:
            raise ValueError(f"Setor inválido: {setor}. Opções válidas: {', '.join(allowed.values())}.")
        setor_normalizado = allowed[key]

     # Gera um ID único para o usuário
    novo_id = str(uuid.uuid4())
    novo_usuario = {
        'id': novo_id,
        'nome': nome,
        'email': email,
        'login': login,
        'setor': setor_normalizado,
        'senha': _hash_senha(senha),
    }
    usuarios[novo_id] = novo_usuario
    return novo_usuario
     #

def obter_usuario(id_usuario: str) -> dict | None:
    return usuarios.get(id_usuario)

def listar_usuarios() -> list[dict]:
    """Retorna uma lista com todos os usuários cadastrados."""
    return list(usuarios.values())
# --- FUNÇÃO AUXILIAR PARA BUSCAR USUÁRIO PELO LOGIN ---

def buscar_usuario_por_login(login: str) -> dict | None:
    """Retorna o usuário com o `login` informado, ou None se não existir."""
    for u in usuarios.values():
        if u.get('login') == login:
            return u
    return None
# --- FUNÇÃO DE LOGIN ---


def realizar_login(login: str | None = None, senha: str | None = None) -> dict | None:
    """Tenta autenticar o usuário.

    Se `login` ou `senha` forem None, solicita via `input()` para compatibilidade com o fluxo CLI.
    Retorna o dicionário do usuário em caso de sucesso, ou `None` em caso de falha.
    """
    if login is None:
        login = input("Login: ").strip()
    if senha is None:
        senha = input("Senha: ").strip()
        # Busca o usuário pelo login

    usuario = buscar_usuario_por_login(login)
    if not usuario:
        return None
    # Verifica a senha

    try:
        if _hash_senha(senha) == usuario.get('senha'):
            return usuario
    except ValueError:
        # Senha inválida (não numérica, por exemplo)
        return None

    return None


if __name__ == "__main__":
    # Exemplo de cadastro de dois usuários
    cadastrar_usuario("Ana", "ana123", "ana@example.com", "123456", "recepção")
    cadastrar_usuario("Beto", "beto456", "beto@example.com", "654321", "enfermagem")
    print("Usuários cadastrados:")
    for u in listar_usuarios():
        print(u)


