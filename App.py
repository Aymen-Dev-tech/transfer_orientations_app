from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
import database_api as db
app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('admin/500.html'), 500


@app.route('/', methods = ["POST", "GET"])
def index():
    #get info from the form 
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        #fetch from db
        if password == "admin":
            if db.adminLogIn(email, password) != None:
                return redirect(url_for('index_admin'))  
            else:
                return render_template('login.html')
        else:
            #Student dashboard
            pass
    return render_template('login.html')


@app.route('/connecter')
def login():
    return render_template('login.html')


@app.route('/admin', methods = ["POST", "GET"])
def index_admin():
    return render_template('admin/index.html')


@app.route('/admin/transfer_interne')
def transferInterne():
    return render_template('admin/transfer_interne.html')


@app.route('/admin/transfer_externe')
def transferExterne():
    return render_template('admin/transfer_externe.html')


@app.route('/admin/orientations')
def orientations():
    return render_template('admin/orientations.html')


@app.route('/admin/conditions')
def conditions():
    return render_template('admin/conditions_orientation.html')


@app.route('/admin/parametres')
def parametres():
    return render_template('admin/parametres.html')


@app.route('/admin/demande_details/<id_transfer>')
def transferInterneDetails(id_transfer):
    return render_template('admin/demande_details.html',id_transfer=id_transfer)


@app.route('/admin/profile')
def profile():
    return render_template('admin/profile.html')

if __name__ == ("__main__"):
    app.run(debug=True)
