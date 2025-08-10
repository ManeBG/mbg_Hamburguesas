from flask import Blueprint, request, jsonify, session
from models.models import Usuario
from common.db import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if Usuario.query.filter_by(correo=data["correo"]).first():
        return jsonify({"error": "El correo ya está registrado"}), 409

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        telefono=data["telefono"],
        password_hash=generate_password_hash(data["password"])
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado correctamente"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(correo=data["correo"]).first()

    if not usuario or not check_password_hash(usuario.password_hash, data["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    session["user_id"] = usuario.id
    session["nombre"] = usuario.nombre
    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "user_id": usuario.id,
        "nombre": usuario.nombre,
        "telefono": usuario.telefono
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada"})


# funciones para probar api en test y ver si todo ok
@auth_bp.route("/dev-login", methods=["POST"])
def dev_login():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "user_id requerido (entero)"}), 400

    session["user_id"] = user_id
    session.permanent = True
    # Si quieres controlar duración:
    session.modified = True
    return jsonify({"ok": True, "user_id": user_id}), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    return jsonify({"user_id": session.get("user_id")}), 200
