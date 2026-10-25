from solicitudes.extra import titulo_menu



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
            "Registrar trámite",
            "Derivar trámites",
            "Registrar personal",
            "Gestionar ciudadanos",
            "Gestionar personal y áreas",
            "Reportes (trámites por área y estado)",
            "Buscar trámites de todas las áreas",
            "Cerrar sesión",
        ]
    elif id_rol == 2:  # Trabajador
        return [
            "Registrar trámite",
            "Bandeja de mi área",
            "Buscar trámites",
            "Derivar trámites",
            "Cerrar sesión",
        ]
    elif id_rol == 3:  # Ciudadano
        return [
            "Registrar trámite",
            "Mis trámites",
            "Cerrar sesión",
        ]
    return []


# Diccionario con funciones de prueba para cada opción
funciones_menu = {

        "Registrar trámite": "Ingresar el nombre de la funcion",
        "Derivar trámites": "Ingresar el nombre de la funcion",
        "Registrar personal": "Ingresar el nombre de la funcion",
        "Gestionar ciudadanos":"Ingresar el nombre de la funcion",
        "Gestionar personal y áreas": "Ingresar el nombre de la funcion",
        "Reportes (trámites por área y estado)": "Ingresar el nombre de la funcion",
        "Buscar trámites de todas las áreas": "Ingresar el nombre de la funcion",
        "Bandeja de mi área": "Ingresar el nombre de la funcion",
        "Buscar trámites": "Ingresar el nombre de la funcion",
        "Mis trámites": "Ingresar el nombre de la funcion"
    }


#MENÚ DINÁMICO SEGÚN EL ROL

#Función ejecutar_menu con parámetro diccionario
def ejecutar_menu(usuario):

    #Se obtienen las opciones que corresponden al diccionario usuario
    opciones = opciones_rol(usuario["id_rol"])
    #Si el rol no existe, no hay opciones y se sale del menú
    if len(opciones) == 0:
        print("Su usuario tiene un rol no reconocido.")
        input("\nPresione Enter para continuar.")
        return

    #En caso tenga rol se guarda el nombre del rol y el nombre completo para mostrarlos en el menú de usuario
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

        #Cualquier otra opción muestra una pantalla con la opción seleccionada
        opcion_seleccionada = opciones[numero - 1]
        titulo_menu(opcion_seleccionada)

        funcion_menu = funciones_menu.get(opcion_seleccionada)

        if funcion_menu:
            print(f"[Pruebas] {funcion_menu}")
        else:
            print("No existe la opción seleccionada, vuelva a intentarlo.")        
        
        input("\nPresione Enter para regresar al menú.")
