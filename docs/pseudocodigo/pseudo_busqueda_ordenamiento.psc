Algoritmo Buscar_Tramites_Area
	Definir opcion Como Entero
	Definir valor Como Caracter
	Si rol_usuario <> "Trabajador" O area_usuario = Nulo Entonces
		Escribir "Acceso denegado."
	SiNo
		Repetir
			Escribir "1. Código  2. Asunto  3. DNI  4. Correo  5. Volver"
			Leer opcion
			Si opcion >= 1 Y opcion <= 4 Entonces
				Repetir
					Leer valor
				Hasta Que valor <> "" Y (opcion <> 3 O (Longitud(valor) = 8 Y EsNumero(valor)))
				// Filtro estricto por el área del trabajador; más recientes primero
				resultados <- Consultar(expedientes DONDE id_area = area_usuario
				                        Y criterio(opcion) coincide con valor
				                        ORDENADO POR fecha_registro DESCENDENTE)
				Si Longitud(resultados) = 0 Entonces
					Escribir "No se encontraron trámites en tu área."
				SiNo
					MostrarTabla(resultados)
				FinSi
			FinSi
		Hasta Que opcion = 5
	FinSi
FinAlgoritmo

SubProceso ordenada <- Ordenar_Burbuja(lista, n, campo, descendente)
	Definir i, j Como Entero
	Definir cambio Como Logico
	ordenada <- CopiarArreglo(lista, n)
	Para i <- 1 Hasta n - 1 Hacer
		cambio <- Falso
		Para j <- 1 Hasta n - i Hacer
			Si (No descendente Y ordenada[j][campo] > ordenada[j+1][campo]) O
			   (descendente Y ordenada[j][campo] < ordenada[j+1][campo]) Entonces
				Intercambiar(ordenada[j], ordenada[j+1])
				cambio <- Verdadero
			FinSi
		FinPara
		Si No cambio Entonces
			i <- n   // parada temprana: la lista ya está ordenada
		FinSi
	FinPara
FinSubProceso
