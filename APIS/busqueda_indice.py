import json
import math
import time
import psutil
import os

def busqueda_indice(query, k):
    vector_resultados = []
    ram = 0
    tiempo = 0

    start_time = time.time() * 1000

    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    with open('indice.json', 'r', encoding='utf-8') as file:
        indice_invertido = json.load(file)

    with open('idf.json', 'r', encoding='utf-8') as file:
        idf = json.load(file)

    def buscar_documentos(consulta, k):
        palabras_consulta = consulta.split()
        documentos_coincidentes = {}
        for palabra in palabras_consulta:
            if palabra in idf:
                documentos = indice_invertido.get(palabra, [])
                for doc_id, tf in documentos:
                    puntaje = tf * idf[palabra]
                    if doc_id in documentos_coincidentes:
                        documentos_coincidentes[doc_id] += puntaje
                    else:
                        documentos_coincidentes[doc_id] = puntaje

        documentos_ordenados = sorted(documentos_coincidentes.items(), key=lambda x: x[1], reverse=True)

        return documentos_ordenados[:k]

    vector_resultados = buscar_documentos(query, k)
    vector_resultados = [{'ID': item[0]} for item in vector_resultados]


    end_time = time.time() * 1000
    tiempo = end_time - start_time
    ram = get_memory_usage()

    return vector_resultados, ram, tiempo


