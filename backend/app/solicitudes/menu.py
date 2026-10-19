from extra import titulo_menu

import os
import sys

# Esto sube un nivel desde 'solicitudes' hasta la carpeta 'app' para ubicar 'auth'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#Importar funciones de login.py
from auth.login import *



#ROLES Y OPCIONES DEL MENÚ

def nombre_del_rol(id_rol):
    if id_rol == 1:
        return "Administrador"
    elif id_rol == 2:
        return "Trabajador"
    elif id_rol == 3:
        return "Ciudadano"
    return "Desconocido"

#Funcion opciones_rol
#Lista de opciones según el rol
def opciones_rol(id_rol):

    if id_rol == 1:  # Administrador
        return [
            "Derivar trámites",
            "Registrar personal",
            "Gestionar personal y áreas (cambiar área, crear usuarios)",
            "Reportes (trámites por área y estado, historial de acciones)",
            "Buscar trámites de todas las áreas (documento, expediente o estado)",
            "Cerrar sesión",
        ]
    elif id_rol == 2:  # Trabajador
        return [
            "Bandeja de mi área",
            "Buscar trámites",
            "Cerrar sesión",
        ]
    elif id_rol == 3:  # Ciudadano
        return [
            "Registrar trámite",
            "Mis trámites y búsqueda (expediente o estado)",
            "Cerrar sesión",
        ]
    return []


#MENÚ DINÁMICO SEGÚN EL ROL


def ejecutar_menu(usuario):

    #Se obtienen las opciones que corresponden al diccionario

    opciones = opciones_rol(usuario["id_rol"])
    #Si el rol no existe, no hay opciones y se sale del menú
    if len(opciones) == 0:
        print("Su usuario tiene un rol no reconocido.")
        input("\nPresione Enter para continuar.")
        return

    #Se guardan el nombre del rol y el nombre completo para mostrarlos en el menú de usuario
    rol_nombre = nombre_del_rol(usuario["id_rol"])
    nombre_completo = f"{usuario['nombre']} {usuario['apellido']}"

    #Bucle para ael menú hasta que el usuario cierre sesión
    while True:
        #Se muestra el encabezado con el título, el usuario y su área (si tiene)
        titulo_menu(f"Menú {rol_nombre}")
        print(f"Usuario: {nombre_completo}")
        if usuario["nombre_area"] is not None:
            print(f"Área: {usuario['nombre_area']}")
        print("-" * 50)


        #Se imprimen las opciones numeradas desde el número 1 (i+1)
        for i in range(len(opciones)):
            print(f" {i + 1}. {opciones[i]}")



        #Se pide la opción y se valida que sea un número dentro del rango
        eleccion = input("\nSeleccione una opción: ").strip()

        #Si la opción escogida no es un número o no está en el rango de opciones se mostrará un error
        if not eleccion.isdigit() or not 1 <= int(eleccion) <= len(opciones):

            input("\nOpción no válida. Presione Enter para reintentar.")
            #Se regresa al inicio del Bucle
            continue


        #La última opción siempre es Cerrar sesión: Se vuelve al login
        numero = int(eleccion)
        if numero == len(opciones):
            titulo_menu("Salida")
            print("Sesión terminada.")
            input("\nPresione Enter para continuar.")
            return

        #Cualquier otra opción muestra una pantalla temporal hasta que se programe
        titulo_menu(opciones[numero - 1])
        print(f"[En desarrollo] Funcionalidad para: {opciones[numero - 1]}")
        input("\nPresione Enter para regresar al menú.")



#FUNCION PRINCIPAL PARA EL MENÚ

def main():
    #Las funciones de pantalla_login y ejecutar_menu se repiten al cerrar sesión
    while True:
        #Se pide el login; si el usuario escribe 'salir' devuelve None
        usuario = pantalla_login()
        if usuario is None:
            titulo_menu("Salida")
            print("El sistema se ha cerrado correctamente.")
            break
        #Si el login fue correcto, se abre el menú según su rol
        ejecutar_menu(usuario)

#Si el archivo es menu.py ejecutar el main() directamente
if __name__ == "__main__":
    main()
