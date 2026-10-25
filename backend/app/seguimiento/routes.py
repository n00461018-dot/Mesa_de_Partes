# Menus de consulta y cambio de estado del expediente.
from .service import consultar_seguimiento
from .estados import TRANSICIONES, actualizar_estado

def menu_seguimiento(conexion, id_usuario):

    numero = input(
        "Ingrese numero de expediente: "
    ).strip()

    try:
        resultado, error = consultar_seguimiento(
            conexion, numero, id_usuario
        )

        if error:
            print(error)
            return

        print("\n===== SEGUIMIENTO =====")
        print("Expediente:", resultado["numero"])
        print("Estado:", resultado["estado"])
        print("Área:", resultado["area"])

        print("\nHISTORIAL")

        for movimiento in resultado["historial"]:
            print("----------------------")
            print("Fecha:", movimiento["fecha"])
            print("Estado:", movimiento["estado"])
            # Ciudadanos no reciben observaciones internas.
            if "observacion" in movimiento:
                print("Observación:", movimiento["observacion"])
            if "nombre" in movimiento:
                print("Responsable:", movimiento["nombre"],
                      movimiento["apellido"])

    except Exception as error:
        print("Error al consultar:", error)


# Importamos las funciones de cambio de estado



# Funcion del menu de cambio de estado asistido
def menu_cambio_estado(conexion, id_usuario):

    # Solicitamos el numero de expediente
    numero = input("Numero del expediente: ").strip()

    # Creamos el cursor para consultar MySQL
    cursor = conexion.cursor(dictionary=True)

    try:
        # Buscamos el expediente y su area responsable
        cursor.execute("""
            SELECT e.estado, a.nombre AS area
            FROM expediente e
            INNER JOIN area a ON e.id_area = a.id_area
            WHERE e.numero_expediente = %s
        """, (numero,))

        expediente = cursor.fetchone()

    finally:
        cursor.close()

    # Verificamos que exista el expediente
    if expediente is None:
        print("Expediente no encontrado.")
        return

    estado = expediente["estado"]

    # Mostramos el estado actual
    print("\n===== EXPEDIENTE ENCONTRADO =====")
    print("Estado actual:", estado)
    print("Area responsable:", expediente["area"])

    # Consultamos las acciones permitidas
    opciones = TRANSICIONES.get(estado, {})

    if not opciones:
        print("No hay cambios disponibles.")
        return

    print("\n===== ACCIONES DISPONIBLES =====")

    for clave, datos in opciones.items():
        print(clave, "-", datos[0])

    print("0 - Cancelar")

    # El empleado selecciona una accion
    accion = input("Seleccione una accion: ").strip()

    if accion == "0":
        print("Operacion cancelada.")
        return

    if accion not in opciones:
        print("Opcion no valida.")
        return

    # El sistema determina el nuevo estado
    descripcion, nuevo_estado = opciones[accion]

    print("\nNuevo estado:", nuevo_estado)

    # Registramos una observacion
    observacion = input(
        "Ingrese observacion: "
    ).strip()

    # Solicitamos confirmacion
    confirmar = input(
        "Confirmar cambio (S/N): "
    ).strip().upper()

    if confirmar != "S":
        print("Operacion cancelada.")
        return

    try:
        # Actualizamos el estado y registramos el movimiento
        resultado = actualizar_estado(
            conexion,
            numero,
            accion,
            observacion,
            id_usuario
        )

        print(resultado)

    except Exception as error:
        print("Error al actualizar:", error)
