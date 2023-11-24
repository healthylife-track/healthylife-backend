from flask import Flask
from flask_wtf.csrf import CSRFProtect
# from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from flask_migrate import Migrate


#instantiate an object of Flask app
app = Flask(__name__, instance_relative_config=True)
# jwt = JWTManager(app)
csrf=CSRFProtect(app)


#Load the config file
from healthapp import config
app.config.from_object(config.LiveConfig)
app.config.from_pyfile('config.py', silent=False)


#database connection
db=SQLAlchemy(app)
mail=Mail(app)
migrate = Migrate(app, db)


#load your routes here
from healthapp import routes #since routes is now a module on its own


#load models
from healthapp import models

#load test
from healthapp import route_test