from flask import Flask

from extensions import db, csrf


app = Flask(__name__)


# Configuración
app.config.from_object('config.Config')


# Inicializar extensiones
db.init_app(app)

csrf.init_app(app)


# Blueprint
from routes.users import users_bp

app.register_blueprint(users_bp)


if __name__ == '__main__':

    app.run(debug=True)