from flask import Blueprint, jsonify
from models.models import EstadoNegocio, HorarioNegocio


estado_bp = Blueprint("estado_bp", __name__)
horario_bp = Blueprint("horario_bp", __name__)

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



@horario_bp.route("/api/horarios", methods=["GET"])
def obtener_horarios():
    horarios = HorarioNegocio.query.order_by(HorarioNegocio.id).all()
    resultado = []

    for h in horarios:
        resultado.append({
            "dia": h.dia_semana,
            "apertura": h.abre.strftime("%H:%M") if h.abre else "",
            "cierre": h.cierra.strftime("%H:%M") if h.cierra else "",
            "activo": h.activo == 1
        })

    return jsonify(resultado)
