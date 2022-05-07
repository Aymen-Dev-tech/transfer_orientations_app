from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('admin/500.html'), 500


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/connecter')
def login():
    return render_template('login.html')


@app.route('/admin')
def index_admin():
    return render_template('admin/index.html')


@app.route('/admin/transfer_interne')
def transferInterne():
    return render_template('admin/transfer_interne.html')


@app.route('/admin/demande_details/<id_transfer>')
def transferInterneDetails(id_transfer):
    return render_template('admin/demande_details.html',id_transfer=id_transfer)


@app.route('/admin/profile')
def profile():
    return render_template('admin/profile.html')


@app.route('/user/<name>')
def user(name):
    return render_template('admin/user.html', name=name)

if __name__ == ("__main__"):
    app.run(debug=True)
