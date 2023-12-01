from flask import Flask, render_template, jsonify, request
import flask_cors
import pandas as pd
import json
import numpy as np
from sklearn.cluster import KMeans
from rtre import find_nearest_neighbors_rtree
from knn_search import find_nearest_neighbors
from pca import find_nearest_neighbors_within_cluster

app = Flask(__name__)
flask_cors.CORS(app)

def obtener_key_cancion(titulo):
    # Cargar los datos del archivo CSV
    df = pd.read_csv("songs.csv")

    # Buscar la canción por su título
    cancion = df[df['track_name'].str.contains(titulo, case=False, na=False)]
    # Verificar si se encontró la canción
    if not cancion.empty:
        # Extraer la letra de la canción
        ids = cancion.iloc[0]['track_id']
        return ids
    else:
        cancion = df[df['lyrics'].str.contains(titulo, case=False, na=False)]
        if not cancion.empty:
            ids = cancion.iloc[0]['track_id']
            return ids
        return "cancion no encontrada"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/knn',methods=['POST'])
def knn():
    key_value = request.form.get('key')
    method = request.form.get('method')
    llave  = obtener_key_cancion(key_value)
    match method:
        case 'knn':       
            response_data = find_nearest_neighbors(llave, 5)
            pass
        case 'pca':
            response_data = find_nearest_neighbors_within_cluster(key_value, 5)
            pass
        case 'rtree':
            response_data = find_nearest_neighbors_rtree(key_value, 5)
    #response_data = [['id1','song1','author1','distance1'],['id2','song2','author2','distance2'],['id3','song3','author3','distance3'],['id4','song4','author4','distance4'],['id5','song5','author5','distance5']]
    # retornar con formato lista de listas
    return jsonify(response_data)

@app.route('/pca',methods=['POST'])
def pca():
    key_value = request.form.get('key')
    method = request.form.get('method')
    llave  = obtener_key_cancion(key_value)
    response_data = find_nearest_neighbors_within_cluster(llave, 5)
    return jsonify(response_data)

@app.route('/rtree',methods=['POST'])
def rtree():
    key_value = request.form.get('key')
    method = request.form.get('method')
    llave  = obtener_key_cancion(key_value)
    response_data = find_nearest_neighbors_within_cluster(llave, 5)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run()  # Ejecuta la aplicación en modo de depuración