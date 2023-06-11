from pydantic import BaseModel


class SensorAtuadorCadastroCompleto(BaseModel):
    id_sensor_atuador: int
    uuid_sensor_atuador: str
    nome_sensor: str
    latitude: float
    longitude: float
    id_usuario_cadastrante: int
    id_area: int
    id_cultura: int
