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


except Exception as e:
    print("algo")