from typing import Optional
from uuid import UUID

from mdl_dao import dao_precadastrar_sensor_atuador


def precadastrar_sensor_atuador_servico(id_tipo_sensor: int, uuid_selecionado: Optional[UUID] = None):
    try:
        # Chamar o DAO para fazer uma query na base de dados e verificar todos os tipos de sensores ou atuadores que podem ser registrados
        # Se o id_tipo_sensor não estiver na lista de tipos de sensores ou atuadores, lançar uma exceção
        lista_ids_tipos_sensores_atuadores = dao_precadastrar_sensor_atuador.obter_lista_tipos_sensores_atuadores()

        if id_tipo_sensor not in lista_ids_tipos_sensores_atuadores:
            raise Exception("ID do tipo de sensor ou atuador é inválido")

        # Chamar o DAO para fazer o precadastro do sensor ou do atuador na base de dados
        uuid_gerado = dao_precadastrar_sensor_atuador.precadastrar_sensor_atuador_base_dados(id_tipo_sensor, uuid_selecionado)

        return uuid_gerado
    except Exception as e:
        raise Exception("Erro ao precadastrar o sensor ou atuador na base de dados", str(e))