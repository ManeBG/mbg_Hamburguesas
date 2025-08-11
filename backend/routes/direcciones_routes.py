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

    direcciones = listar_direcciones(user_id)

    def serialize(d):
        return {
            "id": d.id,
            "calle": d.calle,
            "colonia": d.colonia,
            "ciudad": d.ciudad,
            "codigo_postal": getattr(d, "codigo_postal", None),
            "referencias": getattr(d, "referencias", None),
            "activo": getattr(d, "activo", True),
        }

    return jsonify([serialize(d) for d in direcciones]), 200


@dir_bp.route("", methods=["POST"])
def post_direccion():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400

    # ✨ ahora sí: pasa user_id y data
    try:
        d = crear_direccion(int(user_id), data)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Server error"}), 500

    # responde JSON minimal y estable
    return jsonify({"id": d.id}), 201


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
