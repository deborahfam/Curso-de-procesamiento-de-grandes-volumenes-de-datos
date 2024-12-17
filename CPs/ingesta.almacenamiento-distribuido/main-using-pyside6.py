import time
import json
import requests
from kafka import KafkaProducer, KafkaConsumer
from hdfs import InsecureClient
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer

# ==========================
# Configuración global
# ==========================
API_COIN_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
API_WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?latitude=23.13&longitude=-82.38&current_weather=true'

KAFKA_TOPIC = 'multi_api_data'
HDFS_URL = 'http://localhost:9870'
HDFS_DIR = '/user/data/api_files/'

# Configuración del productor y consumidor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

client = InsecureClient(HDFS_URL, user='root')

# ==========================
# SECCIÓN 1: Captura de Datos de APIs Públicas
# ==========================

def fetch_bitcoin_price():
    """
    Realiza una petición a la API de Coindesk para obtener el precio del Bitcoin.

    Retorno:
        float: Precio actual de Bitcoin en USD.
    """
    try:
        response = requests.get(API_COIN_URL)
        if response.status_code == 200:
            data = response.json()
            return data['bpi']['USD']['rate_float']
        else:
            print("Error al obtener datos de Coindesk")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_weather_data():
    """
    Realiza una petición a la API de Open-Meteo para obtener el clima actual.

    Retorno:
        dict: Diccionario con los datos del clima actual.
    """
    try:
        response = requests.get(API_WEATHER_URL)
        if response.status_code == 200:
            data = response.json()
            return data['current_weather']
        else:
            print("Error al obtener datos de Open-Meteo")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# ==========================
# SECCIÓN 2: Productor de Kafka
# ==========================

def produce_api_data():
    """
    Captura los datos de las APIs y los envía a Kafka.
    """
    while True:
        bitcoin_price = fetch_bitcoin_price()
        weather_data = fetch_weather_data()
        
        if bitcoin_price and weather_data:
            message = {
                'bitcoin_price': bitcoin_price,
                'weather_data': weather_data,
                'timestamp': time.time()
            }
            producer.send(KAFKA_TOPIC, value=message)
            print(f"Datos enviados a Kafka: {message}")
        
        time.sleep(15)  # Capturar cada 15 segundos


# ==========================
# SECCIÓN 3: Consumidor de Kafka y Almacenamiento en HDFS
# ==========================

def consume_and_store_data():
    """
    Consume los datos de Kafka y los almacena de forma distribuida en HDFS.
    """
    for message in consumer:
        data = message.value
        file_path = f"{HDFS_DIR}data_{int(time.time())}.json"
        
        with client.write(file_path, encoding='utf-8') as writer:
            json.dump(data, writer)
        
        print(f"Archivo guardado en HDFS: {file_path}")


# ==========================
# SECCIÓN 4: Interfaz Gráfica (Visualización de archivos HDFS)
# ==========================

class FileTrackerApp(QMainWindow):
    """
    Interfaz gráfica para visualizar el flujo de archivos que se almacenan en HDFS.
    """
    def __init__(self):
        super(FileTrackerApp, self).__init__()
        self.setWindowTitle("Flujo de Archivos en HDFS")
        
        # Configuración del layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Crear el TreeView para mostrar los archivos
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Timestamp', 'Archivo'])
        
        self.layout.addWidget(self.tree)
        
        # Configurar un temporizador para actualizar la lista de archivos cada 10 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_files)
        self.timer.start(10000)  # Actualización cada 10 segundos
        
        self.update_files()
    
    def update_files(self):
        """
        Actualiza la lista de archivos almacenados en HDFS.
        """
        # Limpiar los elementos actuales
        self.tree.clear()
        
        try:
            files = client.list(HDFS_DIR)
            for file in files:
                item = QTreeWidgetItem(self.tree)
                item.setText(0, time.ctime())
                item.setText(1, file)
        except Exception as e:
            print(f"Error al listar archivos en HDFS: {e}")


# ==========================
# SECCIÓN PRINCIPAL
# ==========================

if __name__ == '__main__':
    import threading
    
    # Ejecutar el productor de Kafka en segundo plano
    producer_thread = threading.Thread(target=produce_api_data)
    producer_thread.daemon = True
    producer_thread.start()

    # Ejecutar el consumidor de Kafka en segundo plano
    consumer_thread = threading.Thread(target=consume_and_store_data)
    consumer_thread.daemon = True
    consumer_thread.start()
    
    # Iniciar la aplicación gráfica
    app = QApplication([])
    window = FileTrackerApp()
    window.show()
    app.exec()
