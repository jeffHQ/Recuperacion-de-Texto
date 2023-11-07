import psycopg2
import time
import psutil
import os

def busqueda_postgres(query, k):
    vector_resultados = []
    ram = 0
    tiempo = 0

    start_time = time.time() * 1000  # Registra el tiempo de inicio en milisegundos

    # Función para obtener el uso actual de la memoria RAM
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # En megabytes

    # Realiza la conexión
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Magdalena150")

    # Crea un cursor para interactuar con la base de datos
    cur = conn.cursor()

    # Construye la consulta optimizada
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

    # Ejecuta la consulta
    cur.execute(consulta, (query, query, k))

    # Obtiene los resultados
    resultados = cur.fetchall()

    # Cierra el cursor y la conexión
    cur.close()
    conn.close()

    for row in resultados:
        vector_resultados.append({
            "ID": row[0]
        })

    end_time = time.time() * 1000  # Registra el tiempo de finalización en milisegundos
    tiempo = end_time - start_time  # Calcula el tiempo transcurrido en milisegundos
    ram = get_memory_usage()

    return vector_resultados, ram, tiempo