from typing import Optional

from pydantic import BaseModel


class CulturaPydanticModel(BaseModel):
    id_cultura: Optional[int]
    nome_cultura: str
