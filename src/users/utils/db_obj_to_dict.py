from core.types import ModelType


def db_obj_to_dict(obj: ModelType) -> dict:
    d = {}
    for column in obj.__table__.columns:
        d[column.name] = getattr(obj, column.name)
    return d
