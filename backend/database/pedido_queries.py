# database/pedido_queries.py

import json
from config import get_connection

def guardar_pedido(pedido, total, nombre, telefono, direccion):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Insertar pedido
            sql_pedido = """
                INSERT INTO pedidos (total, nombre_cliente, telefono, direccion_entrega)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_pedido, (total, nombre, telefono, direccion))
            pedido_id = cursor.lastrowid

            # Insertar detalles
            for item in pedido:
                sql_detalle = """
                    INSERT INTO detalles_pedido (pedido_id, nombre_producto, toppings, sin_ingredientes, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_detalle, (
                    pedido_id,
                    item["nombre"],
                    json.dumps(item["toppings"], ensure_ascii=False),
                    json.dumps(item["sin_ingredientes"], ensure_ascii=False),
                    item["total"]
                ))

            conn.commit()
            return True
    except Exception as e:
        print("❌ Error al guardar pedido:", e)
        return False
    finally:
        conn.close()
