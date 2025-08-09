# services/orders_service.py
from common.db import db
from models.models import Pedido, DetallePedido, DireccionEnvio
from datetime import datetime

def crear_pedido(data: dict) -> Pedido:
    items = data.get("pedido", [])
    total = float(data.get("total", 0) or 0)
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    user_id = data.get("user_id")
    direccion_texto = data.get("direccion_entrega")
    direccion_id = data.get("direccion_id")

    # Validaciones mínimas
    if not nombre or not telefono:
        raise ValueError("Nombre y teléfono son obligatorios")
    if not items:
        raise ValueError("El pedido está vacío")
    if not (direccion_texto or direccion_id):
        raise ValueError("Falta dirección (texto) o direccion_id")

    address_id_to_save = None
    if direccion_id:
        d = DireccionEnvio.query.get(int(direccion_id))
        if not d or not d.activo:
            raise ValueError("Dirección no válida")
        if user_id and d.user_id != int(user_id):
            raise ValueError("La dirección no pertenece al usuario")
        direccion_texto = ", ".join(filter(None, [
            d.calle, d.colonia, d.ciudad, d.codigo_postal,
            f"Ref: {d.referencias}" if d.referencias else None
        ]))
        address_id_to_save = d.id

    p = Pedido(
        nombre_cliente=nombre,
        telefono=telefono,
        direccion_entrega=(direccion_texto or "")[:200],  # snapshot SIEMPRE
        total=total,
        user_id=int(user_id) if user_id else None,
        address_id=address_id_to_save,
        fecha=datetime.utcnow()
    )
    db.session.add(p)
    db.session.flush()

    for it in items:
        dp = DetallePedido(
            pedido_id=p.id,
            nombre_producto=it.get("nombre_producto") or it.get("sku") or "Producto",
            toppings=it.get("toppings"),
            sin_ingredientes=it.get("sin_ingredientes"),
            subtotal=it.get("subtotal", 0)
        )
        db.session.add(dp)

    db.session.commit()
    return p
