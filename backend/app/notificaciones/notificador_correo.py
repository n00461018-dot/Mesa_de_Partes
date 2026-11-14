from datetime import datetime
import re

class NotificadorCorreo:
    def __init__(self, db_conexion):
        self.db = db_conexion
        self.remitente_municipal = "mesadepartes@municipalidad.test"

    def registrar_respuesta(self, id_expediente, id_usuario, correo_destino, asunto, contenido):
        # Validación de campos obligatorios
        if not correo_destino or not asunto or not contenido:
            return {"exito": False, "mensaje": "Los campos correo, asunto y contenido son obligatorios."}

        cursor = self.db.cursor()
        
        query_insert = """
            INSERT INTO respuesta_correo 
            (correo_destino, asunto, contenido, fecha_envio, estado_envio, id_expediente, id_usuario)
            VALUES (%s, %s, %s, NULL, 'Pendiente', %s, %s)
        """
        valores = (correo_destino, asunto, contenido, id_expediente, id_usuario)
        
        try:
            cursor.execute(query_insert, valores)
            self.db.commit()
            return {
                "exito": True, 
                "mensaje": "Constancia registrada correctamente en la BD.",
                "id_respuesta": cursor.lastrowid
            }
        except Exception as e:
            self.db.rollback()
            return {"exito": False, "mensaje": f"Error al guardar en BD: {str(e)}"}
        finally:
            cursor.close()

    def enviar_correo(self, id_respuesta, correo_destino, asunto, contenido):
        cursor = self.db.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Validación simulada: comprobar que el correo tenga un formato válido (ej. usuario@dominio.com)
            if not re.match(r"[^@]+@[^@]+\.[^@]+", correo_destino):
                raise ValueError("Formato de correo electrónico inválido.")

            # Simulación visual del envío en consola
            print("\n" + "="*50)
            print("📧 SIMULACIÓN DE ENVÍO DE CORREO ELECTRÓNICO")
            print(f"De:      {self.remitente_municipal}")
            print(f"Para:    {correo_destino}")
            print(f"Asunto:  {asunto}")
            print(f"Fecha:   {fecha_actual}")
            print("-" * 50)
            print(f"{contenido}")
            print("="*50 + "\n")

            # Actualizar estado a "Enviado" y registrar la fecha en BD[cite: 24, 25]
            cursor.execute(
                """
                UPDATE respuesta_correo 
                SET estado_envio = 'Enviado', fecha_envio = %s 
                WHERE id_respuesta = %s
                """, 
                (fecha_actual, id_respuesta)
            )
            self.db.commit()
            return {"enviado": True, "mensaje": "Envío simulado con éxito. Estado actualizado a 'Enviado'."}

        except Exception as e:
            # Si falla la validación simulada, se marca como Error pero se mantiene el registro[cite: 24]
            cursor.execute(
                "UPDATE respuesta_correo SET estado_envio = 'Error' WHERE id_respuesta = %s", 
                (id_respuesta,)
            )
            self.db.commit()
            return {"enviado": False, "mensaje": f"Error en simulación de envío: {str(e)}"}
        finally:
            cursor.close()