from flask import Flask, request, jsonify
from busqueda_indice import busqueda_indice
from busqueda_partition import busqueda_partition
from busqueda_postgres import busqueda_postgres
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/busqueda', methods=['GET','POST'])
def procesar_texto():
    try:
        data = request.get_json()
        query = data.get('query', '')
        k = data.get('k', 0)
        eleccion = int(data.get('eleccion', 0))

        vector_elementos = []
        ram = 0
        tiempo = 0

        print("query: ", query)
        print("k: ", k)
        print("eleccion: ", eleccion)
        if(eleccion == 0):
            vector_elementos, ram, tiempo = busqueda_indice(query, k)
        elif (eleccion == 1):
            vector_elementos, ram, tiempo = busqueda_partition(query, k) 
        elif (eleccion == 2):
            vector_elementos, ram, tiempo = busqueda_postgres(query, k)  

        # Devuelve la respuesta en formato JSON con 3 valores
        response_data = {
            "vector_elementos": vector_elementos,
            "ram": ram,
            "tiempo": tiempo
        }

        return jsonify(response_data)
    except Exception as e:
        print("error aqui")
        return jsonify({"error": str(e)})




@app.route('/leer_cancion', methods=['GET','POST'])
def leer_cancion():
    try:
        data = request.get_json()
        id = data.get('id')
        # Carga el archivo CSV en un DataFrame
        df = pd.read_csv('prueba18454.csv')
        
        song_data = df[df['track_id'] == id]
        song_data = song_data.to_dict(orient='records')[0]
        track_id = song_data['track_id']
        track_name = song_data['track_name']
        track_artist = song_data['track_artist']
        lyrics = song_data['lyrics']
        track_popularity = song_data['track_popularity']
        track_album_id = song_data['track_album_id']
        track_album_name = song_data['track_album_name']
        track_album_release_date = song_data['track_album_release_date']
        playlist_name = song_data['playlist_name']
        playlist_id = song_data['playlist_id']
        playlist_genre = song_data['playlist_genre']
        playlist_subgenre = song_data['playlist_subgenre']
        danceability = song_data['danceability']
        energy = song_data['energy']
        key = song_data['key']
        loudness = song_data['loudness']
        mode = song_data['mode']
        speechiness = song_data['speechiness']
        acousticness = song_data['acousticness']
        instrumentalness = song_data['instrumentalness']
        liveness = song_data['liveness']
        valence = song_data['valence']
        tempo = song_data['tempo']
        duration_ms = song_data['duration_ms']
        language = song_data['language']


        # Devuelve la respuesta en formato JSON con 3 valores
        response_data = {
            "track_id": track_id,
            "track_name" : track_name,
            "track_artist" : track_artist,
            "lyrics": lyrics,
            "track_popularity": track_popularity,
            "track_album_id": track_album_id,
            "track_album_name": track_album_name,
            "track_album_release_date": track_album_release_date,
            "playlist_name": playlist_name,
            "playlist_id": playlist_id,
            "playlist_genre": playlist_genre,
            "playlist_subgenre": playlist_subgenre,
            "danceability": danceability,
            "energy": energy,
            "key": key,
            "loudness": loudness,
            "mode": mode,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
            "liveness": liveness,
            "valence": valence,
            "tempo": tempo,
            "duration_ms": duration_ms,
            "language": language
        }
        return jsonify(response_data)
    except Exception as e:
        print("error aqui")
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)