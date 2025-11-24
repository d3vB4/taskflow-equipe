import sys
import time

# Importa módulos dos outros desenvolvedores
try:
    import usuarios
    import tarefas
    import relatorios
except ImportError as e:
    print(f"ERRO CRÍTICO: Falha ao importar módulos. Verifique se usuarios.py, tarefas.py e relatorios.py existem.")
    print(f"Detalhe: {e}")
    sys.exit(1)

# Variável global para sessão do usuário
usuario_logado = None

def limpar_tela():
    """Simula a limpeza de tela imprimindo linhas vazias."""
    print("\n" * 3)

def aguardar(segundos=1.5):
    """Pausa para que o usuário possa ler a mensagem."""
    time.sleep(segundos)

# --- MENU PRINCIPAL (NÃO LOGADO) ---
def exibir_menu_principal():
    """Exibe o menu de entrada (não logado)."""
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

# --- MENU POR SETOR ---
def exibir_menu_recepcao():
    """Menu específico da Recepção."""
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - RECEPÇÃO")
    print("="*50)
    print("1. Registrar Novo Paciente")
    print("2. Listar Pacientes em Atendimento")
    print("3. Visualizar Fila de Espera")
    print("4. Relatórios")
    print("0. Logout")
    print("-" * 50)
    return input(">>> O que deseja fazer? ")

def exibir_menu_enfermagem():
    """Menu específico da Enfermagem."""
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - ENFERMAGEM")
    print("="*50)
    print("1. Ver Pacientes para Triagem")
    print("2. Realizar Triagem")
    print("3. Administrar Medicamento")
    print("4. Verificar Paciente Pós-Atendimento")
    print("5. Listar Todas as Tarefas")
    print("6. Concluir Tarefa")
    print("7. Relatórios")
    print("0. Logout")
    print("-" * 50)
    return input(">>> O que deseja fazer? ")

def exibir_menu_medico():
    """Menu específico do Médico."""
    limpar_tela()
    print("="*50)
    print(f" Dr(a). {usuario_logado['nome']} - MÉDICO")
    if usuario_logado.get('especialidade'):
        print(f" Especialidade: {usuario_logado['especialidade']}")
    print("="*50)
    print("1. Ver Pacientes Aguardando Consulta")
    print("2. Realizar Atendimento")
    print("3. Solicitar Exames/Procedimentos")
    print("4. Ver Pacientes para Alta")
    print("5. Dar Alta ao Paciente")
    print("6. Listar Todas as Tarefas")
    print("7. Concluir Tarefa")
    print("8. Relatórios")
    print("0. Logout")
    print("-" * 50)
    return input(">>> O que deseja fazer? ")

def exibir_menu_farmacia():
    """Menu específico da Farmácia."""
    limpar_tela()
    print("="*50)
    print(f" Bem-vindo, {usuario_logado['nome']} - FARMÁCIA")
    print("="*50)
    print("1. Ver Receitas Pendentes")
    print("2. Dispensar Medicamento")
    print("3. Listar Todas as Tarefas")
    print("4. Concluir Tarefa")
    print("5. Relatórios")
    print("0. Logout")
    print("-" * 50)
    return input(">>> O que deseja fazer? ")

# --- FLUXO DE AUTENTICAÇÃO ---
def fluxo_login():
    """Gerencia a tentativa de login usando o módulo usuarios."""
    global usuario_logado
    print("\n--- LOGIN ---")
    usuario = usuarios.realizar_login()
    
    if usuario:
        usuario_logado = usuario
        print(f"Login realizado com sucesso! Bem-vindo ao setor: {usuario['setor']}")
        aguardar()
    else:
        print("Login ou senha inválidos.")
        aguardar()

def fluxo_cadastro():
    """Gerencia o cadastro usando o módulo usuarios."""
    print("\n--- NOVO COLABORADOR ---")
    try:
        usuario = usuarios.cadastrar_usuario()
        print(f"Colaborador cadastrado com sucesso no setor: {usuario['setor']}!")
        print("Faça login para entrar no sistema.")
    except ValueError as e:
        print(f"Erro ao cadastrar: {e}")
    aguardar()

# --- FLUXOS DE RECEPÇÃO ---
def fluxo_registrar_paciente():
    """Registra um novo paciente e cria as tarefas iniciais do fluxo hospitalar."""
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
    
    if paciente_id:
        print(f"\n✓ Paciente {nome_paciente} registrado com sucesso!")
        print(f"✓ Tarefas criadas automaticamente para o fluxo de atendimento.")
        print(f"  ID do Paciente: {paciente_id[:8]}...")
    else:
        print("Erro ao registrar paciente.")
    
    aguardar(2)

def fluxo_listar_pacientes_recepcao():
    """Lista pacientes em atendimento (visão recepção)."""
    print("\n--- PACIENTES EM ATENDIMENTO ---")
    tarefas.listar_pacientes_geral()
    input("\nPressione Enter para voltar...")

def fluxo_fila_espera():
    """Mostra fila de espera por setor."""
    print("\n--- FILA DE ESPERA POR SETOR ---")
    tarefas.exibir_fila_por_setor()
    input("\nPressione Enter para voltar...")

# --- FLUXOS DE ENFERMAGEM ---
def fluxo_ver_pacientes_triagem():
    """Lista pacientes aguardando triagem."""
    print("\n--- PACIENTES AGUARDANDO TRIAGEM ---")
    tarefas.listar_tarefas_por_status(usuario_logado, "Pendente", tipo_tarefa="Triagem")
    input("\nPressione Enter para voltar...")

def fluxo_realizar_triagem():
    """Realiza triagem de um paciente."""
    print("\n--- REALIZAR TRIAGEM ---")
    tarefas.realizar_triagem(usuario_logado)
    aguardar(2)

def fluxo_administrar_medicamento():
    """Administra medicamento ao paciente."""
    tarefas.administrar_medicamento(usuario_logado)
    aguardar(2)

def fluxo_verificar_paciente():
    """Verifica sinais vitais pós-atendimento."""
    tarefas.verificar_paciente(usuario_logado)
    aguardar(2)

# --- FLUXOS DE MÉDICO ---
def fluxo_ver_pacientes_consulta():
    """Lista pacientes aguardando consulta médica."""
    print("\n--- PACIENTES AGUARDANDO CONSULTA ---")
    tarefas.listar_tarefas_por_status(usuario_logado, "Pendente", tipo_tarefa="Consulta Médica")
    input("\nPressione Enter para voltar...")

def fluxo_realizar_atendimento():
    """Realiza atendimento médico."""
    print("\n--- REALIZAR ATENDIMENTO MÉDICO ---")
    tarefas.realizar_atendimento_medico(usuario_logado)
    aguardar(2)

def fluxo_solicitar_exames():
    """Solicita exames ou procedimentos."""
    print("\n--- SOLICITAR EXAMES/PROCEDIMENTOS ---")
    tarefas.solicitar_exames(usuario_logado)
    aguardar(2)

def fluxo_ver_pacientes_alta():
    """Lista pacientes prontos para alta."""
    print("\n--- PACIENTES PRONTOS PARA ALTA ---")
    tarefas.listar_tarefas_por_status(usuario_logado, "Pendente", tipo_tarefa="Alta Médica")
    input("\nPressione Enter para voltar...")

def fluxo_dar_alta():
    """Realiza alta médica do paciente."""
    tarefas.dar_alta_paciente(usuario_logado)
    aguardar(2)

# --- FLUXOS DE FARMÁCIA ---
def fluxo_ver_receitas():
    """Lista receitas pendentes."""
    print("\n--- RECEITAS PENDENTES ---")
    tarefas.listar_tarefas_por_status(usuario_logado, "Pendente", tipo_tarefa="Dispensação de Medicamento")
    input("\nPressione Enter para voltar...")

def fluxo_dispensar_medicamento():
    """Dispensa medicamento."""
    print("\n--- DISPENSAR MEDICAMENTO ---")
    tarefas.dispensar_medicamento(usuario_logado)
    aguardar(2)

# --- FLUXOS COMUNS ---
def fluxo_listar_tarefas():
    """Lista todas as tarefas do setor do usuário."""
    print(f"\n--- TAREFAS DO SETOR: {usuario_logado['setor'].upper()} ---")
    tarefas.listar_tarefas_por_setor(usuario_logado)
    input("\nPressione Enter para voltar...")

def fluxo_concluir_tarefa():
    """Conclui uma tarefa do setor."""
    print("\n--- CONCLUIR TAREFA ---")
    tarefas.concluir_tarefa_setor(usuario_logado)
    aguardar(2)

def fluxo_relatorios():
    """Sub-menu de relatórios."""
    print("\n[RELATÓRIOS]")
    print("1. Tarefas Concluídas")
    print("2. Pendentes/Atrasadas")
    print("3. Produtividade da Equipe")
    print("4. Exportar para TXT")
    sub = input("Opção: ")
    
    if sub == '1':
        relatorios.gerar_relatorio_concluidos(usuario_logado)
    elif sub == '2':
        relatorios.gerar_relatorio_pendentes(usuario_logado)
    elif sub == '3':
        relatorios.gerar_relatorio_produtividade(usuario_logado)
    elif sub == '4':
        relatorios.exportar_relatorio_txt(usuario_logado)
    
    input("\nPressione Enter para voltar...")

# --- PROCESSAMENTO POR SETOR ---
def processar_menu_recepcao():
    """Processa menu da recepção."""
    global usuario_logado
    while usuario_logado:
        opcao = exibir_menu_recepcao()
        
        if opcao == '1':
            fluxo_registrar_paciente()
        elif opcao == '2':
            fluxo_listar_pacientes_recepcao()
        elif opcao == '3':
            fluxo_fila_espera()
        elif opcao == '4':
            fluxo_relatorios()
        elif opcao == '0':
            print("Saindo...")
            usuario_logado = None
        else:
            print("Opção inválida!")
            aguardar()

def processar_menu_enfermagem():
    """Processa menu da enfermagem."""
    global usuario_logado
    while usuario_logado:
        opcao = exibir_menu_enfermagem()
        
        if opcao == '1':
            fluxo_ver_pacientes_triagem()
        elif opcao == '2':
            fluxo_realizar_triagem()
        elif opcao == '3':
            fluxo_administrar_medicamento()
        elif opcao == '4':
            fluxo_verificar_paciente()
        elif opcao == '5':
            fluxo_listar_tarefas()
        elif opcao == '6':
            fluxo_concluir_tarefa()
        elif opcao == '7':
            fluxo_relatorios()
        elif opcao == '0':
            print("Saindo...")
            usuario_logado = None
        else:
            print("Opção inválida!")
            aguardar()

def processar_menu_medico():
    """Processa menu do médico."""
    global usuario_logado
    while usuario_logado:
        opcao = exibir_menu_medico()
        
        if opcao == '1':
            fluxo_ver_pacientes_consulta()
        elif opcao == '2':
            fluxo_realizar_atendimento()
        elif opcao == '3':
            fluxo_solicitar_exames()
        elif opcao == '4':
            fluxo_ver_pacientes_alta()
        elif opcao == '5':
            fluxo_dar_alta()
        elif opcao == '6':
            fluxo_listar_tarefas()
        elif opcao == '7':
            fluxo_concluir_tarefa()
        elif opcao == '8':
            fluxo_relatorios()
        elif opcao == '0':
            print("Saindo...")
            usuario_logado = None
        else:
            print("Opção inválida!")
            aguardar()

def processar_menu_farmacia():
    """Processa menu da farmácia."""
    global usuario_logado
    while usuario_logado:
        opcao = exibir_menu_farmacia()
        
        if opcao == '1':
            fluxo_ver_receitas()
        elif opcao == '2':
            fluxo_dispensar_medicamento()
        elif opcao == '3':
            fluxo_listar_tarefas()
        elif opcao == '4':
            fluxo_concluir_tarefa()
        elif opcao == '5':
            fluxo_relatorios()
        elif opcao == '0':
            print("Saindo...")
            usuario_logado = None
        else:
            print("Opção inválida!")
            aguardar()

# --- MAIN ---
def main():
    """Loop principal do programa."""
    global usuario_logado
    try:
        while True:
            if not usuario_logado:
                opcao = exibir_menu_principal()
                
                if opcao == '1':
                    fluxo_login()
                elif opcao == '2':
                    fluxo_cadastro()
                elif opcao == '3':
                    print("\n--- COLABORADORES CADASTRADOS ---")
                    for u in usuarios.listar_usuarios():
                        print(f"- {u['nome']} ({u['setor']}) - Login: {u['login']}")
                    input("\nPressione Enter para voltar...")
                elif opcao == '4':
                    print("Encerrando Sistema Hospitalar. Até logo!")
                    sys.exit(0)
                else:
                    print("Opção inválida, tente novamente.")
                    aguardar()
            else:
                # Roteia para o menu correto baseado no setor
                setor = usuario_logado['setor'].lower()
                
                if setor == 'recepção':
                    processar_menu_recepcao()
                elif setor == 'enfermagem':
                    processar_menu_enfermagem()
                elif setor == 'médico':
                    processar_menu_medico()
                elif setor == 'farmácia':
                    processar_menu_farmacia()
                else:
                    print(f"Setor '{usuario_logado['setor']}' não possui menu específico.")
                    usuario_logado = None

    except KeyboardInterrupt:
        print("\n\nInterrupção forçada (Ctrl+C). Saindo...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[ERRO FATAL] Ocorreu um erro inesperado: {e}")
        print("Por favor, contate o suporte.")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()