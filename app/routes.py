from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.models import Product
from werkzeug.utils import secure_filename
import os
from pathlib import Path

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

        if user and user.check_password(password):
            # Autentica o usuário
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            # Se as credenciais estiverem incorretas, exibe uma mensagem de erro
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
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Define a senha de forma segura
        db.session.add(new_user)
        db.session.commit()

        flash('Registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

@app.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    if request.method == 'GET':
        produtos = Product.query.all()
        return render_template('catalogo.html', produtos=produtos)
    elif request.method == 'POST':
        # Verificar se o campo 'id' está presente no formulário
        produto_id = request.form.get('id')
        if produto_id:
            # Consultar o produto no banco de dados
            produto = Product.query.get(produto_id)
            if produto:
                # Excluir o produto do banco de dados
                db.session.delete(produto)
                db.session.commit()
                flash('Produto excluído com sucesso!', 'success')
            else:
                flash('Produto não encontrado.', 'danger')
        else:
            # Obter os dados do formulário para adicionar um novo produto
            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = request.form['preco']
            
            # Lidar com o arquivo de imagem enviado
            imagem = request.files['imagem']
            if imagem.filename != '':
                filename = secure_filename(imagem.filename)
                # Caminho onde a imagem será salva
                caminho_imagem = Path(app.root_path) / 'static' / 'Imagens' / filename
                # Salvar a imagem no caminho especificado
                imagem.save(caminho_imagem)
                imagem_url = str(caminho_imagem.relative_to(app.root_path))
            else:
                imagem_url = None
            
            # Criar o novo produto
            novo_produto = Product(nome=nome, descricao=descricao, preco=preco, imagem=imagem_url)
            db.session.add(novo_produto)
            db.session.commit()

            flash('Produto adicionado com sucesso!', 'success')

        # Redirecionar de volta para a página do catálogo
        return redirect(url_for('produtos'))


@app.route('/estoque')
@login_required
def estoque():
    return render_template('estoque.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
@app.route('/logout')
def logout():
    logout_user()
    # Redirecione para a página de login, ou qualquer outra página desejada após o logout
    return redirect(url_for('index'))

   



@app.route('/produtos')
@login_required
def produtos():
    produtos = Product.query.all()
    return render_template('produtos.html', produtos=produtos)


