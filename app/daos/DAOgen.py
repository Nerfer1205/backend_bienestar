from abc import ABC, abstractmethod
class DAOGenerico(ABC):
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
    pass

class CONVOCATORIA_TIPO_DAO(DAOGenerico):
    pass

class TIPO_DAO(DAOGenerico):
    pass

class CONDICIONES_DAO(DAOGenerico):
    pass

class DOCUMENTOS_DAO(DAOGenerico):
    pass

class SOLICITUDES_DAO(DAOGenerico):
    pass

class ESTUDIANTES_DAO(DAOGenerico):
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