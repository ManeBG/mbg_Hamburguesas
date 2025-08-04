from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/pedido", methods=["POST"])
def recibir_pedido():
    data = request.get_json()
    print("📦 Pedido recibido:")
    print(data)

    # Crear carpeta pedidos si no existe
    os.makedirs("pedidos", exist_ok=True)

    # Guardar con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pedidos/pedido_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return jsonify({"mensaje": "¡Pedido guardado exitosamente!"})

if __name__ == "__main__":
    app.run(debug=True)
