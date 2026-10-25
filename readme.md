# 📂 Mesa de Partes Digital – Municipalidad Distrital de San Juan de Lurigancho (SJL)

Prototipo de **Mesa de Partes Virtual** desarrollado en **Python** y conectado a una base de datos **MySQL** con 12 tablas relacionales. Este proyecto busca descentralizar y digitalizar la atención a más de 1.2 millones de vecinos de San Juan de Lurigancho, eliminando las colas, reduciendo tiempos de espera y automatizando la gestión de expedientes.

---

## 🎯 Contexto del Proyecto

En el modelo presencial de la Municipalidad de SJL, residentes de zonas alejadas (como Montenegro, Canto Grande o Zárate) enfrentan largas horas de viaje, gasto en fotocopias y retrasos de hasta 30 días en la respuesta de sus solicitudes.

Este prototipo resuelve esta problemática mediante:
* 🕒 **Atención y disponibilidad:** Registro y seguimiento de trámites en cualquier momento.
* 🔍 **Trazabilidad y seguimiento:** Generación de expediente con estado en tiempo real.
* 🌿 **Ecoeficiencia:** Política de "Cero Papel".

---

## 🚀 Características Principales

* **Control de acceso por tipo de usuario:**
  * 🔴 **Administrador (Rol 1):** Gestión de personal y áreas, creación de usuarios, derivación de expedientes entre áreas, reportes globales e historial de acciones.
  * 🟡 **Trabajador municipal (Rol 2):** Bandeja de entrada del área asignada y búsqueda/atención de trámites.
  * 🟢 **Ciudadano (Rol 3):** Registro de nuevos trámites y seguimiento de expedientes por código o estado.
* **Seguridad y Validación:**
  * Control de acceso con límite de **3 intentos de inicio de sesión**.
  * Validación previa de formato de DNI (8 dígitos) y correo electrónico.
  * Consultas SQL parametrizadas (`%s`) para evitar vulnerabilidades de **inyección SQL**.
* **Base de Datos Relacional Completa:**
  * Modelo entidad-relación estructurado con 12 tablas: `usuario`, `rol`, `area`, `ciudadano`, `expediente`, `documento`, `tipo_tramite`, `seguimiento`, `derivacion`, `incidencia`, `notificacion` y `respuesta_correo`.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Base de Datos:** MySQL (Workbench / phpMyAdmin / XAMPP)
* **Conector:** `mysql-connector-python`
* **Modelado de Procesos:** Bizagi Modeler / Diagramas de flujo

---

## ⚙️ Estructura del Código

```text
Mesa_de_Partes/
│
├── App/
│   ├── auth/
│   │   └── login.py         # Módulo de autenticación, validación de DNI/correo e intentos
│   └── solicitudes/
│       ├── extra.py         # Formato visual de títulos y limpiado de consola
│       └── menu.py          # Menú dinámico ejecutable según el rol ingresado
│
├── Database/
│   ├── Mesa_de_partes.sql   # Script ejecutable de la base de datos (12 tablas)
│   └── Modelo_entidad_relación.mwb # Diagrama de modelo de datos MySQL Workbench
│
├── docs/                    # Diagramas, pseudocódigo y bitácoras de visita de campo
└── README.md                # Documentación principal del repositorio
```

---

## 📋 Requisitos Previos

1. Tener instalado **Python 3.x**.
2. Servidor **MySQL** activo (a través de XAMPP, MySQL Workbench o similar).
3. Instalar la librería para la conexión a MySQL:
   ```bash
   pip install mysql-connector-python
   ```

---

## 📥 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/n00461018-dot/Mesa_de_Partes.git
   cd Mesa_de_Partes
   ```

2. **Configurar la base de datos:**
   * Importa el archivo `Database/Mesa_de_partes.sql` en tu gestor de MySQL.
   * Verifica la configuración de tu conexión (servidor, usuario, contraseña) en `App/auth/login.py`.

3. **Ejecutar el sistema:**
   ```bash
   python App/solicitudes/menu.py
   ```

---

## 👥 Equipo de Desarrollo (UPN - Fundamentos de Programación)

* Graciela Lizet Ruiz Ramos
* Aaron Keneth Gonzales Cortez
* Alejandro Miguel Huilcaya Dominguez
* Joan Narciso Villar
* Manuel Anthony Ruiz Perez

**Docente:** Prof. Percy Angel Pardo Zapata  
**Universidad Privada del Norte (UPN)** – 2026