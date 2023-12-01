from sklearn.cluster import KMeans
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

# Seleccionar solo las características relevantes para el clustering
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 
            'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'duration_ms']
X = data[features]

# Definir el número de clusters (puedes ajustarlo)
num_clusters = 10

# Entrenar el modelo de k-means
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Agregar las etiquetas de cluster a los datos originales
data['cluster_label'] = kmeans.labels_

# Función para encontrar las canciones más cercanas dentro del mismo cluster
def find_nearest_neighbors_within_cluster(query_track_id, k):
    query_song = data[data['track_id'] == query_track_id]
    query_cluster = int(query_song['cluster_label'])

    cluster_songs = data[data['cluster_label'] == query_cluster]
    cluster_songs = cluster_songs[cluster_songs['track_id'] != query_track_id]

    distances = []
    for index, row in cluster_songs.iterrows():
        song_data = row.to_dict()
        dist = euclidean_distance(query_song.iloc[0], song_data)
        distances.append((song_data['track_id'], song_data['track_name'], song_data['track_artist'], dist))

    distances.sort(key=lambda x: x[3])
    nearest_neighbors = distances[:k]
    return nearest_neighbors

