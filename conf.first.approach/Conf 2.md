# Conf 2: Arquitectura y ecosistema de Big Data

- Componentes de la arquitectura de Big Data
- Fuentes de datos, almacenamiento, procesamiento, análisis, visualización
- Paradigmas de procesamiento
- Procesamiento por lotes frente a procesamiento en tiempo real
- Introducción a las arquitecturas Lambda y Kappa
- Visión general de las tecnologías Big Data
- Ecosistema Hadoop
- Apache Spark
- Bases de datos NoSQL
- Soluciones de almacenamiento de datos
- Sistemas de archivos distribuidos
- Lagos de datos frente a almacenes de datos

1. Arquitectura General de Big Data (Añadir para la explicacion un diagrama que muestra el flujo desde las fuentes de datos hasta el análisis)

    La arquitectura de Big Data consta de varios componentes esenciales que permiten a las organizaciones gestionar y analizar eficazmente grandes volúmenes de datos. He aquí un resumen de los componentes clave:

    1. Fuentes de datos: Las fuentes de datos son las entradas iniciales de las arquitecturas de Big Data, y abarcan datos estructurados y no estructurados de diversos orígenes, como bases de datos, redes sociales, sensores y registros web. Estos pueden incluir:

       - Bases de datos: Bases de datos relacionales tradicionales.
       - Redes sociales: Datos de plataformas como Twitter y Facebook.
       - Dispositivos IoT: Sensores y dispositivos inteligentes que generan datos en tiempo real.
       - Registros web: Información de registros de servidores e interacciones de usuarios.

    2. Ingestión: La ingesta es el proceso de extracción y transformación de datos de diversas fuentes en un formato coherente adecuado para su almacenamiento y procesamiento. Este paso puede implicar la validación, limpieza y normalización de los datos para garantizar su alta calidad.  

    3. Almacenamiento: El componente de almacenamiento se centra en la selección de la infraestructura adecuada para conservar los datos recopilados. Entre las soluciones más comunes se incluyen:

       - Lagos de datos (Data Lake): Para el almacenamiento de datos en bruto y no estructurados.
       - Almacenes de datos (Data Warehouse): Para el almacenamiento de datos estructurados y organizados.

    4. Procesamiento: El procesamiento implica el uso de tecnologías como Hadoop o Apache Spark para manipular y analizar los datos. Estas tecnologías permiten el procesamiento distribuido, permitiendo la ejecución paralela de tareas a través de grandes conjuntos de datos al tiempo que garantizan la tolerancia a fallos y la escalabilidad.

    5. Análisis: Este componente emplea herramientas y algoritmos para extraer información de los datos. Las técnicas pueden incluir algoritmos de aprendizaje automático, análisis estadístico y herramientas de visualización de datos destinadas a descubrir patrones que informen las decisiones empresariales.

    6. Orquestación: La orquestación se refiere a la automatización de los flujos de trabajo dentro de la arquitectura, garantizando que varios procesos se ejecuten sin problemas y sin intervención manual a medida que llegan nuevos datos.

    7. Procesamiento en tiempo real: Algunas arquitecturas incorporan la ingesta de mensajes en tiempo real y el procesamiento de flujos para gestionar los datos a medida que llegan, lo que permite un análisis y una comprensión inmediatos.

    En conjunto, estos componentes crean un marco sólido que permite la ingestión, el procesamiento, el almacenamiento y el análisis de conjuntos de datos masivos, lo que permite a las organizaciones obtener información procesable y tomar decisiones informadas basadas en sus datos.

2. Paradigmas de Procesamiento: (Grafico para explicar esto, que contraste procesamiento por lotes, de flujos, micro-lotes e interactivo.)

        - Procesamiento por lotes (Batch Processing): Tratamiento de grandes conjuntos de datos estáticos. El procesamiento por lotes implica el manejo de grandes volúmenes de datos a la vez, normalmente de forma programada (por ejemplo, diaria o semanalmente). Este paradigma es adecuado para escenarios en los que el análisis en tiempo real no es crítico. Los resultados suelen almacenarse por separado para su posterior consulta.
        - Procesamiento de flujos (Stream Processing):  El procesamiento de flujos se centra en el análisis de datos en tiempo real, lo que permite a las organizaciones procesar los datos a medida que llegan. Este paradigma se utiliza en aplicaciones que requieren información inmediata, como la supervisión de dispositivos IoT o transacciones financieras. Frameworks como **Apache Kafka** y **Apache Storm** facilitan este tipo de procesamiento al permitir el manejo y análisis de datos con baja latencia.
        -  Procesamiento de micro-lotes (Micro-Batch Processing): El procesamiento en micro-lotes es una variante del procesamiento en flujo que procesa los datos en pequeños lotes en lugar de individualmente. Este método logra un equilibrio entre la latencia del procesamiento por lotes tradicional y la inmediatez del procesamiento de flujos. **Apache Spark Streaming** ejemplifica este paradigma al permitir el procesamiento casi en tiempo real sin dejar de utilizar operaciones orientadas a lotes.
        -  Procesamiento interactivo (Interactive Processing): El procesamiento interactivo permite a los usuarios consultar y analizar datos de forma dinámica, a menudo utilizando herramientas que admiten consultas *ad hoc*. Este paradigma es esencial para los científicos y analistas de datos que requieren un acceso rápido a la información sin tener que esperar a que se completen los trabajos por lotes de larga duración. Tecnologías como Apache Drill o Presto están diseñadas para este fin.

3. Introduction to Lambda and Kappa Architectures (lustraciones de cada arquitectura destacando sus componentes y flujo de datos.)

    1. Lambda
        La arquitectura Lambda es una arquitectura de procesamiento de datos que proporciona una solución para manejar grandes volúmenes de datos de forma escalable y tolerante a fallos. La arquitectura está diseñada para procesar simultáneamente flujos de datos por lotes y en tiempo real. Consta de tres capas:

        - Capa de lotes: La capa de lotes se encarga de almacenar y procesar todos los datos en bruto, sin procesar. Actúa como el conjunto de datos maestro, que puede ser procesado por las otras dos capas. La capa de procesamiento por lotes suele utilizar un sistema de archivos distribuido como Hadoop Distributed File System (HDFS) para almacenar los datos y herramientas de procesamiento por lotes como Apache Spark, Apache Flink o Hadoop MapReduce para el procesamiento.
        - Capa de velocidad: La capa de velocidad procesa los flujos de datos en tiempo real a medida que llegan. Procesa los datos en tiempo real y su resultado se envía a la capa de servicio. La capa de velocidad suele utilizar un marco de procesamiento de flujos como Apache Kafka, Apache Storm o Apache Samza para procesar flujos de datos en tiempo real.
        - Capa de servicio: La capa de servicio proporciona acceso de baja latencia a los resultados de las capas de procesamiento por lotes y de velocidad. Sirve de interfaz entre los datos procesados y los usuarios finales que necesitan acceder a ellos. La capa de servicio suele utilizar una base de datos como Apache Cassandra, HBase o MongoDB para almacenar los datos procesados, y un motor de consulta como Apache Hive, Apache Impala o Presto para servir los datos a los usuarios finales.

        Ejemplo: Supongamos que trabajas para una empresa de redes sociales y necesitas procesar grandes cantidades de datos en tiempo real y por lotes para analizar el comportamiento de los usuarios y proporcionar información a los equipos de producto. He aquí cómo podría funcionar la arquitectura Lambda en este escenario:

        - Capa de lotes: La capa por lotes procesaría grandes volúmenes de datos en su forma cruda y sin procesar, que podría incluir datos como datos demográficos de los usuarios, publicaciones, me gusta, compartidos y comentarios. Los datos se almacenarían en un sistema de archivos distribuido como Hadoop Distributed File System (HDFS), y para procesarlos se utilizarían herramientas de procesamiento por lotes como Apache Spark o Hadoop MapReduce. La capa de procesamiento por lotes generaría vistas por lotes, como agregados diarios o semanales de los datos de comportamiento de los usuarios.
        - Capa de velocidad: La capa de velocidad procesaría flujos de datos en tiempo real a medida que llegan, como los datos de actividad de los usuarios como páginas vistas, clics y acciones. La capa de velocidad utilizaría un marco de procesamiento de flujos como Apache Kafka o Apache Storm para procesar los datos en tiempo real, y el resultado se introduciría en la capa de servicio. La capa de velocidad generaría vistas en tiempo real, como temas de tendencia, publicaciones populares o tasas de participación de los usuarios.
        - Capa de servicio: La capa de servicio combinaría los resultados de las capas de procesamiento por lotes y de velocidad para ofrecer una visión unificada de los datos. Los datos procesados se almacenarían en una base de datos como Apache Cassandra, y un motor de consulta como Apache Hive o Presto se encargaría de procesarlos.

    2. Kappa

        La arquitectura Kappa es una variación de la arquitectura Lambda, que está diseñada para manejar el procesamiento de datos en tiempo real de una manera más ágil y simplificada. Fue propuesta por Jay Kreps, uno de los cofundadores de Apache Kafka, en 2014.

        La Arquitectura Kappa solo tiene una capa para procesar flujos de datos en tiempo real, que es la misma que la capa de velocidad en la Arquitectura Lambda. Utiliza un sistema de procesamiento de flujos como Apache Kafka Streams, Apache Flink o Apache Samza para procesar los datos en tiempo real y almacenarlos en una base de datos como Apache Cassandra o Apache HBase.

        He aquí cómo podría funcionar la arquitectura Kappa en un escenario real:

        - Ingesta de datos: Los datos se ingieren en el sistema en tiempo real utilizando un sistema de mensajería como Apache Kafka.
        - Procesamiento de flujos: Los datos se procesan en tiempo real utilizando un sistema de procesamiento de flujos como Apache Kafka Streams, Apache Flink o Apache Samza. Los datos procesados se almacenan en una base de datos como Apache Cassandra o Apache HBase.
        - Capa de servicio: Los datos procesados se sirven a los usuarios finales utilizando un motor de consulta como Apache Hive o Presto.

        La arquitectura Kappa es más sencilla que la arquitectura Lambda porque elimina la necesidad de una capa de procesamiento por lotes, que requiere recursos adicionales de procesamiento y almacenamiento. Al procesar todos los datos en tiempo real, la arquitectura Kappa proporciona información en tiempo real sin necesidad de procesamiento por lotes. Sin embargo, la arquitectura Kappa puede no ser adecuada para todos los escenarios, especialmente para aquellos que requieren datos históricos.

4. Panorama de las tecnologías de big data

    Una visión general de las tecnologías que permiten el procesamiento de big data:

    - Ecosistema Hadoop: Herramientas de código abierto para almacenamiento y procesamiento distribuido.
    - Apache Spark: Motor para el procesamiento de big data con computación en memoria.
    - Bases de datos NoSQL: Bases de datos como MongoDB y Cassandra para datos no estructurados.

   1. Ecosistema Hadoop

        Un marco que permite el procesamiento distribuido de grandes conjuntos de datos a través de clústeres:

        - HDFS: Hadoop Distributed File System para almacenamiento.
        - MapReduce: Modelo de programación para el procesamiento.
        - YARN: Gestión de recursos.
        - Hive, Pig, HBase: Herramientas de consulta y gestión de datos.

   2. Apache Spark

        Motor de análisis unificado de código abierto para el procesamiento de datos a gran escala, conocido por su velocidad y facilidad de uso:

        Computación en memoria: Acelera el procesamiento.
        APIs: Compatible con Java, Scala, Python y R.
        Bibliotecas: Incluye SQL, streaming, MLlib para machine learning, GraphX.

   3. Bases de datos NoSQL

    Bases de datos no relacionales diseñadas para el almacenamiento de datos a gran escala y para manejar la variedad de big data:

    - Tipos: Bases de datos de documentos, de clave-valor, de columnas anchas y de grafos.
    - Ejemplos: MongoDB, Cassandra, Redis.
    - Ventajas: Escalabilidad, flexibilidad en los modelos de datos.

5. Soluciones de almacenamiento de datos

    Soluciones diseñadas para almacenar big data de forma eficiente:

    - Sistemas de archivos distribuidos: Como HDFS para grandes conjuntos de datos.
    - Lagos de datos: Almacenan datos en bruto en formato nativo.
    - Almacenes de datos: Almacenan datos estructurados y procesados para su análisis.

   1. Data Lakes vs. Data Warehouses

      1. Estructura de datos
           - Lago de datos: Almacena datos en bruto en su formato nativo, dando cabida a datos estructurados, semi-estructurados y no estructurados. No hay un esquema fijo, lo que permite flexibilidad en el almacenamiento y recuperación de datos. Esto se conoce como esquema en lectura.
           - Almacén de datos: Almacena datos procesados y estructurados, y suele requerir un esquema predefinido antes de cargar los datos. Esto se conoce como schema-on-write, que optimiza el rendimiento de las consultas.

      2. Propósito
           - Lago de datos: Diseñado para almacenar grandes cantidades de datos que pueden utilizarse posteriormente para diversos fines analíticos. Permite a las organizaciones conservar todos los datos hasta que sean necesarios para el análisis 34.
           - Almacén de datos: Se centra en proporcionar un repositorio centralizado de datos limpios y organizados específicamente para la inteligencia empresarial y la analítica .

      3. Metodología de procesamiento
        - Lago de datos: Utiliza un enfoque de extracción, carga y transformación (ELT), en el que los datos se cargan primero y se transforman según sea necesario durante el análisis .
        - Almacén de datos: Emplea un proceso de Extracción, Transformación y Carga (ETL), en el que los datos se limpian y estructuran antes de almacenarse.
