import sqlite3
from sqlite3 import Error

#change this path corresponding to where the db file is at
absolute_db_path = 'D:/Projects/transfer_management_app/transfer_orientations_app/'
database = absolute_db_path+'app_data.db'
con = sqlite3.connect(database)
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
def studentLogIn(email:str,password:str):
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

def studentSignUp(matricule:int, email:str, password:str, nom:str, prenom:str, telephone:str ,sexe:str, date_naissance:str):
    try:
        cursor.execute("insert into etudiant values (?,?,?,?,?,?,?,?)",(matricule,email,password,nom,prenom,telephone,sexe,date_naissance))
    except Error as e:
        print(e)
        print('student already exists')
        return None
    else:
        print('student signed up')
        con.commit()
        return 'ok'
    


#admin(email,password,telephone,nom,prenom,id_dep,id_fac)
def adminLogIn(email:str, password:str):
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


def adminSignUp(email:str, password:str, nom:str, prenom:str, telephone:str, id_dep:int, id_fac:int):
    try:
        cursor.execute('insert into admin values (?,?,?,?,?,?,?)',(email,password,telephone,nom,prenom,id_dep,id_fac))
    except Error as e:
        print(e)
        print("admin already exists")
        return None
    else:
        print("admin signed up successfully")
        con.commit()
        return 'ok'



#orientation_deadline(id autoInc,start,finish)
def setOrientationDeadline(start:str,finish:str):
    try:
        cursor.execute('insert into orientation_deadline values (?,?,?)',(1,start,finish))
    except Error as e:
        print(e)
        print('orientation deadline already set !')
        return None
    else:
        print('orientation deadline set successfelly')
        con.commit()
        return 'ok'

def deleteOrientationDeadline():
    try:
        cursor.execute('delete from orientation_deadline where id =:id',{"id":1})
    except Error as e:
        print(e)
        print('orientation deadline does not exist')
        return None
    else:
        print('orientation deadline deleted')
        con.commit()
        return 'ok'

def updateOrientationDeadline(start:str,finish:str):
    return

def getOrientationDeadline():
    return



#transfer_deadline(id autoInc,start,finish)
def setTransferDeadline(start:str,finish:str):
    try:
        cursor.execute('insert into transfer_deadline values (?,?,?)',(1,start,finish))
    except Error as e:
        print(e)
        print('transfer deadline already set !')
        return None
    else:
        print('transfer deadline set successfelly')
        con.commit()
        return 'ok'

def deleteTransferDeadline():
    try:
        cursor.execute('delete from transfer_deadline where id =:id',{"id":1})
    except Error as e:
        print(e)
        print('transfer deadline does not exist')
        return None
    else:
        print('transfer deadline deleted')
        con.commit()
        return 'ok'

def updateTransferDeadline(start:str,finish:str):
    try:
        cursor.execute('update transfer_deadline set start =:start ,finish =:finish',{'start':start,'finish':finish})
    except Error as e:
        print(e)
        return None
    else :
        con.commit()
        return 'ok'
    

def getTransferDeadline():
    cursor.execute('select * from transfer_deadline where id =1')
    res = cursor.fetchone()
    if res != None:
        deadline = {'id':res[0],'start':res[1],'finish':res[2]}
        return deadline
    return None


#transfer(matricule,id_transfer,moyen_bac,filiere_bac,niveau-etude,date_premier_insc,formation,univ_origin,conge_academic,etat,choix1...)
def addTransferRequest():
    return

def updateTransferRequest():
    return

def deleteTransferRequest():
    return

def getTransferRequest(matricule:int):
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

