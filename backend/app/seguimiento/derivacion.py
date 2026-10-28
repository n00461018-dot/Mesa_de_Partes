from datetime import datetime
from .estados import TRANSICIONES

def derivar_expediente_area(conexion, id_usuario):
    """
    Función principal para permitir que un empleado municipal o administrador 
    derive un expediente de un área a otra. 
    Por qué se hace así: Sigue estrictamente el paradigma funcional del equipo 
    (sin clases) y maneja transacciones atómicas para asegurar la integridad de la BD.
    """
    
    # 1. Solicitar el número de expediente a derivar
    numero = input("Ingrese el número de expediente a derivar: ").strip()
    if not numero:
        print("El número de expediente no puede estar vacío.")
        return

    # Creamos el cursor con dictionary=True para poder acceder a las columnas 
    # por su nombre (ej. expediente['estado']), igual que en el resto del proyecto.
    cursor = conexion.cursor(dictionary=True)

    try:
        # 2. Iniciar transacción estricta (Misma lógica que en estados.py)
        # Por qué: Garantiza que si algo falla a mitad del proceso, 
        # ningún cambio parcial se guarde en la base de datos.
        conexion.start_transaction()

        # Buscar el expediente y bloquearlo temporalmente con FOR UPDATE
        # Por qué: Evita problemas de concurrencia. Si otro empleado intenta 
        # modificar el mismo expediente al mismo tiempo, este se espera hasta que termine.
        cursor.execute("""
            SELECT id_expediente, estado, id_area 
            FROM expediente 
            WHERE numero_expediente = %s
            FOR UPDATE
        """, (numero,))
        expediente = cursor.fetchone()

        if expediente is None:
            conexion.rollback() # Revertimos si no existe
            print("Expediente no encontrado.")
            return

        # 3. Comprobar el rol y el área del usuario autenticado
        # Por qué: Seguridad basada en roles (RBAC). Necesitamos saber 
        # si el usuario logueado realmente trabaja en la municipalidad y qué área tiene asignada.
        cursor.execute("""
            SELECT u.id_area, r.nombre AS rol, u.nombre, u.apellido
            FROM usuario u
            INNER JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (id_usuario,))
        usuario = cursor.fetchone()

        if usuario is None:
            conexion.rollback()
            print("Usuario no encontrado.")
            return

        rol = usuario["rol"].lower().strip()
        
        # Validar permisos permitidos (Administrador, Empleado o Trabajador)
        if rol not in ("administrador", "empleado", "trabajador"):
            conexion.rollback()
            print("No tiene permiso para derivar expedientes.")
            return

        # Si el rol no es administrador, obligatoriamente debe pertenecer al área actual del expediente
        # Por qué: Un trabajador de Obras no puede derivar un expediente que le pertenece a Mesa de Partes.
        if rol != "administrador" and usuario["id_area"] != expediente["id_area"]:
            conexion.rollback()
            print("No pertenece al área responsable actual de este expediente.")
            return

        id_area_origen = expediente["id_area"]

        # Consultar el nombre del área de origen para mostrarlo en pantalla de forma amigable
        cursor.execute("SELECT nombre FROM area WHERE id_area = %s", (id_area_origen,))
        area_origen_info = cursor.fetchone()
        
        print(f"\n===== DERIVACIÓN DE EXPEDIENTE =====")
        print(f"Expediente N°: {numero}")
        print(f"Área Origen actual: {area_origen_info['nombre'] if area_origen_info else 'Desconocida'}")

        # 4. Listar las áreas disponibles para el destino (excluyendo la actual)
        # Por qué: No tiene sentido derivar un expediente al mismo área donde ya está.
        cursor.execute("SELECT id_area, nombre FROM area WHERE id_area != %s", (id_area_origen,))
        areas_destino = cursor.fetchall()

        if not areas_destino:
            conexion.rollback()
            print("No hay otras áreas disponibles para derivar.")
            return

        print("\n===== ÁREAS DE DESTINO DISPONIBLES =====")
        for idx, area in enumerate(areas_destino, 1):
            print(f"{idx}. {area['nombre']}")
        print("0. Cancelar")

        opcion_area = input("\nSeleccione el número del área de destino: ").strip()
        if opcion_area == "0" or not opcion_area.isdigit():
            conexion.rollback()
            print("Operación cancelada.")
            return

        indice = int(opcion_area) - 1
        if not (0 <= indice < len(areas_destino)):
            conexion.rollback()
            print("Opción de área no válida.")
            return

        id_area_destino = areas_destino[indice]["id_area"]
        nombre_area_destino = areas_destino[indice]["nombre"]

        # 5. Solicitar motivo y observaciones obligatorias/opcionales
        # Por qué: Toda transferencia en una municipalidad exige justificación legal o administrativa.
        motivo = input("Ingrese el motivo de la derivación: ").strip()
        if not motivo:
            conexion.rollback()
            print("El motivo es obligatorio.")
            return

        observaciones = input("Ingrese observaciones adicionales (opcional): ").strip()

        # Confirmación final por seguridad del usuario antes de ejecutar la BD
        confirmar = input(f"\n¿Confirmar derivación al área '{nombre_area_destino}'? (S/N): ").strip().upper()
        if confirmar != "S":
            conexion.rollback()
            print("Operación cancelada.")
            return

        # 6. Actualizar el expediente: cambiar su área actual y actualizar su estado a 'Derivado'
        # Por qué: Mantiene la tabla principal 'expediente' sincronizada con su ubicación actual.
        nuevo_estado = "Derivado"
        cursor.execute("""
            UPDATE expediente 
            SET id_area = %s, estado = %s 
            WHERE id_expediente = %s
        """, (id_area_destino, nuevo_estado, expediente["id_expediente"]))

        # 7. Registrar el movimiento en la tabla 'derivacion'
        # Por qué: Guarda el historial detallado de origen, destino, motivo y responsable 
        # tal como lo exige el requerimiento del proyecto.
        cursor.execute("""
            INSERT INTO derivacion (fecha_derivacion, motivo, observaciones, id_expediente, id_area_origen, id_area_destino, id_usuario)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s)
        """, (
            motivo, 
            observaciones if observaciones else None, 
            expediente["id_expediente"], 
            id_area_origen, 
            id_area_destino, 
            id_usuario
        ))

        # 8. Registrar también en la tabla 'seguimiento'
        # Por qué: Permite que el módulo de consultas de tus compañeros (service.py y routes.py) 
        # muestre este movimiento cronológicamente en el historial del ciudadano o del trabajador.
        detalle_seguimiento = f"Derivado a {nombre_area_destino}. Motivo: {motivo}"
        if observaciones:
            detalle_seguimiento += f" - Obs: {observaciones}"

        cursor.execute("""
            INSERT INTO seguimiento (fecha, estado, observacion, id_usuario, id_expediente)
            VALUES (NOW(), %s, %s, %s, %s)
        """, (
            nuevo_estado,
            detalle_seguimiento[:200], # Limitado para no exceder el varchar de la BD
            id_usuario,
            expediente["id_expediente"]
        ))

        # 9. Confirmar todos los cambios juntos (Commit)
        # Por qué: Si todas las consultas anteriores salieron bien, se aplican definitivamente en MySQL.
        conexion.commit()
        print(f"\n[OK] ¡Expediente derivado exitosamente a la unidad de {nombre_area_destino}!")

    except Exception as e:
        # Si ocurre cualquier error inesperado, se deshace todo (Rollback)
        conexion.rollback()
        print(f"\n[!] Error crítico al procesar la derivación: {e}")
    finally:
        # Siempre cerramos el cursor para liberar memoria del servidor de base de datos
        cursor.close()