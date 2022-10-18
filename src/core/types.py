from typing import TypeVar

from pydantic import BaseModel

from core.db.base_class import Base
from core.dto import BaseOutSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaOutType = TypeVar("SchemaOutType", bound=BaseOutSchema)
