"""
Script de entrada principal para rodar o servidor na Nuvem (Render/Heroku).
"""
import os
import sys

# Garante que a pasta raiz esteja no caminho do Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from web.app import app
import inicializar # Importa o script que cria os dados

def verificar_dados_existentes():
    """
    Verifica se os arquivos .txt existem. 
    Se não existirem (comum em deploys gratuitos que reiniciam),
    recria os dados iniciais para a apresentação não falhar.
    """
    arquivos_essenciais = ['usuarios.txt', 'tarefas.txt']
    precisa_inicializar = False
    
    for arq in arquivos_essenciais:
        if not os.path.exists(arq):
            precisa_inicializar = True
            break
            
    if precisa_inicializar:
        print(">>> NUVEM: Arquivos de dados não encontrados. Recriando banco de dados...")
        inicializar.main()
    else:
        print(">>> NUVEM: Dados encontrados. Iniciando servidor.")

if __name__ == "__main__":
    # 1. Garante que temos dados antes de subir
    verificar_dados_existentes()

    # 2. Configuração de Porta para a Nuvem
    # O Render/Heroku envia a porta na variável 'PORT'. Localmente usa 5000.
    port = int(os.environ.get("PORT", 5000))
    
    # 3. Inicia o servidor
    print(f"Servidor rodando na porta {port}!")
    app.run(host='0.0.0.0', port=port)