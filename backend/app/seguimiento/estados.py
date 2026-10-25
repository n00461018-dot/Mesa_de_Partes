# Acciones disponibles según el estado actual del expediente.
TRANSICIONES = {
    "Registrado": {
        "1": ("Iniciar revision", "En evaluación")
    },
    "Derivado": {
        "1": ("Confirmar recepcion", "Recibido")
    },
    "Recibido": {
        "1": ("Iniciar revision", "En evaluación")
    },
    "En evaluación": {
        "1": ("Solicitar subsanacion", "Observado")
    },
    "Observado": {
        "1": ("Reanudar revision", "En evaluación")
    }
}


def actualizar_estado(conexion, numero, accion, observacion, id_usuario):
    """Actualiza el estado y registra el movimiento en seguimiento."""
    cursor = conexion.cursor(dictionary=True)

    try:
        conexion.start_transaction()

        # Buscar el expediente antes de modificarlo.
        cursor.execute("""
            SELECT id_expediente, estado, id_area
            FROM expediente
            WHERE numero_expediente = %s
            FOR UPDATE
        """, (numero,))
        expediente = cursor.fetchone()

        if expediente is None:
            conexion.rollback()
            return "Expediente no encontrado."

        # Comprobar el rol y el área del usuario autenticado.
        cursor.execute("""
            SELECT u.id_area, r.nombre AS rol
            FROM usuario u
            INNER JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (id_usuario,))
        usuario = cursor.fetchone()

        if usuario is None:
            conexion.rollback()
            return "Usuario no encontrado."

        rol = usuario["rol"].lower().strip()
        if rol not in ("administrador", "empleado", "trabajador"):
            conexion.rollback()
            return "No tiene permiso para cambiar el estado."

        if rol != "administrador" and usuario["id_area"] != expediente["id_area"]:
            conexion.rollback()
            return "No pertenece al area responsable."

        # Solo permitir acciones correspondientes al estado actual.
        opciones = TRANSICIONES.get(expediente["estado"], {})
        if accion not in opciones:
            conexion.rollback()
            return "Accion no permitida para este estado."

        descripcion, nuevo_estado = opciones[accion]
        observacion = observacion.strip()

        if len(observacion) > 150:
            conexion.rollback()
            return "La observacion supera 150 caracteres."

        if nuevo_estado == "Observado" and not observacion:
            conexion.rollback()
            return "Debe indicar el motivo de la observacion."

        # Guardar el estado actual del expediente.
        cursor.execute("""
            UPDATE expediente
            SET estado = %s
            WHERE id_expediente = %s
        """, (nuevo_estado, expediente["id_expediente"]))

        # Registrar la fecha, el usuario y la observación en el historial.
        detalle = descripcion
        if observacion:
            detalle += ": " + observacion

        cursor.execute("""
            INSERT INTO seguimiento (
                fecha, estado, observacion, id_usuario, id_expediente
            ) VALUES (NOW(), %s, %s, %s, %s)
        """, (
            nuevo_estado,
            detalle[:200],
            id_usuario,
            expediente["id_expediente"]
        ))

        # Confirmar las dos operaciones juntas.
        conexion.commit()
        return "Estado actualizado correctamente."

    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
