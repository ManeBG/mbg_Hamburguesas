from flask import Blueprint, request, jsonify
from services.orders_admin_service import listar_pedidos_admin

admin_pedidos_bp = Blueprint("admin_pedidos_bp", __name__, url_prefix="/api/admin/pedidos")

@admin_pedidos_bp.get("")
def get_pedidos_admin():
    estado = request.args.get("estado")
    page = request.args.get("page", type=int, default=1)
    page_size = request.args.get("page_size", type=int, default=20)
    q = request.args.get("q")

    pedidos, total = listar_pedidos_admin(
        estado=estado, page=page, page_size=page_size, q=q
    )
    return jsonify({
        "pedidos": pedidos,
        "total": total,
        "page": page,
        "page_size": page_size
    })
