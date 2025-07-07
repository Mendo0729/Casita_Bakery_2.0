import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:admin2907@localhost/Casita_Bakery'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
