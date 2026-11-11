from solicitudes.extra import titulo_menu, ROL_ADMIN
from database.conexion_bd import conectar_bd
from database.consultas_bd import consultar_tramites

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

#Funcion para mostrar las opciones de orden para el reporte y devuelve el valor escogido
def rep_elegir_orden():
    #Se crea el menú con las opciones de ordenamiento como submenu
    titulo_menu("Cambiar orden")
    print(" 1. Fecha (más antiguo primero)")
    print(" 2. Fecha (más reciente primero)")
    print(" 3. Área (A-Z)")
    print(" 0. Cancelar")

    #Se pide la selección
    eleccion = input("\nSeleccione una opción: ").strip()
    
    #Si la opción escogida esta dentro de las permitidas la función la retorna
    if eleccion in ("1", "2", "3"):
        return eleccion
        
    #Si ingresa un valor diferente de 0 se notifica el error
    if eleccion != "0":
        input("\nOpción no válida. Presione Enter para continuar.")

    #Si se selecciona 0 pasa a None
    return None

#Función para mostrar en pantalla una tabla con la lista de trámites
def rep_mostrar_tabla(tramites):
    #Comprueba si la lista de trámites esta vacía para mostrar un mensaje y parar la función
    if len(tramites) == 0:
        print("No hay datos para mostrar en la opción seleccionada")
        return

    #Muestra la cabecera de la tabla con espacios fijos
    print(f"{'N° Exp.':<10} | {'Trámite':<26} | {'Fecha':<16} | {'Área':<26} | {'Estado':<12}")
    print("-" * 100)
    
    #Se crea un bucle para revisar cada trámite y dar formato a la fecha y ajustar textos a mostrar
    #En base a los campos de la funcióm consultar_tramites
    for t in tramites:
        fecha = t["fecha_registro"].strftime("%d/%m/%Y %H:%M")
        print(f"{t['numero_expediente']:<10} | {t['tipo_tramite'][:26]:<26} | {fecha:<16} | {t['area'][:26]:<26} | {t['estado']:<12}")
        
    #Mostrar el total de tramites listados
    print("-" * 100)
    print(f"Total de trámites: {len(tramites)}")


#Función principal del reporte que se ejecuta desde el menú del administrador
def menu_reportes(usuario):

    #Se valida que el usuario tenga el rol de administrador para permitirle el acceso
    if usuario["id_rol"] != ROL_ADMIN:
        print("No tiene permiso para ver los reportes.")
        return

    #Se establece la conexión con la base de datos
    conexion = conectar_bd()
    
    #Si la conexión falla, se notifica y se interrumpe la ejecución
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    #Se utiliza un bloque with para asegurar que la conexión se cierre sola al terminar la consulta
    with conexion:
        tramites = consultar_tramites(conexion)

    #Si no existen registros obtenidos, se muestra un mensaje informativo y se sale
    if len(tramites) == 0:
        titulo_menu("Reportes")
        print("No hay datos para mostrar.")
        return

    #Se establecen los valores iniciales: sin filtros activos y ordenados por fecha ascendente
    filtro_campo = None
    filtro_valor = None
    orden = "1"

    #Bucle principal para mantener la interactividad del módulo de reportes
    while True:
        #Se aplica el filtro actual sobre la lista base de trámites
        vista = rep_filtrar(tramites, filtro_campo, filtro_valor)
        
        #Se determina el criterio de ordenamiento según la opción seleccionada
        if orden == "1":
            texto_orden = "Fecha (más antiguo primero)"
            vista = rep_ordenar_burbuja(vista, "fecha_registro", False)
        elif orden == "2":
            texto_orden = "Fecha (más reciente primero)"
            vista = rep_ordenar_burbuja(vista, "fecha_registro", True)
        else:
            texto_orden = "Área (A-Z)"
            vista = rep_ordenar_burbuja(vista, "area", False)

        #Se dibuja el título y el resumen del estado actual de filtros y orden
        titulo_menu("Reportes de trámites")
        if filtro_campo is None:
            print("Filtro: ninguno")
        else:
            print(f"Filtro: {filtro_campo} = {filtro_valor}")
        print(f"Orden: {texto_orden}\n")
        
        #Se imprime la tabla con los datos procesados en memoria
        rep_mostrar_tabla(vista)

        #Se despliegan las opciones de control del menú
        print("\n 1. Ver todos")
        print(" 2. Filtrar por área")
        print(" 3. Filtrar por estado")
        print(" 4. Cambiar orden")
        print(" 5. Volver al menú")
        opcion = input("\nSeleccione una opción: ").strip()

        #Se evalúa la opción elegida por el usuario para modificar la vista o salir
        if opcion == "1":
            filtro_campo = None
            filtro_valor = None
        elif opcion == "2" or opcion == "3":
            campo_filtro = "area" if opcion == "2" else "estado"
            valor = rep_elegir_valor(tramites, campo_filtro)
            if valor is not None:
                filtro_campo = campo_filtro
                filtro_valor = valor
        elif opcion == "4":
            nuevo_orden = rep_elegir_orden()
            if nuevo_orden is not None:
                orden = nuevo_orden
        elif opcion == "5":
            return
        else:
            input("\nOpción no válida. Presione Enter para reintentar.")

