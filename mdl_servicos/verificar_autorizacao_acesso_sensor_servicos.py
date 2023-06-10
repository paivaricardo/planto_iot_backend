from mdl_dao import dao_verificar_autorizacao_acesso_sensor


def verificar_autorizacao_acesso_sensor_servicos(uuid: str, email_usuario: str):
    """
    Verifica se um usuário tem autorização para acessar um sensor ou atuador.

    Retorna um dicionário com o status da autorização de acesso do usuário ao sensor ou atuador.
    """
    try:
        # Chamar o DAO para verificar se o usuário tem autorização para acessar o sensor ou atuador
        sensor_atuador_autorizacao = dao_verificar_autorizacao_acesso_sensor.verificar_autorizacao_acesso_sensor_database(uuid, email_usuario)

        return sensor_atuador_autorizacao
    except Exception as e:
        raise Exception("Erro ao verificar a autorização de acesso do usuário ao sensor ou ao atuador", str(e))