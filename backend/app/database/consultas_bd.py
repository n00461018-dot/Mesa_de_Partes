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



#Función para obtener los trámites con su tipo, fecha, área actual y estado en una lista de diccionarios
def consultar_tramites(conexion):

    #Se establece el cursor para extraer los datos como diccionario
    with conexion.cursor(dictionary=True) as cursor:
        #Se realiza el select de numero_expediente, tipo_tramite, fecha_registro, area y estado
        cursor.execute("""
            SELECT e.numero_expediente, tt.nombre AS tipo_tramite,
                   e.fecha_registro, a.nombre AS area, e.estado
            FROM expediente e
            INNER JOIN tipo_tramite tt ON e.id_tipo_tramite = tt.id_tipo_tramite
            INNER JOIN area a ON e.id_area = a.id_area
        """)

        #Se devuelve todos los diccionarios obtenidos en una lista de diccionarios
        return cursor.fetchall()
    


# HU - Bandeja de mi área
# Obtiene expedientes del área del trabajador autenticado
def consultar_expedientes_mi_area(conexion, id_usuario):
    cursor = conexion.cursor(dictionary=True)
    try:
        sql = """
            SELECT
                e.numero_expediente,
                CONCAT(uc.nombre, ' ', uc.apellido) AS ciudadano,
                e.asunto,
                e.fecha_registro,
                e.estado
            FROM expediente e
            INNER JOIN ciudadano c
                ON e.id_ciudadano = c.id_ciudadano
            INNER JOIN usuario uc
                ON c.id_usuario = uc.id_usuario
            WHERE e.id_area = (
                SELECT u.id_area
                FROM usuario u
                WHERE u.id_usuario = %s
                  AND u.id_rol = 2
                  AND u.id_area IS NOT NULL
            )
            ORDER BY e.fecha_registro DESC
        """
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchall()
    finally:
        cursor.close()
