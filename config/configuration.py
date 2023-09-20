class Config(object):
    DEBUG=False

class ProductionConfig(Config):
    SECRET_KEY = '0c6087e2c019ef369994d4d46a61e19a897e2c15633bc04a78a8446a28b5dc30'
    JWT_SECRET_KEY = '0c6087e2c019ef369994d4d46a61e19a897e2c15633bc04a78a8446a28b5dc30' #SHA-256(BasesDeDatos2 DEV)
    LIB_DIR = ''
    ORACLE_DSN = ''
    ORACLE_USER = ''
    ORACLE_PASS = ''

class DevelopmentConfig(Config):
    SECRET_KEY = 'ff0a7a93cc63f07a9fe083bfb81bdf84a6860b3d3d36ef36bd92f5f3e1297ce4'
    DEBUG=True
    JWT_SECRET_KEY = 'ff0a7a93cc63f07a9fe083bfb81bdf84a6860b3d3d36ef36bd92f5f3e1297ce4' #SHA-256(BasesDeDatos2 DEV)
    LIB_DIR = 'D:/app/Bryant/product/21c/dbhomeXE/bin'
    ORACLE_DSN = 'BRYANT_PDB'
    ORACLE_PASS = 'ADM_SEG'
    ORACLE_USER = 'ADM_SEG'