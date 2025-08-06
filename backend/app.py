import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


from flask import Flask
from flask_cors import CORS
from config import DB_URI
from common.db import db
from routes.pedido_routes import pedido_bp
from models.models import *  # o tus modelos individuales
from routes.estado_routes import estado_bp

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # ✅ Esto es lo que conecta db con Flask

# Registrar blueprints
app.register_blueprint(pedido_bp)
app.register_blueprint(estado_bp)

# Crear tablas (solo se ejecuta una vez si no existen)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
