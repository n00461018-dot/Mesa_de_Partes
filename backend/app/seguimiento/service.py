def consultar_seguimiento(conexion, numero, id_usuario):
    """Devuelve (resultado, error) segun los permisos del usuario."""
    cursor = conexion.cursor(dictionary=True)

    try:
        # Identificamos el rol de la persona que inicio sesion.
        cursor.execute("""
            SELECT LOWER(r.nombre) AS rol, u.id_area
            FROM usuario u
            INNER JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (id_usuario,))
        usuario = cursor.fetchone()

        if usuario is None:
            return None, "Usuario no encontrado."

        rol = usuario["rol"].strip()

        # Buscamos el expediente solo si el usuario puede verlo.
        if rol == "administrador":
            cursor.execute("""
                SELECT e.id_expediente, e.numero_expediente,
                       e.estado, a.nombre AS area
                FROM expediente e
                INNER JOIN area a ON e.id_area = a.id_area
                WHERE e.numero_expediente = %s
            """, (numero,))

        elif rol in ("empleado", "trabajador"):
            cursor.execute("""
                SELECT e.id_expediente, e.numero_expediente,
                       e.estado, a.nombre AS area
                FROM expediente e
                INNER JOIN area a ON e.id_area = a.id_area
                WHERE e.numero_expediente = %s
                  AND (
                      e.id_area = %s
                      OR EXISTS (
                          SELECT 1 FROM derivacion d
                          WHERE d.id_expediente = e.id_expediente
                            AND (d.id_area_origen = %s
                                 OR d.id_area_destino = %s)
                      )
                  )
            """, (numero, usuario["id_area"],
                  usuario["id_area"], usuario["id_area"]))

        elif rol == "ciudadano":
            cursor.execute("""
                SELECT e.id_expediente, e.numero_expediente,
                       e.estado, a.nombre AS area
                FROM expediente e
                INNER JOIN area a ON e.id_area = a.id_area
                INNER JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
                WHERE e.numero_expediente = %s
                  AND c.id_usuario = %s
            """, (numero, id_usuario))

        else:
            return None, "Rol no autorizado."

        expediente = cursor.fetchone()

        if expediente is None:
            return None, "Expediente no encontrado o sin acceso."

        # Consultamos los movimientos guardados en seguimiento.
        if rol == "ciudadano":
            # El ciudadano ve estados y fechas, no notas internas.
            cursor.execute("""
                SELECT fecha, estado
                FROM seguimiento
                WHERE id_expediente = %s
                ORDER BY fecha, id_seguimiento
            """, (expediente["id_expediente"],))
        else:
            cursor.execute("""
                SELECT s.fecha, s.estado, s.observacion,
                       u.nombre, u.apellido
                FROM seguimiento s
                INNER JOIN usuario u ON s.id_usuario = u.id_usuario
                WHERE s.id_expediente = %s
                ORDER BY s.fecha, s.id_seguimiento
            """, (expediente["id_expediente"],))

        movimientos = cursor.fetchall()

        # Organizamos la informacion para mostrarla en routes.py.
        resultado = {
            "numero": expediente["numero_expediente"],
            "estado": expediente["estado"],
            "area": expediente["area"],
            "historial": movimientos
        }
        return resultado, None

    finally:
        cursor.close()
