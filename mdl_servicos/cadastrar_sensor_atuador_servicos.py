from mdl_dao import dao_verificar_sensor_atuador

def cadastrar_sensor_atuador_sevico(uuid: str):
    """
    Cadastra um sensor ou atuador na base de dados do Planto IoT, desde que ele já esteja precastrado cadastrado previamente.

    Retorna os dados que foram cadastrados na base de dados (tb_sensor_atuador).
    """
    try:
        # Chamar o DAO para verificar se o sensor ou atuador existe na base de dados, e se o cadastro foi completo ou não
        sensor_atuador_cadastrado = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(uuid)

        return sensor_atuador_cadastrado
    except Exception as e:
        raise Exception("Erro ao verificar o status do cadastro do sensor ou do atuador na base de dados", str(e))