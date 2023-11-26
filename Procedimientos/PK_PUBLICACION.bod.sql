CREATE OR REPLACE PACKAGE BODY PK_PUBLICACION AS 

    -- Procedimiento para guardar un listado en un archivo
    PROCEDURE PR_GUARDAR_LISTADO(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    )
    IS
        lc_convocatorias SYS_REFCURSOR;
        lf_archivo UTL_FILE.FILE_TYPE;
        lestado_conv convocatoria.estado%TYPE;
        -- Cursor para obtener solicitud aprobadas
        CURSOR c_solicitudes(ck_id_convocatoria convocatoria.id_convocatoria%TYPE) IS
            SELECT s.id_solicitud, s.puntaje_total, e.nombres, e.apellidos, ts.nombre FROM solicitud s, estudiante e, solicitud_aprobada sa, tipo_subsidio ts WHERE 
                s.estado IN ('APROBADA') AND
                e.codigo = s.fk_codigo AND
                sa.fk_id_solicitud = s.id_solicitud AND
                sa.fk_id_tipo_subsidio = ts.id_tipo_subsidio AND
                s.fk_id_convocatoria = ck_id_convocatoria
                ORDER BY s.puntaje_total DESC, e.promedio_ponderado DESC, e.asig_perdidas_sem_pasado ASC, e.ingresos ASC;

    BEGIN
        -- Inicialización de variables locales
        pc_error := 0; 
        pm_error := null;
        --Verificar que el estado de la convocatoria sea PUBLICACION
        DBMS_OUTPUT.PUT_LINE('Pero dime'); 
        SELECT estado INTO lestado_conv FROM convocatoria WHERE id_convocatoria = pid_convocatoria;
        DBMS_OUTPUT.PUT_LINE(lestado_conv); 
        IF lestado_conv = 'PUBLICACION' THEN
    
            -- Abrir el archivo para escritura en el directorio especificado
            lf_archivo := UTL_FILE.FOPEN('DIRECTORIO_DE_ARCHIVOS', 'reporte.txt', 'W');
            DBMS_OUTPUT.PUT_LINE('kha'); 
            -- Escribir información de la convocatoria en el archivo
            UTL_FILE.PUT_LINE(lf_archivo, 'Convocatoria: ' || pid_convocatoria);
            UTL_FILE.PUT_LINE(lf_archivo, 'Id Solicitud' || CHR(9) || 'Puntaje Total' || CHR(9) || 'Estudiante' || CHR(9) || CHR(9) || CHR(9) || 'Tipo Subsidio');

            -- Recorrer y escribir las solicitud aprobadas
            FOR lc_solicitudes IN c_solicitudes(pid_convocatoria) LOOP
                UTL_FILE.PUT_LINE(lf_archivo, lc_solicitudes.id_solicitud || CHR(9) || CHR(9) || lc_solicitudes.puntaje_total || CHR(9) || CHR(9) || lc_solicitudes.nombres || ' ' || lc_solicitudes.apellidos || CHR(9) || CHR(9) || CHR(9) || lc_solicitudes.nombre);
            END LOOP;
            -- Cerrar el archivo
            UTL_FILE.FCLOSE(lf_archivo);
        ELSE 
            pc_error := 2;
            pm_error := 'La convocatoria no esta en estado PUBLICACION';
        END IF;
    -- Manejo de excepciones
    EXCEPTION
        WHEN UTL_FILE.INVALID_PATH THEN
            pc_error := 5;
            pm_error := 'El directorio no es valido o no existe';
        WHEN UTL_FILE.INVALID_FILEHANDLE THEN
            pc_error := 6;
            pm_error := 'El archivo no se puede manipular';
        WHEN UTL_FILE.WRITE_ERROR THEN
            pc_error := 7;
            pm_error := 'El archivo no se puede escribir';
        WHEN NO_DATA_FOUND THEN
            pc_error := 1;
            pm_error := 'La convocatoria '|| pid_convocatoria || ' no existe';
        WHEN OTHERS THEN
            pc_error := 2;
            pm_error := 'Error desconocido: ' || SQLERRM;

    END PR_GUARDAR_LISTADO;

END PK_PUBLICACION;
