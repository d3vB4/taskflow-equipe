from os import name
import time
import sys


try:
    import usuarios
    import tarefas
    import relatorios
except ImportError:
    print("ERRO: Certifique-se que os arquivos 'usuarios.py', 'tarefas.py', e 'relatorios.py' estão na mesma pasta.")
    sys.exit(1)
# -------------------------------------------

# Variável global para armazenar os dados do usuário logado
usuario_logado = None

def limpar_tela():
    """Limpa o console (simples, apenas rolando a tela)."""
    print("\n" * 40)

def aguardar(segundos=2):
    """Pausa a execução por alguns segundos."""
    time.sleep(segundos)


def exibir_menu_principal():
    """Exibe o menu inicial de login e cadastro."""
    limpar_tela()
    print("==========================================")
    print("   TASKFLOW - Sistema de Tarefas   ")
    print("==========================================")
    print("1. Realizar Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Sair do Sistema")
    print("------------------------------------------")
    return input("Escolha uma opção: ")


def exibir_menu_tarefas():
    """Exibe o menu de ações do usuário logado."""
    limpar_tela()
    global usuario_logado
    
    print(f"================== TASKFLOW ==================")
    print(f"Usuário: {usuario_logado.get('nome', 'Desconhecido')}")
    print("------------------------------------------")
    print("1. Criar Nova Tarefa")
    print("2. Listar Minhas Tarefas")
    print("3. Editar Tarefa")
    print("4. Excluir Tarefa")
    print("5. Marcar Tarefa como Concluída")
    print("6. Ver Relatórios de Produtividade")
    print("7. Logout (Voltar ao menu principal)")
    print("------------------------------------------")
    return input("Escolha uma opção: ")


def fluxo_login():
    """Controla o fluxo de login chamando o módulo 'usuarios'."""
    limpar_tela()
    print("--- LOGIN DE USUÁRIO ---")
    
    
    resultado_login = usuarios.realizar_login() 
    
    if resultado_login:
        global usuario_logado
        usuario_logado = resultado_login
        print(f"\nLogin bem-sucedido! Bem-vindo(a), {usuario_logado['nome']}!")
        aguardar(2)
        return True # Indica que o login foi um sucesso
    else:
        print("\nFalha no login. Verifique seu login e senha.")
        aguardar(2)
        return False # Indica que o login falhou

def fluxo_cadastro():
    """Controla o fluxo de cadastro chamando o módulo 'usuarios'."""
    limpar_tela()
    print("--- CADASTRO DE NOVO USUÁRIO ---")
    
    # Chama a função de cadastro do Dev 2
    sucesso = usuarios.cadastrar_usuario()
    
    if sucesso:
        print("\nCadastro realizado com sucesso!")
        print("Você já pode realizar o login.")
    else:
        print("\nOcorreu um erro durante o cadastro.")
        
    aguardar(2)

# --- (Card 6) Integração com 'tarefas.py' e 'relatorios.py' ---
def fluxo_gerenciar_tarefas():
    """Loop principal do menu de tarefas do usuário logado."""
    global usuario_logado
    if not usuario_logado:
        print("Erro: Nenhum usuário logado.")
        aguardar(2)
        return

    while True:
        opcao = exibir_menu_tarefas()
        
        if opcao == '1':
            # Chama a função de criar tarefa do Dev 3
            tarefas.cadastrar_tarefa(usuario_logado)
            aguardar(2)
            
        elif opcao == '2':
            tarefas.listar_tarefas(usuario_logado)
            aguardar(3) 
            
        elif opcao == '3':
            # Chama a função de editar tarefa do Dev 3
            tarefas.editar_tarefa(usuario_logado)
            aguardar(2)
            
        elif opcao == '4':
            # Chama a função de excluir tarefa do Dev 3
            tarefas.excluir_tarefa(usuario_logado)
            aguardar(2)
            
        elif opcao == '5':
            # Chama a função de concluir tarefa do Dev 3
            tarefas.concluir_tarefa(usuario_logado)
            aguardar(2)
            
        elif opcao == '6':
            # Chama o fluxo de relatórios
            fluxo_ver_relatorios()
            
        elif opcao == '7':
            print("Fazendo logout...")
            usuario_logado = None # Desloga o usuário
            aguardar(1)
            break # Quebra o loop, voltando ao menu principal
            
        else:
            print("Opção inválida. Tente novamente.")
            aguardar(1)

def fluxo_ver_relatorios():
    """Sub-menu para visualização de relatórios (chama Dev 4)."""
    limpar_tela()
    print("--- RELATÓRIOS DE PRODUTIVIDADE ---")
    print("1. Ver Tarefas Concluídas")
    print("2. Ver Tarefas Pendentes/Atrasadas")
    print("3. Voltar ao Menu de Tarefas")
    
    opcao_relatorio = input("Escolha uma opção: ")
    
    if opcao_relatorio == '1':
        relatorios.gerar_relatorio_concluidas(usuario_logado)
        
    elif opcao_relatorio == '2':
        relatorios.gerar_relatorio_pendentes(usuario_logado)
        
    elif opcao_relatorio == '3':
        print("Voltando...")
        
    else:
        print("Opção inválida.")
        
    aguardar(4) # Mais tempo para ler o relatório

def main():    
    try:
        while True:
            # Se o usuário não está logado, mostra o menu principal
            if not usuario_logado:
                opcao = exibir_menu_principal()
                
                if opcao == '1':
                    # fluxo_login() retorna True se o login foi bem-sucedido
                    if fluxo_login():
                        # Se o login deu certo, inicia o menu de tarefas
                        fluxo_gerenciar_tarefas()
                
                elif opcao == '2':
                    fluxo_cadastro()
                
                elif opcao == '3':
                    print("Obrigado por usar o TaskFlow. Até logo!")
                    aguardar(1)
                    sys.exit(0) # Encerra o programa
                
                else:
                    print("Opção inválida. Tente novamente.")
                    aguardar(1)
            else:
                # Se o usuário já está logado (improvável cair aqui, mas é uma garantia)
                fluxo_gerenciar_tarefas()
                
    except KeyboardInterrupt:
        print("\n\nOperação interrompida pelo usuário (Ctrl+C).")
        print("Encerrando o sistema...")
        aguardar(1)
        sys.exit(1)
    except Exception as e:
        print(f"\n--- ERRO INESPERADO (Card 7) ---")
        print(f"Ocorreu um erro global não tratado: {e}")
        print("Por favor, reinicie o aplicativo.")
        aguardar(5)
        sys.exit(1)

if name == "main":
    main()