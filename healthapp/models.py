import datetime
from healthapp import db

class User(db.Model):
    user_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    user_fname=db.Column(db.String(225), nullable=False)
    user_lname=db.Column(db.String(225), nullable=False)
    user_email=db.Column(db.String(225), nullable=False)
    user_pass = db.Column(db.String(225), nullable=False)
    user_role = db.Column(db.Enum('patient','doctor'), nullable=True)
    user_phoneNo = db.Column(db.String(16), nullable=False)
    user_licenseNo = db.Column(db.String(50), nullable=True)
    user_bloodgroup = db.Column(db.String(10), nullable=False)
    user_genotype = db.Column(db.String(225), nullable=False)
    user_medCondition = db.Column(db.String(225), nullable=False)
    user_pic = db.Column(db.String(225), nullable=True)
    
    #relationship
    mdobj = db.relationship("Medreminder", back_populates='userobj2')
    loginobj = db.relationship('Login', back_populates='userobj3')
    doctor_written = db.relationship('Medreport', back_populates='doctor',
                                     foreign_keys='Medreport.mr_doctorid')
    reports_received = db.relationship('Medreport', back_populates='patient',
                                       foreign_keys='Medreport.mr_patientid')


class Medreminder(db.Model):
    md_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    md_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    md_drugname = db.Column(db.String(100), nullable=False)
    md_drugunit=db.Column(db.String(10), nullable=True)
    md_time = db.Column(db.String(10), nullable=True)
    md_timeInterval = db.Column(db.String(10), nullable=True)
    md_dayinterval = db.Column(db.String(10), nullable=True)
    md_usage = db.Column(db.Enum('taken','skipped','missed'), 
                         nullable=True, server_default='missed')
    md_userid=db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    userobj2 = db.relationship("User", back_populates='mdobj')


class Medreport(db.Model):
    mr_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    mr_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    mr_report = db.Column(db.Text(), nullable=True)
    mr_doctorid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    mr_patientid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    doctor = db.relationship('User', back_populates='doctor_written', foreign_keys=[mr_doctorid])
    patient = db.relationship('User', back_populates='reports_received', foreign_keys=[mr_patientid])
    
    
class Login(db.Model):
    login_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    login_email=db.Column(db.String(225), nullable=False)
    login_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    logout_date = db.Column(db.DateTime(), nullable=True)
    login_userid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    userobj3 = db.relationship('User', back_populates='loginobj')