
import email
from unicodedata import category
from flask import Flask, render_template, redirect, request, url_for, session
from flask_session import Session
from flask_bootstrap import Bootstrap
from sqlalchemy import null
import database_api as db
from flask_mail import Mail, Message
from threading import Thread
app = Flask(__name__)
#email configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "glm467536@gmail.com"
app.config['MAIL_PASSWORD'] = "glm467536** *"
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[transfer & orientations app]'
app.config['FLASKY_MAIL_SENDER'] = 'transfer & orientations app Admin <glm467536@gmail.com>'
app.config['FLASKY_ADMIN'] = "glm467536@gmail.com"
mail = Mail(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

bootstrap = Bootstrap(app)
mail = Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('admin/500.html'), 500


@app.route('/', methods = ["POST", "GET"])
def index():
    return render_template('index.html')

@app.route('/connecter', methods = ["POST", "GET"])
def login():
    #get info from the form 
    if request.method == "POST":
        email = request.form["email"]
        #save email in user session
        session["email"] = email
        password = request.form["password"]
        #fetch from db
        if password == "admin":
            if db.adminLogIn(email, password) != None:
                db.closeConnection()
                return redirect(url_for('index_admin'))  
            else:
                return render_template('login.html')
        else:
            #Student dashboard
            pass
    return render_template('login.html')


@app.route('/admin', methods = ["POST", "GET"])
def index_admin():
    if session.get("email") != None:
        return render_template('admin/index.html')
    return redirect(url_for('login'))


@app.route('/admin/transfer_interne')
def transferInterne():
     type = "interne"
     if session.get("email") != None:
         if db.getTransferRequests(type) != None:
             db.closeConnection()
             return render_template('admin/transfer_interne.html', data = db.getTransferRequests(type))
         else:
             return render_template('admin/transfer_interne.html')
     return redirect(url_for('login'))



@app.route('/admin/transfer_externe')
def transferExterne():
    type = "externe"
    if session.get("email") != None:
         if db.getTransferRequests(type) != None:
            db.closeConnection()
            return render_template('admin/transfer_externe.html', data = db.getTransferRequests(type))
         else:
             return render_template('admin/transfer_externe.html')
    return redirect(url_for('login'))
    


@app.route('/admin/orientations')
def orientations():
    return render_template('admin/orientations.html')


@app.route('/admin/demande_details/<id_transfer>/')
def transferInterneDetails(id_transfer):
    if session.get("email") != None:
        id_transfer = int(id_transfer)
        transferInfo = db.getTransferRequest(id_transfer)
        matricule = transferInfo['matricule']
        StudentInfo = db.getStudentInfo(matricule)
        db.closeConnection()
        return render_template('admin/demande_details.html', transferInfo = transferInfo, StudentInfo = StudentInfo)
    return redirect(url_for('login'))


@app.route('/admin/conditions')
def condition():
    if session.get("email") != None:
        type = 'orientation'
        conditions = db.getAllConditions(type)
        return render_template('admin/conditions.html', conditions = conditions)
    return redirect(url_for('login'))
    


@app.route('/admin/ajouter_condition')
def ajouter_condition():
    if session.get("email") != None:
        return render_template('admin/ajouter_condition.html')
    return redirect(url_for('login'))


@app.route('/admin/conditions/modifier_condition/<IdCondition>', methods = ["POST", "GET"])
def modifier_condition(IdCondition):
    if session.get("email") != None:
        if request.method == "POST":
            category = request.form.get('category')
            faculty = request.form.get('faculty')
            if faculty == "Nouvelle Technologies d'Informations et Communication": id_fac = 1
            elif faculty == "Sience Humain et Social": id_fac = 2
            elif faculty == "Economie": id_fac = 3
            elif faculty == "Sience des Activites Sportives" : id_fac = 4
            elif faculty == "Bibliotheconomie": id_fac = 5
            elif faculty == "Psychologie":id_fac = 6
            description = request.form.get('description')
            db.updateCondition(int(IdCondition), id_fac, category, description)
            db.closeConnection()
    return render_template('admin/modifier_condition.html', IdCondition = IdCondition)
@app.route('/admin/conditions/modifier_condition/<IdCondition>/delete')
def DeleteCondition(IdCondition):
    if db.deleteCondition(IdCondition) != None:
        redirect(url_for('condition', IdCondition = IdCondition))
    redirect(url_for('condition', IdCondition = IdCondition))

@app.route('/admin/profile')
def profile():
    return render_template('admin/profile.html')


@app.route('/admin/parametres')
def parametres():
    return render_template('admin/parametres.html')


@app.route('/admin/transfer_interne/<matricule>/<State>')
def updateTransferEtat(matricule, State):
    #update Transfer Request Etat in db
    db.setTransferRequestState(matricule, State)
    StudentInfo = db.getStudentInfo(matricule)
    StudentEmail = StudentInfo[1]
    db.closeConnection()
    #send email to Student
    send_email(StudentEmail, 'Transfer State','mail/TransferState', user=StudentEmail, State = State)
    print("sending email to " + StudentEmail)
    return "ok"
@app.route('/etudiant')
def Student_index():
    return render_template('etudiant/index.html')

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@app.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if request.method == "POST":
        email = request.form["email"]
        send_email(email, 'Reset Your Password','mail/reset_password', user=email)
        print("sending email to " + email)
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/newPassword', methods=['GET', 'POST'])
def newPassword():
    if request.method == "POST":
        newPassword = request.form["password"]
        #call update password from the db api
        db.adminPasswordReset(session.get("email"), newPassword)
        db.closeConnection()
        return redirect(url_for('login'))
    return render_template('newPassword.html')

if __name__ == ("__main__"):
    app.run(debug=True)
