# models.py

from config import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    nombre_cliente = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion_entrega = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    estado = db.Column(db.String(20), default="pendiente")

    detalles = db.relationship("DetallePedido", backref="pedido", cascade="all, delete-orphan")

class DetallePedido(db.Model):
    __tablename__ = "detalles_pedido"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    nombre_producto = db.Column(db.String(100))
    toppings = db.Column(db.Text)
    sin_ingredientes = db.Column(db.Text)
    subtotal = db.Column(db.Numeric(10, 2))

class DireccionEnvio(db.Model):
    __tablename__ = "direcciones_envio"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    alias = db.Column(db.String(50))
    calle = db.Column(db.Text)
    referencias = db.Column(db.Text)
    colonia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    activo = db.Column(db.Boolean, default=True)

class EstadoNegocio(db.Model):
    __tablename__ = "estado_negocio"
    id = db.Column(db.Integer, primary_key=True)
    esta_abierto = db.Column(db.Boolean, default=True)
    mensaje = db.Column(db.Text)

class HorarioNegocio(db.Model):
    __tablename__ = "horarios_negocio"
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(10))
    abre = db.Column(db.Time)
    cierra = db.Column(db.Time)
    activo = db.Column(db.Boolean, default=True)
