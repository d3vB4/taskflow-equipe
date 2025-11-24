import datetime
import usuarios
import tarefas
import os

def confirmacao_concluida(tarefa: dict) -> bool:
    """Verifica se a tarefa está concluída (booleano ou string)."""
    if not tarefa: return False
    
    # Verifica campo status
    status = str(tarefa.get('status', '')).lower()
    return status in ('concluida', 'concluída', 'concluido', 'done', 'finalizada')

def imprimir_cabecalho(titulo):
    print()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60)

def converter_data(data_str):
    if not data_str or data_str == 'None': return None
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None

def buscar_nome_usuario(id_usuario):
    """Busca o nome no dicionário de usuários de forma segura."""
    if not id_usuario or id_usuario == 'None':
        return "Sistema/Automático"
    
    # Força recarregamento para garantir que temos todos os dados
    lista_users = usuarios.listar_usuarios()
    for u in lista_users:
        if u['id'] == id_usuario:
            return u['nome']
            
    return "Usuário Removido"

# --- LÓGICA DE PERMISSÃO ---
def pode_ver_tudo(usuario_logado):
    """Define se o usuário pode ver relatórios de todos os setores."""
    if not usuario_logado: return False
    setor = str(usuario_logado.get('setor', '')).lower()
    # Recepção e Admin veem tudo
    return setor in ['recepção', 'admin', 'administração']

# RELATÓRIO 1: CONCLUÍDAS 
def gerar_relatorio_concluidos(usuario_filtro=None):
    titulo = "RELATÓRIO DE CONCLUÍDAS"
    ver_tudo = pode_ver_tudo(usuario_filtro)
    
    if usuario_filtro and not ver_tudo:
        titulo += f": {usuario_filtro['nome']}"
    else:
        titulo += ": GERAL (Visão Gerencial)"
    
    imprimir_cabecalho(titulo)

    lista_alvo = tarefas._carregar_tarefas()
    concluidas_count = 0
    tempo_total_dias = 0
    qtd_com_calculo = 0

    print(f"{'TÍTULO':<25} | {'DATA CONC.':<12} | {'RESPONSÁVEL'}")
    print("-" * 60)

    for tarefa in lista_alvo:
        if not confirmacao_concluida(tarefa):
            continue

        # FILTRO: Se não for Recepção, só vê as suas ou do seu setor
        if usuario_filtro and not ver_tudo:
            eh_responsavel = tarefa.get('responsavel') == usuario_filtro['id']
            eh_concluido_por = tarefa.get('concluida_por') == usuario_filtro['id']
            eh_setor = str(tarefa.get('setor')).lower() == str(usuario_filtro['setor']).lower()
            
            if not (eh_responsavel or eh_concluido_por or eh_setor):
                continue

        concluidas_count += 1
        
        # Quem concluiu a tarefa?
        id_resp = tarefa.get('concluida_por') or tarefa.get('responsavel')
        nome_resp = buscar_nome_usuario(id_resp)
        
        data_fim_str = tarefa.get('data_conclusao') or "---"
        print(f"{tarefa['titulo'][:25]:<25} | {data_fim_str:<12} | {nome_resp}")

        # Cálculo de tempo
        data_criacao = converter_data(tarefa.get('data_criacao'))
        data_conclusao = converter_data(tarefa.get('data_conclusao'))

        if data_criacao and data_conclusao:
            diferenca = data_conclusao - data_criacao
            tempo_total_dias += diferenca.days
            qtd_com_calculo += 1

    print("-" * 60)
    if concluidas_count == 0:
        print(">> Nenhuma tarefa concluída encontrada para este perfil.")
    else:
        print(f"Total concluídas: {concluidas_count}")
        if qtd_com_calculo > 0:
            media = tempo_total_dias / qtd_com_calculo
            print(f"Tempo médio de execução: {int(media)} dias")

# RELATÓRIO 2: PENDÊNCIAS
def gerar_relatorio_pendentes(usuario_filtro=None):
    titulo = "RELATÓRIO DE PENDÊNCIAS"
    ver_tudo = pode_ver_tudo(usuario_filtro)
    
    if usuario_filtro and not ver_tudo:
        titulo += f": {usuario_filtro['nome']}"
    else:
        titulo += ": GERAL (Visão Gerencial)"
    
    imprimir_cabecalho(titulo)

    lista_alvo = tarefas._carregar_tarefas()
    hoje = datetime.datetime.now()
    
    pendentes_count = 0
    atrasadas_count = 0

    print(f"{'TÍTULO':<25} | {'SETOR':<12} | {'PRAZO'}")
    print("-" * 60)

    for tarefa in lista_alvo:
        if confirmacao_concluida(tarefa):
            continue
        
        status_atual = tarefa.get('status', '')
        if 'cancelada' in status_atual.lower():
            continue

        # FILTRO
        if usuario_filtro and not ver_tudo:
            eh_responsavel = tarefa.get('responsavel') == usuario_filtro['id']
            eh_setor = str(tarefa.get('setor')).lower() == str(usuario_filtro['setor']).lower()
            
            if not (eh_responsavel or eh_setor):
                continue

        pendentes_count += 1
        
        prazo_str = tarefa.get('prazo')
        data_prazo = converter_data(prazo_str)
        aviso = ""
        
        if data_prazo and data_prazo.date() < hoje.date():
            aviso = " [ATRASADO!]"
            atrasadas_count += 1
        
        setor_t = tarefa.get('setor', 'Geral')
        print(f"{tarefa['titulo'][:25]:<25} | {setor_t:<12} | {prazo_str}{aviso}")

    print("-" * 60)
    print(f"Total Pendentes: {pendentes_count}")
    print(f"Total Atrasadas: {atrasadas_count}")

# RELATÓRIO 3: PRODUTIVIDADE DA EQUIPE 
def gerar_relatorio_produtividade(usuario_filtro=None):
    imprimir_cabecalho("PRODUTIVIDADE DA EQUIPE (RANKING)")

    # Mapeia ID -> Nome
    mapa_nomes = {}
    for u in usuarios.listar_usuarios():
        mapa_nomes[u['id']] = u['nome']

    contagem = {}
    
    lista_alvo = tarefas._carregar_tarefas()
    total_geral = 0
    
    for tarefa in lista_alvo:
        if confirmacao_concluida(tarefa):
            # Quem concluiu de fato?
            resp_id = tarefa.get('concluida_por')
            
            # Se não tem 'concluida_por', tenta 'responsavel' (mas cuidado com 'sistema')
            if not resp_id or resp_id == 'sistema':
                continue # Tarefas do sistema não contam para ranking de usuários

            nome = mapa_nomes.get(resp_id, "Usuário Removido")
            
            if nome not in contagem:
                 contagem[nome] = 0
            
            contagem[nome] += 1
            total_geral += 1

    # Ordenar
    ranking = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    print(f"{'COLABORADOR':<25} | {'QTD'} | {'GRÁFICO'}")
    print("-" * 60)

    for nome, qtd in ranking:
        barra = "█" * qtd 
        print(f"{nome:<25} | {qtd:^3} | {barra}")

    print("-" * 60)
    print(f"Total de entregas manuais: {total_geral}")

# RELATÓRIO 4: EXPORTAR PARA TXT
def exportar_relatorio_txt(usuario_logado):
    imprimir_cabecalho("EXPORTAR RELATÓRIO")
    
    nome_arquivo = f"relatorio_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    lista_alvo = tarefas._carregar_tarefas()
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO GERAL DE TAREFAS\n")
            f.write(f"Gerado por: {usuario_logado['nome']} em {datetime.datetime.now()}\n")
            f.write("="*50 + "\n\n")
            
            for t in lista_alvo:
                f.write(f"[{t['status']}] {t['titulo']}\n")
                f.write(f"Setor: {t.get('setor')} | Responsável: {t.get('responsavel')}\n")
                f.write(f"Concluída por: {buscar_nome_usuario(t.get('concluida_por'))}\n")
                f.write("-" * 20 + "\n")
        
        print(f"Arquivo exportado com sucesso: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar arquivo: {e}")