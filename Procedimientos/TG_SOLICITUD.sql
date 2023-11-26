-- Trigger que se dispara después de una actualización en la tabla 'solicitud' en las columnas 'puntaje_total' y 'estado'
CREATE OR REPLACE TRIGGER TG_SOLICITUD
AFTER UPDATE OF puntaje_total, estado ON solicitud
FOR EACH ROW
BEGIN
    -- Verifica si los valores de 'puntaje_total' o 'estado' han cambiado
    IF :new.puntaje_total != :old.puntaje_total OR :new.estado != :old.estado THEN
        -- Inserta una entrada en la tabla 'AUDITORIA_SOLICITUD' para auditar los cambios
        INSERT INTO AUDITORIA_SOLICITUD VALUES(NULL, :old.puntaje_total, :new.puntaje_total, :old.estado, :new.estado, SYSDATE, USER, :new.id_solicitud);
    END IF;
END TG_SOLICITUD;
/
