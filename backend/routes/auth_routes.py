from flask import Blueprint, request, jsonify, session
from models.models import Usuario
from common.db import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__)

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
        "nombre": usuario.nombre
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada"})
