# Define la función para gestionar el inicio de sesión del administrador
def login_admin():
    # Imprimimos el inicio del LOGIN ADMINISTRADOR
    print("\n--- LOGIN ADMINISTRADOR ---")
    # Solicita el nombre de usuario por consola y remueve espacios en blanco al inicio y al final
    usuario = input("Usuario Admin: ").strip()
    # Solicita la contraseña por consola y remueve espacios en blanco al inicio y al final
    clave = input("Contraseña: ").strip()

    # Comprueba si el usuario ingresado es "admin" y la contraseña es "1234"
    if usuario == "admin" and clave == "1234":
        # Informa en pantalla que el acceso fue concedido al rol de administrador
        print("Acceso concedido: Administrador")
        # Retorna True indicando autenticación exitosa
        return True
    # En caso de que las credenciales no coincidan con los valores esperados
    else:
        # Informa en pantalla que las credenciales ingresadas son erróneas
        print("Credenciales de administrador incorrectas.")
        # Retorna False indicando que falló el inicio de sesión
        return False


# Define la función para gestionar el inicio de sesión de empleados de planilla
def login_empleado():
    # Imprimimos el inicio del LOGIN EMPLEADO
    print("\n--- LOGIN EMPLEADO (PLANILLA) ---")
    # Solicita el código de planilla y remueve los espacios en blanco sobrantes
    codigo = input("Código de planilla: ").strip()
    # Solicita la contraseña del empleado y remueve los espacios en blanco sobrantes
    clave = input("Contraseña: ").strip()

    # Verifica si el código es exactamente "emp01" y la contraseña es "muni"
    if codigo == "emp01" and clave == "muni":
        # Muestra en consola que la autenticación del empleado fue exitosa
        print("Acceso concedido: Empleado en planilla")
        # Retorna True confirmando el acceso correcto
        return True
    # En caso de que el código o la clave no sean correctos
    else:
        # Muestra un mensaje notificando el error de credenciales
        print("Credenciales de empleado incorrectas.")
        # Retorna False impidiendo el acceso
        return False


# Define la función para gestionar el inicio de sesión de ciudadanos o clientes
def login_cliente():
    # Imprimimos el inicio del LOGIN CLIENTE
    print("\n--- LOGIN CIUDADANO (CLIENTE) ---")
    # Solicita el número de DNI y elimina los espacios en blanco accidentales
    dni = input("Ingrese su DNI: ").strip()
    # Solicita la contraseña del ciudadano y elimina los espacios en blanco accidentales
    clave = input("Contraseña: ").strip()

    # Compara si el DNI es "12345678" y la contraseña corresponde a "abcd"
    if dni == "12345678" and clave == "abcd":
        # Notifica al usuario que su inicio de sesión como ciudadano ha sido exitoso
        print("Acceso concedido: Ciudadano")
        # Retorna True indicando que la verificación fue aprobada
        return True
    # Si el DNI o la contraseña no coinciden
    else:
        # Informa en consola que los datos ingresados no son válidos
        print("DNI o contraseña incorrectos.")
        # Retorna False denegando el ingreso
        return False