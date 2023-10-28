from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required
from app.daos.DAOoracle import DAOgenericoOracle
from app.daos.DAOFactory import DAOFactoryOracle
from app.models.entidades import ESTUDIANTE
from oracledb import Error
import jwt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_login(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_usuario = json_recibido["usuario"]
    req_contrasena = json_recibido["contrasena"]
    current_app.config['ORACLE_USER'] = "U_" + req_usuario
    current_app.config['ORACLE_PASS'] = req_contrasena
    #Validar conexión
    puedoConectarme = DAOgenericoOracle().conectar()
    if puedoConectarme == True:
        token = jwt.encode({'usuario': req_usuario, 'contrasena': req_contrasena}, current_app.config['JWT_SECRET_KEY'])
        return jsonify({"success": True, "message" : "¡Bienvenido!", "token": token}) , HTTPStatus.OK
    
    return jsonify({"success": False, "message" : str(puedoConectarme)}) , HTTPStatus.BAD_REQUEST

@auth_bp.route('/registro', methods=['POST'])
def registro():
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_registro(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_usuario = 'U_' + json_recibido["usuario"]
    req_contrasena = json_recibido["contrasena"]
    req_codigo = json_recibido["codigo"]

    estudiante = ESTUDIANTE(id=req_codigo)
    estudiante = DAOFactoryOracle.get_estudiantes_dao().read(estudiante)
    if isinstance(estudiante, Error):
        return jsonify({"success": False, "message" : str(estudiante)}) , HTTPStatus.BAD_REQUEST
    
    if estudiante is None:
        return jsonify({"success": False, "message" : "Estudiante no encontrado"}) , HTTPStatus.BAD_REQUEST
    
    if estudiante.USUARIO is not None and estudiante.USUARIO != '':
        return jsonify({"success": False, "message" : "El estudiante ya tiene un usuario asignado"}) , HTTPStatus.BAD_REQUEST

    usuarioFueCreado = DAOFactoryOracle.get_usuario_dao().crear_usuario(req_usuario, req_contrasena)
    if isinstance(usuarioFueCreado, Error):
        return jsonify({"success": False, "message" : str(usuarioFueCreado)}) , HTTPStatus.BAD_REQUEST
   
    estudianteActualizado = DAOFactoryOracle.get_estudiantes_dao().actualizar_usuario(req_usuario,req_codigo)
    if isinstance(estudianteActualizado, Error):
        return jsonify({"success": False, "message" : str(estudianteActualizado)}) , HTTPStatus.BAD_REQUEST
    

    return jsonify({"success": True, "message" : "¡Estudiante creado correctamente!"}) , HTTPStatus.OK    



#Verificaciones
def verificar_datos_vacios_login(json_recibido):
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'contrasena' not in json_recibido or len(json_recibido['contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo contrasena vacio"})
    
    return None

def verificar_datos_vacios_registro(json_recibido):
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'contrasena' not in json_recibido or len(json_recibido['contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo contrasena vacio"})
    
    if 'codigo' not in json_recibido or len(json_recibido['codigo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo codigo vacio"})
    
    return None