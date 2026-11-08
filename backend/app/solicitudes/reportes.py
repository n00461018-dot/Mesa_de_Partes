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


#Funcion para devolver una lista nueva solo con los registros cuyo campo coincide con el valor
def rep_filtrar(lista, campo, valor):
    filtrados = []
    for registro in lista:
        if campo is None or registro[campo] == valor:
            filtrados.append(registro)
    return filtrados


#Funcion para mostrar los valores distintos de un campo y devuelve el escogido
def rep_elegir_valor(lista, campo):
    # Se inicializa una lista vacía para almacenar los valores únicos sin repetir
    valores = []
    
    #Se recorren todos los registros de la lista inicial y se agregan a valores sin repetirse
    for registro in lista:
        if registro[campo] not in valores:
            valores.append(registro[campo])

    #Se muestra un título según si el filtro es por área o por estado
    if campo == "area":
        titulo_menu("Filtrar por área")
    else:
        titulo_menu("Filtrar por estado")
        
    #Se listan las opciones para que el usuario pueda elegir (formato i+1 empieza en 1) o 0 para cancelar
    for i in range(len(valores)):
        print(f" {i + 1}. {valores[i]}")
    print(" 0. Cancelar")

    #Se captura y limpia la entrada ingresada por el usuario
    eleccion = input("\nSeleccione una opción: ").strip()
    
    # Se valida si la entrada es un dígito válido dentro del rango de opciones
    if eleccion.isdigit() and 1 <= int(eleccion) <= len(valores):
        return valores[int(eleccion) - 1]
        
    #Luego de validar si la elección está en la lista
    #Se muestra un mensaje si la eleccion no es 0 (caracter diferente) 
    if eleccion != "0":
        input("\nOpción no válida. Presione Enter para continuar.")
    return None