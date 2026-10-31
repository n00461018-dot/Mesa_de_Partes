#Conexion a la base de datos
from datetime import datetime
from database.conexion_bd import conectar_bd

def registrar_documento(usuario):
    conexion = conectar_bd()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conexion.cursor()

