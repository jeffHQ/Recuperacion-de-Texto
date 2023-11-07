import psycopg2
import time
import psutil
import os

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

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    for row in resultados:
        vector_resultados.append({
            "ID": row[0]
        })

    end_time = time.time() * 1000 
    tiempo = end_time - start_time 
    ram = get_memory_usage()

    return vector_resultados, ram, tiempo