# services/orders_service.py
from datetime import datetime
from typing import List, Optional
from flask import jsonify
from common.db import db
from models.models import Pedido, DetallePedido, DireccionEnvio

# Estados válidos centralizados (útiles si los reutilizas en más capas)
ESTADOS_VALIDOS = {"pendiente", "confirmado", "en_preparacion", "en_camino", "entregado", "cancelado"}

# Tolerancia para comparar total vs suma de subtotales (por centavitos)
TOTAL_TOLERANCE = 0.02


def _fmt_direccion_snapshot(d: DireccionEnvio) -> str:
    """Crea un texto snapshot legible a partir de una DireccionEnvio."""
    partes = [
        d.calle,
        d.colonia,
        d.ciudad,
        d.codigo_postal,
        f"Ref: {d.referencias}" if getattr(d, "referencias", None) else None
    ]
    return ", ".join([p.strip() for p in partes if p and str(p).strip()])[:200]


def _coerce_float(x) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def crear_pedido(data: dict) -> Pedido:
    """
    Crea un pedido con snapshot de dirección.
    Reglas:
      - Siempre guarda 'direccion_entrega' (texto), aunque venga 'direccion_id'.
      - Si viene 'direccion_id', valida que exista, esté activa y sea del user.
      - Valida nombre, teléfono, items y total aproximado.
    Espera un payload tipo:
      {
        "user_id": 1,
        "nombre": "Juan",
        "telefono": "744...",
        "direccion_entrega": "texto libre",  # opcional si se manda direccion_id
        "direccion_id": 10,                  # opcional si se manda direccion_entrega
        "total": 199.00,
        "pedido": [
          {
            "nombre_producto": "Hamburguesa Clásica",
            "toppings": ["queso","tocino"],
            "sin_ingredientes": ["cebolla"],
            "subtotal": 99.5
          },
          ...
        ]
      }
    """
    items = data.get("pedido") or data.get("items") or []
    total_cliente = _coerce_float(data.get("total"))
    nombre = (data.get("nombre") or "").strip()
    telefono = (data.get("telefono") or "").strip()
    user_id = data.get("user_id")
    direccion_texto = (data.get("direccion_entrega") or "").strip()
    direccion_id = data.get("direccion_id")

    # Validaciones mínimas
    if not nombre or not telefono:
        raise ValueError("Nombre y teléfono son obligatorios")
    if not items:
        raise ValueError("El pedido está vacío")
    if not (direccion_texto or direccion_id):
        raise ValueError("Falta dirección (texto) o direccion_id")

    # Si mandan direccion_id, validar dueño y armar snapshot
    address_id_to_save: Optional[int] = None
    if direccion_id:
        d: DireccionEnvio | None = DireccionEnvio.query.get(int(direccion_id))
        if not d or not getattr(d, "activo", True):
            raise ValueError("Dirección no válida")
        if user_id and d.user_id != int(user_id):
            raise ValueError("La dirección no pertenece al usuario")
        direccion_texto = _fmt_direccion_snapshot(d)
        address_id_to_save = d.id

    # Sumar subtotales para validar contra total
    suma_subtotales = sum(_coerce_float(it.get("subtotal")) for it in items)
    if abs(suma_subtotales - total_cliente) > TOTAL_TOLERANCE:
        raise ValueError(f"El total no coincide con la suma de los subtotales (cliente={total_cliente}, suma={suma_subtotales})")

    # Crear pedido
    p = Pedido(
        nombre_cliente=nombre,
        telefono=telefono,
        direccion_entrega=direccion_texto[:200] if direccion_texto else "",
        total=round(total_cliente, 2),
        user_id=int(user_id) if user_id else None,
        address_id=address_id_to_save,
        estado="pendiente",
        fecha=datetime.utcnow()
    )
    db.session.add(p)
    db.session.flush()  # para tener p.id

    # Crear detalles
    for it in items:
        dp = DetallePedido(
            pedido_id=p.id,
            nombre_producto=it.get("nombre_producto") or it.get("sku") or "Producto",
            toppings=it.get("toppings"),               # ajusta tipo en el modelo: JSON/Text
            sin_ingredientes=it.get("sin_ingredientes"),
            subtotal=round(_coerce_float(it.get("subtotal")), 2)
        )
        db.session.add(dp)

    db.session.commit()
    return p


def listar_pedidos_de_usuario(user_id: int) -> List[Pedido]:
    """
    Devuelve pedidos de un usuario ordenados por fecha desc.
    Las rutas llaman luego a p.as_dict() para serializar.
    """
    return (Pedido.query
            .filter_by(user_id=int(user_id))
            .order_by(Pedido.fecha.desc())
            .all())


def actualizar_estado_pedido(pedido_id: int, nuevo_estado: str) -> bool:
    """
    Cambia el estado de un pedido si existe y el estado es válido.
    Devuelve True si actualizó; False si no encontró el pedido.
    Lanza ValueError si el estado es inválido.
    """
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise ValueError("Estado inválido")

    p: Pedido | None = Pedido.query.get(int(pedido_id))
    if not p:
        return False

    p.estado = nuevo_estado
    db.session.commit()
    return True
