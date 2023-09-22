class Config(object):
    DEBUG=False

class ProductionConfig(Config):
    SECRET_KEY = '075102ad69bff65857ebfe8b03f0e1f54571cd724713c3710653496702ae6e9f'
    JWT_SECRET_KEY = '9bf2f3683315efd31cc3dfc23d1efe30d245575faa27504c7daf113ca07a9ce4' #SHA-256(BasesDeDatos2 DEV)
    LIB_DIR = ''
    ORACLE_DSN = ''
    ORACLE_USER = ''
    ORACLE_PASS = ''

class DevelopmentConfig(Config):
    SECRET_KEY = '836f57bd4eb7cde5dd6aea4a0d30b14e81aa93c7675dea4067d42ed27ede51c2'
    DEBUG=True
    JWT_SECRET_KEY = '8081907b2886afec69ffb3eeb5a5982d200668b9a6bd0bec65a73f5c6c3e3115'
    LIB_DIR = 'D:/app/Bryant/product/21c/dbhomeXE/bin'
    ORACLE_DSN = 'BRYANT_PDB'
    ORACLE_PASS = 'ADM_SEG'
    ORACLE_USER = 'ADM_SEG'