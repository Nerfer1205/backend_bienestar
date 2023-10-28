import oracledb
from flask import current_app
from app.daos import DAOgen
from app.models.entidades import ESTUDIANTE, CONVOCATORIA, TIPO, CONDICION, SOLICITUD, TIPO_SUBSIDIO, TIPO

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
            placeholder_list = []
            for column in columns:
                if 'FECHA' in column:
                    placeholder_list.append(f"TO_DATE(:{column}, 'YYYY-MM-DD')")
                else:
                    placeholder_list.append(f":{column}")
            placeholders_str = ", ".join(placeholder_list)
            sql = f"INSERT INTO {self.esquema}.{entity.get_name_class()} ({columns_str}) VALUES ({placeholders_str})"
            
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
        
    def update(self, entity, where = ''):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            columns, values = entity.get_attrs()

            placeholder_list = []
            n_values = []
            for index_c,column in enumerate(columns):
                if values[index_c] != '' and values[index_c] != None:
                    if 'FECHA' in column:
                        placeholder_list.append(f"{column} = TO_DATE(:{column}, 'YYYY-MM-DD')")
                    else:
                        placeholder_list.append(f"column = :{column}")
                    n_values.append(values[index_c])
            
            set_clause = ", ".join(placeholder_list)
            where_clause = where
            if entity.id_txt != '':
                where_clause = f'{entity.id_txt} = :{entity.id_txt}'

            sql = f"UPDATE {self.esquema}.{entity.get_name_class()} SET {set_clause} WHERE {where_clause}"
            query_values = [*n_values, entity.id]            
            self.cursor.execute(sql, query_values)
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        except oracledb.Error as error:
            return error

class TIPO_SUBSIDIO_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIPO_SUBSIDIO_DAO):
    pass

class CONVOCATORIA_TIPO_SUBSIDIO_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_TIPO_SUBSIDIO_DAO):
    pass

class CONVOCATORIA_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_DAO):
    pass

class CONVOCATORIA_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONVOCATORIA_DAO):
    def obtener_ultima(self, estado):
        
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.CONVOCATORIA WHERE ESTADO = :estado ORDER BY ID_CONVOCATORIA DESC"
            values = {"estado": estado}
            self.cursor.execute(sql,values)   
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
    def recalcular_maximo_puntaje(self, id_tipo):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"UPDATE {self.esquema}.TIPO SET PUNTAJE_MAX = (SELECT MAX(PUNTAJE) FROM {self.esquema}.CONDICION WHERE FK_ID_TIPO = :id_tipo1) WHERE ID_TIPO = :id_tipo2"
            values = {"id_tipo1": id_tipo, "id_tipo2": id_tipo}
            self.cursor.execute(sql,values)   
            self.conexion.commit()
            return True
        except oracledb.Error as error:
            return error


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

class CONDICION_DAO_ORACLE(DAOgenericoOracle, DAOgen.CONDICION_DAO):
    def condiciones_x_tipo(self, id_tipo):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.CONDICION WHERE FK_ID_TIPO = :id_tipo"
            values = {"id_tipo": id_tipo}
            self.cursor.execute(sql,values)   
            res = self.cursor.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [CONDICION(*r) for r in res]
        except oracledb.Error as error:
            return error

class DOCUMENTO_DAO_ORACLE(DAOgenericoOracle, DAOgen.DOCUMENTO_DAO):
    def actualizar_estado_documento(self, id_solicitud, id_documento, estado, puntaje, observacion):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"UPDATE {self.esquema}.DOCUMENTO SET ESTADO = :estado, PUNTAJE_OBTENIDO = :puntaje, OBSERVACION = :observacion WHERE FK_ID_SOLICITUD = :id_solicitud AND ID_DOCUMENTO = :id_documento"
            values = {"estado" : estado, "puntaje":puntaje, "observacion" : observacion,"id_documento" : id_documento, "id_solicitud" : id_solicitud, }
            self.cursor.execute(sql, values)   
            self.conexion.commit()
            return True
        except oracledb.Error as error:
            return error  
        
        
    def documentos_tipo_condicion_x_solicitud(self,id_convocatoria, id_solicitud):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f'''SELECT t.NOMBRE, c.NOMBRE, d.ESTADO, d.RUTA, d.ID_DOCUMENTO, c.PUNTAJE FROM {self.esquema}.DOCUMENTO d
                        JOIN {self.esquema}.CONDICION c ON c.ID_CONDICION = d.FK_ID_CONDICION
                        JOIN {self.esquema}.TIPO t ON t.ID_TIPO = c.FK_ID_TIPO
                        JOIN {self.esquema}.SOLICITUD s ON s.ID_SOLICITUD = d.FK_ID_SOLICITUD
                        WHERE d.FK_ID_SOLICITUD = :FK_ID_SOLICITUD and
                        s.FK_ID_CONVOCATORIA = :id_convocatoria
                        '''
            values = {"FK_ID_SOLICITUD" : id_solicitud, "id_convocatoria" : id_convocatoria}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchall()
            return res
        except oracledb.Error as error:
            return error        

class SOLICITUD_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUD_DAO):
    def actualizar_estado(self, id_solicitud, estado, motivo = None):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"UPDATE {self.esquema}.SOLICITUD SET ESTADO = :estado, MOTIVO_RECHAZO = :motivo WHERE ID_SOLICITUD = :id_solicitud"
            values = {"estado" : estado, "motivo" : motivo,"id_solicitud" : id_solicitud}
            self.cursor.execute(sql, values)  
            self.conexion.commit() 
            return True
        except oracledb.Error as error:
            return error  

    def solicitud_x_estu_x_conv(self, FK_CODIGO, FK_ID_CONVOCATORIA):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f"SELECT * FROM {self.esquema}.SOLICITUD WHERE FK_CODIGO = :FK_CODIGO AND FK_ID_CONVOCATORIA = :FK_ID_CONVOCATORIA"
            values = {"FK_CODIGO": FK_CODIGO,"FK_ID_CONVOCATORIA" : FK_ID_CONVOCATORIA}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return SOLICITUD(*res)
        except oracledb.Error as error:
            return error
        
    def solicitud_x_convocatoria(self,FK_ID_CONVOCATORIA):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f'''SELECT s.ID_SOLICITUD, s.ESTADO, e.NOMBRES, e.APELLIDOS FROM {self.esquema}.SOLICITUD s, 
                        {self.esquema}.ESTUDIANTE e
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
    
    def solicitudes_aprobadas_x_convocatoria(self,FK_ID_CONVOCATORIA):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            sql = f'''SELECT s.id_solicitud, s.puntaje_total, e.nombres, e.apellidos, e.correo, ts.nombre FROM solicitudes s, estudiantes e, solicitudes_aprobadas sa, tipo_subsidio ts WHERE 
                            s.estado IN('APROBADO') AND
                            e.codigo = s.fk_codigo AND
                            sa.fk_id_solicitud = s.id_solicitud AND
                            sa.fk_id_tipo_subsidio = ts.id_tipo_subsidio AND
                            s.fk_id_convocatoria = :FK_ID_CONVOCATORIA
                            ORDER BY s.puntaje_total DESC, e.promedio_ponderado DESC, e.asig_perdidas_sem_pasado ASC, e.ingresos ASC
                        '''
            print(sql, FK_ID_CONVOCATORIA)
            values = {"FK_ID_CONVOCATORIA" : FK_ID_CONVOCATORIA}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchall()
            return res
        except oracledb.Error as error:
            return error

class ESTUDIANTE_DAO_ORACLE(DAOgenericoOracle, DAOgen.ESTUDIANTE_DAO):
    
    def actualizar_usuario(self, usuario, codigo):
        try:
            sql = f"UPDATE {self.esquema}.ESTUDIANTE SET USUARIO = :USUARIO WHERE CODIGO = :CODIGO"
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
            sql = f"SELECT * FROM {self.esquema}.ESTUDIANTE WHERE USUARIO = :usuario"
            values = {"usuario" : current_app.config['ORACLE_USER']}
            self.cursor.execute(sql, values)   
            res = self.cursor.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return ESTUDIANTE(*res)
        except oracledb.Error as error:
            return error

class SOLICITUD_APROBADA_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUD_APROBADA_DAO):
    pass

class RESPONSABLE_DAO_ORACLE(DAOgenericoOracle, DAOgen.RESPONSABLE_DAO):
    pass

class TIQUETERA_DAO_ORACLE(DAOgenericoOracle, DAOgen.TIQUETERA_DAO):
    pass

class TICKET_DAO_ORACLE(DAOgenericoOracle, DAOgen.TICKET_DAO):
    pass

class SOLICITUD_APROBADA_ACTIVIDAD_DE_APOYO_DAO_ORACLE(DAOgenericoOracle, DAOgen.SOLICITUD_APROBADA_ACTIVIDAD_DE_APOYO_DAO):
    pass

class ACTIVIDAD_DE_APOYO_DAO_ORACLE(DAOgenericoOracle, DAOgen.ACTIVIDAD_DE_APOYO_DAO):
    pass

class DBA_USERS_DAO_ORACLE(DAOgenericoOracle, DAOgen.DBA_USERS_DAO):
    def crear_usuario(self, usuario, contrasena):
        conecto = self.conectar()
        if isinstance(conecto, oracledb.Error):
            return conecto
        try:
            # No se pasan bind variables debido al siguiente error: DPI-1059: bind variables are not supported in DDL statements
            sql = f'''CREATE USER {usuario} IDENTIFIED BY {contrasena} DEFAULT TABLESPACE APOYODEF TEMPORARY TABLESPACE APOYOTEMP1 QUOTA 2M ON APOYODEF'''
            self.cursor.execute(sql)   
            sql = f"GRANT R_ESTUDIANTE TO {usuario}"
            self.cursor.execute(sql)  
            return True
        except oracledb.Error as error:
            return error
