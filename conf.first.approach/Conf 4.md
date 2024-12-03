# Lecture 4: Data Processing with Apache Spark

- Limitations of MapReduce
- Need for faster processing
- Introduction to Apache Spark
      - Unified analytics engine
      - Components: Spark Core, SQL, Streaming, MLlib, GraphX
      - Resilient Distributed Datasets (RDDs)
      - Creation and transformations
      - Actions and lazy evaluation
      - DataFrames and Datasets
      - Advantages over RDDs
      - Working with structured data
      - Spark SQL
      - Querying data with SQL syntax
      - Integration with Hive

1. Limitaciones de MapReduce
   La evolución de las tecnologías de procesamiento de macrodatos comienza con la comprensión de las limitaciones de MapReduce, que ha sido un marco fundacional en el manejo de datos a gran escala. MapReduce procesa los datos en modo batch y depende en gran medida de la E/S en disco entre las tareas map y reduce, lo que provoca una alta latencia e ineficiencias en los cálculos iterativos y los análisis en tiempo real.

   - Latencia en el procesamiento: La fase de reducción no puede comenzar hasta que todos los mappers han completado su trabajo, lo que introduce una latencia considerable en el procesamiento.
   - Uso intensivo del disco: MapReduce depende en gran medida del almacenamiento en disco, lo que ralentiza las operaciones, especialmente en tareas que requieren múltiples lecturas y escrituras.
   - Complejidad y curva de aprendizaje: La programación en MapReduce puede ser compleja, ya que requiere conocimientos de Java y una comprensión profunda del ecosistema Hadoop, lo que dificulta su adopción por nuevos desarrolladores.
   - Rigidez en la ejecución: No se puede controlar el orden en que se ejecutan las tareas, lo que limita la flexibilidad en ciertos tipos de trabajos

    A medida que las empresas enfrentan volúmenes crecientes de datos y demandas de procesamiento más ágiles, las deficiencias de MapReduce se vuelven más evidentes. Esto ha llevado al desarrollo y adopción de tecnologías como Apache Spark, que no solo superan las limitaciones mencionadas, sino que también permiten un procesamiento más eficiente y flexible.

2. Introducción a Apache Spark

    Para hacer frente a estos retos, se nos presenta Apache Spark, un sistema informático distribuido de código abierto diseñado para ofrecer velocidad y facilidad de uso. Spark supera las limitaciones de MapReduce mediante el uso de procesamiento en memoria y estrategias de ejecución optimizadas, lo que mejora significativamente el rendimiento de los datos por lotes y de flujo.

    En esencia, Apache Spark funciona como un motor analítico unificado, capaz de gestionar diversas cargas de trabajo como el procesamiento por lotes, el streaming en tiempo real, el aprendizaje automático y los cálculos de gráficos dentro de un único marco. Esta unificación simplifica la cadena de procesamiento de datos y reduce la complejidad asociada al mantenimiento de varios sistemas.

    El ecosistema Spark consta de varios componentes integrales:

    - Spark Core: La base que proporciona funcionalidades esenciales como la programación de tareas, la gestión de memoria, la recuperación de fallos y las interacciones con el sistema de almacenamiento.
    - Spark SQL: Permite realizar consultas y trabajar con datos estructurados utilizando SQL, así como las API DataFrame y Dataset.
    - Spark Streaming: Facilita el procesamiento escalable y tolerante a fallos de flujos de datos en tiempo real.
    - MLlib: Ofrece un conjunto de algoritmos y utilidades de aprendizaje automático escalables.
    - GraphX: proporciona una API para cálculos de gráficos y gráficos paralelos.

    Un elemento central de la arquitectura de Spark es el concepto de conjuntos de datos distribuidos resistentes (RDD, Resilient Distributed Datasets), que son colecciones inmutables y distribuidas de objetos repartidos en un clúster informático. Los RDD permiten el procesamiento en paralelo y son tolerantes a fallos, automatizan los procesos y reducen los costes.

3. Resilient Distributed Datasets (RDDs)

    Los RDDs son una característica clave de Apache Spark. Son colecciones inmutables y distribuidas que pueden ser procesadas en paralelo. Los RDDs permiten a los usuarios realizar operaciones complejas sin preocuparse por los detalles del manejo de fallos o la distribución de datos. Se pueden crear a partir de datos almacenados en sistemas externos o distribuyendo colecciones desde un programa controlador. Además, los RDDs soportan dos tipos principales de operaciones:

    - Transformaciones: Operaciones que crean un nuevo RDD a partir de uno existente (por ejemplo, map, filter).
    - Acciones: Operaciones que devuelven un resultado al controlador o escriben datos en un sistema externo (por ejemplo, count, collect).

    1. Creación y Transformaciones
        En Apache Spark, los RDDs (Resilient Distributed Datasets) son la base para la creación y manipulación de datos. Se pueden crear a partir de diversas fuentes, como archivos de texto, bases de datos o incluso otros RDDs.
        Las transformaciones son operaciones que permiten modificar un RDD para crear uno nuevo; ejemplos incluyen map, filter, y flatMap. Estas transformaciones son *lazy*, lo que significa que no se ejecutan inmediatamente, sino que se planifican hasta que se invoca una acción.
        Las acciones son operaciones que desencadenan la ejecución del flujo de trabajo en Spark, produciendo resultados finales o escribiendo datos en un sistema externo. Ejemplos de acciones incluyen count, collect y saveAsTextFile.

4. DataFrames y Datasets
    - Los DataFrames son una abstracción más avanzada que los RDDs, organizando los datos en columnas con nombres, similar a una tabla en una base de datos relacional. Los DataFrames permiten realizar operaciones SQL y ofrecen optimizaciones bajo el capó gracias a su integración con el motor de ejecución de Spark SQL. Se pueden crear a partir de diversas fuentes, como archivos CSV, JSON o tablas en Hive.

    - Los Datasets, introducidos en Spark 1.6, combinan las ventajas de los RDDs (fuertemente tipados y capacidad para usar funciones lambda) con las optimizaciones del motor de ejecución de Spark SQL. Un Dataset es esencialmente un DataFrame con un tipo específico, lo que permite un control más riguroso sobre la estructura de los datos.

5. Ventajas sobre RDDs
    Las ventajas de utilizar DataFrames y Datasets sobre RDDs son significativas:

    - Optimización del rendimiento: Los DataFrames utilizan un optimizador llamado Catalyst que permite realizar optimizaciones en tiempo de ejecución basadas en el esquema del dato.
    - Seguridad de tipos: Los Datasets ofrecen seguridad de tipos en tiempo de compilación, lo que ayuda a detectar errores antes de ejecutar el código.
    - Interfaz más fácil: La API para DataFrames y Datasets es más intuitiva y permite expresiones más concisas y legibles en comparación con la API RDD.
    - Integración con SQL: Los DataFrames permiten ejecutar consultas SQL directamente, facilitando la interacción con datos estructurados.

6. Trabajando con Datos Estructurados
    Spark SQL proporciona un marco para procesar datos que tienen una estructura definida, lo que permite a los usuarios interactuar con datos de manera más intuitiva y eficiente. Los datos pueden ser almacenados en diferentes formatos estructurados como JSON, Parquet o tablas en Hive. Esto facilita la carga y consulta de datos desde diversas fuentes.

7. Spark SQL
    Spark SQL es un módulo diseñado específicamente para el procesamiento de datos estructurados. A diferencia de la API básica de RDD, Spark SQL utiliza información adicional sobre la estructura de los datos y las operaciones que se realizan. Esta información permite a Spark aplicar optimizaciones adicionales durante el procesamiento. Spark SQL unifica el acceso a datos mediante diferentes APIs, permitiendo a los desarrolladores alternar entre SQL y la API de DataFrame según lo que resulte más natural para la tarea en cuestión.

8. Consultando Datos con Sintaxis SQL
    Una de las características más destacadas de Spark SQL es su capacidad para ejecutar consultas SQL directamente sobre los datos. Los usuarios pueden escribir consultas en un formato familiar y recibir resultados en forma de DataFrames o Datasets. Esto permite a los analistas y científicos de datos utilizar sus conocimientos previos en SQL sin necesidad de aprender una nueva sintaxis. Además, Spark SQL soporta comandos compatibles con ANSI SQL:2003 y HiveQL, lo que amplía aún más su funcionalidad.

9. Integración con Hive
Spark SQL se integra fácilmente con Hive, lo que permite leer y escribir datos en tablas Hive existentes. Esto es especialmente útil para organizaciones que ya utilizan Hive como parte de su infraestructura de Big Data. La integración permite a los usuarios ejecutar consultas sobre datos almacenados en Hive utilizando la misma sintaxis SQL que emplean para otras fuentes de datos, lo que simplifica el flujo de trabajo y mejora la inter-operabilidad entre sistemas.
