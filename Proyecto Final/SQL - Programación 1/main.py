# --------------------------------------------------------------------------------------------------------------- 
# LIBRERIA
# --------------------------------------------------------------------------------------------------------------- 
import re
import random
import pickle
import os
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

# --------------------------------------------------------------------------------------------------------------- 
# RUTA DE ARCHIVOS
# --------------------------------------------------------------------------------------------------------------- 
RUTA_DB2 = 'C:/Users/marin/OneDrive/Desktop/Evidencia_1/App/mi_base_de_datos.db'
RUTA_CARPETA = r"C:\Users\marin\OneDrive\Desktop\Evidencia_1\App"
RUTA_USUARIOS = os.path.join(RUTA_CARPETA, "usuarios.ispc")
RUTA_ACCESOS = os.path.join(RUTA_CARPETA, "accesos.isps")
RUTA_LOG = os.path.join(RUTA_CARPETA, "logs.txt")
RUTA_DB = os.path.join(RUTA_CARPETA, "registros_pluviales.db")  # Base de datos para registros pluviales

# --------------------------------------------------------------------------------------------------------------- 
# CLASES DE USUARIOS
# --------------------------------------------------------------------------------------------------------------- 
class Usuario:
    def __init__(self, id, nombre, apellido, dni, usuario, clave, correo, fecha_nacimiento):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.usuario = usuario
        self.clave = clave
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre} {self.apellido}, Usuario: {self.usuario}, DNI: {self.dni}"

class Acceso:
    def __init__(self, id, usuarioLogueado):
        self.id = id
        self.fechaIngreso = datetime.now()
        self.fechaSalida = None
        self.usuarioLogueado = usuarioLogueado

    def cerrar_sesion(self):
        self.fechaSalida = datetime.now()

    def __str__(self):
        return (f"Acceso ID: {self.id}, Usuario: {self.usuarioLogueado.usuario}, "
                f"Fecha Ingreso: {self.fechaIngreso}, Fecha Salida: {self.fechaSalida}")

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONES PARA MANEJAR ARCHIVOS BINARIOS
# --------------------------------------------------------------------------------------------------------------- 
def guardar_usuarios(usuarios):
    with open(RUTA_USUARIOS, "wb") as file:
        pickle.dump(usuarios, file)

def cargar_usuarios():
    try:
        with open(RUTA_USUARIOS, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def guardar_accesos(accesos):
    with open(RUTA_ACCESOS, "wb") as file:
        pickle.dump(accesos, file)

def cargar_accesos():
    try:
        with open(RUTA_ACCESOS, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def registrar_log_fallido(usuario, clave):
    with open(RUTA_LOG, "a") as log:
        log.write(f"Intento fallido de acceso: {usuario}, {clave} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONES DE REGISTROS PLUVIALES
# --------------------------------------------------------------------------------------------------------------- 
def crear_db():
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS precipitaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mes TEXT,
        cantidad REAL
    )''')
    conn.commit()
    conn.close()

def agregar_registro_pluvial(mes, cantidad):
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO precipitaciones (mes, cantidad) VALUES (?, ?)", (mes, cantidad))
    conn.commit()
    conn.close()

def obtener_registros_pluviales():
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT mes, cantidad FROM precipitaciones")
    registros = cursor.fetchall()
    conn.close()
    return registros
def graficar_barras_lluvias_anuales():
    registros = obtener_registros_pluviales()
    if registros:
        meses, cantidades = zip(*registros)
        
        plt.figure(figsize=(10, 6))
        plt.bar(meses, cantidades, color='skyblue')
        plt.xlabel('Meses')
        plt.ylabel('Cantidad de precipitaciones (mm)')
        plt.title('Registros pluviales del año')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    elif opcion == "4":
        analizar_mes_precipitacion()  # Llamada a la función para análisis de precipitación mensual
    
# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONES DE LOS GRÁFICOS
# --------------------------------------------------------------------------------------------------------------- 
def graficar_dispersion():
    registros = obtener_registros_pluviales()
    if registros:
        meses, dias, cantidades = [], [], []

        for mes, cantidad in registros:
            # Simular una cantidad de lluvia para cada día, centrada alrededor de cantidad
            # Se asume que cada mes tiene 30 días para simplificar (puedes ajustarlo según el mes)
            for dia in range(1, 31):
                # Generar una variación aleatoria alrededor de la cantidad mensual
                cantidad_diaria = max(0, np.random.normal(cantidad, cantidad * 0.1))  # 10% variación
                meses.append(mes)
                dias.append(dia)
                cantidades.append(cantidad_diaria)

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(meses, dias, c=cantidades, cmap='Blues', alpha=0.7)
        plt.colorbar(scatter, label='Cantidad de Lluvia')
        plt.xlabel('Meses')
        plt.ylabel('Días')
        plt.title('Dispersión de Lluvias por Mes y Día')
        plt.xticks(rotation=45)
        plt.show()

def graficar_pie_lluvias(): 
    registros = obtener_registros_pluviales()
    if registros:
        meses, cantidades = zip(*registros)
        
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=meses, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
        plt.title('Distribución de Lluvias Anuales por Mes')
        plt.show()

def analizar_mes_precipitacion():
    año = input("Ingrese el año para el que desea analizar las precipitaciones (por ejemplo, 2023): ").strip()
    archivo_csv = f"registroPluvial{año}.csv"
    
    # Verificar si el archivo CSV existe
    if not os.path.exists(archivo_csv):
        print(f"No se encontró el archivo para el año {año}.")
        return
    
    # Cargar el archivo CSV
    df = pd.read_csv(archivo_csv)
    print("Meses disponibles:", ", ".join(df.columns))  # Mostrar los meses disponibles
    
    # Selección del mes
    mes = input("Ingrese el mes que desea analizar (por ejemplo, Enero): ").strip()
    if mes not in df.columns:
        print("Mes no encontrado en el archivo.")
        return

    # Extraer y mostrar los datos del mes seleccionado
    datos_mes = df[mes].dropna()  # Eliminamos valores NaN si los hay
    
    if datos_mes.empty:
        print(f"No hay datos de precipitación para {mes} en el año {año}.")
        return

    # Calcular máxima, mínima y promedio de precipitación
    max_precip = np.max(datos_mes)
    min_precip = np.min(datos_mes)
    avg_precip = np.mean(datos_mes)

    print(f"\nAnálisis de precipitaciones para {mes} {año}:")
    print(f"Registros diarios:\n{datos_mes}")
    print(f"Máxima precipitación: {max_precip} mm")
    print(f"Mínima precipitación: {min_precip} mm")
    print(f"Promedio de precipitación: {avg_precip:.2f} mm")

    # Generar gráfico circular con Matplotlib
    plt.figure(figsize=(8, 8))
    plt.pie(datos_mes, labels=[f"Día {i+1}" for i in range(len(datos_mes))],
            autopct='%1.1f%%', startangle=140)
    plt.title(f"Distribución de precipitaciones para {mes} {año}")
    plt.show()
    
# --------------------------------------------------------------------------------------------------------------- 
# MY SQL CONEXIÓN
# --------------------------------------------------------------------------------------------------------------- 
default_values = {
    "host": "localhost",
    "user": "root",
    "password": "4466",
    "database": "d_BaseDatos_Fidelizacion_ISPC"
}

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host=default_values["host"],
            user=default_values["user"],
            password=default_values["password"],
            database=default_values["database"]
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def conectar_db(database=None, user=None, password=None, host=None):
    print("Intentando conectar a la base de datos...")
    
    creds = {
        "host": host or default_values["host"],
        "user": user or default_values["user"],
        "password": password or default_values["password"],
        "database": database or default_values["database"]
    }
    
    print(f"Credenciales: {creds}")  # Verifica si las credenciales están correctas
    
    try:
        # Conectar al servidor sin especificar la base de datos
        print("Conectando al servidor MySQL...")
        conn = mysql.connector.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"]
        )
        print("Conexión inicial exitosa, intentando crear la base de datos...")  # Mensaje de prueba
        
        cursor = conn.cursor()
        print("Cursor creado, ejecutando creación de base de datos...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{creds['database']}`")  # Escapa el nombre de la base de datos
        cursor.execute(f"USE `{creds['database']}`")
        print(f"Base de datos '{creds['database']}' creada o ya existente, usando base de datos.")
        
        cursor.close()
        conn.close()

        # Ahora conectamos a la base de datos que ya fue creada (o ya existía)
        print("Intentando reconectar a la base de datos...")
        conn = mysql.connector.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["database"]
        )
        print(f"Conexión exitosa a la base de datos '{creds['database']}'")
        return conn  # Devuelve la conexión y las credenciales usadas
    
    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return None

# --------------------------------------------------------------------------------------------------------------- 
# FUNCION CREAR TABLA MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def crear_tabla_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conn.cursor()
    print("=== Crear Tabla en la Base de Datos ===")
    
    # Solicitar el nombre de la tabla
    nombre_tabla = input("Ingresa el nombre de la tabla: ").strip()
    
    # Verifica si la tabla ya existe
    try:
        cursor.execute("SHOW TABLES;")
        tablas = [tabla[0] for tabla in cursor.fetchall()]  # Obtener solo los nombres de las tablas
        if nombre_tabla in tablas:
            print("La tabla ya existe.")
            conn.close()  # Cierra la conexión antes de salir
            return
    except mysql.connector.Error as e:
        print(f"Error al verificar las tablas: {e}")
        conn.close()
        return

    # Mostrar instrucciones para las columnas
    print("Ingrese las columnas en el siguiente formato:")
    print("nombre_columna1 tipo_columna1 restricciones, nombre_columna2 tipo_columna2 restricciones")
    print("Ejemplo: nombre VARCHAR(255) PRIMARY KEY, edad INT NOT NULL, comuna VARCHAR(100) DEFAULT 'Desconocida'")
    
    columnas = input("\nIngrese las columnas separadas por comas: ").strip()
    
    # Validar que se hayan ingresado columnas
    if not columnas:
        print("Error: Debe proporcionar al menos una columna.")
        conn.close()
        return

    # Limpiar entradas de columnas y validar que no haya nombres duplicados
    columnas_lista = [col.strip() for col in columnas.split(',')]  # Dividir y limpiar espacios
    columnas_sin_duplicados = list(dict.fromkeys(columnas_lista))  # Eliminar duplicados mientras se conserva el orden
    
    if len(columnas_lista) != len(columnas_sin_duplicados):
        print("Error: Hay nombres de columna duplicados.")
        conn.close()
        return
    
    columnas = ', '.join(columnas_sin_duplicados)  # Volver a unir en una cadena

    # Crear la tabla con IF NOT EXISTS
    query = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({columnas});"
    
    try:
        print(f"Consulta SQL generada: {query}")  # Imprimir la consulta SQL generada
        cursor.execute(query)
        conn.commit()  # Guarda los cambios en la base de datos
        print(f"Tabla '{nombre_tabla}' creada exitosamente.")
    except mysql.connector.Error as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        conn.close()  # Cierra la conexión
    
# --------------------------------------------------------------------------------------------------------------- 
# FUNCION ELIMINAR TABLA MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def eliminar_tabla_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conn.cursor()
    print("=== Eliminar Tabla en la Base de Datos ===")
    
    # Obtener nombres de tablas
    try:
        cursor.execute("SHOW TABLES;")
        tablas = [tabla[0] for tabla in cursor.fetchall()]  # Obtener solo los nombres de las tablas
    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")
        conn.close()  # Cerrar conexión antes de salir
        return

    # Si no hay tablas
    if not tablas:
        print("No hay tablas para eliminar.")
        conn.close()  # Cerrar la conexión antes de salir
        return
    
    # Mostrar tablas disponibles
    print("Tablas disponibles:")
    for tabla in tablas:
        print(tabla)

    # Pedir nombre de tabla a eliminar
    nombre_tabla = input("Ingresa el nombre de la tabla a eliminar: ").strip()
    
    # Verificar si la tabla existe
    if nombre_tabla not in tablas:
        print("La tabla no existe.")
    else:
        try:
            cursor.execute(f"DROP TABLE {nombre_tabla};")
            conn.commit()  # Guardar cambios
            print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
        except mysql.connector.Error as e:
            print(f"Error al eliminar la tabla: {e}")

    conn.close()  # Cerrar conexión

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONE AGREGAR DATOS MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def agregar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conn.cursor()
    print("=== Agregar Datos a la Tabla en la Base de Datos ===")
    
    # Obtener nombres de tablas
    try:
        cursor.execute("SHOW TABLES;")
        tablas = [tabla[0] for tabla in cursor.fetchall()]  # Obtener solo los nombres de las tablas
    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")
        conn.close()  # Cerrar conexión antes de salir
        return

    if not tablas:
        print("No hay tablas para agregar datos.")
        conn.close()  # Cerrar la conexión antes de salir
        return
    
    # Mostrar tablas disponibles
    print("Tablas disponibles:")
    for tabla in tablas:
        print(tabla)

    # Pedir nombre de tabla
    nombre_tabla = input("Ingresa el nombre de la tabla: ").strip()
    if nombre_tabla not in tablas:
        print("La tabla no existe.")
        conn.close()  # Cierra la conexión antes de salir
        return

    # Obtener información de columnas
    try:
        cursor.execute(f"DESCRIBE {nombre_tabla};")
        columnas = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al obtener las columnas: {e}")
        conn.close()  # Cerrar conexión antes de salir
        return

    print("Columnas disponibles:")
    for col in columnas:
        print(f"{col[0]} ({col[1]})")  # Muestra el nombre de la columna y su tipo

    # Crea una lista para los nombres de las columnas
    nombres_columnas = [col[0] for col in columnas]

    # Solicita al usuario cuántas filas desea agregar
    try:
        num_filas = int(input("¿Cuántas filas desea agregar?: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
        conn.close()  # Cierra la conexión antes de salir
        return

    for _ in range(num_filas):
        valores = []
        # Recorre cada columna y pide el dato correspondiente
        for columna in nombres_columnas:
            dato = input(f"Ingrese dato para '{columna}' (deje vacío para NULL): ")           
            dato = dato.strip()  # Elimina espacios al principio y al final
            # Si se deja vacío, se inserta None (que representa NULL en MySQL)
            if dato == "":
                valores.append(None)  # Agrega un valor nulo
            else:
                valores.append(dato)  # Agrega el dato ingresado
        
        # Crea la consulta para insertar los datos
        placeholders = ', '.join(['%s'] * len(valores))  # Crea placeholders para la consulta
        query = f"INSERT INTO {nombre_tabla} ({', '.join(nombres_columnas)}) VALUES ({placeholders});"      
        
        try:
            cursor.execute(query, valores)  # Inserta los valores en la tabla
            print(f"Datos agregados a la tabla {nombre_tabla} correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al insertar los datos: {e}")

    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()   # Cierra la conexión

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONE VIZUALIZAR DATOS MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def visualizar_mysql():
    # Conectar a la base de datos (usa credenciales por defecto)
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    print("Conexión exitosa a la base de datos.")  # Mensaje para verificar si llega aquí
    cursor = conn.cursor()
    # Obtener tablas
    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()
    if not tablas:
        print("No hay tablas en la base de datos.")
        conn.close()
        return
    # Crear un DataFrame para mostrar todas las tablas y sus columnas
    all_tables_info = []
    for tabla in tablas:
        nombre_tabla = tabla[0]
        cursor.execute(f"DESCRIBE {nombre_tabla};")  # Comando para describir las columnas en MySQL
        columnas_info = cursor.fetchall()
        for col in columnas_info:
            all_tables_info.append({
                'Tabla': nombre_tabla,
                'Columna': col[0],  # Nombre de la columna
                'Tipo': col[1],     # Tipo de dato
                'Restricciones': col[2] if col[2] else 'Ninguna'  # MySQL no tiene la misma estructura, así que adaptamos
            })
    # Mostrar todas las tablas y columnas
    df_tablas = pd.DataFrame(all_tables_info)
    print("Estructura de la base de datos:")
    print(df_tablas)
    while True:
        nombre_tabla = input("Ingresa el nombre de la tabla a visualizar (o deja vacío para salir): ").strip()
        if nombre_tabla == '':
            conn.close()
            return
        if (nombre_tabla,) not in tablas:
            print("La tabla no existe. Intente de nuevo.")
            continue
        # Obtener información sobre las columnas
        cursor.execute(f"DESCRIBE {nombre_tabla};")
        columnas_info = cursor.fetchall()
        columnas = [col[0] for col in columnas_info]  # Obtener solo los nombres de las columnas
        tipos = [col[1] for col in columnas_info]     # Obtener tipos de columnas
        print(f"Columnas en la tabla '{nombre_tabla}':")
        for col, tipo in zip(columnas, tipos):
            print(f"{col} ({tipo})")
        # Selección de columnas a visualizar
        columnas_a_visualizar = input("Ingrese las columnas que desea visualizar (separadas por comas) o deje vacío para todas: ")
        if columnas_a_visualizar.strip() == "":
            columnas_a_visualizar = columnas  # Mostrar todas las columnas si no se especifica
        else:
            columnas_a_visualizar = [col.strip() for col in columnas_a_visualizar.split(',')]
        # Selección de filas a visualizar
        while True:
            try:
                n = input("¿Cuántas filas desea visualizar? (n para las primeras, -n para las últimas o vacío para todas): ")
                if n.strip() == "":
                    n = None  # Mostrar todas las filas
                else:
                    n = int(n)
                break
            except ValueError:
                print("Por favor, ingrese un número entero válido.")
        # Construir la consulta
        if n is None:
            query = f"SELECT {', '.join(columnas_a_visualizar)} FROM {nombre_tabla};"
        elif n > 0:
            query = f"SELECT {', '.join(columnas_a_visualizar)} FROM {nombre_tabla} LIMIT {n};"
        else:
            n = abs(n)
            query = f"SELECT {', '.join(columnas_a_visualizar)} FROM {nombre_tabla} ORDER BY id DESC LIMIT {n};"
        # Ejecutar la consulta y visualizar los resultados
        df = pd.read_sql_query(query, conn)
        print("\nResultados:")
        print(df)
        # Pregunta si quiere volver a visualizar otra tabla
        continuar = input("¿Desea visualizar otra tabla? (s/n): ").strip().lower()
        if continuar != 's':
            break
    conn.close()

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONE MODIFICAR DATOS MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def modificar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conn.cursor()
    
    # Mostrar tablas disponibles
    try:
        cursor.execute("SHOW TABLES;")
        tablas = [tabla[0] for tabla in cursor.fetchall()]  # Obtener solo los nombres de las tablas
    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")
        conn.close()  # Cierra la conexión antes de salir
        return

    if not tablas:
        print("No hay tablas en la base de datos.")
        conn.close()
        return
    
    print("Tablas disponibles:")
    for tabla in tablas:
        print(tabla)
    
    nombre_tabla = input("Ingresa el nombre de la tabla: ").strip()
    if nombre_tabla not in tablas:
        print("La tabla no existe.")
        conn.close()
        return
    
    while True:
        print(f"\nFormato: SET columna = nuevo_valor WHERE condicion")
        print("Ejemplo: SET edad = 18 WHERE id = 5")
        print("Para modificar un dato nulo: Ejemplo: SET edad = 30 WHERE edad IS NULL")
        print("Nota: Recuerda poner valores de texto entre comillas simples (' '). Ejemplo: SET nombre = 'Juan' WHERE nombre IS NULL")
        
        query_input = input("Ingresa solamente la condición (o deja vacío para salir): ").strip()
        if query_input == "":
            print("Saliendo de la función.")
            break
        
        try:
            # Verificar que la entrada sea válida
            if 'SET' not in query_input or 'WHERE' not in query_input:
                print("Formato inválido. Asegúrate de usar 'SET columna = valor WHERE condicion'.")
                continue         

            # Ejecutar la consulta
            query = f"UPDATE {nombre_tabla} {query_input}"
            cursor.execute(query)
            conn.commit()  # Guardar los cambios
            print("Datos modificados exitosamente.")
        except mysql.connector.Error as e:
            print(f"Error al modificar los datos: {e}")
    
    conn.close()  # Cierra la conexión

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONE ELIMINAR DATOS MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def eliminar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn = conectar_db()  # Usamos la función conectar_db() ya implementada
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return

    cursor = conn.cursor()
    
    # Mostrar tablas disponibles
    try:
        cursor.execute("SHOW TABLES;")
        tablas = [tabla[0] for tabla in cursor.fetchall()]  # Obtener solo los nombres de las tablas
    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")
        conn.close()  # Cierra la conexión antes de salir
        return

    if not tablas:
        print("No hay tablas en la base de datos.")
        conn.close()
        return
    
    print("Tablas disponibles:")
    for tabla in tablas:
        print(tabla)
    
    nombre_tabla = input("Ingresa el nombre de la tabla: ").strip()
    if nombre_tabla not in tablas:
        print("La tabla no existe.")
        conn.close()
        return
    
    # Mostrar los datos de la tabla seleccionada
    print(f"\nDatos de la tabla '{nombre_tabla}':")
    df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla};", conn)
    print(df)
    
    # Ejemplos de condiciones posibles
    print(f"\nFormato: DELETE FROM {nombre_tabla} WHERE: condicion")
    print("\nEjemplos de condiciones para eliminar:")
    print("1. 'nombre_columna = 'valor'' para eliminar filas donde la columna tenga un valor específico.")
    print("2. 'edad > 30' para eliminar filas donde la edad sea mayor a 30.")
    print("3. 'comuna = 'Madrid' AND edad < 25' para eliminar filas donde la comuna sea 'Madrid' y la edad sea menor a 25.")
    print("4. 'nombre_columna IN ('valor1', 'valor2')' para eliminar filas donde la columna tenga uno de los valores especificados.")
    
    query_input = input("Ingresa únicamente la condición de eliminación (o deja vacío para salir): ").strip()
    if query_input == "":
        print("Saliendo de la función.")
    else:
        try:
            # Ejecutar la consulta
            query = f"DELETE FROM {nombre_tabla} WHERE {query_input};"
            cursor.execute(query)
            conn.commit()  
            print("Datos eliminados exitosamente.")
        except mysql.connector.Error as e:
            print(f"Error al eliminar los datos: {e}")
    
    conn.close()  # Cierra la conexión

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONE CONSULTAR/CONSULTAS DATOS MYSQL
# --------------------------------------------------------------------------------------------------------------- 
def consultar_db2():
    conn = conectar_db()
    print("Comandos disponibles:")
    print("Formato: SELECT (columnas) FROM (tablas) WHERE (condición)")
    print("Puedes seleccionar todas las columnas con '*' o separar varias columnas con comas.")
    print("Ejemplo de selección de columnas: SELECT columna1, columna2 FROM tabla1")
    print("\nPara usar múltiples tablas, puedes emplear JOIN:")
    print("Ejemplo de JOIN: SELECT columna1 FROM tabla1 JOIN tabla2 ON tabla1.id = tabla2.id")
    print("\nCondiciones: Puedes usar operadores como '=', '<', '>', 'AND', 'OR', etc.")
    print("Ejemplo de condición: WHERE columna1 = 'valor' AND columna2 > 10")

    while True:
        query_input = input("\nIngresa tu consulta SQL (o deja vacío para salir): ").strip()
        if query_input == "":
            print("Saliendo de la función.")
            break
        try:
            # Ejecutar la consulta y convertir el resultado en un DataFrame de pandas
            df = pd.read_sql_query(query_input, conn)
            print("\nResultados de la consulta:")
            print(df)
        except Exception as e:
            print(f"Error en la consulta: {e}")
    
    conn.close()  # Cierra la conexión

# --------------------------------------------------------------------------------------------------------------- 
# FUNCIONES PARA REGISTROS PLUVIALES
# --------------------------------------------------------------------------------------------------------------- 
def cargar_registros_pluviales():
    año = input("Ingrese el año (por ejemplo, 2023): ").strip()
    archivo_csv = f"registroPluvial{año}.csv"

    # Verificar si el archivo CSV existe
    if os.path.exists(archivo_csv):
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(archivo_csv)
        print("Archivo CSV encontrado. Meses disponibles:")
        print(df.columns.tolist())  # Muestra los nombres de las columnas (meses)

        mes = input("Ingrese el mes que desea consultar (por ejemplo, Enero): ").strip()
        if mes in df.columns:
            print(f"Registros pluviales de {mes} {año}:")
            print(df[mes])
        else:
            print("Mes no encontrado en el archivo.")
    else:
        print("Archivo no encontrado. Generando datos aleatorios...")
        
        # Generar datos aleatorios para el año
        dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        datos_pluviales = {}
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Generar registros pluviales aleatorios
        for i, mes in enumerate(meses):
            # Generar datos para el mes correspondiente
            registros = [random.randint(0, 100) for _ in range(dias_por_mes[i])]
            datos_pluviales[mes] = registros

        # Crear un DataFrame de pandas
        df_nuevo = pd.DataFrame(dict([(mes, pd.Series(datos_pluviales[mes])) for mes in meses]))

        # Guardar el DataFrame en un archivo CSV
        df_nuevo.to_csv(archivo_csv, index=False)
        print(f"Datos pluviales aleatorios generados y guardados en '{archivo_csv}'.")

        # Permitir al usuario elegir un mes
        mes = input("Ingrese el mes que desea consultar (por ejemplo, Enero): ").strip()
        if mes in df_nuevo.columns:
            print(f"Registros pluviales de {mes} {año}:")
            print(df_nuevo[mes])
        else:
            print("Mes no encontrado en el archivo generado.")

def obtener_registros_pluviales():
    año = input("Ingrese el año para el que desea graficar las precipitaciones: ").strip()
    archivo_csv = f"registroPluvial{año}.csv"
    
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        # Sumar las precipitaciones por mes
        registros = [(mes, df[mes].sum()) for mes in df.columns]
        return registros
    else:
        print(f"No se encontró el archivo para el año {año}.")
        return None
    
def graficar_precipitaciones():
    registros = obtener_registros_pluviales()
    if registros:
        meses, cantidades = zip(*registros)
        
        plt.figure(figsize=(10, 6))
        plt.bar(meses, cantidades, color='skyblue')
        plt.xlabel('Meses')
        plt.ylabel('Cantidad de precipitaciones (mm)')
        plt.title('Registros pluviales del año')
        plt.xticks(rotation=45)  # Rotar etiquetas de meses
        plt.tight_layout()  # Ajustar layout para que no se solapen los textos
        plt.show()
    else:
        print("No hay registros de precipitaciones para graficar.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN DE BIENVENIDA
# ---------------------------------------------------------------------------------------------------------------  
def bienvenida():
    print("--------------------------------------------------------------------------")
    print("-------- ¡Bienvenido a la aplicación de fidelización de clientes! --------")
    print("--------------------------------------------------------------------------")
    print("-------- Por favor, seleccione una opción del menú para continuar. -------")
    print("--------------------------------------------------------------------------")
    print("                                                                          ")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN PARA REGISTRAR USUARIO
# ---------------------------------------------------------------------------------------------------------------  
def registrar_usuario():
    usuarios = cargar_usuarios()

    id_usuario = len(usuarios) + 1
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    
    while not dni.isdigit() or any(u.dni == dni for u in usuarios):
        print("DNI inválido o ya registrado. Intente nuevamente.")
        dni = input("DNI: ")

    correo = input("Correo electrónico: ")
    fecha_nacimiento = input("Fecha de nacimiento (dd/mm/yyyy): ")
    
    while not re.match(r'\d{2}/\d{2}/\d{4}', fecha_nacimiento):
        print("Formato de fecha incorrecto. Ingrese en el formato dd/mm/yyyy.")
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/yyyy): ")

    usuario = input("Nombre de usuario (6-12 caracteres): ")
    while len(usuario) < 6 or len(usuario) > 12 or any(u.usuario == usuario for u in usuarios):
        print("Usuario inválido o ya existente. Intente nuevamente.")
        usuario = input("Nombre de usuario (6-12 caracteres): ")

    clave = input("Contraseña: ")
    while not (len(clave) >= 8 and re.search("[a-z]", clave) and re.search("[A-Z]", clave) and re.search("[0-9]", clave) and re.search("[^a-zA-Z0-9]", clave)):
        print("Contraseña inválida. Requisitos: (8 Caracteres mínimo), (Una Letra Mayúscula), (Al menos un Número), (Un Caracter Especial).")
        clave = input("Contraseña: ")

    nuevo_usuario = Usuario(id_usuario, nombre, apellido, dni, usuario, clave, correo, fecha_nacimiento)
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    print("Usuario creado correctamente.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN PARA INICIAR SESIÓN
# ---------------------------------------------------------------------------------------------------------------  
def iniciar_sesion():
    usuarios = cargar_usuarios()
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")
    intentos_fallidos = 0

    for u in usuarios:
        if u.usuario == usuario:
            while intentos_fallidos < 4:
                if u.clave == clave:
                    print(f"\n¡Bienvenido {usuario}! Has ingresado a la Gestión de Base de Datos de Fidelización de Clientes.")
                    gestion_base_datos()  # Llama al submenú de Gestión de Base de Datos
                    return True
                else:
                    intentos_fallidos += 1
                    print(f"Contraseña incorrecta. Intento {intentos_fallidos}/4")
                    if intentos_fallidos == 4:
                        registrar_log_fallido(usuario, clave)
                        print("Usuario bloqueado.")
                        return False
                    clave = input("Contraseña: ")
            break
    else:
        print("Usuario no encontrado.")
        registrar_log_fallido(usuario, clave)
        return False

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Ordenar usuarios por 'username' y guardar en un archivo separado
# ---------------------------------------------------------------------------------------------------------------  
def ordenar_usuarios_por_username():
    usuarios = cargar_usuarios()
    usuarios.sort(key=lambda u: u.usuario)  # Ordena los usuarios por 'username'
    
    # Guardar usuarios ordenados en un nuevo archivo
    ruta_usuarios_ordenados = os.path.join(RUTA_CARPETA, "usuariosOrdenadosPorUsername.ispc")
    with open(ruta_usuarios_ordenados, "wb") as file:
        pickle.dump(usuarios, file)
    
    print("Usuarios ordenados por 'username' y guardados en 'usuariosOrdenadosPorUsername.ispc'.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar usuario por DNI
# ---------------------------------------------------------------------------------------------------------------  
def buscar_usuario_por_dni(dni):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u.dni == dni:
            print(u)
            return
    print("No se encontró un usuario con ese DNI.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar usuario por 'username'
# ---------------------------------------------------------------------------------------------------------------  
def buscar_usuario_por_username(username):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u.usuario == username:
            print(u)
            return
    print("No se encontró un usuario con ese 'username'.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar usuario por correo electrónico
# ---------------------------------------------------------------------------------------------------------------  
def buscar_usuario_por_email(email):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u.correo == email:
            print(u)
            return
    print("No se encontró un usuario con ese correo electrónico.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Mostrar todos los usuarios desde los archivos
# ---------------------------------------------------------------------------------------------------------------  
def mostrar_todos_los_usuarios():
    usuarios = cargar_usuarios()
    if usuarios:
        print("\nUsuarios en 'usuarios.ispc':")
        for u in usuarios:
            print(u)
    else:
        print("No hay usuarios registrados en 'usuarios.ispc'.")

    ruta_usuarios_ordenados = os.path.join(RUTA_CARPETA, "usuariosOrdenadosPorUsername.ispc")
    if os.path.exists(ruta_usuarios_ordenados):
        with open(ruta_usuarios_ordenados, "rb") as file:
            usuarios_ordenados = pickle.load(file)
            print("\nUsuarios en 'usuariosOrdenadosPorUsername.ispc':")
            for u in usuarios_ordenados:
                print(u)
    else:
        print("\nNo hay usuarios registrados en 'usuariosOrdenadosPorUsername.ispc'.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar Usuario
# ---------------------------------------------------------------------------------------------------------------  
def buscar_usuario_por_username(username):
    ruta_usuarios_ordenados = os.path.join(RUTA_CARPETA, "usuariosOrdenadosPorUsername.ispc")
    if os.path.exists(ruta_usuarios_ordenados):
        print("Se utilizó la búsqueda por username y la técnica fue la búsqueda binaria.")
        usuario = buscar_usuario_binario(username, cargar_usuarios(ruta_usuarios_ordenados))  # Cargar usuarios ordenados
    else:
        print("Se utilizó la búsqueda por username y la técnica fue la búsqueda secuencial.")
        usuario = buscar_usuario(username, cargar_usuarios())  # Cargar usuarios no ordenados

    if usuario:
        print(f"Usuario encontrado:\n{usuario}")
    else:
        print("No se encontró un usuario con ese 'username'.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar Usuario por DNI Binario
# --------------------------------------------------------------------------------------------------------------- 
def buscar_usuario_por_dni_binaria(dni):
    usuarios = cargar_usuarios()
    usuarios.sort(key=lambda x: x.dni)  # Asegurar que esté ordenado

    # Optimización de rango para evitar la búsqueda innecesaria
    if dni < int(usuarios[0].dni):
        print("El DNI a buscar es más pequeño que el más chico registrado. No se realizará la búsqueda.")
        return
    elif dni > int(usuarios[-1].dni):
        print("El DNI a buscar es más grande que el más grande registrado. No se realizará la búsqueda.")
        return

    # Búsqueda binaria
    izquierda, derecha = 0, len(usuarios) - 1
    intentos = 0
    while izquierda <= derecha:
        intentos += 1
        medio = (izquierda + derecha) // 2
        dni_medio = int(usuarios[medio].dni)
        if dni_medio == dni:
            print(f"Usuario encontrado:\n{usuarios[medio]}")
            print(f"Se utilizó la búsqueda por DNI y fue binaria, encontrando el usuario en {intentos} intentos.")
            return
        elif dni_medio < dni:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    print(f"No se encuentra registrado el usuario con el DNI {dni}. Se realizaron {intentos} intentos.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar Usuario por Email
# --------------------------------------------------------------------------------------------------------------- 
def buscar_usuario_por_email(email):
    usuarios = cargar_usuarios()
    intentos = 0
    for u in usuarios:
        intentos += 1
        if u.correo == email:
            print(f"Usuario encontrado:\n{u}")
            print(f"Se utilizó la búsqueda por email y la técnica fue la búsqueda secuencial, encontrando el usuario en {intentos} intentos.")
            return
        else:
            print(f"Intento {intentos}: {email} es distinto a {u.correo}")
    print(f"No se encontró un usuario con el email '{email}' tras {intentos} intentos.")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar Usuario por Busqueda Binaria
# --------------------------------------------------------------------------------------------------------------- 
def registrar_log_busqueda_binaria(tipo_busqueda, valor, detalles):
    fecha = datetime.now().strftime("%Y-%m-%d")
    ruta_log = os.path.join(RUTA_CARPETA, f"búsquedasYordenamientos/buscandoUsuarioPor{tipo_busqueda}-{fecha}.txt")
    os.makedirs(os.path.dirname(ruta_log), exist_ok=True)
    with open(ruta_log, "a") as log_file:
        log_file.write(f"Búsqueda Binaria por {tipo_busqueda}: buscando el {tipo_busqueda} {valor}\n")
        log_file.write("\n".join(detalles) + "\n")
        log_file.write("Fin de la búsqueda\n\n")

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIÓN: Buscar Usuario por DNI Binario
# --------------------------------------------------------------------------------------------------------------- 
    detalles_log = []
    while izquierda <= derecha:
        intentos += 1
        medio = (izquierda + derecha) // 2
        dni_medio = int(usuarios[medio].dni)
        if dni_medio == dni:
            detalles_log.append(f"Intento {intentos}: DNI en posición {medio} es {dni_medio}. Encontrado.")
            registrar_log_busqueda_binaria("DNI", dni, detalles_log)
            print("Usuario encontrado.")
            return
        elif dni_medio < dni:
            detalles_log.append(f"Intento {intentos}: DNI {dni_medio}. Buscar en derecha.")
            izquierda = medio + 1
        else:
            detalles_log.append(f"Intento {intentos}: DNI {dni_medio}. Buscar en izquierda.")
            derecha = medio - 1
    detalles_log.append(f"No se encuentra registrado el usuario con el DNI {dni}. Se realizaron {intentos} intentos.")
    registrar_log_busqueda_binaria("DNI", dni, detalles_log)

# ---------------------------------------------------------------------------------------------------------------  
# FUNCIONES MODIFICAR, ELIMINAR, BUSCAR, ORDENAR USUARIOS. CRUD
# ---------------------------------------------------------------------------------------------------------------  
def modificar_usuario():
    usuarios = cargar_usuarios()
    usuario = input("Ingrese el nombre de usuario o correo del usuario que desea modificar: ")
    
    for u in usuarios:
        if u.usuario == usuario or u.correo == usuario:
            print("Usuario encontrado. Ingrese los nuevos datos (deje en blanco si no desea modificar):")
            nuevo_nombre = input(f"Nombre actual: {u.nombre}. Nuevo nombre: ") or u.nombre
            nuevo_apellido = input(f"Apellido actual: {u.apellido}. Nuevo apellido: ") or u.apellido
            nueva_clave = input("Ingrese nueva contraseña (8 caracteres mínimo, mayúscula, número y caracter especial): ")
            
            while nueva_clave and not (len(nueva_clave) >= 8 and re.search("[a-z]", nueva_clave) and re.search("[A-Z]", nueva_clave) and re.search("[0-9]", nueva_clave) and re.search("[^a-zA-Z0-9]", nueva_clave)):
                print("Contraseña inválida. Intente nuevamente.")
                nueva_clave = input("Nueva contraseña: ")
            nueva_clave = nueva_clave or u.clave

            u.nombre = nuevo_nombre
            u.apellido = nuevo_apellido
            u.clave = nueva_clave

            guardar_usuarios(usuarios)
            print("Usuario modificado correctamente.")
            return
    
    print("Usuario no encontrado.")

def eliminar_usuario():
    usuarios = cargar_usuarios()
    usuario = input("Ingrese el nombre de usuario o correo del usuario que desea eliminar: ")
    
    for u in usuarios:
        if u.usuario == usuario or u.correo == usuario:
            usuarios.remove(u)
            guardar_usuarios(usuarios)
            print("Usuario eliminado correctamente.")
            return
    
    print
def eliminar_usuario():
    usuarios = cargar_usuarios()
    usuario = input("Ingrese el nombre de usuario o correo del usuario que desea eliminar: ")
    
    for u in usuarios:
        if u.usuario == usuario or u.correo == usuario:
            usuarios.remove(u)
            guardar_usuarios(usuarios)
            print("Usuario eliminado correctamente.")
            return
    
    print("Usuario no encontrado.")

def buscar_usuario(username, usuarios):
    """Búsqueda secuencial de usuario"""
    for u in usuarios:
        if u.usuario == username:
            return u
    return None

def buscar_usuario_binario(username, usuarios):
    """Búsqueda binaria de usuario"""
    usuarios.sort(key=lambda x: x.usuario)  # Asegurarse de que la lista esté ordenada
    izquierda, derecha = 0, len(usuarios) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if usuarios[medio].usuario == username:
            return usuarios[medio]
        elif usuarios[medio].usuario < username:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None

def ordenar_usuarios():
    usuarios = cargar_usuarios()
    
    print("Elija un método de ordenamiento:")
    print("1. Ordenamiento Burbuja")
    print("2. Ordenar con sort() de Python")
    
    opcion = input("Opción: ")
    
    if opcion == "1":
        # Ordenamiento Burbuja
        for i in range(len(usuarios)):
            for j in range(0, len(usuarios) - i - 1):
                if usuarios[j].usuario > usuarios[j + 1].usuario:
                    usuarios[j], usuarios[j + 1] = usuarios[j + 1], usuarios[j]
        print("Usuarios ordenados usando el método Burbuja.")
    
    elif opcion == "2":
        usuarios.sort(key=lambda x: x.usuario)
        print("Usuarios ordenados usando sort().")
    
    else:
        print("Opción no válida.")
        return

    guardar_usuarios(usuarios)

# ---------------------------------------------------------------------------------------------------------------  
# CONSULTAS SQL
# --------------------------------------------------------------------------------------------------------------- 

# --- DONE

def consultar_historial_clientes():
    try:
        conexion = conectar_db()
        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return  # Sale de la función si no hay conexión
        
        cursor = conexion.cursor()  # Corregido: crear un cursor de la conexión
        cursor.execute("""
            SELECT Clientes.Nombre, Clientes.Apellido, HistorialCuentas.FechaAlta, HistorialCuentas.AntiguedadCta, HistorialCuentas.Churn
            FROM Clientes
            INNER JOIN HistorialCuentas ON Clientes.IDCliente = HistorialCuentas.IDCliente
        """)
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"Cliente: {fila[0]} {fila[1]}, Fecha Alta: {fila[2]}, Antigüedad: {fila[3]}, Churn: {fila[4]}")
    except Exception as e:
        print(f"Error al consultar historial de clientes: {e}")
    finally:
        if cursor:
            cursor.close()  # Cierra el cursor solo si fue creado
        if conexion:
            conexion.close()  # Cierra la conexión solo si fue creada
        
# --- DONE

def contar_clientes_por_area():
    conexion = conectar_db()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return  # Sale de la función si no hay conexión
    
    cursor = conexion.cursor()
    try:
        # Consulta para contar clientes por área geográfica
        cursor.execute("""
            SELECT AreaGeografica.Estado, COUNT(Clientes.IDCliente) AS NumeroClientes
            FROM Clientes
            INNER JOIN AreaGeografica ON Clientes.IDAreaGeografica = AreaGeografica.IDAreaGeografica
            GROUP BY AreaGeografica.Estado
        """)
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"Área: {fila[0]}, Número de Clientes: {fila[1]}")
    except Exception as e:
        print(f"Error al contar clientes por área: {e}")
    finally:
        cursor.close()
        conexion.close()

# --- DONE

def listar_clientes_activos_inactivos():
    conexion = conectar_db()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * FROM clientes")  # Ajusta esta consulta según lo que necesites
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)
        except mysql.connector.Error as err:
            print(f"Error al listar clientes activos e inactivos: {err}")
        finally:
            cursor.close()
    else:
        print("Error: la conexión no está establecida.")
        
# --- DONE  

def buscar_clientes_por_mes_nacimiento(mes):
    conexion = conectar_db()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return  # Sale de la función si no hay conexión
    
    try:
        cursor = conexion.cursor()
        
        # Asegúrate de usar el nombre correcto de la columna de fecha
        cursor.execute("SELECT * FROM Clientes WHERE MONTH(fechaNacimiento) = %s", (mes,))
        clientes = cursor.fetchall()

        if clientes:
            print(f"Clientes nacidos en el mes {mes}:")
            for cliente in clientes:
                print(cliente)
        else:
            print(f"No hay clientes nacidos en el mes {mes}.")
    
    except Exception as e:
        print(f"Error al buscar clientes por mes de nacimiento: {e}")
    
    finally:
        if cursor:
            cursor.close()  # Cierra el cursor si fue creado
        if conexion:
            conexion.close()  # Cierra la conexión si fue creada

# ---------------------------------------------------------------------------------------------------------------        
# FUNCION MENÚ PRINCIPAL
# ---------------------------------------------------------------------------------------------------------------  
def menu_principal():
    while True:
        bienvenida()  # Llama a la función de bienvenida
        print("------------ Menú Principal ------------")
        print("0. Menú Fidelización de Clientes")
        print("----------------------------------------")
        print("1. Registrar Usuario")
        print("2. Iniciar Sesión")  # Iniciar sesión para acceder a la Gestión de Base de Datos
        print("3. Modificar Usuario")
        print("4. Eliminar Usuario")
        print("----------------------------------------")
        print("Menú Ordenar y Buscar Usuarios")
        print("----------------------------------------")
        print("5. Ordenar y Buscar Usuarios")  
        print("6. Mostrar Todos los Usuarios") 
        print("----------------------------------------")
        print("Cargar / Graficar (Registros Pluviales)")
        print("----------------------------------------")
        print("7. Cargar Registros Pluviales")
        print("8. Graficar Registros Pluviales")
        print("9. Salir")
        print("----------------------------------------")
        
        opcion = input("Seleccione una opción: ")
        
        # Opciones del menú principal
        if opcion == "0":
            menu_FC()  # Llama al menú de Fidelización de Clientes
        elif opcion == "1":
            registrar_usuario()  # Registra un nuevo usuario
        elif opcion == "2":
            iniciar_sesion()  # Permite al usuario iniciar sesión
        elif opcion == "3":
            modificar_usuario()  # Modifica los datos de un usuario
        elif opcion == "4":
            eliminar_usuario()  # Elimina un usuario
        elif opcion == "5":
            menu_ordenamiento_busqueda_usuarios()  # Submenú de ordenamiento y búsqueda
        elif opcion == "6":
            mostrar_todos_los_usuarios()  # Muestra todos los usuarios
        elif opcion == "7":
            cargar_registros_pluviales()  # Cargar registros de lluvia
        elif opcion == "8":
            # Submenú de gráficos
            print("Seleccione un tipo de gráfico:")
            print("1. Gráfico de Barras de Lluvias Anuales")
            print("2. Gráfico de Dispersión (Meses vs Días)")
            print("3. Gráfico Circular de Lluvias por Mes")
            
            grafico_opcion = input("Seleccione una opción de gráfico: ")
            if grafico_opcion == "1":
                graficar_barras_lluvias_anuales()
            elif grafico_opcion == "2":
                graficar_dispersion()
            elif grafico_opcion == "3":
                graficar_pie_lluvias()
            else:
                print("Opción de gráfico no válida.")
        elif opcion == "9":
            print("Saliendo del programa...")
            break  # Finaliza el programa
        else:
            print("Opción no válida, intente de nuevo.")
            
# ---------------------------------------------------------------------------------------------------------------      
#SUB MENÚ Fidelización de Clientes
# ---------------------------------------------------------------------------------------------------------------  
def menu_FC():
    while True:
        print("\n----- Menú Fidelización de Clientes -----")
        print("1. Visualizar base de datos")
        print("2. Crear tabla")
        print("3. Eliminar tabla")
        print("4. Agregar datos")
        print("5. Eliminar datos")
        print("6. Modificar datos")
        print("7. Consultar datos")  # Opción para realizar consultas complejas
        print("8. Volver al Menú Principal")
            
        opcion = input("Seleccione una opción: ")
    
        # Opciones del menú de Fidelización de Clientes
        if opcion == "1":
            visualizar_mysql()  # Visualiza la base de datos
        elif opcion == '2':
            crear_tabla_mysql()  # Crea una nueva tabla
        elif opcion == '3':
            eliminar_tabla_mysql()  # Elimina una tabla existente
        elif opcion == '4':
            agregar_datos_mysql()  # Agrega datos a la tabla
        elif opcion == '5':
            eliminar_datos_mysql()  # Elimina datos de la tabla
        elif opcion == '6':
            modificar_datos_mysql()  # Modifica datos existentes
        elif opcion == '7':
            consultar_db2()  # Realiza consultas a la base de datos
        elif opcion == '8':
            print("Volviendo al menú principal...")
            break  # Vuelve al menú principal
        else:
            print("Opción no válida, intente de nuevo.")  # Mensaje de error si la opción no es válida

# ---------------------------------------------------------------------------------------------------------------  
# SUB MENÚ Opciones de Ordenamiento y Búsqueda de Usuarios
# ---------------------------------------------------------------------------------------------------------------  
def menu_ordenamiento_busqueda_usuarios():
    while True:
        print("\n--- Menú de Ordenamiento y Búsqueda de Usuarios ---")
        print("1. Ordenar Usuarios por Username y Guardar")
        print("2. Buscar Usuario por DNI")
        print("3. Buscar Usuario por Username")
        print("4. Buscar Usuario por Email")
        print("5. Mostrar Todos los Usuarios")
        print("6. Volver al Menú Principal")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ordenar_usuarios_por_username()
        elif opcion == "2":
            dni = input("Ingrese el DNI del usuario: ")
            buscar_usuario_por_dni(dni)
        elif opcion == "3":
            username = input("Ingrese el username del usuario: ")
            buscar_usuario_por_username(username)
        elif opcion == "4":
            email = input("Ingrese el email del usuario: ")
            buscar_usuario_por_email(email)
        elif opcion == "5":
            mostrar_todos_los_usuarios()
        elif opcion == "6":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

# ---------------------------------------------------------------------------------------------------------------  
#SUB MENÚ Gestión de Base de Datos con Consultas Reales
# ---------------------------------------------------------------------------------------------------------------  
def gestion_base_datos():
    while True:
        print("\n--- Gestión de Base de Datos ---")
        print("1. Consultar Historial de Cuentas de Clientes")
        print("2. Contar Clientes por Área Geográfica")
        print("3. Listar Clientes Activos e Inactivos")
        print("4. Buscar Clientes por Mes de Nacimiento")
        print("5. Volver al Menú Principal")
        print("6. Salir de la Aplicación")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            consultar_historial_clientes()  # Consulta con JOIN entre Clientes y HistorialCuentas
        elif opcion == "2":
            contar_clientes_por_area()  # Cuenta clientes por área
        elif opcion == "3":
            listar_clientes_activos_inactivos()  # Lista clientes por estado de actividad
        elif opcion == "4":
            mes = int(input("Ingrese el número de mes (1-12): "))
            buscar_clientes_por_mes_nacimiento(mes)  # Busca clientes por mes de nacimiento
        elif opcion == "5":
            print("Volviendo al menú principal...")
            break
        elif opcion == "6":
            print("Saliendo de la aplicación...")
            exit()
        else:
            print("Opción no válida, intente de nuevo.")

# ---------------------------------------------------------------------------------------------------------------  
# CREAR BASE DE DATOS Y MENÚ PRINCIPAL
# ---------------------------------------------------------------------------------------------------------------  
if __name__ == "__main__":
    crear_db()
    menu_principal()
    crear_conexion()
