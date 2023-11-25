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
    user_bloodgroup = db.Column(db.String(10), nullable=False)
    user_genotype = db.Column(db.String(225), nullable=False)
    user_medCondition = db.Column(db.String(225), nullable=False)
    user_pic = db.Column(db.String(225), nullable=True)
    
    #relationship
    mdobj = db.relationship("Medreminder", back_populates='userobj2')
    loginobj = db.relationship('Login', back_populates='userobj3')
    usermedrepobj = db.relationship("Medreport", back_populates='userMedrep')
    

class Doctor(db.Model):
    doc_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    doc_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    doc_fname=db.Column(db.String(225), nullable=False)
    doc_lname=db.Column(db.String(225), nullable=False)
    doc_email=db.Column(db.String(225), nullable=False)
    doc_pass = db.Column(db.String(225), nullable=False)
    doc_role = db.Column(db.Enum('patient','doctor'), nullable=True)
    doc_phoneNo = db.Column(db.String(16), nullable=False)
    doc_licenseNo = db.Column(db.String(50), nullable=True)
    doc_bloodgroup = db.Column(db.String(10), nullable=False)
    doc_genotype = db.Column(db.String(225), nullable=False)
    doc_medCondition = db.Column(db.String(225), nullable=False)
    doc_pic = db.Column(db.String(225), nullable=True)
    
    #relationship
    mddocobj = db.relationship("Medreminder", back_populates='docobj')
    logindocobj = db.relationship('Login', back_populates='docloginobj')
    docmedrepobj = db.relationship("Medreport", back_populates='docmedrep')

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
    #foreignKey
    md_userid=db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    md_docid=db.Column(db.Integer(), db.ForeignKey('doctor.doc_id'))
    #relationship
    userobj2 = db.relationship("User", back_populates='mdobj')
    docobj = db.relationship("Doctor", back_populates='mddocobj')


class Medreport(db.Model):
    mr_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    mr_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    mr_report = db.Column(db.Text(), nullable=True)
    #foreignKey
    mr_userid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    mr_docid = db.Column(db.Integer(), db.ForeignKey('doctor.doc_id'))
    #relationship
    userMedrep = db.relationship("User", back_populates='usermedrepobj')
    docmedrep = db.relationship("Doctor", back_populates='docmedrepobj')
    
    
    
    
class Login(db.Model):
    login_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    login_email=db.Column(db.String(225), nullable=False)
    login_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), index=True)
    logout_date = db.Column(db.DateTime(), nullable=True)
    #foreignKey
    login_userid = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    login_docid = db.Column(db.Integer(), db.ForeignKey('doctor.doc_id'))
    #Relationship
    userobj3 = db.relationship('User', back_populates='loginobj')
    docloginobj = db.relationship('Doctor', back_populates='logindocobj')