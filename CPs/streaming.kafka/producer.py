from kafka import KafkaProducer
import requests
import json

# TODO: Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# TODO: Definir la URL de la API
API_URL = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"

def fetch_data():
    """
    TODO: Implementar la función para obtener datos de la API
    - Realizar la petición GET a la API
    - Verificar el código de respuesta
    - Retornar los datos si son válidos
    """
    pass

def send_to_kafka(data):
    """
    TODO: Implementar la función para enviar datos a Kafka
    - Iterar sobre los datos
    - Enviar cada registro al topic de Kafka
    - Implementar manejo de errores básico
    """
    pass

if __name__ == "__main__":
    # TODO: Implementar la lógica principal
    pass