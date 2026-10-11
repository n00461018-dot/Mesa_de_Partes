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
    pos = pedir_usuario("Ingrese DNI o codigo de usuario: ")
    if pos is None:
        input("\nPresione Enter para continuar.")
        return

    print("Tipos de tramite disponibles:")
    for i in range(len(tipos_nombres)):
        print(f"  {i + 1}. {tipos_nombres[i]}")
    n = pedir_numero("\nElija el tipo de tramite: ", 1, len(tipos_nombres))
    
    tipo = tipos_nombres[n - 1]
    datos = []
    print(f"\nCampos para '{tipo}':")
    for campo in tipos_campos[n - 1]:
        datos.append(input(f"  - {campo}: ").strip())
        
    print(f"\nExtensiones permitidas: {', '.join(EXTENSIONES)}")
    adjunto = input("  - Nombre del adjunto (ej. documento.pdf): ").strip()

    resultado = registrar_tramite(pos, tipo, datos, adjunto)
    if str(resultado).startswith("Error"):
        print(f"\n[ERROR] {resultado}")
    else:
        print(f"\n[EXITO] Tramite registrado con exito. Codigo asignado: {resultado}")
    input("\nPresione Enter para continuar.")

def opcion_gestionar():
    titulo_menu("2. Gestionar Tramite")
    pos = pedir_usuario("Ingrese su codigo de usuario (ej. MDP-001): ")
    if pos is None:
        input("\nPresione Enter para continuar.")
        return

    codigo = input("Codigo del tramite (ej. 2026-00001): ").strip()
    pt = buscar_posicion(tramites_codigos, codigo)
    if pt is None:
        print("\n[ERROR] El tramite no existe.")
        input("\nPresione Enter para continuar.")
        return

    print("")
    mostrar_detalle_tramite(pt)
    
    print("\nAcciones posibles: tomar | derivar | atender | observar | rechazar")
    accion = input("Accion a realizar: ").strip().lower()
    
    mensaje = ""
    area = ""
    if accion != "tomar":
        mensaje = input("Mensaje / Observacion: ").strip()
    if accion == "derivar":
        print(f"Areas disponibles: {', '.join(areas_nombres)}")
        area = input("Area destino: ").strip()

    # Recibimos el True o el texto de error del backend
    resultado = cambiar_estado(codigo, accion, pos, mensaje, area)
    
    if resultado is True:
        print("\n[EXITO] Estado actualizado correctamente.")
    else:
        print(f"\n{resultado}")
        
    input("\nPresione Enter para continuar.")

def opcion_consultar_e_historial():
    titulo_menu("3. Consultar Tramite e Historial")
    busqueda = input("Ingrese el CODIGO de tramite o DNI del solicitante: ").strip()
    
    pt = buscar_posicion(tramites_codigos, busqueda)
    posiciones = [pt] if pt is not None else buscar_posiciones(tramites_documentos, busqueda)

    if len(posiciones) == 0 or posiciones[0] is None:
        print("\n[ERROR] No se encontraron tramites asociados a la busqueda.")
        input("\nPresione Enter para continuar.")
        return

    for pos in posiciones:
        print("\n" + "="*50)
        mostrar_detalle_tramite(pos)
    
    input("\nPresione Enter para continuar.")

def pedir_numero(texto, minimo, maximo):
    while True:
        valor = input(texto).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"Ingrese un numero entre {minimo} y {maximo}")

def pedir_usuario(texto):
    usuario = input(texto).strip().upper()
    pos = buscar_posicion(usuarios, usuario)
    if pos is None:
        print("Error: El usuario no existe.")
        return None
    print(f"-> Se ingresa con usuario: {nombres[pos]} | Rol: {roles[pos]} | Area: {areas_usuario[pos] or 'N/A'}\n")
    return pos

def mostrar_detalle_tramite(pt):
    doc = tramites_documentos[pt]
    pu = buscar_posicion(documentos, doc)
    nombre_sol = nombres[pu] if pu is not None else "Desconocido"
    resp = tramites_responsables[pt] if tramites_responsables[pt] != "" else "(Sin asignar)"

    print(f"--- DETALLE DEL TRAMITE [{tramites_codigos[pt]}] ---")
    print(f"  Estado:        {tramites_estados[pt]}")
    print(f"  Area actual:   {tramites_areas[pt]}")
    print(f"  Responsable:   {resp}")
    print(f"  Solicitante:   {doc} - {nombre_sol}")
    print(f"  Tipo:          {tramites_tipos[pt]}")
    print(f"  Fecha reg.:    {tramites_fechas[pt]}")
    print(f"  Adjunto:       {tramites_adjuntos[pt]}")
    print("  Campos ingresados:")
    for linea in tramites_datos[pt]:
        print(f"    - {linea}")

if __name__ == "__main__":
    menu_principal()