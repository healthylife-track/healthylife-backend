import datetime
from healthapp import db

class User(db.Model):
    user_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    user_name=db.Column(db.String(225), nullable=False)
    user_email=db.Column(db.String(225), nullable=False)
    user_role = db.Column(db.Enum('patient','doctor'), nullable=True)
    user_phoneNo = db.Column(db.String(16), nullable=False)
    user_licenseNo = db.Column(db.String(50), nullable=True)
    user_bloodgroup = db.Column(db.String(10), nullable=False)
    
    
