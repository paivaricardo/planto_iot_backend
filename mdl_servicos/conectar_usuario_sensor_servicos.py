from uuid import UUID

from mdl_dao import dao_verificar_sensor_atuador, dao_conectar_sensor_atuador_usuario, dao_buscar_id_usuario_com_email


def conectar_usuario_sensor_servico(uuid_sensor_atuador: UUID, email_usuario: str):
    """
    Serviço para conectar um usuário a um sensor ou atuador. O usuário será identificado pelo seu id, ao passo que o sensor ou atuador pelo seu uuid.

    Retorna um dicionário com códigos que representam o status da conexão com o sensor ou atuador, de acordo com o seguinte:
    1 - Conexão realizada com sucesso.
    2 - Usuário já está conectado ao sensor ou atuador.
    3 - Erro. Sensor ou atuador não existe na base de dados.
    4 - Erro. Sensor/atuador existe, mas o usuário não possui autorização para acesso ao sensor/atuador.
    5 - Erro. Cadastro do sensor não foi completado. É necessário completar o cadastro do sensor para que ele possa ser utilizado.
    6 - Erro. Usuário não existe na base de dados.
    7 - Erro desconhecido ao tentar conectar o usuário ao sensor/atuador.
    """
    try:
        # Chamar o DAO para verificar se o sensor ou atuador existe na base de dados, e se o cadastro foi completo ou não
        sensor_atuador_existe = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(
            uuid_sensor_atuador)

        # Se o sensor ou atuador não existe na base de dados, retornar o código correspondente (vide acima)
        if not sensor_atuador_existe["sensor_atuador_existe_bd"]:
            return {"cod_status_conexao": 3, "mensagem": "Erro. Sensor ou atuador não existe na base de dados."}

        # Verificar o id do usuário, a partir do e-mail fornecido
        id_usuario = dao_buscar_id_usuario_com_email.buscar_id_usuario_com_email(email_usuario)

        # Se o usuário não existe na base de dados, retornar o código correspondente (vide acima)
        if not id_usuario:
            return {"cod_status_conexao": 6, "mensagem": "Erro. Usuário não existe na base de dados."}

        # Retornar a lista de autorizações para um usuário em determinado sensor. É nessa autorização que será determinada a conexão do usuário, na coluna visualizacao_ativa
        autorizacoes_usuario = [autorizacao for autorizacao in sensor_atuador_existe["autorizacoes"] if
                                autorizacao["usuario"].id_usuario == id_usuario]

        # Se não houver autorização para o usuário, retornar o código correspondente (vide acima)
        if len(autorizacoes_usuario) == 0:
            return {"cod_status_conexao": 4, "mensagem": "Erro. Sensor/atuador existe, mas o usuário não possui autorização para acesso ao sensor/atuador."}

        # Se o cadastro do sensor não foi completado, retornar o código correspondente (vide acima)
        if not sensor_atuador_existe["sensor_atuador_foi_cadastrado"]:
            return {"cod_status_conexao": 5, "mensagem": "Erro. Cadastro do sensor não foi completado. É necessário completar o cadastro do sensor para que ele possa ser utilizado."}

        # Verificar se o usuário já está conectado ao sensor ou atuador. Se sim, não será feita a conexão e será devolvido o código correspondente (vide acima)
        if autorizacoes_usuario[0]["visualizacao_ativa"]:
            return {"cod_status_conexao": 2, "mensagem": "Usuário já está conectado ao sensor ou atuador."}

        if not autorizacoes_usuario[0]["visualizacao_ativa"]:
            sensor_atuador_conectado_usuario = dao_conectar_sensor_atuador_usuario.conectar_sensor_atuador_usuario_dao(
                autorizacoes_usuario[0])

            # Se a conexão for realizada com sucesso, retornar o código correspondente (vide acima)
            if sensor_atuador_conectado_usuario:
                return {"cod_status_conexao": 1, "mensagem": "Conexão realizada com sucesso."}
    except Exception as e:
        return {"cod_status_conexao": 7, "mensagem": f"Erro desconhecido ao tentar conectar o usuário ao sensor/atuador: {str(e)}"}