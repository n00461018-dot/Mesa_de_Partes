

IF DB_ID(N'SjlBd') IS NULL
    CREATE DATABASE SjlBd COLLATE Modern_Spanish_CI_AS;
GO
USE SjlBd

 
/* ---------- PASO 2: CIUDADANO ----------
   Relaciones (la mantienen otras tablas):
     CIUDADANO 1 --- 0..1 USUARIO   (posee)
     CIUDADANO 1 --- 0..N TRAMITE   (inicia)                                   */
CREATE TABLE CIUDADANO (
    id_ciudadano      INT IDENTITY(1,1) NOT NULL,
    tipo_documento    VARCHAR(20)       NOT NULL,
    numero_documento  VARCHAR(20)       NOT NULL,
    nombres           NVARCHAR(100)     NOT NULL,
    apellidos         NVARCHAR(100)     NOT NULL,
    direccion         NVARCHAR(200)     NULL,
    CONSTRAINT PK_CIUDADANO PRIMARY KEY CLUSTERED (id_ciudadano),
    CONSTRAINT UQ_CIUDADANO_documento UNIQUE (tipo_documento, numero_documento),
    CONSTRAINT CK_CIUDADANO_tipo_documento
        CHECK (tipo_documento IN ('DNI','CE','PASAPORTE','RUC','PTP'))
);
GO
SELECT*FROM CIUDADANO

/* ---------- PASO 3: TIPO_TRAMITE ----------
   Relaciones: TIPO_TRAMITE 1 --- 0..N TRAMITE (clasifica)                    */
CREATE TABLE TIPO_TRAMITE (
    id_tipo_tramite   INT IDENTITY(1,1) NOT NULL,
    nombre            NVARCHAR(100)     NOT NULL,
    descripcion       NVARCHAR(300)     NULL,
    CONSTRAINT PK_TIPO_TRAMITE PRIMARY KEY CLUSTERED (id_tipo_tramite),
    CONSTRAINT UQ_TIPO_TRAMITE_nombre UNIQUE (nombre)
);
SELECT*FROM TIPO_TRAMITE

/* ---------- PASO 4: TIPO_DOCUMENTO ----------
   Relaciones: TIPO_DOCUMENTO 1 --- 0..N DOCUMENTO (clasifica)                */
 
 CREATE TABLE TIPO_DOCUMENTO (
    id_tipo_documento INT IDENTITY(1,1) NOT NULL,
    nombre            NVARCHAR(100)     NOT NULL,
    descripcion       NVARCHAR(300)     NULL,
    CONSTRAINT PK_TIPO_DOCUMENTO PRIMARY KEY CLUSTERED (id_tipo_documento),
    CONSTRAINT UQ_TIPO_DOCUMENTO_nombre UNIQUE (nombre)
);

/* ---------- PASO 5: AREA ----------
   Relaciones: AREA 1 --- 0..N EMPLEADO (agrupa)                              */
CREATE TABLE AREA (
    id_area           INT IDENTITY(1,1) NOT NULL,
    nombre            NVARCHAR(100)     NOT NULL,
    CONSTRAINT PK_AREA PRIMARY KEY CLUSTERED (id_area),
    CONSTRAINT UQ_AREA_nombre UNIQUE (nombre)
);

/* ---------- PASO 6: EMPLEADO ----------*/
CREATE TABLE EMPLEADO (
    id_empleado       INT IDENTITY(1,1) NOT NULL,
    id_area           INT               NOT NULL,
    nombres           NVARCHAR(150)     NOT NULL,
    cargo             NVARCHAR(100)     NOT NULL,
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_EMPLEADO_estado DEFAULT ('ACTIVO'),
    CONSTRAINT PK_EMPLEADO PRIMARY KEY CLUSTERED (id_empleado),
    CONSTRAINT FK_EMPLEADO_AREA FOREIGN KEY (id_area) REFERENCES AREA (id_area),
    CONSTRAINT CK_EMPLEADO_estado CHECK (estado IN ('ACTIVO','INACTIVO'))
);

/* ---------- PASO 7: USUARIO ----------
   FK: id_ciudadano -> CIUDADANO(id_ciudadano)
   UNIQUE en id_ciudadano => relacion 1 a 0..1 (un ciudadano, una cuenta)
   Relaciones: USUARIO 1 --- 0..N NOTIFICACION        (recibe)
               USUARIO 1 --- 0..N RECUPERACION_CUENTA (solicita)              */
CREATE TABLE USUARIO (
    id_usuario        INT IDENTITY(1,1) NOT NULL,
    id_ciudadano      INT               NOT NULL,
    correo            NVARCHAR(150)     NOT NULL,
    contrasena_hash   VARCHAR(255)      NOT NULL,
    correo_verificado BIT               NOT NULL
        CONSTRAINT DF_USUARIO_correo_verificado DEFAULT (0),
    fecha_registro    DATETIME2(0)      NOT NULL
        CONSTRAINT DF_USUARIO_fecha_registro DEFAULT (SYSDATETIME()),
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_USUARIO_estado DEFAULT ('ACTIVO'),
    CONSTRAINT PK_USUARIO PRIMARY KEY CLUSTERED (id_usuario),
    CONSTRAINT UQ_USUARIO_ciudadano UNIQUE (id_ciudadano),
    CONSTRAINT UQ_USUARIO_correo UNIQUE (correo),
    CONSTRAINT FK_USUARIO_CIUDADANO FOREIGN KEY (id_ciudadano) REFERENCES CIUDADANO (id_ciudadano),
    CONSTRAINT CK_USUARIO_estado CHECK (estado IN ('ACTIVO','INACTIVO','BLOQUEADO'))
);

/* ---------- PASO 8: TRAMITE (tabla central) ----------
   FK: id_ciudadano   -> CIUDADANO(id_ciudadano)
       id_tipo_tramite -> TIPO_TRAMITE(id_tipo_tramite)
   Relaciones: TRAMITE 1 --- 0..1 SOLICITUD
               TRAMITE 1 --- 0..N TICKET, DOCUMENTO, INCIDENCIA, ATENCION     */
CREATE TABLE TRAMITE (
    id_tramite        INT IDENTITY(1,1) NOT NULL,
    id_ciudadano      INT               NOT NULL,
    id_tipo_tramite   INT               NOT NULL,
    fecha_inicio      DATETIME2(0)      NOT NULL
        CONSTRAINT DF_TRAMITE_fecha_inicio DEFAULT (SYSDATETIME()),
    fecha_fin         DATETIME2(0)      NULL,
    canal             VARCHAR(20)       NOT NULL
        CONSTRAINT DF_TRAMITE_canal DEFAULT ('VIRTUAL'),
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_TRAMITE_estado DEFAULT ('REGISTRADO'),
    CONSTRAINT PK_TRAMITE PRIMARY KEY CLUSTERED (id_tramite),
    CONSTRAINT FK_TRAMITE_CIUDADANO FOREIGN KEY (id_ciudadano) REFERENCES CIUDADANO (id_ciudadano),
    CONSTRAINT FK_TRAMITE_TIPO_TRAMITE FOREIGN KEY (id_tipo_tramite) REFERENCES TIPO_TRAMITE (id_tipo_tramite),
    CONSTRAINT CK_TRAMITE_canal CHECK (canal IN ('VIRTUAL','PRESENCIAL')),
    CONSTRAINT CK_TRAMITE_estado
        CHECK (estado IN ('REGISTRADO','EN_PROCESO','OBSERVADO','FINALIZADO','ANULADO')),
    CONSTRAINT CK_TRAMITE_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

 
/* BLOQUE : TABLAS QUE CUELGAN DE TRAMITE*/
 
/* ---------- PASO 9: SOLICITUD ----------
   FK: id_tramite -> TRAMITE(id_tramite)
   UNIQUE en id_tramite => relacion 1 a 0..1 (formaliza)
   Relaciones: SOLICITUD 1 --- 0..N RESPUESTA, NOTIFICACION                   */
CREATE TABLE SOLICITUD (
    id_solicitud           INT IDENTITY(1,1) NOT NULL,
    id_tramite             INT               NOT NULL,
    codigo_expediente      VARCHAR(30)       NOT NULL,
    fecha_registro         DATETIME2(0)      NOT NULL
        CONSTRAINT DF_SOLICITUD_fecha_registro DEFAULT (SYSDATETIME()),
    asunto                 NVARCHAR(300)     NOT NULL,
    estado                 VARCHAR(20)       NOT NULL
        CONSTRAINT DF_SOLICITUD_estado DEFAULT ('PENDIENTE'),
    fecha_limite_respuesta DATE              NULL,
    CONSTRAINT PK_SOLICITUD PRIMARY KEY CLUSTERED (id_solicitud),
    CONSTRAINT UQ_SOLICITUD_tramite UNIQUE (id_tramite),
    CONSTRAINT UQ_SOLICITUD_expediente UNIQUE (codigo_expediente),
    CONSTRAINT FK_SOLICITUD_TRAMITE FOREIGN KEY (id_tramite) REFERENCES TRAMITE (id_tramite),
    CONSTRAINT CK_SOLICITUD_estado
        CHECK (estado IN ('PENDIENTE','EN_REVISION','RESPONDIDA','VENCIDA','ANULADA')),
    CONSTRAINT CK_SOLICITUD_fecha_limite
        CHECK (fecha_limite_respuesta IS NULL
               OR fecha_limite_respuesta >= CAST(fecha_registro AS DATE))
);

/* ---------- PASO 10: TICKET ----------
   FK: id_tramite -> TRAMITE(id_tramite)  (genera)
   Relaciones: TICKET 1 --- 0..N ATENCION (identifica)                        */
CREATE TABLE TICKET (
    id_ticket         INT IDENTITY(1,1) NOT NULL,
    id_tramite        INT               NOT NULL,
    numero_ticket     VARCHAR(30)       NOT NULL,
    fecha_emision     DATETIME2(0)      NOT NULL
        CONSTRAINT DF_TICKET_fecha_emision DEFAULT (SYSDATETIME()),
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_TICKET_estado DEFAULT ('EMITIDO'),
    CONSTRAINT PK_TICKET PRIMARY KEY CLUSTERED (id_ticket),
    CONSTRAINT UQ_TICKET_numero UNIQUE (numero_ticket),
    CONSTRAINT FK_TICKET_TRAMITE FOREIGN KEY (id_tramite) REFERENCES TRAMITE (id_tramite),
    CONSTRAINT CK_TICKET_estado CHECK (estado IN ('EMITIDO','EN_ATENCION','ATENDIDO','CANCELADO'))
);

/* ---------- PASO 11: DOCUMENTO ----------
   La ultima es una RELACION RECURSIVA (la tabla se apunta a si misma).       */
CREATE TABLE DOCUMENTO (
    id_documento          INT IDENTITY(1,1) NOT NULL,
    id_tramite            INT               NOT NULL,
    id_tipo_documento     INT               NOT NULL,
    id_documento_anterior INT               NULL,
    nombre_archivo        NVARCHAR(200)     NOT NULL,
    ubicacion_archivo     NVARCHAR(500)     NOT NULL,
    fecha_presentacion    DATETIME2(0)      NOT NULL
        CONSTRAINT DF_DOCUMENTO_fecha_presentacion DEFAULT (SYSDATETIME()),
    resultado_revision    VARCHAR(20)       NULL,
    CONSTRAINT PK_DOCUMENTO PRIMARY KEY CLUSTERED (id_documento),
    CONSTRAINT FK_DOCUMENTO_TRAMITE FOREIGN KEY (id_tramite) REFERENCES TRAMITE (id_tramite),
    CONSTRAINT FK_DOCUMENTO_TIPO_DOCUMENTO FOREIGN KEY (id_tipo_documento) REFERENCES TIPO_DOCUMENTO (id_tipo_documento),
    CONSTRAINT FK_DOCUMENTO_anterior FOREIGN KEY (id_documento_anterior) REFERENCES DOCUMENTO (id_documento),
    CONSTRAINT CK_DOCUMENTO_no_autoreferencia
        CHECK (id_documento_anterior IS NULL OR id_documento_anterior <> id_documento),
    CONSTRAINT CK_DOCUMENTO_resultado_revision
        CHECK (resultado_revision IS NULL OR resultado_revision IN ('APROBADO','OBSERVADO','RECHAZADO'))
);

/* ---------- PASO 12: INCIDENCIA ----------
   FK: id_tramite  -> TRAMITE(id_tramite)   (presenta)
       id_empleado -> EMPLEADO(id_empleado) (registra)                        */
CREATE TABLE INCIDENCIA (
    id_incidencia     INT IDENTITY(1,1) NOT NULL,
    id_tramite        INT               NOT NULL,
    id_empleado       INT               NOT NULL,
    descripcion       NVARCHAR(500)     NOT NULL,
    fecha             DATETIME2(0)      NOT NULL
        CONSTRAINT DF_INCIDENCIA_fecha DEFAULT (SYSDATETIME()),
    solucion          NVARCHAR(500)     NULL,
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_INCIDENCIA_estado DEFAULT ('ABIERTA'),
    CONSTRAINT PK_INCIDENCIA PRIMARY KEY CLUSTERED (id_incidencia),
    CONSTRAINT FK_INCIDENCIA_TRAMITE FOREIGN KEY (id_tramite) REFERENCES TRAMITE (id_tramite),
    CONSTRAINT FK_INCIDENCIA_EMPLEADO FOREIGN KEY (id_empleado) REFERENCES EMPLEADO (id_empleado),
    CONSTRAINT CK_INCIDENCIA_estado CHECK (estado IN ('ABIERTA','EN_PROCESO','RESUELTA','CERRADA'))
);

/* ---------- PASO 13: ATENCION ----------
   FK: id_tramite  -> TRAMITE(id_tramite)   (tiene)
       id_ticket   -> TICKET(id_ticket)     (identifica; OPCIONAL, admite NULL)
       id_empleado -> EMPLEADO(id_empleado) (realiza)                         */
CREATE TABLE ATENCION (
    id_atencion       INT IDENTITY(1,1) NOT NULL,
    id_tramite        INT               NOT NULL,
    id_ticket         INT               NULL,
    id_empleado       INT               NOT NULL,
    fecha_inicio      DATETIME2(0)      NOT NULL
        CONSTRAINT DF_ATENCION_fecha_inicio DEFAULT (SYSDATETIME()),
    fecha_fin         DATETIME2(0)      NULL,
    resultado         NVARCHAR(300)     NULL,
    CONSTRAINT PK_ATENCION PRIMARY KEY CLUSTERED (id_atencion),
    CONSTRAINT FK_ATENCION_TRAMITE FOREIGN KEY (id_tramite) REFERENCES TRAMITE (id_tramite),
    CONSTRAINT FK_ATENCION_TICKET FOREIGN KEY (id_ticket) REFERENCES TICKET (id_ticket),
    CONSTRAINT FK_ATENCION_EMPLEADO FOREIGN KEY (id_empleado) REFERENCES EMPLEADO (id_empleado),
    CONSTRAINT CK_ATENCION_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

/* #############################################################################
   BLOQUE D: RESPUESTA Y COMUNICACION
   ############################################################################# */
 
/* ---------- PASO 14: RESPUESTA ----------
   FK: id_solicitud -> SOLICITUD(id_solicitud) (recibe)                       */
CREATE TABLE RESPUESTA (
    id_respuesta       INT IDENTITY(1,1) NOT NULL,
    id_solicitud       INT               NOT NULL,
    fecha_respuesta    DATETIME2(0)      NOT NULL
     CONSTRAINT DF_RESPUESTA_fecha_respuesta DEFAULT (SYSDATETIME()),
    medio_notificacion VARCHAR(20)       NOT NULL,
    resultado          NVARCHAR(300)     NOT NULL,
    ubicacion_archivo  NVARCHAR(500)     NULL,
    CONSTRAINT PK_RESPUESTA PRIMARY KEY CLUSTERED (id_respuesta),
    CONSTRAINT FK_RESPUESTA_SOLICITUD FOREIGN KEY (id_solicitud) REFERENCES SOLICITUD (id_solicitud),
    CONSTRAINT CK_RESPUESTA_medio
        CHECK (medio_notificacion IN ('CORREO','FISICO','PRESENCIAL','SMS'))
);
/* ---------- PASO 15: NOTIFICACION ----------
   FK: id_usuario   -> USUARIO(id_usuario)      (recibe)
       id_solicitud -> SOLICITUD(id_solicitud)  (relaciona; OPCIONAL, admite NULL) */
CREATE TABLE NOTIFICACION (
    id_notificacion   INT IDENTITY(1,1) NOT NULL,
    id_usuario        INT               NOT NULL,
    id_solicitud      INT               NULL,
    correo_destino    NVARCHAR(150)     NOT NULL,
    tipo              VARCHAR(30)       NOT NULL,
    mensaje           NVARCHAR(1000)    NOT NULL,
    fecha_creacion    DATETIME2(0)      NOT NULL
        CONSTRAINT DF_NOTIFICACION_fecha_creacion DEFAULT (SYSDATETIME()),
    fecha_envio       DATETIME2(0)      NULL,
    estado_envio      VARCHAR(20)       NOT NULL
        CONSTRAINT DF_NOTIFICACION_estado_envio DEFAULT ('PENDIENTE'),
    CONSTRAINT PK_NOTIFICACION PRIMARY KEY CLUSTERED (id_notificacion),
    CONSTRAINT FK_NOTIFICACION_USUARIO FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario),
    CONSTRAINT FK_NOTIFICACION_SOLICITUD FOREIGN KEY (id_solicitud) REFERENCES SOLICITUD (id_solicitud),
    CONSTRAINT CK_NOTIFICACION_estado_envio CHECK (estado_envio IN ('PENDIENTE','ENVIADO','FALLIDO'))
);

/* ---------- PASO 16: RECUPERACION_CUENTA ----------
   FK: id_usuario -> USUARIO(id_usuario) (solicita)                           */
CREATE TABLE RECUPERACION_CUENTA (
    id_recuperacion   INT IDENTITY(1,1) NOT NULL,
    id_usuario        INT               NOT NULL,
    tipo_recuperacion VARCHAR(30)       NOT NULL,
    token_hash        VARCHAR(255)      NOT NULL,
    fecha_solicitud   DATETIME2(0)      NOT NULL
        CONSTRAINT DF_RECUPERACION_fecha_solicitud DEFAULT (SYSDATETIME()),
    fecha_expiracion  DATETIME2(0)      NOT NULL,
    fecha_uso         DATETIME2(0)      NULL,
    estado            VARCHAR(20)       NOT NULL
        CONSTRAINT DF_RECUPERACION_estado DEFAULT ('PENDIENTE'),
    CONSTRAINT PK_RECUPERACION_CUENTA PRIMARY KEY CLUSTERED (id_recuperacion),
    CONSTRAINT FK_RECUPERACION_USUARIO FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario),
    CONSTRAINT CK_RECUPERACION_estado CHECK (estado IN ('PENDIENTE','USADO','EXPIRADO')),
    CONSTRAINT CK_RECUPERACION_fechas CHECK (fecha_expiracion > fecha_solicitud)
);


