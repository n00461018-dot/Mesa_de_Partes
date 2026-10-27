from datetime import datetime
from mysql.connector import Error

class DerivacionRepository:
    def __init__(self, conexion_db):
        self.db = conexion_db

    def derivar_expediente(self, id_expediente, id_area_origen, id_area_destino, motivo, observaciones, id_usuario):
        """
        Permite derivar un expediente de un área a otra, guardando:
        - Área original (id_area_origen)
        - Área destino (id_area_destino)
        - Motivo y observaciones
        - Responsable (id_usuario del empleado municipal)
        """
        """ observación: La función
        tiene que estar conectado a la base de datos para poder realizar la derivación."""
        if not self.db:
            return False, "No hay conexión a la base de datos."

        cursor = self.db.cursor()
        try:
            # 1. Registrar la derivación en la tabla 'derivacion'
            query_derivacion = """
                INSERT INTO derivacion (fecha_derivacion, motivo, observaciones, id_expediente, id_area_origen, id_area_destino, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            fecha_actual = datetime.now()
            cursor.execute(query_derivacion, (
                fecha_actual, motivo, observaciones, id_expediente, id_area_origen, id_area_destino, id_usuario
            ))

            # 2. Actualizar el área actual en la tabla principal 'expediente'
            query_update_expediente = """
                UPDATE expediente 
                SET id_area = %s 
                WHERE id_expediente = %s
            """
            cursor.execute(query_update_expediente, (id_area_destino, id_expediente))

            self.db.commit()
            return True, "Expediente derivado exitosamente entre áreas."
            
        except Error as e:
            self.db.rollback()
            return False, f"Error en la base de datos: {e}"
        finally:
            cursor.close()