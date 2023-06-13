from pydantic import BaseModel


class UsuarioRestModel(BaseModel):
    email_usuario: str
    nome_usuario: str
    id_perfil: int
