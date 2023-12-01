import pandas as pd
import numpy as np
import faiss

# Cargar los datos
data = pd.read_csv('songs.csv')

# Obtener características para construir el índice
features = data[['danceability', 'energy', 'key', 'loudness', 'mode', 
                 'speechiness', 'acousticness', 'instrumentalness', 
                 'liveness', 'valence', 'tempo', 'duration_ms']].values.astype('float32')

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

# Función para encontrar los vecinos más cercanos usando Faiss y HNSW
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

# Definir el track_id de consulta
query_track_id = '0017A6SJgTbfQVU2EtsPNo'

# Encontrar los 5 vecinos más cercanos al track_id de consulta usando Faiss y HNSW
k = 5
nearest = find_nearest_neighbors_faiss(query_track_id, k)

# Crear un DataFrame de Pandas para mostrar los resultados en formato de tabla
results_df = pd.DataFrame(nearest, columns=['Track_ID', 'Track_Name', 'Track_Artist', 'Distance'])
print(results_df[['Track_ID', 'Track_Name', 'Track_Artist']])
