# Importa funciones auxiliares y constantes de roles
from solicitudes.extra import titulo_menu, ROL_TRABAJADOR, validar_dni


# [T.D] Procesar la captura de la búsqueda exacta o parcial que el usuario desea encontrar según la opción elegida en el submenú.
def capturar_valor_busqueda(opcion):
    etiquetas = {
        1: ("código", "Ingrese el código de expediente (exacto o parcial): "),
        2: ("asunto", "Ingrese el asunto o palabra clave: "),
        3: ("dni", "Ingrese el DNI del ciudadano (8 dígitos): "),
        4: ("correo", "Ingrese el correo del ciudadano: "),
    }

    criterio, mensaje = etiquetas[opcion]

    while True:
        valor = input(f"\n{mensaje}").strip()

        # Evita búsquedas vacías o con solo espacios en blanco
        if not valor:
            print("Aviso: El campo de búsqueda no puede estar vacío.")
            continue

        # Si el criterio es DNI, reutiliza la validación estricta de extra.py
        if criterio == "dni":
            error_dni = validar_dni(valor)
            if error_dni is not None:
                print(f"Aviso: {error_dni}")
                continue

        return criterio, valor

# [T.D] Crear función con un submenú interactivo donde se seleccione el criterio específico de búsqueda entre código de expediente, asunto, DNI o correo del ciudadano.
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

        # Captura y valida el valor según el criterio elegido
        criterio, valor_busqueda = capturar_valor_busqueda(opcion)

        # Espacio reservado para la consulta SQL (siguiente actividad)
        input(f"\nCriterio '{criterio}' con valor '{valor_busqueda}' listo. Presione Enter para continuar.")