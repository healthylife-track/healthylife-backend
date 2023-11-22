import datetime
from healthapp import db

class User(db.Model):
    user_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    user_name=db.Column(db.String(225), nullable=False)
    user_email=db.Column(db.String(225), nullable=False)
    user_pass = db.Column(db.String(225), nullable=False)
    user_role = db.Column(db.Enum('patient','doctor'), nullable=True)
    user_phoneNo = db.Column(db.String(16), nullable=False)
    user_licenseNo = db.Column(db.String(50), nullable=True)
    user_bloodgroup = db.Column(db.String(10), nullable=False)
    #relationship
    mtobj = db.relationship("MedTrack", back_populates='userobj')
    mdobj = db.relationship("MedReminder", back_populates='userobj2')
    loginobj = db.relationship('Login', back_populates='userobj3')
    
    

class MedTrack(db.Model):
    mt_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    mt_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    mt_track=db.Column(db.Boolean, default=False)
    mt_userid=db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    userobj = db.relationship("User", back_populates='mtobj')


class MedReminder(db.Model):
    md_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    md_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    md_alert = db.Column(db.String(50), nullable=False)
    md_detail=db.Column(db.Text(), nullable=True)
    md_userid=db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    userobj2 = db.relationship("User", back_populates='mdobj')

class Login(db.Model):
    login_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    login_email=db.Column(db.String(225), nullable=False)
    login_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    logout_date = db.Column(db.DateTime(), nullable=True)
    login_userid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    userobj3 = db.relationship('User', back_populates='loginobj')