"""
TaskFlow Hospital - Aplicação Web Flask
Sistema de rastreamento de pacientes em tempo real
"""

import sys
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import usuarios
import tarefas
import relatorios

# Novos módulos para autoatendimento
import web.atendimentos as atendimentos
import web.qrcode_generator as qrcode_generator
import web.workflow as workflow

app = Flask(__name__)
app.secret_key = 'taskflow-hospital-secret-key-2025'  # Mudar em produção

# Configurações
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora


# ==================== ROTAS PÚBLICAS ====================

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@app.route('/totem')
def totem():
    """Redireciona para o check-in"""
    return redirect(url_for('totem_checkin'))


@app.route('/totem/buscar', methods=['POST'])
def totem_buscar():
    """Busca paciente por ID/senha no totem"""
    senha = request.form.get('senha', '').strip()
    
    if not senha:
        return jsonify({'erro': 'Digite uma senha válida'}), 400
    
    todas_tarefas = tarefas._carregar_tarefas()
    
    # Busca por ID parcial
    paciente_encontrado = None
    for t in todas_tarefas:
        if t.get('id', '').startswith(senha) or senha in t.get('id', ''):
            paciente_encontrado = t
            break
    
    if not paciente_encontrado:
        return jsonify({'erro': 'Paciente não encontrado'}), 404
    
    # Adiciona informação do responsável
    usuario = usuarios.obter_usuario(paciente_encontrado.get('responsavel', ''))
    if usuario:
        paciente_encontrado['setor_responsavel'] = usuario.get('setor', 'Desconhecido')
    
    return jsonify(paciente_encontrado)


# ==================== TOTEM DE CHECK-IN (AUTOATENDIMENTO) ====================

@app.route('/totem/checkin')
def totem_checkin():
    """Totem de check-in - Etapa 1: Identificação"""
    return render_template('totem_checkin.html', etapa='cpf')


@app.route('/totem/checkin/verificar', methods=['POST'])
def totem_checkin_verificar():
    """Totem de check-in - Etapa 2: Verificar/Cadastrar e Redirecionar"""
    cpf = request.form.get('cpf', '').replace('.', '').replace('-', '')
    nome = request.form.get('nome')
    
    # Busca usuário por CPF
    usuario_encontrado = usuarios.buscar_usuario_por_login(cpf)
    
    if not usuario_encontrado:
        # Se não existe, cadastra automaticamente agora mesmo
        if nome:
            usuarios.cadastrar_usuario(
                nome=nome,
                login=cpf,
                senha=cpf,  # Senha inicial é o próprio CPF
                email=f"{cpf}@paciente.taskflow",
                setor="paciente"
            )
        else:
            flash('Nome é obrigatório para novos pacientes', 'danger')
            return redirect(url_for('totem_checkin'))
    
    return redirect(url_for('totem_checkin_medico', cpf=cpf))


@app.route('/totem/checkin/medico/<cpf>')
def totem_checkin_medico(cpf):
    """Totem de check-in - Etapa 3: Seleção de médico"""
    especialidade = request.args.get('especialidade')
    
    # Busca usuário
    todos_usuarios = usuarios.listar_usuarios()
    usuario_encontrado = None
    for u in todos_usuarios:
        if cpf in u.get('login', '') or cpf in u.get('email', ''):
            usuario_encontrado = u
            break
    
    if not usuario_encontrado:
        return redirect(url_for('totem_checkin'))
    
    # Lista médicos
    medicos_disponiveis = []
    if especialidade:
        medicos_disponiveis = [
            u for u in usuarios.listar_usuarios()
            if u.get('setor') == 'médico'
            and u.get('disponivel') == 'true'
            and u.get('especialidade') == especialidade
        ]
    
    return render_template('totem_checkin.html', 
                         etapa='medico',
                         cpf=cpf,
                         paciente_nome=usuario_encontrado.get('nome', ''),
                         especialidades=usuarios.listar_especialidades(),
                         medicos=medicos_disponiveis)


@app.route('/totem/checkin/confirmar', methods=['POST'])
def totem_checkin_confirmar():
    """Totem de check-in - Etapa 4: Confirmar e gerar QR Code"""
    cpf = request.form.get('cpf')
    medico_id = request.form.get('medico_id')
    especialidade = request.form.get('especialidade')
    
    todos_usuarios = usuarios.listar_usuarios()
    usuario_encontrado = None
    for u in todos_usuarios:
        if cpf in u.get('login', '') or cpf in u.get('email', ''):
            usuario_encontrado = u
            break
    
    if not usuario_encontrado:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('totem_checkin'))
    
    medico = usuarios.obter_usuario(medico_id)
    if not medico:
        flash('Médico não encontrado', 'danger')
        return redirect(url_for('totem_checkin'))
    
    atendimento = atendimentos.criar_atendimento(
        cpf=cpf,
        nome_paciente=usuario_encontrado.get('nome'),
        medico_id=medico_id,
        especialidade=especialidade
    )
    
    workflow.criar_workflow_automatico(
        atendimento_token=atendimento['token'],
        nome_paciente=usuario_encontrado.get('nome'),
        medico_id=medico_id,
        medico_nome=medico.get('nome')
    )
    
    qrcode_img = qrcode_generator.gerar_qr_code_atendimento(
        token=atendimento['token'],
        host=request.host
    )
    
    tempo_estimado = atendimentos.calcular_tempo_estimado(int(atendimento['posicao_fila']))
    
    return render_template('totem_checkin.html',
                         etapa='qrcode',
                         senha=atendimento['senha'],
                         qrcode=qrcode_img,
                         medico_nome=medico.get('nome'),
                         especialidade=especialidade,
                         tempo_estimado=tempo_estimado)


# ==================== APP DO PACIENTE (CORREÇÃO AQUI) ====================

@app.route('/paciente/<token>')
def paciente_app(token):
    """App do paciente - Acompanhamento em tempo real"""
    atendimento = atendimentos.obter_atendimento(token)
    
    if not atendimento:
        return render_template('erro.html', mensagem='Atendimento não encontrado'), 404
    
    tarefas_atendimento = workflow.obter_tarefas_atendimento(token)
    medico = usuarios.obter_usuario(atendimento.get('medico_id'))
    medico_nome = medico.get('nome', 'Não informado') if medico else 'Não informado'
    
    progresso = workflow.calcular_progresso(token)
    
    # --- CORREÇÃO DO CÁLCULO DA ETAPA ---
    etapa_atual = workflow.obter_etapa_atual(token)
    
    # Mapa robusto que aceita com e sem acento
    mapa_etapas = {
        'recepção': 0, 'recepcao': 0,
        'médico': 1, 'medico': 1,
        'farmácia': 2, 'farmacia': 2,
        'enfermagem': 3,
        'concluido': 4, 'concluído': 4
    }
    
    etapa_index = mapa_etapas.get(etapa_atual.lower(), 0)
    # ------------------------------------
    
    tempo_estimado = atendimentos.calcular_tempo_estimado(int(atendimento.get('posicao_fila', 1)))
    
    return render_template('paciente_app.html',
                         atendimento=atendimento,
                         tarefas=tarefas_atendimento,
                         medico_nome=medico_nome,
                         progresso=progresso,
                         etapa_index=etapa_index,
                         tempo_estimado=tempo_estimado)


# ==================== ÁREA RESTRITA ====================

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login primeiro', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def setor_required(setor_permitido):
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Você precisa fazer login primeiro', 'warning')
                return redirect(url_for('login'))
            if session.get('usuario_setor', '').lower() != setor_permitido.lower():
                flash(f'Acesso negado. Esta área é exclusiva para {setor_permitido}.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== AUTENTICAÇÃO E DASHBOARD ====================

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_publico():
    if request.method == 'POST':
        nome = request.form.get('nome')
        login_user = request.form.get('login')
        email = request.form.get('email')
        senha = request.form.get('senha')
        setor = request.form.get('setor')
        especialidade = request.form.get('especialidade') if setor == 'médico' else ''
        
        if not (nome and login_user and senha and setor):
            flash('Preencha todos os campos obrigatórios', 'danger')
            return redirect(url_for('cadastro_publico'))
        
        try:
            usuarios.cadastrar_usuario(
                nome=nome, login=login_user, senha=senha, email=email,
                setor=setor, especialidade=especialidade
            )
            flash(f'Usuário {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            return redirect(url_for('cadastro_publico'))
    return render_template('cadastro_publico.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = request.form.get('login')
        senha = request.form.get('senha')
        usuario = usuarios.realizar_login(login=login_user, senha=senha)
        
        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['usuario_setor'] = usuario.get('setor', '')
            
            setor = usuario.get('setor', '').lower()
            if setor == 'farmácia': return redirect(url_for('dashboard_farmacia'))
            elif setor == 'enfermagem': return redirect(url_for('dashboard_enfermagem'))
            elif setor == 'médico': return redirect(url_for('dashboard_medicos'))
            else: return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha inválidos', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    todas_tarefas = tarefas._carregar_tarefas()
    usuario_setor = session.get('usuario_setor', '').lower()
    
    if usuario_setor in ['farmácia', 'farmacia']:
        tarefas_filtradas = [t for t in todas_tarefas if t.get('setor', '').lower() in ['farmácia', 'farmacia']]
    elif usuario_setor == 'enfermagem':
        tarefas_filtradas = [t for t in todas_tarefas if t.get('setor', '').lower() == 'enfermagem']
    elif usuario_setor == 'médico':
        usuario_id = session.get('usuario_id')
        tarefas_filtradas = [t for t in todas_tarefas if t.get('responsavel') == usuario_id or t.get('setor', '').lower() in ['médico', 'medico']]
    else:
        tarefas_filtradas = todas_tarefas
    
    total = len(tarefas_filtradas)
    concluidas = len([t for t in tarefas_filtradas if t.get('status') == tarefas.STATUS_CONCLUIDA])
    pendentes = total - concluidas
    tarefas_recentes = sorted(tarefas_filtradas, key=lambda x: x.get('data_criacao', ''), reverse=True)[:10]
    
    return render_template('dashboard.html', total=total, concluidas=concluidas, pendentes=pendentes, tarefas=tarefas_recentes)


@app.route('/dashboard/farmacia')
@setor_required('farmácia')
def dashboard_farmacia():
    return dashboard()

@app.route('/dashboard/enfermagem')
@setor_required('enfermagem')
def dashboard_enfermagem():
    return dashboard()

@app.route('/dashboard/medicos')
@setor_required('médico')
def dashboard_medicos():
    return dashboard()


@app.route('/pacientes')
@login_required
def pacientes():
    todas_tarefas = tarefas._carregar_tarefas()
    usuario_setor = session.get('usuario_setor', '').lower()
    usuario_id = session.get('usuario_id')
    
    if usuario_setor in ['farmácia', 'farmacia']:
        tarefas_filtradas = [t for t in todas_tarefas if t.get('setor', '').lower() in ['farmácia', 'farmacia']]
    elif usuario_setor == 'enfermagem':
        tarefas_filtradas = [t for t in todas_tarefas if t.get('setor', '').lower() == 'enfermagem']
    elif usuario_setor == 'médico':
        tarefas_filtradas = [t for t in todas_tarefas if t.get('responsavel') == usuario_id or (t.get('setor', '').lower() in ['médico', 'medico'])]
    else:
        tarefas_filtradas = todas_tarefas
    
    for tarefa in tarefas_filtradas:
        responsavel_id = tarefa.get('responsavel', '')
        if responsavel_id == 'sistema':
            tarefa['responsavel_nome'] = 'Sistema'
            tarefa['responsavel_setor'] = tarefa.get('setor', 'N/A')
        else:
            usuario = usuarios.obter_usuario(responsavel_id)
            if usuario:
                tarefa['responsavel_nome'] = usuario.get('nome', 'Desconhecido')
                tarefa['responsavel_setor'] = usuario.get('setor', 'N/A')
            else:
                tarefa['responsavel_nome'] = 'Desconhecido'
                tarefa['responsavel_setor'] = 'N/A'
    
    tarefas_filtradas = sorted(tarefas_filtradas, key=lambda x: x.get('data_criacao', ''), reverse=True)
    return render_template('pacientes.html', pacientes=tarefas_filtradas)


@app.route('/pacientes/novo', methods=['GET', 'POST'])
@login_required
def novo_paciente():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        prazo = request.form.get('prazo')
        
        if not titulo or not prazo:
            flash('Título e prazo são obrigatórios', 'danger')
            return redirect(url_for('novo_paciente'))
        
        usuario_logado = {'id': session['usuario_id'], 'nome': session['usuario_nome'], 'setor': session.get('usuario_setor', '')}
        
        from uuid import uuid4
        nova_tarefa = {
            "id": str(uuid4()),
            "titulo": titulo,
            "descricao": descricao or "",
            "responsavel": usuario_logado['id'],
            "prazo": prazo,
            "status": tarefas.STATUS_PENDENTE,
            "data_criacao": tarefas._data_atual(),
            "data_conclusao": None
        }
        
        todas_tarefas = tarefas._carregar_tarefas()
        todas_tarefas.append(nova_tarefa)
        tarefas._salvar_tarefas(todas_tarefas)
        flash(f'Paciente "{titulo}" cadastrado com sucesso!', 'success')
        return redirect(url_for('pacientes'))
    return render_template('novo_paciente.html')


@app.route('/pacientes/<id>/atualizar', methods=['POST'])
@login_required
def atualizar_paciente(id):
    novo_status = request.form.get('status')
    todas_tarefas = tarefas._carregar_tarefas()
    tarefa = next((t for t in todas_tarefas if t['id'] == id), None)
    
    if tarefa:
        tarefa['status'] = novo_status
        if novo_status == tarefas.STATUS_CONCLUIDA:
            tarefa['data_conclusao'] = tarefas._data_atual()
        tarefas._salvar_tarefas(todas_tarefas)
        flash('Status atualizado com sucesso!', 'success')
    else:
        flash('Paciente não encontrado', 'danger')
    return redirect(url_for('pacientes'))


@app.route('/tarefas/<id>/acao', methods=['POST'])
@login_required
def realizar_acao_tarefa(id):
    acao = request.form.get('acao')
    todas_tarefas = tarefas._carregar_tarefas()
    tarefa_atual = next((t for t in todas_tarefas if t['id'] == id), None)
    
    if not tarefa_atual:
        flash('Tarefa não encontrada', 'danger')
        return redirect(url_for('dashboard'))
    
    tarefa_atual['status'] = tarefas.STATUS_CONCLUIDA
    tarefa_atual['data_conclusao'] = tarefas._data_atual()
    tarefas._salvar_tarefas(todas_tarefas)
    
    atendimento_token = tarefa_atual.get('atendimento_token')
    nome_paciente = tarefa_atual['titulo'].split(' - ')[-1] if ' - ' in tarefa_atual['titulo'] else "Paciente"
    
    if acao == 'encaminhar_medico':
        desc = tarefa_atual.get('descricao', '')
        especialidade = "Clínico Geral"
        if "Especialidade desejada: " in desc:
            try: especialidade = desc.split("Especialidade desejada: ")[1].split(".")[0]
            except: pass
        workflow.adicionar_tarefa_medico(atendimento_token, nome_paciente, especialidade)
        atendimentos.atualizar_status_atendimento(atendimento_token, 'em_atendimento', 'medico')
        flash('Encaminhado para o médico.', 'success')
        
    elif acao == 'alta':
        atendimentos.atualizar_status_atendimento(atendimento_token, 'concluido', 'concluido')
        flash('Atendimento finalizado.', 'success')
        
    elif acao == 'solicitar_medicamento':
        workflow.adicionar_tarefa_farmacia(atendimento_token, nome_paciente)
        atendimentos.atualizar_status_atendimento(atendimento_token, 'em_atendimento', 'farmacia')
        flash('Enviado para Farmácia.', 'success')
        
    elif acao == 'dispensar_medicamento':
        workflow.adicionar_tarefa_enfermagem(atendimento_token, nome_paciente)
        atendimentos.atualizar_status_atendimento(atendimento_token, 'em_atendimento', 'enfermagem')
        flash('Enviado para Enfermagem.', 'success')
        
    elif acao == 'finalizar_atendimento':
        atendimentos.atualizar_status_atendimento(atendimento_token, 'concluido', 'concluido')
        flash('Finalizado.', 'success')
    
    return redirect(url_for('dashboard'))

# Rotas API e Filtros omitidos para brevidade (mantenha os existentes)
# ... (Seu código original tinha filtros e APIs, mantenha-os)
@app.template_filter('status_badge')
def status_badge(status):
    if status == tarefas.STATUS_CONCLUIDA: return 'success'
    return 'primary'

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def novo_usuario():
    if request.method == 'POST':
        # Lógica de cadastro de usuário (mantida)
        usuarios.cadastrar_usuario(request.form['nome'], request.form['login'], request.form['email'], request.form['senha'], request.form['setor'])
        return redirect(url_for('dashboard'))
    return render_template('novo_usuario.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)