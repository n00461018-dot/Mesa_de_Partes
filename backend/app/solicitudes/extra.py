import os
import subprocess

ASUNTO_MIN, ASUNTO_MAX = 10, 300
ROL_ADMIN = 1
ROL_TRABAJADOR = 2
ROL_CIUDADANO = 3
NOMBRE_ARCHIVO_MAX = 150
EXTENSIONES_PERMITIDAS = (".pdf", ".jpg", ".docx")

# Función para crear el título de cada menú
def titulo_menu(titulo):
    titulo_ingresado = titulo.upper()
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("======================================================")
    print(f"    MESA DE PARTES SJL - {titulo_ingresado}")
    print("======================================================\n")


def validar_dni(dni):

    dni= str(dni).strip()

    #La función devuelve un mensaje en caso no sea dígito o no tenga 8 cifras
    #Se usa el método is digit que evalua el str
    if not (dni.isdigit() and len(dni) == 8):
        return "El DNI debe tener 8 dígitos numéricos."
    
    #Si la función devuelve None, pasa la validación
    return None


def validar_asunto(asunto):
    #Si el asunto no está entre los valores de minimo y maximo la función devolverá un mensaje
    if len(asunto) < ASUNTO_MIN:
        return f"El asunto debe tener al menos {ASUNTO_MIN} caracteres."
    if len(asunto) > ASUNTO_MAX:
        return f"El asunto no puede superar {ASUNTO_MAX} caracteres."
    #Si el asunto pasa la validación devuelve None
    return None


def validar_nombre_archivo(adjunto, registrados):

    #Si el largo del adjunto sobrepasa el maximo de bd mostrará un mensaje
    if len(adjunto) > NOMBRE_ARCHIVO_MAX:
        return f"El nombre no puede superar {NOMBRE_ARCHIVO_MAX} caracteres."


    #Si se inserta / o \ mostrará un mensaje
    if "/" in adjunto or "\\" in adjunto:
        return "Escriba solo el nombre del archivo, sin carpetas."

    
    nombre_lower = adjunto.lower()

    #Si el adjunto no termina con la extensión permitida se mostrará la lista de extensiones permitidas
    if not nombre_lower.endswith(EXTENSIONES_PERMITIDAS):
        permitidas = ", ".join(EXTENSIONES_PERMITIDAS)
        return f"Formato inválido. Use: {permitidas}."


    #Se extrae el primer elemento obtenido del rsplit con "." desde la derecha separando el primer punto encontrado
    #Ej: De "dni.pdf" extraerá solo "dni"
    archivo = adjunto.rsplit(".", 1)[0]

    #Si no existe un nombre de archivo la función devuelve un mensaje
    if not archivo.strip():
        return "El nombre del archivo no puede estar vacío."

    
    #Se recorre la lista de adjuntos registrados y se compara con el actual
    for adjunto_registrado in registrados:
        # si ya existe previamente, mostrará un mensaje
        if adjunto_registrado.lower() == adjunto.lower():
            return "Ese archivo ya fue adjuntado."


    #Si el adjunto pasa las validaciones devolverá None
    return None

def extraer_tipo_doc(archivo):
    #Se divide el string con el primer punto encontrado desde la derecha
    #La funcion devuelve la extensión del archivo solicitado
    return archivo.rsplit(".", 1)[1].upper()

#Función reutilizable para validar si una lista está vacía o es nula
def validar_lista_vacia(lista, mensaje="No se encontraron registros."):
    #Si la lista  no tiene los requisitos se mostrará un mensaje de aviso
    if not lista or len(lista) == 0:
        print("-" * 65)
        print(f"Aviso: {mensaje}")
        print("-" * 65)
        return True
    return False

#Funcion para mostrar una lista numerada de diccionarios y devuelve el elemento elegido
def seleccionar_de_lista(items, campo="nombre", titulo="OPCIONES",
                         mensaje="Seleccione una opción: ", cancelar=("0",)):
    #Si la lista llega vacía, avisa al usuario y sale sin pedir datos
    if not items:
        print("\nNo hay opciones disponibles para seleccionar.")
        return None

    print(f"{titulo}\n")
    #Recorre la lista numerando desde 1 y extrae el valor de la clave indicada en 'campo'
    for posicion, item in enumerate(items, 1):
        print(f" {posicion}. {item[campo]}")

    #Muestra un mensaje para cancelar la operación
    if "0" in cancelar:
        print(" 0. Cancelar")
    else:
        print(f"\n(Escriba '{cancelar[0]}' para cancelar)")

    #Repite la solicitud hasta que el usuario cancele o elija un número válido
    while True:
        eleccion = input(f"\n{mensaje}").strip()

        #Comprueba (sin importar mayúsculas/minúsculas) si el usuario decidió cancelar
        if eleccion.lower() in cancelar:
            return None

        #Valida que sea un número entero positivo y que esté dentro del rango de opciones mostradas
        if eleccion.isdecimal() and 1 <= int(eleccion) <= len(items):
            #Resta 1 para convertir el número de opción (base 1) al índice real de la lista (base 0)
            return items[int(eleccion) - 1]

        print(f"\nError: Opción no válida. Ingrese un número entre 1 y {len(items)}.")