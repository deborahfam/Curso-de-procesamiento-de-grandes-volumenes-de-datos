import sys
import time
import json
import requests
from kafka import KafkaProducer, KafkaConsumer
from hdfs import InsecureClient
from rich.console import Console
from rich.table import Table
import threading

# ==========================
# Configuración global
# ==========================
API_COIN_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
API_WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?latitude=23.13&longitude=-82.38&current_weather=true'

KAFKA_TOPIC = 'multi_api_data'
HDFS_URL = 'http://localhost:9870'
HDFS_DIR = '/user/data/api_files/'

# Configuración del productor y consumidor de Kafka
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )
# consumer = KafkaConsumer(
#     KAFKA_TOPIC,
#     bootstrap_servers='localhost:9092',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8')),
#     group_id='my-consumer-group',
#     auto_offset_reset='earliest'
# )




client = InsecureClient(HDFS_URL, user='root')
console = Console()  # Instancia de la consola Rich

# Configuración corregida de Kafka
KAFKA_CONFIG = {
    'bootstrap_servers': ['172.26.0.2:9092'],
    'client_id': 'api_client',
    'request_timeout_ms': 10000,
    'api_version_auto_timeout_ms': 10000,
    'security_protocol': 'PLAINTEXT'
}

# Configuración específica para el producer
PRODUCER_CONFIG = {
    **KAFKA_CONFIG,
    'acks': 'all',
    'retries': 3,
    'retry_backoff_ms': 1000
}

# Configuración específica para el consumer
CONSUMER_CONFIG = {
    **KAFKA_CONFIG,
    'group_id': 'my-consumer-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
    'auto_commit_interval_ms': 1000,
    'session_timeout_ms': 10000,      # 10 segundos para el timeout de sesión
    'request_timeout_ms': 30000,      # 30 segundos para el timeout de request
    'heartbeat_interval_ms': 3000     # 3 segundos para el heartbeat
}

# Primero, verificar si el topic existe, si no, crearlo
try:
    from kafka.admin import KafkaAdminClient, NewTopic
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
        client_id=KAFKA_CONFIG['client_id']
    )
    
    # Verificar si el topic existe
    topics = admin_client.list_topics()
    if KAFKA_TOPIC not in topics:
        console.log(f"[yellow]El topic {KAFKA_TOPIC} no existe. Creándolo...[/yellow]")
        topic = NewTopic(name=KAFKA_TOPIC, num_partitions=1, replication_factor=1)
        admin_client.create_topics([topic])
        console.log(f"[green]Topic {KAFKA_TOPIC} creado exitosamente[/green]")
    else:
        console.log(f"[green]Topic {KAFKA_TOPIC} ya existe[/green]")
except Exception as e:
    console.log(f"[red]Error al verificar/crear el topic: {str(e)}[/red]")
    raise SystemExit(1)

# Inicializar el producer con retry
for attempt in range(3):
    try:
        producer = KafkaProducer(
            **PRODUCER_CONFIG,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        console.log("[green]Conexión exitosa con Kafka producer[/green]")
        break
    except Exception as e:
        console.log(f"[yellow]Intento {attempt + 1} fallido al conectar con Kafka: {str(e)}[/yellow]")
        if attempt == 2:
            console.log("[red]No se pudo establecer conexión con Kafka después de 3 intentos[/red]")
            raise SystemExit(1)
        time.sleep(5)

# Inicializar el consumer con retry
for attempt in range(3):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            **CONSUMER_CONFIG,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        console.log("[green]Conexión exitosa con Kafka consumer[/green]")
        break
    except Exception as e:
        console.log(f"[yellow]Intento {attempt + 1} fallido al conectar con Kafka consumer: {str(e)}[/yellow]")
        if attempt == 2:
            console.log("[red]No se pudo establecer conexión con Kafka consumer después de 3 intentos[/red]")
            raise SystemExit(1)
        time.sleep(5)

def create_hdfs_directory(path):
    """
    Crea la carpeta en HDFS si no existe.
    """
    try:
        if not client.status(path, strict=False):
            console.log(f"[yellow]Creando la carpeta en HDFS: {path}[/yellow]")
            client.makedirs(path)
            client.set_permission(path, permission='777')
            console.log(f"[green]Carpeta {path} creada con éxito en HDFS[/green]")
    except Exception as e:
        console.log(f"[red]Error al crear la carpeta en HDFS: {e}[/red]")

# Crear la carpeta al iniciar el script
create_hdfs_directory(HDFS_DIR)

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
            console.log(f"[red]Error al obtener datos de Coindesk (status {response.status_code})[/red]")
            return None
    except Exception as e:
        console.log(f"[red]Error: {e}[/red]")
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
            console.log(f"[red]Error al obtener datos de Open-Meteo (status {response.status_code})[/red]")
            return None
    except Exception as e:
        console.log(f"[red]Error: {e}[/red]")
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
            future = producer.send(KAFKA_TOPIC, value=message)
            try:
                record_metadata = future.get(timeout=10)
                console.log(f"[green]Mensaje enviado a Kafka - Topic: {record_metadata.topic}, Partition: {record_metadata.partition}, Offset: {record_metadata.offset}[/green]")
            except Exception as e:
                console.log(f"[red]Error al enviar mensaje a Kafka: {str(e)}[/red]")
        
        time.sleep(5) # Capturar cada 15 segundos


# ==========================
# SECCIÓN 3: Consumidor de Kafka y Almacenamiento en HDFS
# ==========================

def consume_and_store_data():
    """
    Consume mensajes de Kafka y los almacena en HDFS.
    """
    console.log("[yellow]Iniciando consumidor de Kafka[/yellow]")
    
    # Verificar conexión con HDFS
    try:
        console.log("[yellow]Verificando conexión con HDFS...[/yellow]")
        client.status('/', strict=True)
        console.log("[green]Conexión con HDFS establecida correctamente[/green]")
    except Exception as e:
        console.log(f"[red]Error de conexión con HDFS: {str(e)}[/red]")
        return

    # Verificar que el directorio existe
    try:
        create_hdfs_directory(HDFS_DIR)
    except Exception as e:
        console.log(f"[red]Error fatal al crear directorio: {str(e)}[/red]")
        return

    # Verificar que estamos recibiendo mensajes de Kafka
    console.log("[yellow]Esperando mensajes de Kafka...[/yellow]")
    
    for message in consumer:
        data = message.value
        console.log(f"[yellow]Mensaje recibido de Kafka: {data}[/yellow]")
        
        try:
            timestamp = int(time.time())
            file_path = f"{HDFS_DIR}data_{timestamp}.json"
            
            # Convertir los datos a string JSON
            json_data = json.dumps(data, indent=2)
            console.log(f"[yellow]Intentando escribir datos: {json_data}[/yellow]")
            
            # Intentar escribir el archivo
            with client.write(file_path, encoding='utf-8', overwrite=True) as writer:
                writer.write(json_data)
                writer.flush()
            
            # Verificar que el archivo se creó
            if client.status(file_path, strict=False):
                console.log(f"[green]Archivo guardado y verificado en HDFS: {file_path}[/green]")
            else:
                console.log(f"[red]¡Error! El archivo no se encuentra después de escribirlo: {file_path}[/red]")
                
        except Exception as e:
            console.log(f"[red]Error al guardar archivo en HDFS ({file_path}): {str(e)}[/red]")
            console.log(f"[red]Tipo de error: {type(e).__name__}[/red]")


# ==========================
# SECCIÓN 4: Visualización de archivos de HDFS en la consola
# ==========================

def display_kafka_and_hdfs():
    """
    Muestra tanto el contenido del topic de Kafka como los archivos en HDFS
    """
    while True:
        # Crear tabla para Kafka
        kafka_table = Table(title="Mensajes en Kafka Topic")
        kafka_table.add_column("Timestamp", justify="center", style="cyan")
        kafka_table.add_column("Bitcoin Price", justify="right", style="green")
        kafka_table.add_column("Temperature", justify="right", style="yellow")
        
        # Crear tabla para HDFS
        hdfs_table = Table(title="Archivos almacenados en HDFS")
        hdfs_table.add_column("Timestamp", justify="center", style="cyan")
        hdfs_table.add_column("Archivo", justify="left", style="green")
        
        # Obtener mensajes de Kafka (últimos 5)
        try:
            # Crear un consumidor temporal solo para mostrar mensajes
            temp_consumer = KafkaConsumer(
                KAFKA_TOPIC,
                **CONSUMER_CONFIG,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=2000  # 2 segundos timeout
            )
            
            messages = []
            for msg in temp_consumer:
                messages.append(msg.value)
                if len(messages) >= 5:  # Mostrar solo los últimos 5 mensajes
                    break
                    
            for msg in messages:
                kafka_table.add_row(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['timestamp'])),
                    f"${msg['bitcoin_price']:,.2f}",
                    f"{msg['weather_data']['temperature']}°C"
                )
            
            temp_consumer.close()
            
        except Exception as e:
            console.log(f"[red]Error al leer mensajes de Kafka: {str(e)}[/red]")
        
        # Obtener archivos de HDFS
        try:
            files = client.list(HDFS_DIR)
            for file in files:
                hdfs_table.add_row(time.ctime(), file)
        except Exception as e:
            console.log(f"[red]Error al listar archivos en HDFS: {str(e)}[/red]")

        # Limpiar consola y mostrar ambas tablas
        console.clear()
        console.print(kafka_table)
        console.print("\n")  # Espacio entre tablas
        console.print(hdfs_table)
        
        time.sleep(10)   # Actualizar cada 10 segundos


# ==========================
# SECCIÓN PRINCIPAL
# ==========================

def main():
    console.log("[yellow]Iniciando aplicación...[/yellow]")
    
    # Iniciar el productor primero
    producer_thread = threading.Thread(target=produce_api_data)
    producer_thread.daemon = True
    producer_thread.start()
    console.log("[green]Productor iniciado correctamente[/green]")

    # Esperar un poco para asegurar que hay datos en el topic
    console.log("[yellow]Esperando 20 segundos para que el productor genere algunos datos...[/yellow]")
    time.sleep(20)

    # Luego iniciar el consumidor
    consumer_thread = threading.Thread(target=consume_and_store_data)
    consumer_thread.daemon = True
    consumer_thread.start()
    console.log("[green]Consumidor iniciado correctamente[/green]")
    
    # Iniciar la visualización combinada
    try:
        display_kafka_and_hdfs()
    except KeyboardInterrupt:
        console.log("[yellow]Deteniendo la aplicación...[/yellow]")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.log("[yellow]Deteniendo la aplicación...[/yellow]")
        sys.exit(0)
