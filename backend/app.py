import sys
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session


load_dotenv()  # carga variables de .env

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
PUBLIC_KEY = os.getenv("MP_PUBLIC_KEY")


# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Configuración y módulos propios
from config import DB_URI
from common.db import db
from models.models import *  # puedes cambiar esto por imports explícitos si quieres más control
from routes.pagos_routes import pagos_bp


# Blueprints
from routes.pedidos_routes import pedidos_bp
from routes.estado_routes import estado_bp, horario_bp
from routes.auth_routes import auth_bp
from routes.direcciones_routes import dir_bp
from routes.direcciones_routes import dir_bp as direcciones_bp  # ✅ nuevo
from routes.admin_pedidos_routes import admin_pedidos_bp

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
app.register_blueprint(pedidos_bp)
app.register_blueprint(estado_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(direcciones_bp)  # ✅ /api/direcciones
app.register_blueprint(admin_pedidos_bp)
app.register_blueprint(pagos_bp)           # 👈 registrar


# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)
