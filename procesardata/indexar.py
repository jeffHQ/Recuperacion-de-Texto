import pandas as pd
import json
from nltk.corpus import stopwords
from collections import defaultdict
import math
import re

columnas_deseadas = ['track_id', 'track_name', 'track_artist', 'lyrics', 'track_album_name', 'track_album_release_date', 'playlist_name', 'playlist_genre', 'playlist_subgenre', 'language']

df = pd.read_csv('prueba1000.csv')

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
for index, row in df.iterrows():
    count+=1
    print(count)
    track_id = row['track_id']
    track_name = row['track_name']
    track_artist = row['track_artist']
    lyrics = row['lyrics']
    language = row['language']

    if pd.notna(lyrics):
        words = [word for word in letras_pattern.findall(lyrics.lower()) if word.lower() not in stop_words]

        num_canciones += 1

        unique_words = set(words)

        doc_length = 0

        for word in unique_words:
            tf = words.count(word) / len(words)
            doc_length += tf ** 2 
            indice[word].append((track_id, tf))

        length[track_id] = math.sqrt(doc_length)

for word, postings in indice.items():
    num_canciones_con_palabra = len(postings)
    idf[word] = math.log(num_canciones / num_canciones_con_palabra)

with open('indice.json', 'w', encoding='utf-8') as file:
    json.dump(indice, file, ensure_ascii=False, indent=4)

with open('idf.json', 'w', encoding='utf-8') as file:
    json.dump(idf, file, ensure_ascii=False, indent=4)

with open('length.json', 'w', encoding='utf-8') as file:
    json.dump(length, file, ensure_ascii=False, indent=4)
