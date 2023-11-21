"""to start an app"""
from flask import render_template, request, flash, redirect, jsonify
from healthapp import app, db, csrf
from healthapp.models import User
from healthapp.signal import contact_signal
from healthapp.email import send_email_alert

"""homepage"""
@app.route('/', methods=['GET'])
def home():
    if request.method=='GET':
        return "Welcome to Health Paltform"

"""register"""
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        role = request.form['role']
        phoneNo = request.form['phoneno']
        licenseNo = request.form['licenseNo']
        bloodgroup = request.form['bloodgroup']
        # csrf_token = csrf.generate_csrf()
        # print(csrf_token)
        if role == 'patient' and licenseNo == 'None':
            if (name =="" and
                email =="" and
                role =="" and
                phoneNo =="" and
                bloodgroup ==""):
                return jsonify({"msg":"One or more field is empty"})
            elif (name !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  bloodgroup !=""):
                newuser = User(user_name=name,
                               user_email=email, 
                               user_role=role, 
                               user_phoneNo=phoneNo, 
                               user_bloodgroup=bloodgroup 
                               )
                db.session.add(newuser)
                return jsonify({"msg":"Registration Successful"})
        
        elif role == 'doctor' and licenseNo !='':
            if (name =="" and
                email =="" and
                role =="" and
                phoneNo =="" and
                licenseNo =="" and
                bloodgroup ==""):
                return jsonify({"msg":"One or more field is empty"})
            elif (name !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  licenseNo !="" and
                  bloodgroup !=""):
                newuser = User(user_name=name,
                               user_email=email, 
                               user_role=role, 
                               user_phoneNo=phoneNo, 
                               user_bloodgroup=bloodgroup)
                db.session.add(newuser)
            return jsonify({"msg":"Registration Successful"})

"""
@contact_signal.connect
def send_email_alart(sender, comment, post_author_email,  recipients):
    subject = f"Codinit:New message"
    body = f"Hi,\n\n My name is {recipients['custom']}, \n\n {comment} \n\n Codinit Team"
    send_email_alert(subject, body, [post_author_email])
    
"""