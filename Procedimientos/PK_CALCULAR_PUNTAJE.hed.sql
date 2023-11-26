CREATE OR REPLACE PACKAGE PK_CALCULAR_PUNTAJE AS 
/*-----------------------------------------------------------------------------------
  Proyecto   : Apoto Aliemntario. Curso BDII
  Descripcion: Paquete que contiene las variables globales, funciones y procedimientos
               asociados al módulo de calculo de puntajes
  Autor	     : Grupo ##
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
    );

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
    ) RETURN NUMBER;

    /*-----------------------------------------------------------------------------------
    Procedimiento para calcular el puntaje de las solicitud de cierta convocatoria
    Parametros de Entrada:
    - pid_convocatoria: El Id de convocatoria a la cual se le recalculará el puntaje
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la ejecución del procedimiento
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_ASIGNAR_PUNTAJE(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    );

END PK_CALCULAR_PUNTAJE;