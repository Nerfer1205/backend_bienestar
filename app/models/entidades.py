import inspect

class Entidad:

    def __init__(self,id,list_no,id_txt):
        self.id = id
        self.no_attr = list_no
        self.id_txt = id_txt

    def get_attrs(self):
        atrrs= []
        values = []

        for i in inspect.getmembers(self):
            # to remove private and protected
            # functions
            if not i[0].startswith('_'):
                # To remove other methods that
                # doesnot start with a underscore
                if not inspect.ismethod(i[1]):
                    if i[0] not in self.no_attr:
                        atrrs.append(i[0])
                        values.append(i[1])
        return tuple(atrrs), tuple(values)
    
    def get_name_class(self):
        return type(self).__name__

    def __str__(self):
        c,v = self.get_attrs()
        zipped = zip(c,v)
        m =" ".join(f"{attr} : {str(value)}, \n" for attr,value in zipped)
        return '{ \n id : '+str(self.id)+', \n '+m+'}'

class TIPO_SUBSIDIO(Entidad):
    def __init__(self, NOMBRE = '', POR_COBERTURA = '', HRS_DEDICACION_X_SEM = 0 , id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","id_txt"], '')
            self.ID_TIPO_SUBSIDIO = id
        else:
            super().__init__(0,["no_attr","id","id_txt"], '')
            self.ID_TIPO_SUBSIDIO = id
        
        self.NOMBRE = NOMBRE
        self.POR_COBERTURA = POR_COBERTURA
        self.HRS_DEDICACION_X_SEM = HRS_DEDICACION_X_SEM

#otra compuesta
class CONVOCATORIA_TIPO_SUBSIDIO(Entidad):
    def __init__(self, FK_ID_CONVOCATORIA = '', FK_ID_TIPO_SUBSIDIO = '', CANTIDAD = 0):
        super().__init__(0,["no_attr","id","id_txt"], '')
        self.FK_ID_CONVOCATORIA = FK_ID_CONVOCATORIA
        self.FK_ID_TIPO_SUBSIDIO = FK_ID_TIPO_SUBSIDIO
        self.CANTIDAD = CANTIDAD



class CONVOCATORIA(Entidad):
    def __init__(self, FECHA_I_CONV = None, FECHA_I_INSC = None, FECHA_I_VERIF = None, FECHA_I_PUBL = None, FECHA_I_CUMP = None, FECHA_F_CUMP = None, PERIODO = '', ESTADO='', VALOR_X_ALMUERZO=0, id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","id_txt"], 'ID_CONVOCATORIA')
            self.ID_CONVOCATORIA = id
        else:
            super().__init__(0,["no_attr","id","id_txt"], 'ID_CONVOCATORIA')
            self.ID_CONVOCATORIA = id
        self.FECHA_I_CONV = FECHA_I_CONV
        self.FECHA_I_INSC = FECHA_I_INSC
        self.FECHA_I_VERIF = FECHA_I_VERIF
        self.FECHA_I_PUBL = FECHA_I_PUBL
        self.FECHA_I_CUMP = FECHA_I_CUMP
        self.FECHA_F_CUMP = FECHA_F_CUMP
        self.PERIODO = PERIODO
        self.ESTADO = ESTADO
        self.VALOR_X_ALMUERZO = VALOR_X_ALMUERZO

# no se q hacer con la compuesta
class CONVOCATORIA_TIPO(Entidad):
    def __init__(self, FK_ID_CONVOCATORIA = '', FK_ID_TIPO=''):
        super().__init__(0,["no_attr","id","id_txt"], '')
        self.FK_ID_CONVOCATORIA = FK_ID_CONVOCATORIA
        self.FK_ID_TIPO = FK_ID_TIPO
        

class TIPO(Entidad):
    def __init__(self, NOMBRE = '', PUNTAJE_MAX=0, id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","id_txt"], '')
            self.ID_TIPO = id
        else:
            super().__init__(0,["no_attr","id","id_txt"], '')
            self.ID_TIPO = id
        
        self.NOMBRE = NOMBRE
        self.PUNTAJE_MAX = PUNTAJE_MAX

class CONDICION(Entidad):
    def __init__(self, NOMBRE = '', PUNTAJE=0, FK_ID_TIPO = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","ID_CONDICION","id","id_txt"], 'ID_CONDICION')
            self.ID_CONDICION = id
        else:
            super().__init__(0,["no_attr","ID_CONDICION","id","id_txt"], 'ID_CONDICION')
            self.ID_CONDICION = id
        
        self.NOMBRE = NOMBRE
        self.PUNTAJE = PUNTAJE
        self.FK_ID_TIPO = FK_ID_TIPO

#otra compuesta
class DOCUMENTO(Entidad):
    def __init__(self, RUTA = '', ESTADO = '', PUNTAJE_OBTENIDO = 0, OBSERVACION = '', FK_ID_CONDICION = None, FK_ID_SOLICITUD = None, id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","id_txt"], '')
            self.ID_DOCUMENTO = id
        else:
            super().__init__(0,["no_attr","id","id_txt"], '')
            self.ID_DOCUMENTO = id
        
        self.RUTA = RUTA
        self.ESTADO = ESTADO
        self.PUNTAJE_OBTENIDO = PUNTAJE_OBTENIDO
        self.OBSERVACION = OBSERVACION
        self.FK_ID_CONDICION = FK_ID_CONDICION
        self.FK_ID_SOLICITUD = FK_ID_SOLICITUD

class SOLICITUD(Entidad):
    def __init__(self, FECHA_CREACION = None, ESTADO = None, PUNTAJE_TOTAL = None, MOTIVO_RECHAZO = None, FK_CODIGO = None, FK_ID_CONVOCATORIA = None, FK_RESPONSABLE_VERIFICAR = None, id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","ID_SOLICITUD","FECHA_CREACION", "ESTADO" ,"id_txt"], 'ID_SOLICITUD')
            self.ID_SOLICITUD = id
        else:
            super().__init__(0,["no_attr","id","ID_SOLICITUD","FECHA_CREACION", "ESTADO" ,"id_txt"], 'ID_SOLICITUD')
            self.ID_SOLICITUD = id
        
        self.FECHA_CREACION = FECHA_CREACION
        self.ESTADO = ESTADO
        self.PUNTAJE_TOTAL = PUNTAJE_TOTAL
        self.MOTIVO_RECHAZO = MOTIVO_RECHAZO
        self.FK_CODIGO = FK_CODIGO
        self.FK_ID_CONVOCATORIA = FK_ID_CONVOCATORIA
        self.FK_RESPONSABLE_VERIFICAR = FK_RESPONSABLE_VERIFICAR

class ESTUDIANTE(Entidad):
    def __init__(self, PROYECTO = '', SEMESTRE = '', TIPO_DOCUMENTO = '' , DOCUMENTO = '', NOMBRES = '', APELLIDOS = '', CORREO = '', DIRECCION = '', MUNICIPIO = '', COSTO_SEM = None , INGRESOS = None, PROMEDIO_PONDERADO = None, ASIG_PERDIDAS_SEM_PASADO = 0, NUM_CREDITOS = 0, ESTADO = '', USUARIO = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","CODIGO","id_txt"], 'CODIGO')
            self.CODIGO = id
        else:
            super().__init__(0,["no_attr","id","CODIGO","id_txt"], 'CODIGO')
            self.CODIGO = id
        
        self.PROYECTO = PROYECTO
        self.SEMESTRE = SEMESTRE
        self.TIPO_DOCUMENTO = TIPO_DOCUMENTO
        self.DOCUMENTO = DOCUMENTO
        self.NOMBRES = NOMBRES
        self.APELLIDOS = APELLIDOS
        self.CORREO = CORREO
        self.DIRECCION = DIRECCION
        self.MUNICIPIO = MUNICIPIO
        self.COSTO_SEM = COSTO_SEM
        self.INGRESOS = INGRESOS
        self.PROMEDIO_PONDERADO = PROMEDIO_PONDERADO
        self.ASIG_PERDIDAS_SEM_PASADO = ASIG_PERDIDAS_SEM_PASADO
        self.NUM_CREDITOS = NUM_CREDITOS
        self.ESTADO = ESTADO
        self.USUARIO = USUARIO

class SOLICITUD_APROBADA(Entidad):
    def __init__(self, FECHA_APROBACION = None, ESTADO = '', MOTIVO_FINALIZACION = '', FK_ID_SOLICITUD = '', FK_ID_TIPO_SUBSIDIO = '', FK_RESPONSABLE_APROBAR = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","ID_APROBACION","id_txt"], 'ID_APROBACION')
            self.ID_APROBACION = id
        else:
            super().__init__(0,["no_attr","id","ID_APROBACION","id_txt"], 'ID_APROBACION')
            self.ID_APROBACION = id
        
        self.FECHA_APROBACION = FECHA_APROBACION
        self.ESTADO = ESTADO
        self.MOTIVO_FINALIZACION = MOTIVO_FINALIZACION
        self.FK_ID_SOLICITUD = FK_ID_SOLICITUD
        self.FK_ID_TIPO_SUBSIDIO = FK_ID_TIPO_SUBSIDIO
        self.FK_RESPONSABLE_APROBAR = FK_RESPONSABLE_APROBAR

class RESPONSABLE(Entidad):
    def __init__(self, TIPO_DOCUMENTO = '', NOMBRES = '', APELLIDOS = '', TELEFONO = '', DIRECCION = '', USUARIO = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","DOCUMENTO","id_txt"], 'DOCUMENTO')
            self.DOCUMENTO = id
        else:
            super().__init__(0,["no_attr","id","DOCUMENTO","id_txt"], 'DOCUMENTO')
            self.DOCUMENTO = id
        
        self.TIPO_DOCUMENTO = TIPO_DOCUMENTO
        self.NOMBRES = NOMBRES
        self.APELLIDOS = APELLIDOS
        self.TELEFONO = TELEFONO
        self.DIRECCION = DIRECCION
        self.USUARIO = USUARIO

class TIQUETERA(Entidad):
    def __init__(self, FECHA_I_VIGENCIA = None, FECHA_F_VIGENCIA = None, ESTADO = '', FK_ID_APROBACION = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        else:
            super().__init__(0,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        
        self.FECHA_I_VIGENCIA = FECHA_I_VIGENCIA
        self.FECHA_F_VIGENCIA = FECHA_F_VIGENCIA
        self.ESTADO = ESTADO
        self.FK_ID_APROBACION = FK_ID_APROBACION

#otra compuesta
class TICKET(Entidad):
    def __init__(self, CODIGO = '', CODIGO_TIQUETERA = '', FECHA = None, RECLAMADO = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        else:
            super().__init__(0,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        
        self.FECHA = FECHA
        self.RECLAMADO = RECLAMADO

#otra compuesta
class SOLICITUD_APROBADA_ACTIVIDAD_DE_APOYO(Entidad):
    def __init__(self, FK_ID_ACTIVIDAD = '', FK_ID_APROBACION = '', HRS_ASISTENCIA = 0, id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        else:
            super().__init__(0,["no_attr","id","CODIGO_TIQUETERA","id_txt"], 'CODIGO_TIQUETERA')
            self.CODIGO_TIQUETERA = id
        
        self.HRS_ASISTENCIA = HRS_ASISTENCIA

class ACTIVIDAD_DE_APOYO(Entidad):
    def __init__(self, DESCRIPCION = '', FECHA = None, FK_RESPONSABLE_SUPERVISAR = '', id = None ):
        
        if id is not None:
            super().__init__(id,["no_attr","id","ID_ACTIVIDAD","id_txt"], 'ID_ACTIVIDAD')
            self.ID_ACTIVIDAD = id
        else:
            super().__init__(0,["no_attr","id","ID_ACTIVIDAD","id_txt"], 'ID_ACTIVIDAD')
            self.ID_ACTIVIDAD = id
        
        self.DESCRIPCION = DESCRIPCION
        self.FECHA = FECHA
        self.FK_RESPONSABLE_SUPERVISAR = FK_RESPONSABLE_SUPERVISAR


