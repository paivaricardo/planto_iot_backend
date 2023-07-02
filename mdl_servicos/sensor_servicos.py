from mdl_dao import dao_sensor


def obter_sensores_servico():
    return dao_sensor.obter_sensores_bd()
