# models/mixins.py
from sqlalchemy.inspection import inspect
from decimal import Decimal

class ToDictMixin:
    def to_dict(self):
        data = {}
        for c in inspect(self).mapper.column_attrs:
            v = getattr(self, c.key)
            if hasattr(v, "isoformat"):
                v = v.isoformat()
            elif isinstance(v, Decimal):
                v = float(v)
            data[c.key] = v
        return data
