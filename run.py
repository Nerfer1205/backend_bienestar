from flask import Flask
from config.configuration import ProductionConfig, DevelopmentConfig
from flask_cors import CORS


app = Flask(__name__)

# Configuración de la base de datos
app.config.from_object(DevelopmentConfig())

CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)