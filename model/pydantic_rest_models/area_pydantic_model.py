from typing import Optional

from pydantic import BaseModel


class AreaPydanticModel(BaseModel):
    id_area: Optional[int]
    nome_area: str
