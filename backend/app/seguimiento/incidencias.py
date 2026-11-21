
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
