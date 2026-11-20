from solicitudes.extra import titulo_menu, validar_dni, seleccionar_de_lista, ROL_ADMIN, ROL_TRABAJADOR
from solicitudes.ciudadanos import ErrorBD, pedir_campo, validar_correo, _obligatorio, _validar_dni_nuevo, _validar_correo_nuevo
from mysql.connector import Error
from database.conexion_bd import conectar_bd


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


    return None