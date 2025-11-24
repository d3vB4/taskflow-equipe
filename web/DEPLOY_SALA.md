# 🚀 TaskFlow Hospital Web - Guia de Deploy para Sala de Aula

## 📋 Pré-requisitos

- Python 3.6 ou superior instalado
- Acesso à internet (para baixar dependências)
- Todos os arquivos do projeto TaskFlow

## 🔧 Instalação e Configuração

### Passo 1: Verificar Python

Abra o terminal/PowerShell e verifique se o Python está instalado:

```bash
python --version
# ou
python3 --version
```

Se não estiver instalado, baixe em: https://www.python.org/downloads/

### Passo 2: Navegar até o diretório do projeto

```bash
cd caminho\para\taskflow-equipe\web
```

### Passo 3: Instalar dependências

```bash
pip install -r requirements.txt
```

**Nota:** Se houver erro, tente:
```bash
python -m pip install -r requirements.txt
```

### Passo 4: Executar a aplicação

```bash
python app.py
```

Você verá uma mensagem como:

```
==================================================
TaskFlow Hospital - Sistema Web
==================================================
Acesse: http://localhost:5000
Totem: http://localhost:5000/totem
==================================================
 * Running on http://0.0.0.0:5000
```

## 🌐 Opções de Deploy para Sala de Aula

### Opção 1: Localhost (Mais Simples)

**Quando usar:** Demonstração individual no seu computador

1. Execute `python app.py`
2. Abra o navegador em `http://localhost:5000`
3. Pronto!

**Vantagens:**
- ✅ Mais rápido
- ✅ Não precisa de internet
- ✅ Sem configuração adicional

**Desvantagens:**
- ❌ Apenas você pode acessar

---

### Opção 2: Rede Local (Recomendado para Sala)

**Quando usar:** Demonstração com múltiplos dispositivos na mesma rede

#### Passo 1: Descobrir seu IP local

**Windows:**
```bash
ipconfig
```
Procure por "Endereço IPv4" (ex: `192.168.1.100`)

**Mac/Linux:**
```bash
ifconfig
# ou
ip addr show
```

#### Passo 2: Executar a aplicação

```bash
python app.py
```

A aplicação já está configurada para aceitar conexões externas (`host='0.0.0.0'`)

#### Passo 3: Compartilhar o link

Compartilhe com os colegas:
```
http://SEU_IP:5000
```

Exemplo: `http://192.168.1.100:5000`

**Totem:**
```
http://SEU_IP:5000/totem
```

**Vantagens:**
- ✅ Múltiplos usuários simultâneos
- ✅ Demonstração realista
- ✅ Testa colaboração

**Desvantagens:**
- ⚠️ Todos precisam estar na mesma rede Wi-Fi
- ⚠️ Firewall pode bloquear (ver troubleshooting)

---

### Opção 3: ngrok (Internet Pública)

**Quando usar:** Demonstração remota ou rede local com problemas

#### Passo 1: Baixar ngrok

1. Acesse: https://ngrok.com/download
2. Baixe e extraia o executável
3. (Opcional) Crie conta gratuita para URL personalizada

#### Passo 2: Executar a aplicação Flask

```bash
python app.py
```

#### Passo 3: Em outro terminal, executar ngrok

```bash
ngrok http 5000
```

Você verá algo como:

```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

#### Passo 4: Compartilhar o link

Compartilhe a URL do ngrok (ex: `https://abc123.ngrok.io`)

**Vantagens:**
- ✅ Acesso de qualquer lugar
- ✅ HTTPS automático
- ✅ Funciona com qualquer rede

**Desvantagens:**
- ⚠️ Precisa de internet
- ⚠️ URL muda a cada execução (versão gratuita)

---

## 👥 Teste com Múltiplos Usuários

### Cenário de Demonstração

**Preparação:**

1. Crie 4 usuários (um para cada setor):

```
Recepção:
- Login: recepcao
- Senha: 123
- Setor: recepção

Médico:
- Login: medico
- Senha: 123
- Setor: médico

Farmácia:
- Login: farmacia
- Senha: 123
- Setor: farmácia

Enfermagem:
- Login: enfermagem
- Senha: 123
- Setor: enfermagem
```

**Fluxo de Demonstração:**

1. **Recepção** cria novo paciente
2. **Totem** mostra paciente na fila (projetar em TV/monitor)
3. **Médico** atualiza status para "Em consulta"
4. **Farmácia** recebe e prepara medicação
5. **Enfermagem** administra e conclui atendimento
6. **Totem** atualiza em tempo real

---

## 🖥️ Configuração do Totem

### Para TV/Monitor na Sala de Espera

1. Abra navegador em modo fullscreen (F11)
2. Acesse: `http://SEU_IP:5000/totem`
3. A página atualiza automaticamente a cada 10 segundos

**Dica:** Use um tablet ou computador dedicado para o totem

---

## 🐛 Troubleshooting

### Erro: "Address already in use"

**Problema:** Porta 5000 já está em uso

**Solução:** Edite `app.py` e mude a porta:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mudou para 5001
```

### Erro: "Connection refused" ao acessar de outro dispositivo

**Problema:** Firewall bloqueando conexões

**Solução Windows:**

1. Abra "Firewall do Windows Defender"
2. Clique em "Permitir um aplicativo"
3. Adicione Python à lista de exceções

**Solução alternativa:** Use ngrok (Opção 3)

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Problema:** Flask não foi instalado

**Solução:**

```bash
pip install Flask
```

### Página não carrega CSS/JS

**Problema:** Arquivos estáticos não encontrados

**Solução:** Verifique se a estrutura de diretórios está correta:

```
web/
├── app.py
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    └── (todos os .html)
```

---

## 📱 Teste em Dispositivos Móveis

A aplicação é responsiva! Teste em:

- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

---

## ⚡ Dicas para Apresentação

1. **Prepare dados de teste** antes da apresentação
2. **Teste a conexão** 5 minutos antes
3. **Tenha um backup** (screenshots/vídeo)
4. **Use o totem** em tela grande para impacto visual
5. **Demonstre colaboração** com múltiplos usuários

---

## 🔒 Segurança

**IMPORTANTE:** Esta é uma aplicação de demonstração!

Para produção, você precisaria:
- Mudar `secret_key` para algo seguro
- Usar HTTPS
- Implementar autenticação mais robusta
- Adicionar validação de entrada
- Usar banco de dados real

---

## 📞 Suporte Rápido

**Problema comum:** "Não consigo acessar de outro computador"

**Checklist:**
1. ✅ Ambos estão na mesma rede Wi-Fi?
2. ✅ Usou o IP correto (não localhost)?
3. ✅ Firewall está permitindo?
4. ✅ Aplicação está rodando?

**Se nada funcionar:** Use ngrok (Opção 3)

---

## 🎯 Checklist de Demonstração

Antes de apresentar:

- [ ] Python instalado e funcionando
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Aplicação inicia sem erros
- [ ] Consegue acessar `http://localhost:5000`
- [ ] Usuários de teste criados
- [ ] Testou em outro dispositivo (se aplicável)
- [ ] Totem funcionando em tela grande
- [ ] Preparou dados de demonstração

**Boa apresentação! 🎉**
