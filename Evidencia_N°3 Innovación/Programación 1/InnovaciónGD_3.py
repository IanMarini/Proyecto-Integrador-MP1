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


# RUTA DE ARCHIVOS
RUTA_DB2 = "ruta/a/tu/base_de_datos.db"
RUTA_CARPETA = r"C:\Users\marin\OneDrive\Desktop\Evidencia_1\App"
RUTA_USUARIOS = os.path.join(RUTA_CARPETA, "usuarios.txt")
RUTA_ACCESOS = os.path.join(RUTA_CARPETA, "accesos.txt")
RUTA_LOG = os.path.join(RUTA_CARPETA, "log.txt")
RUTA_DB = os.path.join(RUTA_CARPETA, "registros_pluviales.db")  # Base de datos para registros pluviales

# CLASES
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


# FUNCIONES PARA MANEJAR ARCHIVOS BINARIOS
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

# FUNCIONES DE REGISTROS PLUVIALES
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

# FUNCIONES DE LOS GRÁFICOS
def graficar_dispersion():
    registros = obtener_registros_pluviales()
    if registros:
        meses, cantidades = zip(*registros)
        
        plt.figure(figsize=(10, 6))
        dias = list(range(1, 32))  # Días del 1 al 31
        plt.scatter(meses * len(dias), dias * len(meses), color='blue')
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

# MYSQL
# Definición de default_values
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
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba inicial
    
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
        return conn, creds  # Devuelve la conexión y las credenciales usadas
    
    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return None, None

    
# FUNCIONES DE FIDELIZACION DE CLIENTES (CRUD)
def crear_tabla_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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
    print("Tipos de columnas: INT, VARCHAR(n), FLOAT, DATE, etc.")
    print("Restricciones: PRIMARY KEY, NOT NULL, UNIQUE, CHECK (condición), DEFAULT (valor)")
    
    columnas = input("\nIngrese las columnas separadas por comas: ")
    
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
        cursor.execute(query)
        conn.commit()  # Guarda los cambios en la base de datos
        print(f"Tabla '{nombre_tabla}' creada exitosamente.")
    except mysql.connector.Error as e:
        print(f"Error al crear la tabla: {e}")   
    finally:
        conn.close()  # Cierra la conexión
    

def eliminar_tabla_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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

def agregar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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
    
def visualizar_mysql():
    # Conectar a la base de datos (usa credenciales por defecto)
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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
    
def modificar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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
    
def eliminar_datos_mysql():
    print("Intentando conectar a la base de datos...")  # Mensaje de prueba
    # Conectar a la base de datos
    conn, creds = conectar_db()  # Usamos la función conectar_db() ya implementada
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

    
def consultar_db2():
    conn = sqlite3.connect(RUTA_DB2)
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


# FUNCIONES PARA REGISTROS PLUVIALES
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

# FUNCIÓN DE BIENVENIDA
def bienvenida():
    print("------------------------------------------------------------------------")
    print("-------- ¡Bienvenido a la aplicación de fidelización de clientes! --------")
    print("------------------------------------------------------------------------")
    print("-------- Por favor, seleccione una opción del menú para continuar. -------")
    print("------------------------------------------------------------------------")

# FUNCIÓN PARA REGISTRAR USUARIO
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

# FUNCIÓN PARA INICIAR SESIÓN
def iniciar_sesion():
    usuarios = cargar_usuarios()
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")
    intentos_fallidos = 0

    for u in usuarios:
        if u.usuario == usuario:
            while intentos_fallidos < 4:
                if u.clave == clave:
                    print(f"Bienvenido {usuario}!")
                    accesos = cargar_accesos()
                    nuevo_acceso = Acceso(len(accesos) + 1, u)
                    accesos.append(nuevo_acceso)
                    guardar_accesos(accesos)
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

# FUNCIONES CRUD ADICIONALES
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
    
# FUNCIONES CRUD
def consultar_historial_clientes(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT Clientes.Nombre, Clientes.Apellido, HistorialCuentas.Fecha, HistorialCuentas.Monto
            FROM Clientes
            JOIN HistorialCuentas ON Clientes.IDCliente = HistorialCuentas.IDCliente
        """)
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"Cliente: {fila[0]} {fila[1]}, Fecha: {fila[2]}, Monto: {fila[3]}")
    except Error as e:
        print(f"Error al consultar historial de clientes: {e}")
    finally:
        cursor.close()

def contar_clientes_por_area(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT AreaGeografica.NombreArea, COUNT(Clientes.IDCliente)
            FROM Clientes
            JOIN AreaGeografica ON Clientes.IDAreaGeografica = AreaGeografica.IDAreaGeografica
            GROUP BY AreaGeografica.NombreArea
        """)
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"Área: {fila[0]}, Total Clientes: {fila[1]}")
    except Error as e:
        print(f"Error al contar clientes por área geográfica: {e}")
    finally:
        cursor.close()

def listar_clientes_actividad(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT NombreUsuario, Churn
            FROM Clientes
        """)
        resultados = cursor.fetchall()
        for fila in resultados:
            estado = "Activo" if fila[1] == 0 else "Inactivo"
            print(f"Usuario: {fila[0]}, Estado: {estado}")
    except Error as e:
        print(f"Error al listar clientes: {e}")
    finally:
        cursor.close()

def buscar_clientes_por_mes_nacimiento(conexion, mes):
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT Nombre, Apellido, FechaNacimiento
            FROM Clientes
            WHERE MONTH(FechaNacimiento) = %s
        """, (mes,))
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"Cliente: {fila[0]} {fila[1]}, Fecha de Nacimiento: {fila[2]}")
    except Error as e:
        print(f"Error al buscar clientes por mes de nacimiento: {e}")
    finally:
        cursor.close()

def menu_principal():
    while True:
        bienvenida()  # Llama a la función de bienvenida
        print("0. Menú Fidelización de Clientes")
        print("1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Modificar Usuario")
        print("4. Eliminar Usuario")
        print("5. Buscar Usuario")
        print("6. Ordenar Usuarios")
        print("7. Cargar Registros Pluviales")
        print("8. Graficar Registros Pluviales")
        print("9. Salir")
        
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
            # Búsqueda de usuario por username
            username = input("Ingrese el nombre de usuario a buscar: ")
            usuarios = cargar_usuarios()  # Carga la lista de usuarios
            resultado = buscar_usuario(username, usuarios)  # Busca el usuario
            if resultado:
                print(f"Usuario encontrado: {resultado}")
            else:
                print("Usuario no encontrado.")
                
            # Búsqueda binaria
            resultado_binario = buscar_usuario_binario(username, usuarios)
            if resultado_binario:
                print(f"Usuario encontrado por búsqueda binaria: {resultado_binario}")
            else:
                print("Usuario no encontrado por búsqueda binaria.")
        elif opcion == "6":
            ordenar_usuarios()  # Ordena la lista de usuarios
        elif opcion == "7":
            cargar_registros_pluviales()  # Carga los registros de lluvia
        elif opcion == "8":
            print("Selecciona un gráfico:")
            print("1. Gráfico de Barras de Lluvias Anuales")
            print("2. Gráfico de Dispersión (Meses vs Días)")
            print("3. Gráfico Circular de Lluvias por Mes")
            
            grafico_opcion = input("Seleccione una opción de gráfico: ")
            
            # Genera el gráfico correspondiente
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
            break  # Sale del programa
        else:
            print("Opción no válida, intente de nuevo.")  # Mensaje de error si la opción no es válida

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

# CREAR BASE DE DATOS Y MENÚ PRINCIPAL
if __name__ == "__main__":
    crear_db()
    menu_principal()
    crear_conexion()