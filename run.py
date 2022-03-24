from flask import Flask
from flask import render_template
from flask import make_response, abort
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)