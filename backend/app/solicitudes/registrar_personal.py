from solicitudes.extra import titulo_menu, validar_dni, ROL_ADMIN, ROL_TRABAJADOR

def gestionar_personal_areas(usuario):

    #Condición para validar que rol de usuario sea Administrador
    if usuario["id_rol"] != ROL_ADMIN:
        print("No tiene permisos para registrar personal.")

        return

#Se crea la función validar_datos_trabajador para la revisión del formato de datos
def validar_datos_trabajador(dni, nombre, apellido, correo, contrasena, telefono=None):

#Se valida que ningun campo obligatorio este vacío o solo tenga espacios
if "" in (dni.strip(), nombre.strip(), apellido.strip(), correo.strip(), contrasena.strip()):
    return "Todos los campos obligatorios deben ser completados."

#Se usa la funcion validar_dni() de extra.py
error_dni = validar_dni(dni)

if error_dni is not None:
    return error_dni

# Reutiliza validar_correo() de ciudadanos.py
if not validar_correo(correo):

    return "Ingrese un correo electrónico válido."



# Reutiliza validar_telefono() de ciudadanos.py si se ingresa teléfono

if telefono is not None and str(telefono).strip() != "":
    if not validar_telefono(str(telefono).strip()):
        return "El teléfono debe contener entre 7 y 15 dígitos numéricos."

return None