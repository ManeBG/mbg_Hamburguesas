from common.db import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    direccion_entrega = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'  # ✔️ nombre correcto

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    nombre_producto = db.Column(db.String(100), nullable=False)
    toppings = db.Column(db.JSON)
    sin_ingredientes = db.Column(db.JSON)
    subtotal = db.Column(db.Numeric(10, 2))

class HorarioNegocio(db.Model):
    __tablename__ = "horarios_negocio"
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)
    abre = db.Column(db.Time, nullable=True)
    cierra = db.Column(db.Time, nullable=True)
    activo = db.Column(db.Integer, nullable=False)  # 1 = abierto, 0 = cerrado


class EstadoNegocio(db.Model):
    __tablename__ = "estado_negocio"
    id = db.Column(db.Integer, primary_key=True)
    esta_abierto = db.Column(db.Integer, nullable=False)  # 1 o 0
    mensaje = db.Column(db.String(255), nullable=True)

