🚀 TaskFlow - Sistema de Controle de Tarefas

Projeto Colaborativo com Python e Git - Atividade Prática de Desenvolvimento de Software.

O TaskFlow é um sistema de linha de comando (CLI) para gerenciamento de tarefas colaborativo. O projeto foi desenvolvido de forma modular, utilizando Python e aplicando os conceitos de versionamento de código com Git e GitFlow.

👥 Equipe

Este projeto foi desenvolvido de forma colaborativa:

- **Dev 1 (main.py)**: Alexandre Calmon - Responsável pelo fluxo principal e menus

- **Dev 2 (usuarios.py)**: Nilton Santana - Responsável por autenticação e usuários

- **Dev 3 (tarefas.py)**: Lucas Freire - Responsável pelo gerenciamento de tarefas

- **Dev 4 (relatorios.py / utils)**: Gustavo Garrido - Responsável por relatórios e persistência

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

```bash
git clone https://github.com/d3vB4/taskflow-equipe.git
cd taskflow-equipe
```


3. Execução

Para iniciar o programa, execute o arquivo main.py através do seu terminal:

```bash
python main.py
```


Ao executar pela primeira vez, os arquivos usuarios.json e tarefas.json serão criados automaticamente (se o módulo utils/arquivos.py estiver implementado corretamente).

🧭 Fluxo de Uso (Exemplo)

Ao iniciar, o sistema apresentará o menu principal.

Escolha a Opção 2 (Cadastrar) para criar um novo usuário.

Escolha a Opção 1 (Login) para acessar o sistema.

Após o login, você será direcionado ao Menu de Tarefas, onde poderá gerenciar suas atividades.

Qualquer alteração (novas tarefas, edições, etc.) é salva automaticamente.

🔄 Versionamento e Colaboração (GitFlow)

Este projeto utilizou o **GitFlow** como metodologia de versionamento.

### Estrutura de Branches

- **main**: Contém o código de produção (releases estáveis)
- **develop**: Branch principal de desenvolvimento; todo o código novo é integrado aqui
- **feature/[modulo]/[descricao]**: Branches usadas para desenvolver cada funcionalidade

### Exemplos de Branches Criadas

- `feature/main/menu-principal` - Menu principal e fluxo do sistema (Dev 1)
- `feature/usuarios/cadastro` - Sistema de cadastro de usuários (Dev 2)
- `feature/login-do-usuario` - Autenticação e login (Dev 2)
- `feature/tarefas` - CRUD de tarefas (Dev 3)
- `feature/relatorios` - Geração de relatórios (Dev 4)

### Processo de Integração

Todo o código foi integrado à `develop` através de **Pull Requests (PRs)**, garantindo:
- Revisão de código (Code Review) pela equipe
- Testes antes da integração
- Histórico claro de mudanças

### Padrão de Commits

Utilizamos mensagens padronizadas seguindo o formato:

```
feat(modulo): descrição da funcionalidade
bugfix(modulo): descrição da correção
merge: integração de branches
```

**Exemplos:**
- `feat(usuarios): implementação da função login`
- `bugfix(tarefas): correção no fluxo de edição`
- `feat(relatorios.py): gerar relatórios das tarefas`