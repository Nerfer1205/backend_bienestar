CREATE OR REPLACE PACKAGE BODY PK_ASIGNAR_BENEFICIO AS 
    /*-----------------------------------------------------------------------------------
    Proyecto   : Proyecto Apoyo alimentario . Curso BDII
    Descripcion: Paquete que contiene las variables globales, funciones y procedimientos
                asociados al módulo de Asignación de puntajes
    Autor      : Grupo ###.
    --------------------------------------------------------------------------------------*/
    
    /*------------------------------------------------------------------------------
    Procedimiento para asignar subsidios a solicitud
    Parametros de Entrada:
    - pk_id_convocatoria: Código de la convocatoria a la que se asignarán los subsidios.
    - pv_solicitudes_tp_subsidio: Arreglo de registros que contiene las solicitud y sus tipos de subsidio.
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la asignación de subsidios.
        = 0: Éxito en la asignación.
        = 2: Error, el índice no existe en el vector.
    - pm_error: Mensaje de error en caso de que ocurra un problema o null en caso de éxito.
    */
    PROCEDURE PR_ASIGNAR_SUBSIDIO_A_SOLICITUDES(
    pk_id_convocatoria IN convocatoria.id_convocatoria%TYPE,
    pv_solicitudes_tp_subsidio IN OUT gt_solicitudes_tipo_sub,
    pc_error OUT NUMBER,
    pm_error OUT VARCHAR
    )
    IS
    -- Declaración de un cursor que selecciona tipos de subsidio disponibles para la convocatoria
    CURSOR c_tipo_subsidio(ck_id_convocatoria convocatoria.id_convocatoria%TYPE) IS
        SELECT ts.id_tipo_subsidio, cts.cantidad FROM convocatoria_tipo_subsidio cts, tipo_subsidio ts
        WHERE cts.fk_id_convocatoria = 2 and ts.id_tipo_subsidio = cts.fk_id_tipo_subsidio
        ORDER BY ts.por_cobertura DESC, ts.hrs_dedicacion_x_sem ASC;
    --Declaración de variables locales
    ln_pos_actual NUMBER(10);
    ln_cantidad_disp NUMBER(10);
    BEGIN
        pc_error := 0; 
        pm_error := null;
        ln_pos_actual := 1;
    
        -- Iterar a través de los tipos de subsidio disponibles
        FOR lc_tipo_subsidio IN c_tipo_subsidio(pk_id_convocatoria) LOOP
            ln_cantidad_disp := lc_tipo_subsidio.cantidad;
            -- Iterar a través de las solicitud y asignar subsidios
            FOR i IN ln_pos_actual..pv_solicitudes_tp_subsidio.COUNT LOOP
                pv_solicitudes_tp_subsidio(i).k_id_tipo_subsidio := lc_tipo_subsidio.id_tipo_subsidio;
                ln_cantidad_disp := ln_cantidad_disp - 1;
                -- Salir del bucle interno si no quedan subsidios disponibles
                
                ln_pos_actual := i + 1;
                
                IF ln_cantidad_disp = 0 THEN
                    EXIT;
                END IF;                
            END LOOP;
            -- Salir del bucle externo si se han asignado todos los subsidios
            IF ln_pos_actual > pv_solicitudes_tp_subsidio.COUNT THEN
                EXIT;
            END IF;
        END LOOP;
    
    -- Manejo de excepciones
    EXCEPTION
        WHEN SUBSCRIPT_OUTSIDE_LIMIT THEN
            pc_error := 4;
            pm_error := 'El índice no existe en el vector';
    END PR_ASIGNAR_SUBSIDIO_A_SOLICITUDES;




    /*------------------------------------------------------------------------------
    Procedimiento para guardar solicitud
    Parametros de Entrada:
    - pv_solicitudes_tp_subsidio: Arreglo de registros que contiene las solicitud y sus tipos de subsidio.
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación de guardado.
        = 0: Éxito en el guardado.
        = 3: Error, no hay responsables relacionados con el usuario que ejecuta el procedimiento.
    - pm_error: Mensaje de error en caso de que ocurra un problema o null en caso de éxito.
    */
    PROCEDURE PR_GUARDAR_SOLICITUDES(
        pv_solicitudes_tp_subsidio IN gt_solicitudes_tipo_sub,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    )
    IS
    -- Declaración de un cursor para seleccionar tipos de subsidio disponibles para una convocatoria
    CURSOR c_tipo_subsidio(ck_id_convocatoria convocatoria.id_convocatoria%TYPE) IS
        SELECT ts.id_tipo_subsidio, cts.cantidad FROM convocatoria_tipo_subsidio cts, tipo_subsidio ts
        WHERE cts.fk_id_convocatoria = ck_id_convocatoria 
        ORDER BY ts.por_cobertura DESC, ts.hrs_dedicacion_x_sem ASC;
    --Declaración de variables locales
    lk_id_responsable VARCHAR2(30);

    BEGIN
    pc_error := 0; 
    pm_error := null;
    -- Obtener el documento del responsable asociado al usuario que ejecuta el procedimiento
    SELECT documento INTO lk_id_responsable FROM responsable WHERE usuario = USER;

    -- Iterar a través de las solicitud en el vector
    FOR i IN 1..pv_solicitudes_tp_subsidio.COUNT LOOP
        IF pv_solicitudes_tp_subsidio(i).k_id_tipo_subsidio IS NULL THEN
            -- Si el tipo de subsidio es nulo, marcar la solicitud como 'RECHAZADA' con motivo de rechazo
            UPDATE solicitud SET estado = 'RECHAZADA', motivo_rechazo = 'Puntaje insuficiente' 
            WHERE id_solicitud = pv_solicitudes_tp_subsidio(i).k_id_solicitud;
        ELSE
            -- Si el tipo de subsidio no es nulo, marcar la solicitud como 'APROBADA'
            UPDATE solicitud SET estado = 'APROBADA' WHERE id_solicitud = pv_solicitudes_tp_subsidio(i).k_id_solicitud;
            
            -- Insertar la solicitud aprobada en la tabla "solicitud_aprobada"
            INSERT INTO solicitud_aprobada VALUES(NULL, SYSDATE, 'APROBADA', NULL, 
                pv_solicitudes_tp_subsidio(i).k_id_solicitud, 
                pv_solicitudes_tp_subsidio(i).k_id_tipo_subsidio,
                lk_id_responsable);
        END IF;        
    END LOOP;
    
    -- Manejo de excepciones
    EXCEPTION
        WHEN NO_DATA_FOUND THEN        
            pc_error := 1;
            pm_error := 'No hay responsables relacionados con el usuario que está ejecutando el procedimiento';
    END PR_GUARDAR_SOLICITUDES;



    /*-----------------------------------------------------------------------------------
    Procedimiento para asignar el beneficio de acuerdo a el puntaje obtenido en la fase anterior
    Parametros de Entrada:
    - pid_convocatoria: El Id de convocatoria a la cual se le recalculará el puntaje
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la búsqueda de convocatorias.
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_ASIGNAR_BENEFICIO(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    )
    IS
    -- Variables locales
    lc_convocatorias SYS_REFCURSOR;
    
    lv_solicitudes_tp_subsidio gt_solicitudes_tipo_sub;
    ln_contador NUMBER(10);

    lestado_conv convocatoria.estado%TYPE;

    -- Declaración de un cursor para seleccionar la solicitud a una convocatoria
    CURSOR c_solicitudes(ck_id_convocatoria convocatoria.id_convocatoria%TYPE) IS
        SELECT s.id_solicitud FROM solicitud s, estudiante e WHERE 
            s.estado IN('PUNTAJE_ASIGNADO') AND
            e.codigo = s.fk_codigo AND
            s.fk_id_convocatoria = ck_id_convocatoria
            ORDER BY s.puntaje_total DESC, e.promedio_ponderado DESC, e.asig_perdidas_sem_pasado ASC, e.ingresos ASC;

    BEGIN

        pc_error := 0; 
        pm_error := null;
        SELECT estado INTO lestado_conv FROM convocatoria WHERE id_convocatoria = pid_convocatoria;
        IF lestado_conv = 'ASIGNACION_S' THEN
        
            ln_contador := 0;
            lv_solicitudes_tp_subsidio := gt_solicitudes_tipo_sub(); -- Inicializar arreglo vacío
            
            -- Cursor para seleccionar las solicitudes de la convocatoria enviada
            FOR lc_solicitudes IN c_solicitudes(pid_convocatoria) LOOP
                ln_contador := ln_contador + 1;
                lv_solicitudes_tp_subsidio(ln_contador).k_id_solicitud := lc_solicitudes.id_solicitud;
            END LOOP;

            -- Si hay solicitud, se procede a asignar subsidios y guardar
            IF ln_contador > 0 THEN
                PR_ASIGNAR_SUBSIDIO_A_SOLICITUDES(pid_convocatoria, lv_solicitudes_tp_subsidio, pc_error, pm_error);
                IF(pc_error = 0) THEN
                    PR_GUARDAR_SOLICITUDES(lv_solicitudes_tp_subsidio, pc_error, pm_error);
                END IF;
            END IF;

            -- Actualizar el estado de la convocatoria a 'PUBLICACION' en caso de no haber error
            IF(pc_error = 0) THEN
                UPDATE convocatoria SET estado = 'PUBLICACION' WHERE id_convocatoria = pid_convocatoria;
                COMMIT;
            END IF;
        ELSE
            pc_error := 3;
            pm_error := 'La convocatoria '|| pid_convocatoria || ' no esta en el estado ASIGNACION_S';
        END IF;

    -- Manejo de excepciones
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            pc_error := 1;
            pm_error := 'La convocatoria '|| pid_convocatoria || ' no existe';
        WHEN OTHERS THEN
            pc_error := 2;
            pm_error := 'Error desconocido: ' || SQLERRM;

    END PR_ASIGNAR_BENEFICIO;
  
END PK_ASIGNAR_BENEFICIO;