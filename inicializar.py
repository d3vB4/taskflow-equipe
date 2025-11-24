"""
Script de Inicialização do TaskFlow Hospital (Modo Web)
Cria dados de exemplo para demonstração e testes de deploy.
Gera arquivos de persistência (.txt) compatíveis com a versão Web.
"""

import sys
import os
from uuid import uuid4

# Adiciona o diretório atual ao path para garantir importações
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa módulos do sistema
try:
    import usuarios
    import tarefas
    # Importa módulos da pasta web
    from web import atendimentos, workflow
except ImportError as e:
    print("ERRO DE IMPORTAÇÃO!")
    print("Certifique-se de que a estrutura de pastas está correta:")
    print("  / (raiz)")
    print("  |-- usuarios.py")
    print("  |-- tarefas.py")
    print("  |-- web/")
    print("      |-- atendimentos.py")
    print("      |-- workflow.py")
    print(f"Detalhe do erro: {e}")
    sys.exit(1)

def limpar_arquivos():
    """Reseta os arquivos de banco de dados para começar limpo."""
    arquivos = ['usuarios.txt', 'tarefas.txt', 'atendimentos.txt', 'pacientes.txt']
    for arq in arquivos:
        if os.path.exists(arq):
            try:
                os.remove(arq)
            except:
                # Se não der para apagar, tenta zerar o conteúdo
                with open(arq, 'w') as f: pass

def criar_usuarios_base():
    """Cria a equipe hospitalar."""
    print("1. Criando equipe hospitalar...")
    
    lista_usuarios = [
        # Admin / Recepção
        {"nome": "Alexandre (Recepção)", "login": "alex", "pass": "123", "setor": "recepção", "email": "alex@hospital.com"},
        {"nome": "Administrador", "login": "admin", "pass": "admin", "setor": "admin", "email": "admin@hospital.com"},
        
        # Médicos
        {"nome": "Dr. House", "login": "house", "pass": "123", "setor": "médico", "crm": "12345", "esp": "Infectologista"},
        {"nome": "Dra. Grey", "login": "grey", "pass": "123", "setor": "médico", "crm": "54321", "esp": "Cirurgia Geral"},
        {"nome": "Dr. Estranho", "login": "strange", "pass": "123", "setor": "médico", "crm": "99999", "esp": "Neurocirurgia"},
        
        # Equipe Técnica
        {"nome": "Enf. Joy", "login": "joy", "pass": "123", "setor": "enfermagem", "email": "joy@hospital.com"},
        {"nome": "Farm. Walter", "login": "walter", "pass": "123", "setor": "farmácia", "email": "walter@hospital.com"},
    ]

    for u in lista_usuarios:
        try:
            usuarios.cadastrar_usuario(
                nome=u["nome"], 
                login=u["login"], 
                senha=u["pass"], 
                email=u.get("email", f"{u['login']}@hospital.com"),
                setor=u["setor"],
                crm=u.get("crm"),
                especialidade=u.get("esp")
            )
        except ValueError:
            pass # Ignora se já existir
            
    print(f"   ✓ {len(lista_usuarios)} usuários criados.")

def avancar_tarefa(atendimento_token, setor_atual, acao_simulada, usuario_responsavel):
    """
    Função auxiliar para simular o clique nos botões do dashboard.
    Avança o workflow de um paciente.
    """
    todas_tarefas = tarefas._carregar_tarefas()
    tarefa_atual = None
    
    # Encontra a tarefa pendente do setor atual para este atendimento
    for t in todas_tarefas:
        if (t.get('atendimento_token') == atendimento_token and 
            t.get('setor', '').lower() == setor_atual.lower() and 
            t.get('status') == tarefas.STATUS_PENDENTE):
            tarefa_atual = t
            break
            
    if not tarefa_atual:
        return False
        
    # Conclui a tarefa atual
    tarefa_atual['status'] = tarefas.STATUS_CONCLUIDA
    tarefa_atual['data_conclusao'] = tarefas._data_atual()
    tarefa_atual['concluida_por'] = usuario_responsavel['id']
    
    # Simula a lógica de negócio do app.py (encaminhamento)
    nome_paciente = tarefa_atual['titulo'].split(' - ')[-1]
    
    if acao_simulada == 'ir_para_farmacia':
        workflow.adicionar_tarefa_farmacia(atendimento_token, nome_paciente)
        
    elif acao_simulada == 'ir_para_enfermagem':
        workflow.adicionar_tarefa_enfermagem(atendimento_token, nome_paciente)
        
    elif acao_simulada == 'alta':
        # Apenas conclui, não cria nova
        pass
        
    tarefas._salvar_tarefas(todas_tarefas)
    return True

def criar_cenarios():
    """Cria pacientes em diferentes estágios do atendimento."""
    print("2. Gerando fluxo de pacientes...")
    
    # Carrega usuários necessários para atribuir responsabilidades
    dr_house = usuarios.buscar_usuario_por_login("house")
    dr_grey = usuarios.buscar_usuario_por_login("grey")
    farmaceutico = usuarios.buscar_usuario_por_login("walter")
    
    if not (dr_house and dr_grey and farmaceutico):
        print("   [ERRO] Falha ao carregar usuários base.")
        return

    # --- CENÁRIO A: Paciente Novo (Aguardando Médico) ---
    print("   Criando: João Silva -> Fila do Dr. House")
    atend_a = atendimentos.criar_atendimento(
        cpf="111.111.111-11",
        nome_paciente="João Silva",
        medico_id=dr_house['id'],
        especialidade=dr_house['especialidade']
    )
    workflow.criar_workflow_automatico(
        atend_a['token'], "João Silva", dr_house['id'], dr_house['nome']
    )
    # Nenhuma ação extra necessária, o workflow padrão já deixa pendente pro médico
    

    # --- CENÁRIO B: Paciente na Farmácia (Já passou pelo médico) ---
    print("   Criando: Maria Santos -> Fila da Farmácia")
    atend_b = atendimentos.criar_atendimento(
        cpf="222.222.222-22",
        nome_paciente="Maria Santos",
        medico_id=dr_grey['id'],
        especialidade=dr_grey['especialidade']
    )
    workflow.criar_workflow_automatico(
        atend_b['token'], "Maria Santos", dr_grey['id'], dr_grey['nome']
    )
    
    # Simula o médico atendendo e mandando para farmácia
    avancar_tarefa(atend_b['token'], 'médico', 'ir_para_farmacia', dr_grey)
    

    # --- CENÁRIO C: Paciente na Enfermagem (Já pegou remédio) ---
    print("   Criando: Pedro Souza -> Fila da Enfermagem")
    atend_c = atendimentos.criar_atendimento(
        cpf="333.333.333-33",
        nome_paciente="Pedro Souza",
        medico_id=dr_house['id'],
        especialidade=dr_house['especialidade']
    )
    workflow.criar_workflow_automatico(
        atend_c['token'], "Pedro Souza", dr_house['id'], dr_house['nome']
    )
    
    # Médico atende -> Farmácia
    avancar_tarefa(atend_c['token'], 'médico', 'ir_para_farmacia', dr_house)
    # Farmácia atende -> Enfermagem
    avancar_tarefa(atend_c['token'], 'farmácia', 'ir_para_enfermagem', farmaceutico)

def main():
    print("="*60)
    print("   INICIALIZADOR TASKFLOW HOSPITAL (WEB)")
    print("="*60)
    
    limpar_arquivos()
    criar_usuarios_base()
    criar_cenarios()
    
    print("\n" + "="*60)
    print("SUCESSO! DADOS GERADOS.")
    print("="*60)
    print("\nLOGIN PARA TESTE:")
    print("-------------------")
    print("RECEPCIONISTA : alex   / 123")
    print("MÉDICO        : house  / 123")
    print("FARMÁCIA      : walter / 123")
    print("ENFERMAGEM    : joy    / 123")
    print("\nAgora execute: python web/app.py")

if __name__ == "__main__":
    main()