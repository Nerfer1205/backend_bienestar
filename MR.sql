/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 15.0 		*/
/*  Created On : 26-sept.-2023 6:27:40 p. m. 				*/
/*  DBMS       : Oracle 						*/
/* ---------------------------------------------------- */

/* Drop Triggers, Sequences for Autonumber Columns */

DECLARE 
  C NUMBER; 
BEGIN 
SELECT COUNT(*) INTO C 
FROM USER_TRIGGERS 
  WHERE TRIGGER_NAME = 'TRG_SOLICITUDES_ID_SOLICITUD'; 
  IF (C > 0) THEN 
    EXECUTE IMMEDIATE 'DROP TRIGGER "TRG_SOLICITUDES_ID_SOLICITUD"'; 
END IF; 
END;
/

DECLARE 
  C NUMBER; 
BEGIN 
SELECT COUNT(*) INTO C 
FROM USER_SEQUENCES 
  WHERE SEQUENCE_NAME = 'SEQ_SOLICITUDES_ID_SOLICITUD'; 
  IF (C > 0) THEN 
    EXECUTE IMMEDIATE 'DROP SEQUENCE "SEQ_SOLICITUDES_ID_SOLICITUD"'; 
END IF; 
END;
/


/* Drop Tables */

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "ACTIVIDADES_DE_APOYO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "CONDICIONES" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "CONVOCATORIA" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "CONVOCATORIA_TIPO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "CONVOCATORIA_TIPO_SUBSIDIO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "DOCUMENTOS" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "ESTUDIANTES" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "RESPONSABLE" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "SOLICITUDES" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "SOLICITUDES_APROBADAS" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "TICKET" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "TIPO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "TIPO_SUBSIDIO" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

begin
	EXECUTE IMMEDIATE 'DROP TABLE   "TIQUETERA" CASCADE CONSTRAINTS';
	EXCEPTION WHEN OTHERS THEN NULL;
end;
/

/* Create Tables */

CREATE TABLE  "ACTIVIDADES_DE_APOYO"
(
	"ID_ACTIVIDAD" VARCHAR2(10) NOT NULL,	-- Identificador unico sobre la actividad de apoyo
	"DESCRIPCION" VARCHAR2(255) NOT NULL,	-- Informacion acerca de la actividad como lugar y labor
	"FECHA" DATE NOT NULL,	-- Fecha en la que se realiza la actividad de apoyo
	"FK_RESPONSABLE_SUPERVISAR" VARCHAR2(10) NULL
)
;

CREATE TABLE  "CONDICIONES"
(
	"ID_CONDICION" VARCHAR2(5) NOT NULL,	-- Identificador único de cada condición en la base de datos.
	"NOMBRE" VARCHAR2(200) NOT NULL,	-- El nombre o la descripción de la condición o métrica. 
	"PUNTAJE" NUMBER(2) NOT NULL,	-- El puntaje asociado a la condición o métrica para un documento específico. Este valor representa la calificación numérica o puntaje asignado al documento en función de esta métrica.
	"FK_ID_TIPO" VARCHAR2(5) NULL
)
;

CREATE TABLE  "CONVOCATORIA"
(
	"ID_CONVOCATORIA" VARCHAR2(10) NOT NULL,	-- Identificador único de cada convocatoria en la base de datos
	"FECHA_I_CONV" DATE NOT NULL,	-- Fecha de apertura hacia los estudiantes para aplicar a la convocatoria
	"FECHA_I_INSC" DATE NOT NULL,	-- Fecha de inicio de inscripciones por parte de los estudiantes
	"FECHA_I_VERIF" DATE NOT NULL,	-- Fecha de inicio de la verificacion de los documentos asociados a una solicitud
	"FECHA_I_PUBL" DATE NOT NULL,	-- Fecha de publicacion de resultados a las solicitudes realizadas
	"FECHA_I_CUMP" DATE NOT NULL,	-- fecha de inicio del subsidio
	"FECHA_F_CUMP" DATE NOT NULL,	-- fecha de final del subsidio
	"PERIODO" VARCHAR2(10) NOT NULL,	-- Semestre para el cual se realiza la convocatoria
	"ESTADO" VARCHAR2(25) DEFAULT 'SIN_INICIAR' NOT NULL,	-- Fase en el que se puede encontrar la convocatoria con respecto a las fechas establecidas por la misma. Sus posibles valores son: CONVOCATORIA, SIN_INICIAR, INSCRIPCION, VERIFICACION_DOC ,CALCULO_P ,ASIGNACION_S ,PUBLICACION ,CUMPLIENTO ,TERMINADA
	"VALOR_X_ALMUERZO" NUMBER(8) NOT NULL	-- Precio en pesos del almuerzo
)
;

CREATE TABLE  "CONVOCATORIA_TIPO"
(
	"FK_ID_CONVOCATORIA" VARCHAR2(10) NOT NULL,	-- Identificador único de cada convocatoria en la base de datos
	"FK_ID_TIPO" VARCHAR2(5) NOT NULL	-- Identificador único de cada tipo de variable o condicion en la base de datos.
)
;

CREATE TABLE  "CONVOCATORIA_TIPO_SUBSIDIO"
(
	"FK_ID_CONVOCATORIA" VARCHAR2(10) NOT NULL,	-- Identificador único de cada convocatoria en la base de datos
	"FK_ID_TIPO_SUBSIDIO" VARCHAR2(5) NOT NULL,	-- Identificador único de cada tipo de subsidio en la base de datos.
	"CANTIDAD" NUMBER(4) NOT NULL	-- Cupos disponibles para ese tipo de subsidio y convocatoria
)
;

CREATE TABLE  "DOCUMENTOS"
(
	"ID_DOCUMENTO" NUMBER(2) NOT NULL,	-- Identificador único de cada documento en la base de datos.
	"FK_ID_SOLICITUD" NUMBER(10) NOT NULL,
	"RUTA" VARCHAR2(255) NOT NULL,	-- Un enlace o ruta que redirige a la ubicación del documento. Es una URL 
	"ESTADO" VARCHAR2(50) DEFAULT 'SIN_CALIFICAR' NOT NULL,	-- El estado actual del documento, que puede ser: SIN_CALIFICAR, APROBADO, RECHAZADO.
	"PUNTAJE_OBTENIDO" NUMBER(2) NOT NULL,
	"FK_ID_CONDICION" VARCHAR2(5) NULL
)
;

CREATE TABLE  "ESTUDIANTES"
(
	"CODIGO" VARCHAR2(11) NOT NULL,	-- numero de identificacion del estudiante asignado por la universidad
	"PROYECTO" VARCHAR2(50) NOT NULL,	-- Carrera a la que pertenece dentro de la universidad
	"SEMESTRE" VARCHAR2(2) NOT NULL,	-- Numero de semestre que esta cursando
	"TIPO_DOCUMENTO" VARCHAR2(2) NOT NULL,	-- El tipo de documento de identificación del estudiante, como cédula de ciudadanía, pasaporte, tarjeta de identidad, etc.
	"DOCUMENTO" VARCHAR2(10) NOT NULL,	-- El número de documento oficial de identificación del estudiante
	"NOMBRES" VARCHAR2(50) NOT NULL,	-- Los nombres del estudiante.
	"APELLIDOS" VARCHAR2(50) NOT NULL,	-- Los apellidos del estudiante
	"TELEFONO" VARCHAR2(10) NOT NULL,	-- El número de teléfono de contacto del estudiante.
	"DIRECCION" VARCHAR2(50) NOT NULL,	-- La dirección física o domicilio del estudiante.
	"MUNICIPIO" VARCHAR2(50) NOT NULL,	-- Nombre del municipio en el que reside el estudiante
	"COSTO_SEM" NUMBER(10) NOT NULL,	-- El costo asociado al semestre académico para el estudiante
	"INGRESOS" NUMBER(10,2) NOT NULL,	-- Esta dato almacena el valor relacionada con los ingresos económicos del estudiante y su familia. Estos datos pueden ser utilizados para determinar la elegibilidad para el apoyo alimentario
	"PROMEDIO_PONDERADO" NUMBER(3,2) NOT NULL,	-- Promedio asociado al estudiante que ha obtenido durante la carrera
	"ASIG_PERDIDAS_SEM_PASADO" NUMBER(1) NULL,	-- Numero de materias reprobadas en el ultimo semestre cursado
	"NUM_CREDITOS" NUMBER(2) NOT NULL,	-- Numero de creditos asociados a las materias cursadas por el estudiante en el semestre actual
	"ESTADO" VARCHAR2(25) NOT NULL,	-- Situacion del estudiante dentro de la universidad. Puede estar: ACTIVO o INACTIVO.
	"USUARIO" VARCHAR2(128) NULL	-- Permite saber el usuario que cierto estudiante tiene en la tabla users del SMDB
)
;

CREATE TABLE  "RESPONSABLE"
(
	"DOCUMENTO" VARCHAR2(10) NOT NULL,	-- El número de documento oficial de identificación del responsable
	"TIPO_DOCUMENTO" VARCHAR2(2) NOT NULL,	-- El tipo de documento de identificación del responsable, como cédula de ciudadanía, pasaporte, tarjeta de identidad, etc.
	"NOMBRES" VARCHAR2(50) NOT NULL,	-- Nombres del responsable
	"APELLIDOS" VARCHAR2(50) NOT NULL,	-- Apellidos del responsable
	"TELEFONO" VARCHAR2(10) NOT NULL,	-- Numero de Telefono del responsable
	"DIRECCION" VARCHAR2(50) NOT NULL,	-- Direccion fisica del hogar del responsable
	"USUARIO" VARCHAR2(128) NOT 	-- Usuario que se relaciona con el que tiene en la tabla dba_users
)
;

CREATE TABLE  "SOLICITUDES"
(
	"ID_SOLICITUD" NUMBER(10) NOT NULL,	-- Identificador único de cada solicitud de apoyo alimentario.
	"FECHA_CREACION" TIMESTAMP(9) DEFAULT CURRENT_TIMESTAMP NOT NULL,	-- La fecha y hora en que se creó la solicitud.
	"ESTADO" VARCHAR2(25) DEFAULT 'SIN_CALIFICAR' NOT NULL,	-- El estado actual de la solicitud, que puede ser: SIN_CALIFICAR, APROBADA, RECHAZADA.
	"PUNTAJE_TOTAL" NUMBER(3) NULL,	-- El puntaje total obtenido por el estudiante en su solicitud. El puntaje puede estar en el rango de 0 a 100.
	"MOTIVO_RECHAZO" VARCHAR2(50) NULL,	-- Una descripción corta del motivo por el cual se rechazó la solicitud, en caso de que la solicitud haya sido rechazada.
	"FK_CODIGO" VARCHAR2(11) NOT NULL,
	"FK_ID_CONVOCATORIA" VARCHAR2(10) NOT NULL,
	"FK_RESPONSABLE_VERIFICAR" VARCHAR2(10) NULL
)
;

CREATE TABLE  "SOLICITUDES_APROBADAS"
(
	"ID_APROBACION" VARCHAR2(5) NOT NULL,	-- Identificador único de cada solicitud en la base de datos
	"FECHA_APROBACION" DATE NOT NULL,	-- Fecha en la que se aprobo la solicitud
	"ESTADO" VARCHAR2(25) NOT NULL,	-- Descripcion de si el subsidio se encuentra activo o no para el estudiante. Sus posibles valores son: APROBADA o REVOCADA.
	"MOTIVO_FINALIZACION" VARCHAR2(50) NULL,	-- Motivo por el cual el estudiante ya no recibe mas el subsidio
	"FK_ID_SOLICITUD" NUMBER(10) NULL,
	"FK_ID_TIPO_SUBSIDIO" VARCHAR2(5) NULL,
	"FK_RESPONSABLE_APROBAR" VARCHAR2(10) NULL
)
;

CREATE TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO"
(
	"FK_ID_ACTIVIDAD" VARCHAR2(10) NOT NULL,	-- Identificador unico sobre la actividad de apoyo
	"FK_ID_APROBACION" VARCHAR2(5) NOT NULL,	-- Identificador único de cada solicitud en la base de datos
	"HRS_ASISTENCIA" NUMBER(3) NOT NULL	-- Horas realizadas en la actividad de apoyo
)
;

CREATE TABLE  "TICKET"
(
	"CODIGO" VARCHAR2(10) NOT NULL,	-- Identificador unico del ticket
	"CODIGO_TIQUETERA" VARCHAR2(50) NOT NULL,
	"FECHA" DATE NOT NULL,	-- Fecha en la que se reclama el ticket
	"RECLAMADO" VARCHAR2(25) NULL	-- Estado en el que se encuentra el ticket, puede estar reclamado o no
)
;

CREATE TABLE  "TIPO"
(
	"ID_TIPO" VARCHAR2(5) NOT NULL,	-- Identificador único de cada tipo de variable o condicion en la base de datos.
	"NOMBRE" VARCHAR2(50) NOT NULL,	-- El nombre o la descripción del tipo de variable.
	"PUNTAJE_MAX" NUMBER(2) NOT NULL	-- El puntaje máximo asignado a las variables en el proceso de convocatoria. Indica el valor máximo que una variable puede contribuir al puntaje total.
)
;

CREATE TABLE  "TIPO_SUBSIDIO"
(
	"ID_TIPO_SUBSIDIO" VARCHAR2(5) NOT NULL,	-- Identificador único de cada tipo de subsidio en la base de datos.
	"NOMBRE" VARCHAR2(25) NOT NULL,	-- El nombre o la descripción del tipo de subsidio, como "Total," "Tipo A," o "Tipo B."
	"POR_COBERTURA" NUMBER(5,2) NOT NULL,	-- El porcentaje de cobertura del subsidio. Indica cuánto del subsidio total se cubre para este tipo. Puede ser el 100% para "Total," el 70% para "Tipo A," o el 40% para "Tipo B."
	"HRS_DEDICACION_X_SEM" NUMBER(3) NOT NULL	-- La cantidad de horas de dedicación requeridas por semana como deber de ser beneficiario del subsidio
)
;

CREATE TABLE  "TIQUETERA"
(
	"CODIGO_TIQUETERA" VARCHAR2(50) NOT NULL,	-- Codigo generado mes a mes que agrupa los tickets de un mes en particular
	"FECHA_I_VIGENCIA" DATE NOT NULL,	-- Fecha desde cuando esta activa la tiquetera para reclamar el subsidio
	"FECHA_F_VIGENCIA" DATE NOT NULL,	-- Fecha de finalizacion de la tiquetera para reclamar el subsidio
	"ESTADO" VARCHAR2(20) NOT NULL,	-- Situacion en la que se encuentra la tiquetera, si esta ACTIVA o INACTIVA.
	"FK_ID_APROBACION" VARCHAR2(5) NULL
)
;

/* Create Comments, Sequences and Triggers for Autonumber Columns */

COMMENT ON TABLE  "ACTIVIDADES_DE_APOYO" IS 'Entidad que almacena informacion acerca de las actividades de apoyo que deben realizar los estudiantes beneficiarios del subsidio'
;


COMMENT ON COLUMN  "ACTIVIDADES_DE_APOYO"."ID_ACTIVIDAD" IS 'Identificador unico sobre la actividad de apoyo';

COMMENT ON COLUMN  "ACTIVIDADES_DE_APOYO"."DESCRIPCION" IS 'Informacion acerca de la actividad como lugar y labor';

COMMENT ON COLUMN  "ACTIVIDADES_DE_APOYO"."FECHA" IS 'Fecha en la que se realiza la actividad de apoyo';

COMMENT ON TABLE  "CONDICIONES" IS 'Esta tabla almacena las condiciones o métricas asociadas a un documento.'
;


COMMENT ON COLUMN  "CONDICIONES"."ID_CONDICION" IS 'Identificador único de cada condición en la base de datos.';

COMMENT ON COLUMN  "CONDICIONES"."NOMBRE" IS 'El nombre o la descripción de la condición o métrica. ';

COMMENT ON COLUMN  "CONDICIONES"."PUNTAJE" IS 'El puntaje asociado a la condición o métrica para un documento específico. Este valor representa la calificación numérica o puntaje asignado al documento en función de esta métrica.';

COMMENT ON TABLE  "CONVOCATORIA" IS 'Esta tabla almacena la información asociada a una convocatoria para el subsidio de apoyo alimentario'
;


COMMENT ON COLUMN  "CONVOCATORIA"."ID_CONVOCATORIA" IS 'Identificador único de cada convocatoria en la base de datos';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_I_CONV" IS 'Fecha de apertura hacia los estudiantes para aplicar a la convocatoria';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_I_INSC" IS 'Fecha de inicio de inscripciones por parte de los estudiantes';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_I_VERIF" IS 'Fecha de inicio de la verificacion de los documentos asociados a una solicitud';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_I_PUBL" IS 'Fecha de publicacion de resultados a las solicitudes realizadas';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_I_CUMP" IS 'fecha de inicio del subsidio';

COMMENT ON COLUMN  "CONVOCATORIA"."FECHA_F_CUMP" IS 'fecha de final del subsidio';

COMMENT ON COLUMN  "CONVOCATORIA"."PERIODO" IS 'Semestre para el cual se realiza la convocatoria';

COMMENT ON COLUMN  "CONVOCATORIA"."ESTADO" IS 'Fase en el que se puede encontrar la convocatoria con respecto a las fechas establecidas por la misma. Sus posibles valores son:
CONVOCATORIA, SIN_INICIAR, INSCRIPCION, VERIFICACION_DOC ,CALCULO_P ,ASIGNACION_S ,PUBLICACION ,CUMPLIENTO ,TERMINADA';

COMMENT ON COLUMN  "CONVOCATORIA"."VALOR_X_ALMUERZO" IS 'Precio en pesos del almuerzo';

COMMENT ON TABLE  "CONVOCATORIA_TIPO" IS 'Entidad que almacena informacion sobre las distintas condiciones o variables solicitadas para una convocatoria'
;


COMMENT ON COLUMN  "CONVOCATORIA_TIPO"."FK_ID_CONVOCATORIA" IS 'Identificador único de cada convocatoria en la base de datos';

COMMENT ON COLUMN  "CONVOCATORIA_TIPO"."FK_ID_TIPO" IS 'Identificador único de cada tipo de variable o condicion en la base de datos.';

COMMENT ON TABLE  "CONVOCATORIA_TIPO_SUBSIDIO" IS 'Entidad que almecena informacion sobre los diferentes tipos de subsidios que tendra una convocatoria'
;


COMMENT ON COLUMN  "CONVOCATORIA_TIPO_SUBSIDIO"."FK_ID_CONVOCATORIA" IS 'Identificador único de cada convocatoria en la base de datos';

COMMENT ON COLUMN  "CONVOCATORIA_TIPO_SUBSIDIO"."FK_ID_TIPO_SUBSIDIO" IS 'Identificador único de cada tipo de subsidio en la base de datos.';

COMMENT ON COLUMN  "CONVOCATORIA_TIPO_SUBSIDIO"."CANTIDAD" IS 'Cupos disponibles para ese tipo de subsidio y convocatoria';

COMMENT ON TABLE  "DOCUMENTOS" IS 'Esta tabla almacena los documentos enviados por medio de la solicitud del estudiante a la convocatoria'
;


COMMENT ON COLUMN  "DOCUMENTOS"."ID_DOCUMENTO" IS 'Identificador único de cada documento en la base de datos.';

COMMENT ON COLUMN  "DOCUMENTOS"."RUTA" IS 'Un enlace o ruta que redirige a la ubicación del documento. Es una URL ';

COMMENT ON COLUMN  "DOCUMENTOS"."ESTADO" IS 'El estado actual del documento, que puede ser: SIN_CALIFICAR, APROBADO, RECHAZADO.';

COMMENT ON TABLE  "ESTUDIANTES" IS 'Esta tabla almacena información sobre los estudiantes matriculados en la institución educativa. '
;


COMMENT ON COLUMN  "ESTUDIANTES"."CODIGO" IS 'numero de identificacion del estudiante asignado por la universidad';

COMMENT ON COLUMN  "ESTUDIANTES"."PROYECTO" IS 'Carrera a la que pertenece dentro de la universidad';

COMMENT ON COLUMN  "ESTUDIANTES"."SEMESTRE" IS 'Numero de semestre que esta cursando';

COMMENT ON COLUMN  "ESTUDIANTES"."TIPO_DOCUMENTO" IS 'El tipo de documento de identificación del estudiante, como cédula de ciudadanía, pasaporte, tarjeta de identidad, etc.';

COMMENT ON COLUMN  "ESTUDIANTES"."DOCUMENTO" IS 'El número de documento oficial de identificación del estudiante';

COMMENT ON COLUMN  "ESTUDIANTES"."NOMBRES" IS 'Los nombres del estudiante.';

COMMENT ON COLUMN  "ESTUDIANTES"."APELLIDOS" IS 'Los apellidos del estudiante';

COMMENT ON COLUMN  "ESTUDIANTES"."TELEFONO" IS 'El número de teléfono de contacto del estudiante.';

COMMENT ON COLUMN  "ESTUDIANTES"."DIRECCION" IS 'La dirección física o domicilio del estudiante.';

COMMENT ON COLUMN  "ESTUDIANTES"."MUNICIPIO" IS 'Nombre del municipio en el que reside el estudiante';

COMMENT ON COLUMN  "ESTUDIANTES"."COSTO_SEM" IS 'El costo asociado al semestre académico para el estudiante';

COMMENT ON COLUMN  "ESTUDIANTES"."INGRESOS" IS 'Esta dato almacena el valor relacionada con los ingresos económicos del estudiante y su familia. Estos datos pueden ser utilizados para determinar la elegibilidad para el apoyo alimentario';

COMMENT ON COLUMN  "ESTUDIANTES"."PROMEDIO_PONDERADO" IS 'Promedio asociado al estudiante que ha obtenido durante la carrera';

COMMENT ON COLUMN  "ESTUDIANTES"."ASIG_PERDIDAS_SEM_PASADO" IS 'Numero de materias reprobadas en el ultimo semestre cursado';

COMMENT ON COLUMN  "ESTUDIANTES"."NUM_CREDITOS" IS 'Numero de creditos asociados a las materias cursadas por el estudiante en el semestre actual';

COMMENT ON COLUMN  "ESTUDIANTES"."ESTADO" IS 'Situacion del estudiante dentro de la universidad. Puede estar: ACTIVO o INACTIVO.';

COMMENT ON COLUMN  "ESTUDIANTES"."USUARIO" IS 'Permite saber el usuario que cierto estudiante tiene en la tabla users del SMDB';

COMMENT ON TABLE  "RESPONSABLE" IS 'Entidad que almacena informacion sobre funcionario administrativo presente en el apoyo alimentario'
;


COMMENT ON COLUMN  "RESPONSABLE"."DOCUMENTO" IS 'El número de documento oficial de identificación del responsable';

COMMENT ON COLUMN  "RESPONSABLE"."TIPO_DOCUMENTO" IS 'El tipo de documento de identificación del responsable, como cédula de ciudadanía, pasaporte, tarjeta de identidad, etc.';

COMMENT ON COLUMN  "RESPONSABLE"."NOMBRES" IS 'Nombres del responsable';

COMMENT ON COLUMN  "RESPONSABLE"."APELLIDOS" IS 'Apellidos del responsable';

COMMENT ON COLUMN  "RESPONSABLE"."TELEFONO" IS 'Numero de Telefono del responsable';

COMMENT ON COLUMN  "RESPONSABLE"."DIRECCION" IS 'Direccion fisica del hogar del responsable';

COMMENT ON COLUMN  "RESPONSABLE"."USUARIO" IS 'Usuario que se relaciona con el que tiene en la tabla dba_users';

COMMENT ON TABLE  "SOLICITUDES" IS 'Esta tabla almacena informacion con respecto a la solicitud que haran los estudiantes sobre las convocatorias al apoyo alimentario'
;


COMMENT ON COLUMN  "SOLICITUDES"."ID_SOLICITUD" IS 'Identificador único de cada solicitud de apoyo alimentario.';

COMMENT ON COLUMN  "SOLICITUDES"."FECHA_CREACION" IS 'La fecha y hora en que se creó la solicitud.';

COMMENT ON COLUMN  "SOLICITUDES"."ESTADO" IS 'El estado actual de la solicitud, que puede ser: SIN_CALIFICAR, APROBADA, RECHAZADA.';

COMMENT ON COLUMN  "SOLICITUDES"."PUNTAJE_TOTAL" IS 'El puntaje total obtenido por el estudiante en su solicitud. El puntaje puede estar en el rango de 0 a 100.';

COMMENT ON COLUMN  "SOLICITUDES"."MOTIVO_RECHAZO" IS 'Una descripción corta del motivo por el cual se rechazó la solicitud, en caso de que la solicitud haya sido rechazada.';

CREATE SEQUENCE "SEQ_SOLICITUDES_ID_SOLICITUD" 
	INCREMENT BY 1 
	START WITH 1 
	NOMAXVALUE 
	MINVALUE  1 
	NOCYCLE 
	NOCACHE 
	NOORDER
;


CREATE OR REPLACE TRIGGER "TRG_SOLICITUDES_ID_SOLICITUD" 
	BEFORE INSERT 
	ON "SOLICITUDES" 
	FOR EACH ROW 
	BEGIN 
		SELECT "SEQ_SOLICITUDES_ID_SOLICITUD".NEXTVAL 
		INTO :NEW."ID_SOLICITUD" 
		FROM DUAL; 
	END;

/


COMMENT ON TABLE  "SOLICITUDES_APROBADAS" IS 'Entidad que almacena informacion sobre las solicitudes que fueron seleccionados para ser beneficiarios del subsidio'
;


COMMENT ON COLUMN  "SOLICITUDES_APROBADAS"."ID_APROBACION" IS 'Identificador único de cada solicitud en la base de datos';

COMMENT ON COLUMN  "SOLICITUDES_APROBADAS"."FECHA_APROBACION" IS 'Fecha en la que se aprobo la solicitud';

COMMENT ON COLUMN  "SOLICITUDES_APROBADAS"."ESTADO" IS 'Descripcion de si el subsidio se encuentra activo o no para el estudiante. Sus posibles valores son: APROBADA o REVOCADA.';

COMMENT ON COLUMN  "SOLICITUDES_APROBADAS"."MOTIVO_FINALIZACION" IS 'Motivo por el cual el estudiante ya no recibe mas el subsidio';

COMMENT ON TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" IS 'Entidad que guarda informacion acerca de los estudiantes con solicitud aprobada y las actividades de apoyo que deben realizar'
;


COMMENT ON COLUMN  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO"."FK_ID_ACTIVIDAD" IS 'Identificador unico sobre la actividad de apoyo';

COMMENT ON COLUMN  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO"."FK_ID_APROBACION" IS 'Identificador único de cada solicitud en la base de datos';

COMMENT ON COLUMN  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO"."HRS_ASISTENCIA" IS 'Horas realizadas en la actividad de apoyo';

COMMENT ON TABLE  "TICKET" IS 'Entidad que almacena informacion sobre los tickets asociados a una ticketera'
;


COMMENT ON COLUMN  "TICKET"."CODIGO" IS 'Identificador unico del ticket';

COMMENT ON COLUMN  "TICKET"."FECHA" IS 'Fecha en la que se reclama el ticket';

COMMENT ON COLUMN  "TICKET"."RECLAMADO" IS 'Estado en el que se encuentra el ticket, puede estar reclamado o no';

COMMENT ON TABLE  "TIPO" IS 'Esta tabla almacena informacion asociada a cada variable o condicion que se solicitara en cada convocatoria. '
;


COMMENT ON COLUMN  "TIPO"."ID_TIPO" IS 'Identificador único de cada tipo de variable o condicion en la base de datos.';

COMMENT ON COLUMN  "TIPO"."NOMBRE" IS 'El nombre o la descripción del tipo de variable.';

COMMENT ON COLUMN  "TIPO"."PUNTAJE_MAX" IS 'El puntaje máximo asignado a las variables en el proceso de convocatoria. Indica el valor máximo que una variable puede contribuir al puntaje total.';

COMMENT ON TABLE  "TIPO_SUBSIDIO" IS 'Esta tabla almacena información sobre los diferentes tipos de subsidio disponibles, incluyendo detalles sobre las horas de dedicación por semana y el porcentaje de cobertura asociado a cada tipo.'
;


COMMENT ON COLUMN  "TIPO_SUBSIDIO"."ID_TIPO_SUBSIDIO" IS 'Identificador único de cada tipo de subsidio en la base de datos.';

COMMENT ON COLUMN  "TIPO_SUBSIDIO"."NOMBRE" IS 'El nombre o la descripción del tipo de subsidio, como "Total," "Tipo A," o "Tipo B."';

COMMENT ON COLUMN  "TIPO_SUBSIDIO"."POR_COBERTURA" IS 'El porcentaje de cobertura del subsidio. Indica cuánto del subsidio total se cubre para este tipo. Puede ser el 100% para "Total," el 70% para "Tipo A," o el 40% para "Tipo B."';

COMMENT ON COLUMN  "TIPO_SUBSIDIO"."HRS_DEDICACION_X_SEM" IS 'La cantidad de horas de dedicación requeridas por semana como deber de ser beneficiario del subsidio';

COMMENT ON TABLE  "TIQUETERA" IS 'Entidad que almacena informacion sobre la etiquetera que se le entrega a cada estudiante'
;


COMMENT ON COLUMN  "TIQUETERA"."CODIGO_TIQUETERA" IS 'Codigo generado mes a mes que agrupa los tickets de un mes en particular';

COMMENT ON COLUMN  "TIQUETERA"."FECHA_I_VIGENCIA" IS 'Fecha desde cuando esta activa la tiquetera para reclamar el subsidio';

COMMENT ON COLUMN  "TIQUETERA"."FECHA_F_VIGENCIA" IS 'Fecha de finalizacion de la tiquetera para reclamar el subsidio';

COMMENT ON COLUMN  "TIQUETERA"."ESTADO" IS 'Situacion en la que se encuentra la tiquetera, si esta ACTIVA o INACTIVA.';

/* Create Primary Keys, Indexes, Uniques, Checks, Triggers */

ALTER TABLE  "ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "PK_ACTIVIDADES__01"
	PRIMARY KEY ("ID_ACTIVIDAD") 
 USING INDEX
;

CREATE INDEX "IXFK_ACTIVIDADES__RESPONS01"   
 ON  "ACTIVIDADES_DE_APOYO" ("FK_RESPONSABLE_SUPERVISAR") 
;

ALTER TABLE  "CONDICIONES" 
 ADD CONSTRAINT "PK_CONDICIONES"
	PRIMARY KEY ("ID_CONDICION") 
 USING INDEX
;

ALTER TABLE  "CONDICIONES" 
 ADD CONSTRAINT "CHK_PUNTAJE_CONDICION" CHECK (PUNTAJE > 0)
;

CREATE INDEX "IXFK_CONDICIONES_TIPO"   
 ON  "CONDICIONES" ("FK_ID_TIPO") 
;

ALTER TABLE  "CONVOCATORIA" 
 ADD CONSTRAINT "PK_CONVOCATORIA"
	PRIMARY KEY ("ID_CONVOCATORIA") 
 USING INDEX
;

ALTER TABLE  "CONVOCATORIA" 
 ADD CONSTRAINT "UK_PERIODO_CONVOCATORIA" UNIQUE ("PERIODO") 
 USING INDEX
;

ALTER TABLE  "CONVOCATORIA" 
 ADD CONSTRAINT "CHK_ESTADO_CONVOCATORIA" CHECK (ESTADO IN ('SIN_INICIAR', 'INSCRIPCION', 'VERIFICACION_DOC', 'CALCULO_P', 'ASIGNACION_S', 'PUBLICACION', 'CUMPLIENTO', 'TERMINADA'))
;

ALTER TABLE  "CONVOCATORIA" 
 ADD CONSTRAINT "CHK_FECHAS_CONVOCATORIA" CHECK (FECHA_I_CONV  < FECHA_I_INSC AND
FECHA_I_INSC  < FECHA_I_VERIF AND
FECHA_I_VERIF < FECHA_I_PUBL AND
FECHA_I_PUBL  < FECHA_I_CUMP AND
FECHA_I_CUMP  < FECHA_F_CUMP )
;

ALTER TABLE  "CONVOCATORIA" 
 ADD CONSTRAINT "CHK_VALOR_X_ALMUERZO_CONVOCATORIA" CHECK (VALOR_X_ALMUERZO > 0)
;

ALTER TABLE  "CONVOCATORIA_TIPO" 
 ADD CONSTRAINT "PK_CONVOCATORIA_01"
	PRIMARY KEY ("FK_ID_CONVOCATORIA","FK_ID_TIPO") 
 USING INDEX
;

CREATE INDEX "IXFK_CONVOCATORIA_CONVOCA01"   
 ON  "CONVOCATORIA_TIPO" ("FK_ID_CONVOCATORIA") 
;

CREATE INDEX "IXFK_CONVOCATORIA_TIPO_TIPO"   
 ON  "CONVOCATORIA_TIPO" ("FK_ID_TIPO") 
;

ALTER TABLE  "CONVOCATORIA_TIPO_SUBSIDIO" 
 ADD CONSTRAINT "PK_CONVOCATORIA_02"
	PRIMARY KEY ("FK_ID_CONVOCATORIA","FK_ID_TIPO_SUBSIDIO") 
 USING INDEX
;

ALTER TABLE  "CONVOCATORIA_TIPO_SUBSIDIO" 
 ADD CONSTRAINT "CHK_CANTIDAD" CHECK (CANTIDAD > 0)
;

CREATE INDEX "IXFK_CONVOCATORIA_CONVOCAT_02"   
 ON  "CONVOCATORIA_TIPO_SUBSIDIO" ("FK_ID_CONVOCATORIA") 
;

CREATE INDEX "IXFK_CONVOCATORIA_TIPO_SU01"   
 ON  "CONVOCATORIA_TIPO_SUBSIDIO" ("FK_ID_TIPO_SUBSIDIO") 
;

ALTER TABLE  "DOCUMENTOS" 
 ADD CONSTRAINT "PK_DOCUMENTOS"
	PRIMARY KEY ("ID_DOCUMENTO","FK_ID_SOLICITUD") 
 USING INDEX
;

ALTER TABLE  "DOCUMENTOS" 
 ADD CONSTRAINT "CHK_ESTADO_DOCUMENTOS" CHECK (ESTADO IN ('SIN_CALIFICAR', 'APROBADO', 'RECHAZADO'))
;

CREATE INDEX "IXFK_DOCUMENTOS_CONDICIONES"   
 ON  "DOCUMENTOS" ("FK_ID_CONDICION") 
;

CREATE INDEX "IXFK_DOCUMENTOS_SOLICITUDES"   
 ON  "DOCUMENTOS" ("FK_ID_SOLICITUD") 
;

ALTER TABLE  "ESTUDIANTES" 
 ADD CONSTRAINT "PK_ESTUDIANTES"
	PRIMARY KEY ("CODIGO") 
 USING INDEX
;

ALTER TABLE  "ESTUDIANTES" 
 ADD CONSTRAINT "UK_USUARIO_ESTUDIANTES" UNIQUE ("USUARIO") 
 USING INDEX
;

ALTER TABLE  "ESTUDIANTES" 
 ADD CONSTRAINT "CHK_ESTADO_ESTUDIANTE" CHECK (ESTADO IN ('ACTIVO', 'INACTIVO'))
;

ALTER TABLE  "RESPONSABLE" 
 ADD CONSTRAINT "PK_RESPONSABLE"
	PRIMARY KEY ("DOCUMENTO") 
 USING INDEX
;

ALTER TABLE  "RESPONSABLE" 
 ADD CONSTRAINT "UK_USUARIO_RESPONSABLE" UNIQUE ("USUARIO") 
 USING INDEX
;

ALTER TABLE  "SOLICITUDES" 
 ADD CONSTRAINT "PK_SOLICITUDES"
	PRIMARY KEY ("ID_SOLICITUD") 
 USING INDEX
;

ALTER TABLE  "SOLICITUDES" 
 ADD CONSTRAINT "CHK_ESTADO_SOLICITUDES" CHECK (ESTADO IN ('SIN_CALIFICAR', 'APROBADA', 'VERIFICADA', 'RECHAZADA'))
;

CREATE INDEX "IXFK_SOLICITUDES_CONVOCATORIA"   
 ON  "SOLICITUDES" ("FK_ID_CONVOCATORIA") 
;

CREATE INDEX "IXFK_SOLICITUDES_ESTUDIANTES"   
 ON  "SOLICITUDES" ("FK_CODIGO") 
;

CREATE INDEX "IXFK_SOLICITUDES_RESPONSABLE"   
 ON  "SOLICITUDES" ("FK_RESPONSABLE_VERIFICAR") 
;

ALTER TABLE  "SOLICITUDES_APROBADAS" 
 ADD CONSTRAINT "PK_SOLICITUDES__01"
	PRIMARY KEY ("ID_APROBACION") 
 USING INDEX
;

ALTER TABLE  "SOLICITUDES_APROBADAS" 
 ADD CONSTRAINT "CHK_ESTADO_SOLICITUDES_APROBADAS" CHECK (ESTADO IN ('APROBADA', 'REVOCADA'))
;

CREATE INDEX "IXFK_SOLICITUDES__ID_SOL_2"   
 ON  "SOLICITUDES_APROBADAS" ("FK_ID_SOLICITUD") 
;

CREATE INDEX "IXFK_SOLICITUDES__RESPONS01"   
 ON  "SOLICITUDES_APROBADAS" ("FK_RESPONSABLE_APROBAR") 
;

CREATE INDEX "IXFK_SOLICITUDES__TIPO_SU01"   
 ON  "SOLICITUDES_APROBADAS" ("FK_ID_TIPO_SUBSIDIO") 
;

ALTER TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "PK_SOLICITUDES__02"
	PRIMARY KEY ("FK_ID_ACTIVIDAD","FK_ID_APROBACION") 
 USING INDEX
;

ALTER TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "CHK_HRS_ASISTENCIA" CHECK (HRS_ASISTENCIA > 0)
;

CREATE INDEX "IXFK_SOLICITUDES__ACTIVID01"   
 ON  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" ("FK_ID_ACTIVIDAD") 
;

CREATE INDEX "IXFK_SOLICITUDES__SOLICIT01"   
 ON  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" ("FK_ID_APROBACION") 
;

ALTER TABLE  "TICKET" 
 ADD CONSTRAINT "PK_TICKET"
	PRIMARY KEY ("CODIGO","CODIGO_TIQUETERA") 
 USING INDEX
;

ALTER TABLE  "TICKET" 
 ADD CONSTRAINT "CHK_RECLAMADO_TICKET" CHECK (RECLAMADO IN ('SI', 'NO'))
;

CREATE INDEX "IXFK_TICKET_TIQUETERA"   
 ON  "TICKET" ("CODIGO_TIQUETERA") 
;

ALTER TABLE  "TIPO" 
 ADD CONSTRAINT "PK_TIPO"
	PRIMARY KEY ("ID_TIPO") 
 USING INDEX
;

ALTER TABLE  "TIPO_SUBSIDIO" 
 ADD CONSTRAINT "PK_TIPO_SUBSIDIO"
	PRIMARY KEY ("ID_TIPO_SUBSIDIO") 
 USING INDEX
;

ALTER TABLE  "TIPO_SUBSIDIO" 
 ADD CONSTRAINT "CHK_HRS_DEDICACION_X_DEM_TIPO_SUBSIDIO" CHECK (HRS_DEDICACION_X_SEM > 0)
;

ALTER TABLE  "TIPO_SUBSIDIO" 
 ADD CONSTRAINT "CHK_POR_COBERTURA_TIPO_SUBSIDIO" CHECK (POR_COBERTURA > 0)
;

ALTER TABLE  "TIQUETERA" 
 ADD CONSTRAINT "PK_TIQUETERA"
	PRIMARY KEY ("CODIGO_TIQUETERA") 
 USING INDEX
;

ALTER TABLE  "TIQUETERA" 
 ADD CONSTRAINT "CHK_ESTADO_TIQUETERA" CHECK (ESTADO IN ('ACTIVA', 'INACTIVA'))
;

CREATE INDEX "IXFK_TIQUETERA_SOLICITUDE01"   
 ON  "TIQUETERA" ("FK_ID_APROBACION") 
;

/* Create Foreign Key Constraints */

ALTER TABLE  "ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "FK_ACTIVIDADES__RESPONSABLE_01"
	FOREIGN KEY ("FK_RESPONSABLE_SUPERVISAR") REFERENCES  "RESPONSABLE" ("DOCUMENTO")
;

ALTER TABLE  "CONDICIONES" 
 ADD CONSTRAINT "FK_CONDICIONES_TIPO"
	FOREIGN KEY ("FK_ID_TIPO") REFERENCES  "TIPO" ("ID_TIPO")
;

ALTER TABLE  "CONVOCATORIA_TIPO" 
 ADD CONSTRAINT "FK_CONVOCATORIA_CONVOCATORI_01"
	FOREIGN KEY ("FK_ID_CONVOCATORIA") REFERENCES  "CONVOCATORIA" ("ID_CONVOCATORIA")
;

ALTER TABLE  "CONVOCATORIA_TIPO" 
 ADD CONSTRAINT "FK_CONVOCATORIA_TIPO_TIPO"
	FOREIGN KEY ("FK_ID_TIPO") REFERENCES  "TIPO" ("ID_TIPO")
;

ALTER TABLE  "CONVOCATORIA_TIPO_SUBSIDIO" 
 ADD CONSTRAINT "FK_CONVOCATORIA_CONVOCATORI_02"
	FOREIGN KEY ("FK_ID_CONVOCATORIA") REFERENCES  "CONVOCATORIA" ("ID_CONVOCATORIA")
;

ALTER TABLE  "CONVOCATORIA_TIPO_SUBSIDIO" 
 ADD CONSTRAINT "FK_CONVOCATORIA_TIPO_SUBSID_01"
	FOREIGN KEY ("FK_ID_TIPO_SUBSIDIO") REFERENCES  "TIPO_SUBSIDIO" ("ID_TIPO_SUBSIDIO")
;

ALTER TABLE  "DOCUMENTOS" 
 ADD CONSTRAINT "FK_DOCUMENTOS_CONDICIONES"
	FOREIGN KEY ("FK_ID_CONDICION") REFERENCES  "CONDICIONES" ("ID_CONDICION")
;

ALTER TABLE  "DOCUMENTOS" 
 ADD CONSTRAINT "FK_DOCUMENTOS_SOLICITUDES"
	FOREIGN KEY ("FK_ID_SOLICITUD") REFERENCES  "SOLICITUDES" ("ID_SOLICITUD")
;

ALTER TABLE  "SOLICITUDES" 
 ADD CONSTRAINT "FK_SOLICITUDES_CONVOCATORIA"
	FOREIGN KEY ("FK_ID_CONVOCATORIA") REFERENCES  "CONVOCATORIA" ("ID_CONVOCATORIA")
;

ALTER TABLE  "SOLICITUDES" 
 ADD CONSTRAINT "FK_SOLICITUDES_ESTUDIANTES"
	FOREIGN KEY ("FK_CODIGO") REFERENCES  "ESTUDIANTES" ("CODIGO")
;

ALTER TABLE  "SOLICITUDES" 
 ADD CONSTRAINT "FK_SOLICITUDES_RESPONSABLE"
	FOREIGN KEY ("FK_RESPONSABLE_VERIFICAR") REFERENCES  "RESPONSABLE" ("DOCUMENTO")
;

ALTER TABLE  "SOLICITUDES_APROBADAS" 
 ADD CONSTRAINT "FK_SOLICITUDES__RESPONSABLE_01"
	FOREIGN KEY ("FK_RESPONSABLE_APROBAR") REFERENCES  "RESPONSABLE" ("DOCUMENTO")
;

ALTER TABLE  "SOLICITUDES_APROBADAS" 
 ADD CONSTRAINT "FK_SOLICITUDES__SOLICITUDES_01"
	FOREIGN KEY ("FK_ID_SOLICITUD") REFERENCES  "SOLICITUDES" ("ID_SOLICITUD")
;

ALTER TABLE  "SOLICITUDES_APROBADAS" 
 ADD CONSTRAINT "FK_SOLICITUDES__TIPO_SUBSID_01"
	FOREIGN KEY ("FK_ID_TIPO_SUBSIDIO") REFERENCES  "TIPO_SUBSIDIO" ("ID_TIPO_SUBSIDIO")
;

ALTER TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "FK_SOLICITUDES__ACTIVIDADES_01"
	FOREIGN KEY ("FK_ID_ACTIVIDAD") REFERENCES  "ACTIVIDADES_DE_APOYO" ("ID_ACTIVIDAD")
;

ALTER TABLE  "SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO" 
 ADD CONSTRAINT "FK_SOLICITUDES__SOLICITUDES_02"
	FOREIGN KEY ("FK_ID_APROBACION") REFERENCES  "SOLICITUDES_APROBADAS" ("ID_APROBACION")
;

ALTER TABLE  "TICKET" 
 ADD CONSTRAINT "FK_TICKET_TIQUETERA"
	FOREIGN KEY ("CODIGO_TIQUETERA") REFERENCES  "TIQUETERA" ("CODIGO_TIQUETERA")
;

ALTER TABLE  "TIQUETERA" 
 ADD CONSTRAINT "FK_TIQUETERA_SOLICITUDES_AP_01"
	FOREIGN KEY ("FK_ID_APROBACION") REFERENCES  "SOLICITUDES_APROBADAS" ("ID_APROBACION")
;
