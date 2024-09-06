import re
import random
from datetime import datetime
import aritmetica

usuarios = {}

def bienvenida():
    print("------------------------------------------------------------------------")
    print("--------¡Bienvenido a la aplicación de fidelización de clientes!--------")
    print("------------------------------------------------------------------------")
    print("--------Por favor, seleccione una opción del menú para continuar.-------")
    print("------------------------------------------------------------------------")
    
#-----------------------------------------------------------------------
#-----------------------Función Registrar Usuario-----------------------
#-----------------------------------------------------------------------
def registrar_usuario():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    
    dni = input("DNI: ")
    while not dni.isdigit() or dni in usuarios:
        print("DNI inválido o ya registrado. Intente nuevamente.")
        dni = input("DNI: ")
    
    correo = input("Correo electrónico: ")
    
    fecha_nacimiento = input("Fecha de nacimiento (dd/mm/yyyy): ")
    while not re.match(r'\d{2}/\d{2}/\d{4}', fecha_nacimiento):
        print("Formato de fecha incorrecto. Ingrese en el formato dd/mm/yyyy.")
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/yyyy): ")
    
    usuario = input("Nombre de usuario (6-12 caracteres): ")
    while len(usuario) < 6 or len(usuario) > 12 or any(u['usuario'] == usuario for u in usuarios.values()):
        print("Usuario inválido o ya existente. Intente nuevamente.")
        usuario = input("Nombre de usuario (6-12 caracteres): ")
    
    clave = input("Contraseña: ")
    while not (len(clave) >= 8 and re.search("[a-z]", clave) and re.search("[A-Z]", clave) and re.search("[0-9]", clave) and re.search("[^a-zA-Z0-9]", clave)):
        print("Contraseña inválida. Requisitos: (8 Caracteres minimo), (Una Letra Mayúscula), (Al menos un Número), (Un Caracter Especial).")
        clave = input("Contraseña: ")

    if captcha_verificacion():
        usuarios[dni] = {
            'nombre': nombre,
            'apellido': apellido,
            'usuario': usuario,
            'clave': clave,
            'correo': correo,
            'fecha_nacimiento': fecha_nacimiento
        }
        contenido = f"Usuario creado: {nombre} {apellido}, Usuario: {usuario}, DNI: {dni}\n"
        guardar_en_archivo("usuariosCreados.txt", contenido)
        print("Usuario creado correctamente.")
    else:
        print("No se completó el registro.")

#--------------------------------------------------------------------
#-----------------------Función Iniciar Seción-----------------------
#--------------------------------------------------------------------

def iniciar_sesion():
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")
    intentos_fallidos = 0

    for dni, data in usuarios.items():
        if data['usuario'] == usuario:
            while intentos_fallidos < 4:
                if data['clave'] == clave:
                    print(f"Bienvenido {usuario}!")
                    contenido = f"{usuario} ingresó el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    guardar_en_archivo("ingresos.txt", contenido)
                    return True
                else:
                    intentos_fallidos += 1
                    print(f"Contraseña incorrecta. Intento {intentos_fallidos}/4")
                    if intentos_fallidos == 4:
                        contenido = f"{usuario} bloqueado por múltiples intentos fallidos el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        guardar_en_archivo("log.txt", contenido)
                        print("Usuario bloqueado.")
                        return False
                    clave = input("Contraseña: ")
            break
    else:
        print("Usuario no encontrado.")
        return False


#----------------------------------------------------------------------------
#-----------------------Función Captcha de Verificaión-----------------------
#----------------------------------------------------------------------------

def captcha_verificacion():
    operaciones = [
        ('suma', aritmetica.sumar),
        ('resta', aritmetica.restar),
        ('multiplicación', aritmetica.multiplicar),
        ('división', aritmetica.dividir)
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

def guardar_en_archivo(ruta, contenido):
    try:
        with open(ruta, "a") as file:
            file.write(contenido)
    except Exception as e:
        print(f"No se pudo escribir en {ruta}. Error: {e}")

def olvidar_contrasena():
    pass  # Implementar si es necesario

def mostrar_menu():
    while True:
        bienvenida()
        print("\n1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Olvidé mi Contraseña")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if iniciar_sesion():
                print("Acceso concedido.")
            else:
                print("Acceso denegado.")
        elif opcion == "3":
            olvidar_contrasena()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

#---------------------------------------------------------------------
#-----------------------Función Guardar Archivo-----------------------
#---------------------------------------------------------------------

import os

# Definir la ruta de la carpeta
ruta_carpeta = r"C:\Users\marin\OneDrive\Desktop\Evidencia_1"

def guardar_en_archivo(nombre_archivo, contenido):
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    try:
        with open(ruta_archivo, "a") as file:
            file.write(contenido)
    except Exception as e:
        print(f"No se pudo escribir en {ruta_archivo}. Error: {e}")

#----------------------------------------------------------
#-----------------------Función Menú-----------------------
#----------------------------------------------------------

def mostrar_menu():
    while True:
        bienvenida()
        print("\n1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Olvidé mi Contraseña")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if iniciar_sesion():
                print("Acceso concedido.")
            else:
                print("Acceso denegado.")
        elif opcion == "3":
            olvidar_contrasena()  # Implementar según necesidad
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    mostrar_menu()
