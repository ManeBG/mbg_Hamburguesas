from flask import Blueprint, request, jsonify
from database.pedido_queries import guardar_pedido, obtener_pedidos
from models.models import Pedido, DetallePedido

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route("/api/pedido", methods=["POST"])
def recibir_pedido():
    data = request.get_json()
    pedido = data.get("pedido")
    total = data.get("total")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    direccion_entrega = data.get("direccion_entrega")
    user_id = data.get("user_id")  # 👈 Aquí se obtiene el user_id

    exito = guardar_pedido(pedido, total, nombre, telefono, direccion_entrega, user_id)

    if exito:
        return jsonify({"mensaje": "Pedido guardado con éxito"})
    else:
        return jsonify({"error": "Hubo un problema al guardar el pedido"}), 500



@pedido_bp.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    try:
        pedidos = obtener_pedidos()
        return jsonify({"pedidos": pedidos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500