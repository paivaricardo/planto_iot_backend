from mdl_dao import dao_verificar_cadastrar_usuario
from model.pydantic_rest_models.usuario_rest_model import UsuarioRestModel


def verificar_cadastrar_usuario_servico(usuario_rest_model: UsuarioRestModel):
    """
        Serviço que verifica se um usuário existe na base de dados, com base no e-mail fornecido. Se não existir, cadastra o usuário na base de dados.

        Retorna o id do usuário cadastrado na base de dados.
    """
    try:
        # Chamar o DAO para verificar se o usuário existe na base de dados
        usuario_cadastrado = dao_verificar_cadastrar_usuario.verificar_usuario_base_dados(usuario_rest_model)

        if usuario_cadastrado is None:
            # Chamar o DAO para verificar se o sensor ou atuador existe na base de dados, e se o cadastro foi completo ou não
            usuario_cadastrado = dao_verificar_cadastrar_usuario.cadastrar_usuario_base_dados(usuario_rest_model)
            return {"usuario_ja_existe_bd": False, "usuario_cadastrado": usuario_cadastrado}
        else:
            return {"usuario_ja_existe_bd": True, "usuario_cadastrado": usuario_cadastrado}
    except Exception as e:
        raise Exception("(Serviço) Erro ao tentar verificar ou cadastrar o usuário na base de dados", str(e))