from flask import Flask, Response, request, render_template
import flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import pickledb


# Application configs
app = Flask(__name__)
appDebugMode = True
service_port = 5000

# Database details
dbName = 'biturlMap.db'
urlDB = pickledb.load(dbName, True)
urlDB.set('g', 'https://google.com')
urlDB.set('fb', 'https://facebook.com')

# Statics
url_not_found_msg = "URL Not Found"
shortenerFormLocation = 'shortenerForm.html'
welcomeHTML = 'Welcome to url shortener'

# Form configurations
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
class ShortenerForm(FlaskForm):
    short = StringField('short', validators=[DataRequired()])
    long = StringField('long', validators=[DataRequired()])
    submit = SubmitField('Create Short URL')


# Rate limiting configs
rate_limit_day = 20 # Per second for a particular url
rate_limit_hour = 10
rate_limit_minute = 15
rate_limit_urlCreate = 1000
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["{} per day".format(rate_limit_day), "{} per hour".format(rate_limit_hour), "{} per minute".format(rate_limit_minute)]
)


# Index page. No functionality
@app.route('/')
@limiter.exempt
def index():
    return welcomeHTML

# Get a url
@app.route('/<short>/', methods=['GET'])
def redirectUrl(short):
    if urlDB.exists(short):
        return flask.redirect(urlDB.get(short))
    else:
        return url_not_found_msg

# Create a new short url
@app.route('/createUrl', methods=['GET', 'POST'])
@limiter.limit("{} per day".format(rate_limit_urlCreate))
def createUrl():
    form = ShortenerForm()
    if form.validate_on_submit():
        urlDB.set(str(form.short.data), str(form.long.data))
        return render_template(shortenerFormLocation, form = form)
    return render_template(shortenerFormLocation, form = form)


if __name__ == '__main__':
    app.run(debug=appDebugMode, port=service_port)
