from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime
import json
from hdfs import InsecureClient
from kafka import KafkaConsumer
import time
import os

# Configuración de Rich
console = Console()
layout = Layout()

# Configuración de HDFS y Kafka
HDFS_URL = 'http://localhost:9870'
HDFS_DIR = '/user/data/bitcoin_prices/'

def setup_hdfs():
    """Configura la conexión HDFS y crea el directorio si no existe"""
    try:
        client = InsecureClient(HDFS_URL, user='root')
        
        # Verificar si el directorio existe
        try:
            client.status(HDFS_DIR)
            console.print(f"[green]Directorio HDFS {HDFS_DIR} existe[/green]")
        except:
            # Crear el directorio y sus padres
            client.makedirs(HDFS_DIR)
            console.print(f"[yellow]Directorio HDFS {HDFS_DIR} creado[/yellow]")
        
        # Verificar permisos escribiendo un archivo de prueba
        test_file = f"{HDFS_DIR}test.txt"
        try:
            with client.write(test_file, encoding='utf-8') as writer:
                writer.write("test")
            client.delete(test_file)
            console.print("[green]Permisos de escritura verificados[/green]")
        except Exception as e:
            console.print(f"[red]Error de permisos: {str(e)}[/red]")
            return None
        
        return client
    except Exception as e:
        console.print(f"[red]Error de conexión con HDFS: {str(e)}[/red]")
        return None

# Configurar HDFS
hdfs_client = setup_hdfs()

# Directorio local como respaldo
LOCAL_DIR = './bitcoin_data/'
os.makedirs(LOCAL_DIR, exist_ok=True)

consumer = KafkaConsumer(
    'bitcoin_price',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def save_data(data, timestamp):
    """Guarda los datos en HDFS o localmente"""
    filename = f"bitcoin_price_{timestamp}.json"
    
    if hdfs_client:
        try:
            file_path = f"{HDFS_DIR}{filename}"
            with hdfs_client.write(file_path, encoding='utf-8') as writer:
                json.dump(data, writer)
            console.print(f"[green]Archivo guardado en HDFS: {filename}[/green]")
            return "HDFS", filename
        except Exception as e:
            console.print(f"[red]Error al escribir en HDFS: {str(e)}[/red]")
    
    # Fallback a almacenamiento local
    local_path = os.path.join(LOCAL_DIR, filename)
    with open(local_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    console.print(f"[yellow]Archivo guardado localmente: {filename}[/yellow]")
    return "Local", filename

def generate_table(messages, files):
    """Genera la tabla de mensajes y archivos"""
    table = Table(title="Bitcoin Price Monitor")
    table.add_column("Timestamp", justify="center", style="cyan")
    table.add_column("Price (USD)", justify="right", style="green")
    table.add_column("Last File Saved", justify="left", style="magenta")
    
    for msg in messages[-5:]:
        table.add_row(
            msg['timestamp'],
            f"${msg['price']:,.2f}",
            msg.get('last_file', 'Not saved yet')
        )
    return table

def main():
    messages = []
    saved_files = []
    last_time = time.time()

    with Live(layout, refresh_per_second=1) as live:
        for message in consumer:
            current_time = time.time()
            data = message.value
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if current_time - last_time > 60:
                storage_type, filename = save_data(data, int(current_time))
                data['last_file'] = f"{storage_type}: {filename}"
                saved_files.append(filename)
                last_time = current_time
            else:
                data['last_file'] = "Waiting for next save..."

            messages.append(data)
            layout.update(generate_table(messages, saved_files))
            live.refresh()

if __name__ == "__main__":
    console.print("[yellow]Starting Bitcoin Price Monitor...[/yellow]")
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]Monitoring stopped by user[/red]")