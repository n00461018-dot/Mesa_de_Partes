from solicitudes.extra import titulo_menu, validar_dni, seleccionar_de_lista, ROL_ADMIN, ROL_TRABAJADOR
from solicitudes.ciudadanos import ErrorBD, pedir_campo, validar_correo, _obligatorio, _validar_dni_nuevo, _validar_correo_nuevo
from mysql.connector import Error
from database.conexion_bd import conectar_bd
from database.consultas_bd import listar_areas


#Se crea la función validar_datos_trabajador para la revisión del formato de datos
def validar_datos_trabajador(dni, nombre, apellido, correo, contrasena):

    #Se valida que ningun campo obligatorio este vacío o solo tenga espacios
    if "" in (dni.strip(), nombre.strip(), apellido.strip(), correo.strip(), contrasena.strip()):
        return "Todos los campos obligatorios deben ser completados."

    #Se usa la funcion validar_dni() de extra.py
    error_dni = validar_dni(dni)

    if error_dni is not None:
        return error_dni

    #Se reutiliza validar_correo() de ciudadanos.py
    if not validar_correo(correo.strip()):

        return "Ingrese un correo electrónico válido."
    return None

#Campos del formulario separado en la clave, el mensaje para el print y la funcion que valida el campo
CAMPOS_PERSONAL = [
    ("dni", "DNI (8 dígitos): ", _validar_dni_nuevo),
    ("nombre", "Nombres: ", _obligatorio),
    ("apellido", "Apellidos: ", _obligatorio),
    ("correo", "Correo electrónico: ", _validar_correo_nuevo),
    ("contrasena", "Contraseña: ", _obligatorio),
]

def _obtener_areas():
    conexion = conectar_bd()
    if conexion is None:
        return False
 
    try:
        return listar_areas(conexion)
    except Error as e:
        print(f"\nError: {e}")
        return False
    finally:
        conexion.close()

# Función para guardar el trabajador en la tabla 'usuario' con rol Trabajador y el área elegida
def registrar_trabajador_bd(dni, nombre, apellido, correo, contrasena, id_area):
    conexion = conectar_bd()
    if conexion is None:
        return False
 
    cursor = None
    try:
        cursor = conexion.cursor()
        # El rol se asigna automáticamente (Trabajador) y el área es la elegida por el administrador
        sql = """
            INSERT INTO usuario (dni, nombre, apellido, correo, contrasena, id_rol, id_area)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (dni, nombre, apellido, correo, contrasena, ROL_TRABAJADOR, id_area))
        conexion.commit()
        return True
 
    except Error as e:
        conexion.rollback()
        #Excepcion MYSQL con codigo 1062 es para registros de valores duplicados
        if e.errno == 1062:
            print("\nError: El DNI o el correo ya se encuentran registrados.")
        else:
            print(f"\nError: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()

#Se muestra el resumen de los datos ingresados y el área seleccionada
def _mostrar_resumen(datos, area):
    titulo_menu("Registrar Personal - Resumen")
    print("Verifique los datos del nuevo trabajador:")
    print("-" * 54)
    print(f" DNI         : {datos['dni']}")
    print(f" Nombres     : {datos['nombre']}")
    print(f" Apellidos   : {datos['apellido']}")
    print(f" Correo      : {datos['correo']}")
    print(f" Área        : {area['nombre']}")
    print(f" Rol         : Trabajador")
    print("-" * 54)

# Pide la confirmación S/N hasta recibir una respuesta válida
# Devuelve True si confirma (S) y False si cancela (N o 'salir')
def _confirmar_registro():
    while True:
        respuesta = input("\n¿Desea confirmar el registro? (S/N): ").strip().upper()
        if respuesta == "S":
            return True
        if respuesta in ("N", "SALIR"):
            return False
        print("\nError: Debe ingresar S o N.")
 
 
def _cancelar_registro():
    print("\nRegistro cancelado. No se guardó ningún dato.")

#Función principal para ejecutar el registro de personal en la tabla usuario con las validaciones y formato válido
def registrar_personal(usuario):

    #Condición para validar que el rol del usuario sea Administrador
    if usuario["id_rol"] != ROL_ADMIN:
        print("No tiene permisos para registrar personal.")
        return
 
    try:
        titulo_menu("Registrar Personal")
        print("Complete los datos del trabajador (o escriba 'salir' para cancelar).")
        print("-" * 54)
 
        #Pedir y validar cada campo al momento de ingresarlo (en cualquiera se puede cancelar)
        datos = {}
        for clave, mensaje, validar in CAMPOS_PERSONAL:
            valor = pedir_campo(mensaje, validar)
            if valor is None:
                _cancelar_registro()
                return
            datos[clave] = valor
 
        #Revisión final del formato de todo el registro
        error = validar_datos_trabajador(
            datos["dni"], datos["nombre"], datos["apellido"],
            datos["correo"], datos["contrasena"]
        )
        if error is not None:
            print(f"\nError: {error}")
            return
 
        #Consultar las areas y pedir que el administrador seleccione de una de la lista numerada
        areas = _obtener_areas()
        if areas is False:
            print("\nNo se pudo consultar las áreas en la base de datos.")
            return
        if len(areas) == 0:
            print("\nNo hay áreas registradas. No se puede registrar personal.")
            return
 
        print("-" * 54)
        area = seleccionar_de_lista(
            areas, campo="nombre", titulo="ÁREAS MUNICIPALES",
            mensaje="Seleccione el área del trabajador: ", cancelar=("salir",)
        )
        if area is None:
            _cancelar_registro()
            return
 
        #Mostrar el resumen y pedir confirmación antes de guardar
        _mostrar_resumen(datos, area)
        if not _confirmar_registro():
            _cancelar_registro()
            return
 
        #Guardar en la tabla 'usuario' con rol Trabajador y el área elegida
        exito = registrar_trabajador_bd(
            datos["dni"], datos["nombre"], datos["apellido"],
            datos["correo"], datos["contrasena"], area["id_area"]
        )
 
        if exito:
            print(f"\n¡Trabajador {datos['nombre']} {datos['apellido']} "
                  f"(DNI: {datos['dni']}) registrado exitosamente en el área '{area['nombre']}'!")
        else:
            print("\nNo se pudo completar el registro del trabajador.")
 
    except ErrorBD:
        print("\nNo se pudo verificar la información en la base de datos.")
 