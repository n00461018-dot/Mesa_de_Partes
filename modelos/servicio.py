class Servicio:
    # Clase para guardar datos de un servicio con sus atributos
 
    def __init__(self, codigo, cliente, dni, lugar, proyecto, observacion,
                 maquinaria, operador, fecha_inicio, fecha_fin,
                 horas_maquina, horas_operador, horometro_inicio, horometro_final,
                 tarifa, gasto_extra=0.0, galones_combustible=0.0,
                 horometro_combustible=0.0):

        # Datos generales que tiene el servicio
        self.codigo = codigo
        self.cliente = cliente
 
        self.dni = dni
        self.lugar = lugar
        self.proyecto = proyecto
        self.observacion = observacion
 
        # Operador y la maquinaria

        self.operador = operador
        self.maquinaria = maquinaria
        
        # Fechas
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
 
        # Horas y horometros
        self.horas_maquina = horas_maquina
        self.horas_operador = horas_operador
        self.horometro_inicio = horometro_inicio
        self.horometro_final = horometro_final
 
        # Costos
        self.tarifa = tarifa
        self.gasto_extra = gasto_extra
 
        # Combustible
        self.galones_combustible = galones_combustible
        self.horometro_combustible = horometro_combustible

        # Datos que se completan después de registrar
        self.mantenimiento = "Sin mantenimiento registrado"
        self.documentos = "Pendiente"

        # Usamos la función calcular_costo() para obtener directamente el costo
        self.costo = self.calcular_costo()

    def calcular_costo(self):

        #Calculamos el costo total aplicando (hrs de máquina * tarifa) + gastos extra y lo creamos como función para reutilizar.

        return (self.horas_maquina * self.tarifa) + self.gasto_extra



 
def buscar_por_codigo(servicios, codigo):
    
    #Función que busca en la lista general de objetos y obtiene la clase Servicio evaluando el codigo
    #Retorna el objeto de clase Servicio si lo encuentra, en caso no exista retorna None
    
    for servicio in servicios:
        if servicio.codigo == codigo:
            return servicio
    return None

 


