import os
from datetime import datetime

RUTA_PADRON_RENIEC = "database/padron_reniec.txt"

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
        suma += int(dni[i]) * factores[i]
    # Calculamos el residuo
    residuo = suma % 11
    # Calculamos el indice para compararlo con la tabla de equivalencia 
    indice = (11 - residuo) % 11 # Se utiliza el "% 11" para evitar un error en caso que el residuo sea igual a 0
    digito_real = equivalencia[indice] # Se busca el digito real en la equivalencia utilizando el indice
    # Si es que el digito ingresado por el usuario no es igual al digito verificador real entonces le aparece el siguiente mensaje
    if digito_ingresado != digito_real:
        return "El código verificador no coincide con el DNI ingresado."
    
    return None

def validar_padron_reniec(dni, emision_texto, caducidad_texto):
    # Validamos que las fechas ingresadas tengan formato DD/MM/AAAA
    try:
        datetime.strptime(emision_texto.strip(), "%d/%m/%Y")
        fecha_caducidad = datetime.strptime(caducidad_texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        return "Formato de fecha inválido. Use el formato DD/MM/AAAA."
    
    # Leer el archivo de padrón RENIEC y cargar en arreglos paralelos (DNI, fecha de emisión, fecha de caducidad)
    if not os.path.exists(RUTA_PADRON_RENIEC):
        return "El archivo de padrón RENIEC no existe."
    
    dnis = []
    emisiones = []
    caducidades = []
    
    with open(RUTA_PADRON_RENIEC, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia != "":
                partes = linea_limpia.split(";")
                dnis.append(partes[0])
                emisiones.append(partes[1])
                caducidades.append(partes[2])
                
    # Buscamos el DNI en el arreglo de DNIs y obtenemos el índice correspondiente            
    indice_encontrador = -1
    for i in range(len(dnis)):
        if dnis[i] == dni:
            indice_encontrador = i
            break
    # Si no se encuentra el DNI en el padrón, retornamos un mensaje indicando que no se encuentra
    if indice_encontrador == -1:
        return f"El DNI {dni} no se encuentra en el padrón RENIEC."
    
    # Comparamos las fechas de emisión y caducidad con las del padrón RENIEC
    if (
        emisiones[indice_encontrador].strip() != emision_texto.strip() or
        caducidades[indice_encontrador].strip() != caducidad_texto.strip()
    ):
        return f"La fecha de emisión o caducidad no coincide con el padrón RENIEC para el DNI {dni}."
    
    if fecha_caducidad < datetime.now().date():
        return f"El DNI {dni} ha caducado según el padrón RENIEC."
    
    return None