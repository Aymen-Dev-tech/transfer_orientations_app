
# from crypt import methods
import email
from unicodedata import category
from flask import Flask, render_template, redirect, request, url_for, session, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap
from sqlalchemy import null
import database_api as db
from flask_mail import Mail, Message
from threading import Thread
from werkzeug.utils import secure_filename
import os
from glob import glob
from io import BytesIO
from zipfile import ZipFile
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


@app.route('/etudiant/ajouter_demande_orientation')
def ajouter_demande_orientation():
    return render_template('etudiant/ajouter_demande_orientation.html')


@app.route('/etudiant/ajouter_demende_transfer_interne')
def ajouter_demande_transfer_interne():
    return render_template('etudiant/ajouter_demende_transfer_interne.html')


@app.route('/etudiant/ajouter_demende_transfer_externe')
def ajouter_demande_transfer_externe():
    return render_template('etudiant/ajouter_demende_transfer_externe.html')


@app.route('/connecter', methods = ["POST", "GET"])
def login():
    #get info from the form 
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        #fetch from db
        if db.adminLogIn(email) != None:
            db.closeConnection()
            #save email in user session
            session["email"] = email
            return redirect(url_for('index_admin'))  
        elif db.studentLogIn(email, password) != None:
            db.closeConnection()
            session["email"] = email
            return redirect(url_for('Student_index')) 
        else:
            return render_template('login.html')
    return render_template('login.html')
        
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/admin')
def index_admin():
    if session.get("email") != None:
        numberOfTransferInterne = len(db.getTransferRequests('interne'))
        numberOfTransferExterne = len(db.getTransferRequests("externe"))
        AdminInfo = db.adminLogIn(session.get("email"))
        idFac = AdminInfo['id_fac']
        numberOfConditions = len(db.getAllConditions(idFac))
        return render_template('admin/index.html', numberOfTransferInterne = numberOfTransferInterne, numberOfTransferExterne = numberOfTransferExterne, numberOfConditions = numberOfConditions)
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
        AdminInfo = db.adminLogIn(session.get("email"))
        idFac = AdminInfo['id_fac']
        conditions = db.getAllConditions(idFac)
        return render_template('admin/conditions.html', conditions = conditions)
    return redirect(url_for('login'))
    


@app.route('/admin/ajouter_condition', methods = ['POST', 'GET'])
def ajouter_condition():
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
            lastId = db.getLastIdOfTable("condition")
            if lastId == None:
                db.addCondition(1, id_fac, category, description)
            lastId+=1
            db.addCondition(lastId, id_fac, category, description)
            db.closeConnection()
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
    return redirect(url_for('login'))

@app.route('/admin/conditions/modifier_condition/<IdCondition>/delete')
def DeleteCondition(IdCondition):
    if session.get("email") != None:
        if db.deleteCondition(IdCondition) != None:
            return redirect(url_for('condition'))
        return redirect(url_for('condition'))
    return redirect(url_for('login'))

@app.route('/admin/profile')
def profile():
    if session.get("email") != None:
        return render_template('admin/profile.html')
    return redirect(url_for('login'))

@app.route('/admin/profile/Edit', methods = ["POST", "GET"])
def EditProfile():
    if session.get("email") != None:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/admin/profile/Add', methods = ["POST", "GET"])
def AddAdmin():
    if session.get("email") != None:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            tel = request.form.get('telephone')
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            faculty = request.form.get('faculty')
            if faculty == "Nouvelle Technologies d'Informations et Communication": id_fac = 1
            elif faculty == "Sience Humain et Social": id_fac = 2
            elif faculty == "Economie": id_fac = 3
            elif faculty == "Sience des Activites Sportives" : id_fac = 4
            elif faculty == "Bibliotheconomie": id_fac = 5
            elif faculty == "Psychologie":id_fac = 6
            departement = request.form.get('departement')
            if departement == "Math et Informatique": id_dep = 1
            elif departement == "Technologies des Logiciel et de System d'Information": id_dep = 2
            elif departement == "Informatique Fondamental et ses Applications": id_dep = 3
            elif departement == "Sience Humain": id_dep = 4
            elif departement == "Sience Social": id_dep = 5
            elif departement == "Sience de Psychologie": id_dep = 6
            elif departement == "Orthoponie": id_dep = 7
            elif departement == "Sience d'Education": id_dep = 8
            elif departement == "Tronc Commun Economie": id_dep = 9
            elif departement == "Science Economique": id_dep = 10
            elif departement == "Finance et Comptabilite": id_dep = 11
            elif departement == "Science de Gestion": id_dep = 12
            elif departement == "Science Commerciale": id_dep = 13
            elif departement == "Tronc Commun Sport": id_dep = 14
            elif departement == "Education et Motricite": id_dep = 15
            elif departement == "Entrainement Sportif et competitif": id_dep = 16
            elif departement == "Tronc Commun Bibliotheconomie": id_dep = 17
            elif departement == "Archive": id_dep = 18
            elif departement == "Bibliotheque": id_dep = 19
            db.adminSignUp(email, password, nom, prenom, tel, id_fac, id_dep)
            db.closeConnection()

        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/admin/profile/Delete', methods = ["POST", "GET"])
def DeleteAdmin():
    if session.get("email") != None:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/admin/parametres')
def parametres():
    return render_template('admin/parametres.html')


@app.route('/admin/transfer_interne/<matricule>/<State>')
def updateTransferEtat(matricule, State):
    #update Transfer Request Etat in db
    db.setTransferRequestState(int(matricule), State)
    StudentInfo = db.getStudentInfo(matricule)
    StudentEmail = StudentInfo[1]
    db.closeConnection()
    #send email to Student
    send_email(StudentEmail, 'Transfer State','mail/TransferState', user=StudentEmail, State = State)
    print("sending email to " + StudentEmail)
    return redirect(url_for('transferInterne'))
@app.route('/etudiant')
def Student_index():
    if session.get("email") != None:
        return render_template('etudiant/index.html')
    return redirect(url_for('login'))
@app.route('/etudiant/profile')
def studentProfile():
    if session.get("email") != None:    
        return render_template('etudiant/profile.html')
    return redirect(url_for('login'))
@app.route('/etudiant/upload', methods = ["POST", "GET"])
def upload():
    if session.get("email") != None:
        if request.method == "POST":
            files = request.files.getlist('files')
            # if user does not select file, browser also
            # submit a empty part without filename
            if files[0].filename == '':
                print('no files')
                return redirect(request.url)
            else:
                for f in files:
                    StudentInfo = db.getStudentInfoByEmail(session.get("email"))
                    app.config['UPLOAD_FOLDER'] = CreateFolder(str(StudentInfo[0]))
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) # this will secure the file
                    return 'file uploaded successfully'
        return render_template('etudiant/uploadingForm.html')
    return redirect(url_for('login'))

#create folders for each student 
def CreateFolder(StudentID):
    upload_folder = f"Docs/{StudentID}"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return upload_folder
@app.route('/admin/transfer_interne/<matricule>/')
def downloadDocs(matricule):
    files = GetAllStudentDocs(matricule)
    print("send the file")
    return send_file(
        files,
        as_attachment=True,
        download_name=f'{matricule}.zip'
    )
def GetAllStudentDocs(matricule):
    #change this to the absolute path of Docs Folder without removing matricule
    target = f'/home/aymen/DEV/TpEdl/Docs/{matricule}/*'
    stream = BytesIO()
    #zip all student docs
    with ZipFile(stream, 'w') as zf:
        for file in glob(target):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    return stream

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
