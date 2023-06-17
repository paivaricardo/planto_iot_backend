from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SensorAtuadorCadastroCompleto(BaseModel):
    id_sensor_atuador: int
    uuid_sensor_atuador: UUID
    nome_sensor: str
    latitude: float
    longitude: float
    email_usuario_cadastrante: str
    id_area: int
    id_cultura: int
    observacoes: Optional[str]
