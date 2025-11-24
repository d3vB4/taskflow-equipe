import sys
import time

# Importa módulos dos outros desenvolvedores
try:
    import usuarios
    import tarefas
    import relatorios
except ImportError as e:
    print(f"ERRO CRÍTICO: Falha ao importar módulos.")
    print(f"Detalhe: {e}")
    sys.exit(1)

usuario_logado = None

def limpar_tela():
    print("\n" * 3)

def aguardar(segundos=1.5):
    time.sleep(segundos)

# --- MENU PRINCIPAL (NÃO LOGADO) ---
def exibir_menu_principal():
    limpar_tela()
    print("="*50)
    print("   SISTEMA HOSPITALAR - Gestão de Atendimentos")
    print("="*50)
    print("1. Login")
    print("2. Cadastrar Usuário (Colaborador)")
    print("3. Listar Colaboradores")
    print("4. Sair")
    print("-" * 50)
    return input(">>> Escolha uma opção: ")

# --- SUB-MENU DE GERENCIAMENTO DE TAREFAS ---
def fluxo_gerenciar_tarefas():
    """Menu CRUD de Tarefas."""
    while True:
        limpar_tela()
        print(f"\n--- GERENCIAMENTO DE TAREFAS ({usuario_logado['setor'].upper()}) ---")
        print("1. Listar Minhas Tarefas")
        print("2. Criar Nova Tarefa")
        print("3. Editar Tarefa Existente")
        print("4. Excluir Tarefa")
        print("5. Concluir Tarefa")
        print("0. Voltar")
        
        op = input(">>> Opção: ")
        
        if op == '1':
            tarefas.listar_tarefas_por_setor(usuario_logado)
            input("Enter para continuar...")
        elif op == '2':
            tarefas.criar_tarefa_manual(usuario_logado)
            aguardar()
        elif op == '3':
            tarefas.editar_tarefa(usuario_logado)
            aguardar()
        elif op == '4':
            tarefas.excluir_tarefa(usuario_logado)
            aguardar()
        elif op == '5':
            tarefas.concluir_tarefa_setor(usuario_logado)
            aguardar()
        elif op == '0':
            break
        else:
            print("Opção inválida.")
            aguardar()

# --- MENUS POR SETOR ---

def exibir_menu_recepcao():
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - RECEPÇÃO")
    print("="*50)
    print("1. Registrar Novo Paciente")
    print("2. Listar Pacientes em Atendimento")
    print("3. Visualizar Fila de Espera")
    print("4. Relatórios")
    print("5. Gerenciar Tarefas (Criar/Editar/Excluir)")
    print("0. Logout")
    return input(">>> Opção: ")

def exibir_menu_enfermagem():
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - ENFERMAGEM")
    print("="*50)
    print("1. Ver Pacientes para Triagem")
    print("2. Realizar Triagem")
    print("3. Administrar Medicamento")
    print("4. Verificar Paciente Pós-Atendimento")
    print("5. Gerenciar Tarefas (Criar/Editar/Excluir)")
    print("7. Relatórios")
    print("0. Logout")
    return input(">>> Opção: ")

def exibir_menu_medico():
    limpar_tela()
    print("="*50)
    print(f" Dr(a). {usuario_logado['nome']} - MÉDICO")
    print("="*50)
    print("1. Ver Pacientes Aguardando Consulta")
    print("2. Realizar Atendimento")
    print("3. Solicitar Exames/Procedimentos")
    print("4. Ver Pacientes para Alta")
    print("5. Dar Alta ao Paciente")
    print("6. Gerenciar Tarefas (Criar/Editar/Excluir)")
    print("8. Relatórios")
    print("0. Logout")
    return input(">>> Opção: ")

def exibir_menu_farmacia():
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - FARMÁCIA")
    print("="*50)
    print("1. Ver Receitas Pendentes")
    print("2. Dispensar Medicamento")
    print("3. Gerenciar Tarefas (Criar/Editar/Excluir)")
    print("5. Relatórios")
    print("0. Logout")
    return input(">>> Opção: ")

# --- FUNÇÕES DE REGISTRO DE PACIENTE (RESTAURADAS) ---

def fluxo_registrar_paciente():
    """Registra um novo paciente e inicia o workflow."""
    print("\n--- REGISTRAR NOVO PACIENTE ---")
    
    nome_paciente = input("Nome do Paciente: ").strip()
    if not nome_paciente:
        print("Erro: O nome não pode ficar em branco.")
        return
    
    cpf = input("CPF: ").strip()
    data_nascimento = input("Data de Nascimento (dd/mm/yyyy): ").strip()
    telefone = input("Telefone: ").strip()
    
    print("\nTipo de Atendimento:")
    print("1. Emergência")
    print("2. Consulta Eletiva")
    print("3. Retorno")
    tipo_atendimento = input("Escolha: ").strip()
    
    tipos = {"1": "Emergência", "2": "Consulta Eletiva", "3": "Retorno"}
    tipo_str = tipos.get(tipo_atendimento, "Consulta Eletiva")
    
    queixa = input("Queixa Principal: ").strip()
    
    try:
        # Cria o paciente (tarefa raiz)
        paciente_id = tarefas.criar_paciente(
            usuario_logado,
            nome_paciente,
            cpf,
            data_nascimento,
            telefone,
            tipo_str,
            queixa
        )
        print(f"\n✓ Paciente {nome_paciente} registrado com sucesso!")
        print(f"✓ Workflow iniciado (Triagem -> Médico -> etc).")
    except Exception as e:
        print(f"Erro ao registrar paciente: {e}")
    
    aguardar(2)

# --- FLUXOS DE AUTENTICAÇÃO ---
def fluxo_login():
    global usuario_logado
    print("\n--- LOGIN ---")
    usuario = usuarios.realizar_login()
    if usuario:
        usuario_logado = usuario
        print(f"Login realizado com sucesso! Setor: {usuario['setor']}")
        aguardar()
    else:
        print("Login ou senha inválidos.")
        aguardar()

def fluxo_cadastro():
    print("\n--- NOVO COLABORADOR ---")
    try:
        u = usuarios.cadastrar_usuario()
        print(f"Cadastrado com sucesso: {u['nome']}")
    except ValueError as e:
        print(f"Erro: {e}")
    aguardar()

# --- PROCESSAMENTO POR SETOR ---
def processar_menu_recepcao():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_recepcao()
        
        if op == '1': 
            fluxo_registrar_paciente()  # <--- CORREÇÃO: Chamando a função real
        elif op == '2': 
            tarefas.listar_pacientes_geral()
            input("Voltar...")
        elif op == '3': 
            tarefas.exibir_fila_por_setor()
            input("Voltar...")
        elif op == '4': 
            fluxo_relatorios()
        elif op == '5': 
            fluxo_gerenciar_tarefas()
        elif op == '0': 
            usuario_logado = None
        else: 
            print("Opção inválida!")
            aguardar()

def processar_menu_enfermagem():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_enfermagem()
        if op == '1': 
            print("Use o menu de 'Realizar Triagem' para ver a fila.") # Simulação
            aguardar()
        elif op == '2': tarefas.realizar_triagem(usuario_logado); aguardar()
        elif op == '3': tarefas.administrar_medicamento(usuario_logado); aguardar()
        elif op == '4': tarefas.verificar_paciente(usuario_logado); aguardar()
        elif op == '5': fluxo_gerenciar_tarefas()
        elif op == '7': fluxo_relatorios()
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def processar_menu_medico():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_medico()
        if op == '1': 
            print("Use 'Realizar Atendimento' para ver a fila.") # Simulação
            aguardar()
        elif op == '2': tarefas.realizar_atendimento_medico(usuario_logado); aguardar()
        elif op == '3': tarefas.solicitar_exames(usuario_logado); aguardar()
        elif op == '4': 
            print("Use 'Dar Alta' para ver a fila.")
            aguardar()
        elif op == '5': tarefas.dar_alta_paciente(usuario_logado); aguardar()
        elif op == '6': fluxo_gerenciar_tarefas()
        elif op == '8': fluxo_relatorios()
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def processar_menu_farmacia():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_farmacia()
        if op == '1': 
            print("Use 'Dispensar Medicamento' para ver a fila.")
            aguardar()
        elif op == '2': tarefas.dispensar_medicamento(usuario_logado); aguardar()
        elif op == '3': fluxo_gerenciar_tarefas()
        elif op == '5': fluxo_relatorios()
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def fluxo_relatorios():
    print("\n[RELATÓRIOS]")
    print("1. Tarefas Concluídas")
    print("2. Pendentes")
    print("3. Produtividade")
    print("4. Exportar TXT")
    op = input("Opção: ")
    if op == '1': relatorios.gerar_relatorio_concluidos(usuario_logado)
    elif op == '2': relatorios.gerar_relatorio_pendentes(usuario_logado)
    elif op == '3': relatorios.gerar_relatorio_produtividade(usuario_logado)
    elif op == '4': relatorios.exportar_relatorio_txt(usuario_logado)
    input("Enter para voltar...")

# --- MAIN ---
def main():
    global usuario_logado
    try:
        while True:
            if not usuario_logado:
                op = exibir_menu_principal()
                if op == '1': fluxo_login()
                elif op == '2': fluxo_cadastro()
                elif op == '3': 
                    for u in usuarios.listar_usuarios(): print(f"- {u['nome']}")
                    input("Voltar...")
                elif op == '4': sys.exit(0)
            else:
                setor = usuario_logado['setor'].lower()
                if 'recepção' in setor: processar_menu_recepcao()
                elif 'enfermagem' in setor: processar_menu_enfermagem()
                elif 'médico' in setor or 'medico' in setor: processar_menu_medico()
                elif 'farmácia' in setor or 'farmacia' in setor: processar_menu_farmacia()
                else:
                    print(f"Setor '{setor}' sem menu definido.")
                    usuario_logado = None
    except KeyboardInterrupt:
        print("\nSaindo...")
        sys.exit(0)

if __name__ == "__main__":
    main()