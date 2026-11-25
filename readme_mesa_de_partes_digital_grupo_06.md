# 🏛️ Mesa de Partes Digital – Municipalidad Distrital de San Juan de Lurigancho

> **Proyecto Final – CIIN1205P: Fundamentos de Programación**  
> **Título del Desafío:** *Del archivador al algoritmo, un prototipo para la mesa de partes digital*  
> **Institución:** Universidad Privada del Norte (UPN) – Facultad de Ingeniería  

---

## 📋 Descripción del Proyecto

Prototipo funcional de **Mesa de Partes Virtual** desarrollado en **Python** con persistencia relacional en **MySQL**, diseñado para digitalizar la recepción, validación, derivación, seguimiento, atención y notificación de trámites documentarios de la **Municipalidad Distrital de San Juan de Lurigancho (SJL)**.

El sistema reemplaza el registro manual en archivadores físicos por un flujo algorítmico estructurado, alineado con la **Ley N.° 31170** (Ley de mesas de partes digitales y notificaciones electrónicas), el **Decreto Legislativo N.° 1412** (Ley de Gobierno Digital) y la **Ley N.° 29733** (Protección de Datos Personales).

---

## ✨ Funcionalidades Principales por Rol

El acceso al sistema es controlado mediante autenticación con **DNI (8 dígitos) o correo electrónico** y contraseña oculta (`getpass`), desplegando un menú dinámico según el perfil del usuario:

### 👤 Ciudadano (`id_rol = 3`)
* **Registro autónomo validado con RENIEC:** Verificación del dígito verificador del DNI (algoritmo módulo 11), existencia en padrón (`padron_reniec.txt`), fechas de emisión/caducidad y control de duplicados en base de datos.
* **Registro de trámites 24/7:** Selección entre 27 tipos de procedimientos municipales, generación automática de código correlativo anual (`AAAA-00001`) y adjunto de 1 a 10 documentos.
* **Seguimiento en tiempo real:** Consulta del estado actual e historial cronológico completo de movimientos y observaciones de cada expediente.
* **Mis trámites y Bandeja de correos:** Visualización de todos los expedientes propios y lectura directa en consola de las respuestas formales emitidas por las áreas municipales.

### 🧑‍💼 Trabajador Municipal (`id_rol = 2`)
* **Bandeja y búsqueda filtrada de área:** Consulta de expedientes asignados exclusivamente a su subgerencia (`id_area`), con filtros por código, asunto, DNI o correo del ciudadano.
* **Gestión de estados y derivación:** Control de transiciones válidas (`Derivado` $\rightarrow$ `En proceso` $\rightarrow$ `Observado` / `Atendido` / `Rechazado`) con validación temprana de permisos por área, y derivación entre las 16 oficinas municipales.
* **Registro de incidencias:** Documentación de anomalías operativas (`Documentación incompleta`, `Error de derivación`, `Error de datos`, `Problema técnico`, `Otro`) sobre expedientes en proceso.
* **Respuesta formal por correo:** Redacción y envío de comunicaciones oficiales vinculadas al expediente hacia el ciudadano.

### 🛠️ Administrador (`id_rol = 1`)
* **Gestión de personal, áreas y ciudadanos:** Alta de nuevos trabajadores, reasignación de áreas y consulta general de administrados.
* **Supervisión y reportes consolidados:** Búsqueda global de expedientes en todas las áreas, generación de reportes estadísticos agrupados por oficina/estado (ordenados mediante algoritmo burbuja optimizado) y control operativo integral.

---

## 🏗️ Estructura del Repositorio

```text
Mesa_de_Partes/
├── main.py                          # Punto de entrada principal del sistema
├── auth/
│   └── login.py                     # Validación de formato, getpass y bloqueo tras 3 intentos
├── database/
│   ├── conexion_bd.py               # Conexión centralizada a MySQL
│   ├── consultas_bd.py              # Consultas SQL reutilizables
│   ├── reniec.py                    # Validación de DNI y lectura de padrón mediante arreglos paralelos
│   ├── padron_reniec.txt            # Archivo plano con datos de padrón RENIEC
│   └── Mesa_de_partes.sql           # Script DDL/DML con las 12 tablas normalizadas
├── solicitudes/
│   ├── menu.py                      # Enrutamiento dinámico de opciones por rol
│   ├── ciudadanos.py                # Registro y consulta de ciudadanos
│   ├── tramites.py                  # Registro transaccional de expedientes y consulta "Mis trámites"
│   ├── bandeja_area.py              # Listado de expedientes asignados al área del trabajador
│   ├── buscar_tramites.py           # Búsqueda multicriterio filtrada por área
│   ├── Expedientes_areas.py         # Búsqueda global de expedientes (Administrador)
│   ├── reportes.py                  # Reportes consolidados y ordenamiento burbuja
│   ├── registrar_personal.py        # Alta de usuarios internos (Trabajador / Administrador)
│   ├── gestionar_personal.py        # Reasignación de áreas del personal
│   └── extra.py                     # Utilidades de consola, constantes de rol y validadores
├── seguimiento/
│   ├── estados.py                   # Máquina de estados finitos y transacciones de actualización
│   ├── routes.py                    # Menús de seguimiento y cambio de estado con filtro de área
│   ├── derivacion.py                # Transferencia de expedientes entre subgerencias
│   └── incidencias.py               # Registro y validación de incidencias en expedientes
├── notificaciones/
│   ├── notificacion.py              # Registro automático de notificaciones de trazabilidad
│   └── notificador_correo.py        # Registro/envío de respuestas por correo y bandeja ciudadana
└── docs/                            # Bitácora de visita, diagramas Bizagi, pseudocódigo y actas
```

---

## 🗄️ Modelo de Base de Datos (`mesa_de_partes`)

El esquema relacional está implementado en **MySQL (InnoDB, `utf8mb4`)** bajo Tercera Forma Normal (3FN) con **12 tablas interconectadas**:

| Tabla | Descripción |
| :--- | :--- |
| `rol` | Perfiles de acceso (`Administrador`, `Trabajador`, `Ciudadano`). |
| `area` | Catálogo de las 16 subgerencias y oficinas municipales. |
| `usuario` | Credenciales y datos base (`dni` y `correo` con restricción `UNIQUE`). |
| `ciudadano` | Datos complementarios de contacto (`telefono`, `direccion`). |
| `tipo_tramite` | Catálogo de 27 procedimientos administrativos municipales. |
| `expediente` | Registro principal del trámite (`numero_expediente`, `asunto`, `estado`). |
| `documento` | Archivos adjuntos asociados a cada expediente. |
| `seguimiento` | Bitácora cronológica inmutable de cambios de estado y observaciones. |
| `derivacion` | Historial de transferencias entre área origen y área destino. |
| `incidencia` | Registro de observaciones operativas durante la atención del trámite. |
| `notificacion` | Alertas automáticas generadas ante movimientos del expediente. |
| `respuesta_correo` | Comunicaciones formales emitidas por las áreas hacia el ciudadano. |

---

## 🚀 Requisitos e Instalación

### 1. Prerrequisitos
* **Python 3.10** o superior.
* **MySQL Server 8.0** o superior.
* Conector oficial de MySQL para Python:
  ```bash
  pip install mysql-connector-python
  ```

### 2. Configuración de la Base de Datos
1. Abrir MySQL Workbench o el cliente de línea de comandos de MySQL.
2. Ejecutar el script `database/Mesa_de_partes.sql` para crear el esquema `mesa_de_partes`, sus 12 tablas y los datos iniciales (roles, áreas, tipos de trámite y usuarios de prueba).
3. Verificar las credenciales de conexión (`host`, `user`, `password`, `database`) en `database/conexion_bd.py`.

### 3. Ejecución del Sistema
Desde la carpeta raíz del proyecto, ejecutar:
```bash
python main.py
```

---

## 🛡️ Seguridad e Ingeniería Aplicada

* **Control de Concurrencia (ACID):** Uso de `start_transaction()`, bloqueo pesimista `SELECT ... FOR UPDATE`, `commit()` y `rollback()` para evitar duplicidad de códigos correlativos (`2026-00001`).
* **Prevención de Inyección SQL:** Todas las consultas utilizan parámetros preparados (`%s`) y validación previa de formato en memoria.
* **Protección de Credenciales:** Lectura de contraseñas sin eco en pantalla mediante `getpass` y bloqueo automático de sesión tras 3 intentos fallidos.
* **Validación Temprana de Permisos:** Verificación inmediata de rol y área responsable (`id_area`) antes de permitir cambios de estado, derivaciones o registro de incidencias.

---

## 👥 Equipo de Desarrollo – Grupo 06

* **Graciela Lizet Ruiz Ramos**
* **Aaron Keneth Gonzales Cortez**
* **Alejandro Miguel Huilcaya Dominguez**
* **Joan Narciso Villar**
* **Manuel Anthony Ruiz Perez**

**Docente:** Prof. Percy Angel Pardo Zapata  
**Curso:** Fundamentos de Programación (`CIIN1205P`) – Universidad Privada del Norte (2026)