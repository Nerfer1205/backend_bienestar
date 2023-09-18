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
    DEBUG=True
    JWT_SECRET_KEY = ''
    LIB_DIR = 'D:/app/Bryant/product/21c/dbhomeXE/bin'
    ORACLE_DSN = 'BRYANT_PDB'
    ORACLE_USER = 'ADM_SEG'
    ORACLE_PASS = 'ADM_SEG'