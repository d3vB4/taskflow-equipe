import uuid
import hashlib
import unicodedata

usuario = {}

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome: str | None = None, login: str | None = None, email: str | None = None, senha: str | None = None, setor: str | None = None) -> bool:

    nome = input("Nome: ") if nome is None else nome
    login = input("Login: ") if login is None else login
    email = input("Email: ") if email is None else email
    senha = input("Senha: ") if senha is None else senha
    setor = input("Setor (Recepção, Enfermagem, Médicos, Farmácias): ") if setor is None else setor 


   
    missing = [k for k, v in(("nome", nome), ("login", login), ("email", email), ("senha", senha), ("setor", setor)) if not v]
    if missing:
        raise ValueError(
            "Parâmetros ausentes para cadastrar_usuario: "
            f"{', '.join(missing)}. Use cadastrar_usuario(nome, login, email, senha, setor)."
        )

  
    def _normalize(s: str) -> str:
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower().strip()

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

 
    novo_id = str(uuid.uuid4())

   
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

def obter_usuario() -> dict:
    return usuario

if __name__ == "__main__":
    exemplo = cadastrar_usuario("Ana", "ana123", "ana@example.com", "senha123")
    print(exemplo)

