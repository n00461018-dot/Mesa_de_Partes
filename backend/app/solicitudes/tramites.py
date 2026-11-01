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