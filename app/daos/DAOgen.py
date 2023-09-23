from abc import ABC, abstractmethod
class DAOGenerico(ABC):
    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def findall(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

class TIPO_SUBSIDIO_DAO(DAOGenerico):
    pass

class CONVOCATORIA_TIPO_SUBSIDIO_DAO(DAOGenerico):
    pass

class CONVOCATORIA_DAO(DAOGenerico):
    @abstractmethod
    def obtener_ultima(self):
        pass


class CONVOCATORIA_TIPO_DAO(DAOGenerico):
    pass

class TIPO_DAO(DAOGenerico):
    @abstractmethod
    def recalcular_maximo_puntaje(self, id_tipo):
        pass
    @abstractmethod
    def tipos_x_convocatoria(self, id_convocatoria):
        pass

class CONDICIONES_DAO(DAOGenerico):
    pass

class DOCUMENTOS_DAO(DAOGenerico):
    @abstractmethod
    def documentos_tipo_condicion_x_solicitud(self, id_solicitud):
        pass

    @abstractmethod
    def actualizar_estado_documento(self, id_solicitud, id_documento, estado):
        pass
    

class SOLICITUDES_DAO(DAOGenerico):
    @abstractmethod
    def actualizar_estado(self, id_solicitud, estado):
        pass
    @abstractmethod
    def solicitud_x_estu_x_conv(self, FK_CODIGO, FK_ID_CONVOCATORIA):
        pass
    @abstractmethod
    def solicitud_x_convocatoria(self,FK_ID_CONVOCATORIA):
        pass

class ESTUDIANTES_DAO(DAOGenerico):
    @abstractmethod
    def actualizar_usuario(self, usuario, codigo):
        pass
    
    @abstractmethod
    def estudiante_x_usuario(self):
        pass

class SOLICITUDES_APROBADAS_DAO(DAOGenerico):
    pass

class RESPONSABLE_DAO(DAOGenerico):
    pass

class TIQUETERA_DAO(DAOGenerico):
    pass

class TICKET_DAO(DAOGenerico):
    pass

class SOLICITUDES_APROBADAS_ACTIVIDADES_DE_APOYO_DAO(DAOGenerico):
    pass

class ACTIVIDADES_DE_APOYO_DAO(DAOGenerico):
    pass

class DBA_USERS_DAO(DAOGenerico):
    @abstractmethod
    def crear_usuario(self,usuario, contrasena):
        pass

