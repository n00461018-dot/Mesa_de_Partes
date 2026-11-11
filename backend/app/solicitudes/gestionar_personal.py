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

    # Inicializar el cursor
    cursor = None

    try:
        # Crear el cursor para consultar MySQL
        cursor = conexion.cursor(dictionary=True)

        # Consultar trabajadores y sus areas
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

        # Ejecutar la consulta de trabajadores
        cursor.execute(consulta)

        # Guardar los resultados en una lista
        trabajadores = cursor.fetchall()

        # Mostrar trabajadores registrados
        print("\nTRABAJADORES REGISTRADOS")

        # Comprobar si existen trabajadores
        if not trabajadores:
            print("No hay trabajadores registrados.")
            return

        # Recorrer y mostrar los trabajadores
        for trabajador in trabajadores:
            print(
                f"{trabajador['id_usuario']} - "
                f"{trabajador['nombre']} "
                f"{trabajador['apellido']} - "
                f"Area: {trabajador['nombre_area'] or 'Sin area'}"
            )

        # Consultar las areas registradas
        consulta_areas = """
            SELECT
                id_area,
                nombre
            FROM area
            ORDER BY nombre
        """

        # Ejecutar la consulta de areas
        cursor.execute(consulta_areas)

        # Guardar las areas en una lista
        areas = cursor.fetchall()

        # Mostrar las areas disponibles
        print("\nAREAS DISPONIBLES")

        # Comprobar si existen areas
        if not areas:
            print("No hay areas registradas.")
            return

        # Recorrer y mostrar las areas
        for area in areas:
            print(
                f"{area['id_area']} - "
                f"{area['nombre']}"
            )

        # Solicitar el ID del trabajador
        id_trabajador = input(
            "\nIngrese el ID del trabajador que desea gestionar: "
        ).strip()

        # Validar que el ID ingresado sea numerico
        if not id_trabajador.isdigit():
            print("Error: El ID del trabajador debe ser numerico.")
            return

        # Convertir el ID ingresado a numero entero
        id_trabajador = int(id_trabajador)

        # Buscar al trabajador en la lista consultada
        trabajador_seleccionado = None

        # Recorrer los trabajadores para encontrar el ID
        for trabajador in trabajadores:
            if trabajador["id_usuario"] == id_trabajador:
                trabajador_seleccionado = trabajador
                break

        # Comprobar si se encontro al trabajador
        if trabajador_seleccionado is None:
            print("Error: El trabajador no esta registrado.")
            return

        # Mostrar los datos del trabajador seleccionado
        print(
            f"\nTrabajador seleccionado: "
            f"{trabajador_seleccionado['nombre']} "
            f"{trabajador_seleccionado['apellido']}"
        )

        # Mostrar el area actual del trabajador
        print(
            f"Area actual: "
            f"{trabajador_seleccionado['nombre_area'] or 'Sin area'}"
        )

        
        # Solicitar el ID del area de destino
        id_area = input(
            "\nIngrese el ID del area de destino: "
        ).strip()

        # Validar que el ID sea numerico
        if not id_area.isdigit():
            print("Error: El ID del area debe ser numerico.")
            return

        # Convertir el ID del area a numero entero
        id_area = int(id_area)

        # Buscar el area seleccionada
        area_seleccionada = None

        # Recorrer las areas registradas
        for area in areas:
            if area["id_area"] == id_area:
                area_seleccionada = area
                break

        # Comprobar si el area existe
        if area_seleccionada is None:
            print("Error: El area seleccionada no existe.")
            return

        # Mostrar el area de destino
        print(
            f"\nArea de destino: "
            f"{area_seleccionada['nombre']}"
        )
        
        
        # Comprobar si el trabajador ya pertenece al area seleccionada
        if trabajador_seleccionado["id_area"] == id_area:
            print(
                "\nEl trabajador ya pertenece al area seleccionada."
            )
            return

        # Mostrar el resumen del cambio solicitado
        print("\nRESUMEN DEL CAMBIO DE AREA")

        print(
            f"Trabajador: "
            f"{trabajador_seleccionado['nombre']} "
            f"{trabajador_seleccionado['apellido']}"
        )

        print(
            f"Area actual: "
            f"{trabajador_seleccionado['nombre_area'] or 'Sin area'}"
        )

        print(
            f"Area nueva: "
            f"{area_seleccionada['nombre']}"
        )

        
        # Solicitar confirmacion para cambiar el area
        confirmacion = input(
            "\n¿Desea confirmar el cambio de area? (S/N): "
        ).strip().upper()

        # Validar que la respuesta sea correcta
        if confirmacion not in ("S", "N"):
            print("Error: Debe ingresar S o N.")
            return

        # Cancelar la operacion si el administrador responde N
        if confirmacion == "N":
            print("Operacion cancelada. No se realizaron cambios.")
            return

        # Informar que la solicitud fue confirmada
       print("\nSolicitud confirmada. Procesando cambio de area...")

        
        # Preparar la consulta para actualizar el area del trabajador
        consulta_actualizar = """
            UPDATE usuario
            SET id_area = %s
            WHERE id_usuario = %s
            AND id_rol = 2
        """

        # Ejecutar la actualizacion con los datos seleccionados
        cursor.execute(
            consulta_actualizar,
            (id_area, id_trabajador)
        )

        # Comprobar si se actualizo un trabajador
        if cursor.rowcount == 0:
            conexion.rollback()
            print("No se pudo actualizar el area del trabajador.")
            return

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Mostrar mensaje de actualizacion exitosa
        print("\nArea del trabajador actualizada correctamente.")

        # Mostrar el resultado final
        print(
            f"Trabajador: "
            f"{trabajador_seleccionado['nombre']} "
            f"{trabajador_seleccionado['apellido']}"
        )

        print(
            f"Nueva area: {area_seleccionada['nombre']}"
        )
 

    # Capturar los errores de MySQL
    except Error as error:
        conexion.rollback()
        print(f"Error al consultar trabajadores y areas: {error}")

    # Cerrar los recursos utilizados
    finally:

        # Cerrar el cursor si fue creado
        if cursor is not None:
            cursor.close()

        # Cerrar la conexion con MySQL
        conexion.close()
