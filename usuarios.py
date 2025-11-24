import uuid # Para gerar IDs únicos
import hashlib # Para hash de senhas
import unicodedata # Para normalização de strings
import os

# Armazena múltiplos usuários por id
usuarios = {}

# Arquivo de persistência
USUARIOS_FILE = 'usuarios.txt'

# --- FUNÇÕES AUXILIARES DE PERSISTÊNCIA ---
def _escape(field: str) -> str:
    if field is None: return ''
    return str(field).replace('|', '<PIPE>').replace('\n', '<NL>')

def _unescape(field: str) -> str:
    if not field: return ''
    return field.replace('<PIPE>', '|').replace('<NL>', '\n')

# --- FUNÇÕES DE PERSISTÊNCIA ---
def _save_usuarios_to_file() -> None:
    try:
        with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
            for u in usuarios.values():
                parts = [
                    u.get('id', ''),
                    _escape(u.get('nome', '')),
                    _escape(u.get('email', '')),
                    _escape(u.get('login', '')),
                    _escape(u.get('setor', '')),
                    _escape(u.get('senha', '')),
                    _escape(u.get('data_cadastro', '')),
                    _escape(u.get('crm', '')),
                    _escape(u.get('especialidade', '')),
                    _escape(u.get('disponivel', '')),
                ]
                f.write('|'.join(parts) + '\n')
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")

def _load_usuarios_from_file() -> None:
    if not os.path.exists(USUARIOS_FILE):
        return

    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                parts = line.split('|')
                # Garante que temos campos suficientes (mínimo 6 para funcionar login)
                if len(parts) < 6: continue
                
                # Preenche com strings vazias se faltar campo no final da linha
                while len(parts) < 10:
                    parts.append('')

                id_u = parts[0]
                
                usuarios[id_u] = {
                    'id': id_u,
                    'nome': _unescape(parts[1]),
                    'email': _unescape(parts[2]),
                    'login': _unescape(parts[3]),
                    'setor': _unescape(parts[4]),
                    'senha': _unescape(parts[5]),
                    'data_cadastro': _unescape(parts[6]),
                    'crm': _unescape(parts[7]),
                    'especialidade': _unescape(parts[8]),
                    'disponivel': _unescape(parts[9]),
                }
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome: str | None = None, login: str | None = None, email: str | None = None, 
                      senha: str | None = None, setor: str | None = None, 
                      crm: str | None = None, especialidade: str | None = None, 
                      disponivel: bool = True) -> dict:
    
    # Solicita dados com .strip() para evitar erros de espaço
    print("\n--- CADASTRO ---")
    if nome is None: nome = input("Nome: ").strip()
    if login is None: login = input("Login: ").strip()
    if email is None: email = input("Email: ").strip()
    if senha is None: senha = input("Senha: ").strip()
    if setor is None: setor = input("Setor (Recepção, Enfermagem, Médico, Farmácia): ").strip()

    # Validação
    if not all([nome, login, email, senha, setor]):
        raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

    # Normaliza setor
    def _normalize(s: str) -> str:
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower().strip()
    
    allowed = {
        'recepcao': 'recepção',
        'enfermagem': 'enfermagem',
        'medico': 'médico',
        'farmacia': 'farmácia',
        'paciente': 'paciente',
        'admin': 'admin'
    }
    
    key = _normalize(setor)
    setor_normalizado = allowed.get(key, setor) # Usa o que digitou se não achar no mapa

    # Verifica se login já existe
    if buscar_usuario_por_login(login):
        print(f"AVISO: O login '{login}' já está em uso. Atualizando dados...")
        # (Opcional: poderia levantar erro, mas aqui atualiza)

    novo_id = str(uuid.uuid4())
    
    novo_usuario = {
        'id': novo_id,
        'nome': nome,
        'email': email,
        'login': login,
        'setor': setor_normalizado,
        'senha': _hash_senha(senha),
        'data_cadastro': '',
        'crm': crm or '',
        'especialidade': especialidade or '',
        'disponivel': 'true' if disponivel else 'false',
    }
    
    usuarios[novo_id] = novo_usuario
    _save_usuarios_to_file()
    return novo_usuario

def obter_usuario(id_usuario: str) -> dict | None:
    return usuarios.get(id_usuario)

def listar_usuarios() -> list[dict]:
    return list(usuarios.values())

def buscar_usuario_por_login(login: str) -> dict | None:
    if not login: return None
    for u in usuarios.values():
        if u.get('login') == login:
            return u
    return None

def realizar_login(login: str | None = None, senha: str | None = None) -> dict | None:
    if login is None:
        login = input("Login: ").strip()
    if senha is None:
        senha = input("Senha: ").strip()

    usuario = buscar_usuario_por_login(login)
    
    if not usuario:
        # Debug (pode remover depois)
        # print(f"[Debug] Usuário '{login}' não encontrado.")
        return None

    try:
        if _hash_senha(senha) == usuario.get('senha'):
            return usuario
        else:
            # Debug
            # print(f"[Debug] Senha incorreta para '{login}'.")
            return None
    except ValueError:
        return None

def listar_especialidades() -> list[str]:
    especialidades = set()
    for u in usuarios.values():
        if u.get('setor') == 'médico' and u.get('especialidade'):
            especialidades.add(u.get('especialidade'))
    return sorted(list(especialidades))

# Carrega ao iniciar
_load_usuarios_from_file()