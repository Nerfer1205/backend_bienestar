class Config(object):
    DEBUG=True

class ProductionConfig(Config):
    SECRET_KEY = 'dev'
    JWT_SECRET_KEY = ''
    LIB_DIR = ''
    ORACLE_DSN = ''
    ORACLE_USER = ''
    ORACLE_PASS = ''

class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    JWT_SECRET_KEY = ''
    LIB_DIR = 'C:/app/USER/product/21c/dbhomeXE/bin'
    ORACLE_DSN = 'PDB1'
    ORACLE_USER = 'bienestar'
    ORACLE_PASS = 'bienestar'