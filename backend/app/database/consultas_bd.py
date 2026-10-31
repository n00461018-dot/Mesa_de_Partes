#Insertar consultas a la BD usadas en las funciones del sistema


# Devuelve la lista de tipos de trámite (id, nombre y descripción que contiene los requisitos)
def listar_tipos_tramite(conexion):
    #Crear un cursor como diccionario
    cursor = conexion.cursor(dictionary=True)
    try:
        #Extraer la lista de tipos de trámite ordenados por id_tipo_tramite
        #Las llaves seran id_tipo_tramite, nombre y descripcion
        cursor.execute("""
            SELECT id_tipo_tramite, nombre, descripcion
            FROM tipo_tramite
            ORDER BY id_tipo_tramite
        """)
        return cursor.fetchall()
    finally:
        cursor.close()