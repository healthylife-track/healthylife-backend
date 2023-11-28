"""to start an app"""
from datetime import timedelta, datetime, time
from flask import render_template, request, jsonify, session, redirect
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from healthapp import app, db, csrf, scheduler
from healthapp.models import User, Login, Medreminder, Medreport, Doctor
from healthapp.signal import reminder_signal
from healthapp.email import send_email_alert


"""homepage"""
@app.route('/', methods=['GET'])
@cross_origin(origins=['*'])
def home():
    if request.method=='GET':
        return render_template('index.html')

"""register"""
@app.route('/register/', methods=['GET','POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def register():
    if request.method=='GET':
        return redirect('/')
    
    if request.method=='POST':
        fname=request.json['firstname']
        lname=request.json['lastname']
        email=request.json['email']
        role = request.json['role']
        phoneNo = request.json['phoneNo']
        pwd=request.json['password']
        cpwd=request.json['confirmPassword']
        licenseNo = request.json['LicenseNo']
        bloodgroup = request.json['bloodGroup']
        genotype = request.json['genotype']
        medCon = request.json['medicalCondition']
        # pic = request.json['profilePicture']
        
        
        if role == 'patient':
            if (fname =="" or
                lname =="" or
                email =="" or
                role =="" or
                phoneNo =="" or
                bloodgroup =="" or
                genotype =="" or
                medCon =="" or
                pwd=="" or
                cpwd==""):
                return jsonify({"msg":"One or more field is empty"})
            
            elif (pwd != cpwd):
                return jsonify({"msg":"Password does not match"})
            
            elif (fname !="" and
                  lname !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  bloodgroup !="" and
                  genotype !="" and
                  medCon !="" and
                  pwd != ""):
                formated = generate_password_hash(pwd)
                newuser = User(user_fname=fname,
                               user_lname=lname,
                               user_email=email, 
                               user_role=role, 
                               user_phoneNo=phoneNo, 
                               user_bloodgroup=bloodgroup,
                               user_genotype=genotype,
                               user_medCondition=medCon,
                               user_pass=formated 
                               )
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg":"Registration Successful"})
        
        elif role == 'doctor':
            if (fname =="" or
                lname =="" or
                email =="" or
                role =="" or
                phoneNo =="" or
                licenseNo =="" or
                bloodgroup =="" or
                genotype =="" or
                medCon =="" or
                pwd=="" or
                cpwd==""):
                return jsonify({"msg":"One or more field is empty"})
            
            elif (pwd != cpwd):
                return jsonify({"msg":"Password does not match"})
            
            elif (fname !="" and
                  lname !="" and
                  email !="" and
                  role !="" and
                  phoneNo !="" and
                  licenseNo !="" and
                  bloodgroup !="" and
                  genotype !="" and
                  medCon !="" and
                  pwd !=""):
                formated = generate_password_hash(pwd)
                newuser = Doctor(doc_fname=fname,
                               doc_lname=lname,
                               doc_email=email, 
                               doc_role=role, 
                               doc_phoneNo=phoneNo, 
                               doc_bloodgroup=bloodgroup,
                               doc_licenseNo=licenseNo,
                               doc_genotype=genotype,
                               doc_medCondition=medCon,
                               doc_pass=formated)
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg":"Registration Successful"})
        else:
            return jsonify({"msg":"Kindly fill all field"})

"""login"""
@app.route('/login/', methods=['GET','POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def login():
    if request.method=='GET':
        return redirect('/')
    
    if request.method=='POST':
        email=request.json['email']
        pwd=request.json['password']
        role=request.json['role']
        if email=="" or pwd=="" or role=="":
            return jsonify({"msg":"One or more field is empty"})
        if email !="" or pwd !="":
            # quering user by filtering with email
            user=db.session.query(User).filter_by(user_email=email, user_role=role).first()
            doct=db.session.query(Doctor).filter_by(doc_email=email, doc_role=role).first()
            
            if user ==None and doct ==None:
                return jsonify({'msg':'kindly supply a valid credentials'})
            else:
                if user:
                    formated_pwd=user.user_pass
                    # checking password hash
                    checking = check_password_hash(formated_pwd, pwd)
                    if checking:
                        session['user']=user.user_id
                        lo=Login(login_email=user.user_email, login_userid=user.user_id)
                        db.session.add(lo)
                        db.session.commit()
                        return jsonify({"msg":"Login successful", "id":session['user']})
                    else:
                        return jsonify({"msg":"kindly supply a valid email address and password"})
                elif doct:
                    formated_pwd=doct.doc_pass
                    # checking password hash
                    checking = check_password_hash(formated_pwd, pwd)
                    if checking:
                        session['doctor']=doct.doc_id
                        lo=Login(login_email=doct.doc_email, login_docid=doct.doc_id)
                        db.session.add(lo)
                        db.session.commit()
                        return jsonify({"msg":"Login successful", "id":session['doctor']})
                    else:
                        return jsonify({"msg":"kindly supply a valid email address and password"})
                else:
                    return jsonify({"msg":"Record not found"})
                    
        

"""logout session"""
@app.route('/logout/')
@cross_origin(origins=['*'])
def logout():
    loggedin = session.get('user')
    doctor = session.get('doctor')
    
    if loggedin==None and doctor==None:
        return redirect('/')
        
    if request.method == 'GET':
        if loggedin:
            session.pop('user', None)
            lo=Login.query.filter_by(login_userid=loggedin, logout_date=None).first()
            lo.logout_date=datetime.utcnow()
            db.session.commit()
            return jsonify({"msg":"You have successfully logout"})
        elif doctor:
            session.pop('doctor', None)
            lo=Login.query.filter_by(login_docid=doctor, logout_date=None).first()
            lo.logout_date=datetime.utcnow()
            db.session.commit()
            return jsonify({"msg":"You have successfully logout"})
            

"""dashboard"""
@app.route('/dashbord/', methods=['GET'])
@cross_origin(origins=['*'])
def dashboard():
    loggedin = session.get('user')
    doctor = session.get('doctor')
    
    if loggedin==None and doctor==None:
        return redirect('/')
    
    if request.method=='GET':
        newuser=User.query.get(loggedin)
        neuser=Doctor.query.get(doctor)
        
        if neuser:            
            doc_obj = {"id":neuser.doc_id,
                        "date":neuser.doc_date,
                        "firstname":neuser.doc_fname,
                        "lastname":neuser.doc_lname,  
                        "email":neuser.doc_email,
                        "role":neuser.doc_role,
                        "phoneNo":neuser.doc_phoneNo,
                        "LicenseNo":neuser.doc_licenseNo,
                        "genotype":neuser.doc_genotype,
                        "bloodGroup":neuser.doc_bloodgroup,
                        "medicalCondition":neuser.doc_medCondition,
                        "medicalReminder":[{
                            "id":md.md_id, 
                            "date":md.md_date,
                            "drugName":md.md_drugname,
                            "drugDosage":md.md_drugunit,
                            "time":md.md_time,
                            "timeInterval":md.md_timeInterval,
                            "dayInterval":md.md_dayinterval,
                            "usage":md.md_usage
                            } for md in neuser.mddocobj]            
                        }
            return jsonify(doc_obj)
        else:
            user_obj = {"id":newuser.user_id,
                        "date":newuser.user_date,
                        "firstname":newuser.user_fname,
                        "lastname":newuser.user_lname,  
                        "email":newuser.user_email,
                        "role":newuser.user_role,
                        "phoneNo":newuser.user_phoneNo,
                        "genotype":newuser.user_genotype,
                        "bloodGroup":newuser.user_bloodgroup,
                        "medicalCondition":newuser.user_medCondition,
                        "medicalReminder":[{
                            "id":md.md_id, 
                            "date":md.md_date,
                            "drugName":md.md_drugname,
                            "drugDosage":md.md_drugunit,
                            "time":md.md_time,
                            "timeInterval":md.md_timeInterval,
                            "dayInterval":md.md_dayinterval,
                            "usage":md.md_usage
                            } for md in newuser.mdobj]            
                        }
            return jsonify(user_obj)


"""reminder"""
@app.route('/reminder/<id>/', methods=['GET'])
@cross_origin(origins=['*'])
def medreminder(id):
    loggedin = session.get('user')
    if loggedin==None:
        return redirect('/')
    
    if request.method=='GET':
        remd=Medreminder.query.filter_by(md_userid=id, md_usage='missed').all()
        remd_obj ={
            "medicalReminder":[{
                "id":md.md_id, 
                "date":md.md_date,
                "drugName":md.md_drugname,
                "drugDosage":md.md_drugunit,
                "time":md.md_time,
                "timeInterval":md.md_timeInterval,
                "dayInterval":md.md_dayinterval,
                "usage":md.md_usage
                } for md in remd]
        }
        return jsonify({"MedicalReminder":remd_obj, "id":loggedin})
    

"""setup reminder"""
@app.route('/set_reminder/', methods=['POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def set_reminder():
    loggedin = session.get('user')
    if loggedin==None:
        return redirect('/')
    
    if request.method=="POST":
        drugname = request.json['drugName']
        drugunit = request.json['drugDosage']
        time = request.json['time']
        timeInterval = request.json['timeInterval']
        dayInterval = request.json['dayInterval']
        usage = request.json['usage']
        userid = request.json['userid']
        
        if (drugname!="" or drugunit!="" or 
            time!="" or timeInterval!="" or
            dayInterval!="" or usage!="" or
            userid!=""):
        
            med=Medreminder(md_drugname=drugname, md_drugunit=drugunit,
                            md_time=time, md_timeInterval=timeInterval,
                            md_dayinterval=dayInterval, md_usage=usage,
                            md_userid=userid )
            db.session.add(med)
            db.session.commit()
            return jsonify({"msg":"Reminder set successfully", "id":loggedin})
        else:
            return jsonify({"msg":"One or more field is empty"})
    

"""report details """
@app.route('/report/detail/<id>/', methods=['GET', 'POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def report(id):
    loggedin = session.get('user')
    doctor = session.get('doctor')
    
    if loggedin!=None and doctor==None:
        return redirect('/')
    
    if request.method=='GET':
        rep = User.query.filter_by(user_id=id).all()
        rep_obj={"User":[{
            "id":user.user_id,
            "firstname":user.user_fname,
            "lastname":user.user_lname,  
            "email":user.user_email,
            "role":user.user_role,
            "phoneNo":user.user_phoneNo,
            "genotype":user.user_genotype,
            "bloodGroup":user.user_bloodgroup,
            "medicalCondition":user.user_medCondition,
            "medicalReminder":[{
                "id":md.md_id, 
                "date":md.md_date,
                "drugName":md.md_drugname,
                "drugDosage":md.md_drugunit,
                "time":md.md_time,
                "timeInterval":md.md_timeInterval,
                "dayInterval":md.md_dayinterval,
                "usage":md.md_usage
                } for md in user.mdobj],
            "MedicalReport":[{
                "id":mr.mr_id,
                "report": mr.mr_report,
                "date":mr.mr_date,
                } for mr in user.usermedrepobj],
            }for user in rep]}
        return jsonify(rep_obj)
            
    if request.method=='POST':
        report_text = request.json['report']
        userId = request.json['userId']
        
        if report_text !="" and userId != "":
            rept = Medreport(mr_report=report_text, mr_userid=userId, mr_docid=doctor)
            db.session.add(rept)
            db.session.commit()
            return jsonify({"msg":"report sent"})
        else:
            return jsonify({"msg":"One or more field is empty"})


"""Patients report """
@app.route('/list/allpatient/', methods=['GET', 'POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def all_patients():
    loggedin = session.get('user')
    doctor = session.get('doctor')
    
    if loggedin!=None and doctor==None:
        return redirect('/')
    if request.method=='GET':
        rep = User.query.filter_by(user_role='patient').all()
        rep_obj={"User":[{
            "id":user.user_id,
            "firstname":user.user_fname,
            "lastname":user.user_lname,
            "genotype":user.user_genotype,
            "bloodGroup":user.user_bloodgroup,
            "medicalCondition":user.user_medCondition
            }for user in rep]}
        return jsonify(rep_obj)
    

def check_due_reminders():
    current_time = datetime.now().strftime("%H:%M")
    remd=Medreminder.query.filter_by(md_usage="missed").all()
        
    for mdrem in remd:
        rem_time = mdrem.md_time
        print(f"this is database time {rem_time}")
        recurrence_intervaltime = mdrem.md_timeInterval
        recurrence_intervalday = mdrem.md_dayInterval
        mduserid = mdrem.md_userid
        scheduler.add_job(id="check_due_reminders", func=check_due_reminders, 
                  trigger="cron", days_of_week="mon-sun", hour=rem_time)
        if current_time == rem_time:
            send_notification(mduserid)

        # Check for recurrent reminders
        elif (recurrence_intervaltime > 0 and 
              current_time == get_next_recurrence(rem_time, recurrence_intervaltime)):
            send_notification(mduserid)
                

def send_notification(mduserid):
    commenter=Medreminder.query.filter_by(md_userid=mduserid, md_usage="missed").first()
    commenter_email=commenter.userobj2.user_email
    reminder_signal.send(app, comment=commenter, email=commenter_email)


def get_next_recurrence(reminder_time, recurrence_intervaltime):
    # Implement logic to calculate the next recurrence time based on the interval
    # For simplicity, you can add recurrence_interval hours to reminder_time
    return (datetime.strptime(reminder_time, "%H:%M") + 
            timedelta(hours=recurrence_intervaltime)).strftime("%H:%M")

@reminder_signal.connect
def send_email_alart(sender, comment, email,  recipients):
    subject = f"Medaidsync:Dosage Reminder"
    body = f"Hi {comment.userobj2.user_fname},\n\n Have you taken your drug dosage today \n You are to take {comment.md_drugunit} unit of {comment.md_drugname}\n\n Medaidsync Team"
    send_email_alert(subject, body, [email])


"updating reminder task (done)"
@app.route('/done_task/<id>/', methods=['POST'])
@csrf.exempt
@cross_origin(origins=['*'])
def done_task(id):
    loggedin = session.get('user')
    doctor = session.get('doctor')
    if loggedin==None and doctor==None:
        return redirect('/')
    if request.method=='POST':
        taken=request.json['taskUpdate']
        if taken == "taken":
            if taken!="":
                md=Medreminder.query.filter_by(md_id=id).first()
                md.md_usage=taken
                db.session.commit()
                return jsonify({"msg":"Task updated successfully"})
        elif taken == "skipped":
            if taken!="":
                md=Medreminder.query.filter_by(md_id=id).first()
                md.md_usage=taken
                db.session.commit()
                return jsonify({"msg":"Task updated successfully"})            
        else:
            return jsonify({"msg":"Task failed to update"})


"""medical history"""
@app.route('/medical_history/<id>/', methods=['GET'])
@cross_origin(origins=['*'])
def medhistory(id):
    loggedin = session.get('user')
    if loggedin==None:
        return redirect('/')
    
    if request.method=='GET':
        remd=Medreminder.query.filter_by(md_userid=id).all()
        remd_obj ={
            "History":[{
                "id":md.md_id, 
                "date":md.md_date,
                "drugName":md.md_drugname,
                "drugDosage":md.md_drugunit,
                "time":md.md_time,
                "timeInterval":md.md_timeInterval,
                "dayInterval":md.md_dayinterval,
                "usage":md.md_usage
                } for md in remd]
        }
        return jsonify({"MedicalHistory":remd_obj, "id":loggedin})