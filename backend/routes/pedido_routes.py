# routes/pedido_routes.py
from flask import Blueprint, request, jsonify
from services.orders_service import crear_pedido
from models.models import Pedido
from common.db import db

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route("/api/pedido", methods=["POST"])
def post_pedido():
    data = request.get_json() or {}
    try:
        pedido = crear_pedido(data)  # <- mueve la lógica al service
        return jsonify({
            "mensaje": "Pedido registrado con éxito",
            "pedido_id": pedido.id,
            "resumen": {
                "cliente": pedido.nombre_cliente,
                "telefono": pedido.telefono,
                "direccion": pedido.direccion_entrega,
                "total": float(pedido.total),
                "estado": pedido.estado
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno"}), 500


@pedido_bp.route('/api/pedidos', methods=['GET'])
@pedido_bp.route('/api/mis-pedidos', methods=['GET'])
def listar_pedidos():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400
    filas = (Pedido.query
             .filter_by(user_id=user_id)
             .order_by(Pedido.fecha.desc())
             .all())
    out = [{
        "id": p.id,
        "fecha": p.fecha.isoformat(),
        "total": float(p.total),
        "estado": p.estado,
        "direccion": p.direccion_entrega
    } for p in filas]
    return jsonify(out)













# from flask import Blueprint, request, jsonify
# from database.pedido_queries import guardar_pedido, obtener_pedidos
# from models.models import Pedido, DetallePedido, DireccionEnvio
# from common.db import db

# pedido_bp = Blueprint('pedido_bp', __name__)

# @pedido_bp.route("/api/pedido", methods=["POST"])
# def recibir_pedido():
#     data = request.get_json()
#     pedido = data.get("pedido")
#     total = data.get("total")
#     nombre = data.get("nombre")
#     telefono = data.get("telefono")
#     direccion_entrega = data.get("direccion_entrega")
#     user_id = data.get("user_id")  # 👈 Aquí se obtiene el user_id

#     exito = guardar_pedido(pedido, total, nombre, telefono, direccion_entrega, user_id)

#     if exito:
#         return jsonify({"mensaje": "Pedido guardado con éxito"})
#     else:
#         return jsonify({"error": "Hubo un problema al guardar el pedido"}), 500



# @pedido_bp.route('/api/pedidos', methods=['GET'])
# def listar_pedidos():
#     try:
#         pedidos = obtener_pedidos()
#         return jsonify({"pedidos": pedidos})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




# @pedido_bp.route("/api/pedido", methods=["POST"])
# def confirmar_pedido():
#     data = request.get_json() or {}
#     items = data.get("pedido", [])
#     total = float(data.get("total", 0))
#     nombre = data.get("nombre")
#     telefono = data.get("telefono")
#     user_id = data.get("user_id")  # puede venir null
#     direccion_texto = data.get("direccion_entrega")  # libre
#     direccion_id = data.get("direccion_id")          # guardada (opcional)

#     # Validaciones mínimas
#     if not nombre or not telefono:
#         return jsonify({"error": "Nombre y teléfono son obligatorios"}), 400
#     if not (direccion_texto or direccion_id):
#         return jsonify({"error": "Falta dirección (texto) o direccion_id"}), 400
#     if not items:
#         return jsonify({"error": "El pedido está vacío"}), 400

#     # Si mandaron direccion_id, construimos el texto legible (snapshot)
#     address_id_to_save = None
#     if direccion_id:
#         d = DireccionEnvio.query.get(int(direccion_id))
#         if not d or not d.activo:
#             return jsonify({"error": "Dirección no válida"}), 400
#         # (Opcional) si trae user_id, validar pertenencia
#         if user_id and d.user_id != int(user_id):
#             return jsonify({"error": "La dirección no pertenece al usuario"}), 403
#         direccion_texto = ", ".join(filter(None, [
#             d.calle, d.colonia, d.ciudad, d.codigo_postal,
#             f"Ref: {d.referencias}" if d.referencias else None
#         ]))
#         address_id_to_save = d.id

#     # Crear pedido
#     p = Pedido(
#         nombre_cliente=nombre,
#         telefono=telefono,
#         direccion_entrega=direccion_texto[:200],  # proteger largo
#         total=total,
#         user_id=int(user_id) if user_id else None,
#         address_id=address_id_to_save
#     )
#     db.session.add(p)
#     db.session.flush()  # para obtener p.id

#     # Detalles
#     for it in items:
#         dp = DetallePedido(
#             pedido_id=p.id,
#             nombre_producto=it.get("nombre_producto") or it.get("sku") or "Producto",
#             toppings=it.get("toppings"),
#             sin_ingredientes=it.get("sin_ingredientes"),
#             subtotal=it.get("subtotal", 0)
#         )
#         db.session.add(dp)

#     db.session.commit()

#     # Respuesta lista para WhatsApp/Telegram si quieres
#     return jsonify({
#         "mensaje": "Pedido registrado con éxito",
#         "pedido_id": p.id,
#         "resumen": {
#             "cliente": nombre,
#             "telefono": telefono,
#             "direccion": p.direccion_entrega,
#             "total": total,
#             "estado": p.estado
#         }
#     }), 201



# @pedido_bp.route("/api/mis-pedidos", methods=["GET"])
# def mis_pedidos():
#     user_id = request.args.get("user_id", type=int)
#     if not user_id:
#         return jsonify({"error": "user_id requerido"}), 400

#     filas = (Pedido.query
#              .filter_by(user_id=user_id)
#              .order_by(Pedido.fecha.desc())
#              .all())

#     out = []
#     for p in filas:
#         out.append({
#             "id": p.id,
#             "fecha": p.fecha.isoformat(),
#             "total": float(p.total),
#             "estado": p.estado,
#             "direccion": p.direccion_entrega
#         })
#     return jsonify(out)
