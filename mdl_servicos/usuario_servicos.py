from mdl_dao import dao_usuario


def obter_usuarios_servico():
    return dao_usuario.obter_usuarios_bd()