from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu_segredo_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitecaramelle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Inicialize o Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models