Algoritmo Login_Mesa_De_Partes
	Definir identificador, clave, nombre, apellido Como Caracter
	Definir intentos_restantes Como Entero
	Definir formato_valido, es_dni, es_correo, conexion_bd, usuario_encontrado Como Logico
	
	// Contador de intentos permitidos, solo 3 intentos hasta que el programa se cierre.
	intentos_restantes <- 3
	
	Mientras intentos_restantes > 0 Hacer
		Escribir "=== ACCESO AL SISTEMA ==="
		Escribir "Intentos disponibles: ", intentos_restantes
		Escribir "------------------------------------------------------"
		
		Escribir "Ingrese DNI o correo (o salir): "
		Leer identificador
		
		// Si el usuario escribe 'salir' se termina el programa
		Si Minusculas(identificador) = "salir" Entonces
			intentos_restantes <- 0
		SiNo
			Escribir "Contraseña: "
			Leer clave
			
			// Validamos si el usuario dejó en blanco el usuario o contraseña, si es así le da error y el formato_valido retorna Falso
			Si identificador = "" O clave = "" Entonces
				Escribir "[!] Error: No puede dejar el usuario o la contraseña en blanco."
				formato_valido <- Falso
			SiNo
				// DNI solo puede tener una longitud de 8 caracteres 
				es_dni <- (Longitud(identificador) = 8)
				es_correo <- (Longitud(identificador) >= 6)
				
				Si No es_dni Y No es_correo Entonces
					Escribir "[!] Formato inválido: Ingrese un DNI de 8 dígitos o un correo válido."
					formato_valido <- Falso
				SiNo
					formato_valido <- Verdadero
				FinSi
			FinSi
			
			// En caso que sea valido el formato retorna Verdadero
			Si formato_valido = Verdadero Entonces
				// Simulación de conexión con la base de datos
				conexion_bd <- Verdadero
				// Simulamos el error de conexión de la base de datos MySQL 
				Si conexion_bd = Falso Entonces
					Escribir "[!] Error al conectar con la base de datos MySQL."
					Escribir "No se pudo consultar la base de datos. Intente de nuevo."
				SiNo
					// Datos en duro simulando datos de la BD, si las credenciales son correctas entonces el usuario está en la BD
					Si (identificador = "12345678" O identificador = "usuario@correo.com") Y clave = "admin" Entonces
						usuario_encontrado <- Verdadero
						nombre <- "Juan"
						apellido <- "Perez"
					SiNo
						usuario_encontrado <- Falso
					FinSi
					
					// Si el usuario no se encuentra entonces se resta un intento
					Si usuario_encontrado = Falso Entonces
						intentos_restantes <- intentos_restantes - 1
						Escribir "[X] DNI/correo o contraseña incorrectos."
						// En caso que queden más intentos, le sale al usuario cuántos intentos restantes tiene
						Si intentos_restantes > 0 Entonces // En caso que ya no tenga más intentos, se le bloquea el acceso
							Escribir "Le quedan ", intentos_restantes, " intento(s)."
						SiNo
							Escribir "[!] Ha superado el límite de 3 intentos fallidos. Acceso bloqueado."
						FinSi
					SiNo // Si encuentra el usuario, entonces se le da la bienvenida
						Escribir "[OK] ¡Bienvenido(a), ", nombre, " ", apellido, "!"
						// Forzamos la salida del bucle Mientras porque ya ingresó (return usuario)
						intentos_restantes <- 0
					FinSi
				FinSi
			FinSi
		FinSi
	FinMientras
FinAlgoritmo