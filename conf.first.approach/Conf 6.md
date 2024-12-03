# Lecture 6: Data Ingestion and ETL Processes

- Data Ingestion Challenges
- Dealing with diverse data sources and formats
- ETL vs. ELT
- Differences and use cases
- Ingestion Tools
- Apache Flume (streaming data)
- Apache Sqoop (relational databases to Hadoop)
- Apache Kafka (distributed streaming platform)
- Data Preprocessing Techniques
- Cleaning, normalization, transformation
- Workflow Scheduling
- Automating ETL processes with Apache Oozie or Airflow.

1. Ingestion de Datos
    La ingestión de datos es el proceso mediante el cual se recopilan y trasladan datos desde diversas fuentes hacia un sistema central para su análisis y procesamiento. Aunque este proceso es fundamental para la generación de información valiosa, presenta múltiples desafíos que las organizaciones deben enfrentar.

2. Desafíos de la Ingestión de Datos
    - Diversidad de Fuentes y Formatos: Las organizaciones suelen lidiar con una variedad de fuentes de datos, como bases de datos, APIs, archivos y plataformas en streaming. Cada fuente puede tener un formato diferente, lo que complica la integración de los datos en un solo sistema. Esto requiere herramientas especializadas para manejar esta diversidad.

    - Calidad y Precisión de los Datos: Mantener la calidad de los datos es crucial, ya que los datos pueden ser incompletos o contener errores. La falta de calidad puede afectar negativamente el análisis y la toma de decisiones. Por lo tanto, es esencial implementar procesos robustos de validación y limpieza de datos.

    - Seguridad y Cumplimiento Normativo: La ingestión de datos también plantea preocupaciones sobre la seguridad y la privacidad. Al recopilar datos de múltiples fuentes, aumenta el riesgo de brechas de seguridad. Las organizaciones deben establecer medidas sólidas para proteger los datos y cumplir con las normativas aplicables.

3. ETL vs. ELT
    La forma en que se procesa la ingestión de datos puede clasificarse principalmente en dos enfoques: ETL (Extract, Transform, Load) y ELT (Extract, Load, Transform).

    - ETL implica extraer los datos de las fuentes, transformarlos para cumplir con los requisitos del sistema de destino y luego cargarlos en dicho sistema. Este enfoque es útil cuando se necesita asegurar la calidad y la estructura del dato antes de su carga.

    - ELT, por otro lado, extrae los datos y los carga directamente en el sistema antes de transformarlos. Este método es más adecuado para trabajar con grandes volúmenes de datos no estructurados y permite un acceso más rápido a los datos en su forma original, lo que puede ser ventajoso para ciertas aplicaciones analíticas.

Es esencial para elegir el enfoque correcto entre ETL y ELT. Por ejemplo, si una organización enfrenta problemas significativos con la calidad del dato debido a su diversidad, podría optar por ETL para garantizar que solo se carguen datos limpios y estructurados. En cambio, si se trata de un entorno donde se generan grandes volúmenes de datos en tiempo real, ELT podría ser más apropiado debido a su capacidad para manejar flujos constantes sin una transformación previa.
