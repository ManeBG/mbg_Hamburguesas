# app.py

from flask import Flask
from flask_cors import CORS
from config import db, DB_URI
from routes.pedido_routes import pedido_bp
from models import *

app = Flask(__name__)
CORS(app)

# Configurar SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar rutas
app.register_blueprint(pedido_bp)

# Crear tablas si no existen (opcional)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
