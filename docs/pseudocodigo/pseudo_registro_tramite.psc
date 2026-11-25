Algoritmo Registrar_Tramite
	// "Cancelar" = mostrar "Operación cancelada" y terminar sin guardar nada
	Definir dni, asunto, archivo, respuesta, codigo, adjuntos Como Caracter
	Definir tipo, n_adj, ultimo, anio, i Como Entero
	Dimension adjuntos[10]
	// 1. Identificar al solicitante
	Si rol_usuario = "Ciudadano" Entonces
		dni <- dni_usuario
	SiNo
		Repetir
			Escribir "DNI del ciudadano solicitante (Enter para cancelar): "
			Leer dni
			Si dni = "" Entonces Cancelar FinSi
		Hasta Que Longitud(dni) = 8 Y EsNumero(dni) Y ExisteCiudadano(dni)
	FinSi
	// 2. Tipo de trámite (lista de 27 tipos; 0 = cancelar)
	Repetir
		Leer tipo
	Hasta Que tipo >= 0 Y tipo <= 27
	Si tipo = 0 Entonces Cancelar FinSi
	// 3. Asunto de 10 a 300 caracteres (0 = cancelar)
	Repetir
		Leer asunto
		Si asunto = "0" Entonces Cancelar FinSi
	Hasta Que Longitud(asunto) >= 10 Y Longitud(asunto) <= 300
	// 4. Adjuntos en un arreglo: de 1 a 10 archivos .pdf, .jpg o .docx sin repetir
	n_adj <- 0
	Repetir
		Leer archivo
		Si archivo = "0" Entonces
			Cancelar
		SiNo
			Si archivo <> "" Y ExtensionValida(archivo) Y No Repetido(archivo, adjuntos, n_adj) Entonces
				n_adj <- n_adj + 1
				adjuntos[n_adj] <- archivo
			FinSi
		FinSi
	Hasta Que (archivo = "" Y n_adj >= 1) O n_adj = 10
	// 5. Confirmar y guardar todo en una sola transacción
	MostrarResumen(dni, tipo, asunto, adjuntos, n_adj)
	Leer respuesta
	Si Mayusculas(respuesta) = "S" Entonces
		anio <- AnioActual()
		ultimo <- MayorCorrelativo(anio)   // SELECT MAX(...) FOR UPDATE; 0 si no hay
		codigo <- ConvertirATexto(anio) + "-" + RellenarCeros(ultimo + 1, 5)
		GuardarExpediente(codigo, dni, tipo, asunto, "Registrado")
		Para i <- 1 Hasta n_adj Hacer
			GuardarDocumento(codigo, adjuntos[i], Mayusculas(Extension(adjuntos[i])))
		FinPara
		GuardarSeguimiento(codigo, "Registrado")
		GuardarNotificacion(codigo, correo_ciudadano)
		Si HuboError() Entonces
			DeshacerTransaccion()   // rollback: no queda nada a medias
			Escribir "No se pudo completar el registro del trámite."
		SiNo
			ConfirmarTransaccion()  // commit
			Escribir "[OK] Trámite registrado. Número de expediente: ", codigo
			EnviarCopiaCorreo(correo_ciudadano, codigo, asunto)
		FinSi
	SiNo
		Cancelar
	FinSi
FinAlgoritmo
