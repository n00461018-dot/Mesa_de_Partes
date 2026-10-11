"""

Se genera el módulo de solicitudes

"""


#Lista de estados de las solicitudes o trámites y sus tipos de archivos adjuntos válidos

ESTADOS = ["Registrado", "Derivado", "En proceso", "Atendido", "Observado", "Rechazado"]
EXTENSIONES = [".pdf", ".jpg", ".png", ".docx"]

#Listas de los campos de una solicitud o trámite

#Lista codigo del trámite
tramites_codigos = []

#Lista del nro. documento del usuario
tramites_documentos = []

#Lista tipo de trámite
tramites_tipos = []

#Lista de datos ingresados al trámite
tramites_datos = []

#Lista de los archivos adjuntos en el trámite
tramites_adjuntos = []

#Lista de Estado del trámite
tramites_estados = []

#Lista del area asignada para el trámite
tramites_areas = []

#Lista del personal responsable del trámite
tramites_responsables = []

#Lista de la fecha de registro del trámite
tramites_fechas = []

# Tipos de trámites y campos mínimos de cada uno
tipos_nombres = ["Trámite 1", "Trámite 2", "Trámite 3", "Trámite 4"]

tipos_campos = [
    ["Codigo ", "Consulta"],  #Campos para trámite 1
    ["Area", "Descripcion"],     #Campos para Trámite 2
    ["Datos adicionales"],      #Campos para Trámite 3
    ["Detalle del trámite 4"]  #Campos para Trámite 4
]

#-----------------------------------------------------TEST----------------------------------------

#Se crean usuarios con roles diferentes

usuarios = ["MDP-001", "MDP-002", "12345678"]
documentos = ["70000001", "70000002", "12345678"]
roles = ["administrador", "trabajador", "ciudadano"]
areas_usuario = ["Mesa de partes", "Finanzas", ""]
nombres = ["Ana Rojas", "Luis Perez", "Carlos Mamani"]

#-----------------------------------------------------TEST----------------------------------------

#Lista de áreas

areas_nombres = ["Mesa de partes", "Finanzas", "Proyectos"]


TRANSICIONES = [
    
    #Lista de estados permitidos en las derivaciones + rol roquerido
    
    #("Estado Actual", "Acción Ejecutada", "Rol Requerido", "Nuevo Estado")
    ("Registrado", "derivar", "administrador", "Derivado"),
    ("Registrado", "observar", "administrador", "Observado"),
    ("Registrado", "rechazar", "administrador", "Rechazado"),
    ("Derivado", "tomar", "trabajador", "En proceso"),
    ("Derivado", "derivar", "trabajador", "Derivado"),
    ("En proceso", "derivar", "trabajador", "Derivado"),
    ("En proceso", "atender", "trabajador", "Atendido"),
    ("En proceso", "observar", "trabajador", "Observado"),
    ("En proceso", "rechazar", "trabajador", "Rechazado")
]


#Funciones Extras
def fecha_actual():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Funcion para buscar posicion de un dato único en una lista
def buscar_posicion(lista, valor):
    
    #Se recorre la lista
    for i in range(len(lista)):
        
        #Se compara si tiene el valor buscado
        if lista[i] == valor:
            
            #La funcion devuelve la posición del valor encontrado
            return i
    #Si luego de recorrer la lista no lo encontró se devuelve None
    return None

#Función para buscar las posiciones en una lista de un dato que se puede repetir
def buscar_posiciones(lista, valor):
    res = []
    for i in range(len(lista)):
        
        #Si encuentra el valor buscaod
        if lista[i] == valor:
            #Se agrega el índice a una lista
            res.append(i)
            
    #Se devuelve la lista de índices encontrados
    return res


#Función para validar si el documento adjunto en un trámite es el correcto
def extension_valida(nombre):
    
    #Se recorre la lista de extensiones válidas
    for ext in EXTENSIONES:
        #Si el nombre del archivo termina en la extensión
        if nombre.lower().endswith(ext):
            
            #La función devuelve True
            return True
    #Si no entra a la condicional devuelve False        
    return False



#Función para registrar la solicitud

def registrar_tramite(pos_usuario, tipo, datos, adjunto):

    #Validaciones previas a registrar el trámite

    #Validar en caso el rol del usuario sea diferente a ciudadano no permitirá registrar
    if roles[pos_usuario] != "ciudadano":
        return "Error: Solo los ciudadanos pueden registrar trámites."
    
    #Validar si el tipo de trámite está en la lista tipos_nombre
    #Usamos la funcion buscar_posicion para obtener el indice encontrado
    indice_tipotramite = buscar_posicion(tipos_nombres, tipo)
    if indice_tipotramite is None:
        return "Error: Tipo de trámite no válido."
        
    #Se crea variable con los campos obligatorios del trámite de acuerdo a su índice
    campos = tipos_campos[indice_tipotramite]
    
    #Si existe una diferencia en la cantidad de datos y los campos requeridos se mostrará el mensaje de error
    if len(datos) != len(campos):
        return "Error: Cantidad de datos incorrecta."
    
    #Validar si algún dato ingresado está vacío y mostrar error de acuerdo al valor del índice
    for i in range(len(datos)):
        if datos[i].strip() == "":
            return "Error: El campo '" + campos[i] + "' no puede estar vacío."
    
    #Validar si la extensión adjuntada no está permitida y mostrar un error.
    if not extension_valida(adjunto):
        return "Error: Extensión del adjunto no permitida."


    #Se creará código de trámite con un formato 2026-xxxxxx
    #Extraer el año actual
    año = fecha_actual()[:4]
    
    #Extraer el número de trámite nuevo (sumandole 1 al total de códigos existente)
    numero = len(tramites_codigos) + 1
    
    #Se crea codigo con formato 2026-xxxxxx
    codigo = año + "-" + str(numero).zfill(6)
    
    #Se crea una lista temporal con una lista de los datos completados por el usuario
    #De acuerdo a la cantidad de campos del trámite
    lineas = []
    for i in range(len(campos)):
        #Se agrega cada dato ingresado a la lista lineas
        lineas.append(campos[i] + ": " + datos[i])
    

    #Añadir los valores a las tablas paralelas
    
    tramites_codigos.append(codigo) #codigo
    tramites_documentos.append(documentos[pos_usuario]) #dni
    tramites_tipos.append(tipo) #tipo tramite
    tramites_datos.append(lineas) #datos de tramite (tramites_datos es una lista de listas)
    tramites_adjuntos.append(adjunto) #documentoa djunto
    tramites_estados.append("Registrado") #estado de trámite inicial
    tramites_areas.append("Mesa de partes") #área de trámite inicial
    tramites_responsables.append("") #trabajador responsable pendiente
    tramites_fechas.append(fecha_actual()) #fecha del trámite


    return codigo


#Función para cambiar estado de la solicitud (solicita codigo tramite, accion, posicion, mensaje y area_destino)
def cambiar_estado(codigo, accion, pos_usuario, mensaje="", area_destino=""):

    #--------------------------------------Validacion de errores-------------------------------------------------------

    #Se usa la función buscar_posicion para validar si el tramite no existe debe mostrar error
    indice_codigo = buscar_posicion(tramites_codigos, codigo)
    if indice_codigo is None:
        return "Error: Trámite no encontrado."    

    #Se extrae el estado del trámite en la lista tramites_estados de acuerdo al indice del código
    estado_actual = tramites_estados[indice_codigo]

    #Se extrae el rol del usuario de la lista de roles general de acuerdo a su indice
    rol_usuario = roles[pos_usuario]


    #Validacion de los cambios de estado permitidos--------------------------------

    #Se crea una tupla con valor None antes de validar
    transicion = None

    #Si la accion está permitida en la lista de TRANSICIONES los valores se guardan en la tupla transicion
    #Recorremos los elementos en TRANSICIONES
    for orig, acc, rol, dest in TRANSICIONES:
        #Si los valores de orig, accion y rol coinciden
        if orig == estado_actual and acc == accion and rol == rol_usuario:
            #Se guardan los valores en la tupla
            transicion = (orig, acc, rol, dest)
            break
    #Si la tupla transicion sigue como  None se mostrará un error
    if not transicion:
        return "Error: La acción no es válida, el estado no coincide o no tiene el rol autorizado."

    # Validaciones adicionales para trabajadores---------------------------------

    #Si el rol de usuario es trabajador y tiene un área diferente al del trámite mostrará un error
    if rol_usuario == "trabajador":
        if areas_usuario[pos_usuario] != tramites_areas[indice_codigo]:
            return "Error: El trámite no pertenece a su área asignada."

        #Si el trámite tiene un responsable diferente al asignado mostrará un error
        if estado_actual == "En proceso" and tramites_responsables[indice_codigo] != usuarios[pos_usuario]:
            return "Error: Solo el responsable actual puede gestionar este trámite."

    #Validacion para el contenido de la accion--------------------------------

    #Si la accion es una diferente a tomar trámite y el mensajes está vacio se mostrará un error
    if accion != "tomar" and mensaje.strip() == "":
        return "Error: Debe ingresar un mensaje para esta acción."    

    #Si la accion es derivar y se ingresa un area destino que no está en la lista areas_nombres se mostrará un error
    if accion == "derivar":
        if buscar_posicion(areas_nombres, area_destino) is None:
            return "Error: Área de destino no válida."   
    

    #------------------------------------------Cambio de estado---------------------------------------------------------------------------

    #Se guarda el valor del nuevo estado con los valores de la transicion que se obtuvo en la validacion previa
    #El indice 3 contiene el estado nuevo
    estado_nuevo = transicion[3]
    #Se guarda este valor en la lista paralela de tramites_estados
    tramites_estados[indice_codigo] = estado_nuevo

    #Si se deriva el tramite se cambia el área destino y se deja vacio el responsable
    if accion == "derivar":
        tramites_areas[indice_codigo] = area_destino
        tramites_responsables[indice_codigo] = ""

    #Si la accion es tomar el trámite se le asigna el responsable y mantiene su área actual
    elif accion == "tomar":
        tramites_responsables[indice_codigo] = usuarios[pos_usuario]    


    #Si la función se completa correctamente devolverá un True
    return True

