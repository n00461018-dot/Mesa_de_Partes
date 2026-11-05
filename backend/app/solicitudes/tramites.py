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

    #Se extrae la lista de diccionarios con los tipos empezando de la posición 1
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


# Funcion para guardar los datos del tramite en la base de datos.
def reg_tramite_guardar_bd(conexion, ciudadano, id_tipo_tramite,
                          asunto, adjuntos, id_usuario, observacion):

    cursor = conexion.cursor(dictionary=True)

    try:
        # Iniciar la transaccion antes de realizar las inserciones.
        conexion.start_transaction()

        # Generar el codigo del nuevo expediente.
        codigo_tramite = reg_tramite_generar_codigo(cursor)

        # Registrar el expediente.
        cursor.execute("""
            INSERT INTO expediente (
                numero_expediente, asunto, estado,
                id_ciudadano, id_tipo_tramite, id_area
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            codigo_tramite,
            asunto,
            ESTADO_INICIAL,
            ciudadano["id_ciudadano"],
            id_tipo_tramite,
            ID_AREA_MESA_PARTES
        ))

        # Obtener el ID generado para relacionar los documentos.
        id_expediente_nuevo = cursor.lastrowid

        # Registrar los documentos adjuntos.
        for archivo in adjuntos:
            cursor.execute("""
                INSERT INTO documento (
                    nombre_archivo, tipo_documento, ruta_archivo,
                    fecha_subida, id_expediente
                ) VALUES (%s, %s, NULL, NOW(), %s)
            """, (
                archivo,
                extraer_tipo_doc(archivo),
                id_expediente_nuevo
            ))

        # Registrar el estado inicial en el seguimiento.
        cursor.execute("""
            INSERT INTO seguimiento (
                fecha, estado, observacion, id_usuario, id_expediente
            ) VALUES (NOW(), %s, %s, %s, %s)
        """, (
            ESTADO_INICIAL,
            observacion,
            id_usuario,
            id_expediente_nuevo
        ))

        # Registrar la notificacion del tramite.
        mensaje = (
            f"Su tramite {codigo_tramite} fue registrado "
            "correctamente en la Mesa de Partes."
        )

        cursor.execute("""
            INSERT INTO notificacion (
                destinatario, mensaje, tipo_notificacion,
                estado_envio, fecha_envio, id_expediente, id_usuario
            ) VALUES (%s, %s, 'Registro', 'Enviado', NOW(), %s, %s)
        """, (
            ciudadano["correo"],
            mensaje,
            id_expediente_nuevo,
            id_usuario
        ))

        # Confirmar todas las inserciones juntas.
        conexion.commit()

        return codigo_tramite

    except Exception as e:
        # Revertir todas las inserciones si ocurre algun error.
        conexion.rollback()
        print(f"Error al registrar el tramite: {e}")
        return None

    finally:
        # Cerrar el cursor al finalizar la operacion.
        cursor.close()



#Se crea la función donde se usan todas las funciones creadas para registrar el trámite
def registrar_tramite(usuario):

    #Se abre la conexión con la bd
    conexion = conectar_bd()
    if conexion is None:
        input("\nPresione Enter para regresar al menú.")
        return

    try:

        titulo_menu("Registrar trámite")

        #Registrar solicitante dandole parámetros de bd y usuario
        ciudadano = reg_tramite_solicitante(conexion, usuario)
        #Si la función devuelve None se cancela la operación
        if ciudadano is None:
            print("Operación cancelada.")
            return

        #Si se obtiene un ciudadano se muestra su nombre
        solicitante = f"{ciudadano['nombre']} {ciudadano['apellido']}"
        print(f"\nSolicitante: {solicitante}\n")

        #Registrar el tipo de trámite
        tipo = reg_tramite_tipo(conexion)

        #Si se inserta 0 la función devuelve None y se cancela la operación
        if tipo is None:
            print("Operación cancelada.")
            return
        #Se muestra el tipo de trámite seleccionado
        print(f"\nTrámite: {tipo['nombre']}")
        print(f"{tipo['descripcion']}")


        #Registrar el asunto
        asunto = reg_tramite_asunto(tipo)
        #Si se inserta 0 la función devuelve None y se cancela la operación
        if asunto is None:
            print("Operación cancelada.")
            return

        #Registrar los adjuntos
        adjuntos = reg_tramite_adjuntos(tipo)
        #Si se inserta 0 la función devuelve None y se cancela la operación
        if adjuntos is None:
            print("Operación cancelada.")
            return

        #Se muestra el resumen del trámite registrado y se pide confirmación del usuario

        titulo_menu("Registrar trámite - Resumen")
        print(" ")
        print("RESUMEN DEL TRÁMITE")
        print(" ")
        print(f"Solicitante : {solicitante}")
        print(f"Correo      : {ciudadano['correo']}")
        print(f"Tipo        : {tipo['nombre']}")
        print(f"Estado      : {ESTADO_INICIAL}")
        print(f"Asunto      : {asunto}")
        print(f"Adjuntos    : {', '.join(adjuntos)}")           #Se muestra una cadena de texto de la lista adjuntos
        print(f"Total Adjuntos. : {len(adjuntos)} documento(s)")

        confirmacion = input("\n¿Confirmar registro? (S/N): ").strip().upper()

        #Si el usuario confirma el registro se usa la función para guardar bd
        if confirmacion == "S":

            #Si el usuario que registra tiene rol ciudadano se muestra un mensaje
            if usuario["id_rol"] == ROL_CIUDADANO:
                observacion = "Trámite registrado por el ciudadano"
            else:
                #Si el usuario que registra tiene otro rol se muestra un mensaje
                observacion = "Trámite registrado por el personal de mesa de partes"

            #Se guarda el trámite en la BD
            codigo_tramite = reg_tramite_guardar_bd(
                conexion, ciudadano, tipo["id_tipo_tramite"], asunto,
                adjuntos, usuario["id_usuario"], observacion
            )

            #Se muestra el número de expediente y la notificación registrada
            print(f"\n[OK] Trámite registrado. Número de expediente: {codigo_tramite}")
            print(f"Se envió una notificación de registro a {ciudadano['correo']}.")
        else:
            #Si no se confirma con S se cancela la operación
            print("Operación cancelada.")

    finally:
        #Se cierra la conexión de bd luego de todo el proceso
        conexion.close()

    input("\nPresione Enter para regresar al menú.")
    
