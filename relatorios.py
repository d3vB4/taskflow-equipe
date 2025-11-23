import datetime
import usuarios
import tarefas

def imprimir_cabecalho(titulo):
    """Padroniza o título dos relatórios."""
    print()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60)

def converter_data(data_str):
    """
    Converte string 'dd/mm/yyyy' para objeto datetime.
    Retorna None se falhar ou se a string for vazia/None.
    """
    if not data_str or data_str == 'None':
        return None
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None

def buscar_usuario(id_usuario):
    """Busca o nome no dicionário de usuários."""
    if not id_usuario:
        return "Não Atribuído"
    usuario = usuarios.obter_usuario(id_usuario)
    return usuario['nome'] if usuario else "Usuário Removido"

# RELATÓRIO 1: CONCLUÍDAS 
def gerar_relatorio_concluidas(usuario_filtro=None):
    """
    Lista tarefas concluídas, mostrando data e calculando o tempo médio de execução.
    """
    titulo = "RELATÓRIO DE CONCLUÍDAS"
    if usuario_filtro:
        titulo += f": {usuario_filtro['nome']}"
    
    imprimir_cabecalho(titulo)

    lista_alvo = tarefas.tarefas
    concluidas_count = 0
    tempo_total_dias = 0
    qtd_com_calculo = 0

    print(f"{'TÍTULO':<25} | {'DATA CONC.':<12} | {'RESPONSÁVEL'}")
    print("-" * 60)

    for tarefa in lista_alvo:
        # 1. Filtro de Status 
        if tarefa.get('status') != 'concluida':
            continue

        # 2. Filtro de Usuário
        if usuario_filtro and tarefa.get('responsavel') != usuario_filtro.get('id'):
            continue

        concluidas_count += 1
        
        # Dados para exibição
        nome_resp = buscar_usuario(tarefa.get('responsavel'))
        data_fim_str = tarefa.get('data_conclusao') or "---"
        print(f"{tarefa['titulo']:<25} | {data_fim_str:<12} | {nome_resp}")

        # Lógica do Código Antigo: Cálculo de Tempo Médio
        data_criacao = converter_data(tarefa.get('data_criacao'))
        data_conclusao = converter_data(tarefa.get('data_conclusao'))

        if data_criacao and data_conclusao:
            diferenca = data_conclusao - data_criacao
            tempo_total_dias += diferenca.days
            qtd_com_calculo += 1

    print("-" * 60)
    if concluidas_count == 0:
        print(">> Nenhuma tarefa concluída encontrada.")
    else:
        print(f"Total concluídas: {concluidas_count}")
        # Cálculo da Média (feature do código antigo)
        if qtd_com_calculo > 0:
            media = tempo_total_dias / qtd_com_calculo
            print(f"Tempo médio de execução: {int(media)} dias")
        else:
            print("Tempo médio: N/A (datas insuficientes)")


# RELATÓRIO 2: PENDÊNCIAS
def gerar_relatorio_pendentes(usuario_filtro=None):
    """
    Lista pendências, avisa se está atrasado e calcula % de produtividade geral.
    """
    titulo = "RELATÓRIO DE PENDÊNCIAS"
    if usuario_filtro:
        titulo += f": {usuario_filtro['nome']}"
    
    imprimir_cabecalho(titulo)

    lista_alvo = tarefas.tarefas
    hoje = datetime.datetime.now()
    
    pendentes_count = 0
    atrasadas_count = 0
    
    # Contadores para o cálculo de porcentagem final
    total_tarefas_usuario = 0
    total_concluidas_usuario = 0

    print(f"{'TÍTULO':<25} | {'PRAZO':<12} | {'STATUS'}")
    print("-" * 60)

    for tarefa in lista_alvo:
        # Lógica para contar totais do usuário (para a porcentagem no final)
        eh_do_usuario = True
        if usuario_filtro and tarefa.get('responsavel') != usuario_filtro.get('id'):
            eh_do_usuario = False
        
        if eh_do_usuario:
            total_tarefas_usuario += 1
            if tarefa.get('status') == 'concluida':
                total_concluidas_usuario += 1
                continue # Se está concluída, não lista no relatório de pendências

        # Se não for do usuário (quando tem filtro) ou se já está concluída, pula visualização
        if not eh_do_usuario or tarefa.get('status') == 'concluida':
            continue

        # Daqui pra baixo é apenas tarefa PENDENTE do usuário selecionado (ou geral)
        pendentes_count += 1
        
        prazo_str = tarefa.get('prazo')
        data_prazo = converter_data(prazo_str)
        aviso = ""
        
        # Lógica do Código Antigo: Verificar Atraso
        if data_prazo:
            # .date() compara apenas dia/mês/ano, ignorando hora
            if data_prazo.date() < hoje.date():
                aviso = " [ATRASADO!!]"
                atrasadas_count += 1
        
        print(f"{tarefa['titulo']:<25} | {prazo_str:<12} | Pendente{aviso}")

    print("-" * 60)
    
    if pendentes_count == 0:
        print(">> Nenhuma pendência encontrada.")
    
    print(f"Total Pendentes: {pendentes_count}")
    print(f"Total Atrasadas: {atrasadas_count}")

    # Lógica do Código Antigo: Porcentagem de Produtividade
    if total_tarefas_usuario > 0:
        porcentagem = (total_concluidas_usuario * 100) / total_tarefas_usuario
        print(f"\nProdutividade Geral (Concluídas/Total): {int(porcentagem)}%")
    else:
        print("\nProdutividade Geral: 0% (Nenhuma tarefa vinculada)")


# RELATÓRIO 3: PRODUTIVIDADE DA EQUIPE 
def gerar_relatorio_produtividade():
    """
    Relatório gerencial de ranking de tarefas por usuário.
    """
    imprimir_cabecalho("PRODUTIVIDADE DA EQUIPE (RANKING)")

    # 1. Inicializar contadores com todos os usuários do sistema
    contagem = {}
    todos_usuarios = usuarios.listar_usuarios()
    
    for u in todos_usuarios:
        contagem[u['id']] = {'nome': u['nome'], 'concluidas': 0}

    # 2. Contar tarefas concluídas varrendo a lista de tarefas
    total_geral = 0
    for tarefa in tarefas.tarefas:
        if tarefa.get('status') == 'concluida':
            resp_id = tarefa.get('responsavel')
            if resp_id in contagem:
                contagem[resp_id]['concluidas'] += 1
            total_geral += 1

    # 3. Ordenar e Exibir
    ranking = sorted(contagem.values(), key=lambda x: x['concluidas'], reverse=True)

    print(f"{'COLABORADOR':<25} | {'QTD'} | {'GRÁFICO'}")
    print("-" * 60)

    for item in ranking:
        qtd = item['concluidas']
        barra = "█" * qtd 
        print(f"{item['nome']:<25} | {qtd:^3} | {barra}")

    print("-" * 60)
    print(f"Total de entregas da equipe: {total_geral}")