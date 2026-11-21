
# Tipos de incidencias disponibles
TIPOS = (
    "Documentación incompleta",
    "Error de derivación",
    "Error de datos",
    "Problema técnico",
    "Otro"
)

# Estados de una incidencia
ESTADOS = ("Abierta", "En seguimiento", "Resuelta")

# Buscar un expediente en la base de datos
def buscar_expediente(conexion, numero):
    cursor = conexion.cursor(dictionary=True)

    # Consultar el número de expediente
    cursor.execute("""
        SELECT id_expediente, numero_expediente, estado, id_area
        FROM expediente
        WHERE numero_expediente = %s
    """, (numero,))

    expediente = cursor.fetchone()
    cursor.close()

    # Comprobar si existe el expediente
    if expediente is None:
        print("Expediente no encontrado.")
        return None

    return expediente


# Verificar los permisos del usuario
def validar_permiso(conexion, expediente, id_usuario):
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_rol, id_area
        FROM usuario
        WHERE id_usuario = %s
    """, (id_usuario,))

    usuario = cursor.fetchone()
    cursor.close()

    if usuario is None:
        print("Usuario no encontrado.")
        return False

    if usuario["id_rol"] not in (1, 2):
        print("No tiene permiso para registrar incidencias.")
        return False

    if usuario["id_rol"] == 2:
        if usuario["id_area"] != expediente["id_area"]:
            print("El expediente no pertenece a su área.")
            return False

    if expediente["estado"] != "En proceso":
        print("El expediente no está en atención.")
        return False

    return True
