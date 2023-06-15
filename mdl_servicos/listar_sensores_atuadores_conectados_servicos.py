from mdl_dao import dao_listar_sensores_atuadores_conectados


def listar_sensores_atuadores_conectados_servico(email_usuario: str):
    """
        Serviço que lista todos os sensores e atuadores conectados a um determinado usuário (de acordo com o ID repassado)
    """
    try:
        # Chamar o DAO para verificar se o usuário existe na base de dados
        return dao_listar_sensores_atuadores_conectados.listar_sensores_atuadores_conectados_bd(email_usuario)

    except Exception as e:
        raise Exception("(Serviço) Erro ao tentar verificar ou cadastrar o usuário na base de dados", str(e))