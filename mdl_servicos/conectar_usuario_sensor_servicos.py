from mdl_dao import dao_verificar_sensor_atuador, dao_conectar_sensor_atuador_usuario


def conectar_usuario_sensor_servico(uuid_sensor_atuador, id_usuario):
    """
    Serviço para conectar um usuário a um sensor ou atuador. O usuário será identificado pelo seu id, ao passo que o sensor ou atuador pelo seu uuid.

    """
    try:
        # Chamar o DAO para verificar se o sensor ou atuador existe na base de dados, e se o cadastro foi completo ou não
        sensor_atuador_existe = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(
            uuid_sensor_atuador)

        # Retornar a lista de autorizações para um usuário em determinado sensor. É nessa autorização que será determinada a conexão do usuário, na coluna visualizacao_ativa
        autorizacoes_usuario = [autorizacao for autorizacao in sensor_atuador_existe["autorizacoes"] if
                                autorizacao["usuario"].id_usuario == id_usuario]

        if sensor_atuador_existe["sensor_atuador_existe_bd"] and len(autorizacoes_usuario) > 0:
            sensor_atuador_conectado_usuario = dao_conectar_sensor_atuador_usuario.conectar_sensor_atuador_usuario_dao(
                autorizacoes_usuario[0])

            return sensor_atuador_conectado_usuario
        else:
            return False
    except Exception as e:
        raise Exception(f"Erro ao tentar conectar o usuario {id_usuario} ao sensor {uuid_sensor_atuador}", str(e))
