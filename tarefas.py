from uuid import uuid4
from datetime import datetime
from utils import arquivos  # Importa o módulo de persistência

# Constantes
ARQUIVO_TAREFAS = "tarefas.txt"
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"

def _data_atual():
    """Retorna a data atual no formato dd/mm/yyyy."""
    return datetime.now().strftime("%d/%m/%Y")

def _validar_data(data_str: str) -> bool:
    """Valida se a data está no formato dd/mm/yyyy."""
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def _carregar_tarefas() -> list:
    """Carrega todas as tarefas do arquivo JSON."""
    return arquivos.carregar_dados(ARQUIVO_TAREFAS)

def _salvar_tarefas(tarefas: list) -> bool:
    """Salva todas as tarefas no arquivo JSON."""
    return arquivos.salvar_dados(tarefas, ARQUIVO_TAREFAS)

def _buscar_tarefa_por_id(id_tarefa: str, tarefas: list):
    """Busca uma tarefa pelo ID."""
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa:
            return tarefa
    return None

# --- (Card 13) Cadastrar Tarefa ---

def cadastrar_tarefa(usuario_logado: dict):
    """Cadastra uma nova tarefa para o usuário logado."""
    print("\n--- Nova Tarefa ---")
    
    titulo = input("Título da tarefa: ").strip()
    if not titulo:
        print("Erro: O título não pode ficar em branco.")
        return
    
    descricao = input("Descrição: ").strip()
    
    prazo = input("Prazo (dd/mm/yyyy): ").strip()
    if not _validar_data(prazo):
        print("Erro: Data inválida. Use o formato dd/mm/yyyy.")
        return
    
    # Cria a nova tarefa
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": titulo,
        "descricao": descricao,
        "responsavel": usuario_logado['id'],
        "prazo": prazo,
        "status": STATUS_PENDENTE,
        "data_criacao": _data_atual(),
        "data_conclusao": None
    }
    
    # Carrega tarefas existentes, adiciona a nova e salva
    todas_tarefas = _carregar_tarefas()
    todas_tarefas.append(nova_tarefa)
    
    if _salvar_tarefas(todas_tarefas):
        print(f"Tarefa '{titulo}' criada com sucesso!")
    else:
        print("Erro ao salvar a tarefa.")

# --- (Card 14) Listar Tarefas ---

def listar_tarefas(usuario_logado: dict):
    """Lista todas as tarefas do usuário logado."""
    print(f"\n--- Suas Tarefas ---")
    
    todas_tarefas = _carregar_tarefas()
    tarefas_do_usuario = [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]
    
    if not tarefas_do_usuario:
        print("Você ainda não tem pacientes (tarefas) cadastrados.")
        print("Dica: Use a opção 'Novo Paciente' no menu para cadastrar.")
        return
    
    print("=" * 60)
    for tarefa in tarefas_do_usuario:
        print(f"ID: {tarefa['id'][:8]}... | Status: {tarefa['status']}")
        print(f"Título: {tarefa['titulo']}")
        print(f"Descrição: {tarefa['descricao']}")
        print(f"Prazo: {tarefa['prazo']}")
        if tarefa['data_conclusao']:
            print(f"Concluída em: {tarefa['data_conclusao']}")
        print("-" * 60)
    
    print(f"\nTotal: {len(tarefas_do_usuario)} tarefa(s)")

# --- (Card 15) Editar Tarefa ---

def editar_tarefa(usuario_logado: dict):
    """Edita uma tarefa existente do usuário."""
    print("\n--- Editar Tarefa ---")
    
    todas_tarefas = _carregar_tarefas()
    tarefas_do_usuario = [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]
    
    if not tarefas_do_usuario:
        print("Você não tem tarefas para editar.")
        return
    
    # Mostra as tarefas
    print("\nSuas tarefas:")
    for i, tarefa in enumerate(tarefas_do_usuario, 1):
        print(f"{i}. {tarefa['titulo']} (Status: {tarefa['status']})")
    
    try:
        escolha = int(input("\nNúmero da tarefa para editar (0 para cancelar): "))
        if escolha == 0:
            return
        if escolha < 1 or escolha > len(tarefas_do_usuario):
            print("Número inválido!")
            return
    except ValueError:
        print("Entrada inválida!")
        return
    
    tarefa_selecionada = tarefas_do_usuario[escolha - 1]
    
    print(f"\nEditando: {tarefa_selecionada['titulo']}")
    print("(Deixe em branco para manter o valor atual)")
    
    novo_titulo = input(f"Novo título [{tarefa_selecionada['titulo']}]: ").strip()
    nova_descricao = input(f"Nova descrição [{tarefa_selecionada['descricao']}]: ").strip()
    novo_prazo = input(f"Novo prazo [{tarefa_selecionada['prazo']}]: ").strip()
    
    # Atualiza apenas os campos que foram preenchidos
    if novo_titulo:
        tarefa_selecionada['titulo'] = novo_titulo
    if nova_descricao:
        tarefa_selecionada['descricao'] = nova_descricao
    if novo_prazo:
        if _validar_data(novo_prazo):
            tarefa_selecionada['prazo'] = novo_prazo
        else:
            print("Data inválida. O prazo não foi alterado.")
    
    if _salvar_tarefas(todas_tarefas):
        print("Tarefa atualizada com sucesso!")
    else:
        print("Erro ao salvar as alterações.")

# --- (Card 16) Excluir Tarefa ---

def excluir_tarefa(usuario_logado: dict):
    """Exclui uma tarefa do usuário."""
    print("\n--- Excluir Tarefa ---")
    
    todas_tarefas = _carregar_tarefas()
    tarefas_do_usuario = [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]
    
    if not tarefas_do_usuario:
        print("Você não tem tarefas para excluir.")
        return
    
    # Mostra as tarefas
    print("\nSuas tarefas:")
    for i, tarefa in enumerate(tarefas_do_usuario, 1):
        print(f"{i}. {tarefa['titulo']} (Status: {tarefa['status']})")
    
    try:
        escolha = int(input("\nNúmero da tarefa para excluir (0 para cancelar): "))
        if escolha == 0:
            return
        if escolha < 1 or escolha > len(tarefas_do_usuario):
            print("Número inválido!")
            return
    except ValueError:
        print("Entrada inválida!")
        return
    
    tarefa_selecionada = tarefas_do_usuario[escolha - 1]
    
    # Confirmação
    confirmacao = input(f"Tem certeza que deseja excluir '{tarefa_selecionada['titulo']}'? (s/n): ")
    if confirmacao.lower() != 's':
        print("Exclusão cancelada.")
        return
    
    # Remove a tarefa da lista
    todas_tarefas.remove(tarefa_selecionada)
    
    if _salvar_tarefas(todas_tarefas):
        print("Tarefa excluída com sucesso!")
    else:
        print("Erro ao excluir a tarefa.")

# --- (Card 17) Concluir Tarefa ---

def concluir_tarefa(usuario_logado: dict):
    """Marca uma tarefa como concluída."""
    print("\n--- Concluir Tarefa ---")
    
    todas_tarefas = _carregar_tarefas()
    tarefas_do_usuario = [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]
    tarefas_pendentes = [t for t in tarefas_do_usuario if t['status'] == STATUS_PENDENTE]
    
    if not tarefas_pendentes:
        print("Você não tem tarefas pendentes para concluir.")
        return
    
    # Mostra apenas tarefas pendentes
    print("\nTarefas pendentes:")
    for i, tarefa in enumerate(tarefas_pendentes, 1):
        print(f"{i}. {tarefa['titulo']} (Prazo: {tarefa['prazo']})")
    
    try:
        escolha = int(input("\nNúmero da tarefa para concluir (0 para cancelar): "))
        if escolha == 0:
            return
        if escolha < 1 or escolha > len(tarefas_pendentes):
            print("Número inválido!")
            return
    except ValueError:
        print("Entrada inválida!")
        return
    
    tarefa_selecionada = tarefas_pendentes[escolha - 1]
    
    # Atualiza o status
    tarefa_selecionada['status'] = STATUS_CONCLUIDA
    tarefa_selecionada['data_conclusao'] = _data_atual()
    
    if _salvar_tarefas(todas_tarefas):
        print(f"Parabéns! Tarefa '{tarefa_selecionada['titulo']}' concluída!")
    else:
        print("Erro ao atualizar a tarefa.")