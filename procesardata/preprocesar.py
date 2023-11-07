import csv

input_file = 'spotify_songs2.csv'
output_file = 'canciones.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as input_csv, open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)

    for row in reader:
        # Elimina las comillas simples de la columna "lyrics"
        row[3] = row[3].replace("'", "")
        writer.writerow(row)

print("Proceso completado. Los datos se han guardado en", output_file)
