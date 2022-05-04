import sqlite3
con = sqlite3.connect('D:/Projects/transfer_management_app/transfer_orientations_app/app_data.db')
cursor = con.cursor()

READY = "ready"
SUSPENDED = "suspended"
REJECTED = "rejected"
ACCEPTED = "accepted"

def closeConnection():
    print("closing connection...")
    con.close


print("test running...")

#these should be predifined in the database
#   faculte(id autoInc,name)
#   departement(id autoInc,nom,id_fac)
#   specialite(id autoInc, name, niveau, orientation_places, transfer_places, id_dep, id_fac)



#orientation(matricule,id_orientation,niveau-etude,date_premier_insc,etat,choix1...)


#etudiant(matricule,email,password,nom,prenom,telephone,sexe,date_naissance)
def studentLogIn(email,password):
    cursor.execute("select * from etudiant where email=:email and password=:password",{"email":email,"password":password})
    res = cursor.fetchone()
    if res != None:
        student = {"matricule":res[0],
        "email":res[1],
        "password":res[2],
        "nom":res[3],
        "prenom":res[4],
        "telephone":res[5],
        "sexe":res[6],
        "date_naissance":res[7],}
        return student
    return None

def studentSignUp(matricule, email, password, nom, prenom, telephone ,sexe, date_naissance):
    try:
        cursor.execute("insert into etudiant values (?,?,?,?,?,?,?,?)",(matricule,email,password,nom,prenom,telephone,sexe,date_naissance))
    except:
        print('student already exists')
        return None
    else:
        print('student signed up')
        con.commit()
        return 'ok'
    


#admin(email,password,telephone,nom,prenom,id_dep,id_fac)
def adminLogIn(email, password):
    cursor.execute("select * from admin where email=:email and password=:password",{"email":email,"password":password})    
    res = cursor.fetchone()
    if res != None:
        admin = {"email":res[0],
        "password":res[1],
        "telephone":res[2],
        "nom":res[3],
        "prenom":res[4],
        "id_dep":res[5],
        "id_fac":res[6]}
        return admin
    
    return None


def adminSignUp(email, password, nom, prenom, telephone, id_dep, id_fac):
    try:
        cursor.execute('insert into admin values (?,?,?,?,?,?,?)',(email,password,telephone,nom,prenom,id_dep,id_fac))
    except:
        print("admin already exists")
        return None
    else:
        print("admin signed up successfully")
        con.commit()
        return 'ok'



#orientation_deadline(id autoInc,start,finish)
def setOrientationDeadline(start,finish):
    try:
        cursor.execute('insert into orientation_deadline values (?,?,?)',(1,start,finish))
    except:
        print('orientation deadline already set !')
        return None
    else:
        print('orientation deadline set successfelly')
        con.commit()
        return 'ok'

def deleteOrientationDeadline():
    try:
        cursor.execute('delete from orientation_deadline where id =:id',{"id":1})
    except:
        print('orientation deadline does not exist')
        return None
    else:
        print('orientation deadline deleted')
        con.commit()
        return 'ok'

def updateOrientationDeadline(start,finish):
    return

def getOrientationDeadline():
    return



#transfer_deadline(id autoInc,start,finish)
def setTransferDeadline(start,finish):
    try:
        cursor.execute('insert into transfer_deadline values (?,?,?)',(1,start,finish))
    except:
        print('transfer deadline already set !')
        return None
    else:
        print('transfer deadline set successfelly')
        con.commit()
        return 'ok'

def deleteTransferDeadline():
    try:
        cursor.execute('delete from transfer_deadline where id =:id',{"id":1})
    except:
        print('transfer deadline does not exist')
        return None
    else:
        print('transfer deadline deleted')
        con.commit()
        return 'ok'
def updateTransferDeadline(start,finish):
    return

def getTransferDeadline():
    return


#transfer(matricule,id_transfer,moyen_bac,filiere_bac,niveau-etude,date_premier_insc,formation,univ_origin,conge_academic,etat,choix1...)
def addTransferRequest():
    return

def updateTransferRequest():
    return

def deleteTransferRequest():
    return

def getTransferRequest(matricule):
    return

def setTransferRequestState():
    return



#condition(id autoInc, cond, type)
#type should be INTERN, EXTERN or ORIENTATION
def addCondition(type, condition):
    return

def deleteCondition(id):
    return

def updateCondition(id,condition):
    return

def selectConditions(type):
    return


#notification(id autoInc, matricule, message)
def addNewNotification(matricule, message):
    return

def getAllNotifications(matricule):
    return

