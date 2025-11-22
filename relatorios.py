import datetime
from utils import arquivos
import ast # Importante para converter a string do txt em dicionário

def carregar_tarefas_do_usuario(id_usuario):
    """Função auxiliar para ler o arquivo e filtrar tarefas do usuário."""
    # Carrega as strings do arquivo usando o módulo arquivos
    linhas_brutas = arquivos.carregar_dados("tarefas.txt")
    
    minhas_tarefas = []
    
    for linha in linhas_brutas:
        try:
            # Tenta converter a linha de texto (string) em um dicionário Python
            t = ast.literal_eval(linha)
            
            # Verifica se a conversão funcionou e se é um dicionário
            if isinstance(t, dict):
                if t.get('responsavel') == id_usuario:
                    minhas_tarefas.append(t)
        except (ValueError, SyntaxError):
            # Pula linhas que não estejam no formato correto de dicionário
            continue
            
    return minhas_tarefas

def gerar_relatorio_concluidas(usuario):
    print("")
    print(f"RELATÓRIO DE CONCLUÍDAS: {usuario['nome']}")
    print("-" * 50)

    minhas_tarefas = carregar_tarefas_do_usuario(usuario['id'])
    
    concluidas = 0
    tempo_total_dias = 0
    qtd_com_data = 0

    print("TAREFAS CONCLUÍDAS:")
    for t in minhas_tarefas:
        if t.get('status') == "Concluída":
            concluidas += 1
            # Mostra titulo e data
            data_fim = t.get('data_conclusao', 'N/A')
            print(f"- {t['titulo']} (Feita em: {data_fim})")
            
            # Cálculo de produtividade (tempo médio)
            if data_fim:
                try:
                    c = t['data_criacao'].split('/')
                    data_c = datetime.datetime(int(c[2]), int(c[1]), int(c[0]))
                    
                    f = data_fim.split('/')
                    data_f = datetime.datetime(int(f[2]), int(f[1]), int(f[0]))
                    
                    tempo = data_f - data_c
                    tempo_total_dias += tempo.days
                    qtd_com_data += 1
                except:
                    pass

    if concluidas == 0:
        print("Nenhuma tarefa concluída encontrada.")
    else:
        print("-" * 50)
        print(f"Total concluídas: {concluidas}")
        if qtd_com_data > 0:
            media = tempo_total_dias / qtd_com_data
            print(f"Tempo médio de execução: {int(media)} dias")

def gerar_relatorio_pendentes(usuario):
    print("")
    print(f"RELATÓRIO DE PENDÊNCIAS: {usuario['nome']}")
    print("-" * 50)

    minhas_tarefas = carregar_tarefas_do_usuario(usuario['id'])
    hoje = datetime.datetime.now()
    
    pendentes = 0
    atrasadas = 0

    print("TAREFAS PENDENTES:")
    for t in minhas_tarefas:
        if t.get('status') == "Pendente":
            pendentes += 1
            aviso = ""
            prazo_str = t.get('prazo', '')
            
            try:
                partes = prazo_str.split('/')
                dia = int(partes[0])
                mes = int(partes[1])
                ano = int(partes[2])
                
                data_prazo = datetime.datetime(ano, mes, dia)
                
                # Verifica atraso
                # .date() remove as horas da comparação
                if data_prazo.date() < hoje.date():
                    aviso = " [ATRASADO!!]"
                    atrasadas += 1
                
                print(f"- {t['titulo']} - Prazo: {prazo_str}{aviso}")
            except:
                print(f"- {t['titulo']} (Prazo inválido ou sem prazo)")

    if pendentes == 0:
        print("Nenhuma pendência encontrada.")
    
    print("-" * 50)
    total = len(minhas_tarefas)
    print(f"Total de tarefas do usuário: {total}")
    print(f"Pendentes: {pendentes}")
    print(f"Atrasadas: {atrasadas}")
    
    if total > 0:
        # Recalcula concluídas apenas para a porcentagem
        concluidas_count = sum(1 for x in minhas_tarefas if x.get('status') == "Concluída")
        porcentagem = (concluidas_count * 100) / total
        print(f"Produtividade Geral: {int(porcentagem)}% concluído.")