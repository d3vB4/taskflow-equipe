from uuid import uuid4
from datetime import datetime, timedelta
import os
import ast  # Para converter strings de dicionários de volta para dict
import usuarios 

# --- CONFIGURAÇÕES E CONSTANTES ---
ARQUIVO_TAREFAS = "tarefas.txt"
ARQUIVO_PACIENTES = "pacientes.txt"

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"
STATUS_CANCELADA = "Cancelada"

# Definição das colunas (Incluindo atendimento_token para o Web funcionar)
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

def _carregar_pacientes() -> list:
    # Simulação simples para evitar dependência circular se utils não existir
    if not os.path.exists(ARQUIVO_PACIENTES): return []
    # Lógica simplificada
    return [] 

def _salvar_pacientes(pacientes: list) -> bool:
    # Lógica simplificada
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

# --- CRUD MANUAL DE TAREFAS (NOVO) ---

def criar_tarefa_manual(usuario_logado: dict):
    """Cria uma tarefa avulsa manualmente."""
    print("\n--- NOVA TAREFA ---")
    titulo = input("Título: ").strip()
    if not titulo:
        print("Erro: Título é obrigatório.")
        return

    descricao = input("Descrição: ").strip()
    prazo = input("Prazo (dd/mm/yyyy): ").strip()
    
    print("Prioridade: 1. Normal | 2. Alta | 3. Urgente")
    prio_op = input("Escolha: ").strip()
    prioridade = {"1": "Normal", "2": "Alta", "3": "Urgente"}.get(prio_op, "Normal")

    nova_tarefa = {
        "id": str(uuid4()),
        "titulo": titulo,
        "descricao": descricao,
        "tipo_tarefa": "Manual",
        "setor": usuario_logado['setor'],
        "responsavel": usuario_logado['id'], # Atribui a si mesmo
        "prazo": prazo,
        "prioridade": prioridade,
        "status": STATUS_PENDENTE,
        "data_criacao": _data_atual(),
        "paciente_nome": "Tarefa Interna"
    }

    tarefas = _carregar_tarefas()
    tarefas.append(nova_tarefa)
    
    if _salvar_tarefas(tarefas):
        print("✓ Tarefa criada com sucesso!")
    else:
        print("Erro ao salvar tarefa.")

def editar_tarefa(usuario_logado: dict):
    """Edita uma tarefa existente do setor."""
    tarefas = _carregar_tarefas()
    setor = str(usuario_logado['setor']).lower()
    
    # Lista tarefas do setor que podem ser editadas
    meus_itens = [t for t in tarefas if str(t.get('setor')).lower() == setor]
    
    if not meus_itens:
        print("Nenhuma tarefa encontrada para editar.")
        return

    print("\n--- EDITAR TAREFA ---")
    for i, t in enumerate(meus_itens, 1):
        print(f"{i}. {t['titulo']} ({t['status']})")
    
    try:
        idx = int(input("\nNúmero da tarefa (0 cancela): ")) - 1
        if idx < 0: return
        alvo = meus_itens[idx]
    except:
        print("Opção inválida.")
        return

    print(f"\nEditando: {alvo['titulo']}")
    print("(Deixe em branco para manter o valor atual)")
    
    novo_titulo = input(f"Título [{alvo['titulo']}]: ").strip()
    if novo_titulo: alvo['titulo'] = novo_titulo
    
    novo_desc = input(f"Descrição [{alvo.get('descricao', '')}]: ").strip()
    if novo_desc: alvo['descricao'] = novo_desc
    
    novo_prazo = input(f"Prazo [{alvo.get('prazo', '')}]: ").strip()
    if novo_prazo: alvo['prazo'] = novo_prazo

    if _salvar_tarefas(tarefas):
        print("✓ Tarefa atualizada!")

def excluir_tarefa(usuario_logado: dict):
    """Exclui uma tarefa do setor."""
    tarefas = _carregar_tarefas()
    setor = str(usuario_logado['setor']).lower()
    
    # Lista tarefas do setor
    meus_itens = [t for t in tarefas if str(t.get('setor')).lower() == setor]
    
    if not meus_itens:
        print("Nenhuma tarefa disponível para excluir.")
        return

    print("\n--- EXCLUIR TAREFA ---")
    for i, t in enumerate(meus_itens, 1):
        print(f"{i}. {t['titulo']} ({t['status']})")
    
    try:
        idx = int(input("\nNúmero da tarefa para EXCLUIR (0 cancela): ")) - 1
        if idx < 0: return
        tarefa_para_excluir = meus_itens[idx]
    except:
        print("Opção inválida.")
        return

    confirmar = input(f"Tem certeza que deseja excluir '{tarefa_para_excluir['titulo']}'? (s/n): ")
    if confirmar.lower() == 's':
        # Remove da lista principal procurando pelo ID
        tarefas = [t for t in tarefas if t['id'] != tarefa_para_excluir['id']]
        
        if _salvar_tarefas(tarefas):
            print("✓ Tarefa excluída.")
    else:
        print("Operação cancelada.")

# --- FLUXO AUTOMÁTICO (MANTIDO) ---

def criar_paciente(usuario_logado: dict, nome: str, cpf: str, 
                   data_nascimento: str, telefone: str, 
                   tipo_atendimento: str, queixa: str) -> str:
    paciente_id = str(uuid4())
    # (Lógica de salvar paciente simplificada para focar nas tarefas)
    
    _criar_fluxo_atendimento(paciente_id, nome, tipo_atendimento, usuario_logado)
    return paciente_id

def _criar_fluxo_atendimento(paciente_id: str, nome_paciente: str, 
                             tipo_atendimento: str, usuario_criador: dict):
    tarefas = _carregar_tarefas()
    hoje = _data_atual()
    prazo_padrao = hoje
    
    t_triagem = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Triagem - {nome_paciente}",
        "descricao": f"Triagem inicial. Tipo: {tipo_atendimento}",
        "tipo_tarefa": "Triagem", "setor": "enfermagem",
        "responsavel": "sistema", "prazo": hoje,
        "prioridade": "Alta" if tipo_atendimento == "Emergência" else "Normal",
        "status": STATUS_PENDENTE, "data_criacao": hoje
    }
    tarefas.append(t_triagem)
    
    t_consulta = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Consulta Médica - {nome_paciente}",
        "descricao": "Realizar atendimento médico. Aguardando triagem.",
        "tipo_tarefa": "Consulta Médica", "setor": "médico",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Normal", "status": STATUS_PENDENTE,
        "dependencia": t_triagem['id'], "data_criacao": hoje
    }
    tarefas.append(t_consulta)
    
    t_farmacia = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Dispensação - {nome_paciente}",
        "descricao": "Dispensar medicamentos. Aguardando prescrição.",
        "tipo_tarefa": "Dispensação de Medicamento", "setor": "farmácia",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Normal", "status": "Aguardando Prescrição",
        "dependencia": t_consulta['id'], "data_criacao": hoje
    }
    tarefas.append(t_farmacia)
    
    t_admin = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Administrar Medicação - {nome_paciente}",
        "descricao": "Administrar medicamentos dispensados.",
        "tipo_tarefa": "Administração de Medicamento", "setor": "enfermagem",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Normal", "status": "Aguardando Medicamento",
        "dependencia": t_farmacia['id'], "data_criacao": hoje
    }
    tarefas.append(t_admin)
    
    t_verif = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Verificação Pós-Atendimento - {nome_paciente}",
        "descricao": "Verificar sinais vitais após atendimento.",
        "tipo_tarefa": "Verificação de Sinais", "setor": "enfermagem",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Normal", "status": STATUS_PENDENTE,
        "dependencia": t_consulta['id'], "data_criacao": hoje
    }
    tarefas.append(t_verif)
    
    t_alta = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Alta Médica - {nome_paciente}",
        "descricao": "Avaliar condições e liberar paciente.",
        "tipo_tarefa": "Alta Médica", "setor": "médico",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Normal", "status": "Aguardando Verificação",
        "dependencia": t_verif['id'], "data_criacao": hoje
    }
    tarefas.append(t_alta)
    
    _salvar_tarefas(tarefas)

# --- FUNÇÕES DE LISTAGEM E AÇÃO ---

def listar_tarefas_por_setor(usuario_logado):
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    print(f"\nTAREFAS DO SETOR: {setor_user.upper()}")
    encontrou = False
    for t in tarefas:
        if str(t.get('setor')).lower() == setor_user:
            encontrou = True
            resp = "Mim" if t.get('responsavel') == usuario_logado['id'] else "Equipe/Sistema"
            print(f"- [{t['status']}] {t['titulo']} (Resp: {resp})")
    
    if not encontrou:
        print(" Nenhuma tarefa encontrada.")

def concluir_tarefa_setor(usuario_logado):
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    pendentes = [t for t in tarefas if str(t.get('setor')).lower() == setor_user and t['status'] == STATUS_PENDENTE]
    
    if not pendentes:
        print("Nada pendente.")
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
        print("Concluída.")
    except:
        print("Erro.")

# --- MANTENDO FUNÇÕES ESPECÍFICAS DO HOSPITAL (Para não quebrar o CLI antigo) ---
def realizar_triagem(usuario_logado):
    # Lógica simplificada para CRUD (ou reimplementar se necessário)
    concluir_tarefa_setor(usuario_logado)

def realizar_atendimento_medico(usuario_logado):
    concluir_tarefa_setor(usuario_logado)

def dispensar_medicamento(usuario_logado):
    concluir_tarefa_setor(usuario_logado)

def administrar_medicamento(usuario_logado):
    concluir_tarefa_setor(usuario_logado)

def verificar_paciente(usuario_logado):
    concluir_tarefa_setor(usuario_logado)

def dar_alta_paciente(usuario_logado):
    concluir_tarefa_setor(usuario_logado)

def listar_pacientes_geral():
    print("Listagem de pacientes...")

def exibir_fila_por_setor():
    print("Exibindo fila...")

def listar_tarefas_por_status(u, s, tipo_tarefa=None):
    listar_tarefas_por_setor(u)