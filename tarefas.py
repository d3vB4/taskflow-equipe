import uuid
import datetime
from utils import arquivos # Importa o trabalho do Dev 4

# (Card 13) Constante para o nome do arquivo
ARQUIVO_TAREFAS = "tarefas.json"

# (Card 13) Constantes de Status
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"

# --- Funções Auxiliares ---

def _validar_data(data_str: str) -> bool:
    """Valida se uma string está no formato DD/MM/AAAA."""
    try:
        datetime.datetime.strptime(data_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def _hoje_str() -> str:
    """Retorna a data de hoje formatada como DD/MM/AAAA."""
    return datetime.date.today().strftime('%d/%m/%Y')

def _buscar_tarefa_por_id(tarefa_id: str, todas_tarefas: list):
    """Busca e retorna uma tarefa pelo ID."""
    for t in todas_tarefas:
        if t['id'] == tarefa_id:
            return t
    return None

def _imprimir_tarefa(tarefa: dict):
    """Imprime os detalhes de uma única tarefa formatada."""
    print("---------------------------------")
    print(f"ID: {tarefa['id'][:8]}...") # Mostra só os 8 primeiros chars do ID
    print(f"Título: {tarefa['titulo']}")
    print(f"Descrição: {tarefa['descricao']}")
    print(f"Prazo: {tarefa['prazo']}")
    print(f"Status: {tarefa['status']}")
    print(f"Criada em: {tarefa['data_criacao']}")
    if tarefa['status'] == STATUS_CONCLUIDA:
        print(f"Concluída em: {tarefa['data_conclusao']}")

# --- (Card 14) Criar Tarefa ---

def cadastrar_tarefa(usuario_logado: dict):
    """Processo de criação de uma nova tarefa para o usuário logado."""
    print("\n--- Criar Nova Tarefa ---")
    titulo = input("Título da tarefa: ")
    descricao = input("Descrição: ")
    prazo = input("Prazo (DD/MM/AAAA): ")

    if not (titulo and descricao and prazo):
        print("Erro: Título, descrição e prazo são obrigatórios.")
        return
        
    if not _validar_data(prazo):
        print("Erro: Formato de data inválido. Use DD/MM/AAAA.")
        return

    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    
    # (Card 13) Estrutura da Tarefa
    nova_tarefa = {
        "id": str(uuid.uuid4()),
        "titulo": titulo,
        "descricao": descricao,
        "responsavel": usuario_logado['id'], # Linka a tarefa ao ID do usuário
        "prazo": prazo,
        "status": STATUS_PENDENTE,
        "data_criacao": _hoje_str(),
        "data_conclusao": None
    }
    
    todas_tarefas.append(nova_tarefa)
    
    if arquivos.salvar_dados(todas_tarefas, ARQUIVO_TAREFAS):
        print(f"Sucesso! Tarefa '{titulo}' cadastrada.")
    else:
        print("Erro: Falha ao salvar a nova tarefa.")

# --- (Card 15) Listar Tarefas ---

def listar_tarefas(usuario_logado: dict):
    """Lista todas as tarefas associadas ao usuário logado."""
    print(f"\n--- Tarefas de {usuario_logado['nome']} ---")
    
    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    tarefas_do_usuario = [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]
    
    if not tarefas_do_usuario:
        print("Você ainda não possui tarefas cadastradas.")
        return

    # Ordena por prazo (pode ser melhorado)
    tarefas_do_usuario.sort(key=lambda x: datetime.datetime.strptime(x['prazo'], '%d/%m/%Y'))
    
    data_hoje = datetime.datetime.strptime(_hoje_str(), '%d/%m/%Y')

    for tarefa in tarefas_do_usuario:
        _imprimir_tarefa(tarefa)
        
        # (Card 15) Destaca tarefas atrasadas
        data_prazo = datetime.datetime.strptime(tarefa['prazo'], '%d/%m/%Y')
        if data_prazo < data_hoje and tarefa['status'] == STATUS_PENDENTE:
            print(">>> ATENÇÃO: ESTA TAREFA ESTÁ ATRASADA! <<<")
            
    print("---------------------------------")

# --- (Card 16) Editar Tarefa ---

def editar_tarefa(usuario_logado: dict):
    """Permite ao usuário editar o título, descrição ou prazo de uma tarefa."""
    print("\n--- Editar Tarefa ---")
    listar_tarefas(usuario_logado) # Mostra as tarefas primeiro
    
    tarefa_id = input("Digite o ID (completo ou os 8 primeiros chars) da tarefa que deseja editar: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return

    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    tarefa_encontrada = None
    
    # Procura a tarefa pelo ID parcial ou completo
    for t in todas_tarefas:
        if t['id'].startswith(tarefa_id) and t['responsavel'] == usuario_logado['id']:
            tarefa_encontrada = t
            break
            
    if not tarefa_encontrada:
        print("Erro: Tarefa não encontrada ou você não tem permissão para editá-la.")
        return
        
    print("\nEditando tarefa (Deixe em branco para manter o valor atual):")
    _imprimir_tarefa(tarefa_encontrada)
    
    novo_titulo = input(f"Novo Título (Atual: {tarefa_encontrada['titulo']}): ")
    nova_descricao = input(f"Nova Descrição (Atual: {tarefa_encontrada['descricao']}): ")
    novo_prazo = input(f"Novo Prazo (Atual: {tarefa_encontrada['prazo']}): ")

    if novo_titulo:
        tarefa_encontrada['titulo'] = novo_titulo
    if nova_descricao:
        tarefa_encontrada['descricao'] = nova_descricao
    if novo_prazo:
        if _validar_data(novo_prazo):
            tarefa_encontrada['prazo'] = novo_prazo
        else:
            print("Aviso: Formato de data inválido. O prazo não foi alterado.")

    if arquivos.salvar_dados(todas_tarefas, ARQUIVO_TAREFAS):
        print("Sucesso! Tarefa atualizada.")
    else:
        print("Erro: Falha ao salvar as alterações.")

# --- (Card 17) Excluir e Concluir ---

def excluir_tarefa(usuario_logado: dict):
    """Exclui permanentemente uma tarefa."""
    print("\n--- Excluir Tarefa ---")
    listar_tarefas(usuario_logado)
    
    tarefa_id = input("Digite o ID (completo ou 8 chars) da tarefa que deseja EXCLUIR: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return

    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    tarefa_encontrada = None
    
    for t in todas_tarefas:
        if t['id'].startswith(tarefa_id) and t['responsavel'] == usuario_logado['id']:
            tarefa_encontrada = t
            break
            
    if not tarefa_encontrada:
        print("Erro: Tarefa não encontrada ou você não tem permissão.")
        return

    _imprimir_tarefa(tarefa_encontrada)
    confirmacao = input(f"Tem certeza que deseja excluir a tarefa '{tarefa_encontrada['titulo']}'? (s/n): ")

    if confirmacao.lower() == 's':
        # Cria uma nova lista sem a tarefa excluída
        novas_tarefas = [t for t in todas_tarefas if t['id'] != tarefa_encontrada['id']]
        
        if arquivos.salvar_dados(novas_tarefas, ARQUIVO_TAREFAS):
            print("Sucesso! Tarefa excluída.")
        else:
            print("Erro: Falha ao salvar as alterações.")
    else:
        print("Exclusão cancelada.")

def concluir_tarefa(usuario_logado: dict):
    """Marca uma tarefa como 'Concluída'."""
    print("\n--- Concluir Tarefa ---")
    listar_tarefas(usuario_logado)
    
    tarefa_id = input("Digite o ID (completo ou 8 chars) da tarefa que deseja concluir: ")
    if not tarefa_id:
        print("Operação cancelada.")
        return
        
    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    tarefa_encontrada = None
    
    for t in todas_tarefas:
        if t['id'].startswith(tarefa_id) and t['responsavel'] == usuario_logado['id']:
            tarefa_encontrada = t
            break
            
    if not tarefa_encontrada:
        print("Erro: Tarefa não encontrada ou você não tem permissão.")
        return
        
    if tarefa_encontrada['status'] == STATUS_CONCLUIDA:
        print("Aviso: Esta tarefa já estava concluída.")
        return

    tarefa_encontrada['status'] = STATUS_CONCLUIDA
    tarefa_encontrada['data_conclusao'] = _hoje_str()
    
    if arquivos.salvar_dados(todas_tarefas, ARQUIVO_TAREFAS):
        print(f"Sucesso! Tarefa '{tarefa_encontrada['titulo']}' marcada como concluída.")
    else:
        print("Erro: Falha ao salvar as alterações.")