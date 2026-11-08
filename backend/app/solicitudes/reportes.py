from solicitudes.extra import titulo_menu, ROL_ADMIN
from database.conexion_bd import conectar_bd
from database.consultas_bd import consulta_reporte_tramites



# Ordenamiento burbuja en base a un campo específico indicado
def rep_ordenar_burbuja(lista, campo, descendente):
    ordenada = lista[:]

    for i in range(len(ordenada) - 1):
        cambio = False
        for j in range(len(ordenada) - 1 - i):
            actual = ordenada[j][campo]
            siguiente = ordenada[j + 1][campo]

            #Se aplica un or para manejar ambos tipos de orden en una sola condición
            #Se evalúa (actual > siguiente) para orden ascendente
            #Se evalúa (actual < siguiente) para orden descendente
            if (actual > siguiente and not descendente) or (actual < siguiente and descendente):
                ordenada[j], ordenada[j + 1] = ordenada[j + 1], ordenada[j]
                cambio = True

        #Si no hay cambios en el recorrido, la lista ya está ordenada
        if not cambio:
            break

    return ordenada