import pandas as pd
import json
from nltk.corpus import stopwords
from collections import defaultdict
import math
import re

# Definir las columnas deseadas
columnas_deseadas = ['track_id', 'track_name', 'track_artist', 'lyrics', 'track_album_name', 'track_album_release_date', 'playlist_name', 'playlist_genre', 'playlist_subgenre', 'language']

# Cargar el archivo CSV
df = pd.read_csv('prueba1000.csv')

# Crear un conjunto de stopwords en español
stop_words = set(stopwords.words('spanish'))

# Crear un diccionario para almacenar el índice invertido
indice = defaultdict(list)

# Crear un diccionario para almacenar el IDF de cada palabra
idf = {}

# Crear un diccionario para almacenar la longitud de cada documento (norma)
length = {}

# Contador para rastrear la cantidad total de documentos (canciones)
num_canciones = 0

# Expresión regular para filtrar palabras que contienen letras
letras_pattern = re.compile(r'\w+')
count = 0
# Iterar a través de las filas del DataFrame
for index, row in df.iterrows():
    count+=1
    print(count)
    # Recopilar la información relevante
    track_id = row['track_id']
    track_name = row['track_name']
    track_artist = row['track_artist']
    lyrics = row['lyrics']
    language = row['language']

    # Verificar si 'lyrics' es un valor nulo (NaN)
    if pd.notna(lyrics):
        # Utilizar expresión regular para encontrar palabras que contienen letras
        words = [word for word in letras_pattern.findall(lyrics.lower()) if word.lower() not in stop_words]

        # Incrementar el contador de canciones
        num_canciones += 1

        # Crear un conjunto para rastrear las palabras únicas en esta canción
        unique_words = set(words)

        # Calcular la longitud de este documento (norma)
        doc_length = 0

        # Calcular el peso TF de cada palabra y guardar en el índice
        for word in unique_words:
            tf = words.count(word) / len(words)
            doc_length += tf ** 2  # Sumar el cuadrado del TF para la norma
            indice[word].append((track_id, tf))

        # Calcular la longitud de este documento (norma)
        length[track_id] = math.sqrt(doc_length)

# Calcular el IDF para cada palabra
for word, postings in indice.items():
    num_canciones_con_palabra = len(postings)
    idf[word] = math.log(num_canciones / num_canciones_con_palabra)

# Guardar el índice, IDF y la longitud de documentos en archivos JSON
with open('indice.json', 'w', encoding='utf-8') as file:
    json.dump(indice, file, ensure_ascii=False, indent=4)

with open('idf.json', 'w', encoding='utf-8') as file:
    json.dump(idf, file, ensure_ascii=False, indent=4)

with open('length.json', 'w', encoding='utf-8') as file:
    json.dump(length, file, ensure_ascii=False, indent=4)
