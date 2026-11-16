# Importa funciones auxiliares y constantes de roles
from solicitudes.extra import titulo_menu, ROL_TRABAJADOR

# [TD] Crear función con un submenú interactivo donde se seleccione el criterio específico de búsqueda entre código de expediente, asunto, DNI o correo del ciudadano.
def buscar_tramites_area(usuario):

    # Verifica que el usuario tenga rol de trabajador y un área asignada
    if usuario.get("id_rol") != ROL_TRABAJADOR or usuario.get("id_area") is None:
        print("Acceso denegado. Esta opción es exclusiva para trabajadores con área asignada.")
        return

    # Bucle interactivo del submenú de búsqueda
    while True:
        titulo_menu("Buscar trámites de mi área")
        if usuario.get("nombre_area") is not None:
            print(f"Área: {usuario['nombre_area']}")
        print("-" * 50)
        print(" 1. Buscar por código de expediente")
        print(" 2. Buscar por asunto")
        print(" 3. Buscar por DNI del ciudadano")
        print(" 4. Buscar por correo del ciudadano")
        print(" 5. Volver al menú")

        eleccion = input("\nSeleccione una opción: ").strip()

        # Valida que la opción ingresada sea un número válido dentro del rango
        if not eleccion.isdigit() or not 1 <= int(eleccion) <= 5:
            input("\nOpción no válida. Presione Enter para reintentar.")
            continue

        opcion = int(eleccion)

        if opcion == 5:
            return

        # Espacio reservado para la siguiente actividad de desarrollo
        input(f"\nOpción {opcion} seleccionada. Presione Enter para continuar.")