from datetime import datetime
from mysql.connector import Error
from database.conexion_bd import *
from database.consultas_bd import *
from solicitudes.extra import *

#Declarar la constante del id de area inicial y estado inicial del trámite
ID_AREA_MESA_PARTES = 1
ESTADO_INICIAL = "Registrado"

#Declarar constantes de mínimo y máximo adjuntos en trámite
MIN_ADJUNTOS = 1
MAX_ADJUNTOS = 10

#PEDIR DATOS PARA EL TRÁMITE   ################################################################################################

#Función para obtener datos del solicitante (ciudadano) al registrar un trámite
def reg_tramite_solicitante(conexion, usuario):
    #Se coloca el título de la pantalla
    titulo_menu("Registrar trámite - Solicitante")

    #Si el solicitante tiene rol ciudadano (dni registrado) se aplicará la funcion buscar_ciudadano_por_dni
    if usuario["id_rol"] == ROL_CIUDADANO:
        # El ciudadano registra a su nombre: se busca con su propio DNI
        ciudadano = buscar_ciudadano_por_dni(conexion, usuario["dni"])
        return ciudadano

    #Usuario con otro rol va a registrar el dni del ciudadano por consola
    while True:
        #Se coloca el título de la pantalla
        titulo_menu("Registrar trámite - Solicitante")

        dni = input("Ingresar el DNI del ciudadano solicitante (Enter para cancelar): ").strip()
        
        #Si no ingresa datos la función reg_tramite_solicitante devuelve None
        if dni == "":
            return None
        
        #Se valida el dni ingresado por consola
        error = validar_dni(dni)
        if error:
            #Si la validación encuentra un error (contiene un valor) se mostrará un mensaje con el error
            print(f"\nError: {error}")
            input("\nPresione Enter para continuar...")
            #Volverá al bucle While desde el inicio
            continue

        #Si pasa las validaciones se extraen los datos del ciudadano por dni en un diccionario "ciudadano"
        ciudadano = buscar_ciudadano_por_dni(conexion, dni)

        #Si no se encuentran datos de ciudadano en la BD se mostrará un mensaje y se volverá a iniciar el bucle
        if ciudadano is None:
            print("\n Error: No existe un ciudadano registrado con ese DNI.")
            input("\nPresione Enter para continuar...")
            continue

        #Si se encuentran datos de ciudadano la función devuelve la información 
        return ciudadano


def reg_tramite_generar_codigo(cursor):
    #Se crea el prefijo del código del trámite: "2026-"
    prefijo = f"{datetime.now().year}-"

    #Se extrae el máximo número de expediente registrado con el prefijo en la tabla expediente 
    cursor.execute("""
        SELECT MAX(numero_expediente) AS ultimo_codigo_bd 
        FROM expediente 
        WHERE numero_expediente LIKE %s
        FOR UPDATE
    """, (prefijo + "%",))

    #Del diccionario cursor se extrae el valor de la clave "ultimo_codigo_bd"
    #El cual guarda el último código registrado en la bd y se pasa a la variable ultimo_codigo
    ultimo_codigo = cursor.fetchone()["ultimo_codigo_bd"]

    if ultimo_codigo is None:
        #Si no existen códigos registrados se empieza el número en uno
        numero_codigo = 1
    else:
        #Si ya hay registro se extrae el número y se suma 1
        #Se usa rsplit para dividir el prefijo del número y se convierte a entero para sumarle 1
        numero_codigo = int(ultimo_codigo.split("-")[1]) + 1

    #Se aplica fstring para juntar el prefijo con el numero obtenido
    codigo_tramite=f"{prefijo}{numero_codigo:05d}"

    #La función devuelve el código del trámite generado
    return codigo_tramite


