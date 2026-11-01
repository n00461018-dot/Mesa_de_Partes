from datetime import datetime
from mysql.connector import Error
from database.conexion_bd import *
from database.consultas_bd import *
from solicitudes.extra import *

#Declarar la constante del id de area inicial y estado inicial del trámite
ID_AREA_MESA_PARTES = 1
ESTADO_INICIAL = "Registrado"

#Declarar constantes de mínimo y máximo adjuntos en trámite
MIN_ADJUNTOS = 1
MAX_ADJUNTOS = 10

#PEDIR DATOS PARA EL TRÁMITE   ################################################################################################

#Función para obtener datos del solicitante (ciudadano) al registrar un trámite
def reg_tramite_solicitante(conexion, usuario):
    #Se coloca el título de la pantalla
    titulo_menu("Registrar trámite - Solicitante")

    #Si el solicitante tiene rol ciudadano (dni registrado) se aplicará la funcion buscar_ciudadano_por_dni
    if usuario["id_rol"] == ROL_CIUDADANO:
        # El ciudadano registra a su nombre: se busca con su propio DNI
        ciudadano = buscar_ciudadano_por_dni(conexion, usuario["dni"])
        return ciudadano

    #Usuario con otro rol va a registrar el dni del ciudadano por consola
    while True:
        #Se coloca el título de la pantalla
        titulo_menu("Registrar trámite - Solicitante")

        dni = input("Ingresar el DNI del ciudadano solicitante (Enter para cancelar): ").strip()
        
        #Si no ingresa datos la función reg_tramite_solicitante devuelve None
        if dni == "":
            return None
        
        #Se valida el dni ingresado por consola
        error = validar_dni(dni)
        if error:
            #Si la validación encuentra un error (contiene un valor) se mostrará un mensaje con el error
            print(f"\nError: {error}")
            input("\nPresione Enter para continuar...")
            #Volverá al bucle While desde el inicio
            continue

        #Si pasa las validaciones se extraen los datos del ciudadano por dni en un diccionario "ciudadano"
        ciudadano = buscar_ciudadano_por_dni(conexion, dni)

        #Si no se encuentran datos de ciudadano en la BD se mostrará un mensaje y se volverá a iniciar el bucle
        if ciudadano is None:
            print("\n Error: No existe un ciudadano registrado con ese DNI.")
            input("\nPresione Enter para continuar...")
            continue

        #Si se encuentran datos de ciudadano la función devuelve la información 
        return ciudadano


#Funcion para listar y pedir el tipo de trámite
def reg_tramite_tipo(conexion):
    #Se crea la variable con la lista de tipos de trámite
    tipos = listar_tipos_tramite(conexion)

    titulo_menu("Registrar trámite - Tipo de Trámite")
    print("TIPOS DE TRÁMITE\n")

    #Se extrae la lista de diccionarios empezando de la posición 1
    for posicion, tipo in enumerate(tipos, 1):
        #Por cada elemento se muestra la posicion (numero de la lista) y el nombre del trámite
        print(f"{posicion}. {tipo['nombre']}")

    #Al final de la lista se mostrará 0 para cancelar
    print(" 0. Cancelar")

    #Se entra en un bucle para seleccionar el trámite
    while True:
        eleccion = input("\nSeleccione el tipo de trámite: ").strip()

        #Si ingresa 0 la función devuelve None
        if eleccion == "0":
            return None
        
        #Si lo ingresado es digito y entra en el rango de opciones la función devolverá el diccionario
        if eleccion.isdigit():
            num_eleccion = int(eleccion)
            if 1 <= num_eleccion <= len(tipos):
                #Se ingresa el indice -1 (debido a que el enumerate en tipos no empieza en 0)
                return tipos[num_eleccion - 1]
            
        #Si no pasa las validaciones mostrará un mensaje como opción no válida y se vuelve al bucle
        print("Opción no válida.")


#Función para pedir el asunto del trámite
#Se pasa el parámetro tipo para mostrar el tipo seleccionado junto al asunto
def reg_tramite_asunto(tipo):
    #Se inserta el título del menú
    titulo_menu("Registrar trámite - Asunto")
    
    #Se muestra el trámite seleccionado y la descripción (Requisitos)
    print(f"Trámite seleccionado: {tipo['nombre']}")
    print(f"Descripción         : {tipo['descripcion']} \n")

    #Bucle para pedir asunto
    while True:
        #Se pide ingresar el asunto por consola
        asunto = input("\nIngrese el asunto del trámite (0 para cancelar): ").strip()

        #Si ingresa 0 se devuelve None
        if asunto == "0":
            return None

        #Se valida el asunto y se guarda el resultado en "error"
        error = validar_asunto(asunto)
        
        #Si pasa la validación la función devuelve el asunto
        if error is None:
            return asunto

        #Si hay un error se muestra en pantalla y vuelve el bucle
        print(f"Error: {error}")




#Función para pedir y validar los documentos adjuntos del trámite
def reg_tramite_adjuntos(tipo):
    #Se inserta el titulo
    titulo_menu("Registrar trámite - Documentos Adjuntos")

    #Se muestran los valores seleccionados al inicio
    print(f"Trámite seleccionado: {tipo['nombre']}")
    print(f"Descripción         : {tipo['descripcion']}")

    print("\nAdjuntos: Ingrese el nombre del archivo"
          "(Ej: dni.pdf)")
    
    #Cadena con las extensiones permitidas para ser mostrada
    ext_permitidas=', '.join(EXTENSIONES_PERMITIDAS)
    print(f"Extensiones permitidas: {ext_permitidas}. ")
    print("Presione Enter para terminar, 0 para cancelar.")
    print(" ")

    #Se crea la lista de archivos adjuntos
    lista_archivos = []

    #Se inicia un bucle mientras no se alcance el máximo de adjuntos permitidos
    while len(lista_archivos) < MAX_ADJUNTOS:

        #Se guarda el total de elementos de la lista de archivos
        total_archivos=len(lista_archivos)

        #Se solicita el nombre del archivo y se muestra el número
        nombre = input(f"Adjunto N° {total_archivos+ 1}: ")

        #Si ingresa 0 la función devuelve None
        if nombre == "0":
            return None

        #Si no ingresa el archivo
        if nombre == "":
            #Si tiene el mínimo de adjuntos se sale del bucle
            if len(lista_archivos) >= MIN_ADJUNTOS:
                break
            #Si no tiene el minimo se muestra un mensaje de error y vuelve al bucle
            print(f"Error: Debe adjuntar al menos {MIN_ADJUNTOS} documento.")
            continue

        #Se valida el contenido de lista_archivos
        error = validar_nombre_archivo(nombre, lista_archivos)
        if error:
            #Si hay un error se muestra en pantalla y vuelve al bucle
            print(f"Error: {error}")
            continue

        #Si pasa las validaciones se agrega el archivo a la lista
        lista_archivos.append(nombre)

    #Se devuelve la lista con los documentos adjuntos
    return lista_archivos





def reg_tramite_generar_codigo(cursor):
    #Se crea el prefijo del código del trámite: "2026-"
    prefijo = f"{datetime.now().year}-"

    #Se extrae el máximo número de expediente registrado con el prefijo en la tabla expediente 
    cursor.execute("""
        SELECT MAX(numero_expediente) AS ultimo_codigo_bd 
        FROM expediente 
        WHERE numero_expediente LIKE %s
        FOR UPDATE
    """, (prefijo + "%",))

    #Del diccionario cursor se extrae el valor de la clave "ultimo_codigo_bd"
    #El cual guarda el último código registrado en la bd y se pasa a la variable ultimo_codigo
    ultimo_codigo = cursor.fetchone()["ultimo_codigo_bd"]

    if ultimo_codigo is None:
        #Si no existen códigos registrados se empieza el número en uno
        numero_codigo = 1
    else:
        #Si ya hay registro se extrae el número y se suma 1
        #Se usa rsplit para dividir el prefijo del número y se convierte a entero para sumarle 1
        numero_codigo = int(ultimo_codigo.split("-")[1]) + 1

    #Se aplica fstring para juntar el prefijo con el numero obtenido
    codigo_tramite=f"{prefijo}{numero_codigo:05d}"

    #La función devuelve el código del trámite generado
    return codigo_tramite


