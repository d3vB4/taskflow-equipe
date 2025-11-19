import datetime
from utils import arquivos # Importa o trabalho do Dev 4 (utils)

# Constantes (importadas de tarefas.py, mas duplicadas aqui por simplicidade)
ARQUIVO_TAREFAS = "tarefas.json"
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"

def _hoje():
    """Retorna o objeto datetime.date de hoje."""
    return datetime.date.today()

def _carregar_tarefas_do_usuario(usuario_logado: dict) -> list:
    """Função auxiliar para carregar e filtrar tarefas do usuário."""
    todas_tarefas = arquivos.carregar_dados(ARQUIVO_TAREFAS)
    return [t for t in todas_tarefas if t['responsavel'] == usuario_logado['id']]

# --- (Card 19) Relatório de Tarefas Concluídas ---

def gerar_relatorio_concluidas(usuario_logado: dict):
    """Imprime um relatório formatado de todas as tarefas concluídas."""
    print(f"\n--- Relatório de Tarefas Concluídas ({usuario_logado['nome']}) ---")
    
    tarefas_do_usuario = _carregar_tarefas_do_usuario(usuario_logado)
    tarefas_concluidas = [t for t in tarefas_do_usuario if t['status'] == STATUS_CONCLUIDA]
    
    if not tarefas_concluidas:
        print("Você ainda não concluiu nenhuma tarefa.")
        print("==============================================")
        return

    tarefas_concluidas.sort(key=lambda x: datetime.datetime.strptime(x['data_conclusao'], '%d/%m/%Y'))
    
    print("==============================================")
    for tarefa in tarefas_concluidas:
        print(f"ID: {tarefa['id'][:8]}...")
        print(f"Título: {tarefa['titulo']}")
        print(f"Concluída em: {tarefa['data_conclusao']}")
        print("----------------------------------------------")
        
    print(f"\nTotal de Tarefas Concluídas: {len(tarefas_concluidas)}")
    print("==============================================")

# --- (Card 20) Relatório de Tarefas Pendentes ---

def gerar_relatorio_pendentes(usuario_logado: dict):
    """Imprime um relatório formatado de tarefas pendentes e atrasadas."""
    print(f"\n--- Relatório de Tarefas Pendentes ({usuario_logado['nome']}) ---")
    
    tarefas_do_usuario = _carregar_tarefas_do_usuario(usuario_logado)
    tarefas_pendentes = [t for t in tarefas_do_usuario if t['status'] == STATUS_PENDENTE]
    
    if not tarefas_pendentes:
        print("Você não tem nenhuma tarefa pendente. Parabéns!")
        print("==============================================")
        return

    tarefas_pendentes.sort(key=lambda x: datetime.datetime.strptime(x['prazo'], '%d/%m/%Y'))
    
    hoje = _hoje()
    total_atrasadas = 0
    
    print("==============================================")
    for tarefa in tarefas_pendentes:
        data_prazo = datetime.datetime.strptime(tarefa['prazo'], '%d/%m/%Y').date()
        
        print(f"ID: {tarefa['id'][:8]}...")
        print(f"Título: {tarefa['titulo']}")
        print(f"Prazo: {tarefa['prazo']}")
        
        if data_prazo < hoje:
            dias_atraso = (hoje - data_prazo).days
            print(f"Status: PENDENTE (ATRASADA HÁ {dias_atraso} DIAS!)")
            total_atrasadas += 1
        else:
            print("Status: Pendente")
            
        print("----------------------------------------------")
        
    print(f"\nTotal de Tarefas Pendentes: {len(tarefas_pendentes)}")
    print(f"Total de Tarefas Atrasadas: {total_atrasadas}")
    print("==============================================")

# --- (Card 21) Relatório de Produtividade ---

def gerar_relatorio_produtividade(usuario_logado: dict, exportar=False):
    """
    Gera um relatório de produtividade consolidado.
    Pode imprimir no console ou retornar uma string para exportação.
    """
    
    tarefas_do_usuario = _carregar_tarefas_do_usuario(usuario_logado)
    
    if not tarefas_do_usuario:
        if not exportar:
            print("\n--- Relatório de Produtividade ---")
            print("Você ainda não tem tarefas para gerar um relatório.")
        return "Nenhuma tarefa encontrada."

    total_tarefas = len(tarefas_do_usuario)
    concluidas = [t for t in tarefas_do_usuario if t['status'] == STATUS_CONCLUIDA]
    pendentes = [t for t in tarefas_do_usuario if t['status'] == STATUS_PENDENTE]
    
    hoje = _hoje()
    atrasadas = 0
    for t in pendentes:
        data_prazo = datetime.datetime.strptime(t['prazo'], '%d/%m/%Y').date()
        if data_prazo < hoje:
            atrasadas += 1
            
    taxa_conclusao = (len(concluidas) / total_tarefas) * 100 if total_tarefas > 0 else 0
    
    # Monta a string do relatório
    relatorio_str = f"""
============================================
RELATÓRIO DE PRODUTIVIDADE
Usuário: {usuario_logado['nome']}
Data: {_hoje_str()}
============================================

Total de Tarefas: {total_tarefas}
Concluídas: {len(concluidas)} ({taxa_conclusao:.1f}%)
Pendentes: {len(pendentes)}
Atrasadas: {atrasadas}

============================================
"""
    
    if exportar:
        return relatorio_str # Retorna a string para o Card 22
    else:
        print(relatorio_str) # Imprime no console

# --- (Card 22) Exportar Relatório para TXT ---

def exportar_relatorio_txt(usuario_logado: dict):
    """
    Gera o relatório de produtividade e o salva em um arquivo .txt.
    """
    print("\n--- Exportar Relatório para TXT ---")
    
    # Chama a função do Card 21 no modo "exportar"
    conteudo_relatorio = gerar_relatorio_produtividade(usuario_logado, exportar=True)
    
    if "Nenhuma tarefa encontrada" in conteudo_relatorio:
        print("Não há dados para exportar.")
        return

    # Cria um nome de arquivo único
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorio_{usuario_logado['login']}_{timestamp}.txt"
    
    # Define o subdiretório 'relatorios/' (conforme Card 22)
    diretorio = "relatorios"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio) # Cria a pasta se ela não existir
        
    caminho_completo = os.path.join(diretorio, nome_arquivo)
    
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo_relatorio)
        
        print(f"Sucesso! Relatório salvo em: {caminho_completo}")
        
    except IOError as e:
        print(f"Erro ao salvar o arquivo de relatório: {e}")