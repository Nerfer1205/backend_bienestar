import oracledb
from flask import current_app
from app.daos import DAOgen
from app.models.entidades import ESTUDIANTES, CONVOCATORIA, TIPO, CONDICIONES, SOLICITUDES, TIPO_SUBSIDIO, TIPO

class DAOgenericoOracle(DAOgen.DAOGenerico):
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.esquema = 'BIENESTAR'
        oracledb.init_oracle_client(current_app.config['LIB_DIR'])
    
    def conectar(self):
        try:
            self.conexion = oracledb.connect(
                user=current_app.config['ORACLE_USER'],
                password=current_app.config['ORACLE_PASS'], 
                dsn=current_app.config['ORACLE_DSN']
            )
            self.cursor = self.conexion.cursor()
            return True
        except oracledb.Error as error:
            return error

    def create(self, entity):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            columns, values = entity.get_attrs()
            columns_str = ", ".join(columns)
            placeholders_str = ", ".join(":" + column for column in columns)
            sql = f"INSERT INTO {self.esquema}.{entity.get_name_class()} ({columns_str}) VALUES ({placeholders_str})"
            print(sql, values)
            self.cursor.execute(sql, values)
            if(entity.id_txt != ''):
                sql = f"SELECT max({entity.id_txt}) FROM {self.esquema}.{entity.get_name_class()}"
                self.cursor.execute(sql)
                res = self.cursor.fetchone()

                id_generada = res[0]
                setattr(entity, entity.id_txt, id_generada)
                entity.id = id_generada 
            self.conexion.commit()
              
            return True
        except oracledb.Error as error:
            return error

    def delete(self, entity):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"DELETE FROM {self.esquema}.{entity.get_name_class()} WHERE {entity.id_txt} = :id"
            values = [entity.id] 
            self.cursor.execute(sql, values)
            if self.cursor.rowcount > 0:
                entity = None
        except oracledb.Error as error:
            return error

    def findall(self, entity):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.{entity.get_name_class()}"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            results = [res[1:] + (res[0],) for res in results]
            ent_type = globals()[entity.get_name_class()]
            entities = [ent_type(*res) for res in results]
            return entities
        except oracledb.Error as error:
            return error

        
    def read(self, entity):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.{entity.get_name_class()} WHERE {entity.id_txt} = :val"
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
    def obtener_ultima(self):
        
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.CONVOCATORIA ORDER BY ID_CONVOCATORIA DESC"
            self.cursor.execute(sql)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return CONVOCATORIA(*res)
        except oracledb.Error as error:
            return error

class CONVOCATORIA_TIPO_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_TIPO_DAO):
    pass

class TIPO_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIPO_DAO):
    def tipos_x_convocatoria(self, id_convocatoria):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT t.* FROM {self.esquema}.TIPO t,{self.esquema}.CONVOCATORIA_TIPO ct WHERE ct.FK_ID_CONVOCATORIA = :id_convocatoria AND ct.FK_ID_TIPO = t.ID_TIPO"
            values = {"id_convocatoria": id_convocatoria}
            self.cursor.execute(sql,values)   
            res = self.cursor.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [TIPO(*r) for r in res]
        except oracledb.Error as error:
            return error

class CONDICIONES_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONDICIONES_DAO):
    def condiciones_x_tipo(self, id_tipo):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.CONDICIONES WHERE FK_ID_TIPO = :id_tipo"
            values = {"id_tipo": id_tipo}
            self.cursor.execute(sql,values)   
            res = self.cursor.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [CONDICIONES(*r) for r in res]
        except oracledb.Error as error:
            return error

class DOCUMENTOS_DAO_ORACLE(DAOgenericoOracle, DAOgen.DOCUMENTOS_DAO):
    def actualizar_estado_documento(self, id_solicitud, id_documento, estado):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"UPDATE {self.esquema}.DOCUMENTOS SET ESTADO = :estado WHERE FK_ID_SOLICITUD = :id_solicitud AND ID_DOCUMENTO = :id_documento"
            values = {"estado" : estado, "id_documento" : id_documento, "id_solicitud" : id_solicitud}
            self.cursor.execute(sql, values)   
            return True
        except oracledb.Error as error:
            return error  
        
        
    def documentos_tipo_condicion_x_solicitud(self, id_solicitud):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f'''SELECT t.NOMBRE, c.NOMBRE, d.ESTADO, d.RUTA, d.ID_DOCUMENTO FROM {self.esquema}.DOCUMENTOS d
                        JOIN {self.esquema}.CONDICIONES c ON c.ID_CONDICION = d.FK_ID_CONDICION
                        JOIN {self.esquema}.TIPO t ON t.ID_TIPO = c.FK_ID_TIPO
                        WHERE d.FK_ID_SOLICITUD = :FK_ID_SOLICITUD
                        '''
            values = {"FK_ID_SOLICITUD" : id_solicitud}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchall()
            return res
        except oracledb.Error as error:
            return error        

class SOLICITUDES_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUDES_DAO):
    def actualizar_estado(self, id_solicitud, estado):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"UPDATE {self.esquema}.SOLICITUDES SET ESTADO = :estado WHERE ID_SOLICITUD = :id_solicitud"
            values = {"estado" : estado, "id_solicitud" : id_solicitud}
            self.cursor.execute(sql, values)   
            return True
        except oracledb.Error as error:
            return error  

    def solicitud_x_estu_x_conv(self, FK_CODIGO, FK_ID_CONVOCATORIA):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.SOLICITUDES WHERE FK_CODIGO = :FK_CODIGO AND FK_ID_CONVOCATORIA = :FK_ID_CONVOCATORIA"
            values = {"FK_CODIGO": FK_CODIGO,"FK_ID_CONVOCATORIA" : FK_ID_CONVOCATORIA}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return SOLICITUDES(*res)
        except oracledb.Error as error:
            return error
        
    def solicitud_x_convocatoria(self,FK_ID_CONVOCATORIA):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f'''SELECT s.ID_SOLICITUD, s.ESTADO, e.NOMBRES, e.APELLIDOS FROM {self.esquema}.SOLICITUDES s, 
                        {self.esquema}.ESTUDIANTES e
                        WHERE s.FK_ID_CONVOCATORIA = :FK_ID_CONVOCATORIA AND
                        e.CODIGO = s.FK_CODIGO
                        '''
            print(sql, FK_ID_CONVOCATORIA)
            values = {"FK_ID_CONVOCATORIA" : FK_ID_CONVOCATORIA}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchall()
            return res
        except oracledb.Error as error:
            return error

class ESTUDIANTES_DAO_ORACLE(DAOgenericoOracle, DAOgen.ESTUDIANTES_DAO):
    
    def actualizar_usuario(self, usuario, codigo):
        try:
            sql = f"UPDATE {self.esquema}.ESTUDIANTES SET USUARIO = :USUARIO WHERE CODIGO = :CODIGO"
            values = {"USUARIO" : usuario, "CODIGO" : codigo}
            self.cursor.execute(sql, values)   
            self.conexion.commit()
            return True
        except oracledb.Error as error:
            return error
        
    def estudiante_x_usuario(self):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.ESTUDIANTES WHERE USUARIO = :usuario"
            values = {"usuario" : current_app.config['ORACLE_USER']}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return ESTUDIANTES(*res)
        except oracledb.Error as error:
            return error

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
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            # No se pasan bind variables debido al siguiente error: DPI-1059: bind variables are not supported in DDL statements
            sql = f'''CREATE USER {usuario} IDENTIFIED BY {contrasena} DEFAULT TABLESPACE BRYDEF TEMPORARY TABLESPACE BRYTMP QUOTA 2M ON BRYDEF'''
            self.cursor.execute(sql)   
            sql = f"GRANT R_ESTUDIANTE TO {usuario}"
            self.cursor.execute(sql)  
            return True
        except oracledb.Error as error:
            return error
