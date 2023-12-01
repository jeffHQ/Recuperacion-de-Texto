from rtree import index
import pandas as pd

# Cargar los datos
data = pd.read_csv('songs.csv')

# Crear un índice R-Tree
p = index.Property()
p.dimension = 12  # Establecer la dimensión según la cantidad de características
idx = index.Index(properties=p)
for i, song_data in data.iterrows():
    coordinates = tuple(song_data[['danceability', 'energy', 'key', 'loudness', 'mode', 
                                   'speechiness', 'acousticness', 'instrumentalness', 
                                   'liveness', 'valence', 'tempo', 'duration_ms']])
    idx.insert(i, coordinates)

# Función para calcular la distancia euclidiana entre dos canciones
def euclidean_distance(song1, song2):
    dist = sum((a - b) ** 2 for a, b in zip(song1, song2))
    return dist ** 0.5

# Función para encontrar las canciones más cercanas usando R-Tree
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

