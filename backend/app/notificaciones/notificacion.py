import time

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