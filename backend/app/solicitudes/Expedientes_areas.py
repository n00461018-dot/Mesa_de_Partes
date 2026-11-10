# Módulo para la gestión y búsqueda global de expedientes (Solo Administrador)
from mysql.connector import Error

def buscar_expedientes_todas_las_areas(conexion, usuario):
    """
    Función principal para buscar expedientes de todas las áreas.
    Valida primero que el usuario tenga rol de Administrador.
    """
    # 1. Validación de seguridad: Verificar si el usuario es Administrador
    # (Asumiendo que el diccionario 'usuario' tiene una clave 'rol' o 'id_rol')
    rol_usuario = usuario.get('rol', '').lower()
    
    if rol_usuario != 'administrador' and rol_usuario != 'admin':
        print("\n[ACCESO DENEGADO] No tienes permisos de Administrador para realizar esta búsqueda global.")
        return

    print("\n--- BÚSQUEDA GLOBAL DE EXPEDIENTES (TODAS LAS ÁREAS) ---")
    print("Acceso concedido. Preparando consulta...")
    
    # Llamamos a la función auxiliar para obtener los datos de la base de datos
    resultados = _consultar_todos_los_expedientes_bd(conexion)
    
    # Validamos si ocurrió un error en la consulta (retorna False)
    if resultados is False:
        print("\n[!] Ocurrió un error al consultar la base de datos.")
        return
        
    # Validamos si la lista está vacía (criterio de aceptación: "si no hay resultados, se informa al usuario")
    if not resultados:
        print("\n[!] No se encontraron expedientes registrados en el sistema.")
        return

    print(f"\n[OK] Se encontraron {len(resultados)} expediente(s) en total.")


def _consultar_todos_los_expedientes_bd(conexion):
    """
    Función auxiliar para ejecutar el SELECT avanzado con JOIN 
    para listar todos los expedientes sin restricciones de área.
    """
    cursor = None
    try:
        # Se inicializa el cursor configurado en diccionario (dictionary=True) 
        # para que los registros se devuelvan como diccionarios clave-valor, 
        # facilitando la lectura de columnas como exp['estado'].
        cursor = conexion.cursor(dictionary=True)
        
        # Consulta SQL global uniendo las tablas clave del sistema sin restricciones de área
        sql = """
            SELECT 
                e.id_expediente,
                e.numero_expediente,
                e.fecha_registro,
                e.estado,
                tt.nombre AS tipo_tramite,
                a.nombre AS nombre_area,
                CONCAT(u.nombre, ' ', u.apellido) AS ciudadano_propietario
            FROM expediente e
            INNER JOIN tipo_tramite tt ON e.id_tipo_tramite = tt.id_tipo_tramite
            INNER JOIN area a ON e.id_area = a.id_area
            LEFT JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
            LEFT JOIN usuario u ON c.id_usuario = u.id_usuario
            ORDER BY e.fecha_registro DESC
        """
        
        # Se ejecuta la sentencia SQL en MySQL
        cursor.execute(sql)
        
        # Se obtienen todos los registros resultantes de la consulta
        return cursor.fetchall()

    except Error as e:
        # Captura cualquier excepción o error de MySQL para evitar que la aplicación se caiga
        print(f"Error al consultar los expedientes en la base de datos: {e}")
        return False
    finally:
        # El bloque finally garantiza que el cursor se cierre siempre, 
        # liberando recursos de memoria en la conexión, tal como lo hace el resto del equipo.
        if cursor is not None:
            cursor.close()