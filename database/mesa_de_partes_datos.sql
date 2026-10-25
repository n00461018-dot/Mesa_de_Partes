-- =====================================================================
-- DATOS DE PRUEBA - MESA DE PARTES DIGITAL 
-- Ejecutar luego del script que crea las tablas
-- El script borra todos los datos actuales de las tablas y los
-- vuelve a cargar desde cero los id
-- =====================================================================

SET NAMES utf8mb4;
USE mesa_de_partes;

-- Limpieza y vaciado de tablas para reiniciar los contadores e identidades

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE respuesta_correo;
TRUNCATE TABLE notificacion;
TRUNCATE TABLE incidencia;
TRUNCATE TABLE derivacion;
TRUNCATE TABLE seguimiento;
TRUNCATE TABLE documento;
TRUNCATE TABLE expediente;
TRUNCATE TABLE tipo_tramite;
TRUNCATE TABLE ciudadano;
TRUNCATE TABLE usuario;
TRUNCATE TABLE area;
TRUNCATE TABLE rol;
SET FOREIGN_KEY_CHECKS = 1;

-- Se insertan los roles principales para el control de acceso al sistema

INSERT INTO rol (nombre) VALUES
('Administrador'),
('Trabajador'),
('Ciudadano');

-- Se cargan las áreas y subgerencias municipales destinatarias de los trámites

INSERT INTO area (nombre, descripcion) VALUES
('Oficina General de Gestión Documental y Atención al Ciudadano', 'Mesa de partes principal: recepción, registro y derivación de documentos, y atención al ciudadano. Área del administrador del sistema.'),
('Subgerencia de Registro, Orientación y Fiscalización Tributaria', 'Registro y actualización de predios, orientación al contribuyente y fiscalización tributaria.'),
('Subgerencia de Recaudación y Control', 'Recaudación de tributos, control de pagos y de deudas, fraccionamientos.'),
('Subgerencia de Ejecución Coactiva', 'Cobranza coactiva de deudas tributarias y administrativas.'),
('Subgerencia de Limpieza Pública', 'Servicio de limpieza pública, barrido de calles y recolección de residuos sólidos.'),
('Subgerencia de Áreas Verdes', 'Mantenimiento de parques, jardines y áreas verdes del distrito.'),
('Subgerencia de Promoción y Formalización Empresarial', 'Licencias de funcionamiento y promoción de la formalización de negocios.'),
('Subgerencia de Gestión del Riesgo de Desastres', 'Prevención y respuesta ante emergencias y desastres; inspecciones técnicas de seguridad (ITSE).'),
('Subgerencia de Serenazgo', 'Seguridad ciudadana y patrullaje del distrito.'),
('Subgerencia de Fiscalización y Sanciones Administrativas', 'Fiscalización de infracciones municipales y aplicación de sanciones administrativas.'),
('Subgerencia de Movilidad Urbana y Transitabilidad', 'Tránsito, transporte y transitabilidad de las vías del distrito.'),
('Subgerencia de Planeamiento Urbano, Catastro y Obras Privadas', 'Planeamiento urbano, catastro, numeración municipal, parámetros urbanísticos y obras privadas.'),
('Subgerencia de Obras Públicas', 'Ejecución y supervisión de obras públicas municipales.'),
('Subgerencia de Mantenimiento Urbano', 'Mantenimiento de pistas, veredas y espacios públicos.'),
('Subgerencia de Servicios Sociales', 'Atención social al adulto mayor, personas con discapacidad, niñez y familia.'),
('Subgerencia de Programas Sociales', 'Programas sociales municipales como comedores populares y vaso de leche.');

-- Se implementa el registro de usuarios de prueba para trabajadores, ciudadanos y admin

INSERT INTO usuario (dni, nombre, apellido, correo, contrasena, id_rol, id_area) VALUES
('10000001', 'Daniel',   'Rojas Medina',       'admin@municipalidad.test',            '1234', 1, 1),
('10000002', 'Rosa',     'Villanueva Torres',  'rosa.villanueva@municipalidad.test',  '1234', 2, 2),
('10000003', 'Miguel',   'Paredes Soto',       'miguel.paredes@municipalidad.test',   '1234', 2, 7),
('10000004', 'Lucía',    'Cárdenas Vega',      'lucia.cardenas@municipalidad.test',   '1234', 2, 12),
('12345678', 'Graciela', 'Ruiz Ramos',         'graciela@gmail.com',                  '1234', 3, NULL),
('87654321', 'Carlos',   'Huamán Quispe',      'carlos.huaman@correo.test',           '1234', 3, NULL);

-- Se agregan los datos complementarios de domicilio y contacto de los ciudadanos

INSERT INTO ciudadano (telefono, direccion, id_usuario) VALUES
('987654321', 'Av. Los Jardines Mz. B Lt. 12, San Juan de Lurigancho', 5),
('954321876', 'Jr. Los Olivos 130, San Juan de Lurigancho', 6);

-- Se agregan los tipos de trámite y requisitos para el catálogo de la tabla tipo_tramite

INSERT INTO tipo_tramite (nombre, descripcion) VALUES
('Reimpresión de declaración jurada HR o PU',
'Requisitos: solicitud simple, copia de DNI, pago de derecho.'),

('Inscripción (alta) de predio por incorporación, compraventa u otras modalidades',
'Requisitos: formulario HR/PU, DNI, documento de propiedad, plano o croquis, pago.'),

('Descargo (baja) de predio por venta, transferencia, demolición u otras causales',
'Requisitos: solicitud de descargo, DNI, documento que sustente la baja, pago.'),

('Declaración jurada de actualización o rectificación de datos del impuesto predial',
'Requisitos: formulario HR/PU, DNI, documento que sustente el cambio, pago.'),

('Deducción de la base imponible del impuesto predial (pensionistas / adultos mayores)',
'Requisitos: solicitud, DNI, boleta de pensión, documento de propiedad, declaración jurada de predio único.'),

('Constancia de contribuyente (impuesto predial)',
'Requisitos: solicitud simple, copia de DNI, pago de derecho.'),

('Recurso de reclamación',
'Requisitos: escrito de reclamo, DNI, copia del acto reclamado, pruebas.'),

('Solicitud de prescripción en materia tributaria',
'Requisitos: solicitud indicando tributo y periodos, copia de DNI.'),

('Licencia de funcionamiento - riesgo bajo (con ITSE posterior)',
'Requisitos: formulario de licencia, RUC, DNI, declaración jurada de seguridad, pago.'),

('Licencia de funcionamiento - riesgo medio (con ITSE posterior)',
'Requisitos: formulario de licencia, RUC, DNI, declaración jurada de seguridad, pago.'),

('Licencia de funcionamiento - riesgo alto (con ITSE previa)',
'Requisitos: formulario de licencia, RUC, DNI, certificado ITSE vigente, pago.'),

('Licencia de funcionamiento - riesgo muy alto (con ITSE previa)',
'Requisitos: formulario de licencia, RUC, DNI, certificado ITSE vigente, pago.'),

('Autorización de elemento de publicidad exterior en bienes de dominio privado',
'Requisitos: formulario, DNI o RUC, diseño y medidas, permiso del propietario, pago.'),

('Separación convencional',
'Requisitos: solicitud conjunta, DNI de ambos, partida de matrimonio, declaración jurada.'),

('Divorcio ulterior',
'Requisitos: solicitud conjunta, DNI de ambos, resolución de separación, partida de matrimonio.'),

('Reconocimiento y registro de organizaciones sociales del distrito',
'Requisitos: solicitud, acta de constitución y estatuto, nómina de miembros, DNI del presidente.'),

('Licencia provisional de funcionamiento para bodegas',
'Requisitos: formulario, DNI, RUC, declaración jurada de seguridad, croquis, pago.'),

('Transferencia de licencia de funcionamiento o cambio de denominación o nombre comercial',
'Requisitos: solicitud, DNI o RUC del titular, licencia vigente, documento de transferencia.'),

('Cese de actividades',
'Requisitos: solicitud de cese, copia de DNI, copia de la licencia.'),

('ITSE posterior al inicio de actividades - riesgo bajo',
'Requisitos: formulario ITSE, copia de licencia, declaración jurada de seguridad, croquis, pago.'),

('Renovación del certificado de ITSE - riesgo bajo',
'Requisitos: solicitud, certificado ITSE anterior, declaración jurada de seguridad, pago.'),

('Asignación de numeración municipal',
'Requisitos: solicitud, DNI, documento de propiedad o posesión, croquis, pago.'),

('Certificado de parámetros urbanísticos y edificatorios',
'Requisitos: solicitud con datos del predio, DNI, plano de ubicación, documento de propiedad, pago.'),

('Constancia de no adeudo tributario (impuesto predial y arbitrios municipales)',
'Requisitos: solicitud, copia de DNI, datos del predio, pago de derecho.'),

('Fraccionamiento de deudas tributarias',
'Requisitos: solicitud, copia de DNI, identificación de la deuda, pago de cuota inicial.'),

('Acceso a la información pública',
'Requisitos: solicitud con nombre, DNI y domicilio, descripción de la información, pago de copias.'),

('Matrimonio civil',
'Requisitos: solicitud, DNI de ambos, partidas de nacimiento, 2 testigos, certificado médico, pago.');

-- Se realiza el registro de expedientes de prueba cubriendo todos los estados del sistema

INSERT INTO expediente (numero_expediente, fecha_registro, asunto, estado, id_ciudadano, id_tipo_tramite, id_area) VALUES
('2026-00001', '2026-10-05 09:15:00', 'Solicito constancia de contribuyente del predio ubicado en Av. Los Jardines Mz. B Lt. 12', 'Atendido', 1, 6, 2),
('2026-00002', '2026-10-08 10:30:00', 'Solicito licencia de funcionamiento para una librería-papelería ubicada en Jr. Las Flores 245', 'En proceso', 1, 9, 7),
('2026-00003', '2026-10-12 11:00:00', 'Solicito asignación de numeración municipal para vivienda en Mz. C Lt. 5, AA.HH. Nueva Esperanza', 'Derivado', 1, 22, 12),
('2026-00004', '2026-10-15 08:45:00', 'Solicito información sobre el presupuesto asignado al servicio de limpieza pública en 2026', 'Registrado', 1, 26, 1),
('2026-00005', '2026-10-19 16:20:00', 'Reclamo por el cobro de arbitrios del 2025 del predio ubicado en Av. Los Jardines Mz. B Lt. 12', 'Observado', 1, 7, 2),
('2026-00006', '2026-10-20 12:10:00', 'Solicito inscripción de predio adquirido por compraventa ubicado en Jr. Las Magnolias 210, Comas', 'Rechazado', 2, 2, 2);

-- Se insertan los documentos adjuntos de prueba vinculados a los expedientes

INSERT INTO documento (nombre_archivo, tipo_documento, ruta_archivo, fecha_subida, id_expediente) VALUES
('dni_graciela_ruiz.pdf',            'PDF',  NULL, '2026-10-05 09:15:00', 1),
('recibo_pago_derecho_tramite.jpg',  'JPG',  NULL, '2026-10-05 09:15:00', 1),
('dni_graciela_ruiz.pdf',            'PDF',  NULL, '2026-10-08 10:30:00', 2),
('ruc_libreria.pdf',                 'PDF',  NULL, '2026-10-08 10:30:00', 2),
('declaracion_jurada_seguridad.pdf', 'PDF',  NULL, '2026-10-08 10:30:00', 2),
('documento_propiedad.pdf',          'PDF',  NULL, '2026-10-12 11:00:00', 3),
('croquis_ubicacion.pdf',            'PDF',  NULL, '2026-10-12 11:00:00', 3),
('solicitud_acceso_informacion.pdf', 'PDF',  NULL, '2026-10-15 08:45:00', 4),
('dni_graciela_ruiz.pdf',            'PDF',  NULL, '2026-10-19 16:20:00', 5),
('escrito_reclamacion.docx',         'DOCX', NULL, '2026-10-19 16:20:00', 5),
('dni_carlos_huaman.pdf',            'PDF',  NULL, '2026-10-20 12:10:00', 6),
('minuta_compraventa.pdf',           'PDF',  NULL, '2026-10-20 12:10:00', 6),
('plano_ubicacion.pdf',              'PDF',  NULL, '2026-10-20 12:10:00', 6);

-- Se registra el historial de seguimiento y trazabilidad de los trámites

INSERT INTO seguimiento (fecha, estado, observacion, id_usuario, id_expediente) VALUES
('2026-10-05 09:15:00', 'Registrado', 'Trámite registrado por el ciudadano', 5, 1),
('2026-10-05 11:40:00', 'Derivado',   'Derivado a la Subgerencia de Registro, Orientación y Fiscalización Tributaria', 1, 1),
('2026-10-06 09:00:00', 'En proceso', 'El área revisa el estado de cuenta del contribuyente', 2, 1),
('2026-10-07 15:30:00', 'Atendido',   'Constancia emitida y notificada al ciudadano', 2, 1),
('2026-10-08 10:30:00', 'Registrado', 'Trámite registrado por el ciudadano', 5, 2),
('2026-10-08 14:00:00', 'Derivado',   'Derivado a la Subgerencia de Promoción y Formalización Empresarial', 1, 2),
('2026-10-09 09:30:00', 'En proceso', 'Se verifica la documentación y las condiciones de seguridad', 3, 2),
('2026-10-12 11:00:00', 'Registrado', 'Trámite registrado por el ciudadano', 5, 3),
('2026-10-12 15:20:00', 'Derivado',   'Derivado a la Subgerencia de Planeamiento Urbano, Catastro y Obras Privadas', 1, 3),
('2026-10-15 08:45:00', 'Registrado', 'Trámite registrado por el ciudadano', 5, 4),
('2026-10-19 16:20:00', 'Registrado', 'Trámite registrado por el ciudadano', 5, 5),
('2026-10-20 09:10:00', 'Derivado',   'Derivado a la Subgerencia de Registro, Orientación y Fiscalización Tributaria', 1, 5),
('2026-10-21 10:00:00', 'En proceso', 'El área revisa el reclamo presentado', 2, 5),
('2026-10-22 12:00:00', 'Observado',  'Falta adjuntar copia de la resolución o acto que se reclama', 2, 5),
('2026-10-20 12:10:00', 'Registrado', 'Trámite registrado por el ciudadano', 6, 6),
('2026-10-20 15:00:00', 'Derivado',   'Derivado a la Subgerencia de Planeamiento Urbano, Catastro y Obras Privadas', 1, 6),
('2026-10-21 09:00:00', 'Derivado',   'Re-derivado a la Subgerencia de Registro, Orientación y Fiscalización Tributaria por error de derivación', 4, 6),
('2026-10-22 10:15:00', 'En proceso', 'El área revisa la solicitud de inscripción de predio', 2, 6),
('2026-10-23 16:40:00', 'Rechazado',  'El predio se ubica fuera de la jurisdicción del distrito', 2, 6);

-- Se implementa el historial de derivaciones internas entre áreas

INSERT INTO derivacion (fecha_derivacion, motivo, observaciones, id_expediente, id_area_origen, id_area_destino, id_usuario) VALUES
('2026-10-05 11:40:00', 'Trámite de naturaleza tributaria (impuesto predial)',   'Derivado desde la mesa de partes para su atención', 1, 1, 2, 1),
('2026-10-08 14:00:00', 'Solicitud de licencia de funcionamiento',               'Derivado desde la mesa de partes para su evaluación', 2, 1, 7, 1),
('2026-10-12 15:20:00', 'Trámite de numeración municipal',                       'Derivado desde la mesa de partes para su atención', 3, 1, 12, 1),
('2026-10-20 09:10:00', 'Reclamo sobre arbitrios municipales',                   'Derivado desde la mesa de partes para su atención', 5, 1, 2, 1),
('2026-10-20 15:00:00', 'Inscripción de predio',                                 'Derivación inicial desde la mesa de partes', 6, 1, 12, 1),
('2026-10-21 09:00:00', 'Error de derivación',                                   'El trámite corresponde a la Subgerencia de Registro, Orientación y Fiscalización Tributaria (alta de predio)', 6, 12, 2, 4);

-- Se agregan las incidencias de prueba para seguimiento operativo

INSERT INTO incidencia (tipo_incidencia, descripcion, estado, fecha_registro, fecha_resolucion, id_expediente, id_usuario) VALUES
('Error de derivación', 'El expediente 2026-00006 fue derivado por error a Planeamiento Urbano; corresponde al área tributaria.', 'Resuelta', '2026-10-21 09:00:00', '2026-10-21 09:05:00', 6, 4),
('Documentación incompleta', 'El expediente 2026-00005 no adjunta la copia de la resolución o acto que se reclama.', 'Abierta', '2026-10-22 12:00:00', NULL, 5, 2);

-- Se inserta el historial de notificaciones enviadas a los administrados

INSERT INTO notificacion (destinatario, mensaje, tipo_notificacion, estado_envio, fecha_envio, id_expediente, id_usuario) VALUES
('graciela@gmail.com',        'Su trámite 2026-00001 fue registrado correctamente.',                                        'Registro',          'Enviado', '2026-10-05 09:16:00', 1, 5),
('graciela@gmail.com',        'Su trámite 2026-00001 fue atendido. Revise el correo con la constancia.',                   'Cambio de estado',  'Enviado', '2026-10-07 15:35:00', 1, 2),
('graciela@gmail.com',        'Su trámite 2026-00002 fue registrado correctamente.',                                        'Registro',          'Enviado', '2026-10-08 10:31:00', 2, 5),
('graciela@gmail.com',        'Su trámite 2026-00003 fue derivado a la Subgerencia de Planeamiento Urbano, Catastro y Obras Privadas.', 'Derivación', 'Enviado', '2026-10-12 15:21:00', 3, 1),
('graciela@gmail.com',        'Su trámite 2026-00005 tiene una observación. Revise el correo para subsanarla.',            'Cambio de estado',  'Enviado', '2026-10-22 12:05:00', 5, 2),
('carlos.huaman@correo.test', 'Su trámite 2026-00006 fue rechazado. Revise el correo con el detalle.',                      'Cambio de estado',  'Enviado', '2026-10-23 16:45:00', 6, 2);

-- Se agregan las respuestas formales por correo electrónico enviadas por las subgerencias

INSERT INTO respuesta_correo (correo_destino, asunto, contenido, fecha_envio, estado_envio, id_expediente, id_usuario) VALUES
('graciela@gmail.com',
'Constancia de contribuyente - Expediente 2026-00001',
'Estimada Graciela Ruiz Ramos: su trámite 2026-00001 (Constancia de contribuyente) fue atendido. Puede recoger la constancia en la mesa de partes presentando su DNI. Atentamente, Subgerencia de Registro, Orientación y Fiscalización Tributaria.',
'2026-10-07 15:40:00', 'Enviado', 1, 2),
('graciela@gmail.com',
'Observación en su trámite 2026-00005',
'Estimada Graciela Ruiz Ramos: su recurso de reclamación fue observado porque falta adjuntar la copia de la resolución o acto que se reclama. Registre un nuevo trámite con la documentación completa. Atentamente, Subgerencia de Registro, Orientación y Fiscalización Tributaria.',
'2026-10-22 12:10:00', 'Enviado', 5, 2),
('carlos.huaman@correo.test',
'Rechazo de su trámite 2026-00006',
'Estimado Carlos Huamán Quispe: su solicitud de inscripción de predio fue rechazada porque el predio se ubica fuera de la jurisdicción del distrito. Debe presentar el trámite en la municipalidad correspondiente. Atentamente, Subgerencia de Registro, Orientación y Fiscalización Tributaria.',
'2026-10-23 16:50:00', 'Enviado', 6, 2);

-- Consulta de verificación para validar el número de filas cargadas por tabla

SELECT 'rol' AS tabla, COUNT(*) AS filas FROM rol
UNION ALL SELECT 'area', COUNT(*) FROM area
UNION ALL SELECT 'usuario', COUNT(*) FROM usuario
UNION ALL SELECT 'ciudadano', COUNT(*) FROM ciudadano
UNION ALL SELECT 'tipo_tramite', COUNT(*) FROM tipo_tramite
UNION ALL SELECT 'expediente', COUNT(*) FROM expediente
UNION ALL SELECT 'documento', COUNT(*) FROM documento
UNION ALL SELECT 'seguimiento', COUNT(*) FROM seguimiento
UNION ALL SELECT 'derivacion', COUNT(*) FROM derivacion
UNION ALL SELECT 'incidencia', COUNT(*) FROM incidencia
UNION ALL SELECT 'notificacion', COUNT(*) FROM notificacion
UNION ALL SELECT 'respuesta_correo', COUNT(*) FROM respuesta_correo;