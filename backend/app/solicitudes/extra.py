import os
import subprocess

ASUNTO_MIN, ASUNTO_MAX = 10, 300
ROL_ADMIN = 1
ROL_TRABAJADOR = 2
ROL_CIUDADANO = 3
NOMBRE_ARCHIVO_MAX = 150
EXTENSIONES_PERMITIDAS = ("pdf", "jpg", "docx")

# Función para crear el título de cada menú
def titulo_menu(titulo):
    titulo_ingresado = titulo.upper()
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("======================================================")
    print(f"    MESA DE PARTES SJL - {titulo_ingresado}")
    print("======================================================\n")


def validar_dni(dni):

    dni= str(dni).strip()

    #La función devuelve un mensaje en caso no sea dígito o no tenga 8 cifras
    #Se usa el método is digit que evalua el str
    if not (dni.isdigit() and len(dni) == 8):
        return "El DNI debe tener 8 dígitos numéricos."
    
    #Si la función devuelve None, pasa la validación
    return None


