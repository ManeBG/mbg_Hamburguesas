from flask import Blueprint, request, jsonify
from services.addresses_service import (
    listar_direcciones,
    crear_direccion,
    actualizar_direccion,
    borrar_direccion,
)

dir_bp = Blueprint("dir_bp", __name__, url_prefix="/api/direcciones")

@dir_bp.route("", methods=["GET"])
def get_direcciones():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400
    direcciones = listar_direcciones(user_id)  # ← lista de modelos
    return jsonify([d.to_dict() for d in direcciones])  # ← usar to_dict()

@dir_bp.route("", methods=["POST"])
def post_direccion():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400
    d = crear_direccion(user_id, data)  # ← regresa el modelo
    return jsonify({"mensaje": "Dirección creada", "id": d.id, "direccion": d.to_dict()}), 201

@dir_bp.route("/<int:dir_id>", methods=["PUT", "PATCH"])
def put_direccion(dir_id):
    data = request.get_json() or {}
    d = actualizar_direccion(dir_id, data)  # ← puede regresar None
    if d is None:
        return jsonify({"error": "No encontrada"}), 404
    return jsonify({"mensaje": "Dirección actualizada", "direccion": d.to_dict()})

@dir_bp.route("/<int:dir_id>", methods=["DELETE"])
def delete_direccion(dir_id):
    d = borrar_direccion(dir_id)  # ← puede regresar None
    if d is None:
        return jsonify({"error": "No encontrada"}), 404
    return jsonify({"mensaje": "Dirección desactivada", "direccion": d.to_dict()})
