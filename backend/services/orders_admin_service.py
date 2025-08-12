from typing import Optional, Tuple
from sqlalchemy import or_
from models.models import Pedido
from common.db import db  # por si quieres queries directas


def listar_pedidos_admin(
    estado: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    q: Optional[str] = None
) -> Tuple[list[dict], int]:
    """
    Lista pedidos para el panel admin, con filtros y paginación.
    Incluye detalles (toppings, sin ingredientes) y snapshot de dirección.
    """
    query = Pedido.query  # ya tiene relación detalles con lazy='selectin'

    if estado and estado != "todos":
        query = query.filter(Pedido.estado == estado)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Pedido.nombre_cliente.ilike(like), Pedido.telefono.ilike(like))
        )

    total = query.count()

    pedidos = (
        query.order_by(Pedido.fecha.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    pedidos_dict = []
    for p in pedidos:
        pedidos_dict.append({
            "id": p.id,
            "estado": p.estado,
            "nombre": p.nombre_cliente,
            "telefono": p.telefono,
            "direccion": p.direccion_entrega,
            "total": float(p.total),
            "creado_en": p.fecha.isoformat(),
            "items": [
                {
                    "producto": d.nombre_producto,
                    "cantidad": 1,  # si luego agregas campo cantidad en DetallePedido, úsalo aquí
                    "precio_unitario": float(d.subtotal),
                    "toppings": d.toppings or [],
                    "sin": d.sin_ingredientes or [],
                    "nota": None
                }
                for d in p.detalles
            ]
        })

    return pedidos_dict, total
