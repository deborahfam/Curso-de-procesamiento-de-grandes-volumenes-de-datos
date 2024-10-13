# Lecture 3: Ecosistema Hadoop

- Introducción a Hadoop
- Historia y evolución
- Componentes principales: HDFS, MapReduce, YARN
- Sistema de archivos distribuidos Hadoop (HDFS)
- Arquitectura y principios de diseño
- Replicación de datos y tolerancia a fallos
- Modelo de programación MapReduce
- Funcionamiento de MapReduce
- Escritura de tareas MapReduce sencillas
- YARN (otro negociador de recursos)
- Gestión de recursos y programación de trabajos
- Herramientas relacionadas
- Hive (consultas tipo SQL)
- Pig (lenguaje de flujo de datos)
- HBase (base de datos NoSQL orientada a columnas)

images: https://www.altexsoft.com/blog/hadoop-pros-cons/

1. Hadoop

    Apache Hadoop es un potente marco de código abierto diseñado para procesar y analizar grandes cantidades de datos mediante procesamiento paralelo y almacenamiento distribuido. Desarrollado inicialmente en 2006 por Doug Cutting y Mike Cafarella para dar soporte al rastreador web Apache Nutch, Hadoop se ha consolidado desde entonces como una tecnología clave para el análisis de Big Data.

    En esencia, Hadoop descompone grandes conjuntos de datos en partes más pequeñas y manejables, distribuyéndolas a través de una red de hardware básico. Este enfoque permite a las organizaciones aprovechar un clúster interconectado de máquinas de bajo coste en lugar de depender de costosos superordenadores.

    - Un **clúster Hadoop** está formado por varios ordenadores, conocidos como nodos, que trabajan juntos como un sistema unificado. Cada nodo funciona de forma independiente con su propia memoria y almacenamiento, compartiendo únicamente una red común para la comunicación. La arquitectura de un cluster Hadoop se organiza típicamente en tres tipos principales de nodos:

    - **Nodo maestro**: Este nodo supervisa la gestión de datos y la asignación de recursos, coordinando las tareas de procesamiento en todo el clúster. Suele estar equipado con el hardware más robusto para gestionar estas responsabilidades con eficacia.

    - **Nodos esclavos** (trabajadores): Estos nodos realizan las tareas reales de procesamiento de datos asignadas por el nodo maestro. Se encargan de ejecutar los trabajos y almacenar los datos.

    - **Nodos cliente (Edge)**: Actuando como pasarelas, los nodos cliente facilitan la interacción entre el clúster Hadoop y los sistemas externos. Se encargan de la carga de datos y la recuperación de resultados sin formar parte de la jerarquía maestro-esclavo.

    El tamaño de un clúster Hadoop puede variar significativamente en función del volumen de datos. Por ejemplo, LinkedIn opera uno de los clústeres más grandes del mundo, con aproximadamente 10.000 nodos. Independientemente de su tamaño, cada clúster Hadoop abarca tres capas funcionales: el Sistema de Archivos Distribuidos Hadoop (HDFS) para el almacenamiento de datos, MapReduce para el procesamiento de datos y YARN (Yet Another Resource Negotiator) para la gestión de recursos.

    El **Hadoop Distributed File System (HDFS)** es una robusta solución de almacenamiento de datos diseñada específicamente para gestionar grandes cantidades de datos, desde gigabytes a petabytes. Divide eficazmente los archivos de gran tamaño en bloques más pequeños, normalmente de 128 MB, que luego se distribuyen entre varias máquinas de un clúster. Este tamaño de bloque puede configurarse en función de requisitos específicos.

2. HDFS

    HDFS funciona según el principio de «escribir una vez, leer muchas veces», priorizando la rápida recuperación de archivos enteros sobre la velocidad de escritura de datos. Una vez que los datos se almacenan en HDFS, no se pueden modificar; sin embargo, se puede acceder a ellos repetidamente para diversas tareas analíticas. Este diseño permite a las organizaciones aprovechar el mismo conjunto de datos para múltiples fines sin riesgo de alterar los datos originales.

    En el corazón de HDFS se encuentra el **NameNode**, un nodo maestro responsable de mantener los metadatos y la información crítica sobre los bloques de datos almacenados. El NameNode gestiona el acceso de los usuarios, supervisa la replicación de datos y coordina las operaciones entre los nodos esclavos. Para garantizar una alta disponibilidad y tolerancia a fallos, HDFS incluye NameNodes de reserva que pueden tomar el relevo si el NameNode primario falla. Hadoop 2 admite un nodo de reserva, mientras que Hadoop 3 permite múltiples nodos de reserva.

    Los nodos esclavos, conocidos como **DataNodes**, están organizados en racks y son responsables de almacenar y recuperar los datos según las indicaciones del NameNode. Cada DataNode gestiona su propio almacenamiento y se comunica con el NameNode para realizar operaciones de lectura y escritura.

3. MapReduce

    **MapReduce** es un paradigma de programación diseñado para el procesamiento distribuido eficiente de grandes conjuntos de datos. Originalmente desarrollado por Google, se ha convertido en un componente fundamental de muchos marcos de procesamiento de datos, siendo Hadoop la implementación de código abierto más ampliamente adoptada.

    El proceso MapReduce consta de dos pasos principales: **map** y **reduce**.

    1. **Fase de mapa**: En esta fase inicial, la función map procesa grandes entradas de datos dividiéndolos en trozos más pequeños. Cada trozo se analiza de acuerdo con las reglas especificadas para generar pares clave-valor. Por ejemplo, si el objetivo es analizar las frecuencias de palabras en un texto, cada palabra serviría de clave, mientras que su recuento correspondiente sería el valor. Si la palabra «aire» aparece tres veces en un determinado segmento de datos, la salida sería el par `<aire, 3>`.

    2. **Fase de reducción**: Tras el mapeo, la función de reducción se encarga de agregar y resumir los resultados. Organiza los pares clave-valor generados durante la fase de mapeo y combina los valores asociados a claves idénticas. En nuestro ejemplo, el reductor sumaría todos los recuentos de cada palabra única recogidos de varios trozos de datos.

    La arquitectura **MapReduce** opera en un modelo maestro-esclavo. El nodo maestro, conocido como **JobTracker**, recibe tareas de los nodos cliente e interactúa con el **NameNode** de HDFS para identificar qué DataNodes contienen los datos necesarios. A continuación, asigna las tareas a los **TaskTrackers** cercanos, que suelen estar ubicados junto a los DataNodes para optimizar el procesamiento de datos.

    Cada TaskTracker ejecuta las tareas map y reduce según las instrucciones del JobTracker y proporciona actualizaciones sobre su progreso. Si un TaskTracker falla durante la ejecución, el JobTracker puede reasignar sus tareas a otro nodo esclavo cercano, lo que garantiza la resistencia y la continuidad del procesamiento.

    Este enfoque estructurado permite a MapReduce gestionar eficazmente el procesamiento de datos a gran escala en clústeres, lo que lo convierte en una herramienta esencial para el análisis de Big Data.

## YARN

    YARN es la abreviatura de Yet Another Resource Negotiator (Otro negociador de recursos). A menudo denominada el cerebro de Hadoop, esta capa controla las aplicaciones distribuidas. Descarga al motor MapReduce de la programación de tareas y desvincula el procesamiento de datos de la gestión de recursos.

    Gracias a YARN, que actúa como un sistema operativo para las aplicaciones de Big Data y las conecta con HDFS, Hadoop puede admitir diferentes métodos de programación, enfoques de análisis de datos y motores de procesamiento distintos de MapReduce, por ejemplo, Apache Spark.

    Un maestro YARN - ResourceManager - tiene una visión holística del consumo de CPU y memoria en todo el clúster y optimiza la utilización de los recursos. Sus esclavos, NodeManagers, se ocupan de los nodos individuales, informando al maestro sobre sus recursos disponibles, su estado y su salud.

## Ecosistema

    Su naturaleza de código abierto y su modularidad atraen a muchos colaboradores que han estado trabajando en proyectos relacionados con Hadoop y mejorando sus capacidades. Como resultado, hoy contamos con un enorme ecosistema de instrumentos interoperables que abordan diversos retos de Big Data.

    Además de HDFS, el ecosistema Hadoop ofrece HBase, una base de datos NoSQL diseñada para albergar tablas de gran tamaño, con miles de millones de filas y millones de columnas.

    Para facilitar la ingestión de datos, existen Apache Flume, que agrega datos de registro de múltiples servidores, y Apache Sqoop, diseñado para transportar información entre Hadoop y bases de datos relacionales (SQL).

    Apache Pig, Apache Hive, Apache Drill y Apache Phoenix simplifican la exploración y el análisis de Big Data permitiendo utilizar lenguajes de consulta SQL y similares a SQL, familiares para la mayoría de los analistas de datos. Todas estas herramientas funcionan de forma nativa con MapReduce, HDFS y HBase.

    Instrumentos como Apache ZooKeeper y Apache Oozie ayudan a coordinar mejor las operaciones, programar los trabajos y realizar un seguimiento de los metadatos en un clúster Hadoop.

    El análisis de flujos se hizo posible con la introducción de Apache Kafka, Apache Spark, Apache Storm, Apache Flink y otras herramientas para construir canalizaciones de datos en tiempo real.

    También puede ejecutar aprendizaje automático en Hadoop con Apache Mahout o MLib y procesamiento de gráficos con Apache Giraph.
