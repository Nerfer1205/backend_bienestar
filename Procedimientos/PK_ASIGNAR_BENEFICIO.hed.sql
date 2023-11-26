CREATE OR REPLACE PACKAGE PK_ASIGNAR_BENEFICIO AS 
/*-----------------------------------------------------------------------------------
  Proyecto   : Apoto Aliemntario. Curso BDII
  Descripcion: Paquete que contiene las variables globales, funciones y procedimientos
               asociados al módulo de aprobacion de solicitud
  Autor	     : Grupo ##
--------------------------------------------------------------------------------------*/
   -- Definición de un tipo de registro para representar solicitud con su tipo de subsidio
    TYPE gt_solicitudes_t IS RECORD(
        k_id_solicitud solicitud.id_solicitud%TYPE,
        k_id_tipo_subsidio tipo_subsidio.id_tipo_subsidio%TYPE
    );
    -- Definición de un tipo de tabla indexada por números enteros para almacenar registros de solicitud
    type gt_solicitudes_tipo_sub IS TABLE OF gt_solicitudes_t INDEX BY BINARY_INTEGER;

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
    );

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
    );


    /*-----------------------------------------------------------------------------------
    Procedimiento para asignar el beneficio de acuerdo a el puntaje obtenido en la fase anterior
    Parametros de Entrada:
    - pid_convocatoria: El Id de convocatoria a la cual se le recalculará el puntaje
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la ejecución del procedimiento
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_ASIGNAR_BENEFICIO(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    );

END PK_ASIGNAR_BENEFICIO;