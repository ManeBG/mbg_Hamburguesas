import sys
import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session

# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Configuración y módulos propios
from config import DB_URI
from common.db import db
from models.models import *  # puedes cambiar esto por imports explícitos si quieres más control

# Blueprints
from routes.pedido_routes import pedido_bp
from routes.estado_routes import estado_bp, horario_bp
from routes.auth_routes import auth_bp
from routes.direcciones_routes import dir_bp
from routes.direcciones_routes import dir_bp as direcciones_bp  # ✅ nuevo

app = Flask(__name__)

# Configuración general
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "clave-ultra-mega-secreta"  # ⚠️ Cámbiala en producción

# Extensiones
CORS(app)
Session(app)
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(pedido_bp)
app.register_blueprint(estado_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(direcciones_bp)  # ✅ /api/direcciones

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)
