import mercadopago
from flask import Blueprint, request, jsonify
import os

pagos_bp = Blueprint("pagos_bp", __name__, url_prefix="/api/pagos")

# Inicia SDK con tu Access Token
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@pagos_bp.route("/checkout", methods=["POST"])
def checkout():
    data = request.json or {}
    print("📩 Datos recibidos:", data)

    # Extraer con .get para evitar errores
    nombre = data.get("nombre", "Producto sin nombre")
    cantidad = int(data.get("cantidad", 1))
    precio = float(data.get("precio", 0))

    # Validaciones básicas
    if precio <= 0:
        return jsonify(error="Precio inválido"), 400

    preference_data = {
        "items": [
            {
                "title": nombre,
                "quantity": cantidad,
                "unit_price": precio,
                "currency_id": "MXN",
            }
        ],
        "back_urls": {
            "success": "http://localhost:5173/success",
            "failure": "http://localhost:5173/failure",
            "pending": "http://localhost:5173/pending",
        },
        "auto_return": "approved",
    }

    try:
        preference = sdk.preference().create(preference_data)
        return jsonify({"init_point": preference["response"]["init_point"]})
    except Exception as e:
        print("❌ Error MercadoPago:", str(e))
        return jsonify(error=str(e)), 400
