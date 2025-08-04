# app.py

from flask import Flask
from flask_cors import CORS
from routes.pedido_routes import pedido_bp

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(pedido_bp)

if __name__ == "__main__":
    app.run(debug=True)
