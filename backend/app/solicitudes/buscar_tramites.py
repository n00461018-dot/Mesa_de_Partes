# Importa funciones auxiliares, constantes de roles, conexión a BD y tabla de reportes
from solicitudes.extra import titulo_menu, ROL_TRABAJADOR, validar_dni, validar_lista_vacia
from solicitudes.reportes import rep_mostrar_tabla
from database.conexion_bd import conectar_bd
from mysql.connector import Error


# [T.D] Crear función con una consulta SQL aplicando el filtro estricto por el ID del área del trabajador y los filtros aplicados
def consultar_tramites_por_criterio(conexion, id_area, criterio, valor):
    try:
        cursor = conexion.cursor(dictionary=True)

        # Base de la consulta uniendo expedientes, ciudadanos, tipos de trámite, estados y área
        query = """
            SELECT e.id_expediente, e.numero_expediente, tp.nombre_tramite AS tipo_tramite,
                   CONCAT(c.nombre, ' ', c.apellido) AS ciudadano, c.dni, c.correo,
                   e.asunto, e.fecha_registro, est.nombre_estado AS estado,
                   a.nombre_area AS area, e.id_area
            FROM expediente e
            INNER JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
            INNER JOIN tipo_tramite tp ON e.id_tipo_tramite = tp.id_tipo_tramite
            INNER JOIN estado est ON e.id_estado = est.id_estado
            INNER JOIN area a ON e.id_area = a.id_area
            WHERE e.id_area = %s
        """

        # Parámetros iniciales con el filtro obligatorio del área del trabajador
        params = [id_area]

        # Aplicación dinámica del filtro según la opción elegida por el usuario
        if criterio == "código":
            query += " AND e.numero_expediente LIKE %s"
            params.append(f"%{valor}%")
        elif criterio == "asunto":
            query += " AND e.asunto LIKE %s"
            params.append(f"%{valor}%")
        elif criterio == "dni":
            query += " AND c.dni = %s"
            params.append(valor)
        elif criterio == "correo":
            query += " AND c.correo LIKE %s"
            params.append(f"%{valor}%")

        # Ordena los expedientes de forma descendente por fecha de registro (más reciente primero)
        query += " ORDER BY e.fecha_registro DESC"

        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    except Error as error:
        print(f"Error al consultar la base de datos: {error}")
        return []


# [T.D] Crear función para integrar la validación de aviso en consola y manejar los casos donde la consulta devuelva cero resultados.
def manejar_sin_resultados(resultados, criterio, valor_busqueda):
    mensaje = f"No se encontraron trámites en tu área con {criterio}: '{valor_busqueda}'."
    if validar_lista_vacia(resultados, mensaje):
        input("\nPresione Enter para intentar con otra búsqueda.")
        return True
    return False


# [T.D] Crear función para adaptar el resultado en el formato de tabla de rep_mostrar_tabla y mostrar los expedientes encontrados ordenadamente.
def adaptar_resultados_tabla(resultados):
    tramites_adaptados = []

    # Se conserva el orden proveniente de la consulta (fecha_registro DESC)
    for r in resultados:
        tramite = {
            "numero_expediente": r["numero_expediente"],
            "tipo_tramite": r["tipo_tramite"],
            "fecha_registro": r["fecha_registro"],
            "area": r["area"],
            "estado": r["estado"],
        }
        tramites_adaptados.append(tramite)

    return tramites_adaptados


# [T.D] Procesar la captura de la búsqueda exacta o parcial que el usuario desea encontrar según la opción elegida en el submenú.
def capturar_valor_busqueda(opcion):
    etiquetas = {
        1: ("código", "Ingrese el código de expediente (exacto o parcial): "),
        2: ("asunto", "Ingrese el asunto o palabra clave: "),
        3: ("dni", "Ingrese el DNI del ciudadano (8 dígitos): "),
        4: ("correo", "Ingrese el correo del ciudadano: "),
    }

    criterio, mensaje = etiquetas[opcion]

    while True:
        valor = input(f"\n{mensaje}").strip()

        # Evita búsquedas vacías o con solo espacios en blanco
        if not valor:
            print("Aviso: El campo de búsqueda no puede estar vacío.")
            continue

        # Si el criterio es DNI, reutiliza la validación estricta de extra.py
        if criterio == "dni":
            error_dni = validar_dni(valor)
            if error_dni is not None:
                print(f"Aviso: {error_dni}")
                continue

        return criterio, valor


# [T.D] Crear función con un submenú interactivo donde se seleccione el criterio específico de búsqueda
def buscar_tramites_area(usuario):

    # Verifica que el usuario tenga rol de trabajador y un área asignada
    if usuario.get("id_rol") != ROL_TRABAJADOR or usuario.get("id_area") is None:
        print("Acceso denegado. Esta opción es exclusiva para trabajadores con área asignada.")
        return

    # Bucle interactivo del submenú de búsqueda
    while True:
        titulo_menu("Buscar trámites de mi área")
        if usuario.get("nombre_area") is not None:
            print(f"Área: {usuario['nombre_area']}")
        print("-" * 50)
        print(" 1. Buscar por código de expediente")
        print(" 2. Buscar por asunto")
        print(" 3. Buscar por DNI del ciudadano")
        print(" 4. Buscar por correo del ciudadano")
        print(" 5. Volver al menú")

        eleccion = input("\nSeleccione una opción: ").strip()

        # Valida que la opción ingresada sea un número válido dentro del rango
        if not eleccion.isdigit() or not 1 <= int(eleccion) <= 5:
            input("\nOpción no válida. Presione Enter para reintentar.")
            continue

        opcion = int(eleccion)

        if opcion == 5:
            return

        # Captura y valida el valor según el criterio elegido
        criterio, valor_busqueda = capturar_valor_busqueda(opcion)

        # Establecer conexión a la base de datos para ejecutar la consulta
        conexion = conectar_bd()
        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            input("\nPresione Enter para continuar.")
            continue

        try:
            # Ejecuta la consulta SQL aplicando el filtro estricto por el ID del área del trabajador
            resultados = consultar_tramites_por_criterio(
                conexion, usuario["id_area"], criterio, valor_busqueda
            )

            # Valida si la consulta devolvió cero resultados
            if manejar_sin_resultados(resultados, criterio, valor_busqueda):
                continue

            # Adapta los resultados al formato esperado por rep_mostrar_tabla y los imprime ordenadamente
            tramites_tabla = adaptar_resultados_tabla(resultados)
            titulo_menu("Resultados de búsqueda")
            print(f"Criterio: {criterio} | Búsqueda: '{valor_busqueda}' | Orden: Fecha (más reciente primero)\n")
            rep_mostrar_tabla(tramites_tabla)
            input("\nPresione Enter para continuar.")

        finally:
            conexion.close()