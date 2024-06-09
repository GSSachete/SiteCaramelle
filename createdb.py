from app import app, db

# Garante que estamos dentro do contexto da aplicação Flask
with app.app_context():
    # Cria todas as tabelas no banco de dados
    db.create_all()

print("Banco de dados criado com sucesso!")
