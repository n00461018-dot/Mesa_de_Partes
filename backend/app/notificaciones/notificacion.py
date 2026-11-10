import time


# FUNCION PARA SELECCIONAR UN EXPEDIENTE
def seleccionar_expediente(conexion, id_usuario):

    cursor = conexion.cursor(dictionary=True)

    try:
        # Consultar el rol y el área del usuario
        cursor.execute("""
            SELECT id_rol, id_area
            FROM usuario
            WHERE id_usuario = %s
        """, (id_usuario,))

        usuario = cursor.fetchone()

        if usuario is None:
            print("Usuario no encontrado.")
            return None

        # Consultar expedientes según el rol
        if usuario["id_rol"] == 1:

            cursor.execute("""
                SELECT e.id_expediente, e.numero_expediente,
                       e.asunto, e.estado,
                       u.nombre, u.apellido, u.correo
                FROM expediente e
                INNER JOIN ciudadano c
                    ON e.id_ciudadano = c.id_ciudadano
                INNER JOIN usuario u
                    ON c.id_usuario = u.id_usuario
                ORDER BY e.fecha_registro DESC
            """)

        elif usuario["id_rol"] == 2:

            if usuario["id_area"] is None:
                print("El trabajador no tiene un área asignada.")
                return None

            cursor.execute("""
                SELECT e.id_expediente, e.numero_expediente,
                       e.asunto, e.estado,
                       u.nombre, u.apellido, u.correo
                FROM expediente e
                INNER JOIN ciudadano c
                    ON e.id_ciudadano = c.id_ciudadano
                INNER JOIN usuario u
                    ON c.id_usuario = u.id_usuario
                WHERE e.id_area = %s
                ORDER BY e.fecha_registro DESC
            """, (usuario["id_area"],))

        else:
            print("No tiene permiso para realizar esta operación.")
            return None

        # Obtener los expedientes encontrados
        expedientes = cursor.fetchall()

        if not expedientes:
            print("No hay expedientes disponibles.")
            return None

        # Mostrar los expedientes
        print("\n===== SELECCIONAR EXPEDIENTE =====")

        for i, expediente in enumerate(expedientes, 1):
            print(f"\n{i}. Expediente: {expediente['numero_expediente']}")
            print(f"   Ciudadano: {expediente['nombre']} {expediente['apellido']}")
            print(f"   Asunto: {expediente['asunto']}")
            print(f"   Estado: {expediente['estado']}")

        print("\n0. Cancelar")

        # Seleccionar expediente
        while True:
            opcion = input("\nSeleccione un expediente: ").strip()

            if opcion == "0":
                print("Operación cancelada.")
                return None

            if not opcion.isdigit():
                print("Ingrese un número válido.")
                continue

            indice = int(opcion) - 1

            if indice >= 0 and indice < len(expedientes):
                print("\nExpediente seleccionado correctamente.")
                return expedientes[indice]

            print("Opción no válida.")

    except Exception as error:
        print("Error al seleccionar expediente:", error)
        return None

    finally:
        cursor.close()


# EN PROCESO DE AVANCE A MEJORAR

def enviar_correo_simulado(destinatario, asunto, mensaje_cuerpo):
    print("\n[SISTEMA] Conectando con el servidor...")
    time.sleep(1.5) 
    print("--------------------------------------------------")
    print(f"ENVIANDO EL CORREO A: {destinatario}")
    print(f"ASUNTO: {asunto}")
    print("--------------------------------------------------")
    time.sleep(1)

def procesar_respuesta_correo_sin_bd(correo_destino, asunto, contenido):
    # 1. Simulamos el envío directamente
    enviar_correo_simulado(correo_destino, asunto, contenido)
    
    # 2. Retornamos los mensajes de éxito
    mensaje_trabajador = "SISTEMA (Trabajador/Admin): El trámite se envió con éxito al correo correspondiente."
    mensaje_usuario = f"AVISO AL CIUDADANO: Su trámite ha sido enviado de forma exitosa. La copia de su trámite se envió a su correo: {correo_destino}"
    
    return f"{mensaje_trabajador}\n{mensaje_usuario}"

# Para probarlo:
resultado = procesar_respuesta_correo_sin_bd(
    "ciudadano@email.com", 
    "Copia de Trámite", 
    "Su trámite fue procesado."
)
print("\n" + resultado)