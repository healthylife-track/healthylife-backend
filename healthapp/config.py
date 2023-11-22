import os

class Config(object):
    DATABASE_URI = "KlesterThon-you#drop"
    MERCHANT_ID="SAMPLE"

class LiveConfig(Config):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/health"
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MERCHANT_ID="*&%1hjk23"
    
    
class Test_config(object):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/test"
    
    DATABASE_URI = "make i test your code"
    