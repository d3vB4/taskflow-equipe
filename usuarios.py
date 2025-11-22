import uuid # Para gerar IDs únicos
import hashlib # Para hash de senhas
import unicodedata # Para normalização de strings

usuario = {}

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome: str | None = None, login: str | None = None, email: str | None = None, senha: str | None = None, setor: str | None = None) -> bool:
    # Solicita os dados do usuário se não fornecidos
    nome = input("Nome: ") if nome is None else nome
    login = input("Login: ") if login is None else login
    email = input("Email: ") if email is None else email
    senha = input("Senha: ") if senha is None else senha
    setor = input("Setor (Recepção, Enfermagem, Médicos, Farmácias): ") if setor is None else setor 

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

    # Cria o dicionário do novo usuário
    novo_usuario = {
        'id': novo_id,
        'nome': nome,
        'email': email,
        'login': login,
        'setor': setor_normalizado,
        'senha': _hash_senha(senha),
    }

    usuario.clear()
    usuario.update(novo_usuario)

    return novo_usuario
     #
def obter_usuario() -> bool:
    return usuario


