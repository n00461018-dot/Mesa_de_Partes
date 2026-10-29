import mysql.connector
from mysql.connector import Error


# CONEXIÓN A LA BASE DE DATOS
def conectar_bd():
    # Se intenta conectar a MySQL; si falla se avisa y se devuelve None
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",          
            password="12345",     
            database="mesa_de_partes",
        )
    except Error as e:
        print(f"\n[!] Error al conectar con la base de datos MySQL: {e}")
        return None