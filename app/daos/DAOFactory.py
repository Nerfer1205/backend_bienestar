from flask import current_app
from app.daos.DAOoracle import (
    TIPO_SUBSIDIO_DAO_ORACLE,
    CONVOCATORIA_TIPO_SUBSIDIO_DAO_ORACLE,
    CONVOCATORIA_DAO_ORACLE,
    CONVOCATORIA_TIPO_DAO_ORACLE,
    TIPO_DAO_ORACLE,
    CONDICION_DAO_ORACLE,
    DOCUMENTO_DAO_ORACLE,
    SOLICITUD_DAO_ORACLE,
    ESTUDIANTE_DAO_ORACLE,
    SOLICITUD_APROBADA_DAO_ORACLE,
    RESPONSABLE_DAO_ORACLE,
    TIQUETERA_DAO_ORACLE,
    TICKET_DAO_ORACLE,
    SOLICITUD_APROBADA_ACTIVIDAD_DE_APOYO_DAO_ORACLE,
    ACTIVIDAD_DE_APOYO_DAO_ORACLE,
    DBA_USERS_DAO_ORACLE,
    PROCEDIMIENTOS
)


class DAOFactoryOracle:
    _instance = None
    _tipo_subsidio_dao = None
    _convocatoria_tipo_subsidio_dao = None
    _convocatoria_dao = None
    _convocatoria_tipo_dao = None
    _tipo_dao = None
    _condiciones_dao = None
    _documentos_dao = None
    _solicitudes_dao = None
    _estudiantes_dao = None
    _solicitudes_aprobadas_dao = None
    _responsable_dao = None
    _tiquetera_dao = None
    _ticket_dao = None
    _solicitudes_aprobadas_actividades_de_apoyo_dao = None
    _actividades_de_apoyo_dao = None
    _usuario_dao = None
    _procedimientos_dao = None

    @classmethod
    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super().__new__(self)
        return self._instance

    @classmethod
    def get_tipo_subsidio_dao(self):
        if not self._tipo_subsidio_dao:
            self._tipo_subsidio_dao = TIPO_SUBSIDIO_DAO_ORACLE()
        return self._tipo_subsidio_dao

    @classmethod
    def get_convocatoria_tipo_subsidio_dao(self):
        if not self._convocatoria_tipo_subsidio_dao:
            self._convocatoria_tipo_subsidio_dao = CONVOCATORIA_TIPO_SUBSIDIO_DAO_ORACLE()
        return self._convocatoria_tipo_subsidio_dao

    @classmethod
    def get_convocatoria_dao(self):
        if not self._convocatoria_dao:
            self._convocatoria_dao = CONVOCATORIA_DAO_ORACLE()
        return self._convocatoria_dao

    @classmethod
    def get_convocatoria_tipo_dao(self):
        if not self._convocatoria_tipo_dao:
            self._convocatoria_tipo_dao = CONVOCATORIA_TIPO_DAO_ORACLE()
        return self._convocatoria_tipo_dao

    @classmethod
    def get_tipo_dao(self):
        if not self._tipo_dao:
            self._tipo_dao = TIPO_DAO_ORACLE()
        return self._tipo_dao

    @classmethod
    def get_condiciones_dao(self):
        if not self._condiciones_dao:
            self._condiciones_dao = CONDICION_DAO_ORACLE()
        return self._condiciones_dao

    @classmethod
    def get_documentos_dao(self):
        if not self._documentos_dao:
            self._documentos_dao = DOCUMENTO_DAO_ORACLE()
        return self._documentos_dao

    @classmethod
    def get_solicitudes_dao(self):
        if not self._solicitudes_dao:
            self._solicitudes_dao = SOLICITUD_DAO_ORACLE()
        return self._solicitudes_dao

    @classmethod
    def get_estudiantes_dao(self):
        if not self._estudiantes_dao:
            self._estudiantes_dao = ESTUDIANTE_DAO_ORACLE()
        return self._estudiantes_dao

    @classmethod
    def get_solicitudes_aprobadas_dao(self):
        if not self._solicitudes_aprobadas_dao:
            self._solicitudes_aprobadas_dao = SOLICITUD_APROBADA_DAO_ORACLE()
        return self._solicitudes_aprobadas_dao

    @classmethod
    def get_responsable_dao(self):
        if not self._responsable_dao:
            self._responsable_dao = RESPONSABLE_DAO_ORACLE()
        return self._responsable_dao

    @classmethod
    def get_tiquetera_dao(self):
        if not self._tiquetera_dao:
            self._tiquetera_dao = TIQUETERA_DAO_ORACLE()
        return self._tiquetera_dao

    @classmethod
    def get_ticket_dao(self):
        if not self._ticket_dao:
            self._ticket_dao = TICKET_DAO_ORACLE()
        return self._ticket_dao

    @classmethod
    def get_solicitudes_aprobadas_actividades_de_apoyo_dao(self):
        if not self._solicitudes_aprobadas_actividades_de_apoyo_dao:
            self._solicitudes_aprobadas_actividades_de_apoyo_dao = SOLICITUD_APROBADA_ACTIVIDAD_DE_APOYO_DAO_ORACLE()
        return self._solicitudes_aprobadas_actividades_de_apoyo_dao

    @classmethod
    def get_actividades_de_apoyo_dao(self):
        if not self._actividades_de_apoyo_dao:
            self._actividades_de_apoyo_dao

    @classmethod
    def get_usuario_dao(self):
        if not self._usuario_dao:
            self._usuario_dao = DBA_USERS_DAO_ORACLE()
        return self._usuario_dao
    
    @classmethod
    def get_procedimientos_dao(self):
        if not self._procedimientos_dao:
            self._procedimientos_dao = PROCEDIMIENTOS()
        return self._procedimientos_dao
    
    