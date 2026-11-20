
# Permite capturar y manejar errores relacionados con MySQL.
from mysql.connector import Error

# Importa funciones auxiliares para validar listas vacías y mostrar títulos.
from solicitudes.extra import validar_lista_vacia, titulo_menu

# Importa la función que establece la conexión con la base de datos MySQL.
from database.conexion_bd import conectar_bd

# Importa la consulta SQL que obtiene los expedientes del área del trabajador autenticado.
from database.consultas_bd import consultar_expedientes_mi_area



#Implementar la función principal encargada de procesar la lista de trámites obtenida de la BD usando las funciones validar_lista_vacia y bandeja_mostrar_tabla



# Función principal que muestra los expedientes del área del trabajador autenticado.
def bandeja_mi_area(usuario):

    # Verifica que el usuario tenga el rol de trabajador.
    if usuario["id_rol"] != 2:
        print("Acceso denegado. Solo trabajadores.")
        return

    # Establece la conexión con la base de datos MySQL.
    conexion = conectar_bd()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        # Muestra el encabezado de la bandeja.
        titulo_menu("Bandeja de mi área")

        # Obtiene los expedientes del área del usuario autenticado.
        expedientes = consultar_expedientes_mi_area(
            conexion, usuario["id_usuario"]
        )

        # Verifica si la consulta devolvió expedientes.
        if validar_lista_vacia(
            expedientes, "No hay expedientes en tu área."
        ):
            return

        # Muestra los expedientes utilizando la tabla existente.
        bandeja_mostrar_tabla(expedientes)

    # Captura los errores que puedan ocurrir en MySQL.
    except Error as error:
        print(f"Error al consultar la bandeja: {error}")

    finally:
        # Cierra la conexión para liberar recursos.
        conexion.close()




#Funcion para mostrar en pantalla una tabla con formatos y valores obtenidos de una lista de diccionarios como parámetro
def bandeja_mostrar_tabla(expedientes):

    #Se muestra el encabezado de la tabla con los valores asociados a los expedientes o trámites
    print(f"{'Código':<10} | {'Ciudadano':<22} | {'Asunto':<30} | {'Fecha':<16} | {'Estado':<12}")
    print("-" * 102)

    #Se recorre cada diccionario que contiene expediente extrayendo sus datos en variables
    for e in expedientes:
        codigo = e["numero_expediente"]
        ciudadano = e["ciudadano"][:22]
        asunto = e["asunto"][:30]
        #Se usa un fstring para mostrar la fecha
        fecha = e["fecha_registro"].strftime("%d/%m/%Y %H:%M")
        estado = e["estado"]

        print(f"{codigo:<10} | {ciudadano:<22} | {asunto:<30} | {fecha:<16} | {estado:<12}")

    print("-" * 102)
    
    #Se guarda el total de expedientes en una variable y se muestra en pantalla
    total_expedientes = len(expedientes)
    print(f"Total de expedientes encontrados: {total_expedientes}")