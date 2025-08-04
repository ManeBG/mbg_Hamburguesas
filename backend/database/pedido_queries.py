from config import db
from models import Pedido, DetallePedido
import json

def guardar_pedido(pedido_items, total, nombre, telefono, direccion):
    try:
        # Crear el objeto pedido
        nuevo_pedido = Pedido(
            total=total,
            nombre_cliente=nombre,
            telefono=telefono,
            direccion_entrega=direccion
        )
        db.session.add(nuevo_pedido)
        db.session.flush()  # obtiene el id antes de commit

        # Agregar detalles del pedido
        for item in pedido_items:
            detalle = DetallePedido(
                pedido_id=nuevo_pedido.id,
                nombre_producto=item["nombre"],
                toppings=json.dumps(item["toppings"], ensure_ascii=False),
                sin_ingredientes=json.dumps(item["sin_ingredientes"], ensure_ascii=False),
                subtotal=item["total"]
            )
            db.session.add(detalle)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print("❌ Error al guardar pedido:", e)
        return False
