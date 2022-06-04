import sqlite3
from sqlite3 import Error
from datetime import date

#change this path corresponding to where the db file is at


#absolute_db_path = 'C:/Users/pc-car/Desktop/project/transfer_orientations_app'
#database = absolute_db_path+'app_data.db'
#=======
#absolute_db_path = 'D:/Projects/transfer_app/'
#database = absolute_db_path+'app_data.db'
database = "/home/aymen/DEV/TpEdl/app_data.db"
con = sqlite3.connect(database, check_same_thread=False)
cursor = con.cursor()
READY = "ready"
SUSPENDED = "suspended"
REJECTED = "rejected"
ACCEPTED = "accepted" 

#Filliere de bac
MATH = "math"
MATH_TECHNIQUE = "math technique"
SCIENCE = "science"
LETTRE = "litterature et philosophe"
LANGUE = "langues"
ECONOMIE_GESTION = "gestion"

#conge academic
HAS_CONJE = 1
DONT_HAVE_CONJE =0

#condition types
INTERN = "intern"
EXTERN = "extern"
ORIENTATION = "orientation"

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
    
def studentPasswordReset(email:str, oldPass:str, newPass:str):
    res =studentLogIn(email,oldPass)
    if(res != None):
        try:
            cursor.execute("update etudiant set password=:newPass where email=:email and password=:oldPass",
            {'email':email,
            'oldPass':oldPass,
            'newPass':newPass})
        except Error as e:
            print(e)
            return None
        else:
            print('password reset success')
            con.commit()
            return 'ok'
    else:
        print('wrong password or email')
        return None


#admin(email,password,telephone,nom,prenom,id_dep,id_fac)
def adminLogIn(email:str):
    try:
        cursor.execute("select * from admin where email=:email",{"email":email})    
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

def adminPasswordReset(email:str, newPass:str):
    #res =adminLogIn(email,oldPass)
        try:
            cursor.execute("update admin set password=:newPass where email=:email",
            {'email':email,
            'newPass':newPass})
        except Error as e:
            print(e)
            return None
        else:
            print('password reset success')
            con.commit()
            return 'ok'
def UpdateAdminInfo(oldEmail, email, password, nom, prenom):
        try:
            qry = "update admin set email = ?, password = ?, nom = ?, prenom = ? where email = ?"
            cursor.execute(qry, (email, password, nom, prenom, oldEmail))
        except Error as e:
            print(e)
            return None
        else:
            print('Update Admin Info Done !')
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
    try:
        qry = "select matricule, id_orientation, etat from orientation_request where etat = ?"
        cursor.execute(qry, (SUSPENDED,))
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        return res

def getOrientationRequest(id_orientation):
    try:
        cursor.execute('select * from orientation_request where id_orientation=:id_orientation',{'id_orientation':id_orientation})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        OrientationRequest = {
            'matricule':res[0],
            'id_orientation':res[1],
            'niveau_etude':res[2],
            'date_premier_insc':res[3],
            'etat':res[4],
            'choix1':res[5],
            'choix2':res[6],
            'choix3':res[7],
            'choix4':res[8],
        }
        IdSpecialite = OrientationRequest['choix1']
        OrientationRequest['choix1'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = OrientationRequest['choix2']
        OrientationRequest['choix2'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = OrientationRequest['choix3']
        OrientationRequest['choix3'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = OrientationRequest['choix4']
        OrientationRequest['choix4'] = getSpecialiteInformation(IdSpecialite)['name']
        return OrientationRequest
def getOrientationRequests():
    try:
        cursor.execute('select * from orientation_request')
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        return res

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
    try:
        cursor.execute("select * from transfer")
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        transfers = []
        for transfer in res:
            t = {'id':transfer[0],
            'id_fac':transfer[1],
            'start':transfer[2],
            'finish':transfer[3]}
            transfers.append(t)
        return transfers



#transfer_request(matricule,id_transfer,moyen_bac,filiere_bac,niveau-etude,date_premier_insc,
# formation, univ_origin,conge_academic,etat,choix1...)
#conge academic 1 or 0 : if he has conge academic 1 else 0
#choix references id of specialite
def addTransferRequest(matricule:int, id_transfer:int, moyen_bac:float, filiere_bac:str, niveau_etude:str,
date_premier_insc:str, annee_bac:int, univ_origin:str, conge_academic:int, etat:str, choix1:int, choix2:int, choix3:int, choix4:int):
    
    try:
        cursor.execute('insert into transfer_request values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(matricule,id_transfer,
        moyen_bac,filiere_bac,niveau_etude,date_premier_insc,annee_bac,univ_origin,conge_academic,etat,choix1,
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

def setOrientationRequestState(matricule:int, etat:str):
    try:
        cursor.execute('update orientation_request set etat=:etat where matricule=:matricule',{'matricule':matricule,'etat':etat})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('transfer request state updated')
        return 'ok'

def getTransferRequest(id_transfer:int):
    try:
        cursor.execute('select * from transfer_request where id_transfer=:id_transfer',{'id_transfer':id_transfer})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        transferRequest = {
            'matricule':res[0],
            'transfer_id':res[1],
            'moyen_bac':res[2],
            'filiere_bac':res[3],
            'niveau_etude':res[4],
            'date_premier_insc':res[5],
            'annee_bac':res[6],
            'univ_origin':res[7],
            'conge_academic':res[8],
            'etat':res[9],
            'choix1':res[10],
            'choix2':res[11],
            'choix3':res[12],
            'choix4':res[13],
        }
        IdSpecialite = transferRequest['choix1']
        transferRequest['choix1'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = transferRequest['choix2']
        transferRequest['choix2'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = transferRequest['choix3']
        transferRequest['choix3'] = getSpecialiteInformation(IdSpecialite)['name']
        IdSpecialite = transferRequest['choix4']
        transferRequest['choix4'] = getSpecialiteInformation(IdSpecialite)['name']
        return transferRequest
    
    
def getAllTransferRequests(matricule:int):
    try:
        cursor.execute('select * from transfer_request where matricule=:matricule',{'matricule':matricule})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        transfer_requests = []
        for tran_req in res:
            transferRequest = {
            'matricule':tran_req[0],
            'transfer_id':tran_req[1],
            'moyen_bac':tran_req[2],
            'filiere_bac':tran_req[3],
            'niveau_etude':tran_req[4],
            'date_premier_insc':tran_req[5],
            'annee_bac':tran_req[6],
            'univ_origin':tran_req[7],
            'conge_academic':tran_req[8],
            'etat':tran_req[9],
            'choix1':tran_req[10],
            'choix2':tran_req[11],
            'choix3':tran_req[12],
            'choix4':tran_req[13],
        }
            transfer_requests.append(transferRequest)
        return transfer_requests

def getAllTransferRequestsOfStudent(matricule):
    try:
        cursor.execute(f'select * from transfer_request where matricule={matricule}')
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        transfer_requests = []
        for tran_req in res:
            transferRequest = {
            'matricule':tran_req[0],
            'transfer_id':tran_req[1],
            'moyen_bac':tran_req[2],
            'filiere_bac':tran_req[3],
            'niveau_etude':tran_req[4],
            'date_premier_insc':tran_req[5],
            'annee_bac':tran_req[6],
            'univ_origin':tran_req[7],
            'conge_academic':tran_req[8],
            'etat':tran_req[9],
            'choix1':tran_req[10],
            'choix2':tran_req[11],
            'choix3':tran_req[12],
            'choix4':tran_req[13],
        }
            transfer_requests.append(transferRequest)
        return transfer_requests


def getTransferRequests(type):
    try:
        if type == "interne":
            qry = 'select * from transfer_request where etat = ? and univ_origin = "constantine 2"'
            cursor.execute(qry, (SUSPENDED,))
        else:
            qry = 'select * from transfer_request where etat = ? and univ_origin != "constantine 2"'
            cursor.execute(qry, (SUSPENDED,))
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        return res
def getStudentInfo(matricule):
    try:
        cursor.execute('select * from etudiant where matricule=:matricule',{'matricule':matricule})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        return res
def getStudentInfoByEmail(email):
    try:
        cursor.execute('select * from etudiant where email=:email',{'email':email})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        return res
#condition(id autoInc,id_fac , cond, type)
#type should be INTERN, EXTERN or ORIENTATION
def addCondition(id, id_fac:int,type:str, condition:str):
    try:
        cursor.execute("insert into condition (id,id_fac,cond,type) values (?,?,?,?)",(id, id_fac,condition,type))
    except Error as e:
        print(e)
        return None
    else :
        con.commit()
        print('condition added !')
        return 'ok'


def deleteCondition(id:int):
    try:
        cursor.execute("delete from condition where id=:id",{'id':id})
    except Error as e:
        print(e)
        return None
    else :
        con.commit()
        print('condition deleted !')
        return 'ok'

def updateCondition(id:int,id_fac, type, cond:str):
    try:
        cursor.execute('update condition set cond=:cond, type=:type, id_fac=:id_fac where id=:id',{'id':id,'cond':cond, 'type':type, 'id_fac':id_fac})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print("condition updated")
        return 'ok'

def getConditions(id_fac:int,type:str):
    try:
        cursor.execute("select * from condition where id_fac=:id and type=:type",{'id':id_fac,'type':type})
    except Error as e:
        print(e)
        return None
    else:
        conditions =[]
        res = cursor.fetchall()
        for cond in res:
            c = {
                'id':cond[0],
                'id_fac':cond[1],
                'cond':cond[2],
                'type':cond[3]
            }
            conditions.append(c)
        return conditions
def getAllConditions(idFac):
    try:
        cursor.execute("select * from condition where id_fac = {idFac}".format(idFac = idFac))
    except Error as e:
        print(e)
        return None
    else:
        conditions =[]
        res = cursor.fetchall()
        for cond in res:
            c = {
                'id':cond[0],
                'id_fac':cond[1],
                'cond':cond[2],
                'type':cond[3]
            }
            conditions.append(c)
            ListOfFaculties = getFaculties()
            for item in ListOfFaculties:
                if item[0] == c['id_fac']: c['id_fac'] = item[1] 
        return conditions
def getAllConditionsOfFacults(type):
    try:
        cursor.execute("select * from condition where type=:type",{'type':type})
    except Error as e:
        print(e)
        return None
    else:
        conditions =[]
        res = cursor.fetchall()
        for cond in res:
            c = {
                'id':cond[0],
                'id_fac':cond[1],
                'cond':cond[2],
                'type':cond[3]
            }
            ListOfFaculties = getFaculties()
            for item in ListOfFaculties:
                if item[0] == c['id_fac']: c['id_fac'] = item[1] 
            conditions.append(c)
        return conditions


#notification(id autoInc, matricule, message)
def addNewNotification(matricule:int, message:str):
    try:
        cursor.execute('insert into notification (matricule,message) values(?,?)',(matricule,message))
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('notification added')
        return 'ok'
def deleteNotification(id:int):
    try:
        cursor.execute("delete from notification where id=:id",{'id':id})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('notification deleted ')
        return 'ok'

def getAllNotifications(matricule:int):
    try:
        cursor.execute('select * from notification where matricule=:matricule',{'matricule':matricule})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        notifications = []
        for notification in res:
            n ={
                'id':notification[0],
                'matricule':notification[1],
                'message':notification[2]
            }
            notifications.append(n)
        return notifications



#specialite(id autoInc, name, niveau, orientation_places, transfer_places, id_dep, id_fac)
def getSpecialites(id_fac:int):
    try:
        cursor.execute("select * from specialite where id_fac=:id",{'id':id_fac})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        specialities = []
        for specialitie in res:
            s = {
                'id':specialitie[0],
                'name':specialitie[1],
                'niveau':specialitie[2],
                'orientation_places':specialitie[3],
                'transfer_places':specialitie[4],
                'id_dep':specialitie[5],
                'id_fac':specialitie[6]
            }
            specialities.append(s)
        return specialities

def getAllSpecialites():
    try:
        cursor.execute("select id, name from specialite")
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        return res

def getSpecialiteInformation(id_specialite:int):
    try:
        cursor.execute('select * from specialite where id=:id',{'id':id_specialite})
    except Error as e:
        print(e)
        return None
    else:
        specialitie = cursor.fetchone()
        return {
                'id':specialitie[0],
                'name':specialitie[1],
                'niveau':specialitie[2],
                'orientation_places':specialitie[3],
                'transfer_places':specialitie[4],
                'id_dep':specialitie[5],
                'id_fac':specialitie[6]
            }

def updateTransferPlaces(id_specialite:int, nbr_places:int):
    try:
        cursor.execute("update specialite set transfer_places=:nbr where id=:id",{'id':id_specialite,'nbr':nbr_places})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('transfer places updated !')
        return 'ok'    


def updateOrientationPlaces(id_specialite:int, nbr_places:int):
    try:
        cursor.execute("update specialite set orientation_places=:nbr where id=:id",{'id':id_specialite,'nbr':nbr_places})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('orientation places updated !')
        return 'ok'    


#   faculte(id autoInc,name)
#   departement(id autoInc,nom,id_fac)
def getFaculties():
    try:
        cursor.execute("select * from faculte")
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        return res

def getDepartements(id_fac:int):
    return
def getLastIdOfTable(tableName):
    try:
        if tableName != "transfer_request" : cursor.execute("SELECT MAX(id) FROM {tableName}".format(tableName = tableName))
        cursor.execute("SELECT MAX(id_transfer) FROM {tableName}".format(tableName = tableName))
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchone()
        return res[0]

def UpdateStudentProfile(email, password, nom, prenom, id):
    try:
        qry = "update etudiant set email = ?, password = ?, nom = ?, prenom = ? where matricule = ?"
        cursor.execute(qry, (email, password, nom, prenom, id))
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('Student info updated !')
        return 'ok' 
def DeleteAdmin(email):
    try:
        cursor.execute("delete from admin where email = :email;", {'email': email})
    except Error as e:
        print(e)
        return None
    else:
        con.commit()
        print('admin is deleted !')
        return 'ok' 

def getMoyensBac(id_fac:int):
    try:
        cursor.execute('select * from moyennes where id_fac=:id',{'id':id_fac})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        moyens = []
        for moy in res:
            s = {
                'id_fac':moy[0],
                'filliere_bac':moy[1],
                'annee':moy[2],
                'moyen':moy[3],
                'priority':moy[4],  
            }
            moyens.append(s)
        return moyens

class TransferRequest:
    def __init__(self,matricule,transfer_id,moyen_bac,filliere_bac,niveau_etude,date_premier_insc,annee_bac,
    univ_origin,conge_academic,etat,choix1,choix2,choix3,choix4):
        self.matricule = matricule
        self.transfer_id = transfer_id
        self.moyen_bac = moyen_bac
        self. filliere_bac = filliere_bac
        self.niveau_etude = niveau_etude
        self.date_premier_insc = date_premier_insc
        self.annee_bac = annee_bac
        self.univ_origin = univ_origin
        self.conge_academic = conge_academic
        self.etat = etat
        self.choix1 = choix1
        self.choix2 = choix2
        self.choix3 = choix3
        self.choix4 = choix4
    
    def __repr__(self):
        return '{'+str(self.matricule)+','+str(self.transfer_id)+','+str(self.moyen_bac)+','+str(self.annee_bac)+','+self.etat+','+str(self.choix1)+','+str(self.choix2)+'}'

def selectAllTransferRequests(id_transfer:int):
    try:
        cursor.execute('select * from transfer_request where id_transfer=:id_transfer',{'id_transfer':id_transfer})
    except Error as e:
        print(e)
        return None
    else:
        res = cursor.fetchall()
        transfer_requests = []
        for tran_req in res:
            request = TransferRequest(tran_req[0],tran_req[1],tran_req[2],tran_req[3],tran_req[4],
            tran_req[5],tran_req[6],tran_req[7],tran_req[8],tran_req[9],tran_req[10],tran_req[11],tran_req[12]
            ,tran_req[13])
            transferRequest = {
            'matricule':tran_req[0],
            'transfer_id':tran_req[1],
            'moyen_bac':tran_req[2],
            'filiere_bac':tran_req[3],
            'niveau_etude':tran_req[4],
            'date_premier_insc':tran_req[5],
            'annee_bac':tran_req[6],
            'univ_origin':tran_req[7],
            'conge_academic':tran_req[8],
            'etat':tran_req[9],
            'choix1':tran_req[10],
            'choix2':tran_req[11],
            'choix3':tran_req[12],
            'choix4':tran_req[13],
            }
            transfer_requests.append(request)
        return transfer_requests

def checkBacValidity(requests,specialities):
    currentYear = date.today().year
    rejected_requests = []
    ready_requests = []
    for req in requests:
        if req.etat == READY:
            annee_bac = req.annee_bac
            required_years = 3
            for spec in specialities:
                if spec["id"] == req.choix1:
                    niveau = spec["niveau"]
                    if niveau =="L2":
                        required_years = 2
                    elif niveau == "L3":
                        required_years = 1

            available_years = 5-(currentYear - annee_bac)
            if req.conge_academic == 1:
                available_years += 1
            if available_years >= required_years:
                ready_requests.append(req)
                req.etat = READY
            else:
                rejected_requests.append(req)
                req.etat = REJECTED
        else:
            req.etat = REJECTED
            rejected_requests.append(req)

    return {"rejected":rejected_requests,"ready":ready_requests}

def sortRequestByMoyen(requests):
    return sorted(requests,key=lambda x: x.moyen_bac, reverse=True)

def getMoyenAndPriority(filliere, annee, moyens):
    for moy in moyens:
        if filliere == moy["filliere_bac"] and annee == moy["annee"]:
            return {'moyen':moy["moyen"],'priority':moy["priority"]}
    return None

def traiterTransferRequests(id_fac:int):
    transfer = getTransferDeadline(id_fac)
    #TODO check if the transfer in not null
    specialites = getSpecialites(id_fac)
    moyens = getMoyensBac(id_fac)
    transfer_requests = selectAllTransferRequests(transfer["id"])
    
    accepted_requests = []

    res = checkBacValidity(transfer_requests, specialites)
    rejected_requests = res["rejected"]
    ready = res["ready"]

    ready = sortRequestByMoyen(ready)
    print(ready)
    for i in range(1,4):
        priority = i
        for request in ready:
            if request.etat == READY:
                moyAndPrioOfAcceptance = getMoyenAndPriority(request.filliere_bac,request.annee_bac,moyens)
           
            #if is null that filliere has no right in this specialite
                if moyAndPrioOfAcceptance == None:
                    request.etat = REJECTED
                    rejected_requests.append(request)
                    print("no right for filliere")
                    #ready.remove(request)
                #remove the request from the ready list TODO
                else:
                    min_moy = moyAndPrioOfAcceptance["moyen"]
                    his_priority = moyAndPrioOfAcceptance["priority"]
                    print(request)
                    print(priority)
                    print(his_priority)
                    if his_priority <= priority:
                        if request.moyen_bac >= min_moy:
                            first_choice_index = None
                            seconde_choice_index = None
                            third_choice_index = None
                            fourth_choice_index = None
                            for k,specialite in enumerate(specialites):
                                if request.choix1 == specialite["id"]:
                                    first_choice_index = k
                                elif request.choix2 == specialite["id"]:
                                    seconde_choice_index = k
                                elif request.choix3 == specialite["id"]:
                                    third_choice_index = k
                                elif request.choix4 == specialite["id"]:
                                    fourth_choice_index = k

                            if specialites[first_choice_index]["transfer_places"]>0:
                                request.choix2 = None
                                request.choix3 = None
                                request.choix4 = None
                                specialites[first_choice_index]["transfer_places"] -=1
                                request.etat = ACCEPTED
                                accepted_requests.append(request)
                                #ready.remove(request)
                            elif specialites[seconde_choice_index]["transfer_places"] >0 :
                                request.choix1 = None
                                request.choix3 = None
                                request.choix4 = None
                                specialites[seconde_choice_index]["transfer_places"] -=1
                                request.etat = ACCEPTED
                                accepted_requests.append(request)
                                #ready.remove(request)
                            elif specialites[third_choice_index]["transfer_places"] >0 :
                                request.choix2 = None
                                request.choix1 = None
                                request.choix4 = None
                                specialites[third_choice_index]["transfer_places"] -=1
                                request.etat = ACCEPTED
                                accepted_requests.append(request)
                               # ready.remove(request)
                            elif specialites[fourth_choice_index]["transfer_places"] >0 :
                                request.choix2 = None
                                request.choix3 = None
                                request.choix1 = None
                                specialites[fourth_choice_index]["transfer_places"] -=1
                                request.etat = ACCEPTED
                                accepted_requests.append(request)
                               # ready.remove(request)
                            else:
                                request.etat = REJECTED
                                rejected_requests.append(request)
                               # ready.remove(request)
                        else:
                            print("min moy")
                            request.etat = REJECTED
                            rejected_requests.append(request)
                           # ready.remove(request)
        
                        

    return {'accepted':accepted_requests,'rejected':rejected_requests}




if __name__ == "__main__":
    print(getStudentInfoByEmail('salahe@gmail.com'))
    
    


#print(studentLogIn("mohamed@gmail.com","mohamed"))
#addTransferRequest(1818,2,12.5,"math","l1","2018","sdf","sdf",0,SUSPENDED,1,1,1,1)
#studentSignUp(1819,"ali@gmail.com","ali","ali","ali","05458796","male","2000")
#addTransferRequest(1819,2,14,"sience","l1","2018","sdf","sdf",1,SUSPENDED,1,1,1,1)
#print(getAllTransferRequests(2))

#studentPasswordReset("mohamed@gmail.com","mohamed3","mohamed4")
#print(studentLogIn("mohamed@gmail.com","mohamed3"))
#adminPasswordReset("admin@gmail.com","admin2","admin")

#closeConnection()
