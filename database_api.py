import sqlite3
from sqlite3 import Error

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
            'formation':res[6],
            'univ_origin':res[7],
            'conge_academic':res[8],
            'etat':res[9],
            'choix1':res[10],
            'choix2':res[11],
            'choix3':res[12],
            'choix4':res[13],
        }
        return transferRequest
    
    
def getAllTransferRequests(id_transfer:int):
    try:
        cursor.execute('select * from transfer_request where id_transfer=:id_transfer',{'id_transfer':id_transfer})
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
            'formation':tran_req[6],
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
            'formation':tran_req[6],
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
            cursor.execute('select * from transfer_request where etat = "En attendre" and univ_origin = "constantine2"')
        else:
            cursor.execute('select * from transfer_request where etat = "En attendre" and univ_origin != "constantine2"')
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
    return

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

if __name__ == "__main__":
    #print(getAllTransferRequests(1))
    #print(getTransferRequests("interne"))
    #print(getAllConditions(4))
    #print(getStudentInfoByEmail("mohamed@gmail.com")[0])
    print(getLastIdOfTable("transfer_request"))
    pass
    
    


#print(studentLogIn("mohamed@gmail.com","mohamed"))
#addTransferRequest(1818,2,12.5,"math","l1","2018","sdf","sdf",0,SUSPENDED,1,1,1,1)
#studentSignUp(1819,"ali@gmail.com","ali","ali","ali","05458796","male","2000")
#addTransferRequest(1819,2,14,"sience","l1","2018","sdf","sdf",1,SUSPENDED,1,1,1,1)
#print(getAllTransferRequests(2))

#studentPasswordReset("mohamed@gmail.com","mohamed3","mohamed4")
#print(studentLogIn("mohamed@gmail.com","mohamed3"))
#adminPasswordReset("admin@gmail.com","admin2","admin")

#closeConnection()
