import sqlite3
con = sqlite3.connect('app_data.db')
cursor = con.cursor()

READY = "ready"
SUSPENDED = "suspended"
REJECTED = "rejected"
ACCEPTED = "accepted"

print("test running...")


#etudiant(matricule,email,password,nom,prenom,telephone,sexe,date_naissance)
#faculte(id autoInc,name)
#departement(id autoInc,nom,id_fac)
#orientation_deadline(id autoInc,start,finish)
#transfer_deadline(id autoInc,start,finish)
#transfer(matricule,id_transfer,moyen_bac,filiere_bac,niveau-etude,date_premier_insc,formation,univ_origin,conge_academic,etat,choix1...)
#orientation(matricule,id_orientation,niveau-etude,date_premier_insc,etat,choix1...)
#specialite(id autoInc, name, niveau, orientation_places, transfer_places, id_dep, id_fac)
#notification(id autoInc, matricule, message)
#condition(id autoInc, cond, type)

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
        print("user already exists")
        return None
    else:
        print("signed up successfully")
        con.commit()
        return 'ok'
        
#orientation_deadline(id autoInc,start,finish)
def setOrientationDeadline():
    return

def setTransferDeadline():
    return

def setTransferRequestState():
    return

def addCondition():
    return

def deleteCondition():
    return

def updateCondition():
    return




def closeConnection():
    print("closing connection...")
    con.close

