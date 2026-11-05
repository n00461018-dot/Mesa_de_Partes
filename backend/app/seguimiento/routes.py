# Menus de consulta y cambio de estado del expediente.
from .service import consultar_seguimiento
from .estados import TRANSICIONES, actualizar_estado


# Funcion del menu de cambio de estado
def menu_cambio_estado(conexion, id_usuario):

    # Solicitar el numero de expediente
    numero = input("Ingrese numero de expediente: ").strip()

    if not numero:
        print("Debe ingresar un numero de expediente.")
        return

    cursor = conexion.cursor(dictionary=True)

    try:
        # Buscar el expediente y su area responsable
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
    print("Numero de expediente:", numero)
    print("Estado actual:", estado)
    print("Area responsable:", expediente["area"])

    # Obtener las acciones permitidas para el estado actual
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

    # Confirmar la operacion
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
