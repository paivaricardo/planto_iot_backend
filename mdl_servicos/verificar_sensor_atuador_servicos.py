from uuid import UUID

from mdl_dao import dao_verificar_sensor_atuador

def verificar_existencia_sensor_atuador_servico(uuid: UUID):
    """
    Verifica se um sensor ou atuador foi precadastrado na base de dados e se o cadastro dele foi completo ou não.

    Retorna um dicionário com o status do precadastro e do cadastro do sensor ou atuador, juntamente com informações do sensor ou do atuador.
    """
    try:
        # Chamar o DAO para verificar se o sensor ou atuador existe na base de dados, e se o cadastro foi completo ou não
        sensor_atuador_status = dao_verificar_sensor_atuador.verificar_existencia_sensor_atuador_base_dados(uuid)

        return sensor_atuador_status
    except Exception as e:
        raise Exception("Erro ao verificar o status do cadastro do sensor ou do atuador na base de dados", str(e))