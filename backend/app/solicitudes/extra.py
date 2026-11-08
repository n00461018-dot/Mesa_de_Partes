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

# Función para el calculo y validación del digito verificador del DNI
def digito_verificador_dni(dni, digito_ingresado):
    # Factores utilizados para la multipliacion con los números del DNI
    factores = [3, 2, 7, 6, 5, 4, 3, 2]
    # Lista de equivalencias dependiendo del índice para calcular el número verificador
    equivalencia = ["6", "7", "8", "9", "0", "1", "1", "2", "3", "4", "5"]
    # Convertimos el dígito ingresado por el usuario a string y eliminamos los espacios con strip
    digito_ingresado = str(digito_ingresado).strip()
    # Si es que el dígito ingresado no es un número y no es de un solo caracter
    if not (digito_ingresado.isdigit() and len(digito_ingresado) == 1):
        # Retorna el mensaje a continuación
        return "El código verificador debe ser 1 dígito numérico (0 - 9)."
    
    # Producto escalar entre los 8 dígitos del DNI y el arreglo de factores
    suma = 0
    # Con este bucle for hacemos que el resultado de la multiplicación de cada número del DNI con su correspondiente factor se almacene en la variable suma
    for i in range(8):
        suma += int(dni[i] * factores[i])
    # Calculamos el residuo
    residuo = suma % 11
    # Calculamos el indice para compararlo con la tabla de equivalencia 
    indice = (11 - residuo) % 11 # Se utiliza el "% 11" para evitar un error en caso que el residuo sea igual a 0
    digito_real = equivalencia[indice] # Se busca el digito real en la equivalencia utilizando el indice
    # Si es que el digito ingresado por el usuario no es igual al digito verificador real entonces le aparece el siguiente mensaje
    if digito_ingresado != digito_real:
        return "El código verificador no coincide con el DNI ingresado."
    
    return None