from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Necessário para default=datetime.utcnow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solicitante = db.Column(db.String(50))
    tipo_servico = db.Column(db.String(30))
    prioridade = db.Column(db.String(10))
    localizacao = db.Column(db.String(100))
    descricao = db.Column(db.Text)

class Tecnico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especialidade = db.Column(db.String(50))

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(200))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))  # "PF" ou "PJ"
    razao_social = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(100))
    cnpj_cpf = db.Column(db.String(20), unique=True)
    data_registro = db.Column(db.Date)  # Data abertura/Aniversário
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(150))  # Endereço
    quadra = db.Column(db.String(20))
    lote = db.Column(db.String(20))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    atividade = db.Column(db.String(100))  # Atividade econômica/Profissão
    total_funcionarios = db.Column(db.Integer)  # Só para PJ
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class HistoricoCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_compra = db.Column(db.DateTime)
    produto_servico = db.Column(db.String(200))
    valor = db.Column(db.Float)
    observacoes = db.Column(db.Text)

class TipoServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    tempo_medio = db.Column(db.Integer)  # Em minutos
    valor_base = db.Column(db.Float)
    ativo = db.Column(db.Boolean, default=True)

# Rotas
@app.route('/')
def dashboard():
    os_list = OrdemServico.query.all()
    return render_template('dashboard.html', ordens=os_list)

@app.route('/cadastrar_os', methods=['GET', 'POST'])
def cadastrar_os():
    if request.method == 'POST':
        nova_os = OrdemServico(
            solicitante=request.form['solicitante'],
            tipo_servico=request.form['tipo_servico'],
            prioridade=request.form['prioridade'],
            localizacao=request.form['localizacao'],
            descricao=request.form['descricao']
        )
        db.session.add(nova_os)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cadastro_os.html')

# Cadastro de tecnico
@app.route('/cadastrar_tecnico', methods=['GET', 'POST'])
def cadastrar_tecnico():
    if request.method == 'POST':
        tecnico = Tecnico(
            nome=request.form['nome'],
            especialidade=request.form['especialidade']
        )
        db.session.add(tecnico)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cadastro_tecnico.html')

# Cadastro de local
@app.route('/cadastrar_local', methods=['GET', 'POST'])
def cadastrar_local():
    if request.method == 'POST':
        local = Local(
            nome=request.form['nome'],
            endereco=request.form['endereco']
        )
        db.session.add(local)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cadastro_local.html')

# Cadastro de cliente
@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        novo_cliente = Cliente(
            tipo=request.form['tipo'],
            razao_social=request.form['razao_social'],
            nome_fantasia=request.form['nome_fantasia'],
            cnpj_cpf=request.form['cnpj_cpf'],
            data_registro=datetime.strptime(request.form['data_registro'], '%Y-%m-%d').date(),
            cep=request.form['cep'],
            rua=request.form['rua'],
            quadra=request.form['quadra'],
            lote=request.form['lote'],
            bairro=request.form['bairro'],
            cidade=request.form['cidade'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            atividade=request.form['atividade'],
            total_funcionarios=int(request.form['total_funcionarios']) if request.form['total_funcionarios'] else None
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cadastro_cliente.html')

# Rota cadastro de serviço
#@app.route('/cadastrar_servico')
#def cadastrar_servico():
    #return render_template('cadastro_servico.html')

# Rota para arquivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Rota para cadastro de serviço
@app.route('/cadastrar_servico', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        novoServico = TipoServico(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            categoria=request.form['categoria'],
            tempo_medio=request.form['tempo_medio'],
            valor_base=request.form['valor_base']
        )
        db.session.add(novoServico)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cadastro_servico.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)