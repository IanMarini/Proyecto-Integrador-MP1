import re
import random
import pickle
import os
from datetime import datetime

# Ruta de archivos
RUTA_CARPETA = r"C:\Users\marin\OneDrive\Desktop\Evidencia_1"
RUTA_USUARIOS = os.path.join(RUTA_CARPETA, "usuarios.ispc")
RUTA_ACCESOS = os.path.join(RUTA_CARPETA, "accesos.ispc")
RUTA_LOG = os.path.join(RUTA_CARPETA, "log.txt")

# Clases
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

# Funciones para manejar archivos binarios
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

# Función de bienvenida
def bienvenida():
    print("------------------------------------------------------------------------")
    print("--------¡Bienvenido a la aplicación de fidelización de clientes!--------")
    print("------------------------------------------------------------------------")
    print("--------Por favor, seleccione una opción del menú para continuar.-------")
    print("------------------------------------------------------------------------")

# Función para registrar usuario
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

    if captcha_verificacion():
        nuevo_usuario = Usuario(id_usuario, nombre, apellido, dni, usuario, clave, correo, fecha_nacimiento)
        usuarios.append(nuevo_usuario)
        guardar_usuarios(usuarios)
        print("Usuario creado correctamente.")
    else:
        print("No se completó el registro.")

# Función para iniciar sesión
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

# Funciones CRUD adicionales
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
    
    print("Usuario no encontrado.")

def buscar_usuario():
    usuarios = cargar_usuarios()
    usuario = input("Ingrese el nombre de usuario o correo a buscar: ")
    
    for u in usuarios:
        if u.usuario == usuario or u.correo == usuario:
            print("Usuario encontrado:")
            print(u)
            return
    
    print("Usuario no encontrado.")

def mostrar_todos_los_usuarios():
    usuarios = cargar_usuarios()
    
    if usuarios:
        print("Usuarios registrados:")
        for u in usuarios:
            print(u)
    else:
        print("No hay usuarios registrados.")

# Función para verificación Captcha
def captcha_verificacion():
    operaciones = [
        ('suma', lambda a, b: a + b),
        ('resta', lambda a, b: a - b),
        ('multiplicación', lambda a, b: a * b),
        ('división', lambda a, b: a / b)
    ]

    while True:
        operacion, funcion = random.choice(operaciones)
        a = round(random.uniform(1, 10), 2)
        b = round(random.uniform(1, 10), 2)

        try:
            resultado_real = round(funcion(a, b), 2)
            resultado_usuario = float(input(f"Resuelve la siguiente {operacion}: {a} y {b} (responde con dos decimales): "))
            
            if resultado_usuario == resultado_real:
                return True
            else:
                print("Captcha incorrecto.")
                opcion = input("¿Desea intentar nuevamente? (S/N): ").upper()
                if opcion != 'S':
                    return False
        except ValueError:
            print("Respuesta no válida. Asegúrate de ingresar un número con dos decimales.")

# Función para mostrar el menú principal
def mostrar_menu():
    while True:
        bienvenida()
        print("\n1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Modificar Usuario")
        print("4. Eliminar Usuario")
        print("5. Buscar Usuario")
        print("6. Mostrar Todos los Usuarios")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if iniciar_sesion():
                print("Acceso concedido.")
            else:
                print("Acceso denegado.")
        elif opcion == "3":
            modificar_usuario()
        elif opcion == "4":
            eliminar_usuario()
        elif opcion == "5":
            buscar_usuario()
        elif opcion == "6":
            mostrar_todos_los_usuarios()
        elif opcion == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecutar el menú principal
if __name__ == "__main__":
    mostrar_menu()
