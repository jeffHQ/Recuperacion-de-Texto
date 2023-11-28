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

# Proyecto 2 Parte 2 - Base d Datos 2
---
## Introducción

En la programación, la implementacion de metodos de busqueda y recuperacion de información basada en el contenido requiere la comprensión de algoritmos eficientes para comparar y evaluar la relevancia del contenido textual. Estos sistemas son fundamentales para aplicaciones como motores de búsqueda, sistemas de recomendación y gestión de documentos. Nuestro proyecto busca lograr crear una implementación que nos permita realizar estas busqueda de la manera mas eficiente posible.

## Objetivos

Nuestro proyecto busca poder realizar la construccion de la forma mas optima del indice invertido para reducir la carga de la busqueda y recuuperacion de informacion n la base de datos. Ademas, de lograr implementar los indices muultidimencionales con los algoritmos de recuperacion basados en el contenido buscando logrando que el usuario pueda obtener los resultados de su busqueda y los mas cercanos a ellos.

## Descripccion del dominio de datos

Nos centramos en desarrollar un algoritmo de búsqueda eficiente utilizando índices invertidos guardados en memoria secundaria para optimizar los costos de tiempo y uso de RAM. Estos índices permiten realizar búsquedas rápidas y precisas en grandes conjuntos de datos como lo pueden ser los datos musicales que incluyen campos relevantes como los artistas, canción, género, playlist, etc.



# Backend


## Índice Invertido
Usamos el método Single-Pass-In-Memory-Index en memoria secundaria para realizar las búsquedas de manera más eficiente. Para el índice hicimos uso de las siguientes características de los documentos:

- Tf: Se obtiene dividiendo el número de veces que un término aparece en un documento por el número total de términos en ese documento.

- Norma:Se calcula como la raíz cuadrada de la suma de los cuadrados de las frecuencias de los términos en cada documento.

- Idf (frecuencia invertida) :Se calcula utilizando la fórmula de logaritmo del número total de documentos dividido por el número de documentos que contienen el término

Para mejorar los resultados usamos la librería ‘ntlk’ para el manejo de stopwords 


````python
for word in unique_words:
            tf = words.count(word) / len(words)
            doc_length += tf ** 2 
            indice[word].append((track_id, tf))


        length[track_id] = math.sqrt(doc_length)


for word, postings in indice.items():
    num_canciones_con_palabra = len(postings)
    idf[word] = math.log(num_canciones / num_canciones_con_palabra)

````

Para el índice invertido en Postgres usamos GIN (Generalized Inverted Index) al vector resultante de las columnas de la tabla 
Hacemos uso de ‘ts_rank’ para medir la similitud entre el vector que se consulta con el resto. De este modo se puede recuperar que los registros son los más similares.

````python
def busqueda_postgres(query, k):
    vector_resultados = []
    ram = 0
    tiempo = 0


    start_time = time.time() * 1000


    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  


    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="")


    cur = conn.cursor()


    consulta = """
        SELECT
            track_id,
            ts_rank(to_tsvector('english', track_name || ' ' || 
                                    track_artist || ' ' || 
                                    lyrics || ' ' || 
                                    track_album_name || ' ' || 
                                    playlist_name || ' ' || 
                                    playlist_genre || ' ' || 
                                    playlist_subgenre || ' ' || 
                                    _language), to_tsquery('english', %s)) AS similitud
        FROM musica 
        WHERE to_tsvector('english', track_name || ' ' || 
                                track_artist || ' ' || 
                                lyrics || ' ' || 
                                track_album_name || ' ' || 
                                playlist_name || ' ' || 
                                playlist_genre || ' ' || 
                                playlist_subgenre || ' ' || 
                                _language) @@ to_tsquery('english', %s)
        ORDER BY similitud DESC LIMIT %s;
    """


    cur.execute(consulta, (query, query, k))

````

### Indice Multidimensional

La extraccion de los vectores caracteristicos se realizaron con diferentes librerias rtree, faiss y sklearn.cluster. 

### KNN search
 Primero cargamos los datos del CSV, posterior a eso, se hace la consulta para asi calcular la distancia eucledianda. Usamos la funcion find_nearest_neighbors() para sacar los K vecinos mas cercanos 

````python
    def find_nearest_neighbors(query_track_id, k):
    # Obtener los datos de la canción de consulta
    query_song = data[data['track_id'] == query_track_id].iloc[0].to_dict()

    distances = []
    for index, row in data.iterrows():
        song_data = row.to_dict()
        if song_data['track_id'] != query_track_id:
            dist = euclidean_distance(query_song, song_data)
            distances.append((song_data['track_id'], song_data['track_name'], song_data['track_artist'], dist))

    # Ordenar las distancias y obtener las K canciones más cercanas
    distances.sort(key=lambda x: x[3])
    nearest_neighbors = distances[:k]
    return nearest_neighbors
````

### Rtree

En el caso del R Tree si requerimos la indexación de los datos basados en su ubicación en el espacio multidimensional. Donde se establece las dimensiones según la cantidad de caracteres que en nuestro caso usamos 12 dimenciones. Seguido, creamos la función find_nearest_neighbors_rtree() y con la query dada hacemos la búsqueda de los K más cercanos. Como en el anterior, calculamos la distancia euclediana y vamos almacenando según las canciones más cercanas. Finalmente, retorna solo las K más parecidas.

````python
def find_nearest_neighbors_rtree(query_track_id, k):
    query_song = data[data['track_id'] == query_track_id].iloc[0]
    query_features = tuple(query_song[['danceability', 'energy', 'key', 'loudness', 'mode',
                                       'speechiness', 'acousticness', 'instrumentalness',
                                       'liveness', 'valence', 'tempo', 'duration_ms']])

    nearest_neighbors = list(idx.nearest(query_features, num_results=k + 1))
    nearest_neighbors.remove(data[data['track_id'] == query_track_id].index[0])

    distances = []
    for neighbor_idx in nearest_neighbors:
        neighbor_song = data.iloc[neighbor_idx]
        dist = euclidean_distance(query_features, tuple(neighbor_song[['danceability', 'energy', 'key', 'loudness', 'mode',
                                                                       'speechiness', 'acousticness', 'instrumentalness',
                                                                       'liveness', 'valence', 'tempo', 'duration_ms']]))
        distances.append((neighbor_song['track_id'], neighbor_song['track_name'], neighbor_song['track_artist'], dist))


    distances.sort(key=lambda x: x[3])
    nearest_neighbors = distances[:k]
    return nearest_neighbors
````

### Faiss 

Esta librería desarrollada por facebook se implementó para la búsqueda eficiente de la similitud por indexación especializado en el trabajo de dimensiones altas como los modelos de aprendizaje profundo. 

![img1](/imagenes/img3.png)
![img1](/imagenes/img1.jpeg)

Para la indexación faiss utiliza un índice espacial aproximado llamado HNSW(Hierarchical Navigable Small World)  que permite mayor velocidad en la búsqueda de vecinos más cercanos. Este divide la estructura jerárquica para así facilitar la búsqueda y ser más eficiente. Este este algoritmo los agrupa en grafo donde cada nodo representa un vector caracteristico del conjunto de datos y las diferestes capas nos muestran los grafos y sus enlaces que se presentan teniendo en la capa superior los enlaces mas largos y en la capa inferior los mas cortos.

![img1](/imagenes/img2.jpeg)

Vamos atravesando las capas para asi poder encontrar el mas cercano a nuestra query hasta llegar a la capa 0 donde se encontraria el vecino mas cercano a la query. 


```` python
# Configuración del índice HNSW
dimension = features.shape[1]
num_clusters = 8
nlist = 10

# Construir el índice
index = faiss.IndexHNSWFlat(dimension, num_clusters)
index.hnsw.efConstruction = 32  # Ajustar el parámetro de construcción según sea necesario
index.hnsw.efSearch = 32  # Ajustar el parámetro de búsqueda según sea necesario
index.train(features)
index.add(features)
````

Al igual que las demás se creo una función find_nearest_neighbors_faiss() para la obtención de los vecinos más cercanos a la consulta.


```` python
def find_nearest_neighbors_faiss(query_track_id, k):
    query_song = data[data['track_id'] == query_track_id].iloc[0]
    query_features = query_song[['danceability', 'energy', 'key', 'loudness', 'mode',
                                'speechiness', 'acousticness', 'instrumentalness',
                                'liveness', 'valence', 'tempo', 'duration_ms']].values.astype('float32')


    _, nearest_neighbors = index.search(query_features.reshape(1, -1), k + 1)


    distances = []
    for neighbor_idx in nearest_neighbors[0][1:]:
        neighbor_song = data.iloc[neighbor_idx]
        dist = np.linalg.norm(query_features - neighbor_song[['danceability', 'energy', 'key', 'loudness', 'mode',
                                                             'speechiness', 'acousticness', 'instrumentalness',
                                                             'liveness', 'valence', 'tempo', 'duration_ms']].values.astype('float32'))
        distances.append((neighbor_song['track_id'], neighbor_song['track_name'], neighbor_song['track_artist'], dist))


    distances.sort(key=lambda x: x[3])
    nearest_neighbors = distances[:k]
    return nearest_neighbors
````


## Experimentos

|  | KNN-search  | Rtree | Faiss|
|--------------|--------------|--------------|--------------|
| N=1000   |     |     |   |
| N=2000    |     |     |    |
| N=4000   |    |     |    |

## Conclusión

Finalmente este proyecto se logro implementar los diferentes metodos de indices multidimencionales los cuales nos han ayudado a comprender que estos enfoques ofrecen una solucion mas eficiente. Al utilizar la representacion vectorial y los calculos de similitud, estos metodos nos ayudan a obtener patrones y relaciones entre los datos logrando facilitar la recuperacion de información. Ademas, verificamos la capacidad de estos metodos con el trabajo de gran cantidad de data y la velocidad de respuesta. En resumen, gracias al proyecto pudimos ver que los metodos de busqueda y recuperación ofrece una solida base de eficacia y precision.           