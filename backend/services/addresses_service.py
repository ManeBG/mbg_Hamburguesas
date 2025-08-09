from models.models import DireccionEnvio
from common.db import db

def listar_direcciones(user_id: int):
    return (DireccionEnvio.query
            .filter_by(user_id=user_id, activo=True)
            .order_by(DireccionEnvio.id.desc())
            .all())

def crear_direccion(user_id: int, data: dict) -> DireccionEnvio:
    d = DireccionEnvio(
        user_id=user_id,
        alias=data.get("alias"),
        calle=data.get("calle"),
        referencias=data.get("referencias"),
        colonia=data.get("colonia"),
        ciudad=data.get("ciudad"),
        codigo_postal=data.get("codigo_postal"),
        activo=True
    )
    db.session.add(d)
    db.session.commit()
    return d

def actualizar_direccion(dir_id: int, data: dict):
    d = DireccionEnvio.query.get(dir_id)
    if not d:
        return None
    for campo in ["alias", "calle", "referencias", "colonia", "ciudad", "codigo_postal", "activo"]:
        if campo in data:
            setattr(d, campo, data[campo])
    db.session.commit()
    return d

def borrar_direccion(dir_id: int):
    d = DireccionEnvio.query.get(dir_id)
    if not d:
        return None
    d.activo = False
    db.session.commit()
    return d
