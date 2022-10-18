from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True


class BaseInSchema(OrmModel):
    pass


class BaseOutSchema(OrmModel):
    id: int
