import os
import subprocess

# This replaces os.system completely


# NOTA: Si tu archivo backend se llama gest_solicitudes.py, cambia "solicitudes" por "gest_solicitudes"
from solicitudes import *

# Funcion reutilizable para asignar un titulo a cada menu ingresado
def titulo_menu(titulo):
    titulo_ingresado = titulo.upper()

    #Proceso para usar  comando CLS y limpiar terminal antes de ingresar al menú
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    print("==================================================")
    print(f"    MESA DE PARTES SJL - {titulo_ingresado}")
    print("==================================================\n")

# Bucle con el menu principal
def menu_principal():
    while True:

        #Se agrega la función para mostrar el título
        titulo_menu("Menu Principal")
        #Se agregan las opciones
        print("1. Registrar tramite")
        print("2. Gestionar tramite (tomar, derivar, atender, observar, rechazar)")
        print("3. Consultar tramite e historial")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opcion: ").strip()
        
        if opcion == "1":
            opcion_registrar()
        elif opcion == "2":
            opcion_gestionar()
        elif opcion == "3":
            opcion_consultar_e_historial()
        elif opcion == "0":
            titulo_menu("Salida")
            print("Se cierra sesión")
            break
        else:
            input("\nOpcion no valida. Presione Enter para reintentar.")

#Opciones de menu de acuerdo a lo seleccionado

def opcion_registrar():

    titulo_menu("1. Registrar Tramite")

    #Se extrae la posición/indice del usuario usando la funcion buscar_posicion dentro de la función pedir_usuario

    pos = pedir_usuario("Ingrese DNI o codigo de usuario: ")
    if pos is None:
        input("\nPresione Enter para continuar.")
        return

    print("Tipos de tramite disponibles:")

    #Se recorre la lista de tipos de trámite
    for i in range(len(tipos_nombres)):

        #Se muestra la lista empezando del 1
        print(f"  {i + 1}. {tipos_nombres[i]}")

        #Se usa la funcion pedir_numero para obtener un número dentro del total de elementos de la tabla tipo_nombres
    n = pedir_numero("\nElija el tipo de tramite: ", 1, len(tipos_nombres))

    #De acuerdo al número ingresado se obtiene el valor de la lista tipos_nombre quitandole 1 que fue agregado en la línea 66
    tipo = tipos_nombres[n - 1]
    datos = []
    #Se muestran los campos de acuerdo al tipo de trámite recorriendo cada valor de la lista tipos_campos
    print(f"\nCampos para '{tipo}':")
    for campo in tipos_campos[n - 1]:
        #Cada valor de la lista será pedido por consola y se agregará a la lista datos
        datos.append(input(f"  - {campo}: ").strip())

    #Se mostrará las extensiones permitidas para adjuntar al trámite    
    print(f"\nExtensiones permitidas: {', '.join(EXTENSIONES)}")
    adjunto = input("  - Nombre del adjunto (ej. documento.pdf): ").strip()

    #Se usa la funcion registrar_tramite con los datos obtenidos del usuario y se guarda en la variable resultado

    resultado = registrar_tramite(pos, tipo, datos, adjunto)

    #Se muestra un error en caso la funcion valide que se ha ingresado datos incorrectos
    if resultado.startswith("Error"):
        print(f"\n[ERROR] {resultado}")
    else:
        #Se muestra un mensaje con el código registrado del trámite
        print(f"\n[EXITO] Tramite registrado con exito. Codigo registrado: {resultado}")

    #El programa volverá al bucle while True con el menú principal
    input("\nPresione Enter para continuar.")

def opcion_gestionar():
    titulo_menu("2. Gestionar Tramite")

    #Se extrae la posición/indice del usuario responsable usando la función pedir_usuario
    pos = pedir_usuario("Ingrese su codigo de usuario (ej. MDP-001): ")
    if pos is None:
        input("\nPresione Enter para continuar.")
        return
    #Se solicita el código del trámite a gestionar y se valida si existe en la lista tramites_codigos   
    codigo = input("Codigo del tramite (ej. 2026-00001): ").strip()
    pt = buscar_posicion(tramites_codigos, codigo)
    if pt is None:
        print("\n[ERROR] El tramite no existe.")
        input("\nPresione Enter para continuar.")
        return

    print("")

    #Se muestra el detalle actual del trámite encontrado según su posición
    mostrar_detalle_tramite(pt)
    
    print("\nAcciones posibles: tomar | derivar | atender | observar | rechazar")
    #Se solicita la acción a realizar convirtiéndola a minúsculas
    accion = input("Accion a realizar: ").strip().lower()
    
    mensaje = ""
    area = ""

    #Si la acción es diferente a tomar, se pedirá un mensaje u observación obligatoria
    if accion != "tomar":
        mensaje = input("Mensaje / Observacion: ").strip()

    #Si la acción es derivar, se muestran las áreas disponibles y se solicita el área destino    
    if accion == "derivar":
        print(f"Areas disponibles: {', '.join(areas_nombres)}")
        area = input("Area destino: ").strip()

    # Recibimos el True o el texto de error del backend usando la función cambiar_estado
    resultado = cambiar_estado(codigo, accion, pos, mensaje, area)

    #Se muestra un mensaje de éxito o el error devuelto por la función
    if resultado is True:
        print("\n[EXITO] Estado actualizado correctamente.")
    else:
        print(f"\n{resultado}")
        
    input("\nPresione Enter para continuar.")

def opcion_consultar_e_historial():
    titulo_menu("3. Consultar Tramite e Historial")

    #Se solicita el código de trámite o DNI para realizar la búsqueda
    busqueda = input("Ingrese el CODIGO de tramite o DNI del solicitante: ").strip()

    #Se busca la posición si es código o las posiciones si es DNI del solicitante
    pt = buscar_posicion(tramites_codigos, busqueda)
    posiciones = [pt] if pt is not None else buscar_posiciones(tramites_documentos, busqueda)


    #Se valida si no se encontraron resultados en la búsqueda
    if len(posiciones) == 0 or posiciones[0] is None:
        print("\n[ERROR] No se encontraron tramites asociados a la busqueda.")
        input("\nPresione Enter para continuar.")
        return

    #Se recorre la lista de posiciones encontradas para mostrar el detalle de cada trámite
    for pos in posiciones:
        print("\n" + "="*50)
        mostrar_detalle_tramite(pos)
    
    input("\nPresione Enter para continuar.")

def pedir_numero(texto, minimo, maximo):
    while True:
        valor = input(texto).strip()
        #Se evalua que el número ingresado esté dentro del rango de opciones
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            #Se devuelve el valor evaluado
            return int(valor)
        print(f"Ingrese un numero entre {minimo} y {maximo}")

def pedir_usuario(texto):

    #Se solicita el código o DNI del usuario y se convierte a mayúsculas
    usuario = input(texto).strip().upper()

    #Se busca la posición del usuario dentro de la lista usuarios usando la funcion buscar_posicion
    pos = buscar_posicion(usuarios, usuario)

    #Se valida si el usuario no existe en la lista
    if pos is None:
        print("Error: El usuario no existe.")
        return None

    #Se muestran los datos del usuario logueado y se devuelve su posición
    print(f"-> Se ingresa con usuario: {nombres[pos]} | Rol: {roles[pos]} | Area: {areas_usuario[pos] or 'N/A'}\n")
    return pos

def mostrar_detalle_tramite(pt):

    #Se obtienen los datos del trámite y del solicitante usando la posición pt
    doc = tramites_documentos[pt]
    pu = buscar_posicion(documentos, doc)
    nombre_sol = nombres[pu] if pu is not None else "Desconocido"
    resp = tramites_responsables[pt] if tramites_responsables[pt] != "" else "(Sin asignar)"
    
    #Se imprime la información detallada del trámite seleccionado
    print(f"--- DETALLE DEL TRAMITE [{tramites_codigos[pt]}] ---")
    print(f"  Estado:        {tramites_estados[pt]}")
    print(f"  Area actual:   {tramites_areas[pt]}")
    print(f"  Responsable:   {resp}")
    print(f"  Solicitante:   {doc} - {nombre_sol}")
    print(f"  Tipo:          {tramites_tipos[pt]}")
    print(f"  Fecha reg.:    {tramites_fechas[pt]}")
    print(f"  Adjunto:       {tramites_adjuntos[pt]}")
    print("  Campos ingresados:")

    #Se recorre la lista de campos ingresados para mostrarlos uno por uno
    for linea in tramites_datos[pt]:
        print(f"    - {linea}")

if __name__ == "__main__":
    menu_principal()