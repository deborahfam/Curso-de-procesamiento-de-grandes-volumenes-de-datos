# Bases de datos NoSQL

En el contexto actual de Big Data, la gestión eficiente de grandes volúmenes de información ha llevado a la adopción de tecnologías que superan las limitaciones de las bases de datos relacionales tradicionales. Aunque estas últimas han sido fundamentales en el desarrollo de sistemas de información durante décadas, su modelo estructurado y rígido presenta desafíos significativos al manejar datos no estructurados o semiestructurados, así como al requerir procesamiento en tiempo real en entornos distribuidos.

En el contexto actual de Big Data, la gestión eficiente de grandes volúmenes de información ha llevado a la adopción de tecnologías que superan las limitaciones de las bases de datos relacionales tradicionales. Aunque estas últimas han sido fundamentales en el desarrollo de sistemas de información durante décadas, su modelo estructurado y rígido presenta desafíos significativos al manejar datos no estructurados o semiestructurados, así como al requerir procesamiento en tiempo real en entornos distribuidos.

## Limitaciones de las bases de datos relacionales

Las bases de datos relacionales, basadas en un esquema fijo y un lenguaje estándar como SQL, presentan varias limitaciones en el contexto de Big Data:

1. **Estructura rígida**: Requieren que los datos se ajusten a un esquema predefinido, lo que dificulta la incorporación de nuevos tipos de datos.
2. **Escalabilidad**: La escalabilidad vertical (aumentar la capacidad del servidor) es costosa y limitada, mientras que NoSQL permite una escalabilidad horizontal más económica.
3. **Rendimiento en tiempo real**: La necesidad de realizar consultas complejas puede afectar el rendimiento, especialmente cuando se manejan grandes volúmenes de información.

Existen varios tipos de bases de datos NoSQL, cada una diseñada para satisfacer diferentes necesidades y casos de uso en el manejo de grandes volúmenes de datos. A continuación se describen los principales tipos:

## Tipos de bases de datos NoSQL

### **1. Bases de datos de clave-valor**
Estas bases de datos almacenan datos como pares de clave y valor. Cada clave es única y se utiliza para acceder a su valor correspondiente, que puede ser un simple dato o una estructura más compleja. Este tipo es ideal para aplicaciones que requieren un acceso rápido a datos y son comúnmente utilizadas en sistemas de caché y gestión de sesiones. Ejemplos incluyen **Redis** y **Amazon DynamoDB**.

### **2. Bases de datos orientadas a documentos**
En este modelo, los datos se almacenan en documentos, típicamente en formatos como JSON o BSON. Cada documento es un conjunto de pares clave-valor que puede contener estructuras anidadas, lo que permite representar relaciones complejas y datos semiestructurados. Este tipo es especialmente útil para aplicaciones web donde los datos pueden variar en estructura. Ejemplos son **MongoDB** y **Couchbase**.

### **3. Bases de datos de columnas anchas**
Las bases de datos orientadas a columnas almacenan datos en tablas, los datos se organizan en familias de columnas, que son grupos de columnas que comparten los mismos atributos. Cada fila de un almacén de datos de columnas anchas se identifica mediante una clave de fila única, y las columnas de esa fila se dividen a su vez en nombres y valores de columna.

A diferencia de las bases de datos relacionales tradicionales, que tienen un número fijo de columnas y tipos de datos, los almacenes de datos de columnas anchas permiten un número variable de columnas y admiten múltiples tipos de datos. Ejemplos incluyen **Apache Cassandra** y **Google Bigtable**.

### **4. Bases de datos basadas en grafos**
Estas están diseñadas para almacenar y consultar datos altamente conectados, representando la información como nodos (entidades) y aristas (relaciones). Este modelo es ideal para aplicaciones que requieren análisis complejos sobre redes sociales, recomendaciones y otros sistemas donde las relaciones son fundamentales. Ejemplos son **Neo4j** y **Amazon Neptune**.

### **5. Bases de datos orientadas a series temporales**
Este tipo se especializa en almacenar datos que cambian con el tiempo, como métricas o eventos cronológicos. Son utilizadas comúnmente en aplicaciones que monitorean sistemas, análisis financiero o IoT. Ejemplos incluyen **InfluxDB** y **TimescaleDB**.

## Bases de datos llave-valor

### Ventajas

- **Alto Rendimiento**: Ideal para aplicaciones con altos requerimientos de velocidad.
- **Escalabilidad Horizontal**: Permite aumentar la capacidad del sistema sin necesidad de hardware costoso.
- **Simplicidad en el Modelo**: Facilita el desarrollo y la integración con otras tecnologías.

### Desventajas

- **Falta de Estructura**: La ausencia de un esquema rígido puede llevar a inconsistencias en los datos si no se gestiona adecuadamente.
- **Limitaciones en Consultas Complejas**: No es adecuado para operaciones que requieren relaciones complejas entre los datos, como las que se manejan en bases de datos relacionales.

### Casos de Uso

1. **Caché**: Utilizadas para almacenar resultados temporales y mejorar el rendimiento.
2. **Gestión de Sesiones**: Perfectas para mantener el estado del usuario en aplicaciones web.
3. **Almacenamiento de Configuraciones**: Se pueden usar para guardar configuraciones dinámicas que cambian con frecuencia.
4. **Aplicaciones en Tiempo Real**: Ideal para sistemas que requieren actualizaciones instantáneas, como redes sociales o juegos online.

## Bases de Datos Basadas en Documentos

Las bases de datos documentales almacenan información en documentos que pueden tener diferentes formatos, como JSON, XML o YAML. A diferencia de las bases de datos relacionales, donde los datos se organizan en tablas con un esquema rígido, las bases de datos documentales permiten una estructura más libre y flexible, lo que facilita la incorporación y modificación de datos.

#### Estructura Básica

- **Documento**: Unidad fundamental que contiene datos y puede incluir múltiples tipos de información.
- **Colección**: Agrupación de documentos que permite organizar la información de manera lógica, similar a una tabla en bases relacionales.

### Ventajas

- **Almacenamiento Semiestructurado**: Permiten gestionar datos que no se ajustan a un formato rígido.
- **Actualizaciones Simples**: Facilitan la adición o modificación de información sin necesidad de alterar todo el esquema.
- **Rápida Escritura**: Priorizan la disponibilidad durante operaciones críticas, lo que mejora la eficiencia incluso en situaciones adversas.

### Desventajas

- **Complejidad en Datos Relacionados**: Manejar relaciones complejas entre documentos puede ser complicado y menos eficiente que en bases relacionales.
- **Inconsistencias Potenciales**: La flexibilidad puede llevar a inconsistencias si no se gestionan adecuadamente los documentos.

### Casos de Uso

1. **Gestión de Contenido**: Ideal para aplicaciones como blogs o sistemas CMS donde los tipos de contenido pueden variar.
2. **Aplicaciones Web**: Utilizadas para almacenar información dinámica que cambia con frecuencia, como perfiles de usuario o configuraciones.
3. **Catálogos y E-commerce**: Perfectas para almacenar productos con diferentes atributos y características.
4. **Datos Semiestructurados**: Adecuadas para almacenar información como correos electrónicos o publicaciones en redes sociales.

### Ejemplo Práctico

Un ejemplo típico sería almacenar información sobre un producto en un formato JSON:

```json
{
  "id": "12345",
  "nombre": "Camiseta",
  "color": "Rojo",
  "tamaño": ["S", "M", "L"],
  "precio": 19.99,
  "disponible": true
}
```

## Escalabilidad

La flexibilidad inherente a los sistemas NoSQL proporciona una escalabilidad superior en comparación con los enfoques relacionales tradicionales. Esta ventaja es especialmente evidente en las bases de datos diseñadas para entornos distribuidos. En estos sistemas, la capacidad de añadir nodos adicionales permite no solo gestionar un mayor volumen de datos, sino también optimizar el rendimiento general del sistema.

## Teorema CAP
El **teorema CAP**, también conocido como **teorema de Brewer**, es un principio fundamental en el campo de los sistemas distribuidos, especialmente relevante para Big Data. Postula que un almacén de datos distribuido sólo puede garantizar simultáneamente dos de las tres propiedades siguientes: **Consistencia**, **Disponibilidad**(Availability) y **Tolerancia a la partición**(Partition Tolerance).

### Conceptos clave

#### 1. **Consistencia**
En el contexto del teorema CAP, la consistencia significa que cada operación de lectura recibe la escritura más reciente o un error. Esto garantiza que todos los nodos de una base de datos distribuida reflejen los mismos datos en cualquier momento. Si un usuario consulta la base de datos, debe recibir los datos más recientes, lo que garantiza que todos los nodos están sincronizados.

#### 2. **Disponibilidad**
La disponibilidad garantiza que cada solicitud recibida por un nodo que no falle dé lugar a una respuesta, independientemente de si se trata de los datos más recientes. Esto significa que aunque algunos nodos no estén actualizados por problemas de red, el sistema seguirá respondiendo a las consultas proporcionando los datos que estén accesibles en ese momento.

#### 3. **Tolerancia a Particiones**
La tolerancia a las particiones es la capacidad de un sistema distribuido de seguir funcionando a pesar de particiones arbitrarias de la red (por ejemplo, fallos de comunicación entre nodos). Dado que los fallos de red son inevitables en los sistemas distribuidos, la tolerancia a las particiones se considera una propiedad necesaria.

### Compromisos en los sistemas distribuidos

Según el teorema CAP, cuando se produce una partición de la red, los diseñadores de sistemas deben elegir entre consistencia y disponibilidad:

- **Elegir consistencia**: El sistema puede negarse a procesar peticiones hasta que pueda garantizar que todos los nodos disponen de los datos más recientes, lo que puede provocar tiempos de inactividad o falta de respuesta durante las particiones.
  
- **Elegir disponibilidad**: El sistema responderá a las solicitudes con los datos que estén disponibles, incluso si esto significa devolver datos obsoletos o incoherentes.

De esta manera los sistemas distribuidos pueden clasificarse en dos grupos:

- **Sistemas CP (Consistencia y Tolerancia a la Partición)**: Estos sistemas priorizan la consistencia sobre la disponibilidad durante las particiones. Algunos ejemplos son las bases de datos relacionales tradicionales como PostgreSQL.
  
- **Sistemas AP (Disponibilidad y tolerancia a particiones)**: Estos sistemas favorecen la disponibilidad sobre la consistencia estricta, permitiendo la consistencia eventual. Ejemplos incluyen bases de datos NoSQL como Cassandra y MongoDB.