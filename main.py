import sys
import time

# Tenta importar os módulos dos outros desenvolvedores.
# Isso satisfaz os Cards 5 e 6 (Integração).
try:
    import usuarios   # Dev 2
    import tarefas    # Dev 3
    import relatorios # Dev 4
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

# --- CARD 4: MENU PRINCIPAL ---
def exibir_menu_principal():
    """Exibe o menu de entrada (não logado)."""
    limpar_tela()
    print("="*40)
    print("      TASKFLOW - Gestão de Tarefas      ")
    print("="*40)
    print("1. Login")
    print("2. Cadastrar Usuário")
    print("3. Sair")
    print("-" * 40)
    return input(">>> Escolha uma opção: ")

# --- CARD 6: MENU DE TAREFAS ---
def exibir_menu_tarefas():
    """Exibe o menu de operações (usuário logado)."""
    limpar_tela()
    print("="*40)
    print(f" Bem-vindo, {usuario_logado['nome']}! ")
    print("="*40)
    print("1. Nova Tarefa")
    print("2. Listar Tarefas")
    print("3. Editar Tarefa")
    print("4. Excluir Tarefa")
    print("5. Concluir Tarefa")
    print("6. Relatórios")
    print("0. Logout")
    print("-" * 40)
    return input(">>> O que deseja fazer? ")

# --- CARD 5: FLUXO DE AUTENTICAÇÃO ---
def fluxo_login():
    """Gerencia a tentativa de login usando o módulo usuarios."""
    global usuario_logado
    print("\n--- LOGIN ---")
    # Chama a função do Dev 2
    usuario = usuarios.realizar_login()
    
    if usuario:
        usuario_logado = usuario
        print("Login realizado com sucesso!")
        aguardar()
    else:
        print("Login ou senha inválidos.")
        aguardar()

def fluxo_cadastro():
    """Gerencia o cadastro usando o módulo usuarios."""
    print("\n--- NOVO USUÁRIO ---")
    # Chama a função do Dev 2
    if usuarios.cadastra1r_usuario():
        print("Usuário cadastrado com sucesso! Faça login para entrar.")
    else:
        print("Erro ao cadastrar usuário.")
    aguardar()

# --- LOGICA DO MENU DE TAREFAS ---
def processar_menu_tarefas():
    """Processa as opções do usuário logado."""
    global usuario_logado
    while usuario_logado:
        opcao = exibir_menu_tarefas()
        
        if opcao == '1':
            tarefas.cadastrar_tarefa(usuario_logado)
        elif opcao == '2':
            tarefas.listar_tarefas(usuario_logado)
            input("\nPressione Enter para voltar...")
        elif opcao == '3':
            tarefas.editar_tarefa(usuario_logado)
        elif opcao == '4':
            tarefas.excluir_tarefa(usuario_logado)
        elif opcao == '5':
            tarefas.concluir_tarefa(usuario_logado)
        elif opcao == '6':
            # Sub-menu de relatórios (Dev 4)
            print("\n[Relatórios]")
            print("1. Tarefas Concluídas")
            print("2. Pendentes/Atrasadas")
            sub = input("Opção: ")
            if sub == '1':
                relatorios.gerar_relatorio_concluidas(usuario_logado)
            elif sub == '2':
                relatorios.gerar_relatorio_pendentes(usuario_logado)
            input("\nPressione Enter para voltar...")
        elif opcao == '0':
            print("Saindo...")
            usuario_logado = None # Logout
        else:
            print("Opção inválida!")
            aguardar()

# --- CARD 7: TRATAMENTO GLOBAL DE ERROS ---
def main():
    """Loop principal do programa."""
    try:
        while True:
            if not usuario_logado:
                opcao = exibir_menu_principal()
                
                if opcao == '1':
                    fluxo_login()
                elif opcao == '2':
                    fluxo_cadastro()
                elif opcao == '3':
                    print("Encerrando TaskFlow. Até logo!")
                    sys.exit(0)
                else:
                    print("Opção inválida, tente novamente.")
                    aguardar()
            else:
                # Se usuário está logado, vai para o menu de tarefas
                processar_menu_tarefas()

    except KeyboardInterrupt:
        # Trata quando o usuário aperta Ctrl+C
        print("\n\nInterrupção forçada (Ctrl+C). Saindo...")
        sys.exit(0)
    except Exception as e:
        # Captura qualquer erro não previsto para o app não 'explodir' na cara do usuário
        print(f"\n\n[ERRO FATAL] Ocorreu um erro inesperado: {e}")
        print("Por favor, contate o suporte.")
        sys.exit(1)

if __name__ == "__main__":
    main()