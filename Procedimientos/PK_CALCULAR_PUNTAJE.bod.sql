CREATE OR REPLACE PACKAGE BODY PK_CALCULAR_PUNTAJE AS 
    /*-----------------------------------------------------------------------------------
    Proyecto   : Proyecto Apoyo alimentario . Curso BDII
    Descripcion: Paquete que contiene las variables globales, funciones y procedimientos
                asociados al módulo de Asignación de puntajes
    Autor      : Grupo ###.
    --------------------------------------------------------------------------------------*/

    /*-----------------------------------------------------------------------------------
    Procedimiento para obtener convocatorias por estado
    Parametros de Entrada:
    - pn_estado: Estado de las convocatorias a buscar.
    Parametros de Salida:
    - pc_convocatorias: Cursor de referencia que contendrá las convocatorias encontradas.
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la búsqueda de convocatorias.
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_OBTENER_CONVOCATORIAS_X_ESTADO(
        pn_estado IN VARCHAR,
        pc_convocatorias OUT SYS_REFCURSOR,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    )
    IS
    BEGIN
        -- Abre el cursor pc_convocatorias y selecciona las convocatorias con el estado especificado
        OPEN pc_convocatorias FOR SELECT id_convocatoria FROM convocatoria WHERE estado = pn_estado;
        -- TO DO: Verificar las excepciones que pueden aplicar
    END PR_OBTENER_CONVOCATORIAS_X_ESTADO;


    /*-----------------------------------------------------------------------------------
    Función para obtener la suma de puntajes por solicitud
    Parametros de Entrada:
    - pk_id_solicitud: ID de la solicitud para la cual se desea obtener la suma de puntajes.
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la obtención de la suma de puntajes.
        = 1: Error, la solicitud no tiene ningún documento.
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    Retorna:
    - Número entero que representa la suma de puntajes de la solicitud.
    */
    FUNCTION FU_OBTENER_SUMA_PUNTAJES_X_SOLICITUD(
        pk_id_solicitud IN solicitud.id_solicitud%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    ) RETURN NUMBER
    IS
        li_puntaje_obtenido NUMBER(3);
    BEGIN
        pc_error := 0; 
        pm_error := null;
        -- Obtiene la suma de puntajes obtenidos de documento verificados para la solicitud dada
        SELECT SUM(puntaje_obtenido) INTO li_puntaje_obtenido FROM documento WHERE fk_id_solicitud = pk_id_solicitud AND estado = 'VERIFICADO';
        RETURN li_puntaje_obtenido;
        -- Manejo de excepciones
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                pc_error := 1;
                pm_error := 'La solicitud '|| pk_id_solicitud || ' no tiene ningún documento';
                RETURN 0;
    END FU_OBTENER_SUMA_PUNTAJES_X_SOLICITUD;


    /*-----------------------------------------------------------------------------------
    Procedimiento para calcular el puntaje de las solicitud de cierta convocatoria
    Parametros de Entrada:
    - pid_convocatoria: El Id de convocatoria a la cual se le recalculará el puntaje
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la búsqueda de convocatorias.
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_ASIGNAR_PUNTAJE(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    )
    IS
    --Variables locales convocatoria
    lc_convocatorias SYS_REFCURSOR;
    

    --Variables locales solicitud
    CURSOR c_solicitudes(ck_id_convocatoria convocatoria.id_convocatoria%TYPE) IS
        SELECT id_solicitud FROM solicitud WHERE estado IN('SIN_CALIFICAR','VERIFICADA') AND fk_id_convocatoria = ck_id_convocatoria;

    --Variables locales documento-condicion
    CURSOR c_doc_condicion(ck_id_solicitud solicitud.id_solicitud%TYPE) IS
        SELECT  d.id_documento, c.puntaje FROM condicion c, documento d WHERE 
                d.fk_id_condicion = c.id_condicion AND
                d.fk_id_solicitud = ck_id_solicitud AND
                d.estado IN('SIN_CALIFICAR','APROBADO');

    li_puntaje NUMBER(3);

    lestado_conv convocatoria.estado%TYPE;

    BEGIN
        pc_error := 0; 
        pm_error := null;
        SELECT estado INTO lestado_conv FROM convocatoria WHERE id_convocatoria = pid_convocatoria;
        
        IF lestado_conv = 'CALCULO_P' THEN
            
            FOR lc_solicitudes IN c_solicitudes(pid_convocatoria) LOOP
                UPDATE documento d SET d.puntaje_obtenido = (SELECT c.puntaje FROM condicion c WHERE c.id_condicion = d.fk_id_condicion),
                    d.estado = 'VERIFICADO'
                    WHERE d.fk_id_solicitud = lc_solicitudes.id_solicitud AND d.estado IN('SIN_CALIFICAR','APROBADO');
                li_puntaje := FU_OBTENER_SUMA_PUNTAJES_X_SOLICITUD(lc_solicitudes.id_solicitud, pc_error, pm_error);
                --Valida que la función no haya tenido errores
                IF(pc_error = 0) THEN
                    UPDATE solicitud SET puntaje_total = li_puntaje, estado = 'PUNTAJE_ASIGNADO' WHERE id_solicitud = lc_solicitudes.id_solicitud;
                END IF;            
            END LOOP;
            IF(pc_error = 0) THEN
                UPDATE convocatoria SET estado = 'ASIGNACION_S' WHERE id_convocatoria = pid_convocatoria;
                COMMIT;
            ELSE
                ROLLBACK;
            END IF;
        ELSE
            pc_error := 3;
            pm_error := 'La convocatoria '|| pid_convocatoria || ' no esta en el estado CALCULO_P';
        END IF;
        
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            pc_error := 1;
            pm_error := 'La convocatoria '|| pid_convocatoria || ' no existe';
        WHEN OTHERS THEN
            pc_error := 2;
            pm_error := 'Error desconocido: ' || SQLERRM;

    END PR_ASIGNAR_PUNTAJE;


END PK_CALCULAR_PUNTAJE;
