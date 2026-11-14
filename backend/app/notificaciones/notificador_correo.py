from datetime import datetime
import re
from database.conexion_bd import conectar_bd
from solicitudes.extra import titulo_menu

class NotificadorCorreo:
    def __init__(self, db_conexion):
        self.db = db_conexion
        self.remitente_municipal = "mesadepartes@municipalidad.test"

    def registrar_respuesta(self, id_expediente, id_usuario, correo_destino, asunto, contenido, enviar_inmediato=False):
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
            id_respuesta_generado = cursor.lastrowid
            
            resultado = {
                "exito": True, 
                "mensaje": f"Constancia registrada correctamente con ID #{id_respuesta_generado} (Estado: Pendiente).",
                "id_respuesta": id_respuesta_generado
            }

            if enviar_inmediato:
                envio = self.simular_envio_correo(id_respuesta_generado, correo_destino, asunto, contenido)
                resultado["detalle_envio"] = envio

            return resultado

        except Exception as e:
            self.db.rollback()
            return {"exito": False, "mensaje": f"Error al guardar en BD: {str(e)}"}
        finally:
            cursor.close()

    def simular_envio_correo(self, id_respuesta, correo_destino, asunto, contenido):
        cursor = self.db.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", correo_destino):
                raise ValueError("Formato de correo electrónico inválido.")

            print("\n" + "=" * 54)
            print("ENVÍO DE CORREO ELECTRÓNICO")
            print(f" De:      {self.remitente_municipal}")
            print(f" Para:    {correo_destino}")
            print(f" Asunto:  {asunto}")
            print(f" Fecha:   {fecha_actual}")
            print("-" * 54)
            print(f" {contenido}")
            print("=" * 54 + "\n")

            cursor.execute(
                """
                UPDATE respuesta_correo 
                SET estado_envio = 'Enviado', fecha_envio = %s 
                WHERE id_respuesta = %s
                """, 
                (fecha_actual, id_respuesta)
            )
            self.db.commit()
            return {"enviado": True, "mensaje": "Correo enviado (simulado) y estado actualizado a 'Enviado'."}

        except Exception as e:
            cursor.execute(
                "UPDATE respuesta_correo SET estado_envio = 'Error' WHERE id_respuesta = %s", 
                (id_respuesta,)
            )
            self.db.commit()
            return {"enviado": False, "mensaje": f"Fallo en simulación de envío: {str(e)}"}
        finally:
            cursor.close()

# FUNCIÓN PRINCIPAL DEL MÓDULO (CON CONEXIÓN INTERNA)
def menu_respuesta_correo(usuario):
    # Validar que sea Administrador (1) o Trabajador (2)
    if usuario["id_rol"] not in (1, 2):
        print("No tiene permiso para registrar respuestas por correo.")
        return

    conexion = conectar_bd()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    notificador = NotificadorCorreo(conexion)
    id_usuario = usuario["id_usuario"]

    try:
        while True:
            titulo_menu("Registrar respuesta por correo")
            print(" 1. Registrar nueva respuesta por correo")
            print(" 2. Enviar un correo que quedó 'Pendiente'")
            print(" 3. Volver al menú anterior")
            print("-" * 50)
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                try:
                    id_exp = int(input("\nID del Expediente: ").strip())
                except ValueError:
                    input("\nEl ID del expediente debe ser numérico. Presione Enter para continuar.")
                    continue

                correo = input("Correo de destino: ").strip()
                asunto = input("Asunto: ").strip()
                contenido = input("Contenido del mensaje: ").strip()
                
                enviar_ahora = input("¿Deseas enviar el correo ahora mismo? (s/n): ").strip().lower()
                enviar_inmediato = (enviar_ahora == 's')

                resultado = notificador.registrar_respuesta(
                    id_expediente=id_exp,
                    id_usuario=id_usuario,
                    correo_destino=correo,
                    asunto=asunto,
                    contenido=contenido,
                    enviar_inmediato=enviar_inmediato
                )
                
                print("\n" + resultado["mensaje"])
                if "detalle_envio" in resultado:
                    print(resultado["detalle_envio"]["mensaje"])
                input("\nPresione Enter para continuar...")

            elif opcion == "2":
                try:
                    id_resp = int(input("\nIngresa el ID de la respuesta pendiente a enviar: ").strip())
                except ValueError:
                    input("\nEl ID debe ser numérico. Presione Enter para continuar.")
                    continue

                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM respuesta_correo WHERE id_respuesta = %s", (id_resp,))
                registro = cursor.fetchone()
                cursor.close()

                if not registro:
                    print("\nNo se encontró ninguna respuesta con ese ID.")
                elif registro["estado_envio"] == "Enviado":
                    print("\nEse correo ya figura como 'Enviado'.")
                else:
                    res_envio = notificador.simular_envio_correo(
                        id_respuesta=registro["id_respuesta"],
                        correo_destino=registro["correo_destino"],
                        asunto=registro["asunto"],
                        contenido=registro["contenido"]
                    )
                    print(res_envio["mensaje"])
                input("\nPresione Enter para continuar...")

            elif opcion == "3":
                break
            else:
                input("\nOpción no válida. Presione Enter para reintentar.")
    finally:
        conexion.close()