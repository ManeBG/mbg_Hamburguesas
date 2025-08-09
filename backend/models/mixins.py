from sqlalchemy.inspection import inspect

class ToDictMixin:
    def to_dict(self):
        data = {}
        for c in inspect(self).mapper.column_attrs:
            v = getattr(self, c.key)
            # conversión simple de Date/Decimal si algún día lo necesitas
            if hasattr(v, "isoformat"):
                v = v.isoformat()
            data[c.key] = v
        return data
