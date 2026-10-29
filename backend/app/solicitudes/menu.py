from solicitudes.extra import titulo_menu
from solicitudes.ciudadanos import menu_ciudadanos
from database.conexion_bd import conectar_bd
from seguimiento.routes import menu_seguimiento, menu_cambio_estado
from seguimiento.derivacion import derivar_expediente_area
# FUNCIÓN PARA CONSULTAR SEGUIMIENTO DE EXPEDIENTES
def ejecutar_seguimiento(usuario):

    conexion = conectar_bd()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        menu_seguimiento(
            conexion,
            usuario["id_usuario"]
        )

    except Exception as error:
        print("Error en el seguimiento:", error)

    finally:
        conexion.close()


# FUNCIÓN PARA CAMBIAR EL ESTADO DE UN EXPEDIENTE
def ejecutar_cambio_estado(usuario):

# FUNCIÓN PARA DERIVAR EXPEDIENTES ENTRE ÁREAS
 def ejecutar_derivacion(usuario):
    conexion = conectar_bd()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        derivar_expediente_area(
            conexion,
            usuario["id_usuario"]
        )

    except Exception as error:
        print("Error en la derivación:", error)

    finally:
        conexion.close()

    # Solo administrador y trabajador
    if usuario["id_rol"] not in (1, 2):
        print("No tiene permiso para cambiar estados.")
        return

    conexion = conectar_bd()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        menu_cambio_estado(
            conexion,
            usuario["id_usuario"]
        )

    except Exception as error:
        print("Error al cambiar el estado:", error)

    finally:
        conexion.close()

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
        "Derivar trámites": lambda conexion, usuario: derivar_expediente_area(conexion, usuario['id_usuario']),
        "Registrar personal": "Ingresar el nombre de la funcion",
        "Gestionar ciudadanos":menu_ciudadanos,
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

        #Cualquier otra opción busca su función en el diccionario
        opcion_seleccionada = opciones[numero - 1]
        funcion_menu = funciones_menu.get(opcion_seleccionada)

        if callable(funcion_menu):
            funcion_menu()
        else:
            titulo_menu(opcion_seleccionada)
            print(f"[Pruebas] {funcion_menu}")
            input("\nPresione Enter para regresar al menú.")