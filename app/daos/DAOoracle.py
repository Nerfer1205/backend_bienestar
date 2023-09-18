import oracledb
from flask import current_app
from app.daos import DAOgen
from app.models.entidades import ESTUDIANTES

class DAOgenericoOracle(DAOgen.DAOGenerico):
    def __init__(self):
        self.__conexion = None
        self.cursor = None
        self.__esquema = 'BIENESTAR'
        oracledb.init_oracle_client(current_app.config['LIB_DIR'])
    
    def conectar(self):
        try:
            self.__conexion = oracledb.connect(
                user=current_app.config['ORACLE_USER'],
                password=current_app.config['ORACLE_PASS'], 
                dsn=current_app.config['ORACLE_DSN']
            )
            self.cursor = self.__conexion.cursor()
            return True
        except oracledb.Error as error:
            return error

    def create(self, entity):
        self.conectar()
        try:
            columns, values = entity.get_attrs()
            columns_str = ", ".join(columns)
            placeholders_str = ", ".join(":" + column for column in columns)
            sql = f"INSERT INTO {self.__esquema}.{entity.get_name_class()} ({columns_str}) VALUES ({placeholders_str})"
            self.cursor.execute(sql, values)
            self.__conexion.commit()
            id_generada = self.cursor.getlastrowid()
            setattr(entity, entity.id_txt, id_generada)
            entity.id = id_generada
        except oracledb.Error as error:
            return error

    def delete(self, entity):
        self.conectar()
        try:
            sql = f"DELETE FROM {self.__esquema}.{entity.get_name_class()} WHERE {entity.id_txt} = :id"
            values = [entity.id] 
            self.cursor.execute(sql, values)
            if self.cursor.rowcount > 0:
                entity = None
        except oracledb.Error as error:
            return error

    def findall(self, entity):
        self.conectar()
        try:
            sql = f"SELECT * FROM {self.__esquema}.{entity.get_name_class()}"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            results = [res[1:] + (res[0],) for res in results]
            ent_type = globals()[entity.get_name_class()]
            entities = [ent_type(*res) for res in results]
            return entities
        except oracledb.Error as error:
            return error

        
    def read(self, entity):
        self.conectar()
        try:
            sql = f"SELECT * FROM {self.__esquema}.{entity.get_name_class()} WHERE {entity.id_txt} = :val"
            values = {"val":entity.id}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            ent_type = globals()[entity.get_name_class()]
            entity = ent_type(*res) 
            return entity

        except oracledb.Error as error:
            return error

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

class DBA_USERS_DAO_ORACLE(DAOgenericoOracle, DAOgen.DBA_USERS_DAO):
    def crear_usuario(self, usuario, contrasena):
        self.conectar()
        try:
            # No se pasan bind variables debido al siguiente error: DPI-1059: bind variables are not supported in DDL statements
            sql = f'''CREATE USER {usuario} IDENTIFIED BY {contrasena} DEFAULT TABLESPACE BRYDEF TEMPORARY TABLESPACE BRYTMP QUOTA 2M ON BRYDEF'''
            self.cursor.execute(sql)   
            sql = f"GRANT R_ESTUDIANTE TO {usuario}"
            self.cursor.execute(sql)  
            return True
        except oracledb.Error as error:
            return error
