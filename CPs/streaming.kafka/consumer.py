from kafka import KafkaConsumer
import json
import os

# TODO: Configurar el consumidor de Kafka
consumer = KafkaConsumer(
    'data_lake_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# TODO: Definir la carpeta del data lake
DATA_LAKE_DIR = "./data_lake"

def save_to_local(data, file_name="population_data.json"):
    """
    TODO: Implementar la función para guardar datos localmente
    - Crear el directorio si no existe
    - Escribir los datos en formato JSON
    - Implementar manejo de errores básico
    """
    pass

if __name__ == "__main__":
    # TODO: Implementar la lógica principal
    # - Crear un buffer para procesar por lotes
    # - Implementar la lógica de consumo de mensajes
    # - Guardar los datos cuando el buffer alcance cierto tamaño
    pass