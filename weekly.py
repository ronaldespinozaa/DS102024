import requests

# URL modificada para exportar la hoja como CSV
CSV_URL = r"https://docs.google.com/spreadsheets/d/1jK4QLKzWCaCBoHDBN1LLmsFjDRPTbHJSeR8qSqltL0E/export?format=csv"


# Ruta local para guardar el archivo CSV
CSV_PATH = "datos_google_sheet.csv"

def descargar_google_sheet(csv_url, csv_path):
    try:
        # Realizar la solicitud para descargar el archivo CSV
        response = requests.get(csv_url)
        response.raise_for_status()  # Lanza una excepción si hay un error

        # Guardar los datos como un archivo CSV
        with open(csv_path, "wb") as file:
            file.write(response.content)
        print(f"Archivo guardado exitosamente en: {csv_path}")
    except Exception as e:
        print(f"Error al descargar la hoja: {e}")

# Ejecutar la función
descargar_google_sheet(CSV_URL, CSV_PATH)
