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

# Configuración de Rich
console = Console()
layout = Layout()

# Configuración de HDFS y Kafka
HDFS_URL = 'http://localhost:9870'
HDFS_DIR = '/user/data/bitcoin_prices/'

client = InsecureClient(HDFS_URL, user='root')
consumer = KafkaConsumer(
    'bitcoin_price',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def generate_table(messages, hdfs_files):
    """Genera la tabla de mensajes Kafka"""
    table = Table(title="Bitcoin Price Monitor")
    table.add_column("Timestamp", justify="center", style="cyan")
    table.add_column("Price (USD)", justify="right", style="green")
    table.add_column("Status", justify="center", style="magenta")
    
    for msg in messages[-5:]:  # Mostrar últimos 5 mensajes
        table.add_row(
            msg['timestamp'],
            f"${msg['price']:,.2f}",
            msg['status']
        )
    return table

def generate_hdfs_panel(hdfs_files):
    """Genera el panel de archivos HDFS"""
    hdfs_content = "\n".join([f"📄 {file}" for file in hdfs_files[-5:]])
    return Panel(
        hdfs_content,
        title="Latest HDFS Files",
        border_style="blue"
    )

def main():
    messages = []
    hdfs_files = []
    last_time = time.time()

    with Live(layout, refresh_per_second=1) as live:
        for message in consumer:
            current_time = time.time()
            data = message.value
            
            # Agregar timestamp y status al mensaje
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['status'] = "✅ Received"
            messages.append(data)

            # Si han pasado más de 60 segundos, guardar en HDFS
            if current_time - last_time > 60:
                file_path = f"{HDFS_DIR}bitcoin_price_{int(current_time)}.json"
                with client.write(file_path, encoding='utf-8') as writer:
                    json.dump(data, writer)
                hdfs_files.append(f"bitcoin_price_{int(current_time)}.json")
                last_time = current_time

            # Actualizar la visualización
            layout.split(
                generate_table(messages, hdfs_files),
                generate_hdfs_panel(hdfs_files)
            )
            live.refresh()

if __name__ == "__main__":
    console.print("[yellow]Starting Bitcoin Price Monitor...[/yellow]")
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]Monitoring stopped by user[/red]")