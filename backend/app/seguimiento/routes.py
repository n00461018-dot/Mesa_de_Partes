# Menus de consulta y cambio de estado del expediente.
from .service import consultar_seguimiento
from .estados import TRANSICIONES, actualizar_estado

# FUNCION PARA CONSULTAR EL SEGUIMIENTO DE EXPEDIENTES
def menu_seguimiento(conexion, id_usuario):

    numero = input("Ingrese numero de expediente: ").strip()

    if not numero:
        print("Debe ingresar un numero de expediente.")
        return

    try:
        resultado, error = consultar_seguimiento(
            conexion, numero, id_usuario
        )

        # Finalizar la transaccion de lectura
        conexion.commit()

        if error:
            print(error)
            return

        print("\n===== SEGUIMIENTO =====")
        print("Expediente:", resultado["numero"])
        print("Estado:", resultado["estado"])
        print("Area:", resultado["area"])

        print("\nHISTORIAL")

        for movimiento in resultado["historial"]:
            print("----------------------")
            print("Fecha:", movimiento["fecha"])
            print("Estado:", movimiento["estado"])

            if "observacion" in movimiento:
                print("Observacion:", movimiento["observacion"])

            if "nombre" in movimiento:
                print(
                    "Responsable:",
                    movimiento["nombre"],
                    movimiento["apellido"]
                )

    except Exception as error:
        conexion.rollback()
        print("Error al consultar el seguimiento:", error)


# FUNCION PARA CAMBIAR EL ESTADO DEL EXPEDIENTE
def menu_cambio_estado(conexion, id_usuario):

    numero = input("Ingrese numero de expediente: ").strip()

    if not numero:
        print("Debe ingresar un numero de expediente.")
        return

    cursor = conexion.cursor(dictionary=True)

    try:
        # Consultar el expediente y su area responsable
        cursor.execute("""
            SELECT e.estado, a.nombre AS area
            FROM expediente e
            INNER JOIN area a ON e.id_area = a.id_area
            WHERE e.numero_expediente = %s
        """, (numero,))

        expediente = cursor.fetchone()

        # Finalizar la transaccion de lectura
        conexion.commit()

    except Exception as error:
        conexion.rollback()
        print("Error al consultar el expediente:", error)
        return

    finally:
        cursor.close()

    # Verificar si existe el expediente
    if expediente is None:
        print("Expediente no encontrado.")
        return

    estado = expediente["estado"]

    # Mostrar los datos del expediente
    print("\n===== EXPEDIENTE ENCONTRADO =====")
    print("Numero:", numero)
    print("Estado actual:", estado)
    print("Area responsable:", expediente["area"])

    # Obtener las acciones permitidas
    opciones = TRANSICIONES.get(estado, {})

    if not opciones:
        print("\nNo hay cambios de estado disponibles.")
        return

    # Mostrar las acciones disponibles
    print("\n===== ACCIONES DISPONIBLES =====")

    for clave, datos in opciones.items():
        print(clave, "-", datos[0])

    print("0 - Cancelar")

    # Solicitar la accion
    accion = input("\nSeleccione una accion: ").strip()

    if accion == "0":
        print("Operacion cancelada.")
        return

    if accion not in opciones:
        print("Opcion no valida.")
        return

    # Obtener la descripcion y el nuevo estado
    descripcion, nuevo_estado = opciones[accion]

    print("\nAccion seleccionada:", descripcion)
    print("Nuevo estado:", nuevo_estado)

    # Solicitar observacion
    observacion = input(
        "\nIngrese observacion (0 para cancelar): "
    ).strip()

    if observacion == "0":
        print("Operacion cancelada.")
        return

    # Validar la observacion
    if len(observacion) > 150:
        print("La observacion no debe superar 150 caracteres.")
        return

    if nuevo_estado == "Observado" and not observacion:
        print("Debe indicar el motivo de la observacion.")
        return

    # Confirmar el cambio
    confirmar = input(
        "\n¿Confirmar cambio de estado? (S/N): "
    ).strip().upper()

    if confirmar != "S":
        print("Operacion cancelada.")
        return

    try:
        # Actualizar el expediente y registrar el seguimiento
        resultado = actualizar_estado(
            conexion,
            numero,
            accion,
            observacion,
            id_usuario
        )

        print("\n" + resultado)

    except Exception as error:
        print("Error al actualizar el estado:", error)
