from datetime import datetime

from database.conexion_bd import conectar_bd


def registrar_documento(usuario):
    conexion = conectar_bd()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = None
    try:
        cursor = conexion.cursor()
        print("=== NUEVO TRÁMITE ===")

        asunto = input("Ingrese el asunto del trámite: ").strip()
        if not asunto:
            print("El asunto no puede estar vacío.")
            return
        if len(asunto) > 300:
            print("El asunto no puede superar los 300 caracteres.")
            return

        cursor.execute(
            "SELECT id_tipo_tramite, nombre FROM tipo_tramite ORDER BY id_tipo_tramite"
        )
        tipos_tramite = cursor.fetchall()
        if not tipos_tramite:
            print("No hay tipos de trámite registrados en la base de datos.")
            return

        print("\nTipos de trámite disponibles:")
        for id_tipo, nombre in tipos_tramite:
            print(f"{id_tipo}. {nombre}")

        id_tipo_ingresado = input("Seleccione el ID del tipo de trámite: ").strip()
        if not id_tipo_ingresado.isdigit():
            print("El ID del tipo de trámite debe ser numérico.")
            return

        id_tipo = int(id_tipo_ingresado)
        if id_tipo not in {tipo[0] for tipo in tipos_tramite}:
            print("El tipo de trámite seleccionado no existe.")
            return

        if usuario.get("id_rol") == 3:
            id_ciudadano = usuario.get("id_ciudadano")
            if id_ciudadano is None:
                print("El usuario no tiene un registro de ciudadano asociado.")
                return
        else:
            dni_ciudadano = input(
                "Ingrese el DNI del ciudadano que presenta el trámite: "
            ).strip()
            if not (dni_ciudadano.isdigit() and len(dni_ciudadano) == 8):
                print("El DNI debe contener exactamente 8 dígitos.")
                return

            cursor.execute(
                """
                SELECT c.id_ciudadano
                FROM ciudadano c
                INNER JOIN usuario u ON u.id_usuario = c.id_usuario
                WHERE u.dni = %s
                """,
                (dni_ciudadano,),
            )
            ciudadano = cursor.fetchone()
            if ciudadano is None:
                print("No se encontró un ciudadano registrado con ese DNI.")
                return
            id_ciudadano = ciudadano[0]

        nombre_archivo = input(
            "Nombre del archivo adjunto (ej. dni.pdf): "
        ).strip()
        if not nombre_archivo:
            print("Debe ingresar el nombre del archivo.")
            return
        if len(nombre_archivo) > 150:
            print("El nombre del archivo no puede superar los 150 caracteres.")
            return

        extension = nombre_archivo.rsplit(".", 1)
        tipo_documento = (
            extension[-1].upper()
            if len(extension) == 2 and extension[-1]
            else None
        )
        if tipo_documento is not None and len(tipo_documento) > 50:
            print("La extensión del archivo no es válida.")
            return

        fecha_actual = datetime.now().replace(microsecond=0)
        año_actual = fecha_actual.year
        conexion.start_transaction()
        cursor.execute(
            "SELECT COUNT(*) FROM expediente WHERE YEAR(fecha_registro) = %s",
            (año_actual,),
        )
        cantidad = cursor.fetchone()[0] + 1
        numero_expediente = f"{año_actual}-{cantidad:05d}"

        sql_expediente = """
            INSERT INTO expediente (numero_expediente, fecha_registro, asunto, estado, id_ciudadano, id_tipo_tramite, id_area)
            VALUES (%s, %s, %s, 'Registrado', %s, %s, 1)
        """
        cursor.execute(sql_expediente, (numero_expediente, fecha_actual, asunto, id_ciudadano, id_tipo))
        id_expediente = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO documento (
                nombre_archivo, tipo_documento, fecha_subida, id_expediente
            ) VALUES (%s, %s, %s, %s)
            """,
            (nombre_archivo, tipo_documento, fecha_actual, id_expediente),
        )

        cursor.execute(
            """
            INSERT INTO seguimiento (
                fecha, estado, observacion, id_usuario, id_expediente
            ) VALUES (%s, 'Registrado', %s, %s, %s)
            """,
            (
                fecha_actual,
                f"Trámite registrado por {usuario['nombre']} {usuario['apellido']}"[:200],
                usuario["id_usuario"],
                id_expediente,
            ),
        )

        conexion.commit()
        print(f"\n¡Éxito! Su trámite fue registrado con el número: {numero_expediente}")

    except Exception as e:
        conexion.rollback()
        print(f"\nError al registrar el trámite: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()