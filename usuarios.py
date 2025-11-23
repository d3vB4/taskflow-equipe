import uuid # Para gerar IDs únicos
import hashlib # Para hash de senhas
import unicodedata # Para normalização de strings

# Agora armazena múltiplos usuários por id
usuarios = {}

# Arquivo de persistência em texto simples (uma linha por usuário)
# Usamos um nome de arquivo relativo e `open()` para não adicionar imports
USUARIOS_FILE = 'usuarios.txt'


def _escape(field: str) -> str:
    return field.replace('|', '<PIPE>').replace('\n', '<NL>') if field is not None else ''


def _unescape(field: str) -> str:
    return field.replace('<PIPE>', '|').replace('<NL>', '\n') if field is not None else ''


def _save_usuarios_to_file() -> None:
    try:
        with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
            for u in usuarios.values():
                parts = [
                    u.get('id', ''),
                    _escape(u.get('nome', '')),
                    _escape(u.get('email', '')),
                    _escape(u.get('login', '')),
                    _escape(u.get('setor', '') or ''),
                    _escape(u.get('senha', '') or ''),
                    _escape(u.get('data_cadastro', '') or ''),
                ]
                f.write('|'.join(parts) + '\n')
    except Exception:
        # Não propagar exceções de I/O aqui
        pass


def _load_usuarios_from_file() -> None:
    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                parts = line.split('|')
                # Esperamos 7 campos: id, nome, email, login, setor, senha, data_cadastro
                if len(parts) < 7:
                    continue
                id_u, nome, email, login_u, setor, senha_u, data_cadastro = parts[:7]
                usuarios[id_u] = {
                    'id': id_u,
                    'nome': _unescape(nome),
                    'email': _unescape(email),
                    'login': _unescape(login_u),
                    'setor': _unescape(setor) or None,
                    'senha': _unescape(senha_u) or None,
                    'data_cadastro': _unescape(data_cadastro) or None,
                }
    except Exception:
        # Arquivo pode não existir ou estar corrompido; apenas ignoramos
        return


def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome: str | None = None, login: str | None = None, email: str | None = None, senha: str | None = None, setor: str | None = None) -> dict:
    # Solicita os dados do usuário se não fornecidos
    nome = input("Nome: ") if nome is None else nome
    login = input("Login: ") if login is None else login
    email = input("Email: ") if email is None else email
    senha = input("Senha: ") if senha is None else senha
    setor = input("Setor (Recepção, Enfermagem, Médico, Farmácia): ") if setor is None else setor 

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
        'medico': 'médico',
        'farmacia': 'farmácia',
    }
    setor_normalizado = None
    if setor:
        key = _normalize(setor)
        if key not in allowed:
            raise ValueError(f"Setor inválido: {setor}. Opções válidas: {', '.join(allowed.values())}.")
        setor_normalizado = allowed[key]

     # Gera um ID único para o usuário
    novo_id = str(uuid.uuid4())
    # Mantemos campo de data sem usar imports adicionais
    data_cadastro = ''
    novo_usuario = {
        'id': novo_id,
        'nome': nome,
        'email': email,
        'login': login,
        'setor': setor_normalizado,
        'senha': _hash_senha(senha),
        'data_cadastro': data_cadastro,
    }
    usuarios[novo_id] = novo_usuario
    # Persiste em arquivo texto
    _save_usuarios_to_file()
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


def procurar_usuario(campo: str | None = None, termo: str | None = None) -> list[dict]:
 # Procura usuários pelo campo e termo fornecidos. Se `campo` ou `termo` forem None, solicita via `input()` para compatibilidade
    allowed = {'id', 'nome', 'login', 'email', 'setor'}
     # Valida o campo
    if campo is None:
        campo = input(f"Campo para buscar ({', '.join(allowed)}): ").strip().lower()
        # Normaliza o campo
    else:
        campo = campo.strip().lower()

    if campo not in allowed:
        raise ValueError(f"Campo inválido: {campo}. Use um entre: {', '.join(allowed)}")

    if termo is None:
        termo = input("Termo de busca: ").strip()

    termo_norm = termo.lower()
    resultados: list[dict] = []
        # Busca nos usuários

    for u in usuarios.values():
        valor = u.get(campo)
        if valor is None:
            continue
        if campo == 'id':
            if str(valor) == termo:
                resultados.append(u)
        else:
            if termo_norm in str(valor).lower():
                resultados.append(u)

    return resultados
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


# Carrega usuários do arquivo texto ao importar o módulo
_load_usuarios_from_file()


