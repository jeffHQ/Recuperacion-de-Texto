import csv

input_file = 'canciones.csv'
output_file = 'canciones2.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as input_csv, open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)

    for row in reader:
        # Asegúrate de que el formato de fecha sea "YYYY-MM-DD"
        if len(row[7]) == 4:  # Verifica si el valor es un año (ej. "1981")
            row[7] = f"{row[7]}-01"

        writer.writerow(row)

print("Proceso completado. Los datos corregidos se han guardado en", output_file)
