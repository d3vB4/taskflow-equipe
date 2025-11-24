"""
Script de Inicialização do TaskFlow Hospital
Cria dados de exemplo para demonstração
"""

import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import medicos
import usuarios

def inicializar():
    """Cria dados de exemplo"""
    print("=" * 60)
    print("TaskFlow Hospital - Inicialização")
    print("=" * 60)
    
    # Cria médicos de exemplo
    print("\n1. Criando médicos de exemplo...")
    medicos_criados = medicos.criar_medicos_exemplo()
    print(f"   ✓ {len(medicos_criados)} médicos criados")
    
    # Cria usuários de exemplo (pacientes)
    print("\n2. Criando usuários de exemplo...")
    
    try:
        # Paciente 1
        usuarios.cadastrar_usuario(
            nome="João Silva",
            login="12345678900",  # CPF como login
            email="joao@email.com",
            senha="123",
            setor="recepção"
        )
        print("   ✓ Paciente: João Silva (CPF: 12345678900)")
    except:
        print("   - João Silva já existe")
    
    try:
        # Paciente 2
        usuarios.cadastrar_usuario(
            nome="Maria Santos",
            login="98765432100",
            email="maria@email.com",
            senha="123",
            setor="recepção"
        )
        print("   ✓ Paciente: Maria Santos (CPF: 98765432100)")
    except:
        print("   - Maria Santos já existe")
    
    try:
        # Usuário admin
        usuarios.cadastrar_usuario(
            nome="Admin Sistema",
            login="admin",
            email="admin@hospital.com",
            senha="admin",
            setor="recepção"
        )
        print("   ✓ Admin: admin / admin")
    except:
        print("   - Admin já existe")
    
    try:
        # Usuário Farmácia
        usuarios.cadastrar_usuario(
            nome="Farmácia Hospital",
            login="farmacia",
            email="farmacia@hospital.com",
            senha="farmacia123",
            setor="farmácia"
        )
        print("   ✓ Farmácia: farmacia / farmacia123")
    except:
        print("   - Usuário Farmácia já existe")
    
    try:
        # Usuário Enfermagem
        usuarios.cadastrar_usuario(
            nome="Enfermagem Hospital",
            login="enfermagem",
            email="enfermagem@hospital.com",
            senha="enfermagem123",
            setor="enfermagem"
        )
        print("   ✓ Enfermagem: enfermagem / enfermagem123")
    except:
        print("   - Usuário Enfermagem já existe")
    
    try:
        # Usuário Médico
        usuarios.cadastrar_usuario(
            nome="Médico Hospital",
            login="medico",
            email="medico@hospital.com",
            senha="medico123",
            setor="médico"
        )
        print("   ✓ Médico: medico / medico123")
    except:
        print("   - Usuário Médico já existe")
    
    print("\n" + "=" * 60)
    print("Inicialização concluída!")
    print("=" * 60)
    print("\nDados de teste criados:")
    print("\nMédicos disponíveis:")
    for m in medicos_criados:
        print(f"  - {m['nome']} ({m['especialidade']})")
    
    print("\nPacientes para teste no totem:")
    print("  - CPF: 12345678900 (João Silva)")
    print("  - CPF: 98765432100 (Maria Santos)")
    
    print("\nAcesso administrativo:")
    print("  - Login: admin / Senha: admin")
    
    print("\nAcessos por setor:")
    print("  - Farmácia: farmacia / farmacia123")
    print("  - Enfermagem: enfermagem / enfermagem123")
    print("  - Médicos: medico / medico123")
    
    print("\nURLs de login por setor:")
    print("  - Farmácia: http://localhost:5000/login/farmacia")
    print("  - Enfermagem: http://localhost:5000/login/enfermagem")
    print("  - Médicos: http://localhost:5000/login/medicos")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    inicializar()
