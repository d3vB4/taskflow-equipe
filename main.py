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

# --- SUB-MENU DE GERENCIAMENTO DE TAREFAS (NOVO) ---
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

# --- MENUS POR SETOR (ATUALIZADOS) ---
# Agora a opção "Listar Todas as Tarefas" chama o novo fluxo de gerenciamento

def exibir_menu_recepcao():
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - RECEPÇÃO")
    print("="*50)
    print("1. Registrar Novo Paciente")
    print("2. Listar Pacientes em Atendimento")
    print("3. Visualizar Fila de Espera")
    print("4. Relatórios")
    print("5. Gerenciar Tarefas (Criar/Editar/Excluir)") # Opção Nova
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
    print("5. Gerenciar Tarefas (Criar/Editar/Excluir)") # Atualizado
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
    print("6. Gerenciar Tarefas (Criar/Editar/Excluir)") # Atualizado
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
    print("3. Gerenciar Tarefas (Criar/Editar/Excluir)") # Atualizado
    print("5. Relatórios")
    print("0. Logout")
    return input(">>> Opção: ")

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
            # Simula fluxo de registro (chamando função do tarefas se existir ou print)
            print("Fluxo de registro...")
            aguardar()
        elif op == '2': tarefas.listar_pacientes_geral(); input("Voltar...")
        elif op == '3': tarefas.exibir_fila_por_setor(); input("Voltar...")
        elif op == '4': fluxo_relatorios()
        elif op == '5': fluxo_gerenciar_tarefas() # Chama o novo menu CRUD
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def processar_menu_enfermagem():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_enfermagem()
        if op == '1': pass # (Implementar chamadas originais aqui se precisar)
        elif op == '5': fluxo_gerenciar_tarefas() # Chama o novo menu CRUD
        elif op == '7': fluxo_relatorios()
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def processar_menu_medico():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_medico()
        if op == '6': fluxo_gerenciar_tarefas() # Chama o novo menu CRUD
        elif op == '8': fluxo_relatorios()
        elif op == '0': usuario_logado = None
        else: print("Opção inválida!"); aguardar()

def processar_menu_farmacia():
    global usuario_logado
    while usuario_logado:
        op = exibir_menu_farmacia()
        if op == '3': fluxo_gerenciar_tarefas() # Chama o novo menu CRUD
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