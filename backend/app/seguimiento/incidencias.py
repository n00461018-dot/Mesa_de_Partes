from datetime import datetime

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


# Solicitar los datos de una incidencia
def registrar_incidencia(conexion, id_usuario):
    print("\n=== REGISTRAR INCIDENCIA ===")

    numero = input("Número de expediente: ").strip()

    if numero == "":
        print("Debe ingresar un expediente.")
        return

    expediente = buscar_expediente(conexion, numero)

    if expediente is None:
        return

    if not validar_permiso(conexion, expediente, id_usuario):
        return

    print("\nTipos de incidencia:")
    for i, tipo in enumerate(TIPOS, 1):
        print(f"{i}. {tipo}")

    opcion = input("Seleccione el tipo: ").strip()

    if not opcion.isdigit():
        print("Opción inválida.")
        return

    opcion = int(opcion)

    if opcion < 1 or opcion > len(TIPOS):
        print("Opción fuera de rango.")
        return

    tipo = TIPOS[opcion - 1]

    
    # Solicitar y validar la descripción
    while True:
        descripcion = input("Descripción: ").strip()

        if descripcion == "":
            print("La descripción es obligatoria.")
        elif len(descripcion) > 300:
            print("Máximo 300 caracteres.")
        else:
            break


    estado = "Abierta"

    # Registrar fecha y hora actual
    fecha_registro = datetime.now()

    # Identificar el área y usuario que registra
    id_area = expediente["id_area"]
    responsable = id_usuario


    print("\nDatos de la incidencia:")
    print("Expediente:", numero)
    print("Tipo:", tipo)
    print("Descripción:", descripcion)
    print("Estado:", estado)
    print("Fecha y hora:", fecha_registro.strftime("%d/%m/%Y %H:%M:%S"))
