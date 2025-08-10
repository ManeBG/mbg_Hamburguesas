from common.db import db
from datetime import datetime
from models.mixins import ToDictMixin
from sqlalchemy import Index



class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class Pedido(ToDictMixin, db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    direccion_entrega = db.Column(db.String(200), nullable=False)  # snapshot SIEMPRE
    telefono = db.Column(db.String(20), nullable=False)
    # Mejor dinero con DECIMAL/Numeric:
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(20), default='pendiente', index=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    # FK real a direcciones_envio
    address_id = db.Column(db.Integer, db.ForeignKey('direcciones_envio.id'), nullable=True)

    detalles = db.relationship(
        'DetallePedido',
        backref='pedido',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    def as_dict(self):
        """Base con to_dict + lista de detalles."""
        base = self.to_dict()
        base["detalles"] = [d.to_dict() for d in self.detalles]
        return base

# Índices compuestos útiles (opcional pero recomendado)
Index("ix_pedidos_user_fecha", Pedido.user_id, Pedido.fecha.desc())

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'  # ✔️ nombre correcto

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    nombre_producto = db.Column(db.String(100), nullable=False)
    toppings = db.Column(db.JSON)
    sin_ingredientes = db.Column(db.JSON)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)


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



class DireccionEnvio(ToDictMixin, db.Model):
    __tablename__ = "direcciones_envio"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    alias = db.Column(db.String(50))
    calle = db.Column(db.Text)
    referencias = db.Column(db.Text)
    colonia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    activo = db.Column(db.Boolean, default=True)

