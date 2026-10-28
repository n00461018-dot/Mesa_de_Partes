from mysql.connector import Error
from solicitudes.extra import titulo_menu
from database.conexion_bd import conectar_bd


# ==============================================================================
# VALIDACIONES DE FORMATO Y DUPLICADOS
# ==============================================================================

def validar_formato_ciudadano(dni, nombre, apellido, correo, contrasena, telefono):
    # Verificar que los campos obligatorios no estén vacíos
    if (
        dni == ""
        or nombre == ""
        or apellido == ""
        or correo == ""
        or contrasena == ""
        or telefono == ""
    ):
        print("\n[!] Error: Todos los campos obligatorios deben ser completados.")
        return False

    # En la BD el DNI tiene 8 dígitos numéricos
    if not (dni.isdigit() and len(dni) == 8):
        print("\n[!] Formato inválido: El DNI debe contener exactamente 8 dígitos numéricos.")
        return False

    # El correo debe contener un @, un punto (.), sin espacios y al menos 6 caracteres
    es_correo = (
        "@" in correo
        and "." in correo
        and " " not in correo
        and len(correo) >= 6
    )
    if not es_correo:
        print("\n[!] Formato inválido: Ingrese un correo electrónico válido.")
        return False

    # En la BD el teléfono es VARCHAR(15) NOT NULL (entre 7 y 15 dígitos numéricos)
    if not (telefono.isdigit() and 7 <= len(telefono) <= 15):
        print("\n[!] Formato inválido: El teléfono debe contener entre 7 y 15 dígitos numéricos.")
        return False

    return True


def verificar_duplicado(dni, correo):
    # Consulta si el DNI o el correo ya existen en la tabla 'usuario'
    # Devuelve True si hay duplicado, False si está disponible o None si hubo error de BD
    conexion = conectar_bd()
    if conexion is None:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT dni, correo FROM usuario WHERE dni = %s OR correo = %s"
        cursor.execute(sql, (dni, correo))
        registro = cursor.fetchone()

        if registro is not None:
            if registro["dni"] == dni:
                print(f"\n[!] Error: Ya existe un usuario registrado con el DNI {dni}.")
            elif registro["correo"].lower() == correo.lower():
                print(f"\n[!] Error: El correo '{correo}' ya se encuentra registrado.")
            return True

        return False

    except Error as e:
        print(f"\n[!] Error al verificar duplicados en la base de datos: {e}")
        return None
    finally:
        # Siempre se cierran el cursor y la conexión
        if cursor is not None:
            cursor.close()
        conexion.close()


# ==============================================================================
# FUNCIONES DE BASE DE DATOS (REGISTRAR Y CONSULTAR CIUDADANOS)
# ==============================================================================

def registrar_ciudadano_bd(dni, nombre, apellido, correo, contrasena, telefono, direccion):
    # Inserta primero en 'usuario' (id_rol = 3 para Ciudadano) y luego en 'ciudadano'
    conexion = conectar_bd()
    if conexion is None:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()

        # 1. Insertar datos generales en la tabla 'usuario' (id_rol = 3 -> Ciudadano, id_area = NULL)
        sql_usuario = """
            INSERT INTO usuario (dni, nombre, apellido, correo, contrasena, id_rol, id_area)
            VALUES (%s, %s, %s, %s, %s, 3, NULL)
        """
        cursor.execute(sql_usuario, (dni, nombre, apellido, correo, contrasena))
        id_usuario_nuevo = cursor.lastrowid

        # Si la dirección se dejó en blanco, se guarda como NULL en la BD
        direccion_bd = direccion if direccion != "" else None

        # 2. Insertar datos de contacto en la tabla 'ciudadano'
        sql_ciudadano = """
            INSERT INTO ciudadano (telefono, direccion, id_usuario)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_ciudadano, (telefono, direccion_bd, id_usuario_nuevo))

        # Confirmar ambas inserciones en la base de datos
        conexion.commit()
        return True

    except Error as e:
        # Si ocurre algún problema, se deshacen los cambios para no dejar registros incompletos
        conexion.rollback()
        print(f"\n[!] Error al registrar al ciudadano: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def consultar_ciudadano_por_dni(dni):
    # Busca a un ciudadano por su DNI y cuenta sus expedientes registrados
    # Devuelve un diccionario con los datos, None si no existe o False si hubo error de BD
    conexion = conectar_bd()
    if conexion is None:
        return False

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT c.id_ciudadano, u.id_usuario, u.dni, u.nombre, u.apellido,
                   u.correo, c.telefono, c.direccion,
                   COUNT(e.id_expediente) AS total_expedientes
            FROM ciudadano c
            INNER JOIN usuario u ON c.id_usuario = u.id_usuario
            LEFT JOIN expediente e ON c.id_ciudadano = e.id_ciudadano
            WHERE u.dni = %s
            GROUP BY c.id_ciudadano, u.id_usuario, u.dni, u.nombre, u.apellido,
                     u.correo, c.telefono, c.direccion
        """
        cursor.execute(sql, (dni,))
        return cursor.fetchone()

    except Error as e:
        print(f"\n[!] Error en la consulta por DNI: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def listar_ciudadanos_bd(filtro=""):
    # Lista todos los ciudadanos o filtra por coincidencias en DNI, nombre o apellido
    conexion = conectar_bd()
    if conexion is None:
        return False

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT c.id_ciudadano, u.dni, u.nombre, u.apellido,
                   u.correo, c.telefono, c.direccion
            FROM ciudadano c
            INNER JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE u.dni LIKE %s OR u.nombre LIKE %s OR u.apellido LIKE %s
            ORDER BY u.apellido ASC, u.nombre ASC
        """
        patron = f"%{filtro}%"
        cursor.execute(sql, (patron, patron, patron))
        return cursor.fetchall()

    except Error as e:
        print(f"\n[!] Error al listar ciudadanos: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


# ==============================================================================
# PANTALLAS INTERACTIVAS DE CONSOLA
# ==============================================================================

def mostrar_ficha_ciudadano(ciudadano):
    # Imprime de forma ordenada los datos de un ciudadano
    direccion_texto = ciudadano["direccion"] if ciudadano["direccion"] is not None else "No especificada"
    print("-" * 54)
    print(f" ID Ciudadano : {ciudadano['id_ciudadano']}")
    print(f" DNI          : {ciudadano['dni']}")
    print(f" Nombres      : {ciudadano['nombre']}")
    print(f" Apellidos    : {ciudadano['apellido']}")
    print(f" Correo       : {ciudadano['correo']}")
    print(f" Teléfono     : {ciudadano['telefono']}")
    print(f" Dirección    : {direccion_texto}")
    if "total_expedientes" in ciudadano:
        print(f" Expedientes  : {ciudadano['total_expedientes']} registrado(s)")
    print("-" * 54)


def pantalla_registrar_ciudadano():
    while True:
        titulo_menu("Registrar Ciudadano")
        print("Complete los datos del ciudadano (o escriba 'salir' para cancelar).")
        print("-" * 54)

        dni = input("DNI (8 dígitos): ").strip()
        if dni.lower() == "salir":
            return

        nombre = input("Nombres: ").strip()
        if nombre.lower() == "salir":
            return

        apellido = input("Apellidos: ").strip()
        if apellido.lower() == "salir":
            return

        correo = input("Correo electrónico: ").strip()
        if correo.lower() == "salir":
            return

        contrasena = input("Contraseña: ").strip()
        if contrasena.lower() == "salir":
            return

        telefono = input("Teléfono / Celular: ").strip()
        if telefono.lower() == "salir":
            return

        direccion = input("Dirección (opcional, Enter para omitir): ").strip()
        if direccion.lower() == "salir":
            return

        # 1. Validar el formato de los campos antes de conectar a MySQL
        if not validar_formato_ciudadano(dni, nombre, apellido, correo, contrasena, telefono):
            input("\nPresione Enter para intentar de nuevo.")
            continue

        # 2. Verificar que el DNI o correo no estén duplicados en la BD
        duplicado = verificar_duplicado(dni, correo)
        if duplicado is None:
            print("\nNo se pudo verificar la información en la base de datos.")
            input("\nPresione Enter para continuar.")
            return
        if duplicado is True:
            input("\nPresione Enter para intentar con otros datos.")
            continue

        # 3. Guardar en las tablas 'usuario' y 'ciudadano'
        exito = registrar_ciudadano_bd(
            dni, nombre, apellido, correo, contrasena, telefono, direccion
        )

        if exito:
            print(f"\n[OK] ¡Ciudadano {nombre} {apellido} (DNI: {dni}) registrado exitosamente!")
        else:
            print("\n[X] No se pudo completar el registro del ciudadano.")

        input("\nPresione Enter para continuar.")
        return


def pantalla_consultar_ciudadano():
    while True:
        titulo_menu("Consultar Ciudadanos")
        print(" 1. Buscar ciudadano por DNI")
        print(" 2. Buscar ciudadano por nombre o apellido")
        print(" 3. Listar todos los ciudadanos registrados")
        print(" 4. Volver al menú anterior")
        print("-" * 54)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            titulo_menu("Buscar Ciudadano por DNI")
            dni_busqueda = input("Ingrese el DNI de 8 dígitos a consultar: ").strip()

            if not (dni_busqueda.isdigit() and len(dni_busqueda) == 8):
                print("\n[!] Formato inválido: El DNI debe tener 8 dígitos numéricos.")
                input("\nPresione Enter para continuar.")
                continue

            ciudadano = consultar_ciudadano_por_dni(dni_busqueda)
            if ciudadano is False:
                print("\nNo se pudo realizar la consulta en la base de datos.")
            elif ciudadano is None:
                print(f"\n[X] No se encontró ningún ciudadano con el DNI {dni_busqueda}.")
            else:
                print("\n[OK] Ciudadano encontrado:")
                mostrar_ficha_ciudadano(ciudadano)

            input("\nPresione Enter para continuar.")

        elif opcion == "2":
            titulo_menu("Buscar Ciudadano por Nombre o Apellido")
            termino = input("Ingrese nombre o apellido a buscar: ").strip()

            if termino == "":
                print("\n[!] Error: Debe ingresar al menos un texto para buscar.")
                input("\nPresione Enter para continuar.")
                continue

            resultados = listar_ciudadanos_bd(termino)
            if resultados is False:
                print("\nNo se pudo realizar la consulta en la base de datos.")
            elif len(resultados) == 0:
                print(f"\n[X] No se encontraron ciudadanos que coincidan con '{termino}'.")
            else:
                print(f"\n[OK] Se encontraron {len(resultados)} coincidencia(s):")
                for c in resultados:
                    mostrar_ficha_ciudadano(c)

            input("\nPresione Enter para continuar.")

        elif opcion == "3":
            titulo_menu("Listado de Ciudadanos Registrados")
            resultados = listar_ciudadanos_bd("")

            if resultados is False:
                print("\nNo se pudo obtener el listado de la base de datos.")
            elif len(resultados) == 0:
                print("\n[!] Aún no hay ciudadanos registrados en el sistema.")
            else:
                print(f"Total de ciudadanos registrados: {len(resultados)}")
                for c in resultados:
                    mostrar_ficha_ciudadano(c)

            input("\nPresione Enter para continuar.")

        elif opcion == "4":
            return

        else:
            input("\nOpción no válida. Presione Enter para reintentar.")


def menu_ciudadanos():
    # Submenú unificado para gestionar el registro y consulta de ciudadanos
    while True:
        titulo_menu("Gestión de Ciudadanos")
        print(" 1. Registrar nuevo ciudadano")
        print(" 2. Consultar ciudadanos")
        print(" 3. Volver")
        print("-" * 54)

        eleccion = input("\nSeleccione una opción: ").strip()

        if eleccion == "1":
            pantalla_registrar_ciudadano()
        elif eleccion == "2":
            pantalla_consultar_ciudadano()
        elif eleccion == "3":
            return
        else:
            input("\nOpción no válida. Presione Enter para reintentar.")