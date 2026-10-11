def login_admin():
    print("\n--- LOGIN ADMINISTRADOR ---")
    usuario = input("Usuario Admin: ").strip()
    clave = input("Contraseña: ").strip()

    if usuario == "admin" and clave == "1234":
        print("Acceso concedido: Administrador")
        return True
    else:
        print("Credenciales de administrador incorrectas.")
        return False


def login_empleado():
    print("\n--- LOGIN EMPLEADO (PLANILLA) ---")
    codigo = input("Código de planilla: ").strip()
    clave = input("Contraseña: ").strip()

    if codigo == "emp01" and clave == "muni":
        print("Acceso concedido: Empleado en planilla")
        return True
    else:
        print("Credenciales de empleado incorrectas.")
        return False


def login_cliente():
    print("\n--- LOGIN CIUDADANO (CLIENTE) ---")
    dni = input("Ingrese su DNI: ").strip()
    clave = input("Contraseña: ").strip()

    if dni == "12345678" and clave == "abcd":
        print("Acceso concedido: Ciudadano")
        return True
    else:
        print("DNI o contraseña incorrectos.")
        return False