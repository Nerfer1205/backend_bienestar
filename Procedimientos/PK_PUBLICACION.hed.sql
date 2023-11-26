CREATE OR REPLACE PACKAGE PK_PUBLICACION AS 
    /*-----------------------------------------------------------------------------------
    Proyecto   : Apoyo Alimentario. Curso BDII
    Descripción: Paquete que contiene las variables globales, funciones y procedimientos
                asociados al módulo de asignación de cupos
    Autor      : Grupo ##
    --------------------------------------------------------------------------------------*/
    /*Procedimiento para guardar un listado en un archivo txt
    Parametros de Entrada:
    - pid_convocatoria: El Id de convocatoria a la cual se le recalculará el puntaje
    Parametros de Salida:
    - pc_error: Código de error que indica el resultado de la operación.
        = 0: Éxito en la ejecución del procedimiento
    - pm_error: Mensaje de error en caso de que ocurra algún problema o null en caso de éxito.
    */
    PROCEDURE PR_GUARDAR_LISTADO(
        pid_convocatoria IN convocatoria.id_convocatoria%TYPE,
        pc_error OUT NUMBER,
        pm_error OUT VARCHAR
    );

END PK_PUBLICACION;
