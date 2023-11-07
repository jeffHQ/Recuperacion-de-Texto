import json
import os

# Carpeta donde se guardarán las particiones en archivos JSON
particiones_folder = 'particiones_json'

# Asegurarse de que la carpeta de particiones exista
if not os.path.exists(particiones_folder):
    os.makedirs(particiones_folder)

# Cargar el índice invertido desde el archivo JSON
with open('indice.json', 'r', encoding='utf-8') as file:
    indice_invertido = json.load(file)

# Define una función para guardar una partición en disco en un archivo JSON
def guardar_particion(palabra, documentos):
    particion_path = os.path.join(particiones_folder, f'particion_{palabra}.json')
    particion = {'palabra': palabra, 'documentos': documentos}
    with open(particion_path, 'w', encoding='utf-8') as file:
        json.dump(particion, file, ensure_ascii=False, indent=4)

# Itera a través del índice invertido y guarda cada partición en archivos JSON
cont=0
for palabra, documentos in indice_invertido.items():
    cont+=1
    print(cont)
    guardar_particion(palabra, documentos)

print("Particiones guardadas en disco en archivos JSON.")
