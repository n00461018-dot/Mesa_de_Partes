
from database.conexion_bd import conectar_bd
from mysql.connector import Error
from solicitudes.extra import titulo_menu


def gestionar_personal_areas(usuario):

    # Validar que el usuario sea administrador
    if usuario["id_rol"] != 1:
        print("No tiene permisos para gestionar personal.")
        return

    # Mostrar el titulo de la funcion
    titulo_menu("Gestion de personal y areas")

    # Crear la conexion con MySQL
    conexion = conectar_bd()

    # Comprobar si la conexion fallo
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = None

    try:
        # Crear el cursor para consultar MySQL
        cursor = conexion.cursor(dictionary=True)

        # Consultar trabajadores y sus áreas
        consulta = """
            SELECT
                u.id_usuario,
                u.nombre,
                u.apellido,
                u.id_area,
                a.nombre AS nombre_area
            FROM usuario u
            LEFT JOIN area a
                ON u.id_area = a.id_area
            WHERE u.id_rol = 2
            ORDER BY u.apellido, u.nombre
        """

        cursor.execute(consulta)

        # Guardar los resultados en una lista
        trabajadores = cursor.fetchall()

        # Mostrar trabajadores registrados
        print("\nTRABAJADORES REGISTRADOS")

        for trabajador in trabajadores:
            print(
                f"{trabajador['id_usuario']} - "
                f"{trabajador['nombre']} "
                f"{trabajador['apellido']} - "
                f"Área: {trabajador['nombre_area'] or 'Sin área'}"
            )

        # Consultar las áreas registradas
        consulta_areas = """
            SELECT
                id_area,
                nombre
            FROM area
            ORDER BY nombre
        """

        # Ejecutar la consulta
        cursor.execute(consulta_areas)

        # Guardar las áreas en una lista
        areas = cursor.fetchall()

        # Mostrar las áreas disponibles
        print("\nÁREAS DISPONIBLES")

        for area in areas:
            print(
                f"{area['id_area']} - "
                f"{area['nombre']}"
            )

    except Error as error:
        print(f"Error al consultar trabajadores y áreas: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
