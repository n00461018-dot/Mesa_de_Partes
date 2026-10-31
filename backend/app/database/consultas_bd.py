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


#Funcion que devuelve los datos de un ciudadano con su DNI
def buscar_ciudadano_por_dni(conexion, dni):
    #Crear un cursor como diccionario
    cursor = conexion.cursor(dictionary=True)
    try:
        #Extraer los datos del ciudadano y su usuario usando el DNI
        #Las llaves del cursor serán id_ciudadano de la tabla ciudadano, id_usuario, nombre, apellido y correo de la tabla usuario
        cursor.execute("""
            SELECT c.id_ciudadano, u.id_usuario, u.nombre, u.apellido, u.correo
            FROM ciudadano c
            INNER JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE u.dni = %s
        """, (dni,))
        return cursor.fetchone()
    finally:
        cursor.close()