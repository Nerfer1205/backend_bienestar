from flask import Flask
from config.configuration import ProductionConfig, DevelopmentConfig
from flask_cors import CORS
from app.controllers.AuthController import auth_bp

app = Flask(__name__)

# Configuración de la base de datos
app.config.from_object(DevelopmentConfig())

CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)