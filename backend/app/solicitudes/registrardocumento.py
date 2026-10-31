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

        #Recuperamos el ID que MSQL acaba de generar para este expediente
        id_expediente = cursor.lastrowid

        nombre_archivo = input("Nombre del archivo adjunto (ej. dni.pdf): ")
        
        sql_doc = "INSERT INTO documento (nombre_archivo, tipo_documento, fecha_subida, id_expediente) VALUES (%s, 'PDF', %s, %s)"
        cursor.execute(sql_doc, (nombre_archivo, fecha_actual, id_expediente))

        sql_seg = "INSERT INTO seguimiento (fecha, estado, observacion, id_usuario, id_expediente) VALUES (%s, 'Registrado', 'Trámite registrado por el ciudadano', %s, %s)"
        cursor.execute(sql_seg, (fecha_actual, usuario["id_usuario"], id_expediente))

        # Confirmamos que los tres registros se guarden permanentemente
        conexion.commit() #Guarda los cambios
        print(f"\n¡Éxito! Su trámite fue registrado con el número: {numero_expediente}")

    except Exception as e:
        # Si algo falla, deshacemos todos los cambios para no dejar datos incompletos
        conexion.rollback() #Revierte si hay error
        print(f"\nError al registrar el documento: {e}")

    # Aquí es donde se usa 'cursor' para cerrarlo de forma segura
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()