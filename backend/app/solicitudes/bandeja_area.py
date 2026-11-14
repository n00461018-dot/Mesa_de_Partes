
# Permite capturar y manejar errores relacionados con MySQL.
from mysql.connector import Error

# Importa funciones auxiliares para validar listas vacías y mostrar títulos.
from solicitudes.extra import validar_lista_vacia, titulo_menu

# Importa la función que establece la conexión con la base de datos MySQL.
from database.conexion_bd import conectar_bd

# Importa la consulta SQL que obtiene los expedientes del área del trabajador autenticado.
from database.consultas_bd import consultar_expedientes_mi_area



#Implementar la función principal encargada de procesar la lista de trámites obtenida de la BD usando las funciones validar_lista_vacia y bandeja_mostrar_tabla




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