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
