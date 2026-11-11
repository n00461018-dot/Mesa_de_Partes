# Módulo para la gestión y búsqueda global de expedientes (Solo Administrador)
from mysql.connector import Error

def buscar_expedientes_todas_las_areas(conexion, usuario):
    """
    Función principal para buscar expedientes de todas las áreas.
    Valida primero que el usuario tenga rol de Administrador.
    """
    # 1. Validación de seguridad alineada al estándar del proyecto (id_rol == 1 para Administrador)
    if usuario.get("id_rol") != 1:
        print("\n[ACCESO DENEGADO] No tienes permisos de Administrador para realizar esta búsqueda global.")
        return

    print("\n--- BÚSQUEDA GLOBAL DE EXPEDIENTES (TODAS LAS ÁREAS) ---")
    
    # Solicitamos al administrador el criterio de búsqueda (número de expediente, DNI, área, etc.)
    filtro_texto = input("Ingrese el número de expediente, DNI, área o término a buscar (Enter para ver todo): ").strip()

    print("\nProcesando búsqueda global...")
    
    # Llamamos a la función auxiliar enviándole el filtro ingresado por consola
    resultados = _consultar_todos_los_expedientes_bd(conexion, filtro_texto)
    
    # Validamos si ocurrió un error en la consulta (retorna False)
    if resultados is False:
        print("\n[!] Ocurrió un error al consultar la base de datos.")
        return
        
    # Validamos si la lista está vacía (Criterio de aceptación Trello: "Si no hay resultados, se informa al usuario")
    if not resultados:
        print("\n[!] No se encontraron expedientes coincidentes en el sistema.")
        return

    print(f"\n[OK] Se encontraron {len(resultados)} expediente(s) en total.")
    
    # Nota: Los datos detallados de la búsqueda se mostrarán en el siguiente commit con formato tabular.
    for exp in resultados:
        print(f"- Expediente: {exp['numero_expediente']} | Área: {exp['nombre_area']} | Estado: {exp['estado']}")


def _consultar_todos_los_expedientes_bd(conexion, filtro_texto=""):
    """
    Función auxiliar para ejecutar el SELECT avanzado con JOIN y 
    filtros dinámicos seguros mediante parámetros SQL contra inyecciones.
    """
    cursor = None
    try:
        # Se inicializa el cursor configurado en diccionario (dictionary=True) 
        # para que los registros se devuelvan como diccionarios clave-valor.
        cursor = conexion.cursor(dictionary=True)
        
        # Consulta SQL base uniendo las tablas clave del sistema sin restricciones de área
        sql = """
            SELECT 
                e.id_expediente,
                e.numero_expediente,
                e.fecha_registro,
                e.asunto,
                e.estado,
                tt.nombre AS tipo_tramite,
                a.nombre AS nombre_area,
                u.dni AS dni_ciudadano,
                CONCAT(u.nombre, ' ', u.apellido) AS ciudadano_propietario
            FROM expediente e
            INNER JOIN tipo_tramite tt ON e.id_tipo_tramite = tt.id_tipo_tramite
            INNER JOIN area a ON e.id_area = a.id_area
            LEFT JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
            LEFT JOIN usuario u ON c.id_usuario = u.id_usuario
        """
        
        parametros = []
        
        # Si el administrador ingresa texto, agregamos la cláusula WHERE con LIKE de manera segura
        if filtro_texto:
            sql += """ 
                WHERE e.numero_expediente LIKE %s 
                   OR tt.nombre LIKE %s 
                   OR a.nombre LIKE %s 
                   OR u.dni LIKE %s 
                   OR u.nombre LIKE %s 
                   OR u.apellido LIKE %s
            """
            # Creamos el patrón con comodines '%' para búsquedas parciales
            patron = f"%{filtro_texto}%"
            # Asignamos el valor para cada uno de los 6 parámetros de la consulta
            parametros = [patron, patron, patron, patron, patron, patron]
            
        # Ordenamos los resultados del más reciente al más antiguo
        sql += " ORDER BY e.fecha_registro DESC"
        
        # Se ejecuta la sentencia SQL pasando los parámetros de forma segura (previene Inyección SQL)
        cursor.execute(sql, tuple(parametros))
        
        # Retorna todos los registros resultantes
        return cursor.fetchall()

    except Error as e:
        # Captura errores de MySQL
        print(f"Error al consultar los expedientes en la base de datos: {e}")
        return False
    finally:
        # Bloque de seguridad para cerrar el cursor y liberar memoria
        if cursor is not None:
            cursor.close()