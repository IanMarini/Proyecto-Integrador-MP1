import os

# Define la ruta de tu base de datos
RUTA_DB2 = "C:/Users/marin/OneDrive/Desktop/ProyectoFinal/App/mi_base_de_datos.db"

# Verifica si la base de datos existe
if not os.path.exists(RUTA_DB2):
    print(f"El archivo de base de datos no existe en la ruta: {RUTA_DB2}")
else:
    print("La base de datos existe.")