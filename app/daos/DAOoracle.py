import oracledb
from flask import current_app
from app.daos import DAOgen

class DAOgenericoOracle:
    def __init__(self):
        oracledb.init_oracle_client(current_app.config['LIB_DIR'])
        self.conexion = oracledb.connect(
            user=current_app.config['ORACLE_USER'],
            password=current_app.config['ORACLE_PASS'], 
            dsn=current_app.config['ORACLE_DSN']
        )
        self.cursor = self.conexion.cursor()

    def create(self, entity):
        try:
            columns, values = entity.get_attrs()
            columns_str = ", ".join(columns)
            placeholders_str = ", ".join(":" + column for column in columns)
            sql = f"INSERT INTO {entity.get_name_class()} ({columns_str}) VALUES ({placeholders_str})"
            self.cursor.execute(sql, values)
            self.conexion.commit()
            id_generada = self.cursor.getlastrowid()
            setattr(entity, entity.id_txt, id_generada)
            entity.id = id_generada
        except oracledb.Error as error:
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def delete(self, entity):
        try:
            sql = f"DELETE FROM {entity.get_name_class()} WHERE {entity.id_txt} = :id"
            values = [entity.id] 
            self.cursor.execute(sql, values)
            if self.cursor.rowcount > 0:
                entity = None
        except oracledb.Error as error:
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def findall(self, entity):
        try:
            sql = f"SELECT * FROM {entity.get_name_class()}"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            results = [res[1:] + (res[0],) for res in results]
            ent_type = globals()[entity.get_name_class()]
            entities = [ent_type(*res) for res in results]
            return entities
        except oracledb.Error as error:
            print("Se produjo un error durante la ejecución de la consulta:", error)

class TIPO_SUBSIDIO_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIPO_SUBSIDIO_DAO):
    pass

class CONVOCATORIA_TIPO_SUBSIDIO_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_TIPO_SUBSIDIO_DAO):
    pass

class CONVOCATORIA_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_DAO):
    pass

class CONVOCATORIA_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_DAO):
    pass

class CONVOCATORIA_TIPO_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_TIPO_DAO):
    pass

class TIPO_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIPO_DAO):
    pass

class CONDICIONES_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONDICIONES_DAO):
    pass

class DOCUMENTOS_DAO_ORACLE(DAOgenericoOracle, DAOgen.DOCUMENTOS_DAO):
    pass

class SOLICITUDES_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUDES_DAO):
    pass

class ESTUDIANTES_DAO_ORACLE(DAOgenericoOracle, DAOgen.ESTUDIANTES_DAO):
    pass

class SOLICITUDES_APROBADAS_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUDES_APROBADAS_DAO):
    pass

class RESPONSABLE_DAO_ORACLE(DAOgenericoOracle, DAOgen.RESPONSABLE_DAO):
    pass

class TIQUETERA_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIQUETERA_DAO):
    pass

class TICKET_DAO_ORACLE(DAOgenericoOracle, DAOgen.TICKET_DAO):
    pass

class SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO_DAO):
    pass

class ACTIVIDADES_DE_APOYO_DAO_ORACLE(DAOgenericoOracle, DAOgen.ACTIVIDADES_DE_APOYO_DAO):
    pass