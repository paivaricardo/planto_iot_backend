import base64
from io import BytesIO

import matplotlib.pyplot as plt


def gerar_relatorio_leitura_sensor(informacoes_sensor, leituras_sensor_dicts):
    try:
        if informacoes_sensor["sensor_atuador_info"].id_tipo_sensor == 10000:
            values = [float(leitura['json_leitura']['percentualUmidadeSolo']) for leitura in
                                       leituras_sensor_dicts]
            timestamps = [leitura['data_hora_leitura'] for leitura in leituras_sensor_dicts]

            # Gerar o gráfico usando o matplotlib
            plt.plot(timestamps, values)
            plt.xlabel('Datas')
            plt.ylabel('Value')
            plt.title('Sensor Readings')
            plt.xticks(rotation=45)

            # Salvar o gráfico em um buffer de memória BytesIO
            image_buffer = BytesIO()
            plt.savefig(image_buffer, format='png')
            image_buffer.seek(0)

            # Close the matplotlib figure to free resources
            plt.close()

            # Convert image file to bytes
            image_bytes = image_buffer.read()

            # Encode image bytes as base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            return encoded_image
        else:
            raise Exception(f"[REPORT - ERRO] Não existe um relatório para o tipo de sensor de UUID {informacoes_sensor['sensor_atuador_info'].id_tipo_sensor}")
    except Exception as e:
        raise Exception(f"[REPORT - ERRO] Erro ao tentar gerar o relatório de leitura do sensor de UUID {leituras_sensor_dicts[0]['id_sensor_atuador']}: {str(e)}")
