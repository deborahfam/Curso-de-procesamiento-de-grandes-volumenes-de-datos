# cp2 Ingesta, Almacenamiento distribuido y procesamiento distribuido

## Ejercicio 1: Configuración del entorno con Docker, HDFS y Kafka
Configurar un entorno que incluya un clúster HDFS y Kafka utilizando Docker. Crea un archivo `docker-compose.yml` que contenga la configuración para los servicios de HDFS y Kafka.

## Ejercicio 2: Captura de datos desde una API pública y envío a Kafka en tiempo real

En este ejercicio, utilizaremos la API pública de "https://api.coindesk.com/v1/bpi/currentprice.json" para obtener el precio de Bitcoin en tiempo real y enviarlo a Kafka actualizando cada 10 segundos. De esta manera, estaremos trabajando con datos que se actualizan continuamente.

## Ejercicio 3: Almacenamiento de datos en HDFS en tiempo real
En este ejercicio, vamos a crear un consumidor de Kafka que lea los datos sobre el precio de Bitcoin, los procese y luego los almacene en HDFS. Utilizaremos HDFS para almacenar los datos de manera distribuida y generar archivos cada cierto intervalo de tiempo.

## Ejercicio 4: Integración de múltiples APIs y visualización del flujo de archivos en HDFS

Capturar datos en tiempo real desde múltiples APIs públicas (ejemplo: precio de Bitcoin y el clima de una ciudad específica).
Usar un Kafka producer para enviar los datos de las APIs a un tópico de Kafka.
Crear un Kafka consumer que procese los datos de Kafka y los almacene de forma distribuida en HDFS.
Integrar con la interfaz gráfica con Tkinter que permita ver el flujo de archivos que se van guardando y procesando en HDFS.

Por ejemplo:

- https://api.coindesk.com/v1/bpi/currentprice.json
- https://api.open-meteo.com/v1/forecast?latitude=23.13&longitude=-82.38&current_weather=true
