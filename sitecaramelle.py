from app import app, db
from flask_migrate import Migrate

migrate = Migrate(app, db)
app.secret_key = 'palesao'
if __name__ == '__main__':
    app.run(debug=True)