from solicitudes.extra import titulo_menu, validar_dni, ROL_ADMIN, ROL_TRABAJADOR

def gestionar_personal_areas(usuario):

    #Condición para validar que rol de usuario sea Administrador
    if usuario["id_rol"] != ROL_ADMIN:
        print("No tiene permisos para registrar personal.")

        return