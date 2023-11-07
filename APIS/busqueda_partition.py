import json
import math
import os
import time
import psutil

def busqueda_partition(query, k):
    vector_resultados = []
    ram = 0
    tiempo = 0


    start_time = time.time() * 1000  # Registra el tiempo de inicio en milisegundos

    # Función para obtener el uso actual de la memoria RAM
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # En megabytes

    # Cargar el índice IDF desde el archivo JSON en memoria secundaria
    with open('idf.json', 'r', encoding='utf-8') as file:
        idf = json.load(file)

    # Carpeta donde se guardaron las particiones
    particiones_folder = 'particiones_json'

    # Define una función para buscar documentos que contienen una palabra específica en las particiones
    def buscar_palabra_en_particion(palabra):
        try:
            with open(os.path.join(particiones_folder, f'particion_{palabra}.json'), 'r', encoding='utf-8') as file:
                particion = json.load(file)
                return particion['documentos']
        except FileNotFoundError:
            return []  # La partición no existe

    # Define una función para realizar la búsqueda de documentos que contienen todas las palabras de la consulta
    def buscar_documentos(consulta, k):
        palabras_consulta = consulta.split()
        documentos_coincidentes = {}  # Un diccionario para rastrear el puntaje de cada documento
        for palabra in palabras_consulta:
            # Verificar si la palabra está en el índice IDF
            if palabra in idf:
                documentos = buscar_palabra_en_particion(palabra)
                for doc_id, tf in documentos:
                    # Calcula el puntaje para el documento usando TF-IDF
                    puntaje = tf * idf[palabra]
                    if doc_id in documentos_coincidentes:
                        documentos_coincidentes[doc_id] += puntaje
                    else:
                        documentos_coincidentes[doc_id] = puntaje

        # Ordena los documentos por puntaje en orden descendente
        documentos_ordenados = sorted(documentos_coincidentes.items(), key=lambda x: x[1], reverse=True)

        # Retorna los documentos con los puntajes más altos
        return documentos_ordenados[:k]

    # Ejemplo de búsqueda
    vector_resultados = buscar_documentos(query, k)
    vector_resultados = [{'ID': item[0]} for item in vector_resultados]

    # Obtiene el uso de la memoria RAM al final de la ejecución
    ram = get_memory_usage()
    end_time = time.time() * 1000  # Registra el tiempo de finalización en milisegundos
    tiempo = end_time - start_time  # Calcula el tiempo transcurrido en milisegundos


    return vector_resultados, ram, tiempo


