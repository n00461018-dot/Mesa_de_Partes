import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class NotificadorCorreo:
    def __init__(self, db_conexion):
        self.db = db_conexion
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_user = "tu_correo_municipalidad@gmail.com"
        self.smtp_pass = "tu_contraseña_de_aplicacion"

    def registrar_respuesta(self, id_expediente, id_usuario, correo_destino, asunto, contenido):
        # Validación de campos obligatorios
        if not correo_destino or not asunto or not contenido:
            return {"exito": False, "mensaje": "Los campos correo, asunto y contenido son obligatorios."}

        cursor = self.db.cursor()
        
        # Guardado inicial con estado "Pendiente" y sin fecha de envío aún
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