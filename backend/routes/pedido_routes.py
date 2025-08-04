from flask import Blueprint, request, jsonify
from database.pedido_queries import guardar_pedido

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route("/api/pedido", methods=["POST"])
def recibir_pedido():
    data = request.get_json()
    pedido = data.get("pedido")
    total = data.get("total")
    nombre = data.get("nombre")
    telefono = data.get("telefono")
    direccion = data.get("direccion")

    exito = guardar_pedido(pedido, total, nombre, telefono, direccion)

    if exito:
        return jsonify({"mensaje": "Pedido guardado con éxito"})
    else:
        return jsonify({"error": "Hubo un problema al guardar el pedido"}), 500
