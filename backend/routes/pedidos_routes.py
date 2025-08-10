# routes/pedidos_routes.py
from flask import Blueprint, request, jsonify, session
from decimal import Decimal
from services.orders_service import (
    crear_pedido as service_crear_pedido,
    listar_pedidos_de_usuario,
    actualizar_estado_pedido,
    ESTADOS_VALIDOS
)

pedidos_bp = Blueprint("pedidos_bp", __name__, url_prefix="/api/pedidos")

def _to_money_str(v) -> str:
    # v puede ser Decimal, float o int
    if isinstance(v, Decimal):
        return f"{v:.2f}"
    try:
        return f"{float(v):.2f}"
    except Exception:
        return "0.00"

def _pedido_to_json(p):
    return {
        "id": p.id,
        "nombre_cliente": p.nombre_cliente,
        "telefono": p.telefono,
        "direccion_entrega": p.direccion_entrega,
        "estado": p.estado,
        "fecha": p.fecha.isoformat() if p.fecha else None,
        "total": _to_money_str(p.total),
        "detalles": [
            {
                "id": d.id,
                "nombre_producto": d.nombre_producto,
                "toppings": d.toppings or [],
                "sin_ingredientes": d.sin_ingredientes or [],
                "subtotal": _to_money_str(d.subtotal),
            }
            for d in p.detalles
        ],
    }

# ------------------------
# Crear un pedido
# ------------------------
@pedidos_bp.route("", methods=["POST"])
def post_pedido():
    data = request.get_json(silent=True) or {}
    try:
        pedido = service_crear_pedido(data)
        return jsonify({
            "mensaje": "Pedido registrado con éxito",
            "pedido_id": pedido.id,
            "estado": pedido.estado,
            "direccion_entrega": pedido.direccion_entrega,
            "total": _to_money_str(pedido.total)
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Opcional: loggear e para debug
        from common.db import db
        db.session.rollback()
        return jsonify({"error": "Error interno"}), 500

# ------------------------
# Listar pedidos (admin por user_id)
# ------------------------
@pedidos_bp.route("", methods=["GET"])
def listar_pedidos():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400
    pedidos = listar_pedidos_de_usuario(user_id)
    return jsonify([_pedido_to_json(p) for p in pedidos]), 200

# ------------------------
# Listar mis pedidos (sesión)
# ------------------------
@pedidos_bp.route("/mios", methods=["GET"])
def listar_mis_pedidos():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401
    pedidos = listar_pedidos_de_usuario(user_id)
    return jsonify([_pedido_to_json(p) for p in pedidos]), 200

# ------------------------
# Cambiar estado de un pedido
# ------------------------
@pedidos_bp.route("/<int:pedido_id>/status", methods=["POST"])
def set_estado_pedido(pedido_id):
    data = request.get_json(silent=True) or {}
    estado = data.get("estado")
    if estado not in ESTADOS_VALIDOS:
        return jsonify({"error": "estado inválido", "permitidos": sorted(list(ESTADOS_VALIDOS))}), 400

    ok = actualizar_estado_pedido(pedido_id, estado)
    if not ok:
        return jsonify({"error": "pedido no encontrado"}), 404

    return jsonify({"ok": True, "pedido_id": pedido_id, "nuevo_estado": estado}), 200














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
