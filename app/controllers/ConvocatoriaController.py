import os
from werkzeug.utils import secure_filename

from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required
from app.daos.DAOFactory import DAOFactoryOracle
from app.models.entidades import CONVOCATORIA, DOCUMENTOS, SOLICITUDES
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
        return jsonify({"success": False, "message" : str(convocatoria)}) , HTTPStatus.BAD_REQUEST

    estudiante = DAOFactoryOracle.get_estudiantes_dao().estudiante_x_usuario()
    if isinstance(estudiante, Error):
        return jsonify({"success": False, "message" : str(estudiante)}) , HTTPStatus.BAD_REQUEST
    if estudiante is None:
        return jsonify({"success": False, "message" : "No hay ningun estudiante relacionado a este usuario"}) , HTTPStatus.BAD_REQUEST
    
    solicitud = DAOFactoryOracle.get_solicitudes_dao().solicitud_x_estu_x_conv(estudiante.CODIGO, id_convocatoria)
    if isinstance(solicitud, Error):
        return jsonify({"success": False, "message" : str(solicitud)}) , HTTPStatus.BAD_REQUEST
    if solicitud is not None:
        return jsonify({"success": False, "message" : "Ya existe una solicitud creada para este estudiante"}) , HTTPStatus.BAD_REQUEST
    
    upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", 'static/uploads'))

    tipos_x_convocatoria = DAOFactoryOracle.get_tipo_dao().tipos_x_convocatoria(id_convocatoria)
    if isinstance(tipos_x_convocatoria, Error):
        return jsonify({"success": False, "message" : str(tipos_x_convocatoria)}) , HTTPStatus.BAD_REQUEST
    

    
    for tipo in tipos_x_convocatoria:
        nm_var = 'documento_' + str(tipo.ID_TIPO)
        nm_var_condicion = 'condicion_' + str(tipo.ID_TIPO)
        if nm_var_condicion not in request.form.keys():
            return jsonify({"success": False, "message" : "No se envió la condicion para: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
        if nm_var not in request.files:
            return jsonify({"success": False, "message" : "No se envió el documento: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
        else:
            file = request.files[nm_var]
            if file.filename == '':
                return jsonify({"success": False, "message" : "No se envió el documento: " + tipo.NOMBRE}) , HTTPStatus.BAD_REQUEST
    
    solicitud_c = SOLICITUDES(FK_CODIGO=estudiante.CODIGO, FK_ID_CONVOCATORIA=id_convocatoria)
    creoSolicitud = DAOFactoryOracle.get_solicitudes_dao().create(solicitud_c)
    if isinstance(creoSolicitud, Error):
        return jsonify({"success": False, "message" : str(creoSolicitud)}) , HTTPStatus.BAD_REQUEST

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
                    return jsonify({"success": False, "message" : str(creoDocumento)}) , HTTPStatus.BAD_REQUEST

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

def verificar_datos_vacios_inscribirme(json_recibido):
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'contrasena' not in json_recibido or len(json_recibido['contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo contrasena vacio"})
    
    return None

def dateToStr(date):
    fecha = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
    return fecha.strftime("%Y-%m-%d")
     