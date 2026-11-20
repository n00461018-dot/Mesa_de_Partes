from mysql.connector import Error
from solicitudes.extra import titulo_menu, validar_dni
from database.conexion_bd import conectar_bd
from database.reniec import validar_padron_reniec


# ==============================================================================
# VALIDACIONES DE FORMATO
# ==============================================================================

def validar_correo(correo):
    # Verificar que no tenga espacios, puntos seguidos y que contenga exactamente un @
    if " " in correo or ".." in correo or correo.count("@") != 1:
        return False

    usuario_correo, dominio = correo.split("@")
    # Verificar que exista usuario antes del @ y un punto dentro del dominio
    if not usuario_correo or usuario_correo.startswith(".") or usuario_correo.endswith(".") or "." not in dominio:
        return False

    partes_dominio = dominio.split(".")
    # Verificar que ninguna parte del dominio esté vacía y que la extensión final tenga al menos 2 letras
    if "" in partes_dominio:
        return False

    extension = partes_dominio[-1]
    return len(extension) >= 2 and extension.isalpha()


def validar_telefono(telefono):
    # En la BD el teléfono es VARCHAR(15) NOT NULL (entre 7 y 15 dígitos numéricos)
    return telefono.isdigit() and 7 <= len(telefono) <= 15


# ==============================================================================
# CONSULTAS A LA BASE DE DATOS
# ==============================================================================

# Excepción para cancelar el registro si no se puede consultar la BD
class ErrorBD(Exception):
    pass


# Función auxiliar para ejecutar un SELECT abriendo y cerrando su propia conexión
# Devuelve una fila (uno=True) o la lista de filas, y False si hubo error de BD
def _consultar(sql, parametros, mensaje_error, uno=False):
    conexion = conectar_bd()
    if conexion is None:
        return False

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchone() if uno else cursor.fetchall()

    except Error as e:
        print(f"\n[!] {mensaje_error}: {e}")
        return False
    finally:
        # Siempre se cierran el cursor y la conexión
        if cursor is not None:
            cursor.close()
        conexion.close()


# Consultas para saber si el DNI o el correo ya existen en la tabla 'usuario'
SQL_DUPLICADO = {
    "dni": "SELECT 1 FROM usuario WHERE dni = %s LIMIT 1",
    "correo": "SELECT 1 FROM usuario WHERE correo = %s LIMIT 1",
}


def existe_usuario(campo, valor):
    # Devuelve True si el dato ya está registrado y lanza ErrorBD si no se pudo consultar
    registro = _consultar(SQL_DUPLICADO[campo], (valor,),
                          "Error al verificar duplicados en la base de datos", uno=True)
    if registro is False:
        raise ErrorBD()
    return registro is not None


# Función para registrar el ciudadano en la BD
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

        # 2. Insertar datos de contacto en la tabla 'ciudadano'
        # Si la dirección se dejó en blanco, se guarda como NULL en la BD
        sql_ciudadano = """
            INSERT INTO ciudadano (telefono, direccion, id_usuario)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_ciudadano, (telefono, direccion or None, id_usuario_nuevo))

        # Confirmar ambas inserciones en la base de datos
        conexion.commit()
        return True

    except Error as e:
        # Si ocurre algún problema (por ejemplo, un DNI o correo duplicado que la BD
        # rechaza por ser UNIQUE), se deshacen los cambios para no dejar registros incompletos
        conexion.rollback()
        print(f"\n[!] Error al registrar al ciudadano: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


# Función para consultar el ciudadano utilizando su DNI
def consultar_ciudadano_por_dni(dni):
    # Busca a un ciudadano por su DNI y cuenta sus expedientes registrados
    # Devuelve un diccionario con los datos, None si no existe o False si hubo error de BD
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
    return _consultar(sql, (dni,), "Error en la consulta por DNI", uno=True)


def listar_ciudadanos_bd(filtro=""):
    # Lista todos los ciudadanos o filtra por coincidencias en DNI, nombre o apellido
    # Devuelve una lista de diccionarios o False si hubo error de BD
    sql = """
        SELECT c.id_ciudadano, u.dni, u.nombre, u.apellido,
               u.correo, c.telefono, c.direccion
        FROM ciudadano c
        INNER JOIN usuario u ON c.id_usuario = u.id_usuario
        WHERE u.dni LIKE %s OR u.nombre LIKE %s OR u.apellido LIKE %s
        ORDER BY u.apellido ASC, u.nombre ASC
    """
    patron = f"%{filtro}%"
    return _consultar(sql, (patron, patron, patron), "Error al listar ciudadanos")


# ==============================================================================
# REGISTRO DE CIUDADANO
# ==============================================================================

# Validadores de cada campo del registro: devuelven el mensaje de error o None si el dato es válido
def _obligatorio(valor):
    return None if valor else "Error: Este campo es obligatorio."


def _validar_dni_nuevo(dni):
    error_dni = validar_dni(dni)
    if error_dni is not None:
        return f"Formato inválido: {error_dni}"
    # Verificar inmediatamente en la BD si el DNI ya está registrado
    if existe_usuario("dni", dni):
        return f"Error: Ya existe un usuario registrado con el DNI {dni}."
    return None


def _validar_correo_nuevo(correo):
    if not validar_correo(correo):
        return "Formato inválido: Ingrese un correo electrónico válido."
    # Verificar inmediatamente en la BD si el correo ya está registrado
    if existe_usuario("correo", correo):
        return f"Error: El correo '{correo}' ya se encuentra registrado."
    return None


def _validar_telefono_nuevo(telefono):
    if not validar_telefono(telefono):
        return "Formato inválido: El teléfono debe contener entre 7 y 15 dígitos numéricos."
    return None


# Campos del formulario de registro en el orden en que se piden: (clave, mensaje, validador)
CAMPOS_REGISTRO = [
    ("dni", "DNI (8 dígitos): ", _validar_dni_nuevo),
    ("digito", "Código verificador (9no dígito al costado del DNI): ", _obligatorio),
    ("emision", "Fecha de emisión del DNI (DD/MM/AAAA): ", _obligatorio),
    ("caducidad", "Fecha de caducidad del DNI (DD/MM/AAAA): ", _obligatorio),
    ("nombre", "Nombres: ", _obligatorio),
    ("apellido", "Apellidos: ", _obligatorio),
    ("correo", "Correo electrónico: ", _validar_correo_nuevo),
    ("contrasena", "Contraseña: ", _obligatorio),
    ("telefono", "Teléfono / Celular: ", _validar_telefono_nuevo),
    ("direccion", "Dirección (opcional, Enter para omitir): ", None),
]


def pedir_campo(mensaje, validar=None):
    # Pide un dato hasta que sea válido. Devuelve None si el usuario escribe 'salir'
    while True:
        valor = input(mensaje).strip()
        if valor.lower() == "salir":
            return None

        error = validar(valor) if validar is not None else None
        if error is None:
            return valor
        print(f"\n[!] {error}\n")


def pantalla_registrar_ciudadano():
    try:
        while True:
            titulo_menu("Registrar Ciudadano")
            print("Complete los datos del ciudadano (o escriba 'salir' para cancelar).")
            print("-" * 54)

            # 1. Pedir y validar cada campo al momento de ingresarlo
            datos = {}
            for clave, mensaje, validar in CAMPOS_REGISTRO:
                valor = pedir_campo(mensaje, validar)
                if valor is None:
                    return
                datos[clave] = valor

            # 2. Validar el DNI con el padrón RENIEC (dígito verificador y fechas)
            error_padron = validar_padron_reniec(
                datos["dni"], datos["digito"], datos["emision"], datos["caducidad"]
            )
            if error_padron is not None:
                print(f"\n[!] Validación RENIEC fallida: {error_padron}")
                input("\nPresione Enter para intentar de nuevo.")
                continue

            # 3. Guardar en las tablas 'usuario' y 'ciudadano'
            exito = registrar_ciudadano_bd(
                datos["dni"], datos["nombre"], datos["apellido"], datos["correo"],
                datos["contrasena"], datos["telefono"], datos["direccion"]
            )

            if exito:
                print(f"\n[OK] ¡Ciudadano {datos['nombre']} {datos['apellido']} (DNI: {datos['dni']}) registrado exitosamente!")
            else:
                print("\n[X] No se pudo completar el registro del ciudadano.")

            input("\nPresione Enter para continuar.")
            return

    except ErrorBD:
        print("\nNo se pudo verificar la información en la base de datos.")
        input("\nPresione Enter para continuar.")


# ==============================================================================
# CONSULTA DE CIUDADANOS
# ==============================================================================

# Función para mostrar todos los datos del ciudadano
def mostrar_ficha_ciudadano(ciudadano):
    # Imprime de forma ordenada los datos de un ciudadano
    print("-" * 54)
    print(f" ID Ciudadano : {ciudadano['id_ciudadano']}")
    print(f" DNI          : {ciudadano['dni']}")
    print(f" Nombres      : {ciudadano['nombre']}")
    print(f" Apellidos    : {ciudadano['apellido']}")
    print(f" Correo       : {ciudadano['correo']}")
    print(f" Teléfono     : {ciudadano['telefono']}")
    print(f" Dirección    : {ciudadano['direccion'] or 'No especificada'}")
    if "total_expedientes" in ciudadano:
        print(f" Expedientes  : {ciudadano['total_expedientes']} registrado(s)")
    print("-" * 54)


# Función para mostrar una lista de ciudadanos con sus mensajes de error, vacío y total
def mostrar_listado(resultados, mensaje_error, mensaje_vacio, mensaje_total):
    if resultados is False:
        print(mensaje_error)
    elif len(resultados) == 0:
        print(mensaje_vacio)
    else:
        print(mensaje_total.format(len(resultados)))
        for c in resultados:
            mostrar_ficha_ciudadano(c)


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

            if validar_dni(dni_busqueda) is not None:
                print("\n[!] Formato inválido: El DNI debe tener 8 dígitos numéricos.")
            else:
                ciudadano = consultar_ciudadano_por_dni(dni_busqueda)
                if ciudadano is False:
                    print("\nNo se pudo realizar la consulta en la base de datos.")
                elif ciudadano is None:
                    print(f"\n[X] No se encontró ningún ciudadano con el DNI {dni_busqueda}.")
                else:
                    print("\n[OK] Ciudadano encontrado:")
                    mostrar_ficha_ciudadano(ciudadano)

        elif opcion == "2":
            titulo_menu("Buscar Ciudadano por Nombre o Apellido")
            termino = input("Ingrese nombre o apellido a buscar: ").strip()

            if termino == "":
                print("\n[!] Error: Debe ingresar al menos un texto para buscar.")
            else:
                mostrar_listado(
                    listar_ciudadanos_bd(termino),
                    "\nNo se pudo realizar la consulta en la base de datos.",
                    f"\n[X] No se encontraron ciudadanos que coincidan con '{termino}'.",
                    "\n[OK] Se encontraron {} coincidencia(s):",
                )

        elif opcion == "3":
            titulo_menu("Listado de Ciudadanos Registrados")
            mostrar_listado(
                listar_ciudadanos_bd(),
                "\nNo se pudo obtener el listado de la base de datos.",
                "\n[!] Aún no hay ciudadanos registrados en el sistema.",
                "Total de ciudadanos registrados: {}",
            )

        elif opcion == "4":
            return

        else:
            input("\nOpción no válida. Presione Enter para reintentar.")
            continue

        # Pausa común a las opciones 1, 2 y 3
        input("\nPresione Enter para continuar.")


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
