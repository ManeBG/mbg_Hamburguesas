from flask import Blueprint, jsonify
from models.models import EstadoNegocio

estado_bp = Blueprint("estado_bp", __name__)

@estado_bp.route("/api/estado", methods=["GET"])
def obtener_estado():
    estado = EstadoNegocio.query.first()

    if not estado:
        return jsonify({"estado": "cerrado", "mensaje": "Sin datos"}), 500

    estado_str = "abierto" if estado.esta_abierto == 1 else "cerrado"

    return jsonify({
        "estado": estado_str,
        "mensaje": estado.mensaje or ""
    })
