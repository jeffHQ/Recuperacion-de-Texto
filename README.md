![Texto Alternativo](/imagenes/logo.jpg)

<h1 align="center">Motor de Búsqueda por Indexación Invertida</h1>

# Proyecto
Realizamos un motor de búsqueda utilizando un indice invertido guardado en memoria secundaria para optimizar los costos de tiempo y RAM.

# Carpetas
Este proyecto está dividido en 3 carpetas:
## 1. /APIS
Esta carpeta contiene las API's y las funciones de la aplicación (Backend). Aqui podemos encontrar 3 funciones principales:
### Busqueda_indice.py
Esta función carga todo el indice a RAM (.json) y realiza una busqueda por clave y nos devuelve la coleccion de (palabra{id_musica, peso}) paraluego iterarlo y junto con el idf hallar el top k documentos mas similares.

<h4 align="center">Metodo de indexación</h4>
Para este proyecto, se uso el metodo de indexación Single-Pass-In-Memory-Index para un Indice invertido, donde se usaron fórmulas matematicas para lograrlo:

![Alt text](/imagenes/singlepass.png)

* Norma = sqrt(sum(frecuencia^2 de todos los términos en el documento))
* TF = (Número de veces que el término aparece en el documento) / (Número total de términos en el documento)
* IDF = log(Número total de documentos / Número de documentos que contienen el término)

![Texto Alternativo](/imagenes/indice.jpg)
**Indice de la forma: {"palabra": [musica_id, tf]}**
![Texto Alternativo](/imagenes/idf.jpg)
**IDF de la forma: {"palabra": idf}**
![Texto Alternativo](/imagenes/length.jpg)
**Norma de la forma: {"musica_id": norma}**

### Busqueda_partition.py
* Esta funcion es la misma que la de "busqueda_indice.py", solo que realiza la busqueda del indice en la carpeta "/particiones_json" donde buscara el indice de la respectiva palabra a consultar y lo cargará a la RAM (Así evitamos cargar todo el indice a la RAM).
![Alt text](/imagenes/partition.png)

### Busqueda_postgres
Esta es una busqueda implementada en postgres. Para optimizar la consulta se convirtieron las columnas de la tabla a vectores de texto. Esto nos permite realizar busquedas de texto completo en todos los datos (Sin la necesidad de utilizar %ILIKE%).

1. Primero, debemos recordar que la complejidad de %ILIKE% es O(n), por lo que realizarla en grandes conjuntos de datos puede ser muy pesado:
![Texto Alternativo](/imagenes/ilike.jpg)Tiempo de ejecución de 2 segundos.

2. Por lo que, para esta clase de consultas se utiliza un GIN especial basado en vectores
![Texto Alternativo](/imagenes/gin.jpg)
GIN está diseñado para acelerar las consultas que buscan elementos específicos dentro de conjuntos (arrays) o estructuras complejas de datos. Permite buscar en conjuntos de datos sin necesidad de recorrer todas las filas de una tabla.

3. La consulta utiliza la función to_tsvector para convertir varias columnas de la tabla "musica" en vectores de texto
![GA](/imagenes/query_vector.jpg)
La consulta busca registros en la tabla "musica" donde la similitud calculada sea mayor que cero, lo que significa que coincide con el término de búsqueda proporcionado.

Este tipo de consulta se utiliza comúnmente en aplicaciones de búsqueda de texto completo, donde se busca la similitud entre los datos almacenados y una consulta de búsqueda dada. La consulta busca resultados que sean más relevantes en función de la similitud con el término de búsqueda.

## 2. /Frontend
Aqui se guarda la GUI de la aplicación, un servicio web construido con Vue.js

## 3. /ProcesarData
En esta carpeta están:

1. Codigos de procesamiento del dataset de Kaggle.com, este dataset funciona bien para Python, pero al momento de subirlo a una tabla en Postgres devuelve errores los cuales se arreglan procesando los archivos .csv

2. Códigos de indexación y particionamiento de los datos en memoria secundaria.


3. Dataset inicial y datasets procesador de 1000, 2000, 4000, 8000 y 18454 filas.

# Experimentación

Primero realizamos una comparación de tiempo usando los 3 indices correspondientes, luego hicimos pruebas de uso de RAM:
* Indice invertido completo a RAM
* Indice partido a RAM
* PostgreSQL

## 1. Tiempo de ejecución

![Texto Alternativo](/imagenes/comp1.jpg)

Al realizarlo nos dimos cuenta que el tiempo en consulta era muy disparejo y a medida que el número de documentos subia el tiempo de ejecución subia aún mas, por lo que decidimos realizar otra gráfica.

![Texto Alternativo](/imagenes/comp2.jpg)

En esta nueva gráfica comparamos Indice Partido vs PostgreSQL, donde podemos apreciar que el tiempo de ejecución de nuestra implementación de Indice partido resulta mejor en tiempos de ejecución.

## 2. Uso de RAM


![Texto Alternativo](/imagenes/comp3.jpg)

Para esta experimentación podemos apreciar que el uso de RAM por parte del Indice Invertido Completo usa una mayor cantidad de recursos al cargar todo el indice a la RAM, cosa que no pasa con el Indice Partido, que busca el (.json) respectivo para cada palabra de cada consulta, por lo que utiliza menos recursos.

# Conclusiones:

No me pagan lo suficiente