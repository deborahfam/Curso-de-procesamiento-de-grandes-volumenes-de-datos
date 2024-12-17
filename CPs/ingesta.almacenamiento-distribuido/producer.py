import time
import json
import requests
from kafka import KafkaProducer

# URL de la API pública de Coindesk
API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# Configuración de Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_bitcoin_price():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            return data['bpi']['USD']['rate_float']
        else:
            print("Error al obtener datos de la API")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

while True:
    price = fetch_bitcoin_price()
    if price:
        message = {
            'price': price,
            'timestamp': time.time()
        }
        producer.send('bitcoin_price', value=message)  # Enviar datos a Kafka
        print(f"Precio de Bitcoin enviado a Kafka: {price}")
    time.sleep(10)  # Esperar 10 segundos antes de la siguiente captura
