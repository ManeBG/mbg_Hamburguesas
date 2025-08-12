# routes/admin_dev_routes.py  (SOLO DEV)
from flask import Blueprint, jsonify
from common.db import db
from sqlalchemy import text

admin_dev_bp = Blueprint("admin_dev_bp", __name__, url_prefix="/api/admin/dev")

@admin_dev_bp.post("/reset-pedidos")
def reset_pedidos():
    db.session.execute(text("DELETE FROM pedidos"))  # CASCADE borra detalles
    db.session.execute(text("ALTER TABLE detalles_pedido AUTO_INCREMENT = 1"))
    db.session.execute(text("ALTER TABLE pedidos AUTO_INCREMENT = 1"))
    db.session.commit()
    return jsonify({"ok": True})


@admin_dev_bp.get("/dbinfo")
def dbinfo():
    row = db.session.execute(text("SELECT DATABASE() AS db, @@sql_mode AS sql_mode")).mappings().first()
    return jsonify({"database": row["db"], "sql_mode": row["sql_mode"]})