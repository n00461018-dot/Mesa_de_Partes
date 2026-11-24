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
            print(" ENVÍO DE CORREO ELECTRÓNICO")
            print(" ")
            print(f" De:      {self.remitente_municipal}")
            print(f" Para:    {correo_destino}")
            print(f" Asunto:  {asunto}")
            print(f" Fecha:   {fecha_actual}")
            print("-" * 54)
            print(f"Contenido: {contenido}")
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
            return {"enviado": True, "mensaje": "[OK] Correo enviado a la bandeja del destinatario y estado actualizado a 'Enviado'."}

        except Exception as e:
            cursor.execute(
                "UPDATE respuesta_correo SET estado_envio = 'Error' WHERE id_respuesta = %s", 
                (id_respuesta,)
            )
            self.db.commit()
            return {"enviado": False, "mensaje": f"[!] Fallo en el envío: {str(e)}"}
        finally:
            cursor.close()


# FUNCIÓN AUXILIAR PARA NO PERDER LO ESCRITO SI UN CAMPO QUEDA VACÍO
def _pedir_dato_obligatorio(etiqueta, validar_email=False):
    while True:
        valor = input(etiqueta).strip()
        if not valor:
            print("[!] Este campo es obligatorio. Por favor, ingréselo.\n")
            continue
        if validar_email and not re.match(r"[^@]+@[^@]+\.[^@]+", valor):
            print("[!] Formato de correo inválido (ej. usuario@dominio.com).\n")
            continue
        return valor


# PANTALLA PARA ADMINISTRADOR Y TRABAJADOR (REGISTRAR Y ENVIAR)
def menu_respuesta_correo(usuario):
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
                # Permitir buscar por ID interno o por el numero visible del expediente.
                while True:
                    expediente_str = input("\nID o numero de Expediente (0 para cancelar): ").strip()
                    if expediente_str == "0":
                        id_exp = None
                        break
                    if not expediente_str:
                        print("[!] Debe ingresar un ID o numero de expediente.")
                        continue

                    id_busqueda = int(expediente_str) if expediente_str.isdigit() else 0
                    cursor = conexion.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT e.id_expediente, e.numero_expediente, u.correo
                        FROM expediente e
                        INNER JOIN ciudadano c ON e.id_ciudadano = c.id_ciudadano
                        INNER JOIN usuario u ON c.id_usuario = u.id_usuario
                        WHERE e.id_expediente = %s OR e.numero_expediente = %s
                    """, (id_busqueda, expediente_str))
                    exp_info = cursor.fetchone()
                    cursor.close()

                    if not exp_info:
                        print(f"[!] No existe ningun expediente con el identificador '{expediente_str}'.")
                        continue
                    print(f"[Info] Expediente {exp_info['numero_expediente']} - Correo registrado del ciudadano: {exp_info['correo']}")
                    id_exp = exp_info["id_expediente"]
                    break

                if id_exp is None:
                    continue

                # Solicitar cada campo obligando a llenarlo sin borrar los anteriores
                correo = _pedir_dato_obligatorio("Correo de destino: ", validar_email=True)
                asunto = _pedir_dato_obligatorio("Asunto: ")
                contenido = _pedir_dato_obligatorio("Contenido del mensaje: ")
                
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


# BANDEJA DE ENTRADA DEL CIUDADANO EN CONSOLA
def bandeja_correos_ciudadano(usuario):
    if usuario["id_rol"] != 3:
        print("Esta bandeja es exclusiva para ciudadanos.")
        return

    conexion = conectar_bd()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        titulo_menu("Bandeja de Correos Recibidos")
        print(f"Bandeja de: {usuario['correo']}\n")

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT rc.id_respuesta, e.numero_expediente, rc.asunto, rc.contenido, rc.fecha_envio
            FROM respuesta_correo rc
            INNER JOIN expediente e ON rc.id_expediente = e.id_expediente
            WHERE rc.correo_destino = %s
              AND rc.estado_envio = 'Enviado'
            ORDER BY rc.fecha_envio DESC
        """, (usuario["correo"],))
        correos = cursor.fetchall()
        cursor.close()

        if not correos:
            print("No tiene mensajes nuevos en su bandeja de entrada.")
            return

        for c in correos:
            fecha = c["fecha_envio"].strftime("%d/%m/%Y %H:%M") if c["fecha_envio"] else "Sin fecha"
            print("=" * 54)
            print(f" De:         mesadepartes@municipalidad.test")
            print(f" Expediente: {c['numero_expediente']}")
            print(f" Fecha:      {fecha}")
            print(f" Asunto:     {c['asunto']}")
            print("-" * 54)
            print(f" {c['contenido']}")
            print("=" * 54 + "\n")

        print(f"Total de correos recibidos: {len(correos)}")
    finally:
        conexion.close()