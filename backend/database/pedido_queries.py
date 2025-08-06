from common.db import db  # ✅ correcto
from models.models import Pedido, DetallePedido
import json

def guardar_pedido(pedido_items, total, nombre, telefono, direccion_entrega):
    try:
        # Crear el objeto pedido
        nuevo_pedido = Pedido(
            nombre_cliente=nombre,
            telefono=telefono,
            direccion_entrega=direccion_entrega,  # 👈 importante
            total=total,
            estado="pendiente"
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


def obtener_pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    resultado = []

    for pedido in pedidos:
        detalles = DetallePedido.query.filter_by(pedido_id=pedido.id).all()
        detalles_data = [{
            "nombre_producto": d.nombre_producto,
            "toppings": d.toppings,
            "sin_ingredientes": d.sin_ingredientes,
            "subtotal": float(d.subtotal)
        } for d in detalles]

        resultado.append({
            "id": pedido.id,
            "nombre_cliente": pedido.nombre_cliente,
            "direccion_entrega": pedido.direccion_entrega,
            "telefono": pedido.telefono,
            "total": pedido.total,
            "estado": pedido.estado,
            "fecha": pedido.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "detalles": detalles_data
        })

    return resultado
