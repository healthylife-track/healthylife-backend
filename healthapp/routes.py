"""to start an app"""
import datetime
from flask import render_template, request, jsonify, session, redirect
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from healthapp import app, db, csrf
from healthapp.models import User, Login
from healthapp.signal import contact_signal
from healthapp.email import send_email_alert

"""homepage"""
@app.route('/', methods=['GET'])
def home():
    if request.method=='GET':
        return render_template('index.html')

"""register"""
@app.route('/register/', methods=['GET','POST'])
@csrf.exempt
@cross_origin()
def register():
    if request.method=='GET':
        return redirect('/')
    
    if request.method=='POST':
        name=request.json['name']
        email=request.json['email']
        role = request.json['role']
        phoneNo = request.json['phoneno']
        pwd=request.json['pwd']
        cpwd=request.json['cpwd']
        licenseNo = request.json['licenseNo']
        bloodgroup = request.json['bloodgroup']
        
        if role == 'patient' and licenseNo == 'None':
            if (name =="" or
                email =="" or
                role =="" or
                phoneNo =="" or
                bloodgroup =="" or
                pwd=="" or
                cpwd==""):
                return jsonify({"msg":"One or more field is empty"})
            
            elif (pwd != cpwd):
                return jsonify({"msg":"Password does not match"})
            
            elif (name !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  bloodgroup !="" and
                  pwd != ""):
                formated = generate_password_hash(pwd)
                newuser = User(user_name=name,
                               user_email=email, 
                               user_role=role, 
                               user_phoneNo=phoneNo, 
                               user_bloodgroup=bloodgroup,
                               user_pass=formated 
                               )
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg":"Registration Successful"})
        
        elif role == 'doctor' and licenseNo !='':
            if (name =="" or
                email =="" or
                role =="" or
                phoneNo =="" or
                licenseNo =="" or
                bloodgroup =="" or
                pwd=="" or
                cpwd==""):
                return jsonify({"msg":"One or more field is empty"})
            
            elif (pwd != cpwd):
                return jsonify({"msg":"Password does not match"})
            
            elif (name !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  licenseNo !="" and
                  bloodgroup !="" and
                  pwd !=""):
                formated = generate_password_hash(pwd)
                newuser = User(user_name=name,
                               user_email=email, 
                               user_role=role, 
                               user_phoneNo=phoneNo, 
                               user_bloodgroup=bloodgroup,
                               user_pass=formated)
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg":"Registration Successful"})
        else:
            return jsonify({"msg":"Kindly fill all field"})

"""login"""
@app.route('/login/', methods=['GET','POST'])
@csrf.exempt
@cross_origin()
def login():
    if request.method=='GET':
        return redirect('/')
    
    if request.method=='POST':
        email=request.json['email']
        pwd=request.json['pwd']
        print(email)
        print(pwd)
        if email=="" or pwd=="":
            return jsonify({"msg":"One or more field is empty"})
        if email !="" or pwd !="":
            # quering user by filtering with email
            user=db.session.query(User).filter_by(user_email=email).first()
            if user ==None:
                return jsonify({'msg':'kindly supply a valid credentials'})
            else:
                formated_pwd=user.user_pass
                # checking password hash
                checking = check_password_hash(formated_pwd, pwd)
                if checking:
                    session['user']=user.user_id
                    lo=Login(login_email=user.user_email, login_userid=user.user_id)
                    db.session.add(lo)
                    db.session.commit()
                    return jsonify({"msg":"Login successful"})
                else:
                    return jsonify({"msg":"kindly supply a valid email address and password"})
        

"""logout session"""
@app.route('/logout/')
def logout():
    loggedin = session.get('user')
    if loggedin==None:
        return redirect('/')
        
    if request.method == 'GET':
        session.pop('user', None)
        lo=Login.query.filter_by(login_userid=loggedin, logout_date=None).first()
        lo.logout_date=datetime.utcnow()
        db.session.commit()
        return jsonify({"msg":"You have successfully logout"})
            
"""
@contact_signal.connect
def send_email_alart(sender, comment, post_author_email,  recipients):
    subject = f"Codinit:New message"
    body = f"Hi,\n\n My name is {recipients['custom']}, \n\n {comment} \n\n Codinit Team"
    send_email_alert(subject, body, [post_author_email])
    
"""
