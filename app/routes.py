from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica se o usuário existe no banco de dados
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            # Se as credenciais estiverem corretas, redirecione para a página principal ou qualquer outra página desejada
            # Neste caso, redirecionarei para a página inicial
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            # Se as credenciais estiverem incorretas, exiba uma mensagem de erro
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('register'))

        # Verifica se o email já está em uso
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso. Por favor, use outro.', 'danger')
            return redirect(url_for('register'))

        # Cria um novo usuário e adiciona ao banco de dados
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)