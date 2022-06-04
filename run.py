import pypyodbc
from flask import Flask, redirect, url_for, request
from flask import render_template
from flask import make_response, abort
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os
#from flask import Mail
import azurecred
from AzureDB import AzureDB

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
OAUTHLIB_INSECURE_TRANSPORT = 1
github_blueprint = make_github_blueprint(
    client_id = "8fc2322c96b258571441",
    client_secret = "e971030f33d961eea6163cdce85145bc7a826414"
)
app.register_blueprint(github_blueprint, url_prefix = '/github_login')

class AzureDB:


    dsn = 'DRIVER=' + azurecred.AZDBDRIVER + ';SERVER=tcp:' + azurecred.AZDBSERVER + ';PORT=1433;DATABASE = '+azurecred.AZDBNAME+';UID =w12'+';PWD =Haslo123'

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT name,text from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT name, text from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit(1)

    def azureAddData(self):
        # cname: str = request.form.get('cname')
        # comment: str = request.form.get('comment')
        self.cursor.execute("""INSERT INTO data (name, text) VALUES (?,?)""",
                            (request.form.get('cname'), request.form.get('comment')))
        self.conn.commit()
#mail = Mail(app)
#
# app.config('MAIL_SERVER') = 'smtp.gmail.com'
# app.config('MAIL_PORT') =   465
# app.config('MAIL_USERNAME') = 'yourId@gmail.com'
# app.config('MAIL_PASSWORD') = '*****'
# app.config('MAIL_USE_TLS') = False
# app.config('MAIL_USE_SSL') = True
# mail = Mail(app)

@app.route('/error_denied')
def error_denied():
    abort(401)

@app.route('/error_internal')
def error_internal():
    return render_template('template.html', name='ERROR 505'), 505

@app.route('/error_not_found')
def error_not_found():
    response = make_response(render_template('template.html', name='ERROR 404'), 404)
    response.headers['X-Something'] = 'A value'
    return response

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return render_template('index.html')
    return '<h1>Request failed!</h1>'

@app.route("/index")
def homePage():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')
@app.route("/guests")
def guests():
    # with AzureDB() as a:
    #     data = a.azureGetData()
    # return render_template("guests.html", data = data)
    return render_template('guests.html')


if __name__ == '__main__':
    app.run(debug=True)
