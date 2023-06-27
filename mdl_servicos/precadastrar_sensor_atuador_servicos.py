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

        # Caso haja um uuid selecionado, verificar se ele já está cadastrado na base de dados
        if uuid_selecionado is not None:
            uuid_inedito = dao_precadastrar_sensor_atuador.verificar_uuid_selecionado_inedito(uuid_selecionado)

            if not uuid_inedito:
                return {"status": 1, "message": "UUID selecionado já está precadastrado na base de dados."}

        # Chamar o DAO para fazer o precadastro do sensor ou do atuador na base de dados
        sensor_atuador_precadastrado_info = dao_precadastrar_sensor_atuador.precadastrar_sensor_atuador_base_dados(id_tipo_sensor, uuid_selecionado)

        return {"status": 2, "message": "Sensor ou atuador precadastrado com sucesso na base de dados.", "sensor_atuador_precadastrado_info": sensor_atuador_precadastrado_info}
    except Exception as e:
        raise Exception("Erro ao precadastrar o sensor ou atuador na base de dados", str(e))