# Módulo para la gestión y búsqueda global de expedientes (Solo Administrador)
from mysql.connector import Error
from database.conexion_bd import conectar_bd
from solicitudes.extra import titulo_menu

def _mostrar_tabla_expedientes(expedientes):
    """
    Función auxiliar para mostrar los expedientes en un formato tabular 
    alineado en consola, respetando el estándar visual del proyecto.
    """
    if not expedientes or len(expedientes) == 0:
        print("\n[!] No hay datos para mostrar.")
        return

    # Cabecera de la tabla con anchos de columna fijos
    print(f"{'N° Exp.':<12} | {'Tipo Trámite':<24} | {'Área Responsable':<24} | {'Estado':<12} | {'Fecha':<16}")
    print("-" * 96)
    
    # Recorremos la lista para alinear textualmente cada columna y formatear la fecha
    for e in expedientes:
        fecha_str = ""
        if e.get("fecha_registro"):
            fecha_str = e["fecha_registro"].strftime("%d/%m/%Y %H:%M")
            
        num_exp = str(e.get("numero_expediente", ""))[:12]
        tipo_t = str(e.get("tipo_tramite", ""))[:24]
        area_n = str(e.get("nombre_area", ""))[:24]
        estado = str(e.get("estado", ""))[:12]
        
        print(f"{num_exp:<12} | {tipo_t:<24} | {area_n:<24} | {estado:<12} | {fecha_str:<16}")
        
    print("-" * 96)
    print(f"Total de expedientes listados: {len(expedientes)}")

def buscar_expedientes_todas_las_areas(usuario):
    """
    Función principal para buscar expedientes de todas las áreas.
    Valida el rol de Administrador y gestiona su propia conexión a la BD.
    """
    # [T.D] Desarrollar la función de búsqueda global sin filtros restrictivos de área para el rol de administrador.
    if usuario.get("id_rol") != 1:
        print("\n[ACCESO DENEGADO] No tienes permisos de Administrador para realizar esta búsqueda global.")
        return
    
    conexion = conectar_bd()
    if conexion is None:
        print("\n[!] No se pudo conectar a la base de datos.")
        return
    try:
        titulo_menu("Búsqueda Global de Expedientes")
        print("Supervisión global de trámites a nivel de toda la municipalidad.\n")
        
        filtro_texto = input("Ingrese N° de expediente, DNI, área o término (Enter para ver todos): ").strip()
        print("\nProcesando búsqueda global...")
        
        resultados = _consultar_todos_los_expedientes_bd(conexion, filtro_texto)
        
        if resultados is False:
            print("\n[!] Ocurrió un error al consultar la base de datos.")
            return
        # [T.D] Implementar una validación condicional que compruebe si la consulta arrojó registros para mostrar el mensaje de "sin resultados" en caso de estar vacía.
        if not resultados:
            print("\n[!] No se encontraron expedientes coincidentes en el sistema.")
            return

        print(f"\n[OK] Se encontraron {len(resultados)} coincidencia(s):\n")
        _mostrar_tabla_expedientes(resultados)

    finally:
        conexion.close()

def _consultar_todos_los_expedientes_bd(conexion, filtro_texto=""):
    """
    Función auxiliar para ejecutar el SELECT avanzado con JOIN y 
    filtros dinámicos seguros mediante parámetros SQL contra inyecciones.
    """
    cursor = None
    try:
        # Se inicializa el cursor configurado en diccionario (dictionary=True)
        cursor = conexion.cursor(dictionary=True)
        
        # [T.D] Obtener el nombre del área responsable y el estado actual del trámite.
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
        # [T.D] Programar consultas SQL para buscar por número de expediente o Usuario en la base de datos.
        # Si el administrador ingresa texto, agregamos la cláusula WHERE con LIKE
        if filtro_texto:
            sql += """ 
                WHERE e.numero_expediente LIKE %s 
                   OR tt.nombre LIKE %s 
                   OR a.nombre LIKE %s 
                   OR u.dni LIKE %s 
                   OR u.nombre LIKE %s 
                   OR u.apellido LIKE %s
            """
            patron = f"%{filtro_texto}%"
            parametros = [patron, patron, patron, patron, patron, patron]
            
        sql += " ORDER BY e.fecha_registro DESC"
        
        # Se ejecuta la sentencia SQL con los parámetros sanitizados en tupla
        cursor.execute(sql, tuple(parametros))
        
        return cursor.fetchall()
    
    except Error as e:
        print(f"Error al consultar los expedientes en la base de datos: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()