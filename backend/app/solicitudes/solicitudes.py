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

    return 