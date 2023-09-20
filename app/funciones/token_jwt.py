import jwt
from functools import wraps
from http import HTTPStatus
from flask import jsonify, request, current_app

#crear decorador para obtener token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
           return jsonify({'error': 'Token faltante'}), HTTPStatus.UNAUTHORIZED

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'])
            current_app.config['ORACLE_USER'] = "U_" + data['usuario']
            current_app.config['ORACLE_PASS'] = data['contrasena']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'El token ha expirado'}), HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), HTTPStatus.UNAUTHORIZED
        except:
            return jsonify({'error': 'Token inválido'}), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated

def ver_datos_token():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], ["HS256"])
    return data