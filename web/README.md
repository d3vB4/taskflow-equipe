# 📚 TaskFlow Hospital Web - README

## 🏥 Sobre o Projeto

TaskFlow Hospital é um sistema web de rastreamento de pacientes em tempo real, permitindo acompanhar a jornada do paciente desde a recepção até a alta.

### Conceito: "Uberização" da Espera Hospitalar

Assim como você acompanha uma entrega de comida ou um Uber, os pacientes podem acompanhar em tempo real o status do seu atendimento hospitalar.

## ✨ Funcionalidades

### 🔓 Área Pública

- **Página Totem**: Visualização em tempo real para sala de espera
  - Timeline visual da jornada do paciente
  - Auto-refresh a cada 10 segundos
  - Busca por senha do paciente
  - Design otimizado para TV/monitor

### 🔐 Área Restrita (Requer Login)

- **Dashboard**: Estatísticas e visão geral
- **Gestão de Pacientes**: CRUD completo
- **Atualização de Status**: Acompanhamento em tempo real
- **Relatórios**: Análise de produtividade

## 🎯 Jornada do Paciente

```
Recepção → Médico → Farmácia → Enfermagem
```

1. **Recepção**: Check-in e cadastro
2. **Médico**: Consulta e prescrição
3. **Farmácia**: Separação de medicamentos
4. **Enfermagem**: Administração e alta

## 🚀 Como Executar

### Instalação Rápida

```bash
cd web
pip install -r requirements.txt
python app.py
```

Acesse: `http://localhost:5000`

### Documentação Completa

Veja [DEPLOY_SALA.md](DEPLOY_SALA.md) para:
- Guia de instalação detalhado
- 3 opções de deploy (localhost, rede local, ngrok)
- Troubleshooting
- Dicas para apresentação

## 📁 Estrutura do Projeto

```
web/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── static/
│   ├── css/
│   │   └── style.css     # Estilos customizados
│   └── js/
│       └── main.js       # JavaScript
└── templates/
    ├── base.html         # Template base
    ├── index.html        # Página inicial
    ├── totem.html        # Totem público
    ├── login.html        # Login
    ├── dashboard.html    # Dashboard
    ├── pacientes.html    # Lista de pacientes
    └── novo_paciente.html # Formulário
```

## 🔗 Rotas Principais

| Rota | Descrição | Acesso |
|------|-----------|--------|
| `/` | Página inicial | Público |
| `/totem` | Totem de visualização | Público |
| `/login` | Autenticação | Público |
| `/dashboard` | Dashboard | Restrito |
| `/pacientes` | Lista de pacientes | Restrito |
| `/pacientes/novo` | Novo paciente | Restrito |

## 👥 Usuários de Teste

Para demonstração, crie usuários para cada setor:

```
Recepção: recepcao / 123
Médico: medico / 123
Farmácia: farmacia / 123
Enfermagem: enfermagem / 123
```

## 🎨 Tecnologias

- **Backend**: Flask 3.0
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Persistência**: TXT (reutiliza módulos CLI)
- **Ícones**: Bootstrap Icons

## 🔄 Integração com Módulos CLI

A aplicação web **reutiliza** os módulos existentes do projeto CLI:

- `usuarios.py` - Autenticação
- `tarefas.py` - Gestão de pacientes
- `relatorios.py` - Estatísticas
- `utils/arquivos.py` - Persistência

**Nenhum código foi modificado!** A aplicação web é uma camada adicional.

## 📊 Benefícios

### Para Pacientes
- ✅ Transparência no atendimento
- ✅ Redução de ansiedade
- ✅ Informação em tempo real

### Para Hospital
- ✅ Identificação de gargalos
- ✅ Otimização de processos
- ✅ Melhoria na experiência do paciente

## 🐛 Problemas Comuns

### Porta em uso
```bash
# Mude a porta em app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Flask não instalado
```bash
pip install Flask
```

### Não acessa de outro dispositivo
- Verifique firewall
- Use ngrok como alternativa

Veja [DEPLOY_SALA.md](DEPLOY_SALA.md) para mais soluções.

## 📝 Licença

Projeto educacional - TaskFlow Hospital

## 👨‍💻 Equipe

- Dev 1: Alexandre Calmon (main.py)
- Dev 2: Nilton Santana (usuarios.py)
- Dev 3: Lucas Freire (tarefas.py)
- Dev 4: Gustavo Garrido (relatorios.py, web)

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como parte da atividade prática de Projeto Colaborativo com Python e Git.

**Repositório:** https://github.com/d3vB4/taskflow-equipe

---

**Desenvolvido com ❤️ para melhorar a experiência hospitalar**
