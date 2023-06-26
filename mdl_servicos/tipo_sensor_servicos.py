from mdl_dao import dao_tipo_sensor


def obter_tipos_sensores_servico():
    return dao_tipo_sensor.obter_tipos_sensores_bd()