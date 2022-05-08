import sqlite3
from sqlite3 import Error

#change this path corresponding to where the db file is at
absolute_db_path = 'D:/Projects/transfer_app/'
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
    try:
        cursor.execute("select * from etudiant where email=:email and password=:password",{"email":email,"password":password})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        if res != None:
            student = {"matricule":res[0],
            "email":res[1],
            "password":res[2],
            "nom":res[3],
            "prenom":res[4],
            "telephone":res[5],
            "sexe":res[6],
            "date_naissance":res[7]}
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
    try:
        cursor.execute("select * from admin where email=:email and password=:password",{"email":email,"password":password})    
    except Error as e:
        print(e)
        return None
    else:
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



#orientation(id autoInc,id_fac,start,finish)
def addOrientation(id_fac:int,start:str,finish:str):
    try:
        cursor.execute('insert into orientation values (?,?,?,?)',(id_fac+1,id_fac,start,finish))
    except Error as e:
        print(e)
        print('orientation already added !')
        return None
    else:
        print('orientation set successfelly')
        con.commit()
        return 'ok'

def deleteOrientation(id_fac:int):
    try:
        cursor.execute('delete from orientation where id_fac =:id',{"id":id_fac})
    except Error as e:
        print(e)
        print('orientation does not exist')
        return None
    else:
        print('orientation deleted')
        con.commit()
        return 'ok'

def updateOrientationDeadline(id_fac:int,start:str,finish:str):
    try:
        cursor.execute('update orientation set start =:start ,finish =:finish where id_fac=:id',
        {'id':id_fac,'start':start,'finish':finish})
    except Error as e:
        print(e)
        return None
    else :
        con.commit()
        return 'ok'

def getOrientationDeadline(id_fac:int):
    try:
        cursor.execute('select * from orientation where id_fac=:id',{'id':id_fac})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        if res != None:
            deadline = {'id':res[0],'id_fac':res[1],'start':res[2],'finish':res[3]}
            return deadline
    return None

def getAllOrientations():
    return

#transfer(id autoInc,id_fac,start,finish)
def addTransfer(id_fac:int,start:str,finish:str):
    try:
        cursor.execute('insert into transfer values (?,?,?,?)',
        (id_fac+1,id_fac,start,finish))
    except Error as e:
        print(e)
        print('transfer already added !')
        return None
    else:
        print('transfer set successfelly')
        con.commit()
        return 'ok'

def deleteTransfer(id_fac:int):
    try:
        cursor.execute('delete from transfer where id_fac =:id',{"id":id_fac})
    except Error as e:
        print(e)
        print('transfer does not exist')
        return None
    else:
        print('transfer deleted')
        con.commit()
        return 'ok'

def updateTransferDeadline(id_fac:int,start:str,finish:str):
    try:
        cursor.execute('update transfer set start =:start ,finish =:finish where id_fac=:id',
        {'id':id_fac,'start':start,'finish':finish})
    except Error as e:
        print(e)
        return None
    else :
        con.commit()
        return 'ok'
    

def getTransferDeadline(id_fac:int):
    try:
        cursor.execute('select * from transfer where id_fac =:id',{'id':id_fac})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        if res != None:
            deadline = {'id':res[0],'id_fac':res[1],'start':res[2],'finish':res[3]}
            return deadline
    return None

def getAllTransfers():
    return



#transfer_request(matricule,id_transfer,moyen_bac,filiere_bac,niveau-etude,date_premier_insc,formation,univ_origin,conge_academic,etat,choix1...)
#conge academic 1 or 0 : if he has conge academic 1 else 0
#choix references id of specialite
def addTransferRequest(matricule:int, id_transfer:int, moyen_bac:float, filiere_bac:str, niveau_etude:str,
date_premier_insc:str, formation:str, univ_origin:str, conge_academic:int, etat:str, choix1:int, choix2:int, choix3:int, choix4:int):
    
    try:
        cursor.execute('insert into transfer_request values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(matricule,id_transfer,
        moyen_bac,filiere_bac,niveau_etude,date_premier_insc,formation,univ_origin,conge_academic,etat,choix1,
        choix2,choix3,choix4))
    except Exception as e:
        print(e)
        return None
    else:
        print('transfer request saved !')
        con.commit()
        return 'ok'
    

def updateTransferRequest(matricule:int, choix1:int, choix2:int, choix3:int, choix4:int):
    
    try:
        cursor.execute('update transfer_request set choix1=:choix1 ,choix2=:choix2 ,choix3=:choix3 ,choix4=:choix4 where matricule=:matricule',
        {'matricule':matricule,
        'choix1':choix1,
        'choix2':choix2,
        'choix3':choix3,
        'choix4':choix4,})
    except Exception as e:
        print(e)
        return None
    else:
        con.commit()
        print('transfer request updated')
        return 'ok'

def deleteTransferRequest(matricule:int):
    try:
        cursor.execute('delete from transfer_request where matricule=:matricule',{'matricule':matricule})
    except Exception as e:
        print(e)
        return None
    else:
        con.commit()
        print('transfer request deleted')
        return 'ok'


def setTransferRequestState(matricule:int, etat:str):
    try:
        cursor.execute('update transfer_request set etat=:etat where matricule=:matricule',{'matricule':matricule,'etat':etat})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('transfer request state updated')
        return 'ok'

def getTransferRequest(matricule:int):
    try:
        cursor.execute('select * from transfer_request where matricule=:matricule',{'matricule':matricule})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        transferRequest = {
            'matricule':res[0],
            'transfer_id':res[1]
        }
        return res
    
    
def getTransferRequests(id_transfer:int):
    return


#condition(id autoInc,id_fac , cond, type)
#type should be INTERN, EXTERN or ORIENTATION
def addCondition(id_fac:int,type:str, condition:str):
    return

def deleteCondition(id:int):
    return

def updateCondition(id:int,condition:str):
    return

def selectConditions(id_fac:int,type:str):
    return



#notification(id autoInc, matricule, message)
def addNewNotification(matricule, message):
    return

def getAllNotifications(matricule):
    return



#specialite
def getSpecialites(id_fac:int):
    return

def updateTransferPlaces(id_specialite:int, nbr_places:int):
    return

def updateOrientationPlaces(id_specialite:int, nbr_places:int):
    return

#   faculte(id autoInc,name)
#   departement(id autoInc,nom,id_fac)
def getFaculties():
    return

def getDepartements(id_fac:int):
    return
