from mysql.connector import Error
from solicitudes.extra import titulo_menu
from database.conexion_bd import conectar_bd

# Función básica para validar el formato antes de consultar la BD
def validar_formato_entrada(identificador, clave):
    if identificador == "" or clave == "":
        print("\n[!] Error: No puede dejar el usuario o la contraseña en blanco.")
        return False

    # En la BD el DNI tiene 8 dígitos numéricos
    es_dni = identificador.isdigit() and len(identificador) == 8
    # El correo debe contener un @, un punto (.), no debe tener espacios y debe de tener 6 caracteres o más
    es_correo = (
        "@" in identificador
        and "." in identificador
        and " " not in identificador
        and len(identificador) >= 6
    )

    if not es_dni and not es_correo:
        print("\n[!] Formato inválido: Ingrese un DNI de 8 dígitos o un correo válido.")
        return False

    return True


# Función para iniciar sesión (Consulta el DNI o correo y la contraseña en la BD)
def iniciar_sesion(identificador, clave):
    # Devuelve un diccionario con los datos del usuario, None si no lo encuentra
    # o False si hubo un error con la base de datos
    conexion = conectar_bd()
    if conexion is None:
        return False

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        # Agregamos u.dni, u.id_area y c.id_ciudadano para usarlos luego en menu.py
        sql = """
            SELECT u.id_usuario, u.dni, u.nombre, u.apellido, u.id_rol, 
                   u.id_area, a.nombre AS nombre_area, c.id_ciudadano
            FROM usuario u
            LEFT JOIN area a ON u.id_area = a.id_area
            LEFT JOIN ciudadano c ON u.id_usuario = c.id_usuario
            WHERE (u.dni = %s OR u.correo = %s) AND BINARY u.contrasena = %s
        """
        cursor.execute(sql, (identificador, identificador, clave))
        return cursor.fetchone()

    except Error as e:
        print(f"Error en la consulta: {e}")
        return False
    finally:
        # Siempre se cierran el cursor y la conexión
        if cursor is not None:
            cursor.close()
        conexion.close()


# Función para mostrar el login con límite de intentos
def pantalla_login():
    # Contador de intentos permitidos
    intentos_restantes = 3

    while intentos_restantes > 0:
        titulo_menu("Acceso al Sistema")
        print(f"Intentos disponibles: {intentos_restantes}")
        print("-" * 54)

        identificador = input("Ingrese DNI o correo (o 'salir'): ").strip()
        if identificador.lower() == "salir":
            return None

        clave = input("Contraseña: ").strip()

        # Primero validamos el formato sin gastar conexión a MySQL
        if not validar_formato_entrada(identificador, clave):
            input("\nPresione Enter para intentar de nuevo.")
            continue

        # Si el formato es correcto, consultamos en la Base de Datos
        usuario = iniciar_sesion(identificador, clave)

        if usuario is False:
            print("\nNo se pudo consultar la base de datos. Intente de nuevo.")
            input("\nPresione Enter para continuar.")
        elif usuario is None:
            intentos_restantes -= 1
            print("\n[X] DNI/correo o contraseña incorrectos.")
            if intentos_restantes > 0:
                input(f"\nLe quedan {intentos_restantes} intento(s). Presione Enter para continuar.")
            else:
                print("\n[!] Ha superado el límite de 3 intentos fallidos. Acceso bloqueado.")
                input("\nPresione Enter para salir del sistema.")
                return None
        else:
            # Si las credenciales son correctas, damos bienvenida y retornamos el diccionario
            print(f"\n[OK] ¡Bienvenido(a), {usuario['nombre']} {usuario['apellido']}!")
            input("Presione Enter para ingresar a su menú...")
            return usuario