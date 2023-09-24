import os
from werkzeug.utils import secure_filename

from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required
from app.daos.DAOFactory import DAOFactoryOracle
from app.models.entidades import CONVOCATORIA, DOCUMENTOS, SOLICITUDES, TIPO_SUBSIDIO, TIPO, CONVOCATORIA_TIPO_SUBSIDIO, CONVOCATORIA_TIPO, CONDICIONES
from oracledb import Error
import datetime


ruta = 'http://127.0.0.1:5000/static/uploads/'

convocatoria_bp = Blueprint('convocatoria', __name__)

@convocatoria_bp.route('/ver-ultima/',methods=["GET"])
@token_required
def ver_ultima():
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().obtener_ultima()
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST
    if convocatoria is None:
        return jsonify({"success": False, "message" : "Aun no existen convocatorias"}) , HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "Convocatoria consultada con éxito!", "data": {
        "CONVOCATORIA" : {
            "ID_CONVOCATORIA": convocatoria.ID_CONVOCATORIA,
            "FECHA_I_INSC": dateToStr(convocatoria.FECHA_I_INSC),
            "FECHA_F_INSC": dateToStr(convocatoria.FECHA_I_VERIF),
            "ESTADO": convocatoria.ESTADO
        }
    }}) , HTTPStatus.OK

@convocatoria_bp.route('/ver-para-estudiante/<id_convocatoria>',methods=["GET"])
@token_required
def ver_para_estudiante(id_convocatoria):
    convocatoria = CONVOCATORIA(id=id_convocatoria)
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().read(convocatoria)
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST
    
    
    tipos_x_convocatoria = DAOFactoryOracle.get_tipo_dao().tipos_x_convocatoria(id_convocatoria)
    if isinstance(tipos_x_convocatoria, Error):
        return jsonify({"success": False, "message" : str(tipos_x_convocatoria)}) , HTTPStatus.BAD_REQUEST
    
    data = {"CONVOCATORIA" : {"ID_CONVOCATORIA": convocatoria.ID_CONVOCATORIA, "TIPOS": []}}
    for tipo in tipos_x_convocatoria:
        temp_condiciones = []        
        condiciones_x_tipo = DAOFactoryOracle.get_condiciones_dao().condiciones_x_tipo(tipo.ID_TIPO)
        if isinstance(condiciones_x_tipo, Error):
            return jsonify({"success": False, "message" : str(condiciones_x_tipo)}) , HTTPStatus.BAD_REQUEST
        for condicion in condiciones_x_tipo:
            temp_condiciones.append({
                "ID_CONDICION": condicion.ID_CONDICION,
                "NOMBRE": condicion.NOMBRE
            })

        data["CONVOCATORIA"]["TIPOS"].append({
            "ID_TIPO": tipo.ID_TIPO,
            "NOMBRE": tipo.NOMBRE,
            "CONDICIONES" : temp_condiciones
        })

    return jsonify({"success": True, "message" : "Convocatoria consultada con éxito!", "data": data}) , HTTPStatus.OK



@convocatoria_bp.route('/inscribirme',methods=["POST"])
@token_required
def inscribir_estudiante():
    
    if 'id_convocatoria' not in request.form or len(request.form.get('id_convocatoria').strip()) == 0:
        return jsonify({"success": False, "error" : "Campo id convocatoria vacio"}), HTTPStatus.BAD_REQUEST
    
    id_convocatoria = request.form.get('id_convocatoria')
    convocatoria = CONVOCATORIA(id=id_convocatoria)
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().read(convocatoria)
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "origen": "convocatoria", "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST

    estudiante = DAOFactoryOracle.get_estudiantes_dao().estudiante_x_usuario()
    if isinstance(estudiante, Error):
        return jsonify({"success": False, "origen": "estudiante", "message" : str(estudiante)}) , HTTPStatus.BAD_REQUEST
    if estudiante is None:
        return jsonify({"success": False, "message" : "No hay ningun estudiante relacionado a este usuario"}) , HTTPStatus.BAD_REQUEST
    
    solicitud = DAOFactoryOracle.get_solicitudes_dao().solicitud_x_estu_x_conv(estudiante.CODIGO, id_convocatoria)
    if isinstance(solicitud, Error):
        return jsonify({"success": False, "origen": "solicitud", "message" : str(solicitud)}) , HTTPStatus.BAD_REQUEST
    if solicitud is not None:
        return jsonify({"success": False, "message" : "Ya existe una solicitud creada para este estudiante"}) , HTTPStatus.BAD_REQUEST
    
    upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", 'static/uploads'))

    tipos_x_convocatoria = DAOFactoryOracle.get_tipo_dao().tipos_x_convocatoria(id_convocatoria)
    if isinstance(tipos_x_convocatoria, Error):
        return jsonify({"success": False, "origen": "tipos_x_convocatoria", "message" : str(tipos_x_convocatoria)}) , HTTPStatus.BAD_REQUEST
    

    
    for tipo in tipos_x_convocatoria:
        nm_var = 'documento_' + str(tipo.ID_TIPO)
        nm_var_condicion = 'condicion_' + str(tipo.ID_TIPO)
        if nm_var_condicion not in request.form.keys():
            return jsonify({"success": False,  "message" : "No se envió la condicion para: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
        if nm_var not in request.files:
            return jsonify({"success": False, "message" : "No se envió el documento: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
        else:
            file = request.files[nm_var]
            if file.filename == '':
                return jsonify({"success": False, "message" : "No se envió el documento: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
    
    solicitud_c = SOLICITUDES(FK_CODIGO=estudiante.CODIGO, FK_ID_CONVOCATORIA=id_convocatoria)
    creoSolicitud = DAOFactoryOracle.get_solicitudes_dao().create(solicitud_c)
    if isinstance(creoSolicitud, Error):
        return jsonify({"success": False,"origen": "creoSolicitud", "message" : str(creoSolicitud)}) , HTTPStatus.BAD_REQUEST

    contador = 1
    for tipo in tipos_x_convocatoria:
        nm_var = 'documento_' + str(tipo.ID_TIPO)
        nm_var_condicion = 'condicion_' + str(tipo.ID_TIPO)
        if nm_var in request.files:
            file = request.files[nm_var]
            if file.filename != '':
                documento_ruta = secure_filename(file.filename)
                documento_condicion = request.form.get(nm_var_condicion)
                file.save(os.path.join(upload_folder, documento_ruta))
                documento_bd = DOCUMENTOS(
                    id=contador,
                    RUTA=documento_ruta,
                    ESTADO='POR REVISAR',
                    FK_ID_CONDICION=documento_condicion,
                    FK_ID_SOLICITUD=solicitud_c.ID_SOLICITUD
                )
                creoDocumento = DAOFactoryOracle.get_documentos_dao().create(documento_bd)
                if isinstance(creoDocumento, Error):
                    return jsonify({"success": False,"origen": "creoDocumento" , "message" : str(creoDocumento)}) , HTTPStatus.BAD_REQUEST

        contador+=1
    return jsonify({"success": True, "message" : "Solicitud agregada con éxito!"}) , HTTPStatus.OK

@convocatoria_bp.route('/ver-solicitudes-ultima-conv',methods=["GET"])
@token_required
def ver_solicitudes_ultima_conv():
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().obtener_ultima()
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST
    if convocatoria is None:
        return jsonify({"success": False, "message" : "Aun no existen convocatorias"}) , HTTPStatus.BAD_REQUEST
    
    consultaSolicitudes = DAOFactoryOracle.get_solicitudes_dao().solicitud_x_convocatoria(convocatoria.ID_CONVOCATORIA)
    if isinstance(consultaSolicitudes, Error):
        return jsonify({"success": False, "message" : str(consultaSolicitudes)}) , HTTPStatus.BAD_REQUEST

    solicitudes_dict = [{"ID_SOLICITUD": respSol[0],
                         "ESTADO_SOLICITUD": respSol[1],
                         "NOMBRE_ESTUDIANTE": respSol[2],
                         "APELLIDO_ESTUDIANTE": respSol[3]
                         } for respSol in consultaSolicitudes]
    
    return jsonify({"success": True, "message" : "Solicitudes consultadas con éxito!", "data": {
        "SOLICITUDES": solicitudes_dict,
        "CONVOCATORIA": {
            "ID_CONVOCATORIA": convocatoria.ID_CONVOCATORIA,
            "FECHA_I_INSC": dateToStr(convocatoria.FECHA_I_INSC),
            "FECHA_F_INSC": dateToStr(convocatoria.FECHA_I_VERIF),
            "ESTADO": convocatoria.ESTADO
        }
    }}) , HTTPStatus.OK

@convocatoria_bp.route('/ver-documentos/<id_convocatoria>/<id_solicitud>',methods=["GET"])
@token_required
def ver_documentos_x_convocatoria_solicitud(id_convocatoria, id_solicitud):
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().read(CONVOCATORIA(id=id_convocatoria))
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST
    if convocatoria is None:
        return jsonify({"success": False, "message" : "Convocatoria no encontrada"}) , HTTPStatus.BAD_REQUEST
    
    solicitud = DAOFactoryOracle.get_solicitudes_dao().read(SOLICITUDES(id=id_solicitud))
    if isinstance(solicitud, Error):
        return jsonify({"success": False, "message" : str(solicitud)}) , HTTPStatus.BAD_REQUEST
    if solicitud is None:
        return jsonify({"success": False, "message" : "Solicitud no encontrada"}) , HTTPStatus.BAD_REQUEST
    
    consultaDocumentos = DAOFactoryOracle.get_documentos_dao().documentos_tipo_condicion_x_solicitud(id_solicitud)
    if isinstance(consultaDocumentos, Error):
        return jsonify({"success": False, "message" : str(consultaDocumentos)}) , HTTPStatus.BAD_REQUEST

    documentos_dict = [{ "NOMBRE_TIPO": respDoc[0],
                         "NOMBRE_CONVOCATORIA": respDoc[1],
                         "ESTADO_DOC": respDoc[2],
                         "RUTA_DOC": ruta+respDoc[3],
                         "ID_DOC": respDoc[4]
                         } for respDoc in consultaDocumentos]
    
    return jsonify({"success": True, "message" : "Documentos consultados con éxito!", "data": {
        "DOCUMENTOS": documentos_dict
    }}) , HTTPStatus.OK

@convocatoria_bp.route('/actualizar-documentos',methods=["POST"])
@token_required
def actualizar_documentos():

    if 'id_convocatoria' not in request.form or len(request.form.get('id_convocatoria').strip()) == 0:
        return jsonify({"success": False, "error" : "Campo id convocatoria vacio"}), HTTPStatus.BAD_REQUEST
    
    if 'id_solicitud' not in request.form or len(request.form.get('id_solicitud').strip()) == 0:
        return jsonify({"success": False, "error" : "Campo id solicitud vacio"}), HTTPStatus.BAD_REQUEST
    
    id_convocatoria = request.form.get('id_convocatoria')
    id_solicitud = request.form.get('id_solicitud')
    convocatoria = CONVOCATORIA(id=id_convocatoria)
    convocatoria = DAOFactoryOracle.get_convocatoria_dao().read(convocatoria)
    if isinstance(convocatoria, Error):
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST

    solicitud = SOLICITUDES(id=id_solicitud)
    solicitud = DAOFactoryOracle.get_solicitudes_dao().read(solicitud)
    if isinstance(solicitud, Error):
        return jsonify({"success": False, "message" : str(solicitud)}) , HTTPStatus.BAD_REQUEST
    if solicitud is None:
        return jsonify({"success": False, "message" : "Solicitud no encontrada"}) , HTTPStatus.BAD_REQUEST
    
    consultaDocumentos = DAOFactoryOracle.get_documentos_dao().documentos_tipo_condicion_x_solicitud(id_solicitud)
    if isinstance(consultaDocumentos, Error):
        return jsonify({"success": False, "message" : str(consultaDocumentos)}) , HTTPStatus.BAD_REQUEST
    for respDoc in consultaDocumentos:
        nm_var_documento = 'estado_documento_' + str(respDoc[4])
        if nm_var_documento not in request.form.keys():
            return jsonify({"success": False, "message" : "No se envió la verificación para el documento con ID: " + respDoc[4]}) , HTTPStatus.BAD_REQUEST

    for respDoc in consultaDocumentos:
        nm_var_documento = 'estado_documento_' + str(respDoc[4])
        documento_estado = request.form.get(nm_var_documento)
        actualizoDocumento = DAOFactoryOracle.get_documentos_dao().actualizar_estado_documento(id_solicitud, respDoc[4], documento_estado)
        if isinstance(actualizoDocumento, Error):
            return jsonify({"success": False, "message" : str(actualizoDocumento)}) , HTTPStatus.BAD_REQUEST
        
    actualizoSolicitud = DAOFactoryOracle.get_solicitudes_dao().actualizar_estado(id_solicitud, 'VERIFICADA')
    if isinstance(actualizoSolicitud, Error):
        return jsonify({"success": False, "message" : str(actualizoSolicitud)}) , HTTPStatus.BAD_REQUEST

    return jsonify({"success": True, "message" : "Estado de los documentos actualizados con éxito!"}) , HTTPStatus.OK

@convocatoria_bp.route('/tipos-subsidios',methods=["GET"])
@token_required
def obtener_tipos_subsidios():
    tipos_subsidios = DAOFactoryOracle.get_tipo_subsidio_dao().findall(TIPO_SUBSIDIO())
    if isinstance(tipos_subsidios, Error):
        return jsonify({"success": False, "message" : str(tipos_subsidios)}) , HTTPStatus.BAD_REQUEST
    print(tipos_subsidios)

    tipos_subsidios_dict = [{"ID_TIPO_SUBSIDIO": tip.ID_TIPO_SUBSIDIO,
                         "NOMBRE": tip.NOMBRE,
                         "POR_COBERTURA": tip.POR_COBERTURA,
                         "HRS_DEDICACION_X_SEM": tip.HRS_DEDICACION_X_SEM
                         } for tip in tipos_subsidios]
    
    return jsonify({"success": True, "message" : "Tipos de subsidios consultados con éxito!", "data": {
        "TIPOS_SUBSIDIOS" : tipos_subsidios_dict
    }}) , HTTPStatus.OK

@convocatoria_bp.route('/variables',methods=["GET"])
@token_required
def obtener_variables():
    variables = DAOFactoryOracle.get_tipo_subsidio_dao().findall(TIPO())
    if isinstance(variables, Error):
        return jsonify({"success": False, "message" : str(variables)}) , HTTPStatus.BAD_REQUEST
    
    variables_dict = []
    for variable in variables:        
        condiciones = DAOFactoryOracle.get_condiciones_dao().condiciones_x_tipo(variable.ID_TIPO)
        if isinstance(condiciones, Error):
            return jsonify({"success": False, "message" : str(condiciones)}) , HTTPStatus.BAD_REQUEST
        condiciones_dict = [{"ID_CONDICION": condicion.ID_CONDICION, "NOMBRE": condicion.NOMBRE} for condicion in condiciones]
        variables_dict.append({"ID_TIPO":variable.ID_TIPO, "NOMBRE": variable.NOMBRE, "PUNTAJE_MAX":variable.PUNTAJE_MAX, "CONDICIONES" : condiciones_dict }) 
    
    return jsonify({"success": True, "message" : "Tipos de subsidios consultados con éxito!", "data": {
        "VARIABLES" : variables_dict
    }}) , HTTPStatus.OK

@convocatoria_bp.route('/nueva',methods=["POST"])
@token_required
def nueva_convocatoria():
    json_recibido = request.get_json()

    campos_validar = [
        'ID_CONVOCATORIA',
        'FECHA_I_CONV',
        'FECHA_I_INSC',
        'FECHA_I_VERIF',
        'FECHA_I_PUBL',
        'FECHA_I_CUMP',
        'FECHA_F_CUMP',
        'PERIODO',
        'VALOR_X_ALMUERZO'
    ]

    for campo in campos_validar:
        if campo not in json_recibido or len(str(json_recibido[campo]).strip()) == 0:
            return jsonify({"success": False, "error" : f"Campo {campo} vacio"}), HTTPStatus.BAD_REQUEST

    if 'TIPOS_SUBSIDIO' not in json_recibido or len(json_recibido['TIPOS_SUBSIDIO']) == 0:
        return jsonify({"success": False, "error" : f"Campo TIPOS_SUBSIDIO vacio"}), HTTPStatus.BAD_REQUEST
    
    if 'VARIABLES' not in json_recibido or len(json_recibido['VARIABLES']) == 0:
        return jsonify({"success": False, "error" : f"Campo VARIABLES vacio"}), HTTPStatus.BAD_REQUEST
    
    req_ID_CONVOCATORIA = json_recibido['ID_CONVOCATORIA']
    req_FECHA_I_CONV = json_recibido['FECHA_I_CONV']
    req_FECHA_I_INSC = json_recibido['FECHA_I_INSC']
    req_FECHA_I_VERIF = json_recibido['FECHA_I_VERIF']
    req_FECHA_I_PUBL = json_recibido['FECHA_I_PUBL']
    req_FECHA_I_CUMP = json_recibido['FECHA_I_CUMP']
    req_FECHA_F_CUMP = json_recibido['FECHA_F_CUMP']
    req_PERIODO = json_recibido['PERIODO']
    req_VALOR_X_ALMUERZO = json_recibido['VALOR_X_ALMUERZO']
    req_TIPOS_SUBSIDIO = json_recibido['TIPOS_SUBSIDIO']
    req_VARIABLES = json_recibido['VARIABLES']

    tipos_subsidiosUsados = []
    for item_TIPO_SUBSIDIO in req_TIPOS_SUBSIDIO:
        if item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"] == "NUEVA":            
            campos_validar = [
                'TIPO_SUBSIDIO_NOM',
                'TIPO_SUBSIDIO_POR',
                'TIPO_SUBSIDIO_HOR',
            ]
            for campo in campos_validar:
                if campo not in item_TIPO_SUBSIDIO or len(str(item_TIPO_SUBSIDIO[campo]).strip()) == 0:
                    return jsonify({"success": False, "error" : f"Campo {campo} vacio"}), HTTPStatus.BAD_REQUEST
        else:
            if item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"] in tipos_subsidiosUsados:
                return jsonify({"success": False, "error" : f"ID_TIPO_SUBSIDIO duplicado, enviá solo una un mismo tipo de subsidio"}), HTTPStatus.BAD_REQUEST
            tipos_subsidiosUsados.append(item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"])
        
        if 'TIPO_SUBSIDIO_CUP' not in item_TIPO_SUBSIDIO or len(str(item_TIPO_SUBSIDIO['TIPO_SUBSIDIO_CUP']).strip()) == 0:
            return jsonify({"success": False, "error" : f"Campo TIPO_SUBSIDIO_CUP vacio"}), HTTPStatus.BAD_REQUEST

    variablesUsadas = []
    for item_VARIABLES in req_VARIABLES:
        if item_VARIABLES["ID_VARIABLE"] == "NUEVA":
            campos_validar = [
                'VARIABLE_NOM'
            ]
            for campo in campos_validar:
                if campo not in item_VARIABLES or len(str(item_VARIABLES[campo]).strip()) == 0:
                    return jsonify({"success": False, "error" : f"Campo {campo} vacio"}), HTTPStatus.BAD_REQUEST
        else:
            if item_VARIABLES["ID_VARIABLE"] in variablesUsadas:
                return jsonify({"success": False, "error" : f"ID_VARIABLE duplicado, enviá solo una un mismo de variables"}), HTTPStatus.BAD_REQUEST
            variablesUsadas.append(item_VARIABLES["ID_VARIABLE"])
            
        if 'VARIABLE_CONDICIONES' not in item_VARIABLES:
            return jsonify({"success": False, "error" : f"Cada variable debe tener al menos una opción"}), HTTPStatus.BAD_REQUEST
        
        varCondiciones = item_VARIABLES['VARIABLE_CONDICIONES']
        for item_condicion in varCondiciones:
            campos_validar = [
                'CONDICION_NOM',
                'CONDICION_PUN',
            ]
            for campo in campos_validar:
                if campo not in item_condicion or len(str(item_condicion[campo]).strip()) == 0:
                    return jsonify({"success": False, "error" : f"Campo {campo} vacio"}), HTTPStatus.BAD_REQUEST
                
            
    #Creo Convocatoria
    convocatoria = CONVOCATORIA(
        FECHA_I_CONV = req_FECHA_I_CONV,
        FECHA_I_INSC = req_FECHA_I_INSC,
        FECHA_I_VERIF = req_FECHA_I_VERIF,
        FECHA_I_PUBL = req_FECHA_I_PUBL,
        FECHA_I_CUMP = req_FECHA_I_CUMP,
        FECHA_F_CUMP = req_FECHA_F_CUMP,
        PERIODO = req_PERIODO,
        ESTADO= 'CREADA',
        VALOR_X_ALMUERZO= req_VALOR_X_ALMUERZO,
        id = req_ID_CONVOCATORIA 
    )
    creoConvocatoria = DAOFactoryOracle.get_convocatoria_dao().create(convocatoria)
    if isinstance(creoConvocatoria, Error):
        return jsonify({"success": False, "message" : str(creoConvocatoria)}) , HTTPStatus.BAD_REQUEST

    for item_TIPO_SUBSIDIO in req_TIPOS_SUBSIDIO:
        if item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"] == "NUEVA":
            tipo_subidio = TIPO_SUBSIDIO(
                NOMBRE = item_TIPO_SUBSIDIO["TIPO_SUBSIDIO_NOM"],
                POR_COBERTURA = item_TIPO_SUBSIDIO["TIPO_SUBSIDIO_POR"],
                HRS_DEDICACION_X_SEM = item_TIPO_SUBSIDIO["TIPO_SUBSIDIO_HOR"],
                id = "TS" + item_TIPO_SUBSIDIO["TIPO_SUBSIDIO_NOM"][0:3]
            )
            creoTipoSubsidio = DAOFactoryOracle.get_convocatoria_dao().create(tipo_subidio)
            if isinstance(creoTipoSubsidio, Error):
                return jsonify({"success": False, "message" : str(creoTipoSubsidio)}) , HTTPStatus.BAD_REQUEST
            
            item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"] = tipo_subidio.ID_TIPO_SUBSIDIO

        nuevaRelTipoSubsidio = CONVOCATORIA_TIPO_SUBSIDIO(
            FK_ID_CONVOCATORIA = convocatoria.ID_CONVOCATORIA,
            FK_ID_TIPO_SUBSIDIO = item_TIPO_SUBSIDIO["ID_TIPO_SUBSIDIO"],
            CANTIDAD = item_TIPO_SUBSIDIO["TIPO_SUBSIDIO_CUP"]
        )
        creoNuevaRelTipoSubisidio = DAOFactoryOracle.get_tipo_subsidio_dao().create(nuevaRelTipoSubsidio)
        if isinstance(creoNuevaRelTipoSubisidio, Error):
            return jsonify({"success": False, "message" : str(creoNuevaRelTipoSubisidio)}) , HTTPStatus.BAD_REQUEST

    variablesUsadas = []
    for item_VARIABLES in req_VARIABLES:
        if item_VARIABLES["ID_VARIABLE"] == "NUEVA":
            variable = TIPO(NOMBRE=item_VARIABLES["VARIABLE_NOM"], id="T"+item_VARIABLES["VARIABLE_NOM"][0:4])
            creoVariable = DAOFactoryOracle.get_tipo_dao().create(variable)
            if isinstance(creoVariable, Error):
                return jsonify({"success": False, "message" : str(creoVariable)}) , HTTPStatus.BAD_REQUEST
            item_VARIABLES["ID_VARIABLE"] = variable.ID_TIPO
        
        nuevaRelVariable = CONVOCATORIA_TIPO(
            FK_ID_CONVOCATORIA = convocatoria.ID_CONVOCATORIA,
            FK_ID_TIPO = item_VARIABLES["ID_VARIABLE"]
        )
        creoNuevaRelVariable = DAOFactoryOracle.get_convocatoria_tipo_dao().create(nuevaRelVariable)
        if isinstance(creoNuevaRelVariable, Error):
            return jsonify({"success": False, "message" : str(creoNuevaRelVariable)}) , HTTPStatus.BAD_REQUEST

        varCondiciones = item_VARIABLES['VARIABLE_CONDICIONES']
        for i_condicion,item_condicion in enumerate(varCondiciones):
            condicion = CONDICIONES(
                NOMBRE = item_condicion["CONDICION_NOM"],
                PUNTAJE = item_condicion["CONDICION_PUN"],
                FK_ID_TIPO = item_VARIABLES["ID_VARIABLE"],
                id = "CON"+item_VARIABLES["ID_VARIABLE"]+str(i_condicion)
            )
            creoCondicion = DAOFactoryOracle.get_condiciones_dao().create(condicion)
            if isinstance(creoCondicion, Error):
                return jsonify({"success": False, "message" : str(creoCondicion)}) , HTTPStatus.BAD_REQUEST
                  
        recalculoMaximo = DAOFactoryOracle.get_tipo_dao().recalcular_maximo_puntaje(item_VARIABLES["ID_VARIABLE"])
        if isinstance(recalculoMaximo, Error):
            return jsonify({"success": False, "message" : str(recalculoMaximo)}) , HTTPStatus.BAD_REQUEST
        

    return jsonify({"success": True, "message" : "Convocatoria creada con éxito!"}) , HTTPStatus.OK

    
    
    


def verificar_datos_vacios_inscribirme(json_recibido):
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'contrasena' not in json_recibido or len(json_recibido['contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo contrasena vacio"})
    
    return None

def dateToStr(date):
    fecha = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
    return fecha.strftime("%Y-%m-%d")
     