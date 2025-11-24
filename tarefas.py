from uuid import uuid4
from datetime import datetime, timedelta
import os
import ast
import usuarios 

# --- CONFIGURAÇÕES E CONSTANTES ---
ARQUIVO_TAREFAS = "tarefas.txt"
ARQUIVO_PACIENTES = "pacientes.txt"

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"
STATUS_CANCELADA = "Cancelada"

COLUNAS_TAREFAS = [
    'id', 'paciente_id', 'paciente_nome', 'titulo', 'descricao',
    'tipo_tarefa', 'setor', 'responsavel', 'prazo', 'prioridade',
    'status', 'dependencia', 'data_criacao', 'data_conclusao',
    'concluida_por', 'prescricao', 'observacoes', 
    'dados_triagem', 'sinais_vitais', 'estado_geral', 
    'lote_medicamento', 'via_administracao', 'dose',
    'atendimento_token'
]

# --- FUNÇÕES AUXILIARES DE PERSISTÊNCIA ---

def _escape(valor):
    if valor is None: return ''
    if isinstance(valor, dict):
        return str(valor).replace('|', '<PIPE>').replace('\n', '<NL>')
    return str(valor).replace('|', '<PIPE>').replace('\n', '<NL>')

def _unescape(valor):
    if not valor or valor == 'None' or valor == '': return None
    texto = valor.replace('<PIPE>', '|').replace('<NL>', '\n')
    if texto.startswith('{') and texto.endswith('}'):
        try: return ast.literal_eval(texto)
        except: return texto
    return texto

def _salvar_tarefas(tarefas: list) -> bool:
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            f.write('|'.join(COLUNAS_TAREFAS) + '\n')
            for t in tarefas:
                linha = []
                for col in COLUNAS_TAREFAS:
                    linha.append(_escape(t.get(col)))
                f.write('|'.join(linha) + '\n')
        return True
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")
        return False

def _carregar_tarefas() -> list:
    if not os.path.exists(ARQUIVO_TAREFAS): return []
    lista_tarefas = []
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            if len(linhas) < 2: return []
            for linha in linhas[1:]:
                linha = linha.strip()
                if not linha: continue
                partes = linha.split('|')
                tarefa = {}
                for i, col in enumerate(COLUNAS_TAREFAS):
                    if i < len(partes): tarefa[col] = _unescape(partes[i])
                    else: tarefa[col] = None
                lista_tarefas.append(tarefa)
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
        return []
    return lista_tarefas

# --- PERSISTÊNCIA DE PACIENTES (Simples) ---
def _carregar_pacientes() -> list:
    # Tenta usar o utils se existir, senão usa lógica local simples
    try:
        import utils.arquivos as arq
        return arq.carregar_dados(ARQUIVO_PACIENTES)
    except ImportError:
        if not os.path.exists(ARQUIVO_PACIENTES): return []
        # (Implementação simplificada de leitura se necessário)
        return [] 

def _salvar_pacientes(pacientes: list) -> bool:
    try:
        import utils.arquivos as arq
        return arq.salvar_dados(pacientes, ARQUIVO_PACIENTES)
    except:
        return True

def _data_atual():
    return datetime.now().strftime("%d/%m/%Y")

def _hora_atual():
    return datetime.now().strftime("%H:%M")

def _buscar_tarefa_por_id(id_tarefa: str, tarefas: list = None):
    if tarefas is None: tarefas = _carregar_tarefas()
    for t in tarefas:
        if t['id'] == id_tarefa: return t
    return None

# --- CRUD MANUAL DE TAREFAS ---

def criar_tarefa_manual(usuario_logado: dict):
    print("\n--- NOVA TAREFA MANUAL ---")
    titulo = input("Título: ").strip()
    if not titulo: return
    descricao = input("Descrição: ").strip()
    prazo = input("Prazo (dd/mm/yyyy): ").strip()
    
    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": titulo,
        "descricao": descricao,
        "tipo_tarefa": "Manual",
        "setor": usuario_logado['setor'],
        "responsavel": usuario_logado['id'],
        "prazo": prazo,
        "prioridade": "Normal",
        "status": STATUS_PENDENTE,
        "data_criacao": _data_atual(),
        "paciente_nome": "Interno"
    }
    tarefas = _carregar_tarefas()
    tarefas.append(nova_tarefa)
    _salvar_tarefas(tarefas)
    print("✓ Tarefa criada.")

def editar_tarefa(usuario_logado: dict):
    tarefas = _carregar_tarefas()
    setor = str(usuario_logado['setor']).lower()
    meus_itens = [t for t in tarefas if str(t.get('setor')).lower() == setor]
    
    if not meus_itens:
        print("Nada para editar.")
        return

    for i, t in enumerate(meus_itens, 1):
        print(f"{i}. {t['titulo']}")
    
    try:
        idx = int(input("Número: ")) - 1
        if idx < 0: return
        alvo = meus_itens[idx]
        novo_titulo = input(f"Título [{alvo['titulo']}]: ")
        if novo_titulo: alvo['titulo'] = novo_titulo
        _salvar_tarefas(tarefas)
        print("✓ Editado.")
    except: pass

def excluir_tarefa(usuario_logado: dict):
    tarefas = _carregar_tarefas()
    setor = str(usuario_logado['setor']).lower()
    meus_itens = [t for t in tarefas if str(t.get('setor')).lower() == setor]
    
    for i, t in enumerate(meus_itens, 1):
        print(f"{i}. {t['titulo']}")
        
    try:
        idx = int(input("Número para excluir: ")) - 1
        if idx < 0: return
        alvo = meus_itens[idx]
        tarefas = [t for t in tarefas if t['id'] != alvo['id']]
        _salvar_tarefas(tarefas)
        print("✓ Excluído.")
    except: pass

# --- FLUXO AUTOMÁTICO ---

def criar_paciente(usuario_logado: dict, nome: str, cpf: str, 
                   data_nascimento: str, telefone: str, 
                   tipo_atendimento: str, queixa: str) -> str:
    paciente_id = str(uuid4())
    # Aqui chamaria o salvamento de pacientes se necessário
    _criar_fluxo_atendimento(paciente_id, nome, tipo_atendimento, usuario_logado)
    return paciente_id

def _criar_fluxo_atendimento(paciente_id: str, nome_paciente: str, 
                             tipo_atendimento: str, usuario_criador: dict):
    tarefas = _carregar_tarefas()
    hoje = _data_atual()
    
    # Cria as tarefas encadeadas
    t1 = {"id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
          "titulo": f"Triagem - {nome_paciente}", "descricao": "Realizar triagem.",
          "tipo_tarefa": "Triagem", "setor": "enfermagem", "responsavel": "sistema",
          "prazo": hoje, "prioridade": "Normal", "status": STATUS_PENDENTE, "data_criacao": hoje}
    
    t2 = {"id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
          "titulo": f"Consulta - {nome_paciente}", "descricao": "Atendimento médico.",
          "tipo_tarefa": "Consulta Médica", "setor": "médico", "responsavel": "sistema",
          "prazo": hoje, "prioridade": "Normal", "status": STATUS_PENDENTE, 
          "dependencia": t1['id'], "data_criacao": hoje}
          
    tarefas.extend([t1, t2])
    _salvar_tarefas(tarefas)

# --- FUNÇÕES DE LISTAGEM E VISUALIZAÇÃO (REIMPLEMENTADAS) ---

def listar_tarefas_por_setor(usuario_logado):
    """Lista tarefas específicas do setor do usuário logado."""
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    print(f"\n--- TAREFAS: {setor_user.upper()} ---")
    encontrou = False
    for t in tarefas:
        if str(t.get('setor')).lower() == setor_user:
            encontrou = True
            status = t.get('status')
            print(f"[{status}] {t['titulo']}")
            print(f"   Desc: {t.get('descricao')}")
            print("-" * 40)
            
    if not encontrou:
        print(" Nenhuma tarefa encontrada.")

def concluir_tarefa_setor(usuario_logado):
    """Marca uma tarefa como concluída."""
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    # Filtra pendentes do setor
    pendentes = [t for t in tarefas if str(t.get('setor')).lower() == setor_user and t['status'] == STATUS_PENDENTE]
    
    if not pendentes:
        print("Nada pendente para concluir.")
        return

    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['titulo']}")
        
    try:
        idx = int(input("Número: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
        
        selecionada['status'] = STATUS_CONCLUIDA
        selecionada['data_conclusao'] = _data_atual()
        selecionada['concluida_por'] = usuario_logado['id']
        _salvar_tarefas(tarefas)
        print("✓ Tarefa concluída!")
    except: pass

def exibir_fila_por_setor():
    """
    Mostra um painel geral de todas as filas do hospital.
    Ideal para ver onde os pacientes estão parados.
    """
    tarefas = _carregar_tarefas()
    
    # Define a ordem lógica do fluxo hospitalar
    setores_ordem = ['recepção', 'enfermagem', 'médico', 'farmácia']
    
    print("\n" + "="*60)
    print(f"{'FILA DE ESPERA GERAL':^60}")
    print("="*60)
    
    total_geral = 0
    
    for setor in setores_ordem:
        # Filtra tarefas pendentes deste setor
        fila_setor = [
            t for t in tarefas 
            if str(t.get('setor')).lower() == setor 
            and t.get('status') == STATUS_PENDENTE
        ]
        
        print(f"\n=== {setor.upper()} ({len(fila_setor)}) ===")
        if not fila_setor:
            print("  (Fila vazia)")
        else:
            for t in fila_setor:
                # Mostra detalhes importantes (Paciente e Título da Tarefa)
                nome_pac = t.get('paciente_nome', 'Desconhecido')
                titulo = t.get('titulo', 'Sem título')
                prio = "🚨" if t.get('prioridade') == 'Alta' else "•"
                print(f"  {prio} {nome_pac} -> {titulo}")
        
        total_geral += len(fila_setor)
        
    print("-" * 60)
    print(f"Total de pacientes em espera no hospital: {total_geral}")
    print("-" * 60)

def listar_pacientes_geral():
    """
    Lista todos os pacientes que têm tarefas ativas no sistema.
    Isso substitui a necessidade de ler o arquivo 'pacientes.txt' se ele estiver com problemas.
    """
    tarefas = _carregar_tarefas()
    
    # Coleta pacientes únicos baseados nas tarefas
    pacientes_ativos = {}
    
    for t in tarefas:
        pid = t.get('paciente_id')
        if pid and pid not in pacientes_ativos:
            pacientes_ativos[pid] = {
                'nome': t.get('paciente_nome'),
                'tarefas': []
            }
        
        if pid:
            pacientes_ativos[pid]['tarefas'].append(f"{t['titulo']} ({t['status']})")
            
    print("\n" + "="*60)
    print(f"{'PACIENTES EM ATENDIMENTO':^60}")
    print("="*60)
    
    if not pacientes_ativos:
        print("Nenhum paciente encontrado.")
    
    for pid, dados in pacientes_ativos.items():
        print(f"👤 {dados['nome']}")
        # Mostra as últimas 2 tarefas para dar contexto
        ultimas = dados['tarefas'][-2:]
        for task in ultimas:
            print(f"   └─ {task}")
        print("-" * 60)

# Funções placeholders para manter compatibilidade com chamadas antigas do main.py
# (Caso o main.py tente chamar funções específicas de setor que foram generalizadas)
def realizar_triagem(u): concluir_tarefa_setor(u)
def realizar_atendimento_medico(u): concluir_tarefa_setor(u)
def dispensar_medicamento(u): concluir_tarefa_setor(u)
def administrar_medicamento(u): concluir_tarefa_setor(u)
def verificar_paciente(u): concluir_tarefa_setor(u)
def dar_alta_paciente(u): concluir_tarefa_setor(u)
def solicitar_exames(u): print("Funcionalidade em breve.")