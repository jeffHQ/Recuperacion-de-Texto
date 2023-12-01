import pandas as pd
import numpy as np

# Cargar los datos
data = pd.read_csv('songs.csv')

# Función para calcular la distancia euclidiana entre dos canciones
def euclidean_distance(song1, song2):
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                'speechiness', 'acousticness', 'instrumentalness', 
                'liveness', 'valence', 'tempo', 'duration_ms']
    dist = np.sqrt(np.sum([(song1[feat] - song2[feat]) ** 2 for feat in features]))
    return dist

# Función para encontrar los K vecinos más cercanos a una canción de consulta
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

# Definir el track_id de consulta
#query_track_id = '0017A6SJgTbfQVU2EtsPNo'

# Encontrar los 5 vecinos más cercanos al track_id de consulta
#k = 5
#nearest = find_nearest_neighbors(query_track_id, k)
#print(nearest)

# Crear un DataFrame de Pandas para mostrar los resultados en formato de tabla
#results_df = pd.DataFrame(nearest, columns=['Track_ID', 'Track_Name', 'Track_Artist', 'Distance'])
#print(results_df[['Track_ID', 'Track_Name', 'Track_Artist']])
