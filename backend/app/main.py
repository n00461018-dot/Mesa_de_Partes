from solicitudes.extra import titulo_menu
from auth.login import pantalla_login
from solicitudes.menu import ejecutar_menu

# FUNCIÓN PRINCIPAL DEL SISTEMA
def main():
    # Las funciones de pantalla_login y ejecutar_menu se repiten al cerrar sesión
    while True:
        # Se pide el login; si el usuario escribe 'salir' o supera los intentos devuelve None
        usuario = pantalla_login()
        if usuario is None:
            titulo_menu("Salida")
            print("El sistema se ha cerrado correctamente.")
            break

        # Si el login fue correcto, se abre el menú dinámico según su rol
        ejecutar_menu(usuario)


# Punto de entrada principal del programa
if __name__ == "__main__":
    main()
