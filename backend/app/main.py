import sys

# Evita que Python cree las carpetas __pycache__ (.pyc) al ejecutar el sistema
# Debe ir antes de importar los módulos del proyecto
sys.dont_write_bytecode = True

from solicitudes.extra import titulo_menu
from auth.login import pantalla_login
from solicitudes.menu import ejecutar_menu
from solicitudes.ciudadanos import pantalla_registrar_ciudadano

# FUNCIÓN PRINCIPAL DEL SISTEMA
def main():

    while True:
        titulo_menu("Bienvenido al Sistema")
        print(" 1. Iniciar sesión (DNI o correo)")
        print(" 2. Registrarse como nuevo ciudadano")
        print(" 3. Salir del sistema")
        print("-" * 54)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            usuario = pantalla_login()
            if usuario is not None:
                ejecutar_menu(usuario)
        elif opcion == "2":
            pantalla_registrar_ciudadano()
        elif opcion == "3": 
            titulo_menu("Salida")
            print("El sistema se ha cerrado correctamente.")
            break
        else:
            input("\nOpción no válida. Presione Enter para reintentar.")


# Punto de entrada principal del programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C en cualquier pantalla, se cierra sin mostrar el error de Python
        # (las conexiones abiertas se cierran en los bloques finally de cada módulo)
        print("\n\nEl sistema se ha cerrado correctamente.")
