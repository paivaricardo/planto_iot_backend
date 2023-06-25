from typing import Optional

from pydantic import BaseModel


class AutorizacaoPydanticModel(BaseModel):
    id_sensor_atuador: int
    email_usuario: str
    id_perfil_autorizacao: int
    conectar: Optional[bool]
