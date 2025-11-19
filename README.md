🚀 TaskFlow - Sistema de Controle de Tarefas

Projeto da disciplina de [Nome da Disciplina] do curso de [Nome do Curso] - [Nome da Faculdade/Universidade].

O TaskFlow é um sistema de linha de comando (CLI) para gerenciamento de tarefas colaborativo. O projeto foi desenvolvido de forma modular, utilizando Python e aplicando os conceitos de versionamento de código com Git e GitFlow.

👥 Equipe (Equipe X)

Este projeto foi desenvolvido de forma colaborativa:

Dev 1 (main.py): [Alexandre Calmon] - [@seu-github]

Dev 2 (usuarios.py): [Nilton Santana] - [@github-dev2]

Dev 3 (tarefas.py): [Lucas Freire] - [@github-dev3]

Dev 4 (relatorios.py / utils): [Gustavo Garrido] - [@github-dev4]

⚙️ Funcionalidades Principais

Autenticação: Cadastro e Login de usuários com persistência em JSON.

Gerenciamento de Tarefas: Sistema CRUD completo (Criar, Listar, Editar, Excluir) para tarefas.

Controle de Status: Marque tarefas como "Concluídas".

Relatórios: Gere relatórios de produtividade, visualizando tarefas pendentes, atrasadas e concluídas.

Persistência: Todos os dados de usuários e tarefas são salvos em arquivos .json locais.

🛠️ Arquitetura Modular

O projeto foi dividido em módulos para organizar responsabilidades, facilitando a manutenção e o desenvolvimento paralelo.

TaskFlow/
│
├── main.py        # Ponto de entrada, menus e fluxo principal (Dev 1)
├── usuarios.py    # Funções de cadastro e login (Dev 2)
├── tarefas.py     # Funções CRUD de tarefas (Dev 3)
├── relatorios.py  # Funções de geração de relatórios (Dev 4)
│
├── utils/
│   └── arquivos.py # Funções de leitura/escrita de JSON (Dev 4)
│
├── usuarios.json    # Banco de dados de usuários
├── tarefas.json     # Banco de dados de tarefas
└── README.md


🏃‍♂️ Como Executar

Este projeto usa apenas bibliotecas nativas do Python 3. Não é necessário instalar pacotes externos.

1. Pré-requisitos

Python (versão 3.6 ou superior)

Git

2. Instalação

Clone o repositório para sua máquina local:

git clone [https://github.com/](https://github.com/)[seu-usuario]/taskflow-equipeX.git
cd taskflow-equipeX


3. Execução

Para iniciar o programa, execute o arquivo main.py através do seu terminal:

python main.py


Ao executar pela primeira vez, os arquivos usuarios.json e tarefas.json serão criados automaticamente (se o módulo utils/arquivos.py estiver implementado corretamente).

🧭 Fluxo de Uso (Exemplo)

Ao iniciar, o sistema apresentará o menu principal.

Escolha a Opção 2 (Cadastrar) para criar um novo usuário.

Escolha a Opção 1 (Login) para acessar o sistema.

Após o login, você será direcionado ao Menu de Tarefas, onde poderá gerenciar suas atividades.

Qualquer alteração (novas tarefas, edições, etc.) é salva automaticamente.

🔄 Versionamento e Colaboração (GitFlow)

Este projeto utilizou o GitFlow como metodologia de versionamento.

main: Contém o código de produção (releases estáveis).

develop: Branch principal de desenvolvimento; todo o código novo é integrado aqui.

feature/modulo/descricao: Branches usadas para desenvolver cada funcionalidade (ex: feature/usuarios/cadastro).

Todo o código foi integrado à develop através de Pull Requests (PRs), garantindo a revisão de código (Code Review) pela equipe.