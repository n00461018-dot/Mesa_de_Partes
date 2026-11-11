import time

# SIMULACION DE ENVÍO DE CORREOS

def enviar_copia_tramite_correo(correo_destino, numero_expediente, asunto_tramite):
    """
    Simula el envío de un correo al ciudadano con la copia de su trámite
    inmediatamente después de registrarlo.
    """
    print("\n[SISTEMA] Generando copia del expediente para el ciudadano...")
    time.sleep(1)
    
    asunto_correo = f"Registro Exitoso - Expediente N° {numero_expediente}"
    cuerpo_correo = (
        f"Estimado ciudadano,\n"
        f"Su trámite sobre '{asunto_tramite}' ha sido ingresado correctamente a la Mesa de Partes.\n"
        f"Número de Expediente: {numero_expediente}\n"
        f"Se adjunta a este correo la copia de su registro."
    )
    print("\n[SISTEMA] Conectando con el servidor de correos...")
    time.sleep(1.5)
    print("=" * 50)
    print(f"DESTINATARIO : {correo_destino}")
    print(f"ASUNTO       : {asunto_correo}")
    print("=" * 50)
    print(f"{cuerpo_correo}")
    print("=" * 50)
    time.sleep(1)

    print(f"\n[OK] ¡Aviso! Se ha enviado una copia de respaldo a su correo: {correo_destino}")