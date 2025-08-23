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

    items = data.get("items", [])
    if not items:
        return jsonify(error="Carrito vacío"), 400

    preference_data = {
        "items": [
            {
                "title": item.get("nombre", "Producto"),
                "quantity": int(item.get("cantidad", 1)),
                # 👇 usamos precio_base (unitario) o total/cantidad
                "unit_price": float(item.get("precio_base", item.get("total", 0))),
                "currency_id": "MXN",
            }
            for item in items
        ],
        "back_urls": {
            "success": "https://mbgzone.com/success",
            "failure": "https://mbgzone.com/failure",
            "pending": "https://mbgzone.com/pending",
        },
        "auto_return": "approved",
        # "auto_return": "approved", por ahora en  produccion sin autoreturn
    }

    try:
        preference = sdk.preference().create(preference_data)
        print("✅ Respuesta completa MercadoPago:", preference)
        
        init_point = (
            preference["response"].get("init_point")
            or preference["response"].get("sandbox_init_point")
        )

        if not init_point:
            return jsonify(error="No se pudo generar el link de pago"), 400

        return jsonify({"init_point": init_point})

    except Exception as e:
        print("❌ Error MercadoPago:", str(e))
        return jsonify(error=str(e)), 400
