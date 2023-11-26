-- Creación de un directorio llamado "DIRECTORIO_DE_ARCHIVOS" en la base de datos
CREATE DIRECTORY DIRECTORIO_DE_ARCHIVOS AS 'archivosPLSQL';

-- Otorgar permisos de lectura y escritura en el directorio "DIRECTORIO_DE_ARCHIVOS" al usuario "BIENESTAR"
GRANT READ, WRITE ON DIRECTORY DIRECTORIO_DE_ARCHIVOS TO BIENESTAR;

