from uuid import uuid4
from datetime import datetime, timedelta
import os
import ast  # Para converter strings de dicionários de volta para dict

# Importa módulos locais (apenas para logging de usuário ou tipos, se necessário)
# Não usamos mais arquivos.py para tarefas para garantir a integridade do esquema
import usuarios 

# --- CONFIGURAÇÕES E CONSTANTES ---
ARQUIVO_TAREFAS = "tarefas.txt"
ARQUIVO_PACIENTES = "pacientes.txt"

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"
STATUS_CANCELADA = "Cancelada"

# Definição estrita das colunas para garantir que o relatório funcione
COLUNAS_TAREFAS = [
    'id', 'paciente_id', 'paciente_nome', 'titulo', 'descricao',
    'tipo_tarefa', 'setor', 'responsavel', 'prazo', 'prioridade',
    'status', 'dependencia', 'data_criacao', 'data_conclusao',
    'concluida_por', 'prescricao', 'observacoes', 
    'dados_triagem', 'sinais_vitais', 'estado_geral', 
    'lote_medicamento', 'via_administracao', 'dose'
    'atendimento_token'
]

# --- FUNÇÕES AUXILIARES DE PERSISTÊNCIA (CORE FIX) ---

def _escape(valor):
    """Trata caracteres especiais para salvar no TXT sem quebrar o pipe."""
    if valor is None: 
        return ''
    # Se for dicionário (ex: dados da triagem), converte para string
    if isinstance(valor, dict):
        return str(valor).replace('|', '<PIPE>').replace('\n', '<NL>')
    return str(valor).replace('|', '<PIPE>').replace('\n', '<NL>')

def _unescape(valor):
    """Restaura caracteres e tenta converter strings de volta para objetos."""
    if not valor or valor == 'None' or valor == '': 
        return None
    
    texto = valor.replace('<PIPE>', '|').replace('<NL>', '\n')
    
    # Tenta converter string de dicionário "{'a': 1}" de volta para dict
    if texto.startswith('{') and texto.endswith('}'):
        try:
            return ast.literal_eval(texto)
        except:
            return texto
    return texto

def _salvar_tarefas(tarefas: list) -> bool:
    """
    Salva as tarefas forçando a escrita de TODAS as colunas definidas em COLUNAS_TAREFAS.
    Isso corrige o bug de relatórios vazios.
    """
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            # Escreve Cabeçalho
            f.write('|'.join(COLUNAS_TAREFAS) + '\n')
            
            for t in tarefas:
                linha = []
                for col in COLUNAS_TAREFAS:
                    valor = t.get(col)
                    linha.append(_escape(valor))
                f.write('|'.join(linha) + '\n')
        return True
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")
        return False

def _carregar_tarefas() -> list:
    """Carrega as tarefas mapeando as colunas corretamente."""
    if not os.path.exists(ARQUIVO_TAREFAS):
        return []

    lista_tarefas = []
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
            # Se arquivo vazio ou só cabeçalho
            if len(linhas) < 2: 
                return []

            # Ignoramos o cabeçalho do arquivo e usamos nossa constante para garantir ordem
            # Mas verificamos se o arquivo não está corrompido
            
            for linha in linhas[1:]:
                linha = linha.strip()
                if not linha: continue
                
                partes = linha.split('|')
                
                # Reconstrói o dicionário
                tarefa = {}
                for i, col in enumerate(COLUNAS_TAREFAS):
                    if i < len(partes):
                        tarefa[col] = _unescape(partes[i])
                    else:
                        tarefa[col] = None
                
                lista_tarefas.append(tarefa)
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
        return []
    
    return lista_tarefas

# --- PERSISTÊNCIA SIMPLIFICADA PARA PACIENTES ---
# Mantemos uma lógica simples para pacientes, já que o foco do erro era nas tarefas
def _carregar_pacientes() -> list:
    import utils.arquivos as arq
    return arq.carregar_dados(ARQUIVO_PACIENTES)

def _salvar_pacientes(pacientes: list) -> bool:
    import utils.arquivos as arq
    return arq.salvar_dados(pacientes, ARQUIVO_PACIENTES)

# --- FUNÇÕES DE DATA/HORA ---

def _data_atual():
    return datetime.now().strftime("%d/%m/%Y")

def _hora_atual():
    return datetime.now().strftime("%H:%M")

def _buscar_tarefa_por_id(id_tarefa: str, tarefas: list = None):
    if tarefas is None: tarefas = _carregar_tarefas()
    for t in tarefas:
        if t['id'] == id_tarefa: return t
    return None

def _buscar_paciente_por_id(id_paciente: str, pacientes: list = None):
    if pacientes is None: pacientes = _carregar_pacientes()
    for p in pacientes:
        if p['id'] == id_paciente: return p
    return None

# --- FLUXO DE CRIAÇÃO (WORKFLOW) ---

def criar_paciente(usuario_logado: dict, nome: str, cpf: str, 
                   data_nascimento: str, telefone: str, 
                   tipo_atendimento: str, queixa: str) -> str:
    paciente_id = str(uuid4())
    novo_paciente = {
        "id": paciente_id,
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "tipo_atendimento": tipo_atendimento,
        "queixa_principal": queixa,
        "data_entrada": _data_atual(),
        "hora_entrada": _hora_atual(),
        "status_atendimento": "Em Atendimento",
        "responsavel_registro": usuario_logado['id']
    }
    
    pacientes = _carregar_pacientes()
    pacientes.append(novo_paciente)
    _salvar_pacientes(pacientes)
    
    _criar_fluxo_atendimento(paciente_id, nome, tipo_atendimento, usuario_logado)
    return paciente_id

def _criar_fluxo_atendimento(paciente_id: str, nome_paciente: str, 
                             tipo_atendimento: str, usuario_criador: dict):
    tarefas = _carregar_tarefas()
    hoje = _data_atual()
    
    # Define prazos básicos
    prazo_padrao = hoje 
    
    # 1. Triagem (Enfermagem)
    t_triagem = {
        "id": str(uuid4()), "paciente_id": paciente_id, "paciente_nome": nome_paciente,
        "titulo": f"Triagem - {nome_paciente}",
        "descricao": f"Realizar triagem inicial. Tipo: {tipo_atendimento}",
        "tipo_tarefa": "Triagem", "setor": "enfermagem",
        "responsavel": "sistema", "prazo": prazo_padrao,
        "prioridade": "Alta" if tipo_atendimento == "Emergência" else "Normal",
        "status": STATUS_PENDENTE, "data_criacao": hoje
    }
    tarefas.append(t_triagem)
    
    # 2. Consulta Médica
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
    
    # 3. Farmácia (Espera)
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
    
    # 4. Enfermagem (Administração - Espera)
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
    
    # 5. Enfermagem (Verificação)
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
    
    # 6. Alta Médica
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

# --- AÇÕES DE ENFERMAGEM ---

def realizar_triagem(usuario_logado: dict):
    tarefas = _carregar_tarefas()
    # Filtra tarefas
    pendentes = [t for t in tarefas if t['tipo_tarefa'] == 'Triagem' and t['status'] == STATUS_PENDENTE]
    
    if not pendentes:
        print(">> Nenhuma triagem pendente.")
        return

    print("\n--- PACIENTES NA FILA DE TRIAGEM ---")
    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['paciente_nome']} ({t['prioridade']})")
    
    try:
        idx = int(input("\nSelecione o número (0 volta): ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except:
        return

    print(f"\nRealizando triagem de: {selecionada['paciente_nome']}")
    pa = input("PA: ")
    temp = input("Temp: ")
    fc = input("FC: ")
    classificacao = input("Classificação de Risco (Emergência/Urgente/Normal): ")
    obs = input("Observações: ")

    # Atualiza tarefa atual
    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['observacoes'] = obs
    selecionada['dados_triagem'] = {
        'pa': pa, 'temperatura': temp, 'freq_cardiaca': fc, 'risco': classificacao
    }

    # Atualiza prioridade da Consulta Médica vinculada
    for t in tarefas:
        if t['paciente_id'] == selecionada['paciente_id'] and t['tipo_tarefa'] == 'Consulta Médica':
            if classificacao.lower() in ['emergencia', 'emergência']:
                t['prioridade'] = 'Alta'
                t['descricao'] += " [RISCO ALTO]"
    
    _salvar_tarefas(tarefas)
    print("✓ Triagem realizada.")

def administrar_medicamento(usuario_logado):
    tarefas = _carregar_tarefas()
    pendentes = [t for t in tarefas if t['tipo_tarefa'] == 'Administração de Medicamento' and t['status'] == STATUS_PENDENTE]
    
    if not pendentes:
        print(">> Nenhuma administração pendente.")
        return
        
    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['paciente_nome']} - {t.get('descricao')}")
    
    try:
        idx = int(input("Selecione: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except: return

    via = input("Via (Oral/IV/IM): ")
    obs = input("Observações: ")

    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['via_administracao'] = via
    selecionada['observacoes'] = obs
    
    _salvar_tarefas(tarefas)
    print("✓ Medicamento administrado.")

def verificar_paciente(usuario_logado):
    tarefas = _carregar_tarefas()
    # Só pode verificar se a consulta já acabou (dependencia)
    pendentes = []
    for t in tarefas:
        if t['tipo_tarefa'] == 'Verificação de Sinais' and t['status'] == STATUS_PENDENTE:
            # Checa dependencia
            dep_id = t.get('dependencia')
            dep_ok = True
            if dep_id:
                dep_task = _buscar_tarefa_por_id(dep_id, tarefas)
                if dep_task and dep_task['status'] != STATUS_CONCLUIDA:
                    dep_ok = False
            
            if dep_ok:
                pendentes.append(t)

    if not pendentes:
        print(">> Nenhuma verificação disponível (aguarde consultas).")
        return

    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['paciente_nome']}")
    
    try:
        idx = int(input("Selecione: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except: return

    print("Verificando sinais...")
    estado = input("Estado geral (Estável/Instável): ")
    apto = input("Apto para alta? (s/n): ")
    
    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['estado_geral'] = estado
    
    # Libera Alta Médica se apto
    if apto.lower() == 's':
        for t in tarefas:
            if t['paciente_id'] == selecionada['paciente_id'] and t['tipo_tarefa'] == 'Alta Médica':
                t['status'] = STATUS_PENDENTE
                t['descricao'] += f" | Paciente {estado}"

    _salvar_tarefas(tarefas)
    print("✓ Verificação registrada.")

# --- AÇÕES DE MÉDICO ---

def realizar_atendimento_medico(usuario_logado):
    tarefas = _carregar_tarefas()
    # Consulta depende de triagem?
    pendentes = []
    for t in tarefas:
        if t['tipo_tarefa'] == 'Consulta Médica' and t['status'] == STATUS_PENDENTE:
            dep_id = t.get('dependencia')
            # Se tiver dependencia, checa se está concluida
            pode_atender = True
            if dep_id:
                triagem = _buscar_tarefa_por_id(dep_id, tarefas)
                if triagem and triagem['status'] != STATUS_CONCLUIDA:
                    pode_atender = False
            
            if pode_atender:
                pendentes.append(t)
    
    if not pendentes:
        print(">> Nenhuma consulta pronta para atendimento.")
        return

    # Ordena por prioridade (Alta primeiro)
    pendentes.sort(key=lambda x: x.get('prioridade') == 'Alta', reverse=True)

    print("\n--- PACIENTES AGUARDANDO MÉDICO ---")
    for i, t in enumerate(pendentes, 1):
        prio = "🚨" if t['prioridade'] == 'Alta' else ""
        print(f"{i}. {prio} {t['paciente_nome']}")

    try:
        idx = int(input("Selecione: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except: return

    # Mostra dados da triagem se houver
    if selecionada.get('dependencia'):
        triagem = _buscar_tarefa_por_id(selecionada['dependencia'], tarefas)
        if triagem and triagem.get('dados_triagem'):
            print(f"Dados Triagem: {triagem['dados_triagem']}")

    diag = input("Diagnóstico: ")
    prescrever = input("Prescrever medicamentos? (s/n): ")
    prescricao_texto = ""
    
    if prescrever.lower() == 's':
        prescricao_texto = input("Medicamentos: ")
        # Ativa Farmácia
        for t in tarefas:
            if t['paciente_id'] == selecionada['paciente_id'] and t['tipo_tarefa'] == 'Dispensação de Medicamento':
                t['status'] = STATUS_PENDENTE
                t['prescricao'] = prescricao_texto
                t['descricao'] = f"Dispensar: {prescricao_texto}"
    else:
        # Se não prescreveu, cancela farmácia e adm e libera verificação
        for t in tarefas:
            if t['paciente_id'] == selecionada['paciente_id']:
                if t['tipo_tarefa'] in ['Dispensação de Medicamento', 'Administração de Medicamento']:
                    t['status'] = 'Cancelada (Não prescrito)'
                if t['tipo_tarefa'] == 'Verificação de Sinais':
                    # Remove dependencia da farmacia/adm se houver, vincula direto a consulta
                    t['dependencia'] = selecionada['id']

    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['observacoes'] = f"Diag: {diag}"
    
    _salvar_tarefas(tarefas)
    print("✓ Atendimento finalizado.")

def solicitar_exames(usuario_logado):
    print("Funcionalidade futura.")

def dar_alta_paciente(usuario_logado):
    tarefas = _carregar_tarefas()
    pendentes = [t for t in tarefas if t['tipo_tarefa'] == 'Alta Médica' and t['status'] == STATUS_PENDENTE]

    if not pendentes:
        print(">> Nenhuma alta pendente.")
        return

    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['paciente_nome']}")

    try:
        idx = int(input("Selecione: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except: return

    orientacoes = input("Orientações de Alta: ")
    
    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['observacoes'] = orientacoes

    # Finaliza paciente
    pacientes = _carregar_pacientes()
    pac = _buscar_paciente_por_id(selecionada['paciente_id'], pacientes)
    if pac:
        pac['status_atendimento'] = "Alta Concluída"
        _salvar_pacientes(pacientes)
    
    _salvar_tarefas(tarefas)
    print("✓ Alta realizada.")

# --- AÇÕES DE FARMÁCIA ---

def dispensar_medicamento(usuario_logado):
    tarefas = _carregar_tarefas()
    pendentes = [t for t in tarefas if t['tipo_tarefa'] == 'Dispensação de Medicamento' and t['status'] == STATUS_PENDENTE]

    if not pendentes:
        print(">> Nenhuma dispensação pendente.")
        return

    for i, t in enumerate(pendentes, 1):
        print(f"{i}. {t['paciente_nome']} - Prescrição: {t.get('prescricao')}")

    try:
        idx = int(input("Selecione: ")) - 1
        if idx < 0: return
        selecionada = pendentes[idx]
    except: return

    lote = input("Lote: ")
    
    selecionada['status'] = STATUS_CONCLUIDA
    selecionada['data_conclusao'] = _data_atual()
    selecionada['concluida_por'] = usuario_logado['id']
    selecionada['lote_medicamento'] = lote

    # Libera administração
    for t in tarefas:
        if t['paciente_id'] == selecionada['paciente_id'] and t['tipo_tarefa'] == 'Administração de Medicamento':
            t['status'] = STATUS_PENDENTE
            t['descricao'] = f"Administrar: {selecionada.get('prescricao')}"
    
    _salvar_tarefas(tarefas)
    print("✓ Medicamento dispensado.")

# --- LISTAGENS E RELATÓRIOS ---

def listar_tarefas_por_setor(usuario_logado):
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    print(f"\nTAREFAS DO SETOR: {setor_user.upper()}")
    encontrou = False
    for t in tarefas:
        if str(t.get('setor')).lower() == setor_user:
            encontrou = True
            print(f"- [{t['status']}] {t['titulo']} (Prazo: {t['prazo']})")
    
    if not encontrou:
        print(" Nenhuma tarefa encontrada.")

def listar_tarefas_por_status(usuario_logado, status, tipo_tarefa=None):
    tarefas = _carregar_tarefas()
    setor_user = str(usuario_logado['setor']).lower()
    
    count = 0
    for t in tarefas:
        eh_do_setor = str(t.get('setor')).lower() == setor_user
        mesmo_status = t['status'] == status
        mesmo_tipo = (tipo_tarefa is None) or (t['tipo_tarefa'] == tipo_tarefa)
        
        if eh_do_setor and mesmo_status and mesmo_tipo:
            count += 1
            print(f"- {t['titulo']}")
    
    if count == 0:
        print(f"Nenhum registro encontrado.")

def exibir_fila_por_setor():
    tarefas = _carregar_tarefas()
    setores = ['enfermagem', 'médico', 'farmácia']
    
    for setor in setores:
        lista = [t for t in tarefas if str(t.get('setor')).lower() == setor and t['status'] == STATUS_PENDENTE]
        print(f"\n=== {setor.upper()} ({len(lista)}) ===")
        for t in lista:
            print(f" > {t['paciente_nome']} - {t['tipo_tarefa']}")

def concluir_tarefa_setor(usuario_logado):
    # Função genérica para concluir tarefas que não têm fluxo específico
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

def listar_pacientes_geral():
    pacientes = _carregar_pacientes()
    print("\n--- PACIENTES ---")
    for p in pacientes:
        if p.get('status_atendimento') != 'Alta Concluída':
            print(f"Nome: {p['nome']} | Status: {p['status_atendimento']}")
