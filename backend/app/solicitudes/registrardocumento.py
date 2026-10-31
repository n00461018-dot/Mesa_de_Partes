#Conexion a la base de datos
from datetime import datetime

from database.conexion_bd import conectar_bd

def registrar_documento(usuario):
    conexion = conectar_bd()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conexion.cursor()

    #Captura de datos del documento
    try:
        print("=== NUEVO TRAMITE ===")
        asunto = input("Ingrese el asunto del trámite: ")
        id_tipo = input("Ingrese el ID del tipo de trámite (son de 6 digitos): ")

        # Generar el número de expediente
        año_actual = datetime.now().year
        cursor.execute("SELECT COUNT(*) FROM expediente WHERE YEAR(fecha_creacion) = %s",(año_actual,))
        cantidad = cursor.fetchone()[0] + 1
        numero_expediente = f"{año_actual}-{cantidad:05d}"

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Guardamos el registro principal
        id_ciudadano = 1            # Reemplaza por la consulta real
        sql_expediente = """
            INSERT INTO expediente (numero_expediente, fecha_registro, asunto, estado, id_ciudadano, id_tipo_tramite, id_area)
            VALUES (%s, %s, %s, 'Registrado', %s, %s, 1)
        """

        cursor.execute(sql_expediente, (numero_expediente, fecha_actual, asunto, id_ciudadano, id_tipo))

        id_expediente = cursor.lastrowid


    except Exception as e:
        print("algo")

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()