import os
import subprocess


# Función para crear el título de cada menú
def titulo_menu(titulo):
    titulo_ingresado = titulo.upper()
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("======================================================")
    print(f"    MESA DE PARTES SJL - {titulo_ingresado}")
    print("======================================================\n")
